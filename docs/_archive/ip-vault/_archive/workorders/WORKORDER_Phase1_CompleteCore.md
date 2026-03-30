---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# WORK ORDER: Phase 1 — Complete Core
*Issued by ALX · March 6, 2026 · Priority: CRITICAL PATH*
*Linear: GRO-137, GRO-142, GRO-145, GRO-138, GRO-102, GRO-123*
*Plan Source: `Canary_Platform_Roadmap_v1.0.docx`, `Canary_Phase1_Work_Order_v1.0.md`*

**Context:** 77 issues shipped. 29 Chirp rules firing. Owl chatting. Fox managing cases. Three-panel mobile live. But merchants can't get in, can't drill into alerts, can't search their data in English, can't see fiscal periods, and can't pay. Phase 1 closes every one of those gaps.

**Goal:** Ship a complete product a Square merchant can find, connect, use, and pay for by March 31, 2026. Two parallel tracks: Intelligence (search, calendar, alert detail) and Revenue (onboarding, billing, beta). Both converge at beta launch.

**The Method:** Every piece of prior work feeds this phase. Localization → multi-market readiness. Device architecture → register-level identity. RaaS → the lens principle. Namespace → entity correlation. That was all Heartbeat DNA. Now it runs.

---

## SHIPPED FOUNDATION — WHAT WE'RE BUILDING ON

### Chirp: 29 Detection Rules (Live)

```
PAYMENT (11)    C-001..C-011   refunds, velocity, split tender, manual entry, delay holds
CASH_DRAWER (4) C-101..C-104   no-sale abuse, cash variance, paid-out, after-hours drawer
ORDER (4)       C-201..C-204   discounts, line voids, sweethearting, untendered orders
TIMECARD (3)    C-301..C-303   off-clock, break transactions, wrong location
VOID (2)        C-501..C-502   void rate, post-void
GIFT_CARD (2)   C-601..C-602   load velocity, drain
LOYALTY (4)     C-801..C-804   point accumulation, bulk redemption, cross-location, enrollment
```

6 critical-tier rules auto-create Fox cases: C-009, C-104, C-204, C-301, C-502, C-602.

Source: `canary/services/chirp/rule_definitions.py`

### Owl: MCP + Personality Router (Live)

Three personalities (Jim/Tom/PhD), deterministic router, 4 output types, 9 action codes, closed-loop dispatcher. Ollama qwen3:14b on host:11434.

Source: `canary/services/owl/`, `canary/blueprints/owl_api.py`

### Fox: Case Management + Evidence Locker (Live)

Full lifecycle, hash-chained timeline, GUID evidence refs to RaaS, subject tracking, access logging.

Source: `canary/services/fox/`, `canary/models/fox/`

### Infrastructure (Live)

Docker Compose (PostgreSQL 17 + Valkey 8), 3-layer test suite (321 unit tests), Cloudflare Tunnel (dev.growdirect.app), QA pipeline to iMac, Square OAuth blueprint, onboarding UX flow, TSP webhook pipeline.

---

## TRACK A: INTELLIGENCE (Parallel — No Cross-Dependencies)

### WO-A1: Owl Search (GRO-137)

**Owner:** Jeremy
**QA:** Jim
**Dependencies:** GRO-129 ✔, GRO-131 ✔ (Owl system shipped)
**Accept:** Merchant types plain English → Owl returns structured CRDM results
**IP Source:** CRDMSearchableBuilder archive

**Code already written:** `canary/services/owl/search.py`
- `OWL_SEARCH_FIELDS` — searchable field catalog (CRDM column registry)
- `OwlSearchParser` — natural language intent extraction
- `OwlSearchExecutor` — CRDM query builder
- `OwlSearchFormatter` — result presentation with context

**Remaining work:**

1. **Unit tests** — `tests/unit/test_owl_search.py`
   - Test OwlSearchParser with 10+ natural language queries covering each field type
   - Test OwlSearchExecutor query building for each CRDM dimension (time, employee, location, category)
   - Test OwlSearchFormatter output structure (verify closed-loop envelope format)
   - Test edge cases: ambiguous queries, empty results, invalid field references

2. **Integration tests** — `tests/integration/test_owl_search_db.py`
   - Seed test merchant with known data (use existing `test_reset.py --seed` flow)
   - Run end-to-end: natural language → parse → execute → format → verify result counts
   - Test multi-dimension queries ("refunds last week at store 3")
   - Test with the 3 Owl personalities — verify search results are consistent regardless of personality

