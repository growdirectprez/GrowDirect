---
date: 2026-04-10
type: wiki
tags: [platform, governance, documents, brain, content-engine]
sources: [CLAUDE.md, content-engine/engine.py]
last-compiled: 2026-04-10
needs-review: 2026-05-26
---

# Document Management Strategy

Every file in GrowDirect is one of seven types. Each type has one home, one lifecycle, and one relationship to Brain. If a file doesn't fit a type, it's a session artifact and gets deleted.

## The Seven Document Types

### 1. Source Documents
**What:** Original PDFs, scans, downloaded city records. Evidence that doesn't change.
**Home:** `<Project>/docs/archive/originals/<category>/`
**Lifecycle:** Created once. Never edited. Transcriptions and analysis reference them.
**Brain link:** Cited as `sources:` in wiki articles. Never ingested directly.
**Examples:** 1949 Declaration of Easements PDF, city council staff reports, coastal commission filings, assessor maps, Seacove blueprints.

### 2. Transcriptions
**What:** Markdown versions of source documents. OCR output cleaned up into readable text.
**Home:** `<Project>/docs/archive/originals/transcriptions/`
**Lifecycle:** Created once from a source PDF. May have both verbatim (-Verbatim.md) and cleaned versions. Not edited after initial creation.
**Brain link:** Cited as `sources:` in wiki articles. Can be ingested as raw intake if they contain novel analysis.
**Naming:** Match the source PDF name exactly, lowercase with hyphens. `1949-Declaration-of-Easements.pdf` → `1949-Declaration-of-Easements.md`

### 3. Research & Analysis
**What:** Briefs, legal analysis, competitive research, investigation notes. Synthesized thinking about a topic.
**Home:** `<Project>/docs/admin/research/<topic>/`
**Lifecycle:** Created by a session. Must be ingested into Brain during the same session (rule 9). If it covers a topic Brain already has a wiki article for, update the article instead.
**Brain link:** Ingested via `content-engine/engine.py ingest`. Becomes raw intake → processed → compiled into wiki.
**Examples:** Legal brief on 0 Clipper, 501(c)(3) strategy, lot H community action brief, competitive intelligence.

### 4. Design Documents
**What:** System design docs (SDDs), specs, plans, PRDs, architecture decision records (ADRs).
**Home:**
  - SDDs: `docs/sdds/<project>/`
  - Plans: `docs/plans/<project>/`  
  - Specs: `docs/specs/<project>/`
  - Decisions: `docs/decisions/`
  - PRDs: `docs/prds/<project>/`
