# Foundation Track A — Week 1 Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Launch a Foundation surface at `~/abalonecove/foundation/` (subdomain `foundation.abalonecove.org` via Cloudflare DNS) containing the Karshner-template content that supports the Community of Abalone Cove board president's third-director recruitment effort, publishes the Foundation's founding story, and hosts concrete project proposals — all before the next Community of Abalone Cove meeting.

**Architecture:** New `/foundation/` section in the existing `~/abalonecove/` static site repo. Georgia-serif / shell-teal brand consistency with the rest of the site. Karshner 1972 seven-section structure. No backend — embedded Google Form / Tally for signatures and Buttondown for newsletter (already established in `~/abalonecove/sign/`). Content produced in Foundation corporate voice per §7 of the Foundation spec, not pseudonymous.

**Tech Stack:** Static HTML, inline CSS with `var(--shell-*)` tokens, Georgia serif, GitHub Pages deploy, Cloudflare DNS. No build step, no JS beyond the existing embeds.

**Parent spec:** [`docs/superpowers/specs/2026-04-18-abalone-cove-foundation-design.md`](../specs/2026-04-18-abalone-cove-foundation-design.md) §6 Surface 1 + §8 Track A + §10 Karshner template + §11 Concrete Projects.

**Sibling plan:** [`docs/superpowers/plans/2026-04-19-foundation-track-b-week-1.md`](2026-04-19-foundation-track-b-week-1.md) runs in parallel. Neither blocks the other.

---

## Blocker Gates (per §14 Open Decisions)

These must be resolved before the flagged tasks proceed. They are not work items — they are decisions the user makes.

| Gate | §14 item | Blocks | Default if user wants to proceed |
|---|---|---|---|
| **B-A1 — Voice register** | abalonecove.org spec §"Voice" reconciliation | All content drafting tasks (T3–T9) | Foundation corporate voice per Foundation spec §7 — restrained "I might be right" register; not pseudonymous; named director bylines only after Track B Task T2 confirms directors |
| **B-A2 — Domain strategy** | §14.4 | Deploy task (T14) | `foundation.abalonecove.org` subdomain via Cloudflare; cove.org acquisition pursued separately |
| **B-A3 — Named directors** | §14.2 (waits on Track B) | "The Committee" section (T5) | Ship placeholder text: "Directors to be confirmed [date]" — update once Track B T2 completes. Does NOT block deploy |
| **B-A4 — Carlsbad citation** | abalonecove.org spec §12 OC-1 | Any article copy that cites Carlsbad | Do not cite until pulled; the argument holds without it |
| **B-A5 — HCD certification status** | §14 item 10 (OC-4) | Any copy that asserts estoppel-strength on 2024 HE | Cite 1990 + 2001 HE "Not buildable" verbatim; qualify 2024 posture as "under HCD review" until pulled |

**Gate clearance protocol:** each task below lists which gate(s) it depends on. If gate is open, skip the task and continue with gate-free work; revisit when the user clears it.

---

## File Structure

```
~/abalonecove/
├── foundation/
│   ├── index.html              # Karshner 7-section landing — the primary surface
│   ├── story.html              # Founding Story — Karshner §8 (separated for length)
│   ├── projects.html           # Concrete projects page — Karshner §7 expanded
│   ├── committee.html          # The Committee (named directors post-Track-B)
│   └── evidence/               # Foundation-specific evidence room deep-links
│       └── index.html          # Curated list of Brain/wiki/cove-* + coac-* + foundation-*
├── sign/index.html             # existing — add a Foundation-specific petition CTA
└── (existing site files unchanged)
```

**Repo:** `~/abalonecove/` is the GitHub Pages source for abalonecove.org. Not inside GrowDirect. Commits here deploy directly.

**Content sources (read these first):**
- `docs/superpowers/specs/2026-04-18-abalone-cove-foundation-design.md` — Foundation spec
- `docs/superpowers/specs/2026-04-16-abalonecove-org-design.md` — site-level voice & structure (see voice-reconciliation flag)
- `Brain/wiki/cove-rpv-planning-framework-2026.md` — planning framework synthesis
- `Brain/wiki/cove-case-law-lessons.md` — 19 rules
- `Brain/wiki/cove-endangered-species-constraints.md` — species → trigger map
- `Brain/wiki/cove-rpv-safety-element-2018.md` — 2018 Safety Element
- `Brain/wiki/cove-lessons-learned.md` — 35 lessons
- `Brain/wiki/coac-pv-endangered-species.md` — 5 scientific papers

