---
name: canary-blueprint
description: |
  Factory Process plan-writing skill. Use when you have a spec, requirements,
  GRO issue, or Jeffe directive for a multi-step task — before touching code.
  Creates implementation plans that follow the Factory Process, enforce data
  integrity, and produce bite-sized TDD tasks scoped to the Canary stack.
  Replaces superpowers:writing-plans with Canary-specific guardrails.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Edit
  - Write
  - TodoWrite
---

# Canary Blueprint — Factory Process Plan Writing

> "Documents first, then build and tie it all together soup to nuts in a factory process."
> — Jeffe, Feb 17, 2026

## Overview

Write implementation plans that a skilled developer with zero Canary context can
execute without drift. Every plan maps to the Factory Process. Every task is
bite-sized, test-first, and scoped to one clear deliverable.

**Announce at start:** "I'm using canary-blueprint to write the Factory Process implementation plan."

**Save plans to:** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`
**Save specs to:** `docs/superpowers/specs/YYYY-MM-DD-<feature-name>-design.md`

---

## Pre-Flight: Before Writing Anything

### 1. Confirm the Ticket

Every plan requires a source:

```
-> GRO issue number? (check Linear)
-> Explicit Jeffe directive? (quote it)
-> Neither? STOP. No ticket = no work.
```

If Jeffe gave a verbal directive without a GRO number, create the Linear issue
first. The plan references the issue. The issue references the plan. Traceability
is non-negotiable.

### 2. Load Context

```bash
# Recall what we know about this domain
memory_recall("your topic here")

# Load domain context if touching a specific service
domain_context("service_name")  # identity, tsp, chirp, alert, owl, fox, analytics, alx, raas, ops, ui_bff

