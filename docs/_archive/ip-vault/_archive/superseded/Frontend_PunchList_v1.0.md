---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Canary LP — Frontend Punch List v1.0
**Date:** March 1, 2026
**Owner:** ALX
**Reviewers:** Art (UX), Jim (QA), Jeremy (Dev)
**Prototypes on disk:**
- Mobile: `_ALX/WorkOrders/output/Art/Canary_Mobile_Prototype_v1.0.html`
- Desktop: `_ALX/WorkOrders/output/Art/Canary_Desktop_Admin_v1.0.html`

---

## 1. Two Products, One Architecture

**Mobile Companion** — the handheld app merchants use between customers. Wizard-driven, max 3 action cards, no charts, no tables. Six module tabs (Canary, Owl, Fox, Bull, Rooster, Goose). Starts with Canary (Chirps/Alerts).

**Desktop Admin Suite** — the back-office app for owners, managers, and admins. Sidebar nav, data tables, full CRUD, audit logs, settings. GitHub dark mode meets Stripe dashboard.

**Shared foundation:** Same design tokens, same API contracts, same vocabulary pack resolution. The mobile app calls the same endpoints as the desktop app — they're two projections of the same CRDM.

---

## 2. Backend Tie Points (for Jeremy/Qwen)

Every screen in both prototypes maps to real Flask blueprints and database tables. Here's the wiring:

### Mobile: Today's View
| UI Element | API Endpoint | Blueprint | DB Table(s) |
|---|---|---|---|
| Greeting + chirp count | `GET /companion/api/today` | `companion_wired.py` | alerts, merchants, users |
| Hero Chirp Banner | `GET /companion/api/alerts/recent` | `companion_wired.py` | alerts (severity, status, created_at) |
| Action Cards | `GET /companion/api/actions` | `companion_wired.py` | alerts, cash_drawer_shifts, employee_timecards |
| Health Bar | `GET /companion/api/health` | `companion_wired.py` | alerts (aggregate severity) |

### Mobile: Wizard Flows
| Wizard | API Endpoint | Blueprint | DB Write |
|---|---|---|---|
| Process 1: Open Store | `POST /companion/wizard/open-store` | `companion_wired.py` | cash_drawer_shifts (INSERT, status=OPEN) |
| Process 2: Count Drawer | `POST /companion/wizard/count-drawer` | `companion_wired.py` | cash_drawer_shifts (UPDATE status=CLOSED), cash_drawer_events (INSERT) |
| Process 3: Refund Alert | `POST /companion/wizard/resolve-alert` | `companion_wired.py` | alerts (UPDATE status), cases (INSERT if escalated) |
| Process 4: Cash Shortage | `POST /companion/wizard/shortage` | `companion_wired.py` | alerts (UPDATE), case_evidence (INSERT if photo), cases (INSERT if escalated) |

### Desktop: Dashboard
| UI Element | API Endpoint | Blueprint | DB Table(s) |
|---|---|---|---|
| Transaction count | `GET /api/stats` | `app.py` | transactions (COUNT) |
| Active chirps | `GET /api/stats` | `app.py` | alerts (COUNT WHERE status=open) |
| Revenue | `GET /api/stats` | `app.py` | transactions (SUM amount) |
| Shrink rate | `GET /api/stats` | `app.py` | alerts, transactions (computed) |
| Recent alerts table | `GET /api/alerts?limit=5` | `alerts_wired.py` | alerts JOIN transactions |

### Desktop: Chirps Management
| UI Element | API Endpoint | Blueprint | DB Table(s) |
|---|---|---|---|
| Chirps table | `GET /chirp/list` | `chirp_wired.py` | alerts (full query with filters) |
| Resolve action | `POST /chirp/{id}/resolve` | `chirp_wired.py` | alerts (UPDATE status) |
| Chirp rules config | `GET /chirp/rules` | `chirp_wired.py` | merchant_settings (chirp_rules JSON) |

### Desktop: Cases (Fox)
| UI Element | API Endpoint | Blueprint | DB Table(s) |
|---|---|---|---|
| Kanban board | `GET /fox/cases` | `fox_wired.py` | cases, subjects, case_subjects, case_evidence |
| Case detail | `GET /fox/cases/{id}` | `fox_wired.py` | cases, case_timeline, case_actions |
| Evidence chain | `GET /fox/cases/{id}/evidence` | `fox_wired.py` | case_evidence (IMMUTABLE), evidence_access_log |

### Desktop: Employees
| UI Element | API Endpoint | Blueprint | DB Table(s) |
|---|---|---|---|
| Employee table | `GET /employees/list` | `employees_wired.py` | (Square API → local cache) |
| Risk scores | `GET /employees/{id}/risk` | `employees_wired.py` | transactions, alerts (computed per employee) |
| Shift data | `GET /employees/{id}/shifts` | `employees_wired.py` | employee_timecards |

### Desktop: Audit Log
| UI Element | API Endpoint | Blueprint | DB Table(s) |
|---|---|---|---|
| Audit entries | `GET /admin/audit-log` | `admin/audit_log.html` | audit_log (IMMUTABLE — INSERT only) |

---

## 3. Art Review Checklist

Art — open both prototypes and verify:

### Mobile Prototype
- [ ] Color tokens match Brand Guide v3 exactly (ink, charcoal, card, signal-yellow, health-green/yellow/red)
- [ ] Typography: Inter body, Space Grotesk headings — sizes match Blueprint v2.0
- [ ] Canary mascot: golden body, beak, gentle bob animation, green pulse ring
- [ ] Hero chirp: health-wave animation (green → yellow → red arcs from beak)
- [ ] 6 SVG module icons match Blueprint §2.6 geometry exactly (Canary, Owl, Fox, Bull, Rooster, Goose)
- [ ] Touch targets ≥ 44×44px (bottom nav, action cards, wizard buttons)
- [ ] Max 3 action cards rule enforced
- [ ] No charts, no tables on mobile (hard design rule)
- [ ] One-number scorecards only
- [ ] Wizard progress bar updates correctly per step
- [ ] Confetti animation fires on wizard completion
- [ ] Skeleton module tabs feel consistent (icon size, messaging, layout)
- [ ] Safe area handling for notched devices (bottom nav)
- [ ] 768px+ breakpoint: bottom nav to top, 2-column action cards

### Desktop Prototype
- [ ] Sidebar 240px, color-coded module sections
- [ ] Active nav: gold border-left + gold glow background
- [ ] Tables: hover states, severity dots, badge pills
- [ ] Kanban (Fox cases): cards with severity, evidence count, assigned
- [ ] Settings tabs: General / Chirp Rules / Notifications / Integrations
- [ ] Risk score progress bars: green/yellow/red per employee
- [ ] Audit log: reverse-chronological, immutable-feeling
- [ ] Search box: gold focus border
- [ ] Notification bell: red dot indicator
- [ ] Consistent with mobile design tokens (same color palette, same dark theme)

---

## 4. Jim QA Checklist

Jim — open both prototypes and verify:

### Mobile
- [ ] All 6 bottom nav tabs switch correctly
- [ ] Hero chirp tap launches Process 4 wizard
- [ ] Peek indicator navigates to alerts list (not wizard)
- [ ] All 4 wizard flows complete end-to-end (Open Store 4 steps, Count Drawer 5, Refund Alert 5, Shortage 6)
- [ ] Back button on every wizard step returns to previous step
- [ ] Progress bar width matches current step / total steps
- [ ] Form inputs accept valid data, reject negatives
- [ ] "Back to Home" on completion returns to Today's View
- [ ] Filter chips on alerts list change active state
- [ ] Confetti triggers only on positive completions
- [ ] No dead-end screens — every tap does something
- [ ] Wizard state: can you go back after selecting a cause? Is data preserved?

### Desktop
- [ ] All sidebar nav items switch pages correctly
- [ ] Dashboard stats display correct values
- [ ] Tables have proper hover states
- [ ] Chirps table shows 8 varied rules
- [ ] Fox kanban has cards in correct columns (Open/Investigating/Review/Closed)
- [ ] Settings tabs switch: General → Chirp Rules → Notifications → Integrations
- [ ] Toggle switches on chirp rules flip states
- [ ] Audit log entries are chronologically ordered
- [ ] Skeleton pages display "Coming in Sprint 7" message
- [ ] Search box takes focus with gold border
- [ ] No JavaScript errors in console

### Cross-Product
- [ ] Same alert data appears in both mobile and desktop (cash shortage $47.50, refund pattern)
- [ ] Same employee names (Maria S., James T., Tyler R., Priya K.)
- [ ] Same location names (Main Street Café, University Ave, Downtown Express)
- [ ] Coffee shop vocabulary used consistently (Barista, Register, Café)

---

## 5. Jeremy/Qwen Build Path

### Phase 1 — React Conversion (Mobile)
1. Convert mobile prototype to React SPA (Vite + React Router)
2. Extract components: TopBar, HeroChirp, ActionCard, BottomNav, WizardOverlay, WizardStep
3. Wire to existing Flask endpoints (companion_wired.py already serves HTMX — adapt to JSON API)
4. Vocabulary pack resolution: load `en-US.json` at startup, resolve all display strings
5. Theme pack: extract CSS custom properties into `theme.json`

### Phase 2 — React Conversion (Desktop)
1. Convert desktop prototype to React SPA (same Vite project, route-based code splitting)
2. Sidebar nav component with collapsible state
3. Data table component (reusable: chirps, transactions, employees, audit log)
4. Fox kanban component
5. Settings form with tab switching

### Phase 3 — API Unification
1. Both apps hit same endpoints, different projections
2. Mobile gets simplified payloads (max 3 cards, hero chirp only)
3. Desktop gets full payloads (all records, all fields)
4. Vocabulary pack resolution happens server-side — API returns resolved strings

### Token Coverage (from Blueprint v2.0)
Jeremy: every hardcoded string in these prototypes maps to a token key in `B068_TokenRegistry_v1.0.md`. When building the React version, use `{{token.key}}` references resolved from `LocalePacks/en-US.json`. The resolved English in these prototypes IS the default fallback — if no vocab override exists, that's what displays.

---

## 6. Dependencies

| Blocker | Owner | Status |
|---|---|---|
| Vocabulary pack files (en-US.json) | Condor (B-068-C) | ON DISK |
| Token registry (B068_TokenRegistry) | Condor (B-068-B) | ON DISK |
| Chirp rules config (26 rules) | PRD_ChirpConfig_APIGateway_v1.0.md | ON DISK |
| Brand Guide v3 | Art | ON DISK |
| Flask companion blueprint | Jeremy | EXISTS (companion_wired.py) |
| Fox case management blueprint | Jeremy | EXISTS (fox_wired.py) |
| Square OAuth (Phase 1 self-auth) | Jeremy (B-070) | IN PROGRESS |

---

*Punch list delivered March 1, 2026. Prototypes on disk. Review with Art and Jim. Build path for Jeremy/Qwen. — ALX*
