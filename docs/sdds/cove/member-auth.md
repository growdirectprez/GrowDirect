# Member Auth & Privacy

> **Status:** Complete — written from code
> **Namespace:** cove
> **Last updated:** 2026-03-30
> **Code location:** `Cove/cove/auth/`, `Cove/cove/member/`

---

## 1. Overview

Member Auth & Privacy governs how Cove authenticates HOA members, manages their
sessions, and enforces the privacy rules that control what personal information
appears in the member directory.

The system is built around two constraints that are unique to HOA governance:

1. **Lot-based email identity.** Every property in the association has a
   permanent email address (`{lot#}{street}@abalonecove.org`, e.g.,
   `25SeaCove@abalonecove.org`). This address belongs to the lot, not the
   owner. When ownership transfers, the lot email stays; Cloudflare Email
   Routing updates the forwarding destination. A member authenticates using
   either their lot email or their personal email, but the lot email is the
   canonical identity.

2. **Privacy defaults that match community norms.** Lot email and address are
   always visible — they are property records, not personal data. A member's
   personal contact information (phone, personal email) is hidden by default
   and requires explicit opt-in. Board members can override all privacy
   preferences to perform governance work.

Authentication uses magic links as the primary path (no password to remember or
lose) with a werkzeug password hash as a dev/fallback path. Sessions are stored
in Valkey DB 1 via Flask-Session. All new members must accept the Cove privacy
policy before accessing any protected route.

---

## 2. Architecture

### Component Diagram

```
Browser
  │
  ├─ GET/POST /auth/login ──────────────── auth_bp (cove/auth/routes.py)
  │    ├─ LoginForm (WTForms)
  │    ├─ generate_magic_link_token()      cove/auth/services.py
  │    └─ send_magic_link_email()          cove/auth/email.py
  │
  ├─ GET /auth/verify/<token> ─────────── auth_bp
  │    └─ verify_magic_link_token()        cove/auth/services.py
  │
  ├─ GET /auth/logout ─────────────────── auth_bp
  │
  ├─ GET/POST /member/onboarding ─────── member_bp (cove/member/routes.py)
  │    └─ complete_onboarding()            cove/member/services.py
  │
  ├─ GET/POST /member/accept-privacy ─── member_bp
  │    └─ privacy_consent_at stamp
  │
  ├─ GET/POST /member/profile ────────── member_bp
  │    ├─ update_profile()                 cove/member/profile_services.py
  │    └─ update_directory_preferences()   cove/member/services.py
  │
  └─ GET /member/directory[/<apn>] ───── member_bp
       ├─ search_directory()               cove/member/services.py
       └─ get_parcel_profile_data()        cove/member/services.py

Extensions (cove/extensions.py)
  ├─ db         — SQLAlchemy 2.0 (PostgreSQL 17)
  ├─ login_manager  — Flask-Login, login_view="auth.login"
  ├─ mail       — Flask-Mail (MailHog dev / Cloudflare prod)
  ├─ csrf       — Flask-WTF CSRFProtect
  ├─ sess       — Flask-Session → Valkey DB 1
  ├─ talisman   — Flask-Talisman (CSP, HSTS, X-Frame)
  └─ limiter    — Flask-Limiter (rate limit on /auth/login, /auth/verify)

Data layer
  ├─ Member (members)
  ├─ Role (roles)
  ├─ MemberRole (member_roles) — temporal
  └─ DirectoryPreference (directory_preferences)
```

### Request / Data Flow

**Magic link login:**

```
1. User submits email (or short lot ID, e.g. "25seacove") to POST /auth/login
2. Route normalises input: if no "@", appends "dr@abalonecove.org"
3. Lookup: SELECT FROM members WHERE lot_email = ? OR personal_email = ?
4. If member not found: flash generic message (no user enumeration)
5. If found and no password in form:
   a. Generate UUID nonce, persist to member.magic_link_nonce
   b. Call generate_magic_link_token(member.id, nonce)
      → URLSafeTimedSerializer.dumps({member_id, nonce}, salt="magic-link")
   c. Call send_magic_link_email(member, token)
      → Raises ValueError if member.personal_email is None
   d. Flash "Check your email..." and redirect to GET /auth/login
6. User clicks /auth/verify/<token>
7. verify_magic_link_token(token) → loads with salt="magic-link", max_age=MAGIC_LINK_EXPIRY
   → Returns {member_id, nonce} or None on SignatureExpired / BadSignature
8. Lookup member by member_id; compare member.magic_link_nonce == payload["nonce"]
   → Nonce mismatch = link already used
9. Rotate: set member.magic_link_nonce = None, set last_login_at, commit
10. login_user(member, remember=True)
11. Redirect: /member/onboarding if not member.onboarded, else /member/dashboard
```

