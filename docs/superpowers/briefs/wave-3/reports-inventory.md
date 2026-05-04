---
screen: /reports/inventory
title: Inventory Report
role: MGR | BYR
wave: W3
origin: O
cp_equivalent: "Inventory reports (multiple in CP) — no cross-store aggregation, no shrink line, no days-on-hand"
---

# Inventory Report

**URL:** `/reports/inventory`  
**Primary role:** MGR; BYR  
**Entry points:** Primary sidebar nav (Reports section)

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Inventory Report", as-of date selector, store selector | Default: today / all stores |
| Filter bar | Category, On-Hand range, Days-on-Hand range, Zero-Stock toggle | |
| Main content | Inventory table | |
| Bottom section | Totals + export | |

## Key Elements

### Inventory Table
Columns: Item #, Description, Category, Store (or "All Stores" aggregate), On Hand, On Order (open PO quantities not yet received), Committed (items allocated to open orders), Available (On Hand − Committed), Avg Cost ($), Inventory Value ($), Days on Hand, Reorder Point, Reorder Qty, Last Count Date, Shrink ($ since last count).

**Days on Hand:** On Hand ÷ (avg daily sales units over last 30 days). How many days of stock at current sales rate. < 7 days = at-risk; > 90 days = potential overstock.

**Shrink ($ since last count):** Difference between expected on-hand (from perpetual ledger continuous updates) and last physical count result, expressed in dollars. This is the rolling shrink metric — it accumulates between counts and resets at each physical count post. High shrink on an item between counts is a flag for either a counting error or ongoing loss.

**Zero-Stock toggle:** Filters to items where On Hand = 0. The stockout monitor — anything at zero needs attention (reorder or deactivate).

### Cross-Store Aggregation
When store selector is "All Stores" (BYR default), one row per item shows the aggregate On Hand and Inventory Value across all stores, plus a breakdown button to expand into per-store rows. This answers "how much of item #8812 do I have in the system?" without running multiple single-store queries.

**Empty state:** "No inventory data for the selected filters."

## Interaction Flows

1. **Stock-at-risk review:** MGR filters Days on Hand < 7 → 8 items at risk → sorts by Inventory Value descending → prioritizes reorder for highest-value items at risk → creates POs or transfers
2. **Overstock identification:** BYR filters Days on Hand > 90 → 14 items → checks if any have active promotions or transfers already planned → submits markdown recommendations for the remainder
3. **Shrink audit:** LP filters Shrink > $50 → 6 items showing significant shrink since last count → cross-references with alert history for those items → 4 have associated alerts; 2 are unalerted and become LP investigative targets

## UX Callout

CP's inventory reports are single-store and single-dimension — you can get on-hand by department, or on-hand by item, but not days-on-hand and shrink-since-last-count in the same report. The shrink column is a Canary addition that has no CP equivalent: CP's perpetual ledger doesn't track the delta between expected and counted, it just replaces the on-hand with the count result. Canary tracks both the continuous perpetual position and the last-count result, so the shrink between counts is always visible. This converts the physical count from a one-time event into a continuous accountability signal.

## Navigation Exits

- `/items/:id` — from item row
- `/inventory/count/new` — from zero-stock or high-shrink items
- `/orders/new` — from at-risk items reorder action

## Open Questions

None.
