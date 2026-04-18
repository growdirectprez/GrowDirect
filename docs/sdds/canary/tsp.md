# Transaction Stream Processor (TSP) -- Pipeline Overview

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]
**Architecture:** [[docs/sdds/canary/architecture|Canary Architecture SDD]]

> **Type:** App Service (Canary) -- Pipeline Coordinator
> **Status:** Production Readiness Review -- 2026-04-13
> **Code location:** `Canary/canary/services/tsp/`, `Canary/canary/blueprints/webhooks_tsp.py`, `Canary/canary/blueprints/receipt_tsp.py`
> **Patent:** Application #63/991,596 (hash-before-parse, chain hash, Merkle inscription)

---

## Purpose

The Transaction Stream Processor is Canary's core data ingestion pipeline. It receives Square webhook events via HTTP, validates HMAC signatures, computes content-addressable SHA-256 hashes from raw bytes before any parsing, publishes events to a Valkey stream, and fans them out to four independent consumer groups. Each consumer is documented in its own SDD.

## Sub-Consumer SDDs

| Consumer | SDD | Docker Service | Stream | Function |
|----------|-----|----------------|--------|----------|
| Sub 1 -- Hash & Seal | [[docs/sdds/canary/tsp-sub1|TSP Sub 1]] | `tsp-sub1` | `canary:events` | Write-once evidence sealing with chain hashes |
| Sub 2 -- Parse & Route | [[docs/sdds/canary/tsp-sub2|TSP Sub 2]] | `tsp-sub2` | `canary:events` | CRDM record parsing, detection stream publishing |
| Sub 3 -- Merkle Batcher | [[docs/sdds/canary/tsp-sub3|TSP Sub 3]] | `tsp-sub3` | `canary:events` | Merkle tree batching for Bitcoin inscription |
| Sub 4 -- Chirp Detection | [[docs/sdds/canary/tsp-sub4|TSP Sub 4]] | `tsp-sub4` | `canary:detection` | Rule engine evaluation, alert generation |

---

## Dependencies

| Dependency | Role | Required |
|------------|------|----------|
| `growdirect_postgres:5432` | `canary` database (schemas: `canary_sales`, `canary_app`) | Yes |
| `growdirect_valkey:6379` | DB 3: dedup keys (TTL 24h); DB 4: streams (`canary:events`, `canary:detection`, `canary:dead_letter`, `canary:batch:current`, `canary:heartbeat:*`) | Yes |
| Square Webhooks | Event source -- POSTs to `/webhooks/square` | Yes |
| Square Orders API | Synchronous enrichment for `order.*` events | Optional (graceful fallback) |
| `SQUARE_WEBHOOK_SIGNATURE_KEY` | Per-subscription HMAC key from Square Developer Dashboard | Yes (prod) |
| `SQUARE_NOTIFICATION_URL` | Registered webhook URL -- must match for HMAC computation | Yes (prod) |
| Chirp Rule Engine | Sub 4 depends on `canary.services.chirp.rule_engine` | Yes (Sub 4 only) |

---

## Data Flow & PII Map

### Architecture Diagram

```
Square Webhooks
      |
      v
[ POST /webhooks/<source> ]   (Flask -- webhooks_tsp.py)
      |
      | 1. HMAC-SHA256 validate
      | 2. SHA-256 hash raw bytes (patent-critical: hash BEFORE parse)
      | 3. JSON parse + enrich (order events call Square Orders API)
      | 4. Stateless Chirp (Tier 1) -- no DB access
      | 5. Idempotency check (Valkey DB 3, TTL 24h)
      | 6. XADD -> canary:events (Valkey DB 4)
      | 7. INSERT ingestion_log
      |
      v
 canary:events (Valkey Stream DB 4)
      |
      +----------+-----------+
      |          |           |
      v          v           v
  sub1-seal  sub2-parse  sub3-merkle
  (Sub 1)    (Sub 2)     (Sub 3)
      |          |           |
      |          | XADD      |
      |          v           |
      |    canary:detection  |
      |    (Valkey DB 4)     |
      |          |           |
      v          v           v
evidence_  CRDM tables  inscription_pool
records    (canary_sales) + event_inscriptions
                   |
            detection-engine
                (Sub 4)
                   |
                   v
            canary_app.alerts
```

### What Enters

