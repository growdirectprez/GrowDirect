# Alert

**Type:** App Service (Canary)
**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]], [[Brain/wiki/canary-detection|Canary Detection]]
**Architecture:** [[docs/sdds/canary/architecture|Canary Architecture SDD]]
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[docs/team/Architect|Architect]] · **Operator role:** [[docs/team/Engineer|Engineer]]

## Purpose

The Alert domain is the terminal consumer of Canary's detection pipeline. Chirp writes alert rows; the Alert domain owns everything after: lifecycle state tracking, dollar-impact scoring, notification delivery, and MCP tool access. Alerts are never forwarded to another domain -- they are resolved, dismissed, escalated to Fox cases, or auto-archived by TTL.

## Dependencies

| Dependency | Type | Required | Purpose |
|------------|------|----------|---------|
| PostgreSQL (`canary` DB, `app` schema) | Database | Yes | Alert, AlertHistory, NotificationLog, NotificationSchedule tables |
| Valkey (DB 0) | Cache | Yes | Session backend for JWT/session auth on REST routes |
| Chirp rule engine | Internal | Yes | Writes alert rows via `rule_engine._write_alerts()` |
| Fox case service | Internal | Optional | `open-case` route creates Fox cases |
| Owl action dispatcher | Internal | Optional | Routes resolve/dismiss/case_create actions through `POST /owl/action` |
| Twilio | External | Optional | SMS delivery (not yet wired in production dispatcher) |
| MerchantSettings | Internal | Yes | Notification preferences (opt-in, quiet hours, daily limit) |

## Data Flow & PII Map

### What enters

- **From Chirp:** Alert rows written by `rule_engine._write_alerts()` after rule matches. Contains `merchant_id`, `employee_id`, `location_id`, `amount_cents`, `rule_id`, `severity`, and `details` JSON.
- **From REST API:** Status change requests (`investigate`, `dismiss`, `escalate`, `open-case`) with `user_id` from JWT auth.
- **From Owl:** Action dispatcher routes (`resolve`, `dismiss`, `case_create`, `follow_up`) via `POST /owl/action`.

### What's stored

| Table | Field | PII Classification | Encryption | Notes |
|-------|-------|--------------------|------------|-------|
| `alerts` | `merchant_id` | internal | plaintext | FK to merchants -- tenant isolation key |
| `alerts` | `employee_id` | sensitive | **plaintext** | FK to employees -- identifies suspect employee |
| `alerts` | `location_id` | internal | plaintext | FK to locations |
| `alerts` | `amount_cents` | internal | plaintext | Transaction amount (financial data) |
| `alerts` | `impact_cents` | internal | plaintext | Calculated dollar impact |
| `alerts` | `details` | sensitive | **plaintext** | JSON with rule-specific context; may contain transaction details, employee names |
| `alerts` | `source_id` | internal | plaintext | Row ID in source transaction table |
| `alert_history` | `changed_by` | internal | plaintext | User ID or "system:ttl" |
| `alert_history` | `notes` | internal | plaintext | Free-text; may contain employee references in dismiss reasons |
| `notification_log` | `recipient` | sensitive | **plaintext** | Phone number or email address |
| `notification_log` | `message_preview` | sensitive | **plaintext** | First 255 chars of notification body; contains rule ID + severity |
| `notification_schedule` | `merchant_id` | internal | plaintext | Per-merchant routing rules |

### What exits

- **To REST API consumers:** Alert data including `employee_id`, `amount_cents`, `details` -- returned via `/api/alerts/*` routes (JWT-gated).
- **To MCP tool consumers:** Same alert data via `canary-alert` MCP tools (2 DB-read tools expose `employee_id`, `location_id`, `amount_cents`).
- **To Twilio (future):** SMS messages containing alert severity and rule description. Phone numbers read from `MerchantSettings.notif_phone`.
- **To Fox:** Alert ID linkage when case is created via `open-case` route.

## API Contract

### REST API (`alerts_wired.py` at `/api/alerts/*`)

