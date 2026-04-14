# Webhook Pipeline

**Type:** External Integration (Type 4)
**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]
**Last reviewed:** 2026-04-13 (code review + ops upgrade)

## Purpose

The Webhook Pipeline is Canary's data ingestion front door. Every external event
entering the system passes through this service: HMAC-validated, hashed,
deduplicated, and published to Valkey Streams for downstream consumer processing.
It is the only externally-accessible write endpoint in the Canary platform.

## Dependencies

| Dependency | Type | Required | Notes |
|------------|------|:--------:|-------|
| PostgreSQL 17 (`canary` database) | Database | Yes | `canary_sales.ingestion_log` writes, `canary_app.merchants` lookups |
| Valkey 8 (DB 3) | Cache | Yes (fail-open) | Dedup cache (`SET NX`, 24h TTL). Fails open — DB constraint is backstop |
| Valkey 8 (DB 4) | Stream | Yes (hard) | `canary:events` stream. Failure = 503, event rejected |
| Square Webhooks API | External | Yes | Source of all webhook POSTs. Per-subscription HMAC key |
| Square Orders API | External | No | Enrichment only — order.* webhooks fetch full order data |
| Flask app container | Runtime | Yes | Blueprint runs inside `canary-flask` container on port 5001 |
| TSP Consumers (Sub1-4) | Downstream | No (decoupled) | Read from Valkey stream independently. Webhook does not wait for them |

## Data Flow & PII Map

### What enters

Square sends HTTP POST to `POST /webhooks/square` with:
- Raw JSON body (max 1MB) containing transaction, order, loyalty, payout, dispute, cash drawer, gift card, inventory, and timecard events
- `X-Square-Hmacsha256-Signature` header (Base64-encoded HMAC-SHA256)
- 27 registered webhook event types post-onboarding

### PII fields in webhook payloads

| Field | Source | Classification | Storage | Notes |
|-------|--------|---------------|---------|-------|
| `raw_payload` (full JSON body) | Square POST | **sensitive** | Plaintext in `evidence_records.raw_payload`, Valkey stream `canary:events` | Contains all fields below; no field-level redaction |
| `card_fingerprint` | `payment.card_details.card.fingerprint` | **sensitive** | Plaintext in `transactions.card_fingerprint` | Tokenized by Square, but unique per card — linkable |
| `card_last4` | `payment.card_details.card.last_4` | **internal** | Plaintext in `transactions.card_last4`, `transaction_tenders.card_last4` | Last 4 digits of card |
| `card_bin` | `payment.card_details.card.bin` | **sensitive** | Plaintext in `transactions.card_bin` | First 6 digits — identifies issuing bank |
| `card_exp_month/year` | `payment.card_details.card.exp_month/year` | **internal** | Plaintext in `transactions` | Card expiration |
| `phone_number` | `loyalty_account.mapping.phone_number` | **sensitive** | **Hashed** (SHA-256) in `loyalty_accounts.phone_hash` | Only PII field with protection applied |
| `employee_id` | Multiple event types | **internal** | Plaintext in `transactions`, `cash_drawer_shifts/events`, `timecards`, `gift_card_activities`, `refund_links` | Square team_member_id — identifies individual employees |
| `customer_id` | `payment.customer_id` | **internal** | Plaintext in `transactions.customer_id` | Square customer reference — parser deliberately drops name/email/phone |
| `ip_address` | `request.remote_addr` | **sensitive** | Plaintext in `ingestion_log.ip_address` | Source IP of webhook POST (Square infrastructure IP) |
| `user_agent` | `request.headers["User-Agent"]` | **internal** | Plaintext in `ingestion_log.user_agent` | HTTP User-Agent of webhook sender |
| `merchant_id` | Payload root | **internal** | Plaintext across all tables (tenant key) | Square merchant identifier |
| `device_id` | `payment.device_details.device_id` | **internal** | Plaintext in `transactions.device_id` | POS terminal identifier |
| `location_id` | Multiple event types | **internal** | Plaintext across tables | Physical store location |

