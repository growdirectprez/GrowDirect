---
title: canary.growdirect.io — Site Update Instructions
tags: [canary, site, content-ops]
updated: 2026-04-28
last-compiled: 2026-04-28
needs-review: 2026-05-12
---

# canary.growdirect.io — Site Update Instructions

**Governing rule:** The product site is a projection of the live app. When the app changes, the site must follow. This card tells you exactly which files to check and what to update.

---

## Source of truth locations

| Site section | App route | Template file | Blueprint handler |
|---|---|---|---|
| Splash / home | `/` | `Canary/templates/marketing/splash.html` | `views_wired.py` → `index()` |
| Dashboard | `/home` | `Canary/templates/app/home.html` | `app_dashboard()` |
| Detection & alerts | `/chirps` | `Canary/templates/app/chirps.html` | `app_chirps()` |
| Alert detail | `/alert/<id>` | `Canary/templates/app/alert_detail.html` | `app_alert_detail()` |
| Case management (Vault) | Vault tab in `/chirps` | `Canary/templates/app/chirps.html` (Vault panel) | `app_chirps()` |
| Case detail | `/case/<id>` | `Canary/templates/app/case_detail.html` | `app_case_detail()` |
| Analytics search | `/owl` | `Canary/templates/app/owl.html` | `app_owl()` |
| Transactions | `/transactions` | `Canary/templates/app/transactions.html` | `app_transactions()` |
| Transaction detail | `/txn/<id>` | `Canary/templates/app/txn_detail.html` | `app_transaction_detail()` |
| Health reports | `/reports` | `Canary/templates/app/reports.html` | `app_reports()` |
| Detection rules | `/rule/<id>` | `Canary/templates/app/rule_editor.html` | `app_rule_editor()` |
| Settings | `/settings` | `Canary/templates/app/settings.html` | `app_settings()` |
| Team / employee scores | `/team` | `Canary/templates/app/team.html` | `app_team()` |

All blueprint handlers live in `Canary/canary/blueprints/views_wired.py`.

---

## What to check after each app release

### Detection rules changed (new rules, renamed rules, threshold changes)

1. Read `Canary/docs/sdds/v2/chirp.md` — the catalog table lists all rules with severity and category
2. Check `Canary/canary/blueprints/views_wired.py` → `_build_rule_map()` for the current rule set
3. Update the rule-count claim on the splash: `Canary/templates/marketing/splash.html` (currently "37 detection rules")
4. Update the rule-category table in the content brief: `docs/superpowers/specs/canary-growdirect-io-content-brief.md` section 4.7

### Event catalog changed (new event types)

1. Check `Canary/templates/marketing/splash.html` — the event-grid section lists 27 event types explicitly
2. Any new event type that ships in the pipeline needs a chip added to the grid
3. Update the count claim: currently "27 registered event types"
4. Source of record for event types: `Canary/docs/sdds/v2/webhook-pipeline.md`

### New feature module added (new top-level route or screen)

1. Check `views_wired.py` for any new `@views_bp.route()` decorators added since last review
2. Determine if the screen is user-facing or internal-only (admin routes, dev routes, MCP endpoints)
3. If user-facing: add a page entry to the page map in `docs/superpowers/specs/canary-growdirect-io-content-brief.md`
4. If the module is ready for external visibility, build the corresponding product page

### API endpoints changed

1. The 5 endpoints on the splash are documented in `Canary/templates/marketing/splash.html` (the `endpoint-list` section)
2. Canonical REST API is anchored by: `POST /webhooks/<source>`, `GET /api/alerts`, `GET /api/fox/cases`, `GET /api/analytics`, `GET /api/receipt/<event_id>`
3. Any new externally-relevant endpoint: update the splash endpoint list and the integration reference page

### Score model or health report structure changed

1. Check `Canary/docs/sdds/v2/analytics.md` — the scoring model and band classification logic live here
2. Check `Canary/docs/sdds/v2/owl.md` — heartbeat score computation and owl_sessions schema
3. Health report template: `Canary/templates/app/reports.html`
4. Update the Health Reports section of the content brief if the score ring or band labels change

---

## What NOT to sync to the site

These parts of the app are internal and should never appear in external product pages:

- `Canary/templates/admin/` — all admin templates (user management, config, audit log)
- `Canary/templates/ops/` — ops console, atlas, QA test lab, pipeline debug
- `Canary/canary/blueprints/ops_console.py` — internal monitoring
- `Canary/canary/blueprints/devops_monitor.py` — health check internals
- Any route prefixed `/admin/`, `/api/trace/`, `/api/rule-guide/` (internal reference)
- `Canary/templates/pipeline_trace.html` — dev observability only

---

## Quick site health check

Run this before any content update to confirm the routes being documented are still live:

```bash
# Verify app is running
curl -s http://localhost:5001/health

# Verify key routes respond (requires a valid session cookie — use demo merchant)
# curl -s -b "session=<your-session>" http://localhost:5001/home
# curl -s -b "session=<your-session>" http://localhost:5001/chirps
# curl -s -b "session=<your-session>" http://localhost:5001/owl
```

If a route returns 404 or redirects to login, it may have been renamed — check
`views_wired.py` for the current `@route()` decorator.

---

## Related files

- Content brief: `docs/superpowers/specs/canary-growdirect-io-content-brief.md`
- Splash template: `Canary/templates/marketing/splash.html`
- All blueprints: `Canary/canary/blueprints/views_wired.py`
- Architecture SDD: `Canary/docs/sdds/v2/architecture.md`
- Detection engine SDD: `Canary/docs/sdds/v2/chirp.md`
- Case management SDD: `Canary/docs/sdds/v2/fox.md`
- Analytics SDD: `Canary/docs/sdds/v2/analytics.md`
- AI search SDD: `Canary/docs/sdds/v2/owl.md`
