# Factory Pipeline

> **Status:** Complete — written from code
> **Namespace:** platform
> **Last updated:** 2026-03-30
> **Code location:** `factory-manifest.json`, `.claude/skills/factory-*.md`

---

## 1. Overview

The Factory Pipeline is GrowDirect's standardized nine-stage process for
delivering software changes across all platform apps. It is not a CI/CD system
— it is a cognitive workflow that headless builder agents follow to take a
Linear issue from intake to ship with consistent quality, testability, and
traceability.

Every piece of work executed by a builder agent runs through the same pipeline:
Preflight, Research, Blueprint, TDD, Assembly, Verify, QA, Ship, Close. Each
stage has defined inputs, outputs, required MCP integrations, and a corresponding
skill file that specifies exactly how the agent should execute that stage.

The pipeline has two primary design goals:

1. **Consistency** — any builder working on any app produces outputs that look
   the same and meet the same standards, regardless of the domain.

2. **Traceability** — every stage gate produces an artifact (report, plan, test
   result, commit) that can be inspected after the fact. Nothing happens without
   leaving evidence.

The pipeline is declared in `factory-manifest.json` at the repo root and
implemented through skill files in `.claude/skills/factory-*.md`. App-specific
variants (e.g., `canary-blueprint.md`, `cove-tdd.md`) delegate to the factory
base skills and add domain-specific guardrails on top.

---

## 2. Architecture

### Component Diagram

```
Linear (GRO Issue)
    |
    v
[factory-preflight]  <-- reads factory-manifest.json, CLAUDE.md files, memory bus
    |
    v
[factory-research]   <-- memory bus, GitNexus, Obsidian, Firecrawl (all optional)
    |
    v
[factory-blueprint]  <-- produces docs/plans/{date}-{slug}.md
    |                    Linear: issue moved to "In Progress"
    v
[factory-tdd]        <-- produces failing tests in tests/
    |
    v
[factory-assembly]   <-- implements to make tests pass, commits per task
    |
    v
[factory-verify]     <-- full test suite run, migration check, diff review
    |
    v
[factory-qa]         <-- route testing, auth check, standards compliance
    |
    v
[factory-ship]       <-- git push, Linear update to "Done"
    |
    v
[factory-close]      <-- session summary, memory writes, post-mortem (if shipping)
```

Supporting skills used at stage boundaries:

```
factory-linear     -- Linear MCP operations (preflight / blueprint / ship / close)
factory-postmortem -- Post-mortem capture (invoked by factory-close after ship)
factory-newapp     -- New app scaffolding (used once per new product, not per feature)
```

### Request / Data Flow

A complete pipeline run starts with a GRO issue identifier provided by ALX
(the dispatcher). Data flows forward through the pipeline as structured
artifacts:

```
GRO Issue ID
  → preflight_report         (infra status, app context, issue metadata)
    → context_bundle         (prior art from memory bus / GitNexus / docs)
      → docs/plans/{slug}.md (blueprint — architecture decisions, task list)
        → tests/             (failing tests, one per behavior)
          → implementation   (code changes, one commit per task)
            → verify_report  (test counts, regressions, migration status)
              → qa_report    (route test results, compliance findings)
                → git_push   (pushed branch, Linear updated)
                  → session_summary (close artifacts, memory writes)
```

Each stage consumes the output of the preceding stage. A stage that cannot
proceed because a prior artifact is missing or failed must stop and report —
it must not skip forward.

### Key Design Decisions

**No GRO issue = no work.**
The pipeline cannot start without a Linear issue. The preflight skill enforces
this by calling `get_issue` at startup. An issue that doesn't exist, is already
Done, or is Cancelled causes an immediate STOP.

**Sequential, not parallel.**
Stages run in strict order. TDD cannot start until blueprint is confirmed.
Assembly cannot start until TDD is complete and tests are failing. This
sequencing is the mechanism that prevents the "lazy pipe" anti-pattern — half-
built features with no tests and no end-to-end verification.

**App context determines which skill variant runs.**
The preflight stage identifies the target app (Canary, Cove, or Platform). From
blueprint onward, the app-specific override skill is used instead of the factory
base. The override delegates to the base and adds domain checks (PCI awareness
for Canary, Davis-Stirling compliance for Cove).

**Linear is the message bus.**
All stage transitions are communicated to Linear. Blueprint moves the issue to
"In Progress". Ship moves it to "Done". Close posts the session summary as a
comment. This means ALX can monitor pipeline status by reading Linear without
being in the builder's session.

**Gate conditions are binary.**
Each stage either passes completely or stops the pipeline. There is no partial
pass. A RED status at preflight stops everything. A failing test at verify
stops progress to QA. This is intentional — partial progress creates more work
than stopping and fixing does.

---

## 3. Data Model

The factory pipeline has no database tables. It is a configuration-driven
orchestration layer. The authoritative schema is `factory-manifest.json`.

### factory-manifest.json Schema

