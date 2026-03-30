---
type: workorder
domain: canary
status: active
created: 2026-03-14
updated: 2026-03-19
---
# Canary Skills Audit & Consolidation Plan

**Version:** 1.0
**Date:** March 14, 2026
**Author:** ALX
**Purpose:** Full inventory of all development skills, overlap analysis, and consolidation plan to create one focused Canary-flavored skill set

---

## The Problem

We have skills from four sources that partially overlap, partially conflict, and don't carry our DNA:

| Source | Count | Where They Live | Status |
|--------|-------|-----------------|--------|
| Canary Custom | 13 | `.claude/skills/` + `.canary-skills/` + `WarChest/skill/` | ✅ Active, project-specific |
| Obra Superpowers | 7 core | CLI-installed (Claude Code / VS Code) | ⚠️ Generic — no retail, no Factory Process |
| Anthropic Platform | 6 | System-level (Cowork) | ✅ Active — docx, pdf, pptx, xlsx, schedule, skill-creator |
| gstack (reference) | 10 | Not installed — cloned for study | 📚 Reference only |

**The gap:** Obra Superpowers provides the engineering guardrails (TDD, debugging, planning, verification) but they're generic. They know nothing about:

- The Factory Process (Blueprint → Parts → Assembly → QC → Packaging → Ship)
- Data integrity ("people's lives and jobs we are analyzing")
- Merchant-first design ("ease the stress, don't add to it")
- Jim's QA veto gate (no ship without Jim's signature)
- The CRDM, the gLog, or the tLog → gLog through-line
- Bitcoin-native infrastructure integrity
- The 27-feature MVP freeze
- GRO issue scoping discipline

Meanwhile, our 13 custom skills handle session lifecycle, deployment, QA, and team operations — but there's no bridge between the two. The Obra skills are the *how* of building. The Canary skills are the *what* of operating. Neither carries Jeffe's *why*.

---

## Inventory: Obra Superpowers (CLI Skills)

These are the 7 core skills referenced in CLAUDE.md and installed for Claude Code:

### 1. writing-plans
**What it does:** Creates implementation plans from specs. Maps file structure, decomposes into bite-sized TDD tasks, includes exact file paths and code. Saves to `docs/superpowers/plans/`.
**Strength:** Excellent structure — the plan format is battle-tested and our `docs/superpowers/plans/` directory has 16 plans generated from it.
**Gap:** No Factory Process stages. No scope check against MVP freeze. No GRO issue requirement. No data integrity checkpoints. Generic tech assumptions (npm/cargo) vs. our stack (Python/Flask/SQLAlchemy/PostgreSQL).

### 2. executing-plans
**What it does:** Loads a plan, reviews critically, executes tasks with TodoWrite tracking. Stops on blockers. Calls finishing-a-development-branch at the end.
**Strength:** Solid execution discipline with checkpoint cadence.
**Gap:** No protected file awareness (Guardian). No rooster integration between tasks. No session memory (pgvector). No Linear issue tracking.

### 3. test-driven-development
**What it does:** Enforces RED → GREEN → REFACTOR. Iron Law: no production code without a failing test first. Delete code written before tests.
**Strength:** The most opinionated and best-written of the set. The rationalizations table is excellent.
**Gap:** All examples are TypeScript/JavaScript. No Python/pytest examples. No retail-specific test philosophy. No connection to "data accuracy" or "no hallucinating data" principles. No CRDM schema awareness.

### 4. systematic-debugging
**What it does:** 4-phase root cause investigation: investigate → pattern analysis → hypothesis → fix. 3-fix limit before questioning architecture.
**Strength:** The 3-fix architectural escalation rule is gold. The "gather evidence in multi-component systems" section maps well to our TSP pipeline.
**Gap:** No awareness of Canary's specific debugging surfaces (webhook integrity, TSP subscriber pipeline, PostgreSQL immutability constraints, MCP server health). No connection to data integrity principle.

### 5. verification-before-completion
**What it does:** Evidence before claims. Run the verification command, read the output, then claim the result. "Claiming work is complete without verification is dishonesty."
**Strength:** The strongest philosophical alignment with Jeffe's "verify before done" principle. Nearly 1:1 with ALX Behavior Rule #11.
**Gap:** No Jim's QA gate integration. No rooster test suite reference. No North Star check ("does this ease the merchant's stress?"). No canary-uat integration.

