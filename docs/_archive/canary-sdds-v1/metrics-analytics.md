# Metrics & Analytics

> **Status:** Complete — written from code
> **Namespace:** canary
> **Last updated:** 2026-03-30
> **Code location:** `Canary/canary/services/metrics/`, `Canary/canary/services/metrics_etl.py`, `Canary/canary/models/metrics/`

---

## 1. Overview

The Metrics & Analytics system is Canary's analytics data layer. It transforms raw Square sales events (transactions, tenders, line items, timecards, gift cards, loyalty events, disputes, invoices, inventory adjustments, and Chirp alerts) into a star schema optimized for loss-prevention reporting and risk assessment.

The system has three distinct stages:

1. **Dimension loading** — Populates conformed dimension tables (`dim_date`, `dim_location`, `dim_employee`) from app schema sources. Idempotent, run once and refreshed as needed.
2. **Daily ETL** — Aggregates raw sales and event data into granular fact tables (`daily_metrics`, `hourly_metrics`, `employee_daily_metrics`, `product_daily_metrics`). Idempotent over any date range.
3. **Period aggregation** — Rolls daily facts up to NRF 4-5-4 fiscal period fact tables (`period_metrics`, `employee_period_metrics`). Computes SRA (Shrink Risk Assessment) at the period level.

The resulting data feeds:
- The Owl Analytics REST API (`/api/analytics/*`) — period summaries, trend series, top-risk entities, and entity drill-downs
- The Analytics MCP server (`analytics_mcp_bp`) — tool-registry interface for AI-assisted analytics queries
- Employee risk scoring — `risk_score_snapshot` and `EntityRiskScore` are populated inline during the ETL

---

## 2. Architecture

### Component Diagram

```
Square API
    │
    ▼
TSP (Transaction Sync Pipeline)
    │  writes to
    ▼
canary.sales schema
  ├── transactions
  ├── transaction_line_items
  ├── line_item_discounts
  ├── transaction_tenders
  ├── cash_drawer_shifts
  ├── employee_timecards
  ├── gift_card_activities
  ├── loyalty_events
  ├── disputes
  ├── invoices
  └── inventory_adjustments

canary.app schema
  ├── alerts   (Chirp)
  ├── locations
  └── employees

        │
        │  metrics_etl.run_etl()
        ▼
canary.metrics schema
  Dimensions
  ├── dim_date          (conformed calendar, NRF fiscal fields)
  ├── dim_location      (store/location registry)
  └── dim_employee      (employee registry + risk category)

  Daily Fact Tables
  ├── daily_metrics             (merchant × location × day)
  ├── hourly_metrics            (merchant × location × employee × hour)
  ├── employee_daily_metrics    (merchant × employee × location × day)
  └── product_daily_metrics     (merchant × product × location × day)

  Period Fact Tables
  ├── period_metrics            (merchant × location × NRF fiscal period)
  └── employee_period_metrics   (merchant × employee × NRF fiscal period)

  Risk & ML Tables
  ├── transaction_features      (ML feature vectors per transaction)
  ├── feature_definitions       (ML feature catalog)
  ├── ml_models                 (trained model registry)
  ├── entity_risk_scores        (current score per entity — SCD Type 1)
  ├── risk_score_history        (append-only score audit trail)
  └── metric_baselines          (statistical baselines for anomaly detection)

  Scoring & Config Tables
  ├── velocity_baselines        (XPLOSS velocity anomaly detection)
  ├── scorecard_thresholds      (configurable heatmap bands per merchant)
  ├── weekly_scorecard          (week-level KPI JSON snapshots)
  ├── monthly_scorecard         (month-level KPI JSON snapshots)
  └── dashboard_config          (per-merchant dashboard preferences)

        │
        ▼
  Analytics Blueprint   /api/analytics/*
  Analytics MCP         /analytics/*  (tool registry)
```

### Request / Data Flow

**ETL flow (nightly or on-demand):**

```
run_etl(merchant_id, start_date, end_date)
  │
  ├── aggregate_daily_metrics()
  │     ├── DELETE daily_metrics WHERE merchant+range    (idempotent purge)
  │     ├── SELECT transactions → GROUP BY location+date
  │     ├── SELECT cash_drawer_shifts → cash_variance_lookup
  │     ├── SELECT transactions (no line items) → custom_amount_lookup
  │     ├── SELECT tenders → tender_lookup (cash/card/other)
  │     ├── SELECT line_items → basket_lookup
  │     ├── SELECT app.alerts → alert_lookup
  │     ├── SELECT gift_card_activities → gift_card_lookup
  │     ├── SELECT loyalty_events → loyalty_lookup
  │     ├── SELECT disputes → dispute_lookup
  │     ├── SELECT invoices → invoice_lookup
  │     ├── SELECT inventory_adjustments (SHRINKAGE) → shrinkage_lookup
  │     └── INSERT daily_metrics rows
  │
  ├── aggregate_hourly_metrics()
  │     ├── DELETE hourly_metrics WHERE merchant+range
  │     ├── SELECT transactions → GROUP BY location+employee+date+hour
  │     ├── SELECT app.alerts → hourly_alert_lookup
  │     └── INSERT hourly_metrics rows
  │
  ├── aggregate_employee_daily_metrics()
  │     ├── DELETE employee_daily_metrics WHERE merchant+range
  │     ├── SELECT transactions (employee_id NOT NULL) → GROUP BY employee+location+date
  │     ├── SELECT app.alerts (employee scoped) → emp_alert_lookup
  │     ├── SELECT transactions (no line items, employee) → emp_custom_lookup
  │     ├── SELECT employee_timecards → emp_shifts (off-clock detection)
  │     ├── Compute shift_hours_lookup (closed shifts, sum hours by emp+date)
  │     ├── SELECT transactions NOT IN timecard windows → off_clock_lookup
  │     ├── SELECT line_item_discounts → emp_discount_lookup (fixed vs pct)
  │     ├── SELECT gift_card_activities (employee) → emp_gift_card_lookup
  │     ├── SELECT loyalty_events (employee) → emp_loyalty_lookup
  │     ├── SELECT inventory_adjustments SHRINKAGE (employee) → emp_shrinkage_lookup
  │     ├── INSERT employee_daily_metrics rows
  │     └── compute_employee_risk_scores() → write risk_score_snapshot inline
  │
  ├── aggregate_product_daily_metrics()
  │     ├── DELETE product_daily_metrics WHERE merchant+range
  │     ├── SELECT line_items JOIN transactions → GROUP BY product+location+date
  │     └── INSERT product_daily_metrics rows (with return_rate computed inline)
  │
  ├── session.commit()                              (daily facts committed)
  │
  └── aggregate_period_metrics(session, merchant_id, fiscal_year)
        ├── DELETE period_metrics for FY (full rebuild pattern)
        ├── SELECT daily_metrics → GROUP BY NRF fiscal period
        ├── Compute SRA: refund_amount + void_total + cash_variance + discounts
        ├── INSERT period_metrics rows
        ├── DELETE employee_period_metrics for FY
        ├── SELECT employee_daily_metrics → GROUP BY employee + fiscal period
        └── INSERT employee_period_metrics rows

session.commit()
```

