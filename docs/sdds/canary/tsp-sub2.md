# TSP Sub 2 -- Parse & Route

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]
**Architecture:** [[docs/sdds/canary/architecture|Canary Architecture SDD]]
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[docs/team/Architect|Architect]] · **Operator role:** [[docs/team/Engineer|Engineer]]

> **Type:** App Service (Canary) -- Stream Consumer
> **Parent SDD:** [[docs/sdds/canary/tsp|TSP Pipeline Overview]]
> **Status:** Production Readiness Review -- 2026-04-13
> **Code location:** `Canary/canary/services/tsp/consumers/sub2_parse.py`, `Canary/canary/services/webhook_dispatch.py`

---

## Purpose

Sub 2 is the CRDM (Canonical Retail Data Model) parser. It reads events from the `canary:events` stream, parses raw webhook payloads into structured domain models via the webhook dispatch registry, writes them to PostgreSQL, and publishes detection events to the `canary:detection` stream for Sub 4. Sub 2 covers all ~145 Square webhook event types. LP-critical events get full parse/store/detect treatment. Log-only events are accepted and ACK'd without CRDM writes.

Sub 2 also handles employee and customer upserts as side effects of transaction parsing -- these are not separate consumers but inline operations within the parse flow.

## Dependencies

| Dependency | Role | Required |
|------------|------|----------|
| Valkey DB 4 | Reads from `canary:events`, publishes to `canary:detection` | Yes |
| PostgreSQL (`canary` DB) | Writes CRDM tables in `canary_sales` schema, updates `ingestion_log` status, upserts employees/customers in `canary_app` | Yes |
| `webhook_dispatch.py` | Event type -> parser/model routing registry | Yes |
| `stream_publisher.publish_detection_event()` | Publishes to detection stream | Yes |

---

## Data Flow & PII Map

### What Enters

9-field queue message from `canary:events` (same as Sub 1). The key field for Sub 2 is `raw_payload` -- the complete webhook JSON that gets parsed into structured CRDM records.

### What's Stored

Sub 2 writes to **18+ CRDM tables** across `canary_sales` and `canary_app`. PII-bearing fields:

| Table | PII Field(s) | Classification | Encryption | Notes |
|-------|-------------|---------------|------------|-------|
| `transactions` | `card_last4`, `card_fingerprint`, `card_bin`, `card_exp_month`, `card_exp_year` | sensitive | **NONE (P0)** | PCI-relevant card data elements |
| `transactions` | `employee_id`, `customer_id`, `device_id` | internal | NONE | Linkable identifiers |
| `transactions` | `payload` | **restricted** | **NONE (P0)** | Full webhook payload (forensic copy) |
| `transaction_tenders` | `card_brand`, `card_last4` | sensitive | **NONE (P0)** | Tender-level card data |
| `employees` (app schema) | `employee_name`, `email` | **sensitive** | **NONE (P0)** | Plaintext PII via `_upsert_employee()` |
| `cash_drawer_shifts` | `employee_id` | internal | NONE | Links to employee names |
| `cash_drawer_events` | `employee_id` | internal | NONE | Cash drawer operator |
| `gift_card_activities` | `buyer_payment_instrument_ids` | sensitive | **NONE (P0)** | JSON array of payment instrument IDs |
| `loyalty_accounts` | `phone_hash` | sensitive | SHA-256 | One-way hash -- good |
| `disputes` | `payment_id`, `order_id` | internal | NONE | Links to transaction PII |
| `invoices` | `primary_recipient` | **sensitive** | **NONE (P0)** | JSONB with customer name/email/phone/address |
| `invoices` | `raw_square_object` | **restricted** | **NONE (P0)** | Complete Square API response |
| `devices` | `ip_address`, `serial_number`, `wifi_network_name` | sensitive/internal | **NONE (P0)** | Device identification data |
| `employee_timecards` | `employee_id` | internal | NONE | Links to employee names |
| `inventory_adjustments` | `team_member_id` | internal | NONE | Employee linkage |

