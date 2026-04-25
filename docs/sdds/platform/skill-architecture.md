---
classification: confidential
owner: GrowDirect LLC
---

# GrowDirect Skill Architecture

> **Type:** Platform Service
> **Status:** Active — 38 skills deployed, 19 planned, eval framework designed
> **Date:** 2026-03-30 (ops upgrade 2026-04-13)
> **Linear:** GRO-378
> **Author role:** [[docs/team/Architect|Architect]] · **Operator role:** [[docs/team/ALX|ALX]]

**Wiki:** [[Brain/wiki/document-management|Document Management]] · [[Brain/wiki/growdirect-workflow|GrowDirect Workflow]]
**Method:** [[Brain/projects/Method|Method MOC]] · [[Brain/method/Techniques|Method › Techniques]]
**Related:** [[docs/sdds/platform/factory-pipeline|Factory Pipeline]] · [[docs/sdds/platform/memory-bus|Memory Bus]]

---

## Purpose

Defines the skill taxonomy, evaluation strategy, and pipeline integration for
all Claude Code skills across the GrowDirect platform. Skills are the operational
knowledge layer — they extract domain rules from source material (bylaws, SDDs,
API docs) and wire them into the factory pipeline so agents make correct decisions
during build sessions.

---

## Dependencies

| Dependency | Type | Required |
|------------|------|----------|
| `.claude/skills/` directory | Skill file storage | Yes |
| `factory-manifest.json` | Stage-to-skill mapping | Yes |
| Memory Bus MCP (port 8003) | Session memory for skill outputs | Optional |
| Linear MCP | Issue routing for factory stages | For factory pipeline skills |
| Obsidian MCP | Brain knowledge access | For domain skills |
| Source material (bylaws, SDDs, API docs) | Knowledge extraction input | Per skill |

---

## Architecture Overview

Four layers, each with domain-specific skills extracted from operational source material.

```
┌─────────────────────────────────────────────────────┐
│  Layer 1: GrowDirect Corp (DOA)                     │
│  Platform standards, factory process, agent topology │
├─────────────────────────────────────────────────────┤
│  Layer 2a: Cove          │  Layer 2b: Canary        │
│  HOA governance          │  Loss prevention          │
│  Davis-Stirling          │  PCI awareness            │
├──────────────────────────┴──────────────────────────┤
│  Layer 3: Shared Memory (ALX)                       │
│  Cross-app knowledge, context assembly, prior art   │
└─────────────────────────────────────────────────────┘
```

---

## Data Flow & PII Map

Skills themselves contain no PII. However, skills may access PII during execution:

| Skill Category | PII Access | Classification |
|---------------|-----------|---------------|
| Factory pipeline skills (Layer 1) | None — infrastructure checks | N/A |
| Cove governance skills (Layer 2a) | Member data via DB queries | **internal** (gated by app auth) |
| Canary LP skills (Layer 2b) | Transaction data via DB queries | **sensitive** (merchant PII) |
| Memory Bus skills (Layer 3) | Session decisions, architectural notes | internal |

Skills do not store PII. They read from app databases during execution and
write structured outputs to memory bus or Linear. PII handling is governed by
the app-level SDDs, not the skill layer.

---

## Skill Inventory

### Layer 1: GrowDirect Corp (DOA) — 11 Existing

| Skill | File | Purpose | Eval Type |
|-------|------|---------|-----------|
| Factory Preflight | `factory-preflight.md` | Infrastructure health + context loading | Binary |
| Factory Research | `factory-research.md` | Prior art from memory bus, GitNexus, docs | Pattern |
| Factory Blueprint | `factory-blueprint.md` | Plan writing with architecture decisions | Pattern |
| Factory TDD | `factory-tdd.md` | Test-first development (RED-GREEN-REFACTOR) | Binary |
| Factory Assembly | `factory-assembly.md` | Implement blueprint tasks incrementally | Binary |
| Factory Verify | `factory-verify.md` | Full test suite + regression detection | Binary |
| Factory QA | `factory-qa.md` | Route testing, auth, standards compliance | Pattern |
| Factory Ship | `factory-ship.md` | Pre-ship checklist, push, Linear update | Binary |
| Factory Close | `factory-close.md` | Session summary, memory writes, new issues | Pattern |
| Factory Linear | `factory-linear.md` | Linear MCP integration at stage boundaries | Binary |
| Factory New App | `factory-newapp.md` | Scaffold new app from proven patterns | Pattern |

### Layer 2a: Cove (HOA Governance) — 8 Existing

| Skill | File | Purpose | Eval Type |
|-------|------|---------|-----------|
| Cove Preflight | `cove-preflight.md` | Factory + Davis-Stirling context | Binary |
| Cove Blueprint | `cove-blueprint.md` | Plan writing with compliance checks | Pattern |
| Cove TDD | `cove-tdd.md` | Test-first with governance rules | Binary |
| Cove Assembly | `cove-assembly.md` | Implementation + blueprint registration, RLS | Binary |
| Cove Verify | `cove-verify.md` | Test suite + compliance verification | Binary |
| Cove QA | `cove-qa.md` | Route testing + governance compliance | Pattern |
| Cove Ship | `cove-ship.md` | Ship with Davis-Stirling documentation | Binary |
| Cove Close | `cove-close.md` | Session close + compliance notes | Pattern |

