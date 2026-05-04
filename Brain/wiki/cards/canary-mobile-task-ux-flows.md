---
last-compiled: 2026-05-04
needs-review: false
type: reference
status: active
tags: [canary, mobile, ux, task-flows, receiving, replenishment, cycle-count, android, functional-requirements]
created: 2026-05-04
---
last-compiled: 2026-05-04
needs-review: false

# Canary — Mobile Task UX Flows

Functional flow specifications for the four core store operations tasks. These are the daily-use screens for floor associates and owner-operators. The design principle throughout: one action per screen, confirm by scan, exception is never a dead end. Built for Android (phone + tablet), with a sidebar note on Android POS integration where relevant.

Enterprise WMS used RF terminals with 20-character screens and function key navigation. That era is over. These flows assume a modern Android device with a camera (scan via phone camera or Bluetooth ring scanner), persistent connectivity (with offline queue fallback), and a touch interface.

---
last-compiled: 2026-05-04
needs-review: false

## Design Principles

**One screen, one question.** Each step of a flow asks the operator one thing: scan this, confirm this quantity, choose this disposition. No forms with 12 fields. No tabbed interfaces mid-flow.

**Scan is the primary input.** Every item, every location, every container is identified by scanning a barcode or QR code. Manual entry is a fallback — not the standard path.

**Exception is not an error.** A damaged case, a wrong quantity, a location that's full — these are normal events. The UX should handle them in stride, capture the data, and move on. Never a dead end.

**Progress is visible.** Multi-step flows show where the operator is in the sequence. "3 of 8 cases received."

**Offline works.** Back-of-house receiving areas often have poor cellular. The app queues events locally and syncs on reconnect. The operator should not know the difference — same UX, with a subtle sync indicator.

---
last-compiled: 2026-05-04
needs-review: false

## Task 1: Receiving

**Trigger:** a delivery arrives. Operator opens Canary, goes to Receiving.

**Entry points:**
- From PO: operator taps the relevant open PO → "Start Receiving"
- From delivery (no PO): operator selects "Unplanned Delivery" → scans supplier barcode or selects supplier manually

---
last-compiled: 2026-05-04
needs-review: false

**Screen 1 — PO Summary**

```
[Supplier Name]                          PO #12847
Expected: Today, ~2pm                   [In Transit]

Items: 14 lines | 48 cases expected
─────────────────────────────────────
[ Start Receiving ]
[ View Item List ]
```

Tap "Start Receiving" begins the flow.

---
last-compiled: 2026-05-04
needs-review: false

**Screen 2 — Scan Container**

```
Scan next case or pallet label

    [ Camera / Scanner view or barcode input ]

    ─────────────
    Cases received this session: 0 of 48
```

Operator scans the barcode on the incoming case. System matches it to the PO line.

If the barcode matches a PO line → moves to Screen 3.
If the barcode does not match any PO line → Exception branch (Screen 2E).

---
last-compiled: 2026-05-04
needs-review: false

**Screen 3 — Confirm Quantity**

```
[Item Name]           SKU: 0000012847
Expected: 12 units (1 case of 12)

Received quantity:   [ 12 ]   ← editable

[ Confirm ]    [ Exception ]
```

Default quantity is populated from PO. Operator confirms (one tap if quantity is correct) or adjusts. If the case is damaged, taps "Exception."

**Quantity override logic:** if operator types a quantity different from expected, a note field appears: "Reason (optional) — short shipped / damaged / split case." Optional, but captured if provided.

---
last-compiled: 2026-05-04
needs-review: false

**Screen 3E — Exception**

```
[Item Name]   SKU: 0000012847

Exception type:
  ○ Damaged — some units unusable
  ○ Short shipment — fewer units than declared
  ○ Over-shipment — more units than ordered
  ○ Wrong item — not on this PO
  ○ Refused — returning to supplier

Quantity received (good units): [ ___ ]
Quantity damaged / refused: [ ___ ]

[ Confirm Exception ]
```

Exception is logged per unit. Supplier credit claim is queued automatically for damaged or refused quantities.

---
last-compiled: 2026-05-04
needs-review: false

**Screen 4 — Putaway Direction**

```
[Item Name]
12 units confirmed ✓

📍 Put on floor — Aisle 4, Shelf B
   (SOH below display minimum: 3 units on floor, minimum is 6)

   or

📦 Put in back-stock — Zone C, Bin 14

[ Floor ]    [ Back-Stock ]    [ Let me decide ]
```

System recommends floor or back-stock based on current SOH vs. display minimum. The opportunistic-to-floor routing from RDM — when the floor needs stock, the received case goes there immediately, not to back-stock first.

If operator taps "Let me decide" → shows both options without a recommendation.

---
last-compiled: 2026-05-04
needs-review: false

**Screen 5 — Scan Location (if directed)**

```
Confirm location

Scan the shelf label at Aisle 4, Shelf B

    [ Scanner view ]

    [ Skip location scan ]
```

If the store has printed location QR codes at the shelf edge → operator scans to confirm delivery. If not → "Skip location scan" proceeds without scan confirmation. Location scan is best practice but not a hard requirement for v1.