All routes require JWT authentication. Role-gated actions require owner/manager/admin.

| Route | Method | Auth | Purpose |
|-------|--------|------|---------|
| `/` | GET | JWT | List alerts. Filters: `severity`, `rule_id`, `created_after`, `created_before`. Pagination: `page`, `limit` (default 20). Returns `{alerts, pagination}`. |
| `/<alert_id>` | GET | JWT | Single alert with full history array. |
| `/<alert_id>/investigate` | PUT | JWT + roles(owner/manager/admin) | Set status to "investigating". Rejects if already processed. |
| `/<alert_id>/dismiss` | PUT | JWT + roles(owner/manager/admin) | Dismiss with required `reason`. Writes AlertHistory(status="dismissed"). |
| `/<alert_id>/escalate` | POST | JWT + roles(owner/admin) | Escalate alert priority. |
| `/<alert_id>/open-case` | POST | JWT + roles(owner/operator/admin) | Create Fox case from alert. Writes AlertHistory(status="case_opened"). Returns `{case_id, case_number}`. |
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

`dispatch_alert_notification(db_session, merchant_id, alert_data)` -- internal, no REST endpoint. Called from `rule_engine._write_alerts()` after alert flush. Checks: per-rule notify toggle (GRO-254), severity threshold, quiet hours, daily cap. Currently delivers in-app only; email/SMS suppressed pending delivery provider wiring. Logs every attempt to `notification_log`.

`NotificationService.send_chirp_alert(merchant_id, chirp_alert)` -- legacy SMS path via Twilio. Checks: opt-in preference, severity threshold (HIGH/CRITICAL), quiet hours, daily cap.

## Data Model

All tables in the `app` schema of the `canary` database. The Alert domain owns 4 tables. Core access pattern is APPEND-ONLY.

### `alerts`

Immutable after creation. Written by Chirp rule engine (via `sub4_detect` in the webhook pipeline).

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `id` | VARCHAR(36) | No | PK (UUID) |
| `merchant_id` | VARCHAR(36) | No | FK -> merchants.id (tenant isolation) |
| `rule_id` | VARCHAR(20) | No | FK -> detection_rules.rule_id (e.g. "C-001") |
| `alert_type` | VARCHAR(50) | No | Rule category name |
| `severity` | VARCHAR(20) | No | critical / high / medium / low |
| `source_table` | VARCHAR(50) | No | Source data table name |
| `source_id` | VARCHAR(36) | No | Source record ID |
| `employee_id` | VARCHAR(36) | Yes | FK -> employees.id (suspect linkage) |
| `location_id` | VARCHAR(36) | Yes | FK -> locations.id |
| `amount_cents` | INTEGER | Yes | Transaction amount in cents |
| `impact_cents` | INTEGER | Yes | Calculated dollar impact (set once at creation) |
| `details` | TEXT | Yes | JSON string with rule-specific context |
| `created_at` | TIMESTAMP | No | Alert creation time (immutable) |
| `created_by` | VARCHAR(36) | Yes | "chirp" or user who manually triggered |

**Note:** No `updated_at` column. Alert rows are never updated.

Indexes: `merchant_id`, `(merchant_id, created_at)`, `(merchant_id, rule_id)`, `(merchant_id, employee_id)`, `(merchant_id, location_id)`, `(merchant_id, severity)`.

### `alert_history`

APPEND-ONLY status log. Every state change = new row. Status derived from latest entry per `alert_id`.

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `id` | VARCHAR(36) | No | PK (UUID) |
| `alert_id` | VARCHAR(36) | No | FK -> alerts.id |
| `status` | VARCHAR(50) | No | new / investigating / escalated / dismissed / case_opened / resolved / follow_up / archived |
| `changed_by` | VARCHAR(36) | Yes | FK -> users.id, or "system:ttl" for auto-archival |
| `notes` | TEXT | Yes | Free-text (required for dismiss, auto-generated for archival) |
| `created_at` | TIMESTAMP | No | Status change time (via AuditMixin) |