### What's stored

- **Valkey DB 3:** Dedup keys `dedup:square:{source_event_id}` (24h TTL, auto-expire)
- **Valkey DB 4:** Stream messages `canary:events` (9 fields including `raw_payload`)
- **canary_sales.ingestion_log:** One row per accepted webhook (includes `ip_address`, `user_agent`)
- **canary_sales.evidence_records:** Write-once sealed copy (via Sub1, includes `raw_payload`)
- **canary_app.webhook_events:** Legacy raw payload storage (append-only)
- **canary_app.schema_fingerprints / schema_drift_alerts:** Schema shape tracking (no PII)

### What exits

- **To Valkey stream `canary:events`:** 9-field message with full `raw_payload` (consumed by Sub1-4)
- **To Valkey stream `canary:detection`:** 5-field message (no PII, just IDs and routing keys — published by Sub2)
- **HTTP response to Square:** Status + event_id only. No payload reflection.

## API Contract

### POST /webhooks/\<source\>
- **Auth:** HMAC-SHA256 signature in `X-Square-Hmacsha256-Signature` header
- **Formula:** `Base64(HMAC-SHA256(notification_url + raw_body, signature_key))`
- **Comparison:** Timing-safe via `hmac.compare_digest()`
- **Request:** Raw JSON body (max 1MB, configurable via `MAX_PAYLOAD_BYTES`). Only `source ∈ {"square"}` accepted.
- **Response 200:** `{"status": "accepted", "event_id": "<ULID>", "received_at": "<ISO8601>"}`
- **Response 200 (duplicate):** `{"status": "accepted", "event_id": "duplicate:<id>", "duplicate": true}`
- **Response 401:** Signature verification failed
- **Response 404:** Unsupported source
- **Response 413:** Payload exceeds size limit
- **Response 503:** Signature key not configured or Valkey unavailable. Includes `retry_after_seconds: 30`

**Critical invariant:** Never return 200 unless the event has been published to the Valkey stream. The stream is the source of truth, not the database.

### GET /webhooks/health
- **Auth:** None
- **Response 200:** `{"status": "healthy", "queue_connected": true, "version": "1.0.0"}`
- **Response 503:** `{"status": "degraded", "queue_connected": false, "version": "1.0.0"}`

### GET /webhooks/ready
- **Auth:** None. Checks queue connection, signature key, and notification URL.
- **Response 200:** `{"status": "ready"}`
- **Response 503:** `{"status": "not_ready", "errors": [...]}`

### GET /webhooks/live
- **Auth:** None. Process liveness probe.
- **Response 200:** `{"status": "alive"}`

### Valkey Stream Messages

**canary:events (9 fields):** `event_id` (ULID), `merchant_id`, `source` ("square"), `source_event_id`, `event_type` (e.g. "payment.created"), `event_hash` (SHA-256 hex), `raw_payload` (UTF-8), `received_at` (ISO 8601), `parse_failed` ("true"/"false").

**canary:detection (5 fields):** `transaction_id` (CDM record PK), `merchant_id`, `event_type`, `event_id` (ULID), `detection_type` ("transaction"/"cash_drawer"/"gift_card"/"loyalty").

### Configuration

| Variable | Required | Default | Purpose |
|----------|:--------:|---------|---------|
| `SQUARE_WEBHOOK_SIGNATURE_KEY` | Yes | — | Per-subscription HMAC key from Square Developer Dashboard |
| `SQUARE_NOTIFICATION_URL` | Yes | — | URL Square posts to — part of HMAC computation |
| `MAX_PAYLOAD_BYTES` | No | 1048576 (1MB) | Maximum acceptable payload size |
| `VALKEY_URL` | Yes | `redis://localhost:6379/0` | Valkey connection (base URL; DB overridden for dedup/streams) |
| `VALKEY_STREAM_DB` | No | 4 | Valkey DB number for streams |
| `VALKEY_STREAM` | No | `canary:events` | Stream name for webhook events |
| `VALKEY_DEAD_LETTER_STREAM` | No | `canary:events:dead` | Dead letter stream name |
| `DETECTION_STREAM` | No | `canary:detection` | Detection routing stream |
| `SQUARE_ACCESS_TOKEN` | No | — | Required for order enrichment only |
| `SQUARE_ENVIRONMENT` | No | `sandbox` | Square API environment for enrichment calls |

