---
screen: /reports/promotions
title: Promotions Report
role: MGR | BYR
wave: W4
origin: N
cp_equivalent: "None — CP has no aggregate promotion performance report"
---

# Promotions Report

**URL:** `/reports/promotions`  
**Primary role:** MGR; BYR  
**Entry points:** Primary sidebar nav (Reports section → Merchandising)

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Promotions Report", date range selector, store selector | |
| Filter bar | Promo type, Status (Active / Completed / All), Category | |
| Main content | Promotions performance table | |
| Bottom section | Totals + period comparison | |

## Key Elements

### Promotions Performance Table
Columns: Promo Name, Type, Period (start-end), Transactions, Discount Value ($), Avg Discount per Transaction ($), Incremental Units (est.), Net Revenue Impact ($), LP Alert Count, ROI (est.).

**ROI (est.):** Net Revenue Impact ÷ Discount Value. A simplified proxy for promotion return. > 1.0 means the promotion generated more incremental revenue than it cost in discounts. < 0 means the discount was given with no measurable lift (price was reduced but units didn't increase). This is an estimate — Canary uses pre/post velocity comparison rather than a true controlled experiment.

**LP Alert Count:** Total LP alerts associated with transactions using each promotion. The column that flags potentially abused promotions — a promotion with 8× the alert density of other promotions during the same period is a pattern worth examining.

**Period comparison:** Side-by-side or delta comparison to the same period last year for recurring promotions (e.g., "Spring Sale 2026 vs Spring Sale 2025").

**Empty state:** "No promotions in the selected period."

## Interaction Flows

1. **Post-season promotion review:** BYR opens promotions report → last 90 days → all completed promotions → sorts by ROI descending → top 3 promotions for repeat next season; bottom 2 (negative ROI) for redesign or elimination
2. **Budget reconciliation:** Finance opens report → sum Discount Value column = total promotional discounts for the quarter → compares to promotional budget → 12% overspend → flags top 3 promotions for cost review
3. **LP ROI check:** LP opens report → sorts LP Alert Count descending → 1 promotion has 34 alerts vs 0-3 for all others → opens promotion detail for LP context investigation

## UX Callout

In CP, promotion performance requires exporting transaction data, filtering by promotion code, and manually calculating the relevant metrics. There is no aggregate promotion performance report. Canary's promotions report is the post-hoc evaluation tool that closes the promotion lifecycle: design → execute → measure → iterate. Without measurement, promotions run on intuition. The LP alert column brings the same cross-module signal as the flash report's discount rate and the labor report's alert count — LP intelligence embedded passively in the normal merchandising review, not confined to the LP module.

## Navigation Exits

- `/promotions/:id` — from promotion row
- `/reports/sales` — for transaction-level drill-down

## Open Questions

None.
