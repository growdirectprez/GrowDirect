---
type: sdd
status: v0.1-design
domain: consulting
component: clarks-retail-diagnostic
author: Geoffrey C. Lyle
date: 2026-04-24
owner: GrowDirect LLC
classification: confidential
tags: [sdd, consulting, retail-diagnostic, ibm-bcs, methodology-as-code]
related:
  - Brain/wiki/methodology-ibm-retail-diagnostic.md
  - docs/sdds/consulting/SDD-consulting-skills.md
  - Brain/raw/.extract/Clarks/clarks-retail-diagnostic.md
  - Canary-Retail-Brain/case-studies/canary-retail-diagnostic-archetype.md
---

# SDD — Clarks Retail Diagnostic: Method as SDD

## Status

**v0.1 design** — structural specification derived from the parsed IBM BCS 2006 Clarks Retail Diagnostic (102 pages). Extraction complete. Awaiting mapping to skill workflow and Canary spine integration (Stage 3–4).

---

## Purpose

Codify the IBM Business Consulting Services 2006 Clarks Retail Diagnostic as an executable agent skill (`consulting:retail-diagnostic`). The skill is a **shape enforcer**: given a retailer's evidence (financial extracts, transaction data, workshop notes), it produces a 7-section, numbered-navigator, Big-4-grade diagnostic deck in pptx + docx format. The skill enforces the frame; the analyst brings the evidence.

---

## Source Provenance

| Attribute | Value |
|-----------|-------|
| **Original** | *Clarks Retail Diagnostic — Final v 1.0.ppt* (IBM BCS, March 2006, 102 pages) |
| **Custodian** | Geoffrey C. Lyle (archive; IBM era) |
| **Status** | Methodology reference (structure preserved, client data redacted) |
| **Extraction** | 4699-line markdown via `python3 -m markitdown`, dated 2026-04-24 |
| **Archive Path** | `Brain/raw/.extract/Clarks/clarks-retail-diagnostic.md` |
| **Use** | Structural pattern for `consulting:retail-diagnostic` skill design |

---

## The Seven-Section Frame

Every slide in the source deck carries a numbered navigator ribbon (1–7) in the top-right corner. The frame is:

### Section 1 — Executive Summary (Source: pp.3–25)

**Purpose:** Miniature of entire deck; read-standalone for C-suite review.

**Structure:**
- One-page mini-summary of each of Sections 2–7.
- Roll-up prize-sizing table (all themes combined, low/high range).
- Phased roadmap with milestones overlay (Phase 1 quick wins, Phase 2 platform build, Phase 3 end-state).
- Navigation carousel showing 1–7 section tabs.

**Slide count in source:** ~23 pages.

**Acceptance criteria for generated output:**
- Carries navigator ribbon "1" on every slide.
- Summarizes financial baseline (Section 3) in 3–4 bullet points with £ callouts.
- Summarizes each theme (Sections 4–5) as "Overview → Prize → Root-cause thumbnails → Recommendations summary."
- Phased roadmap visible above fold on one slide with milestone markers.
- All numbers cited to source section/slide.

---

### Section 2 — Background, Scope & Approach (Source: pp.26–30)

**Purpose:** Workshop frame, scope constraints, analytical method.

**Structure:**
- **Page 1:** Workshop themes (objectives, alignment to strategic plan).
- **Page 2:** Scope (what was in, what was out; store sample strategy; data sources).
- **Page 3:** Analytical approach (phases of work; team composition; data-extraction dates).

**Slide count in source:** 5 pages.

**Acceptance criteria for generated output:**
- Carries navigator ribbon "2" on every slide.
- Scope constraints explicitly stated ("Diagnostic focused on Availability & Margin; Store Labour; out of scope: Supply Chain Strategy, Central Merchandising").
- Store sample size and geography documented.
- Data-extraction date and period-analyzed labeled on data-sourced slides.

---

### Section 3 — Financial Baseline & Industry Drivers (Source: pp.31–39)

**Purpose:** Establish financial reality and credibility for prize-sizing.

**Structure:**
- **Slide 1:** Sales, margin, EBIT, stock-turn, CSI (Customer Satisfaction Index) current-state vs. peer benchmark.
- **Slides 2–4:** Drill into margin erosion drivers, stock turn drivers, labor-cost drivers.
- **Slide 5:** Industry peer comparison (Best in Class, Industry Average, Clarks).

