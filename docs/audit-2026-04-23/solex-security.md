---
date: 2026-04-24
type: security-audit-report
classification: confidential
owner: GrowDirect LLC
phase: G2-extension
scope: Solex app (browser-facing Flask + Square sandbox)
---

# Solex Security Audit

## Summary

Solex is a browser-facing Flask 3.0.3 storefront with magic-link auth, Square sandbox checkout, subscriptions, and an admin console. The dedicated security pass surfaced **0 CRITICAL, 6 HIGH, 8 MEDIUM, 7 LOW** findings. The G2 platform-level concerns were confirmed and quantified, plus several additional issues — most consequentially CSRF protection is **disabled on every authentication and checkout endpoint**, both LoginManagers register against the same Flask app (the second wins), and there is no request-host allowlist.

**Recommendation: do not open partner access until at least all HIGH findings are remediated.** The specific blockers are:

- H1 (CSRF disabled on auth + cart + checkout)
- H2 (no `SESSION_COOKIE_SECURE`)
- H3 (no Host allowlist + `_external=True` magic links)
- H4 (no security response headers / Talisman)
- H5 (Dockerfile runs as root)
- H6 (vulnerable Jinja2 / Flask / python-dotenv)

Webhook signature verification, magic-link token entropy, magic-link TTL/one-shot enforcement, OWASP A03/A07 coverage, and SQLi posture are all in good shape — those areas are clean.

## Tool results

Outputs at `docs/audit-2026-04-23/solex-security-tool-output/`.

### bandit (12 findings — 1 HIGH, 11 LOW, all HIGH-confidence)

| Severity | Test | Location | Note |
|---|---|---|---|
| HIGH | B324 (weak MD5) | `solex/services/placeholder_gen.py:30` | False positive — MD5 used to deterministically derive a tile color from SKU; not security-bearing. Recommend `hashlib.md5(..., usedforsecurity=False)` to silence. |
| LOW | B101 (assert) | `solex/services/auth.py:36` | `assert audience in ("admin", "customer")` — fine in dev, but `assert` is stripped under `python -O`. Replace with explicit check + raise. |
| LOW | B101 (assert) | `solex/services/scenarios/high_value_sale.py:43`, `round_amount_cluster.py:52` | Same — replace asserts. |
| LOW | B110 (try/except/pass) | 6 sites in `routes/checkout.py`, `routes/lab.py`, `services/catalog_import.py`, `services/checkout.py`, `services/returns.py`, `services/subscriptions.py` | Most are intentional best-effort cart-clear/email-send. Document each with a comment so future readers can tell intentional from sloppy. |
| LOW | B311 (random) | `solex/services/scenarios/base.py:55` | Scenario simulator uses `random.*` — not a security path. Acceptable. |

### semgrep (4 findings — 1 ERROR, 3 WARNING)

Rule packs: `p/python`, `p/flask`, `p/owasp-top-ten`, `p/jwt`.

| Sev | Rule | Location |
|---|---|---|
| ERROR | `dockerfile.security.missing-user.missing-user` | `devops/Dockerfile:31` |
| WARN | `flask-url-for-external-true` | `solex/routes/account_auth.py:28` |
| WARN | `flask-url-for-external-true` | `solex/routes/admin_auth.py:40` |
| WARN | `insecure-hash-algorithm-md5` | `solex/services/placeholder_gen.py:30` |

The two `_external=True` warnings exactly match the platform-audit pre-flag (H3 below).

### pip-audit

Tool's bundled venv is Python 3.14, which can't resolve the pinned `psycopg[binary]==3.2.3` (oldest 3.14-compatible wheel is 3.2.10). Re-ran with that line excluded (`--no-deps --skip-editable`). psycopg is reviewed manually — current pin is two minor versions behind, no advisories tracked for 3.2.3 in OSV/PyPA.

**Production deps** (`requirements.txt`, 49 dists scanned):