```json
{
  "version": "string",               // Schema version, currently "1.0"
  "pipeline": ["string"],            // Ordered list of stage names (9 entries)
  "stages": {
    "<stage_name>": {
      "replaces": "string",          // Optional: prior skill this stage supersedes
      "inputs": ["string"],          // Artifact names this stage requires
      "outputs": ["string"],         // Artifact names this stage produces
      "required_mcps": ["string"],   // MCPs that must be available (STOP if missing)
      "optional_mcps": ["string"],   // MCPs used if available, skipped gracefully if not
      "checks": ["string"],          // Named infrastructure checks (preflight only)
      "skill": "string",             // Skill file name (without .md extension)
      "eval": "string",              // Path to eval suite (relative to repo root)
      "eval_threshold": 0.0          // Minimum pass rate (0.0–1.0)
    }
  },
  "apps": {
    "<app_name>": {
      "compliance": "string",        // Compliance regime (pci-awareness, davis-stirling)
      "overrides": ["string"],       // Stages with app-specific override skills
      "domain_skills": {             // App-specific non-pipeline skills
        "<skill_name>": {
          "skill": "string",         // Skill file name
          "module": "string",        // Python module path this skill evaluates
          "eval": "string",          // Eval file path
          "eval_threshold": 0.0      // Minimum pass rate
        }
      }
    }
  }
}
```

### Current pipeline declaration

```json
["preflight", "research", "blueprint", "tdd", "assembly", "verify", "qa", "ship", "close"]
```

### Stage definitions (current state)

| Stage | Required MCPs | Optional MCPs | Skill | Eval |
|-------|---------------|---------------|-------|------|
| preflight | linear | memory-bus | factory-preflight | evals/skills/test_platform_preflight.py |
| research | — | memory-bus, gitnexus, obsidian, firecrawl | — | — |
| blueprint | linear | memory-bus | — | — |
| tdd | — | — | — | — |
| assembly | — | — | — | — |
| verify | — | — | — | — |
| qa | — | — | — | — |
| ship | linear | — | — | — |
| close | linear | memory-bus | — | — |

Note: Only `preflight` has a skill and eval fully declared in the manifest.
The remaining stages have skill files implemented but not yet wired into the
manifest with `skill` and `eval` fields. See Section 11 (Known Issues).

### App override declarations

| App | Compliance | Override stages |
|-----|-----------|-----------------|
| canary | pci-awareness | preflight, blueprint, tdd, assembly, verify, qa, ship, close |
| cove | davis-stirling | preflight, blueprint, tdd, assembly, verify, qa, ship, close |

### Domain skills (Cove only)

| Skill | Module | Eval | Threshold |
|-------|--------|------|-----------|
| cove-quorum | cove.governance.quorum | evals/skills/test_quorum_calculator.py | 0.90 |

### Eval threshold semantics

- `1.0` — 100% pass rate required. Used for binary infrastructure checks
  (preflight) where any failure means the environment is broken.
- `0.90` — 90% pass rate required. Used for domain logic skills with a mix of
  binary checks and LLM-as-judge assertions where partial passage is acceptable.

---

## 4. Interfaces

### Skill invocation interface

Factory skills are Markdown files consumed by Claude Code at runtime. They are
not callable functions — they are instructions the builder agent reads and
follows. The invocation interface is natural language within a Claude Code
session.

**Direct invocation (via slash command or Skill tool):**
```
/factory-preflight
/factory-research
/factory-blueprint
... etc.
```

**App-specific invocation:**
```
/canary-preflight   -- delegates to factory-preflight, adds Canary checks
/cove-blueprint     -- delegates to factory-blueprint, adds Cove compliance
```

### Stage inputs and outputs

Each stage declares its expected inputs and the artifacts it produces. The
builder is responsible for ensuring prior stage outputs exist before proceeding.

| Stage | Inputs | Outputs |
|-------|--------|---------|
| preflight | gro_issue | preflight_report |
| research | gro_issue, preflight_report | context_bundle |
| blueprint | gro_issue, preflight_report, context_bundle | docs/plans/{date}-{slug}.md |
| tdd | plan | tests/ (failing test files) |
| assembly | plan, failing_tests | implementation (committed code) |
| verify | implementation | verify_report |
| qa | verify_report | qa_report |
| ship | qa_report | git_push, linear_update |
| close | ship_result | session_summary |

### factory-linear invocation points

`factory-linear` is a support skill called by other factory skills at stage
transitions. Builders do not call it directly. Invocation points:

| Stage | Action |
|-------|--------|
| preflight | `get_issue` — read and validate the GRO issue |
| blueprint | `save_issue` (→ In Progress), `create_document` (plan attachment) |
| ship | `save_comment` (ship report), `save_issue` (→ Done) |
| close | `save_comment` (session summary) |

### Preflight report format

```
Preflight: [GREEN/YELLOW/RED]
  Docker:     [status]
  PostgreSQL: [status]
  Valkey:     [status]
  Ollama:     [status]
  Git:        [status]
  Linear:     [status]
  Memory Bus: [status]

App: [canary / cove / platform]
Branch: [current branch]
Task: GRO-XXX — [title]

[Any YELLOW warnings listed here]
```

### Verify report format

```
Tests: [N] passed, [N] failed, [N] skipped
New tests: [N]
Regressions: none / [list any]
Migrations: [applied / not needed]
Diff: [matches plan / deviations noted]
```

---

## 5. Service Layer

This section documents each factory skill: its purpose, when it runs, what it
reads, what it produces, and its key behavioral rules.

### factory-preflight

