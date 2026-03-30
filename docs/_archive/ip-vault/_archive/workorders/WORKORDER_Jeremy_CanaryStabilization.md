---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Work Order: Canary App Stabilization

**Linear Project:** Canary LP
**Date:** 2026-03-04
**Issued by:** Jeffe
**Priority:** High — ship blocker

---

## Context

The Canary LP codebase was renamed from `alpha3x` to `canary` but never properly rebaselined. The result is 13 symptoms that trace back to 3 root causes. This work order addresses all three in sequence.

**Do not fix symptoms individually.** The issues are entangled — fixing one without the others creates new bugs. Execute the phases in order.

---

## Phase 1: Rebaseline (GRO-71)

**Goal:** Complete the alpha3x → canary transition in one clean sweep.

### 1A. Scrub alpha3x naming (GRO-42)

- Run `grep -ri alpha3x` across the entire codebase
- Rename all 192 references to `canary`
- This includes module names, docstrings, comments, config keys, log messages
- Do NOT rename git history or branch names — only live code

### 1B. Resolve duplicate files (GRO-35)

Two pairs of same-named files exist in different directories:

| File | Location A | Location B |
|------|-----------|-----------|
| `card_profiles.py` | `canary/card_profiles.py` | `canary/models/app/card_profiles.py` |
| `session_factory.py` | `canary/models/session_factory.py` | `canary/db/session_factory.py` |

**For each pair:**
1. Check which copy is actually imported (grep for `from canary.` and `import`)
2. Keep the one that's imported, delete the orphan
3. Update any stale imports pointing to the deleted path
4. Verify: `python -c "from canary.db.session_factory import ..."` succeeds

Also verify: 3 different `decorators.py` files (auth, permissions, billing) — these may be intentional but confirm each is imported somewhere.

### 1C. Consolidate template directories (GRO-37)

Two template dirs exist: `templates/` and `canary/templates/`.

1. Determine which directory Flask's `template_folder` points to in `wsgi.py`
2. Move all templates to that single canonical directory
3. Delete the empty directory
4. Verify: all Jinja2 `render_template()` calls resolve

### 1D. Clean dead imports (GRO-62)

- `canary/blueprints/__init__.py` references `webhooks.py` which was deleted
- Remove the import
- Check for any other imports of deleted modules: `python -m py_compile canary/blueprints/__init__.py`

### 1E. Fix SQLite docstrings (GRO-43)

- Docstrings in several modules still describe SQLite as the database
- The app runs on PostgreSQL
- Update docstrings to reflect actual architecture
- Add to `CLAUDE.md`: "No SQLite. Canary uses PostgreSQL. Do not introduce SQLite for any reason."

### 1F. Wire views_wired blueprint (GRO-68)

`canary/blueprints/views_wired.py` contains all desktop UI routes but is not registered in `wsgi.py`.

1. Add `views_wired.py` to `BLUEPRINT_SPECS` in `wsgi.py`
2. Remove or move the root `/` JSON health endpoint to `/api/info` to avoid conflict
3. Verify: `http://localhost:5001/` serves the dashboard HTML page
4. Verify: all template routes render — `/dashboard`, `/chirps`, `/transactions`, `/employees`, `/reports`, `/fox`, `/settings`, `/audit_log`

### 1G. Fix OAuth env var mismatch (GRO-69)

Code uses different env var names than `.env` file:

| Code expects | .env has |
|-------------|----------|
| `SQUARE_APP_ID` | `SQUARE_APPLICATION_ID` |
| `SQUARE_APP_SECRET` | `SQUARE_APPLICATION_SECRET` |

