# Factory Hardening — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Harden the factory process with a machine-readable manifest, preflight health checks, research stage, Linear integration skill, and flat skill directory — eliminating 3-level nesting and implicit pipeline discovery.

**Architecture:** `factory-manifest.json` at GrowDirect root declares the 9-stage pipeline. All 42 skills flattened into `~/GrowDirect/.claude/skills/` with app prefixes. Three new skills (preflight, linear, research) replace startup and standardize integrations. Old skill directories deleted.

**Tech Stack:** Markdown skills / JSON manifest / Bash health checks

**Spec:** `docs/superpowers/specs/2026-03-30-factory-hardening-design.md`

**GRO Issue:** GRO-376

---

## File Structure

| Action | File | Responsibility |
|--------|------|----------------|
| Create | `factory-manifest.json` | Pipeline declaration, stage contracts, app overrides |
| Create | `.claude/skills/factory-preflight.md` | Infra checks + context loading (replaces startup) |
| Create | `.claude/skills/factory-linear.md` | Standardized Linear integration at stage boundaries |
| Create | `.claude/skills/factory-research.md` | Prior art and context bundle before blueprint |
| Create | `.claude/skills/factory-newapp.md` | App scaffolding (from grow-newapp) |
| Create | `.claude/skills/file-guardian.md` | Protected file gate (from critical-file-guardian) |
| Create | `.claude/skills/gitnexus.md` | Consolidated code intelligence reference |
| Create | `.claude/skills/canary-preflight.md` | Canary override for preflight |
| Create | `.claude/skills/cove-preflight.md` | Cove override for preflight |
| Move | 10 Cove skills → `.claude/skills/cove-*.md` | Flatten from nested SKILL.md |
| Move | 14 Canary skills → `.claude/skills/canary-*.md` | Flatten from nested SKILL.md |
| Move | 7 platform skills → `.claude/skills/*.md` | Flatten from nested SKILL.md |
| Delete | `.claude/skills/factory-startup.md` | Replaced by preflight |
| Delete | `Cove/.claude/skills/` | All skills moved to root |
| Delete | `Canary/.claude/skills/` | All skills moved to root |
| Delete | `Cove/.worktrees/cove-parcel-contacts/.claude/skills/` | Stale worktree copies |
| Modify | `CLAUDE.md` | Update Factory Process to 9 stages |
| Create | `docs/skills/canary-deploy/` | Reference material for canary-deploy |

---

## Chunk 1: Manifest and New Skills

### Task 1: Create factory-manifest.json

**Files:**
- Create: `factory-manifest.json`

- [ ] **Step 1: Write manifest**

Create `~/GrowDirect/factory-manifest.json` with the exact JSON from the spec — 9-stage pipeline, stage contracts with inputs/outputs/required_mcps/optional_mcps, and app override declarations.

- [ ] **Step 2: Validate JSON**

```bash
python3 -c "import json; json.load(open('factory-manifest.json')); print('Valid JSON')"
```

Expected: `Valid JSON`

- [ ] **Step 3: Commit**

```bash
git add factory-manifest.json
git commit -m "feat: factory-manifest.json — machine-readable pipeline contract (GRO-376)"
```

---

### Task 2: Write factory-preflight.md

**Files:**
- Create: `.claude/skills/factory-preflight.md`

- [ ] **Step 1: Write the skill**

Content should include:
- YAML frontmatter: `name: factory-preflight`, description, allowed-tools (Bash, Read, Grep, Glob, TodoWrite, plus Linear MCP tools)
- Purpose: replaces factory-startup, runs before any factory stage
- Step 1: Read `factory-manifest.json` to get pipeline and stage contracts
- Step 2: Infrastructure checks with red/yellow/green reporting:
  - Docker: `docker ps --format "table {{.Names}}\t{{.Status}}" | grep growdirect`
  - PostgreSQL: `docker exec growdirect_postgres pg_isready`
  - Valkey: `docker exec growdirect_valkey valkey-cli ping`
  - Ollama: `curl -s http://localhost:11434/api/tags | python3 -c "import sys,json; print('OK' if json.load(sys.stdin) else 'EMPTY')"`
  - Git: `git status --porcelain`
  - Linear: use `get_issue` MCP tool to validate GRO issue exists
  - Memory bus (optional): `curl -s http://localhost:8003/health`
