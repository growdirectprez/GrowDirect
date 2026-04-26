---
type: wiki
status: active
date: 2026-04-26
owner: GrowDirect LLC
tags: [catz, methodology, retail, consulting, engagement, canary, phase-1, phase-2]
related:
  - Brain/wiki/canary-platform-overview.md
  - Brain/wiki/retail-merchandise-planning-otb.md
  - Brain/wiki/retail-promotion-workflow.md
  - Brain/wiki/retail-po-from-plan.md
  - Canary-Retail-Brain/modules/
source-vault: /Users/gclyle/CATz
last-compiled: 2026-04-26
needs-review: 2026-05-10
---

# CATz — Counterpoint Architecture & Transformation Method

## Governing Thesis

CATz is GrowDirect's two-phase engagement model for specialty retail transformation. It compresses Big-4-grade advisory discipline — diagnosis, architecture evaluation, vendor selection — into a format an SMB retailer can absorb in weeks rather than months, and lands on Canary Retail as the runtime, not a deck. The engagement doesn't end with a recommendation; it ends with a running platform. That is what makes it different from consulting.

---

## The Two Phases at a Glance

```
Phase I — Assess & Design
  ↓ 10 parallel workstreams
  ↓ Output: signed decision (vision + business case)

Phase II — Select & Implement
  ↓ 6 workstreams (sequential-with-parallelism)
  ↓ Output: signed vendor contract + funded implementation plan

Phase III — Implementation (separate, vendor/SI-driven, CBM v2 governance overlay)
```

| | Phase I | Phase II |
|---|---|---|
| **Question answered** | What is the operating reality and what is the prize? | What's the right system path and how do we commit? |
| **Duration (SMB)** | 2–4 weeks compressed | 4–8 weeks |
| **Duration (mid-market)** | 6–10 weeks | 8–14 weeks |
| **Exit gate** | Steering committee signs vision + business case | Contract executed, SOW signed, funding approved |
| **Primary deliverable** | Retail Diagnostic deck | IT Architecture Options deck + vendor contract |

---

## Phase I — Assess & Design

Ten workstreams run in parallel. Each produces its own artifact trail.

| # | Workstream | What It Produces | When |
|---|---|---|---|
| 1 | Executive Interviews | Per-executive analysis + compilation + summary | Wk 1–2 |
| 2 | Field Visits | Per-store visit reports + compilation | Wk 1–3 |
| 3 | As-Is Workshops | One as-is deck per business domain | Wk 2–5 |
| 4 | Executive Visioning | Target operating state in presentation + doc form | Wk 3–5 |
| 5 | Benchmarking | KPI comparison vs. industry peers (margin, turn, GMROI, labor) | Wk 2–4 |
| 6 | Balanced Scorecards | Scorecard applied to current state (financial / customer / process / learning) | Wk 3–4 |
| 7 | Quantitative Analysis | 4–6 focused analyses, each answering one question from the data | Wk 2–5 |
| 8 | Business Case | Benefits case + cost model + NPV synthesis + solution-to-value traceability | Wk 4–6 |
| 9 | Presentations | Numbered, dated, Final-marked SC decks; steering committee every 2 weeks | Continuous |
| 10 | Change Management | Readiness assessment + stakeholder plan + communications plan | Wk 2–6 |

**Business domains covered in As-Is Workshops:** Commercial, Supply Chain, Finance, Store Ops, Space/Range/Display, People/Labor, Property/Assets, Loss Prevention, Technology.

### Phase I exit criteria

Phase I does not close until all five conditions are met:

1. Vision signed by steering committee
2. Business case signed (benefits, cost, NPV all validated)
3. Phase II scope defined
4. Change-readiness assessment complete
5. Executive sponsor confirms "proceed"

Compressing Phase I by skipping the sign-off is a documented failure mode. The method forces the gate.

---

## Phase II — Select & Implement

Six workstreams, sequential-with-parallelism.