Square sends webhook POST requests containing transaction, order, payment, refund, cash drawer, gift card, loyalty, dispute, invoice, payout, inventory, timecard, device, and terminal event data. Payloads can contain:

- Merchant identifiers (Square merchant_id)
- Card payment data (last4, brand, fingerprint, BIN, expiry, entry method)
- Employee identifiers (team_member_id, names via Team Members API)
- Customer identifiers (customer_id, phone via loyalty)
- Device metadata (serial number, IP address, WiFi SSID)
- Transaction amounts and line item details

### What's Stored -- PII Field Map

| Field | Table(s) | Classification | Encryption | Notes |
|-------|----------|---------------|------------|-------|
| `raw_payload` | `evidence_records` | **restricted** | **NONE (P0)** | Complete webhook JSON including all PII. Write-once, no updates/deletes. |
| `parsed_payload` | `evidence_records` | **restricted** | **NONE (P0)** | Parsed JSON copy of raw_payload. |
| `payload` | `transactions` | **restricted** | **NONE (P0)** | Full webhook payload stored as forensic copy. |
| `card_last4` | `transactions`, `transaction_tenders` | sensitive | NONE (P0) | Last 4 digits of card number. PCI-relevant. |
| `card_fingerprint` | `transactions` | sensitive | NONE (P0) | Square card fingerprint -- pseudonymous but linkable. |
| `card_bin` | `transactions` | sensitive | NONE (P0) | First 6 digits -- issuer BIN. |
| `card_exp_month/year` | `transactions` | sensitive | NONE (P0) | Card expiration date. |
| `employee_id` | Multiple CRDM tables | internal | NONE | Square team_member_id -- maps to employee names. |
| `customer_id` | `transactions` | internal | NONE | Square customer_id -- links to customer PII. |
| `phone_hash` | `loyalty_accounts` | sensitive | SHA-256 (one-way) | Phone number hashed before storage -- good. |
| `ip_address` | `ingestion_log`, `devices` | sensitive | **NONE (P0)** | Source IP of webhook, device IP. |
| `wifi_network_name` | `devices` | internal | NONE | WiFi SSID -- location-identifying. |
| `serial_number` | `devices` | internal | NONE | Device serial number. |
| `primary_recipient` | `invoices` | **sensitive** | **NONE (P0)** | JSONB -- may contain customer name, email, phone, address. |
| `email` | `employees` (via Sub 2 upsert) | **sensitive** | **NONE (P0)** | Employee email stored plaintext. |
| `employee_name` | `employees` (via Sub 2 upsert) | **sensitive** | **NONE (P0)** | Employee display name stored plaintext. |
| `merchant_id` | All tables | internal | NONE | Tenant partition key. |
| `event_hash` | `ingestion_log`, `evidence_records`, `event_inscriptions` | public | NONE | SHA-256 content hash -- not PII. |
| `chain_hash` | `evidence_records` | public | NONE | Derived hash -- not PII. |
| `merkle_root` | `inscription_pool` | public | NONE | Aggregate hash -- not PII. |

### What Exits

| Destination | Data | Classification |
|-------------|------|---------------|
| `canary:events` stream | 9-field queue message including `raw_payload` | restricted (contains full PII) |
| `canary:detection` stream | `{transaction_id, merchant_id, event_type, detection_type}` | internal (IDs only) |
| Receipt endpoints (`/receipt/*`) | Evidence receipt with chain hash, inscription proof | public (hashes only, no PII) |
| MCP tools (`/tsp/*`) | Stream health, ingestion stats, dead letter contents | mixed (DLQ contains raw payloads) |

---

## API Contract

### Webhook Endpoints (`webhooks_tsp_bp` -- registered at `/webhooks`)

**`POST /webhooks/<source>`**
- Request: Raw webhook body (Square JSON format)
- Headers: `X-Square-Hmacsha256-Signature` (required for Square)
- `200`: `{"status": "accepted", "event_id": "<ulid>", "received_at": "<iso8601>"}`
- `200` (dup): `{"status": "accepted", "event_id": "duplicate:<source_event_id>", "duplicate": true}`
- `401`: HMAC validation failed
- `404`: Unknown source
- `413`: Payload exceeds `MAX_PAYLOAD_BYTES` (1 MB)
- `503`: Valkey unavailable -- caller should retry

