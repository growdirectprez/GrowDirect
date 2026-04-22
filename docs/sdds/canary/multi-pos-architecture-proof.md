# Multi-POS Architecture — Abstraction Layer & Adapter Pattern

**Service Type:** App Service (Canary)
**Status:** Architecture validated, Phase 1 (Square) implemented
**Date:** 2026-04-13 (ops upgrade from 2026-03-22 original)
**Author:** ALX (COO Agent)
**Reviewed by:** Jeffe (CEO)

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]
**Architecture:** [[docs/sdds/canary/architecture|Canary Architecture SDD]]
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[docs/team/Architect|Architect]] · **Operator role:** [[docs/team/Engineer|Engineer]]

---

## Purpose

Canary is a horizontal data platform. The loss prevention engine operates on
canonical data models (CRDM) that are POS-agnostic by design. Adding a new
POS system requires adapter code — not architectural changes.

This SDD documents the abstraction layer that enables multi-POS support, the
adapter pattern each new POS must implement, and the current production state
of the architecture with code review findings.

---

## Dependencies

| Dependency | Type | Required For |
|---|---|---|
| PostgreSQL 17 (`canary` database, `app` + `sales` schemas) | Database | Source registry, external identities, merchant sources, CRDM models |
| Valkey 8 (DB 0 sessions, DB 3 dedup cache) | Cache/Stream | Webhook dedup, event stream (`canary:events`) |
| TSP Pipeline (Sub1-Sub4 consumers) | Internal service | Event processing after webhook receipt |
| Chirp Detection Engine | Internal service | Rule evaluation against parsed CRDM data |
| Source POS APIs (Square, Toast, Clover) | External API | Webhook delivery, OAuth/auth, data enrichment |

---

## Data Flow & PII Map

### What Enters

- **Webhook POST payloads** from POS systems via `POST /webhooks/<source>`.
  Currently Square only (`REGISTERED_SOURCES = {"square"}`). Raw bytes read
  before JSON parsing (patent-critical ordering).
- **HMAC signature headers** per source (`x-square-hmacsha256-signature` for
  Square). Validated before any payload processing.
- **OAuth tokens** during merchant onboarding (stored AES-256-GCM encrypted
  in `app.oauth_tokens`).

### What's Stored

| Table | Schema | PII Fields | Encryption Status | Classification |
|---|---|---|---|---|
| `source_systems` | app | None | N/A | public |
| `merchant_sources` | app | `external_merchant_id` | **Plaintext** | internal |
| `external_identities` | app | `external_id` (source-side entity IDs) | **Plaintext** | internal |
| `ingestion_log` | sales | `ip_address`, `user_agent` | **Plaintext** | sensitive |
| `transactions` | sales | `card_fingerprint`, `card_last4`, `card_bin`, `card_brand`, `card_exp_month`, `card_exp_year` | **Plaintext** | sensitive |
| `transactions` | sales | `payload` (full webhook JSON) | **Plaintext** | restricted |
| `dead_letter_queue` | sales | `payload` (full event payload for replay) | **Plaintext** | restricted |

### What Exits

- Parsed CRDM records written to `canary_sales` tables via Sub2 consumer.
- Detection stream events published for Chirp evaluation via Sub4.
- Stateless Tier 1 Chirp alerts written to `app.alerts` inline.
- Ingestion log records for audit trail.

---

## API Contract

### Webhook Entry Point

```
POST /webhooks/<source>
```

| Parameter | Source | Description |
|---|---|---|
| `source` (path) | URL | POS identifier, must be in `REGISTERED_SOURCES` |
| Body | Raw bytes | Full webhook payload |
| `x-square-hmacsha256-signature` | Header | HMAC signature (Square) |

**Response:** `200 OK` with `event_id` on success, `401` on HMAC failure,
`404` on unknown source, `413` on payload > 1MB, `503` on queue unavailable.

### Health Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/webhooks/health` | GET | Valkey stream connectivity + version |
| `/webhooks/ready` | GET | Signature key loaded, notification URL set, queue reachable |
| `/webhooks/live` | GET | Process alive |

### Internal Interfaces