## Signature Validation (Type 4)

**Method:** HMAC-SHA256 with timing-safe comparison.

**Key storage:** `SQUARE_WEBHOOK_SIGNATURE_KEY` loaded from environment variable via `os.getenv()`. In dev, stored in `.env` file. In production, must be in AWS Secrets Manager.

**Validation sequence:**
1. Extract `X-Square-Hmacsha256-Signature` header (case-insensitive)
2. If header is empty/missing, return `False` immediately
3. Load signature key from env (raises `RuntimeError` if not configured -> 503)
4. Load notification URL from env (raises `RuntimeError` if not configured)
5. Compute: `Base64(HMAC-SHA256(notification_url + raw_body_utf8, key_utf8))`
6. Compare expected vs received using `hmac.compare_digest()` (timing-safe)

**Key rotation:** Not implemented. Single static key per Square webhook subscription. No rotation procedure documented.

**Source file:** `canary/services/tsp/validators/square.py`

## Retry & Idempotency Strategy (Type 4)

### Square retry behavior
Square retries failed webhook deliveries (non-2xx responses) with exponential backoff for up to 72 hours. Canary must be idempotent to handle retries.

### Idempotency implementation
- **Dedup cache:** Valkey DB 3, key `dedup:{source}:{source_event_id}`, `SET NX` with 24h TTL
- **Fail-open:** If Valkey dedup check fails (connection error), the event is allowed through. The database unique constraint on `(merchant_id, event_id)` in `evidence_records` is the backstop.
- **Duplicate response:** Returns 200 with `"duplicate": true` — Square treats this as successful delivery and stops retrying.
- **No source_event_id:** If the payload has no extractable event ID (parse failure), dedup is skipped entirely. The event is accepted and hashed regardless.

### DLQ and retry (downstream)
- Dead letter stream `canary:dead_letter` for poison messages in consumers
- DLQ retry processor (`canary/services/tsp/dlq_processor.py`): exponential backoff 5s -> 30s -> 5min (3 retries max)
- Exhausted entries remain in `dead_letter_queue` table with full error context

## Degradation Behavior (Type 4)

| Failure | Behavior | Response |
|---------|----------|----------|
| Signature key not configured | Reject all webhooks | 503 + `retry_after_seconds: 30` |
| Notification URL not configured | Reject all webhooks | 503 (via readiness check) |
| Valkey stream (DB 4) unavailable | Reject event (do NOT return 200) | 503 + `retry_after_seconds: 30` |
| Valkey dedup cache (DB 3) unavailable | **Fail open** — allow event through | 200 (DB constraint is backstop) |
| PostgreSQL unavailable (ingestion_log) | Event still accepted — stream write is source of truth | 200 (log failure logged to stderr) |
| JSON parse failure | Accept and hash raw bytes; set `parse_failed=true` | 200 (Sub1 stores raw, Sub2 skips parsing) |
| Square Orders API unavailable (enrichment) | Skip enrichment, use notification-only payload | 200 (best-effort enrichment) |
| Merchant lookup failure | Use Square merchant_id as-is (fallback) | 200 (non-blocking) |
| Stateless chirp evaluation failure | Swallowed — webhook still accepted | 200 (chirps are additive, non-blocking) |

**Design principle:** The webhook endpoint only returns 503 when the Valkey stream is unavailable or HMAC validation cannot be performed. All other failures are non-blocking. Square will retry 503s with backoff.

