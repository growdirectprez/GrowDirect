---
screen: /inventory/count/new
title: Count Setup
role: MGR
wave: W2
origin: N
cp_equivalent: "frmimphysicalcount setup — Windows-only, no item filtering at initiation, no counter assignment"
---

# Count Setup

**URL:** `/inventory/count/new`  
**Primary role:** MGR  
**Entry points:** Count list → New Count button

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "New Physical Count", Save Draft / Start Count buttons | Start Count transitions status to In Progress |
| Top section | Count parameters (store, type, date, notes) | |
| Main content | Scope definition — item/department selector | Shown after type selection |
| Right rail | Summary panel (item count in scope) | Updates as scope is refined |
| Action bar | Save Draft, Start Count, Cancel | |

## Key Elements

### Count Parameters
- **Store:** Dropdown (required). Single store per count — no multi-store counts.
- **Count Type:** Full / Department / Spot (required). Selection changes the scope definition UI.
- **Scheduled Date:** Date picker. Defaults to today. Used for planning and scheduling counter assignments.
- **Notes:** Optional free text. Reason for count, special instructions for counters.

### Scope Definition (by type)
**Full Count:** No scope selector shown. All active items at the selected store are in scope (count is generated from the perpetual ledger at the moment of Start).

**Department Count:** Department multi-selector appears. MGR selects one or more departments. Item count in scope shown in right rail as departments are selected.

**Spot Count:** Item search field appears. Search by item number or description. Add individual items. Right rail shows running list. Minimum 1 item.

### Counter Assignment (optional)
"Assign Counters" section: add users with CNT role at the selected store. Assigned counters receive an in-app notification: "Count [ID] is ready — open the count to begin entering quantities." Unassigned counts are still accessible to all CNT-role users at the store.

### Start Count Action
Transitions status Draft → In Progress. Freezes the item scope (no additions after start). The count sheet is generated from the current perpetual ledger — item records and expected quantities are captured at this moment. The count remains open until all lines are entered and the MGR completes it.

**Save Draft:** Saves parameters without starting. Count remains Draft; no counters are notified.

**Empty state:** Not applicable — create form.

## Interaction Flows

1. **Schedule a department count:** MGR selects Store 3, type = Department, departments = Tropicals + Succulents → scope = 47 items → assigns two CNT users → Start Count → counters notified
2. **LP spot count:** LP identifies item #8812 as missing-unit alert trigger → MGR creates Spot Count for item #8812 at Store 2 → Start → single-item count sheet generated → CNT enters quantity → post
3. **Draft for future date:** MGR plans next week's full count → Save Draft with next Tuesday's date → no counters notified yet; MGR returns to start the count on the day

## UX Callout

CP's count initiation has no equivalent to counter assignment or real-time scope summary. The MGR creates the count form, prints a tally sheet, and distributes it manually. Canary assigns directly from the setup screen, notifies counters in-app, and shows the item count in scope before committing. A spot count in CP requires the LP investigator to know the item number and ask a manager to manually add it to a count record; in Canary, LP can trigger a spot count with two inputs (store + item #) and the system handles everything else.

## Navigation Exits

- `/inventory/count` — after Start Count (redirects to new count's entry screen) or Cancel
- `/inventory/count/:id` — on Start Count (auto-navigated to count entry)

## Open Questions

None.
