# Metrics & Analytics — Risk Scoring & Analytics Dashboard

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]], [[Brain/wiki/canary-data-model|Canary Data Model]]
**Architecture:** [[docs/sdds/canary/architecture|Canary Architecture SDD]]

> **Type:** App Service (Canary)
> **Status:** Operational — code review complete
> **Last updated:** 2026-04-13
> **Code location:** `Canary/canary/services/employee_risk_scoring.py`, `Canary/canary/services/dashboard.py`, `Canary/canary/services/dashboard_queries.py`, `Canary/canary/services/dashboard_tiles.py`, `Canary/canary/blueprints/analytics.py`, `Canary/canary/blueprints/analytics_mcp.py`, `Canary/canary/models/metrics/risk.py`
> **Split from:** Original `metrics-analytics.md` (7000 words, two deployable concerns)

**Companion SDD:** [[docs/sdds/canary/metrics-analytics|Metrics Analytics ETL]] — Star schema ETL pipeline, dimension loading, fact tables, period aggregation
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[Canary/docs/profiles/ops/Tom|Tom]] + [[Canary/docs/profiles/ops/Research|Research]] · **Operator role:** [[Canary/docs/profiles/ops/Jeremy|Jeremy]]

---

## Purpose

The Risk Scoring & Analytics Dashboard provides the read path and scoring layer on top of the metrics star schema. It computes employee risk scores using peer-relative z-score normalization, scores KPIs against configurable threshold bands for heatmap visualization, and exposes analytics data through REST and MCP endpoints. This is what merchants see when they open the Canary dashboard.

---

## Dependencies

| Dependency | Type | Required | What it provides |
|-----------|------|----------|-----------------|
| Metrics ETL Pipeline | Upstream service | Yes | Populated fact tables: `daily_metrics`, `employee_daily_metrics`, `period_metrics`, `employee_period_metrics` |
| PostgreSQL 17 (`growdirect_postgres`) | Infrastructure | Yes | `canary` database, `metrics` schema |
| Valkey 8 (`growdirect_valkey`) | Infrastructure | No | Session storage for JWT auth (DB 0) |
| Fiscal Calendar service | Internal | Yes | `get_current_fiscal_period()` for determining active period |

---

## Data Flow & PII Map

### What enters

- **Source:** Metrics schema fact tables (populated by ETL pipeline)
- **Trigger:** HTTP requests to `/api/analytics/*` endpoints or MCP tool calls

### What is stored

**Risk & ML tables:**

| Table | Purpose | PII Classification |
|-------|---------|-------------------|
| `entity_risk_scores` | Current risk score per entity (employee, card, device, location). SCD Type 1 — overwritten each scoring pass. | **sensitive** — `entity_id` can resolve to an employee; `risk_score` + `risk_category` + `factors` (JSON) constitute behavioral profiling of individuals |
| `risk_score_history` | Append-only audit trail of all scoring passes. | **sensitive** — same as entity_risk_scores, historical |
| `transaction_features` | ML feature vector per transaction (JSON). | **internal** — transaction-level, no direct PII; `risk_score` is per-transaction |
| `feature_definitions` | ML feature catalog (names, types, sources). | **public** — schema metadata only |
| `ml_models` | Trained model registry (versions, metrics). | **public** — model metadata only |
| `metric_baselines` | Statistical baselines (mean + stddev per metric). | **internal** — aggregate statistics, no PII |
| `velocity_baselines` | XPLOSS velocity baselines per time slot. | **internal** — aggregate statistics |

**Scoring & config tables:**

| Table | Purpose | PII Classification |
|-------|---------|-------------------|
| `scorecard_thresholds` | Per-merchant configurable threshold bands for heatmap. | **internal** — merchant configuration |
| `dashboard_config` | Per-merchant dashboard layout and display preferences. | **internal** — merchant preferences |
| `weekly_scorecard` | Pre-computed weekly KPI JSON snapshots. | **internal** — aggregate KPIs |
| `monthly_scorecard` | Pre-computed monthly KPI JSON snapshots. | **internal** — aggregate KPIs |