3. **Smoke tests** — `tests/smoke/test_owl_search_http.py`
   - `POST /owl/chat` with search-intent messages → verify response contains search results
   - Verify MCP tool registration: `/owl/tools` lists the search tool
   - `POST /owl/tools/search` directly → verify structured response

4. **Rebuild + Jim QA sign-off**
   ```bash
   cd ~/GrowDirect/Canary && docker compose -f devops/docker-compose.localhost.yml up -d --build flask
   ```

---

### WO-A2: 4-5-4 Retail Calendar (GRO-145)

**Owner:** Jeremy
**QA:** Jim
**Dependencies:** GRO-96 ✔ (DB foundation shipped)
**Accept:** dim_date populated with fiscal fields, period aggregation running
**IP Source:** Walmart SRA Scorecards archive (NRF 4-5-4 standard)
**Parent Epic:** GRO-144 (Ops Dashboard)

**Phase 1: Schema changes**

1. **Alembic migration** — add 7 columns to `canary_metrics.dim_date`:

   | Column | Type | Description |
   |---|---|---|
   | `fiscal_year` | INTEGER | NRF fiscal year (may differ from calendar year) |
   | `fiscal_quarter` | INTEGER | 1–4 |
   | `fiscal_period` | INTEGER | 1–12 (4-5-4 pattern within each quarter) |
   | `fiscal_week` | INTEGER | 1–53 |
   | `period_type` | VARCHAR(10) | '4-week' or '5-week' |
   | `fiscal_week_of_year` | INTEGER | 1–53 |
   | `fiscal_day_of_week` | INTEGER | 1–7 (Saturday=1, Friday=7) |

   File: `canary/models/metrics/dimensions.py` — add columns to `DimDate` model

2. **New tables** — add to `canary/models/metrics/facts.py`:

   ```python
   class PeriodMetrics(Base):
       __tablename__ = "period_metrics"
       __table_args__ = {"schema": "canary_metrics"}
       # merchant_id, location_id, fiscal_year, fiscal_period
       # aggregated: transaction_count, gross_sales_cents, refund_count,
       # refund_amount_cents, void_count, no_sale_count, cash_variance_cents,
       # alert_count, unique_employees, unique_customers

   class EmployeePeriodMetrics(Base):
       __tablename__ = "employee_period_metrics"
       __table_args__ = {"schema": "canary_metrics"}
       # merchant_id, employee_id, location_id, fiscal_year, fiscal_period
       # aggregated: transaction_count, refund_count, void_count,
       # no_sale_count, discount_total_cents, alert_count, risk_score_avg
   ```

3. **Calendar generation utility** — `canary/services/metrics/fiscal_calendar.py`
   - `generate_nrf_454_calendar(start_year, end_year)` → returns list of date rows with fiscal fields
   - NRF rules: fiscal year starts February, Saturday–Friday weeks, 4-5-4 pattern per quarter
   - Populate dim_date fiscal columns for 2024–2027 initially

4. **Period aggregation job** — `canary/services/metrics/period_aggregator.py`
   - Reads daily_metrics, joins on dim_date fiscal fields
   - Writes to period_metrics grouped by (merchant, location, fiscal_year, fiscal_period)
   - Writes to employee_period_metrics grouped by (merchant, employee, location, fiscal_year, fiscal_period)
   - Idempotent: re-running for the same period overwrites cleanly

5. **Tests:**
   - Unit: calendar generation produces correct 4-5-4 pattern (verify week counts per period: 4,5,4,4,5,4,4,5,4,4,5,4)
   - Unit: Saturday is day 1, Friday is day 7
   - Unit: fiscal year boundary handling (Jan dates belong to prior fiscal year)
   - Integration: migration runs, calendar populates dim_date, aggregation produces period_metrics

6. **Rebuild**

---

### WO-A3: Alert Detail Viewer (GRO-138)

**Owner:** Art (design) + Jeremy (code)
**QA:** Jim
**Dependencies:** GRO-125 ✔, GRO-107 ✔ (Mobile UX + Alert model shipped)
**Accept:** Tap alert card → see transaction detail with action buttons

**Problem:** Clicking an alert in the Chirps panel goes nowhere. `templates/mobile/home.html` renders alert cards but the `onclick` has no destination route.

**New files to create:**

| File | Purpose |
|---|---|
| `templates/mobile/alert_detail.html` | Alert detail view (extends `mobile/base_mobile.html`) |
| `canary/blueprints/alert_detail_api.py` | API endpoint: `/api/alerts/<alert_id>/detail` |

**Files to edit:**