**Password login (fallback):**

```
1. User submits email + password to POST /auth/login
2. Same member lookup (lot_email or personal_email)
3. check_password_hash(member.password_hash, password)
4. On success: set last_login_at, login_user(member, remember=True)
5. Redirect to ?next= param (safe redirect check) or dashboard/onboarding
6. On failure: flash "Invalid email or password."
```

**Privacy consent gate (before_request hook in cove/__init__.py):**

```
Every request from an authenticated, onboarded member:
  IF member.privacy_consent_at IS NULL
  AND endpoint is not in {auth.*, public.*, static, agent.*, member.accept_privacy}
  → Redirect to /member/accept-privacy

POST /member/accept-privacy:
  form.accepted == True → member.privacy_consent_at = utcnow(), commit
  form.accepted == False → flash error, stay on page
```

**Onboarding flow (first login only):**

```
login_user() → member.onboarded is False → redirect /member/onboarding
  OnboardingForm: display_name, personal_email, phone, show_email, show_phone
  complete_onboarding():
    - Sets member.name, personal_email, phone
    - Sets member.onboarded = True
    - Assigns "member" role if not already present (MemberRole with term_start=now)
    - Calls update_directory_preferences(show_name=True, show_address=True,
        show_email=form value, show_phone=form value)
    - Commits
```

### Key Design Decisions

**Lot email as canonical identity, not personal email.**
The lot email (`25SeaCove@abalonecove.org`) is the permanent identifier for the
lot. It is always shown in the directory because it is a property-level address,
not personal information. It is the login username. When a property sells, the
lot email continues to exist; only the Cloudflare Email Routing target changes.
Personal email is the forwarding destination and is treated as PII — hidden by
default.

**Magic link over OTP or TOTP.**
HOA members are not sophisticated software users. A link in email requires no
app, no code entry, and no password management. The one-time nonce stored on
the Member row ensures links cannot be replayed. The 15-minute expiry is short
enough to prevent abuse of stolen emails but long enough to account for mail
delivery delay.

**Nonce rotation on use.**
`magic_link_nonce` is set to a new UUID when a link is generated and set to
`NULL` when the link is verified. A second click on the same link will find
`member.magic_link_nonce != payload["nonce"]` (NULL vs. the nonce in the token)
and reject the request. Generating a new magic link also invalidates all
previous links because the nonce changes.

**No user enumeration.**
When a magic link request is made for an unknown email, the response is
identical to a successful request: "If that email is registered, you'll receive
a login link shortly." This prevents probing for which emails are registered.

**Board view overrides all privacy preferences.**
`current_user.is_board` is tested at every directory access point. Board members
see all contact information regardless of `DirectoryPreference` settings. This
is intentional — board members need full contact access for governance work
(quorum notices, violation letters, emergency communication).

**Lot-short login.**
Members may enter just their lot ID (`25seacove`) without an email address. The
login route appends `dr@abalonecove.org` to construct the full lot email. This
matches the WPBCA address pattern (all lots on Sea Cove Dr, Packet Rd,
Barkentine Ln, Clipper Ln, Peppertree Ln — the `dr` suffix is a convenience
default for the most common street). Members on other streets must use their
full lot email.

---

## 3. Data Model

All models are in `Cove/cove/models/member.py`. Primary keys use `String(36)`
(UUID stored as string) — a holdover from the initial schema. New tables use
native `Mapped[uuid.UUID]`. Do not propagate the String(36) pattern.

### Member

Table: `members`

