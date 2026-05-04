---
last-compiled: 2026-05-04
needs-review: false
type: reference
status: active
tags: [canary, operations-hub, dashboard, morning-briefing, exceptions, mobile, tablet, functional-requirements]
created: 2026-05-04
---
last-compiled: 2026-05-04
needs-review: false

# Canary — Operations Hub

The Operations Hub is the owner-operator's daily control surface. It is the first screen they see when they open Canary. It answers: what needs my attention right now, what is happening in my store, and are we on track today?

Every enterprise WMS had a version of this — RDM called it the Visibility Workbench; ORMS had the buyer worksheet queue; RPAS had the exception alert dashboard. All of them assumed a dedicated operations team monitoring multiple screens all day. The SMB translation: one person, one screen, a few minutes in the morning and a periodic check during the day.

The design principle: surface the most urgent thing first, then give enough context to decide without digging. The operator should be able to do a meaningful morning review in under 3 minutes.

---
last-compiled: 2026-05-04
needs-review: false

## The Owner-Operator's Morning Questions

In order of urgency:

1. **What went wrong overnight?** — stockouts, failed deliveries, system anomalies
2. **What's arriving today?** — expected deliveries, what's on order, what needs to be ready
3. **What do I need to order today?** — orders due before the review cycle closes
4. **How did yesterday go?** — sales vs. expectation, top movers, slow movers
5. **What does my team need to do today?** — task queue, replenishment plan, receiving assignments
6. **Is anything trending badly?** — items approaching stockout, suppliers with fill-rate issues

The Operations Hub is structured around these questions, in this order.

---
last-compiled: 2026-05-04
needs-review: false

## Hub Layout — Tablet (Primary Surface)

```
┌─────────────────────────────────────────────────────────────────┐
│  Good morning, [Store Name]          Mon May 4  │  8:14 AM      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ⚠ NEEDS ATTENTION (3)                                           │
│  ─────────────────────────────────────────────────────           │
│  🔴 Stockout: [Item A] — 0 units, no order pending              │
│  🟡 Delivery missed: [Supplier B] expected yesterday            │
│  🟡 Proposed order ready for review: [Supplier C] — $847        │
│                                                                   │
│  ─────────────────────────────────────────────────────           │
│  TODAY                                                            │
│  📦 Deliveries expected: 2 (Supplier D ~10am, Supplier E ~2pm)  │
│  📋 Tasks in queue: 14 (8 replenishments, 4 receiving prep, 2 ↗) │
│  📬 Orders due to submit: 1 (Supplier F — closes at noon)        │
│                                                                   │
│  ─────────────────────────────────────────────────────           │
│  YESTERDAY                                                        │
│  💰 Sales: $3,241  (▲ 8% vs same day last week)                 │
│  📦 Units sold: 847  │  Items with 0 sales: 23                  │
│  🏆 Top mover: [Item G] — 42 units                               │
│  🐌 Slow: [Item H] — 0 sales, 18 days straight                  │
│                                                                   │
│  ─────────────────────────────────────────────────────           │
│  WATCH LIST (5 items trending toward stockout)                   │
│  [Item J] 3 days left │ [Item K] 2 days left │ [+ 3 more]       │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

Every line is tappable. Tapping a stockout alert opens that item's detail. Tapping "Orders due to submit" opens the PO for review. Tapping "Tasks in queue" opens the task dashboard. The Hub is a summary surface; everything behind it is one tap away.

---
last-compiled: 2026-05-04
needs-review: false

## Hub Layout — Phone (Associate / On-the-Floor View)

Phone view collapses to task-first — the associate's job is executing tasks, not reviewing analytics:

```
┌─────────────────────────────┐
│  Canary                     │
│                  Mon 8:14am │
├─────────────────────────────┤
│  MY TASKS (3)               │
│  ─────────────────────────  │
│  📦 Replenish: Aisle 4 Shelf B     │
│  📦 Replenish: Aisle 2 Shelf A     │
│  📋 Receiving: Supplier D ~10am    │
├─────────────────────────────┤
│  ALERTS (1)                 │
│  🔴 Stockout: [Item A]      │
│     Notify manager?  [Yes]  │
├─────────────────────────────┤
│  [ Full Store View ]        │
└─────────────────────────────┘
```

The associate sees their task queue and any alerts that require a human response. "Notify manager?" is a one-tap escalation — the alert goes to the owner's Hub immediately.

---
last-compiled: 2026-05-04
needs-review: false

## Attention Queue — Exception Classification

The Hub's "Needs Attention" list is prioritized by severity and time-sensitivity:

| Priority | Condition | Why it matters |
|---|---|---|
| 🔴 Critical | Stockout — item at zero SOH, no order pending | Revenue loss happening now |
| 🔴 Critical | Receiving task overdue — delivery arrived, not processed | SOH won't update; floor may run out |
| 🟡 High | Proposed order ready — review window closing | Miss it and the order doesn't go this cycle |
| 🟡 High | Delivery expected but supplier hasn't confirmed | Risk of no-show; associate prep may be wasted |
| 🟡 High | Item below display minimum — replenishment not yet complete | SOH low but not zero; risk of stockout today |
| 🔵 Info | Velocity spike on item — selling faster than normal | May need an emergency order; worth checking |
| 🔵 Info | Supplier performance flag — 3rd short shipment in a row | Pattern, not a crisis; worth noting |
| 🔵 Info | Trial item approaching 8-week review | Range decision due; no urgency |

Critical items appear with an alert badge on the app icon. Info items do not push notifications — they surface when the operator opens the Hub.

**Attention queue resolution:** tapping an item either resolves it directly (one-tap "order now" for a stockout) or navigates to a detail screen where action can be taken. Once resolved, the item drops off the queue. The queue should never grow unboundedly — if the operator ignores a critical alert for 48 hours, it escalates (notification, not just Hub display).

---
last-compiled: 2026-05-04
needs-review: false

## Today's Deliveries — Receiving Prep

The Hub shows every delivery expected today with status:

```
TODAY'S DELIVERIES

  📦 Supplier D — expected 8am–noon
     PO #12847 | 14 items | 48 cases | $1,847
     Status: In Transit (confirmed yesterday)
     Associate: [Name assigned / Unassigned]

  📦 Supplier E — expected 2pm–4pm
     PO #12851 | 6 items | 12 cases | $620
     Status: Unconfirmed (no ASN received)
     ⚠ Call to confirm?  [Call]  [Mark as confirmed]
