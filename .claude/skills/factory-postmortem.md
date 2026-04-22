---
name: factory-postmortem
roles-primary:[ProgramManager]
roles-assist:[Engineer, QA]
description: |
  Post-mortem capture after shipping sessions. Extracts lessons learned from
  the build cycle and stores them as structured memories tagged by layer.
  Invoked by factory-close for shipping sessions only.
---

# factory-postmortem — Post-Mortem Capture

> Invoked by factory-close after a shipping session completes.

**Announce at start:** "Writing post-mortem for this shipping session."

## When to use

- After a shipping session (factory-ship completed successfully)
- NOT for research-only, blueprint-only, or aborted sessions

## Process

### Step 1: Gather session data

Collect from the current session:
- GRO issue number(s) worked on
- Files created or modified (from git diff)
- Tests written and pass rate
- Decisions made during the session
- Problems encountered and how they were resolved
- Anything surprising or non-obvious

### Step 2: Write post-mortem file

Write to `~/GrowDirect/docs/post-mortems/YYYY-MM-DD-<feature-slug>.md`:

```markdown
# Post-Mortem: <feature name>

**Date:** YYYY-MM-DD
**GRO:** GRO-XXX
**App:** <canary / cove / platform>
**Session:** <session number if multi-session>

## What shipped
- [specific deliverables with file paths]

## What worked
- [specific things that went smoothly and why]

## What didn't
- [specific things that caused delays or rework and why]

## What to change
- [concrete suggestions for next time — not vague aspirations]

## Decisions made
- [key decisions with rationale — these become memory entries]

## Metrics
- Tests: X written, Y% pass rate
- Files: X created, Y modified
- Eval score: X% (if skill has eval suite)
```

### Step 3: Store lessons as memories

For each significant lesson, store to memory bus with correct layer tag:

| Memory type | When to use | Layer |
|-------------|-------------|-------|
| `decision` | Choices made that affect future work | App or corp |
| `finding` | Bugs found, gaps identified, surprising behavior | App |
| `architecture` | Structural changes to codebase | App or corp |
| `procedure` | New workflows or process changes | Corp |

**Layer tagging rules:**
- Platform standards changes → `corp`
- App-specific findings → `canary` or `cove`
- Cross-app patterns → `shared`
- Factory process changes → `corp`

### Step 4: Update Linear

Post a summary comment on the GRO issue with:
- Link to post-mortem file
- Key lessons (1-2 sentences each)
- Any follow-up issues created

## What NOT to store

- Ephemeral task details (already in git history)
- Code patterns (derivable from reading the code)
- Things already in CLAUDE.md
- Debugging steps (the fix is in the code)

## Key rule

Agent writes the post-mortem. Jeffe reviews and decides what gets promoted
to platform standards. The agent does NOT update `~/GrowDirect/CLAUDE.md` —
human gate prevents bloat.
