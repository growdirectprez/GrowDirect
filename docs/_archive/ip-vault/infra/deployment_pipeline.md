---
type: spec
domain: infra
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Canary LP — Deployment Pipeline

> Last updated: 2026-03-07

---

## Environments

| Environment | Machine | IP | URL | Compose File |
|-------------|---------|-----|-----|-------------|
| **Dev** | Mac Mini M4 | 192.168.10.102 | https://dev.growdirect.app | `docker-compose.localhost.yml` |
| **QA** | iMac | 192.168.10.117 | https://qa.growdirect.app (pending) | `docker-compose.qa.yml` |

Both machines are on the same wired LAN segment (192.168.10.x) behind the DSR-250 router.

---

## Deploy Scripts

### `canary_deploy.sh` — Local Stack Orchestration

**Location:** `devops/scripts/canary_deploy.sh`
**Runs on:** Any machine with Docker + repo clone
**Purpose:** Build, migrate, test, report — the universal deploy script

**Modes:**
| Flag | What It Does |
|------|-------------|
| `--full` | Nuke containers + volumes, rebuild from scratch, migrate, test |
| `--app` | Rebuild Flask container only (fast iteration) |
| `--migrate <db>` | Run Alembic migrations (app / sales / metrics / all) |
| `--test` | Run pytest only (unit + integration) |
| `--no-test` | Skip test phase |
| `--fast` | Use Docker cache (no `--no-cache`) |
| `--profile qa` | QA profile settings |
| `--verbose` / `--quiet` | Output control |
| `--report-only` | Show last deployment report |

**What `--full` does (in order):**
1. Preflight checks (Docker, Python, ports, disk, env validation)
2. Teardown (containers + volumes + database reset)
3. Build Docker images
4. Start services with health monitoring
5. Alembic migrations (canary_app, canary_sales, canary_metrics)
6. Run pytest (all 3 layers) in container
7. Smoke test (`/health` endpoint)
8. Write timestamped report to `devops/deploy_reports/`

### `remote_deploy.sh` — Remote QA Deployment

**Location:** `devops/scripts/remote_deploy.sh`
**Runs from:** Mac Mini (or anywhere with SSH access to iMac)
**Purpose:** Push code to QA via SSH

**Modes:**
| Flag | What It Does |
|------|-------------|
| (default) | Full rebuild on iMac |
| `--status` | Check stack health without rebuilding |
| `--logs [service]` | Tail service logs on iMac |
| `--branch <name>` | Checkout specific branch before build |
| `--fast` | Use Docker cache |
| `--no-test` | Skip pytest |

**What it does:**
1. SSH to iMac (`gclyle@192.168.10.117` via `~/.ssh/id_canary`)
2. Preflight checks (SSH connectivity, Docker, repo state, env file)
3. `git pull` (or checkout `--branch`)
4. Run `canary_deploy.sh --full` remotely on iMac
5. Stream output back to caller
6. Print summary with Flask URL and demo access

### `deploy.sh` — Legacy (Obsolete)

**Location:** `devops/scripts/deploy.sh`
**Status:** Superseded by `remote_deploy.sh`. Do not use.

---

## SSH Configuration

```
Host imac 192.168.10.117
  HostName 192.168.10.117
  User gclyle
  IdentityFile ~/.ssh/id_canary
```

**Keys:**
| Key | Purpose |
|-----|---------|
| `~/.ssh/id_canary` | SSH to iMac for deployments |
| `~/.ssh/id_github_canary` | Git operations on iMac (pull from GitHub) |

---

## Docker Compose Files

| File | Environment | Services |
|------|-------------|----------|
| `docker-compose.localhost.yml` | Dev (Mac Mini) | nginx, Flask, PostgreSQL, Valkey, pgAdmin, TSP sub1-4 |
| `docker-compose.qa.yml` | QA (iMac) | Flask, PostgreSQL, Valkey, pgAdmin |
| `docker-compose.canary.yml` | Full enterprise | 11 core + 4 QA profile services |
| `docker-compose.prod.yml` | Production | Template only — not deployed |

---

## Database Architecture

All environments create the same 3-database structure:

| Database | Purpose |
|----------|---------|
| `canary_app` | Auth, merchants, alerts, Fox cases, audit log |
| `canary_sales` | Transactions, refunds, cash drawer, loyalty |
| `canary_metrics` | Star schema, fiscal calendars, scorecards |