```

One tap assigns an associate to receive the delivery. One tap calls the supplier. One tap starts the receiving flow when the truck arrives.

**Unconfirmed deliveries** are flagged — the operator hasn't heard from the supplier that the order is coming. Canary doesn't know if it will arrive. The flag reminds the operator to confirm before dispatching a receiving team to wait.

---
last-compiled: 2026-05-04
needs-review: false

## Yesterday's Performance — Daily Sales Summary

This is the SMB equivalent of the morning P&L review. For a solo operator, it replaces pulling a report from the POS back-office.

```
YESTERDAY — Sunday, May 3

Revenue:          $3,241    (▲ 8.2% vs last Sunday)
Transactions:        187    (avg $17.33)
Units sold:          847

Top 5 movers:
  1. [Item A]     42 units   ($189)
  2. [Item B]     38 units   ($152)
  3. [Item C]     31 units   ($124)
  4. [Item D]     28 units   ($112)
  5. [Item E]     24 units   ($96)

Items with no sales:   23   [ View list ]
Items below minimum:    8   [ View + replenish ]

Shrinkage/adjustments:  -$42 (2 damaged units logged)
```

"Items with no sales" is a ranging signal — 23 items sat on the shelf all day and sold nothing. Over time, this list drives Phase-Out decisions. "Items below minimum" is an operational flag — the replenishment system should have already fired tasks, but this confirms what's outstanding.

**Comparison cadence:** the Hub defaults to comparing yesterday to the same day last week (Sunday vs. Sunday). This accounts for day-of-week patterns without requiring sophisticated modeling. A simple and correct comparison.

---
last-compiled: 2026-05-04
needs-review: false

## Watch List — Predictive Stockout Alert

Items approaching stockout before the next expected delivery:

```
WATCH LIST — approaching stockout

  [Item J]   3 days of stock remaining | Next delivery: Friday
               → Will stock out 1 day before delivery
               [ Emergency order ]   [ Adjust minimum ]

  [Item K]   2 days of stock remaining | Next delivery: Thursday
               → Will barely make it. Consider topping up.
               [ Emergency order ]   [ Monitor ]

  [Item L]   5 days | Next delivery: Wednesday → OK
  [Item M]   4 days | Next delivery: Tuesday → OK
  [Item N]   6 days | Next delivery: Saturday → Borderline
