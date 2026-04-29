---
card-type: domain-module
card-id: retail-vendor-lifecycle
card-version: 1
domain: merchandising
layer: domain
status: approved
agent: ALX
feeds: [retail-vendor-scorecard, retail-vendor-compliance-standards, retail-purchase-order-model, retail-chargeback-matrix]
tags: [vendor, supplier, lifecycle, onboarding, rationalization, discontinuation, retail-ops]
last-compiled: 2026-04-29
needs-review: false
---

## What this is

The end-to-end lifecycle for a retail vendor relationship: from initial selection and setup through active partnership management to rationalization or discontinuation.

## Purpose

Vendor lifecycle management exists to maximize profit and sales through disciplined supplier relationships. The lifecycle governs which vendors the retailer commits to, what standards they must meet, how performance is measured, and under what conditions the relationship ends. Without a defined lifecycle, vendor sprawl accumulates, compliance gaps go unmeasured, and chargeback rights erode.

## Structure

The vendor lifecycle has seven stages:

**1. Select Vendor** — Evaluate candidates against a defined matrix: product quality, pricing, availability, RTV policy, carton and packing standards, routing and transportation compliance, EDI capability, co-op and rebate terms, and marketing support. Assign relative importance weights before any evaluation begins.

**2. Set Up Vendor** — Establish vendor master record with all terms, compliance standards, payment terms, and EDI parameters. Record agreed-upon compliance standards in vendor management, not informally. Vendor guidelines must cover accounting, traffic, store, and warehouse compliance.

**3. Define Vendor Guidelines** — Document the compliance standards that govern the ongoing relationship. These include: product quality acceptance criteria, availability commitments, net pricing terms, RTV policy, carton quality and marking standards, unit load specifications, transportation and routing requirements, discount and rebate schedules, co-op and marketing support, and shared forecast obligations. These are the clauses that chargebacks enforce.

**4. Evaluate Performance (Scorecard)** — Run the vendor scorecard by period (month, season, year). Dimensions cover all facets of the supply chain: fill rate, on-time delivery, ASN accuracy, EDI compliance, product quality, invoice accuracy, and RTV compliance. Performance feeds chargeback calculations and purchase allocation decisions.

**5. Negotiate** — Use scorecard data as the basis for commercial renegotiation. Buyers engage vendors with quantitative performance history. Terms, pricing, and compliance requirements are renegotiated on evidence, not relationship.

**6. Rationalize Vendors** — Periodically reduce the vendor base. Concentrate purchasing on a smaller set of high-performing strategic partners. Track vendor profitability — not just vendor revenue — as the rationalization criterion. Strategic partners receive forecast-sharing and preferred terms; commodity vendors are reduced or exited.

**7. Discontinue Vendor** — Execute a formal discontinuation process: close open POs, resolve outstanding chargebacks and credits, settle allowances, and archive the vendor record. Discontinuation criteria are defined in advance, not decided ad hoc.

## Consumers

The Vendor Agent uses lifecycle state to gate PO creation — a vendor in discontinuation cannot receive new orders. The Receiving module reads compliance standards to trigger chargebacks at receipt. The Finance module reads payment terms for AP settlement. The Operations Agent monitors scorecard health and flags vendors approaching rationalization thresholds.

## Invariants

- Vendor compliance standards must be recorded in vendor master, not in email or informal agreements. Chargebacks are only defensible if terms were documented at setup.
- Rationalization decisions must be driven by vendor profitability, not vendor revenue. A high-volume vendor with poor margins is a rationalization candidate.
- Scorecard dimensions and weighting factors must be established before evaluation begins — not reverse-engineered from a desired outcome.

## Related

- [[retail-vendor-compliance-standards]] — the compliance clause matrix this lifecycle enforces
- [[retail-vendor-scorecard]] — the performance measurement model used in stage 4
- [[retail-chargeback-matrix]] — the financial enforcement layer triggered by non-compliance
- [[retail-purchase-order-model]] — gated by vendor lifecycle state
