---
title: Canary Retail Spine — L1–L4 Process Decomposition
tags: [modules, spine, counterpoint, l1-l4]
---

# Canary Retail Spine on the NCR Counterpoint Backbone
## L1–L4 Process Decomposition

The Canary Retail Spine is a 13-module ARTS-native operating layer. On a Counterpoint substrate, each module maps to specific Document types, API endpoints, and vertical adaptations. This index presents the full four-level hierarchy.

| Level | What it represents |
|---|---|
| **L1** | Business domain (RBIS-derived: Customer, Products & Services, Merchandising, Store Ops, Corporate Finance, Workforce) |
| **L2** | Canary module (one of 13 ARTS-prefixed modules: T, R, N, A, Q, C, D, F, J, S, P, L, W) |
| **L3** | Process group within the module |
| **L4** | Activity → Counterpoint endpoint → L&G-specific adaptation |

**Coverage key:** ● Full direct  ◐ Partial (gap = Canary-native)  ★ Canary native (no Counterpoint analog)

---

## L1: Store Operations Management

### L2: Q — Loss Prevention ★ Canary native

> Counterpoint exposes the full audit substrate (drawer sessions, voids, discount reasons, pricing decisions). Q adds the detection layer. No Counterpoint analog exists.

| L3 Process group | L4 highlights | L&G adaptation |
|---|---|---|
| Q.1 Substrate ingestion | `PS_DOC_HDR`, `PS_DOC_LIN`, `PS_DOC_PMT` | Live-goods DOC_TYP allow-list; cash vendor receipts excluded from monitoring scope |
| Q.2 Detection rule execution | 23 rules across 10 families; Chirp engine | Mix-and-match pricing (`MIX_MATCH_COD`) suppresses discount-abuse false positives |
| Q.3 Detection lifecycle | Alert → Owl triage → Fox case | Seasonal staff spike raises baseline; per-season threshold tuning required |
| Q.4 Tuning & allow-list management | Per-tenant rule weights, category exclusions | 5 garden-center allow-lists: cash vendor pay, fractional units, dead-count write-offs, mix-match pricing, ad-hoc vendor onboarding |
| Q.5 Investigator & analyst surface | Owl NL query + Fox case dashboard | Store GM primary actor; LP analyst secondary |
| Q.6 Vertical configuration | L&G allow-list bundle as named preset | Pre-configured at tenant onboarding; VAR deploys in under 1 hour |
| Q.7 Deployment phasing | Observer → alert → case — no Counterpoint write-back | Phase 1: read-only observe; Phase 2: GM alert; Phase 3: Fox case auto-open |

→ [Full Q article](Q-loss-prevention)

### L2: N — Device ● Full

> Counterpoint exposes workstation and station identifiers on every Document. N builds the device registry and telemetry surface.

| L3 Process group | Counterpoint source |
|---|---|
| N.1 Device discovery | `STA_ID`, `WRK_STA_ID` on PS_DOC_HDR |
| N.2 Device telemetry | Transaction velocity, error rates per station |
| N.3 Device anomaly detection | Feeds A (Asset Management) bubble layer |

→ [N stub](N-device)

### L2: A — Asset Management ◐ Design pending

> Anomaly detection engine over the N device registry. Implementation pending v1 shipping.

→ [A stub](A-asset-management)

---

## L1: Merchandising Management

### L2: D — Distribution ◐ Partial

> Counterpoint per-location inventory snapshots are direct. Transfer workflow routes through Document omnibus (DOC_TYP=XFER). Transfer-loss detection and multi-store distribution recommendations are Canary-native gaps.

| L3 Process group | L4 highlights | L&G adaptation |
|---|---|---|
| D.1 Inventory snapshot ingestion | `Inventory_ByLocation`, `Items_ByLocation`, `InventoryLocations` | Item-code drift normal; adapter tolerates multiple ITEM_NO for same plant |
| D.2 Per-location item attribution | `InventoryCost`, `InventoryControl` | Variable cost basis (multiple growers, same plant) — weighted average cost logic |
| D.3 Transfer detection (XFER) | `DOC_TYP=XFER` via Document omnibus | Fractional unit transfers (partial flats) require QTY rounding rules |
| D.4 Transfer-loss reconciliation ★ | Canary-native: shipped QTY vs received QTY delta | Live-goods shrink in transit is a primary L&G loss vector |
| D.5 Multi-store distribution recommendations ★ | Demand signal (T) + inventory position (D.1) → rebalance suggestion | Rebalance logic weather-adjusted in peak season; spring inventory concentration risk |
| D.6 Substrate contracts | 9 contracts to downstream modules (Q, F, J) | — |

→ [Full D article](D-distribution)

### L2: J — Forecast & Order ◐ Partial

> Counterpoint covers PO/PREQ/RECVR/RTV via Document family. Demand forecasting, replenishment parameters, and OTB management are Canary-native gaps.

