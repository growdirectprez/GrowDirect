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

---

## Structural Extract & Deeper Patterns (2026-04-24)

**Full-text source extraction:** 102 slides extracted to markdown via `python3 -m markitdown` (2026-04-24). Extraction file: `Brain/raw/.extract/Clarks/clarks-retail-diagnostic.md` (4699 lines).

**Deeper structural observations:**

1. **Navigator ribbon as structural spine:** Every slide (1–102) carries a numbered navigator (1–7) in the top-right corner. The ribbon is the deck's single strongest enforcer of section discipline. Slides without a ribbon or with mismatched section numbers should be removed (quality gate).

2. **Repeating four-element pattern (Sections 4–5):** Every theme (Availability, Store Labour) uses:
   - Overview slide (left: findings summary, right: root-cause navigator TOC, footer: three callouts)
   - Prize slide (center: £ low/high table, right: derivation narrative, footer: three callouts)
   - Per-root-cause drills (6–8 repeating pattern: Findings left, Leading Practice right, three callouts footer)
   - Recommendations block (numbered actions, 5-axis implementation challenges, three callouts)
   This pattern is **transferable**: applies to any theme, any retailer.

3. **Symmetry rule:** Sections 4–5 (two themes) have roughly equal slide depth (27 vs. 22 pages). Asymmetry (8 vs. 10 drills per theme) is OK if justified by evidence depth; perfect symmetry (8–8, 9–9) is preferred for reader training.

4. **Three-phase roadmap naming convention:** Phases answer sequential questions:
   - Phase 1: "What are our quick wins?" (6–12 months, minimal org change)
   - Phase 2: "What builds the system?" (12–24 months, platform investment)
   - Phase 3: "What's the end state?" (24+ months, capability/culture shift)
   This naming is **not** unique to Clarks; it's foundational to any multi-year diagnostic roadmap.

5. **Milestones overlay discipline:** Roadmap is not a theoretical future state; it's overlaid on **client's existing programme calendar** (e.g., "Fusion Go-Live Q2-07", "CIPR1 Release 3a Q3-07"). This grounds the diagnostic in organizational reality, not consultant fantasy.

---

## Cross-Reference: Clarks Frame → Canary Spine

The Clarks seven-section methodology maps directly to Canary's spine ring sequencing:

| Clarks Section | Frame Element | Canary Module(s) | Canary Ring | Notes |
|---|---|---|---|---|
| **1** | Executive Summary | All (roll-up) | All rings | Summarizes financial baseline + themes + roadmap. |
| **2** | Approach | (metadata) | — | Documents diagnostic scope, data sources, stores sampled. |
| **3** | Financial Baseline | T (Transaction), Sales | Current state | Establishes merchant's financial reality: sales, margin, stock-turn, CSI. Peer benchmarks provide context. |
| **4** | Theme 1: Availability | Q (Chirp: loss prevention) | Existing (v1) | Drill into root causes of stock-outs, lost sales, untendered orders, cash-handling delays. Chirp rules C-009, C-104, C-204, C-301, C-502, C-602 are detection mechanisms. |
| **5** | Theme 2: Store Labour / Efficiency | D (Demand), J (Journey), F (Financial Control) | v2 ring | Drill into perpetual-ledger accuracy (D), demand forecast + replenishment (D+J), order fulfillment orchestration (J), shrink root-cause (F). |
| **6** | Opportunity Priorities & Roadmap | D, J, S, P, L, W | v2 + v3 rings | Heat-map prioritization. Phased roadmap aligns to Canary product delivery cadence. Phase 1 (Q existing), Phase 2 (v2 ring: D/J/F), Phase 3 (v3 ring: S/P/L/W). |
| **7** | Case for Action | (strategic narrative) | Vision | Grounded in competitive/regulatory pressure. Quantifies risk of inaction + upside of execution. Aligns roadmap to merchant's strategic imperatives. |

**Canary v2 ring modules directly address Clarks Theme 2 root causes:**
- **Module D (Demand):** Perpetual ledger, demand forecast, OTB enforcement, automated replenishment trigger. Addresses root causes: Replenishment Process Lead-Time, Book Stock Accuracy, Upstream Supply Chain visibility.
- **Module O (Journey):** Customer order fulfillment orchestration, inter-location inventory visibility, backorder tracking. Addresses root causes: Store Ordering Process, Margin-Driven Delivery Restrictions, Range Complexity.
- **Module F (Financial Control):** Shrink variance root-cause analysis, daily reconciliation discipline. Cross-theme infrastructure.

