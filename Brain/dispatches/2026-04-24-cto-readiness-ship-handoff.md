---
title: Dispatch — CTO-Readiness Audit Ship Handoff
type: dispatch
status: open
created: 2026-04-24
updated: 2026-04-24
classification: confidential
owner: GrowDirect LLC
project: cto-readiness
tags: [dispatch, cto-readiness, audit, security, brand-voice, factory, cleanup, ship-handoff]
related:
  - "[[docs/superpowers/specs/2026-04-23-cto-readiness-audit-design|CTO-Readiness Audit — Design Spec]]"
  - "[[Brain/projects/Method|Method MOC]]"
  - "[[Brain/projects/Factory|Factory MOC]]"
  - "[[Brain/projects/Canary|Canary MOC]]"
  - "[[Brain/projects/GrowDirect|GrowDirect MOC]]"
---

# Dispatch — CTO-Readiness Audit Ship Handoff

**Governing thesis.** The CTO-readiness audit is designed; this dispatch
ships it. Canary and the SHOW-scoped GrowDirect platform need to be in a
defensible, honest, confidence-backed state by the week of 2026-04-28,
when first technical-co-founder access begins. Design lives in the spec
at `docs/superpowers/specs/2026-04-23-cto-readiness-audit-design.md` and
is the authority on dimensions, scope, philosophy, and standards. This
dispatch is the executable wrapper: seven phases, gated by founder
review, dispatched to subagents inside worktrees, definition-of-done
binary at every gate. No new design decisions live here; everything is a
pointer back to the spec or a resolution captured during execution.

## Scope at a glance

| Phase | Mode | Owner | Wall-clock | Done when |
|---|---|---|---|---|
| **0** Bootstrap | Serial | Founder + Architect | ~30 min | Spec approved; `security/platform-hardening` triaged; freeze cadence agreed |
| **1** Brain MVP split | Serial | Subagent (Architect-supervised) | ~30 min | Canary App Brain in `Canary/brain/`; Platform Brain stays; both branches merged |
| **2** Audit dispatch | Parallel — read-only | 5 subagents in one message | 15–30 min | Five audit reports under `docs/audit-2026-04-23/` per repo |
| **3** Audit review | Serial — gate | Founder | Founder-paced | Dispositions assigned; judgment calls resolved; secret-rotation workstream triggered if needed |
| **4** Cleanup dispatch | Parallel — via worktrees | 3 subagents (canary / platform / security-fix) | 30–60 min | Three cleanup branches with `cleanup-report.md`; subagents do not merge |
| **5** Cleanup review | Serial — gate | Founder | Founder-paced | Branches merged in defined order; history rewrite (if any) executed and verified |
| **6** Cold-reader verification | Parallel — read-only | 1 subagent | ~15 min | `ready-to-show-confirmation.md` per SHOW'd repo says PASS |
| **7** Ready-to-share | Serial | Founder | ~30 min | Repo rename, tags, mailboxes, sharing matrix, access-grant email out |

Total wall-clock target: **2.5–3 hours of subagent time**, plus founder
review gates. Calendar target: complete by **2026-04-27** to have buffer
before the 2026-04-28 partner window.

## What this dispatch does NOT do

The spec's *non-goals* list governs. The audit ships a hygiene-and-scoping
state, not a hardening sprint. Out of scope here:

- Full Personal/Ops/Platform/App Brain hierarchy.
- Enterprise-lineage narrative document (the sanitized retail-LP →
  Canary forward story). Stays a future session.
- Closing Kroger-benchmark scale gaps. The audit *documents* them; it
  does not *close* them.
- Feature work or refactor-for-cleanliness beyond audit-driven cleanup.
- Third-party penetration testing (deferred to commercial-engagement
  time).

If a finding implies any of the above, the cleanup subagent surfaces it
to the founder under `## Judgment Calls` and does not act unilaterally.

## Phase walkthroughs

Each phase's authoritative detail is in the spec. The notes below capture
**handoff instructions** — what the executor needs to know that isn't in
the spec or that requires emphasis.

### Phase 0 — Bootstrap

Two non-trivial actions before any subagent fires:

1. **`security/platform-hardening` disposition.** Confirm whether this
   Canary branch carries unmerged security fixes. If yes, founder
   approves merge to `main` so Phase 2 sees current state — *stale
   security state would distort findings and erode the credibility the
   audit is meant to build*. If already merged or abandoned, document
   and delete.
2. **Feature-session freeze cadence.** Cleanup subagents (Phase 4) run
   inside worktrees on `chore/cto-readiness-audit-2026-04-23`. Feature
   sessions must not land SHOW-scope changes between Phase 2 (audit
   baseline) and Phase 4 cleanup, OR each cleanup subagent re-runs the
   audit-dimension check on its branch immediately before producing its
   report. The founder picks one and the plan codifies it.

