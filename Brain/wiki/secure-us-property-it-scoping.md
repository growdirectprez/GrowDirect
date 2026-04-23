---
date: 2026-04-23
type: wiki
tags: [secure, retail-career, ibm-consulting, us-property, scoping, pre-secure]
sources:
  - Brain/raw/inbox/property-app-overview.md
last-compiled: 2026-04-23
needs-review: 2026-05-07
---

**Wiki:** [[Brain/Home|Home]]

# US Property IT Requirements — Scoping Document (IBM, pre-Secure)

## Summary

An "IBM and Client Confidential" discussion document labelled **Property IT Requirements** for a **US retailer** (client identity behind an internal codename in the source deck). Appears to be a scoping / design-validation kick-off deck for a US property IT engagement, part of IBM's pre-Secure retail consulting practice.

**Deployment archetype:** US retailer with a growing property portfolio, development-partner relationships at multiple sites, and a fragmented property IT stack (spreadsheets + email). Needed a centralised property management system for site acquisition, construction, and facilities management.

Agenda covers: introductions + expectations, current-state of US Property IT against the group offering, scoping questions / gaps / critical issues, Design Validation approach and responsibilities (three named reviewers: Tony, Mark, Steve — internal engagement leads), review of Build Facilities / Maintain Facilities / Cost to Build / Asset Management.

## Findings Captured

### Site Acquisition / Construction

**Critical business requirements:**

- Centralised issue log to track RFIs between the property team and Development Partners
- Centralised location database to manage site details, current status, and drive reporting
- Workflow capabilities to manage communication between Property, Developers, Attorneys, Insurance, Contractors
- End-to-end project cost tracking integrated with Oracle Financials

**Technical issues:**

- No database solution in use — heavy reliance on spreadsheets
- Manual communication and email used to track issue logs
- Non-standard procedures per development partner
- Property Team evaluating **QuickBase** for communication/workflow management

### Property Management

**Current understanding:**

- Property Management functions to be outsourced to an un-named partner
- The client requested that the outsourcing partner implement and use **Versai Property management** software (originally referenced "Verisai") for facilities management and lease administration
- Energy Management requirements need to be defined further

**Issues:**

- Possible integration points with third-party property management provider + Versai software (unclear scope)

## Open Questions / Notes for Synthesis

- **Client identity** — the extract refers only to the internal engagement codename and "US Property." IBM used retail-client codenames in this era. Left intentionally un-named per `feedback_scrub_client_names.md`.
- **Date** — the markitdown extract header shows "04/23/26" which appears to be the extraction/markitdown timestamp, not the document date. Document date is not otherwise stated.
- **Vendor stack referenced:** Oracle Financials (ERP), QuickBase (workflow), Versai (property/facilities management).

## Why This Matters

A short but representative example of the scoping-phase deliverable from IBM's retail consulting practice: current-state findings, critical business requirements, technical issues, vendor stack assessment, and next-step design-validation framing — all in one discussion deck. Useful as pattern precedent for:

- How a scoping deck frames "gaps + critical issues" without prescribing a solution
- How vendor software choices (Oracle, QuickBase, Versai) get flagged for integration analysis
- The "Design Validation" step that followed scoping — see also [[Brain/wiki/secure-dv-private-label-2006|Private Label Food Setup Design Validation]], a Design Validation workshop output from 2006

## Related

- [[Brain/projects/Secure|Secure MOC]]
- [[Brain/wiki/secure-retail-career-archive|Pre-Secure Retail Career Archive]]
- [[Brain/wiki/secure-property-services-operating-model-2002|UK Property Services Operating Model (2002)]] — parallel property engagement
- [[Brain/wiki/secure-dv-private-label-2006|Private Label Food Setup Design Validation]] — example of a downstream Design Validation deliverable
- [[Brain/wiki/secure-retail-operating-model-2006|Retail Operating Model 2006]] — same-era IBM retail consulting practice

## Sources

Raw intake retains the original engagement codename + client-identifying content as source of record per `feedback_scrub_client_names.md`.

- `Brain/raw/inbox/Property App Overview.ppt` — Property IT Requirements Discussion Document (IBM and Client Confidential)

Extraction path: legacy `.ppt` → LibreOffice `.pptx` → markitdown.
