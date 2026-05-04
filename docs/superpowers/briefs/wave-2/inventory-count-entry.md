---
screen: /inventory/count/:id
title: Count Entry + Manager View
role: CNT | MGR
wave: W2
origin: N
cp_equivalent: "frmimphysicalcount entry — Windows-only, no mobile, no real-time progress, paper tally then key-in"
---

# Count Entry + Manager View

**URL:** `/inventory/count/:id`  
**Primary role:** CNT (mobile entry); MGR (portal view + oversight)  
**Entry points:** Count list row; counter in-app notification link

## Layout — CNT (Mobile)

| Zone | Content | Notes |
|---|---|---|
| Header | Count ID, store name, item progress (47 / 120) | No nav chrome — focused mobile form |
| Main content | Active line card (one item at a time) | Swipe or tap Next to advance |
| Entry field | Large numeric keypad for quantity | Full-width tap target |
| Action bar | Next Item, Flag Issue, Save & Exit | |

## Layout — MGR (Portal)

| Zone | Content | Notes |
|---|---|---|
| Header | Count ID, status badge, store, count type, progress bar | |
| Filter bar | Status (Not Started / Entered / Flagged), Department | |
| Main content | Count sheet table | All lines, sortable |
| Right rail | Count summary — items entered, items remaining, flagged lines | |
| Action bar | Complete Count, Export Sheet, Print Sheet | Complete available when all lines entered |

## Key Elements — CNT Mobile

### Active Line Card
Shows: Item # · Description · Department · Storage location (if configured) · Entry field.

**Expected Qty is intentionally hidden on the CNT entry view.** Counter enters what they physically count, unanchored by the system's expectation. Showing expected quantity biases the count — counters are tempted to round to the expected number rather than count accurately. This is standard cycle-count practice.

### Navigation Between Lines
CNT can tap "Next Item" to advance sequentially, or use search to jump to a specific item by scanning its barcode. Barcode scan jumps directly to that item's entry card.

### Flag Issue
If CNT cannot locate or count an item (e.g., item is stocked in a locked case, item appears missing from shelf), they tap "Flag Issue" and optionally add a note. Flagged lines are visible to MGR and require resolution before the count can be completed.

### Save & Exit
CNT saves current progress and exits. Returns to the count list. Re-entering the count later resumes from the next uncounted line.

## Key Elements — MGR Portal

### Count Sheet Table
Columns: Item #, Description, Department, Storage Location, Expected Qty (from perpetual ledger at count start), Entered Qty, Variance Qty (entered − expected), Status (Not Started / Entered / Flagged).

**Variance column:** Real-time. Shows variance as CNT entries are submitted. Positive = over. Negative = short. Color: zero = green, positive = blue, negative = orange (>10% or >$50 value = red).

### Complete Count Action
Available only when all lines are Entered (no Not Started lines remaining). Flagged lines must be resolved or explicitly overridden ("mark as unresolved — proceed"). Completing the count transitions status → Completed and unlocks the Post screen.

### Real-Time Progress
Progress bar in header and right rail summary update as CNT entries come in. MGR can watch the count proceed from the portal while counters work the floor.

### Export / Print Sheet
Exports a PDF or CSV of the count sheet at any point. Used for manual backup, audit documentation, or offline fallback if a counter's device fails mid-count.

## Interaction Flows

1. **Counter scans and enters (mobile):** CNT opens notification link → count entry card loads → scans barcode of first item → enters 42 → taps Next → repeats through all 120 lines → Save & Exit
2. **Manager monitors in real time:** MGR watches portal → sees 60/120 lines entered → variance column shows −3 on item #7734 (flagged by CNT as "not on shelf") → MGR resolves flag by confirming item is physically missing → count proceeds
3. **Barcode shortcut:** CNT at a random shelf location scans item #6692 → jumps directly to that item's entry card → enters count → continues scanning nearby items in any order

## UX Callout

The hidden-expected-quantity design is the most important behavioral detail on this screen. In CP, the count entry form shows the system's on-hand next to the entry field — the count is biased before the counter has typed anything. Canary hides expected quantities from counters intentionally: the count is a physical audit, and it only has evidentiary value if it's independent of what the system believes. This is not a missing feature; it's a deliberate integrity constraint. (Managers see expected quantities in the portal view — that's appropriate; they're not the ones doing the physical count.)

The two-persona design (mobile counter + portal manager) reflects the physical reality of a count: counters are on the floor with phones, managers are at the office or watching remotely. CP requires both to use the same desktop form, which means one or the other is doing something awkward.

## Navigation Exits

- `/inventory/count` — Save & Exit (counter) or back (manager)
- `/inventory/count/:id/post` — after Complete Count (manager)

## Open Questions

None.
