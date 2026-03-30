---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Canary LP — Frontend Punch List v2.0
**Date:** March 1, 2026
**Owner:** ALX
**Reviewers:** Art (UX), Jim (QA), Jeremy (Dev)
**Prototypes on disk:**
- Mobile v2.0: `_ALX/WorkOrders/output/Art/Canary_Mobile_Prototype_v2.0.html`
- Desktop v2.0: `_ALX/WorkOrders/output/Art/Canary_Desktop_Admin_v2.0.html`
- Icon Gallery: `_ALX/WorkOrders/output/Art/module_icons.html`
- v1.0 files archived (not deleted)

---

## Changelog from v1.0

- **Hero bird replaced**: Original canary hero SVG (`canary-hero-1024.svg`) with color-coded severity chirp waves now used in both prototypes
- **Chirp waves = health indicator**: Red (critical), Yellow (warning), Green (healthy). Separate health bar REMOVED from mobile.
- **6 illustrative mascot icons built**: Owl, Fox, Bull, Rooster, Goose all rendered in the Canary hero art style (round shapes, fill+dark shade depth, dark eye with highlight). Gallery at `module_icons.html`.
- **Chirp Config page added to mobile**: View + toggle only. 8 categories, 26 chirps. "Edit on desktop" for threshold changes.
- **Module skeleton tabs fleshed out**: Hero icon + feature list for each module (mobile), icon + tagline + placeholder tables (desktop)
- **Desktop Settings**: All 4 tabs functional (General, Chirp Rules, Notifications, Integrations)
- **Action cards**: 3 visible + peek of 4th (scroll hint)
- **Wizard completion**: Clean summary card with result details. No confetti.
- **Vocabulary**: Coffee shop throughout. "Sunrise Coffee" as sample merchant.

---

## 1. Design Decisions (Locked by Jeffe — March 1, 2026)

| Decision | Choice | Rationale |
|---|---|---|
| Chirp wave colors | Color-coded by severity (red/yellow/green) | Bird IS the health indicator |
| Icon style | Illustrative hero-style mascots | All 6 modules get full character icons matching canary hero |
| Chirp Config (mobile) | View + toggle only | Edit thresholds on desktop. Mobile is glanceable control. |
| Health display | Bird chirp waves only | No separate health bar. Bird tells the whole story. |
| Action cards | 3 visible + scroll hint | Peek of 4th card visible, swipe for more |
| Wizard end state | Summary card, no confetti | Professional tone. Clean result card with check icon. |
| Module skeletons (mobile) | Hero icon + feature list | Informational, shows planned capabilities |
| Module skeletons (desktop) | Icon + tagline + placeholder tables | Matches mobile style with data table column headers |
| Desktop Settings tabs | All 4 functional | Full scaffold, not just Chirp Rules |
| Demo latency | N/A — not a demo prop | "Build the whole scaffold so we know where to focus" |
| Vocabulary pack | Coffee shop only | No cannabis in demo. Coffee + Retail are the first verticals. |

---

## 2. Two Products, One Architecture

**Mobile Companion** — the handheld app merchants use between customers. Wizard-driven, max 3 visible action cards + scroll, no charts, no tables. Six module tabs (Canary, Owl, Fox, Bull, Rooster, Goose). Canary fully built, others skeleton with feature lists.

**Desktop Admin Suite** — the back-office app for owners, managers, and admins. 240px sidebar nav, data tables, full CRUD, audit logs, settings with 4 tabs. GitHub dark mode meets Stripe dashboard.

**Shared foundation:** Same design tokens, same API contracts, same vocabulary pack resolution. Same illustrative mascot icons. Same hero bird as health indicator.

---

## 3. Backend Tie Points (for Jeremy/Qwen)

Every screen in both prototypes maps to real Flask blueprints and database tables.

