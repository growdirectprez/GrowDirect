---
type: home
---

# GrowDirect — Second Brain

Knowledge base for GrowDirect — a solo-founder operation building SaaS tools with AI assistance. Brain is the bridge between Claude Code sessions (which build) and Cowork sessions (which strategize). Start with the project MOC for whatever you're working on.

## Projects

| Project | Status | What it is | Start here |
|---------|--------|------------|------------|
| [[Brain/projects/Canary\|Canary]] | Near-beta | Loss prevention analytics for Square merchants | [[Brain/wiki/canary-architecture\|Architecture]] |
| [[Brain/projects/Cove\|Cove]] | Early dev | HOA governance platform for WPBCA (81 lots, Abalone Cove, RPV) | [[Brain/wiki/cove-legal-framework\|Legal Framework]] |
| [[Brain/projects/Angel\|Angel]] | Active | Real estate intelligence + content engine for Compass agents (TheHillPV.com) | [[Brain/wiki/south-bay-wiki-architecture\|Wiki Architecture]] |
| [[Brain/projects/Seacove\|25 Seacove]] | Standalone | SketchUp model-building pipeline for 25 Seacove Drive | [[Brain/wiki/seacove-project\|Project Overview]] |

## Vault Structure

| Path | What's there |
|------|-------------|
| `Brain/projects/` | **Project MOCs** — start here for any project |
| `Brain/wiki/` | Synthesized knowledge articles (49 articles across all projects) |
| `Brain/playbooks/` | Repeatable workflows (neighborhood content hub pilot) |
| `Brain/raw/inbox/` | Unprocessed intake notes — content engine feeds here |
| `Brain/raw/processed/` | Processed intake notes by project |
| `Brain/templates/` | Note templates (wiki, raw-intake, decision, meeting) |
| `Brain/decisions/` | Cross-project architecture decision records |

## Content Engine

Brain intake is managed by `content-engine/engine.py`:

```bash
# Check if Brain already covers a topic before creating new docs
python3 content-engine/engine.py registry check "<topic>"

# Ingest a file into Brain raw/inbox
python3 content-engine/engine.py ingest <file> -p <project>

# Rebuild the topic registry
python3 content-engine/engine.py registry build
```

The registry (`Brain/REGISTRY.json`) indexes all wiki articles and their topics. Always check it before creating new documents.

## Key Knowledge by Project

### Cove — 10 wiki articles
Legal framework, Lot H discovery, 0 Clipper threat, community history, property geology, governance operations, city position cross-reference, PV Corp declaration scheme, platform development. Plus the [[Cove/docs/site/narrative|Story of Abalone Cove]] narrative and mapping/engineering playbooks in `Cove/docs/archive/wiki/`.

### Canary — 4 wiki articles
Architecture (16 services, MCP layer), detection engine (37 Chirp rules), data model (60+ models), sales strategy. Plus 50+ Atlas diagrams in `Canary/docs/atlas/`.

### Angel — 32 wiki articles
Architecture, data platform, content engine, market intelligence, Ninja Selling, brand & team, voice training, buyer/listing processes, transaction timeline, Compass Concierge, content archive index, weekly CRMLS pull, South Bay wiki architecture. Plus 19 neighborhood content profiles covering PVE, RPV, Rolling Hills, and South Bay.

### Seacove — 1 wiki article
[[Brain/wiki/seacove-project|Project overview]] — property history, ARC pipeline, permit context.

## System Design Documents (SDDs)

The spec layer between Brain knowledge and code. Agents should read relevant SDDs at session start to frame their work.