**Slide count in source:** 9 pages.

**Acceptance criteria for generated output:**
- Carries navigator ribbon "3" on every slide.
- All figures carry source footer (Period: Q1–Q4 2005, Extract: 2006-03-15, Source: Clarks EPOS + GL).
- Peer benchmarks carry attribution (Source: Dun & Bradstreet / RetailMeNot / industry published data).
- At least one financial metric (margin, stock turn) shows worst/best/actual band with commentary on what closes the gap.

---

### Section 4 — Theme 1 — Availability: Findings & Observations (Source: pp.40–66)

**Purpose:** Drill into root causes of lost sales and margin due to stock unavailability.

**Structure:** Uses the repeating four-element pattern:

1. **Overview slide (Slide 1):**
   - Left: High-level findings (6–8 bullets, quantified where possible).
   - Right: Root-cause navigator mini-TOC (e.g., "Replenishment Lead-Time / Book Stock Accuracy / Supplier Delivery / Range Complexity").
   - Footer: Three bold one-liners ("There is a significant prize to be gained in lost sales and margin").

2. **Prize slide (Slide 2):**
   - Center: Low/High £ quantification table.
     ```
     | Driver | Low £ | High £ |
     |--------|-------|--------|
     | Replenishment Process & Lead-Time | £10m | £15m |
     | Upstream Supply Chain | £2.5m | £4m |
     | Store Stock File Accuracy | £2m | £3m |
     | Total Sales Opportunity | £14.5m | £22m |
     ```
   - Right: Narrative explaining derivation (data period, method, assumptions).
   - Footer: Three bold callouts ("A responsive supply chain is a key enabler").

3. **Per-root-cause drill slides (Slides 3–N):**
   - Title: "Causes of Poor Availability — [Root Cause]"
   - Left column: **Findings** (5–8 bullet-evidence pairs, each anchored to fact).
   - Right column: **Leading Practice** (what best-in-class retailers do; 3–5 bullets).
   - Left-edge ribbon: Root-cause navigator with current slide highlighted.
   - Footer: Three bold one-line conclusions.

4. **Recommendations block (Final slide of theme):**
   - Title: "Availability — Recommendations"
   - Left: Numbered recommendations (each bound to a root cause).
   - Right: **Implementation Challenges** by discipline (People / Process / Technology / Financial / 3rd Parties).
   - Footer: Three bold anchors.

**Slide count in source:** 27 pages.

**Root causes in source:** Replenishment Process Lead-Time, Supplier Delivery, Upstream Supply Chain, Store Stock-on-Hand File Accuracy, Book Stock File Accuracy, Range Complexity & Seasonality, Store Ordering Process, Margin-Driven Delivery Restrictions.

**Acceptance criteria for generated output:**
- Carries navigator ribbon "4" on every slide.
- At least 8 root-cause drill slides (one per navigator entry).
- Prize table shows 3–4 drivers, low and high range, sum total visible.
- Each drill slide carries evidence-on-left / leading-practice-on-right pattern.
- Recommendations slide explicitly lists which recommendation addresses which root cause.
- All evidence bullets cite data period and source (e.g., "Average replenishment lead-time: 14 days (EPOS data, Q1–Q4 2005)").

---

### Section 5 — Theme 2 — Store Labour: Findings & Observations (Source: pp.67–88)

**Purpose:** Drill into root causes of store labor cost inefficiency.

**Structure:** Identical four-element pattern as Section 4.

1. **Overview slide:** Root-cause navigator (e.g., "Labor Scheduling / Rota Planning / Time & Attendance / Store Layout & Process / Customer Service Model").
2. **Prize slide:** Low/High £ quantification by labor-cost driver.
3. **Per-root-cause drills (Slides 3–N):** Findings / Leading Practice pattern.
4. **Recommendations block:** Implementation challenges by discipline.

**Slide count in source:** 22 pages.

**Root causes in source:** Labour Scheduling & Rota Planning, Time & Attendance Accuracy, Store Layouts & Processes, Task-Based Activity Assignment, Stock-Handling Efficiency.

