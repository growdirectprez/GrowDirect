---
type: workorder
domain: infra
status: active
created: 2026-03-18
updated: 2026-03-19
---
# WORK ORDER: Jeremy — Local Pre-UAT Deployment Pipeline (`canary_deploy.sh`)
*Issued by ALX · February 24, 2026 · Priority: 🟡 HIGH — Sprint 5 critical path enabler*

**Context:** We're 7 days from UAT (March 3). Before we push anything to the iMac over SSH, we need to prove the full deployment works locally on Jeffe's MacBook. One script. Zero assumptions. Every run proves the code is deployable.

**Goal:** Build `devops/canary_deploy.sh` — a single deployment script with four modes that covers every real-world deployment scenario. This becomes THE deployment path for both local pre-UAT and (Phase 2) remote iMac deployment.

**Jeffe directive:** "If we have a local pre-UAT environment we can make sure our code drops and deployments are clean and we assume a full environment prerequisite check and rebuild every time."

---

## THE FOUR MODES

The script has four operating modes. Each mode runs only the checks and actions appropriate to its scope. **Tests always run unless `--no-test` is explicitly passed.**

```bash
./devops/canary_deploy.sh --full                  # Nuke everything, rebuild from scratch
./devops/canary_deploy.sh --app                   # Rebuild Flask only, keep DBs (or run SQLite-mode)
./devops/canary_deploy.sh --migrate app,sales      # Run migrations on specific DB(s), restart app
./devops/canary_deploy.sh --test                   # Just run pytest against whatever's running
```

### Mode Summary

| Mode | Preflight Scope | Teardown | Build | Migrate | Test |
|---|---|---|---|---|---|
| `--full` | Everything (Docker, Git, env, ports, disk) | All containers + all volumes | All images (no-cache) | All 3 DBs | ✅ |
| `--app` | Docker running (if Postgres expected), env exists, Git clean | Flask container only | Flask image only | None | ✅ |
| `--migrate <db>` | Docker running, target DB(s) healthy | Flask container (restart after migrate) | None | Specified DB(s) only | ✅ |
| `--test` | Flask reachable (Docker or local venv) | None | None | None | ✅ |

---

## MODE 1: `--full` — Clean Room Deployment

This is the "prove it works from nothing" mode. Used for: starting a new test cycle, validating after major changes, pre-UAT confidence check.

### Phase 1: PREFLIGHT (zero assumptions)

Check every prerequisite. Any failure = hard stop with a clear, actionable error message (not a Docker stack trace).