**File:** `.claude/skills/factory-preflight.md`
**Position:** Stage 1 — runs before any other stage
**Replaces:** factory-startup

**Purpose:** Verify the build environment is healthy before any work begins.
Load context so the builder doesn't waste time discovering the environment is
broken mid-task.

**Trigger:** Invoked at the start of every factory session, regardless of which
stage the builder is entering.

**Inputs:** GRO issue identifier (from ALX dispatch)

**Outputs:** preflight_report (structured GREEN/YELLOW/RED status for each
infrastructure component, plus app context and issue metadata)

**Infrastructure checks (from manifest `checks` field):**
- `docker` — all four growdirect containers running (postgres, valkey, ollama, pgadmin)
- `postgres` — accepting connections, `pg_isready` returns 0
- `valkey` — responds to PING
- `ollama` — reachable and `qwen3-embedding:8b` model loaded
- `git_clean` — working tree clean (YELLOW if dirty, RED if not a repo)
- `gro_exists` — Linear issue exists and is not Done/Cancelled

**Gate rule:** Any RED status stops the pipeline immediately. The builder
reports what is broken and how to fix it. YELLOW statuses allow the pipeline
to continue with a warning logged in the report.

**Context loading (after checks pass):**
1. Reads `~/GrowDirect/CLAUDE.md` (platform standards)
2. Reads the app's `CLAUDE.md` if working in an app directory
3. Reads `factory-manifest.json`
4. Loads GRO issue from Linear via `factory-linear`
5. Queries memory bus for prior art (skips gracefully if not running)

**App identification:** The builder determines which app the work targets from
the GRO issue's project field, the current working directory, or explicit user
input. This determines which `{app}-{stage}.md` override skills apply going
forward.

**Eval:** `evals/skills/test_platform_preflight.py`, threshold 1.0 (100%)

---

### factory-research

**File:** `.claude/skills/factory-research.md`
**Position:** Stage 2 — between preflight and blueprint

**Purpose:** Gather prior art and existing context so the blueprint doesn't
start from scratch. Prevents re-solving problems that have already been solved.

**Trigger:** Invoked after a passing preflight, before blueprint writing.

**Inputs:** gro_issue, preflight_report

**Outputs:** context_bundle (structured markdown document with prior decisions,
domain context, code impact, and external references)

**Sources (all independently optional, graceful degradation):**
- **Memory bus** — `memory_recall(query)` for prior decisions, then
  `context_assemble(topic, gro_issue)` for domain context. Skipped if memory
  bus is not running (YELLOW from preflight).
- **GitNexus** — `gitnexus_impact` for blast radius on key symbols,
  `gitnexus_query` for architecture context. Skipped if not configured.
- **Obsidian** — notes related to the GRO issue domain. Skipped if not
  configured.
- **Firecrawl** — third-party API documentation (Square, Stripe, etc.) for
  issues involving external integrations. Skipped if not configured.

**Key principle:** Research must never block the pipeline. If all sources
fail, blueprint proceeds without context — the same as before this stage
existed. Research adds value when sources are available; its absence is not
an error.

**Fallback output if no sources available:**
```
No prior context found. Blueprint starts from scratch.
```

**Eval:** Not yet defined in manifest.

---

### factory-blueprint

**File:** `.claude/skills/factory-blueprint.md`
**Position:** Stage 3 — produces the implementation plan

**Purpose:** Specify exactly what will be built before any code is written.
The blueprint is the contract between the planning stage and the execution
stages. It prevents scope creep, captures architectural decisions, and provides
the task list that assembly follows.

**Trigger:** After research completes (or after preflight if research is
skipped). Requires explicit confirmation from ALX before proceeding to TDD.

**Inputs:** gro_issue, preflight_report, context_bundle

**Outputs:** `docs/plans/{date}-{slug}.md` — a structured plan document.
Linear issue moved to "In Progress" via `factory-linear`.

**Required content:**
- Plan header with GRO number, date, app, issue URL, and one-sentence goal
- Architecture section answering: models needed, routes (URL + method + auth),
  service functions, templates, test scenarios, migration needed?
- File structure table (action, file path, responsibility)
- Numbered task list — max 8 tasks, each completable in 2–5 minutes
- Protected files checklist (justified if any touched)
- Quality checklist (no SQLite, Mapped[] syntax, @login_required, no secrets,
  no CDN, component CSS classes only)

**Task format:** Each task specifies: write failing test, confirm it fails,
implement, confirm it passes, run smoke tests, commit.

**Split rule:** If a plan requires more than 8 tasks, it must be split into
two GRO issues. This enforces scope discipline at the planning stage.

**Cross-app check:** Before designing a solution, the builder checks whether
the other app already solved the same problem (CLAUDE.md Hard Rule 8).

**Document filing:** Plans are working documents stored in `docs/plans/` for
the session. Lasting artifacts (ADRs, SDDs) are filed per the document filing
rules in CLAUDE.md.

**Gate:** Requires confirmation before moving to TDD. This is the human review
point in the pipeline.

---

### factory-tdd

**File:** `.claude/skills/factory-tdd.md`
**Position:** Stage 4 — writes all tests before any implementation

**Purpose:** Enforce test-first development. Every behavior gets a test written
before the code that satisfies it. Tests that pass before implementation is
written indicate either a broken test or a feature that already exists.

