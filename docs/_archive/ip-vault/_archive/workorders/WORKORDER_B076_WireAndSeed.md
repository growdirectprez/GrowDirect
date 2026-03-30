---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# WORK ORDER B-076: Wire to Data + Seed — Make the Numbers Real
**Date:** March 1, 2026
**Owner:** ALX
**Assigned to:** Jeremy (primary)
**Priority:** 🔴 HIGH — B-075 scaffold is visible but all data is hardcoded
**Depends on:** B-075 (COMPLETE — scaffold shipped, all pages navigable)
**Parallel with:** B-070 (QA/UAT gate — does not block this)
**Branch:** `frontend-scaffold` (continue from B-075 work)

---

## 1. Objective

> "Leave the icons — we need to see the website."
> — Jeffe, March 1, 2026

B-075 shipped the shell. Jeffe can click through every page. But every number is a Python dict. This work order replaces the hardcoded demo data with real database queries and seeds the database so there's something worth looking at.

**What "done" looks like:** Jeffe opens `localhost:5050`, sees Sunrise Coffee's dashboard with real numbers from the database. Changes a chirp threshold in Settings, refreshes, sees the update. The data is alive.

---

## 2. Current State (What B-075 Delivered)

### What works now
- `wsgi_b075.py` boots on port 5050, serves both template directories
- 20 routes, all return HTTP 200
- Dark theme, v2.0 design system, sidebar navigation, mobile companion
- Zero console errors, zero server errors

### What's fake
Every page renders from hardcoded Python dicts in `canary/blueprints/views_wired.py`:
- `_demo_stats()` — dashboard stat cards
- `_demo_alerts()` — dashboard recent alerts table
- `_demo_activity()` — dashboard activity timeline
- `_demo_chirps()` — chirps management table
- `_demo_transactions()` — transactions list
- `_demo_cases()` — Fox kanban board
- `_demo_employees()` — employee card grid
- `_demo_audit_log()` — audit log table
- `_demo_settings()` — settings 4-tab content

---

## 3. The Problem (Why This Isn't Just "Replace Demo Dicts")

The survey of existing wired blueprints revealed **field name mismatches** between the blueprints and the actual SQLAlchemy models. The blueprints were written against an earlier schema draft. They will crash if called against the real database.

### Blueprint → Model Mismatches (Must Fix First)

| Blueprint | References | Actual Model Field | Fix |
|---|---|---|---|
| `alerts_wired.py` | `alert.score` | Not on `Alert` model | Remove or compute from `severity` |
| `alerts_wired.py` | `alert.status` | Not on `Alert` — lives in `AlertHistory` | Join `AlertHistory` for current status |
| `alerts_wired.py` | `alert.transaction_id` | Not on `Alert` — use `source_table` + `source_id` | Fix reference pattern |
| `employees_wired.py` | `employee.name` | `employee_name` | Rename |
| `employees_wired.py` | `employee.phone` | Not on model | Remove |
| `employees_wired.py` | `filter_by(date_range=...)` | Invalid SQLAlchemy | Fix to `.filter(Transaction.transaction_date.between(...))` |
| `employees_wired.py` | `risk_score.score`, `.trend`, `.contributing_rules` | `.risk_score`, `.risk_category`, `.factors` | Rename |
| `merchants_wired.py` | `merchant.name` | `merchant_name` | Rename |
| `merchants_wired.py` | `merchant.business_name`, `.email`, `.phone` | Not on model | Remove or add to model |
| `merchants_wired.py` | `settings.currency`, `.notification_preferences` | Not on `MerchantSettings` | Add columns or use `label_overrides` JSON |
| `locations_wired.py` | `location.name` | `location_name` | Rename |
| `locations_wired.py` | `location.address` | `address_line1` + `city` + `state` | Compose from parts |
| `locations_wired.py` | `DailyMetrics.date` | `metric_date` | Rename |
| `locations_wired.py` | `metric.total_sales_cents`, `.total_refunds_cents` | `gross_sales_cents`, `refund_amount_cents` | Rename |

