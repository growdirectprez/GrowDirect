# SDD: Auth Module

**Status:** Active
**Last updated:** 2026-03-29
**Blueprint:** `auth_bp`, registered at `/auth`

**Wiki:** [[Brain/wiki/cove-governance|Cove Governance]]

---

## Overview

Handles member authentication via two paths: password login (dev/fallback) and magic link (production). Session management is via Flask-Login with `remember=True`. New members are routed to onboarding on first login.

---

## Routes

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/auth/login` | None | Show login form (redirects to dashboard if already authenticated) |
| POST | `/auth/login` | None | Password login (fields: `email`+`password`) or magic link (field: `email` only) |
| GET | `/auth/verify/<token>` | None | Consume a magic link token, log in, rotate nonce |
| GET | `/auth/logout` | Required | Logout and redirect to public landing |

### Login dispatch logic

`POST /auth/login`:
- Uses `LoginForm` which validates `email` (required) and `password` (optional)
- If `password` present → password login path: find member by `email`, check hash, `login_user()`
- If `password` empty → magic link path: find member, generate nonce + token, send email
- Magic link path always flashes a non-revealing message and redirects to `/auth/login` regardless of whether the email is found (no enumeration)

### Verify behavior

`GET /auth/verify/<token>`:
- On failure (expired/invalid token or nonce mismatch): flashes error and renders `auth/verify.html` with `success=False`
- On success: rotates nonce to `None`, updates `last_login_at`, calls `login_user()`, redirects to onboarding or dashboard

---

## Forms

**`cove/auth/forms.py`**

### `LoginForm` (extends `CoveForm`)

| Field | Type | Validators | Notes |
|-------|------|------------|-------|
| `email` | `StringField` | `DataRequired` | Primary login identifier (accepts email or lot ID like `25seacove`) |
| `password` | `PasswordField` | (none) | Optional — when empty, triggers magic link path |

---

## Models Used

**Member** (`members` table):
- `lot_email` — primary login identifier; accepts bare prefix (`25SeaCove`) or full address
- `personal_email` — magic link delivery target; must be set before magic link works
- `password_hash` — werkzeug hash; nullable; dev/fallback only
- `magic_link_nonce` — UUID rotated on every successful login; one-time use enforcement
- `last_login_at` — updated on each successful login
- `onboarded` — if False, redirects to `/member/onboarding` post-login
- `is_active` — Flask-Login uses this to block inactive accounts

Email lookup: case-insensitive OR across `lot_email` and `personal_email` using SQLAlchemy `or_()`.

---

## Services

**`cove/auth/services.py`**

| Function | What it does |
|----------|-------------|
| `generate_magic_link_token(member_id, nonce)` | Signs `{"member_id": ..., "nonce": ...}` with `itsdangerous.URLSafeTimedSerializer`, salt `"magic-link"` |
| `verify_magic_link_token(token, max_age=None)` | Verifies signature and age (default: `MAGIC_LINK_EXPIRY` config, 900s). Returns payload dict or None |

**`cove/auth/email.py`**

| Function | What it does |
|----------|-------------|
| `send_magic_link_email(member, token)` | Sends HTML+text email to `member.personal_email` via Flask-Mail. Raises `ValueError` if `personal_email` is unset. Link: `url_for("auth.verify", token=token, _external=True)` |

---

## Templates

| Template | Description |
|----------|-------------|
| `auth/login.html` | Alpine.js mode toggle between password and magic link forms |
| `auth/verify.html` | Rendered on verify failure (`success=False`); shows error flash and link to request a new login link |

---

## Session Management

- `login_user(member, remember=True)` — persistent cookie
- Session duration governed by `SESSION_DURATION_DAYS` env var (default 7)
- `login_manager.login_view = "auth.login"` — unauthenticated requests redirect here with `?next=<url>`
- User loader: `db.session.get(Member, user_id)` registered via `@login_manager.user_loader` inside `create_app()` in `cove/__init__.py`

---

## Security Notes

- Magic link nonce is rotated on every successful verify — tokens are single-use
- Email enumeration is prevented: flash message is identical whether or not the address exists, and the route redirects to login in both cases
- Password re-authentication is required at vote cast time (not just login)
- `personal_email` must be set before magic link delivery works; members without it fall back to password login
- Open redirect protection: `next` parameter is validated to be a relative URL only (`_is_safe_redirect` checks for empty scheme and netloc)
