---
date: 2026-04-23
type: design-spec
status: draft
classification: confidential
owner: GrowDirect LLC
tags: [cto-readiness, audit, security, brand-voice, factory, cleanup]
---

# CTO-Readiness Audit — Design Spec

## Context

GrowDirect is preparing to share Canary and selected GrowDirect platform
components with a technical co-founder / CTO-type partner under NDA or
access acknowledgment, with first disclosure expected in the week of
2026-04-28.

The work to date has been AI-accelerated across every surface — code,
architecture docs, Brain knowledge. This is credible engineering output
but produces predictable hygiene issues: AI-voice commentary,
placeholder TODOs, half-baked stubs, and drift between documentation
and code. Separately, Brain accumulated sensitive material from prior
client engagements (retail loss-prevention work) that cannot travel
with a shared codebase.

The audit establishes a defensible, honest, confidence-backed state
before external eyes arrive. It is a hygiene and scoping pass, not a
feature-development or scale-hardening pass.

## Goal

Put Canary and the SHOW-scoped GrowDirect platform in a state where a
technical co-founder can read the code, architecture docs, process
artifacts, and scale-honesty story, form a real opinion of the
engineering work, and see exactly where gaps are by design and where
gaps are by roadmap — with no sloppy surface area, no sensitive
material leaking, and no AI-generated artifacts embarrassing the
operation.

## Success Criteria

All must be true before first CTO-partner access is granted:

1. Zero `TODO`, `FIXME`, `XXX`, `HACK`, `WIP`, `NOCOMMIT`, `TEMP`,
   `DEBUG` markers in SHOW scope. Each resolved, converted to a Linear
   issue reference, or converted to a thoughtful future-proofing stub
   (see Conservative Cleanup Philosophy).
2. Zero sloppy stub functions. Thoughtful stubs permitted only when
   they pass the five-point thoughtfulness test.
3. Zero AI-voice commentary in code or docs. No apologetic tone, no
   celebratory emoji, no preserved chat artifacts, no patterns listed
   in the Audit Dimensions table.
4. Zero client names, personal names, or sensitive project references
   in SHOW scope — including but not limited to prior retail LP
   clients, consulting engagements, current client-adjacent projects
   (Cove, Angel, Seacove), and the private HOA / Foundation work.
5. Every SHOW-scope source file carries a GrowDirect LLC
   confidentiality header (code) or frontmatter fields (markdown —
   both `classification` and `owner`). Every SHOW-scope repo carries
   `NOTICE.md`, `ACKNOWLEDGMENT.md`, and `SECURITY.md` at root.
6. An enterprise-scale gap analysis exists per scope, documenting what
   we have, what the enterprise bar requires, and the honest delta —
   distinguishing gaps-by-roadmap from choices-by-design. Written
   without naming any specific prior-client reference material.
7. Git state is clean. No loose files at repo roots. No uncommitted
   intent on main. No stale AI-agent-generated branches. Every SHOW'd
   repo's remote, default branch, and visibility are verified.
8. A minimum-viable Brain scope split has carved the Canary App Brain
   (and the Platform-supporting Brain) into the surfaces that travel
   with their respective repos, leaving all sensitive and off-scope
   Brain content in the existing GrowDirect/Brain/ vault (implicitly
   Personal/Ops for now).
9. A repo-sharing matrix documents which repos get access, under what
   instrument, excluding what content.
10. Security audit has run: dependency vulnerability scan, SAST, full
    git-history secret scan, container/image scan, and a structured
    OWASP Top 10 code-level review. Findings are either resolved or
    documented with disposition. **Committed secrets are a special
    case: any secret discovered in git history must be rotated AND
    purged from history (BFG or `git filter-repo`) before first
    partner access is granted. "Documented" is not a sufficient
    disposition for a committed secret.**
11. A dry-run "cold CTO reader" verification pass has passed without
    regressions.

### Non-goals for this work

Explicitly out of scope for this week — each is its own separate
future session:

- Full hierarchical Personal/Ops/Platform/App Brain restructure.
- Full enterprise-lineage narrative document (the sanitized forward
  story connecting prior retail LP experience to Canary).
- Closing the Kroger-benchmark scale gaps. This work *documents* them
  honestly; it does not *close* them.
- Feature development or refactoring beyond audit-findings-driven
  cleanup.
- Third-party human penetration testing. The automated + code-level
  security review substitutes for the hygiene pass; formal pen test is
  deferred to commercial-engagement time.

## Scope

### SHOW scope (what the CTO partner may see under NDA or acknowledgment)

