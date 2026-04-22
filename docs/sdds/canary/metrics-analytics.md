# Metrics & Analytics — Star Schema ETL Pipeline

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]], [[Brain/wiki/canary-data-model|Canary Data Model]]
**Architecture:** [[docs/sdds/canary/architecture|Canary Architecture SDD]]

> **Type:** App Service (Canary)
> **Status:** Operational — code review complete
> **Last updated:** 2026-04-13
> **Code location:** `Canary/canary/services/metrics_etl.py`, `Canary/canary/services/metrics/dim_loader.py`, `Canary/canary/services/period_aggregation.py`, `Canary/canary/services/fiscal_calendar.py`, `Canary/canary/models/metrics/`
> **Split from:** Original `metrics-analytics.md` (7000 words, two deployable concerns)

**Companion SDD:** [[docs/sdds/canary/metrics-risk-scoring|Metrics Risk Scoring]] — Entity risk scoring, SRA computation, heatmap scoring, analytics dashboard
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[docs/team/Architect|Architect]] + [[docs/team/PhD|PhD]] · **Operator role:** [[docs/team/Engineer|Engineer]]

---

## Purpose

The Metrics ETL pipeline transforms raw Square sales events from the `canary.sales` schema into a star schema optimized for loss-prevention reporting. It runs three stages: dimension loading (conformed calendar + entity dimensions), daily ETL (four granularity-level fact tables), and period aggregation (NRF 4-5-4 fiscal rollups with SRA computation). The resulting star schema feeds the analytics dashboard, the Analytics MCP server, and the Chirp anomaly detection engine.

---

## Dependencies

| Dependency | Type | Required | What it provides |
|-----------|------|----------|-----------------|
| PostgreSQL 17 (`growdirect_postgres`) | Infrastructure | Yes | `canary` database, `metrics` schema |
| TSP (Transaction Sync Pipeline) | Upstream service | Yes | All `canary.sales` schema tables: transactions, line_items, tenders, cash_drawers, timecards, gift_cards, loyalty, disputes, invoices, inventory_adjustments |
| Chirp (Alert Pipeline) | Upstream service | Yes | `canary.app.alerts` table (cross-schema join for alert counts) |
| Square Locations API | External (via TSP) | Yes | `canary.app.locations` — source for `dim_location` |
| Square Team Members API | External (via TSP) | Yes | `canary.app.employees` — source for `dim_employee` |
| Fiscal Calendar service | Internal | Yes | `canary/services/fiscal_calendar.py` — NRF 4-5-4 calendar generation |
| Employee Risk Scoring | Internal | Yes | `canary/services/employee_risk_scoring.py` — called inline during employee daily ETL |

---

## Data Flow & PII Map

### What enters

- **Source:** 11 tables from `canary.sales` schema + 3 tables from `canary.app` schema
- **Format:** SQLAlchemy model rows via `get_session()`
- **Trigger:** CLI command (`flask metrics run-etl`) or scheduled job
- **Volume:** All transactions for a merchant within a date range (default 90-day lookback)

### What is stored (metrics schema)

**Dimension tables:**

| Table | Fields | PII Classification |
|-------|--------|-------------------|
| `dim_date` | date_key, year, quarter, month, week, day_of_week, day_name, is_weekend, is_holiday, fiscal_year, fiscal_week_of_year, fiscal_day_of_week | **public** — calendar data only |
| `dim_location` | id, merchant_id, square_location_id, location_name, city, state, timezone | **internal** — store names visible to authenticated merchant users |
| `dim_employee` | id, merchant_id, square_employee_id, employee_name, primary_location_id, risk_category | **sensitive** — employee_name is PII; risk_category reveals behavioral assessment of an individual |

**Daily fact tables:**

