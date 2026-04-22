# Analytics (KPI Dashboard + Velocity Engine)

**Type:** App Service (Canary)
**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]
**Architecture:** [[docs/sdds/canary/architecture|Canary Architecture SDD]]
**Linear:** GRO-144, GRO-146, GRO-147, GRO-139, GRO-174, GRO-176, GRO-236, GRO-277
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[Canary/docs/profiles/ops/Tom|Tom]] + [[Canary/docs/profiles/ops/Research|Research]] · **Operator role:** [[Canary/docs/profiles/ops/Jeremy|Jeremy]]

## Purpose

Analytics is Canary's read-heavy metrics domain. It owns the KPI dashboard
orchestration, heatmap band scoring, velocity anomaly detection, period
aggregation (NRF 4-5-4 fiscal calendar), and risk entity ranking. The domain
answers "how is this merchant doing?" by combining pre-computed period
aggregates with two statistical scoring engines (heatmap + velocity).

## Dependencies

| Dependency | Type | Required |
|------------|------|----------|
| PostgreSQL (`canary` DB, `metrics` schema) | Database | Yes |
| `canary_app` schema (employees, locations, alerts) | Database | Yes (name lookups, alert counts) |
| Valkey (DB 0) | Cache | No (no caching implemented) |
| Chirp (detection engine) | Service | No (consumes Chirp output via alert_count columns) |
| Alert Lifecycle (`alert_lifecycle.py`) | Service | Yes (lifecycle_summary for dashboard) |
| MCP SDK (`canary.mcp`) | Library | Yes (MCP tool registration) |

**No external API dependencies.** Analytics is entirely internal — it reads from
`canary_metrics` and `canary_app` and serves data to REST endpoints, MCP tools,
and the Owl AI analysis engine.

## Data Flow & PII Map

### What Enters

| Source | Data | Format |
|--------|------|--------|
| `metrics.period_metrics` | Pre-aggregated KPIs per merchant x location x fiscal period | SQLAlchemy rows |
| `metrics.employee_period_metrics` | Per-employee KPIs per fiscal period | SQLAlchemy rows |
| `metrics.daily_metrics` | Daily fact rows (consumed by period aggregation) | SQLAlchemy rows |
| `metrics.employee_daily_metrics` | Per-employee daily facts | SQLAlchemy rows |
| `metrics.metric_baselines` | Statistical baselines (mean, stddev) | SQLAlchemy rows |
| `metrics.scorecard_thresholds` | Per-merchant band config | SQLAlchemy rows |
| `app.employees` | Employee name lookups | SQLAlchemy rows |
| `app.locations` | Location name lookups | SQLAlchemy rows |

### What's Stored (Analytics-Owned Tables)

Analytics owns writes to `period_metrics` and `employee_period_metrics` via the
period aggregation pipeline. All other metrics tables are written by upstream
services (TSP sub-consumers, scheduled jobs).

### What Exits

| Consumer | Data | Format |
|----------|------|--------|
| REST API (`/api/analytics/*`) | Dashboard JSON, trends, top risks, drilldown | JSON via Flask |
| MCP Tools (`canary-analytics` server) | Same data shaped for agent consumption | Dict via MCP handler |
| Owl AI Engine | Dashboard payload via `get_dashboard_data()` | Python dict |
| UI/BFF (views_wired.py) | Dashboard rendering data | Python dict |

### PII Classification

| Field | Classification | Location | Encryption | Notes |
|-------|---------------|----------|------------|-------|
| `merchant_id` | internal | All metrics tables | Plaintext | Square merchant ID, tenant key |
| `employee_id` | internal | `employee_period_metrics`, `entity_risk_scores` | Plaintext | Square employee ID |
| `employee_name` | **sensitive** | `app.employees` (read only) | **Plaintext** | Looked up for display in risk rankings |
| `location_id` | internal | All metrics tables | Plaintext | Square location ID |
| `location_name` | internal | `app.locations` (read only) | Plaintext | Looked up for display |
| `entity_id` | internal | `entity_risk_scores` | Plaintext | Could be employee, card, device, location |
| `risk_score` | internal | `entity_risk_scores`, `risk_score_history` | Plaintext | 0.0-1.0 score |
| `contributing_factors` | internal | `entity_risk_scores` | Plaintext | JSON array of factor objects |

