---
type: dispatch
status: ready-for-execution
date: 2026-04-25
target: laptop-side Claude Code (this conversation OR a fresh laptop session) — driving the mini via SSH alias `mini`
priority: high
execution-model: laptop-driven via SSH; the mini does NOT host its own Claude Code during this dispatch. Claude Code runs on the laptop; commands execute on the mini through SSH.
prerequisite: bootstrap-equivalent for SSH execution — health check + sanitize + Claude cleanup + baseline must be founder-approved before reconfig changes are made
unblocks: production-grade GrowDirect asset state on the mini; future mini-resident Claude Code (post-reconfig); engineering dispatches that follow
inputs:
  - prior inspection state captured in this dispatch (originally produced 2026-04-25 inspection session)
tags: [mini, reconfig, hardening, asset, ssh-driven, production-discipline]
---

# Dispatch — Mini Reconfig as GrowDirect LLC Company Asset

## Operational discipline (read first)

**Execution model:** This dispatch is executed BY laptop-side Claude Code (SSH-driving the mini), NOT by a Claude instance running on the mini. The mini is the remote target for SSH-driven commands. Decisions and commit work happen on the laptop; state changes happen on the mini through SSH.

The mini is **actively serving production traffic** — reconfig work must avoid disrupting live workloads. If anything is ambiguous, surface it for founder decision and wait.

This dispatch sets up the mini as a stand-alone GrowDirect LLC company asset. Future mini-resident Claude Code (and the ALXjr persona) becomes possible AFTER this reconfig completes. Engineering dispatches that depend on a fully-prepared mini also follow this.

## Why this exists

The Mac mini is being reconfigured from a personal device ("Geoff's Mac mini") to a stand-alone GrowDirect LLC company asset with a narrowed steady-state role: **serve Quartz portals + Canary/Cove apps + supporting infra. Nothing else.** No Claude Code on the mini, no engineering work, no exploratory operation. The mini is a hosting target.

The reconfig formalizes ownership, hardens the asset, removes any prior personal-device drift (including any Claude state), and documents the inventory record — all without taking the production workloads offline.

**Post-reconfig steady state on the mini:**
- Quartz portals at `methodology.growdirect.io` and `architecture.growdirect.io` (when stood up — currently the public hostnames are Canary/QA/abalonecove)
- Canary production stack (port 5100)
- Cove production stack (port 5002)
- Supporting infra: postgres (5432), valkey (6379), pgvector (5433), pgadmin (5050)
- Cloudflare Tunnel daemon
- **Nothing else.** No Claude Code, no Node engineering tooling beyond what Quartz/apps need, no ad-hoc state.

## Reaching the mini

- **SSH alias:** `mini` (configured in `~/.ssh/config` on the operator workstation)
- **IP:** 192.168.10.102 (LAN; gateway 192.168.10.1)
- **User:** gclyle (sole admin)
- **Key:** `~/.ssh/id_canary` (ed25519); two `canary-dev@growdirect`-labeled keys in `authorized_keys`

## Hardware / OS

- Mac mini M4, Model MU9D3LL/A (Mac16,10), 16 GB RAM, 228 GB SSD (~134 GB free)
- Serial: C731W91WMJ
- macOS 26.3.1 (Darwin 25.3.0, arm64 / T8132)
- Uptime ~10+ days; ethernet via `en0` (MAC `d0:11:e5:8b:3f:37`)

## Current identity (still consumer-named — needs reconfig)

- ComputerName: "Geoff's Mac mini"
- LocalHostName: "Geoffs-Mac-mini"
- HostName: not set
- No asset tag, no MDM, no inventory record tying serial → GrowDirect LLC

## LIVE production workloads — DO NOT bounce without coordination

Public hostnames (via Cloudflare Tunnel `4e130be4-783a-4b03-9f36-be3d4d738b0f`, config at `~/.cloudflared/config.yml`, running as `/Library/LaunchDaemons/com.cloudflare.cloudflared.plist`):

| Hostname | Origin port | Container | Status |
|---|---|---|---|
| canary.growdirect.app | 5100 | canary_prod_flask + 4 TSP subs | healthy ~40h |
| qa.growdirect.app | 5001 | canary_qa_app | TSP subs unhealthy ~9d |
| abalonecove.org / * | 5002 | devops-cove-web-1 | live |