### Missing FoxCaseService Methods

| Method Called by `fox_wired.py` | Status |
|---|---|
| `get_cases(merchant_id, status, created_after, page, limit)` | MISSING |
| `get_case_by_id(case_id, merchant_id)` | MISSING |
| `add_subject(case_id, type, entity_id, name, role)` | MISSING |
| `get_case_evidence(case_id)` | MISSING |
| `get_evidence_by_id(evidence_id)` | MISSING |

### Seed Data Gaps

| Data | Existing (`level_b_demo.py`) | Needed for B-076 |
|---|---|---|
| Merchant | 1 (Offset Coffee) | 1 (Sunrise Coffee — match B-075 vocabulary) |
| Location | 1 | 1 (Torrance) |
| Employees | 2 | 6 (match B-075 employee cards) |
| Transactions | 3 | 30+ (mix of SALE, RETURN, VOID, NO_SALE) |
| Alerts | 2 | 8+ (2 critical, 3 warning, 3 info) |
| Fox Cases | 1 | 3 (1 new, 1 investigating, 1 closed) |
| Audit Log | 0 | 12+ entries |
| Detection Rules | 2 | All 26 from `en-US.json` locale pack |
| MerchantRuleConfig | 0 | 19 active rule configs |
| MerchantSettings | 0 | 1 row (timezone, locale, preferences) |
| DailyMetrics | 0 | 7 days of metrics |
| EmployeeDailyMetrics | 0 | 7 days × 6 employees |
| Cash Drawer Shifts | 1 | 4 shifts (2 days × 2 registers) |

---

## 4. The Work (Three Phases)

### Phase A: Fix the Plumbing (Jeremy — 2-3 hours)
**Goal:** Existing wired blueprints can be called against the real database without crashing.

**Tasks:**
1. **Fix `alerts_wired.py` field references:**
   - Remove `alert.score` — use `alert.severity` for display
   - Replace `alert.status` with a join to `AlertHistory` (most recent by `alert_id`)
   - Replace `alert.transaction_id` with `alert.source_table` / `alert.source_id` lookup
   - Verify `list_alerts()` and `get_alert()` work against real `Alert` + `AlertHistory` tables

2. **Fix `employees_wired.py` field references:**
   - `employee.name` → `employee.employee_name`
   - Remove `employee.phone` reference
   - Fix `filter_by(date_range=...)` → `.filter(Transaction.transaction_date.between(start, end))`
   - Fix `EntityRiskScore` references: `.score` → `.risk_score`, `.trend` → `.risk_category`, `.contributing_rules` → `.factors`

3. **Fix `merchants_wired.py` field references:**
   - `merchant.name` → `merchant.merchant_name`
   - Remove `merchant.business_name`, `.email`, `.phone` (or add to model if needed)
   - Fix `MerchantSettings` references — currency lives on `Merchant` model, notification_preferences can use `label_overrides` JSON for now

4. **Fix `locations_wired.py` field references:**
   - `location.name` → `location.location_name`
   - `location.address` → compose from `address_line1`, `city`, `state`, `postal_code`
   - `DailyMetrics.date` → `DailyMetrics.metric_date`
   - `metric.total_sales_cents` → `metric.gross_sales_cents`
   - `metric.total_refunds_cents` → `metric.refund_amount_cents`

5. **Implement missing `FoxCaseService` methods:**
   - `get_cases(merchant_id, status=None, created_after=None, page=1, limit=20)` — query `FoxCase` with optional filters, paginate
   - `get_case_by_id(case_id, merchant_id)` — single case with subjects, alerts, evidence count
   - `add_subject(case_id, subject_type, entity_id, name, role)` — insert `FoxSubject`
   - `get_case_evidence(case_id)` — query `FoxEvidence` by case_id
   - `get_evidence_by_id(evidence_id)` — single evidence record

**Validation:** Each fixed blueprint can be imported without `AttributeError`. Run `python -c "from canary.blueprints.alerts_wired import alerts_bp"` etc.

