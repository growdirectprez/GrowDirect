---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# GRO-27 — Polling Adapter Design: Square Labor API + Cash Drawer API

**Issue:** GRO-27 (B-047) — Scope expanded per GRO-20 audit findings
**Prepared By:** ALX (Chief of Staff)
**Date:** March 2, 2026
**Classification:** Internal — Architecture Design Document
**Gate:** Tom validates architecture. Jim writes test plan.
**Done When:** Polling adapter design documented and approved.
**Scope:** Design only. No build.

---

## 1. Problem Statement

Two Square API families critical to Canary LP's detection engine have **no webhook support**:

| API Family | SDK Namespace | Webhook Events | LP Signal |
|-----------|--------------|----------------|-----------|
| **Labor (Timecards)** | `client.labor` | NONE — poll-only | Ghost employee, off-clock transactions (C-301), during-break transactions (C-302), wrong-location activity (C-303) |
| **Cash Drawers** | `client.cash_drawers.shifts` | NONE — poll-only | Cash variance (C-201), excessive paid-out (C-202), high no-sale (C-203), drawer left open |

**Source:** GRO-20 (Square SDK → CRDM Alignment Audit) + B-067-A (Square Capability Map)

The TSP pipeline (TSP-01 through TSP-06) is designed around webhook-driven events published to Valkey Streams. Poll-only APIs cannot use this path directly. We need a polling adapter that fetches data on a schedule, wraps it in the TSP message format, and publishes to the same `canary:events` stream — making poll-sourced events indistinguishable from webhook-sourced events downstream.

---

## 2. Design Principle: Synthetic Events

The polling adapter generates **synthetic webhook events** — messages in the exact same format as real webhook events (TSP-01 v1.1 schema, 9 fields). Downstream consumers (Sub 1, Sub 2, Sub 3, Detection Engine) cannot and should not distinguish between real and synthetic events.

This means:
- Sub 1 seals synthetic events identically (raw evidence)
- Sub 2 parses synthetic events into the same CRDM tables
- Sub 3 batches synthetic events into the same Merkle trees
- TSP-06 evaluates Chirp rules against synthetic events identically

The only difference is the `source` field and event origin tracking in metadata.

---

## 3. Architecture

```
┌──────────────────────────────────────────────┐
│  Polling Adapter Service                      │
│  (Docker container — runs alongside TSP)      │
│                                               │
│  ┌─────────────┐    ┌──────────────────────┐ │
│  │ Scheduler    │    │ Poll Workers         │ │
│  │ (APScheduler │───▶│                      │ │
│  │  or Airflow  │    │ ┌──────────────────┐ │ │
│  │  DAG)        │    │ │ Labor Poller     │ │ │
│  │              │    │ │ - search_timecards│ │ │
│  │              │    │ │ - diff detection  │ │ │
│  │              │    │ └──────────────────┘ │ │
│  │              │    │ ┌──────────────────┐ │ │
│  │              │    │ │ Cash Drawer Poll │ │ │
│  │              │    │ │ - list shifts    │ │ │
│  │              │    │ │ - diff detection  │ │ │
│  │              │    │ └──────────────────┘ │ │
│  └─────────────┘    └──────────┬───────────┘ │
│                                │              │
│  ┌─────────────────────────────▼────────────┐ │
│  │ Synthetic Event Publisher                 │ │
│  │ XADD canary:events * (TSP-01 schema)     │ │
│  └───────────────────────────────────────────┘ │
└──────────────────────────────────────────────┘
                         │
                         ▼
              canary:events (Valkey Stream)
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
          Sub 1      Sub 2      Sub 3
         (seal)     (parse)   (inscribe)
```

---

## 4. Polling Strategy: Change Detection

### The Problem with Naive Polling

Naive approach: poll every N minutes, insert everything. This creates massive duplication. Square doesn't provide a "changes since" filter for Labor or Cash Drawers.

### Solution: High-Water Mark + Diff

Each poller maintains a **high-water mark** (HWM) — the last-seen state per entity. On each poll cycle:

1. Fetch current state from Square API (with time-bounded pagination per B-067-A coding standards)
2. Compare against last-known state (stored in `canary_app.polling_state`)
3. Emit synthetic events ONLY for changes

### 4.1 Labor Poller

