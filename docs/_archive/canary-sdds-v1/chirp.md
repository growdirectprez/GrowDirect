# Chirp Detection Engine

> **Status:** Complete — written from code
> **Namespace:** canary
> **Last updated:** 2026-03-30
> **Code location:** `Canary/canary/services/chirp/`

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]

---

## 1. Overview

Chirp is Canary's fraud and loss prevention detection engine. It evaluates Square merchant transaction data against a catalog of 37 detection rules, produces structured alerts, and automatically escalates critical findings to Fox (the case management service).

The engine is triggered in two paths:

- **Real-time (Tier 1):** The TSP Sub4 consumer (`sub4_detect`) receives parsed webhook payloads and calls the stateless engine directly. No database reads. Zero latency.
- **Batch (Tier 2/3):** The `ChirpRuleEngine` class runs per-transaction and per-period evaluations against PostgreSQL (canary_sales and canary_app schemas). Triggered by the `/sweep` endpoint or the TSP Sub4 pipeline after DB persistence.

Rules span 10 categories: `payment`, `cash_drawer`, `order`, `timecard`, `void`, `gift_card`, `loyalty`, `composite`, `dispute`, and `invoice`. Severity levels are `critical`, `high`, `medium`, and `low`. Critical alerts auto-create Fox investigation cases.

---

## 2. Architecture

### Component Diagram

```
Square Webhooks
      |
      v
  TSP (sub4_detect consumer)
      |
      +-------> stateless_engine.evaluate_stateless()   [Tier 1: no DB]
      |
      +-------> ChirpRuleEngine.evaluate_readonly()     [Tier 2/3: DB reads]
                     |
                     v
               write_alerts_to_session()
                     |
                     +---> Alert + AlertHistory rows (canary_app)
                     |
                     +---> _auto_create_cases()          [Fox integration]
                     |
                     +---> _dispatch_notifications()     [GRO-254]
                     |
                     +---> schedule_risk_update()        [GRO-247]
                                  |
                                  v
                          risk_aggregator.update_employee_risk()
                          -> Employee.risk_score
                          -> EntityRiskScore (metrics schema)
                          -> RiskScoreHistory (metrics schema)

Batch sweep (POST /api/chirp/sweep or scheduled)
      |
      v
  ChirpRuleEngine.evaluate_batch()
      -> evaluate_transaction() per txn in window
      -> _check_untendered_orders()   [C-204, batch-only]
      -> _check_sra_rules()           [C-901, period-level composite]
```

### Request / Data Flow

**Tier 1 — Stateless path (webhook → alert dict, no DB):**

1. TSP Sub4 calls `stateless_engine.evaluate_stateless(parsed, thresholds, disabled_rules)`.
2. Engine checks each Tier 1 rule against fields in the parsed payload dict.
3. Returns a list of alert dicts. No writes. No DB access.
4. Caller (TSP) decides whether to persist the dicts via `write_alerts_to_session()`.

**Tier 2/3 — Full engine path (transaction → alert → Fox):**

1. TSP Sub4 (or `/sweep` endpoint) loads a `Transaction` ORM object from canary_sales.
2. Calls `ChirpRuleEngine.evaluate_readonly(txn, merchant_id)`.
3. Engine calls `_load_merchant_thresholds(merchant_id)` — reads `DetectionRule` (global active) and `MerchantRuleConfig` (per-merchant overrides) with SAVEPOINT protection for cross-schema safety.
4. Dispatches to rule checkers: `_check_payment_rules`, `_check_void_rules`, `_check_timecard_rules`, `_check_order_rules` (when `order_id` is present), `_check_cash_drawer_rules`, `_check_gift_card_rules`, `_check_loyalty_rules`, `_check_dispute_rules`, `_check_invoice_rules`.
5. Returns alert dicts. Caller writes them via `write_alerts_to_session()`.
6. After flush+commit, `_auto_create_cases()` fires for rules in `_AUTO_CASE_RULES`.
7. `_dispatch_notifications()` fires for all written alerts (per-rule notify toggle).
8. `schedule_risk_update()` recalculates `Employee.risk_score` for affected employees.

**C-204 / C-901 — Batch-only rules:**

- C-204 (UNTENDERED_ORDER) runs during `evaluate_batch()`, not per-transaction. It queries order_ids with exactly one transaction older than the stale threshold.
- C-901 (SRA_THRESHOLD_BREACH) runs during `evaluate_batch()`, queries `PeriodMetrics` for the latest fiscal period.

