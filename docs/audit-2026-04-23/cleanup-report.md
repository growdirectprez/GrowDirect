---
classification: confidential
owner: GrowDirect LLC
---

# CTO Readiness Audit — Cleanup Report

Tracks remediation passes against findings in `platform.md`, `docs-brain.md`,
`security.md`, and `enterprise-scale-gap-analysis.md`.

## Confidentiality header sweep

Date: 2026-04-24
Phase: G4
Source finding: `docs-brain.md` L1–L48 ("100% of audited SHOW files lack
`classification: confidential` and `owner: GrowDirect LLC` frontmatter")
plus the parallel Python-header gap surfaced in `platform.md`.

### Python files — header added (33)

`# GrowDirect LLC — Confidential & Proprietary` block prepended to:

- `content-engine/` (4): `engine.py`, `tests/__init__.py`, `tests/test_extract.py`, `tests/test_method.py`
- `services/alx/` (1): `__init__.py`
- `services/growdirect-mcp/` (9): `growdirect_mcp/{__init__,auth,bridge,registry,tool}.py`, `tests/{test_auth,test_bridge,test_registry,test_tool}.py`
- `services/memory-bus/` (19): `memory_bus/{__init__,config,embeddings,server,store}.py`, `migrations/{__init__,env}.py`, `migrations/versions/{__init__,001_baseline,002_drop_seed_embeddings,003_hnsw_index,004_session_fk}.py`, `scripts/seed_clean.py`, `tests/{__init__,conftest,test_config,test_embeddings,test_smoke,test_store}.py`

Shebang preservation: `services/memory-bus/scripts/seed_clean.py` retained
its `#!/usr/bin/env python3` line; header inserted on lines 2–3.

### Markdown files — frontmatter updated (43)

`classification: confidential` and `owner: GrowDirect LLC` inserted into
the frontmatter block (or new block created if absent):

- `docs/sdds/platform/` (5): `aws-target-architecture`, `factory-pipeline`, `memory-bus`, `shared-infrastructure`, `skill-architecture`
- `docs/sdds/alx/` (2): `mcp-service-layer`, `test-lab`
- `docs/dispatches/` (5): `dispatch-{api-docs-gateway,demo-prep,primetime,site,vscode-library-narrative}-2026-04-{22,23}`
- `docs/superpowers/briefs/` (2): `2026-04-growdirect-method-initiative`, `2026-04-secure-to-canary-handoff`
- `docs/superpowers/specs/` (10): `2026-03-30-{mcp-consolidation,sdd-buildout}-design`, `2026-04-{11-growdirect-workflow-wiki,13-sdd-ops-upgrade,14-growdirect-io-portfolio-site,15-growdirect-site-refresh,20-growdirect-services-page,21-qa-agent-tier-0-unblock,22-qa-agent-page-context-primary,23-qa-agent-linear-filing-atlas-inline}-design`
- `docs/superpowers/dispatches/` (1): `2026-04-22-demo-reseed`
- `docs/superpowers/plans/` (8): `2026-03-30-mcp-consolidation`, `2026-04-{14-growdirect-io-portfolio-site,15-growdirect-site-refresh,21-qa-agent-tier-0-unblock,22-qa-agent-page-context-primary,23-qa-agent-linear-filing-atlas-inline,23-cto-readiness-audit,24-cto-readiness-remaining}`
- `Brain/method/` (7): `Activities`, `CommDocs`, `Models`, `Orchestration`, `Roles`, `Techniques`, `WorkProducts`
- `Brain/wiki/` (1): `growdirect-factory-process`
- `Brain/dispatches/` (2): `2026-04-24-batch-inbox-intake`, `2026-04-24-cto-readiness-phase-7-handoff`

Of the 43, 15 had pre-existing frontmatter (classification/owner inserted at top of block); 28 had no frontmatter (new block prepended).

### Skipped (already had classification)

- `docs/superpowers/specs/2026-04-23-cto-readiness-audit-design.md` — already `classification: confidential`
- `Brain/dispatches/2026-04-24-cto-readiness-ship-handoff.md` — already classified
- `Brain/projects/{Method,Factory,GrowDirect,RetailSpine}.md` — preserved at `classification: internal` per founder decision (set in prior batch)

### Surfaced as ambiguous (declined to classify unilaterally)

These files sit on the boundary between SHOW (platform-level) and HIDE
(app/project-specific). Audit's 48-file SHOW list did not enumerate them;
they live under `Brain/dispatches/` which the spec described only as
"non-HIDE-scope" without an explicit roster. Founder review needed:

- `Brain/dispatches/2026-04-23-abalonecove-regen.md` — Foundation/Cove project; likely HIDE.
- `Brain/dispatches/2026-04-24-consulting-skills.md` — references `docs/sdds/consulting/` (HIDE) and `methodology-ibm-*` wikis (HIDE per founder); likely HIDE.
- `Brain/dispatches/2026-04-24-cio-leave-behind-wedge.md` — references `plugins/consulting/` (HIDE-adjacent); likely HIDE but content is platform-flavored.
- `Brain/dispatches/2026-04-24-retail-corpus-intake-and-manifesto.md` — `third-branch` retail-manifesto / corpus intake; straddles RetailSpine (now `internal`) and Brain operations.
- `Brain/dispatches/dispatch-platform-brand-consolidation-2026-04.md` — platform brand consolidation, but tagged `katz, canary-retail, cbm-v2`; ambiguous.

Recommendation: classify each individually in a follow-up; the SHOW/HIDE
boundary in `Brain/dispatches/` should be made explicit in the spec.

### Out of scope (per prompt)

- `growdirect-platform.plugin/` — binary removed, not present in worktree.
- Repo-root `README.md`, `CLAUDE.md`, `SECURITY.md` — audit recommends these be `classification: public`; not in this sweep's scope.

### Counts summary

- Python headers added: 33
- Markdown frontmatter updated: 43 (15 in-place, 28 new block)
- Skipped (already classified): 6 (1 spec + 1 dispatch + 4 MOCs)
- Surfaced as ambiguous: 5