**Init script:** `devops/init-db/01-create-databases.sql` — runs on container startup, creates DBs + extensions (pgcrypto, uuid-ossp) + RLS helper functions.

**Migrations:** Alembic, 3 separate migration chains:
- `canary/migrations/versions/` — canary_app
- `canary/migrations/sales/versions/` — canary_sales
- `canary/migrations/metrics/versions/` — canary_metrics

---

## Test Gates

Three-layer strategy. All layers run during deploy unless `--no-test` is used.

| Layer | Location | What | Runner | Gate |
|-------|----------|------|--------|------|
| **Unit** | `tests/unit/` | Business logic, no DB | `pytest tests/unit/` | Blocks merge |
| **Integration** | `tests/integration/` | PostgreSQL end-to-end | `pytest tests/integration/ -m postgres` | Must pass before QA push |
| **Smoke** | `tests/smoke/` | HTTP against live stack | `pytest tests/smoke/` | Must pass after every rebuild |

---

## Cloudflare Tunnels

**Tunnel:** `canary-qa` (ID: 831b63d5-4957-4f64-9c16-e45b82c5b936)

Two machines, two `cloudflared` processes, both always-on, both connected to the same tunnel. Hostname-based routing sends traffic to the right machine.

| Hostname | Machine | cloudflared Config | Routes To |
|----------|---------|-------------------|-----------|
| dev.growdirect.app | Mac Mini (.102) | Local config (`~/.cloudflared/config.yml`) | localhost:5001 |
| qa.growdirect.app | iMac (.117) | Token-based (Cloudflare dashboard) | localhost:5001 |

**Mac Mini config:** `~/.cloudflared/config.yml`
```yaml
tunnel: 831b63d5-4957-4f64-9c16-e45b82c5b936
credentials-file: /Users/geofflyle/.cloudflared/831b63d5-...json

ingress:
  - hostname: dev.growdirect.app
    service: http://localhost:5001
  - service: http_status:404
```

**iMac:** Runs `cloudflared tunnel run --token <token>` — routing managed in Cloudflare Zero Trust dashboard, not a local config file.

**Key point:** Both tunnels are always-on. When we deploy to QA (iMac), the tunnel picks up the new container automatically. No tunnel restart needed on either machine.

---

## Environment Files

| File | Location | Purpose |
|------|----------|---------|
| `.env` | Repo root | Dev credentials + DB URLs. **Never overwrite.** |
| `.env.template` | Repo root | Reference template for `.env` variables |
| `.env.canary` | `devops/` | Enterprise stack config (used by `canary_deploy.sh`) |

---

## Dev Workflow — Daily Cycle

### Quick iteration (code change → verify):
```bash
# Edit files, then rebuild Flask only:
cd ~/GrowDirect/Canary && docker compose -f devops/docker-compose.localhost.yml up -d --build flask
```

### Full local rebuild:
```bash
cd ~/GrowDirect/Canary && ./devops/scripts/canary_deploy.sh --full
```

### Run tests only:
```bash
cd ~/GrowDirect/Canary && ./devops/scripts/canary_deploy.sh --test
```

### Push to QA:
```bash
cd ~/GrowDirect/Canary && ./devops/scripts/remote_deploy.sh
```

### Check QA status:
```bash
cd ~/GrowDirect/Canary && ./devops/scripts/remote_deploy.sh --status
```

### Check QA logs:
```bash
cd ~/GrowDirect/Canary && ./devops/scripts/remote_deploy.sh --logs flask
```

---

## Deployment Reports

`canary_deploy.sh` writes timestamped reports to `devops/deploy_reports/DEPLOY_YYYYMMDD_HHMMSS.txt`:
- Branch + commit info
- Service health status
- Migration revision numbers
- Test results (passed / failed / skipped)
- Smoke test results
- Final verdict (SUCCESS or FAILED)

Review last report: `./devops/scripts/canary_deploy.sh --report-only`

---

## Known Gaps

| Gap | Impact | Priority |
|-----|--------|----------|
| `qa.growdirect.app` tunnel routing not configured | QA not accessible externally | Medium — easy fix |
| No incremental deploys | Every QA push is a full nuke + rebuild | Low — acceptable for current scale |
| No rollback script | Must redeploy previous commit manually | Medium |
| No CI/CD (GitHub Actions) | Tests only run locally | Low — pre-revenue |
| No `.env.canary.template` in repo | Manual env setup for new machines | Low |
| No blue-green deployments | Single stack per environment | Low — future |
