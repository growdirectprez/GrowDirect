---
type: spec
title: Canary Go — Canonical Site Map (v2)
status: draft
date: 2026-05-04
source: 2026-05-04-canary-go-screen-scenario-map.md × 2026-05-04-counterpoint-canary-ux-crosswalk.md × 2026-05-04-canary-go-l4-gap-delta.md × 2026-05-03-canary-go-ui-wave-plan.md
gro: TBD
purpose: Single canonical reference for Canary Go's complete URL hierarchy, navigation structure, user roles per screen, wave assignment, and Counterpoint equivalent. v2 adds: OTB, Distribution Recommendations, AR Aging, Demand Forecast, Device Management, Agents Dashboard, and DevOps module from L4 gap delta + founder direction.
---

# Canary Go — Canonical Site Map (v2)

**Governing thesis:** Canary Go organizes its ~110 screens into twelve navigable sections. The left sidebar is role-scoped — an LP Investigator sees Surveillance, Investigations, Customers; a Buyer sees Inventory, Purchasing, Finance, Merchandising; a Manager sees store-ops sections; an ADM sees everything including Devices, Agents, and DevOps. This document is the authoritative URL hierarchy behind that sidebar.

**Notation:**

| Key | Meaning |
|---|---|
| O | Original wave plan screen |
| N | New — added from Counterpoint crosswalk |
| L4 | New — added from CRB L4 gap delta |
| FD | New — founder direction (this session) |
| † | Tab or panel on a parent screen (not a separate route) |
| [W1]–[W5] | Wave assignment |
| [ADM] | Admin section — separate from sidebar nav |

---

## Navigation Architecture

```
Left sidebar (role-scoped):
├── Dashboard                           /
│
├── Surveillance ─────────────────── (LP, MGR)
│   ├── Alerts                          /alerts
│   ├── Live Feed (Chirps)              /chirps
│   ├── Transactions                    /transactions
│   └── Detection Rules                 /rules
│
├── Investigations ──────────────────── (LP, MGR)
│   ├── Cases                           /cases/hawk
│   ├── Analytics                       /cases/hawk/analytics
│   └── Patterns                        /cases/hawk/patterns
│
├── Customers ───────────────────────── (LP, MGR)
│   └── Customer Lookup                 /customers
│
├── Inventory ───────────────────────── (MGR, BYR, LP)
│   ├── Items                           /items
│   ├── Transfers                       /transfers
│   ├── Physical Counts                 /inventory/count
│   └── Adjustments                     /inventory/adjustments
│
├── Purchasing ──────────────────────── (BYR, RCV, MGR)
│   ├── Vendors                         /vendors
│   ├── Suggested Orders                /orders/suggested
│   ├── Distribution Recommendations    /orders/distribution        ← L4
│   ├── Purchase Orders                 /orders
│   ├── Open-to-Buy                     /otb                        ← L4
│   └── Receiving                       /receiving
│
├── Finance ─────────────────────────── (MGR, ADM)
│   ├── EOD Summary                     /reports/eod
│   ├── Finance Report                  /reports/finance
│   ├── Payments                        /reports/payments
│   ├── Tax                             /reports/tax
│   ├── AR Aging                        /reports/ar-aging           ← L4
│   └── Gift Cards                      /reports/gift-cards         ← L4
│
├── Merchandising ───────────────────── (BYR, MGR)
│   ├── Promotion Calendar              /promotions
│   ├── Markdowns                       /markdowns                  ← L4
│   ├── Range Analysis                  /reports/range
│   ├── Demand Forecast                 /reports/forecast           ← L4
│   ├── Price History                   /reports/price-history
│   ├── Flash Sales                     /reports/flash
│   ├── Markdown Effectiveness          /reports/markdowns
│   └── Grid Report                     /reports/grid
│
├── Employees ───────────────────────── (MGR, ADM, EMP)
│   ├── Timecards                       /timecards
│   ├── Time Clock                      /timeclock
│   └── Payroll Export                  /timecards/export
│
├── Devices ─────────────────────────── (ADM, MGR)               ← FD
│   ├── Station Registry                /devices
│   ├── Station Detail                  /devices/:id
│   └── Device Health                   /devices/health
│
├── Agents ──────────────────────────── (ADM)                    ← FD
│   ├── Agent Activity Dashboard        /agents
│   ├── Junction Map                    /agents/junctions
│   ├── Agent Detail                    /agents/:id
│   └── Agent Config                    /agents/config
│
├── Operations (W) ──────────────────── (LP, MGR — Wave 5)
│   ├── All Exceptions                  /exceptions
│   ├── Cases                           /cases
│   └── Case Reports                    /reports/cases
│
└── Settings ────────────────────────── (ADM, MGR)
    ├── Alert Routing                   /settings/alert-routing
    ├── Training Mode                   /settings/training-mode
    ├── Allow-Lists (4)                 /settings/allowlist/*
    ├── Store Config (LP thresholds)    /settings/store/*
    ├── Station & Device Config         /settings/store/stations    ← L4/FD
    ├── Payment / Tender Classification /settings/payment           ← L4
    ├── Loyalty Programs                /settings/loyalty/programs
    ├── Price Rules                     /settings/pricing/rules
    └── Catalog Config                  /settings/catalog

Admin (top-bar link, not sidebar):
├── Users                               /admin/users
├── Audit Log                           /admin/audit
├── Config Health                       /admin/config
├── Tenant Management                   /admin/tenants              ← FD
├── Tenant Detail                       /admin/tenants/:id          ← FD
└── DevOps                              /admin/devops               ← FD
    ├── Service Health                  /admin/devops/health
    ├── Deployment Log                  /admin/devops/deployments
    └── Infrastructure                  /admin/devops/infra
```

