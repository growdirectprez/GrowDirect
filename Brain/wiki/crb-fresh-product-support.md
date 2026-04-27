---
title: "CRB Fresh Product Support — Perishables on the RetailSpine"
type: wiki
status: v0.1
tags: [crb, retail-spine, fresh-product, perishables, ornamental-plants, produce, dsd, shrink, ordering, gfo, rapidpos, canary]
created: 2026-04-27
updated: 2026-04-27
related:
  - "[[retail-integration-spine]]"
  - "[[growdirect-the-crdm]]"
  - "[[canary-module-d-distribution]]"
  - "[[canary-module-q-loss-prevention]]"
  - "[[canary-module-p-pricing-promotion]]"
  - "[[Brain/projects/RetailSpine|RetailSpine MOC]]"
last-compiled: 2026-04-27
needs-review: 2026-05-11
---

# CRB Fresh Product Support — Perishables on the RetailSpine

**Governing thesis.** The algorithms that manage perishable landscape and
ornamental plants at SMB retail are structurally identical to those that
manage fresh produce at grocery — short shelf life, velocity-driven
replenishment, shrink as a P&L line, direct-to-store delivery, and a
markdown curve that compresses faster than any other category. Volume
differs by an order of magnitude; the math does not. The Canary Retail
Brain can assert fresh-product support on these shared mechanics and
identify precisely where implementation gaps sit by mapping the perishable
pattern onto the canonical RetailSpine integration surface.

---

## I. The perishable algorithm — shared across ornamentals and produce

Both categories exhibit the same five operational pressures that make
perishable retail hard:

| Pressure | Ornamental / Landscape Plants | Fresh Produce | Algorithm |
|---|---|---|---|
| **Short shelf life** | Days to ~2 weeks depending on species and season | 2–14 days for most fresh lines | Sell-through velocity model; days-on-hand target must stay below life expectancy |
| **No DC buffer** | Grower ships direct to garden center / nursery floor | Grower or packer ships direct to store or DC with sub-24hr dwell | DSD receipt at store; GRN same-day; no warehouse holding cost |
| **Shrink as P&L** | Unsold units die; typical shrink 5–25% | Category shrink 5–20% | Waste tracking as a first-class ledger verb; RTV or write-down at reason-code level |
| **Velocity-driven ordering** | Order to 2–5 days of sell-through; reorder 1–3× per week | Order to days-of-supply target; daily to 3× per week for fast movers | Replenishment = f(velocity, shelf capacity, lead time, shrink rate) |
| **Markdown curve** | Price break at day N to clear before death | Markdown schedule tied to sell-by date | Automated trigger: days remaining / expected velocity < threshold → markdown |
| **Yield variance at receipt** | Count variance; quality rejects at delivery | Weight variance; grade rejects | Receipt-side RTV / quantity adjustment; quality-hold workflow |
| **Seasonal demand** | Spring planting peak; holiday color; fall rotation | Summer peak; holiday basket programs | Seasonal index on forecast; pre-season allocation model |

**Volume difference in context.** A garden center ornamental program runs
50–200 active SKUs with weekly DSD from 3–8 growers. A supermarket produce
department runs 200–800 active PLUs with daily DSD from dozens of
distributors. The model is identical; the parameterization differs.
Industry practice treats ornamental plants and produce as the same
algorithmic bucket — distinct from non-food replenishment — because both
require time-bounded ordering logic that conventional min/max replenishment
cannot safely execute.

---

## II. DEX / NEX — the DSD receipt protocol

DSD deliveries (direct-store-delivery, bypassing the DC) use an electronic
scan-based confirmation protocol at point of receipt:

- **DEX** (Direct Exchange) — serial/RS-232 transport; legacy standard;
  still dominant in produce and beverage DSD
- **NEX** (Network Exchange) — IP-based successor; same message schema,
  different transport layer

Both carry the same payload: PO reference, item-level delivered quantity,
cost extension, supplier invoice number. The store's receiving system
confirms receipt, posts the GRN, and triggers the three-way match
(PO → GRN → invoice). For ornamentals and produce, the DEX session also
carries quality-grade fields and item-level reject counts — the mechanism
for posting a same-day RTV without a separate return authorization workflow.

