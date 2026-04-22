# Chirp Detection Engine

**Type:** App Service (Canary)
**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]], [[Brain/wiki/canary-detection|Canary Detection]]
**Architecture:** [[docs/sdds/canary/architecture|Canary Architecture SDD]]
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[Canary/docs/profiles/ops/Tom|Tom]] + [[Canary/docs/profiles/ops/Research|Research]] · **Operator role:** [[Canary/docs/profiles/ops/Jeremy|Jeremy]]
**Linear:** GRO-85, GRO-128, GRO-132, GRO-174, GRO-247, GRO-278, GRO-279, GRO-289

## Purpose

Chirp is Canary's stateless detection rule engine. It evaluates Square merchant transactions, cash drawer shifts, gift card activities, loyalty events, disputes, and invoices against a catalog of 37 detection rules across 10 categories. When a rule fires, Chirp produces an alert with a contextual risk score (0-100), writes it to `canary_app`, and optionally auto-creates a Fox investigation case for 6 critical-severity rules. Chirp never mutates source transaction data.

## Dependencies

| Dependency | Type | Required | Purpose |
|------------|------|----------|---------|
| PostgreSQL (`canary`) | Database | Yes | `app` schema (alerts, rule config, employees), `sales` schema (transactions, shifts, gift cards, loyalty, disputes, invoices), `metrics` schema (entity risk scores, period metrics) |
| Valkey (DB 0) | Cache | No (degrades gracefully) | Threshold cache (`chirp:thresholds:*`, `chirp:active_rules:*`, 300s TTL) |
| Webhook Pipeline (TSP Sub4) | Internal caller | Yes | Triggers real-time evaluation on incoming Square webhooks |
| Fox Case Service | Internal callee | No (best-effort) | Auto-creates investigation cases for 6 critical rules |
| Risk Aggregator | Internal callee | No (best-effort) | Recalculates employee risk scores after alert batch |
| Alert Config Service | Internal module | Yes | Sensitivity presets, templates, threshold validation |
| JWT Auth Middleware | Internal module | Yes | Protects REST API endpoints |

## Data Flow & PII Map

### What Enters

| Source | Data | Format |
|--------|------|--------|
| TSP Sub4 (`sub4_detect`) | Parsed webhook payload | Dict: `amount_cents`, `transaction_type`, `transaction_date`, `employee_id`, `location_id`, `card_fingerprint`, `delay_action`, `approved_amount_cents`, `entry_method`, `external_id`, `merchant_id` |
| `canary_sales` schema | Transaction, CashDrawerShift, GiftCardActivity, LoyaltyEvent, Dispute, Invoice ORM objects | SQLAlchemy model instances loaded by rule engine |
| ThresholdManager | Per-merchant rule thresholds | Dict keyed by rule_id from Valkey/DB/catalog defaults |

### What's Stored (Chirp-Owned Tables)

All tables in `canary_app` schema.

| Table | Column | PII Classification | Encryption | Notes |
|-------|--------|-------------------|------------|-------|
| `detection_rules` | `rule_id`, `rule_name`, `description`, `category`, `severity`, `default_threshold` | public | None | Global catalog, 37 frozen rules, not tenant-scoped |
| `merchant_rule_config` | `merchant_id` | internal | None (plaintext UUID) | FK to merchants table |
| `merchant_rule_config` | `rule_id`, `is_enabled`, `custom_threshold` | internal | None | JSON threshold overrides |

### What's Written (Cross-Domain)

Chirp writes to tables owned by the Alert domain:

| Table | Column | PII Classification | Encryption | Notes |
|-------|--------|-------------------|------------|-------|
| `alerts` | `employee_id` | internal | None (plaintext UUID) | Resolved from Square ID to app UUID before INSERT |
| `alerts` | `location_id` | internal | None (plaintext UUID) | Resolved from Square ID to app UUID before INSERT |
| `alerts` | `details` (JSON) | **sensitive** | **None (plaintext)** | Contains `employee_id`, `card_fingerprint` (truncated to 8 chars), `original_employee_id`, `refund_employee_id`, transaction amounts, break times. **P0: PII in plaintext JSON.** |
| `alerts` | `amount_cents` | internal | None | Transaction dollar amounts |
| `alert_history` | `status`, `changed_by` | internal | None | Audit trail for alert status |

