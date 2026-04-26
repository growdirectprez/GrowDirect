---
type: sdd
status: v0.1-design
domain: consulting
component: it-architecture-options-methodology
date: 2026-04-24
owner: GrowDirect LLC
classification: confidential
tags: [sdd, consulting, it-architecture, ibm-bcs, methodology-as-code]
related:
  - Brain/wiki/methodology-ibm-it-architecture-options.md
  - docs/sdds/consulting/SDD-consulting-skills.md
  - case-studies/canary-finance-architecture-options.md
  - Brain/projects/Method.md
---

# SDD — Morrisons IT Architecture Options: Method as Executable Frame

## Purpose

Codify the IBM Business Consulting Services (2006) IT Architecture Options evaluation frame from the Morrisons deliverable as an SDD-driven artifact suite. This SDD itself is a **method artifact**, not a product feature. It serves as the reference specification for the `consulting:it-architecture-options` skill and documents the structural pattern that ensures any architecture decision (legacy vs. package vs. integrated) receives a fair, defensible, three-option comparison.

## Source Provenance

**Original deliverable:** Morrisons IT Architecture Options Final Review (IBM BCS, 2006). 104 pages; author-custodian Geoffrey C. Lyle (archive preservation; IBM era).

**Preserved in:** `/Users/gclyle/GrowDirect/Brain/wiki/methodology-ibm-it-architecture-options.md` (structural extract; client data redacted; methodology preserved in full).

**Use classification:** Methodology reference only. Structural pattern and evaluation frame are public-domain analytical practice; IBM's execution and proprietary heuristics are not re-disclosed. This SDD codifies only the frame.

## The Morrisons Eight-Section Skeleton

The deck's power comes from its invariant structure: **frame the problem once, evaluate three options symmetrically against that frame, recommend based on structured comparison.**

### Section 1: Introduction (Engagement context)
- Purpose of the engagement
- Stakeholder team composition
- Document structure roadmap
- Glossary of terms (tailored to industry)

### Section 2: Business Targets ("Optimisation" Programme)
**Critical anchor.** Client's explicit business objectives, typically quantified:
- Margin improvement (e.g., "up X basis points")
- Overhead reduction (e.g., "£Y cost-out by 2027")
- Headcount reduction (e.g., "£Z reduction in payroll")
- Sales growth (e.g., "W% annualized growth")
- Profit growth (e.g., "£V EBIT by year YYYY")

**Enforced rule:** Every architecture option's benefits are evaluated against these specific targets. No hand-waving; targets are the sizing anchor.

### Section 3: Business Requirements — Sell/Plan/Move/Buy Frame
**Shared process taxonomy.** Twelve operational process areas grouped into four value-chain phases:

| Frame | Process Areas | Examples |
|-------|---------------|----------|
| **Sell** | Sell Products, Serve Customers, Manage Branch | POS, eComm, CRM |
| **Plan** | Range Planning, Promotions Planning, Category Planning, Product Pricing | Markdown mgmt, assortment, price optimization |
| **Move** | Supply Chain Planning, Manage Replenishment, Physical Logistics | Forecasting, DC operations, transportation |
| **Buy** | Product Sourcing & Buying | Vendor negotiation, RFQ, PO issuance |

**Plus**: Reporting · Control · Processing overlay for Finance and HR (GL posting, payroll, audit).

**Usage rule:** This taxonomy is authored once, in Section 3. Every option's architecture is evaluated against it in two views (org structure, process flow). The merchant and IT leadership each see the frame they care about.

### Section 4: Implications for Legacy Systems
**Heat-map baseline.** Current-state application architecture evaluated against Section 2 (Optimisation) targets using a **4-color legend**:

- **Green:** Very good functional support — limited changes required
- **Yellow:** Good functional support — large number of small changes
- **Amber:** Good functional support — significant changes required
- **Red:** Poor or no functional support — major rewrite or replacement

