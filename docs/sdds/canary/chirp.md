# Chirp

## Overview

Chirp is Canary's stateless detection rule engine. It evaluates Square merchant transactions, cash drawer shifts, gift card activities, and loyalty events against a catalog of 29 frozen detection rules across 8 categories. When a rule fires, Chirp produces an alert with a contextual risk score (0-100), writes it to `canary_app`, and optionally auto-creates a Fox investigation case for 6 critical-severity rules.

**Design principle:** Webhook in -> Score -> Decide -> Fire (or don't) -> Done. Chirp never mutates transaction data. The source transaction stays in Square; only the alert decision persists in Canary.

### Evaluation Tiers

| Tier | Engine | DB Access | Rule Count |
|------|--------|-----------|------------|
| 1 (Stateless) | `stateless_engine.py` | None | 6 rules (C-004, C-007, C-009, C-010, C-011, C-502) |
| 2 (Lightweight) | `rule_engine.py` | Valkey counters | 9 rules (windowed aggregation) |
| 3 (Full DB) | `rule_engine.py` | SQLAlchemy queries against `canary_sales` | 14 rules (cross-reference checks) |

### Rule Categories (29 rules)

| Category | IDs | Count |
|----------|-----|-------|
| payment | C-001 through C-011 | 11 |
| cash_drawer | C-101 through C-104 | 4 |
| order | C-201 through C-204 | 4 |
| timecard | C-301 through C-303 | 3 |
| void | C-501, C-502 | 2 |
| gift_card | C-601, C-602 | 2 |
| loyalty | C-801 through C-804 | 4 |

### Code Entry Points

| File | Role |
|------|------|
| `canary/services/chirp/rule_definitions.py` | Frozen dataclass rule catalog (29 `ChirpRuleDefinition` instances) |
| `canary/services/chirp/stateless_engine.py` | Tier 1 pure-function evaluation (6 rules, no ORM) |
| `canary/services/chirp/rule_engine.py` | `ChirpRuleEngine` class — all tiers, requires SQLAlchemy session |
| `canary/services/chirp/threshold_manager.py` | Per-merchant threshold CRUD with 3-layer Valkey cache |
| `canary/services/chirp/tools.py` | 10 MCP tool definitions for `canary-chirp` server |
| `canary/services/alert_config.py` | Sensitivity presets, templates, validation |
| `canary/blueprints/chirp_wired.py` | REST API at `/api/chirp/*` (JWT + admin/owner) |
| `canary/blueprints/chirp_mcp.py` | MCP blueprint at `/chirp/*` (manifest, tools, health) |

### Velocity/Heatmap Scoring (SDD-006)

Velocity and heatmap scoring engines are the statistical backbone for "something changed" detection. The velocity engine uses Poisson-process modeling with z-score analysis against rolling baselines. The heatmap engine classifies KPIs into score bands (normal/watch/review/investigate) for dashboard rendering. Both are pure functions with no database access. Primary documentation lives in `analytics.md`; they are cross-referenced here because 15 scored metrics map directly to Chirp rules.

### Key Dependencies

Inbound: Webhook Pipeline calls `ChirpRuleEngine.evaluate_transaction()` via `sub4_detect`. Ops calls `chirp_lab` for test evaluations.
Outbound: Writes `Alert` + `AlertHistory` rows to `canary_app`. Auto-creates Fox cases for 6 critical rules (C-009, C-104, C-204, C-301, C-502, C-602).


## API Contracts

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

| Tool Name | Category | DB? | Purpose |
|-----------|----------|-----|---------|
| `get_rules` | rules | No | List rules, optional category/tier filter |
| `get_rule` | rules | No | Look up single rule by ID |
| `evaluate_stateless` | evaluation | No | Run Tier 1 rules against parsed webhook payload |
| `apply_sensitivity` | configuration | No | Compute adjusted thresholds at a sensitivity level |
| `get_templates` | configuration | No | List config templates (retail_standard, food_service, etc.) |
| `apply_template` | configuration | No | Apply template, return full rule config |
| `validate_thresholds` | configuration | No | Validate proposed thresholds (field names, ranges, extremes) |
| `get_config_summary` | configuration | No | Summarize merchant config vs catalog defaults |
| `estimate_sensitivity` | configuration | No | Classify current thresholds to closest sensitivity level |
| `get_merchant_thresholds` | configuration | Yes | Get merchant thresholds (Valkey cache -> DB -> defaults) |

### Sensitivity Presets

| Preset | Effect |
|--------|--------|
| `strict` | Lower thresholds, more alerts (aggressive detection) |
| `default` | Catalog defaults (balanced) |
| `relaxed` | Higher thresholds, fewer alerts |
| `minimal` | Highest thresholds, lowest false positive rate |

### Configuration Templates

Industry-specific threshold profiles: `retail_standard`, `food_service`, `high_value`, `high_volume`, `new_merchant`. Each template adjusts thresholds and enable/disable flags across all 29 rules.


## Data Model

All Chirp-owned tables live in the `app` schema (`canary_app` database).

### `detection_rules` (global catalog)

Not tenant-scoped. 29 frozen rules across 8 categories.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | String(36) | PK, uuid4 | |
| `rule_id` | String(20) | UNIQUE, NOT NULL | C-001 through C-804 |
| `rule_name` | String(255) | NOT NULL | Human-readable name (e.g., RAPID_REFUND) |
| `description` | Text | nullable | What the rule detects |
| `category` | String(50) | NOT NULL | payment/cash_drawer/order/timecard/void/inventory/gift_card/loyalty |
| `default_threshold` | Text | nullable | JSON: `{field: value}` |
| `severity` | String(20) | NOT NULL, default "medium" | low/medium/high/critical |
| `is_active` | Boolean | NOT NULL, default True | |

Mixins: AuditMixin. Indexes: `idx_detection_rules_rule_id`, `idx_detection_rules_category`.

### `merchant_rule_config` (per-merchant overrides)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | String(36) | PK, uuid4 | |
| `merchant_id` | String(36) | NOT NULL, TenantMixin | FK to merchants |
| `rule_id` | String(20) | NOT NULL | FK to `detection_rules.rule_id` |
| `is_enabled` | Boolean | NOT NULL, default True | Whether rule fires for this merchant |
| `custom_threshold` | Text | nullable | JSON: overrides `default_threshold` |

Mixins: TenantMixin, AuditMixin. Index: `idx_merchant_rule_config_merchant_rule` (merchant_id, rule_id).

### Related Tables (owned by Alert domain)

Chirp writes to these but does not own them (see `alert.md`):

- **`alerts`** -- Append-only. Columns: id, merchant_id, rule_id, alert_type, severity, source_table, source_id, employee_id, location_id, details (JSON), amount_cents, impact_cents, created_at, created_by.
- **`alert_history`** -- Status audit trail. Columns: id, alert_id, status (new/acknowledged/investigating/resolved/false_positive), changed_by, notes.

### ThresholdManager Cache (Valkey)

Three-layer resolution for merchant-specific thresholds:

1. **Valkey cache** -- Key: `chirp:thresholds:{merchant_id}:{rule_id}`, TTL: 300s
2. **Database** -- `MerchantRuleConfig` row in `canary_app`
3. **Catalog defaults** -- `ChirpRuleDefinition.default_thresholds`

Additional cache key: `chirp:active_rules:{merchant_id}` (300s TTL) for bulk active-rule lookups.

### Access Patterns

- Rule catalog: read-only lookups by `rule_id`, `category`, or `tier` via helper functions (`RULE_MAP`, `get_rule()`, `get_rules_by_category()`, `get_rules_by_tier()`)
- Merchant config: upsert on threshold change, bulk load for config summary, cache invalidation on write/delete
- Alerts: append-only inserts during rule evaluation, never updated by Chirp


## Workflows

### Real-Time Detection (Webhook-Triggered)

```
1. Square webhook arrives at webhooks_tsp.py
2. TSP pipeline parses payload (sub2_parse)
3. sub4_detect triggers Chirp evaluation:
   a. stateless_engine.evaluate_stateless(parsed, thresholds)
      - Runs 6 Tier 1 rules (no DB, pure function)
      - Each checker returns 0 or 1 alert dicts
   b. ChirpRuleEngine.evaluate_transaction(txn_id, merchant_id)
      - _load_merchant_thresholds() via ThresholdManager (3-layer lookup)
      - Runs category-specific checkers:
        _check_payment_rules (C-001..C-008)
        _check_cash_drawer_rules (C-101..C-104)
        _check_order_rules (C-201..C-203)
        _check_timecard_rules (C-301..C-303)
        _check_void_rules (C-501..C-502)
        _check_gift_card_rules (C-601..C-602)
        _check_loyalty_rules (C-801..C-804)
4. _write_alerts() inserts Alert + AlertHistory (status="new")
5. _auto_create_cases() creates Fox cases for 6 critical rules (best-effort)
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
6. Writes all accumulated alerts
```

### Health Check Pipeline (Demo/Ops Mode)

```
1. MerchantSimulator generates synthetic transactions
2. ChirpRuleEngine.evaluate_readonly(txn, merchant_id) -> alert dicts (no write)
3. Caller writes alerts via write_alerts_to_session(alerts, merchant_id, app_session)
4. Separate sessions: canary_sales (read) and canary_app (write)
```

### Velocity/Heatmap Scoring Pipeline

Velocity engine builds `VelocityProfile` from historical daily values, selects best baseline (hourly > daily > overall), and runs `detect_anomaly()` with sigma=2.0. Classifies as spike/drop/zero/none with confidence scaling by sample size (7=0.5, 30=0.85, 60+=0.95). Anomalies surface in Owl and drive alert generation.

Heatmap scoring classifies 15 KPIs into bands (normal/watch/review/investigate) via `score_all_metrics()`. Supports `higher_is_worse` (refunds, voids: 100/110/120% bands) and `lower_is_worse` (sales, txn count: 100/90/80% inverted bands). Scored metrics map to Chirp rules (REFUND_RATE->C-002, VOID_COUNT->C-501, etc.). Results render as color-coded dashboard grid. See `analytics.md` for full detail.

### Threshold Configuration Flow

```
1. Merchant selects sensitivity preset (strict/default/relaxed/minimal)
   OR applies industry template (retail_standard, food_service, etc.)
   OR sets per-rule custom thresholds
2. Validation: validate_thresholds() checks field names, value ranges, warns on extremes
3. Write: ThresholdManager.set_merchant_threshold() upserts MerchantRuleConfig row
4. Cache invalidation: Valkey key cleared, next evaluation loads fresh threshold
```

### Auto-Case Creation

Six rules in `_AUTO_CASE_RULES` automatically create Fox investigation cases after alert flush:
- C-009 (SQUARE_DELAY_HOLD), C-104 (AFTER_HOURS_DRAWER), C-204 (UNTENDERED_ORDER)
- C-301 (OFF_CLOCK_TRANSACTION), C-502 (POST_VOID_ALERT), C-602 (GIFT_CARD_DRAIN)

Auto-case creation is best-effort via `FoxCaseService.create_case()`. Failures logged as warnings, never block the alert pipeline.

### Error Handling

- Each rule checker is wrapped in try/except; one rule failure does not block others
- `_write_alerts()` catches per-alert write failures and continues
- `_load_merchant_thresholds()` uses SAVEPOINT (`begin_nested()`) for cross-database safety, falls back to catalog defaults
- ThresholdManager Valkey operations are all try/except guarded; cache misses silently fall through
- `_auto_create_cases()` is best-effort; failures never propagate


## Risk Aggregator Service (GRO-247)

Entity-level risk score aggregation. Converts per-alert Chirp scores (0-100 int) into a normalized entity risk score (0.0-1.0 float) using recency-weighted averaging.

### Code Entry Point

| File | Role |
|------|------|
| `canary/services/chirp/risk_aggregator.py` | Entity risk score aggregation — employee and card profiles |

### Functions

| Function | Purpose |
|----------|---------|
| `aggregate_entity_risk(alerts)` | Core aggregation: per-alert scoring → recency weighting → normalized average. Returns `(risk_score, factors_dict)` |
| `update_employee_risk(merchant_id, employee_id, session)` | Full pipeline: query alerts → aggregate → upsert EntityRiskScore + RiskScoreHistory + Employee.risk_score |
| `update_card_risk(merchant_id, card_fingerprint, session)` | Same pattern for card profiles. **Gated** — returns 0.0 until `Alert.card_fingerprint` column exists (GRO-263) |
| `_alert_score(alert)` | Per-alert risk score (0-100) via `compute_risk_score()`. Handles JSON/dict details parsing |
| `_recency_weight(alert_age)` | Maps alert age to recency weight band |
| `_score_to_category(score)` | Maps 0.0-1.0 float to risk category string |

### Recency Weight Bands

| Age | Weight |
|-----|--------|
| Within 24h | 3.0x |
| 1-7 days | 2.0x |
| 7-30 days | 1.0x |
| Over 30 days | 0.5x |

Normalization: `total_weighted_score / (alert_count * max_weight)` — recent alerts contribute full score, old alerts damped to 1/6th.

### Score Categories

| Score Range | Category |
|-------------|----------|
| < 0.3 | low |
| 0.3 - 0.6 | medium |
| 0.6 - 0.8 | high |
| >= 0.8 | critical |

### Pipeline Flow

```
1. Query Alert rows for entity (employee_id or card_fingerprint)
   - Excludes dismissed/false_positive via AlertHistory subquery
     (latest status per alert_id, filtered by cleared_statuses set)
2. Per-alert: _alert_score() → compute_risk_score(severity, amount_cents, details)
3. Per-alert: _recency_weight(now - created_at) → weight band
4. aggregate_entity_risk(): weighted_sum / (count * max_weight) → clamped [0.0, 1.0]
5. _score_to_category(risk_score) → low/medium/high/critical
6. Persist:
   a. Employee.risk_score (app schema) — direct attribute update
   b. EntityRiskScore upsert (metrics schema) — SCD Type 1
   c. RiskScoreHistory append (metrics schema) — immutable audit trail
```

### Cross-Domain Data Access

- **Reads:** `Alert`, `AlertHistory` (app schema) — alert query + status filtering
- **Writes:** `EntityRiskScore`, `RiskScoreHistory` (metrics schema) — score persistence
- **Updates:** `Employee.risk_score` (app schema) — denormalized score on entity row
- **Dependency:** `compute_risk_score()` from `rule_engine.py`, `RULE_MAP` from `rule_definitions.py`

### Constraints

- Card risk scoring (`update_card_risk`) is gated — returns 0.0 until `Alert.card_fingerprint` column is added (GRO-263). Previous implementation used `details.contains()` substring matching which caused false positives and could not use indexes.
- All operations run within a single SQLAlchemy session (caller must commit/rollback)
- Factor contributions are keyed by rule category (payment, void, cash_drawer, etc.) resolved via `RULE_MAP`
