---
date: 2026-04-22
type: wiki
tags: [growdirect, working-papers, ip-vault, warchest, numbering-scheme]
sources:
  - docs/_archive/ip-vault/warchest/WORKING_PAPERS.md
  - docs/_archive/ip-vault/warchest/manifest.json
  - docs/_archive/ip-vault/strategy/GrowDirect_Manifesto_v1.1.md
  - docs/_archive/ip-vault/strategy/PITCH_SPINE_v0.4.md
last-compiled: 2026-04-22
needs-review: 2026-05-06
---

**Wiki:** [[Brain/Home|Home]]

# GrowDirect Working Papers — Structure

## Summary

Every piece of GrowDirect intellectual property has a permanent address in a 7-domain tree. The address never changes. Content moves through states; the address stays. Doctrine flows top-down — the Manifesto changes first, War Chest sources update from it, outputs rebuild from sources. Work fills it in bottom-up. The War Chest is the directory where this IP lives; the Working Papers index is how to navigate it.

## Details

### Address format

```
WP-[DOMAIN].[CHAPTER].[SECTION]
```

Example: `WP-1.1.N` = Narrative domain, Chapter 1 (The Pitch), first Narrative asset.

### The 7 domains (top-level, permanent)

| Domain | Code | Scope |
|---|---|---|
| The Narrative | **WP-1** | Founder story, pitch, vision, article — external-facing prose |
| The Product | **WP-2** | Canary modules, features, UX, interactive prototypes |
| The Architecture | **WP-3** | CRDM, pipeline, databases, gLog, security, infrastructure |
| The Business | **WP-4** | Market, model, economics, thesis, financials |
| The Shield | **WP-5** | Compliance, IP, legal, regulatory, contracts |
| The Operations | **WP-6** | Process, team, sprint methodology, DevOps |
| The Reference Library | **WP-7** | API docs, schemas, code index, data dictionary, research |

Domains are permanent. Chapters and sections evolve; the domain names do not.

### Asset type suffixes (on files, not WP numbers)

| Suffix | Type | Example |
|---|---|---|
| `.N` | Narrative | `WP-1.1.N` — prose, investor-facing markdown |
| `.S` | Schema | `WP-3.2.S` — DDL, ERD, migration files |
| `.A` | API | `WP-3.1.A` — endpoint definitions, Swagger/OpenAPI |
| `.C` | Code | `WP-2.1.C` — module structure, key implementation files |
| `.V` | Visual | `WP-1.1.V` — diagrams, SVGs, interactive HTML |
| `.D` | Data | `WP-3.2.D` — sample data, fixtures, field mappings |
| `.L` | Legal | `WP-5.1.L` — contracts, assessments, filings |
| `.R` | Research | `WP-4.1.R` — briefs, analysis, position papers |
| `.T` | Test | `WP-2.1.T` — QA plans, test suites, scenarios |
| `.O` | Operations | `WP-6.3.O` — deployment configs, infrastructure scripts |
| `.P` | PRD | `WP-2.1.P` — product requirements documents |

One address can hold multiple asset types. `WP-1.1.N` and `WP-1.1.V` both live at Chapter 1 of the Narrative; one is prose, one is a visual.

### Status markers

| Marker | Meaning |
|---|---|
| `EXISTS` | File exists, mapped, content is current |
| `DRAFT` | File exists, needs editing before external use |
| `STUB` | Node defined, no content yet — to be written |
| `PLANNED` | On roadmap, not yet scoped |
| `CONFIDENTIAL` | Exists but restricted distribution — not for external outputs |

### Output targets

| Target | Description |
|---|---|
| `pack` | War Chest multi-page gated briefing |
| `investor` | Single-page investor site |
| `public` | growdirect.io public site |
| `internal` | Team reference only |
| `diligence` | Investor due diligence room |
| `legal` | Attorney/legal review only |

Each asset declares which output targets it feeds. A single `WP-1.1.N` might feed `pack + investor`; a `WP-5.1.L` probably feeds `diligence + legal` only.

