---
status: active
date: 2026-04-20
target: fresh Claude Code session (laptop or mini)
branch: feat/coac-hoa-qa-instance
repo: github.com:growdirectprez/Cove.git
---

# Dispatch — Continue CoAC HOA Instance Build

You are picking up a mid-flight implementation. The plan is executing via `superpowers:subagent-driven-development`. Two of ten chunks are shipped. Eight chunks remain. This dispatch gives you everything you need to resume.

## Before you start — read these three files

Order matters. Don't skip.

1. **Spec (WHAT):** `docs/superpowers/specs/2026-04-20-coac-president-demo-tenant-design.md`
   GrowDirect repo. Describes the design: production-mode gating, 5 net-new features, preload manifest, sensitivity filter, deployment target.

2. **Plan (HOW):** `docs/superpowers/plans/2026-04-20-coac-hoa-qa-instance.md`
   GrowDirect repo. 10-chunk executable plan. You'll execute chunks 3–10.

3. **Cove context:** `Cove/CLAUDE.md`
   Cove repo. Platform conventions, hard rules (APN primary key, secret-ballot separation, Davis-Stirling compliance, lot-based email identity).

## Environment you need

### On the laptop (where Chunks 3–8 run)
- Docker stack running:
  ```bash
  cd ~/GrowDirect/devops && docker compose up -d
  cd ~/GrowDirect/Cove/devops && docker compose up -d
  ```
- Branch checked out:
  ```bash
  cd ~/GrowDirect/Cove && git checkout feat/coac-hoa-qa-instance && git pull
  ```
- Database state:
  - `cove` (dev) — migration `78fc094c3225` already applied
  - `cove_test` — recreated fresh this session; uses `db.create_all()` (no alembic)
  - Verify: `docker exec growdirect_postgres psql -U growdirect -d cove -c "\dt advisor_acknowledgements"`
- Image deps (weasyprint + qrcode system libs): already in Dockerfile, already in image. Don't rebuild unless you change `requirements.txt` or `Dockerfile`.

### On the mini (where Chunk 9 deploys to)
SSH works via `ssh mini` (IdentityFile `~/.ssh/id_canary` on the laptop, pubkey already installed on `gclyle@Geoffs-Mac-mini`). Mini state:
- macOS 26.3.1 arm64, Docker + git + python3 installed
- **Missing:** node, brew, cloudflared, claude, gpg, b2 — install when Chunk 9 needs them
- No `~/GrowDirect/Cove/` checkout on the mini yet — first Chunk 9 step is `git clone`
- `growdirect_postgres` + `growdirect_valkey` already running
- Existing `devops-cove-*` containers of unknown vintage running; **do not touch without user approval** (user is deliberating whether to leave them)

## What's done (don't redo)

All on `feat/coac-hoa-qa-instance` in the Cove repo. 11 commits off main at `b487b88`:

| Commit | Chunk.Task | What |
|---|---|---|
| `4008a1a` | Pre-flight 0.3 | weasyprint + qrcode deps + Dockerfile system libs + home dir for fontconfig |
| `cd0e015` | 1.1 | `COVE_DEPLOYMENT_MODE` config + `cove/deployment.py` helpers |
| `59d7e23` | 1.2 | Conditional blueprint registration; ARC gate refactor (module→app hook) |
| `584d334` | 1.3 | Fail-fast production startup assertion |
| `35bd5d9` | 1.4 | `.env.example` documents `COVE_DEPLOYMENT_MODE` |
| `6a7808d` | 2.1 | `AdvisorAcknowledgement` model + tests |
| `3a2d1c4` | 2.2 | `ProposalTallyCertification` model |
| `f002477` | 2.3 | `Document.published_at` / `publish_to_members` / `compliance_category` |
| `67631ff` | 2.4 | Alembic migration `78fc094c3225` (two tables, three columns, president role seed) |
| `bc7e0b6` | 2.5 | `Member.is_president` property |
| `1f31762` | cleanup | `InvalidDeploymentMode` + type hints + test refresh() |

Tests currently at ~40 pre-existing failures (unchanged baseline — our chunks introduced zero regressions). 13/13 tests pass across `test_deployment_mode.py`, `test_advisor_token.py`, `test_member_is_president.py`.

## What's next — execute in order

Each chunk follows the same workflow: dispatch implementer subagent with the task text from the plan → spec compliance reviewer → code quality reviewer → mark complete. Loop.

- **Chunk 3 — Publish cascade.** `cove/vault/channels/` with in-app / lot-email / door-hanger PDF adapters, plus `cove/vault/publish.py` orchestrator. 5 tasks. Uses weasyprint + qrcode (already installed). Tests via MailHog for email, tmpdir for PDFs.
- **Chunk 4 — President's Desk.** `/board/president` role-gated dashboard, three-item checklist template. 1 task. Small.
- **Chunk 5 — Inspector's Paper Tally.** `/vote/paper-tally/<proposal_id>` with per-choice count entry, auto-sum, PDF certification. Must not write to `ballots` / `ballot_envelopes`. 1 task.
- **Chunk 6 — Consulted Advisor E-ack.** `/advisor/acknowledge/<token>` magic-link flow, new `advisor_bp` blueprint package. 1 task.
- **Chunk 7 — §4525 Compliance Dashboard + Packet Builder.** `/documents/compliance` with category checklist, packet zip generator, cover sheet. 2 tasks.
- **Chunk 8 — Seed + sensitivity.** `scripts/import_disc_docs.py` + `scripts/seed_coac_president_demo_tenant.py` + sensitivity filter tests. 2 tasks. Disc at `/Volumes/My Disc/` — verify mounted before running.
- **Chunk 9 — Deploy to mini + board proposal packet.** `devops/docker-compose.production.yml`, runbooks, board packet docs (cover letter + §4525 memo + election notice draft + demo script). 2 tasks. Run via SSH to mini.
- **Chunk 10 — Security hardening.** 9 tasks. Least-privilege DB user, non-root container (already done — skip Task 10.2), encrypted backup, login lockout, audit log wiring, Cloudflare WAF config, secrets rotation runbook, mini hardening checklist, incident response playbook.