| Artifact | Path |
|---|---|
| Canary app | `Canary/` (separate repo, remote `growdirectprez/canary` post-rename — see Resolved Naming Decisions) |
| Shared devops | `GrowDirect/devops/` |
| Platform services | `GrowDirect/services/` |
| Content engine | `GrowDirect/content-engine/` |
| GrowDirect platform plugin | `GrowDirect/growdirect-platform.plugin/` |
| Canary App Brain + Platform-supporting Brain (scoped — see Brain MVP Split) | split from `GrowDirect/Brain/` |
| Platform SDDs | `GrowDirect/docs/sdds/canary/`, `docs/sdds/platform/`, `docs/sdds/alx/` |
| Platform-scoped specs and plans (post-split) | `GrowDirect/docs/superpowers/specs/` and `docs/superpowers/plans/` — non-Canary-scoped entries only |
| Repo-root standards files | `NOTICE.md`, `ACKNOWLEDGMENT.md`, `SECURITY.md`, `CONTRIBUTING.md`, `CLAUDE.md`, `README.md` per SHOW'd repo |

### HIDE scope (explicitly excluded — canonical list)

The following are excluded from every SHOW artifact. This list is the
canonical exclusion set; the Brain MVP Split section's "Explicitly
excluded" list must remain consistent with this list.

- Marketing site: `~/growdirectprez.github.io/`
- Cove: `GrowDirect/Cove/`, `Brain/wiki/cove-*`, `Brain/projects/Cove.md`, `docs/sdds/cove/`
- Angel: `GrowDirect/Angel/`, `Brain/wiki/angel-*`, `Brain/projects/Angel.md`, `docs/sdds/angel/`
- Seacove: `GrowDirect/Seacove/`, `Brain/projects/Seacove.md`, `docs/sdds/arc/` (Seacove-related)
- ownpalosverdes: `GrowDirect/ownpalosverdes/`, Brain content
- Private: `GrowDirect/private/`
- Prior retail LP IP: all `Brain/wiki/secure-*`, `Brain/projects/Secure.md`, external NAS archive
- Linear (entirely — roadmap stays external)
- Raw intake: `Brain/raw/inbox/` (all 119 files)
- Personal operational Brain: timelogs, sales cards, team cards (`Brain/wiki/growdirect-timelog-*`, `growdirect-sales-*`, `Brain/wiki/canary-sales-strategy.md`, `Brain/wiki/growdirect-sales-square-opportunity.md`, team cards)
- Foundation / HOA: `Brain/wiki/*dao*`, `Brain/wiki/*wpbca*`, Foundation three-entity material, ocean-easement content, reactivation-blitz content
- Archives: `docs/_archive/` (all)
- Non-Canary-non-Platform dispatches: `docs/superpowers/dispatches/` entries not Canary-scoped or Platform-scoped
- All Cove/Angel/Seacove/ownpv `.claude/skills/` entries

### Case-by-case access

SHOW items can be granted individually per partner. Access is granted
only after the partner acknowledges the access terms via reply-to-email
with the contents of `ACKNOWLEDGMENT.md` (Mechanism 1, see Standards).

## Audit Dimensions

The dispatched audit subagent checks every SHOW-scope file and repo
against these dimensions. Each finding records: file path, line
number, exact offending text, severity, and recommended action.

### General dimensions

| Dimension | Trigger | Severity |
|---|---|---|
| Unresolved markers | `TODO`, `FIXME`, `XXX`, `HACK`, `WIP`, `NOCOMMIT`, `TEMP`, `DEBUG`, committed `console.log`, committed `print(` debug | **HIGH** |
| Sloppy stubs | Function body is `pass`, `...`, bare `NotImplementedError`, returns placeholder, no docstring, docstring says "TODO: implement" | **HIGH** |
| AI-voice commentary | `# Let me think`, `# Here's a great`, `# Actually,`, `# I'll`, comment-block emoji, apologetic tone, `# Note that`, `# Certainly`, `# Of course`, `# Great question`, verbose explanation of obvious code, preserved chat fragments | **HIGH** |
| Orphan code | Functions, classes, files with no callers. Dead imports. Commented-out code blocks longer than three lines | **MEDIUM** — default action: remove |
| Client / personal / sensitive names | Prior-client names, personal names from prior engagements, current adjacent-project names, specific addresses, sandbox credentials or IDs, merchant-specific PII | **CRITICAL** — any hit stops the show until scrubbed |
| Confidentiality markings missing | Source files without GrowDirect LLC header; markdown without `classification: confidential` + `owner: GrowDirect LLC` frontmatter; repos without root `NOTICE.md` / `ACKNOWLEDGMENT.md` / `SECURITY.md` | **HIGH** |
| SDD ↔ code drift | SDDs referencing features/endpoints/modules that don't exist in the codebase (search-verifiable); `factory-manifest.json`-listed modules without a corresponding SDD entry; frontmatter `last-compiled` older than 30 days | **MEDIUM** — document in report, don't try to close drift this week |
| Doc quality | Empty sections, Lorem-ipsum placeholders, unresolved template brackets, `[TBD]`, `[TODO]`, broken internal links | **HIGH** |
| Factory-process compliance | Code lacking SDD ancestry, specs without implementation plans, plans without execution evidence | **MEDIUM** — gap documented honestly |
| Configuration hygiene | Hardcoded URLs / API keys / tokens, `DEBUG = True` in committed config, missing `.env.example`, `pdb.set_trace()` in committed code | **HIGH** |
| Test coverage surface | Per-module existence of tests (presence, not coverage percentage). Integration tests use real database fixtures (no DB mocking) — this is a project-level rule rooted in prior mock-divergence incident; codify in `CONTRIBUTING.md` during cleanup | **LOW/MEDIUM** — document gap, don't try to close this week |

