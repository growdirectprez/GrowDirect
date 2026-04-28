---
spec-version: 1.0
target-implementation: Go
stack: PostgreSQL 17 + pgx + sqlc | Chi HTTP | REST | go-redis | pgvector-go
source: Curated from Canary Python prototype SDDs (GRO-617)
status: handoff-ready
---

# Canary Architecture

**Type:** Platform Service (Canary index SDD)
**Last reviewed:** 2026-04-13
**Source SDDs:** SDD-045, SDD-047, SDD-048, SDD-049, SDD-050, SDD-051, SDD-052, SDD-053, SDD-054, SDD-057, SDD-059, SDD-060, SDD-062

---

## Purpose

Canary LP is a 7-layer distributed system for AI-powered loss prevention, built on 12+ bounded service domains exposed through MCP servers. The platform processes POS events from multiple providers — Square via webhook push, NCR Counterpoint via poll-based REST — evaluates transactions against detection rules (37 Square-era + 25+ Counterpoint-specific), and surfaces actionable insights through an AI-powered assistant.

This is the **Canary index SDD** — it documents the platform topology, startup order, service dependencies, cross-boundary data flows, and links to all domain-specific SDDs. Individual domain behavior is documented in its own SDD.

### Hawk + Bull Additions (Phase 1+)

Two new service domains join the architecture in Hawk Phase 1:

| Domain | SDD | Sits on | Purpose |
|---|---|---|---|
| **Hawk** | Hawk SDD | Q.5.4 (Fox case workflow) | Incident-typed case management with wizard FSM, dual-track action codes, card factory. Supersedes Fox's flat case lifecycle. |
| **Bull** | Bull SDD | D.4 + D.5 (transfer-loss, distribution recs) | Phase 3 stub — Canary-native Module D intelligence. Gated on Module D substrate. |

Fox remains operational as the evidence-chain backbone (INSERT-only tables, hash-chain triggers). Hawk cases link to Fox via `hawk_cases.fox_case_id` for evidentiary operations.

---

## Dependencies

### Shared Infrastructure

| Service | Purpose |
|---------|---------|
| PostgreSQL 17 | All databases (canary, canary_test, growdirect_memory) |
| Valkey 8 | Sessions, cache, rate limiting, TSP streams |
| pgAdmin | DB administration UI |
| LLM Inference Service (Ollama) | LLM inference (qwen3:14b) + embeddings (qwen3-embedding:8b, 1024-dim) |
| Memory Bus | Platform session memory service (pgvector-backed) |

### Canary Application Services

| Service | Port | Purpose |
|---------|------|---------|
| HTTP Service (primary) | 5001 | Monolith: 29 route groups, 12 MCP server handlers, all business logic |
| Reverse Proxy | 80, 443 | TLS termination, reverse proxy |
| TSP Sub1 (Seal) | — | Message queue stream consumer: hash-seal incoming events |
| TSP Sub2 (Parse) | — | Message queue stream consumer: parse + route + feed detection stream |
| TSP Sub3 (Merkle) | — | Message queue stream consumer: Merkle tree construction |
| TSP Sub4 (Detect) | — | Message queue stream consumer: Chirp rule evaluation |
| Owl MCP | 8001 | Standalone AI/chat MCP server (proof of concept extraction) |
| QA Agent | 8002 | AI Agent SDK sidecar for ops QA |

### Enterprise Stack (QA / future production)

The full enterprise stack is self-contained, with dedicated infrastructure:

| Service | Port | Profile | Purpose |
|---------|------|---------|---------|
| PostgreSQL 17 | 5432 | core | Dedicated Canary instance |
| Valkey 8 | 6379 | core | Dedicated cache/broker |
| PgBouncer | 6432 | core | Connection pooling (transaction mode, max 200 clients) |
| HTTP Service | 5001 | core | Business logic (4 HTTP service instances in enterprise mode) |
| Apache Superset 6 | 8088 | core | Analytics dashboards |
| Apache Airflow 3 | 8793 | core | ETL orchestration, Chirp sweeps |
| Keycloak 26 | 8080 | qa | OIDC identity provider |
| Hasura v2 CE | 8081 | qa | GraphQL/REST auto-generated API |
| Directus 11 | 8055 | qa | Internal admin panel |
| Reverse Proxy | 80 | qa | Reverse proxy |

### External APIs

| API | Auth Method | Purpose |
|-----|------------|---------|
| Square Connect API | OAuth 2.0 (AES-256-GCM encrypted tokens) | Merchant data, transactions, webhooks |
| Square Webhooks | HMAC-SHA256 signature validation | Real-time event push |

---

## Startup Order and Dependency Graph

### Dev Stack