**Two views:**
1. **Org-structure view** (Shop Systems / Distribution / Retail Ops / Trading / Finance / Reporting / IT)
2. **Process view** (Sell / Plan / Move / Buy + Finance/HR overlay)

Same data, two axes. Prevents one audience from seeing their landscape hidden in unfamiliar structure.

### Section 5–7: Option A, B, C — Seven-Slide Skeleton (Repeated)
Each option (A = Legacy Enhancement, B = Best-of-Breed Package, C = Integrated Package) is rendered identically:

#### Slide 1: Option Title + One-liner
Example:
- "Option A — Legacy Enhancement: Extend in-place, bespoke development, maximize existing investment"
- "Option B — Best-of-Breed: Integrate specialized packages; merchant remains the integrator"
- "Option C — Integrated Platform: Single vendor ERP/SaaS; eliminate integration"

#### Slide 2: Architecture vs. Optimisation Targets (Org View)
Heat-map: How well does this option's future-state architecture support the Optimisation programme targets (Section 2)?
Same 4-color legend. Same org-structure view as Section 4.

#### Slide 3: Architecture vs. Optimisation Targets (Process View)
Same data as Slide 2, rendered on Sell/Plan/Move/Buy axes.

#### Slide 4: Development Effort Estimate
Table (always in man-days / man-years):

| Application Area | Design | Build/Test | Dev Total | Roll-out | Total |
|---|---|---|---|---|---|
| (per system) | | | | | |
| **Total Man Days** | X | Y | Z | W | V |
| **Total Man Years** | | | | | N |

**Enforced rule:** Every estimate carries a footnote citing basis (e.g., "From interviews with IT leadership; EPOS excluded assuming 2 releases/year; 10% contingency embedded"). No estimates without provenance.

#### Slide 5: Architecture vs. Aspirational Targets (Org View)
Heat-map: If the client wants to evolve further (3–5 years out), does this option's design support it? Or does it paint the merchant into a corner?
Shift from Optimisation (near-term) to Aspirational (future-state).

#### Slide 6: Architecture vs. Aspirational Targets (Process View)
Same shift, same axes as Slide 3.

#### Slide 7: Advantages / Disadvantages + Target Architecture Diagram
**Left column:** 4–6 Advantages, evidence-grounded.
**Right column:** 4–6 Disadvantages, evidence-grounded.
**Below:** Target-state architecture diagram with legend: boxes labelled "Legacy Enhanced," "Rewritten," "Packaged," "Out of scope."

### Section 8: Summary and Conclusion
**Three pages; money section.**

#### Page 1: Architecture Comparison
Single slide with all three option target architectures rendered adjacent (left–right: A | B | C).
Rows: Sell / Plan / Move / Buy + Finance/HR. Columns: one per option.
Eye can compare box-for-box; no need to flip back to Section 5–7.

#### Page 2: Implementation Comparison
Three columns (A | B | C), each with bullets covering:
- Implementation timescale (e.g., "2 years" vs. "4 years")
- Risk of schedule overrun
- External resource dependency (is the merchant dependent on vendor availability?)
- Technology lock-in
- Phasing and modularity (can the merchant roll out in waves, or is it all-or-nothing?)
- Time to first measurable benefits

#### Page 3: Recommendation
**Single recommendation with explicit reasoning:**
- Named chosen option (A, B, or C)
- Phasing sequence (which modules / process areas first)
- Major decision gates (where the merchant can re-evaluate)
- Resource commitment (headcount + budget, internal + external)
- First-90-day actions

**Enforced rule:** Recommendation explicitly maps back to Section 2 business targets. "We chose B because it delivers the margin target by Q3 2027 while keeping headcount flat, whereas A overruns and C locks us into a 5-year cycle."

## Why This Structure Endures

Four properties that make the methodology durable:

### 1. Frame Predates Options
Section 3 (Sell/Plan/Move/Buy) and Section 4 (legacy heat-map) are authored **once**. Every option is then evaluated against that frame — same process taxonomy, same heat-map legend, same estimation schema. The merchant cannot be sold a story where one option is evaluated on criteria another isn't.

### 2. Two-Axis Heat-Maps
Every option's architecture is rendered twice — org-structure view and process view — so different reader audiences (IT leadership vs. business leadership) each get the frame that matters to them. Analyst work is not duplicated.

### 3. Dual Time-Horizons
Every option is evaluated against both **Optimisation targets** (the programme running now) and **Aspirational targets** (where the business wants to be in 3–5 years). This prevents a "cheap now, dead-end later" option from winning on cost alone. The merchant sees both horizons and can judge trade-offs.

### 4. Side-by-Side is the Only Judgment
The recommendation slide is the **only place** the analyst renders an opinion. Everything prior is structured, symmetric, defensible frame. The merchant is given the analytical scaffolding and then told, on one page, which leg of it to pick. No hidden scoring; all evidence is visible before the judgment.

## Acceptance Criteria

An SDD-conformant Morrisons-pattern deliverable must:

- [ ] Include all eight sections in order
- [ ] Section 2 cites specific, quantified business targets
- [ ] Section 3 renders the same process frame (default: Sell/Plan/Move/Buy) that all options are evaluated against
- [ ] Section 4 is a heat-map with two views; heat-map legend is 4-color (Green/Yellow/Amber/Red)
- [ ] Sections 5–7 render exactly seven slides each, in the order listed above
- [ ] Every Slide 2, 3, 5, 6 uses the same process taxonomy and heat-map legend
- [ ] Every Slide 4 effort estimate includes a footnote citing basis
- [ ] Section 8, Page 1 renders all three architectures on aligned process rows (same Sell/Plan/Move/Buy rows)
- [ ] Section 8, Page 3 recommendation explicitly maps to Section 2 targets
- [ ] All facts carry source footnotes
- [ ] Appendix includes glossary and methodology attribution (IBM BCS 2006, custodian Geoffrey C. Lyle)

## Mapping to the Consulting Skills Ecosystem

This SDD specifies **what** the `consulting:it-architecture-options` skill enforces. The skill:

- Accepts as input: client systems inventory (CSV/JSON), business targets, Optimisation/Aspirational requirements, option definitions
- Scaffolds Sections 1–8 with the seven-slide skeleton enforced per option
- Auto-generates heat-maps (Section 4, Slides 2–3, 5–6) from systems inventory and requirements
- Populates effort-estimate tables with pluggable heuristics
- Renders the side-by-side summary (Section 8) from the three option scaffolds
- Refuses to render a fact without a source footnote
- Outputs pptx + companion docx

The analyst (human or agent) fills in evidence, reasoning, and judgment; the skill enforces the frame.

## Open Questions

- **Q-1:** Should Aspirational requirements (Section 3–5 slides) be mandatory, or optional for shorter engagements? Current rule: mandatory. Revisit if a real engagement has tight scope.
- **Q-2:** The effort-estimate heuristics (man-days per application area per activity) are parameterized in the skill's config. How frequently are these calibrated against actual engagements? Plan: annual refresh post-dogfood.
- **Q-3:** The four-color legend has served retail IT for 20 years (Morrisons, 2006 to present). Is there a better heat-map semantics for other industries (SaaS, manufacturing, fintech)? Current answer: use the same legend; change the application labels.
- **Q-4:** Should the skill support a fourth option (e.g., "hybrid / phased")? Current design: no; three options force a crisp choice. Revisit if merchant demands greater optionality.

## Related

- [[Brain/wiki/methodology-ibm-it-architecture-options|Methodology · IBM IT Architecture Options]]
- [[case-studies/canary-finance-architecture-options|Case Study · Canary v2.F Finance]]
- [[docs/sdds/consulting/SDD-consulting-skills|SDD · Consulting Skills]]
- [[Brain/projects/Method|Method MOC]]
