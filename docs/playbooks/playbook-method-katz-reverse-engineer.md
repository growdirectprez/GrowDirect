# Method Playbook — Reverse-Engineer the Katz Engagement Template

Katz is a clean working-papers archive from a 2003 retail supply chain
transformation engagement (Katz Group — Canadian drug chain: Rexall, IDA,
PharmaPlus, Pharma Plus Drug Marts). The folder structure is disciplined,
the artifact naming is consistent, the phase progression is explicit.
It's a textbook consulting engagement. Reverse-engineer the method and
formalize it as a reusable Model in the GrowDirect Method catalog.

---

## Goal

Produce three linked outputs:

1. **Wiki article** — `Brain/wiki/methods/retail-transformation-engagement.md`
   that describes the Katz-derived method as a reusable engagement model.
2. **Template skeleton** — `Brain/templates/engagement-template/` — an
   empty folder structure matching the Katz shape, ready to clone for
   future engagements (or internal product workstreams).
3. **Method MOC update** — add the new model to
   `Brain/projects/Method.md`'s Models section so it appears alongside
   the Factory Pipeline as a parallel GrowDirect Model.

The point is not to revive Katz — it's to harvest the structural
discipline and make it cloneable.

---

## What Katz actually looks like (pre-analyzed)

Saves you the discovery phase. This is what's on disk right now.

### Two-phase engagement structure

```
Katz/
├── Phase I — Assess & Design
│   ├── 01 - Executive Interviews
│   ├── 02 - Store Visits
│   ├── 03 - As-Is Workshops
│   ├── 04 - Executive Visioning
│   ├── 05 - Benchmarking
│   ├── 06 - Balanced Scorecards
│   ├── 07 - Inventory Analysis
│   ├── 08 - Business Case
│   ├── 09 - Presentations
│   └── 10 - Change Management
└── Phase II — Select & Implement
    ├── 03 - System Selection & Supply Chain Optimization
    │   ├── 01. To Be Workshops
    │   ├── 02. RFP Distributed to Vendors
    │   ├── 03. RFP Responses (JDA, SAP, i2, JDE, Retek)
    │   └── 08. Gartner Information
    ├── 04 - Supporting IT Architecture
    └── 07 - Presentations
```

### Artifact patterns worth extracting

**Multi-level compilation pattern.** Individual raw files → compiled
file → summarized compiled file. Example:
- `01 - Executive Interviews/` has one `.xls` per executive (Al Wilkie,
  Craig Taylor, Peter Davidson, Sue Macabe, George Edwards, Grant
  Schwartz, Bruce Moody, Larry Latowsky)
- Plus `Interview compilation.xls` (all interviews merged, untransformed)
- Plus `Interview compilation - summarized.xls` (distilled insights)

Same pattern in `02 - Store Visits/`: per-store files + `Store Visit
Compilation.xls`.

**Per-domain workshops.** Each business domain gets its own as-is and
to-be workshop artifact, versioned and dated:
- Phase I as-is: POS, Pricing, Forecasting, Category Management,
  Inventory, Move (logistics), Manage Vendor, ProPharm (pharmacy
  specialty)
- Phase II to-be: Finance, Store Operations, Suppliers, Merchandising,
  Planning & Analysis, Planning & Distribution

**Naming convention:** `Katz As Is Process WS <Domain> <MM DD YY> v<N>.ppt`
— project prefix + phase + domain + date + version. Parseable, sortable,
unambiguous.

**Steering Committee cadence.** `Katz SC#1 Presentation Final.ppt`, `Phase
II SC#1 Final.ppt`. Numbered, marked Final. SC presentations are the
heartbeat of the engagement.

**Business case triad.** `08 - Business Case/` contains:
- `Katz Group Benefits Case v2.xls` (benefits)
- `Retail Systems Cost Model DRAFT V5.xls` (costs)
- `NPV Model v2.xls` (financial synthesis)
- `Solution Contribution to Value Opportunities V3.xls` (traceability
  from solution components to business value)

Four docs, one financial story. Clean separation of what, how much, by
when, and why-it's-worth-it.

**Executive Visioning as a distinct workstream.** Separate from
interviews. Forward-looking. Has its own deliverable (presentation + doc).
Typically done after as-is but before business case.

**Balanced Scorecards as a framing artifact.** Not a workstream per se —
it's a lens applied over everything. One spreadsheet + one deck.

**Inventory Analysis as proof-of-problem.** Quantitative analysis that
grounds the narrative: `Service Levels.xls`, `Discontinued by Store
v3.xls`, `Inventory Turns By Vendor.xls`, `Inventory Turns By Vendor &
Category.xls`. Four focused analyses, each answering one question.