## Operations

### Startup sequence
1. Flask app starts via `gunicorn wsgi:app --bind 0.0.0.0:5001`
2. On first webhook POST, Valkey stream client is lazily initialized (singleton)
3. Consumer groups must be created before events are published — `init_consumer_groups()` in `stream_publisher.py` creates groups with `$` (only new messages). Called separately.
4. TSP consumers start as independent Docker services after Flask is healthy

### Health checks
- `/webhooks/health` — verifies Valkey stream connectivity (used by load balancers)
- `/webhooks/ready` — verifies Valkey + signature key + notification URL (Kubernetes readiness)
- `/webhooks/live` — process liveness (always returns 200 if Flask is running)
- Flask-level health: `GET /health` (container healthcheck in Docker compose, 10s interval)

### Failure modes
- **Valkey stream down:** All webhooks rejected with 503. Square retries. No data loss if Square retry window (72h) exceeds outage.
- **Valkey dedup cache down:** Duplicates may slip through. `evidence_records` unique constraint prevents double-writes. Benign.
- **PostgreSQL down (ingestion_log):** Events still flow to stream and consumers. Ingestion log gap — consumers are source of truth.
- **Slow consumer processing:** No backpressure on webhook handler. Stream accumulates. Consumers catch up independently.
- **Consumer crash:** Messages stay in PEL (Pending Entry List). Consumer restart reprocesses pending messages.
- **Consecutive consumer errors (10+):** Consumer self-terminates. Docker `restart: unless-stopped` brings it back.

### Monitoring (what to alert on)

| Metric | Normal | Alert Threshold |
|--------|--------|-----------------|
| Webhook response time (p95) | < 50ms | > 500ms |
| 503 responses | 0 | > 5 in 5 minutes |
| 401 responses (HMAC failures) | 0 | > 10 in 1 hour (possible key compromise or misconfiguration) |
| Valkey stream length (`canary:events`) | < 1000 | > 10,000 (consumers falling behind) |
| Dedup cache miss rate | < 1% | > 10% (cache may be down) |
| Consumer heartbeat age | < 30s | > 60s (consumer stalled) |
| DLQ entries (unresolved) | 0 | > 50 (systemic parse/write failure) |
| Schema drift alerts (unresolved) | 0 | Any new alert (Square API changed) |

### Webhook ingest flow (10-step sequence)

```
Square POST -> webhooks_tsp_bp.receive_webhook(source)
  1. raw_bytes = request.get_data()           # BEFORE JSON parse (patent-critical)
  2. Validate source in REGISTERED_SOURCES     # 404 if unknown
  3. Check len(raw_bytes) <= MAX_PAYLOAD_BYTES # 413 if oversized
  4. HMAC-SHA256 verify (timing-safe)          # 401 if invalid, 503 if unconfigured
  5. event_hash = SHA-256(raw_bytes)           # Content-addressable anchor
  6. JSON parse -> merchant_id, event_type     # parse_failed=true if bad JSON
  7. Dedup check: Valkey DB 3 SET NX 24h TTL   # 200+duplicate if seen, fail-open
  7a. Enrichment: fetch full object from API   # order.* events only, best-effort
  7b. Tier 1 stateless Chirps (non-blocking)   # GRO-128, fire-and-forget
  8. event_id = ULID()                         # Canary-internal ID
  9. XADD canary:events (9 fields)             # 503 if Valkey down
 10. INSERT ingestion_log (best-effort)        # Stream is source of truth
 11. Return 200 {event_id, received_at}
```

### Schema drift detection
On each webhook: hash sorted field paths (SHA-256). Known hash -> increment `occurrence_count`. New hash -> diff against latest fingerprint, create `SchemaDriftAlert` (new_fields, missing_fields). Resolution: update parser, mark `is_resolved=true`.

## Deployment

### Docker service definition