**PII exposure path:** Employee names flow from `app.employees` through
`dashboard_queries._get_employee_name()` into the `top-risks` API response and
MCP `get_top_risks` tool output. The name is returned in plaintext JSON to
authenticated callers (JWT-required).

## API Contract

### REST Endpoints (`analytics.py` at `/api/analytics/*`)

All endpoints require JWT authentication and are merchant-scoped via `g.merchant_id`.

| Endpoint | Method | Drill-Down Level | Purpose |
|----------|--------|-----------------|---------|
| `/api/analytics/dashboard` | GET | L1: Period Summary | Health score, scored KPI bands, anomaly count, top concern, alert summary |
| `/api/analytics/trends` | GET | L1 (temporal) | Sparkline data for a single metric across periods. Query: `?metric=REFUND_RATE` |
| `/api/analytics/top-risks` | GET | L2-3 | Top 5 employees and top 5 locations ranked by aggregate risk score |
| `/api/analytics/drilldown` | GET | L3-4 | Entity detail. Query: `?entity_type=employee&entity_id=xxx` |
| `/api/analytics/export` | GET | All | **Stub** — returns 501 Not Implemented |

### MCP Tools (`canary-analytics` server, 7 tools)

MCP blueprint at `/analytics/*` via `analytics_mcp.py`. All tools registered in
`canary/services/analytics/tools.py`.

| Tool Name | Category | DB? | PII Access | Description |
|-----------|----------|-----|------------|-------------|
| `get_dashboard` | dashboard | Yes | merchant_id | Period summary — health score (0-100), scored KPI bands, anomaly count, top concern |
| `get_top_risks` | dashboard | Yes | employee_name, employee_id | Top 5 employees and locations ranked by aggregate band penalties |
| `get_trends` | dashboard | Yes | merchant_id | Sparkline data for one metric across N periods (1-13) |
| `get_drilldown` | dashboard | Yes | employee_id or location_id | All scored metrics for a single employee or location |
| `get_period_metrics` | metrics | Yes | merchant_id | Raw KPI actuals for a fiscal period (unscored) |
| `score_metrics` | scoring | No | None | Pure: score actuals dict against baselines dict through heatmap engine |
| `detect_velocity` | scoring | No | None | Pure: z-score anomaly detection from current_value + historical_values array |

### Dashboard Response Shape (`get_dashboard` / `serialize_period_summary`)

```json
{
  "fiscal_year": 2026, "fiscal_period": 3,
  "period_label": "P3 FY2026",
  "health_score": 75.0,
  "anomaly_count": 2,
  "top_concern": "Refund Rate: investigate (285% of baseline)",
  "alert_summary": {},
  "metrics": [
    {
      "name": "REFUND_RATE", "label": "Refund Rate",
      "actual": 4.2, "baseline": 1.5,
      "pct_of_baseline": 280.0, "band": "investigate",
      "color": "#ef4444", "format": "percent",
      "is_alert_worthy": true
    }
  ]
}
```

### Drill-Down Chain (5 levels)

| Level | Source | Description |
|-------|--------|-------------|
| L1 | `PeriodMetrics` (aggregate) | Merchant-wide metrics for a fiscal period |
| L2 | `PeriodMetrics` WHERE location_id | Same metrics split by location |
| L3 | `EmployeePeriodMetrics` WHERE location_id | Per-employee metrics within a location |
| L4 | `DailyMetrics` / `EmployeeDailyMetrics` | Per-day metrics for a specific entity |
| L5 | `transactions` WHERE date + entity | Individual transactions. Evidence: `raas:{merchant_id}:{source_table}:{source_id}` |

## Data Model

All Analytics-owned tables live in the `metrics` schema (`canary_metrics`). 20
tables organized as star schema.

### Fact Tables (6)

- **`daily_metrics`** — Grain: merchant x location x date. 18+ metric columns.
  UNIQUE on `(merchant_id, location_id, metric_date)`.
