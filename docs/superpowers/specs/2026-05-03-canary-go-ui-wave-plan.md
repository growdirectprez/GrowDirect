---
type: spec
title: Canary Go UI Wave Plan — L4 Process-Grounded Screen Inventory
status: approved
date: 2026-05-03
source: CRB deep/process-decomp/ (GRO-670 pass)
gro: GRO-771
---

# Canary Go UI Wave Plan

**Governing thesis:** Every screen on the Canary Go portal maps to one or more L3 processes in the CRB. This spec enumerates those mappings, sequences them into delivery waves, and calls out the Go module each screen draws from. The CRB UI Surface Scan (GRO-670) identified 135 L3s requiring a user surface; this plan addresses them in four waves plus one admin cross-cut.

**Today's baseline:** 20 templates exist — most are functional stubs. The Q (loss prevention) core is partially built; no S, D, J, P, L, W, or admin screens exist.

**Priority logic:** Category A (Canary owns) before Category B (interface layer). LP investigator surface first because that's the product. Admin cross-cuts all waves because you can't operate without it.

---

## Admin (Cross-Wave — GRO-770)

Blocked by GRO-769 (identity middleware). Ships concurrent with Wave 1 unblocking.

| Screen | URL | L3 Source | Go Module | Surface Type |
|--------|-----|-----------|-----------|-------------|
| Users list | `/admin/users` | Admin / identity | `internal/identity` | Config/Admin |
| User detail + role assign | `/admin/users/:id` | Admin / identity | `internal/identity` | Config/Admin |
| Audit log | `/admin/audit` | T.2.6 mutation-lock + identity events | `internal/identity`, `cmd/tsp` | Dashboard |
| System config health | `/admin/config` | N.1.1–N.3.5 store config ingestion status | `internal/tenant`, `internal/obs` | Dashboard |

**Design notes:**
- User admin is the only surface where a Canary operator can create/deactivate accounts and assign investigator vs manager vs viewer roles
- Audit log shows all Canary mutations with actor + timestamp + hash — same evidentiary model as Fox case timeline
- Config health surfaces which tenants have completed N.1–N.3 ingestion (store config sync) and whether the LP substrate fields are populated

---

## Wave 1 — LP Investigator Core (Q + C + N.4)

**What it is:** The primary operator experience. An investigator gets an alert, opens the case, pulls customer context, acts on evidence. This is the entire Category A, Q-module surface.

**Current state:** Alerts list, Rules list, Cases list/detail, Chirps feed exist as stubs. All need real handler wiring and data. The config surfaces (allow-lists, N.4 thresholds) are entirely absent.

### Q — Loss Prevention Investigator Surface

