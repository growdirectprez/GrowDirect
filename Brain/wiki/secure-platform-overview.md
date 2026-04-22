---
date: 2026-04-21
type: wiki
tags: [secure, appriss, retail, loss-prevention, product-line, canary-lineage]
sources:
  - Brain/raw/inbox/secure-5-solution-architecture-docx.md
  - Brain/raw/inbox/secure-lite-overview-docx.md
  - Brain/raw/inbox/secure-omnichannel-overview-oct2018-pdf.md
  - Brain/raw/inbox/factory-overview-v2-pptx.md
  - Brain/raw/inbox/new-delivery-process-pptx.md
last-compiled: 2026-04-21
needs-review: 2026-05-05
---

**Wiki:** [[Brain/Home|Home]]

# Secure Platform Overview

## Summary

Secure was the Appriss Retail loss-prevention platform (2010s–2019), deployed on-premise at enterprise retailers. It ingested POS transaction data, applied exception-based reporting and case-management workflows, and served three user roles — Executive, Analyst, Investigator — on a Microsoft .NET + SQL Server stack. The product line expanded over time into three variants: **Secure 5** (full enterprise), **Secure Lite** (SMB turn-key configuration), and **Secure Omnichannel** (ecommerce/BOPIS risk). Canary targets the same problem space — retail loss prevention — for a different buyer (Square merchants) on different infrastructure (multi-tenant SaaS, Postgres, Python, Ollama).

## Details

### Product identity

"Secure" is the application layer. Underneath is the **Appriss Retail Platform** (ARP), the data and service fabric. The two names appear interchangeably in source material depending on audience — "Secure" in user-facing docs, "ARP" in infrastructure docs. By 2018 the platform had been rebuilt with a modern stack (.NET 4.7, SQL Server 2017, Python 3.7, Apache Lucene.NET 4.8, PostgreSQL 10.x).

### Product line (2018)

| Variant | Target buyer | Delivery model | Key constraint |
|---|---|---|---|
| Secure 5 | Enterprise retailers | On-premise, full client services engagement | Highest flexibility; largest TCO |
| Secure Lite | SMB retailers | Turn-key standard configuration, reduced client services | Fixed role templates; minimal tuning |
| Secure Omnichannel | Retailers with multi-channel presence | Extension to Secure 5 | Focused on ecommerce risk after the "buy" button |

**Secure Lite** specifically removes: file app access, report designer, user/permission management, task management, teams, data policy editing, export manager, developer mode, Job system console. SMB retailers get Executive/Analyst/Investigator roles with pre-baked dashboards and a standard risk dictionary — no consulting hours required to stand it up.

**Secure Omnichannel** adds detection for: Buy Online Return In-Store (BORIS), Buy Online Pickup In-Store (BOPIS), order cancellation from store-fulfilled orders, returns of off-range products, fictitious damaged/missing goods, resellers reserving stock, payroll time wasted on fraudulent store pickups.

### Three-role operator model

Every Secure variant ships with the same three roles. This split is durable and bears replication:

- **Executive** — dashboards, store-model outliers, case-result rollups, key-actor lookups, "quick start" questions. No investigative workflow. Read-only summary layer.
- **Analyst** — search composer, metric search, risk-dictionary searches, work-item composer, Factboard + EBR case management, CRDM access. The investigator-enabler who tunes detection and routes cases.
- **Investigator** — work items, EBR + case dashboards, case management, key-actor profile lookups, notifications + reports. Closes cases.

Canary's current operator model (merchant → admin) is flatter. The Secure three-role split is a candidate pattern for Canary when merchants scale past single-admin deployments.

### Architecture shape

See [[Brain/wiki/secure-architecture|Secure Architecture]] for depth. Summary layers:

- **Client** — Single Page Applications (jQuery, HTML5, AngularJS, CSS). Grade-A browsers: IE 10+, Chrome 60+.
- **Presentation** — Common Presentation Framework (CPF) on ASP.NET MVC 5.
- **Dynamic Messaging Service (DMS)** — internal queue from Web App to service layer.
- **Service Layer** — Windows .NET Services, C#, including the Data Service Host (DSH) running on Windows Integrated Authentication.
- **Data** — SQL Server 2017 Enterprise (required for partitioning + compression), plus PostgreSQL 10 as transient staging, Apache Lucene.NET 4.8 for search.
- **Integration** — Python 3.7 + Real Time Integrator (RTI), MSMQ for trickle feeds, SFTP/FTP/file-share for batch.