**Brand tokens (already in use across the site):**
- `--shell-teal` — primary accent
- `--shell-cream` — background
- `--shell-warm` — secondary accent
- `--shell-sage` — dividers / era labels
- `--shell-dark` — body text
- Typography: Georgia serif, 680px max-width, sticky header with hamburger nav

---

## Chunk 1: Scaffolding + Non-Blocking Setup

### Task T1: Create the `/foundation/` directory tree

**Files:**
- Create: `~/abalonecove/foundation/index.html`
- Create: `~/abalonecove/foundation/story.html`
- Create: `~/abalonecove/foundation/projects.html`
- Create: `~/abalonecove/foundation/committee.html`
- Create: `~/abalonecove/foundation/evidence/index.html`

**Gates:** none.

- [ ] **Step 1: Verify the abalonecove repo is clean**

Run:
```bash
cd ~/abalonecove && git status
```
Expected: `working tree clean` or only intentional in-progress changes.

- [ ] **Step 2: Create the five scaffold files with the site's existing HTML head block**

Copy the `<head>` + sticky header + footer from `~/abalonecove/index.html` into each new file, replacing the article body with a single `<h1>` placeholder. This inherits brand tokens, nav, hamburger, and footer for free. For each file set `<title>` per:

| File | Title |
|---|---|
| `foundation/index.html` | "Abalone Cove Foundation" |
| `foundation/story.html` | "Founding Story — Abalone Cove Foundation" |
| `foundation/projects.html` | "Concrete Projects — Abalone Cove Foundation" |
| `foundation/committee.html` | "The Committee — Abalone Cove Foundation" |
| `foundation/evidence/index.html` | "Foundation Evidence Room" |

- [ ] **Step 3: Verify each file renders**

Run:
```bash
cd ~/abalonecove && python3 -m http.server 8765 &
open http://localhost:8765/foundation/
open http://localhost:8765/foundation/story.html
open http://localhost:8765/foundation/projects.html
open http://localhost:8765/foundation/committee.html
open http://localhost:8765/foundation/evidence/
kill %1
```
Expected: each page loads with sticky header + hamburger + footer; placeholder `<h1>` visible.

- [ ] **Step 4: Commit scaffold**

```bash
cd ~/abalonecove && git add foundation/ && git commit -m "foundation: scaffold /foundation/ section with brand-consistent HTML"
```

### Task T2: Add `/foundation/` to the main nav

**Files:**
- Modify: every `~/abalonecove/*/index.html` sticky header's hamburger menu to include a "Foundation" link

**Gates:** none.

- [ ] **Step 1: Find the existing nav pattern**

Run:
```bash
cd ~/abalonecove && grep -l 'href="/evidence' index.html about/index.html sign/index.html timeline/index.html evidence/index.html map/index.html position/index.html
```
Expected: list of files with the nav pattern.

- [ ] **Step 2: Insert Foundation link in the nav block of each file**

Open each file, find the `<nav>` block, and add `<a href="/foundation/">Foundation</a>` in the position matching the site's existing ordering (likely after "About" or before "Sign"). Match existing styling exactly — do not introduce new classes.

- [ ] **Step 3: Verify nav consistency**

Run:
```bash
cd ~/abalonecove && grep -c 'href="/foundation/"' index.html about/index.html sign/index.html timeline/index.html evidence/index.html map/index.html position/index.html foundation/index.html
```
Expected: `1` for every file.

- [ ] **Step 4: Visual verification — click-through from every page**

Run local server and click the Foundation link from every page. Confirm no broken link.

- [ ] **Step 5: Commit**

```bash
cd ~/abalonecove && git add -A && git commit -m "foundation: add /foundation/ to site-wide nav"
```

---

## Chunk 2: Primary Surface Content (Gates B-A1, B-A4, B-A5)

**All tasks in this chunk require Gate B-A1 (voice register) cleared.** If not cleared, stop here and return to the user.

### Task T3: Front-page / "The Situation" section on `foundation/index.html`

**Files:**
- Modify: `~/abalonecove/foundation/index.html`

