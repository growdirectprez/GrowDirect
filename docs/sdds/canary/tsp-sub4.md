# TSP Sub 4 -- Chirp Detection Consumer

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]], [[Brain/wiki/canary-detection|Canary Detection]]
**Architecture:** [[docs/sdds/canary/architecture|Canary Architecture SDD]]
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[Canary/docs/profiles/ops/Tom|Tom]] · **Operator role:** [[Canary/docs/profiles/ops/Jeremy|Jeremy]]

> **Type:** App Service (Canary) -- Stream Consumer
> **Parent SDD:** [[docs/sdds/canary/tsp|TSP Pipeline Overview]]
> **Status:** Production Readiness Review -- 2026-04-13
> **Code location:** `Canary/canary/services/tsp/consumers/sub4_detect.py`

---

## Purpose

Sub 4 is the detection consumer. It reads parsed CRDM events from the `canary:detection` stream (fed by Sub 2), routes each event to the appropriate Chirp rule engine evaluate method based on `detection_type`, and writes resulting alerts to `canary_app.alerts`. Sub 4 is the bridge between the data ingestion pipeline and the detection/alerting system.

Key architectural difference from Sub 1-3: Sub 4 reads from `canary:detection` (not `canary:events`), and it needs **two database sessions** -- `canary_sales` for reading CRDM data and `canary_app` for writing alerts.

## Dependencies

| Dependency | Role | Required |
|------------|------|----------|
| Valkey DB 4 | Reads from `canary:detection` stream | Yes |
| PostgreSQL (`canary` DB, `canary_sales` schema) | Reads CRDM records for rule evaluation | Yes |
| PostgreSQL (`canary` DB, `canary_app` schema) | Writes alerts via `write_alerts_to_session()` | Yes |
| `ChirpRuleEngine` | Rule evaluation engine (`canary.services.chirp.rule_engine`) | Yes |
| `write_alerts_to_session()` | Alert persistence function | Yes |
| Sub 2 (upstream) | Publishes detection events after CRDM writes | Yes (indirect) |

---

## Data Flow & PII Map

### What Enters

5-field message from `canary:detection` stream (published by Sub 2):
- `transaction_id` -- Primary key of the CRDM record in `canary_sales`
- `merchant_id` -- Tenant identifier
- `event_type` -- Original webhook event type (e.g., `payment.created`)
- `event_id` -- Original event_id from TSP pipeline
- `detection_type` -- Routing key: `transaction`, `cash_drawer`, `gift_card`, `loyalty`, `dispute`, `invoice`

The stream message contains **IDs only, no PII**. PII is accessed indirectly when the rule engine queries CRDM tables.

### What's Read (via Chirp Rule Engine)

The rule engine queries CRDM tables in `canary_sales` to evaluate detection rules. PII accessed during evaluation:
- Transaction details (amounts, card data, employee_id, customer_id)
- Cash drawer shifts (employee_id, variance)
- Gift card activities (amounts, employee_id)
- Loyalty events (account linkages)
- Disputes (payment_id, amounts)
- Invoices (creator, recipient)

This data is **read, not stored** by Sub 4. The rule engine holds it in memory during evaluation only.

### What's Stored

**`canary_app.alerts`** table (written via `write_alerts_to_session()`):

| Field | Classification | Encryption | Notes |
|-------|---------------|------------|-------|
| Alert metadata | internal | NONE | Rule ID, severity, merchant_id, location_id, timestamp |
| `employee_id` | internal | NONE | Employee linked to the alert trigger |
| `transaction_id` | internal | NONE | Reference to the triggering CRDM record |
| Alert description | internal | NONE | Human-readable description of the detection -- may reference amounts, patterns |

Sub 4 does not store raw PII (no card numbers, names, emails). Alert records contain identifiers that link back to PII in CRDM tables.

### What Exits

Nothing downstream. Sub 4 writes alerts to `canary_app.alerts` and that's its terminal output. Alerts are consumed by the Alert Lifecycle service, Fox Case Management, and the UI/BFF.

---

## API Contract

Sub 4 exposes no HTTP endpoints. It is a Valkey stream consumer only.

**Consumer Group:** `detection-engine`
**Stream:** `canary:detection` (Valkey DB 4)
**Batch Size:** 1
**Block Timeout:** `SUB4_BLOCK_MS` (default 5000ms)

### Detection Type Routing

| `detection_type` | Rule Engine Method | CRDM Source |
|-------------------|--------------------|-------------|
| `transaction` | `evaluate_readonly(txn, merchant_id)` | `transactions` |
| `cash_drawer` | `evaluate_cash_drawer(shift_id, merchant_id)` | `cash_drawer_shifts` |
| `gift_card` | `evaluate_gift_card_activity(activity_id, merchant_id)` | `gift_card_activities` |
| `loyalty` | `evaluate_loyalty_event(event_id, merchant_id)` | `loyalty_events` |
| `dispute` | `evaluate_dispute(dispute_id, merchant_id)` | `disputes` |
| `invoice` | `evaluate_invoice(invoice_id, merchant_id)` | `invoices` |

Unknown `detection_type` values are logged as warnings and ACK'd (no alerts generated).

---

## Operations

### Processing Sequence

