# Factory Pipeline

> **Status:** Operational — code-reviewed 2026-04-13
> **Type:** Platform Service
> **Namespace:** platform
> **Code location:** `factory-manifest.json`, `.claude/skills/factory-*.md`
> **Companion:** [[docs/sdds/platform/skill-architecture|Skill Architecture]] — skill taxonomy, eval strategy, layer tagging
> **Author role:** [[Canary/docs/profiles/ops/Tom|Tom]] · **Operator role:** [[Canary/docs/profiles/ops/ALX|ALX]]

**Wiki:** [[Brain/wiki/growdirect-workflow|GrowDirect Workflow]] · [[Brain/wiki/document-management|Document Management]]
**Method:** [[Brain/projects/Method|Method MOC]] · [[Brain/projects/Factory|Factory MOC]]
**Related:** [[docs/sdds/platform/shared-infrastructure|Shared Infrastructure]] · [[docs/sdds/platform/memory-bus|Memory Bus]]

---

## Purpose

The Factory Pipeline is GrowDirect's nine-stage cognitive workflow that builder
agents follow to take a Linear issue from intake to ship. It enforces
consistency (same structure regardless of app or domain), traceability (every
stage produces an inspectable artifact), and scope control (no work without a
GRO issue, max 8 tasks per plan).

It is not a CI/CD system. It is a set of Markdown skill files consumed by
Claude Code agents at runtime. The pipeline is declared in
`factory-manifest.json` and implemented through skill files in
`.claude/skills/factory-*.md`. App-specific variants (`canary-*.md`,
`cove-*.md`) delegate to the factory base and add domain guardrails.

---

## Dependencies

| Dependency | Required | Role |
|-----------|:--------:|------|
| Docker + shared infra stack | Yes | PostgreSQL 17, Valkey 8, Ollama, pgadmin |
| Linear MCP | Yes (preflight) | GRO issue read/write at stage boundaries |
| Memory Bus MCP (port 8003) | Optional | Prior art recall, session memory writes |
| GitNexus MCP | Optional | Code impact analysis during research |
| Obsidian MCP | Optional | Domain knowledge during research |
| Firecrawl MCP | Optional | External API docs during research |
| `factory-manifest.json` | Yes | Pipeline definition, stage declarations |
| `.claude/skills/factory-*.md` | Yes | Stage implementation (12 skill files) |
| App `CLAUDE.md` files | Yes | Platform + domain standards |

**Startup order:** Shared infra (Docker Compose) must be running before
preflight. Linear MCP must be reachable. All other MCPs degrade gracefully.

**Blast radius:** If the factory pipeline is unavailable (manifest missing,
skill files deleted), no builder agent can execute structured work. Manual
ad-hoc development is still possible but loses all traceability guarantees.

---

## Data Flow

No PII passes through the factory pipeline. It is an agent orchestration
layer with no user-facing surface, no authentication, and no database tables.

**Artifacts flow forward through 9 stages:**

```
GRO Issue ID (from Linear)
  -> preflight_report      (infra status, app context, issue metadata)
  -> context_bundle         (prior art from memory bus / GitNexus / docs)
  -> docs/plans/{slug}.md   (blueprint — architecture decisions, task list)
  -> tests/                 (failing tests, one per behavior)
  -> implementation         (code changes, one commit per task)
  -> verify_report          (test counts, regressions, migration status)
  -> qa_report              (route tests, compliance, standards)
  -> git_push + linear_update (branch pushed, issue -> Done)
  -> session_summary        (close artifacts, memory writes)
```

Each stage consumes the prior stage's output. A stage that cannot proceed
because a prior artifact is missing or failed must stop and report.

---

## Operations

### How a session enters the pipeline

