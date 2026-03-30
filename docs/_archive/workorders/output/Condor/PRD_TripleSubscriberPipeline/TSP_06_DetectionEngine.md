---
type: spec
domain: tsp
status: active
created: 2026-03-18
updated: 2026-03-19
---
# PRD: Detection Engine
**PRD ID:** TSP-06
**Version:** 1.2
**Owner:** Jeremy
**Patent Figure Reference:** FIG. 2 — T+100ms Detection box, FIG. 3 — Application Layer (Detection Engine + Dashboard)
**Depends on:** TSP-04 (Sub 2 Parse & Route)
**Gates:** Merchant dashboard (Today's View)
**Sprint target:** Sprint 6

---

## Purpose

The Detection Engine evaluates parsed event data from Sub 2's structured store against 26 Chirp rules across 8 categories, fires alerts when thresholds are breached, persists alert records, and pushes real-time notifications to the merchant dashboard via SSE (Phase 1) or WebSocket (Phase 2). This is the component that transforms raw transaction data into actionable loss prevention intelligence. The detection engine is the reason merchants use Canary — everything upstream is infrastructure; this is the product.

**Reference:** PRD E1-F14 (`_ALX/WorkOrders/PRD_ChirpConfig_APIGateway_v1.0.md`) defines the Chirp Config UI, all 26 rule mappings, and the merchant toggle API. This PRD extends E1-F14 with the detection engine internals — how rules are triggered, evaluated, and delivered. Do NOT duplicate rule definitions here; reference E1-F14.

---

## Architecture Position

**What feeds it:** TSP-04 (Sub 2) publishes detection notifications to Valkey Stream `canary:detection` after writing structured records. Each notification contains:

```json
{
  "event_id": "evt_01HXYZ789ABC",
  "merchant_id": "offset-coffee-001",
  "event_type": "payment.created",
  "tables_written": ["transactions", "transaction_tenders"],
  "row_ids": {
    "transactions": "txn_abc123",
    "transaction_tenders": ["tt_xyz456"]
  },
  "parse_failed": false,
  "parsed_at": "2026-02-26T14:23:01.020Z"
}
```

**Why Streams instead of pub/sub:** Pub/sub is fire-and-forget — if the detection engine is down when Sub 2 publishes, the message is lost. Streams provide durability (messages persist until consumed). The detection engine reads from consumer group `detection-engine` on the `canary:detection` stream. This guarantees no missed events without relying on polling fallback.

**Cross-PRD Sync (Gap 1):** Synced: detection notification uses XADD to `canary:detection` Stream (not pub/sub). See TSP-04 Detection Notification section.

**row_ids field:** The detection engine evaluates rules against structured tables (transactions, cash_drawer_shifts, etc.), not raw pipeline events. It needs the row IDs written by Sub 2 to query the correct rows. The existing `ChirpRuleEngine.evaluate_transaction()` takes a `transaction_id`, not an `event_id`.

**parse_failed events:** Events with `parse_failed=true` are skipped by Sub 2 (TSP-04 v1.1) — no structured rows are written, no detection notification is published. The detection engine never sees them. This is correct — detection requires parsed structured data.

**What it feeds:** Merchant dashboard (Today's View) via SSE (Phase 1) / WebSocket (Phase 2). Alert records in `canary_app.alerts` and `canary_app.alert_history`.

**FIG. 2 mapping:** T+100ms — rules evaluate. Alerts fire. Dashboard updated.

**FIG. 3 mapping:** Application Layer — Detection Engine + Dashboard (Flask · React Frontend).

---

## API Contract

### Detection Trigger (Input — from Sub 2 via Valkey Stream)

Reads from Valkey Stream `canary:detection`, consumer group `detection-engine`:

```
XREADGROUP GROUP detection-engine worker-1 COUNT 10 BLOCK 5000 STREAMS canary:detection >
```

Each message contains the notification shape defined in Architecture Position above. The detection engine:

1. Extracts `event_type` and `row_ids` from the notification.
2. Routes to the appropriate rule checker based on `event_type`.
3. Queries the structured row(s) from `canary_sales` using the `row_ids`.
4. Evaluates all enabled Chirp rules for that merchant against the structured data.
5. XACKs the message after evaluation completes (regardless of whether alerts fired).

**Startup:** Defensive `XGROUP CREATE canary:detection detection-engine $ MKSTREAM` on startup.

### Rule Evaluation Interface

```
Input:  event_type (determines which rule checker to invoke)
      + row_ids (keys into CRDM structured tables)
      + merchant_config (which Chirps are enabled, thresholds from ThresholdManager)
Output: Alert[] (zero or more alerts)
```

### Event Type → Rule Checker Routing (Phase 1)

| Event Type | Rule Checker | Rules Evaluated | Table(s) Queried |
|------------|-------------|-----------------|------------------|
| `payment.created` | `_check_payment_rules()` | C-004, C-007 (implemented). C-001, C-002, C-003, C-005, C-006, C-008 (TODO — window queries) | `transactions`, `transaction_tenders` |
| `refund.created` | `_check_payment_rules()` | C-001 (rapid refund), C-002 (refund rate), C-007 (high value refund) | `refund_links`, `transactions` |
| `cash_drawer.shift.*` | `_check_cash_drawer_rules()` | C-101 (no sale abuse), C-102 (cash variance), C-103 (paid out), C-104 (after hours) | `cash_drawer_shifts`, `cash_drawer_events` |
| `cash_drawer.event.created` | `_check_cash_drawer_rules()` | C-101 (no sale count check) | `cash_drawer_events` |

**Deferred to Phase 2+:** Order rules (C-201 to C-203), void rules (C-501 to C-502), gift card (C-601 to C-602), loyalty (C-801 to C-804) — Sub 2 doesn't parse these event types in Phase 1.

**Deferred to Phase 3 (polling adapter):** Timecard cross-reference rules (C-301, C-302, C-303) — Labor API timecards are poll-only per Jeremy SDK Audit P0-1. Requires polling adapter infrastructure.

Each alert (aligned with existing `Alert` model):
```json
{
  "id": "uuid-generated",
  "merchant_id": "offset-coffee-001",
  "rule_id": "C-102",
  "alert_type": "CASH_VARIANCE",
  "severity": "high",
  "title": "Drawer came up short",
  "description": "Cash drawer shift #SD-1234 closed $23.50 short at Main St location.",
  "source_table": "cash_drawer_shifts",
  "source_id": "shift-uuid-1234",
  "event_id": "evt_01HXYZ789ABC",
  "employee_id": "emp-maria-santos",
  "location_id": "loc-main-st",
  "amount_cents": -2350,
  "details": "{\"expected_cents\": 50000, \"counted_cents\": 47650, \"variance_cents\": -2350}",
  "created_at": "2026-02-26T14:23:01.100Z",
  "created_by": "chirp"
}
```

**Note:** `details` is stored as JSON text (String), not JSONB — matching existing model. `alert_type` is derived from rule name in `RULE_MAP`. `source_table` + `source_id` replace the PRD v1.0 generic `event_id` as the primary alert anchor.

### Real-Time Alert Push (Merchant Dashboard)

**Phase 1 — Server-Sent Events (SSE) via existing Flask/Gunicorn stack:**

```
GET /api/alerts/stream/{merchant_id}
Accept: text/event-stream
Authorization: Bearer {jwt_token}
```

Response (streaming):
```
event: new_alert
data: {"id": "uuid", "rule_id": "C-102", "alert_type": "CASH_VARIANCE",
       "severity": "HIGH", "merchant_id": "offset-coffee-001",
       "created_at": "2026-02-26T14:23:01.100Z"}

event: new_alert
data: {"id": "uuid", "rule_id": "C-005", ...}
```

**Why SSE for Phase 1:**
1. Flask 3.0 + Gunicorn (sync workers) does not natively support WebSocket
2. SSE works over standard HTTP — no Nginx upgrade configuration, no new Docker service
3. Path-based routing through existing Flask blueprint on port 5001 (same as API)
4. No port conflict (no port 3000 needed)

**Authentication:** SSE connection requires a valid session token passed as `Authorization` header or query parameter. Flask session cookie (same auth as dashboard). The SSE handler validates `merchant_id` matches the authenticated user's merchant. Unauthenticated or mismatched connections are rejected with 401/403.

**Reconnection:** On SSE disconnect, client reconnects with `Last-Event-ID` header.
Server replays missed alerts from in-memory ring buffer (last 50 per merchant).

**Phase 2 — WebSocket upgrade (if SSE latency or fan-out is insufficient):**

Upgrade to WebSocket via `flask-sock` + Gunicorn with `gevent` worker class:
```yaml
# docker-compose.alpha3x.yml change:
command: gunicorn wsgi_alpha3x:app --bind 0.0.0.0:5001 --worker-class gevent --workers 4
```
Requires adding `flask-sock` + `gevent` to `requirements.txt`. WebSocket upgrade happens
on the same port 5001 via path `/ws/alerts/{merchant_id}`. No new port.

### Chirp Config API (reference — defined in E1-F14)

- `GET /api/chirp/config` — all 26 rules with merchant-specific enabled state
- `PUT /api/chirp/rules/{rule_id}/toggle` — toggle single rule on/off

---

## Data Model

### SQLAlchemy Bind Routing

This component writes to PostgreSQL databases routed by Flask-SQLAlchemy multi-bind
configuration. The three databases are configured in `docker-compose.alpha3x.yml`:

| Env Var | Database | SQLAlchemy Base |
|---------|----------|-----------------|
| `DATABASE_URL` | `canary_app` | `AppBase` (default) |
| `DATABASE_URL_SALES` | `canary_sales` | `SalesBase` |
| `DATABASE_URL_METRICS` | `canary_metrics` | `MetricsBase` |

Models declare their bind via their base class (defined in `canary/models/base.py`):
- `AppBase` models → `canary_app` (alerts, detection rules, replay logs)
- `SalesBase` models → `canary_sales` (transactions, ingestion log, evidence records)
- `MetricsBase` models → `canary_metrics` (aggregation tables)

**This PRD:** `alerts`, `detection_rules`, `merchant_rule_config` → `AppBase` / `canary_app`

### Rule Source Reconciliation

**Current state:** 26 Chirp rules defined as frozen dataclasses in
`canary/services/chirp/rule_definitions.py` (`RULE_CATALOG` list + `RULE_MAP` dict).
`ThresholdManager` reads from `RULE_MAP` for default threshold lookup.

**PRD assumption:** Rules stored in `detection_rules` DB table (`canary_app`).

**Resolution — dual-source with DB seed:**

**Phase 1 (Sprint 6):** `RULE_CATALOG` remains the source of truth for rule definitions.
On app startup, seed the `detection_rules` DB table FROM `RULE_CATALOG` (idempotent upsert
by `rule_id`). `ThresholdManager` continues using `RULE_MAP` for defaults. The DB table
enables the Chirp Config UI to query rules via API without importing Python code.

**Phase 2 (post-Sprint 6):** If per-tenant rule customization beyond threshold tuning is
needed (custom rule definitions, not just enable/disable), migrate rule authoring to the
DB table and deprecate `RULE_CATALOG`.

**No code change to `rule_definitions.py` in Sprint 6. Startup seed script only.**

### ThresholdManager Valkey Wiring

**Current state:** `ThresholdManager.__init__()` in `canary/services/chirp/threshold_manager.py`
accepts `valkey_client=None`. When None, all threshold lookups bypass cache and query
PostgreSQL directly. This works but adds latency to every detection evaluation.

**Sprint 6 requirement:** Wire `valkey_client` during detection engine initialization:

```python
import redis
valkey = redis.Redis.from_url(app.config["VALKEY_URL"], db=1)  # DB 1 = Chirp rule cache
threshold_mgr = ThresholdManager(db_session=session, valkey_client=valkey)
```

### Codebase Reconciliation Note

The existing codebase (`canary/models/app/detection.py`) already defines four models: `DetectionRule`, `MerchantRuleConfig`, `Alert`, and `AlertHistory`. The schemas below reflect the **existing code as source of truth** with Sprint 6 additions noted. Do NOT create parallel schemas — extend what's built.

### Detection Rules Table (EXISTING — no changes needed)

**Database:** `canary_app`
**Table:** `detection_rules`
**Model:** `DetectionRule` in `canary/models/app/detection.py`

Already contains: `rule_id` (C-001 through C-804), `rule_name`, `description`, `category`, `default_threshold` (JSON text), `severity`, `is_active`. Global catalog — not tenant-scoped. Seeded from `rule_definitions.py` (26 rules across 8 categories).

### Alerts Table (EXISTING — Sprint 6 additions)

**Database:** `canary_app`
**Table:** `alerts`
**Model:** `Alert` in `canary/models/app/detection.py`

Existing columns (keep as-is):
- `id` (UUID PK), `merchant_id`, `rule_id`, `alert_type`, `severity`
- `source_table`, `source_id` — table + row that triggered the alert
- `employee_id`, `location_id` — nullable FKs
- `details` (Text/JSON), `amount_cents` (Integer)
- `created_at`, `created_by` (system: 'chirp')

**Sprint 6 additions:**

```sql
ALTER TABLE alerts ADD COLUMN event_id TEXT;
ALTER TABLE alerts ADD COLUMN title TEXT;
ALTER TABLE alerts ADD COLUMN description TEXT;
ALTER TABLE alerts ADD CONSTRAINT uq_alerts_rule_event UNIQUE (rule_id, source_table, source_id);

CREATE INDEX idx_alerts_event_id ON alerts (event_id);
```

- `event_id`: links alert back to the pipeline event (for TSP-07/TSP-08 cross-reference).
- `title` + `description`: human-readable alert text for the dashboard (Today's View).
- `uq_alerts_rule_event`: deduplication constraint — same rule + same source row = no duplicate alert.

### Alert History Table (EXISTING — no changes needed)

**Database:** `canary_app`
**Table:** `alert_history`
**Model:** `AlertHistory` in `canary/models/app/detection.py`

Status lifecycle: `new` → `acknowledged` → `investigating` → `resolved` | `false_positive`. One row per status change. Already built.

### Merchant Rule Config Table (EXISTING — field name alignment)

**Database:** `canary_app`
**Table:** `merchant_rule_config`
**Model:** `MerchantRuleConfig` in `canary/models/app/detection.py`

Existing columns: `id` (UUID PK), `merchant_id`, `rule_id`, `is_enabled` (Boolean), `custom_threshold` (Text/JSON).

**Note:** Code uses `is_enabled` (not `enabled`) and `custom_threshold` (not `thresholds`). The `ThresholdManager` already handles cache → DB → defaults fallback with optional Valkey cache (TTL 300s). No schema changes needed.

---

## Acceptance Criteria

1. Within 500ms of Sub 2 writing a structured record, the detection engine evaluates all enabled Chirp rules for that merchant against the new data.
2. Only rules toggled ON for that merchant (via `merchant_rule_config.is_enabled`) are evaluated. ThresholdManager loads thresholds with cache → DB → defaults fallback.
3. When a rule fires, an alert record is written to the `alerts` table with full context (rule_id, alert_type, severity, title, description, source_table, source_id, event_id, employee_id, location_id, amount_cents, details). An `alert_history` record is created with status `new`.
4. An SSE event (Phase 1) or WebSocket message (Phase 2) is pushed to all authenticated, connected clients for that merchant within 100ms of alert creation.
5. Rules that do NOT fire produce no alert record and no push notification.
6. The detection engine handles rule evaluation failures gracefully — a failing rule does not prevent other rules from being evaluated. Per-rule try/catch with logging.
7. Alert deduplication: UNIQUE constraint on `(rule_id, source_table, source_id)` prevents duplicate alerts for the same rule on the same source row. INSERT ON CONFLICT DO NOTHING.
8. Latency target: Sub 2 INSERT → alert visible in Today's View < 500ms (p95).
9. Detection engine reads from Valkey Stream `canary:detection` via consumer group `detection-engine`. No messages lost if detection engine is temporarily down.
10. On startup, detection engine defensively creates consumer group and processes any backlog.
11. Phase 1 Sprint 6 scope: payment rules (C-004, C-007 fully implemented; C-001, C-002, C-003 window queries), cash drawer rules (C-101, C-102, C-103, C-104), void rules (C-502). All other categories deferred.
12. SSE/WebSocket connections require valid session authentication. Unauthenticated connections rejected.

---

## Error Handling

| Error | Detection | Response | Recovery |
|-------|-----------|----------|----------|
| Detection stream message missed | Detection engine was down | Not possible — Valkey Streams persist messages until consumed. On restart, XREADGROUP delivers backlog. | Automatic — process backlog on startup. |
| Rule evaluation exception | Try/catch per rule | Log error with rule_id, event_type, merchant_id, and source row context. Skip that rule. Evaluate remaining rules. XACK the message (don't block stream). | Fix rule logic. No data loss — event data still in structured store for re-evaluation. |
| Alert INSERT failure | PostgreSQL error or UNIQUE constraint violation | UNIQUE violation = expected dedup, log at DEBUG. Other errors: log at ERROR, retry once. If persistent, alert ops. | Investigate DB. Event data persists in structured store. |
| SSE/WebSocket connection dropped | Client disconnect | Last 50 alerts cached per merchant in ring buffer. Delivered on reconnect via Last-Event-ID. Client deduplicates by alert.id. | Automatic reconnect with cached delivery. |
| ThresholdManager lookup failure | Config table or Valkey unavailable | Use default thresholds from `RULE_CATALOG`. Log warning. | Investigate canary_app DB or Valkey. Detection continues with defaults. |
| Unknown event_type in notification | event_type not in routing table | Log warning. XACK the message. No rule evaluation. | Add parser + routing entry when new event types are supported. |
| Structured row not found | row_ids point to non-existent row | Sub 2 may not have committed yet (race condition). Retry after 100ms. If still missing after 3 retries, log error and XACK. | Rare — indicates Sub 2 transaction failure. Event data in evidence_records for audit. |

---

## Test Cases

### Happy Path

1. **C-102 fires on short drawer:** Sub 2 writes a `cash_drawer_shifts` record where counted < expected by > threshold, publishes to `canary:detection` stream. Verify: detection engine reads notification, queries shift row via `row_ids`, C-102 evaluates, alert created with correct `source_table=cash_drawer_shifts`, `source_id`, `amount_cents=-2350`, `alert_type=CASH_VARIANCE`. SSE event pushed to authenticated merchant client.

2. **Rule toggle OFF suppresses alert:** Toggle C-102 OFF via `merchant_rule_config.is_enabled=false`. Insert same short drawer. Verify: no alert created. ThresholdManager cache invalidated.

3. **C-004 fires on after-hours payment:** Sub 2 writes a `transactions` record with `created_at` at 2 AM. Verify: C-004 alert fires with `source_table=transactions`, `details={"hour": 2}`.

### Deduplication

4. **Duplicate event produces no duplicate alert:** Same event processed twice (e.g., stream re-delivery). Verify: UNIQUE constraint on `(rule_id, source_table, source_id)` prevents second alert. INSERT ON CONFLICT DO NOTHING. No error logged.

### Stream Durability

5. **Detection engine down during events:** Stop detection engine. Sub 2 processes 10 events and publishes to `canary:detection` stream. Start detection engine. Verify: all 10 notifications processed from backlog. All alerts created correctly.

### Toy Store Spike

6. **5,000 events, mixed types:** Simulate 6-hour inflow. Verify: detection evaluates all events. Alerts fire only for threshold breaches. No false alerts from parsing delay. Stream consumer group lag stays < 50 messages.

### Timing

7. **End-to-end latency:** Square webhook → gateway → queue → Sub 2 parse → detection → SSE push. Total < 600ms for p95.

### Authentication

8. **Unauthenticated SSE rejected:** Connect to `/api/alerts/stream/{merchant_id}` without session token. Verify: connection rejected with 401.

9. **Wrong merchant SSE rejected:** Connect with valid session for merchant A but request alerts for merchant B. Verify: connection rejected with 403.

---

## Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `DATABASE_URL` | string | — | canary_app connection |
| `SALES_DATABASE_URL` | string | — | canary_sales connection (read structured data) |
| `VALKEY_URL` | string | `redis://localhost:6379` | For streams and ThresholdManager cache |
| `DETECTION_STREAM` | string | `canary:detection` | Valkey Stream for detection notifications |
| `DETECTION_CONSUMER_GROUP` | string | `detection-engine` | Consumer group name |
| `STREAM_BLOCK_MS` | integer | 5000 | XREADGROUP block timeout |
| `STREAM_BATCH_SIZE` | integer | 10 | Messages per XREADGROUP call |
| `ROW_LOOKUP_RETRY_MS` | integer | 100 | Delay before retry when structured row not found |
| `ROW_LOOKUP_MAX_RETRIES` | integer | 3 | Max retries for missing structured row |
| `SSE_RING_BUFFER_SIZE` | integer | 50 | Alerts cached per merchant for SSE reconnection replay |
| `MAX_ALERT_CACHE_PER_MERCHANT` | integer | 50 | Buffered alerts for reconnecting clients |
| `THRESHOLD_CACHE_TTL_SECONDS` | integer | 300 | ThresholdManager Valkey cache TTL |

---

## Deployment Readiness (Docker Compose)

1. **Stateless?** Yes. All state in PostgreSQL and Valkey. SSE connections are ephemeral.
2. **Horizontal scaling?** Scaling is via Gunicorn `--workers N` flag in the Flask container (`devops/docker-compose.alpha3x.yml`, line ~279). For dedicated worker processes (queue consumers), add a new service definition to docker-compose.alpha3x.yml inheriting the same build context with a different `command:` entrypoint. No orchestrator — manual `docker compose up --scale service=N`.
3. **Rolling deployment?** Not supported in Docker Compose. Blue-green deployment via `docker compose up -d` with new image tag. Downtime window: ~5 seconds during container replacement.
4. **Scaling trigger?** Manual. Monitor via Prometheus metrics + Grafana dashboards. Alert threshold: Detection stream consumer group lag > 100 messages. Or SSE connection count > 1,000.
5. **Toy store scaling profile:** Single instance handles 50x volume. Detection is CPU-light (rule evaluation is simple comparison logic, most rules are threshold checks).

**Cross-PRD Sync (Gap 7):** Synced: all deployment sections reference Docker Compose + Gunicorn (no K8s).

---

## Non-Functional Requirements

| Metric | Target |
|--------|--------|
| **Detection latency (p95)** | < 500ms from Sub 2 INSERT to alert record written |
| **SSE push (p95)** | < 100ms from alert creation to client delivery |
| **Rule evaluation throughput** | 1,000 events/second (26 rules per event = 26,000 rule evaluations/sec) |
| **False positive target** | < 30% across all rules (measured over first month of live data) |

---

## IP Protection Notes

Chirp rule definitions, threshold values, and detection logic are Crown Jewels. This PRD describes the detection engine MECHANICS (how it's triggered, how it evaluates, how it delivers alerts) but does NOT include rule logic, thresholds, or evaluation algorithms. Rule mappings are in PRD E1-F14 (merchant-facing names only). Internal rule logic is in `Canary/canary/services/chirp/rule_definitions.py` (never externalized).

---

## Integration Checklist

- [ ] **TSP-04 cross-update needed:** Sub 2 must publish to Valkey Stream `canary:detection` (not pub/sub) with `row_ids` field in notification
- [ ] Depends on TSP-04 — detection notification shape agreed (event_type + row_ids + parse_failed)
- [ ] References PRD E1-F14 — rule definitions and toggle API
- [ ] Existing codebase reconciled — `Alert` model extended with `event_id`, `title`, `description` columns; dedup UNIQUE constraint added
- [ ] `DetectionRule` table seeded from `rule_definitions.py` (26 rules)
- [ ] SSE endpoint (`/api/alerts/stream/{merchant_id}`) accessible from frontend with session authentication
- [ ] Alert table schema aligned with Today's View frontend expectations (source_table + source_id + alert_type + title)
- [ ] ThresholdManager instantiated with live Valkey client (DB 1) in detection engine startup
- [ ] Cache hit/miss logging verified in detection engine test run
- [ ] ThresholdManager integration verified (cache → DB → defaults)
- [ ] Phase 1 rule checkers implemented: payment (C-004, C-007 done; C-001, C-002, C-003 window queries), cash drawer (C-101, C-102, C-103, C-104), void (C-502)
- [ ] Phase 3 dependency: Jeremy SDK Audit (P0-1) — Labor API polling adapter for C-301/C-302/C-303

---

---

## Revision Log

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-26 | Initial draft |
| 1.1 | 2026-02-28 | (ALX review) Replaced Valkey pub/sub trigger with Valkey Streams (`canary:detection` stream, consumer group `detection-engine`) for message durability. Removed polling fallback (Streams provide durability natively). Added `row_ids` to notification shape — detection engine needs structured table row IDs, not pipeline event_id, to evaluate rules. Reconciled data model with existing codebase (`canary/models/app/detection.py`): kept existing `Alert` model as source of truth, added Sprint 6 columns (`event_id`, `title`, `description`), added dedup UNIQUE constraint on `(rule_id, source_table, source_id)`. Documented existing `DetectionRule`, `AlertHistory`, `MerchantRuleConfig` models — no parallel schemas. Added Phase 1 Sprint 6 rule scope: payment (C-004, C-007 implemented; C-001/C-002/C-003 TODO), cash drawer (C-101 through C-104), void (C-502). Deferred order/timecard/gift card/loyalty rules. Added Event Type → Rule Checker routing table. Added WebSocket authentication requirement (session token validation). Added parse_failed handling note (detection never sees them — correct). Added 9 test cases (up from 4). Updated error handling for Streams semantics. Updated config vars. Added TSP-04 cross-update flag (publish to Stream with row_ids). Fixed FIG. 3 mapping (Flask, not Node.js). |
| 1.2 | 2026-02-27 | (ALX, B-059) Deployment Readiness rewritten for Docker Compose + Gunicorn (removed K8s references). Clarified SSE Phase 1 replaces WebSocket for real-time alert push. Replaced polling fallback with Streams-based trigger. Added rule routing dispatcher (event_type → applicable Chirp rules). Added Toy Store Spike Scenario. Cross-PRD sync notes added (Gap 1: Streams not pub/sub, Gap 7: Docker Compose). |

---

*TSP-06 | Detection Engine | CONFIDENTIAL*
*Condor | February 27, 2026*