```python
class Member(UserMixin, db.Model):
    id: Mapped[str]                      # String(36), PK, uuid4
    organization_id: Mapped[str]         # FK → organizations.id
    apn: Mapped[str | None]              # FK → parcels.apn, nullable
    name: Mapped[str]                    # Display name (255)
    lot_email: Mapped[str]               # Unique. "25SeaCove@abalonecove.org"
    personal_email: Mapped[str | None]   # Forwarding target. PII.
    phone: Mapped[str | None]            # PII. Opt-in for directory.
    unit_identifier: Mapped[str]         # "25 Sea Cove Dr" (100)
    voting_weight: Mapped[int]           # Default 1. Combined lot = 1 vote still.
    delivery_preference: Mapped[str]     # "electronic" | "paper" | "both"
    membership_status: Mapped[str]       # "active" | "suspended" | "inactive"
    assessment_status: Mapped[str]       # "current" | "delinquent"
    password_hash: Mapped[str | None]    # werkzeug hash. Dev / fallback only.
    magic_link_nonce: Mapped[str | None] # UUID. Rotated on each login. NULL after use.
    is_active: Mapped[bool]              # Flask-Login. Default True.
    onboarded: Mapped[bool]              # False until first login flow complete.
    privacy_consent_at: Mapped[datetime | None]  # NULL until policy accepted.
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    last_login_at: Mapped[datetime | None]

    # Relationships
    parcel: Mapped["Parcel"]                          # back_populates="member"
    roles: Mapped[list["MemberRole"]]                 # lazy="joined"
    directory_preferences: Mapped["DirectoryPreference"]  # uselist=False

    # Computed properties (not columns)
    @property is_admin   # role.name == "admin" AND mr.is_current
    @property is_board   # role.name in ("board", "admin") AND mr.is_current
    @property is_inspector  # role.name == "inspector" AND mr.is_current
    @property is_arc     # role.can_access_arc AND mr.is_current
```

Flask-Login integration: `get_id()` returns `self.id`. User loader:
`db.session.get(Member, user_id)`.

### Role

Table: `roles`

```python
class Role(db.Model):
    id: Mapped[str]               # String(36), PK, uuid4
    organization_id: Mapped[str]  # FK → organizations.id
    name: Mapped[str]             # "admin" | "board" | "member" | "inspector" | "arc_committee"
    description: Mapped[str | None]
    can_vote: Mapped[bool]              # Default True
    can_create_proposals: Mapped[bool]  # Default False
    can_manage_members: Mapped[bool]    # Default False
    can_manage_treasury: Mapped[bool]   # Default False
    can_access_envelopes: Mapped[bool]  # Inspector only. Default False.
    can_access_arc: Mapped[bool]        # ARC committee. Default False.
    created_at: Mapped[datetime]
```

Role names in use at WPBCA: `admin`, `board`, `member`, `inspector`,
`arc_committee`. Roles are organization-scoped — the same `roles` table serves
all orgs in a multi-tenant deployment.

### MemberRole

Table: `member_roles` — temporal join between Member and Role.

```python
class MemberRole(db.Model):
    id: Mapped[str]               # String(36), PK, uuid4
    member_id: Mapped[str]        # FK → members.id
    role_id: Mapped[str]          # FK → roles.id
    term_start: Mapped[datetime]  # When the role becomes active
    term_end: Mapped[datetime | None]  # NULL = indefinite (e.g. regular member)
    assigned_by: Mapped[str | None]   # FK → members.id, nullable
    created_at: Mapped[datetime]

    @property is_current  # term_start <= utcnow() <= term_end (or open-ended)
```

Board director terms have `term_end` set to the end of their elected term.
The base "member" role assigned at onboarding has `term_end = NULL` (indefinite).
`is_current` is evaluated in Python — not a database-level flag — so role checks
always reflect the current wall clock.

### DirectoryPreference

Table: `directory_preferences` — one row per member, created at onboarding.

```python
class DirectoryPreference(db.Model):
    id: Mapped[str]              # String(36), PK, uuid4
    member_id: Mapped[str]       # FK → members.id, UNIQUE
    show_name: Mapped[bool]      # Default False (set True at onboarding)
    show_address: Mapped[bool]   # Default False (set True at onboarding)
    show_email: Mapped[bool]     # Default False. Personal email opt-in.
    show_phone: Mapped[bool]     # Default False. Phone opt-in.
    updated_at: Mapped[datetime]
```

Note: the table defaults `show_name` and `show_address` to `False`, but
`complete_onboarding()` and `update_directory_preferences()` always write
`show_name=True, show_address=True` as the starting state. Lot email is never
gated by this table — it is always visible.

---

## 4. Interfaces

