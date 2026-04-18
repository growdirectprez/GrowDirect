# Platform Security Hardening — Implementation Plan

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Address 30 security audit findings across shared infrastructure, Canary, and Cove — prioritized by blast radius and exploitability.

**Architecture:** Three independent workstreams (infra, Canary, Cove) that can execute in parallel. Infra tasks land first because app changes depend on them (Valkey auth, localhost binding, database roles). Within each workstream, tasks are ordered by severity: Critical first, then Important, then Minor.

**Tech Stack:** Docker Compose, PostgreSQL 17, Valkey 8, Flask 3, Python 3.12

---

## Chunk 1: Shared Infrastructure Hardening

### Task 1: Bind all ports to localhost only

**Files:**
- Modify: `devops/docker-compose.yml:33-34,48-49,67-68,84-85`

- [ ] **Step 1: Change all port bindings to 127.0.0.1**

```yaml
# postgres (line 34)
    ports:
      - "127.0.0.1:5432:5432"

# valkey (line 49)
    ports:
      - "127.0.0.1:6379:6379"

# pgadmin (line 68)
    ports:
      - "127.0.0.1:5050:80"

# ollama (line 85)
    ports:
      - "127.0.0.1:11434:11434"
```

- [ ] **Step 2: Also bind Canary Flask to localhost**

In `Canary/devops/docker-compose.localhost.yml` line 78, change:
```yaml
      - "5001:5001"
```
to:
```yaml
      - "127.0.0.1:5001:5001"
```

- [ ] **Step 3: Verify compose parses correctly**

```bash
cd ~/GrowDirect/devops && docker compose config --quiet
cd ~/GrowDirect/Canary/devops && docker compose -f docker-compose.localhost.yml config --quiet
```

Expected: Both exit 0, no errors

- [ ] **Step 4: Commit**

```bash
git add devops/docker-compose.yml Canary/devops/docker-compose.localhost.yml
git commit -m "security: bind all shared infra and app ports to localhost only"
```

---

### Task 2: Add Valkey authentication

**Files:**
- Modify: `devops/docker-compose.yml:45-56`
- Modify: `devops/README.md` (connection settings section)

- [ ] **Step 1: Add requirepass to Valkey service**

In `devops/docker-compose.yml`, add a `command` directive to the valkey service:

```yaml
  valkey:
    image: valkey/valkey:8-alpine
    container_name: growdirect_valkey
    command: ["valkey-server", "--requirepass", "valkey_dev"]
    ports:
      - "127.0.0.1:6379:6379"
    volumes:
      - valkey_data:/data
    healthcheck:
      test: ["CMD", "valkey-cli", "-a", "valkey_dev", "ping"]
      interval: 5s
      retries: 5
    restart: unless-stopped
```

- [ ] **Step 2: Update README with authenticated connection string**

In `devops/README.md`, update the Valkey connection format to:

```
VALKEY_URL=redis://:valkey_dev@growdirect_valkey:6379/<db_number>
```

- [ ] **Step 3: Update ALL Canary VALKEY_URL references**

In `Canary/.env`, update VALKEY_URL to include the password (this is a local-only change, not committed):

```
VALKEY_URL=redis://:valkey_dev@growdirect_valkey:6379/0
```

In `Canary/devops/docker-compose.localhost.yml`, update ALL 5 occurrences of VALKEY_URL. Each one changes from `redis://growdirect_valkey:6379/0` to `redis://:valkey_dev@growdirect_valkey:6379/0`:

```
Line 102:  VALKEY_URL: redis://:valkey_dev@growdirect_valkey:6379/0
Line 245:  VALKEY_URL: redis://:valkey_dev@growdirect_valkey:6379/0
Line 275:  VALKEY_URL: redis://:valkey_dev@growdirect_valkey:6379/0
Line 306:  VALKEY_URL: redis://:valkey_dev@growdirect_valkey:6379/0
Line 336:  VALKEY_URL: redis://:valkey_dev@growdirect_valkey:6379/0
```

In `Canary/devops/docker-compose.qa.yml`, update ALL 5 occurrences similarly:

```
Line 55:   VALKEY_URL: redis://:valkey_dev@growdirect_valkey:6379/0
Line 124:  VALKEY_URL: redis://:valkey_dev@growdirect_valkey:6379/0
Line 145:  VALKEY_URL: redis://:valkey_dev@growdirect_valkey:6379/0
Line 167:  VALKEY_URL: redis://:valkey_dev@growdirect_valkey:6379/0
Line 188:  VALKEY_URL: redis://:valkey_dev@growdirect_valkey:6379/0
```

