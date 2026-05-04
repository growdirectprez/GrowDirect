---
last-compiled: 2026-05-04
needs-review: false
type: reference
status: active
tags: [canary, demand, forecasting, replenishment, analytics, smb, algorithm, functional-requirements]
created: 2026-05-04
---
last-compiled: 2026-05-04
needs-review: false

# Canary — Demand Sensing for SMB

RPAS (Oracle Retail Predictive Application Server) is an extraordinarily powerful demand forecasting platform. It is also completely inappropriate for a $5M retailer. The workbook/worksheet model, the 4-tuple measure taxonomy, the spread method hierarchy, the exception alerting framework — all of it assumes a dedicated planning team that does nothing else all day.

The question for Canary: what does a solo operator actually need from demand sensing? What's the 20% of the capability that delivers 80% of the value — and what can be computed automatically from POS data without any manual parameter maintenance?

This card answers that question and defines Canary's demand sensing architecture.

---
last-compiled: 2026-05-04
needs-review: false

## What the Operator Actually Needs

Three decisions, made repeatedly:

1. **When to reorder** — am I about to run out?
2. **How much to order** — what quantity gets me to the right level without over-buying?
3. **When something has changed** — is this item selling faster than usual? Did something break?

Everything else (store-level forecasting, markdown optimization, range planning) is downstream of getting these three right for every item in the store.

---
last-compiled: 2026-05-04
needs-review: false

## The Velocity Model — Core Primitive

The fundamental input to all three decisions is **velocity**: units sold per day, per item.

```
velocity(item, store, window) = units_sold / days_in_window
```

**Rolling window:** Canary maintains a 56-day (8-week) rolling velocity calculation per item. Why 56 days? Long enough to smooth daily noise; short enough to respond to trend changes within a season. RPAS uses configurable windows from 4 to 52 weeks — SMB needs a sensible fixed default, not a parameter.

**Decay weighting:** more recent sales weighted higher than older sales. A simple exponential decay:

```
weighted_velocity = Σ(units_sold_day_i × decay_factor^(today - day_i))
decay_factor = 0.97  (each day's sales are worth 3% less than the day before)
```

At decay 0.97, sales from 3 weeks ago contribute about 50% of the weight of today's sales. This is not the full RPAS Holt-Winters exponential smoothing — it is directionally correct and computationally trivial.

**Why not a more complex model?** Because it doesn't matter yet. For a 500-SKU store, the difference between a well-tuned Holt-Winters and a decayed rolling average is measured in edge cases. Get the model running first. Upgrade the algorithm later when the operator cares.

---
last-compiled: 2026-05-04
needs-review: false

## From Velocity to Replenishment Parameters

### Min/Max from Velocity

If the operator selects "Auto" replenishment for an item, Canary derives Min and Max from velocity automatically:

```
Lead Time (days):    from supplier profile (COLT — current order lead time)
Review Cycle (days): from supplier profile (how often orders are generated)
Safety Factor:       default 1.5 (operator adjustable: aggressive / balanced / conservative)

Minimum (order point) = velocity × (lead_time + review_cycle/2) × safety_factor
Maximum (order up to) = velocity × (lead_time + review_cycle + ISD)

ISD (Inventory Selling Days) = default 7 (operator sets: 5 / 7 / 10 / 14)
```

**Plain English translation of these numbers:**

