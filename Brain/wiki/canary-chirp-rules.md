---
date: 2026-04-23
type: wiki
tags: [canary, chirp, rules, detection, thresholds, alerts, risk-scoring]
sources:
  - Canary/docs/sdds/v2/chirp.md
  - Canary/canary/services/chirp/
  - Canary/canary/blueprints/chirp_wired.py
  - Canary/canary/blueprints/chirp_mcp.py
last-compiled: 2026-04-23
needs-review: 2026-05-07
method-role: Writer
method-stage: close
---

# Canary Chirp Rules

## Summary

Chirp is Canary's rule engine. It takes a parsed Square transaction (or cash drawer shift, gift card activity, loyalty event), runs it against a catalog of frozen detection rules, scores any violations, and writes alerts to the `app` schema. The rules are tiered by how much data they need — stateless rules run on the webhook payload alone, lightweight rules read Valkey counters, full rules query PostgreSQL. Merchants override thresholds; the engine never mutates the rule catalog or the source transaction.

## What it does

Chirp answers one question for every event: "does this look wrong?" If yes, it writes an `Alert` row, a risk score, and — for six critical rules — an auto-created Fox case. The rule catalog is the single source of truth for what can fire. Merchants tune sensitivity but cannot redefine what a rule checks. Evaluation is deterministic: same event, same thresholds, same alerts.

The engine is designed to be cheap to run in-line with webhook processing. Tier 1 rules fire from the HTTP handler itself (fire-and-forget, non-blocking). Tier 2 and Tier 3 rules run in the Sub4 consumer after the transaction is written to `canary_sales`.

## How it works

### The three tiers

Rules are classified by what they need to read to decide.

**Tier 1 — stateless.** Pure functions over a single webhook payload. No database, no cache, no lookups. `stateless_engine.py` runs these six rules: C-004 (after-hours transaction), C-007 (high-value refund), C-009 (Square delay hold), C-010 (partial authorization), C-011 (no-sale detected), C-502 (post-void). These are the only rules that can fire from the TSP HTTP handler without adding latency.

**Tier 2 — lightweight.** Valkey-backed sliding-window counters. Nine rules. They need to see patterns across multiple events but don't need historical database queries. Examples: per-employee refund ratio (C-002), card fingerprint frequency (C-005), cross-location loyalty velocity (C-803).

**Tier 3 — full.** SQLAlchemy queries against `canary_sales`. Fourteen rules. These cross-reference transactions with timecards, orders with payments, and shifts with employee attribution. Most expensive but most powerful. Examples: rapid refund with original sale lookup (C-001), off-clock transaction with timecard join (C-301), untendered order scan (C-204).

`ChirpRuleEngine` (in `rule_engine.py`) handles Tier 2 and Tier 3 and requires a SQLAlchemy session. `stateless_engine.py` handles Tier 1 only and takes no session.

### The rule catalog

`rule_definitions.py` holds 29 `ChirpRuleDefinition` frozen dataclasses, organized into eight categories:

| Category | IDs | Count | Role |
|---|---|---|---|
| payment | C-001 through C-011 | 11 | Core LP signals: refund abuse, structuring, card velocity, manual entry, Square-computed flags |
| cash_drawer | C-101 through C-104 | 4 | No-sale abuse, variance, paid-out anomalies, after-hours drawer access |
| order | C-201 through C-204 | 4 | Sweethearting: discounts, line item voids, unapproved discounts, untendered orders |
| timecard | C-301 through C-303 | 3 | Off-clock transactions, break-time rings, wrong-location clock-ins |
| void | C-501, C-502 | 2 | High void rate, post-void (completed → canceled) |
| gift_card | C-601, C-602 | 2 | Load velocity, full drain |
| loyalty | C-801 through C-804 | 4 | Point accumulation, bulk redemption, cross-location velocity, enrollment fraud |

Each rule carries an ID, name, description, category, default thresholds (JSON), severity (`low`/`medium`/`high`/`critical`), and a tier classification. The catalog is seeded into the `detection_rules` table on first boot but the code is the authority — rows in the table are a convenience for admin UIs, not the source of truth.

The user-facing [[canary-alerts-guide|Canary Alerts Guide]] references additional rule IDs (dispute and invoice families, for example). Those live in related rule sets evaluated alongside Chirp; the Chirp catalog itself is the 29 rules in `rule_definitions.py`.

### Threshold resolution

Every rule has default thresholds. Merchants can override any of them. `ThresholdManager` resolves the effective threshold for a given rule and merchant with a three-layer lookup:

1. Valkey cache at `chirp:thresholds:{merchant_id}:{rule_id}` (TTL 300s)
2. `merchant_rule_config` row in `canary_app`
3. Catalog default from `ChirpRuleDefinition.default_thresholds`