---

## Screen Inventory

### Admin (Cross-Wave)

| URL | Screen Title | Roles | Wave | Origin | CP Equivalent |
|---|---|---|---|---|---|
| `/admin/users` | Users List | ADM | Cross | O | `frmsecuritycodes` + user records |
| `/admin/users/:id` | User Detail + Role Assignment | ADM | Cross | O | User maintenance + security code assignment |
| `/admin/audit` | Audit Log | ADM, LP | Cross | O | None |
| `/admin/config` | Config Health (adapter status, backfill, sync) | ADM | Cross | O | None |
| `/admin/tenants` | Tenant Management | ADM | Cross | FD | None |
| `/admin/tenants/:id` | Tenant Detail (LP rollout phase, adapter, backfill) | ADM | Cross | FD | None |
| `/admin/devops/health` | Service Health Dashboard | ADM | Cross | FD | None |
| `/admin/devops/deployments` | Deployment Log | ADM | Cross | FD | None |
| `/admin/devops/infra` | Infrastructure Overview (GCP resources) | ADM | Cross | FD | None |

---

### Dashboard

| URL | Screen Title | Roles | Wave | Origin | CP Equivalent |
|---|---|---|---|---|---|
| `/` | Dashboard | All | Cross | O | None |

---

### Surveillance

| URL | Screen Title | Roles | Wave | Origin | CP Equivalent |
|---|---|---|---|---|---|
| `/alerts` | Alert List | LP, MGR | W1 | O | None |
| `/alerts/:id` | Alert Detail + Acknowledge | LP, MGR | W1 | O | None |
| `/chirps` | Live Transaction Feed | LP, MGR | W1 | O | Z-Tape (post-close only) |
| `/chirps/:id` | Chirp Detail | LP | W1 | O | `frmpstickethistory` |
| `/transactions` | Transaction List | LP, MGR | W2 | O | `frmpstickethistory` |
| `/transactions/:id` | Transaction Detail | LP, MGR | W2 | O | Ticket History detail |
| `/transactions/:id/proof` | Audit Proof Verification | LP, ADM | W2 | O | None |
| `/rules` | Detection Rules List | LP, ADM | W1 | O | None |
| `/rules/:id` | Rule Detail + Enable / Dry Run / Parameters | LP, ADM | W1 | O+L4 | None |

---

### Investigations

