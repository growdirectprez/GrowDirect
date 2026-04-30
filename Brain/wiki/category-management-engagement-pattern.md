---
classification: internal
type: wiki
status: active
date: 2026-04-30
last-compiled: 2026-04-30
needs-review: 2026-05-30
source: PLCB workplan narrative + 3 SOWs from a 2005 national sporting-goods chain merchandise planning PMO; pattern extracted, parties scrubbed
tags: [canary, category-management, methodology, engagement-model, consulting-pattern, reference]
project: canary
---

# Category Management Engagement Pattern (2005–2006 Enterprise Era)

The structural pattern that big consultancies used to deliver retail category management and merchandise planning engagements in the mid-2000s — what survives, what gets thrown out, and how it maps to a SaaS platform's onboarding model. Source material: a public-sector liquor authority workplan plus three versions of a Statement of Work for a national sporting-goods chain merchandise-planning PMO. Names scrubbed; structure preserved.

## Executive summary

The engagement pattern that produced these documents is the legacy shape Canary inherits and disrupts. The structural keepers are real and worth importing: **phased gates, a two-side joint PMO, fast SLAs, wave-based delivery, written risks-and-assumptions, operational handoff as exit criterion**. The discardable patterns are the commercial ones: **billable-hour economics, heavy paper artifacts, three-party vendor triangle, ceremonial governance, methodology-as-services**.

The consultancy's real product in this era was *governance and methodology*, not software and not analytics. The analytical deliverables were the artifacts; the engagement model was the IP. Canary inverts this — **the platform is the methodology, and the configured platform is the deliverable**. But the rhythm of how a multi-store retailer absorbs a new way of working is unchanged since 2006. Borrow the rhythm. Throw out the rate card.

## The engagement shape — one-paragraph thesis

Multi-store retailers know assortment and space planning are broken but cannot self-diagnose or self-implement the fix. The engagement arc moves from **current-state diagnosis → future-state methodology → phased implementation plan → operational handoff**. Three parties are constant: the **retailer** (sponsor + business SMEs + IS), the **consultancy** (methodology, PMO leadership, SME muscle), and the **software vendor** (in this era: JDA/Intactix for space, separate tooling for assortment). Success looks like a working planogram cycle, a documented assortment methodology, and a client PM who can run the next wave without the consultancy in the room.

## Phase structure

Two divergent shapes in the source material. Both are valid; they're optimized for different buyers.

### Public-sector workplan (PA LCB)

Four phases over ~9 months. Assessment-heavy and recommendation-terminal.

| Phase | Focus | Key deliverables | Decision gate |
|---|---|---|---|
| Project Discovery | Current-state baseline, stakeholder mapping, governance setup | Detailed work plan, governance model, current-state process map | Sponsor sign-off on charter |
| Assortment Planning Assessment | Delisting + core assortment methodology evaluation | Delisting Procedure report, Core Assortment Methodology report | Methodology approval |
| Space Planning Assessment | Planogramming, adjacencies, shelf-set, SKU count, category right-sizing | Shelf Set Strategy, Location SKU Count methodology, Category Right-Sizing methodology, Wood Shelf Product Placement Strategy | Future-state design approval |
| Project Rollout | Implementation plan + handoff | Future State Implementation Plan, recommended follow-on activities | Plan accepted; engagement ends or extends |

### Private-sector SOWs (national sporting-goods chain, ~400 stores)

Three SOWs, written sequentially as the engagement matured. Delivery-heavy and wave-iterative.

| SOW | Window | Hours | Fee | Focus |
|---|---|---|---|---|
| Sept 16 v1 | ~6.5 weeks | 280 | (blank) | Project charter, system info flow diagram, 2005 plan, 2006 rollout strategy, budget estimates |
| Sept 27 v2 | ~6.5 weeks | 306 | $82,000 | Same scope, business case + benefit metrics carved out to separate SOW; charter promoted to primary deliverable |
| Nov 3 v3 | 13 weeks | 519 | $139,800 | Wave 1 launch support + transition of PMO leadership to newly hired client PM |

**The delta between the two shapes.** Public-sector procurement rewards thorough assessment with clear deliverables that survive an audit; private-sector clients want the consultancy out of the chair as fast as possible because the burn rate is theirs. The public-sector phases describe *what to think about*. The private-sector SOWs describe *what to ship and when*.

For a SaaS platform, the right hybrid is **delivery-heavy public-sector phases**: the four-phase shell (Discovery → Assessment → Design → Deploy/Transfer), but with each phase's deliverable being a *configured platform state* rather than a strategy document.

