# Bull — Distribution Intelligence (Module D Native Layer)

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]
**Module card:** [[Brain/wiki/canary-module-d-distribution|Module D Functional Decomposition]]
**CRB:** [[GrowDirect-CRB/modules/D-distribution|D Distribution]]
**Status:** Phase 3 — design complete, implementation gated on Module D substrate

## Purpose

Bull is the Canary-native intelligence layer for Module D (Distribution). It covers the two L2 process areas that have no Counterpoint analog: **D.4 Transfer-loss reconciliation** and **D.5 Multi-store distribution recommendations**. Counterpoint exposes rich per-location inventory snapshots and transfer documents via the Document omnibus (DOC_TYP=XFER), but it does not reconcile what was lost in transit or recommend cross-location stock rebalancing. Bull closes that gap.

Bull is to Module D what Chirp is to Module Q — the Canary-native detection and recommendation engine built on substrate that the POS provides but doesn't analyze.

## Phase Gating

Bull is **not buildable** until the following prerequisites are operational:

| Prerequisite | SDD | Status |
|---|---|---|
| T.1 Counterpoint adapter ingress (poll-based) | `ncr-counterpoint-tsp-adapter.md` | Phase 1 — in progress |
| T.3.2 DOC_TYP type-routing (XFER → D subscriber) | `tsp.md` §T.3, `ncr-counterpoint-tsp-adapter.md` | Phase 1 — in progress |
| T.4.6 Transfer event publication to D | `tsp.md` §T.4 | Phase 1 — in progress |
| D.1 Inventory snapshot ingestion | `ncr-counterpoint-inventory-adapter.md` | Phase 2 — planned |
| D.2 Per-location item attribution | `ncr-counterpoint-inventory-adapter.md` | Phase 2 — planned |
| D.3 Transfer detection (XFER Documents) | Module D service layer | Phase 2 — planned |

**Critical dependency chain:** T adapter → T.3.2 type-routing → T.4.6 XFER publication → D.3 transfer detection → Bull (D.4 + D.5).

## Expected Interfaces

### D.4 — Transfer-Loss Reconciliation

| Interface | Description |
|---|---|
| **Input:** D.3 XFER-RECVR document pairs | Matched transfer-initiation and receiving documents |
| **Input:** D.1 inventory snapshots (pre/post transfer) | SOH deltas around transfer events |
| **Output:** TRANSFER-VARIANCE records | Per (XFER, item) variance with match-confidence flag |
| **Output:** Systematic loss patterns | Per-route aggregated variance trends |
| **Output:** Q-IS-03 accumulation feed | Transfer-loss detections routed to Chirp's Q-IS-03 rule |
| **Output:** UNATTRIBUTED-MOVEMENT events | SOH deltas not explained by any Document |

### D.5 — Multi-Store Distribution Recommendations

| Interface | Description |
|---|---|
| **Input:** D.1 per-location SOH | Current stock position per (item, location) |
| **Input:** O.2 ROP + safety stock targets | Demand-derived reorder points |
| **Output:** Excess/deficit matching | Location pairs where transfer is cheaper than new PO |
| **Output:** Transfer recommendations with OTB context | Scored by transfer-cost vs replenishment-cost |
| **Output:** Buyer review queue | Same approval UX pattern as O.4 PO recommendations |

### MCP Tools (planned — `canary-bull` server)

| Tool | Description |
|---|---|
| `get_transfer_variance` | Per-XFER variance detail with match confidence |
| `list_transfer_losses` | Aggregated loss by route, item, or time window |
| `get_distribution_recommendations` | Excess/deficit matches ranked by savings |
| `approve_transfer_recommendation` | Buyer accepts/modifies/rejects a rebalancing suggestion |
| `get_unattributed_movements` | SOH deltas not explained by known Documents |

### Cross-Module Contracts

| Contract | Consumer | What Bull promises |
|---|---|---|
| D.6.3 TRANSFER-VARIANCE | Q (Q-IS-03), F (cost reconciliation) | Variance per XFER-RECVR pair with match-confidence flag |
| D.6.4 In-transit hold | J (on-order), C (OTB) | In-transit NOT counted as available-for-sale |
| D.6.5 UNATTRIBUTED-MOVEMENT | Q, F | Every unexplained SOH delta named, not dropped |
| D.6.9 In-transit timeout | Operations | 72h (configurable) timeout alert on unconfirmed transfers |

## Schema (stub — not yet in migration)

Bull tables will live in `app` schema alongside Hawk. Expected tables:

| Table | Purpose |
|---|---|
| `bull_transfer_variances` | Per-XFER-item variance records with match_confidence |
| `bull_unattributed_movements` | SOH deltas not explained by Documents |
| `bull_distribution_recommendations` | Rebalancing suggestions with scoring |
| `bull_transfer_costs` | Per-route configurable transfer costs |

Schema will be added in a dedicated Alembic migration when Phase 3 development begins.

## Garden-Center Operating Context

Bull's design is heavily informed by garden-center operating reality (see `Brain/wiki/garden-center-operating-reality.md`):

- **End-of-season consolidation:** Large transfers from seasonal stores to main warehouse with expected live-goods spoilage. D.4.6 allow-list prevents these from flooding Q-IS-03.
- **Undocumented transfers:** Some L&G operators move stock between locations without creating Counterpoint XFER Documents. D.4.4 detects these as UNATTRIBUTED-MOVEMENT events — a high-value signal, not just an edge case (ASSUMPTION-D-09).
- **Live-goods transfer loss:** Plants that die in transit are a cost, not theft. Bull must distinguish spoilage-in-transit from pilferage-in-transit using seasonal baselines.

## Assumptions Inherited from Module D Card

| ID | Assumption | Resolution path |
|---|---|---|
| ASSUMPTION-D-03 | Transfer completion confirmed via RECVR Document | Sandbox workflow test |
| ASSUMPTION-D-04 | DOC_TYP=XFER is the correct code for store-to-store transfers | Sandbox workflow test |
| ASSUMPTION-D-06 | Transfer cost per route not stored in Counterpoint | Customer interview |
| ASSUMPTION-D-09 | Undocumented transfers are a known L&G practice | Customer interview |

## Production Readiness

- [x] Design complete — D.4 and D.5 L2/L3 processes defined in Module D functional decomposition
- [x] Cross-module contracts documented — D.6.3–D.6.9
- [x] Assumption markers identified — 4 blocking, all resolution-pathed
- [ ] Schema migration — **gated on Phase 3 start**
- [ ] Service layer — **gated on Phase 3 start**
- [ ] MCP tools — **gated on Phase 3 start**
- [ ] Contract tests against T.4.6 XFER routing — **gated on T adapter shipping**

---
*Canary LP | GrowDirect LLC | Confidential*