**Acceptance criteria for generated output:**
- Carries navigator ribbon "5" on every slide.
- At least 5 root-cause drill slides.
- Prize table quantifies labor-cost opportunity (e.g., "Schedule optimization: £2m–£3.5m; labor utilization: £1m–£1.5m").
- Each drill anchors findings to staffing-level data or time-motion observations.

---

### Section 6 — Opportunity Priorities & Roadmap (Source: pp.89–98)

**Purpose:** Prioritize all recommendations; phase them against client's existing milestones.

**Structure:**
1. **Heat-map table (Slides 1–2):** All initiatives scored on five axes:
   - **Prize axes (3):** Availability impact, Margin impact, Store Labour impact (red = high, green = none).
   - **Cost axes (2):** Cost of Change, Complexity of Change (inverted; red = high cost, green = low cost).
   - Heat-map color code: Red → Green gradient for visual prioritization.

2. **2×2 Scatter (Slide 3):** Prize (X) vs. Cost-of-Change (Y). Each initiative plotted. Quadrants labeled:
   - High prize / Low cost → **Phase 1 (Quick Wins)**
   - High prize / High cost → **Phase 2 (Build the System) or Phase 3**
   - Low prize / High cost → **Drop or defer**

3. **Phased Roadmap (Slides 4–5):**
   - **Phase 1** (Q1–Q4 Year 1) — "What are our quick wins?" — initiatives that deliver in 12 months with minimal organizational change.
   - **Phase 2** (Year 2) — "What builds the system?" — platform investments (new replenishment system, EPOS upgrade, BI tooling).
   - **Phase 3** (Year 3+) — "What's the end-state?" — cultural/capability shifts (board-level availability ownership, new operating model).
   - **Milestones overlay:** Align each phase with client's known programme deliverables (e.g., "Fusion Go-Live Q2-07", "CIPR1 / Release 3a Q3-07").

**Slide count in source:** 10 pages.

**Acceptance criteria for generated output:**
- Carries navigator ribbon "6" on every slide.
- Heat-map table visible with all recommendations scored on all five axes.
- 2×2 matrix shows prize × cost/complexity, with quadrant labels.
- Phased roadmap spans 8 quarters minimum (Q1 Year1 through Q4 Year2).
- Milestones named (e.g., "System Upgrade Go-Live") and plotted above phase bars.
- Phase 1 initiatives visibly distinct from Phase 2 (different coloring, grouping, or annotation).

---

### Section 7 — Prioritised Case for Action (Source: pp.99–102)

**Purpose:** The "why now" argument; executive trigger for commitment.

**Structure:**
1. **Slide 1: Case for Action narrative** — Why now? What is the strategic imperative? (2–3 bold opening sentences, then 3–4 supporting bullets).
2. **Slide 2: Risk of Inaction** — What happens if these initiatives are not executed? (Competitor positioning, margin erosion, market-share loss, org risk).
3. **Slide 3: Strategic Upside** — What is the 3–5-year end state if the roadmap is executed? (CSI, NPS, sales per sq-ft, labor efficiency percentile).
4. **Slide 4: Action Plan** — Pre-requisites (governance, resourcing, comms). Phase 1 quick-start checklist. Phase 2/3 governance gates.

**Slide count in source:** 4 pages.

**Acceptance criteria for generated output:**
- Carries navigator ribbon "7" on every slide.
- "Why now" grounded in one specific market fact or competitive move (not generic urgency).
- Risk narrative explicitly quantifies downside (e.g., "Failure to act: 2–3 point margin erosion, ~£5m EBIT impact").
- Upside narrative aligns to Section 3 baselines (e.g., "Move from 75th-percentile CSI to 90th; stock-turn from 2.1x to 2.8x").
- Action Plan checklist is enumerated and assignable (governance structure, owner roles, first 90-day milestones).

---

## Per-Section Slide Skeletons

### Universal Rules (all sections)

1. **Navigator ribbon:** Every slide must display 1–7 in top-right corner. Current section number highlighted or bolded.
2. **Source footer:** Every slide carrying data must carry a one-line source cite in footer (e.g., "Source: EPOS extract, 2006-03-15, Period: Q1–Q4 2005").
3. **Three-bold-callouts footer pattern:** Sections 3–6 close each content slide with three bold one-line takeaways (not data, but conclusions).
4. **Left-right column pattern (Sections 4–5):** Findings on left, Leading Practice on right (or Evidence on left, Recommendation on right). Column headers visible and consistent across all slides in section.
5. **Title pattern:** Section + theme + root-cause or topic. E.g., "4 — Availability: Replenishment Lead-Time Causes of Poor Availability."