- **`hourly_metrics`** — Grain: merchant x location x date x hour (0-23). For
  intraday pattern analysis and velocity profiling.
- **`period_metrics`** — Grain: merchant x location x fiscal period. Aggregated
  from `daily_metrics` by `period_aggregation.py`. Includes SRA columns.
  UNIQUE on `(merchant_id, location_id, fiscal_year, fiscal_period)`.
- **`employee_daily_metrics`** — Per-employee daily. Adds `employee_id`,
  `risk_score_snapshot`, off-clock flags, discount decomposition (GRO-277).
- **`employee_period_metrics`** — Per-employee period. Adds `employee_id`,
  `off_clock_days`, `avg_risk_score`, `max_risk_score`, `sales_per_hour_cents`.
- **`product_daily_metrics`** — Per-product daily: `catalog_object_id`,
  `item_name`, `units_sold`, `revenue_cents`.

### Dimension Tables (3)

- **`dim_date`** — PK: `date_key` (Date). Calendar + fiscal attributes.
  `fiscal_period` computed at query time via `get_fiscal_period()`.
- **`dim_location`** — SCD Type 2. Location attributes mirrored at measurement time.
- **`dim_employee`** — SCD Type 2. Employee attributes mirrored at measurement time.

### Risk & Scoring Tables (4)

- **`entity_risk_scores`** — Current risk per entity (employee/card/device/location):
  `risk_score` (0.0-1.0), `risk_category` (low/medium/high/critical),
  `factors` (JSON). SCD Type 1 (overwritten).
- **`risk_score_history`** — Append-only risk score timeline for trend analysis.
- **`scorecard_thresholds`** — Per-merchant, per-metric threshold config.
  UNIQUE on `(merchant_id, metric_name)`. Seeded by `seed_default_thresholds()`.
  21 default metrics across higher_is_worse and lower_is_worse directions.
- **`dashboard_config`** — Per-merchant dashboard config: layout, refresh
  interval, display toggles. UNIQUE on `merchant_id`.

### Baseline Tables (2)

- **`metric_baselines`** — Statistical baselines (mean, stddev, sample_size)
  per merchant per metric. Used by heatmap scoring and Chirp.
- **`velocity_baselines`** — Rate-of-change baselines for velocity engine.
  Indexed by merchant x metric x day_of_week x hour_of_day.

### ML Feature Store (3)

- **`transaction_features`** — Per-transaction feature vectors with ML risk scores.
- **`feature_definitions`** — Feature catalog with computation metadata.
- **`ml_models`** — Model registry: version, accuracy, deployment state.

### Scorecards (2)

- **`weekly_scorecard`** — Weekly aggregated KPI snapshots (JSON `kpis` column).
- **`monthly_scorecard`** — Monthly aggregated KPI snapshots.

### Monetary Convention

All monetary columns use `BigInteger` storing cents (divide by 100 for dollars).
`dashboard_queries.py` performs the conversion when building metric dicts.

## Workflows

### Period Aggregation Pipeline

```
Square webhooks -> TSP -> canary_sales (write-once facts)
                            |
                            v
         DailyMetrics + EmployeeDailyMetrics (canary_metrics)
                            |
                            v
         aggregate_period_metrics(merchant_id, fiscal_year)
           - Reads MerchantSettings for calendar_type, anchor_month,
             week_start_day, fiscal_pattern
           - DELETE existing period rows for target merchant/year
           - Re-INSERT from daily_metrics (full rebuild pattern)
           - Aggregates both merchant-level and employee-level
           - Computes SRA v2 (4 components)
                            |
                     +------+------+
                     |             |
                     v             v
              PeriodMetrics   EmployeePeriodMetrics
```

Returns `PeriodAggResult(merchant_id, fiscal_year, periods_created,
employee_periods_created, pattern)`. Uses `session.flush()` not
`session.commit()` — caller controls the transaction boundary.

### Dashboard Build Pipeline

