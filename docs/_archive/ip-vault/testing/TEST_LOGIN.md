---
type: spec
domain: canary
status: active
created: 2026-03-14
updated: 2026-03-19
---
# Login Test Checklist — Canary LP

> Run this checklist after any auth-related deploy or when login is broken.

## Prerequisites

- Stack is healthy: `curl -s http://localhost:5001/health` → 200
- `.env` has `CANARY_ADMIN_MERCHANTS=MLE55GCYANCYT`
- Containers rebuilt: `docker compose -f devops/docker-compose.localhost.yml up -d --build flask`

---

## Desktop — Safari

1. Safari → Settings → Privacy → Manage Website Data → remove `localhost` and `local.growdirect.app`
2. Navigate to `http://localhost:5001/auth/join`
3. **Expected:** "Join the Flock" page with Square OAuth button
4. Click "Connect Your Square Account"
5. **Expected:** Square OAuth consent screen (sandbox)
6. Authorize → redirect back to Canary
7. **Expected:** `/m/welcome` page. Check session: admin nav should be visible (your merchant ID is in the admin list)
8. Navigate to `http://localhost:5001/auth/clear-session`
9. **Expected:** Redirected to `/auth/join` — session nuked, clean slate
10. Repeat steps 4-7 — should work first try

## Desktop — Chrome

1. Chrome → Settings → Privacy and Security → Clear browsing data → Cookies → select `localhost`
2. Same flow as Safari steps 2-10
3. Alternative: Chrome DevTools → Application → Storage → Clear site data

## Mobile — Safari (iOS)

1. Settings → Safari → Clear History and Website Data
2. Navigate to dev tunnel URL (e.g. `https://dev.growdirect.app/auth/join`)
3. Same flow as Desktop steps 3-10
4. Note: Square OAuth consent screen may look different on mobile

## Nuclear Reset (When Everything is Broken)

1. Clear browser cookies (all of them for localhost)
2. `docker exec canary_localhost_valkey valkey-cli FLUSHDB`
3. `cd ~/GrowDirect/Canary && docker compose -f devops/docker-compose.localhost.yml restart flask`
4. Wait 10 seconds
5. `curl -s http://localhost:5001/health` → must return 200
6. Navigate to `http://localhost:5001/auth/join` → start OAuth flow

## Smoke Test (Post-Deploy)

```bash
# 1. Health check
curl -s http://localhost:5001/health

# 2. Sandbox OAuth (creates merchant + settings rows)
curl -s http://localhost:5001/oauth/sandbox -L -c /tmp/canary_cookies.txt

# 3. Check session has admin role
curl -s http://localhost:5001/auth/userinfo -b /tmp/canary_cookies.txt

# 4. Clear session works
curl -s http://localhost:5001/auth/clear-session -L -b /tmp/canary_cookies.txt -c /tmp/canary_cookies.txt
```