**Trigger:** After blueprint is confirmed.

**Inputs:** plan (the blueprint document)

**Outputs:** `tests/` — a set of failing test files

**The TDD cycle (per behavior):**
1. Write one test in the correct file (`tests/unit/`, `tests/integration/`,
   or `tests/smoke/`)
2. Run it — confirm it fails (acceptable failures: ImportError, AttributeError,
   assertion failure)
3. Write minimal implementation — only enough to make this one test pass
4. Run it — confirm it passes
5. Run smoke tests to catch regressions
6. Commit: `git commit -m "test: <behavior> (GRO-XXX)"`

**Test naming convention:** `test_<what>_<condition>_<expected>`

**Minimum coverage per feature:**
- Happy path (valid input, expected success)
- Validation error (bad input, expected failure)
- Auth required (unauthenticated → 302 to login)
- Not found (missing UUID → 404)

**Fixtures:** Use `conftest.py` fixtures. Do not create inline test databases
or test users. Standard fixtures: `app`, `client`, `authenticated_client`,
`db_session`, sample model objects.

**Split rule:** "and" in a test name = two behaviors = two tests.

**Gate:** Do not move to factory-assembly until all tests are written and
failing for the correct reason. A test that passes before implementation is
a defect in the test.

---

### factory-assembly

**File:** `.claude/skills/factory-assembly.md`
**Position:** Stage 5 — implements the blueprint tasks

**Purpose:** Execute the blueprint task list to make the TDD tests pass.
Implementation is incremental: one task at a time, test after each, smoke
test after each task, commit per logical unit.

**Trigger:** After all TDD tests are written and failing.

**Inputs:** plan (blueprint), failing_tests

**Outputs:** implementation (code changes, one commit per task)

**Task loop (per task in blueprint order):**
1. Read the task — understand what it requires before touching any file
2. Execute the change described
3. Run the specific test: `python3 -m pytest tests/path/test_file.py::test_name -v`
   — if it fails, stop, diagnose, fix, re-run. Do not skip.
4. Run smoke tests: `python3 -m pytest tests/ -k smoke -v`
   — if smoke breaks, a regression was introduced. Fix before continuing.
5. Commit: `git add <specific files> && git commit -m "feat: <task> (GRO-XXX)"`

**Commit discipline:** One commit per task, not one commit at the end of all
tasks. Granular commits make regressions easy to isolate.

**Failure protocol:** Stop immediately. Read the error in full. Check the
relevant model/service/route for the cause. Fix and re-run — do not skip or
work around. If the fix is outside scope, create a new Linear issue and return
to the original task.

**Scope control:** Bugs found outside the current GRO issue are noted, a new
Linear issue is created, and the finding is not fixed inline. Scope creep is
treated as a defect.

**Done condition:** All tests from TDD are green. Smoke tests pass. Every task
has a commit.

---

### factory-verify

**File:** `.claude/skills/factory-verify.md`
**Position:** Stage 6 — full verification before QA

**Purpose:** Prove that the complete test suite passes, no regressions were
introduced, all new code has tests, and any migrations are applied cleanly.

**Trigger:** After assembly completes (all tasks done, all tests passing).

**Inputs:** implementation (assembled codebase)

**Outputs:** verify_report

**Verification steps:**
1. Run full test suite: `python3 -m pytest tests/ -v` — paste actual output,
   do not summarize. Evidence before assertions.
2. Regression check: compare test counts before and after. Any previously
   passing test now failing = regression. Fix before proceeding.
3. Coverage check: for every new file or function added during assembly, confirm
   there is a test covering the happy path and at least one error path.
4. Migration check (if models changed): `alembic upgrade head` must succeed.
   If migration is missing, generate it, review the output, then commit.
5. Diff check: `git diff HEAD~<n> --stat` — does the set of changed files
   match what the blueprint planned? Unexpected changes must be investigated.

**Key rule:** Do not proceed to QA with any failures. The verify report must
show zero failures before QA begins.

---

### factory-qa

**File:** `.claude/skills/factory-qa.md`
**Position:** Stage 7 — quality assurance pass

**Purpose:** Verify that new and modified functionality works correctly at the
HTTP level, meets platform standards, and does not introduce compliance or
security issues.

**Trigger:** After verify_report shows clean results.

**Inputs:** verify_report

**Outputs:** qa_report (findings per check category)

**QA checks:**

**Route testing** (for every new or modified route):
- Hit it — does it return the expected response?
- Submit valid form data — does it succeed?
- Submit invalid/missing data — does it show inline errors below each field?
- Hit it unauthenticated — does it redirect to login?

**Auth check:**
- Every non-public route must have `@login_required`. No exceptions.
- Check by grepping each modified blueprint file for route definitions.

**Standards compliance:**
- Models: `Mapped[]` type annotations (no `Column()`), UUID primary key,
  `created_at` and `updated_at` on every table
- Config: no hardcoded secrets (everything from `os.environ`), no SQLite
  references

**CSS compliance:**
- Templates use component classes from `static/css/<appname>.css`
- No raw Tailwind utility chains in templates
- No CDN `<script>` or `<link>` tags — all JS/CSS from npm build pipeline

