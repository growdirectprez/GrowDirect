---
last-compiled: 2026-05-04
needs-review: false
type: reference
status: active
tags: [canary, store-ops, mobile, android-pos, functional-requirements, application-design]
created: 2026-05-04
---
last-compiled: 2026-05-04
needs-review: false

# Store Operations Capability Model

A synthesis of enterprise WMS and replenishment system design patterns (RDM, ORMS, RPAS) reframed as modern application capabilities for Canary. The source material represents a decade of operational intelligence — the goal here is to extract the functional requirements that proved durable, discard the implementation artifacts of the thick-client / RF-terminal era, and rewire them for a mobile-first, Android POS-integrated architecture.

This is an application design reference, not a source analysis. Build from this, not from the source docs.

---
last-compiled: 2026-05-04
needs-review: false

## The Core Thesis

Enterprise WMS and replenishment systems solved hard problems correctly in the 1990s and 2000s. They got the domain model right:

- Every inventory unit is tracked by a license plate through every location transition
- Every task is a directed assignment with a measurable standard
- Every planning decision is an algorithm with explicit inputs and a traceable output
- Every deviation from plan produces an exception event that surfaces to a human

What they got wrong was delivery: thick-client Windows GUIs, RF handheld terminals with 20-character screens, batch-mode integrations, and separate systems for every functional layer.

**Canary collapses those delivery layers into one stack.** The domain model is inherited. The delivery layer is rebuilt: mobile-first (tablet + phone), Android POS-native, real-time packet-speed, MCP-connected.

---
last-compiled: 2026-05-04
needs-review: false

## Capability Layer 1: Inventory & Location Model

**What enterprise got right:**
Every item has a location. Every location has a type. Every move is recorded. The container / license plate model creates a continuous chain of custody from receiving dock to sales floor.

**Canary's implementation:**

| Capability | Design requirement |
|---|---|
| Item-location binding | Every SKU has a mapped primary floor location (zone + shelf) and a back-stock zone |
| Location classes | Zones typed by temperature, handling, security, display format |
| Container / LP | Every receiving unit gets a scan-assigned ID; movements tracked against that ID |
| Multi-location items | High-velocity SKUs can have multiple active locations in different zones |
| Location capacity | Each location has a defined display minimum (floor) and maximum (capacity) |
| Putaway direction | System suggests putaway location based on zone, capacity, and proximity to active face |

**Android POS integration point:** The POS scans the barcode on the item at sale. That event should decrement the floor inventory in Canary in real time — not via a nightly batch. The POS is Canary's SOH sensor on the active location. The integration contract: sale event → item + quantity → Canary SOH adjustment.

---
last-compiled: 2026-05-04
needs-review: false

## Capability Layer 2: Replenishment Logic

**What enterprise got right:**
Four replenishment methods of increasing sophistication: Constant (fixed max) → Min/Max (order points) → Time Supply (days-of-supply) → Dynamic (forecast + service level). The escalation path from simple to sophisticated is the right model for SMB onboarding.

**Canary's implementation:**

**Replenishment Method Selector** — shown to the user as a progressive disclosure:

```
Level 1: Min/Max (no forecasting required)
  → Set a floor (display minimum) and a ceiling (order up to)
  → Task fires when SOH < floor
  → Parameters: min units, max units, increment (typically 1 case)

Level 2: Days-of-Supply (forecast-based floor and ceiling)
  → System calculates min and max from velocity × days window
  → User sets: days to hold (ISD equivalent), lead time
  → Less manual maintenance; adapts to velocity changes

Level 3: Dynamic (service level + safety stock)
  → Full ORMS Dynamic-Issues algorithm
  → Inputs: service level %, lost sales factor, lead time (COLT/NOLT)
  → Output: recommended order quantity per review cycle
  → Requires forecast data (typically 8+ weeks of sales history)
```

**UI principle:** the method selector should show the user the trade-off, not just the name. "Min/Max: simple, manual — works for any item. Days-of-Supply: auto-adjusts to sales pace. Dynamic: full algorithm — best for high-velocity items where stockouts are costly."

**Android POS integration point:** POS sales velocity is the input to the Days-of-Supply and Dynamic calculations. Canary must subscribe to the POS sales stream (SKU + quantity + timestamp) and maintain a rolling velocity model per SKU per location. This is the core data dependency — without it, Level 2 and Level 3 replenishment are unavailable.

---
last-compiled: 2026-05-04
needs-review: false

## Capability Layer 3: Task Queue & Directed Work

