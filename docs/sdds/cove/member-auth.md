# Member Auth

> **Type:** App Service (Cove)
> **Status:** Production-grade operational contract
> **Last updated:** 2026-04-13
> **Code location:** `Cove/cove/auth/`, `Cove/cove/member/`, `Cove/cove/models/member.py`
> **Wiki:** [[Brain/wiki/cove-governance|Cove Governance]]

---

## Purpose

Member Auth is the authentication, session management, and privacy consent
layer for Cove. It authenticates HOA members via lot-based email identity using
magic links (primary) or password hash (dev/fallback), stores sessions in
Valkey, enforces privacy consent before access, and controls PII visibility
through directory preference toggles. This is the PII entry point for all of
Cove — every member's personal data flows through this service first.

---

## Dependencies

| Dependency | Type | Required at | Purpose |
|------------|------|-------------|---------|
| PostgreSQL 17 (`growdirect_postgres:5432`, database `cove`) | Datastore | Runtime | Member, Role, MemberRole, DirectoryPreference tables |
| Valkey 8 (`growdirect_valkey:6379/1`) | Session store | Runtime | Server-side session storage, rate limiter backing store |
| Flask-Login | Library | Runtime | `@login_required`, `login_user()`, `current_user` proxy |
| itsdangerous | Library | Runtime | `URLSafeTimedSerializer` — magic link token signing |
| werkzeug | Library | Runtime | `check_password_hash` / `generate_password_hash` |
| Flask-Mail | Library | Runtime | SMTP delivery of magic link emails |
| Flask-WTF / WTForms | Library | Runtime | Form definitions, CSRF protection |
| Flask-Session | Library | Runtime | Server-side session via Valkey |
| Flask-Limiter | Library | Runtime | Rate limiting (Valkey-backed in dev/prod, memory in tests) |
| Flask-Talisman | Library | Runtime | CSP, HSTS, X-Frame-Options, X-Content-Type-Options |
| MailHog | Service | Dev only | SMTP trap (web `:8026`, SMTP `:1026`) |
| Cloudflare Email Routing | Service | Prod only | Lot email forwarding to personal inbox |

---

## Data Flow & PII Map

### What enters

| Source | Data | How |
|--------|------|-----|
| Login form (`POST /auth/login`) | Email address or short lot ID, optional password | Form POST (CSRF-protected) |
| Onboarding form (`POST /member/onboarding`) | Display name, personal email, phone, directory prefs | Form POST |
| Profile form (`POST /member/profile`) | Name, bio, personal email, phone, avatar file, share toggles | Form POST + file upload |
| Privacy consent form (`POST /member/accept-privacy`) | Boolean acceptance | Form POST |
| Magic link callback (`GET /auth/verify/<token>`) | Signed token in URL path | GET request |

### What's stored

| Table | Field | PII Classification | Encryption | Notes |
|-------|-------|--------------------|------------|-------|
| `members` | `lot_email` | **internal** | Plaintext | Property-level address, always visible. Not personal data under HOA norms. |
| `members` | `personal_email` | **sensitive** | **Plaintext** | Forwarding target. Hidden by default. PII. |
| `members` | `phone` | **sensitive** | **Plaintext** | Opt-in for directory. PII. |
| `members` | `name` | **internal** | Plaintext | Display name. Visible to all authenticated members. |
| `members` | `password_hash` | **sensitive** | Hashed (werkzeug/pbkdf2) | Dev/fallback only. One-way hash, not reversible. |
| `members` | `magic_link_nonce` | **internal** | Plaintext | UUID. Rotated on each login. NULL after use. Short-lived. |
| `members` | `privacy_consent_at` | **internal** | Plaintext | Timestamp of policy acceptance. |
| `members` | `last_login_at` | **internal** | Plaintext | Audit field. |
| `members` | `membership_status` | **internal** | Plaintext | active/suspended/inactive. |
| `members` | `assessment_status` | **internal** | Plaintext | current/delinquent. Financial status. |
| `directory_preferences` | `show_email`, `show_phone` | **internal** | Plaintext | Controls PII visibility in directory. |
| Valkey DB 1 | Session data | **sensitive** | **Plaintext** | Contains session ID referencing member identity. |

