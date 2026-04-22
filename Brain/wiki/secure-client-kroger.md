---
date: 2026-04-21
type: wiki
tags: [secure, kroger, retail, loss-prevention, client-implementation, retek, ebr, dsd, canary-lineage]
sources:
  - Brain/raw/inbox/kroger-solution-architecture---lyle-comments-docx.md
  - Brain/raw/inbox/kroger-pos-baseline-pdf.md
  - Brain/raw/inbox/kroger-pos-selfhost-baseline-pdf.md
  - Brain/raw/inbox/max-replacement-appriss-follow-up-docx.md
  - Brain/raw/inbox/kroger-secure-rfp-resource-plan-pdf.md
  - Brain/raw/inbox/kroger-secure-rfp-timeline-pdf.md
  - Brain/raw/inbox/kroger-sysrepublic-secure-3-5-ebr-pricing-estimate-3-30-17-xlsx.md
  - Brain/raw/inbox/kroger-opportunity-fact-sheet-07242017-xlsx.md
  - Brain/raw/inbox/kroger-dsd-requirements-docx.md
  - Brain/raw/inbox/kroger-retek-project-sam-xls.md
  - Brain/raw/inbox/data-gathering-agenda-v9-aug_1-doc.md
  - Brain/raw/inbox/workarounds-doc.md
  - Brain/raw/inbox/deliverable-responsibilities-doc.md
  - Brain/raw/inbox/gantt-charts-xls.md
  - Brain/raw/inbox/rfi-8-15---lyle-comments-xlsx.md
  - Brain/raw/inbox/secure-store-client-services-process-pdf.md
  - Brain/raw/inbox/secure-store-engagement-overview-pdf.md
  - Brain/raw/inbox/secure-store-project-roles-pdf.md
last-compiled: 2026-04-21
needs-review: 2026-05-05
---

**Wiki:** [[Brain/Home|Home]]

# Secure Client: Kroger

## Summary

