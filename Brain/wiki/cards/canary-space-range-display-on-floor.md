---
last-compiled: 2026-05-04
needs-review: false
type: reference
status: active
tags: [canary, space, range, display, planogram, assortment, mobile, android-pos, functional-requirements]
created: 2026-05-04
---
last-compiled: 2026-05-04
needs-review: false

# Canary — Space, Range & Display: On the Floor

Space, Range, and Display (SRD) has been a back-office discipline since the first planogram software appeared in the 1980s. JDA (now Blue Yonder) built the dominant platform — used by Tesco, Walmart, Kroger, and virtually every major retailer. The workflow: category managers design planograms at HQ workstations, planograms are exported nightly, stores receive PDFs, associates implement from printed maps, performance data feeds back weekly, category managers review quarterly. The latency in that loop is measured in weeks.

Canary moves SRD to the floor. The planogram is on the associate's device. Performance is live from the POS. Range decisions happen at the shelf, not at a desk three thousand miles away. This is not a feature addition — it's a structural collapse of what used to be a separate organizational function.

---
last-compiled: 2026-05-04
needs-review: false

## The JDA Data Model — What Was Right

JDA Intactix got the data model right. Everything else was wrong (batch, back-office, desktop). The model:

```
Store
└── Floorplan (the store's shelf layout — which planograms go where)
    └── Planogram (a shelf-section layout — product positions within a fixture)
        └── Segment / Module (a column of the planogram, left to right)
            └── Fixture / Shelf (a horizontal level, bottom to top)
                └── Position (a product slot, left to right within the shelf)
                    └── Product (SKU, facings, merchandising style, facing width)
```

Performance data at four levels:
- Product performance (velocity by item)
- Product × Planogram performance (velocity for this item in this planogram)
- Planogram performance (total velocity across all items in the planogram)
- Planogram × Store performance (total velocity for this planogram in this store)

This hierarchy is correct and should be preserved in Canary. The data model is sound. The delivery mechanism — nightly batch exports, integration layer holding tables, weekly feeds — is what Canary replaces.

---
last-compiled: 2026-05-04
needs-review: false

## The Three Domains: Space, Range, Display

These are distinct capabilities that traditional SRD systems bundled together at HQ. Canary separates them by audience:

| Domain | What it decides | Traditional audience | Canary audience |
|---|---|---|---|
| **Range** | Which items are stocked in which stores | Category managers at HQ | Owner-operator, assisted by Canary |
| **Space** | How much shelf space each item gets; where it's located | Space planners at HQ | Canary suggests; operator decides |
| **Display** | How items are physically presented on the shelf | Category managers + visual merchandisers | Associate, guided by mobile planogram |

For a Main Street SMB operator, these three decisions are made by the same person — usually the owner — without dedicated tools, and usually based on gut feel, habit, or what the sales rep recommends. Canary provides the data layer and the workflow for all three without requiring a planning department.

---
last-compiled: 2026-05-04
needs-review: false

## Capability 1: Range Management — What's In the Store

**Range** = the set of items stocked in a given store. Enterprise range management involves elaborate ranging controls: items are ranged or de-ranged by planogram version, by store format, by region, by event calendar. JDA Intactix tracked "Range In Progress" (RIP) — items being evaluated for inclusion.

**Canary's Range Model:**

Every item in Canary has a range status:

```
Range Status
├── Active — on the shelf, being replenished
├── On Trial — recently added, being evaluated (velocity tracked, not yet committed)
├── Seasonal — active only during a defined date window
├── Phase-Out — deactivating; no new orders generated; existing stock sells down
└── Inactive — not carried; visible in catalog but not in replenishment
```

**How range decisions are triggered:**

The operator doesn't need to think about "range management" as a concept. They get surfaced nudges:

| Signal | Canary nudge |
|---|---|
| Item below 0.5 units/week for 6+ weeks | "This item hasn't been selling. Consider removing or marking down." |
| Item at zero SOH with no pending order | "You're out of [item] — reorder or deactivate?" |
| Trial item after 8 weeks | "[Item] trial complete — keep, phase out, or convert to seasonal?" |
| Sales rep proposes new item | "Add [New Item] to trial range?" → starts On Trial status |
| Seasonal window approaching | "Time to activate [seasonal item]. Set up order?" |

