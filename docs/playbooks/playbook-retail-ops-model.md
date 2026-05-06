# Retail Ops Model — Functional Requirements Synthesis Playbook

Mine the working papers in `Brain/raw/inbox/` (Harrods + Heartbeat archives)
to catalog the best functional requirements we can derive from them, and
synthesize a Retail Operations Model + BRD set that informs Canary's
product direction.

---

## Goal

Produce a structured **Retail Operations Model** and companion **BRD
(Business Requirements Document) set** grounded in actual prior-art retail
consulting work — not invented from scratch. The model becomes the frame
for future Canary features, partner conversations, and deck-level
positioning.

Output artifacts, in order of value:

1. **Retail Ops Model v1** — wiki article at `Brain/wiki/retail-ops-model.md`
   describing the end-to-end operational domains of a retail business and
   how they relate. Canonical reference.
2. **BRD set** — one BRD per domain (merchandising, inventory, order
   management, store ops, loss prevention, etc.), stored at
   `Brain/wiki/brds/<domain>.md`.
3. **Linear issues** — one parent epic + children for anything in the BRDs
   that should feed Canary's roadmap.

---

## Scope decision — before starting

The inbox contains two distinct archives. Pick which is in scope for this
pass. Recommendation: **both**, but process Harrods first (higher-value
BRD material) then Heartbeat.

- [ ] **Harrods archive** — `Brain/raw/inbox/Harrods/` — ~50 files.
      Content: vendor quant analysis, checklists, process flows,
      merchandising processes, customer/mdse attributes, software eval,
      BMS assumptions, BAA session notes. This is BRD gold.
- [ ] **Heartbeat / Fireball archive** — `Brain/raw/inbox/Heartbeat/` — ~20
      files. Content: Retail BizTalk Resource Kit, M&S architecture, OOS
      architecture, notification design, web-based fireball
      documentation. Architecture-heavy, more systems-design than BRD.

Record scope decision: ________________________

---

## Phase 0 — Create the Linear parent

Per CLAUDE.md "No scaffolding without a Linear issue" rule — do this first.

- [ ] Create Linear issue: **"Retail Ops Model — synthesize BRD set from
      Brain/raw/inbox archives"** in the Growdirect team, Canary project.
- [ ] Description: "Process Harrods + Heartbeat archives per
      docs/playbook-retail-ops-model.md. Produce Retail Ops Model wiki
      article + BRD set. Parent for child issues per domain."
- [ ] Priority: Medium. Label: Strategy & Research.
- [ ] Note the GRO-### and reference it in every commit.

---

## Phase 1 — Extract + ingest (mechanical)

Follow the Intake Protocol from CLAUDE.md. This is the "I have project
working papers to process" flow.

- [ ] Verify `content-engine/` tooling works:
      `cd content-engine && python3 engine.py --help`
- [ ] Run extract on Harrods: binaries → markdown scratch.
      `python3 engine.py extract Brain/raw/inbox/Harrods/`
      - Note files that fail to parse (.vsd Visio files, .mpp MS Project,
        .zip archives, .ppt with heavy graphics often fail). Log them.
- [ ] Run ingest: scratch → `Brain/raw/inbox/<slug>.md` with source path
      in frontmatter. `python3 engine.py ingest`
- [ ] Rebuild registry: `python3 engine.py registry build`
- [ ] Verify with `engine.py registry check "harrods"` — should return
      count matching the extracted file count.
- [ ] Repeat for Heartbeat archive (if in scope).

Report back after Phase 1: total files in, extraction failure count, list
of files that need manual attention.

---

## Phase 2 — Categorize (analytical)

Before synthesis, sort the intakes by retail operational domain. Don't
write anything yet — just tag.

- [ ] Read through each intake in `Brain/raw/inbox/*.md` and classify into
      one of these domains (standard retail ops taxonomy):
  - **Merchandising** — assortment planning, category management, pricing,
    promotions, markdown management
  - **Supply Chain / Inventory** — vendor management, POs, receiving, stock
    counts, shrink, replenishment
  - **Order Management** — customer orders, fulfillment, returns, exchanges
  - **Store Operations** — opening/closing, labor, training, compliance
  - **Loss Prevention** — shrink detection, fraud, audit, investigations
    *(direct Canary relevance — prioritize)*
  - **Customer / Loyalty** — CRM, customer attributes, segmentation
  - **Integration / Architecture** — system interfaces, data flows, BizTalk
    patterns *(mostly Heartbeat content)*
  - **Cross-cutting** — strategy, org design, training, pros/cons docs
- [ ] Produce a category index: simple markdown table with filename →
      domain → one-line summary. Save at
      `Brain/raw/inbox/_category-index.md`.

---

## Phase 3 — Synthesize the Retail Ops Model (the core deliverable)

Now write the wiki article. This is the canonical reference.

- [ ] Create `Brain/wiki/retail-ops-model.md` following the Brain template
      convention (check `Brain/templates/` for format).
- [ ] Structure the article around the 8 domains from Phase 2.
- [ ] For each domain, include:
  - **Purpose** — what this domain does in retail ops, in one paragraph
  - **Key processes** — bullet list, 3-7 processes
  - **Key data entities** — what moves through this domain (orders,
    items, customers, etc.)
  - **Interfaces** — upstream/downstream domains it touches
  - **Prior-art references** — link to specific intakes from Phase 1 that
    informed this section, e.g.
    `[[inbox/harrods-merchandising-processes]]`
  - **Canary relevance** — how current or future Canary features map to
    this domain (loss prevention is central; others peripheral)