| Screen | URL | L3 Source | Go Module | Surface Type |
|--------|-----|-----------|-----------|-------------|
| Alert list (exists — stub) | `/alerts` | Q.5.1–Q.5.3 | `internal/alert` | Alert/Notification |
| Alert detail + acknowledge | `/alerts/:id` | Q.5.3 acknowledgment, Q.5.4 escalation | `internal/alert` | Workflow/Approval |
| Alert routing config | `/settings/alert-routing` | Q.5.2 routing by severity/type/store | `internal/alert` | Config/Admin |
| Detection rules list (exists — stub) | `/rules` | Q.2.1–Q.2.10 (24 rules, 11 families) | `internal/fox` | Config/Admin |
| Detection rule detail + enable/disable | `/rules/:id` | Q.2.x + allow-list linkage | `internal/fox` | Config/Admin |
| Chirp feed (exists — stub) | `/chirps` | Q.1.1–Q.1.5 substrate ingestion | `internal/fox` | Dashboard |
| Chirp detail | `/chirps/:id` | Q.1.x + evidence hash | `internal/fox` | MCP Investigator |
| Case list — Hawk (exists) | `/cases/hawk` | Q.3.1 (Fox INSERT-only ledger) | `internal/fox` | MCP Investigator |
| Case detail — Hawk (exists) | `/cases/hawk/:id` | Q.3.2–Q.3.5 (timeline, evidence) | `internal/fox` | MCP Investigator |
| Evidence attach | `/cases/hawk/:id/evidence` | Q.7.3 hash-chained evidence submission | `internal/fox` | Workflow/Approval |
| Case analytics | `/cases/hawk/analytics` | Q.7.5 LP performance dashboard | `internal/fox`, `internal/analytics` | Dashboard |
| Cross-case pattern view | `/cases/hawk/patterns` | Q.7.6 multi-case correlation | `internal/fox` | MCP Investigator |
| Allow-list admin — dead count | `/settings/allowlist/dead-count` | Q.6.1 known-good cashiers per store | `internal/fox` | Config/Admin |
| Allow-list admin — discounts | `/settings/allowlist/discounts` | Q.6.2 pre-approved discount patterns | `internal/fox` | Config/Admin |
| Allow-list admin — admin voids | `/settings/allowlist/voids` | Q.6.3 authorized admin-void reason codes | `internal/fox` | Config/Admin |
| Allow-list admin — comps | `/settings/allowlist/comps` | Q.6.4 authorized comp reason codes | `internal/fox` | Config/Admin |
| Training mode toggle | `/settings/training-mode` | Q.6.5 suppress LP during training | `internal/fox` | Config/Admin |

### C — Customer Investigator Surface

| Screen | URL | L3 Source | Go Module | Surface Type |
|--------|-----|-----------|-----------|-------------|
| Customer lookup (investigator) | `/customers` | C.6.1 investigator customer search | `internal/customer` | MCP Investigator |
| Customer detail | `/customers/:id` | C.6.2 purchase history, C.6.3 risk score | `internal/customer` | MCP Investigator |
| Customer risk score surface | `/customers/:id/risk` | C.6.3 risk indicator + C.2.1–C.2.4 scoring | `internal/customer`, `internal/fox` | MCP Investigator |
| Customer cross-module context | `/customers/:id/context` | C.6.4 presence across cases + subjects | `internal/customer`, `internal/fox` | MCP Investigator |

### N — LP Substrate Configuration

| Screen | URL | L3 Source | Go Module | Surface Type |
|--------|-----|-----------|-----------|-------------|
| Drawer threshold config | `/settings/store/drawer` | N.4.1 → feeds Q Q-DC-01 | `internal/tenant` | Config/Admin |
| Discount cap config | `/settings/store/discounts` | N.4.2 max discount per reason code → Q Q-DR-01 | `internal/tenant` | Config/Admin |
| Void reason codes | `/settings/store/void-reasons` | N.4.3 valid void list → Q Q-VO-01 | `internal/tenant` | Config/Admin |
| Comp reason codes | `/settings/store/comp-reasons` | N.4.4 valid comp list → Q Q-CO-01 | `internal/tenant` | Config/Admin |

**Wave 1 total: 25 new/upgraded screens + 4 admin screens**

---

## Wave 2 — Store Ops Visibility (T + D + S item + N device)

**What it is:** Everything a store manager needs to see what's happening operationally. Transaction audit, inventory position, transfers, device health, item intelligence. Category A analytics surfaces + full Category B read-through.

### T — Transaction Detail + Audit Proof

| Screen | URL | L3 Source | Go Module | Surface Type |
|--------|-----|-----------|-----------|-------------|
| Transaction list (exists — stub) | `/transactions` | T.3.1–T.3.8 parsing, T.4.1–T.4.9 canonical events | `cmd/tsp` | Dashboard |
| Transaction detail | `/transactions/:id` | T.2.3 hash-before-parse, T.2.4 seal record | `cmd/tsp` | MCP Investigator |
| Audit proof verification | `/transactions/:id/proof` | T.5.1–T.5.5 Merkle anchoring + audit proof | `cmd/tsp` | MCP Investigator |