**Range decisions have immediate operational consequences:** changing an item to Phase-Out stops new orders from being generated and stops replenishment tasks from firing. The space freed becomes available for a replacement item. The inventory on hand sells through without additional orders until SOH reaches zero.

**New item induction (from SRD Service Induction process):** when an operator adds a new item to the range, Canary walks through a structured induction:

```
1. Item identity (scan barcode → auto-fill from product database if available)
2. Supplier assignment + first order
3. Floor location + display minimum
4. Replenishment method selection (Trial status defaults to Min/Max)
5. First delivery confirmation (item goes Active when first received)
```

Until step 5, the item is pending — no floor location, no replenishment trigger, no POS item master sync. The induction flow ensures items don't hit the system half-configured.

---
last-compiled: 2026-05-04
needs-review: false

## Capability 2: Space Allocation — How Much Shelf the Item Gets

**Facings** = the number of units of an item visible from the aisle (the number of product "faces" on the shelf). More facings = more visual presence = higher probability of purchase. The space planning question: which items get more facings, and which get fewer?

In JDA, space allocation is calculated by comparing an item's velocity (Av_Wkly_Unit_Mvmt) against its shelf facing width and capacity, and adjusting to maximize velocity per linear foot. This is the core algorithm of every space planning system.

**Canary's space model:**

Every item has:
- **Display minimum**: fewest units that should be visible at any time (the "floor" — if below this, replenishment fires)
- **Display maximum**: most units that fit in the designated space (the "ceiling" — the shelf capacity)
- **Facing count**: how many product faces are shown (affects how visible the product is)
- **Shelf location**: zone + aisle + shelf level + position

**Space optimization nudges:**

| Condition | Canary suggestion |
|---|---|
| Item at maximum velocity, constantly triggering replenishment | "Consider adding a facing for [item] — it's selling faster than its space supports." |
| Item's space has been empty > 20% of observations | "This shelf often sits empty between replenishments. Reduce facing count or increase display min." |
| Two adjacent items with very different velocities | "Consider swapping [slow item] and [fast item] — the fast item would benefit from [location]." |
| Item velocity dropped after location change | "Sales on [item] dropped 30% after the last shelf move. Consider returning to previous location." |

These nudges are suggestions, not commands. The operator makes the decision. Canary tracks what happened before and after location changes so the learning compounds.

---
last-compiled: 2026-05-04
needs-review: false

## Capability 3: Display — The Shelf as a Mobile-Guided Experience

This is the most direct departure from the JDA model. JDA produced planograms as static outputs — PDF maps, printed sheets, and (in the Tesco implementation) shelf-edge label extracts that required a nightly batch to stay current.

**Canary's planogram is live and on-device.**

**For the associate implementing a reset or new planogram:**

```
Planogram View (tablet, landscape)

Store | Aisle 4 | Section: Coffee & Tea

[Visual shelf diagram — top to bottom, left to right]
  Position 1A: [Item A] — 2 facings
  Position 1B: [Item B] — 3 facings
  Position 2A: [Item C] — 2 facings
  ...

  [Tap any item for: current SOH / velocity / facing recommendation]

[ Implement This Planogram ]
   Tap to start step-by-step guided reset
```

**Guided reset flow:** the app walks the associate through the reset position by position. "Move [Item A] to Position 1A. Scan item to confirm." Scan confirmation generates an implementation event — the planogram goes from "pending" to "implemented" with a timestamp. No more "was the planogram actually implemented?" mystery.

**Live performance overlay:** after implementation, the same planogram view shows performance:

```
Position 1A: [Item A]  ●●●○○  3.2 units/week  [Above average]
Position 1B: [Item B]  ●●○○○  1.8 units/week  [Below average — flag?]
```

The color coding is immediate feedback. A visual merchandiser walking the aisle with a tablet sees at a glance which positions are performing and which are dead spots.

**Shelf-edge label generation:** when a planogram is implemented or modified, Canary can generate shelf-edge labels (price + item description + barcode) for any positions that changed. Labels print to a connected label printer (Bluetooth, typical in small retail). No nightly extract. No waiting for a batch job. The associate changes the planogram → prints the label → done.

---
last-compiled: 2026-05-04
needs-review: false

## Capability 4: Point-of-Purchase SRD Integration

This is the insight the user named: SRD needs to be at the point of purchase, not just back office.

**What "at point of purchase" means in practice:**