**Canary v3 ring modules extend into Clarks Phase 3 (end-state strategy):**
- **Module S (Sales Margin Analytics):** Real-time margin visibility by product/category/location. Addresses residual margin erosion from unplanned discounting + product-mix drift.
- **Module P (Pricing Intelligence):** Automated markdown recommendations, price-elasticity modeling. Drives margin recovery on slow-movers without customer experience degradation.
- **Module L (Long-term Planning):** Strategic inventory planning, seasonality alignment, range-optimization. Reduces overstock root-cause before it becomes a clearance burden.
- **Module E (Wholesale / Multi-Channel):** Foundation for future expansion (marketplace, B2B wholesale, subscription). Out of scope for v2 diagnostic.

**Key insight:** The Clarks methodology's three-phase roadmap pattern **naturally aligns to Canary's spine rings** (Existing + v2 + v3). This is not coincidence; it reflects how enterprise retail systems evolve: immediate loss-prevention wins, then operational-efficiency platform build, then strategic margin/growth optimization.

---

## Worked Example: Canary Retail Diagnostic (Archetype Specialty Retailer)

**Location:** `Canary-Retail-Brain/case-studies/canary-retail-diagnostic-archetype.md` (772 lines; dated 2026-04-24).

**Summary by section:**

1. **Executive Summary:** Specialty footwear retailer (8 stores, £12m revenue). Three opportunities: £280k–£420k loss-prevention (Chirp), £1.2m–£1.8m inventory/replenishment (D+J), £280k–£400k margin analytics (S+P, Phase 3). Cumulative prize: £1.48m–£2.22m annual EBIT uplift (12–18% margin improvement).

2. **Background & Approach:** Q1–Q4 2025 analysis; 142,847 transactions; Canary schema (T, Sales, Metrics) + SFRA 2025 benchmark (n=87, £8m–£15m revenue band).

3. **Financial Baseline:** Sales £12.1m, margin 15.7% (1.3 pts below peer median 17.0%). Margin delta £280k. Stock turn 1.8x vs. peer median 2.1x (£140k working capital tied up). CSI 3.2/5 vs. peer 3.8/5 (lost-sales impact).

4. **Theme 1 — Loss Prevention (6 root-cause drills):**
   - Settlement Delays (C-009): £35k–£65k opportunity (float cost, reconciliation risk).
   - After-Hours Drawer (C-104): £28k–£52k (unscheduled activity, cash variance).
   - Untendered Orders (C-204): £85k–£142k (merchandise removed without sale).
   - Off-Clock Transactions (C-301): £42k–£78k (employee discount abuse, comping leakage).
   - Post-Void Cancellations (C-502): £58k–£96k (process errors, rework cost, lost sales).
   - Gift Card Drain (C-602): £32k–£47k (anomalous redemptions, fraud).
   - **Total:** £280k–£420k annual opportunity.

5. **Theme 2 — Inventory & Replenishment (5 root-cause drills):**
   - Perpetual Ledger Accuracy: £240k–£360k (shrink variance closure via daily reconciliation).
   - Demand Forecast & Replenishment Triggers: £310k–£465k (stock-out reduction, availability uplift).
   - Multi-Location Visibility: £310k–£465k (inter-location transfer optimization, lost-sales avoidance).
   - Order Fulfillment Orchestration: £150k–£225k (backorder capture, repeat-purchase drive).
   - Shrink Variance & Root-Cause Analysis: (rolled into Perpetual Ledger opportunity).
   - **Total:** £1.2m–£1.8m annual opportunity (phased over Phase 2: 12–18 months).

6. **Opportunity Priorities & Roadmap:**
   - Heat-map: 7 recommendations × 5 axes (3 prize, 2 cost/complexity).
   - 2×2 Matrix: Phase 1 Quick Wins (Chirp, Loss Review) vs. Phase 2 Build the System (D, J modules).
   - Phase 1 (Q1–Q4 2026): Chirp detection + 24h SLA. £140k–£210k benefit (50% of loss-prevention opportunity). Effort: 3 weeks merchant, 1 week Canary support. Cost: £3k–£5k.
   - Phase 2 (Q1–Q4 2027): Build Module D (perpetual ledger) + demand forecast + auto-replenishment + Module O (fulfillment orchestration). £800k–£1.2m cumulative benefit (full inventory opportunity). Effort: 40–50 weeks Canary dev, 20–25 weeks merchant scale. Cost: £35k (amortized across merchants).
   - Phase 3 (2028+): Module S (margin analytics) + Module P (pricing intelligence). £280k–£400k incremental. Out of scope for this diagnostic; scoped in 2027.