### 6. finishing-a-development-branch
**What it does:** Verify tests → present 4 options (merge/PR/keep/discard) → execute → cleanup worktree.
**Strength:** Clean workflow with good safety checks.
**Gap:** No canary-deploy pipeline integration. No Jim sign-off gate. No Factory Process stage tracking (QC → Packaging → Ship). No Linear issue update.

### 7. requesting-code-review
**What it does:** Dispatches a code-reviewer subagent with precise context (base SHA, head SHA, plan reference). Acts on Critical/Important/Minor feedback.
**Strength:** Good separation of concerns — reviewer gets clean context, not session history.
**Gap:** No Factory Process compliance check. No data integrity review. No brand template compliance check. No retail domain awareness.

---

## Inventory: Canary Custom Skills (13)

### Session Lifecycle (3)
| Skill | What It Does | Overlap with Obra |
|-------|-------------|-------------------|
| **alx-startup** | Bootstrap: stack health, git, env, guardian manifest, tunnel, memory recall, Linear | None — unique to Canary |
| **alx-session-close** | Teardown: Linear updates, pgvector memory store, timelog, Jeffe confirm | None — unique to Canary |
| **project-timelog** | Append session summary to daily timelog file | None — unique to Canary |

### Deployment & Infrastructure (3)
| Skill | What It Does | Overlap with Obra |
|-------|-------------|-------------------|
| **canary-deploy** | 7-step gated pipeline: dev (Mac Mini) → QA (iMac) | Partial overlap with `finishing-a-development-branch` at the ship stage |
| **canary-uat** | Quick health check: endpoints, login, static assets, routes, errors | None directly — verification-before-completion is philosophical, this is operational |
| **critical-file-guardian** | Protected file gate: approval → backup → edit → validate → manifest | None — unique to Canary |

### Testing (1)
| Skill | What It Does | Overlap with Obra |
|-------|-------------|-------------------|
| **rooster** | 4-layer E2E: unit, context integrity, feature patrol, Playwright. 295+ tests mapped to MVP Epics | Partial overlap with `test-driven-development` at the philosophy level, but rooster is execution, TDD is methodology |

### Content & Documentation (3)
| Skill | What It Does | Overlap with Obra |
|-------|-------------|-------------------|
| **content-extractor** | Harvest docs from Word/PDF/PPTX into markdown packages | None |
| **session-synthesis** | Synthesize Grok/AI brainstorm transcripts into structured session docs | None |
| **war-chest** | CMS for investor/public content. Catalog → Builder → Publisher | None |

### Team Operations (3)
| Skill | What It Does | Overlap with Obra |
|-------|-------------|-------------------|
| **remember-quote** | Capture CEO quotes with status tracking and keyword indexing | None |
| **founder-probe** | Surface biographical gems from Jeffe through natural follow-up probes | None |
| **canary-interview** | HRGirl candidate screening workflow | None |

---

## Overlap Map

```
OBRA SUPERPOWERS (generic)          CANARY CUSTOM (specific)
═══════════════════════             ═══════════════════════
writing-plans ─────────────────┐
executing-plans ───────────────┤    alx-startup (session bootstrap)
                               ├──▶ [GAP: no Canary-flavored plan/execute]
test-driven-development ───────┤    rooster (E2E testing execution)
                               ├──▶ [GAP: TDD + rooster not connected]
systematic-debugging ──────────┤
                               ├──▶ [GAP: no Canary debug surfaces]
verification-before-completion ┤    canary-uat (health check)
                               ├──▶ [GAP: verify + UAT not connected]
finishing-a-development-branch ┤    canary-deploy (7-step pipeline)
                               ├──▶ [OVERLAP: both handle "ship" stage]
requesting-code-review ────────┤
                               └──▶ [GAP: no Factory Process review]

[NOT IN OBRA — UNIQUE TO CANARY]
    alx-startup, alx-session-close, project-timelog
    critical-file-guardian
    content-extractor, session-synthesis, war-chest
    remember-quote, founder-probe, canary-interview

[NOT IN EITHER — INSPIRED BY GSTACK]
    plan-ceo-review → Jeffe taste check / vision alignment
    plan-eng-review → Tom-level architecture review
```

---

## Consolidation Plan: The Canary Factory Skills

