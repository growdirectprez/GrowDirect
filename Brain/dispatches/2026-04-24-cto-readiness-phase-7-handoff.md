---
classification: confidential
owner: GrowDirect LLC
type: dispatch
status: ready-for-handoff
date: 2026-04-24
target: claude-code-session (next)
priority: high
tags: [cto-readiness, ship, catz, canary-retail-brain, phase-7, handoff]
---

# Dispatch — CTO-Readiness Ship (Handoff)

Hand-off brief for the next Claude Code session to close out the
CTO-readiness preparation. Today's session (2026-04-23 → -24)
merged the audit work with the CATz methodology brand, scaffolded
both externally-facing vaults, landed Stream 4 (Solex worked-
example anchoring), renamed the methodology brand from KATZ to
CATz (Canary Agent Taskforce) to avoid Katz Group trademark
collision, and brought all three SHOW surfaces to a state where
only execution-and-operational steps remain.

This dispatch captures everything the next session needs to pick
up cleanly.

## Decisions captured (no re-asking)

| Decision | Answer |
|---|---|
| GitHub org for externally-facing repos | New `growdirect-llc` org (user to create); all three SHOW repos land there |
| External author / attribution name | **Geoffrey C. Lyle** — official / author-credit. **Geoff** or **Jeffe** = informal / internal only (never external) |
| Agent persona identity for ALX | **Alejandro Castillo aka ALX** — used where ALX needs a human identity |
| Methodology brand name | **CATz** = **Canary Agent Taskforce**. Replaces KATZ globally. Rename complete this session. |
| Canary repo rename | `growdirectprez/growdirect-ops` → `growdirect-llc/canary-retail` (new org) |
| `contact@growdirect.io` / `security@growdirect.io` | User to set up via Fastmail after this session; no blocker for Phase 7 scaffolding |
| 7 committed-secret history rewrite | **Deferred.** Partner read under NDA is low-risk; revisit if commercial engagement escalates |
| GrowDirect monorepo | **Internal forever.** No structural work; HIDE content stays in place |
| Next-session priority | **Multiple in parallel:** Phase 7 ship + CATz content expansion + some skill dogfood, interleaved |

---

## State at handoff

### Three external-facing surfaces — all content-complete, all verification PASS

**Canary** (`/Users/gclyle/GrowDirect/Canary/`, remote
`growdirectprez/growdirect-ops` — rename + transfer to
`growdirect-llc/canary-retail` pending)

- Main tip: `745b1b6 docs: cross-reference CATz + Canary-Retail-Brain
  siblings, scrub residual Jeffe refs from CLAUDE.md`
- Phase 5 merges complete (Canary cleanup + security-fix)
- Phase 6 verification: PASS with 3 minor hygiene items (non-blocking)
- Ready for Phase 7 tag + rename + access-grant

**CATz** (`/Users/gclyle/CATz/` — separate git repo, no remote yet)

- 26 markdown files across 3 commits
- Commits: `8881c26` scaffold, `c93d301` proof-case, `8596a54` expand
- Verification PASS with zero regressions (earlier)
- Ready for remote setup + push + access-grant

**Canary-Retail-Brain** (`/Users/gclyle/Canary-Retail-Brain/` —
separate git repo, no remote yet)

- 3 commits: scaffold, wikilink fix, Stream 4 Solex anchoring
- Verification PASS with zero regressions (earlier)
- Ready for remote setup + push + access-grant

### Internal-only surfaces

**GrowDirect monorepo** (`/Users/gclyle/GrowDirect/`) — stays
internal. Main has the audit cleanup, platform cleanup, Brain MVP
split, key-management doc, and today's three dispatches committed.
Not shown to any external party.

---

## Phase 7 — the remaining ship sequence

Execute in this order. Each step has a yes/no gate from the user
(captured in the questions section below) before firing.

### Step 1 — User stands up the `growdirect-llc` GitHub org

User action. Creates `https://github.com/growdirect-llc`. Adds
Geoffrey C. Lyle as owner. Once the org exists, the next session
executes the push steps below.

### Step 2 — Push CATz + CRB to the new org

```bash
cd /Users/gclyle/CATz
git remote add origin git@github.com:growdirect-llc/catz.git
git push -u origin main

cd /Users/gclyle/Canary-Retail-Brain
git remote add origin git@github.com:growdirect-llc/canary-retail-brain.git
git push -u origin main
```

### Step 3 — Canary repo rename + org transfer