### Mobile: Today's View
| UI Element | API Endpoint | Blueprint | DB Table(s) |
|---|---|---|---|
| Greeting + chirp count | `GET /companion/api/today` | `companion_wired.py` | alerts, merchants, users |
| Hero Bird (health indicator) | `GET /companion/api/health` | `companion_wired.py` | alerts (aggregate severity → chirp wave colors) |
| Hero Chirp Banner | `GET /companion/api/alerts/recent` | `companion_wired.py` | alerts (severity, status, created_at) |
| Action Cards (3+scroll) | `GET /companion/api/actions` | `companion_wired.py` | alerts, cash_drawer_shifts, employee_timecards |

### Mobile: Chirp Configuration (NEW)
| UI Element | API Endpoint | Blueprint | DB Table(s) |
|---|---|---|---|
| Category list (8 groups) | `GET /chirp/categories` | `chirp_wired.py` | merchant_settings (chirp_rules JSON) |
| Chirp rows (26 rules) | `GET /chirp/rules` | `chirp_wired.py` | merchant_settings.chirp_rules |
| Toggle on/off | `PATCH /chirp/rules/{id}` | `chirp_wired.py` | merchant_settings (UPDATE chirp_rules.enabled) |
| Detail view (read-only) | `GET /chirp/rules/{id}` | `chirp_wired.py` | merchant_settings, alert_history |

### Mobile: Wizard Flows
| Wizard | API Endpoint | Blueprint | DB Write |
|---|---|---|---|
| Process 1: Open Store | `POST /companion/wizard/open-store` | `companion_wired.py` | cash_drawer_shifts (INSERT, status=OPEN) |
| Process 2: Count Drawer | `POST /companion/wizard/count-drawer` | `companion_wired.py` | cash_drawer_shifts (UPDATE), cash_drawer_events (INSERT) |
| Process 3: Refund Alert | `POST /companion/wizard/resolve-alert` | `companion_wired.py` | alerts (UPDATE status), cases (INSERT if escalated) |
| Process 4: Cash Shortage | `POST /companion/wizard/shortage` | `companion_wired.py` | alerts (UPDATE), case_evidence (INSERT), cases (INSERT if escalated) |

### Desktop: Dashboard
| UI Element | API Endpoint | Blueprint | DB Table(s) |
|---|---|---|---|
| Today's Revenue | `GET /api/stats` | `app.py` | transactions (SUM amount) |
| Active Chirps (with bird) | `GET /api/stats` | `app.py` | alerts (COUNT WHERE status=open) + severity distribution |
| Transaction count | `GET /api/stats` | `app.py` | transactions (COUNT) |
| Store Health (bird icon) | `GET /api/stats` | `app.py` | alerts (aggregate → health %) |
| Recent alerts table | `GET /api/alerts?limit=8` | `alerts_wired.py` | alerts JOIN transactions |
| Activity timeline | `GET /api/activity?limit=6` | `app.py` | audit_log (recent entries) |

### Desktop: Chirps Management
| UI Element | API Endpoint | Blueprint | DB Table(s) |
|---|---|---|---|
| Chirps table (12+ rows) | `GET /chirp/list` | `chirp_wired.py` | alerts (full query with filters) |
| Filter bar | `GET /chirp/list?category=&severity=&status=` | `chirp_wired.py` | alerts |
| Resolve action | `POST /chirp/{id}/resolve` | `chirp_wired.py` | alerts (UPDATE status) |
| Detail panel (slide-in) | `GET /chirp/{id}` | `chirp_wired.py` | alerts, merchant_settings, alert_history |

### Desktop: Cases (Fox)
| UI Element | API Endpoint | Blueprint | DB Table(s) |
|---|---|---|---|
| Kanban board (4 cols) | `GET /fox/cases` | `fox_wired.py` | cases, subjects, case_subjects, case_evidence |
| Case detail | `GET /fox/cases/{id}` | `fox_wired.py` | cases, case_timeline, case_actions |
| Evidence chain | `GET /fox/cases/{id}/evidence` | `fox_wired.py` | case_evidence (IMMUTABLE) |
| Move card (status change) | `PATCH /fox/cases/{id}` | `fox_wired.py` | cases (UPDATE status) |

