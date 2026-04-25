# CTO-Readiness Audit Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Execute the CTO-readiness audit — hygiene-and-scoping pass across Canary and SHOW-scope GrowDirect platform components, producing a defensible state under NDA for an external co-founder review.

**Architecture:** Eight sequenced phases (0–7). Phase 0 bootstrap → Phase 1 Brain MVP split → Phase 2 audit (read-only, parallel) → Phase 3 user review gate → Phase 4 cleanup (worktree-isolated) → Phase 5 user review gate → Phase 6 dry-run verification → Phase 7 ready-to-share. Cleanup uses git worktrees to avoid disturbing concurrent feature sessions.

**Tech Stack:** Python 3.12, `pip-audit`, `bandit`, `semgrep`, `gitleaks`, `trufflehog`, `trivy`, GitHub CLI (`gh`), git worktrees, Obsidian MCP, Claude Code Agent tool.

**Source spec:** [docs/superpowers/specs/2026-04-23-cto-readiness-audit-design.md](../specs/2026-04-23-cto-readiness-audit-design.md)

**Total wall-clock:** ~2.5–3 hours across subagent phases + user review gate time.

---

## Chunk 1 — Phase 0 Bootstrap + Phase 1 Brain MVP Split

### Task 1: Verify prerequisites

**Files:**
- Read: `/Users/gclyle/GrowDirect/CLAUDE.md`, `/Users/gclyle/GrowDirect/Canary/CLAUDE.md`
- Verify: git state on both repos, tool availability

- [ ] **Step 1.1: Verify current branch state in GrowDirect**

Run: `git -C /Users/gclyle/GrowDirect branch --show-current && git -C /Users/gclyle/GrowDirect worktree list`

Expected: primary checkout on some branch (may not be main); worktree list includes `.worktrees/cto-spec/ [chore/cto-readiness-spec-2026-04-23]`

Record the primary checkout's current branch. Do NOT switch it — another session may be using it.

- [ ] **Step 1.2: Verify Canary repo branch state**

Run: `git -C /Users/gclyle/GrowDirect/Canary branch --show-current && git -C /Users/gclyle/GrowDirect/Canary branch -a 2>&1 | head -20`

Expected: lists branches including `security/platform-hardening`, 6× `claude/*` agent-generated branches, `gro-386-fix-canary-login-*`, `main`. Record which branch is currently checked out.

- [ ] **Step 1.3: Verify security tools are installable**

Run: `which uvx && which pipx && which brew && which go`

Expected: at least `uvx` or `pipx` present (for Python tools), `brew` for Go binaries. If none available, abort and surface to user — tooling setup is a user-approval required step per memory `feedback_flag_dependency_changes.md`.

- [ ] **Step 1.4: Confirm worktree baseline**

Run: `git -C /Users/gclyle/GrowDirect/.worktrees/cto-spec log --oneline -3`

Expected: top commit is `chore: cto-readiness audit design spec + pre-audit hygiene` at `048cdac`.

---

### Task 2: Evaluate Canary `security/platform-hardening` branch

**Files:**
- Read: `git log security/platform-hardening` in Canary repo
- Decision artifact: in-memory disposition noted by user

This task blocks Phase 2 because the audit must reflect current state, not stale state.

- [ ] **Step 2.1: Check if branch is merged into Canary main**

Run: `git -C /Users/gclyle/GrowDirect/Canary log main..security/platform-hardening --oneline`

Expected: either empty (already merged) or a list of commits (unmerged).

- [ ] **Step 2.2: If unmerged, inspect contents**

Run: `git -C /Users/gclyle/GrowDirect/Canary diff main...security/platform-hardening --stat`

Read the commits: `git -C /Users/gclyle/GrowDirect/Canary log main..security/platform-hardening --format="%h %s%n%b" -5`

- [ ] **Step 2.3: Surface disposition to user**

Present to user: (a) what's in the branch, (b) whether it looks like real security fixes vs stub/experimental work, (c) recommendation — merge to main now so audit sees current state, or delete if abandoned.

Wait for user decision. DO NOT merge or delete without explicit approval.

- [ ] **Step 2.4: Execute user's decision**

If merge: `git -C /Users/gclyle/GrowDirect/Canary checkout main && git -C /Users/gclyle/GrowDirect/Canary merge --no-ff security/platform-hardening -m "merge: security/platform-hardening into main (pre-audit bootstrap)"`

If delete: `git -C /Users/gclyle/GrowDirect/Canary branch -d security/platform-hardening` (use `-D` only if user explicitly approves force-delete).

If defer: record the disposition in a comment in the audit branch and note in audit report.

---

### Task 3: Agree feature-session cutoff with user

- [ ] **Step 3.1: Enumerate active sessions touching SHOW-scope**

Run: `git -C /Users/gclyle/GrowDirect/Canary log --since="24 hours ago" --oneline` and same for GrowDirect.

Expected: list of recent commits. Identify which branches are actively being worked.

- [ ] **Step 3.2: Present cutoff options to user**

Offer three choices:
- **Freeze SHOW-scope changes between Phase 2 audit and Phase 4 cleanup** — simplest, requires user to pause other sessions for ~45 min.
- **Cleanup subagent re-runs audit on its worktree branch** — handles concurrent changes, slightly more work per subagent.
- **Hybrid — freeze for Phase 2 only, cleanup re-checks in Phase 4** — balanced.

Record the chosen cutoff in the plan execution log.

---

### Task 4: Install security tooling

**Files:** no source changes; tools installed into shell environment.

- [ ] **Step 4.1: Install Python-tool dependencies via pipx or uv tool**

Run (choose one based on availability from Step 1.3):

```bash
pipx install pip-audit && pipx install bandit && pipx install semgrep
# OR, if using uv:
uv tool install pip-audit && uv tool install bandit && uv tool install semgrep
```

Verify: `pip-audit --version && bandit --version && semgrep --version`
Expected: all three report versions.

Also install `ripgrep` for grep operations throughout: `which rg || brew install ripgrep`

- [ ] **Step 4.2: Install gitleaks via brew**

Run: `brew install gitleaks`
Verify: `gitleaks version`
Expected: version string.

- [ ] **Step 4.3: Install trufflehog via brew**

Run: `brew install trufflehog`
Verify: `trufflehog --version`
Expected: version string.

- [ ] **Step 4.4: Install trivy via brew**

Run: `brew install trivy`
Verify: `trivy --version`
Expected: version string.

- [ ] **Step 4.5: Confirm no app dependencies were touched**

