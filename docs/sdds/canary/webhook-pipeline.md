# Webhook Pipeline

## Overview

The Webhook Pipeline is Canary's data ingestion front door. Every external event entering the system passes through this domain: HMAC-validated, hashed, streamed, parsed, sealed, and scored.

**Entry point:** `POST /webhooks/<source>` receives Square webhook POSTs. The blueprint `webhooks_tsp_bp` (`canary/blueprints/webhooks_tsp.py`) performs a strict 10-step sequence: read raw bytes, validate source, check payload size (1MB max), verify HMAC-SHA256 signature (timing-safe `hmac.compare_digest()`), compute SHA-256 hash of raw bytes **before** JSON parsing (patent-critical ordering), parse JSON for routing fields, idempotency check via Valkey DB 3 (`SET NX`, 24h TTL), generate ULID event_id, fire Tier 1 stateless Chirps (GRO-128, non-blocking), publish 9-field message to Valkey Stream `canary:events` (DB 4), write `ingestion_log`, return 200 with event_id.

**Consumer pipeline:** Four stream consumers run as independent Docker services via `python -m canary.services.tsp.run_consumer --consumer sub1|sub2|sub3|sub4`. Each uses `XREADGROUP` blocking reads with independent consumer groups on the `canary:events` stream (Sub1-3) or `canary:detection` stream (Sub4):

- **Sub1 (sub1-seal):** Verifies event hash integrity, computes per-merchant chain hash (`SHA-256(prev_chain_hash || event_hash)`), writes write-once `evidence_records`. Uses `pg_advisory_xact_lock` per merchant for serialization. Hash mismatches are tamper alerts routed to dead letter stream.
- **Sub2 (sub2-parse):** Routes events via `webhook_dispatch.resolve_route(event_type)` to the Square parser suite (6 parser modules, 12 parse functions). Builds SQLAlchemy CDM model instances and writes to `canary_sales`. Updates `ingestion_log` status to "parsed". Publishes detection-eligible events to `canary:detection` stream.
- **Sub3 (sub3-merkle):** Accumulates event hashes in Valkey sorted set `canary:batch:current`. Flushes at count >= 100 or elapsed >= 600s. Builds deterministic Merkle tree (sorted hex, double-hash leaves, power-of-2 padding). Writes `inscription_pool` + `event_inscriptions` with proof paths. Mock Bitcoin inscription in Sprint 6.
- **Sub4 (detection-engine):** Reads from `canary:detection`, routes by `detection_type` (transaction/cash_drawer/gift_card/loyalty) to `ChirpRuleEngine`. Dual-session: reads from `canary_sales`, writes alerts to `canary_app`.

**Square parser suite:** Pure functions (JSON dict in, flat dict out, no side effects). Six modules: `square_payment_parser` (payments + refunds), `square_order_parser` (orders + line items + tenders), `square_loyalty_parser` (accounts + events with PII-hashed phone), `square_payout_parser`, `square_dispute_parser`, `square_auxiliary_parsers` (cash drawer shifts/events, timecards, inventory, gift cards). All under `canary/services/parsers/`.

**Receipt blueprint:** `receipt_tsp_bp` (`canary/blueprints/receipt_tsp.py`) at `/api/receipt` exposes `GET /by-hash/<event_hash_hex>` and `GET /by-id/<event_id>` for sealed evidence + inscription proof lookup.

**Schema drift detection:** Fingerprints webhook payloads by hashing sorted field paths. New variants create `SchemaFingerprint` + `SchemaDriftAlert` records. Known variants increment `occurrence_count`. Unresolved drift alerts surface in DevOps dashboard.

**Key files:** `canary/blueprints/webhooks_tsp.py`, `canary/blueprints/receipt_tsp.py`, `canary/services/tsp/stream_publisher.py`, `canary/services/tsp/consumers/sub1_seal.py`, `canary/services/tsp/consumers/sub2_parse.py`, `canary/services/tsp/consumers/sub3_merkle.py`, `canary/services/tsp/consumers/sub4_detect.py`, `canary/services/tsp/validators/square.py`, `canary/services/tsp/merkle.py`, `canary/services/tsp/run_consumer.py`, `canary/services/webhook_dispatch.py`, `canary/services/evidence_chain.py`, `canary/services/parsers/square_*.py`.

