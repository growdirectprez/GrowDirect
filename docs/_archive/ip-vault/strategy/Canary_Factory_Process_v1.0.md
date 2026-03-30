---
type: strategy
domain: business
status: active
created: 2026-03-19
updated: 2026-03-19
---
# Canary LP — The Factory Process
**Document Type:** Program Management Standard Operating Procedure
**Version:** 1.0
**Date:** February 17, 2026
**Author:** Eva (Program Manager)
**Status:** ACTIVE — All work on Canary follows this process. No exceptions.

---

## Eva's Foreword

Jeffe called this right. The hardest thing in building software is not writing code — it is deciding what not to write, in what order to write it, and proving it works before anyone ships it. The Canary team has a lot of ideas. That is a strength. But ideas without a process become scope creep, half-built features, and technical debt you can never pay back. I watched that happen at companies that had more resources than we do.

The Factory Process is the answer. It is not bureaucracy. It is not Jira tickets for the sake of Jira tickets. It is six stages that go in order, every time, for every feature. The stages are: **Blueprint → Parts → Assembly → QC → Packaging → Ship.** You do not start the next stage until the current stage passes its gate. That's it.

Jeffe's principle was "do it right, do it once." The Factory Process is how we honor that.

> *"I tried this at SysRepublic but then we got acquired and the infighting started so we never progressed."*
>
> — Jeffe, February 17, 2026

We're not getting acquired right now. We are building something nobody else is building, with a team that knows how. Let's do it right.

---

## The Hierarchy: How Work Is Organized

Before the process, you need to understand how Canary work is structured. Every piece of work fits into exactly one level of this hierarchy:

```
EPIC
└── FEATURE
    └── USER STORY
        └── ACCEPTANCE CRITERIA (list of testable conditions)
            └── TASK (implementation step, max 1 day)
```

### What is an Epic?

An Epic is a large body of work that delivers a meaningful capability to the business. Epics take multiple sprints to complete. They map to Canary's product modules.

*Examples: Fox Case Management, Square Marketplace Certification, Goose Bitcoin Integration*

**Rule:** An Epic must have a business owner, a definition of done, and a "why it matters" statement that Jeffe can articulate in one sentence.

### What is a Feature?

A Feature is a meaningful slice of an Epic that delivers value to a user on its own. Features are completed in one sprint (2 weeks). You can demo a Feature to a real merchant when it's done.

*Examples: Incident Report Form, Evidence Chain of Custody, Lightning Invoice Generation*

**Rule:** A Feature must be demonstrable without explanation. If you have to tell the merchant what it does, it is not ready.

### What is a User Story?

A User Story captures who needs something, what they need, and why. Format: **As a [role], I want [goal], so that [benefit].**

*Example: As a store manager, I want to receive an SMS alert when a refund exceeds $50, so that I can intervene before the transaction clears.*

**Rule:** Every User Story must be written before any code is written for it. If the story does not exist, the code does not exist.

### What is an Acceptance Criterion?

An Acceptance Criterion is a specific, testable condition that must be true for a User Story to be considered complete. Acceptance Criteria are written by Eva, validated by Jim, and signed off by the story's business owner.

*Example: Given a refund of $55 is processed, when Chirp detects it, then the merchant receives an SMS within 30 seconds containing the amount, card last-4, and alert severity.*

**Rule:** Acceptance Criteria are written BEFORE development starts. If you cannot write the test before you write the code, you do not understand the requirement.

---

## The Six Stages

### STAGE 1: BLUEPRINT
*"Write it before you build it."*

**What happens here:**
- The Epic is defined with a one-sentence business justification
- Features within the Epic are listed with owners
- User Stories are written for every Feature
- Acceptance Criteria are written for every User Story
- The database schema impact is identified and Tom reviews it
- The API contract is defined (endpoints, inputs, outputs, error codes)
- Security considerations are flagged (PCI, OAuth, RBAC, tenant isolation)