In the RetailSpine surface, DEX/NEX maps to the **D-prefix + F-prefix
boundary**: direct receipt interfaces (GRN into the stock ledger), purchase
order interfaces (the PO the DEX session validates against), and invoice
acknowledgement (triggering three-way match). The cycle closes at the
reconciled-invoice step.

---

## III. RetailSpine mapping — fresh product interfaces

The canonical retail integration spine covers fresh product without any
category-specific extensions. The fresh-product surface is assembled from
these existing interface families:

### J — Group Forecasting & Ordering (GFO)

GFO is the planning and replenishment nervous system. "Group" refers to the
ordering group — the set of stores and items managed under a shared
replenishment plan. For perishables, GFO parameterization is aggressive:
high-turn targets, short lead times, days-of-supply ceiling tied to shelf life.

| Interface | Role in fresh product |
|---|---|
| **J004** — Sales from POS | Primary velocity signal; daily or intra-day for fast-moving perishables |
| **J009** — Authorised Range + Shelf Capacities | Shelf capacity is the order-quantity ceiling for ornamentals and produce — no backroom buffer exists |
| **J010** — Current Stock On Hand | SOH baseline for replenishment calc; SOH + on-order must not exceed shelf capacity × days-of-supply target |
| **J015** — Sales Forecast | Fresh forecast horizon: 2–7 days; model must incorporate day-of-week, weather index, seasonal coefficient |
| **J017** — Auto-replenishment Order | The replenishment trigger: calculated order → PO → supplier |
| **J019** — Direct Store Order | DSD-route order: bypasses DC, generates the PO the DEX session validates against |
| **J035** — Actual Sales feedback | Closes the forecast loop; actual vs model drives safety-stock and shrink-rate recalibration |
| **J114** — Promotions | Seasonal promotions (spring plant sales, holiday produce displays) must pre-load forecast to avoid stockout on event opening |

### D — Distribution (DSD receipt, RTV, adjustment)

For perishables, D carries three flows that do not exist in non-perishable
categories at the same frequency or urgency:

| Interface | Role in fresh product |
|---|---|
| **D031/D034** — Direct PO Receipt | DSD receipt: GRN posted same-day; triggers stock ledger update and invoice match initiation |
| **D030/D032/D035** — Return to Vendor | Quality rejects at receipt; posts in the same DEX session as the receipt; updates vendor compliance metrics |
| **D019/D020/D033** — Inventory Adjustment | Daily write-downs for unsold perishables at end of shelf life; reason codes: WASTE, EXPIRED, MARKDOWN-CLEARANCE |
| **D021/D022/D029** — Cycle Count | High-frequency for perishables (daily or shift-level); establishes shrink baseline for loss prevention |

### S — Space, Range & Display

Shelf capacity is not optional metadata for perishables — it is the
maximum order quantity, enforced at the replenishment trigger. A planogram
allocating N linear feet to an ornamental category defines a hard ceiling
on what can be ordered without creating an overflow condition.

| Interface | Role in fresh product |
|---|---|
| **S003/S082** — Historical Sales + Waste | Waste is a first-class field alongside sales; margin calculation includes shrink-adjusted COGS |
| **S047** — Store Range + Capacity → Planning | Shelf capacity flows into the replenishment model as the order-quantity ceiling |
| **S075** — Capacity Information | Per-store constraints (floor space, cooler capacity for cut flowers / refrigerated produce) |

### F — Finance (procure-to-pay for DSD)

| Interface | Role in fresh product |
|---|---|
| **F001** — Purchase Order | DSD PO issued before delivery window; supplier's DEX session keys off this reference |
| **F013** — PO Acknowledgement | Confirms delivery quantity; starts the supplier invoice clock |
| **F004** — Supplier Invoice | DEX-confirmed quantities become the invoice basis |
| **F014** — Reconciled Invoice | Closes three-way match; RTV quantity deductions post as invoice credits |

---

## IV. Canary / CRB spine — implementation status for fresh product

Canary is an SMB merchant analytics platform built on Square POS data.
Fresh product support maps to the following implementation state:

| Domain | RetailSpine surface | Canary status | Fresh-product coverage |
|---|---|---|---|
| **Sales velocity** | J004 | **Live** — Square ingestion, transaction model, Identity engine | Full; intra-day velocity available via Square webhook |
| **Shrink / Loss Prevention** | D019/D033 (adj), D021 (cycle count), J010 (SOH) | **Designed** — Module Q, Module D; no code yet | Shrink detection logic designed; adjustment and cycle-count verbs projected |
| **DSD Receipt** | D031/D034, F001/F013 | **Designed** — Module D receipt service projected; no code yet | DEX/NEX session validation not yet specified; PO receipt workflow projected |
| **Replenishment / Ordering** | J017/J019, J015 | **Not yet designed** | **Priority gap:** replenishment trigger and forecast model not implemented |
| **Shelf capacity as order ceiling** | S047/S075, J009 | **Partially designed** — Module S carries planogram capacity; not wired to ordering | Order-ceiling logic: designed in S, not connected |
| **Markdown trigger** | P-prefix, C010 | **Partially live** — Module P has promotion detection; perishable markdown rule not implemented | Markdown curve for perishables: undesigned gap |
| **Vendor performance / RTV** | D030/D035, J097 | **Not designed** | RTV workflow and quality-reject tracking not in current scope |
| **Seasonal forecast** | J015, J114 | **Not designed** | Seasonal index and promotional pre-load not in current forecast model |
| **Waste accounting** | S003/S082 | **Not designed** | Waste as a ledger verb with COGS impact not yet in stock-ledger model |

### Three gaps that block credible fresh-product claims

**1. Replenishment trigger** (J017/J019 analog).  
Canary has no ordering module. For perishables, the calculation is:

```
order_qty = max(0, (daily_velocity × lead_days × safety_factor) - (SOH + on_order))
```
capped at `shelf_capacity`. This is a small, well-defined function that
belongs in a new Canary module or as an extension of Module D.

**2. Waste as a first-class ledger verb** (D019 analog, reason = WASTE/EXPIRED).  
Module D projects a generic inventory-adjustment verb. Perishable waste
needs a distinct reason-code family separating shrink-to-expiry from theft
from damage — because the P&L treatment and the loss-prevention signal
are categorically different.

**3. Markdown trigger** (P-prefix extension).  
A rule engine that compares days-remaining-to-shelf-life against current
sell-through rate and fires a price reduction when the item will not clear
at current velocity. Currently undesigned. Rule form:

```
if (days_remaining × daily_velocity) < current_SOH → trigger markdown_schedule[n]
```

---

## V. RapidPOS SMB context

RapidPOS is a representative POS substrate for garden center and nursery
merchants in the Square ecosystem. The Canary integration surface for these
merchants:

| Touchpoint | Data flow | Canary status |
|---|---|---|
| POS transactions | Square webhook → Canary sales ingestion → velocity model | **Live** |
| DSD receipt | Vendor delivers plants → receiving clerk accepts/rejects → DEX session (or manual entry) → GRN → stock ledger | Module D receipt service projected; not built |
| Daily shrink write-down | End-of-day unsold perishables → WASTE-EXPIRED adjustment → stock ledger | Adjustment verb designed; WASTE reason-code family needed |
| Reorder | Velocity-based order calculation → supplier contact → new DSD PO | **Gap — not designed** |
| Markdown clearance | Days-remaining rule → price reduction → clearance scan | Rule engine not designed |

**Volume does not change the architecture.** A garden center running 100
plant SKUs with 2× weekly DSD from 4 growers generates ~800 DSD receipt
lines per week. The model is identical; the batch size differs. Canary's
event-driven architecture (Square webhook → Valkey stream → worker) handles
both without structural change.

---

## VI. What CRB can claim today vs. what requires the roadmap

| Claim | Status |
|---|---|
| Real-time sales velocity for perishable categories | ✅ Live |
| Shrink / loss detection via inventory discrepancy | 🔧 Designed, not built |
| DSD receipt and GRN posting | 🔧 Designed, not built |
| Vendor quality tracking and RTV | ❌ Not yet designed |
| Velocity-based replenishment trigger | ❌ Not yet designed — priority gap |
| Perishable markdown rule | ❌ Not yet designed |
| Waste as COGS-impacting ledger verb | ❌ Not yet designed |
| Shelf-capacity-constrained ordering | 🔧 Capacity designed in S; order connection missing |
| Seasonal demand index | ❌ Not yet designed |

CRB can credibly claim the velocity and loss-detection surface today.
The replenishment, markdown, and waste-accounting claims require the
three priority gaps to be closed — collectively a well-scoped module
addition to Canary v2, not a structural rearchitecture.

---

*v0.1 — 2026-04-27 | GrowDirect Inc.*