## API Contracts

### POST /webhooks/\<source\>
- **Auth:** HMAC-SHA256 signature in `X-Square-Hmacsha256-Signature` header. Formula: `Base64(HMAC-SHA256(notification_url + raw_body, signature_key))`. Timing-safe comparison via `hmac.compare_digest()`.
- **Request:** Raw JSON body (max 1MB, configurable via `MAX_PAYLOAD_BYTES`). Only registered sources accepted (`REGISTERED_SOURCES = {"square"}`).
- **Response 200:** `{"status": "accepted", "event_id": "<ULID>", "received_at": "<ISO8601>"}`
- **Response 200 (duplicate):** `{"status": "accepted", "event_id": "duplicate:<id>", "duplicate": true}`
- **Response 401:** Signature verification failed.
- **Response 404:** Unsupported source.
- **Response 413:** Payload exceeds size limit.
- **Response 503:** Signature key not configured or Valkey unavailable. Includes `retry_after_seconds: 30`.

**Critical invariant:** Never return 200 unless the event has been published to the Valkey stream. The stream is the source of truth, not the database.

### GET /webhooks/health
- **Auth:** None.
- **Response 200:** `{"status": "healthy", "queue_connected": true, "version": "1.0.0"}`
- **Response 503:** `{"status": "degraded", "queue_connected": false, "version": "1.0.0"}`

### GET /webhooks/ready
- **Auth:** None. Checks queue connection, signature key, and notification URL.
- **Response 200:** `{"status": "ready"}`
- **Response 503:** `{"status": "not_ready", "errors": [...]}`

### GET /webhooks/live
- **Auth:** None. Process liveness probe.
- **Response 200:** `{"status": "alive"}`

### GET /api/receipt/by-hash/\<event_hash_hex\>
- **Auth:** JWT. Looks up sealed evidence record + inscription proof by SHA-256 hex hash.
- **Response 200:** Evidence record with chain hash, Merkle proof path, inscription status.
- **Response 404:** Event not found.

### GET /api/receipt/by-id/\<event_id\>
- **Auth:** JWT. Same as above but queried by ULID event_id.

### Valkey Stream Messages

**canary:events (9 fields):** `event_id` (ULID), `merchant_id`, `source` ("square"), `source_event_id`, `event_type` (e.g. "payment.created"), `event_hash` (SHA-256 hex), `raw_payload` (UTF-8), `received_at` (ISO 8601), `parse_failed` ("true"/"false").

**canary:detection (5 fields):** `transaction_id` (CDM record PK), `merchant_id`, `event_type`, `event_id` (ULID), `detection_type` ("transaction"/"cash_drawer"/"gift_card"/"loyalty").

### CLI Entry Point
`python -m canary.services.tsp.run_consumer --consumer sub1|sub2|sub3|sub4` — each consumer runs as a Docker Compose service with independent scaling.

### Configuration
`SQUARE_WEBHOOK_SIGNATURE_KEY` (required), `SQUARE_NOTIFICATION_URL` (required), `MAX_PAYLOAD_BYTES` (1MB), `VALKEY_URL`, `VALKEY_STREAM_DB` (4), `VALKEY_STREAM` ("canary:events"), `DETECTION_STREAM` ("canary:detection"), `VALKEY_DEAD_LETTER_STREAM` ("canary:dead_letter"), `BATCH_COUNT_THRESHOLD` (100), `BATCH_TIME_THRESHOLD_SECONDS` (600), `MOCK_INSCRIPTION` (true), `SQUARE_API_VERSION` (2026-01-22).

## Data Model

### canary_app schema (3 tables)

