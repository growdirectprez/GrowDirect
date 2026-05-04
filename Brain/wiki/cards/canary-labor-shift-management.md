---
last-compiled: 2026-05-04
needs-review: false
type: reference
status: active
tags: [canary, labor, shift, task-assignment, productivity, functional-requirements, mobile]
created: 2026-05-04
---
last-compiled: 2026-05-04
needs-review: false

# Canary — Labor & Shift Management

Enterprise labor management (Retek Labor Management, JDA Workforce Management) was built for DCs with 200–500 workers where even a 5% productivity improvement saves $2M per year. The SMB translation is a store with 3–10 associates and a shift supervisor who is often also the owner-operator.

The job is different at this scale — not optimizing across hundreds of workers, but making sure 4 associates know what to do today, that the right tasks are assigned to the right people, and that the owner can see whether the shift is on track without being physically present.

The RLM principles that survive the translation: directed tasks, activity group routing, time standards, skip/exception logging, and shift-level productivity visibility. The enterprise mechanisms that don't survive: engineered time studies, X/Y/Z coordinate travel calculations, time-and-attendance system integration, and interleaving algorithms designed for forklift operators.

---
last-compiled: 2026-05-04
needs-review: false

## The Shift Model

A **shift** in Canary is a named work period with defined staff and a task load. It is the unit of labor planning.

```
Shift
├── Start time + End time
├── Associates assigned
│   ├── [Name 1] — role: floor associate
│   ├── [Name 2] — role: receiver
│   └── [Name 3] — role: cashier (POS only, no Canary tasks)
├── Task load at shift start
│   ├── Replenishment tasks: 12
│   ├── Receiving tasks: 4 (delivery expected 10am)
│   └── Cycle count tasks: 0 (not scheduled today)
├── Estimated completion: 3.5 hours with 2 floor associates
└── Shift notes: "[Supplier D] delivery — large order, may need help 10-11am"
```

**Shift creation:** the owner-operator creates shifts manually or from a template (Mon–Fri standard template, Weekend template). Canary does not do full workforce scheduling — it doesn't know who is available or what hours each employee works. That lives in a separate scheduling system (or in the owner's head). Canary takes in "who is on today" and optimizes the task load across them.

**Shift templates:** a Monday morning shift might always have: 8 replenishments + receiving prep + 2 zone checks. A Friday afternoon might always have: 15 replenishments + planogram check + end-of-week cycle count. Templates let the operator configure once and reuse.

---
last-compiled: 2026-05-04
needs-review: false

## Associate Roles and Task Routing

Not every associate should receive every task type. Activity group routing from RDM — simplified:

| Role | Task types they receive |
|---|---|
| **Floor Associate** | Replenishment, cycle count, shelf moves, planogram implementation |
| **Receiver** | Receiving, putaway, new item onboarding |
| **Shift Lead / Supervisor** | All task types + exception escalations, task reassignment |
| **Cashier** | POS tasks only — no Canary task queue (they have their own job) |

Role is set on the employee profile. An associate can hold multiple roles (small stores often have floor associates who also receive).

**Task assignment modes:**
- **Auto-assign at shift start:** Canary distributes the task queue across available floor associates and receivers based on their roles. Each associate starts their shift with a pre-loaded task list.
- **Manual assign:** supervisor assigns specific tasks to specific people — useful when one associate is faster at receiving, or one zone is someone's responsibility.
- **Queue mode:** tasks are unassigned; associates pull the next task from the queue when they complete one. No pre-assignment. Best for flexible staffing.

---
last-compiled: 2026-05-04
needs-review: false

## Task Time Standards — SMB Version

RLM used engineered time studies and X/Y/Z travel distance calculations. For SMB, the equivalent is a lookup table based on task type and store size:

```
Task Type Standards (configurable per store)

Replenishment:        8–12 minutes per task
  (includes walk to back-stock, pick case, walk to floor, stock shelf)

Receiving (per case): 2–3 minutes per case
  (includes scan, quantity confirm, putaway direction, walk)

Cycle count (per location): 3–5 minutes per location
  (includes walk to zone, count items, enter counts)

New item onboarding:  10–15 minutes per item
  (includes scan, setup wizard, location assignment, first putaway)

Shelf move:           20–30 minutes per planogram section
  (includes clearing shelf, relabelling, restocking in new position)
```