Use find-and-replace: `redis://growdirect_valkey:6379/0` → `redis://:valkey_dev@growdirect_valkey:6379/0` across both files.

- [ ] **Step 4: Update Cove VALKEY_URL references**

In `Cove/.env`, update (local-only, not committed):

```
VALKEY_URL=redis://:valkey_dev@growdirect_valkey:6379/1
```

In `Cove/devops/docker-compose.yml` line 16:

```yaml
      VALKEY_URL: redis://:valkey_dev@growdirect_valkey:6379/1
```

- [ ] **Step 5: Verify all compose files parse correctly**

```bash
cd ~/GrowDirect/devops && docker compose config --quiet
cd ~/GrowDirect/Canary/devops && docker compose -f docker-compose.localhost.yml config --quiet
cd ~/GrowDirect/Cove/devops && docker compose config --quiet
```

Expected: All exit 0

- [ ] **Step 6: Commit**

Note: `.env` files are gitignored — only compose files are committed. Update `.env` files manually on each dev machine.

```bash
git add devops/docker-compose.yml devops/README.md Canary/devops/docker-compose.localhost.yml Canary/devops/docker-compose.qa.yml Cove/devops/docker-compose.yml
git commit -m "security: add Valkey authentication across shared infra and apps"
```

---

### Task 3: Make CREATE DATABASE idempotent

**Files:**
- Modify: `devops/init-db/01-create-databases.sql:1-10`

- [ ] **Step 1: Wrap CREATE DATABASE in idempotent PL/pgSQL blocks**

Replace lines 5-10 with:

```sql
-- Create app databases (idempotent — safe to re-run)
SELECT 'CREATE DATABASE canary OWNER growdirect'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'canary')\gexec

SELECT 'CREATE DATABASE canary_test OWNER growdirect'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'canary_test')\gexec

SELECT 'CREATE DATABASE canary_memory OWNER growdirect'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'canary_memory')\gexec

SELECT 'CREATE DATABASE cove OWNER growdirect'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'cove')\gexec

SELECT 'CREATE DATABASE cove_test OWNER growdirect'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'cove_test')\gexec
```

The `\gexec` pattern runs the SELECT output as a command. If the database exists, the SELECT returns no rows and nothing executes.

- [ ] **Step 2: Update the comment on line 2 to remove the misleading claim**

Change line 2 from:
```sql
-- Runs once on first postgres container boot (idempotent via IF NOT EXISTS)
```
to:
```sql
-- Runs once on first postgres container boot (idempotent — safe to re-run)
```

- [ ] **Step 3: Commit**

```bash
git add devops/init-db/01-create-databases.sql
git commit -m "security: make CREATE DATABASE statements idempotent for recovery"
```

---

### Task 4: Enable pgAdmin master password

**Files:**
- Modify: `devops/docker-compose.yml:65-66`

- [ ] **Step 1: Enable master password requirement**

Change line 66 from:
```yaml
      PGADMIN_CONFIG_MASTER_PASSWORD_REQUIRED: "False"
```
to:
```yaml
      PGADMIN_CONFIG_MASTER_PASSWORD_REQUIRED: "True"
```

- [ ] **Step 2: Commit**

```bash
git add devops/docker-compose.yml
git commit -m "security: require pgAdmin master password"
```

---

### Task 5: Add Cove database extensions

**Files:**
- Modify: `devops/init-db/01-create-databases.sql:133-137`

- [ ] **Step 1: Add missing extensions to cove and cove_test**

Replace lines 133-137 with:

```sql
\c cove
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

\c cove_test
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

- [ ] **Step 2: Commit**

```bash
git add devops/init-db/01-create-databases.sql
git commit -m "fix: add missing pgcrypto and uuid-ossp extensions to Cove databases"
```

---

### Task 6: Fix incomplete GRANT chains for Canary roles

**Files:**
- Modify: `devops/init-db/01-create-databases.sql:51-62,130-131`

- [ ] **Step 1: Add table-level grants and DEFAULT PRIVILEGES for canary_app**

After line 55 (`GRANT USAGE ON SCHEMA public TO canary_app;`), add:

```sql
-- canary_app: full DML on app and metrics schemas
ALTER DEFAULT PRIVILEGES FOR ROLE growdirect IN SCHEMA app
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO canary_app;
ALTER DEFAULT PRIVILEGES FOR ROLE growdirect IN SCHEMA metrics
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO canary_app;
-- canary_app: read-only on sales
ALTER DEFAULT PRIVILEGES FOR ROLE growdirect IN SCHEMA sales
  GRANT SELECT ON TABLES TO canary_app;
