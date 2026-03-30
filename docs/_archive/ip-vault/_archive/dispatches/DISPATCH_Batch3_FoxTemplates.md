---
type: workorder
domain: fox
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Batch 3 Dispatch — Fox Routes + Template Consolidation

**Date:** 2026-03-04
**Dispatcher:** ALX
**Issues:** GRO-41, GRO-44, GRO-37
**Depends on:** Batch 1 (cleanup) ✅, Batch 2 (wire UI) ✅

---

## Executive Summary

All three Batch 3 issues were **already resolved** by the GRO-71 Rebaseline and GRO-72 Route Contract work that landed earlier today. The dispatch below documents the evidence for each and recommends closing all three after a single verification pass.

---

## GRO-41 — Bug: /fox/cases returns 401 in stub mode

**Original problem:** `canary/fox/routes.py` had a `set_merchant_context()` before_request hook that overwrote `g.merchant_id` set by `wsgi.py`'s `load_current_user()`, causing the sidebar link to return a JSON 401.

**Current state — FIXED:**

| Layer | What happens |
|---|---|
| `wsgi.py` line 134 | `load_current_user()` runs as `@app.before_request`, sets `g.merchant_id` from `SQUARE_MERCHANT_ID` env var |
| `views_wired.py` line 1025 | `@views_bp.route("/fox")` renders `fox/cases.html` — no JWT required |
| `sidebar.html` line 39 | Sidebar links to `/fox` (not `/fox/cases`) |
| `fox_wired.py` | Registered at `/api/fox` — API-only, JWT-protected (by design) |

The old `canary/fox/routes.py` with `set_merchant_context()` **no longer exists**. The current `fox_wired.py` has no before_request hook — it uses `@jwt_required()` per-route, which is correct for the API layer. The HTML route at `/fox` goes through `views_bp` and only needs the env-based merchant context.

**Verify:** `curl -s http://localhost:5001/fox` should return HTML (not 401 JSON).

---

## GRO-44 — Route conflict: fox_bp API shadows views_bp HTML

**Original problem:** Both `fox_bp` and `views_bp` registered `/fox/cases` — the API blueprint shadowed the HTML view.

**Current state — FIXED:**

```
wsgi.py BLUEPRINT_SPECS:
  fox_bp    → prefix "/api/fox"   → /api/fox/cases (JSON, JWT-required)
  views_bp  → prefix ""           → /fox           (HTML, no auth)
```

The route conflict is gone. API and HTML live at distinct prefixes:

- Browser sidebar → `/fox` → `views_bp` → renders `templates/fox/cases.html`
- Frontend JS/API → `/api/fox/cases` → `fox_bp` → returns JSON (JWT required)

**Verify:** `flask routes` output should show no duplicate `/fox/cases` registrations.

---

## GRO-37 — Two template directories — consolidate

**Original problem:** Both `templates/` (root) and `canary/templates/` existed, unclear which Flask used.

**Current state — FIXED:**

```
templates/           ← EXISTS (20+ files, all app templates including fox/)
canary/templates/    ← DOES NOT EXIST (removed during rebaseline)
```

Only one template directory remains. Flask's default `template_folder` resolves to `templates/` at project root, which is where all templates live.

**Verify:** `ls canary/templates/` should return "No such file or directory".

---

## Recommended Actions

1. **Verify all three** with a single `dev.sh up` + manual checks (3 curl commands)
2. **Close GRO-41, GRO-44, GRO-37** in Linear with verification comments
3. **Update parent issues** if these were the last children

## Verification Script

```bash
# From project root
echo "=== GRO-41: /fox returns HTML (not 401) ==="
curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/fox

echo -e "\n=== GRO-44: No route conflict ==="
curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/fox
curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer stub" http://localhost:5001/api/fox/cases

echo -e "\n=== GRO-37: canary/templates/ does not exist ==="
ls canary/templates/ 2>&1 || echo "PASS — single template directory"
```

Expected: GRO-41 → 200, GRO-44 → 200 + 200, GRO-37 → "No such file or directory"

---

*Canary LP | GrowDirect Inc. | Confidential*
