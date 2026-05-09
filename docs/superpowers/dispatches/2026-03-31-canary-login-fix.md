# Dispatch: GRO-386 — Canary Login Fix

**Date:** 2026-03-31
**Priority:** Urgent
**App:** Canary
**Branch:** `gro-386-fix-canary-login-broken-wire-flask-session-to-valkey-harden`

---

## Paste this into a Canary Claude Code session

```
You are the Canary builder. Read ~/GrowDirect/CLAUDE.md then ~/GrowDirect/Canary/CLAUDE.md.

Your issue is GRO-386: Canary login is broken because Flask is using signed cookie sessions instead of the platform-standard Valkey server-side backend.

Run the full factory pipeline for this issue. Here is your scope:

## What's wrong

Flask has no SESSION_TYPE configured. Sessions are werkzeug signed cookies (client-side). The VALKEY_URL exists in compose and .env but is only used for rate limiting and TSP streams — never for sessions. Behind the nginx TLS proxy with SESSION_COOKIE_SECURE=False, the OAuth callback sets session values in a cookie that gets dropped on redirect.

## What to fix (in order)

1. Add flask-session with Valkey DB 0 backend (check requirements.txt first, install if missing)
   - SESSION_TYPE = "redis"
   - SESSION_REDIS = Redis.from_url(VALKEY_URL) — use DB 0 per platform allocation
   - SESSION_KEY_PREFIX = "canary:session:"
   - Init Session(app) in the app factory

2. Add user existence check in canary/middleware/jwt_auth.py load_session_user()
   - Query DB for user by session["user_id"]
   - If user missing or inactive → session.clear(), redirect to login

3. Fix SESSION_COOKIE_SECURE — must be True when behind nginx TLS proxy

4. Move OAuth state to Valkey — store square_oauth_state server-side with 5-min TTL

5. Read rate limiter URI from env in extensions.py instead of hardcoding

6. Add session.permanent = True in OAuth callback after login

## Reference implementation

Look at Cove's session setup — same platform, same pattern:
- ~/Cove/cove/extensions.py (Session extension)
- ~/Cove/cove/__init__.py (Session init in factory)
- ~/Cove/cove/config.py (SESSION_TYPE config)

Match Cove's pattern exactly. Same problem, same solution.

## Protected files

wsgi.py, canary/extensions.py, and requirements.txt are guardian-protected. Use the critical-file-guardian skill.

## Tests

- Smoke: GET /auth/join returns 200
- Integration: OAuth mock flow → session persists in Valkey (not cookie)
- Integration: invalidate session server-side → next request redirects to login
- Integration: load_session_user() with nonexistent user_id → session cleared
- Verify: redis-cli -n 0 KEYS "canary:session:*" shows sessions after login
- All existing auth tests still pass

## Acceptance

- Login flow works end-to-end (OAuth → callback → dashboard)
- Sessions stored in Valkey DB 0, not cookies
- User validation on every request via session loader
- No regression in rate limiting or TSP streams

Start with preflight. Go.
```