```python
# Polling cycle (every 5 minutes)
def poll_labor(merchant_id: str, location_ids: list[str]):
    for location_id in location_ids:
        # Time-bounded query (never open-ended per coding standard 4)
        timecards = client.labor.search_timecards(
            filter={
                "location_ids": [location_id],
                "start": {
                    "start_at": last_poll_timestamp  # HWM
                }
            }
        )

        for tc in timecards:
            known_state = get_polling_state(merchant_id, 'timecard', tc.id)

            if known_state is None:
                # New timecard — emit labor.shift.created
                emit_synthetic_event(
                    event_type='labor.shift.created',
                    merchant_id=merchant_id,
                    payload=serialize_timecard(tc)
                )
            elif tc.updated_at > known_state.last_seen_at:
                if tc.status == 'CLOSED' and known_state.status != 'CLOSED':
                    # Shift closed — emit labor.shift.closed
                    emit_synthetic_event(
                        event_type='labor.shift.closed',
                        merchant_id=merchant_id,
                        payload=serialize_timecard(tc)
                    )
                else:
                    # Updated (break start/end, etc.) — emit labor.shift.updated
                    emit_synthetic_event(
                        event_type='labor.shift.updated',
                        merchant_id=merchant_id,
                        payload=serialize_timecard(tc)
                    )

            # Update HWM
            upsert_polling_state(merchant_id, 'timecard', tc.id, tc.status, tc.updated_at)
```

**SDK calls:**
- `client.labor.search_timecards(filter={"location_ids": [...], "start": {"start_at": ...}})` — paginated with time window
- `client.labor.retrieve_timecard(timecard_id=...)` — for individual refresh if needed

**Note:** Square renamed Shift→Timecard in v2025-05-21. SDK uses `search_timecards()` / `retrieve_timecard()`. CRDM table is `employee_timecards`.

### 4.2 Cash Drawer Poller

```python
# Polling cycle (every 5 minutes)
def poll_cash_drawers(merchant_id: str, location_ids: list[str]):
    for location_id in location_ids:
        shifts = client.cash_drawers.shifts.list(
            location_id=location_id,
            begin_time=last_poll_timestamp,  # HWM
            end_time=now()
        )

        for shift in shifts:
            known_state = get_polling_state(merchant_id, 'cash_drawer_shift', shift.id)

            if known_state is None:
                # New shift — emit cash_drawer.shift.created
                emit_synthetic_event(
                    event_type='cash_drawer.shift.created',
                    merchant_id=merchant_id,
                    payload=serialize_cash_drawer_shift(shift)
                )
            elif shift.state != known_state.status:
                # State changed (OPEN → CLOSED) — emit cash_drawer.shift.updated
                emit_synthetic_event(
                    event_type='cash_drawer.shift.updated',
                    merchant_id=merchant_id,
                    payload=serialize_cash_drawer_shift(shift)
                )

                # If closed, fetch detailed shift to get events
                if shift.state == 'CLOSED':
                    detail = client.cash_drawers.shifts.retrieve(
                        shift_id=shift.id,
                        location_id=location_id
                    )
                    for event in detail.events:
                        if not event_already_seen(merchant_id, event.id):
                            emit_synthetic_event(
                                event_type='cash_drawer.event.created',
                                merchant_id=merchant_id,
                                payload=serialize_cash_drawer_event(event, shift.id)
                            )

            upsert_polling_state(merchant_id, 'cash_drawer_shift', shift.id, shift.state, now())
```

**SDK calls:**
- `client.cash_drawers.shifts.list(location_id=..., begin_time=..., end_time=...)` — list shifts
- `client.cash_drawers.shifts.retrieve(shift_id=..., location_id=...)` — get shift detail with events

---

## 5. Synthetic Event Format

Synthetic events use the EXACT same TSP-01 v1.1 message schema:

```
XADD canary:events * \
  event_id       "evt_poll_01HY2A3B4C5D" \
  merchant_id    "6SSW7HV8K2ST5" \
  source         "square:poll" \
  source_event_id "TIMECARD_abc123" \
  event_type     "labor.shift.created" \
  event_hash     "<SHA-256 of serialized payload>" \
  raw_payload    "<JSON — synthetic payload matching Square webhook format>" \
  received_at    "2026-03-02T15:00:05Z" \
  parse_failed   "false"
```

