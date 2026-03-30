---
type: workorder
domain: owl
status: active
created: 2026-03-15
updated: 2026-03-19
---
# ALX Sprint Dispatch — Owl + Metrics Scan

**Date:** 2026-03-15
**Sprint:** Owl Intelligence + Metrics Pipeline
**Dispatched by:** Jeffe via Cowork
**Skills:** canary-blueprint → canary-tdd → canary-assembly → canary-verify → canary-qa → canary-ship

---

## Situation

The Owl is 100% built (13 core files, 8 MCP tools, 4 memory tables, personality routing, search subsystem, delta engine, health check reports, closed-loop action dispatch). What it lacks is live metrics data — the metrics ETL pipeline is stubbed, all 5 metrics tables have 0 rows, and the Owl's dashboard/health check tools can't surface trends or SRA scoring without data.

Additionally, the risk dictionary currently lives on the dashboard page. Jeffe wants it moved to the Owl page, replacing the existing basic search tiles with risk dictionary entries. The Owl page becomes the primary intelligence surface.

**Key SDDs:** SDD-032 (metrics star schema), SDD-020 (dashboard service), v2/owl.md (consolidated Owl SDD), SDD-040 (ETL batch), SDD-004 (initial data sync)

**Related GRO Issues:** GRO-226 (metrics ETL stub), GRO-145 (dim_date fiscal calendar), GRO-129 (Owl brain), GRO-146 (dashboard metrics), GRO-147 (heatmap scoring)

---

## Work Items (dependency order)

### WI-1: Metrics ETL Pipeline [P0 — Urgent]

**Branch:** `gro-226-metrics-etl-pipeline`
**Est:** 3-4h | **GRO:** GRO-226 | **SDDs:** SDD-032, SDD-040

**Problem:** The Airflow DAG at `devops/airflow/dags/canary_metrics_etl.py` is 100% stubbed — every task logs "Jeremy to implement" and does nothing. The `metrics_etl.py` service has 4 working aggregation functions but nothing triggers them. All 5 metrics tables have 0 rows.

**Memory recall before starting:**
```
memory_recall("SDD-032 metrics star schema")
memory_recall("SDD-040 ETL batch dead letter queue")
memory_recall("metrics_etl aggregation functions")
```

**Blueprint:**
- Replace the stubbed Airflow DAG with a Flask-native ETL runner at `canary/services/metrics/etl_runner.py`
- Wire the 4 existing aggregation functions from `metrics_etl.py`: `aggregate_daily_metrics()`, `aggregate_hourly_metrics()`, `aggregate_employee_daily_metrics()`, `aggregate_product_daily_metrics()`
- Add period aggregation via `period_aggregation.py` (already implemented per GRO-146)
- Add CLI entry point: `flask metrics run-etl`
- Add before/after row count logging for every table
- Idempotent: re-running for the same date range should not duplicate rows

**TDD first (canary-tdd):**
```python
# tests/integration/test_etl_runner.py
def test_etl_populates_daily_metrics():
    """Row count goes from 0 → N after ETL run."""
    before = session.query(DailyMetrics).count()
    run_etl(merchant_id="MLE55GCYANCYT", date_range=("2026-03-01", "2026-03-14"))
    after = session.query(DailyMetrics).count()
    assert after > before
    assert after == expected_days * locations

def test_etl_idempotent():
    """Running twice produces same row count."""
    run_etl(...)
    count_1 = session.query(DailyMetrics).count()
    run_etl(...)
    count_2 = session.query(DailyMetrics).count()
    assert count_1 == count_2

def test_etl_populates_all_five_tables():
    """All 5 metrics tables have rows after full ETL."""
    run_etl(...)
    for model in [DailyMetrics, HourlyMetrics, EmployeeDailyMetrics, ProductDailyMetrics, PeriodMetrics]:
        assert session.query(model).count() > 0
```

**Verify (canary-verify):**
- Row counts > 0 in all 5 tables
- `daily_metrics.transaction_count` sum matches `sales.transactions` count for same date range
- No orphaned rows (all merchant_ids exist in app.merchants)
- `period_metrics.sra_total_cents` = refund + void + cash_variance + discounts

