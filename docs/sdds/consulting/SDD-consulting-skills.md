---
type: sdd
status: draft-v1
domain: consulting
component: consulting-skills
author: Geoffrey C. Lyle
date: 2026-04-24
related:
  - Brain/wiki/methodology-ibm-retail-diagnostic.md
  - Brain/wiki/methodology-ibm-it-architecture-options.md
  - dispatches/2026-04-24-consulting-skills.md
  - plugins/consulting/plugin.json
  - plugins/consulting/skills/retail-diagnostic/SKILL.md
  - plugins/consulting/skills/it-architecture-options/SKILL.md
  - Brain/projects/Method.md
---

# SDD — Consulting Skills (IBM BCS Lineage)

## Purpose

Codify two consulting methodologies — **Retail Diagnostic** (Clarks pattern)
and **IT Architecture Options** (Morrisons pattern) — as executable Cowork
skills so GrowDirect can produce Big-4-grade retail consulting deliverables
by plugging client evidence into a known-good structural frame. These skills
are not content generators; they are **shape enforcers**. The analyst (human
or agent) still brings the evidence and the judgment; the skill enforces
that the evidence is presented in the seven-section, numbered-navigator
frame that makes the deliverable credible and defensible.

## Context

**Lineage.** Both methodologies originate from IBM Business Consulting
Services deliverables Geoffrey produced / reviewed in 2006. The original
.ppt files are preserved as source-of-truth reference material (see
`Brain/wiki/methodology-ibm-*.md`). The client-specific data in those files
is not part of the skill; only the structural methodology is codified.

**Why now.** Geoffrey's CIO positioning (see the Personal CIO Playbook)
asserts that the credential for a CIO / Chief AI Officer / Chief Product
role comes from *operating evidence* — building something real. These two
skills turn Geoffrey's methodological IP from the IBM era into operating
evidence for the GrowDirect era. Each skill is a demonstration that
Geoffrey can reproduce, at will, the kind of deliverable boards pay for,
and that he can do so inside a small-team / AI-assisted workflow.

**Scope boundary.** v1 produces the structural deck (pptx) and companion
docx write-up. It does not produce the client-engagement collateral
(statement of work, engagement letter, pricing schedule). Those are
separate skills for a later sprint if the consulting toolset develops
into a revenue line.

## Requirements

### Functional

**FR-1: Retail Diagnostic skill** — `consulting:retail-diagnostic` must
produce a 7-section deck (Executive Summary · Background/Scope/Approach ·
Financial Analysis & Industry Drivers · Theme 1 F&O · Theme 2 F&O ·
Opportunity Priorities & Roadmap · Prioritised Case for Action) in pptx
format with numbered navigator ribbon on every slide.

**FR-2: Per-theme drill pattern** — inside Theme 1 and Theme 2 sections,
the skill must enforce the four-element pattern (Overview → Prize →
Per-root-cause drills with Findings+Leading-Practice+three-callouts →
Recommendations with 5-axis implementation challenges).

**FR-3: Prize quantification** — every theme must end in a £ low/high
range table with method cite. Skill refuses to render "significant
opportunity" without numbers.

**FR-4: Two-axis heat-maps** — `consulting:it-architecture-options` must
render every option's architecture twice (org-structure axis, process
axis) using the 4-color legend (Very good / Good+small changes / Good+
significant changes / Poor or no support).

**FR-5: Symmetric option skeleton** — for every option evaluated, all
seven slides must be produced (title · opt-vs-optimisation-orgview ·
opt-vs-optimisation-procview · effort estimate · opt-vs-aspirational-orgview ·
opt-vs-aspirational-procview · advantages-disadvantages + target arch).

**FR-6: Side-by-side summary** — IT Architecture skill's final section
must render all options on aligned process-frame rows so the eye can
compare box-for-box.

**FR-7: Recommendation slide mapping** — IT Architecture skill's
recommendation must explicitly cite the Section 2 business targets
(margin / overhead / headcount / sales / profits) that motivated the
choice.

**FR-8: Evidence traceability** — every fact on every slide carries a
source footnote. Skill refuses to render a fact without one.

### Non-functional

**NFR-1: Invocation cost** — each skill must complete a synthetic
retailer engagement (small data pack, three themes max) in under 10
minutes of wall-clock time on a Cowork session.

**NFR-2: Output fidelity** — pptx output must open cleanly in both
PowerPoint and Keynote. No exotic fonts; system-safe only (Calibri,
Arial, Times New Roman).

**NFR-3: Source provenance** — skill outputs carry a footer citing the
IBM BCS 2006 methodology lineage, and the methodology's own wiki article
URL inside the vault.

**NFR-4: Reusable shared elements** — the Sell/Plan/Move/Buy process
taxonomy and the 4-color legend are shared between both skills and
factored to `consulting/_shared/` if any second client engagement proves
the pattern is stable.

## Design

### Plugin file layout

