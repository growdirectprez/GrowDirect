# Heartbeat / Fireball (2002) Deep-Dive Playbook

Mine the entire `Brain/raw/inbox/Heartbeat/` archive (417 files, PwC
Consulting + Microsoft + Intel, ~2001–2003) as prior art for Canary.
**Everything in the folder matters.** This is a goldmine deep-dive, not
a blueprint-synthesis pass — the 2002 Heartbeat / Fireball system is
the direct architectural ancestor of what Canary is now building for
Square merchants, and the full archive deserves the same research
treatment Staples L2, Tesco TOM, and IBM Retail BI already got.

---

## Naming disambiguation — read first

**There are two "Heartbeats" in this project, and Jeffe has confirmed
they are related.** The playbook treats them as distinct-but-connected
— one is the 2002 prior-art product, the other is a 2026 evolution of
the same thinking into Bitcoin-native retail infrastructure:

1. **Heartbeat / Fireball (2002)** — PwC Consulting + Microsoft +
   Intel retail out-of-stock detection + notification product.
   Microsoft BizTalk Server. Sold to Marks & Spencer, American Eagle,
   and others. **This playbook is about this one.**

2. **Canary Heartbeat Network (2026)** — Manifesto V.5.6 / Data
   Strategy NorthStar (Feb 2026): every IoT device in a store anchors
   its event timestamps to a shared Bitcoin-derived heartbeat,
   enabling cross-merchant provable event ordering. Referenced in
   [[Brain/wiki/growdirect-data-strategy|Data Strategy NorthStar]]
   and the Canary `services/tsp/heartbeat.py` module.

**The relationship is a Phase 6 deliverable to characterize exactly.**
Plausible forms:

- **Direct homage** — Jeffe named the Canary module deliberately after
  the 2002 product concept
- **Conceptual lineage** — the "periodic signal of liveness broadcast
  from a system to subscribers" metaphor is the same thing; Canary's
  Bitcoin-anchor evolution is the next-generation take on it
- **Architectural lineage** — the trickle-feed-to-subscribers pattern
  from Heartbeat/Fireball 2002 is the direct ancestor of Canary's
  TSP (Triple Subscriber Pipeline), and the Heartbeat naming reflects
  that architectural DNA

Every research output uses **"Heartbeat / Fireball (2002)"** in titles
when referring to the historical product and **"Canary Heartbeat
Network"** for the 2026 module, to keep the documents unambiguous
even while the conceptual thread runs between them.

---

## Why a playbook for this

Canary and Heartbeat / Fireball 2002 solve the same structural problem
— **transaction-stream exception detection with plain-language
notifications to a business operator.** Heartbeat solved it in 2002 for
enterprise retailers (Marks & Spencer, American Eagle, others) using
BizTalk trickle feeds and a PwC services implementation. Canary solves
it in 2026 for Square SMBs using webhooks and self-service SaaS.

Heartbeat is not a competitor to study. It is the **prior art blueprint
that Canary unknowingly re-derived**, and that blueprint was funded
and productized by one of the Big Four plus Microsoft plus Intel.
That's IP validation Canary would otherwise never have.

We have prior art for how to mine this kind of archive — three prior
deep-dives produced high-value output:

- `docs/research/tesco-tom/` (2026-03 Jeffe sprint) — Tesco Operating
  Model mined into OM_MAP, TOM_PROPERTY_SERVICES, CANARY_PROCESS_MAP
- `docs/research/staples-l2/` (2026-03 Jeffe sprint) — Staples Level 2
  process library (Management Horizons / PwC 1996) mined into 15 files
  + INDEX + CANARY_PROCESS_MAP
- `docs/research/ibm-retail-bi/` (2026-03 Jeffe sprint) — IBM Retail BI
  mined into RETAIL_BI_SOLUTION_V7 + CANARY_LINEAGE_MAP + INDEX

