---
type: spec
title: Canary Go — Current-State Audit + Wave Plan Rebaseline
status: draft
date: 2026-05-07
supersedes: docs/superpowers/specs/2026-05-03-canary-go-ui-wave-plan.md
gro: TBD (filing dispatches as approved)
---

# Canary Go — Current-State Audit + Wave Plan Rebaseline

**Governing thesis:** The 2026-05-03 UI Wave Plan was a planning artifact, not a build queue. Code has moved past it in two directions: (1) deeper than the spec assumed (protocol/payment/adapter/workflow rails are real), and (2) shallower at the surface (most portal routes are cosmetic stubs over working modules). The scope was also too narrow — it covered the LP investigator surface only and ignored the broader capability surface (Owl analytics, Workflow substrate, Protocol portal, supplier/PO lifecycle, mobile UX, ecom channel, MCP tool surface, onboarding flow). This spec rebases against the code that actually exists and the 166 capability cards in `Brain/wiki/cards/`.

---

## 1. What's actually built

### 1.1 Layered inventory

| Layer | Reality | Evidence |
|---|---|---|
| **Protocol substrate** (Sub 1 hash → Sub 2 parse → Sub 3 Merkle anchor; 13 subpackages incl. anchor, audit, cockroach, evidence, hmac, namespace, publisher, secrets, validate, webhook) | Real, tested, in production paths | `internal/protocol/*`, `cmd/sub*-*/`, GRO-750/751/752/754 |
| **Payment rails** (LNURL-auth + L402 sat-gated validation API) | Real, migrated, mounted on gateway | migrations 022/023, `internal/auth/lnurl/`, `internal/protocol/validate/` |
| **Workflow substrate** (`app.workflow_definitions` + `app.workflow_executions`, pg_advisory_lock cross-replica coord; 3 engines: three-way-match, L402 charge cycle, investigation lifecycle) | Real | `internal/workflow/`, GRO-763 |
| **MCP gateway** (26 tools across 7 modules + `/.well-known/mcp.json` discovery) | Real | `cmd/gateway/`, `internal/mcp/`, GRO-767, GRO-802 Day 5 |
| **POS adapters** (Counterpoint REST polling, Square OAuth + token refresh + AES-GCM at-rest, public mirror to `growdirect-llc/canary-go`) | Real, demo path active | `cmd/edge/`, `internal/squareauth/`, GRO-801, GRO-802 |
| **Inventory engines** (SOH consumer, Min/Max replenishment trigger, directed-task queue: receiving + replenishment + cycle_count) | Real | `cmd/bull/`, `internal/inventory/`, GRO-798/799/800 |
| **Detection schema** (rules + detections + lp_substrate + allow_list, all tenant-scoped) | Real, migrated, read-store wired into web.Deps + gateway | migration 024, `internal/lp/substrate.go` |
| **Owl semantic surface** (RFM rollups per party, LP-rate metrics aggregation, Wave C dashboards) | Real but under-surfaced (single `/owl` route) | `internal/owl/` (10 files) |
| **Module layer** (~25 internal modules with store + handler + tests) | Real | alert, analytics, asset, billing, casemgmt, chirp, customer, employee, fox, inventory, item, owl, pricing, report, returns, transaction, etc. |
| **Web portal** (70 routes, 60+ templates) | Mostly cosmetic | `internal/web/handler.go` — see §1.3 |
| **Active workstreams (parallel)** | Square demo (GRO-802 — May 12 dry run), LangGraph workflow (GRO-813), Mercury Splashdown (ALX on Vertex AI Agent Engine), Ruptiv brand engagement, Canary Retail pitch deck v1 (GRO-738) | last 30 days of commits |

### 1.2 Active migrations (11)

| # | Purpose | Status |
|---|---|---|
| 019 | report_jobs | done |
| 020 | protocol_anchors | done |
| 021 | protocol_namespace | done |
| 022 | protocol_validation (L402 surface) | done |
| 023 | lnurl_auth | done |
| 024 | **detection schema (rules, detections, lp_substrate, allow_list)** | done — read-store wired, write-store missing |
| 025 | inventory_soh_consumer | done |
| 026 | directed_tasks | done |
| 027 | inventory_thresholds | done |
| 028 | pos_tenant_credentials | done |
| 029 | pos_tenant_credentials_expires_at | done |

