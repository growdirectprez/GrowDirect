---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Jim QA Report — B-067: Square Capability Dashboard (Wired QA)
**Work Order:** B-067 Wired QA
**Date:** February 28, 2026
**File Under Test:** `Canary/static/square_explorer.html` + `Canary/canary/blueprints/square_explorer_wired.py` + `Canary/canary/services/square_capability_explorer.py`
**Backend:** Flask (wsgi_alpha3x.py) on port 5099, sandbox credentials
**Validated Against:** `_ALX/WorkOrders/output/Condor/B067_SquareCapabilityMap_v1.0.md`
**Previous QA:** Static shell PASS (Jim_B067C_DashboardQA_Report.md) + Pre-QA backend verification PASS (Jim_B067_BackendVerification_PreQA.md)
**Verdict:** **CONDITIONAL PASS — 2 bugs found, neither blocking backend delivery**

---

## Executive Summary

The B-067-B backend (Jeremy) is fully operational. All 16 Square API families return correct, well-structured JSON from sandbox. The wiring between `square_capability_explorer.py` and `square_explorer_wired.py` is clean. Two bugs prevent the full end-to-end browser experience from working as designed — both are quick fixes that route back to Jeremy.

---

## Bug Report

### BUG #1: `/explorer` route returns 404 (BLOCKING — dashboard won't load from Flask)

**Severity:** HIGH — prevents dashboard from being served by Flask
**File:** `canary/blueprints/square_explorer_wired.py`, line 22
**Root cause:** `send_from_directory` computes wrong path.

```python
# CURRENT (broken):
static_dir = os.path.join(current_app.root_path, "..", "static")
# Resolves to: /Users/geofflyle/GrowDirect/static (WRONG — file not here)

# FIX:
static_dir = os.path.join(current_app.root_path, "static")
# Resolves to: /Users/geofflyle/GrowDirect/Canary/static (CORRECT — file is here)
```

**Why:** `current_app.root_path` is `/Users/geofflyle/GrowDirect/Canary` (the CWD where wsgi_alpha3x.py runs). The blueprint assumed `root_path` would be `canary/` (the Python package dir), but Flask resolves `root_path` from `__name__` of the app module, not the blueprint's package.

**Fix:** Remove the `".."` from the path join. One-line change.

**Workaround for QA:** Patched `app.view_functions['square_explorer.explorer_dashboard']` at runtime to confirm the fix works. HTTP 200 confirmed with patch applied.

---

### BUG #2: "empty" status renders as red error state (COSMETIC — misleading UX)

**Severity:** MEDIUM — wrong visual feedback for 8 families
**File:** `Canary/static/square_explorer.html`, JS function `fetchFamily()`, lines 1218-1234
**Root cause:** No handler for `data.status === 'empty'`.

The backend returns `status: "empty"` for families with no sandbox data (cash_drawers, labor, inventory, gift_cards, loyalty, invoices, disputes, subscriptions). The JS only checks for `ok` and `scope_not_granted` — everything else falls through to the `else` branch which applies `response-panel error` (red border) and sets `countEl.textContent = 'Error'`.

**Expected behavior:** Empty families should show neutral/info state with "0 records" label, not red error.

**Fix:** Add an `else if (data.status === 'empty')` branch:

```javascript
} else if (data.status === 'empty') {
    panel.className = 'response-panel success';  // or add 'response-panel empty' class
    countEl.textContent = '0 records';
    sdkCallEl.textContent = data.sdk_call || '';
    jsonEl.textContent = '[]';
}
```

Also add CSS class `.response-panel.empty` if a distinct visual state (e.g., amber or muted) is desired instead of green.

---

## Backend API Test Results — 16/16 PASS

All 16 families tested via `curl` against `http://127.0.0.1:5099/explore/<family>`.