- [ ] Include a top-level diagram (Mermaid, in the wiki article) showing
      how the 8 domains relate. Think concentric circles with store ops
      at the center, or a value chain left-to-right.
- [ ] Cross-link aggressively — wiki-style `[[article-name]]` links to
      other Brain articles where relevant.

---

## Phase 4 — Extract BRDs per domain

One BRD per domain that has enough raw material to justify one. Loss
prevention and merchandising will almost certainly; others may be thin.

For each domain with ≥5 relevant intakes:

- [ ] Create `Brain/wiki/brds/<domain>.md`.
- [ ] Structure:
  - **Background & scope** — one page
  - **Business objectives** — bullet list, tied to prior-art evidence
  - **Functional requirements** — numbered list (FR-001, FR-002...) with
    each requirement citing the intake(s) it came from
  - **Non-functional requirements** — performance, security,
    integration, reporting
  - **Out of scope** — explicit
  - **Open questions** — things the source material didn't answer
- [ ] Keep it descriptive, not prescriptive. This is "what retail ops
      requires" distilled from prior engagements — not "what we will
      build." Avoid language that commits Canary to anything.

---

## Phase 5 — Link to Canary roadmap

Where the BRDs surface something Canary should build, formalize it.

- [ ] For each FR that implies a Canary feature, create a child Linear
      issue under the parent from Phase 0.
- [ ] Title format: "Retail Ops Model FR-### — <feature>".
- [ ] Description should link to the BRD and quote the relevant FR.
- [ ] Priority based on Canary roadmap fit, not BRD completeness.

---

## Phase 6 — Cleanup

Per CLAUDE.md "Clean up your own artifacts" rule.

- [ ] Delete the `_category-index.md` scratch file (content is now in the
      BRDs and wiki article).
- [ ] Keep the extracted intakes in `Brain/raw/inbox/` — they're the
      permanent trail. They're not cleanup artifacts.
- [ ] Commit: "Retail Ops Model v1: ingested Harrods + Heartbeat,
      wiki + BRDs (closes GRO-###)".

---

## Reference — what's in the inbox right now

Top of mind for planning purposes.

**Harrods (`Brain/raw/inbox/Harrods/`):** ~50 files, mostly .doc, .ppt,
.xls, .vsd. Highlights spotted:
- `Harrods_Process_Arch.ppt`, `Harrods_Process_List.xls`,
  `Harrods_Flows.ppt` — process architecture, will seed the "Store Ops"
  and "Merchandising" sections
- `Merchandising_Processes.xls`, `Merchandise processes Doc.doc`,
  `Mdse Attributes v1.1.doc`, `HOT Mdse Hierarchy 1.1.doc` — merchandising
  domain
- `Customer Attributes 1.0.doc`, `Customer Order.vsd` — customer/order
  management
- `Order management process.doc` — order management
- `Returns.vsd` — order management / customer service
- `Vendor Quantitative Analysis.xls`, `Checklist-Purchase Order.doc`,
  `Checklist-Inventory.doc` — supply chain / vendor management
- `BMS Assumptions.xls`, `Assessment.xls`, `Issues.xls` — strategy /
  cross-cutting
- `Harrods JDA BAA Session Notes.doc` — BAA (Business Area Analysis)
  session, will be a central source
- `Software eval scripts_2.xls`, `Pros_Cons.doc` — software evaluation
  (could inform Canary's sales narrative)
- `Harrods Strategy and Org Questions.doc` — strategy / org design

**Heartbeat (`Brain/raw/inbox/Heartbeat/`):** ~20 files, mostly architecture
and BizTalk resource kit content. Highlights:
- `Heartbeat OOS Architecture.ppt` — out-of-stock architecture
- `Notification System Specification1221.doc` — notification/alerting
  (has LP relevance)
- `Fireball_Notification_StoryBoard.ppt` — UX for operational alerts
- `MarksSpencer Architecture.ppt` — M&S retail architecture (reference)
- `Phase-I Pilot Assessment.doc` — implementation assessment
- Retail BizTalk Resource Kit docs — integration patterns

**Not expected to extract cleanly:** `.vsd`, `.mpp`, `.zip`, very-graphics
`.ppt`. Those need manual review or alternate tooling.

---

## Related Linear context

These existing issues are adjacent — reference them in the wiki so the
Retail Ops Model connects to current Canary work, not just historical
archives.

- **GRO-144** — Ops Dashboard (Walmart SRA Scorecards DNA). Done. The
  retail ops scorecard pattern that Canary already implements.
- **GRO-145** — 4-5-4 retail fiscal calendar. Done. Retail time domain.
- **GRO-297** — Sandbox seeder: inventory adjustments + ordering for
  shrink rule testing. Backlog. Direct Canary/inventory domain tie-in.
- **GRO-129** — The Owl: agentic retail intelligence engine. Done.
- **GRO-496** — Distill manifesto + warchest into wiki articles.
  Backlog. Complementary knowledge distillation work.

---

## Sizing

Rough estimates:
- Phase 1 (extract/ingest): 1-2 hours, mostly waiting on extraction
- Phase 2 (categorize): 2-4 hours of reading
- Phase 3 (wiki article): 3-6 hours of writing + thinking
- Phase 4 (BRDs): 2-4 hours per domain × 4-6 domains = 8-24 hours
- Phase 5 (Linear issues): 1-2 hours
- Phase 6 (cleanup): 30 min

Total: 2-5 sessions of focused work. Can be chunked cleanly.