**RFP process structure.** Sequential numbered folders:
- `01. To Be Workshops` — define what you're asking for
- `02. RFP Distributed to Vendors` — what went out, per-vendor
  (one RFP doc per vendor: i2, JDE, JDA, Retek, SAP)
- `03. RFP Responses` — what came back, per-vendor, including legal
  appendices (EULAs, escrow agreements, SIG outlines)

Vendor folders are parallel. Inside each, the same artifact shape (main
response + attachments/appendices). Would-be shortlist and scoring
artifacts are missing from what's on disk but implied.

**Versioning and "Final" marking.** Documents are explicitly versioned
(v2, v3, v4, v5). The terminal version is marked `Final`. Draft and
revision status is part of the filename. You never wonder which is
canonical.

**Change Management as its own workstream.** Folder `10 - Change
Management/` contains `Draft CRA Katzv6.ppt` (CRA = Change Readiness
Assessment or similar). A reminder that no transformation succeeds on
analysis alone.

---

## Phase 0 — Create Linear parent

- [ ] Create Linear issue: **"Method: Retail Transformation Engagement
      Template (Katz-derived)"** in Growdirect team, appropriate project
      (maybe the Platform or Method project if one exists; otherwise
      GrowDirect Operations).
- [ ] Description: "Per docs/playbook-method-katz-reverse-engineer.md.
      Reverse-engineer the Katz engagement structure into a reusable
      GrowDirect Model. Three outputs: wiki article, template skeleton,
      Method MOC update."
- [ ] Priority: Medium. Label: Method / Documentation.
- [ ] Record GRO-### here: ________________________

---

## Phase 1 — Catalog what exists (confirm + extend)

I've done an initial directory scan. You read through the actual content
to confirm the extracted pattern holds and to find anything I missed.

- [ ] Walk through each Phase I workstream folder (01-10) in order.
      For each:
  - Read the 1-2 key artifacts (the final presentation, the summarized
    compilation). Don't read everything — read the distilled versions.
  - Note the workstream's **purpose**, **inputs**, **outputs**, and
    **who-does-it** (SMEs, consultants, execs).
