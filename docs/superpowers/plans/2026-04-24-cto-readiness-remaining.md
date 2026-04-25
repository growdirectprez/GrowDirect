# CTO-Readiness — Remaining Work Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Take the GrowDirect platform repo from current state to ready-to-share parity with the already-shipped Canary repo, completing the CTO-readiness audit defined in the source spec.

**Architecture:** Eight phases (G0–G7) mirroring the original plan's phases for the **GrowDirect side only** — Canary is already done (tag `cto-review-ready-2026-04-24`). This plan picks up from current `main`, resolves housekeeping-branch consolidation, runs the audit on GrowDirect SHOW scope, executes cleanup, and produces a tagged ready-to-share state. Worktree-isolated cleanup, founder-gated phase boundaries, conservative-cleanup philosophy from the spec.

**Tech Stack:** Python 3.12, `pip-audit`, `bandit`, `semgrep`, `gitleaks`, `trufflehog`, `trivy`, GitHub CLI (`gh`), git worktrees, Obsidian MCP, Claude Code Agent tool.

**Source spec:** [`docs/superpowers/specs/2026-04-23-cto-readiness-audit-design.md`](../specs/2026-04-23-cto-readiness-audit-design.md) (preserved on `chore/cto-readiness-housekeeping`)

**Source plan:** [`docs/superpowers/plans/2026-04-23-cto-readiness-audit.md`](2026-04-23-cto-readiness-audit.md) — 1075-line full plan, also on `chore/cto-readiness-housekeeping`. This plan **defers to it** for any phase detail not modified here.

**Total wall-clock:** ~2–2.5 hours subagent work + founder review gates.

**Calendar target:** Ready by **2026-04-27** for the 2026-04-28 partner window.

---

## State Summary

**Canary repo (`growdirect-llc/canary-retail`) — DONE:**
- Tag `cto-review-ready-2026-04-24` on Canary `main`.
- `Canary/docs/audit-2026-04-23/` contains `canary.md`, `security.md`, `security-tool-output/` with bandit, gitleaks, pip-audit, semgrep, trivy, trufflehog, trufflehog-fs results.
- `Canary/NOTICE.md`, `Canary/ACKNOWLEDGMENT.md`, `Canary/SECURITY.md` exist.
- `Canary/brain/wiki/` (11 files) and `Canary/brain/projects/Canary.md` populated.
- Cleanup merged: `190b045 merge: CTO-readiness audit cleanup` and `16c03f4 merge: CTO-readiness security findings`.
- Sibling-vault refs scrubbed (Jeffe → CATz/Canary-Retail-Brain).

**GrowDirect repo — IN PROGRESS:**
- `chore/cto-readiness-housekeeping` (1 commit ahead of main): spec finalized, 1075-line plan preserved, 8 dispatches consolidated, CLAUDE.md "Flow In, Filtered Out" posture, root `SECURITY.md`. Not merged.
- No `docs/audit-2026-04-23/` at root.
- No `NOTICE.md`, no `ACKNOWLEDGMENT.md`, no `CONTRIBUTING.md`, no `docs/repo-sharing-matrix.md`, no `docs/standards/confidentiality-markings.md`.
- No `cto-review-ready-2026-04-24` tag.
- No worktrees active (`.worktrees/cto-spec/` referenced in source plan no longer exists).

**Brain MVP split — DRIFT FROM SPEC:**
- Spec called for `git mv` of Canary-scoped Brain into Canary repo, removing from `GrowDirect/Brain/`.
- Reality: Canary-scoped content is **duplicated** — present in both `GrowDirect/Brain/wiki/canary-*` and `Canary/brain/wiki/canary-*`. The GrowDirect-side removal did not happen. Recent founder work added `Brain/wiki/canary-module-*` cards on GrowDirect side, suggesting the founder vault is treated as superset, not a strict source of truth.
- **Decision required in Phase G1.**

---

## File Structure — what this plan creates

| Path | Purpose | Phase |
|---|---|---|
| `docs/audit-2026-04-23/platform.md` | GrowDirect platform code audit findings | G2 |
| `docs/audit-2026-04-23/docs-brain.md` | GrowDirect SHOW-scope docs + Platform-supporting Brain audit findings | G2 |
| `docs/audit-2026-04-23/security.md` | GrowDirect security audit findings | G2 |
| `docs/audit-2026-04-23/security-tool-output/` | Raw tool outputs (bandit, gitleaks, pip-audit, semgrep, trivy, trufflehog × 2) | G2 |
| `docs/audit-2026-04-23/enterprise-scale-gap-analysis.md` | Sanitized enterprise-scale gap analysis (was deferred from Canary side per spec — lives at GrowDirect level) | G2 |
| `docs/audit-2026-04-23/ready-to-show-confirmation.md` | Cold-reader verification report | G6 |
| `docs/audit-2026-04-23/cleanup-report.md` | Phase G4 cleanup report | G4 |
| `NOTICE.md` | Confidentiality notice (per spec template) | G7 |
| `ACKNOWLEDGMENT.md` | Access acknowledgment (per spec template) | G7 |
| `CONTRIBUTING.md` | Branch hygiene + loose-file rules (per spec) | G7 |
| `docs/standards/confidentiality-markings.md` | Canonical confidentiality-markings standard | G7 |
| `docs/repo-sharing-matrix.md` | Living access document | G7 |

---

## Chunk 1 — Phase G0: Bootstrap & branch consolidation

### Task G0.1: Verify current state matches plan assumptions

