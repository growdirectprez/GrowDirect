---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Jeremy Session Prompt — B-067-B: Square Capability Explorer Backend
**Work Order:** B-067-B
**Date:** February 28, 2026
**Dispatched by:** ALX
**Priority:** HIGH
**Depends on:** Condor B-067-A capability map (**DELIVERED** — on disk)
**Pre-validated:** Jim QA PASSED B-067-C dashboard shell (`_ALX/WorkOrders/output/Jim/Jim_B067C_DashboardQA_Report.md`)
**Updated:** Feb 28 — ALX fixed 5 slug mismatches between registry and dashboard (merchant→merchants, cash_drawer_shifts→cash_drawers, timecards→labor, added invoices + subscriptions, removed devices + webhook_subscriptions)

---

## Mission

Build one Python module with one read-only function per Square API family. Build a Flask blueprint with one route. Qwen's dashboard calls your endpoint. Jeffe clicks a card and sees real sandbox data.

No unit tests. Square SDK is stable. Trust it, use it, ship it.

---

## Data Flow — Top Down

```
Square SDK v44 APIs (source of truth — what Square actually returns)
    ↓
square_capability_explorer.py (this module — one explore_ function per family)
    ↓
square_explorer_wired.py (Flask blueprint — /explore/<family>)
    ↓
square_explorer.html (dashboard — B-067-C, Jim QA PASSED)
    ↓
B-068 Foundation Layer (vocabulary, tokenization, locale packs — supports display labels)
```

**The dashboard is the contract.** Its 16 `data-family` slugs define the API. The Square SDK defines what data comes back. B-068's vocabulary layer (Token Registry v1.0, 178 tokens, 32 vocab-overridable) supports the labels and terminology the dashboard uses. Everything pushes down from Square's APIs through this pipe. If the old SDK had something, the v44 SDK still has it — Condor verified all 16 families against the cloned v44 repo.

---

## Read First

```
/Users/geofflyle/GrowDirect/Canary/square/square-python-sdk/README.md
/Users/geofflyle/GrowDirect/Canary/square/SQUARE_SCAN_NOTES.md
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Condor/B067_SquareCapabilityMap_v1.0.md
```

Wait for Condor's capability map before implementing — it has the exact SDK method names and sample calls.

---

## Build

### File 1: Explorer Module
```
/Users/geofflyle/GrowDirect/Canary/canary/services/square_capability_explorer.py
```