**Analytics read flow:**

```
GET /api/analytics/dashboard
  └── jwt_required() → g.merchant_id
        └── get_dashboard_data(merchant_id)
              ├── get_current_fiscal_period()  → (fiscal_year, fiscal_period)
              ├── fetch_period_metrics()        → PeriodMetrics for current period
              ├── fetch_baselines()             → MetricBaseline map
              ├── fetch_thresholds()            → ScorecardThreshold map
              └── score_metrics()              → DashboardMetric list with bands

GET /api/analytics/trends?metric=REFUND_RATE
  └── jwt_required()
        ├── get_current_fiscal_period()
        ├── fetch_trend_periods()  → last 6 periods of metric values
        ├── fetch_baselines()
        └── build_trend_data()    → trend point list with pct_of_baseline

GET /api/analytics/drilldown?entity_type=employee&entity_id=<id>
  └── jwt_required()
        ├── get_current_fiscal_period()
        ├── Query EmployeePeriodMetrics or PeriodMetrics for entity
        └── build_drilldown()    → scored metrics for entity
```

### Key Design Decisions

**Star schema, not normalized OLTP.** Fact tables are pre-aggregated and denormalized. This makes dashboard queries single-table scans rather than multi-join ad hoc queries.

**Idempotent ETL via delete-then-insert.** Every aggregation function deletes existing rows in the target date range before inserting new ones. This means the ETL can be re-run to correct errors, backfill missing data, or incorporate late-arriving records without duplication. Period tables use a full `DROP + re-INSERT` for the entire fiscal year because periods are only meaningful when all daily rows are present.

**Money in cents, always BigInteger.** All monetary columns store cents as `BigInteger` (never floats). This eliminates floating-point rounding in financial aggregations.

**Fiscal calendar at the dimension, not fact, layer.** `DimDate` stores `fiscal_year`, `fiscal_week_of_year`, and `fiscal_day_of_week` from the NRF 4-5-4 calendar. Fiscal period grouping (`fiscal_period`, `fiscal_quarter`) is applied during period aggregation by `FiscalCalendar.get_period_for_week()`. Weeks are the atomic unit; period/quarter grouping is a reporting concern.

**Risk scoring inline with ETL.** `compute_employee_risk_scores()` is called at the end of `aggregate_employee_daily_metrics()`. The resulting `risk_score_snapshot` is written directly to `EmployeeDailyMetrics` rows in the same session, avoiding a second ETL pass.

**Alert counts are a cross-schema join.** `app.alerts` (Chirp) lives in the `app` schema, not `sales`. The ETL crosses schema boundaries by querying `Alert` via SQLAlchemy to populate `alert_count` on daily, hourly, and employee daily fact rows.

---

## 3. Data Model

All models use `MetricsBase`, SQLAlchemy 2.0 `Mapped[]` syntax, and UUID primary keys. The metrics schema is `canary.metrics`.

### Dimensions

#### DimDate

Pre-populated conformed calendar. Primary key is `date_key` (the date itself, not a UUID). One row per calendar day, 2024–2027 by default. Fiscal fields are nullable for dates outside the NRF calendar range.

```python
class DimDate(MetricsBase):
    __tablename__ = "dim_date"

    date_key: Mapped[date]                      # PK — YYYY-MM-DD
    year: Mapped[int]                           # Calendar year
    quarter: Mapped[int]                        # 1-4
    month: Mapped[int]                          # 1-12
    week: Mapped[int]                           # ISO week 1-53
    day_of_week: Mapped[int]                    # 0=Monday, 6=Sunday
    day_name: Mapped[str]                       # "Monday", "Tuesday", etc.
    is_weekend: Mapped[bool]                    # True if Sat or Sun
    is_holiday: Mapped[bool]                    # US federal holidays (manually maintained)
    fiscal_year: Mapped[Optional[int]]          # NRF fiscal year
    fiscal_week_of_year: Mapped[Optional[int]]  # 1-52/53 within fiscal year
    fiscal_day_of_week: Mapped[Optional[int]]   # 1-7, 1=week start day

    Indexes: ix_dim_date_date, ix_dim_date_fiscal_year_week, year (index), month (index), is_holiday (index)
```