| # | Family | Status | Count | SDK Call | Error | Verdict |
|---|--------|--------|-------|---------|-------|---------|
| 1 | payments | ok | 10 | `client.payments.list()` | None | PASS |
| 2 | refunds | ok | 9 | `client.refunds.list()` | None | PASS |
| 3 | merchants | ok | 1 | `client.merchants.get(merchant_id='me')` | None | PASS |
| 4 | locations | ok | 4 | `client.locations.list()` | None | PASS |
| 5 | orders | ok | 10 | `client.orders.search(location_ids=[...], limit=LIMIT)` | None | PASS |
| 6 | cash_drawers | empty | 0 | `client.cash_drawers.shifts.list(location_id=..., limit=LIMIT)` | None | PASS |
| 7 | labor | empty | 0 | `client.labor.search_timecards(limit=LIMIT)` | None | PASS |
| 8 | inventory | empty | 0 | `client.inventory.batch_get_changes(location_ids=[...])` | None | PASS |
| 9 | catalog | ok | 10 | `client.catalog.list(types='ITEM')` | None | PASS |
| 10 | customers | ok | 10 | `client.customers.list()` | None | PASS |
| 11 | team_members | ok | 6 | `client.team_members.search(limit=LIMIT)` | None | PASS |
| 12 | gift_cards | empty | 0 | `client.gift_cards.list()` | None | PASS |
| 13 | loyalty | empty | 0 | `client.loyalty.search_events(query={...}, limit=LIMIT)` | None | PASS |
| 14 | invoices | empty | 0 | `client.invoices.search(query={...}, limit=LIMIT)` | None | PASS |
| 15 | disputes | empty | 0 | `client.disputes.list()` | None | PASS |
| 16 | subscriptions | empty | 0 | `client.subscriptions.search(query={...}, limit=LIMIT)` | None | PASS |

**Summary:** 8 ok + 8 empty + 0 errors. All `api_family` fields match slugs. All `data` fields present (list or dict). All `sdk_call` strings populated. All `error` fields are `None`.

---

## Response Schema Validation

Every endpoint returns this exact schema:

```json
{
    "api_family": "<slug>",
    "status": "ok" | "empty" | "error",
    "count": <int>,
    "data": <list | dict>,
    "sdk_call": "<string>",
    "error": null | "<string>"
}
```

Verified for all 16 families + 1 invalid family (`nonexistent` returns `status: "error"` with proper error message). Schema is consistent and parseable by the dashboard JS.

---

## Slug Alignment — 16/16 MATCH

All `data-family` attributes in HTML match `EXPLORER_REGISTRY` keys in backend:

```
payments, refunds, merchants, locations, orders,
cash_drawers, labor, inventory, catalog, customers,
team_members, gift_cards, loyalty, invoices, disputes,
subscriptions
```

---

## Condor B-067-A Cross-Validation

All 16 `explore_` function names match Condor's capability map. SDK namespaces confirmed:

| Family | Condor SDK Namespace | Backend SDK Call | Match |
|--------|---------------------|-----------------|-------|
| payments | client.payments | client.payments.list() | MATCH |
| refunds | client.refunds | client.refunds.list() | MATCH |
| merchants | client.merchants | client.merchants.get(merchant_id='me') | MATCH |
| locations | client.locations | client.locations.list() | MATCH |
| orders | client.orders | client.orders.search(...) | MATCH |
| cash_drawers | client.cash_drawers.shifts | client.cash_drawers.shifts.list(...) | MATCH |
| labor | client.labor | client.labor.search_timecards(...) | MATCH |
| inventory | client.inventory | client.inventory.batch_get_changes(...) | MATCH |
| catalog | client.catalog | client.catalog.list(types='ITEM') | MATCH |
| customers | client.customers | client.customers.list() | MATCH |
| team_members | client.team_members | client.team_members.search(...) | MATCH |
| gift_cards | client.gift_cards | client.gift_cards.list() | MATCH |
| loyalty | client.loyalty | client.loyalty.search_events(...) | MATCH |
| invoices | client.invoices | client.invoices.search(...) | MATCH |
| disputes | client.disputes | client.disputes.list() | MATCH |
| subscriptions | client.subscriptions | client.subscriptions.search(...) | MATCH |

