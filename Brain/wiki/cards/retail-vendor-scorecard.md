---
card-type: domain-module
card-id: retail-vendor-scorecard
card-version: 1
domain: merchandising
layer: domain
status: approved
agent: ALX
feeds: [retail-chargeback-matrix, retail-vendor-lifecycle]
receives: [retail-vendor-compliance-standards, retail-three-way-match, retail-receiving-disposition]
tags: [vendor, scorecard, performance, KPI, chargeback-trigger, EDI-compliance, fill-rate]
last-compiled: 2026-04-29
needs-review: false
---

## What this is

The vendor performance scorecard: the dimensions, weighting model, and period-based measurement framework that translates vendor compliance data into a composite score used for purchase allocation, renegotiation, and rationalization decisions.

## Purpose

The scorecard converts raw compliance events — a short shipment here, a late ASN there — into a structured performance record that buyers can act on. Without a scorecard, vendor relationship decisions are made on relationships and gut feel. With one, they're made on evidence. The scorecard also defines the chargeback trigger thresholds: poor scorecard performance in a given dimension automatically generates a chargeback at the established administrative fee rate.

## Structure

**Measurement period** — Scorecard runs by month, season, and year. Purchases must be linked to receipts that may cross period boundaries; the scoring methodology must account for this lag.

**Core performance dimensions:**

| Dimension | What it measures |
|-----------|-----------------|
| Fill rate | Units shipped ÷ units ordered, by PO |
| On-time delivery | % of deliveries within agreed delivery window |
| ASN accuracy | % of ASNs that match the physical receipt (quantity, item, UPC) |
| EDI compliance | % of EDI transactions (850, 855, 856, 810) transmitted correctly and on time |
| Invoice accuracy | % of invoices matching PO cost and terms without adjustment |
| Product quality | % of units received meeting acceptance criteria (defect rate below threshold) |
| Carton/marking compliance | % of cartons meeting packing, marking, and unit-load specifications |
| RTV compliance | % of RTV requests resolved within agreed credit timeline |

**Weighting factors** — Each dimension is assigned a relative weight that sums to 100. Weights must be established before any evaluation period begins, agreed with vendor leadership. A retailer with a fragile supply chain might weight fill rate and on-time delivery heavily; one with quality issues might weight acceptance criteria.

**Composite score** — Weighted average of dimension scores produces a single vendor score per period. Composite score drives: (1) purchase allocation — high-scoring vendors receive preferred buying; (2) negotiation posture — score becomes the buyer's opening data point; (3) rationalization candidate list — vendors below a defined threshold for N consecutive periods are flagged for rationalization review.

**Chargeback triggers** — Each compliance dimension has a defined threshold below which automatic chargebacks are generated. The chargeback matrix specifies the administrative fee rate and occurrence escalation logic. The scorecard is the source data; the chargeback matrix is the enforcement mechanism.

## Consumers

Buyers use the scorecard in negotiation sessions and purchase allocation decisions. The Operations Agent monitors scorecard trends and alerts when a vendor approaches a rationalization threshold or a chargeback-trigger threshold. The smart contract layer, for smart-contract-native vendors, encodes scorecard thresholds as on-chain conditions: falling below threshold automatically triggers the contractual consequence without human intervention.

## Invariants

- Scorecard dimensions and weights must be agreed with the vendor before the measurement period begins. Retroactive reweighting is not permitted.
- The scorecard must be run on a consistent schedule — monthly at minimum, with seasonal and annual aggregates. Irregular scoring destroys its credibility in negotiation.
- Purchases linked to cross-period receipts must use a defined methodology (receipt date or PO close date) applied consistently. The methodology must be documented.

## Related

- [[retail-vendor-compliance-standards]] — the clause matrix that defines what is being measured
- [[retail-vendor-lifecycle]] — the lifecycle stage that triggers scorecard evaluation
- [[retail-chargeback-matrix]] — translates scorecard dimension failures into financial consequences
- [[retail-three-way-match]] — the receipt-side data source for fill rate and ASN accuracy
