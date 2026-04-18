---
type: project-moc
status: development
tags: [cove, governance, hoa, wpbca]
---

# Cove

Community governance platform for WPBCA (West Portuguese Bend Community Association). 81 lots at Abalone Cove, Rancho Palos Verdes. Davis-Stirling compliant HOA management with modules for elections, treasury, parcels, meetings, and document vault.

## Status
In Development. Foundation rebuild in progress (GRO-346).

---

## Wiki — Start Here

| [[Brain/wiki/cove-baughey-1947|Baughey 1947]] | PV Corp's own historian: Dominguez (1784) → Sepulveda → Bixby → Vanderlip chain of title. Primary source. |
| [[Brain/wiki/cove-lrpmp|LRPMP]] | Full RDA property inventory, Horan Agreement, federal/state encumbrances, easement index, landslide data |
| [[Brain/wiki/cove-rpv-redevelopment-conveyance|RPV Redevelopment Conveyance]] | 2014 transfer of 11 govt-use properties (incl. Shoreline Park) from Successor Agency to city via LRPMP |
These articles synthesize the full archive into navigable knowledge:

| Article | What it covers |
|---------|---------------|
| [[Brain/wiki/cove-legal-framework|Legal Framework]] | The CC&R chain (1949-2012), enforcement authority, housing law analysis |
| [[Brain/wiki/cove-lot-h-discovery|Lot H Discovery]] | The key finding — 1950 declaration covering hundreds of parcels |
| [[Brain/wiki/cove-0-clipper|0 Clipper Road]] | The threat, the developer, the lawsuit, the counter-proposal |
| [[Brain/wiki/cove-community-history|Community History]] | Tongva to Vanderlip to Shore Club to today |
| [[Brain/wiki/cove-property-geology|Property & Geology]] | Landslide complex, parcel maps, geological hazards |
| [[Brain/wiki/cove-governance|Governance & Operations]] | WPBCA structure, 501(c)(3) strategy, 90-day action plan |
| [[Brain/wiki/cove-city-positions|City Positions Cross-Reference]] | What the city says vs what we say, by topic — catch contradictions |
| [[Brain/wiki/cove-pv-declaration-scheme|PV Corp Declaration Scheme]] | Olmsted legacy, Declaration 100/101, Art Jury, the coverage gap |
| [[Brain/wiki/claim-lot-h-scope-correction|Lot H Scope Correction]] | CORRECTION: Lot H Declaration only had racial language, not building restrictions |
| [[Brain/wiki/cove-platform|Platform Development]] | Tech stack, architecture, modules, SDDs |

---

## The Story
- [[Cove/docs/site/narrative|The Story of Abalone Cove]] — the full member-facing narrative

---

## Mapping & Engineering Operations

Project-specific playbooks and references in `Cove/docs/archive/wiki/`:

- `SOURCE-REGISTER.md` — Master index of all source documents for Clipper lot research
- `11-mapping-engineering/survey-monuments.md` — Survey monument reference
- `11-mapping-engineering/coordinate-reference.md` — Coordinate transforms (DXF to WGS84)
- `11-mapping-engineering/PLAYBOOK-FIELDBOOK-TO-ANCHOR.md` — Field book to anchor point workflow
- `PLAYBOOK-DEED-TO-LAYER.md` — Deed description to polygon layer workflow
- `11-mapping-engineering/adjacency-map.md` — Parcel adjacency relationships
- `11-mapping-engineering/snap-rules.md` — Polygon snapping rules

---

## Source Archive

### PV Corp Declarations (1929) — County Recorder Originals
- [[Cove/docs/archive/originals/transcriptions/1929-Declaration-100-Basic-Protective-Restrictions-Verbatim|Declaration No. 100 — Basic Protective Restrictions (Verbatim)]] — Book 9436, Pg 155. Constitutional framework (~20% legible)
- [[Cove/docs/archive/originals/transcriptions/1929-Declaration-101-Local-Protective-Restrictions-Verbatim|Declaration No. 101 — Local Protective Restrictions (Verbatim)]] — Book 9482, Pg 37. Seven parcels, restrictions (~75% legible)
- Photos: `Cove/docs/archive/originals/property/county-recorder-declarations/` (38 JPEGs)
- Verified survey: `Cove/scripts/survey/data/1929-declaration-101-seven-parcels.yaml`

### Founding Documents (1949-1952)
- [[Cove/docs/admin/research/founding/1949-declaration-of-easements|1949 Declaration of Easements]]
- [[Cove/docs/admin/research/founding/1949-modification-of-restrictions|1949 Modification of Restrictions]]
- [[Cove/docs/admin/research/founding/1950-declaration-one-a|1950 Declaration One-A]]
- [[Cove/docs/admin/research/founding/1952-grant-deed-lot-1|1952 Grant Deed Lot 1]]

### Governance
- [[Cove/docs/legal/governance/2009-restated-declaration|2009 Restated Declaration]]
- [[Cove/docs/legal/governance/2012-bylaws|2012 Bylaws]]

### Litigation (Case 24TRCP00352)
- [[Cove/docs/legal/litigation/2024-08-fppc-complaint|FPPC Complaint]]
- [[Cove/docs/legal/litigation/2024-09-petition-filed|Petition Filed]]
- [[Cove/docs/legal/litigation/2024-09-summons|Summons]]
- [[Cove/docs/legal/litigation/2024-09-case-assignment|Case Assignment]]
- [[Cove/docs/legal/litigation/2024-11-city-demurrer|City Demurrer]]
- [[Cove/docs/legal/litigation/2024-12-opposition-to-demurrer|Opposition to Demurrer]]