**Standards calibration:** the first 4 weeks of using Canary generates actual completion time data per task type per associate. After that, Canary compares actual vs. standard. The standards auto-adjust based on observed actuals — if replenishment tasks are consistently completing in 6 minutes, the standard adjusts to 6 minutes. The operator can override (e.g., "this store has longer aisles").

**Shift capacity estimate:** at shift start, Canary calculates:

```
Available labor hours = (number of floor associates) × (shift duration − breaks)
Task load = sum of (tasks × standard time)

Estimate:
  Available: 2 associates × 3.5 hours = 7 hours
  Task load: 12 replenishments × 10min + 4 receiving × 3min × 12 cases
           = 120min + 144min = 264 min = 4.4 hours
  Slack: 2.6 hours — capacity to handle unplanned tasks

  [or]

  Estimate: 1 associate × 3.5 hours = 3.5 hours  
  Task load: 5.5 hours
  ⚠ Overloaded — prioritize by urgency or request additional coverage
```

The overloaded warning is important for a solo operator who is also the only floor associate. If the task queue is larger than one person can complete in a shift, they need to know at the start — not at the end when tasks are still outstanding.

---
last-compiled: 2026-05-04
needs-review: false

## Productivity Tracking

**Per-associate view (shift summary):**

```
[Name 1] — Floor Associate
Shift: 8:00am – 4:00pm

Tasks completed: 11
  Replenishments: 8    Avg time: 9.2 min (standard: 10 min)  ✓ On pace
  Cycle counts:   2    Avg time: 4.1 min (standard: 4 min)   ✓ On pace
  Other:          1

Exceptions flagged: 1  (Aisle 3 shelf damage)
Tasks skipped: 0

On-task time: 3.5 hours / 6.5-hour shift
  (Gap: 3 hours — breaks + untracked time + cashier assist)
```

Canary tracks time from task-start to task-complete for every task. The gap between on-task time and shift length includes breaks, customer assists, cashier relief, and anything else the associate was doing but Canary didn't see. Canary does not track non-task time — it doesn't know why someone wasn't in the task queue.

**What this is for:** the owner reviewing Monday's performance can see that Associate 1 completed 11 tasks averaging 9 minutes each (slightly ahead of standard) and Associate 2 completed 7 tasks averaging 14 minutes (behind standard). This is not punitive data — it's calibration data. Maybe Associate 2 was helping customers all morning. The productivity view is a conversation starter, not a performance evaluation system.

**Skip tracking (from RDM — preserved):** when an associate uses the Skip button to bypass an assigned task, Canary logs it:
- Which task was skipped
- Who skipped it
- What they did instead (the next task they picked up)
- Optional reason (required if the same task is skipped twice)

A pattern of skipped tasks for a specific zone or task type surfaces in the shift summary. It may indicate a physical problem (location blocked, item hard to access), a training gap, or an associate avoiding something. The supervisor investigates.

---
last-compiled: 2026-05-04
needs-review: false

## Exception Management

Exceptions generated during task execution need to land somewhere actionable. They flow to:
1. The associate's device (immediate: "task paused — exception flagged")
2. The shift lead's task dashboard (within 60 seconds)
3. The Hub attention queue (if critical — stockout, receiving issue)

**Exception types and routing:**

| Exception | Severity | Who sees it |
|---|---|---|
| Shelf damaged | Medium | Shift lead + Hub |
| Location empty / can't find item | High | Shift lead immediately |
| Receiving quantity mismatch | High | Shift lead + operations log |
| SOH appears wrong (counted less than expected) | High | Generates cycle count task |
| Task cannot be completed — reason given | Medium | Shift lead dashboard |
| Task skipped twice | Medium | Shift lead dashboard |

**Exception resolution:** the shift lead receives the exception and either:
- Investigates and resolves themselves (marks exception resolved with a note)
- Reassigns to a different associate with context ("this shelf needs the ladder — give it to Name 3")
- Escalates to the owner if it requires a decision above the shift lead's authority