ALTER DEFAULT PRIVILEGES FOR ROLE growdirect IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO canary_app;
```

- [ ] **Step 2: Add table-level grants and DEFAULT PRIVILEGES for canary_tsp**

After line 62 (`ALTER ROLE canary_tsp SET search_path TO sales, app, public;`), add:

```sql
-- canary_tsp: full DML on sales
ALTER DEFAULT PRIVILEGES FOR ROLE growdirect IN SCHEMA sales
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO canary_tsp;
-- canary_tsp: read-only on app
ALTER DEFAULT PRIVILEGES FOR ROLE growdirect IN SCHEMA app
  GRANT SELECT ON TABLES TO canary_tsp;
```

- [ ] **Step 3: Add USAGE grant in canary_memory for canary_app**

After line 131, add:

```sql
GRANT USAGE ON SCHEMA public TO canary_app;
ALTER DEFAULT PRIVILEGES FOR ROLE growdirect IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO canary_app;
```

- [ ] **Step 4: Replicate grants in canary_test**

After the existing canary_test schema grants (line 77), add matching DEFAULT PRIVILEGES:

```sql
ALTER DEFAULT PRIVILEGES FOR ROLE growdirect IN SCHEMA app
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO canary_app;
ALTER DEFAULT PRIVILEGES FOR ROLE growdirect IN SCHEMA metrics
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO canary_app;
ALTER DEFAULT PRIVILEGES FOR ROLE growdirect IN SCHEMA sales
  GRANT SELECT ON TABLES TO canary_app;
ALTER DEFAULT PRIVILEGES FOR ROLE growdirect IN SCHEMA sales
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO canary_tsp;
ALTER DEFAULT PRIVILEGES FOR ROLE growdirect IN SCHEMA app
  GRANT SELECT ON TABLES TO canary_tsp;
```

- [ ] **Step 5: Commit**

```bash
git add devops/init-db/01-create-databases.sql
git commit -m "security: add table-level grants and DEFAULT PRIVILEGES for Canary roles"
```

---

### Task 7: Add Ollama healthcheck

**Files:**
- Modify: `devops/docker-compose.yml:81-88`

- [ ] **Step 1: Add healthcheck to Ollama service**

Add healthcheck block after `restart: unless-stopped` (line 88):

```yaml
  ollama:
    image: ollama/ollama
    container_name: growdirect_ollama
    ports:
      - "127.0.0.1:11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    healthcheck:
      test: ["CMD-SHELL", "curl -sf http://localhost:11434/api/tags || exit 1"]
      interval: 10s
      start_period: 30s
      retries: 5
    restart: unless-stopped
```

- [ ] **Step 2: Commit**

```bash
git add devops/docker-compose.yml
git commit -m "infra: add healthcheck to Ollama service"
```

---

### Task 8: Update README to include canary_memory database

**Files:**
- Modify: `devops/README.md` (databases table section)

- [ ] **Step 1: Add canary_memory to the databases table**

Add a row to the databases table:

```
| canary_memory | growdirect | ALX agent knowledge graph |
```

- [ ] **Step 2: Commit**

```bash
git add devops/README.md
git commit -m "docs: add canary_memory to README database table"
```

---

## Chunk 2: Canary Security Fixes

### Task 9: Fix JWT dev-mode bypass — validate with a dev secret

**Files:**
- Modify: `Canary/canary/middleware/jwt_auth.py:320-335`

- [ ] **Step 1: Replace open bypass with dev-secret validation**

Find and replace this exact block in `jwt_auth.py` (lines 320-335):

```python
            # Dev mode: accept any Bearer token, use env defaults
            # MCP tools (ALX, OWL) need this to function locally
            # SECURITY: Only allowed when CANARY_ENV is explicitly development
            canary_env = os.getenv('CANARY_ENV', 'development').lower()
            if canary_env == 'production':
                logger.warning("JWT dev mode blocked — CANARY_ENV is production")
                abort(401)
            g.user_id = "dev-user"
            g.roles = ["admin"]
            g.organization_id = os.getenv('CANARY_DEFAULT_ORG', 'org-growdirect-000000000001')
            dev_merchants = os.getenv('CANARY_DEFAULT_MERCHANTS', 'demo-sq-farmers-market-0001')
            # Resolve Square merchant IDs → internal UUIDs at boundary
            g.merchant_ids = [_resolve_merchant_uuid(m.strip()) for m in dev_merchants.split(',')]
            g.merchant_id = g.merchant_ids[0]

            return func(*args, **kwargs)