```
1. get_current_fiscal_period(session, merchant_id)
   -> Most recent period_metrics row, or estimate from calendar date
2. fetch_period_actuals(session, merchant_id, fy, fp)
   -> Aggregates across locations: sums counts/amounts, max for unique entities
   -> Computes derived: REFUND_RATE, VOID_RATE, AVG_TRANSACTION, SRA_PCT_SALES
3. fetch_baselines(session, merchant_id) -> {metric_name: baseline_value}
4. fetch_thresholds(session, merchant_id) -> {metric_name: threshold_dict}
   -> Falls back to DEFAULT_THRESHOLDS (21 metrics) if none configured
5. build_period_summary(actuals, baselines, thresholds, fy, fp)
   -> score_all_metrics() — heatmap scoring, sorted by severity
   -> Filter to SUMMARY_METRICS (14 metrics including GRO-277 timecard)
   -> _compute_health_score() — 100 minus band penalties
   -> lifecycle_summary() for alert context
   -> _find_top_concern() — worst band, highest pct_of_baseline
6. serialize_period_summary() -> JSON-safe dict
```

### Health Score Algorithm

Health starts at 100 and subtracts penalties per non-normal band:

| Band | Penalty | Color |
|------|---------|-------|
| normal | 0 | #22c55e (green) |
| watch | 5 | #eab308 (yellow) |
| review | 15 | #f97316 (orange) |
| investigate | 30 | #ef4444 (red) |
| insufficient_data | 0 | #94a3b8 (slate) |

Score = max(0, 100 - sum_of_penalties). Min transaction threshold: 20
transactions required for reliable scoring; below this returns
`insufficient_data` band.

### Heatmap Scoring Engine

`score_metric(metric_name, actual, baseline, thresholds)` classifies into bands:
- **higher_is_worse** (19 metrics): normal < 100%, watch 100-110%, review 110-120%, investigate > 120%
- **lower_is_worse** (2 metrics: GROSS_SALES, TRANSACTION_COUNT): inverted thresholds
- Zero baseline: investigate if actual > 0 and higher_is_worse, else normal
- `score_all_metrics()` returns results sorted by severity (investigate first)
- `seed_default_thresholds()` creates 21 `ScorecardThreshold` rows on merchant onboarding (idempotent)

### Velocity Anomaly Detection

Poisson-process z-score detection. `compute_baseline(historical_values)` computes
mean, std_dev (sample variance, n-1), min, max. Reliable if sample_count >= 7.

`detect_anomaly(current_value, baseline, sigma=2.0, direction="both")` classifies:
- **spike** — z_score > sigma_threshold
- **drop** — z_score < -sigma_threshold
- **zero** — current=0 when baseline.mean > 0
- **none** — within normal range

Confidence scaling: <7 samples=0.0, 7-13=0.5, 14-29=0.7, 30-59=0.85, 60+=0.95.

`VelocityProfile` supports time-aware baselines: hourly > daily > overall
fallback via `get_best_baseline()`. `check_velocities()` batch-checks multiple
metrics, returning only anomalous results.

### Fiscal Calendar Engine

Two calendar modes configured per merchant:

| Calendar Type | Periods/Year | Period Labels |
|--------------|-------------|---------------|
| `nrf_454` (default) | 13 (52-53 weeks) | P1-P13, FY2026 |
| `calendar_month` | 12 | January 2026 |

NRF parameters: `anchor_month` (default 2/Feb), `week_start_day` (default
6/Sunday), `fiscal_pattern` (default 4,5,4 — must sum to 13). Week 53 maps to
P13 (last period absorbs extra week). `backfill_dim_date()` updates dim_date
in batches of 500.

### Error Handling

- Empty metrics: `build_period_summary()` with empty actuals returns
  health_score=100.0, empty metrics list
- Missing baselines: `score_metric()` handles zero baselines gracefully
- Invalid fiscal calendar: `FiscalCalendar` raises `ValueError` for
  out-of-range parameters; pattern must sum to 13
- Period aggregation failures: flush-based (caller controls transaction);
  empty daily data returns periods_created=0
- Unreliable velocity baseline: `detect_anomaly()` returns is_anomaly=False,
  confidence=0.0
