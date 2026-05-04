---
last-compiled: 2026-05-04
needs-review: false
type: reference
status: complete
tags: [rdm, retek, wms, warehouse, distribution, canary-context]
created: 2026-05-04
source: Retek Distribution Management V10.0–10.3 scope documents, 2001–2003
---
last-compiled: 2026-05-04
needs-review: false

# RDM — WMS Core Concepts & DC Execution Model

Retek Distribution Management (RDM) is an enterprise warehouse management system covering the full lifecycle of merchandise through a distribution center — from inbound appointment scheduling to outbound trailer loading. Oracle acquired Retek in 2005; RDM became Oracle Retail Warehouse Management System (RWMS). The source corpus here is the V7.1–V10.3 scope documentation, written 2001–2003.

---
last-compiled: 2026-05-04
needs-review: false

## What RDM Is

A DC-level execution system, not a planning system. RDM manages physical inventory movement within four walls — it does not own buying, replenishment parameters, or demand forecasting. Those live upstream in ORMS/RMS and GFO. RDM's job: receive what was ordered, store it correctly, pick what was requested, ship it on time.

**Integration boundary:**

| Upstream | Data sent to RDM | Data returned |
|---|---|---|
| RMS / ORMS | POs, ASNs, item master, supplier data | Receipt confirmations, inventory adjustments |
| OMS / Retek Direct | Customer orders (e-comm / DTC) | Order status, shipped confirmation |
| Labor Management (RLM) | None — RLM bolt-on | Activity history, timing events |
| Host / POS | Store orders, transfers | Shipment confirmation |
| ReIM | Invoice matching | — |
| RIB (Retek Integration Bus) | XML-based all-direction | All |

The Retek Integration Bus (RIB) is the XML middleware layer. All inter-system traffic routes through it. Direct point-to-point is not RDM's model.

---
last-compiled: 2026-05-04
needs-review: false

## Container / License Plate Model

The central organizing concept in RDM is the **container** — a license-plated physical unit (pallet, carton, tote). Every piece of inventory lives inside a container. Every container has a location. Every movement is a container movement.

```
Container
├── License Plate Number (LPN)
├── Location
├── Item(s) + Quantities
├── Status (Receiving / In-Storage / Picked / Packed / Loaded)
└── Parent Container (pallet may hold child cartons)
```

Mixed-SKU pallets are supported natively — a pallet can hold containers of different items. Container consolidation and deconsolidation operations (V8) let the DC merge and split units as needed.

---
last-compiled: 2026-05-04
needs-review: false

## Location Hierarchy

```
DC
├── Zone Group
│   └── Zone
│       └── Location (with Location Type + Location Class)
│           ├── Reserve storage
│           ├── Forward / Active picking
│           ├── Staging (inbound / outbound)
│           ├── WIP processing area
│           └── Shipping / receiving door
```

**Location Type:** physical dimensions (length/width/height/cube), capacity, equipment compatibility.

**Location Class (V10.2):** user-defined grouping by like characteristics — e.g., all refrigerated case-pick locations share a class. Class-level defaults eliminate per-location setup for large location populations.

**Putaway plan:** a sequence of location alternatives for an item. RDM proposes the best-fit location; the user may override (with a warning if the override violates the plan criteria).

---
last-compiled: 2026-05-04
needs-review: false

## Item Hierarchy

```
Department → Section → Class → Item
                                ├── Item Master (attributes, dimensions, hazmat, catch weight)
                                ├── Unit of Measure (Ti × Hi pallet config, inner packs, eaches)
                                ├── Item Class (V10.2 — processing group)
                                └── DC Characteristics (item-level DC config per merch hierarchy)
```

**Ti × Hi:** Tiers × High — pallet build configuration. Ti=12, Hi=5 means 12 cases per layer, 5 layers = 60 cases/pallet. Used for rigid putaway calculations (V10.2), replenishment quantities, and wave cube estimates.

**Catch weights:** items sold by weight rather than unit count (produce, meat, deli). RDM captures actual weight at receiving and/or outbound; transmitted to host for invoice reconciliation. V8 added initial catch weight support; V10.2 enhanced with per-item-class configuration of when to weigh (inbound / outbound / both).

**Item Class (V10.2):** assigns default processing rules — e.g., "high-value items" class enforces outbound QC audit. Processing is then driven by class, not individual item configuration.

---
last-compiled: 2026-05-04
needs-review: false

## Foundation Data Model (V10.2)

The V10.2 "Foundation Basics" release introduced a process-driven distribution engine replacing hard-coded workflow:

```
Item Class + Location Class → Process → Presentation Style
```

- **Process** = a task type (receiving, putaway, case picking, pallet picking, replenishment…) bound to a presentation method (RF screen, label, paper pick sheet)
- **Capture attributes** = data the system collects during the process (serial number, lot number, best-before date)
- **Validate attributes** = data the system forces the user to confirm (scan UPC vs. scan location ID)
- **Match attributes** = constraints that must be satisfied for item→location assignment (REFRIGERATED item can only go to REFRIGERATED location)

This is RDM's version of rules-based warehouse configuration — a significant architectural advance over the V8 era where processes were largely hard-coded.

---
last-compiled: 2026-05-04
needs-review: false

## Data Integrations — Version History

| Feature | Version |
|---|---|
| Web ASN entry + packing slip | V7.1 |
| Catch weights, impact analysis, space utilization | V8 |
| Enhanced returns (RMA), personalization services, order status tracking, e-comm fulfillment | V9 |
| First Time SKU, QA/VA, mixed-SKU pallets, sorter management, outbound audit GUI | V10.0 |
| Top-off replenishment, dynamic overflow, SKU profiling (Streamsoft FlowTrak) | V10.1 |
| Foundation classes, forward case picking, Labor Management (RLM) | V10.2 |
| Concentric putaway, wave-based replenishment, concentric putaway, RF screen sizing | V10.3 |

---
last-compiled: 2026-05-04
needs-review: false

## Canary Relevance

RDM's DC execution model is the operational precedent for Canary's store operations engine. The mappings:

| RDM Concept | Canary Analogue |
|---|---|
| Container / LPN | SKU-level inventory unit tracked through store lifecycle |
| Forward pick location | Active shelf face; display floor |
| Reserve location | Back-stock / receiving area |
| Location class | Store zone definition (produce / refrigerated / general) |
| Item class | Canary merchandise class with default replenishment + handling rules |
| Foundation process engine | Canary workflow engine: task type × presentation (mobile app vs. label vs. report) |
| RIB (integration bus) | Canary MCP junction layer — 166 endpoints, all-direction |
| Ti × Hi | Pack config used in Canary order quantity calculations |
| Catch weight | Produce and deli weight capture at receiving or POS |
| DC audit log | Canary evidentiary rail — every inventory event blockchain-anchored |

**What RDM doesn't do that Canary must:**
- Store-level replenishment (RDM was DC-only; Canary owns DC→Store AND store-level)
- Real-time POS integration (RDM was batch-interface; Canary has live packet-speed feeds)
- Mobile-native UX (RDM used RF handheld terminals with custom screens; Canary is web/mobile first)
- Cost-per-junction billing (RDM had no commercial metering; Canary bills by satoshi per event)

[[Brain/wiki/cards/rdm-inbound-and-receiving]] · [[Brain/wiki/cards/rdm-picking-and-outbound]] · [[Brain/wiki/cards/rdm-task-and-labor]] · [[Brain/projects/Canary]]
