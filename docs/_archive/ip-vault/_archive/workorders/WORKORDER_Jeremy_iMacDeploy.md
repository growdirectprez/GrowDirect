---
type: workorder
domain: infra
status: active
created: 2026-03-18
updated: 2026-03-19
---
# WORK ORDER: Jeremy — iMac Remote Deploy Script (`imac_deploy.sh`)
*Issued by ALX · February 26, 2026 · Priority: 🟡 HIGH — Sprint 5 / Demo readiness*

**Context:** We've had repeated pain setting up and re-deploying on the iMac Ubuntu box. We need a single script that can be run from any machine on the same network — after a clean `git pull` — to fully rebuild the Docker stack on the iMac over SSH. No manual steps. No assumptions about what's currently running.

**Goal:** Build `devops/imac_deploy.sh` — a remote deploy script that SSH's into the iMac, pulls latest code, and invokes the existing `canary_deploy.sh` there. This script wraps the local deploy pipeline we already have; it does not duplicate it.

**Jeffe's directive:** "Script a deploy for the iMac already running Ubuntu, already SSH ready — I can just execute after doing a clean git pull to rebuild the whole stack in Docker."

---

## DESIGN PRINCIPLE

`imac_deploy.sh` is a thin SSH wrapper. All real deploy logic lives in `canary_deploy.sh` (already built). The remote script:

1. Verifies SSH connectivity to the iMac
2. Does a `git pull` on the iMac repo
3. Calls `canary_deploy.sh` on the iMac with the requested mode
4. Streams output back to the calling terminal live

No logic duplication. Any fix to `canary_deploy.sh` is automatically picked up remotely.

---

## DEFAULTS

| Setting | Value | Notes |
|---|---|---|
| iMac host | `192.168.10.102` | Overridable via `--host` flag |
| iMac user | `jeffe` | SSH as this user |
| iMac repo path | `~/GrowDirect/Canary` | Where the git repo lives on the iMac |
| Default branch | `alpha-clean` | What to pull |
| Default deploy mode | `--full` | Full nuke and rebuild unless overridden |

---

## USAGE

```bash
./devops/imac_deploy.sh                        # Full rebuild (git pull + canary_deploy.sh --full)
./devops/imac_deploy.sh --fast                 # Full rebuild, cached Docker layers
./devops/imac_deploy.sh --no-test              # Full rebuild, skip pytest
./devops/imac_deploy.sh --app                  # Flask-only rebuild, keep DBs
./devops/imac_deploy.sh --test                 # Run tests only on iMac
./devops/imac_deploy.sh --status               # Show what's running, no deploy
./devops/imac_deploy.sh --host 192.168.1.X     # Override iMac IP
./devops/imac_deploy.sh --help                 # Show usage
```

All flags except `--host` and `--status` are forwarded directly to `canary_deploy.sh` on the iMac.

---

## SCRIPT FLOW (step by step)

### Step 1: SSH Connectivity Check
Test that the iMac is reachable before doing anything. If SSH fails, print a clear troubleshooting message:
- Is the iMac on the same network? (`ping <host>`)
- Is Remote Login enabled? (System Settings → General → Sharing → Remote Login)
- Is the SSH key installed? (`ssh-copy-id jeffe@<host>`)

Hard stop if SSH is not available. Do not proceed.

### Step 2: Git Pull on iMac
SSH in and run:
```bash
cd ~/GrowDirect/Canary
git fetch origin
git checkout alpha-clean
git pull origin alpha-clean
```

If the working tree is dirty (local changes on the iMac from a previous session), stash them automatically before pulling:
```bash
git stash push -m "imac_deploy auto-stash $(date +%Y%m%d_%H%M%S)"
```

Report branch and latest commit to the caller's terminal after pull.

### Step 3: Ensure `canary_deploy.sh` is Executable
```bash
chmod +x ~/GrowDirect/Canary/devops/canary_deploy.sh
```

### Step 4: Run `canary_deploy.sh` on iMac
Call the local deploy script with whatever mode and flags were passed:
```bash
./devops/canary_deploy.sh --full [additional flags]
```

Stream all output back to the calling terminal live (not buffered). The caller should see exactly what they'd see if they were sitting at the iMac terminal.

### Step 5: Report Result
On success: print the demo URL and Flask health URL.
On failure: print the exit code and a pointer to `docker logs canary_flask` for diagnosis.

---

## STATUS MODE (`--status`)

No deploy. Just SSH in and report:
- Current git branch and latest commit
- `docker compose ps` output (service name, status, ports)
- Flask `/health` endpoint response
- The demo URL

Useful for checking the iMac state without touching anything.

---

## ACCEPTANCE CRITERIA

| # | Criterion |
|---|---|
| AC-1 | `./devops/imac_deploy.sh` from any machine on the same network SSHs into the iMac, pulls `alpha-clean`, and runs `canary_deploy.sh --full` — zero manual steps |
| AC-2 | If SSH fails, script prints a clear troubleshooting message and exits — no cryptic errors |
| AC-3 | If the iMac working tree is dirty, script auto-stashes before pulling — no manual intervention required |
| AC-4 | All deploy output streams live to the calling terminal — caller can see progress in real time |
| AC-5 | `--fast`, `--no-test`, `--app`, `--test` flags are forwarded correctly to `canary_deploy.sh` |
| AC-6 | `--status` reports service health without triggering a deploy |
| AC-7 | `--host` flag overrides the default IP — script works if iMac IP changes |
| AC-8 | Script has `--help` flag with clear usage examples |
| AC-9 | Script is idempotent — running it twice in a row produces the same result |
| AC-10 | Script does NOT duplicate logic from `canary_deploy.sh` — it wraps it |

**The gate test:** Jeffe runs `./devops/imac_deploy.sh` from his machine, walks away, comes back to a fully rebuilt stack with the demo URL printed at the end. No questions asked.

---

## ONE-TIME PREREQUISITE (document in the script header)

SSH key must be installed on the iMac before the script will work passwordlessly:
```bash
ssh-copy-id jeffe@192.168.10.102
```

The script should detect if it's being prompted for a password (i.e. key not installed) and fail with a helpful message rather than hanging.

---

## FILE LOCATIONS

| File | Path |
|---|---|
| This work order | `_ALX/WorkOrders/WORKORDER_Jeremy_iMacDeploy.md` |
| New script (to create) | `Canary/devops/imac_deploy.sh` |
| Existing deploy script (to wrap) | `Canary/devops/canary_deploy.sh` |
| Existing compose file | `Canary/devops/docker-compose.alpha3x.yml` |
| Env file on iMac | `~/GrowDirect/Canary/devops/.env.alpha3x` |

---

## ESTIMATED EFFORT

**2–3 hours.** The deploy logic already exists. This is SSH plumbing, argument forwarding, and output streaming. The auto-stash and connectivity check are the only non-trivial pieces.

**Priority relative to smoke validation work order:** Secondary. Complete the smoke validation and seed data (WORKORDER_Jeremy_Sprint5_SmokeValidation.md) first. This script is infrastructure for future deploys — useful before Sprint 6, not required for Friday's dry-run.

---

*Issued by ALX.*
*Acceptance: Jeffe runs one command from his machine and the iMac stack rebuilds. No manual steps.*