```

Replace with:

```python
            # Dev mode: validate Bearer token against a known dev secret
            # MCP tools (ALX, OWL) need this to function locally
            # SECURITY: Production always rejects; dev/test require matching secret
            canary_env = os.getenv('CANARY_ENV', 'development').lower()
            if canary_env == 'production':
                logger.warning("JWT validation not implemented for production — rejecting")
                abort(401)

            dev_secret = os.getenv('CANARY_DEV_JWT_SECRET')
            if not dev_secret:
                logger.error("CANARY_DEV_JWT_SECRET not set — cannot authenticate dev requests")
                abort(401)

            if token != dev_secret:
                logger.warning("JWT dev-mode auth failed — token does not match CANARY_DEV_JWT_SECRET")
                abort(401)

            g.user_id = "dev-user"
            g.roles = ["admin"]
            g.organization_id = os.getenv('CANARY_DEFAULT_ORG', 'org-growdirect-000000000001')
            dev_merchants = os.getenv('CANARY_DEFAULT_MERCHANTS', 'demo-sq-farmers-market-0001')
            # Resolve Square merchant IDs → internal UUIDs at boundary
            g.merchant_ids = [_resolve_merchant_uuid(m.strip()) for m in dev_merchants.split(',')]
            g.merchant_id = g.merchant_ids[0]

            return func(*args, **kwargs)
```

- [ ] **Step 2: Add CANARY_DEV_JWT_SECRET to Canary .env**

Generate a random secret and add to `Canary/.env`:

```bash
python3 -c "import secrets; print(f'CANARY_DEV_JWT_SECRET={secrets.token_hex(32)}')" >> ~/GrowDirect/Canary/.env
```

- [ ] **Step 3: Add CANARY_DEV_JWT_SECRET to all Canary docker-compose environment sections**

Add the same value to `Canary/devops/docker-compose.localhost.yml` and any other compose files in the `environment:` block.

- [ ] **Step 4: Add CANARY_DEV_JWT_SECRET to .env.test**

Add to `Canary/.env.test`:

```
CANARY_DEV_JWT_SECRET=test-jwt-secret-for-automated-tests
```

- [ ] **Step 5: Commit**

```bash
git add Canary/canary/middleware/jwt_auth.py Canary/.env.test
git commit -m "security: require dev JWT secret instead of accepting any Bearer token"
```

---

### Task 10: Add .env.test to .gitignore

**Files:**
- Modify: `Canary/.gitignore:15-17`

- [ ] **Step 1: Add .env.test to gitignore**

After line 17 (`.env.local`), add:

```
.env.test
```

- [ ] **Step 2: Remove .env.test from git tracking (if tracked)**

```bash
cd ~/GrowDirect/Canary && git ls-files --error-unmatch .env.test 2>/dev/null && git rm --cached .env.test || echo ".env.test not tracked, skipping"
```

- [ ] **Step 3: Create .env.test.template**

Create `Canary/.env.test.template` with placeholder values (no real secrets):

```
# Canary LP — Test Environment Variables Template
# Copy to .env.test and fill in values.

