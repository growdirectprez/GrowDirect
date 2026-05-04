---
last-compiled: 2026-05-04
needs-review: false
type: reference
status: active
tags: [canary, multi-store, chain, intelligence, analytics, transfer-orders, functional-requirements]
created: 2026-05-04
---
last-compiled: 2026-05-04
needs-review: false

# Canary — Multi-Store Intelligence

The single-store operator is the beachhead. The multi-store operator — 2 to 10 locations, same owner — is the growth path. For Bart's VAR channel, multi-store capability is the upsell: deploy Canary at one location, demonstrate value, expand to the others. This card defines what changes architecturally and functionally when a single tenant operates more than one store.

The enterprise precedent: ORMS managed replenishment across a DC-to-store network; RPAS planned across store clusters; RDM managed DC operations as a single node in a larger chain. Canary starts at the store node and grows up toward the chain view. But the architecture must anticipate the chain from day one — retrofitting multi-tenancy into a single-store design is expensive.

---
last-compiled: 2026-05-04
needs-review: false

## What Changes at Multi-Store

**Single store:** everything is store-scoped. SOH, tasks, planograms, orders — all isolated to one tenant.

**Multi-store (same owner):** the operator needs two views simultaneously:
1. **Store view** — what's happening at each specific location, as if viewing through the store's eyes
2. **Portfolio view** — consolidated performance across all locations; anomalies visible at the aggregate level; decisions that cross store boundaries (transfers, shared suppliers, category resets)

These are different audiences for the same data. The store manager cares about their store. The owner cares about the portfolio. A great multi-store product serves both without making either feel like they're fighting the tool.

---
last-compiled: 2026-05-04
needs-review: false

## Tenant Architecture

**Multi-store under one account:**

```
Account (owner)
├── Store A  (its own SOH, task queue, planogram, POS integration)
├── Store B  (same)
└── Store C  (same)

Portfolio analytics (cross-store view):
├── Consolidated sales
├── Cross-store velocity comparison
├── Aggregated exception queue
└── Transfer order management
```

Each store remains fully isolated in its operational data — one store's stockout doesn't automatically trigger a transfer from another store; that requires a deliberate decision. But the owner's Hub shows all three stores simultaneously, with drill-down into any one.

**Data isolation rules:**
- Store A employees see only Store A data (by default)
- Store managers see only their store
- Owner account sees all stores, plus the consolidated portfolio view
- Transfer order events are visible to both the source and destination store

---
last-compiled: 2026-05-04
needs-review: false

## Portfolio Hub — The Owner's Cross-Store Dashboard

The owner with 3 stores opens Canary to a Portfolio Hub:

```
┌──────────────────────────────────────────────────────────────────┐
│  Portfolio View         [Store A ▼] [Store B ▼] [Store C ▼]     │
├──────────────────────────────────────────────────────────────────┤
│  ATTENTION (5 across all stores)                                  │
│  🔴 Store B: Stockout — [Item X] — 0 units, no order pending    │
│  🟡 Store A: Proposed order — [Supplier D] $847 — review now    │
│  🟡 Store C: Delivery overdue — [Supplier E] expected yesterday  │
│  🟡 Store B: 4 tasks outstanding from morning shift              │
│  🔵 All stores: [Item Y] velocity up 40% this week              │
│                                                                   │
│  YESTERDAY PERFORMANCE                                            │
│  Store A: $3,241  ▲8%   Store B: $2,108  ▼3%   Store C: $4,812 ▲12%  │
│  Portfolio total: $10,161  ▲6.4%                                 │
│                                                                   │
│  INVENTORY HEAT (items low across multiple stores)               │
│  [Item Z]: Store A ●●○○○  Store B ●○○○○  Store C ●●●○○         │
│  [Item W]: Store A ●●●○○  Store B ●●○○○  Store C ●○○○○         │
│                                                                   │
│  ORDERS DUE TODAY                                                 │
│  Store A: [Supplier D] — review by noon                          │
│  Store B: [Supplier F] — auto, will send at 10am                │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

**Inventory heat map:** items that are low across multiple stores simultaneously. This is the multi-store replenishment signal — if Item Z is running low everywhere, it's a category issue, not a single-store anomaly. Maybe the supplier had a short delivery. Maybe there's a velocity spike happening market-wide. The owner sees this pattern; a single-store manager cannot.

**Cross-store velocity comparison:** the same item at three stores with very different velocity profiles is a ranging insight. If Item Y sells 3× faster at Store C than Store A, maybe Store A's planogram or location is wrong. The performance disparity is the signal; the investigation and correction is the human decision.

---
last-compiled: 2026-05-04
needs-review: false

## Transfer Orders — Moving Stock Between Stores

When Store B is out of an item and Store A has excess, the owner can initiate a transfer rather than waiting for a supplier order.

**Transfer order flow:**

```
Portfolio Hub → Inventory Heat → [Item Z] detail

  Item Z — Stock by store:
  Store A: 28 units (max: 24, surplus: 4)
  Store B: 0 units  (min: 6, stockout)
  Store C: 18 units (max: 24, adequate)

  Suggested transfer: Store A → Store B | 6 units

  [ Create Transfer Order ]
```

**Transfer order flow:**

```
Transfer Order #T-001
From: Store A | To: Store B
Item: [Item Z] | Quantity: 6 units