**Completeness Gate:** Data goes in (ETL writes), data comes out (query returns real numbers), row counts match source, API contract honored.

---

### WI-2: Dimension Table Population [P0 — Urgent]

**Branch:** `gro-145-dimension-tables`
**Est:** 2-3h | **GRO:** GRO-145 | **SDDs:** SDD-032, SDD-004

**Problem:** `dim_date`, `dim_location`, `dim_employee` models exist in `canary/models/metrics/dimensions.py` but tables are empty. Star schema joins fail without dimensions. The fiscal calendar service exists (GRO-145 done) but `dim_date` isn't populated with fiscal fields.

**Memory recall before starting:**
```
memory_recall("SDD-032 metrics star schema")
memory_recall("fiscal calendar 4-5-4 NRF")
memory_recall("dim_date dimension table")
```

**Blueprint:**
- Build `canary/services/metrics/dim_loader.py` with 3 functions:
  - `populate_dim_date(start_year=2024, end_year=2027)` — generate calendar rows, apply NRF 4-5-4 fiscal fields via `fiscal_calendar` service
  - `populate_dim_location(merchant_id)` — sync from `app.locations` (Square Locations API data)
  - `populate_dim_employee(merchant_id)` — sync from `app.employees` (Square Team Members API data)
- Register CLI: `flask metrics load-dims`
- Idempotent: upsert pattern, don't duplicate on re-run

**TDD first (canary-tdd):**
```python
def test_dim_date_has_fiscal_fields():
    populate_dim_date(2024, 2027)
    row = session.query(DimDate).filter_by(date_key=date(2026, 3, 15)).one()
    assert row.fiscal_year is not None
    assert row.fiscal_week_of_year is not None
    assert row.day_name == "Sunday"

def test_dim_date_row_count():
    populate_dim_date(2024, 2027)
    count = session.query(DimDate).count()
    assert count >= 1095  # 3 years minimum

def test_dim_location_matches_source():
    populate_dim_location("MLE55GCYANCYT")
    source = session.query(Location).filter_by(merchant_id="MLE55GCYANCYT").count()
    dim = session.query(DimLocation).filter_by(merchant_id="MLE55GCYANCYT").count()
    assert dim == source
```

**Verify:** dim_date 1095+ rows, fiscal_year not null, dim_location/dim_employee cross-reference to source counts.

---

### WI-3: Risk Dictionary → Owl Page [P1 — High]

**Branch:** `risk-dictionary-owl-page`
**Est:** 2-3h | **GRO:** NEW (create) | **SDDs:** SDD-020, v2/owl.md

**Problem:** The dashboard has a risk dictionary with structured risk categories. The Owl page has basic search tiles that don't leverage this intelligence. Jeffe directive: move the risk dictionary to the Owl page, replace the existing tiles with risk dictionary ones.

**Memory recall before starting:**
```
memory_recall("owl MCP tools API")
memory_recall("dashboard service metrics orchestration")
memory_recall("risk dictionary categories")
memory_recall("chirp detection rules")
```

**Blueprint:**
- Extract risk dictionary data structure from dashboard template/service
- Create `GET /owl/risk-dictionary` endpoint returning all risk categories with metadata
- Build Owl page risk tile template — each tile shows: category name, description, severity indicator, current alert count
- Wire tile click → Owl search query scoped to that risk category (uses existing `search` MCP tool)
- Remove risk dictionary section from dashboard template
- Keep dashboard focused on KPI metrics and scorecards

**TDD first:**
```python
def test_risk_dictionary_endpoint():
    response = client.get("/owl/risk-dictionary")
    assert response.status_code == 200
    data = response.json
    assert len(data["categories"]) > 0
    assert all("name" in c and "severity" in c for c in data["categories"])

def test_risk_tile_triggers_owl_search():
    response = client.post("/owl/tools/search", json={
        "params": {"query": "HIGH_EMPLOYEE_REFUND_RATE", "limit": 10},
        "context": {"merchant_id": "MLE55GCYANCYT"}
    })
    assert response.status_code == 200

def test_dashboard_renders_without_risk_section():
    response = client.get("/m/dashboard")
    assert response.status_code == 200
    assert "risk-dictionary" not in response.data.decode()
```