```python
"""
Square Capability Explorer
One read-only function per Square API family.
Sandbox only. All calls return structured dict.

Return schema:
{
    "api_family": str,       # e.g. "payments"
    "status": str,           # "ok" | "scope_not_granted" | "error" | "empty"
    "count": int,            # number of records returned
    "data": list | dict,     # the actual records (serializable)
    "sdk_call": str,         # the SDK method called, for display
    "error": str | None      # error message if status != "ok"
}

# SQUARE OPEN SOURCE
# SDK patterns from: /Users/geofflyle/GrowDirect/Canary/square/square-python-sdk/
"""

from square import Square
import os
import json

LIMIT = 10  # default page size for all list calls

def _client() -> Square:
    return Square(
        token=os.environ["SQUARE_ACCESS_TOKEN"],
        environment=os.environ.get("SQUARE_ENVIRONMENT", "sandbox"),
    )

def _ok(api_family, data, sdk_call):
    records = list(data) if hasattr(data, '__iter__') and not isinstance(data, (str, dict)) else [data]
    return {"api_family": api_family, "status": "ok", "count": len(records),
            "data": _serialize(records), "sdk_call": sdk_call, "error": None}

def _scope_error(api_family, sdk_call):
    return {"api_family": api_family, "status": "scope_not_granted", "count": 0,
            "data": [], "sdk_call": sdk_call,
            "error": "OAuth scope not granted for this API family. Required for Phase 2."}

def _error(api_family, sdk_call, e):
    return {"api_family": api_family, "status": "error", "count": 0,
            "data": [], "sdk_call": sdk_call, "error": str(e)}

def _serialize(records):
    """Convert SDK objects to JSON-safe dicts."""
    result = []
    for r in records:
        if hasattr(r, '__dict__'):
            result.append({k: str(v) for k, v in r.__dict__.items() if not k.startswith('_')})
        elif isinstance(r, dict):
            result.append(r)
        else:
            result.append(str(r))
    return result

def explore_merchants():
    sdk_call = "client.merchants.list()"
    try:
        client = _client()
        # implement using Condor's sample call
        pass
    except Exception as e:
        # check if 403 / permission error → return _scope_error
        return _error("merchants", sdk_call, e)

def explore_locations():
    sdk_call = "client.locations.list()"
    try:
        client = _client()
        pass
    except Exception as e:
        return _error("locations", sdk_call, e)

def explore_payments():
    sdk_call = "client.payments.list(limit=LIMIT)"
    try:
        client = _client()
        pass
    except Exception as e:
        return _error("payments", sdk_call, e)

def explore_refunds():
    sdk_call = "client.refunds.list(limit=LIMIT)"
    try:
        client = _client()
        pass
    except Exception as e:
        return _error("refunds", sdk_call, e)

def explore_orders():
    sdk_call = "client.orders.search(...)"
    try:
        client = _client()
        pass
    except Exception as e:
        return _error("orders", sdk_call, e)

def explore_cash_drawers():
    sdk_call = "client.cash_drawers.shifts.list(location_id=..., limit=LIMIT)"
    try:
        client = _client()
        pass
    except Exception as e:
        if "403" in str(e) or "INSUFFICIENT_SCOPES" in str(e):
            return _scope_error("cash_drawers", sdk_call)
        return _error("cash_drawers", sdk_call, e)

def explore_labor():
    sdk_call = "client.labor.search_timecards(filter={...})"
    try:
        client = _client()
        pass
    except Exception as e:
        if "403" in str(e) or "INSUFFICIENT_SCOPES" in str(e):
            return _scope_error("labor", sdk_call)
        return _error("labor", sdk_call, e)

def explore_inventory():
    sdk_call = "client.inventory.list(limit=LIMIT)"
    try:
        client = _client()
        pass
    except Exception as e:
        if "403" in str(e) or "INSUFFICIENT_SCOPES" in str(e):
            return _scope_error("inventory", sdk_call)
        return _error("inventory", sdk_call, e)

def explore_disputes():
    sdk_call = "client.disputes.list(limit=LIMIT)"
    try:
        client = _client()
        pass
    except Exception as e:
        if "403" in str(e) or "INSUFFICIENT_SCOPES" in str(e):
            return _scope_error("disputes", sdk_call)
        return _error("disputes", sdk_call, e)

def explore_gift_cards():
    sdk_call = "client.gift_cards.list(limit=LIMIT)"
    try:
        client = _client()
        pass
    except Exception as e:
        if "403" in str(e) or "INSUFFICIENT_SCOPES" in str(e):
            return _scope_error("gift_cards", sdk_call)
        return _error("gift_cards", sdk_call, e)

def explore_customers():
    sdk_call = "client.customers.list(limit=LIMIT)"
    try:
        client = _client()
        pass
    except Exception as e:
        if "403" in str(e) or "INSUFFICIENT_SCOPES" in str(e):
            return _scope_error("customers", sdk_call)
        return _error("customers", sdk_call, e)

def explore_team_members():
    sdk_call = "client.team_members.list(limit=LIMIT)"
    try:
        client = _client()
        pass
    except Exception as e:
        if "403" in str(e) or "INSUFFICIENT_SCOPES" in str(e):
            return _scope_error("team_members", sdk_call)
        return _error("team_members", sdk_call, e)

def explore_catalog():
    sdk_call = "client.catalog.list(limit=LIMIT)"
    try:
        client = _client()
        pass
    except Exception as e:
        return _error("catalog", sdk_call, e)

def explore_invoices():
    sdk_call = "client.invoices.search(query={...})"
    try:
        client = _client()
        pass
    except Exception as e:
        if "403" in str(e) or "INSUFFICIENT_SCOPES" in str(e):
            return _scope_error("invoices", sdk_call)
        return _error("invoices", sdk_call, e)

def explore_subscriptions():
    sdk_call = "client.subscriptions.search(query={...})"
    try:
        client = _client()
        pass
    except Exception as e:
        if "403" in str(e) or "INSUFFICIENT_SCOPES" in str(e):
            return _scope_error("subscriptions", sdk_call)
        return _error("subscriptions", sdk_call, e)

def explore_loyalty():
    sdk_call = "client.loyalty.accounts.search(...)"
    try:
        client = _client()
        pass
    except Exception as e:
        if "403" in str(e) or "INSUFFICIENT_SCOPES" in str(e):
            return _scope_error("loyalty", sdk_call)
        return _error("loyalty", sdk_call, e)

# Dispatch table — maps URL slug to function
# CRITICAL: slugs MUST match dashboard data-family attributes in square_explorer.html
EXPLORER_REGISTRY = {
    "merchants": explore_merchants,
    "locations": explore_locations,
    "payments": explore_payments,
    "refunds": explore_refunds,
    "orders": explore_orders,
    "cash_drawers": explore_cash_drawers,
    "labor": explore_labor,
    "inventory": explore_inventory,
    "catalog": explore_catalog,
    "customers": explore_customers,
    "team_members": explore_team_members,
    "gift_cards": explore_gift_cards,
    "loyalty": explore_loyalty,
    "invoices": explore_invoices,
    "disputes": explore_disputes,
    "subscriptions": explore_subscriptions,
}

def explore(api_family: str) -> dict:
    """Dispatch to the correct explore function by family name."""
    fn = EXPLORER_REGISTRY.get(api_family)
    if not fn:
        return {"api_family": api_family, "status": "error", "count": 0,
                "data": [], "sdk_call": "N/A", "error": f"Unknown API family: {api_family}"}
    return fn()
```