### 1.3 Web handler real-vs-stub map

Of 70 GET/POST routes in `internal/web/handler.go`:

| Status | Count | Examples |
|---|---|---|
| **Real handlers** wired to real stores | ~13 | `alertListPage`, `alertDetailPage`, `customersListPage`, `customerDetailPage`, `customerRiskPage`, `customerContextPage`, `hawkListPage`, `hawkDetailPage`, `hawkEvidencePage`, `chirpListPage`, `chirpDetailPage`, `rulesListPage`, `ruleDetailPage` |
| **Real handler signature, stub data** | ~10 | `transactionDetailPage`, `transactionProofPage`, `transferDetailPage`, `transferVariancePage`, `itemDetailPage`, `employeeDetailPage`, `receivingDetailPage`, `returnsDetailPage`, etc. |
| **Inline closure stubs** via `h.page(...)` | ~48 | All settings/* allowlist + N.4 routes, all reports/* routes, promotions, exceptions, cross-domain cases, OTB, suggested orders, distribution/inventory reports, etc. |

`AllowListStore` is wired into `web.Deps` ([deps.go:19](CanaryGo/internal/web/deps.go:19)) and the gateway main ([gateway/main.go:229](CanaryGo/cmd/gateway/main.go:229)) — but the 4 allow-list settings handlers ignore it and return nil entries. **This is the actual gap, not "build allow-list backend."**

### 1.4 Surfaces with engines but no portal

Modules with real depth that have zero or single-route portal coverage:

| Module | Files | Capability | Current portal surface |
|---|---|---|---|
| `internal/owl/` | 10 | Wave C semantic analytics — RFM, LP-rate, dashboards | Single `/owl` page |
| `internal/workflow/` | 5 | Three-way match, L402 charge cycle, investigation lifecycle | None |
| `internal/protocol/` | 13 subpackages | Anchor proof, evidence chain, namespace, validation, charges | None (proof page is stub) |
| `internal/asset/` | 4 | Asset registry per `canary-asset.md` card | None |
| `internal/billing/` | 4 | Tenant billing surface | None |
| `internal/webhook/` | 4 | Backpressure, DLQ, idempotency intake | None |
| `internal/devops/` | 3 | Pipeline monitor, API explorer, releases panel | `/devops` (DEV_CONSOLE=1, internal-only) |
| `internal/mcp/` | 10 | 26 MCP tools across 7 modules | Discovery endpoint only; no tenant tool surface |

---

## 2. Where the 2026-05-03 wave plan fell short

| Issue | Symptom | Root cause |
|---|---|---|
| **Spec bar = scaffold bar** | Every wave dispatch's "Deliverables" reads `Templates + routes + stubs wired`. Closeable at the cosmetic stage; closed dispatch ≠ working feature. | Plan was written from UI surface inventory (135 L3s → 70 screens), not feature-completion definition. |
| **Parallel platform work invisible** | Protocol/payment/workflow/adapter/MCP/owl work (15+ GRO tickets) wasn't in the wave plan. Looks like nothing's happening on portal because attention is elsewhere. | Plan only covered the LP investigator portal, not the full platform. |
| **No closeout discipline** | GRO-665 was "closed in narrative" 2026-05-01 but state stayed Todo until 2026-05-07. Wave 1A scaffolds shipped 2026-05-04 but nobody closed any of GRO-771-774. | No ritual for "scaffold meets spec → close" or "code passed dispatch → close." |
| **Wrong unit of work** | 11 wave dispatches for one sprint of work = too many. Each wave duplicated the same pattern at varying L3 surfaces. | L3 inventory used as dispatch list instead of grouping by integration boundary. |
| **Coverage gaps** | Owl, Workflow, Protocol portal, Asset, Billing, MCP tenant surface, Mobile UX, Ecom channel, Onboarding flow, Compliance, Multi-store intelligence, Supplier/PO lifecycle — none in the wave plan despite all having capability cards in Brain. | Plan scoped from CRB UI surface scan only; capability cards weren't cross-referenced. |

---

## 3. Rebaselined wave plan

**Operating principle:** Each wave is one **integration boundary**, not one UI surface. Done = the user-visible flow works end-to-end against real persistence + real workflows, not "templates render."

**No firewall on parallel tracks.** Demo (GRO-802), LangGraph (GRO-813), Mercury Splashdown, Ruptiv, pitch deck — all run alongside wave work. Founder triages priority across both lanes.

### Tier 1 — Plumbing (highest leverage, smallest blast radius)

**W1 — Allow-list write path + N.4 thresholds**

- Extend `internal/lp/substrate.go` `AllowListStore` with `Create` / `Update` / `Delete` methods
- Replace 4 inline allow-list stub closures in `handler.go:225-228` with real handlers calling `AllowListStore.ListByRuleID` filtered by rule_code
- Add POST handlers + CSRF + redirect-after-post
- Update 4 templates: editable list view (add row form, delete buttons, expires_at picker)
- **N.4 threshold persistence: extend `detection.allow_list.pattern` jsonb with type discriminator** (decision: agreed). Per-rule thresholds stored as `{type:"threshold", kind:"drawer|discount|void|comp", value:...}`
- Tests: integration against real Postgres (not mocks), tenant-scoped happy/404/cross-leak paths

Estimate: 1 focused session (~6 hours).

**W2 — Portal data-wiring sweep (parallel sub-dispatches)**

Each sub-dispatch wires existing module → existing routes. No new schema, no new modules. **Decision: parallel subagent dispatch (agreed).** Per `superpowers:dispatching-parallel-agents`, each sub-dispatch hits a different module and different routes — fully independent.

| Sub-dispatch | Routes | Module wired |
|---|---|---|
| W2a Transaction | `/transactions/{id}`, `/transactions/{id}/proof` | `cmd/tsp` + `internal/protocol/validate` |
| W2b Inventory + Transfers | `/transfers/*`, `/reports/inventory`, `/reports/distribution` | `internal/inventory` |
| W2c Items + Devices | `/items/*`, `/reports/category`, `/settings/devices*` | `internal/item`, `internal/tenant` |
| W2d Receiving + Returns | `/receiving/*`, `/returns/*` | `internal/returns` (receiving + RTV) |
| W2e Reports surface | All `/reports/*` (finance, payments, tax, OTB, range, pricing, markdowns, labor, cases) | `internal/report` (read-through) |
| W2f Promotions + Pricing | `/promotions`, `/reports/pricing*`, `/reports/markdowns` | `internal/pricing` |
| W2g Employees + Labor | `/employees/{id}`, `/reports/labor` | `internal/employee` |

Estimate: 7 sub-dispatches × ~3-5 hours each. With parallel subagents, ~1 calendar day for the full sweep.

**W3 — Detection rule consumption (closes the W1 loop)**

- `internal/fox` rule evaluator reads `AllowListStore` per detection
- Suppression: detection bypassed if matching pattern active and not expired
- N.4 threshold consumption: rules pull thresholds from `allow_list.pattern` jsonb (per W1 design)
- Audit: suppressed detections logged to `detection.detections` with `status='dismissed'` + suppression reason
- Tests: rule eval with allow-list match (suppressed), no match (fires), expired (fires)

Estimate: 1 session.

### Tier 2 — Workflow + engine surfaces

**W4 — Workflow engine surfaces**

`internal/workflow/` has three engines (three-way-match, L402 charge cycle, investigation lifecycle) with no portal surface. Each gets:
- List view (executions in-flight, per workflow type)
- Detail view (execution trace — current step, context, history)
- Manual advance / cancel actions for stuck executions
- Reference cards: `canary-l402-otb.md`, `retail-three-way-match.md`

Estimate: 1-2 sessions.

**W5 — Engine surfaces (OTB + replenishment + receiving)**

Engines exist (`cmd/bull/` directed-task queue, replenishment trigger, SOH consumer) — surfaces don't.
- `/receiving/*` → wire directed-task queue (claim/complete actions for current operator)
- `/orders/suggested` → wire replenishment-trigger output (review/approve/reject)
- `/reports/otb` → wire OTB calculation
- Workflow POST handlers (receive, approve order, dispatch task)
- Reference cards: `canary-receiving.md`, `retail-replenishment-model.md`, `canary-l402-otb.md`

Estimate: 1-2 sessions.

**W6 — Owl semantic intelligence surface**

`internal/owl/` has 10 files including `aggregator`, `dashboards`, `dashboards_handler`, `metrics`, `period`, RFM rollups, LP-rate metrics. Single `/owl` route surfaces ~5% of the module's depth.
- Operator-facing analytics dashboards: party RFM, LP performance over time, signal heatmaps, alert volume by rule
- Period selector (day / week / month / quarter)
- Drill-down from aggregate → underlying detection list
- Reference cards: `canary-os-thesis.md`, `canary-store-brain.md`

Estimate: 1-2 sessions.

**W7 — Protocol portal surfaces**

`internal/protocol/` has 13 subpackages with no portal coverage.
- Anchor proof browser (`/protocol/anchors`) — Merkle root + Bitcoin L2 anchor reference
- Evidence chain viewer (`/protocol/evidence`) — hash chain per case
- Namespace registry (`/protocol/namespace`) — `.jeffe` registrations
- L402 charge log (`/protocol/charges`) — sat-gated request audit
- Validation API status (`/protocol/validation`) — backpressure, DLQ, request rate
- Webhook intake monitor (`/protocol/webhooks`) — backpressure, DLQ, idempotency stats
- Reference cards: `canary-protocol-gateway-live-on-gcp.md`, `canary-evidentiary-rail.md`, `canary-blockchain-anchor.md`, `infra-l402-otb-settlement.md`

Estimate: 2 sessions.

### Tier 3 — Platform surfaces

**W8 — Asset + Billing portal**

Both modules exist, no portal surface.
- Asset: registry per tenant — devices, locations, equipment, services. Per `canary-asset.md` card.
- Billing: tenant subscription view, satoshi cost-meter, invoice history, payment method. Per `canary-meter-model-token-plan.md`, `infra-satoshi-cost-rollup.md`, `canary-ildwac.md`.

Estimate: 1-2 sessions.

**W9 — Compliance + admin surface**

- Audit log viewer (`/admin/audit`) — actor + timestamp + hash, all mutations
- Multi-authority tax report (`/reports/tax`) wired to real data — F.6.3 — supports ISO27001 audit playbook
- ISO27001 controls dashboard — per `iso27001-audit-playbook.md` card
- User admin (`/admin/users`) — depends on GRO-769 identity middleware + GRO-770 admin module
- Config health (`/admin/config`) — N.1-N.3 ingestion completeness per tenant
- Reference cards: `canary-compliance.md`, `iso27001-audit-playbook.md`

Estimate: 2 sessions (blocked partially on GRO-769/770 for identity).

**W10 — Multi-store intelligence**

- Store hierarchy admin — chains, regions, formats per `merchant-org-hierarchy.md`
- Cross-store dashboards — comparative LP rate, sell-through, shrink
- Network integrity surface — per `canary-store-network-integrity.md`, `store-network-integrity.md`
- Store switcher in nav for multi-store operators
- Reference cards: `canary-multi-store-intelligence.md`

Estimate: 1-2 sessions.

### Tier 4 — New capability surfaces

**W11 — Supplier + Purchase Order lifecycle**

Capability cards exist (`canary-supplier-profile-and-ordering.md`, `canary-purchase-order-lifecycle.md`, `retail-purchase-order-model.md`, `retail-three-way-match.md`, `retail-vendor-lifecycle.md`, `retail-vendor-scorecard.md`, `retail-vendor-compliance-standards.md`) but no module or surface.
- New `internal/supplier/` module — supplier profile CRUD
- New `internal/po/` module — purchase order lifecycle (draft → submitted → received → closed)
- Three-way match completion surface (PO + receiving + invoice → variance flags)
- Vendor scorecard surface
- Routes: `/suppliers`, `/po`, `/po/{id}`, `/po/{id}/match`

Estimate: 3-4 sessions (new modules + tables + UI + workflow integration).

**W12 — MCP tool surface for tenants**

Gateway exposes 26 tools but tenants have no visibility into what they can call.
- Tool catalog (`/mcp/tools`) — list available tools per tenant tier
- Tool usage log (`/mcp/usage`) — call history, satoshi cost, error rate
- Tool playground (`/mcp/playground`) — internal-only debug surface
- Reference cards: `canary-protocol-gateway-live-on-gcp.md`, MCP discovery endpoint

Estimate: 1-2 sessions.

**W13 — Onboarding flow (the missing wizard)**

Currently no end-to-end onboarding UI. Operator connects Square OAuth via `/connect`, then... nothing. Need:
- Wizard steps: connect POS → import store config (N.1-N.3) → enable detection rules → first detection
- Default seed data: standard void/comp reason vocab on tenant creation
- Health check at each step + retry path
- Welcome dashboard for first-week operators (what to look at first)
- Reference cards: `canary-os-thesis.md`, `canary-store-brain.md`

Estimate: 2-3 sessions.

**W14 — Mobile / Android POS UX**

Capability card exists (`canary-mobile-task-ux-flows.md`) but nothing built. This is its own product surface — likely a Tailwind Alpine.js responsive cut of receiving + directed-task screens, plus device-side scan integrations.
- Mobile-first directed-task list (claim/complete on phone/tablet)
- Receiving line entry on mobile (scan → confirm)
- Cycle-count workflow on mobile
- Alert acknowledge on mobile
- Android POS integration contract per `canary-android-pos-integration.md` and `canary-device-contracts.md`

Estimate: 4-6 sessions (deeper because it's a new delivery channel).

### Tier 5 — Capstone

**W15 — Ecom channel surface**

`canary-ecom-channel.md` capability card exists. Probably last-priority surface unless an Ecom-flagged tenant lands.

Estimate: TBD.

**W16 — W execution / cross-domain case management capstone**

Currently 7 routes stub-rendered (`casesNewPage`, `casesEvidencePage`, `casesCorrelationPage`, `casesRemediatePage`, `exceptionDetailPage`). Real work in `internal/casemgmt/`. Depends on Tiers 1-3 being real, not scaffolded.
- Cross-domain exception list pulling from all modules
- Case create that auto-pulls evidence from inventory + cases + customers + transactions
- Subject-based correlation across modules
- Remediation routing to target module workflow
- Reference cards: `canary-hawk.md`, `canary-operations-hub.md`

Estimate: 2-3 sessions.

---

## 4. Out-of-scope coverage (acknowledged, not waved)

The following capability cards exist but are deliberately not wave-ified yet — they're either signal feeds (not a build until a tenant needs them), reference architecture (already inherent in code), or strategic positioning (not portal work):

- Signal feeds: `signal-civil-services.md`, `signal-community-intel.md`, `signal-property-landlord.md`, `signal-seasonality.md`, `signal-social-threat.md`, `signal-weather-seo.md`, `shelf-edge-demand-heartbeat.md`, `local-market-agent.md`
- Tier model: `tier-bulk-window.md`, `tier-change-feed.md`, `tier-daily-batch.md`, `tier-reference.md`, `tier-stream.md` (reflected in code already)
- Strategy/positioning: `canary-commercial.md`, `canary-os-thesis.md`, `mission-main-street.md`, `competitive-landscape.md`, `counterpoint-product-state-2026.md`, `counterpoint-var-landscape.md`, `ncr-ecosystem-2026.md`, `var-acquisition-thesis.md`, `vertical-smb-health-hypothesis.md`
- Retail-domain reference: `retail-chargeback-matrix.md`, `retail-demand-forecasting.md`, `retail-event-management.md`, `retail-import-management.md`, `retail-inventory-audit.md`, `retail-inventory-valuation-mac.md`, `retail-item-authorization.md`, `retail-merchandise-financial-planning.md`, `retail-merchandise-hierarchy.md`, `retail-operations-kpis.md`, `retail-receiving-disposition.md`, `retail-replenishment-model.md`, `retail-sales-audit.md`, `retail-site-management.md`, `retail-space-range-management.md`, `retail-vendor-compliance-standards.md`, `retail-vendor-lifecycle.md`, `retail-vendor-scorecard.md`, `rms-replenishment-screen-flows.md`, `rpas-planning-paradigm.md` — these inform W4-W11 design but don't become their own waves
- Runbooks: `runbook-*.md` cards — operational docs, not portal features
- Ruptiv-track: `ruptiv-*.md` cards — separate engagement, not Canary portal

If any of these become user-facing in a tenant request, file a dedicated dispatch at that time.

---

## 5. Parallel tracks (not part of wave plan but consume capacity)

| Track | What | Status |
|---|---|---|
| **Square demo** | GRO-802 May 12 dry run — Square OAuth, dashboard from sandbox data, webhook feed, public mirror, autodiscovery, vault/GitHub footers | Active, last commit today |
| **LangGraph workflow** | GRO-813 — codegen pipeline (generate / review / emit), releases panel in `/devops` | Recently shipped |
| **Mercury Splashdown** | ALX on Vertex AI Agent Engine parallel track | SDD + plan committed; build TBD |
| **Ruptiv brand engagement** | Architecture partnership, brand enforcement skill, deployment posture brief | Separate workstream |
| **Pitch decks** | GRO-738 Canary Retail v1 (internal + external) | Shipped |
| **OpenAPI 3.0 protocol spec** | GRO-740 auto-generator | Merged |

Founder triages capacity across wave work and parallel tracks.

---

## 6. Dispatch hygiene actions (run after spec approval)

| Dispatch | Action | Reason |
|---|---|---|
| GRO-665 | Cancelled | Stale architecture (this session) |
| GRO-771, 772, 774 | Closed Done | Scaffolds shipped; counted at cosmetic bar (this session) |
| GRO-773 | Re-open | W1 here is the real finish (this session) |
| GRO-775, 776, 777, 778, 779, 780 | **Cancel** | Scaffold dispatches superseded by W2 sub-dispatches with real-data DoD |
| GRO-770 | Keep open | Admin module — reframed as W9 prereq |
| GRO-769 | Verify status | Identity middleware — W9 dependency |
| GRO-788–796 | Verify status | Wave-1 LP core implementation plan series — likely overlap with new W1; cancel or re-scope after audit |
| **New** | File dispatches W1, W2a-g, W3, W4-W16 | Per template in §7 |

### 6.1 New dispatch shape

Every new wave dispatch follows this template — *not* the old "templates + routes + stubs wired" pattern:

```
## What
[One-paragraph user-visible flow — what does the operator do, what changes for them]

## Done when
- [Specific UX: "an investigator can add a cashier ID to dead-count allow-list,
   refresh the page, and see the entry persist; deleting works; tenant isolation enforced"]
- [Specific code: "AllowListStore.Create returns row with generated UUID; tests cover
   happy + duplicate + cross-tenant leak"]
- [Specific verification: "exercised against real Postgres in `make test-integration`"]

## Out of scope
[Explicit list — what this dispatch does NOT do, e.g. "rule consumption is W3, not W1"]

## Reference cards
[Capability card paths — `Brain/wiki/cards/X.md` — load via memory_recall before starting]
```

---

## 7. Recommended sequence (no firewall, founder-triaged)

| Tier | Waves | Notes |
|---|---|---|
| 1 | W1, W2a-g, W3 | ~10 sub-dispatches; W2 parallelizable; biggest portal impact per hour |
| 2 | W4, W5, W6, W7 | Workflow + engine + Owl + Protocol surfaces |
| 3 | W8, W9, W10 | Asset/Billing + Compliance + Multi-store |
| 4 | W11, W12, W13, W14 | New modules: Supplier/PO, MCP tenant, Onboarding, Mobile |
| 5 | W15, W16 | Ecom + W cross-domain capstone |

Total: ~30-40 dispatches. With parallel sub-dispatching where feasible and 1-3 sessions per dispatch, the portal goes from "~13 real routes / ~57 stubs" to "fully real" in roughly 4-6 weeks of focused build time, plus tier 4 new modules adding another 3-4 weeks. Mobile (W14) is the longest single tier — separate delivery channel.

---

## 8. What's NOT in this spec (deliberately)

- Nothing about Cove, Angel, or non-Canary projects
- Nothing about CRMS / NCR vault content
- Nothing about marketing/positioning
- No new architecture decisions — uses what's already built
- No SDD back-fill — capability cards in `Brain/wiki/cards/` remain authoritative per memory feedback ("Code is ahead of SDDs — compare against capability cards")
- No process-change automation (close-on-merge) — table for separate decision
- No "demo firewall" — wave work and parallel tracks run side-by-side; founder triages