**Android POS — associate lookup:**
When a customer asks "where is [item]?" the associate's POS or handheld shows:
```
[Item] — Zone C / Aisle 4 / Shelf B / Position 3
2 units in stock | Last replenished 2 hours ago
```
This requires the planogram data to be live in the POS, not exported nightly. The product-store-planogram map (what JDA computed each night for shelf-edge labelling) becomes a real-time query in Canary. The question "where is this item?" is answered from the same data that drives replenishment.

**Android POS — planogram compliance at ring:**
When an item is scanned at the register, the POS can flag if the item's planogram position is unexpected — e.g., the item scanned was supposed to be in a different location. Not a hard stop — just a signal. Over time, these flags identify merchandising drift: items that were moved from their planogram position and never moved back.

**Android POS — customer-facing display:**
At a kiosk or customer-facing tablet in a store, the shopper can search for an item and see its aisle and shelf position. The store map is a direct output of the Canary planogram — no separate "store wayfinding" system required.

**BOPIS / e-comm integration:**
When an online order is received, the pick task generated by Canary includes the planogram location: "Go to Aisle 4, Shelf B, Position 3 — pick 2 units of [item]." The picker follows the planogram, not a memory of where things are. This only works if the planogram is live, current, and on-device.

---
last-compiled: 2026-05-04
needs-review: false

## The Data Loop — Closing the Back-Office Lag

JDA's SRD loop had a latency problem:

```
JDA: planogram designed (week 1)
    → Object Lifecycle approval (week 2–3)
        → Nightly export to store (week 3)
            → Store implements from printed map (week 3–4)
                → Sales data feeds back weekly
                    → Performance review by category manager (week 8–12)
                        → Range/space decision
                            → Planogram revised (week 12+)
```

Total loop: 3–12 weeks from design to performance feedback.

**Canary's loop:**

```
Canary: planogram change proposed (Day 1)
    → Operator approves on mobile (Day 1)
        → Guided implementation by associate (Day 1)
            → POS sales start contributing velocity immediately
                → Performance overlay visible to operator (Day 2)
                    → Decision: keep / adjust / revert (Day 3–7)
```

Total loop: 1–7 days. The feedback cycle for a planogram change compresses from months to a week.

This is not a minor efficiency gain. It changes what decisions are possible. At 12-week latency, only major range changes are worth making — the overhead is too high for small adjustments. At 1-week latency, operators can experiment continuously: move an item, watch what happens, adjust. The store becomes a testbed.

---
last-compiled: 2026-05-04
needs-review: false

## What Canary Is Not Building (Yet)

| Out of scope | Why |
|---|---|
| JDA-level space optimization (automated linear foot calculation) | Requires fixture dimension data and automated planogram generation — Phase 3 |
| Multi-store range management (HQ → store) | Multi-tenant capability — Phase 2 |
| Category management workbench (full JDA replacement) | Enterprise capability — long-term roadmap |
| Automated planogram generation from sales data | AI-driven; requires the data accumulation Phase 1 builds |

The v1 goal: live planogram on mobile, guided implementation, shelf-edge label print, performance overlay, range status management, and POS location lookup. That is the complete structural replacement of what JDA + batch exports + printed PDFs used to do — not the full depth of JDA's category management, but the 80% that an SMB operator needs.

---
last-compiled: 2026-05-04
needs-review: false

## Build Priority for SRD

1. **Item-location map** (zone + aisle + shelf + position per item) — the foundation; everything else queries against this
2. **Planogram view** (visual shelf layout, tapable items, SOH and velocity overlay)
3. **Range status model** (Active / Trial / Seasonal / Phase-Out / Inactive) + status-change workflow
4. **POS location lookup** (associate queries "where is this item?" from Android POS or Canary mobile)
5. **Guided implementation** (step-by-step reset, scan confirmation, implementation timestamp)
6. **Shelf-edge label print** (triggered by planogram change; Bluetooth label printer)
7. **Performance overlay** (velocity band color coding on planogram view)
8. **Range decision nudges** (slow movers, trial expiry, phase-out candidates)

Items 1–4 are the core. Items 5–8 are the intelligence layer that makes the core valuable.

[[Brain/wiki/cards/store-ops-capability-model]] · [[Brain/wiki/cards/canary-demand-sensing-smb]] · [[Brain/wiki/cards/rpas-planning-paradigm]] · [[Brain/projects/Canary]]