**Key differences from real webhooks:**
- `source` = `"square:poll"` (not `"square"`) — allows downstream to distinguish if needed, but Sub 1/2/3 don't look at this field
- `event_id` prefix = `"evt_poll_"` — ULID, but with poll prefix for tracing
- `source_event_id` = Square object ID (timecard ID or shift ID), not a webhook event ID
- `raw_payload` = JSON serialization of the Square API response object, wrapped in a structure that matches the webhook event envelope

### Payload Envelope (Mimics Webhook)

```json
{
  "merchant_id": "6SSW7HV8K2ST5",
  "type": "labor.shift.created",
  "event_id": "evt_poll_01HY2A3B4C5D",
  "created_at": "2026-03-02T15:00:05Z",
  "data": {
    "type": "timecard",
    "id": "TIMECARD_abc123",
    "object": {
      "timecard": {
        "id": "TIMECARD_abc123",
        "employee_id": "EMP_xyz789",
        "location_id": "L88917AVBK2S5",
        "clockin_at": "2026-03-02T08:00:00Z",
        "clockout_at": null,
        "status": "OPEN",
        "breaks": []
      }
    }
  }
}
```

This envelope format means Sub 2 parsers (TSP-04) can use the same field paths (`data.object.timecard.*`) regardless of whether the event came from a real webhook or a poll.

---

## 6. State Storage: `polling_state` Table

New table in `canary_app`:

```sql
CREATE TABLE canary_app.polling_state (
    id                  UUID            NOT NULL DEFAULT gen_random_uuid(),
    merchant_id         UUID            NOT NULL,
    entity_type         TEXT            NOT NULL,
    entity_id           TEXT            NOT NULL,
    last_status         TEXT,
    last_seen_at        TIMESTAMPTZ     NOT NULL,
    last_hash           TEXT,           -- SHA-256 of last-seen serialized state
    poll_source         TEXT            NOT NULL DEFAULT 'square',
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),

    CONSTRAINT pk_polling_state PRIMARY KEY (id),
    CONSTRAINT uq_polling_state UNIQUE (merchant_id, entity_type, entity_id, poll_source),
    CONSTRAINT chk_ps_entity_type CHECK (entity_type IN (
        'timecard', 'cash_drawer_shift', 'cash_drawer_event'
    ))
);

CREATE INDEX idx_polling_state_merchant ON polling_state (merchant_id, entity_type);
CREATE INDEX idx_polling_state_last_seen ON polling_state (merchant_id, last_seen_at);
```

**Purpose:** Track what we've already seen so we only emit synthetic events for changes. The `last_hash` column enables deep diff — if the JSON serialization changes but the status doesn't, we still detect the change.

### High-Water Mark Table

```sql
CREATE TABLE canary_app.polling_high_water_marks (
    id                  UUID            NOT NULL DEFAULT gen_random_uuid(),
    merchant_id         UUID            NOT NULL,
    poll_type           TEXT            NOT NULL,
    location_id         TEXT,
    last_poll_at        TIMESTAMPTZ     NOT NULL,
    last_success_at     TIMESTAMPTZ,
    consecutive_failures INTEGER        NOT NULL DEFAULT 0,

    CONSTRAINT pk_hwm PRIMARY KEY (id),
    CONSTRAINT uq_hwm UNIQUE (merchant_id, poll_type, location_id),
    CONSTRAINT chk_hwm_type CHECK (poll_type IN ('labor', 'cash_drawer'))
);
```

**Purpose:** Track when we last polled each merchant/location/type. Enables:
- Resuming after downtime (poll from last HWM, not from epoch)
- Circuit breaker (if `consecutive_failures` > 5, pause polling for this merchant and alert)
- Metrics (last_poll_at vs now = polling freshness)

---

## 7. Scheduling

### Option A: APScheduler (Recommended for MVP)

```python
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

# Labor: poll every 5 minutes
scheduler.add_job(
    poll_all_merchants_labor,
    'interval',
    minutes=5,
    id='labor_poller',
    max_instances=1,  # prevent overlap
    misfire_grace_time=120
)

# Cash Drawers: poll every 5 minutes
scheduler.add_job(
    poll_all_merchants_cash_drawers,
    'interval',
    minutes=5,
    id='cash_drawer_poller',
    max_instances=1,
    misfire_grace_time=120
)

scheduler.start()
```

