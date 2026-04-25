---
classification: internal
type: wiki
date: 2026-04-25
last-compiled: 2026-04-25
needs-review: 2026-05-09
source-archive: /Volumes/My Passport/CLIENTS/DELIVERY/ + /Volumes/My Passport/macpro/Users/geoff/Documents/ (sanitized)
provenance: Brain/wiki/founder-context-secure-engagement-archive.md
---

# Delivery Framework — Cross-Engagement Discipline

A four-phase, governance-gated framework for running customer engagements. Reusable across any kind of solution sale: hosted analytics, packaged software, video integration, custom build. The shape is well-tested — it predates and outlasts any particular product. Use it as the discipline layer wrapped around any single engagement (the 100-day deployment shape sits inside this framework as one Construction iteration).

## Four phases

The framework is divided into four phases. Each is delivered by a specific team, produces specific artifacts, and clears at a specific quality gate.

```
INCEPTION ──── ELABORATION ──── CONSTRUCTION ──── COMPLETION
   Sales         Delivery          Delivery         Delivery
                                                    + Client Services
                                                    + Service Support
   Gate 1        Gate 2, 3         Gate 4           Gate 5, 6
```

**Inception** is owned by Sales. Output: a signed contract and an agreed Statement of Work. Gates: Envision (Q1: are we doing the right thing?).

**Elaboration** is owned by Delivery. Output: a baselined plan, a documented design, a built QA environment, an approved risk register. Gates: Scope (Q2: are the requirements defined?), Plan (Q3: can we do it within time and budget?).

**Construction** is owned by Delivery, with Client Services and Service Support engaged. Output: a built and validated solution, a built production environment, a deployed system. Gates: Build (Q4: are we ready to integrate?).

**Completion** is owned by Delivery for handover, then transferred to Service Support for ongoing operations. Output: a live production system, a closed project, a benefits assessment. Gates: Stabilise (Q5: are we ready for support?), Assess (Q6: are we realising value?).

Elaboration and Construction iterate. The framework explicitly supports running them as a loop for additional business releases without re-running Inception.

## Six quality gates

Each gate is a governance question with a specific answer. Gates control progression — a phase does not end until its gate clears.

| # | Track | Question | Variance | Where |
|---|---|---|---|---|
| 1 | Envision | Are we doing the right thing? | Pre-contract — qualitative | After Submit Proposal |
| 2 | Scope | Are the requirements defined? | ±30% scope/time/resources | After Define Proposed Solution |
| 3 | Plan | Can we do it within time and budget? | ±20% | After Finalise Plans |
| 4 | Build | Are we ready to integrate? | ±15% | After Verify and Validate Solution |
| 5 | Stabilise | Are we ready for support? | — | After Go Live |
| 6 | Assess | Are we realising value? | ±5% | After Benefits Realisation |

The variance discipline is the framework's most important feature. Each gate ratchets uncertainty down: Pre-Gate-2 you have 30% headroom on scope/time/resources; by Gate 4 you have 15%; by Gate 6 you should be within 5%. Change requests after Gate 4 are formal and re-priced — scope creep stops being free.

Not every gate is mandatory for every engagement. The Delivery Manager decides at project initiation which gates apply. A small extension to an existing customer might run only Gates 2, 4, and 5. A new platform deployment runs all six.

## Twelve milestones

Milestones are observable transitions, not gates. They are tracked weekly by the PM:

1. Contracts and MSA signed off
2. Statement of Work signed off, Purchase Order received
3. Resources allocated
4. Key documents received from customer
5. QA environment built
6. Design approved
7. Development complete (unit-tested locally)
8. Production environment built
9. Test complete (issue tracker up to date)
10. Go/No-Go decision
11. Customer signs off training and testing
12. Production go-live; solution accepted into Service Support
13. Project closure

Milestones are deliverables-shaped (built, signed off, complete), not activities-shaped. This is deliberate — a milestone closes when something is true, not when work has happened.

## Artifact register

Fifteen named documents (A through O), produced across the engagement and tracked as a register:

| ID | Document | Phase | Owner |
|---|---|---|---|
| A | Proposal | Inception | Sales |
| B | Contracts and Master Services Agreement | Inception | Sales |
| C | Delivery Portfolio | Inception | Solutions Manager |
| D | Statement of Work | Inception | Account Manager |
| E | Initial Project Plan and Approach; Issue Tracker established | Inception | PM |
| F | QA Infrastructure Request | Elaboration | Infrastructure |
| G | Business Requirements Document; Risk Dictionary | Elaboration | Client Services |
| H | Solution Architecture and Solution Design | Elaboration | Tech Lead |
| I | Project Plan, Test Plan, Implementation Plan | Elaboration | PM |
| J | Production Infrastructure Request; capacity sizing; CRM ticket | Construction | Infrastructure |
| K | Reference data mapping; Interface specs; Configuration checklist | Construction | Tech Lead |
| L | Support and Operations Guide | Completion | Delivery Project team |
| M | Project Completion Report | Completion | PM |
| N | Project Dashboard | Cross-phase | PM |
| O | Change Request Form | Cross-phase | Account Manager |

The register lets a steering group see "what artifacts exist for this engagement" at any moment. Missing artifacts are visible. Documents are not all mandatory — the SoW selects which apply for the engagement.

## Cadence

Three rhythms run in parallel during an engagement:

**Weekly status meeting** — required during active phases (Elaboration, Construction). Attendees: PM, Tech Lead, Customer PM. Purpose: review milestones since last week, raise risks, agree the week ahead. Duration: 30-60 minutes. Output: status summary in the Project Dashboard.