### What exits

| Destination | Data | How |
|-------------|------|-----|
| Member's personal email inbox | Magic link URL containing signed token | SMTP via Flask-Mail |
| Browser cookie | Session ID (opaque key, no PII) | `Set-Cookie` with Secure/HttpOnly/SameSite flags (prod) |
| Directory views | Name, lot email, address (always); personal email, phone (opt-in or board view) | HTML response |
| Downstream services (Governance, Vault, etc.) | `current_user` proxy (Member object in request context) | In-process; no network boundary |

---

## API Contract

### Auth Blueprint (`/auth`)

| Method | Path | Auth | Rate Limit | Description |
|--------|------|------|------------|-------------|
| GET | `/auth/login` | None | 10/min per IP (shared) | Render login form |
| POST | `/auth/login` | None | 5/min POST per IP + 3/15min per email | Magic link dispatch or password auth |
| GET | `/auth/verify/<token>` | None | 10/min per IP (shared) | Consume magic link token, start session |
| POST | `/auth/logout` | `@login_required` | 10/min per IP (shared) | Destroy session, redirect to landing |

**POST /auth/login — magic link path**

Request body (form-encoded, CSRF token required):
```
email=<lot_email or personal_email or short_lot_id>
```
Response: 302 redirect to `GET /auth/login` with flash message. Response is
identical whether the email exists or not (no user enumeration).

**POST /auth/login — password fallback path**

Request body:
```
email=<email>
password=<password>
```
Response: 302 to `/member/dashboard` or `/member/onboarding` on success.
Flash error on failure. Timing-equalized via dummy hash comparison.

**GET /auth/verify/`<token>`**

URL-safe signed token (itsdangerous). On success: session created, 302 to
onboarding or dashboard. On failure: renders `auth/verify.html` with
`success=False` and flash error.

### Member Blueprint (`/member`) — auth-adjacent routes

All routes require `@login_required`.

| Method | Path | Description |
|--------|------|-------------|
| GET/POST | `/member/onboarding` | First-login setup (name, personal email, phone, prefs) |
| GET/POST | `/member/accept-privacy` | Privacy policy acceptance gate |
| GET/POST | `/member/profile` | Edit profile, contact info, directory preferences |
| GET | `/member/directory` | Directory listing; `?q=` for search |
| GET | `/member/directory/<apn>` | APN-centric profile page |

### Decorators (`cove/auth/decorators.py`)

| Decorator | Checks | Used by |
|-----------|--------|---------|
| `@board_required` | `current_user.is_board` | Board admin routes |
| `@board_or_admin_required` | `is_board or is_admin` | Board management |
| `@admin_required` | `current_user.is_admin` | Admin-only operations |
| `@arc_required` | `current_user.is_arc` | Research Workbench (map, archive, parcels) |
| `@inspector_required` | `current_user.is_inspector` | Ballot envelope access (Davis-Stirling) |

All decorators must be placed AFTER `@login_required` so `current_user` is available.

---

## Operations

### Magic Link Flow (step by step)

```
1. Member submits email/lot ID to POST /auth/login
2. Route normalizes input: bare "25seacove" → "25seacovedr@abalonecove.org"
3. SELECT from members WHERE lot_email = ? OR personal_email = ?
4. If not found → flash generic message, redirect (no user enumeration)
5. Generate UUID nonce → store in member.magic_link_nonce → commit
6. generate_magic_link_token(member.id, nonce)
   → URLSafeTimedSerializer.dumps({member_id, nonce}, salt="magic-link", key=SECRET_KEY)
7. send_magic_link_email(member, token)
   → Flask-Mail Message to member.personal_email (raises ValueError if NULL)
8. Flash "Check your email..." → redirect to GET /auth/login

--- User clicks link in email ---

9. GET /auth/verify/<token>
10. verify_magic_link_token(token)
    → URLSafeTimedSerializer.loads(token, salt="magic-link", max_age=900)
    → Returns {member_id, nonce} or None on SignatureExpired/BadSignature
11. Lookup member by member_id
12. Compare member.magic_link_nonce == payload["nonce"]
    → NULL (already used) or mismatched nonce → reject
13. Rotate: member.magic_link_nonce = None, member.last_login_at = now() → commit
14. login_user(member, remember=True)
15. Redirect: /member/onboarding if not onboarded, else /member/dashboard
```