The webhook handler runs inside the `flask` service (no dedicated container). TSP consumers run as separate containers using the same image.

```yaml
# From docker-compose.localhost.yml
flask:
  image: canary-flask
  build:
    context: ..
    dockerfile: Dockerfile
  command: gunicorn --bind 0.0.0.0:5001 --workers 1 --threads 4 --timeout 120 --reload wsgi:app
  ports:
    - "127.0.0.1:5001:5001"
  healthcheck:
    test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:5001/health')"]
    interval: 10s
    timeout: 5s
    retries: 5
    start_period: 20s
  restart: unless-stopped
```

TSP consumers (4 containers, same image, different entrypoint):
```yaml
tsp-sub1:
  image: canary-flask
  command: python -m canary.services.tsp.run_consumer --consumer sub1
  healthcheck:
    test: ["CMD", "python", "devops/scripts/tsp_healthcheck.py"]
    interval: 15s
    timeout: 5s
    retries: 3
    start_period: 30s
```

### AWS target architecture
- **Webhook handler:** ECS/Fargate behind ALB. Auto-scaling on request count. ALB health check on `/webhooks/health`.
- **TSP consumers:** ECS/Fargate tasks (1 container per consumer, independently scalable).
- **Valkey:** ElastiCache (Valkey-compatible). DB 3 for dedup, DB 4 for streams.
- **PostgreSQL:** RDS PostgreSQL 17 with Multi-AZ.
- **Secrets:** AWS Secrets Manager for `SQUARE_WEBHOOK_SIGNATURE_KEY`, `SQUARE_NOTIFICATION_URL`, database credentials.
- **TLS:** ALB terminates TLS. Square requires HTTPS notification URLs in production.

### CI/CD requirements
- Container image build and push on merge to main
- Alembic migration check (no pending migrations) before deploy
- Health check validation post-deploy (hit `/webhooks/ready`)
- Consumer group existence verification (`init_consumer_groups()` must run before first event)

## Code Review Findings

### P0 — Blocks Production

**P0-1: Signature key stored in .env file, loaded via `os.getenv()`**
- **File:** `canary/services/tsp/validators/square.py:22-24`
- **Gap:** `SQUARE_WEBHOOK_SIGNATURE_KEY` is read from environment, sourced from `.env` file. In production, secrets must be in AWS Secrets Manager with `boto3` retrieval at startup. A leaked `.env` compromises all webhook authentication.
- **Fix:** Add Secrets Manager integration. Load key at app startup, cache in memory, support rotation signal.
- **Linear:** GRO-TBD

**P0-2: Raw webhook payloads stored with PII in plaintext**
- **File:** `canary/blueprints/webhooks_tsp.py:172-179` (stream publish), `canary/services/tsp/consumers/sub1_seal.py` (evidence_records)
- **Gap:** `raw_payload` is stored verbatim in Valkey stream and `evidence_records.raw_payload`. Payloads contain card fingerprints, card BINs, employee IDs, phone numbers (pre-hash), customer IDs, and device IDs. No field-level redaction or encryption.
- **Fix:** Implement field-level redaction for evidence storage. The hash-before-parse ordering (patent-critical) means `event_hash` is computed on unmodified bytes, but `raw_payload` stored in evidence_records could have sensitive fields masked after hashing.
- **Linear:** GRO-TBD

**P0-3: IP addresses logged in plaintext**
- **File:** `canary/blueprints/webhooks_tsp.py:203` (writes `request.remote_addr`)
- **Gap:** `ingestion_log.ip_address` stores the source IP in plaintext. While these are typically Square infrastructure IPs (not end-user IPs), they still reveal network topology.
- **Fix:** Hash or mask IP addresses before storage. Consider whether IP logging is needed at all — the HMAC validation already authenticates the source.
- **Linear:** GRO-TBD

### P1 — Before GA