1. ALX (the dispatcher) provides a GRO issue identifier
2. Builder invokes `/factory-preflight` (or `/canary-preflight`, `/cove-preflight`)
3. Preflight runs infrastructure checks (Docker, PostgreSQL, Valkey, Ollama, git, Linear, memory bus)
4. Preflight identifies the target app from the GRO issue project field
5. App identification determines which `{app}-{stage}.md` override skills apply

**No GRO issue = no work.** The pipeline cannot start without a Linear issue.
An issue that is Done or Cancelled causes an immediate STOP.

### Stage transitions and gate conditions

| Stage | Gate to proceed | What blocks progress |
|-------|----------------|---------------------|
| Preflight | All checks GREEN or YELLOW | Any RED check (Docker down, DB unreachable, no GRO issue) |
| Research | Always proceeds (all sources optional) | Nothing — degrades gracefully |
| Blueprint | Explicit confirmation from ALX/user | Plan exceeds 8 tasks (must split), standards violations |
| TDD | All tests written and failing correctly | Test passes before implementation (defective test) |
| Assembly | All TDD tests green + smoke tests pass | Any test failure, any regression |
| Verify | Full suite green, migrations clean, diff matches plan | Any failure, any regression, unexpected file changes |
| QA | All findings fixed | Auth missing on routes, standards violations, CSS issues |
| Ship | Pre-ship checklist complete | Dirty working tree, bad commit messages, test failures |
| Close | Always completes | Nothing — runs even if ship was not reached |

**Gate conditions are binary.** Each stage passes completely or stops the
pipeline. There is no partial pass.

### Failure modes

| Failure | Impact | Recovery |
|---------|--------|----------|
| Docker not running | RED at preflight, full stop | `cd ~/GrowDirect/devops && docker compose up -d` |
| Linear MCP unreachable at preflight | RED, full stop | Check MCP configuration |
| Linear MCP unreachable at later stages | Warning, pipeline continues | Skipped actions noted for manual follow-up |
| Memory bus not running | YELLOW, skip memory operations | Research and close degrade gracefully |
| Test failure during assembly | Stop task loop, diagnose, fix | Do not skip; fix before next task |
| Smoke test regression | Stop, fix regression | Confirm smoke green before continuing |
| Out-of-scope bug found | Do not fix inline | Create new Linear issue, continue current task |
| Session interrupted mid-stage | Next session restarts from preflight | Preflight detects where pipeline left off via git log + Linear status |

### Monitoring

The pipeline has no runtime metrics or health endpoints. Monitoring is via:
- **Linear issue status:** ALX reads issue state to track pipeline progress
- **Git log:** Commit messages reference GRO issues, providing an audit trail
- **Session summaries:** Posted as Linear comments by factory-close

### Configuration

Two configuration sources, both read at preflight:
- `~/GrowDirect/factory-manifest.json` — pipeline structure, stage definitions
- `~/GrowDirect/CLAUDE.md` + app `CLAUDE.md` — platform standards, domain context

No environment variables required for the pipeline itself. App-specific env
vars are checked indirectly through Docker container health.

---

## API Contract

### Skill invocation

Skills are Markdown files read by Claude Code agents. Invocation is via slash
command or the Skill tool:

```
/factory-preflight     /factory-research     /factory-blueprint
/factory-tdd           /factory-assembly     /factory-verify
/factory-qa            /factory-ship         /factory-close
```

App-specific overrides: `/canary-preflight`, `/cove-blueprint`, etc.

Support skills (not invoked directly by builders):
- `factory-linear` — Linear MCP operations at stage boundaries
- `factory-postmortem` — post-mortem capture, invoked by factory-close
- `factory-newapp` — new app scaffolding, out-of-band

### Stage inputs/outputs

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

### Linear integration points (via factory-linear)

| Stage | Action | Tools |
|-------|--------|-------|
| preflight | Read and validate GRO issue | `get_issue` |
| blueprint | Move to "In Progress", attach plan | `list_issue_statuses`, `save_issue`, `create_document` |
| ship | Post ship report, move to "Done" | `save_comment`, `list_issue_statuses`, `save_issue` |
| close | Post session summary comment | `save_comment` |

