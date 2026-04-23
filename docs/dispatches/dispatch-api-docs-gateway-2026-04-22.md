# Dispatch: API Gateway Docs — Update Spec + Serve on /devops/api
## For: Fresh Claude Code session inside `~/GrowDirect/Canary/`
## Linear: GRO-169 (reopen + close)
## Session startup: `/alx-startup` first — this is Canary ALX work

---

## Why

We have an OpenAPI 3.0.3 spec at `docs/api/canary-api-v1.yaml` (v1.1.0, ~87 KB)
but (a) it's 5 weeks stale and (b) nothing serves it. GRO-169 was filed to
deliver an interactive docs UI on our devops surface. That's still open.

**Two deliverables:**

1. **Bring `canary-api-v1.yaml` up to current reality** — blueprints,
   endpoints, request/response shapes, rule counts.
2. **Serve it at `https://dev.growdirect.app/devops/api`** with Redoc, so
   the team has a live interactive reference.

Bonus deliverable 3: mirror the YAML to the static site
(`canary-site/docs/assets/canary-api-v1.yaml`) so the parallel narrative
dispatch (the one landing on `canary.growdirect.io/docs/API.html`) can
point at a single canonical copy via URL.

---

## Ground rules

1. **Documentation as code.** The YAML should be generated or verified
   against `app.url_map` — not hand-edited.
2. **Don't change API behavior.** This issue is doc-only — no new routes,
   no renamed endpoints, no refactors. If you find a drift, fix the YAML,
   not the code.
3. **wsgi.py is Guardian-protected.** If a blueprint needs registering
   for `/devops/api`, go through `critical-file-guardian`. Adding a route
   inside an existing blueprint does NOT require Guardian.
4. **No new heavy dependencies.** Use Redoc via CDN (one `<script>` tag).
   Don't add `flasgger`, `flask-swagger`, or `flask-smorest` for this
   iteration.

---

## Deliverable 1 — Update the spec

### Source of truth for endpoints
`wsgi.py` registers blueprints via `BLUEPRINT_SPECS` (around line 180).
At runtime, `app.url_map.iter_rules()` gives every route with its
methods and endpoint name.

### Verification script
Write `devops/scripts/api_spec_audit.py`:
- Import the Flask app.
- Walk `app.url_map.iter_rules()`. Filter out Flask internals
  (`/static/...`, `/health`) — keep everything under the business
  blueprints.
- Load `docs/api/canary-api-v1.yaml`.
- Produce two lists side-by-side:
  - **In live app, not in YAML** → endpoints to add
  - **In YAML, not in live app** → endpoints to remove
- Exit code 0 if in sync, 1 with diff if not.

Run it. Reconcile. Re-run until exit 0.

### Content to sync in the YAML
Also update (these drift fastest):
- `info.version` — bump to `1.2.0`
- `info.description` — current blueprint count, rule count, MCP server
  count. Current CLAUDE.md says "37 detection rules"; verify against
  `canary.services.chirp.rule_definitions.RULE_CATALOG`.
- `servers` — add `https://canary.growdirect.app` (production target
  when it comes up) and keep `dev.growdirect.app` + `localhost`
- Security schemes — confirm JWT-bearer for protected routes, API key
  for `/owl/*` manifest endpoints, HMAC for webhook endpoints
- `components/schemas` — check that `Alert`, `FoxCase`, `Transaction`,
  `Merchant` match the SQLAlchemy models. The Pydantic/dataclass
  definitions in `canary/schemas/` are source of truth.

### Avoid manual-edit drift in the future
Add a brief section to `docs/api/README.md` (or create it) noting:
- How to regenerate: `python3 devops/scripts/api_spec_audit.py`
- Where the spec is served: `/devops/api`
- Who owns drift: whoever added the endpoint

---

## Deliverable 2 — Serve at /devops/api

### Route
Add to `canary/blueprints/devops_monitor.py`:

```python
from flask import send_from_directory, render_template_string

API_SPEC_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "docs", "api",
)

@devops_monitor_bp.route("/api")
def api_docs():
    """Redoc-rendered interactive API reference."""
    return render_template_string(_REDOC_TEMPLATE)

@devops_monitor_bp.route("/api/spec.yaml")
def api_spec():
    """Serve the raw OpenAPI YAML."""
    response = send_from_directory(API_SPEC_PATH, "canary-api-v1.yaml")
    response.headers["Content-Type"] = "text/yaml; charset=utf-8"
    response.headers["Cache-Control"] = "no-store"
    return response

_REDOC_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
  <title>Canary API — Interactive Reference</title>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700"
        rel="stylesheet">
  <style>body { margin: 0; padding: 0; background: #060608; }</style>
</head>
<body>
  <redoc spec-url="/devops/api/spec.yaml"
         theme='{"colors": {"primary": {"main": "#FBBF24"}}, "typography": {"fontFamily": "Inter, system-ui, sans-serif"}}'
         hide-loading></redoc>
  <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
</body>
</html>"""
```

### Registration
`devops_monitor_bp` already mounts at `/devops` (wsgi.py line ~191).
New routes will resolve at:
- `https://dev.growdirect.app/devops/api` — Redoc UI
- `https://dev.growdirect.app/devops/api/spec.yaml` — raw spec

The `sandbox_guard()` before-request hook on this blueprint — check
whether the `/api` routes should be protected the same way as
`/monitor`. If yes, leave the guard in place. If the spec should be
publicly readable (it's non-sensitive reference material), add the
decorator `@public` or exempt these two endpoints in `sandbox_guard`.

**Recommended:** keep the guard. Anyone with `/devops/monitor` access
can also see `/devops/api`.

### Verification
1. `python3 -c "from wsgi import app; print([str(r) for r in app.url_map.iter_rules() if r.rule.startswith('/devops/api')])"`
   → expect two rules.
2. `docker compose … exec flask curl -s http://localhost:5001/devops/api/spec.yaml | head -5`
   → expect `openapi: 3.0.3`
3. Hit `https://dev.growdirect.app/devops/api` in a browser → Redoc
   renders the spec.

---

## Deliverable 3 — Mirror to the static site

Copy the **updated** `canary-api-v1.yaml` to
`~/canary-site/docs/assets/canary-api-v1.yaml`. Commit to that repo too.

This lets the parallel narrative dispatch (`dispatch-vscode-library-narrative-2026-04-22.md`)
point its `API.html` at a single canonical YAML via:
```html
<redoc spec-url="assets/canary-api-v1.yaml"></redoc>
```

---

## Tests

Unit: `tests/unit/test_api_docs_route.py`
- `GET /devops/api` → 200, content-type text/html, body contains `<redoc>`
- `GET /devops/api/spec.yaml` → 200, content-type `text/yaml`, starts `openapi:`

Integration: run the audit script; expect exit 0.

No new smoke tests required — `/devops/monitor` smoke coverage already
exists and this is additive.

---

## Commit pattern

Three commits, in order:

1. `docs(api): sync canary-api-v1.yaml with live url_map (v1.2.0)` —
   YAML update only
2. `feat(devops): serve OpenAPI spec at /devops/api with Redoc` —
   blueprint route + template
3. `chore(api): add audit script to catch spec drift` — new
   `devops/scripts/api_spec_audit.py`

Then canary-site:
4. `chore(docs): mirror canary-api-v1.yaml for static API.html` — copy
   yaml into `canary-site/docs/assets/` and push.

Co-author trailer:
```
Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## Linear

- **Update** GRO-169 with:
  - Work completed
  - Three PR commit hashes
  - Live URL: https://dev.growdirect.app/devops/api
  - Audit command for future drift
- **Move** GRO-169 → `Done`

---

## Return envelope

Paste back to orchestrator:
1. Audit script diff before/after (endpoint counts added/removed)
2. YAML version + sizes before/after
3. Commit hashes (Canary repo + canary-site repo)
4. Live URL verification result (HTTP status + content-type)
5. GRO-169 status after update

---

## Out of scope

- Kong or any API gateway infra work (GRO-190 already landed)
- New endpoints or schema changes
- Authentication flow changes
- Rate limiting config changes

---

*Dispatch prepared by ALX · 2026-04-22*