### What's Read (Cross-Domain)

| Schema | Table | Fields Accessed | PII Level | Purpose |
|--------|-------|----------------|-----------|---------|
| `sales` | `Transaction` | `id`, `external_id`, `merchant_id`, `employee_id`, `location_id`, `amount_cents`, `transaction_type`, `transaction_date`, `card_fingerprint`, `entry_method`, `delay_action`, `approved_amount_cents`, `order_id` | internal (employee_id, location_id), **sensitive** (card_fingerprint) | Rule evaluation |
| `sales` | `RefundLink` | `original_external_id`, `refund_external_id`, `refund_amount_cents` | internal | C-001, C-502 refund correlation |
| `sales` | `TransactionTender` | `transaction_id`, `payment_id` | internal | C-006 split-tender, C-001 fallback lookup |
| `sales` | `TransactionLineItem` | `gross_sales_cents`, `total_discount_cents`, `is_voided`, `item_name` | internal | C-201/C-202/C-203 order rules |
| `sales` | `CashDrawerShift` | `id`, `employee_id`, `location_id`, `opened_at`, `cash_variance_cents` | internal | C-101 through C-104 |
| `sales` | `CashDrawerEvent` | `shift_id`, `event_type`, `amount_cents` | internal | C-101 no-sale count, C-103 paid-out total |
| `sales` | `EmployeeTimecard` | `employee_id`, `start_at`, `end_at`, `breaks` (JSON), `location_id` | internal | C-301/C-302/C-303 timecard cross-reference |
| `sales` | `GiftCardActivity` | `gift_card_id`, `activity_type`, `amount_cents`, `occurred_at` | internal | C-601/C-602 gift card rules |
| `sales` | `LoyaltyEvent` | `loyalty_account_id`, `event_type`, `points`, `occurred_at`, `location_id`, `employee_id` | internal | C-801 through C-804 |
| `sales` | `LoyaltyAccount` | `enrolled_by_employee_id`, `enrolled_at` | internal | C-804 enrollment fraud |
| `sales` | `Dispute` | `state`, `reason`, `amount_cents`, `payment_id`, `location_id`, `reported_at` | internal | C-D01 through C-D03 |
| `sales` | `Invoice` | `invoice_status`, `next_payment_amount_cents` | internal | C-I01 through C-I03 |
| `app` | `Employee` | `id`, `square_employee_id`, `risk_score` | internal | Square ID resolution, risk score update |
| `app` | `Location` | `id`, `square_location_id` | internal | Square ID resolution |
| `app` | `Alert`, `AlertHistory` | alert rows + latest status | internal | Risk Aggregator reads alerts to compute entity scores |
| `metrics` | `PeriodMetrics` | `sra_pct_sales`, `sra_total_cents`, `gross_sales_cents` | internal | C-901 SRA threshold breach |
| `metrics` | `EntityRiskScore`, `RiskScoreHistory` | entity risk score persistence | internal | Risk Aggregator writes |

### What Exits

| Destination | Data | Format |
|-------------|------|--------|
| Alert table (`canary_app`) | Alert + AlertHistory rows | ORM INSERT |
| Fox Case Service | Case creation request for 6 critical rules | Internal function call (best-effort) |
| Risk Aggregator | Employee risk score recalculation trigger | Internal function call (best-effort) |
| REST API responses | Rule catalog, thresholds, config summaries | JSON (no raw PII — rule metadata only) |
| MCP tool responses | Rule catalog, stateless evaluation results | JSON (alert dicts may contain employee_id, amounts) |
| Logs | Alert fire events, rule evaluation results | Structured logging (`merchant_id`, rule counts, `employee_id` in C-005) |

## Rule Catalog (37 Rules, 10 Categories)

### Evaluation Tiers

| Tier | Engine | DB Access | Rule Count |
|------|--------|-----------|------------|
| 1 (Stateless) | `stateless_engine.py` | None (pure payload) | 10 rules (C-004, C-007, C-009, C-010, C-011, C-D01, C-D02, C-I01, C-I02, C-I03) |
| 2 (Lightweight) | `rule_engine.py` | Valkey counters / windowed DB queries | 10 rules (C-002, C-003, C-005, C-006, C-008, C-501, C-502, C-601, C-801, C-803, C-804, C-D03) |
| 3 (Full DB) | `rule_engine.py` | SQLAlchemy queries against `canary_sales` | 17 rules (cross-reference checks, batch-only) |

