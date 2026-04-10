# Analytics

## Overview

Analytics is Canary's read-heavy metrics domain. It owns the `canary_metrics` star schema (20 tables), dashboard orchestration, heatmap scoring, velocity anomaly detection, period aggregation, and fiscal calendar computation. The domain answers "how is this merchant doing?" by combining pre-computed KPI aggregates with statistical scoring engines.

**Architecture:** Three collaborating layers — (1) a pure-logic dashboard orchestrator (`dashboard.py`) that never touches the database, (2) a DB-to-dict bridge (`dashboard_queries.py`) that fetches and shapes PostgreSQL data, and (3) two scoring engines (`heatmap_scoring.py` for band classification, `velocity_engine.py` for z-score anomaly detection) that operate as pure functions on pre-loaded data.

**Metric Registry:** One canonical list of 30+ KPIs derived from Square's 11 data domains. All systems (dashboard, Chirp, heatmap, Owl) reference metrics by the same `metric_name` key. Tier 1 (11 summary card metrics): GROSS_SALES, TRANSACTION_COUNT, REFUND_COUNT, REFUND_RATE, VOID_COUNT, VOID_RATE, NO_SALE_COUNT, CASH_VARIANCE, DISCOUNT_TOTAL, AVG_TRANSACTION, SRA_PCT_SALES. Tier 2 (4 scored, visible on expand): CUSTOM_AMOUNT_COUNT, COUPON_COUNT, ALERT_COUNT, SRA_TOTAL. Tier 3 (15+ tracked, drill-down only): REFUND_AMOUNT, VOID_AMOUNT, NET_SALES, DISCOUNT_RATE, UNIQUE_EMPLOYEES, UNIQUE_CUSTOMERS, PAID_OUT_COUNT, OFF_CLOCK_COUNT, GC_LOAD_COUNT, GC_LOAD_AMOUNT, GC_REDEEM_COUNT, LOYALTY_ADJUSTMENTS, DISPUTE_COUNT, DISPUTE_AMOUNT, INVENTORY_ADJUSTMENTS, SHRINK_UNITS.

**SRA v2 (Shrink Risk Assessment):** Composite loss-exposure indicator. `SRA_TOTAL = abs(refund_amount) + abs(void_total) + abs(cash_variance) + abs(discount_total)`. `SRA_PCT_SALES = (SRA_TOTAL / gross_sales) * 100`. Four components map to Beck & Peacock's Total Retail Loss framework categories.

**Closed-Loop Contract:** Every scored metric has at least one Chirp rule or velocity detection monitoring it. When Chirp fires on metric X, the dashboard shows metric X in a non-normal band. The merchant sees both the metric anomaly and the alert.

**Velocity/Heatmap Scoring (SDD-006 cross-reference):** Velocity and heatmap scoring engines are documented primarily in `chirp.md` for their detection aspects. This domain owns the dashboard rendering pipeline that consumes their output: `score_all_metrics()` results render as the color-coded KPI grid, and velocity anomalies feed anomaly_count on the period summary.

### Code Entry Points

| File | Role |
|------|------|
| `canary/services/dashboard.py` | Pure-logic dashboard orchestrator (dataclasses, scoring, serialization) |
| `canary/services/dashboard_queries.py` | DB-to-dict bridge (period actuals, baselines, thresholds, trends) |
| `canary/services/heatmap_scoring.py` | Band classification engine (normal/watch/review/investigate) |
| `canary/services/velocity_engine.py` | Poisson-process z-score anomaly detection |
| `canary/services/period_aggregation.py` | Daily-to-period aggregation with fiscal calendar |
| `canary/services/fiscal_calendar.py` | NRF 4-5-4 fiscal calendar engine |
| `canary/services/analytics/tools.py` | 7 MCP tool definitions for `canary-analytics` server |
| `canary/blueprints/analytics.py` | REST API at `/api/analytics/*` (JWT auth) |
| `canary/blueprints/analytics_mcp.py` | MCP blueprint at `/analytics/*` |

### Key Dependencies

Inbound: Owl reads dashboard data via `get_dashboard_data()`. UI/BFF renders dashboard views. Ops uses velocity engine in health checks.
Outbound: Reads `canary_metrics` star schema (aggregation writes only via scheduled period aggregation). Reads `canary_app` for employee/location names and alert counts. No outbound writes to other domains.


