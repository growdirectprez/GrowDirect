# TSP Sub 1 -- Hash & Seal Evidence Writer

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]
**Architecture:** [[docs/sdds/canary/architecture|Canary Architecture SDD]]
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[docs/team/Architect|Architect]] · **Operator role:** [[docs/team/Engineer|Engineer]]

> **Type:** App Service (Canary) -- Stream Consumer
> **Parent SDD:** [[docs/sdds/canary/tsp|TSP Pipeline Overview]]
> **Status:** Production Readiness Review -- 2026-04-13
> **Code location:** `Canary/canary/services/tsp/consumers/sub1_seal.py`
> **Patent:** FIG. 1 Node 3, FIG. 2 T+15ms Sub 1 lane

---

## Purpose

Sub 1 is the forensic evidence writer. It reads each event from the `canary:events` stream, re-verifies the SHA-256 hash of the raw payload, computes a chain hash linking the event to its predecessor within the same merchant, and inserts a write-once `EvidenceRecord`. The evidence table is enforced as INSERT-only at the database layer via triggers -- no updates, no deletes. This creates a tamper-evident, sequentially-linked record of every webhook received.

## Dependencies

| Dependency | Role | Required |
|------------|------|----------|
| Valkey DB 4 | Reads from `canary:events` stream, writes to `canary:dead_letter` | Yes |
| PostgreSQL (`canary` DB, `canary_sales` schema) | Writes to `evidence_records`, reads previous `chain_hash` | Yes |
| `evidence_chain.compute_chain_hash()` | Chain hash computation function | Yes |

---

## Data Flow & PII Map

### What Enters

9-field queue message from `canary:events` (TSP-01 schema):
- `event_id`, `merchant_id`, `source`, `source_event_id`, `event_type`
- `event_hash` (hex SHA-256), `raw_payload` (complete webhook JSON), `received_at`, `parse_failed`

### What's Stored

**`evidence_records`** table (write-once, INSERT-only):

| Field | Classification | Encryption | Notes |
|-------|---------------|------------|-------|
| `raw_payload` | **restricted** | **NONE (P0)** | Verbatim webhook payload as UTF-8 TEXT. Contains all PII from the original webhook. |
| `parsed_payload` | **restricted** | **NONE (P0)** | JSONB parse of raw_payload (NULL if parse_failed). Same PII content. |
| `event_hash` | public | N/A | SHA-256 of raw payload (32 bytes BYTEA). Not PII. |
| `chain_hash` | public | N/A | SHA-256(previous_chain_hash \|\| event_hash). Derived. |
| `previous_chain_hash` | public | N/A | NULL for genesis record. |
| `merchant_id` | internal | NONE | Tenant partition key. |
| `source_event_id` | internal | NONE | Square's event_id. |
| `event_type` | public | NONE | e.g., `payment.created`. |
| `event_id` | public | NONE | ULID from gateway. |

**`dead_letter_queue`** (Valkey stream `canary:dead_letter`):

| Field | Classification | Encryption | Notes |
|-------|---------------|------------|-------|
| All original 9 fields | restricted | NONE | Quarantined event with full payload. |
| `dead_letter_reason` | internal | NONE | Why it was quarantined. |

### What Exits

Nothing. Sub 1 is a terminal writer. It does not publish to any downstream stream or service. Evidence records are read-only by receipt endpoints and MCP tools.

---

## API Contract

Sub 1 exposes no HTTP endpoints. It is a Valkey stream consumer only.

**Consumer Group:** `sub1-seal`
**Stream:** `canary:events` (Valkey DB 4)
**Batch Size:** 1 (MUST be 1 -- enforced in code for chain integrity)
**Block Timeout:** `SUB1_BLOCK_MS` (default 5000ms)

---

## Operations

### Processing Sequence

1. `XREADGROUP sub1-seal` reads one message from `canary:events`
2. Validate required fields (event_id, merchant_id, source, event_hash, raw_payload, received_at). Missing fields -> dead letter + ACK.
3. Re-verify `event_hash`: recompute `SHA-256(raw_payload)`, compare with queue field. Mismatch -> dead letter + ACK (tamper detected).
4. Parse `parsed_payload` from `raw_payload` JSON (if `parse_failed=false`).
5. Acquire PostgreSQL advisory lock per `merchant_id`: `pg_advisory_xact_lock(hashtext(merchant_id))`.
6. Read previous `chain_hash` for this merchant from `evidence_records` (latest by `id DESC`).
7. Compute `chain_hash = SHA-256(previous_chain_hash || event_hash)`. Genesis: uses only `event_hash`.
8. INSERT `EvidenceRecord` (write-once).
9. XACK on success. On DB failure, do NOT ACK (message redelivered from PEL).

### Startup Sequence

1. Consumer app created via `create_consumer_app()` (minimal Flask, DB config only)
2. Database session factory initialized
3. Consumer group created defensively (catches BUSYGROUP)
4. Blocking loop begins

### Health Checks

- Valkey heartbeat: `canary:heartbeat:sub1` (TTL 120s, written every loop iteration)
- Docker healthcheck: `devops/scripts/tsp_healthcheck.py` (reads heartbeat, 15s interval)

### Failure Modes

| Failure | Behavior | Recovery |
|---------|----------|----------|
| Missing required fields | Move to dead letter stream, ACK (clear poison) | Manual review via `get_dead_letters` MCP tool |
| Hash mismatch (tamper) | Move to dead letter stream, ACK | Investigate: data corruption in transit or replay attack |
| Duplicate event (`uq_evidence_merchant_event`) | ACK -- already sealed | Normal: idempotent |
| PostgreSQL advisory lock timeout | DB exception, do NOT ACK | Redelivered on next read |
| PostgreSQL connection failure | Do NOT ACK, exponential backoff | Message stays in PEL until DB recovers |
| 10 consecutive errors | Consumer stops (raises exception) | Docker restart. Investigate root cause. |
| Valkey connection failure | Consumer blocks, then exponential backoff | Reconnects automatically |

