---
name: project-timelog
description: |
  Write a session timelog. Runs at end of every working session. Just write what
  happened — no transcript parsing, no token analysis, no research. Append to
  today's timelog file.
allowed-tools:
  - Read
  - Edit
  - Write
---

# Project Timelog

## What This Does

Writes a quick session summary to `~/GrowDirect/IP/timelogs/YYYY/MM-Month/daily/YYYY-MM-DD.md`.

## Rules

1. **Don't read anything new.** You already know what happened this session. Write from memory.
2. **Append to today's file.** If the file exists, add a new session section. If not, create it.
3. **Keep it under 50 lines.** Summary, deliverable table, blockers. Done.
4. **Same-day only.** Never backdate.

## Format

```markdown
## Session [N] — [Short Title]

**Agent:** [agent name]
**Platform:** [platform]
**Duration:** ~Xh

### Deliverables

| # | Issue | What shipped | Status |
|---|---|---|---|
| 1 | GRO-XX | One-line description | Done / In Progress |

### Key Decisions
- Decision 1
- Decision 2

### Blockers
- What's stuck and why (or "None")
```

## File Location

`~/GrowDirect/IP/timelogs/YYYY/MM-Month/daily/YYYY-MM-DD.md`

Adjust year and month folder as calendar changes.

## What NOT To Do

- Don't parse JSONL transcripts for token counts
- Don't run Python scripts
- Don't calculate cost-per-deliverable
- Don't write sprint retrospectives
- Don't load files to "verify" what you did — you were there
- Don't make it longer than it needs to be