```
1. PostgreSQL         (healthcheck: pg_isready)
2. Valkey             (healthcheck: valkey-cli ping)
   ├── pgAdmin            (depends: postgres healthy)
   ├── LLM Inference      (independent)
   └── Memory Bus         (depends: postgres healthy)
3. Infrastructure sentinel  (waits for postgres + valkey reachability)
4. HTTP Service (primary)   (depends: sentinel, healthcheck: HTTP GET /health)
   Boot phases:
     Phase 1: Database connection pool init (consolidated schema)
     Phase 2: Security middleware registration (CSRF, rate limiting, security headers, session store)
     Phase 3: Route group registration (29 groups, resilient — each try/recover)
     Phase 4: TSP consumer group init, detection rule seeding, audit chain verification
     Phase 5: Boot summary log
5. Reverse Proxy       (depends: HTTP service healthy)
6. TSP Sub{1,2,3,4}   (depends: HTTP service healthy)
7. Owl MCP            (depends: HTTP service healthy)
8. QA Agent           (depends: HTTP service healthy)
```

### Enterprise Stack

```
1. PostgreSQL          (healthcheck: pg_isready)
2. Valkey              (healthcheck: valkey-cli ping)
3. PgBouncer           (depends: postgres healthy)
4. HTTP Service        (depends: postgres healthy + valkey healthy)
5. Airflow scheduler   (depends: postgres healthy)
   Airflow web         (depends: postgres healthy)
   Superset            (depends: postgres healthy + valkey healthy)
6. [qa profile] Keycloak → Hasura → Directus → Reverse proxy
```

### Failure Cascade

| If this goes down... | ...these break |
|---------------------|---------------|
| PostgreSQL | Everything (HTTP service degrades to health-only mode, pipeline consumers stall, Owl MCP returns errors) |
| Valkey | Sessions lost, rate limiting fails open, TSP stream processing halts, Chirp threshold cache stale |
| LLM Inference | Owl AI chat returns errors, ALX embeddings fail, analytics AI features unavailable |
| HTTP Service | All HTTP endpoints down; pipeline consumers continue processing independently but cannot write alerts without HTTP service health |
| Reverse Proxy | External HTTPS access lost; direct service port still reachable |
| Any TSP consumer | That processing stage stalls; upstream/downstream consumers continue; dead letter stream catches failures |

---

## Data Flow & PII Map

### Database Architecture

| Database | Schema | Tables | Write Pattern |
|----------|--------|--------|---------------|
| `canary` | `app` | ~40 | CRUD with soft delete + audit trail |
| `canary` | `sales` | ~19 | IMMUTABLE (PostgreSQL trigger-enforced, no UPDATE/DELETE) |
| `canary` | `metrics` | ~20 | Aggregation (fully re-derivable from sales) |
| `growdirect_memory` | `memory` | ~2 | pgvector embeddings (1024-dim HNSW cosine) |

**Database session contract:** Single connection pool, three schemas. Row-Level Security (RLS) is activated at the start of every transaction by calling `set_current_merchant(:mid)` via a connection pool event listener on `begin`. All inserts across all three schemas are schema-qualified.

### PII Classification (Platform-Level Cross-Boundary Flows)

| Data Category | Fields | Classification | Storage | Encryption | Crosses Boundary To |
|--------------|--------|----------------|---------|------------|-------------------|
| OAuth tokens | `access_token`, `refresh_token` | **restricted** | `app.merchant_sources` | AES-256-GCM | Square API (HTTP), Owl MCP |
| Merchant identity | `business_name`, `merchant_id` | internal | `app.merchants` | plaintext | All services, UI, analytics |
| Square merchant ID | `square_merchant_id` | internal | `app.merchant_sources` | plaintext | TSP pipeline, webhooks |
| Transaction data | `customer_id`, `tender_id`, amounts | internal | `sales.*` (immutable) | plaintext | Chirp (detection), Owl (analysis), Fox (cases) |
| Employee data | `employee_id`, `first_name`, `last_name` | **sensitive** | `app.employees` | plaintext | Chirp alerts, Fox cases, analytics |
| Location data | `address`, `name` | internal | `app.locations` | plaintext | UI, analytics |
| Alert content | `description`, linked txn/employee IDs | internal | `app.alerts` | plaintext | Notifications (email stub), Fox cases |
| Case evidence | screenshots, notes, txn references | internal | `app.fox_cases` + evidence locker | plaintext | Owl analysis |
| Session data | `session_id`, `merchant_id` | internal | session store | plaintext | Request context |
| AI chat history | merchant questions, Owl responses | internal | Valkey (ephemeral) + ALX memory | plaintext | LLM inference |
| Webhook payloads | raw Square event JSON (may contain customer PII) | **sensitive** | `sales.raw_webhooks` | plaintext | TSP Sub1-4 |
| Detection results | rule match details, severity scores | internal | `app.alerts`, `metrics.*` | plaintext | UI, notifications |
| Notification log | channel, status, recipient metadata | internal | `app.notification_log` | plaintext | Email (stub), SMS (stub) |

