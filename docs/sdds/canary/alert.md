# Alert

## Overview

The Alert domain is the terminal consumer of Canary's detection pipeline. Chirp writes alert rows; the Alert domain owns everything after: lifecycle state tracking, dollar-impact scoring, notification delivery, and MCP tool access. Alerts are never forwarded to another domain — they are resolved, dismissed, escalated to Fox cases, or auto-archived by TTL.

**Core principle: APPEND-ONLY.** The `alerts` row is immutable after creation. All state changes are new `alert_history` rows. Status is derived by reading the latest history entry (no history = "new").

**Services (all pure-logic, no ORM imports):**

- `alert_lifecycle.py` — TTL staleness (default 14 days), auto-archival, age decay for Owl priority, active/stale filtering, lifecycle summary counts.
- `impact_scoring.py` — Category-specific dollar impact at alert creation. Rule prefix maps to formula (C-1xx=refund, C-2xx=void, C-3xx=cash, C-4xx=no-sale, C-5xx=discount at 1.5x, C-6xx=time-based at 2.0x, C-7xx=custom at 1.2x). Severity-based fallback when no amount available (critical=$500, high=$200, medium=$50, low=$10).
- `notification_service.py` — Routes alerts to SMS/email/in-app/push channels. Applies severity filtering, quiet-hours suppression, daily rate caps, and digest batching (realtime/hourly/daily/weekly).

**Status machine:** `new` -> `investigating` / `escalated` / `resolved` [TERMINAL] / `dismissed` [TERMINAL] / `case_opened` [TERMINAL] / `archived` [TERMINAL]. Four terminal states. No alert purgatory.

**MCP server:** `canary-alert` with 6 tools (4 pure, 2 DB-read). Blueprint at `/alert/*` via `alert_mcp.py`. REST API at `/api/alerts/*` via `alerts_wired.py`.

**Domain boundaries:** Inbound from Chirp (alert writes), Webhook Pipeline (via sub4_detect), and Owl (reads alerts, writes history via action dispatcher). Outbound to none — terminal domain.

## API Contracts

### REST API (`alerts_wired.py` -> `/api/alerts/*`)

All routes require JWT authentication. Role-gated actions require owner/manager/admin.

| Route | Method | Auth | Purpose |
|-------|--------|------|---------|
| `/` | GET | JWT | List alerts. Filters: `severity`, `rule_id`, `created_after`, `created_before`. Pagination: `page`, `limit` (default 20). Returns `{alerts, pagination}`. |
| `/<alert_id>` | GET | JWT | Single alert with full history array. |
| `/<alert_id>/investigate` | PUT | JWT+roles | Set status to "investigating". Rejects if already processed. |
| `/<alert_id>/dismiss` | PUT | JWT+roles | Dismiss with required `reason`. Writes AlertHistory(status="dismissed"). |
| `/<alert_id>/escalate` | POST | JWT+roles(owner/admin) | Escalate alert priority. |
| `/<alert_id>/open-case` | POST | JWT+roles(owner/operator/admin) | Create Fox case from alert. Writes AlertHistory(status="case_opened"). Returns `{case_id, case_number}`. |
| `/summary` | GET | JWT | Counts by severity, by status, and by time window (24h/7d/30d). |

Error responses: 404 (not found), 400 (already processed, missing reason, bad request), 500 (internal, logged).

### MCP Server (`canary-alert` at `/alert/*`)

6 tools registered in `canary/services/alerts/tools.py`:

| Tool | Category | DB? | Input | Output |
|------|----------|-----|-------|--------|
| `lifecycle_summary` | lifecycle | No | `alerts[]`, `history_by_alert{}`, `ttl_days?` | Counts: active, stale, archived, resolved, dismissed, case_opened |
| `calculate_impact` | impact | No | `rule_id`, `amount_cents?`, `severity?`, `avg_txn_cents?` | `impact_cents`, `impact_dollars`, `category`, `formula` |
| `rank_alerts` | impact | No | `alerts[]`, `severity_weight?`, `impact_weight?` | Sorted alerts array, highest priority first |
| `get_impact_summary` | impact | No | `alerts[]` | `total_impact_cents`, `count_with_impact`, `highest_impact_alert`, `impact_by_category` |
| `list_alerts` | alerts | Yes | `merchant_id`, `severity?`, `rule_id?`, `page?`, `limit?` | Paginated alert list with current status |
| `get_alert` | alerts | Yes | `merchant_id`, `alert_id` | Single alert with full history and current_status |

**Design note:** No `open_case` tool in Alert MCP. Case creation routes through Owl's action dispatcher (`POST /owl/action` with `action=case_create`), which orchestrates Fox case creation + AlertHistory writes in a single transaction.