Indexes: `alert_id`, `(alert_id, status)`.

### `notification_log`

Tracks every notification attempt, regardless of outcome. Used for rate limiting and audit.

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `id` | VARCHAR(36) | No | PK (UUID) |
| `merchant_id` | VARCHAR(36) | No | FK -> merchants.id |
| `alert_id` | VARCHAR(36) | Yes | FK -> alerts.id (NULL for digest/summary) |
| `channel` | VARCHAR(10) | No | email / sms / in_app / push |
| `status` | VARCHAR(12) | No | pending / sent / failed / batched / suppressed |
| `frequency_mode` | VARCHAR(10) | No | realtime / hourly / daily / weekly |
| `severity` | VARCHAR(10) | Yes | Alert severity at time of send |
| `recipient` | VARCHAR(255) | Yes | Phone number, email address, or device token |
| `message_preview` | VARCHAR(255) | Yes | First 255 chars of notification body |
| `failure_reason` | VARCHAR(255) | Yes | Reason for failure/suppression |
| `digest_batch_id` | VARCHAR(36) | Yes | Groups notifications in same digest window |
| `created_at` | TIMESTAMP(tz) | No | Delivery attempt time |

Indexes: `(merchant_id, created_at)`, `(merchant_id, status)`, `digest_batch_id`.

### `notification_schedule`

Per-merchant, per-category routing rules. Falls back to `_default` category if no specific match.

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `id` | VARCHAR(36) | No | PK (UUID) |
| `merchant_id` | VARCHAR(36) | No | FK -> merchants.id |
| `alert_category` | VARCHAR(30) | No | Alert category or "_default" |
| `channel_email` | BOOLEAN | No | Email notifications enabled |
| `channel_sms` | BOOLEAN | No | SMS notifications enabled |
| `channel_in_app` | BOOLEAN | No | In-app notifications enabled |
| `channel_push` | BOOLEAN | No | Push notifications enabled |
| `freq_critical` | VARCHAR(10) | No | Frequency for critical alerts |
| `freq_high` | VARCHAR(10) | No | Frequency for high alerts |
| `freq_medium` | VARCHAR(10) | No | Frequency for medium alerts |
| `freq_low` | VARCHAR(10) | No | Frequency for low alerts |
| `freq_info` | VARCHAR(10) | No | Frequency for info alerts |
| `hourly_cap` | INTEGER | No | Max notifications per hour (default 50) |
| `daily_cap` | INTEGER | No | Max notifications per day (default 100) |
| `impact_threshold_cents` | INTEGER | No | Min impact to trigger notification (0 = no filter) |
| `is_active` | BOOLEAN | No | Schedule active flag |

Unique index: `(merchant_id, alert_category)`.

### Key Relationships

- `alerts.merchant_id` -> `merchants.id` (tenant isolation)
- `alerts.employee_id` -> `employees.id` (nullable, suspect linkage)
- `alerts.location_id` -> `locations.id` (nullable, where it happened)
- `alert_history.alert_id` -> `alerts.id` (status chain)
- `alert_history.changed_by` -> `users.id` (who changed it)
- `fox_case_alerts.alert_id` -> `alerts.id` (junction to Fox cases, owned by Fox domain)
- `notification_log.alert_id` -> `alerts.id` (notification audit trail)

## Workflows

### Status Machine

```
new -> investigating -> resolved [TERMINAL]
 |         |              dismissed [TERMINAL]
 |         |              case_opened [TERMINAL]
 |         +-> escalated -> resolved [TERMINAL]
 |                          case_opened [TERMINAL]
 +-> resolved [TERMINAL]
 +-> dismissed [TERMINAL]
 +-> archived [TERMINAL]  (system:ttl auto-archival after 14 days)
```

Four terminal states: `resolved`, `dismissed`, `case_opened`, `archived`. No alert purgatory.

**Core principle: APPEND-ONLY.** The `alerts` row is immutable after creation. All state changes are new `alert_history` rows. Status is derived by reading the latest history entry (no history = "new").