SQUARE_APPLICATION_ID=test-app-id
SQUARE_APPLICATION_SECRET=test-secret
SQUARE_ACCESS_TOKEN=test-token
SQUARE_ENVIRONMENT=sandbox
SECRET_KEY=<generate with: python3 -c "import secrets; print(secrets.token_hex(32))">
CANARY_DB_URL=postgresql://growdirect:growdirect_dev@localhost:5432/canary_test
CANARY_DEV_JWT_SECRET=<generate with: python3 -c "import secrets; print(secrets.token_hex(32))">
SQUARE_REDIRECT_URL=http://localhost:5001/oauth/callback
POLLING_ENABLED=0
POLLING_INTERVAL_SECONDS=10
CANARY_ENV=testing
FLASK_ENV=testing
```

- [ ] **Step 4: Commit**

```bash
git add Canary/.gitignore Canary/.env.test.template
git commit -m "security: remove .env.test from tracking, add template"
```

---

### Task 11: Change clear-session to POST only

**Files:**
- Modify: `Canary/canary/blueprints/auth.py:53`

- [ ] **Step 1: Change methods from GET to POST**

Change line 53 from:
```python
@auth_bp.route("/clear-session", methods=["GET"])
```
to:
```python
@auth_bp.route("/clear-session", methods=["POST"])
```

- [ ] **Step 2: Add CSRF exemption since this is a session reset**

Add `@csrf.exempt` before the function (same pattern as lines 63-64):

```python
@auth_bp.route("/clear-session", methods=["POST"])
@csrf.exempt
def clear_session():
```

Note: CSRF exemption is needed here because the user's session may be corrupted (that's why they're hitting this endpoint), and CSRF tokens are session-bound.

- [ ] **Step 3: Update any templates or JS that link to /clear-session**

Search for references to `/clear-session` or `clear-session` in templates and update from links to form posts:

```bash
grep -r "clear-session" ~/GrowDirect/Canary/templates/
```

If found as an `<a>` tag, replace with a `<form method="post" action="/auth/clear-session"><button>` pattern.

- [ ] **Step 4: Commit**

```bash
git add Canary/canary/blueprints/auth.py
git commit -m "security: change clear-session from GET to POST to prevent CSRF"
```

---

### Task 12: Add authentication to MCP manifest/tools and Owl personalities

**Files:**
- Modify: `Canary/canary/mcp/blueprint.py:62-68`
- Modify: `Canary/canary/blueprints/owl_api.py:257`

- [ ] **Step 1: Add @jwt_required to manifest and tools_list in blueprint.py**

Change lines 62-68 from:
```python
    @bp.route("/manifest", methods=["GET"])
    def manifest():
        return jsonify(registry.get_manifest())

    @bp.route("/tools", methods=["GET"])
    def tools_list():
        return jsonify({"tools": registry.list_tools()})
```
to:
```python
    @bp.route("/manifest", methods=["GET"])
    @jwt_required
    def manifest():
        return jsonify(registry.get_manifest())

    @bp.route("/tools", methods=["GET"])
    @jwt_required
    def tools_list():
        return jsonify({"tools": registry.list_tools()})
```

- [ ] **Step 2: Add @jwt_required to Owl personalities endpoint**

Change lines 257-258 from:
```python
@owl_api_bp.route("/personalities")
def personalities():
```
to:
```python
@owl_api_bp.route("/personalities")
@jwt_required
def personalities():
```

Ensure `jwt_required` is imported at the top of `owl_api.py`. Check existing imports — it's likely already imported since other routes use it.

- [ ] **Step 3: Commit**

```bash
git add Canary/canary/mcp/blueprint.py Canary/canary/blueprints/owl_api.py
git commit -m "security: add JWT auth to MCP discovery and Owl personalities endpoints"
```

---

### Task 13: Add rate limiting to MCP endpoints

**Files:**
- Modify: `Canary/canary/mcp/blueprint.py:55-60`

- [ ] **Step 1: Replace blanket exemption with per-route limits**

The challenge: `limiter` is imported inside a try/except because tests run without `canary.extensions`. We need to handle this gracefully.

Change the entire rate limiter block AND the route definitions. Replace lines 55-68 with:

```python
    # MCP endpoints are agent-to-agent — higher limit, not exempt
    try:
        from canary.extensions import limiter
        _has_limiter = True
    except ImportError:
        _has_limiter = False  # Extensions unavailable (unit tests outside Docker)

    def _limit(limit_string):
        """Apply rate limit decorator if limiter is available, otherwise no-op."""
        def decorator(f):
            if _has_limiter:
                return limiter.limit(limit_string)(f)
            return f
        return decorator

    @bp.route("/manifest", methods=["GET"])
    @jwt_required
    @_limit("100/hour")
    def manifest():
        return jsonify(registry.get_manifest())

    @bp.route("/tools", methods=["GET"])
    @jwt_required
    @_limit("100/hour")
    def tools_list():
        return jsonify({"tools": registry.list_tools()})
```

Also add `@_limit("1000/hour")` to the tool_invoke route (after `@jwt_required`):

```python
    @bp.route("/tools/<tool_name>", methods=["POST"])
    @jwt_required
    @_limit("1000/hour")
    def tool_invoke(tool_name):