## API Contracts

### REST Endpoints (`analytics.py` at `/api/analytics/*`)

All endpoints require JWT authentication and are merchant-scoped via `g.merchant_id`.

| Endpoint | Method | Drill-Down Level | Purpose |
|----------|--------|-----------------|---------|
| `/api/analytics/dashboard` | GET | L1: Period Summary | Health score, scored KPI bands, anomaly count, top concern, alert summary |
| `/api/analytics/trends` | GET | L1 (temporal) | Sparkline data for a single metric across periods. Query: `?metric=REFUND_RATE` |
| `/api/analytics/top-risks` | GET | L2-3 | Top 5 employees and top 5 locations ranked by aggregate risk score |
| `/api/analytics/drilldown` | GET | L3-4 | Entity detail. Query: `?entity_type=employee&entity_id=xxx` |
| `/api/analytics/export` | GET | All | CSV/PDF export (stub, future implementation) |

### MCP Tools (`canary-analytics` server, 7 tools)

MCP blueprint at `/analytics/*` via `analytics_mcp.py`. All tools registered in `canary/services/analytics/tools.py`.

| Tool Name | Category | DB? | Purpose |
|-----------|----------|-----|---------|
| `get_dashboard` | dashboard | Yes | Period summary — health score (0-100), scored KPI bands, anomaly count, top concern |
| `get_top_risks` | dashboard | Yes | Top 5 employees and locations ranked by aggregate band penalties |
| `get_trends` | dashboard | Yes | Sparkline data for one metric across N periods (1-13). Params: metric, num_periods |
| `get_drilldown` | dashboard | Yes | All scored metrics for a single employee or location |
| `get_period_metrics` | metrics | Yes | Raw KPI actuals for a fiscal period (unscored). Params: fiscal_year, fiscal_period |
| `score_metrics` | scoring | No | Pure: score actuals dict against baselines dict through heatmap engine |
| `detect_velocity` | scoring | No | Pure: z-score anomaly detection from current_value + historical_values array |

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

The dashboard provides a 5-level drill-down from aggregate period metrics to individual transactions, terminating at RaaS GUID evidence references.

| Level | Source | Description |
|-------|--------|-------------|
| L1 | `PeriodMetrics` (aggregate) | Merchant-wide metrics for a fiscal period |
| L2 | `PeriodMetrics` WHERE location_id | Same metrics split by location |
| L3 | `EmployeePeriodMetrics` WHERE location_id | Per-employee metrics within a location |
| L4 | `DailyMetrics` / `EmployeeDailyMetrics` | Per-day metrics for a specific entity |
| L5 | `transactions` WHERE date + entity | Individual transactions. Evidence: `raas:{merchant_id}:{source_table}:{source_id}` |

### Serialization Functions

| Function | Input | Output |
|----------|-------|--------|
| `serialize_period_summary(PeriodSummary)` | PeriodSummary | dict (JSON-safe) |
| `serialize_trend(List[TrendPoint])` | list of TrendPoint | list of dicts |
| `serialize_top_risks(Dict)` | RiskEntity dict | dict of lists |

All serializers round floats to 1 decimal place.


## Data Model

All Analytics-owned tables live in the `metrics` schema (`canary_metrics`). 20 tables organized as star schema: 6 fact tables, 3 dimension tables, 3 ML feature store tables, 2 risk scoring tables, 2 baseline tables, 2 scorecard tables, and 2 derived scorecard tables.

### Fact Tables (6)

**`daily_metrics`** — Primary grain: merchant x location x date. 18 metric columns. Key columns: `transaction_count`, `gross_sales_cents`, `refund_count`, `refund_amount_cents`, `void_count`, `void_total_cents`, `no_sale_count`, `cash_variance_cents`, `discount_total_cents`, `custom_amount_count`, `coupon_count`, `tip_total_cents`, `unique_customers`, `unique_employees`, `alert_count`. UNIQUE index on `(merchant_id, location_id, metric_date)`.

**`hourly_metrics`** — Grain: merchant x location x date x hour (0-23). Subset of daily columns: `transaction_count`, `total_sales_cents`, `refund_count`, `void_count`, `alert_count`. Used for intraday pattern analysis and velocity profiling.

