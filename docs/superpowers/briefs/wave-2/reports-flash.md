---
screen: /reports/flash
title: Flash Report
role: MGR | ADM
wave: W2
origin: O
cp_equivalent: "Sales Summary report — single-store, requires period selection, no cross-store compare"
---

# Flash Report

**URL:** `/reports/flash`  
**Primary role:** MGR; ADM  
**Entry points:** Primary sidebar nav (Reports section); home dashboard → Flash Report link

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Flash Report", date selector, store selector | Defaults to today / current user's store |
| Top section | Daily KPI tiles | |
| Main content | Sales + transaction breakdown | |
| Right rail | vs. Prior Period comparison | |
| Bottom section | By-hour transaction chart | |

## Key Elements

### Daily KPI Tiles
Five tiles for the selected day and store(s):
- **Net Sales ($):** Total net sales (after returns and discounts)
- **Transaction Count:** Total transactions for the day
- **Average Ticket ($):** Net Sales ÷ Transaction Count
- **Discount Rate (%):** Total discount amount ÷ gross sales
- **Return Rate (%):** Total return value ÷ net sales

Each tile shows the day's value plus a delta vs prior period (same day last week, or configurable). Green = improved, red = degraded. The LP-relevant tiles are Discount Rate and Return Rate.

### Sales Breakdown Table
Columns: Hour, Transaction Count, Net Sales, Avg Ticket, Discount $, Return $. One row per operating hour. Shows exactly when sales volume peaks and troughs, and where discounting concentrates.

**LP read:** A 2pm–3pm row showing 3 transactions and $0 discounts followed by 4pm–5pm showing 8 transactions with 40% discount rate is a pattern worth examining in the chirp feed.

### By-Hour Transaction Chart
Bar chart of transaction count by hour. Standard retail operating pattern for the location. Unusual dips during otherwise busy periods surface visually here before a manager notices them in a report.

### vs. Prior Period (Right Rail)
Comparison column for each KPI: Today vs. Last Week (same day) and Today vs. Last Year (same calendar day if available). Simple +/- delta. Not a deep analytics tool — a quick sanity check for "is today normal?"

### Multi-Store View (ADM)
ADM can select multiple stores or "All Stores." KPI tiles show aggregate totals; the sales breakdown table shows one row per store rather than per hour. Click a store row to drill into that store's hourly breakdown.

**Empty state:** "No transactions recorded for the selected date and store."

## Interaction Flows

1. **Morning flash:** MGR opens Flash Report → defaults to yesterday's data → scans KPIs: net sales on target, discount rate 4% (normal range 2-6%), return rate 1.8% (normal) → no issues, proceed with day
2. **Anomaly detection:** MGR sees discount rate = 14% for yesterday → drills into by-hour table → 2pm–3pm shows $340 in discounts on 4 transactions → opens chirp feed filtered to that window → 3 transactions show comp flag
3. **Cross-store comparison:** ADM opens Flash Report → selects All Stores → sees Store 3's discount rate is 18% vs 3-5% for all other stores → flags for LP review

## UX Callout

CP's sales summary report is a single-store, single-period query that produces a static table. The flash report in Canary is not a replacement for that report — it's a different tool. The prior-period comparison, the by-hour breakdown, and the multi-store ADM view are designed for the 5-minute morning review that a manager does before opening, not the end-of-month financial analysis. The LP-relevant metrics (discount rate, return rate) surfacing as tiles means a manager who glances at the flash report before their morning walkthrough has already done LP triage without knowing it.

## Navigation Exits

- `/chirps` — from by-hour table drill (time-filtered)
- `/reports/category` — deeper category-level analysis
- `/alerts/list` — from high discount rate / return rate tiles

## Open Questions

None.