SCD Type: Type 1 (full delete + re-insert per year range).
Populated by: `populate_dim_date()` in `canary/services/metrics/dim_loader.py`.

#### DimLocation

One row per Square location per merchant. Synced from `app.locations`.

```python
class DimLocation(MetricsBase):
    __tablename__ = "dim_location"

    id: Mapped[str]                         # UUID PK
    merchant_id: Mapped[str]               # Tenant
    square_location_id: Mapped[str]        # Square location_id
    location_name: Mapped[str]             # Store display name
    city: Mapped[Optional[str]]
    state: Mapped[Optional[str]]
    timezone: Mapped[Optional[str]]        # IANA timezone string
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]

    Indexes: ix_dim_location_merchant
```

SCD Type: Type 2 (upsert — update existing rows, insert new ones).
Populated by: `populate_dim_location(db_session, merchant_id)`.

#### DimEmployee

One row per active Square team member per merchant. Risk category reflects the ML scoring pipeline output.

```python
class DimEmployee(MetricsBase):
    __tablename__ = "dim_employee"

    id: Mapped[str]                         # UUID PK
    merchant_id: Mapped[str]               # Tenant
    square_employee_id: Mapped[str]        # Square team_member_id
    employee_name: Mapped[str]             # Display name
    primary_location_id: Mapped[Optional[str]]
    risk_category: Mapped[str]             # "low" | "medium" | "high"
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]

    Indexes: ix_dim_employee_merchant, ix_dim_employee_risk (merchant_id + risk_category)
```

Risk category thresholds: 0.0–0.3 = low, 0.3–0.7 = medium, 0.7–1.0 = high. Set by `_score_to_category()` during sync.
SCD Type: Type 2 (upsert — updates existing rows).
Populated by: `populate_dim_employee(db_session, merchant_id)`.

---

### Fact Tables — Daily Granularity

#### DailyMetrics

Core daily KPI table. One row per merchant × location × calendar date. The primary source for period rollups and the Owl dashboard.

```python
class DailyMetrics(MetricsBase):
    __tablename__ = "daily_metrics"

    id: Mapped[str]                              # UUID PK
    merchant_id: Mapped[str]
    location_id: Mapped[str]
    metric_date: Mapped[date]

    # Volume
    transaction_count: Mapped[int]
    gross_sales_cents: Mapped[int]               # BigInteger
    refund_count: Mapped[int]
    refund_amount_cents: Mapped[int]             # BigInteger
    void_count: Mapped[int]
    void_total_cents: Mapped[int]                # BigInteger (SDD-032 v2)
    no_sale_count: Mapped[int]
    cash_variance_cents: Mapped[int]             # Sum of closed drawer variances
    unique_employees: Mapped[int]
    unique_customers: Mapped[int]

    # LP-specific (SRA inputs)
    discount_total_cents: Mapped[int]            # BigInteger
    custom_amount_count: Mapped[int]             # Open-ring (SALE with no line items)
    tip_total_cents: Mapped[int]                 # BigInteger

    # Tender mix
    cash_txn_count: Mapped[int]
    card_txn_count: Mapped[int]
    other_txn_count: Mapped[int]

    # Basket
    total_items_sold: Mapped[int]

    # Chirp
    alert_count: Mapped[int]

    # Gift card domain (GRO-249 L7)
    gift_card_load_count: Mapped[int]
    gift_card_load_cents: Mapped[int]            # BigInteger
    gift_card_redeem_count: Mapped[int]
    gift_card_redeem_cents: Mapped[int]          # BigInteger

    # Loyalty domain (GRO-249 L7)
    loyalty_accrual_count: Mapped[int]
    loyalty_redeem_count: Mapped[int]
    loyalty_points_net: Mapped[int]              # Positive = earned, negative = redeemed

    # Dispute / invoice / shrinkage domains (GRO-249 L7)
    dispute_count: Mapped[int]
    dispute_amount_cents: Mapped[int]            # BigInteger
    invoice_count: Mapped[int]
    invoice_amount_cents: Mapped[int]            # BigInteger
    shrinkage_count: Mapped[int]
    shrinkage_quantity: Mapped[Optional[float]]

    created_at: Mapped[datetime]

    Indexes: ix_daily_merchant_date, ix_daily_location_date
```

#### HourlyMetrics

Intraday fact table. One row per merchant × location × employee × date × hour. Enables hourly pattern detection and off-clock alerts.

```python
class HourlyMetrics(MetricsBase):
    __tablename__ = "hourly_metrics"

    id: Mapped[str]                              # UUID PK
    merchant_id: Mapped[str]
    location_id: Mapped[str]
    metric_date: Mapped[date]
    metric_hour: Mapped[int]                     # 0-23 UTC
    employee_id: Mapped[Optional[str]]           # Nullable for location-level rows
    transaction_count: Mapped[int]
    gross_sales_cents: Mapped[int]               # BigInteger
    refund_count: Mapped[int]
    void_count: Mapped[int]
    no_sale_count: Mapped[int]
    discount_total_cents: Mapped[int]            # BigInteger
    alert_count: Mapped[int]
    created_at: Mapped[datetime]

    Indexes: ix_hourly_merchant_date_hour, ix_hourly_location
```

#### EmployeeDailyMetrics

Per-employee daily fact table. One row per merchant × employee × location × date. Enables employee-level SRA, off-clock detection, and risk trending.