```

The calculation: current SOH ÷ velocity = days remaining. Compare against next expected delivery date. If the math says the item runs out before the delivery, it surfaces on the Watch List with the shortfall visible.

"Emergency order" initiates a manual PO to the supplier outside the normal review cycle. "Adjust minimum" increases the display minimum so the replenishment algorithm is more aggressive next cycle.

This is the most operationally valuable prediction Canary makes. An operator who catches a Watch List item on Monday morning can place a supplemental order before the problem becomes a Monday afternoon stockout.

---
last-compiled: 2026-05-04
needs-review: false

## Task Dashboard — Shift Ops View

From the Hub, one tap opens the full task dashboard — the supervisor's view of what's happening on the floor:

```
TASK DASHBOARD — Monday May 4

Shift started: 8:00am | 3 associates on floor

QUEUE DEPTH
  Replenishments:  8  tasks  (est. 2.5 hrs)
  Receiving:       4  tasks  (delivery ~10am)
  Cycle counts:    0  tasks  (next scheduled: Thursday)
  Other:           2  tasks

IN PROGRESS
  [Name 1]  → Replenishment | Aisle 3 Shelf C | started 8:18am
  [Name 2]  → Unassigned
  [Name 3]  → Unassigned

COMPLETED TODAY
  3 tasks (2 replenishments, 1 receiving prep)

EXCEPTIONS
  [Name 1] flagged: Aisle 3 Shelf C — shelf damaged, needs attention
```

The supervisor can see instantly that 2 associates are unassigned, 8 replenishment tasks are waiting, and there's a flagged shelf issue. From this screen they can assign tasks, look at the flagged exception, and adjust priorities.

**Auto-assignment:** if enabled, Canary distributes the task queue automatically across available associates at shift start. The supervisor reviews the plan and adjusts if needed. Manual assignment is always available.

---
last-compiled: 2026-05-04
needs-review: false

## Analytics vs. Alerting — What Belongs on the Hub

**On the Hub:**
- Anything requiring a decision within the next 4 hours
- Any deviation from normal that is material (8% sales lift is notable; 2% is noise)
- Any operational task with a time-sensitivity (order window closing, delivery arriving)

**Not on the Hub (in the analytics section instead):**
- Trend data (week over week, month over month)
- Supplier scorecards
- Margin analysis by item
- Replenishment efficiency metrics
- Range performance by category

The Hub is the morning briefing, not the monthly review. The monthly review lives in a dedicated Analytics section accessed from the nav — not the home screen.

---
last-compiled: 2026-05-04
needs-review: false

## Home Screen vs. App Nav

The Hub is the home screen. The nav provides access to all modules:

```
Bottom nav (phone) / Left sidebar (tablet):

  🏠 Hub            — Morning briefing + exception queue
  📦 Inventory      — Item list, SOH by item, location map
  📋 Tasks          — Task queue, shift dashboard
  🚚 Orders         — PO lifecycle, supplier list
  🗂 Planogram      — Space + range + display
  📊 Analytics      — Performance, trends, supplier scorecard
  ⚙ Settings       — Store config, supplier setup, user management
```

Eight destinations. Every major capability reachable in two taps from anywhere in the app.

---
last-compiled: 2026-05-04
needs-review: false

## The Canary Hub vs. The POS Back-Office

Most POS systems (NCR Counterpoint, Clover, Square) have a back-office reporting module. It is where operators currently get sales data and limited inventory information. The Canary Hub replaces the workflow of checking the POS back-office for operational status — but it does not replace the POS back-office for accounting, tax, and financial reporting. Those stay in the POS. Canary owns operations; the POS owns the transaction of record.

The division: POS back-office = financial transactions. Canary Hub = operational status and decisions. Both are necessary. They show different things. Operators should not have to choose.

[[Brain/wiki/cards/store-ops-capability-model]] · [[Brain/wiki/cards/canary-mobile-task-ux-flows]] · [[Brain/wiki/cards/canary-demand-sensing-smb]] · [[Brain/projects/Canary]]