- Step 3: Red = stop and report. Yellow = warn and continue. Green = proceed.
- Step 4: Load context — read `CLAUDE.md`, read app `CLAUDE.md`, load GRO issue description from Linear
- Step 5: Query memory bus for prior art on GRO issue (if available, skip gracefully if not)
- Step 6: Identify app context for stage branching (from GRO issue project or working directory)
- Step 7: Report format: "Preflight: [GREEN/YELLOW/RED]. App: [canary/cove/platform]. Branch: [name]. Task: [GRO-XXX — title]."

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/factory-preflight.md
git commit -m "feat: factory-preflight skill — replaces startup with health checks (GRO-376)"
```

---

### Task 3: Write factory-linear.md

**Files:**
- Create: `.claude/skills/factory-linear.md`

- [ ] **Step 1: Write the skill**

Content:
- YAML frontmatter: `name: factory-linear`, description, allowed-tools (Linear MCP tools, Read, Bash)
- Purpose: standardize all Linear integration at stage boundaries
- Sections for each stage boundary:
  - **Preflight**: `get_issue` → validate exists, extract title/description/labels
  - **Blueprint**: `save_issue` → update status to "In Progress", `create_document` → attach plan as Linear document
  - **Ship**: `save_comment` → post verify/QA results, `save_issue` → move to "Done"
  - **Close**: `save_comment` → post session summary with completed items, pending items, new issues
- Error handling: if Linear MCP unreachable, log warning and continue (don't block the pipeline)

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/factory-linear.md
git commit -m "feat: factory-linear skill — standardized Linear integration (GRO-376)"
```

---

### Task 4: Write factory-research.md

**Files:**
- Create: `.claude/skills/factory-research.md`

- [ ] **Step 1: Write the skill**

Content:
- YAML frontmatter: `name: factory-research`, description, allowed-tools (memory bus MCP tools, Read, Grep, Glob, WebSearch, WebFetch, TodoWrite)
- Purpose: gather context before blueprint, output a context bundle
- Step 1: Query memory bus `memory_recall` with GRO issue title/description keywords
- Step 2: Query memory bus `context_assemble` for domain context if issue touches a known domain
- Step 3: (Optional, if GitNexus MCP available) Query for blast radius on files mentioned in GRO issue
- Step 4: (Optional, if Obsidian MCP available) Search for related architecture notes
- Step 5: (Optional, if Firecrawl MCP available) Crawl external API docs if GRO involves third-party APIs
- Step 6: Compile context bundle as markdown:
  ```
  ## Research Context for GRO-XXX
  ### Prior Decisions
  [memory_recall results]
  ### Domain Context
  [context_assemble results]
  ### Architecture Notes
  [Obsidian/GitNexus results if available]
  ```
