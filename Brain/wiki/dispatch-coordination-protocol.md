---
date: 2026-04-24
type: protocol
status: active
owner: GrowDirect LLC
classification: confidential
tags: [dispatch, coordination, autonomous, mini, laptop, alxjr, canary-builder, multi-machine]
sources:
  - CLAUDE.md (Dispatch Protocol section)
  - Linear Dispatch project (b9211ef5-7420-4a16-91da-5654604059a5)
last-compiled: 2026-04-24
needs-review: 2026-05-24
---

# Dispatch Coordination Protocol

> **Purpose.** Make multi-machine autonomous Claude execution actually
> work — without machines stomping on each other, dispatches dropping
> silently, or work landing without verification. This protocol is the
> canonical reference every dispatch links to.

## The six principles

1. **Self-contained dispatches.** The agent on the receiving machine
   has zero session context — it sees only the Linear ticket. Every
   dispatch includes the why, the what, the file paths it should
   touch, the done condition. Treat each as a smart-colleague brief.

2. **Bounded scope.** A dispatch fits one autonomous session — call it
   2–4 hours of agent-time. Anything bigger needs splitting into
   multiple dispatches with `Blocked by` relations.

3. **Explicit `Blocked by` relations.** Dependencies are declared on
   the Linear issue, not implied in description text. The agent picks
   up the next available unblocked dispatch with its `Target/<machine>`
   label.

4. **Verification baked into Done — narration during work.** Every
   dispatch's Done comment must include: (a) what changed (commit SHA,
   file paths), (b) what was tested (unit test added or run), (c) what
   was observed (smoke test output, log excerpt). Without verification,
   autonomous work compounds error silently. Likewise, every transition
   from `Todo` to `In Progress` posts a *starting comment* (template
   below) so other agents and humans can see who's working what —
   silent in-flight work creates collision risk and corrupts the audit
   trail. A Done flip without a Done-comment is reverted to In Progress;
   an In Progress flip without a starting comment is reverted to Todo.

5. **Branch hygiene + ownership boundaries.** Mini and laptop never
   touch the same file in the same dispatch. Branch naming:
   `mini/gro-<n>-<slug>` and `laptop/gro-<n>-<slug>`. Commit messages
   reference the GRO ticket. Both push to feature branches; humans
   open PRs.

6. **Stop-and-escalate triggers.** If the agent hits an architectural
   decision not in scope, it does NOT decide on its own. Cancel the
   dispatch with `Cancelled` status + reason comment, optionally
   create a follow-up dispatch describing the decision needed. Next
   human-supervised session resolves it.

## Lifecycle

A dispatch moves through this state machine on Linear:

```
Backlog → Todo → In Progress → Done
                            ↘ Cancelled (with reason)
```

| State | Who sets it | When |
|---|---|---|
| `Backlog` | Author (often human or supervised agent) | Drafted; not yet ready for pickup |
| `Todo` | Author (or human after blocking dispatches finish) | Ready for the targeted machine to pick up |
| `In Progress` | Receiving agent | On pickup; post starting comment (template below) |
| `Done` | Receiving agent | On completion; comment with verification evidence |
| `Cancelled` | Receiving agent | On stop-and-escalate; comment with reason |

Status advances are deliberate. No silent transitions; every status
change is paired with a Linear comment that says why.

## Labels

Required on every dispatch:

| Label parent | Values | Required |
|---|---|---|
| `Target/` | `mini`, `laptop`, `any` | exactly one |
| `Agent/` | `ALXjr`, `Canary Builder`, `Cove Builder`, `ALX`, `Jeffe` | exactly one |

The `Target` label says which machine. The `Agent` label says which
persona on that machine executes. `Agent/Jeffe` means human-only —
the dispatch represents a decision or action only the founder can
take.

Optional: `Stage/<x>` for factory stage classification, type labels
(`Feature`, `Bug`, `Tech Debt`, `Research`, `Strategy & Research`),
compliance labels.

## Starting comment template

On every `Todo → In Progress` transition, the receiving agent posts:

```markdown
## Starting

**Machine / Agent:** mini / ALXjr (or laptop / Jeffe, etc.)
**Branch:** mini/gro-<n>-<slug>
**ETA:** <minutes / hours>
**Plan:** <one paragraph — what the agent intends to do, in scope>
**Concurrency check:** <any other Linear tickets touching the same
files / containers / migrations — flag collision risk if found>
```