Target state: `growdirect-llc/canary-retail` (renamed from
`growdirectprez/growdirect-ops`).

```bash
# Option A: rename then transfer (two steps, explicit)
gh repo rename canary-retail --repo growdirectprez/growdirect-ops --yes
gh repo transfer growdirectprez/canary-retail growdirect-llc

# Option B: transfer then rename
gh repo transfer growdirectprez/growdirect-ops growdirect-llc
gh repo rename canary-retail --repo growdirect-llc/growdirect-ops --yes

# Update local remote
git -C /Users/gclyle/GrowDirect/Canary remote set-url origin git@github.com:growdirect-llc/canary-retail.git
git -C /Users/gclyle/GrowDirect/Canary ls-remote origin 2>&1 | head -3  # verify
```

GitHub preserves URL redirects on both rename and transfer — old
URLs keep working.

### Step 4 — Tag all three SHOW surfaces

```bash
TAG=cto-review-ready-2026-04-24

git -C /Users/gclyle/GrowDirect/Canary tag -a $TAG -m "CTO-readiness audit complete — Canary ready for partner access"
git -C /Users/gclyle/CATz tag -a $TAG -m "CTO-readiness audit complete — CATz methodology vault ready for partner access"
git -C /Users/gclyle/Canary-Retail-Brain tag -a $TAG -m "CTO-readiness audit complete — Canary-Retail-Brain ready for partner access"

# Push tags (after remotes set)
git -C /Users/gclyle/GrowDirect/Canary push origin $TAG
git -C /Users/gclyle/CATz push origin $TAG
git -C /Users/gclyle/Canary-Retail-Brain push origin $TAG
```

### Step 5 — Verify mail receiving

Confirm `contact@growdirect.io` and `security@growdirect.io`
receive mail. Send a test email from external address. Verify
delivery. (User-side Fastmail config; see Q5.)

### Step 6 — Repo-sharing matrix finalization

Update `GrowDirect/docs/repo-sharing-matrix.md` with post-rename
names and the new CATz + CRB entries. Commit to GrowDirect main.

### Step 7 — Draft access-grant email

Template at the end of this dispatch. Customize per partner.

### Step 8 — Grant GitHub access when partner acknowledges

```bash
# After partner replies "I acknowledge and agree" to the email:
gh api --method PUT /repos/growdirect-llc/canary-retail/collaborators/<partner-handle> -f permission=read
gh api --method PUT /repos/growdirect-llc/catz/collaborators/<partner-handle> -f permission=read
gh api --method PUT /repos/growdirect-llc/canary-retail-brain/collaborators/<partner-handle> -f permission=read
```

Record in `GrowDirect/docs/repo-sharing-matrix.md`.

---

## Ready-to-execute work (no user-gate needed beyond go-ahead)

These items are scoped, the content is known, and execution can
fire as soon as the next session starts.

### A — Populate remaining CATz directories

Referenced from Home.md but not yet written:

- `method/roles/architect.md`, `writer.md`, `pmo.md` — mirror the
  data-detective / digital-plumber role playbook shape.
- `method/artifacts/sdd-template.md`, `interface-spec-template.md`,
  `context-diagram-template.md`, `traceability-matrix-template.md`
  — cloneable skeletons matching GrowDirect's existing SDD
  conventions (internal reference: `docs/sdds/`).
- `method/workstreams/` — one file per workstream named in
  Home.md (commercial, supply-chain, finance, store-operations,
  space-range-display, people-labor, property-assets,
  loss-prevention, technology). Short — ~50 lines each describing
  purpose, inputs, outputs, typical artifacts.
- `about/founder.md` — bio per Q3 author-name decision.
- `standards/arts/README.md` with enumerated ARTS models adopted
  (POSLog, Customer, Device, Site) and mapping to CRDM.

Estimated: 1–2 hours for placeholder-quality; 2–3 hours for first-
draft quality.

### B — Populate remaining Canary-Retail-Brain articles

- `platform/arts-adoption.md` — expansion of the ARTS mentions in
  crdm.md; POSLog, Customer, Device, Site model mappings explicitly
  documented.
- `platform/differentiated-five-add-on.md` — the T+R+N+A+Q story
  separately from the spine article.
- `modules/t-transaction-pipeline.md`, `r-customer.md`,
  `n-device.md`, `a-asset-management.md`, `q-loss-prevention.md`
  — one article per v1 Differentiated-Five module.
- `architecture/service-mesh.md`, `tsp-pipeline.md`,
  `chirp-engine.md`, `fox-cases.md`, `evidence-chain.md` — sanitized
  from Canary's internal SDDs.
