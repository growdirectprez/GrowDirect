---
date: 2026-04-23
type: wiki
tags: [secure, retail-career, evant, lillian-vernon, merchandising, rfp, multi-channel, 2003, pre-secure]
sources:
  - Brain/raw/inbox/merchandising-system-rfp---evant-response-working.md
last-compiled: 2026-04-23
needs-review: 2026-05-07
---

**Wiki:** [[Brain/Home|Home]]

# Merchandising System RFP — Evant Response for Lillian Vernon (Sept 2003)

## Summary

Evant's response to a Merchandise Forecasting / Planning **Request for Proposal** from **Lillian Vernon Corporation (LVC)**, dated **8 September 2003**. A 23+ section RFP response spanning Executive Summary, Solution Summary, Product/Solution Functionality, Top-Line Business Objectives, Solution Support, Implementation + Team, Implementation Schedule, Investment/Pricing, Company Overview, References/Qualifications, and a Merchandise Planning & Execution Process Overview.

LVC was a US multi-channel (catalog + web + retail) retailer aiming to become "a $1 billion leading multi-channel retailer known for superior products, values, customer experience, operations and profitability." Evant proposed a phased implementation of their Retail Management suite to support that goal.

## The Evant Retail Management Suite

Three workflow components, presented as an integrated suite:

1. **Evant Merchandising** — transaction management including purchasing, pricing, inventory management. *Not proposed for LVC.*
2. **Evant Planning** — planning + forecasting workflows
3. **Evant Enterprise Information Management (EIM)** — centralised system of record for retail enterprise data driving reporting

Evant's positioning language:

> *"The first multi-channel retail planning solution that enables cross-channel and channel-specific merchandising… a replenishment solution that drives optimal inventory considering multiple channels… the first enterprise information management system that provides a centralized system of record repository for retail enterprise data that drives reporting… the only enterprise software for the retail industry built on a scalable J2EE platform."*

## Modules Proposed to LVC

| Module | Purpose | Proposed for LVC? |
|---|---|---|
| Evant Merchandise Planning (MP) | Planning + forecasting (one of two forecast modules) | ✅ |
| Evant Demand Planning & Replenishment (DPR) | Planning + forecasting (second module) | ✅ |
| Evant Enterprise Information Management (EIM) | Master data for vendor/product/location/channel | ✅ |
| Evant Decision Support | Data models for catalog/web/product/inventory/selling, integrated into LVC's BI tool (MicroStrategy, Oracle Express, etc.) | ✅ |
| Evant Merchandising | Transaction management (purchasing/pricing/inventory) | ❌ (not in scope) |

Implementation approach: **phased** — combine functional pieces from each module to address the most critical needs first, then layer remaining functionality.

## Why This Matters

A clean representative of the **retail software RFP response** form circa 2003:

- **Buyer framing** — opens with the retailer's own strategic goals ("$1B multi-channel leader") and wraps Evant's offering around them rather than leading with product features
- **Explicit module fit** — states up-front which modules are in-scope vs out-of-scope, rather than leaving it to later clarification
- **Vendor ecosystem context** — names specific BI tools (MicroStrategy, Oracle Express) for data-model integration, and flags J2EE as the platform differentiator
- **Phased implementation** — the dominant pattern in 2000s retail software sales: "phase 1 critical needs, phase 2 augmentation"

Notable for GrowDirect / Canary lineage: Evant's pitch of "centralized system of record repository for retail enterprise data that drives reporting" is conceptually the same value proposition as Canary's CRDM (Canary Retail Data Model) — a master dataset that unifies merchandising, location, channel, and product information. The difference is **2026 merchants get this automatically over OAuth from their POS; 2003 LVC got it as a multi-million-dollar integration project.**

Lillian Vernon itself filed for bankruptcy in 2008 and ceased operations as a standalone business — a reminder that in retail, even the best merchandising technology doesn't save a declining business model.

## Related

- [[Brain/projects/Secure|Secure MOC]]
- [[Brain/wiki/secure-retail-career-archive|Pre-Secure Retail Career Archive]]
- [[Brain/wiki/secure-integrated-maps-2003|Integrated Maps 2003/04]] — same-year ecosystem map
- [[Brain/wiki/secure-tesco-tom-2006|Tesco TOM 2006]] — later operating-model work

## Sources

- `Brain/raw/inbox/Merchandising System RFP - Evant Response-working.doc` — Evant's response to LVC RFP, 8 Sept 2003

Extraction path: legacy `.doc` → markitdown.