**Lifecycle:** Created when building a feature. Lives as long as the feature exists. When superseded, the old version is deleted (not archived — git has the history). Plans for completed work get deleted.
**Brain link:** Linked from project MOCs. SDDs are referenced in wiki articles as deep-dive sources.
**Naming:** `YYYY-MM-DD-<topic>.md` for plans/specs/decisions. `<domain>.md` for SDDs (no dates — they're living documents).

### 5. Knowledge Articles
**What:** Brain wiki articles and project MOCs. Synthesized, maintained understanding.
**Home:** `Brain/wiki/` for articles, `Brain/projects/` for MOCs.
**Lifecycle:** Compiled from raw intake notes and source documents. Updated whenever new information arrives. These are the system of record — if Brain says something, it's current.
**Brain link:** These ARE Brain. They link to everything else.
**Rules:** Every project must have at least one wiki article. A wiki article that hasn't been updated in 30 days should be reviewed.

### 6. Operational Documents
**What:** Runbooks, deploy procedures, environment setup, team profiles, configuration guides.
**Home:** `<Project>/docs/runbooks/` for project-specific. `docs/team/` for people. `devops/` for infrastructure.
**Lifecycle:** Lives as long as the system it documents. Updated when the system changes. Deleted when the system is decommissioned.
**Brain link:** Linked from project MOCs under an "Operations" section.
**Examples:** Cloudflare email routing runbook, Docker compose setup, team role profiles.

### 7. Session Artifacts
**What:** Reports, manifests, one-shot scripts, triage outputs, index files, build prompts. Anything created during a session to accomplish a task.
**Home:** Nowhere permanent. Created in the working directory, used, then deleted.
**Lifecycle:** Born and dies within a single session. If the artifact contains knowledge worth keeping, ingest it into Brain first, then delete the file. If it's a tool (like engine.py), it lives in `content-engine/`. If it's output from a tool, it gets deleted.
**Brain link:** None. If it needs one, it's not a session artifact — it's type 3, 4, or 5.
**Examples:** Duplicate reports, triage manifests, cleanup scripts, scan outputs, migration scripts, test data.

---

## Where Things Live (One Location Per Type)

```
GrowDirect/
├── Brain/
│   ├── wiki/                    ← Type 5: Knowledge articles
│   ├── projects/                ← Type 5: Project MOCs
│   ├── raw/inbox/               ← Processing queue (temporary)
│   ├── decisions/               ← Type 4: Cross-project ADRs
│   ├── templates/               ← Note templates
│   └── REGISTRY.json            ← Topic index (auto-generated)
│
├── docs/
│   ├── sdds/<project>/          ← Type 4: System design docs
│   ├── plans/<project>/         ← Type 4: Implementation plans
│   ├── specs/<project>/         ← Type 4: Specifications
│   ├── decisions/               ← Type 4: Platform-level ADRs
│   ├── team/                    ← Type 6: Team profiles
│   └── research/                ← Type 3: Platform-level research
│
├── <Project>/docs/
│   ├── archive/originals/       ← Type 1: Source documents (PDFs)
│   │   ├── <category>/          ← Organized by topic
│   │   └── transcriptions/      ← Type 2: Markdown transcriptions
│   ├── admin/research/          ← Type 3: Project-specific analysis
│   ├── runbooks/                ← Type 6: Operational procedures
│   └── site/                    ← Type 6: Public-facing content
│
├── content-engine/
│   └── engine.py                ← The tool (permanent)
│
└── devops/                      ← Type 6: Infrastructure config
```

**Everything not in this tree is either misplaced or a session artifact.**

---

## The Rules

### Rule 1: One file, one home
Every document lives in exactly one location. No copies in "convenient" second locations. If two places need it, the second place links to the first.

### Rule 2: Check Brain first
Before creating any document of type 3, 4, or 5, check whether Brain already covers the topic. Run `registry check` or search the wiki. If coverage exists, update — don't create a parallel document.

### Rule 3: Ingest or delete
Every session that produces knowledge (type 3) must either ingest it into Brain or delete it before the session ends. No loose analysis files accumulating between sessions.

### Rule 4: No archives of archives
When a design document is superseded, delete the old version. Git preserves history. Don't create `_archive/`, `v1/`, `old/`, or `deprecated/` folders. The only archive folder is for type 1 source documents (originals that came from outside the project).

### Rule 5: Flat and shallow
No directory should be more than 3 levels deep from the project root. If you need a fourth level, the structure is wrong. Use filenames for specificity, not folder nesting.

### Rule 6: Date-prefix for temporal documents
Plans, specs, decisions, and any document tied to a point in time uses `YYYY-MM-DD-<topic>.md`. Living documents (SDDs, wiki articles, runbooks) don't get date prefixes.

### Rule 7: Session artifacts die with the session
Reports, manifests, scripts, indices — if it was generated to accomplish a task and the task is done, delete it. The content engine is a permanent tool; its output is temporary.

---

## How Brain Stays Current

### The Intake Pipeline

```
New content created in a session
        │
        ▼
  Is it knowledge? ──No──▶ Is it a tool? ──No──▶ DELETE
        │                       │
       Yes                     Yes
        │                       │
        ▼                       ▼
  Check Brain registry    Keep in content-engine/
        │                 or project scripts/
        ▼
  Topic exists? ──Yes──▶ Update the wiki article
        │
       No
        │
        ▼
  Create raw-intake note in Brain/raw/inbox/
        │
        ▼
  Fill in Key Takeaways + Links
        │
        ▼
  Compile into wiki article (same session or next)
        │
        ▼
  Rebuild registry
```

### Registry Maintenance
The registry (`Brain/REGISTRY.json`) maps topics to wiki articles. It's rebuilt whenever a wiki article is created or updated. Sessions check it before creating new content. It's auto-generated — never edit it manually.

### What Brain Must Cover (Minimum)
Each active project needs at minimum:
- 1 project MOC in `Brain/projects/`
- 1 wiki article covering the architecture/what-it-is
- Wiki articles for any domain knowledge that sessions repeatedly need

Currently covered: Cove (7 articles + MOC). Missing: Canary (MOC only, no wiki articles), Seacove (MOC only).

---

## Migration Plan (Current State → Target State)

### Already done
- Content engine built with scan, dupes, triage, ingest, registry commands
- Brain registry built (10 articles, 121 topics indexed)
- Cove duplicate analysis complete (44 files identified for deletion)
- Session discipline updated in CLAUDE.md (rules 8, 9, 10)

### Needs to happen next
1. Run the Cove cleanup (44 files — exact dupes, web junk, diverged copies)
2. Move Cove plans/specs from `Cove/docs/plans/` and `Cove/docs/specs/` to `docs/plans/cove/` and `docs/specs/cove/`
3. Triage `docs/_archive/` (479 markdown files) — ingest valuable content into Brain, delete the rest
4. Write Canary wiki articles (architecture, fraud model, alert pipeline)
5. Consolidate team profiles (merge `Canary/docs/profiles/ops/` into `docs/team/`, delete dupes)
6. Prune `.claude/skills/` to skills that are actually used
7. Delete `docs/_archive/` once everything valuable has been extracted

### How sessions enforce this going forward
Every Cowork session that touches documents should:
1. Start: `registry check "<topic>"` — know what Brain already has
2. Work: Create documents in their canonical locations (not wherever is convenient)
3. End: Ingest knowledge into Brain, delete artifacts, rebuild registry if wiki changed