### Canary (25 SDDs)
[[docs/sdds/canary/architecture|Architecture]] · [[docs/sdds/canary/data-model|Data Model]] · [[docs/sdds/canary/tsp|TSP Pipeline]] · [[docs/sdds/canary/tsp-sub1|TSP Sub1 — Hash-Seal]] · [[docs/sdds/canary/tsp-sub2|TSP Sub2 — Parse-Route]] · [[docs/sdds/canary/tsp-sub3|TSP Sub3 — Merkle]] · [[docs/sdds/canary/tsp-sub4|TSP Sub4 — Chirp]] · [[docs/sdds/canary/chirp|Chirp Detection]] · [[docs/sdds/canary/fox|Fox Cases]] · [[docs/sdds/canary/owl|Owl Analytics]] · [[docs/sdds/canary/alert|Alerts]] · [[docs/sdds/canary/identity|Identity]] · [[docs/sdds/canary/identity-square|Identity-Square]] · [[docs/sdds/canary/external-identities|External Identities]] · [[docs/sdds/canary/webhook-pipeline|Webhook Pipeline]] · [[docs/sdds/canary/goose|Goose]] · [[docs/sdds/canary/raas|RaaS]] · [[docs/sdds/canary/ops|Ops]] · [[docs/sdds/canary/alx|ALX Agent]] · [[docs/sdds/canary/qa-agent|QA Agent]] · [[docs/sdds/canary/ui-bff|UI/BFF]] · [[docs/sdds/canary/analytics|Analytics]] · [[docs/sdds/canary/metrics-analytics|Metrics]] · [[docs/sdds/canary/metrics-risk-scoring|Risk Scoring]] · [[docs/sdds/canary/multi-pos-architecture-proof|Multi-POS Proof]]

### Cove (18 SDDs)
[[docs/sdds/cove/architecture|Architecture]] · [[docs/sdds/cove/member-auth|Member Auth]] · [[docs/sdds/cove/governance-engine|Governance Engine]] · [[docs/sdds/cove/governance-voting|Governance Voting]] · [[docs/sdds/cove/secret-ballot-elections|Elections]] · [[docs/sdds/cove/ballot-security|Ballot Security]] · [[docs/sdds/cove/treasury|Treasury]] · [[docs/sdds/cove/vault|Vault]] · [[docs/sdds/cove/parcel-map-engine|Parcel Maps]] · [[docs/sdds/cove/map-rendering|Map Rendering]] · [[docs/sdds/cove/meetings|Meetings]] · [[docs/sdds/cove/archive-system|Archive]] · [[docs/sdds/cove/board|Board]] · [[docs/sdds/cove/notifications|Notifications]] · [[docs/sdds/cove/knowledge|Knowledge]] · [[docs/sdds/cove/agent|Agent]] · [[docs/sdds/cove/sitemap-redesign|Sitemap Redesign]] · [[docs/sdds/cove/sitemap-redesign-issues|Sitemap Issues]]

### Angel (7 SDDs)
[[docs/sdds/angel/angel-overview|Overview]] · [[docs/sdds/angel/data-platform|Data Platform]] · [[docs/sdds/angel/angel-agent|Agent]] · [[docs/sdds/angel/web-strategy|Web Strategy]] · [[docs/sdds/angel/brand-and-launch|Brand & Launch]] · [[docs/sdds/angel/execution-plan|Execution Plan]] · [[docs/sdds/angel/lp-integration|LP Integration]]

### Platform (5 SDDs)
[[docs/sdds/platform/shared-infrastructure|Shared Infrastructure]] · [[docs/sdds/platform/aws-target-architecture|AWS Target Architecture]] · [[docs/sdds/platform/memory-bus|Memory Bus]] · [[docs/sdds/platform/factory-pipeline|Factory Pipeline]] · [[docs/sdds/platform/skill-architecture|Skill Architecture]]

### Other (3 SDDs)
[[docs/sdds/alx/mcp-service-layer|MCP Service Layer]] · [[docs/sdds/alx/test-lab|Test Lab]] · [[docs/sdds/arc/seacove-site-plan|Seacove Site Plan]]

---

## Platform Governance

- [[Brain/wiki/growdirect-workflow|GrowDirect Workflow]] — Operating manual: two agent systems, knowledge layers, session lifecycle, working style
- [[Brain/wiki/document-management|Document Management Strategy]] — The 7 document types, where they live, lifecycle rules

## Vault Health

- [[Brain/Brain Health Dashboard]] — at-a-glance Bases view of vault health
- [[Brain/wiki/brain-broken-links-baseline-2026-05-01|Broken-Links Baseline (2026-05-01)]] — known false-positive link checker noise; baseline for diff-only health checks

## Setup

See [[Brain/Setup Guide]] for first-time Obsidian setup.