### Timing Oracle Protections

- **Password path:** When member is not found or has no `password_hash`, the
  route calls `check_password_hash(DUMMY_HASH, password)` so response time
  is constant whether the member exists or not. `DUMMY_HASH` is computed once
  at module load via `generate_password_hash("dummy-timing-equalization")`.
- **Magic link path:** The flash message is identical for found and not-found
  members. No timing-significant code path difference — both branches redirect
  immediately.

### Session Backend (Valkey)

- **Backend:** Flask-Session with `SESSION_TYPE="redis"` pointing to Valkey 8 on DB 1.
- **Cookie contents:** Opaque session ID only. No PII in the cookie.
- **Session duration:** `REMEMBER_COOKIE_DURATION` defaults to Flask-Login's 365 days
  unless overridden. `SESSION_DURATION_DAYS` config (default 7) exists but is
  **not wired** to `REMEMBER_COOKIE_DURATION` or `PERMANENT_SESSION_LIFETIME`
  in current code — see Finding CR-AUTH-05.
- **Cookie flags (prod):** `Secure=True`, `HttpOnly=True`, `SameSite=Lax`.
  Remember-cookie mirrors these flags. `SESSION_COOKIE_SECURE=False` in DevConfig.
- **Initialization:** `create_app()` creates a `redis.from_url(VALKEY_URL)` client.
  If the `redis` package is not installed, falls back to cookie sessions with a
  warning log.

### What Happens When Valkey is Down

| Scenario | Behavior |
|----------|----------|
| Valkey unreachable at startup | `redis.from_url()` succeeds (lazy connect). First request that touches session will fail with `ConnectionError`. |
| Valkey goes down mid-operation | Flask-Session raises `ConnectionError` on session read/write. Unhandled — results in 500 error. |
| Rate limiter with Valkey down | Flask-Limiter falls back to allowing all requests (no rate limiting) unless `RATELIMIT_STORAGE_URI` is explicitly set to `memory://`. |
| Recovery | Valkey restart restores service. Existing sessions are lost (members must re-authenticate). |

**Failure mode:** Valkey down = authentication broken. No graceful degradation.
The `/health` endpoint does not check Valkey connectivity — it always returns
`{"status": "ok"}`.

### Nonce Rotation Logic

- On magic link generation: `member.magic_link_nonce = str(uuid.uuid4())` → committed.
- On magic link use: `member.magic_link_nonce = None` → committed.
- Effect: Only one magic link is valid at a time. Generating a new link invalidates
  all previous links. Using a link invalidates itself. Replay is impossible.

### Privacy Consent Gate

`_check_privacy_consent()` runs as a `before_request` hook on every request:
1. Skip if unauthenticated.
2. Skip if endpoint starts with: `auth.`, `public.`, `static`, `agent.`,
   `angel_web.`, `angel_chat.`.
3. Skip if endpoint is `member.accept_privacy`.
4. If `current_user.privacy_consent_at is None` AND `current_user.onboarded` →
   redirect to `/member/accept-privacy`.

This is a blocking gate — no platform functionality until the member accepts.

### HTTP Security Headers (Flask-Talisman)

| Header | Value | Notes |
|--------|-------|-------|
| Content-Security-Policy | `default-src 'self'; script-src 'self'` (with nonce); `style-src 'self' 'unsafe-inline' fonts.googleapis.com`; `img-src 'self' data: *.tile.openstreetmap.org server.arcgisonline.com`; `font-src 'self' fonts.gstatic.com`; `connect-src 'self'` | Nonce injection for script-src |
| X-Frame-Options | `DENY` | Clickjacking prevention |
| X-Content-Type-Options | `nosniff` | MIME sniffing prevention |
| Strict-Transport-Security | Enabled when `SESSION_COOKIE_SECURE=True` | Prod/staging only |