### MCP requirements by stage

| Stage | Required | Optional |
|-------|----------|----------|
| preflight | linear | memory-bus |
| research | -- | memory-bus, gitnexus, obsidian, firecrawl |
| blueprint | linear | memory-bus |
| tdd | -- | -- |
| assembly | -- | -- |
| verify | -- | -- |
| qa | -- | -- |
| ship | linear | -- |
| close | linear | memory-bus |

Required MCPs that are unreachable cause a STOP. Optional MCPs that are
unavailable are silently skipped and noted in the report.

---

## How SDDs Function as Operational Contracts

After the SDD ops upgrade (2026-04-13), SDDs are the operational contract at
every pipeline stage, not just design references:

| Stage | How the SDD is used |
|-------|---------------------|
| Preflight | Check that service dependencies listed in SDD are running |
| Research | Read SDD for PII map, current findings, operational context |
| Blueprint | Design against SDD's API contract and PII classification |
| TDD | Write tests that validate SDD's production readiness checklist items |
| Assembly | Implement against SDD's operational requirements |
| Verify | Validate all checklist items in SDD pass |
| QA | Confirm no new P0 findings introduced |
| Ship | SDD's deployment section defines the deploy process |
| Close | Update SDD with any new findings from the session |

---

## Deployment

### Current state

The factory pipeline has no deployment artifact. It runs inside Claude Code
sessions as skill files read from disk. The skill files and manifest are
committed to git and available in any checkout of the GrowDirect repo.

### AWS target

Not applicable. The factory pipeline is a development-time orchestration
layer, not a deployed service. It runs wherever Claude Code runs — currently
the developer's local machine.

### Docker

Not applicable. No container, no image, no compose service.

---

## Code Review Findings

### P0 — Blocks production

None. The factory pipeline is a development-time tool, not a production
service. It has no user-facing surface, handles no PII, and requires no
secrets management or encryption.

### P1 — Before GA

**P1-1: Skill file `allowed-tools` authorization inconsistent**

Only 4 of 12 factory skill files declare `allowed-tools` in their YAML
frontmatter: `factory-preflight`, `factory-research`, `factory-linear`,
`factory-newapp`. The remaining 8 skills (`factory-blueprint`,
`factory-tdd`, `factory-assembly`, `factory-verify`, `factory-qa`,
`factory-ship`, `factory-close`, `factory-postmortem`) have no `allowed-tools`
declaration, meaning they run with unrestricted tool access.

- **Risk:** A skill that should only read files could invoke destructive
  tools (Write, Edit, Bash with `rm`). The authorization boundary is the
  frontmatter — without it, the boundary does not exist.
- **Fix:** Add `allowed-tools` to all 8 remaining skill files. Each skill's
  tool set should be the minimum needed for its stage (e.g., factory-tdd
  needs Bash + Read + Write + Edit; factory-ship needs Bash + Read + the
  Linear MCP tools via factory-linear delegation).
- **Linear:** Not yet filed.

**P1-2: Manifest only wires skill/eval for preflight stage**

`factory-manifest.json` declares `skill` and `eval` fields only for the
`preflight` stage. The remaining 8 stages have skill files implemented but
are not registered in the manifest with their skill file references or eval
thresholds.

- **Risk:** The manifest cannot be used programmatically to discover which
  skill implements each stage (beyond preflight). No manifest-level eval
  gate for stages 2-9.
- **Fix:** Add `skill` and `eval` fields to each stage entry in the manifest.
  Write eval suites for stages that lack them (at minimum: blueprint output
  format validation, ship checklist verification).
- **Linear:** Not yet filed.

**P1-3: Research skill declares WebSearch/WebFetch but manifest says
memory-bus/gitnexus/obsidian/firecrawl**