The Kroger archive spans **two distinct engagements separated by 16 years**: the 2001 Kroger Retek Procurement CRP (a PwC-led ERP rollout for DC-to-store merchandising on Retek RMS) and the 2017 Kroger Secure RFP (Appriss Secure Store 3.5 replacing Kroger's legacy "Max" T-log monitoring system). The two engagements bracket the evolution of retail LP tooling — from ERP-gap workarounds to purpose-built exception-based reporting. Knowledge in this archive is concrete: real transaction volumes (2,700 POS tx/store/day, 6.6 basket size), real pricing ($660K first-year subscription, $450K install for POS T-log), real architectural trade-offs (7-week Optimal vs 26-week Large configuration), and a worked-example workaround catalog showing where off-the-shelf retail ERPs leave gaps.

## Details

### Engagement 1 — Kroger Retek Procurement CRP (2001)

**Date:** August 2001.
**Partner:** PricewaterhouseCoopers (Drew Riegler, Partner; Tanya Kovacik, Principal Consultant; Garry Birkhofer, Director; John Farrell, Director; Jeff Goethals, Principal Consultant).
**Kroger sponsor:** Ron Langford, Paul Tudor.
**Location:** Cincinnati, OH.
**Scope:** Enterprise Procurement project — supply chain / DC-to-store merchandising, inventory productivity, on Retek RMS.

This is **pre-Secure, pre-Appriss** — the earliest Kroger engagement in the archive. It's a full ERP rollout, not an LP project. Its value for Secure lineage is the **workaround catalog** (see Workarounds source) — a concrete enumeration of where Retek RMS (the dominant retail merchandising system of the era) left gaps, and what retailers did to compensate.

**Workarounds catalog (from `Workarounds.doc`).** Each entry is a gap in Retek RMS Java allocation + the process workaround Kroger implemented:

| Area | Retek gap | Workaround |
|---|---|---|
| Allocation | Java allocation can't reserve DC stock for new stores | Use base RMS "new store hold bucket" under non-sellable; manual unit inventory adjustments |
| Allocation | Java allocation doesn't auto-reallocate short-shipped POs (some stores get 100%, others 0%) | ASN-based (EDI 856) for ASN vendors; avg-fill-rate % allocation for non-ASN with second allocation if over-ship |
| Pricing / Markdowns | Adding items to an existing clearance promotion requires store-by-store, not chain/zone | Separate clearance markdown per late-add |
| Purchasing | RMS doesn't allow a single PO across multiple OTB months | Separate PO per OTB month |
| Transfers | RMS lets transfer quantities be modified after approval | Policy + procedure (not a code fix) |
| Reporting | No online total-company stock ledger view above department level | Hard-copy report out of RMS |
| Inventory | Dollar inventory adjustments require SKU/store level, not vendor/dept | "Dummy" classes + SKUs to book dept-level adjustments |
| Inventory | Non-sellable indirect items still post to stock ledger despite flag | Separate department for non-sellable + customized RMS→financials interface |

This catalog is **prior-art reference material** for Canary: it shows what retailers actually do when their merchandising system doesn't fit. The workaround patterns (dummy classes, hold buckets, interface customization, separate POs per month) are things retail-LP detection logic needs to accommodate because they'll surface as anomalies in transaction streams.

### Engagement 2 — Kroger Secure RFP + Max Replacement (2017)

**Date:** Q1 2017 (RFP), kick-off planning mid-2017.
**Vendor:** Appriss Retail (successor to Sysrepublic).
**Product:** Secure Store 3.5 (EBR — Exception-Based Reporting).
**Kroger attendees (bid follow-up):** Don Boyle, John Teller, AJ Crawford, Travis McGuire, Glenn Campbell, Nicholas Creech, Kevin Larson, Chris McCarrick.
**Appriss attendees:** Bob Walters, Geoff Lyle.
**Scope:** Replace "Max" — Kroger's legacy G-Store T-log file monitoring self-hosted LP solution.

**Expansion phases:** POS T-logs (phase 1) → DSD (Direct Store Delivery) → Pharmacy → eCommerce.

#### Scale (from data-volume survey)

| Metric | Daily average | Peak |
|---|---|---|
| POS transactions per store | 2,700 | Not measured |
| Basket size (items per tx) | 6.6 | Not measured |
| Tender types per tx | 0.9 | Not measured |
| Discounted line items per tx | 3.3 | Not measured |

At Kroger's ~2,800 store count (2017 era), this is ~7.5M transactions/day across the chain. Main data repository sized at **~4TB** in the Appriss estimate.

#### Pricing structure (documented in Max Replacement follow-up)

| Component | Year-1 subscription | Install |
|---|---|---|
| POS T-log (self-hosted) | $660K | $450K |
| DSD (post-install add-on) | ~$350K | — |
| Pharmacy (post-install add-on) | ~$500K | — |
| eCommerce (post-install add-on) | TBD | — |

Enterprise agreement, no limits on end users / data sources / data size. Annual subscription increase not documented in source. Alternative bundled up-front payment option available.

Included in the bid:
- Dedicated account person
- 3rd-line 24/7 help desk
- LPMS (LP Management System) integration
- 100 hours of report consultation
- 2–3 day training workshop onsite

#### Architecture choices (from Solution Architecture + lyle comments)

Two sizing scales offered:

- **Large Configuration @ 26 weeks** — full redundancy, multi-DC, highest capacity.
- **Optimal Configuration @ 7 weeks** — right-sized, faster deployment.

Solution Architecture doc (v1 of Secure Store 3.2 era — version at the start of the bid) covered:
- Presentation / Service / Data layer decomposition
- Deployment architectures: Virtual Non-Redundant (typical), Physical, Virtual Machine Redundancy
- Server inventory specific to Secure 3.2
- Redundancy + load balancing options
- Non-prod hardware requirements

Kroger chose **self-hosted** over SaaS. Appriss supported both; install timeline similar (~20 weeks for self-host POS only).

#### Identity integration ask

Kroger's Siteminder Enterprise Identity Management (SSO) needed to integrate with Secure. Appriss response: Secure supports Azure AD, ADFS, SAML 2.0, OpenID Connect natively; Siteminder wraps into the SAML 2.0 framework as an identity provider.

#### Data retention

Appriss initial offer: 7 weeks. Kroger requirement: significantly longer. Appriss path: tune physical architecture for longer retention + data aggregation strategy for higher-level metrics beyond the detail retention window. Not resolved in the follow-up doc.

#### Cloud-readiness ask

Kroger asked about Pivotal Cloud Foundry compatibility. Appriss preferred physical hardware for Kroger's volume. Left as TBD pending IT infrastructure governance review.

### DSD extension (Kroger Direct Store Delivery)

Separately documented in `Kroger DSD requirements.docx`. DSD is the Kroger adjacency where vendors deliver inventory directly to stores, bypassing the DC. This creates a distinct fraud surface:
- Vendor driver / store receiver collusion (short deliveries, signed-for-but-not-received)
- Damaged goods claims at receiving
- Returns to vendor mismatches
- Invoice-to-receipt reconciliation gaps

Secure's DSD module extended base POS EBR into this surface. See [[Brain/wiki/secure-omnichannel|Secure Omnichannel]] for how DSD fits into the broader omnichannel risk taxonomy.

### Implementation artifacts in the archive

- **Kroger Solution Architecture.docx** — with Geoff Lyle's comments. The authoritative arch doc for the Secure 3.2 → 3.5 bid.
- **Kroger POS Baseline.pdf / Kroger POS SelfHost Baseline.pdf** — 61-row project baselines (MS Project export to PDF)
- **Kroger Secure RFP Resource Plan.pdf** — roles + allocation
- **Kroger Secure RFP Timeline.pdf** — Gantt starting Jan 2017
- **Kroger Sysrepublic Secure 3.5 EBR Pricing Estimate 3 30 17.xlsx** — pricing sheet
- **Kroger Opportunity Fact Sheet 07242017.xlsx** — commercial summary
- **RFI 8.15 (with lyle comments).xlsx** — August 15 RFI responses
- **Kroger Retek Project SAM.xls** — from the 2001 engagement
- **Gantt charts.xls / Deliverable Responsibilities.doc / Data Gathering Agenda.doc** — 2001 PwC engagement artifacts

### Files in archive but not ingested

Several files failed markitdown conversion (legacy `.ppt`, `.xls`, `.mpp` formats):
- `Info Gathering Agenda Aug_7.ppt`, `Lessons learned.ppt`, `Retek CRP Proposal v6-FEES.ppt`, `Retek CRP Proposal v6-FINAL.ppt`, `Retek Quals v3.ppt` (old .ppt — markitdown doesn't handle)
- `Kroger CRP additional v1.xls`, `Kroger CRP v1.xls` (old .xls — failed conversion)
- Multiple `.mpp` files (MS Project binary — no markitdown support)

Defer to a future NAS indexing pass with LibreOffice conversion path.

## What this teaches Canary

1. **Real scale numbers for retail LP.** 2,700 POS tx/store/day daily average, 6.6 basket, 4TB for a major grocery chain. Canary's Square merchants are 2–3 orders of magnitude smaller per merchant, but the multi-tenant total across the Canary customer base will eventually hit comparable aggregate volume. The Secure sizing model is reference material for Canary capacity planning.

2. **Legacy-system-replacement is the dominant deal motion at scale.** Kroger was replacing "Max" — the T-log monitor they'd built/bought a decade earlier. Canary's growth motion will increasingly be "replace your existing LP tool" rather than greenfield. Max-replacement-follow-up.docx is a template for the competitive conversation: pricing, self-host vs SaaS, scope expansion phasing, integration concerns.

3. **Expansion-path pricing.** Secure's DSD @ $350K, Pharmacy @ $500K post-install pricing is a **product-expansion pricing model**: core (POS T-log) gets the deep discount + install; adjacent modules get standalone post-install pricing. Canary Chirp packs + future modules (ecom, payroll, inventory) should consider this pricing shape.

4. **Workaround catalog as detection signal.** The 2001 Retek workaround list (dummy classes, new-store hold buckets, separate POs per OTB month) is the kind of retailer-specific oddity that produces **noise in LP detection** if not understood. Canary's detection rules need a mental model for "that's a workaround, not fraud." Worth a Chirp rule tuning guide section.

5. **Self-host vs SaaS at enterprise.** Kroger chose self-host. Secure supported both paths but clearly preferred SaaS for smaller customers. Canary is SaaS-only by design; the Secure lesson is that enterprise retailers will ask for self-host and will sometimes require it for IT-governance reasons. Canary's path at enterprise is a private cloud / VPC deployment tier, not full self-host — but the conversation shape is predictable.

6. **Identity: SAML is the entry ticket at enterprise retail.** Siteminder wrapped into SAML 2.0. Canary's magic-link auth is correctly simpler for SMB; the enterprise path requires SAML 2.0 + OIDC at minimum. See [[Brain/wiki/secure-architecture|Secure Architecture]] identity section.

7. **Data retention is a negotiation, not a fixed number.** Appriss opened at 7 weeks. Kroger demanded more. The resolution path is physical architecture + data-aggregation strategy, not just "more disk." Canary's retention policy needs a similar two-tier shape: detail retention window + aggregated-metrics window beyond.

## Related

- [[Brain/projects/Secure|Secure]] MOC
- [[Brain/wiki/secure-platform-overview|Secure Platform Overview]]
- [[Brain/wiki/secure-architecture|Secure Architecture]] — the architecture Kroger bought into
- [[Brain/wiki/secure-omnichannel|Secure Omnichannel]] — DSD fits in this taxonomy
- [[Brain/projects/Canary|Canary]] — forward project
- [[docs/superpowers/briefs/2026-04-secure-to-canary-handoff|Secure → Canary Handoff]] — Kroger-derived patterns feed into this

## Sources

Full list in frontmatter. Primary sources:

- `Kroger Solution Architecture - lyle comments.docx` — Secure 3.2 architecture bid for Kroger with own comments
- `Max Replacement Appriss follow-up.docx` — bid discussion notes covering pricing, architecture, identity, data retention, cloud
- `Kroger Secure RFP Resource Plan.pdf` + `Timeline.pdf` — 2017 engagement planning
- `Kroger Sysrepublic Secure 3.5 EBR Pricing Estimate.xlsx` — 2017 pricing detail
- `Kroger DSD requirements.docx` — DSD-specific requirements
- `Data Gathering Agenda.doc` (Aug 2001) — PwC-led earliest engagement
- `Workarounds.doc` — Retek RMS gap catalog from 2001
- Secure Store Client Services Process / Engagement Overview / Project Roles PDFs — how Secure engagements were run
