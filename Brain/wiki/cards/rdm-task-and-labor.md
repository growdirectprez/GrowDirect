---
last-compiled: 2026-05-04
needs-review: false
type: reference
status: complete
tags: [rdm, retek, wms, warehouse, task-management, labor, operations, canary-context]
created: 2026-05-04
source: Retek Distribution Management V10.0–10.3 scope documents, 2001–2003
---
last-compiled: 2026-05-04
needs-review: false

# RDM — Task Management & Labor

The task management and labor layer is where RDM connects physical work to measurable output. This card covers the task queue model, activity groups, the Retek Labor Management (RLM) module, operations management, and the Visibility Workbench — all direct analogues for Canary's store operations intelligence layer.

---
last-compiled: 2026-05-04
needs-review: false

## Task Management Overview

Every physical activity in the DC is represented as a **task** in the RDM task queue:

| Task type | Description |
|---|---|
| Receiving | Unload + scan container from inbound trailer |
| Putaway | Move container from staging to storage location |
| Replenishment | Move stock from reserve to forward pick location |
| Case pick | Pick a case from active location to build a pallet |
| Unit pick | Pick individual eaches for an order |
| Bulk pick | Move a full pallet to a staging or shipping area |
| QA / VA | Process merchandise in WIP area |
| Cycle count | Count inventory in a location |
| Move | Relocate a container from one location to another |
| Load | Stage pallets into a trailer |

Tasks are sequenced in the queue. Operators receive directed task assignments from the queue — they do not self-select work. The WMS tells the picker what to do next.

---
last-compiled: 2026-05-04
needs-review: false

## Task Queue Mechanics

**Task priority:** each task has a numeric priority. The queue serves the highest-priority task first. Priority is set by wave planning and modified dynamically (V10.2 replenishment priority escalation).

**Activity group filter (V10.0):** tasks are grouped into activity groups. Operators can be assigned to a specific activity group — e.g., a replenishment crew only sees replenishment tasks; they do not compete with pickers for queue access. This prevents priority inversions where a replenishment truck hogs tasks needed by the pick floor.

**Task monitoring (V10.0):** supervisor screen showing all in-progress tasks, their assignees, and elapsed time. Exceptions (task overdue, task abandoned) surface in the monitor.

**Task queue totals (V10.2):** the task maintenance screen shows total CASE PICKS and PALLET PICKS outstanding — not just the next task in queue, but the depth of the queue. A manager can see "192 case picks remaining" at a glance.

**Skipped task audit trail (V10.2):** when an operator uses the skip key to bypass a task assigned to them (to search for a different task), the system logs who skipped, what was skipped, and when. Captured in the Activity History Log. A direct accountability mechanism — skip behavior was previously invisible to management.

**Task lookup filtered by pending tasks (V10.2):** task search restricted to tasks that are actually available to be picked up. Eliminates confusion from seeing locked or assigned tasks in search results.

---
last-compiled: 2026-05-04
needs-review: false

## Interleaved Task Scheduling

**Interleaving** is the practice of assigning a worker a sequence of tasks from different categories, designed to minimize travel distance while balancing workload. A forklift operator might receive: putaway task (zone A) → replenishment task (zone B) → cycle count task (zone A) — each task positioned to minimize deadhead travel.

RDM supports interleaved task scheduling. The interleaving logic accounts for:
- Current operator location
- Task location (zone, aisle, bay)
- Task type (must have equipment to complete — e.g., pallet jack required for bulk)
- Task priority

Labor Management reporting (V10.2) can report on interleaved tasks using logical operators, isolating the performance impact of interleaving decisions.

---
last-compiled: 2026-05-04
needs-review: false

## Foundation Process Engine (V10.2) — Task Configuration

V10.2 introduced a process-driven approach where tasks are defined as combinations of:

```
Task Type + Presentation Style → Process
                                  ├── Capture attributes (what data to collect)
                                  ├── Validate attributes (what to force-confirm)
                                  └── Match attributes (item-location constraints)
```

**Presentation Style** defines HOW the task is executed:
- RF screen (handheld / arm-mounted / truck-mounted terminal)
- Label (print + apply)
- Paper (pick sheet or putaway sheet)
- GUI (supervisor screen)

Each process can have its own labor standard — a case pick via RF has a different standard than a case pick via paper. The same physical task executed differently is a different process with a different productivity baseline.

---
last-compiled: 2026-05-04
needs-review: false

## Retek Labor Management (RLM) — V10.2

RLM is a bolt-on module introduced November 2002. It can run with RDM or as a standalone integrated to any WMS via the RIB XML layer.

### Data Flow

```
RDM (activity events) → RIB (XML) → RLM (labor module)
                                          ↓
                                    Standards + Reports
```

RLM receives activity history from RDM via published APIs. It does not sit in the transaction path — it consumes the event log as its data source.

### Labor Standards

A **standard** is the expected time to complete a defined process. Standards have two components:
- **Fixed:** setup time, system overhead, fixed distance
- **Variable:** travel distance, unit count, weight

Travel distance uses X, Y, Z coordinates assigned to each location. Vehicle speeds (loaded/unloaded, vertical/horizontal movement) are factored separately. The system calculates expected travel time from coordinates + speed, not fixed estimates.

Standards can be set as:
- **Engineered** (from a time study)
- **Historical** (derived from actual performance data)
- **Estimated** (placeholder during initial setup)

Standards cover both **direct activities** (productive tasks — picking, putaway, replenishment) and **indirect activities** (non-productive — waiting, training, meetings).

