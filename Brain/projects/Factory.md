---
type: project-moc
status: operational
classification: internal
owner: GrowDirect LLC
tags: [factory, method, pipeline, growdirect-method, orchestration]
---

# Factory

The 9-stage pipeline GrowDirect agents use to take a Linear issue from intake to ship. Declared in [[factory-manifest.json]], implemented by [[.claude/skills/|factory-* skills]], specified in [[docs/sdds/platform/factory-pipeline|Factory Pipeline SDD]].

## The pipeline

```
preflight → research → blueprint → tdd → assembly → verify → qa → ship → close
```

Each stage consumes the prior stage's output. A stage that can't proceed stops and reports.

## Stages — full matrix

| # | Stage | Input | Output | Skill | Primary Role | Assist Roles |
|---|---|---|---|---|---|---|
| 1 | **Preflight** | GRO issue | `preflight_report` | [[.claude/skills/factory-preflight\|factory-preflight]] | [[Canary/docs/profiles/ops/ALX\|ALX]] | [[Canary/docs/profiles/ops/Eva\|Eva]] (program), [[Canary/docs/profiles/ops/Jeremy\|Jeremy]] (infra checks) |
| 2 | **PhD** | GRO issue + preflight | `context_bundle` | [[.claude/skills/factory-research\|factory-research]] | [[Canary/docs/profiles/ops/Research\|Research]] | [[Canary/docs/profiles/ops/Tom\|Tom]] (arch), [[Canary/docs/profiles/ops/Jess\|Jess]] (docs) |
| 3 | **Blueprint** | GRO + preflight + context | `docs/plans/{date}-{slug}.md` | [[.claude/skills/factory-blueprint\|factory-blueprint]] | [[Canary/docs/profiles/ops/Tom\|Tom]] (architect) | [[Canary/docs/profiles/ops/ALX\|ALX]], [[Canary/docs/profiles/ops/Eva\|Eva]] |
| 4 | **TDD** | Plan | `tests/` (failing, one per behavior) | — | [[Canary/docs/profiles/ops/Jeremy\|Jeremy]] | [[Canary/docs/profiles/ops/Tom\|Tom]] |
| 5 | **Assembly** | Plan + failing tests | Implementation (one commit per task) | [[.claude/skills/factory-assembly\|factory-assembly]] | [[Canary/docs/profiles/ops/Jeremy\|Jeremy]] (builder) | [[Canary/docs/profiles/ops/Tom\|Tom]], [[Canary/docs/profiles/ops/Art\|Art]] (UI) |
| 6 | **Verify** | Implementation | `verify_report` (test counts, regressions, migrations) | — | [[Canary/docs/profiles/ops/Jeremy\|Jeremy]] | [[Canary/docs/profiles/ops/Jim\|Jim]] (customer-sentiment QA) |
| 7 | **QA** | Verify report | `qa_report` (routes, compliance, standards) | [[.claude/skills/factory-qa\|factory-qa]] | [[Canary/docs/profiles/ops/Compliance\|Compliance]] | [[Canary/docs/profiles/ops/Legal\|Legal]], [[Canary/docs/profiles/ops/Art\|Art]] |
| 8 | **Ship** | QA report | `git_push` + `linear_update` | [[.claude/skills/factory-ship\|factory-ship]] | [[Canary/docs/profiles/ops/Jeremy\|Jeremy]] | [[Canary/docs/profiles/ops/DevOps\|DevOps]] |
| 9 | **Close** | Shipped state | `session_summary` + memory writes | [[.claude/skills/factory-close\|factory-close]] | [[Canary/docs/profiles/ops/ALX\|ALX]] | [[Canary/docs/profiles/ops/Eva\|Eva]], [[Canary/docs/profiles/ops/Jess\|Jess]] |

## App-specific variants

Each app overrides stages where it needs domain guardrails. Base factory skill is the contract; app skill adds specifics.

- **Canary** — [[.claude/skills/canary-preflight|canary-preflight]], [[.claude/skills/canary-blueprint|canary-blueprint]], [[.claude/skills/canary-tdd|canary-tdd]], [[.claude/skills/canary-assembly|canary-assembly]], [[.claude/skills/canary-verify|canary-verify]], [[.claude/skills/canary-qa|canary-qa]], [[.claude/skills/canary-ship|canary-ship]], [[.claude/skills/canary-close|canary-close]], [[.claude/skills/canary-data-expansion|canary-data-expansion]], [[.claude/skills/canary-debug|canary-debug]], [[.claude/skills/canary-deploy|canary-deploy]], [[.claude/skills/canary-review|canary-review]], [[.claude/skills/canary-scenario|canary-scenario]], [[.claude/skills/canary-uat|canary-uat]]
- **Cove** — [[.claude/skills/cove-archive|cove-archive]] (currently narrow scope; other stages pending)
- **Cross-app** — [[.claude/skills/factory-linear|factory-linear]], [[.claude/skills/factory-newapp|factory-newapp]], [[.claude/skills/factory-postmortem|factory-postmortem]]