**Fix:** Update code to match `.env` naming (the `.env` names match Square's official SDK naming).

Also fix in `square_oauth_wired.py`:
- Redirect URL: append params dict to URL (currently builds params but never uses them)
- Callback: read `SQUARE_REDIRECT_URL` from env instead of `request.args`
- Token exchange: use `json=` not `data=` for Square API
- Error redirects: point to `/settings` not `/connect`
- `.env`: redirect URL should be `/oauth/callback` not `/callback`
- Fernet init: catch `ValueError` if `CANARY_ENCRYPTION_KEY` is not a valid Fernet key

### Phase 1 verification

```bash
# No alpha3x references remain
grep -ri alpha3x canary/ templates/ --include="*.py" --include="*.html" --include="*.env" | wc -l
# Should return 0

# No duplicate files
find . -name "card_profiles.py" | wc -l  # Should be 1
find . -name "session_factory.py" | wc -l  # Should be 1

# One template directory
find . -type d -name "templates" | wc -l  # Should be 1

# App boots clean
python -c "from canary.blueprints import *"  # No ImportError

# Dashboard serves HTML
curl -s http://localhost:5001/ | head -1  # Should start with <!DOCTYPE or <html
```

---

## Phase 2: Route Contract (GRO-72)

**Goal:** All API endpoints under `/api/`, all HTML views at root. No shadowing, no hook interference.

### 2A. Prefix API blueprints (GRO-44)

The `fox_bp` blueprint registers JSON routes at `/fox/cases`, which shadows the HTML view at the same path.

1. Change `fox_bp` url_prefix from `/fox` to `/api/fox` in `canary/fox/routes.py`
2. Update `canary/blueprints/registry.py` prefix from `/fox` to `/api/fox`
3. Update all test URLs in `canary/fox/test_fox_selenium.py`
4. Audit ALL other API blueprints — any that don't already have `/api/` prefix need it
5. Update docstrings and docker-compose comments

### 2B. Fix merchant context hook (GRO-41)

`set_merchant_context()` in `canary/fox/routes.py` (before_request hook) unconditionally overwrites `g.merchant_id`, breaking stub mode.

**Current (broken):**
```python
else:
    g.merchant_id = request.headers.get('X-Merchant-ID', type=int)  # → None
    g.user_id = request.headers.get('X-User-ID', 1, type=int)

if not g.merchant_id:
    return jsonify({'error': 'Merchant context required'}), 401
```

**Fix:**
```python
if hasattr(g, 'user') and g.user:
    g.merchant_id = g.user.get('merchant_id')
    g.user_id = g.user.get('id')
elif not getattr(g, 'merchant_id', None):
    g.merchant_id = request.headers.get('X-Merchant-ID', type=int)
    g.user_id = request.headers.get('X-User-ID', 1, type=int)

if not g.merchant_id:
    return jsonify({'error': 'Merchant context required'}), 401
```

### 2C. Fix dashboard template data shapes (GRO-70)

Three bugs in the dashboard:

1. **Button hrefs** — "Connect Sandbox" links to `/sandbox` (404), should be `/oauth/sandbox`. "Connect via OAuth" links to `/authorize` (404), should be `/oauth/authorize`.

2. **Connected state** — `dashboard()` view in `views_wired.py` never passes `connected` to the template. Fix: query `SquareOAuthService` for token, pass `connected`, `merchant_id`, `merchant_name`, `square_environment` to template context.

3. **Alert keys** — Template references `alert.alert_type`, `alert.employee_id`, `alert.refund_count`, `alert.created_at`, `alert.resolved` — but `_get_alerts()` and `_demo_alerts()` return dicts with keys `message`, `employee`, `time`, `status`. Fix: update the template loop to use the actual dict keys.

### Phase 2 verification

```bash
# No route shadowing — API and HTML should not share paths
# Check registered routes
python -c "
from canary.wsgi import create_app
app = create_app()
for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
    print(f'{rule.rule:40s} → {rule.endpoint}')
" | grep fox
# Should show /api/fox/cases (JSON) and /fox/cases (HTML) — different prefixes

# Stub mode works
curl -s http://localhost:5001/fox/cases | head -1  # Should be HTML, not JSON 401

# Dashboard renders with connect state
curl -s http://localhost:5001/ | grep -c "oauth/sandbox"  # Should be >= 1
```

---

## Phase 3: QA Gate (GRO-73)

**Blocked by:** Phase 1 + Phase 2 complete.

### 3A. Cloudflare Tunnel (GRO-24)

On Mac Mini (192.168.10.102, macOS):

```bash
brew install cloudflared
cloudflared tunnel login
cloudflared tunnel create canary-qa
cloudflared tunnel route dns canary-qa qa.growdirect.app
cloudflared tunnel run canary-qa
```

Configure tunnel to route `qa.growdirect.app` → `http://localhost:5001`.

Domain `growdirect.app` nameservers already migrated to Cloudflare.

### 3B. QA sweep — all 9 routes (GRO-12)

Verify from QA iMac (192.168.10.117, Ubuntu) via `qa.growdirect.app`:

| # | Route | Expected |
|---|-------|----------|
| 1 | `/` or `/dashboard` | Dashboard HTML with connect card or merchant data |
| 2 | `/chirps` | Chirps/alerts list page |
| 3 | `/transactions` | Transaction list page |
| 4 | `/employees` | Employee list page |
| 5 | `/reports` | Reports page |
| 6 | `/fox/cases` | Cases HTML page (not JSON) |
| 7 | `/settings` | Settings page |
| 8 | `/audit_log` | Audit log page |
| 9 | `/companion` | Companion page |

**Pass criteria for each route:**
- Returns 200
- Content-Type is `text/html`
- No Jinja2 UndefinedError
- Sidebar navigation links work
- Demo/stub data renders (no blank pages)

---

## Out of scope

**GRO-63** (Chirp: flag untethered transactions) — genuine new feature, not stabilization. Do not bundle with this work order.

---

## Execution notes

- Phases 1 and 2 can be worked in parallel by different people, but both must be done before Phase 3
- Phase 1 is the biggest — estimate 1-2 hours for a focused sweep
- Phase 2 is surgical — estimate 30-45 minutes
- Phase 3 is verification — estimate 30 minutes (tunnel) + 30 minutes (QA sweep)
- Commit after each phase, not after each sub-task
- Tag commits with the parent GRO issue number (GRO-71, GRO-72, GRO-73)