### Owl Action Dispatcher (alert-related actions)

The Owl action dispatcher at `POST /owl/action` (JWT) and `POST /m/owl/action` (session) handles these alert-terminal actions:

| Action Code | Disposition | Effect |
|-------------|-------------|--------|
| `resolve` | `resolved` | Writes AlertHistory(status="resolved"). Terminal. |
| `dismiss` | `dismissed` | Requires reason. Writes AlertHistory(status="dismissed"). Terminal. |
| `case_create` | `case_opened` | Creates FoxCase, links alerts, writes AlertHistory. Terminal. |
| `follow_up` | `follow_up` | Creates evidence refs in Fox, writes AlertHistory. |

### Notification API

`NotificationService.send_chirp_alert(merchant_id, chirp_alert)` — internal, no REST endpoint. Checks: opt-in preference, severity threshold (HIGH/CRITICAL), quiet hours, daily cap. Delivers via Twilio SMS. Logs every attempt to `notification_log`.

## Data Model

All tables in the `app` schema of the `canary` database. The Alert domain owns 4 tables. Access pattern is APPEND-ONLY.

### `alerts`

Immutable after creation. Written by Chirp rule engine (via sub4_detect in the webhook pipeline).

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | PK |
| `merchant_id` | UUID | FK -> merchants.id |
| `rule_id` | VARCHAR | Detection rule ID (e.g. "C-001") |
| `alert_type` | VARCHAR | Rule category name |
| `severity` | VARCHAR | critical / high / medium / low |
| `source_table` | VARCHAR | Source data table name |
| `source_id` | VARCHAR | Source record ID |
| `employee_id` | UUID | FK -> employees.id (nullable) |
| `location_id` | UUID | FK -> locations.id (nullable) |
| `amount_cents` | INTEGER | Transaction amount in cents (nullable) |
| `impact_cents` | INTEGER | Calculated dollar impact (set once at creation) |
| `details` | TEXT | JSON string with rule-specific context |
| `created_at` | TIMESTAMP | Alert creation time |

### `alert_history`

APPEND-ONLY status log. Every state change = new row. Status derived from latest entry per alert_id.

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | PK |
| `alert_id` | UUID | FK -> alerts.id |
| `status` | VARCHAR | new / investigating / escalated / dismissed / case_opened / resolved / follow_up / archived |
| `changed_by` | VARCHAR | User ID or "system:ttl" for auto-archival |
| `notes` | TEXT | Free-text (required for dismiss, auto-generated for archival) |
| `created_at` | TIMESTAMP | Status change time |

### `notification_log`

Tracks every notification attempt, regardless of outcome. Used for daily rate limiting and audit.

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | PK |
| `merchant_id` | UUID | FK -> merchants.id |
| `alert_id` | UUID | FK -> alerts.id |
| `channel` | VARCHAR | email / sms / in_app / push |
| `status` | VARCHAR | sent / failed / suppressed |
| `created_at` | TIMESTAMP | Delivery attempt time |

### `notification_schedule`

Per-merchant, per-category routing rules. Falls back to `_default` category if no specific match.

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | PK |
| `merchant_id` | UUID | FK -> merchants.id |
| `category` | VARCHAR | Alert category or "_default" |
| `frequency` | VARCHAR | realtime / hourly / daily / weekly |
| `channels` | TEXT | JSON array of enabled channels |
| `severity_threshold` | VARCHAR | Minimum severity to notify |
| `impact_threshold_cents` | INTEGER | Minimum impact to notify |

### Key relationships

- `alerts.merchant_id` -> `merchants.id` (tenant isolation)
- `alerts.employee_id` -> `employees.id` (nullable, suspect linkage)
- `alerts.location_id` -> `locations.id` (nullable, where it happened)
- `alert_history.alert_id` -> `alerts.id` (status chain)
- `fox_case_alerts.alert_id` -> `alerts.id` (junction to Fox cases, owned by Fox domain)

## Workflows

### Risk Aggregation Hook (post-alert creation)

- After alert creation in `rule_engine._write_alerts()`, the risk aggregator is called to recalculate entity risk scores.
- Flow: Alert INSERT -> flush -> `update_employee_risk()` -> `EntityRiskScore` upsert + `Employee.risk_score` update.
- This ensures risk scores reflect newly created alerts before the transaction commits.
- Cross-ref: `chirp.md` risk_aggregator section.

### Alert Lifecycle: Creation to Terminal State