### Auth Blueprint (`/auth`)

| Method | Path | Rate limit | Description |
|--------|------|------------|-------------|
| GET | `/auth/login` | 5/min | Render login form |
| POST | `/auth/login` | 5/min | Magic link dispatch or password auth |
| GET | `/auth/verify/<token>` | 5/min | Consume magic link token, start session |
| GET | `/auth/logout` | — | Destroy session, redirect to landing |

**POST /auth/login — magic link path**

Request body (form-encoded):
```
email=<lot_email or personal_email or short_lot_id>
```
Response: redirect to `GET /auth/login` with flash message. Never reveals
whether the email exists.

**POST /auth/login — password fallback path**

Request body:
```
email=<email>
password=<password>
```
Response: redirect to `/member/dashboard` or `/member/onboarding` on success.
Flash error on failure.

**GET /auth/verify/`<token>`**

URL-safe signed token (itsdangerous). On success: session started, redirect to
onboarding or dashboard. On failure: renders `auth/verify.html` with
`success=False`.

### Member Blueprint (`/member`)

All routes require `@login_required`. Unauthenticated requests are redirected
to `/auth/login?next=<original_url>`.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/member/dashboard` | Member dashboard with notifications and parcel profile |
| GET | `/member/directory` | Full directory listing; `?q=` for search |
| GET | `/member/directory/<apn>` | APN-centric profile page |
| GET/POST | `/member/profile` | Edit profile, contact info, directory preferences |
| GET | `/member/uploads/avatars/<filename>` | Serve uploaded avatar (login required) |
| GET/POST | `/member/accept-privacy` | Privacy policy acceptance gate |
| GET/POST | `/member/onboarding` | First-login setup flow |
| GET | `/member/notifications` | All notifications |
| POST | `/member/notifications/<id>/read` | Mark one read |
| POST | `/member/notifications/read-all` | Mark all read |

### Forms

**LoginForm** (`cove/auth/forms.py`)
- `email`: StringField, DataRequired. Accepts lot email, personal email, or
  short lot ID.
- `password`: PasswordField, Optional. Presence triggers password auth path.
- Inherits CSRFProtect from CoveForm.

**OnboardingForm** (`cove/member/forms.py`)
- `display_name`: StringField, Optional, max 255
- `personal_email`: StringField, Optional, Email validator, max 255
- `phone`: StringField, Optional, max 20
- `show_email`: BooleanField, default False
- `show_phone`: BooleanField, default False

**ProfileForm** (`cove/member/forms.py`)
- `display_name`, `bio` (max 1000), `personal_email`, `phone`
- `avatar`: FileField, allowed: jpg, jpeg, png, gif; max 2 MB
- `share_avatar`, `share_bio`: BooleanField (parcel profile visibility)
- `show_phone`, `show_email`: BooleanField (directory preference visibility)

**PrivacyAcceptForm** (`cove/member/forms.py`)
- `accepted`: BooleanField, manually checked in route (not WTForms DataRequired)
- `submit`: SubmitField

---

## 5. Service Layer

### cove/auth/services.py

**`generate_magic_link_token(member_id: str, nonce: str) -> str`**

Creates a URL-safe signed token using `itsdangerous.URLSafeTimedSerializer`.
Payload: `{"member_id": str, "nonce": str}`. Signed with `SECRET_KEY`,
salted with `"magic-link"`. Returns the token string for embedding in the
verification URL.

**`verify_magic_link_token(token: str, max_age: int | None = None) -> dict | None`**

Loads and validates the token. Defaults `max_age` to `MAGIC_LINK_EXPIRY`
config (default 900s). Returns `{"member_id": str, "nonce": str}` on success.
Returns `None` on `SignatureExpired` or `BadSignature`. Never raises.

### cove/auth/email.py

**`send_magic_link_email(member: Member, token: str) -> None`**

Constructs the verification URL with `url_for("auth.verify", token=token, _external=True)`.
Sends a Flask-Mail `Message` to `member.personal_email`.
Raises `ValueError` if `member.personal_email` is `None` — the route catches
this and flashes an error asking the member to use their password instead.
Sends both plain-text and HTML bodies. HTML uses inline styles; no external
CSS dependencies.

### cove/member/services.py

**`complete_onboarding(member, display_name, personal_email, phone, show_email, show_phone) -> Member`**

Called from `POST /member/onboarding`. Sets `member.name`, `personal_email`,
`phone`. Sets `member.onboarded = True`. Assigns the "member" role via
`MemberRole` if not already present (looks up `Role` by `name="member"` within
the member's organization). Calls `update_directory_preferences()` with
`show_name=True, show_address=True` and the caller-supplied email/phone flags.
Commits.

**`update_directory_preferences(member_id, show_name, show_address, show_email, show_phone) -> DirectoryPreference`**

Upsert on `directory_preferences`. Creates a new row if none exists.
Always commits.

**`get_directory_listings(org_id: str, board_view: bool = False) -> list[dict]`**

Returns all parcels where `is_association_member=True`, ordered by street then
numeric address. Each entry is built by `_parcel_to_entry()`. Includes parcels
with no registered Cove account (`has_account=False`). Used for full directory
render when no search query is present.

**`search_directory(org_id: str, query: str, board_view: bool = False) -> list[dict]`**

If query is empty, delegates to `get_directory_listings()`. Otherwise searches
`parcels` by `owner_name`, `street`, `address`, or `apn` using `ilike`. Returns
same dict structure. Searching is always against the parcel table so unregistered
lots are still findable.

**`get_parcel_profile_data(apn: str, board_view: bool = False) -> dict | None`**

Builds the full data dict for the `/member/directory/<apn>` profile page.
Returns `None` if the parcel does not exist. Applies share toggles
(`share_household`, `share_pets`, `share_bio`) unless `board_view=True`.
Redacts `email` and `phone` from contacts who are minors. Returns:
`parcel`, `member`, `profile`, `display_name`, `bio`, `avatar_url`,
`contacts`, `pets`, `show_email`, `show_phone`, `voting_weight`, `roles`.

**`_parcel_to_entry(parcel, board_view) -> dict`**

Internal. Constructs a flat directory entry from a Parcel + optional Member +
optional ParcelProfile. Privacy logic:
- `lot_email`: always populated from `parcel.lot_email`
- `address`: always populated
- `phone`: populated only if `board_view` or `prefs.show_phone`
- `personal_email`: populated only if `board_view` or `prefs.show_email`
- `avatar_url`, `bio`, `pets`: from `get_profile_for_directory()` which
  applies `share_avatar`, `share_bio`, `share_pets` toggles

### cove/member/profile_services.py

**`get_or_create_profile(apn: str) -> ParcelProfile`**

Returns the `ParcelProfile` for the given APN, creating an empty one if none
exists. Commits on creation.

**`update_profile(apn: str, **kwargs) -> ParcelProfile`**

Sets any combination of allowed fields:
`display_name`, `avatar_url`, `bio`, `pets`,
`share_bio`, `share_household`, `share_pets`, `share_avatar`.
Rejects unknown keys via `_ALLOWED_FIELDS` guard. Commits.

**`get_profile_for_directory(apn: str) -> dict`**

Returns only what the owner chose to share:
`display_name` (always), `avatar_url` (if `share_avatar`), `bio` (if
`share_bio`), `pets` (if `share_pets`). Returns a dict of all-`None` values
if no profile exists.

---

## 6. Configuration

All values are read from environment variables (or `.env`). Set in
`Cove/cove/config.py`.

| Key | Default | Description |
|-----|---------|-------------|
| `SECRET_KEY` | required | Signs magic link tokens and CSRF tokens |
| `MAGIC_LINK_EXPIRY` | `900` | Token max age in seconds (15 minutes) |
| `SESSION_DURATION_DAYS` | `7` | Flask-Login "remember me" duration |
| `SESSION_TYPE` | `"redis"` | Flask-Session backend. `"null"` in TestConfig. |
| `VALKEY_URL` | `redis://growdirect_valkey:6379/1` | Valkey DB 1 for sessions |
| `MAIL_SERVER` | `"localhost"` | SMTP host (MailHog in dev) |
| `MAIL_PORT` | `1025` | SMTP port (MailHog: 1025 / 1026) |
| `MAIL_USE_TLS` | `false` | TLS for SMTP (true in prod via Cloudflare) |
| `MAIL_DEFAULT_SENDER` | `"cove@abalonecove.org"` | From address |
| `DOMAIN` | `"abalonecove.org"` | Used for lot email construction |
| `UPLOAD_FOLDER` | `<project_root>/uploads` | Avatar storage path |
| `MAX_AVATAR_SIZE` | `2097152` (2 MB) | Avatar upload limit |

