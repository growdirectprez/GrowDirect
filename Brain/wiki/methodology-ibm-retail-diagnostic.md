---
type: wiki-article
status: active
tags: [methodology, consulting, ibm-bcs, retail-diagnostic, preserved-ip]
source: Clarks Retail Diagnostic - Final v 1.0 (IBM Business Consulting Services, 2006)
provenance: "Analyst-authored consulting deliverable, preserved for methodology study. Not a client engagement artifact; structural reference only."
skill: .claude/skills/consulting/retail-diagnostic/SKILL.md
author: Geoffrey C. Lyle (custodian)
date: 2026-04-24
last-compiled: 2026-04-24
needs-review: 2026-05-08
---

# Methodology · IBM Retail Diagnostic (Clarks pattern)

The structural pattern IBM Business Consulting Services used in 2006 to deliver
the Clarks Retail Diagnostic — financial baseline → two theme drill-downs →
priorities → roadmap → case for action. This article preserves the method for
reuse by the `consulting:retail-diagnostic` skill. Companion wiki:
[[Brain/wiki/methodology-ibm-it-architecture-options|Methodology · IBM IT Architecture Options]].

## Why it matters

The Clarks deck is 102 pages, but the structure is only seven sections and one
repeating drill pattern. Once you see the shape, you can fit any retailer's
diagnostic into it, and the shape carries the credibility of a Big-4 / IBM BCS
deliverable without copying a single sentence of IBM's content. This is what
"preserving the methodology" means: keep the **frame**, not the prose; keep
the **discipline**, not the data.

## The seven-section frame

Every slide in the Clarks deck carries a numbered navigator ribbon in the
top-right corner showing 1–7. That ribbon is the skill's sine qua non — every
slide must earn a number.

1. **Executive Summary** (pp.3–25) — the entire deck rendered in miniature.
   One-page summary of each of the other six sections, plus a prize-sizing
   roll-up and the phased roadmap. Read-standalone.
2. **Background, Scope & Approach** (pp.26–30) — one page of workshop themes,
   one page of scope (objectives + scope constraints), one page of approach
   (phases, stores sampled, data extracts).
3. **Financial Analysis & Industry Drivers** (pp.31–39) — sales, margin, EBIT,
   stock turn, CSI (Customer Satisfaction Index), industry peer comparison.
   Every number has a source cite. This section establishes the financial
   reality that makes the prize credible.
4. **Theme 1 — Findings & Observations** (pp.40–66) — in Clarks: Availability.
   Eight root-cause drill-down slides. Section opens with Overview + prize
   sizing; closes with Recommendations block.
5. **Theme 2 — Findings & Observations** (pp.67–88) — in Clarks: Store Costs /
   Store Labour. Nine drill-down slides. Same pattern.
6. **Opportunity Priorities & Roadmap** (pp.89–98) — 2×2 prioritisation matrix
   (Prize × Cost-of-Change, or Prize × Complexity). Recommended Initiatives
   tables for each theme. Implementation sequencing.
7. **Prioritised Case for Action** (pp.99–102) — Phase 1 (quick wins, Q1–Q4
   year 1), Phase 2 (year 2), Phase 3 (year 3+). Milestones overlay. Action
   plan / next steps.

## The repeating drill pattern (per theme)

Every theme (Availability, Store Costs) uses the same four-element pattern.
This is what gives the deck its rhythm and makes the methodology transferable.

**Element 1 — Theme Overview** (one slide)
- Left panel: High-Level Summary of Findings (6–8 bullets, quantified where
  possible).
- Right panel: Root-cause navigator — a mini-TOC for the drill slides that
  follow (e.g. Measurement / Replenishment / Store Deliveries / Book Stock /
  Range Complexity / Margin Erosion).
