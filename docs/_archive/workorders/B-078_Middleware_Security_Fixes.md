---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Work Order B-078: Middleware Security Fixes
**Created:** March 1, 2026
**Source:** Full Codebase Code Review (ALX)
**Severity:** CRITICAL
**Gates:** B-064 (Production Heartbeat)
**Owner:** Jeremy
**QA:** Jim
**Mode:** DISPATCH

---

## Objective

Fix all broken middleware so that webhook validation and JWT authentication actually work. Without this, production heartbeat (B-064) cannot proceed.

## Deliverables

### 1. HMAC Webhook Validation (C-02, H-09)
**File:** `canary/middleware/hmac_verify.py`
**Also fix:** Missing `functools.wraps` import (C-04)

**What's wrong:**
- Computes hex digest but Square sends Base64-encoded HMAC signatures
- Uses `==` comparison instead of `hmac.compare_digest()` (timing attack)
- Missing `from functools import wraps`

**Reference implementation:** `canary/services/tsp/validators/square.py` already has the correct pattern.

**Acceptance criteria:**
- [ ] HMAC computed as Base64 (matching Square's format)
- [ ] `hmac.compare_digest()` used for constant-time comparison
- [ ] `functools.wraps` imported and decorator works
- [ ] Test: mock Square webhook with known signature validates correctly
- [ ] Test: tampered payload rejected

### 2. JWT Authentication (C-03, H-06)
**File:** `canary/middleware/jwt_auth.py`

**What's wrong:**
- Calls `jwt.get_unverified_json()` which does not exist in PyJWT
- JWKS cache has no thread safety (race condition on concurrent requests)
- No error handling for missing kid in JWKS response

**Acceptance criteria:**
- [ ] JWKS fetched via `urllib.request.urlopen` + `json.loads`
- [ ] Thread-safe JWKS cache (use `threading.Lock`)
- [ ] Graceful error when kid not found in JWKS
- [ ] Cache TTL configurable via env var (default 300s)
- [ ] Test: valid JWT passes, expired JWT rejected, unknown kid rejected

### 3. Missing Imports (C-04, C-09, H-07)
**Files:**
- `canary/middleware/hmac_verify.py` — `from functools import wraps`
- `canary/blueprints/square_oauth_wired.py` — `import requests`, `from datetime import datetime, timedelta`
- `canary/services/notification_service.py` — `import pytz`

**Acceptance criteria:**
- [ ] All three files import correctly
- [ ] No `NameError` on any decorated route or service call
- [ ] `python -c "from canary.middleware.hmac_verify import *"` succeeds
- [ ] `python -c "from canary.blueprints.square_oauth_wired import *"` succeeds
- [ ] `python -c "from canary.services.notification_service import *"` succeeds

## Estimated Effort
~4 hours Jeremy + 2 hours Jim QA

## Routing
- Jeremy builds all three items
- Jim adds middleware validation to UAT checklist (B-070)
- ALX confirms gate clearance before B-064 proceeds

---
*Dispatched by ALX | Code Review Session | March 1, 2026*