**Why APScheduler for MVP:**
- Already Python (no new language/runtime)
- Runs in the same Docker container or a dedicated `polling-adapter` service
- `max_instances=1` prevents overlap if a poll cycle runs long
- Lightweight — no Airflow overhead for 2 jobs

### Option B: Airflow DAG (Phase 2+ at Scale)

```python
# canary/devops/airflow/dags/canary_polling_adapter.py
# (placeholder already exists at canary_timecard_sync.py)

with DAG('canary_polling_adapter', schedule_interval='*/5 * * * *') as dag:
    poll_labor = PythonOperator(task_id='poll_labor', python_callable=poll_all_merchants_labor)
    poll_cash = PythonOperator(task_id='poll_cash_drawers', python_callable=poll_all_merchants_cash_drawers)
    poll_labor >> poll_cash  # sequential to avoid API rate limit overlap
```

**When to migrate:** When we exceed 50 merchants OR need per-merchant scheduling granularity OR Airflow 3.0 migration (GRO-30) is complete.

### Polling Frequency Decision

| Factor | Consideration |
|--------|--------------|
| **Square rate limits** | 120 requests/minute per application. At 1 merchant × 2 locations × 2 APIs = 4 calls/cycle. Plenty of headroom. |
| **Detection latency** | C-301 (off-clock transaction) needs timely timecard data. 5-minute polling means worst-case 5-minute delay in detection. |
| **Cost** | API calls are free (no per-call charge from Square). Infrastructure cost only. |
| **Scaling** | At 100 merchants × 5 locations × 2 APIs = 1,000 calls/cycle. At 5-min interval = 200 calls/min. Within Square rate limits but getting close. May need staggered scheduling. |

**Recommendation:** 5-minute interval for MVP. Configurable per-merchant via environment variable. Consider 1-minute for Phase 2 if detection latency matters for specific Chirp rules.

---

## 8. Chirp Rules Enabled by Polling Adapter

These rules are currently deferred to Phase 2 pending the polling adapter. This design unblocks them:

### Labor-Dependent Chirps

| Rule | Name | What It Detects | Polling Data Needed |
|------|------|-----------------|---------------------|
| C-301 | `OFF_CLOCK_TRANSACTION` | Transaction processed when no employee is clocked in | Join `transactions.created_at` against `employee_timecards` for active shifts |
| C-302 | `BREAK_TRANSACTION` | Transaction processed during employee's break period | Join `transactions.created_at` against `employee_timecards.breaks` JSONB |
| C-303 | `WRONG_LOCATION_ACTIVITY` | Employee clocked in at Location A, transaction at Location B | Compare `employee_timecards.location_id` vs `transactions.location_id` |

### Cash Drawer-Dependent Chirps

| Rule | Name | What It Detects | Polling Data Needed |
|------|------|-----------------|---------------------|
| C-201 | `CASH_VARIANCE` | Cash drawer over/short at close exceeds threshold | `cash_drawer_shifts.variance_cents` (expected - counted) |
| C-202 | `EXCESSIVE_PAID_OUT` | Too many paid-out events per shift | Count of `cash_drawer_events` where `event_type = 'PAID_OUT'` per shift |
| C-203 | `HIGH_NO_SALE_FREQUENCY` | Too many no-sale drawer opens per shift | Count of `cash_drawer_events` where `event_type = 'NO_SALE'` per shift |
| C-204 | `DRAWER_LEFT_OPEN` | Cash drawer shift not closed within expected timeframe | `cash_drawer_shifts.status = 'OPEN'` AND `opened_at` > threshold |

**Note:** C-204 is a new rule proposal — not in CRDM v1.0 Chirp list. Adding it here because the polling adapter makes this detection trivial.

---

## 9. Error Handling