**`GET /webhooks/health`** -- Returns stream connectivity status
**`GET /webhooks/ready`** -- Readiness probe (checks Valkey, signature key, notification URL)
**`GET /webhooks/live`** -- Liveness probe (always 200)

### Receipt Endpoints (`receipt_tsp_bp` -- registered at `/receipt`)

**`GET /receipt/by-hash/<event_hash_hex>`** -- Lookup by SHA-256 hash
**`GET /receipt/by-event/<event_id>`** -- Lookup by ULID event_id
**`GET /receipt/health`** -- Health check

Receipt responses include: event_hash, chain_hash, chain_position, inscription proof (if available), verification status.

### MCP Tools (`tsp_mcp_bp` -- 7 tools via `canary-tsp` registry)

| Tool | Category | Parameters | Write | Description |
|------|----------|-----------|:-----:|-------------|
| `get_stream_health` | health | none | No | Stream lengths, consumer groups, pending counts |
| `get_dead_letters` | health | `limit` (int, default 20) | No | List failed events from DLQ stream |
| `replay_event` | management | `stream_id` (required) | **Yes** | Replay dead-letter entry back to main stream |
| `get_ingestion_stats` | analytics | `merchant_id`, `hours` | No | Throughput, latency, error rates |
| `get_receipt` | evidence | `event_hash` or `event_id` | No | Sealed evidence receipt with proof |
| `verify_merkle` | evidence | `event_hash`, `proof`, `expected_root` | No | Verify Merkle inclusion proof |
| `process_dead_letters` | management | `batch_size` (default 10) | **Yes** | Process eligible DLQ entries with backoff |

---

## Operations

### Startup Sequence

1. Shared infra must be running: `growdirect_postgres`, `growdirect_valkey`
2. Flask app starts (`canary_flask`) -- registers webhook and receipt blueprints, calls `init_consumer_groups()` to create all 4 consumer groups on `canary:events` and `detection-engine` on `canary:detection`
3. TSP consumers start (depends_on flask healthy): `tsp-sub1`, `tsp-sub2`, `tsp-sub3`, `tsp-sub4`
4. Each consumer defensively creates its own consumer group (catches BUSYGROUP)
5. Sub 4 recovers pending messages from PEL before switching to new messages

### Health Checks

| Service | Endpoint/Mechanism | Interval | Healthy |
|---------|--------------------|----------|---------|
| Webhook gateway | `GET /webhooks/health` | 15s | Valkey stream reachable |
| Webhook readiness | `GET /webhooks/ready` | on-demand | Valkey + signature key + notification URL configured |
| Receipt service | `GET /receipt/health` | 15s | Returns 200 |
| Each consumer | Valkey heartbeat `canary:heartbeat:<name>` (TTL 120s) | Every loop iteration | Heartbeat younger than 60s |
| Docker health | `devops/scripts/tsp_healthcheck.py` | 15s | Reads consumer heartbeat from Valkey |

### Failure Modes

| Failure | Impact | Recovery |
|---------|--------|----------|
| Valkey down | Gateway returns 503, consumers block indefinitely | Consumers reconnect via exponential backoff. Square retries webhooks. |
| PostgreSQL down | Consumers fail on DB writes, do NOT ACK messages | Messages stay in PEL, redelivered when DB recovers. |
| Single consumer crash | Other consumers unaffected (independent groups) | Docker restarts container. PEL messages redelivered. |
| 10 consecutive errors | Consumer stops (raises exception) | Docker restart policy (`unless-stopped`). Requires investigation. |
| HMAC key misconfigured | All webhooks rejected with 401 | Fix env var, restart Flask. |
| Square Orders API down | Order enrichment skipped, unenriched payload published | Graceful degradation -- Sub 2 processes without line items. |

### Monitoring

- **Alert on:** Consumer heartbeat stale >60s, DLQ stream length >0, pending message count growing, ingestion error rate >5%
- **Normal:** DLQ empty, all heartbeats fresh, pending counts near 0, ingestion latency <100ms

---

## Deployment

### Docker Services (from `docker-compose.localhost.yml`)

All consumers share the `canary-flask` image with different entry commands:

| Service | Container | Command | Memory |
|---------|-----------|---------|--------|
| `flask` | `canary_flask` | `gunicorn wsgi:app --bind 0.0.0.0:5001` | 512M |
| `tsp-sub1` | `canary_localhost_tsp_sub1` | `python -m canary.services.tsp.run_consumer --consumer sub1` | (default) |
| `tsp-sub2` | `canary_localhost_tsp_sub2` | `python -m canary.services.tsp.run_consumer --consumer sub2` | (default) |
| `tsp-sub3` | `canary_localhost_tsp_sub3` | `python -m canary.services.tsp.run_consumer --consumer sub3` | (default) |
| `tsp-sub4` | `canary_localhost_tsp_sub4` | `python -m canary.services.tsp.run_consumer --consumer sub4` | (default) |

All consumers depend on `flask: condition: service_healthy`. All use env_file `../.env` plus explicit environment overrides. Network: `growdirect` (external).

### AWS Target

- Flask + consumers: ECS Fargate tasks (1 task per consumer)
- PostgreSQL: RDS PostgreSQL 17
- Valkey: ElastiCache for Redis (Valkey-compatible)
- Secrets: AWS Secrets Manager for `SQUARE_WEBHOOK_SIGNATURE_KEY`, `CANARY_ENCRYPTION_KEY`, `SQUARE_ACCESS_TOKEN`

### CI/CD Requirements

- Consumer image is the same as Flask image -- single build
- Each consumer deployed as a separate ECS service for independent scaling
- Health check: Valkey heartbeat read (not HTTP)

---

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `VALKEY_URL` | `redis://localhost:6379/0` | Base Valkey connection URL |
| `VALKEY_STREAM_DB` | `4` | Stream DB number (isolated from cache DBs 0-3) |
| `VALKEY_STREAM` | `canary:events` | Primary event stream name |
| `VALKEY_DEAD_LETTER_STREAM` | `canary:dead_letter` | Dead letter stream |
| `DETECTION_STREAM` | `canary:detection` | Detection routing stream for Sub 4 |
| `SQUARE_WEBHOOK_SIGNATURE_KEY` | (required) | Per-subscription HMAC key |
| `SQUARE_NOTIFICATION_URL` | (required) | Registered webhook URL |
| `SQUARE_ACCESS_TOKEN` | (optional) | For order enrichment |
| `SQUARE_ENVIRONMENT` | `sandbox` | Controls which Square API endpoint is called |
| `MAX_PAYLOAD_BYTES` | `1048576` | Max webhook payload size (1 MB) |
| `DATABASE_URL` / `CANARY_DB_URL` | (required) | PostgreSQL connection string |
| `SUB1_BLOCK_MS` | `5000` | Sub 1 XREADGROUP blocking timeout |
| `SUB2_BLOCK_MS` | `5000` | Sub 2 XREADGROUP blocking timeout |
| `SUB3_BLOCK_MS` | `2000` | Sub 3 XREADGROUP blocking timeout |
| `SUB4_BLOCK_MS` | `5000` | Sub 4 XREADGROUP blocking timeout |
| `BATCH_COUNT_THRESHOLD` | `100` | Sub 3 Merkle batch flush count |
| `BATCH_TIME_THRESHOLD_SECONDS` | `600` | Sub 3 Merkle batch flush time (10 min) |
| `MOCK_INSCRIPTION` | `true` | Sub 3 mock OrdinalsBot responses (Sprint 6) |
| `CANARY_ENCRYPTION_KEY` | (required prod) | AES-256-GCM key for token encryption |

**Socket timeout rule:** Valkey stream client uses `socket_timeout=30s`, which must exceed the max `XREADGROUP block_ms` (5s) by a safe margin.

---

## Shared Service Layer

### `stream_publisher.py`
Singleton Valkey client (DB 4, `socket_timeout=30`, `socket_connect_timeout=5`). Exports:
- `get_stream_client()` -- lazy-initialized stream client
- `init_consumer_groups()` -- creates all consumer groups (safe to call multiple times)
- `publish_event(...)` -- XADD to `canary:events` (9-field TSP-01 schema)
- `publish_detection_event(...)` -- XADD to `canary:detection` (5 fields)

### `validators/square.py`
HMAC-SHA256 validation: `Base64(HMAC-SHA256(notification_url + raw_body, signature_key))` with timing-safe comparison via `hmac.compare_digest`.

### `enrichers/square.py`
Order webhook enrichment -- fetches full order from Square Orders API synchronously. Falls back gracefully if token absent or API fails.