### Navigator Ribbon Rule

- **Implementation:** SVG or shape element in top-right, 1.5cm × 0.5cm (est.), with seven circles/boxes. Current section filled or highlighted; others muted or outline-only.
- **Font:** 9–10pt, sans-serif (Arial or Calibri), muted gray unless highlighted.
- **Placement:** Consistent across all 102 slides in source; no variation.
- **Failure mode:** If ribbon is missing, slide is invalid. Skill must reject or repair.

### Prize-Sizing Table Rule

**Structure:**
```
| Driver / Cause | Low £ | High £ |
|---|---|---|
| Driver 1 | £Xm | £Ym |
| Driver 2 | £Am | £Bm |
| ... | ... | ... |
| **TOTAL** | **£Sum** | **£Sum** |
```

**Rules:**
- At least 3 drivers per theme.
- Low and High columns clearly labeled.
- Total row bolded and clearly summed.
- All ranges justified by 1–2-sentence narrative on same slide or referenced slide (e.g., "Replenishment: 10 days wasted per cycle × £1.5m annual sales = £10m–£15m range (conservative / aggressive assumptions)").
- Source cite for each number (e.g., "Replenishment lead-time: EPOS data; margin %: Q1–Q4 2005 GL; peer benchmark: RetailMeNot 2005 RFM").

---

## Numbered Navigator Ribbon Discipline

The source deck's navigator ribbon is the structural glue. Every slide must carry it.

**Rule:** If a slide is missing the ribbon, or if the ribbon is in the wrong position, or if the ribbon number does not match the section, the slide is invalid and must be removed or repaired before output.

**Enforcement:**
- Skill scans every generated slide's top-right quadrant for the ribbon SVG.
- If missing, logs warning and removes slide (or flags as defective).
- If present but wrong number, logs critical error and stops.
- If navigation carousel is present on Section 1 overview, it must match the slide count per section (e.g., Section 1 = ~23 slides → 23 dots in carousel).

---

## Prize-Sizing Pattern: Math Transparency

Every prize-size range must show its math on the same slide or a linked slide.

**Example (from source, Availability theme):**

| Driver | Calculation | Low £ | High £ |
|--------|---|---|---|
| Replenishment Lead-Time | Lost sales × margin. 14-day lead-time vs. 3-day best-in-class: ~£1.5m annual retail sales lost (conservative) to £2.2m (aggressive). Margin preservation 40–45% → £0.6m–£0.99m opportunity. | £10m | £15m |

**Rule:** If a number is stated without a method cite, the slide is invalid.

**Acceptance:** Both low and high range must be defensible from the input evidence pack. No made-up numbers.

---

## Theme Drill-Down Structure: 8–9 Root-Cause Slides per Theme

Each theme (Availability, Store Labour) must have:

1. **Overview slide (1)** — navigator + findings summary + prize callout.
2. **Prize slide (1)** — £ table + narrative.
3. **Root-cause drills (6–7 minimum)** — one per navigator entry. Findings / Leading Practice pattern.
4. **Recommendations block (1)** — numbered actions + 5-axis implementation challenges.

**Total per theme:** 9–10 slides (in source: Availability 27 pages ≈ 9 slides; Store Labour 22 pages ≈ 7 slides, allowing for multi-slide per root-cause).

**Acceptance:** Asymmetry is OK (one theme 8 slides, other 10) if justified by evidence depth. Symmetry is preferred (8–8, 9–9).

---

## Three-Phase Roadmap Pattern

Every roadmap must answer three sequential questions:

1. **Phase 1 (Q1–Q4 Year 1):** "What are our quick wins?"
   - 3–5 initiatives that can start in Q1 and deliver benefit in 12 months with minimal org change.
   - Example: Robust availability measure (process redesign, no tech); 72-hour customer-order lead-time (process + modest system config); store labour benchmarking (data analytics, no new platform).
2. **Phase 2 (Q1–Q4 Year 2):** "What builds the system?"
   - 3–5 initiatives requiring platform investment or organizational structure change.
   - Example: Advanced replenishment system (new platform); segmented replenishment model (process re-design + new system); BI tooling (analytics platform).
