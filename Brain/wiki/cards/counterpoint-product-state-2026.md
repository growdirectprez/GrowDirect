---
card-type: market-intelligence
card-id: counterpoint-product-state-2026
card-version: 1
domain: platform
layer: cross-cutting
status: approved
agent: ALX
tags: [counterpoint, ncr-voyix, product-architecture, migration, 2026, secure-pay, voyix-connect, sql-server, maintenance-mode, smb-retail]
last-compiled: 2026-05-01
needs-review: false
---

## What this is

The 2026 product state of NCR Counterpoint — architecture, pricing model, active compliance forcing function (October 2026 migration deadline), and investment posture as of current intelligence. The product layer beneath the ecosystem card; read [[ncr-ecosystem-2026]] first for corporate context.

## Purpose

Understanding Counterpoint as a product — not just as a market category — tells Canary what it is integrating with, where the seams are, and why the installed base is fragile. The October 2026 forcing function is the most actionable near-term signal.

## Architecture

**Stack.** Counterpoint runs on Microsoft .NET (C#), ServiceStack for the REST API layer, and Microsoft SQL Server as the database engine (SQL Server 2016+ in most active deployments). The client applications are Windows-native. The on-premise deployment model is the default; most installations run on a Windows Server inside the store building. The "store as mini data center" pattern is the practical reality: the store server holds the POS database, transaction history, inventory ledger, and customer records.

**API surface.** The Counterpoint REST API (CPAPI) v2.4 exposes 71 paths, 95 documented operations across 9 functional groups: Administrative, Customers, Documents (transactions), ECom (ecommerce bridge), GiftCards, Inventory, Stores, System, and Workstations. The OpenAPI-derived spec lives at `docs/sdds/canary/ncr-counterpoint-openapi.yaml`. Of the 95 endpoints, approximately 25 matter for Canary steady-state adapter coverage; the remainder are setup, admin, and edge-case operations.

**Data model anchors.** Key tables (SQL Server naming convention): `PS_DOC_HDR` (transaction header), `IM_ITEM` (item master), `AR_CUST` (customer), `PS_STR` (store), `EC_*` (ecommerce bridge tables), `SY_*` (system tables). The Module T adapter reads `PS_DOC_HDR` directly from SQL Server for transaction ingestion — faster than REST and available offline. The REST API is used for cloud-side operations where latency is acceptable.

**Architecture vintage.** The .NET/SQL Server/on-premise pattern is 2000s-era enterprise architecture. ServiceStack was added as a REST façade over what is fundamentally a client-server SQL application. This is not a criticism; it is an accurate characterization of what the product is. The architecture is well-understood, stable, and predictably integrated. It is also not a cloud-native SaaS platform and cannot be made into one without a full rewrite — which is not happening (see investment posture below).

## Pricing Model

**License structure.** Counterpoint is sold as a perpetual software license with an annual maintenance contract. Typical license pricing:

- Single-station entry license: $2,000–$4,000
- Multi-station / multi-user: adds per-seat or per-workstation increments; $500–$1,500 per additional station
- Annual maintenance (required for updates and support): 18–22% of license value per year

**Full deployment economics (per site, mid-market estimate):**

| Component | Typical range |
|-----------|--------------|
| Software license | $4,000–$15,000 |
| Annual maintenance | $800–$3,000/year |
| Implementation (VAR billable) | $5,000–$25,000 |
| Hardware (server + POS terminals) | $8,000–$30,000 |
| Annual support (VAR contract) | $1,500–$6,000/year |
| **Total first-year** | **$18,000–$79,000** |
| **Annual run rate (yr 2+)** | **$2,300–$9,000** |

**Revenue to Voyix per site.** License + maintenance, net of VAR margin: Voyix realistically captures $1,500–$5,000/year per active site in software revenue. At the estimated 5,600–15,000 US Counterpoint sites, annualized Voyix Counterpoint software revenue is approximately $8.4M–$75M. The wide range reflects uncertainty in active-vs-lapsed maintenance contracts and VAR margin structures.

**The maintenance contract is the leverage point.** Sites on lapsed maintenance cannot upgrade without paying to reinstate. Sites facing the October 2026 migration (see below) must be on active maintenance to get v8.6.5+. VARs have meaningful pricing power in this renewal cycle — and meaningful cross-sell leverage for adjacent platforms.

## The October 2026 Forcing Function

**What is happening.** NCR Secure Pay, the payment processing middleware embedded in Counterpoint, is being retired. Replacement: NCR Voyix Connect (Voyix's next-generation payment integration layer). The cutover deadline is October 2026.

**Requirement.** Counterpoint v8.6.5 or later is required to connect to Voyix Connect. Sites running v8.6.4 or earlier will lose card processing capability when Secure Pay is decommissioned. Card processing is not optional for a retail POS. October 2026 is a hard wall.

**Scale of the affected population.** Any Counterpoint site that has not actively maintained updates since the v8.6.5 release is affected. No public data exists on the version distribution of the installed base, but the pattern is predictable: smaller sites on thin IT budgets, running stable deployments for years without updates, are the most likely to be on pre-v8.6.5. The sites most likely to be affected are exactly the SMB specialty retailers in the Canary ICP.

**The VAR workload implication.** Upgrading from a legacy Counterpoint version is not a patch. It involves:
- Version compatibility review (custom modifications, third-party integrations, hardware drivers)
- Database schema migration
- Payment processor reconfiguration
- Staff retraining on any UI changes
- Testing in a staging environment before live cutover

For a VAR managing hundreds of accounts, October 2026 is a high-volume forced-service event. Every one of those sites is a relationship touch. The VAR who owns the migration conversation owns the renewal conversation, the hardware refresh conversation, and any "what comes after Counterpoint?" conversation.

**The Canary insertion point.** The migration conversation is the natural moment to introduce Canary's intelligence layer. "While we're in there, let's wire up the analytics layer so you can see what's actually happening in your stores." The bar is low: Canary adds value without disrupting the Counterpoint installation. No rip-and-replace. No parallel migration. Low friction.

## Investment Posture

**What Counterpoint is receiving.** Sustaining engineering: security patches, payment compliance updates (including the October 2026 migration itself), bug fixes, and maintenance of existing features. The product team has not announced new capabilities, new modules, or architectural modernization.

**What Counterpoint is not receiving.** Strategic investment. New module development. Cloud-native migration. Any of the capabilities in the Voyix Commerce Platform (microservices, cloud-native architecture, grocery/c-store feature depth). NRF 2026 confirmed this: Voyix's new retail investment is in Voyix Commerce Platform, which targets enterprise grocery/c-store/fuel — not SMB specialty retail.

**The upgrade trap.** Counterpoint customers have no upgrade path to Voyix Commerce Platform. The new platform is not a Counterpoint replacement; it is a different product for different customer profiles. An SMB specialty retailer on Counterpoint who wants "the new Voyix product" has nowhere to go within the Voyix ecosystem. This is the moat Canary can walk through: when the installed base realizes the vendor's investment is aimed elsewhere, the loyalty that kept them from evaluating alternatives begins to erode.

**Technology debt trajectory.** The .NET/SQL Server/on-premise architecture will continue to run. It is not going to break. But it will fall progressively further behind cloud-native alternatives in capabilities: real-time analytics, mobile management, multi-store visibility, API-first integrations. The debt is not a cliff; it is a slow gradient. Over a 3-5 year horizon, the capability gap relative to modern retail platforms will become visible to Counterpoint customers without anyone at Voyix doing anything dramatic. The architecture documents what the product is; the trajectory documents where it's going.

## Version Minimum Summary

| Version | Status | Notes |
|---------|--------|-------|
| v8.6.5+ | Required by Oct 2026 | Voyix Connect compatible; current active maintenance stream |
| v8.6.4 and earlier | End of payment processing | Secure Pay EOL; loss of card processing after October 2026 |
| v8.5.x and earlier | Long-tail risk | May require paid maintenance reinstatement before upgrade is available |

## Related

- [[ncr-ecosystem-2026]] — corporate structure context; Candescent divestiture; Voyix Commerce Platform investment signal; read this first
- [[counterpoint-var-landscape]] — VAR channel; the October 2026 migration service opportunity at scale
- [[icp-murdochs-reference]] — canonical enterprise-scale ICP; item authorization + firearms compliance demonstrates where Counterpoint's architecture falls short for complex assortments
- [[retail-item-authorization]] — the unified salability gate that Counterpoint's POS parameter files approximate manually
- Brain/wiki/ncr-counterpoint-phase-0-context-brief.md — Phase 0 technical dispatch; CRDM×spine mapping; adapter architecture
- docs/sdds/canary/ncr-counterpoint-openapi.yaml — derived OpenAPI spec; 71 paths, 95 operations
