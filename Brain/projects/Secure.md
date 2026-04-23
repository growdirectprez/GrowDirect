---
type: project-moc
status: archive-active
tags: [secure, retail, loss-prevention, ibm, appriss, sysrepublic, canary-lineage]
---

# Secure

Historical retail loss-prevention product suite (IBM → Appriss → Sysrepublic era, ~2010–2019). Product is shipped and mature; Brain captures the IP and carries it forward as domain lineage for **Canary**, which rebuilds this problem space for Square merchants.

## Status

Archive. Product history, architecture, detection concepts, and client implementations preserved. Active for Canary cross-reference and founder-credibility material.

## Wiki Articles

### Secure Product Line (core)

- [[Brain/wiki/secure-platform-overview|Platform Overview]] — what Secure was, product line, positioning, mapping to Canary
- [[Brain/wiki/secure-architecture|Architecture]] — S5 on-premise, SSO, Factory + New Delivery Process
- [[Brain/wiki/secure-lite|Secure Lite]] — product variant for smaller merchants (overview + config)
- [[Brain/wiki/secure-omnichannel|Omnichannel]] — omnichannel positioning + Appriss retail data spec
- [[Brain/wiki/secure-customer-order-management-flow-2017|Customer Order Management Flow (2017)]] — omnichannel data-flow diagram
- [[Brain/wiki/secure-5-inventory|Secure 5 Inventory]] — Secure Inventory product module (S5.1 data reqs, discount-retailer kickoff 2018, Secure 3→5 conversion 2021)
- [[Brain/wiki/secure-dsd-ired-analytics|DSD iRED Analytics]] — US grocery chain DSD vendor-credit variance analysis

### Client Implementations

All entries abstracted to deployment archetypes per `feedback_scrub_client_names.md` — raw intakes retain original client identifiers as source of record.

- [[Brain/wiki/secure-client-kroger|Top-5 Grocery Chain Implementation]] — first client deep-dive (POS baseline, CRP, DSD) *(legacy card — client name in filename pending scrub)*
- [[Brain/wiki/secure-lpms-case-management-2015|Sporting-Goods Chain LPMS (2015)]] — case-management taxonomies, reporting, sample case extract, firearms-regulated segment

### Requirements Artefacts

- [[Brain/wiki/secure-sysrepublic-xbr-2016|xBR Replacement — Sysrepublic Response (2016)]] — athleisure-retailer FRS vendor-response with Secure Store EBR / ICMS scope boundary
- [[Brain/wiki/secure-eagle-eye-fnr-2018|Eagle Eye FR/NFR v4.0 (2018)]] — traceability-matrix requirements workbook with NS review comments

### Pre-Secure Retail Career Archive (IBM era)

- [[Brain/wiki/secure-retail-career-archive|Pre-Secure Retail Career Archive]] — top-level index (expand via child cards below)
- [[Brain/wiki/secure-retail-operating-model-2006|Retail Operating Model 2006]] — 8-deck Target Operating Model engagement at UK global grocer (Commercial, Finance, Supply Chain, Retail Ops, Space/Range/Display, Forecast/Ordering, People, Property)
- [[Brain/wiki/secure-property-services-operating-model-2002|Property Services Operating Model (2002)]] — UK dept-store + grocery group P&BS operating model + DS process workshops
- [[Brain/wiki/secure-us-property-it-scoping|US Property IT Scoping]] — IBM-and-Client-Confidential scoping document for US property IT
- [[Brain/wiki/secure-integrated-maps-2003|Integrated Maps — Retail Hardlines Landscape (2003)]] — SAP / ISV / IBM solution map
- [[Brain/wiki/secure-merchandising-rfp-evant-response-2003|Merchandising RFP — Evant Response (Sept 2003)]] — multi-channel retail planning RFP response
- [[Brain/wiki/secure-dv-private-label-2006|Private Label Food Setup Design Validation (Aug 2006)]] — US Design Validation workshop

### Reference Materials (non-Secure)

- [[Brain/wiki/reference-oracle-project-costing|Oracle Project Costing User Guide (2005)]] — Oracle E-Business Suite 11i reference, relevant to US Property IT Scoping + Property Services engagements
- [[Brain/wiki/reference-hoa-disclosure-sample-2018|HOA Disclosure Documents Sample (2018)]] — California HOA disclosure pack reference (not WPBCA; PII-sensitive)

## Source Archives

Originals live in place — Brain references them by path, never copies.

| Archive | Path | Scope |
|---|---|---|
| Curated product docs | `/Users/gclyle/secure/` (local) | 15 top-level Secure product docs — Sprint 1 covers these |
| Secure-era client work | `/Users/gclyle/mnt/nas-archive/Work/Clients/` + `Work/Projects/` (NAS) | Kroger (Sprint 1), Wal-Mart / Harrods / Staples / Toys / Heartbeat / TSA / Retek / SAP (future) |
| Modern Secure 5 (2017) | `/Users/gclyle/mnt/nas-archive/Work/Clients/SECURE 5/` (NAS) | EBR4/EBR5, KAP requirements, post-Appriss era |
| Email context | `/Users/gclyle/mnt/nas-archive/Email/CLIENTS/SECURE 5/` (NAS) | Light — complementary only |

## Canary Lineage

- [[docs/superpowers/briefs/2026-04-secure-to-canary-handoff|Secure → Canary Handoff]] — patterns to adopt, adapt, or reject
- [[Brain/projects/Canary|Canary]] — forward project (same problem, different buyer, different tech)

## Client Implementations

- **Kroger** — [[Brain/wiki/secure-client-kroger|deep-dive]] (Sprint 1 first client)
- Wal-Mart, Harrods, Staples, Toys 'R' Us, Heartbeat, TSA — Sprint 2+ (sources on NAS)

## Future Work

### NAS Archive Indexing (separate sprint)

The broader NAS archive (`~/mnt/nas-archive/Work/`, `Reference/`, `Unsorted/`) holds 15+ years of retail consulting and product work beyond the Secure product line itself. High-value candidates for later extraction:

- **SDD material** — old user manuals, functional guides, design session notes → Canary SDD source material
- **Functional requirements docs** — FRs at the depth Canary would take months to write from scratch
- **Database schemas** — older retail data models to cross-reference against Canary's current schema
- **Methodology guides** — old delivery methodologies (IBM Method Web, JDA, factory/delivery process patterns) → agent-team playbooks
- **Agent-team guides** — role-based playbooks derivable from how the consulting practice actually ran

This is NOT Sprint 1 scope. Sprint 1 processes the already-curated Secure + Kroger content only. A future sprint will:

1. Index the NAS archive (inventory + topic taxonomy + value-tier classification)
2. Triage treasures → deferred extraction backlog
3. Extract and synthesize selected treasures into SDDs / FR docs / methodology guides

## Related Projects

- [[Brain/projects/Canary|Canary]] — the forward evolution (retail LP for Square merchants)
- [[Brain/wiki/secure-retail-career-archive|Pre-Secure Retail Career]] — earlier IBM consulting era (stubbed, deferred)
