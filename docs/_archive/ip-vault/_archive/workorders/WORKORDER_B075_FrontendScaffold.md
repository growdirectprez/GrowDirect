---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# WORK ORDER B-075: Frontend Scaffold — Wire the Website
**Date:** March 1, 2026
**Owner:** ALX
**Assigned to:** Jeremy (primary) + Qwen (boilerplate/templates)
**Priority:** 🔴 HIGH — Jeffe wants to see the website running
**Parallel with:** B-070 (QA/UAT gate — does not block this)
**Branch:** `frontend-scaffold` (cut from `sprint-6-tsp` HEAD: `996562f`)

---

## 1. Objective

> "Leave the icons — we need to see the website."
> — Jeffe, March 1, 2026

Get the Canary LP desktop admin and mobile companion running in a browser with the v2.0 design system, wired to real Flask endpoints, serving real-ish data. Not pixel-perfect. Not production. **Visible and navigable.**

**What "done" looks like:** Jeffe opens `localhost:5000` in Chrome and can click through every page in the sidebar, see data in the tables, and navigate the mobile companion on his phone.

---

## 2. What Already Exists (Don't Start from Scratch)

### Flask App (`Canary/app.py`)
The Flask server is live. It runs. Don't rewrite it.

### 10 Wired Blueprints (in `canary/blueprints/`)
| Blueprint | File | Status |
|---|---|---|
| Alerts | `alerts_wired.py` | ✅ Wired to DB |
| Chirp | `chirp_wired.py` | ✅ Wired to DB |
| Companion | `companion_wired.py` | ✅ Wired to DB |
| Employees | `employees_wired.py` | ✅ Wired to DB |
| Fox | `fox_wired.py` | ✅ Wired to DB |
| Locations | `locations_wired.py` | ✅ Wired to DB |
| Merchants | `merchants_wired.py` | ✅ Wired to DB |
| Square Explorer | `square_explorer_wired.py` | ✅ Wired to DB |
| Square OAuth | `square_oauth_wired.py` | ✅ Wired to DB |
| Webhooks | `webhooks_wired.py` | ✅ Wired to DB |

### Existing Templates (in `Canary/templates/` + `canary/templates/`)
**Desktop:** `dashboard.html`, `base.html`, `base_app.html`, `receipt_detail.html`, `admin/audit_log.html`, `admin/users.html`, `settings/profile.html`, `settings/team.html`, `settings/company.html`, `settings/subscription.html`, `settings/labels.html`, `auth/login.html`, `auth/register.html`, `errors/404.html`, `errors/403.html`, `errors/500.html`

**Mobile companion:** `companion/today.html` (or `todays_view.html`), `companion/wizard_step.html`, `companion/scorecard.html`, `companion/mobile_shell.html`, `companion/partials/mobile_nav.html`

### Three PostgreSQL Databases
`canary_app`, `canary_sales`, `canary_metrics` — schema exists, tables exist.

---

## 3. The Work (Four Phases)

### Phase 1: Design System Reskin (Qwen — boilerplate)
**Goal:** Apply Canary Design System v3.0 to existing templates. Dark theme, correct colors, correct fonts. Every page looks like the v2.0 prototype when you open it.

**Input:** Both v2.0 HTML prototypes (the visual source of truth):
- Mobile: `_ALX/WorkOrders/output/Art/Canary_Mobile_Prototype_v2.0.html`
- Desktop: `_ALX/WorkOrders/output/Art/Canary_Desktop_Admin_v2.0.html`

**Tasks:**
1. **Create `base_v2.html`** — new Jinja2 base template with Design System v3.0 tokens:
   - Background: `#0D1117` (dark), Surface: `#161B22`, Border: `#30363D`
   - Primary text: `#E6EDF3`, Secondary: `#8B949E`
   - Signal yellow: `#FBBF24`, Health green: `#3FB950`, Critical red: `#F85149`, Warning orange: `#D29922`
   - Fonts: Inter (body), Space Grotesk (headings) — load from Google Fonts
   - Spacing scale: 4px base (`--space-1: 4px` through `--space-8: 32px`)
   - All CSS goes in `static/css/canary-v2.css` (one file, no external deps beyond fonts)