Shared infra containers:
- `growdirect_postgres` (postgres:17, port 5432) — all DBs
- `growdirect_valkey` (valkey:8, port 6379)
- `canary_qa_pgadmin` (port 5050)
- `devops-cove-db-1` (pgvector:pg17, port 5433)

Plus stale exited containers from QA cycles (`canary_qa_pg`, `canary_qa_valkey`).

## Tooling on the mini

- Docker Desktop 29.2.1 (`/Applications/Docker.app`) — **NOT** OrbStack/Colima
- `/usr/bin/python3` (3.9.6 system); git 2.50.1
- No homebrew, no node, no pnpm
- `cloudflared` installed via pkg (binary not in user PATH; runs as LaunchDaemon)

## Code on the mini

- `~/GrowDirect/Canary` (branch: main)
- `~/GrowDirect/Cove` (branch: main)
- `~/GrowDirect/devops` (shared compose stack)
- `~/GrowDirect` itself is **NOT** a git repo
- Total size ~845 MB. Home Library is 52 GB.

## Security posture (gaps in BOLD)

- FileVault: ON
- **Application Firewall: OFF**
- **Time Machine: no destinations configured**
- Remote Login: enabled (SSH)
- **Single human-named admin account (`gclyle`); no service / ops role account**
- 2 SSH keys, both labeled `canary-dev@growdirect`

## Scope — seven categories of reconfig work

1. **Identity** — rename ComputerName / LocalHostName / HostName to GrowDirect-convention (e.g., `growdirect-mini-01` / `mini.growdirect.local`); record serial, MAC, location, owner-of-record (GrowDirect LLC).
2. **Backup** — configure Time Machine to a dedicated destination. Verify Postgres data dirs are captured OR explicitly excluded with separate pg backups documented.
3. **Firewall** — enable Application Firewall + stealth mode; review listener exposure (5001/5002/5050/5432/5433/6379) — which should be LAN-only, which need lockdown.
4. **Account hygiene** — consider separating personal vs. company admin; rotate / re-label SSH keys with explicit hostnames; audit `authorized_keys`.
5. **Stack cleanup** — prune exited QA containers; decide fate of `qa.growdirect.app` stack (TSP subs unhealthy ~9d); document image/tag conventions.
6. **Claude cleanup** — inventory and clean any prior Claude Code state on the mini before it becomes a production asset. Targets: `~/.claude/` (settings, projects, sessions, agents, MCP configs, history, telemetry caches), `~/Library/Application Support/Claude/`, `~/Library/Caches/Claude*`, `~/Library/Logs/Claude*`, `~/Library/Preferences/com.anthropic.*`, any `claude*` binaries in `/usr/local/bin`, any Claude-related launchd entries, residual environment exports in shell rc files. Inventory first, propose for removal, founder approves before deletion. Goal: clean baseline so when Claude Code is later installed for production-mini use, there's no drift from prior personal-device usage.
7. **Asset record** — write an inventory/hardening doc with serial, location, contacts, recovery procedure, quarterly review date.

## Constraints / discipline

- **Production workloads above MUST keep serving.** No reboots without a window; no `docker compose down` on prod stacks without a cutover plan.
- The cloudflared tunnel daemon serves all four public hostnames from one config — **editing it is a blast-radius event**.
- Operator wants two artifacts produced from this work:
  - **(a) Hardening checklist** landed under `Canary/devops/` OR a more appropriate platform location (`devops/` at repo root is shared infra; the mini hosts both Canary and Cove, so platform scope may fit better — decide before writing).
  - **(b) Linear issue** — operator believes a NEW Linear project was created for this work. **Search Linear first.** If not found, ASK before filing under Platform / Deploy.
- Existing references to a "Mini Hardening Checklist" exist as a stub heading inside `docs/superpowers/plans/2026-04-20-coac-hoa-qa-instance.md` — it has no real content; treat as a placeholder, **not** source of truth.
- **Branch hygiene:** do NOT commit to whatever branch the session starts on by default. Check `git status` and create a fresh branch off `main` (or use the existing `chore/cto-readiness-audit-2026-04-24` worktree at `/Users/gclyle/.worktrees/growdirect-cto-cleanup` if appropriate).

