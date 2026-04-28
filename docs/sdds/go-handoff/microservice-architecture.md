---
spec-version: 1.0
target-implementation: Go
stack: PostgreSQL 17 + pgx + sqlc | Chi HTTP | REST | go-redis | pgvector-go
source: GRO-617 — Canary Go rebuild
status: handoff-ready
---

# Canary — Microservice Architecture

## Governing principle

Each microservice is an independently deployable Go binary. It owns its domain, exposes a REST API, reads and writes only its own tables, and communicates with peers via HTTP. No shared in-process state. No direct cross-service database reads. The pipeline is event-driven via Valkey streams; the rest of the system is request/response REST.

---

## Service map

```
                        ┌─────────────────────────────────────────┐
                        │           External POS systems           │
                        │    (Square webhooks / Counterpoint poll) │
                        └────────────────┬────────────────────────┘
                                         │
                              ┌──────────▼──────────┐
                              │   canary-gateway     │  :8080
                              │  Webhook receipt     │
                              │  HMAC verify         │
                              │  Stream write        │
                              └──────────┬──────────┘
                                         │ Valkey stream: canary:events
                              ┌──────────▼──────────┐
                              │    canary-tsp        │  :8081
                              │  4-stage pipeline    │
                              │  seal→parse→merkle   │
                              │  →detect trigger     │
                              └──────┬────────┬─────┘
                                     │        │ Valkey stream: canary:detection
                          writes     │        └─────────────┐
                          sales.*    │               ┌───────▼──────┐
                                     │               │ canary-chirp │  :8082
                                     │               │ Rule eval    │
                                     │               │ Alert create │
                                     │               └───────┬──────┘
                                     │                       │ REST POST /alerts
                                     │               ┌───────▼──────┐
                                     │               │ canary-alert │  :8083
                                     │               │ Alert CRUD   │
                                     │               │ Lifecycle SM │
                                     │               └───────┬──────┘
                                     │                       │ REST POST /cases
                                     │               ┌───────▼──────┐
                                     │               │  canary-fox  │  :8084
                                     │               │ Case mgmt    │
                                     │               │ Evidence     │
                                     │               │ Hash chain   │
                                     │               └──────────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                       │
    ┌─────────▼──────┐   ┌───────────▼──────┐   ┌──────────▼──────┐
    │  canary-owl    │   │canary-analytics  │   │canary-identity  │
    │  :8085         │   │  :8086           │   │  :8087          │
    │ pgvector search│   │ Metric rollups   │   │ Auth / tenants  │
    │ Risk Dictionary│   │ Risk scoring     │   │ OAuth / sessions│
    │ EJ Spine       │   │ Baselines        │   │                 │
    └────────────────┘   └──────────────────┘   └─────────────────┘

              POS Adapter layer (one binary per POS):
    ┌─────────────────┐   ┌────────────────────┐
    │  canary-hawk    │   │   canary-bull       │
    │  :8090          │   │   :8091             │
    │ Square adapter  │   │ Counterpoint adapter│
    │ OAuth + webhooks│   │ API key + polling   │
    └─────────────────┘   └────────────────────┘
```

---

## Services

### canary-gateway — Webhook Gateway
**Port:** 8080
**Role:** The only public-facing ingress point for POS events. Receives webhooks, verifies HMAC signatures, deduplicates, and writes to the ingestion stream. Does not touch the database directly.

**REST API:**
```
POST /webhooks/square          — Square webhook receiver
POST /webhooks/counterpoint    — Counterpoint event receiver (polling adapter pushes here)
GET  /health                   — Liveness probe
```

**Request contract (all webhook endpoints):**
```
Headers:
  X-Signature:   HMAC-SHA256 hex digest of request body
  X-Merchant-Id: POS-native merchant/location identifier
  Content-Type:  application/json

Response 200: {"received": true, "event_id": "<uuid>"}
Response 400: {"error": "invalid_signature"}
Response 409: {"error": "duplicate_event", "event_id": "<existing-uuid>"}
Response 503: {"error": "stream_unavailable"}
```

