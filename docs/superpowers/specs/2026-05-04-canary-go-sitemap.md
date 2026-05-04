---
type: spec
title: Canary Go — Canonical Site Map
status: draft
date: 2026-05-04
source: 2026-05-04-canary-go-screen-scenario-map.md × 2026-05-04-counterpoint-canary-ux-crosswalk.md × 2026-05-03-canary-go-ui-wave-plan.md
gro: TBD
purpose: Single canonical reference for Canary Go's complete URL hierarchy, navigation structure, user roles per screen, wave assignment, and Counterpoint equivalent. Input for wireframe briefs and navigation implementation.
---

# Canary Go — Canonical Site Map

**Governing thesis:** Canary Go organizes its ~100 screens into nine navigable sections. The left sidebar exposes the sections relevant to the signed-in user's role — an LP Investigator sees Surveillance, Investigations, and Customers; a Buyer sees Inventory, Purchasing, and Merchandising; a Manager sees everything except Admin. This document is the complete URL hierarchy behind that sidebar.

**Notation:**

| Key | Meaning |
|---|---|
| O | Original wave plan screen |
| N | New — added from Counterpoint crosswalk |
| † | Tab or panel on a parent screen (not a separate route) |
| * | Settings screen — sidebar under Settings section |
| [W1]–[W5] | Wave assignment |
| [ADM] | Admin section — separate from sidebar nav |

---

## Navigation Architecture

```
Left sidebar (role-scoped):
├── Dashboard                      /
├── Surveillance ──────────────── (LP, MGR)
│   ├── Alerts                     /alerts
│   ├── Live Feed (Chirps)         /chirps
│   ├── Transactions               /transactions
│   └── Detection Rules            /rules
├── Investigations ─────────────── (LP, MGR)
│   ├── Cases                      /cases/hawk
│   ├── Analytics                  /cases/hawk/analytics
│   └── Patterns                   /cases/hawk/patterns
├── Customers ──────────────────── (LP, MGR)
│   └── Customer Lookup            /customers
├── Inventory ──────────────────── (MGR, BYR, LP)
│   ├── Items                      /items
│   ├── Transfers                  /transfers
│   ├── Physical Counts            /inventory/count
│   └── Adjustments                /inventory/adjustments
├── Purchasing ─────────────────── (BYR, RCV, MGR)
│   ├── Vendors                    /vendors
│   ├── Suggested Orders           /orders/suggested
│   ├── Purchase Orders            /orders
│   └── Receiving                  /receiving
├── Finance ────────────────────── (MGR, ADM)
│   ├── EOD Summary                /reports/eod
│   ├── Finance Report             /reports/finance
│   ├── Payments                   /reports/payments
│   └── Tax                        /reports/tax
├── Merchandising ──────────────── (BYR, MGR)
│   ├── Promotion Calendar         /promotions
│   ├── Range Analysis             /reports/range
│   ├── Price History              /reports/price-history
│   ├── Flash Sales                /reports/flash
│   ├── Markdowns                  /reports/markdowns
│   └── Grid Report                /reports/grid
├── Employees ──────────────────── (MGR, ADM, EMP)
│   ├── Timecards                  /timecards
│   ├── Time Clock                 /timeclock
│   └── Payroll Export             /timecards/export
├── Operations (W) ─────────────── (LP, MGR — Wave 5)
│   ├── All Exceptions             /exceptions
│   ├── Cases                      /cases
│   └── Case Reports               /reports/cases
└── Settings ───────────────────── (ADM, MGR)
    ├── Alert Routing              /settings/alert-routing
    ├── Training Mode              /settings/training-mode
    ├── Allow-Lists (4)            /settings/allowlist/*
    ├── Store Config (4)           /settings/store/*
    ├── Loyalty Programs           /settings/loyalty/programs
    ├── Price Rules                /settings/pricing/rules
    └── Catalog Config             /settings/catalog

Admin (top-bar link, not sidebar):
├── Users                          /admin/users
├── Audit Log                      /admin/audit
└── Config Health                  /admin/config
```

---

## Screen Inventory

### Admin (Cross-Wave)

| URL | Screen Title | Roles | Wave | Origin | CP Equivalent |
|---|---|---|---|---|---|
| `/admin/users` | Users List | ADM | Cross | O | `frmsecuritycodes` + user records |
| `/admin/users/:id` | User Detail + Role Assignment | ADM | Cross | O | User maintenance + security code assignment |
| `/admin/audit` | Audit Log | ADM, LP | Cross | O | None |
| `/admin/config` | Config Health | ADM | Cross | O | None |

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
| `/chirps/:id` | Chirp / Transaction Detail | LP | W1 | O | `frmpstickethistory` (no hash, no rules) |
| `/transactions` | Transaction List | LP, MGR | W2 | O | `frmpstickethistory` |
| `/transactions/:id` | Transaction Detail | LP, MGR | W2 | O | Ticket History detail |
| `/transactions/:id/proof` | Audit Proof Verification | LP, ADM | W2 | O | None |
| `/rules` | Detection Rules List | LP, ADM | W1 | O | None |
| `/rules/:id` | Rule Detail + Enable/Disable | LP, ADM | W1 | O | None |

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
| `/customers/:id/risk` | Customer Risk Score† | LP | W1 | O | None |
| `/customers/:id/context` | Customer Cross-Module Context† | LP | W1 | O | None |
| `/customers/:id/loyalty` | Customer Loyalty Tab† | MGR | W4 | N | `frmarloyptsadjustmentsenter` + enrollment form |
| `/customers/:id/ar` | Customer A/R View† | MGR | W3 | N | `frmaraccountsenter` open items tab |