### What exits

- **REST API responses** — JSON payloads containing scored metrics, health scores, trend data, entity drilldowns (to authenticated merchant users only)
- **MCP tool responses** — same data via tool registry for AI-assisted queries (Owl)
- **Fox case context** — `entity_risk_scores` and `risk_score_history` queried by case management

---

## API Contract

### REST API — Analytics Blueprint

`Canary/canary/blueprints/analytics.py` — registered at `/api/analytics/`.

All endpoints require JWT authentication (`@jwt_required()`). All responses are merchant-scoped via `g.merchant_id`.

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/analytics/dashboard` | JWT | Current period summary with health score and heatmap-scored metrics |
| GET | `/api/analytics/trends?metric=<name>` | JWT | Trend data for a single metric across the last 6 fiscal periods. Default: `REFUND_RATE` |
| GET | `/api/analytics/top-risks` | JWT | Top risk employees and locations |
| GET | `/api/analytics/drilldown?entity_type=<type>&entity_id=<id>` | JWT | Scored metric detail for a single employee or location. Returns 400 if entity_id missing, 404 if no data |
| GET | `/api/analytics/export` | JWT | **Not implemented** — returns 501 |

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

**Error responses:**
- `400` — missing required parameter (entity_id)
- `404` — no data for the requested entity
- `501` — export endpoint not implemented

### MCP Server — Analytics MCP Blueprint

`Canary/canary/blueprints/analytics_mcp.py` — registered at `/analytics/`.

Built with `create_mcp_blueprint()` using the tool registry from `canary/services/analytics/tools.py`. Health endpoint reports `service: "canary-analytics"` and tool count. Inherits authentication from the MCP framework.

---

## Employee Risk Scoring Engine

### Algorithm

`canary/services/employee_risk_scoring.py` implements peer-relative risk scoring based on the Coles Cashier Risk Report methodology (Sysrepublic, 2011), modernized with z-score normalization.

**Per-category scoring:**
1. Compute rate for each employee (e.g., `void_count / transaction_count`)
2. Z-score normalize across the peer group (all employees for the merchant in the date range)
3. CDF transform to 0.0-1.0 (higher = more risk)
4. Direction-aware: invert for `lower_is_worse` metrics (e.g., `items_per_txn`, `sales_per_hour`)

**Total risk score:** Weighted average of all category scores. Default weight: 1.0 for each category.

**Minimum threshold:** Employees with fewer than 20 transactions (`MIN_TRANSACTION_THRESHOLD`) are excluded from peer comparison.

### Risk Categories (13)

| Category | Numerator | Denominator | Direction |
|----------|-----------|-------------|-----------|
| void_rate | void_count | transaction_count | higher_is_worse |
| refund_rate | refund_count | transaction_count | higher_is_worse |
| no_sale_rate | no_sale_count | transaction_count | higher_is_worse |
| custom_amount_rate | custom_amount_count | transaction_count | higher_is_worse |
| discount_rate | discount_total_cents | gross_sales_cents | higher_is_worse |
| alert_rate | alert_count | transaction_count | higher_is_worse |
| items_per_txn | total_items_sold | transaction_count | lower_is_worse |
| gc_load_rate | gift_card_load_count | transaction_count | higher_is_worse |
| loyalty_redeem_rate | loyalty_redeem_count | transaction_count | higher_is_worse |
| shrinkage_rate | shrinkage_count | transaction_count | higher_is_worse |
| off_clock_rate | off_clock_txn_count | transaction_count | higher_is_worse |
| fixed_discount_rate | discount_fixed_count | discount_count | higher_is_worse |
| sales_per_hour | sales_per_hour_cents | (constant 1) | lower_is_worse |

### Risk Category Mapping

`_score_to_category()` in `dim_loader.py`:
- 0.0 - 0.3 = `low`
- 0.3 - 0.7 = `medium`
- 0.7 - 1.0 = `high`

`EntityRiskScore.risk_category` adds a fourth tier:
- `low`, `medium`, `high`, `critical`

### Heatmap Scoring

`ScorecardThreshold` defines per-merchant threshold bands as percentages of baseline:

| Band | Range | Color |
|------|-------|-------|
| normal | < `normal_upper_pct` (e.g., < 100%) | green |
| watch | `normal_upper_pct` to `watch_upper_pct` (e.g., 100-110%) | yellow |
| review | `watch_upper_pct` to `review_upper_pct` (e.g., 110-120%) | orange |
| investigate | >= `review_upper_pct` | red |

Direction is `higher_is_worse` (default) or `lower_is_worse`. Thresholds are seeded with platform defaults on merchant onboarding and are merchant-configurable.

### SRA v2 (Shrink Risk Assessment)

Computed at the period level during period aggregation:
```
sra_total_cents = refund_amount_cents + void_total_cents + abs(cash_variance_cents) + discount_total_cents
sra_pct_sales   = (sra_total_cents / gross_sales_cents) * 100
```

Stored on `period_metrics.sra_total_cents` and `period_metrics.sra_pct_sales`.

---

## Operations

### Startup / Health

Analytics endpoints are part of the Canary Flask app. No separate process.

MCP health check: `GET /analytics/health` returns `{"service": "canary-analytics", "healthy": true, "tools": <count>}`.

### Failure Modes

| Failure | Impact | Recovery |
|---------|--------|----------|
| No period_metrics data (new merchant) | Dashboard returns empty response | Not an error — run ETL first to populate |
| No baselines (cold start) | All metrics scored as "investigate" | Baselines populate after first full period of data |
| Employee risk scoring with < 20 transactions | Employee excluded from peer comparison, no risk score | By design — insufficient data for meaningful comparison |
| Dashboard service exception | Individual endpoint returns 500 | Check logs; most errors are data-related (missing fiscal period, null baseline) |
| MCP tool registry failure | AI-assisted queries fail | Analytics REST endpoints still work independently |

### Monitoring

| Metric | Alert Threshold | Notes |
|--------|----------------|-------|
| `/api/analytics/dashboard` response time | > 2 seconds | May indicate missing indexes or large period tables |
| 5xx rate on analytics endpoints | > 1% | Investigate data quality or missing fiscal periods |
| MCP tool call failures | Any | Check MCP server health endpoint |

### Configuration

| Setting | Source | Default | Notes |
|---------|--------|---------|-------|
| `DATABASE_URL` | `.env` | — | PostgreSQL connection |
| Dashboard refresh interval | `DashboardConfig.refresh_interval_seconds` | 300s (5 min) | Per-merchant, stored in DB |
| Scorecard thresholds | `ScorecardThreshold` rows | Seeded defaults | Per-merchant, per-metric |
| Risk scoring weights | `DEFAULT_WEIGHTS` in `employee_risk_scoring.py` | 1.0 for all 13 categories | Hardcoded, not yet per-merchant configurable |
| Min transaction threshold | `MIN_TRANSACTION_THRESHOLD` | 20 | Employees below this are excluded from risk scoring |

---

## Deployment

### Docker

Runs inside the `canary-web` container. Analytics blueprint and MCP blueprint are registered in the Flask app factory. No separate container.

### AWS Target

- **Compute:** ECS/Fargate — part of the Canary web service
- **Database:** RDS PostgreSQL 17
- **Secrets:** `DATABASE_URL` via AWS Secrets Manager

### CI/CD

- Route tests (`test_analytics_routes.py`) must pass
- Smoke test (`test_analytics_smoke.py`) must pass with real data
- MCP health endpoint must respond

---

## Code Review Findings

### P0 — Blocks Production

| # | Finding | Description | Recommended Fix |
|---|---------|-------------|-----------------|
| 1 | **Employee risk scores are PII-adjacent with no access control** | `entity_risk_scores` contains behavioral profiling data (risk_score, risk_category, factors JSON) linked to employee_id. Any authenticated user for the merchant can view all employee risk data. No role-based access control for risk data. | Implement RBAC: restrict risk score visibility to manager/owner roles. Log access to risk score endpoints. |
| 2 | **Risk score factors stored as plaintext JSON** | `EntityRiskScore.factors` and `RiskScoreHistory.factors` contain detailed behavioral breakdown (e.g., "void_rate: 0.85, refund_rate: 0.72"). This data could be used to identify employees even without names. | Encrypt `factors` column at rest. Consider whether factor detail should be available in the API or only in admin views. |
| 3 | **Database credentials in .env** | Same as ETL pipeline — `DATABASE_URL` in `.env`. | AWS Secrets Manager. |

### P1 — Before GA

| # | Finding | Description | Recommended Fix |
|---|---------|-------------|-----------------|
| 4 | **No audit logging for risk score access** | Dashboard endpoints serve employee risk data with no audit trail of who viewed it. Employment law in some jurisdictions requires logging access to employee performance data. | Add audit log entries for `/api/analytics/drilldown?entity_type=employee` and `/api/analytics/top-risks` calls. |
| 5 | **Risk scoring weights are hardcoded** | `DEFAULT_WEIGHTS` assigns 1.0 to all 13 categories. No per-merchant customization mechanism exists. Different merchant types (restaurant vs retail) need different weight profiles. | Add a `risk_scoring_config` table or extend `dashboard_config` with weight overrides. |
| 6 | **Export endpoint is a stub (501)** | `GET /api/analytics/export` returns 501. No implementation. Merchants will need data export for their own LP investigations. | Implement CSV/PDF export of period metrics and risk scores. |
| 7 | **No rate limiting on analytics endpoints** | All analytics endpoints lack rate limiting. An authenticated user could enumerate all employee risk data rapidly. | Add Flask-Limiter: 60 requests/minute per merchant for analytics endpoints. |
| 8 | **Drilldown exposes limited metrics** | `_fetch_entity_metrics` only returns 5 KPIs (REFUND_COUNT, VOID_COUNT, NO_SALE_COUNT, DISCOUNT_TOTAL, CUSTOM_AMOUNT_COUNT) for employee drilldown. The model stores 20+ metrics. | Expand drilldown to include all employee_period_metrics fields, or make the metric set configurable. |
| 9 | **RiskScoreHistory not populated by ETL** | The `risk_score_history` table exists but is never written to. The `risk_score_snapshot` on `employee_daily_metrics` provides daily snapshots but no formal history table is used. | Wire `risk_score_history` inserts into the ETL or risk scoring service. |

### P2 — Post-Launch

| # | Finding | Description | Recommended Fix |
|---|---------|-------------|-----------------|
| 10 | **Velocity baselines not populated** | `VelocityBaseline` schema exists (XPLOSS equivalent) but no service populates it. The velocity anomaly detection feature is schema-only. | Implement velocity baseline computation as part of the ETL or a separate scheduled job. |
| 11 | **Dashboard health score computation undocumented** | `health_score` appears in dashboard response but the computation formula is not documented in the SDD or in code comments. | Document the health score formula in code and in this SDD. |
| 12 | **MCP tool registry contents undocumented** | `analytics_mcp_bp` references `canary/services/analytics/tools.py` but the specific tools registered are not enumerated in this SDD. | Enumerate MCP tools with their parameters, auth requirements, and PII access levels. |

---

## Production Readiness Checklist

- [ ] PII encrypted at rest — risk score factors need encryption (P0 #2)
- [ ] Secrets in AWS Secrets Manager — `DATABASE_URL` in `.env` (P0 #3)
- [x] Health check endpoint responds — MCP health at `/analytics/health`
- [ ] Audit logging for sensitive operations — no logging for risk data access (P1 #4)
- [ ] Data retention policy implemented — no retention for risk_score_history (grows indefinitely)
- [ ] Rate limiting on public endpoints — no rate limiting on analytics (P1 #7)
- [ ] Error responses don't leak internals — verified; errors return structured JSON with safe messages
- [x] Multi-tenant isolation — all queries scoped to `g.merchant_id` from JWT
- [x] Authentication on all endpoints — `@jwt_required()` on every route
- [ ] RBAC for employee risk data — all merchant users see all risk data (P0 #1)