**Valkey writes:**
- Stream: `canary:events` — one message per verified event
- Dedup key: `canary:dedup:<sha256(body)>` — SET NX, TTL 24h

**Tables owned:** none (stateless)

**Dependencies:** Valkey (stream write only)

---

### canary-tsp — Transaction Stream Processor
**Port:** 8081
**Role:** Consumes `canary:events`, runs 4 pipeline stages (seal → parse → merkle → detect-trigger), writes to `sales.*` schema, publishes detection-ready events to `canary:detection`. This service is the data spine of the system.

**REST API:**
```
GET  /health          — Liveness
GET  /status          — Pipeline stage lag metrics
POST /replay/:event_id — Replay a specific event (ops use only, requires admin token)
```

**Pipeline stages:**

| Stage | Consumer group | Input | Output | Idempotent |
|---|---|---|---|---|
| 1 — Seal | `tsp:seal` | `canary:events` | `app.ingestion_log`, chain hash | YES — unique constraint on event_id |
| 2 — Parse | `tsp:parse` | `canary:events` (ACK after seal) | `sales.*` rows | YES — upsert on external_id + merchant_id |
| 3 — Merkle | `tsp:merkle` | batch accumulator | `app.merkle_batches` | YES — batch_id idempotency |
| 4 — Detect | `tsp:detect` | `canary:events` | `canary:detection` stream | YES — stream message dedup |

**Tables owned:** `sales.transactions`, `sales.refund_links`, `sales.line_items`, `sales.line_item_discounts`, `sales.cash_drawer_shifts`, `sales.cash_drawer_events`, `app.ingestion_log`, `app.merkle_batches`

**Dependencies:** PostgreSQL (sales schema), Valkey (streams), canary-identity (merchant context lookup on startup)

---

### canary-chirp — Detection Engine
**Port:** 8082
**Role:** Consumes `canary:detection` stream. Evaluates Chirp rules against transaction data. Creates alerts via canary-alert REST API. Stateless evaluation — all state is in the database.

**REST API:**
```
GET  /health                    — Liveness
GET  /rules                     — List all active rules and their thresholds
GET  /rules/:rule_id            — Get single rule definition
POST /rules/:rule_id/evaluate   — Force-evaluate a rule for a merchant (ops use)
```

**Rule evaluation contract:**
- Pulls threshold config from `app.merchant_rule_configs` (merchant-level override) → `app.location_rule_configs` (location-level override) → `app.detection_rules` (global default)
- Executes rule SQL contract against `sales.*` schema
- On violation: POST to canary-alert `/alerts`

**Tables owned:** `app.detection_rules`, `app.merchant_rule_configs`, `app.location_rule_configs`

**Dependencies:** PostgreSQL (sales schema reads, app schema reads), Valkey (canary:detection stream), canary-alert (POST /alerts)

---

### canary-alert — Alert Service
**Port:** 8083
**Role:** Alert lifecycle management. Owns alert creation, state transitions, history, and dismissal. The authoritative record of what Chirp detected.

**REST API:**
```
POST   /alerts                        — Create alert (called by canary-chirp)
GET    /alerts?merchant_id=&severity=&status=&from=&to=  — List alerts
GET    /alerts/:id                    — Get alert
PATCH  /alerts/:id/acknowledge        — Transition: OPEN → ACKNOWLEDGED
PATCH  /alerts/:id/investigate        — Transition: ACKNOWLEDGED → INVESTIGATING
PATCH  /alerts/:id/dismiss            — Transition: any → DISMISSED
PATCH  /alerts/:id/escalate           — Transition: any → ESCALATED (creates Fox case)
GET    /alerts/:id/history            — Alert state history

Request body for state transitions:
{
  "actor_id": "<user-uuid>",
  "note": "optional human note"
}

Response: full alert object with current state
```

**Alert state machine:**
```
OPEN → ACKNOWLEDGED → INVESTIGATING → DISMISSED
                   ↘              ↗
                    → ESCALATED (triggers Fox case creation)
```

**Tables owned:** `app.alerts`, `app.alert_history`