**Protected files audit:**
- List every protected file touched during this GRO issue
- Confirm each change was necessary for the feature (not incidental) and minimal

**Rule:** Any finding in QA is fixed before ship. QA findings are not carried
into the next session.

---

### factory-ship

**File:** `.claude/skills/factory-ship.md`
**Position:** Stage 8 — deployment preparation and push

**Purpose:** Execute the final checklist before pushing to remote. Ensure the
branch is clean, commits are well-formed, migrations are applied, and Linear
reflects the work is done.

**Trigger:** After QA passes with no outstanding findings.

**Inputs:** qa_report

**Outputs:** git_push (branch pushed to remote), linear_update (issue → Done)

**Pre-ship checklist:**
1. Final test run — paste summary line. Zero failures required.
2. Migrations — `alembic upgrade head` must complete without errors. Confirm
   with `alembic current`.
3. Git log review — `git log --oneline origin/main..HEAD`. Every commit must
   reference the GRO issue number. No "fix", "wip", or "changes" commit
   messages.
4. No uncommitted changes — `git status` must show a clean working tree.
5. Push to remote — `git push origin <branch>`
6. Update Linear — move issue to "Done" (or "In Review" if PR review is
   required). Post comment with commit range or PR link via `factory-linear`.

**Rule:** No force-push to main.

---

### factory-close

**File:** `.claude/skills/factory-close.md`
**Position:** Stage 9 — session teardown

**Purpose:** Produce a structured record of what was accomplished, what was
not completed, and what new issues were discovered. Invoke post-mortem capture
if this was a shipping session.

**Trigger:** After ship completes (or at end of any session, even if ship
was not reached).

**Inputs:** ship_result (or current session state if ship was not reached)

**Outputs:** session_summary

**Close actions:**
1. Session summary — list files created or modified, tests written and passing,
   features delivered (tied to GRO issue), migrations added
2. Pending items — what was not completed, why, and what the next step is
3. New issues — any bugs or gaps found outside the current GRO scope. Create
   a Linear issue for each. Do not fix inline.
4. Post-mortem — if this session ended with a ship, invoke `factory-postmortem`
5. Document filing verification — confirm all documents created this session
   are filed correctly per CLAUDE.md document filing rules. No homeless docs.

**Close output format:**
```
Session done. Completed: [list]. Pending: [list or none]. New issues: [GRO numbers or none].
```

---

### factory-linear

**File:** `.claude/skills/factory-linear.md`
**Position:** Support skill — invoked by other factory skills at stage boundaries

**Purpose:** Standardize all Linear read/write operations. All Linear MCP
calls from the factory pipeline go through this skill.

**Not invoked directly** by builders. Called by preflight, blueprint, ship,
and close skills.

**Operations by stage:**

| Stage | Operation | Tools used |
|-------|-----------|-----------|
| preflight | Read and validate GRO issue | `get_issue` |
| blueprint | Move to "In Progress", attach plan | `list_issue_statuses`, `save_issue`, `create_document` |
| ship | Post ship report, move to "Done" | `save_comment`, `list_issue_statuses`, `save_issue` |
| close | Post session summary comment | `save_comment` |

**Error handling:** If Linear MCP is unreachable at any stage, log a warning
("Linear MCP unreachable — skipping [action]") and continue the pipeline.
Linear integration is important but not blocking. The skipped action is noted
in the session summary for manual follow-up.

---

### factory-postmortem

**File:** `.claude/skills/factory-postmortem.md`
**Position:** Support skill — invoked by factory-close for shipping sessions only

**Purpose:** Extract lessons learned from the build cycle and store them as
structured memories. Produce a permanent record that feeds platform
improvements.

**Trigger:** Invoked by factory-close only when a ship has completed
successfully. Not invoked for research-only, blueprint-only, or aborted sessions.

**Process:**
1. Gather session data — GRO issues, git diff (files and tests), decisions
   made, problems encountered, anything surprising
2. Write post-mortem to `docs/post-mortems/YYYY-MM-DD-<feature-slug>.md`
3. Store significant lessons to the memory bus with correct layer tags
4. Post summary comment on the Linear issue with link to post-mortem file

**Post-mortem document structure:**
- What shipped (specific deliverables with file paths)
- What worked
- What didn't
- What to change (concrete, not aspirational)
- Decisions made (with rationale — these become memory entries)
- Metrics (tests written, pass rate, files created/modified, eval score)

**Memory layer tagging:**

| Memory type | Layer | When to use |
|-------------|-------|-------------|
| decision | App or corp | Choices that affect future work |
| finding | App | Bugs found, gaps identified, surprising behavior |
| architecture | App or corp | Structural codebase changes |
| procedure | Corp | New workflows or process changes |

**Human gate:** The agent writes the post-mortem. Jeffe decides what gets
promoted to platform standards. The agent does NOT update
`~/GrowDirect/CLAUDE.md` — that file has a human gate.

---

### factory-newapp

**File:** `.claude/skills/factory-newapp.md`
**Position:** Out-of-band — not part of the nine-stage feature pipeline

**Purpose:** Scaffold a new GrowDirect platform app from proven patterns.
Used when starting a new product, not when building features in an existing app.

**Trigger:** "new app", "new project", "scaffold", "prototype", "spin up",
"start a new", "platform template"