## PMO and governance model

Day-to-day mechanics, distilled across all four documents:

- **Joint PMO structure.** Two part-time client PMs (one business, one IS) paired with a single consultancy program manager. By Wave 1 of delivery, this graduates to one full-time client PM.
- **Working teams** organized by domain: business process, data/interface (application development), technical infrastructure, change management (org change + communications + training).
- **Status cadence.** Weekly status reports submitted by the consultancy PM to the client PM. Regular status meetings on a fixed cadence. Checkpoints at phase boundaries with named executive participants.
- **Decision rights.** Three named executives "available for project planning checkpoints, approach sign-offs, deliverable evaluations." That's the steering-committee surrogate — a three-person executive panel, not a 12-seat ceremonial committee.
- **Escalation path.** **Three-day SLA on assumption breaks** before escalation. **24-hour SLA** on urgent information requests and on deliverable approvals.
- **Joint workshop pattern.** Cross-functional teams convened in dedicated scrum/conference rooms with whiteboards and flip charts to gather requirements, validate documentation, evaluate solutions. The workshop is the unit of work, not the analyst's desk.

The consultancy earned its keep here: imposing cadence, enforcing SLAs, running the workshops, owning the change-control procedure.

**For Canary:** the joint-PMO shape, the SLAs, and the workshop-as-unit-of-work all transfer cleanly. A two-person client side (one business owner + one ops/IS lead) plus a Canary deployment lead is the same shape, scaled to SMB. Twenty-four-hour SLAs on data pulls and deliverable acceptance is **competitive differentiation** at the SMB price point — most SaaS vendors run on best-effort cadences.

## Roles and staffing

### Consultancy side — lean by design

| Role | Hours range | Pattern |
|---|---|---|
| Engagement Partner | 6–40 hrs total | "As needed" — relationship and escalation |
| Program Manager | 240–495 hrs | The workhorse role, full duration |
| Senior Consultant | (rate-card only) | $215/hr; reserved for change-order overflow |
| Consultant | (rate-card only) | $170/hr; reserved for change-order overflow |

The named bench was small. Most analytical headcount lived on the client side or got pulled in via change order.

### Client side — where the real headcount lives

- Three named executive sponsors with sign-off authority
- Two part-time PMs (business + IS), graduating to one FT PM
- Dedicated team leads: business process, data/interface, technical infrastructure, change management
- Single point of contact for scheduling
- One analyst with strong Excel + financial-data fluency for business-case modeling
- IS resources for data extract / cleanse / convert
- Subject-matter experts pulled from Merchandise Planning, Assortment & Replenishment, Store Operations, Finance, Strategy, HR, Training

### RACI shape

| Activity | Consultancy | Client | Software vendor |
|---|---|---|---|
| Methodology, templates, governance mechanics, status discipline | **R/A** | C/I | I |
| Deliverable creation | C | **R/A** | I |
| Decisions and post-engagement run | I | **R/A** | I |
| Technical fit, sizing, integration | C | C | **R/A** |

This is a **deliberate design**: the consultancy is not on the hook for the artifacts, only for the process that produces them. It limits liability and forces client ownership. Quote from the Sept 27 SOW: the consultancy will assist by "providing guidance and sample templates rather than being responsible for deliverable creation."

**For Canary, this RACI inverts.** SaaS reverses the liability model: Canary IS responsible for the configured deliverable (the working assortment, the working POS integration, the running planogram). Own the artifact, not just the process. This is a structural advantage; don't rebuild the consulting RACI.

## Deliverable taxonomy

Across the four source documents, deliverables sort into four categories. Mix differs by buyer type.

| Category | Public sector | Private sector |
|---|---|---|
| **Analytical** (data + reports) | Delisting Procedure report, Core Assortment Methodology report | System Information Flow Diagram, High-Level Functionality Gap Assessment, List of Operating Business Decisions |
| **Methodology** (frameworks + playbooks) | Shelf Set Strategy, Location SKU Count methodology, Category Right-Sizing methodology, Wood Shelf Product Placement Strategy | Project Charter, operating guidelines, deliverables-and-storage framework |
| **System** (configs + integrations) | Implicit; not direct outputs | Intactix functionality fit assessment, data flow design, database sizing, technical-architecture estimates |
| **Operational** (run-the-business handoffs) | Future State Implementation Plan, recommended follow-on activities | 2005 Project Plan, 2006 Roll-Out Strategy, budget estimates, transition of PM role |