### Security dimensions — automated

| Tool | Target | Finds |
|---|---|---|
| `pip-audit` | `requirements.txt`, `requirements-dev.txt` | Python dependency CVEs |
| `bandit` | All `.py` in SHOW scope | Python SAST — hardcoded secrets, SQL injection, weak crypto, insecure deserialization, shell injection |
| `semgrep` with `p/python`, `p/flask`, `p/owasp-top-ten`, `p/jwt` rulesets | All Python + JS | Framework-specific anti-patterns, auth flaws |
| `gitleaks` | Full git history per repo | Secrets committed at any point |
| `trufflehog` | Full git history per repo | Secondary secret scan |
| `trivy` | Docker images + `devops/` configs | Container CVEs, compose misconfigurations |
| `npm audit` | Any `package.json` in SHOW scope | Node dependency CVEs |

Tools are installed into the dispatch environment (`uvx` / `pipx` /
`brew` / `go install`), not into the app's dependency tree. No changes
to `requirements.txt` or `package.json`.

### Security dimensions — manual / subagent-led

| Area | Checked for |
|---|---|
| **OWASP Top 10 (2021)** | Per-endpoint authz check, password hashing, token entropy / expiration / one-time-use, parameterized queries, Flask debug off in prod, cookie flags, magic-link flow, session fixation, Square OAuth state param, webhook signature verification, integrity checks, logging adequacy, SSRF |
| **Multi-tenant isolation** | Every DB query scoped to tenant. No unscoped queries. Session state can't leak. Async jobs carry tenant context |
| **Auth flows** | Magic link token entropy + expiration + one-time-use. Password path algorithm (PBKDF2 / bcrypt / argon2). Session storage in Valkey with sane TTL. Square OAuth state + token storage |
| **Webhook handling** | Signature verification, replay protection, idempotency |
| **Data handling** | PII inventory, no PII in logs, audit log for admin actions, no real PII in test fixtures |
| **Infra config** | Postgres / Valkey / Ollama not internet-exposed, `.env` files correctly gitignored AND absent from history, containers run non-root where possible, prod vs dev config distinct |
| **Dependency freshness** | Packages > 12 months behind or end-of-life flagged |
| **Rate limiting** | Auth and API endpoints have rate limits; gaps documented |
| **Security headers** | CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy |

## Conservative Cleanup Philosophy

Default decisions when on the fence.

**1. Branch everything.** All cleanup lives on
`chore/cto-readiness-audit-2026-04-23` on each repo. Nothing merges to
main until the user explicitly approves.

**2. Scale back over polish-in-place.** When a function, module, or
doc looks half-baked, the default is one of:
- Remove (if no caller depends on it).
- Feature-flag off (default-disabled) if half-wired.
- Convert to a thoughtful stub per Rule 3 if the interface shape is
  worth preserving as a future-proofing signal.

Never "try to make it better." Conservation means if it can't be told
straight, don't show it.

**3. Thoughtful-stub five-point test.** A stub passes iff all five:
- Named interface with explicit types / signature.
- Docstring stating what the function does (present tense, declarative).
- `# Future:` comment with single-sentence rationale.
- `NotImplementedError` with human-readable message including a Linear
  issue reference.
- The rationale is defensible on a cold read — "this is the seam for
  X, which lands in Y phase" — not "future feature."

If all five, keep. Otherwise, Rule 2.

**4. TODO disposition.** Three outcomes:
- Resolve: do the thing, remove the comment.
- Convert: create Linear issue, replace TODO with `# See GRO-NNN`.
- Remove: delete silently if no longer relevant.

**5. No silent surprise-refactoring.** Audit finds findings. Cleanup
fixes those findings. Nothing else. Unrelated improvements get logged
as separate findings; the current pass does not touch them.

**6. Subagents don't merge.** Cleanup subagent produces a branch and a
cleanup report. The user reviews and merges. Every change traces to an
audit-dimension finding.

**7. Judgment calls surface to user.** Subagent produces a `##
Judgment Calls` section for items it won't decide unilaterally. User
decides; subagent executes in a follow-up pass.

**8. Preserve git history.** No `rebase -i`, no `filter-repo`. One
exception: if the security scan finds a committed secret, history
rewrite is mandatory for that secret, run as its own workstream with
user sign-off.

