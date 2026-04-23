---
date: 2026-04-21
type: wiki
tags: [secure, architecture, appriss, sso, saml, oidc, factory, delivery-process, canary-lineage]
sources:
  - Brain/raw/inbox/s5-on-premise-solution-architecture-docx.md
  - Brain/raw/inbox/s5-on-premise-solution-architecture-v1-1-draft-docx.md
  - Brain/raw/inbox/secure-5-solution-architecture-docx.md
  - Brain/raw/inbox/sso-overview-v2-docx.md
  - Brain/raw/inbox/factory-overview-v2-pptx.md
  - Brain/raw/inbox/new-delivery-process-pptx.md
  - Brain/raw/inbox/dev-ops-docx.md
  - Brain/raw/inbox/dev-ops-deliverables-pptx.md
last-compiled: 2026-04-21
needs-review: 2026-05-05
---

**Wiki:** [[Brain/Home|Home]]

# Secure Architecture

## Summary

Secure was a five-layer enterprise web application on the Microsoft .NET + SQL Server stack: client SPA → ASP.NET MVC presentation → Dynamic Messaging Service → .NET service layer (Data Service Host) → SQL Server 2017 data layer, with a Python/PostgreSQL integration layer feeding CRDM. Identity was federated via SAML 2.0 or OpenID Connect with role mapping through assertions. The Factory was the build-pipeline repository consolidating all Secure 3.5 apps. The New Delivery Process (NDP, Oct 2018) was the organizational reform aligning quote-to-contract-to-invoice with fewer hand-offs.

## Details

### Physical architecture tiers

**Client tier.** Single Page Applications built in jQuery, HTML5, AngularJS, CSS. Grade-A browser support: IE 10+, Chrome 60+. JavaScript required. Fonts loaded from site for glyph-like icons.

**Presentation tier.** Common Presentation Framework (CPF) on ASP.NET MVC 5 + .NET 4.7. Web Application servers are horizontally scaled, load-balanced. Windows Server 2016 + IIS 7.5 / 8.5.

**Dynamic Messaging Service (DMS).** Internal queue layer passing messages from Web App to Data Service Host. MSMQ under the hood when trickle feeds are in play.

**Service tier.** Windows .NET Services + C#. Two kinds:
- **Common Services** — shared across Appriss Retail Platform apps
- **Secure Services** — Secure-specific
Plus the **Data Service Host (DSH)** — a single Windows service that hosts Appriss Retail databases (SQL exposure) and runs all hosted services under one umbrella. DSH uses Windows Integrated Authentication; each operation has an AD-group ACL. Each web server + DSH maintains an in-memory cache ("Memory Vault").

**Data tier.** SQL Server 2017 Enterprise Edition (partitioning + compression require Enterprise). PostgreSQL 10.x for transient integration staging. Apache Lucene.NET 4.8 for search.

**Integration tier.** Python 3.7 + Real Time Integrator (RTI) 4 cores / 8GB. Collects/receives data via SFTP, FTP, file share, or MSMQ. An "ingest persistence" tier (Windows or Linux, Python + PostgreSQL) processes received data into the appropriate repository.

### Deployment configurations

| Shape | Use | Key features |
|---|---|---|
| Non-redundant scale | Development, non-mission-critical prod | Horizontal web + service farm on VMs |
| Redundant single-DC | Prod with uptime requirements | SQL Server Always On Highly Available Group |
| Cross-DC redundancy | Prod with DR requirements | VM replication between sites, single HA group spanning DCs |

Typical enterprise prod database specs: HP DL-class server, 4× Intel Gold 6154 (18-core, 3.0GHz), 256GB RAM (8× 16GB DDR4-2666), 22× HPE 960GB SAS SSDs, HPE Smart Array P816i-a RAID controller. Storage: RAID5 for IO optimization across spindles; SanDisk Fusion IO for extreme-IO workloads; NVMe for latest-generation deployments. Network: 10GbE inter-server, 16GbE fiber channel to SAN.

### CRDM + persistence stores

The data layer is split into 14 logical stores. This decomposition is the most portable architectural idea in Secure:

| Store | Purpose |
|---|---|
| **CRDM** | Common Retail Data Model — sales transaction data over which Secure operates |
| Reference | Client-specific People / Product / Place data |
| Case Management | All case-related data |
| Factboard | Pre-case investigation scratch (watching, not yet a case) |
| Job System | Async chronological operations |
| Membership | Users, permissions |
| SSO | Single Sign On state |
| Notification | Generated from monitors |
| Standard Data Load | Load progress logging |
| Stats | Metrics, report/search stats |
| Structure | Hierarchies (product, location) |
| Generic Secure Schema | Repository + language resources, logging, user activity |
| Reporting | Report generation |
| Work View | Work View items |

**CRDM as abstraction contract.** CRDM isolates the detection/case layer from thousand-variant retailer POS data formats. Data comes in via Standard Data Load (SDL), lands in the staging PostgreSQL, gets mapped and enriched through the integration tier, then persists in CRDM-shaped SQL Server tables. Everything upstream of CRDM is ETL; everything downstream operates on the stable CRDM shape.

### Identity: SAML 2.0 + OpenID Connect

Secure supports federated identity via two protocols:

- **SAML 2.0** — Service-Provider-Initiated workflow. Assertion includes NameID, attributes for role mapping, signed response. Secure is the SP; retailer IdP is the source of truth for identity.
- **OpenID Connect (OIDC)** — token-based, JSON, used where SAML is overkill or where modern IdPs (Okta, Azure AD) prefer OIDC.