### Layer 2b: Canary (Loss Prevention) — 14 Existing

| Skill | File | Purpose | Eval Type |
|-------|------|---------|-----------|
| Canary Preflight | `canary-preflight.md` | Factory + stack health, env, tunnel | Binary |
| Canary Blueprint | `canary-blueprint.md` | Plan writing with data integrity guardrails | Pattern |
| Canary TDD | `canary-tdd.md` | Test-first with retail-aware philosophy | Binary |
| Canary Assembly | `canary-assembly.md` | Implementation with data integrity checks | Binary |
| Canary Verify | `canary-verify.md` | Evidence-before-assertions, five-step gate | Binary |
| Canary QA | `canary-qa.md` | Diff-aware QA (4 modes) | Pattern |
| Canary Ship | `canary-ship.md` | Bisectable commits, deployment bridge | Binary |
| Canary Close | `canary-close.md` | Session teardown + ALX memory storage | Pattern |
| Canary Deploy | `canary-deploy.md` | 7-step deployment pipeline | Binary |
| Canary Data Expansion | `canary-data-expansion.md` | Square data model expansion (4 patterns) | Pattern |
| Canary Debug | `canary-debug.md` | 4-phase root cause investigation | Pattern |
| Canary Review | `canary-review.md` | Code review process | Pattern |
| Canary Scenario | `canary-scenario.md` | Scenario testing | Pattern |
| Canary UAT | `canary-uat.md` | User acceptance testing | Pattern |

### Layer 3: Shared Memory (ALX) — 5 Existing

| Skill | File | Purpose | Eval Type |
|-------|------|---------|-----------|
| GitNexus | `gitnexus.md` | Code intelligence queries | Binary |
| Session Synthesis | `session-synthesis.md` | Chat transcript to structured doc | Pattern |
| File Guardian | `file-guardian.md` | Protected file modification gate | Binary |
| Jeffe Review | `jeffe-review.md` | CEO-level plan review | LLM-as-judge |
| Founder Probe | `founder-probe.md` | Biographical depth via follow-up probes | LLM-as-judge |

### Planned Skills (19 total)

| Layer | Skill | Source Material | Priority |
|-------|-------|----------------|----------|
| Corp | Platform Preflight (formalized) | factory-preflight + infra standards | Session 1 |
| Corp | Factory Dispatch | Agent topology, Linear routing | Session 3 |
| Corp | Weekly Rollup | Cross-project status | Future |
| Corp | Issue Triage | CLAUDE.md hard rules | Future |
| Corp | Architecture Decision (ADR) | Tech stack standards | Future |
| Cove | Quorum Calculator | Bylaws, AB 2460 | Session 2 |
| Cove | Governance Compliance Check | Davis-Stirling Act | Future |
| Cove | Election Builder | Bylaws, Civil Code 5100-5145 | Future |
| Cove | Archive Intake | Chain of custody rules | Future |
| Cove | Parcel Resolver | Bylaws 5.2, APN database | Future |
| Canary | Rule Tuning | Chirp rule definitions | Future |
| Canary | Merchant Onboarding | Square OAuth flow | Future |
| Canary | Evidence Package | Fox case workflow | Future |
| Canary | Weekly Money Report | Owl narrative patterns | Future |
| Canary | Detection Pattern Design | LP Pattern Catalog | Future |
| Shared | Context Assembly | Memory bus tools | Session 3 |
| Shared | Knowledge Gap Detection | Task vs memories | Future |
| Shared | Post-Mortem Capture | Factory close patterns | Session 3 |
| Shared | Prior Art Search | Memory bus + GitNexus | Future |

---

## Eval Strategy

Every skill gets an eval suite before deployment. Target: 90%+ pass rate.

### Eval Types

| Type | Method | When to Use |
|------|--------|-------------|
| **Binary** | Pass/fail assertions (exit codes, file existence, regex) | Infrastructure, build gates, data validation |
| **Pattern** | Regex matching on output (sections, formats, values) | Structured output skills |
| **LLM-as-judge** | Claude evaluates against domain criteria | Compliance reasoning, narrative quality |

### Ratio Guideline

- Infrastructure/build: 100% binary
- Structured output: ~85% pattern + ~15% LLM-as-judge
- Domain reasoning: ~50% pattern + ~50% LLM-as-judge

### Eval File Convention

```
evals/skills/
  test_platform_preflight.py
  test_quorum_calculator.py
  conftest.py
```

---

## Pipeline Integration

`factory-manifest.json` maps stages to skills. Current state includes skill
reference and eval path for preflight stage. Target: all stages get eval
entries.

```json
{
  "preflight": {
    "skill": "factory-preflight",
    "eval": "evals/skills/test_platform_preflight.py",
    "eval_threshold": 1.0
  }
}
```