| Interface | Description |
|---|---|
| `webhook_dispatch.resolve_route(event_type)` | Maps event type to `EventRoute` (parser, CRDM model, detection type) |
| `webhook_dispatch.import_parser(parser_path)` | Dynamic import of parser function from `canary.services.parsers.*` |
| `stream_publisher.publish_event(...)` | Publishes to Valkey stream `canary:events` |
| `enrichers.enrich_payload(source, payload, event_type)` | Source-specific payload enrichment before stream publish |
| `square_validator.validate_signature(raw_bytes, sig_header)` | HMAC-SHA256 timing-safe validation |

---

## Architecture — Abstraction Layer

### Layer Scorecard (Current State from Code)

| Layer | Implementation | Multi-POS Ready? |
|---|---|---|
| **Source Registry** (`app.source_systems`) | Reference table: `code` PK, `display_name`, `category`, `is_active`. Designed for N sources. | **Ready** — INSERT a row per POS |
| **Merchant Connection** (`app.merchant_sources`) | `(merchant_id, source_code)` unique, FK to `source_systems.code`. Status lifecycle, RaaS namespace. | **Ready** — no schema changes |
| **Identity Resolution** (`app.external_identities`) | Source-agnostic bridge: `(merchant_id, source_code, entity_type, external_id)` unique. 5 entity types. | **Ready** — INSERT with new `source_code` |
| **Webhook Entry** (`/webhooks/<source>`) | Route parameterized on `<source>`, gated by `REGISTERED_SOURCES` set. `SOURCE_VALIDATORS` dict maps source to validator module. | **Ready** — add source to set + validator dict |
| **Signature Validation** (`tsp/validators/`) | Strategy pattern: `validators/__init__.py` describes pattern, `validators/square.py` implements Square HMAC. Interface: `validate_signature()`, `extract_merchant_id()`, `extract_source_event_id()`, `extract_event_type()`. | **Ready** — add `validators/toast.py` following same interface |
| **Payload Enrichment** (`tsp/enrichers/`) | Strategy pattern: `_SOURCE_ENRICHERS` dict, `enrichers/square.py` implements Square order fetch. | **Ready** — add `enrichers/toast.py` |
| **Event Dispatch** (`webhook_dispatch.py`) | Flat `event_type -> EventRoute` lookup. ~70 exact-match routes + ~25 prefix routes. All Square event types. | **Needs generalization** — dispatch keys are bare event types, not `(source_code, event_type)` compound keys |
| **Parser Suite** (`services/parsers/`) | 17 `square_*` parser files. Pure functions: JSON in, flat dict out. Dynamic import via `import_parser()`. | **Needs new code** — add `toast_*` parser files following same pattern |
| **CRDM Models** (Transaction, etc.) | Source-agnostic columns. `card_fingerprint` indexed. No `source_code` column on Transaction. | **Needs minor changes** — add `source_code` column |
| **Stateless Chirps** (Tier 1) | Hardcoded `if source == "square"` check in `webhooks_tsp.py` line 167. | **Needs generalization** — remove source guard |
| **Evidence Chain** (Sub1 seal + Sub3 Merkle) | Operates on raw event bytes and chain hashes. No POS-specific field dependency. | **Ready** — source-agnostic by design |

### POS Adapter Pattern

Each new POS requires five components — a repeatable sprint:

| Component | Responsibility | Location Pattern |
|---|---|---|
| **Auth Adapter** | Connect merchant, manage tokens | `canary/services/<pos>_oauth.py` |
| **Signature Validator** | Verify inbound webhooks | `canary/services/tsp/validators/<pos>.py` |
| **Payload Enricher** | Fetch full objects for lightweight notifications | `canary/services/tsp/enrichers/<pos>.py` |
| **Event Registry** | Map POS events to CRDM parsers | Entries in `webhook_dispatch.py` (needs compound key) |
| **Parser Suite** | Transform POS JSON to CRDM flat dicts | `canary/services/parsers/<pos>_*.py` |

### Current Implementation (Square)

- **17 parser files** in `canary/services/parsers/`: payment, order, dispute, loyalty, payout, auxiliary, card, invoice, terminal, bank account, transfer order, subscription, customer, location, device, gift card, team member.
- **~70 exact-match event routes** + ~25 prefix catch-all routes covering all ~145 Square webhook event types.
- **Validator module:** `tsp/validators/square.py` — HMAC-SHA256 with `SQUARE_WEBHOOK_SIGNATURE_KEY` and `SQUARE_NOTIFICATION_URL` env vars.
- **Enricher module:** `tsp/enrichers/square.py` — fetches full order objects for lightweight Square order webhooks.