### Data Flow Diagram

```
Square Webhooks (HMAC-SHA256 validated)
  │
  ▼
HTTP Service /webhooks/square (TSP publisher)
  │
  ├──▶ Valkey stream canary:events
  │     │
  │     ├──▶ Sub1 (Seal): hash + write to sales.raw_webhooks
  │     ├──▶ Sub2 (Parse): parse JSON → sales.transactions + emit canary:detection
  │     ├──▶ Sub3 (Merkle): build Merkle tree for integrity chain
  │     └──▶ Sub4 (Detect): Chirp rule evaluation → app.alerts → notifications
  │
  ├──▶ Owl MCP (:8001) → LLM Inference (qwen3:14b) → AI chat responses
  │     └──▶ ALX Memory (pgvector) → institutional knowledge retrieval
  │
  └──▶ UI Layer → Browser
        ├── Dashboard (analytics from metrics.*)
        ├── Chirps (alert feed from app.alerts)
        ├── Fox (cases from app.fox_cases)
        └── Owl (AI chat, SSE streaming)
```

---

## API Contract

### MCP Server Registry (12 servers, 84 tools)

Each domain exposes four standard endpoints:

- `GET /{prefix}/manifest` — server manifest (JWT required, 100/hr)
- `GET /{prefix}/tools` — list available tools (JWT required, 100/hr)
- `POST /{prefix}/tools/<name>` — invoke a tool (JWT required, 1000/hr)
- `GET /{prefix}/health` — service health (public, no auth)

Response envelope: `{"tool": name, "ok": true/false, "result"|"error": ..., "timestamp": ISO}`

| # | Domain | Prefix | Tools | SDD | Description |
|---|--------|--------|-------|-----|-------------|
| 1 | Identity | `/identity` | 6 | Identity SDD | Merchants, users, roles, Square OAuth, tenant context |
| 2 | TSP | `/tsp` | 6 | TSP SDD | Webhook intake, stream processing, parsing |
| 3 | Chirp | `/chirp` | 10 | Chirp SDD | Detection rules, threshold config, sensitivity presets |
| 4 | Alert | `/alert` | 6 | Alert SDD | Alert lifecycle, history, impact scoring, notifications |
| 5 | Owl | `/owl` | 8 | Owl SDD | AI chat, personalities, MCP tools, merchant memory |
| 6 | Fox | `/fox` | 8 | Fox SDD | Evidence locker, hash-chained timeline (EBR class inside Hawk) |
| 6b | Hawk | `/hawk` | 9 | Hawk SDD | Incident-typed case management, wizard FSM, card factory |
| 7 | Analytics | `/analytics` | 7 | Analytics SDD | Dashboard metrics, heatmaps, velocity baselines |
| 8 | ALX | `/alx` | 7 | ALX SDD | Institutional memory (pgvector, 954+ memories) |
| 9 | RaaS | `/raas` | 7 | RaaS SDD | Namespace resolution, merchant onboarding |
| 10 | Ops | `/ops` | 8 | Ops SDD | Health check runner, simulator, Chirp Lab |
| 11 | BFF | `/bff` | 4 | UI/BFF SDD | Desktop + mobile rendering, feature flags |
| 12 | Condor | `/condor` | 7 | — | Industry benchmarks, regulatory intelligence |

Additional MCP servers (non-domain, standalone):
- **Atlas** (`/atlas`) — diagram service (GRO-323)
- **Owl MCP** (`:8001`) — standalone extraction of Owl, same tools as monolith `/owl/*`
- **QA Agent** (`:8002`) — AI Agent SDK sidecar, proxied via `/ops/qa/chat`

### Route Registry (29 route groups)