**Gates:** B-A1 (voice register). If not cleared, stop.

- [ ] **Step 1: Draft the 500-word front page**

Draft per Foundation spec §10 item 1 ("Front page / Context"). Voice: Foundation corporate, restrained, factual. Open with the situation stated neutrally:

Content brief (not verbatim — draft in voice):
- Community of Abalone Cove (formerly WPBCA) is currently below the Davis-Stirling director threshold (2 of 5 seats filled)
- The Portuguese Bend landslide complex reactivated; the 0 Clipper rezoning to RM-22 is in active litigation (Case 24TRCP00352)
- The Abalone Cove Foundation is a California Nonprofit Public Benefit Corporation (in formation) — steward of the scenic south coast as a community asset; research, documentation, convening partner
- Links: to [[Brain/wiki/cove-rpv-planning-framework-2026]] findings summary on `/foundation/evidence/`; to "Founding Story" at `/foundation/story.html`; to "Concrete Projects" at `/foundation/projects.html`

Target length: 500 words. Use the existing article-body CSS class(es) from `~/abalonecove/index.html`.

- [ ] **Step 2: Verification — read aloud + 3 checks**

Read the draft aloud. Verify:
1. No hype language ("revolutionary", "game-changing", "unprecedented") — fail fast if present
2. No pseudonymous first-person — if "I found…" appears, it's a voice regression
3. No claims that require Gate B-A4 or B-A5 resolution

- [ ] **Step 3: Commit section**

```bash
cd ~/abalonecove && git add foundation/index.html && git commit -m "foundation(site): draft front-page context section"
```

### Task T4: "Options" section — restore board / projects / §V §5 reserved

**Files:**
- Modify: `~/abalonecove/foundation/index.html` (append section)

**Gates:** B-A1.

- [ ] **Step 1: Draft the Options section**

Three restoration paths stated neutrally per Foundation spec §10 item 3:
1. Restore Community of Abalone Cove board function — elect third director; resume regular board activity
2. Support concrete projects — trail restoration, Olmsted overlay, 0 Clipper preservation per 1980 Wong subdivision, creek conservation easement to PVPLC, fire station relocation per Schematic Plan #2
3. If escalation becomes necessary — §V §5 reactivation pathway held in reserve

**Critical constraint:** For path 3, use only the neutral-description voice. **Do not** describe the reactivation as a strategy or blitz — per feedback memory, reactivation is sensitive and coac-* articles are private-until-board-authorized. The public Foundation surface can name the reserve mechanism factually without describing operational plans.

Target length: 400 words. Each path one paragraph.

- [ ] **Step 2: Verification**

Verify:
1. No operational detail about §V §5 reactivation (no 15-HOA committee math, no timing, no Declaration 100 boundary speculation)
2. No ocean-path-easement advocacy copy (also sensitive per memory)
3. All five projects are listed with the correct names from spec §11

- [ ] **Step 3: Commit**

```bash
cd ~/abalonecove && git add foundation/index.html && git commit -m "foundation(site): draft Options section with reserve-only §V §5 posture"
```

### Task T5: "The Committee" section (placeholder)

**Files:**
- Modify: `~/abalonecove/foundation/index.html` (append section) + `~/abalonecove/foundation/committee.html`

**Gates:** B-A1. **Soft gate: B-A3 (named directors)** — ship with placeholder; update on Track B T2 completion.

- [ ] **Step 1: Draft committee section with placeholder**

Content:
- Foundation's role: California Nonprofit Public Benefit Corporation (in formation)
- Mission and scope of activity per Foundation spec §2 + §4 (three roles)
- Director list: **"Directors to be confirmed and announced [target date]"** — placeholder text; do not fabricate names
- Link to standalone `/foundation/committee.html` for expanded directors page once confirmed

For `committee.html`, draft the shell page structure — title, intro paragraph, empty directors table with column headers (Name / Role / Bio / Conflict disclosure). Do not populate until Track B T2 confirms.

- [ ] **Step 2: Verification**

Verify:
1. No placeholder names — `[[name]]` or "TBD" is acceptable; never invent
2. Link `/foundation/committee.html` exists and loads
3. Conflict-disclosure column present per Foundation spec §4 note on conflicts

- [ ] **Step 3: Commit**