```python
class EmployeeDailyMetrics(MetricsBase):
    __tablename__ = "employee_daily_metrics"

    id: Mapped[str]
    merchant_id: Mapped[str]
    employee_id: Mapped[str]
    location_id: Mapped[str]
    metric_date: Mapped[date]

    # Transactions
    transaction_count: Mapped[int]
    gross_sales_cents: Mapped[int]               # BigInteger
    refund_count: Mapped[int]
    void_count: Mapped[int]
    no_sale_count: Mapped[int]
    discount_total_cents: Mapped[int]
    alert_count: Mapped[int]
    custom_amount_count: Mapped[int]

    # Off-clock (GRO-249, GRO-277a)
    off_clock_flag: Mapped[bool]                 # True if any txn outside shift windows
    off_clock_txn_count: Mapped[int]
    off_clock_amount_cents: Mapped[int]          # BigInteger

    # Timecard enrichment (GRO-277)
    shift_hours_worked: Mapped[Optional[float]]
    sales_per_hour_cents: Mapped[Optional[int]]  # BigInteger

    # Discount decomposition (GRO-277a)
    discount_count: Mapped[int]
    discount_fixed_count: Mapped[int]            # FIXED_AMOUNT, VARIABLE_AMOUNT
    discount_percentage_count: Mapped[int]       # FIXED_PERCENTAGE, VARIABLE_PERCENTAGE

    # Risk
    risk_score_snapshot: Mapped[Optional[float]] # 0.0-1.0 as of EOD

    # Domain metrics (GRO-249 L7)
    gift_card_load_count: Mapped[int]
    gift_card_load_cents: Mapped[int]            # BigInteger
    gift_card_redeem_count: Mapped[int]
    gift_card_redeem_cents: Mapped[int]          # BigInteger
    loyalty_accrual_count: Mapped[int]
    loyalty_redeem_count: Mapped[int]
    shrinkage_count: Mapped[int]
    shrinkage_quantity: Mapped[Optional[float]]

    created_at: Mapped[datetime]

    Indexes: ix_emp_metric_merchant_emp_date, ix_emp_metric_location_date
```

#### ProductDailyMetrics

Per-product daily fact table. One row per merchant × product (SKU) × location × date. Enables product-level return rate analysis.

```python
class ProductDailyMetrics(MetricsBase):
    __tablename__ = "product_daily_metrics"

    id: Mapped[str]
    merchant_id: Mapped[str]
    product_id: Mapped[str]                      # catalog_object_id from Square
    location_id: Mapped[str]
    metric_date: Mapped[date]
    units_sold: Mapped[Optional[float]]          # BigInteger (nullable)
    units_returned: Mapped[Optional[float]]      # BigInteger (nullable)
    return_rate: Mapped[Optional[float]]         # units_returned / units_sold
    gross_sales_cents: Mapped[int]               # BigInteger
    discount_cents: Mapped[int]                  # BigInteger
    created_at: Mapped[datetime]

    Indexes: ix_prod_metric_merchant_product_date, ix_prod_metric_location_date
```

---

### Fact Tables — Period Granularity

#### PeriodMetrics

NRF 4-5-4 fiscal period rollup. One row per merchant × location × fiscal period. Full rebuild per fiscal year (not incremental). The SRA v2 formula is computed at this level.

**SRA v2 formula:**
```
sra_total_cents = refund_amount_cents + void_total_cents + cash_variance_cents + discount_total_cents
sra_pct_sales   = sra_total_cents / gross_sales_cents * 100
```

```python
class PeriodMetrics(MetricsBase):
    __tablename__ = "period_metrics"

    id: Mapped[str]
    merchant_id: Mapped[str]
    location_id: Mapped[str]
    fiscal_year: Mapped[int]                     # SmallInteger
    fiscal_quarter: Mapped[int]                  # SmallInteger 1-4
    fiscal_period: Mapped[int]                   # SmallInteger 1-13 (absolute)
    period_start_date: Mapped[date]
    period_end_date: Mapped[date]
    days_in_period: Mapped[int]                  # Calendar days with data

    # Summed from daily_metrics
    transaction_count: Mapped[int]
    gross_sales_cents: Mapped[int]               # BigInteger
    refund_count: Mapped[int]
    refund_amount_cents: Mapped[int]             # BigInteger
    void_count: Mapped[int]
    void_total_cents: Mapped[int]                # BigInteger
    no_sale_count: Mapped[int]
    cash_variance_cents: Mapped[int]
    discount_total_cents: Mapped[int]            # BigInteger
    custom_amount_count: Mapped[int]
    cash_txn_count: Mapped[int]
    card_txn_count: Mapped[int]
    other_txn_count: Mapped[int]
    total_items_sold: Mapped[int]
    alert_count: Mapped[int]
    unique_employees: Mapped[int]                # Max single-day unique employees
    unique_customers: Mapped[int]                # Max single-day unique customers

    # Domain metrics (GRO-249 L7)
    gift_card_load_count: Mapped[int]
    gift_card_load_cents: Mapped[int]            # BigInteger
    gift_card_redeem_count: Mapped[int]
    gift_card_redeem_cents: Mapped[int]          # BigInteger
    loyalty_accrual_count: Mapped[int]
    loyalty_redeem_count: Mapped[int]
    loyalty_points_net: Mapped[int]
    dispute_count: Mapped[int]
    dispute_amount_cents: Mapped[int]            # BigInteger
    invoice_count: Mapped[int]
    invoice_amount_cents: Mapped[int]            # BigInteger
    shrinkage_count: Mapped[int]
    shrinkage_quantity: Mapped[Optional[float]]

    # SRA v2 (Shrink Risk Assessment)
    sra_total_cents: Mapped[int]                 # BigInteger
    sra_pct_sales: Mapped[Optional[float]]       # 0.0-100.0

    created_at: Mapped[datetime]

    Indexes: ix_period_merchant_fy_period, ix_period_location_fy
```

