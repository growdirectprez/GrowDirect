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

**Tone:** Charles C. Mann's *1491* — an investigative journalist who took a
subject everyone thought they knew, followed the evidence, and showed the
established narrative was wrong. Not argumentative. Not academic. A smart
person surprised by what they found, sharing it like a conversation. The
reader discovers it alongside the author. LA Times Sunday Home section
execution — clean prose, tight paragraphs, opens with "here's something
you didn't know about LA." The facts are the argument. The conclusion is
simply: this has been tried before, and this is going to fail too.

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
1882 Superior Court decision — Bixby owns the Rancho. Vanderlip buys from
Bixby syndicate 1913. Jekyll Island. The Fed. Olmsted Brothers hired — but
the Olmsted map was an artist's rendering of the contracts, the dream, never
fully realized. Declaration 100, 101, the Art Jury. The grand plan.

### 4. The Lawyer Brothers and the Depression (~500 words)
**[GAP — needs research]**
1929-1948. Shore Club incorporation. Filiorum Corporation. Neptune Fountain,
La Venta Inn. The legal vehicles built between the crash and the boom.
Vanderlip Sr. dies 1937. The interregnum.

### 5. The Parceling of the Hill (~400 words)
Post-war. PV Corp subdivides. The three sister HOAs. Portuguese Bend Club
vs. the neighborhoods. Arrowroot lots — no HOA. Lot H — the declaration on
the NEGATIVE SPACE (everything not in a named tract). The mapping exercise
that revealed this pattern. PV Corp → PV Properties → Great Lakes Carbon.
The 1949-1952 declarations. Let people do their own research from here.

### 6. The Slide (~400 words)
1956. 900 acres. Plumbing as catalyst. Wayfarers Chapel — had to be
disassembled after they started watering the grapes, triggering movement.
If watering grapes destabilized a chapel, what does 16 units of plumbing
do? Jim York's house — why was he allowed to build? Catalina Gardens —
why is it there? 2.14 inches per week today.

### 7. Condos vs. the Beach (~400 words)
1972. Karl Rodi proposes 138-170 units. Dick Karshner organizes the vote.
The community chooses the park. Same question, fifty-four years later.

### 8. The Coastal Wall (~500 words)
RPV incorporates 1973 to stop developers. Coastal Act 1976. Coastal Specific
Plan 1978. SB4. Layer after layer built to prevent exactly this.

