---
screen: /transfers
title: Transfer List
role: MGR | RCV
wave: W2
origin: O
cp_equivalent: "Transfer Out + Transfer In (two separate screens in CP — no unified view)"
---

# Transfer List

**URL:** `/transfers`  
**Primary role:** MGR; RCV  
**Entry points:** Primary sidebar nav (Inventory section)

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Page title "Transfers", New Transfer button | New Transfer → /transfers/new |
| Filter bar | Status, Store (from/to), Date range, Overdue Only toggle | |
| Main content | Transfer table | |

## Key Elements

### Transfer Table
Columns: Transfer ID, From Store, To Store, Item Count (line count), Initiated Date, Expected Receipt Date, Status badge (Initiated / In Transit / Received / Variance-Flagged), Variance indicator (appears on Variance-Flagged rows — shows dollar amount of variance).

**Status color-coding:** Initiated = blue, In Transit = purple, Received = green, Variance-Flagged = red.

**Overdue filter:** Highlights transfers where Expected Receipt Date has passed and status is still In Transit. Color: orange row tint + "Overdue" badge. This surfaces transit shrink candidates — items that have been "in transit" too long may have been stolen.

**Empty state:** "No transfers in the selected period. Click 'New Transfer' to initiate an inventory transfer between stores."

### Variance-Flagged Rows
Red status badge. Click row → navigates to `/transfers/:id/variance`. LP is also notified via alert when variance exceeds threshold — the table gives MGR the same visibility without waiting for an LP alert.

### New Transfer Button
Navigates to `/transfers/new`. Visible to MGR role only — RCV can receive but cannot initiate.

## Interaction Flows

1. **Morning receiving check:** RCV opens transfers → filters to To Store = their store, Status = In Transit → sees 3 inbound transfers → clicks each to see what to expect → prepares receiving dock
2. **Identify overdue transfer:** MGR applies "Overdue Only" toggle → sees Transfer #T-1049 from Store 2 to Store 3 initiated 8 days ago, expected 5 days ago, still In Transit → contacts Store 2 manager to investigate
3. **Review variance history:** LP opens transfers → filters by Status = Variance-Flagged → reviews all flagged transfers over the past 60 days → identifies Store 2 → Store 3 route has 5 variance events in 60 days → opens `/cases/hawk/patterns` to check if a subject appears consistently

## UX Callout

CP splits transfer management into Transfer Out (origin store) and Transfer In (destination store) — two completely separate forms with no unified visibility. A manager wanting to see all in-transit transfers across their operation has to query both forms separately, with no automated alert when a transfer is overdue. Canary's unified Transfer List surfaces the entire transfer pipeline — initiated, in-transit, received, variance-flagged — in one view. The Overdue Only toggle specifically addresses the transit shrink scenario, which CP has no mechanism to detect.

## Navigation Exits

- `/transfers/new` — initiate new transfer
- `/transfers/:id` — transfer detail
- `/transfers/:id/receive` — receipt entry (destination store)
- `/transfers/:id/variance` — variance review (from Variance-Flagged rows)

## Open Questions

None.