### D — Distribution + Transfer

| Screen | URL | L3 Source | Go Module | Surface Type |
|--------|-----|-----------|-----------|-------------|
| Transfer list | `/transfers` | D.3.1 initiation, D.3.5 receipt confirmation | `internal/inventory` | Dashboard |
| Transfer detail | `/transfers/:id` | D.3.2–D.3.4 in-transit tracking | `internal/inventory` | Workflow/Approval |
| Transfer variance review | `/transfers/:id/variance` | D.4.1 transfer-loss adjudication | `internal/inventory` | Workflow/Approval |
| Distribution reconciliation report | `/reports/distribution` | D.5.1 variance by lane | `internal/report` | Dashboard |
| Inventory balance report | `/reports/inventory` | D.5.2 snapshot vs perpetual | `internal/report` | Dashboard |

### S — Item + Category Intelligence

| Screen | URL | L3 Source | Go Module | Surface Type |
|--------|-----|-----------|-----------|-------------|
| Item catalog search | `/items` | S.7.1 item lookup for investigators + buyers | `internal/item` | MCP Investigator |
| Item detail | `/items/:id` | S.2.1 display attributes, S.7.2 margin target | `internal/item` | Dashboard |
| Category performance | `/reports/category` | S.7.3 margin + volume by category | `internal/report`, `internal/item` | Dashboard |
| Item drift alerts | `/alerts?type=item-drift` | S.5.1–S.5.2 drift + lifecycle alerts | `internal/item`, `internal/alert` | Alert/Notification |

### N — Device Health + Store Config Viewer

| Screen | URL | L3 Source | Go Module | Surface Type |
|--------|-----|-----------|-----------|-------------|
| Device health dashboard | `/settings/devices` | N.5.1–N.5.2 device + connectivity alerts | `internal/tenant` | Alert/Notification |
| Store config viewer | `/settings/store` | N.1.1–N.3.5 read-through (~150 fields) | `internal/tenant` | Config/Admin |
| Device registration | `/settings/devices/new` | N.3.1 POS terminal + peripheral registration | `internal/tenant` | Config/Admin |

**Wave 2 total: 16 screens**

---

## Wave 3 — Finance + Receiving (F + J)

**What it is:** LP-connected financial visibility and the receiving clerk workflow. Finance surfaces show the cost of shrink; receiving workflow is the Category B read-through that feeds inventory and OTB.

### F — Finance (LP-Connected Analytics)

| Screen | URL | L3 Source | Go Module | Surface Type |
|--------|-----|-----------|-----------|-------------|
| Financial summary | `/reports/finance` | F.6.1 daily/weekly/period P&L surface | `internal/report` | Dashboard |
| Payment method report | `/reports/payments` | F.6.4 tender mix + Secure Pay summary | `internal/report` | Dashboard |
| Tax liability report | `/reports/tax` | F.6.3 multi-authority tax summary | `internal/report` | Dashboard |

### J — Receiving + RTV Workflow

| Screen | URL | L3 Source | Go Module | Surface Type |
|--------|-----|-----------|-----------|-------------|
| Receiving sessions list | `/receiving` | O.6.1 receiving initiation | `internal/returns` (receiving) | Dashboard |
| Receiving session — line entry | `/receiving/:id` | O.6.2–O.6.3 line confirmation + discrepancy | `internal/returns` | Workflow/Approval |
| Receiving close + post | `/receiving/:id/close` | O.6.7 close and post | `internal/returns` | Workflow/Approval |
| RTV list | `/returns` | O.7.1 return initiation | `internal/returns` | Dashboard |
| RTV detail | `/returns/:id` | O.7.2 quantity confirmation, O.7.4 credit reconciliation | `internal/returns` | Workflow/Approval |
| OTB dashboard | `/reports/otb` | O.3.5 budget vs actual open-to-buy by period | `internal/report` | Dashboard |
| Suggested orders list | `/orders/suggested` | O.4.1–O.4.3 suggested order + buyer review | `internal/report` | Workflow/Approval |