### Startup Sequence

1. `create_app(config_name)` reads config.
2. Initialize extensions: `db`, `login_manager`, `mail`, `csrf`, `sess` (if not null), `talisman`, `limiter`.
3. Register 17 blueprints.
4. Register `user_loader` callback.
5. Register `_check_privacy_consent` before_request hook.
6. Register error handlers (429, standard errors).
7. `/health` endpoint registered (returns `{"status": "ok"}`).

### Health Check

```
GET /health → {"status": "ok"}, 200
```
**Limitation:** Does not verify PostgreSQL or Valkey connectivity. Always returns
200. Not suitable for production load balancer health checks — see Finding CR-AUTH-08.

---

## Deployment

### Docker Service

Auth runs inside the `cove_flask` container — no separate deployment unit.

```yaml
# Cove/devops/docker-compose.yml
cove_flask:
  image: cove-flask
  build: ..
  ports: ["5002:5000"]
  networks: [growdirect]
  environment:
    - DATABASE_URL=postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/cove
    - VALKEY_URL=redis://growdirect_valkey:6379/1
    - SECRET_KEY=${SECRET_KEY}
    - FLASK_ENV=dev
```

### AWS Target

| Component | AWS Service | Notes |
|-----------|------------|-------|
| Flask app | ECS Fargate | Part of Cove task definition |
| PostgreSQL | RDS PostgreSQL 17 | `cove` database |
| Valkey | ElastiCache (Redis-compatible) | DB 1, single node or cluster |
| Secrets | AWS Secrets Manager | `SECRET_KEY`, database credentials, mail credentials |
| Email (prod) | Cloudflare Email Routing | Lot email → personal email forwarding |
| Email (transactional) | SES or Cloudflare Workers | Magic link delivery |

### CI/CD Requirements

- Run `pytest Cove/tests/` — auth tests must pass.
- Verify rate limiter storage URI points to ElastiCache, not localhost.
- Verify `SESSION_COOKIE_SECURE=True` in prod config.
- Verify `SECRET_KEY` is sourced from Secrets Manager, not `.env`.

---

## Configuration

| Key | Default | Env-specific | Description |
|-----|---------|-------------|-------------|
| `SECRET_KEY` | **required** | All | Signs magic link tokens, CSRF tokens, session cookies |
| `MAGIC_LINK_EXPIRY` | `900` | All | Token max age in seconds (15 minutes) |
| `SESSION_DURATION_DAYS` | `7` | All | **Not wired** — config exists but is not consumed (see CR-AUTH-05) |
| `SESSION_TYPE` | `"redis"` | `"null"` in TestConfig | Flask-Session backend |
| `VALKEY_URL` | `redis://localhost:6379/1` | All | Valkey connection string |
| `SESSION_COOKIE_SECURE` | `False` (dev), `True` (prod) | Per-env | HTTPS-only cookies |
| `SESSION_COOKIE_HTTPONLY` | `True` | All | Prevent JS access to session cookie |
| `SESSION_COOKIE_SAMESITE` | `"Lax"` | All | CSRF protection via SameSite |
| `REMEMBER_COOKIE_HTTPONLY` | `True` | All | Prevent JS access to remember cookie |
| `REMEMBER_COOKIE_SECURE` | `True` (prod only) | ProdConfig | HTTPS-only remember cookie |
| `MAIL_SERVER` | `"localhost"` | All | SMTP host |
| `MAIL_PORT` | `1025` | All | SMTP port (MailHog dev / Cloudflare prod) |
| `MAIL_USE_TLS` | `false` | All | TLS for SMTP |
| `MAIL_DEFAULT_SENDER` | `"cove@abalonecove.org"` | All | From address on magic link emails |
| `DOMAIN` | `"abalonecove.org"` | All | Lot email domain |
| `RATELIMIT_STORAGE_URI` | From `VALKEY_URL` | `"memory://"` in TestConfig | Rate limiter backing store |

