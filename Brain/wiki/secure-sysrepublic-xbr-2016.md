---
date: 2026-04-23
type: wiki
tags: [secure, sysrepublic, xbr, lululemon, ebr, case-management, icms, requirements, 2016]
sources:
  - Brain/raw/inbox/20160608-sysrepublic-xbr-replacement-func-req---sr-comments.md
last-compiled: 2026-04-23
needs-review: 2026-05-07
---

**Wiki:** [[Brain/Home|Home]]

# Lululemon xBR Replacement — Sysrepublic Functional Requirements Response (June 2016)

## Summary

Functional requirements response spreadsheet for the **Lululemon xBR replacement project**, dated **2016-06-08**. Lululemon Asset Protection issued a Functional Requirements Specification (FRS) for replacing their existing **xBR (Exception-Based Reporting)** solution; Sysrepublic responded with line-by-line fit statements against their **Secure Store EBR** product, noting scope boundaries (what's included) and scope gaps (what sits in the separate **ICMS — Intelligent Case Management System** product).

The extracted spreadsheet (`Sheet1`) has one row per requirement, organised into 10 functional categories.

## Requirement Categories (10)

| Category | Req-ID Prefix | Nature |
|---|---|---|
| Foundation Objects | `Sec-Sys-FOU-*` | Case hierarchies, relationships, multilingual, staff, core reference data, task management |
| Self Service | `Sec-Sys-CSS-*` | Password reset, print, subscriptions, alerts, receipt re-print |
| Knowledge Base | `Sec-Sys-KNO-*` | Organisation, search, user review, UI, content usage tracking |
| Workgroups Management | `Sec-Sys-WGM-*` | Workgroup assignment, org hierarchy, agent workload, case list |
| Lead Development | `Sec-Sys-LDM-*` | Automated + ad-hoc lead generation, territory mgmt, case identification, merge, assignment, notification, visibility, activity tracking, notes, pipeline, reports, homepage, quick-activity |
| Investigation Information Management | `Sec-Sys-Info-*` | Action reminders, assigned actions, attendance tracking, print |
| Case Management | `Sec-Sys-Case-*` | Case associations (to scams, fraud models, alerts) |
| Business Analytics | `Sec-Sys-BAL-*` | Data export, ad-hoc reporting, standard reporting, dashboards, case analytics |
| Security | `Sec-Sys-STY-*` | 2FA, HTTPS/TLS, session timeout, IAM integration, password handling, cryptography |
| Integration & Data Migration | `Sec-Sys-INT-*` | SFTP application integration, data migration |

## Key Sysrepublic Positioning (from vendor responses)

### Two-product boundary: Secure Store EBR vs. ICMS

The recurring theme across the spreadsheet: Lululemon asked for a single unified case-management + exception-reporting tool. Sysrepublic responded that their product line is **split into two products** and the agreement is scoped to Secure Store EBR only:

- **Secure Store EBR** — the core exception-based reporting product. Basic case-management functionality sufficient for building an investigation from a detected exception. In scope.
- **Sysrepublic ICMS** — full Case Management workflow + Resolution capabilities. **Not in scope under this agreement.**

This boundary drove roughly 20% of the responses in the sheet. Requirements around case relationships, task management, subscriptions, alerts, multi-level case workflow, and case merging were consistently flagged "part of case management — not in scope."

### What Secure Store EBR *did* cover

- Core reference data (Item Master, Employee/Cashier Master, Store Org Hierarchy) — imported from the Enterprise Landing Area
- Multi-lingual capability (Unicode), but only translated when an additional language is funded as a change order
- Lead generation — scheduled automated + on-demand ad-hoc queries, territory-based definition
- Lead-to-case qualification workflow (manager creates case when qualifying lead)
- Activity tracking against leads/cases (tasks, meetings, phone calls, emails, attached files/notes)
- Standard reports + ad-hoc reporting + management dashboards
- Role-based access; **no user-based personalisation of portals/homepages** — Sysrepublic eliminated this due to historical issues, restricted to role-level admin-created
- HTTPS (SSL v3.1 / TLS v1.0), session timeouts, role-based access, encryption at rest (one-way for passwords)
- **No 2FA token support** at the time of the response — IAM integration yes, application-level token no
- SFTP-based integration + data migration tooling

### Notable open clarifications the vendor flagged

- "need more clarity" on Case Hierarchies, Staff Details, Case Identification, Quick Activity Creation
- Receipt re-print with Lululemon-branded format was confirmed YES, exportable to PDF + other formats
- Lead/Case pipeline dashboard = "this would be developed out of the 100 hours of consultancy" — i.e., part of the implementation services budget, not out-of-the-box
- Data export to external BI: possible but would incur additional development costs for the outbound interface

## Why This Matters

A clean example of **how Sysrepublic scoped the Secure Store EBR product in vendor negotiations** — and a precise artefact of the Secure / ICMS product-line split as it existed in June 2016. Useful for:

- Understanding the historical boundary between Secure Store EBR and Sysrepublic ICMS (case management)
- Seeing what Lululemon (a mid-market specialty retailer) actually needed from an LP/EBR system — many of these requirements map directly onto Canary's Chirp + Fox architecture today
- Reference point for the **"this would be out of the 100 hours of consultancy"** model — where vendor software is sold with a bundled services block for dashboard/report customisation, a pattern Canary explicitly avoids (SaaS pricing, no services block)

## Canary Lineage Notes

- **Foundation Objects** maps to Canary's tenant + merchant + location data model
- **Lead Development** is Sysrepublic's terminology for what Canary calls **detection → Chirp** (the automated query generation that surfaces suspicious patterns)
- **Case Management** is Canary's **Fox module** (case management + evidence chain)
- **Homepage personalisation restriction** — Sysrepublic's "eliminated user-based personalisation due to issues" is a useful pattern note: Canary's dashboard similarly favours role-based layouts over per-user customisation

## Related

- [[Brain/projects/Secure|Secure MOC]]
- [[Brain/wiki/secure-platform-overview|Secure Platform Overview]]
- [[Brain/wiki/secure-architecture|Secure Architecture]]
- [[Brain/wiki/secure-eagle-eye-fnr-2018|Eagle Eye FR/NFR (2018)]] — follow-on requirements work 20 months later
- [[Brain/wiki/secure-lpms-case-management|LPMS Case Management (2015)]] — the case-management product Sysrepublic was protecting the boundary of
- [[Brain/projects/Canary|Canary]] — forward lineage (Chirp + Fox)

## Sources

- `Brain/raw/inbox/20160608 Sysrepublic xBR Replacement Func Req - SR Comments.xlsx` — Lululemon FRS response sheet with Sysrepublic vendor comments, 2016-06-08

Extraction path: `.xlsx` → markitdown.