Every exception is logged with a resolution timestamp. Over time, the pattern of exceptions by zone, task type, and time-of-day identifies systemic operational problems.

---
last-compiled: 2026-05-04
needs-review: false

## The Associate Mobile Experience

The associate's phone view is deliberately minimal. They have one job: work through their task queue.

```
┌─────────────────────────────┐
│  [Name 1]     ○ Available   │
├─────────────────────────────┤
│  NEXT TASK                  │
│  ─────────────────────────  │
│  📦 Replenishment           │
│  [Item Name]                │
│  Back-stock: Zone C, Bin 14 │
│  Floor: Aisle 4, Shelf B    │
│  Qty: 12 units              │
│                             │
│  [ Start Task ]             │
│  [ Can't do this — skip ]   │
├─────────────────────────────┤
│  Remaining today: 8 tasks   │
│  Est. finish: 11:42am       │
└─────────────────────────────┘
```

"Estimated finish" is calculated from remaining tasks × standard time, updated after each completion. If the associate is running ahead of pace, the estimate moves earlier. This gives the associate a sense of progress without requiring them to know how many tasks are in the queue. It also surfaces whether they're going to finish before the shift ends — if the estimate says 1:00pm and the shift ends at noon, something needs to change.

**No analytics, no dashboards, no settings on the associate view.** Those belong to the shift lead and owner. The associate's phone is a task terminal, not a management tool.

---
last-compiled: 2026-05-04
needs-review: false

## Multi-Associate Coordination — Avoiding Conflicts

In a small store, two associates might independently decide to replenish the same item, or one might start receiving while another is still in the back-stock area. Task assignment prevents this — if a task is assigned to Associate 1, Associate 2 won't see it.

**Task locking:** when an associate taps "Start Task," the task is locked to them. Other associates' task queues don't show locked tasks. If the associate abandons the task mid-way (phone dies, emergency), the task unlocks after 30 minutes and returns to the queue.

**Area awareness:** the app can optionally notify when two associates are assigned to the same zone at the same time — not a hard block, just a coordination signal. Useful during a large receiving event when the back-of-house is crowded.

---
last-compiled: 2026-05-04
needs-review: false

## Shift Close — What Gets Captured

At the end of a shift, Canary produces a shift summary:

```
SHIFT CLOSE — Monday May 4 | 4:00pm

Associates on shift: 3
Tasks completed: 26 | Outstanding: 2 (pushed to next shift)

Performance:
  [Name 1]: 11 tasks, 9.2 min avg — On pace
  [Name 2]: 10 tasks, 11.4 min avg — Slightly below standard
  [Name 3]: 5 tasks, 8.8 min avg — On pace

Exceptions: 2 logged, 1 resolved, 1 pending (shelf damage — awaiting repair)

SOH changes this shift:
  Replenishments processed: 8 (84 units stocked)
  Receiving: 48 cases (6 items, PO #12847)
  Adjustments: -4 units (1 cycle count correction)

Outstanding: 2 replenishment tasks deferred to evening shift
```

The shift summary is stored. Over time it becomes the labor efficiency record: shifts where tasks were completed on pace, shifts where they weren't, and the context (delivery day, short staffed, high customer traffic from POS data) that explains the variance.

---
last-compiled: 2026-05-04
needs-review: false

## What This Is Not

Canary's labor module is **not** a workforce scheduling system. It does not:
- Manage employee availability or hours
- Generate shift schedules based on predicted demand
- Interface with payroll
- Handle complex labor law compliance (overtime rules, break requirements, minor work rules)

Those problems are hard and solved by purpose-built tools (7shifts, Homebase, When I Work). Canary integrates with them in the future — import who's on today, export task completion as a productivity signal. For now, the operator tells Canary who is working, and Canary manages the work.

[[Brain/wiki/cards/store-ops-capability-model]] · [[Brain/wiki/cards/canary-operations-hub]] · [[Brain/wiki/cards/canary-mobile-task-ux-flows]] · [[Brain/wiki/cards/rdm-task-and-labor]] · [[Brain/projects/Canary]]