| Table | Grain | Key Fields | PII Classification |
|-------|-------|-----------|-------------------|
| `daily_metrics` | merchant x location x date | 30+ aggregated KPI columns, all monetary in cents (BigInteger) | **internal** — no direct PII; location_id is a Square identifier |
| `hourly_metrics` | merchant x location x employee x date x hour | transaction_count, gross_sales, refund/void/no-sale counts, discount, alert_count | **internal** — employee_id links to PII via dim_employee |
| `employee_daily_metrics` | merchant x employee x location x date | All daily KPIs + off_clock_flag, shift_hours, discount decomposition, risk_score_snapshot | **sensitive** — employee behavioral profiling data; risk_score_snapshot is PII-adjacent |
| `product_daily_metrics` | merchant x product x location x date | units_sold, units_returned, return_rate, gross_sales, discount | **internal** — product identifiers only |

**Period fact tables:**

| Table | Grain | Key Fields | PII Classification |
|-------|-------|-----------|-------------------|
| `period_metrics` | merchant x location x fiscal period | All daily KPIs summed + SRA (sra_total_cents, sra_pct_sales) | **internal** — no direct PII |
| `employee_period_metrics` | merchant x employee x fiscal period | All employee daily KPIs summed + avg/max risk scores | **sensitive** — employee behavioral profiling |

### What exits

- To **Analytics REST API** (`/api/analytics/*`) — period summaries, trends, drilldowns (see [[docs/sdds/canary/metrics-risk-scoring|Metrics Risk Scoring]])
- To **Analytics MCP** (`/analytics/*`) — same data via tool registry
- To **Chirp** — `daily_metrics`, `employee_daily_metrics` for anomaly threshold evaluation
- To **Fox** — `entity_risk_scores`, `risk_score_history` for LP case context

---

## API Contract

### CLI Commands

```bash
flask metrics load-dims                        # Load all three dimensions
flask metrics load-dims --dim date             # Just dim_date
flask metrics load-dims --merchant-id <id>     # dim_location + dim_employee for one merchant
flask metrics run-etl --merchant-id <id>       # Run full ETL (90-day lookback default)
flask metrics run-etl --merchant-id <id> --start-date 2026-01-01 --end-date 2026-03-30
```

### Internal Python API

| Function | Location | Signature | Returns |
|---------|----------|-----------|---------|
| `populate_dim_date` | `metrics/dim_loader.py` | `(db_session, start_year=2024, end_year=2027)` | int (rows created) |
| `populate_dim_location` | `metrics/dim_loader.py` | `(db_session, merchant_id)` | int (rows synced) |
| `populate_dim_employee` | `metrics/dim_loader.py` | `(db_session, merchant_id)` | int (rows synced) |
| `aggregate_daily_metrics` | `metrics_etl.py` | `(merchant_id, start_date, end_date)` | int (rows created) |
| `aggregate_hourly_metrics` | `metrics_etl.py` | `(merchant_id, start_date, end_date)` | int (rows created) |
| `aggregate_employee_daily_metrics` | `metrics_etl.py` | `(merchant_id, start_date, end_date)` | int (rows created) |
| `aggregate_product_daily_metrics` | `metrics_etl.py` | `(merchant_id, start_date, end_date)` | int (rows created) |
| `run_etl` | `metrics_etl.py` | `(merchant_id, start_date=None, end_date=None, lookback_days=90)` | dict of row counts |
| `aggregate_period_metrics` | `period_aggregation.py` | `(session, merchant_id, fiscal_year, ...)` | PeriodAggResult |

---

## Operations

### ETL Execution Flow

```
run_etl(merchant_id, start_date, end_date)
  1. aggregate_daily_metrics()       — 11 SQL queries → daily_metrics rows
  2. aggregate_hourly_metrics()      — 2 SQL queries → hourly_metrics rows
  3. aggregate_employee_daily_metrics() — 10+ queries → employee_daily_metrics rows
     └─ compute_employee_risk_scores() — inline risk scoring on same session
  4. aggregate_product_daily_metrics()  — 1 query → product_daily_metrics rows
  5. session.commit()                   — daily facts durably written
  6. FOR EACH fiscal_year in range:
     └─ aggregate_period_metrics()     — daily → period rollup + SRA v2
  7. session.commit()                   — period facts durably written
  8. RETURN {table: row_count, ...}
```

### Startup / Health

No standalone process. Runs within the Canary Flask app as CLI commands or scheduled tasks. Health is implicit — if the Flask app is up and `get_session()` returns a valid session, the ETL can run.