**Verify:** Owl page loads with risk tiles. Each tile click returns relevant Owl intelligence. Dashboard renders clean without risk section. No 500s on either page.

**→ Run jeffe-review in HOLD SCOPE mode after completion (product-facing change).**

---

### WI-4: Owl Metrics Integration [P1 — High]

**Branch:** `owl-metrics-integration`
**Est:** 3-4h | **GRO:** GRO-129+ | **SDDs:** v2/owl.md, SDD-020

**Depends on:** WI-1 and WI-2 must be merged first (metrics tables need data).

**Problem:** Owl's `dashboard` and `check_heartbeat` tools pull from alerts and scores only. They don't query the metrics star schema for trends, period comparisons, or SRA scoring. PhD personality can't answer "What's my SRA this period?" because it has no metrics access.

**Memory recall before starting:**
```
memory_recall("owl context assembly 4 windows")
memory_recall("owl dashboard MCP tool")
memory_recall("period metrics SRA calculation")
memory_recall("owl personality routing PhD analytics")
```

**Blueprint:**
- Expand Owl `dashboard` MCP tool in `canary/services/owl/tools.py` to query `daily_metrics` + `period_metrics` for current merchant
- Add metrics summary to health check's 4-window context assembly — expand Window 3 (Heartbeat + Dashboard) to include: current period SRA, daily transaction trend (7 days), refund/void rate trend
- Add metrics tables to `search/registry.py` allowlist so PhD personality can query them
- Add period-over-period comparison to health check report output
- Enable PhD to handle: "What's my SRA?", "Show refund trends", "Compare this period to last period"

**TDD first:**
```python
def test_dashboard_tool_returns_metrics():
    result = dashboard_tool(merchant_id="MLE55GCYANCYT")
    assert "daily_trend" in result
    assert "period_sra" in result
    assert result["period_sra"]["sra_pct_sales"] is not None

def test_health_check_includes_metrics():
    report = generate_health_report(merchant_id="MLE55GCYANCYT", alerts=[])
    assert "period_comparison" in report or "sra" in report.get("analytics_assessment", "").lower()

def test_phd_routes_metrics_question():
    routed = route_message("What's my SRA this period?")
    assert routed.personality.name == "phd"
```

**Verify:** Owl dashboard returns real metrics numbers. Health check report includes trend data. PhD answers SRA questions with actual values from period_metrics. No hardcoded responses.

**→ Run jeffe-review in HOLD SCOPE mode after completion.**

---

### WI-5: Auto Scan + Orphan Report [P2 — Normal]

**Branch:** `scan-refresh-march`
**Est:** 1-2h | **GRO:** NEW (create) | **SDDs:** SDD-057

**Problem:** The `auto_scan.py` and `scan_runner.sh` haven't been run against the current codebase. After all recent work (MCP servers, dashboard, owl, metrics), traceability matrix and orphan report are stale.

**Blueprint:**
- Run `devops/scripts/scan_runner.sh --scan-only`
- Review `ORPHAN_REPORT.md` output for unwired routes, untested services
- Run `--analyze` if Qwen available for gap analysis
- File GRO issues for any critical orphans
- Store scan results to pgvector memory for future recall

**Verify:** `devops/scan/` has fresh outputs dated 2026-03-15. `TRACEABILITY_MATRIX.md` covers all current blueprints. Orphan count known and documented. Critical gaps filed.

---

## Execution Rules

1. **One branch at a time.** Merge before starting the next item.
2. **canary-blueprint first.** Every work item starts with a plan. Recall SDDs. Check scope.
3. **canary-tdd before code.** RED test first. Especially row count tests.
4. **canary-verify before claiming done.** Row counts. Pipeline proof. North Star check.
5. **canary-qa before shipping.** Diff-aware mode. Health score >= 75 to ship.
6. **canary-ship to close.** Pre-landing review. Bisectable commits. PR with evidence.
7. **jeffe-review for product changes.** WI-3 and WI-4 require HOLD SCOPE review.
8. **No lazy pipes.** A route returning hardcoded JSON is not done. A service that doesn't persist is not done.

## One-Line Test

> Does this work help GrowDirect mint the pool, seal the event, or collect the sat?

> "We don't want to add to the stress. We want to ease it." — Jeffe