| Package | Pinned | Vulns | Fix |
|---|---|---|---|
| flask | 3.0.3 | CVE-2026-27205 (missing `Vary: Cookie`, cache-poisoning of session-bearing responses) | 3.1.3 |
| jinja2 | 3.1.4 | CVE-2024-56326, CVE-2024-56201, CVE-2025-27516 (sandbox escapes; Solex doesn't use Jinja sandbox, so impact is informational) | 3.1.6 |
| python-dotenv | 1.0.1 | CVE-2026-28684 (symlink TOCTOU on `.env` writes — only triggered if `set_key()` is called, which Solex doesn't) | 1.2.2 |

**Dev deps** (`requirements-dev.txt`, 18 dists scanned):

| Package | Pinned | Vulns | Fix |
|---|---|---|---|
| pytest | 8.3.3 | CVE-2025-71176 (UNIX local DoS via `/tmp/pytest-of-{user}`) | 9.0.3 |
| Pillow | 11.0.0 | CVE-2026-25990 (PSD OOB write), CVE-2026-40192 (FITS decompression bomb). Pillow runs in CI/dev only via `placeholder_gen.py`; not on the request path. | 12.2.0 |

### gitleaks

Per audit instructions, gitleaks should have run on the full repo earlier (`docs/audit-2026-04-23/security-tool-output/gitleaks.json`). That file does **not exist** on disk — only `solex-security-tool-output/` is present under `docs/audit-2026-04-23/`. Recommend re-running the platform-wide gitleaks scan before partner access. Manual `grep` of `Solex/solex/`, `Solex/devops/`, `Solex/wsgi.py` for hardcoded secrets returned no matches.

`Solex/.env` exists locally with **real Square sandbox credentials** (`SQUARE_SANDBOX_ACCESS_TOKEN=EAAAl3ns-...`, webhook signature key, etc.) but `git check-ignore` confirms it is gitignored and not in the index. Sandbox-scoped, so blast radius is bounded — but rotate after partner access if those creds get embedded in any partner-facing artifact.

## Manual review

| Area | Finding |
|---|---|
| Magic-link token entropy | **Clean.** `secrets.token_urlsafe(32)` → 256 bits. SHA-256 hash stored, plaintext token only emailed. (`solex/services/auth.py:37`) |
| Magic-link TTL | **Clean.** 20 minutes hard-coded constant. (`solex/services/auth.py:12`) |
| Magic-link one-time-use | **Clean.** `consumed_at` set on use, second consume returns `None`. (`solex/services/auth.py:54`) |
| Magic-link issuance rate limit | **Clean.** `@limiter.limit("5 per minute")` on both `/admin/login/magic` and `/account/login/magic`. Customer-facing `/admin` form rate-limits at 10/min. |
| Magic-link replay protection | **Clean.** Tied to `consumed_at` + TTL + per-issuance new token. |
| `_external=True` Host allowlist | **HIGH (H3).** Both magic-link routes use `url_for(..., _external=True)`. No `SERVER_NAME`, no `TRUSTED_HOSTS`, no `ProxyFix` — Flask derives the URL from the `Host` request header. Attacker submits a magic-link request with `Host: evil.example` → user receives email with link to `evil.example/account/login/magic/<token>` → token leaks to attacker. The 5/min limit is per-IP, doesn't block this. |
| Session cookie flags | **HIGH (H2).** `BaseConfig` sets `HTTPONLY=True` and `SAMESITE="Lax"` but **no `SESSION_COOKIE_SECURE`**, and `ProdConfig` doesn't override. Session cookies will travel over plain HTTP if the deployment ever serves it. Same gap for any future remember-me cookie. |
| Security headers | **HIGH (H4).** No Flask-Talisman, no `@after_request` header injection, no CSP, no HSTS, no X-Frame-Options, no X-Content-Type-Options, no Referrer-Policy, no Permissions-Policy. The Square Web Payments SDK loads cross-origin iframes — without CSP, any future XSS is unbounded. |
| Square OAuth | **N/A.** Solex uses static Square sandbox token (`SQUARE_SANDBOX_ACCESS_TOKEN` env var); no merchant OAuth flow, no state param, no callback. |
| Square access token storage | **MEDIUM (M1).** Token sits in plaintext in `.env` and `current_app.config["SQUARE_ACCESS_TOKEN"]`. Acceptable for sandbox; for production should move to a secrets manager + vault rotation. |
| Square card token storage | **Clean.** Solex never stores raw card numbers — only Square's opaque `card_id` for cards-on-file (`solex/services/checkout.py:152` → `customer.square_customer_id` + `card['id']`). |
| Webhook signature verification | **Clean.** HMAC-SHA256, constant-time `hmac.compare_digest` (`solex/services/square_client.py:351`). Bad sig → `401`. |
| Webhook URL trust | **MEDIUM (M2).** `verify_webhook_signature` uses `request.url` (derived from `Host` header). If a reverse proxy strips/alters the Host or scheme, signatures will mismatch valid Square requests, *or* a misconfigured `X-Forwarded-*` could let an attacker forge the URL portion. Mitigation: pin the public webhook URL via config; pass that to verify rather than `request.url`. |
| Webhook idempotency | **Clean.** `square_event_id` has unique constraint; duplicate POSTs no-op via `IntegrityError` rollback (`solex/services/webhooks.py:36`). |
| Webhook timestamp/replay | **MEDIUM (M3).** No timestamp window check beyond Square's signature. An attacker who captures one valid signed webhook body can replay it indefinitely (within Square's signature lifetime, which Square doesn't bind to time). Idempotency on `square_event_id` blunts impact (already-seen → no-op), but a brand-new replay before legit delivery would still process. Add: reject events with `created_at` more than ~5 minutes old. |
| Rate limiting — login | **Clean.** Admin password 10/min, magic links 5/min each. Account dashboards/cart endpoints have no per-route limit; the global default is whatever `Flask-Limiter` defaults to (currently none — `Limiter(key_func=...)` with no `default_limits`). |
| Rate limiting — checkout | **MEDIUM (M4).** `/checkout/submit` has **no rate limit** and accepts JSON. Combined with no CSRF token (CSRF exempt), an attacker can drive Square API calls that consume Square's account-level rate budget and may incur per-call costs. Add a 10–20/min limit per IP and per session. |
| Rate limiting — cart | **LOW (L1).** Cart add/update/remove are unbounded. Worst case is Valkey memory pressure via cart bloat; not an account-fraud path. |
| Input validation — cart | **LOW (L2).** `qty = max(1, int(request.form.get("qty", 1)))` and `qty = max(0, int(request.form["qty"]))` accept arbitrary positive ints. No upper bound. Bad actor → quantity = 1e9 → ints overflow gracefully but cart `subtotal_cents` becomes meaningless. Cap at e.g. 99 per line. |
| Input validation — checkout price | **Clean.** `CartLineIn.price_cents` is sourced from the **server-side** Valkey snapshot, not client input (`solex/routes/checkout.py:62-71`). Client cannot tamper with line price. SKU is also server-snapshotted. |
| Input validation — checkout JSON | **MEDIUM (M5).** `data["email"]`, `data["name"]`, `data["shipping_address"]`, `data["payment_token"]` are pulled with raw `[]` dict access. No schema validation. A missing key throws `KeyError` → uncaught → 500. A malformed `shipping_address` (e.g., not a dict) propagates into `Order.shipping_address_json` (JSONB column, accepts anything). Recommend Pydantic input model. |
| Input validation — admin refund | **MEDIUM (M6).** `int(request.form.get("amount_cents", order.total_cents))` accepts any int including negative. A negative refund would fail at Square but the local code doesn't bound it. Should clamp `0 < amount_cents <= order.total_cents - already_refunded`. |
| Input validation — inventory adjust | **LOW (L3).** `delta = int(request.form["delta"])` is unbounded. Admin-only, but typo could create absurd inventory. UI bound or server bound recommended. |
| Logging — PII/tokens | **Clean.** No `current_app.logger.*` call interpolates magic-link tokens, payment tokens, passwords, or full email bodies. `EmailLog` table records `to` (email) and `template` only. |
| Audit log — admin actions | **MEDIUM (M7).** Inventory adjustments record `admin_user_id`. Refunds record nothing — `RefundsService.issue_refund` doesn't capture the issuing admin. Same for product create/update/delete in `admin_catalog`. Add `admin_user_id` to refund + product mutation paths. |
| Dockerfile runs as root | **HIGH (H5).** Confirmed. `devops/Dockerfile:31` has no `USER` directive; gunicorn runs as root inside the container. Fix: `RUN useradd -m -u 1000 solex && chown -R solex /app` and `USER solex`. |
| CSRF on auth/cart/checkout | **HIGH (H1).** `solex/__init__.py:39-43` exempts five blueprints: `api`, `cart`, `checkout`, `admin_auth`, `account_auth`. Combined consequences: <br>· `/account/login/magic` (POST email) — attacker page can POST with the victim's email field but using the attacker's session — pre-auth, low impact. <br>· `/admin/login` (POST password) — same, pre-auth. <br>· `/cart/add`, `/cart/update`, `/cart/remove` — attacker site can mutate victim's cart. Cosmetic alone, but combined with `/checkout/submit` and a stored card it's a fraud vector. <br>· **`/checkout/submit`** — accepts JSON, no CSRF. If a logged-in customer with `store_payment_token` visits attacker's page, attacker can `fetch('/checkout/submit', {credentials:'include', body:...})`. Same-Origin Policy blocks reading the response, but the **side effect (Square charge + saved-card) still fires**. Mitigation: re-enable CSRF on `cart` + `checkout` (forms can pass token via header), and on `admin_auth` and `account_auth` POSTs (use `flask-wtf` form). `api` (Square webhook) is correctly exempt. |
| Dual LoginManager bug | **HIGH (H8 → MEDIUM-HIGH).** `solex/extensions.py:34-37` instantiates both `admin_login` and `customer_login` and `init_app(app)` is called on **both** in `init_extensions` (lines 46-47). Flask-Login's `LoginManager.init_app` overwrites `app.login_manager` — the second-registered manager wins (here: `customer_login`). The `admin_required` helper in `routes/admin_utils.py` knows this and reads the session directly to load `AdminUser`. So admin auth works, but: <br>· `flask_login.current_user` resolves via `customer_login.user_loader` which fetches `Customer` by id — admin sessions where `_user_id` is an `AdminUser.id` will return `None` from `current_user`, *or* worse, return a Customer if a Customer happens to share that UUID (UUID collision is astronomically unlikely, but the bug class is real). <br>· The session itself is shared. There is no isolation between customer-facing `/account` and admin-facing `/admin` sessions — same cookie, same store, same `_user_id`. A customer who learned an admin's UUID and could write that to their session would be admin. (They can't write the session directly because Valkey is server-side, but if `SECRET_KEY` ever leaked, they could forge.) <br>Fix: use Flask blueprints with separate session prefixes, or use a single LoginManager with a polymorphic user model (rare in practice). The cleanest near-term fix is to scope admin auth to a separate cookie via `SESSION_COOKIE_NAME` with a request-time switch — or document that admin and customer must never log in from the same browser. |
| OWASP A01 — Broken Access Control | All `/account/*` routes scope by `current_user.id` and 404 on mismatch (verified in `account_orders.py`, `account_addresses.py`, `account_subscriptions.py`). All `/admin/*` routes use `@admin_required`. |
| OWASP A02 — Crypto failures | Magic links: SHA-256 hash, 256-bit token. Passwords: `werkzeug.security.generate_password_hash` (scrypt). Webhook: HMAC-SHA256. No issues. |
| OWASP A03 — Injection | All ORM-mediated. One raw `text("SELECT 1")` health probe, plus parameterized `:q` binding for FTS in `services/search.py`. No string-built SQL. No `eval`/`exec`/`shell=True`. |
| OWASP A04 — Insecure Design | Magic-link audience param (`"admin"|"customer"`) is asserted not enforced — see L4 below. |
| OWASP A05 — Misconfiguration | H2 (no Secure cookie), H4 (no security headers), H5 (root Docker), L5 (DEBUG-derived `WTF_CSRF_TIME_LIMIT = None` — token never expires within a session). |
| OWASP A06 — Vulnerable Components | H6 (Flask 3.0.3, Jinja 3.1.4, python-dotenv 1.0.1, Pillow 11.0.0). |
| OWASP A07 — Identification & Authentication | Mostly clean (entropy + TTL + one-shot + rate limit). Concerns: H1 (CSRF), H8 (dual LoginManager). |
| OWASP A08 — Data integrity | Webhook signature verified. Order records snapshot price/SKU server-side. |
| OWASP A09 — Logging & monitoring | EmailLog and SquareWebhookEvent are persisted. No admin-action audit trail for refunds/product CRUD (M7). |
| OWASP A10 — SSRF | No outbound HTTP based on user input. Square SDK uses pinned environment URL. Clean. |

## Findings by severity

### CRITICAL

(none)

### HIGH

- **H1. CSRF protection disabled on auth, cart, and checkout endpoints.** `solex/__init__.py:39-43` exempts five blueprints. `/checkout/submit` is the most material — a cross-site POST from a malicious page can trigger a Square charge against a logged-in customer with a stored card.
- **H2. `SESSION_COOKIE_SECURE` not set.** Neither `BaseConfig` nor `ProdConfig` set it. Session cookies will be transmitted over plaintext HTTP if the deployment ever serves it (or during a TLS-stripped MITM).
- **H3. Magic-link `_external=True` without Host allowlist.** Both `account_auth.request_magic` and `admin_auth.request_magic` build the link from the request's Host header. No `SERVER_NAME`, no `TRUSTED_HOSTS`, no `ProxyFix`. Host header injection → phishing email with attacker-controlled domain → token leaks.
- **H4. No security response headers.** No CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy. Flask-Talisman not installed. With Square Web Payments SDK loading cross-origin iframes, any future XSS is unbounded.
- **H5. Dockerfile runs as root.** `devops/Dockerfile` has no `USER` directive; gunicorn runs as `root` inside the container. Container escape → host privilege.
- **H6. Vulnerable production dependencies.** Flask 3.0.3 (CVE-2026-27205, missing Vary: Cookie), Jinja2 3.1.4 (three sandbox-escape CVEs — Solex doesn't use the sandbox so impact is informational, but pin should advance), python-dotenv 1.0.1 (CVE-2026-28684, only triggered by `set_key()` which Solex doesn't call).

### MEDIUM

- **M1. Square access token in plaintext env file.** Sandbox-scoped, but should move to secrets manager before partner access touches anything sensitive.
- **M2. Webhook signature uses `request.url`.** Reverse-proxy hosting could break verification or, with a misconfigured `X-Forwarded-*`, allow URL-portion forgery. Pin the public webhook URL via config.
- **M3. No webhook timestamp/replay guard beyond `square_event_id` dedupe.** Captured-and-replayed brand-new event hits the dispatcher once. Add `created_at` window check.
- **M4. No rate limit on `/checkout/submit`.** Lets attacker burn Square API budget and triggers payment side effects from cross-site posts (compounded by H1).
- **M5. Checkout JSON payload has no schema validation.** Raw dict access; missing keys → 500. Use a Pydantic model on the boundary.
- **M6. Admin refund amount unbounded.** No clamp to `[0, order.total_cents - already_refunded]`. Square will reject most over-refunds, but local invariant is weak.
- **M7. No admin-action audit log on refunds and product CRUD.** Inventory adjustments are logged with `admin_user_id`; refunds and catalog mutations aren't.
- **M8 (was H8). Dual `LoginManager` registration overwrites `app.login_manager`.** Customer manager wins; admin auth survives only because `admin_required` reads the session directly. Single shared session cookie with no admin/customer separation. Risky if `SECRET_KEY` ever leaks (token forgery yields admin access). Recommend either separate session cookies or a unified user model.

### LOW

- **L1. Cart endpoints unbounded.** Valkey memory pressure path only.
- **L2. Cart `qty` not capped per line.** Cap at e.g. 99.
- **L3. Inventory `delta` not bounded.** Admin-only, typo risk.
- **L4. Magic-link audience asserted with `assert` statement.** Stripped under `python -O`. Replace with `if audience not in (...): raise ValueError`.
- **L5. `WTF_CSRF_TIME_LIMIT = None`.** Token valid for the full session lifetime (7 days). Once H1 is fixed, tighten to 24h.
- **L6. `secrets.token_urlsafe(16)` for `Order.public_token`.** 128 bits — fine. Note that the `/order/<token>` confirmation route is **unauthenticated** and discloses customer name, address, and items to anyone with the token. Ensure tokens are not logged in proxy access logs or email subject lines.
- **L7. `try/except: pass` patterns** at six sites. All appear intentional but should carry an inline comment explaining why so future readers don't strip the safety.

## Recommended fixes (prioritized)

Order is partner-window-blocking → infrastructure → polish.

1. **(H1)** Re-enable CSRF on `cart`, `checkout`, `admin_auth`, `account_auth`. Move forms to `flask-wtf` and pass tokens via `X-CSRFToken` header from JS for the JSON endpoints. Keep `api` exempt (webhook is HMAC-verified, not session-authenticated).
2. **(H2)** Add `SESSION_COOKIE_SECURE = True` and `REMEMBER_COOKIE_SECURE = True` to `ProdConfig`.
3. **(H3)** Add `SERVER_NAME = os.environ["SOLEX_PUBLIC_HOST"]` to `ProdConfig` (and `PREFERRED_URL_SCHEME = "https"`). Mount `werkzeug.middleware.proxy_fix.ProxyFix` if behind a reverse proxy. Validate `request.host` against an allowlist on the magic-link issuance route as a belt-and-braces check.
4. **(H4)** Install Flask-Talisman (or write an `@after_request` header injector). Minimum: HSTS (max-age=31536000), CSP allowing Square's domains, X-Frame-Options DENY, X-Content-Type-Options nosniff, Referrer-Policy strict-origin-when-cross-origin.
5. **(H5)** Add `RUN useradd -m -u 1000 solex && chown -R solex /app` + `USER solex` to `devops/Dockerfile` before `CMD`.
6. **(H6)** Bump `Flask>=3.1.3`, `Jinja2>=3.1.6`, `python-dotenv>=1.2.2`, `Pillow>=12.2.0`, `pytest>=9.0.3`. Bump `psycopg[binary]` to a 3.14-compatible release while you're in there. **Get user approval before changing requirements** (per the platform rule on dep changes).
7. **(M8)** Either (a) collapse to a single `LoginManager` and discriminate user type via session key, or (b) split admin auth onto a separate cookie name. Document the chosen path in `Solex/CLAUDE.md` and Brain wiki.
8. **(M2, M3)** Pin webhook URL via `SQUARE_PUBLIC_WEBHOOK_URL` config; pass it to `verify_webhook_signature` instead of `request.url`. Reject events with `created_at` older than 5 minutes.
9. **(M4)** Add `@limiter.limit("20 per minute; 5 per second")` to `/checkout/submit`.
10. **(M5)** Validate the checkout JSON with a Pydantic model.
11. **(M6)** Clamp refund amount to `[1, order.total_cents - already_refunded_cents]`.
12. **(M7)** Add `issued_by_admin_id` to `Refund` and `created_by_admin_id` / `updated_by_admin_id` to `Product` (or write to an `AdminAuditLog` table).
13. **(M1)** Move Square access token to a secrets manager when production infra lands. Sandbox can stay in `.env`.
14. **(L1-L5)** Sweep at the end of the cleanup branch.
15. **(Bandit findings)** Replace asserts with explicit raises; comment intentional `try/except: pass` blocks.

## Out of scope / deferred

- **Production deployment hardening.** TLS termination, ProxyFix configuration, Cloudflare WAF rules — handled when the production infra is set up (per `project_production_infra` memory).
- **Square OAuth.** Currently static sandbox token. When/if Solex grows merchant-onboarding (it isn't planned to in the near term — Solex is a single-merchant storefront), revisit OAuth state, callback CSRF, token-at-rest encryption.
- **Email content pen testing.** Did not exhaustively review email template rendering for HTML injection paths via product names / customer names. Templates are server-rendered with autoescape on (default Jinja2), so impact should be limited.
- **Subscription endpoint authorization.** `/account/subscriptions/*/cancel` is gated by `current_user.id` ownership check, but `pause`/`resume` require `SOLEX_FLAG_SUB_SELFSERVE=true` — currently false. When that flag flips, re-audit.
- **Static asset/CDN.** `/static` is served by Flask in dev. No issue, but production should serve via reverse proxy.
- **`gitleaks` re-run.** Audit instructions referenced an existing run at `docs/audit-2026-04-23/security-tool-output/gitleaks.json` — that file does not exist in the audit directory. Recommend platform-wide `gitleaks detect --source /Users/gclyle/GrowDirect` before partner access.
- **Dependency-tree audit.** pip-audit ran with `--no-deps` because the pinned `psycopg[binary]==3.2.3` couldn't be resolved on Python 3.14. Transitive deps not scanned. Re-run inside the project venv (Python 3.12) for a complete picture.