### Alert Lifecycle: Creation to Terminal State

```
1. Webhook arrives -> sub4_detect calls ChirpRuleEngine.evaluate_transaction()
2. Rule matches -> calculate_impact(rule_id, amount_cents, severity)
   -> ImpactResult with impact_cents, category, formula
3. INSERT alerts row (immutable) + AlertHistory(status="new")
3a. Risk aggregation hook: update_employee_risk() recalculates EntityRiskScore
4. dispatch_alert_notification(db_session, merchant_id, alert_data)
   -> checks per-rule notify toggle, severity threshold, quiet hours, daily limit
   -> currently: in-app only; email/SMS suppressed
5. Alert appears in feed (/api/alerts/, mobile Chirps panel, Owl chat)
6. Merchant acts via REST or Owl action dispatcher:
   - resolve   -> AlertHistory(status="resolved")   [TERMINAL]
   - dismiss   -> AlertHistory(status="dismissed")   [TERMINAL, reason required]
   - open-case -> FoxCase created + AlertHistory(status="case_opened") [TERMINAL]
   - follow_up -> FoxEvidence created + AlertHistory(status="follow_up")
7. Unactioned alerts eligible for auto-archive after TTL (14 days default)
```

### TTL Auto-Archival

Logic lives in `alert_lifecycle.py` as pure functions. **No scheduled job or cron exists to execute archival.** The functions `get_stale_alerts()` and `build_archive_entries()` produce `ArchiveEntry` dataclasses, but nothing calls them on a schedule to INSERT the resulting `AlertHistory` rows.

```
1. get_stale_alerts(alerts, history, ttl_days=14)
   -> Returns alerts that are NOT terminal AND older than TTL
2. build_archive_entries(stale_alerts)
   -> ArchiveEntry(alert_id, status="archived", changed_by="system:ttl",
      notes="Auto-archived: unactioned for 14+ days")
3. [MISSING] No cron/scheduler invokes this to write AlertHistory rows
```

### Impact Scoring Calculation

Impact is calculated once at alert creation and stored immutably on the alert.

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

### Notification Delivery Pipeline

```
1. Alert written by Chirp -> rule_engine._write_alerts() calls dispatch_alert_notification()
2. dispatch_alert_notification():
   a. Check MerchantRuleConfig.notify_enabled for this rule_id (GRO-254)
   b. Load MerchantSettings for merchant_id
   c. Filter checks:
      - Severity >= notif_severity_threshold?
      - In quiet hours? (suppresses all channels)
      - Under daily limit?
   d. Deliver:
      - in_app: logged as STATUS_SENT (actual in-app delivery mechanism TBD)
      - email: logged as STATUS_SUPPRESSED ("Email delivery pending provider")
      - sms: logged as STATUS_SUPPRESSED ("SMS delivery pending provider")
   e. Write NotificationLog row for every attempt
3. Legacy SMS path (NotificationService.send_chirp_alert):
   - Twilio-based, checks opt-in + severity + quiet hours + daily cap
   - Separate from dispatch_alert_notification flow
```

### Owl Priority Ranking

