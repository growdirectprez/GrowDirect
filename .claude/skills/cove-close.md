---
name: cove-close
description: |
  Session close for Cove development. Run at the end of every session before
  closing. Ensures all work is committed, tests pass, and main is up to date.
  Use when: ending a session, 'close', 'done', 'wrap up', 'session close'.
allowed-tools:
  - Read
  - Bash
  - Edit
  - Write
---

# Cove Close — Session Teardown

> Delegates to: `factory-close` for standard session close workflow.

Run the factory-close skill, then apply the Cove-specific additions below.

## Cove-Specific Additions

### Linear Update

If a GRO issue was worked on:
- Update the issue status in Linear (In Progress -> In Review, or add comment)
- Note what was done and what remains
- Any Davis-Stirling compliance decisions -> document in the issue

### Session Sign-Off

The session close summary should be attributed to "Cove builder". Format:

```
## Session Close — [date]

### What was done
- [bullet list of commits/work]

### Commits
- `abc1234` — description

### Open items
- [anything unfinished, with GRO reference if applicable]

### Tests
- X passed, Y failed

### State
- Branch: main
- Clean: yes/no
```

If all factory gates pass: "Session clean. Everything on main."
If any fail: fix it or flag it — don't close dirty.

---

*Cove Close v1.0 — Session Teardown*
*Delegates to: factory-close*