Total: roughly 23 more implementer cycles + their reviews.

## Deferred follow-ups (don't forget)

### Non-blocking, batch when convenient
- `can_vote=FALSE` on president role seed (current migration set TRUE; semantic mismatch)
- `updated_at` column on `proposal_tally_certifications` OR explicit "append-only" docstring
- Python-side UUID generation in the president role seed INSERT (replaces `gen_random_uuid()::text` for cross-env consistency)
- Flask import alias consolidation in `cove/__init__.py` (`_arc_req`, `_abort`, `_req`, `_redir`, `_url` — multiple aliasing conventions in one function)
- Runbook note: `COVE_DEPLOYMENT_MODE=production` disables Angel CLI (`flask crawl`, `flask market`, `flask crmls`) and SEO routes

### Pre-existing tech debt (NOT part of HOA feature — separate work)
Schema drift detected when generating migration `78fc094c3225`. Each item deserves its own focused migration:
- Drop table `leads` (model deleted)
- Drop `members.electronic_ballot_consent_at`
- Drop `organizations.electronic_voting_authorized_at`
- Drop `survey_descriptions.search_vector` + `survey_references.search_vector` + their GIN indexes
- Drop `ix_knowledge_chunks_embedding` (HNSW index)
- Drop `ix_market_snapshots_area` + `ix_market_snapshots_period`
- Add NOT NULL to `created_at`/`updated_at` on `community_events`, `local_entities`, `local_sources`, `market_snapshots`
- Add FK `listings.apn → parcels.apn` (model has it, DB doesn't)

## Sensitivity guardrails (re-read before every UI-facing commit)

Nothing in the HOA-facing surface may reference:
- Article II §5, Declaration 100, reactivation, 15-owner network, trustee slate, blitz
- Lot H, 0 Clipper, ocean path easement, Parcel 106
- `coac-*` Brain content
- Modernization package in full (only the election-notice draft ships)
- Foundation 501(c)(3) / 501(c)(4) surfaces

The automated sensitivity-filter tests in Chunk 8 will catch regressions. Run them after every UI or template change in Chunks 4–7.

## Workflow mechanics

### To resume on the laptop (same session continuation)
1. Invoke `superpowers:subagent-driven-development` (it guides dispatch pattern — implementer → spec review → quality review → mark complete).
2. For each task: extract the exact task text from the plan file, craft an implementer-subagent prompt that includes the project context block (branch, container, test DB, key conventions), full task text, TDD steps, and commit instructions. Pattern is established in the 11 commits already on the branch — mirror it.
3. Dispatch `general-purpose` for implementers and spec reviewers. Dispatch `superpowers:code-reviewer` for code quality review.
4. One implementer-subagent per task (or one per chunk of tightly-coupled tasks, as Chunk 2 was).
5. Never skip either review. Never `--no-verify` on commits. Pre-commit hook is patched for bash 3.2 already — should pass cleanly.

### To resume on the mini (fresh Claude Code session on 192.168.10.102)
First: install prereqs.
```bash
# Homebrew (if missing)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Required tooling
brew install node cloudflared git

# Clone
mkdir -p ~/GrowDirect && cd ~/GrowDirect
git clone git@github.com:growdirectprez/Cove.git
cd Cove && git checkout feat/coac-hoa-qa-instance
```

Then: point Docker at the cloned repo and follow Chunk 9's runbook (once that chunk's artifacts exist — they don't yet).

### If a subagent returns BLOCKED or NEEDS_CONTEXT
- Read the concern. Usually it's about a fixture name, a missing helper, or an unexpected schema column.
- Answer precisely with `SendMessage` to the same agent, or re-dispatch a fresh subagent with additional context. Don't fix by hand — that pollutes orchestrator context.

## Quick sanity verification before resuming

```bash
cd ~/GrowDirect/Cove
git branch --show-current                   # → feat/coac-hoa-qa-instance
git log --oneline | head -12                # top commit: 1f31762 (cleanup)
docker ps --format "{{.Names}}: {{.Status}}" | grep cove_flask
docker exec cove_flask pytest tests/integration/test_deployment_mode.py tests/unit/test_advisor_token.py tests/unit/test_member_is_president.py -v
# expect: 13 passed
```

If those all check out, start dispatching Chunk 3's first task.

## One-sentence status line for a handoff message
> Chunks 1 + 2 shipped on `feat/coac-hoa-qa-instance` at commit `1f31762`; 13/13 new tests pass, zero regressions; Chunk 3 (multi-channel publish cascade) is next.