**`period_metrics`** — Grain: merchant x location x fiscal period. Aggregated from `daily_metrics` by `period_aggregation.py`. Includes fiscal coordinates (`fiscal_year`, `fiscal_quarter`, `fiscal_period`, `period_start_date`, `period_end_date`, `days_in_period`) plus SRA columns (`sra_total_cents`, `sra_pct_sales`). `fiscal_period` range: 1-13 (NRF 4-5-4) or 1-12 (calendar month). UNIQUE index on `(merchant_id, location_id, fiscal_year, fiscal_period)`.

**`employee_daily_metrics`** — Per-employee daily. Adds `employee_id` and `risk_score_snapshot` (Float, point-in-time) to daily_metrics columns.

**`employee_period_metrics`** — Per-employee period. Adds `employee_id`, `off_clock_days`, `avg_risk_score`, `max_risk_score` to period columns.

**`product_daily_metrics`** — Per-product daily: `catalog_object_id`, `item_name`, `units_sold`, `revenue_cents`, `discount_cents`, `void_count`, `return_count`.

### Dimension Tables (3)

**`dim_date`** — PK: `date_key` (Date). Calendar attributes: `day_of_week`, `day_name`, `week_of_year`, `month`, `quarter`, `year`. Fiscal attributes: `fiscal_year`, `fiscal_week_of_year`, `fiscal_day_of_week`. Flags: `is_weekend`, `is_holiday`. Note: `fiscal_period` is NOT stored — computed at query time via `get_fiscal_period(fiscal_week, pattern)` because the pattern is merchant-configurable. Backfilled by `fiscal_calendar.backfill_dim_date()`.

**`dim_location`** — SCD Type 2. Location attributes mirrored at measurement time.

**`dim_employee`** — SCD Type 2. Employee attributes mirrored at measurement time.

### ML Feature Store (3)

**`transaction_features`** — Per-transaction feature vectors: `transaction_id`, `feature_vector` (JSON text), `model_id`, `computed_at`.
**`feature_definitions`** — Feature catalog with computation metadata.
**`ml_models`** — Model registry: version, accuracy, deployment state.

### Risk Scoring (2)

**`entity_risk_scores`** — Current risk per entity (merchant/employee/location/card): `risk_score` (0.0-1.0), `risk_band` (low/medium/high/critical), `contributing_factors` (JSON).
**`risk_score_history`** — Risk score timeline for trend analysis.

### Baselines (2)

**`metric_baselines`** — Statistical baselines (mean, stddev, percentiles) from historical data. Used by Chirp and dashboard. Queried via `dashboard_queries.fetch_baselines()`.
**`velocity_baselines`** — Rate-of-change baselines for velocity engine.

### Scorecards (2)

**`scorecard_thresholds`** — Per-merchant, per-metric threshold config: `metric_name`, `normal_upper_pct`, `watch_upper_pct`, `review_upper_pct`, `direction` (higher_is_worse/lower_is_worse), `is_active`. Seeded on onboarding via `seed_default_thresholds()`. 15 default metrics.
**`dashboard_config`** — Per-merchant dashboard config. Seeded via `seed_default_dashboard_config()`.

### Derived Scorecards (2)

**`weekly_scorecards`** — Weekly aggregated scorecard snapshots.
**`monthly_scorecards`** — Monthly aggregated scorecard snapshots.

### All Amounts in Cents

All monetary columns use `BigInteger` storing cents (divide by 100 for dollars). `dashboard_queries.py` performs the conversion when building metric dicts.


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

Returns `PeriodAggResult(merchant_id, fiscal_year, periods_created, employee_periods_created, pattern)`. Uses `session.flush()` not `session.commit()` — caller controls the transaction boundary.

### Fiscal Calendar Engine

Two calendar modes configured per merchant via `MerchantSettings.calendar_type`:

| Calendar Type | Who Uses It | Periods/Year | Period Labels |
|--------------|-------------|-------------|---------------|
| `nrf_454` (default) | Multi-location retail, chains | 13 (52-53 weeks) | P1-P13, FY2026 |
| `calendar_month` | Small cafes, single-location | 12 | January 2026 |

