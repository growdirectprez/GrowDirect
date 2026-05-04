---
last-compiled: 2026-05-04
needs-review: false
type: reference
status: active
tags: [canary, purchase-orders, supplier, workflow, mobile, android-pos, functional-requirements]
created: 2026-05-04
---
last-compiled: 2026-05-04
needs-review: false

# Canary — Purchase Order Lifecycle

The full arc from "I need to reorder this" to "it's on the shelf and SOH is current." This is the operational heartbeat of a retail store — it happens multiple times per week for a multi-supplier operation. The RMS/ORMS model got the data structure right; the delivery was wrong (buyer workstations, batch EDI, approval queues that required a desktop). Canary does the same workflow on a phone.

---
last-compiled: 2026-05-04
needs-review: false

## The Business Problem

A Main Street retailer sources from 10–40 suppliers. Each has a different order cadence, minimum order value, lead time, and delivery schedule. The operator is simultaneously managing the floor, handling customers, and trying to figure out what to order before the weekly rep call. There is no buyer. There is no purchasing department. The operator IS the buyer.

The job to be done: make the right order, to the right supplier, at the right quantity, without a spreadsheet, without a phone call, and without missing the delivery window.

---
last-compiled: 2026-05-04
needs-review: false

## Order Control Modes

Three modes, selectable per supplier. The key insight from ORMS: not every supplier needs the same approval posture.

| Mode | How it works | When to use |
|---|---|---|
| **Auto** | System generates and submits the order without review | High-trust, high-velocity suppliers where the algorithm is reliable (e.g., primary grocery supplier on Dynamic replenishment) |
| **Review** | System proposes the order; operator reviews and approves before submission | Default for most suppliers — operator wants to see the order but not calculate it |
| **Manual** | Operator creates the order entirely | New supplier relationships, custom orders, seasonal buys |

The order control mode is set on the supplier profile and can be changed per order if needed. Auto mode should require explicit opt-in — the default should be Review, because the operator needs to trust the algorithm before delegating to it.

---
last-compiled: 2026-05-04
needs-review: false

## PO Status Machine

```
Draft → Submitted → Confirmed → In Transit → Received (partial / complete) → Closed
                  ↘ Cancelled (at any pre-receipt status)
```

| Status | Who controls | Key events |
|---|---|---|
| **Draft** | Operator / system | Order created; items and quantities editable; no supplier visibility |
| **Submitted** | Operator | Transmitted to supplier (EDI, email, or portal); order locked for edits |
| **Confirmed** | Supplier | Supplier acknowledges; may modify quantities (back-order flags per line) |
| **In Transit** | System (ASN or manual) | Delivery en route; expected arrival date confirmed |
| **Received** | Operator (receiving flow) | Goods counted and scanned; SOH updated; exceptions flagged |
| **Closed** | System | All lines received or cancelled; invoice reconciliation complete |

**Edit rules by status (from RMS — still correct):**

| Action | Draft | Submitted | Confirmed |
|---|---|---|---|
| Add lines | ✓ | ✗ | ✗ |
| Change quantity (up) | ✓ | ✗ (cancel + reorder) | ✗ |
| Change quantity (down) | ✓ | Cancel line | Cancel line |
| Change delivery date | ✓ | ✓ (notify supplier) | ✓ (notify supplier) |
| Cancel entire PO | ✓ | ✓ (notify supplier) | ✓ (notify supplier, may have penalties) |

Once submitted, the order is a commitment. Canary should enforce this — no silent quantity edits after submission.

---
last-compiled: 2026-05-04
needs-review: false

## Supplier Profile — Required Fields

Every supplier in Canary has a profile that drives order behavior. These are the fields that matter operationally (not billing/contact — those live elsewhere):

```
Supplier Profile
├── Order Control Mode: Auto / Review / Manual
├── Lead Time (days): COLT and NOLT (current and next cycle, per ORMS)
├── Review Cycle: how often orders are generated (daily / weekly / by day-of-week)
├── Order Minimum: dollar value or case count threshold (order fails if below)
├── Delivery Schedule: which days supplier delivers; what warehouse/DC they ship from
├── Truck Split: does the supplier split large orders into multiple deliveries? (truckload threshold)
├── Rounding Rule: round quantities to case / layer / pallet (relevant for case-pack items)
└── Transmission Method: EDI / email / portal URL / phone (manual)
```

**Supplier minimums enforcement:** if a generated order falls below the supplier minimum, Canary presents three options:
1. Hold — save as draft, add more items before submitting
2. Accept — submit below minimum (supplier may charge a short-order fee)
3. Skip this cycle — defer to next review cycle

This replaces the RMS "purge orders failing minimums" binary. The operator decides, not the system.

---
last-compiled: 2026-05-04
needs-review: false

## PO Creation Flows

### Flow A: System-Proposed (Review Mode)

Most common for established suppliers.

```
Review cycle triggers (scheduled or manual)
    ↓
System calculates ROQ per item (Min/Max or Dynamic algorithm)
    ↓
Items with ROQ > 0 aggregated into a draft PO for the supplier
    ↓
Operator receives notification: "Proposed order for [Supplier] — review required"
    ↓
Mobile review screen:
  - Item list with: current SOH | recommended qty | unit cost | line total
  - Adjust any quantity (up or down)
  - Remove any line
  - Add items not on the proposed list
  - Supplier minimum check shown live (running total vs. minimum)
    ↓
Approve → PO moves to Submitted → transmission to supplier
```

