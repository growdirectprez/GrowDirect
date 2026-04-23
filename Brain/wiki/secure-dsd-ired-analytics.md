---
date: 2026-04-23
type: wiki
tags: [secure, dsd, ired, direct-store-delivery, vendor-analytics, credit-invoice, variance, us-grocery]
sources:
  - Brain/raw/inbox/copy-of-fne-dsd-annual-summary-ired-view.md
last-compiled: 2026-04-23
needs-review: 2026-05-07
---

**Wiki:** [[Brain/Home|Home]]

# Secure DSD iRED Analytics — US Grocery Chain Annual Summary

## Summary

A **Direct Store Delivery (DSD) Annual Summary** report in **iRED** (intelligent Retail Exception Detection) format — the analytical view Secure used to surface **vendor delivery vs. credit variance patterns** that indicate receiving errors, overbilling, or invoice fraud. Source is a **US grocery chain with heavy DSD dependency** (beverage, adult beverage, food) operating across multiple US state regions — client identity carried behind an internal codename in the source workbook. The workbook is a master DSD Summary with per-vendor rows and a rich column set of derived ratios.

**Deployment archetype:** US grocery chain, multi-state footprint, heavy beverage + DSD vendor dependency, running DSD analytics as part of a vendor-compliance / shrink-management program.

DSD is the retail practice where vendors deliver product directly to individual stores rather than through a retailer's DC. Store receivers accept goods at the back door, and the retailer pays the invoice after the fact. This model is systematically vulnerable to over-billing, short-shipment, and "credit friction" — the practice of making post-delivery credits onerous so they don't get taken.

## The iRED Analytical View

Each vendor row carries delivery-side data, credit-side data, and derived ratios:

**Delivery side (what the vendor invoiced):**
- Delivery Invoice Count
- Delivery Dollars
- Delivery Item Count
- Delivery value per invoice
- Delivery value per item
- Delivery items per invoice

**Credit side (what the retailer clawed back):**
- Credit Invoice Count
- Credit Dollars (typically negative)
- Credit Item Count
- Credit value per invoice
- Credit value per item
- Credit items per invoice

**Derived exception signals:**
- Delivery item $ − Credit item $ (value gap)
- Variant ratio — industry avg: **−63%**
- Delivery to Sales Ratio (per Vendor / per Category / per SKU)
- Credit / Delivery ratio (invoice-level, value-level, item-level)

Time horizons: per month/period, rolling 12-week, rolling 6-month, rolling 12-month, YTD. Primaries A/B/C/D vs. LY ("Last Year same") comparison brackets.

## Sample Vendor Pattern (anonymised)

Vendor rows in the extract show per-vendor Delivery Invoices / Delivery $ / Credit Invoices / Credit $ / Variant Ratio. High-volume beverage vendors in the sample hit variant ratios between −26% and −176% — well below the industry average of −63%, which is exactly the anomaly the iRED view is built to surface.

Industry average variant ratio is **−63%**. Vendors at or below that mark get flagged for investigation — either the retailer's receiving process isn't catching issues (driving credit rates too low) or the vendor is engaging in systematic over-billing without pushback.

## Key Metrics The Analyst Uses

- **Credit-to-delivery invoice ratio** — "1 credit invoice for every _ delivery invoices." Healthy retailers with active receiving catch issues on ~5–10% of invoices; a ratio much lower suggests receiving is missing problems.
- **Credit-to-delivery value ratio** — "1 credit dollar for every _ delivery dollars." A low ratio (say, 1:5,000) combined with high delivery volume is a screaming signal of receiving breakdown.
- **Delivery-to-sales ratio** — per SKU, per Category, per Vendor. If a vendor's delivery dollars to store exceed the store's actual sales of that vendor's goods, the store is accumulating phantom inventory (either shrink or over-shipment).

## Why This Matters

**DSD analytics is one of the most profitable LP disciplines** — every dollar of improved credit capture flows straight to margin. It's also one of the least automated: most retailers rely on spreadsheet-wrangling analysts, which is why Secure productised the iRED view.

Direct Canary lineage:

- The Canary CRDM's normalised transaction + vendor model supports this same class of analysis when Square merchants start capturing vendor invoice data
- The **Chirp** concept (plain-language alerts) is the UX evolution of the iRED view — instead of showing the merchant a ratio table, we'd say *"you've received $X,XXX of deliveries from this vendor this month but only credited $Y back. Industry peers credit 63% more on this volume. Check your back-door receiving process."*
- The "variant ratio industry avg −63%" is a concrete example of a **cross-merchant benchmark** — exactly the network-intelligence moat Canary is building

## Open Questions for Session Review

- **iRED vs. Secure EBR.** Relationship between the iRED product line and the broader Secure EBR is not made explicit in this extract.

## Related

- [[Brain/projects/Secure|Secure MOC]]
- [[Brain/wiki/secure-5-inventory|Secure 5 Inventory]] — adjacent Secure EBR product
- [[Brain/wiki/secure-client-top5-grocery-chain|Top-5 Grocery Chain Implementation]] — DSD was also a focus in the grocery-chain implementation covered there
- [[Brain/wiki/secure-platform-overview|Secure Platform Overview]]
- [[Brain/projects/Canary|Canary]] — forward lineage

## Sources

Raw intake retains original client-codename filename + sample vendor rows as source of record per `feedback_scrub_client_names.md`.

- `Brain/raw/inbox/Copy of FnE DSD Annual Summary iRED view.xlsx` — DSD Summary Master workbook in iRED analytical view format

Extraction path: `.xlsx` → markitdown.
