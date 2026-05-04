---
last-compiled: 2026-05-04
needs-review: false
type: reference
status: active
tags: [canary, supplier, ordering, onboarding, wizard, functional-requirements, mobile]
created: 2026-05-04
---
last-compiled: 2026-05-04
needs-review: false

# Canary — Supplier Profile & Ordering Setup

The supplier profile is the operational contract between the store and a vendor. It drives everything downstream: when orders are generated, how they're transmitted, what quantities are acceptable, when deliveries arrive. Getting this right at setup eliminates the most common replenishment errors — orders placed to the wrong schedule, quantities below supplier minimums, deliveries that arrive on days the store is closed.

ORMS (Oracle RMS) solved this with the SIM (Supplier Inventory Management) configuration — a dense form with 15+ fields across multiple screens. The functional requirements are correct. The UX was designed for a buyer at a desktop who configures suppliers once and forgets. Canary's version is a mobile-first wizard that an owner-operator can complete in 4 minutes, with sensible defaults pre-populated.

---
last-compiled: 2026-05-04
needs-review: false

## Supplier Profile — Complete Field Set

Every field listed here has a purpose. No decorative fields.

### Identity

| Field | Purpose |
|---|---|
| Supplier name | Display everywhere |
| Supplier code | Optional internal code; defaults to a Canary-assigned ID |
| Account number | The store's account number with this supplier (for PO transmission) |
| Sales rep name + phone | Shown on the supplier profile; used when the operator needs to call |
| Transmission method | How orders are sent: EDI / email / supplier portal URL / text / phone |

### Ordering Parameters

| Field | Purpose | Default |
|---|---|---|
| Order Control | Auto / Review / Manual | Review |
| Review Cycle | How often orders are generated | Weekly |
| Review Day | Day(s) of week the system proposes orders | Sunday |
| Lead Time — current (COLT) | Days from order submission to delivery for the current order | Required |
| Lead Time — next cycle (NOLT) | Lead time to use when calculating the NEXT order | = COLT |
| Order Minimum | Minimum dollar value or case count required by supplier | None |
| Order Minimum Action | What to do when below minimum: Hold / Accept / Skip | Hold |

**COLT vs. NOLT distinction (from ORMS):** current order lead time is how long this specific delivery will take. The next order lead time is what the system assumes for the NEXT replenishment calculation. Usually the same — but promotions and seasonal supply constraints can make them different. Exposing both is the right model. For v1, default NOLT = COLT and let the operator override when needed.

### Delivery Schedule

| Field | Purpose |
|---|---|
| Delivery days | Which days of the week supplier delivers |
| Delivery window | Approximate arrival time (e.g., "mornings," "8am–noon") |
| Dock / receiving area | Which entrance deliveries arrive at (relevant for multi-door stores) |

**Delivery schedule drives "Not Before Date" calculation.** If the supplier delivers on Tuesdays and Thursdays, and today is Monday with a 2-day lead time, the system sets Not Before Date = Wednesday (not Tuesday, since Tuesday won't work for a 2-day lead time from Monday). This prevents orders that can't be received on the expected delivery day.

### Case Pack & Rounding

| Field | Purpose | Default |
|---|---|---|
| Default rounding | Round order quantities to: case / none | Case |
| Inner pack size | Units per inner (sub-case pack) | Optional |
| Case pack size | Units per case (overridden per item if item has its own case size) | Required |

**Rounding logic:** when the system calculates an ROQ of 47 units and the case pack is 12, the rounding rule determines the output. "Round to case" → 48 units (4 full cases). "No rounding" → 47 units (3 cases + 11 loose, which the supplier may not accept). For most suppliers, "Round to case" is correct.

### Order Constraints

| Field | Purpose |
|---|---|
| Order maximum (dollar) | If the store has a budget constraint per supplier per cycle |
| Truck size / pallet limit | Maximum order size before the supplier splits into multiple deliveries |
| Pallet minimum | Some suppliers require a minimum pallet count (common in produce wholesale) |

**Supplier splitting (truck split from ORMS):** if an order exceeds the supplier's truck capacity, it should be flagged for the operator. "This order is 6 pallets — [Supplier] typically delivers a maximum of 4. Do you want to split across two deliveries?" The operator decides; Canary does not auto-split (that's too opaque for SMB).

---
last-compiled: 2026-05-04
needs-review: false

## Supplier Setup Wizard — UX Flow

A 5-step wizard. Operator can save and return at any point. Progress persists.

---
last-compiled: 2026-05-04
needs-review: false

**Step 1 — Supplier Identity (30 seconds)**

```
Add Supplier

Supplier Name:    [ _________________ ]
Account #:        [ _________________ ]   (optional)
Sales Rep:        [ Name ]  [ Phone ]

How do you usually order from them?
  ○ Send them an email
  ○ Their website / portal
  ○ EDI (automatic)
  ○ Phone or text

[ Next ]
```

---
last-compiled: 2026-05-04
needs-review: false

**Step 2 — Ordering Schedule**

```
How often do you order from [Supplier]?

  ○ Daily
  ● Weekly
  ○ Bi-weekly
  ○ Monthly
  ○ On demand

Which day should we propose your order?
  [ Sun ▼ ]

When you place an order, how many days until delivery arrives?
  [ 2 ] days

[ Next ]
```

