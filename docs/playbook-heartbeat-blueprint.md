# Heartbeat / Fireball (2002) — Essential Design Extraction Playbook

Extract the **working solution** from the 417-file
`Brain/raw/inbox/Heartbeat/` archive: a 2001–2003 retail out-of-stock
detection + notification system built on Microsoft BizTalk, implemented
at multiple enterprise retailers. Strip out the noise (sales decks,
alliance paperwork, pricing, client specifics, marketing versions) and
surface the essential design as direct prior art for Canary.

Output is a tight research folder (6–7 files), not an archival library.
Every file earns its place by mapping a 2002 design decision to a
Canary design choice. Everything client-specific or commercial is
scrubbed.

---

## Naming disambiguation — read first

**Two "Heartbeats" in this project. Jeffe has confirmed they are
related.** The playbook treats them as distinct-but-connected:

1. **Heartbeat / Fireball (2002)** — the enterprise retail OOS +
   notification product in this folder, built on Microsoft BizTalk.
   **This playbook is about this one.**
2. **Canary Heartbeat Network (2026)** — Manifesto V.5.6 / Data
   Strategy NorthStar: IoT device timestamp anchoring to a Bitcoin-
   derived heartbeat. Referenced in
   [[Brain/wiki/growdirect-data-strategy|Data Strategy NorthStar]]
   and `canary/services/tsp/heartbeat.py`.

The relationship — direct homage, conceptual lineage, or architectural
DNA — is a Phase 5 deliverable. Every research file uses
**"Heartbeat / Fireball (2002)"** in titles to keep the documents
unambiguous while the thread runs between them.

---

## Rule: scrub client names

Per `feedback_scrub_client_names.md`. All output abstracts named
retail clients into **NFR deployment archetypes** (scale / vertical /
geography / regulatory surface). Raw intakes at
`Brain/raw/inbox/Heartbeat/` stay intact as source of record. The
research folder and downstream wiki/brief never name the retailer.

Rewrite table for known clients surfaced in the archive:

| Archive reference | Archetype |
|---|---|
| UK multi-format retail flagship | "UK multi-format grocery + general-merchandise chain, ~800 stores" |
| US specialty apparel retailer | "US specialty apparel retailer, mall-anchor footprint" |
| Midwestern client (by codename) | "US regional chain, mid-market scale" |

If the archive surfaces additional clients not in this table, add new
archetypes rather than naming them.

---

## Rule: extract the working solution, not the noise

Per `feedback_extract_working_solution.md`. Focus on **how the system
worked**. Skip how it was sold, priced, partnered, or positioned.

| Signal (extract) | Noise (skip or index only) |
|---|---|
| Data architecture + pipeline design | Sales decks (v1, v3, v4) |
| OOS detection algorithm | PwC + MS + Intel alliance structure |
| Notification subsystem design | Marketing update decks |
| Event XML schema (and its evolution) | CVCS diagnostic methodology |
| Phase-I Pilot Assessment (retrospective) | Go-to-Market pricing estimates |
| Vision / Scope document | Partnership Integrated Value Maps |
| Network topology diagrams | Client-specific proposal PDFs |
| BizTalk AIC integration pattern | Service Offering phase plans (commercial framing) |
| Process Flows + Functional Overview | Retail POV / industry-positioning decks |

The Phase-I Pilot Assessment is the one commercial-flavored doc worth
deep-reading — it's the honest retrospective of whether the design
actually worked. Extract the technical signal, drop the commercial
framing.

---

## Goal

Produce a **tight essential-design research folder** at
`docs/research/heartbeat-fireball-2002/` containing **6 files**:

| # | File | What it answers | Source material (signal only) |
|---|---|---|---|
| 1 | `INDEX.md` | What this folder is, reading order, what got scrubbed as noise | — (curated) |
| 2 | `THE_PROBLEM.md` | What NFR profile the system solved for (scale / vertical / data volumes / latency / regulatory) | `MS Overview/Background.htm`, `MS Overview/Functional Overview.htm`, `Fireball Vision Scope.doc` |
| 3 | `THE_ARCHITECTURE.md` | End-to-end working data pipeline: ingest → process → store → notify | `Approved Heartbeat Data Architecture.ppt`, `Trickle Feed Data flow.ppt`, `MS Overview/Solution Architecture.htm`, `MS Overview/Process Flows.htm`, `BTS AIC Architecture.vsd`, `Fireball Network Architecture.vsd`, `Heartbeat OOS Architecture.ppt` |
| 4 | `THE_ALGORITHM.md` | Core out-of-stock detection method — the intellectual centre of the product | `MS Overview/Algorithm.htm`, `A4R - Sample Process Flow.ppt`, `a4r scenario.vsd` |
| 5 | `THE_NOTIFICATION_SYSTEM.md` | Alerting subsystem — **direct Canary Chirp analogue**. Trigger rules, delivery channels, storyboard/UX, subscription management, XML event schema + its evolution | All 7 Notification Design docs (Spec, System Specification1221, Subsystem Documentation, Customer Aug 6, Storyboard, XML schema Aug + Jan versions) |
| 6 | `CANARY_LINEAGE_MAP.md` | **Synthesis.** Per-component mapping of the 2002 design to Canary's current architecture (1:1 / transformed / net-new). Plus the honest retrospective of what worked and what didn't, from the Phase-I Pilot Assessment, abstracted to NFR-profile outcomes | All of the above + `Service Offering/Phase-I Pilot Assessment.doc` (technical signal only) |

Optional 7th file if it earns its place:

- `THE_RUNTIME_CODE.md` — what survives in `Program Files/Biztalk DLLs/`
  (NotificationSubscriptions.BAK, SortFile1.xsl, SortFile2.xsl). Only
  if one of those XSL files reveals a non-obvious design decision not
  captured in the spec docs. Skip if the code just confirms what the
  specs already say.

### What is explicitly NOT in the output

- Per-client deployment files — no `CLIENT_*` anything. The pilot
  retrospective's findings get abstracted into `CANARY_LINEAGE_MAP`.
- GTM / sales / pricing / alliance files — noise.
- CVCS Diagnostic folder — methodology, not the product. Skip.
- RBK (Microsoft Retail BizTalk Resource Kit) — Microsoft's IP, not
  the working solution. Mention in one line of `THE_ARCHITECTURE.md`
  as the foundation, link out, move on.

---

## Downstream deliverables (after the research folder is complete)

- **1 Brain wiki card** — `Brain/wiki/secure-heartbeat-fireball-2002.md`.
  The 5-minute-read version of the research folder. Headlines the
  essential design + the Canary-parallel finding. References the
  research folder as authoritative. Uses archetypes, not client names.
- **1 brief** (optional) — `docs/briefs/2026-04-heartbeat-fireball-blueprint.md`.
  1–2 pages. Audience: co-founder / investor. Answers the
  *"why is this different from enterprise LP vendors"* question
  grounded in the 2002 prior art. Skip if the wiki card alone carries
  the message.

Total output: **6 research files + 1 wiki card** (plus 1 optional
brief). Down from the archival-style 19 files of a Staples L2-scale
sweep — because we're extracting design signal, not cataloguing an
engagement.

---

## Phase 0 — Linear parent + folder scaffold

- [ ] Create Linear issue: *"Heartbeat / Fireball 2002 — essential
      design extraction from Brain/raw/inbox/Heartbeat/"*. Growdirect
      team, Canary project. Priority Medium. Label Strategy &
      Research.
- [ ] Description: *"6-file research extraction per
      `docs/playbook-heartbeat-blueprint.md`. Target:
      `docs/research/heartbeat-fireball-2002/` (INDEX, THE_PROBLEM,
      THE_ARCHITECTURE, THE_ALGORITHM, THE_NOTIFICATION_SYSTEM,
      CANARY_LINEAGE_MAP) + 1 Brain wiki card. Client names scrubbed,
      GTM/alliance/marketing material skipped per
      feedback_scrub_client_names.md + feedback_extract_working_solution.md."*
- [ ] `mkdir -p docs/research/heartbeat-fireball-2002`
- [ ] Seed `INDEX.md` with the 6-file table. Checkboxes per file.
      Becomes the progress tracker.

