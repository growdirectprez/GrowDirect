---
last-compiled: 2026-05-04
needs-review: false
type: reference
status: complete
tags: [rdm, retek, wms, warehouse, inbound, receiving, asn, qa, canary-context]
created: 2026-05-04
source: Retek Distribution Management V10.0–10.3 scope documents, 2001–2003
---
last-compiled: 2026-05-04
needs-review: false

# RDM — Inbound & Receiving

The inbound lifecycle in RDM covers the full arc from appointment scheduling through put-to-stock confirmation. This card extracts the business logic and screen-flow patterns relevant for building Canary's receiving and inbound workflows.

---
last-compiled: 2026-05-04
needs-review: false

## Inbound Flow Overview

```
ASN received from vendor (EDI / web entry)
    ↓
Appointment scheduled (dock door, time window, PO/supplier)
    ↓
Truck arrives → door assigned → receiving begins
    ↓
Containers scanned / license plated
    ↓
[QA/VA check if triggered]
    ↓
[First Time SKU processing if new item]
    ↓
Putaway directed → reserve or active location
    ↓
Receipt confirmation transmitted to host (RMS/ORMS)
```

Each step produces an audit event. The receiving record is immutable once confirmed.

---
last-compiled: 2026-05-04
needs-review: false

## ASN (Advance Ship Notice)

The ASN is the supplier's declaration of what is on the truck, at container level.

**V7.1 addition:** Web ASN entry — suppliers could submit ASNs via browser rather than EDI-only. This was a significant reduction in trading-partner onboarding friction for smaller suppliers.

**ASN content:**
- PO number(s) and line items
- Container count and pallet configuration (Ti × Hi)
- Item + quantity per container
- Best-before dates (required for perishable items — V10.2 enforced at ASN entry)
- HAZMAT codes (carried through to outbound labels — V10.2)

**Reuse ASNs (V10.0):** the system can flag an ASN to be reused — useful for standing orders from the same supplier on a recurring delivery schedule without requiring a new ASN each cycle.

**Non-Specified Casepack Receiving (V10.0):** handles scenarios where the received casepack does not match the supplier's declared casepack on the ASN or PO. Previously a hard exception requiring manual override; V10.0 normalized the handling workflow.

---
last-compiled: 2026-05-04
needs-review: false

## First Time SKU Processing (V10.0)

When a new item arrives at the DC for the first time — no existing location assignment, no slotting decision made — RDM triggers the First Time SKU workflow:

1. System flags the container as containing an unslotted item
2. Receiving supervisor is alerted
3. Item is directed to a staging / holding area (not putaway to permanent location)
4. Slotting decision is made (either manually or via SKU profiling — see Streamsoft FlowTrak integration, V10.1)
5. Once slotted, item is assigned to a forward pick location and reserve location
6. Putaway proceeds

Without this flow, a new item arriving for the first time would either block the receiving line or land in a random location with no associated pick logic.

---
last-compiled: 2026-05-04
needs-review: false

## QA / VA Processing (V10.0)

**Quality Assurance (QA):** inspection of inbound merchandise against quality standards.

**Value-Added Services (VA):** tasks performed on merchandise before it reaches the pick face — ticketing, hangtag attachment, security tagging, folding, repackaging.

RDM's QA/VA logic:
- Item or supplier flagged for QA/VA inspection
- On receipt, container is diverted to a WIP processing area (not direct-to-putaway)
- QA: inspector samples a defined percentage; records pass/fail; can disposition to Return-to-Vendor or quarantine
- VA: service code applied; worker completes specified service; container released
- Processing is tracked in the activity log with timing data (input to labor standards)

**V10.0 outbound QC audit (GUI):** separate from inbound QA — a spot-check of outbound containers before loading. Provides a manager-screen audit view of what has been packed, against what was picked. Distinct from the RF-based picking confirmation.

---
last-compiled: 2026-05-04
needs-review: false

## Opportunistic Active Replenishment (V10.0)

When inbound merchandise arrives for an item that is running low in its active (forward pick) location, RDM can interrupt the standard putaway flow and direct the container directly to the active location rather than to reserve first.

Logic:
- On receipt, system checks inventory level in the item's forward pick location
- If below reorder point, the container is flagged as an opportunistic replenishment
- Putaway direction sent to active location instead of reserve
- No separate replenishment task generated — the inbound act IS the replenishment

