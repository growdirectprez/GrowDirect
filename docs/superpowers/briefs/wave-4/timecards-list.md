---
screen: /timecards
title: Timecard List
role: MGR | EMP
wave: W4
origin: O
cp_equivalent: "CP timeclock (frmimtimeclock) — Windows-only or dedicated $1,500 hardware; no mobile entry, no exception flagging"
---

# Timecard List

**URL:** `/timecards`  
**Primary role:** MGR; EMP (Employee — own timecards only)  
**Entry points:** Primary sidebar nav (Labor section)

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Timecards", date range selector, store selector | |
| Filter bar | Status (Pending Review / Approved / Exception), Employee | |
| Main content | Timecard table | |
| Action bar | Approve All (MGR), Export (MGR) | |

## Key Elements

### Timecard Table
Columns: Employee, Store, Date, Clock-In, Clock-Out, Hours, Break Time, Total Paid Hours, Status badge, Exception indicator.

**Status values:**
- **Pending Review:** MGR has not yet approved the timecard entry
- **Approved:** MGR reviewed and approved
- **Exception:** Timecard has a flag requiring MGR attention before approval

**Exception types (visible on hover/expand):**
- Long shift (hours > configured maximum, e.g., > 10 hours)
- Missing clock-out (employee clocked in but no clock-out event recorded)
- Clock-in during closed hours (employee clocked in before store open or after close)
- Duplicate clock-in (two clock-in events without an intervening clock-out)
- Overlapping shifts (employee appears on two shift records simultaneously — possible clock device issue)

**LP context:** The Labor module's detection rules (Q-L family) watch for transactions outside an employee's clocked shift. A cashier processing a high-discount transaction at 6pm while their timecard shows they clocked out at 5pm is either a timecard error or an unauthorized session. The Labor exception flags and the LP alert feed are correlated when this pattern appears.

### Approve All
MGR can approve all Pending Review (non-exception) timecards for the selected period in one action. Exceptions require individual review before approval.

**Empty state:** "No timecards for the selected period and store."

## Interaction Flows

1. **End-of-week approval:** MGR opens timecards → date range = this week → 34 entries, 3 Exceptions → approves all Pending Review in bulk → opens each exception: 2 are missing clock-outs (employee forgot) → MGR enters correct clock-out time with note → approves → 1 is a clock-in during closed hours → investigates
2. **Employee self-review:** EMP opens timecards → filtered to own entries → reviews the week's hours → notices a missing clock-out → notifies MGR for correction
3. **LP timecard correlation:** LP sees a discount alert on a transaction at 6:45pm from cashier #C-0019 → opens timecards → cashier clocked out at 5:30pm → unauthorized session — escalates

## UX Callout

CP's timeclock module runs on Windows PCs or requires a dedicated $1,500 timeclock terminal. The comparison to Canary's timeclock is the same as transfer receipt vs the dock PC: any browser on any device at any location is the Canary model. No dedicated hardware. No CP installation required. A staff member at a remote greenhouse can clock in on their phone. The exception flags automate the review that a manager would otherwise do manually for each of 30+ timecard entries per week — missing clock-outs and after-hours clock-ins are caught automatically, not discovered when payroll runs. The LP correlation with the transaction feed is the integration that CP's disconnected timeclock hardware makes structurally impossible.

## Navigation Exits

- `/timecards/:id` — individual timecard detail / edit
- `/timecards/clock` — clock in/out action (EMP)

## Open Questions

None.