| Route Group | Prefix | Auth | CSRF Exempt | Description |
|-------------|--------|------|:-----------:|-------------|
| Health | `/health` | None | Yes | Health checks |
| Auth | `/auth` | Session | No | Keycloak auth |
| Webhooks TSP | `/webhooks` | HMAC | Yes | Square webhook receiver |
| Fox | `/api/fox` | JWT | Yes | Fox case CRUD |
| Alerts | `/api/alerts` | JWT | Yes | Alert CRUD |
| Chirp | `/api/chirp` | JWT | Yes | Chirp config CRUD |
| Square OAuth | `/oauth` | Session | Yes | Square OAuth flow |
| Merchants | `/api/merchants` | JWT | Yes | Merchant CRUD |
| Locations | `/api/locations` | JWT | Yes | Location CRUD |
| Employees | `/api/employees` | JWT | Yes | Employee CRUD |
| Analytics | `/api/analytics` | JWT | Yes | Analytics queries |
| Receipt TSP | `/api/receipt` | JWT | Yes | Receipt proof |
| Square Explorer | — | JWT | Yes | Square Capability Explorer |
| Views | — | Session | No | Desktop UI (server-rendered templates) |
| DevOps Monitor | `/devops` | JWT | Yes | DevOps pipeline monitor |
| Ops Console | `/ops` | JWT | Yes | Operations console |
| Charts | `/api/charts` | JWT | Yes | Dashboard chart APIs |
| 12 MCP route groups | `/{domain}` | JWT | Yes | See MCP registry above |

---

## Operations

### Startup Sequence

Key behavioral requirements:

1. **Infrastructure must be reachable before the HTTP service starts.** PostgreSQL and Valkey connectivity are prerequisites.
2. **Route registration is resilient.** Each route group loads independently via try/recover. A missing handler degrades one domain, not the whole service. The service can run in "health-only mode" if the database is unreachable.
3. **TSP consumer groups** are initialized during service startup. If Valkey is unreachable, consumers will not receive events until groups are manually created.
4. **Detection rules** are seeded on first boot (idempotent).
5. **Audit hash chain** is verified on startup. A tampered chain logs CRITICAL but does not block startup (fail-open). Fail-closed in production is the recommended target state.

### Health Checks

| Service | Endpoint | Method | Interval | Timeout |
|---------|----------|--------|----------|---------|
| HTTP Service | `http://localhost:5001/health` | HTTP GET | 10s | 5s |
| Reverse Proxy | `http://localhost/nginx-health` | HTTP GET | 10s | 3s |
| TSP Sub{1-4} | Script-based check | CMD | 15s | 5s |
| Owl MCP | `http://localhost:8001/health` | HTTP GET | 10s | 5s |
| QA Agent | `http://localhost:8002/health` | HTTP GET | 10s | 5s |
| PostgreSQL | `pg_isready` | CMD-SHELL | 5s (dev) / 10s (enterprise) | 5s |
| Valkey | `valkey-cli ping` | CMD | 5s (dev) / 10s (enterprise) | 5s |

### Failure Modes

| Failure | Detection | Behavior | Recovery |
|---------|-----------|----------|----------|
| PostgreSQL down | HTTP service health returns 503 | Service enters health-only mode; CRUD endpoints return 500 | Auto-reconnect via connection pool health checks |
| Valkey down | Rate limiting fails open | Sessions lost (users re-auth); TSP streams stall; threshold cache stale but usable (300s TTL) | Consumers retry on reconnect |
| LLM Inference down | Owl health returns unhealthy | AI chat returns error; embeddings fail; detection rules continue (no AI dependency) | Restart inference service |
| TSP consumer crash | Healthcheck fails | Container/process restarts; unprocessed messages remain in stream | Consumer resumes from last ACK |
| Route group import failure | Logged at startup | Single domain degraded; all other domains continue | Fix import, restart service |
| Audit chain tampered | CRITICAL log on startup | Continues running (fail-open) | Investigate chain, rebuild if needed |

### Configuration (Environment Variables)

| Variable | Required | Default | Purpose |
|----------|:--------:|---------|---------|
| `SECRET_KEY` | Prod: Yes | — | Session signing key (must not fall back in production) |
| `CANARY_ENV` | No | `development` | Environment: development/testing/production |
| `CANARY_DB_URL` | Yes | — | PostgreSQL connection string |
| `VALKEY_URL` | Yes | — | Valkey connection string (session store) |
| `CANARY_ENCRYPTION_KEY` | Prod: Yes | — | AES-256-GCM key (base64-encoded 32 bytes) |
| `CANARY_HOST` | No | — | Hostname for HTTPS enforcement decision |
| `SQUARE_APPLICATION_ID` | Yes | — | Square OAuth app ID |
| `SQUARE_APPLICATION_SECRET` | Yes | — | Square OAuth secret |
| `SQUARE_WEBHOOK_SIGNATURE_KEY` | Yes | — | HMAC-SHA256 webhook validation key |
| `OWL_URL` | No | `http://ollama:11434` | LLM inference endpoint |
| `OWL_MODEL` | No | `qwen3:14b` | LLM model for AI chat |
| `CANARY_MEMORY_DB_URL` | No | — | Memory bus PostgreSQL connection |
| `VALKEY_STREAM` | No | `canary:events` | TSP primary stream name |
| `VALKEY_STREAM_DB` | No | `4` | Valkey logical store for TSP streams |
| `QA_AGENT_URL` | No | `http://qa-agent:8002` | QA Agent sidecar endpoint |
| `CANARY_DEV_JWT_SECRET` | Dev only | — | JWT signing secret for dev/test |

