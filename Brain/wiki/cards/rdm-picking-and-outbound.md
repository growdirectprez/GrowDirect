---
last-compiled: 2026-05-04
needs-review: false
type: reference
status: complete
tags: [rdm, retek, wms, warehouse, picking, wave, outbound, canary-context]
created: 2026-05-04
source: Retek Distribution Management V10.0–10.3 scope documents, 2001–2003
---
last-compiled: 2026-05-04
needs-review: false

# RDM — Picking & Outbound

Covers the full pick-and-ship arc: wave planning, active vs. reserve picking, sorter management, order consolidation, packing, loading, and the order status state machine. This is the most operationally dense section of RDM — the core execution logic that runs the DC floor.

---
last-compiled: 2026-05-04
needs-review: false

## Location Architecture: Active vs. Reserve

The physical DC is divided into two inventory layers:

| Layer | Purpose | How merchandise gets there |
|---|---|---|
| **Active / Forward Pick** | The pick face — what pickers touch | Putaway from inbound or replenishment from reserve |
| **Reserve / Bulk Storage** | Overflow stock | Direct putaway from inbound |

Every high-velocity item has a **forward pick location (FPL)** — a designated slot sized for the item's daily pick volume. When the FPL runs low, a **replenishment task** is generated to pull stock from reserve. The picker never goes to reserve; reserve moves to the pick face.

**Multiple active locations per item (V9):** A single item can have active locations in multiple pick zones, each assigned a relative priority. Replenishments and distribution logic both honor priority order.

---
last-compiled: 2026-05-04
needs-review: false

## Pick Methods

| Method | What it is | When to use |
|---|---|---|
| **Case pick** | Full case picked from active or reserve | High-volume, store replenishment, pallet-build |
| **Unit pick (stationary SKU)** | Individual eaches from a fixed location | DTC / e-comm, mixed orders |
| **Bulk pick** | Full pallet moved as a unit | Cross-dock, high-velocity case flow |
| **Forward case picking (FCP)** | Case pick from a dedicated forward case location (V10.2) | Belt-pick / pallet-build environments |
| **Put-to-order (dynamic slotting)** | Aggregated SKU requirements pulled to staging; units directed into order-specific slots | DTC high-volume pick/pack |
| **Paper picking** | Pick sheet (barcode group ID) for non-RF environments | Peak season supplemental labor |

**Paper picking (V9):** enabled/disabled per wave. Prints a pick sheet grouped by location sequence. Group ID scanned at confirmation screen — if no exceptions, confirmed in one step; exceptions entered line by line. Allows peak-season temp labor to operate without RF hardware.

---
last-compiled: 2026-05-04
needs-review: false

## Wave Planning

A **wave** is a planned batch of order picks executed together. Wave planning determines:
1. Which orders get selected
2. How picks are grouped and sequenced
3. What time window the wave targets

**Wave selection criteria (V9, expanded):**
- Order type (store, customer)
- Number of lines (singles vs. multi-line)
- Piece count
- Value-added service requirement
- Unit pick zone assignment
- Ship-not-before date
- Route / delivery type
- Cube and weight totals (V10.3)

**Automatic wave generation (V9):** scripted iterative process. User defines desired wave size (orders / lines / pieces / cube). System fills waves against user-specified priority sequence until cutoff. Significantly reduces administrative overhead.

**Max time wave (V10.2):** user inputs MAX TIME (hours + minutes). Wave build accumulates orders until the calculated processing time reaches the limit. Output = a wave sized to fit the available labor window.

**Ship-complete orders (V9):** if a wave cannot fully satisfy a ship-complete order, no picks are generated for that order — it returns to the allocation pool. Checked at three points: OMS (before release), wave planning, and pack-out.

---
last-compiled: 2026-05-04
needs-review: false

## Sorter Management (V10.0)

In DCs with automated unit sorters, RDM manages sorter capacity and chute assignment.

**Sorter capacity:** wave planning considers total sorter throughput — picks generated cannot exceed sorter capacity in the time window.

**Chute management:** orders assigned to chutes (output lanes on the sorter). One chute = one order destination (store or customer). Chute assignment is the link between pick and pack — picked items divert to the correct chute; packer collects from the chute and packs.

**Multiple RF put-to-store systems (V8):** RDM supports multiple simultaneous put-to-store (PTS) grids operating in parallel. Each grid handles a subset of destinations. Necessary for DCs serving large store counts where a single PTS grid is insufficient.

---
last-compiled: 2026-05-04
needs-review: false

## Replenishment Triggers and Types

| Trigger | Description | Version |
|---|---|---|
| Wave-demand replenishment | Generated during wave planning when FPL projected to be insufficient | Base |
| Reorder point replenishment | Triggered when FPL inventory falls below defined threshold | Base |
| Top-off replenishment | Fills FPL to capacity during off-peak, regardless of demand trigger | V10.1 |
| Dynamic overflow | Creates a temporary overflow FPL when primary location at hard capacity limit | V10.1 |
| Opportunistic (inbound) | Inbound merchandise directed straight to FPL when below reorder point | V10.0 |
| Wave-based replenishment (V10.3) | Configurable algorithm per location; timed release when FPL capacity allows | V10.3 |

**Replenishment priority escalation (V10.2):** a background process continuously monitors FPL inventory. When a pick demand will outpace the current on-hand, replenishment task priority is automatically escalated. Returns to original priority when demand falls below on-hand. This is real-time priority management — not a wave-planning artifact.

---
last-compiled: 2026-05-04
needs-review: false

## Order Status State Machine (V9)

Order and order-line status is maintained end-to-end:

```
Open → Selected → Pending Picks → Picked → Packed → Loaded/Manifested → Shipped
```