```bash
cd ~/abalonecove && git add foundation/index.html foundation/committee.html && git commit -m "foundation(site): draft Committee section with placeholder directors"
```

### Task T6: "Expert Citations" section

**Files:**
- Modify: `~/abalonecove/foundation/index.html` (append section)

**Gates:** B-A1. B-A4 for Carlsbad only (do not cite).

- [ ] **Step 1: Draft Expert Citations per Foundation spec §10 item 5**

Link to the evidence-library items and the five synthesis articles. Use the expanded citation list from the 2026-04-19 spec edit:

Scientific / geological:
- Woodring 1946 (USGS federal report)
- Ehlig 1982 (AEG landslide guidebook)
- LGC Valley 2011 (RPV-commissioned Zone 2 geotech)
- CSUDH 2012 (McNulty field guide)

City planning instruments:
- 1978 Coastal Specific Plan (Subregion 4)
- 2018 RPV Safety Element (PV Fault Mw 7.3 / MMI XI; Landslide Inventory Figure 3; Fire Hazard Severity Zone Figure 1)
- 1990 + 2001 RPV Housing Elements ("Not buildable" verbatim inventory entries)

Case law:
- *Albers v. County of Los Angeles* (1965, 62 Cal. 2d 250)
- *Monks v. RPV* (2008, 167 Cal. App. 4th 263)
- *Colyear v. RHCA* (2024, B308382) — caveat: certified for partial publication

Conservation science:
- Dalkey 2016 (coastal cactus wren)
- Mattoni 1994 + 2003 (PVB rediscovery + mass rearing)
- 2005 PVB pupae-salvage mitigation
- Marincovich (Late Pleistocene terraces)

Each citation: one line — case/document name, year, brief description, link to `/foundation/evidence/` entry.

**Do not cite** Carlsbad (Gate B-A4) until pulled.

- [ ] **Step 2: Verification**

Verify:
1. Every external citation has a corresponding entry in `/foundation/evidence/index.html` (even if the evidence page is itself a stub pointing to Brain/wiki/)
2. No broken internal links
3. Carlsbad citation absent

- [ ] **Step 3: Commit**

```bash
cd ~/abalonecove && git add foundation/index.html && git commit -m "foundation(site): draft Expert Citations with 2026-04-19 synthesis sources"
```

### Task T7: "Q&A Scenarios" section

**Files:**
- Modify: `~/abalonecove/foundation/index.html` (append section)

**Gates:** B-A1.

- [ ] **Step 1: Draft Q&A per Foundation spec §10 item 6**

Questions + one-paragraph factual responses. Each response ends with a "See: [[wiki]]" link. Minimum 8 Q&A items:

| Q | A source |
|---|---|
| Why can't the community just build on this land? | `cove-rpv-safety-element-2018` §5.3 (landslide) + `cove-case-law-lessons` R11 (Monks) |
| What about the wildlife? | `cove-endangered-species-constraints` species-trigger map |
| What about the creek? | `cove-pvplc-partnership` creek conservation easement ask |
| Isn't there a traffic concern? | `cove-rpv-safety-element-2018` §8.6 disaster routes |
| Who controls the water supply on the hill? | `cove-rpv-safety-element-2018` §5.1 / §8 (water company; electronic telemetric monitoring) |
| What happens if there's a fire? | `cove-rpv-safety-element-2018` §3 Fire Hazard Severity Zone |
| What about beach access? | Neutral description — "beach access is governed by the 1949 Declaration of Easements and the Coastal Specific Plan." **Do not** extend into ocean-path-easement detail (private governance matter) |
| What about Fire Station 53? | Spec §11 Project 5 + Coastal Specific Plan Schematic Plan #2 |

- [ ] **Step 2: Verification**

Verify:
1. Beach access Q does not cross into ocean-path-easement advocacy (Foundation does neutral documentation per memory)
2. Every A ends with a "See:" wiki link
3. No Q asserts a position that requires Gate B-A4 or B-A5

- [ ] **Step 3: Commit**

```bash
cd ~/abalonecove && git add foundation/index.html && git commit -m "foundation(site): draft Q&A Scenarios"
```

### Task T8: "Formal Positions for Member Action" section

**Files:**
- Modify: `~/abalonecove/foundation/index.html` (append section)