---

## Deployment

### Service Topology (Dev)

8 services total (+ 1 sentinel). All pipeline consumers share the same application image as the primary HTTP service. Owl MCP and QA Agent use separate images.

**Boot command:** `./devops/scripts/dev.sh up`

### Service Topology (QA)

6 services: HTTP service + 4 pipeline consumers + test runner (profile). No reverse proxy (direct access). No Owl MCP or QA Agent in QA yet.

### AWS Target Architecture

| Component | Dev/Current | AWS Target |
|-----------|-------------|-----------|
| HTTP Service | Local container | ECS Fargate (1 vCPU, 512MB) |
| Pipeline consumers (TSP) | Local containers | ECS Fargate (4 tasks) |
| PostgreSQL | Shared local instance | RDS PostgreSQL 17 (db.t4g.micro) |
| Valkey | Shared local instance | ElastiCache Valkey (cache.t4g.micro) |
| LLM Inference | Local container | Mac Studio (local) or Bedrock fallback |
| Secrets | Environment files | AWS Secrets Manager |
| TLS | Cloudflare Tunnel | ALB + ACM |
| DNS | Cloudflare | Route 53 + Cloudflare CDN |

Infrastructure phases: Phase 1 (local lab, ~$10/mo), Phase 2 (hybrid: RDS + local inference, ~$100-150/mo), Phase 3 (full AWS: ECS Fargate + Bedrock, ~$205/mo).

### CI/CD

| Script | Purpose |
|--------|---------|
| `canary_deploy.sh --full` | Pull, build, migrate, test, deploy (local Mac Mini) |
| `remote_deploy.sh` | SSH push to QA host, same sequence |

Test gates: unit tests block merge, integration tests block QA push, smoke tests run after every rebuild.

---

## Multi-Tenant Isolation

### Current State

| Layer | Mechanism | Enforcement |
|-------|-----------|-------------|
| Application | `merchant_id` on every model (VARCHAR(36), indexed) | 18 models require merchant_id; `merchant_id` set from JWT/session on every request |
| Database (RLS) | `set_current_merchant(:mid)` called at transaction start | Pool event listener on connection `begin` |
| Cache (Valkey) | Key prefix includes `{merchant_id}` | e.g. `chirp:thresholds:{merchant_id}:{rule_id}` |
| Session | `session["merchant_id"]` set after OAuth | Session store (Valkey), 1-hour TTL |
| MCP tools | `context["merchant_id"]` injected from JWT | MCP handler injects from request context |

### Gaps

- RLS policies exist in the database but application code does not enforce them consistently — some queries bypass the `merchant_id` filter.
- Pipeline consumers process events for all merchants in a single consumer group — no per-tenant stream isolation.
- Message queue streams (`canary:events`) are shared across all tenants — a high-volume merchant could starve others.
- No tenant-aware rate limiting — all merchants share the same IP-based rate limits.

---

## Blast Radius

| Component | Services Affected | Data at Risk | User Impact | Recovery Time |
|-----------|-------------------|-------------|-------------|---------------|
| PostgreSQL | Everything | All stored data | Complete outage | Minutes (restart) to hours (corruption) |
| Valkey | Sessions, TSP, cache, rate limiting | In-flight stream messages | Auth broken, detection delayed | Seconds (restart), messages re-derivable |
| HTTP Service (primary) | All HTTP, all MCP, UI | None (stateless) | Complete UI + API outage | Seconds (process restart) |
| Single pipeline consumer | One processing stage | Messages queue in stream | Detection delayed for that stage | Seconds (auto-restart) |
| LLM Inference | Owl AI, ALX embeddings | None | AI features unavailable, detection rules continue | Minutes (model reload) |
| Reverse Proxy | External HTTPS access | None | External users cannot connect | Seconds (restart), direct port still works |
| Memory Bus | ALX memory recall, session memory | None (separate DB) | AI responses lack institutional context | Seconds (restart) |

---

## 7-Layer Stack

| Layer | Name | Components |
|-------|------|------------|
| 0 | Infrastructure | Container orchestration (local/dev), ECS Fargate (cloud target) |
| 1 | Data | PostgreSQL 17 (1 instance, 3 schemas + memory DB), Valkey 8 (streams + cache), PgBouncer |
| 2 | Domain Services | 12 MCP servers, one per bounded context |
| 3 | Agent Mesh | Owl, ALX, Chirp, Fox, Inscription, Condor (6 agents) |
| 4 | Orchestration | Mastra (TypeScript) agent workflows (target) |
| 5 | Gateway | Kong (self-hosted) / AWS API Gateway (target) |
| 6 | Frontend | Server-rendered templates (current), Next.js App Router + RSC + PWA (target) |
| 7 | Protocol | elJeffe / RaaS: Bitcoin L1 inscription + Avalanche L2 naming |