This playbook follows the same pattern, scaled to Heartbeat's 417
files. Output folder: `docs/research/heartbeat-fireball-2002/`.

---

## Goal

Produce a **complete research breakdown** of the Heartbeat / Fireball
2002 archive, parallel in quality and structure to the Staples L2 and
Tesco TOM breakdowns. Not a wiki summary. A research library.

### Primary output location

`docs/research/heartbeat-fireball-2002/`

### Expected files (minimum — more if the archive warrants)

| File | Source material | Purpose |
|---|---|---|
| `INDEX.md` | n/a — curated | Entry point, TOC, reading order |
| `VISION_SCOPE.md` | `MS Overview/Fireball Vision Scope.doc` + `Background.htm` + `Functional Overview.htm` | The product's manifesto — what Heartbeat was trying to be |
| `OOS_ALGORITHM.md` | `MS Overview/Algorithm.htm` + `Heartbeat OOS Architecture.ppt` + `A4R - Sample Process Flow.ppt` | The core out-of-stock detection algorithm |
| `DATA_ARCHITECTURE.md` | `Approved Heartbeat Data Architecture.ppt` + `Trickle Feed Data flow.ppt` + `MS Overview/Solution Architecture.htm` + `MS Overview/Process Flows.htm` | The end-to-end data pipeline (ingest → process → output) |
| `NETWORK_ARCHITECTURE.md` | `Fireball Network Architecture.vsd` + `Fireball Future Implementation.vsd` + `Fireball Implementation.vsd` + `BTS AIC Architecture.vsd` + `biztalk.jpg` | Physical network topology and BizTalk Application Integration Component layer |
| `NOTIFICATION_DESIGN.md` | All files in `Notification Design/` (7 files including both XML schema versions + storyboard + customer spec + subsystem doc) | The notification subsystem — the direct analogue to Canary's Chirp module |
| `XML_SCHEMA_EVOLUTION.md` | `Project-Hearbeat_XMLschema_6_Aug[1].doc` + `..._15_Jan.doc` | Event schema evolution between Aug and Jan — what changed and why |
| `RBK_REFERENCE.md` | `rbk/Retail Biztalk Resource Kit/` + `Retail Biztalk Resource Kit/` (108 htm files) | Microsoft's Retail BizTalk Resource Kit that Heartbeat was built on. Index + summary, not full reproduction |
| `SERVICE_OFFERING.md` | All files in `Service Offering/` (8 files: phase plans, pilot assessment, GTM estimates, technical infrastructure questionnaire, generic tech pack) | What was being sold, at what stage of productization |
| `GTM_SALES_DECKS.md` | `sales deck v1.ppt` + `v3.ppt` + `v4.ppt` + `POV 4 Box.ppt` + `Retail POV - RCU Final.ppt` + `sales deck v3.ppt` + `PWCNov20Background.ppt` + `PWCNov25Products.ppt` + `Retail Update Jan 31 (herb kleinberger).ppt` | Sales narrative evolution |
| `CLIENT_MARKS_SPENCER.md` | `MarksSpencer Architecture.ppt` + any M&S-specific notification design docs | Marks & Spencer implementation deep-dive |
| `CLIENT_AMERICAN_EAGLE.md` | `american eagle proposal 01_01 v2.pdf` | American Eagle proposal analysis |
| `CLIENT_COLUMBUS.md` | `Columbus17Dec.ppt` + `2002-04-02 heartbeat project status.ppt` | Columbus client status + program-level status |
| `CVCS_DIAGNOSTIC.md` | All 8 zipped artifacts in `CVCS Diagnostic/` | Collaborative Value Chain Solutions methodology — Heartbeat's companion sales methodology |
| `PWC_MS_INTEL_ALLIANCE.md` | `PwC_MS_Intel_IVM.vsd` + related alliance-shape artifacts | The three-way partnership structure |
| `CODE_ARTIFACTS.md` | `Program Files/Biztalk DLLs/*` (NotificationSubscriptions.BAK, SortFile1.xsl, SortFile2.xsl) | What code existed and what it did |
| `CANARY_LINEAGE_MAP.md` | All of the above | Synthesis — maps every Heartbeat component to a Canary analogue (1:1 / transformed / net-new). Parallel to `docs/research/ibm-retail-bi/CANARY_LINEAGE_MAP.md` |
| `TIMELINE.md` | All dated artifacts across the archive | When what was built, shipped, and what happened to the product |
| `OPEN_QUESTIONS.md` | n/a — curated | What the archive does NOT tell us, and where to look to resolve |

