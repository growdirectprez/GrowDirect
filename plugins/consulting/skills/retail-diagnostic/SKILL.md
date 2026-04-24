---
name: consulting:retail-diagnostic
description: |
  Produce a Big-4-grade Retail Diagnostic deliverable from a retailer's evidence pack,
  using the IBM BCS 2006 Clarks-pattern seven-section frame (Executive Summary →
  Background/Scope/Approach → Financial Analysis & Industry Drivers → Theme 1 F&O →
  Theme 2 F&O → Opportunity Priorities & Roadmap → Prioritised Case for Action).
  Use when the user says "retail diagnostic", "financial baseline for this retailer",
  "find the prize in this retailer", "prioritize the retailer roadmap", "where's the
  lost-sales opportunity", or uploads a retailer's financial extract + systems
  inventory and asks for a consulting-grade diagnosis.
triggers:
  - retail diagnostic
  - financial baseline for retailer
  - find the prize
  - prioritized retailer roadmap
  - where's the lost-sales opportunity
  - retailer opportunity analysis
  - clarks-style diagnostic
author: Geoffrey C. Lyle
lineage: IBM Business Consulting Services, 2006 (Clarks Retail Diagnostic pattern)
methodology: Brain/wiki/methodology-ibm-retail-diagnostic.md
status: v0.1-scaffold
---

# consulting:retail-diagnostic

Produce a 7-section retail diagnostic deck (pptx + companion docx) for a
retailer, using the IBM BCS 2006 Clarks-pattern methodology.

**Read first:** [[Brain/wiki/methodology-ibm-retail-diagnostic|Methodology · IBM Retail Diagnostic]].
That article is the authoritative definition of the structural frame this
skill enforces.

## What this skill does

Plugs into a retailer's evidence pack (financial extract, POS data, systems
inventory, workshop notes) and renders a 7-section consulting deck with:

1. Executive Summary (the whole deck in miniature)
2. Background, Scope & Approach
3. Financial Analysis & Industry Drivers
4. Theme 1 — Findings & Observations (drill per root cause)
5. Theme 2 — Findings & Observations (same pattern)
6. Opportunity Priorities & Roadmap (2×2 matrix + Recommended Initiatives)
7. Prioritised Case for Action (Phase 1 / 2 / 3)

Every slide carries a numbered navigator ribbon. Every theme follows the
four-element drill pattern (Overview → Prize → Per-root-cause drills →
Recommendations). Every prize is quantified in £ low/high range. Every fact
gets a source footnote.

## What this skill does NOT do

- Does not invent financial figures. If the client's financial extract is
  not provided, the skill hard-fails with an explicit error.
- Does not generate a statement of work, engagement letter, or pricing.
- Does not replace analyst judgment — the skill enforces the frame; the
  analyst still brings the evidence and chooses which findings to emphasize.

## Inputs

Required:
- Client name and scope (division, geography)
- Financial extract (xlsx): sales, margin, stock, EBIT over ≥1 fiscal year
- Target themes (1–3) to drill: e.g. Availability, Store Costs, Margin,
  Range Complexity, Promotions

Optional:
- POS / transaction extract (enables margin analysis per-SKU)
- Systems inventory (enables systems-layer recommendations)
- Workshop notes (md or text) — themes from stakeholder interviews
- Client milestones (programme releases, board gates) — used by Section 7
  to align the phased roadmap to already-scheduled events

## Workflow

1. **Intake** — skill asks for inputs above; validates the financial
   extract has at least 12 months of data and 4 measures (sales, margin,
   stock, EBIT). Hard-fail on missing financial extract.
2. **Scope & approach page** — skill drafts Section 2 using the client
   name, scope, and a templated approach phasing (workshops → data
   analysis → benchmarking → synthesis → readout).
3. **Financial analysis** — skill computes headline metrics (sales
   trend, margin %, stock turn, EBIT %) and renders Section 3 with
   industry driver context drawn from the skill's curated corpus.
4. **Per-theme drill-down** — for each of the 1–3 target themes, skill
   runs the four-element pattern:
   - Overview slide (summary of findings + root-cause navigator)
   - Prize slide (£ low/high table + method cite)
   - Per-root-cause drill slides (Findings left / Leading Practice right
     / three bold callouts)
   - Recommendations slide (numbered initiatives + 5-discipline
     implementation challenges: People · Process · Technology · Financial
     · 3rd Parties)
5. **Priorities & Roadmap** — skill builds the Recommended Initiatives
   heat-map (5 axes: Prize1 × Prize2 × Prize3 × Cost × Complexity)
   and the 2×2 prioritisation scatter.
6. **Case for Action** — 3-phase roadmap aligned to client milestones
   if provided.
7. **Executive Summary** — generated last, summarising Sections 2–7.
8. **Render** — pptx output matching the 7-section skeleton. Companion
   docx narrative for leave-behind reading.
9. **Output** — `/outputs/<slug>-retail-diagnostic-v1.pptx` +
   `/outputs/<slug>-retail-diagnostic-v1.docx`. Provenance footer on
   every slide: "Methodology: IBM BCS 2006 / G. Lyle custodian /
   `methodology-ibm-retail-diagnostic.md`".

## Templates referenced

- `templates/deck-skeleton.pptx` — 7-section master with navigator ribbon
  and 4-color palette (Sprint 2)
- `templates/theme-drill-template.md` — the 4-element pattern per theme
  (Sprint 2)
- `templates/prize-table-template.xlsx` — £ low/high range (Sprint 2)
- `_shared/process-taxonomy-sell-plan-move-buy.md` — shared with
  `consulting:it-architecture-options`
- `_shared/heatmap-legend-4color.md` — shared
- `_shared/navigator-ribbon-template.md` — shared

## Example invocations

> "Run a retail diagnostic on the Square merchant data we have from
> Canary. Themes: Availability and Margin. Client milestones: quarterly
> board meetings."

> "We have 12 months of financial data for a 40-store apparel retailer
> and a stakeholder workshop transcript. Produce a diagnostic deck."

> "Find the prize in this retailer." (skill will ask for evidence)

## Acceptance criteria (build sprint)

- Skill triggers on the phrases above
- Running against a synthetic retailer evidence pack produces output
  matching the structural frame of the Clarks deck (spot-check:
  navigator ribbon present; 4-element theme drill pattern; prize
  tables in £; 2×2 matrix; 3-phase roadmap)
- Both pptx and docx outputs render cleanly
- Companion wiki cross-referenced in output footers
- Documented in Method MOC under Techniques

## Related

- [[Brain/wiki/methodology-ibm-retail-diagnostic|Methodology · Retail Diagnostic]] (authoritative)
- [[docs/sdds/consulting/SDD-consulting-skills|SDD · Consulting Skills]]
- Sibling skill: [[plugins/consulting/skills/it-architecture-options/SKILL|consulting:it-architecture-options]]
- [[Brain/projects/Method|Method MOC]]