## 11 Service Domains

| # | Domain | Purpose | MCP Tools | SDD |
|---|--------|---------|-----------|-----|
| 1 | Identity | Merchants, users, roles, Square OAuth, tenant context | 6 | Identity SDD, Identity-Square SDD |
| 2 | Webhook Pipeline (TSP) | Webhook intake, HMAC validation, stream processing, parsing | 6 | TSP SDD, Webhook Pipeline SDD |
| 3 | Chirp | Stateless detection rules, threshold config, sensitivity presets | 10 | Chirp SDD |
| 4 | Alert | Alert lifecycle, history, impact scoring, notifications | 6 | Alert SDD |
| 5 | Owl | AI chat, personalities, MCP tools, merchant memory, reports | 8 | Owl SDD |
| 6 | Fox | Case management, evidence locker, hash-chained timeline | 8 | Fox SDD |
| 7 | Analytics | Dashboard metrics, heatmaps, velocity baselines, scorecards | 7 | Analytics SDD, Metrics Analytics SDD |
| 8 | ALX | Institutional memory (pgvector semantic search, 954+ memories) | 7 | ALX SDD |
| 9 | RaaS | Namespace resolution, merchant onboarding, source registration | 7 | RaaS SDD |
| 10 | Ops | Health check runner, simulator, ops console, Chirp Lab | 8 | Ops SDD |
| 11 | UI/BFF | Desktop + mobile rendering, feature flags, config | 4 | UI/BFF SDD |

Additional SDDs:
- **Data Model** — Cross-schema data model reference (PII map anchor)
- **External Identities** — Entity resolution, PII abstraction
- **Goose** — Treasury/payment layer, Bitcoin/L402
- **Multi-POS Architecture Proof** — Multi-source adapter pattern
- **QA Agent** — QA orchestration, 30+ MCP tools

---

## Table Schema Contracts

### Schema Organization

Three schemas in the `canary` database. All tables are schema-qualified in queries.

| Schema | Tables | Write Pattern |
|--------|--------|---------------|
| `app` | ~40 | Operational (merchants, alerts, cases). CRUD with soft delete + audit trail. |
| `sales` | ~19 | IMMUTABLE event stream (transactions, raw webhooks). PostgreSQL `BEFORE UPDATE OR DELETE` trigger blocks any modification. |
| `metrics` | ~20 | Analytics star schema. Fully re-derivable from `sales`. Never the source of truth. |

### Standard Column Contracts

Every table must include:

| Column | Type | Purpose |
|--------|------|---------|
| `id` | UUID (default: uuid_generate_v4()) | Primary key. Used for all lookups, links, cache keys, and drill paths. Never use external IDs as row identifiers. |
| `created_at` | TIMESTAMPTZ | Row creation timestamp |
| `updated_at` | TIMESTAMPTZ | Last modification timestamp |

Tables that participate in multi-tenancy must also include:

| Column | Type | Purpose |
|--------|------|---------|
| `merchant_id` | VARCHAR(36), indexed | Tenant isolation key. Required on 18 models. |

### GSLM Mixin Contracts

| Mixin | Columns | Applied To | Purpose |
|-------|---------|------------|---------|
| Tenant | `merchant_id` VARCHAR(36) indexed | 18 models | Multi-tenant isolation key |
| Audit | `created_at`, `updated_at`, `created_by`, `modified_by` | 29 models | Audit timestamps and attribution |
| SoftDelete | `db_status`, `db_effective_from`, `db_effective_to` | 9 models | Soft delete with effective dating |
| Immutable | (trigger-enforced, no columns) | All sales tables | PostgreSQL `BEFORE UPDATE OR DELETE` trigger — raises exception on any mutation attempt |

### Data Mutation Rules

| Pattern | Scope | Enforcement |
|---------|-------|-------------|
| WRITE-ONCE IMMUTABLE | `sales.*` (all 19 tables) | PostgreSQL BEFORE trigger — raises exception |
| APPEND-ONLY | Alert, AlertHistory, AuditLog, NotificationLog | Application-enforced convention |
| SOFT DELETE | 9 app models | `db_status` + effective dating columns |
| OPERATIONAL | All other app models | Standard CRUD with audit trail |

---

## Security Contracts

### CSRF and Authentication

