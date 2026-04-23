---
date: 2026-04-23
type: wiki
tags: [secure, dsd, ired, direct-store-delivery, vendor-analytics, credit-invoice, variance, fne]
sources:
  - Brain/raw/inbox/copy-of-fne-dsd-annual-summary-ired-view.md
last-compiled: 2026-04-23
needs-review: 2026-05-07
---

**Wiki:** [[Brain/Home|Home]]

# Secure DSD iRED Analytics — FnE Annual Summary

## Summary

A **Direct Store Delivery (DSD) Annual Summary** report in **iRED** (intelligent Retail Exception Detection) format — the analytical view Secure used to surface **vendor delivery vs. credit variance patterns** that indicate receiving errors, overbilling, or invoice fraud. Source is FnE (client codename, likely Fresh & Easy). The workbook is a master DSD Summary with per-vendor rows and a rich column set of derived ratios.

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

## Sample Vendors (from extract)

| Rank | Vendor | Major / Minor | Del Invoices | Del $ | Cred Invoices | Cred $ | Variant Ratio |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | MARKSTEIN BEVERAGE (Sacramento) | Beverage / Adult / Beer | 73 | $29,886 | 1 | −$62 | −176% |
| 2 | HEIMARK DISTRIBUTING (Indio) | Beverage | 82 | $46,224 | 2 | −$113 | −170% |
| 3 | VALLEY WIDE BEVERAGE (Fresno) | Beverage / Adult / Beer | 97 | $53,629 | 3 | −$205 | −34% |
| 4 | CRESCENT CROWN DISTRIBUTING (Phoenix) | Beverage | 2,649 | $2,483,885 | 4 | −$570 | −26% |
| 5 | ROMEROS FOOD PRODUCTS (Santa Fe Springs) | Food | 198 | $1,108,058 | 1 | −$144 | −25% |

Industry average variant ratio is **−63%**. Vendors at or below that mark get flagged for investigation — either the retailer's receiving process isn't catching issues (driving credit rates too low) or the vendor is engaging in systematic over-billing without pushback.

## Key Metrics The Analyst Uses

- **Credit-to-delivery invoice ratio** — "1 credit invoice for every _ delivery invoices." Healthy retailers with active receiving catch issues on ~5–10% of invoices; a ratio much lower suggests receiving is missing problems.
- **Credit-to-delivery value ratio** — "1 credit dollar for every _ delivery dollars." A low ratio (say, 1:5,000) combined with high delivery volume is a screaming signal of receiving breakdown.
- **Delivery-to-sales ratio** — per SKU, per Category, per Vendor. If a vendor's delivery dollars to store exceed the store's actual sales of that vendor's goods, the store is accumulating phantom inventory (either shrink or over-shipment).

## Why This Matters

**DSD analytics is one of the most profitable LP disciplines** — every dollar of improved credit capture flows straight to margin. It's also one of the least automated: most retailers rely on spreadsheet-wrangling analysts, which is why Secure productised the iRED view.

Direct Canary lineage:

- The Canary CRDM's normalised transaction + vendor model supports this same class of analysis when Square merchants start capturing vendor invoice data
- The **Chirp** concept (plain-language alerts) is the UX evolution of the iRED view — instead of showing the merchant a ratio table, we'd say *"you've received $4,358 of deliveries from Crescent Crown this month but only credited $570 back. Industry peers credit 63% more on this volume. Check your back-door receiving process."*
- The "variant ratio industry avg −63%" is a concrete example of a **cross-merchant benchmark** — exactly the network-intelligence moat Canary is building

## Open Questions for Session Review

- **Client codename FnE.** Almost certainly **Fresh & Easy** (Tesco's US grocery chain). If correct, this artefact is contemporaneous with the [[Brain/wiki/secure-tesco-tom-2006|Tesco TOM engagement]] or a later Secure client engagement — worth confirming during review.
- **iRED vs. Secure EBR.** Relationship between the iRED product line and the broader Secure EBR is not made explicit in this extract.

## Related

- [[Brain/projects/Secure|Secure MOC]]
- [[Brain/wiki/secure-5-inventory|Secure 5 Inventory]] — adjacent Secure EBR product
- [[Brain/wiki/secure-client-kroger|Kroger Implementation]] — DSD was also a focus at Kroger (POS baseline + CRP + DSD)
- [[Brain/wiki/secure-platform-overview|Secure Platform Overview]]
- [[Brain/projects/Canary|Canary]] — forward lineage

## Sources

- `Brain/raw/inbox/Copy of FnE DSD Annual Summary iRED view.xlsx` — DSD Summary Master workbook in iRED analytical view format

Extraction path: `.xlsx` → markitdown.