- *Minimum* = how much stock you need when you place the order to cover the time until the delivery arrives, with a safety buffer
- *Maximum* = how much you want to have in total after the delivery (enough to last until the next delivery plus a week's comfort)
- *Safety Factor 1.5* = order 50% more than the bare minimum to absorb variability

**Example:**
- Item sells 2 units/day
- Supplier lead time: 3 days
- Review cycle: 7 days
- Safety factor: 1.5
- ISD: 7 days

```
Minimum = 2 × (3 + 3.5) × 1.5 = 19.5 → round to 20 units
Maximum = 2 × (3 + 7 + 7) = 34 units
ROQ = Maximum - current_SOH (if SOH < Minimum)
```

These parameters recalculate automatically as velocity changes. The operator does not touch them unless they want to override.

### When to Escalate to Dynamic Mode

The Min/Max-from-velocity approach works well for stable, steady sellers. It degrades in three scenarios:

1. **High demand variability** — items whose daily sales swing widely (produce, deli, seasonal)
2. **Promotional items** — velocity spikes are predictable but not captured in the rolling average
3. **Perishables** — order-to-serve-to-waste optimization requires a tighter model

For these items, Canary should offer a "Dynamic" mode that exposes the full algorithm (service level %, lost sales factor) once the operator has enough sales history to configure it meaningfully. Gate it behind 8+ weeks of data — otherwise the algorithm has nothing to calibrate against.

---
last-compiled: 2026-05-04
needs-review: false

## Velocity Bands — Classification Without Configuration

Manually categorizing 500 SKUs into velocity tiers is the kind of work that belongs in a planning system and not in the life of a solo operator. Canary should classify automatically:

```
Velocity Band (weekly units sold)
├── A items: > 20 units/week   (high velocity — replenish frequently, tight safety stock)
├── B items: 5–20 units/week   (medium velocity — weekly replenishment)
├── C items: 1–5 units/week    (low velocity — bi-weekly or monthly)
└── D items: < 1 unit/week     (very slow — manual ordering only; flag for ranging review)
```

Bands update monthly as velocity changes. When an item moves bands, Canary notifies the operator: "This item has slowed down — it was selling 12 units/week, now averaging 3. Review your order quantities."

**Band behavior in replenishment:**
- A items: daily SOH check; replenishment task fires immediately when SOH < Minimum
- B items: check on review cycle (e.g., every 7 days)
- C items: check bi-weekly
- D items: manual only; system prompts to deactivate replenishment or flag for ranging review

---
last-compiled: 2026-05-04
needs-review: false

## Seasonality — Lightweight Version

RPAS models seasonality with complex indices updated across planning levels. For SMB, the equivalent is simpler: **year-over-year velocity comparison** for the same week, flagged when the current week diverges from last year.

```
seasonal_signal = this_week_velocity / same_week_last_year_velocity

If > 1.3: item is running hotter than seasonal expectation → raise order quantity suggestion
If < 0.7: item is running cooler → lower order quantity suggestion
If no prior year data: no seasonal adjustment (use rolling 56-day window only)
```

The operator sees this as a nudge, not a parameter: "Sales for [item] are running 40% above last year at this time. Consider increasing your order."

**Promotional flag:** the operator can flag a future week as a promotional event (holiday, sale). Canary applies a promotional lift multiplier to velocity for that window and adjusts the pre-event order quantity accordingly. The multiplier is operator-set (e.g., "I expect 2x normal sales for Thanksgiving week") rather than system-calculated.

---
last-compiled: 2026-05-04
needs-review: false

## Exception Detection — What Broke?

The most valuable daily output of a demand sensing system is not the forecast — it's the exception list. What changed since yesterday that needs attention?

**Exception types Canary monitors:**

| Exception | Signal | Action |
|---|---|---|
| **SOH approaching zero** | Current SOH < 2 days of velocity | Urgent replenishment alert |
| **SOH at zero** | SOH = 0, item still active | Stockout alert; affects fill rate metric |
| **Velocity spike** | This week's velocity > 2× prior 4-week average | "Selling fast" alert — check if order is en route |
| **Velocity drop** | This week's velocity < 0.3× prior 4-week average | "Slow mover" alert — check for quality issue, expired stock, pricing |
| **Receiving anomaly** | Ordered 48, received 36 — same pattern 3+ cycles | Supplier fill rate issue — flag for PO review |
| **Stale inventory** | Item in back-stock with no movement for 30+ days | Storage cost accumulating — review for markdown or return |
| **High variance item** | Day-to-day sales swing > 3× the average | Min/Max is unreliable for this item; suggest Dynamic mode |

The exception list is the operator's morning briefing. Not a report — a prioritized action queue. Each exception has one next action: reorder / investigate / mark down / call supplier.

---
last-compiled: 2026-05-04
needs-review: false

## The SOH Accuracy Problem — And Why It Matters

Every calculation above depends on SOH being accurate. If Canary's SOH is wrong, every recommendation is wrong.

SOH accuracy erodes from:
1. **Theft / shrinkage** — items leaving the store without a POS scan
2. **Receiving errors** — cases counted wrong or not scanned at all
3. **Return processing** — customer returns not recorded in Canary
4. **Damage disposal** — associate throws away broken items without adjusting inventory
5. **Scan errors at POS** — wrong item scanned at register

**Canary's SOH defense mechanisms:**

| Problem | Defense |
|---|---|
| Shrinkage | Cycle counts surface discrepancies; shrinkage reason code builds a pattern over time |
| Receiving errors | Required scan confirmation per case (can't skip without flagging) |
| Unreturned returns | Return flow in POS must trigger Canary SOH event |
| Damage disposal | Damage flag in receiving + damage adjustment task in the task queue |
| POS scan errors | POS → Canary event includes item verification; Canary flags when a single transaction deducts an implausible quantity |

**Ghost inventory problem:** SOH shows units, but they're not there. Typically caused by shrinkage. Canary detects: item has SOH > 0 but velocity has dropped to near zero and no replenishment has been triggered. Could be ghost inventory — flag for cycle count.

**Negative SOH:** should not be possible if Canary is the authoritative SOH system. If POS sends a sale event that would drive SOH negative, Canary logs it as an anomaly, adjusts SOH to zero, and flags for investigation. The anomaly may indicate a POS scan error or an unrecorded receiving event.

---
last-compiled: 2026-05-04
needs-review: false

## From Velocity to Margin Intelligence

Once velocity is accurate, Canary can compute gross contribution per item — not just margin on paper but actual in-store margin after ops cost:

```
Gross margin per unit = selling price - unit cost
Ops cost per unit = sum of activity costs associated with that item
  (receiving cost + storage cost + replenishment cost + cycle count allocation)

Net contribution per unit = gross margin - ops cost
```

This is the cost-to-serve model from RDM V9's activity cost metrics, denominated in satoshis for the blockchain ledger, but shown to the operator in dollars.

**Actionable output:** items sorted by net contribution per unit. The bottom of the list are items that are costing more to handle than they generate. Some of those are range candidates for removal — not because they sell slowly, but because they cost too much to service relative to what they generate.

**The "loss leader audit":** some items intentionally generate low margin (or even a loss) because they drive traffic. Canary should let the operator flag items as intentional loss leaders — excluded from the "low contribution" exception list but tracked separately as traffic drivers.

---
last-compiled: 2026-05-04
needs-review: false

## What Canary Is Not Building (Yet)

These enterprise capabilities are out of scope for the SMB tier:

| Out of scope | Why |
|---|---|
| Hierarchical forecasting (store → district → chain) | Single-store operator has no hierarchy |
| Markdown optimization | Requires pricing authority and competitive data feeds |
| Assortment optimization (range planning) | Complex — deferred to a later module |
| Collaborative planning with supplier (CPFR) | Requires supplier integration infrastructure not yet built |
| Demographic demand modeling | Data not available at SMB level |

The above are Phase 3+ capabilities. They require either multi-store operators (who have enough scale to justify the complexity) or the aggregated network data that accumulates once Canary has a meaningful merchant base.

---
last-compiled: 2026-05-04
needs-review: false

## Algorithm Transparency — Show the Math

RPAS showed operators results, not reasoning. "System recommends 48 units" — no further explanation. Operators learned to distrust recommendations they couldn't verify, and override rates were high.

Canary's approach: every recommendation shows the inputs.

```
Recommended Order: 36 units

How we got there:
  Velocity:     3.2 units/day (56-day weighted average)
  Lead time:    3 days (from [Supplier] profile)
  Review cycle: 7 days
  Safety:       1.5× (Balanced)

  Minimum: 3.2 × (3 + 3.5) × 1.5 = 31 units
  Current SOH: 8 units → below minimum
  Max: 3.2 × (3 + 7 + 7) = 54 units
  Order to reach Max: 54 - 8 = 46 → rounded to 36 (3 cases of 12)

[ Adjust ]  [ Accept ]
```

This is the "algorithm transparency" gap that RMS explicitly did not fill. Canary fills it. When the operator understands why the recommendation is 36 units, they either trust it (and accept) or they have the information to disagree intelligently (and adjust). Over time, their adjustments become the signal for tuning the algorithm.

[[Brain/wiki/cards/store-ops-capability-model]] · [[Brain/wiki/cards/canary-purchase-order-lifecycle]] · [[Brain/wiki/cards/rpas-planning-paradigm]] · [[Brain/projects/Canary]]