| Route Auth Pattern | Mechanism | Exempt? |
|---|---|---|
| Session-authenticated routes | CSRF token required on POST/PUT/DELETE | No |
| JWT-authenticated routes (API, MCP) | JWT validates request; CSRF not applicable | Yes |
| HMAC-authenticated routes (webhooks) | HMAC signature validates request; CSRF not applicable | Yes |
| Public routes (health) | No auth | Yes |

### Rate Limiting

| Scope | Limit |
|-------|-------|
| Default (all routes) | 2000/day, 500/hour |
| MCP tool invocations | 1000/hour |
| Merchant tier — Open | 100/min |
| Merchant tier — Standard | 60/min |
| Merchant tier — Burst | 300/min |
| Merchant tier — Internal | 1000/min |

### Security Headers

Required on all responses:
- HSTS (HTTP Strict Transport Security)
- Content-Security-Policy
- X-Frame-Options: DENY
- Force HTTPS: enabled in production, disabled for localhost development

### Encryption Contracts

| Scope | Algorithm | Key Source |
|-------|-----------|-----------|
| OAuth tokens | AES-256-GCM | `CANARY_ENCRYPTION_KEY` (env/secrets manager) |
| Session data | None (plaintext in Valkey) | — |
| Employee PII | None (plaintext) — P0 finding, encrypt before GA | — |
| Webhook payloads | None (plaintext) — P0 finding, redact before GA | — |

---

## Test Strategy

| Layer | Purpose | Gate |
|-------|---------|------|
| Unit | Business logic, pure functions, rule evaluation | CI blocks merge |
| Integration | Database writes/reads, API contracts, pipeline flow | Before QA push |
| Smoke | Service health, critical path availability | After every build |

---

## Target State

The target-state architecture extracts domains from the monolith into standalone service containers, adds an API gateway, and introduces Mastra for multi-step agent orchestration. The same MCP tool contracts stay — transport changes from in-process calls to HTTP.

### API Gateway (Phase 2: Kong, Phase 3: AWS API Gateway)

Externalizes cross-cutting concerns: TLS termination, JWT validation, HMAC webhook verification, rate limiting per merchant tier, path-based routing, CORS enforcement, SSE proxy, and request/response logging with correlation IDs.

Auth evolution: middleware (now) → Keycloak OIDC (self-hosted) → AWS Cognito. All produce identical JWT payloads: `{sub, merchant_id, organization_id, roles, iss, exp}`.

### Service Extraction (Phase 4)

Each agent becomes an independent service: MCP server + MCP client + event bus consumer + service logic + PgBouncer sidecar. AI agents (Owl, ALX, Condor) co-locate with the LLM inference service. Deterministic agents (Chirp, Fox, Alert) stay with the database. Agent discovery via Valkey hash (`canary:registry:<agent>`), 30-second heartbeat.

### Process Ontology Alignment

Canary's detection rules implement a 30-year retail operations process ontology:

| Source | Year | Canary Mapping |
|--------|------|----------------|
| Staples Level 2 (Hoover/PwC) | 1996 | 26 processes → Chirp rule categories |
| Tesco Operating Model v1.24 | 2007 | ~100 processes → KPI framework |
| Beck & Peacock "New Loss Prevention" | 2009 | Operational failure taxonomy → detection philosophy |
| Speights, Downs & Raz | 2017 | Statistical methods → velocity z-scores, baseline modeling |

The 6-layer scoring stack: per-transaction (Sales Audit), per-alert (Performance Monitoring), per-period heatmap (Performance Levers), time-series velocity (XPLOSS/Poisson), aggregate health (Heartbeat/CDSS), entity risk (SRA Scorecards).

**Source SDDs:** SDD-059 (Modern Architecture Blueprint), SDD-060 (Process Ontology Alignment), SDD-062 (API Gateway).

---

## Code Review Findings

### P0 — Blocks Production

| # | Finding | Detail | Recommended Fix |
|---|---------|--------|-----------------|
| P0-1 | Employee PII stored plaintext | `first_name`, `last_name` in `app.employees` have no encryption. These fields flow to alerts, cases, and analytics. | Extend AES-256-GCM encryption to employee PII fields. Encrypt at write, decrypt at read. |
| P0-2 | Webhook payloads stored with raw customer data | `sales.raw_webhooks` preserves full POS JSON including customer IDs, tender details. Immutable table means redaction requires compensating INSERT. | Add a redaction step in TSP Sub1 (Seal) — strip customer PII before persisting raw payload. Store hash of original for integrity. |
| P0-3 | Encryption key in environment file | `CANARY_ENCRYPTION_KEY` stored in plaintext environment file. Key compromise exposes all OAuth tokens. | Migrate to AWS Secrets Manager. Load at startup via SDK. Rotate key quarterly. |
| P0-4 | `SECRET_KEY` falls back to insecure default | Non-production environments fall back to `dev-fallback-not-for-production`. If environment is misconfigured, production runs with a known key. | Remove fallback entirely. Fail hard if `SECRET_KEY` is not set, regardless of environment. |
| P0-5 | QA config embeds encryption key in plaintext | A hardcoded encryption key value appears in a committed QA configuration file. | Remove from config. Use environment file (gitignored) or secrets management. |