**P1-1: No rate limiting on webhook endpoint**
- **File:** `canary/blueprints/webhooks_tsp.py` (entire blueprint)
- **Gap:** Flask-Limiter is configured in the app (`canary/extensions.py`) but no rate limit decorators are applied to `receive_webhook()`. A compromised or misconfigured Square subscription could flood the endpoint.
- **Fix:** Apply rate limiting to `POST /webhooks/<source>`. Suggested: 1000 req/min per source IP. Must not block legitimate Square burst traffic during high-volume periods (Black Friday).
- **Linear:** GRO-TBD

**P1-2: No audit logging for webhook operations**
- **File:** All webhook handling code
- **Gap:** The `ingestion_log` records accepted events, but there is no audit trail for: HMAC validation failures (beyond `logger.warning`), dedup cache failures, enrichment API calls, or stateless chirp alert writes. Production needs structured audit logs that survive log rotation.
- **Fix:** Implement structured audit logging (JSON format) for all security-relevant operations. Forward to centralized logging (CloudWatch Logs / Datadog).
- **Linear:** GRO-TBD

**P1-3: No data retention policy for webhook data**
- **File:** `canary_sales.ingestion_log`, `canary_sales.evidence_records`, `canary_app.webhook_events`
- **Gap:** Webhook data accumulates indefinitely. No automated purge for ingestion logs, evidence records, or dedup cache entries (beyond 24h TTL). Valkey stream has no `MAXLEN` cap.
- **Fix:** Define retention policy: ingestion_log 24 months, evidence_records permanent (legal hold), Valkey stream `MAXLEN ~100000` for bounded memory. Implement automated cleanup job.
- **Linear:** GRO-TBD

**P1-4: Dedup key namespace collision risk**
- **File:** `canary/blueprints/webhooks_tsp.py:287-299`
- **Gap:** Dedup key format is `dedup:{source}:{source_event_id}`. The Valkey client connects to a new `Redis` instance on every dedup check (no connection pooling, no singleton). This creates connection churn under load.
- **Fix:** Use the existing stream client singleton (DB 4) or create a dedup client singleton. The dedup DB (3) should have its own connection pool.
- **Linear:** GRO-TBD

**P1-5: Error responses on /webhooks/ready leak internal details**
- **File:** `canary/blueprints/webhooks_tsp.py:263-264`
- **Gap:** The `/ready` endpoint returns raw exception messages in the `errors` array (e.g., `"queue: Connection refused"`). In production, error details should be logged server-side but not returned to the caller.
- **Fix:** Return generic error categories (`"queue_unavailable"`, `"signature_key_missing"`) instead of raw exception text. Log full details server-side.
- **Linear:** GRO-TBD

### P2 — Post-Launch

**P2-1: No key rotation procedure for webhook signature key**
- **Gap:** Single static `SQUARE_WEBHOOK_SIGNATURE_KEY`. No documented rotation procedure. Square supports multiple active keys during rotation, but Canary validates against only one.
- **Fix:** Document rotation procedure. Support validating against current + previous key during rotation window. Log which key was used for successful validation.
- **Linear:** GRO-TBD

**P2-2: No metrics/observability instrumentation**
- **Gap:** No Prometheus/StatsD metrics emitted. Monitoring relies entirely on log parsing. No request duration histograms, no dedup hit rate counters, no stream publish latency tracking.
- **Fix:** Add OpenTelemetry or StatsD instrumentation to webhook handler. Key metrics: request_duration_seconds, hmac_validation_result, dedup_hit_total, stream_publish_duration_seconds.
- **Linear:** GRO-TBD

**P2-3: Valkey dedup client creates new connection per request**
- **File:** `canary/blueprints/webhooks_tsp.py:286-296`
- **Gap:** `_is_duplicate()` creates a new `Redis.from_url()` connection on every call. Under sustained load (100+ webhooks/sec), this will exhaust file descriptors or create connection storms.
- **Fix:** Create a module-level dedup client singleton (same pattern as `stream_publisher._stream_client`).
- **Linear:** GRO-TBD