**Seven-step process:**
1. Define the domain (app name, one-liner, primary entity, users, compliance)
2. Create the repo and directory structure
3. Copy the platform skeleton (app factory, extensions, config, Docker compose)
4. Create security and compliance documents (data retention, encryption,
   breach notification, privacy policy, terms)
5. Write CLAUDE.md before building features
6. Create app-specific factory skill overrides
7. Build the first domain-specific feature

**Key constraints enforced:**
- App connects to shared GrowDirect Postgres and Valkey (does not run its own)
- Docker compose must declare `name: <appname>` (prevents project name collision)
- Every service with `build:` must declare `image: <appname>-<service>`
  (prevents image tag collision)
- Port and Valkey DB number registered in platform CLAUDE.md

---

## 6. Configuration

### Eval thresholds

| Skill | Eval file | Threshold | Type |
|-------|-----------|-----------|------|
| factory-preflight | evals/skills/test_platform_preflight.py | 1.0 (100%) | Binary |
| cove-quorum | evals/skills/test_quorum_calculator.py | 0.90 (90%) | Binary + LLM-as-judge |

**Threshold semantics:**
- `1.0` — used for infrastructure checks where partial pass is not acceptable.
  Any failing check means the environment is broken.
- `0.90` — used for domain logic with a mixed eval strategy (85% binary/regex,
  15% LLM-as-judge). Some tolerance for LLM judgment variation is built in.

### App-specific compliance overrides

**Canary (`compliance: "pci-awareness"`):**
App-specific skills add PCI awareness checks at each stage. Overrides exist
for all eight post-preflight stages. Canary also uses the `critical-file-guardian`
skill for protected file modifications (separate from the factory pipeline),
and the GitNexus MCP for impact analysis before editing any symbol.

**Cove (`compliance: "davis-stirling"`):**
App-specific skills add Davis-Stirling compliance checks at each stage.
Overrides exist for all eight post-preflight stages. The ballot separation rule
(no `member_id` on `ballots` table) and PostgreSQL Row-Level Security on
`ballot_envelopes` are enforced at blueprint and verify stages. The quorum
calculator domain skill (with its own eval suite) operates outside the main
factory pipeline as a domain service.

### MCP requirements by stage

| Stage | Required MCPs | Optional MCPs |
|-------|---------------|---------------|
| preflight | linear | memory-bus |
| research | — | memory-bus, gitnexus, obsidian, firecrawl |
| blueprint | linear | memory-bus |
| tdd | — | — |
| assembly | — | — |
| verify | — | — |
| qa | — | — |
| ship | linear | — |
| close | linear | memory-bus |

Required MCPs that are unreachable cause a STOP at that stage. Optional MCPs
that are unavailable are silently skipped and noted in the report.

### Environment configuration

The factory pipeline reads its configuration from two sources at preflight:

- `~/GrowDirect/factory-manifest.json` — pipeline structure and stage definitions
- `~/GrowDirect/CLAUDE.md` (and app `CLAUDE.md`) — platform standards and
  app-specific context

No environment variables are required for the pipeline itself. App-specific
environment variables (DATABASE_URL, VALKEY_URL, SECRET_KEY, etc.) are checked
by the preflight skill through Docker container health checks, not by reading
`.env` directly.

---

## 7. Security & Compliance

This section is not applicable.

The factory pipeline is an agent orchestration layer — it is not user-facing
and has no authentication surface. It does not handle user data, process
payments, or make network requests to external systems (beyond MCP tool calls
to Linear and the optional sources in research).

Security and compliance considerations are enforced within individual app
pipelines through their override skills:
- Canary applies PCI awareness checks at blueprint and QA stages
- Cove enforces Davis-Stirling secret ballot separation at blueprint, verify,
  and QA stages

For platform-level security policies (secrets management, Docker stack
configuration, protected files), see `CLAUDE.md § Hard Rules` and
`CLAUDE.md § Protected Files`.

---

## 8. Error Handling

### Preflight failures

| Severity | Condition | Action |
|----------|-----------|--------|
| RED | Docker not running | STOP. Provide `docker compose up -d` command. |
| RED | PostgreSQL not accepting connections | STOP. Report container status. |
| RED | Valkey not responding | STOP. Report container status. |
| RED | Ollama unreachable | STOP. Report container status. |
| RED | Not a git repository | STOP. |
| RED | GRO issue not found or already Done/Cancelled | STOP. Ask ALX for clarification. |
| YELLOW | Containers unhealthy or restarting | Continue with warning. |
| YELLOW | Git working tree dirty | Continue with warning. |
| YELLOW | Ollama running but embedding model not loaded | Pull model, then continue. |
| YELLOW | Memory bus not running | Continue. Research and close skip memory operations. |

### Mid-pipeline failures

**Test failure during assembly:** Stop the task loop immediately. Do not
move to the next task. Diagnose the failure from the error output. Fix the
implementation. Re-run the failing test. Do not skip.

**Smoke test regression:** A previously passing smoke test fails after a
task is completed. This means a regression was introduced. Stop. Fix the
regression. Confirm smoke is green before proceeding to the next task.

**Out-of-scope bug found:** Do not fix it. Create a new Linear issue. Note the
GRO number in the session. Continue with the current task.

