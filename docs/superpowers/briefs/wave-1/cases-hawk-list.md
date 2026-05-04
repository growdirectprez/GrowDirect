---
screen: /cases/hawk
title: Case List (Hawk)
role: LP | MGR
wave: W1
origin: O
cp_equivalent: "None"
---

# Case List (Hawk)

**URL:** `/cases/hawk`  
**Primary role:** LP; secondary: MGR  
**Entry points:** Primary sidebar nav (Investigations section); alert detail → "Escalate to case"

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Page title "Cases", New Case button, open case count | "23 open cases" format |
| Filter bar | Status, Store, Assignee, Date range, Case type, Search | Search covers case ID, subject name, cashier, ticket # |
| Main content | Case table | Primary working surface |

## Key Elements

### Case Table
Columns: Case ID, Subject Name (cashier name or customer name — primary subject), Store, Case Type (Void Fraud / Discount Abuse / Transfer Shrink / Refund Fraud / Pattern — expandable), Status badge (Open / Under Review / Pending / Closed), Days Open (integer — urgency signal), Evidence Count, Assigned Investigator.

Sorted by Days Open descending by default — oldest open cases first. This is intentional: stale cases are a real operational problem.

**Days Open field:** Color-coded: < 7 days = grey (normal), 7–14 days = yellow (attention), > 14 days = red (stale). LP managers use this column to manage caseload without running a report.

**Empty state:** "No open cases. Create a new case or escalate an alert to begin an investigation."

### Status Badge Colors
Open = blue, Under Review = purple, Pending = orange (awaiting manager review/HR action), Closed = grey. Status progression: Open → Under Review → Pending → Closed.

### New Case Button
Creates a blank case directly (without a seed alert). Used when LP starts an investigation from a pattern observed in the chirp feed rather than from an alert. Navigates to a case creation modal → creates case → redirects to `/cases/hawk/:id`.

## Interaction Flows

1. **Start-of-shift caseload review:** LP opens cases list → sees their 5 open cases → sorts by Days Open → identifies 2 cases > 14 days (red) → prioritizes working those first
2. **Search for case by subject:** LP received a manager inquiry about cashier J. Martinez → searches "Martinez" → finds all open cases with Martinez as subject → selects the relevant one
3. **Case created from alert escalation:** LP is in `/alerts/:id` → escalates → case created → list auto-navigates to the new case → case appears at top of list with Days Open = 0

## UX Callout

Days open as a visible, color-coded, sort-default column is the single most operationally important design decision on this screen. In every LP department that manually manages cases (spreadsheets, email threads), stale investigations are the norm — cases fall through the cracks because there's no system forcing attention on them. Canary's cases list surfaces stale cases through ordering and color-coding, without requiring a report or a manager's manual audit. CP has no case management concept at all.

## Navigation Exits

- `/cases/hawk/:id` — case detail for any row
- `/cases/hawk/analytics` — aggregated case analytics (tab or separate nav item)
- `/cases/hawk/patterns` — cross-case pattern view

## Open Questions

None.
