---
title: Brain Health Check — 2026-04-21
type: raw-intake
created: 2026-04-21
source: scheduled-task (brain-health-check)
status: clean
---

# Brain Health Check — 2026-04-21

Weekly automated scan of the GrowDirect Brain (Obsidian vault).

## Summary

| Check | Result |
|---|---|
| Registry | ✅ 142 entries (135 wiki + 7 project MOCs), 2,297 topics; rebuilt clean |
| Lint | ✅ 135/135 wiki files pass required frontmatter |
| Stale (>30d past `needs-review`) | ✅ 0 |
| Orphans | ✅ 0 |
| Inbox backlog (>7d) | ⚠️ 1 very-old file (`HOA+DOCS.pdf`, 2018 mtime) + 35 fresh Secure/Kroger extracts from today |
| Intake bypasses | ⚠️ 3 loose docs in repo root (Tax, LP-Integration-Spec, 2025 Tax Prep) + image/html strays |
| Registry gap | ✅ 142:142 perfect match |

Net: vault is structurally healthy. One long-stalled PDF in the inbox and a cluster of today's Secure/Kroger markdown extracts that still need routing. Loose files in repo root should be triaged.

## Stale Articles

None. No wiki article is >30 days past its `needs-review` date. One frontmatter anomaly flagged below.

### Frontmatter anomaly

- `Brain/wiki/card-yogasix-rolling-hills.md` — `needs-review: false` (not a valid date).
  - **Action recommended:** set to a real date (e.g., `2026-05-21`) or remove the field. **Flagged, not auto-fixed** — the `false` value may be an intentional marker I'm not aware of.

## Orphans

None. All 135 wiki articles have at least one inbound link from a project MOC or another wiki article. The previous sandbox file `__lint_test.md` is no longer present.

## Inbox Backlog

`Brain/raw/inbox/` currently contains 36 markdown files plus 1 PDF.

### Old (>7 days)

- **`HOA+DOCS.pdf`** — mtime 2018-06-27 (2,854 days old by mtime). The 2018 date is likely the preserved original file's timestamp, not actual inbox age, but it has clearly not been processed. **Flagged** — judgment call whether this should be split/extracted into the Brain pipeline, moved to `Brain/raw/processed/cove/` as a raw reference, or archived elsewhere.

### Fresh (≤7 days) — dropped today (2026-04-21)

35 markdown files, all extracted from legacy Kroger/Secure source documents. Not stalled per the 7-day rule, but they form a coherent batch that should land in `Brain/raw/processed/secure/` once the Secure wiki articles (`secure-*.md`) that already consume them are confirmed complete.

Batch contents:

- Secure platform overviews (`secure-5-solution-architecture-*`, `s5-on-premise-*`, `secure-omnichannel-overview-*`, `secure-lite-*`, `secure-store-*`, `sso-overview-*`)
- Kroger engagement artifacts (`kroger-pos-*`, `kroger-secure-rfp-*`, `kroger-dsd-*`, `kroger-solution-architecture-*`, `kroger-retek-project-sam-*`, `kroger-sysrepublic-*`, `kroger-opportunity-fact-sheet-*`)
- Process/planning docs (`dev-ops-*`, `factory-overview-v2-*`, `gantt-charts-*`, `new-delivery-process-*`, `workarounds-*`, `deliverable-responsibilities-*`, `data-gathering-agenda-*`, `rfi-8-15-*`, `5-1-requirements-*`, `appriss-retail-data-specification-*`, `max-replacement-appriss-follow-up-*`)

**Action recommended:** once the current Secure wiki session wraps, move this batch to `Brain/raw/processed/secure/<subtopic>/`. **Not moved during this run** — destination folders don't yet exist and placement is a canonicality call.

## Intake Bypasses

### Repo-root loose files (clear flags)

These violate the "No loose files in repo root or Brain inbox" memory rule. Each should be triaged to Brain, project docs, or deleted:

- `2025_Tax_Strategy_Brief.docx` (Apr 12)
- `2025_Tax_Prep_Workbook.xlsx`
- `AngeliqueLyle-LP-Integration-Spec.docx` (Apr 8) — likely belongs under `Angel/` or `Brain/raw/`
- `10584-max.jpeg`, `13328-max.jpeg`, `15658-max.jpeg` — unlabeled image strays
- `Torrance _ San Pedro - Sheet A08 of Book 9, County Surveyor Coordinates 15_169. - Maps - Huntington Digital Library.html` — probably a research clip, belongs under `Brain/raw/clips/` or `Brain/raw/research/`
- `formspree.rtf` — looks like a stray credential/config note

### App-local source docs (not flagged — judgment calls)

Not treated as bypasses because they live inside legitimate project docs trees per CLAUDE.md file layout:

- `Canary/docs/strategic/Canary_Platform_Overview_v1.0*.docx` — source docs for `canary-platform-overview.md` wiki
- `Cove/docs/cove-architecture-review.docx` + `Cove/docs/archive/` — Cove research pipeline
- `Angel/knowledge/heritage/1926-pv-estates-sales-brochure.pdf` — source for wiki
- `Angel/Compass Content - Angelique Lyle/**` — Compass-distributed marketing PDFs (93 files); not Brain-pipeline candidates
- `Seacove/**` — Seacove blueprint set, tracked by the SketchUp pipeline not Brain

## Registry Gaps

None.

- Wiki: 135 live files ↔ 135 registry entries
- Project MOCs: 7 live files ↔ 7 registry entries
- No dangling entries, no missing entries

## Cleanup Needed

- **Repo-root loose docs:** 7 files above — needs owner to pick targets (Brain/raw/inbox, project docs, or delete).
- **Inbox PDF:** `HOA+DOCS.pdf` needs a destination decision.
- **Today's Secure/Kroger batch:** move to `Brain/raw/processed/secure/…` once the Secure content session is complete.
- **Frontmatter fix:** set a real `needs-review` date on `card-yogasix-rolling-hills.md` or explicitly define semantics for `false`.

No actions were taken on these items during this run — all are judgment calls that require session context.

## Actions Taken This Run

- Rebuilt `Brain/REGISTRY.json` (clean, 142 entries, 2,297 topics).
- Confirmed lint clean (135/135 wiki files).
- No frontmatter auto-fix was needed (lint reported clean before the `--fix` pass would have run).
- Stale, orphan, and registry-gap checks ran clean — no edits required.