**Dependencies:** PostgreSQL, canary-fox (POST /cases on ESCALATED transition)

---

### canary-fox — Case Management
**Port:** 8084
**Role:** Investigation case lifecycle. Evidence hash chain. Append-only timeline. The legal record of what happened and what was done about it.

**REST API:**
```
POST   /cases                          — Open a case (called by canary-alert on escalation)
GET    /cases?merchant_id=&status=     — List cases
GET    /cases/:id                      — Get case with timeline
PATCH  /cases/:id/status               — Transition case status
POST   /cases/:id/evidence             — Add evidence record (append-only)
POST   /cases/:id/timeline             — Add timeline event
GET    /cases/:id/evidence/:record_id  — Get single evidence record
GET    /cases/:id/chain                — Verify hash chain integrity
```

**Hash chain invariant:**
- Every `evidence_records` INSERT computes `chain_hash = SHA256(record_payload || prev_chain_hash)`
- A DB trigger blocks all UPDATE and DELETE on `evidence_records` — the trigger DDL is in fox.md and must be deployed
- `GET /cases/:id/chain` recomputes and verifies the full chain on demand

**Tables owned:** `app.fox_cases`, `app.fox_timeline`, `app.fox_evidence`, `app.fox_subjects`

**Dependencies:** PostgreSQL

---

### canary-owl — Intelligence and Search
**Port:** 8085
**Role:** pgvector-powered semantic search over merchant data. Risk Dictionary lookup. EJ (Employee Journey) Spine entity resolution. All vector ops go through PostgreSQL/pgvector — no external vector database.

**REST API:**
```
POST   /search                  — Semantic search
       Body: {"query": "...", "merchant_id": "...", "limit": 10, "filters": {...}}
       Response: [{id, content, similarity, entity_type, metadata}]

GET    /risk-dictionary/:entity_id   — Risk profile for an entity
GET    /ej-spine/:employee_id        — Employee journey spine (full activity graph)
POST   /embed                        — Generate embedding for a text string
       Body: {"text": "..."}
       Response: {"embedding": [1024 floats]}

GET    /health
```

**Vector search SQL contract:**
```sql
SELECT
    id,
    content,
    entity_type,
    metadata,
    1 - (embedding <=> $1) AS similarity
FROM app.owl_chunks
WHERE merchant_id = $2
  AND entity_type = ANY($3)
ORDER BY embedding <=> $1
LIMIT $4
```

**Embedding generation:** POST to embedding service at `EMBEDDING_SERVICE_URL/api/embeddings`. Model: `qwen3-embedding:8b`, dimensions: 1024.

**Tables owned:** `app.owl_chunks`, `app.owl_sessions`, `app.risk_scores`, `app.risk_score_history`

**Dependencies:** PostgreSQL (pgvector), embedding service (HTTP)

---

### canary-analytics — Metrics and Risk Scoring
**Port:** 8086
**Role:** Scheduled metric rollups, entity risk scoring, baseline computation. Reads from `sales.*`, writes to `metrics.*`. No user-facing reads — serves as the metrics write engine. Dashboard queries go to the database directly or via canary-owl.

**REST API:**
```
GET  /health
POST /rollup/daily    — Trigger daily rollup (normally cron-driven)
POST /rollup/hourly   — Trigger hourly rollup
POST /score/:merchant_id  — Recompute risk scores for a merchant
GET  /status          — Last run times and row counts for each job
```

**Scheduled jobs:**

| Job | Trigger | Input | Output table |
|---|---|---|---|
| hourly-rollup | Every hour, :05 | `sales.transactions` last 2h | `metrics.hourly_rollups` |
| daily-rollup | 02:00 UTC | `sales.transactions` yesterday | `metrics.daily_rollups` |
| employee-rollup | 02:30 UTC | `sales.transactions` yesterday | `metrics.employee_rollups` |
| risk-scoring | 03:00 UTC | `metrics.*_rollups` | `metrics.entity_risk_scores` |
| baseline-update | Sunday 04:00 UTC | 90-day window | `metrics.metric_baselines` |

