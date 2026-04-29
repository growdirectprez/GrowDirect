---
card-type: domain-module
card-id: retail-three-way-match
card-version: 1
domain: finance
layer: domain
status: approved
agent: ALX
feeds: [retail-chargeback-matrix, retail-inventory-valuation-mac, retail-ap-vendor-terms]
receives: [retail-purchase-order-model, retail-receiving-disposition]
tags: [three-way-match, receiving, invoice, PO, ASN, discrepancy, finance, AP, inventory]
last-compiled: 2026-04-29
needs-review: false
---

## What this is

The three-way match: the reconciliation of Purchase Order, Advance Ship Notice, and physical Receipt that gates invoice approval and triggers chargeback events when discrepancies are found.

## Purpose

The three-way match is the financial control point at the intersection of purchasing, receiving, and accounts payable. It verifies that what was ordered (PO), what the vendor said they shipped (ASN), and what the retailer physically received (Receipt) all agree before an invoice is approved for payment. Discrepancies between any two of the three documents trigger specific financial consequences — chargebacks, deductions, or credits — rather than being resolved informally.

## Structure

**The three documents:**

| Document | Source | Key data |
|----------|--------|----------|
| Purchase Order (PO) | Buyer/replenishment system | Item, ordered qty, PO cost, delivery location, delivery window |
| Advance Ship Notice (ASN) | Vendor via EDI 856 | Item, shipped qty, carton configuration, ship date, carrier |
| Receipt | Receiving system at DC or store | Item, received qty, condition, receipt date, receiving method |

**Match logic** — A complete three-way match requires all three documents to agree within defined tolerances on item identity, quantity, and timing. The sequence of comparisons:

1. **PO vs. ASN** — Vendor shipped what was ordered? Item substitutions, quantity overages/underages, and missing items are flagged. An ASN that does not reference a valid open PO is rejected.

2. **ASN vs. Receipt** — Physical receipt matches what vendor said was shipped? Carton count variance, inner pack discrepancies, and missing shipments are flagged. This comparison also validates ASN accuracy for the vendor scorecard.

3. **PO vs. Receipt** — Combined: did the retailer receive what it ordered, at the ordered cost? Quantity variance drives short-shipment chargebacks. Cost variance drives invoice deductions.

**Receiving methods and confidence levels** — Three receiving methods produce the Receipt document, each with different accuracy confidence:

- **Assumed receiving** — Receipt accepted as equal to the ASN without physical count. High throughput, low accuracy. Used for trusted high-compliance vendors with strong ASN track records. Retrospective audits validate assumption accuracy.
- **Outer-case scan** — Carton barcodes scanned; inner pack counts are assumed from item master. Medium confidence. Efficient for high-volume standard-pack items.
- **Manual count** — Full unit-level count of all received items. Highest accuracy, highest cost. Required for high-value items, first shipments from new vendors, or vendors with poor ASN compliance history.

**Discrepancy handling** — Discrepancies between PO, ASN, and Receipt fall into categories: shortage (received less than invoiced), overage (received more), substitution (different item), damage (units received in unacceptable condition), and timing violation (received outside the delivery window). Each category maps to a defined chargeback type in the chargeback matrix.

**Invoice approval gate** — An invoice is approved for payment only when the three-way match is complete within tolerance. Invoices with open discrepancies are held. The AP module generates debit memos for deductions before releasing payment. Invoice hold aging is monitored to avoid vendor relationship damage from unexplained holds.

## Consumers

The Finance/AP module executes the match and holds invoices on discrepancy. The Vendor Agent records match results as compliance events in the vendor scorecard. The Inventory module updates on-hand quantities based on confirmed receipt. The Operations Agent monitors match failure rates by vendor and surfaces vendors where match failure is systematic rather than episodic.

## Invariants

- Every invoice payment must be gated on a completed three-way match. Paying on invoice alone removes all chargeback leverage.
- Discrepancy tolerance thresholds (acceptable quantity variance %) are maintained in vendor management, not set ad hoc by the receiving team.
- All three documents must reference the same PO number as the common key. Orphaned receipts (no PO) and phantom invoices (no receipt) are exception alerts, not normal process outcomes.

## Related

- [[retail-purchase-order-model]] — the PO that anchors the match
- [[retail-receiving-disposition]] — the operational response to quality discrepancies at receipt
- [[retail-chargeback-matrix]] — the financial consequences of match failures
- [[retail-ap-vendor-terms]] — the invoice approval and payment process that the match gates
- [[retail-inventory-valuation-mac]] — MAC update triggered by confirmed receipts
