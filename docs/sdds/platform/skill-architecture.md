# GrowDirect Skill Taxonomy

> GRO-378 — Skill architecture: top-down knowledge pipeline from DOA to app domain
>
> Created: 2026-03-30

## Architecture Overview

Four layers, each with domain-specific skills extracted from operational source material.
Skills follow George Nurijanian's 7-step pipeline: load source → extract operational
knowledge → wire to build environment → scaffold → design evals → run evals → validate
against source.

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

## Layer 1: GrowDirect Corp (DOA)

Source material: `CLAUDE.md`, `factory-manifest.json`, agent topology docs,
Docker conventions, port allocation, volume mounting rules.

### Existing Skills (11)

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

### Planned Skills

| Skill | Source Material | Eval Type | Priority |
|-------|----------------|-----------|----------|
| Platform Preflight (formalized) | `factory-preflight.md` + infra standards | 100% binary | **Session 1** |
| Factory Dispatch | Agent topology, Linear routing rules | Pattern + binary | Session 3 |
| Weekly Rollup | Cross-project status patterns | LLM-as-judge | Future |
| Issue Triage | CLAUDE.md hard rules, scope control | Pattern | Future |
| Architecture Decision (ADR) | Tech stack standards, prior ADRs | Pattern + LLM | Future |

---

## Layer 2a: Cove (HOA Governance)

Source material: WPBCA Bylaws (77 pages, 2012), Davis-Stirling Act (Civil Code §4000+),
AB 502, AB 2159, AB 2460, AB 130, SB 900, `wpbca-bylaws-config.json`, archive corpus.

### Existing Skills (8)

| Skill | File | Purpose | Eval Type |
|-------|------|---------|-----------|
| Cove Preflight | `cove-preflight.md` | Delegates to factory + adds Davis-Stirling context | Binary |
| Cove Blueprint | `cove-blueprint.md` | Plan writing with compliance checks | Pattern |
| Cove TDD | `cove-tdd.md` | Test-first with governance rules | Binary |
| Cove Assembly | `cove-assembly.md` | Implementation + blueprint registration, RLS | Binary |
| Cove Verify | `cove-verify.md` | Test suite + compliance verification | Binary |
| Cove QA | `cove-qa.md` | Route testing + governance compliance | Pattern |
| Cove Ship | `cove-ship.md` | Ship with Davis-Stirling documentation | Binary |
| Cove Close | `cove-close.md` | Session close + compliance notes | Pattern |

### Planned Skills

| Skill | Source Material | Eval Type | Priority |
|-------|----------------|-----------|----------|
| Quorum Calculator | Bylaws §5.9, §6.6, §8.12, AB 2460, `wpbca-bylaws-config.json` | 85% regex + 15% LLM | **Session 2** |
| Governance Compliance Check | Davis-Stirling Act, Bylaws full text | LLM-as-judge | Future |
| Election Builder | Bylaws §5.9, §8.12, §8.14, Civil Code §5100-5145 | Pattern + LLM | Future |
| Archive Intake | Chain of custody rules, document classification | Pattern | Future |
| Parcel Resolver | Bylaws §5.2, APN database, combined lot rules | Binary | Future |

---

## Layer 2b: Canary (Loss Prevention)

Source material: LP Dashboard Pattern Catalog (52 patterns), Chirp rule definitions
(29 rules), Square API docs, PCI-DSS requirements, SDDs (16 documents).

### Existing Skills (14)

| Skill | File | Purpose | Eval Type |
|-------|------|---------|-----------|
| Canary Preflight | `canary-preflight.md` | Delegates to factory + stack health, env, tunnel | Binary |
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

### Planned Skills

| Skill | Source Material | Eval Type | Priority |
|-------|----------------|-----------|----------|
| Rule Tuning | Chirp rule definitions, threshold config | Binary + LLM | Future |
| Merchant Onboarding | Square OAuth flow, data pipeline docs | Binary | Future |
| Evidence Package | Fox case workflow, hash-chain export | Binary | Future |
| Weekly Money Report | Owl the_one_thing, narrative patterns | LLM-as-judge | Future |
| Detection Pattern Design | LP Pattern Catalog, Chirp rules | Pattern + LLM | Future |

---

## Layer 3: Shared Memory (ALX)

Source material: Memory bus service (`services/memory-bus/`), ALX session patterns,
cross-app knowledge base.

### Existing Skills (5)