**Files:**
- Verify (read-only): branch state, tag list, root files, housekeeping branch contents.

- [ ] **Step G0.1.1: Verify GrowDirect branch state**

Run: `git -C /Users/gclyle/GrowDirect branch --show-current && git -C /Users/gclyle/GrowDirect log --oneline -5 && git -C /Users/gclyle/GrowDirect log --oneline main..chore/cto-readiness-housekeeping`

Expected: current branch printed (any working branch acceptable); housekeeping shows exactly 1 commit ahead of main (`1e7f389 chore(housekeeping)`).

If housekeeping has more than 1 commit, surface to founder — additional work landed there since plan author last looked.

- [ ] **Step G0.1.2: Verify Canary "done" state**

Run: `git -C /Users/gclyle/GrowDirect/Canary tag -l 2>&1 | grep cto-review-ready && ls /Users/gclyle/GrowDirect/Canary/{NOTICE.md,ACKNOWLEDGMENT.md,SECURITY.md} && ls /Users/gclyle/GrowDirect/Canary/docs/audit-2026-04-23/`

Expected: tag `cto-review-ready-2026-04-24` present; three root files present; audit dir contains `canary.md`, `security.md`, `security-tool-output/`.

If any missing, this plan's premise is wrong — surface to founder.

- [ ] **Step G0.1.3: Verify security tool availability on dispatch host**

Run: `which uvx pipx brew go 2>&1`

Expected: at least `uvx` or `pipx` (for Python tools); `brew` for trivy/gitleaks/trufflehog Go binaries. Memory `feedback_flag_dependency_changes.md` requires founder approval before any tool install. If tools missing, surface to founder; do not auto-install.

- [ ] **Step G0.1.4: Verify no active worktree from prior CTO-readiness work**

Run: `git -C /Users/gclyle/GrowDirect worktree list`

Expected: only the primary checkout. If a stale `.worktrees/cto-spec/` or similar appears, surface — may need cleanup before Phase G4 worktrees fire.

### Task G0.2: Resolve housekeeping branch fate

**Files:**
- `chore/cto-readiness-housekeeping` (read), `main` (target after merge).

- [ ] **Step G0.2.1: Inspect housekeeping commit content**

Run: `git -C /Users/gclyle/GrowDirect show 1e7f389 --stat`

Read: spec frontmatter changes, plan file size (1075 lines), dispatches list, CLAUDE.md additions.

- [ ] **Step G0.2.2: Surface merge decision to founder**

Present to founder:

> The `chore/cto-readiness-housekeeping` branch contains the finalized spec, the full 1075-line implementation plan, 8 consolidated dispatches, and CLAUDE.md "Flow In, Filtered Out" posture. It does NOT contain the audit reports or root standards files yet — those land in later phases. Should this branch be:
> 
> (a) Merged to `main` now to land the spec + plan + dispatches + CLAUDE.md changes as the baseline before audit runs, OR
> (b) Kept as-is until Phase G7, where everything (audit + cleanup + standards files) merges together?
> 
> Recommendation: (a) — landing the spec and plan on main first means the audit subagent in Phase G2 can reference the canonical spec at the canonical path, not at a branch path. This reduces "where does the source of truth live" ambiguity for downstream subagents.

- [ ] **Step G0.2.3: Execute founder's decision**