### `heartbeat.py`
Valkey-based liveness: `canary:heartbeat:<consumer_name>` with TTL 120s. Best-effort writes (swallows errors). `check_heartbeat()` returns True if younger than 60s.

### `run_consumer.py`
CLI entry point: `python -m canary.services.tsp.run_consumer --consumer <sub1|sub2|sub3|sub4>`. Creates minimal Flask app (DB config only, no blueprints/security).

### `dlq_processor.py`
Processes `DeadLetterQueue` DB rows with exponential backoff (5s, 30s, 5min). After 3 retries, marks as exhausted.

### `merkle.py`
Deterministic Merkle tree construction (algorithm version 1). Sorted hex-ascending leaves, duplicate-last-leaf padding to power of 2, double-hashing (SHA-256) for second-preimage attack prevention.

### `crypto.py` (shared utility)
AES-256-GCM encryption for OAuth tokens. Key from `CANARY_ENCRYPTION_KEY` (base64-encoded 32 bytes). Supports Fernet legacy migration. Currently used only for OAuth tokens -- **not used for any TSP data fields** (P0 finding).

---

## Code Review Findings

### P0 -- Blocks Production

| # | Finding | Description | Recommended Fix |
|---|---------|-------------|-----------------|
| P0-TSP-01 | **Raw payloads stored plaintext with full PII** | `evidence_records.raw_payload` and `evidence_records.parsed_payload` contain complete webhook JSON including card data, customer IDs, employee names, IP addresses. No encryption at rest. This is the highest PII density in the platform -- every webhook payload is preserved verbatim. | Encrypt `raw_payload` and `parsed_payload` with AES-256-GCM using the existing `crypto.py` pattern before INSERT. Decrypt on read in evidence audit workflows only. |
| P0-TSP-02 | **Transaction.payload stored plaintext** | `transactions.payload` stores a full copy of the webhook JSON as forensic evidence. Same PII as evidence_records but in a second location. | Encrypt with AES-256-GCM or remove the forensic copy (evidence_records already holds the original). |
| P0-TSP-03 | **Card data fields not encrypted** | `card_last4`, `card_fingerprint`, `card_bin`, `card_exp_month`, `card_exp_year` in `transactions` are stored plaintext. PCI DSS requires encryption at rest for card data elements. | Field-level AES-256-GCM encryption on card_* fields. Create encrypted column type or use application-level encrypt/decrypt. |
| P0-TSP-04 | **Employee PII stored plaintext** | Sub 2 upserts employee records with `employee_name` and `email` in plaintext. Employee names are also in `raw_payload`. | Encrypt `employee_name` and `email` fields. Consider hashing email for lookup and encrypting the display value. |
| P0-TSP-05 | **IP addresses stored plaintext** | `ingestion_log.ip_address` and `devices.ip_address` store raw IP addresses. | Hash or encrypt IP addresses. For audit purposes, use HMAC with a rotating key. |
| P0-TSP-06 | **Invoice recipient PII in JSONB** | `invoices.primary_recipient` is a JSONB field that may contain customer name, email, phone, and mailing address from Square's Invoice API. Stored plaintext. | Encrypt the entire JSONB blob or extract and encrypt individual PII fields. |
| P0-TSP-07 | **Encryption key in .env file** | `CANARY_ENCRYPTION_KEY` is loaded from `.env` via `os.getenv()`. In production, secrets must not be in environment files on disk. | Move to AWS Secrets Manager. Load at startup via `boto3`. |
| P0-TSP-08 | **SQUARE_WEBHOOK_SIGNATURE_KEY in .env** | HMAC signing key loaded from environment. Compromise allows forged webhooks. | Move to AWS Secrets Manager. |
| P0-TSP-09 | **DLQ replay_event MCP tool has no auth** | The `replay_event` tool re-publishes events to the main stream. No authentication or authorization check on who can trigger replays. | Require authenticated MCP session with admin role. |
| P0-TSP-10 | **Raw payload in Valkey stream (in-transit PII)** | The 9-field queue message includes `raw_payload` as a plaintext string in Valkey. Valkey has no TLS or AUTH configured in dev. | Enable Valkey AUTH + TLS in production. Consider encrypting `raw_payload` before XADD. |

### P1 -- Before GA

