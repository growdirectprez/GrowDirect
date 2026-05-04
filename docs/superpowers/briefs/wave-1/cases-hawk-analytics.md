---
screen: /cases/hawk/analytics
title: Case Analytics
role: LP | MGR
wave: W1
origin: O
cp_equivalent: "None"
---

# Case Analytics

**URL:** `/cases/hawk/analytics`  
**Primary role:** MGR; secondary: LP  
**Entry points:** Investigations nav → Analytics tab; Cases list navigation

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Page title "Case Analytics", date range selector, store filter | Defaults to current 30-day period |
| KPI row | 4 summary KPIs — cases open, cases closed, avg days to close, estimated dollars at risk | Full-width row, above all charts |
| Left column | Chart: Cases by Store + Chart: Cases by Rule Family | ~50% width |
| Right column | Investigator Workload table + Case Age Histogram | ~50% width |
| Bottom | Period comparison: this period vs prior period | Full-width summary table |

## Key Elements

### KPI Row
- **Cases Open:** Count of all open cases (all statuses except Closed)
- **Cases Closed This Period:** Count of cases closed within the selected date range
- **Avg Days to Close:** Mean age of cases closed this period. Benchmark: 7 days = healthy; > 14 days = stale
- **Estimated Dollars at Risk:** Sum of transaction amounts attached as evidence across all open cases. Calculated field — not a loss figure, a risk exposure figure. Contextualizes LP caseload for management.

### Cases by Store Chart
Bar chart — one bar per store. X-axis: store name, Y-axis: case count. Click bar → filters entire dashboard to that store. Reveals which stores have disproportionate LP caseload relative to transaction volume.

### Cases by Rule Family Chart
Pie or bar chart — one segment/bar per rule family (Void, Discount, Drawer, Return, etc.). Shows which detection families are generating investigation work. If "Void Fraud" is 70% of all cases, LP and MGR should discuss whether void rules are calibrated correctly or if there's a genuine void abuse pattern.

### Investigator Workload Table
Columns: Investigator name, Open Cases, Closed Cases (period), Avg Days to Close, Estimated Dollars Active. Allows LP manager to see if workload is unevenly distributed.

**Empty state (no closed cases):** "No cases closed in this period. Avg days to close: —"

### Case Age Histogram
Distribution of open case ages (0–7 days, 7–14, 14–30, > 30). Visual answer to: "are we closing cases promptly?" A healthy LP operation has most cases in the 0–7 bucket.

## Interaction Flows

1. **Period performance review:** MGR opens analytics → sets date range to current month → reviews KPIs → sees estimated dollars at risk = $4,200 across 8 open cases → downloads report for management review
2. **Identify troubled store:** MGR sees "Cases by Store" chart with Store 3 having 3× the case count of other stores → filters dashboard to Store 3 → sees cases are primarily Void Fraud family → checks rule calibration
3. **Workload rebalancing:** LP manager sees investigator A has 12 open cases vs investigator B with 3 → reassigns cases from investigator A to B (assignment change made in case detail, not from this screen)

## UX Callout

Estimated dollars at risk — calculated from transaction amounts in evidence across all open cases — is the LP management metric that neither CP nor any standard spreadsheet-based LP operation can produce automatically. It answers the CFO question "how much are we investigating right now?" in a single field. CP LP managers answer this question by running manual reports, multiplying loss rates by case count, and estimating. Canary computes it from the actual evidence attached.

## Navigation Exits

- `/cases/hawk` — back to case list
- `/cases/hawk/patterns` — pattern view
- `/cases/hawk/:id` — any case referenced by chart drill-down

## Open Questions

None.