---

### Inventory

| URL | Screen Title | Roles | Wave | Origin | CP Equivalent |
|---|---|---|---|---|---|
| `/items` | Item Catalog Search | LP, MGR, BYR | W2 | O | `frmitems` (no cross-loc on-hand) |
| `/items/:id` | Item Detail | LP, MGR, BYR | W2 | O | `frmitems` (no analytics overlay) |
| `/items/new` | Item Create | ADM, BYR | W2 | N | `frmitems` new record |
| `/items/:id/edit` | Item Edit | ADM, BYR | W2 | N | `frmitems` |
| `/transfers` | Transfer List | MGR, RCV | W2 | O | Transfer Out + Transfer In (no unified view) |
| `/transfers/new` | Transfer Initiation | MGR | W2 | N | `frmimtransferout` (Windows-only) |
| `/transfers/:id` | Transfer Detail | MGR, RCV | W2 | O | Transfer Out detail |
| `/transfers/:id/receive` | Transfer Receipt | RCV, MGR | W2 | N | `frmimtransferin` (Windows-only) |
| `/transfers/:id/variance` | Transfer Variance Review | LP, MGR | W2 | O | None in CP |
| `/inventory/count` | Physical Count List | MGR | W2 | N | `frmimphyscountenter` list |
| `/inventory/count/new` | Physical Count Create | MGR, ADM | W2 | N | `frmimphyscountcreate` (Windows-only) |
| `/inventory/count/:id` | Physical Count Entry | EMP, MGR | W2 | N | `frmimphyscountenter` (Windows-only) |
| `/inventory/count/:id/post` | Physical Count Post | MGR | W2 | N | Physical count post (Windows-only) |
| `/inventory/adjustments` | Adjustment List | MGR | W2 | N | None |
| `/inventory/adjustments/new` | Inventory Adjustment Create | MGR | W2 | N | `frmimadjustmentsenter` (Windows-only) |

---

### Purchasing

| URL | Screen Title | Roles | Wave | Origin | CP Equivalent |
|---|---|---|---|---|---|
| `/vendors` | Vendor List | BYR, ADM | W3 | N | Vendor maintenance (no scorecard) |
| `/vendors/:id` | Vendor Detail + Scorecard | BYR | W3 | N | `frmvendors` (no performance metrics) |
| `/orders/suggested` | Suggested Orders Queue | BYR | W3 | O | Purchasing Advice report (printed, no interaction) |
| `/orders` | Purchase Order List | BYR, MGR | W3 | O | PO list — Windows-only |
| `/orders/new` | Purchase Order Create | BYR | W3 | N | `frmpopreqenter` (Windows-only) |
| `/orders/:id` | Purchase Order Detail | BYR, MGR | W3 | O | PO detail |
| `/receiving` | Receiving Sessions List | RCV, MGR | W3 | O | `frmporeceivingsenter` list |
| `/receiving/:id` | Receiving Session — Line Entry | RCV | W3 | O | `frmporeceivingsenter` (Windows-only) |
| `/receiving/:id/close` | Receiving Close + Post | MGR, RCV | W3 | O | Receiving close and voucher |
| `/receiving/blind` | Blind Receiving (no PO) | RCV, MGR | W3 | N | Blind receiving option in CP |
| `/returns` | RTV List | BYR, RCV | W3 | O | RTV list |
| `/returns/:id` | RTV Detail | BYR, RCV | W3 | O | RTV entry form (Windows-only) |

---

### Finance

| URL | Screen Title | Roles | Wave | Origin | CP Equivalent |
|---|---|---|---|---|---|
| `/reports/eod` | End-of-Day Summary | MGR, ADM | W3 | N | X-Tape / Z-Tape (run at register) |
| `/reports/finance` | Finance Report | MGR, ADM | W3 | O | Crystal Reports — Financial Summary |
| `/reports/payments` | Payments + Tender Mix | MGR | W3 | O | Crystal Reports — Tender Analysis |
| `/reports/tax` | Tax Report | MGR, ADM | W3 | O | Crystal Reports — Tax Detail |

---

### Merchandising

