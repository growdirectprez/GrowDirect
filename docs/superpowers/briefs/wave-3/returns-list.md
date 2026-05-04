---
screen: /returns
title: Customer Returns
role: MGR | LP
wave: W3
origin: O
cp_equivalent: "Returns processed in CP at register — no aggregate view, no LP flagging, no pattern analysis"
---

# Customer Returns

**URL:** `/returns`  
**Primary role:** MGR; LP  
**Entry points:** Primary sidebar nav (Store Ops section); alert detail → return evidence link

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Returns", date range selector, store selector | |
| Filter bar | Status (Approved / Flagged / Pending Review), Reason Code, Cashier, Amount range | |
| Main content | Returns table | |

## Key Elements

### Returns Table
Columns: Return ID, Date, Store, Transaction ID (original sale), Items, Return Value ($), Reason Code, Cashier, Customer, Status badge, Alert indicator.

**Status values:**
- **Approved:** Return processed normally within policy.
- **Flagged:** Return triggered a detection rule (e.g., Q.M return rule). Alert may be open.
- **Pending Review:** Return exceeds a threshold requiring MGR sign-off before processing. Not yet resolved.

**Alert indicator:** If a return is associated with an open alert, the alert icon appears in that row. Clicking navigates to the alert detail.

**Reason Code column:** The reason the customer gave for the return. LP uses this to identify fraudulent return reason patterns (e.g., "defective" claimed on non-defective items, "purchased in error" used repeatedly by the same customer).

**LP filter pattern:** LP sorts by Return Value descending, filters Status = Flagged, to see the highest-value flagged returns — the priority triage queue.

**Empty state:** "No returns in the selected period."

## Interaction Flows

1. **Daily return review:** MGR opens returns → today → reviews Flagged rows → 2 flagged returns, both from the same customer → opens each → customer profile shows 8 returns in 30 days → escalates to LP
2. **LP return fraud pattern:** LP filters by Customer (known subject) → sees 12 returns over 60 days totaling $840 → all with "defective" reason code, all different cashiers — customer is the pattern, not cashier conduct
3. **High-value pending:** MGR opens returns → sees $280 return in Pending Review → original sale was 22 days ago (at edge of return policy window) → reviews original transaction → approves with note

## UX Callout

CP processes returns at the register — they appear in the transaction history as negative sales. There is no aggregate view of returns, no flagging mechanism, and no LP visibility. An LP investigator in CP trying to understand a customer's return history must pull transaction reports and manually filter for negative-value transactions, then manually calculate return rate and total value. Canary's returns list is a first-class record type with LP fields built in — reason code, flag status, and customer linkage are native. Return fraud patterns are visible at the list level without pulling a report.

## Navigation Exits

- `/returns/:id` — return detail
- `/alerts/list` — from alert indicator
- `/customers/:id` — from customer column link
- `/transactions/:id` — from original transaction link

## Open Questions

None.
