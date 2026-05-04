---
screen: /reports/category
title: Category Performance Report
role: MGR | BYR
wave: W2
origin: O
cp_equivalent: "Sales by Department report — no GMROI, no sell-through rate, single-period only"
---

# Category Performance Report

**URL:** `/reports/category`  
**Primary role:** MGR; BYR (Buyer/Merch Manager)  
**Entry points:** Primary sidebar nav (Reports section); item detail → category performance link

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Category Performance", date range selector, store selector | Defaults to last 30 days / current store |
| Filter bar | Category / Department, Compare Period toggle | |
| Main content | Category performance table | |
| Bottom section | Top items within selected category | Appears when a category row is expanded/clicked |

## Key Elements

### Category Performance Table
Rows: one per department/category. Columns: Category, Net Sales ($), Units Sold, Avg Unit Price ($), Cost of Goods ($), Gross Margin (%), Sell-Through Rate (%), GMROI, Return Rate (%), Discount Rate (%), vs Prior Period delta.

**Key column definitions:**
- **Sell-Through Rate:** Units sold ÷ beginning inventory units for the period. Measures how effectively the category is turning. < 20% = slow; 40-70% = healthy range for most categories.
- **GMROI (Gross Margin Return on Inventory Investment):** Gross margin ÷ average inventory cost. How many dollars of gross margin the business gets back for every dollar invested in inventory. < 1.0 = losing money on inventory position; > 2.5 = strong.
- **Return Rate:** Return units ÷ units sold. High return rate against a category may indicate quality issues, misrepresentation, or (LP context) return fraud targeting that category.

**Compare Period toggle:** When enabled, adds a comparison column for each metric showing prior period (previous 30 days, or same 30-day window last year). Deltas highlighted in green/red.

### Category Drill-Down
Clicking any category row expands or navigates to a sub-table showing top 10 items within that category by Net Sales. Each item row shows the same metrics. Item # in the sub-table links to `/items/:id`.

### Sort and Filter
All columns sortable. BYR typically sorts by GMROI ascending to find underperforming inventory positions. MGR typically sorts by Net Sales descending to understand contribution. LP typically sorts by Return Rate descending to find fraud-susceptible categories.

**Empty state:** "No sales data for the selected period and store."

## Interaction Flows

1. **Buyer quarterly review:** BYR opens Category Report → last 90 days → sorts by GMROI ascending → Hardscape: GMROI = 0.8 → drills down → bottom 3 items are large-format pavers with < 5% sell-through → candidate for markdown or destock
2. **Return rate flag:** LP sorts by Return Rate descending → Tropicals showing 18% return rate vs 2-4% for other categories → drills down → 3 items account for 80% of returns → items are high-value cacti — opening a fraud investigation for coordinated buy/return scheme
3. **Manager margin check:** MGR opens Category Report → this month → sorts by Gross Margin ascending → finds one category at 8% margin → investigates pricing — discovers cost increase not yet reflected in sell price

## UX Callout

CP's Sales by Department report shows net sales and units — nothing beyond. GMROI and sell-through rate require the manager to export to Excel and join against inventory and cost data manually. Canary computes them in place because the perpetual ledger and cost data are in the same system as the sales data. A buyer looking at GMROI in Canary is making the same calculation a Big Box buying team makes in their planning tools — the Main Street operator just never had access to it before. The return rate column is the LP addition: return fraud has a category signature, and it only becomes visible when you look at returns relative to sales at the category level, not as isolated line-item events.

## Navigation Exits

- `/items/:id` — from category drill-down item rows
- `/reports/flash` — back to flash summary
- `/alerts/list` — from high return rate category drill

## Open Questions

None.