| Check | How | Fail action |
|---|---|---|
| Git installed | `git --version` | Hard stop |
| Git branch | `git branch --show-current` | Report branch, warn if not `alpha-clean` or `main` |
| Git working tree | `git status --porcelain` | Warn if dirty (don't block — dev may have local changes) |
| Docker installed | `docker --version` | Hard stop |
| Docker daemon running | `docker info` | Hard stop: "Start Docker Desktop" |
| Docker memory | `docker info --format '{{.MemTotal}}'` ≥ 8GB | Hard stop: "Allocate at least 8GB to Docker Desktop" |
| Docker Compose | `docker compose version` | Hard stop |
| Python 3.11+ | `python3 --version` | Hard stop |
| `.env.alpha3x` exists | `test -f devops/.env.alpha3x` | Hard stop: "Copy .env.alpha3x.template" |
| `.env.alpha3x` no placeholders | `grep CHANGE_ME` | Hard stop: "Fill in all CHANGE_ME values" |
| Required ports free | Check 5432, 5001, 6379 | Hard stop: "Port in use — kill the process or change the port" |
| Disk space | ≥ 10GB free | Warn |

### Phase 2: TEARDOWN

```bash
docker compose --env-file devops/.env.alpha3x -f devops/docker-compose.alpha3x.yml down -v
docker image prune -f  # optional: only dangling images
```

Remove all named volumes (postgres_data, valkey_data, flask_data, etc.). This is the zero-assumptions guarantee.

### Phase 3: BUILD

```bash
docker compose --env-file devops/.env.alpha3x -f devops/docker-compose.alpha3x.yml build --no-cache
```

Builds the Flask image from `devops/Dockerfile`. Pulls latest upstream images.

Add `--fast` flag to skip `--no-cache` for quick iteration when you know the base hasn't changed.

### Phase 4: UP

```bash
docker compose --env-file devops/.env.alpha3x -f devops/docker-compose.alpha3x.yml up -d
```

Core profile (default): Postgres, Valkey, PgBouncer, Flask, Superset, Airflow (7 services).

Wait for health checks with a **per-service timeout** and clear status reporting:

```
[WAITING] postgres .......... ✅ healthy (8s)
[WAITING] valkey ............. ✅ healthy (3s)
[WAITING] pgbouncer ......... ✅ healthy (2s)
[WAITING] flask .............. ✅ healthy (12s)
[WAITING] superset ........... ✅ healthy (45s)
[WAITING] airflow-webserver .. ✅ healthy (60s)
[WAITING] airflow-scheduler .. ✅ running (no healthcheck)
```

**Global timeout: 5 minutes.** If any service isn't healthy by then → hard stop with `docker logs <service>` tail.

### Phase 5: MIGRATE

Run Alembic migrations inside the Flask container:

```bash
docker exec canary_flask alembic -c canary/migrations/alembic.ini upgrade head
docker exec canary_flask alembic -c canary/migrations/sales/alembic.ini upgrade head
docker exec canary_flask alembic -c canary/migrations/metrics/alembic.ini upgrade head
```

**Verification:** After each migration, verify:
- `alembic_version` table exists and has a row
- For canary_app: `pgcrypto` extension loaded, `keycloak`/`hasura`/`airflow`/`superset` schemas exist
- For canary_sales: `pgcrypto` extension loaded

Report migration status per database.

### Phase 6: TEST

```bash
docker exec canary_flask pytest tests/ -v --tb=short \
  --ignore=tests/browser --ignore=tests/e2e \
  -m "not docker"
```

**Hard gate:** Any test failure = script exits non-zero. No "deployment successful" message.

Report format:
```
═══ TEST RESULTS ═══════════════════════════════
  Passed:  541
  Failed:  0
  Errors:  0
  Skipped: 216
  VERDICT: ✅ GREEN
```

### Phase 7: SMOKE

```bash
curl -sf http://localhost:5001/health || exit 1
```

Verify Flask responds on the expected port. Optionally hit `/login` to verify template rendering.

### Phase 8: REPORT

```
╔══════════════════════════════════════════════════╗
║  CANARY DEPLOYMENT REPORT                         ║
╠══════════════════════════════════════════════════╣
║  Mode:       --full                               ║
║  Branch:     alpha-clean                          ║
║  Commit:     a1b2c3d (2026-02-24 10:30:00)        ║
║  Timestamp:  2026-02-24T10:35:22-08:00            ║
║                                                    ║
║  SERVICES                                          ║
║    postgres ........... ✅ healthy                  ║
║    valkey ............. ✅ healthy                  ║
║    pgbouncer .......... ✅ healthy                  ║
║    flask .............. ✅ healthy                  ║
║    superset ........... ✅ healthy                  ║
║    airflow-web ........ ✅ healthy                  ║
║    airflow-sched ...... ✅ running                  ║
║                                                    ║
║  MIGRATIONS                                        ║
║    canary_app ......... ✅ head                     ║
║    canary_sales ....... ✅ head                     ║
║    canary_metrics ..... ✅ head                     ║
║                                                    ║
║  TESTS                                             ║
║    541 passed / 0 failed / 216 skipped             ║
║                                                    ║
║  SMOKE                                             ║
║    /health ............ ✅ 200 OK                   ║
║                                                    ║
║  ELAPSED: 3m 42s                                   ║
║                                                    ║
║  ✅ DEPLOYMENT SUCCESSFUL — READY FOR UAT          ║
╚══════════════════════════════════════════════════╝
```

Save this report to `devops/deploy_reports/DEPLOY_<timestamp>.txt` for audit trail.

---

## MODE 2: `--app` — Application Rebuild Only

**Use case:** Jeremy pushed new Flask code. Databases are fine. Just redeploy the app and re-test.

**Key design decision (Jeffe directive):** `--app` does NOT require Postgres to be running. It should work in two contexts:
- **Docker stack is up:** Rebuild Flask container, restart it, test against Postgres
- **No Docker stack:** Run Flask in venv against SQLite (the old deploy_qa.sh path)

### Preflight:
- Git, Python present
- `.env` or `.env.alpha3x` exists
- If Docker is running AND canary_postgres is healthy → Docker app mode
- If Docker is not running OR no Postgres container → SQLite/venv mode (auto-detect)

### Docker app mode:
```bash
docker compose --env-file devops/.env.alpha3x -f devops/docker-compose.alpha3x.yml up -d --build flask
```
Rebuilds only the Flask image. Other services untouched. Then run tests inside the container.

### SQLite/venv mode:
```bash
source venv/bin/activate  # or create venv if missing
pip install -r requirements.txt -r requirements-dev.txt --quiet
pytest tests/ -v --tb=short --ignore=tests/browser --ignore=tests/e2e -m "not docker and not postgres"
```

Report indicates which mode was used.

---

## MODE 3: `--migrate <databases>` — Selective Migration

**Use case:** New Alembic migration landed for canary_sales. Don't touch canary_app or canary_metrics.

```bash
./devops/canary_deploy.sh --migrate sales          # just canary_sales
./devops/canary_deploy.sh --migrate app,sales       # canary_app + canary_sales
./devops/canary_deploy.sh --migrate all             # same as --full minus teardown/rebuild
```

### Preflight:
- Docker running
- Target database(s) healthy and reachable
- Flask container running

### Actions:
1. Run Alembic `upgrade head` on specified database(s) only
2. Restart Flask container (to pick up any model changes)
3. Run full test suite

---

## MODE 4: `--test` — Test Only

**Use case:** "Where are we? Just run the tests."

### Preflight:
- Either Flask container is running (Docker) OR venv is available (local)
- Auto-detect which, same as `--app`

### Actions:
- Run pytest. Report results. That's it.

---

## GLOBAL FLAGS

| Flag | Effect | Available in |
|---|---|---|
| `--no-test` | Skip pytest (for debugging compose/build issues) | All modes |
| `--fast` | Use cached Docker builds (skip `--no-cache`) | `--full`, `--app` |
| `--profile qa` | Also bring up Keycloak, Hasura, Directus, Nginx | `--full` |
| `--verbose` | Show full Docker/pytest output (not just summary) | All modes |
| `--quiet` | Minimal output — just pass/fail per phase | All modes |
| `--report-only` | Show last deployment report without running anything | N/A |

---

## ACCEPTANCE CRITERIA

1. **AC-1:** `./devops/canary_deploy.sh --full` from a fresh `git clone` on Jeffe's MacBook produces a running, tested, healthy stack with zero manual steps.
2. **AC-2:** Running `--full` twice in a row produces identical results (idempotent).
3. **AC-3:** Any prerequisite failure in any mode produces a clear, actionable error message — not a Docker stack trace.
4. **AC-4:** `--app` auto-detects Docker vs. SQLite/venv mode and works in both contexts.
5. **AC-5:** `--migrate sales` runs only canary_sales migrations, does not touch canary_app or canary_metrics.
6. **AC-6:** Test gate is enforced in all modes (unless `--no-test`). Failed tests = non-zero exit code + no success message.
7. **AC-7:** Deployment report is saved to `devops/deploy_reports/` with timestamp.
8. **AC-8:** Script is executable, has a help flag (`--help`), and uses colored output consistent with existing scripts (preflight.sh style).

---

## FILE LOCATIONS

| File | Path | Notes |
|---|---|---|
| The script | `Canary/devops/canary_deploy.sh` | Executable, bash |
| Deploy reports | `Canary/devops/deploy_reports/` | Gitignored, local audit trail |
| Env file (alpha3x) | `Canary/devops/.env.alpha3x` | Already exists |
| Env template | `Canary/devops/.env.alpha3x.template` | Already exists |
| Docker compose (alpha3x) | `Canary/devops/docker-compose.alpha3x.yml` | Existing — no changes needed |
| Docker compose (dev/test) | `Canary/devops/docker-compose.yml` | Existing — no changes needed |
| Dockerfile | `Canary/devops/Dockerfile` | Existing — no changes needed |
| Init DB SQL | `Canary/devops/init-db/01-create-databases.sql` | Existing — no changes needed |

---

## WHAT THIS REPLACES

Nothing gets deleted. But:
- `canary_deploy.sh --full` supersedes the manual sequence of `docker compose down -v && docker compose build && docker compose up`
- `canary_deploy.sh --app` supersedes `deploy_qa.sh` for local testing
- `canary_deploy.sh --test` supersedes `make test` for deployment-context testing

---

## DEPENDENCIES

- None on other agents. This is pure Jeremy work.
- Requires existing `.env.alpha3x` to be populated (already done per devops/.env.alpha3x).
- Does NOT require iMac access — this is local-only for now.

---

## FUTURE (Phase 2 — not this work order)

- `--remote <host>` flag: SSH into iMac, pull latest git, run the same script remotely
- Integration with GitHub Actions (CI runs `canary_deploy.sh --full` on every PR)
- Slack notification on deploy success/failure (after B-013 Slack workspace is up)

---

## ESTIMATED EFFORT

**1 day.** The building blocks all exist (Dockerfile, compose files, Makefile targets, preflight.sh patterns). This is assembly + polish + the auto-detect logic for `--app` mode.

**Priority relative to Sprint 5 Phase 2:** Phase 2 is DONE (verified Feb 24, commit `5effb5e`). Deploy script is now the enabler for Phase 3.

**🔴 REVISED PRIORITY (Feb 25 — Jeffe directive): Level B Guided Demo by Friday Feb 28.**

Jeffe is targeting a guided in-person demo with a real SoCal Square merchant (Offset Coffee, Torrance — 5-6 locations, full Square stack) on Monday March 3. This changes Jeremy's priority sequencing for the week:

**Suggested sequence (UPDATED):**
1. `canary_deploy.sh --full` working — **Wednesday Feb 26** (gets the stack serving)
2. **Today's View UI rendering (Art v1.1 wireframe implemented)** — **Wednesday-Thursday** 🔴 THIS IS THE DEMO CENTERPIECE
3. **Process 4 wizard functional (cash variance threshold → 6-step flow)** — **Thursday** 🔴 THIS IS THE "DO SOMETHING" MOMENT
4. **Coffee-shop seed data loaded** (realistic transactions for a specialty coffee chain — Jim provides spec) — **Thursday-Friday**
5. **Phone/tablet access via local Wi-Fi or ngrok tunnel** — **Friday**
6. iMac deployment — **using the script, after local validation**

**What is NOT required for Monday March 3 Level B demo:**
- Square OAuth sandbox (seed data is fine)
- Webhook ingestion E2E (deferred)
- Role gating (only testing owner persona)
- Multi-location switcher (nice-to-have, can show single location)
- Hawk ENV 2-4 pipeline (ENV 1 local dev is enough)

**The test:** Can a merchant hold a phone, see Today's View, tap a Chirp, walk through Process 4, and say "I get it"? If yes, demo succeeds.

---

*Issued by ALX. Dispatch to Jeremy via Cowork or Code tab.*
*Acceptance review: Jim runs the script on a clean checkout. If Jim can deploy without asking Jeremy a question, it passes.*