| File | Change |
|---|---|
| `templates/mobile/home.html` | Wire alert card `onclick` → `/m/alert/<alert_id>` |
| `canary/blueprints/views_wired.py` | Add route: `GET /m/alert/<alert_id>` → render `mobile/alert_detail.html` |
| `wsgi.py` | Register `alert_detail_api_bp` if created as separate blueprint (or add to existing) |

**Alert detail view must show:**

1. **Alert header** — rule code, severity badge, timestamp, status
2. **Transaction context** — RaaS GUID resolution: `raas:{merchant_id}:{source_table}:{source_id}` → fetch the relevant row from canary_sales
3. **Rule explanation** — human-readable description from `rule_definitions.py` (each rule has `.description`)
4. **Related alerts** — other alerts for the same entity (employee/device/card) in the last 7 days
5. **Timeline** — if alert is linked to a Fox case, show FoxCaseTimeline entries
6. **Action buttons** — resolve, dismiss (with reason picker), open case, follow up. All route through `POST /owl/action` (existing closed-loop dispatcher)

**Design direction:** Extends mobile design language from GRO-125. Dark header with severity color accent. Card-based layout. Pull-to-refresh. Back button returns to Chirps panel.

**Tests:**
- Unit: alert detail API returns correct structure for each alert status
- Smoke: `GET /m/alert/<id>` returns 200 with expected template
- Smoke: action buttons trigger correct POST to /owl/action

**Rebuild**

---

## TRACK B: REVENUE (Sequential — Each Depends on Previous)

### WO-B1: One-Click Onboarding (GRO-142) — URGENT

**Owner:** Tom
**QA:** Jim
**Dependencies:** GRO-69 ✔ (OAuth), GRO-127 ✔ (Onboarding UX), GRO-97 ✔ (TSP pipeline)
**Accept:** Merchant goes from zero to first Chirp alert in under 5 minutes
**Blocks:** GRO-102 (Billing), GRO-123 (Beta)

**The pipeline (end-to-end):**

```
Merchant taps "Connect Square"
  → Square OAuth consent screen
  → OAuth callback → store access_token + refresh_token (canary_app.merchants)
  → Automatic webhook registration (Square Webhooks API → our TSP endpoint)
  → Initial data sync:
      catalog_items → canary_sales
      employees → canary_app
      locations → canary_app + canary_metrics.dim_location
  → Baseline calculation:
      seed dim_date if needed
      compute initial MetricBaseline rows from synced data
  → Chirp activation:
      mark merchant as chirp_active
      next webhook → Chirp evaluates → first alert
  → Redirect to /m/chirps (mobile) or / (desktop)
```

**Files to edit:**

| File | Change |
|---|---|
| `canary/blueprints/views_wired.py` | Add onboarding pipeline orchestration after OAuth callback |
| `canary/services/square/oauth.py` | Ensure token storage + refresh token rotation works |
| `canary/services/square/webhooks.py` | Add `register_webhooks(merchant_id)` — creates webhook subscription via Square API |
| `canary/services/square/sync.py` | Create or extend — initial catalog/employee/location pull |
| `canary/services/metrics/baseline.py` | Create or extend — compute initial MetricBaseline rows from synced data |

**Critical path items:**
- Webhook registration must use the correct Square API version (check SDK currency: `pip show squareup`)
- Token refresh must handle expiry gracefully — Square access tokens expire after 30 days
- Baseline calculation must not block the UI — run async or with a progress indicator
- If initial sync has no transactions yet, Chirp activation still proceeds — first real webhook will be the first alert

**Tests:**
- Integration: OAuth flow → token stored → webhooks registered → sync completes → baseline exists
- Smoke: Full flow with sandbox merchant (use existing sandbox credentials from .env)

**Rebuild**

---

### WO-B2: Square Subscription Billing (GRO-102)

**Owner:** Tom
**QA:** Jim
**Dependencies:** GRO-142 (Onboarding) — must ship first
**Accept:** Canary LP registered as Square software product, merchants can subscribe

**Scope:**

1. **Square Subscriptions API** — register Canary LP as a software subscription
   - Create subscription plan(s): free beta tier initially, paid tiers TBD
   - USD payment via Square (BTC payment is future — park for now)
   - Handle subscription lifecycle: create, invoice, payment, renewal, cancel

2. **Billing webhook handlers** — `canary/blueprints/billing_webhooks.py`
   - `subscription.created` → activate merchant
   - `subscription.updated` → update tier
   - `invoice.payment_made` → record payment
   - `subscription.canceled` → deactivate (soft — data preserved)

