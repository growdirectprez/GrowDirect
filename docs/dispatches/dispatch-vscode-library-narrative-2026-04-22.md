# Dispatch: Canary Technical Library — Narrative Docs Uplift
## For: Fresh VS Code Claude Code session
## Skill: `engineering:documentation` (load first)
## Repos touched: `canary-site` (GitHub Pages), read-only `Canary` (source)

---

## Why this dispatch exists

The Canary Technical Library at https://canary.growdirect.io/docs/ currently
ships with five tiles, all source-of-truth but all **reference material**:

| Tile | Type | Source |
|---|---|---|
| The Mermaid Atlas | 52 SVG diagrams | `Canary/docs/atlas/` |
| The CRDM | Hand-written narrative (data model) | War Chest (kept) |
| The Field Registry | Auto-generated md→HTML | `Canary/docs/field-registry.md` |
| The Detection Catalog | Auto-generated AST→HTML | `Canary/canary/services/chirp/rule_definitions.py` |
| The Risk Dictionary | Auto-generated AST→HTML | `Canary/canary/services/risk_dictionary.py` |

**The gap:** a reader landing on the library can see the *shape* of the
system (every field, every rule, every diagram) but there's no **mental
model** doc — no walkthrough, no "how this works end-to-end", no getting
started path, no API reference.

Your job is to write the narrative product docs that sit alongside the
reference material.

---

## Ground rules (non-negotiable)

1. **This is product documentation, not sales copy.** No "sovereign stack,"
   "sound money," "softwar," "bitcoin-native revolution," "the dome."
   Jeffe has specifically called this out. Write for a senior engineer
   evaluating the system, not a conference audience.
2. **Source of truth over authored prose.** When you need a detail, pull
   it from the code, the SDDs, or the existing auto-generated docs — don't
   make it up or embellish.
3. **Link, don't duplicate.** The Field Registry already lists every column.
   Your architecture doc should reference it, not redocument it.
4. **Reader-first.** For each doc, answer: who is reading this, what do
   they need, where do they go next?
5. **Style matches existing library.** Use `../css/canary-docs.css`. Use the
   existing `<header class="site-header">` / `<nav class="doc-nav">` /
   `<main class="doc-main">` / `<article class="doc-body">` / `<footer
   class="site-footer">` pattern from any shipped doc (read
   `~/canary-site/docs/The CRDM.html` as the template).

---

## Deliverables

### 1. `Architecture.html` — Platform Architecture Overview

**Goal:** A reader understands how the Canary system works end-to-end in
15 minutes of reading.

**Source material** (read these before writing):
- `Canary/docs/sdds/v2/architecture.md`
- `Canary/docs/sdds/v2/data-model.md`
- `Canary/docs/sdds/v2/webhook-pipeline.md`
- `Canary/docs/sdds/v2/chirp.md`
- `Canary/docs/sdds/v2/fox.md`
- `Canary/CLAUDE.md` (for current stack reality)
- Atlas diagrams I-01 (Docker Stack), I-02 (DB Schema), O-01 (Service Mesh),
  P-00 (TSP Orchestration)

**Structure** (write in this order, ~2500 words total):
1. **System context** (200w) — what Canary does, who uses it, what it's not
2. **Component map** (400w) — webhook ingress → TSP subscribers → Chirp detection →
   Fox case mgmt → Owl search → dashboard. Embed Atlas figure O-01 as an img.
3. **Data architecture** (500w) — one DB, three schemas (`app`/`sales`/`metrics`),
   how they relate, immutability tiers (append-only, insert-only, hash-chained).
   Link to Field Registry + CRDM.
4. **Detection pipeline** (400w) — TSP (Triple Subscriber Pipeline), tiered rule
   execution, why the tiers exist. Link to Detection Catalog. Embed P-00 figure.
5. **Investigation lifecycle** (300w) — alert → fox case → evidence → resolution.
6. **Search & metrics** (300w) — Owl natural-language search, Risk Dictionary
   drill paths, daily/period metrics engine.
7. **Deployment shape** (300w) — Docker stack, Postgres/Valkey/Ollama, where
   each service lives. Embed I-01.
8. **Where to go next** (100w) — links to the other library tiles.

**Nav update:** add `<a href="Architecture.html">Architecture</a>` to the
doc-nav bar between "CRDM" and "Field Registry" on **every** library doc.

### 2. `Getting Started.html` — 15-Minute Onboarding

**Goal:** A new technical reader moves from "just landed on the site" to
"I understand the system well enough to ask real questions" in 15 minutes.

**Structure** (~1500 words):
1. **What this is** (2 paragraphs, hard limit)
2. **The 15-minute tour** — step-by-step click path:
   - Open `/atlas/` → look at Infrastructure category (I-01, I-02) — 2 min
   - Open `/docs/The CRDM.html` → read sections 1–3 — 5 min
   - Open `/docs/The Field Registry.html` → search for a table you know
     (e.g. `transactions`) — 3 min
   - Open `/docs/The Detection Catalog.html` → skim the categories — 3 min
   - Open `/prototype/` → click through — 2 min