---

## Phase 1 — Focused extraction (signal-only)

Do NOT run a full 417-file extract. Extract only the signal files.

### Files to extract (and no others)

Core architecture + product narrative:

```
Brain/raw/inbox/Heartbeat/MS Overview/Background.htm
Brain/raw/inbox/Heartbeat/MS Overview/Functional Overview.htm
Brain/raw/inbox/Heartbeat/MS Overview/Fireball Vision Scope.doc
Brain/raw/inbox/Heartbeat/MS Overview/Algorithm.htm
Brain/raw/inbox/Heartbeat/MS Overview/Solution Architecture.htm
Brain/raw/inbox/Heartbeat/MS Overview/Process Flows.htm
Brain/raw/inbox/Heartbeat/Approved Heartbeat Data Architecture.ppt
Brain/raw/inbox/Heartbeat/Trickle Feed Data flow.ppt
Brain/raw/inbox/Heartbeat/Fireball Documentation/Fireball Documentation/Heartbeat/Heartbeat OOS Architecture.ppt
Brain/raw/inbox/Heartbeat/A4R - Sample Process Flow.ppt
```

Visio network / architecture diagrams:

```
Brain/raw/inbox/Heartbeat/Fireball Documentation/Fireball Documentation/Fireball Network Architecture.vsd
Brain/raw/inbox/Heartbeat/Fireball Documentation/Fireball Documentation/BTS AIC Architecture.vsd
Brain/raw/inbox/Heartbeat/Fireball Documentation/Fireball Documentation/Fireball Implementation.vsd
Brain/raw/inbox/Heartbeat/a4r scenario.vsd
```

Notification subsystem (all of it — this is the Chirp analogue):

```
Brain/raw/inbox/Heartbeat/Fireball Documentation/Fireball Documentation/Notification Design/*.doc
Brain/raw/inbox/Heartbeat/Fireball Documentation/Fireball Documentation/Notification Design/Fireball_Notification _StoryBoard.ppt
```

Retrospective (for CANARY_LINEAGE_MAP Phase 3):

```
Brain/raw/inbox/Heartbeat/Service Offering/Phase-I Pilot Assessment.doc
```

That's ~18 source files out of 417. Do not extract the rest.

### Extraction pipeline

Per the 2026-04-23 pattern:

- [ ] Verify tooling: `which soffice` + `python3
      content-engine/engine.py --help`.
- [ ] Legacy `.ppt` conversion: run `soffice --headless --convert-to
      pptx --outdir /tmp/converted-pptx <each-ppt-file>`.
- [ ] `.vsd` conversion: `soffice --headless --convert-to pdf
      --outdir /tmp/converted-vsd <each-vsd-file>`. Expect low-fidelity
      text — may need manual inspection + transcription of key
      components into the research file rather than clean extraction.
- [ ] `.htm` files: markitdown handles directly, or `html2text`.
- [ ] `.doc` files: markitdown.
- [ ] Ingest each via `engine.py ingest` into `Brain/raw/inbox/<slug>.md`.
- [ ] Expect 15–18 new intakes (each source → one intake). Not 60+
      like a full-folder sweep would produce.

### What to do if a source won't extract

Two of the Visio `.vsd` files may resist clean conversion to PDF (the
Network Architecture diagram especially). Fallback: open the `.vsd`
in LibreOffice Draw visually, screenshot the key components, and
transcribe the topology directly into `THE_ARCHITECTURE.md`. Text
description beats a low-fidelity auto-extract for an architecture
diagram.

---

## Phase 2 — Write the 6 research files

Order matters. Write in the sequence below.

### 1. `THE_PROBLEM.md` — first, so the rest has a frame

Read: Background, Vision Scope, Functional Overview.

Answer:

- What was the problem the system solved for? (strip the marketing
  layer — get to the technical statement)
- What was the target deployment archetype? (scale, vertical,
  geography, regulatory surface — NOT named clients)