### Key Design Decisions

**Tier classification.** Rules are classified into three tiers based on their data requirements:
- Tier 1 (stateless): Fires from a single webhook payload. No database. No lookups. Pure payload inspection. Tier 1 rules can fire in the TSP pipeline before any DB write.
- Tier 2 (Valkey counters): Requires window-based counting — uses either Valkey counters or SQLAlchemy aggregate queries against canary_sales.
- Tier 3 (full DB): Requires cross-table joins, shift reconciliation, period aggregates, or refund correlation.

**Separate read and write sessions.** The TSP pipeline uses separate SQLAlchemy sessions for reads (canary_sales) and writes (canary_app). `evaluate_readonly()` never writes. `write_alerts_to_session()` is the write entry point, accepting a caller-provided session.

**Square ID resolution.** Transaction data stores Square team_member_id and Square location_id strings. The `alerts` table FKs reference `employees.id` and `locations.id` (UUIDs). `_resolve_square_ids()` does a single-pass batch lookup before any INSERT to prevent FK violations without N+1 queries.

**SAVEPOINT protection for threshold loading.** `_load_merchant_thresholds()` wraps the DB reads in `session.begin_nested()` so a cross-schema failure (e.g., when the session is bound to canary_sales but MerchantRuleConfig lives in canary_app) does not abort the outer transaction.

**Alert append-only contract.** The `alerts` table has no UPDATE or DELETE. Status changes are tracked in `alert_history`. `AlertHistory` is written atomically alongside each alert: initial status is always `new`.

**Auto-case threshold.** Only six rules auto-create Fox cases. The set is a frozen constant (`_AUTO_CASE_RULES`) defined in `rule_engine.py`. Adding a rule to this set is the only way to enable auto-case creation for it.

---

## 3. Data Model

All models use SQLAlchemy 2.0 `Mapped[]` syntax. Located in `Canary/canary/models/app/detection.py`.

### DetectionRule

Global detection rule catalog. Not tenant-scoped. Seeded from `RULE_CATALOG` on first boot via `seed_detection_rules()`.

```python
class DetectionRule(AppBase, AuditMixin):
    __tablename__ = "detection_rules"

    id: Mapped[str]                  # UUID (String 36), PK
    rule_id: Mapped[str]             # C-001 through C-I03 (unique, indexed)
    rule_name: Mapped[str]           # Human-readable name (e.g., RAPID_REFUND)
    description: Mapped[Optional[str]]  # Plain-language description
    category: Mapped[str]            # payment | cash_drawer | order | timecard |
                                     # void | gift_card | loyalty | composite |
                                     # dispute | invoice
    default_threshold: Mapped[Optional[str]]  # JSON: {field: value}
    severity: Mapped[str]            # low | medium | high | critical
    is_active: Mapped[bool]          # Global default (True unless explicitly disabled)
```

Indexes: `idx_detection_rules_rule_id`, `idx_detection_rules_category`.

### MerchantRuleConfig

Per-merchant threshold and enable/disable overrides. Tenant-scoped (inherits `TenantMixin` → `merchant_id` FK). One row per merchant+rule_id combination.

```python
class MerchantRuleConfig(AppBase, TenantMixin, AuditMixin):
    __tablename__ = "merchant_rule_config"

    id: Mapped[str]                  # UUID (String 36), PK
    rule_id: Mapped[str]             # FK → detection_rules.rule_id (indexed)
    is_enabled: Mapped[bool]         # Per-merchant override (wins over global is_active)
    custom_threshold: Mapped[Optional[str]]  # JSON: overrides default_threshold
    notify_enabled: Mapped[bool]     # GRO-254: per-rule notification toggle
```

Index: `idx_merchant_rule_config_merchant_rule` on `(merchant_id, rule_id)`.

### Alert

Detected fraud alert. Append-only (no UPDATE, no DELETE). Each row represents one rule firing on one source event.

