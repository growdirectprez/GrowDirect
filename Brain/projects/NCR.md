---
type: project-moc
status: active
external-repo: https://github.com/growdirect-llc/ncr
external-site: https://ncr.growdirect.io
audience: NCR Counterpoint VARs — Rapid Garden POS + channel
local-clone: none (clone-on-demand only — see CLAUDE.md "External Vaults — Clone on Demand")
tags: [ncr, counterpoint, var, partner-vault, public-vault, rapidpos]
---

# NCR — Canary for NCR Counterpoint (VAR Partner Vault)

Co-sell enablement site for NCR Counterpoint VARs. Serves Rapid Garden POS (Bart McCleskey) as the lead channel partner, expanding to the full Counterpoint VAR ecosystem. Content originates in `GrowDirect/Brain/` and is curated outward — not authored directly in this repo.

Served at: https://ncr.growdirect.io
Source repo: https://github.com/growdirect-llc/ncr

## What it covers

Two lanes:

**Partner lane (commercial):** Vertical playbooks (L&G full, others stubbed), why-canary positioning, pitch assets.

**Technical lane:** L1–L4 process decomposition of the 13-module Canary Retail Spine on the RapidPOS L&G backbone. Counterpoint API surface (endpoint families, Document omnibus, adapter notes). Sandbox access path.

## Site sections

- [Home](https://ncr.growdirect.io) — co-sell overview
- [Verticals](https://ncr.growdirect.io/verticals/lawn-garden) — L&G playbook (full) + 4 vertical stubs
- [Modules](https://ncr.growdirect.io/modules/index) — L1–L4 spine decomposition (13 modules; Q and J ship with full L4 content)
- [Why Canary](https://ncr.growdirect.io/why-canary/index) — positioning, TAM, gap map
- [Integration](https://ncr.growdirect.io/integration/index) — Counterpoint API surface
- [Sandbox](https://ncr.growdirect.io/sandbox/index) — path to demo
- [Pitch](https://ncr.growdirect.io/pitch/index) — leave-behinds (in production)

## Build stack

Quartz v4 + counterpoint-teal accent (`#0B6E8B`). Deployed via GitHub Actions on push to `main`. CNAME: ncr.growdirect.io.

## Architecture rationale

See `Brain/dispatches/2026-04-26-three-vault-jekyll-pages-architecture.md` and `docs/superpowers/specs/2026-04-26-ncr-vault-design.md`.

## Content sourcing map

| Vault section | Brain sources |
|---|---|
| `verticals/lawn-garden` | `garden-center-operating-reality`, `rapid-pos-counterpoint-user-pain-points`, `socal-home-garden-target-customers-brief` |
| `why-canary/` | `voyix-counterpoint-rapid-pos-engagement-context`, `rapid-pos-counterpoint-market-research-tam`, `canary-raas-positioning` |
| `integration/` | `ncr-counterpoint-api-reference`, `ncr-counterpoint-document-model`, `ncr-counterpoint-endpoint-spine-map` |
| `modules/` | All 13 `canary-module-*-functional-decomposition.md` cards + `canary-module-q-counterpoint-rule-catalog` |
| `sandbox/` | `ncr-counterpoint-connection-runbook`, `ncr-counterpoint-sandbox-setup-checklist` |

## Pending content (from 2026-04-27 card research session)

27 research cards from a Cowork session covering NCR overview, financials, leadership, roadmap, tech debt, competitors, RapidPOS full profile, POS market, and more. To be ingested into Brain/wiki/ and then curated into the NCR vault via a synthesis pass.

## Wiki Articles

### Functional Decomposition
- [[Brain/wiki/ncr-counterpoint-functional-decomposition|NCR Counterpoint Full Functional Decomposition]] — atom-level feature map: 18 modules, 95 forms, 50+ reports, API gap analysis; UX source for Canary Go screen design

### Integration & Sandbox
- [[Brain/wiki/ncr-counterpoint-api-reference|NCR Counterpoint API Reference]] — endpoint families, authentication, Document omnibus
- [[Brain/wiki/ncr-counterpoint-document-model|NCR Counterpoint Document Model]] — API Document object taxonomy
- [[Brain/wiki/ncr-counterpoint-endpoint-spine-map|Endpoint × CRDM × Spine Map]] — 200+ endpoints cross-referenced to Canary data model
- [[Brain/wiki/ncr-counterpoint-connection-runbook|Connection Runbook]] — step-by-step setup for sandbox and production API access
- [[Brain/wiki/ncr-counterpoint-sandbox-setup-checklist|Sandbox Setup Checklist]] — operator action checklist for standing up the NCR sandbox
- [[Brain/wiki/ncr-counterpoint-phase-0-context-brief|Phase 0 Context Brief]] — session context brief for the NCR Counterpoint integration sprint

### Engagement Context
- [[Brain/wiki/voyix-counterpoint-rapid-pos-engagement-context|Voyix / Counterpoint / Rapid POS Engagement Context]] — channel partner background
- [[Brain/wiki/bart-mccleskey-rapid-garden-pos|Bart McCleskey — Rapid Garden POS]] — lead VAR contact profile
- [[Brain/wiki/rapid-pos-counterpoint-market-research-tam|RapidPOS / Counterpoint Market Research + TAM]] — market sizing and TAM analysis
- [[Brain/wiki/rapid-pos-counterpoint-user-pain-points|RapidPOS / Counterpoint User Pain Points]] — user pain points and FAQs
- [[Brain/wiki/ncr-rapidpos-alignment-notes|NCR Vault–RapidPOS Alignment Notes]] — Hawk Phase 1 alignment notes

### Reference Cases & Workflows
- [[Brain/wiki/murdochs-workflow-cards-user-stories-scenarios|Murdoch's — Workflow Cards, User Stories, Scenarios]] — farm/ranch reference case (firearms, live animals, BOPIS)

## Related

- [[Brain/projects/CATz]] — method vault (how GrowDirect works)
- [[Brain/projects/CanaryRetailBrain]] — product vault (Canary spine, vendor-neutral)
- [[Brain/projects/Canary]] — Canary app project MOC (code and SDDs)
- [[Brain/wiki/bart-mccleskey-rapid-garden-pos]] — lead VAR contact
- [[Brain/wiki/voyix-counterpoint-rapid-pos-engagement-context]] — engagement context
