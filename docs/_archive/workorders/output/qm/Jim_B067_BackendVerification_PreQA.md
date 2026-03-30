---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Jim Pre-QA: B-067-B Backend Verification
**Work Order:** B-067 (backend readiness for wired QA)
**Date:** February 28, 2026
**Verified by:** ALX (programmatic — not browser QA)
**Purpose:** Confirms Jeremy's backend is ready for Jim's live wired QA pass

---

## Backend Smoke Test Results — All 16 Families

Ran directly against sandbox credentials (`SQUARE_ACCESS_TOKEN` from `.env`, `SQUARE_ENVIRONMENT=sandbox`).

| # | Family | Status | Records | SDK Call | Notes |
|---|---|---|---|---|---|
| 1 | merchants | ok | 1 | `client.merchants.get(merchant_id='me')` | Merchant profile returned |
| 2 | locations | ok | 4 | `client.locations.list()` | 4 sandbox locations |
| 3 | payments | ok | 10 | `client.payments.list()` | Full LIMIT page |
| 4 | refunds | ok | 9 | `client.refunds.list()` | 9 sandbox refunds |
| 5 | orders | ok | 10 | `client.orders.search(...)` | Full LIMIT page |
| 6 | cash_drawers | empty | 0 | `client.cash_drawers.shifts.list(...)` | No shifts in sandbox (poll-only B-047) |
| 7 | labor | empty | 0 | `client.labor.search_timecards(...)` | No timecards in sandbox (poll-only B-047) |
| 8 | inventory | empty | 0 | `client.inventory.batch_get_changes(...)` | No changes in sandbox |
| 9 | catalog | ok | 10 | `client.catalog.list(types='ITEM')` | Full LIMIT page |
| 10 | customers | ok | 10 | `client.customers.list()` | Full LIMIT page |
| 11 | team_members | ok | 6 | `client.team_members.search(...)` | 6 sandbox team members |
| 12 | gift_cards | empty | 0 | `client.gift_cards.list()` | No gift cards in sandbox |
| 13 | loyalty | empty | 0 | `client.loyalty.search_events(...)` | No loyalty program (404→empty) |
| 14 | invoices | empty | 0 | `client.invoices.search(...)` | No invoices in sandbox |
| 15 | disputes | empty | 0 | `client.disputes.list()` | No disputes in sandbox |
| 16 | subscriptions | empty | 0 | `client.subscriptions.search(...)` | No subscriptions in sandbox |

**Result: 16/16 pass (8 ok + 8 empty, 0 errors, 0 scope gaps)**

---

## What Jim Should Expect in Browser

### Cards with Data (8 families — "ok" status)
When Jim clicks "Fetch Live Data" on these cards, the response panel should show:
- Green success state
- Record count (e.g., "10 records")
- SDK call used (e.g., `client.payments.list()`)
- Pretty-printed JSON data in the `<pre>` block

### Cards without Data (8 families — "empty" status)
When Jim clicks "Fetch Live Data" on these cards, the response panel should show:
- Neutral/info state (not error red)
- "0 records"
- SDK call used
- Empty JSON array `[]`
- No error message

### Auto-Fetch on Load
- Merchants: 1 record should appear automatically
- Locations: 4 records should appear automatically

---

## Slug Alignment Verified

All 16 `data-family` attributes in the dashboard HTML match the `EXPLORER_REGISTRY` keys in the backend:

```
payments, refunds, merchants, locations, orders,
cash_drawers, labor, inventory, catalog, customers,
team_members, gift_cards, loyalty, invoices, disputes,
subscriptions
```

16/16 MATCH. Zero mismatches.

---

## Jim's Remaining QA (Browser Required)

1. [ ] Start Flask app (port 5001) — `python wsgi_alpha3x.py` or Docker
2. [ ] Load `/explorer` in browser
3. [ ] Confirm merchants + locations auto-fetch with real data (not "Backend not running")
4. [ ] Click all 16 "Fetch Live Data" buttons — verify JSON renders
5. [ ] Verify "empty" families show 0 records cleanly (no red error state)
6. [ ] Verify response panel styling matches design (green=ok, neutral=empty)
7. [ ] Check JS console for errors during fetch operations
8. [ ] Mobile responsive test with live data
9. [ ] Network disconnect test (kill Flask, confirm graceful failure)

---

## Bugs Found During Backend Build (Fixed)

| Bug | Root Cause | Fix |
|---|---|---|
| `'str' object has no attribute 'value'` on all calls | SDK v44 `environment` param requires `SquareEnvironment` enum, not string | Added `SquareEnvironment` import, mapped string→enum in `_client()` |
| `'InventoryClient' has no attribute 'batch_get_inventory_changes'` | Correct method name is `batch_get_changes` (SDK naming differs from Condor map) | Fixed method name |
| Loyalty returns 404 instead of empty list | No loyalty program configured in sandbox | Added 404→"empty" handling |

All three fixed before delivery. No known remaining issues.

---

*ALX | February 28, 2026 | Pre-QA backend verification for Jim*
*Jim fires live browser QA when Flask is running.*
