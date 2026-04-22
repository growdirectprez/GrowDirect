---
title: Brain Health Check — 2026-04-19 (latest run)
type: raw-intake
created: 2026-04-19
source: scheduled-task (brain-health-check)
status: clean
---

# Brain Health Check — 2026-04-19

Weekly automated scan of the GrowDirect Brain (Obsidian vault). This file supersedes the earlier 2026-04-19 run; most of that report's action items have since been addressed (inbox routing migrated to `Brain/raw/processed/`, orphans linked, `last-compiled` fields backfilled).

## Summary

| Check | Result |
|---|---|
| Registry | ✅ 127 articles, 2,036 topics; rebuilt clean |
| Lint | ✅ 123/123 wiki files pass required frontmatter |
| Stale (>30d past `needs-review`) | ✅ 0 |
| Orphans | ✅ 0 (1 found → linked, see below) |
| Inbox backlog (>7d) | ✅ Empty |
| Intake bypasses | ✅ None in pipeline; legitimate project archives only |
| Registry gap | ✅ 127:127 perfect match |

Net: vault is healthy. One orphan linked during the run. No stalled intake. No cleanup needed.

## Stale Articles

None. No wiki article is >30 days past its `needs-review` date.

The lone article without a dated `needs-review` field is `card-yogasix-rolling-hills.md` (`needs-review: false`) — intentional for a location card with no review cadence.

## Orphans

One orphan detected against MOCs (`Brain/projects/*.md`), `Brain/Home.md`, and all wiki articles. Sandbox stub `__lint_test.md` excluded per instructions.

### Action taken

- **`seacove-wpbca-demo-plan`** → linked from [`Brain/projects/Seacove.md`](Brain/projects/Seacove.md) under the Wiki section, alongside the `seacove-arc-module` stub and project overview. This matches its scope (turning 25 Seacove's accumulated permit assets into a neighbor-consultant demo methodology).

No orphans remain.

## Inbox Backlog

`Brain/raw/inbox/` contains only `.gitkeep`, `.DS_Store`, and this file. No stalled items. Prior week's `brain-health-check-2026-04-14.md` was properly archived into `Brain/raw/processed/` (was flagged in earlier report; now resolved).

## Intake Bypasses

Nothing flagged. Spot-checks:

- **`Cove/docs/*.md` (top level)** — three operational docs (`bylaws-as-config.md`, `cove-tech-debt-audit.md`, `url-inventory.md`). All reference their Brain wiki parent (`cove-governance`) and are legitimate project operational docs. Not intake bypasses.
- **`Angel/knowledge/*.md`** — 13 authored domain references. Per `CLAUDE.md`, `Angel/` is the Angel knowledge repo; these are intentional, not bypassed intake.
- **`docs/growdirect-io-architecture.md`** — platform architecture blueprint; legitimate.
- **`Cove/docs/archive/**`** — per CLAUDE.md Rule 6, flat archive destination for Cove project research. Not a bypass.
- **Council notes & advisor memos** — properly migrated to `Brain/raw/processed/council/` and `Brain/raw/processed/advisor-memos/` since the earlier report. Clean.

## Registry Gaps

Perfect symmetry:

- Registry entries: 127
- Live wiki + project MOC files: 127
- Entries with no live file: 0
- Live files missing from registry: 0

## Cleanup Needed

None. No one-shot scripts, scratch files, or session artifacts were created during this run — all checks executed via inline `python3` heredocs and `content-engine/engine.py` subcommands.

One cosmetic change to the repo: the link addition in `Brain/projects/Seacove.md` (resolving the orphan). Ready to commit alongside other Brain content already in-flight.