- `integrations/pos-adapters.md`, `payments.md`, `ecommerce.md`,
  `security-hardware.md`, `mdm-and-itam.md` — one article per
  integration category.
- `case-studies/smb-specialty-archetype.md`, `multi-store-apparel.md`,
  `food-and-beverage.md`, `sporting-goods.md`, `mlm-direct-selling.md`
  — abstracted patterns, no named clients.
- `roadmap/v1-differentiated-five.md`, `v2-crdm-expansion.md`,
  `v3-full-spine.md` — milestones tied to customer-acquisition
  gates (per self-diagnostic Phase 1 recommendations).

Estimated: 2–4 hours for first-draft quality across all.

### C — Skill dogfood runs

Two subagent dispatches, each heavy but important:

1. **retail-diagnostic skill against Clarks ppt** — validates the
   skill reproduces the Clarks deliverable structure. Binary ppt
   extraction required (use `python-pptx` or similar tooling).
   Output: validation report + skill-generated pptx deck matching
   Clarks structure.
2. **retail-diagnostic skill against the self-diagnostic evidence
   pack** — produces the first real skill-generated pptx from the
   hand-written self-diagnostic. Compare skill output against the
   self-diagnostic to tune skill prompts.
3. **it-architecture-options skill against Morrisons ppt** —
   validates the second skill the same way.

Each run is ~3–4 hours. Best dispatched as background subagents
with periodic checkpoints. Note: prior subagent stream-timeout
risk observed earlier today; break each run into 2–3 smaller
subagent dispatches if possible.

### D — Backlog items (each a separate dispatch when fired)

- `MLE55GCYANCYT` env-var-ization (Canary seed code + tests + docs)
- `.jeffe` namespace rename (62 code refs across 10 files —
  product-naming decision needed first)
- 7-secret history rewrite (blocks on Q6 rotation status)
- Solex website coordination (blocks on Q8)
- Personal CIO Playbook v2 (dispatch 2026-04-24-cio-leave-behind-wedge
  issue 2)
- Board-ready pitch packet (dispatch 2026-04-24-cio-leave-behind-wedge
  issue 3)
- LinkedIn long-form (dispatch 2026-04-24-cio-leave-behind-wedge
  issue 4, timing-dependent)
- Heartbeat/Fireball playbook execution (separate dispatch)
- Interface Design Documents intake processing (separate dispatch)

---

## Access-grant email template

Customize per-partner. Save drafts in `GrowDirect/private/outbound-
drafts/` (gitignored) or similar.

```
Subject: GrowDirect engineering access — please acknowledge

[Partner name],

Per our conversation, here are the three surfaces I'd like to
share under confidentiality:

1. Canary Retail — the product repo (code, tests, architecture)
   https://github.com/growdirect-llc/canary-retail

2. CATz — the Canary Agent Taskforce methodology vault
   (engagement model, capability framework, artifact templates,
   role playbooks)
   https://github.com/growdirect-llc/catz

3. Canary-Retail-Brain — the product brand and architecture
   vault (platform positioning, module spine, CRDM, worked
   example)
   https://github.com/growdirect-llc/canary-retail-brain

Each repo has an ACKNOWLEDGMENT.md at the root. Before I grant
access, please read and reply to this email with "I acknowledge
and agree" — the reply is the durable record.

If anything in the acknowledgment is unworkable on your end,
let me know what needs to change.

— [Founder name]
GrowDirect LLC
contact@growdirect.io
```

---

## Session-close notes

- All three repos have their own NOTICE, ACKNOWLEDGMENT, SECURITY,
  CONTRIBUTING files at root. Access is granted per-repo, not as
  a bundle.
- All markdown carries `classification: confidential` +
  `owner: GrowDirect LLC` frontmatter.
- Zero prior-client-name leaks across the three surfaces
  (verification confirmed).
- The dispatch-3 authoring rules (no prior-client names, no
  former-company lineage, all-GrowDirect-attribution) are enforced
  in all three surfaces' CONTRIBUTING.md.

---

**Dispatch author:** Claude Code session, 2026-04-24 (after
merging CTO audit with CATz, landing Stream 4, populating
phases + CBM v2 deep-dives)
**Executor:** Claude Code session (next)
**Review gate:** User answers the 8 questions in the companion
AskUserQuestion prompt before Phase 7 steps 1–3 fire. Steps 4–7
are operational / user-driven.