| # | Workstream | What It Produces | When |
|---|---|---|---|
| 1 | To-Be Workshops | One to-be deck per domain in scope | Wk 1–3 |
| 2 | RFP Package | Per-vendor RFP + attachments + legal appendices; every vendor receives identical package | Wk 2–4 |
| 3 | RFP Responses | Per-vendor folder (response + EULAs + escrow agreements + per-domain answers) | Wk 4–8 |
| 4 | IT Architecture | Target architecture diagram + transition plan + integration architecture + NFRs | Wk 2–8 |
| 5 | Scorecard & Shortlist | Scored comparison, shortlist rationale, finalist recommendation | Wk 8–10 |
| 6 | Contract Negotiation | Executed agreement + signed SOW + implementation funding approved | Wk 10–14 |

IT Architecture (workstream 4) runs in parallel with vendor RFPs deliberately — the architecture must not be vendor-driven.

### Phase II exit criteria

1. Vendor selected and contracted
2. Implementation SOW signed
3. Implementation funding approved
4. Target architecture signed
5. Cutover plan agreed
6. Handoff to implementation team documented

---

## Two Signature Deliverables

CATz ships as two agent-powered consulting skills.

### Retail Diagnostic (Phase I output)

A 7-section diagnostic deck structured to be read standalone by a board.

| Section | Content |
|---|---|
| 1 | Executive Summary — full deck in miniature, prize-sizing roll-up, phased roadmap |
| 2 | Background, Scope & Approach |
| 3 | Financial Analysis & Industry Drivers — every number source-cited |
| 4 | Theme 1 — Findings & Observations (drill pattern) |
| 5 | Theme 2 — Findings & Observations (drill pattern) |
| 6 | Opportunity Priorities & Roadmap — 2×2 matrix (Prize × Cost-of-Change) |
| 7 | Prioritised Case for Action — Phase 1 (quick wins), Phase 2, Phase 3 |

**The repeating drill pattern** (applies to every theme, every time):
1. Theme Overview slide — summary findings + root-cause navigator + three bold callouts
2. The Prize slide — low/high quantification table with method cite
3. Per-root-cause drill slides — Findings (data-anchored) + Leading Practice (best-in-class) + three callouts
4. Recommendations slide — numbered list bound to root causes + implementation challenges across five disciplines (People / Process / Technology / Financial / 3rd Parties)

The prize is never stated without a low/high range. The range is never stated without a method cite on the same slide.

### IT Architecture Options (Phase II bridge)

An 8-section multi-option evaluation deck. Three architectural paths evaluated symmetrically — typically: enhance legacy, best-of-breed package, integrated package.

**Per-option slide skeleton** (every option, same seven slides):
1. Application architecture heat-map — 4-color legend (full / partial / gap / not applicable)
2. Aspirational heat-map — same structure, against future-state processes
3. Development effort estimate — design days + build-test days + rollout days = man-years
4. Target application architecture
5. Advantages / Disadvantages
6. Implementation timeline and risk — phased plan with named milestones
7. Resource / sourcing plan — FTE and skills breakdown

**Decision matrix (section 8):** rows are decision dimensions (fit to targets, requirement coverage, effort, timeline, cost, risk, strategic flexibility, capability change required); columns are the options. Recommendation is the last row, filled after the evidence in the preceding rows is complete.

---

## Two Novel Roles

### Data Detective

Translates a retailer's heterogeneous data — POS exports, spreadsheets, legacy system extracts, invoice archives, interview notes — into GrowDirect's canonical retail data model (People × Places × Things × Events × Workflows).

**Delivers:** data map (every source, format, custodian, cadence), source-to-canonical mapping, structured evidence pack (JSON input for both skills), gap register (severity-rated: blocks / degrades / nice-to-have).

**Critical anti-pattern:** accepting "we have ten years of data in this system" at face value. The Data Detective verifies completeness, consistency, and accessibility — not just system age. The gap register is what makes the diagnostic defensible.

