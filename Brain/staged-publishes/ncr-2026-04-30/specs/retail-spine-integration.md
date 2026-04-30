---
title: NCR Counterpoint Retail Spine Integration
tags: [specs, counterpoint, integration, architecture, sdd]
nav_order: 51
audience: NCR Counterpoint VARs
last-updated: 2026-04-30
---

# SDD — NCR Counterpoint Retail Spine Integration

## 1. Architecture overview

```
┌────────────────────────────────┐         ┌──────────────────────────┐
│  Customer site (e.g. H&G chain)│         │  Canary infrastructure   │
│                                │         │                          │
│  ┌──────────────────────────┐  │         │  ┌────────────────────┐  │
│  │  NCR Counterpoint v8.5+  │  │         │  │  TSP Counterpoint  │  │
│  │  (Windows on-prem)       │  │         │  │     adapter        │  │
│  └────────────┬─────────────┘  │         │  └─────────┬──────────┘  │
│               │ TLD            │         │            │             │
│               ▼                │         │            ▼             │
│  ┌──────────────────────────┐  │ HTTPS   │  ┌────────────────────┐  │
│  │  Counterpoint REST API   │◄─┼─────────┼──┤  Polling / fetch   │  │
│  │  Server (.NET 4.5.2)     │  │ Basic+  │  └─────────┬──────────┘  │
│  │  Windows host, 8889 etc. │  │ APIKey  │            │             │
│  └──────────────────────────┘  │         │            ▼             │
│                                │         │  ┌────────────────────┐  │
└────────────────────────────────┘         │  │  CRDM (Postgres)   │  │
                                           │  └─────────┬──────────┘  │
                                           │            │             │
                                           │            ▼             │
                                           │  ┌────────────────────┐  │
                                           │  │  Downstream Canary │  │
                                           │  │  modules (Chirp,   │  │
                                           │  │  Fox, dashboards)  │  │
                                           │  └────────────────────┘  │
                                           └──────────────────────────┘
```

**Path:** Counterpoint REST API → TSP Counterpoint adapter → CRDM → downstream Canary modules.

**Network:** Counterpoint API server is at the customer's site, on Windows. Canary's adapter polls / fetches from it over HTTPS using HTTP Basic auth + APIKey header. Customer-provided host or Canary-provided edge box is a per-deployment decision (see §10 Risks).

## 2. Source-of-truth references

- **API spec** — `Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/` (cloned from `github.com/NCRCounterpointAPI/APIGuide`)
  - `README.md` — entry point + endpoint chart
  - `Basics/Requests.md`, `Basics/Responses.md`, `Basics/DateFormats.md`
  - `InstallationAndConfiguration/Configuring.md`, `Licensing.md`, `TLS1.2.md`, `TokenizationUtility.md`
  - `Endpoints/*.md` — **95 documented endpoints** (97 files; 2 are header-only stubs: `GET_Customer_Address.md`, `GET_Customer_Note.md`. README chart correctly omits both. File-naming inconsistencies present: `PATCH_Customer_Address` (no extension), `POST_Document_Note.md.md` (stutter). Earlier drafts of this SDD said 99 — corrected against the file inventory 2026-04-25.)
  - `Release_Notes/API_2.{0,1,2,3,4}_Release_Notes.md`
- **Spine wikis** — `Brain/wiki/canary-module-*.md` (one per module letter)
- **Existing TSP** — `Brain/wiki/canary-tsp-pipeline.md`
- **CRDM** — `Brain/wiki/canary-data-model.md`
- **Derived spec** — `docs/sdds/canary/ncr-counterpoint-openapi.yaml` (OpenAPI 3.0; 71 paths, 95 operations, 49 schemas; validates)
- **Endpoint × CRDM × Spine map** — `Brain/wiki/ncr-counterpoint-endpoint-spine-map.md` (full per-endpoint mapping; this SDD §4 is the class-level summary, that wiki is the per-endpoint detail)
- **Stand-up runbook** — `Brain/wiki/ncr-counterpoint-connection-runbook.md`

## 3. Authentication + authorization

| Endpoint class | Auth | APIKey required? | Notes |
|---|---|---|---|
| System administration (`/AdminUsers`, `/APIKey`, `/Database`, `/Roles`, ...) | HTTP Basic with **system** admin creds | Per endpoint — see Endpoints/ | Used during initial setup; rare in steady state |
| Company functions (everything operational: customers, items, transactions, ...) | HTTP Basic with `<company>.<username>:<password>` | Yes (most) | Per Counterpoint company; multi-company deployments use multiple credentials |

