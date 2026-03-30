---
name: canary-assembly
description: |
  Factory Process plan execution. Use when you have a written implementation plan
  to execute. Loads context, enforces Guardian on protected files, runs smoke tests
  between tasks, stops and retriages when blocked. Replaces superpowers:executing-plans.
allowed-tools:
  - Read
  - Bash
  - Edit
  - Write
  - Grep
  - Glob
  - TodoWrite
---

# Canary Assembly — Factory Process Plan Execution

> "Documents first, then build and tie it all together soup to nuts in a factory process."
> — Jeffe, Feb 17, 2026

## Overview

Load a plan written by `canary-blueprint`. Review it critically. Execute
every task using `canary-tdd`. Report when complete.

**Announce at start:** "I'm using canary-assembly to execute this plan."

## The Process

### Step 1: Load Context

Before touching any code:

```bash
# Load session context from knowledge graph
session_start(gro_issues=["GRO-XXX"])

# Recall domain knowledge relevant to this plan
memory_recall("topic from the plan")

# If the plan touches Goose, TSP, Fox, or any pipeline node — load architecture context
memory_recall("six-node pipeline staged immutability")
memory_recall("tLog to gLog")
```

Read the plan file. Read CLAUDE.md. If the plan touches a specific service domain,
load it:

```bash
domain_context("service_name")
```

Check the plan's **Pipeline Position** field. If it touches Nodes 1-3 (ingestion),
recall TSP architecture. If it touches Nodes 4-5 (detection/cases), recall Chirp
and Fox context. If it touches Node 6 (anchor), recall the staged immutability
pipeline and Bitcoin ordinal architecture.

### Step 2: Review Plan Critically

Read the full plan. Before executing, check:

```
-> Do I understand every task?
-> Are there ambiguous steps? (If yes: stop and clarify, don't guess.)
-> Does the file structure match the current codebase? (Files may have moved.)
-> Are any Guardian-protected files involved? (Flag them now.)
-> Does any task touch canary_sales? (Data integrity rules apply.)
```

If concerns exist, raise them before starting. Don't push through confusion —
it compounds.

### Step 3: Create TodoWrite

Map every plan task to a TodoWrite item. One task = one todo.

### Step 4: Execute Tasks

For each task:

1. Mark as `in_progress`
2. Use `canary-tdd` for implementation (RED -> GREEN -> REFACTOR)
3. Follow each step exactly — the plan has bite-sized steps for a reason
4. Run verifications as specified in the plan
5. **Run smoke tests after each task:**
   ```bash
   python3 -m pytest tests/smoke/ -v --timeout=30
   ```
6. If smoke tests break -> fix before moving on. Don't accumulate regressions.
7. Mark as `completed`
8. Commit with GRO reference

### Step 5: Guardian Enforcement

When a task modifies a protected file (`.env`, `wsgi.py`, `session_factory.py`,
`Dockerfile`, `docker-compose.*.yml`):

**STOP normal execution. Invoke `file-guardian` skill.**

The Guardian handles: pre-flight snapshot -> approval -> backup -> edit -> validate ->
manifest update. Do not bypass this. Direct edits to protected files are a
protocol violation.

### Step 6: Complete Development

After all tasks pass:

1. Run full test suite:
   ```bash
   python3 -m pytest tests/unit/ -v
   python3 -m pytest tests/smoke/ -v --timeout=30
   ```
2. Use `canary-verify` to confirm completion
3. Use `canary-ship` for merge/PR/deploy options

---

## When to Stop

**STOP executing immediately when:**
- A test fails that the plan says should pass
- You hit a missing dependency or unclear instruction
- Smoke tests break and you can't fix without changing the plan
- You've spent more than 15 minutes stuck on a single step
- Something feels architecturally wrong

**When stopped:**
- Don't guess. Don't push through.
- State what's blocked and why.
- If the plan needs revision, say so — don't patch around it.
- Return to the plan and re-evaluate before continuing.

> "If something goes sideways mid-execution: STOP. Re-triage. Re-plan.
> Do not push through confusion — it compounds."

---

## Subagent Execution

When running with subagent support (Claude Code):

- Dispatch a fresh subagent per task
- Each subagent gets: the task from the plan, CLAUDE.md, and relevant domain context
- Two-stage review: spec compliance first, code quality second
- Use `canary-review` between tasks for code review
- Parent agent tracks overall progress via TodoWrite

When running without subagents:

- Execute in current session with checkpoints
- After every 3 tasks, pause and review progress
- If context is getting long, store key decisions to memory and summarize

---

## Memory and Tracking

During execution:

- **Decisions:** When you make a judgment call not in the plan, note it. Store to
  pgvector memory at session close.
- **Discoveries:** When you find something unexpected (dead code, missing index,
  stale config), log it as a new Linear issue. Don't fix inline.
- **Blockers:** If blocked, update TRIAGE.md if the blocker affects other work.

---

*Canary Assembly v1.0 — Factory Process Plan Execution*
*Replaces: superpowers:executing-plans*