### Phase B: Seed Data (Jeremy — 2-3 hours)
**Goal:** `make seed` populates all three databases with Sunrise Coffee demo data. Idempotent — safe to run multiple times.

**File:** `canary/seeds/demo_seed.py`

**Approach:** Follow `level_b_demo.py` pattern (raw `psycopg2`, `INSERT ... ON CONFLICT DO NOTHING`). But expand significantly:

**canary_app database:**
```
1  Merchant:           Sunrise Coffee (merchant_id: demo_merch_sunrise_001)
1  Location:           Torrance, CA
6  Employees:          Alex R. (owner), Marcus T. (lead), Sarah K., Jordan P.,
                       Casey M., Riley B. — matching B-075 demo data names
1  User:               Alex (owner role)
26 DetectionRules:     All C-001 through C-804 from en-US.json locale pack
19 MerchantRuleConfig: Active rule configurations with thresholds
8  Alerts:             2 critical, 3 warning, 3 info — across rule categories
8  AlertHistory:       Matching status records (3 new, 2 acknowledged, 2 resolved, 1 investigating)
3  FoxCases:           1 open (post-void), 1 investigating (no-sale pattern), 1 closed (cash variance)
3  FoxSubjects:        Linked to cases above
6  FoxCaseTimeline:    2 per case
12 AuditLog:           Mix of alert/chirp/auth/config/case types
1  MerchantSettings:   timezone, locale, date/time format, label overrides
```

**canary_sales database:**
```
30 Transactions:       15 SALE, 5 RETURN, 4 VOID, 3 NO_SALE, 2 PAID_OUT, 1 PAID_IN
                       Mix of cash + card. Spread across 2 days. Amounts: $3.50–$47.50
4  CashDrawerShifts:   2 days × 2 registers. One with -$18 variance.
12 CashDrawerEvents:   Mix of NO_SALE, PAID_IN, PAID_OUT, CASH_TENDER_PAYMENT
```

**canary_metrics database:**
```
7  DailyMetrics:       7 days. Revenue $3,800–$4,500/day. 18–25 txns/day.
42 EmployeeDailyMetrics: 7 days × 6 employees. Risk scores 12–85.
7  HourlyMetrics:      Today only, 7am–2pm (coffee shop hours)
```

**Employee seed data must match B-075 views_wired.py demo names exactly:**

| Name | Role | Risk Score | TXNs | Refunds | Voids |
|---|---|---|---|---|---|
| Alex R. | Owner / Manager | 12 (green) | 34 | 1 | 0 |
| Marcus T. | Barista — Lead | 78 (red) | 48 | 6 | 2 |
| Sarah K. | Barista | 45 (yellow) | 31 | 2 | 1 |
| Jordan P. | Barista | 62 (orange) | 27 | 4 | 3 |
| Casey M. | Barista — Weekend | 18 (green) | 15 | 0 | 0 |
| Riley B. | Barista — New | 8 (green) | 12 | 1 | 0 |

**Run:** `make seed` → connects to all three databases, seeds, reports row counts.

**Requirements:**
- Idempotent: `ON CONFLICT DO NOTHING` for all inserts
- Fast: < 30 seconds total
- Env vars: reads `CANARY_APP_DB_URL`, `CANARY_SALES_DB_URL`, `CANARY_METRICS_DB_URL`
- Fallback: if no DB URLs set, print clear error with instructions

### Phase C: Wire Views to Real Data (Jeremy — 3-4 hours)
**Goal:** Replace every `_demo_*()` function in `views_wired.py` with real database queries.

**Wiring map — each demo function replaced with real query:**