**Per-customer auth bootstrap:**
1. Customer's Counterpoint license must have the **API user option** enabled in `registration.ini` (paid add-on; bulk of endpoints require it).
2. NCR-issued APIKey installed on the customer's Counterpoint API server.
3. Canary-side: store credentials per tenant (encrypted at rest); rotate quarterly.

**Cross-cutting auth concern:** Canary's TSP must NEVER store unencrypted Counterpoint credentials. Use Canary's standard secret-store; rotate via the secret-rotation runbook (see `docs/audit-2026-04-23/secret-rotation-runbook.md`).

## 4. CRDM alignment

Canary's CRDM uses 5 entity classes (People × Places × Things × Events × Workflows). Counterpoint endpoints map across them. The table below is the class-level summary; per-endpoint detail lives in `Brain/wiki/ncr-counterpoint-endpoint-spine-map.md`.

| CRDM class | Counterpoint endpoint groups | Spine modules |
|---|---|---|
| **People** | Customer*, Customer_Address, Customer_Note, Customer_OpenItems | R, C |
| **Places** | Store*, Store_Station, Device_Config; InventoryLocations | N (Store/Device); **D (InventoryLocations primary)** |
| **Things** | Item*, ItemCategor*, ItemSerial*, Item_Images, Item_Inventory, Inventory*, GiftCard (code/template definitions only) | S, A |
| **Events** | Document* (sales tickets/transactions); GiftCard* (transactions + tender activity); returns/voids embedded in Document | T, **F (GiftCard primary as tender)**, Q |
| **Workflows** | EC (ecommerce), forecasting/ordering endpoints (per Endpoints/ — verify), tasks where supported | W, J, C |
| **Platform / cross-cutting** | AdminUser*, Roles, RoleUsers, RoleEndpoints, APIKey, Database, SystemInfo, CACHE | platform (no spine letter — API server self-administration; out of CRDM) |

**Mapping refinements vs draft-1 (recorded 2026-04-25 after per-endpoint extraction):**
- **AdminUser/Roles → Platform.** Earlier draft put them under People (R/L/C). They are API-server self-administration, not customer or labor data. Moved off People, onto a new Platform row.
- **GiftCard\* → Events / F primary.** Earlier draft put them under Things (S/A/P). Per-endpoint reading: gift card *codes/templates* are catalog entries (S, secondary), but the endpoint surface is dominantly transaction/tender (F, primary). The "P" attribution was not defensible.
- **InventoryLocations → D primary.** Earlier draft listed N, D for the whole Places row. InventoryLocations is dominantly a Distribution concept (transfers, multi-location stock); Stores and Devices remain N. Both modules retained on the row, with D explicitly primary for InventoryLocations.

Per-module mapping detail in §6 below.

## 5. ARTS standards alignment

Counterpoint emits ARTS-compatible structures (verified via `onlinehelp.ncr.com` Advanced Store + ACS docs):

- **POSLog 2.2.1** — Counterpoint Document* endpoints produce POSLog-compatible transaction data. Canary's POSLog parser plans for **v2.x as primary**; v4 backward-compat (older NCR deployments); v6 forward-compat (hypothetical).
- **Customer model** — Customer / Customer_Address / Customer_Note → ARTS Customer entity
- **Device model** — Store / Store_Station / Device_Config → ARTS Device entity
- **Site model** — Store / InventoryLocations → ARTS Site entity

**Out of scope:** non-ARTS extensions specific to Counterpoint that don't have an ARTS analog (per-module §6 calls these out).

## 6. Module-by-module mappings

For each module: **spine intent**, **Counterpoint endpoints**, **CRDM entities**, **ARTS alignment**, **MCP tool surface**, **TSP adapter notes**, **open questions**.

### 6.1 Module T — Transactions

- **Spine intent:** sales tickets, returns, voids, payments, discounts. The data backbone.
- **Counterpoint endpoints:** `Document*` family (most numerous), `GET_Document.md`, `Document_Contact`, `Document_Note`. PayCode* relates here too.
- **CRDM entities:** `Events.transactions`, `Events.returns`, `Events.voids`, `Events.discounts`, `Events.payments`
- **ARTS:** POSLog 2.2.1 transaction structures (full conformance)
- **MCP tool surface:**
  - `get_transactions(date_range, store, status?)` — paginated
  - `get_voids(date_range)` — paginated
  - `get_returns(date_range)` — paginated
  - `get_transaction_detail(document_id)` — single
