---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# B-067 — Square Capability Dashboard: Master Dispatch
**Work Order:** B-067
**Date:** February 28, 2026
**Dispatched by:** ALX
**Priority:** HIGH — Strategic visibility for Jeffe
**Session type:** Three-lane parallel build
**Output:** One single-page HTML dashboard. Jeffe opens it, sees everything Square exposes, understands what Canary already covers and what is next.

---

## What This Is

Jeffe needs to see what he has. Not a spec. Not a roadmap. A live, clickable inventory of every Square API family wired to real sandbox data — side by side with what the TSP pipeline already handles and what is coming in Phase 2+.

This is a strategic instrument, not a dev tool. When Jeffe is done with it, he knows:
- What Square gives us for free (14 API families)
- What Canary already ingests (payments + refunds — Phase 1 LIVE)
- What the TSP pipeline seals and inscribes (the heartbeat)
- What Phase 2 unlocks (cash drawer, labor, orders, inventory, gift cards)
- The full LP coverage arc: 14% today to 85% at Phase 3

No unit tests. Square's SDK is stable open source — trust it. The job is to knit it together and show it.

---

## Credentials (Sandbox Only)

All three agents use these. Source: `/Users/geofflyle/GrowDirect/Canary/.env`

```
SQUARE_ACCESS_TOKEN=EAAAl3ns-vSWSvjgQL7KMKyTxoWP5PMPns6W2PP3pQ_43Fs8lf3_qHV_wyj693Rl
SQUARE_APPLICATION_ID=sandbox-sq0idb-SduFLmiaE43X0BeFC37Taw
SQUARE_ENVIRONMENT=sandbox
SQUARE_MERCHANT_ID=MLE55GCYANCYT
```

Sandbox base URL: `https://connect.squareupsandbox.com`

---

## Three Lanes — Run in Parallel

**LANE A: Condor** — Architecture + capability map (the intellectual backbone)
**LANE B: Jeremy** — Backend Python module + Flask endpoint
**LANE C: Qwen** — Frontend HTML dashboard shell

Condor's first deliverable gates Jeremy's wiring pass. Qwen scaffolds in parallel — does not need to wait.

---

## LANE A — Condor: Capability Map

**Session prompt:** `dispatches/Condor_B067A_CapabilityMap.md`

**Read first:**
```
/Users/geofflyle/GrowDirect/Canary_IP/Markdown/Specs/Square_API_LP_Coverage_Analysis_Jeremy_v1.0.md
/Users/geofflyle/GrowDirect/Canary/square/SQUARE_SCAN_NOTES.md
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Condor/TSP_ConsolidatedReview_v1.0.md
/Users/geofflyle/GrowDirect/Canary/square/square-python-sdk/README.md
```

**Produce:** `/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Condor/B067_SquareCapabilityMap_v1.0.md`

For each of the 14 Square API families, produce one block in this exact format:

```
API Family:               [Name]
SDK Namespace:            client.[namespace]
Sandbox Permission:       [OAuth scope name]
Canary Phase:             [Phase 1 LIVE | Phase 2 | Phase 3 | Not planned]
TSP Component:            [TSP-01 through TSP-09, or N/A]
LP Signal:                [one sentence — what fraud or loss this catches]
Key Read Methods:         [3-5 SDK method names]
Sample Call:              [one Python line using square-python-sdk v44 syntax]
Dashboard Section Title:  [what Jeffe sees as the header]
Fetch Button Label:       [the button text on the card]
Phase Badge:              [LIVE | PHASE 2 | PHASE 3]
```