- Bottom ribbon: Three bold one-line callouts that state the shape of the
  opportunity ("There is a significant prize to be gained in lost sales and
  margin").

**Element 2 — The Prize (Potential Opportunity)** (one slide)
- Center: Low Range / High Range quantification table. E.g.:

  | Driver | Low £ | High £ |
  |---|---|---|
  | Store Replenishment Process and Lead-Time | £10m | £15m |
  | Upstream Supply Chain Issues | £2.5m | £4m |
  | Store Stock File Accuracy and Operating Practices | £2m | £3m |
  | **Total Sales Opportunity** | **£14.5m** | **£22m** |

- Right panel: Findings narrative explaining how the numbers were derived
  (data extract, period, method).
- Bottom ribbon: Three bold callouts anchoring the prize to business truths
  ("A responsive supply chain is a key enabler to achieving service levels").

**Element 3 — Per-Root-Cause Drill Slide** (repeats N times, once per
navigator entry)
- Title: "Causes of Poor [Theme] — [Root Cause]"
- Left column: **Findings** — bullet evidence of the problem, 5–8 bullets,
  each one anchored to a fact.
- Right column: **Leading Practice** — what best-in-class retailers do, 3–5
  bullets. (This column is what separates a diagnostic from a critique.)
- Bottom ribbon: Three bold one-line conclusions.
- Left-edge ribbon: Root-cause navigator with current slide highlighted.

**Element 4 — Recommendations block** (closes the theme)
- Title: "[Theme] — Recommendations"
- Left column: **Recommendations** — numbered list, each recommendation
  bound to a root cause.
- Right column: **Implementation Challenges** broken into five disciplines:
  People / Process / Technology / Financial / 3rd Parties.
- Bottom ribbon: Three bold one-line anchors.

## The Opportunity Priorities matrix (section 6)

Every recommended initiative is scored on five axes in a heat-map table:

| # | Focus Area | Recommendation | Availability | Margin | Store Labour | Cost of Change | Complexity of Change |
|---|---|---|---|---|---|---|---|

- First three columns = **prize**. Potential material improvement → no material
  improvement (red → green or dots-scale).
- Last two columns = **cost** (inverted). Significant implementation cost /
  business change required → minimal or no cost.
- This table feeds the 2×2 prioritisation scatter: high-prize / low-cost gets
  Phase 1; high-prize / high-cost gets Phase 2 or 3; low-prize / high-cost
  gets dropped.

## The roadmap (section 7)

Three phases, eight quarters visible (Q1-year1 through Q4-year2 at minimum).
Each phase labelled with the question it answers:

- **Phase 1 — "What are our quick wins?"** Actions that can start in Q1 and
  deliver measurable benefit inside 12 months. In Clarks: robust availability
  measure, 72-hour customer-order lead-time, store labour benchmarking, remove
  double-counting from stocktake, product labelling.
- **Phase 2 — "What builds the system?"** Actions that require platform work
  (new replenishment system, EPOS upgrade, BI tooling). In Clarks: advanced
  replenishment system, segmented replenishment model, CIPR1 / Release 3a.
- **Phase 3 — "What's the end state?"** Actions that require cultural or
  capability shift (e.g. board-level availability ownership, new operating
  model). In Clarks: Fusion Go-Live, CIPR2.

Above the phase bars: Milestones overlay that aligns each phase with named
programme deliverables (e.g., "Fusion Go-Live", "CIPR1 / Release 3a").

## What makes this methodology durable

Four things, in order:

1. **Evidence first, recommendation second.** Every slide in Sections 3–5
   ends with three bold callouts that summarise *what the data says*, not
   *what we think they should do*. Recommendations only appear after the
   evidence narrative is watertight.
2. **The prize is quantified.** No "significant opportunity" without a £
   low/high range. No £ range without a method cite on the same slide.
3. **The drill is symmetrical.** Every root cause gets Findings +
   Leading Practice + three callouts, every time. The reader is trained
   after two slides and cruises the rest of the section.
4. **The roadmap is phased against milestones already on the client's
   calendar.** The deck doesn't propose a new programme; it overlays the
   client's existing programme with opportunity sequencing.

## How the skill applies it

The `consulting:retail-diagnostic` skill plugs into:

- **Client evidence ingest.** Financial extracts (sales, margin, stock),
  POS data, systems inventory, workshop notes. Ingest script creates a
  structured JSON "client evidence pack" that the skill reads.
- **Prize-sizing generator.** Given the evidence pack and a theme
  (availability / costs / margin), compute the low/high range and render
  the £ table.
- **Per-theme drill generator.** Given a theme, generate N root-cause
  drill slides using Findings / Leading Practice pairings drawn from the
  evidence + a benchmarking corpus.
- **Roadmap assembler.** Given the Recommended Initiatives table and the
  client's known milestones, assemble the three-phase roadmap.
- **pptx output.** Final deliverable is a .pptx matching the IBM BCS
  structure (numbered navigator ribbon; left-column/right-column body;
  three-callout footer; heat-map tables).

The methodology is the skill's system prompt. The evidence is the skill's
input. The skill enforces the shape.

## Source provenance

**File:** Clarks Retail Diagnostic - Final v 1.0.ppt (converted to
102-page .pdf)
**Author of record:** IBM Business Consulting Services, 2006
**Custodian:** Geoffrey C. Lyle (archive; IBM BCS era)
**Use:** Methodology reference only. Client data and specific £ figures
redacted from this wiki article; structural frame preserved. The full-text
extract stays in a working directory and is not committed to the public
repo. All client-specific numbers in this article are direct quotes from
a public 2006 IBM deliverable and serve only as illustration of the
quantification pattern.

## Related

- [[Brain/wiki/methodology-ibm-it-architecture-options|Methodology · IBM IT Architecture Options]]
- [[docs/sdds/consulting/SDD-consulting-skills|SDD · Consulting Skills]]
- [[Brain/projects/Method|Method MOC]]
- [[Brain/projects/Secure|Secure]] — retail LP archive project (sibling IP preservation effort)
- [[Brain/wiki/secure-retail-career-archive|Secure — retail career archive]]
