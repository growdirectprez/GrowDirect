# abalonecove.org — Design Spec

**Date:** 2026-04-16
**Project:** Cove (pivot from governance platform to public editorial site)
**Domain:** abalonecove.org (owned, Cloudflare DNS)
**Entity:** 501(c)(3) nonprofit foundation (to be formed)
**Stack:** Content engine + Brain wiki → static site → GitHub Pages

---

## What This Is

A single long-form feature article (~7,500 words) published at abalonecove.org,
written in the voice of a pseudonymous HOA board member who used AI tools to
research the history of Abalone Cove, the Palos Verdes Peninsula, and the legal
and geological record behind a proposed 16-unit development on an active
landslide.

The editorial model is a Sunday magazine exposé — personal, sourced, detailed,
with the quiet authority of someone who lives there and did the work. The site
is the article. Everything else supports the read.

**Thesis:** This fight has already been fought. This land shouldn't be built on.
The public record proves it. The system that's supposed to protect it has been
captured by the economics of city planning departments that need developer
revenue to survive.

**Voice:** First-person, pseudonymous HOA board member. Restrained, not
sprawling. The author doesn't over-narrate — they present facts and let the
reader sit with them.

**Tone:** LA Times Sunday Home section. Clean prose, tight paragraphs, the kind
of feature that opens with "here's something you didn't know about LA" and
then shows you why it matters. Not advocacy. Not anger. The facts are the
argument. The conclusion is simply: this has been tried before, and this is
going to fail too.

---

## The Narrative Spine

~7,500 words across 13 sections. Each section is a few paragraphs — enough to
establish the facts and move the story forward. The reader who wants primary
sources clicks through to the evidence room.

### 1. Here's Something You Didn't Know About LA (~400 words)
The hook. A board member on the Palos Verdes Peninsula starts pulling a
thread. What they found.

### 2. The Olmsted Thread (~300 words)
USC, 1988. Kenneth Starr, PVE, Declaration 1. The name stuck. Time in
Olmsted cities. Coming home to the hill.

### 3. Vanderlip (~500 words)
Jekyll Island. The Fed. The peninsula purchase (1913). Olmsted Brothers.
Declaration 100, 101, the Art Jury. The grand plan.

### 4. The Lawyer Brothers and the Depression (~500 words)
**[GAP — needs research]**
1929-1948. Shore Club incorporation. Filiorum Corporation. Neptune Fountain,
La Venta Inn. The legal vehicles built between the crash and the boom.
Vanderlip Sr. dies 1937. The interregnum.

### 5. The Parceling of the Hill (~400 words)
Post-war. PV Corp subdivides. The three sister HOAs. Portuguese Bend Club
vs. the neighborhoods. Arrowroot lots — no HOA. PV Corp → PV Properties →
Great Lakes Carbon. The 1949-1952 declarations. Let people do their own
research from here.

### 6. The Slide (~400 words)
1956. 900 acres. Plumbing as catalyst. 2.14 inches per week today.

### 7. Condos vs. the Beach (~400 words)
1972. Karl Rodi proposes 138-170 units. Dick Karshner organizes the vote.
The community chooses the park. Same question, fifty-four years later.

### 8. The Coastal Wall (~500 words)
RPV incorporates 1973 to stop developers. Coastal Act 1976. Coastal Specific
Plan 1978. SB4. Layer after layer built to prevent exactly this.

### 9. The Wong Subdivision (~300 words)
1980. Proper density. Chain of title to Clipper Development LLC.

### 10. The Rezoning (~500 words)
Three ordinances in 63 days. HCD says Site 16 can be removed. City keeps it.
The planning department economics.

### 11. The Tools (~500 words)
How AI made this possible. Deed chains, 75-year-old declarations, GIS,
legal description comparison. What one person can do now.

### 12. The Absurdity (~400 words)
FEMA declarations. Flashing signs. The fire station driveway. 2+ inches
per week. Sixteen units.

### 13. Why? (~300 words)
No call to action. Just the question. The record is right there.

---

## Site Architecture

### Pages