# Load pipeline architecture context — every plan needs this
memory_recall("six-node pipeline staged immutability")
memory_recall("tLog to gLog")
```

Read CLAUDE.md. Check if this work touches a blocker.

### 2b. Identify Pipeline Position

Every feature sits somewhere in the six-node pipeline:

```
Node 1: Webhook Receipt (Square -> TSP ingestion)
Node 2: Evidence Store (Sub 1 — raw seal, legal witness)
Node 3: Structured Store (Sub 2 — parse, route, CRDM)
Node 4: Detection Engine (Chirp rules -> alerts)
Node 5: Case Management (Fox — investigation, evidence chain)
Node 6: Immutable Anchor (Sub 3 — Bitcoin ordinal, gLog)
```

```
-> Which node(s) does this feature touch?
-> Does this feature create data that should flow to the gLog? If yes, how?
-> Does this feature maintain merchant-first isolation (per-merchant hash chain)?
-> If this feature doesn't touch the pipeline directly, what pipeline node does it serve?
```

If you can't answer these, recall more context before writing the plan.

### 3. Scope & Phase Check

We have a full working app headed toward beta. The gate is `auth/join.html` —
the beta authorization and onboarding flow.

```
-> Does this plan serve the path to beta launch? Proceed.
-> Does this plan add a net-new module or vertical? Flag it — Jeffe + Eva decide timing.
-> Does this plan harden, polish, or fix something in the live app? Proceed.
-> Is this blocking the join/auth flow? Prioritize it.
```

If you're not sure whether something is in scope, it probably isn't. Ask Jeffe.

### 4. Infrastructure Integrity Check

If this plan introduces a new dependency (package, service, database, external API):

```
-> Open license? (MIT, Apache 2.0, BSD — not SSPL, not BUSL)
-> Bitcoin-native alignment? (or at minimum, not hostile to it)
-> Production-grade? (not alpha, not abandoned, not single-maintainer)
-> No rebuild risk? ("If this thing works we might have to rebuild everything
   and consume months of costs because I was lazy." — Jeffe)
```

If it fails any of these, find the right tool first. Don't adopt and migrate later.

---

## Plan Document Header

Every plan starts with this header:

```markdown
# [Feature Name] — Implementation Plan

> **For agentic workers:** REQUIRED: Use canary-assembly to implement
> this plan. Steps use checkbox (`- [ ]`) syntax for tracking. Run
> canary-tdd for all implementation steps.

**GRO Issue:** GRO-XXX
**Goal:** [One sentence — what this builds and why it matters for the merchant]

**Pipeline Position:** [Which node(s) this touches: Receipt / Evidence / Structured / Detection / Case / Anchor]
**gLog Impact:** [Does this create data that flows to the immutable ledger? Yes/No — if yes, how]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** Python 3.12 / Flask / SQLAlchemy 2.0 / PostgreSQL 17 / Valkey 8

**Spec:** `docs/superpowers/specs/YYYY-MM-DD-<feature-name>-design.md`

**Factory Stage:** Blueprint

---
```

---

## Scope Check

If the spec covers multiple independent subsystems, break it into separate plans.
Each plan should produce working, testable software on its own.

**The one-line test for everything in the plan:**
> *Does this work help GrowDirect mint the pool, seal the event, or collect the sat?
> If yes — ship it. If no — park it.*

If a task in the plan doesn't pass this test and isn't infrastructure that enables
something that passes it, cut it. Be ruthless.

---

## File Structure

Before defining tasks, map which files will be created or modified:

```markdown
## File Structure

| Action | File | Responsibility |
|--------|------|---------------|
| Modify | `canary/path/to/file.py` | What this file does |
| Create | `canary/path/to/new_file.py` | What this new file does |
| Test   | `tests/unit/test_file.py` | What it tests |
```

**Rules:**
- Absolute paths from project root (`~/GrowDirect/Canary/`)
- One responsibility per file. Split by responsibility, not by layer.
- Follow existing patterns. Don't restructure the codebase in a feature plan.
- Flag Guardian-protected files: `.env`, `wsgi.py`, `session_factory.py`,
  `Dockerfile`, `docker-compose.*.yml` — these require `file-guardian`.
  Include a Guardian step in the task.

### Data Integrity Flag

If any file touches `canary_sales` schema:

```
DATA INTEGRITY: This plan modifies the sales schema.
- canary_sales is INSERT-only. No UPDATE. No DELETE.
- PostgreSQL triggers enforce immutability at the database level.
- Every change must include a test that verifies INSERT-only constraint preservation.
- Hash chain integrity must be maintained.
```

If any file touches `canary_app` schema with FK constraints:

```
REFERENTIAL INTEGRITY: This plan modifies app schema FK relationships.
- All ForeignKey() constraints must reference merchants.id (UUID PK), never merchants.merchant_id (Square ID).
- Include Alembic migration for any schema change.
- Include integration test that verifies FK rejection on bad reference.
```

---

## Task Structure — The Factory Parts

Each task follows the Factory Process "Parts" stage: test-first manufacturing.

````markdown
### Task N: [Component Name]

**Files:**
- Create: `canary/exact/path/to/file.py`
- Modify: `canary/exact/path/to/existing.py:123-145`
- Test: `tests/unit/test_file.py`

**Markers:** `unit` / `smoke` / `chirp` / `fox` / `owl` / `square` / `raas` (match pytest.ini)

- [ ] **Step 1: Write the failing test**

```python
# tests/unit/test_specific_behavior.py
import pytest
from canary.module.component import function

class TestSpecificBehavior:
    def test_expected_outcome(self):
        result = function(input_data)
        assert result == expected_output

    def test_edge_case(self):
        with pytest.raises(ValueError):
            function(bad_input)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/unit/test_specific_behavior.py -v`
Expected: FAIL with `ImportError` or `ModuleNotFoundError` (function doesn't exist yet)

- [ ] **Step 3: Write minimal implementation**

```python
# canary/module/component.py
def function(input_data):
    """One-line docstring explaining what this does."""
    return expected_output
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/unit/test_specific_behavior.py -v`
Expected: PASS — all green

- [ ] **Step 5: Run smoke test**

Run: `python3 -m pytest tests/smoke/ -v --timeout=30`
Expected: All existing smoke tests still green (no regressions)

- [ ] **Step 6: Commit**

```bash
git add tests/unit/test_specific_behavior.py canary/module/component.py
git commit -m "feat(GRO-XXX): add specific feature

Test-first implementation. Refs GRO-XXX."
```
````

---

## Bite-Sized Task Granularity

Each step is one action (2-5 minutes):
- "Write the failing test" — step
- "Run it to make sure it fails" — step
- "Implement the minimal code" — step
- "Run tests to make sure they pass" — step
- "Run smoke tests" — step
- "Commit" — step

If a task has more than 8 steps, break it into two tasks. If a task takes more
than 30 minutes, it's too big.

---

## Guardian Tasks

When a plan touches protected files, include a dedicated Guardian task:

```markdown
### Task N: [Guardian] Modify wsgi.py for new blueprint registration

**PROTECTED FILE — requires file-guardian skill**

- [ ] **Step 1: Invoke file-guardian**

Run: `/file-guardian`
Target: `wsgi.py`
Reason: Register new blueprint for [feature]

- [ ] **Step 2: Follow Guardian workflow**

Guardian handles: pre-flight snapshot -> approval -> backup -> edit -> validate -> manifest update

- [ ] **Step 3: Verify guardian manifest updated**

Run: `cat .guardian-manifest | grep wsgi.py`
Expected: New SHA256 hash recorded
```

---

## Factory Process Stage Gates

Every plan must declare which Factory stages it covers and what gates apply:

```markdown
## Factory Process Tracking

| Stage | Status | Gate |
|-------|--------|------|
| Blueprint | This plan | Plan reviewed and approved |
| TDD | Tasks 1-N | Each task has passing tests |
| Assembly | Integration | All tasks integrated, smoke tests green |
| Verify | canary-verify | Evidence before claims |
| QA | canary-qa | Diff-aware testing, health score >= 75 |
| Ship | canary-ship | Pre-landing review, bisectable commits, PR |
```

**The rule:** No stage skipped. No code without a spec. No ship without QA gate pass.

---

## Plan Quality Checklist

Before saving the plan, verify:

- [ ] GRO issue referenced in header
- [ ] Goal statement explains merchant impact
- [ ] Pipeline Position identified (which node(s) this touches)
- [ ] gLog impact stated (does this create data for the immutable ledger?)
- [ ] Tech stack matches Canary (Python 3.12, Flask, SQLAlchemy 2.0, PostgreSQL 17, Valkey 8)
- [ ] File structure table is complete with exact paths
- [ ] Every task has a failing test as Step 1
- [ ] Every task has a smoke test step
- [ ] Every commit message references GRO issue
- [ ] Guardian tasks flagged for protected files
- [ ] Data integrity flag included if touching canary_sales
- [ ] Scope check passed (serves beta launch path or hardens existing app)
- [ ] Infrastructure integrity check passed for new dependencies
- [ ] Factory Process tracking table included
- [ ] Pytest markers assigned per `pytest.ini` (unit, smoke, chirp, fox, owl, square, raas)
- [ ] No file creates `_v2`, `_new`, or `_backup` variants (edit in place)
- [ ] All paths are absolute from project root

---

## Plan Review

After completing the plan, self-review against these questions:

```
-> Could a developer with zero Canary context execute this without asking questions?
-> Does every task produce a testable, committable unit of work?
-> Are there any tasks that skip the test-first step? (If yes, fix them.)
-> Does this plan move toward the gLog — or does it create more mutable state?
-> Does this plan maintain merchant-first isolation (per-merchant data boundaries)?
-> If this plan creates events, do they reach the hash chain (Node 3+)?
-> Does anything in this plan require a dependency that fails the infrastructure integrity check?
```

---

## Execution Handoff

After saving the plan:

**"Plan complete and saved to `docs/superpowers/plans/<filename>.md`. Ready to execute?"**

**Execution:**
- Use `canary-assembly` to execute the plan
- canary-assembly handles: context loading, Guardian enforcement, rooster integration,
  stop-and-retriage, Linear updates, session memory writes
- If subagents are available, dispatch fresh subagent per task with two-stage review
- If no subagents, execute in current session with checkpoints

---

## Remember

- **Exact file paths.** Always. From project root.
- **Complete code in plan.** Not "add validation" — show the validation code.
- **Exact commands with expected output.** The executor doesn't guess.
- **Python 3.12 syntax.** `Mapped[]`, type hints, no legacy patterns.
- **`python3` not `python`.** Always.
- **DRY. YAGNI. TDD. Frequent commits.** The classics apply.
- **One behavior per test.** "and" in the test name? Split it.

---

## North Star Check

Before finalizing any plan, ask one question:

> "We don't want to add to the stress. We want to ease it."
> — Jeffe, Feb 26, 2026

Does this plan make the merchant's life easier? Does it reduce their cognitive
load? If the feature requires recovery steps, explanation, or back-and-forth —
it fails. Go back to the Blueprint and simplify.

---

*Canary Blueprint v1.0 — Factory Process Plan Writing*
*Replaces: superpowers:writing-plans*
*Maintained by: ALX*
