---
classification: internal
type: wiki
date: 2026-04-25
last-compiled: 2026-04-25
needs-review: 2026-05-09
source: github.com/NCRCounterpointAPI/APIGuide v2.4 (cloned 2026-04-25 into Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/)
companion-sdd: docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md
---

# NCR Counterpoint API Reference

Canonical reference for the NCR Counterpoint REST API surface as relevant to Canary integration. Built from a systematic read of the 97-endpoint repo. **This is the synthesis layer**; the source repo at `Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/` is authoritative.

## Properties at a glance

| Property | Value | Source |
|---|---|---|
| API style | REST over HTTPS | README |
| Implementation | .NET 4.5.2, ServiceStack framework | README |
| Auth | HTTP Basic + APIKey header (most endpoints) | Basics/Requests.md |
| Username format | `<CompanyAlias>.<UserName>` for company endpoints; bare username for system admin | Basics/Requests.md |
| Date format | ISO 8601 (`yyyy-mm-ddThh:mm:ss`) | Basics/DateFormats.md |
| Content type | JSON in/out | Basics/Requests.md |
| Hosting | On-prem Windows (7+ desktop / Server 2012 R2+), customer-side | README |
| Multi-company | Single API server can serve many Counterpoint companies | README |
| Multi-version | Detects version via `DB_CTL.DB_VER`; supports v8.5.x + v8.6.x officially | README |
| Versioning | API versions 2.0 → 2.4 (current); release notes in Release_Notes/ | README |
| Gating | "API user option" in `registration.ini` (paid Counterpoint license add-on); most endpoints require it | README |
| HTTP errors | 200 / 201 / 400 / 401 / 403 / 404 / 500 | Basics/Responses.md |
| Error envelope | `{ErrorCode, Message}` with structured ErrorCodes enum | Basics/Responses.md |
| Caching | 24h server-side cache for static-ish data; invalidate via `ServerCache: no-cache` header or DELETE /CACHE | Basics/Requests.md |

## Authentication detail

```
Authorization: Basic <base64(<CompanyAlias>.<UserName>:<password>)>
APIKey: <provisioned-per-app-key>
```

- Base64 is encoding, not encryption — security comes from TLS
- 401 = bad credentials; 403 = APIKey missing/invalid OR `registration.ini` API option not enabled
- System admin endpoints don't carry company prefix; default install user is `admin`
- Per-customer credentials are best stored in Canary's secret store, rotated per `docs/audit-2026-04-23/secret-rotation-runbook.md`

## Caching policy

The server caches the following data for 24 hours from first read:

- Company, Customer Control, Databases, eCommerce Control, eCommerce Categories
- Gift Card Codes, Inventory Control, Item Categories, Items (metadata; NOT inventory level), PayCodes, Stores, Stations, Tax Codes, Workstations

POSTs through the API auto-update the cache. Out-of-band edits (UI / direct DB) do NOT — Canary's adapter must:
- Send `ServerCache: no-cache` on first poll of each cycle if external changes are possible
- Or call `DELETE /CACHE` to flush

For high-cadence polling against transactional endpoints (Documents), cache is not a concern — transactional data isn't cached.

## Error codes

```
SUCCESS
ERROR_MISSING_REQUIRED_DATA
ERROR_RECORD_NOT_FOUND
ERROR_UNKNOWN
ERROR_DOCUMENT_ALREADY_COMPLETED
ERROR_INVALID_APIKEY
ERROR_DOCUMENT_NOT_FULLY_PAID
ERROR_CARD_PAYMENT_FAILED
ERROR_INVALID_GIFTCARD_PAYMENT
ERROR_AR_PAYMENT_FAILED
ERROR_INVALID_LIN_TYP
ERROR_NOT_PURE_ORDER
ERROR_DOCUMENT_HAS_SHIPPING_ADDRESS
ERROR_DOCUMENT_HAS_BILLING_ADDRESS
ERROR_INVALID_CONTACT_ID
ERROR_DOCUMENT_BILLING_ADDRESS_NOT_FOUND
ERROR_DOCUMENT_SHIPPING_ADDRESS_NOT_FOUND
ERROR_INVALID_CONFIGURATION
```