| L3 Process group | L4 highlights | L&G adaptation |
|---|---|---|
| J.1 Demand forecasting ★ | Canary-native; Counterpoint has no forecast endpoint | Weather-adjusted seasonal model; spring revenue 40-60% of annual — base forecast must isolate seasonality |
| J.2 Replenishment parameters ★ | Min/max, lead time, safety stock per SKU-location | SKU lifecycle short and seasonal; catalog not stable; ad-hoc new items mid-season |
| J.3 Open-to-Buy management ★ | OTB pyramid: plan → commit → receipt; Canary enforces guardrails | OTB critical during spring build — cash flow negative in winter shoulder; spring overbuy risk is real |
| J.4 PO recommendation + approval | Canary plan → buyer approval → Counterpoint PO | Buyer-in-Counterpoint-UI default (v2); Canary POST-back optional (v3+) |
| J.5 PO generation + transmission | `DOC_TYP=PO` via Document POST or buyer UI | Large nurseries: EDI-capable; mid-tier: PDF/email; hobbyist: cash-and-paper — three vendor tiers |
| J.6 Receiving + 3-way match | `DOC_TYP=RECVR`; PO qty vs receiver qty vs invoice | Receiver with thin metadata (paper invoice) is normal — flag-and-ingest, not reject |
| J.7 Short-ship + RTV | `DOC_TYP=RTV` | Live-goods RTV (dead-on-arrival plants) creates specific RTV pattern; distinguish from standard merchandise RTV |
| J.8 Promotional demand isolation | Cross-module contract with P (Pricing & Promotion) | Spring promotion lift must be quarantined from next-year base or replenishment double-orders |

→ [Full J article](J-forecast-order)

### L2: S — Space, Range, Display ◐ Design complete

> Assortment gatekeeper: no item enters a PO without S clearance. Counterpoint Item master is the substrate.

→ [S stub](S-space-range-display)

### L2: P — Pricing & Promotion ◐ Publisher

> Reads Counterpoint pricing tables; publishes price and markdown events to the ledger.

→ [P stub](P-pricing-promotion)

---

## L1: Products & Services Management

### L2: T — Transaction Pipeline ● Full direct

> Primary ingest module. Every detection (Q), customer record (R), and ledger movement (D/F) traces back to a T write. Counterpoint Document family: 11 endpoints.

| L3 Process group | L4 highlights | L&G adaptation |
|---|---|---|
| T.1 Adapter ingress | Poll-only (no webhook); Document omnibus GET | Counterpoint poll cadence: 60s steady-state; 15s during active store hours |
| T.2 Sealing & integrity | Raw-bytes hash chain; immutable CRDM write | — |
| T.3 Provider-keyed parsing | `DOC_TYP` routing: SALE/RTRN/VOID/XFER/PO/RECVR/RTV → CanonicalEvent | Live-goods write-off DOC_TYP TBD (ASSUMPTION-T-07); verify against real garden-center data |
| T.4 Canonical event publication | Dispatch to R, N, S, F, D, J, Q modules | — |
| T.5 Merkle anchoring | Batch tree; anchor cadence per tenant config | — |
| T.6 Replay, backfill & idempotency | Watermark per `(tenant, entity)`; idempotent on DOC_ID | — |
| T.7 Cross-module substrate contracts | 12 contracts; Q.1 is primary consumer | — |

→ [Full T article](T-transaction-pipeline)

### L2: R — Customer ● Full (v1 minimal)

> Privacy-bounded customer registry from Counterpoint Customer records.

→ [R stub](R-customer)

---

## L1: Corporate Finance Management

### L2: F — Finance ◐ Reconciler + publisher

> 3-way match reconciler; publishes GL events. Counterpoint AR/AP surface is the substrate.

→ [F stub](F-finance)

### L2: C — Commercial ◐ Publisher

> B2B commercial intelligence: landscaper/wholesale account risk, credit posture, tier pricing. Counterpoint `CATEG_COD` + AR fields.

| L3 (key) | L&G relevance |
|---|---|
| C.2 B2B account risk scoring | Landscaper accounts = 20–40% of L&G revenue; Counterpoint surfaces tier pricing, not credit risk |
| C.3 Cost-update publishing | Vendor cost changes from RECVR feed into COGS ledger |

→ [C stub](C-commercial)

---

## L1: Workforce Management

### L2: L — Labor & Workforce ◐ Design complete

> Labor scheduling and time-entry. Counterpoint has no labor endpoint; integration via Homebase/Deputy/TimeForge or Canary-native (strategic decision pending).

| L&G note |
|---|
| Peak-season labor demand is 2–4x baseline. Part-time/seasonal staff spike. L module priority elevated vs steady-demand verticals. |

→ [L stub](L-labor-workforce)

### L2: W — Work Execution ◐ Capstone (design complete)

> Cross-domain capstone: task orchestration, execution audit, reconciliation across all other modules.

→ [W stub](W-work-execution)