---

## Data Model

All models in `Cove/cove/models/member.py`. Primary keys use `String(36)` (UUID
stored as string) — historical holdover. Do not propagate to new tables.

### Member (`members`)

```
id                  String(36)  PK, uuid4
organization_id     String(36)  FK → organizations.id
apn                 String(20)  FK → parcels.apn, nullable
name                String(255) Display name
lot_email           String(255) Unique. "25SeaCove@abalonecove.org"
personal_email      String(255) Nullable. PII. Forwarding target.
phone               String(20)  Nullable. PII.
unit_identifier     String(100) "25 Sea Cove Dr"
voting_weight       Integer     Default 1
delivery_preference String(20)  "electronic" | "paper" | "both"
membership_status   String(20)  "active" | "suspended" | "inactive"
assessment_status   String(20)  "current" | "delinquent"
password_hash       String(255) Nullable. werkzeug hash. Dev/fallback only.
magic_link_nonce    String(36)  Nullable. UUID. Rotated on each login.
is_active           Boolean     Default True. Flask-Login gate.
onboarded           Boolean     Default False. First-login flow gate.
privacy_consent_at  DateTime    Nullable. NULL until policy accepted.
created_at          DateTime
updated_at          DateTime
last_login_at       DateTime    Nullable.
```

Flask-Login integration: `get_id()` returns `self.id`. `UserMixin` provides
`is_authenticated`, `is_active`.

Computed properties (not columns): `is_admin`, `is_board`, `is_inspector`,
`is_arc` — all check `MemberRole.is_current` against `Role.name`/permissions.

### Role (`roles`)

```
id                   String(36)  PK
organization_id      String(36)  FK → organizations.id
name                 String(50)  "admin" | "board" | "member" | "inspector" | "arc_committee"
can_vote             Boolean     Default True
can_create_proposals Boolean     Default False
can_manage_members   Boolean     Default False
can_manage_treasury  Boolean     Default False
can_access_envelopes Boolean     Default False (inspector only)
can_access_arc       Boolean     Default False
```

### MemberRole (`member_roles`)

Temporal join. `term_start` and `term_end` (nullable = indefinite) determine
`is_current` at evaluation time (Python, not DB flag).

### DirectoryPreference (`directory_preferences`)

One row per member. `show_name`, `show_address`, `show_email`, `show_phone` —
all default `False` in schema, but service layer writes `show_name=True`,
`show_address=True` at onboarding.

---

## Code Review Findings

### CR-AUTH-01: Personal email and phone stored plaintext

**Severity:** P0 — blocks production

`members.personal_email` and `members.phone` are stored as plaintext
`String(255)` / `String(20)`. These are PII fields. A database breach exposes
every member's personal contact information. Canary's `crypto.py` demonstrates
AES-256-GCM field-level encryption — the same pattern should be applied here.

**Affected code:** `Cove/cove/models/member.py` lines 33-34.

**Recommended fix:** Implement field-level AES-256-GCM encryption for
`personal_email` and `phone` using the Canary `crypto.py` pattern. Key stored
in AWS Secrets Manager. Encrypt on write, decrypt on read. Index on ciphertext
not possible — lookup by personal_email requires an exact-match encrypted index
or application-level scanning.

**Linear issue:** TBD (GRO-xxx)

---

### CR-AUTH-02: No session regeneration after login (session fixation)

**Severity:** P0 — blocks production

Neither the magic link path nor the password path regenerates the session ID
after successful authentication. `login_user(member, remember=True)` is called
but the Flask session ID remains the same as the pre-authentication session.
An attacker who obtains a pre-auth session ID (via network sniffing in dev, XSS,
or session prediction) can hijack the authenticated session.

**Affected code:** `Cove/cove/auth/routes.py` lines 61-69 (password path),
lines 119-127 (magic link path).