Canary's adapter maps these to internal error categories. `ERROR_INVALID_APIKEY` and `ERROR_RECORD_NOT_FOUND` are the two most operationally common.

## Endpoint catalog by category

### System administration (~17 endpoints)

Out-of-scope for Canary's runtime path. Used during initial customer provisioning.

- **API users + roles**: `GET/POST/PUT/DELETE_AdminUser(s)`, `POST_APIAdmin`, `GET_Role(s)`, `GET_Role`, `PUT/DELETE_Role`, `GET/PUT/DELETE_RoleUsers`, `GET_RoleEndpoints`, `GET_RoleNames`, `GET/PUT/DELETE_UserRoles`
- **API keys**: `GET_APIKey(s)`, `POST_APIKey`
- **Companies**: `GET_Company`, `GET/POST/PUT/DELETE_CompanyAdmin(s)`
- **Databases**: `GET_Database(s)`, `GET_Databases_Ini`, `POST_Databases`, `PUT/DELETE_Database`
- **System info**: `GET_SystemInfo`

### Spine Module N — Device / Stores / Stations (6 endpoints)

- `GET_Store` — single store detail
- `GET_StoreTokenizeInfo`, `GET_StoresTokenized`, `POST_StoreTokenize` — card-on-file tokenization scope
- `GET_Store_Station` — station / register info
- `GET_Device_Config` — device-level configuration
- `GET_Workgroup` — likely store-grouping concept (verify by reading the doc)

CRDM mapping: `Places.stores`, `Places.stations`, `Places.devices`, `Places.workgroups` (new).

### Spine Module T — Transactions / Documents (11 endpoints)

- `GET_Document` — read sales ticket / order / transfer / etc.
- `POST_Document` — create
- `POST_Document_Lines` — add line items
- `GET/POST/PUT/DELETE_Document_Contact` — billing/shipping contacts on a document
- `GET/POST/PUT/DELETE_Document_Note` — notes
- `POST_Document_Payments` — record payment
- `POST_NSPTransaction` — Non-Standard Payment Transaction (verify; possibly card-not-present or external-tender)

CRDM mapping: `Events.transactions`, `Events.transaction_lines`, `Events.payments`, `Events.contacts`, `Events.notes`.

**Document is the omnibus container.** "Documents" in Counterpoint includes sales tickets, orders, transfers, returns, voids — all expressed as Document records with different type codes. **This means Module T, Module D (transfers), and possibly Module J (orders) all flow through the same endpoint family**, distinguished by Document type. Critical for adapter design.

### Spine Module R — Customer (17 endpoints)

- `GET_Customer`, `GET_Customers`, `GET_Customers_EC` (ecommerce customers), `POST_Customer`, `PATCH_Customer`
- `GET_CustomerControl` — system-level customer config (tier definitions, defaults). **Cached.**
- `GET/POST/PATCH/DELETE_Customer_Address`
- `GET/POST/PATCH/DELETE_Customer_Note`
- `GET_Customer_OpenItems` — open AR balances
- `POST/PATCH/DELETE_Customer_Card` — card-on-file management

CRDM mapping: `People.customers`, `People.customer_addresses`, `People.customer_notes`, `Events.ar_balances`.

**B2B vs retail tier**: lives in CustomerControl + Customer-record fields. Multi-tier customer pricing relies on this — Module P depends on R for tier mapping.

### Spine Module S — Items / Catalog (~17 endpoints)

- `GET_Item`, `GET_Items`, `GET_Items_ByLocation`
- `GET_ItemCategories`, `GET_ItemCategory`
- `GET_ItemSerial`, `GET_ItemSerials`
- `GET_Item_Images`, `GET_Item_ImageFilename`
- `GET_Item_Inventory`
- `GET_Inventory_ByLocation`, `GET_InventoryControl`, `GET_InventoryCost`, `GET_InventoryEC`, `GET_InventoryLocations`
- `GET_VendorItem`
- `GET_EC`, `GET_ECCategories` (ecommerce catalog)