- [ ] Repeat for Phase II workstreams.
- [ ] Produce a quick one-pager summary at
      `Brain/raw/inbox/Katz/_method-notes.md` with the confirmed /
      extended taxonomy. (Delete this later per CLAUDE.md cleanup rule;
      it's scaffolding.)

---

## Phase 2 — Extract the method

Go from "what Katz did" to "what the method is" — generalize away from
the specific retail-pharmacy context.

- [ ] For each workstream, answer four questions in a structured way:
  - **What question does this workstream answer?** (E.g., Executive
    Interviews answer "what do leaders think is broken and what do they
    want?")
  - **What are its input artifacts?** (E.g., stakeholder list, interview
    guide, exec calendars)
  - **What are its output artifacts?** (E.g., individual analyses,
    compilation, summarized compilation, themes deck)
  - **When in the sequence does it run?** (E.g., week 1-2, before
    visioning)
- [ ] Identify the workstreams that are **sequential** (must precede
      another) vs. **parallel** (can run alongside).
- [ ] Identify the workstreams that are **universal** (every engagement
      needs them) vs. **conditional** (only when relevant — e.g., RFP
      only if system selection is in scope).
- [ ] Map the artifact patterns into reusable conventions:
  - Naming: `<Project> <Phase> <Workstream> <Artifact> <Date> v<N>[.Final].ext`
  - Compilation triad: raw → compiled → summarized
  - Business case triad: benefits / costs / NPV / solution-value
  - SC cadence: numbered, dated, Final-marked
  - Per-domain parallel artifacts (one deliverable per business domain
    in scope)

---

## Phase 3 — Write the method article

Canonical reference. This becomes the referenceable Model.

- [ ] Create `Brain/wiki/methods/retail-transformation-engagement.md`
      (check Brain templates folder for the appropriate wiki-article
      template first).
- [ ] Structure:
  - **Overview** — what this method is, when to use it, duration
    (Katz-scale engagement is 6-12 months)
  - **Preconditions** — when does this method apply? (Enterprise-scale
    operational change with technology implications. Not for product
    development, not for small ops changes.)
  - **Two-phase structure** — diagram (Mermaid) showing Phase I and
    Phase II and the handoff between them
  - **Phase I — Assess & Design** — one subsection per workstream
    (01-10), each with purpose / inputs / outputs / timing from Phase 2
  - **Phase II — Select & Implement** — same treatment
  - **Artifact conventions** — naming, versioning, compilation triad,
    business case triad, SC cadence
  - **Ceremonies** — kickoff, weekly SC, visioning sessions, workshops
    (as-is and to-be), RFP process, final report
  - **Adaptations** — how this method flexes: for product-only work,
    for SaaS migration, for pure analysis (no selection)
  - **Anti-patterns** — common ways this method fails (skipping
    visioning, business case without traceability, RFP without clear
    requirements, no change management)
  - **Reference implementation** — Katz 2003 (link to archive), maybe
    Harrods (if similar structure, though less disciplined)
- [ ] Cross-link to existing Method assets:
  - `[[Brain/projects/Method|Method MOC]]` — this is a sibling to
    Factory, both are Models
  - `[[Brain/projects/Factory|Factory Pipeline]]` — contrast: product
    dev, not transformation
  - Any role profiles (ALX, Tom, Eva) that map to engagement roles
    (engagement lead, solution architect, PMO)

---

## Phase 4 — Build the template skeleton

Create the cloneable starter kit.

- [ ] Create `Brain/templates/engagement-template/` with the structure:

```
engagement-template/
├── README.md                              (how to use this template)
├── Phase I - Assess & Design/
│   ├── 01 - Executive Interviews/
│   │   ├── _README.md                     (what goes here)
│   │   ├── _interview-guide-template.md
│   │   └── _compilation-template.md
│   ├── 02 - Field Visits/                 (renamed from "Store Visits" — generic)
│   │   ├── _README.md
│   │   └── _visit-report-template.md
│   ├── 03 - As-Is Workshops/
│   │   ├── _README.md
│   │   └── _workshop-deck-template.md
│   ├── 04 - Executive Visioning/
│   ├── 05 - Benchmarking/
│   ├── 06 - Balanced Scorecards/
│   ├── 07 - Quantitative Analysis/        (renamed from "Inventory Analysis" — generic)
│   ├── 08 - Business Case/
│   │   ├── _README.md
│   │   ├── _benefits-template.md
│   │   ├── _cost-model-template.md
│   │   ├── _npv-template.md
│   │   └── _solution-value-traceability-template.md
│   ├── 09 - Presentations/
│   │   ├── _kickoff-deck-template.md
│   │   ├── _sc-deck-template.md
│   │   └── _final-report-template.md
│   └── 10 - Change Management/
├── Phase II - Select & Implement/
│   ├── 01 - To-Be Workshops/
│   ├── 02 - RFP Package/                  (renamed from "RFP Distributed..." — simpler)
│   ├── 03 - RFP Responses/
│   │   └── _vendor-folder-template/       (clone per vendor)
│   ├── 04 - IT Architecture/
│   ├── 05 - Scorecard & Shortlist/        (added — was implied in Katz but not present)
│   ├── 06 - Contract Negotiation/         (added — Katz has legal artifacts but no explicit workstream)
│   ├── 07 - Presentations/
│   └── 08 - Research & External/          (renamed from "Gartner Information" — generic)
└── _engagement-charter-template.md        (new — Katz didn't have one explicitly, but modern engagements should)
```

- [ ] Each `_README.md` in a workstream folder answers the same four
      questions from Phase 2: what question does this workstream answer,
      inputs, outputs, timing.
- [ ] Each `_*-template.md` is a fillable markdown skeleton for the
      corresponding artifact. Obsidian-friendly frontmatter.
- [ ] The top-level `README.md` is the usage guide:
      "To start a new engagement, clone this folder, rename to
      `<Project>/`, delete workstream folders that don't apply, fill in
      the charter."

---

## Phase 5 — Integrate with the Method MOC

- [ ] Edit `Brain/projects/Method.md`. In the Models section, add a
      bullet alongside Factory:

```
- [[Brain/wiki/methods/retail-transformation-engagement|Retail
  Transformation Engagement]] — 2-phase engagement model
  (assess/design → select/implement) derived from the Katz 2003 archive.
  Use for enterprise operational change with technology implications.
```

- [ ] Also add to `Brain/method/Models` index (the referenced "Models
      Index" from Method MOC).
- [ ] Add a note in the Method MOC's "How to use" section:
      *"Starting an engagement (not a product build)?" See
      [[Brain/wiki/methods/retail-transformation-engagement|Retail
      Transformation Engagement]] method and the clonable template at
      `Brain/templates/engagement-template/`.*

---

## Phase 6 — Apply the method (test it)

The method isn't proven until it's used. Trial-run it on something small.

- [ ] Pick one of: an in-flight GrowDirect workstream (e.g., the
      Canary beta launch), or a hypothetical engagement (e.g., if
      someone asked you to do a supply chain transformation for a
      mid-sized retailer, how would you shape it?).
- [ ] Clone `Brain/templates/engagement-template/` to a working location.
- [ ] Populate the engagement charter + 1-2 workstreams enough to feel
      whether the template fits.
- [ ] Note friction — where does the template force you into patterns
      that don't fit? Update the template and the wiki article
      accordingly.

---

## Phase 7 — Cleanup

- [ ] Delete `Brain/raw/inbox/Katz/_method-notes.md` (scratch from Phase 1).
- [ ] Keep the Katz archive at `Brain/raw/inbox/Katz/` as the reference
      implementation — do NOT move or reorganize it. Its structure IS
      the reference.
- [ ] Commit: "Method: Retail Transformation Engagement Template derived
      from Katz archive (closes GRO-###)".

---

## Design notes for the wiki article

Things worth saying explicitly when you write Phase 3:

**The method's strength is its discipline, not its novelty.** Every piece
here is standard consulting practice. What makes Katz clean is that
nothing is missing, nothing is duplicated, and naming / versioning is
enforced. The discipline is the product.

**Two-phase separation matters.** Phase I ends with a decision (to
proceed, to a specific vision, to a business case). Phase II is
execution against that decision. Blurring them — "let's do visioning
while also evaluating vendors" — is a common failure mode. The method
forces the sequence.

**Compilation triads are load-bearing.** Raw → compiled → summarized is
how you avoid losing the thread of an interview series. The individual
files are audit trail; the compilation is the thesis; the summary is
what the SC actually reads. Dropping any layer breaks the chain.

**The business case triad is the bridge between phases.** Benefits
articulate the prize. Cost model sizes the investment. NPV synthesizes.
Solution-value traceability links the business case back to the
to-be design. Without that traceability, Phase II becomes untethered.

**Per-domain workshops force completeness.** You don't get to skip
Inventory. You don't get to fold Forecasting into Pricing. The domain
boundaries force coverage. Yes, it's rigid. That's the point.

**Change Management as a workstream, not an afterthought.** Katz's folder
`10 - Change Management/` is sparsely populated (one draft deck), which
is actually a failure mode worth calling out — CM tends to get
deprioritized. The method says: make it a workstream, give it a folder,
track it like everything else. Whether it's done well is a separate
question; the method at least forces its visibility.

**What Katz was missing (and the template should add):**
- Explicit engagement charter document (scope, roles, governance, dates)
- Scoring rubric for RFP responses (not visible in archive)
- Shortlist rationale (how did JDA/SAP rise and i2/JDE fall?)
- Contract negotiation artifacts as their own workstream (the SAP
  response folder has legal appendices but no negotiation trail)
- Post-selection handoff brief (Phase II → implementation partner)

Call those out as template improvements.

**Adaptation guidance.** Most GrowDirect work is product development,
not transformation — Factory Pipeline covers that. The Retail
Transformation Engagement model is for:
- External client work if GrowDirect picks up consulting
- Internal "transformation moments" — e.g., the email migration is a
  micro-version of a tiny transformation; the real test is something
  bigger (AWS cutover? Platform v2?)
- Applying the engagement discipline to strategic decisions that are
  otherwise ad-hoc (e.g., "which MLM vertical do we pursue?" could run
  through a compressed Phase I in 2 weeks)

---

## Sizing

- Phase 1 (read through Katz to confirm): 3-4 hours (lots of .xls, .ppt
  to skim; you don't need to read every cell)
- Phase 2 (extract method): 2-3 hours of synthesis
- Phase 3 (wiki article): 3-5 hours of writing
- Phase 4 (template skeleton): 2-4 hours (mostly README + template
  stubs; can be incrementally populated)
- Phase 5 (Method MOC integration): 30 min
- Phase 6 (test application): 2-4 hours depending on test scope
- Phase 7 (cleanup): 15 min

**Total: 2-3 sessions of focused work.** Can be chunked across more
sessions without losing state — each phase produces its own artifact.

---

## Related Linear / Brain context

- **`Brain/projects/Method.md`** — existing Method MOC. This work adds a
  Model to the Models section.
- **`Brain/projects/Factory.md`** — the dominant current Model.
  Retail Transformation is the parallel sibling Model for engagement-shaped
  work.
- **GRO-520** — Hierarchical Brain architecture. Relevant because
  the engagement template sits at a specific trust boundary (personal
  method / ops brain). Coordinate placement.
- **Retail Ops Model playbook** (`docs/playbook-retail-ops-model.md`) —
  parallel but different goal. That playbook mines the Harrods/Heartbeat
  archives for *content* (functional requirements). This playbook mines
  Katz for *structure* (engagement method). Cross-reference: the Retail
  Ops Model could itself be produced *using* the engagement method. Meta,
  but valid.
