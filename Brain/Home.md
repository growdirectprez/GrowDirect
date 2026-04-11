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
| [[Brain/projects/Seacove\|25 Seacove]] | Standalone | SketchUp model-building pipeline for 25 Seacove Drive | [[Brain/projects/Seacove\|Blueprints]] |

## Vault Structure

| Path | What's there |
|------|-------------|
| `Brain/projects/` | **Project MOCs** — start here for any project |
| `Brain/wiki/` | Synthesized knowledge articles (16 articles, 353 indexed topics) |
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
Legal framework, Lot H discovery, 0 Clipper threat, community history, property geology, governance operations, city position cross-reference, PV Corp declaration scheme, platform development. Plus the [[Cove/docs/site/narrative|Story of Abalone Cove]] narrative.

### Canary — 4 wiki articles
Architecture (16 services, MCP layer), detection engine (29 Chirp rules), data model (60+ models), sales strategy. Plus 50+ Atlas diagrams in `Canary/docs/atlas/`.

### Angel — 1 wiki article + playbook
South Bay wiki architecture. Neighborhood content hub playbook in `Brain/playbooks/`. Content pools in `Angel/knowledge/content-pools/`.

## Platform Governance

- [[Brain/wiki/growdirect-workflow|GrowDirect Workflow]] — Operating manual: two agent systems, knowledge layers, session lifecycle, working style
- [[Brain/wiki/document-management|Document Management Strategy]] — The 7 document types, where they live, lifecycle rules

## Setup

See [[Brain/Setup Guide]] for first-time Obsidian setup.
