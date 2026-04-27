---
name: alx-startup
roles-primary: [ALX]
roles-assist: [DevOps, QA]
description: |
  Session startup for the Mac mini UAT site (canary.growdirect.app).
  Run at the start of every Canary session on the mini. Checks shared
  infra, Canary stack, Cloudflare tunnel, and domain reachability.
  Diagnoses and surfaces any issues before work begins.
allowed-tools:
  - Bash
  - Read
---

# ALX Startup — Mini UAT Site

Run this at the start of every session on the mini. Target:
**`canary.growdirect.app`** → `canary-qa` tunnel (831b63d5) → localhost:5001

---

## Phase 1 — Git Health

```bash
git status --short && git branch --show-current
```

Verify: on `main`, no unexpected untracked files or modified tracked files.
If on a feature branch or there are staged changes, surface this before
doing any work.

---

## Phase 2 — Shared Infrastructure

```bash
docker ps --format "table {{.Names}}\t{{.Status}}" | grep -E "growdirect_(postgres|valkey|ollama|pgadmin)|NAME"
```

Expected containers: `growdirect_postgres` (healthy), `growdirect_valkey`
(healthy). `growdirect_ollama` and `growdirect_pgadmin` can be unhealthy —
they're non-blocking.

**If postgres or valkey is missing:**
```bash
cd ~/GrowDirect/devops && docker compose up -d
```
If that fails with "POSTGRES_PASSWORD missing", the devops/.env is absent.
Check with the founder before recreating it — it contains production credentials.

---

## Phase 3 — Canary Stack

```bash
docker ps --format "table {{.Names}}\t{{.Status}}" | grep -E "canary_|NAME"
```

Expected containers and acceptable states:

| Container | Expected |
|---|---|
| `canary_flask` | Up, healthy |
| `canary_localhost_nginx` | Up (unhealthy OK — IPv6 healthcheck bug) |
| `canary_localhost_tsp_sub1` | Up, healthy |
| `canary_localhost_tsp_sub2` | Up, healthy |
| `canary_localhost_tsp_sub3` | Up, healthy |
| `canary_localhost_tsp_sub4` | Up, healthy |
| `canary_localhost_owl_mcp` | Up, healthy |
| `canary_localhost_qa_agent` | Up, healthy |

**If any container is missing or exited:**
```bash
cd ~/GrowDirect/Canary && docker compose -f devops/docker-compose.localhost.yml up -d
```

**If Flask fails to start** (most common issue):
```bash
docker logs canary_flask --tail 50
```
Look for: import errors (rebuild image), DB connection refused (infra not up),
missing env vars (check .env).

**Force rebuild** (new packages or Dockerfile change):
```bash
cd ~/GrowDirect/Canary && docker compose -f devops/docker-compose.localhost.yml up -d --build flask
```

---

## Phase 4 — Local Flask Health

```bash
curl -s http://localhost:5001/health | python3 -m json.tool
```

Expected: `{"service":"canary-lp","status":"ok","version":"..."}`.

If this fails, Flask is not up. Check Phase 3.

---

## Phase 5 — Cloudflare Tunnel

```bash
pgrep -la cloudflared
```

Expected: cloudflared process running with
`--config /Users/gclyle/.cloudflared/config.yml run`

**If not running:**
```bash
cloudflared tunnel run canary-qa > /tmp/cloudflared.log 2>&1 &
sleep 3 && pgrep -la cloudflared
```

**Verify canary.growdirect.app is in the ingress config:**
```bash
grep "canary.growdirect.app" ~/.cloudflared/config.yml
```

Expected: `- hostname: canary.growdirect.app` with `service: http://localhost:5001`

**If missing**, add it:
```bash
# Edit ~/.cloudflared/config.yml to add the ingress rule before dev.growdirect.app:
#   - hostname: canary.growdirect.app
#     service: http://localhost:5001
# Then reload:
kill -HUP $(pgrep cloudflared)
```

**Verify DNS routes to this tunnel (canary-qa / 831b63d5):**
The Cloudflare DNS for `canary.growdirect.app` must CNAME to
`831b63d5-4957-4f64-9c16-e45b82c5b936.cfargotunnel.com`.

Test:
```bash
curl -s -o /dev/null -w "%{http_code}" https://canary.growdirect.app/health
```

Expected: 200. If you get anything else or no new log entries appear in
`docker logs canary_flask`, the Cloudflare DNS record still points elsewhere
(likely an A record for an EC2 instance). Fix in the Cloudflare dashboard:
- Zone: `growdirect.app`
- Record: `canary` → CNAME → `831b63d5-4957-4f64-9c16-e45b82c5b936.cfargotunnel.com`
- Proxied: yes

Note: `cloudflared tunnel route dns canary-qa canary.growdirect.app` fails
because the cloudflared credentials don't have edit access to the
`growdirect.app` zone — the fix requires the Cloudflare dashboard.

---

## Phase 6 — Smoke Test via Public Domain

```bash
# Health
curl -s -o /dev/null -w "health: %{http_code}\n" https://canary.growdirect.app/health

# Login page
curl -s -o /dev/null -w "login: %{http_code}\n" https://canary.growdirect.app/auth/login-page

# QA agent
curl -s -o /dev/null -w "qa-agent: %{http_code}\n" http://localhost:8002/health
```

Expected: all 200.

---

## Phase 7 — Load Session Context

```bash
# Via memory bus CLI (if context needed):
cd ~/GrowDirect/services/memory-bus && python3 -m memory_bus.cli recall "canary session context"
```

Or call `session_start` via the `canary-alx` MCP server if available.

---

## Status Report Format

```
ALX STARTUP — Mini UAT
Date:       [timestamp]
Domain:     canary.growdirect.app
Tunnel:     canary-qa (831b63d5)
Branch:     [branch name]
───────────────────────────────
Phase 1 — Git              [OK / WARN: description]
Phase 2 — Shared Infra     [OK / FAIL: description]
Phase 3 — Canary Stack     [OK / FAIL: description]
Phase 4 — Flask Health     [OK / FAIL: description]
Phase 5 — Tunnel           [OK / FAIL: description]
Phase 6 — Smoke (domain)   [OK / FAIL: description]
───────────────────────────────
RESULT:  [READY / BLOCKED]

Open issues:
- [list any failures and remediation steps]
```

Stop and surface any FAIL before doing any work.

---

## Quick Restart (all services)

If everything is down and you need a clean boot:

```bash
# 1. Shared infra
cd ~/GrowDirect/devops && docker compose up -d

# 2. Canary stack
cd ~/GrowDirect/Canary && docker compose -f devops/docker-compose.localhost.yml up -d

# 3. Wait for Flask health
until curl -sf http://localhost:5001/health > /dev/null; do sleep 2; done && echo "Flask up"

# 4. Cloudflared (if not running)
pgrep cloudflared || cloudflared tunnel run canary-qa > /tmp/cloudflared.log 2>&1 &
```

---

*alx-startup v1.0 — Mini UAT site (canary.growdirect.app)*
