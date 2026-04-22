---
name: canary-uat
roles-primary: [Jim]
roles-assist: [Eva]
description: |
  Quick UAT health check for the Canary build. Use when Jeffe or any team member
  says: 'check the app', 'is the app working', 'run UAT', 'health check',
  'test the build', 'smoke test', 'is the site up', 'check localhost', 'validate
  the deployment'. 6-step workflow under 60 seconds.
allowed-tools:
  - Bash
  - Read
---

# Canary UAT — Quick Health Check

A lightweight validation that confirms the Canary build is alive, serving pages,
and not throwing errors. Under 60 seconds.

## When to Run

- After any code change or git pull
- After Docker container restart
- After environment variable changes
- Before handing off for QA
- Whenever someone says "is it working?"

## Health Check Workflow

Run in order. Stop on first failure.

### Step 1: Health Endpoint (Critical)

```bash
curl -s http://localhost:5001/health
```

Expected: `{"service":"canary-lp","status":"ok","version":"..."}`.
If this fails, the app is not running.

### Step 2: Login Page Renders

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/
```

Expected: HTTP 200 or 302.

### Step 3: Static Assets Load

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/static/css/canary.css
curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/static/js/canary.js
```

Expected: HTTP 200.

### Step 4: Key Route Responses

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/dashboard
curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/admin
curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/fox
curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/settings
curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/authorize
```

Expected: HTTP 200 or 302. 404 = route not registered. 500 = code error.

### Step 5: Error Log Scan

```bash
docker compose -f devops/docker-compose.yml logs --tail=50 dev 2>&1 | grep -i "error\|traceback\|exception"
```

Expected: No tracebacks.

### Step 6: Browser Visual Check (if Chrome MCP available)

Navigate to `http://localhost:5001` and screenshot. Verify login page renders
with branding, CSS loading, no JS errors.

## Report Format

```
CANARY UAT — HEALTH CHECK REPORT
Date:     [timestamp]
Target:   http://localhost:5001
Version:  [from /health response]
──────────────────────────────────
Step 1: Health Endpoint    [status]
Step 2: Login Page         [status]
Step 3: Static Assets      [status]
Step 4: Key Routes         [status]
Step 5: Error Log          [status]
Step 6: Browser Visual     [status]
──────────────────────────────────
RESULT:  [PASS/FAIL] (N/N checks)
```

---

*Canary UAT v1.0 — Quick Health Check*