**P2-4: Enrichment uses `SQUARE_ACCESS_TOKEN` from env (not per-merchant OAuth token)**
- **File:** `canary/services/tsp/enrichers/square.py:55-56`
- **Gap:** Order enrichment uses a single `SQUARE_ACCESS_TOKEN` from env, not the per-merchant OAuth token stored in `merchant_credentials`. This works for single-merchant dev/sandbox but will fail in multi-tenant production.
- **Fix:** Look up the merchant's OAuth token from `merchant_credentials` based on the `merchant_id` extracted from the webhook payload.
- **Linear:** GRO-TBD

**P2-5: Consumer health checks not wired in QA compose**
- **File:** `Canary/devops/docker-compose.qa.yml`
- **Gap:** TSP consumer health checks exist in localhost compose but are not configured in the QA/enterprise compose file. Tracked as GRO-264.
- **Linear:** GRO-264

## Production Readiness Checklist

- [ ] PII encrypted at rest (P0-2: raw_payload, card_fingerprint, card_bin, ip_address stored plaintext)
- [ ] Secrets in AWS Secrets Manager (P0-1: signature key in .env via os.getenv)
- [x] Health check endpoint responds (`/webhooks/health`, `/webhooks/ready`, `/webhooks/live` all implemented)
- [ ] Audit logging for sensitive operations (P1-2: HMAC failures only logged to stdout)
- [ ] Data retention policy implemented (P1-3: no purge for any webhook data)
- [ ] Rate limiting on public endpoints (P1-1: Flask-Limiter exists but not applied to webhook route)
- [ ] Error responses don't leak internals (P1-5: /ready returns raw exception messages)
- [x] HMAC signature validation with timing-safe comparison (implemented, `hmac.compare_digest()`)
- [x] Idempotency via dedup cache + DB unique constraint (implemented, fail-open design)
- [x] Degradation behavior documented and implemented (503 for critical failures, fail-open for non-critical)
- [x] Consumer heartbeat monitoring (GRO-256, implemented in Valkey)
- [x] Dead letter queue with retry processor (GRO-251, implemented with 3-retry backoff)
- [x] Schema drift detection (implemented, fingerprint + alert system)
- [ ] Key rotation procedure documented (P2-1: single static key, no rotation)
- [ ] Observability instrumentation (P2-2: no metrics, no tracing)
- [ ] Connection pooling for dedup client (P2-3: new connection per request)

## Key Files

| File | Purpose |
|------|---------|
| `canary/blueprints/webhooks_tsp.py` | Webhook receipt blueprint (10-step pipeline) |
| `canary/services/tsp/validators/square.py` | HMAC-SHA256 signature validation |
| `canary/services/tsp/stream_publisher.py` | Valkey stream publish + consumer group init |
| `canary/services/tsp/enrichers/__init__.py` | Source-agnostic enrichment interface |
| `canary/services/tsp/enrichers/square.py` | Square order enrichment (API fetch) |
| `canary/services/tsp/heartbeat.py` | Consumer heartbeat (Valkey-based liveness) |
| `canary/services/tsp/dlq_processor.py` | Dead letter queue retry processor |
| `canary/services/tsp/consumers/sub1_seal.py` | Evidence sealing consumer |
| `canary/services/tsp/consumers/sub2_parse.py` | CDM parsing consumer |
| `canary/services/tsp/consumers/sub3_merkle.py` | Merkle tree batching consumer |
| `canary/services/tsp/consumers/sub4_detect.py` | Detection routing consumer |
| `canary/services/tsp/run_consumer.py` | Consumer CLI entry point |
| `devops/docker-compose.localhost.yml` | Docker service definitions (flask + 4 consumers) |
| `devops/scripts/tsp_healthcheck.py` | Docker health check script for consumers |

---
*Canary | GrowDirect Inc. | Confidential*