```

- [ ] **Step 2: Commit**

```bash
git add Canary/canary/mcp/blueprint.py
git commit -m "security: add rate limits to MCP endpoints instead of blanket exemption"
```

---

### Task 14: Remove hardcoded SECRET_KEY from Canary compose

**Files:**
- Modify: `Canary/devops/docker-compose.localhost.yml:84`

- [ ] **Step 1: Remove the SECRET_KEY line from compose environment**

Delete line 84 (`SECRET_KEY: localhost-dev-key-not-for-production-use`) from the environment block. The key will come from `.env` via the `env_file` directive.

- [ ] **Step 2: Verify compose still parses**

Run: `cd ~/GrowDirect/Canary/devops && docker compose -f docker-compose.localhost.yml config --quiet`
Expected: Exit 0

- [ ] **Step 3: Commit**

```bash
git add Canary/devops/docker-compose.localhost.yml
git commit -m "security: remove hardcoded SECRET_KEY from compose, use .env only"
```

---

### Task 15: Tighten CSP — remove unsafe-eval

**Files:**
- Modify: `Canary/wsgi.py:131`

- [ ] **Step 1: Remove unsafe-eval from script-src**

Change line 131 from:
```python
            "script-src": "'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net",
```
to:
```python
            "script-src": "'self' 'unsafe-inline' https://cdn.jsdelivr.net",
```

Note: `unsafe-inline` is kept for now because removing it requires auditing all inline scripts and adding nonces. `unsafe-eval` is removed because it's rarely needed and is the higher-risk directive. If any JS breaks after this change, identify the specific library that needs `eval()` and add a more targeted exception.

- [ ] **Step 2: Test the app loads correctly**

Start the Canary app and verify no console errors related to CSP violations:

```bash
cd ~/GrowDirect/Canary/devops && docker compose -f docker-compose.localhost.yml up -d flask
docker logs canary_flask --tail 20
```

Check browser console for `Refused to evaluate a string as JavaScript` errors.

- [ ] **Step 3: Commit**

```bash
git add Canary/wsgi.py
git commit -m "security: remove unsafe-eval from CSP script-src"
```

---

### Task 16: Fix Dockerfile healthcheck to use python3

**Files:**
- Modify: `Canary/Dockerfile:20`

- [ ] **Step 1: Change python to python3**

Change line 20 from:
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5001/health')" || exit 1
```
to:
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:5001/health')" || exit 1
```

- [ ] **Step 2: Commit**

```bash
git add Canary/Dockerfile
git commit -m "fix: use python3 in Dockerfile healthcheck per platform standards"
```

---

## Chunk 3: Cove Security Fixes

### Task 17: Add file extension validation and auth to avatar upload/serve

**Files:**
- Modify: `Cove/cove/member/routes.py:104,155-160`

- [ ] **Step 1: Add extension validation to avatar upload**

After line 104 (`ext = os.path.splitext(avatar_file.filename)[1].lower()`), add validation:

```python
            ext = os.path.splitext(avatar_file.filename)[1].lower()
            allowed_avatar_ext = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
            if ext not in allowed_avatar_ext:
                flash("Avatar must be a PNG, JPG, GIF, or WebP image.", "error")
                return render_template("member/profile.html", form=form, profile=parcel_profile)
```

- [ ] **Step 2: Add @login_required to serve_avatar**

Change lines 155-160 from:
```python
@member_bp.route("/uploads/avatars/<filename>")
def serve_avatar(filename: str):
    avatar_dir = os.path.join(
        current_app.config.get("UPLOAD_FOLDER", "uploads"), "avatars"
    )
    return send_from_directory(avatar_dir, filename)
```
to:
```python
@member_bp.route("/uploads/avatars/<filename>")
@login_required
def serve_avatar(filename: str):
    avatar_dir = os.path.join(
        current_app.config.get("UPLOAD_FOLDER", "uploads"), "avatars"
    )
    return send_from_directory(avatar_dir, filename)
```

Ensure `login_required` is imported — check existing imports at top of file. It's likely already imported since other routes use it.

- [ ] **Step 3: Commit**

```bash
git add Cove/cove/member/routes.py
git commit -m "security: validate avatar extensions and require auth on serve endpoint"
```

---

### Task 18: Remove hardcoded secrets from Cove compose

**Files:**
- Modify: `Cove/devops/docker-compose.yml:12-13`

- [ ] **Step 1: Remove FLASK_DEBUG and SECRET_KEY from compose environment**

Remove lines 12-13:
```yaml
      FLASK_DEBUG: "1"
      SECRET_KEY: localhost-dev-key-not-for-production-use
