---
screen: /exceptions
title: Exception Queue
role: LP | MGR
wave: W5
origin: N
cp_equivalent: "None — CP has no exception workflow; LP exceptions are discovered by querying multiple reports"
---

# Exception Queue

**URL:** `/exceptions`  
**Primary role:** LP; MGR  
**Entry points:** Primary sidebar nav (LP section — W-module); home dashboard LP widget

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Exceptions", date range selector, store selector | |
| Filter bar | Status (New / In Review / Escalated / Resolved / Dismissed), Rule Family, Cashier, Store, Amount range | |
| Main content | Exception queue table | |

## Key Elements

### Exception Queue Table
Columns: Exception ID, Date, Store, Cashier, Rule Family, Exception Type, Amount ($), Transaction ID, Status badge, Age (days since created), Investigator (assigned LP user), Priority.

**Exception vs Alert:** Alerts are the first-level signal — a transaction rule fires. Exceptions are the curated queue that emerges from the alert triage process. An exception is an alert (or group of alerts) that has been confirmed to represent a genuine anomaly worth formal review. Not every alert becomes an exception; every exception starts from an alert.

**Exception types** (the W-module classification system):
- **Suspicious Void:** Void + re-ring pattern with amount or timing anomalies
- **Over-Discount:** Discount applied in excess of authorized rate, not covered by allow-list
- **Unauthorized Return:** Return without receipt or return-to-wrong-account
- **Register Manipulation:** Tender manipulation, drawer-open-no-sale patterns
- **Inventory Discrepancy:** Transaction-level inventory anomaly (item sold but not in stock)
- **B2B Anomaly:** B2B account activity outside expected patterns (routes from the B2B alert class)

**Age column:** Color-coded — < 3 days grey, 3-7 days yellow, > 7 days orange, > 14 days red. Exception velocity matters for LP credibility — exceptions that age out without resolution erode the program's effectiveness.

**Priority:** Computed from exception amount + rule family risk weight + cashier history. High-priority exceptions surface to the top of the investigator's queue.

**Empty state:** "No exceptions in the selected period. Exceptions appear here when alert investigations are escalated."

## Interaction Flows

1. **Morning triage:** LP opens exception queue → filters Status = New → 4 new exceptions overnight → reviews each: 2 assigned to self, 2 assigned to colleague → opens first exception for investigation
2. **Escalation to MGR:** LP reviews an exception → pattern implicates a store manager, not a cashier → escalates status to Escalated → routes to ADM LP team
3. **Batch resolution:** LP reviews 8 Unauthorized Return exceptions → 6 are resolved (subject identified, case opened) → 2 are dismissed (legitimate returns with missing receipts, no further pattern) → batch-resolves the 6, batch-dismisses the 2

## UX Callout

CP has no exception queue. An LP investigator in a CP environment works from report outputs: they export transaction exception reports, sort by amount, manually identify patterns, and track their work in a spreadsheet or a personal notebook. Canary's exception queue is the formal LP workflow layer that the W-module adds on top of the alert feed. The alert feed tells LP what happened. The exception queue is LP's structured response: what is being investigated, by whom, at what stage, and how old it is. The queue discipline is what makes a retail LP program professional rather than reactive — investigations are tracked, assigned, and aged, not discovered in reports and forgotten.

## Navigation Exits

- `/exceptions/:id` — exception detail
- `/cases/hawk/:id` — escalate to case from exception
- `/cases/all/:id` — all-domain case context

## Open Questions

None.