**Minimum: 19 files.** Expand if client-specific material warrants
standalone treatment or if the RBK yields unexpected depth.

### Secondary output — wiki cards

After the research folder is complete and CANARY_LINEAGE_MAP is
written, produce a small set of Brain wiki cards that reference it:

- `Brain/wiki/secure-heartbeat-fireball-2002.md` — top-level product
  card, ~ the "Secure Platform Overview" equivalent for Heartbeat.
  Cites the research folder. Short (5–8 minute read).
- `Brain/wiki/secure-heartbeat-fireball-blueprint.md` — the
  Canary-positioning synthesis derived from CANARY_LINEAGE_MAP.
- Update `Brain/wiki/secure-retail-career-archive.md` — convert the
  "Heartbeat — Secure adjacent" stub into a proper card link.

### Tertiary output — brief

`docs/briefs/2026-04-heartbeat-fireball-blueprint.md` — 2–3 page
product memo for co-founder / investor audience. Companion to the
existing `docs/superpowers/briefs/2026-04-secure-to-canary-handoff.md`.

---

## Source inventory

**417 files** at `Brain/raw/inbox/Heartbeat/`. Extension breakdown:

| Count | Extension | Treatment |
|---:|---|---|
| 108 | `.htm` | FrontPage-era documentation sites — extract via `html2text` or markitdown; skim aggressively, deep-read only MS Overview + Fireball TOC |
| 66 | `.gif` | Mostly web-site icons + screenshots. Skip except where figures are called out in .htm/.doc |
| 45 | `.jpg` | Same treatment as .gif |
| 36 | `.doc` | Core content — full extraction via markitdown. Includes vision, notification specs, XML schemas |
| 28 | `.ppt` | Core content — full extraction via LibreOffice → .pptx → markitdown (per 2026-04-23 legacy-.ppt pipeline) |
| 28 | `.class` | Compiled Java — skip |
| 20 | `.xml` | Schema + config — inspect selectively |
| 16 | `.wmz` | Windows Metafile compressed — embedded in docs, skip standalone |
| 11 | `.zip` | Unpack CVCS Diagnostic zips; skip WebFiles.zip / RBKFinal.zip (redundant with unpacked directories) |
| 9 | `.vsd` | Visio architecture diagrams — critical. LibreOffice Draw → PDF + screenshot + OCR |
| 6 | `.xls` | Core content — full extraction |
| 5 | `.fp_folder_info`, `.cnf` | FrontPage scaffolding — skip |
| 4 | `.xdr` | XML Data Reduced schemas — inspect with XML |
| — | other | Case-by-case |

### Primary-value assets (read first)

Follow this reading order for anyone executing Phase 2. Do not
shortcut.

