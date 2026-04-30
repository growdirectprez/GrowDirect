---
classification: internal
type: wiki
status: active
date: 2026-04-30
last-compiled: 2026-04-30
needs-review: 2026-05-30
source: PA LCB RFP 20060127 (April 2006); generalized via control-state structural analysis
tags: [canary, control-state, public-rfp, category-management, liquor, procurement, reference]
project: canary
---

# Control-State Liquor Procurement — Requirements Grid

Reference architecture for how a US control-state liquor authority procures category management, assortment, and merchandising services. Anchored on the Pennsylvania Liquor Control Board's 2006 RFP 20060127 — the most comprehensive publicly available example — with structural notes for generalizing to Wyoming, Utah, Idaho, Mississippi, and the other 13 control jurisdictions.

## Executive summary

A control-state liquor authority is, structurally, **a vertically integrated retailer running on procurement-code rails**. The buyer wants a defined product, not a relationship. They will pay for analytical clarity and methodological air cover; they will not buy open-ended consulting.

Three things define this buyer:

1. **They are sophisticated about their own operation but constrained by procurement code.** The PA LCB had been doing category management since 1997, ran a 20-store/20-control merchandising experiment in 2005, and re-clustered their stores in 2004 based on actual performance variance. The procurement document looks like checklist boilerplate; the underlying business is articulate.
2. **They buy fixed-fee, deliverables-based, with optional implementation phases.** Tasks 1–3 of the PLCB RFP are fixed-price for analysis. Task 4 (implementation PMO) is a rate card placeholder for downstream pull. This is not accidental — they are pre-positioning a sole-source rollout while keeping competition honest on the analysis fee.
3. **Audit and IP capture run through everything.** Audited annual financials during the contract term. Three-year post-payment record retention. Unrestricted state ownership of work product. Antitrust claim assignment. Contractor IP indemnity uncapped and time-unlimited. The cost of doing business with a control state is significant and largely invisible to first-time bidders.

For a SaaS platform vendor — Canary's posture — these RFPs translate as **surface contracts, not deep engagements**. The right move is to treat the procurement document as a description of the *outcome*, not the *delivery model*. Bid the platform as the delivery model; map the deliverables to platform output.

## What a control state actually is

Seventeen US jurisdictions exercise some form of state monopoly over alcohol distribution. Not all monopolies are the same:

| Jurisdiction | Wholesale | Retail | Notes |
|---|---|---|---|
| Pennsylvania | State | State | ~650 stores; largest control state by revenue |
| Utah | State | State | DABC (now DABS); ~50 state stores plus package agencies |
| Wyoming | State | License | Wholesale-only — state is sole importer/distributor of spirits and wine; private retail |
| Idaho | State | State | ~67 state-owned stores + ~120 contract stores |
| Mississippi | State | License | Wholesale-only |
| Montana | State | License | Wholesale-only with mixed private retail |
| North Carolina | State | Local | County/municipal ABC boards run retail under state wholesale |
| New Hampshire | State | State | NH Liquor Commission; turnpike-store model |
| Oregon | State | License (agency) | OLCC manages distribution + agent retail stores |
| Vermont | State | License (agency) | Agency stores, state-controlled assortment |
| Virginia | State | State | Virginia ABC; ~400 stores |
| Alabama | State | Both | ABC operates state stores alongside licensed private retail |
| Iowa | State | License | Wholesale-only (spirits) |
| Maine | State | License | Wholesale-only (spirits) |
| Michigan | State | License | Wholesale-only (spirits) |
| Ohio | State | License (agency) | Agency-store model under state wholesale |
| West Virginia | State | License (agency) | Agency-store model |

**The procurement posture is structurally similar across all of them.** Public-procurement boilerplate, conflict-of-interest screens, fixed-fee preference, audited financials, IP capture by the state. What varies is *what they procure*: wholesale-only states (Wyoming, Iowa, Maine, Michigan, Mississippi) buy demand planning, supplier-side category management, and warehouse optimization; full-stack states (PA, Utah, Virginia, NH) buy retail assortment, planogramming, and store-level execution.

For Canary's GTM, this matters: **the wedge into a wholesale-only state is supplier-relationship and warehouse, not store-level merchandising**. The wedge into a full-stack state is the same shape as a private retail chain, with public-procurement overhead.

## The procurement event — what to expect

PA LCB RFP 20060127 defined the canonical timeline. Most control-state procurements follow this rhythm with state-specific variation:

| Event | PA LCB | Typical range |
|---|---|---|
| RFP issuance | April 4 | Spring or fall, fiscal-year aligned |
| Optional site tour | April 25 | 2–3 weeks after issuance |
| Questions due | May 2 | ~30 days after issuance |
| Q&A response | May 12 | Mailed or posted to procurement portal |
| **Mandatory pre-proposal conference** | May 9 | **Failure to attend = automatic disqualification** |
| Proposal due | June 9, 1:00 p.m. | ~60–90 days after issuance |
| Selection target | within 120 days | 90–180 days |
| Contract term | 3 years base + 2 × 1-year options | 3–5 year rolling structure |

**The mandatory pre-proposal conference is the gate.** PA LCB is explicit; most control states match this. A bidder who skips the conference is excluded from consideration regardless of proposal quality.

**Twelve hardcopies, separately sealed cost submittal.** Mis-filing a cost number into the technical proposal disqualifies. Disadvantaged Business and Cost submittals are physically segregated in their own sealed envelopes. This is procurement hygiene — assume any control state runs this discipline.

**No travel reimbursement.** Buried in the standard terms. Monthly on-site working sessions in Harrisburg (or Cheyenne, or Salt Lake City) are absorbed into the loaded rate. A bidder who unloads travel as expense pass-through has misread the contract.

**Proposal bond.** $5,000 in PA. Modest, but its forfeiture is the contractual remedy for non-performance during the proposal phase. Standard in most control states.

## Scope of work — the anatomy of a category management deliverable set

The PA LCB Statement of Work is short and surgical — three required tasks plus an optional fourth. This is the canonical decomposition:

### Task 1 — Assortment methodology assessment

Two analytical reports:
- **Financial impact analysis of existing delisting methodology** — recommend changes
- **Financial impact analysis of existing core assortment methodology** — recommend changes

The phrasing is diagnostic. The buyer suspects their internal methodology is leaving money on the table; they want quantified evidence and an outside recommendation. They are *not* asking for a new methodology from scratch — they are asking the contractor to grade the work the merchant team already did.

### Task 2 — Space planning and shelf strategy

A bundle of methodology documents:
- Shelf-set strategy per display category, incorporating completed merchandising-test results
- Planogramming strategy with cost-benefit on alternatives, including warehouse/store-ops impact
- Category adjacency model — analysis approach plus cost-benefit
- Category right-sizing strategy with cost-benefit
- Optimal SKU count methodology by store size
- Wood-section vs. metal-section product placement strategy with downstream impact

The diagnostic tell: **"incorporating completed merchandising-test results."** PA LCB had already run the experiment. They wanted interpretation, not study design. A bidder who proposes a fresh test-and-learn loop has misread the buyer.

### Task 3 — Rollout and ongoing reporting

- Reset rollout strategy (which stores, when, in what order) with cost-benefit
- Guidance document or "manual" for stores to use during resets
- Quarterly financial impact reports on stores already reset
- Quarterly alternate-merchandising recommendations through end of contract

This task explicitly extends through the contract term. The contractor produces ongoing analytical deliverables on a quarterly cadence. This is the closest the base scope gets to "operational" — and it's still analysis, not operations.

### Task 4 (optional) — Implementation PMO

On-site project management at the agency's discretion. Hourly/daily rate card. **Costs not scored in the evaluation.** This is the lock-in vector — the agency reserves the right to retain the analyst as the implementer at the analyst's published rate, without rebidding.

### What's not in the base scope

- System integration work — not in scope, not asked for
- Software licenses — bidder must furnish their own; PLCB provides nothing
- Ongoing operational execution — explicitly carved out into Task 4
- New methodology design — the buyer wants validation and codification of internal direction, not transformation

## Mandatory technical and experience requirements

This is where the unsophisticated bidder gets eliminated.