2. **Create `sidebar_v2.html` partial** — 240px sidebar matching desktop prototype:
   - Logo area (Canary text + bird placeholder)
   - 8 nav items: Dashboard, Chirps, Transactions, Cases, Employees, Reports, Audit Log, Settings
   - Each item has module color left-border on active state
   - Collapse to icon-only on mobile width (< 768px)
   - **Icons:** Use simple colored circles (12px) as placeholders until Art delivers final mascot icons. Colors: Dashboard (#FBBF24), Chirps (#FBBF24), Transactions (#3B82F6), Cases (#F97316), Employees (#22C55E), Reports (#8B5CF6), Audit Log (#8B949E), Settings (#8B949E)
3. **Create `mobile_shell_v2.html`** — mobile base template matching prototype:
   - Bottom tab bar with 6 module tabs (Canary, Owl, Fox, Bull, Rooster, Goose)
   - Same placeholder icons (colored circles)
   - Top bar with bird area (placeholder SVG) + merchant name + notification bell
4. **Reskin `dashboard.html`** — apply v2 base template, match prototype layout:
   - 4 stat cards (Revenue, Active Chirps, Transactions, Store Health)
   - Recent alerts table (8 rows)
   - Activity timeline (6 entries)
5. **Reskin `companion/today.html`** — apply mobile shell, match prototype:
   - Hero bird section (placeholder)
   - Greeting + chirp count
   - 3 action cards + scroll hint

**Output:** All existing pages render with v2.0 design system. No new features yet. Just reskinned.

**Qwen can do 100% of this.** It's CSS + HTML templating. No business logic.

### Phase 2: New Pages (Qwen templates + Jeremy routes)
**Goal:** Add pages that exist in the v2.0 prototype but don't exist as templates yet.

**New templates needed:**

| Page | Template Path | Route | Blueprint |
|---|---|---|---|
| Chirps Management | `templates/chirps.html` | `GET /chirps` | `chirp_wired.py` |
| Transactions List | `templates/transactions.html` | `GET /transactions` | new or `alerts_wired.py` |
| Fox Cases (kanban) | `templates/fox/cases.html` | `GET /fox/cases` | `fox_wired.py` |
| Employees Grid | `templates/employees.html` | `GET /employees` | `employees_wired.py` |
| Settings (4 tabs) | `templates/settings_v2.html` | `GET /settings` | new `settings_wired.py` |
| Chirp Config (mobile) | `canary/templates/companion/chirp_config.html` | `GET /companion/chirps` | `chirp_wired.py` |
| Module Skeletons ×5 | `canary/templates/companion/module_{name}.html` | `GET /companion/{module}` | `companion_wired.py` |

**Qwen writes the template HTML** (copy structure from the v2.0 prototypes — they're the source of truth). **Jeremy wires the routes** (add Flask `@app.route` decorators + pass data from blueprints to templates).

**Settings v2 has 4 tabs — each is its own partial:**
- `settings/general.html` — store profile, vocab pack selector
- `settings/chirp_rules.html` — full editor (thresholds, severities, 26 rules by category)
- `settings/notifications.html` — channel toggles, quiet hours
- `settings/integrations.html` — Square connected, Camera/QuickBooks/Xero status

### Phase 3: Wire to Data (Jeremy — surgical)
**Goal:** Every page shows real data from the database. No more hardcoded HTML.

**API endpoints to wire (mapped in Punch List v2.0 Section 3):**

**Desktop endpoints (Jeremy):**
```
GET  /api/stats                          → dashboard stat cards
GET  /api/alerts?limit=8                 → dashboard recent alerts
GET  /api/activity?limit=6               → dashboard activity timeline
GET  /chirp/list?category=&severity=     → chirps management table
POST /chirp/{id}/resolve                 → resolve chirp action
GET  /fox/cases                          → kanban board
PATCH /fox/cases/{id}                    → move card (status change)
GET  /employees/list                     → employee cards
GET  /employees/{id}/risk                → risk scores
GET/PUT /settings/general                → general tab
GET/PUT /chirp/rules                     → chirp rules tab
GET/PUT /settings/notifications          → notifications tab
GET  /settings/integrations              → integrations tab
GET  /admin/audit-log                    → audit log
```

**Mobile endpoints (Jeremy):**
```
GET  /companion/api/today                → greeting + chirp count
GET  /companion/api/health               → hero bird health state
GET  /companion/api/alerts/recent        → hero chirp banner
GET  /companion/api/actions              → action cards
GET  /chirp/categories                   → chirp config categories
GET  /chirp/rules                        → chirp rules list
PATCH /chirp/rules/{id}                  → toggle on/off
POST /companion/wizard/open-store        → wizard 1
POST /companion/wizard/count-drawer      → wizard 2
POST /companion/wizard/resolve-alert     → wizard 3
POST /companion/wizard/shortage          → wizard 4
```

**Many of these endpoints already exist in the wired blueprints.** Jeremy's job is:
1. Verify they return the data the templates need
2. Add any missing fields (e.g., health calculation → chirp wave color mapping)
3. Add any missing routes (e.g., `/api/stats` aggregate endpoint)
4. Wire Jinja2 context: `return render_template('chirps.html', chirps=chirps, filters=filters)`

### Phase 4: Seed Data (Jeremy)
**Goal:** When Jeffe opens localhost, there's something to look at.

**Seed script:** `canary/seeds/demo_seed.py`
- Merchant: "Sunrise Coffee" (coffee shop vocabulary)
- 30+ transactions (mix of cash, card, refunds)
- 8 active chirps (spread across severity levels: 2 critical, 3 warning, 3 info)
- 3 Fox cases (1 new, 1 in-progress, 1 resolved)
- 6 employees with varying risk scores
- 2 days of cash drawer shifts
- 10+ audit log entries
- Chirp rules: all 26 loaded from `LocalePacks/en-US.json` config

**Run:** `make seed` or `python -m canary.seeds.demo_seed`

---

## 4. What to Skip (for now)

| Item | Reason |
|---|---|
| Mascot icons | Art still iterating with Jeffe. Use colored circles as placeholders. |
| Hero bird SVG with animated chirp waves | Art deliverable. Use static placeholder. |
| React/Next.js migration | Flask+Jinja2 first. React comes after we validate the UX. |
| Real Square API data | Use seed data. Production Square integration is B-070. |
| Authentication | Skip login for now. Hardcode merchant context for demo. |
| SSE/WebSocket real-time | Later. Use manual refresh for now. |
| Responsive breakpoints | Desktop is desktop, mobile is mobile. Don't combine. |
| Wizard form validation | Show the flow. Validate later. |

---

## 5. File Organization

```
Canary/
├── app.py                          # main Flask app (exists — don't rewrite)
├── canary/
│   ├── blueprints/                 # all *_wired.py files (exist)
│   │   └── settings_wired.py       # NEW — 4-tab settings
│   ├── seeds/
│   │   └── demo_seed.py            # NEW — seed data
│   └── templates/
│       └── companion/              # mobile templates (exists + new)
│           ├── mobile_shell_v2.html    # NEW — v2 base
│           ├── today_v2.html           # NEW — reskinned today's view
│           ├── chirp_config.html       # NEW — chirp config page
│           ├── wizard/                 # NEW — 4 wizard flows
│           └── modules/                # NEW — 5 skeleton pages
├── templates/                      # desktop templates (exists + new)
│   ├── base_v2.html                # NEW — v2 base
│   ├── partials/
│   │   └── sidebar_v2.html         # NEW — 240px sidebar
│   ├── dashboard_v2.html           # NEW — reskinned dashboard
│   ├── chirps.html                 # NEW
│   ├── transactions.html           # NEW
│   ├── fox/cases.html              # NEW
│   ├── employees.html              # NEW
│   ├── settings_v2.html            # NEW — 4-tab container
│   └── settings/
│       ├── general.html            # NEW
│       ├── chirp_rules.html        # NEW
│       ├── notifications.html      # NEW
│       └── integrations.html       # NEW
├── static/
│   ├── css/canary-v2.css           # NEW — design system v3.0 tokens
│   └── img/                        # icon placeholders (until Art delivers)
└── Makefile                        # add `make seed` target
```

---

## 6. Acceptance Criteria

| # | Criteria | Verified by |
|---|---|---|
| AC-1 | `make run` starts Flask, opens in browser at localhost:5000 | Jeremy |
| AC-2 | Desktop: sidebar navigates to all 8 pages without errors | Jim |
| AC-3 | Desktop: dashboard shows 4 stat cards with seed data values | Jim |
| AC-4 | Desktop: chirps table shows 8+ rows with filter dropdowns | Jim |
| AC-5 | Desktop: Fox kanban shows 3 cases across columns | Jim |
| AC-6 | Desktop: employees grid shows 6 cards with risk indicators | Jim |
| AC-7 | Desktop: settings 4 tabs switch and display content | Jim |
| AC-8 | Desktop: audit log shows 10+ entries | Jim |
| AC-9 | Mobile: today's view shows greeting, bird placeholder, 3 action cards | Jim |
| AC-10 | Mobile: chirp config shows 8 categories with toggles | Jim |
| AC-11 | Mobile: all 4 wizards navigate step-by-step to summary card | Jim |
| AC-12 | Mobile: 6 tab bar icons navigate to correct screens | Jim |
| AC-13 | All pages render in dark theme (#0D1117 background) | Art |
| AC-14 | No JavaScript console errors on any page | Jim |
| AC-15 | `make seed` populates demo data in < 30 seconds | Jeremy |
| AC-16 | Coffee shop vocabulary used throughout (no generic terms) | Jim |

---

## 7. Task Routing

| Task | Agent | Tool | Est. Time |
|---|---|---|---|
| Phase 1: CSS + base templates | Qwen | Local Qwen 3 | 2-3 hours |
| Phase 2: New page templates | Qwen | Local Qwen 3 | 2-3 hours |
| Phase 2: Flask routes for new pages | Jeremy | Claude | 1-2 hours |
| Phase 3: Wire endpoints to templates | Jeremy | Claude | 3-4 hours |
| Phase 4: Seed data script | Jeremy | Claude | 1-2 hours |
| QA: All acceptance criteria | Jim | Manual | 1-2 hours |
| Design review: visual check | Art | Manual | 30 min |

**Total estimated:** 1–2 working days (Qwen parallel with Jeremy)

---

## 8. Dependencies

| Dependency | Status | Impact if missing |
|---|---|---|
| Flask app runs locally | ✅ Exists | Blocker — nothing works |
| Wired blueprints | ✅ 10 exist | Most data endpoints ready |
| DB schema + migrations | ✅ Exist | Tables ready for seed data |
| v2.0 prototype HTML files | ✅ On disk | Visual source of truth |
| Punch list v2.0 Section 3 | ✅ On disk | API endpoint map |
| Mascot icons | ❌ Pending (Art) | Not a blocker — use placeholders |
| Hero bird SVG | ✅ On disk | Use static version for now |
| Square API credentials | ⚠️ B-070 in progress | Not needed — seed data covers it |

---

## 9. Reference Files

| File | Path | What Jeremy/Qwen needs from it |
|---|---|---|
| Mobile prototype v2.0 | `_ALX/WorkOrders/output/Art/Canary_Mobile_Prototype_v2.0.html` | Visual source of truth — every screen's HTML structure |
| Desktop prototype v2.0 | `_ALX/WorkOrders/output/Art/Canary_Desktop_Admin_v2.0.html` | Visual source of truth — layout, tables, sidebar |
| Punch List v2.0 | `_ALX/WorkOrders/output/Art/Frontend_PunchList_v2.0.md` | Section 3: every UI element → API endpoint → blueprint → DB table |
| Coding Standards | `_ALX/WorkOrders/output/Condor/Square_TSP_CodingStandards_v1.0.md` | Code style rules |
| Locale Pack | `_ALX/WorkOrders/output/Triangulation/LocalePacks/en-US.json` | Coffee shop vocabulary terms |
| Token Registry | `_ALX/WorkOrders/output/Condor/B068_TokenRegistry_v1.0.md` | String resolution spec |
| Chirp Config PRD | `_ALX/WorkOrders/PRD_ChirpConfig_APIGateway_v1.0.md` | 26 chirp rules, categories, threshold ranges |
| Brand Guide v3 | `Canary/brand/BRAND_GUIDE_v3.html` | Color tokens, font rules |
| Design System v3.0 | Embedded in prototype CSS | CSS custom properties — extract from v2.0 HTML |

---

## 10. North Star Check

> "We don't want to add to the stress. We want to ease it."

This work order builds the thing the merchant sees. Every screen should reduce cognitive load. If Jeremy or Qwen adds a page and it feels cluttered, confusing, or requires explanation — rewrite it.

The merchant opens the app, sees their store health, taps an alert, resolves it in 3 steps, and goes back to making coffee. That's it.

---

*Filed by ALX · March 1, 2026 · Routes to Jeremy (primary), Qwen (boilerplate)*