1. `MS Overview/Background.htm` — what is this product
2. `MS Overview/Fireball Vision Scope.doc` — the manifesto
3. `MS Overview/Functional Overview.htm` — scope
4. `MS Overview/Algorithm.htm` — the OOS detection math
5. `MS Overview/Solution Architecture.htm` — stack
6. `MS Overview/Process Flows.htm` — data flow
7. `Approved Heartbeat Data Architecture.ppt` — the canonical architecture deck
8. `Trickle Feed Data flow.ppt` — ingest pattern
9. `Heartbeat OOS Architecture.ppt` — the flagship use case architecture
10. `Fireball Network Architecture.vsd` — network topology
11. `BTS AIC Architecture.vsd` — BizTalk Application Integration Component layer
12. `A4R - Sample Process Flow.ppt` + `a4r scenario.vsd` — Alerts for Retail scenarios
13. `Notification Design/Notification Design Spec.doc`
14. `Notification Design/Notification System Specification1221.doc`
15. `Notification Design/Notification Subsystem Documentation.doc`
16. `Notification Design/Notification Design Customer Aug 6.doc`
17. `Notification Design/Fireball_Notification_StoryBoard.ppt`
18. `Notification Design/Project-Heartbeat_XMLschema_6_Aug[1].doc`
19. `Notification Design/Project-Heartbeat_XMLschema_15_Jan.doc`
20. `sales deck v1.ppt` → `v3.ppt` → `v4.ppt` (narrative evolution)
21. `Retail POV - RCU Final.ppt` — industry positioning
22. `PwC_MS_Intel_IVM.vsd` — alliance structure
23. `Fireball Go to Market Solution Estimates.xls` — pricing
24. `Service Offering/Phase-I Pilot Assessment.doc` — pilot retrospective
25. `Service Offering/Phase II development plan.doc.vsd` — what was next
26. `MarksSpencer Architecture.ppt` — M&S reference client
27. `american eagle proposal 01_01 v2.pdf` — AE pursuit
28. `Columbus17Dec.ppt` — Columbus program status
29. `2002-04-02 heartbeat project status.ppt` — April 2002 program-level snapshot
30. `Retail Update Jan 31 (herb kleinberger).ppt` — Herb Kleinberger update

### Secondary-value assets (read second)

- `CVCS Diagnostic/` — 8 zipped artifacts (Issue Mapping v3.0, Sales
  Deck, Practitioners Guide v3.0, HP PwC white paper Creating Value
  through Collaboration, Presentation of Findings, Industry POVs,
  ROI Model v3.0, Diagnostic Sales Deck). Unpack + skim.
- `PWCNov20Background.ppt` + `PWCNov25Products.ppt` — PwC consulting
  background.
- `Heartbeat/Fireball Documentation/Fireball Documentation/Budget.xls`

### Tertiary-value / reference-only

- `rbk/Retail Biztalk Resource Kit/Documentation/` + parallel
  `Retail Biztalk Resource Kit/Documentation/` (108 .htm files) —
  Microsoft's Retail BizTalk Resource Kit. This is Microsoft's IP,
  not Heartbeat's. **Do NOT deep-read it.** Index it as the foundation
  Heartbeat was built on (RBK_REFERENCE.md), link out, move on.
- `WebFiles/` + `WebFiles.zip` — Fireball product website content.
  Redundant with MS Overview content. Skim once, reference only.

### Skip entirely

- `_vti_cnf/`, `_vti_*`, `.fp_folder_info`, image thumbnails in
  `*_files/` directories (FrontPage scaffolding)
- `Program Files/Biztalk DLLs/*.class` — Java compiled binaries
- Redundant zip archives where the unpacked content exists
  (`RBKFinal.zip`, `WebFiles.zip`, `Fireball Documentation.zip`,
  `Service Offering.zip`)

---

## Phase 0 — Linear parent + folder scaffold

- [ ] Create Linear issue: **"Heartbeat / Fireball 2002 — research
      deep-dive of Brain/raw/inbox/Heartbeat/"** in Growdirect team,
      Canary project. Priority: Medium. Label: Strategy & Research.
- [ ] Description: *"417-file PwC + MS + Intel retail OOS +
      notification archive. Deep-dive per
      `docs/playbook-heartbeat-blueprint.md`. Output:
      `docs/research/heartbeat-fireball-2002/` research library
      (min 19 files) + Brain wiki cards + brief. Parallel in structure
      to `docs/research/staples-l2/` and `docs/research/tesco-tom/`."*