- Zero std_dev with deviation: returns infinite z-score, classified as anomaly

## Operations

### Startup Sequence

Analytics has no independent startup — it runs within the Canary Flask process
(port 5001). The analytics blueprint is registered during app factory
initialization. The MCP blueprint registers 7 tools via `MCPRegistry`.

### Health Checks

**MCP health endpoint:** `analytics_mcp_bp` includes a health function
(`_analytics_health`) that returns service name, healthy status, and tool count.
Available at the MCP blueprint health route.

**No REST health endpoint.** The `/api/analytics/*` blueprint has no dedicated
health check route. Health is implicitly checked by the main Canary app health
endpoint.

### Failure Modes

| Failure | Impact | Behavior |
|---------|--------|----------|
| PostgreSQL down | Dashboard returns no data | `get_dashboard_data()` returns `None`; API returns empty JSON |
| No period_metrics rows | Dashboard shows empty state | Returns `None` from `fetch_period_actuals()` |
| No baselines configured | All metrics score against zero | `fetch_baselines()` returns `None`, scoring uses 0.0 baseline |
| No thresholds configured | Default thresholds apply | Falls back to `DEFAULT_THRESHOLDS` (21 metrics) |
| Fiscal calendar misconfiguration | `ValueError` raised | Pattern must sum to 13; anchor_month 1-12; week_start_day 0-6 |
| Period aggregation partial failure | Flush-based, caller rolls back | Returns `PeriodAggResult` with periods_created=0 |
| Employee name lookup fails | Shows employee_id instead | `_get_employee_name()` catches all exceptions, returns raw ID |

### Monitoring

**What to alert on:**
- Dashboard API response time > 2s (multiple cross-schema joins)
- Period aggregation produces 0 periods for a merchant with daily data
- Velocity engine confidence consistently at 0.0 (insufficient baseline data)
- Health score drops below 30 across multiple merchants simultaneously

**What's normal:**
- Health scores between 50-100 for active merchants
- 1-3 velocity anomalies per period per merchant
- Period aggregation rebuilds delete and re-insert (not incremental)

### Configuration

| Env Var / Setting | Purpose | Default |
|-------------------|---------|---------|
| `MerchantSettings.calendar_type` | `nrf_454` or `calendar_month` | `nrf_454` |
| `MerchantSettings.anchor_month` | Fiscal year start month | 2 (February) |
| `MerchantSettings.week_start_day` | Week start day | 6 (Sunday) |
| `MerchantSettings.fiscal_pattern` | Period grouping | (4, 5, 4) |
| `ScorecardThreshold` rows | Per-metric band boundaries | 21 defaults seeded |
| `DashboardConfig.refresh_interval_seconds` | Auto-refresh | 300 (5 min) |
| `MIN_TRANSACTION_THRESHOLD` | Min txns for reliable scoring | 20 |
| `DEFAULT_SIGMA_THRESHOLD` | Velocity z-score threshold | 2.0 |
| `DEFAULT_WINDOW_DAYS` | Velocity baseline window | 30 |
| `MIN_SAMPLE_SIZE` | Min data points for velocity baseline | 7 |

## Deployment

### Docker Service Definition

Analytics runs inside the main Canary Flask container. No separate service.

```yaml
# Part of canary-web service in Canary/devops/docker-compose.yml
canary-web:
  image: canary-web
  ports:
    - "5001:5001"
  networks:
    - growdirect
  depends_on:
    - growdirect_postgres
    - growdirect_valkey
```

### AWS Target

- **Compute:** ECS/Fargate — same task as Canary web
- **Database:** RDS PostgreSQL 17 — `canary` database, `metrics` schema
- **Cache:** ElastiCache (Valkey) — currently unused by analytics but available
- **Secrets:** AWS Secrets Manager for DB credentials

### CI/CD Requirements

- Alembic migrations for any metrics schema changes
- Integration tests against `canary_test` database
- Period aggregation smoke test with known daily data

## Code Entry Points

