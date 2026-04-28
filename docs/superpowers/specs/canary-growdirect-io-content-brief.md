# canary.growdirect.io — Content Brief

**Thesis:** The public splash already establishes platform positioning and API
footprint. The deeper product site earns its keep by turning an authorized VAR's
first look into a conviction — converting "I see what this does" into "I know
exactly how to deploy it." Every page beyond the splash serves that job, not general
awareness.

**Version:** 2026-04-28  
**Audience:** Authorized RapidPOS VARs, Counterpoint channel prospects, technical
evaluators

---

## 1. Purpose

`canary.growdirect.io` is a product information site, not a consumer marketing site.
Three audiences, in priority order:

| Audience | Job to be done | Access tier |
|---|---|---|
| RapidPOS VARs | Understand the deployment model, see the product working, get the technical brief | Gated (authorized partners) |
| Counterpoint channel prospects | Confirm fit before requesting a demo | Public (product overview only) |
| Internal / GrowDirect agents | Source of truth on what the live prototype does | Open |

The site exists on the **public→gated spectrum**: the splash (already live) is open
to anyone. Feature detail and integration reference belong behind a lightweight gate
(email + company, no friction account creation) once content exists to justify one.

---

## 2. What to Show vs. What to Gate

The existing splash covers the public surface well. It should not be touched.

| Layer | Content | Gate? |
|---|---|---|
| **Splash (live)** | Platform positioning · 4 pillars · 5 API endpoints · 27 event catalog · RapidPOS partner band | Open |
| **Feature Overview** | Annotated screenshots of each major screen · what each module does in plain terms | Open — this is the evaluation content prospects need before asking for a demo |
| **Deployment Guide** | VAR onboarding steps · health check setup · Counterpoint connection model | Gated — for authorized RapidPOS VARs |
| **Integration Reference** | Full event catalog details · canonical data model summary · ingest payload structure | Gated — for technical buyers |
| **Release Notes / Changelog** | What shipped recently, what's coming in Phase 2 | Gated — internal + partner visibility |

Do not gate the feature overview. The product is not mature enough for a wall to do
useful qualification work — it will just kill inbound interest.

---

## 3. Page Map

Proposed site structure, mapped to live app screens and routes.

| Page | URL | Maps to | Gate? |
|---|---|---|---|
| Home / Splash | `/` | `templates/marketing/splash.html` | Open |
| Dashboard | `/product/dashboard` | `/home` (route: `app_dashboard`) | Open |
| Detection & Alerts | `/product/detection` | `/chirps` (route: `app_chirps`) + `/alert/<id>` | Open |
| Case Management | `/product/cases` | Vault tab in `/chirps` + `/case/<id>` | Open |
| Analytics Search | `/product/search` | `/owl` (route: `app_owl`) | Open |
| Transactions | `/product/transactions` | `/transactions` + `/txn/<id>` | Open |
| Health Reports | `/product/reports` | `/reports` (route: `app_reports`) | Open |
| Detection Rules | `/product/rules` | `/rule/<rule_id>` (route: `app_rule_editor`) | Open |
| VAR Deployment Guide | `/partners/deploy` | Onboarding flow: `/welcome` + `/connect` | **Gated** |
| Integration Reference | `/partners/api` | SDD: `webhook-pipeline.md`, `chirp.md` | **Gated** |

Pages not to build: ops console (`/admin/*`), pipeline trace (`/api/trace/*`),
audit log (`/admin/audit-log`), Square OAuth flow, dev-only endpoints. These are
internal tooling with no external audience.

---

## 4. Content Per Section

### 4.1 Dashboard (`/product/dashboard`)

**What the screen does:**  
The merchant home screen. Shows a 30-day trend chart (sales, refunds, alerts),
a four-tile KPI summary (transactions, refunds, voids, alert count), a per-employee
transaction breakdown, best-selling products, tender analysis, and a pipeline status
bar (ingestion → sales data → metrics → latest report). Alert-rule grid tiles link
directly to filtered alert feeds. Tapping any KPI tile drills to the analytics search
view.

**What to show on the product site:**  
- Annotated screenshot or screen recording: name each section, explain what
  the data means in LP terms