- [ ] Note the GRO-### and reference in every commit.
- [ ] Create folder: `mkdir -p docs/research/heartbeat-fireball-2002`
- [ ] Seed `INDEX.md` with the expected-files table from Goal
      section above. Checkboxes for each. This becomes the progress
      tracker.

---

## Phase 1 — Extract + ingest everything

Legacy `.ppt`, `.doc`, `.xls` + `.vsd` extraction. Use the pipeline
built for the 2026-04-23 synthesis pass.

- [ ] Verify tooling: `which soffice`, `python3
      content-engine/engine.py --help`
- [ ] Run markitdown first: `python3 content-engine/engine.py extract
      Brain/raw/inbox/Heartbeat --target /tmp/scratch-heartbeat
      --execute`. Expect many legacy-`.ppt` failures.
- [ ] Run LibreOffice fallback for failed `.ppt`:
      `find Brain/raw/inbox/Heartbeat -iname "*.ppt" -not -iname
      "*.pptx" -type f -print0 | xargs -0 -I{} soffice --headless
      --convert-to pptx --outdir /tmp/converted-pptx "{}"`
- [ ] Re-run markitdown extract against `/tmp/converted-pptx/`.
- [ ] `.vsd` files: `find Brain/raw/inbox/Heartbeat -iname "*.vsd"
      -type f -print0 | xargs -0 -I{} soffice --headless
      --convert-to pdf --outdir /tmp/converted-vsd "{}"`. Then
      markitdown the PDFs.
- [ ] `.htm` files — markitdown handles them directly, or use
      `html2text`. Batch-convert MS Overview directory as a priority;
      defer WebFiles and RBK directories.
- [ ] For each successfully-extracted artifact, either:
      - Ingest it into `Brain/raw/inbox/<slug>.md` (same pattern as
        the 2026-04-23 pass), OR
      - If low-signal (scaffolding, redundant with a primary source),
        skip with a note in the skipped-artifact tracker.
- [ ] Record failures: expect some `.vsd` (image-only diagrams),
      some very old `.doc` files with broken encoding, possibly the
      Biztalk DLL binaries. Note which content survives the
      extraction gauntlet.
- [ ] Rebuild registry: `python3 content-engine/engine.py registry
      build`.
- [ ] Lint inbox: `python3 content-engine/engine.py lint --all`.

### Expected intake count

~60–100 new intakes after filtering. The ~108 RBK htm files collapse
into a single RBK_REFERENCE card; the 45 jpg + 66 gif files collapse
into the referencing docs; the Java class files get skipped. High
signal-to-noise once filtering is applied.

---

## Phase 2 — Write the research breakdown files

This is the work. Produce the 19 research files listed in the Goal
section, in this order.

### Batch 1 — Product narrative (read before writing anything)

1. `VISION_SCOPE.md` — mine `MS Overview/Background.htm` + `Fireball
   Vision Scope.doc` + `Functional Overview.htm`. Answer: what was
   Heartbeat trying to be? What problem, what scope, what non-scope?
2. `TIMELINE.md` — scan every dated artifact. Build a chronological
   timeline from earliest to latest signal. The answer to *"what
   happened to Heartbeat"* lives somewhere in this timeline.

### Batch 2 — Architecture

3. `DATA_ARCHITECTURE.md` — `Approved Heartbeat Data Architecture.ppt`
   + `Trickle Feed Data flow.ppt` + `MS Overview/Solution
   Architecture.htm` + `MS Overview/Process Flows.htm`. The data flow
   from POS → BizTalk → Fireball database → notification output.
4. `NETWORK_ARCHITECTURE.md` — all Visio .vsd files + biztalk.jpg.
   Physical deployment topology. Where did the software run, how did
   it connect to the retailer's network.
5. `OOS_ALGORITHM.md` — `Algorithm.htm` + `Heartbeat OOS
   Architecture.ppt` + `A4R - Sample Process Flow.ppt`. The core
   out-of-stock detection method. This is the intellectual centre of
   the product.