**9. Don't add features. Don't refactor for cleanliness.** Hygiene
only. The audit prompt will enforce scope strictly.

## Kroger Benchmark — Enterprise Scale Gap Analysis

The audit produces one file per SHOW scope:
`<repo>/docs/audit-2026-04-23/enterprise-scale-gap-analysis.md`.

Dimensions compared (enterprise bar is phrased generically — no client
names in artifacts):

| Dimension | Enterprise bar |
|---|---|
| Aggregate transaction volume | Tens of millions of POS transactions per day across the customer base, TB-scale repository |
| Per-tenant transaction volume | Thousands of transactions per store per day, continuous ingest |
| Data-model abstraction | Stable schema contract between raw heterogeneous POS data and detection/case layer |
| Persistence decomposition | Logically separate stores for sales data, cases, users, hierarchies, reporting, job system |
| Identity federation | SAML 2.0 + OpenID Connect, role mapping via assertions, both self-service and admin-assigned role paths |
| Deployment redundancy | Tiered: non-redundant → single-DC-redundant → cross-DC |
| Self-host / VPC option | Enterprise customers expect the option |
| Data retention tiering | Detail window + aggregated-metrics window |
| Opinionated defaults | Pre-wired install, not a kit of parts |
| Rule tuning for retailer patterns | Per-customer tunable rule engine |
| Delivery organization scale | Enterprise-tier deployments (6-figure first-year subscription, 4–6 month implementation windows) vs SMB self-serve — state Canary's positioning |
| Adjacent-module pricing | Core product plus adjacent modules at independent pricing |

Writing rules:
- State what exists concretely (code paths, schemas, endpoints).
- State the enterprise bar in generic terms. No prior-client names.
- State the honest gap. No hand-waving. Either roadmap quarter or
  "out of scope by design because [reason]."
- Explicitly separate GAP from CHOICE. SMB-first SaaS with magic-link
  auth is a choice, not a deficiency.

The gap analysis is the single most credibility-building artifact in
the review.

## Brain MVP Split

Minimum restructure to scope the Canary App Brain and the
Platform-supporting Brain for this meeting. Full hierarchical
Personal/Ops/Platform/App rework is a separate session.

### Moves — from GrowDirect/Brain + GrowDirect/docs into Canary repo

Canary MOC, Canary wiki (architecture, data-model, detection,
platform-overview), GrowDirect-flagged Canary wiki
(`growdirect-canary`, `growdirect-the-chirp`, `growdirect-the-fox`,
`growdirect-chirp-udq-strategy` — after content check), Canary SDDs
(21 files in `docs/sdds/canary/`), Canary-scoped specs and plans in
`docs/superpowers/`, the April 22 demo-reseed dispatch.

Destination: `Canary/brain/wiki/`, `Canary/brain/projects/`,
`Canary/docs/sdds/`, `Canary/docs/superpowers/`.

Mechanics: `git mv` preserves in-repo history in GrowDirect. Canary
receives fresh file history — acceptable for MVP; original provenance
remains queryable in GrowDirect. Subtree-split to preserve full history
across repos is deferred.

### Stays in GrowDirect — Platform-supporting Brain (SHOW)

Platform method MOC (`Brain/projects/Method.md`), Factory MOC
(`Brain/projects/Factory.md`), GrowDirect platform MOC
(`Brain/projects/GrowDirect.md`), `Brain/method/` (7 files),
factory-process wiki, `docs/sdds/platform/`, `docs/sdds/alx/`, factory
skills in `.claude/skills/factory-*` (5 files). Canary factory skills
in `.claude/skills/canary-*` (14 files): decision on whether to move
into Canary repo or keep centralized — defaulted to keep centralized
for MVP (see Open Question 1).

### Explicitly excluded from SHOW — stays in GrowDirect/Brain/ as implicit Personal/Ops

This is a restatement. The canonical exclusion set is the HIDE scope
in the Scope section above. Any divergence is a bug in this spec and
the Scope section's HIDE list wins.

- `Brain/wiki/secure-*.md` (6 files), `Brain/projects/Secure.md`
- All Cove / Angel / Seacove / WPBCA / Foundation / DAO / ownpv
  material across `Brain/wiki/` and `Brain/projects/`
- Timelog / sales / team cards: `Brain/wiki/growdirect-timelog-*`,
  `Brain/wiki/growdirect-sales-*`, `Brain/wiki/canary-sales-strategy.md`,
  `Brain/wiki/growdirect-sales-square-opportunity.md`, team cards
- Foundation / HOA: `Brain/wiki/wpbca-*`, `Brain/wiki/coac-*`, 
  `Brain/wiki/growdirect-dao-*`, reactivation-blitz content,
  ocean-easement content
- `Brain/raw/inbox/` (119 files — raw prior-client material)
- `docs/sdds/cove/`, `docs/sdds/angel/`, `docs/sdds/arc/` (Seacove)
- `docs/_archive/`
- Non-Canary, non-Platform `docs/superpowers/dispatches/`