```python
class Alert(AppBase, TenantMixin, AuditMixin):
    __tablename__ = "alerts"

    id: Mapped[str]                  # UUID (String 36), PK
    rule_id: Mapped[str]             # FK → detection_rules.rule_id (indexed)
    alert_type: Mapped[str]          # Rule name derived from rule_id
    severity: Mapped[str]            # low | medium | high | critical
    source_table: Mapped[str]        # transactions | cash_drawer_shifts |
                                     # gift_card_activities | loyalty_events |
                                     # disputes | invoices | period_metrics
    source_id: Mapped[str]           # Row ID in source_table
    employee_id: Mapped[Optional[str]]  # FK → employees.id (nullable, indexed)
    location_id: Mapped[Optional[str]]  # FK → locations.id (nullable, indexed)
    details: Mapped[Optional[str]]   # JSON: {reason, values, context}
    amount_cents: Mapped[Optional[int]]  # Transaction amount (if applicable)
    impact_cents: Mapped[Optional[int]]  # Estimated dollar impact (GRO-141, immutable)
    created_at: Mapped[datetime]     # Alert detection timestamp (immutable)
    created_by: Mapped[Optional[str]]   # 'chirp' or triggering user ID
```

Compound indexes:
- `idx_alerts_merchant_created` on `(merchant_id, created_at)` — primary list query
- `idx_alerts_merchant_rule` on `(merchant_id, rule_id)` — rule-specific queries
- `idx_alerts_merchant_employee` on `(merchant_id, employee_id)` — employee risk
- `idx_alerts_merchant_location` on `(merchant_id, location_id)` — location drill
- `idx_alerts_severity` on `(merchant_id, severity)` — severity filters

### AlertHistory

One row per status transition. Provides full audit trail for each alert.

```python
class AlertHistory(AppBase, AuditMixin):
    __tablename__ = "alert_history"

    id: Mapped[str]                  # UUID (String 36), PK
    alert_id: Mapped[str]            # FK → alerts.id (indexed)
    status: Mapped[str]              # new | investigating | resolved |
                                     # false_positive | dismissed
    changed_by: Mapped[Optional[str]]   # FK → users.id (None for system-generated)
    notes: Mapped[Optional[str]]     # Free text
```

Indexes: `idx_alert_history_alert_id`, `idx_alert_history_status` on `(alert_id, status)`.

---

## 4. Interfaces

### REST Endpoints — `chirp_wired.py` (Blueprint: `chirp`, prefix: `/api/chirp`)

All routes require JWT authentication (`@jwt_required()`). Most require `admin` or `owner` role.

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/rules` | admin, owner | List all rules. Optional `?category=` filter. Returns rule catalog + category list. |
| GET | `/rules/<rule_id>` | admin, owner | Get one rule with default + merchant thresholds. |
| PUT | `/rules/<rule_id>/thresholds` | admin, owner | Upsert merchant-specific thresholds for a rule. |
| DELETE | `/rules/<rule_id>/thresholds` | admin, owner | Reset merchant thresholds to defaults (invalidates Valkey cache). |
| GET | `/config` | admin, owner | Get all active rules with merchant thresholds. |
| POST | `/sweep` | admin | Trigger a batch sweep over the past N minutes. Returns alert count. |
| GET | `/categories` | admin, owner | List distinct rule categories. |
| GET | `/sensitivity` | admin, owner | List sensitivity presets (strict/default/relaxed/minimal) with multipliers. |
| POST | `/sensitivity/preview` | admin, owner | Preview adjusted thresholds for a rule at a sensitivity level. |
| POST | `/sensitivity/estimate` | admin, owner | Estimate closest sensitivity level for given thresholds. |
| GET | `/templates` | admin, owner | List configuration templates (retail_standard, food_service, high_value, high_volume, new_merchant). |
| POST | `/templates/preview` | admin, owner | Preview template effect on all rules. |
| POST | `/templates/apply` | admin, owner | Apply a template — writes MerchantRuleConfig rows for every rule. |
| POST | `/validate` | admin, owner | Validate proposed thresholds before saving. Returns is_valid, errors, warnings. |
| GET | `/summary` | admin, owner | Summarize merchant configuration vs defaults (enabled/disabled/customized counts). |

### MCP Server — `chirp_mcp.py` (server: `canary-chirp`, prefix: `/chirp`)

10 MCP tools registered via `MCPRegistry`. 9 are pure (no DB). 1 reads merchant thresholds.

| Tool | Category | DB | Description |
|------|----------|----|-------------|
| `get_rules` | rules | No | List catalog, filter by category or tier |
| `get_rule` | rules | No | Look up single rule by ID |
| `evaluate_stateless` | evaluation | No | Run Tier 1 rules against a parsed payload dict |
| `apply_sensitivity` | configuration | No | Compute thresholds at a sensitivity level |
| `get_templates` | configuration | No | List available templates |
| `apply_template` | configuration | No | Apply template, return full rule config |
| `validate_thresholds` | configuration | No | Validate proposed thresholds for a rule |
| `get_config_summary` | configuration | No | Summarize merchant config vs defaults |
| `estimate_sensitivity` | configuration | No | Classify thresholds against sensitivity presets |
| `get_merchant_thresholds` | configuration | Yes | Get effective thresholds (cache → DB → defaults) |

---

## 5. Service Layer

### rule_definitions.py — Frozen Rule Catalog

Defines `ChirpRuleDefinition` (frozen dataclass) and `RULE_CATALOG` (list of 37 rules). `RULE_MAP` is a dict keyed by `rule_id` for O(1) lookup.

Fields per definition: `rule_id`, `name`, `category`, `severity`, `description`, `default_thresholds`, `tier`.

Helper functions: `get_rule(rule_id)`, `get_rules_by_category(category)`, `get_all_categories()`, `get_rules_by_tier(tier)`, `get_stateless_rules()`.

### stateless_engine.py — Tier 1 Evaluation

`evaluate_stateless(parsed, thresholds, disabled_rules) -> List[Dict]`

Evaluates all Tier 1 rules from a single parsed webhook dict. No database. No ORM imports. Returns alert dicts or an empty list.

Tier 1 rules implemented:
- **C-004** — After-hours transaction (hour check against open_hour/close_hour)
- **C-007** — High-value refund (transaction_type in RETURN/REFUND + amount threshold)
- **C-009** — Square delay hold (delay_action present + payment still APPROVED)
- **C-010** — Partial authorization (approved_amount_cents < amount_cents by more than variance_cents)
- **C-011** — No-sale detected (transaction_type == NO_SALE)

Each checker is a private function (`_check_*`) returning a list with 0 or 1 alert. Alert dicts are built by `_make_alert(rule_id, parsed, details)` and include: `id` (UUID4), `rule_id`, `name`, `severity`, `category`, `source` ("stateless"), `source_id`, `merchant_id`, `employee_id`, `location_id`, `amount_cents`, `details`, `fired_at`.

### rule_engine.py — Full Detection Engine

**`compute_risk_score(severity, amount_cents, details) -> int`**

Returns a contextual risk score 0–100.

```
base_score = SEVERITY_BASE_SCORES[severity]
  critical = 90, high = 70, medium = 45, low = 20, info = 10