**Environment-specific overrides:**

`DevConfig`: `DEBUG=True`, `SESSION_COOKIE_SECURE=False`

`TestConfig`: `WTF_CSRF_ENABLED=False`, `SESSION_TYPE="null"` (no Valkey
dependency in tests), `SQLALCHEMY_ENGINE_OPTIONS={}` (no pool options).

`ProdConfig`: `SESSION_COOKIE_SECURE=True`, `SESSION_COOKIE_HTTPONLY=True`,
`SESSION_COOKIE_SAMESITE="Lax"`, `REMEMBER_COOKIE_SECURE=True`,
`REMEMBER_COOKIE_HTTPONLY=True`.

**Rate limiting:**
`RATELIMIT_STORAGE_URI` is set from `VALKEY_URL` in the app factory.
`/auth/login` and `/auth/verify/<token>` are decorated with
`@limiter.limit("5/minute")`.

---

## 7. Security & Compliance

### Lot-Based Email Identity and PII Boundary

The lot email (`25SeaCove@abalonecove.org`) is treated as property-level
information, not personal data. It is always visible in the directory, included
in public-facing parcel records, and used as the login username. This is
intentional and consistent with HOA governance practice — the email address
corresponds to the property, not the resident.

Personal email (`member.personal_email`) is PII. It is:
- Hidden from the directory by default (`show_email=False`)
- Only revealed when the member explicitly opts in, or to board members
- Never sent in magic link emails to lot emails (magic links go to
  `personal_email` only, which is why onboarding must collect it first)

