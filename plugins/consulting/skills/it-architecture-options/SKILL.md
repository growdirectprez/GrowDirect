---
name: consulting:it-architecture-options
description: |
  Produce a multi-option IT architecture evaluation deliverable for a retailer
  (or adjacent enterprise), using the IBM BCS 2006 Morrisons-pattern eight-section
  frame (Introduction → Programme targets → Sell/Plan/Move/Buy requirements →
  Legacy implications → Option A → Option B → Option C → Summary & recommendation).
  Every option is evaluated through the same seven-slide skeleton (heat-map vs.
  Optimisation, heat-map vs. Aspirational, effort estimate, advantages/disadvantages,
  target architecture). Use when the user says "evaluate IT options", "legacy vs.
  package", "buy vs. build vs. replatform", "architecture options for this retailer",
  or uploads a systems inventory and asks for a structured buy-vs-enhance comparison.
triggers:
  - evaluate IT options
  - legacy vs package decision
  - architecture options for retailer
  - buy vs enhance vs replatform
  - legacy enhancement vs best-of-breed vs integrated
  - morrisons-style architecture review
author: Geoffrey C. Lyle
lineage: IBM Business Consulting Services, 2006 (Morrisons IT Architecture pattern)
methodology: Brain/wiki/methodology-ibm-it-architecture-options.md
status: v0.1-scaffold
---

# consulting:it-architecture-options

Produce an 8-section multi-option IT architecture evaluation deck (pptx +
companion docx) using the IBM BCS 2006 Morrisons-pattern methodology.

**Read first:** [[Brain/wiki/methodology-ibm-it-architecture-options|Methodology · IBM IT Architecture Options]].
Authoritative definition of the structural frame this skill enforces.

## What this skill does

Plugs into a retailer's systems inventory + business programme targets and
renders an 8-section architecture-options deck with:

1. Introduction
2. Programme Targets (margin / overhead / headcount / sales / profits)
3. Business Requirements — Sell / Plan / Move / Buy process frame
4. Implications for Legacy Systems (two heat-map views: org structure + process)
5. Option A — Legacy Enhancement (seven-slide skeleton)
6. Option B — Best-of-Breed Package (same skeleton)
7. Option C — Integrated Package (same skeleton)
8. Summary & Conclusion (side-by-side comparison + recommendation)

Every option is evaluated through the identical seven-slide skeleton:
- Title + one-liner
- Architecture vs. Optimisation requirements (org-structure heat-map)
- Architecture vs. Optimisation requirements (process heat-map)
- Development effort estimate (man-days → man-years)
- Architecture vs. Aspirational requirements (org-structure heat-map)
- Architecture vs. Aspirational requirements (process heat-map)
- Advantages / Disadvantages + target architecture diagram

The summary section renders all three target architectures on aligned
process-frame rows so the reader compares box-for-box. The recommendation
slide is mapped explicitly to Section 2 programme targets.

## What this skill does NOT do

- Does not produce the effort estimate without a systems inventory. Skill
  hard-fails on missing inventory.
- Does not recommend specific vendors (Retek, SAP, Oracle, etc.) unless
  the analyst provides vendor data in the inventory. Skill's recommendation
  stays at the option-class level (Legacy / BoB / Integrated) unless given
  specifics.
- Does not author the statement of work or migration RFP — those are
  separate sprints / separate skills.

## Inputs

Required:
- Client name
- Systems inventory (csv or json): app name, function, technology, age,
  vendor, integration pattern
- Business programme targets (margin, overheads, headcount, sales, profits)
  with target year

Optional:
- Optimisation requirements (near-term, 12–24 months) — narrative or bullet
  list
- Aspirational requirements (3–5 years)
- Options to evaluate (default: A=Legacy Enhancement, B=Best-of-Breed,
  C=Integrated Package; configurable up to 5 options)
- Process taxonomy override (default: Sell/Plan/Move/Buy; swap in CBM
  Component Business Model or other frame if engagement calls for it)

## Workflow

1. **Intake** — skill asks for inputs; validates systems inventory has
   at minimum app name, function, technology fields. Hard-fail on missing.
2. **Section 2 Programme Targets** — rendered verbatim from input.
3. **Section 3 Process Frame** — rendered from shared
   `process-taxonomy-sell-plan-move-buy.md` (default) or custom frame.
4. **Section 4 Legacy Heat-map** — for each app in the inventory, skill
   evaluates against Optimisation requirements and applies 4-color legend.
   Two views: org-structure axis (Shop Systems / Distribution / Retail Ops
   / Trading / Finance-Personnel / Reporting / IT), process axis
   (Sell/Plan/Move/Buy).
5. **Per-option loop (Sections 5–7, and more if requested)** — for each
   option, skill runs the 7-slide skeleton. Effort estimates derived from
   inventory + effort-factor heuristics (configurable in
   `templates/effort-estimate-factors.yml`).
6. **Section 8 Summary** —
   - Page 8.1: Architecture comparison — three target architectures on
     aligned Sell/Plan/Move/Buy rows
   - Page 8.2: Implementation comparison — timescale, risk, dependencies,
     modularity, time-to-benefits
   - Page 8.3: Recommendation — mapped to Section 2 programme targets
7. **Render** — pptx output matching 8-section skeleton. Companion docx
   executive narrative for leave-behind.
8. **Output** — `/outputs/<slug>-it-architecture-v1.pptx` +
   `/outputs/<slug>-it-architecture-v1.docx`. Provenance footer:
   "Methodology: IBM BCS 2006 / G. Lyle custodian /
   `methodology-ibm-it-architecture-options.md`".

## Templates referenced

- `templates/deck-skeleton.pptx` — 8-section master (Sprint 2)
- `templates/option-skeleton.md` — 7-slide per-option template (Sprint 2)
- `templates/effort-estimate-template.xlsx` — man-days schema (Sprint 2)
- `templates/effort-estimate-factors.yml` — heuristic factor config (Sprint 2)
- `_shared/process-taxonomy-sell-plan-move-buy.md` — shared default
- `_shared/heatmap-legend-4color.md` — shared
- `_shared/navigator-ribbon-template.md` — shared (1..8 for this skill)

## Example invocations

> "Evaluate IT options for this 200-store grocer. Systems inventory is
> attached as csv. Programme targets: 1% margin up, £100m overheads down
> by 2028. Evaluate Legacy Enhancement, Best-of-Breed, and SAP."

> "We're deciding whether to extend our existing in-house WMS or move to
> Blue Yonder. Treat this as a two-option analysis (Legacy vs. Integrated)."

> "Architecture options for a retailer modernizing POS." (skill asks for
> inventory + targets)

## Acceptance criteria (build sprint)

- Skill triggers on the phrases above
- Running against a synthetic systems-inventory produces output matching
  the structural frame of the Morrisons deck (spot-check: 4-color legend;
  two-axis heat-maps; 7-slide option skeleton; man-days estimate table;
  side-by-side summary; recommendation mapped to targets)
- Both pptx and docx outputs render cleanly
- Side-by-side summary is the only opinion — all prior sections are
  structural, symmetric, defensible
- Companion wiki cross-referenced in output footers

## Related

- [[Brain/wiki/methodology-ibm-it-architecture-options|Methodology · IT Architecture Options]] (authoritative)
- [[docs/sdds/consulting/SDD-consulting-skills|SDD · Consulting Skills]]
- Sibling skill: [[plugins/consulting/skills/retail-diagnostic/SKILL|consulting:retail-diagnostic]]
- [[Brain/projects/Method|Method MOC]]