**Gate to proceed:** Jess has reviewed the Feature spec. Tom has confirmed no schema-breaking changes. Eva has confirmed every story has acceptance criteria. Jeffe has approved the Epic's business justification.

**Deliverable:** A Feature Spec document in `Documents/` following the Canary template. Named: `Canary_[Feature]_Spec_v1.0.docx`.

**Who is responsible:** The feature owner writes the spec. Eva reviews it. Jess formats it. Tom validates the data model. Jeremy validates the API contract feasibility.

**What kills this stage:** Writing code before the spec is done. This is scope creep's entry point. If Jeremy starts coding while the spec is still being written, we are off-process. Eva will call it out.

---

### STAGE 2: PARTS
*"Build the foundation before the walls."*

**What happens here:**
- Database migration is written (Alembic) and reviewed by Tom
- Migration runs clean on dev and test — no errors, no warnings
- API stubs are created (routes exist, return 501 Not Implemented)
- Unit tests are written for all critical paths *before* the implementation
- The test file is committed to GitHub before feature code

**Gate to proceed:** Migration runs clean. Test file is committed. Jeremy has confirmed the stub structure matches the API contract from Stage 1.

**Deliverable:** Migration file + stub file + test file, committed to GitHub in a feature branch.

**Who is responsible:** Jeremy. Tom reviews the migration. Eva confirms the test file is committed before implementation starts.

**What kills this stage:** "I'll write the tests after." No. Tests come first on critical paths: auth, payments, detection logic, multi-tenant isolation, evidence integrity. These are not optional.

---

### STAGE 3: ASSEMBLY
*"Now you write the code."*

**What happens here:**
- Jeremy writes feature implementation to make the tests pass
- Code follows existing patterns in the codebase — no new frameworks without Eva approval
- PRs are kept small (< 400 lines of meaningful code per PR)
- Jeremy tags PRs with the User Story they fulfill
- Daily commits — something is in the PR every day

**Gate to proceed:** All unit tests pass. All integration tests pass. No new linting errors. PR has been self-reviewed.

**Deliverable:** A passing PR linked to the User Story, ready for review.

**Who is responsible:** Jeremy writes. Eva reviews PRs for completeness (are all acceptance criteria addressed?). Tom reviews for architecture alignment.

**What kills this stage:** Scope creep inside the PR. "While I was in here I also refactored..." No. File it as tech debt. Keep the PR scoped to the story. Bigger PRs are harder to review, harder to revert, and harder to test.

---

### STAGE 4: QUALITY CONTROL
*"You do not ship what you have not tested."*

**What happens here:**
- **The Rooster runs first.** Before Jim touches it, the automated test suite must pass all three modes:
  - Mode 1: Quick Crow (health check — is the app alive?)
  - Mode 2: Feature Patrol (API-level E2E — does the feature work at the HTTP level?)
  - Mode 3: Full Strut (Playwright browser — does the page render without JS errors, template crashes, or brand violations?)
- **If any Rooster test fails, the build goes back to Stage 3.** Jeremy fixes, re-runs, until green. No manual QA begins on a red build.
- Jim runs the acceptance criteria as test cases, exactly as written in Stage 1
- Jim documents pass/fail for each criterion in the test library
- Load test is run on any change that affects the webhook pipeline or database writes
- A store manager persona test is conducted: can a non-technical user complete the core flow without help?
- Security review for any feature touching OAuth, payments, or evidence storage

**Gate to proceed:** All Rooster tests green. All acceptance criteria pass. Jim signs the QA record. No P1 or P2 defects open. Eva issues a go/no-go.

**Deliverable:** Rooster test report (all green) + completed QA record in Jim's test library. Eva's go/no-go decision documented.

**Who is responsible:** Jim owns QA execution and The Rooster test suite. Eva owns the go/no-go decision. Nobody else issues the green light. **If it doesn't work on the dev sandbox, it doesn't work anywhere** (Jeffe directive, Feb 20, 2026).

