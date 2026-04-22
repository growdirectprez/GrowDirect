---
name: canary-close
roles-primary:[ALX]
roles-assist:[ProgramManager]
stage: close
description: |
  Session teardown for Canary development. Updates Linear issues, stores findings
  to ALX pgvector memory, writes timelog, and confirms with Jeffe. Use when:
  'session close', 'wrap up', 'end session', 'close out', or any variation of
  ending a working session.
allowed-tools:
  - Read
  - Bash
  - Edit
  - Write
---

# Canary Close — Session Teardown

No session ends without completing all steps below. Do not skip. Do not batch.

## Step 1: Update Linear Issues

For every GRO issue touched this session:

- Update status (In Progress -> Done, or add comment with findings)
- Add comments for any blockers, decisions, or scope changes discovered
- If new issues were found: create them in Linear under project **Canary**

## Step 2: Store Session Findings to ALX Memory

Store important decisions, findings, and architectural changes to pgvector memory.
Use the appropriate `memory_type`:

| Type | When to Use |
|---|---|
| `decision` | Choices made (e.g., "chose approach B for CLAUDE.md streamline") |
| `finding` | Bugs found, gaps identified, unexpected behavior |
| `architecture` | Structural changes to the codebase |
| `procedure` | New workflows or process changes |

```bash
curl -s -X POST http://localhost:5001/alx/tools/memory_store \
  -H "Content-Type: application/json" \
  -d '{
    "content": "YOUR_FINDING_HERE",
    "memory_type": "decision",
    "metadata": {
      "session_date": "YYYY-MM-DD",
      "gro_issues": ["GRO-XXX"]
    }
  }' | python3 -m json.tool
```

Tag every memory with the session date and relevant GRO issue numbers.

**What to store:**
- Decisions that would be useful in future sessions
- Bugs or gaps that weren't fixed (logged as new issues)
- Architecture changes that affect how future work should be done
- Patterns or gotchas discovered during the session

**What NOT to store:**
- Ephemeral task details (that's what the commit history is for)
- Anything already captured in code comments or commit messages

## Step 3: Write Timelog

Invoke `project-timelog`. Do not duplicate its logic here.

## Step 4: Confirm with Jeffe

Present a summary to Jeffe before closing:

- Linear issues updated (list with new statuses)
- Memories stored (one-line summary each)
- Timelog written (confirm file path)
- Any open questions or blockers for next session

**Never close without Jeffe's confirmation.**

---

*Canary Close v1.0 — Session Teardown*
*Replaces: alx-session-close*