- One-sentence summary: "Everything that happened in your store this month,
  in one screen — from raw transaction volume to which detection rules fired and
  how often."
- Callout: the 30-day trend chart and alert-density heatmap are built from real
  POS data, not sampled estimates

---

### 4.2 Detection & Alerts (`/product/detection`)

**What the screen does:**  
Two-panel view: Alerts tab and Vault tab. Alerts tab shows detection rule firings
sorted by severity (critical → high → medium → low), with tiered display caps that
surface the most actionable items first (10 critical, 8 high, 4 medium). Each alert
card shows rule name, severity badge, employee, timestamp, and amount. Tapping an
alert opens a full detail view: rule name, description, severity, location, source
transaction link, and action buttons (dismiss, escalate, open case). Inline rule
drawer lets the merchant adjust rule thresholds without navigating to settings.

**What to show on the product site:**  
- Severity triage model: explain the tiered display logic — not a firehose
- Alert detail screenshot: show what a fired rule looks like with full context
- Rule examples (plain-English names, not IDs): Late No-Sale, Excessive Voids,
  Discount Ceiling Breach, Refund Without Receipt, Large Refund, Post-Void Chain
- Stat: 37 detection rules in the current catalog, extending to 62+ for
  Counterpoint-specific rule families

---

### 4.3 Case Management (`/product/cases`)

**What the screen does:**  
Vault tab in the same view as Alerts. Cases displayed as kanban-style cards
grouped by status: open, investigating, pending review, escalated, closed,
referred to law enforcement. Each case card shows case number, title, priority,
status, and last-updated time. Tapping a case opens a full detail view: case
header (priority, status, title, case number), description, subjects list,
timeline (append-only audit log), evidence attachments, and lifecycle action
buttons (escalate, close, investigate, refer). Evidence is stored with a
cryptographic hash chain — each record is linked to the previous one, making
the chain tamper-evident.

**What to show on the product site:**  
- Screenshot of the Vault kanban with a case in "escalated" state
- Highlight the hash chain: "Evidence attached to a case can't be altered
  retroactively — the record is signed at write time and chained to every
  prior entry."
- Status lifecycle diagram: Open → Investigating → Pending Review → Escalated
  → Closed / Referred

---

### 4.4 Analytics Search (`/product/search`)

**What the screen does:**  
A natural-language search surface over the store's data. The Risk Dictionary
provides a curated set of starting queries grouped by risk category (discount
abuse, refund patterns, void behavior, cash handling, employee exceptions).
Tapping a dictionary tile executes a pre-built analytical query. Results include
aggregated counts, transaction breakdowns, and employee-level data. Breadcrumb
trail shows the drill path. The same surface backs the dashboard KPI tile
drill-downs.

**What to show on the product site:**  
- Screenshot: Risk Dictionary grid with a fired query result
- Explain the Risk Dictionary concept: "A library of LP-relevant questions,
  pre-built and categorized. One tap runs the query against live data."
- Sample questions from the dictionary (plain English):
  - "Show me voids by employee this month"
  - "Which employees had the most discounts applied?"
  - "Refunds with no receipt in the last 30 days"

---

### 4.5 Transactions (`/product/transactions`)

**What the screen does:**  
A day-by-day transaction log showing date, count, and total revenue for the
trailing 90 days. Tapping a day expands to individual transaction records.
Tapping a transaction opens a full detail view: type badge (SALE / REFUND /
VOID / NO_SALE), amount, timestamp, employee, location, entry method (card
present / keyed / contactless), tender breakdown, and line items. Voided and
refunded transactions are color-coded. An EJ Spine view shows the complete
canonical event record with hash and source fields — the unambiguous audit
trail for any transaction under review.

**What to show on the product site:**  
- Screenshot: transaction list with the detail drawer open on a voided transaction
- EJ Spine callout: "Every transaction carries a tamper-evident electronic journal
  record. Useful when you're building a case and need to prove exactly what happened."

---

### 4.6 Health Reports (`/product/reports`)

**What the screen does:**  
A merchant-facing LP health report. A score ring shows an overall heartbeat score
(0–100) with a band classification (Healthy / Watch / Concern / Critical). Below:
KPI grid (score, alerts, findings, sessions), alert category gauges, top-priority
finding highlighted, findings list with severity and recommended actions, assessments
across three dimensions (LP, Ops, Analytics), and a trajectory sentence. Reports
are generated by the AI analysis engine from the aggregated metrics data.