A separate key, `chirp:active_rules:{merchant_id}`, caches the enabled-rule set for bulk lookups. Writes invalidate both.

The `merchant_rule_config` table has two tuning fields: `is_enabled` (whether the rule fires at all for this merchant) and `custom_threshold` (JSON overriding the default). Writes are upserts keyed on `(merchant_id, rule_id)`.

### Sensitivity presets and templates

Merchants rarely tune rules one at a time. Two higher-level controls compose into per-rule thresholds:

**Sensitivity presets** (`strict`, `default`, `relaxed`, `minimal`) are multipliers applied across the catalog. Strict lowers thresholds (more alerts). Relaxed raises them.

**Templates** are industry profiles (`retail_standard`, `food_service`, `high_value`, `high_volume`, `new_merchant`) that set thresholds and enable/disable flags for specific rule subsets.

Both are applied by `apply_template` or `apply_sensitivity`, which write `merchant_rule_config` rows. The previewing tools (`preview`, `estimate_sensitivity`, `validate_thresholds`) are pure — they never write. Validation catches bad field names, out-of-range values, and flags extremes that would produce alert floods.

### Real-time evaluation

The path from webhook to alert:

1. Square POSTs a webhook. TSP Sub1 seals it, Sub2 parses it, Sub2 publishes a `canary:detection` message.
2. Sub4 reads the detection message, loads the transaction from `canary_sales`, and calls `ChirpRuleEngine.evaluate_transaction(txn_id, merchant_id)`.
3. The engine calls `_load_merchant_thresholds()` once via `ThresholdManager`, then dispatches to category-specific checkers (`_check_payment_rules`, `_check_cash_drawer_rules`, etc.).
4. Each checker is wrapped in try/except — one rule failing never blocks the others.
5. `_write_alerts()` inserts `Alert` rows (status=`new`) and `AlertHistory` rows into `canary_app`.
6. `_auto_create_cases()` opens Fox cases for six critical rules (C-009, C-104, C-204, C-301, C-502, C-602). This is best-effort; case creation failures log a warning but never block the alert pipeline.

Tier 1 rules also run from the TSP HTTP handler itself (non-blocking, GRO-128) so the stateless signals surface before the transaction is even parsed into the CDM.

### Risk scoring

`compute_risk_score()` produces a 0-100 integer from three inputs:

- Severity base: `critical=90`, `high=70`, `medium=45`, `low=20`, `info=10`
- Amount boost: +5 for over $100, +10 for over $500, +15 for over $1000
- Rule-specific override: if the rule set `details["score"]`, it blends 60/40 with the base
- Result clamped to [0, 100]

This is per-alert. Entity-level risk — "how risky is this employee?" — is aggregated by the Risk Aggregator service.

### Entity risk aggregation

The Risk Aggregator (`risk_aggregator.py`, GRO-247) rolls per-alert scores up to employee and card profiles. It converts the 0-100 alert scores into a 0.0-1.0 float via recency-weighted averaging:

| Alert age | Weight |
|---|---|
| Within 24h | 3.0x |
| 1-7 days | 2.0x |
| 7-30 days | 1.0x |
| Over 30 days | 0.5x |

Normalization is `total_weighted_score / (alert_count * max_weight)`, so recent alerts carry full score and old alerts damp to one-sixth. The aggregator queries `Alert` and `AlertHistory` (excluding dismissed and false-positive via latest-status subquery), writes `EntityRiskScore` (SCD Type 1) and `RiskScoreHistory` (append-only audit) in the `metrics` schema, and updates the denormalized `Employee.risk_score` in `app`.

Score categories: `<0.3` low, `0.3-0.6` medium, `0.6-0.8` high, `≥0.8` critical.

Card risk scoring is gated until `Alert.card_fingerprint` is a first-class column (GRO-263). The previous implementation used `details.contains()` substring matching, produced false positives, and couldn't use indexes.

### Velocity and heatmap scoring

Two statistical engines sit adjacent to Chirp and contribute to the same dashboards. The velocity engine models event arrival as a Poisson process and runs z-score analysis against rolling baselines. The heatmap engine classifies 15 KPIs into score bands (normal/watch/review/investigate) for the dashboard grid. Both are pure functions, no database. Full detail lives in the analytics SDD; they are cross-referenced here because many scored metrics map directly to Chirp rule IDs (REFUND_RATE → C-002, VOID_COUNT → C-501, and so on).

### Batch sweep