**Wave 3 total: 10 screens**

---

## Wave 4 — Merchandising + Labor (S range + P + L)

**What it is:** The buyer + manager experience. Range analytics for item planning decisions, promotion calendar visibility for LP accuracy, labor productivity surface. Mostly Category C analytics (Canary provides the data; the decision stays with the buyer/manager).

### S — Range Planning Analytics

| Screen | URL | L3 Source | Go Module | Surface Type |
|--------|-----|-----------|-----------|-------------|
| Range performance dashboard | `/reports/range` | S.6.1 sell-through, turn, GMROI | `internal/report`, `internal/item` | Dashboard |

### P — Pricing + Promotion Visibility

| Screen | URL | L3 Source | Go Module | Surface Type |
|--------|-----|-----------|-----------|-------------|
| Promotion calendar view | `/promotions` | P.6.3 publish promotion calendar (read-only) | `internal/pricing` | Dashboard |
| Competitive pricing dashboard | `/reports/pricing` | P.4.1 price position vs market | `internal/pricing`, `internal/report` | Dashboard |
| Price change history | `/reports/price-history` | P.4.2 price movement audit trail | `internal/pricing`, `internal/report` | Dashboard |
| Markdown effectiveness | `/reports/markdowns` | P.3.3–P.3.5 markdown monitoring | `internal/pricing`, `internal/report` | Dashboard |

### L — Labor + Productivity

| Screen | URL | L3 Source | Go Module | Surface Type |
|--------|-----|-----------|-----------|-------------|
| Employee list (exists — stub) | `/employees` | L.1.1–L.1.3 employee sync | `internal/employee` | Dashboard |
| Employee detail | `/employees/:id` | L.3.3 productivity signal to Q LP context | `internal/employee` | Dashboard |
| Productivity dashboard | `/reports/labor` | L.3.1 transactions/hour vs store average | `internal/report`, `internal/employee` | Dashboard |

**Wave 4 total: 8 screens**

---

## Wave 5 — W Execution (Cross-Domain Case Management)

**What it is:** The v3 capstone. Execution module generalizes the Q investigator pattern across all domains — not just LP events but any cross-domain exception. Depends on Waves 1–4 being fully wired (W pulls context from all modules).

| Screen | URL | L3 Source | Go Module | Surface Type |
|--------|-----|-----------|-----------|-------------|
| Exception list (all domains) | `/exceptions` | E.1.1–E.2.3 detection + aggregation | `internal/casemgmt` | MCP Investigator |
| Exception detail | `/exceptions/:id` | E.5.1 exception search tool | `internal/casemgmt` | MCP Investigator |
| Cross-domain case create | `/cases/new` | E.5.2 W-level case creation | `internal/casemgmt` | Workflow/Approval |
| Evidence aggregation view | `/cases/:id/evidence` | E.5.3 cross-domain evidence view | `internal/casemgmt` | MCP Investigator |
| Cross-domain correlation | `/cases/:id/correlation` | E.5.4 subject-based pattern surface | `internal/casemgmt` | MCP Investigator |
| Remediation routing | `/cases/:id/remediate` | E.5.5 dispatch remediation to target module | `internal/casemgmt` | Workflow/Approval |
| Cross-domain case analytics | `/reports/cases` | E.5.6 cross-domain case performance | `internal/casemgmt`, `internal/report` | Dashboard |

**Wave 5 total: 7 screens**

---

## Screen Inventory Summary

