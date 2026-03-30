---
name: canary-deploy
description: |
  Orchestrates the full Canary LP deployment pipeline from dev to Demo (Mac Mini
  QA at demo.growdirect.app). Use when asked to deploy, push to Demo/QA, run
  the deployment pipeline, or check Demo health. 7-step gated pipeline with
  safety checks at each gate.
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
---

# Canary Deploy — Dev to Demo Pipeline

## Purpose

Run the full dev->Demo deployment pipeline as discrete, verifiable steps. Each step
must pass its gate check before the next step begins. No step is skipped.

**The two machines:**
| Machine | IP | Role |
|---|---|---|
| M5 MacBook Pro (dev) | 192.168.10.124 | Code lives here |
| Mac Mini (Demo/QA) | 192.168.10.102 | Demo stack runs here (demo.growdirect.app) |

**The 7-step pipeline:**
1. DEV GATE CHECK — Is dev clean and ready to push?
2. GIT PUSH — Push alpha-clean to GitHub
3. DEMO CONNECTIVITY — Can we reach the Mac Mini?
4. DEMO STACK TEARDOWN — Kill whatever's running on the Mac Mini
5. GIT PULL (on Mac Mini) — Pull latest from GitHub
6. DOCKER BUILD + UP — Rebuild containers on Mac Mini
7. VERIFY — Confirm Demo site is live and healthy

Each step has: BEFORE CHECK, ACTION, AFTER VERIFY. If any verify fails, pipeline stops.

---

## Step 1: Dev Gate Check

- Branch must be `alpha-clean`
- Working tree must be clean
- Tests must pass: `./devops/canary_deploy.sh --test`

## Step 2: Git Push

```bash
git push origin alpha-clean
```
Verify local HEAD == `origin/alpha-clean`.

## Step 3: QA Connectivity

```bash
ping -c 3 192.168.10.102
ssh -o ConnectTimeout=10 gclyle@192.168.10.102 "echo CONNECTED"
```

## Step 4: QA Stack Teardown

```bash
ssh gclyle@192.168.10.102 "cd ~/GrowDirect/Canary && docker compose -f devops/docker-compose.qa.yml down -v --remove-orphans"
```

## Step 5: Git Pull on Mac Mini

```bash
ssh -A gclyle@192.168.10.102 "cd ~/GrowDirect/Canary && git checkout alpha-clean && git pull origin alpha-clean"
```
Verify dev commit hash == QA commit hash.

## Step 6: Docker Build + Up

```bash
cd /Users/gclyle/GrowDirect/Canary && ./devops/remote_deploy.sh
```
Gate: all 7 services healthy, all 3 migrations at head, 0 test failures, smoke green.

## Step 7: QA Verify

```bash
curl -sf http://192.168.10.102:5001/health
./devops/remote_deploy.sh --status
```

---

## Quick Reference

```bash
./devops/remote_deploy.sh          # Full pipeline
./devops/remote_deploy.sh --status # Check QA without deploying
./devops/canary_deploy.sh --test   # Tests only (local)
./devops/canary_deploy.sh --full   # Full local deploy (on Mac Mini)
./devops/canary_deploy.sh --app    # Flask-only rebuild (keep DBs)
./devops/canary_deploy.sh --migrate all  # Migrations only
```

## Safety Rules

1. Never push to QA with failing tests
2. Always teardown before pulling
3. Verify commit hashes are in sync before building
4. Never declare QA healthy without smoke check
5. Log every deploy — report saved to `deploy_reports/`

---

*Canary Deploy v1.0 — Dev to Demo Pipeline*