**The closed loop (Jeffe directive, Feb 20, 2026):**
```
PRD (Blueprint) → Acceptance Criteria → Jim's Rooster Tests →
Jeremy writes code → Rooster runs (all 3 modes) →
ALL GREEN? → Jim signs off → Eva releases
ANY RED? → Back to Stage 3 → Fix → Re-run → Repeat until green
```

**What kills this stage:** "It works on my machine." That is not a QA result. QA runs on the test environment (iMac Docker box), against real data patterns, against the exact acceptance criteria written in Stage 1. The Rooster runs the same tests on every build, every time, no exceptions. If the criteria are not met, the feature goes back to Stage 3.

---

### STAGE 5: PACKAGING
*"The feature does not exist until it is documented."*

**What happens here:**
- Jess writes or updates the merchant-facing documentation for the feature
- Jess updates the relevant module doc (Fox.md, Goose.md, Owl.md, etc.)
- Any new SDK, API, or data source used is logged in the Reference Library
- Release notes are drafted
- If the feature introduces a new database table or schema change, the Platform Schema doc is updated

**Gate to proceed:** Jess signs off on documentation completeness. Reference Library is current. Release notes exist.

**Deliverable:** Updated documentation, signed off by Jess. Updated Reference Library entry if applicable.

**Who is responsible:** Jess owns documentation. She has sign-off authority over this stage. No feature ships without her OK.

**What kills this stage:** "We'll document it after it ships." That is how documentation debt accumulates and never gets paid. Jess does not sign off until it is done. Eva does not ship until Jess signs.

---

### STAGE 6: SHIP
*"Deploy it, watch it, confirm it."*

**What happens here:**
- Feature is deployed to production (AWS) via the CI/CD pipeline
- Post-deploy smoke test runs automatically
- Jeremy monitors error rates and webhook processing for 2 hours post-deploy
- Merchant-facing release announcement drafted by Will (if user-visible)
- Syd reviews any external communication before it goes out
- Feature is marked "Done" in the sprint board

**Gate to proceed:** Smoke tests pass. No elevated error rate in the first 2 hours. Merchant communication cleared by Syd and Jeffe.

**Deliverable:** Feature live in production. Status updated. Sprint board reflects completion.

**Who is responsible:** Jeremy deploys. Eva confirms the deploy gate. Syd/Jeffe approve external comms. Everyone monitors.

**What kills this stage:** Deploying on a Friday. Deploying without a rollback plan. Deploying without post-deploy monitoring. Deploying without merchant communication on user-visible changes.

---

## The Scope Discipline Rules

These rules exist specifically because of the pattern Jeffe described: good ideas that never ship because they keep growing. The Factory Process enforces scope through structure, not willpower.

### Rule 1: The Spec Gate
No code is written without a spec. If Jeremy is writing code for something that does not have a User Story with Acceptance Criteria, Eva stops it immediately. The code is discarded. The spec is written. Then the code is written.

### Rule 2: The Sprint Contract
At the beginning of each sprint, the team commits to a specific set of User Stories. That set is the sprint contract. Adding stories to an in-progress sprint requires Eva's explicit approval and a corresponding removal of equivalent scope. Stories do not sneak in.

### Rule 3: The Tech Debt Register
Every good idea that comes up during implementation but is out of scope gets logged in the Tech Debt Register (`Documents/Canary_Tech_Debt_Register.md`) with a brief description and a priority rating. It is not ignored. It is parked. It will be scheduled. This is how we honor Jeffe's ideas without losing the sprint.

### Rule 4: The MVP Boundary
The MVP is defined in `Documents/Canary_MVP_Epics_v1.0.md`. Everything inside the MVP boundary gets built to ship quality. Everything outside it is a future release. When someone says "can we also add X," Eva checks the MVP boundary. If X is outside it, it goes in the Tech Debt Register and Phase 2 backlog. No negotiation. No exceptions during MVP sprints.