**What to show on the product site:**  
- Screenshot: report with a score ring, findings section, and one recommendation visible
- Explain the score: "A composite of alert volume, severity distribution, and how
  many findings have been acted on — updated each time you run a new analysis."
- Distinguish from a dashboard: "The dashboard shows what's happening now.
  The Health Report interprets it — patterns, trajectory, what to prioritize."

---

### 4.7 Detection Rules (`/product/rules`)

**What the screen does:**  
Per-rule configuration screen. Shows rule name, ID, description, severity, and
category. Toggle to enable/disable. Threshold controls: sensitivity presets
(Low / Medium / High) and merchant-specific overrides. Rule behavioral summary
explains what triggers the rule and at what value. Reset to default available.
Changes save immediately. Accessible from the Settings screen (Rules tab) and
via inline drawer from the Alerts view.

**What to show on the product site:**  
- Screenshot: rule editor for one rule (e.g., Large Refund) with threshold visible
- Brief copy: "Every detection rule is individually configurable — adjust thresholds
  to match your store's normal operations without disabling the rule."
- Table: rule categories and example rules (no internal IDs)

| Category | Example rules |
|---|---|
| Refund exceptions | Large refund, refund without receipt, refund-to-different-card |
| Void patterns | Excessive voids, post-void chain, supervisor override |
| Discount abuse | Discount ceiling breach, manual price override frequency |
| Cash handling | No-sale drawer open, drawer shortage, unbalanced close |
| Employee behavior | Late clock-out, multiple tender types, return abuse |

---

### 4.8 VAR Deployment Guide (gated — `/partners/deploy`)

**Audience:** Authorized RapidPOS VARs doing a customer deployment.

**Content:**
- Prerequisites: Counterpoint version, API key provisioning, network requirements
- Onboarding flow walkthrough (maps to `/welcome` and `/connect` screens)
- Health check: what it does, how long it takes, what "connected" means
- Lookback configuration: what the 7/30/90-day window controls
- Merchant reset workflow for demo environments
- First 30 days: what data populates when, when detection rules start firing

---

### 4.9 Integration Reference (gated — `/partners/api`)

**Audience:** Technical buyers, integration developers.

**Content:**
- Canonical event model: the 6 core fields every ingest payload carries
- 27 registered event types with classification (transaction, payment, inventory, employee, drawer, loyalty)
- 5 REST endpoints with auth model
- Ingest pipeline stages: receive → seal → parse → detect → alert
- Tamper-evidence design: SHA-256 hash on arrival, Merkle batch commitment
- Multi-POS note: the canonical model is POS-agnostic; Counterpoint is the Phase 1 source

---

## 5. What to Omit

The following exist in the app but have no place on an external product site:

| What | Why omit |
|---|---|
| Ops console (`/admin/*`) | Internal tooling — user management, config health, audit log |
| Pipeline trace (`/api/trace/<event_id>`) | Dev observability only |
| Square OAuth flow | Deprecated POS path; not relevant to Counterpoint deployment |
| Raw row counts and metrics observability | Dashboard-internal state; not meaningful to evaluators |
| Team/employee risk scoring detail | Sensitive operational data; LP workflow, not product demo |
| MCP server mesh (12 servers) | Architecture detail for internal documentation, not prospect-facing |
| Agent tooling (ALX) | Internal to operator workflows |

---

## 6. Visual and Voice Notes

- **Palette:** The splash's forest-green Armstrong palette (`#1C3A2B` / `#F5F0E8` / `#BF8700`) should persist into all product pages for visual consistency.
- **Screenshots:** Dark-mode app UI (GitHub dark palette) against the parchment site — use framed device mockups or bordered light-shadow cards to avoid contrast clash.
- **Voice:** Direct and technical. The audience is experienced POS operators and VARs, not retail SMB owners. Skip the reassurance copy. Lead with specifics.
- **No codenames in external copy.** Detection engine, case management, analytics search, and AI analysis are the right terms. Internal module names stay internal.