**Recommended fix:** Call `session.clear()` followed by
`session.regenerate()` (or equivalent Flask-Session API) immediately before
`login_user()`. If Flask-Session does not expose `regenerate()`, manually clear
the session and set a new session ID.

**Linear issue:** TBD (GRO-xxx)

---

### CR-AUTH-03: SECRET_KEY in .env file

**Severity:** P0 — blocks production

`SECRET_KEY` is read from `os.environ["SECRET_KEY"]` which is populated from
`.env` in development. The `.env` file is not in `.gitignore` (or may be).
`SECRET_KEY` signs magic link tokens, CSRF tokens, and session cookies. If
compromised, an attacker can forge magic link tokens for any member, bypass
CSRF protection, and hijack any session.

**Affected code:** `Cove/cove/config.py` line 10.

**Recommended fix:** In production, source `SECRET_KEY` from AWS Secrets Manager
via `boto3` at startup. Remove from `.env` in prod environments. Ensure `.env`
is in `.gitignore`.

**Linear issue:** TBD (GRO-xxx)

---

### CR-AUTH-04: No audit logging for authentication events

**Severity:** P1 — before GA

Successful logins, failed logins, magic link generation, magic link verification,
logout events, and privacy consent acceptance are not logged to the `audit_log`
table. There is no trail for investigating unauthorized access, brute force
attempts, or account takeover.

**Affected code:** `Cove/cove/auth/routes.py` — all route handlers.

**Recommended fix:** Write audit log entries for: `login_success`,
`login_failure`, `magic_link_sent`, `magic_link_verified`, `magic_link_expired`,
`magic_link_replay`, `logout`, `privacy_consent_accepted`. Include IP address
(hashed — see CR-AUTH-09), user agent, and member_id (if known). Use Cove's
existing `audit_log` table.

**Linear issue:** TBD (GRO-xxx)

---

### CR-AUTH-05: SESSION_DURATION_DAYS config not wired

**Severity:** P1 — before GA

`BaseConfig.SESSION_DURATION_DAYS` (default 7) exists in config but is never
consumed. Neither `REMEMBER_COOKIE_DURATION` nor `PERMANENT_SESSION_LIFETIME`
is set from this value. Flask-Login's default `REMEMBER_COOKIE_DURATION` is
365 days. This means the "remember me" cookie persists for a full year, not 7
days as the config name implies.

**Affected code:** `Cove/cove/config.py` line 30.

**Recommended fix:** In `BaseConfig`, add:
```python
from datetime import timedelta
REMEMBER_COOKIE_DURATION = timedelta(days=SESSION_DURATION_DAYS)
PERMANENT_SESSION_LIFETIME = timedelta(days=SESSION_DURATION_DAYS)
```

**Linear issue:** TBD (GRO-xxx)

---

### CR-AUTH-06: No data retention policy

**Severity:** P1 — before GA

There is no automated purge for: expired sessions in Valkey, old magic link
nonces (though these are NULLed on use), `last_login_at` history, or inactive
member records. Session data accumulates in Valkey indefinitely unless Valkey
eviction policy handles it.

**Affected code:** No code exists — this is a missing feature.

**Recommended fix:** Implement retention: Valkey TTL on session keys (match
`SESSION_DURATION_DAYS`), periodic cleanup of `membership_status="inactive"`
members older than a policy threshold, and document the retention schedule.

**Linear issue:** TBD (GRO-xxx)

---

### CR-AUTH-07: Rate limiter fails open when Valkey is down

**Severity:** P1 — before GA

Flask-Limiter with Valkey storage falls back to allowing all requests if
Valkey is unreachable. This means auth endpoints lose rate limiting during
Valkey outages, enabling brute force attacks on the password path.

**Affected code:** `Cove/cove/__init__.py` lines 57-62 (limiter storage init).

**Recommended fix:** Configure Flask-Limiter with
`RATELIMIT_IN_MEMORY_FALLBACK_ENABLED=True` and
`RATELIMIT_IN_MEMORY_FALLBACK="50/minute"` so rate limiting degrades to
in-memory rather than being disabled entirely.

**Linear issue:** TBD (GRO-xxx)