---
last-compiled: 2026-05-04
needs-review: false

**Step 3 — Delivery Days**

```
Which days does [Supplier] deliver to you?

  ☐ Mon   ☐ Tue   ● Wed   ☐ Thu   ● Fri   ☐ Sat   ☐ Sun

What time do they typically arrive?
  [ Morning (8am–noon) ▼ ]

[ Next ]
```

---
last-compiled: 2026-05-04
needs-review: false

**Step 4 — Minimums & Case Packs**

```
Does [Supplier] have a minimum order?

  ○ No minimum
  ● Dollar minimum:  $ [ 250 ]
  ○ Case minimum:    [ ___ ] cases

If my order is below the minimum:
  ● Hold it and remind me to add more
  ○ Send it anyway
  ○ Skip this cycle and try next time

Default case pack size: [ 12 ] units per case
(You can override this per item)

[ Next ]
```

---
last-compiled: 2026-05-04
needs-review: false

**Step 5 — Order Control**

```
How would you like to manage orders with [Supplier]?

  ○ I'll create orders myself (Manual)

  ● Suggest orders for me to review (Review)
      "Canary proposes based on your stock levels. You approve before it's sent."

  ○ Send automatically when stock is low (Auto)
      "Canary orders without review. Best for trusted suppliers with reliable fill rates."

[ Save Supplier ]
```

---
last-compiled: 2026-05-04
needs-review: false

**Confirmation Screen**

```
✓ [Supplier Name] is set up

Orders proposed: Sundays
Deliveries: Wednesdays and Fridays
Mode: Review (you approve before sending)

Next: add items from this supplier →
      [ Go to Items ]   [ Done ]
```

If the operator taps "Go to Items," they're taken to a filtered item list showing items without a supplier assignment — they can bulk-assign items to this supplier. This seeds the replenishment system.

---
last-compiled: 2026-05-04
needs-review: false

## Item-Supplier Linking

Each item in Canary is linked to a primary supplier and optionally one or more alternate suppliers. This drives:
- Which supplier PO the item appears on during the review cycle
- Which lead time and delivery schedule applies
- Which case pack size is used for rounding

**Bulk linking:** after adding a supplier, the operator can select multiple items and assign them to the supplier in one action. This is especially useful when adding a new category supplier (e.g., a new produce wholesaler) who supplies 30+ SKUs at once.

**Alternate supplier:** if an item can be sourced from two suppliers (a primary and a backup), the operator can designate both. The system always proposes from the primary. If the operator switches the order to the alternate (e.g., primary is out of stock), the lead time and case pack from the alternate supplier profile are used for that order.

---
last-compiled: 2026-05-04
needs-review: false

## Supplier Performance — Automatic Tracking

Every completed PO generates a receiving record. Canary accumulates these into a supplier scorecard:

```
Supplier Scorecard — [Supplier Name]
Last 90 days (12 deliveries)

On-time delivery:     10 / 12  (83%)
Fill rate:            94.2%    (ordered 1,440 units, received 1,356)
Short shipments:       4 events (avg: -2.3 cases)
Wrong items:           1 event

Cost per delivery:    $1,847 avg
```

This is surfaced on the supplier profile. No dashboard needed — it's on the supplier card. The operator can see at a glance that a supplier has a 20% late delivery rate and decide whether to adjust lead time assumptions or switch to an alternate.

**Lead time auto-calibration:** if the supplier consistently delivers in 2 days but the operator has 3 days configured, Canary suggests adjusting the lead time: "Actual delivery has averaged 1.8 days over the last 12 orders. Adjust lead time to 2 days?" Accepting the change immediately affects all replenishment calculations for that supplier's items.

---
last-compiled: 2026-05-04
needs-review: false

## Transmission — How Orders Actually Get Sent

| Method | What Canary does |
|---|---|
| Email | Generates a formatted PO and attaches as PDF; opens email compose with supplier email pre-filled |
| Supplier portal | Opens the portal URL in browser; Canary has generated the order for manual entry (copy-paste assist) |
| EDI | Transmits the 850 Purchase Order transaction set directly; updates PO status to Submitted on acknowledgment |
| Phone / text | Generates a summary view the operator reads from; logs the order as submitted when operator marks "called in" |

For v1, email and portal cover the vast majority of SMB suppliers. EDI is a later-stage capability — it requires a trading partner agreement and EDI mapping work per supplier. Phone/text fallback handles the occasional local supplier with no digital ordering.

---
last-compiled: 2026-05-04
needs-review: false

## What This Unlocks

The supplier profile is the control plane for replenishment. Without it, the demand sensing algorithms have no lead time to work with, no delivery schedule to calculate against, and no transmission method to use. The supplier wizard is not an onboarding step — it's the prerequisite for the entire replenishment system.

An operator who configures 5 suppliers in the first session has effectively activated the entire replenishment engine. Canary can start generating proposed orders on the next review cycle.

[[Brain/wiki/cards/store-ops-capability-model]] · [[Brain/wiki/cards/canary-demand-sensing-smb]] · [[Brain/wiki/cards/canary-purchase-order-lifecycle]] · [[Brain/projects/Canary]]
