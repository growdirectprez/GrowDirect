---
screen: /reports/labor
title: Labor Report
role: MGR | ADM
wave: W4
origin: O
cp_equivalent: "Labor/payroll summary in CP — single-store, no labor efficiency metric, no LP correlation column"
---

# Labor Report

**URL:** `/reports/labor`  
**Primary role:** MGR; ADM  
**Entry points:** Primary sidebar nav (Reports section → Labor)

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Labor Report", date range selector, store selector | |
| Filter bar | Employee, Department, Status (Approved / Pending / Exception) | |
| Main content | Labor table | |
| Bottom section | Totals + export | |

## Key Elements

### Labor Table (Grouping: By Employee)
Default grouping. Columns: Employee, Store, Total Hours, Approved Hours, Pending Hours, Exception Hours, Avg Hours/Day, Alert Count During Shifts, LP Exception flag.

**Alert Count During Shifts:** The LP labor intelligence column. For each employee in the period, how many LP alerts fired during their clocked-in time. This is the inverse of the timecard-LP correlation: instead of asking "was the employee clocked in when this alert fired?", the labor report asks "how many alerts are associated with this employee's active shifts?"

A cashier with 120 clocked hours and 0 alerts is operating normally. A cashier with 120 hours and 28 alerts is a statistical outlier worth examining in the alert detail.

**LP Exception flag:** Appears when the employee has transactions outside their clocked shift time (Q-L rule fired) in the selected period. The LP exception isn't surfaced in the alert feed only — it's visible here as a workforce-level signal.

### Labor Table (Grouping: By Day)
Date-row grouping. Columns: Date, Total Staff Hours, Transactions, Labor Efficiency (transactions per labor hour), Discount Rate, LP Alerts.

**Labor Efficiency (transactions/labor hour):** A simple throughput metric. Not the only measure of productivity, but anomalous dips — a day with 12 staff hours and 20 transactions — might reflect low customer volume, overstaffing, or (rarely) data integrity issues.

### Export
Standard CSV export of the current view. Used for payroll processing integration — the approved hours export feeds wherever the operator runs payroll.

**Empty state:** "No timecard data for the selected period."

## Interaction Flows

1. **Payroll prep:** MGR opens labor report → current week → all employees → filters Status = Approved → exports approved hours → sends to payroll
2. **LP workforce triage:** LP opens labor report → sorts Alert Count During Shifts descending → top 3 cashiers have significantly more alerts than peers → opens each cashier's profile in the alert system
3. **Staffing efficiency:** MGR opens By Day grouping → compares labor hours vs transactions per day → identifies Monday as consistently overstaffed (8 staff hours, same volume as Tuesday with 5 hours) → adjusts Monday scheduling

## UX Callout

The LP columns (Alert Count During Shifts, LP Exception flag) are the additions that make the labor report more than a payroll summary. In CP, labor data and LP data are in separate systems — correlating them requires manual export and join operations. Canary keeps them together because the correlation question ("which employees are generating LP alerts?") is a routine LP management task, not a special investigation. Making it visible in the standard labor report means MGR gets a passive LP signal every time they run payroll, without having to know to look for it.

## Navigation Exits

- `/timecards` — detail view per employee
- `/alerts/list` — from alert count column (filtered to employee)

## Open Questions

None.