**webhook_events** — Raw Square webhook payload storage, append-only. Columns: `id` (UUID4 PK), `merchant_id` (TenantMixin), `event_id` (UNIQUE, Square event_id), `event_type`, `payload` (Text, raw JSON), `processed_at` (nullable), `processing_status` ("pending"/"processed"/"failed"), `error_message` (nullable). Indexes: `(merchant_id, event_type)`, `(merchant_id, processing_status)`. Lifecycle: pending -> processed | failed.

**schema_fingerprints** — Event schema signature tracking, not tenant-scoped. Columns: `id` (UUID4 PK), `event_type`, `payload_hash` (SHA-256 of sorted field set, UNIQUE), `field_paths` (JSON of all field names), `first_seen_at`, `last_seen_at`, `occurrence_count` (default 1). Index: `(event_type)`.

**schema_drift_alerts** — Alerts when Square API structure changes. Columns: `id` (UUID4 PK), `event_type`, `new_fields` (JSON), `missing_fields` (JSON), `payload_hash` (SHA-256), `detected_at`, `is_resolved` (default false). Indexes: `(event_type)`, `(is_resolved)`.

### canary_sales schema (19 tables) — WRITE-ONCE IMMUTABLE (trigger-enforced)

**ingestion_log** — Every accepted webhook gets logged. Columns: `merchant_id`, `source`, `event_id` (ULID), `source_event_id`, `event_type`, `event_hash` (BYTEA), `received_at`, `processed_at` (null until Sub2), `status` ("accepted" -> "parsed"), `ip_address`, `user_agent`.

**etl_batches** — Batch grouping for ingestion tracking. Types: WEBHOOK, INITIAL_SYNC, DAILY_REFRESH, BACKFILL. Lifecycle: running -> completed | partial | failed.

**dead_letter_queue** — Events that exhausted retries (3 attempts: 5s, 30s, 5min). Methods: `list_dead_letters`, `replay_dead_letter`, `replay_all`, `resolve`. Retry strategy: exponential backoff, then DLQ with full error context.

**evidence_records** — Write-once sealed evidence (Sub1). Columns: `id` (SERIAL PK), `event_id` (ULID), `merchant_id`, `source`, `source_event_id`, `event_type`, `event_hash` (BYTEA 32 bytes), `chain_hash` (BYTEA 32 bytes), `previous_chain_hash` (BYTEA, NULL for genesis), `raw_payload` (TEXT), `parsed_payload` (JSONB, NULL if parse_failed), `parse_failed` (BOOLEAN), `received_at`. Constraint: UNIQUE `(merchant_id, event_id)`. No UPDATEs or DELETEs.

**inscription_pool** — Merkle batch records (Sub3). Columns: `batch_id` (ULID PK), `merkle_root` (BYTEA 32 bytes), `batch_event_count`, `padded_leaf_count`, `tree_depth`, `tree_algorithm_version` (1), `status` ("tree_built" -> "confirmed"), `inscription_id`, `bitcoin_txid`, `bitcoin_block`, `block_explorer_url`, `fee_sats`, batch timestamps.

**event_inscriptions** — Per-event Merkle proof paths (Sub3). Columns: `event_hash` (BYTEA), `event_id` (ULID), `merchant_id`, `batch_id` (FK to inscription_pool), `leaf_index`, `merkle_proof_path` (JSONB: siblings + root + leaf_hash + depth).

**transactions** — Core CDM table. Source domains: payments, refunds, orders. Columns include: `id` (UUID4), `merchant_id`, `external_id` (Square ID), `transaction_type` (SALE/RETURN/VOID/POST_VOID/NO_SALE), `amount_cents`, `card_fingerprint`, `risk_level`, `entry_method`, `processing_fee_cents`, `employee_id`, `location_id`, `transaction_date`. ON CONFLICT `(merchant_id, external_id)` DO NOTHING.

**transaction_line_items** — Order line items. FK to transactions.id. Columns: `catalog_object_id`, `item_name`, `quantity`, `gross_sales_cents`, `discount_cents`, `tax_cents`, `is_voided` (derived from returns cross-reference), `return_reason`.