The `factory-research.md` `allowed-tools` lists `WebSearch` and `WebFetch`.
The manifest `optional_mcps` lists `memory-bus`, `gitnexus`, `obsidian`,
`firecrawl`. Neither set includes tools from the other. The skill body
references memory bus and GitNexus operations but has no `allowed-tools`
entries for those MCP tools.

- **Risk:** Research skill cannot invoke memory bus or GitNexus MCP tools
  because they are not in its `allowed-tools`. The `allowed-tools` acts as
  a whitelist — tools not listed are blocked.
- **Fix:** Update `factory-research.md` `allowed-tools` to include the
  memory bus and GitNexus MCP tool IDs, or remove `allowed-tools` if
  research should have unrestricted access like the other 8 skills.
- **Linear:** Not yet filed.

### P2 — Post-launch

**P2-1: No deployment stage for production shipping**

The `factory-ship` skill pushes a git branch and updates Linear. It does not
trigger a Docker image build, run database migrations in a staging
environment, or deploy to AWS. Production deployment is entirely manual.

- **Risk:** No risk for current dev-only usage. Becomes a gap when any app
  ships to production (Canary first).
- **Fix:** Add a `factory-deploy` skill (Canary already has `canary-deploy`
  with a 7-step pipeline) or formalize the deployment step in factory-ship.
- **Linear:** Not yet filed.

**P2-2: Post-mortem directory empty**

`docs/post-mortems/` contains only a README. The `factory-postmortem` skill
specifies writing post-mortems to this directory, but no post-mortems have
been captured. Either the skill has never been invoked via factory-close, or
post-mortems are being written elsewhere.

- **Risk:** No institutional memory from completed build cycles. Lessons
  learned are not being captured.
- **Fix:** Verify factory-close actually invokes factory-postmortem after
  shipping sessions. Run a retrospective post-mortem for past ships.
- **Linear:** Not yet filed.

**P2-3: Canary legacy skill naming**

`Canary/CLAUDE.md` references a pre-factory skill framing
(`Blueprint -> Parts -> Assembly -> QC -> Packaging -> Ship`) that predates
the nine-stage factory nomenclature. Canary's 14 skills include 6
domain-specific capabilities (deploy, debug, review, scenario, uat,
data-expansion) with no factory-pipeline equivalents.

- **Risk:** Naming confusion for new agents. Both systems work — the Canary
  skills delegate to factory base skills — but the vocabulary mismatch adds
  cognitive load.
- **Fix:** Align Canary CLAUDE.md terminology with factory pipeline names.
  Document the Canary-specific skills as domain extensions, not pipeline
  replacements.
- **Linear:** Not yet filed.

---

## Production Readiness Checklist

- [x] PII encrypted at rest — N/A (no PII handled)
- [x] Secrets in AWS Secrets Manager — N/A (no secrets; app secrets are app-level concern)
- [x] Health check endpoint responds — N/A (no deployed service)
- [ ] Audit logging for sensitive operations — N/A but Linear comments serve as audit trail
- [x] Data retention policy implemented — N/A (no stored data)
- [x] Rate limiting on public endpoints — N/A (no public endpoints)
- [x] Error responses don't leak internals — N/A (no user-facing responses)
- [ ] All skill files have `allowed-tools` authorization (P1-1)
- [ ] All stages wired in manifest with skill + eval fields (P1-2)
- [ ] Research skill `allowed-tools` matches manifest MCP declarations (P1-3)

---

## Companion Reference

The skill taxonomy, eval strategy, layer tagging rules, and full skill
inventory (38 existing, 19 planned across 4 layers) are documented in:

**[[docs/sdds/platform/skill-architecture|Skill Architecture]]**

That document covers the four-layer architecture (Corp / Cove / Canary /
Shared), the 7-step skill creation pipeline, eval type ratios, memory
tagging rules, and complete skill inventory. It is a companion to this
document — do not look here for skill taxonomy or eval strategy detail.