**The delta.** Public-sector mix is heavy on methodology — six of seven deliverables are framework-style strategy documents. Private-sector mix is heavy on operational — charters, plans, budgets, transitions. Public-sector buyers want a documented future-state to defend; private-sector buyers want a working schedule and a budget number.

**For Canary, both should collapse to System.** The methodology is documented *in the system*, not *next to* the system. A "Shelf Set Strategy" as a Word document is a 2006 deliverable; the 2026 equivalent is a configured planogram running in production with a one-page operating note.

## Risk and assumption language — what fails

Risks repeat across all three SOWs with growing maturity:

| Risk | Appears in |
|---|---|
| Decisions not made in a timely manner | All three |
| Key personnel and resources not available during critical times | All three |
| Delays getting necessary documentation and data | All three |
| Personnel reluctant to change or not on board | All three |
| Alignment of client, software vendor, consultancy methodology and approaches | Sept 27 onward (added during planning sprint) |
| Current budget constrains scope | Nov 3 (added at delivery start) |
| Scope not clarified and managed | Nov 3 |
| Benefits not clearly defined | Nov 3 |

**What this tells you.** Engagements of this shape fail in four ways: **decision latency, resource starvation, data unavailability, and political resistance** — in roughly that order. The Nov 3 additions reveal that by Wave 1, scope creep and undefined benefits had become salient. The consultancy was protecting itself in writing as the client's commitment ambiguity became visible.

Risks-and-assumptions sections in this era of consulting are not analytical artifacts; they are **legal positioning for the inevitable change order**.

**For Canary:** every deployment SOW (or its SaaS-MSA equivalent) should carry a risks-and-assumptions section that addresses the same four failure modes. Not legal CYA — diagnostic clarity for both sides. The retailer who reads "delays getting data is a risk" before signing is a different retailer than the one who discovers it on Day 30.

## Pricing, change-control, commercial structure

The 2005–2006 commercial bones:

- **T&M, not fixed-fee.** All three SOWs explicitly: "This project will be conducted on a time and materials basis." The dollar figure was an *estimate* with explicit "any estimate is only an estimate" hedging.
- **Published rate card.** Project Partner $360 / Program Manager $265 / Senior Consultant $215 / Consultant $170 (2005 rates).
- **Hour-bound staffing tables.** Each SOW lists positions, estimated hours, and duration. The bill is bounded by the hours, not by deliverable acceptance.
- **Change control via Master Services Agreement Section 10.3.1.** All scope deviations route through one named procedure. Three-day SLA on assumption-break resolution before escalation.
- **Phase-by-phase SOWs, not one umbrella contract.** Each SOW was 6 weeks, 6.5 weeks, 13 weeks. "This document amends the prior SOW dated September 27, 2005." Re-papering at every phase boundary is the commercial discipline — preserves optionality, narrows scope as learning accumulates, lets pricing reset.
- **Expense pass-through** at policy rate (48.5¢/mile, public-transport actuals, T&L at cost).
- **Completion criteria** = deliverables accepted *or* either party terminates. No retainer-style perpetual engagement.

**The commercial structure was T&M with phase-gate optionality.** This is a defensible model for an unknown-scope engagement, and indefensible for a productized one. Canary's revenue should be SaaS-recurring with a one-time deployment fee bounded by scope, not hours. Don't sell the methodology as billable services — the methodology is product.

## Version-to-version delta — the story the diff tells

Sept 16 → Sept 27 → Nov 3. Each version narrows scope, hardens assumptions, re-prices.

**Sept 16 v1.** Aspirational scope. Includes business case, financial modeling, ROI validation. Two roles, 280 hours, dollar amount blank ("$xxx"). Risks list short (4 items). Flags the software vendor, mentions the platform, says benefits will be developed.

**Sept 27 v2.** Scope narrowed. Business case, financial modeling, success criteria, benefit metrics **explicitly carved out** to "a separate SOW." Project Charter promoted to primary deliverable. Hours up to 306, fees firmed at $82,000. New risk: "Alignment of client, vendor, consultancy methodology" — the consultancy realized during the planning sprint that three-way alignment was harder than anticipated. Conference-room/scrum-room facility added to assumptions. Assumptions tightened on PM skill-set requirements (now four explicit competencies A–D).

**Nov 3 v3.** Engagement extended into delivery. Scope shifted from "develop charter and plan" to "support Wave 1 launch + transition PM role." Duration jumped from 6.5 weeks to 13 weeks. Hours to 519. Fees to $139,800. Named the new client PM — meaning the *transition target* was hired during the planning sprint. Two new risks: budget constraining scope, benefits not clearly defined. Holiday calendar baked into schedule. Assumptions added around dedicated team leads for process, data, infra, change management.