| # | Finding | Description | Recommended Fix |
|---|---------|-------------|-----------------|
| P1-TSP-01 | **No audit logging for evidence access** | Receipt endpoints return sealed evidence (including chain hashes and inscription proofs) with no audit trail of who accessed what. | Add audit log entries for receipt lookups: who, when, which event_hash. |
| P1-TSP-02 | **No data retention policy** | Evidence records, CRDM tables, and ingestion logs grow indefinitely. No automated purge or archival. | Define retention windows: evidence 7 years (SOX), CRDM 24 months, ingestion_log 12 months, DLQ 90 days. Implement automated archival. |
| P1-TSP-03 | **No rate limiting on webhook endpoint** | `POST /webhooks/<source>` has no rate limiting. A malicious or misconfigured Square webhook subscription could flood the pipeline. | Add Flask-Limiter on webhook endpoint. Square's retry behavior is bounded, but defense-in-depth requires rate limiting. |
| P1-TSP-04 | **Consumer memory limits not set** | TSP consumer Docker services have no `deploy.resources.limits.memory` configured. A memory leak could consume host memory. | Set memory limits (256M per consumer is reasonable). |
| P1-TSP-05 | **No structured logging format** | Consumers use Python `logging` with basic format. Production requires JSON-structured logs for CloudWatch/Datadog ingestion. | Switch to JSON log formatter. Include `event_id`, `merchant_id`, `consumer` as structured fields. |
| P1-TSP-06 | **Dual DLQ mechanisms not synchronized** | Valkey stream `canary:dead_letter` (immediate quarantine by Sub 1) and `dead_letter_queue` PostgreSQL table (scheduled retry) are independent. Events can be in one but not the other. | Unify: write to both on quarantine, or use DB table as single source of truth with Valkey stream as a notification channel. |
| P1-TSP-07 | **Error responses may leak internals** | Gateway error responses include raw exception messages in some paths (e.g., `RuntimeError` from missing signature key). | Sanitize error responses. Log full errors server-side, return generic messages to callers. |

### P2 -- Post-Launch

| # | Finding | Description | Recommended Fix |
|---|---------|-------------|-----------------|
| P2-TSP-01 | **No key rotation procedure** | `CANARY_ENCRYPTION_KEY` has no documented rotation process. Rotating requires re-encrypting all stored tokens. | Document rotation procedure. Implement dual-key read (old+new) during rotation window. |
| P2-TSP-02 | **Valkey stream unbounded growth** | `canary:events` stream has no MAXLEN. Long-running streams consume increasing memory. | Add `MAXLEN ~10000` to XADD calls (approximate trimming). |
| P2-TSP-03 | **Mock inscription still default** | `MOCK_INSCRIPTION=true` is the default. Production requires real OrdinalsBot API integration (spend gate pending). | Complete OrdinalsBot integration when spend gate approved. |
| P2-TSP-04 | **Consumer scaling limited to 1** | Each consumer group has 1 worker. Sub 2 and Sub 4 could benefit from horizontal scaling. Sub 1 is limited to 1 by advisory lock design. | Implement consumer-per-shard for Sub 2/Sub 4. Document Sub 1's single-worker constraint. |
| P2-TSP-05 | **No metrics/tracing integration** | No OpenTelemetry spans or Prometheus metrics on the pipeline. | Add OTEL spans for gateway, each consumer stage. Export pipeline latency, throughput, error rate metrics. |

---

## Production Readiness Checklist

- [ ] PII encrypted at rest (P0-TSP-01 through P0-TSP-06)
- [ ] Secrets in AWS Secrets Manager (P0-TSP-07, P0-TSP-08)
- [ ] Health check endpoint responds (DONE -- `/webhooks/health`, `/webhooks/ready`, `/webhooks/live`)
- [ ] Consumer health checks functional (DONE -- Valkey heartbeat + Docker healthcheck script)
- [ ] Audit logging for sensitive operations (P1-TSP-01)
- [ ] Data retention policy implemented (P1-TSP-02)
- [ ] Rate limiting on public endpoints (P1-TSP-03)
- [ ] Error responses don't leak internals (P1-TSP-07)
- [ ] Consumer memory limits configured (P1-TSP-04)
- [ ] Structured JSON logging (P1-TSP-05)
- [ ] Valkey AUTH + TLS in production (P0-TSP-10)
- [ ] MCP tools require authentication (P0-TSP-09)
- [ ] Stream MAXLEN configured (P2-TSP-02)