6. `NOTIFICATION_DESIGN.md` — all 7 Notification Design files. The
   alerting subsystem. **Direct Canary Chirp analogue — write this
   with extra care.** Cover: trigger rules, delivery channels,
   storyboard / UX, subscription management.
7. `XML_SCHEMA_EVOLUTION.md` — the two XML schema documents. Diff
   them. Explain what changed between August and January and what
   that implies about product learning.

### Batch 3 — Ecosystem + GTM

8. `SERVICE_OFFERING.md` — everything in `Service Offering/`. The
   Phase-I pilot assessment is the most important single document in
   the archive after Vision Scope — it's the retrospective of whether
   the product actually worked.
9. `GTM_SALES_DECKS.md` — sales deck v1/v3/v4 + POV 4 Box +
   Retail POV RCU + PWCNov decks + Kleinberger Jan 31. Evolution of
   the sales narrative. Pricing signals.
10. `PWC_MS_INTEL_ALLIANCE.md` — `PwC_MS_Intel_IVM.vsd`. What each
    party brought. How the alliance monetized.
11. `CVCS_DIAGNOSTIC.md` — unpack all 8 zips. Summarize what CVCS
    (Collaborative Value Chain Solutions) was as a PwC methodology
    and how it fed Heartbeat sales.

### Batch 4 — Clients

12. `CLIENT_MARKS_SPENCER.md` — M&S Architecture deck + any M&S-named
    notification docs. M&S is the flagship reference client.
13. `CLIENT_AMERICAN_EAGLE.md` — AE proposal PDF. Pre-contract,
    pursuit phase. What did the AE pitch look like.
14. `CLIENT_COLUMBUS.md` — Columbus17Dec + 2026-04-02 heartbeat
    project status. Program-level status. Who was Columbus — code
    name or Columbus, Ohio retailer?

### Batch 5 — Supporting references

15. `RBK_REFERENCE.md` — short. Index Microsoft's Retail BizTalk
    Resource Kit. Explain its role as the foundation layer. Link out
    to the source directory. Do not deep-read.
16. `CODE_ARTIFACTS.md` — short. What existed in
    `Program Files/Biztalk DLLs/`. What we can infer (not read — the
    binaries are opaque).

### Batch 6 — Synthesis (write these last)

17. `OPEN_QUESTIONS.md` — what the archive does not tell us. Candidate
    questions:
    - What happened to Heartbeat as a product?
    - Did Marks & Spencer go to production?
    - Did American Eagle sign?
    - When did the PwC-MS-Intel alliance wind down?
    - Is the Canary-internal Heartbeat naming coincidence or homage?
    - Is "Fireball" specifically what got productized, with Heartbeat
      as the parent product line, or is the terminology interchangeable?
    - Who were the other named clients beyond M&S / AE / Columbus?
18. `CANARY_LINEAGE_MAP.md` — **the synthesis deliverable.** Table per
    Heartbeat component mapped to Canary component with classification
    (1:1 / transformed / net-new) and commentary. Parallel to
    `docs/research/ibm-retail-bi/CANARY_LINEAGE_MAP.md`. This is the
    file that gets referenced in the wiki cards and the brief.
19. `INDEX.md` — finalize. TOC for the 19 files. Reading order for a
    newcomer. Headline findings. Link to wiki cards + brief.

### Tone + form guidance (from memory + prior research folder precedent)

- **Direct, serious, tangible.** No hype. No AI-sounding copy.
  Describe what the artifact says. Name what the artifact leaves
  unsaid.
- **Every research file cites its sources.** At top or bottom, list
  the specific intakes / binaries that fed the document.
- **Mark open questions explicitly.** Use `> **Open:**` call-outs.
  Carry them to `OPEN_QUESTIONS.md`.
- **No volatile data in research.** If the archive contains client
  pricing, projected revenue, contract values — paraphrase, don't
  transcribe. M&S and American Eagle are real companies with real
  legal surfaces.