| URL | Screen Title | Roles | Wave | Origin | CP Equivalent |
|---|---|---|---|---|---|
| `/cases/hawk` | Case List (Hawk) | LP, MGR | W1 | O | None |
| `/cases/hawk/:id` | Case Detail | LP, MGR | W1 | O | None |
| `/cases/hawk/:id/evidence` | Evidence Attach | LP | W1 | O | None |
| `/cases/hawk/analytics` | Case Analytics | LP, MGR | W1 | O | None |
| `/cases/hawk/patterns` | Cross-Case Pattern View | LP | W1 | O | None |

---

### Customers

| URL | Screen Title | Roles | Wave | Origin | CP Equivalent |
|---|---|---|---|---|---|
| `/customers` | Customer Lookup | LP | W1 | O | `frmcustomers` (no risk score) |
| `/customers/:id` | Customer Detail | LP, MGR | W1 | O | `frmcustomers` A/R + Ticket History tabs |
| `/customers/:id` → Risk† | Customer Risk Score | LP | W1 | O | None |
| `/customers/:id` → Context† | Cross-Module Context | LP | W1 | O | None |
| `/customers/:id` → Commercial† | B2B Classification, Credit Posture, AR Summary | MGR | W3 | L4 | `frmaraccountsenter` |
| `/customers/:id` → Loyalty† | Loyalty Balance, Earn/Redeem History, Adj | MGR | W4 | N | `frmarloyptsadjustmentsenter` |
| `/customers/:id` → AR† | Open AR Items, Aging | MGR | W3 | N | `frmaraccountsenter` |

---

### Inventory

| URL | Screen Title | Roles | Wave | Origin | CP Equivalent |
|---|---|---|---|---|---|
| `/items` | Item Catalog Search | LP, MGR, BYR | W2 | O | `frmitems` |
| `/items/:id` | Item Detail (attrs, inventory, KPIs, pricing, replenishment†) | LP, MGR, BYR | W2 | O+L4 | `frmitems` |
| `/items/new` | Item Create | ADM, BYR | W2 | N | `frmitems` new record |
| `/items/:id/edit` | Item Edit | ADM, BYR | W2 | N | `frmitems` |
| `/transfers` | Transfer List | MGR, RCV | W2 | O | Transfer Out + Transfer In |
| `/transfers/new` | Transfer Initiation | MGR | W2 | N | `frmimtransferout` |
| `/transfers/:id` | Transfer Detail | MGR, RCV | W2 | O | Transfer Out detail |
| `/transfers/:id/receive` | Transfer Receipt | RCV, MGR | W2 | N | `frmimtransferin` |
| `/transfers/:id/variance` | Transfer Variance Review | LP, MGR | W2 | O | None in CP |
| `/inventory/count` | Physical Count List | MGR | W2 | N | `frmimphyscountenter` list |
| `/inventory/count/new` | Physical Count Create | MGR, ADM | W2 | N | `frmimphyscountcreate` |
| `/inventory/count/:id` | Physical Count Entry (mobile) | EMP, MGR | W2 | N | `frmimphyscountenter` |
| `/inventory/count/:id/post` | Physical Count Post | MGR | W2 | N | Physical count post |
| `/inventory/adjustments` | Adjustment List | MGR | W2 | N | None |
| `/inventory/adjustments/new` | Inventory Adjustment Create | MGR | W2 | N | `frmimadjustmentsenter` |

---

### Purchasing