The 14 families (from Jeremy's LP analysis):
1. Payments API
2. Refunds API
3. Orders API
4. Cash Drawer Shifts API
5. Labor / Timecards API
6. Inventory API
7. Disputes API
8. Gift Cards API
9. Customers API
10. Loyalty API
11. Team Members API
12. Catalog API
13. Devices API
14. Webhooks / Subscriptions API

Also produce a TSP coverage table — for each family: what Sub 1, Sub 2, Sub 3 do with it, and current status: LIVE / PLANNED / NOT STARTED.

Deliver this before Jeremy starts his wiring pass.

---

## LANE B — Jeremy: API Module + Flask Blueprint

**Session prompt:** `dispatches/Jeremy_B067B_APIModule.md`

**Read first:**
```
/Users/geofflyle/GrowDirect/Canary/square/square-python-sdk/README.md
/Users/geofflyle/GrowDirect/Canary/square/SQUARE_SCAN_NOTES.md
Condor B067_SquareCapabilityMap_v1.0.md  (wait for this before wiring)
```

**Build:**
```
/Users/geofflyle/GrowDirect/Canary/canary/services/square_capability_explorer.py
/Users/geofflyle/GrowDirect/Canary/canary/blueprints/square_explorer_wired.py
```

**Pattern for the explorer module — one function per API family:**

```python
"""
Square Capability Explorer
One function per Square API family. All reads. Sandbox only.
Returns structured dict: {api_family, status, count, data, error}

# SQUARE OPEN SOURCE — follows SDK patterns from:
# /Users/geofflyle/GrowDirect/Canary/square/square-python-sdk/
"""
from square import Square
import os

def _client():
    return Square(
        token=os.environ["SQUARE_ACCESS_TOKEN"],
        environment=os.environ.get("SQUARE_ENVIRONMENT", "sandbox"),
    )

def explore_payments(limit=10): ...
def explore_refunds(limit=10): ...
def explore_orders(limit=10): ...
def explore_cash_drawer_shifts(limit=5): ...
def explore_timecards(limit=10): ...
def explore_inventory(limit=10): ...
def explore_disputes(limit=10): ...
def explore_gift_cards(limit=10): ...
def explore_customers(limit=10): ...
def explore_team_members(limit=10): ...
def explore_catalog(limit=10): ...
def explore_devices(): ...
def explore_webhook_subscriptions(): ...
def explore_merchant(): ...
def explore_locations(): ...
```

Rules:
- All reads. No creates, updates, or deletes.
- SDK paginators: first page only — do not materialize full datasets.
- Return dict with keys: `api_family`, `status`, `count`, `data`, `sdk_call`, `error`.
- If scope not granted, return `status: "scope_not_granted"` — do not crash.
- `sdk_call` key: log the actual SDK method called as a string — shows in dashboard.
- Use exact method names from cloned repo. Do not guess.

Flask blueprint — one route:
```
GET /explore/<api_family>  →  calls matching explore_* function  →  returns JSON
```

Register blueprint in app. Jeffe's dashboard calls this for each card.

Also: confirm Flask serves the static file at `/explorer`.

---

## LANE C — Qwen: Dashboard Shell

**Session prompt:** `dispatches/Qwen_B067C_DashboardShell.md`

**Match design language of:**
```
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Art/eljeffe-dev/index.html
```
- Background: `#0a0d12`
- Accent: `#f59e0b` (Bitcoin amber)
- Font: JetBrains Mono (code/data), Syne (headers)

**Output:** `/Users/geofflyle/GrowDirect/Canary/static/square_explorer.html`

**Page layout:**

```
HEADER
  elJeffe logo | "Square Capability Explorer" | SANDBOX badge | merchant: MLE55GCYANCYT

HERO STRIP (3 stat tiles, hard-coded for now)
  [ 14 API Families ] [ Phase 1: 2 LIVE ] [ Phase 3: 85% LP Coverage ]

CAPABILITY GRID — 14 cards, CSS grid 3-across
  Each card:
    Phase badge (top-right corner): LIVE / PHASE 2 / PHASE 3
    API family name (header)
    SDK namespace (monospace, small)
    LP Signal (one line, muted)
    TSP Component (one line)
    [ Fetch Live Data > ] button
    Response panel (hidden until fetch, expands below button)
      - Shows: record count badge, sdk_call used, formatted JSON

TSP PIPELINE STRIP (below grid)
  Horizontal flow: Square API Family → Sub 2 Parser → Sub 1 Seal → Sub 3 Ordinal → Receipt
  Color-coded by phase: LIVE=green, PHASE 2=amber, NOT STARTED=gray

FOOTER
  "Sandbox only. No real transactions. Patent Pending."
```

Phase badge colors:
- LIVE: green `#22c55e`
- PHASE 2: amber `#f59e0b`
- PHASE 3: gray `#6b7280`

Fetch behavior:
- Button click: `fetch('/explore/<api_family>')` — use the family name lowercased with underscore
- Loading: amber spinner, button disabled
- Error: red border on response panel, error message
- Success: green border, record count badge, `sdk_call` value shown in header of response panel, JSON prettified below

Placeholder text for LP Signal and TSP Component until Condor delivers the map. Qwen fills these in after Condor's map arrives or leaves clear TODO comments for Jeremy to paste into.

---

## Integration Step (Jeremy, after both lanes deliver)

1. Confirm `/explorer` serves the HTML page
2. Test all 14 "Fetch Live Data" buttons — note which return data vs `scope_not_granted`
3. Produce a scope gap list: which families need additional OAuth permissions
4. That list routes to Syd (permission expansion brief) and Eva (Sprint 7 scope)

---

## Deliverables

| File | Owner | Path |
|---|---|---|
| Capability map | Condor | `_ALX/WorkOrders/output/Condor/B067_SquareCapabilityMap_v1.0.md` |
| Explorer module | Jeremy | `Canary/canary/services/square_capability_explorer.py` |
| Flask blueprint | Jeremy | `Canary/canary/blueprints/square_explorer_wired.py` |
| Dashboard HTML | Qwen | `Canary/static/square_explorer.html` |

---

## What Jeffe Sees

Jeffe opens `http://localhost:5000/explorer`.

14 cards. He clicks Payments — real sandbox payments render. He clicks Cash Drawer — data or a clear scope gap message. He clicks Webhooks — his live subscription, the ngrok URL, the 26 events from this morning.

In 10 minutes he knows exactly what Square gives him, what Canary already handles, and what Phase 2 unlocks. That is the strategic conversation.

---

## Standing Directives

- Sandbox only. No production credentials.
- No unit tests. Trust the SDK.
- MVP scope is frozen. This is a visibility tool, not a feature.
- B-064 production heartbeat runs parallel — not blocked by this.
- Session close: all three agents update HANDOFF.md.

---

*ALX | February 28, 2026 | B-067*
*Pure reads. Sandbox only. Show Jeffe what he has.*