| Status | Description |
|---|---|
| Open | Unprocessed — in allocation pool |
| Selected | Included in a wave for picking |
| Pending Picks | Picks generated, not yet completed |
| Picked | All picks confirmed |
| Packed | Picked and packed for delivery |
| Loaded/Manifested | Loaded onto trailer, awaiting departure |
| Shipped | Trailer departed |

Status maintained at **order line level** — different lines on the same order can be at different statuses (e.g., one line shipped, another backordered). Customers (or host OMS) can query status per line.

---
last-compiled: 2026-05-04
needs-review: false

## Packing and Outbound Audit

**Pack-out process:** once picked, items are conveyed to the pack station. Packer assembles the order, checks for completeness (ship-complete enforcement point 3 if applicable), and seals the container.

**Packing slip (V9):** enumerates contents of the current shipment AND items shipping separately (back order / ship-alone indicators per line). Communicates to the customer what is in this box and what is coming later.

**Outbound QC audit GUI (V10.0):** manager-level screen providing an audit view of packed containers against wave picks. Not RF-based — a supervisor screen that confirms packed quantities before loading authorization.

**Wave monitoring (V10.0):** dashboard view of wave execution status in real time — picks in progress, picks completed, packs completed, exceptions flagged.

**Hot picks (V10.0):** priority overrides for urgent orders that arrive after the wave has started. Hot picks are injected into the active wave and processed ahead of non-priority picks.

---
last-compiled: 2026-05-04
needs-review: false

## Outbound Loading and Shipping

**Load sequencing (V9, V10.2):** RDM supports route-based load sequencing — the sequence in which stores are loaded onto the trailer. Reverse loading = the first stop is loaded last (so it's the first off the trailer). Load sequencing ensures the right pallet is at the door at the right time when the route sequence is fixed.

**Load sequence validation (V10.2):** if a picker starts loading a destination out of sequence, the system issues a warning that merchandise for a prior destination on the route has not yet been loaded. Prevents stop-sequencing errors that create delivery chaos.

**Route-based shipping schedules (V9):** dispatch schedule per route with cut-off times. System directs picking and loading so merchandise for each route is ready by its departure window.

**Trailer management (V10.3):** multiple seal numbers, trailer maintenance screen, ship trailer warning when trailer departs without all expected pallets confirmed.

**Routing package interface (V10.3):** export of cube/weight totals to a 3rd-party routing package for truck load planning. Integration point, not an internal capability.

---
last-compiled: 2026-05-04
needs-review: false

## Outbound Order Consolidation (V10.0)

When a customer or store order is fulfilled across multiple picks (from different zones, different pick times), the consolidation step brings them together into a single outbound container before packing. RDM manages consolidation staging locations and the merging logic.

---
last-compiled: 2026-05-04
needs-review: false

## SKU Profiling — Streamsoft FlowTrak (V10.1)

RDM 10.1 added an API to the Streamsoft FlowTrak SKU profiling engine. FlowTrak analyzes:
- SKU velocity (order frequency × piece count)
- SKU physical dimensions
- Location types and racking configuration
- Aisle range and slotting strategies by product group

Output: recommended FPL assignments (or re-assignments) based on velocity and location characteristics. RDM receives the profile recommendation and automatically generates the SKU-FPL association and queues the required Move task.

This is the DC equivalent of Canary's assortment optimization — except FlowTrak targets travel distance efficiency, not sell-through rate.

---
last-compiled: 2026-05-04
needs-review: false

## FIFO / Pick-to-Clean / Best-Before Distribution Methods (V8)

When multiple containers of the same item exist in reserve, RDM determines which to pick first:

| Method | Logic |
|---|---|
| **FIFO** | First received = first picked (receipt date order) |
| **Pick-to-clean** | Pick from the location with the least quantity to empty it first (space recovery) |
| **Best-before** | Pick the container with the nearest expiry date first (perishable management) |

Method configured per item or item class. Perishable items default to best-before.

---
last-compiled: 2026-05-04
needs-review: false

## Canary Relevance

| RDM Picking Concept | Canary Analogue |
|---|---|
| Forward pick location | Active shelf face (display floor) |
| Reserve location | Back-stock |
| Wave planning | Canary task scheduling: batch replenishment tasks by zone and time window |
| Wave status machine | Canary store ops: task status from assigned → in-progress → complete → verified |
| Order status machine | Canary inbound PO + outbound transfer tracking |
| Replenishment priority escalation | Canary live SOH monitor: escalate replenishment task if shelf drops to display minimum |
| Top-off replenishment | Canary "pre-shift top-off" task: fill active locations before peak traffic hours |
| Sorter / chute management | Canary pick-pack for BOPIS or curbside: order-specific container assignment |
| Ship-complete logic | Canary BOPIS: flag order as incomplete if any line unavailable; hold vs. partial-fulfill |
| FIFO / best-before | Canary freshness compliance for produce / deli — date-stamped receiving, FEFO picking |
| Wave monitoring dashboard | Canary task dashboard: active tasks by employee + zone + status |
| FlowTrak SKU profiling | Canary slotting optimizer: velocity-based shelf assignment suggestions |

**The wave planning pattern is the most directly reusable concept.** Canary's store operations model should adopt the wave as the scheduling unit: a wave = a shift's replenishment plan, sized by task time budget, ordered by zone sequence, with real-time priority escalation for at-risk shelves.

[[Brain/wiki/cards/rdm-wms-core-concepts]] · [[Brain/wiki/cards/rdm-inbound-and-receiving]] · [[Brain/wiki/cards/rdm-task-and-labor]] · [[Brain/projects/Canary]]