CRDM mapping: `Things.items`, `Things.item_categories`, `Things.item_serials`, `Things.item_images`, `Things.item_inventory_by_location`, `Things.vendor_items`.

**Caching matters**: Items metadata is cached. Inventory level is NOT (transactional). Adapter polls items rarely; inventory continuously.

### Spine Module F — Finance / Tenders / Tax (8-10 endpoints)

- `GET_PayCode`, `GET_PayCodes`, `PUT_PayCode` — tender taxonomy. **Cached.**
- `GET_GiftCard`, `GET_GiftCards`, `GET_GiftCardCode`, `GET_GiftCardCodes` — gift card detail + lookup
- `GET_TaxCodes` — tax code list. **Cached.**
- `POST_Document_Payments` — write side (also Module T)
- `POST_NSPTransaction` — non-standard payment (also touches T)

CRDM mapping: `Events.payments`, `Events.taxes`, `Things.gift_cards`, `Things.tax_codes`, `Things.pay_codes`.

**Tax detail level**: Counterpoint exposes a TaxCodes list. Tax application per transaction lives in Document (line-level tax fields). No tax-authority hierarchy or jurisdiction lookup at the API level.

### Spine Module L — Labor / Workforce (NEAR-ZERO Counterpoint coverage)

**Open question §6.12 in SDD: ANSWERED.** Counterpoint's REST API does NOT expose:
- Employees as a domain entity
- Timeclock / time records
- Schedule / availability
- Labor cost detail

What it DOES expose (User/Role endpoints) is API-level access management, not workforce data.

**Implication**: Module L cannot be sourced from Counterpoint REST. Canary needs another upstream system for L (e.g., a workforce-management product, or store-level timeclock data exported via a different channel). The SDD must be updated.

### Spine Module P — Pricing / Promotion (NO dedicated endpoints)

**Open question §6.11 in SDD: PARTIALLY ANSWERED.** Counterpoint's REST API does NOT expose:
- A Pricing endpoint family
- A Promotion endpoint family
- Pricing rule definitions

What it DOES expose:
- Item-level prices (in `GET_Item` payload — verify by reading the endpoint doc)
- Customer tier flags (in `CustomerControl` + per-Customer fields)
- Multi-tier customer pricing is therefore DERIVED at consume-time, not directly modeled

**Implication**: Module P's mapping in the SDD needs revision. The "MCP tool surface" for P depends on derived computation across Item + Customer; there's no direct "get_active_promotions" endpoint to call.

### Spine Module D — Distribution (4-5 endpoints, partially via Documents)

- `GET_InventoryLocations`, `GET_Inventory_ByLocation`, `GET_Items_ByLocation` — inventory snapshots per location
- `GET_VendorItem` — vendor-item relationships

**Transfers** (the workflow side of Distribution) likely flow through `POST_Document` with a transfer-type code, not a separate endpoint. Confirms SDD §6.7 hypothesis that Document is the omnibus.

### Spine Module J — Forecast / Order (sparse)

- `GET_VendorItem` — vendor item info (touches J)
- Order-type Documents (via POST_Document with order type) — verify

**No dedicated forecasting endpoints.** Replenishment engine is likely UI-only or driven by integrations external to the API.

### Spine Modules A, C, Q, W — no Counterpoint coverage

- **A (Asset Management)**: no dedicated endpoints; non-saleable items might be flagged in Item, but no asset-lifecycle data
- **C (Commercial / B2B)**: derived from Customer + Customer_OpenItems + AR-related fields; no separate B2B endpoint family
- **Q (Loss Prevention)**: Canary-internal; no Counterpoint endpoints
- **W (Work Execution)**: confirmed absent from Counterpoint REST

## Cross-cutting findings — adapter design implications

### Document is the omnibus

A single endpoint family handles sales, returns, voids, transfers, orders. Adapter must:
- Filter by Document type code
- Route to the correct CRDM event entity per type
- Detect type codes via `GET_Document` payload inspection (verify by reading the endpoint doc)