## Work Products produced by the Factory

Every stage writes an artifact. The artifacts themselves live in Git + Linear, but their **templates** are documented:

- Linear issue (intake format) — no template yet; candidate for [[Brain/templates/|Brain templates]]
- `preflight_report` — stage skill defines format
- `context_bundle` — stage skill defines format
- Plan — [[docs/superpowers/plans/|recent plans]] + brainstorm-driven structure from `superpowers:writing-plans`
- Test files — TDD convention (one test per behavior)
- Code + commit — standard git
- `verify_report` — stage skill defines format
- `qa_report` — stage skill defines format
- `session_summary` — [[.claude/skills/factory-close|factory-close]] defines format

## Roles that interact with the Factory

All roles defined in `Canary/docs/profiles/ops/`. See [[Brain/method/Roles|Method › Roles]] for the role index.

Primary runners: [[docs/team/ALX|ALX]] (orchestration), [[docs/team/Architect|Architect]] (architecture), [[docs/team/Engineer|Engineer]] (build + DevOps), [[docs/team/Compliance|Compliance]] (QA).
Support: [[docs/team/ProgramManager|ProgramManager]] (program), [[docs/team/Writer|Writer]] (docs), [[docs/team/UX|UX]] (UX), [[docs/team/QA|QA]] (sentiment), [[docs/team/Owl|Owl]] (AI), [[docs/team/PhD|PhD]] (context).
Gates: [[docs/team/Legal|Legal]], [[docs/team/Compliance|Compliance]], [[docs/team/DevOps|DevOps]].

## Technique library (skills) used inside stages

Factory stages call into domain skills from installed plugins:

- **superpowers** — brainstorming, writing-plans, executing-plans, subagent-driven-development, test-driven-development, systematic-debugging, verification-before-completion, requesting-code-review, using-git-worktrees, finishing-a-development-branch, writing-skills
- **engineering** — architecture, code-review, debug, deploy-checklist, documentation, incident-response, system-design, tech-debt, testing-strategy, standup
- **brand-voice** — discover-brand, generate-guidelines, enforce-voice
- **legal** — review-contract, compliance-check, triage-nda, legal-response, legal-risk-assessment, signature-request, vendor-check, meeting-briefing, brief
- **marketing** — campaign-plan, content-creation, draft-content, email-sequence, brand-review, competitive-brief, performance-report, seo-audit
- **enterprise-search** — search, digest, knowledge-synthesis, search-strategy, source-management
- **rpv-permit-architect** — archive-navigator, rpv-building-codes, drawing-set-planner, project-history, cost-estimating, sketchup-guide
- **claude-api** — Claude API / SDK best practices
- **anthropic-skills** — pdf, docx, xlsx, pptx, setup-cowork, consolidate-memory, skill-creator, schedule

See [[Brain/method/Techniques|Method › Techniques]] for the full technique index.

## Pipeline controls

- **Preflight gate** — Docker + Linear MCP must be up, GRO issue must exist, git clean. Factory refuses to start otherwise.
- **Plan gate** — max 8 tasks per plan, enforced in blueprint stage.
- **TDD gate** — failing tests must exist before assembly.
- **Verify gate** — regressions fail the pipeline.
- **QA gate** — compliance + standards check fails the pipeline.

## Related

- [[docs/sdds/platform/factory-pipeline|Factory Pipeline SDD]] — authoritative spec
- [[docs/sdds/platform/skill-architecture|Skill Architecture SDD]] — how skills compose
- [[docs/sdds/platform/memory-bus|Memory Bus SDD]] — session persistence
- [[factory-manifest.json|factory-manifest.json]] — machine-readable pipeline definition
- [[Brain/projects/Method|Method MOC]] — parent navigation for Factory + adjacent methods
- [[Brain/method/Models|Method › Models]] — other methods (brainstorm, brand-voice, legal flows)

## Future work

- Add explicit `Produces` / `Uses` / `Performs` frontmatter to each role profile (Sprint B of the Method initiative)
- Tag skills with `roles:` frontmatter so role → technique cross-reference surfaces in queries (Sprint C)
- Pipeline evals beyond preflight (`eval_threshold: 1.0` is defined only for preflight today)
- Tag Brain templates with `stage:` and `role:` so WP → stage cross-reference surfaces
