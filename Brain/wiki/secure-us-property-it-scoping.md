---
date: 2026-04-23
type: wiki
tags: [secure, retail-career, ibm-consulting, tiger, property-it, us-property, pre-secure]
sources:
  - Brain/raw/inbox/property-app-overview.md
last-compiled: 2026-04-23
needs-review: 2026-05-07
---

**Wiki:** [[Brain/Home|Home]]

# Tiger (US) — Property IT Requirements Discussion Document

## Summary

An "IBM and Client Confidential" discussion document labelled **Property IT Requirements** for a US retailer codenamed **Tiger** (client identity not explicitly stated in the extract). Appears to be a scoping / design-validation kick-off deck for a US property IT engagement, part of IBM's pre-Secure retail consulting practice.

Agenda covers: introductions + expectations, current-state of US Property IT against the group offering, scoping questions / gaps / critical issues, Design Validation approach and responsibilities (named reviewers: Tony, Mark, Steve), review of Build Facilities / Maintain Facilities / Cost to Build / Asset Management.

## Findings Captured

### Site Acquisition / Construction

**Critical business requirements:**

- Centralised issue log to track RFIs between Tiger and Development Partners
- Centralised location database to manage site details, current status, and drive reporting
- Workflow capabilities to manage communication between Tiger Property, Developers, Attorneys, Insurance, Contractors
- End-to-end project cost tracking integrated with Oracle Financials

**Technical issues:**

- No database solution in use — heavy reliance on spreadsheets
- Manual communication and email used to track issue logs
- Non-standard procedures per development partner
- Property Team evaluating **QuickBase** for communication/workflow management

### Property Management

**Current understanding:**

- Property Management functions to be outsourced to an un-named partner
- US Property has requested that partner implement and use **Versai Property management** software (originally referenced "Verisai") for facilities management and lease administration
- Energy Management requirements need to be defined further

**Issues:**

- Possible integration points with third-party property management provider + Versai software (unclear scope)

## Open Questions / Notes for Synthesis

- **Client identity** — the extract refers only to "Tiger Property" and "US Property." IBM used retail-client codenames in this era. Plausible candidates include Tesco's US expansion (pre–Fresh & Easy), though no confirmation in the text. Flag for Jeffe to resolve during review.
- **Date** — the markitdown extract header shows "04/23/26" which appears to be the extraction/markitdown timestamp, not the document date. Document date is not otherwise stated.
- **Vendor stack referenced:** Oracle Financials (ERP), QuickBase (workflow), Versai (property/facilities management).

## Why This Matters

A short but representative example of the scoping-phase deliverable from IBM's retail consulting practice: current-state findings, critical business requirements, technical issues, vendor stack assessment, and next-step design-validation framing — all in one discussion deck. Useful as pattern precedent for:

- How a scoping deck frames "gaps + critical issues" without prescribing a solution
- How vendor software choices (Oracle, QuickBase, Versai) get flagged for integration analysis
- The "Design Validation" step that followed scoping — see also [[Brain/wiki/secure-dv-private-label-2006|DV Private Label Food Setup]], a Design Validation workshop output

## Related

- [[Brain/projects/Secure|Secure MOC]]
- [[Brain/wiki/secure-retail-career-archive|Pre-Secure Retail Career Archive]]
- [[Brain/wiki/secure-jlp-property-services-2002|JLP Property Services Operating Model (2002)]] — parallel property engagement (UK)
- [[Brain/wiki/secure-dv-private-label-2006|DV Private Label Food Setup]] — example of a downstream Design Validation deliverable
- [[Brain/wiki/secure-tesco-tom-2006|Tesco TOM 2006]] — same-era IBM retail consulting practice

## Sources

- `Brain/raw/inbox/Property App Overview.ppt` — Property IT Requirements Discussion Document (IBM and Client Confidential)

Extraction path: legacy `.ppt` → LibreOffice `.pptx` → markitdown.