### What Exits

| Destination | Data | Classification |
|-------------|------|---------------|
| `canary:detection` stream | `{transaction_id, merchant_id, event_type, event_id, detection_type}` | internal (IDs only, no PII) |
| `ingestion_log` | Status update to `'parsed'` | internal |

---

## API Contract

Sub 2 exposes no HTTP endpoints. It is a Valkey stream consumer only.

**Consumer Group:** `sub2-parse`
**Stream:** `canary:events` (Valkey DB 4)
**Batch Size:** 1 (per-message processing for CRDM accuracy)
**Block Timeout:** `SUB2_BLOCK_MS` (default 5000ms)

### Webhook Dispatch Registry

Sub 2 routes events by `event_type` through the `webhook_dispatch` registry. Each route specifies:
- **Parser function:** Extracts fields from webhook JSON and creates model instances
- **Target model class:** SQLAlchemy model for the CRDM table
- **Detection type (optional):** Routing key for Sub 4 (`transaction`, `cash_drawer`, `gift_card`, `loyalty`, `dispute`, `invoice`)

Events without a registered route are treated as log-only: ACK'd without CRDM writes.

---

## Operations

### Processing Sequence

1. `XREADGROUP sub2-parse` reads one message from `canary:events`
2. Extract `raw_payload` and parse to JSON. If `parse_failed=true`, ACK without CRDM writes.
3. Resolve `event_type` through webhook dispatch registry to get parser, model class, and detection_type.
4. Parser function creates CRDM model instance(s) from parsed payload.
5. Write CRDM records to PostgreSQL `canary_sales`.
6. Side-effect upserts: employee records (`_upsert_employee`), customer records (`_upsert_customer`), employee-location assignments (`_sync_employee_locations`), external identity mappings.
7. Update `ingestion_log.status` to `'parsed'`.
8. If route has `detection_type`, publish to `canary:detection` via `publish_detection_event()`.
9. XACK on success.

### Employee Fallback Logic (GRO-299)

When a transaction has no `team_member_id`, Sub 2 looks up the primary employee for the location via `EmployeeLocationAssignment.is_primary`. This is best-effort -- if lookup fails, `employee_id` is NULL on the transaction.

### Startup Sequence

1. Consumer app created via `create_consumer_app()` (minimal Flask, DB config only)
2. Database session factory initialized
3. Consumer group created defensively (catches BUSYGROUP)
4. Blocking loop begins

### Health Checks

- Valkey heartbeat: `canary:heartbeat:sub2` (TTL 120s)
- Docker healthcheck: `devops/scripts/tsp_healthcheck.py` (15s interval)

### Failure Modes

| Failure | Behavior | Recovery |
|---------|----------|----------|
| `parse_failed=true` | ACK without CRDM writes | Normal -- raw bytes already sealed by Sub 1 |
| Unknown event_type (no dispatch route) | ACK (log-only event) | Normal -- not all Square events need CRDM records |
| `IntegrityError` on CRDM insert | Log and ACK (typically duplicate) | Normal -- idempotent on unique constraints |
| PostgreSQL failure (other) | Do NOT ACK, exponential backoff | Message redelivered from PEL |
| `publish_detection_event` fails | CRDM write succeeds but detection skipped | Detection gap -- manually replay via MCP tool |
| Employee upsert fails | Transaction saved without employee_id | Best-effort -- logged as debug |
| 10 consecutive errors | Consumer stops | Docker restart |

---

## Deployment

### Docker Service

```yaml
tsp-sub2:
  image: canary-flask
  container_name: canary_localhost_tsp_sub2
  command: python -m canary.services.tsp.run_consumer --consumer sub2
  environment:
    DETECTION_STREAM: "canary:detection"
  healthcheck:
    test: ["CMD", "python", "devops/scripts/tsp_healthcheck.py"]
    interval: 15s
  depends_on:
    flask: { condition: service_healthy }
  restart: unless-stopped
```