### Failure Modes

| Failure | Impact | Recovery |
|---------|--------|----------|
| ETL fails mid-aggregation | Delete-before-insert means partial run leaves table either empty or complete for that date range | Re-run `run_etl` for the same date range — fully idempotent |
| Period aggregation fails | Daily facts are already committed; period tables may be stale | `run_etl` wraps period aggregation in try/except per fiscal year — logs warning, does not rollback daily facts |
| Missing source data (no transactions) | Empty fact tables for that date range | Not an error — dashboard shows empty state |
| No timecard data for employee | `off_clock_flag` defaults to False | By design — cannot detect off-clock without reference window |
| Missing baselines (new merchant) | Dashboard scores all metrics as "investigate" | Cold-start condition — baselines populate after first full period of data |
| Database connection failure | ETL cannot run | Retry; no partial state to clean up |

### Monitoring

| Metric | Alert Threshold | Notes |
|--------|----------------|-------|
| `run_etl` execution time | > 10 minutes per merchant | Watch for growth as transaction volume scales |
| Row count delta | 0 rows created for a merchant with known activity | Indicates source data pipeline (TSP) may be stalled |
| Period aggregation warnings in log | Any `period aggregation failed` log entry | Investigate fiscal calendar or daily data gaps |

### Configuration

| Setting | Source | Default | Notes |
|---------|--------|---------|-------|
| `DATABASE_URL` | `.env` | — | PostgreSQL connection string |
| `lookback_days` | `run_etl()` param | 90 | Days to process when no explicit range given |
| `start_year` / `end_year` | `populate_dim_date()` params | 2024 / 2027 | Calendar range for dim_date |
| Fiscal anchor month | `FiscalCalendar(anchor_month=2)` | February | NRF standard |
| Fiscal week start | `FiscalCalendar(week_start_day=6)` | Sunday | Python weekday 6 = Sunday |
| NRF period pattern | `aggregate_period_metrics(pattern=(4,5,4))` | (4, 5, 4) | Weeks per period within each quarter |

---

## Key Design Decisions

**Star schema, not normalized OLTP.** Fact tables are pre-aggregated and denormalized. Dashboard queries hit single tables, not multi-join ad hoc queries.

**Idempotent ETL via delete-then-insert.** Every aggregation function deletes existing rows in the target date range before inserting. Re-runs are always safe. Period tables use full DROP + re-INSERT for the entire fiscal year because periods are only meaningful when all daily rows are present.

**Money in cents, always BigInteger.** All monetary columns store cents as `BigInteger`. No floating-point arithmetic on monetary fields. Division for rates happens in Python after aggregation with guarded zero-division.

**Fiscal calendar at the dimension layer.** `DimDate` stores fiscal fields from the NRF 4-5-4 calendar. Period grouping is applied during period aggregation by `FiscalCalendar.get_period_for_week()`.

**Risk scoring inline with ETL.** `compute_employee_risk_scores()` runs at the end of `aggregate_employee_daily_metrics()`. The resulting `risk_score_snapshot` is written directly to `EmployeeDailyMetrics` rows in the same session — no second ETL pass.

**Cross-schema alert join.** `app.alerts` (Chirp) lives in the `app` schema. The ETL queries `Alert` via SQLAlchemy to populate alert counts on daily, hourly, and employee daily fact rows.

---

## Deployment

### Docker

Runs inside the `canary-web` container. No separate container for ETL. CLI commands execute within the Flask app context.

### AWS Target

- **Compute:** ECS/Fargate task for scheduled ETL runs (triggered by EventBridge cron)
- **Database:** RDS PostgreSQL 17 with `canary` database, `metrics` schema
- **Secrets:** `DATABASE_URL` via AWS Secrets Manager

### CI/CD

- Alembic migration must pass before deployment
- Integration tests (`test_metrics_etl.py`) must pass with `canary_test` database
- Row count verification in integration tests (write → read → delta check)

---

## Code Review Findings

### P0 — Blocks Production