1. `XREADGROUP detection-engine` reads one message from `canary:detection`
2. Validate `transaction_id` and `merchant_id`. Missing -> ACK (don't redeliver malformed messages).
3. Instantiate `ChirpRuleEngine` with `canary_sales` session.
4. Route by `detection_type` to appropriate evaluate method via `_evaluate_by_type()`.
5. For `transaction` type: load `Transaction` record from `canary_sales`, pass to `evaluate_readonly()`.
6. For other types: pass record ID and merchant_id to corresponding evaluate method.
7. If alerts generated: call `write_alerts_to_session(alerts, merchant_id, app_session)` and commit.
8. XACK on success. On rule engine failure: do NOT ACK (redelivered).

### Pending Message Recovery

Sub 4 has a unique startup behavior: it reads pending messages (PEL) first by using `_read_id = "0"`, then switches to new messages (`_read_id = ">"`) once all pending messages are processed. This ensures crash recovery processes backlogged events before new ones.

### Startup Sequence

1. Consumer app created via `create_consumer_app()`
2. Database session factory initialized
3. Consumer group created defensively
4. Recover pending messages from PEL (read with id `"0"`)
5. Once PEL drained, switch to blocking reads for new messages (id `">"`)

### Health Checks

- Valkey heartbeat: `canary:heartbeat:sub4` (TTL 120s)
- Docker healthcheck: `devops/scripts/tsp_healthcheck.py` (15s interval)

### Failure Modes

| Failure | Behavior | Recovery |
|---------|----------|----------|
| Missing transaction_id/merchant_id | ACK (malformed, don't redeliver) | Normal -- prevent infinite redelivery of bad messages |
| CRDM record not found | ACK (record may not exist yet or was deleted) | Normal -- logged as warning |
| Rule engine exception | Do NOT ACK, exponential backoff | Redelivered from PEL. If persistent, investigate rule code. |
| App session commit failure | Alert write lost, message redelivered | Alerts recreated on redelivery (rule engine is idempotent on read) |
| 10 consecutive errors | Consumer stops | Docker restart |

### Dual Session Requirement

Sub 4 creates two separate `get_session()` calls per message:
- `app_session`: Bound to `canary_app` schema for writing alerts
- `sales_session`: Bound to `canary_sales` schema for reading CRDM records

**Code finding:** Both sessions are obtained from the same `get_session()` factory. This works because the canary database uses a single connection with schema search path. However, the variable naming (`app_session` vs `sales_session`) implies separate databases -- the abstraction is misleading but functionally correct.

---

## Deployment

### Docker Service

```yaml
tsp-sub4:
  image: canary-flask
  container_name: canary_localhost_tsp_sub4
  command: python -m canary.services.tsp.run_consumer --consumer sub4
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

- ECS Fargate task (can scale horizontally -- no shared state constraint)
- Memory: 256-512 MB (rule engine queries can be complex)
- CPU: 0.25 vCPU

---

## Code Review Findings

### P0 -- Blocks Production

| # | Finding | Recommended Fix |
|---|---------|-----------------|
| P0-S4-01 | **Dual session creates two connections to the same database.** `get_session()` is called twice per message, creating two SQLAlchemy sessions. In a connection-pooled environment, this doubles connection usage per message. Under load, this could exhaust the connection pool. | Use a single session for both reads and writes (same database, same schema search path). The dual-session pattern was designed for a future split but the split hasn't happened. |

### P1 -- Before GA

| # | Finding | Recommended Fix |
|---|---------|-----------------|
| P1-S4-01 | **Alert deduplication relies on rule engine idempotency.** If a message is redelivered and the rule engine fires the same alert again, duplicate alerts are created. No dedup at the alert write layer. | Add dedup: check for existing alert with same `rule_id + transaction_id + merchant_id` before insert. |
| P1-S4-02 | **`event_type` read but unused.** Line 104: `fields.get("event_type", "")` reads the field and discards it (not assigned to a variable). Dead code. | Either use event_type for logging/metrics or remove the read. |
| P1-S4-03 | **No audit trail for alert creation.** Alerts are written without logging who/what triggered them beyond the consumer process. | Add structured log entry for each alert creation with rule_id, merchant_id, detection_type. |
| P1-S4-04 | **Pending recovery reads ALL pending with count=1.** The PEL drain loop reads one message at a time with `block=0` (non-blocking). For a large backlog after a crash, this is slow but correct. | Increase count to 10-50 for PEL drain phase. |

### P2 -- Post-Launch

| # | Finding | Recommended Fix |
|---|---------|-----------------|
| P2-S4-01 | **No detection latency metrics.** No measurement of time from CRDM write (Sub 2) to alert creation (Sub 4). Critical for SLA. | Add OTEL span or metric for detection latency: `alert_created_at - detection_event_published_at`. |
| P2-S4-02 | **No rule engine execution metrics.** No tracking of which rules fire, how often, false positive rates. | Add per-rule execution counters and alert-generation rates. |
| P2-S4-03 | **Horizontal scaling untested.** Multiple Sub 4 instances should work (Valkey consumer groups distribute messages), but this is unvalidated. | Test with 2+ Sub 4 instances and validate: no duplicate alerts, all messages processed, heartbeats work. |

---

## Production Readiness Checklist

- [x] No direct PII storage (alerts contain IDs, not raw PII)
- [ ] Alert deduplication (P1-S4-01)
- [ ] Connection pool usage optimized (P0-S4-01)
- [ ] Secrets in AWS Secrets Manager
- [x] Health check functional (Valkey heartbeat + Docker healthcheck)
- [x] Pending message recovery on startup
- [ ] Audit logging for alert creation (P1-S4-03)
- [ ] Detection latency metrics (P2-S4-01)
- [x] Error handling with exponential backoff
- [x] Graceful handling of missing CRDM records
- [x] Unknown detection_type handled (logged + ACK'd)