### Property & Geological Records
- [[Cove/docs/archive/property/rpv-zone2-landslide-eir-geology|Zone 2 Landslide EIR — Geology]]
- [[Cove/docs/archive/property/laca-parcel-maps-tract-14649|LA County Parcel Maps — Tract 14649]]
- [[Cove/docs/archive/property/2026-ctc-title-report-0-clipper|CTC Title Report — 0 Clipper]]
- [[Cove/docs/archive/property/2015-title-report-25-seacove|Title Report — 25 Seacove]]
- [[Cove/docs/archive/property/1985-assessor-map-7573-7|1985 Assessor Map]]

### Shore Club Archives
- [[Cove/docs/archive/originals/shore-club/1972-karshner-proposal|1972 Karshner Proposal — Condos vs Park]]
- [[Cove/docs/archive/originals/shore-club/1972-abalone-cove-fact-sheet|1972 Fact Sheet]]
- [[Cove/docs/archive/originals/shore-club/1972-corporate-archives|Corporate Archives]]
- [[Cove/docs/archive/originals/shore-club/1929-1963-incorporation|Shore Club Incorporation]]

### Analysis & Strategy
- [[Cove/docs/legal/briefs/legal-brief-0-clipper|Legal Brief — 0 Clipper]]
- [[Cove/docs/legal/briefs/lot-h-community-action-brief|Lot H Community Action Brief]]
- [[Cove/docs/legal/briefs/legal-risk-assessment|Legal Risk Assessment]]
- [[Cove/docs/legal/briefs/501c3-strategy|501(c)(3) Strategy]]
- [[Cove/docs/legal/briefs/counter-proposal|Counter-Proposal — Abalone Shore Community Campus]]
- [[Cove/docs/legal/briefs/ccc-access-conflicts-research|CCC Access Conflicts Research]]
- [[Cove/docs/legal/briefs/lot-h-negative-image-research|Lot H Negative Image Research]]
- [[Cove/docs/legal/briefs/pv-corp-delaware-search-2026-03-25|PV Corp Delaware Search]]

---

## System Design Documents (18 SDDs)

### Core
- [[docs/sdds/cove/architecture|Architecture]] — Platform overview, modules, deployment
- [[docs/sdds/cove/member-auth|Member Auth]] — Magic link login, Flask-Login, session management
- [[docs/sdds/cove/sitemap-redesign|Sitemap Redesign]] — Role-gated navigation
- [[docs/sdds/cove/sitemap-redesign-issues|Sitemap Issues]] — Issue specifications

### Governance & Elections
- [[docs/sdds/cove/governance-engine|Governance Engine]] — Proposal lifecycle, Davis-Stirling
- [[docs/sdds/cove/governance-voting|Governance Voting]] — Vote casting, tallying, quorum
- [[docs/sdds/cove/secret-ballot-elections|Secret Ballot Elections]] — Election orchestration, envelope scheme
- [[docs/sdds/cove/ballot-security|Ballot Security]] — RLS policies, cryptographic proofs

### Modules
- [[docs/sdds/cove/treasury|Treasury]] — Assessments, payments, ledger
- [[docs/sdds/cove/vault|Vault]] — Document storage, access tiers
- [[docs/sdds/cove/parcel-map-engine|Parcel Map Engine]] — 5,514 APNs, GeoJSON, Leaflet
- [[docs/sdds/cove/map-rendering|Map Rendering]] — Tract maps, rendering pipeline
- [[docs/sdds/cove/meetings|Meetings]] — Meeting management, ARC reviews
- [[docs/sdds/cove/board|Board]] — Board-only operations, bulletins
- [[docs/sdds/cove/notifications|Notifications]] — Delivery routing, email
- [[docs/sdds/cove/archive-system|Archive System]] — Document viewer, knowledge chunks

### AI & Knowledge
- [[docs/sdds/cove/knowledge|Knowledge]] — pgvector legal search, MCP server
- [[docs/sdds/cove/agent|Agent]] — AI Q&A assistant

## Plans & Specs
- [[Cove/docs/plans/2026-03-24-foundation-rebuild|Foundation Rebuild Plan]]
- [[Cove/docs/plans/2026-03-24-apn-data-platform|APN Data Platform Plan]]
- [[Cove/docs/plans/2026-03-24-covenant-matrix-map|Covenant Matrix Map Plan]]
- [[Cove/docs/plans/2026-03-24-sprint-identity|Sprint Identity Plan]]
- [[Cove/docs/plans/2026-03-25-sprint-cleanup-and-delivery|Sprint Cleanup Plan]]
- [[Cove/docs/plans/2026-03-26-meetings-arc|Meetings Arc Plan]]
- [[Cove/docs/specs/2026-03-26-apn-master-data-model|APN Master Data Model Spec]]
- [[Canary/docs/superpowers/plans/2026-03-23-cove-mvp|Cove MVP Plan]]
- [[Canary/docs/superpowers/specs/2026-03-23-cove-governance-platform-design|Governance Platform Design Spec]]

## Runbooks
- [[Cove/docs/runbooks/cloudflare-email-routing|Cloudflare Email Routing]]
