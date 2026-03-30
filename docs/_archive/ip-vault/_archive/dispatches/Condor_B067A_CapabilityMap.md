---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Condor Session Prompt — B-067-A: Square Capability Map
**Work Order:** B-067-A
**Date:** February 28, 2026
**Dispatched by:** ALX
**Priority:** HIGH — gates Jeremy's wiring pass

---

## Mission

Produce the definitive Square capability map. This is the intellectual backbone of the B-067 dashboard. Jeremy and Qwen both read from it.

One goal: for every Square API family, tell Jeremy exactly what the SDK call looks like and tell Qwen exactly what to show Jeffe.

---

## Read First (in this order)

```
/Users/geofflyle/GrowDirect/Canary_IP/Markdown/Specs/Square_API_LP_Coverage_Analysis_Jeremy_v1.0.md
/Users/geofflyle/GrowDirect/Canary/square/SQUARE_SCAN_NOTES.md
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Condor/TSP_ConsolidatedReview_v1.0.md
/Users/geofflyle/GrowDirect/Canary/square/square-python-sdk/README.md
```

---

## Produce

**File:** `/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Condor/B067_SquareCapabilityMap_v1.0.md`

For each of the 14 Square API families, one block in this exact format:

```
### [N]. [API Family Name]

SDK Namespace:            client.[namespace]
Sandbox Permission:       [OAuth scope — e.g. PAYMENTS_READ]
Canary Phase:             [Phase 1 LIVE | Phase 2 | Phase 3 | Not planned]
TSP Component:            [TSP-01 through TSP-09, or N/A]
LP Signal:                [one sentence — what fraud/loss this catches]
Key Read Methods:         [3-5 actual SDK method names from square-python-sdk v44]
Sample Call (Python):     [one line — real v44 syntax, e.g. client.payments.list(limit=10)]
Dashboard Section Title:  [what Jeffe sees as the card header]
Fetch Button Label:       Fetch Live Data
Phase Badge:              [LIVE | PHASE 2 | PHASE 3]
explore_ function name:   [e.g. explore_payments]
```

The 14 families:
1. Payments API
2. Refunds API
3. Orders API
4. Cash Drawer Shifts API
5. Labor / Timecards API
6. Inventory API
7. Disputes API
8. Gift Cards API
9. Customers API
10. Loyalty API
11. Team Members API
12. Catalog API
13. Devices API
14. Webhooks / Subscriptions API

Also include two utility families Jeremy needs for context calls:
15. Merchant API (anchor record — `explore_merchant`)
16. Locations API (required for cash drawer + inventory — `explore_locations`)

---

## Also Produce: TSP Coverage Table

After the 14 blocks, add a table:

| API Family | Sub 2 Parser | Sub 1 Seal | Sub 3 Inscribe | Status |
|---|---|---|---|---|
| Payments | parse_payment | hash + seal | ordinal | LIVE |
| Refunds | parse_refund | hash + seal | ordinal | LIVE |
| ... | ... | ... | ... | PLANNED / NOT STARTED |

---

## Rules

- Verify SDK method names against the cloned repo — do not guess.
- Sample calls must use `from square import Square` / `client = Square(...)` v44 syntax. Not the old `Client` pattern.
- If a permission scope is unclear, note it — Jeremy will confirm during his scope gap test.
- Phase 1 LIVE = Payments + Refunds + Webhooks (confirmed operational today).
- Phase 2 = everything in Jeremy's LP analysis Tier 1 + Tier 2 recommendations.
- Phase 3 = everything else.

---

## Deliver Before Jeremy's Wiring Pass

This is the gate. Jeremy starts his explore_ functions after this file exists.

---

*ALX | February 28, 2026 | B-067-A*