### War Chest numbering (source-file layer)

The War Chest is the filesystem at `docs/_archive/ip-vault/warchest/`. Source files use a two-digit numeric prefix matching the **Pitch Spine** narrative order (not the WP-X domain order):

| Range | Act | What |
|---|---|---|
| 00–09 | OPEN + Acts 1–3 | Demo, Why, What |
| 10–19 | Act 4 | How We Make Money — 7 Layers |
| 20–29 | Act 5 | How It's Built — Technology |
| 30–39 | Acts 6–7 | Moat + Numbers |
| 40–42 | Act 8 + Close | Ask + Sovereignty |
| 45–54 | Supporting detail | In War Chest but not in Pitch Spine |
| 90–93 | Utility | Disclaimer, changelog, issues, references |

49 source files currently live in `warchest/sources/` — from `00-the-demo.md` through `91-changelog.md`. Each maps to one or more WP addresses via the manifest.

### Version lock

The Manifesto and the War Chest track major-version locked together:

> **Manifesto v1.x → War Chest v3.x**
> **Manifesto v2.x → War Chest v4.x**

**Rule:** Manifesto updates first. War Chest sources update from it. Outputs rebuild from sources.

Current state: Manifesto v1.2, War Chest v3.1 (restructured 2026-02-27 to match Pitch Spine v0.4).

## How to use this

### When starting a new deliverable

1. Find the WP-X address it maps to (what domain + chapter + section). If no address exists yet, it's probably a STUB candidate — decide whether to register it.
2. Check the manifest for the declared asset type suffix and output targets.
3. Draft into the appropriate source file (or new file under `warchest/sources/`).
4. Outputs rebuild from sources — don't hand-edit generated pack/investor pages.

### When the thinking changes

1. Update the **Manifesto** first (it's the master source).
2. Identify which War Chest sources are affected.
3. Update those source files.
4. Rebuild outputs.

**Do not** edit an output page (pack, investor, public) directly. It will lose the edit on the next rebuild.

### When ingesting new material (intake protocol)

1. Say "I have GrowDirect working papers to process" (per [[CLAUDE.md|platform CLAUDE.md]]).
2. Point at the binary or directory.
3. Extract + ingest runs; intake notes land in `Brain/raw/inbox/` with source-path frontmatter.
4. Synthesize: decide which WP address the new material belongs to, write or update the relevant source file.
5. Optionally: update the Manifesto if the new material changes doctrine.

## Related

- [[Brain/projects/GrowDirect|GrowDirect MOC]]
- [[docs/_archive/ip-vault/warchest/WORKING_PAPERS|WORKING_PAPERS.md — master index]]
- [[docs/_archive/ip-vault/warchest/manifest.json|manifest.json — machine-readable spine]]
- [[docs/_archive/ip-vault/strategy/GrowDirect_Manifesto_v1.1|GrowDirect Manifesto]] — the master source
- [[docs/_archive/ip-vault/strategy/PITCH_SPINE_v0.4|Pitch Spine v0.4]] — the narrative the War Chest is built around
- [[docs/_archive/ip-vault/strategy/PRODUCTION_CHAIN_v0.1|Production Chain v0.1]] — Manifesto → sources → outputs pipeline
- [[CLAUDE.md|Platform CLAUDE.md]] — Documentation as Code principle + Intake Protocol

## Sources

Full source paths in frontmatter. Primary:

- `docs/_archive/ip-vault/warchest/WORKING_PAPERS.md` — numbering scheme, domain list, asset type table, status markers, full WP-X directory
- `docs/_archive/ip-vault/warchest/manifest.json` — machine-readable version (War Chest v3.1)
- `docs/_archive/ip-vault/strategy/GrowDirect_Manifesto_v1.1.md` — the doctrine; version lock rules
- `docs/_archive/ip-vault/strategy/PITCH_SPINE_v0.4.md` — the narrative order driving the 00–93 file numbering
