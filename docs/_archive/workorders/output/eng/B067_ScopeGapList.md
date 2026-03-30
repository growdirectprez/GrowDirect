---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# B-067-B: Square API Scope Gap List
**Work Order:** B-067-B
**Author:** Jeremy
**Date:** February 28, 2026
**SDK Version:** squareup 44.0.1.20260122
**Environment:** Sandbox
**Routes to:** Syd (OAuth scope planning) + Eva (Phase 2 sprint scope)

---

## Smoke Test Results — All 16 API Families

| # | Family | Status | Records | Notes |
|---|---|---|---|---|
| 1 | merchants | ok | 1 | Merchant profile returned |
| 2 | locations | ok | 4 | 4 sandbox locations |
| 3 | payments | ok | 10 | Full page returned |
| 4 | refunds | ok | 9 | 9 sandbox refunds |
| 5 | orders | ok | 10 | Full page returned |
| 6 | cash_drawers | empty | 0 | No cash drawer shifts in sandbox (poll-only, B-047) |
| 7 | labor | empty | 0 | No timecards in sandbox (poll-only, B-047) |
| 8 | inventory | empty | 0 | No inventory changes in sandbox |
| 9 | catalog | ok | 10 | Full page returned |
| 10 | customers | ok | 10 | Full page returned |
| 11 | team_members | ok | 6 | 6 sandbox team members |
| 12 | gift_cards | empty | 0 | No gift cards in sandbox |
| 13 | loyalty | empty | 0 | No loyalty program configured (404) |
| 14 | invoices | empty | 0 | No invoices in sandbox |
| 15 | disputes | empty | 0 | No disputes in sandbox |
| 16 | subscriptions | empty | 0 | No subscriptions in sandbox |

---

## Scope Gap Analysis

**scope_not_granted count: 0**

Sandbox environment grants all OAuth scopes by default. No scope gaps detected during sandbox testing. This means:

1. **All 16 API families are accessible in sandbox.** No permission barriers.
2. **Production will require explicit OAuth scope grants.** When moving to GrowDirect Lab (B-064 production gate), the following scopes will need to be requested during the OAuth authorization flow:

### Phase 1 (already authorized via marketplace app)
- `PAYMENTS_READ` — payments, refunds
- `MERCHANT_PROFILE_READ` — merchants, locations
- `ORDERS_READ` — orders

### Phase 2 (must be added to OAuth scope request)
- `ITEMS_READ` — catalog
- `INVENTORY_READ` — inventory
- `CUSTOMERS_READ` — customers
- `EMPLOYEES_READ` — team members
- `CASH_DRAWER_READ` — cash drawers
- `TIMECARDS_READ` — labor/timecards
- `GIFTCARDS_READ` — gift cards

### Phase 3 (future)
- `LOYALTY_READ` — loyalty
- `INVOICES_READ` — invoices
- `DISPUTES_READ` — disputes
- `SUBSCRIPTIONS_READ` — subscriptions (not planned, but scope exists)

---

## Empty vs Scope Error — Distinction

| Status | Meaning | Action |
|---|---|---|
| `empty` | API accessible, no data exists in sandbox | Seed sandbox data for testing, or accept as-is |
| `scope_not_granted` | OAuth scope missing — API call rejected (403) | Add scope to OAuth flow before Phase 2 |
| `error` | Unexpected failure | Debug and fix |

All 8 "empty" results are legitimate — the sandbox simply has no data for those families. This is expected behavior and not a scope gap.

---

## B-047 Note

Cash Drawers and Labor both returned `empty`. These are **poll-only APIs** (no webhooks). The empty result is expected in sandbox but also masks the B-047 polling adapter requirement. When production data flows, these families will need the TSP-02 polling adapter to feed data into the pipeline.

---

*Jeremy | B-067-B | February 28, 2026*
*Routes: Syd (OAuth scope planning), Eva (Phase 2 sprint scope)*