---
last-compiled: 2026-05-04
needs-review: false

**Screen 6 — Next**

```
✓ Received: 12 units of [Item Name]
   → Aisle 4, Shelf B

Progress: 3 of 14 lines | 12 of 48 cases

[ Scan next case ]    [ Done for now ]
```

Loop back to Screen 2 for the next case, or exit mid-flow and resume later. In-progress receiving state is saved.

---
last-compiled: 2026-05-04
needs-review: false

**Completion Screen**

```
✓ Receiving Complete — PO #12847

14 lines received
  ✓ 12 lines: fully received
  ⚠ 1 line: short shipment — 8 of 12 units (note flagged)
  ✗ 1 line: wrong item — refused, return queued

SOH updated: 14 items
Supplier exceptions logged: 2
Invoice ready: $1,847.20

[ Close PO ]    [ Keep Open (back-order expected) ]
```

---
last-compiled: 2026-05-04
needs-review: false

## Task 2: Replenishment

**Trigger:** replenishment task appears in the task queue (system-generated when SOH < display minimum). Operator opens their task queue on mobile and picks up the task — or supervisor assigns it.

---
last-compiled: 2026-05-04
needs-review: false

**Screen 1 — Task Overview**

```
Replenishment Task
─────────────────
Aisle 4, Shelf B → Floor

[Item Name]    SKU 0000012847
Floor SOH: 2 units  |  Minimum: 6
Back-stock: 24 units (Zone C, Bin 14)

Replenish: 12 units (1 case)

[ Start ]    [ Can't complete — flag issue ]
```

All the information the associate needs to decide whether to pick up the task. If they tap "Can't complete" — they choose a reason (location empty / item not found / location blocked) and the task returns to the queue with an exception flag.

---
last-compiled: 2026-05-04
needs-review: false

**Screen 2 — Confirm Pick Location**

```
Go to: Zone C, Bin 14

Scan location label when you arrive

    [ Scanner view ]

[ Skip scan ]
```

Operator walks to back-stock. Scans the bin label (or skips). Location confirmation closes the loop on where stock was pulled from — important for SOH accuracy on the back-stock location.

---
last-compiled: 2026-05-04
needs-review: false

**Screen 3 — Confirm Quantity**

```
Zone C, Bin 14  ✓

Pick quantity:   [ 12 ]   ← default from task

Back-stock remaining after pick: 12 units

[ Confirm Pick ]
```

If the bin has fewer units than the task quantity → operator adjusts. Back-stock SOH is updated immediately on confirmation.

---
last-compiled: 2026-05-04
needs-review: false

**Screen 4 — Confirm Delivery to Floor**

```
Bring to: Aisle 4, Shelf B

Scan shelf label when stocked

    [ Scanner view ]

[ Skip scan ]
```

---
last-compiled: 2026-05-04
needs-review: false

**Screen 5 — Done**

```
✓ Replenishment complete

[Item Name] → Aisle 4, Shelf B
12 units added | Floor SOH now: 14 units

[ Done ]    [ Flag shelf issue ]
```

"Flag shelf issue" opens a free-text note field — operative for planogram violations, damaged shelf, wrong price label. Note goes to the supervisor queue.

---
last-compiled: 2026-05-04
needs-review: false

## Task 3: Cycle Count

**Trigger:** operator is assigned a cycle count zone (typically automated — zones rotate on a schedule). Or operator initiates an ad-hoc count on a specific item/location.

**Purpose:** compare physical count to Canary's recorded SOH. When they differ, investigate and correct. Rolling cycle counts replace the annual wall-to-wall physical inventory.

---
last-compiled: 2026-05-04
needs-review: false

**Screen 1 — Count Assignment**

```
Cycle Count — Zone C
8 locations to count

Estimated time: ~25 minutes

[ Start Count ]
```

---
last-compiled: 2026-05-04
needs-review: false

**Screen 2 — Navigate to Location**

```
Count location 1 of 8

Zone C, Bin 14

Scan location label to begin count

    [ Scanner view ]
```

---
last-compiled: 2026-05-04
needs-review: false

**Screen 3 — Count Items**

```
Zone C, Bin 14  ✓

Items in this location:

  [Item A]  SKU 0000012847   System SOH: 12
  Count: [ ___ ]

  [Item B]  SKU 0000099231   System SOH: 6
  Count: [ ___ ]

[ Confirm count ]    [ Location is empty ]
```

Operator physically counts each item and enters the actual quantity. If an item appears in the location that is not in the system, they scan it → Canary prompts for a quantity and creates an inventory adjustment.

---
last-compiled: 2026-05-04
needs-review: false

**Screen 4 — Discrepancy Review**

If any count differs from system SOH:

```
⚠ Discrepancy found

[Item A]  SKU 0000012847
  System says: 12 units
  Your count:  8 units
  Difference:  -4 units

Reason (optional):
  ○ Theft / shrinkage
  ○ Damaged and disposed
  ○ Moved to another location
  ○ Receiving error
  ○ Unknown

[ Adjust SOH ]    [ Recount ]
```