- What were the non-functional requirements? (latency, data volume,
  reliability, operator skill level, integration surface with the
  retailer's existing stack)
- What was explicitly out of scope for the product?

Length guide: ~1–2 pages. Short.

### 2. `THE_ARCHITECTURE.md` — the working pipeline

Read: Approved Data Architecture, Trickle Feed, Solution Architecture,
Process Flows, BTS AIC Architecture, Network Architecture, OOS
Architecture.

Answer:

- How did data get into the system? (trickle feed from the retailer's
  POS / operational systems — what format, what frequency, what
  failure modes)
- How did it get processed? (BizTalk AIC layer — what the Application
  Integration Components did, how they composed)
- How did it get stored? (what datastore, what schema shape, what
  retention)
- How did output get delivered? (to the notification subsystem, not
  the details of the subsystem itself — those go in #5)

One-line reference to the Retail BizTalk Resource Kit as the
Microsoft platform the product was built on. No deep dive.

**Map to Canary as you go.** Every major component gets a "Canary
analogue" footnote or inline note. Don't write a separate Canary
section per paragraph — just cross-reference inline so the lineage
map in file #6 writes itself.

Length guide: ~3–5 pages. The thickest file in the folder.

### 3. `THE_ALGORITHM.md` — the intellectual centre

Read: Algorithm.htm, A4R Sample Process Flow, a4r scenario.vsd.

Answer:

- What was the out-of-stock detection method in plain technical prose?
  (rule-based? threshold? statistical? Bayesian? something stranger?)
- What inputs did it operate on? (POS events only? inventory feeds?
  both?)
- What false-positive / false-negative control was there?
- How did it distinguish "out of stock" from "out for restocking" or
  "reduced range"?
- What tunability did operators have?

If the algorithm isn't fully described in the available artifacts
(possible — it may have been trade secret even internally), document
what IS known and flag the gap explicitly.

Canary analogue: the Chirp detection rule engine + the Bayesian /
KAP scoring layer. Compare directly.

Length guide: ~1–2 pages. Shorter than architecture, but dense.

### 4. `THE_NOTIFICATION_SYSTEM.md` — the Chirp ancestor

Read: all 7 Notification Design docs.

This is the **single most Canary-parallel artifact in the archive.**
Give it room.

Answer:

- Trigger rules — what events caused a notification to fire?
- Subscription model — who subscribed to what, and how was that
  managed?
- Delivery channels — email, pager, web dashboard, other? How did
  the 2002 product assume its notifications would reach a human?
- Event schema evolution — what changed between the August and
  January XML schema versions, and what does that change say about
  product learning?
- Storyboard / UX — what did the alert look like on the receiving
  end? Plain language? Dashboard chart? Something else?
- Failure modes — what happened if the notification couldn't be
  delivered? Retry? Queue? Drop?

Canary analogue: Chirp module end-to-end. Compare every dimension.

Length guide: ~3–4 pages. Second-thickest file.

### 5. `THE_SCHEMA.md` — embedded in #4 or standalone?

**Decision point.** If the XML schema evolution is substantive enough
that it warrants its own file, split it out. Otherwise keep it inside
`THE_NOTIFICATION_SYSTEM.md`.

Criteria for splitting: if the schema has >30 fields, or if the
Aug→Jan delta reveals multiple categories of learning (new signals
added, field semantics changed, cardinality changes), split. If it's
a narrower evolution, keep inline.

Recommend: start inline in #4. Split only if the inline treatment
bloats that file past ~5 pages.

### 6. `CANARY_LINEAGE_MAP.md` — the payoff

Structure:

```
## Component map

| 2002 Heartbeat/Fireball | Canary (2026) | Match | Notes |
|---|---|---|---|
| Trickle feed from POS | TSP webhook ingest | Transformed | Push/webhook vs pull/batch. Same role, different generation. |
| BizTalk AIC layer | Flask ingestion + Sub 1/2/3 workers | Transformed | Same integration + routing function, commodity stack instead of enterprise platform. |
| OOS detection algorithm | Chirp detection rules (27+) + Bayesian / KAP scoring | Transformed | Single flagship algo → multi-rule engine with statistical scoring. Canary broadens the detection surface. |
| Notification Subsystem | Chirp module | 1:1 conceptually | Same job, plain-language alerts to a business operator. Delivery-channel set has modernised but the core design choice is identical. |
| XML event schema | JSON webhook payloads + CRDM normalised rows | Transformed | XML → JSON, enterprise-schema → commodity/mobile-friendly. |
| Professional-services deployment | OAuth self-service onboarding | Net-new | The biggest single delta. 2002's sale required consulting; 2026's doesn't. |
| (no equivalent) | Bitcoin Ordinal evidence chain | Net-new | Canary's sovereignty moat has no 2002 analogue. |
| (no equivalent) | Lightning micro-payment plumbing | Net-new | Also no analogue. |

## What the 2002 design got right

- [list 3–5 specific design decisions, each with a one-sentence
  justification]

## What the 2002 design got wrong (or was right-for-2002-wrong-for-2026)

- [list 3–5 specific design decisions, each with a one-sentence
  justification]

## What the Phase-I Pilot Assessment revealed (abstracted)

- [technical retrospective findings from the pilot — whether the
  algorithm actually caught the exceptions it needed to catch,
  whether the notifications reached the operator, whether the
  integration held under production load. **Abstracted to the NFR
  profile, not named at the client.** E.g., "in the mid-market UK
  deployment archetype, the trickle-feed integration held but the
  notification-delivery rate fell below target in X% of cases due
  to Y."]

## What Canary inherits (knowingly or not)

- [the specific design decisions Canary made that the 2002 design
  had already validated]

## What is genuinely new in Canary

- [the design decisions with no 2002 precedent — infrastructure-
  enabled and thesis-driven]

## Open questions

- [anything the archive leaves unresolved — the relationship between
  the two Heartbeat concepts being the biggest]
```

Length guide: ~3–4 pages. Dense. This is the document that gets
cited downstream.

---

## Phase 3 — Brain wiki card

Only after the research folder is complete.

- [ ] `Brain/wiki/secure-heartbeat-fireball-2002.md`
- [ ] Frontmatter tags: `[secure, heartbeat, fireball, prior-art,
      canary-lineage, biztalk, retail-oos, essential-design, 2002]`
- [ ] **No client-name tags.** No `[lululemon]`, `[marks-spencer]`,
      etc.
- [ ] Length: 5-minute read. Headlines the essential design + the
      Canary-parallel finding. References the research folder as the
      deep source.
- [ ] Structure:
      - `## Summary` — one paragraph on what it was + why it matters
      - `## The Essential Design` — distilled from research folder
        files 2–5 (one paragraph per: problem / architecture /
        algorithm / notification system)
      - `## Canary Lineage` — distilled from research file 6
      - `## Why This Matters for Canary Today` — the brand-story
        hook, if Phase 5 resolves the naming relationship
      - `## Related` — link to the research folder, Secure MOC,
        Canary MOC, TSP pipeline wiki, Chirp module
      - `## Sources` — link to the 6 research files (not the raw
        intakes — the research folder is the authoritative layer)
- [ ] Update `Brain/wiki/secure-retail-career-archive.md` — convert
      the "Heartbeat — Secure adjacent" stub into a link to the new
      card. Scrub any named retailers while you're there if the
      archive already has them in the stub.

---

## Phase 4 — Brief (optional)

Skip unless the wiki card alone can't carry the co-founder / investor
message.

If you write it:

- Path: `docs/briefs/2026-04-heartbeat-fireball-blueprint.md`
- Length: 1–2 pages
- Anchor on: *"a Fortune 500 software stack from 2002, reshipped as a
  self-service SaaS for every SMB in 2026, is the positioning. Here's
  the prior art."*
- No named clients. Archetype language only.

---

## Phase 5 — Resolve the naming relationship with Jeffe

Jeffe has confirmed the two Heartbeats are related. Pin down the
form:

- **Direct homage** — Jeffe named the Canary module deliberately after
  the 2002 product concept
- **Conceptual lineage** — the "periodic signal of liveness from a
  system to subscribers" metaphor is the same thing; Canary's
  Bitcoin-anchor evolution is the next-generation take
- **Architectural lineage** — the trickle-feed-to-subscribers pattern
  from 2002 is the direct ancestor of Canary's TSP (Triple Subscriber
  Pipeline), and the Heartbeat naming reflects that architectural DNA

Action:

- [ ] Ask Jeffe directly — ideally in the session where the research
      folder is being reviewed for final sign-off.
- [ ] Record the answer in:
      - `CANARY_LINEAGE_MAP.md` under "Open questions → resolved"
      - The Brain wiki card's "Why This Matters for Canary Today"
        section
      - `Brain/projects/Canary.md` near the Heartbeat module reference
- [ ] If the answer is genuinely "all three simultaneously," say so —
      it may well be.

---

## Phase 6 — MOC update + registry rebuild + commits

- [ ] `Brain/projects/Secure.md` — add the new wiki card under "Prior-
      Art Blueprints" (new subsection if needed). Link the research
      folder.
- [ ] `Brain/projects/Canary.md` — link the blueprint card. Record
      Phase 5 decision here.
- [ ] Lint: `python3 content-engine/engine.py lint
      Brain/wiki/secure-heartbeat-*.md`
- [ ] Registry: `python3 content-engine/engine.py registry build`
- [ ] Commit chain:
      1. `research(heartbeat-fireball): essential design extraction [GRO-###]`
      2. `brain(secure): heartbeat / fireball 2002 wiki card [GRO-###]`
      3. `brain: rebuild registry post heartbeat extraction`
      4. (optional) `docs: heartbeat / fireball blueprint brief [GRO-###]`
- [ ] Close Linear issue with links to the 6 research files + wiki
      card.

---

## Pitfalls to avoid

1. **Don't extract the 400 files you don't need.** The signal list is
   ~18 source files. Everything else is noise. Resist the urge to
   completeness.
2. **Don't write client-specific files.** No `CLIENT_*.md`. The pilot
   retrospective's findings get abstracted into NFR-profile language
   in `CANARY_LINEAGE_MAP.md`.
3. **Don't write GTM files.** No sales deck analysis, no alliance
   structure file, no pricing breakdown, no partnership paperwork.
   This is an engineering exercise.
4. **Don't reproduce named clients in wiki.** Scrub in
   synthesis. Raw intakes stay intact.
5. **Don't hype-credit the 2002 design.** Name what it got right,
   name what it got wrong. Reverence is noise.
6. **Don't let Phase 1 eat the session.** 18 targeted extractions
   should take an hour. If it's eating the day, you're extracting the
   wrong files.
7. **Don't skip Phase 5.** The naming relationship is what turns this
   from archival exercise into origin-story surface.
8. **Don't let Visio diagrams become a black hole.** If `.vsd` won't
   convert cleanly, screenshot + transcribe. A text description of
   the topology is better than a low-fidelity auto-extract.

---

## When complete

Summary report (for commit body + user chat):

- Signal files extracted: __ / ~18 expected
- Research files produced: __ / 6 expected (+ 0 or 1 optional schema
  split + 0 or 1 optional runtime-code file)
- Wiki card produced: yes / no
- Brief produced: yes / no
- Linear issue: GRO-___
- Phase 5 naming relationship resolved: yes / no (decision: _____)
- Client names scrubbed: yes / spot-check result
- Pilot assessment key finding (abstracted): _____
- Open items: _____

---

## References

- [[docs/research/staples-l2/INDEX.md|Staples L2 precedent]] (different
  shape — full archival — but same research quality bar)
- [[docs/research/tesco-tom/INDEX.md|Tesco TOM precedent]]
- [[docs/research/ibm-retail-bi/INDEX.md|IBM Retail BI precedent]]
- [[Brain/projects/Secure|Secure MOC]]
- [[Brain/projects/Canary|Canary MOC]]
- [[Brain/wiki/growdirect-data-strategy|Data Strategy NorthStar]] —
  Canary Heartbeat Network concept (the DIFFERENT Heartbeat, V.5.6)
- `feedback_scrub_client_names.md` — the client-name rule
- `feedback_extract_working_solution.md` — the signal-vs-noise rule
- [[CLAUDE.md|Platform CLAUDE.md]] — Intake Protocol + Rule Zero