| URL | Screen Title | Roles | Wave | Origin | CP Equivalent |
|---|---|---|---|---|---|
| `/promotions` | Promotion Calendar | BYR, MGR | W4 | O | `frmimplannedpromotions` (Windows-only) |
| `/reports/range` | Range Analysis | BYR | W4 | O | Crystal Reports — Merchandise Analysis |
| `/reports/price-history` | Price Change History | BYR, LP | W4 | O | None in CP |
| `/reports/flash` | Flash Sales / Intraday Pacing | MGR | W2 | N | X-Tape (manual run at register) |
| `/reports/markdowns` | Markdown Effectiveness | BYR | W4 | O | Crystal Reports — Markdown History (no effectiveness) |
| `/reports/grid` | Grid Report (Color × Size) | BYR | W4 | N | Crystal Reports — Sales by Color/Size |
| `/reports/category` | Category Performance | BYR, MGR | W2 | O | Crystal Reports — Category Analysis |
| `/reports/pricing` | Competitive Pricing | BYR | W4 | O | None in CP |

---

### Employees

| URL | Screen Title | Roles | Wave | Origin | CP Equivalent |
|---|---|---|---|---|---|
| `/timecards` | Timecard Editor | MGR | W4 | N | `frmsytimecardsenter` (Windows-only) |
| `/timeclock` | Mobile Clock-In / Clock-Out | EMP | W4 | N | Windows time clock workstation |
| `/timecards/export` | Payroll Export | MGR, ADM | W4 | N | Timecard export (Windows-only, single format) |

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
| `/settings/alert-routing` | Alert Routing Config | ADM, MGR | W1 | O | None |
| `/settings/training-mode` | Training Mode Toggle | ADM, MGR | W1 | O | None |
| `/settings/allowlist/dead-count` | Allow-List — Dead Count | ADM | W1 | O | None |
| `/settings/allowlist/discounts` | Allow-List — Discounts | ADM | W1 | O | None |
| `/settings/allowlist/voids` | Allow-List — Voids | ADM | W1 | O | None |
| `/settings/allowlist/comps` | Allow-List — Comps | ADM | W1 | O | None |
| `/settings/store/drawer` | Store Config — Drawer Threshold | ADM | W1 | O | `frmpscontrol` (200-field form) |
| `/settings/store/discounts` | Store Config — Discount Cap | ADM | W1 | O | `frmpscontrol` |
| `/settings/store/void-reasons` | Store Config — Void Reasons | ADM | W1 | O | `frmpscontrol` |
| `/settings/store/comp-reasons` | Store Config — Comp Reasons | ADM | W1 | O | `frmpscontrol` |
| `/settings/store/locations` | Location / Location Group Config | ADM | W2 | N | Location maintenance in CP |
| `/settings/loyalty/programs` | Loyalty Program Config | ADM | W4 | N | Loyalty setup — 3 separate CP screens |
| `/settings/pricing/rules` | Price Rules — BOGO / Mix-Match | BYR, ADM | W4 | N | `frmimmixmatchcodes` + promotions rules tab |
| `/settings/catalog` | Catalog Config — Attributes + Profiles | ADM | W2 | N | Item attribute and profile code setup in CP |

---

## Rollup by Wave

| Wave | Section(s) | Original | New | Total |
|---|---|---|---|---|
| Admin (cross-wave) | Admin | 4 | 0 | 4 |
| W1 — LP Investigator Core | Surveillance (partial), Investigations, Customers (partial), Settings (LP subset) | 25 | 0 | 25 |
| W2 — Store Ops Visibility | Surveillance (transactions), Inventory, Merchandising (flash, category) | 9 | 9 | 18 |
| W3 — Finance + Receiving | Purchasing, Finance | 7 | 5 | 12 |
| W4 — Merchandising + Labor | Merchandising, Employees, Settings (loyalty, pricing), Customers (loyalty†) | 8 | 9 | 17 |
| W5 — W Execution | Operations | 8 | 0 | 8 |
| **Total** | | **61** | **23** | **~84** |

*Note: Tabs (†) and detail views of existing screens are not counted separately in this rollup.*

---

## Rollup by User Role

| Role | Primary sections | Approx screen count |
|---|---|---|
| LP Investigator | Surveillance, Investigations, Customers | ~28 |
| Store Manager | Surveillance, Inventory, Purchasing, Finance, Employees, Operations | ~40 |
| Buyer / Merch Manager | Inventory, Purchasing, Merchandising, Settings (pricing, loyalty) | ~25 |
| Receiving Clerk | Purchasing (receiving + RTV), Inventory (transfers) | ~8 |
| Admin | Admin, Settings (all), Users | ~20 |
| Employee | Time Clock only | 1 |

*Role counts overlap — a screen accessible to LP and MGR counts in both.*

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

---

*Source: docs/superpowers/specs/2026-05-04-canary-go-screen-scenario-map.md × docs/superpowers/specs/2026-05-04-counterpoint-canary-ux-crosswalk.md × docs/superpowers/specs/2026-05-03-canary-go-ui-wave-plan.md*