Operator can recount before committing. Reason codes are optional but build a shrinkage database over time — after 6 months, the operator can see that 80% of Zone C discrepancies are "Theft/Shrinkage" and take action.

---
last-compiled: 2026-05-04
needs-review: false

**Completion Screen**

```
✓ Cycle Count — Zone C Complete

8 locations counted
  ✓ 6 locations: no discrepancy
  ⚠ 2 locations: adjusted

SOH adjustments:
  [Item A]: -4 units (reason: unknown)
  [Item C]: +2 units (receiving entry error)

[ Done ]
```

---
last-compiled: 2026-05-04
needs-review: false

## Task 4: New Item Onboarding

**Trigger:** a new item arrives in a delivery (not previously in Canary). This is the First Time SKU workflow from RDM, rebuilt for a solo SMB operator.

---
last-compiled: 2026-05-04
needs-review: false

**Screen 1 — New Item Detected**

```
⚡ New Item

Barcode: 0 12345 67890 5

This item is not in your inventory system.

Add it now?   [ Yes ]   [ Not now ]
```

"Not now" defers — the case is flagged as unidentified and placed in a holding area. The operator gets a reminder.

---
last-compiled: 2026-05-04
needs-review: false

**Screen 2 — Item Details**

```
New Item Setup

Name / Description:   [ _________________ ]
Supplier:             [ Current supplier ▼ ]
Supplier Case Size:   [ ___ ] units per case
Unit Cost:            $ [ _____ ]
Selling Price:        $ [ _____ ]

[ Continue ]
```

Minimum viable item record. If a product database lookup is available (Open Food Facts, UPC lookup API), Canary pre-fills Name from the barcode and the operator corrects if needed.

---
last-compiled: 2026-05-04
needs-review: false

**Screen 3 — Location Assignment**

```
Where does this item live?

Zone:  [ Zone C ▼ ]
Aisle: [ 4 ▼ ]     Shelf: [ B ▼ ]

Display Minimum (floor):   [ 6 ] units
Display Maximum (capacity): [ 24 ] units

[ Set Location ]
```

---
last-compiled: 2026-05-04
needs-review: false

**Screen 4 — Replenishment Method**

```
How should we reorder this item?

  ○ Min/Max — I'll set the numbers manually
      "Reorder when floor drops below minimum; order up to maximum."

  ○ Auto (needs 4+ weeks of sales data)
      "System learns the sell rate and adjusts automatically."

  ○ Manual only — I'll order when I decide
      "No automatic suggestions."

[ Save and Add to Inventory ]
```

---
last-compiled: 2026-05-04
needs-review: false

**Completion Screen**

```
✓ [Item Name] is now in Canary

Location: Zone C | Aisle 4 | Shelf B
Display min: 6 | Max: 24
Replenishment: Min/Max

Received: 12 units → put on floor (below minimum)

[ Done ]    [ Add another new item ]
```

After onboarding, the item is active in Canary AND queued for sync to the POS item master so it can be scanned at the register.

---
last-compiled: 2026-05-04
needs-review: false

## Android POS Integration Notes

**Register-side scan:** DriftPOS / NCR Counterpoint scan events do not interact with Canary's receiving flow directly — receiving is an operator action, not a POS action. But the POS is the validation surface: if an operator onboards an item in Canary, the item needs to be in the POS before the first sale. Canary → POS item master push should complete within seconds of the Canary onboarding confirmation.

**Ring scanner vs. camera:** for high-volume receiving, operators typically use a Bluetooth ring scanner rather than pointing a phone at every barcode. The app should support both — camera mode via the device camera, Bluetooth mode via standard Android Bluetooth HID profile. The UI should not care which input method provides the scan — it listens for barcode text input regardless of source.

**Tablet vs. phone layout:** the flows above are designed for phone (one action per screen). On a 10" tablet in landscape, multiple screens can consolidate: Screen 2–3 of receiving (scan + confirm quantity) can be a split-pane view. The task system should detect device size and adapt the layout — the flow logic is identical, only the visual density changes.

---
last-compiled: 2026-05-04
needs-review: false

## What These Flows Replace

In a store without Canary, this work looks like:
- Receiving: count boxes against a paper packing slip, write numbers on the slip, hand it to the owner who enters it in the POS back-office (or doesn't)
- Replenishment: walk the floor, eyeball shelves, carry stock from the back when you notice it's low (if you notice)
- Cycle count: the annual physical inventory count during which the store closes early
- New item: manually enter item into the POS back-office, hope the barcode is right

The friction is enormous. The accuracy is low. The timing is wrong (you find out stock is low when a customer tells you). Canary's task flows are not a feature — they are the operational substrate that makes everything else (replenishment intelligence, cost-to-serve, analytics) possible. Garbage in = garbage out. These flows are where accurate data is created.

[[Brain/wiki/cards/store-ops-capability-model]] · [[Brain/wiki/cards/canary-purchase-order-lifecycle]] · [[Brain/wiki/cards/canary-demand-sensing-smb]] · [[Brain/projects/Canary]]