If (a): `git -C /Users/gclyle/GrowDirect checkout main && git -C /Users/gclyle/GrowDirect merge --no-ff chore/cto-readiness-housekeeping -m "merge: CTO-readiness spec + plan + housekeeping baseline"` — do NOT delete the branch yet (it's still useful as a reference).

If (b): no action; proceed to G0.3.

DO NOT push to origin without founder approval.

### Task G0.3: Decide feature-session freeze cadence

The original spec called for a Phase 0 decision on whether feature sessions freeze SHOW-scope changes between Phase 2 (audit) and Phase 4 (cleanup), or whether the cleanup subagent re-runs audit-dimension checks on its branch immediately before producing its report.

- [ ] **Step G0.3.1: Surface freeze decision to founder**

Present:

> Cleanup subagents (Phase G4) work in `~/.worktrees/growdirect-cto-cleanup/` on `chore/cto-readiness-audit-2026-04-24`. Between Phase G2 audit baseline and Phase G4 cleanup, feature sessions on `main` could land SHOW-scope changes that would distort the cleanup-vs-baseline diff. Two options:
> 
> (a) Freeze: do not land SHOW-scope changes on `main` between G2 baseline and G4 cleanup merge.
> (b) Re-baseline: cleanup subagent re-runs audit-dimension scan on its worktree branch immediately before producing cleanup-report.md, surfaces any new findings introduced by concurrent landings.
> 
> Recommendation: (b) — Solex / consulting / brain work is in active progress and freezing main isn't realistic. Re-baseline is cheap (15 min audit re-run inside the worktree) and gives an honest report.

- [ ] **Step G0.3.2: Document decision**

Append to this plan a note under each Phase G2 task: "Cadence: re-baseline (per G0.3) / freeze (per G0.3)".

### Task G0.4: Commit Phase G0 outcomes

- [ ] **Step G0.4.1: Commit any pending state**

If G0.2 produced a merge commit, that's already on main. If G0.3 modified this plan file, stage and commit.

```bash
git -C /Users/gclyle/GrowDirect add docs/superpowers/plans/2026-04-24-cto-readiness-remaining.md
git -C /Users/gclyle/GrowDirect commit -m "chore(cto-readiness): phase G0 bootstrap decisions captured"
```

---

## Chunk 2 — Phase G1: Brain MVP split reconciliation

### Task G1.1: Surface Brain split drift to founder

**Files:**
- Read: `Brain/wiki/canary-*.md`, `Brain/projects/Canary.md`, `Canary/brain/wiki/canary-*.md`, `Canary/brain/projects/Canary.md`.

- [ ] **Step G1.1.1: Compare GrowDirect Brain vs Canary brain contents**

Run:
```bash
ls /Users/gclyle/GrowDirect/Brain/wiki/canary-*.md | sort > /tmp/gd-canary-wiki.txt
ls /Users/gclyle/GrowDirect/Canary/brain/wiki/canary-*.md | sort > /tmp/canary-canary-wiki.txt
diff /tmp/gd-canary-wiki.txt /tmp/canary-canary-wiki.txt
```

Expected: GrowDirect side has more files (the recent `canary-module-*` cards plus duplicates of what's already in Canary). Canary side has only the original 11 from the Phase 1 split.

- [ ] **Step G1.1.2: Identify content drift between duplicates**

For each file present in both vaults, compare:

```bash
for f in canary-architecture canary-data-model canary-detection canary-fox-case-management canary-platform-overview; do
  echo "=== $f ==="
  diff /Users/gclyle/GrowDirect/Brain/wiki/$f.md /Users/gclyle/GrowDirect/Canary/brain/wiki/$f.md 2>&1 | head -10
done
```

Expected: differences show GrowDirect-side has more recent edits (recent commits on `fix/solex-live-debug-pass` modified `canary-architecture`, `canary-data-model`, `canary-detection`, `canary-fox-case-management`, `canary-platform-overview`).

- [ ] **Step G1.1.3: Present three-option decision to founder**

> Brain MVP split drift: Canary-scoped wiki files are present in both `GrowDirect/Brain/wiki/canary-*` and `Canary/brain/wiki/canary-*`. The GrowDirect copies have ~6 weeks of edits the Canary copies do not. Three options:
> 
> (a) **Strict spec compliance:** `git rm` the Canary-scoped files from GrowDirect/Brain. Re-sync Canary side from GrowDirect first to capture the drift edits. Future Canary edits happen in Canary repo only. Founder vault loses the unified-view convenience.
> 
> (b) **Founder vault as superset:** Treat `GrowDirect/Brain/` as the founder's working vault (superset). `Canary/brain/` is the SHOW-scoped projection — refreshed manually before partner access. Canary-scoped files stay in GrowDirect/Brain/. Drift is acceptable as long as the SHOW projection is up to date at access time.
> 
> (c) **Symlink:** Replace `Canary/brain/wiki/canary-*` with symlinks to `GrowDirect/Brain/wiki/canary-*`. Single source of truth without mental overhead. Risk: cross-repo symlinks are fragile; broken on clone-without-sibling-checkout.
> 
> Recommendation: (b) for MVP. Document that Canary repo's `brain/` is a periodic projection, not a live mirror. Refresh script runs in Phase G7 just before partner access. (a) is "more correct" by spec but loses founder workflow value; (c) is fragile.

- [ ] **Step G1.1.4: Document founder's decision**

Append a frontmatter note to this plan capturing the chosen option. Update spec §"Brain MVP Split" if needed (spec lives on housekeeping branch or main depending on G0.2 outcome).

### Task G1.2: Execute reconciliation per founder decision

Three branches by decision:

#### G1.2-A: Strict spec compliance (option a)

- [ ] **Step G1.2-A.1: Sync GrowDirect drift edits into Canary brain**

For each Canary-scoped wiki file with content drift:
```bash
cp /Users/gclyle/GrowDirect/Brain/wiki/canary-X.md /Users/gclyle/GrowDirect/Canary/brain/wiki/canary-X.md
```

Stage in Canary repo:
```bash
git -C /Users/gclyle/GrowDirect/Canary add brain/wiki/canary-*.md
git -C /Users/gclyle/GrowDirect/Canary commit -m "brain: sync drift edits from GrowDirect/Brain pre-removal"
```

- [ ] **Step G1.2-A.2: Identify full removal list**

Per spec §"Brain MVP Split" — Canary wiki, Canary projects, Canary SDDs, Canary-scoped specs/plans, demo-reseed dispatch. Build canonical list:
```bash
ls /Users/gclyle/GrowDirect/Brain/wiki/canary-*.md /Users/gclyle/GrowDirect/Brain/wiki/growdirect-canary*.md /Users/gclyle/GrowDirect/Brain/wiki/growdirect-the-chirp*.md /Users/gclyle/GrowDirect/Brain/wiki/growdirect-the-fox*.md /Users/gclyle/GrowDirect/Brain/wiki/growdirect-chirp-udq*.md /Users/gclyle/GrowDirect/Brain/projects/Canary.md /Users/gclyle/GrowDirect/docs/sdds/canary/ 2>&1
```

Cross-reference with Canary brain — anything in the GrowDirect list but NOT in Canary brain is a sync gap to resolve before removal.

- [ ] **Step G1.2-A.3: Execute git mv equivalent (rm on GrowDirect side)**

```bash
git -C /Users/gclyle/GrowDirect checkout -b chore/brain-mvp-split-completion-2026-04-24
git -C /Users/gclyle/GrowDirect rm Brain/wiki/canary-*.md Brain/projects/Canary.md
# additional rm calls per the canonical list from G1.2-A.2
```

- [ ] **Step G1.2-A.4: Run Obsidian broken-link pass**

Use `mcp__obsidian__find_broken_links_tool` on the GrowDirect vault. Fix or remove broken links in the platform-supporting Brain that pointed to removed Canary content.

- [ ] **Step G1.2-A.5: Commit the removal**

```bash
git -C /Users/gclyle/GrowDirect add -u Brain/ docs/sdds/
git -C /Users/gclyle/GrowDirect commit -m "chore(brain): complete MVP split — remove Canary-scoped content from GrowDirect/Brain"
```

Surface to founder for merge to main.

#### G1.2-B: Founder vault as superset (option b — recommended)

- [ ] **Step G1.2-B.1: Document the model in CLAUDE.md**

Add a brief section to `/Users/gclyle/GrowDirect/CLAUDE.md` under "Brain — Domain Knowledge":

```markdown
### Canary Brain projection

`Canary/brain/` is a SHOW-scoped projection of `GrowDirect/Brain/` —
refreshed manually before partner access. Live edits happen in
`GrowDirect/Brain/`. Canary repo is not the source of truth for Brain
content; the platform vault is. Drift between the two is acceptable
between projections.

A refresh script (Phase G7 deliverable) syncs Canary-scoped wiki
articles, project MOCs, and SDDs from `GrowDirect/Brain/` and
`docs/sdds/canary/` into the corresponding `Canary/brain/` and
`Canary/docs/sdds/` paths.
```

- [ ] **Step G1.2-B.2: Refresh Canary projection from current GrowDirect state**

For each Canary-scoped file in GrowDirect with drift edits, copy into Canary:
```bash
cp /Users/gclyle/GrowDirect/Brain/wiki/canary-architecture.md /Users/gclyle/GrowDirect/Canary/brain/wiki/canary-architecture.md
# repeat for all drift files identified in G1.1.2
```

Also copy the new module cards added recently:
```bash
cp /Users/gclyle/GrowDirect/Brain/wiki/canary-module-*.md /Users/gclyle/GrowDirect/Canary/brain/wiki/
cp /Users/gclyle/GrowDirect/Brain/wiki/canary-architecture-decisions-index.md /Users/gclyle/GrowDirect/Canary/brain/wiki/
cp /Users/gclyle/GrowDirect/Brain/wiki/canary-vsm-*.md /Users/gclyle/GrowDirect/Canary/brain/wiki/
cp /Users/gclyle/GrowDirect/Brain/wiki/canary-ej-spine-and-sales-audit.md /Users/gclyle/GrowDirect/Canary/brain/wiki/
cp /Users/gclyle/GrowDirect/Brain/wiki/canary-raas-positioning.md /Users/gclyle/GrowDirect/Canary/brain/wiki/
cp /Users/gclyle/GrowDirect/Brain/projects/Canary.md /Users/gclyle/GrowDirect/Canary/brain/projects/Canary.md
```

- [ ] **Step G1.2-B.3: Commit projection refresh in Canary repo**

```bash
git -C /Users/gclyle/GrowDirect/Canary add brain/
git -C /Users/gclyle/GrowDirect/Canary commit -m "brain: refresh Canary projection from GrowDirect/Brain (pre-cto-review)"
```

- [ ] **Step G1.2-B.4: Run broken-link pass on Canary brain**

Use `mcp__obsidian__find_broken_links_tool` against the `Canary/brain/` vault — wikilinks that reference content NOT in the Canary projection (e.g., `[[secure-architecture]]`) need to be removed or rewritten.

- [ ] **Step G1.2-B.5: Commit CLAUDE.md change**

```bash
git -C /Users/gclyle/GrowDirect add CLAUDE.md
git -C /Users/gclyle/GrowDirect commit -m "docs(claude.md): document Canary/brain/ as projection of GrowDirect/Brain/"
```

#### G1.2-C: Symlink (option c)

Not detailed here. If founder picks (c), pause execution and re-plan; symlinks add operational complexity beyond MVP scope.

---

## Chunk 3 — Phase G2: Audit dispatch (GrowDirect SHOW scope)

The Canary side already ran. This phase produces the platform-side audit reports. **Reuse the Phase 2 audit dispatch prompt from the source plan** — `docs/superpowers/plans/2026-04-23-cto-readiness-audit.md` Chunk 2 — adapted to GrowDirect-only scope.

### Task G2.1: Prepare audit-output directory

- [ ] **Step G2.1.1: Create directory structure**

```bash
mkdir -p /Users/gclyle/GrowDirect/docs/audit-2026-04-23/security-tool-output
```

- [ ] **Step G2.1.2: Stage gitkeep so dir tracks**

```bash
touch /Users/gclyle/GrowDirect/docs/audit-2026-04-23/.gitkeep
git -C /Users/gclyle/GrowDirect add docs/audit-2026-04-23/.gitkeep
git -C /Users/gclyle/GrowDirect commit -m "chore(cto-readiness): scaffold audit output directory for G2"
```

### Task G2.2: Dispatch four parallel audit subagents

Per spec §"Phase 2 — Audit dispatch [P — read-only, parallel-safe]". Fire **four** subagents in a single message (no `canary-audit` — Canary is done):

- `platform-audit` → `docs/audit-2026-04-23/platform.md`
- `docs-brain-audit` → `docs/audit-2026-04-23/docs-brain.md` (GrowDirect platform-supporting Brain only)
- `security-audit` → `docs/audit-2026-04-23/security.md` + `security-tool-output/` (full git history)
- `enterprise-scale-gap` → `docs/audit-2026-04-23/enterprise-scale-gap-analysis.md` (sanitized)

- [ ] **Step G2.2.1: Read the source plan's Chunk 2 audit-dispatch prompts**

The four subagent prompts are defined in detail at:
- `docs/superpowers/plans/2026-04-23-cto-readiness-audit.md` — Tasks 5, 6, 7 (in plan terms — see Chunk 2).

Adapt:
- Drop `canary-audit` (Canary done).
- `platform-audit` scope: `devops/`, `services/`, `content-engine/`, `growdirect-platform.plugin/`, root-level Python.
- `docs-brain-audit` scope: `docs/sdds/platform/`, `docs/sdds/alx/`, SHOW-scope `docs/superpowers/specs/` (non-Canary), `docs/superpowers/dispatches/` (non-Canary), `Brain/projects/Method.md`, `Brain/projects/Factory.md`, `Brain/projects/GrowDirect.md`, `Brain/method/`, factory-process wiki, Platform-supporting Brain.
- `security-audit` scope: GrowDirect repo full history; tools per spec §"Security dimensions — automated".
- `enterprise-scale-gap` scope: sanitized; reads existing Canary audit outputs as input.

- [ ] **Step G2.2.2: Use superpowers:dispatching-parallel-agents skill**

Per the parallel-dispatch skill, fire 4 Agent calls in a single message. Each gets:
- Audit dimensions table from spec §"Audit Dimensions"
- File-path scope (above)
- Output path (above)
- Finding format: file path, line number, exact offending text, severity (CRITICAL/HIGH/MEDIUM/LOW), recommended action.
- Strict instruction: read-only, no source-file mutations, no `requirements.txt` / `package.json` changes (per memory `feedback_flag_dependency_changes.md`).

- [ ] **Step G2.2.3: Verify reports landed**

```bash
ls -la /Users/gclyle/GrowDirect/docs/audit-2026-04-23/
ls /Users/gclyle/GrowDirect/docs/audit-2026-04-23/security-tool-output/
```

Expected: `platform.md`, `docs-brain.md`, `security.md`, `enterprise-scale-gap-analysis.md`, plus 7 `*.json` + `*.stderr` pairs in security-tool-output.

- [ ] **Step G2.2.4: Commit audit reports**

```bash
git -C /Users/gclyle/GrowDirect add docs/audit-2026-04-23/
git -C /Users/gclyle/GrowDirect commit -m "audit: CTO-readiness audit reports — GrowDirect platform side (Phase G2)"
```

---

## Chunk 4 — Phase G3: Audit review (founder gate)

### Task G3.1: Founder reads four reports

- [ ] **Step G3.1.1: Render report summaries**

Surface to founder: brief per-report summary — finding counts by severity, top 5 highest-severity findings per dimension. Source plan's Phase 3 task structure applies.

- [ ] **Step G3.1.2: Founder assigns dispositions**

Per spec §"Conservative Cleanup Philosophy" Rule 4 — TODO disposition is one of resolve / convert-to-Linear / remove. Also: judgment calls per Rule 7 surface for founder decision.

- [ ] **Step G3.1.3: Critical decision — committed-secret rotations**

If `gitleaks` or `trufflehog` found ANY secret in git history, success criterion 10 mandates rotate AND purge from history (BFG or `git filter-repo`). Per spec, this triggers a separate workstream with founder sign-off. Document each finding with one of:
- `rotate-and-rewrite-history` workstream triggered → exits this plan, re-enters at G5.
- `not-a-real-secret` (e.g., test fixture, public-by-design key) — disposition logged in audit report.

- [ ] **Step G3.1.4: Confirm enterprise-scale-gap framing**

Founder reviews `enterprise-scale-gap-analysis.md` for: (a) sanitization (no prior-client names), (b) honest separation of GAP-by-roadmap vs CHOICE-by-design, (c) defensibility on cold read. Edit as needed; commit edits.

---

## Chunk 5 — Phase G4: Cleanup dispatch (worktree-isolated)

### Task G4.1: Create worktree and branch

- [ ] **Step G4.1.1: Use superpowers:using-git-worktrees skill**

Per the worktree skill, create:
```bash
git -C /Users/gclyle/GrowDirect worktree add ~/.worktrees/growdirect-cto-cleanup -b chore/cto-readiness-audit-2026-04-24 main
```

(Date suffix `2026-04-24` matches Canary's tag, not the spec's `2026-04-23` — the spec was authored 04-23 but Canary tagged 04-24 and partner window is 04-28.)

- [ ] **Step G4.1.2: Verify worktree**

```bash
git -C /Users/gclyle/GrowDirect worktree list
ls ~/.worktrees/growdirect-cto-cleanup/
```

### Task G4.2: Dispatch two cleanup subagents (one message)

Per spec §"Phase 4 — Cleanup dispatch [P via git worktrees]":

- `platform-cleanup` → operates inside `~/.worktrees/growdirect-cto-cleanup/`
- `security-fix` → operates on a separate branch `chore/security-findings-2026-04-24` (rollback characteristics differ; security fixes can be reverted independently of TODO/scrub work)

- [ ] **Step G4.2.1: Read source plan's Chunk 3 cleanup-dispatch prompts**

`docs/superpowers/plans/2026-04-23-cto-readiness-audit.md` — Phase 4 task structure.

- [ ] **Step G4.2.2: Dispatch with re-baseline cadence (per G0.3)**

Each subagent re-runs audit-dimension scan on its branch immediately before producing report. Folds new findings into cleanup scope or surfaces out-of-scope.

Cleanup scope per Phase G2 findings + the eight rules of Conservative Cleanup Philosophy:
- Rule 1: branch-only, no main-direct work.
- Rule 2: scale-back over polish-in-place.
- Rule 3: thoughtful-stub five-point test for any remaining stubs.
- Rule 4: TODO disposition (resolve/convert/remove).
- Rule 5: no surprise refactoring.
- Rule 6: subagents don't merge.
- Rule 7: judgment calls surface to founder.
- Rule 8: preserve git history (one exception: secret rotation, separate workstream).

Confidentiality markings sweep:
- Source files: GrowDirect LLC header (per spec §"Standards").
- Markdown frontmatter: `classification: confidential`, `owner: GrowDirect LLC` on every SHOW'd `.md`.

- [ ] **Step G4.2.3: Verify cleanup-report.md per branch**

```bash
ls ~/.worktrees/growdirect-cto-cleanup/docs/audit-2026-04-23/cleanup-report.md
git -C /Users/gclyle/GrowDirect log chore/security-findings-2026-04-24 --oneline | head -10
```

### Task G4.3: Subagents do NOT merge

Per Rule 6. Founder reviews and merges in Phase G5.

---

## Chunk 6 — Phase G5: Cleanup review (founder gate)

Per spec §"Phase 5":

- [ ] **Step G5.1: Founder reviews cleanup-report.md**

Walk through every changed file. Approve or flag for adjustment.

- [ ] **Step G5.2: Merge order**

1. `chore/cto-readiness-audit-2026-04-24` first.
2. (If history-rewrite workstream triggered:) committed-secret rewrite, with founder sign-off.
3. `chore/security-findings-2026-04-24` second.

```bash
git -C /Users/gclyle/GrowDirect checkout main
git -C /Users/gclyle/GrowDirect merge --no-ff chore/cto-readiness-audit-2026-04-24 -m "merge: CTO-readiness audit cleanup (Phase G4 platform)"
git -C /Users/gclyle/GrowDirect merge --no-ff chore/security-findings-2026-04-24 -m "merge: CTO-readiness security findings (Phase G4 security-fix)"
```

DO NOT push to origin without founder approval (CLAUDE.md rule).

- [ ] **Step G5.3: Worktree cleanup**

```bash
git -C /Users/gclyle/GrowDirect worktree remove ~/.worktrees/growdirect-cto-cleanup
git -C /Users/gclyle/GrowDirect branch -d chore/cto-readiness-audit-2026-04-24 chore/security-findings-2026-04-24
```

---

## Chunk 7 — Phase G6: Cold-reader verification

### Task G6.1: Cold-reader subagent

- [ ] **Step G6.1.1: Dispatch one read-only subagent**

Per spec §"Phase 6 — Dry-run cold-reader verification". Subagent simulates a cold technical-co-founder reader: starts at `README.md`, walks architecture → code → tests → audit reports.

Verifies:
- `NOTICE.md`, `ACKNOWLEDGMENT.md`, `SECURITY.md`, `CONTRIBUTING.md` at root (Phase G7 produces these — verify they're present after G7 lands; this phase runs LAST among gating phases).

**NOTE:** Phase 6 in the source spec runs BEFORE Phase 7 because the source spec assumed Phase 7 only produced repo-rename, tag, mailbox. In this remaining-work plan, Phase G7 produces the root standards files (because they don't exist yet on GrowDirect). Re-order: **G7 runs before G6**.

- [ ] **Step G6.1.2: Re-confirm phase order**

Update this plan's phase headers: G7 before G6, OR keep order and have G6 verify post-G7-creation state. Founder's call.

Recommendation: keep numeric order but document that G7 task outputs (root standards files) are inputs to G6 verification. G7 cleanup pass at end of G7 produces the verification target; G6 then runs.

- [ ] **Step G6.1.3: Subagent produces ready-to-show-confirmation.md**

Output: `docs/audit-2026-04-23/ready-to-show-confirmation.md` — either **PASS** or a regression list.

If regression: return to G4 for one more cleanup pass. Do not paper over.

- [ ] **Step G6.1.4: Commit confirmation**

```bash
git -C /Users/gclyle/GrowDirect add docs/audit-2026-04-23/ready-to-show-confirmation.md
git -C /Users/gclyle/GrowDirect commit -m "audit: cold-reader confirmation PASS (Phase G6)"
```

---

## Chunk 8 — Phase G7: Ready-to-share

### Task G7.1: Create root standards files

Per spec §"Standards — confidentiality markings and repo-root files".

**Files (create on `main`, or on a small chore branch then fast-forward):**
- Create: `/Users/gclyle/GrowDirect/NOTICE.md`
- Create: `/Users/gclyle/GrowDirect/ACKNOWLEDGMENT.md`
- Create: `/Users/gclyle/GrowDirect/CONTRIBUTING.md`
- Create: `/Users/gclyle/GrowDirect/docs/standards/confidentiality-markings.md`
- Create: `/Users/gclyle/GrowDirect/docs/repo-sharing-matrix.md`
- Verify exists: `/Users/gclyle/GrowDirect/SECURITY.md` (already exists — minor edit may be needed to add audit-completion sentence per spec template)

- [ ] **Step G7.1.1: Author NOTICE.md**

Use the exact text from spec §"Repo-root `NOTICE.md`":

```markdown
# Confidential & Proprietary

Copyright © 2026 GrowDirect LLC. All rights reserved.

This repository contains confidential and proprietary information of
GrowDirect LLC. Access is granted only to parties who have acknowledged
the access terms set forth in ACKNOWLEDGMENT.md or are subject to a
written agreement with GrowDirect LLC.

Disclosure, reproduction, distribution, or derivative use of any part
of this repository — including code, documentation, designs,
architecture, data models, and process artifacts — is prohibited
without prior written consent of GrowDirect LLC.

Inquiries: contact@growdirect.io
```

Reference Canary's NOTICE.md for any minor adaptations: `cat /Users/gclyle/GrowDirect/Canary/NOTICE.md`.

- [ ] **Step G7.1.2: Author ACKNOWLEDGMENT.md**

Use spec §"Repo-root `ACKNOWLEDGMENT.md`" template verbatim. Reference `Canary/ACKNOWLEDGMENT.md` for adaptations.

- [ ] **Step G7.1.3: Author CONTRIBUTING.md**

Codify per spec §"Enduring hygiene standards":
- Branch hygiene: `feat/*`, `fix/*`, `chore/*`, `security/*`, `gro-NNN-*`. AI-agent-generated random names merged+deleted or evaluated+deleted within 7 days.
- Loose-file rule: no `.md` at repo root except `README.md`, `CLAUDE.md`, `AGENTS.md`, `NOTICE.md`, `ACKNOWLEDGMENT.md`, `SECURITY.md`, `CONTRIBUTING.md`, `LICENSE`.
- Integration test rule (spec §"Audit Dimensions" / "Test coverage surface"): integration tests use real database fixtures (no DB mocking) — codified as project rule.

- [ ] **Step G7.1.4: Author docs/standards/confidentiality-markings.md**

Canonical reference. Move spec §"Standards" content here. Includes:
- Code file header (two lines, language-equivalent comment syntax).
- Markdown frontmatter (`classification: confidential`, `owner: GrowDirect LLC`).
- Where the standards apply (every SHOW'd file).

- [ ] **Step G7.1.5: Author docs/repo-sharing-matrix.md**

Per spec §"Repo-sharing matrix — deliverable artifact" template:

```markdown
| Repo | Classification | Default access | Instrument | Contains | Excluded |
|---|---|---|---|---|---|
| `growdirect-llc/canary-retail` | Confidential | SHOW under NDA or acknowledgment | Reply-to-email Mechanism 1 default; formal NDA escalation available | Canary app + Canary brain projection | Cove, Angel, Seacove, ownpv, Secure, commercial strategy |
| GrowDirect monorepo (private) | Confidential | SHOW under NDA or acknowledgment, scoped view | Same | Shared platform, method, factory, platform-supporting Brain | All HIDE items per spec §Scope |
| `growdirectprez.github.io` | Public | Public | N/A | Marketing site only | N/A |
| Future — Cove, Angel, Seacove, ownpalosverdes | Confidential (separate scope) | HIDE for current CTO partner; separate agreements if ever shown | Separate per scope | Per-project | N/A |
```

Update with current remote URL for GrowDirect (the org name and repo name).

- [ ] **Step G7.1.6: Update SECURITY.md (minor)**

Append to existing `/Users/gclyle/GrowDirect/SECURITY.md` per spec template — add audit-completion paragraph:

```markdown
GrowDirect LLC has completed automated vulnerability scanning, static
application security testing (SAST), full git-history secret scanning,
and a structured OWASP Top 10 code-level review. A formal third-party
penetration test has not been performed and is scheduled if-and-when
commercial engagement proceeds. Findings from the automated and
code-level review are documented in `docs/audit-2026-04-23/security.md`
and `docs/audit-2026-04-23/security-tool-output/`.
```

- [ ] **Step G7.1.7: Commit standards files**

```bash
git -C /Users/gclyle/GrowDirect add NOTICE.md ACKNOWLEDGMENT.md CONTRIBUTING.md SECURITY.md docs/standards/confidentiality-markings.md docs/repo-sharing-matrix.md
git -C /Users/gclyle/GrowDirect commit -m "chore(cto-readiness): root standards files + sharing matrix (Phase G7)"
```

### Task G7.2: Confirm Phase G6 prerequisites and run G6

Per G6.1.2 — re-order: G6 runs after G7.1 produces the standards files.

Loop back to Chunk 7. After G6 PASS, return to G7.3.

### Task G7.3: Tag ready-to-share state

- [ ] **Step G7.3.1: Tag GrowDirect**

```bash
git -C /Users/gclyle/GrowDirect tag -a cto-review-ready-2026-04-24 -m "CTO-review ready state — GrowDirect platform side"
```

(Use 2026-04-24 to align with Canary tag; OR pick the actual date of completion if later than 04-24.)

- [ ] **Step G7.3.2: Verify both repos tagged**

```bash
git -C /Users/gclyle/GrowDirect tag -l | grep cto-review-ready
git -C /Users/gclyle/GrowDirect/Canary tag -l | grep cto-review-ready
```

Both should print `cto-review-ready-2026-04-24` (or matching date).

### Task G7.4: Mailbox confirmation

- [ ] **Step G7.4.1: Founder confirms `contact@growdirect.io` and `security@growdirect.io` are receiving mail**

Founder action — verify in Fastmail (or whatever provider). NOT a subagent task. Surface to founder for confirmation only.

### Task G7.5: Access-grant email template

- [ ] **Step G7.5.1: Author template at `docs/access-grant-email-template.md`**

```markdown
Subject: GrowDirect — Repository Access for [Partner Name]

Hi [Partner Name],

Per our conversation, attached are the access details for evaluating
the GrowDirect platform under acknowledgment of confidentiality.

Acknowledgment terms: [paste contents of ACKNOWLEDGMENT.md, OR link
to the file in the repo if the partner is being granted GitHub access
ahead of reply].

Please reply to this email with the literal phrase "I acknowledge and
agree" before access is granted. The email thread is the durable
record of acknowledgment.

Repos in scope for this access (see repo-sharing-matrix.md for
exclusions):

- growdirect-llc/canary-retail
- GrowDirect monorepo (scoped read-only invite once acknowledgment received)

Excluded from this access (per repo-sharing-matrix.md): Cove, Angel,
Seacove, ownpalosverdes, prior-client retail loss-prevention IP,
Linear roadmap, raw intake material, founder operational Brain.

Inquiries: contact@growdirect.io
Security reports: security@growdirect.io
```

- [ ] **Step G7.5.2: Commit access-grant template**

```bash
git -C /Users/gclyle/GrowDirect add docs/access-grant-email-template.md
git -C /Users/gclyle/GrowDirect commit -m "docs(cto-readiness): access-grant email template (Phase G7)"
```

- [ ] **Step G7.5.3: Founder sends access-grant email**

NOT a subagent task. Founder customizes per partner and sends.

### Task G7.6: Optional — push to origin

- [ ] **Step G7.6.1: Surface push decision to founder**

```bash
git -C /Users/gclyle/GrowDirect log origin/main..main --oneline
```

Show all commits that would be pushed. Founder approves push:

```bash
git -C /Users/gclyle/GrowDirect push origin main
git -C /Users/gclyle/GrowDirect push origin cto-review-ready-2026-04-24
```

Same for Canary if not already pushed.

DO NOT force-push under any circumstance.

---

## Definition of Done — dispatch level

All eleven success criteria from the spec verify true on **both repos**:

1. Zero unresolved markers in SHOW scope (Canary ✅; GrowDirect — verify via Phase G2/G4).
2. Zero sloppy stubs (Canary ✅; GrowDirect — verify).
3. Zero AI-voice commentary (Canary ✅; GrowDirect — verify).
4. Zero client / personal / sensitive names in SHOW scope (Canary ✅; GrowDirect — verify, especially `Brain/wiki/methodology-ibm-*`, `Brain/wiki/secure-architecture.md`, retail consulting SDDs).
5. Confidentiality markings on every SHOW'd file; root standards files (Canary ✅; GrowDirect — Phase G7 produces).
6. Enterprise-scale gap analysis exists, sanitized (Canary side has no gap doc currently — produced fresh in G2 at GrowDirect level for both repos).
7. Git state clean (Canary ✅; GrowDirect — Phase G5 produces).
8. Brain MVP split executed (Canary ✅; GrowDirect — Phase G1 reconciliation per founder choice).
9. `docs/repo-sharing-matrix.md` finalized (G7.1.5).
10. Security audit findings resolved or have explicit founder disposition (Canary ✅; GrowDirect — Phase G3/G4). Committed secrets rotated AND purged from history if found.
11. Cold-reader verification PASS per repo (Canary — re-run if any post-tag changes; GrowDirect — Phase G6).

When all eleven verify, this plan closes. Tag `cto-review-ready-2026-04-24` on each repo + `docs/repo-sharing-matrix.md` are the durable artifacts.

---

## Open decisions (carry forward)

From spec §"Open questions / deferred decisions" — reaffirmed for this remaining-work plan:

1. **Canary factory skills location** — defaulted *centralized*; revisit only if G4 surfaces a finding.
2. **Brain subtree split for history preservation** — accepted as MVP compromise; not closed.
3. **Full hierarchical Brain restructure** — out of scope; not closed.
4. **Enterprise lineage narrative** — out of scope; not closed.
5. **History rewrite on security findings** — closed *if-and-when* gitleaks/trufflehog surface a committed secret in G2.
6. **NEW: Brain split posture** — strict / superset / symlink (G1.1.3). Recommendation: superset (option b).
7. **NEW: Feature-session freeze cadence** — freeze / re-baseline (G0.3.1). Recommendation: re-baseline.
8. **NEW: Phase G6/G7 ordering** — G7 produces standards files that G6 verifies; document the dependency, run G7.1 before G6, then G7.3-G7.6.

---

## Sources

- Source spec: `docs/superpowers/specs/2026-04-23-cto-readiness-audit-design.md` (preserved on `chore/cto-readiness-housekeeping`).
- Source plan: `docs/superpowers/plans/2026-04-23-cto-readiness-audit.md` (1075 lines, same branch).
- Canary repo state assessment: 2026-04-24 — tag `cto-review-ready-2026-04-24`, audit reports in place, three confidentiality files present.
- GrowDirect repo state assessment: 2026-04-24 — main lacks NOTICE/ACKNOWLEDGMENT/CONTRIBUTING/sharing-matrix; housekeeping branch carries spec + plan + dispatches.
- Memory feedback: `feedback_no_loose_files.md`, `feedback_git_health_check_first.md`, `feedback_flag_dependency_changes.md`, `feedback_full_sweep_no_deferrals.md`.

---

*Authored 2026-04-24 by Claude as the remaining-work plan picking up from the original 2026-04-23 plan, scoped to the GrowDirect platform side after Canary side fully shipped. Defers to source spec for design decisions; defers to source plan for unchanged phase detail.*