```

The `FLASK_ENV: development` on line 11 is sufficient for Flask to enable debug mode via the config class. SECRET_KEY comes from `.env` via `env_file`.

- [ ] **Step 2: Verify compose still parses**

Run: `cd ~/GrowDirect/Cove/devops && docker compose config --quiet`
Expected: Exit 0

- [ ] **Step 3: Commit**

```bash
git add Cove/devops/docker-compose.yml
git commit -m "security: remove hardcoded FLASK_DEBUG and SECRET_KEY from Cove compose"
```

---

### Task 19: Fix StagingConfig to inherit ProdConfig security settings

**Files:**
- Modify: `Cove/cove/config.py:51-52`

- [ ] **Step 1: Make StagingConfig inherit from ProdConfig**

`StagingConfig` is currently defined at line 51 BEFORE `ProdConfig` at line 55. We need to swap them so `ProdConfig` is defined first.

**Step 1a: Move ProdConfig above StagingConfig.** The new ordering in config.py should be:

```python
class ProdConfig(BaseConfig):
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True


class StagingConfig(ProdConfig):
    """Staging inherits all production security settings."""
    pass
```

This means: delete the current `StagingConfig` block (lines 51-52), then insert it after `ProdConfig` (what was lines 55-60) with `ProdConfig` as the parent class.

- [ ] **Step 2: Commit**

```bash
git add Cove/cove/config.py
git commit -m "security: StagingConfig inherits ProdConfig cookie security settings"
```

---

### Task 20: Remove credentials from alembic.ini

**Files:**
- Modify: `Cove/alembic.ini:3`

- [ ] **Step 1: Replace hardcoded URL with placeholder**

Change line 3 from:
```ini
sqlalchemy.url = postgresql://growdirect:growdirect_dev@localhost:5432/cove
```
to:
```ini
sqlalchemy.url = driver://
```

The actual URL is loaded from `DATABASE_URL` environment variable by `migrations/env.py`. This line is only a fallback and should not contain real credentials.

- [ ] **Step 2: Verify Alembic still works**

Run from inside the container or with env set:
```bash
cd ~/GrowDirect/Cove && DATABASE_URL=postgresql://growdirect:growdirect_dev@localhost:5432/cove python3 -m alembic current
```

Expected: Shows current migration head, no errors about missing URL.

- [ ] **Step 3: Commit**

```bash
git add Cove/alembic.ini
git commit -m "security: remove hardcoded credentials from alembic.ini"
```

---

### Task 21: Bind Cove MailHog ports to localhost

**Files:**
- Modify: `Cove/devops/docker-compose.yml:41-43`

- [ ] **Step 1: Bind MailHog ports to localhost**

Change lines 41-43 from:
```yaml
    ports:
      - "1026:1025"
      - "8026:8025"
```
to:
```yaml
    ports:
      - "127.0.0.1:1026:1025"
      - "127.0.0.1:8026:8025"
```

- [ ] **Step 2: Also bind Cove Flask to localhost**

Change line 8-9 from:
```yaml
    ports:
      - "5002:5000"
```
to:
```yaml
    ports:
      - "127.0.0.1:5002:5000"
```

- [ ] **Step 3: Commit**

```bash
git add Cove/devops/docker-compose.yml
git commit -m "security: bind all Cove ports to localhost only"
```

---

### Task 22: Add security headers to Cove (flask-talisman)

**Files:**
- Modify: `Cove/cove/__init__.py` (app factory)
- Modify: `Cove/cove/extensions.py`
- Modify: `Cove/requirements.txt`

- [ ] **Step 1: Check if flask-talisman is in requirements.txt**

```bash
grep -i talisman ~/GrowDirect/Cove/requirements.txt
```

If not present, add `flask-talisman` to `Cove/requirements.txt`.

- [ ] **Step 2: Add talisman to extensions.py**

Add to `Cove/cove/extensions.py`:

```python
from flask_talisman import Talisman
talisman = Talisman()
```

- [ ] **Step 3: Initialize talisman in app factory**

In `Cove/cove/__init__.py`, first update the import line to include `talisman`:

```python
from cove.extensions import db, login_manager, mail, csrf, sess, talisman
```

Then after the other extension initializations, add:

```python
    talisman.init_app(
        app,
        force_https=app.config.get("SESSION_COOKIE_SECURE", False),
        session_cookie_secure=app.config.get("SESSION_COOKIE_SECURE", False),
        content_security_policy={
            "default-src": "'self'",
            "script-src": "'self' 'unsafe-inline'",
            "style-src": "'self' 'unsafe-inline'",
            "img-src": "'self' data:",
            "font-src": "'self'",
        },
        frame_options="DENY",
        x_content_type_options=True,
        strict_transport_security=app.config.get("SESSION_COOKIE_SECURE", False),
    )