This eliminates the latency of: putaway to reserve → replenishment task generation → replenishment pick → move to active. For high-velocity items with tight delivery windows, this is significant.

---
last-compiled: 2026-05-04
needs-review: false

## Putaway Algorithms

RDM supports multiple putaway sequencing methods, with increasing sophistication by version:

| Method | Logic | Version |
|---|---|---|
| Standard putaway plan | Ordered sequence of candidate locations; first available wins | Base |
| Putaway by cube | Selects location whose cube most closely matches container dimensions (space utilization) | V8 |
| Alternate putaway sequences | Item can have multiple putaway plans by zone or condition | V10.0 |
| Concentric putaway | Minimizes travel distance: selects location geometrically closest to the item's forward pick face, using 3D coordinate distance formula | V10.3 |
| Rigid dimensions | When Ti × Hi is defined, uses physical dimensions instead of liquid cube for location fit check | V10.2 |

**Concentric putaway algorithm (V10.3):**

```
D = sqrt((x2-x1)² + (y2-y1)² + (z2-z1)²)
```

Starting point = item's forward pick location. All eligible locations scored by distance. Shortest distance wins. Cross-reference-point calculation adds stored inter-reference-point distance when two locations are in different reference zones.

**Override logic:** users may override the suggested putaway location. V10.2 added a warning if the override violates the putaway plan criteria. Override events are logged for audit.

---
last-compiled: 2026-05-04
needs-review: false

## Returns Processing (V9)

Two return types with distinct workflows:

### Customer Returns (DTC / e-comm)
1. **RMA matching:** return matched against original order via RMA number. If no RMA, multi-variable lookup by item / name / postal code
2. **Reason Code:** user-defined why-returned codes (damaged, wrong item, changed mind…)
3. **Action Code:** disposition instruction (Return to Stock / Service & Repair / Liquidate / Return to Vendor)
4. **VA code:** if action requires further processing (repair, repackaging), a VA code routes the item to the correct WIP area
5. **Replacement:** system supports sending replacement item to customer — configurable via system parameter (can be disabled to force OMS-driven replacements only)
6. Return transaction transmitted to OMS with reason, action, and confirmation

### Return to Vendor (RTV)
- Planned (seasonal recall, obsolescence) or unplanned (customer return → vendor)
- Merchandise staged by vendor and merchandise type in RTV area
- Accumulates until location full or time elapsed
- RDM tracks RMA + reason codes for all RTV merchandise
- Inventory inquiry by vendor shows pending RTV containers
- On shipment: documentation generated + host notified

---
last-compiled: 2026-05-04
needs-review: false

## Receiving Business Rules — Key Constraints

- Container must be associated with an ASN / PO before putaway can proceed
- Items flagged for QA/VA cannot be directed to pick locations until cleared
- First Time SKUs held in staging until slotting decision confirmed
- Perishable items require best-before date at ASN entry (V10.2); pre-filled during receiving
- HAZMAT items automatically print hazmat code on all outbound labels generated downstream
- Non-standard casepacks trigger a receiving exception workflow, not a hard stop

---
last-compiled: 2026-05-04
needs-review: false

## Canary Relevance

| RDM Inbound Concept | Canary Analogue |
|---|---|
| ASN web entry | Supplier PO confirmation + expected delivery form in Canary portal |
| First Time SKU | New item onboarding workflow: slotting → active location assignment |
| QA/VA WIP processing | Receiving check: quantity confirm + damage flag + VA service log |
| Opportunistic replenishment | Live inventory check at receiving: if item below floor, direct to floor immediately |
| Reason / Action codes | Canary return processing: configurable reason + disposition lookup |
| Putaway plan | Canary store layout: zone assignment per item with capacity and adjacency rules |
| Concentric putaway | Canary "nearest shelf" putaway suggestion for back-stock → floor moves |
| Audit log | Every receiving event → Canary evidentiary hash on blockchain |

The opportunistic active replenishment pattern is directly usable in Canary's store-level inbound flow: when a truck delivery arrives, check the live store floor against the delivery manifest and route items directly to the floor when the shelf is below display minimum.

[[Brain/wiki/cards/rdm-wms-core-concepts]] · [[Brain/wiki/cards/rdm-picking-and-outbound]] · [[Brain/projects/Canary]]