A status flip to In Progress without a starting comment is incomplete
and should be rolled back to Todo until narrated. The starting comment
lets a parallel agent on the same machine — or the founder spot-checking
state — know who's working what without having to read git history or
inspect runtime infra.

## Done comment template

Every Done transition includes a comment in this shape:

```markdown
## Done — verification

**Branch:** mini/gro-<n>-<slug> (or laptop/gro-<n>-<slug>)
**Commit:** <SHA>
**Files touched:**
- <path 1>
- <path 2>
- <path 3>

**Tests:**
- <test command run> — <pass / fail / N tests added>
- <smoke output excerpt if applicable>

**Observations:**
- <what was checked manually>
- <anything notable that came up>

**Open follow-ups (if any):**
- <new dispatch GRO-N created for <X>>
- <flagged for human review: <Y>>
```

A Done comment without these sections is incomplete and the dispatch
should be reverted to In Progress until it's filled in.

## Cancelled comment template

Every Cancelled transition includes a comment in this shape:

```markdown
## Cancelled — reason

**Stop trigger:** <what blocked progress>
**Why this is escalation, not failure:** <one sentence>
**What was attempted:** <list>
**State left in:** <branch state, partial commits if any>
**Follow-up needed:**
- <decision required from <person>>
- <or: new dispatch GRO-N created>
```

## Coordination boundaries

For the current handoff (substrate spine code-wiring + NCR adapter):

**Mini owns:**
- `Canary/canary/services/ej_spine/`
- `Canary/canary/services/sales_audit/`
- `app.merchant_module_cutover_status` table + service
- Satoshi-precision migrations on existing ledger-facing tables
- `.claude/skills/canary-vsm.md` updates (cutover-awareness + diagnostic-mode)
- Per-module manifest deepening (entities + MCP tools per module)

**Laptop (dev station) owns:**
- `Canary/canary/services/parsers/ncr_*`
- `Canary/canary/services/oauth/ncr.py`
- NCR webhook blueprint + ingestion pipeline
- NCR-specific tests
- NCR sandbox connection + first end-to-end flow

If a dispatch needs to touch the other machine's territory, it gets
split into two dispatches — one per machine — with the cross-machine
dispatch becoming a `Blocked by` of the integration dispatch.

## Verification expectations

After every dispatch, the next human-supervised session can verify
state by:

1. Reading Linear: which dispatches completed, which got cancelled,
   what reasons
2. Reading the commit log on each branch (git log --since=<date>)
3. Running a build / test pass on the mini's branches
4. Spot-checking files that landed against the design specs
   (substrate articles, manifests, ADRs)

The `Done` comment is the audit trail. The Linear status is the index.

## Pacing

- Agents do not work continuously. The mini picks up new dispatches
  when triggered (cron or human trigger), executes one dispatch,
  reports Done, and stops until next trigger.
- The dev station is exploratory — it can pick up any unblocked
  `Target/laptop` dispatch when the founder is at the laptop and
  triggers it.
- Daily Linear digest: each machine writes a one-line comment on its
  open dispatch at end-of-day with status. Lets the founder scan
  progress in 30 seconds.

## Risk mitigations

- **Skill-path protections.** `.claude/skills/` may be write-protected
  in some session contexts. If the dispatch fails, cancel with that
  exact reason — don't paper over it.
- **Real Alembic migrations require a clean local DB test before
  commit.** No migration commits without a successful `alembic
  upgrade head` + `alembic downgrade -1` round-trip.
- **No new architectural decisions in autonomous dispatches.** Stop
  and escalate. Architectural decisions go through the Morrisons-frame
  ADR pattern with human review.
- **Drift between substrate design and code.** Periodic verification
  pass (every 5–10 dispatches) checks substrate articles against
  shipped code and surfaces drift. This can itself be a scheduled
  dispatch.

## Related

- [`CLAUDE.md` Dispatch Protocol section](file:///Users/gclyle/GrowDirect/CLAUDE.md) — original protocol definition
- [Linear Dispatch project](https://linear.app/growdirect/project/dispatch-0f172b44bfe6) — control plane
- [GRO-548 spine state at close](https://linear.app/growdirect/issue/GRO-548) — the design baseline this protocol services

## Sources

- Direct user direction, 2026-04-24 — "thoughts make suggestions on how best to run autonomously for a while"
- CLAUDE.md Dispatch Protocol section
- Linear Dispatch project description + label inventory
