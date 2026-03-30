# GRO-376 — Factory Hardening Design

**Date:** 2026-03-30
**Status:** Approved
**Issue:** [GRO-376](https://linear.app/growdirect/issue/GRO-376)

## Problem

The factory process (8 platform skills + app overrides) works but has no machine-readable contract. Skills are nested 3 levels deep. Sessions rediscover the pipeline by reading markdown. There's no preflight check, no standardized Linear integration, and no research stage.

## Decisions

1. **Manifest** — `factory-manifest.json` declares the pipeline, stages, app overrides
2. **Preflight replaces startup** — one stage for infra checks + context loading
3. **Research stage added** — queries memory bus + optional sources before blueprint
4. **Linear standardized** — dedicated skill for all Linear read/write at stage boundaries
5. **All skills flattened** — one directory at `~/GrowDirect/.claude/skills/`, app-prefixed
6. **Official MCP SDK going forward** — new services use `FastMCP`, not custom Flask MCP
7. **GitNexus consolidated** — 6 skills → 1 platform skill, full setup deferred to new GRO

## Pipeline

```
factory-preflight → factory-research → factory-blueprint → factory-tdd →
    factory-assembly → factory-verify → factory-qa → factory-ship → factory-close
```

Preflight identifies the app context. From that point, every stage checks: does `{app}-{stage}.md` exist? If yes, use it (it runs factory base + app-specific additions). If no, use `factory-{stage}.md`.

**Note:** `research` is intentionally absent from app override lists. The factory-level research (memory bus + GitNexus + optional sources) is sufficient for all apps. App-specific research overrides can be added later if an app needs to query a unique source (e.g., Canary querying Square API docs via Firecrawl).

## 1. factory-manifest.json

Lives at `~/GrowDirect/factory-manifest.json`:

```json
{
  "version": "1.0",
  "pipeline": ["preflight", "research", "blueprint", "tdd", "assembly", "verify", "qa", "ship", "close"],
  "stages": {
    "preflight": {
      "replaces": "startup",
      "inputs": ["gro_issue"],
      "outputs": ["preflight_report"],
      "required_mcps": ["linear"],
      "optional_mcps": ["memory-bus"],
      "checks": ["docker", "postgres", "valkey", "ollama", "git_clean", "gro_exists"]
    },
    "research": {
      "inputs": ["gro_issue", "preflight_report"],
      "outputs": ["context_bundle"],
      "required_mcps": [],
      "optional_mcps": ["memory-bus", "gitnexus", "obsidian", "firecrawl"]
    },
    "blueprint": {
      "inputs": ["gro_issue", "preflight_report", "context_bundle"],
      "outputs": ["docs/plans/{date}-{slug}.md"],
      "required_mcps": ["linear"],
      "optional_mcps": ["memory-bus"]
    },
    "tdd": {
      "inputs": ["plan"],
      "outputs": ["tests/"],
      "required_mcps": []
    },
    "assembly": {
      "inputs": ["plan", "failing_tests"],
      "outputs": ["implementation"],
      "required_mcps": []
    },
    "verify": {
      "inputs": ["implementation"],
      "outputs": ["verify_report"],
      "required_mcps": []
    },
    "qa": {
      "inputs": ["verify_report"],
      "outputs": ["qa_report"],
      "required_mcps": []
    },
    "ship": {
      "inputs": ["qa_report"],
      "outputs": ["git_push", "linear_update"],
      "required_mcps": ["linear"]
    },
    "close": {
      "inputs": ["ship_result"],
      "outputs": ["session_summary"],
      "required_mcps": ["linear"],
      "optional_mcps": ["memory-bus"]
    }
  },
  "apps": {
    "canary": {
      "compliance": "pci-awareness",
      "overrides": ["preflight", "blueprint", "tdd", "assembly", "verify", "qa", "ship", "close"]
    },
    "cove": {
      "compliance": "davis-stirling",
      "overrides": ["preflight", "blueprint", "tdd", "assembly", "verify", "qa", "ship", "close"]
    }
  }
}
```

## 2. New Skills

### factory-preflight (replaces factory-startup)

Runs before any factory stage. Three-tier result:

| Check | Green | Yellow | Red |
|-------|-------|--------|-----|
| Docker stack | All containers healthy | Some unhealthy | Docker not running |
| PostgreSQL | Connected, app DB exists | Slow response | Unreachable |
| Valkey | Connected | High memory | Unreachable |
| Ollama | Connected, model loaded | Model not loaded | Unreachable |
| Linear MCP | Reachable, GRO issue found | Issue not found | Unreachable |
| Git status | Clean working tree | Uncommitted changes | Not a git repo |
| Memory bus | Connected | Not running | — (optional) |

Yellow = warn and continue. Red on any check = stop and report.

After checks pass, preflight loads context: reads `CLAUDE.md`, reads `factory-manifest.json`, loads GRO issue from Linear, queries memory bus for prior art (if available). Identifies app context for stage branching.

### factory-linear

Standardizes all Linear integration at stage boundaries:

| Stage | Linear Action |
|-------|--------------|
| Preflight | Read issue, validate exists, pull description |
| Blueprint | Attach plan doc as issue document, move to "In Progress" |
| Ship | Post verify/QA results as comment, move to "Done" |
| Close | Post session summary as comment |

### factory-research

Runs between preflight and blueprint. Queries available sources:

1. **Memory bus** — `memory_recall` for prior decisions, `context_assemble` for domain context
2. **GitNexus** (optional) — blast radius and architecture context for files the GRO issue touches
3. **Obsidian** (optional) — related architecture notes
4. **Firecrawl** (optional) — external API docs if GRO involves third-party integrations

Outputs a context bundle (markdown) consumed by blueprint. If sources aren't available, research skips gracefully — blueprint starts from scratch.

## 3. Skill Flattening

All skills move to `~/GrowDirect/.claude/skills/`. Flat `.md` files, no subdirectories.

### Platform skills (no app prefix)

| Skill | Origin | Notes |
|-------|--------|-------|
| `factory-preflight.md` | new | Replaces startup |
| `factory-research.md` | new | |
| `factory-linear.md` | new | |
| `factory-blueprint.md` | stays | |
| `factory-tdd.md` | stays | |
| `factory-assembly.md` | stays | |
| `factory-verify.md` | stays | |
| `factory-qa.md` | stays | |
| `factory-ship.md` | stays | |
| `factory-close.md` | stays | |
| `factory-newapp.md` | was `Cove/.claude/skills/grow-newapp` | |
| `file-guardian.md` | was `Canary/.claude/skills/critical-file-guardian` | |
| `gitnexus.md` | consolidated from 6 gitnexus skills | |
| `jeffe-review.md` | was `Canary/.claude/skills/jeffe-review` | |
| `founder-probe.md` | was `Canary/.claude/skills/founder-probe/founder-probe/SKILL.md` | |
| `remember-quote.md` | was `Canary/.claude/skills/remember-quote/remember-quote/SKILL.md` | |
| `project-timelog.md` | was `Canary/.claude/skills/project-timelog/SKILL.md` | |
| `session-synthesis.md` | was `Canary/.claude/skills/session-synthesis/session-synthesis/SKILL.md` | |
| `rooster.md` | was `Canary/.claude/skills/rooster/rooster/SKILL.md` | |

### Canary-specific

| Skill | Origin |
|-------|--------|
| `canary-preflight.md` | new (replaces `alx-startup`) |
| `canary-blueprint.md` | was `Canary/.claude/skills/canary-blueprint/SKILL.md` |
| `canary-tdd.md` | was `Canary/.claude/skills/canary-tdd/SKILL.md` |
| `canary-assembly.md` | was `Canary/.claude/skills/canary-assembly/SKILL.md` |
| `canary-verify.md` | was `Canary/.claude/skills/canary-verify/SKILL.md` |
| `canary-qa.md` | was `Canary/.claude/skills/canary-qa/SKILL.md` |
| `canary-ship.md` | was `Canary/.claude/skills/canary-ship/SKILL.md` |
| `canary-close.md` | was `Canary/.claude/skills/alx-session-close/SKILL.md` |
| `canary-data-expansion.md` | was `Canary/.claude/skills/canary-data-expansion/SKILL.md` |
| `canary-debug.md` | was `Canary/.claude/skills/canary-debug/SKILL.md` |
| `canary-deploy.md` | was `Canary/.claude/skills/canary-deploy/SKILL.md` (inline refs) |
| `canary-review.md` | was `Canary/.claude/skills/canary-review/SKILL.md` |
| `canary-scenario.md` | was `Canary/.claude/skills/canary-scenario/SKILL.md` |
| `canary-uat.md` | was `Canary/.claude/skills/canary-uat/canary-uat/SKILL.md` |

### Cove-specific

| Skill | Origin |
|-------|--------|
| `cove-preflight.md` | new (replaces `cove-startup`) |
| `cove-blueprint.md` | was `Cove/.claude/skills/cove-blueprint/SKILL.md` |
| `cove-tdd.md` | was `Cove/.claude/skills/cove-tdd/SKILL.md` |
| `cove-assembly.md` | was `Cove/.claude/skills/cove-assembly/SKILL.md` |
| `cove-verify.md` | was `Cove/.claude/skills/cove-verify/SKILL.md` |
| `cove-qa.md` | was `Cove/.claude/skills/cove-qa/SKILL.md` |
| `cove-ship.md` | was `Cove/.claude/skills/cove-ship/SKILL.md` |
| `cove-close.md` | was `Cove/.claude/skills/cove-close/SKILL.md` |
| `cove-archive.md` | was `Cove/.claude/skills/cove-archive/SKILL.md` |

### Deleted

- `factory-startup.md` — replaced by `factory-preflight.md`
- `Cove/.claude/skills/cove-startup/SKILL.md` — replaced by `cove-preflight.md`
- `Canary/.claude/skills/alx-startup/SKILL.md` — replaced by `canary-preflight.md`
- `Canary/.claude/skills/content-extractor/` — stale, dropped
- `Canary/.claude/skills/gitnexus/` (6 skills) — consolidated into `gitnexus.md`
- `Cove/.worktrees/cove-parcel-contacts/.claude/skills/` — stale worktree copies
- All nested `SKILL.md` directory structures under `Cove/.claude/skills/` and `Canary/.claude/skills/`

### Skills with assets/references/scripts

Skills that had `assets/`, `references/`, `scripts/` subdirectories (canary-deploy, canary-uat, founder-probe, project-timelog, remember-quote, rooster, session-synthesis):
- Essential content inlined into the flat `.md` file
- Reference data that's still needed moves to `docs/skills/{skill-name}/` (e.g., `docs/skills/canary-deploy/environment.md`)
- Stale assets and `.fuse_hidden*` files dropped

**Total after flattening: 42 flat `.md` files in one directory.**

## 4. Verification

- `factory-manifest.json` passes JSON schema validation
- Every skill in the manifest exists as a `.md` file in `GrowDirect/.claude/skills/`
- Every app override has a corresponding `{app}-{stage}.md` file
- Old skill directories are gone (`Cove/.claude/skills/` and `Canary/.claude/skills/` removed). Note: `.claude/settings.json` files in each app are preserved — only the `skills/` subdirectory is removed.
- `.fuse_hidden*` files in skill directories cleaned up during migration
- Preflight runs successfully against healthy Docker stack
- Factory process works end-to-end from new flat location
- CLAUDE.md Factory Process section updated to reflect 9-stage pipeline (preflight, research, blueprint, tdd, assembly, verify, qa, ship, close)

## 5. New GRO Issue (out of scope)

**GitNexus platform setup** — index both apps at GrowDirect root, run GitNexus MCP server as sidecar, integrate with `factory-research`. Filed separately.

## Acceptance Criteria

- [ ] `factory-manifest.json` exists at GrowDirect root, valid JSON
- [ ] `factory-preflight` runs and reports red/yellow/green
- [ ] `factory-linear` handles read-issue → update-status → attach-document
- [ ] `factory-research` queries memory bus + optional sources before blueprint
- [ ] All skills flattened to `~/GrowDirect/.claude/skills/` — no nesting
- [ ] Old skill directories deleted from Cove and Canary
- [ ] Existing factory process works after reorganization
- [ ] Pipeline: preflight → research → blueprint → tdd → assembly → verify → qa → ship → close
- [ ] CLAUDE.md Factory Process section updated to match 9-stage pipeline
- [ ] `.claude/settings.json` preserved in both Canary and Cove after skills directory removal