- **TSP adapter:** incremental polling via `/Documents` with timestamp filter. Idempotent upsert keyed on `document_id`. Backfill capability for historical sync. Pagination via skip/take (see Counterpoint pagination convention).
- **Open questions:**
  - Ticket-line vs document granularity — does Counterpoint expose line items as nested or separate endpoint?
  - Void-of-sale vs return distinction in Counterpoint's data model
  - Tender / payment-method coverage via PayCode endpoints

### 6.2 Module R — Customer

- **Spine intent:** customer entity, contact info, history, segmentation, B2B vs retail distinction
- **Counterpoint endpoints:** `Customer*`, `Customers`, `Customers_EC` (ecommerce), `Customer_Address`, `Customer_Note`, `Customer_OpenItems`, `Customer_Card` (delete/manage card-on-file), `CustomerControl`
- **CRDM entities:** `People.customers`, `People.customer_addresses`, `People.customer_notes`
- **ARTS:** Customer model
- **MCP tool surface:**
  - `get_customer(customer_id)` — single
  - `search_customers(query, status?)` — paginated
  - `get_customer_history(customer_id, date_range?)` — paginated transactions
  - `get_customer_open_items(customer_id)` — open balances / accounts receivable
- **TSP adapter:** full sync nightly + incremental on-demand. Watch for B2B customer-tier indicators (multi-tier customer pricing is H&G-relevant).
- **Open questions:**
  - Loyalty program data — separate endpoint?
  - Customer-tier mapping (retail vs landscaper vs commercial) — likely a CustomerControl field
  - Card-on-file / tokenization integration (see TokenizationUtility.md)

### 6.3 Module N — Device

- **Spine intent:** POS terminals, scanners, scales, registers. The physical store endpoint inventory.
- **Counterpoint endpoints:** `Store*`, `Store_Station`, `Device_Config`, `StoreTokenizeInfo`, `StoresTokenized`
- **CRDM entities:** `Places.stores`, `Places.stations`, `Places.devices`
- **ARTS:** Device model + Site model
- **MCP tool surface:**
  - `get_stores()` — full list
  - `get_store(store_id)` — single
  - `get_store_stations(store_id)` — stations per store
  - `get_device_config(store_id, station_id)` — device-level config
- **TSP adapter:** infrequent sync (stores + devices change rarely). On-demand refresh on tokenization-flow events.
- **Open questions:**
  - Hardware model / firmware version coverage — typically not exposed via REST
  - Network shape per device (LAN-only vs cloud-reachable) — out-of-band

### 6.4 Module A — Asset Management

- **Spine intent:** non-saleable assets (equipment, fixtures, stock-keeping but not item-level inventory)
- **Counterpoint endpoints:** likely none directly; assets are tracked in Counterpoint as items with non-saleable flags. Verify via `Endpoints/GET_Items.md` for asset-flagged items.
- **CRDM entities:** `Things.assets`
- **ARTS:** N/A (not modeled)
- **MCP tool surface:**
  - `get_assets()` — derived view of items with asset flag
- **TSP adapter:** filter on `Items` endpoint with appropriate flag. Implementation detail to verify against `GET_Item.md`.
- **Open questions:**
  - Does Counterpoint distinguish saleable vs non-saleable items at the API level?
  - Depreciation / asset lifecycle data — likely external system

### 6.5 Module Q — Loss Prevention

- **Spine intent:** Canary's CORE module. Detection rules over transaction events.
- **Counterpoint endpoints:** consumes Module T outputs (no Counterpoint-specific endpoints). May leverage `Customer_OpenItems` for AR-related fraud signals.
- **CRDM entities:** `Events.detections`, `Events.alerts` (Canary-internal)
- **ARTS:** N/A (Canary-specific)
- **MCP tool surface:**
  - `query_detections(rule, date_range, store?)` — paginated
  - `get_detection_detail(detection_id)`
  - `list_active_rules()`
- **TSP adapter:** N/A — this module is downstream of T. Detection rules execute against CRDM events, not Counterpoint directly.
- **Phasing note:** comes in **Phase 4** because detection needs T+R+L+N populated first (substrate).
- **Open questions:**
  - Counterpoint-specific fraud patterns (different from Square — e.g., voided-tender patterns, employee discount abuse via PayCodes)

### 6.6 Module C — Commercial