Run: `git -C /Users/gclyle/GrowDirect diff requirements.txt && git -C /Users/gclyle/GrowDirect/Canary diff requirements.txt`
Expected: no output (no changes). If anything shows, revert — these tools must NOT be in app deps per memory `feedback_flag_dependency_changes.md`.

---

### Task 5: Create Brain MVP split branches

**Files:**
- Create branches: `chore/brain-mvp-split-2026-04-23` on both GrowDirect and Canary repos
- Worktrees: `/Users/gclyle/GrowDirect/.worktrees/growdirect-brain-split/` and `/Users/gclyle/GrowDirect/.worktrees/canary-brain-split/`

- [ ] **Step 5.1: Create GrowDirect worktree for Brain split from main**

Run: `git -C /Users/gclyle/GrowDirect worktree add -b chore/brain-mvp-split-2026-04-23 .worktrees/growdirect-brain-split main`

Verify: `ls /Users/gclyle/GrowDirect/.worktrees/growdirect-brain-split/Brain/projects/Canary.md`
Expected: file exists (we're on a main-derived branch with full Brain content).

- [ ] **Step 5.2: Create Canary worktree for Brain split**

Run: `git -C /Users/gclyle/GrowDirect/Canary worktree add -b chore/brain-mvp-split-2026-04-23 ../.worktrees/canary-brain-split main`

Verify: `ls /Users/gclyle/GrowDirect/.worktrees/canary-brain-split/canary/__init__.py`
Expected: file exists.

---

### Task 6: Execute Brain MVP split moves — GrowDirect side (removals)

**Files to remove from GrowDirect (moved to Canary):**
- `Brain/projects/Canary.md`
- `Brain/wiki/canary-architecture.md`
- `Brain/wiki/canary-data-model.md`
- `Brain/wiki/canary-detection.md`
- `Brain/wiki/canary-platform-overview.md`
- `Brain/wiki/growdirect-canary.md`
- `Brain/wiki/growdirect-the-chirp.md`
- `Brain/wiki/growdirect-the-fox.md`
- `Brain/wiki/growdirect-chirp-udq-strategy.md`
- `docs/sdds/canary/` (entire directory, 21 files)
- `docs/superpowers/specs/2026-04-14-canary-growdirect-io-design.md`
- `docs/superpowers/specs/2026-04-15-canary-account-credit-system-design.md`
- `docs/superpowers/plans/2026-04-14-canary-growdirect-io.md`
- `docs/superpowers/plans/2026-04-15-canary-account-credit-system.md`
- `docs/superpowers/dispatches/2026-04-22-demo-reseed.md` (if exists; already moved in earlier hygiene commit)

Note: `Brain/wiki/growdirect-chirp-udq-strategy.md` should be skimmed before moving — if it contains commercial/sales strategy content, keep in GrowDirect HIDE scope instead.

- [ ] **Step 6.1: Skim `growdirect-chirp-udq-strategy.md` for commercial content**

Run: `grep -iE "pricing|revenue|gtm|upsell|closes|tier|sales motion" /Users/gclyle/GrowDirect/.worktrees/growdirect-brain-split/Brain/wiki/growdirect-chirp-udq-strategy.md | head -10`

If hits found: surface to user. Decide per-file whether product-focused (move) or commercial (keep in GrowDirect HIDE). Record decision.

- [ ] **Step 6.2: Copy Canary-scoped files into a staging area (for later move to Canary)**

Using a staging directory inside the worktree so we can `git rm` from GrowDirect and `git add` into Canary as two separate repo operations:

```bash
mkdir -p /tmp/brain-mvp-staging-2026-04-23/brain/projects /tmp/brain-mvp-staging-2026-04-23/brain/wiki /tmp/brain-mvp-staging-2026-04-23/docs/sdds /tmp/brain-mvp-staging-2026-04-23/docs/superpowers/specs /tmp/brain-mvp-staging-2026-04-23/docs/superpowers/plans /tmp/brain-mvp-staging-2026-04-23/docs/superpowers/dispatches
cd /Users/gclyle/GrowDirect/.worktrees/growdirect-brain-split/
cp Brain/projects/Canary.md /tmp/brain-mvp-staging-2026-04-23/brain/projects/
cp Brain/wiki/canary-architecture.md Brain/wiki/canary-data-model.md Brain/wiki/canary-detection.md Brain/wiki/canary-platform-overview.md Brain/wiki/growdirect-canary.md Brain/wiki/growdirect-the-chirp.md Brain/wiki/growdirect-the-fox.md /tmp/brain-mvp-staging-2026-04-23/brain/wiki/
# chirp-udq-strategy: copy only if Step 6.1 kept it in-scope
cp Brain/wiki/growdirect-chirp-udq-strategy.md /tmp/brain-mvp-staging-2026-04-23/brain/wiki/  # conditional
cp -r docs/sdds/canary/ /tmp/brain-mvp-staging-2026-04-23/docs/sdds/
cp docs/superpowers/specs/2026-04-14-canary-growdirect-io-design.md docs/superpowers/specs/2026-04-15-canary-account-credit-system-design.md /tmp/brain-mvp-staging-2026-04-23/docs/superpowers/specs/
cp docs/superpowers/plans/2026-04-14-canary-growdirect-io.md docs/superpowers/plans/2026-04-15-canary-account-credit-system.md /tmp/brain-mvp-staging-2026-04-23/docs/superpowers/plans/
[ -f docs/superpowers/dispatches/2026-04-22-demo-reseed.md ] && cp docs/superpowers/dispatches/2026-04-22-demo-reseed.md /tmp/brain-mvp-staging-2026-04-23/docs/superpowers/dispatches/
ls -la /tmp/brain-mvp-staging-2026-04-23/
```

Verify: staging dir contains all Canary-scoped files.

- [ ] **Step 6.3: git rm moved files from GrowDirect worktree**

```bash
cd /Users/gclyle/GrowDirect/.worktrees/growdirect-brain-split/
git rm Brain/projects/Canary.md
git rm Brain/wiki/canary-architecture.md Brain/wiki/canary-data-model.md Brain/wiki/canary-detection.md Brain/wiki/canary-platform-overview.md Brain/wiki/growdirect-canary.md Brain/wiki/growdirect-the-chirp.md Brain/wiki/growdirect-the-fox.md
# chirp-udq conditional on Step 6.1
git rm Brain/wiki/growdirect-chirp-udq-strategy.md  # conditional
git rm -r docs/sdds/canary/
git rm docs/superpowers/specs/2026-04-14-canary-growdirect-io-design.md docs/superpowers/specs/2026-04-15-canary-account-credit-system-design.md
git rm docs/superpowers/plans/2026-04-14-canary-growdirect-io.md docs/superpowers/plans/2026-04-15-canary-account-credit-system.md
[ -f docs/superpowers/dispatches/2026-04-22-demo-reseed.md ] && git rm docs/superpowers/dispatches/2026-04-22-demo-reseed.md
git status --short | head -30
```

Expected: all staged as deletions.

- [ ] **Step 6.4: Update Brain/projects/Method.md and Brain/projects/GrowDirect.md to remove broken wikilinks**

Run Obsidian link-check:

```bash
# Find files in GrowDirect that link to moved content
grep -rl "\[\[Brain/projects/Canary\|\[\[Brain/wiki/canary-\|\[\[Brain/wiki/growdirect-canary\|\[\[Brain/wiki/growdirect-the-chirp\|\[\[Brain/wiki/growdirect-the-fox\|\[\[docs/sdds/canary" /Users/gclyle/GrowDirect/.worktrees/growdirect-brain-split/Brain/
```

For each hit: either remove the link, replace with explicit cross-repo path like `Canary/brain/wiki/canary-architecture.md`, or add a pointer note "moved to Canary repo."

Conservative default: remove the wikilink (can't resolve in GrowDirect view anyway).

- [ ] **Step 6.5: Commit GrowDirect removals**

```bash
cd /Users/gclyle/GrowDirect/.worktrees/growdirect-brain-split/
git add Brain/ docs/
git status --short
```

Verify only Brain/ and docs/ changes staged. Commit:

```bash
git commit -m "$(cat <<'EOF'
chore: Brain MVP split — remove Canary-scoped content (moved to Canary repo)

Part of CTO-readiness audit per design spec
docs/superpowers/specs/2026-04-23-cto-readiness-audit-design.md.

Removes Canary-scoped Brain and docs content from the GrowDirect
monorepo. Corresponding content is added to the Canary repo in a
paired commit on chore/brain-mvp-split-2026-04-23.

Files removed:
- Brain/projects/Canary.md
- Brain/wiki/canary-*.md (4 files)
- Brain/wiki/growdirect-{canary,the-chirp,the-fox}.md
- docs/sdds/canary/ (21 files)
- docs/superpowers/specs/*canary*.md (2 files)
- docs/superpowers/plans/*canary*.md (2 files)

Cross-vault wikilinks in remaining GrowDirect Brain content updated
to either remove links to moved content or note the new home.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 7: Execute Brain MVP split moves — Canary side (additions)

**Files created in Canary:**
- `brain/projects/Canary.md`
- `brain/wiki/` — 7–8 wiki files
- `docs/sdds/` — 21 SDD files (moved from `docs/sdds/canary/` in GrowDirect, now at `Canary/docs/sdds/` without the `canary/` subdir since everything in this repo IS Canary)
- `docs/superpowers/specs/` — 2 files
- `docs/superpowers/plans/` — 2 files
- `docs/superpowers/dispatches/2026-04-22-demo-reseed.md` — 1 file (conditional)

- [ ] **Step 7.1: Copy from staging into Canary worktree**

```bash
cd /Users/gclyle/GrowDirect/.worktrees/canary-brain-split/
mkdir -p brain/projects brain/wiki docs/sdds docs/superpowers/specs docs/superpowers/plans docs/superpowers/dispatches
cp /tmp/brain-mvp-staging-2026-04-23/brain/projects/Canary.md brain/projects/
cp /tmp/brain-mvp-staging-2026-04-23/brain/wiki/*.md brain/wiki/
cp -r /tmp/brain-mvp-staging-2026-04-23/docs/sdds/canary/* docs/sdds/
cp /tmp/brain-mvp-staging-2026-04-23/docs/superpowers/specs/*.md docs/superpowers/specs/
cp /tmp/brain-mvp-staging-2026-04-23/docs/superpowers/plans/*.md docs/superpowers/plans/
[ -f /tmp/brain-mvp-staging-2026-04-23/docs/superpowers/dispatches/2026-04-22-demo-reseed.md ] && cp /tmp/brain-mvp-staging-2026-04-23/docs/superpowers/dispatches/2026-04-22-demo-reseed.md docs/superpowers/dispatches/
git status --short | head -30
```

Expected: all listed as untracked (new files).

- [ ] **Step 7.2: Initialize Canary's brain as an Obsidian vault**

Create `brain/.obsidian/` with minimal config so Obsidian treats this as its own vault:

```bash
cd /Users/gclyle/GrowDirect/.worktrees/canary-brain-split/brain/
mkdir -p .obsidian
cat > .obsidian/app.json <<'EOF'
{
  "promptDelete": false,
  "alwaysUpdateLinks": true
}
EOF
cat > .gitignore <<'EOF'
.obsidian/workspace.json
.obsidian/graph.json
EOF
```

- [ ] **Step 7.3: Run link hygiene pass on Canary's new brain**

```bash
cd /Users/gclyle/GrowDirect/.worktrees/canary-brain-split/brain/
# Find wikilinks that reference GrowDirect-only paths
grep -rlE "\[\[Brain/method/|\[\[Brain/projects/Method|\[\[Brain/wiki/growdirect-factory-process|\[\[docs/sdds/platform" .
```

For each hit: either (a) replace wikilink with explicit markdown link citing `GrowDirect/Brain/...` path (works when both vaults accessible via founder view-shell) or (b) remove the link and add prose context.

- [ ] **Step 7.4: Add confidentiality frontmatter to moved Brain files**

For every `.md` in `Canary/brain/` that lacks `classification: confidential` + `owner: GrowDirect LLC`, add it. Per the spec's Standards section.

Use a Python one-liner or manual edits. Sample script:

```python
import os, re, pathlib
for p in pathlib.Path('/Users/gclyle/GrowDirect/.worktrees/canary-brain-split/brain').rglob('*.md'):
    content = p.read_text()
    if 'classification: confidential' in content: continue
    if content.startswith('---'):
        # Has frontmatter — inject fields
        fm_end = content.index('---', 3)
        fm = content[3:fm_end]
        new_fm = fm
        if 'classification:' not in fm: new_fm += 'classification: confidential\n'
        if 'owner:' not in fm: new_fm += 'owner: GrowDirect LLC\n'
        content = '---' + new_fm + content[fm_end:]
    else:
        # No frontmatter — add it
        content = '---\nclassification: confidential\nowner: GrowDirect LLC\n---\n\n' + content
    p.write_text(content)
    print(f"Updated {p}")
```

Run and verify output.

- [ ] **Step 7.5: Commit Canary additions**

```bash
cd /Users/gclyle/GrowDirect/.worktrees/canary-brain-split/
git add brain/ docs/
git status --short | head -30
# Verify ONLY intended files are staged
git commit -m "$(cat <<'EOF'
chore: Brain MVP split — add Canary-scoped content (moved from GrowDirect)

Part of CTO-readiness audit per design spec
docs/superpowers/specs/2026-04-23-cto-readiness-audit-design.md
in the GrowDirect repo.

Adds Canary-scoped Brain and docs content moved from the GrowDirect
monorepo. Corresponding removals are on chore/brain-mvp-split-2026-04-23
in the GrowDirect repo.

Files added:
- brain/projects/Canary.md
- brain/wiki/{canary-architecture,canary-data-model,canary-detection,canary-platform-overview,growdirect-canary,growdirect-the-chirp,growdirect-the-fox}.md
- brain/.obsidian/ (minimal Obsidian vault init)
- docs/sdds/ (21 SDD files, moved from docs/sdds/canary/ in GrowDirect)
- docs/superpowers/specs/2026-04-*canary*.md (2 files)
- docs/superpowers/plans/2026-04-*canary*.md (2 files)
- docs/superpowers/dispatches/2026-04-22-demo-reseed.md (conditional)

All moved Markdown files carry classification: confidential and
owner: GrowDirect LLC frontmatter.

Cross-vault wikilinks resolved: broken links either removed or
replaced with explicit GrowDirect/ paths for founder view-shell.

Note: file history starts fresh in Canary; provenance remains
queryable in GrowDirect. Subtree-split to preserve full history
is deferred per spec Open Question 2.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 8: User reviews Brain-split branches

**Gate.** No automated action.

- [ ] **Step 8.1: Present both branches to user**

Report:
- GrowDirect branch: `chore/brain-mvp-split-2026-04-23`, N files deleted/renamed
- Canary branch: `chore/brain-mvp-split-2026-04-23`, N files added
- Any wikilinks that were removed vs rewritten
- Any open judgment calls (e.g., chirp-udq-strategy decision)

- [ ] **Step 8.2: User reviews and approves merges**

Wait for user approval. Do NOT merge without explicit approval.

- [ ] **Step 8.3: Merge to main on both repos (after approval)**

```bash
# GrowDirect
git -C /Users/gclyle/GrowDirect checkout main
git -C /Users/gclyle/GrowDirect merge --no-ff chore/brain-mvp-split-2026-04-23 -m "merge: Brain MVP split — GrowDirect side (Canary content moved to Canary repo)"

# Canary
git -C /Users/gclyle/GrowDirect/Canary checkout main
git -C /Users/gclyle/GrowDirect/Canary merge --no-ff chore/brain-mvp-split-2026-04-23 -m "merge: Brain MVP split — Canary side (content moved from GrowDirect)"
```

Verify on both: `git log --oneline -3` shows the merge commits.

**Checkpoint:** Brain MVP split is merged. The repo structure now matches what Phase 2 audit will see.

---

## Chunk 2 — Phase 2 Audit Dispatch

Phase 2 fires FOUR parallel subagents, then ONE serial subagent. The four parallel scopes (canary, platform, docs-brain, security) are read-only. The serial fifth (enterprise-scale-gap) runs after the other four complete because it consumes their output. The audit prompt is a separate dispatchable file: `docs/superpowers/dispatches/2026-04-23-cto-readiness-audit.md`.

### Task 9: Verify audit dispatch prompt file exists

**File:** `/Users/gclyle/GrowDirect/.worktrees/cto-spec/docs/superpowers/dispatches/2026-04-23-cto-readiness-audit.md`

The prompt was authored alongside this plan. Verify it exists and is committed to `chore/cto-readiness-spec-2026-04-23`.

- [ ] **Step 9.1: Verify file exists**

Run: `ls -la /Users/gclyle/GrowDirect/.worktrees/cto-spec/docs/superpowers/dispatches/2026-04-23-cto-readiness-audit.md`

Expected: file present, several hundred lines.

- [ ] **Step 9.2: Verify committed**

Run: `git -C /Users/gclyle/GrowDirect/.worktrees/cto-spec log --oneline -5 -- docs/superpowers/dispatches/2026-04-23-cto-readiness-audit.md`

Expected: at least one commit. If missing, the prompt file needs committing — see Task 12's commit step.

---

### Task 10: Fire four parallel audit subagents, then one serial

**Preconditions:** Phase 0 + Phase 1 merged to main on both repos. Tooling from Task 4 installed. An `audit/cto-readiness-2026-04-23` branch has been created on both repos — subagents check this branch out in their working directory so their report writes land on the audit branch (not main).

Setup:
```bash
git -C /Users/gclyle/GrowDirect checkout -b audit/cto-readiness-2026-04-23
git -C /Users/gclyle/GrowDirect/Canary checkout -b audit/cto-readiness-2026-04-23
```

Fire the first four in a single message with multiple `Agent()` tool calls so they run concurrently. After they return, fire the fifth (`enterprise-scale-gap`) serially since it consumes their output.

- [ ] **Step 10.1: Dispatch `canary-audit`**

Subagent type: `general-purpose`
Prompt: reference the audit dispatch file at `docs/superpowers/dispatches/2026-04-23-cto-readiness-audit.md` with scope variable set to "canary"

The subagent:
- Reads every file in `Canary/` repo (post-split) except `node_modules`, `.venv`, `__pycache__`, `.git`, `.worktrees`
- Runs all audit dimensions from the spec against each file
- Produces: `Canary/docs/audit-2026-04-23/canary.md`

Expected duration: 15–30 min.

- [ ] **Step 10.2: Dispatch `platform-audit`**

Subagent type: `general-purpose`
Scope: `GrowDirect/devops/`, `GrowDirect/services/`, `GrowDirect/content-engine/`, `GrowDirect/growdirect-platform.plugin/`
Produces: `GrowDirect/docs/audit-2026-04-23/platform.md`

- [ ] **Step 10.3: Dispatch `docs-brain-audit`**

Subagent type: `general-purpose`
Scope: both repos' SHOW-scope docs and Brain (post-split structure)
Produces: `Canary/docs/audit-2026-04-23/docs-brain.md` AND `GrowDirect/docs/audit-2026-04-23/docs-brain.md`

- [ ] **Step 10.4: Dispatch `security-audit`**

Subagent type: `general-purpose`
Scope: both repos' full git history + current source tree
Tools: `pip-audit`, `bandit`, `semgrep`, `gitleaks`, `trufflehog`, `trivy`
Produces: `Canary/docs/audit-2026-04-23/security.md` + `Canary/docs/audit-2026-04-23/security-tool-output/` and same for GrowDirect.

- [ ] **Step 10.5: Dispatch `enterprise-scale-gap` (SERIAL, after 10.1–10.4 complete)**

Subagent type: `general-purpose`
This step runs AFTER steps 10.1–10.4 all return. NOT in the parallel batch.
Reads: each audit report + `Brain/wiki/secure-client-kroger.md` + `Brain/wiki/secure-architecture.md` (source material for enterprise bar, but DO NOT name these sources in the output)
Produces: `GrowDirect/docs/audit-2026-04-23/enterprise-scale-gap-analysis.md`

Must follow writing rules: generic phrasing of the enterprise bar, no prior-client names, honest gap vs choice distinction.

- [ ] **Step 10.6: Verify all audit reports exist**

```bash
find /Users/gclyle/GrowDirect/Canary/docs/audit-2026-04-23/ -type f 2>&1 | head -10
find /Users/gclyle/GrowDirect/docs/audit-2026-04-23/ -type f 2>&1 | head -10
```

Expected: at minimum `canary.md`, `docs-brain.md`, `security.md`, `security-tool-output/*.json`, and on GrowDirect side also `platform.md`, `enterprise-scale-gap-analysis.md`.

- [ ] **Step 10.7: Commit audit reports**

```bash
cd /Users/gclyle/GrowDirect/Canary/
git checkout -b audit/cto-readiness-2026-04-23
git add docs/audit-2026-04-23/
git commit -m "audit: CTO-readiness audit reports 2026-04-23 (Phase 2 output)"

cd /Users/gclyle/GrowDirect/
git checkout -b audit/cto-readiness-2026-04-23
git add docs/audit-2026-04-23/
git commit -m "audit: CTO-readiness audit reports 2026-04-23 (Phase 2 output)"
```

Audit reports are committed on dedicated branches — not merged yet. They stay visible for user review and as historical record. Merge into main happens in Phase 5 alongside cleanup.

---

### Task 11: User reviews audit reports (Phase 3 gate)

**Gate.** No automated action.

- [ ] **Step 11.1: Surface report locations to user**

Report file paths:
- Canary: `Canary/docs/audit-2026-04-23/canary.md`, `docs-brain.md`, `security.md`
- GrowDirect: `GrowDirect/docs/audit-2026-04-23/platform.md`, `docs-brain.md`, `security.md`, `enterprise-scale-gap-analysis.md`

- [ ] **Step 11.2: Summarize findings by severity**

Produce a one-page summary: total counts per severity (CRITICAL / HIGH / MEDIUM / LOW), top 10 most important findings, any committed-secret findings (which trigger the history-rewrite workstream).

- [ ] **Step 11.3: Wait for user decisions**

User decides:
- Approve cleanup scope (all findings get cleaned, OR a subset)
- Judgment calls on thoughtful-stub candidates (which sloppy-looking stubs should become thoughtful stubs vs be removed)
- Kroger-gap framing (accept as written, or adjust per-dimension)
- Committed-secret disposition (if any: confirm rotate + history rewrite needed, OR confirm finding is benign)

Record decisions in `docs/audit-2026-04-23/user-decisions.md` on each repo before proceeding to Phase 4.

- [ ] **Step 11.4: Merge `audit/cto-readiness-2026-04-23` into main (after approval)**

Cleanup subagents in Phase 4 need to READ the audit reports. Cleanup worktrees cut from main — so audit reports must be on main before cleanup worktrees are created.

```bash
git -C /Users/gclyle/GrowDirect/Canary checkout main
git -C /Users/gclyle/GrowDirect/Canary merge --no-ff audit/cto-readiness-2026-04-23 -m "merge: CTO-readiness audit reports (Phase 2 output)"

git -C /Users/gclyle/GrowDirect checkout main
git -C /Users/gclyle/GrowDirect merge --no-ff audit/cto-readiness-2026-04-23 -m "merge: CTO-readiness audit reports (Phase 2 output)"
```

Verify: `git -C /Users/gclyle/GrowDirect/Canary log main --oneline -3` shows the merge.

If committed-secret findings require history rewrite, that workstream (Task 16) runs AFTER this merge and BEFORE cleanup worktrees are created (Task 13).

---

## Chunk 3 — Phase 4 Cleanup Dispatch

Phase 4 dispatches cleanup subagents into worktrees. Each subagent reads audit findings and applies conservative-philosophy cleanup. The cleanup prompt is a separate dispatchable file: `docs/superpowers/dispatches/2026-04-23-cto-readiness-cleanup.md`.

### Task 12: Verify cleanup dispatch prompt file exists + commit spec/plan/dispatches

**File:** `/Users/gclyle/GrowDirect/.worktrees/cto-spec/docs/superpowers/dispatches/2026-04-23-cto-readiness-cleanup.md`

- [ ] **Step 12.1: Verify cleanup dispatch file exists**

Run: `ls -la /Users/gclyle/GrowDirect/.worktrees/cto-spec/docs/superpowers/dispatches/2026-04-23-cto-readiness-cleanup.md`
Expected: file present.

- [ ] **Step 12.2: Commit plan + dispatch prompts**

From the `cto-spec` worktree, commit the plan + both dispatch prompt files if not already committed:

```bash
cd /Users/gclyle/GrowDirect/.worktrees/cto-spec/
git add docs/superpowers/plans/2026-04-23-cto-readiness-audit.md docs/superpowers/dispatches/2026-04-23-cto-readiness-audit.md docs/superpowers/dispatches/2026-04-23-cto-readiness-cleanup.md
git status --short
git commit -m "chore: add CTO-readiness implementation plan + audit/cleanup dispatch prompts"
```

---

### Task 13: Create cleanup worktrees

- [ ] **Step 13.1: Canary cleanup worktree**

```bash
git -C /Users/gclyle/GrowDirect/Canary worktree add -b chore/cto-readiness-audit-2026-04-23 ../.worktrees/canary-cto-cleanup main
```

Verify: `ls /Users/gclyle/GrowDirect/.worktrees/canary-cto-cleanup/` shows full Canary tree.

- [ ] **Step 13.2: GrowDirect cleanup worktree**

```bash
git -C /Users/gclyle/GrowDirect worktree add -b chore/cto-readiness-audit-2026-04-23 .worktrees/growdirect-cto-cleanup main
```

Verify: `ls /Users/gclyle/GrowDirect/.worktrees/growdirect-cto-cleanup/` shows full GrowDirect tree.

- [ ] **Step 13.3: Security-fix branches (separate from main cleanup)**

```bash
git -C /Users/gclyle/GrowDirect/Canary worktree add -b chore/security-findings-2026-04-23 ../.worktrees/canary-security-fix main
git -C /Users/gclyle/GrowDirect worktree add -b chore/security-findings-2026-04-23 .worktrees/growdirect-security-fix main
```

---

### Task 14: Fire cleanup subagents

Cleanup subagents operate inside their respective worktrees. Fire in parallel via multiple Agent() calls in one message.

- [ ] **Step 14.1: Dispatch `canary-cleanup`**

Reference `docs/superpowers/dispatches/2026-04-23-cto-readiness-cleanup.md` with:
- `SCOPE`: canary
- `WORKTREE`: `/Users/gclyle/GrowDirect/.worktrees/canary-cto-cleanup/`
- `AUDIT_REPORT`: `Canary/docs/audit-2026-04-23/canary.md` + `docs-brain.md`
- `BRANCH`: `chore/cto-readiness-audit-2026-04-23`

Produces: branch with fixes + `cleanup-report.md` in worktree.

- [ ] **Step 14.2: Dispatch `platform-cleanup`**

Scope: GrowDirect platform directories (`devops/`, `services/`, `content-engine/`, `growdirect-platform.plugin/`) + SHOW-scope docs + Platform-supporting Brain.
Worktree: `/Users/gclyle/GrowDirect/.worktrees/growdirect-cto-cleanup/`
Audit reports: `GrowDirect/docs/audit-2026-04-23/platform.md` + `docs-brain.md`

- [ ] **Step 14.3: Dispatch `canary-security-fix` and `growdirect-security-fix`**

Parallel to 14.1/14.2 but targeting `chore/security-findings-2026-04-23` branches. Scope: only HIGH/CRITICAL security findings from the security audit report.

If any CRITICAL committed-secret findings exist: the subagent MUST NOT try to fix them — it flags them for the history-rewrite workstream (Task 16) and the user handles rotation externally.

- [ ] **Step 14.4: Pre-report audit re-scan (per spec Phase 4 requirement)**

Each cleanup subagent, before producing its cleanup report, re-runs the audit-dimension check on its own worktree branch and diffs against the Phase 2 baseline. Any new findings introduced by concurrent feature-session landings get folded into the cleanup or flagged as out-of-scope.

- [ ] **Step 14.5: Verify cleanup branches produced**

```bash
git -C /Users/gclyle/GrowDirect/.worktrees/canary-cto-cleanup log --oneline -5
git -C /Users/gclyle/GrowDirect/.worktrees/growdirect-cto-cleanup log --oneline -5
git -C /Users/gclyle/GrowDirect/.worktrees/canary-security-fix log --oneline -5
git -C /Users/gclyle/GrowDirect/.worktrees/growdirect-security-fix log --oneline -5
```

Expected: each worktree has commits on its branch. Each worktree has a `cleanup-report.md` or `security-fix-report.md` in a location determined by the subagent.

- [ ] **Step 14.6: Verify standards applied (confidentiality markings + repo-root files)**

The cleanup dispatch prompt includes this as its Section 3 work. This step is a verification check after the cleanup subagents return.

For each SHOW-scope repo, confirm:
- Two-line GrowDirect LLC header present on every source file (spot-check 10 files)
- Every `.md` frontmatter has `classification: confidential` + `owner: GrowDirect LLC`
- `NOTICE.md`, `ACKNOWLEDGMENT.md`, `SECURITY.md`, `CONTRIBUTING.md` exist at repo root
- `docs/standards/confidentiality-markings.md` exists in GrowDirect

If any check fails, flag back to the cleanup subagent for a targeted fix pass.

---

### Task 15: User reviews cleanup branches (Phase 5 gate)

**Gate.** No automated action.

- [ ] **Step 15.1: Surface branch state to user**

Report per worktree:
- Files changed (count, list top 20 by change-size)
- Cleanup report summary
- Judgment calls flagged for user decision

- [ ] **Step 15.2: Execute user decisions on judgment calls**

User picks per judgment call: accept as-coded, edit, revert. Subagent executes in follow-up pass if edits are needed.

- [ ] **Step 15.3: Merge cleanup branches to main (after approval)**

Audit reports were already merged to main in Step 11.4. Cleanup branches merge now in order:

1. `chore/cto-readiness-audit-2026-04-23` (main cleanup)
2. `chore/security-findings-2026-04-23` (security fixes)

```bash
# Canary
git -C /Users/gclyle/GrowDirect/Canary checkout main
git -C /Users/gclyle/GrowDirect/Canary merge --no-ff chore/cto-readiness-audit-2026-04-23 -m "merge: CTO-readiness audit cleanup"
git -C /Users/gclyle/GrowDirect/Canary merge --no-ff chore/security-findings-2026-04-23 -m "merge: security findings from CTO-readiness audit"

# GrowDirect
git -C /Users/gclyle/GrowDirect checkout main
git -C /Users/gclyle/GrowDirect merge --no-ff chore/cto-readiness-audit-2026-04-23 -m "merge: CTO-readiness audit cleanup"
git -C /Users/gclyle/GrowDirect merge --no-ff chore/security-findings-2026-04-23 -m "merge: security findings from CTO-readiness audit"
```

---

### Task 16: History rewrite (conditional — only if committed secret found)

**Trigger:** Task 10.4 security audit finds a committed secret in git history.
**Actor:** User executes rotation; subagent assists with BFG/git-filter-repo run.

- [ ] **Step 16.1: User rotates the secret externally**

User: regenerate API key / credential at the provider (Square, Anthropic, GitHub, etc.), confirm rotation complete.

- [ ] **Step 16.2: Identify all commits containing the secret**

Run: `git log --all -p -S "<partial_secret_pattern>" --oneline`

- [ ] **Step 16.3: Create a history-rewrite branch**

```bash
git -C /Users/gclyle/GrowDirect/<affected-repo> checkout -b chore/history-rewrite-2026-04-23
```

- [ ] **Step 16.4: Run BFG Repo-Cleaner or git-filter-repo**

```bash
# Option A: BFG
bfg --replace-text /tmp/secret-patterns.txt

# Option B: git-filter-repo
git filter-repo --replace-text /tmp/secret-patterns.txt
```

Verify: `git log --all -p -S "<partial_secret_pattern>"` returns empty.

- [ ] **Step 16.5: Force-push coordinate**

⚠️ Destructive — requires explicit user approval. Force-pushing rewrites remote history and breaks all existing clones.

Only proceed after user confirms:
- Secret is rotated (Step 16.1)
- No other clones exist that would silently lose history (ask the user)
- Ready to communicate history-rewrite to any collaborators

```bash
git push --force-with-lease origin main
```

- [ ] **Step 16.6: All team members re-clone the repo**

Document in PR/Slack/email that history was rewritten and old clones must be deleted and re-cloned.

---

## Chunk 4 — Phase 6 Dry-Run + Phase 7 Ready-to-Share

### Task 17: Dry-run cold-reader verification

**Gate:** Phase 5 cleanup merges complete. Main branches on both repos carry cleaned state.

- [ ] **Step 17.1: Dispatch `cold-reader-verification` subagent**

Subagent type: `general-purpose`
Prompt: "Simulate a cold CTO reader. You have never seen this codebase. Start at each SHOW'd repo's README.md. Navigate through architecture → code → tests. You are a skilled Python engineer with no prior context. Verify:
- `README.md`, `NOTICE.md`, `ACKNOWLEDGMENT.md`, `SECURITY.md`, `CONTRIBUTING.md` at root.
- No TODOs / FIXMEs / HACKs in code or docs.
- No AI-voice commentary (no `# Let me think`, celebratory emoji, apologetic tone).
- No client or personal names from prior engagements (search for: Kroger, Wal-Mart, Harrods, Staples, Appriss, Sysrepublic, Don Boyle, Drew Riegler, WPBCA, Abalone Cove, Cove, Angel, Seacove).
- Every source file has the GrowDirect LLC two-line header.
- Every `.md` has `classification: confidential` + `owner: GrowDirect LLC` frontmatter.
- Cross-doc links resolve (run Obsidian broken-link check or grep-based link resolution).
- Enterprise-scale gap analysis reads defensibly — specific, honest, separates gap from choice.

Produce one of:
- PASS — report any observations worth noting, say 'READY TO SHOW'
- FAIL — list every regression with file:line and severity"

Fire against both Canary and GrowDirect.

- [ ] **Step 17.2: Produce verification reports**

Subagent writes:
- `Canary/docs/audit-2026-04-23/ready-to-show-confirmation.md`
- `GrowDirect/docs/audit-2026-04-23/ready-to-show-confirmation.md`

- [ ] **Step 17.3: If FAIL, loop back to Task 14**

If verification finds regressions: fire cleanup subagents again on the specific findings. Re-run verification. Loop until PASS. If loop count > 3, surface to user — something structural is wrong.

---

### Task 18: Tag ready-to-share state

- [ ] **Step 18.1: Tag each repo**

```bash
git -C /Users/gclyle/GrowDirect/Canary tag -a cto-review-ready-2026-04-23 -m "CTO-readiness audit complete — first partner-access-ready state"
git -C /Users/gclyle/GrowDirect tag -a cto-review-ready-2026-04-23 -m "CTO-readiness audit complete — first partner-access-ready state"
```

- [ ] **Step 18.2: Push tags to origin**

```bash
git -C /Users/gclyle/GrowDirect/Canary push origin cto-review-ready-2026-04-23
git -C /Users/gclyle/GrowDirect push origin cto-review-ready-2026-04-23
```

---

### Task 19: Canary repo rename

- [ ] **Step 19.1: Execute GitHub rename**

```bash
gh repo rename canary --repo growdirectprez/growdirect-ops --yes
```

Expected: GitHub confirms rename. URL redirects configured automatically.

- [ ] **Step 19.2: Update local remote**

```bash
git -C /Users/gclyle/GrowDirect/Canary remote set-url origin git@github.com:growdirectprez/canary.git
git -C /Users/gclyle/GrowDirect/Canary remote -v
```

Verify: origin now points to `canary`, not `growdirect-ops`.

- [ ] **Step 19.3: Verify redirect works**

```bash
git -C /Users/gclyle/GrowDirect/Canary ls-remote origin 2>&1 | head -3
```

Expected: no errors; remote is reachable.

---

### Task 20: Infrastructure readiness

- [ ] **Step 20.1: Verify `contact@growdirect.io` receives mail**

User action: configure Fastmail to route `contact@growdirect.io` to user's primary inbox. Send a test email from an external address. Verify delivery.

- [ ] **Step 20.2: Verify `security@growdirect.io` receives mail**

Same as above for `security@growdirect.io`.

- [ ] **Step 20.3: Verify NOTICE / ACKNOWLEDGMENT / SECURITY files visible on GitHub**

Visit repo web UI; confirm the three files are present at repo root and render correctly.

---

### Task 21: Finalize repo-sharing matrix

- [ ] **Step 21.1: Update `GrowDirect/docs/repo-sharing-matrix.md` with post-rename names**

The file was created by the cleanup pass. Confirm it references `canary` (post-rename), not `growdirect-ops`. Add any new repos that need entries. Commit.

```bash
git -C /Users/gclyle/GrowDirect add docs/repo-sharing-matrix.md
git -C /Users/gclyle/GrowDirect commit -m "chore: finalize repo-sharing matrix post-rename"
```

---

### Task 22: Send access-grant email to CTO partner

- [ ] **Step 22.1: Draft email**

Template:

```
Subject: GrowDirect engineering access — please acknowledge

[Partner name] —

Per our conversation, I'd like to share the GrowDirect engineering
artifacts and Canary product under confidentiality so you can take a
real look.

Before I grant access, please read and agree to the attached/linked
access acknowledgment:

https://github.com/growdirectprez/canary/blob/main/ACKNOWLEDGMENT.md

Reply with "I acknowledge and agree" to this email if you accept the
terms. I'll then send you GitHub access to the repos we discussed.

If anything in the acknowledgment is unworkable on your end, let me
know what needs to change.

— Geoff
```

- [ ] **Step 22.2: Send email, wait for reply**

User action.

- [ ] **Step 22.3: On reply, grant GitHub access**

```bash
gh api --method PUT /repos/growdirectprez/canary/collaborators/<partner-github-handle> -f permission=read
# and for GrowDirect if they're accessing that repo too
gh api --method PUT /repos/growdirectprez/<growdirect-repo-name>/collaborators/<partner-github-handle> -f permission=read
```

Verify: partner receives GitHub invite notification.

- [ ] **Step 22.4: Record the access grant**

Update `GrowDirect/docs/repo-sharing-matrix.md` with: date, partner name (or opaque identifier), repo(s) granted, access level, acknowledgment thread reference.

---

### Task 23: Close-out

- [ ] **Step 23.0: Merge `chore/cto-readiness-spec-2026-04-23` to main**

The spec, plan, and dispatch prompts currently live on the `cto-spec` worktree's branch. Merge them to main now that the audit is complete (they're the historical record):

```bash
git -C /Users/gclyle/GrowDirect checkout main
git -C /Users/gclyle/GrowDirect merge --no-ff chore/cto-readiness-spec-2026-04-23 -m "merge: CTO-readiness audit spec, plan, and dispatch prompts"
```

- [ ] **Step 23.1: Delete cleanup worktrees**

Worktrees only needed during cleanup pass. After merges are in main:

```bash
git -C /Users/gclyle/GrowDirect/Canary worktree remove ../.worktrees/canary-cto-cleanup
git -C /Users/gclyle/GrowDirect/Canary worktree remove ../.worktrees/canary-security-fix
git -C /Users/gclyle/GrowDirect worktree remove .worktrees/growdirect-cto-cleanup
git -C /Users/gclyle/GrowDirect worktree remove .worktrees/growdirect-security-fix
git -C /Users/gclyle/GrowDirect/Canary worktree remove ../.worktrees/canary-brain-split
git -C /Users/gclyle/GrowDirect worktree remove .worktrees/growdirect-brain-split
```

Keep: `.worktrees/cto-spec/` (this worktree — the spec + plan lives here) until the `chore/cto-readiness-spec-2026-04-23` branch is also merged to main.

- [ ] **Step 23.2: Clean up stale Canary branches (per Git Triage item 5–6)**

Audit each `claude/*` branch and `gro-386-fix-canary-login-*` per the spec's Task 5–7 in the Git Triage table. Present disposition to user. Delete after approval.

- [ ] **Step 23.3: Final sanity check**

```bash
git -C /Users/gclyle/GrowDirect/Canary branch | head -20
git -C /Users/gclyle/GrowDirect branch | head -20
git -C /Users/gclyle/GrowDirect/Canary log --oneline -10
git -C /Users/gclyle/GrowDirect log --oneline -10
```

Expected: clean branch list, recent history shows the audit + cleanup + merge + tag sequence.

- [ ] **Step 23.4: Summary to user**

Report:
- Total findings found, total cleaned, any deferred
- Security scan summary (deps scanned, secrets found, dispositions)
- Repo state: branches, tags, current main commit
- Partner access grant status
- Open items for future sessions (per spec Open Questions 1–5)

---

## Chunk 5 — Dispatch Prompt Files (already written, verify)

Two dispatch prompts were authored alongside this plan as separate files:

- `/Users/gclyle/GrowDirect/.worktrees/cto-spec/docs/superpowers/dispatches/2026-04-23-cto-readiness-audit.md`
- `/Users/gclyle/GrowDirect/.worktrees/cto-spec/docs/superpowers/dispatches/2026-04-23-cto-readiness-cleanup.md`

Both are self-contained — a fresh Claude Code session pointed at either repo can paste the prompt and execute. Both live on branch `chore/cto-readiness-spec-2026-04-23` in the `.worktrees/cto-spec/` worktree.

Task 9 verifies the audit prompt; Task 12 verifies the cleanup prompt and commits the plan+dispatches together if not already committed.

---

## Post-Plan Notes

### Rollback strategy

If the audit reveals issues that make Phase 4 cleanup infeasible in one pass:
- Cleanup branches are preserved (never force-deleted)
- Ready-to-show tag is not placed
- Repo rename deferred
- Partner access not granted
- User decides: one more cleanup pass, or reschedule the meeting

### Success definition

The execution is successful when:
- All 11 spec success criteria are true
- All Phase 6 verification subagents return PASS
- User approves all merges
- Tag `cto-review-ready-2026-04-23` exists on both repos
- Partner has acknowledged and received access

### Branches this plan creates

| Repo | Branch | Purpose |
|---|---|---|
| GrowDirect | `chore/cto-readiness-spec-2026-04-23` | This spec + plan + dispatch prompts (already created) |
| GrowDirect | `chore/brain-mvp-split-2026-04-23` | Brain MVP split — removals (Phase 1) |
| Canary | `chore/brain-mvp-split-2026-04-23` | Brain MVP split — additions (Phase 1) |
| GrowDirect | `audit/cto-readiness-2026-04-23` | Audit reports (Phase 2 output) |
| Canary | `audit/cto-readiness-2026-04-23` | Audit reports (Phase 2 output) |
| GrowDirect | `chore/cto-readiness-audit-2026-04-23` | Main cleanup (Phase 4) |
| Canary | `chore/cto-readiness-audit-2026-04-23` | Main cleanup (Phase 4) |
| GrowDirect | `chore/security-findings-2026-04-23` | Security fixes (Phase 4) |
| Canary | `chore/security-findings-2026-04-23` | Security fixes (Phase 4) |
| GrowDirect | `chore/history-rewrite-2026-04-23` (conditional) | Only if committed secret found |

### Tags this plan creates

- `cto-review-ready-2026-04-23` on both repos — Phase 7

### Worktrees this plan creates

All worktrees live under `/Users/gclyle/GrowDirect/.worktrees/`:
- `cto-spec/` — spec + plan + dispatch prompts (this worktree, already exists)
- `growdirect-brain-split/` — Phase 1, deleted in Task 23
- `canary-brain-split/` — Phase 1, deleted in Task 23
- `canary-cto-cleanup/` — Phase 4, deleted in Task 23
- `growdirect-cto-cleanup/` — Phase 4, deleted in Task 23
- `canary-security-fix/` — Phase 4, deleted in Task 23
- `growdirect-security-fix/` — Phase 4, deleted in Task 23

### Memory references applied

- `feedback_git_health_check_first.md` — Task 1 pre-flight checks
- `feedback_flag_dependency_changes.md` — Task 4.5 no-app-deps check
- `feedback_no_loose_files.md` — dispatch-code file moves in earlier hygiene commit
- `feedback_full_sweep_no_deferrals.md` — no findings get punted to "later" without explicit deferral in Open Questions
- `feedback_know_the_whole_solution.md` — Task 1 verifies whole state before acting
- `feedback_no_hype_copy.md` — cleanup subagents enforce this on audit/cleanup reports

