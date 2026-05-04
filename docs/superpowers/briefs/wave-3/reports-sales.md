---
screen: /reports/sales
title: Sales Report
role: MGR | BYR | ADM
wave: W3
origin: O
cp_equivalent: "Sales reports (multiple) — no unified cross-store view, no GMROI, no role-scoped defaults"
---

# Sales Report

**URL:** `/reports/sales`  
**Primary role:** MGR; BYR; ADM  
**Entry points:** Primary sidebar nav (Reports section)

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Sales Report", date range selector, store selector, grouping selector | |
| Filter bar | Category, Cashier, Customer segment, Item search | |
| Main content | Sales table (grouped by selected dimension) | |
| Bottom section | Totals row + export | |

## Key Elements

### Grouping Selector
Drives the row structure of the report:
- **By Day:** One row per day in the date range. Trend analysis.
- **By Week:** One row per week. Standard period comparison.
- **By Category:** One row per department. Category performance view.
- **By Item:** One row per item. Item-level sales analysis.
- **By Cashier:** One row per cashier. Staffing analysis + LP context.
- **By Store:** One row per store (ADM + multi-store only). Cross-location comparison.

### Sales Table Columns (shared across groupings)
Net Sales ($), Transactions, Avg Ticket ($), Units Sold, Gross Margin ($), Margin %, Discount ($), Discount %, Return ($), Return %, vs Prior Period delta columns.

**Discount % and Return % persist across all groupings.** These are the LP-adjacent columns that a manager passively monitors while reviewing normal sales data. An elevated discount % on a specific cashier (By Cashier grouping) is the same signal that drives the LP alert, visible here before any alert fires.

### Export
CSV export of the current view. Standard export — all visible columns, current filter state.

### Role-Scoped Defaults
- **MGR:** Defaults to By Day, current week, own store. By Cashier grouping is available.
- **BYR:** Defaults to By Category, last 30 days, all stores. Item-level drill available.
- **LP:** Defaults to By Cashier, last 30 days — the LP default for this report is the workforce analysis view.

**Empty state:** "No sales data for the selected filters and period."

## Interaction Flows

1. **Weekly review:** MGR opens sales report → By Week → current month → sees week 2 net sales down 12% vs prior year → filters to By Category → Tropicals is the drag → expected (storm event last week)
2. **Cashier analysis:** MGR opens By Cashier → current month → sorts by Discount % descending → one cashier at 22% vs 3-6% for all others → flags for LP
3. **BYR category review:** BYR opens By Category → last quarter → sorts by Margin % ascending → bottom 3 categories are candidates for pricing adjustment or destock

## UX Callout

CP has multiple sales reports — by department, by item, by date — each a separate screen with overlapping but inconsistent column sets. Canary's sales report is a single screen with a grouping selector that changes the analytical dimension without changing the column logic. The LP-adjacent columns (Discount %, Return %) are present regardless of grouping — a manager using the sales report for normal business review is also passively reviewing LP-relevant signals. This is the design philosophy that makes Canary feel different from CP: LP intelligence isn't a separate module you open when you suspect something, it's visible in the normal operational view.

## Navigation Exits

- `/reports/flash` — back to flash summary
- `/reports/category` — category-level drill (dedicated view)

## Open Questions

None.