**Tables owned:** `metrics.*` (all metrics schema tables)

**Dependencies:** PostgreSQL (reads sales.*, writes metrics.*)

---

### canary-identity — Identity and Auth
**Port:** 8087
**Role:** Merchant registration, user management, OAuth flows, session tokens. The authentication authority for the entire system. Every other service validates tokens by calling canary-identity or by verifying a shared JWT secret.

**REST API:**
```
POST   /merchants                    — Register merchant
GET    /merchants/:id                — Get merchant
PATCH  /merchants/:id                — Update merchant

POST   /oauth/authorize              — Begin OAuth flow
GET    /oauth/callback               — OAuth callback
POST   /oauth/refresh                — Refresh access token
DELETE /oauth/disconnect             — Disconnect POS

POST   /sessions                     — Create session (login)
DELETE /sessions/:token              — Invalidate session (logout)
POST   /sessions/validate            — Validate session token
       Body: {"token": "..."}
       Response 200: {"valid": true, "merchant_id": "...", "user_id": "...", "roles": [...]}
       Response 401: {"valid": false}

POST   /users                        — Create user
GET    /users/:id
PATCH  /users/:id
GET    /health
```

**Session contract:**
- Sessions are JWT tokens, signed with `SESSION_SECRET`
- Payload: `{merchant_id, user_id, roles[], iat, exp}`
- TTL: 8 hours (configurable)
- Storage: Valkey SET with key `session:<token_hash>` for fast invalidation

**Tables owned:** `app.merchants`, `app.users`, `app.merchant_sources`, `app.merchant_settings`, `app.oauth_states`

**Dependencies:** PostgreSQL, Valkey (session store)

---

### canary-hawk — Square Adapter
**Port:** 8090
**Role:** Square POS adapter. Handles Square OAuth, webhook signature verification, and event normalization to the Canary CRDM. Pushes normalized events to canary-gateway.

**REST API:**
```
GET  /health
POST /webhooks/inbound       — Receives Square webhooks (registered with Square)
GET  /oauth/connect          — Begin Square OAuth
GET  /oauth/callback         — Square OAuth callback
POST /sync/pull              — Trigger manual pull sync (ops use)
GET  /sync/status            — Last sync watermarks
```

**Auth model:** Square OAuth 2.0. Tokens stored in `app.hawk_oauth_tokens`. Refresh handled automatically before expiry.

**Webhook verification:** `HMAC-SHA256` of request body using Square webhook signature key. Header: `X-Square-Hmacsha256-Signature`.

**Tables owned:** `app.hawk_oauth_tokens`, `app.hawk_webhook_subscriptions`, `app.hawk_sync_cursors`, `app.hawk_event_log`, and 4 additional Square-specific staging tables (see hawk.md).

**Dependencies:** Square API (external), canary-gateway (POST /webhooks/square), canary-identity (merchant lookup), PostgreSQL

---

### canary-bull — Counterpoint Adapter
**Port:** 8091
**Role:** NCR Counterpoint adapter. API key auth (no OAuth). Polling model — Counterpoint has no native webhooks. Polls Counterpoint REST API on configurable interval, normalizes to CRDM, pushes to canary-gateway.

**REST API:**
```
GET  /health
POST /merchants/:id/connect     — Register API key for a merchant
DELETE /merchants/:id/connect   — Remove credentials
GET  /merchants/:id/sync/status — Last poll watermarks and lag
POST /merchants/:id/sync/pull   — Force immediate poll
```

**Auth model:** API key per merchant, stored encrypted in `app.bull_api_credentials`. Header: `APIKey <key>` on all Counterpoint requests.

**Poll cycle:**
1. Read watermark from `app.bull_poll_watermarks`
2. GET Counterpoint `/Documents` (and other endpoints) with `ModifiedDate >= watermark`
3. Normalize each document to CRDM
4. POST to canary-gateway `/webhooks/counterpoint`
5. Update watermark

**Default poll interval:** 5 minutes (configurable per merchant via `app.bull_merchant_config`).