**transaction_tenders** — Payment tenders. FK to transactions.id. Columns: `tender_type` (CARD/CASH/etc), `amount_cents`, `card_brand`, `card_last4`, `payment_id`.

**refund_links** — Junction: refund -> original payment. Columns: `refund_external_id`, `original_external_id`, `refund_amount_cents`, `reason`.

**cash_drawer_shifts** — Shift-level cash management. Columns: `expected_cash_cents`, `actual_cash_cents`, `cash_variance_cents` (computed: actual - expected), employee attribution.

**cash_drawer_events** — Individual cash events (adds, removes, etc.).

**gift_card_activities** — Load/redeem activities. Columns: `activity_type`, `balance_after_cents`, `amount_cents`.

**loyalty_accounts** — Columns: `square_loyalty_id`, `phone_hash` (SHA-256 of phone, PII protection), `points_balance`, `lifetime_points`.

**loyalty_events** — Columns: `event_type` (ACCUMULATE/REDEEM/ADJUST/EXPIRE), `points` (positive for accrual, negative for redemption/expiry).

**disputes** — Columns: `square_dispute_id`, `payment_id`, `order_id`, `reason`, `state`, `amount_cents`, `due_at`, `reported_at`.

**payouts** — Columns: `square_payout_id`, `status` (SENT/PAID/FAILED), `destination_type`, `amount_cents`, `arrival_date`, `failure_reason`.

**inventory_adjustments** — Columns: `adjustment_type` (PHYSICAL_COUNT/ADJUSTMENT), `quantity_change`.

**employee_timecards** — Columns: `clock_in`, `clock_out`, `breaks_json`, `hourly_rate_cents`.

All 19 canary_sales tables follow WRITE-ONCE IMMUTABLE pattern enforced by PostgreSQL triggers. Data enters only via TSP consumer pipeline (webhook) or initial data sync (batch). No direct writes permitted (SOX compliance).

## Workflows

### Webhook Ingest Flow (end-to-end)

```
Square POST → webhooks_tsp_bp.receive_webhook(source)
  1. raw_bytes = request.get_data()           # BEFORE JSON parse (patent-critical)
  2. Validate source ∈ REGISTERED_SOURCES      # 404 if unknown
  3. Check len(raw_bytes) <= MAX_PAYLOAD_BYTES  # 413 if oversized
  4. HMAC-SHA256 verify (timing-safe)           # 401 if invalid, 503 if unconfigured
  5. event_hash = SHA-256(raw_bytes)            # Content-addressable anchor
  6. JSON parse → merchant_id, event_type       # parse_failed=true if bad JSON
  7. Dedup check: Valkey DB 3 SET NX 24h TTL    # 200+duplicate if seen, fail-open
  8. event_id = ULID()                          # Canary-internal ID
  8b. Tier 1 stateless Chirps (non-blocking)    # GRO-128, fire-and-forget
  9. XADD canary:events (9 fields)              # 503 if Valkey down
  10. INSERT ingestion_log (best-effort)         # Stream is source of truth
  11. Return 200 {event_id, received_at}
```

### Consumer Pipeline (4-stage, independent consumer groups)

**Sub1 — Seal (evidence writer):**
1. XREADGROUP sub1-seal from canary:events (block 5s, batch 1)
2. Validate 9 required fields; malformed -> dead letter stream + ACK
3. Recompute SHA-256(raw_payload), compare to event_hash; mismatch = TAMPER DETECTED -> dead letter
4. Parse raw_payload to JSON for parsed_payload column
5. pg_advisory_xact_lock(merchant_id) for chain serialization
6. Read previous chain_hash for merchant (ORDER BY id DESC LIMIT 1)
7. Compute chain_hash: genesis = SHA-256(event_hash), subsequent = SHA-256(prev_chain_hash || event_hash)
8. INSERT evidence_records (write-once, immutable)
9. XACK on success; duplicate (unique constraint) -> ACK silently; error -> no ACK (redelivery via PEL)

