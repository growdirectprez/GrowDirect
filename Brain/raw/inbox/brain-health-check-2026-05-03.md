---
type: health-check
date: 2026-05-03
tool: scheduled-task/brain-health-check
status: re-verified
runs:
  - 2026-05-03T03:48Z (initial scan)
  - 2026-05-03T04:11Z (post-remediation re-run)
---

# Brain Health Check — 2026-05-03 (post-remediation re-run)

Vault state after the remediation pass. Structural items closed; review-backlog and synthesis items remain on humans/sessions.

## Re-run delta vs. initial scan

| Metric | Initial | After remediation | Delta |
|---|---|---|---|
| Articles indexed | 376 | **379** | +3 (new health-check report, handoff doc, raas design review) |
| Topics | 4,528 | **4,585** | +57 |
| Stale (`last-compiled` >30d) | 0 | **0** | clean |
| `needs-review` past due | 59 | **59** | unchanged — needs human review pass |
| Orphan files | 15 | **0** | ✓ all reconnected, including the new raas-namespace card just created |
| Loose `.md` at repo root (excl CLAUDE/README/DEPLOY/SECURITY/AGENTS) | 1 | **0** | ✓ handoff doc routed to inbox |
| Loose `.md` at `docs/` top-level | 8 | **0** | ✓ all moved into proper subdirs |
| `Brain/raw/inbox/` `.md` count | 389 | 391 | +2 (this report, the routed handoff) |

## Current state

### ✓ Closed in this remediation pass

- 15 → 0 orphan wiki files. The 16th orphan that appeared mid-pass (`raas-namespace-design-review-2026-05-05.md`, created today) was caught and linked from the GrowDirect Patent Visuals section before this re-run.
- 8 → 0 loose `docs/` top-level files. New subdir `docs/playbooks/` created. 33 cross-references rewritten across 11 files.
- 1 → 0 loose handoff doc at repo root. Routed to `Brain/raw/inbox/2026-05-03-substrate-port-and-officer-architecture-handoff.md`.
- Registry rebuilt and re-verified: 379 articles, 4,585 topics.

### ⏳ Still open — require human action

| Item | Why still open | Action |
|---|---|---|
| Remove `CATz/` directory (49 wiki files + CLAUDE.md) | Permanent deletion is outside Cowork's authorization scope | `git rm -r CATz/ && git commit -m "remove: persistent CATz local clone (clone-on-demand per CLAUDE.md)"` — verified 52/59 files duplicate Brain by basename; the 6 "unique" files are pre-rename module letters with post-rename equivalents in Brain (M/O/L/C/S/E from C/J/L/R/S/W) |
| Triage 59 `needs-review`-past-due cards | Requires content judgment, not mechanical scan | Schedule a `/state` session — start with the angel-* batch (32 cards, all 2026-04-27, single review pass) |
| Synthesize 391 inbox `.md` items + binary corpus | Requires sustained cognitive work | Schedule a Secure-pattern synthesis sprint |
| Audit `outputs/` session leftovers | Permanent deletion is outside Cowork's authorization scope | Review then `git rm` what shouldn't ship |

## Coverage check

Wiki article counts by project keyword (single-bucket assignment, longest-prefix wins):

| Project | Articles | Status |
|---|---|---|
| platform | 91 | healthy |
| canary | 58 | healthy |
| cove | 43 | healthy |
| angel | 36 | healthy |
| secure | 20 | healthy |
| ncr | 15 | healthy |
| seacove | (counts under cove) | n/a — categorization artifact |

The seacove/cove split is a categorization artifact in the bucketing logic, not real coverage drift — `seacove-project.md` exists in `Brain/wiki/` and is reachable from the Seacove MOC.

## Verdict

Brain is structurally clean. The synthesis backlog (review-due cards, inbox corpus) is real work that lives outside the auto-fixable space.