| Wave | Screens | Primary Modules | Priority | Blocking Dep |
|------|---------|----------------|----------|-------------|
| Admin (cross-wave) | 4 | identity | Urgent | GRO-769 |
| Wave 1 — LP Core | 25 | fox, alert, customer, tenant | P0 | None |
| Wave 2 — Store Ops | 16 | tsp, inventory, item, tenant, report | P1 | Wave 1 config |
| Wave 3 — Finance + Receiving | 10 | report, returns | P1 | Wave 2 inventory |
| Wave 4 — Merch + Labor | 8 | pricing, item, employee, report | P2 | Wave 2 item |
| Wave 5 — W Execution | 7 | casemgmt | P3 | Waves 1–4 |
| **Total** | **70** | | | |

**Existing screens (stubs needing real handler wiring):** dashboard, chirps, transactions, alerts, cases/hawk (3), employees, reports, rules, settings, owl, connect = 13

---

## Navigation Architecture

Current sidebar has: Dashboard, Chirps, Transactions, Alerts, Cases, Employees, Reports, Settings, Owl.

Wave additions require sidebar expansion or grouped sub-navigation:

```
Dashboard
──────────────
Alerts              (Q — existing + Wave 1 upgrade)
  └ Alert Routing   (settings sub)
Chirps              (Q — existing)
Rules               (Q — existing + Wave 1 detail)
Cases               (Q hawk — existing + W cross-domain Wave 5)
Customers           (C — Wave 1 new)
Exceptions          (W — Wave 5)
──────────────
Transactions        (T — existing + Wave 2 detail)
Transfers           (D — Wave 2)
Receiving           (J — Wave 3)
Returns / RTV       (J — Wave 3)
Items               (S — Wave 2)
──────────────
Reports
  ├ Finance         (F — Wave 3)
  ├ Category        (S — Wave 2)
  ├ Range           (S — Wave 4)
  ├ Distribution    (D — Wave 2)
  ├ OTB             (J — Wave 3)
  ├ Labor           (L — Wave 4)
  ├ Pricing         (P — Wave 4)
  └ Cases           (W — Wave 5)
Employees           (L — existing + Wave 4)
Promotions          (P — Wave 4)
──────────────
Settings
  ├ Store Config    (N — Wave 2)
  ├ Devices         (N — Wave 2)
  ├ Alert Routing   (Q — Wave 1)
  ├ Allow-lists     (Q — Wave 1)
  ├ LP Thresholds   (N.4 — Wave 1)
  └ Training Mode   (Q — Wave 1)
──────────────
Owl                 (semantic — existing)
Admin               (identity — GRO-770)
```

---

## Dispatch Recommendation

| GRO | Title | Wave | Screens |
|-----|-------|------|---------|
| GRO-770 | Admin module (users, audit, config health) | Admin | 4 |
| GRO-772 | Wave 1A: Alert + Rules detail screens | Wave 1 | Alert detail, Rule detail, Chirp detail |
| GRO-773 | Wave 1B: Customer investigator surface | Wave 1 | Customer lookup, detail, risk, context |
| GRO-774 | Wave 1C: Allow-list + N.4 LP threshold config | Wave 1 | 9 config screens |
| GRO-775 | Wave 1D: Case evidence attach + analytics | Wave 1 | Evidence attach, Case analytics, Cross-case patterns |
| GRO-776 | Wave 2A: Transaction detail + audit proof | Wave 2 | Txn detail, Merkle proof |
| GRO-777 | Wave 2B: Transfers + inventory reports | Wave 2 | Transfer list/detail/variance, Distribution + inventory reports |
| GRO-778 | Wave 2C: Item catalog + device health | Wave 2 | Item catalog, Item detail, Category report, Device health |
| GRO-779 | Wave 3: Finance + Receiving workflow | Wave 3 | 10 screens |
| GRO-780 | Wave 4: Merch + Labor analytics | Wave 4 | 8 screens |
| GRO-781 | Wave 5: W Execution cross-domain | Wave 5 | 7 screens |

---

*Source: CRB deep/process-decomp/ (GRO-670) · UI Surface Scan + MVP Scope Matrix + Process Map*
*135 CRB UI-surface L3s → 70 portal screens across 5 waves + admin*
