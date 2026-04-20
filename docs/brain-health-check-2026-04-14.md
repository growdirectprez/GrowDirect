---
date: 2026-04-14
type: raw-intake
status: unprocessed
tags: [brain-health-check, automation]
source: scheduled-task/brain-health-check
---

# Brain Health Check — 2026-04-14

Automated weekly scan. See scheduled-tasks/brain-health-check.

## Registry Stats

- Articles indexed: **54**
- Topics indexed: **916**
- Registry path: `Brain/REGISTRY.json` (rebuilt this run)

## Stale Articles (`last-compiled` > 30 days)

- None. All 21 wiki articles with `last-compiled` frontmatter are dated 2026-04-10 or later (within 4 days of today).

## Needs-Review Past Due

- None found.

## Orphan Files (no incoming wikilinks or md-links from other Brain files)

- None. All files in `Brain/wiki/` and `Brain/projects/` are linked from at least one other Brain document.

## Intake Bypass Violations

Loose knowledge/strategy docs (last 7 days) created outside `Brain/` that look like they should have been routed through the intake pipeline:

- `Canary/docs/Canary-Blue-Ocean-Strategy-Analysis.md` — strategic analysis doc. References `[[Brain/wiki/canary-architecture]]` but lives outside Brain. **Fix:** ingest via `python3 content-engine/engine.py ingest Canary/docs/Canary-Blue-Ocean-Strategy-Analysis.md -p canary`, then either distill into `canary-sales-strategy.md` or delete the loose copy.
- `Angel/PRODUCT-VISION.md` — vision/strategy doc at Angel repo root. **Fix:** ingest with `-p angel`; decide whether its content belongs in `angel-architecture.md` or warrants a new `angel-product-vision.md` wiki article.
- `Angel/WEBHOOK_SCAFFOLD.md` — borderline; reads as dev-reference/code-adjacent. **Fix (optional):** if the scaffold is historical and no longer in use, delete. Otherwise leave in place — not every README-style file needs Brain routing.

Note: 598 markdown files were modified in the last 7 days. The vast majority are code/config-adjacent (SKILL.md, CLAUDE.md, READMEs, SDDs under `docs/sdds/`, atlas figures under `Canary/docs/atlas/`, field-research packets under `Cove/docs/parcels/field-research/`, ADRs, superpowers specs, etc.). Those are legitimate in-repo locations per the project conventions and are not flagged.

## Stalled Inbox Items (> 7 days in `Brain/raw/inbox/`)

- None. Inbox is empty (only `.gitkeep` and `.DS_Store`).

## Registry Gap Analysis

| Project | Wiki article count | Status |
|--------|:-:|---|
| canary | 4 + 1 MOC | OK (≥3) |
| cove   | 9 direct + MOC, plus many tangential matches | OK |
| angel  | 30+ (includes content-pool raw articles) | OK |
| seacove | 1 + 1 MOC | **Below threshold** — only one wiki article (`seacove-project.md`). |

## Recommended Actions (for next session)

1. Ingest `Canary/docs/Canary-Blue-Ocean-Strategy-Analysis.md` into Brain; decide: distill into `canary-sales-strategy.md` or promote to its own wiki article. Then remove the loose copy.
2. Ingest `Angel/PRODUCT-VISION.md` into Brain; merge into `angel-architecture.md` or split out `angel-product-vision.md`. Remove the loose copy if redundant.
3. Decide fate of `Angel/WEBHOOK_SCAFFOLD.md` — delete if obsolete given "Angel is a Cove module" decision; otherwise leave.
4. Consider whether Seacove warrants a second wiki article (e.g., construction-log or SketchUp-pipeline notes) to clear the <3 threshold, or document that Seacove is intentionally a thin knowledge footprint.
5. Process this health check report: either act on the items above and delete this file, or promote findings into tracked Linear issues.