Deployment configurations: non-redundant scale (horizontal web + service farm), redundant single-datacenter (SQL Server Always On), cross-DC redundancy (VM replication between sites). Typical enterprise database sizing: 10TB on HP DL-class servers with 256GB RAM, SAS SSD arrays or NVMe for extreme IO.

### Modules (Secure 5 standard)

Administration, Dashboards, User Data, Files, Reports, Notifications, Work View, User Tasks, **EBR**, **LP Case Management**.

EBR = Exception-Based Reporting — the classic LP discipline of finding transactions that deviate from expected patterns (refunds without receipts, voids, price overrides, associate sales to themselves, etc.). This is the core of what Secure did.

### Persistence stores (CRDM + specialists)

Secure split persistence into 14 logical stores, each addressing a specific concern:

- **CRDM** (Common Retail Data Model) — the sales transaction store; the fabric everything else operates on
- **Case Management** — all case-related data
- **Factboard** — pre-case investigation notes (the "might become a case" scratchpad)
- **Job System** — async out-of-process operations
- **Membership, SSO** — users and permissions
- **Reference** — client-specific people/product/place data
- **Structure** — hierarchies (product, location)
- **Notification, Reporting, Stats, Work View, Standard Data Load, Generic Secure Schema** — specialist stores

The **CRDM abstraction** is the single most portable idea in Secure. It's a schema contract that isolates the detection/case layer from the thousand variations of retailer POS data formats. Canary's data model is the modern equivalent — same goal, different implementation.

### Loss-prevention problem model

Secure's worldview (useful as a domain reference):

- **Internal actors** — employees who commit fraud, need investigation; vs. employees with training/process issues, need retraining
- **External actors** — customers gaming return policies, wardrobing/renting, reselling stock, abusing BOPIS/BORIS
- **The "divorce customer" framing** — some customers cost more than they contribute due to fraudulent returns or habitual policy abuse; LP flags them for retailer decision
- **Shrink vectors** — internal theft, fraudulent refunds, gift-card abuse, BOPIS fraud, damaged-goods fraud, transfer-to-store abuse, inventory adjustment abuse

### What this teaches Canary

Secure is 10+ years of productized retail LP IP. Five immediate knowledge transfers (see [[docs/superpowers/briefs/2026-04-secure-to-canary-handoff|full handoff brief]] for depth):

1. **CRDM as a schema abstraction pattern** — Canary's multi-POS adapter layer is solving the same problem. Check how CRDM separates transaction storage from merchant-specific schemas.
2. **Factboard vs Case distinction** — pre-case scratchpad is a real concept. Canary's Fox cases may benefit from a Factboard analog for "watching, not yet a case."
3. **Three-role operator model** — Executive/Analyst/Investigator is a durable split when merchants grow beyond single-admin deployments.
4. **Omnichannel risk taxonomy** — BORIS/BOPIS/cancel/damaged-goods/reseller as specific fraud patterns with dedicated detection logic. Directly mappable to Canary Chirp rules.
5. **Lite variant as a pricing/delivery lever** — Secure Lite removed config surface to serve SMBs without consulting hours. Canary's merchant tier strategy can borrow this "less knobs, faster deploy" framing.

## Related

- [[Brain/projects/Secure|Secure]] — project MOC
- [[Brain/wiki/secure-architecture|Secure Architecture]] — deeper technical detail
- [[Brain/wiki/secure-lite|Secure Lite]] — SMB variant detail
- [[Brain/wiki/secure-omnichannel|Secure Omnichannel]] — ecommerce variant detail
- [[Brain/projects/Canary|Canary]] — the forward project
- [[docs/superpowers/briefs/2026-04-secure-to-canary-handoff|Secure → Canary Handoff]] — pattern-porting brief

## Sources

- `/Users/gclyle/secure/Secure 5 Solution Architecture.docx` — Appriss Retail Platform architecture, deployment options, SQL Server 2017 + SSO + CRDM
- `/Users/gclyle/secure/Secure Lite Overview.docx` — Secure Lite role definitions, what's included vs excluded vs Secure 5
- `/Users/gclyle/secure/Secure Omnichannel Overview-Oct2018.pdf` — omnichannel risk areas, BORIS/BOPIS/cancel patterns
- `/Users/gclyle/secure/Factory Overview v2.pptx` — build pipeline context
- `/Users/gclyle/secure/New Delivery Process.pptx` — release/delivery process context
- Intake notes in `Brain/raw/inbox/secure-*-*.md` + `s5-on-premise-*.md`