| URL | Screen Title | Roles | Wave | Origin | CP Equivalent |
|---|---|---|---|---|---|
| `/vendors` | Vendor List + Scorecard | BYR, ADM | W3 | N | Vendor maintenance |
| `/vendors/:id` | Vendor Detail (terms, items, POs, RTVs, performance) | BYR | W3 | N | `frmvendors` |
| `/orders/suggested` | Suggested Orders Queue | BYR | W3 | O | Purchasing Advice report |
| `/orders/distribution` | Distribution Recommendations Queue | BYR, MGR | W3 | L4 | None in CP |
| `/orders` | Purchase Order List | BYR, MGR | W3 | O | PO list |
| `/orders/new` | Purchase Order Create | BYR | W3 | N | `frmpopreqenter` |
| `/orders/:id` | Purchase Order Detail | BYR, MGR | W3 | O | PO detail |
| `/otb` | Open-to-Buy Dashboard | BYR, MGR | W3 | L4 | None in CP |
| `/otb/:period` | OTB Period Detail (category/vendor breakdown, approval queue) | BYR, MGR | W3 | L4 | None in CP |
| `/receiving` | Receiving Sessions List | RCV, MGR | W3 | O | `frmporeceivingsenter` list |
| `/receiving/:id` | Receiving Session — Line Entry | RCV | W3 | O | `frmporeceivingsenter` |
| `/receiving/:id/close` | Receiving Close + Post | MGR, RCV | W3 | O | Receiving close and voucher |
| `/receiving/blind` | Blind Receiving (no PO) | RCV, MGR | W3 | N | Blind receiving option |
| `/returns` | RTV List | BYR, RCV | W3 | O | RTV list |
| `/returns/:id` | RTV Detail | BYR, RCV | W3 | O | RTV entry form |

---

### Finance

| URL | Screen Title | Roles | Wave | Origin | CP Equivalent |
|---|---|---|---|---|---|
| `/reports/eod` | End-of-Day Summary | MGR, ADM | W3 | N | X/Z-Tape |
| `/reports/finance` | Finance Report | MGR, ADM | W3 | O | Crystal Reports — Financial Summary |
| `/reports/payments` | Payments + Tender Mix | MGR | W3 | O | Crystal Reports — Tender Analysis |
| `/reports/tax` | Tax Report | MGR, ADM | W3 | O | Crystal Reports — Tax Detail |
| `/reports/ar-aging` | AR Aging — Aggregate Commercial | MGR, ADM | W3 | L4 | None in CP |
| `/reports/gift-cards` | Gift Card Liability + Balance | MGR | W3 | L4 | None in CP |

---

### Merchandising

| URL | Screen Title | Roles | Wave | Origin | CP Equivalent |
|---|---|---|---|---|---|
| `/promotions` | Promotion Calendar | BYR, MGR | W4 | O | `frmimplannedpromotions` |
| `/markdowns` | Markdown List | BYR | W4 | L4 | None in CP |
| `/markdowns/new` | Markdown Proposal Create | BYR | W4 | L4 | None in CP |
| `/markdowns/:id` | Markdown Detail + Approval | BYR, MGR | W4 | L4 | Crystal Reports — Markdown History |
| `/reports/range` | Range Analysis | BYR | W4 | O | Crystal Reports — Merchandise Analysis |
| `/reports/forecast` | Demand Forecast View | BYR, MGR | W3 | L4 | None in CP |
| `/reports/price-history` | Price Change History | BYR, LP | W4 | O | None in CP |
| `/reports/flash` | Flash Sales / Intraday Pacing | MGR | W2 | N | X-Tape (manual) |
| `/reports/markdowns` | Markdown Effectiveness | BYR | W4 | O | Crystal Reports — Markdown History |
| `/reports/grid` | Grid Report (Color × Size) | BYR | W4 | N | Crystal Reports |
| `/reports/category` | Category Performance | BYR, MGR | W2 | O | Crystal Reports |
| `/reports/pricing` | Competitive Pricing | BYR | W4 | O | None in CP |

---

### Employees

| URL | Screen Title | Roles | Wave | Origin | CP Equivalent |
|---|---|---|---|---|---|
| `/timecards` | Timecard Editor | MGR | W4 | N | `frmsytimecardsenter` |
| `/timeclock` | Mobile Clock-In / Clock-Out | EMP | W4 | N | Windows time clock workstation |
| `/timecards/export` | Payroll Export | MGR, ADM | W4 | N | Timecard export |

---

### Devices

| URL | Screen Title | Roles | Wave | Origin | CP Equivalent |
|---|---|---|---|---|---|
| `/devices` | Station Registry — all stores | ADM, MGR | W2 | FD | Station config in CP (no cloud surface) |
| `/devices/:id` | Station Detail (type, store, last-active, adapter, status) | ADM | W2 | FD | None |
| `/devices/health` | Device Health Dashboard (offline count, latency, error rate by station) | ADM | W2 | FD | None |

