---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Work Order: B-089 / B-087 / B-088
**Flask Crash Fix + DevOps Monitor + pgAdmin Validation**

**Date:** March 2, 2026
**Assigned to:** Jeremy
**Priority:** CRITICAL (B-089) / HIGH (B-087, B-088)
**Sprint:** 6.5
**Branch:** `sprint-6-tsp`

---

## B-089 — Fix Flask Crash Loop (CRITICAL)

**Problem:** After the tech debt purge (14 files deleted, configs unified on `wsgi:app :5001`), the `canary_localhost_flask` container is crash-looping. Docker shows status `Restarting (3)` while PostgreSQL, Valkey, and pgAdmin are all healthy.

**Likely causes (check in order):**

1. **Dangling import** — one of the deleted files (`app.py`, `database.py`, `ingestion.py`, `parser_registry.py`, `square_client.py`, `chirp.py`, `init_db.py`, 8 stub blueprints) is still imported somewhere
2. **Missing dependency** — `devops_monitor.py` imports `valkey` (check `requirements.txt`)
3. **Blueprint registration** — `devops_monitor_bp` was added to `registry.py` SPECS; verify the module path resolves
4. **Template directory** — `canary/templates/devops/monitor.html` needs the `devops/` subdirectory to exist

**Debug steps:**

```bash
# 1. Pull crash logs
docker logs canary_localhost_flask 2>&1 | tail -50

# 2. If import error, grep for the missing module
grep -r "from canary.blueprints.devops_monitor" canary/
grep -r "import parser_registry" canary/
grep -r "import database" canary/

# 3. Verify blueprint registration
python -c "from canary.blueprints.registry import SPECS; print([s[0] for s in SPECS])"

# 4. Check requirements
pip show valkey

# 5. Once fixed, restart just Flask
docker compose -f devops/docker-compose.localhost.yml restart flask
```

**Acceptance criteria:**

- [ ] `docker compose up -d` — all 4 containers healthy
- [ ] `localhost:5001` — dashboard loads with no errors
- [ ] `docker logs canary_localhost_flask` — clean startup, no tracebacks

---

## B-087 — Validate DevOps Pipeline Monitor (HIGH)

**What:** New blueprint at `/devops/monitor` that shows pipeline flow in real time. Polls every 3 seconds.

**New files:**
- `canary/blueprints/devops_monitor.py` — REST API endpoints
- `canary/templates/devops/monitor.html` — single-page dashboard (dark theme, vanilla JS)
- `canary/blueprints/registry.py` — added `devops_monitor_bp` to SPECS

**Validation steps:**

1. Open `localhost:5001/devops/monitor` — dashboard renders
2. Click "Generate Transaction" — event appears in live feed
3. Watch table counts update (ingestion_log → evidence_records → transactions)
4. Check Valkey stream panel shows stream lengths and consumer lag
5. Click any event row — trace modal shows event journey through all stages
6. Verify sandbox guard: set `SQUARE_ENVIRONMENT=production`, confirm 403

**Acceptance criteria:**

- [ ] Dashboard loads and auto-polls without errors
- [ ] Generate Transaction creates visible event in feed
- [ ] Table counts increment after transaction flows through consumers
- [ ] Event trace modal works
- [ ] Sandbox-only guard blocks access in production mode

---

## B-088 — Validate pgAdmin (HIGH)

**What:** pgAdmin 4 added to Docker stack at `:5050` with all 3 databases pre-configured.

**New files:**
- `devops/pgadmin/servers.json` — pre-configured server connections
- `devops/docker-compose.localhost.yml` — pgAdmin service added

**Credentials:** `admin@canary.dev` / `canary_dev_2026`

**Validation steps:**

1. Open `localhost:5050` — pgAdmin login page
2. Login with credentials above
3. Expand server list — all 3 databases visible (canary_app, canary_sales, canary_metrics)
4. Connect to canary_app — browse schema, verify tables exist
5. Run a simple query: `SELECT COUNT(*) FROM ingestion_log;`

**Acceptance criteria:**

- [ ] pgAdmin loads and authenticates
- [ ] All 3 databases connect without additional configuration
- [ ] Can browse schema and run queries

---

## Notes

- Fix B-089 first — nothing else validates until Flask boots
- The DevOps Monitor is poll-based (not SSE) by design for v1 — works with gunicorn workers
- Action buttons in the monitor reuse sandbox_tools endpoints — no new write paths
- pgAdmin is already confirmed working (Jeffe verified login page)
