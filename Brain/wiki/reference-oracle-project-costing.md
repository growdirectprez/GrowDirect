---
date: 2026-04-23
type: wiki
tags: [reference, oracle, project-costing, erp, retail-tech-era, 2005]
sources:
  - Brain/raw/inbox/oracle-project-costing-user-guide.md
last-compiled: 2026-04-23
needs-review: 2026-05-07
---

**Wiki:** [[Brain/Home|Home]]

# Oracle Project Costing — User Guide, Release 11i (May 2005)

## Summary

The full **Oracle Project Costing User Guide** for **Oracle E-Business Suite Release 11i**, May 2005, Part No. B10855-02. Primary authors: Jeffrey Colvard, Stephen A. Gordon. An Oracle-published reference document — not a proprietary engagement artefact — archived in the inbox alongside the IBM/retail consulting material.

## What the Document Covers

Oracle Project Costing is the module in Oracle E-Business Suite responsible for tracking, recording, and reporting the costs incurred on projects — labour, expenditures, capital outlays, allocations, indirect cost calculations, revenue recognition tie-ins, and project-to-GL integration. It's the ERP backbone that enterprise IT, property, and construction projects run on, and it's named explicitly in the [[Brain/wiki/secure-tiger-property-it|Tiger Property IT]] discussion document as the target integration point for that engagement's cost-tracking requirement.

The guide is ~500+ pages covering: project structures, budgeting, expenditure entry and import, labour costing (standard/actual cost methods), cross-charges, burden schedules, indirect cost allocation, revenue generation, project status reporting, capital projects + asset capitalisation, transfer pricing, multi-currency handling, and security + auditing.

## Why This Is Kept as Reference

- **Cross-reference for consulting-era artefacts.** Multiple 2002–2006 engagement docs reference Oracle Financials / Project Costing as the target integration. This guide is the canonical spec for what those integrations had to talk to.
- **Retail-tech-era context.** Release 11i was the dominant Oracle EBS version through the mid-2000s, before the Fusion / Cloud ERP transition. Understanding 11i data model + terminology unlocks the 2002–2006 retail consulting material.
- **Not Secure product line.** This is **Oracle's own product documentation** — preserved here as reference material, not Canary / Secure IP.

## Who Should Consult This

- Anyone synthesising older engagement docs that reference Oracle Financials / Project Costing integration points
- Anyone building Canary financial-integration capability and wanting to understand what an enterprise-grade project-cost system looks like on the inside
- Anyone writing an SDD that needs to speak the ERP-vendor-native language of labour, burden, burden schedule, indirect cost allocation, expenditure type, etc.

## Related

- [[Brain/projects/Secure|Secure MOC]] — Reference Materials section
- [[Brain/wiki/secure-us-property-it-scoping|US Property IT Scoping]] — document that references Oracle Financials integration
- [[Brain/wiki/secure-property-services-operating-model-2002|Property Services Operating Model (2002)]] — adjacent property-services engagement
- [[Brain/wiki/secure-integrated-maps-2003|Integrated Maps 2003/04]] — 2003 retail tech landscape including SAP as the ERP counterweight

## Sources

- `Brain/raw/inbox/Oracle Project Costing User Guide.pdf` — Oracle Project Costing User Guide, Release 11i, May 2005 (Part No. B10855-02)

Extraction path: `.pdf` → markitdown. Full text extraction succeeded.