- **Match the Staples L2 depth.** Look at
  `docs/research/staples-l2/INDEX.md` + `CANARY_PROCESS_MAP.md` as
  the quality bar. Not a summary. A research library.

---

## Phase 3 — Brain wiki cards

Only after Phase 2's CANARY_LINEAGE_MAP is complete.

- [ ] `Brain/wiki/secure-heartbeat-fireball-2002.md` — top-level
      product card. Frontmatter tags `[secure, heartbeat, fireball,
      pwc, microsoft, intel, biztalk, retail-oos, 2002, canary-lineage]`.
      Parallel structure to `secure-platform-overview.md`. Cites the
      research folder as authoritative source; card is the 10-minute
      read version.
- [ ] `Brain/wiki/secure-heartbeat-fireball-blueprint.md` —
      Canary-positioning card. Derived from CANARY_LINEAGE_MAP.
      Structure:
      - `## The Thesis` — if you rebuilt Heartbeat for today's SMB,
        you'd build Canary
      - `## Architecture Parallel` — distilled from
        CANARY_LINEAGE_MAP + DATA_ARCHITECTURE
      - `## GTM Parallel` — distilled from GTM_SALES_DECKS +
        PWC_MS_INTEL_ALLIANCE
      - `## What Canary Owes Heartbeat` — specific design choices to
        credit
      - `## What Canary Does That Heartbeat Could Not` — infra deltas
      - `## What Heartbeat Did That Canary Should Not` — anti-patterns
      - `## What Happened to Heartbeat` — findings
      - `## Open Questions`
      - `## Related` + `## Sources`
- [ ] Update `Brain/wiki/secure-retail-career-archive.md` — convert
      the "Heartbeat — Secure adjacent" stub into a link to
      `secure-heartbeat-fireball-2002`.

---

## Phase 4 — Brief

- [ ] `docs/briefs/2026-04-heartbeat-fireball-blueprint.md`
- [ ] Length 1000–1500 words. 2–3 pages.
- [ ] Audience: co-founder / investor / advisor / future-Jeffe.
- [ ] Structure:
      - The problem Heartbeat solved (one paragraph)
      - Why nobody else has been solving it for SMBs (infrastructure
        gap)
      - The 23-year-later thesis — Canary rebuilds Heartbeat for every
        merchant
      - Three design decisions Heartbeat got right that Canary
        inherited
      - Three design decisions Canary had to invert
      - What this means for Canary positioning, specifically for the
        *"why is this different from enterprise LP vendors"* question
- [ ] Companion to
      `docs/superpowers/briefs/2026-04-secure-to-canary-handoff.md`.

---

## Phase 5 — MOC updates + registry rebuild + commits

- [ ] `Brain/projects/Secure.md` — add new wiki cards under "Prior-Art
      Blueprints" section (new section if needed). Add research folder
      reference.
- [ ] `Brain/projects/Canary.md` — link the blueprint card as
      canonical historical reference. If Phase 6 resolves the naming
      question, record decision near the Heartbeat-module reference.
- [ ] Lint: `python3 content-engine/engine.py lint
      Brain/wiki/secure-heartbeat-*.md`
- [ ] Registry: `python3 content-engine/engine.py registry build`
- [ ] Commit chain (per 2026-04-23 precedent):
      1. `research(heartbeat-fireball): Phase 1 — extract + ingest 417-file archive [GRO-###]`
      2. `research(heartbeat-fireball): Phase 2 — 19-file research breakdown [GRO-###]`
      3. `brain(secure): heartbeat / fireball 2002 wiki cards [GRO-###]`
      4. `docs: heartbeat / fireball → canary blueprint brief [GRO-###]`
      5. `brain: rebuild registry post heartbeat deep-dive`
- [ ] Close the Linear issue with links to research folder + wiki
      cards + brief.

---

## Phase 6 — Resolve open questions with Jeffe

