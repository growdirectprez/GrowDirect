---
type: runbook
status: active
runbook-id: canary-go-auth
issue-shape: Dev gateway can't get a session — /login shows "Square OAuth not configured" or the demo button is missing
service: canary-go-gateway
engines: [identity]
modules: []
owner: ALX
last-verified: 2026-05-08
last-compiled: 2026-05-08
needs-review: 2026-08-08
tags: [runbook, devops, auth, square, oauth, login, dev]
---

# CanaryGo gateway auth — Demo Login + Square sandbox wiring

The CanaryGo gateway has two paths for getting a session in development: a **Demo Login** bypass (signs a session cookie for the seeded Acme Main Street merchant — no external dependencies) and **Square OAuth** (real Square sandbox round-trip — needs developer-account credentials). This runbook covers both.

## When to use this

- New dev environment, can't log in
- `/login` shows "Square OAuth not configured" notice and you want to fix it
- "Demo Login (dev only)" button is missing from `/login` and you need it back
- Square OAuth callback returns an error — credentials may be stale or wrong
- `/auth/square` returns HTTP 503

If `/auth/connect` 404s or unauthenticated users see `/connect` directly, that's a different issue — those paths were patched in `cf4f090` + `bf101e7` (May 2026). Pull `main` and rebuild the gateway image.

## Prerequisites

- Docker running
- `growdirect_postgres` + `growdirect_valkey` containers up: `cd ~/GrowDirect/devops && docker compose up -d`
- `make db-seed` has been run at least once (creates Acme Main Street merchant `33333333-0000-0000-0000-000000000001`)
- For Square OAuth path only: a Square Developer account + sandbox application

## Path A — Demo Login (no external dependencies)

Default in dev compose. If it works, you're done.

### Verify it's enabled

```bash
docker compose -f CanaryGo/deploy/docker-compose.yml exec canarygo-gateway env | grep DEV_DEMO_LOGIN
```

Expected: `DEV_DEMO_LOGIN=1`

If unset, edit `CanaryGo/deploy/docker-compose.yml` under `canarygo-gateway.environment` and add:

```yaml
DEV_DEMO_LOGIN: "1"
```

Then restart:

```bash
cd CanaryGo/deploy
docker compose up -d canarygo-gateway
```

### Use the Demo Login

1. Open http://localhost:9080/login
2. Click **Demo Login (dev only)**
3. Browser lands on `/dashboard` as Acme Main Street

Expected: Sidebar shows Alerts, Chirps, etc. `demo_merchant` cookie is signed and valid for 7 days.

### Verify the round-trip via curl

```bash
COOKIE=$(curl -s -i http://localhost:9080/auth/demo | grep -i "set-cookie:" | sed 's/[Ss]et-[Cc]ookie: //' | cut -d';' -f1)
curl -s -o /dev/null -b "$COOKIE" -w "%{http_code}\n" http://localhost:9080/dashboard
# → 200
```

### Production safety

- `DEV_DEMO_LOGIN` is **not set** in any production compose file
- The `/auth/demo` route is mounted unconditionally but `handleDevDemoLogin` returns 404 when the env flag is unset — never reveals the route exists
- Demo cookie still signed via `SESSION_SECRET`, so a leaked dev cookie won't validate against a different `SESSION_SECRET`

## Path B — Real Square sandbox OAuth

Use when you want to test the actual OAuth flow, webhook delivery, or real Square API calls. Demo Login alone won't exercise these.

### Step 1 — Get sandbox credentials

1. Sign in at <https://developer.squareup.com/apps>
2. Open the Canary application (or create one named `canary-dev` under your developer account)
3. Switch the environment toggle to **Sandbox** (top-right)
4. Copy the three values from the **OAuth** tab:
   - **Application ID** (looks like `sandbox-sq0idb-...`)
   - **Application Secret** (under the "Production / Sandbox" subtabs — sandbox tab; click "Show")
   - **Redirect URL** — set this to `http://localhost:9080/auth/square/callback` and save

> Note: the project's `Square sandbox is shared` constraint applies here — multiple apps share one sandbox account, existing data can't be deleted.

### Step 2 — Wire credentials into the gateway

Edit `CanaryGo/deploy/docker-compose.yml` under `canarygo-gateway.environment`:

```yaml
SQUARE_APPLICATION_ID: "sandbox-sq0idb-XXXXXXXXXXXXXXXXXX"
SQUARE_APPLICATION_SECRET: "sandbox-sq0csb-XXXXXXXXXXXXXXXXXXXXXXXXXX"
SQUARE_REDIRECT_URI: "http://localhost:9080/auth/square/callback"
```

For per-developer secrets, the cleaner alternative is a `.env.local` file (gitignored) that the compose file reads:

```yaml
environment:
  SQUARE_APPLICATION_ID: ${SQUARE_APPLICATION_ID}
  SQUARE_APPLICATION_SECRET: ${SQUARE_APPLICATION_SECRET}
  SQUARE_REDIRECT_URI: ${SQUARE_REDIRECT_URI:-http://localhost:9080/auth/square/callback}
```