### 9. The Wong Subdivision (~300 words)
1980. Proper density already established. Chain of title: Wong → Hartman
(held 16 years, couldn't build, sold) → Clipper Development LLC. Clipper
isn't a savvy developer who found a deal nobody else saw — they're the
latest speculator left holding the bag on land that has defeated every
owner for a century. The city didn't allow the Hartmans to go beyond
what was in the 1980 subdivision — and then that subdivision somehow
never came up during the planning commission or the lawsuit. Why not?

### 10. The Rezoning (~500 words)
Three ordinances in 63 days. HCD says Site 16 can be removed. City keeps it.
The planning department economics.

### 11. The Tools (~500 words)
How AI made this possible. Deed chains, 75-year-old declarations, GIS,
legal description comparison. What one person can do now.

### 12. The Absurdity (~400 words)
FEMA declarations. Flashing signs. The fire station driveway. 2+ inches
per week. Sixteen units. And the HOA — the enforcement mechanism the
Vanderlips built in 1949 — can't function. $20/month dues can't fund
legal action. Board members who try to enforce get personally named in
lawsuits. Neighbors sue each other and the board can't intervene without
D&O insurance it can't afford. The state tells HOAs they can't restrict
development (SB9, AB 670) while courts say CC&Rs still have teeth
(Carlsbad, April 2026). The city ignores the same CC&Rs when a developer
wants to build. The governance structure designed to protect this land
is toothless — by economics, by liability, by design. But they wrote your gardener a $250 ticket for a leaf blower.
And cited your dog off-leash in a park the city closed.

### 13. Why? (~300 words)
No call to action. Just the question. The record is right there.
Last line: "And so we created a 501(c)(3) to prevent them from paving
this piece of paradise."

---

## Site Architecture

### Pages

| Route | Content |
|-------|---------|
| `/` | The feature article (the spine above) |
| `/evidence` | Evidence room — organized by topic, links to primary sources |
| `/map` | Interactive map (Leaflet) — parcels, declarations, geological zones |
| `/about` | The foundation, the AI methodology, contact |
| `/sign` | Petition signatures, newsletter signup, visitor counter |
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
| CSS | Inline CSS with custom properties | No build step; abalone shell palette |
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

## Community Engagement (Static — No Backend)

### `/sign` Page

Branded with the Abalone Cove letterhead (abalone shell logo, Georgia serif).
Three components, all embedded services — no server infrastructure:

**1. Petition / Signature Collection**
- Google Form embedded on page (or linked from a branded button)
- Fields: name, address (proves residency), email, optional comment
- Responses flow to a Google Sheet — the Sheet IS the petition database
- Sheet can be made public (read-only) so visitors see the signature count
- The form itself is styled to match the site (Google Forms allows CSS overrides
  via iframe, or use a Tally.so form for better visual control)

**2. Newsletter Signup**
- Buttondown (free tier, 100 subscribers) or Mailchimp free tier
- Simple `<form>` embed: email field + submit button
- Styled to match the letterhead aesthetic
- Newsletter content: updates on the investigation, new documents found,
  city council actions, Coastal Commission developments

**3. Visitor Counter**
- GoatCounter (free, open source, privacy-friendly)
- One `<script>` tag — displays live visitor count
- Optional: public stats page at goatcounter.com showing traffic over time
- Alternative: just use GA4 (already planned) and don't show a public count

**Page layout:**
- Abalone Cove letterhead at top (the shell logo + wordmark)
- Brief statement: "If you care about this coastline, add your name."
- Petition form (prominent)
- Newsletter signup (below petition)
- Visitor count (footer or sidebar — subtle)
- No pressure language. The story already made the case.

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
- **The previous owner of the house:** Was on the WPBCA board in the 1950s
  AND was the Shore Club director. The documents in the garage aren't random —
  they're the institutional archive of someone at the center of both the HOA
  and the Shore Club during the founding era. This is the provenance that
  makes the documentary record credible. Current board member finds
  founding-era documents from a prior board member/Shore Club director.
- **Hartman (separate):** Thomas Hartman (28 Sea Cove, inside WPBCA) sold the
  0 Clipper parcel to Clipper Development LLC. A different thread.
- **Davis-Stirling + technology:** The AI journey started with a practical
  question — wondering about electronic voting and what technology could do
  for HOA governance (Sterling Davis-Stirling Act). That question led to
  exploring AI tools, which led to the document research, which uncovered the
  whole history.
- **"Here's something you didn't know about LA"** — the hook. Even people who
  think they know PV don't know this story. The site becomes where the full
  timeline lives for the first time, and invites readers who know other pieces
  to fill in gaps.
- **The core discovery moment:** "Wait — this isn't just any HOA. This is the
  HOA the Vanderlips created for their own estate." Finding the Vanderlip name
  on the HOA documents, connecting it to the Fed, to Olmsted, to the peninsula
  purchase. And then the contradiction: the city won't fix the beach path
  (CC&Rs won't let them modify the parking lot), but right next door they'll
  rezone for 16 units. The restrictions are an obstacle when the city doesn't
  want to spend money, and invisible when a developer wants to build.
- **Don't get long-winded.** Keep it LA Times Sunday Home section. Clean prose,
  tight paragraphs. Let the facts breathe. The author's personal story is
  connective tissue, not the centerpiece.

### Deep narrative threads (for spine baseline session)

These threads tie the sections together and are the real discoveries:

- **1882 Superior Court decision** — Bixby ownership of Rancho de los Palos
  Verdes, established by court ruling. This is the legal genesis. Vanderlip
  buys from Bixby syndicate in 1913. The chain of title starts here.
- **Lot H and the negative space** — The Vanderlips put declarations on parcels
  they were selling (specific tracts). Lot H was the declaration on the
  NEGATIVE SPACE — everything not covered by named tracts. This is the key
  insight that the mapping exercise revealed.
- **The mapping exercise** — Realizing the negative space pattern is what drove
  the GIS/AI mapping work. You have to MAP the declarations spatially to
  understand coverage. That's what AI + GIS made possible for one person.
- **The sister HOA tracts** — Three HOAs carved from the same PV Corp land,
  each with their own declaration chain. How they relate, where the boundaries
  are, which lots fell through the cracks.
- **The Olmsted map was the dream, not the reality** — The Olmsted plan was an
  artist's rendering of what the contracts described. It was the vision, never
  fully realized. And 0 Clipper/RM-22 is the same kind of pipe dream —
  beautiful density numbers on paper, impossible on an active landslide.
- **Jim York's house** — Why did he get to build there? What was the exception
  or the history that allowed it? Raises the question of precedent.
- **Catalina Gardens** — Why is it there? Same question. What allowed this
  development in this area?
- **HOA enforcement paralysis** — The governance structure the Vanderlips
  built is toothless in 2026. $20/month dues can't fund legal action. Board
  members get personally named when they try to enforce. Neighbors sue each
  other and the board can't intervene without D&O coverage the HOA can't
  afford. Meanwhile: state says HOAs can't restrict (SB9, AB 670), courts
  say CC&Rs still apply (Carlsbad April 2026 ruling), city ignores CC&Rs
  when it suits a developer. CalMatters article (April 2026) confirms HOA
  authority is "largely unregulated by state enforcement agencies."
- **Wayfarers Chapel** — Lloyd Wright's chapel had to be disassembled after
  they started watering the grapes, which triggered slide movement. Same
  thesis as the plumbing-as-catalyst finding: water + this geology = disaster.
  If watering grapes destabilized a chapel, what does 16 units of plumbing do?
- **100 years vacant** — "There is a reason a 1.58-acre lot has sat vacant
  for 100 years of California development, owned by the man who invented it."
  Vanderlip could have built anything. Left it vacant. Every owner after him
  left it vacant. That's not an accident — that's the land telling you something.
- **Infill is the point** — Housing element compliance was designed for infill
  corridors: Jefferson Blvd in West LA, La Cienega, Pleasanton in the East
  Bay. Not condos on the beach on an active landslide.
- **The consulting firm** — City hired a consultant for the April 2025 planning
  commission. Said this was "just about numbers" and nobody would ever need
  permits here. Who is this firm? Where do they pop up around the South Bay?
  Research needed. If no one needs permits, the rezoning is compliance theater.
  But the developer has a $2.1M loan (Hankey Capital, Nov 2025). Someone
  intends to build.

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