Before the deep-dive is truly complete:

- [ ] **Canary Heartbeat lineage — characterize the relationship.**
      Jeffe has confirmed the two Heartbeats are related. Pin down
      the form: direct homage, conceptual lineage (same metaphor
      carried forward), or architectural lineage (TSP descended from
      Heartbeat/Fireball's trickle-feed-to-subscribers pattern).
      Record the answer in `Brain/projects/Canary.md` near the
      Heartbeat module reference, and make the blueprint card the
      canonical origin-story reference. **This is now a Canary
      Brand Story surface — protect it.**
- [ ] **What happened to Heartbeat?** Jeffe's own recollection may
      resolve this faster than archive archaeology. Document answer
      in `OPEN_QUESTIONS.md` and `CLIENT_*` files.
- [ ] **Columbus identification.** Codename or city? Resolve.
- [ ] **Fireball vs Heartbeat nomenclature.** Same product, different
      marketing layer, or two products in the same family? Resolve.

---

## Pitfalls to avoid (learned from 2026-04-23 synthesis)

1. **Don't skip the RBK filter.** 108 Microsoft htm files will swallow
   the session if read in depth. Index them. Move on.
2. **Don't over-consolidate.** Each of the 19 research files has a
   specific job. Keep them distinct even when topics overlap — cross-
   reference rather than merge.
3. **Don't reproduce client-specific PII.** M&S, American Eagle, and
   whoever Columbus was are real organizations with real legal
   surfaces. Paraphrase contract specifics, contact names, pricing.
4. **Don't hype-credit Heartbeat.** Heartbeat was a product with
   specific scope and specific limitations. Name them honestly.
   Blueprint value lives in parallels, not reverence.
5. **Don't let Phase 1 eat the session.** Extraction is mechanical.
   Protect time for Phase 2 writing — that's where the research
   value sits.
6. **Don't let Visio diagrams become a black hole.** LibreOffice can
   convert `.vsd` to PDF but the result is often low-fidelity. If
   the diagram doesn't extract cleanly, screenshot it + transcribe
   the key components into the relevant research file. Don't spend
   hours trying to get a pristine conversion.
7. **Don't forget Phase 6.** The Canary naming question is the
   reason this playbook is Canary-defining, not just archival.
8. **Don't skip the Phase-I Pilot Assessment doc.** It's the single
   most important document for "did the product actually work" and
   deserves its own deep read, not just a summary paragraph.

---

## When complete

Summary report (for commit body + user chat):

- Intakes processed / skipped / failed: __ / __ / __
- Research files produced: __ / 19 expected
- Wiki cards produced: __ / 2 expected
- Brief produced: yes / no
- Linear issue: GRO-___
- Canary Heartbeat naming resolved: yes / no (decision: _____)
- "What happened to Heartbeat" resolved: yes / no (answer: _____)
- Top 3 surprises from the archive: _____
- Open items: _____

---

## References

- [[docs/research/staples-l2/INDEX.md|Staples L2 precedent]] — the
  quality bar for this playbook
- [[docs/research/tesco-tom/INDEX.md|Tesco TOM precedent]]
- [[docs/research/ibm-retail-bi/INDEX.md|IBM Retail BI precedent]]
- [[Brain/projects/Secure|Secure MOC]] — where the output wiki cards land
- [[Brain/projects/Canary|Canary MOC]] — where the blueprint card lands
- [[Brain/wiki/secure-platform-overview|Secure Platform Overview]] —
  structural parallel for the top-level Heartbeat card
- [[Brain/wiki/growdirect-data-strategy|Data Strategy NorthStar]] —
  Canary Heartbeat Network concept (the DIFFERENT Heartbeat, V.5.6)
- [[CLAUDE.md|Platform CLAUDE.md]] — Intake Protocol + Rule Zero
- `docs/superpowers/briefs/2026-04-secure-to-canary-handoff.md` —
  companion brief template