### Obsidian linking

Canary's `brain/` becomes its own vault (has its own `.obsidian/`).
Wikilinks inside Canary resolve locally. Links from platform wiki to
Canary-scoped wiki break post-move; link hygiene pass runs via
`mcp__obsidian__find_broken_links_tool` and cleans up.

### Optional founder view-shell (post-MVP)

A `~/views/founder/` shell vault symlinking all scope vaults into one
workspace, opened daily by the founder, never shared. Mentioned for
completeness; not blocking for this meeting.

## Git and Repo Hygiene

### Current-state triage — executed at start of cleanup dispatch

Ranked by blast radius. Non-destructive items completed at end of
design session (2026-04-23).

| # | Finding | Action | Status |
|---|---|---|---|
| 1 | Loose `dispatch-code-2026-04-22-demo-reseed.md` at GrowDirect root | `git mv` to `docs/superpowers/dispatches/2026-04-22-demo-reseed.md` (interim home; final home is Canary) | Completed |
| 2 | `.obsidian/workspace.json`, `graph.json`, `app.json`, `appearance.json` tracked, leaking user-local state | Added to `.gitignore`, `git rm --cached` | Completed |
| 3 | `Brain/projects/Method.md` modified uncommitted | Phantom diff; no-op | N/A |
| 4 | 119 files in `Brain/raw/inbox/` — mix of ingested markdown and raw prior-client binaries | Personal Brain territory, HIDE from SHOW scope. Triage by user after meeting: process via `engine.py extract` + `ingest`, move to NAS archive, or delete if processed | Deferred |
| 5 | Canary: 6 stale `claude/*` agent-generated branches | Audit each for merged / abandoned / in-flight status; produce per-branch disposition; user approves; delete | In cleanup dispatch |
| 6 | Canary: `gro-386-fix-canary-login-*` branch | Check Linear GRO-386 status; evaluate merge / keep / delete | In cleanup dispatch |
| 7 | Canary: `security/platform-hardening` branch | Evaluate contents. If unmerged security fixes, merge before Phase 2 audit runs so findings reflect current state | Phase 0 bootstrap (pre-audit) |
| 8 | Loose `dispatch-code-2026-04-23-abalonecove-regen.md` at GrowDirect root (created by active session) | Pattern violation — sweep in full cleanup pass | In cleanup dispatch |

### Enduring hygiene standards

**`.gitignore` audit per SHOW'd repo.** Verify exclusions for
`.env`, `__pycache__`, `.pytest_cache`, `node_modules`, `.DS_Store`,
Obsidian user-local state, local admin configs. Executed during
cleanup.

**Secret-in-history check.** `gitleaks` and `trufflehog` run against
full git history. If a secret ever existed, it's still a leak.
Disposition per finding: confirm rotated (benign), or rewrite history.
Rewrite runs as separate workstream with user sign-off.

**Root-level loose-file rule.** No `.md` at repo root except
`README.md`, `CLAUDE.md`, `AGENTS.md`, `NOTICE.md`, `ACKNOWLEDGMENT.md`,
`SECURITY.md`, `CONTRIBUTING.md`, `LICENSE` (if applicable). Codified
in `CONTRIBUTING.md`.

**Branch hygiene rule.** Working branches named by type: `feat/*`,
`fix/*`, `chore/*`, `security/*`, `gro-NNN-*`. AI-agent-generated
random names merged+deleted or evaluated+deleted within 7 days of
creation. Codified in `CONTRIBUTING.md`.

**Repo-remote verification.** Before partner access, per SHOW'd repo:
confirm remote URL, default branch is `main`, branch protection
configuration, no unintended collaborators. `gh repo view --json
visibility,nameWithOwner,defaultBranchRef,collaborators` per repo.

### Repo-sharing matrix — deliverable artifact

Lives at `GrowDirect/docs/repo-sharing-matrix.md`. Template:

| Repo | Classification | Default access | Instrument | Contains | Excluded |
|---|---|---|---|---|---|
| `canary` (renamed in Phase 7 from `growdirect-ops`; GitHub redirect preserves old URLs) | Confidential | SHOW under NDA or acknowledgment | Reply-to-email Mechanism 1 default; formal NDA escalation available | Canary app + Canary brain | Cove, Angel, Seacove, ownpv, Secure, commercial strategy |
| GrowDirect monorepo | Confidential | SHOW under NDA or acknowledgment, scoped view | Same | Shared platform, method, factory, platform-supporting Brain | All HIDE items listed in Scope section |
| `growdirectprez.github.io` | Public | Public | N/A | Marketing site only | N/A |
| Future — Cove, Angel, Seacove, ownpalosverdes | Confidential (separate scope) | HIDE for current CTO partner; separate agreements if ever shown | Separate per scope | Per-project | N/A |