---

### CR-AUTH-08: Health check does not verify dependencies

**Severity:** P1 — before GA

`GET /health` returns `{"status": "ok"}` unconditionally. It does not check
PostgreSQL connectivity or Valkey availability. A load balancer using this
endpoint will continue routing traffic to a node that cannot authenticate
users or retrieve sessions.

**Affected code:** `Cove/cove/__init__.py` lines 171-173.

**Recommended fix:** Health check should attempt `db.session.execute(text("SELECT 1"))`
and a Valkey `PING`. Return 503 if either fails. Consider a `/health/ready`
(deep check) vs `/health/live` (process alive) split.

**Linear issue:** TBD (GRO-xxx)

---

### CR-AUTH-09: IP addresses not hashed in future audit logging

**Severity:** P1 — before GA

When audit logging is implemented (CR-AUTH-04), IP addresses should be hashed
or masked to avoid storing PII. `Flask-Limiter` uses `get_remote_address` as
the key function, which accesses the raw IP. Rate limiter storage in Valkey
contains plaintext IP addresses as keys.

**Affected code:** `Cove/cove/extensions.py` line 18.

**Recommended fix:** For audit logging, hash IPs with a keyed hash
(HMAC-SHA256 with a daily rotating salt) so the same IP produces the same hash
within a day (for correlation) but cannot be reversed. For rate limiting, the
raw IP in Valkey is acceptable since Valkey is an ephemeral store with TTLs.

**Linear issue:** TBD (GRO-xxx)

---

### CR-AUTH-10: Logout is POST-only but no CSRF validation visible

**Severity:** P2 — post-launch

The logout route (`POST /auth/logout`) correctly requires POST (not GET),
preventing CSRF logout via image tags. CSRF protection is global via
Flask-WTF's `CSRFProtect`. However, the logout form in templates should be
verified to include the CSRF token. If the form uses a bare `<form>` without
`{{ form.hidden_tag() }}` or `{{ csrf_token() }}`, the CSRF check will reject
the request, effectively breaking logout.

**Affected code:** Logout template (verify `templates/` for CSRF token
inclusion).

**Recommended fix:** Verify that the logout form in the navigation template
includes `<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">`.

**Linear issue:** TBD (GRO-xxx)

---

### CR-AUTH-11: Short lot login hardcodes "dr" street suffix

**Severity:** P2 — post-launch

The short lot ID feature appends `dr@abalonecove.org` to bare input. This
only works for Sea Cove Drive members. Members on Packet Rd, Barkentine Ln,
Clipper Ln, or Peppertree Ln must type their full lot email. Not a security
issue but a UX gap that will cause support tickets.

**Affected code:** `Cove/cove/auth/routes.py` line 45.

**Recommended fix:** Either remove the shortcut (require full lot email
always) or implement a lookup table that tries multiple street suffixes. Low
priority — only affects 5-10 of 81 lots.

**Linear issue:** TBD (GRO-xxx)

---

### CR-AUTH-12: Valkey session data unencrypted

**Severity:** P2 — post-launch

Session data in Valkey DB 1 is stored without encryption or AUTH. Anyone with
network access to Valkey can read session contents. In the Docker dev
environment, Valkey is exposed without a password.

**Affected code:** `Cove/cove/config.py` line 16 (VALKEY_URL has no password),
`Cove/cove/__init__.py` line 24 (redis.from_url with no TLS).

**Recommended fix:** In production, enable Valkey AUTH via password in the
connection URL (`redis://:password@host:6379/1`). Enable TLS for Valkey
connections (`rediss://` scheme). Configure `SESSION_KEY_PREFIX` to namespace
Cove sessions.

**Linear issue:** TBD (GRO-xxx)

---

### CR-AUTH-13: String(36) primary keys — UUID migration needed

**Severity:** P2 — post-launch

All four models (`Member`, `Role`, `MemberRole`, `DirectoryPreference`) use
`String(36)` for UUIDs instead of the platform standard `Mapped[uuid.UUID]`
with native PostgreSQL UUID type. This wastes storage, prevents native UUID
indexing, and diverges from platform standards.