### Error Handling

- Exponential backoff on consecutive errors: `min(2^(n-1), 30)` seconds, max 10 consecutive
- Dead letter writes are best-effort (errors swallowed to avoid cascading failures)
- Heartbeat writes are best-effort (Valkey hiccup does not crash consumer)

---

## Deployment

### Docker Service

```yaml
tsp-sub1:
  image: canary-flask
  container_name: canary_localhost_tsp_sub1
  command: python -m canary.services.tsp.run_consumer --consumer sub1
  healthcheck:
    test: ["CMD", "python", "devops/scripts/tsp_healthcheck.py"]
    interval: 15s
    timeout: 5s
    retries: 3
    start_period: 30s
  depends_on:
    flask: { condition: service_healthy }
  restart: unless-stopped
```

### AWS Target

- ECS Fargate task (1 task, 1 container)
- Single worker only -- advisory lock design requires exactly 1 Sub 1 instance per deployment
- Memory: 256 MB sufficient
- CPU: 0.25 vCPU sufficient (I/O-bound, not compute-bound)

---

## Data Model

### EvidenceRecord (`evidence_records`)

Write-once immutable evidence store. Database-level INSERT-only triggers prevent UPDATE and DELETE. Primary key is `BIGSERIAL` (auto-incrementing integer) -- defines chain ordering within a merchant.

| Column | Type | Notes |
|--------|------|-------|
| `id` | BIGSERIAL | Chain ordinal within merchant |
| `event_id` | str | ULID (unique across all merchants) |
| `merchant_id` | str | Tenant partition key |
| `source` | str | e.g., `square` |
| `source_event_id` | str | Square's event_id |
| `event_type` | str | e.g., `payment.created` |
| `event_hash` | bytes (BYTEA) | SHA-256 of raw_payload (32 bytes) |
| `chain_hash` | bytes (BYTEA) | SHA-256(prev \|\| current) |
| `previous_chain_hash` | bytes (BYTEA, nullable) | NULL for genesis |
| `raw_payload` | str (TEXT) | Verbatim webhook payload |
| `parsed_payload` | dict (JSONB, nullable) | Parsed JSON (NULL if parse_failed) |
| `parse_failed` | bool | True if gateway could not parse JSON |
| `received_at` | datetime | Gateway receipt timestamp |
| `sealed_at` | datetime | server_default=now() |

**Unique constraint:** `(merchant_id, source_event_id)`
**Indexes:** `(merchant_id, received_at)`, `event_hash`, `(merchant_id, id)`, `(source, source_event_id)`

### DeadLetterQueue (Valkey stream `canary:dead_letter`)

Poison messages quarantined for investigation. Fields mirror the 9-field queue message plus:
- `original_msg_id`: Stream message ID
- `original_stream`: `canary:events`
- `original_group`: `sub1-seal`
- `dead_letter_reason`: Human-readable failure description

---

## Code Review Findings

### P0 -- Blocks Production

| # | Finding | Recommended Fix |
|---|---------|-----------------|
| P0-S1-01 | `raw_payload` stored as plaintext TEXT in `evidence_records`. Contains complete webhook JSON with card data, employee names, customer IDs, IP addresses. Every webhook ever received is permanently stored in the clear. | Encrypt `raw_payload` with AES-256-GCM before INSERT. Add `decrypt_evidence_payload()` for authorized audit access only. |
| P0-S1-02 | `parsed_payload` stored as plaintext JSONB. Duplicate of raw_payload PII in a second column. | Encrypt alongside raw_payload, or derive on-demand from decrypted raw_payload instead of storing twice. |
| P0-S1-03 | Dead letter stream contains full `raw_payload` in Valkey (plaintext, no AUTH/TLS). | Encrypt raw_payload before XADD to dead letter. Enable Valkey AUTH + TLS in production. |

### P1 -- Before GA

| # | Finding | Recommended Fix |
|---|---------|-----------------|
| P1-S1-01 | No audit log for evidence record creation. The seal event itself is the record, but there is no separate audit trail for who/what triggered the seal. | Log seal events to a separate audit table with timestamp, consumer ID, and event reference. |
| P1-S1-02 | Advisory lock uses `hashtext(merchant_id)` which could theoretically collide across merchants. Low probability but non-zero. | Document the collision risk. Consider using `pg_advisory_xact_lock(hashtext(merchant_id), hashtext('sub1'))` for namespace isolation. |

### P2 -- Post-Launch

| # | Finding | Recommended Fix |
|---|---------|-----------------|
| P2-S1-01 | Single-worker constraint is enforced by code convention (`BATCH_SIZE=1`) but not by infrastructure. Nothing prevents deploying 2 Sub 1 instances. | Add a Valkey-based distributed lock or startup check that prevents multiple Sub 1 instances for the same deployment. |

---

## Production Readiness Checklist

- [ ] `raw_payload` encrypted at rest (P0-S1-01)
- [ ] `parsed_payload` encrypted or removed (P0-S1-02)
- [ ] Dead letter stream encrypted in transit (P0-S1-03)
- [ ] Secrets in AWS Secrets Manager
- [x] Health check functional (Valkey heartbeat + Docker healthcheck)
- [ ] Audit logging for seal operations (P1-S1-01)
- [ ] Single-instance enforcement (P2-S1-01)
- [x] Error handling with exponential backoff
- [x] Dead letter quarantine for poison messages
- [x] Idempotent on duplicate events (unique constraint)
