---
type: pitch
domain: business
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# How We Build

> *"Do it right, do it once."*

---

## The Factory Process

Software built without a process becomes scope creep, half-built features, and technical debt you can never pay back. GrowDirect operates a six-stage factory process — inherited from a decade of enterprise SaaS platform development and refined for the current team.

The process was first attempted at a previous company, where the founder built the LP platform that became the industry standard. An acquisition interrupted the process before it matured. GrowDirect is the continuation — the factory rebuilt from zero, without the politics.

---

## Six Stages

Every feature, every sprint, every deliverable passes through six stages in order. You do not start the next stage until the current stage passes its gate.

### Stage 1: Blueprint
*"Write it before you build it."*

- Epic defined with one-sentence business justification
- Features listed with owners
- User stories written for every feature
- Acceptance criteria written for every user story
- Database schema impact identified and reviewed
- API contract defined (endpoints, inputs, outputs, error codes)
- Security considerations flagged

**Gate:** Spec reviewed, schema validated, every story has acceptance criteria, business justification approved.

### Stage 2: Parts
*"Build the foundation before the walls."*

- Database migration written and reviewed
- Migration runs clean on dev and test — no errors, no warnings
- API stubs created (routes exist, return 501 Not Implemented)
- Unit tests written for all critical paths *before* implementation
- Test file committed to source control before feature code

**Gate:** Migration runs clean. Test file is committed. Stub structure matches the API contract.

### Stage 3: Assembly
*"Now you write the code."*

- Feature implementation written to make the tests pass
- Code review by a second team member
- Integration tests added for cross-module interactions
- Documentation updated inline

**Gate:** All tests pass. Code review approved. No new warnings.

### Stage 4: Quality Control
*"QA has veto power. No exceptions."*

- QA executes test plan against every acceptance criterion
- Regression tests confirm nothing existing is broken
- Edge cases tested: empty states, error conditions, concurrent access
- Performance baseline captured

**Gate:** QA sign-off. Every acceptance criterion verified. No P1 or P2 defects open.

### Stage 5: Packaging
*"If a store manager can't understand it, simplify."*

- Documentation finalized — companion guides, API docs, release notes
- Brand compliance verified (design system, naming standards)
- Deployment configuration validated across all environments
- Rollback procedure documented and tested

**Gate:** Documentation complete. Deployment tested on staging. Rollback verified.

### Stage 6: Ship
*"Something commits every day."*

- Deploy to production
- Smoke test in production environment
- Merchant notification if user-facing change
- Monitoring confirmed — alerts configured for new endpoints

**Gate:** Running in production. No critical alerts. Merchant confirmed (if applicable).

---

## Scope Discipline

Six rules that prevent feature creep:

1. **No code without a spec.** If the story does not exist, the code does not exist.
2. **No tests after.** Tests come first on critical paths: auth, payments, detection logic, multi-tenant isolation, evidence integrity.
3. **No skipping QA.** QA veto is absolute. Nothing ships without sign-off.
4. **No scope expansion mid-sprint.** New ideas go to the backlog. Current sprint scope is locked.
5. **No "I'll fix it later."** If it's not right, it does not pass the gate.
6. **No solo heroics.** Every change gets a second set of eyes before merge.

---

## Sprint Rhythm

| Cadence | What Happens |
|---|---|
| **Daily** | Standup — blockers surfaced, work committed |
| **Weekly** | Demo to stakeholders — working software, not slides |
| **Bi-weekly** | Sprint close — retrospective, velocity captured, next sprint planned |
| **Monthly** | Gate review — are we on track for the nearest milestone? |

---

## Why It Matters

The factory process is not bureaucracy. It is the mechanism that ensures:

- **Every feature has a business reason** before any code is written
- **Every user story has testable criteria** before development starts
- **Every critical path has tests** before implementation
- **QA has absolute veto** — nothing ships that does not work
- **Documentation ships with the code** — not as an afterthought

The founder tried this once before. The company was acquired before the process matured. This time, there is no acquirer. The factory runs to completion.

---

*GrowDirect Confidential*
