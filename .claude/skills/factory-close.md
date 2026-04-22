---
name: factory-close
roles-primary: [ALX]
roles-assist: [Eva, Jess]
stage: close
description: |
  Session teardown. Session summary, pending items flagged, new issues created for out-of-scope work, post-mortem for shipping sessions.
---

# factory-close — Session Close

## Session summary

State what was completed this session:
- Files created or modified (list them)
- Tests written and passing
- Features delivered (tie each to the GRO issue)
- Migrations added

## Pending items

What was NOT completed? Why? What's the next step to unblock it?

## New issues found

Any bugs or gaps discovered outside the current GRO scope? Create a Linear issue for each one. Do not fix inline — note the GRO number and move on.

## Post-mortem (shipping sessions only)

If this session ended with a ship, invoke `factory-postmortem` skill.
Post-mortems go to `docs/post-mortems/YYYY-MM-DD-{feature}.md`.

Agent writes the post-mortem. Jeffe decides what gets promoted to platform standards.
Agent does NOT update `~/GrowDirect/CLAUDE.md` — that file has a human gate.

## Document filing

Before closing, verify any documents created this session are filed correctly
per CLAUDE.md § Document Filing Rules:

- SDDs → `docs/sdds/{namespace}/{service}.md`
- Architecture decisions → `docs/decisions/YYYY-MM-DD-{title}.md`
- Post-mortems → `docs/post-mortems/YYYY-MM-DD-{feature}.md`
- Superseded docs → `docs/_archive/YYYY-MM-DD-{name}.md`

No homeless docs. If a file was created outside these paths, move it.

## Close output

"Session done. Completed: [list]. Pending: [list or none]. New issues: [GRO numbers or none]."