### Magic Link Security Properties

- **One-time use.** The nonce on the Member row is `NULL`ed after first use.
  Subsequent clicks on the same link fail the nonce check.
- **Short-lived.** 15-minute expiry enforced by `itsdangerous` timestamp
  in the token itself.
- **One active link.** Generating a new magic link overwrites `magic_link_nonce`,
  invalidating all previous links for that member.
- **No user enumeration.** The login route returns the same flash message
  whether the email is found or not.
- **Signed token.** `URLSafeTimedSerializer` uses `SECRET_KEY` + `"magic-link"`
  salt. Tampering produces `BadSignature`.

### Open Redirect Prevention

`_is_safe_redirect(target)` in `auth/routes.py` checks that `scheme == ""`
and `netloc == ""`. Only relative paths are accepted for the `?next=` redirect
after login.

### CSRF Protection

All forms inherit from `CoveForm` which wraps `FlaskForm`. `csrf` extension
(Flask-WTF `CSRFProtect`) is applied globally at the app factory. CSRF is
disabled only in `TestConfig` (`WTF_CSRF_ENABLED=False`).

### Session Security

- Sessions stored server-side in Valkey DB 1 (not in the cookie). The cookie
  contains only a session ID.
- In production: `SESSION_COOKIE_SECURE=True`, `HTTPONLY=True`,
  `SAMESITE="Lax"`. Remember-cookie has the same flags.
- Logout calls `flask_login.logout_user()` which invalidates the server-side
  session.

### HTTP Security Headers (Flask-Talisman)

The `talisman` extension enforces:
- Content-Security-Policy: `default-src 'self'` with narrow allowlists for
  inline scripts (Alpine.js), Google Fonts, and OpenStreetMap tiles.
- `X-Frame-Options: DENY` (clickjacking prevention)
- `X-Content-Type-Options: nosniff`
- HSTS: enabled only when `SESSION_COOKIE_SECURE=True` (prod/staging)

### Privacy Policy Gate

`_check_privacy_consent()` runs on every request from an authenticated,
onboarded member. If `privacy_consent_at` is NULL, all non-exempt routes
redirect to `/member/accept-privacy`. Exempt endpoints: `auth.*`, `public.*`,
`static`, `agent.*`, `member.accept_privacy`. This is a blocking gate — the
member cannot access any platform functionality until they accept.

### Board Access Override

`current_user.is_board` bypasses all `DirectoryPreference` and
`ParcelProfile` share toggles in `services.py` and `profile_services.py`.
This is explicit — board members need full contact access for governance work.
The override is enforced in the service layer, not in templates, so it cannot
be bypassed by direct route calls.