**Tables owned:** `app.bull_api_credentials`, `app.bull_poll_watermarks`, `app.bull_merchant_config`, `app.bull_event_log`

**Dependencies:** NCR Counterpoint REST API (external), canary-gateway (POST /webhooks/counterpoint), canary-identity (merchant lookup), PostgreSQL

---

## Inter-service communication

### Synchronous (REST)

| Caller | Callee | Call |
|---|---|---|
| canary-chirp | canary-alert | POST /alerts |
| canary-alert | canary-fox | POST /cases (on escalation) |
| canary-hawk | canary-gateway | POST /webhooks/square |
| canary-bull | canary-gateway | POST /webhooks/counterpoint |
| All services | canary-identity | POST /sessions/validate |

### Asynchronous (Valkey streams)

| Stream | Producer | Consumer |
|---|---|---|
| `canary:events` | canary-gateway | canary-tsp |
| `canary:detection` | canary-tsp (stage 4) | canary-chirp |

---

## Authentication between services

All internal REST calls carry a service token in the `Authorization` header:

```
Authorization: Bearer <service-jwt>
```

Service JWTs are signed with `INTERNAL_SERVICE_SECRET` (shared secret, not the user session secret). Each service validates inbound calls from other services using this key. canary-identity validates user-facing session tokens using `SESSION_SECRET`.

External-facing endpoints (canary-gateway webhooks, canary-identity OAuth) use POS-specific auth (HMAC, OAuth).

---

## Database ownership

Each service owns its tables exclusively. No service may write to another service's tables.

| Service | Schema | Tables |
|---|---|---|
| canary-tsp | sales.* | transactions, refund_links, line_items, line_item_discounts, cash_drawer_shifts, cash_drawer_events |
| canary-tsp | app | ingestion_log, merkle_batches |
| canary-chirp | app | detection_rules, merchant_rule_configs, location_rule_configs |
| canary-alert | app | alerts, alert_history |
| canary-fox | app | fox_cases, fox_timeline, fox_evidence, fox_subjects |
| canary-owl | app | owl_chunks, owl_sessions, risk_scores, risk_score_history |
| canary-analytics | metrics.* | all metrics schema tables |
| canary-identity | app | merchants, users, merchant_sources, merchant_settings, oauth_states |
| canary-hawk | app | hawk_* tables (8) |
| canary-bull | app | bull_* tables (4) |

Cross-service reads (e.g., chirp reading sales.transactions) are permitted read-only and do not violate ownership — ownership means write authority, not read exclusivity.

---

## Health check contract

Every service exposes `GET /health` returning:

```json
{
  "ok": true,
  "service": "canary-chirp",
  "version": "1.0.0",
  "checks": {
    "database": "ok",
    "valkey": "ok"
  }
}
```

On any dependency failure, return HTTP 503 with `"ok": false` and the failing check identified.

---

## Deployment topology

Each service is a standalone Go binary. Deployment target: containerized (one container per service). All services share one PostgreSQL instance and one Valkey instance in the initial deployment. Database connection pools are per-service.

**Recommended connection pool sizing (initial):**

| Service | Max connections |
|---|---|
| canary-tsp | 20 (pipeline throughput) |
| canary-analytics | 5 (scheduled jobs only) |
| canary-owl | 10 (vector queries) |
| All others | 10 |

**Port allocation summary:**

| Service | Port |
|---|---|
| canary-gateway | 8080 |
| canary-tsp | 8081 |
| canary-chirp | 8082 |
| canary-alert | 8083 |
| canary-fox | 8084 |
| canary-owl | 8085 |
| canary-analytics | 8086 |
| canary-identity | 8087 |
| canary-hawk | 8090 |
| canary-bull | 8091 |

---

## Environment variables (required by all services)

```
DATABASE_URL          postgresql://user:pass@host:5432/canary
VALKEY_URL            redis://host:6379
INTERNAL_SERVICE_SECRET  <shared secret for service-to-service JWTs>
LOG_LEVEL             info
```

Service-specific vars are documented in each service's section above and in the individual SDDs.