### Rule 5: The "Why Now" Test
Before any new feature or task is added to the current sprint, Eva asks: *"Why does this have to ship in this sprint and not the next one?"* If the answer is not clear and compelling, the item moves to the backlog. First-mover advantage is real but it requires us to actually ship, not to make the backlog bigger.

### Rule 6: One Thing at a Time
Jeremy works on one User Story at a time. Not three in parallel. Not "mostly done" on four. One story at a time, completed to definition of done, then the next. This is how we maintain quality and catch integration problems early.

---

## The Sprint Rhythm

| Day | Activity |
|---|---|
| **Monday (Sprint start)** | Standup + Sprint Planning (30 min). Stories assigned, acceptance criteria confirmed, dependencies identified. |
| **Tue–Thu** | Build. Daily 15-min standup. Blockers escalated by noon. |
| **Friday** | Demo (30 min). Stories that meet definition of done are demoed. Stories that don't are discussed — root cause, not blame. |
| **Friday (cont.)** | Sprint retro (15 min). One thing that went well. One thing to change. Action item for next sprint. |
| **Monday+1** | New sprint begins with next set of committed stories. |

Sprints are 1 week for now (Canary is a small team). Moving to 2-week sprints when the team reaches 5+ developers.

---

## The Quality Gates Summary

| Stage | Gate Owner | Minimum to Pass |
|---|---|---|
| Blueprint | Eva + Jeffe | Spec written, AC defined, Tom schema review complete |
| Parts | Jeremy + Tom | Migration clean, tests committed before code |
| Assembly | Eva | All tests pass, PR < 400 lines, self-reviewed |
| QC | Jim | **Rooster green (all 3 modes)**, all AC pass, go/no-go issued, no open P1/P2 bugs |
| Packaging | Jess | Docs complete, Reference Library current |
| Ship | Eva | Smoke tests pass, monitoring active, comms cleared |

---

## What "Done" Means at Canary

A User Story is done when all six stages are complete. Not "mostly done." Not "done except the docs." Not "done but needs a minor fix." Done means:

- ✅ Code committed and passing all tests
- ✅ **Rooster green — all 3 modes (Quick Crow + Feature Patrol + Full Strut)**
- ✅ Deployed to production
- ✅ Acceptance criteria verified by Jim
- ✅ Documentation updated and signed by Jess
- ✅ Reference Library current
- ✅ Merchant-facing communication sent (if applicable)

If any item is unchecked, the story is **In Progress**, not Done.

---

## The SysRepublic Factory — Where This Came From

The Canary Factory Process is not invented from scratch. It is the second implementation of a methodology Jeffe built and attempted to complete at his prior company, SysRepublic. It was interrupted by an acquisition (April 2016) and organizational infighting that prevented the process from fully taking hold.

> *"I tried this at SysRepublic but then we got acquired and the infighting started so we never progressed."* — Jeffe, February 17, 2026

### What the SysRepublic Factory Was

The Factory Overview slides (uploaded by Jeffe from his archive, now in `Documents/` as `Factory Overview.pptx` and `Factory Overview v2.pptx`) show the actual SysRepublic factory methodology as it existed in late 2016 — just before the acquisition closed. Key concepts:

**Factory Applications Built on the Sysrepublic Platform (Secure 3.5 / Secure 4):**

