---
screen: /reports/shrink
title: Shrink Report
role: LP | MGR | ADM
wave: W3
origin: N
cp_equivalent: "None — CP has no shrink report; inventory adjustments and variances are not aggregated"
---

# Shrink Report

**URL:** `/reports/shrink`  
**Primary role:** LP; MGR; ADM  
**Entry points:** Primary sidebar nav (Reports section → LP Reports); case analytics → shrink link

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Shrink Report", period selector, store selector | |
| Top section | Shrink KPI tiles | |
| Main content | Shrink breakdown table | |
| Bottom section | Shrink by source chart | |

## Key Elements

### Shrink KPI Tiles
Four tiles for the selected period:
- **Total Shrink ($):** All confirmed shrink events (transfer variances, count variances, adjustment write-offs)
- **Shrink Rate (%):** Total Shrink ÷ Net Sales. The standard retail shrink metric. Industry benchmark: 1-2% for specialty retail; > 3% is concerning.
- **Known Loss:** Shrink with identified cause (transfer variance → carrier loss, damage write-off, etc.)
- **Unknown Loss:** Shrink with no identified cause. The LP target — unknown loss is the theft and undetected shrink pool.

**Unknown Loss % of Total:** The most important LP signal. Known loss explains itself; unknown loss requires investigation. Rising unknown loss % is a leading indicator of internal theft acceleration.

### Shrink Breakdown Table
Rows grouped by source type: Transfer Variance / Physical Count Variance / Manual Adjustment / Return Write-off / Vendor Return. Columns: Source, Events (#), Shrink Value ($), % of Total Shrink, Avg Event Size ($), Stores Affected.

Expandable rows: click a source type to see individual events in that category for the period.

### Shrink by Source (Chart)
Pie chart or stacked bar: proportion of total shrink by source. Visual representation of where loss is coming from. Transfer variance dominating → focus on transit shrink. Manual adjustment dominating → focus on adjustment discipline. Physical count variance dominating → focus on counting accuracy or between-count loss.

### Shrink by Store (secondary view)
Bar chart: shrink value per store for the period. Identifies high-shrink locations. Combined with shrink rate (shrink ÷ that store's sales), shows whether a high-shrink store is simply high-volume or genuinely high-loss.

**Empty state:** "No shrink events recorded for the selected period."

## Interaction Flows

1. **Monthly LP review:** LP opens shrink report → last 30 days → unknown loss = 64% of total ($1,840 of $2,870 total) → unexpectedly high → drills into unknown loss events → 3 physical count variances with no associated alerts → opens investigation
2. **Store comparison:** ADM opens shrink report → All Stores → Shrink by Store chart shows Store 3 at 4.2% shrink rate vs 1.1-1.8% for all others → LP priority investigation for Store 3
3. **Transfer variance analysis:** LP opens shrink report → Transfer Variance source → expands rows → same two stores (Store 1 → Store 3) account for 80% of transfer variance events → cross-references with transfer list → pattern alert already flagged by system

## UX Callout

CP cannot produce a shrink report. Shrink in CP is distributed across manual adjustment records, transfer variance events, and count adjustments — three separate record types with no aggregation. An LP manager wanting to know their shrink rate for the quarter must export all three record types, join them manually, and calculate the metric in Excel. Canary aggregates all shrink events into a single report with the known/unknown split as a first-class metric. The unknown loss percentage is the LP insight that drives investigation priority: it converts the abstract question "are we losing money?" into the operational question "where is the unaccounted loss, and in which stores?"

## Navigation Exits

- `/cases/hawk/analytics` — for case-level context on unknown loss
- `/inventory/adjustments` — from adjustment source drill-down
- `/transfers/:id/variance` — from transfer variance source drill-down

## Open Questions

None.