**Affected code:** `Cove/cove/models/member.py` — all model classes.

**Recommended fix:** Schema migration to native UUID columns. Requires
coordinated migration across all FK references. Non-blocking but should be
done before the table grows large.

**Linear issue:** TBD (GRO-xxx)

---

## Production Readiness Checklist

- [ ] **PII encrypted at rest** — `personal_email` and `phone` stored plaintext (CR-AUTH-01)
- [ ] **Secrets in AWS Secrets Manager** — `SECRET_KEY` in `.env` (CR-AUTH-03)
- [x] **Health check endpoint responds** — `/health` returns 200 (but does not check deps — CR-AUTH-08)
- [ ] **Audit logging for sensitive operations** — No auth event logging (CR-AUTH-04)
- [ ] **Data retention policy implemented** — No retention policy (CR-AUTH-06)
- [x] **Rate limiting on public endpoints** — `/auth/login` and `/auth/verify` rate-limited (but fails open — CR-AUTH-07)
- [x] **Error responses don't leak internals** — Generic flash messages, no stack traces in prod
- [x] **CSRF protection on all forms** — Global via Flask-WTF CSRFProtect
- [x] **HTTP security headers** — Flask-Talisman configured (CSP, HSTS, X-Frame, X-Content-Type)
- [x] **Open redirect prevention** — `_is_safe_redirect()` rejects absolute URLs
- [x] **No user enumeration** — Identical responses for found/not-found emails
- [x] **Timing oracle protection** — Dummy hash on password path
- [x] **One-time magic link use** — Nonce rotation prevents replay
- [ ] **Session fixation prevention** — No session regeneration after login (CR-AUTH-02)
- [ ] **Session duration enforced** — `SESSION_DURATION_DAYS` not wired (CR-AUTH-05)
- [ ] **Dependency health in health check** — `/health` does not check Postgres or Valkey (CR-AUTH-08)

---

## Testing

### Test Files

- `Cove/tests/integration/test_auth_routes.py`
- `Cove/tests/integration/test_member_routes.py`
- `Cove/tests/integration/test_directory_profile.py`
- `Cove/tests/unit/test_access_tiers.py`
- `Cove/tests/smoke/test_auth_redirects.py`

### Coverage Summary

| Area | Covered | Gap |
|------|---------|-----|
| Login form renders | Yes | — |
| Bad credentials rejected | Yes | — |
| Logout redirects | Yes | — |
| Bad token renders error | Yes | — |
| Protected routes redirect to login | Yes (parametrized smoke) | — |
| Dashboard/profile/directory for auth user | Yes | — |
| Magic link generation + verification | **Partial** | No test for nonce rotation rejection |
| Rate limiting | **No** | No test for rate limit enforcement |
| Privacy consent gate | **No** | No test for redirect to accept-privacy |
| Session fixation | **No** | No test for session ID change on login |
| Timing oracle | **No** | No test for constant-time response |

### Test Configuration

`TestConfig`: `WTF_CSRF_ENABLED=False`, `SESSION_TYPE="null"` (no Valkey needed),
`RATELIMIT_STORAGE_URI="memory://"`. Uses `cove_test` database.

---

## Known Issues & Tech Debt

| Issue | Impact | Status |
|-------|--------|--------|
| `String(36)` PKs instead of native UUID | Storage waste, no native UUID indexing | Tracked (CR-AUTH-13) |
| `datetime.utcnow()` in model defaults | Naive UTC timestamps, should be timezone-aware | Known divergence |
| `complete_onboarding()` uses `datetime.utcnow()` for `term_start` | Mixed aware/naive timestamps in `member_roles` | Known divergence |
| `DirectoryPreference` column defaults are False but service writes True | Schema/service mismatch at onboarding | Minor tech debt |
| Privacy consent gate exempts `agent.*` | Safe now but review if agent surfaces member data | Intentional |
| Short lot login covers Sea Cove Dr only | Other streets need full lot email | UX gap (CR-AUTH-11) |