- **Spine intent:** B2B / account customer flows — landscapers, contractors, multi-PO accounts
- **Counterpoint endpoints:** `Customer*` with B2B flag, `Customer_OpenItems` for AR balances. PayCode* for B2B-specific tenders (purchase orders, account charges). Document* with customer-account ticket types.
- **CRDM entities:** `People.commercial_accounts`, `Workflows.purchase_orders`
- **ARTS:** Customer model with extensions
- **MCP tool surface:**
  - `get_commercial_accounts()` — filtered customer list
  - `get_account_balance(customer_id)` — open AR
  - `get_account_purchase_history(customer_id)` — POs
- **TSP adapter:** filter on customer + tender endpoints for B2B distinguishing fields.
- **Open questions:**
  - PO matching logic (Counterpoint vs Canary)
  - Credit limit enforcement (Canary observes; Counterpoint enforces?)

### 6.7 Module D — Distribution

- **Spine intent:** inter-store inventory transfers, multi-location operations
- **Counterpoint endpoints:** `InventoryLocations`, `Inventory_ByLocation`, `Items_ByLocation`, plus distribution-specific Document* types (verify in Endpoints/)
- **CRDM entities:** `Workflows.transfers`, `Things.inventory_by_location`
- **ARTS:** Site model
- **MCP tool surface:**
  - `get_transfers(date_range, source_store?, dest_store?)` — paginated
  - `get_inventory_by_location(item_id)` — per-store inventory
  - `get_low_stock_locations(threshold?)` — derived
- **TSP adapter:** Inventory* endpoints for snapshot; Document* with transfer ticket types for movement events.
- **Open questions:**
  - Transit / in-flight inventory representation
  - Backorder handling

### 6.8 Module F — Finance

- **Spine intent:** payments, tenders, taxes, reconciliation, day-end close
- **Counterpoint endpoints:** `PayCode*`, GiftCard* (gift cards as tenders), Document* (transaction-level financial detail), Tax* (verify in Endpoints/)
- **CRDM entities:** `Events.payments`, `Events.taxes`, `Events.gift_card_transactions`
- **ARTS:** POSLog 2.2.1 tender + tax structures
- **MCP tool surface:**
  - `get_payments(date_range, tender_type?)` — paginated
  - `get_tax_summary(date_range, store?)` — aggregate
  - `get_gift_card_balance(card_id)` — single
  - `get_day_end_close(store_id, date)` — single
- **TSP adapter:** Document* with payment detail, PayCode* for tender taxonomy.
- **Open questions:**
  - Tax authority + rate detail level
  - Day-end close vs continuous reconciliation

### 6.9 Module J — Forecast / Order

- **Spine intent:** demand forecasting, replenishment ordering, vendor PO
- **Counterpoint endpoints:** verify in Endpoints/ — likely Vendor*, PO*, ReplenishmentOrder* (need to scan full endpoint list)
- **CRDM entities:** `Workflows.purchase_orders`, `Workflows.forecasts`, `People.vendors`
- **ARTS:** N/A (not in core ARTS scope)
- **MCP tool surface:**
  - `get_open_purchase_orders(vendor?, status?)` — paginated
  - `get_vendor(vendor_id)` — single
  - `get_replenishment_recommendations(store, item?)` — derived
- **TSP adapter:** ordering endpoints (TBD in Endpoints/ scan)
- **Open questions:**
  - Whether Counterpoint exposes its replenishment engine via REST or only via UI
  - Vendor catalog vs item catalog separation

### 6.10 Module S — Space / Range / Display

- **Spine intent:** item hierarchy, categories, planogram, range. The catalog backbone.
- **Counterpoint endpoints:** `Item*`, `ItemCategor*`, `ItemSerial*`, `Item_Images`, `Item_ImageFilename`, `Items`, `Items_ByLocation`
- **CRDM entities:** `Things.items`, `Things.item_categories`, `Things.item_serials`, `Things.item_images`
- **ARTS:** Item / Product model
- **MCP tool surface:**
  - `get_items(category?, status?)` — paginated
  - `get_item(item_id)` — single
  - `get_item_categories()` — full hierarchy
  - `get_item_inventory(item_id)` — multi-store
  - `get_item_images(item_id)`
- **TSP adapter:** Item* endpoints with full sync nightly + incremental on item-edit events.
- **Open questions:**
  - Lawn/garden module-specific fields (perishables, plant-care chemicals, dead-count tracking) — likely custom fields on Item
  - Mix-and-match flat tracking (garden-center-specific feature mentioned in `lawngardenmarketing.org` listing)