```
1. get_active_alerts(alerts, history, ttl_days=14)
   -> Excludes terminal + stale alerts
2. age_decay_factor(created_at, ttl_days=14)
   -> Linear decay: 1.0 at creation, 0.5 at 7 days, 0.0 at 14 days
3. rank_by_impact(alerts, severity_weight=0.6, impact_weight=0.4)
   -> Composite: (0.6 * severity_normalized) + (0.4 * impact_normalized)
4. Top-ranked alert = "The One Thing" in Owl
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

## Operations

### Startup Sequence

The Alert service runs inside the Canary Flask container (port 5001). No separate process.

1. Canary Flask app starts via `wsgi.py`
2. Blueprint `alerts_bp` registered at `/api/alerts` (REST API)
3. Blueprint `alert_mcp_bp` registered at `/alert` (MCP server)
4. Both blueprints share the same PostgreSQL session factory and Valkey connection
5. No migration or seed step specific to alerts -- tables created by Alembic

### Health Checks

- **MCP health:** `GET /alert/health` returns `{"service": "canary-alert", "healthy": true, "tools": 6}` via `_alert_health()` in `alert_mcp.py`
- **REST health:** No dedicated alert health endpoint. Covered by Canary-level `/ops/health`
- **Database dependency:** Both blueprints will 500 if PostgreSQL is unreachable. No circuit breaker.

### Failure Modes

| Failure | Impact | Behavior |
|---------|--------|----------|
| PostgreSQL down | All alert reads/writes fail | REST routes return 500. MCP tools return `{ok: false, error: ...}`. Alert creation in Chirp pipeline fails, blocking webhook processing. |
| Valkey down | Session auth fails | JWT auth still works (stateless). Session-based auth (browser) fails. |
| Twilio unavailable | SMS notifications fail | `_send_sms()` catches exception, logs error, returns `{success: false}`. Alert creation unaffected. |
| Alert creation fails mid-transaction | Webhook processing fails | Chirp pipeline rolls back. Transaction data is preserved but alert not created. Webhook will not retry (no retry mechanism in TSP). |
| N+1 query in summary endpoint | Performance degradation | `get_summary()` queries `_latest_status()` per alert in a loop. Degrades with alert volume. |

### Monitoring

| Metric | What to alert on | Normal range |
|--------|------------------|--------------|
| Alert creation rate | >1000/hour suggests webhook flood or rule misconfiguration | 0-100/hour per merchant |
| Notification suppression rate | >90% suppressed suggests misconfigured preferences | 20-50% suppressed |
| Summary endpoint latency | >5s indicates N+1 problem at scale | <1s |
| MCP tool errors | Any `{ok: false}` response | 0 errors |

### Configuration

| Env Var | Purpose | Default |
|---------|---------|---------|
| `TWILIO_ACCOUNT_SID` | Twilio SMS credentials | None (SMS disabled) |
| `TWILIO_AUTH_TOKEN` | Twilio SMS credentials | None (SMS disabled) |
| `TWILIO_FROM_NUMBER` | Twilio sender number | None (SMS disabled) |
| `CANARY_APP_URL` | Base URL for alert links in SMS | `https://app.canarylp.com` |
| `CANARY_MCP_API_KEY` | API key for agent-to-agent MCP calls | None |
| `CANARY_DEV_JWT_SECRET` | Dev-mode JWT secret | None (blocks auth if unset) |

## Deployment

### Docker Service

The Alert service is not a separate container. It runs inside the Canary Flask container defined in `Canary/devops/docker-compose.yml`. The Canary image includes all alert code.

```
canary-web:5001
  ├── /api/alerts/*   (REST API via alerts_bp)
  └── /alert/*        (MCP server via alert_mcp_bp)
```

### AWS Target

- **Compute:** ECS/Fargate (single Canary task definition includes alert service)
- **Database:** RDS PostgreSQL 17 (`canary` database, `app` schema)
- **Secrets:** AWS Secrets Manager for Twilio credentials, JWT secret
- **Cache:** ElastiCache (Valkey-compatible) for sessions

### CI/CD

- Alert code ships with every Canary deployment
- No independent deployment lifecycle
- Alembic migrations run as part of Canary deploy pipeline

## Code Review Findings

### P0 -- Blocks Production

**P0-1: `notification_log.recipient` stores phone numbers and emails in plaintext**

The `NotificationLog.recipient` column (VARCHAR 255) stores raw phone numbers and email addresses with no encryption. The `NotificationService.send_chirp_alert()` path reads `notif_phone` from `MerchantSettings` and passes it directly to Twilio and the log. The notification dispatcher also stores `recipient` via `_log_notification()`.

Recommended fix: Encrypt `recipient` field using the Canary `crypto.py` AES-256-GCM pattern (same as OAuth tokens). Decrypt only at delivery time.

**P0-2: `notification_log.message_preview` may contain PII**

