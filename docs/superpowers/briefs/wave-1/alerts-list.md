---
screen: /alerts
title: Alert List
role: LP | MGR
wave: W1
origin: O
cp_equivalent: "None — Counterpoint has no alert surface"
---

# Alert List

**URL:** `/alerts`  
**Primary role:** LP; secondary: MGR  
**Entry points:** Primary sidebar nav; email notification link (deep-link to `/alerts?filter=new`); dashboard alert widget

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Page title "Alerts", alert count badge (unacknowledged), bulk-acknowledge button | Count updates in real-time |
| Filter bar | Severity, Store, Alert Type, Status, Date range | Persistent; multi-select where applicable |
| Main content | Paginated alert table | Primary working surface |
| Action bar | Bulk-select controls (select all, deselect, acknowledge selected) | Appears when any row is selected |

## Key Elements

### Alert Table
Columns: Severity badge (Critical / High / Medium — color-coded red/orange/yellow), Alert Type (e.g., Drawer Variance, Discount Cap, Void, Comp), Rule Name (e.g., "Q-DC-01 Drawer Cash Detection"), Store, Cashier/Terminal, Transaction Amount, Timestamp (relative, e.g., "12 minutes ago"), Status badge (New / Acknowledged / Escalated / Case-Linked).

Rows sort by: newest first (default), severity descending, amount descending. Click row → navigates to `/alerts/:id`.

**Empty state:** "No alerts match the current filters." For new tenants in Phase 1 (config sync only): "LP monitoring is not yet active for this tenant. Complete configuration in `/settings/store` to enable detection rules."

### Bulk-Acknowledge
Checkbox on each row. Select multiple → "Acknowledge Selected" button appears in action bar. Opens a batch disposition modal: disposition code (Explained / False Positive) + optional note. Does not require opening each alert individually. Essential for clearing low-severity noise at the start of a shift.

### Severity Filter
Single-click to toggle severity levels. LP investigator standard workflow: start with Critical only → work to High → end with Medium. Filter state persists in session.

## Interaction Flows

1. **Shift start triage:** LP opens alerts, filters to Critical + New → reviews high-priority alerts → bulk-acknowledges the ones that are clearly explainable → clicks remaining alerts one by one to investigate
2. **Store-specific review:** MGR filters by their store → sees alert volume for the week → identifies a spike on Tuesday evening → clicks through to the date-filtered view
3. **Escalate to case:** LP finds an alert that warrants investigation → clicks row → opens `/alerts/:id` → escalates from detail view (not from the list)

## UX Callout

This is the primary entry point for every LP shift. Every design decision on this screen serves triage speed: severity filtering is front-and-center rather than buried in an advanced filter panel; bulk-acknowledge exists specifically because LP teams start every shift drowning in medium-severity alerts that are explainable at a glance; the status badge distinguishes New/Acknowledged/Escalated/Case-Linked so LP managers can see at a glance where each alert is in the lifecycle. Counterpoint has no alert surface at all — LP teams in CP shops discover anomalies only after running manual reports, hours after the transaction.

## Navigation Exits

- `/alerts/:id` — alert detail for any row
- `/settings/alert-routing` — if receiving too many / too few notifications
- `/rules` — to understand which rules are generating the most alerts

## Open Questions

None.