| Skill | File | Purpose | Eval Type |
|-------|------|---------|-----------|
| GitNexus | `gitnexus.md` | Code intelligence queries | Binary |
| Session Synthesis | `session-synthesis.md` | Chat transcript → structured doc | Pattern |
| File Guardian | `file-guardian.md` | Protected file modification gate | Binary |
| Jeffe Review | `jeffe-review.md` | CEO-level plan review | LLM-as-judge |
| Founder Probe | `founder-probe.md` | Biographical depth via follow-up probes | LLM-as-judge |

### Planned Skills

| Skill | Source Material | Eval Type | Priority |
|-------|----------------|-----------|----------|
| Context Assembly | Memory bus `context_assemble` tool, session patterns | Pattern | Session 3 |
| Knowledge Gap Detection | Task requirements vs. available memories | LLM-as-judge | Future |
| Post-Mortem Capture | Factory close patterns, lesson extraction | Pattern | **Session 3** |
| Prior Art Search | Memory bus `memory_recall`, GitNexus queries | Binary | Future |

---

## Eval Strategy

Every skill gets an eval suite before deployment. Target: 90%+ pass rate.

### Eval Types

| Type | Method | When to Use |
|------|--------|-------------|
| **Binary** | Pass/fail assertions (subprocess exit codes, file existence, regex match) | Infrastructure checks, build gates, data validation |
| **Pattern** | Regex matching on output (required sections, correct formats, expected values) | Structured output skills (blueprints, reports, taxonomies) |
| **LLM-as-judge** | Claude evaluates output against domain criteria | Compliance reasoning, narrative quality, domain expertise |

### Ratio Guideline

- Infrastructure/build skills: 100% binary
- Structured output skills: ~85% pattern + ~15% LLM-as-judge
- Domain reasoning skills: ~50% pattern + ~50% LLM-as-judge

### Eval File Convention

```
evals/
  skills/
    test_platform_preflight.py     # Layer 1 eval
    test_quorum_calculator.py      # Layer 2a eval
    test_post_mortem_capture.py    # Layer 3 eval
    conftest.py                    # Shared fixtures
```

Each eval file contains:
- `test_*` functions with binary pass/fail assertions
- Optional `eval_*` functions for LLM-as-judge checks
- Docstring citing source material for each test

---

## Pipeline Per Skill

Adapted from George Nurijanian's 7-step process:

1. **Load source material** — bylaws PDF, CLAUDE.md, SDDs, archive docs
2. **Extract operational knowledge** — rules, thresholds, decision criteria, worked examples
3. **Wire to build environment** — memory bus `memory_recall` + Linear documents as query layer
4. **Scaffold the skill** — `skill-creator` tool with frontmatter, modes, templates
5. **Design evals** — binary pass/fail + regex pattern matching + LLM-as-judge
6. **Run evals, fix, iterate** — unattended optimization loop
7. **Validate against source** — cross-check outputs against original domain material

Key insight: **"The extraction step determines the ceiling."** Skills built from
operational source material (bylaws text, LP patterns, Chirp rules) will always
outperform skills built from CLAUDE.md summaries.

---

## Manifest Integration

`factory-manifest.json` declares which skills are required per stage. Current state
maps stages to skill files. Target state adds:

```json
{
  "stages": {
    "preflight": {
      "skill": "factory-preflight",
      "eval": "evals/skills/test_platform_preflight.py",
      "eval_threshold": 1.0
    }
  }
}
```

Each stage entry gains:
- `skill` — skill file reference
- `eval` — eval suite path
- `eval_threshold` — minimum pass rate (0.0–1.0)

---

## Memory Tagging

All memory writes tagged by layer:

| Layer | Tag | Example |
|-------|-----|---------|
| Corp | `corp` | Platform standards decisions, factory process changes |
| Cove | `cove` | Governance compliance findings, bylaws interpretations |
| Canary | `canary` | LP pattern discoveries, Chirp rule tuning results |
| Shared | `shared` | Cross-app patterns, agent topology decisions |

Memory bus `memory_store` already supports the `layer` parameter. Skills use it
at close to tag their outputs correctly.

---

## Inventory Summary

| Layer | Existing | Planned | Total |
|-------|----------|---------|-------|
| Corp (DOA) | 11 | 5 | 16 |
| Cove | 8 | 5 | 13 |
| Canary | 14 | 5 | 19 |
| Shared (ALX) | 5 | 4 | 9 |
| **Total** | **38** | **19** | **57** |

*Note: 4 additional utility skills (remember-quote, rooster, project-timelog, cove-archive)
exist but are not part of the factory pipeline.*