---

### Agents

| URL | Screen Title | Roles | Wave | Origin | CP Equivalent |
|---|---|---|---|---|---|
| `/agents` | Agent Activity Dashboard (active agents, throughput, error rate, latency) | ADM | W3 | FD | None |
| `/agents/junctions` | Junction Map (all 166 MCP junctions — active/erroring/idle) | ADM | W3 | FD | None |
| `/agents/:id` | Agent Detail (junction count, recent activity, config, error log) | ADM | W3 | FD | None |
| `/agents/config` | Agent Configuration (enable/disable agent behaviors, tune parameters) | ADM | W3 | FD | None |

---

### Operations — Wave 5 (W-Module)

| URL | Screen Title | Roles | Wave | Origin | CP Equivalent |
|---|---|---|---|---|---|
| `/exceptions` | All Exceptions List | MGR, LP | W5 | O | None |
| `/exceptions/:id` | Exception Detail | MGR, LP | W5 | O | None |
| `/cases` | Cases — All Domains | LP, MGR | W5 | O | None |
| `/cases/new` | Create Case (Any Exception) | LP, MGR | W5 | O | None |
| `/cases/:id/evidence` | Evidence Attach (Cross-Domain) | LP | W5 | O | None |
| `/cases/:id/correlation` | Cross-Domain Subject Correlation | LP | W5 | O | None |
| `/cases/:id/remediate` | Dispatch Remediation Action | MGR | W5 | O | None |
| `/reports/cases` | Cross-Domain Case Performance | MGR | W5 | O | None |

---

### Settings

| URL | Screen Title | Roles | Wave | Origin | CP Equivalent |
|---|---|---|---|---|---|
| `/settings/alert-routing` | Alert Routing Config (incl. B2B alert class) | ADM, MGR | W1 | O+L4 | None |
| `/settings/training-mode` | Training Mode Toggle | ADM, MGR | W1 | O | None |
| `/settings/allowlist/dead-count` | Allow-List — Dead Count | ADM | W1 | O | None |
| `/settings/allowlist/discounts` | Allow-List — Discounts | ADM | W1 | O | None |
| `/settings/allowlist/voids` | Allow-List — Voids | ADM | W1 | O | None |
| `/settings/allowlist/comps` | Allow-List — Comps | ADM | W1 | O | None |
| `/settings/store/drawer` | Store Config — Drawer Threshold | ADM | W1 | O | `frmpscontrol` |
| `/settings/store/discounts` | Store Config — Discount Cap | ADM | W1 | O | `frmpscontrol` |
| `/settings/store/void-reasons` | Store Config — Void Reasons | ADM | W1 | O | `frmpscontrol` |
| `/settings/store/comp-reasons` | Store Config — Comp Reasons | ADM | W1 | O | `frmpscontrol` |
| `/settings/store/locations` | Location / Location Group Config | ADM | W2 | N | Location maintenance |
| `/settings/store/stations` | Station & Device Registration | ADM | W2 | FD | Station config in CP |
| `/settings/payment` | Tender Classification + EDC Config | ADM | W3 | L4 | `frmpscontrol` tender section |
| `/settings/loyalty/programs` | Loyalty Program Config | ADM | W4 | N | 3 CP loyalty screens |
| `/settings/pricing/rules` | Price Rules — BOGO / Mix-Match | BYR, ADM | W4 | N | `frmimmixmatchcodes` |
| `/settings/catalog` | Catalog Config — Attributes + Profiles | ADM | W2 | N | Item attribute setup |
| `/settings/vertical-pack` | Vertical Pack Management | ADM | W5 | L4 | None |

---

## Rollup by Wave