**Sub2 — Parse (CDM writer):**
1. XREADGROUP sub2-parse from canary:events (block 5s, batch 1)
2. Skip if parse_failed=true
3. Route via webhook_dispatch.resolve_route(event_type) -> parser function + CDM model + detection_type
4. Log-only routes: ACK immediately
5. Call parser, _build_models() constructs SQLAlchemy instances (handles refunds: Transaction+RefundLink; orders: Transaction+LineItems+Tenders; standard: single model)
6. Write to canary_sales
7. Update ingestion_log.status = "parsed"
8. If detection_type present: XADD canary:detection (5 fields) for Sub4
9. XACK; duplicates ACK silently

**Sub3 — Merkle (batcher):**
1. XREADGROUP sub3-merkle from canary:events (block 2s, batch 1)
2. Add event_hash to Valkey sorted set canary:batch:current (score=timestamp)
3. DO NOT XACK during accumulation — track pending msg IDs
4. Flush when count >= 100 OR elapsed >= 600s:
   a. Read all accumulator entries, sort hashes by hex ascending
   b. Build Merkle tree: double-hash leaves, pad to power-of-2
   c. BEGIN: INSERT inscription_pool + event_inscriptions with proof paths
   d. COMMIT, XACK all pending, clear accumulator
5. Mock inscription (Sprint 6): deterministic fake Bitcoin values

**Sub4 — Detect (Chirp evaluation):**
1. XREADGROUP detection-engine from canary:detection (block 5s, batch 1)
2. Route by detection_type:
   - "transaction" -> engine.evaluate_readonly(txn, merchant_id)
   - "cash_drawer" -> engine.evaluate_cash_drawer(record_id, merchant_id)
   - "gift_card" -> engine.evaluate_gift_card_activity(record_id, merchant_id)
   - "loyalty" -> engine.evaluate_loyalty_event(record_id, merchant_id)
3. If alerts: write_alerts_to_session(alerts, merchant_id, app_session) + commit
4. XACK; record not found -> ACK (don't retry missing data)
5. Dual-session: canary_sales for reads, canary_app for alert writes

### Error Handling (all consumers)
Consecutive error limit: 10 -> shutdown. Backoff: min(2^(errors-1), 30)s. XACK only on success; failed messages stay in PEL for redelivery. Dead letter stream `canary:dead_letter` for poison messages. Consumer groups auto-created with BUSYGROUP guard.

### Dead Letter Queue
Retry strategy: 5s -> 30s -> 5min -> DLQ (dead_letter_queue in canary_sales). Methods: list, replay single, replay all, resolve. Metrics queryable from ingestion_log + etl_batches.

### DLQ Retry Processor (GRO-251)

- **Module:** `canary/services/tsp/dlq_processor.py`
- Exponential backoff retry for dead-lettered events
- Backoff calculation module computes delay per attempt
- MCP tool (`canary-ops`) exposes manual retry for individual or batch DLQ entries
- Retries re-enter the consumer pipeline at the failed stage
- Exhausted retries remain in `dead_letter_queue` with full error context

### TSP Consumer Heartbeat (GRO-256)

- **Module:** `canary/services/tsp/heartbeat.py`
- Heartbeat module wired into all 4 consumers (sub1-seal, sub2-parse, sub3-merkle, sub4-detect)
- Each consumer emits periodic heartbeat to Valkey for liveness tracking
- **Docker health check script:** `devops/scripts/tsp_healthcheck.py` — queries heartbeat state per consumer
- Health checks not yet wired in QA compose (tracked as GRO-264)

### Schema Drift Detection
On each webhook: hash sorted field paths (SHA-256). Known hash -> increment occurrence_count. New hash -> diff against latest fingerprint, create SchemaDriftAlert (new_fields, missing_fields). Resolution: update parser, mark is_resolved=true.

### Initial Data Sync
Post-OAuth, `OnboardingCoordinator` registers 27 webhook event types, pulls 90-day history across 10 Square domains, computes merchant baselines. Sync records tagged `source_type="BATCH"`. Error-isolated per domain. Gated by `CANARY_ONBOARDING_SYNC`.

---
*Canary | GrowDirect Inc. | Confidential*