### Desktop: Employees
| UI Element | API Endpoint | Blueprint | DB Table(s) |
|---|---|---|---|
| Employee card grid | `GET /employees/list` | `employees_wired.py` | (Square API → local cache) |
| Risk scores | `GET /employees/{id}/risk` | `employees_wired.py` | transactions, alerts (computed) |
| Shift data | `GET /employees/{id}/shifts` | `employees_wired.py` | employee_timecards |
| Detail panel | `GET /employees/{id}` | `employees_wired.py` | all employee tables |

### Desktop: Settings (4 tabs)
| Tab | API Endpoint | Blueprint | DB Table(s) |
|---|---|---|---|
| General (store profile) | `GET/PUT /settings/general` | `settings_wired.py` | merchants |
| Vocab pack selector | `GET /settings/vocabulary` | `settings_wired.py` | merchant_settings.vocabulary_pack |
| Chirp Rules (full editor) | `GET/PUT /chirp/rules` | `chirp_wired.py` | merchant_settings.chirp_rules |
| Notifications | `GET/PUT /settings/notifications` | `settings_wired.py` | merchant_settings.notification_prefs |
| Integrations | `GET /settings/integrations` | `settings_wired.py` | merchant_integrations |

### Desktop: Audit Log
| UI Element | API Endpoint | Blueprint | DB Table(s) |
|---|---|---|---|
| Audit entries (20 rows) | `GET /admin/audit-log` | `admin/audit_log.html` | audit_log (IMMUTABLE — INSERT only) |
| Export CSV | `GET /admin/audit-log/export` | `admin/audit_log.html` | audit_log |

---

## 4. Art Review Checklist (v2.0)

Art — open both v2.0 prototypes and verify:

### Mobile (14 items + 4 new)
- [ ] Hero bird renders at 120px in top bar with color-coded chirp waves (red/yellow/green)
- [ ] Bird chirp waves correctly represent store health — no separate health bar
- [ ] All 6 tab icons are illustrative mascots matching hero bird art style
- [ ] Tab bar highlights active tab with module color underline + label
- [ ] Action cards: 3 fully visible + peek of 4th, horizontal scroll works
- [ ] Chirp Config page: 8 collapsible categories, toggle switches, "Edit on desktop" note
- [ ] Chirp detail view shows read-only threshold, schedule, last triggered
- [ ] 5 skeleton module tabs show hero icon + feature list
- [ ] Wizard summary cards: clean check icon + result details, no confetti
- [ ] Wizard progress indicators show current step
- [ ] Alert list filter chips work (All/Critical/Warning/Info)
- [ ] Dark theme colors match design system v3.0 tokens
- [ ] Font pairing: Inter body + Space Grotesk headings
- [ ] Spacing consistent with 4px scale
- [ ] Coffee shop vocabulary throughout (barista, register, café)
- [ ] Touch targets ≥ 44px
- [ ] All screens accessible from bottom tab bar
- [ ] Transitions between screens smooth (200ms)

### Desktop (10 items + 5 new)
- [ ] Sidebar shows all 6 modules with illustrative mascot icons (24px)
- [ ] Active sidebar item has module-color left border
- [ ] Dashboard: 4 stat cards with bird icon on Store Health card
- [ ] Chirps Management: filter bar + 12-row table + detail panel
- [ ] Fox Cases: 4-column kanban with severity badges
- [ ] Employees: card grid with risk scores (color-coded)
- [ ] Settings: all 4 tabs functional (General, Chirp Rules, Notifications, Integrations)
- [ ] General tab: vocabulary pack selector shows coffee shop terms
- [ ] Chirp Rules tab: threshold inputs, severity dropdowns, 26 rules grouped by category
- [ ] Notifications tab: channel toggles, alert routing, quiet hours
- [ ] Integrations tab: Square connected, Camera/QuickBooks/Xero status cards
- [ ] Audit Log: 20 rows, export button
- [ ] Module skeleton pages: hero icon + tagline + placeholder tables
- [ ] Hover states on tables and cards
- [ ] Font sizes readable at standard desktop zoom