**Workshops** — half- to full-day collaborative sessions. Five named workshops in the framework:
- W1 — Sales evaluation (during Inception)
- W2 — Project Kickoff (start of Elaboration)
- W3 — Design Authority (end of Elaboration, signs off design)
- W4 — User Acceptance Testing / success criteria (during Construction)
- W5 — Lessons Learned (during Completion)

The framework prescribes a 1/3-1/3-1/3 workshop time split: a third uncovering the problem, a third brainstorming solutions, a third sizing and prioritizing. Workshops are interactive, not presentational.

**Meetings** — shorter targeted sessions, typically <2 hours. Eleven named meetings spread across the engagement, each with a specific agenda topic. Examples: Delivery Kickoff (M1, internal), Internal Project Kickoff (M2), Initiate Technical Design (M3), Initiate Process Design (M4), Confirm Infrastructure (M5), Handover to Client Services (M6), Service Support Engagement (M7), Train Users (M8), Service Support Handover (M9), Post-Implementation Review (M10), Benefits Realisation (M11).

## Governance and escalation paths

The framework defines a clear hierarchy of authority for governance decisions:

- **Project Manager / Delivery Manager / Lead Technical Consultant** — runs the engagement day-to-day, owns weekly status, calls workshops, signs milestones.
- **Solutions Manager** — owns the Delivery Portfolio (cross-engagement resource view), bookmarks resource allocations, escalates portfolio-level conflicts.
- **Account Manager** — owns the customer commercial relationship, owns Change Requests, chases final payments. Escalation point for scope conflict.
- **Change Board** — approves QA Infrastructure Requests (F), Production Infrastructure Requests (J), and Production Go-Live (Milestone 12). Cross-engagement authority for environment changes.
- **Design Authority workshop (W3)** — internal sign-off on solution design. Reviews data load patterns, capacity plans, architecture, product gaps. Required before Gate 3 (Plan).
- **Service Support** — must accept the solution at handover. Has veto over Go-Live if the Support and Operations Guide (L) is incomplete.

Escalation paths:
- Scope conflict during Elaboration → Account Manager → re-priced Change Request
- Resource conflict across engagements → Solutions Manager → Delivery Portfolio review
- Environment / change approval → Change Board
- Design conflict → Design Authority workshop
- Handover readiness → Service Support, with veto power
- Customer escalation → PM/Delivery Manager → Account Manager → Service Support Service Manager (post-handover)

## Sign-off discipline

Five sign-off events anchor the engagement:

1. **Contracts/MSA sign-off (Milestone 1)** — closes Inception's commercial side.
2. **Statement of Work sign-off + PO received (Milestone 2)** — authorizes Delivery to begin.
3. **Design Approval (Milestone 6, after W3 Design Authority)** — closes Elaboration's design phase. Customer may impose its own approval process atop this.
4. **Customer Sign-Off of Training and Testing (Milestone 11)** — required before Go/No-Go.
5. **Solution Accepted into Service Support (Milestone 13)** — closes the Delivery team's warranty period; Service Support assumes ongoing operations.

Each sign-off is a signed document or a recorded decision. The framework does not accept verbal sign-off as closing a milestone.

## Change management

Change Requests (Document O) are formal during Elaboration and mandatory during Construction. Process: Account Manager defines the change, costs it, and gains customer approval before it enters scope. The framework explicitly notes that scope increases after development begins are re-priced, with impacts to time, resources, and cost. This stops the most common engagement failure mode (silent scope creep absorbed by the delivery team).

## Continuous monitoring and continuous control

Two cross-phase tracks run for the entire engagement:

**Monitoring (Planning and Reporting)** — owned by the PM. Outputs: Project Dashboard (Document N), weekly status, milestone tracking, risk register. Active from Inception through Completion.

**Controlling (Change Management)** — owned by the Account Manager. Outputs: Change Request log (Document O), commercial impact assessments, re-priced contract amendments. Active from Inception through Completion.

These two tracks distinguish "running the engagement" from "running the business of the engagement." The PM owns time and quality; the Account Manager owns scope and money.

## How this framework wraps the 100-day deployment shape

The 100-day deployment is a single Construction iteration of this framework. Specifically:

- Inception happens before Day 1 (Proposal, Contracts/MSA, SoW, Project Initiation).
- Elaboration runs Days 1-30 (Mobilisation, Define Tech Reqs, Define Operational Processes, Solution Design, Risk Assessment, Finalise Plans).
- Construction runs Days 30-100 (Build & Configure, Verify & Validate, Build Production, Deploy, Engage Service Support, UAT, Complete Solution Documents, Implementation Review, Deliver Training).
- Completion runs Days 100+ (Go Live, Support Handover, Post-Implementation Review, Continuous Client Services, Benefits Realisation, Continuous Service Support).

Phase 2 is a second Construction iteration without a new Inception — the SoW already covered it. This is the framework's intent: Construction loops; Inception runs once.

## Tailoring guidance

The framework explicitly states that not every process, meeting, or document is required for every engagement. The Delivery Team decides the model at Project Initiation, based on the proposal and Statement of Work. Hosted-platform projects with a known shape (the 100-day deployment archetype) can use a pre-defined subset; bespoke or first-of-kind engagements should run the full framework.

For a 25-store retail integration on a packaged retail-management platform, expected tailoring:
- Inception condensed (qualified opportunity, no RFP, single-pass SoW).
- Elaboration condensed to ~3 weeks (single design workshop, single risk review).
- Construction full discipline (the 100-day Phase 1 is the Construction iteration).
- Completion full discipline (handover to Support Desk is critical for a packaged-platform engagement).
- Documents: A, B, D, E, G, H, I, J, K, L, M required. C, F, N, O optional based on customer's procurement process.
- Gates: 1, 2, 3, 4, 5 mandatory. 6 (Benefits) often deferred to after first 90 days of production.