Referenced from each `ACKNOWLEDGMENT.md`. Updated each time access
changes.

## Work Plan and Sequence

Phases with parallel/serial markings. **[P]** = parallel-safe with
other active sessions. **[S]** = serial, requires coordination.

Total wall-clock estimate: ~2.5–3 hours across all subagent phases,
plus user-review gate time between phases. See
`docs/superpowers/plans/2026-04-23-cto-readiness-audit.md` for
dispatch-prompt details (produced by the `writing-plans` skill
invocation after this spec is approved).

### Phase 0 — Finalize design + pre-audit bootstrap [S]

- Write this design spec. (Current step.)
- Run spec-document-reviewer loop; iterate until Approved.
- User reviews spec file.
- Invoke `writing-plans` skill → produces implementation plan with
  dispatchable prompts.
- **Pre-audit bootstrap actions** (before Phase 1 runs):
  - Evaluate Canary's `security/platform-hardening` branch. If it
    contains unmerged security fixes, merge it into `main` (with user
    approval) so the Phase 2 security audit sees current state, not
    stale state. If it's already merged or abandoned, note disposition
    and delete.
  - Verify feature-session landing cadence on SHOW-scope files. Agree
    with user on a cutoff: between Phase 2 (audit) and Phase 4
    (cleanup), feature sessions should either freeze SHOW-scope
    changes, OR the cleanup subagent re-runs the audit-dimension
    check on its own branch immediately before producing its report.
    This cutoff is documented in the plan.

Touches: new spec file; possible `security/platform-hardening`
merge with user approval. Duration: ~30 min.

### Phase 1 — Brain MVP split [S]

Runs before audit so audit sees final structure.

- Per Brain MVP Split section: `git mv` operations move
  Canary-scoped Brain and docs content from GrowDirect repo to
  Canary repo. Platform-supporting Brain stays in GrowDirect.
- Two repo branches:
  - `chore/brain-mvp-split-2026-04-23` in GrowDirect (records removals)
  - `chore/brain-mvp-split-2026-04-23` in Canary (records additions)
- Link hygiene pass across both vaults (resolve or remove broken
  cross-vault wikilinks).
- User reviews both branches, merges to `main` on each repo.

After merge, the repo structure matches what the audit will see.
Duration: ~30 min.

### Phase 2 — Audit dispatch [P — read-only, parallel-safe]

Five parallel subagents fire in a single message:

| Subagent | Scope | Produces |
|---|---|---|
| `canary-audit` | Canary repo (post-split) | `Canary/docs/audit-2026-04-23/canary.md` |
| `platform-audit` | GrowDirect shared platform: `devops/`, `services/`, `content-engine/`, `growdirect-platform.plugin/` | `GrowDirect/docs/audit-2026-04-23/platform.md` |
| `docs-brain-audit` | SHOW-scope docs + Brain (in both repos, post-split) | `GrowDirect/docs/audit-2026-04-23/docs-brain.md` (platform docs/Brain) and `Canary/docs/audit-2026-04-23/docs-brain.md` (Canary docs/Brain) |
| `security-audit` | Cross-cutting; both repos' full git history | `Canary/docs/audit-2026-04-23/security.md` and `GrowDirect/docs/audit-2026-04-23/security.md` + `security-tool-output/` raw results in each repo |
| `enterprise-scale-gap` | Runs after findings summarize; reads audit reports + source material for enterprise bar | `GrowDirect/docs/audit-2026-04-23/enterprise-scale-gap-analysis.md` (sanitized — no prior-client names) |

No source file changes. Duration: 15–30 min wall clock.

### Phase 3 — User reviews audit [S — gate]

User reads reports. Approves cleanup scope. Flags judgment calls.
Confirms or adjusts enterprise-gap framing. Decides dispositions for
committed-secret findings (if any) — either rotate-and-rewrite-history
workstream or "not a real secret" disposition.

### Phase 4 — Cleanup dispatch [P via git worktrees]

Each affected repo gets a worktree on
`chore/cto-readiness-audit-2026-04-23`. Subagents work inside
worktrees; feature sessions continue in primary checkouts untouched.

| Subagent | Worktree | Scope |
|---|---|---|
| `canary-cleanup` | `~/.worktrees/canary-cto-cleanup/` (Canary repo) | TODO/stub cleanup, AI-voice scrub, name scrub, feature-flag sloppy functions, insert confidentiality headers on all Canary code + docs + Canary Brain |
| `platform-cleanup` | `~/.worktrees/growdirect-cto-cleanup/` (GrowDirect repo) | Same dimensions, platform scope: shared code + SHOW-scope docs + Platform-supporting Brain |
| `security-fix` | Separate branch `chore/security-findings-2026-04-23` on each affected repo | Security HIGH/CRITICAL findings, separate branch because rollback characteristics differ; CRITICAL committed-secret findings trigger history-rewrite as own workstream with user sign-off |