---

## Skill Pipeline (Per Skill)

Adapted from George Nurijanian's 7-step process:

1. **Load source material** — bylaws, CLAUDE.md, SDDs, archive docs
2. **Extract operational knowledge** — rules, thresholds, decision criteria
3. **Wire to build environment** — memory bus + Linear as query layer
4. **Scaffold the skill** — `skill-creator` tool with frontmatter, modes, templates
5. **Design evals** — binary + regex + LLM-as-judge
6. **Run evals, fix, iterate** — unattended optimization loop
7. **Validate against source** — cross-check against original domain material

---

## Operations

### Startup Sequence

Skills are loaded by Claude Code at session start. No separate startup process.
The factory pipeline reads `factory-manifest.json` to determine which skill
applies to each stage.

### Health Checks

- All 38 skill files exist in `.claude/skills/`
- `factory-manifest.json` references valid skill files
- Eval suites pass at threshold (currently only preflight has eval)

### Failure Modes

| Failure | Behavior | Recovery |
|---------|----------|----------|
| Skill file missing | Factory stage falls back to unguided behavior | Restore from git |
| Eval threshold not met | Skill flagged as degraded, still usable | Fix skill, re-run evals |
| Memory Bus unavailable | Skills that write to memory silently skip | Memory bus restart |
| Source material outdated | Skills produce stale guidance | Re-extract from updated sources |

### Monitoring

| Metric | Alert Threshold |
|--------|----------------|
| Skill count mismatch (files vs manifest) | Any discrepancy |
| Eval pass rate per skill | Below 90% |
| Skills without evals | More than 50% of deployed skills |

### Configuration

| Setting | Location | Purpose |
|---------|----------|---------|
| Skill files | `.claude/skills/*.md` | Skill definitions |
| Stage mapping | `factory-manifest.json` | Which skill runs at which stage |
| Eval suites | `evals/skills/` | Test files per skill |
| Memory tags | Per skill (`corp`, `cove`, `canary`, `shared`) | Layer-based memory tagging |

---

## Deployment

Skills are git-tracked files, not running services. Deployment is a git push.
No Docker containers, no AWS services.

### Multi-Tenant Isolation

Skills are app-scoped by layer (Corp, Cove, Canary, Shared). A Cove skill
cannot access Canary data and vice versa — isolation is enforced by the app's
auth layer, not the skill itself.

### Domain Guardrails

Each app layer has domain-specific constraints that its skills enforce:

| Layer | Guardrail |
|-------|-----------|
| Cove | Davis-Stirling compliance checks on every governance feature |
| Canary | Data integrity checks on every transaction pipeline change |
| Corp | Platform standards (UUID PKs, Mapped[] syntax, no Column()) |
| Shared | Cross-app knowledge must be tagged by source layer |

---

## Code Review Findings

### P1 — Before GA

| # | Finding | Recommended Fix | Linear |
|---|---------|----------------|--------|
| 1 | Only 1 of 38 skills has an eval suite (preflight) — 97% coverage gap | Prioritize evals for high-impact skills: Cove Preflight, Canary Verify, Factory TDD | — |
| 2 | No runtime validation that skill files match manifest entries | Add preflight check: every manifest skill reference resolves to a file | — |
| 3 | Planned skills (19) have no timeline beyond "Session N" or "Future" | Prioritize top 5 planned skills in Linear with concrete session targets | — |
| 4 | Memory tagging (`corp`, `cove`, `canary`, `shared`) is documented but not validated | Add memory bus tag validation to factory close stage | — |

### P2 — Post-Launch

| # | Finding | Recommended Fix | Linear |
|---|---------|----------------|--------|
| 1 | 4 utility skills (remember-quote, rooster, project-timelog, cove-archive) exist outside the taxonomy | Classify: keep as utility, promote to layer, or archive | — |
| 2 | No skill versioning — changes to skills overwrite in-place with no rollback beyond git | Acceptable for current scale; add version frontmatter if skill count exceeds 60 | — |
| 3 | Eval framework designed but `evals/skills/` directory may not exist yet | Create directory with conftest.py scaffold | — |

---

## Production Readiness Checklist

- [ ] All deployed skills have eval suites (target: 90%+ coverage)
- [ ] factory-manifest.json references valid skill files
- [ ] Eval threshold enforced at stage boundaries
- [ ] Memory bus tags validated per layer
- [ ] Planned skills prioritized in Linear
- [ ] Domain guardrails documented per app layer
- [ ] Skill files backed up via git (standard)

---

## Inventory Summary

| Layer | Existing | Planned | Total |
|-------|----------|---------|-------|
| Corp (DOA) | 11 | 5 | 16 |
| Cove | 8 | 5 | 13 |
| Canary | 14 | 5 | 19 |
| Shared (ALX) | 5 | 4 | 9 |
| **Total** | **38** | **19** | **57** |

*Note: 4 additional utility skills exist but are not part of the factory pipeline.*

---

*GrowDirect Skill Architecture — GrowDirect Inc.*