#### EmployeePeriodMetrics

Per-employee NRF fiscal period rollup. One row per merchant × employee × fiscal period. Aggregated from `employee_daily_metrics`. Enables period-over-period employee risk trending.

```python
class EmployeePeriodMetrics(MetricsBase):
    __tablename__ = "employee_period_metrics"

    id: Mapped[str]
    merchant_id: Mapped[str]
    employee_id: Mapped[str]
    location_id: Mapped[str]
    fiscal_year: Mapped[int]                     # SmallInteger
    fiscal_quarter: Mapped[int]                  # SmallInteger
    fiscal_period: Mapped[int]                   # SmallInteger
    period_start_date: Mapped[date]
    period_end_date: Mapped[date]

    # Summed from employee_daily_metrics
    transaction_count: Mapped[int]
    gross_sales_cents: Mapped[int]               # BigInteger
    refund_count: Mapped[int]
    void_count: Mapped[int]
    no_sale_count: Mapped[int]
    discount_total_cents: Mapped[int]            # BigInteger
    custom_amount_count: Mapped[int]
    alert_count: Mapped[int]
    off_clock_days: Mapped[int]
    off_clock_txn_count: Mapped[int]
    off_clock_amount_cents: Mapped[int]          # BigInteger
    shift_hours_worked: Mapped[Optional[float]]
    sales_per_hour_cents: Mapped[Optional[int]]  # BigInteger
    discount_count: Mapped[int]
    discount_fixed_count: Mapped[int]
    discount_percentage_count: Mapped[int]
    avg_risk_score: Mapped[Optional[float]]
    max_risk_score: Mapped[Optional[float]]

    # Domain metrics (GRO-249 L7)
    gift_card_load_count: Mapped[int]
    gift_card_load_cents: Mapped[int]            # BigInteger
    gift_card_redeem_count: Mapped[int]
    gift_card_redeem_cents: Mapped[int]          # BigInteger
    loyalty_accrual_count: Mapped[int]
    loyalty_redeem_count: Mapped[int]
    shrinkage_count: Mapped[int]
    shrinkage_quantity: Mapped[Optional[float]]

    created_at: Mapped[datetime]

    Indexes: ix_emp_period_merchant_emp_fy, ix_emp_period_location_fy
```

---

### Risk & ML Tables

#### TransactionFeature

ML feature vector per transaction. Populated by the ML scoring pipeline (not the ETL). `feature_vector` is a JSON string.

#### FeatureDefinition

Catalog of all ML input features (TRANSACTION_AMOUNT, REFUND_RATIO, EMPLOYEE_DISCOUNT_RATE, etc.). Describes `feature_type` (numeric|categorical|boolean), source table, and source column.

#### MLModel

Registry of trained models with version, type, training timestamp, and JSON performance metrics. Only one model has `is_active = True` at a time.

#### EntityRiskScore

Current risk score per entity (`employee`, `card`, `device`, `location`). SCD Type 1 — overwritten on each scoring pass. Stores the contributing factors as a JSON array: `[{name, weight, value}, ...]`. Unique constraint on `(merchant_id, entity_type, entity_id)`.

#### RiskScoreHistory