## Operating procedure — what this dispatch does FIRST

1. Confirm git state and choose / create the right branch (per branch hygiene above).
2. Confirm Linear project — search Linear; if uncertain, **ASK** before filing.
3. Confirm where the hardening doc lives — `Canary/devops/` vs platform `devops/` vs `docs/ops/`. Decide before writing.
4. THEN propose the hardening checklist outline (TOC + section stubs) and wait for founder review.
5. **DO NOT make changes on the mini until the checklist is reviewed.**

After the checklist is reviewed, work each of the seven scope categories in order of risk (lowest blast radius first). Recommend sequence: identity → asset record → Claude cleanup (inventory only first, then proposal, then founder-approved removal) → stack cleanup (only stale exited containers, never live ones) → account hygiene → firewall → backup. Each category produces:
- A diff (or file change) for the checklist doc
- A change record (what was changed, when, verified-via)
- A rollback procedure if applicable

All commands execute via SSH from the laptop:

```bash
ssh mini '<command>'
```

Inspection commands run freely. Mutation commands (anything that changes mini state) get drafted, reviewed by founder, then executed.

## Out of scope (do NOT do)

- Do NOT touch the cloudflared daemon config until the cutover plan is reviewed. Single point of public-facing failure.
- Do NOT bounce, restart, or reconfigure the production containers (`canary_prod_flask`, `canary_prod_tsp_*`, `devops-cove-web-1`, `growdirect_postgres`, `growdirect_valkey`) without a coordinated window.
- Do NOT remove SSH keys or change `authorized_keys` without staging a replacement key first and verifying access.
- Do NOT reformat or re-image. The mini is a live asset; reconfig in place.
- Do NOT install MDM until founder explicitly authorizes — adding MDM is a strategic decision, not a hardening default.
- Do NOT commit code without founder review. Each category produces drafts; founder reviews before merge.
- Do NOT chat with the founder about non-dispatch topics. Production discipline.

## Acceptance criteria

- [ ] Git state confirmed; branch chosen / created per branch hygiene
- [ ] Linear project confirmed (existing or filed under approved bucket after asking)
- [ ] Hardening doc location decided + documented
- [ ] Hardening checklist outline drafted + founder-approved BEFORE any change
- [ ] Each of the six categories closed with: change record, verification, rollback note
- [ ] Asset record written: serial, MAC, location, owner-of-record, contacts, recovery procedure, quarterly review date
- [ ] Linear issue filed and linked to the hardening doc
- [ ] Production workloads still serving (verified at end of each category): cloudflared tunnel up, all four hostnames responding, container health unchanged from start

## Reporting cadence

- Checkpoint at end of each scope category. Founder reviews before next category begins.
- Surface blockers immediately; do not grind through ambiguity.
- Report format: one-page status — what's done, what's next, what's blocked, production-state confirmation.

## Useful commands (verified working from operator workstation)

```bash
ssh mini 'docker ps --format "table {{.Names}}\t{{.Status}}"'
ssh mini 'cat ~/.cloudflared/config.yml'
ssh mini 'scutil --get ComputerName; scutil --get LocalHostName'
ssh mini 'fdesetup status; /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate'
ssh mini 'tmutil destinationinfo'
```

## Related

- `CATz/agents/ALXjr.md` — the persona executing this dispatch (bootstrap protocol runs first)
- Memory: `project_sandbox_vs_mini_separation.md` — production-dispatch-driven discipline
- `dispatches/2026-04-25-tsp-crdm-counterpoint-flow.md` — engineering dispatch that loads AFTER this reconfig is complete
- `docs/superpowers/plans/2026-04-20-coac-hoa-qa-instance.md` — contains stub "Mini Hardening Checklist" heading (placeholder only, NOT source of truth)
- `/Users/gclyle/.worktrees/growdirect-cto-cleanup` — pre-existing worktree on `chore/cto-readiness-audit-2026-04-24` branch; may be the right working location

---

**Dispatch author:** Founder via senior ALX (laptop/sandbox), 2026-04-25
**Executor:** ALXjr / Mac mini (production-dispatch-driven)
**Review gate:** Founder reviews git/branch choice, Linear project, doc location, checklist outline, and each category output before next category begins
