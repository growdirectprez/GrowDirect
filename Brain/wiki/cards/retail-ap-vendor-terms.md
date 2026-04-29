---
card-type: domain-module
card-id: retail-ap-vendor-terms
card-version: 1
domain: finance
layer: domain
status: approved
agent: ALX
feeds: [retail-operations-kpis]
receives: [retail-three-way-match, retail-chargeback-matrix, retail-inventory-valuation-mac]
tags: [AP, accounts-payable, vendor-terms, settlement, net-30, net-45, EDI, invoice-matching, discount-terms]
last-compiled: 2026-04-29
needs-review: false
---

## What this is

The accounts payable and vendor terms model: how vendor invoices are validated, how payment terms are structured, how deductions and allowances are settled, and how EDI enables a scalable, paperless AP process.

## Purpose

AP vendor terms management closes the procurement-to-payment cycle. A well-run AP process captures all earned discounts, enforces all chargeback deductions, and maintains vendor relationships through predictable, accurate payment behavior. A poorly run AP process leaves earned discounts uncaptured, pays invoices before three-way match is complete, and generates vendor disputes that cost more to resolve than the amounts in question. AP is where the financial value of vendor compliance standards is either captured or lost.

## Structure

**Payment terms** — Standard payment terms are negotiated at vendor setup and maintained in the vendor master. Common structures:

| Term | Definition |
|------|-----------|
| Net 30 | Full invoice amount due 30 days from invoice date |
| Net 45 | Full invoice amount due 45 days from invoice date |
| 2/10 net 30 | 2% discount if paid within 10 days; full amount due at 30 days |
| Net EOM | Full amount due at end of the month following invoice |
| Consignment | Payment made only on units sold, not on receipt |

**Invoice approval gate** — Invoices are approved for payment only after the three-way match (PO × ASN × Receipt) is complete within tolerance. An invoice without a matching receipt is held — not rejected, but quarantined. The hold aging is monitored: invoices held longer than the discount window are flagged, as a hold that prevents a 2% early payment discount carries a real cost.

**Deduction process** — All chargeback deductions, allowance claims, and discount adjustments are applied to the invoice before payment release. The AP module generates a debit memo for each deduction, referencing the original PO, receipt event, and compliance clause. The vendor-visible remittance advice itemizes all deductions so the vendor can reconcile without dispute.

**EDI AP workflow** — EDI-capable vendors use the 810 (invoice) transaction. The 810 is matched electronically against the PO (850) and receipt. Matched invoices within tolerance auto-approve for payment on terms. Exception invoices go to a work queue for human review. EDI AP eliminates paper invoice handling and reduces AP headcount requirements for high-volume vendor relationships.

**Subsequent settlement** — Beyond the invoice itself, the AP process handles post-receipt financial adjustments: volume rebate settlements (typically annual), promotional allowance claims (post-event), markdown allowance credits, and freight variance settlements. These are processed as separate debit or credit memos against the vendor account, with full reference to the originating events.

**Centralized AP structure** — Best practice is to centralize the AP function with a multi-functional staff organized around commodity categories (so AP staff understand the business context of their vendor relationships) and co-located with purchasing. Centralized AP enables consistent policy enforcement, volume-based negotiating leverage, and consolidated vendor performance tracking.

**Performance benchmarks** — Historical benchmarks for AP operational efficiency:

| Metric | Best practice target |
|--------|---------------------|
| Invoice processing cycle time | 3–5 days from receipt to approval |
| % invoices processed via EDI | 70%+ for high-volume vendors |
| Discount capture rate | 95%+ of available early payment discounts |
| Invoice exception rate | < 5% requiring manual resolution |

## Consumers

The Finance module executes payment runs on approved, matched invoices. The AP Agent applies deductions from the chargeback matrix and allowance tracking. The Vendor Agent reads payment history as a vendor relationship health indicator. The Operations Agent monitors discount capture rate and invoice hold aging as financial efficiency KPIs.

## Invariants

- No invoice is released for payment without a completed three-way match. The match is the gate, not a recommendation.
- All deductions must be itemized on the remittance advice with the originating event reference. Unexplained deductions generate vendor disputes regardless of their legitimacy.
- Discount window timing starts from invoice date, not receipt date. AP must track both to ensure discount capture.

## Related

- [[retail-three-way-match]] — the match that gates invoice approval
- [[retail-chargeback-matrix]] — the deduction taxonomy applied before payment release
- [[retail-inventory-valuation-mac]] — subsequent settlement adjustments flow back into MAC through allowance credits
- [[retail-vendor-lifecycle]] — payment terms established in vendor setup govern the AP process