**Decision D-0 (new):** These skills ship as a plugin (`consulting`), not
as platform `.claude/skills/` entries. Rationale: parity with existing
namespaced plugins (`brand-voice:*`, `legal:*`, `marketing:*`,
`engineering:*`); clear IP boundary for potential productization; reuses
the `cowork-plugin-management:create-cowork-plugin` path for scaffolding.

```
plugins/consulting/
├── plugin.json                    (manifest — name, version, skills index, provenance)
├── README.md                      (plugin overview + links to methodology wikis)
├── commands/                      (future: slash-commands if needed)
└── skills/
    ├── _shared/
    │   ├── process-taxonomy-sell-plan-move-buy.md
    │   ├── heatmap-legend-4color.md
    │   └── navigator-ribbon-template.md
    ├── retail-diagnostic/
    │   ├── SKILL.md                    (trigger + workflow)
    │   ├── prompt.md                   (system prompt; Sprint 2)
    │   ├── templates/
    │   │   ├── deck-skeleton.pptx      (7-section master with navigator ribbon)
    │   │   ├── theme-drill-template.md (4-element pattern per theme)
    │   │   └── prize-table-template.xlsx
    │   └── examples/
    │       └── synthetic-retailer-evidence.json
    └── it-architecture-options/
        ├── SKILL.md
        ├── prompt.md                   (Sprint 2)
        ├── templates/
        │   ├── deck-skeleton.pptx      (8-section master)
        │   ├── option-skeleton.md      (7-slide per-option pattern)
        │   ├── effort-estimate-template.xlsx
        │   └── effort-estimate-factors.yml
        └── examples/
            └── synthetic-systems-inventory.json
```

### Invocation flow — `consulting:retail-diagnostic`

1. **Trigger** (SKILL.md description matches): "retail diagnostic",
   "financial baseline for retailer", "find the prize", "prioritized
   retailer roadmap".
2. **Input prompt** — skill asks for:
   - Client name and scope (which division, which geography)
   - Financial extract (xlsx) — sales, margin, stock, EBIT
   - POS / transaction extract (optional; enables margin analysis)
   - Systems inventory (optional; enables systems recommendations)
   - Workshop notes (text or md) — subjective themes from stakeholder
     interviews
   - Target themes (1–3) — typically Availability + Store Costs, but
     configurable (e.g. Margin + Range Complexity + Promotions).
3. **Section 1 — Executive Summary** — generated last, from sections
   2–7, by the skill's summariser.
4. **Section 2 — Background, Scope, Approach** — generated from input
   prompt answers + skill's templated language for approach phases.
5. **Section 3 — Financial Analysis** — generated from the financial
   extract. Skill refuses to proceed if the financial extract is not
   provided; Big-4 diagnostics require a financial baseline.
6. **Section 4–5 — Theme drill-downs** — for each target theme, skill
   runs the four-element pattern. Findings/Leading-Practice pairings
   sourced from the skill's benchmarking corpus (retail operations
   research, publicly available peer data).
7. **Section 6 — Priorities & Roadmap** — skill builds the Recommended
   Initiatives heat-map table (prize × cost × complexity) and renders
   the 2×2 prioritisation scatter.
8. **Section 7 — Case for Action** — three-phase roadmap aligned to
   client-provided milestones if available, else a generic "quick wins
   / build-the-system / end-state" phasing.
9. **Render** — pptx using the 7-section skeleton. Companion docx
   write-up for leave-behind reading.
10. **Output** — /outputs/<slug>-retail-diagnostic-v1.pptx +
    /outputs/<slug>-retail-diagnostic-v1.docx.

### Invocation flow — `consulting:it-architecture-options`

1. **Trigger**: "evaluate IT options", "legacy vs. package", "architecture
   options", "buy vs. enhance vs. replatform".
2. **Input prompt** asks for:
   - Client name
   - Systems inventory (csv or json) — mandatory
   - Business programme targets (margin / headcount / etc.) — mandatory
   - Optimisation requirements (near-term, 12–24 months)
   - Aspirational requirements (3–5 years)
   - Options to evaluate (default A/B/C = Legacy / BoB / Integrated;
     configurable)
3. **Section 1 — Introduction** — generated from input prompt.
4. **Section 2 — Programme targets** — generated verbatim from input.
5. **Section 3 — Sell/Plan/Move/Buy frame** — rendered from shared
   process taxonomy (swappable frame supported).
6. **Section 4 — Legacy implications** — heat-map generated from
   systems inventory.
7. **Section 5–7 — Options** — for each option, skill produces the
   7-slide skeleton. Effort estimate table populated from the systems
   inventory + skill's effort-factor heuristics (configurable).
8. **Section 8 — Summary & recommendation** — side-by-side architecture
   diagrams, implementation comparison, and recommendation slide mapped
   to Section 2 targets.
9. **Render** — pptx using 8-section skeleton. Companion docx for
   executive leave-behind.
10. **Output** — /outputs/<slug>-it-architecture-v1.pptx +
    /outputs/<slug>-it-architecture-v1.docx.