**What enterprise got right:**
Workers do not decide what to do next — the system tells them. Every task is in a queue with a priority. Activity groups route different task types to the right people. Deviations (skipped tasks, overrides) are logged.

**Canary's implementation:**

**Task model:**

```
Task
├── Type: receiving | putaway | replenishment | cycle count | move | outbound
├── Priority: 1–5 (system-assigned, escalatable)
├── Location: zone + shelf (scan-confirmable)
├── Item: SKU + quantity
├── Assignee: employee (or unassigned — in queue)
├── Status: queued → assigned → in-progress → complete → verified
└── Estimated time: from labor standard lookup
```

**Mobile task screen (tablet / phone):**
- One task at a time — no queue management for floor workers
- Location shown with zone map thumbnail
- Confirm by scan (barcode or QR at shelf edge label)
- Skip button (with required reason — logged)
- Exception flag (damage, wrong quantity, location blocked)

**Supervisor dashboard:**
- Queue depth by task type
- Tasks in progress by employee
- Exceptions pending
- Overdue tasks highlighted
- Shift performance vs. standard

**Android POS integration point:** When a POS transaction creates a replenishment need (SOH drops below floor), the replenishment task appears in the Canary task queue immediately. No polling interval — event-driven. The POS sale event is the trigger.

---
last-compiled: 2026-05-04
needs-review: false

## Capability Layer 4: Wave Planning for Store Ops

**What enterprise got right:**
A wave is the unit of planning: a bounded batch of work, sized to a time window, sequenced for travel efficiency, with explicit start and end criteria. It turns a backlog of individual tasks into a shift plan.

**Canary's adaptation for store context:**

The enterprise "wave" becomes the **shift replenishment plan** in a store context:

```
Wave = Shift Replenishment Plan
  ├── Triggered: shift start (or manually on demand)
  ├── Sized by: time budget (MAX TIME concept from RDM 10.2)
  ├── Ordered by: zone sequence (minimize travel — same concentric logic as RDM 10.3)
  ├── Priority: items below display minimum ranked above items approaching minimum
  └── Output: ordered task list for the shift crew
```

**Max Time sizing:** user inputs available labor hours (e.g., "2 associates, 3 hours"). Canary calculates which replenishments fit in the time budget, ordered by priority. Items that don't fit flag for the next wave or for manager escalation.

**Real-time escalation:** within the wave, if a high-priority item is depleted faster than planned (flash sale, unexpected traffic), the replenishment task priority is elevated and inserted ahead of lower-priority tasks — same logic as RDM's background replenishment priority process.

**Mobile wave view (tablet):** shift supervisor sees the full wave as a kanban of tasks across zones. Drag to reprioritize (with confirmation). Real-time completion progress.

---
last-compiled: 2026-05-04
needs-review: false

## Capability Layer 5: Receiving & Inbound

**What enterprise got right:**
Receiving is not just counting boxes. It's the moment of truth for SOH accuracy — the system must capture what actually arrived (vs. what was declared) and immediately route it to the right destination (floor, back-stock, or holding for new-item setup).

**Canary's implementation:**

**Receiving flow (mobile):**

```
1. Delivery arrives → PO pulled from Canary (or manually entered supplier + items)
2. Scan each case as it's unloaded
3. System compares received vs. expected (quantity + item match)
4. Exception if: quantity short, item mismatch, damage flag
5. Putaway direction: floor (if below display min) or back-stock
6. Receiving event → SOH updated immediately
7. Exception report transmitted to supplier record
```

**Opportunistic to-floor routing:** if a received SKU is below its display minimum on the floor, Canary routes it to the floor immediately — not to back-stock first. The picker carries it straight to the shelf. This eliminates the latency of: putaway → replenishment task generation → replenishment pick → floor. One movement instead of three.

**New item onboarding:** first delivery of a new SKU triggers an onboarding flow: assign floor zone + shelf, set display minimum and maximum, select replenishment method. Receiving does not complete until the item is slotted. Back-stock holding zone used in the interim.

**Android POS integration point:** New items received in Canary must also be present in the POS item master to be scannable at the register. Integration: Canary new-item event → POS item master sync. The Canary item record is the source; POS is the consumer. This is a push, not a pull.

---
last-compiled: 2026-05-04
needs-review: false

## Capability Layer 6: Order Status & Tracking

**What enterprise got right:**
Status at the line level, not just the order level. A multi-item order has independent status per line — one line can be picked while another is on backorder. Every status transition is a timestamp.

**Canary's adaptation:**

For store-to-warehouse transfer orders and supplier purchase orders:

```
PO / Transfer Order Status
├── Draft → Submitted → Confirmed → In Transit → Received (partial / complete)
└── Per-line status: ordered → confirmed → in-transit → received → stocked
```

For BOPIS / e-comm orders (if applicable):

```
Order Status
Open → Staged for Pick → Picking → Picked → Ready for Pickup → Fulfilled
```

**Mobile notification:** customer receives status push at Picked and Ready for Pickup. Associate receives task at Staged for Pick.

**Ship-complete rule:** configurable per order type. If ship-complete is on and a line cannot be filled, no pick starts — order held with manager alert.

---
last-compiled: 2026-05-04
needs-review: false

## Capability Layer 7: Analytics & Cost-to-Serve

**What enterprise got right:**
Activity-based costing. Every task has a type. Every task type has a cost rate. Accumulated cost per item = cost to receive + cost to store + cost to pick + cost to ship. Storage cost = time in location × location cost rate.

**Canary's implementation:**

Every event in Canary generates a cost credit:

```
Event cost = base rate (by task type) + variable (quantity / distance / time)
```

Aggregated at:
- SKU level: total cost-to-serve per unit sold
- Supplier level: cost of receiving per supplier (correlates with ASN accuracy)
- Employee level: productivity (tasks / standard time)
- Store level: ops cost as % of sales

**The satoshi model:** event costs denominated in satoshis (Bitcoin L2). The aggregated cost per SKU is the verifiable, auditable cost basis for pricing and margin decisions. A merchant looking at margin on SKU X can trace every cost component back to a signed event hash. No enterprise WMS ever had this — it's a new capability enabled by the blockchain evidentiary rail.

**Insight surface (tablet dashboard):**
- SKU margin waterfall: revenue − COGS − ops cost-to-serve = true margin
- Slow-movers by storage cost (items costing more to hold than they generate)
- Labor efficiency by zone and shift
- Replenishment hit rate: % of replenishment tasks completed before SOH hit zero

---
last-compiled: 2026-05-04
needs-review: false

## Android POS Integration Architecture

Bart's operation is Android POS (DriftPOS / RapidPOS). This is not an edge case — it is the primary integration surface for the channel.

**Integration contract:**

| Direction | Event | Canary action |
|---|---|---|
| POS → Canary | Sale (item + qty + timestamp + store) | SOH decrement; check replenishment trigger |
| POS → Canary | Void / return (item + qty) | SOH increment; note return reason if available |
| POS → Canary | End-of-day close | Reconcile SOH vs. POS running total; flag discrepancies |
| Canary → POS | Item master update (new item, price change) | POS item master sync |
| Canary → POS | Inventory count (cycle count result) | POS SOH update |
| Canary → POS | Order status (BOPIS ready) | POS customer notification trigger |

**Technical notes:**
- Android POS likely exposes an API (REST or webhook) for sale events — RapidPOS / NCR Counterpoint both have documented endpoints
- Canary should be the authoritative SOH system; POS is a source of truth for transactions only
- Conflict resolution: if POS SOH and Canary SOH diverge, Canary flags for cycle count — neither auto-wins
- Authentication: per-store API key, scoped to the store's tenant in Canary

**Mobile-first implications for Canary screen design:**
- All task screens must be fully functional on a 5–6" phone screen (associates won't always have tablets)
- Supervisor dashboard optimized for 10" tablet in landscape
- Receiving flow must work offline (cellular dead zones in back-of-house) — queue events locally, sync on reconnect
- Task confirmation via barcode scan is primary; manual entry is fallback (not the other way around)
- Dark mode for back-of-house low-light environments

---
last-compiled: 2026-05-04
needs-review: false

## Summary: What to Build First

Priority order based on immediate commercial value (Bart's operation as the pilot):

1. **POS sale event integration** — the data feed that makes everything else work
2. **SOH model** — real-time inventory by SKU by location
3. **Replenishment trigger + task generation** — Min/Max to start; Days-of-Supply when velocity data accumulates
4. **Mobile task screen** — receiving, replenishment, cycle count (three screens, one flow)
5. **Shift wave plan** — sized batch of tasks for the crew
6. **Supervisor dashboard** — queue depth + exception surface
7. **Cost-to-serve analytics** — activity cost accumulation per SKU

Everything in items 1–4 should be in the hands of a pilot store operator within 8 weeks. Items 5–7 are the intelligence layer that makes Canary worth paying for.

[[Brain/wiki/cards/rdm-wms-core-concepts]] · [[Brain/wiki/cards/rms-replenishment-screen-flows]] · [[Brain/wiki/cards/rpas-planning-paradigm]] · [[Brain/projects/Canary]]