| Demo Function | Replace With | Database | Key Query |
|---|---|---|---|
| `_demo_stats()` | `DailyMetrics` aggregate | canary_metrics | Today's `DailyMetrics` row for merchant + sum |
| `_demo_alerts()` | `Alert` + `AlertHistory` join | canary_app | 8 most recent alerts with current status |
| `_demo_activity()` | `AuditLog` | canary_app | 6 most recent audit entries |
| `_demo_chirps()` | `Alert` + `RULE_MAP` | canary_app | All active alerts with rule metadata |
| `_demo_transactions()` | `Transaction` | canary_sales | Today's transactions, newest first |
| `_demo_cases()` | `FoxCase` + `FoxSubject` | canary_app | All cases grouped by status |
| `_demo_employees()` | `Employee` + `EmployeeDailyMetrics` | canary_app + canary_metrics | Employees with latest risk scores |
| `_demo_audit_log()` | `AuditLog` | canary_app | All entries, newest first |
| `_demo_settings()` | `MerchantSettings` + `MerchantRuleConfig` + `DetectionRule` | canary_app | Settings row + active rules + integrations |

**Pattern for each replacement:**
```python
# Before (B-075 demo):
def _demo_stats():
    return {"revenue": "$4,250.00", "chirps": 3, ...}

# After (B-076 wired):
def _get_stats(merchant_id):
    """Dashboard stats from DailyMetrics."""
    from canary.models.metrics.facts import DailyMetrics
    from canary.models.session_factory import MetricsSession
    today = date.today()
    row = MetricsSession.query(DailyMetrics).filter_by(
        merchant_id=merchant_id, metric_date=today
    ).first()
    if not row:
        return _demo_stats()  # graceful fallback
    return {
        "revenue": f"${row.gross_sales_cents / 100:,.2f}",
        "chirps": row.alert_count,
        "transactions": row.transaction_count,
        "health": _calculate_health(row),
    }
```

**Critical design rule:** Every wired function must have a **graceful fallback** to the demo data. If the DB is not available or the table is empty, show the hardcoded data instead of crashing. This lets Jeffe always see something.

**Views that need wiring (in priority order):**
1. Dashboard (`/dashboard`) — stats, alerts, activity
2. Chirps (`/chirps`) — alert list with filters
3. Transactions (`/transactions`) — transaction list
4. Employees (`/employees`) — employee grid with risk scores
5. Fox Cases (`/fox/cases`) — kanban board
6. Audit Log (`/admin/audit-log`) — audit entries
7. Settings (`/settings`) — merchant settings + chirp rules
8. Mobile Today (`/companion/today-v2`) — greeting + chirp count

---

## 5. What to Skip (for now)

| Item | Reason |
|---|---|
| Real-time data refresh (SSE/WebSocket) | Manual refresh is fine for demo |
| Write operations (resolve chirp, update settings) | Read-only wiring first. Write comes in Sprint 7. |
| Square API live data | Use seed data. B-070 handles production Square integration. |
| Metrics aggregation pipeline | Seed metrics directly. Airflow pipeline is Sprint 7. |
| Cross-database joins | Use separate queries per DB, compose in Python |

---

## 6. Acceptance Criteria

| # | Criteria | Verified by |
|---|---|---|
| AC-1 | `make seed` populates all 3 databases in < 30 seconds | Jeremy |
| AC-2 | `make seed` is idempotent — running twice produces no errors or duplicates | Jeremy |
| AC-3 | Dashboard stat cards show values from `DailyMetrics` (not hardcoded) | Jim |
| AC-4 | Dashboard alerts table shows rows from `Alert` + `AlertHistory` | Jim |
| AC-5 | Chirps table shows real alerts with correct rule names from `RULE_MAP` | Jim |
| AC-6 | Transactions table shows 30+ rows from `canary_sales.Transaction` | Jim |
| AC-7 | Fox kanban shows 3 cases from `FoxCase` (1 per status column) | Jim |
| AC-8 | Employees grid shows 6 employees with risk scores from DB | Jim |
| AC-9 | Audit log shows 12+ entries from `AuditLog` | Jim |
| AC-10 | Settings General tab shows Sunrise Coffee from `MerchantSettings` | Jim |
| AC-11 | Settings Chirp Rules tab shows 19 rules from `MerchantRuleConfig` | Jim |
| AC-12 | If DB is unavailable, all pages fall back to demo data (no crashes) | Jeremy |
| AC-13 | No new JavaScript console errors | Jim |
| AC-14 | Mobile today view shows greeting + chirp count from DB | Jim |
| AC-15 | All 6 employee names match between seed data and employee grid | Jim |
| AC-16 | Coffee shop vocabulary used throughout — no generic terms | Jim |