3. **Phase 3 (Year 3+):** "What's the end state?"
   - 2–3 strategic initiatives requiring cultural or capability shift.
   - Example: Board-level availability ownership (governance); new operating model (org re-design); multi-channel fulfillment network (strategic expansion).

**Milestones overlay:** Align with client's known programme calendar. E.g., "Fusion Go-Live (Q2-07)", "CIPR1 Release 3a (Q3-07)", "CIPR2 Go-Live (Q1-08)".

**Acceptance criteria:**
- Phase 1 initiatives visibly fast-track (duration ≤ 6 months, no major tech spend).
- Phase 2 initiatives visibly platform-dependent (duration ≥ 9 months, tech/ops spend quantified).
- Phase 3 initiatives visibly strategic or multi-year (duration ≥ 12 months, org/cultural dependencies noted).
- Milestones named and positioned above phase bars to show alignment.
- At least 8 quarters visible on timeline.

---

## Case for Action Structure

The final narrative must answer:

1. **Why now?** — One specific competitive or operational fact that creates urgency (not generic "optimization" language).
2. **Risk of inaction** — Quantified downside if initiatives are deferred (margin erosion, market-share loss, capability gap).
3. **Strategic upside** — 3–5-year end-state performance vs. current baseline (e.g., CSI: 75th → 90th percentile; Stock turn: 2.1x → 2.8x; Labor efficiency: 65th → 80th percentile).
4. **Action plan** — Enumerated pre-requisites (governance, resourcing, comms) and first-90-day checklist.

**Acceptance:**
- "Why now" not generic. Grounded in one named competitive move, regulatory change, or market shift.
- Risk quantification visible (e.g., "2–3 point margin erosion = £4m–£6m annual EBIT").
- Upside aligned to Section 3 baseline (not invented numbers; delta from current state).
- Action plan checkboxes assigned (owner, due date, success criteria).

---

## Mapping to the Canary Spine

This SDD codifies the Clarks method. Stage 3 applies it to the Canary Retail Spine for an archetype SMB specialty retailer (illustrative archetype, not a real client).

### Theme 1 — Availability (Canary's Loss Prevention Domain)

Maps to Canary's **Chirp** (Q) module: six escalating detection rules for lost sales risk:

- C-009 SQUARE_DELAY_HOLD — delayed settlement = cash flow risk + reconciliation error.
- C-104 AFTER_HOURS_DRAWER — unscheduled drawer activity = stock/cash loss.
- C-204 UNTENDERED_ORDER — merchandise not rung up = lost sales, margin.
- C-301 OFF_CLOCK_TRANSACTION — employee transactions off-record = inventory risk, theft risk.
- C-502 POST_VOID — canceled sale after close = reconciliation burden, margin loss.
- C-602 GIFT_CARD_DRAIN — unexplained gift card redemptions = fraud or loyalty-program leak.

**In Availability diagnostic:**
- Theme 1 root cause: "Visibility of sales & stock position" (e.g., delayed settlements hide true inventory position).
- Evidence: Chirp rule-fire rates, merchant thresholds vs. benchmarks, trend analysis.
- Leading practice: Automated chirp escalation, real-time EPOS integration, daily reconciliation.
- Recommendation: Implement Chirp baseline detection, escalate 4 rules to auto-investigation, establish 24h response SLA.

### Theme 2 — Inventory & Replenishment (Canary's Operational Intelligence Domain)

Maps to Canary's **v2 ring** gaps (Modules D + J):

- **Module D (Demand):** No perpetual ledger tie-out, no OTBI enforcement, no replenishment auto-trigger.
- **Module J (Journey):** No customer-order orchestration, no multi-channel fulfillment, no inventory visibility across locations.

**In Store Labour diagnostic:**
- Theme 2 root cause: "Inventory management process efficiency" (e.g., manual stock counts take 4 hours/week, no perpetual ledger reconciliation).
- Evidence: Store-level labor allocation, task-time data, shrink variance vs. peer benchmark.
- Leading practice: Perpetual ledger with daily EPOS tie-out, automated replenishment triggers, mobile fulfillment tools.
- Recommendation: Build Canary D + J pipeline (perpetual ledger, OTB enforcement, replenishment auto-trigger). Phase 2 project.