The `message_preview` field stores the first 255 chars of the notification body, which is constructed from `rule_id`, `severity`, and `alert_data.details`. The `details` JSON can contain employee names, transaction descriptions, and other sensitive context.

Recommended fix: Strip or redact PII from message previews before storage. Store only rule_id + severity + impact, not free-text details.

**P0-3: `alerts.details` stores rule-specific context as plaintext JSON**

The `details` TEXT column contains JSON with rule-specific context that may include employee names, transaction amounts, customer-facing descriptions, and other data that qualifies as PII-adjacent.

Recommended fix: Encrypt the `details` field at rest using field-level AES-256-GCM, or redact PII fields from the JSON before storage.

**P0-4: Twilio credentials loaded from environment variables at call time**

`NotificationService._send_sms()` calls `os.getenv('TWILIO_ACCOUNT_SID')` and `os.getenv('TWILIO_AUTH_TOKEN')` on every SMS send. In production, these must be in AWS Secrets Manager, not `.env` files.

Recommended fix: Load Twilio credentials from AWS Secrets Manager at startup via `boto3`. Cache in memory with TTL for rotation support.

### P1 -- Before GA

**P1-1: No TTL archival scheduler exists**

The `alert_lifecycle.py` module provides pure functions for identifying stale alerts and building archive entries, but nothing invokes them on a schedule. Stale alerts accumulate indefinitely. The `lifecycle_summary` MCP tool can report stale counts, but the actual archival (writing `AlertHistory` rows) never happens.

Recommended fix: Implement a scheduled task (Valkey-based task queue or cron job) that runs `get_stale_alerts()` + `build_archive_entries()` and writes the resulting `AlertHistory` rows. Run daily per merchant.

**P1-2: N+1 query in summary endpoint and list endpoint**

`get_summary()` in `alerts_wired.py` loads all alert IDs for a merchant, then calls `_latest_status()` per alert in a Python loop. Each call is a separate DB query. The `list_alerts` route has the same pattern. With 1000+ alerts, this degrades severely.

Recommended fix: Use a single subquery or lateral join to get the latest status per alert. Alternatively, materialize current status as a denormalized column on `alerts` (updated via trigger or application code on AlertHistory INSERT).

**P1-3: No audit logging for alert status changes beyond AlertHistory**

AlertHistory tracks status changes but there is no structured audit log that captures the full context: who changed it, from what IP, via which endpoint (REST vs MCP vs Owl), with what role. The `changed_by` field is a user ID string with no FK enforcement in all code paths (the model has `ForeignKey("users.id")` but the Owl dispatcher and system:ttl bypass this).

Recommended fix: Add a dedicated audit event for status transitions that captures: actor, actor_type (user/system/agent), source_endpoint, previous_status, new_status, timestamp, IP address (hashed).

**P1-4: No rate limiting on REST alert endpoints**

The `/api/alerts/` endpoints have no rate limiting. An attacker with a valid JWT could enumerate all alerts or flood status change endpoints.

Recommended fix: Add Flask-Limiter to alert REST routes. Suggested limits: 60 req/min for reads, 10 req/min for writes.

**P1-5: No data retention policy for alerts or notification logs**

Alerts and notification logs accumulate indefinitely. No cleanup job exists. For merchants processing high transaction volumes, the `alerts` and `notification_log` tables will grow without bound.

Recommended fix: Define retention policy (suggested: alerts 24 months, notification_log 12 months). Implement a scheduled purge job that archives to cold storage before deletion.

**P1-6: Email and SMS delivery channels are stubbed**

The `dispatch_alert_notification()` function logs email and SMS attempts as `STATUS_SUPPRESSED` with "delivery pending provider". The legacy `NotificationService` has Twilio wiring but is a separate code path. Two notification systems exist in parallel.

Recommended fix: Consolidate to a single notification dispatch path. Wire email (SendGrid/SES) and SMS (Twilio) into `dispatch_alert_notification()`. Remove or deprecate the legacy `NotificationService` class.

