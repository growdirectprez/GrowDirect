---
screen: /promotions
title: Promotions List
role: MGR | BYR
wave: W4
origin: O
cp_equivalent: "frmimpromotions — Windows-only, no active/expired at-a-glance, no LP impact visibility"
---

# Promotions List

**URL:** `/promotions`  
**Primary role:** MGR; BYR  
**Entry points:** Primary sidebar nav (Merchandising section)

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Promotions", New Promotion button | |
| Filter bar | Status (Active / Scheduled / Expired / Draft), Store, Category, Date range | |
| Main content | Promotions table | |

## Key Elements

### Promotions Table
Columns: Promo ID, Name, Type (Discount % / Buy X Get Y / Fixed Price / Bundle), Store(s), Categories / Items, Start Date, End Date, Status badge, Discount Value ($) since start, Transaction Count (# transactions using this promo), Avg Ticket Impact ($), LP Risk flag.

**Status color-coding:** Draft = grey, Scheduled = blue, Active = green, Expired = teal, Paused = yellow.

**LP Risk flag:** Appears when a promotion is associated with a disproportionate alert volume. If a 20%-off promotion on a category coincides with a 300% increase in void-related alerts, the LP Risk flag fires and LP is notified. The promotion may be legitimate; the alert volume spike requires explanation.

**Discount Value ($) since start:** Running total of discounts applied to transactions through this promotion. A promotion running $4,200 in discounts against a $2,000 budgeted discount spend is an overrun signal for BYR.

**Empty state:** "No promotions in the selected period."

## Interaction Flows

1. **Active promotions check:** MGR opens promotions → filters Status = Active → sees 3 running promotions → checks transaction counts vs expectations
2. **LP risk review:** LP opens promotions → LP Risk flag on 1 active promotion → opens to investigate alert volume spike → determines whether promotion is being abused (e.g., cashiers applying promo to non-qualifying transactions)
3. **Seasonal promotion planning:** BYR opens promotions → creates new promotions for spring sale season → schedules each for correct date range → moves to Draft until final approval

## UX Callout

CP's promotion module shows a list of promotions with no performance context. A buyer looking at promotions in CP cannot see how many transactions have used each promotion or how much discount value has been distributed without running a separate report. Canary shows promotion performance inline. The LP Risk flag is the connection between the merchandising module and LP intelligence — a promotion that drives unusual alert patterns is either being abused or has an unintended overlap with a detection rule, and the flag surfaces this without requiring LP to monitor every active promotion manually.

## Navigation Exits

- `/promotions/new` — create new promotion
- `/promotions/:id` — promotion detail

## Open Questions

None.
