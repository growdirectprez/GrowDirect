---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# WORK ORDER: B-023 — Fix Blueprint Model Imports
**From:** ALX  
**To:** Jeremy (Code Tab)  
**Date:** February 24, 2026  
**Priority:** 🔴 HIGHEST — clears ~25 of 43 remaining test failures  
**Estimated effort:** 5 minutes

---

## Problem

Three blueprint files use `from .models import ...` — a relative import that looks for `canary/blueprints/models.py`, which doesn't exist. The models live in `canary.models` (the package at `canary/models/__init__.py`). This causes `registry.py` to log `"No module named 'canary.blueprints.models'"` and skip the Merchants, Locations, and Employees blueprints entirely.

## The Fix — 3 lines changed in 3 files

### File 1: `canary/blueprints/merchants_wired.py`
Line 4 — change:
```python
from .models import Merchant, MerchantSettings
```
to:
```python
from canary.models import Merchant, MerchantSettings
```

### File 2: `canary/blueprints/locations_wired.py`
Line 4 — change:
```python
from .models import Location, DailyMetrics
```
to:
```python
from canary.models import Location, DailyMetrics
```

### File 3: `canary/blueprints/employees_wired.py`
Line 4 — change:
```python
from .models import Employee, Transaction, Alert, EntityRiskScore
```
to:
```python
from canary.models import Employee, Transaction, Alert, EntityRiskScore
```

## No other files are affected
All other `*_wired.py` files (`fox_wired`, `alerts_wired`, `chirp_wired`, `companion_wired`, `square_oauth_wired`, `webhooks_wired`) already use absolute imports. Only these three have the bug.

## Verification

After making the changes, run:
```bash
cd /Users/geofflyle/GrowDirect/Canary
python -m pytest tests/ -x -q 2>&1 | tail -20
```

Expected: test count jumps from 498 pass toward 520+ as blueprint_wiring, model_coverage, scaffold, and smoke_routes tests start passing.

## What this unblocks
- `test_blueprint_wiring.py` — 7 tests
- `test_model_coverage.py` — 14 tests  
- `test_scaffold.py` — 3 tests
- `test_smoke_routes.py` — 1 test
- Total: ~25 of the 43 remaining failures
