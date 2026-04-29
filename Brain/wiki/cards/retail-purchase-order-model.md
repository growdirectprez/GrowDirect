---
card-type: domain-module
card-id: retail-purchase-order-model
card-version: 1
domain: merchandising
layer: domain
status: approved
agent: ALX
feeds: [retail-three-way-match, retail-receiving-disposition, retail-vendor-scorecard]
receives: [retail-merchandise-financial-planning, retail-replenishment-model, retail-vendor-lifecycle]
tags: [purchase-order, PO, ASN, advance-ship-notice, OTB, vendor-acknowledgment, EDI, receiving]
last-compiled: 2026-04-29
needs-review: false
---

## What this is

The purchase order management model: PO creation, vendor communication, ASN receipt, open-order tracking, and the lifecycle of a purchase commitment from initiation through receipt.

## Purpose

Purchase order management ensures continuous product supply by tracking commitments from order placement through delivery. The PO is the legal commitment that triggers vendor performance obligations, opens the chargeback window, and initiates the three-way match at receipt. Without rigorous PO management, inventory accuracy, vendor accountability, and financial reconciliation all degrade.

## Structure

**PO creation** — Purchase orders are created from three sources: replenishment-generated suggested orders, buyer-initiated direct orders, and allocation-driven store distribution orders. Key PO data elements: vendor, items (with UPC), ordered quantities in eaches, cost per unit (including all applicable allowances), delivery-to location(s), requested delivery date, and ship-not-before/ship-not-after window.

OTB (Open-to-Buy) gates PO creation at the buyer level. A PO that would exceed planned OTB requires authorization override. The OTB check is a hard gate, not a soft warning, for planned purchases; buyers may set soft or hard warnings depending on business rules.

A single PO may have multiple ship-to locations (e.g., direct store delivery to five stores on one truck), enabling vendor consolidation at the purchase commitment level.

**Vendor acknowledgment** — For EDI-capable vendors, the 855 PO acknowledgment confirms vendor acceptance, any item substitutions, and confirmed ship dates. Non-EDI vendors are not required to provide formal acknowledgment. Discrepancy standards for acknowledgment (acceptable date variance, quantity variance) are maintained in vendor management.

**ASN management** — The 856 Advance Ship Notice is the vendor's electronic declaration of what was shipped, in what carton configuration, and when it left the facility. ASN data drives receiving efficiency: the system can pre-stage expected receipts, validate carton contents against the ASN at scan, and detect discrepancies before the physical count is complete. ASN accuracy is a scored vendor compliance dimension.

**Open order tracking** — All open POs are monitored against planned receipt dates. An exception-based view surfaces: orders past their ship-not-after date without an ASN, orders with confirmed ASNs not yet received, and orders with quantities diverging from acknowledgment by more than the defined tolerance.

**PO maintenance** — Quantity, cost, and date changes to open POs require buyer authorization. Changes initiated by the vendor enter through vendor management, not directly into the PO. All changes are version-controlled and audit-trailed.

**PO communication** — POs are transmitted to vendors via EDI 850. Non-EDI vendors receive POs via email or portal. Partners (freight brokers, mixing centers, shipping lines) may also receive PO data when relevant to logistics coordination.

## Consumers

The Replenishment module generates suggested orders that become POs. The Receiving module reads open PO data to validate inbound shipments. The Finance module reads PO cost data for three-way match at invoice. The Vendor Agent updates open PO status when ASNs arrive. The Operations Agent monitors open PO age and surfaces exception reports.

## Invariants

- All external interface feeds (UPC database, vendor pricing) must be validated before a PO is created. A PO with bad item or cost data corrupts the entire downstream chain.
- Base order quantities are in eaches/units. Mixed units of measure are not permitted on a single PO line.
- Vendor PO changes are routed through vendor management — buyers do not accept verbal change requests directly into the PO system.

## Related

- [[retail-merchandise-financial-planning]] — OTB that gates PO creation
- [[retail-replenishment-model]] — the demand-driven source of suggested orders
- [[retail-three-way-match]] — what happens when the ordered goods arrive
- [[retail-vendor-compliance-standards]] — the compliance obligations this PO activates