**Result:** 16/16 match. Zero discrepancies.

---

## Blueprint Registration

Flask boot log confirms Square Capability Explorer registered successfully:

```
✓  (Square Capability Explorer)
```

Note: Blueprint registered with empty URL prefix `""`, so routes are at root level (`/explore/<family>`, `/explorer`). 13/14 total blueprints loaded (only TSP Webhook Pipeline skipped — missing `valkey` module, unrelated to B-067).

---

## Infrastructure Notes

- **Docker container on port 5001** does NOT have B-067-B code — it's an older build. Dashboard QA requires running Flask natively or rebuilding Docker image.
- **Database:** Not required. Explorer is read-only against Square sandbox API — no local DB dependency.
- **Valkey:** Not required. TSP webhook blueprint skipped, doesn't affect explorer.
- **Square SDK:** v44.0.1 confirmed. `SquareEnvironment` enum properly handled (was a bug, already fixed per pre-QA report).

---

## Checklist Summary

| # | Check | Verdict | Notes |
|---|-------|---------|-------|
| 1 | Flask app starts, /health responds | PASS | Port 5099 (Docker occupies 5001) |
| 2 | /explorer serves dashboard HTML | **FAIL** | BUG #1 — path resolution error |
| 3 | /explore/<family> returns JSON for all 16 | PASS | 8 ok, 8 empty, 0 errors |
| 4 | Auto-fetch merchants on load | PASS (backend) | Would work once BUG #1 fixed |
| 5 | Auto-fetch locations on load | PASS (backend) | Would work once BUG #1 fixed |
| 6 | "ok" families show green success state | PASS (schema) | JSON schema correct for JS handler |
| 7 | "empty" families show clean 0-record state | **FAIL** | BUG #2 — falls to red error state |
| 8 | Slug alignment HTML ↔ backend | PASS | 16/16 match |
| 9 | Condor B-067-A cross-validation | PASS | 16/16 match |
| 10 | Invalid family returns error gracefully | PASS | `nonexistent` → proper error JSON |
| 11 | Response schema consistency | PASS | All 16 + 1 follow identical schema |

---

## Routing

### Jeremy — Fix both bugs

**BUG #1 (HIGH):** `square_explorer_wired.py` line 22 — change `"..", "static"` to `"static"`. One-line fix. Test: `curl http://127.0.0.1:5001/explorer` should return 200.

**BUG #2 (MEDIUM):** `square_explorer.html` `fetchFamily()` function — add `else if (data.status === 'empty')` handler. ~5 lines. Optional: add `.response-panel.empty` CSS class for distinct visual state.

### Jim — Re-test after fixes

Once Jeremy lands both fixes, Jim runs full browser QA:
1. Start Flask (single port, no Docker conflict)
2. Load `/explorer` — verify HTML renders
3. Confirm merchants + locations auto-fetch with green success state
4. Click all 16 fetch buttons — verify 8 green, 8 neutral/info
5. Mobile responsive test
6. Network disconnect test (kill Flask, confirm catch block fires)

---

## Verdict

**CONDITIONAL PASS.** Backend is clean — Jeremy's `square_capability_explorer.py` and the Flask blueprint wiring are production-quality. Two quick fixes needed:

1. **BUG #1** (path resolution) — `/explorer` route 404. One-line fix in blueprint.
2. **BUG #2** (empty status handling) — 8 families show red error instead of neutral state. ~5-line fix in JS.

Neither bug affects the core value: **all 16 Square API families are callable, returning real sandbox data through a clean dispatch pattern.** The dashboard shell (already PASSED static QA) will render correctly once these wiring bugs are fixed.

**Jim's veto is NOT exercised.** Dashboard is not blocked — it needs two small fixes and a re-test.

---

*Jim | QA Manager | February 28, 2026 | B-067 Wired QA*
*Validated: API endpoint testing (all 16 families) + source code review + Condor cross-validation + blueprint registration verification*
*Flask backend: port 5099 with runtime view_function patch to work around BUG #1*