**Mobile UX requirement:** the review screen must surface the recommendation clearly but make it trivially easy to change. The operator is a domain expert — the system's recommendation is a starting point, not an override. Default to the system quantity; let the operator edit without friction.

### Flow B: Manual Order

For new suppliers, seasonal buys, or items not on the replenishment system.

```
Operator initiates: "New Order" → select supplier
    ↓
Item search / scan (barcode scan to add item)
    ↓
Enter quantity per item
    ↓
Set delivery date (Not Before Date — from ORMS model)
    ↓
Review summary → Submit or Save as Draft
```

**Not Before Date:** the earliest acceptable delivery date. Critical for operators who need to control when merchandise arrives (pre-weekend for a Saturday sale, post-renovation for a reset). The system should default to Today + Lead Time but let the operator override.

### Flow C: Auto Mode

```
Review cycle triggers
    ↓
System calculates ROQ and verifies supplier minimum is met
    ↓
If minimum met: order submitted automatically; operator notified (FYI, not approval request)
If minimum not met: order held in Draft; operator notified to review
    ↓
Confirmation from supplier (if EDI) or assumed confirmed (if manual transmission)
```

Auto mode should produce a daily digest notification, not a per-order notification. Operators in auto mode have opted out of individual order management — don't pull them back in.

---
last-compiled: 2026-05-04
needs-review: false

## Receiving Against a PO

When a delivery arrives, the operator opens the corresponding PO in Canary and works through the receiving flow (detailed in the Mobile Task UX card). The key PO-level behaviors:

**Expected vs. received reconciliation:** every line on the PO has an expected quantity. Receiving records the actual quantity. Discrepancies generate exceptions:

| Discrepancy type | System action |
|---|---|
| Short shipment (received < expected) | Flag line as partial; leave open for back-order fulfillment or closure |
| Over-shipment (received > expected) | Flag for operator decision: accept overage or return |
| Item not ordered | Flag as unauthorized; operator decision to accept or return |
| Item damaged | Record damage quantity; flag for supplier credit claim |

**Partial receipt:** the PO can remain open after a partial delivery. When the back-order portion arrives, the operator scans against the same PO. Only closes when all lines are fully received or explicitly cancelled.

**SOH update timing:** SOH is updated at scan confirmation, not at PO close. The moment a case is scanned as received, Canary's inventory is current. No waiting for end-of-day.

---
last-compiled: 2026-05-04
needs-review: false

## Android POS Integration Points

| PO event | POS action |
|---|---|
| New item added to PO (first-time order) | Queue POS item master add (pending until receiving confirmed) |
| Item received (line closed) | Update POS SOH for the item at this store |
| Over-shipment accepted | Update POS SOH for accepted quantity |
| PO closed | Trigger invoice ready event for accounting integration |

**Item master timing:** new items should NOT appear in the POS until they are physically received and shelf-located. A PO for a new item should not pre-activate the item in the POS — that creates a POS scan error if the item hasn't arrived yet. Canary triggers the POS item master add at the moment of first receiving confirmation.

---
last-compiled: 2026-05-04
needs-review: false

## Supplier Minimums and Scaling — SMB Reality

ORMS had an elaborate truck-splitting and order-scaling engine. For SMB, the translation is simpler:

**Order scaling for SMB:** if the system-proposed order exceeds what will fit in the store's back-stock capacity (a constraint ORMS didn't have — DCs have unlimited reserve), Canary should flag it. "This order would create more back-stock than your zone capacity allows. Recommend reducing by X cases or scheduling a split delivery."

**Rounding to case packs:** every item has a supplier case pack size (e.g., 12 units per case). Canary rounds order quantities to the nearest full case and shows the operator: "Recommended 47 units → rounded to 48 (4 cases of 12)." The increment percent concept from ORMS — 100% means always order in full case multiples.

---
last-compiled: 2026-05-04
needs-review: false

## Canary-Specific Additions (No Enterprise Precedent)

**Order cost transparency:** each proposed order shows total cost, estimated margin impact (if cost basis is current), and days-of-supply covered. An operator reviewing a proposed $2,400 order for one supplier should see: "$2,400 — covers ~18 days at current velocity — 28% estimated margin."

**Supplier performance tracking:** every PO generates a receipt that compares expected vs. actual delivery. Over time: on-time delivery rate, fill rate, short-shipment frequency. Surfaced on the supplier profile and in the ops analytics. No enterprise WMS surfaced this to the operator directly — it lived in buyer reports that a solo operator never saw.

**Repeat order intelligence:** if an operator creates the same manual order for the same items every 2 weeks, Canary offers to add those items to the replenishment system. "You've ordered [item] manually 3 times. Add to Auto-Replenishment?" This is how the system learns from manual behavior and reduces operator work over time.

[[Brain/wiki/cards/store-ops-capability-model]] · [[Brain/wiki/cards/canary-mobile-task-ux-flows]] · [[Brain/wiki/cards/rms-replenishment-screen-flows]] · [[Brain/projects/Canary]]