**Goal:** Replace the 7 generic Obra Superpowers with 8 Canary-flavored versions that carry our DNA. Keep all 13 custom skills unchanged. The result is one unified set.

**Naming convention:** `canary-[function]` — lives in `.claude/skills/` alongside existing skills.

**Architecture:** Each skill follows the Factory Process stages and references Jeffe's principles where they naturally apply. Not forced — where the Obra skill is already good, we keep the structure and add the Canary context.

### Skill 1: `canary-blueprint` (replaces: writing-plans)
**Factory Stage:** Blueprint
**What changes:**
- Plans map to Factory Process stages (Blueprint → Parts → Assembly → QC → Packaging → Ship)
- Every plan requires a GRO issue number or explicit Jeffe directive
- Scope check against the 27-feature MVP freeze (Non-Negotiable #7)
- File structure section includes Guardian-protected file flags
- Tech stack locked to: Python 3.12 / Flask / SQLAlchemy 2.0 / PostgreSQL 17 / Valkey 8
- Data integrity checkpoint in every plan that touches canary_sales (INSERT-only, no UPDATE, no DELETE)
- Plan header includes CRDM schema references where relevant
- Saves to `docs/superpowers/plans/` (existing convention preserved)

**Jeffe quote baked in:**
> "Documents first, then build and tie it all together soup to nuts in a factory process."

### Skill 2: `canary-assembly` (replaces: executing-plans)
**Factory Stage:** Assembly
**What changes:**
- Calls `alx-startup` context (memory recall, Linear status) before execution
- Guardian enforcement for protected files during execution
- Rooster smoke test between major tasks (Quick Crow layer)
- Stop-and-retriage rule: if something goes sideways, STOP → re-read TRIAGE.md → re-plan (ALX Behavior Rule #2)
- Linear issue status updates at task boundaries
- Session memory writes for decisions made during execution

**Jeffe quote baked in:**
> "If this thing works we might have to rebuild everything and consume months of costs because I was lazy."

### Skill 3: `canary-tdd` (replaces: test-driven-development)
**Factory Stage:** Parts (test-first manufacturing)
**What changes:**
- All examples rewritten for Python 3.12 / pytest / SQLAlchemy 2.0
- Data accuracy principle woven into test philosophy: "We can't have any hallucinating data. But this is all math, and solvable, verifiable math."
- CRDM schema tests: every model change includes a test that verifies INSERT-only constraints on canary_sales
- Retail-specific test examples (webhook verification, alert threshold, drawer variance calculation)
- Rooster integration: new tests map to Epic markers (@pytest.mark.e0 through @pytest.mark.e3)
- The "people's lives and jobs" principle as the moral anchor for why TDD matters here

**Jeffe quote baked in:**
> "When we accuse someone, we have to be sure. The data model enforces this at the database level — immutable evidence, hash verification, chain of custody, append-only timeline. This isn't just a software feature. It's an ethical obligation."

### Skill 4: `canary-debug` (replaces: systematic-debugging)
**Factory Stage:** QC (defect investigation)
**What changes:**
- Canary-specific debugging surfaces added to Phase 1:
  - TSP pipeline: check each subscriber (Sub 1 seal, Sub 2 parse, Sub 3 anchor)
  - Webhook integrity: verify HMAC signatures, check for dropped events
  - PostgreSQL immutability: verify INSERT-only triggers haven't been bypassed
  - MCP server health: check all 12 canary-* MCP servers
  - Valkey cache state: check for stale/corrupt cache entries
- 3-fix escalation routes to Tom (architecture) not generic "question the architecture"
- Data flow tracing follows the CRDM: canary_app → canary_sales → canary_metrics
- "The problem was never the people. The problem was the log." as the debugging North Star

**Jeffe quote baked in:**
> "At the end of the day we are generating metrics and serving up dashboards — they have to be accurate."

### Skill 5: `canary-verify` (replaces: verification-before-completion)
**Factory Stage:** QC → Packaging gate
**What changes:**
- Jim's QA veto gate is the ultimate verification: "ALX never routes a release without Jim's signature"
- Rooster test layers as verification evidence (not just "run tests" — specify which layer)
- North Star check added: "Does this feature ease the merchant's stress or add to it?"
- canary-uat integration: run health check as part of verification
- Brand template compliance check for any rendered output
- Linear issue acceptance criteria check before claiming done

**Jeffe quote baked in:**
> "We don't want to add to the stress. We want to ease it."

### Skill 6: `canary-ship` (replaces: finishing-a-development-branch)
**Factory Stage:** Packaging → Ship
**What changes:**
- Integrates with canary-deploy (7-step gated pipeline) instead of generic git workflow
- Jim sign-off gate is a hard dependency before ship
- Factory Process gate enforcement: no ship without passing through Blueprint → Parts → Assembly → QC → Packaging
- Linear issue transitions (In Progress → In Review → Done)
- Session close triggers: timelog, TRIAGE.md update, HANDOFF.md if cross-agent
- External comms check: if this touches anything public, Syd reviews, Jeffe approves (Non-Negotiable #6)

**Jeffe quote baked in:**
> "Documents first, then build and tie it all together soup to nuts in a factory process."

### Skill 7: `canary-review` (replaces: requesting-code-review)
**Factory Stage:** QC (peer review)
**What changes:**
- Review checklist includes Factory Process compliance (was there a Blueprint? Were Parts tested first?)
- Data integrity review: does this change touch canary_sales? If so, verify INSERT-only preserved
- Infrastructure integrity review: any new dependency evaluated against open license, Bitcoin-native alignment, production-grade, no rebuild risk (Non-Negotiable #10)
- Brand template compliance for any rendered output
- Retail domain awareness: reviewer considers merchant impact
- Review feedback routes through ALX dispatch (not generic "fix Critical issues")

### Skill 8: `jeffe-review` (NEW — inspired by gstack plan-ceo-review)
**Factory Stage:** Blueprint (vision alignment gate)
**What changes from gstack:**
- Three modes preserved: SCOPE EXPANSION / HOLD SCOPE / SCOPE REDUCTION
- But the review philosophy is Jeffe's, not Garry Tan's:
  - "Does this serve the merchant who's losing $12,800/year and doesn't know it?"
  - "Does this move us toward the gLog — the permanent successor to the tLog?"
  - "Is this Bitcoin-native by design, or are we bolting it on later?"
  - "Would this survive the trust collapse? When AI can fake any document, does our proof still hold?"
  - "Does this create the data platform the merchant stays for after they signed up for LP?"
- The one-line test from the Manifesto: "Does this work help GrowDirect mint the pool, seal the event, or collect the sat? If yes — ship it. If no — park it."
- North Star check: "We don't want to add to the stress. We want to ease it."
- Component Business Model check: does this serve the matrix (capabilities × verticals)?

---

## CLAUDE.md Workflow Table Update

Current:
```
| Activity | Skill | Key Enforcement |
|---|---|---|
| Any feature or bugfix | test-driven-development | Test-first. RED before GREEN. |
| Debugging | systematic-debugging | Root cause before fix. 3-fix limit. |
| Plan execution | executing-plans | TodoWrite tracking. Stop on blockers. |
| Before claiming done | verification-before-completion | Evidence before assertions. |
| Branch completion | finishing-a-development-branch | Tests pass → options → cleanup. |
| Code review | requesting-code-review | After each task, before merge. |
```

Proposed:
```
| Activity | Skill | Key Enforcement |
|---|---|---|
| Vision / scope check | canary:jeffe-review | North Star + one-line test + Factory stage gate |
| Writing plans | canary:canary-blueprint | GRO issue, MVP freeze check, Factory stages, data integrity |
| Any feature or bugfix | canary:canary-tdd | Test-first. RED before GREEN. People's lives and jobs. |
| Debugging | canary:canary-debug | Root cause. 3-fix limit. TSP pipeline awareness. |
| Plan execution | canary:canary-assembly | Guardian, rooster between tasks, stop-and-retriage. |
| Before claiming done | canary:canary-verify | Jim's gate. Rooster evidence. North Star check. |
| Code review | canary:canary-review | Factory compliance. Data integrity. Infrastructure check. |
| Branch completion | canary:canary-ship | canary-deploy pipeline. Jim sign-off. Linear update. |
| Deploy to QA | canary-deploy | 7-step gated pipeline. (unchanged) |
| E2E testing | rooster | 4-layer test suite. (unchanged) |
```

---

## Build Order

Skills should be built in dependency order. Each skill is usable independently, but they reference each other:

| Priority | Skill | Depends On | Estimated Effort |
|----------|-------|------------|-----------------|
| 1 | `canary-blueprint` | None | Medium — rewrite writing-plans with Factory Process |
| 2 | `canary-tdd` | None | Medium — port examples to Python, add data integrity |
| 3 | `canary-assembly` | canary-blueprint, canary-tdd | Medium — integrate with alx-startup, Guardian, rooster |
| 4 | `canary-debug` | None | Small — add Canary surfaces to existing 4-phase |
| 5 | `canary-verify` | canary-tdd, rooster | Small — tightest skill, mostly adding gates |
| 6 | `canary-review` | canary-blueprint | Medium — build review checklist with Factory compliance |
| 7 | `canary-ship` | canary-deploy, canary-verify | Small — bridge existing canary-deploy with branch workflow |
| 8 | `jeffe-review` | canary-blueprint | Large — most original writing, Jeffe voice throughout |

---

## What Stays Unchanged

These 13 custom skills are clean and don't need consolidation:

| Skill | Reason |
|-------|--------|
| alx-startup | Unique session bootstrap — no overlap |
| alx-session-close | Unique session teardown — no overlap |
| project-timelog | Unique operational logging — no overlap |
| canary-deploy | Stays as-is; canary-ship will call it |
| canary-uat | Stays as-is; canary-verify will call it |
| critical-file-guardian | Stays as-is; canary-assembly will enforce it |
| rooster | Stays as-is; multiple skills will reference it |
| content-extractor | Unique content tool — no overlap |
| session-synthesis | Unique brainstorm tool — no overlap |
| war-chest | Unique CMS — no overlap |
| remember-quote | Unique CEO capture — no overlap |
| founder-probe | Unique interview tool — no overlap |
| canary-interview | Unique HR tool — no overlap |

---

## What Gets Retired

Once the Canary-flavored skills are built and tested:

| Obra Skill | Replaced By | Action |
|------------|-------------|--------|
| writing-plans | canary-blueprint | Remove from CLAUDE.md workflow table |
| executing-plans | canary-assembly | Remove from CLAUDE.md workflow table |
| test-driven-development | canary-tdd | Remove from CLAUDE.md workflow table |
| systematic-debugging | canary-debug | Remove from CLAUDE.md workflow table |
| verification-before-completion | canary-verify | Remove from CLAUDE.md workflow table |
| finishing-a-development-branch | canary-ship | Remove from CLAUDE.md workflow table |
| requesting-code-review | canary-review | Remove from CLAUDE.md workflow table |

The Obra skills remain installed globally for other projects. They just stop being referenced in Canary's CLAUDE.md.

---

## The DNA That Gets Baked In

Every Canary skill carries these principles. Not as a preamble — woven into the instructions where they naturally apply:

### From Jeffe (Quotes & Manifesto)
- **Data Integrity Principle:** "We treat data integrity with the utmost seriousness. This is people's lives and jobs we are analyzing. If we accuse someone, we have to be sure and have the facts."
- **Factory Process:** "Documents first, then build and tie it all together soup to nuts in a factory process."
- **Product North Star:** "We don't want to add to the stress. We want to ease it."
- **Infrastructure Integrity:** "If this thing works we might have to rebuild everything and consume months of costs because I was lazy."
- **Data Accuracy:** "At the end of the day we are generating metrics and serving up dashboards — they have to be accurate. We can't have any hallucinating data."
- **Hiring Philosophy:** "I'm not looking for pedigrees necessarily — I want work ethic and teachable."
- **The One-Line Test:** "Does this work help GrowDirect mint the pool, seal the event, or collect the sat?"

### From the Factory Process
- Blueprint → Parts → Assembly → QC → Packaging → Ship
- No stage skipped. No code without a spec. No ship without Jim's sign-off.
- PRD → AC → Jim's test → Rooster → green → ship.

### From the Through-Line
- The tLog was broken. The gLog fixes it. Every design decision flows from this.
- INSERT-only. Append-only. Immutable by physics, not by policy.
- "The problem was never the people. The problem was the log."

### From the Operating Model
- GRO issue or explicit Jeffe directive — no work without a ticket
- ALX dispatches with authority; agents own their domain decisions
- Jim's QA veto is non-negotiable
- External comms: Syd reviews, Jeffe approves. Always.

---

*Audit Version: 1.0*
*Maintained by: ALX*
*Next step: Jeffe reviews and selects build order. First skill gets built same session or next.*
