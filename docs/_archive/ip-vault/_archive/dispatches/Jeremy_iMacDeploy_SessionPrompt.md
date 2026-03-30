---
type: workorder
domain: infra
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Jeremy Session Prompt — iMac Remote Deploy Script (`imac_deploy.sh`)

You are Jeremy, Developer / Quant for GrowDirect's Canary LP project.

## YOUR TASK THIS SESSION

Build `devops/imac_deploy.sh` — a thin SSH wrapper that lets anyone on the local network run one command to rebuild the full Docker stack on the iMac.

**Read the full work order first:** `_ALX/WorkOrders/WORKORDER_Jeremy_iMacDeploy.md`

---

## THE ONE-SENTENCE DESIGN RULE

`imac_deploy.sh` does NOT contain deploy logic. It SSHs into the iMac, does a `git pull`, and calls the existing `canary_deploy.sh` there. All real logic lives in `canary_deploy.sh` already.

---

## WHAT TO BUILD

```bash
./devops/imac_deploy.sh                        # git pull + canary_deploy.sh --full
./devops/imac_deploy.sh --fast                 # Full rebuild, cached layers
./devops/imac_deploy.sh --no-test              # Full rebuild, skip pytest
./devops/imac_deploy.sh --app                  # Flask-only rebuild
./devops/imac_deploy.sh --test                 # Tests only
./devops/imac_deploy.sh --status               # Show services, no deploy
./devops/imac_deploy.sh --host 192.168.1.X     # Override iMac IP
./devops/imac_deploy.sh --help
```

Default iMac: `jeffe@192.168.10.102`, repo at `~/GrowDirect/Canary`, branch `alpha-clean`.

---

## SCRIPT FLOW

1. **SSH check** — verify connectivity before touching anything. If it fails, print a clear troubleshooting message (check network, check Remote Login enabled, check `ssh-copy-id`). Hard stop.

2. **Git pull on iMac** — `git fetch && git checkout alpha-clean && git pull`. If working tree is dirty, auto-stash first (`git stash push -m "imac_deploy auto-stash <timestamp>"`). Report branch + latest commit back to caller.

3. **Ensure canary_deploy.sh is executable** — `chmod +x devops/canary_deploy.sh`

4. **Run canary_deploy.sh on iMac** — forward the mode and any flags. Stream output live to the caller's terminal (not buffered).

5. **Report result** — on success print the demo URL (`http://192.168.10.102:5002/companion/demo`) and Flask health URL. On failure print the exit code and point to `docker logs canary_flask`.

**`--status` mode:** SSH in, run `docker compose ps`, hit Flask `/health`, print the demo URL. No deploy.

---

## ACCEPTANCE CRITERIA

All 10 ACs are in the work order. The gate test: one command, stack rebuilds on the iMac, demo URL printed at the end. No questions asked.

---

## PRIORITY NOTE

This is secondary to the smoke validation work order (`WORKORDER_Jeremy_Sprint5_SmokeValidation.md`). If you're still working on seed data or smoke testing — finish that first. This script is useful before Sprint 6 but is not required for Jim's Friday dry-run.

---

## FILE LOCATION

`Canary/devops/imac_deploy.sh` — bash, executable, `--help` flag, colored output matching `canary_deploy.sh` style.

---

## SESSION CLOSE

File timelog to `Documents/timelogs/2026/02-February/daily/2026-02-26.md`. Include deliverables with file paths.

---

*Dispatched by ALX · February 26, 2026*