### Caching is the friend

Static-ish data (Stores, PayCodes, TaxCodes, Item categories, Customer Control) is cached server-side for 24h. Canary's adapter:
- Polls these at low cadence (daily / on-demand)
- Uses `ServerCache: no-cache` only when staleness is suspected
- Polls Documents + inventory levels at high cadence (continuously / minute-level)

### Multi-company is real

API server maps `<company>.<user>` per request. Canary's tenancy model needs:
- `tenant_id` (Canary tenant)
- `counterpoint_company_alias` (per-tenant; one Canary tenant can have N Counterpoint companies)
- Credentials stored per `(tenant_id, company_alias)` tuple

### What's NOT in the API surface

Pre-built Phase 1+ assumptions to revise based on this finding:

1. **Module L** — needs external upstream (workforce-management vendor)
2. **Module P** — derived, not direct; SDD §6.11 needs rework
3. **Module W** — out of Counterpoint scope entirely; alternative upstream needed if W is on the roadmap

These three findings should be folded into the SDD's per-module sections and the Phase 1 dispatch's scope clarification questions.

## Phase priorities (refined post-deep-dive)

| Phase | Modules | Counterpoint coverage | Adapter complexity |
|---|---|---|---|
| 0 (foundation) | TSP/CRDM shell | N/A | Medium |
| 1 (priority) | T R N F | High | Medium |
| 1 (priority — degraded) | L | **near-zero — needs upstream alternative** | Low (just User/Role surface) |
| 2 (catalog) | S | High | Medium |
| 2 (catalog — derived) | P | Derived from S + R | High (derivation logic) |
| 3 (operations) | D (partial), J (partial) | Document-omnibus | Medium |
| 3 (operations — gap) | W | **out of scope — needs upstream alternative** | N/A |
| 4 (tertiary) | A (partial), C (derived from R), Q (Canary-internal) | Sparse | Low |
| 5 (cutover) | runbook + monitoring | N/A | Low |

**Recommended scope adjustment**: Phase 1 drops L from the priority list (defer to a separate workforce-data dispatch). Replace L in Phase 1 with explicit treatment of S (currently in Phase 2) — moving S forward gives Module Q (Phase 4) substrate sooner.

Decision pending founder review.

## Open questions remaining (post-deep-dive)

Of the SDD's original 11 open questions:

| # | Question | Status |
|---|---|---|
| 1 | Document line items nested vs separate | Open — read GET_Document next |
| 2 | Void vs return distinction | Open — read GET_Document next |
| 3 | Customer-tier representation | Mostly answered: in CustomerControl + Customer fields. Read GET_CustomerControl + GET_Customer for confirmation |
| 4 | Loyalty program data | Open — likely embedded in Customer |
| 5 | Timeclock via REST | **ANSWERED — NO** |
| 6 | Replenishment engine REST | Mostly answered — likely UI-only; derive from VendorItem + Inventory_ByLocation |
| 7 | Lawn/garden custom fields on Item | Open — read GET_Item next |
| 8 | Promotion stacking | **ANSWERED — no Promotion endpoint exists; module P is derived** |
| 9 | Multi-company strategy | **ANSWERED — `<company>.<user>` auth prefix; CRDM tenant_id × company_alias** |
| 10 | Workflow / task in Counterpoint | **ANSWERED — NO** |

Plus new questions surfaced:

11. What is `POST_NSPTransaction`? (Non-Standard Payment? specific use?)
12. What is `GET_Workgroup`? (store grouping for hierarchy / region?)
13. What does `GET_Document` payload look like? (line items, type codes, void/return semantics)
14. What's in `GET_CustomerControl`? (tier definitions, customer-default fields)

Next reads to close these: GET_Document, GET_Customer, GET_CustomerControl, GET_Item, GET_Workgroup, POST_NSPTransaction.

## Source

`Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/` — full repo, 97 endpoint docs, Basics/, InstallationAndConfiguration/, Release_Notes/.