`POST /api/chirp/sweep` triggers batch evaluation. Admin-only. Takes a `since_minutes` window (default 60), queries all transactions in that window for the merchant, calls `evaluate_transaction()` on each, and runs the batch-only C-204 (untendered orders) scan. Used hourly for catch-up and for rules that need to see a closed window rather than a single event.

### Error handling

Every checker is wrapped. `_write_alerts()` catches per-alert write failures and continues. `_load_merchant_thresholds()` uses `begin_nested()` (SAVEPOINT) for cross-database safety, falling back to catalog defaults if the threshold query errors. All `ThresholdManager` Valkey operations are try/except guarded — cache misses silently fall through to the database. `_auto_create_cases()` is entirely best-effort.

## Key decisions

**Frozen rule catalog.** Rules are dataclasses with `frozen=True`. The catalog is code, not config. Adding a rule is a code change with tests, not a database write. This keeps the catalog reviewable, diffable, and immune to runtime drift.

**Tiering by data need.** Splitting rules into three tiers means the cheap rules stay cheap. The Tier 1 engine has no SQLAlchemy dependency at all, which is what makes fire-and-forget evaluation from the HTTP handler viable. Engineers can look at any rule and know immediately what it costs to run.

**One engine per rule, one session per consumer.** The engine doesn't parallelize rule evaluation. It runs the checkers serially within a single SQLAlchemy session. Parallelism lives at the consumer level — scale Sub4 horizontally, not rule evaluation within it.

**Dual-database sessions.** Sub4 reads from `canary_sales` and writes to `canary_app`. The engine takes two sessions explicitly rather than routing through a session manager. This keeps the read/write boundary visible and reviewable.

**Best-effort auto-casing.** Fox case creation happens after the alert commits. If it fails, the alert still exists. This means an investigator always has the alert to act on even when the Fox service is degraded.

**Validation before apply.** The threshold preview/validate tools are pure. They check field names, ranges, and flag extremes before any database write. This pairs with the MCP surface — an agent can propose thresholds, check them, and only then apply.

**MCP surface is mostly pure.** Nine of the ten Chirp MCP tools touch no database. They operate on the catalog, compute sensitivity adjustments, and validate thresholds. Only `get_merchant_thresholds` reads from the database. This keeps the agent-facing surface fast and safe.

## Code pointers

- [canary/services/chirp/rule_definitions.py](../../Canary/canary/services/chirp/rule_definitions.py) — Frozen catalog of 29 rules, lookup helpers (`RULE_MAP`, `get_rule`, `get_rules_by_category`, `get_rules_by_tier`)
- [canary/services/chirp/stateless_engine.py](../../Canary/canary/services/chirp/stateless_engine.py) — Tier 1 pure-function evaluation, no ORM
- [canary/services/chirp/rule_engine.py](../../Canary/canary/services/chirp/rule_engine.py) — `ChirpRuleEngine` class, Tier 2 and Tier 3, category dispatchers, alert writes, auto-case hook
- [canary/services/chirp/threshold_manager.py](../../Canary/canary/services/chirp/threshold_manager.py) — Three-layer threshold resolution, cache invalidation
- [canary/services/chirp/tools.py](../../Canary/canary/services/chirp/tools.py) — 10 MCP tool definitions
- [canary/services/chirp/risk_aggregator.py](../../Canary/canary/services/chirp/risk_aggregator.py) — Entity-level recency-weighted risk aggregation
- [canary/services/alert_config.py](../../Canary/canary/services/alert_config.py) — Sensitivity presets, templates, validation
- [canary/blueprints/chirp_wired.py](../../Canary/canary/blueprints/chirp_wired.py) — REST API at `/api/chirp/*`, JWT + admin/owner gated
- [canary/blueprints/chirp_mcp.py](../../Canary/canary/blueprints/chirp_mcp.py) — MCP blueprint at `/chirp/*`

## Related

- [[canary-detection|Canary Detection Engine]] — Architecture overview (complementary to this rules-focused deep dive)
- [[canary-alerts-guide|Canary Alerts Guide]] — Merchant-facing plain-English reference for every rule
- [[canary-tsp-pipeline|Canary TSP Pipeline]] — How transactions reach Chirp (Sub4)
- [[canary-fox-case-management|Canary Fox Case Management]] — What auto-case creation hands off to
- [[canary-data-model|Canary Data Model]] — `detection_rules`, `merchant_rule_config`, `alerts`, `alert_history`
- [[Brain/projects/Canary|Canary MOC]]

## Sources

- `Canary/docs/sdds/v2/chirp.md` — Source SDD (design authority)
- `Canary/canary/services/chirp/` — Implementation (code authority)
- `Canary/canary/blueprints/chirp_wired.py`, `chirp_mcp.py` — HTTP and MCP surfaces