| File | Role |
|------|------|
| `canary/services/dashboard.py` | Pure-logic dashboard orchestrator (dataclasses, scoring, serialization) |
| `canary/services/dashboard_queries.py` | DB-to-dict bridge (period actuals, baselines, thresholds, trends) |
| `canary/services/dashboard_tiles.py` | Tile configuration registry for UI rendering (GRO-236) |
| `canary/services/heatmap_scoring.py` | Band classification engine (normal/watch/review/investigate) |
| `canary/services/velocity_engine.py` | Poisson-process z-score anomaly detection |
| `canary/services/period_aggregation.py` | Daily-to-period aggregation with fiscal calendar |
| `canary/services/fiscal_calendar.py` | NRF 4-5-4 fiscal calendar engine |
| `canary/services/analytics/tools.py` | 7 MCP tool definitions for `canary-analytics` server |
| `canary/blueprints/analytics.py` | REST API at `/api/analytics/*` (JWT auth) |
| `canary/blueprints/analytics_mcp.py` | MCP blueprint at `/analytics/*` |
| `canary/models/metrics/risk.py` | Risk scoring, baseline, threshold, scorecard models |
| `canary/models/metrics/facts.py` | Fact table models (daily, hourly, period, employee) |

## Code Review Findings

### P0 — Blocks Production

**P0-ANA-1: Employee names returned in plaintext through API and MCP tools.**
`dashboard_queries._get_employee_name()` looks up `Employee.employee_name` and
returns it directly in the `top-risks` and `drilldown` API responses. Employee
names are sensitive PII — they should be encrypted at rest in the `employees`
table and only decrypted at the presentation layer for authenticated callers.
The MCP `get_top_risks` and `get_drilldown` tools also surface employee names
without any PII access logging.
**Fix:** Encrypt employee names at rest using the existing `crypto.py` AES-256-GCM
pattern. Add PII access logging when names are decrypted for API responses.

**P0-ANA-2: No tenant isolation enforcement on MCP tools.**
All 5 DB-backed MCP tools accept `merchant_id` as an optional parameter,
falling back to `context.get("merchant_id")`. If the MCP context does not
enforce tenant isolation, a tool caller could pass any `merchant_id` and
access another merchant's dashboard data, risk rankings, and employee names.
The REST API is protected by JWT + `g.merchant_id`, but the MCP path has no
equivalent guard.
**Fix:** MCP tool handlers must validate `merchant_id` against the authenticated
context. Reject requests where `params["merchant_id"]` differs from
`context["merchant_id"]` unless the caller has admin privileges.

**P0-ANA-3: `get_session()` called without context in dashboard orchestrators.**
`get_dashboard_data()` and `get_top_risks_data()` (lines 578-649 in
`dashboard.py`) call `get_session()` directly from a service module, outside
Flask request context. This works in the current single-process dev setup but
creates session lifecycle risks in production (sessions not properly closed,
connection pool exhaustion under load).
**Fix:** Accept `session` as a parameter from the caller (blueprint or MCP
handler) instead of creating sessions internally. This aligns with the
pattern used by all `dashboard_queries.py` functions.

### P1 — Before GA

**P1-ANA-1: No audit logging for risk data access.**
When a user or agent views employee risk rankings (`top-risks`, `drilldown`),
no audit trail is created. For a loss prevention product that surfaces employee
risk scores, this is an operational gap — merchants need to know who viewed
which employee's risk data and when.
**Fix:** Add audit log entries for `get_top_risks`, `get_drilldown` API calls
and MCP tool invocations. Log: timestamp, caller identity, merchant_id,
entity_type, entity_id accessed.

**P1-ANA-2: No rate limiting on analytics endpoints.**
The `/api/analytics/*` endpoints have no rate limiting. Dashboard and trend
endpoints execute multiple DB queries per request (4-5 queries for
`/dashboard`). A malicious or buggy client could overwhelm the database.
**Fix:** Add Flask-Limiter on analytics endpoints. Suggested limits:
`/dashboard` 30/min, `/trends` 60/min, `/top-risks` 30/min,
`/drilldown` 60/min.

