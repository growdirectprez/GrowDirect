---
type: project-moc
status: active
tags: [growdirect, company, working-papers, ip-vault, strategy]
---

# GrowDirect

GrowDirect Inc. — the solo-founder holding company behind Canary, Cove, Angel, and future apps. This MOC indexes the company-level IP: the Manifesto, working papers, strategy docs, white papers, and press artifacts. Not an app MOC — those live at [[Brain/projects/Canary|Canary]], [[Brain/projects/Cove|Cove]], [[Brain/projects/Angel|Angel]].

## Status

Active. Manifesto v1.2 is the master source. War Chest v3.x is the current IP tree, version-locked to the Manifesto. Work flows top-down: doctrine changes in the Manifesto first, War Chest sources update from it, outputs rebuild from sources.

## Wiki Articles

- [[Brain/wiki/growdirect-working-papers|Working Papers Structure]] — WP-[DOMAIN].[CHAPTER].[SECTION] numbering, 7 domains, asset type suffixes (.N/.S/.A/.C/.V/.D/.L/.R/.T/.O/.P), status markers, output targets

(More to come. Clipper-style: we add wikis as we process working papers. Organize and optimize as we go.)

## Working Papers — Master Index

Live at [[docs/_archive/ip-vault/warchest/WORKING_PAPERS|WORKING_PAPERS.md]] in the IP vault. Machine-readable manifest at [[docs/_archive/ip-vault/warchest/manifest.json|manifest.json]]. Current version: War Chest v3.1 (restructured 2026-02-27 to match Pitch Spine v0.4).

## 7 Domains

- **WP-1 The Narrative** — Founder story, pitch, vision, article. External-facing prose.
- **WP-2 The Product** — Canary modules, features, UX, interactive prototypes.
- **WP-3 The Architecture** — CRDM, pipeline, databases, gLog, security, infrastructure.
- **WP-4 The Business** — Market, model, economics, thesis, financials.
- **WP-5 The Shield** — Compliance, IP, legal, regulatory, contracts.
- **WP-6 The Operations** — Process, team, sprint methodology, DevOps.
- **WP-7 The Reference Library** — API docs, schemas, code index, data dictionary, research.

## Strategy Documents

Live at [[docs/_archive/ip-vault/strategy/|ip-vault/strategy/]]. 10 docs covering doctrine, positioning, and operational strategy.

- `GrowDirect_Manifesto_v1.0.md` + `v1.1.md` — the master source (v1.2 is latest; file says v1.1, header says v1.2 — version drift to resolve)
- `Canary_Strategic_Thesis_v1.0.md`
- `Canary_Attack_Plan_v3.0.md`
- `Canary_Factory_Process_v1.0.md` — precedent for the [[docs/sdds/platform/factory-pipeline|Factory Pipeline SDD]]
- `Canary_Data_Strategy_NorthStar_v1.0.md`
- `Chirp_UDQ_Branch_Strategy_v1.0.md`
- `CompetitiveIntel_Oracle_OCI_Polling.md`
- `PITCH_SPINE_v0.4.md` — the spine the War Chest is built around
- `PRODUCTION_CHAIN_v0.1.md`

## White Papers

Live at [[docs/_archive/ip-vault/white-papers/|ip-vault/white-papers/]]. Binaries (`.docx`), ingest candidates via `engine.py extract`:

- Canary White Paper v1.3
- Canary Competitive Landscape
- Canary Micropayment Strategy Position Paper v1.0
- Canary Quant Peer Review v1.0

## Research Papers (top-level)

Already in markdown at `docs/_archive/ip-vault/`:

- `Canary_Bitcoin_Architecture_Research_Paper_v1.0.md`
- `Canary_Reference_Library_v1.0.md`
- `Cannabis_Retail_Risk_Dictionary_v1.0.md`
- `WORM_Exposure_Sprint_Deliverables.md`
- `glossary.md`

## Patent Visuals, Press, Sales, Team

Subdirectories at `docs/_archive/ip-vault/`:

- `patent-visuals/` — diagrams supporting IP filings
- `press/` — press-facing artifacts (requires Legal review before external use)
- `sales/` — sales-enablement material
- `Team/` — team documents
- `timelogs/` — time-tracking

## Applications Built on GrowDirect IP

- [[Brain/projects/Canary|Canary]] — retail loss prevention for Square merchants (primary commercial product)
- [[Brain/projects/Cove|Cove]] — HOA governance platform (first deployment: WPBCA, Abalone Cove, RPV)
- [[Brain/projects/Angel|Angel]] — real estate intelligence for Compass agents (Cove module + Angel knowledge repo)
- [[Brain/projects/Seacove|Seacove]] — SketchUp modeling pipeline (standalone demo)
- [[Brain/projects/Secure|Secure]] — archival retail LP IP from IBM / Appriss / Sysrepublic (career-lineage reference)

## Platform Method

The method that runs across all apps. Lives at [[Brain/projects/Method|Method MOC]] with [[Brain/projects/Factory|Factory Pipeline]] as the operational layer.

## Intake Protocol (active)

Working papers flow into Brain via the [[CLAUDE.md|platform CLAUDE.md intake protocol]]. Say "I have GrowDirect working papers to process" and the pipeline runs: extract → ingest → register → synthesize.

## Principles

- **Documentation as Code** — SDDs → chunked memories → wikis → code. Top-down doctrine, bottom-up work. See [[CLAUDE.md|platform CLAUDE.md]].
- **Manifesto first, outputs rebuild** — War Chest pipeline respects the version lock. Don't edit outputs that should rebuild from source.
- **One address forever** — WP numbering is permanent. Content moves through states; the address stays.

## Related

- [[CLAUDE.md|Platform CLAUDE.md]] — Rule zero, Documentation as Code, Intake Protocol
- [[Brain/projects/Method|Method MOC]] — the how-work-happens layer
- [[Brain/projects/Factory|Factory Pipeline]] — the 9-stage machinery