| Wave | Sections | Screens (routes) | Key additions in v2 |
|---|---|---|---|
| Admin (cross-wave) | Admin | 9 | Tenant management, DevOps (3 screens) |
| W1 — LP Investigator Core | Surveillance (partial), Investigations, Customers (W1 tabs), Settings (LP) | 25 | Rule dry-run / parameters panel; B2B alert class on alert routing |
| W2 — Store Ops + Devices | Inventory, Surveillance (transactions), Devices, Settings (store+devices) | 22 | 3 device screens; station config |
| W3 — Finance + Purchasing + Planning | Purchasing, Finance, Agents, Merchandising (forecast) | 22 | OTB (2), Distribution Recs (1), AR Aging, Gift Cards, Forecast, Agents (4) |
| W4 — Merch + Labor | Merchandising, Employees, Settings (loyalty, pricing) | 19 | Markdown workflow (3 screens) |
| W5 — W Execution | Operations, Settings (vertical-pack) | 9 | Vertical-pack screen |
| **Total** | | **~106** | |

---

## Rollup by User Role

| Role | Sections visible | Approx screens |
|---|---|---|
| LP Investigator | Surveillance, Investigations, Customers | ~30 |
| Store Manager | Surveillance, Inventory, Purchasing, Finance, Employees, Operations | ~45 |
| Buyer / Merch Manager | Inventory, Purchasing, Merchandising, Settings (pricing, loyalty) | ~30 |
| Receiving Clerk | Purchasing (receiving + RTV), Inventory (transfers) | ~10 |
| Admin | Admin, Devices, Agents, Settings (all) | ~30 |
| Employee | Time Clock only | 1 |

---

## UX Displacement Summary

Ten screens where Canary's design explicitly beats Counterpoint's:

| # | Canary Screen | CP Form(s) Displaced | Key Improvement |
|---|---|---|---|
| 1 | `/inventory/count/:id` (mobile) | `frmimphyscountenter` | Mobile-first, real-time progress — no paper worksheets |
| 2 | `/items/:id` (price panel) | `frmpricetest` + `frmitems` | All applicable prices in one view vs 3-form navigation |
| 3 | `/items` (search results) | `frmitems` | Cross-location on-hand in search results vs open-and-navigate |
| 4 | `/orders/suggested` | Purchasing Advice report | Live approval queue vs print → read → key |
| 5 | `/settings/loyalty/programs` | 3 CP loyalty config screens | Unified builder with live transaction preview |
| 6 | `/timeclock` | Windows clock hardware | Any browser replaces $1,500 dedicated workstation |
| 7 | `/transactions/:id/proof` | None | Cryptographic audit proof — CP has no integrity chain |
| 8 | `/transfers/:id/variance` | None | Auto-alerts LP at receipt vs manual paper note |
| 9 | `/reports/eod` | X/Z-Tape | Web-native daily close vs register-side procedure |
| 10 | `/settings/pricing/rules` | `frmimmixmatchcodes` + promotions rules tab | Unified BOGO + mix-match builder with basket preview |

**Net-new capabilities (no CP equivalent at all):**

| Screen | What Canary does that CP cannot |
|---|---|
| `/otb` + `/otb/:period` | Open-to-Buy budget control with committed receipt tracking |
| `/orders/distribution` | Multi-location inventory rebalancing recommendations |
| `/agents` + `/agents/junctions` | MCP agent network observability (166 junctions) |
| `/reports/forecast` | Machine-generated demand forecast per item/location |
| `/reports/ar-aging` | Aggregate commercial AR aging across all B2B accounts |
| `/customers/:id` → Commercial† | B2B credit posture and classification intelligence |
| `/transactions/:id/proof` | Hash-chained cryptographic audit proof |
| `/devices/health` | Real-time store hardware health from cloud |

---

*Source: docs/superpowers/specs/2026-05-04-canary-go-screen-scenario-map.md × docs/superpowers/specs/2026-05-04-counterpoint-canary-ux-crosswalk.md × docs/superpowers/specs/2026-05-04-canary-go-l4-gap-delta.md × docs/superpowers/specs/2026-05-03-canary-go-ui-wave-plan.md*

*v2 changes: +OTB (2), +Distribution Recs (1), +AR Aging (1), +Gift Cards (1), +Demand Forecast (1), +Devices section (3), +Agents section (4), +DevOps/Admin (3), +Markdown workflow (3), +Tenant management (2), +Commercial customer tab, +B2B alert class, +Vertical-pack setting, +Station config, +Payment config = ~22 additions → ~106 total routes*