### AWS Target

- ECS Fargate task (can scale horizontally -- no advisory lock constraint)
- Memory: 256-512 MB (parsing is lightweight but model imports are heavy)
- CPU: 0.25 vCPU

---

## Code Review Findings

### P0 -- Blocks Production

| # | Finding | Recommended Fix |
|---|---------|-----------------|
| P0-S2-01 | **Employee name and email stored plaintext.** `_upsert_employee()` writes `employee_name` and `email` to `canary_app.employees` without encryption. These are direct PII. | Encrypt `employee_name` and `email` with AES-256-GCM. Hash email for lookup. |
| P0-S2-02 | **Transaction.payload contains full webhook JSON plaintext.** Forensic copy of the entire webhook payload including card data, customer data. Duplicates `evidence_records.raw_payload`. | Remove `payload` field from `transactions` (evidence_records already holds the canonical copy) or encrypt it. |
| P0-S2-03 | **Card data fields stored plaintext.** `card_last4`, `card_fingerprint`, `card_bin`, `card_exp_month`, `card_exp_year` in `transactions` table. PCI DSS requires encryption at rest. | Field-level AES-256-GCM encryption. |
| P0-S2-04 | **Invoice recipient PII in JSONB.** `invoices.primary_recipient` may contain name, email, phone, address. `invoices.raw_square_object` contains complete API response. Both plaintext. | Encrypt JSONB fields or extract and encrypt individual PII fields. |
| P0-S2-05 | **Device IP address stored plaintext.** `devices.ip_address` is stored as-is from Square's API response. | Hash or encrypt. |
| P0-S2-06 | **Gift card buyer payment instrument IDs plaintext.** `gift_card_activities.buyer_payment_instrument_ids` is a JSON array that could link to payment methods. | Encrypt or assess if this field is needed for LP detection. |

### P1 -- Before GA

| # | Finding | Recommended Fix |
|---|---------|-----------------|
| P1-S2-01 | **No audit trail for employee upserts.** Employee records are created/updated silently. No log of who changed what. | Add audit log entries for employee create/update with before/after values. |
| P1-S2-02 | **Detection event publication not transactional with CRDM write.** If `publish_detection_event()` fails after CRDM commit, the transaction is stored but never evaluated by Chirp. | Wrap detection publish in the same DB transaction (use outbox pattern) or add a reconciliation job. |
| P1-S2-03 | **Model cache (`_MODEL_CACHE`) is module-level global.** Not thread-safe if Sub 2 is ever run with multiple threads. | Use `threading.Lock` around cache writes, or accept single-threaded constraint. |

### P2 -- Post-Launch

| # | Finding | Recommended Fix |
|---|---------|-----------------|
| P2-S2-01 | **No parser coverage metrics.** No tracking of which event types are parsed vs. log-only. Useful for identifying new Square event types that should get parsers. | Add metrics counter per event_type with parse/skip outcome. |
| P2-S2-02 | **Employee location sync does DELETE.** `_sync_employee_locations()` deletes stale `EmployeeLocationAssignment` records. This could cause issues if the assignment is referenced elsewhere. | Use soft-delete (set `is_active=false`) instead of hard delete. |

---

## Production Readiness Checklist

- [ ] Employee PII encrypted at rest (P0-S2-01)
- [ ] Card data fields encrypted (P0-S2-03)
- [ ] Transaction.payload encrypted or removed (P0-S2-02)
- [ ] Invoice PII encrypted (P0-S2-04)
- [ ] Device IP encrypted (P0-S2-05)
- [ ] Secrets in AWS Secrets Manager
- [x] Health check functional (Valkey heartbeat + Docker healthcheck)
- [ ] Audit logging for employee upserts (P1-S2-01)
- [ ] Detection publish reliability (P1-S2-02)
- [x] Error handling with exponential backoff
- [x] Idempotent on duplicate CRDM records (IntegrityError handling)
- [x] Graceful handling of unparseable events