---

## 7. Task Routing

| Task | Agent | Est. Time |
|---|---|---|
| Phase A: Fix blueprint field mismatches | Jeremy | 2-3 hours |
| Phase B: Seed data script | Jeremy | 2-3 hours |
| Phase C: Wire views_wired.py to real queries | Jeremy | 3-4 hours |
| QA: All acceptance criteria | Jim | 1-2 hours |

**Total estimated:** 1–1.5 working days

---

## 8. Dependencies

| Dependency | Status | Impact if missing |
|---|---|---|
| B-075 scaffold (all pages navigable) | ✅ COMPLETE | Foundation for this work |
| PostgreSQL databases running (Docker) | ⚠️ Requires `make docker-up` | Blocker — seed script needs live DBs |
| SQLAlchemy models defined | ✅ All models exist | Schema layer ready |
| `level_b_demo.py` seed pattern | ✅ On disk | Pattern to follow for new seed |
| `en-US.json` locale pack (26 rules) | ✅ On disk | Source for detection rule seeds |
| `wsgi_b075.py` entry point | ✅ COMPLETE | Serves the pages |

---

## 9. Reference Files

| File | Path | What Jeremy needs from it |
|---|---|---|
| Views blueprint (current) | `Canary/canary/blueprints/views_wired.py` | Demo dicts to replace |
| Alert model | `Canary/canary/models/app/detection.py` | `Alert`, `AlertHistory`, `DetectionRule`, `MerchantRuleConfig` |
| Employee model | `Canary/canary/models/app/employees.py` | `Employee` field names |
| Fox models | `Canary/canary/models/fox/cases.py` | `FoxCase`, `FoxSubject`, `FoxCaseTimeline` |
| Transaction model | `Canary/canary/models/sales/transactions.py` | `Transaction` field names |
| Metrics models | `Canary/canary/models/metrics/facts.py` | `DailyMetrics`, `EmployeeDailyMetrics` |
| Session factory | `Canary/canary/models/session_factory.py` | `AppSession`, `SalesSession`, `MetricsSession` |
| Existing seed | `Canary/devops/seeds/level_b_demo.py` | Pattern for raw psycopg2 seeding |
| Locale pack | `_ALX/WorkOrders/output/Triangulation/LocalePacks/en-US.json` | All 26 chirp rule definitions |
| Alerts blueprint | `Canary/canary/blueprints/alerts_wired.py` | Field mismatches to fix |
| Employees blueprint | `Canary/canary/blueprints/employees_wired.py` | Field mismatches to fix |
| Merchants blueprint | `Canary/canary/blueprints/merchants_wired.py` | Field mismatches to fix |
| Locations blueprint | `Canary/canary/blueprints/locations_wired.py` | Field mismatches to fix |
| Fox case service | `Canary/canary/services/fox/case_service.py` | Missing methods to implement |

---

## 10. Execution Order (Optimized)

```
Phase A (fix plumbing)  ──→  Phase B (seed data)  ──→  Phase C (wire views)
       ↓                            ↓                          ↓
  Blueprints don't crash    DB has something to show    Pages render real data
```

Phase A must complete first — if blueprints crash on field names, wiring is pointless.
Phase B can partially overlap with Phase A (seed script is independent of blueprint fixes).
Phase C depends on both A and B.

---

## 11. North Star Check

> "We don't want to add to the stress. We want to ease it."

B-075 proved the shell works. B-076 proves the data works. When Jeffe sees real numbers from a real database, the product stops being a demo and starts being software. The graceful fallback rule ensures it never breaks — if the DB hiccups, the page still renders. That's the standard.

---

*Filed by ALX · March 1, 2026 · Routes to Jeremy (primary)*