| Route | Content |
|-------|---------|
| `/` | The feature article (the spine above) |
| `/evidence` | Evidence room — organized by topic, links to primary sources |
| `/map` | Interactive map (Leaflet) — parcels, declarations, geological zones |
| `/about` | The foundation, the AI methodology, contact |
| `/timeline` | Visual chronological timeline (1913-2026) |

### Evidence Room Structure

Documents organized by the narrative sections, not by type:

- Olmsted Plans (NPS Archive, File No. 8023)
- Founding Documents (1949-1952 declarations, recorded deeds)
- Shore Club Records (incorporation, lease, 1972 ballot)
- Landslide Documentation (geological surveys, moratorium ordinances, Governor's declaration)
- Coastal Regulation (Coastal Specific Plan, General Plan, municipal code)
- 0 Clipper Parcel (tract maps, chain of title, assessor data)
- Rezoning Record (ordinances 678U/680U/681, community opposition letter, HCD correspondence)
- Litigation (petition, demurrer, opposition — Case 24TRCP00352)

Each evidence item: title, date, source, brief description, link/embed of
primary document.

### Interactive Map

Companion to the narrative. Not the homepage. Features:

- Parcel boundaries (Tract 14649, Tract 32977/43725 — Wong subdivision area)
- Declaration coverage zones (which declarations apply where)
- Geological hazard overlay (existing `landslide-complex` + `landslide-moratorium` layers; APBL boundary may need new GeoJSON work)
- Coastal zone boundary
- Shore Club / Shoreline Park footprint
- 0 Clipper parcel highlighted
- Clickable parcels → deed chain, HOA membership, zoning

Built on existing Cove map module work (Leaflet, GeoJSON layers, manifests).
Note: porting from Flask-served dynamic app to static GitHub Pages requires
extracting client-side JS and GeoJSON loading from the Flask wrapper. Some
layers (Shore Club footprint, APBL boundary) may need new GeoJSON work.
Declaration layers partially exist (101 parcels 1-7, Declaration One, One-A).

---

## Tech Stack

Same as OwnPV — another flavor of the existing pipeline:

| Component | Tool | Notes |
|-----------|------|-------|
| Content source | Brain wiki (`Brain/wiki/cove-*`) | Existing articles rewritten for editorial voice |
| Narrative source | Documentary record sections | `Cove/docs/archive/report/section-*.md` — spine already exists |
| Content engine | `content-engine/` | Scans/triages content; voice rewriting done in Cowork sessions |
| Static site generator | Same as OwnPV | Templates, build pipeline |
| Hosting | GitHub Pages | abalonecove.org via Cloudflare DNS |
| Map | Leaflet.js | Existing Cove map module layers/overlays |
| CSS | Tailwind | New palette appropriate for the brand (abalone shell tones) |
| Typography | Georgia / serif stack | Matches the letterhead aesthetic |

### Brand Identity

- **Logo:** Abalone shell (from the existing letterhead template)
- **Typography:** Georgia serif — serious, readable, editorial
- **Palette:** Derived from the abalone shell — teals, sea greens, warm grays,
  cream paper backgrounds. Not the Cove platform blue.
- **Tone:** Clean, quiet, authoritative. No flashy UI. The content is the design.

---

## Content Pipeline

### Phase 1: Spine Baseline (separate session)

A dedicated session to:

1. Read all 10 existing report sections (`section-00` through `section-09`)
2. Read all Brain wiki articles (`cove-*`)
3. Identify the narrative gaps (especially 1929-1948)
4. Produce a detailed outline mapping existing content to the 13-section spine
5. Flag what needs to be written from scratch vs. rewritten from existing material
6. Baseline the personal narrative frame (the author's story arc)

This is the first deliverable. The site doesn't get built until the spine is solid.

### Phase 2: Site Build

1. Create the static site repo/branch (or new directory in GrowDirect)
2. Adapt OwnPV site template for abalonecove.org brand
3. Build the article page (long-form single-page layout)
4. Build the evidence room (document index with links)
5. Port the map module (Leaflet + existing GeoJSON layers)
6. Build the timeline page
7. Build the about page
8. Deploy to GitHub Pages, point abalonecove.org

### Phase 3: Content Production

1. Content engine rewrites report sections into editorial voice
2. Fill the 1929-1948 gap with new research
3. Write the personal narrative frame (sections 1, 2, 11, 13)
4. Integrate narrative + research sections into final article
5. Populate evidence room with primary source documents
6. Editorial review and polish

### Phase 4: 501(c)(3) Formation

Parallel to content work:
- Choose entity name (Abalone Cove Foundation, Abalone Shore Heritage Foundation, etc.)
- File Articles of Incorporation (California)
- Apply for 501(c)(3) status (Form 1023-EZ if eligible)
- Mission statement aligned with site: preservation, education, public record access
- Timeline: 2-4 months

---

## What This Is NOT

- **Not a governance platform.** The Cove Flask app (secret ballots, elections,
  treasury) is a separate project. This site is static content.
- **Not advocacy.** No petitions, no "call your councilmember," no yard signs.
  The story is the statement.
- **Not anonymous in the legal sense.** The 501(c)(3) is a public filing. The
  pseudonymous voice is editorial choice, not legal concealment.
- **Not a news site.** This is one article, well-supported, with an evidence
  room. It's not a blog that publishes weekly.

---

## Success Criteria

1. A person searching "Abalone Cove development" or "0 Clipper Road Rancho Palos Verdes"
   or "Portuguese Bend landslide housing" finds abalonecove.org on page 1
2. The article is credible enough that a journalist covering the issue would cite it
3. The evidence room contains primary sources that aren't easily findable elsewhere
4. The map shows something nobody else has assembled — declaration boundaries,
   geological zones, and parcel data in one interactive view
5. The Coastal Commission, HCD, or a litigant could use the documentary record
   as a reference

---

## Existing Assets to Leverage

| Asset | Location | Use |
|-------|----------|-----|
| Documentary record (183 pages) | `Cove/docs/archive/report/` | Spine + evidence room content |
| Brain wiki articles (9) | `Brain/wiki/cove-*` | Research base for editorial rewriting |
| Map module (Leaflet + GeoJSON) | `Cove/cove/map/` | Interactive map component |
| Letterhead template | Existing (abalone shell logo) | Brand identity |
| OwnPV site architecture | Existing repo | Template for static site build |
| Content engine | `content-engine/` | Editorial content production |
| Primary source PDFs | To be assembled (not yet in repo) | Evidence room documents |

---

## Narrative Details (for spine baseline session)

These details came out of the brainstorm and should be woven into the spine:

- **The house:** Architect's blueprints found in the garage — what drew the
  author to the house. Don't reveal the address.
- **The previous owner:** Thomas Hartman (28 Sea Cove) was on the board. Now
  the author is on the board. And the author found the documents. The continuity
  of stewardship — and the irony that Hartman sold the 0 Clipper parcel to
  Clipper Development LLC.
- **Davis-Stirling + technology:** The AI journey started with a practical
  question — wondering about electronic voting and what technology could do
  for HOA governance (Sterling Davis-Stirling Act). That question led to
  exploring AI tools, which led to the document research, which uncovered the
  whole history.
- **"Here's something you didn't know about LA"** — the hook. Even people who
  think they know PV don't know this story. The site becomes where the full
  timeline lives for the first time, and invites readers who know other pieces
  to fill in gaps.
- **Don't get long-winded.** Keep it LA Times Sunday Home section. Clean prose,
  tight paragraphs. Let the facts breathe. The author's personal story is
  connective tissue, not the centerpiece.

---

## Open Questions

1. **Entity name** — Abalone Cove Foundation? Abalone Shore Heritage Foundation?
   Something else? Needs to sound educational/preservation, not adversarial.
2. **Pseudonym** — Does the author need a pen name, or is "an HOA board member
   in Rancho Palos Verdes" sufficient attribution?
3. **1929-1948 research** — How much primary source material exists for the
   Lawyer Brothers / Filiorum / Depression era? Is this in Brain or does it
   need new research?
4. **Map data readiness** — Are the existing GeoJSON layers sufficient for the
   public-facing map, or do they need cleanup/expansion?
5. **Legal review** — Should the article be reviewed by counsel before
   publication? (Defamation, fair comment, public figure doctrine)