amount_boost:
  >= $1000 (100000 cents): +15
  >= $500 (50000 cents):   +10
  >= $100 (10000 cents):   +5

override (from details["score"]):
  base = int((base * 0.4) + (details["score"] * 0.6))

final = min(100, max(0, base + amount_boost))
```

**`ChirpRuleEngine`**

Stateful class initialized with a SQLAlchemy `Session`. Primary evaluation methods:

| Method | Trigger | Rules covered |
|--------|---------|---------------|
| `evaluate_transaction(transaction_id, merchant_id)` | TSP / ad hoc | C-001 to C-011, C-501, C-502, C-301 to C-303, C-201 to C-203 |
| `evaluate_readonly(txn, merchant_id)` | TSP Sub4 (read-only) | Same as above, no writes |
| `evaluate_cash_drawer(shift_id, merchant_id)` | TSP cash drawer events | C-101 to C-104 |
| `evaluate_batch(merchant_id, since_minutes)` | Sweep endpoint | All transaction rules + C-204 + C-901 |
| `evaluate_gift_card_activity(activity_id, merchant_id)` | TSP gift card events | C-601, C-602 |
| `evaluate_loyalty_event(event_id, merchant_id)` | TSP loyalty events | C-801 to C-804 |
| `evaluate_dispute(dispute_id, merchant_id)` | TSP dispute events | C-D01 to C-D03 |
| `evaluate_invoice(invoice_id, merchant_id, event_type)` | TSP invoice events | C-I01 to C-I03 |

**Rule evaluation dispatch (`_evaluate_with_thresholds`):**
1. `_check_payment_rules(txn)` → C-001 through C-011
2. `_check_void_rules(txn)` → C-501, C-502
3. `_check_timecard_rules(txn)` → C-301, C-302, C-303
4. If `txn.order_id` present: load `TransactionLineItem` rows, call `_check_order_rules(line_items)` → C-201, C-202, C-203
5. `_filter_disabled(alerts, thresholds)` removes alerts for rules in `thresholds["_disabled"]`

**C-502 tiered void detection:**
- IMMEDIATE (gap < 120s): No alert. Legitimate correction.
- WATCH (120s to 900s): `severity=high`, `tier="watch"`.
- SUSPICIOUS (900s to 28800s): `severity=critical`, `tier="suspicious"`.
- Beyond 28800s: No alert.
- Self-refund bonus: +10 to score when `txn.employee_id == original.employee_id`.
- Requires `RefundLink` record correlating refund to original sale.

**Auto-case creation (`_AUTO_CASE_RULES`):**

The following six rules trigger automatic Fox case creation after alert commit:

| Rule ID | Name |
|---------|------|
| C-009 | SQUARE_DELAY_HOLD |
| C-104 | AFTER_HOURS_DRAWER |
| C-204 | UNTENDERED_ORDER |
| C-301 | OFF_CLOCK_TRANSACTION |
| C-502 | POST_VOID_ALERT |
| C-602 | GIFT_CARD_DRAIN |

Case data: `title = "Auto: {rule_name}"`, `priority = "critical"`, `case_type = {rule.category}`, `created_by = "chirp"`. Best-effort: failure never blocks the alert pipeline.

**`write_alerts_to_session(alerts, merchant_id, session) -> int`**

Standalone function (not a method) for use in cross-session pipelines (TSP Sub4). Steps:
1. Calls `_resolve_square_ids()` to batch-resolve Square employee/location IDs → UUIDs.
2. Inserts `Alert` + `AlertHistory` rows (status `new`) per alert dict.
3. Flushes and commits. Returns count of successfully written alerts.
4. On success, calls `schedule_risk_update()` for affected employees.

**`_load_merchant_thresholds(merchant_id) -> Dict`**

Loads effective thresholds for all rules. Priority order:
1. Catalog defaults (always base layer).
2. `DetectionRule.is_active` — global enable flag.
3. `MerchantRuleConfig.is_enabled` — per-merchant override (wins over global).
4. `MerchantRuleConfig.custom_threshold` — per-merchant threshold values.

Disabled rule IDs collected into `thresholds["_disabled"]` (a `set`). Uses `session.begin_nested()` (SAVEPOINT) to protect against cross-schema failures.

### threshold_manager.py — `ThresholdManager`

Manages the read and write path for merchant rule configuration, with optional Valkey caching.

Cache key patterns:
- Per-rule: `chirp:thresholds:{merchant_id}:{rule_id}` (TTL 300s)
- All rules: `chirp:active_rules:{merchant_id}` (TTL 300s)

Read path: Valkey cache → `MerchantRuleConfig` DB query → rule catalog defaults.

Write path: `set_merchant_threshold(merchant_id, rule_id, thresholds)` — upserts `MerchantRuleConfig`, then calls `invalidate_cache(merchant_id, rule_id)` to evict both the per-rule key and the active rules list.

### risk_aggregator.py — Entity Risk Scoring

**`aggregate_entity_risk(alerts) -> (float, Dict[str, float])`**

Converts a list of `Alert` objects into a normalized entity risk score (0.0–1.0) using recency-weighted averaging.

Recency weights:
- Within 24h: 3.0x
- 1–7 days: 2.0x
- 7–30 days: 1.0x
- Over 30 days: 0.5x

Formula:
```
per_alert_score = compute_risk_score(alert.severity, alert.amount_cents, alert.details) / 100.0
weighted = per_alert_score * recency_weight(age)
risk_score = sum(weighted) / (len(alerts) * max_weight)  # max_weight = 3.0
risk_score = clamp(risk_score, 0.0, 1.0)
```

Returns `(risk_score, factors)` where `factors` maps each rule category to its contribution to the total score.

Risk category bands: `critical` (>= 0.8), `high` (>= 0.6), `medium` (>= 0.3), `low` (< 0.3).

**`update_employee_risk(merchant_id, employee_id, session) -> float`**

Full pipeline:
1. Query active alerts for employee, excluding those whose latest `AlertHistory.status` is `dismissed` or `false_positive`.
2. Call `aggregate_entity_risk()`.
3. Update `Employee.risk_score` in app schema.
4. Upsert `EntityRiskScore` in metrics schema (SCD Type 1).
5. Append `RiskScoreHistory` in metrics schema (permanent record).

**`update_card_risk(merchant_id, card_fingerprint, session) -> float`**

Same pattern as employee risk, but for `CardProfile`. Currently gated (GRO-263): returns 0.0 because `Alert` lacks a dedicated `card_fingerprint` column. `EntityRiskScore` and `RiskScoreHistory` rows are still written at 0.0 to maintain schema consistency.

### seed_rules.py — Catalog Seeding

`seed_detection_rules() -> int`

Populates the `detection_rules` table from `RULE_CATALOG` on first boot. Only runs when the table is empty. All 37 rules seeded as `is_active=True`.

`_sync_rule_catalog(session, DetectionRule) -> int`

Runs on every subsequent boot. Syncs `severity` and `description` from the code catalog to the DB to prevent drift from earlier deployments that defaulted severity to `medium`.

### rule_guides.py — Plain-Language Alert Guides

`RULE_GUIDES: dict[str, RuleGuide]` — guides for the top 8 rules: C-502, C-301, C-004, C-007, C-001, C-005, C-101, C-102.

Each `RuleGuide` contains: `what_happened` (narrative), `why_it_matters`, `what_to_do` (list of action steps), `example` (concrete scenario).

Functions: `get_rule_guide(rule_id)`, `get_all_guide_ids()`, `guide_to_dict(guide)`.

---

## 6. Configuration

### Rule Thresholds

All thresholds are configurable per merchant. Catalog defaults are defined in `rule_definitions.py` as `default_thresholds` on each `ChirpRuleDefinition`. Merchants override them via `MerchantRuleConfig.custom_threshold` (JSON).

Default thresholds by rule:

| Rule | Threshold key(s) | Default |
|------|-----------------|---------|
| C-001 | seconds | 900 |
| C-002 | percent, min_transactions | 15%, 5 txns |
| C-003 | count, window_seconds | 5, 3600 |
| C-004 | open_hour, close_hour | 6, 22 |
| C-005 | count, window_seconds | 5, 3600 |
| C-006 | count, window_seconds | 3, 3600 |
| C-007 | amount_cents | 10000 ($100) |
| C-008 | count, window | 5, shift |
| C-010 | variance_cents | 0 |
| C-101 | count, window | 5, shift |
| C-102 | amount_cents | 2000 ($20) |
| C-103 | amount_cents | 5000 ($50) |
| C-104 | open_hour, close_hour | 6, 22 |
| C-201 | percent | 50% |
| C-202 | percent, min_items | 10%, 10 items |
| C-203 | amount_cents | 2000 ($20) |
| C-204 | stale_hours | 24 |
| C-301–C-303 | (none — binary checks) | — |
| C-501 | count, window | 5, shift |
| C-502 | immediate_max_seconds, watch_max_seconds, suspicious_max_seconds, self_refund_score_boost, off_clock_score_boost | 120, 900, 28800, 10, 15 |
| C-601 | count, window_seconds | 3, 3600 |
| C-602 | seconds_after_load | 1800 |
| C-801 | count, window_seconds | 5, 3600 |
| C-802 | points | 5000 |
| C-803 | location_count, window_seconds | 3, 7200 |
| C-804 | count, window_seconds | 10, 86400 |
| C-D03 | count, window_days | 3, 30 |
| C-I03 | amount_cents | 50000 ($500) |
| C-901 | sra_pct_sales_max | 3.0% |

### Sensitivity Presets

Sensitivity levels are defined in `canary/services/alert_config.py` and exposed via `/api/chirp/sensitivity`. They apply a multiplier to numeric threshold fields. Levels: `strict`, `default`, `relaxed`, `minimal`.

### Configuration Templates

Five templates are available via `/api/chirp/templates/apply`: `retail_standard`, `food_service`, `high_value`, `high_volume`, `new_merchant`. Applying a template writes `MerchantRuleConfig` rows for every rule in the catalog and invalidates Valkey caches.

### Valkey Cache Keys

| Pattern | TTL | Content |
|---------|-----|---------|
| `chirp:thresholds:{merchant_id}:{rule_id}` | 300s | JSON threshold dict |
| `chirp:active_rules:{merchant_id}` | 300s | JSON list of all active rules with thresholds |

---

## 7. Security & Compliance

### Rule Severity Classification

| Severity | Score Base | Rules |
|----------|------------|-------|
| critical | 90 | C-104, C-204, C-204, C-301, C-502, C-602, C-D02 |
| high | 70 | C-001, C-002, C-005, C-007, C-009, C-010, C-011, C-101, C-102, C-201, C-202, C-203, C-302, C-303, C-501, C-601, C-802, C-803, C-901, C-D01, C-D03, C-I02, C-I03 |
| medium | 45 | C-003, C-004, C-006, C-008, C-103, C-801, C-804, C-I01 |

### Auto-Escalation

Six rules bypass the standard alert queue and immediately create Fox investigation cases:
- **C-009** SQUARE_DELAY_HOLD — Square's own risk systems have flagged a payment.
- **C-104** AFTER_HOURS_DRAWER — Cash drawer opened outside business hours.
- **C-204** UNTENDERED_ORDER — Order exists with no corresponding payment.
- **C-301** OFF_CLOCK_TRANSACTION — Payment processed without a matching timecard.
- **C-502** POST_VOID_ALERT — Full refund of a completed sale (classic cashier theft pattern).
- **C-602** GIFT_CARD_DRAIN — Gift card fully redeemed immediately after load (laundering signal).

Auto-escalation is best-effort: failure creates a warning log entry but does not prevent the alert from being written.

### Data Access

- All REST endpoints require JWT authentication.
- Rule configuration (`/rules`, `/config`, `/templates`) is limited to `admin` and `owner` roles.
- Batch sweep (`/sweep`) is `admin`-only.
- Alert data is always scoped to `merchant_id` (TenantMixin). No cross-merchant data access is possible through the engine.
- The stateless engine has no authentication: it operates on pre-parsed dict data passed by the TSP pipeline, which owns authentication.

### Notification Toggle

Each `MerchantRuleConfig` row has a `notify_enabled` flag (GRO-254). When `False`, the rule fires and the alert is written, but no notification is dispatched. This prevents alert fatigue without disabling detection.

---

## 8. Error Handling

**Rule checker failures are isolated.** Each rule checker is wrapped in a try/except. A failure in one rule (e.g., a missing column, a DB error) logs an error and continues. The engine never stops evaluation due to a single rule failure.

**Alert write failures are isolated.** Each alert INSERT is wrapped in try/except. If one alert fails to write, the engine continues with the remaining alerts. A flush/commit failure triggers a session rollback and returns 0 written.

**Auto-case failures are non-fatal.** `_auto_create_cases()` is wrapped in a broad except that logs a warning. Fox integration failure never blocks alert creation.

**Notification failures are non-fatal.** `_dispatch_notifications()` uses per-alert try/except. One failed notification does not prevent others.

**Risk update failures are non-fatal.** `schedule_risk_update()` uses per-employee try/except with a session rollback on the failed metrics write. A failed risk update does not prevent alert persistence.

**Threshold loading failures fall back to defaults.** `_load_merchant_thresholds()` uses SAVEPOINT. On SAVEPOINT failure, it logs a warning and continues with catalog defaults and an empty disabled set (all rules active, all at default thresholds).

**Valkey failures are silent.** `ThresholdManager` wraps every Valkey read and write in try/except, logging warnings. A Valkey outage causes a DB fallback, not a service failure.

---

## 9. Testing

Tests are located in `Canary/tests/`. The Chirp engine has coverage across all three test layers.

**Unit tests (`tests/unit/`):**
- `test_rule_definitions.py` — RULE_CATALOG structure, RULE_MAP completeness, tier assignments, default threshold presence.
- `test_stateless_engine.py` — Each Tier 1 checker with boundary cases: hours at exactly open/close, amount at exactly threshold, disabled rules list, empty parsed dict.
- `test_risk_aggregator.py` — Recency weighting, score normalization, category factor computation, empty alert list, dismissed alert exclusion.
- `test_compute_risk_score.py` — Base scores per severity, amount boost tiers, details["score"] override, clamping at 100.

**Integration tests (`tests/integration/` — requires PostgreSQL, `-m postgres`):**
- `test_chirp_rules.py` — Full pipeline: transaction written to canary_sales, engine evaluated, alert and alert_history rows verified in canary_app.
- `test_threshold_manager.py` — Upsert thresholds, cache invalidation, fallback to defaults.
- `test_seed_rules.py` — First-boot seed, idempotency, catalog sync on re-boot.
- `test_auto_case_creation.py` — C-301 and C-502 trigger Fox case creation; non-auto rules do not.

**Smoke tests (`tests/smoke/`):**
- `test_chirp_health.py` — `/api/chirp/categories` returns 200 with expected category list.

---

## 10. Dependencies

### Upstream

| Source | Data | Consumed by |
|--------|------|-------------|
| TSP sub4_detect consumer | Parsed webhook payloads (dict) | `stateless_engine.evaluate_stateless()` |
| TSP sub4_detect consumer | Transaction ORM objects (canary_sales) | `ChirpRuleEngine.evaluate_readonly()` |
| Square Webhooks (via TSP) | `payment.*`, `refund.*`, `order.*`, `cash_drawer.*`, `gift_card.*`, `loyalty.*`, `dispute.*`, `invoice.*` events | TSP delivers parsed payloads and ORM objects |

### Downstream

| Destination | Trigger | Data |
|-------------|---------|------|
| Fox (`FoxCaseService.create_case`) | Alert written for any of the 6 `_AUTO_CASE_RULES` | Alert rule_id, severity, score, category, alert UUID |
| Notification dispatcher (`dispatch_alert_notification`) | Any alert written where `MerchantRuleConfig.notify_enabled` is True | Merchant ID, alert dict |
| `Employee.risk_score` (canary_app) | Any alert written with an employee_id | New recency-weighted risk score |
| `EntityRiskScore` (metrics schema) | Any alert written with an employee_id | Risk score, category, factor breakdown |
| `RiskScoreHistory` (metrics schema) | Any alert written with an employee_id | Timestamped score record |

### Shared Infrastructure

| Service | Usage |
|---------|-------|
| PostgreSQL 17 (`canary` database) | `app` schema: `detection_rules`, `merchant_rule_config`, `alerts`, `alert_history`, `employees`, `locations`. `sales` schema: `transactions`, `cash_drawer_shifts`, `refund_links`, `gift_card_activities`, `loyalty_events`, `disputes`, `invoices`. `metrics` schema: `entity_risk_scores`, `risk_score_history`, `period_metrics`. |
| Valkey 8 (DB 0) | Threshold cache. Keys: `chirp:thresholds:{merchant_id}:{rule_id}`, `chirp:active_rules:{merchant_id}`. TTL: 300s. Optional — all reads fall back to DB on Valkey unavailability. |

---

## 11. Known Issues & Reconciliation

**GRO-263 — Card risk scoring gated.**
`update_card_risk()` returns 0.0 for all card entities. The root cause is that `Alert` has no `card_fingerprint` column. The previous implementation queried `Alert.details.contains(fingerprint)` which caused false positives via substring matching and cannot use indexes. Until GRO-263 adds a `card_fingerprint` column to `alerts` and wires in card-specific rules, card risk scoring is disabled. `EntityRiskScore` and `RiskScoreHistory` rows are written at 0.0.

**C-502 vs C-001 overlap.**
Both C-001 (RAPID_REFUND, threshold 900s) and C-502 (POST_VOID_ALERT, WATCH tier up to 900s) can fire on the same refund event. C-001 fires based on the sale-to-refund time window alone; C-502 also fires but additionally checks for full refund amount and classifies by tier. A refund at 8 minutes by the same employee on a full-amount RETURN can produce both a C-001 alert and a C-502 WATCH alert. This is intentional — C-001 is a volume signal, C-502 is a pattern signal.

**C-004 duplicate in stateless and full engine.**
C-004 (AFTER_HOURS_TRANSACTION) is implemented in both `stateless_engine.py` (Tier 1) and `rule_engine.py` `_check_payment_rules`. The TSP pipeline should invoke only one. The stateless engine fires first from the raw payload; the full engine fires from the ORM object. If both paths run on the same transaction event, a duplicate alert will be written. The TSP Sub4 consumer is responsible for deduplication.

**C-501 void type scope.**
C-501 (HIGH_VOID_RATE) counts `VOID` and `POST_VOID` transaction types per GRO-257 (CANCEL was removed as a canonical type). If historical data contains CANCEL-type transactions, they are not counted toward C-501. This is correct behavior for new data; a one-time backfill migration may be warranted for historical analysis.

**Batch sweep does not debounce.**
`evaluate_batch()` re-evaluates all transactions in the time window without checking for existing alerts. Running the sweep twice within the same window will produce duplicate alerts for the same transactions. The sweep endpoint is intended to be called once per window, not re-run. A deduplication guard (checking for existing alert with same `rule_id` + `source_id`) is not yet implemented.

**Rule guide coverage.**
`RULE_GUIDES` covers 8 of the 37 rules: C-502, C-301, C-004, C-007, C-001, C-005, C-101, C-102. The remaining 29 rules have no plain-language guide. Guides for C-009, C-104, C-204, C-301, and the dispute/invoice rules are the highest-priority additions given their auto-escalation or critical severity.