Each subagent, before producing its cleanup report, re-runs the
audit-dimension check on the worktree branch and compares against
the Phase 2 baseline. Any new findings introduced by concurrent
feature-session landings get folded into the cleanup scope or flagged
as out-of-scope with user-surface.

Each produces branch + `cleanup-report.md` documenting every file
touched. Subagents do NOT merge — the user reviews and merges in
Phase 5. Duration: 30–60 min.

### Phase 5 — User reviews cleanup branches [S — gate]

Merge order per repo: `chore/cto-readiness-audit-2026-04-23` first,
then `chore/security-findings-2026-04-23` second. The
`chore/brain-mvp-split-2026-04-23` branch was already merged in
Phase 1 and does not appear in this phase. If a history-rewrite is
required (committed-secret case), it runs between the two cleanup
merges as its own workstream.

### Phase 6 — Dry-run cold-reader verification [P]

Single subagent simulates a cold CTO reader. Walks each SHOW'd repo
from README, navigates architecture → code → tests. Verifies:

- `NOTICE.md`, `ACKNOWLEDGMENT.md`, `SECURITY.md` at root.
- No TODOs / stubs / AI-voice residue.
- Client-name scrub clean.
- Confidentiality markings on all files.
- Cross-doc links resolve.
- Enterprise-gap analysis reads defensibly.

Produces `Canary/docs/audit-2026-04-23/ready-to-show-confirmation.md`
and `GrowDirect/docs/audit-2026-04-23/ready-to-show-confirmation.md`
— each either PASS or a regression list that needs one more cleanup
pass.

### Phase 7 — Ready-to-share state [S]

- Tag `cto-review-ready-2026-04-23` on each repo.
- Execute Canary repo rename: `growdirectprez/growdirect-ops` →
  `growdirectprez/canary` (GitHub preserves redirects).
- `contact@growdirect.io` and `security@growdirect.io` receive mail
  (Fastmail setup — user action).
- Repo-sharing matrix finalized.
- User sends access-grant email with `ACKNOWLEDGMENT.md` link.

## Artifacts Produced

### Design-time

- This spec: `docs/superpowers/specs/2026-04-23-cto-readiness-audit-design.md`
- Plan: `docs/superpowers/plans/2026-04-23-cto-readiness-audit.md`
- Audit prompt: `docs/superpowers/dispatches/2026-04-23-cto-readiness-audit.md`
- Cleanup prompt: `docs/superpowers/dispatches/2026-04-23-cto-readiness-cleanup.md`

### Audit-time (under `docs/audit-2026-04-23/` in each SHOW'd repo)

- `canary.md`, `platform.md`, `docs-brain.md` — findings by scope
- `security.md` + `security-tool-output/` with raw tool results
- `enterprise-scale-gap-analysis.md`
- `ready-to-show-confirmation.md`

### Cleanup-time

- Branches: `chore/cto-readiness-audit-2026-04-23`,
  `chore/security-findings-2026-04-23`,
  `chore/brain-mvp-split-2026-04-23` per affected repo
- `cleanup-report.md` per branch

### Enduring (new baseline)

- `NOTICE.md`, `ACKNOWLEDGMENT.md`, `SECURITY.md` at each SHOW'd
  repo root
- Confidentiality markings on every SHOW'd source file + markdown
- Updated `.gitignore` per repo
- `docs/standards/confidentiality-markings.md` — canonical standards
- `docs/repo-sharing-matrix.md` — living access document
- `CONTRIBUTING.md` — branch hygiene + loose-file rules
- `Canary/brain/` directory — the Canary App Brain
- Git tags: `cto-review-ready-2026-04-23` per repo

### Operational

- `contact@growdirect.io` and `security@growdirect.io` receiving mail
- Access-grant email template

## Standards — confidentiality markings and repo-root files

These standards also live at
`docs/standards/confidentiality-markings.md` as a canonical reference.

### Code file header (two lines at top of every SHOW'd source file)

```
# GrowDirect LLC — Confidential & Proprietary
# Copyright (c) 2026 GrowDirect LLC. All rights reserved.
```

(Equivalent comment syntax per language.)

### Markdown frontmatter (every SHOW'd `.md` file)

```yaml
---
classification: confidential
owner: GrowDirect LLC
---
```

### Repo-root `NOTICE.md`

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

### Repo-root `ACKNOWLEDGMENT.md`