**Gates:** B-A1.

- [ ] **Step 1: Draft member-action list per spec §10 item 7**

Concrete actions (bulleted):
1. Attend the next Community of Abalone Cove meeting [date TBD via board]
2. Serve as director — the board needs a third director to restore quorum; candidacy criteria and process
3. Give a proxy (link to proxy form; see `/sign/` if the existing form can be repurposed, otherwise add)
4. Update the membership roster — contact info for the Community of Abalone Cove secretary
5. Endorse the Foundation's proposed implementation of Subregion 4 policies (link to endorsement form on `/sign/`)
6. Sign the beach-path inter-HOA restoration letter when circulated (CHOA-routed where possible) — **stub only; actual letter is CoAC / CHOA work product, not Foundation public-voice**

- [ ] **Step 2: Verification**

Verify:
1. Item 6 does NOT present the beach-path letter as Foundation work — it's CoAC/CHOA
2. Item 2 does not include promises of indemnity or D&O coverage the Foundation cannot make
3. All links exist or are explicitly marked `(form coming [date])`

- [ ] **Step 3: Commit**

```bash
cd ~/abalonecove && git add foundation/index.html && git commit -m "foundation(site): draft Formal Positions for Member Action"
```

---

## Chunk 3: Founding Story + Projects Pages (Gate B-A1)

### Task T9: `/foundation/story.html` — Founding Story per spec §7

**Files:**
- Modify: `~/abalonecove/foundation/story.html`

**Gates:** B-A1. **Sensitivity constraint:** per feedback memory, `foundation-founders-narrative.md` is `visibility: internal-only-until-foundation-seated`. **Do not** publish founder personal narrative (55 years old, Raspberry Pi BTC mining 2014, sliding seaside cottage, wife is CA realtor, etc.) Publishable: Betty archive documentary inheritance, Shore Club 1972 inspiration, general archival-research methodology.

- [ ] **Step 1: Draft founding story**

Narrative structure (restrained):
- Betty — a previous WPBCA board member + Shore Club board 1950s — left a documentary archive in banker boxes
- Current Foundation organizer found and followed the trail
- Dick Karshner / 1972 Shore Club as the direct community-precedent inspiration (1972 successful vote against Karl Rodi 138-170 unit proposal)
- Foundation is not the Shore Club's legal successor — new CA Nonprofit Public Benefit Corp, own board, own bylaws
- "What it inherits from the Shore Club is community continuity, organizational template, and documentary archive"
- Link to evidence library at `/foundation/evidence/`

Target length: 800–1,200 words.

- [ ] **Step 2: Sensitivity check**

Read draft. Verify absence of:
- Personal founder identifying details (age, profession, tech background, asset details, family)
- Any ownership claims not publicly known
- Anything from `foundation-founders-narrative.md` marked `visibility: internal-only-until-foundation-seated`
- Reactivation operational detail (private per memory)
- Ocean-path-easement advocacy (private governance matter)

If any present, strike before commit.

- [ ] **Step 3: Commit**

```bash
cd ~/abalonecove && git add foundation/story.html && git commit -m "foundation(site): publish Founding Story — documentary inheritance, Shore Club precedent"
```

### Task T10: `/foundation/projects.html` — five concrete projects

**Files:**
- Modify: `~/abalonecove/foundation/projects.html`

**Gates:** B-A1.

- [ ] **Step 1: Draft projects page from spec §11**

Each of the 5 projects as an H2 section with:
- **Title** (e.g., "Trail Restoration — Community of Abalone Cove ↔ PV Bay Club")
- **The ask** — one sentence
- **The basis** — what CC&R / regulatory / geographic / scientific record supports it
- **Who does what** — roles for Foundation, CoAC board, CHOA, PVPLC, city, neighbor HOAs
- **Current status** — "Proposed" / "Drafting" / "Under review"
- **Link to synthesis wiki** if applicable

Project 4 (Creek Conservation Easement) gets the strongest treatment per Foundation spec §11 Project 4 updated text — cite NCCP/HCP, Section 7/10, PVPLC partnership, Filiorum documentary arc. This is the flagship.

- [ ] **Step 2: Verification**