### Shared elements

`consulting/_shared/process-taxonomy-sell-plan-move-buy.md` defines the
12-process-area taxonomy (Sell / Plan / Move / Buy + Reporting-Control-
Processing overlay for Finance/HR). Both skills load this as default;
either skill can override with a different taxonomy per engagement.

`consulting/_shared/heatmap-legend-4color.md` defines the 4-color legend
used in IT Architecture heat-maps and structurally compatible with the
Retail Diagnostic 5-axis Recommended Initiatives table.

`consulting/_shared/navigator-ribbon-template.md` defines the numbered
navigator (1–7 for retail diagnostic, 1–8 for IT architecture) that
appears on every slide.

## Decisions

**D-1: pptx, not Google Slides.** The IBM BCS deliverables are native
PowerPoint; the methodology assumes pptx slide constructs (footers,
slide masters, grouped-object heat maps). Google Slides and Keynote are
acceptable targets for export but not for authoring.

**D-2: Skill refuses on missing evidence.** Both skills hard-fail if
mandatory inputs are not supplied (financial extract for diagnostic;
systems inventory for architecture). This is a deliberate enforcement
of the "evidence first" methodology principle. The analyst gets a clear
error, not a hallucinated deck.

**D-3: Benchmarking corpus is curated, not scraped.** The Findings /
Leading Practice pairings in the retail diagnostic skill draw from a
curated corpus of retail-operations research (ECR reports, published
case studies, public regulatory filings). No web-scrape at skill
invocation time; the corpus is cached in the skill's templates
directory and versioned.

**D-4: Output includes provenance footer.** Every deck carries a footer
citing the IBM BCS 2006 methodology lineage and Geoffrey as custodian.
This is both intellectual honesty and a positioning signal (CIO
candidate bringing methodology from Big-4 era into the agent era).

**D-5: v1 is structural; v2 may add live connectors.** v1 reads static
evidence files. v2 (post-dogfood, if there's a real engagement) may add
connectors to Square data, NetSuite, retail POS APIs, etc. v1 ships
first.

## Open questions

- **Q-1: (ANSWERED — plugin.)** The `consulting:*` skills ship as a plugin
  at `plugins/consulting/`, with parity to `brand-voice`, `legal`,
  `marketing`, `engineering` in the user's installed plugin list. See
  Decision D-0 above. This preserves the IP boundary, enables clean
  distribution if the toolset productizes, and keeps the platform
  `.claude/skills/` tree reserved for GrowDirect-internal tooling.
- **Q-2:** Do we license the methodology's shape (public-domain analysis
  frame) or its *execution* (the skill's prompt, templates, benchmarking
  corpus)? The former is obviously public; the latter is Geoffrey's IP
  investment.
- **Q-3:** Is there a role in the Method MOC for a new category — *Consulting
  Methodologies* — or do these skills fit under Techniques with a
  `domain: consulting` tag? Probably the latter; revisit if the toolset
  grows past three skills.
- **Q-4:** Should the evidence-ingest step (file parsing, taxonomy
  extraction) be a shared intake pipeline with the existing
  `content-engine` / `Brain/raw/inbox/` flow? Leaning yes; a third
  synergy beyond retailer-diagnostic and architecture-options.

## Acceptance (from the dispatch)

- Both skill files exist at the paths in the file layout.
- Both skills trigger on the phrases listed in FR-1 and FR-5.
- Running each skill against synthetic evidence produces output matching
  the structural frame (spot-checked against the original IBM decks for
  shape, not content).
- Both methodology wikis are cross-linked from the skill files.
- This SDD is cross-linked in the Method MOC under
  [[Brain/method/Techniques|Techniques Index]].

## Sprint plan

- **Sprint 1 (this session):** dispatch + methodology wikis + SDD + skill
  scaffolds. No deck generation yet.
- **Sprint 2:** populate skill templates with deck-skeleton.pptx files
  (real slide masters with navigator ribbon and 4-color legend palette).
  Populate prize-table and effort-estimate xlsx templates.
- **Sprint 3:** implement the skill's input-prompt flow; test with
  synthetic retailer evidence; structural diff vs. Clarks and Morrisons.
- **Sprint 4:** dogfood — run `consulting:retail-diagnostic` against a
  real retailer evidence pack (possibly Canary's own customer data, or
  a public 10-K). Evaluate output quality.
- **Sprint 5 (conditional):** v2 with live connectors, if dogfood
  results warrant.

## Related

- [[Brain/wiki/methodology-ibm-retail-diagnostic|Methodology · Retail Diagnostic]]
- [[Brain/wiki/methodology-ibm-it-architecture-options|Methodology · IT Architecture]]
- [[Brain/projects/Method|Method MOC]]
- [[Brain/projects/Secure|Secure]] — retail IP archive sibling project
- [[dispatches/2026-04-24-consulting-skills|Dispatch (this initiative)]]