```
1. Webhook arrives -> sub4_detect calls ChirpRuleEngine.evaluate_transaction()
2. Rule matches -> calculate_impact(rule_id, amount_cents, severity)
   -> ImpactResult with impact_cents, category, formula
3. INSERT alerts row (immutable) + AlertHistory(status="new")
3a. Risk aggregation hook: update_employee_risk() recalculates EntityRiskScore + Employee.risk_score
4. NotificationRouter.route(alert) -> apply schedule, filter, deliver
5. Alert appears in feed (/api/alerts/, mobile Chirps panel, Owl chat)
6. Merchant acts via REST or Owl action dispatcher:
   - resolve   -> AlertHistory(status="resolved")   [TERMINAL]
   - dismiss   -> AlertHistory(status="dismissed")   [TERMINAL, reason required]
   - open-case -> FoxCase created + AlertHistory(status="case_opened") [TERMINAL]
   - follow_up -> FoxEvidence created + AlertHistory(status="follow_up")
7. Unactioned alerts auto-archive after TTL (14 days default)
```

### TTL Auto-Archival (Batch)

```
1. Load all alerts for merchant
2. Load AlertHistory grouped by alert_id
3. get_stale_alerts(alerts, history, ttl_days=14)
   -> Returns alerts that are NOT terminal AND older than TTL
4. build_archive_entries(stale_alerts)
   -> ArchiveEntry(alert_id, status="archived", changed_by="system:ttl",
      notes="Auto-archived: unactioned for 14+ days")
5. INSERT AlertHistory row for each entry
6. lifecycle_summary() for reporting
```

### Impact Scoring Calculation

Impact is calculated once at alert creation and stored immutably on the alert.

**Category formulas (rule prefix -> calculation):**

| Prefix | Category | Formula | Multiplier |
|--------|----------|---------|------------|
| C-1xx | Refund | `amount_cents` directly | 1.0x |
| C-2xx | Void | `amount_cents * 1.0` | 1.0x |
| C-3xx | Cash variance | `abs(amount_cents)` | 1.0x |
| C-4xx | No-sale | `avg_txn_cents` (default $25) | -- |
| C-5xx | Discount | `amount_cents * 1.5` | 1.5x |
| C-6xx | Time-based | `avg_txn_cents * 2.0` | 2.0x |
| C-7xx | Custom amount | `amount_cents * 1.2` | 1.2x |
| C-8xx | Pattern | Severity fallback | -- |

**Severity fallback** (when no amount available): critical=$500, high=$200, warning=$100, medium=$50, low=$10, info=$0.

### Owl Priority Ranking

```
1. get_active_alerts(alerts, history, ttl_days=14)
   -> Excludes terminal + stale alerts
2. age_decay_factor(created_at, ttl_days=14)
   -> Linear decay: 1.0 at creation, 0.5 at 7 days, 0.0 at 14 days
   -> Formula: factor = 1 - (age_days / ttl_days), clamped [0, 1]
3. rank_by_impact(alerts, severity_weight=0.6, impact_weight=0.4)
   -> Composite: (0.6 * severity_normalized) + (0.4 * impact_normalized)
   -> Severity normalized: critical=1.0, high/warning=0.75, medium=0.5, low=0.25, info=0.0
4. Top-ranked alert = "The One Thing" in Owl
5. alert_age_label(created_at) -> "just now", "5m ago", "3h ago", "2d ago"
```

### Notification Delivery Pipeline

```
1. Alert written by Chirp
2. NotificationRouter.route(alert):
   a. Load NotificationSchedule for (merchant_id, alert.category)
      -> Falls back to _default category
   b. Filter checks:
      - Severity >= threshold? (skip if below)
      - Impact >= impact_threshold_cents? (skip if below)
      - In quiet hours? (suppress SMS/push, allow in-app)
      - Under hourly cap (50) / daily cap (100)? (suppress if exceeded)
   c. Route by frequency:
      - realtime -> immediate delivery
      - hourly/daily/weekly -> batch into digest (digest_batch_id)
   d. Write NotificationLog (every attempt, regardless of outcome)
3. Channel delivery:
   - SMS: via Twilio (check_merchant_preferences for opt-in, phone, quiet hours)
   - Email: transactional (future: SendGrid/SES)
   - In-app: notification queue
   - Push: FCM/APNs (future)
4. Rate limiting via Valkey counters with TTL-based windows
```

### Key Constants

| Constant | Value | Used By |
|----------|-------|---------|
| `DEFAULT_TTL_DAYS` | 14 | Lifecycle staleness, archival |
| `ARCHIVE_ACTOR` | "system:ttl" | Auto-archival changed_by |
| `DEFAULT_AVG_TXN_CENTS` | 2500 ($25) | No-sale/off-clock impact fallback |
| `severity_weight` | 0.6 | Owl ranking composite |
| `impact_weight` | 0.4 | Owl ranking composite |
| `hourly_cap` | 50 | Notification rate limit |
| `daily_cap` | 100 | Notification rate limit |