NRF parameters: `anchor_month` (default 2/Feb), `week_start_day` (default 6/Sunday), `fiscal_pattern` (default 4,5,4 — must sum to 13). `FiscalCalendar.fiscal_year_start(fy)` computes the nearest `week_start_day` to 1st of `anchor_month`. Week 53 maps to Q4 period 3 (last period absorbs extra week).

### Dashboard Build Pipeline

```
1. get_current_fiscal_period(session, merchant_id)
   -> Most recent period_metrics row, or estimate from calendar date
2. fetch_period_actuals(session, merchant_id, fy, fp)
   -> Aggregates across locations: sums counts/amounts, max for unique entities
   -> Computes derived: REFUND_RATE, VOID_RATE, AVG_TRANSACTION, SRA_PCT_SALES
3. fetch_baselines(session, merchant_id) -> {metric_name: baseline_value}
4. fetch_thresholds(session, merchant_id) -> {metric_name: threshold_dict}
   -> Falls back to DEFAULT_THRESHOLDS (15 metrics) if none configured
5. build_period_summary(actuals, baselines, thresholds, fy, fp)
   -> score_all_metrics() — heatmap scoring, sorted by severity
   -> Filter to SUMMARY_METRICS (11 Tier 1 metrics)
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

Score = max(0, 100 - sum_of_penalties). Top concern: investigate > review > watch; within same band, highest `pct_of_baseline` wins.

### Risk Entity Scoring

Each entity's risk score = sum of band penalties across all its metrics. Worst metric identified by highest penalty. Entities sorted descending, top N returned (default 5). `build_top_risks()` produces parallel employee and location rankings.

### Heatmap Scoring Engine

`score_metric(metric_name, actual, baseline, thresholds)` classifies into bands:
- **higher_is_worse** (13 metrics): normal < 100%, watch 100-110%, review 110-120%, investigate > 120%
- **lower_is_worse** (2 metrics: GROSS_SALES, TRANSACTION_COUNT): normal >= 100%, watch 90-100%, review 80-90%, investigate < 80%
- Zero baseline: investigate if actual > 0 and higher_is_worse, else normal
- `score_all_metrics()` returns results sorted by severity (investigate first)
- `seed_default_thresholds()` creates 15 `ScorecardThreshold` rows on merchant onboarding (idempotent)

### Velocity Anomaly Detection

`compute_baseline(historical_values)` computes mean, std_dev (sample variance, n-1), min, max. Reliable if sample_count >= 7. `detect_anomaly(current_value, baseline, sigma=2.0, direction="both")` classifies:
- **spike** — z_score > sigma_threshold (value above baseline)
- **drop** — z_score < -sigma_threshold (value below baseline)
- **zero** — current=0 when baseline.mean > 0
- **none** — within normal range

Confidence scaling: <7 samples=0.0, 7-13=0.5, 14-29=0.7, 30-59=0.85, 60+=0.95. Direction filter: "both" (default), "higher" (spikes only), "lower" (drops only). `VelocityProfile` supports time-aware baselines: hourly > daily > overall fallback via `get_best_baseline()`. `check_velocities()` batch-checks multiple metrics, returning only anomalous results.

### Closed-Loop Alert Flow

```
Metric X crosses threshold
  |
  +-> Heatmap band = review/investigate (dashboard shows red/orange)
  +-> Chirp rule for metric X fires (alert created with severity)
  |
  v
Dashboard shows:
  - Metric X card in non-normal band
  - Alert count incremented
  - Employee/location risk score updated
  |
  v
Merchant sees BOTH the metric anomaly AND the alert
  -> One-tap action: resolve / dismiss / open case
  -> Action logged, alert_count decremented next period
```

### Error Handling

- Empty metrics: `build_period_summary()` with empty actuals returns health_score=100.0, empty metrics list
- Missing baselines: `score_metric()` handles zero baselines gracefully (pct_of_baseline=None)
- Invalid fiscal calendar: `FiscalCalendar` raises `ValueError` for out-of-range anchor_month or week_start_day; pattern must sum to 13
- Period aggregation failures: flush-based (caller controls transaction); empty daily data returns periods_created=0
- Unreliable velocity baseline: `detect_anomaly()` returns is_anomaly=False, confidence=0.0
- Zero std_dev with deviation: returns infinite z-score, classified as anomaly