| Error | Detection | Response | Recovery |
|-------|-----------|----------|----------|
| Square API rate limit (429) | HTTP 429 response | Exponential backoff (SDK built-in: max 2 retries). Log warning. | Retry next poll cycle. Increment `consecutive_failures`. |
| Square API timeout | Connection timeout | Log error. Do NOT emit synthetic events for this cycle. | Retry next cycle. HWM unchanged — no data gap. |
| Square API auth failure (401) | HTTP 401 | ALERT — merchant OAuth token may be expired or revoked. | Pause polling for this merchant. Alert ops. Require merchant re-auth. |
| Valkey XADD failure | XADD returns error | Do NOT update HWM. Events will be re-detected next cycle. | Retry next cycle. |
| Duplicate detection | Same entity, same state, same hash | Skip — no synthetic event emitted. | Design intent. |
| Merchant has no active locations | Location list empty | Skip merchant. Log info. | Normal for deactivated merchants. |
| Poller overlap (previous cycle still running) | APScheduler `max_instances=1` | Skip this cycle. Log warning. | Previous cycle completes. Next cycle runs normally. |
| Circuit breaker (>5 consecutive failures) | `consecutive_failures > 5` in HWM table | Pause polling for this merchant. Emit alert. | Manual investigation. Reset `consecutive_failures` after fix. |

---

## 10. Observability

### Prometheus Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `canary_poll_cycle_duration_seconds` | Histogram | Time per poll cycle by poll_type and merchant |
| `canary_poll_events_emitted_total` | Counter | Synthetic events published by type |
| `canary_poll_api_calls_total` | Counter | Square API calls by endpoint |
| `canary_poll_errors_total` | Counter | Errors by type (rate_limit, timeout, auth, etc.) |
| `canary_poll_freshness_seconds` | Gauge | Time since last successful poll per merchant/type |
| `canary_poll_hwm_lag_seconds` | Gauge | Difference between HWM and now |

### Grafana Dashboard

New panel on existing DevOps dashboard:
- Poll cycle health (success/failure rate)
- Events emitted per cycle
- API call budget vs. usage
- Per-merchant polling freshness
- Circuit breaker status

---

## 11. Migration from Phase 1 → Phase 2

### What Changes in TSP

| Component | Change | Effort |
|-----------|--------|--------|
| TSP-01 | No change — doesn't know about polling | 0 |
| TSP-02 | No change — stream accepts all XADD sources | 0 |
| TSP-03 (Sub 1) | No change — seals all events identically | 0 |
| TSP-04 (Sub 2) | Enable `labor.shift.*` and `cash_drawer.*` parsers (already defined in Phase 2 scope) | ~1 day |
| TSP-05 (Sub 3) | No change — inscribes all events | 0 |
| TSP-06 (Detection) | Enable C-201, C-202, C-203, C-301, C-302, C-303 rules | ~2 days |
| **Polling Adapter** | New service (this design) | ~3-4 days |

**Total estimated effort:** ~6-7 days to go from Phase 1 (webhook-only) to Phase 2 (webhook + poll hybrid).

---

## 12. Open Questions for Tom

1. **Synthetic event hashing:** Should the `event_hash` for synthetic events be computed from the serialized payload (consistent with TSP-01) or from a canonical form (sorted JSON keys)? The payload is constructed by us, not received from Square, so we control the format.

2. **Poll-vs-webhook deduplication:** If Square eventually adds webhooks for Labor/Cash Drawers (not announced but possible), we'd receive both webhook events AND poll-detected changes. How do we deduplicate? Proposal: `source_event_id` (Square object ID) is the dedup key — the existing `canary:dedup` cache (DB 3) handles this.

3. **Multi-merchant scheduling:** At 50+ merchants, sequential polling will take too long for 5-minute cycles. Switch to per-merchant parallel polling with a semaphore to respect Square rate limits? Or partition merchants across multiple poller instances?

4. **C-204 (Drawer Left Open):** New rule or existing? If new, what's the default threshold? 4 hours? 8 hours (full shift)? Per-location configurable?

5. **Polling adapter container:** Separate Docker service (`canary-poller`) or thread within the main Flask app? Recommendation: separate service for isolation and independent scaling.

---

## 13. Routing

| Agent | Action | Deliverable |
|-------|--------|-------------|
| **Tom** | Validate architecture, answer 5 open questions, confirm synthetic event schema | Approved design |
| **Jeremy** | Review implementation approach, estimate effort, confirm APScheduler vs Airflow | Effort estimate + tech selection |
| **Jim** | Write QA plan: poll cycle testing, synthetic event validation, Chirp rule activation | Test plan |

---

*ALX | GRO-27 | March 2, 2026*
*CONFIDENTIAL*