### Productivity Reporting

RLM compares actual time vs. standard time at:
- Individual operator level
- Team level
- Department level
- Shift level
- Facility level

Timeframe is user-defined (day, week, month, custom window). Reports can be scoped to specific processes or work elements.

**Time & Attendance interface:** RLM integrates with a T&A system. Start/end-of-day and breaks/lunches are ingested from T&A. This enables paid time vs. system time comparisons — i.e., was the operator clocked in but not generating task completions? Direct/indirect ratio is visible.

**Measured vs. unmeasured functions:** some activities (training, breaks, equipment maintenance) cannot have engineered standards. RLM tracks the split between measured time (with standards) and unmeasured time to give a true picture of labor utilization.

---
last-compiled: 2026-05-04
needs-review: false

## Cycle Counting

Cycle counting is RDM's perpetual inventory verification method — a rolling program of location counts that replaces the annual wall-to-wall physical inventory.

- Any bulk or bulk replenishment screen has a function key to flag the current location for cycle count (V10.2 — previously not available on bulk screens, now consistent with all picking screens)
- Cycle count tasks generated by zone or item-class priority
- Count team performs the count via RF; exceptions (count ≠ system) surfaced for investigation
- System SOH adjusted on confirmed count

---
last-compiled: 2026-05-04
needs-review: false

## Operations Management / Visibility Workbench (V10.3)

The Visibility Workbench is the highest-order operations management surface in the V10.x scope — a management dashboard providing end-to-end DC performance visibility.

Scope covers:
- **Inbound:** appointment status, receiving throughput, dock door utilization
- **Inventory:** current SOH by zone, location utilization, putaway queue depth
- **Outbound:** wave status, picks in progress, packs completed, load sequencing status
- **Labor:** task queue depth by activity group, operator productivity vs. standard
- **Exceptions:** overdue tasks, skipped tasks, QA holds, sorter jams

The Workbench is the DC equivalent of a control tower — it does not direct individual tasks (that's the queue) but gives management the situational awareness to intervene before exceptions cascade.

---
last-compiled: 2026-05-04
needs-review: false

## Logistics Activity Cost Metrics (V9)

RDM V9 added activity-based and storage-based cost measurement:

**Activity-based cost:**
- Every activity (task) has a configured cost rate
- Per-task cost = rate × activity (units, time, distance)
- Tracked by item + activity + PO + store/customer order
- Enables cost-per-unit analysis: what does it cost to receive, store, pick, and ship SKU X?

**Storage cost:**
- Calculated periodically for merchandise in storage
- = time in storage × location cost rate
- Also captured at point of replenishment pull — how long did this merchandise sit in reserve?

**Report:** cost-per-unit analysis by item or merchandise group, with activity cost and storage cost components displayed separately.

This is the first version of a cost-to-serve model in RDM. It is the intellectual ancestor of Canary's satoshi-per-event cost model — every junction traversal has a cost, and the system tracks it.

---
last-compiled: 2026-05-04
needs-review: false

## Impact Analysis (V8)

V8 introduced an impact analysis suite — a planning capability that answers "what happens to the DC if we change this?" before committing to the change:

- **DC Overview:** high-level summary of facility impact from a proposed change
- **Inbound impact:** how does a change in inbound volume or SKU mix affect receiving throughput?
- **Outbound impact:** how does a change in order profile or wave size affect pick/pack throughput?

Impact analysis is a read-only modeling tool — it doesn't generate tasks or change inventory. It gives supervisors and planners the evidence to make scheduling decisions.

---
last-compiled: 2026-05-04
needs-review: false

## Canary Relevance

| RDM Task/Labor Concept | Canary Analogue |
|---|---|
| Task queue with directed assignment | Canary store ops: employee mobile app receives directed tasks (replenishment, receiving, cycle count) |
| Activity group filter | Canary role-based task routing: receiving associate sees receiving tasks; floor associate sees replenishment tasks |
| Skipped task audit | Canary accountability: task-skip events logged per employee; visible in ops dashboard |
| Task queue totals | Canary shift dashboard: "42 replenishments pending" at a glance |
| Labor standards (engineered + historical) | Canary labor module: expected time per task type; actual vs. standard comparison |
| X, Y, Z travel distance calculation | Canary store map: zone-level travel time estimates for task scheduling |
| RLM bolt-on via RIB | Canary Labor module: separate analytics layer consuming activity events from the core via MCP events |
| Activity cost metrics | Canary cost-per-event: satoshi-denominated cost-to-serve per item per activity |
| Visibility Workbench | Canary Operations Hub: real-time store ops dashboard for shift supervisors and owner/operators |
| Impact analysis | Canary scenario modeling: "what happens to floor coverage if I reduce staff by 2 on Saturday?" |
| Cycle count | Canary perpetual inventory: rolling count program with RF/mobile confirmation |
| Time & Attendance interface | Canary Labor: shift log integration; clock-in/out vs. task completions; productive vs. idle time |

**The most strategically important pattern:** the task queue + labor standards + cost metric triad. Canary's store ops model should be built around this triad from day one — not added later. Every task generated in the store has a type, a standard time, and a cost. The gap between standard and actual is the efficiency signal. The accumulated cost is the basis for the satoshi billing model. These three things are the same thing viewed from three different angles: operations, HR, and finance.

[[Brain/wiki/cards/rdm-wms-core-concepts]] · [[Brain/wiki/cards/rdm-picking-and-outbound]] · [[Brain/wiki/cards/rdm-inbound-and-receiving]] · [[Brain/projects/Canary]]