### Inspector Separation (Davis-Stirling)

The `inspector_required` decorator aborts 403 for any non-inspector accessing
ballot envelope routes. The `Role.can_access_envelopes` flag is the data-layer
guard. `BallotEnvelope` additionally uses PostgreSQL Row-Level Security. These
are complementary controls — both must be in place.

---

## 8. Error Handling

| Scenario | Behavior |
|----------|----------|
| Magic link expired (> 15 min) | `verify_magic_link_token` returns `None`. Flash "expired or invalid". Render `auth/verify.html` with `success=False`. |
| Magic link already used (nonce rotated) | `member.magic_link_nonce != payload["nonce"]`. Flash "already been used". Same template. |
| Magic link tampered | `BadSignature` caught by `verify_magic_link_token`. Returns `None`. Same template. |
| Email not found at login | Flash generic message (no enumeration). Redirect to GET /auth/login. |
| Magic link to member with no personal_email | `send_magic_link_email` raises `ValueError`. Route catches, flashes "No personal email on file. Please enter your password." |
| Wrong password | Flash "Invalid email or password." Stay on login form. |
| Unauthenticated access to protected route | Flask-Login redirects to `/auth/login?next=<url>`. |
| Authenticated but missing privacy consent | `before_request` redirects to `/member/accept-privacy`. |
| Privacy form submitted with `accepted=False` | Flash "You must accept..." Stay on accept-privacy page. |
| Directory profile for unknown APN | `get_parcel_profile_data` returns `None`. Route calls `abort(404)`. |
| Avatar file too large | Flash "Avatar image must be under 2 MB." Re-render profile form. |
| Avatar file wrong type | Flash "Avatar must be a PNG, JPG, GIF, or WebP image." Re-render. |
| Non-board member accessing board route | `board_required` / `board_or_admin_required` decorator calls `abort(403)`. |
| Non-inspector accessing envelope route | `inspector_required` calls `abort(403)`. |

---

## 9. Testing

Test files:
- `Cove/tests/integration/test_auth_routes.py`
- `Cove/tests/integration/test_member_routes.py`
- `Cove/tests/integration/test_directory_profile.py`
- `Cove/tests/unit/test_access_tiers.py`
- `Cove/tests/smoke/test_auth_redirects.py`

### Smoke Tests (`test_auth_redirects.py`)

Parametrized over `PROTECTED_ROUTES`:
- Every protected route (`/member/dashboard`, `/vote/`, `/vault/`, `/meetings/`,
  `/map/`, `/treasury/`, `/archive/`, `/board/`) returns a 3xx redirect for
  unauthenticated requests.
- Redirect location contains `"login"` or `"auth"`.

### Integration Tests — Auth Routes (`test_auth_routes.py`)

- `GET /auth/login` returns 200 and renders form
- `POST /auth/login` with bogus credentials stays on login or shows error
- `GET /auth/logout` redirects to `/` (landing)
- `GET /auth/verify/<bad_token>` renders verify template with error, no 500

### Integration Tests — Member Routes (`test_member_routes.py`)

- Dashboard returns 200 for `authenticated_client`
- Dashboard redirects unauthenticated to login
- Profile page returns 200 for authenticated user
- Directory returns 200 for authenticated user
- Notifications page returns 200 for authenticated user

### Unit Tests — Access Tiers (`test_access_tiers.py`)

- `AccessTier` enum values
- Document defaults to `AccessTier.MEMBER`
- `Role.can_access_arc` defaults to `False`
- `Member.is_arc` is `True` with active ARC role, `False` without

### Test Configuration Notes

`TestConfig` sets `WTF_CSRF_ENABLED=False` and `SESSION_TYPE="null"`. No Valkey
connection required in tests. The `authenticated_client` fixture in
`conftest.py` creates a test member and establishes a login session using the
test client. Tests use `cove_test` database (`TEST_DATABASE_URL` env var or
default `localhost:5432/cove_test`).

---

## 10. Dependencies

### Upstream