- Step 7: If no sources available, output: "No prior context found. Blueprint starts from scratch."
- Graceful degradation: each source is independently optional

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/factory-research.md
git commit -m "feat: factory-research skill — prior art gathering before blueprint (GRO-376)"
```

---

## Chunk 2: Flatten Platform Skills

### Task 5: Flatten platform-generic skills from Canary

**Files:**
- Create from Canary sources: `file-guardian.md`, `gitnexus.md`, `jeffe-review.md`, `founder-probe.md`, `remember-quote.md`, `project-timelog.md`, `session-synthesis.md`, `rooster.md`

- [ ] **Step 1: Read each source skill**

Read the SKILL.md content from each Canary skill directory. For skills with double-nested paths (`founder-probe/founder-probe/SKILL.md`, etc.), read from the correct depth.

- [ ] **Step 2: Create flat .md files at GrowDirect root skills directory**

For each skill:
1. Read the source SKILL.md
2. Strip any Canary-specific path references and update to new flat location
3. Write to `~/GrowDirect/.claude/skills/{skill-name}.md`
4. If the skill has `references/` content that's essential, inline it. If it's large reference material, move to `docs/skills/{skill-name}/`.

Specific handling:
- `critical-file-guardian/SKILL.md` → `file-guardian.md` (rename, remove Canary-specific file list — make it generic with configurable protected files)
- `gitnexus/` (6 skills) → `gitnexus.md` (consolidate into single reference: setup instructions, tool list, usage patterns. Keep it as a reference for when GitNexus MCP is set up.)
- `jeffe-review/SKILL.md` → `jeffe-review.md` (no path changes needed)
- `founder-probe/founder-probe/SKILL.md` → `founder-probe.md` (flatten, inline essential assets)
- `remember-quote/remember-quote/SKILL.md` → `remember-quote.md` (flatten, inline)
- `project-timelog/SKILL.md` → `project-timelog.md` (update timelog path from Canary-specific to platform)
- `session-synthesis/session-synthesis/SKILL.md` → `session-synthesis.md` (flatten)
- `rooster/rooster/SKILL.md` → `rooster.md` (flatten, inline test patterns)

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/file-guardian.md .claude/skills/gitnexus.md \
       .claude/skills/jeffe-review.md .claude/skills/founder-probe.md \
       .claude/skills/remember-quote.md .claude/skills/project-timelog.md \
       .claude/skills/session-synthesis.md .claude/skills/rooster.md
git commit -m "feat: flatten platform-generic skills from Canary to root (GRO-376)"
```

---

### Task 6: Flatten factory-newapp from Cove

**Files:**
- Create: `.claude/skills/factory-newapp.md` from `Cove/.claude/skills/grow-newapp/SKILL.md`

- [ ] **Step 1: Read grow-newapp source**

```bash
cat ~/GrowDirect/Cove/.claude/skills/grow-newapp/SKILL.md
```

- [ ] **Step 2: Create factory-newapp.md**

Rename to `factory-newapp.md`, update any Cove-specific references to be platform-generic.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/factory-newapp.md
git commit -m "feat: flatten grow-newapp to factory-newapp at platform level (GRO-376)"
```

---

## Chunk 3: Flatten App-Specific Skills

### Task 7: Flatten Canary factory process skills

**Files:**
- Create: `canary-preflight.md`, `canary-blueprint.md`, `canary-tdd.md`, `canary-assembly.md`, `canary-verify.md`, `canary-qa.md`, `canary-ship.md`, `canary-close.md`

- [ ] **Step 1: Read each Canary factory skill**

Read SKILL.md from:
- `Canary/.claude/skills/canary-blueprint/SKILL.md`
- `Canary/.claude/skills/canary-tdd/SKILL.md`
- `Canary/.claude/skills/canary-assembly/SKILL.md`
- `Canary/.claude/skills/canary-verify/SKILL.md`
- `Canary/.claude/skills/canary-qa/SKILL.md`
- `Canary/.claude/skills/canary-ship/SKILL.md`
- `Canary/.claude/skills/alx-session-close/SKILL.md` (becomes canary-close)
- `Canary/.claude/skills/alx-startup/SKILL.md` (reference for canary-preflight)

- [ ] **Step 2: Create flat files**

For each skill:
1. Read source content
2. Update delegation line from `~/GrowDirect/.claude/skills/factory-startup.md` → `~/GrowDirect/.claude/skills/factory-preflight.md` (for startup references)
3. Write to `.claude/skills/{skill-name}.md`

For `canary-preflight.md` (new):
- Delegates to `factory-preflight.md`
- Adds Canary-specific checks: pipeline position identification, gLog impact assessment, six-node pipeline health
- Absorbs relevant content from `alx-startup`

For `canary-close.md` (renamed from alx-session-close):
- Delegates to `factory-close.md`
- Adds: memory bus session close, ALX-specific session summary format

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/canary-*.md
git commit -m "feat: flatten Canary factory process skills to root (GRO-376)"
```