| Requirement | What it means |
|---|---|
| All software, materials, equipment furnished by contractor | Bidder provides shelf-management software, workstations, network, everything. Agency provides nothing. |
| Detailed work plan with PERT diagram or equivalent | Visual project plan, hours per task, **percentage of agency staff time required** explicit |
| Statement of experience with shelf-management software, named | Bidder must name the package(s) — diagnostic for IT readiness and methodological discipline |
| Personnel data for every named professional | Resume, length of tenure, location during contract, percentage of time dedicated, plus turnover rates for HQ and field offices |
| Subcontractor disclosure with same depth as prime | No transparent pass-through; subcontractor relationships are visible in evaluation |
| Training plan with delivery modality | Hands-on / web / train-the-trainer — explicit |
| Objections to standard contract terms disclosed in proposal | **Failure to object waives the right.** Substituting bidder's own T&Cs is forbidden. One integrated contract only. |
| Cost submittal contains no assumptions | Caveats on scope can disqualify the proposal. Buyer wants a clean number. |
| 3 customer references with current contact info | Buyer reserves right to call any and all |
| 3 most recent audited annual financial statements | Unaudited statements require explanation |

**The experience bar is qualitative but pointed:**

- Experience in **category management** specifically — not general consulting
- Consultancy experience
- Experience in the **beverage alcohol industry** specifically
- Experience tied to **the individuals actually assigned**, not just the firm

A generalist consulting firm without direct beverage-alcohol category-management track record at the analyst level is at a structural disadvantage from page one of qualifications. This is a real moat for category-experienced bidders and a real hurdle for SaaS platform vendors entering the space.

## Audit and accountability obligations

Heavier than a private-sector engagement. Run through these line items before bidding:

- **Audited financial statements within 90 days of fiscal year-end** during the contract term — not just at proposal time
- **3-year post-final-payment retention** of cost/pricing records, with full and free access to Commonwealth representatives
- **Books, records, documents** available at contractor's office during reasonable times for inspection, audit, or reproduction by any authorized state representative
- **Reimbursement of state investigation costs** if those investigations result in suspension/debarment
- **Quarterly Disadvantaged Business utilization report** to BMWBO + Contracting Officer
- **15-day notification** of any suspension/debarment by any state or federal entity
- **Confidential Information** treatment with carve-outs for prior knowledge, independent development, lawful third-party acquisition, public domain
- **Prior approval required** for news releases, internet postings, advertisements regarding the project

This is the procurement-code shape of an audit relationship that lives for ~5 years past contract end. It is not optional, not negotiable, and not visible to a bidder who hasn't read the standard terms in Appendix Q.

## Pricing structure

Two-tier:

1. **Base scope (Tasks 1–3): fixed-fee, deliverables-based.**
   - Payment only on deliverable completion and agency acceptance
   - Monthly itemized invoices showing percent-complete by deliverable
   - Single consolidated invoice per month
   - CPI-W escalator with mandatory written application 15 days before contract-year end (or the increase is waived)

2. **Additional services + Task 4: hourly and daily rate card** by job classification.
   - Daily rate = 8-hour day
   - Applies to Project Change Requests and option-year work
   - Task 4 costs not scored in evaluation — pure rate sheet for downstream pull

**No travel or per diem reimbursement.** Rates absorb travel.

**Undisputed claims paid within 30 days.** Failure to pay accrues interest under PA Procurement Code (and most state procurement codes mirror this).

## Evaluation criteria

Five-factor evaluation. Cost is "weighted heavily" but not deterministic. Cost score is a ratio formula — `(lowest_bid / this_bid) × max_points`.

Technical scoring covers four sub-factors, in document order (which usually maps to weighted priority):

1. **Understanding the problem** — does the proposal demonstrate domain comprehension
2. **Proposer qualifications** — firm's CM track record + beverage alcohol experience + financial capacity
3. **Professional personnel** — named individuals' experience, with explicit emphasis on "service similar to that described in the RFP"
4. **Soundness of approach** — does the technical proposal meet objectives

Plus three non-technical factors:
- Disadvantaged Business participation (4-tier priority structure)
- Enterprise Zone Small Business participation (4-tier priority)
- Domestic Workforce Utilization — US-onshore labor scored highest

Oral presentations are discretionary. References will be checked. The agency reserves rejection rights for any "unqualified" proposer regardless of price.

## Things that surprised — non-obvious requirements

For first-time bidders, these are the landmines:

| Trap | What it costs you |
|---|---|
| Travel absorbed into rate | $20–60K of margin if you're flying analysts in monthly |
| Task 4 rate card unscored | Tempting to load rates high; competitors will too. The agency gets a fixed-fee analysis at competitive bid pricing and a rate-card implementation that's barely market |
| Antitrust claim assignment | Contractor assigns to agency any antitrust claims against its own suppliers — unusual outside federal procurement |
| Unrestricted state ownership of work product | No retention rights for the contractor. Cannot publish results, cannot use deliverables in marketing, without written permission |
| Patent/copyright indemnity uncapped and time-unlimited | "Continues without time limit." Insurance and risk-pricing implications. |
| Liquor Code conflict screen | No agency employee or immediate-family-of-employee can hold >5% in contractor or sub. Five-year bar plus felony exposure. Bench-level diligence required before bidding. |
| Audited financials annually during the term | Not just at proposal. Recurring cost for the contractor. |
| Pre-proposal conference attendance gating | Skip it, you're out. |
| "No assumptions" cost submittal | Industry-standard caveats can disqualify. |
| Pre-existing test results | Buyer has often already run the experiment. Proposing a fresh study is a misread. |

## What this RFP reveals about how the buyer thinks

This is a **sophisticated buyer wearing checklist clothes**. The procurement-division apparatus is heavy with state boilerplate — Disadvantaged Business priority ranks, Enterprise Zone preferences, Adverse Interest Act, ADA, contractor-integrity provisions — but the underlying business problem is articulate and self-aware.

What the RFP signals:

- **They want validation and codification, not transformation.** They have an internal CM organization and an ERP rollout in progress. The outside firm provides methodological air cover for changes their own organization already suspects need to happen.
- **They want a documented playbook.** The "guidance document or manual" deliverable is explicit. The contractor leaves behind something the agency can run going forward.
- **They want optionality on implementation.** Task 4 is structured to give the agency the option of retaining or self-executing, without rebidding.
- **They have been burned, or watched peers be burned, by open-ended consulting.** Everything about the structure — deliverables-based fixed fee, segregated cost submittal, audit rights, IP capture, optional implementation — is consistent with a buyer protecting against that pattern.

## Generalizing to Wyoming, Utah, Idaho

The PA LCB RFP is the most comprehensive control-state category-management procurement publicly documented. Smaller control states issue lighter procurement events, but the structural shape persists.

**Wyoming Liquor Division** (Wyoming Department of Revenue) is wholesale-only — state is sole importer and distributor of spirits and wine; retail is private. The category management deliverable shape shifts:

- **Out:** store-level shelf-set, planogramming, store reset rollout
- **In:** demand planning, SKU listing/delisting at the wholesale level, supplier-relationship management, warehouse slotting, allocation to private retailers
- **Same:** procurement-code overhead, audit rights, IP capture, fixed-fee preference, conflict screen
- **Different:** smaller scale (single warehouse vs PA's three), single-tier customer base (private retailers, not state stores), tighter staff (Wyoming Liquor Division is a department within Department of Revenue, not a standalone agency)

**Utah DABS, Idaho ISLD, Virginia ABC, NH Liquor Commission** — all run the full-stack model (state wholesale + state retail). Procurement documents from these agencies follow the PA pattern with state-specific overlay (Utah's procurement code, Idaho's procurement preferences, Virginia's ABC governance structure).

**The play across all of them:**

1. Read the agency's annual report and strategic plan first — they tell you where the buyer thinks they're weak
2. Watch the procurement portal for upcoming RFPs in the category — recompete cycles run 3–5 years
3. Treat the pre-proposal conference as a relationship-building event, not a checkbox
4. Build a beverage-alcohol category-management track record before bidding the first state — qualifications evaluation is brutal without it
5. Bid the platform as the delivery model — fixed-fee for the analytical deliverables, SaaS subscription for the ongoing reporting, separate scope for the implementation PMO

## Related

- [[canary-control-state-fit]] — accountability-rails-to-requirements mapping; thesis-fit analysis
- [[category-management-engagement-pattern]] — methodology pattern from the 2005-2006 enterprise consulting era; what to keep, what to discard
- [[platform-thesis]] — Canary mission and three accountability rails
- [[canary-canonical-positioning]] — what / who / how

## Sources

- `Brain/raw/inbox/pa-lcb-rfp20060127-pdf.md` — the RFP itself (raw intake)
- `Brain/raw/inbox/rfp20060127-ibm-questions-doc.md` — vendor Q&A submission
- `Brain/raw/inbox/-revised--rfp20060127-ibm-questions-doc.md` — revised Q&A
- `Brain/raw/inbox/clarifications-for-ibm-question-doc.md` — agency clarifications
- `Brain/raw/inbox/plcb--workplan-narrative-v1-doc.md` — vendor workplan narrative
- Public-source: National Alcohol Beverage Control Association (NABCA) member directory; control-state classification matrices