Verify:
1. Each project has the 5 required elements (title, ask, basis, roles, status)
2. No overclaiming — "Proposed" is fine; "Agreed" is not unless a signed agreement exists
3. Project 4 cites `cove-endangered-species-constraints` + `cove-pvplc-partnership`
4. Project 5 (Fire Station 53) mentions Coastal Specific Plan Schematic Plan #2 and the current-site-unstable basis

- [ ] **Step 3: Commit**

```bash
cd ~/abalonecove && git add foundation/projects.html && git commit -m "foundation(site): publish 5 concrete projects"
```

---

## Chunk 4: Foundation Evidence Room + Cross-linking

### Task T11: `/foundation/evidence/index.html` — Foundation evidence room

**Files:**
- Modify: `~/abalonecove/foundation/evidence/index.html`

**Gates:** none.

- [ ] **Step 1: Draft the Foundation evidence room**

Mirror the style of `~/abalonecove/evidence/index.html` — same markup, same brand tokens. Sections:

1. **Foundation Synthesis** — 5 internal Brain wiki links:
   - cove-rpv-planning-framework-2026
   - cove-case-law-lessons
   - cove-endangered-species-constraints
   - cove-rpv-safety-element-2018
   - cove-lessons-learned
2. **Case Law** — the 12 cases from cove-case-law-lessons
3. **City Planning Instruments** — 1975/1990/2001/2018 planning docs + 2024 HE adoption staff report
4. **Conservation Science** — the 5 papers from coac-pv-endangered-species
5. **Pointer to main site evidence room** — link to `/evidence/`

**Important:** Brain/wiki files are not directly published on the static site. For each entry, use a short description + "See: `Brain/wiki/<slug>.md`" notation. The actual Brain content lives in the GrowDirect repo, not abalonecove.org. Do not copy wiki content into the site.

- [ ] **Step 2: Verify**

Run local server, load `/foundation/evidence/`, confirm:
1. Each of the 4 content sections has at least 5 entries
2. Each entry has a title, a year, and a source descriptor
3. Brand consistent with `/evidence/`

- [ ] **Step 3: Commit**

```bash
cd ~/abalonecove && git add foundation/evidence/ && git commit -m "foundation(site): publish Foundation evidence room with synthesis cross-refs"
```

### Task T12: Add Foundation-specific CTA to `/sign/`

**Files:**
- Modify: `~/abalonecove/sign/index.html`

**Gates:** none.

- [ ] **Step 1: Add a third CTA to the existing sign page**

Current `/sign/` has petition + newsletter + visitor counter. Add a Foundation-specific section: "Support the Foundation" — describe mission in one sentence, link to `/foundation/`. If a donation form is not ready, add "Donation intake opening [Track B T6 completion date]" — not a false promise.

- [ ] **Step 2: Verify page still renders + no broken links**

- [ ] **Step 3: Commit**

```bash
cd ~/abalonecove && git add sign/index.html && git commit -m "foundation(site): add Foundation CTA to /sign/"
```

---

## Chunk 5: Pre-deploy Verification + Deploy

### Task T13: Pre-deploy verification sweep

**Gates:** B-A1, B-A4, B-A5 must all be cleared on published copy.

- [ ] **Step 1: Link health check**

Run:
```bash
cd ~/abalonecove && python3 -m http.server 8765 &
```

Then manually click every link on `/foundation/`, `/foundation/story.html`, `/foundation/projects.html`, `/foundation/committee.html`, `/foundation/evidence/`. Every link should either load a page or load an external URL that returns 200. Run:
```bash
# Rough external-link check
grep -rEoh 'href="https?://[^"]+"' ~/abalonecove/foundation/ | sort -u | while read line; do
  url=$(echo "$line" | sed 's/href="//;s/"$//')
  echo -n "$url: "
  curl -sI -o /dev/null -w '%{http_code}\n' "$url"
done
```
Expected: every URL returns 200 or 3xx. Flag any 4xx / 5xx before deploy.

- [ ] **Step 2: Voice / sensitivity pass**

Open every new page. Grep for red flags:
```bash
grep -riE '(revolutionary|game-changing|unprecedented|unleash|leverage|cutting-edge)' ~/abalonecove/foundation/
```
Expected: empty output. If anything matches, rewrite.

Grep for private-memory content that leaked:
```bash
grep -riE '(raspberry pi|bitcoin miner|sliding cottage|reactivation blitz|15 owner network|hollister)' ~/abalonecove/foundation/
```
Expected: empty output.

