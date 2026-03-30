---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Work Order B-080: Security Hardening Pass
**Created:** March 1, 2026
**Source:** Full Codebase Code Review (ALX)
**Severity:** HIGH
**Gates:** Production readiness
**Owner:** Jeremy (build) + Jim (QA) + Syd (review token storage policy)
**Mode:** DISPATCH

---

## Objective

Close all security gaps identified in code review that would expose the application to attack in production. Grouped by priority.

## Priority 1: Fix This Week (Before B-064)

### 1.1 SQL Injection in Audit Logger (C-06)
**File:** `canary/audit/logger.py` (lines ~181, ~261)

**What's wrong:** ORDER BY clause built via f-string interpolation of user input.

**Fix:** Whitelist order parameter to `{'ASC', 'DESC'}` only. Default to DESC.

**Acceptance criteria:**
- [ ] `order` parameter validated against whitelist before use in query
- [ ] Test: `order=ASC; DROP TABLE audit_log; --` is rejected
- [ ] Same fix applied to `search_audit_log()` method

### 1.2 Hardcoded Secrets Removal (C-07)
**Files:**
- `wsgi_b075.py` line 48: `SECRET_KEY = "b075-demo-key-not-for-production"`
- `canary/blueprints/square_oauth.py`: hardcoded `client_id=stub_app_id`
- `canary/blueprints/auth.py`: fake JWT tokens in stub responses

**Fix:** All secrets from environment variables. Stub responses clearly marked as dev-only with env check.

**Acceptance criteria:**
- [ ] `SECRET_KEY` sourced from `os.getenv('SECRET_KEY')` with no default in production
- [ ] OAuth client_id from env var
- [ ] Stub auth responses gated behind `CANARY_ENV != 'production'`
- [ ] Grep confirms: no hardcoded tokens, keys, or passwords in Python files

### 1.3 Config Validation at Startup (C-08)
**File:** `canary/config.py` + app factory

**What's wrong:** `ProductionConfig.validate()` exists but is never called.

**Fix:** Call validation in app factory when `CANARY_ENV=production`.

**Acceptance criteria:**
- [ ] App factory calls `config.validate()` during startup
- [ ] Missing `SECRET_KEY` in production raises `RuntimeError` before app starts
- [ ] Missing database URLs in production raises `RuntimeError`

### 1.4 AlertHistory Tenant Isolation (C-11)
**File:** `canary/models/app/detection.py`

**What's wrong:** AlertHistory model missing TenantMixin. Cross-tenant data exposure in multi-tenant queries.

**Fix:** Add TenantMixin to AlertHistory class.

**Acceptance criteria:**
- [ ] `AlertHistory` inherits from `TenantMixin`
- [ ] `merchant_id` column present with proper FK
- [ ] Row-level security applies to AlertHistory queries

## Priority 2: Sprint 6 Completion

### 2.1 Rate Limiting on Auth (H-11)
**File:** `canary/blueprints/auth.py`

**Fix:** Add `flask-limiter` with 5 attempts/minute/IP on login endpoint.

**Acceptance criteria:**
- [ ] `flask-limiter` in requirements
- [ ] Login endpoint: 5/minute per IP
- [ ] OAuth endpoints: 10/minute per IP
- [ ] 429 response returned with retry-after header

### 2.2 CSRF Protection (H-12)
**Scope:** All state-changing POST endpoints except webhook receivers.

**Fix:** Add Flask-WTF CSRF protection. Exempt `/webhooks/*` endpoints.

**Acceptance criteria:**
- [ ] CSRF token required on: settings update, OAuth disconnect, threshold changes
- [ ] Webhook endpoints exempt (they use HMAC validation)
- [ ] Frontend templates include CSRF tokens in forms

### 2.3 Input Validation (H-13)
**File:** `canary/blueprints/merchants_wired.py`

**What's wrong:** `setattr(merchant, key, value)` accepts any value without validation.

**Fix:** Validate field types and ranges before applying.

**Acceptance criteria:**
- [ ] `currency` validated against ISO 4217 whitelist
- [ ] `subscription_tier` validated against known tiers
- [ ] `merchant_name` max length enforced (255 chars)
- [ ] Invalid values return 400 with descriptive error

### 2.4 Pagination Bounds (H-14)
**Scope:** All list endpoints.

**Fix:** Enforce `page >= 1, page <= 10000, limit >= 1, limit <= 100`.

**Acceptance criteria:**
- [ ] `limit=999999` returns 400 or is clamped to 100
- [ ] Negative page values rejected
- [ ] Applied consistently across alerts, merchants, locations, employees endpoints

### 2.5 Bare Exception Cleanup (C-10)
**Scope:** All services.

**What's wrong:** `except Exception` throughout swallows everything including `MemoryError`, `SystemExit`.

**Fix:** Catch specific exceptions. Let system errors propagate. Log with traceback.

**Acceptance criteria:**
- [ ] No bare `except Exception` in critical paths
- [ ] Each catch block specifies expected exception types
- [ ] All caught exceptions logged with `logger.exception()`

## Priority 3: Pre-Production (Syd Review Required)

### 3.1 Token Encryption (M-12)
**File:** `canary/blueprints/square_oauth_wired.py` + `canary/services/square_oauth.py`

**What's wrong:** Square OAuth tokens stored as plaintext in database. DB compromise = all merchant API keys.

**Fix:** Encrypt tokens with `cryptography.fernet` before storage, decrypt on retrieval.

**Routing:** Syd to advise on encryption key management policy. Jeremy to implement. Connects to B-074 (Vault).

**Acceptance criteria:**
- [ ] Tokens encrypted at rest using Fernet symmetric encryption
- [ ] Encryption key from Vault (B-074) or env var as interim
- [ ] Existing plaintext tokens migrated (one-time migration script)
- [ ] Syd sign-off on key management approach

### 3.2 Financial Column Precision (H-03)
**Scope:** All `Numeric` columns in sales models.

**What's wrong:** Missing `asdecimal=True` causes financial values to lose precision via float conversion.

**Fix:** Add `asdecimal=True` to all `Numeric(12,2)` and `Numeric(10,4)` columns.

**Acceptance criteria:**
- [ ] All financial columns have `asdecimal=True`
- [ ] Python receives `Decimal` objects, not `float`
- [ ] No existing data migration required (storage is already precise, only Python representation changes)

## Estimated Total Effort
- Priority 1: ~4 hours Jeremy
- Priority 2: ~12 hours Jeremy + 4 hours Jim
- Priority 3: ~4 hours Jeremy + 1 hour Syd review

## Routing
- Jeremy builds all items
- Jim QA validates each priority level before next begins
- Syd reviews 3.1 (token encryption policy) before implementation
- Eva tracks as sprint 6 delivery item
- Tom reviews if any schema changes are needed (3.2 may require migration review)

---
*Dispatched by ALX | Code Review Session | March 1, 2026*