The SysRepublic factory produced a portfolio of LP applications, all on a shared foundation:
- **Foundation Management** — Users, Roles, Locations, Products, People (= Canary's E0 Foundation Epic)
- **Incident Management (ICMS)** — Incident Case Management System (= Canary's Fox module)
- **Refund Management** — Refund abuse detection (= Canary's Chirp / E1 Core Fraud)
- **EBR** — Exception-Based Reporting (= Canary's Owl analytics oracle)
- **BOLO** — Be On The Lookout proximity alerts (= Canary's Fox BOLO network, Sprint 3)
- **ORC** — Organized Retail Crime tracking (= Canary's Fox threat categories)
- **Audit & Survey** — Store compliance audits (= future Canary module)
- **Risk Management** — Enterprise risk scoring (= Canary's Owl threat scoring)
- **Cashier Performance / KPIs / Transaction Viewer** (v2 only — = Canary's Dog module concept)
- **MoneyGram / Giftcards / Known Loss / Rewards** — Financial product fraud (= Canary future modules)

**SysRepublic Factory Concepts (Direct Parallels to Canary Factory Process):**

| SysRepublic (2016) | Canary (2026) |
|---|---|
| Common Data Center Instances (QA & PROD) | Dev → Test (Docker) → Prod (AWS) |
| TFS Online repository for all artifacts | GitHub (feature branches, PR workflow) |
| Test Harnesses / Scripts | Unit tests committed before implementation (Stage 2: Parts) |
| Specification Templates + Documentation | Feature Spec template → `Canary_[Feature]_Spec_v1.0.docx` |
| Trello for project management | Sprint board + CLAUDE.md task tracking |
| Factory Team owns the generic solution | Eva owns the Factory Process; Jeremy owns implementation |
| Customer configuration is checked out from the Factory | Merchant-specific config is isolated; core platform is standard |
| Factory applications are tested as an integrated whole | Jim runs acceptance criteria against exact conditions from Stage 1 |

**SysRepublic Factory Life Cycle (Their Words, Our Principles):**

> *"A continuous improvement process aimed at developing a core set of common application capabilities in a consistent, supportable format. As new requirements are identified and capabilities evolve, they are built upon the common foundation layer to ensure consistency and manage the portfolio of offerings. Client-specific requirements are managed at the project level, and brought back into the overall capability matrix where they expand the generic offering."*
> — Factory Overview.pptx, SysRepublic, ~2016

This is the exact philosophy behind Canary's Epic/Feature/User Story hierarchy. E0 (Foundation) = the common foundation layer. Individual merchant needs = project-level requirements. The whole platform = the capability matrix.

### The Live Evidence: factory.solutions-sysrepublic.com

Two browser session state files (`factory.solutions-sysrepublic[1].xml` and `factoryqa.solutions-sysrepublic[1].xml`) were uploaded by Jeffe from his archive. These are browser localStorage exports from SysRepublic's actual production and QA platforms, captured in 2016:

- **`factory.solutions-sysrepublic.com/secure4/app/lpcasemanagement`** (Nov 11, 2016) — Production environment. Shows a user navigating the LP Case Management module of Secure 4 — the direct predecessor to Canary's Fox module.
- **`factoryqa.solutions-sysrepublic.com/Secure4/icms/form/read/00326275477`** (April 4, 2016) — QA environment. Shows a user viewing an actual ICMS (Incident Case Management System) incident form, with "My Incidents" search active.

These are not mockups. These are real session state snapshots from a live enterprise LP platform that Jeffe built and that served real retailers — the same architectural patterns Canary is now rebuilding, with Bitcoin-native rails replacing the legacy infrastructure.

### What This Means for the Canary Team

The Factory Process in this document is not a theoretical methodology. It is institutional knowledge — learned from building it once (SysRepublic), watching an acquisition cut it short, and now executing it again with the full team aligned from day one.

Jeffe's mandate is clear: this time, it completes.

> *"We're not getting acquired right now. We are building something nobody else is building, with a team that knows how. Let's do it right."* — Eva's Foreword, this document

Every stage gate, every scope discipline rule, every quality bar exists because someone who has done this before is telling you exactly where it goes wrong when you skip steps.

---

## A Note on the Factory Overview Presentations

Jeffe's original Factory Overview slide decks (`Factory Overview.pptx` and `Factory Overview v2.pptx`) are archived from SysRepublic (~2016). These files are now accessible in the Canary workspace `Documents/` folder. Key content extracted above. Both files show v1 (8 slides) and v2 (6 slides, adds Cashier Performance/KPI/Transaction Viewer modules) of the SysRepublic factory presentation — the visual ancestor of what is now the Canary Factory Process.

---

*Canary LP | Confidential*
*Eva — Program Manager | February 17, 2026*
