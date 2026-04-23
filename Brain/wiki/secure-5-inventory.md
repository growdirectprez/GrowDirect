---
date: 2026-04-23
type: wiki
tags: [secure, secure-5, appriss, inventory, ollies, s5-1, ebr, shrink, availability, accuracy, 2018, 2021]
sources:
  - Brain/raw/inbox/s5-1-inventory-data-requirements.md
  - Brain/raw/inbox/inventory-mock-up.md
  - Brain/raw/inbox/secure-inventory-overview-022221.md
  - Brain/raw/inbox/secure-inventory-overview-v2.md
last-compiled: 2026-04-23
needs-review: 2026-05-07
---

**Wiki:** [[Brain/Home|Home]]

# Secure 5 Inventory

## Summary

The **Secure Inventory** product module within the Appriss Retail **Secure Exception Based Reporting (EBR)** family. Four intakes covering the product's scope, data requirements, a transactional model mock-up, and two client-facing rollout artefacts — the **Ollie's Bargain Outlet Secure Store Kickoff** (March 2018, launch of Secure 5 at Ollie's 271 stores) and a **February 2021 Marketing Update on Secure 3 → Secure 5 conversions**.

Secure Inventory extends the Secure EBR platform beyond POS exception detection into the **inventory dimension** — surfacing issues across three risk axes:

- **Shrink** — unexplained inventory loss
- **Availability** — out-of-stock or excess-stock at unit level
- **Accuracy** — unit-level on-hand integrity

## Data Requirements (S5.1)

Authored by **Richard Williams**, the **Inventory Data Requirements document** (S5.1) is the canonical source-data specification for Secure Inventory — what the product needs from the retailer to be able to compute the shrink/availability/accuracy signals. The extracted version captures the document frame (title, version table, reviewer signoff grid) but individual data-field definitions are preserved in the source `.docx` at the path in frontmatter.

## The Inventory Transactional Model (2018 mock-up)

A simple one-sheet demonstration of the daily inventory ledger Secure Inventory operates on. Six fields per row:

| Field | Meaning |
|---|---|
| DATE | Transaction day |
| BOH | Beginning On Hand |
| RTN | Returns (inbound) |
| ADJ | Adjustments (manual or system) |
| RCT | Receipts (delivery / replenishment) |
| EOH | Ending On Hand |

Example rows (March 2018):

| DATE | BOH | RTN | ADJ | RCT | EOH |
|---|---:|---:|---:|---:|---:|
| 2018-03-01 | 5 | 1 | 0 | 10 | 16 |
| 2018-03-02 | 16 | 0 | 0 | 0 | 16 |
| 2018-03-04 | 16 | 2 | 2 | 0 | 20 |
| 2018-03-05 | 20 | 1 | −1 | 0 | 20 |
| 2018-03-06 | 20 | 0 | 3 | 10 | 33 |
| 2018-03-12 | 38 | 5 | −3 | 0 | 40 |

The invariant is `EOH = BOH + RTN + ADJ + RCT − units_sold`. Exceptions arise when the math doesn't balance, which points at either POS data gaps, adjustment errors, receiving errors, or shrink.

## Ollie's Secure Store Kickoff (March 2018)

Secure Store v5 was rolled out to **Ollie's Bargain Outlet** across **271 retail locations** starting with a March 7, 2018 kickoff. Scope:

- Exception-Based Reporting on 12 months of detailed POS transactional data
- Daily batch feed of: POS sales data, store + item master data, employee reference data
- Additional feed of returns data from Ollie's Refund Management system
- Base Appriss Retail **Enterprise Case Management** application configuration included in the project scope

The kickoff deck frames Secure Store v5 as an **Exception-Based Reporting System designed to assist Loss Prevention and Store Operations in identifying anomalies at point of sale** — which is the same product thesis that Canary reapplies to Square merchants today, at a different price point and via a different data pipeline (webhooks vs batch).

## Secure 3 → Secure 5 Conversion Program (Feb 2021 Marketing Update)

As of February 2021, Appriss Retail was running a coordinated plan to convert the **remaining 30 Secure 3 accounts to Secure 5** over an 18-month horizon. The goal: significantly reduce upgrade time and effort. Streamlining coordinated across Legal, Finance, and Customer Success — particularly the renewal contracting process.

Accounts grouped by strategic archetype to focus resources:

1. **Complex technical solutions for important accounts** — highest-touch conversions
2. **Strategic cross-sell opportunities** — upgrade + upsell combined
3. **Grocery** — vertical-specific grouping
4. **Low value** — streamlined / lighter treatment

The same deck also introduces Secure Inventory as the surrounding product context:

> *"Secure Inventory is part of the Appriss Retail Secure Exception Based Reporting (EBR) family of products, leveraging all of the platform capabilities to identify Inventory risks associated with Shrink (Unexplained Loss), Availability (out of stock or excess stock), and Accuracy (unit level on hand). Secure relies on a prescriptive set of Inventory data sources which are required to identify issues related to shrink, stock availability, and inventory accuracy within the store."*

A subsequent slide introduces the **DSD Work Item List** — tying Secure Inventory into the same Direct Store Delivery analytics family as the [[Brain/wiki/secure-dsd-ired-analytics|FnE DSD iRED analytics]] content.

## Why This Matters

- **Canary lineage.** The BOH/RTN/ADJ/RCT/EOH ledger model is a direct precursor to Canary's inventory module. The Secure 5 data-requirements + Ollie's kickoff give a blueprint for the data feeds + scope a Secure-lineage Inventory product depends on.
- **Multi-year product strategy reference.** The Secure 3 → Secure 5 conversion program illustrates how Appriss Retail managed a multi-year product-migration at scale (30 accounts, 18 months, three strategic cohorts). Pattern precedent for any future Canary major-version migration.
- **Ollie's deployment scale.** 271 store locations on a daily batch feed is a useful anchor for "what a real mid-market Secure 5 deployment looked like in 2018."

## Related

- [[Brain/projects/Secure|Secure MOC]]
- [[Brain/wiki/secure-platform-overview|Secure Platform Overview]] — Secure product line context
- [[Brain/wiki/secure-architecture|Secure Architecture]] — S5 on-premise architecture
- [[Brain/wiki/secure-customer-order-management-flow-2017|Secure Customer Order Management Flow (2017)]] — adjacent Secure 5 omnichannel flow
- [[Brain/wiki/secure-dsd-ired-analytics|Secure DSD iRED Analytics]] — adjacent vendor-DSD analytics
- [[Brain/projects/Canary|Canary]] — forward lineage

## Sources

- `Brain/raw/inbox/S5.1 Inventory Data Requirements.docx` — S5.1 data requirements, authored by Richard Williams
- `Brain/raw/inbox/Inventory Mock Up.xlsx` — BOH/RTN/ADJ/RCT/EOH daily ledger mock-up (March 2018)
- `Brain/raw/inbox/Secure Inventory Overview-v2.pptx` — Ollie's Secure Store v5 Kickoff, March 7, 2018
- `Brain/raw/inbox/Secure Inventory Overview 022221.pptx` — Marketing Update: Secure 3 Conversions + Secure Inventory, February 2021 (©Appriss Retail, Proprietary and Confidential)

Extraction path: `.docx` / `.xlsx` / `.pptx` → markitdown.