3. **Merchant billing portal** — minimal UI in Vault panel (settings tab)
   - Current plan, next billing date, payment history
   - Upgrade/downgrade (when multiple tiers exist)
   - Cancel subscription

4. **Tests:**
   - Unit: billing webhook handlers create correct DB records
   - Integration: subscription lifecycle (create → invoice → pay → renew)

**Rebuild**

---

### WO-B3: Beta Sign-Up Flow (GRO-123)

**Owner:** Will (copy) + Art (design) + Jeremy (code)
**QA:** Jim
**Dependencies:** GRO-142 ✔ (Onboarding), GRO-102 ✔ (Billing), Syd legal review ✔
**Accept:** Public page → beta registration → Square OAuth → active merchant
**Legal clearance:** Syd confirmed March 5, 2026 — beta onboarding permitted under Square Developer Terms.

**Scope:**

1. **Landing page** — `growdirect.app` (served by Flask or static)
   - Value prop: "AI-powered loss prevention for Square merchants"
   - Beta sign-up form: business name, email, Square account (optional — can connect later)
   - CTA: "Connect Square" → triggers GRO-142 onboarding pipeline

2. **Beta registration** — `canary/blueprints/beta.py`
   - `POST /beta/register` → create pending merchant record
   - Email confirmation (or skip for MVP — direct to OAuth)
   - Track beta invites: who signed up, who connected, who activated

3. **Landing page design** — Art provides
   - Mobile-first
   - Canary brand (not eljeffe.io ops theme)
   - Social proof / credibility signals
   - Clear path to "Connect Square" button

**Rebuild**

---

## DEPENDENCY MAP

```
Track A (Intelligence) — parallel:
  WO-A1: GRO-137 Owl Search ────────────────┐
  WO-A2: GRO-145 4-5-4 Calendar ────────────┤
  WO-A3: GRO-138 Alert Detail ──────────────┤
                                              ├──→ BETA LAUNCH (March 31)
Track B (Revenue) — sequential:               │
  WO-B1: GRO-142 Onboarding (URGENT) ───┐    │
  WO-B2: GRO-102 Billing ───────────────┤    │
  WO-B3: GRO-123 Beta Flow ─────────────┘────┘
```

**Critical path:** WO-B1 (Onboarding) is the keystone. Start here. Everything in Track B is blocked until onboarding works end-to-end.

**Parallel work:** Track A has zero dependencies on Track B. Jeremy can run A1+A2+A3 while Tom runs B1→B2. Art splits time between A3 (design) and B3 (landing page).

---

## WHAT PHASE 1 SHIPS

When complete, a Square merchant can:

1. Find Canary LP online and sign up for the beta
2. Connect their Square account in one tap
3. See their first alert within minutes (29 rules, 7 categories)
4. Tap an alert and see the full transaction context with action buttons
5. Ask the Owl a question in plain English and get structured answers
6. View data through the 4-5-4 retail calendar their business runs on
7. Subscribe and pay through Square

This is not a demo. This is the product.

---

## PHASE 2 PREVIEW (April 2026)

| GRO | Deliverable | What It Adds |
|---|---|---|
| GRO-139 | Velocity Monitoring | Statistical anomaly detection (XPLOSS equivalent) |
| GRO-141 | Lost Opportunity Calc | Dollar impact scoring — every alert gets a price tag |
| GRO-146 | Dashboard Metrics | New columns + period_metrics aggregation |
| GRO-147 | Heatmap Scoring | Peer-benchmark thresholds: green/yellow/orange/red |
| GRO-135 | PhD Deep Analysis | Square Configuration Optimizer |

---

## REFERENCE DOCUMENTS

| Document | Location |
|---|---|
| Product Blueprint v1.0 | `Canary_Product_Blueprint_v1.0.docx` |
| PRD: Owl Search v1.0 | `PRD_Owl_Search_v1.0.docx` |
| Ops Dashboard Spec v1.0 | `Canary_Ops_Dashboard_Spec_v1.0.docx` |
| Platform Roadmap v1.0 | `Canary_Platform_Roadmap_v1.0.docx` |
| Canary CLAUDE.md | `Canary/CLAUDE.md` |
| Test Strategy | `Canary/devops/TEST_STRATEGY.md` |
| Chirp Rule Definitions | `canary/services/chirp/rule_definitions.py` |

---

> "We don't want to add to the stress. We want to ease it."
> — Jeffe, Feb 26, 2026

---

*Canary LP | GrowDirect Inc. | Confidential*
