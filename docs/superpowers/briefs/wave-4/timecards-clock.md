---
screen: /timecards/clock
title: Clock In / Clock Out
role: EMP
wave: W4
origin: O
cp_equivalent: "CP timeclock entry — Windows-only or $1,500 hardware terminal; no mobile, no geo-validation"
---

# Clock In / Clock Out

**URL:** `/timecards/clock`  
**Primary role:** EMP  
**Entry points:** EMP home dashboard clock widget; direct URL; supervisor-shared link

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Employee name, current clock status (Clocked In / Clocked Out) | |
| Main content | Single action button (Clock In or Clock Out) + current time | |
| Status section | Current shift summary (if clocked in) | |

## Key Elements

### Clock Action Button
Single large button. Shows "Clock In" when employee is clocked out; shows "Clock Out" when clocked in.

**Clock In:** Records timestamp, employee, and store. Status changes to "Clocked In at [time]." Shift summary section appears showing elapsed time.

**Clock Out:** Records timestamp. Status changes to "Clocked Out at [time]. Shift: [duration]." Calculates hours for the timecard entry.

### Store Confirmation (multi-store employees)
For employees assigned to more than one store, a store selector appears before the clock action: "Which store are you clocking in at?" Required — timecard entries are store-scoped.

### Current Shift Summary
Visible only when clocked in: Clock-In time · Elapsed time (live counter) · Scheduled shift end (if schedule integration is available — TBD). Simple operational context for the employee.

### Break Recording
"Start Break" / "End Break" buttons appear when clocked in. Break time is tracked separately from shift time. Paid vs unpaid break handling is a configuration parameter (by default, break time is not deducted from paid hours; configurable per labor law requirements).

### Geo-Validation (optional — ADM-configurable)
If enabled, the clock event captures the device's geo-location at the time of clock-in. If the location is outside a configured radius of the store address, a flag is added to the timecard: "Clock-in location: [N] miles from store address." Does not prevent the clock event — flags for MGR review. Addresses remote greenhouse, outdoor nursery, and multi-location operational realities.

**Duplicate clock-in protection:** If the employee attempts to clock in while already clocked in (e.g., they're on a different device), the system shows: "You are already clocked in since [time]. Are you sure you want to clock in again?" Prevents the duplicate-clock-in exception automatically.

**Empty state:** Not applicable — action screen.

## Interaction Flows

1. **Standard shift start:** EMP opens clock page → taps Clock In → confirmation shown: "Clocked in at 8:02 AM" → returns to normal work
2. **Break recording:** EMP taps Start Break → "Break started at 10:15 AM" → returns from break → taps End Break → "Break: 18 minutes" → shift time continues
3. **Shift end:** EMP taps Clock Out → "Clocked out at 4:47 PM. Shift: 8h 45min (with 18min break)." → timecard enters Pending Review queue for MGR approval

## UX Callout

The entire point of this screen is that it runs on any browser, on any device, at any location. The $1,500 timeclock terminal is a piece of hardware that enforces physical presence at a specific location (the device is bolted to the wall near the time office). Canary's clock screen is intentionally untethered — an employee at the greenhouse 200 yards away, or staging a display in the parking lot, can clock in on their phone without walking to the timeclock first. The geo-validation flag (when enabled) replaces the physical-location enforcement with a post-hoc audit: the clock event is recorded where the employee is, and any anomalies are flagged for MGR review rather than blocked at the point of action.

## Navigation Exits

- `/timecards` — after clock-in or clock-out (for EMP: own timecard view)

## Open Questions

None.