Status flow:
  Requested → Accepted (Store A confirms can release) →
  Picked (Store A associate picks 6 units) →
  In Transit →
  Received (Store B associate confirms receipt) → Closed
```

**SOH handling:**
- On "Picked": Store A SOH decremented by 6
- On "Received": Store B SOH incremented by 6
- In Transit: the 6 units are in limbo — not in either store's operational SOH, but tracked in the transfer order record

**Replenishment interaction:** when a transfer is in progress, Store A's replenishment engine knows to exclude the 6 transferred units from its available SOH. Store B's engine knows an inbound transfer is arriving and won't generate a supplier order for the same quantity concurrently.

---
last-compiled: 2026-05-04
needs-review: false

## Shared Supplier Orders — Consolidated Purchasing

A multi-store operator buying from the same supplier across locations has negotiating leverage for volume discounts and delivery consolidation. Canary can generate consolidated orders:

**Consolidated order mode (optional per supplier):**

Instead of three separate orders to Supplier D from three stores, one consolidated order is generated, listing quantities per store. The supplier delivers to each store on their normal schedule, but they receive one order communication.

```
Consolidated PO — Supplier D
Account: [Owner Name]

Deliver to Store A:  [Item A] 36 units, [Item B] 24 units
Deliver to Store B:  [Item A] 24 units, [Item C] 48 units
Deliver to Store C:  [Item A] 48 units, [Item B] 36 units

Total value: $4,218

Submit as: ○ One PO  ● Separate POs per store  ○ Let supplier decide
```

Consolidated ordering is the multi-store operator's volume tool. It requires supplier cooperation (they need to know where each line is going) but it gives the owner a single review point rather than three separate approvals.

---
last-compiled: 2026-05-04
needs-review: false

## Cross-Store Analytics — What Requires Multiple Stores

**Category velocity benchmarking:** for a single store, velocity is an absolute number. For a portfolio, velocity is also a relative number — is this item selling better or worse at Store B compared to Store A? Category performance disparity is a ranging and placement signal that's invisible in a single-store view.

**A/B testing planogram changes:** change the planogram in Store A; keep it the same in Store B and C. After 4 weeks, compare velocity for the affected category across stores. This is a controlled experiment — controlled at the portfolio level. Single-store operators can't do this. Enterprise retailers do it all the time. Multi-store SMB operators have never had the tool for it. Canary makes it trivial.

**Supplier fill rate by store:** if Supplier D consistently short-ships Store B but not Store A, and both are ordering similar quantities, there may be a delivery route issue, a relationship issue, or a store-level problem (difficult receiving dock, late opening). The pattern is visible in the portfolio view; it's invisible if you're only looking at one store.

**Theft/shrinkage patterns:** if Store B consistently has higher shrinkage than Store A and Store C for the same items, that's a security or operational issue specific to Store B. Visible in portfolio analytics; invisible to a store manager who only sees their own store.

---
last-compiled: 2026-05-04
needs-review: false

## Multi-Store Employee Management

**Employee profiles are account-scoped, not store-scoped.** An employee can be assigned to one or more stores. A store manager can be configured to see their store only. The owner sees all stores.

**Floating associates:** some operators have associates who work at multiple locations in a week. Their task history and productivity metrics should aggregate across both stores — not be split into two separate records that the owner has to mentally merge.

**Supervisor permissions by store:**
- Associate: sees their own task queue at their assigned store(s)
- Store Manager: sees full task dashboard and Hub for their store; can create/assign tasks; cannot see other stores
- Owner: sees portfolio view; can act on any store; can override any decision
- Canary Admin: configuration access; no operational data access by default

---
last-compiled: 2026-05-04
needs-review: false

## When to Introduce Multi-Store

The multi-store architecture should be built into the data model from day one — not bolted on. The tenant isolation layer, the portfolio Hub concept, the transfer order schema — these need to be in the data model even if a pilot operator runs only one store.

**What to defer:** the cross-store analytics UI and consolidated ordering workflow are Phase 2 features. The underlying data model (store-scoped SOH, account-level ownership, transfer order entity) is Phase 1 infrastructure.

The moment a second store is added to an account, the portfolio Hub should activate automatically. The operator should not have to do anything special — they add Store B, and the portfolio view appears. If the data model is correct, this is a configuration change, not an engineering project.

---
last-compiled: 2026-05-04
needs-review: false

## The Network Effect Begins at Multi-Store

A single-store operator using Canary generates a private dataset — useful to them, but isolated. A multi-store operator generates a network dataset. When 10 multi-store operators on the same channel are using Canary, the network dataset becomes a category intelligence signal: velocity benchmarks by store type, by geography, by item category, by supplier. No individual operator holds this view. Canary holds it in aggregate (anonymized, not attributable to any single merchant).

This is the long-term network moat: the more stores on Canary, the better the benchmarking, and the more useful Canary is to every store. A solo operator benefits from the velocity benchmarks established by the network. A new store can bootstrap its demand sensing from category benchmarks rather than starting cold.

The network data strategy begins at the moment the second store is added to the first account. The architecture must be designed to support it — opt-in, privacy-preserving, aggregated at the category level. The Canary-as-anonymous-protocol architecture (el jefe agent, custodian of flow) applies here: the network learns without exposing any individual merchant's data.

[[Brain/wiki/cards/store-ops-capability-model]] · [[Brain/wiki/cards/canary-operations-hub]] · [[Brain/wiki/cards/canary-android-pos-integration]] · [[Brain/projects/Canary]]