**P1-ANA-3: No data retention policy for metrics tables.**
The 20 metrics tables accumulate data indefinitely. `daily_metrics` and
`employee_daily_metrics` grow linearly with merchant activity. No purge,
archival, or partition strategy exists.
**Fix:** Implement retention policy: daily metrics > 24 months archived to cold
storage, period metrics retained indefinitely (aggregates), risk score history
> 24 months pruned. Add partition-by-month on `daily_metrics.metric_date`.

**P1-ANA-4: Dashboard API returns no data status 200 instead of 204/404.**
When `get_dashboard_data()` returns `None` (no metrics exist), the `/dashboard`
endpoint returns `jsonify(None)` with status 200. This makes it impossible for
the client to distinguish "healthy merchant with no data" from "data exists."
**Fix:** Return 204 No Content when no period metrics exist for the merchant.
Return 200 with payload when data exists.

**P1-ANA-5: Export endpoint is a permanent stub.**
`/api/analytics/export` returns 501 Not Implemented. If exposed in production,
it signals incomplete functionality to merchants.
**Fix:** Either implement CSV export (straightforward given existing
serialization functions) or remove the route before GA.

**P1-ANA-6: No caching on dashboard queries.**
Each `/dashboard` request executes 4 sequential database queries
(`get_current_fiscal_period`, `fetch_period_actuals`, `fetch_baselines`,
`fetch_thresholds`). Period metrics change only when aggregation runs
(infrequent). Dashboard data is an ideal caching candidate.
**Fix:** Cache `get_dashboard_data()` results in Valkey (DB 0) with a 60-second
TTL, keyed by `analytics:dashboard:{merchant_id}`. Invalidate on period
aggregation.

### P2 — Post-Launch

**P2-ANA-1: Trend query fetches all locations then aggregates.**
`fetch_trend_periods()` queries `PeriodMetrics` without aggregating across
locations — it returns individual location rows and the caller gets whichever
N rows happen to sort first. For multi-location merchants, trends may show
inconsistent data.
**Fix:** Add GROUP BY or SUM aggregation in `fetch_trend_periods()` for
merchant-level trend data, or pass location_id for location-level trends.

**P2-ANA-2: Health score can go negative in theory.**
`_compute_health_score()` caps at `max(0.0, 100 - total_penalty)`, but if a
merchant has more than ~4 metrics in `investigate` band (4 x 30 = 120 penalty),
health hits 0 and all additional investigate bands are indistinguishable.
Consider a logarithmic or weighted penalty model for extreme cases.

**P2-ANA-3: Period aggregation is full rebuild — no incremental mode.**
`aggregate_period_metrics()` DELETEs all period rows for a fiscal year then
re-inserts from daily data. For large merchants with 12 months of data, this
is O(n) on every run. An incremental mode (aggregate only the current period)
would reduce write amplification.

**P2-ANA-4: `_get_employee_name()` and `_get_location_name()` execute N+1 queries.**
Risk ranking fetches up to 10 employees/locations, then issues one name lookup
query per entity. Should batch lookups into a single IN query.

**P2-ANA-5: SUMMARY_METRICS list hardcoded — not configurable per merchant.**
The 14 metrics shown on the dashboard summary card are hardcoded in
`dashboard.py`. `DashboardConfig` has a `layout` JSON column that could drive
this, but it's not wired.

## Production Readiness Checklist

- [ ] PII encrypted at rest (P0-ANA-1: employee names in `app.employees`)
- [ ] MCP tenant isolation enforced (P0-ANA-2: merchant_id validation)
- [ ] Session management fixed in orchestrators (P0-ANA-3: accept session param)
- [ ] Secrets in AWS Secrets Manager (not .env)
- [ ] Health check endpoint responds (MCP has one; REST needs one)
- [ ] Audit logging for risk data access (P1-ANA-1)
- [ ] Rate limiting on analytics endpoints (P1-ANA-2)
- [ ] Data retention policy implemented (P1-ANA-3)
- [ ] Error responses don't leak internals (verified: errors return generic JSON)
- [ ] Dashboard caching in Valkey (P1-ANA-6)
- [ ] Export endpoint resolved — implement or remove (P1-ANA-5)