---

### Task 8: Flatten Canary domain skills

**Files:**
- Create: `canary-data-expansion.md`, `canary-debug.md`, `canary-deploy.md`, `canary-review.md`, `canary-scenario.md`, `canary-uat.md`

- [ ] **Step 1: Read each Canary domain skill**

Read SKILL.md from:
- `Canary/.claude/skills/canary-data-expansion/SKILL.md`
- `Canary/.claude/skills/canary-debug/SKILL.md`
- `Canary/.claude/skills/canary-deploy/SKILL.md` + `references/environment.md`, `references/fallback-deploy.md`, `references/troubleshooting.md`
- `Canary/.claude/skills/canary-review/SKILL.md`
- `Canary/.claude/skills/canary-scenario/SKILL.md`
- `Canary/.claude/skills/canary-uat/canary-uat/SKILL.md`

- [ ] **Step 2: Create flat files**

For `canary-deploy.md`: inline essential reference content. Move large reference files (environment.md, fallback-deploy.md, troubleshooting.md) to `docs/skills/canary-deploy/`.

```bash
mkdir -p ~/GrowDirect/docs/skills/canary-deploy
```

For `canary-uat.md`: read from double-nested path `canary-uat/canary-uat/SKILL.md`, flatten to single `.md`. Inline essential assets.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/canary-data-expansion.md .claude/skills/canary-debug.md \
       .claude/skills/canary-deploy.md .claude/skills/canary-review.md \
       .claude/skills/canary-scenario.md .claude/skills/canary-uat.md
git add docs/skills/ 2>/dev/null
git commit -m "feat: flatten Canary domain skills to root (GRO-376)"
```

---

### Task 9: Flatten Cove skills

**Files:**
- Create: `cove-preflight.md`, `cove-blueprint.md`, `cove-tdd.md`, `cove-assembly.md`, `cove-verify.md`, `cove-qa.md`, `cove-ship.md`, `cove-close.md`, `cove-archive.md`

- [ ] **Step 1: Read each Cove skill**

Read SKILL.md from:
- `Cove/.claude/skills/cove-blueprint/SKILL.md`
- `Cove/.claude/skills/cove-tdd/SKILL.md`
- `Cove/.claude/skills/cove-assembly/SKILL.md`
- `Cove/.claude/skills/cove-verify/SKILL.md`
- `Cove/.claude/skills/cove-qa/SKILL.md`
- `Cove/.claude/skills/cove-ship/SKILL.md`
- `Cove/.claude/skills/cove-close/SKILL.md`
- `Cove/.claude/skills/cove-archive/SKILL.md`
- `Cove/.claude/skills/cove-startup/SKILL.md` (reference for cove-preflight)

- [ ] **Step 2: Create flat files**

For each: read source, write to `.claude/skills/cove-{stage}.md`.

For `cove-preflight.md` (new):
- Delegates to `factory-preflight.md`
- Adds Cove-specific checks: Davis-Stirling compliance context loaded, APN chain verification ready

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/cove-*.md
git commit -m "feat: flatten Cove skills to root (GRO-376)"
```

---

## Chunk 4: Cleanup and Verification

### Task 10: Delete old skill directories

**Files:**
- Delete: `Cove/.claude/skills/` (entire directory)
- Delete: `Canary/.claude/skills/` (entire directory)
- Delete: `Cove/.worktrees/cove-parcel-contacts/.claude/skills/` (stale copies)
- Delete: `.claude/skills/factory-startup.md`

- [ ] **Step 1: Verify .claude/settings.json preserved**

```bash
ls ~/GrowDirect/Cove/.claude/settings.json
ls ~/GrowDirect/Canary/.claude/settings.json
```