### P1 — Before GA

| # | Finding | Detail | Recommended Fix |
|---|---------|--------|-----------------|
| P1-1 | No data retention policy | No automated purge for any table. `sales.*` is immutable and append-only — will grow indefinitely. | Implement retention: raw webhooks >12mo archived, sessions >30d purged, audit logs >24mo cold storage. |
| P1-2 | Session data unencrypted in Valkey | Session state stored as plaintext. No AUTH required on dev Valkey. | Enable Valkey AUTH + TLS in production. Consider session payload encryption. |
| P1-3 | No audit logging for MCP tool invocations | MCP tool dispatch does not log caller identity, tool name, params, or result status. | Add audit log entry for every `POST /tools/<name>` with caller identity, tool name, params hash, result status. |
| P1-4 | Error responses may leak internals | Missing error handler templates can cause internal details to appear in error responses. | Ensure all error handlers exist. Add catch-all JSON error handler for API routes. Strip stack traces in production. |
| P1-5 | RLS context fails open | If `merchant_id` is absent from the request context, no RLS filter is applied — queries see all tenants. | Add explicit `set_current_merchant('none')` when merchant_id is absent, or fail the query if tenant context is required. |
| P1-6 | No key rotation procedure | No GCM-to-GCM rotation procedure. Key compromise requires manual re-encryption of all tokens. | Document rotation procedure. Build CLI command to re-encrypt all tokens with a new key. |
| P1-7 | Notification email/SMS stubs | No actual delivery channel is wired for email or SMS. | Wire SendGrid or SES for email before GA. SMS can remain stub with clear user documentation. |

### P2 — Post-Launch

| # | Finding | Detail | Recommended Fix |
|---|---------|--------|-----------------|
| P2-1 | No structured monitoring | No Prometheus metrics, no dashboards, no alerting rules. Health checks exist but are not scraped. | Expose Prometheus metrics: request latency, error rates, TSP throughput, queue depth. |
| P2-2 | Single service instance in dev | Production needs multiple service instances for throughput. Enterprise configuration has 4+ instances. | Ensure production deployment uses 4+ HTTP service instances. |
| P2-3 | No request correlation IDs | No `X-Request-ID` or trace ID propagated across the HTTP service, pipeline consumers, and Owl MCP. | Add middleware to generate/propagate correlation ID in all log entries. |
| P2-4 | Audit chain verification is fail-open | A tampered audit chain only produces a CRITICAL log, does not block startup. | Consider fail-closed in production: if audit chain is tampered, refuse to serve write endpoints. |
| P2-5 | Pipeline consumers share one stream for all tenants | `canary:events` stream processes all merchants in one consumer group. High-volume merchants can delay processing for others. | Add per-tenant stream partitioning or priority-based routing in Phase 4 service extraction. |

---

## Production Readiness Checklist

- [ ] PII encrypted at rest (P0-1: employee names, P0-2: webhook payloads)
- [ ] Secrets in AWS Secrets Manager, not environment files (P0-3, P0-5)
- [x] Health check endpoint responds (`/health` on primary service, Owl MCP, QA Agent, pipeline consumers)
- [ ] Audit logging for sensitive operations (P1-3: MCP tool invocations not logged)
- [ ] Data retention policy implemented (P1-1: no automated purge)
- [x] Rate limiting on public endpoints (2000/day, 500/hour default; MCP: 1000/hour)
- [ ] Error responses don't leak internals (P1-4: missing handler fallback risk)
- [x] CSRF protection active (all session-auth routes)
- [x] TLS termination (Cloudflare Tunnel / reverse proxy)
- [x] OAuth tokens encrypted (AES-256-GCM)
- [x] Immutable sales data (PostgreSQL BEFORE trigger enforced)
- [x] Multi-tenant isolation at DB layer (RLS via `set_current_merchant`)
- [ ] Multi-tenant isolation fail-safe (P1-5: RLS fails open when merchant_id is None)
- [ ] Key rotation procedure documented (P1-6)
- [ ] Session encryption in Valkey (P1-2)
- [ ] Monitoring and alerting (P2-1)
- [ ] Request correlation IDs (P2-3)