The plan file at `docs/superpowers/plans/2026-04-23-cto-readiness-audit.md`
captures dispatch prompts; produced by the `writing-plans` skill once the
spec is approved.

### Phase 1 — Brain MVP split

Mechanic: `git mv` from GrowDirect into Canary. Two branches, two repos,
both named `chore/brain-mvp-split-2026-04-23`. Canary receives fresh
in-repo file history; original provenance stays queryable in GrowDirect.
Subtree-split for full history preservation is **deferred** (Open
Question 2 in spec).

Critical link-hygiene step: after `git mv`, run
`mcp__obsidian__find_broken_links_tool` on both vaults; resolve or
remove broken cross-vault wikilinks before merge.

Confidentiality note for executor: anything touched here gets the
markdown frontmatter (`classification: confidential`, `owner:
GrowDirect LLC`) added in Phase 4, not Phase 1. Phase 1 moves files;
Phase 4 marks them.

### Phase 2 — Audit dispatch

Five subagents fire in a **single message**. They are read-only, produce
findings only, do not change source files. Reports land at:

| Subagent | Report path |
|---|---|
| `canary-audit` | `Canary/docs/audit-2026-04-23/canary.md` |
| `platform-audit` | `GrowDirect/docs/audit-2026-04-23/platform.md` |
| `docs-brain-audit` | `GrowDirect/docs/audit-2026-04-23/docs-brain.md` and `Canary/docs/audit-2026-04-23/docs-brain.md` |
| `security-audit` | `<repo>/docs/audit-2026-04-23/security.md` + `security-tool-output/` per repo |
| `enterprise-scale-gap` | `GrowDirect/docs/audit-2026-04-23/enterprise-scale-gap-analysis.md` (post-findings; sanitized — no prior-client names) |

Tool installs go to the dispatch environment via `uvx` / `pipx` / `brew`
/ `go install`. **No** changes to `requirements.txt` or `package.json` —
this is an auto-memory rule, not a stylistic preference.

Each finding records: file path, line number, exact offending text,
severity (CRITICAL / HIGH / MEDIUM / LOW), recommended action.

### Phase 3 — Audit review (founder gate)

The founder reads all five reports, assigns dispositions for each
finding, flags judgment calls, and confirms the enterprise-gap framing.

**Special case — committed secrets.** If `gitleaks` or `trufflehog` find
a secret in git history, "documented" is not a sufficient disposition.
The secret must be rotated AND purged from history before first partner
access (success criterion 10 in spec). This triggers a separate
history-rewrite workstream with explicit founder sign-off, run between
the two cleanup merges in Phase 5.

### Phase 4 — Cleanup dispatch

Three subagents, each in its own worktree (per resolved naming):

| Subagent | Worktree | Branch |
|---|---|---|
| `canary-cleanup` | `~/.worktrees/canary-cto-cleanup/` | `chore/cto-readiness-audit-2026-04-23` (Canary) |
| `platform-cleanup` | `~/.worktrees/growdirect-cto-cleanup/` | `chore/cto-readiness-audit-2026-04-23` (GrowDirect) |
| `security-fix` | (per-repo separate branch) | `chore/security-findings-2026-04-23` (per affected repo) |

Cleanup philosophy is the spec's *Conservative Cleanup Philosophy*
section, eight rules. The two that bite hardest in practice:

- **Rule 2 (Scale back over polish-in-place):** when a function or doc
  looks half-baked, default action is remove / feature-flag-off / convert
  to thoughtful stub. Never "try to make it better."
- **Rule 5 (No silent surprise-refactoring):** cleanup fixes findings.
  Nothing else. Unrelated improvements log as separate findings; the
  current pass does not touch them.

Each subagent re-runs the audit-dimension check on its worktree branch
before producing its report and reconciles against the Phase 2 baseline.
New findings introduced by concurrent feature-session landings either
fold into cleanup scope or surface to the founder as out-of-scope.

Subagents do **not** merge. The founder reviews and merges in Phase 5.

### Phase 5 — Cleanup review (founder gate)

Merge order per repo:
1. `chore/cto-readiness-audit-2026-04-23` first.
2. (If history rewrite required:) committed-secret rewrite as own workstream.
3. `chore/security-findings-2026-04-23` second.

`chore/brain-mvp-split-2026-04-23` was already merged in Phase 1.

### Phase 6 — Cold-reader verification

One subagent simulates a cold technical-co-founder reader: starts at
`README.md`, walks architecture → code → tests → audit reports.
Verifies confidentiality markings, root files (`NOTICE.md`,
`ACKNOWLEDGMENT.md`, `SECURITY.md`), no TODO/stub/AI-voice residue, no
client-name leaks, cross-doc links resolve, enterprise-gap analysis
reads defensibly.

Output per SHOW'd repo: `docs/audit-2026-04-23/ready-to-show-confirmation.md`
— either **PASS** or a regression list. A regression list returns to
Phase 4 for one more cleanup pass; do not paper over.