### Categories

| Category | IDs | Count |
|----------|-----|-------|
| payment | C-001 through C-011 | 11 |
| cash_drawer | C-101 through C-104 | 4 |
| order | C-201 through C-204 | 4 |
| timecard | C-301 through C-303 | 3 |
| void | C-501, C-502 | 2 |
| gift_card | C-601, C-602 | 2 |
| loyalty | C-801 through C-804 | 4 |
| composite | C-901 | 1 |
| dispute | C-D01 through C-D03 | 3 |
| invoice | C-I01 through C-I03 | 3 |

### Auto-Case Creation Rules

Six rules in `_AUTO_CASE_RULES` automatically create Fox investigation cases:
C-009 (SQUARE_DELAY_HOLD), C-104 (AFTER_HOURS_DRAWER), C-204 (UNTENDERED_ORDER), C-301 (OFF_CLOCK_TRANSACTION), C-502 (POST_VOID_ALERT), C-602 (GIFT_CARD_DRAIN).

## API Contract

### REST Endpoints (`chirp_wired.py` at `/api/chirp/*`)

All endpoints require JWT authentication and `admin` or `owner` role.

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/chirp/rules` | GET | List all rules (optional `?category=` filter) |
| `/api/chirp/rules/<rule_id>` | GET | Rule detail with merchant thresholds vs defaults |
| `/api/chirp/rules/<rule_id>/thresholds` | PUT | Set merchant-specific thresholds |
| `/api/chirp/rules/<rule_id>/thresholds` | DELETE | Reset rule to catalog defaults |
| `/api/chirp/config` | GET | All active rules for merchant with effective thresholds |
| `/api/chirp/sweep` | POST | Trigger batch evaluation (admin only). Body: `{"since_minutes": 60}` |
| `/api/chirp/categories` | GET | List all rule categories |
| `/api/chirp/sensitivity` | GET | List sensitivity presets with multipliers |
| `/api/chirp/sensitivity/preview` | POST | Preview adjusted thresholds for a rule at a sensitivity level |
| `/api/chirp/sensitivity/estimate` | POST | Estimate closest sensitivity level for given thresholds |
| `/api/chirp/templates` | GET | List available configuration templates |
| `/api/chirp/templates/preview` | POST | Preview template output across all rules |
| `/api/chirp/templates/apply` | POST | Apply template to merchant (writes `MerchantRuleConfig` rows) |
| `/api/chirp/validate` | POST | Validate proposed thresholds before saving |
| `/api/chirp/summary` | GET | Summary of merchant config vs defaults |

### MCP Tools (`canary-chirp` server, 10 tools)

MCP blueprint at `/chirp/*` via `chirp_mcp.py`. 9 pure (no DB) + 1 DB-read.

| Tool Name | Category | DB? | PII Access | Purpose |
|-----------|----------|-----|------------|---------|
| `get_rules` | rules | No | None | List rules, optional category/tier filter |
| `get_rule` | rules | No | None | Look up single rule by ID |
| `evaluate_stateless` | evaluation | No | **Yes** (parsed payload contains employee_id, amounts) | Run Tier 1 rules against parsed webhook payload |
| `apply_sensitivity` | configuration | No | None | Compute adjusted thresholds at a sensitivity level |
| `get_templates` | configuration | No | None | List config templates |
| `apply_template` | configuration | No | None | Apply template, return full rule config |
| `validate_thresholds` | configuration | No | None | Validate proposed thresholds |
| `get_config_summary` | configuration | No | None | Summarize merchant config vs catalog defaults |
| `estimate_sensitivity` | configuration | No | None | Classify current thresholds to closest sensitivity level |
| `get_merchant_thresholds` | configuration | Yes | None (threshold values only) | Get merchant thresholds (Valkey cache -> DB -> defaults) |

### Sensitivity Presets

| Preset | Effect |
|--------|--------|
| `strict` | Lower thresholds, more alerts (aggressive detection) |
| `default` | Catalog defaults (balanced) |
| `relaxed` | Higher thresholds, fewer alerts |
| `minimal` | Highest thresholds, lowest false positive rate |

### Configuration Templates

Industry-specific threshold profiles: `retail_standard`, `food_service`, `high_value`, `high_volume`, `new_merchant`. Each template adjusts thresholds and enable/disable flags across all 37 rules.

## Code Entry Points

| File | Role |
|------|------|
| `canary/services/chirp/rule_definitions.py` | Frozen dataclass rule catalog (37 `ChirpRuleDefinition` instances) |
| `canary/services/chirp/stateless_engine.py` | Tier 1 pure-function evaluation (10 rules, no ORM) |
| `canary/services/chirp/rule_engine.py` | `ChirpRuleEngine` class — all tiers, requires SQLAlchemy session |
| `canary/services/chirp/threshold_manager.py` | Per-merchant threshold CRUD with 3-layer Valkey cache |
| `canary/services/chirp/risk_aggregator.py` | Entity risk score aggregation — employee and card profiles |
| `canary/services/chirp/tools.py` | 10 MCP tool definitions for `canary-chirp` server |
| `canary/services/alert_config.py` | Sensitivity presets, templates, validation |
| `canary/blueprints/chirp_wired.py` | REST API at `/api/chirp/*` (JWT + admin/owner) |
| `canary/blueprints/chirp_mcp.py` | MCP blueprint at `/chirp/*` (manifest, tools, health) |

## Operations

### Startup Sequence

Chirp has no independent startup — it runs inside the Canary Flask process on port 5001. The rule catalog (`RULE_CATALOG`, `RULE_MAP`) is built at module import time from frozen dataclass instances. No database seeding is required for the catalog to function; `seed_rules.py` exists for populating the `detection_rules` table.

The ThresholdManager is instantiated per-request with a DB session and optional Valkey client. The Valkey client is currently hardcoded to `None` in `chirp_wired.py` (Sprint 4 TODO).

### Health Check

The MCP blueprint exposes a health endpoint via `_chirp_health()` returning `{"service": "canary-chirp", "healthy": True, "tools": 10}`. This is a shallow check — it confirms the MCP registry is loaded but does not verify DB connectivity or Valkey availability.

### Failure Modes

| Failure | Impact | Behavior |
|---------|--------|----------|
| PostgreSQL down | No rule evaluation for Tier 2/3 rules | `_load_merchant_thresholds()` uses SAVEPOINT (`begin_nested()`) and falls back to catalog defaults. Tier 1 stateless rules continue to fire. |
| Valkey down | Threshold cache misses on every request | ThresholdManager catches all Valkey exceptions and falls through to DB/defaults. Performance degrades but correctness maintained. |
| Single rule checker throws | One rule fails, others continue | Each `_check_*_rules()` method has per-rule try/except. Failures logged, not propagated. |
| Alert write fails | Alert lost for that transaction | `_write_alerts()` catches per-alert write failures and continues. Batch flush failure triggers rollback. |
| Fox case creation fails | No investigation case created | `_auto_create_cases()` is best-effort. Failures logged as warnings, never block the alert pipeline. |
| Risk score update fails | Employee risk score stale | `schedule_risk_update()` catches per-employee failures, rolls back the failed metrics write, and logs. Alert persistence is already committed. |
| Threshold DB query fails | Falls back to catalog defaults | 3-layer resolution ensures detection always runs with at least default thresholds. |

### Monitoring

| Metric | Source | Alert Threshold |
|--------|--------|----------------|
| Alerts generated per merchant per hour | `_write_alerts()` log lines | Spike > 3x baseline = possible false positive storm |
| Rule evaluation errors | `logger.error` in `_check_*_rules()` | Any sustained errors = rule implementation bug |
| Threshold cache hit rate | Valkey cache hits vs DB lookups | < 50% hit rate = Valkey issue or excessive invalidation |
| Batch sweep duration | `evaluate_batch()` timing | > 60s for < 1000 transactions = query performance issue |
| Risk update failures | `schedule_risk_update()` error logs | Any = metrics schema issue |

### Configuration

| Config | Source | Default | Notes |
|--------|--------|---------|-------|
| Rule catalog | `rule_definitions.py` (code) | 37 rules, frozen | Change requires code deploy |
| Threshold defaults | `ChirpRuleDefinition.default_thresholds` (code) | Per-rule | Change requires code deploy |
| Merchant overrides | `merchant_rule_config` table | Catalog defaults | Runtime-configurable via REST API |
| Threshold cache TTL | Hardcoded in `ThresholdManager` | 300 seconds | No env var |
| Auto-case rules | `_AUTO_CASE_RULES` frozenset (code) | 6 rules | Change requires code deploy |
| Valkey client | `chirp_wired.py` | `None` (disabled) | Sprint 4 TODO |
| Batch sweep window | REST API body param | 60 minutes | Per-request |

## Workflows

### Real-Time Detection (Webhook-Triggered)

```
1. Square webhook arrives at webhooks_tsp.py
2. TSP pipeline parses payload (sub2_parse)
3. sub4_detect triggers Chirp evaluation:
   a. stateless_engine.evaluate_stateless(parsed, thresholds)
      - Runs 10 Tier 1 rules (no DB, pure function)
      - Each checker returns 0 or 1 alert dicts
   b. ChirpRuleEngine.evaluate_readonly(txn, merchant_id)
      - _load_merchant_thresholds() via ThresholdManager (3-layer lookup)
      - Runs category-specific checkers:
        _check_payment_rules (C-001..C-008)
        _check_void_rules (C-501..C-502)
        _check_timecard_rules (C-301..C-303)
        _check_order_rules (C-201..C-203, if order_id present)
4. write_alerts_to_session() resolves Square IDs to UUIDs, inserts Alert + AlertHistory
5. schedule_risk_update() recalculates employee risk scores (synchronous, post-commit)
6. _auto_create_cases() creates Fox cases for 6 critical rules (best-effort)
```

### Risk Scoring (`compute_risk_score`)

Contextual 0-100 score from three factors:
- **Severity base:** critical=90, high=70, medium=45, low=20, info=10
- **Amount boost:** +5 for >$100, +10 for >$500, +15 for >$1000
- **Rule-specific override:** if `details["score"]` set, blended 60% weight with 40% base
- Result clamped to [0, 100]

### Batch Sweep (Hourly)

```
1. POST /api/chirp/sweep triggers chirp_wired.trigger_sweep(since_minutes=60)
2. ChirpRuleEngine.evaluate_batch(merchant_id, since_minutes)
3. Queries all transactions in time window from canary_sales
4. evaluate_transaction() on each transaction
5. _check_untendered_orders() for C-204 (batch-only rule)
6. _check_sra_rules() for C-901 (period-level composite)
7. Writes all accumulated alerts
```

### Threshold Configuration Flow

```
1. Merchant selects sensitivity preset (strict/default/relaxed/minimal)
   OR applies industry template (retail_standard, food_service, etc.)
   OR sets per-rule custom thresholds
2. Validation: validate_thresholds() checks field names, value ranges, warns on extremes
3. Write: ThresholdManager.set_merchant_threshold() upserts MerchantRuleConfig row
4. Cache invalidation: Valkey key cleared, next evaluation loads fresh threshold
```

## Risk Aggregator Service (GRO-247)

Entity-level risk score aggregation. Converts per-alert Chirp scores (0-100 int) into a normalized entity risk score (0.0-1.0 float) using recency-weighted averaging.

### Recency Weight Bands

| Age | Weight |
|-----|--------|
| Within 24h | 3.0x |
| 1-7 days | 2.0x |
| 7-30 days | 1.0x |
| Over 30 days | 0.5x |

### Score Categories

| Score Range | Category |
|-------------|----------|
| < 0.3 | low |
| 0.3 - 0.6 | medium |
| 0.6 - 0.8 | high |
| >= 0.8 | critical |

### Pipeline

```
1. Query Alert rows for entity (employee_id or card_fingerprint)
   - Excludes dismissed/false_positive via AlertHistory subquery
2. Per-alert: _alert_score() -> compute_risk_score(severity, amount_cents, details)
3. Per-alert: _recency_weight(now - created_at) -> weight band
4. aggregate_entity_risk(): weighted_sum / (count * max_weight) -> clamped [0.0, 1.0]
5. Persist: Employee.risk_score (app), EntityRiskScore upsert (metrics), RiskScoreHistory append (metrics)
```

### Constraints

- Card risk scoring (`update_card_risk`) is gated — returns 0.0 until `Alert.card_fingerprint` column is added (GRO-263).
- All operations run within a single SQLAlchemy session (caller must commit/rollback).

## Deployment

### Docker

Chirp runs inside the Canary Flask container — no separate service. It is loaded as two Flask blueprints registered at startup:
- `chirp_bp` at `/api/chirp/*` (REST)
- `chirp_mcp_bp` at `/chirp/*` (MCP)

No dedicated Docker service, port, or health check beyond the MCP health endpoint.

### AWS Target

| Component | AWS Service | Notes |
|-----------|-------------|-------|
| Canary Flask (includes Chirp) | ECS/Fargate | Single task definition for all Canary services |
| PostgreSQL | RDS (Aurora PostgreSQL 17) | `canary` database with `app`, `sales`, `metrics` schemas |
| Valkey | ElastiCache (Valkey mode) | DB 0, threshold cache |
| Secrets | AWS Secrets Manager | DB credentials, JWT signing key |

### CI/CD Requirements

- Rule catalog changes (`rule_definitions.py`) require code deploy — no hot-reload
- Threshold overrides are runtime-configurable via REST API
- New rule categories require: code + migration (if new tables) + deploy

## Code Review Findings

### P0 — Blocks Production

**P0-CHIRP-01: PII in plaintext alert details JSON**
Alert `details` column stores employee IDs, card fingerprints (truncated), transaction times, and break schedules as plaintext JSON. The `details` field is a Text column with no encryption. Employee IDs appear in at least 15 rule checkers. Card fingerprint appears truncated to 8 chars in C-005 but full fingerprint is read from the Transaction table without redaction logging.
- **Recommended fix:** Encrypt the `details` JSON column using the existing `crypto.py` AES-256-GCM pattern. Redact `card_fingerprint` to last-4 in alert details. Add field-level encryption for `employee_id` in alerts.
- **Linear:** Needs GRO issue

**P0-CHIRP-02: Employee IDs logged in structured logs**
`stateless_engine.py` logs `merchant_id` and fired rule IDs (acceptable), but `rule_engine.py` logs `employee_id` directly in C-005 check (`txn.card_fingerprint[:12]` logged), C-001 debug lines, and `evaluate_readonly()`. Production logs should not contain employee identifiers or partial card fingerprints.
- **Recommended fix:** Replace employee_id and card_fingerprint with hashed/masked values in log output. Log only rule_id, merchant_id, and alert counts.
- **Linear:** Needs GRO issue

**P0-CHIRP-03: No secrets management for production**
DB credentials and JWT signing keys referenced in config but stored in `.env` files. No integration with AWS Secrets Manager.
- **Recommended fix:** Retrieve secrets from AWS Secrets Manager at startup using `boto3`. Remove from `.env` for production.
- **Linear:** Needs GRO issue (platform-wide, see design spec known findings)

### P1 — Before GA

**P1-CHIRP-01: No rate limiting on REST endpoints**
All 15 `/api/chirp/*` endpoints are protected by JWT + role check but have no rate limiting. The `/api/chirp/sweep` endpoint triggers a full batch evaluation — an authenticated admin could accidentally or maliciously trigger continuous sweeps.
- **Recommended fix:** Add Flask-Limiter to chirp_bp. Suggested limits: 60/min for reads, 10/min for writes, 1/min for sweep.
- **Linear:** Needs GRO issue

**P1-CHIRP-02: No audit logging for threshold changes**
`ThresholdManager.set_merchant_threshold()` logs the change but does not write an audit trail record. Threshold changes directly affect detection sensitivity — who changed what and when must be traceable.
- **Recommended fix:** Write an audit log entry (or use existing AlertHistory pattern) for every threshold upsert, template apply, and threshold reset.
- **Linear:** Needs GRO issue

**P1-CHIRP-03: No data retention policy for alerts**
Alerts are append-only with no purge mechanism. Over time, the alerts table will grow unbounded. The Risk Aggregator queries all alerts for an entity without time limits (only filtering by status).
- **Recommended fix:** Implement retention policy: archive alerts older than 24 months, limit Risk Aggregator queries to 12-month window.
- **Linear:** Needs GRO issue (platform-wide)

**P1-CHIRP-04: Valkey client hardcoded to None**
`chirp_wired.py` line 22: `valkey_client = None`. The ThresholdManager's 3-layer cache (Valkey -> DB -> defaults) always falls through to DB for REST API calls. MCP tools also do not pass a Valkey client.
- **Recommended fix:** Wire the Valkey client from the Flask app config at blueprint registration time. This was flagged as Sprint 4 TODO.
- **Linear:** Needs GRO issue

**P1-CHIRP-05: Error responses may leak internals**
Several endpoints catch broad `Exception` and return `str(e)` in JSON error responses (e.g., `apply_template_endpoint`, `config_summary`). Stack traces and internal error messages should not reach the client.
- **Recommended fix:** Return generic error messages to clients. Log full exception details server-side.
- **Linear:** Needs GRO issue

**P1-CHIRP-06: DELETE threshold endpoint does not actually delete the DB row**
`reset_rule_thresholds()` only calls `invalidate_cache()` — it clears the Valkey cache but does not delete or nullify the `MerchantRuleConfig` row in the database. On next evaluation, the stale custom threshold will be reloaded from DB.
- **Recommended fix:** Delete or nullify the `MerchantRuleConfig.custom_threshold` for the rule, then invalidate cache.
- **Linear:** Needs GRO issue

### P2 — Post-Launch

**P2-CHIRP-01: No key rotation documentation**
Encryption keys (once PII encryption is implemented) need documented rotation procedures.
- **Recommended fix:** Document key rotation procedure tied to AWS Secrets Manager rotation schedule.

**P2-CHIRP-02: Batch sweep runs synchronously**
`evaluate_batch()` iterates all transactions in the time window sequentially in the request thread. For large merchants, this blocks the HTTP response.
- **Recommended fix:** Move batch sweep to a Valkey-backed task queue (background worker) and return a job ID from the REST endpoint.

**P2-CHIRP-03: Shallow MCP health check**
`_chirp_health()` returns static `healthy: True` without checking DB or Valkey connectivity. A deeper health check would verify the threshold resolution path works end-to-end.
- **Recommended fix:** Add DB ping and Valkey ping to health check. Return degraded status if Valkey is down but DB is up.

**P2-CHIRP-04: SDD vs code rule count drift**
The original SDD documented 29 rules across 8 categories. The actual code has 37 rules across 10 categories (dispute C-D01-D03, invoice C-I01-I03, composite C-901 added since SDD was written). This SDD now reflects the code.
- **Recommended fix:** Maintain SDD/code parity through CI validation or rule catalog metadata endpoint.

**P2-CHIRP-05: Risk Aggregator runs synchronously post-commit**
`schedule_risk_update()` runs in the request thread after alert commit. For batches with many distinct employees, this adds latency to the webhook response path.
- **Recommended fix:** Move risk recalculation to background task queue.

## Production Readiness Checklist

- [ ] PII encrypted at rest — **BLOCKED (P0-CHIRP-01):** alert details contain plaintext employee IDs and card fingerprints
- [ ] Secrets in AWS Secrets Manager — **BLOCKED (P0-CHIRP-03):** credentials in .env files
- [x] Health check endpoint responds — MCP health at `/chirp/health` (shallow, see P2-CHIRP-03)
- [ ] Audit logging for sensitive operations — **BLOCKED (P1-CHIRP-02):** no audit trail for threshold changes
- [ ] Data retention policy implemented — **BLOCKED (P1-CHIRP-03):** no alert purge mechanism
- [ ] Rate limiting on API endpoints — **BLOCKED (P1-CHIRP-01):** no rate limiting on chirp REST API
- [ ] Error responses don't leak internals — **BLOCKED (P1-CHIRP-05):** exception messages returned to client
- [x] JWT authentication on all endpoints — all 15 REST endpoints require `@jwt_required()` + `@roles_required()`
- [x] Graceful degradation — Valkey down: falls through to DB. DB down: falls back to catalog defaults. Individual rule failure: logged, not propagated.
- [x] Cross-database safety — `_load_merchant_thresholds()` uses `begin_nested()` SAVEPOINT for cross-schema operations
- [ ] Valkey cache wired — **BLOCKED (P1-CHIRP-04):** client hardcoded to None
- [ ] PII redacted from logs — **BLOCKED (P0-CHIRP-02):** employee IDs and partial card fingerprints in production logs