### 6.11 Module P — Pricing / Promotion

> **REVISED 2026-04-25 post deep-dive:** Counterpoint's REST API has **no dedicated Pricing or Promotion endpoint family**. Module P is **derived**, not directly mapped. See `Brain/wiki/ncr-counterpoint-api-reference.md`.

- **Spine intent:** pricing rules, promotions, multi-tier customer pricing
- **Counterpoint endpoints (verified):**
  - **No** Pricing* endpoints
  - **No** Promotion* endpoints
  - Item-level prices live in `GET_Item` payload (verify exact fields)
  - Customer tier flags in `GET_CustomerControl` + per-Customer fields
- **CRDM entities:** `Things.item_prices` (derived), `Things.customer_tiers` (derived)
- **ARTS:** Price model (Promotion model: not applicable — Counterpoint doesn't expose promotion semantics at API level)
- **MCP tool surface (revised — all derived computations):**
  - `get_price(item_id, customer_id?, store?)` — derives from Item base price + CustomerControl tier + per-Customer tier flag
  - `get_pricing_tier(customer_id)` — derives from CustomerControl
  - ~~`get_active_promotions`~~ — N/A (no promotion endpoint)
- **TSP adapter:** Item + CustomerControl + Customer endpoints. Pricing logic lives in the adapter / a CRDM materialization layer.
- **H&G specifics:** multi-tier customer pricing (retail / landscaper / commercial) still critical, but model is "derive at consume time," not "sync a pricing rules table."
- **Open questions (post deep-dive):**
  - ~~Promotion stacking rules~~ — N/A (no promotion endpoint)
  - Effective dating + override behavior — N/A at API level; managed in Counterpoint UI
  - Mix-and-match flat pricing — likely a Counterpoint-internal feature not exposed via API; needs alternative ingestion (CSV export, direct DB read, or UI scraping if customer authorizes)
  - Exact pricing fields on `GET_Item` — read endpoint doc to confirm available fields

### 6.12 Module L — Labor / Workforce

> **REVISED 2026-04-25 post deep-dive:** Counterpoint's REST API has **near-zero workforce coverage**. No Employee, Timeclock, Schedule, or Labor-cost endpoints exist. SDD's prior open question §6.12 (timeclock via REST) is answered: **NO**. Module L cannot be sourced from Counterpoint.

- **Spine intent:** employees, time clock, labor cost, scheduling
- **Counterpoint endpoints (verified):**
  - **No** Employee* endpoints
  - **No** Timeclock* endpoints
  - **No** Schedule* endpoints
  - The User/Role endpoints (`GET_Users`, `GET_Roles`, `GET_UserRoles`, etc.) are API-access-management surfaces, NOT workforce data
- **CRDM entities:** `People.employees`, `Events.timeclock`, `Workflows.schedules` — must be sourced from upstream system other than Counterpoint REST
- **ARTS:** Party model (when sourced from elsewhere)
- **Implication:** Module L's full coverage requires one of:
  - **(a)** A workforce-management product (Kronos, ADP, Homebase, When I Work, Deputy, etc.) feeding Canary directly — integration burden, customer pays for two systems
  - **(b)** Counterpoint's underlying SQL database queried out-of-band — out of scope for the public REST API; brittle; customer-permission dependent
  - **(c)** Deferred coverage until an alternative source is identified — Module L sits gappy in the CRDM
  - **(d) Canary-native labor scheduling module** — treat the Counterpoint REST gap as a product wedge. Build Module L inside Canary as a one-stop-shop differentiator for SMB retailers. POS-data-native: schedule from sales velocity in CRDM, not generic forecasts. Tradeoffs: real compliance burden (overtime, breaks, jurisdiction-specific labor laws), crowded category (Homebase et al. are mature), Phase 6+ work not Phase 1. **This is a product-strategic option — escalate to founder before committing roadmap scope.** See memory: `project_canary_native_labor_module_opportunity.md`.
- **MCP tool surface (degraded for Phase 1):**
  - `get_api_users(company)` — derives from User/Role endpoints — operational user inventory only
  - Full `get_employees`, `get_timeclock`, `get_labor_cost`: **DEFERRED** until alternative upstream identified
- **TSP adapter:** Phase 1 implements only the User/Role surface. The full Module L is parked.
- **Recommended scope adjustment:** **drop L from Phase 1 priority modules**; defer to a separate workforce-data dispatch.

### 6.13 Module W — Work Execution

> **REVISED 2026-04-25 post deep-dive:** Counterpoint's REST API has **no work-execution / task / checklist endpoints**. Module W is fully out of Counterpoint scope.

- **Spine intent:** daily operating tasks, store-floor workflows, ops checklists
- **Counterpoint endpoints (verified):** none
- **CRDM entities:** `Workflows.tasks`, `Workflows.checklists` — must be sourced from upstream system other than Counterpoint
- **ARTS:** N/A (not in core ARTS)
- **Implication options** (parallel to Module L's option set):
  - **(a)** Source from a task-management / store-ops product (Beekeeper, YOOBIC, Foko Retail, etc.) feeding Canary directly — third-party tool, customer pays for two systems
  - **(b)** Custom store-ops tool (customer-built) — customer cost, integration burden
  - **(c)** Defer — Module W sits gappy in CRDM
  - **(d) Canary-native work-execution module** — same one-stop-shop wedge framing as Module L. Native task management, daily-ops checklists, store-floor workflows inside Canary. Tradeoffs: store-ops UI is a real surface to build, mature competitors exist, Phase 6+ work not Phase 1. **Same product-strategic call as Module L; escalate to founder before committing roadmap scope.** See memory: `project_canary_native_labor_module_opportunity.md` (which covers the wedge logic generically).
- **MCP tool surface:** N/A (out of scope for Counterpoint integration; lives in Module W's own product surface if option (d) chosen)
- **TSP adapter:** N/A (no Counterpoint endpoints)
- **Recommended scope adjustment:** **remove Module W from Phase 3** of the Counterpoint build plan. Phase 3 covers D + J only; W becomes a separate effort with its own SDD if/when it's prioritized.

## 7. Cross-cutting concerns

### 7.1 Idempotency

All TSP upserts keyed on Counterpoint primary keys (e.g., `customer_id`, `document_id`, `item_id`). Replay-safe. Adapter writes are idempotent UPSERTs at the CRDM boundary.

### 7.2 Error handling

| HTTP status | Handling |
|---|---|
| 200 OK | Process response |
| 401 Unauthorized | Re-authenticate; rotate creds if 401 persists after re-auth |
| 403 Forbidden | Check APIKey + per-endpoint role permissions; surface to operator |
| 404 Not Found | Log as warning; continue |
| 429 Too Many Requests | Exponential backoff; alert if sustained |
| 5xx | Backoff + retry (3x, exponential); alert if 3 retries fail |

### 7.3 Batching + pagination

- Default batch size: 100 records per request
- Max batch: 1000 records (per Counterpoint API server pagination guidance — verify)
- Pagination via skip/take parameters (see `Basics/Requests.md`)
- Long sync jobs: chunked + checkpointed in CRDM `sync_state` table

### 7.4 Monitoring + alerting

- Per-endpoint sync timestamp + record count → CRDM `sync_telemetry` table
- Drift alerts: if no records in expected window for a given endpoint
- Auth-failure alerts: any 401 or 403
- Latency alerts: p95 latency > N seconds for a given endpoint
- Alert sink: TBD (Linear / Slack / PagerDuty integration)

### 7.5 Multi-version Counterpoint

- Adapter supports v8.5.x and v8.6.x (current Counterpoint API tested versions)
- Version detection via `DB_CTL.DB_VER` query (per NCR README)
- Per-version branching only where API surface differs

### 7.6 Multi-company

- Counterpoint API server is multi-company capable; one Canary tenant may map to multiple Counterpoint companies
- Authentication uses `<company>.<username>` prefix
- CRDM `tenant_id` distinguishes Canary tenants; nested `company_id` per Counterpoint company

## 8. Implementation phasing

Reproduced from build plan; canonical source is `docs/superpowers/plans/2026-04-25-ncr-counterpoint-spine-build.md`.

| Phase | Modules | Output |
|---|---|---|
| 0 | TSP rebuild + CRDM + adapter shell | foundation, no module endpoints yet |
| 1 | T, R, F, L, N | priority modules |
| 2 | P, S | catalog modules (H&G-critical) |
| 3 | D, W, J | operations modules |
| 4 | A, C, Q | tertiary modules (Q comes last because it consumes earlier modules) |
| 5 | cutover + monitoring | runbook + alerting + capacity |

## 9. Acceptance criteria

Per-module:

- [ ] CRDM mapping documented
- [ ] TSP adapter implemented + integration-tested against the public Counterpoint API surface
- [ ] At least one MCP tool surface exposed
- [ ] Fixture suite: happy path + 5 edge cases
- [ ] Wiki article updated with Counterpoint-mapping section

Program-level (see build plan §Acceptance criteria for full list):

- [ ] All 13 modules complete per per-module criteria
- [ ] First production deployment to Boutique H&G chain succeeds
- [ ] Memory-bus has SDD chunked + recallable per module

## 10. Risks

(Reproduced + extended from build plan)

- **Customer license gating** — `registration.ini` API user option (paid add-on)
- **Windows-on-prem assumption** — Counterpoint API server requires Windows + .NET 4.5.2
- **POSLog version drift** — 2.x primary, v4 backward, v6 forward
- **Endpoint surface scope** — 95 documented endpoints (97 files, 2 stubs); ~25 actually needed in steady state
- **Multi-version Counterpoint** — must test v8.5 + v8.6
- **API user option requirement** — bulk of endpoints require it; some "limited functions" work without it (per NCR README) — Canary's must-haves all fall in the requires-API-option bucket
- **Card-on-file tokenization** — separate concern; see `TokenizationUtility.md`. Canary likely does NOT touch this, but adapter must avoid leaking PAN data
- **Multi-company complexity** — one customer may have multiple Counterpoint companies (e.g., legal entities, store groupings); CRDM must accommodate without conflating

## 11. Open questions (status updated 2026-04-25 post deep-dive)

| # | Question | Status |
|---|---|---|
| 1 | Does Counterpoint expose ticket-line items as nested in Document or as separate endpoint? | **ANSWERED — NESTED.** Lines are in `PS_DOC_LIN[]` array on the Document response (per `Brain/wiki/ncr-counterpoint-document-model.md`). `POST_Document_Lines` exists for adding lines but reads come whole. |
| 2 | How does Counterpoint distinguish void-of-sale from return at the data-model level? | **Mostly answered** — Documents reference originating tickets via `PS_DOC_HDR_ORIG_DOC[]` array; return vs. void distinguished by DOC_TYP code (exact codes pending verification with non-sale samples) |
| 3 | Customer-tier representation in CustomerControl — how many tiers, how named? | **ANSWERED.** Customer tier = `CATEG_COD` field on the Customer record (e.g., "MEMBERS"). User-defined codes; not enumerated at CustomerControl level. CustomerControl carries system-level customer config (aging periods, custom-field enablement, loyalty enabled flag) but not tier definitions. |
| 4 | Loyalty program data — separate endpoint or embedded in Customer? | **ANSWERED — EMBEDDED.** Customer record has `LOY_PGM_COD`, `LOY_PTS_BAL`, `TOT_LOY_PTS_EARND`, `TOT_LOY_PTS_RDM`, `TOT_LOY_PTS_ADJ`, `LOY_CARD_NO`, `LST_LOY_EARN_TKT_DAT/TIM`, `LST_LOY_PTS_EARN`, `LST_LOY_EARN_TKT_NO`, `LST_LOY_PTS_RDM`, `LST_LOY_ADJ_DAT`, `LST_LOY_PTS_ADJ`. CustomerControl has `USE_LOY_PGMS: Y/N` system flag. |
| 5 | Does Counterpoint expose timeclock via REST? | **ANSWERED — NO.** Module L cannot be sourced from Counterpoint REST. See §6.12 revised. |
| 6 | Replenishment engine REST? | **Mostly answered** — likely UI-only; derive from VendorItem + Inventory_ByLocation |
| 7 | Lawn/garden module's custom fields on Item | **Mostly answered.** Items have `CATEG_COD` + `SUBCAT_COD` (2-level), `ATTR_COD_1` + `ATTR_COD_2` (extensible attributes), `MIX_MATCH_COD` (mix-and-match group), `ITEM_TYP` (I/K/etc.), `IS_TXBL`, `IS_FOOD_STMP_ITEM`, ecommerce flags. Mix-and-match IS exposed via API as a code reference. Plant-specific custom fields likely use the attribute codes. Customer-level custom fields use 5×4 (alpha/code/date/number) profile slots enabled in CustomerControl. |
| 8 | Promotion stacking + effective-dating semantics | **ANSWERED — N/A.** No Promotion endpoint exists; Module P is derived. See §6.11 revised. |
| 9 | Multi-company addressing strategy | **ANSWERED.** `<CompanyAlias>.<UserName>` auth prefix; CRDM tenant_id × counterpoint_company_alias |
| 10 | Workflow / task in Counterpoint | **ANSWERED — NO.** Module W not sourced from Counterpoint. See §6.13 revised. |

New questions surfaced post deep-dive:

| # | Question | Status |
|---|---|---|
| 11 | What is `POST_NSPTransaction`? | **ANSWERED.** Endpoint to record secure-pay transactions from **Monetra** (a payment processor / gateway). Used by Counterpoint customers using Monetra. NSP = Non-Standard Payment. Resulting payments still appear as Document_Payments in normal Documents — Canary doesn't need to touch NSPTransaction directly. |
| 12 | What is `GET_Workgroup`? | **ANSWERED.** Workgroup is a **store / location grouping** concept (multi-store coordination). Each workgroup has next-number generators for transactions, transfers, POs, etc. Carries `THIS_LOC_ID`, `THIS_STR_ID`, `LOC_GRP_ID`. NOT a labor workgroup. Useful for Module N hierarchy + multi-store deployments. |
| 13 | What does `GET_Document` payload look like? | **ANSWERED.** See `Brain/wiki/ncr-counterpoint-document-model.md`. PS_DOC_HDR + 11 nested arrays (lines, payments, taxes, audit, etc.). Document is omnibus: covers sales, returns, voids, transfers, POs, RTVs, GFC. |
| 14 | What's in `GET_CustomerControl`? | **ANSWERED.** AR_CTL record: aging-period config (4 periods + messages), customer-profile field enablement (5 each of alpha/code/date/number), loyalty-program system flag, statement settings. Does NOT define tiers; tiers are user-defined codes on the Customer record's CATEG_COD field. |
| 15 | Counterpoint Document type-code taxonomy | **Partially answered** — at minimum: `T` (ticket/sale), `XFER`, `RECVR`, `PO`, `PREQ`, `RTV`, `STC`, `EVENT`, `GFC`, `AR_DOC` (inferred from Workgroup's next-number generators). Need to read additional sample payloads to confirm exact DOC_TYP code strings. |

**Status summary post 2026-04-25 deep-dive:**

- 9 of 10 original open questions ANSWERED or MOSTLY ANSWERED
- 4 of 5 new questions ANSWERED
- Remaining open: exhaustive DOC_TYP code list (Q15 partial), void-DOC_TYP-vs-return semantics edge cases, IS_OFFLINE / IS_DOC_COMMITTED behavior

The SDD is sufficiently grounded for Phase 0–1 implementation. Remaining gaps surface during fixture-test development against an NCR sandbox.

## 12. Phasing dependencies + serialization gates

```
Phase 0 (foundation) ──┬─→ Phase 1 (T R F L N) ──┬─→ Phase 4 (A C Q)
                       │                          │
                       └─→ Phase 2 (P S) ─────────┘
                       │                          │
                       └─→ Phase 3 (D J) ──────────┘
                                                  │
                                                  └─→ Phase 5 (cutover)
```

Phases 1, 2, 3 can run in parallel after Phase 0 if multiple sessions / engineers are available. Phase 4 (especially Q — Loss Prevention) depends on Phases 1–3 outputs. Phase 5 depends on all prior phases.

## 13. Related

- `docs/superpowers/plans/2026-04-25-ncr-counterpoint-spine-build.md` — companion build plan (operational)
- `Brain/dispatches/2026-04-25-tsp-crdm-counterpoint-flow.md` — Phase 0 dispatch
- `Brain/wiki/canary-tsp-pipeline.md` — current TSP architecture
- `Brain/wiki/canary-data-model.md` — current CRDM
- `Brain/wiki/canary-module-*.md` — per-module spine wikis
- `Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/` — source corpus
- `docs/sdds/canary/ncr-counterpoint-openapi.yaml` — derived OpenAPI 3.0 spec (validates; 95 ops / 71 paths / 49 schemas)
- `Brain/wiki/ncr-counterpoint-endpoint-spine-map.md` — per-endpoint × CRDM × spine mapping table + coverage gap report
- `Brain/wiki/ncr-counterpoint-connection-runbook.md` — Windows-host stand-up + smoke tests + auth bootstrap
- `CATz/method/phases/phase-2-select-and-implement.md` — CATz Phase II frame
- `docs/audit-2026-04-23/secret-rotation-runbook.md` — secret-rotation procedure (relevant for per-customer Counterpoint creds)

---

**Author:** Senior ALX (laptop), 2026-04-25
**Status:** draft-1 — open questions remain; Phase 0 execution will surface answers to many
**Review gate:** founder reviews before Phase 1 dispatch is written