**Migration fails at verify:** Do not proceed to QA. Investigate the migration.
If `autogenerate` was used, review the generated migration manually — Alembic
autogenerate misses some cases (e.g., server defaults, RLS policies, custom
types). Fix the migration and re-run.

**Linear MCP unreachable:** Log a warning. Continue the pipeline. Record the
skipped Linear action for manual follow-up in the session summary.

**Scope creep during assembly:** If a task requires changes outside the
blueprint's planned file set, stop. Investigate whether the blueprint was
under-specified. If the work is genuinely new scope, create a new Linear issue.

### Factory-level failure recovery

If the pipeline is interrupted mid-stage (e.g., session ends), the next session
restarts from preflight. The preflight report identifies where the pipeline
left off (via git log and Linear issue status). The builder picks up at the
stage where work was interrupted, not from the beginning.

---

## 9. Testing

### Eval strategy

Skill evals test the *output* of skills — not the skill files themselves as
executable code. They validate that infrastructure is correctly configured,
domain calculations produce correct results, and structured outputs meet
pass/fail criteria derived from source material.

Three eval types are used, per the strategy defined in
`docs/sdds/platform/skill-architecture.md`:

| Type | Method | Target skills |
|------|--------|---------------|
| Binary | Pass/fail assertions (subprocess exit codes, file existence, regex) | Infrastructure checks, build gates, data validation |
| Pattern | Regex matching on structured output | Blueprint format, report format, taxonomy output |
| LLM-as-judge | Claude evaluates against domain criteria | Compliance reasoning, narrative quality |

### Eval files

**`evals/skills/test_platform_preflight.py`** — threshold 1.0 (100%)

Tests the complete preflight infrastructure check suite. All binary assertions.

| Test class | What it checks | Source |
|------------|----------------|--------|
| TestDockerStack | Docker daemon available, all 4 containers running | CLAUDE.md § Shared Infrastructure |
| TestPostgreSQL | `pg_isready` passes, all 6 databases accessible | CLAUDE.md § Database Layout |
| TestValkey | Container responds to PING | CLAUDE.md § Shared Infrastructure |
| TestOllama | Reachable on port 11434, `qwen3-embedding:8b` loaded | CLAUDE.md § Embeddings |
| TestGitStatus | Is a git repo, HEAD not detached | factory-preflight.md |
| TestManifest | `factory-manifest.json` exists, valid JSON, correct pipeline order, preflight checks declared | factory-manifest.json |
| TestSkillFiles | All 9 factory skill files exist and have valid YAML frontmatter with `name:` field | factory-manifest.json |
| TestContextFiles | `CLAUDE.md` exists for platform, Canary, and Cove | factory-preflight.md |

**`evals/skills/test_quorum_calculator.py`** — threshold 0.90 (90%)

Tests the Cove quorum calculator domain skill. Mix of binary and pattern
assertions. ~85% binary/regex, ~15% LLM-as-judge (tested separately).

| Test class | What it checks | Source |
|------------|----------------|--------|
| TestConfigIntegrity | 81 lots, 7 proposal types, 5 quorum contexts, required fields | wpbca-bylaws-config.json |
| TestQuorumThresholds | Exact threshold values (1/3 general, 1/2 assessment, 0 secret ballot, 20% reconvened, 50% board) | Bylaws §5.9, §6.6, AB 2460 |
| TestQuorumNumbers | Correct member counts for 81 lots (ceil math) | Bylaws + config |
| TestVoteThresholds | Approval thresholds per proposal type (majority, plurality, supermajority) | Bylaws §5.14, §13.2, §4270 |
| TestSecretBallotFlags | Secret ballot required/not required per type | Bylaws §5.9 |
| TestElectronicVoting | AB 2159 exclusions (special assessments not electronic) | AB 2159 (2024) |
| TestNoticePeriods | Notice days per type (4 to 35 days) | Bylaws §6.4.2, §8.10, §8.20.1 |
| TestBylawCitations | Quorum results cite correct bylaw sections | Bylaws section numbers |
| TestEdgeCases | 0 lots, 1 lot, quorum_met True/False, votes_needed_to_pass | Boundary conditions |
| TestAcclamation | AB 502 uncontested seat logic | AB 502 (2022) |

**`evals/skills/conftest.py`** — shared fixtures

Provides `docker_running` (skips test if Docker unavailable) and
`growdirect_containers` (returns list of running growdirect_* containers).

**`evals/skills/test_memory_layer_tagging.py`** — not yet referenced in manifest

Memory bus layer tagging eval. See Section 11 (Known Issues).

### Running evals

```bash
# Platform preflight eval
cd ~/GrowDirect && python3 -m pytest evals/skills/test_platform_preflight.py -v

# Quorum calculator eval (requires Cove Docker stack)
cd ~/GrowDirect && python3 -m pytest evals/skills/test_quorum_calculator.py -v

# All evals
cd ~/GrowDirect && python3 -m pytest evals/skills/ -v
```

### App test suites

App-level tests are separate from skill evals. They test application code,
not pipeline orchestration.

| App | Test database | Runner | Layers |
|-----|--------------|--------|--------|
| Canary | `canary_test` | `python3 -m pytest tests/` in Canary container | unit, integration, smoke |
| Cove | `cove_test` | `python3 -m pytest tests/` in Cove container | unit, integration, smoke |