```

Note: `unsafe-inline` for scripts and styles is a starting point. Audit and tighten in a follow-up.

- [ ] **Step 4: Rebuild Cove container if flask-talisman was added**

```bash
cd ~/GrowDirect/Cove/devops && docker compose build flask && docker compose up -d flask
```

- [ ] **Step 5: Commit**

```bash
git add Cove/requirements.txt Cove/cove/extensions.py Cove/cove/__init__.py
git commit -m "security: add flask-talisman for CSP and security headers"
```

---

### Task 23: Add rate limiting to Cove login endpoints

**Files:**
- Modify: `Cove/cove/extensions.py`
- Modify: `Cove/cove/auth/routes.py`
- Modify: `Cove/requirements.txt`

- [ ] **Step 1: Check if flask-limiter is in requirements.txt**

```bash
grep -i limiter ~/GrowDirect/Cove/requirements.txt
```

If not present, add `Flask-Limiter` to requirements.txt.

- [ ] **Step 2: Add limiter to extensions.py**

Add to `Cove/cove/extensions.py`:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
limiter = Limiter(key_func=get_remote_address)
```

- [ ] **Step 3: Initialize limiter in app factory**

In `Cove/cove/__init__.py`, add `limiter` to the import from `cove.extensions`, then after other extension inits:

```python
    limiter.init_app(app, storage_uri=app.config.get("VALKEY_URL", "memory://"))
```

- [ ] **Step 4: Add rate limits to auth routes**

In `Cove/cove/auth/routes.py`, import limiter and add decorators:

```python
from cove.extensions import limiter
```

Then add `@limiter.limit("5/minute")` to the login route. Note: In Cove, magic link generation happens inside the `/login` POST handler (lines 64-81 of `auth/routes.py`), not as a separate endpoint. So rate-limiting `/login` covers both password and magic link attempts:

```python
@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5/minute")
def login():
    ...
```

Also add `@limiter.limit("5/minute")` to the `/verify/<token>` route to prevent token brute-forcing.

- [ ] **Step 5: Rebuild if flask-limiter was added**

```bash
cd ~/GrowDirect/Cove/devops && docker compose build flask && docker compose up -d flask
```

- [ ] **Step 6: Commit**

```bash
git add Cove/requirements.txt Cove/cove/extensions.py Cove/cove/__init__.py Cove/cove/auth/routes.py
git commit -m "security: add rate limiting to Cove login and magic link endpoints"
```

---

## Post-Implementation Checklist

After all tasks are complete:

- [ ] Run `cd ~/GrowDirect/devops && docker compose config --quiet` to validate shared infra
- [ ] Run `cd ~/GrowDirect/Canary/devops && docker compose -f docker-compose.localhost.yml config --quiet` to validate Canary
- [ ] Run `cd ~/GrowDirect/Cove/devops && docker compose config --quiet` to validate Cove
- [ ] Restart shared infra: `cd ~/GrowDirect/devops && docker compose down && docker compose up -d`
- [ ] Restart Canary: `cd ~/GrowDirect/Canary/devops && docker compose down && docker compose up -d`
- [ ] Restart Cove: `cd ~/GrowDirect/Cove/devops && docker compose down && docker compose up -d`
- [ ] Verify Valkey requires auth: `docker exec growdirect_valkey valkey-cli ping` should return `NOAUTH` error
- [ ] Verify ports are localhost only: `docker port growdirect_postgres` should show `127.0.0.1:5432`
- [ ] Run Canary test suite: `cd ~/GrowDirect/Canary && python3 -m pytest tests/ -x`
- [ ] Run Cove test suite: `cd ~/GrowDirect/Cove && python3 -m pytest tests/ -x`

---

## Deferred Items (Not in This Plan)

These were identified in the audit but are lower priority or require separate planning:

| # | Issue | Why Deferred |
|---|-------|-------------|
| I3 | CSP unsafe-inline removal (Canary) | Requires full inline JS audit — separate plan |
| I3 | `growdirect` superuser → scoped roles for app connections | Requires app connection string changes across all environments — separate migration plan |
| C5 | Cove RLS bypass (`growdirect` → `cove_app` role) | Depends on I3 above + `has_voted()` redesign |
| M4 | Container resource limits | Dev convenience tradeoff — add when moving to production |
| M3 | Ollama non-root user | Requires custom Docker image — separate |
| S1-S5 | Infra suggestions (read_only, no-new-privileges, image pinning, .env pattern, override example) | Best practices, not security blockers |
| M6 | `datetime.utcnow()` → `datetime.now(timezone.utc)` (40+ Cove files) | Large refactor, no security impact |
