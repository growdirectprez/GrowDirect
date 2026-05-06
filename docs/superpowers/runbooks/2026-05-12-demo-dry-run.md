---
title: Demo Dry Run — May 12, 2026
runbook-id: demo-dry-run-2026-05-12
version: 1
status: ready
domain: canary
linear: GRO-802
last-compiled: 2026-05-06
---

# Demo Dry Run — May 12, 2026

End-to-end verification of the GRO-802 demo system. Executable by a fresh session with no assumed chat state. Every step has an expected output — if the output doesn't match, the contingency table at the end of each section tells you what to do.

**Target state:** `demo.growdirect.io` walks through a complete Square OAuth sandbox connection and shows real data. `canary.growdirect.io` reads cleanly as a technical vault. `/.well-known/mcp.json` returns a usable discovery document. A Claude Code instance can connect to `POST /mcp` and enumerate tools.

**Time estimate:** 45–60 minutes end-to-end, including contingency time.

**Abort condition:** if any §1–§4 check fails and cannot be resolved in 30 minutes, slip the demo by 24 hours. Do not run the demo against a broken system.

---

## Pre-flight

Before running any section, confirm:

- [ ] `main` branch is current — `git pull origin main` from GrowDirect root
- [ ] You have access to the GCP console for project `canary-rapidpos`
- [ ] Square sandbox credentials are available (SQUARE_APPLICATION_ID, SQUARE_APPLICATION_SECRET in Secret Manager)
- [ ] A demo API key exists in `app.api_keys` — see §4 to provision one if not

---

## §1 — DNS and TLS

Verify both subdomains resolve and TLS is clean.

```bash
# demo subdomain
curl -sI https://demo.growdirect.io/health | head -5

# vault
curl -sI https://canary.growdirect.io | head -5
```

**Expected:**

```
HTTP/2 200
content-type: application/json
```

for demo (health returns JSON), and `HTTP/2 200` for the vault.

**If demo returns a connection error or 5xx:** check Cloud Run service status in GCP Console → Cloud Run → `canary-gateway-staging`. If the service is not running, trigger a deploy:

```bash
cd CanaryGo
gcloud builds submit \
  --config=deploy/cloudbuild.gateway.yaml \
  --project=canary-rapidpos \
  .
```

**If vault returns 404 or connection error:** check GitHub Pages build status at `github.com/growdirectprez/canary-site/actions`. Pages builds usually complete within 2 minutes of a push.

---

## §2 — Square OAuth flow

This is the core demo. Walk it completely before any audience is present.

### 2a — Connect flow

1. Navigate to `https://demo.growdirect.io/auth/square` in a fresh browser tab (not incognito — Square sandbox needs cookies).
2. **Expected:** landing page with "Connect Square" button and the Canary bird mark.
3. Click **Connect Square**.
4. **Expected:** redirected to Square's OAuth consent screen for the sandbox application. The app name should match `SQUARE_APPLICATION_ID` registered in the sandbox.
5. Authorize the connection.
6. **Expected:** redirected to `https://demo.growdirect.io/dashboard` with:
   - Merchant name (sandbox business name)
   - At least one location
   - Payment list (may be empty in fresh sandbox — see §2b)

### 2b — Sandbox data check

If the dashboard shows no payments, seed the sandbox:

1. Log in to the [Square Sandbox Dashboard](https://developer.squareup.com/apps) → your sandbox test account.
2. Create a test transaction via the Square Sandbox Seller Dashboard → Transactions → New transaction.
3. Reload `https://demo.growdirect.io/dashboard`.
4. **Expected:** transaction appears in the payment list within 15 seconds (webhook pipeline) or on manual page reload.

### 2c — Disconnect and reconnect

1. Navigate to `https://demo.growdirect.io/auth/square/disconnect`.
2. **Expected:** redirected back to `/auth/square` with the connect button. No error.
3. Reconnect by repeating 2a. Confirm the dashboard loads again.
4. This verifies the token lifecycle (store → load → refresh) is clean.

### 2d — Devops panel check

1. Navigate to `https://demo.growdirect.io/devops/square`.
   *(Note: `/devops` is gated by `DEV_CONSOLE=1` env var in the Cloud Run config. If it 404s, check that the env var is set in the staging service.)*
2. **Expected:** connections table shows the sandbox merchant with status `active`, `expires_at` populated, and no `expired`/`expiring soon` badges.
3. Click **Test** on the connection row.
4. **Expected:** `✓ <business name>` appears within 3 seconds.

---

## §3 — Vault

Verify `canary.growdirect.io` is complete and readable.

```bash
# Landing page
curl -sI https://canary.growdirect.io | grep -E "HTTP|content-type"

# SDD index
curl -sI https://canary.growdirect.io/sdds/ | grep HTTP

# Coding standards
curl -sI https://canary.growdirect.io/coding-standards | grep HTTP
```

**Expected:** `HTTP/2 200` for all three.

Manual check — open each in a browser and confirm:

| Page | Must show |
|---|---|
| `/` | Landing paragraph, three link buttons (Demo, Source, SDD Index), curated SDD list |
| `/sdds/` | 12 SDDs in grouped reading order with tags |
| `/coding-standards` | Three sections: Service Scaffold, Commit Conventions, Dispatch Protocol |

**If any page 404s:** check the `growdirectprez/canary-site` repo for the file (`index.html`, `sdds/index.html`, `coding-standards.html`) and confirm Pages rebuilt after the last commit.

---

## §4 — MCP autodiscovery and tool surface

### 4a — Discovery document

```bash
curl -s https://demo.growdirect.io/.well-known/mcp.json | jq .
```

**Expected output (key fields):**

```json
{
  "mcp_version": "2025-03-26",
  "name": "Canary Retail Ops",
  "endpoint": "https://demo.growdirect.io/mcp",
  "transport": "http-post",
  "auth": {
    "type": "api_key",
    "header": "X-API-Key"
  },
  "tools_count": 28,
  "modules": ["alert","analytics","asset","customer","employee","returns","report"]
}
```

**If the endpoint field shows `http://` instead of `https://`:** the `PUBLIC_URL` env var is not set in Cloud Run. Update the staging service:

```bash
gcloud run services update canary-gateway-staging \
  --update-env-vars PUBLIC_URL=https://demo.growdirect.io \
  --region us-central1 \
  --project canary-rapidpos
```

### 4b — Provision demo API key (if not already present)

Check whether a demo key exists:

```bash
# Via Cloud SQL proxy (run in a separate terminal first):
# cloud-sql-proxy canary-rapidpos:us-central1:canary-pg --port=5433

psql "host=127.0.0.1 port=5433 dbname=canary_gcp user=canary_app" \
  -c "SELECT id, agent_name, status, created_at FROM app.api_keys WHERE agent_name = 'demo-dry-run' LIMIT 1;"
```

If no row exists, provision one using the Go identity package from the CanaryGo shell:

```bash
cd CanaryGo
# Compile a one-shot key generator
cat > /tmp/provision_key.go << 'EOF'
//go:build ignore
package main

import (
    "context"
    "fmt"
    "os"

    "github.com/jackc/pgx/v5/pgxpool"
    "github.com/growdirect-llc/rapidpos/internal/identity"
)

func main() {
    pool, err := pgxpool.New(context.Background(), os.Getenv("DATABASE_URL"))
    if err != nil { panic(err) }
    defer pool.Close()
    plaintext, id, err := identity.CreateAPIKeyRow(context.Background(), pool, nil, "demo-dry-run", []string{"read", "mcp"}, 600, nil)
    if err != nil { panic(err) }
    fmt.Printf("key_id:    %s\nplaintext: %s\n", id, plaintext)
    fmt.Println("SAVE THE PLAINTEXT — it will not be shown again.")
}
EOF
DATABASE_URL="$(gcloud secrets versions access latest \
  --secret=canary-gateway-database-url --project=canary-rapidpos)" \
  go run /tmp/provision_key.go
```

Save the plaintext token as `DEMO_API_KEY` for the next step.

### 4c — Tools list

```bash
DEMO_API_KEY=<plaintext from 4b>

curl -s https://demo.growdirect.io/mcp \
  -H "X-API-Key: $DEMO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
  | jq '.result.tools | length'
```

**Expected:** `28`

```bash
# Spot-check a specific tool
curl -s https://demo.growdirect.io/mcp \
  -H "X-API-Key: $DEMO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' \
  | jq '[.result.tools[].name] | sort'
```

**Expected:** 28 tool names across alert, analytics, asset, customer, employee, returns, report domains.

### 4d — Claude Code MCP wiring (optional but recommended for the demo)

Add to `.mcp.json` in any project:

```json
{
  "mcpServers": {
    "canary": {
      "type": "http",
      "url": "https://demo.growdirect.io/mcp",
      "headers": {
        "X-API-Key": "<DEMO_API_KEY>"
      }
    }
  }
}
```

Start a Claude Code session in that project. Run `/mcp` to confirm the server connects and tools are listed.

---

## §5 — Public mirror

```bash
# README exists and has correct content
curl -s https://raw.githubusercontent.com/growdirect-llc/canary-go/main/README.md | head -5

# OpenAPI spec is reachable (14,908 lines)
curl -sI https://raw.githubusercontent.com/growdirect-llc/canary-go/main/services/canary-protocol/openapi/openapi.yaml \
  | grep content-length
```

**Expected:** README starts with `# Canary Go`. Content-length should be ~600KB for the OpenAPI spec.

---

## §6 — Contingency table

| Symptom | Most likely cause | Action |
|---|---|---|
| `demo.growdirect.io` 502/503 | Cloud Run instance not running | Redeploy via `gcloud builds submit` |
| `demo.growdirect.io` 404 on `/auth/square` | Square env vars not set | Add SQUARE_APPLICATION_ID, SQUARE_APPLICATION_SECRET, SQUARE_REDIRECT_URI to Secret Manager and redeploy |
| OAuth redirects to error page | SQUARE_REDIRECT_URI mismatch | Verify URI in Square Developer Dashboard matches `https://demo.growdirect.io/auth/square/callback` |
| Dashboard shows no merchant name | Token not stored — check `app.pos_tenant_credentials` | `SELECT * FROM app.pos_tenant_credentials WHERE source_code = 'square';` via Cloud SQL proxy |
| `/.well-known/mcp.json` endpoint field is `http://` | PUBLIC_URL not set | `gcloud run services update` with `--update-env-vars PUBLIC_URL=https://demo.growdirect.io` |
| `POST /mcp` returns 401 | API key not provisioned or wrong key | Re-run §4b; confirm key status is `active` in `app.api_keys` |
| `tools/list` returns fewer than 28 | MCP registry partial | Check `cmd/gateway/main.go` — all 7 `Register*Tools` calls must be present |
| `canary.growdirect.io` pages 404 | GitHub Pages hasn't rebuilt | Check Actions tab on `growdirectprez/canary-site`; push an empty commit to trigger rebuild |
| OpenAPI raw URL 404 | Mirror not pushed | Run `bash CanaryGo/scripts/mirror-public.sh` |

---

## §7 — Post dry-run checklist

After all sections pass:

- [ ] Note any non-critical issues as follow-up dispatches (do not fix mid dry-run unless blocking)
- [ ] Confirm `demo.growdirect.io` Square flow works on mobile viewport (founder's phone)
- [ ] Confirm Claude Code MCP connection from §4d shows all 28 tools in a real session
- [ ] File the senior dev engagement dispatch in Linear (Target/laptop, Backlog, trigger condition: 2026-05-13)
- [ ] Comment on GRO-802 in Linear: dry run complete, artifacts verified, demo ready

---

*Runbook authored 2026-05-06 · GRO-802 Day 7 · executable by a fresh session with no assumed chat state*