### Digital Plumber

Wires the source-to-canonical mappings into the runtime integration layer. Builds connectors with idempotency, observability, and runbooks.

**Delivers:** connector inventory (type, auth, cadence, owner), idempotency and dedup strategy per connector, evidence chain (every row traceable to source event), observability dashboard, runbook per connector.

**Critical discipline:** every connector runs in shadow mode for ≥7 days before cutover. Direct cutover from old flow to new connector is how a week of data is lost on a silent schema mismatch.

---

## The Discipline That Makes It Work

| Principle | What It Means Operationally |
|---|---|
| **Compilation triad** | Raw source → compiled/merged → summarized. Per interview, visit, workshop. Individual files are audit trail; compilation is the thesis; summary is what decision-makers read. |
| **Evidence first, recommendation second** | Every finding is anchored to data. Every recommendation closes the loop from evidence to action. A finding without data is a vibe. |
| **Per-domain parallel workshops** | Every business domain gets its own as-is and to-be artifact. No folding Pricing into Forecasting. The domain boundaries enforce coverage. |
| **Symmetric deliverables** | Every option, every theme, every root cause gets the same slide structure. The reader is trained once and compares cleanly after. |
| **Steering committee cadence** | Numbered, dated, Final-marked presentations every two weeks. The SC deck is the engagement's heartbeat; every other artifact feeds it. |
| **Versioning and "Final" marking** | Terminal version is explicitly marked Final. Draft and revision status is part of the filename. No ambiguity about canonical version. |
| **Business case triad** | Benefits / Costs / NPV — plus solution-to-value traceability that maps solution components back to value opportunities. Without traceability, Phase II becomes untethered. |

---

## CATz and Canary Retail

CATz is not an independent consulting practice. It is the onboarding and transformation method for Canary Retail engagements. The three connections:

1. **The same canonical data model anchors both.** The CRDM (Canonical Retail Data Model) that drives the diagnostic evidence pack is the same model Canary Retail runs at runtime. The engagement lands on the platform; it doesn't produce a deck that then has to be translated.

2. **Agent-native execution.** Phase I ingest, as-is analysis, and Phase II option modeling are scaffolded by agents running against the canonical model. The two consulting skills are agent skills, not templates — they produce structured output from evidence, not from consultant judgment.

3. **SMB compression.** The method compresses what a Big 4 engagement delivers in months — diagnostic, architecture evaluation, vendor selection — into weeks for an SMB retailer. The agent layer is what makes that compression possible without degrading quality.

**Self-diagnostic proof case.** GrowDirect has run the retail-diagnostic method against its own platform (proof case at `/Users/gclyle/CATz/proof-cases/canary-self-diagnostic.md`). This is by design — the first validation that the method works is that it works on its builder.

---

## Adoption Contexts

| Context | How CATz Is Used |
|---|---|
| **SMB retailer onboarding to Canary Retail** | Full two-phase engagement; Phase II selects Canary Retail as the platform path |
| **Internal platform transformation moments** | Platform v2 moves, major vendor cutovers — the discipline applies to ourselves |
| **Strategic decisions otherwise made ad-hoc** | Which module to productize next, which partnership to invest in |
| **Partner / VAR delivery** | CATz is the delivery method partners use for customer engagements |

---

## Related

- **Canary platform overview:** [[Brain/wiki/canary-platform-overview]]
- **Retail merchandise planning (domain source):** [[Brain/wiki/retail-merchandise-planning-otb]]
- **Promotion workflow (domain source):** [[Brain/wiki/retail-promotion-workflow]]
- **PO from plan (domain source):** [[Brain/wiki/retail-po-from-plan]]
- **CATz source vault:** `/Users/gclyle/CATz/method/`
- **Self-diagnostic proof case:** `/Users/gclyle/CATz/proof-cases/canary-self-diagnostic.md`