### Theme 3 (Future) — Margin Protection (Canary's Financial Intelligence Domain)

Not in source Clarks deck (out of scope), but foundational to roadmap Phase 2+3:

- Maps to Canary's **v3 ring** (Modules S + P): Sales margin analytics (S) + Pricing intelligence (P).
- Root causes: Promotional margin leakage, markdown velocity, pricing elasticity misalignment.
- Evidence: POS margin by category, promotional effectiveness, competitive pricing data.
- Leading practice: Real-time margin-by-transaction visibility, automated markdown recommendations, A/B price testing.

### Spine Ring Sequencing Alignment

| Phase | Canary Ring | Modules | Roadmap Activity |
|-------|---|---|---|
| Phase 1 (Quick Wins) | Existing + Q | Q only | Implement Chirp loss-prevention detection; establish baseline. ~3 months. |
| Phase 2 (Build the System) | v2 | D, J, F | Build perpetual ledger (D), customer-order fulfillment (J), real-time cash position (F). ~12 months. |
| Phase 3 (End State) | v3 | S, P, L, W | Sales margin analytics (S), pricing intelligence (P), long-term strategy (L), wholesale/multi-channel (W). ~24 months. |

---

## Acceptance Criteria for Deliverable

A Canary Retail Diagnostic produced by the skill is **done** when:

1. **7 sections complete** — all section headers (1–7) present, navigator ribbon on every slide.
2. **Section 1 (Executive Summary):** Summarizes Sections 2–7, prize roll-up visible, phased roadmap on one slide.
3. **Section 3 (Financial Baseline):** Sales, margin, stock-turn, CSI baseline established with peer benchmarks. All numbers dated and sourced.
4. **Section 4 (Theme 1):** 8–9 slides following Overview → Prize → N drills → Recommendations pattern. Prize table with 3+ drivers, low/high range, sum. All evidence cited to input data.
5. **Section 5 (Theme 2):** 7–9 slides, same pattern. Prize quantified.
6. **Section 6 (Opportunity Priorities):** Heat-map table with all initiatives scored on prize (3 axes) and cost (2 axes). 2×2 scatter plot visible. Phased roadmap spans 8+ quarters with milestones labeled.
7. **Section 7 (Case for Action):** "Why now" grounded in one named fact. Risk of inaction quantified. Upside aligned to baseline. Action plan enumerated.
8. **Output formats:** pptx (primary), docx (companion write-up, same 7-section structure).
9. **Fidelity checks:**
    - Opens in PowerPoint and Keynote without font fallbacks.
    - No placeholder text ("INSERT CLIENT NAME HERE", "TBD", etc.).
    - All tables render with visible borders and alignment.
    - All evidence bullets ≤ 80 chars per line (wrapping OK, but readable).
10. **Traceability:** Every fact carries footer cite. No unsourced claims.

---

## Related

- [[Brain/wiki/methodology-ibm-retail-diagnostic|Methodology · IBM Retail Diagnostic]]
- [[docs/sdds/consulting/SDD-consulting-skills|SDD · Consulting Skills]] (parent document)
- [[Canary-Retail-Brain/case-studies/canary-retail-diagnostic-archetype|Canary Retail Diagnostic — Worked Example (Archetype Specialty Retailer)]]
- [[Brain/projects/Method|Method MOC]]
- [[Brain/projects/Canary|Canary MOC]]

---

## Open Questions

1. **Evidence pack format (Stage 3):** Should the input evidence pack be JSON, YAML, or markdown? Recommend JSON with structured schema for financial metrics, transaction data, evidence notes.
2. **Merchant threshold mapping:** The source Clarks deck shows peer benchmarks for CSI, stock-turn, labor % of sales. Should the skill auto-map Canary merchant metrics to the same benchmarks, or require manual input?
3. **Multi-theme extension:** The source focuses on Availability + Store Labour (2 themes). Should the skill be designed to accept N themes (Margin, Supply Chain, etc.) with the same pattern, or lock to 2?
4. **Recommendation-to-action mapping:** Should each recommendation in Section 6 carry a "estimated cost" and "estimated duration" that feeds into Phase sequencing logic, or is that manual in v1?
5. **Canary integration depth:** Should the skill call Canary APIs to extract financial baselines (sales, margin, shrink) and transaction data directly, or require manual data-pack input?