- [ ] **Step 3: Responsive / mobile check**

Open each page in browser at 375px width (iPhone SE / mobile viewport). Verify:
1. Sticky header doesn't overflow
2. Hamburger menu opens
3. Article body wraps at 680px max-width
4. No horizontal scroll

- [ ] **Step 4: Accessibility quick check**

Check each page:
- Each image has an `alt` attribute
- Heading hierarchy is logical (`h1` → `h2` → `h3`, no skipping)
- Link text is descriptive (no "click here")

- [ ] **Step 5: Commit any fixes**

```bash
cd ~/abalonecove && git add -A && git commit -m "foundation(site): pre-deploy verification fixes"
```

### Task T14: Deploy via GitHub Pages + DNS

**Gates:** B-A2 (domain strategy). **If B-A2 open:** deploy to `abalonecove.org/foundation/` (existing domain path) — the subdomain can be added later.

- [ ] **Step 1: Push to GitHub**

```bash
cd ~/abalonecove && git push origin main
```

Expected: GitHub Pages build triggers automatically.

- [ ] **Step 2: Verify deploy**

Wait 1–2 minutes. Then:
```bash
curl -sI https://abalonecove.org/foundation/ | head -5
curl -sI https://abalonecove.org/foundation/story.html | head -5
curl -sI https://abalonecove.org/foundation/projects.html | head -5
```
Expected: `HTTP/2 200` for each.

- [ ] **Step 3: Cloudflare DNS for subdomain (if Gate B-A2 resolved to subdomain)**

In Cloudflare dashboard for `abalonecove.org`:
1. Add a CNAME record: `foundation` → `<github-pages-hostname>` (same as root) with proxy enabled
2. In the abalonecove.org repo, add `foundation/CNAME` containing `foundation.abalonecove.org`
3. Push; wait for GH Pages to recognize

Run:
```bash
dig foundation.abalonecove.org
curl -sI https://foundation.abalonecove.org/ | head -5
```
Expected: DNS resolves; page returns 200.

- [ ] **Step 4: Post-deploy screenshot / visual check**

Open `https://abalonecove.org/foundation/` in browser. Screenshot the front page for the session record. Save to `Brain/raw/processed/foundation/2026-04-XX-foundation-site-launch-screenshot.png`.

- [ ] **Step 5: Board review circulation**

Circulate the URL to the Community of Abalone Cove board president (and counsel if Gate §14.7 resolved) for review before wider distribution. **Do not** share externally until board has had 48 hours to review.

- [ ] **Step 6: Commit post-deploy log**

Write a short log at `Brain/raw/processed/foundation/2026-04-XX-track-a-week-1-completion.md` listing: tasks completed, gates cleared, gates still open, URL, next-review date. Then:

```bash
cd ~/GrowDirect && git add Brain/raw/processed/foundation/ && git commit -m "foundation: Track A Week 1 launch log + screenshot"
```

---

## Exit criteria for Track A Week 1

- [ ] `/foundation/` surface published at `abalonecove.org/foundation/` (or subdomain)
- [ ] All 5 pages (index, story, projects, committee, evidence) live and linked
- [ ] Link health clean (no 404s on deployed copy)
- [ ] Voice reconciled to Foundation corporate register per Gate B-A1
- [ ] No private-memory content leaked
- [ ] Board president + counsel have the URL for 48-hour review
- [ ] Track A Week 1 completion log in `Brain/raw/processed/foundation/`
- [ ] Track B T2 (directors confirmed) → when resolved, revisit Task T5 + T9 to publish named directors

## Known handoffs to Track B

- Track B T2 confirms three initial directors → Track A follow-up task to update `committee.html` and `foundation/index.html` placeholder
- Track B T6 (IRS determination letter received) → Track A follow-up to update status text from "Foundation (in formation)" to "California Nonprofit Public Benefit Corporation, 501(c)(3) status effective [date]"

## Post-Week-1 backlog (not in this plan)

- Wired-style feature article (Surface 3 per Foundation spec §6) — separate plan, do not start Week 1
- Governance Engine (Surface 4) — deferred per Foundation spec §13
- Founder narrative publication — gated on Foundation being seated