**Role assignment** happens in two modes:
- **SSO-driven** — the assertion/token includes role claims that map to Secure roles (Executive / Analyst / Investigator + subtypes)
- **Manual** — Secure admin assigns roles post-SSO-bind

This dual-protocol + dual-assignment model is the kind of identity flexibility enterprise retailers require. Canary's magic-link + Square-OAuth identity model is simpler by design (SMB buyer); if Canary ever sells to enterprise, SAML is the path.

### The Factory

Factory = a **single consolidated repository** for all Secure 3.5 applications. Not just source — a full operational pre-configured install with features, dashboards, reports, and searches working together on a common foundation. Covered apps:

- **EBR** (Exception-Based Reporting — the core)
- **Cashier Performance**
- **Audit & Survey**
- **Refund Management**
- **Foundation Management** (users, roles, locations, products, people)
- **Incident Management**
- **Risk Management** (internal, external, digital)

Adjacent surfaces: BOLO (Be On the Look Out), Giftcards, MoneyGram, ORC (Organized Retail Crime), Known Loss, Rewards.

Factory philosophy: ship one pre-wired install, not a dozen independent components to be stitched. This reduces implementation time and standardizes what "Secure 3.5" means for any client. Canary's approach to Chirp rule packs + default dashboard is a direct analog — opinionated defaults, opt-out of pieces, not opt-in.

### New Delivery Process (NDP, Oct 2018)

NDP was the organizational reform aligning Appriss Retail's quote-to-contract-to-invoice flow. The problem it solved: too many people in every meeting, unclear accountability, quality incidents at specific mid-market accounts where hand-off gaps produced rework. Scope of the reform:

- Define the org model and reporting lines
- Clarify accountability from quote → contract → delivery → invoice
- Standardize data ingest and product surface so role requirements shrink
- Reach 10% labor efficiency target, reinvest half in R&D

Forecast at the time: ~12 Secure projects per year (new accounts + conversions) + ~4 Verify/Incent projects + ~$1M of SOW work. This scale defined the right-sizing exercise.

The relevant-to-Canary piece is the **standardization** push: if the product is pre-wired (see Factory above), the delivery engagement gets much shorter and the role coverage model shrinks. Canary is designed for self-serve merchants — no engagement at all in the small end — so the NDP lesson is "every optional configuration step costs delivery labor; default everything."

### Server accounts + DB permissions (reference)

Windows service accounts per environment: `DevSecureStoreSVC`, `CertSecureStoreSVC`, `SecureStoreSVC`. Local Admin recommended. Permissions: Run Services, MSMQ r/w/d, file shares r/w/d, app directories r/w/d.

Database roles:
- **CRDM staging**: SELECT, UPDATE, EXECUTE, DROP, TRUNCATE, RESEED, INSERT, DELETE
- **Application DBs (all)**: SELECT, UPDATE, INSERT, DELETE, EXECUTE
- **CRDM prod**: full DDL (CREATE/DROP VIEW, ALTER PROCEDURE, ALTER FUNCTION, SWITCH PARTITION, CREATE/DROP INDEX)
- **EXPRESS DB**: DROP/CREATE TEMP TABLES, ALTER + REBUILD INDEX

### Development + test environments

Each prod environment requires two non-prod siblings:
- **Development** — landing + local config changes. VMs for web + integration, shared DB server. Explicit policy: no PII or card tokens; PCI-compliant sample data only.
- **Test / Certification** — where changes are tested before production promotion.

### What this teaches Canary

- **Persistence decomposition** — 14 logical stores is probably too many for a multi-tenant SaaS, but the principle (case data separate from factboard-scratch separate from reference data separate from sales transactions) is sound. Canary has `app/sales/fox/metrics` schemas — fewer, but the same pattern.
- **CRDM abstraction layer** — a stable schema contract between "raw retailer data" and "detection logic" is the single most portable idea. Canary's multi-POS proof is solving the same problem; Secure's CRDM is prior art worth studying.
- **Identity flexibility** — SAML + OIDC + manual-assignment as a three-way identity model is an enterprise pattern Canary can adopt later. Current Canary is correctly simpler for its SMB target.
- **Factory philosophy** — ship opinionated defaults, not a la carte. Canary's Chirp pack defaults should be stronger.
- **NDP lesson** — every configuration step costs delivery labor. Default everything, let power users tune.

## Related

- [[Brain/projects/Secure|Secure]] MOC
- [[Brain/wiki/secure-platform-overview|Secure Platform Overview]]
- [[Brain/wiki/secure-lite|Secure Lite]] — config restriction pattern
- [[Brain/wiki/secure-omnichannel|Secure Omnichannel]] — module extension pattern
- [[Brain/projects/Canary|Canary]] — forward project
- [[docs/superpowers/briefs/2026-04-secure-to-canary-handoff|Secure → Canary Handoff]]

## Sources

- `/Users/gclyle/secure/Secure 5 Solution Architecture.docx` — physical architecture, tiers, deployment, SQL/HP specs
- `/Users/gclyle/secure/S5 On Premise Solution Architecture.docx` / `v1.1 Draft.docx` — earlier architecture drafts
- `/Users/gclyle/secure/SSO Overview v2.docx` — SAML 2.0 + OIDC federated identity (Jerry Caldwell + Geoff Lyle authors)
- `/Users/gclyle/secure/Factory Overview v2.pptx` — Secure 3.5 Factory consolidated build
- `/Users/gclyle/secure/New Delivery Process.pptx` — Oct 2018 org reform
- `/Users/gclyle/secure/Dev Ops.pptx`, `Dev Ops Deliverables.pptx` — ops context