### Phase 7 — Ready-to-share

Founder actions, not subagent:

- Tag `cto-review-ready-2026-04-23` on each SHOW'd repo.
- Execute `growdirectprez/growdirect-ops` → `growdirectprez/canary`
  rename. GitHub preserves redirects; old URLs continue to resolve.
- Confirm `contact@growdirect.io` and `security@growdirect.io` receive
  mail (Fastmail setup — this is a founder action, not in the
  cleanup scope).
- Finalize `docs/repo-sharing-matrix.md`.
- Send access-grant email containing or linking `ACKNOWLEDGMENT.md`
  text. Mechanism 1 is default: partner replies *"I acknowledge and
  agree"*. The thread is the durable record. Escalation to a form at
  `growdirect.io/acknowledge` is available if 1-on-1 doesn't scale.

## Sequencing

```
T+0       (now, 2026-04-24)        Spec final → plan written → dispatch out
T+0.5h                              Phase 0 bootstrap done; security/platform-hardening triaged
T+1h                                Phase 1 Brain MVP split merged on both repos
T+1.5h                              Phase 2 audit reports in
T+ founder-review                   Phase 3 dispositions resolved; secret-rotation triggered if any
T+ founder + 1h                     Phase 4 cleanup branches in
T+ founder-review                   Phase 5 cleanup branches merged in order
T+ founder + 0.5h                   Phase 6 cold-reader PASS per repo
T+ founder + 0.5h                   Phase 7 tags, rename, sharing matrix, access-grant email
```

Calendar target: all-green by **end of day 2026-04-27**, leaving 2026-04-28
buffer before the partner window.

## Definition of done (dispatch level)

All eleven success criteria from the spec must verify true:

1. Zero unresolved markers in SHOW scope.
2. Zero sloppy stubs (only thoughtful stubs passing the five-point test).
3. Zero AI-voice commentary in code or docs.
4. Zero client / personal / sensitive names in SHOW scope.
5. Confidentiality markings on every SHOW'd file; root standards files
   (`NOTICE.md`, `ACKNOWLEDGMENT.md`, `SECURITY.md`) at every SHOW'd repo.
6. Enterprise-scale gap analysis exists per scope, sanitized,
   distinguishes gap-by-roadmap from choice-by-design.
7. Git state clean: no loose root files, no uncommitted intent on main,
   no stale agent branches; remote / default-branch / visibility verified
   per repo.
8. Brain MVP split executed; Canary App Brain in `Canary/brain/`;
   Platform-supporting Brain stays in GrowDirect; HIDE scope intact in
   `GrowDirect/Brain/`.
9. `docs/repo-sharing-matrix.md` finalized.
10. Security audit findings either resolved or have explicit founder
    disposition. **Committed secrets are rotated AND purged from
    history.** "Documented" is not sufficient for a committed secret.
11. Cold-reader verification PASS per repo.

When all eleven verify, this dispatch closes and the
`cto-review-ready-2026-04-23` tag is the durable artifact.

## Open decisions execute-time may need to close

From spec §"Open questions / deferred decisions":

1. **Canary factory skills location** — defaulted *centralized*. Revisit
   only if cleanup surfaces an `.claude/skills/canary-*` finding that
   forces the question.
2. **Brain subtree split for history preservation** — accepted as MVP
   compromise; not closed by this dispatch.
3. **Full hierarchical Brain restructure** — out of scope; not closed.
4. **Enterprise lineage narrative** — out of scope; not closed.
5. **History rewrite on security findings** — closed *if-and-when*
   `gitleaks` / `trufflehog` find a committed secret in Phase 2. Until
   then, no decision needed.

## Handoff

- **Authority:** Founder, against the spec.
- **Architect / executor:** Claude, dispatching subagents per phase.
- **Gate:** Founder reviews and approves at every phase boundary; no
  subagent merges to `main` without explicit approval.
- **Linear:** issues opened per phase as needed; this dispatch linked
  from each issue body.
- **Audit + cleanup logs:** under `docs/audit-2026-04-23/` per SHOW'd
  repo; durable.
- **Closing artifact:** `cto-review-ready-2026-04-23` tag per repo,
  plus `docs/repo-sharing-matrix.md` updated.

This dispatch becomes reference material once all eleven success
criteria verify. The spec at
`docs/superpowers/specs/2026-04-23-cto-readiness-audit-design.md`
remains the durable design record; the dispatch is the trace of how
shipping happened.

---

*Source: design spec dated 2026-04-23, founder conversation 2026-04-23
to 2026-04-24. Authored against CLAUDE.md delivery-mode standards
(governing thesis first paragraph, MECE decomposition, framework per
section). Handoff unit: phase, with founder gate at each boundary.
Subagent dispatches do not bypass gates.*