```markdown
# Access Acknowledgment

By accessing, viewing, cloning, or otherwise obtaining a copy of this
repository, you acknowledge and agree that:

1. The contents are confidential and proprietary information of
   GrowDirect LLC ("GrowDirect").

2. You will not disclose, reproduce, distribute, publish, or use any
   part of the contents — including code, documentation, designs,
   architecture, data models, and process artifacts — for any purpose
   other than the evaluation or collaboration expressly authorized by
   GrowDirect.

3. You will protect the contents with at least the same degree of care
   you use for your own confidential information, and in no event less
   than reasonable care.

4. You will return or destroy all copies in your possession upon
   GrowDirect's request.

5. These obligations survive the termination of any access or
   collaboration and continue until the information becomes publicly
   available through no fault of yours.

6. Nothing in this acknowledgment grants you any license, ownership
   interest, or right to the contents beyond the evaluation or
   collaboration authorized by GrowDirect.

If you do not agree to these terms, do not access the repository and
delete any copies you may have obtained.

Contact: contact@growdirect.io
```

### Repo-root `SECURITY.md`

```markdown
# Security

Report suspected vulnerabilities to security@growdirect.io. Do not
open public issues for security matters.

GrowDirect LLC has completed automated vulnerability scanning, static
application security testing (SAST), full git-history secret scanning,
and a structured OWASP Top 10 code-level review. A formal third-party
penetration test has not been performed and is scheduled if-and-when
commercial engagement proceeds. Findings from the automated and
code-level review are documented in `docs/audit-2026-04-23/security.md`
and `docs/audit-2026-04-23/security-tool-output/`.
```

### Acknowledgment capture mechanism — default Mechanism 1

Access-grant email pastes or links the `ACKNOWLEDGMENT.md` text. The
partner replies *"I acknowledge and agree"* before access is granted.
The email thread is the durable record.

Escalation path: if 1-on-1 doesn't scale, upgrade to a form at
`growdirect.io/acknowledge` (Google Form / Typeform) capturing name,
email, organization, IP, timestamp, explicit checkbox.

## Resolved naming decisions

**Canary repo rename.** `growdirectprez/growdirect-ops` →
`growdirectprez/canary`. The `growdirectprez` org name carries the
GrowDirect identity; the repo name is the product. `growdirect-canary`
would be redundant in the fully-qualified form
`growdirectprez/growdirect-canary`. GitHub preserves redirects so the
rename is non-disruptive. Executed in Phase 7.

**Canary App Brain directory.** `Canary/brain/` at repo root. Lowercase
matches Canary repo convention for top-level directories (matches
`Canary/canary/`, `Canary/devops/`, `Canary/docs/`).

**Audit report directory.** `docs/audit-2026-04-23/` per SHOW'd repo.
Date-stamped so future audits don't collide.

**Cleanup branch names.** `chore/cto-readiness-audit-2026-04-23` for
the main cleanup. `chore/security-findings-2026-04-23` for security
fixes. `chore/brain-mvp-split-2026-04-23` for the Brain move.

**Worktree paths.** `~/.worktrees/canary-cto-cleanup/` and
`~/.worktrees/growdirect-cto-cleanup/`. Matches existing
`.worktrees/` gitignore entry.

**Git tag for ready-to-share state.** `cto-review-ready-2026-04-23`
per repo.

## Open questions / deferred decisions

1. **Canary factory skills location.** `.claude/skills/canary-*` (14
   files) currently live in GrowDirect. Decision whether to move to
   `Canary/.claude/skills/` or keep centralized. Defaulted to keep
   centralized for MVP.
2. **Brain subtree split.** MVP accepts fresh git history on Canary
   App Brain in the Canary repo. Full subtree-split to preserve
   history is deferred.
3. **Full hierarchical Brain restructure.** Personal / Ops / Platform /
   App decomposition with founder view-shell is deferred to its own
   session.
4. **Enterprise lineage narrative.** The forward-looking sanitized
   story connecting prior retail LP experience to Canary is deferred
   to its own session. The enterprise-scale-gap-analysis within this
   audit is the minimum story; the lineage narrative is the fuller
   story.
5. **History rewrite on security findings.** If `gitleaks` or
   `trufflehog` find a committed secret, history rewrite is required
   for that secret. Triggered as a separate workstream with user
   sign-off. Deferred until findings land.

## Related

- [[Brain/projects/Canary|Canary MOC]]
- [[Brain/projects/Method|Method MOC]]
- [[Brain/projects/Factory|Factory MOC]]
- [[Brain/wiki/growdirect-factory-process|Factory Process]]

## Sources

- Conversation with user, 2026-04-23
- Git state assessment 2026-04-23 (working tree, `.gitignore`, Canary
  branches)
- Existing Brain content: `secure-client-kroger.md`,
  `secure-architecture.md` (for enterprise-benchmark dimensions only,
  not for inclusion in artifacts)
- Existing auto-memory:
  `feedback_no_loose_files.md`,
  `feedback_git_health_check_first.md`,
  `feedback_flag_dependency_changes.md`,
  `feedback_know_the_whole_solution.md`,
  `feedback_no_hype_copy.md`,
  `feedback_full_sweep_no_deferrals.md`,
  `feedback_fix_everything_not_just_one.md`,
  `project_foundation_three_entity_structure.md`,
  `reference_obsidian_config.md`