| # | Finding | Description | Recommended Fix |
|---|---------|-------------|-----------------|
| 1 | **Employee names stored plaintext in dim_employee** | `dim_employee.employee_name` is PII stored in cleartext. This dimension is queried by the dashboard to resolve display names. | Apply field-level AES-256-GCM encryption using Canary's `crypto.py` pattern. Decrypt at read time in dashboard service layer. |
| 2 | **Database credentials in .env** | `DATABASE_URL` containing password is in a `.env` file, not a secrets manager. | Migrate to AWS Secrets Manager with `boto3` retrieval at startup. |
| 3 | **No audit logging for risk score writes** | `risk_score_snapshot` is written to `employee_daily_metrics` inline during ETL with no audit trail of who/what triggered the computation. `RiskScoreHistory` exists but is not populated by the ETL. | Populate `RiskScoreHistory` during ETL alongside `risk_score_snapshot` writes. |

### P1 — Before GA

| # | Finding | Description | Recommended Fix |
|---|---------|-------------|-----------------|
| 4 | **No data retention policy** | Metrics fact tables grow indefinitely. No automated purge for historical data beyond the active analysis window. | Implement retention: daily facts > 24 months archived/deleted, period facts retained indefinitely, scorecard snapshots > 24 months purged. |
| 5 | **ETL has no execution timeout** | `run_etl` can run indefinitely on a large merchant with years of data. No timeout or circuit breaker. | Add configurable timeout (default 30 minutes). Log and alert if exceeded. |
| 6 | **WeeklyScorecard / MonthlyScorecard tables not populated** | Schema defines these tables but no ETL or service writes to them. Dashboard reads from `period_metrics` directly. | Either wire scorecard population into the ETL or remove the unused tables from the schema. |
| 7 | **is_holiday field non-functional** | `DimDate.is_holiday` is always `False`. No holiday calendar import exists. Holiday-adjusted baseline calculations cannot work. | Implement US federal holiday import (static list or API) during `populate_dim_date`. |
| 8 | **ETL file location inconsistency** | `metrics_etl.py` lives at `services/metrics_etl.py` while dim_loader lives at `services/metrics/dim_loader.py`. Inconsistent with the codebase convention of service subdirectories. | Move to `services/metrics/etl.py`, update imports. Track as cleanup GRO issue. |

### P2 — Post-Launch

| # | Finding | Description | Recommended Fix |
|---|---------|-------------|-----------------|
| 9 | **Period aggregation full-rebuild is not incremental** | `aggregate_period_metrics` deletes and rebuilds all period rows for an entire fiscal year each run. Scales linearly with number of locations x fiscal years. | Partial-rebuild: only rebuild the current open period + one prior. |
| 10 | **No index on employee_daily_metrics.risk_score_snapshot** | Risk score queries scan all rows without a targeted index. | Add index on `(merchant_id, risk_score_snapshot)` for top-risk queries. |
| 11 | **Off-clock detection misses open shifts** | `_is_off_clock()` only considers timecards with non-NULL `end_at`. Open shifts are excluded. | Document as a known limitation. Optionally: use `start_at` only for partial detection. |

---

## Production Readiness Checklist

- [ ] PII encrypted at rest — `dim_employee.employee_name` needs field-level encryption (P0 #1)
- [ ] Secrets in AWS Secrets Manager — `DATABASE_URL` still in `.env` (P0 #2)
- [ ] Health check endpoint responds — implicit via Flask app health; no ETL-specific health
- [ ] Audit logging for sensitive operations — risk score writes lack audit trail (P0 #3)
- [ ] Data retention policy implemented — no retention policy exists (P1 #4)
- [ ] Rate limiting on public endpoints — N/A (ETL is internal, no public endpoints)
- [ ] Error responses don't leak internals — N/A (CLI output only)
- [x] Multi-tenant isolation — all tables have `merchant_id`, all queries scoped
- [x] Idempotent ETL — delete-then-insert pattern verified in code
- [x] Monetary precision — all money in cents as BigInteger, no float arithmetic
- [x] NRF 4-5-4 fiscal calendar — implemented and tested via FiscalCalendar service
