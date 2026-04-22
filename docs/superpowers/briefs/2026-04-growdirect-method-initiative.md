---
title: GrowDirect Method Initiative — Sprints A–E
date: 2026-04-21
type: brief
sprint: method-initiative-closeout
status: shipped
---

# GrowDirect Method Initiative — Closeout Brief

## Purpose

Summary of a five-sprint initiative that turned GrowDirect's scattered operational assets into a navigable "method" — modeled on IBM Global Services MethodWeb (2001) but native to Obsidian, Linear, and Claude Code skills. Reference artifact for future sessions.

## What was built

### Sprint A — MOC scaffolding (no content changes)
- `Brain/projects/Method.md` — top-level navigation MOC
- `Brain/projects/Factory.md` — 9-stage pipeline MOC with roles × skills × work products matrix
- 5 category MOCs at `Brain/method/`: `Models.md`, `Roles.md`, `Techniques.md`, `WorkProducts.md`, `Activities.md`, `CommDocs.md`

### Sprint B — Role profile augmentation
- 12 role profiles in `Canary/docs/profiles/ops/` each gained a `## Method cross-reference` section with:
  - Factory stage affinity (primary/assist)
  - Skills frequently invoked (plugin-namespaced)
  - Produces (with wiki links to templates + doc paths)
  - Coordinates with (wiki-linked to peer profiles)
  - Linear activity filter (label / type query)

### Sprint C — Reverse-direction tagging
- 36 skills in `.claude/skills/factory-*`, `canary-*`, `cove-*` gained `roles-primary`, `roles-assist`, `stage` frontmatter
- 7 Brain templates gained `method-role` + `method-stage`
- 5 platform SDDs gained `Author role` + `Operator role` in their callout headers
- Non-factory-family skills (gitnexus, rooster, jeffe-review, file-guardian, project-timelog, remember-quote, session-synthesis, founder-probe) left untagged — not in the Factory stage taxonomy

### Sprint D — Query CLI
New `method` command group in `content-engine/engine.py`:
- `method skills-for --role <Name> [--stage <stage>] [--primary-only]`
- `method templates-for --role <Name>`
- `method roles` — all roles with stage coverage
- `method stats` — tagged vs untagged counts

8 new pytest tests in `content-engine/tests/test_method.py`. Also tagged 10 core Canary SDDs (architecture, platform-overview, data-model, identity, tsp, chirp, fox, owl, alx, ops).

Also fixed a pre-existing bug: PDF fixture tests now skip gracefully when `sample.pdf` is missing (gitignored via `*.pdf`).

### Sprint E — Coverage completion
40 additional SDDs tagged across Canary (13 remaining), Cove (16), Angel (6), ALX-dir (2), ARC (1). Idempotent script used `/tmp/tag-sdds.py` with filename-keyword heuristics (governance→Compliance+Legal, metrics→Tom+Research, ui→Art+Jeremy, etc.).

## End-state inventory

| Asset class | Total | Tagged |
|---|---|---|
| Role profiles | 12 | 12 (100%) |
| In-repo skills (.claude/skills) | 45 | 36 factory-family (80%) |
| Brain templates | 7 | 7 (100%) |
| Platform SDDs | 5 | 5 (100%) |
| Canary SDDs | 26 | 23 |
| Cove SDDs | 18 | 16 (2 skipped — no anchor header) |
| Angel SDDs | 7 | 6 (1 skipped) |
| ALX SDDs | 2 | 2 (100%) |
| ARC SDDs | 1 | 1 (100%) |
| **Total Method-tagged files** | — | **~108** |

## How to use the Method

### For humans — navigate in Obsidian
1. Open `Brain/projects/Method.md` — landing page for the whole method
2. Drill into `Brain/projects/Factory.md` for the 9-stage pipeline with roles + skills matrix
3. Open any role profile in `Canary/docs/profiles/ops/` — scroll to `## Method cross-reference` for that role's techniques + WPs + stage affinity
4. Use Obsidian graph view on `Method.md` to see the whole cluster at once

### For agents — query via CLI
```bash
# Who uses which skills?
python3 content-engine/engine.py method skills-for --role ALX

# Which skills run a factory stage?
python3 content-engine/engine.py method skills-for --stage blueprint

# What templates does a role author?
python3 content-engine/engine.py method templates-for --role Research

# Method coverage stats
python3 content-engine/engine.py method stats

# All roles + their stages + skills
python3 content-engine/engine.py method roles
```

### For new skills — set frontmatter at creation
When creating a new skill file under `.claude/skills/`, add these keys after `name:`:

```yaml
---
name: my-new-skill
roles-primary: [<role>]
roles-assist: [<role>]
stage: <factory_stage_name>   # omit if cross-cutting
description: ...
---
```

Query tools will pick it up automatically after the next `engine.py registry build`.

### For new SDDs — add Method links
Every new SDD gets two lines in its header block:

```markdown
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[Canary/docs/profiles/ops/<Name>|<Name>]] · **Operator role:** [[Canary/docs/profiles/ops/<Name>|<Name>]]
```

## Real coverage data (from `method stats`)

```
Skills:    36 tagged, 9 untagged
Templates: 7 tagged, 0 untagged

  Stage coverage (skills):
    assembly     3    preflight    3    tdd        3
    blueprint    3    qa           3    verify     3
    close        3    research     1    ship       3

  Role coverage (primary skills):
    Jeremy       14   Compliance   4    Research     1
    ALX          7    Jim          2    DevOps       1
    Tom          5                      Eva          1
                                        Jess         1
```

## Insights surfaced by the data

1. **Jeremy is over-leveraged** — 14 primary skills vs. 1 for Jess or Eva. If the skill inventory reflects real work distribution, Jeremy is the bottleneck.
2. **Research has 1 primary skill (`factory-research`)** — the role is newer; skill coverage will grow as more research techniques get codified.
3. **No skills tagged for `research` stage beyond 1** — suggests the research stage may be under-specified in the factory skill catalog. Opportunity to add techniques (competitive-brief, prior-art-scan, decision-log-lookup, etc.) as skills.
4. **Stage symmetry is solid** — every main stage (preflight, blueprint, tdd, assembly, verify, qa, ship, close) has exactly 3 skills (one each for factory/canary/cove). The app-variant pattern is consistent.

## Skills NOT in the method (and why that's OK)

Non-factory-family skills exist for cross-cutting concerns and aren't tagged with a Factory stage:

- `gitnexus` — code intelligence queries, cross-stage
- `rooster` — Jim's QA test-scenario framework, orthogonal to Factory
- `jeffe-review` — founder vision check, before any Factory run
- `file-guardian` — protected-file editor, orthogonal
- `project-timelog` — Eva's tracking, spans all stages
- `remember-quote`, `session-synthesis` — ALX memory tools, cross-stage
- `founder-probe` — discovery tool, pre-Factory

These remain un-method-tagged intentionally. If a future session wants them in the graph, add a `roles-primary: [...]` frontmatter field (no stage needed).

## Files skipped (manual tag later if valued)

- `docs/sdds/cove/member-auth.md` — no anchor header for the script
- `docs/sdds/angel/lp-integration.md` — same

## What comes next (not in scope of this initiative)

1. **Plugin skills (outside `.claude/skills/`)** — `superpowers:*`, `engineering:*`, `legal:*`, `marketing:*`, etc. live in `~/.claude/plugins/cache/` and are plugin-maintained. Proposal: a sidecar index at `Brain/method/plugin-skills.md` that maps plugin skills to roles without modifying plugin files.
2. **Linear saved-view URLs** — role profile activity filters are prose today; they become clickable once the views exist in Linear.
3. **Pipeline evals** — only `preflight` has `eval_threshold: 1.0` in `factory-manifest.json`. Other stages are undeclared.
4. **`method roles --concise`** — the full output is ~450 lines on real data. A concise mode would fit on one screen.
5. **Skill inventory rebalancing** — Jim / Jess / Eva / Research have thin skill coverage. Worth an audit of what techniques those roles actually run day-to-day and whether they'd benefit from being codified as skills.
6. **Linear GRO issues to file** — one per "what comes next" item above, plus the seven handoff brief items from the Secure → Canary initiative.

## Commits (on main)

Sprint A, B, C, D, E each shipped as 1-2 commits. ~12 commits total for the Method initiative.

## Related

- [[Brain/projects/Method|Method MOC]]
- [[Brain/projects/Factory|Factory MOC]]
- [[Brain/method/Models|Method › Models]]
- [[Brain/method/Roles|Method › Roles]]
- [[Brain/method/Techniques|Method › Techniques]]
- [[Brain/method/WorkProducts|Method › Work Products]]
- [[Brain/method/Activities|Method › Activities]]
- [[Brain/method/CommDocs|Method › CommDocs]]
- [[docs/sdds/platform/factory-pipeline|Factory Pipeline SDD]]
- [[docs/sdds/platform/skill-architecture|Skill Architecture SDD]]
- IBM MethodWeb (inspiration only, not ingested): `/Users/gclyle/Desktop/IBM Method Web/IBMGSM40/`

## Sources

- `content-engine/engine.py` — added `method` command group (lines 1291+ in post-sprint state)
- `content-engine/tests/test_method.py` — 8 new tests
- `/tmp/tag-sdds.py`, `/tmp/tag-skills.py` — transient tagger scripts (not committed)
- 12 role profiles in `Canary/docs/profiles/ops/`
- 7 templates in `Brain/templates/`
- 36+ skills in `.claude/skills/`
- 60+ SDDs across `docs/sdds/{canary,platform,cove,angel,alx,arc}/`