3. **Pick a path by interest** — 5 short sections, one per persona:
   - "I'm evaluating this for a merchant integration" → CRDM + Field Registry
   - "I'm evaluating this for architecture fit" → Architecture + Atlas
   - "I'm evaluating the detection logic" → Detection Catalog + Chirp SDD
   - "I'm evaluating case management" → Fox SDD + lifecycle diagrams
   - "I'm evaluating the data platform" → Field Registry + Schema ERDs
4. **Contact** — single email link, no form.

**Nav update:** make this the second tile after Atlas (replacing CRDM's
current second-position prominence). Nav bar order:
Atlas → Getting Started → Architecture → CRDM → Field Registry →
Detection Catalog → Risk Dictionary → API.

### 3. `API.html` — OpenAPI Reference

**Goal:** Browsable API reference, single-page HTML.

**Source:** `Canary/docs/api/canary-api-v1.yaml`

**Implementation:** Render with Redoc via CDN (single `<script>` tag
against a static YAML file). Copy the YAML to
`canary-site/docs/assets/canary-api-v1.yaml` so the site is self-contained.

Redoc snippet:
```html
<redoc spec-url="assets/canary-api-v1.yaml"></redoc>
<script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
```

Wrap in the same site-header / doc-nav / footer pattern as other docs
(so it doesn't feel like an alien page). Redoc renders its own body.

**Nav update:** last tile.

---

## Template & deploy

### File locations
- Site repo: `~/canary-site/` (GitHub Pages, separate repo)
- Source repo (read only): `~/GrowDirect/Canary/`

### Template anatomy (copy from `~/canary-site/docs/The CRDM.html`)
```
<header class="site-header">…logo + Launch Demo→/prototype/…</header>
<nav class="doc-nav">…7-link bar w/ active class on current…</nav>
<main class="doc-main">
  <div class="doc-header">kicker / h1 / subtitle</div>
  <article class="doc-body">[your content here]</article>
</main>
<footer class="site-footer">…</footer>
```

### Nav bar — final 8-link version after all 3 docs ship
```html
<nav class="doc-nav">
  <a href="/atlas/">Mermaid Atlas</a>
  <a href="Getting Started.html">Getting Started</a>
  <a href="Architecture.html">Architecture</a>
  <a href="The CRDM.html">The CRDM</a>
  <a href="The Field Registry.html">Field Registry</a>
  <a href="The Detection Catalog.html">Detection Catalog</a>
  <a href="The Risk Dictionary.html">Risk Dictionary</a>
  <a href="API.html">API</a>
</nav>
```

Mark the current page with `class="active"` on its own link.

### Deploy steps
For each doc:
1. Write to `~/canary-site/docs/<filename>.html`
2. Update nav on all existing shipped docs (5 of them) + the new ones
3. Update `~/canary-site/docs/index.html` library grid with new tiles (3 new)
4. Update hub page at `~/growdirectprez.github.io/canary/index.html`
   Tech Library section with new tiles (3 new)
5. Commit both repos, push, verify live in ~30s

### Commit messages
Use the existing pattern — `feat(docs): <what>` subject, short prose body,
co-author trailer:
```
Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## Use the skill

Invoke `engineering:documentation` first. Its guidance:

- **README** → inform the *Getting Started* doc structure
- **Architecture Doc** → inform the *Architecture* doc
- **API Documentation** → inform the *API* doc structure
- **Runbook** → don't need for this dispatch

Then follow the skill's principles throughout (reader-first, show don't tell,
link don't duplicate, keep current).

---

## Don't touch

- Mermaid Atlas (`canary.growdirect.io/atlas/`) — already gold
- The CRDM (kept; may need light polish only if something is factually
  outdated — otherwise leave)
- Field Registry / Detection Catalog / Risk Dictionary — auto-generated
  from Canary source; re-running the build scripts re-produces them.
  Don't hand-edit the HTML.

---

## Return envelope

When done, paste back to the orchestrator:
1. Files created (paths + byte sizes)
2. Commit hashes — one for `canary-site`, one for `growdirectprez.github.io`
3. Live URLs (should all 200 in ~30s after push)
4. Any source gaps you hit (e.g. "API YAML has no `/alerts/{id}` endpoint documented")
5. Any deviations from this dispatch, with one-sentence reasons

---

## Out of scope

- Rewriting CRDM narrative (keep as-is)
- Adding tiles beyond the 3 specified
- Rebuilding Atlas, Field Registry, Detection Catalog, or Risk Dictionary
- Changing the template or CSS
- Bitcoin-evangelism content, founder's-case storytelling, or pitch material

---

*Dispatch prepared by ALX · 2026-04-22*