| Dependency | Version | Use |
|------------|---------|-----|
| Flask-Login | — | Session management, `@login_required`, `current_user` |
| itsdangerous | — | Magic link token signing (`URLSafeTimedSerializer`) |
| werkzeug | — | `check_password_hash`, `generate_password_hash` (seed / admin) |
| Flask-Mail | — | SMTP delivery of magic link emails |
| Flask-WTF / WTForms | — | Form definitions, CSRF protection |
| Flask-Session | — | Server-side session storage |
| Flask-Limiter | — | Rate limiting on auth endpoints |
| Flask-Talisman | — | HTTP security headers, CSP |
| redis (Python) | — | Valkey client used by Flask-Session |
| SQLAlchemy 2.0 | — | ORM, `Mapped[]` syntax |
| PostgreSQL 17 | — | Primary data store (`cove` database) |
| Valkey 8 | DB 1 | Session store |
| MailHog | dev | SMTP trap (web UI port 8026, SMTP port 1026) |
| Cloudflare Email Routing | prod | Lot email forwarding to personal inbox |

### Downstream

**Governance (`cove/governance/`):** Voting eligibility is derived from
`Member.membership_status == "active"` and `Member.voting_weight > 0`.
The governance service queries members to determine quorum counts and ballot
issuance. It does not call auth services directly — it reads the Member model.

**Parcels (`cove/parcels/`):** The `Parcel ↔ Member` relationship is 1:1 via
`parcels.apn = members.apn`. Parcel routes display the member's role and
contact info in the parcel detail view (board view only). `ParcelProfile`
(in `cove/models/parcel_profile.py`) is managed by `profile_services.py` and
is keyed on `apn`, not `member_id` — surviving ownership transfers.

**Board (`cove/board/`):** Board management routes use `board_required` /
`admin_required` decorators from `cove/auth/decorators.py`. The board invite
flow creates pre-populated Member rows and assigns roles — it depends on
`complete_onboarding()` not running for board-imported members until they
first log in.

**Vault, Meetings, Treasury, Archive:** All protected by `@login_required`.
Some use `board_required` for admin actions. No direct calls into auth
services — only the decorator layer.

**Notifications (`cove/notifications/`):** Notification services use
`member_id` from `current_user.id`. The `before_request` hook runs before
the notification count context processor so unauthenticated users never hit
notification queries.

### Shared Infrastructure

- `growdirect_postgres:5432` — `cove` database
- `growdirect_valkey:6379/1` — Valkey DB 1, session store
- Cove MailHog (`cove_localhost_mailhog`) — dev SMTP, web UI at `:8026`

---

## 11. Known Issues & Reconciliation

**Short lot login covers Sea Cove Dr only.** The `dr@abalonecove.org` suffix
appended to bare lot IDs only works for members on Sea Cove Drive. Members on
Packet Road, Barkentine Lane, Clipper Lane, or Peppertree Lane must enter their
full lot email. This is a convenience shortcut for the most common address
pattern in the WPBCA test deployment, not a generalizable feature.

**`String(36)` primary keys.** All four models in `cove/models/member.py`
(`Member`, `Role`, `MemberRole`, `DirectoryPreference`) use `String(36)` for
UUIDs rather than the platform standard `Mapped[uuid.UUID]`. This is a
historical holdover. A migration to native UUID columns would be schema-breaking
and is tracked separately. Do not propagate `String(36)` to any new models.

**`datetime.utcnow()` in model defaults.** Several `mapped_column` defaults use
`datetime.utcnow` (naive UTC). The platform standard is `datetime.now(timezone.utc)`
(timezone-aware). This is consistent within the existing codebase but is a
known divergence. Awareness timestamps should be normalized when the Member
model is next migrated.

**`complete_onboarding()` uses `datetime.utcnow()` directly.** The `term_start`
written to `MemberRole` in `complete_onboarding()` calls `datetime.utcnow()`,
inconsistent with the route layer's use of `datetime.now(timezone.utc)`. Not a
functional bug but produces mixed-aware/naive timestamps in the same table if
roles are assigned through different paths.

**Privacy consent gate exempts `agent.*`.** The AI agent transparency routes
are exempt from the privacy consent redirect. This is intentional (agent
endpoints serve as a public/semi-public accountability log) but should be
reviewed if the agent endpoint ever surfaces member-specific data.

**DirectoryPreference `show_name` / `show_address` schema defaults are False.**
The column defaults on the table are `False` for all four fields. The service
layer always writes `show_name=True, show_address=True` during onboarding and
profile updates, so live data reflects the intended defaults. The mismatch
between table default and service intent is a minor tech debt — a future
migration should change the column defaults to match.