Append-only audit trail of entity risk scores. Every scoring pass appends a new row. Enables trend analysis (is this employee's risk increasing?).

#### MetricBaseline

Statistical baseline (mean + std deviation) per metric name, optionally scoped to a location. Used by the heatmap scoring engine to determine deviation bands. Example: `DAILY_TRANSACTION_COUNT` baseline = 150, std_dev = 35.

#### VelocityBaseline (GRO-139)

XPLOSS-equivalent velocity anomaly detection. Stores mean/stddev per metric per time slot (`day_of_week` + `hour_of_day`). Granularity can be daily, hourly, or overall. Unique constraint on `(merchant_id, metric_name, location_id, day_of_week, hour_of_day)`.

---

### Scoring & Config Tables

#### ScorecardThreshold (GRO-147)

Per-merchant configurable threshold bands for heatmap scoring. Thresholds are expressed as percentages of baseline:

| Band | Range |
|------|-------|
| normal | < `normal_upper_pct` (e.g. < 100%) |
| watch | `normal_upper_pct` to `watch_upper_pct` (e.g. 100-110%) |
| review | `watch_upper_pct` to `review_upper_pct` (e.g. 110-120%) |
| investigate | >= `review_upper_pct` |

Direction is either `higher_is_worse` or `lower_is_worse`. Seeded with platform defaults on merchant onboarding.

#### DashboardConfig

Per-merchant dashboard layout and display preferences: metric card order, auto-refresh interval (default 300s), employee heatmap visibility, trend arrow visibility.

#### WeeklyScorecard / MonthlyScorecard

Pre-computed KPI JSON snapshots at weekly and monthly granularity. `kpis` column is a JSON object with keys: `total_sales`, `refund_count`, `refund_rate`, `void_count`, `alerts`, etc.

---

## 4. Interfaces

### REST API — Analytics Blueprint

`Canary/canary/blueprints/analytics.py` — registered at `/api/analytics/`.

All endpoints require JWT authentication (`@jwt_required()`). All responses are merchant-scoped via `g.merchant_id`. No demo fallbacks — if no data exists, returns empty or 404.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/analytics/dashboard` | Current period summary with health score and heatmap-scored metrics. Delegates to `get_dashboard_data(merchant_id)`. |
| GET | `/api/analytics/trends?metric=<name>` | Trend data for a single metric across the last 6 fiscal periods. Default metric: `REFUND_RATE`. |
| GET | `/api/analytics/top-risks` | Top risk employees and locations. Delegates to `get_top_risks_data(merchant_id)`. |
| GET | `/api/analytics/drilldown?entity_type=<type>&entity_id=<id>` | Scored metric detail for a single employee or location. Returns 400 if `entity_id` missing, 404 if no data. |
| GET | `/api/analytics/export` | Not yet implemented — returns 501. |

**Dashboard response shape:**
```json
{
  "period": {"fiscal_year": 2026, "fiscal_period": 3},
  "health_score": 72.4,
  "scored_metrics": [
    {
      "name": "REFUND_RATE",
      "label": "Refund Rate",
      "actual": 4.2,
      "baseline": 3.1,
      "pct_of_baseline": 135.5,
      "band": "investigate",
      "color": "red",
      "format": "percent",
      "is_alert_worthy": true
    }
  ]
}
```

**Trends response shape:**
```json
{
  "metric": "REFUND_RATE",
  "data": [
    {"period": 1, "value": 3.0, "pct_of_baseline": 96.8, "band": "normal"},
    {"period": 2, "value": 3.8, "pct_of_baseline": 122.6, "band": "investigate"}
  ]
}
```

**Drilldown response shape:**
```json
{
  "entity_type": "employee",
  "entity_id": "<id>",
  "scored_metrics": [...],
  "alert_worthy_metrics": [
    {"name": "VOID_COUNT", "label": "Void Count", "band": "review", "color": "yellow"}
  ]
}
```

### MCP Server — Analytics MCP Blueprint

`Canary/canary/blueprints/analytics_mcp.py` — registered at `/analytics/`.

Built with `create_mcp_blueprint()` using the tool registry from `canary/services/analytics/tools.py`. Exposes all registered tools to MCP clients (e.g., Owl). Health endpoint reports `service: "canary-analytics"` and tool count.

### CLI — Metrics Commands

The `flask metrics` CLI group (registered in the Flask app factory) provides:

```bash
flask metrics load-dims                        # Load all three dimensions
flask metrics load-dims --dim date             # Just dim_date
flask metrics load-dims --merchant-id <id>     # dim_location + dim_employee for one merchant
flask metrics run-etl --merchant-id <id>       # Run full ETL (90-day lookback default)
flask metrics run-etl --merchant-id <id> --start-date 2026-01-01 --end-date 2026-03-30
```

---

## 5. Service Layer

### `canary/services/metrics/dim_loader.py`

Three idempotent dimension loading functions.

**`populate_dim_date(db_session, start_year=2024, end_year=2027) -> int`**

Generates one `DimDate` row per calendar day in the range. Fiscal fields are applied using `FiscalCalendar(anchor_month=2, week_start_day=6)` (NRF defaults: fiscal year starts in February, week starts on Sunday). Existing rows in the year range are deleted before re-insertion. Returns row count.

**`populate_dim_location(db_session, merchant_id) -> int`**

Reads active `Location` records from `app.locations` for the merchant. Upserts into `dim_location`: updates existing rows by `square_location_id`, inserts new ones. Returns total row count after sync.

**`populate_dim_employee(db_session, merchant_id) -> int`**

Reads active (`is_active=True`) `Employee` records from `app.employees` for the merchant. Upserts into `dim_employee`. Calls `_score_to_category(emp.risk_score)` to map the float score to `low|medium|high` for the dimension row. Returns total row count after sync.

**`_score_to_category(risk_score: Optional[float]) -> str`**

Thresholds: None or < 0.3 → `"low"`, 0.3–0.7 → `"medium"`, >= 0.7 → `"high"`.

---

### `canary/services/metrics_etl.py`

The main ETL orchestrator. Contains four aggregation functions and one coordinator.

**`aggregate_daily_metrics(merchant_id, start_date, end_date) -> int`**

Executes 10 separate SQL queries against the sales and app schemas and merges results into `DailyMetrics` rows. Queries run independently; results are joined in Python via lookup dictionaries keyed on `(location_id, metric_date)`.

Sub-queries executed:
1. Transactions → volume metrics (count, sales, refunds, voids, no-sales, discounts, tips, unique employees/customers)
2. `cash_drawer_shifts` (state=CLOSED) → `cash_variance_cents`
3. Transactions with no line items (correlated NOT EXISTS) → `custom_amount_count`
4. `transaction_tenders` → tender mix (cash/card/other)
5. `transaction_line_items` → `total_items_sold`
6. `app.alerts` → `alert_count` (cross-schema join)
7. `gift_card_activities` → load/redeem counts and amounts
8. `loyalty_events` → accrual/redeem counts and net points
9. `disputes` → count and amount
10. `invoices` → count and amount
11. `inventory_adjustments` (type=SHRINKAGE) → count and quantity

**`aggregate_hourly_metrics(merchant_id, start_date, end_date) -> int`**

Groups transactions by `location_id + employee_id + date + hour` (UTC). Cross-joins `app.alerts` at hourly granularity. Produces one row per employee per hour.

**`aggregate_employee_daily_metrics(merchant_id, start_date, end_date) -> int`**

Most complex aggregation. Only processes transactions with non-NULL `employee_id`. In addition to standard volume metrics, computes:

- **Off-clock flag** — cross-references `employee_timecards` to detect transactions outside any shift window. Requires closed timecards (end_at IS NOT NULL). If no timecards exist for an employee, defaults to False (cannot determine).
- **Off-clock magnitude** — uses a NOT EXISTS correlated subquery against `employee_timecards` to count transactions and sum amounts for employees who have timecards but whose transactions fall outside shift boundaries.
- **Shift hours** — sums closed shift durations from `employee_timecards` per employee per date.
- **Sales per hour** — `gross_sales_cents / shift_hours_worked` (zero if no shift data).
- **Discount decomposition** — joins `line_item_discounts` to split discounts into fixed-amount vs percentage types.
- **Domain metrics** — gift card, loyalty, and shrinkage aggregated at the employee level.
- **Risk score snapshot** — after inserting all `EmployeeDailyMetrics` rows, calls `compute_employee_risk_scores()` to write `risk_score_snapshot` on the same session objects before `flush()`.

**`aggregate_product_daily_metrics(merchant_id, start_date, end_date) -> int`**

Joins `transaction_line_items` to `transactions`. Only processes line items with a non-NULL `catalog_object_id`. Groups by `product_id + location_id + date`. Computes `return_rate = units_returned / units_sold` inline (None if no sales).

**`run_etl(merchant_id, start_date=None, end_date=None, lookback_days=90) -> dict`**

Orchestrates the full pipeline:
1. Calls all four daily aggregation functions.
2. Commits the session (daily facts are durably written).
3. Derives fiscal year(s) from the date range (NRF fiscal year starts in February — dates in January belong to the prior fiscal year).
4. Calls `aggregate_period_metrics(session, merchant_id, fy)` for each fiscal year in scope.
5. Commits again.
6. Returns a dict of row counts per table: `{daily_metrics, hourly_metrics, employee_daily_metrics, product_daily_metrics, period_metrics, employee_period_metrics}`.

---

### Supporting Services (referenced by ETL)

| Service | Location | Role |
|---------|----------|------|
| `FiscalCalendar` | `canary/services/fiscal_calendar.py` | NRF 4-5-4 calendar generation; `get_period_for_week()` maps fiscal weeks to periods |
| `aggregate_period_metrics` | `canary/services/period_aggregation.py` | Rolls `daily_metrics` and `employee_daily_metrics` up to period fact tables; computes SRA v2 |
| `compute_employee_risk_scores` | `canary/services/employee_risk_scoring.py` | Peer-relative risk scoring; called inline at the end of `aggregate_employee_daily_metrics` |
| `get_dashboard_data` | `canary/services/dashboard.py` | Reads `PeriodMetrics`, applies threshold scoring, returns heatmap-ready response |
| `build_trend_data` | `canary/services/dashboard.py` | Constructs period-over-period trend series for sparklines |
| `build_drilldown` | `canary/services/dashboard.py` | Entity-scoped scored metric response |
| `fetch_trend_periods`, `fetch_baselines`, `fetch_thresholds`, `get_current_fiscal_period` | `canary/services/dashboard_queries.py` | Query helpers for the analytics blueprint |

---

## 6. Configuration

The metrics ETL has no separate config file. It reads from the Flask app's environment via `get_session()`.

| Setting | Source | Notes |
|---------|--------|-------|
| `DATABASE_URL` | `.env` | PostgreSQL connection for all metrics queries |
| `start_year` / `end_year` | `populate_dim_date()` params | Default 2024–2027; change at dim load time |
| `lookback_days` | `run_etl()` param | Default 90 days if no explicit date range |
| Fiscal anchor month | `FiscalCalendar(anchor_month=2)` | NRF default: February |
| Fiscal week start | `FiscalCalendar(week_start_day=6)` | Sunday = 6 in Python weekday (0=Mon) |
| Dashboard refresh interval | `DashboardConfig.refresh_interval_seconds` | Default 300 seconds, per-merchant |
| Scorecard thresholds | `ScorecardThreshold` rows | Seeded on merchant onboarding, merchant-configurable |

---

## 7. Security & Compliance

**Multi-tenancy.** Every table in the metrics schema includes `merchant_id` as a non-nullable column with an index. All ETL functions are scoped to a single `merchant_id` argument. Analytics endpoints read `g.merchant_id` from the JWT token — there is no mechanism for a merchant to query another merchant's data.

**Authentication.** All REST endpoints use `@jwt_required()`. The Analytics MCP server inherits authentication from `create_mcp_blueprint()`.

**No PII in fact tables.** Fact tables store only Square-issued identifiers (`employee_id`, `customer_id`, `product_id`, `location_id`). Display names and contact information remain in `app.employees`, `app.customers`, and `dim_employee`. Dashboard drill-down responses resolve names via the dimension tables.

**Monetary precision.** All monetary values are stored as cents (BigInteger). No floating-point arithmetic is performed on monetary fields. Division for rates (e.g., `sra_pct_sales`, `return_rate`, `sales_per_hour_cents`) is performed in Python after aggregation, with guarded zero-division.

---

## 8. Error Handling

**ETL idempotency on failure.** Because each aggregation function deletes existing rows before inserting, a partial ETL run leaves the table either empty (if it failed before the flush) or complete. Re-running the ETL for the same date range is always safe.

**Period aggregation failure isolation.** In `run_etl()`, period aggregation is wrapped in a `try/except` per fiscal year. A failure in period rollup logs a warning and continues — daily facts are already committed and are not rolled back.

**Off-clock detection with no timecards.** `_is_off_clock()` returns `False` when no timecard data exists for an employee. This is by design — the system cannot flag off-clock activity without a reference window.

**Missing baselines.** If `fetch_baselines()` returns empty (new merchant, no historical data), the dashboard service defaults baseline values to 0.0, resulting in all metrics being scored as `investigate`. This is a known cold-start condition, not an error.

**Export endpoint.** `GET /api/analytics/export` returns HTTP 501 Not Implemented. This is an intentional placeholder.

---

## 9. Testing

Tests are co-located in the standard test layout:

```
tests/
├── unit/
│   ├── test_dim_loader.py          # populate_dim_date, populate_dim_location, populate_dim_employee
│   └── test_score_to_category.py   # _score_to_category thresholds
├── integration/
│   ├── test_metrics_etl.py         # run_etl end-to-end, row count verification
│   ├── test_daily_metrics.py       # aggregate_daily_metrics isolation
│   ├── test_employee_metrics.py    # aggregate_employee_daily_metrics + off-clock
│   └── test_analytics_routes.py   # /api/analytics/* HTTP contract
└── smoke/
    └── test_analytics_smoke.py     # Health check + /api/analytics/dashboard with real data
```

**Completeness gate.** Before any ETL function is marked done, the four-step gate must pass:
1. `pytest tests/integration/test_metrics_etl.py -v` — write verification
2. `pytest tests/integration/test_analytics_routes.py -v` — read verification
3. Row count check via `pg_stat_user_tables` — delta matches expected
4. `curl http://localhost:5001/api/analytics/dashboard` — 200 OK with non-empty payload

**Fixtures.** Integration tests use a `canary_test` database populated by the standard `conftest.py` app factory. Test data must fully populate all Square payload fields (no nulls) per platform memory `feedback_fully_populate_data`.

---

## 10. Dependencies

### Upstream

| Service | What it provides | Why metrics depends on it |
|---------|-----------------|--------------------------|
| **TSP** (Transaction Sync Pipeline) | `canary.sales` schema tables: transactions, line_items, line_item_discounts, tenders, cash_drawer_shifts, timecards, gift_card_activities, loyalty_events, disputes, invoices, inventory_adjustments | These are the source tables for all ETL aggregation |
| **Chirp** (Alert Pipeline) | `canary.app.alerts` table | Alert counts are joined cross-schema into daily and hourly fact tables |
| **Square Locations API** | `canary.app.locations` table | Source for `populate_dim_location` |
| **Square Team Members API** | `canary.app.employees` table | Source for `populate_dim_employee` |
| **Employee Risk Scoring** | `canary/services/employee_risk_scoring.py` | `compute_employee_risk_scores()` called inline during employee daily ETL |
| **Fiscal Calendar** | `canary/services/fiscal_calendar.py` | NRF 4-5-4 calendar used in `populate_dim_date` and `aggregate_period_metrics` |

### Downstream

| Consumer | What it reads |
|----------|--------------|
| **Owl** (Analytics Dashboard) | All period fact tables, entity risk scores, scorecard thresholds via the `/api/analytics/*` REST endpoints |
| **Analytics MCP** | Same data via the `/analytics/*` MCP tool registry |
| **Chirp** (alert engine) | `daily_metrics`, `employee_daily_metrics`, `metric_baselines`, `velocity_baselines` for anomaly threshold evaluation |
| **Fox** (case management) | `entity_risk_scores`, `risk_score_history` when building LP case context |

### Shared Infrastructure

| Resource | Details |
|----------|---------|
| PostgreSQL 17 (`growdirect_postgres`) | `canary` database; metrics tables live in the `metrics` schema |
| `MetricsBase` | SQLAlchemy declarative base scoped to the metrics schema (defined in `canary/models/base.py`) |
| `get_session()` | Session factory from `canary/db/session_factory.py`; used directly by all ETL functions |

---

## 11. Known Issues & Reconciliation

### ETL file location inconsistency

`metrics_etl.py` lives at `Canary/canary/services/metrics_etl.py` (the `services/` root), while all dimension loader code lives at `Canary/canary/services/metrics/dim_loader.py` (the `services/metrics/` subdirectory). This is an organizational inconsistency.

The convention for other service domains in this codebase is to collect related service modules inside a subdirectory (e.g., `services/analytics/`, `services/identity/`). `metrics_etl.py` should be at `services/metrics/etl.py` to match. Correcting this requires updating all import paths. Track as a cleanup GRO issue — do not inline-fix.

### Period aggregation: full-rebuild pattern

`aggregate_period_metrics` deletes and rebuilds all period rows for an entire fiscal year on each run. This is correct (periods are only meaningful once all daily data is present) but is not incremental. For merchants with many locations and multiple years, this will become slow. A partial-rebuild strategy (rebuild only the current open period + the one prior) is a future optimization.

### `is_holiday` field is not maintained

`DimDate.is_holiday` is set to `False` for all rows during `populate_dim_date`. There is no automated holiday calendar import. The field exists in the schema but is currently non-functional for any holiday-adjusted baseline calculations.

### Off-clock detection requires closed timecards

`_is_off_clock()` only considers timecard entries with a non-NULL `end_at`. Open shifts (employee still clocked in) are excluded. This means an employee working an open shift who processes transactions will not be flagged, even if those transactions occur before `start_at`.

### `WeeklyScorecard` / `MonthlyScorecard` not populated by ETL

These tables are defined in the schema but are not written by `run_etl()` or `aggregate_period_metrics`. They appear to be populated by a separate job or are not yet wired. The dashboard currently reads from `period_metrics`, not from these scorecard tables.

### Analytics export endpoint is a stub

`GET /api/analytics/export` returns HTTP 501. No export implementation exists. Flagged for a future GRO issue.