**The pattern.** First SOW promises everything. Second SOW carves out the politically difficult work. Third SOW shifts from planning to wave delivery + handoff once the client hires their own PM. **Don't fight scope at signing — move it to the next SOW.** This is the canonical consultancy pattern.

For Canary's deployment model, this maps to **wave-based onboarding with explicit milestone gates**. Pilot store → second wave → full chain. Each wave gets its own milestone. Scope that doesn't fit the current wave moves to the next wave, not into an open-ended bucket.

## What's transferable to a Canary-style platform engagement

### Keepers — import these

- **Phased onboarding with explicit gates.** Even a SaaS deployment benefits from a Discovery → Design → Deploy → Transfer arc. "Self-serve" is a myth at the SMB-to-mid-market level. The four-phase shell is sound.
- **Joint working-team structure.** A two-person client side (one business + one ops/IS) plus a Canary deployment lead is the same shape, scaled down. Role definitions (process, data/interface, change management) map directly.
- **Twenty-four-hour SLA on urgent decisions and approvals.** Differentiation at the SMB price point.
- **Status cadence + checkpoint architecture.** Weekly status, named executive checkpoints at phase boundaries. Rebrand as "Wave Reviews" — the mechanic is the same.
- **Risks/assumptions as commercial positioning.** Diagnostic clarity for both sides.
- **Wave-based delivery with re-papering.** Plan → Wave 1 → Wave 2+ maps cleanly to multi-store onboarding.
- **Client-side PM transition as success criterion.** Cleaner exit definition than "configuration complete." Operational, not technical.

### Anti-patterns — do not bring forward

- **Armies of analysts.** The 2005 model assumed cheap junior labor was a feature. SaaS economics destroy that assumption. CATz should be a thin operator + the platform, not a PMO with a $170/hr consultant rate card.
- **Fixed-price methodology lock-in (or its T&M cousin).** T&M billing for methodology delivery is a 2005 commercial structure. Canary's revenue is SaaS-recurring with a bounded deployment fee.
- **Heavy paper artifacts as deliverables.** The 2026 equivalent of "Wood Shelf Product Placement Strategy" is a configured assortment in the platform itself — running config, not a strategy doc.
- **Three-deep executive checkpoint culture.** Three named executive sign-offs at every phase gate works for a $50M retailer's 9-month engagement. For a $5M retailer's 6-week onboarding, one executive sponsor + the operator is enough. Scale governance to engagement size.
- **JDA-style vendor triangle.** The 2005 model bakes in a third party (the software vendor) as a co-equal participant. Canary IS the software vendor *and* the methodology owner — collapse the triangle into a two-party engagement. Don't rebuild it by partnering deep on tooling.
- **Consultancy off the hook for deliverables.** SaaS reverses this. Canary owns the artifact, not just the process.

## The CATz alignment

Canary's CATz method (the documented engagement framework) is the natural inheritor of this pattern, with the corrections applied. The structural keepers map to CATz phases:

| 2005 phase | CATz equivalent | Difference |
|---|---|---|
| Project Discovery | Discovery + Onboarding | Replaces work plan with platform configuration |
| Assortment Planning Assessment | Assortment design (configured in Canary) | Output is running assortment, not Word doc |
| Space Planning Assessment | (Out of scope — Canary is not a planogram tool) | Refer to JDA/Intactix-class partner |
| Project Rollout | Wave deployment + handoff | Operator takes over by end of Wave 2 |

The CATz method is in some sense the 2005 enterprise pattern, productized and stripped of the billable-hours economics. It works because the underlying rhythm of how a multi-store retailer absorbs a new way of working hasn't changed. What changed is who delivers it and how it's priced.

## Related

- [[control-state-procurement-requirements]] — public-sector procurement structure; PA LCB anchor
- [[canary-control-state-fit]] — accountability-rails-to-requirements mapping
- [[canary-canonical-positioning]] — what / who / how
- [[platform-thesis]] — Canary mission and three accountability rails

## Sources

- `Brain/raw/inbox/plcb--workplan-narrative-v1-doc.md` — public-sector workplan (raw intake)
- `Brain/raw/inbox/ibm---tsa-merch-plan-pmo-sow-091605v2-doc.md` — private-sector SOW v1 (raw intake)
- `Brain/raw/inbox/ibm---tsa-planning-pmo-sow-092705-doc.md` — private-sector SOW v2 (raw intake)
- `Brain/raw/inbox/ibm---tsa-planning-pmo-sow-110305-doc.md` — private-sector SOW v3 (raw intake)