---

## 10. Dependencies

### Required at all times

| Dependency | Version | Role |
|-----------|---------|------|
| Docker | Current | Runs shared infrastructure containers |
| growdirect_postgres | PostgreSQL 17 | All app databases |
| growdirect_valkey | Valkey 8 | Session store, cache |
| growdirect_ollama | Current | Embedding model serving |
| Linear MCP | — | GRO issue read/write at stage boundaries |

### Required at specific stages

| Dependency | Stages | If absent |
|-----------|--------|-----------|
| Linear MCP (`linear`) | preflight, blueprint, ship, close | STOP at preflight; skip at later stages with warning |
| Memory Bus MCP (`memory-bus`) | preflight (optional), research (optional), close (optional) | Skip gracefully, note in report |
| GitNexus MCP (`gitnexus`) | research (optional) | Skip gracefully |
| Obsidian MCP (`obsidian`) | research (optional) | Skip gracefully |
| Firecrawl MCP (`firecrawl`) | research (optional) | Skip gracefully |

### App-level dependencies (not factory pipeline)

The factory pipeline does not install or manage application dependencies. These
are managed per-app through `requirements.txt` (Python) and `package.json`
(npm for CSS/JS build). New pip packages require a Docker image rebuild — the
pipeline does not handle this automatically. The preflight skill will detect a
`ModuleNotFoundError` in container logs as a sign that a rebuild is needed.

### Skill file locations

All factory skills are in `~/GrowDirect/.claude/skills/`. App-specific override
skills follow the same pattern:

| App | Skill pattern | Location |
|-----|--------------|----------|
| Platform | `factory-{stage}.md` | `~/GrowDirect/.claude/skills/` |
| Canary | `canary-{stage}.md` | `~/GrowDirect/.claude/skills/` |
| Cove | `cove-{stage}.md` | `~/GrowDirect/.claude/skills/` |

---

## 11. Known Issues & Reconciliation

### Manifest gaps: skill and eval fields only wired for preflight

**Observed:** `factory-manifest.json` declares `skill` and `eval` fields only
for the `preflight` stage. The remaining eight stages have skill files
implemented in `.claude/skills/` but are not wired in the manifest with their
skill file references and eval thresholds.

**Impact:** The manifest cannot be used programmatically to discover which skill
implements each stage (beyond preflight), and there is no manifest-level eval
coverage for stages 2–9.

**Status:** Accepted gap. The skill files exist and are used by builders. The
manifest wiring is planned work (see skill-architecture.md § Manifest
Integration).

### test_memory_layer_tagging.py not referenced in manifest

**Observed:** `evals/skills/test_memory_layer_tagging.py` exists and tests
memory bus layer tagging behavior, but no stage in `factory-manifest.json`
references it as an eval suite.

**Impact:** The eval exists but has no manifest gate. It can be run manually
but is not enforced at any pipeline stage.

**Status:** Accepted gap. Memory layer tagging is validated as a post-mortem
skill behavior; it may be wired into a future `factory-postmortem` manifest
entry.

### Research stage has no skill field or eval

**Observed:** The `research` stage in the manifest has no `skill` field (unlike
preflight, which references `factory-preflight`). `factory-research.md` exists
and implements the stage, but the manifest does not register it.

**Impact:** Consistent with the broader manifest gap above. The skill works;
it is just not registered.

### Canary workflow still references pre-factory skill names

**Observed:** `Canary/CLAUDE.md` references a legacy skill set (`canary-blueprint`,
`canary-assembly`, `canary-verify`, etc.) using a `Blueprint → Parts → Assembly →
QC → Packaging → Ship` framing that predates the nine-stage factory nomenclature.
The Canary skill set is more extensive than the Cove set (14 existing skills vs.
8) and includes Canary-specific capabilities (canary-deploy, canary-debug,
canary-review, canary-scenario, canary-uat) that have no factory-pipeline
equivalents.

**Impact:** Canary operates on a hybrid workflow — the factory pipeline applies
at the platform level, but Canary's CLAUDE.md references its own richer skill
set. Both are valid; they are not in conflict. The Canary skills delegate to
factory base skills per the factory-newapp convention.

**Status:** By design. Canary was built before the factory pipeline was
formalized. Canary's skill set is a superset of the factory pipeline, not a
replacement for it.

### factory-newapp is outside the nine-stage pipeline

**Observed:** `factory-manifest.json` does not include `factory-newapp` in the
pipeline array or stages object. `factory-newapp.md` exists as a skill but is
invoked out-of-band.

**Impact:** None. New app scaffolding is a one-time operation per product, not
a repeating feature-delivery stage. It intentionally operates outside the
feature pipeline.

### Companion reference

The skill taxonomy, eval strategy, layer tagging rules, and skill inventory
(38 existing, 19 planned across all layers) are documented in the companion
reference:

**`docs/sdds/platform/skill-architecture.md`**

That document covers: the four-layer skill architecture (Corp / Cove / Canary /
Shared), the 7-step skill creation pipeline per George Nurijanian's method,
eval type ratios by skill category, memory tagging rules, and the full skill
inventory with planned additions. It is a companion to this document, not a
subset — do not look here for skill taxonomy or eval strategy detail.