```bash
# .env at repo root (gitignored)
SQUARE_APPLICATION_ID=sandbox-sq0idb-XXXXXXXXXXXXXXXXXX
SQUARE_APPLICATION_SECRET=sandbox-sq0csb-XXXXXXXXXXXXXXXXXXXXXXXXXX
```

### Step 3 — Restart the gateway

```bash
cd CanaryGo/deploy
docker compose up -d canarygo-gateway
sleep 3
docker logs canarygo-canarygo-gateway-1 --tail 20 | grep -i square
```

Expected: no `SQUARE_APPLICATION_ID not set` warnings. The startup log should show `tokens stored plaintext (sandbox only)` (acceptable in dev) but no errors about missing OAuth config.

### Step 4 — Verify the OAuth flow

Open http://localhost:9080/login. The **"Square OAuth not configured"** notice should be gone, replaced by the working **Connect Your Square** button.

Click it. Expected sequence:

1. Browser navigates to `https://connect.squareupsandbox.com/oauth2/authorize?...`
2. Sign in with a sandbox merchant account
3. Approve the requested scopes
4. Square redirects to `http://localhost:9080/auth/square/callback?code=...&state=...`
5. Gateway exchanges the code, stores the token, sets `demo_merchant` cookie, redirects to `/dashboard`

Curl-equivalent for the unauthorized check:

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:9080/auth/square
# → 302 (was 503 before this step)
```

### Production posture

- Production sets `SQUARE_APPLICATION_ID` etc via the secrets backend (`SECRET_BACKEND=pgx` or whichever is configured), **not** plain compose env vars
- `CANARY_ENCRYPTION_KEY` should be set in production so OAuth tokens are encrypted at rest (dev compose runs without it; the gateway logs `tokens stored plaintext (sandbox only)`)
- `SESSION_SECRET` rotates per environment — leaking the dev key doesn't unlock production sessions
- `DEV_DEMO_LOGIN` is **never** set in production

## If it doesn't work

| Symptom | Likely cause | Fix |
|---|---|---|
| `/login` still shows "not configured" notice | env vars set in compose but container not restarted | `docker compose up -d canarygo-gateway` after editing compose |
| OAuth redirect comes back with `error=invalid_request` | `SQUARE_REDIRECT_URI` doesn't match what Square has on file | update the redirect URL in the Square dashboard to match exactly (scheme, host, port, path) |
| OAuth callback returns 400 "state mismatch (CSRF)" | browser ate the `square_oauth_state` cookie (incognito? cross-site?) | retry from `/login` in a normal window; cookie is `SameSite=Lax` |
| `/auth/square/callback` returns 502 "code exchange failed" | wrong client secret, or sandbox/production mismatch | re-copy the **Sandbox** application secret (not Production) |
| `demo_merchant` cookie set but `/dashboard` still redirects to `/login` | `make db-seed` not run, demo merchant UUID not in DB | `cd CanaryGo && make db-seed` then retry |
| Demo Login button missing on `/login` | `DEV_DEMO_LOGIN` not propagating into the container | `docker compose exec canarygo-gateway env | grep DEV_DEMO_LOGIN` to confirm; rebuild image if cached |
| `/auth/demo` returns 404 with the env set | container running an older image without the route | `docker compose build canarygo-gateway && docker compose up -d canarygo-gateway` |
| `/connect` or `/welcome` returns 200 without a session | gateway image predates `cf4f090` (May 2026 auth-gate fix) | pull `main` and rebuild the gateway image |

## Why this works

- `squareauth.handleAuthorize` (line 71 of `internal/squareauth/handler.go`) gates on all three Square env vars being non-empty; missing any of them returns 503
- `squareauth.handleCallback` exchanges the OAuth code, stores the access token, and **signs a `demo_merchant` cookie via HMAC-SHA256 using `SESSION_SECRET`** before redirecting
- The signed cookie is the input to `MerchantResolver: squareSvc.MerchantFromRequest` (wired in `cmd/gateway/main.go` line 318) — every protected request resolves the merchant from this cookie
- `web.requireTenantMiddleware` redirects to `/login` when no merchant resolves; with a valid cookie it forwards to the handler
- `squareauth.handleDevDemoLogin` is a shortcut that signs the same cookie shape pointing at the seeded Acme merchant — bypasses the OAuth round-trip entirely. Gated on `DEV_DEMO_LOGIN=1`; production never enables it.

## References

- Spec: [[docs/superpowers/specs/2026-05-07-sysadmin-module-design]] — sysadmin module + auth posture
- Code: `CanaryGo/internal/squareauth/handler.go` — OAuth handlers, demo login, cookie signing
- Code: `CanaryGo/internal/web/handler.go` (loginPage, squareConfigured, demoLoginEnabled)
- Compose: `CanaryGo/deploy/docker-compose.yml` — `canarygo-gateway.environment`
- Seed: `CanaryGo/deploy/schema/99_seed.sql` — Acme Main Street merchant UUID `33333333-0000-0000-0000-000000000001`
- Memory: [[project_square_sandbox_shared]] — single sandbox shared across apps
- Memory: [[feedback_dont_change_redirects]] — OAuth redirects to `/connect` (bird progress ring), not `/welcome`