---

## 5. Jim QA Checklist (v2.0)

Jim — functional flow testing:

### Mobile (12 items + 4 new)
- [ ] Today's View loads with bird health indicator
- [ ] Tap action card → wizard launches correctly
- [ ] Open Store wizard: 4 steps, correct progression, summary card at end
- [ ] Count Drawer wizard: 5 steps, bill/coin grids functional, summary with variance
- [ ] Refund Alert wizard: 5 steps, action selection works, summary card
- [ ] Cash Shortage wizard: 6 steps, timeline + resolution, summary card
- [ ] Wizard back/forward navigation works on all 4 wizards
- [ ] Alert list: filter chips toggle correctly
- [ ] Alert tap → detail expands with investigate button
- [ ] Chirp Config: categories expand/collapse
- [ ] Chirp Config: toggles switch on/off
- [ ] Chirp Config: tap row → detail view appears
- [ ] Tab navigation: all 6 tabs switch screens
- [ ] Action card scroll: swipe reveals 4th card
- [ ] Skeleton tabs display feature list content
- [ ] No JavaScript errors in console

### Desktop (11 items + 4 new)
- [ ] Sidebar navigation: all pages load on click
- [ ] Dashboard stat cards show data
- [ ] Dashboard alerts table has 8 rows
- [ ] Chirps table: filter dropdowns + search functional
- [ ] Transactions table: 15 rows render
- [ ] Fox kanban: cards display in 4 columns
- [ ] Employee cards: 6 cards with risk scores
- [ ] Settings: tab switching works between all 4 tabs
- [ ] Settings General: vocab pack selector
- [ ] Settings Chirp Rules: editable table renders
- [ ] Settings Notifications: toggles work
- [ ] Settings Integrations: status indicators display
- [ ] Audit log: 20 rows render, export button present
- [ ] Breadcrumb updates on navigation
- [ ] No JavaScript errors in console

### Cross-Product (4 items)
- [ ] Same chirp names appear in both mobile config and desktop rules
- [ ] Same color tokens used across both prototypes
- [ ] Same bird hero art style across both
- [ ] Vocabulary consistent (coffee shop terms match)

---

## 6. Jeremy/Qwen Build Path (React Migration)

### Phase 1: React Mobile Companion
- Convert v2.0 HTML prototype to React Native / Expo
- Implement all 4 wizard flows with form validation
- Wire to Flask API endpoints listed in Section 3
- Chirp Config: GET categories + rules, PATCH toggle
- Use design tokens from CSS custom properties

### Phase 2: React Desktop Admin
- Convert v2.0 HTML prototype to React (Next.js or Vite)
- Implement Settings CRUD across all 4 tabs
- Wire kanban drag-and-drop to case status API
- Implement audit log with real-time SSE streaming
- Chirp Rules full editor with threshold validation

### Phase 3: API Unification
- Shared API gateway for both clients
- Vocabulary pack resolution at API layer
- Real-time alerts via SSE (mobile) and WebSocket (desktop)
- Auth: Keycloak JWT on all endpoints

---

## 7. Dependencies

| Dependency | Owner | Status | Blocks |
|---|---|---|---|
| Illustrative mascot SVGs (6) | Art/ALX | ✅ DONE (module_icons.html) | Both prototypes |
| Canary hero bird SVG | Art/ALX | ✅ DONE (canary-hero-1024.svg) | Both prototypes |
| Chirp Rules PRD (26 rules) | Condor | ✅ DONE (PRD_ChirpConfig) | Chirp Config page |
| Vocab pack JSON (coffee) | Condor | ✅ DONE (en-US.json) | Settings vocab selector |
| Token Registry | Condor | ✅ DONE (B068_TokenRegistry) | String resolution |
| Brand Guide v3 | Art | ✅ DONE | Color/font validation |
| Square API integration | Jeremy | IN PROGRESS (B-070) | Employee data, transactions |
| Flask blueprint wiring | Jeremy | PENDING | All API endpoints |
