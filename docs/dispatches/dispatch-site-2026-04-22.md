---
classification: confidential
owner: GrowDirect LLC
---

# Dispatch: Static Site Updates — 2026-04-22
## For: Claude Code session in growdirectprez.github.io repo

**Context:** The static sites (growdirect.io + canary.growdirect.io) are now
maintained in the `growdirectprez.github.io` GitHub Pages repo, separate from
the GrowDirect monorepo. The last site build in the monorepo was at commit
`52d58bb` (before removal at `8efaf62`). Source War Chest HTML files are in
the GrowDirect monorepo at commit `fd3db16` under
`docs/_archive/ip-vault/warchest/site/`.

---

## Task 1: Restore + Reformat Canary Technical Library

### Source files (GrowDirect repo, commit fd3db16)

Restore these War Chest HTML source files and reformat them into a clean
Technical Library with a shared `canary-docs.css` stylesheet:

| War Chest source file | → Library document title |
|---|---|
| `the-crdm.html` | The CRDM — Canonical Reference Data Model |
| `the-architecture.html` | Platform Architecture |
| `how-we-build.html` | How We Build — The Factory |
| `eljeffe.html` | El Jeffe — Detection Protocol |
| `the-chirp.html` | The Chirp — Detection Engine |

Also pull the large roadshow doc from commit `fd3db16`:
- `docs/_archive/workorders/output/docs/canary_technical_roadshow_v1.0.html`

### Reformat rules

1. **Preserve real content.** Do NOT regenerate or rewrite body text. Extract
   the actual HTML content from each War Chest file and wrap it in the new
   template. These are authored documents — treat them as source of truth.
2. **Shared stylesheet:** Create `css/canary-docs.css` with the GrowDirect
   dark theme (#060608 bg, #FBBF24 gold accents, Space Grotesk headings,
   Inter body, Space Mono for code/labels).
3. **Document template:** Each doc gets a consistent nav header linking to all
   5 library docs + back to canary.growdirect.io. Footer with copyright.
4. **File naming:** Use human-readable names, not developer-hyphenated slugs.
   - `The CRDM.html`, `Platform Architecture.html`, `How We Build.html`,
     `El Jeffe Protocol.html`, `The Chirp Engine.html`,
     `Technical Roadshow.html`
5. **Nav consistency:** Every doc's nav links must match every other doc's nav.
   Test by opening each file and clicking through.

### Output location

Place in `docs/` directory of the GitHub Pages repo:
```
docs/
  The CRDM.html
  Platform Architecture.html
  How We Build.html
  El Jeffe Protocol.html
  The Chirp Engine.html
  Technical Roadshow.html
css/
  canary-docs.css
```

---

## Task 2: Update canary.growdirect.io Gated Section

In `canary/index.html`, update the password-gated section (password: `canary2026`):

1. **Add clickable document links** to each of the 6 Technical Library docs
   formatted as a clean card grid or link list.
2. **Remove any sales strategy / pricing content** from the gated section —
   this is for technical deep-dives only.
3. **Add a "Launch Demo" button** that links to `https://dev.growdirect.app`
   (the live Canary development site). Style it prominently — gold/orange CTA.

---

## Task 3: Add Portfolio Section to growdirect.io Hub

In `index.html` (the growdirect.io hub page), add a **Portfolio** section
with case study cards for each project. Place it ABOVE the contact/footer
section. **Remove the "What's Built" section entirely** — the Portfolio
replaces it.

### Case study cards

**Canary LP** — Loss Prevention Analytics
- Tagline: "Real-time loss prevention for Square merchants"
- Key stats: 29 detection rules, 8 categories, 3 execution tiers
- Tech highlights: PostgreSQL 17, pgvector, Triple Subscriber Pipeline
- Link: canary.growdirect.io

**Cove** — HOA Governance Platform
- Tagline: "Modern governance for Abalone Cove homeowners"
- Key stats: 81 lots, parcel-level GIS mapping, Leaflet.js integration
- Tech highlights: Flask + SQLAlchemy, interactive map UI, document management
- Link: (coming soon)

**Angel** — Real Estate Intelligence
- Tagline: "AI-powered lead generation for Compass agents"
- Key stats: Property analysis, market intelligence, automated outreach
- Tech highlights: Ollama embeddings, pgvector similarity search, agent sidecar
- Link: (coming soon)

**Consulting & Advisory**
- Tagline: "Solo founder, full-stack builder"
- Description: 20+ years building data platforms, from enterprise architecture
  to startup MVPs. Specializing in Python/PostgreSQL stacks, real-time event
  processing, and AI-augmented development workflows.
- Notable: Built entire GrowDirect platform with AI pair programming
  (Claude Code + Cowork). Every line of code, every architecture decision,
  every deployment — one founder, one AI.

