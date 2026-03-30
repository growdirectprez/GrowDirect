---
name: war-chest
version: "2.0"
description: |
  The War Chest is GrowDirect's single-source-of-truth content system. It manages a canonical
  library of .md source files, builds three output targets from them (investor pack, investor
  single-page site, public site), supports section-level updates that cascade to all outputs,
  and tracks published versions like a CMS. MANDATORY TRIGGER: war chest, the pack, briefing
  site, content pack, rebuild the deck, growdirect.io pack, update the war chest, push to the
  pack, refresh the site, what's in the pack, show me the manifest, list the sections.
---

# War Chest v2.0 — GrowDirect Content System

The War Chest is three things:

1. **The Catalog** — a canonical library of .md source files that IS the knowledge base
2. **The Builder** — compiles those sources into polished HTML outputs for different audiences
3. **The Publisher** — versions and deploys published pages like a CMS

Every piece of outward-facing content — investor briefings, the public site, API docs, LEO assets — traces back to a .md source in the War Chest. When the source changes, downstream outputs rebuild. When an output is ready, it gets published with a version stamp.

---

## File Locations

| What | Where |
|---|---|
| Manifest | `_ALX/WarChest/manifest.json` |
| Source files | `_ALX/WarChest/sources/` |
| Build script | `_ALX/WarChest/skill/scripts/build_site.py` |
| **Output: Pack** | `_ALX/WarChest/site/` |
| **Output: Investor** | `_ALX/WarChest/outputs/investor/` |
| **Output: Public** | `_ALX/WarChest/outputs/public/` |
| Published versions | `_ALX/WarChest/published/` |
| Archive (pack) | `_ALX/WarChest/archive/` |
| Deploy target | `_deploy/growdirectprez.github.io/` |
| Skill definition | `_ALX/WarChest/skill/SKILL.md` |

---

## 1. The Catalog

### Structure

Every section in the War Chest has a .md or .html source file in `sources/`. The manifest registers every section with its metadata. If a section exists in the manifest but the source file is missing, that's a **content gap** — it needs to be written.

### manifest.json

The manifest is the contract. It defines:

- **sections** — the content catalog (what exists, where it lives, who it's for)
- **outputs** — the build targets (what gets compiled, from which sections, in what format)
- **published** — the version registry (what's been released, when)

```json
{
  "title": "GrowDirect — War Chest",
  "version": "1.0",
  "last_built": "2026-02-27T16:10:00",
  "sections": [
    {
      "order": 1,
      "name": "The Pitch",
      "slug": "the-pitch",
      "source": "sources/01-the-pitch.md",
      "description": "Investor story — problem, solution, economy, market, vision",
      "audience": "investor",
      "last_updated": "2026-02-27",
      "feeds": ["pack", "investor"]
    }
  ],
  "outputs": {
    "pack": {
      "format": "multi-page",
      "gated": true,
      "password": "eljeffe2026",
      "dir": "site/",
      "version": "0.7"
    },
    "investor": {
      "format": "single-page",
      "gated": true,
      "password": "eljeffe2026",
      "dir": "outputs/investor/",
      "version": "3.0",
      "template": "growdirect_investor"
    },
    "public": {
      "format": "multi-page",
      "gated": false,
      "dir": "outputs/public/",
      "deploy": "_deploy/growdirectprez.github.io/",
      "version": "1.0"
    }
  },
  "published": {
    "investor": [
      { "version": "3.0", "date": "2026-02-27", "file": "published/investor/v3.0.html" }
    ],
    "pack": [
      { "version": "0.6", "date": "2026-02-27", "dir": "archive/v0.6/" }
    ],
    "public": []
  }
}
```

### Section Fields

| Field | Type | Description |
|---|---|---|
| `order` | int | Display sequence across all outputs |
| `name` | string | Human-readable section title |
| `slug` | string | URL-safe identifier (used for filenames) |
| `source` | string | Path to source file relative to WarChest/ |
| `description` | string | One-line summary (appears in TOC, nav, index) |
| `audience` | enum | `investor`, `technical`, `internal`, `press`, `public` |
| `last_updated` | date/null | When the source was last modified. Null = content gap |
| `feeds` | array | Which outputs this section flows into: `["pack", "investor", "public"]` |
| `embed_mode` | string | For .html sources: `full` (copy as-is) or omit (extract body + wrap in template) |

### Content Sections (current catalog)

| # | Section | Source | Audience | Status | Feeds |
|---|---|---|---|---|---|
| 01 | The Pitch | `01-the-pitch.md` | investor | Written | pack, investor |
| 02 | elJeffe | `02-eljeffe.html` | investor | Written | pack |
| 03 | The Economy | `03-the-economy.html` | investor | Written | pack, investor |
| 04 | The Play | `04-the-play.md` | investor | Written | pack |
| 05 | The Product | `05-the-product.html` | investor | Written | pack |
| 06 | The Fox | `06-the-fox.md` | investor | Written | pack, investor |
| 07 | The Goose | `07-the-goose.md` | investor | Written | pack, investor |
| 08 | The Owl | `08-the-owl.md` | investor | Written | pack, investor |
| 09 | Investment Thesis | `09-investment-thesis.md` | investor | **GAP** | pack, investor |
| 10 | The Architecture | `10-the-architecture.md` | technical | **GAP** | pack |
| 11 | The Data Model | `11-the-data-model.md` | technical | **GAP** | pack |
| 12 | How We Build | `12-how-we-build.md` | internal | **GAP** | pack |
| 13 | The Team | `13-the-team.md` | investor | **GAP** | pack, investor, public |
| 14 | Compliance | `14-compliance.md` | investor | **GAP** | pack, investor |
| 15 | Protection | `15-protection.md` | investor | **GAP** | pack, investor |
| 16 | The Article | `16-the-article.md` | press | **GAP** | pack, public |

**Content gap** means the section is registered but the source file hasn't been written yet. Run `list --gaps` to see what's missing.

### Source File Rules

- Every source file lives in `_ALX/WarChest/sources/`
- .md files are converted to HTML by the build script (markdown → styled HTML)
- .html files with `embed_mode: full` are copied as-is (standalone interactive pages)
- .html files without embed_mode have their body extracted and wrapped in the page template
- No internal agent names in any source file. Ever.
- Naming: elJeffe (no space), gLog (no space), tLog (lowercase t), jeffe.io

---

## 2. The Builder

### Output Targets

The War Chest builds three outputs from the same source catalog:

#### Pack (multi-page briefing)
- **What:** Password-gated multi-page HTML site. Index with TOC → individual section pages.
- **Where:** `_ALX/WarChest/site/`
- **Includes:** ALL sections in the manifest (complete catalog)
- **Design:** Dark theme, Bebas Neue headers, DM Sans body, Space Mono labels, Bitcoin orange/gold accents, grain overlay, watermark
- **Gate:** Client-side password (`eljeffe2026`)
- **Use:** Private briefing — send the folder, recipient enters code, browses all sections

#### Investor (single-page site)
- **What:** Single scrolling HTML page with all investor-audience content compiled into one narrative flow. Matches `growdirect_investor_v3.0.html` format.
- **Where:** `_ALX/WarChest/outputs/investor/`
- **Includes:** Sections tagged with `feeds: ["investor"]` — assembled in order as one continuous page
- **Design:** Same visual language as pack but single-page with section nav, hero, and footer
- **Gate:** Client-side password
- **Use:** The investor brief — one file, one link, password-gated. Currently deployed to `_deploy/growdirectprez.github.io/investor.html`

#### Public (growdirect.io)
- **What:** The public-facing website. Multi-page, no password gate.
- **Where:** `_ALX/WarChest/outputs/public/` → deployed to `_deploy/growdirectprez.github.io/`
- **Includes:** Sections tagged with `feeds: ["public"]` — curated subset, public-safe language
- **Design:** Modern public site style (Inter/Space Grotesk, dark theme, gold accents)
- **Gate:** None — public internet
- **Use:** growdirect.io — what the world sees. Includes index, about, API docs landing

### Build Commands

```
rebuild                              # Full rebuild of ALL outputs
rebuild --output pack                # Rebuild only the pack
rebuild --output investor            # Rebuild only the investor site
rebuild --output public              # Rebuild only the public site

update --section [slug]              # Update one section's source → rebuild all outputs that include it
update --section the-pitch           # Example: update The Pitch, cascades to pack + investor

add --name "Name" --source path.md   # Add a new section to the manifest
add --name "API Docs" --source sources/17-api-docs.md --audience technical --feeds pack

remove --section [slug]              # Remove a section from manifest (source file NOT deleted)

list                                 # Show full catalog with status
list --gaps                          # Show only sections missing source files
list --output investor               # Show sections that feed the investor output
```

### Build Process

1. Read `manifest.json`
2. For each output target:
   a. Filter sections by `feeds` array (which sections go into this output)
   b. Sort by `order`
   c. For each section: read source → convert .md to HTML (or copy .html)
   d. Wrap in output-specific template (multi-page with nav, or single-page scroll)
   e. Apply design system (fonts, colors, gate if configured)
   f. Write to output directory
3. Update `manifest.json` with build timestamp and version

### Design System

All outputs share the core visual language:

| Token | Value | Usage |
|---|---|---|
| Background | `#080808` | Page background |
| Cards | `#141414` | Card/panel background |
| Borders | `#1e1e1e` | Dividers, card borders |
| Text | `#E8E4DC` | Primary body text |
| Muted | `#8a8a8a` | Secondary text, labels |
| Bitcoin Orange | `#F7931A` | Primary accent, links |
| Gold | `#FBBF24` | Secondary accent, gradients |
| Green | `#22C55E` | Positive indicators |
| Red | `#EF4444` | Alerts, errors |
| Headers | Bebas Neue | Uppercase, letter-spacing 0.12em, gradient fill |
| Body | DM Sans | Weight 300, line-height 1.7 |
| Labels/Code | Space Mono | 10px, uppercase, letter-spacing 0.15em |
| Quotes | DM Serif Display | Italic |
| Grain | Fractal noise SVG | Opacity 0.02, fixed overlay |
| Gate | Bebas Neue logo + Space Mono input | Client-side JS password |

---

## 3. The Publisher

### Versioning Model

Each output has its own version number. Versions are tracked in `manifest.json` under `published`.

| Output | Current | Next on publish |
|---|---|---|
| Pack | 0.6 | 0.7 |
| Investor | 3.0 | 3.1 |
| Public | — | 1.0 |

### Publish Commands

```
publish --output investor            # Snapshot current investor build → published/investor/v3.1.html
publish --output pack                # Snapshot current pack → published/pack/v0.7/
publish --output public              # Copy to deploy target → published/public/v1.0/

publish --output investor --major    # Major version bump: v3.1 → v4.0
```

### Publish Process

1. Build the output (if not already current)
2. Copy output to `published/[output]/v[version]/`
3. Increment version in manifest
4. Log the publish in `manifest.json → published`
5. For public output: copy to `_deploy/growdirectprez.github.io/` and commit

### Published Directory Structure

```
published/
├── investor/
│   ├── v2.1.html                    # Previous investor site
│   ├── v3.0.html                    # Current investor site
│   └── latest.html                  # Always points to newest
├── pack/
│   ├── v0.5/                        # Previous full pack
│   ├── v0.6/                        # Current full pack
│   └── latest/                      # Always points to newest
└── public/
    ├── v1.0/                        # First public site release
    └── latest/                      # Always points to newest
```

---

## 4. Section-Level Updates

This is the cascade mechanism. When you say "update the pitch," here's what happens:

```
INPUT: "update --section the-pitch"
  │
  ▼
READ manifest.json
  → Section "the-pitch" has feeds: ["pack", "investor"]
  │
  ▼
REBUILD affected outputs only:
  ├─ Pack: regenerate the-pitch.html, update nav across all pack pages
  └─ Investor: recompile full single-page (the-pitch content updated in place)
  │
  ▼
UPDATE manifest.json
  → the-pitch.last_updated = today
  → pack.last_built = now
  → investor.last_built = now
```

The `feeds` array on each section is the routing table. Change a section's source file → the builder knows exactly which outputs need to rebuild.

### Workflow: Rework a Section

1. Edit the source .md in `sources/`
2. Run `update --section [slug]`
3. Builder reads the updated source, regenerates HTML for all outputs that include it
4. Review the rebuilt outputs
5. When satisfied, `publish --output [target]` to snapshot the new version

### Workflow: Add New Content

1. Write the .md file to `sources/`
2. Run `add --name "Section Name" --source sources/XX-slug.md --audience investor --feeds pack,investor`
3. Manifest updates with new section
4. Run `rebuild` to generate all outputs with the new section
5. Review → `publish`

---

## 5. Integration with Agent Dispatches

When a B-series work order produces content (PhD writes a brief, Syd reviews compliance language, Art creates diagrams), the output routes to the War Chest:

### Ingest Flow

```
Work order deliverable (e.g., PhD Brief 5)
  │
  ▼
ALX reviews: Does this update an existing section or create a new one?
  │
  ├─ UPDATE: Copy content into existing sources/XX-slug.md → run update --section [slug]
  └─ NEW: Write sources/XX-new-section.md → run add → run rebuild
  │
  ▼
Review built outputs → publish when approved
```

### Agent Roles in War Chest Pipeline

| Agent | War Chest Role |
|---|---|
| PhD | Writes/updates narrative .md source files |
| Art | Produces visual assets (SVG diagrams embedded in .html sources) |
| Syd | Reviews all content before publish — no publish without Syd sign-off |
| Jess | Builds custom visual sections (.html with embed_mode) |
| Jeremy | Updates API documentation sources |
| Will | Updates LEO terms and agent-readable descriptions |
| ALX | Orchestrates: triggers builds, routes content, manages manifest |

### Syd Gate

**No output publishes without Syd's review.** The `publish` command requires Syd sign-off as a precondition. Build freely. Publish only after legal review.

---

## 6. Naming Standards (non-negotiable)

- **elJeffe** — no space, always
- **gLog** — no space, always
- **tLog** — lowercase t, always
- **jeffe.io** — the API domain
- `jeffe.io/glog` — the canonical gLog API endpoint
- No virtual team member names in any external-facing content
- No file paths, classification markings, or internal references in outputs
- All external-facing copy uses investor/public language, never internal jargon

---

## 7. Quality Checks

After every build, verify:

1. Password gate works (for gated outputs)
2. Navigation links work across all pages (pack)
3. Section anchors work (investor single-page)
4. No broken source references (all sources in manifest exist)
5. No internal agent names in external-audience sections
6. Version stamp is current
7. Design system is consistent (colors, fonts, spacing match tokens)
8. Muted text is readable (min `#8a8a8a` — never darker for body text)

---

## 8. Content Gap Tracker

Sections registered in the manifest with `last_updated: null` are content gaps. These need to be written before the War Chest is complete.

### Current Gaps (as of Feb 27, 2026)

| Section | Source Needed | Feed From |
|---|---|---|
| Investment Thesis | `09-investment-thesis.md` | PhD Brief 5 (B-054) |
| The Architecture | `10-the-architecture.md` | Tom's architecture docs + Art's diagrams |
| The Data Model | `11-the-data-model.md` | CRDM v1.0 spec |
| How We Build | `12-how-we-build.md` | Factory Process v1.0 |
| The Team | `13-the-team.md` | Sanitized team overview (no agent names) |
| Compliance | `14-compliance.md` | Syd's B-058 legal memo (Option B language) |
| Protection | `15-protection.md` | Patent filing, IP strategy docs |
| The Article | `16-the-article.md` | Long-form Canary narrative |

### Priority Order for Gap Fill

1. **Investment Thesis** — PhD Brief 5 is written, just needs formatting as War Chest source
2. **Compliance** — Syd's Option B language from B-058 is approved, needs packaging
3. **Protection** — Patent filing language exists, needs external-facing version
4. **The Architecture** — Art's gLog architecture diagrams are done, needs narrative wrap
5. **The Data Model** — CRDM v1.0 exists, needs investor-facing summary
6. **The Team** — Needs to be written fresh (sanitized, no agent names)
7. **How We Build** — Factory Process exists, needs external-facing version
8. **The Article** — Long-form, lowest priority until other gaps filled

---

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | Feb 27, 2026 | Initial skill created from WarChest pack builder |
| 2.0 | Feb 27, 2026 | Complete redesign: unified catalog, three output targets, section-level cascade, CMS versioning, content gap tracker |

---

*War Chest Skill v2.0 — ALX, February 27, 2026*
*The catalog is the knowledge base. The outputs are the products. The manifest is the contract.*