7. **Case for Action:**
   - **Why now:** DTC e-commerce pressure (3–5 pt market-share loss annually); UK labor legislation (labor costs rising); Canary v2 ring now available.
   - **Risk of inaction:** £580k–£850k EBIT downside by 2028 (margin erosion 0.5–1.0 pt annually, competitive share loss, working-capital cost increase).
   - **Strategic upside:** Stock turn improves to 2.1x, CSI to 3.8/5, margin to 16.8% (0.8 pt improvement, £230k–£290k EBIT). Revenue growth from improved availability: £600k–£800k. Cumulative EBIT uplift: £370k–£430k annual by 2028.
   - **Net swing:** £950k–£1.28m to operator/shareholder vs. do-nothing scenario.

**Methodology proof:** This case study demonstrates the Clarks frame produces Big-4-grade consulting output when applied to a real retailer (illustrative archetype, not a real engagement). All seven-section structure, repeating drill pattern, prize-sizing transparency, and phased roadmap are preserved. Root causes map to Canary spine modules (Q, D, J, S, P); roadmap aligns to Canary v2/v3 delivery cadence.

---

## SDD: Clarks Retail Diagnostic — Method as SDD

**Location:** `docs/sdds/consulting/SDD-clarks-retail-diagnostic-v2.md` (452 lines; dated 2026-04-24).

**Status:** v0.1 design. Structural specification derived from parsed IBM BCS 2006 Clarks deck (102 pages). Extraction complete. Awaiting mapping to skill workflow + Canary integration (Stage 3–4 in progress).

**Key sections:**

- **Purpose:** Codify IBM BCS 2006 Clarks Retail Diagnostic as executable skill (`consulting:retail-diagnostic`). Shape enforcer: given retailer's evidence, produces 7-section pptx + docx deck with numbered navigator on every slide.

- **Seven-Section Frame:** Executive Summary → Background/Scope/Approach → Financial Baseline → Theme 1 → Theme 2 → Opportunity Priorities & Roadmap → Prioritised Case for Action.

- **Per-Section Slide Skeletons:** Detailed rules for navigator ribbon placement, prize-sizing table structure, left-right column pattern (Findings/Leading Practice), three-callout footer rule, root-cause drill skeleton.

- **Theme Drill Pattern:** 4-element repeating structure (Overview → Prize → N root-cause drills → Recommendations block). Same pattern applies to any theme, any retailer.

- **Prize-Sizing Pattern:** Math transparency rule — every £ range must show its calculation on same slide. No "significant opportunity" without numbers.

- **Phased Roadmap Pattern:** Three phases answering sequential questions: Phase 1 "quick wins?" (6–12 mo, low change), Phase 2 "build system?" (12–24 mo, platform investment), Phase 3 "end state?" (24+ mo, strategic shift). Align to client's known milestones.

- **Case for Action Structure:** Why now? (grounded in one named competitive/regulatory fact). Risk of inaction (quantified downside). Strategic upside (aligned to baseline). Action plan (pre-requisites, first-90-day checklist).

- **Acceptance Criteria:** 10 criteria for a delivered diagnostic (7 sections complete, all slide types present, source citations visible, no placeholder text, opens in PowerPoint + Keynote).

- **Mapping to Canary Spine:** 7-row table showing Clarks sections → Canary modules (Q, D, J, S, P, L, W) → spine rings (Existing, v2, v3).

- **Open Questions:** Evidence pack format (JSON vs. YAML vs. markdown)? Multi-theme extension beyond 2 themes? Cost/duration estimates per recommendation? Direct Canary API integration vs. manual data-pack input?

**Status for next sprint:** SDD is design-complete (v0.1). Next phase (not part of this dispatch) would be Skill.md definition (trigger, workflow, prompt, invocation pattern) + pptx template scaffolding + evidence-pack schema definition.

---

## Related

- [[docs/sdds/consulting/SDD-clarks-retail-diagnostic-v2|SDD · Clarks Retail Diagnostic — Method as SDD]]
- [[Canary-Retail-Brain/case-studies/canary-retail-diagnostic-archetype|Worked Example: Canary Retail Diagnostic (Archetype Specialty Retailer)]]
- [[docs/sdds/consulting/SDD-consulting-skills|SDD · Consulting Skills]] (parent framework)
- [[Brain/wiki/methodology-ibm-it-architecture-options|Methodology · IBM IT Architecture Options]] (sibling methodology)
- [[Brain/projects/Method|Method MOC]]
- [[Brain/projects/Canary|Canary MOC]]