**P1-7: Quiet hours check uses UTC, not merchant timezone**

`_in_quiet_hours()` in `notification_dispatcher.py` compares against UTC time (`datetime.now(timezone.utc).strftime("%H:%M")`), but quiet hours are presumably configured in the merchant's local timezone. This means quiet hours are applied incorrectly for non-UTC merchants.

The legacy `NotificationService._is_quiet_hours()` correctly uses the merchant's timezone via pytz. The newer dispatcher does not.

Recommended fix: Resolve merchant timezone from `MerchantSettings.timezone` and convert current time before checking quiet hours in `_in_quiet_hours()`.

### P2 -- Post-Launch

**P2-1: `alert_history.changed_by` FK constraint may be violated by system actors**

The model declares `ForeignKey("users.id")` on `changed_by`, but system actors like `"system:ttl"` and `"chirp"` are not valid user IDs. The FK is not enforced at the DB level in practice (string comparison), but if constraints are tightened, these inserts will fail.

Recommended fix: Either use a well-known system user UUID for system actors, or change `changed_by` to not have a FK constraint and add a separate `actor_type` column.

**P2-2: `dismiss` route does not check for terminal status**

The `dismiss_alert()` route does not verify that the alert is not already in a terminal state. A dismissed alert could be dismissed again, creating duplicate history entries. The `investigate` route checks for this but `dismiss` and `escalate` do not.

Recommended fix: Add terminal state check to `dismiss_alert()` and `escalate_alert()` routes, consistent with `investigate_alert()`.

**P2-3: `open-case` route creates case and history in separate commits**

The `open_case()` route calls `FoxCaseService.create_case()` and then creates an `AlertHistory` row with a separate `get_session().commit()`. If the history write fails after case creation, the alert status won't reflect the case. These should be in a single transaction.

Recommended fix: Ensure both operations share the same session and commit atomically.

**P2-4: MCP tools expose `employee_id` without access control beyond merchant scoping**

The `list_alerts` and `get_alert` MCP tools return `employee_id` in their responses. Any agent or tool consumer with a valid `merchant_id` context can see which employees are associated with alerts. There is no additional RBAC beyond merchant-level scoping.

Recommended fix: Consider role-based field filtering for sensitive fields like `employee_id` in MCP tool responses. At minimum, document the access level required.

**P2-5: Two parallel notification dispatch systems**

`notification_service.py` (class-based, Twilio-wired, legacy) and `notification_dispatcher.py` (function-based, per-rule toggles, GRO-254) exist side by side. The dispatcher is called from `rule_engine._write_alerts()`, while the service is available but may not be called in the current flow.

Recommended fix: Consolidate into the dispatcher pattern. Migrate Twilio wiring from the legacy service into the dispatcher.

## Production Readiness Checklist

- [ ] PII encrypted at rest -- `notification_log.recipient` and `message_preview` plaintext (P0-1, P0-2)
- [ ] `alerts.details` encrypted or PII-redacted (P0-3)
- [ ] Secrets in AWS Secrets Manager (not .env) -- Twilio credentials in env vars (P0-4)
- [ ] Health check endpoint responds -- MCP health at `/alert/health` exists; REST relies on `/ops/health`
- [ ] Audit logging for sensitive operations -- AlertHistory exists but lacks actor context (P1-3)
- [ ] Data retention policy implemented -- no retention or purge for alerts or notification_log (P1-5)
- [ ] Rate limiting on public endpoints -- no rate limiting on REST routes (P1-4)
- [ ] Error responses don't leak internals -- generic error handler in `alerts_wired.py` catches exceptions, logs details, returns generic 500
- [ ] TTL archival scheduled -- pure logic exists, no scheduler (P1-1)
- [ ] N+1 queries resolved -- summary and list endpoints have per-alert status queries (P1-2)
- [ ] Notification channels operational -- email/SMS stubbed (P1-6)
- [ ] Quiet hours timezone-aware -- dispatcher uses UTC instead of merchant timezone (P1-7)