### Design guidelines

- Dark card grid matching GrowDirect brand (#060608 bg, subtle grain texture)
- Gold accent borders or hover effects (#FBBF24)
- Bebas Neue or DM Serif Display for card headings
- Inter for body text
- Each card should feel substantial but scannable

---

## Task 4: Commit and Deploy

1. Commit all changes to `growdirectprez.github.io` with a clear message
2. Push to trigger GitHub Pages deployment
3. Verify both sites render correctly:
   - https://growdirect.io — hub with new Portfolio section, no "What's Built"
   - https://canary.growdirect.io — gated section with doc links + demo button
   - All 6 Technical Library docs load with consistent nav and styling

---

## Git references (GrowDirect monorepo)

To restore source files:
```bash
# War Chest HTML sources
git checkout fd3db16 -- docs/_archive/ip-vault/warchest/site/

# Previous site build (for reference/structure)
git checkout 5464b9f -- site/

# Most recent canary page before removal
git checkout 52d58bb -- site/canary/index.html
```



---

## Task 0: Monorepo Cleanup (Do First)

147 uncommitted changes across the GrowDirect monorepo. Before building
anything, triage and commit.

### Delete: Root-level junk files

These are loose files dumped into the vault root. They don't belong here:

| File | Size | Action |
|---|---|---|
| `10584-max.jpeg` | 807K | Delete — unlabeled image |
| `13328-max.jpeg` | 480K | Delete — unlabeled image |
| `15658-max.jpeg` | 1.5M | Delete — unlabeled image |
| `2025_Tax_Prep_Workbook.xlsx` | 74K | Delete — personal finance, not code |
| `2025_Tax_Strategy_Brief.docx` | 18K | Delete — personal finance, not code |
| `AngeliqueLyle-LP-Integration-Spec.docx` | 21K | Move to Angel/docs/ or delete |
| `formspree.rtf` | 481B | Delete — one-off form config |
| `Torrance _ San Pedro - Sheet A08...html` | 150K | Move to Seacove/docs/ or delete |
| `Canary Technical Library/` | empty | Already removed (was empty dir) |

### Delete: Restored archive files (from previous session git checkout)

These were restored from git history for reference but shouldn't stay on HEAD:

| Path | Reason |
|---|---|
| `docs/_archive/ip-vault/warchest/site/` (53 files) | War Chest HTML — in git history at fd3db16, don't need on disk |
| `docs/_archive/workorders/` | Restored workorder output — in git history, don't need on disk |

The site dispatch (Task 1) tells the Code session to `git checkout` these
from fd3db16 when needed — they don't need to live on HEAD.

### Commit: 114 modified Brain/wiki files

The bulk of the 147 uncommitted changes are Brain wiki articles (new Cove
research, Angel updates, project MOC changes). These should be committed as
a batch:

```bash
git add Brain/ Angel/knowledge/
git commit -m "brain: batch wiki updates — Cove research, Angel knowledge, project MOCs"
```

### Commit: New Brain wiki articles (untracked)

17 new wiki articles (mostly Cove research):
```
Brain/wiki/coac-bylaws-moc.md
Brain/wiki/cove-arc-posture.md
Brain/wiki/cove-art-jury-vs-wpbca-arc.md
Brain/wiki/cove-case-law-lessons.md
Brain/wiki/cove-declaration-100-scope-open.md
Brain/wiki/cove-document-retention.md
Brain/wiki/cove-endangered-species-constraints.md
Brain/wiki/cove-lessons-learned.md
Brain/wiki/cove-permit-tech-landscape.md
Brain/wiki/cove-rpv-planning-framework-2026.md
Brain/wiki/cove-rpv-safety-element-2018.md
Brain/wiki/seacove-wpbca-demo-plan.md
Brain/raw/inbox/brain-health-check-2026-04-21.md
Brain/raw/processed/brain-health-check-*.md
Brain/raw/processed/advisor-memos/
Brain/raw/processed/council/
```

Add these to the same Brain commit.

### Commit or .gitignore: Misc untracked

| Path | Action |
|---|---|
| `.claude/scheduled_tasks.lock` | Add to .gitignore |
| `devops/git-hooks/` | Review — if useful, commit; if WIP, hold |
| `devops/pgadmin-servers.json` | Add to .gitignore (local config) |
| `docs/superpowers/plans/2026-04-19-foundation-track-*.md` | Commit if current, archive if stale |
| `dispatch-site-2026-04-22.md` | This dispatch — delete after executing |

### Commit: .obsidian changes

```bash
git add .obsidian/
git commit -m "obsidian: sync workspace + graph state"
```

These are harmless Obsidian workspace state changes. Commit to clear noise.