---

## Toast and Clover Validation

### Toast (Restaurant POS)

Toast uses OAuth 2.0 client-credentials grant (machine-to-machine, no merchant
consent flow). Primary webhook is `order_updated` containing the full Order
object with Check-level granularity. ~8 event types total.

**Card fingerprint gap:** Toast's `cardPaymentId` is unreliable for EMV/chip
transactions (frequently null). Best available: `last4Digits + cardType`
composite key (~50K collision space vs Square's cryptographic fingerprint).

**Structural advantages:** Split check awareness, three-level void tracking
(`voided` + `voidDate` + `voidBusinessDate` at order/check/selection),
employee directly on order (`server.guid`), native `businessDate` field.

### Clover (General Retail POS)

Clover uses OAuth 2.0 authorization-code grant (like Square). Sends
**notification-only webhooks** — payload contains object ID + event type, not
full object. Requires fetch-then-parse pattern.

**Card fingerprint gap:** No native fingerprint. Composite key:
`first6 + last4 + cardType` (~50B collision space — better than Toast because
BIN is exposed on card-present reads).

**Architectural wrinkle:** Notification-only webhooks require a fetch step
between webhook receipt and parser dispatch. The enricher pattern already
handles this — `enrichers/clover.py` would always fetch the full object.

### Source-Aware Confidence Tiers (Proposed)

| Tier | Criteria | Card Identity Method | Confidence |
|---|---|---|---|
| **Tier 1** | Cryptographic fingerprint available | `card.fingerprint` (Square) | High |
| **Tier 2** | Composite key with BIN | `first6 + last4 + brand` (Clover) | Medium-high |
| **Tier 2** | Composite key without BIN | `last4 + brand` (Toast) | Medium |
| **Tier 3** | Cash / no card data | N/A | N/A — rule skipped |

Impact on Chirp rules: C-005 (CARD_VELOCITY) degrades from exact-match to
probabilistic on non-Square POS. C-008 (MANUAL_ENTRY_SPIKE) works across all.
Card risk scoring (GRO-263) and refund-to-different-card detection blocked
on Toast/Clover.

---

## Operations

### Startup Sequence

1. Flask app loads, registers `webhooks_tsp_bp` at `/webhooks` prefix
2. CSRF protection exempts webhook blueprint (documented in `wsgi.py`)
3. Readiness probe (`/webhooks/ready`) checks: Valkey stream ping, signature
   key loaded (`SQUARE_WEBHOOK_SIGNATURE_KEY`), notification URL configured
   (`SQUARE_NOTIFICATION_URL`)
4. If any check fails, readiness returns 503 — load balancer stops routing

### Failure Modes

| Failure | Impact | Behavior |
|---|---|---|
| Valkey stream unreachable | Webhooks cannot be queued | Returns 503 with `retry_after_seconds: 30`. Source POS retries with backoff. |
| Signature key not configured | Cannot validate any webhooks | Returns 503. Readiness probe fails. |
| JSON parse failure | Payload corrupted or non-JSON | Accepts and hashes raw bytes. Publishes with `parse_failed=true`. Sub1 stores, Sub2 skips structured parse. |
| Duplicate event | Idempotency | Returns 200 OK with `duplicate: true`. Checked via Valkey DB 3 dedup cache (24h TTL). DB unique constraint is backstop. |
| DB write failure (ingestion_log) | Audit trail gap | Logs error but does NOT fail the webhook — stream is the source of truth. |
| Enrichment failure | Lightweight payload persists | Logs warning, continues with unenriched payload. Non-blocking. |
| Stateless chirp failure | Detection gap | Logs warning, continues. Tier 1 chirps are additive, never block pipeline. |

### Monitoring

| Metric | Alert Threshold | Source |
|---|---|---|
| Webhook acceptance rate | < 95% over 5 min | Ingestion log status counts |
| HMAC failure rate | > 5% over 1 min | Logger warnings (`HMAC verification failed`) |
| Stream publish failures | Any | Logger errors (`Failed to publish to stream`) |
| Dedup cache hit rate | Informational | Valkey DB 3 key count |
| Parse failure rate | > 1% over 15 min | Ingestion log `parse_failed` flag |

### Configuration

| Env Var | Required | Default | Purpose |
|---|---|---|---|
| `SQUARE_WEBHOOK_SIGNATURE_KEY` | Yes | — | HMAC signing key for Square webhooks |
| `SQUARE_NOTIFICATION_URL` | Yes | — | URL Square posts to (used in HMAC computation) |
| `MAX_PAYLOAD_BYTES` | No | `1048576` (1MB) | Maximum webhook payload size |
| `VALKEY_URL` | Yes | `redis://localhost:6379/0` | Valkey connection (DB 0) |
| `VALKEY_STREAM` | No | `canary:events` | Stream name for event publishing |
| `VALKEY_DEAD_LETTER_STREAM` | No | `canary:dead_letter` | Dead letter stream name |
| `CANARY_ENCRYPTION_KEY` | Yes | — | AES-256-GCM key for OAuth token encryption |

---

## Deployment

### Docker Service

The webhook endpoint runs inside the Canary Flask container (`canary-web`),
not as a separate service. Blueprint registered at `/webhooks` prefix in
`wsgi.py`. Port 5001.

### AWS Target

| Component | AWS Service | Notes |
|---|---|---|
| Webhook endpoint | ECS/Fargate (Canary Flask) | Behind ALB, path-based routing to `/webhooks/*` |
| Valkey stream | ElastiCache (Valkey mode) | DB 0 (sessions), DB 3 (dedup cache) |
| PostgreSQL | RDS PostgreSQL 17 | `canary` database, `app` + `sales` schemas |
| Signature keys | Secrets Manager | `SQUARE_WEBHOOK_SIGNATURE_KEY`, future POS keys |
| Encryption key | Secrets Manager | `CANARY_ENCRYPTION_KEY` |

### CI/CD Requirements

- Unit tests: `tests/unit/test_webhook_dispatch.py`, `tests/unit/test_webhook_merchant_resolve.py`, `tests/unit/test_webhook_usecase_map.py`
- Integration tests: `tests/integration/test_merchant_lifecycle.py`
- Smoke tests: `tests/smoke/test_api_endpoints.py`, `tests/smoke/test_security.py`
- Each new POS adapter needs its own validator test, parser tests, and integration test for the webhook-to-CRDM flow

---

## Code Review Findings

### P0 — Blocks Production

**P0-1: Raw webhook payloads stored with PII in plaintext.**
`Transaction.payload` (full JSON) and `DeadLetterQueue.payload` store complete
webhook payloads including card data (`card_fingerprint`, `card_last4`,
`card_bin`, `card_exp_month/year`), customer IDs, and employee IDs. No
field-level encryption or redaction before storage.
**Fix:** Redact PII fields from `payload` column before persistence. Apply
`crypto.py` AES-256-GCM encryption to retained forensic payloads. Consider
storing only the fields needed for replay, not full payloads.
**Linear:** GRO-TBD

**P0-2: Card data fields stored in plaintext on Transaction model.**
`card_fingerprint`, `card_last4`, `card_bin`, `card_exp_month`, `card_exp_year`
are stored as plaintext strings in `sales.transactions`. These are PCI-adjacent
fields.
**Fix:** Encrypt `card_fingerprint`, `card_last4`, `card_bin` at rest using
`crypto.py` pattern. Hash `card_fingerprint` for index lookups (store both
encrypted value and HMAC hash for search).
**Linear:** GRO-TBD

**P0-3: Encryption key in .env file.**
`CANARY_ENCRYPTION_KEY` and `SQUARE_WEBHOOK_SIGNATURE_KEY` are stored in `.env`
and `.env.template`. Production deployment must use AWS Secrets Manager.
**Fix:** Add `boto3` Secrets Manager retrieval at app startup. Remove keys
from `.env` in production.
**Linear:** GRO-TBD

**P0-4: IP address logged in plaintext.**
`ingestion_log.ip_address` stores raw source IP addresses. PII under GDPR
and CCPA.
**Fix:** Hash or mask IPs before storage. Use HMAC with a rotating salt for
IP-based rate limiting lookups without storing raw IPs.
**Linear:** GRO-TBD

### P1 — Before GA

**P1-1: No rate limiting on webhook endpoint.**
`POST /webhooks/<source>` has no rate limiting. A compromised or misbehaving
POS integration could flood the pipeline.
**Fix:** Add Flask-Limiter on webhook endpoint. Suggested: 100 req/s per
source IP, 1000 req/s global.
**Linear:** GRO-TBD

**P1-2: Event dispatch not generalized for multi-POS.**
`webhook_dispatch.py` uses flat `event_type` keys (e.g., `payment.completed`).
Adding Toast requires `(source_code, event_type)` compound keys to avoid
collision between POS systems that may use the same event type string.
**Fix:** Change `EVENT_ROUTES` key to `f"{source}:{event_type}"` or add
source-prefixed dispatch tables.
**Linear:** GRO-TBD

**P1-3: Stateless chirp evaluation hardcoded to Square.**
`webhooks_tsp.py` line 167: `if not parse_failed and source == "square"`.
This blocks Tier 1 detection on any non-Square source.
**Fix:** Remove source guard. Dispatch already resolves the parser; if the
parser exists for the source/event_type, run stateless chirps.
**Linear:** GRO-TBD

**P1-4: No `source_code` column on Transaction model.**
The `sales.transactions` table has no column to identify which POS system
originated the record. Multi-POS queries (e.g., "show all Toast transactions")
would require joining through `ingestion_log` or `external_identities`.
**Fix:** Add `source_code` column to `Transaction` model. Alembic migration.
Backfill existing rows with `'square'`.
**Linear:** GRO-TBD

**P1-5: No data retention policy for ingestion_log or dead_letter_queue.**
`ingestion_log` and `dead_letter_queue` grow unbounded. No automated purge.
**Fix:** Implement retention: ingestion_log > 90 days archived, DLQ resolved
entries > 30 days purged.
**Linear:** GRO-TBD

**P1-6: No confidence tier metadata on Chirp alerts.**
Alerts carry no `detection_confidence` field. When non-Square sources with
composite card identity feed the pipeline, downstream consumers (Fox cases,
dashboard) cannot weight alerts appropriately.
**Fix:** Add `detection_confidence` field to Alert model. Source-aware Chirp
rule evaluation sets confidence based on card identity quality per source.
**Linear:** GRO-TBD

### P2 — Post-Launch

**P2-1: No key rotation procedure documented.**
`CANARY_ENCRYPTION_KEY` and `SQUARE_WEBHOOK_SIGNATURE_KEY` have no rotation
procedure. Adding POS sources adds more keys to manage.
**Fix:** Document rotation procedure per key. Implement dual-key read
(decrypt with current, fallback to previous) for zero-downtime rotation.
**Linear:** GRO-TBD

**P2-2: Dedup cache uses separate Valkey DB connection per request.**
`_is_duplicate()` creates a new `Redis.from_url()` connection on every webhook.
No connection pooling for DB 3.
**Fix:** Use a module-level connection pool or share the connection via
`stream_publisher.get_stream_client()` pattern.
**Linear:** GRO-TBD

**P2-3: Merchant ID lookup inside webhook handler creates DB session per request.**
Lines 119-124 of `webhooks_tsp.py` import and query `Merchant` model inline,
creating a new DB session per webhook. This should use the existing session
factory or a cached lookup.
**Fix:** Refactor merchant ID resolution to use a cached lookup (Valkey or
in-memory LRU) instead of per-request DB query.
**Linear:** GRO-TBD

**P2-4: Parser import uses `importlib.import_module` on every event.**
`import_parser()` in `webhook_dispatch.py` dynamically imports parser modules
on every call. No caching of imported modules.
**Fix:** Add module-level cache (dict) for imported parser functions, similar
to `_MODEL_CACHE` pattern in `sub2_parse.py`.
**Linear:** GRO-TBD

---

## Production Readiness Checklist

- [ ] PII encrypted at rest — **FAIL**: Card data fields, IP addresses, and
  full webhook payloads stored plaintext (P0-1, P0-2, P0-4)
- [ ] Secrets in AWS Secrets Manager — **FAIL**: Keys in `.env` files (P0-3)
- [x] Health check endpoint responds — `/webhooks/health`, `/webhooks/ready`,
  `/webhooks/live` all implemented
- [ ] Audit logging for sensitive operations — **PARTIAL**: `ingestion_log`
  records webhook receipt but no audit trail for key access, config changes,
  or source registration
- [ ] Data retention policy implemented — **FAIL**: No automated purge for
  ingestion_log or DLQ (P1-5)
- [ ] Rate limiting on public endpoints — **FAIL**: No rate limiting on
  webhook endpoint (P1-1)
- [x] Error responses don't leak internals — webhook responses return
  structured JSON with status codes, no stack traces or internal paths
- [ ] Multi-POS dispatch generalized — **FAIL**: Flat event type keys, no
  compound `(source, event_type)` dispatch (P1-2)
- [ ] Source-aware detection confidence — **FAIL**: No confidence tiers on
  alerts (P1-6)
- [x] Idempotency — Valkey dedup cache + DB unique constraint implemented
- [x] Signature validation — Timing-safe HMAC-SHA256 implemented for Square
- [x] Graceful degradation — JSON parse failure, enrichment failure, and
  stateless chirp failure all handled without blocking pipeline

---

## Appendix A: Three-POS Comparison — Card Identity

| Capability | Square | Toast | Clover |
|---|---|---|---|
| Card fingerprint | Native `card.fingerprint` — cryptographic, deterministic | `cardPaymentId` — unreliable for EMV | None |
| BIN (first 6) | Available | Auth flow only, not on Orders API | Available via `?expand=cardTransaction` |
| Last 4 | Available | Available | Available |
| Card brand | Available | Available | Available |
| Entry method | Available | Available | Available |
| Composite key quality | Not needed (fingerprint) | `last4 + brand` (~50K space) | `first6 + last4 + brand` (~50B space) |
| Confidence tier | **Tier 1** (high) | **Tier 2** (medium) | **Tier 2** (medium-high) |

## Appendix B: Toast CRDM Field Mapping

| Canary CRDM Field | Square Source | Toast Source | Status |
|---|---|---|---|
| `transaction.external_id` | `payment.id` | `order.guid` | Direct map |
| `transaction.card_fingerprint` | `card.fingerprint` | Composite: `last4 + cardType` | **Degraded** |
| `transaction.entry_method` | `card_details.entry_method` | `payment.cardEntryMode` | Direct map (enum remap) |
| `transaction.employee_id` | `tender.employee_id` | `order.server.guid` | Direct map |
| `transaction.device_id` | `tender.device_id` | `order.device` | Direct map |
| `transaction.location_id` | `payment.location_id` | Header: `Toast-Restaurant-External-ID` | Direct map |
| `transaction.customer_id` | `order.customer_id` | Only on takeout/delivery | **Gap** (no dine-in customer) |
| `transaction.business_date` | Computed | `order.businessDate` | Direct map (Toast native) |
| `tender.tender_type` | `tender.type` | `payment.type` | Enum remap |
| `tender.card_brand` | `card.card_brand` | `payment.cardType` | Direct map |
| `tender.card_last4` | `card.last_4` | `payment.last4Digits` | Direct map |
| `tender.amount_cents` | `tender.amount_money.amount` | `payment.amount` x 100 | Unit conversion |

## Appendix C: Implementation Scope per POS

Each new POS is a sprint — five adapter components:

| Work Item | Complexity | One-Time? |
|---|---|---|
| Auth adapter (source-specific OAuth/credentials) | Medium | Per POS |
| Webhook signature validator | Low | Per POS |
| Event registry entries | Low | Per POS |
| Parser suite (source-specific field mappings) | Medium | Per POS |
| Payload enricher (for notification-only webhooks) | Low | Per POS (Clover) |
| Generalize dispatch to `(source_code, event_type)` | Low | **One-time** |
| Add `source_code` to Transaction table | Low | **One-time** |
| Chirp confidence tiers | Medium | **One-time** |
| Remove `source == "square"` guard on stateless chirps | Low | **One-time** |

**Verdict:** The horizontal platform thesis is validated. Three structurally
different POS systems map to the same adapter pattern without architectural
changes. The one-time generalizations (dispatch compound key, `source_code`
column, confidence tiers) serve all future POS integrations.

---

*Canary | GrowDirect Inc. | Confidential*