Expected: both exist. We're deleting `skills/` subdirectory only, not `.claude/`.

- [ ] **Step 2: Delete old directories**

```bash
rm -rf ~/GrowDirect/Cove/.claude/skills/
rm -rf ~/GrowDirect/Canary/.claude/skills/
rm -rf ~/GrowDirect/Cove/.worktrees/cove-parcel-contacts/.claude/skills/
rm ~/GrowDirect/.claude/skills/factory-startup.md
```

- [ ] **Step 3: Verify settings.json still exists**

```bash
ls ~/GrowDirect/Cove/.claude/settings.json
ls ~/GrowDirect/Canary/.claude/settings.json
```

Expected: both still present

- [ ] **Step 4: Commit**

```bash
git add -u
git commit -m "cleanup: delete old nested skill directories (GRO-376)"
```

---

### Task 11: Update CLAUDE.md

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Update Factory Process section**

Change from 6 stages to 9:

```markdown
## Factory Process

Nine stages, in order:

1. **Preflight** — Infrastructure checks, context loading, app identification (`factory-preflight` skill)
2. **Research** — Prior art from memory bus, GitNexus, Obsidian (`factory-research` skill)
3. **Blueprint** — Specify what you're building (`factory-blueprint` skill)
4. **TDD** — Write failing tests first (`factory-tdd` skill)
5. **Assembly** — Implement to make tests pass (`factory-assembly` skill)
6. **Verify** — Run full test suite, check integration (`factory-verify` skill)
7. **QA** — Quality assurance pass (`factory-qa` skill)
8. **Ship** — Deployment preparation (`factory-ship` skill)
9. **Close** — Session summary and post-mortem (`factory-close` skill)

Pipeline contract: `factory-manifest.json` at GrowDirect root.
```

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: update Factory Process to 9-stage pipeline (GRO-376)"
```

---

### Task 12: Verification

- [ ] **Step 1: Count skills in flat directory**

```bash
ls ~/GrowDirect/.claude/skills/*.md | wc -l
```

Expected: 42

- [ ] **Step 2: Verify manifest references exist**

```bash
python3 -c "
import json, os
manifest = json.load(open('factory-manifest.json'))
skills_dir = os.path.expanduser('~/GrowDirect/.claude/skills')
missing = []
for stage in manifest['pipeline']:
    path = os.path.join(skills_dir, f'factory-{stage}.md')
    if not os.path.exists(path):
        missing.append(f'factory-{stage}.md')
for app, info in manifest['apps'].items():
    for stage in info['overrides']:
        path = os.path.join(skills_dir, f'{app}-{stage}.md')
        if not os.path.exists(path):
            missing.append(f'{app}-{stage}.md')
if missing:
    print(f'MISSING: {missing}')
else:
    print('All manifest skills exist')
"
```

Expected: `All manifest skills exist`

- [ ] **Step 3: Verify old directories gone**

```bash
ls ~/GrowDirect/Cove/.claude/skills/ 2>&1
ls ~/GrowDirect/Canary/.claude/skills/ 2>&1
```

Expected: "No such file or directory" for both

- [ ] **Step 4: Verify settings.json preserved**

```bash
cat ~/GrowDirect/Cove/.claude/settings.json | python3 -c "import sys,json; json.load(sys.stdin); print('Valid')"
cat ~/GrowDirect/Canary/.claude/settings.json | python3 -c "import sys,json; json.load(sys.stdin); print('Valid')"
```

Expected: `Valid` for both

- [ ] **Step 5: Verify no .fuse_hidden files remain**

```bash
find ~/GrowDirect/.claude/skills/ -name ".fuse_hidden*" 2>/dev/null | wc -l
```

Expected: 0

- [ ] **Step 6: Commit verification results**

```bash
git commit --allow-empty -m "verify: factory hardening — all 42 skills flat, manifest valid, old dirs removed (GRO-376)"
```