Fill in all the `pass` stubs using exact SDK method names from Condor's map and the cloned `square-python-sdk`. The scaffold above is the contract — implement it.

---

### File 2: Flask Blueprint

```
/Users/geofflyle/GrowDirect/Canary/canary/blueprints/square_explorer_wired.py
```

```python
"""
Square Capability Explorer Blueprint
GET /explore/<api_family>  ->  JSON response from square_capability_explorer
GET /explorer              ->  serves static/square_explorer.html
"""
from flask import Blueprint, jsonify, send_from_directory, current_app
from canary.services.square_capability_explorer import explore
import os

square_explorer_bp = Blueprint("square_explorer", __name__)

@square_explorer_bp.route("/explore/<api_family>")
def explore_family(api_family):
    result = explore(api_family)
    return jsonify(result)

@square_explorer_bp.route("/explorer")
def explorer_dashboard():
    static_dir = os.path.join(current_app.root_path, "..", "static")
    return send_from_directory(static_dir, "square_explorer.html")
```

Register `square_explorer_bp` in the app's blueprint registry. Follow the same wiring pattern as other `_wired.py` blueprints in the codebase.

---

## After Wiring

Test all 16 functions manually before handing off:

```bash
cd /Users/geofflyle/GrowDirect/Canary
python -c "
from canary.services.square_capability_explorer import EXPLORER_REGISTRY
for name, fn in EXPLORER_REGISTRY.items():
    result = fn()
    print(f'{name}: {result[\"status\"]} ({result[\"count\"]} records)')
"
```

Note any `scope_not_granted` results — these are the Phase 2 OAuth expansion list. Write them to:
```
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Jeremy/B067_ScopeGapList.md
```

That file routes to Syd and Eva.

---

## Standing Directives

- All reads. No writes.
- SDK paginators: first page only — never `.list()` to exhaustion.
- Trust the SDK. Do not re-implement what Square already built.
- B-063: confirm SDK is still 44.0.1.20260122 before session start.

---

*ALX | February 28, 2026 | B-067-B*
