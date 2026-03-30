---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Work Order B-079: Blueprint Registration Cleanup
**Created:** March 1, 2026
**Source:** Full Codebase Code Review (ALX)
**Severity:** CRITICAL
**Gates:** Clean app startup
**Owner:** Jeremy
**QA:** Jim
**Mode:** DISPATCH

---

## Objective

Resolve the duplicate blueprint registration conflict that prevents clean Flask startup. Two competing systems exist. Pick one, kill the other.

## Background

**The problem:** `canary/blueprints/__init__.py` registers old stub blueprints (empty/placeholder). `canary/blueprints/registry.py` registers the new "wired" blueprints (real implementations). Both try to register blueprints with the same names (e.g., `merchants_bp`). Flask raises `ValueError: the name 'merchants' is already registered`.

## Deliverables

### 1. Keep registry.py, retire __init__.py

**Acceptance criteria:**
- [ ] `canary/blueprints/__init__.py` no longer registers any blueprints (keep as empty `__init__` or remove registration logic)
- [ ] `canary/blueprints/registry.py` is the SOLE registration system
- [ ] App factory calls only `registry.register_blueprints(app)`
- [ ] Verify: `python -c "from canary import create_app; app = create_app()"` succeeds without ValueError

### 2. Delete Root models.py Shadow (C-01 / B-016)

**File:** `Canary/models.py` (root level)

This file uses legacy SQLAlchemy 1.x patterns and shadows the `canary/models/` package. Confirmed tech debt from B-016.

**Acceptance criteria:**
- [ ] `Canary/models.py` deleted
- [ ] No import references to root `models.py` remain in any file
- [ ] All imports point to `canary.models.*` subpackages
- [ ] Grep confirms: `grep -r "from models import" Canary/` returns zero hits
- [ ] Grep confirms: `grep -r "import models" Canary/` returns zero hits (excluding `canary.models`)

### 3. Verify Endpoint Routing

After cleanup, verify all wired blueprints are reachable:

**Acceptance criteria:**
- [ ] `GET /health/liveness` returns 200
- [ ] `GET /health/readiness` returns 200
- [ ] `GET /merchants/` returns 200 (with auth)
- [ ] `GET /locations/` returns 200 (with auth)
- [ ] `POST /webhooks/square` returns 200 (with valid HMAC)
- [ ] All 9 frontend routes at :5050 still render

## Estimated Effort
~2 hours Jeremy + 1 hour Jim QA

## Routing
- Jeremy executes cleanup
- Jim re-runs full route matrix after changes
- Eva tracks as sprint 6 gate item

---
*Dispatched by ALX | Code Review Session | March 1, 2026*
