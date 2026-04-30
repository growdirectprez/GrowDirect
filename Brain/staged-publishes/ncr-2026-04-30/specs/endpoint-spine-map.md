---
title: Endpoint × Spine Map
tags: [specs, counterpoint, endpoints, spine, crdm]
nav_order: 54
audience: NCR Counterpoint VARs
last-updated: 2026-04-30
---

---
classification: internal
type: wiki
status: active
date: 2026-04-25
last-compiled: 2026-04-25
needs-review: 2026-05-09
source: github.com/NCRCounterpointAPI/APIGuide v2.4 (cloned)
----

# NCR Counterpoint API — Endpoint × CRDM × Spine Map

## Governing thesis

The Counterpoint REST API surface is dominated by three things — customer
master, item master, and document (transaction) — and almost everything
else is plumbing or thin metadata around them. Mapped to Canary's CRDM
classes and the spine letter scheme used in the Counterpoint integration
SDD, the 95 documented endpoints (97 files minus 2 stubs) cluster
unambiguously around **T (Transactions)**, **R (Customer)**, **S (Space /
Range / Display)**, **F (Finance)**, and **N (Device)**. Modules **L
(Labor)** and **W (Work Execution)** have zero coverage from this surface
and must be sourced elsewhere or deferred.

This article is the per-endpoint detail companion to
`docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md` §4–§6. The
SDD asserts module groupings at the endpoint-family level; this article
checks that assertion endpoint-by-endpoint and flags the few places where
the per-endpoint reading argues for a different module than the SDD's
family-level reading.

It is **not** a redefinition of the spine letter scheme — that lives in
`Brain/wiki/retail-integration-spine.md` (canonical C / D / F / J / S
active; P / R placeholder) and is extended by the SDD with **L Labor**, **W
Work Execution**, plus letters **T / R / N / Q / A / C** that the SDD uses
to address Canary's own module decomposition. Where the SDD letters
diverge from the canonical spine wiki, the SDD is the operative scheme for
this Counterpoint engagement; the divergence is itself flagged in the gap
report below.

## Method

For each of the 97 endpoint files in `Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/Endpoints/`:

1. Read method + path verbatim from the file header (or README chart where
   the file header is generic).
2. Identify the dominant Counterpoint table prefix (`AR_CUST`, `IM_ITEM`,
   `PS_DOC_HDR`, `PS_STR`, `EC_*`, `SY_*`).
3. Map to a CRDM entity class: People · Places · Things · Events ·
   Workflows · platform.
4. Assign a spine module letter from SDD §4 — or `platform` for endpoints
   that exist purely to operate the API server (APIKey, AdminUser,
   Database, Role, SystemInfo).

## Mapping table

Endpoints are grouped by resource noun. Two source files
(`GET_Customer_Address.md`, `GET_Customer_Note.md`) are header-only
placeholders with no documented endpoint and are listed here for
inventory completeness, marked `(stub-only)`. Total rows: **97** (95
real + 2 stub).

### Platform — system administration

| Method + Path | CRDM class | Spine module | Notes |
|---|---|---|---|
| `GET /SystemInfo` | platform | platform | Server health. No APIKey, sysadmin only. |
| `GET /AdminUsers` | platform | platform | Lists API server admins. |
| `DELETE /AdminUser/{UserId}` | platform | platform | Removes an admin. |
| `POST /User/Admin` | platform | platform | File `POST_APIAdmin.md`. Adds sysadmin. README chart says registration option required — likely a chart bug. |
| `GET /APIKey` | platform | platform | Stub-light; introspects one key. |
| `GET /APIKeys` | platform | platform | Lists installed keys, force-reloads cache. |
| `POST /APIKey` | platform | platform | Installs a signed XML key. |
| `GET /Company` | platform | platform | SY_COMP + DB_CTL metadata. Could arguably be **N** (places — site-of-record), but for this engagement it is treated as platform metadata and surfaced once at tenant-bootstrap time. |
| `GET /CompanyAdmins/{CompanyName}` | platform | platform | |
| `POST /CompanyAdmins/{CompanyName}` | platform | platform | |
| `PUT /CompanyAdmins/{CompanyName}` | platform | platform | |
| `DELETE /CompanyAdmin/{CompanyName}/{AdminUser}` | platform | platform | |
| `GET /Database/{Id}` | platform | platform | Counterpoint company registration. |
| `PUT /Database/{Id}` | platform | platform | |
| `DELETE /Database/{Id}` | platform | platform | |
| `GET /Databases` | platform | platform | |
| `POST /Databases` | platform | platform | |
| `GET /Databases/ini` | platform | platform | Reads companies.ini for bulk-add UX. |

### Platform — authorization (Roles, Users)

| Method + Path | CRDM class | Spine module | Notes |
|---|---|---|---|
| `GET /Role/Endpoints` | platform | platform | Lists endpoint+verb pairs grantable to roles. |
| `GET /Role/{RoleName}` | platform | platform | |
| `PUT /Role/{RoleName}` | platform | platform | |
| `DELETE /Role/{RoleName}` | platform | platform | |
| `GET /Role/{RoleName}/Users` | platform | platform | |
| `PUT /Role/{RoleName}/Users` | platform | platform | |
| `GET /Roles` | platform | platform | |
| `GET /Roles/Names` | platform | platform | |
| `GET /Roles/Users` | platform | platform | |
| `GET /User/{UserID}` | platform | platform | API-level user introspection. NOT Counterpoint employees — see SDD §6.12 L Labor open question. |
| `GET /User/{UserID}/Roles` | platform | platform | |
| `PUT /User/{UserID}/Roles` | platform | platform | |
| `DELETE /User/{UserID}/Roles` | platform | platform | |
| `PUT /User/Password` | platform | platform | |
| `GET /Users` | platform | platform | |
| `GET /Users/{CompanyName}` | platform | platform | |
| `GET /Users/Roles` | platform | platform | |

### Customer — module R

| Method + Path | CRDM class | Spine module | Notes |
|---|---|---|---|
| `POST /Customer` | People | R | AR_CUST insert. Workgroup-template fallback. |
| `GET /Customer/{CustNo}` | People | R | Returns AR_CUST + nested AR_CUST_NOTE / AR_SHIP_ADRS / AR_CUST_CARDS. |
| `PATCH /Customer/{CustNo}` | People | R | |
| `GET /CustomerControl` | People | R | AR_CUST_CTL — defaults + loyalty enable. **Cross-cuts to module P** for multi-tier customer pricing flags (per SDD §6.11). |
| `GET /Customers` | People | R | Paginated, RS_UTC_DT-filterable. The incremental-sync workhorse. |
| `GET /Customers/EC` | People | R | eCommerce-flagged customers. Spine module **R** primary, with a **C Commercial** dotted-line (B2B accounts often live here). |
| `GET /Customer/{CustNo}/OpenItems` | People | R | AR_OPN_ITEM aging. **Cross-cuts to module F** (AR is finance) and **C Commercial** (B2B credit). |
| `POST /Customer/{CustNo}/Address` | People | R | AR_SHIP_ADRS insert. |
| `PATCH /Customer/{CustNo}/Address` | People | R | Source file `PATCH_Customer_Address` lacks `.md` extension. |
| `DELETE /Customer/{CustNo}/Address` | People | R | |
| `POST /Customer/{CustNo}/Card` | People | R | AR_CUST_CARDS. Source file path is lowercase (`/customer/{custNo}/CARD`); README normalizes. **Cross-cuts to tokenization**. |
| `PATCH /Customer/{CustNo}/Card` | People | R | |
| `DELETE /Customer/{CustNo}/Card` | People | R | |
| `POST /Customer/{CustNo}/Note` | People | R | AR_CUST_NOTE. |
| `PATCH /Customer/{CustNo}/Note` | People | R | |
| `DELETE /Customer/{CustNo}/Note` | People | R | |
| `GET /Customer/{CustNo}/Address` | People | R | **(stub-only)** — file is a placeholder, no documented endpoint. |
| `GET /Customer/{CustNo}/Note` | People | R | **(stub-only)** — file is a placeholder, no documented endpoint. |

### Document — module T (with F and Q downstream)

| Method + Path | CRDM class | Spine module | Notes |
|---|---|---|---|
| `POST /Document` | Events | T | PS_DOC_HDR insert. The single most important POST. **Q (Loss Prevention) consumes this.** |
| `GET /Document/{DocId}` | Events | T | Retrieves an unposted ticket. |
| `POST /Document/{DocId}/Contact` | Events | T | Bill-to / ship-to contact attach. |
| `PUT /Document/{DocId}/Contact` | Events | T | README chart labels this PATCH; source file is PUT. **Discrepancy logged.** |
| `DELETE /Document/{DocId}/Contact` | Events | T | |
| `POST /Document/{DocId}/Lines` | Events | T | PS_DOC_LIN append. |
| `POST /Document/{DocId}/Note` | Events | T | Source file is `POST_Document_Note.md.md` (double `.md`). **Discrepancy logged.** |
| `PUT /Document/{DocId}/Note` | Events | T | |
| `DELETE /Document/{DocId}/Note` | Events | T | |
| `POST /Document/{DocId}/Payments` | Events | T+F | PS_DOC_PMT — payment attach. **Primary T, secondary F (tender).** |

### Item / catalog — module S (with A as derived view)

| Method + Path | CRDM class | Spine module | Notes |
|---|---|---|---|
| `GET /Item/{ItemNo}` | Things | S | IM_ITEM master. |
| `GET /Items` | Things | S | Paginated, category/subcategory-filterable. **A (Asset Management) is a derived view of this** — filter on item-type / asset flag (per SDD §6.4). |
| `GET /Items/{LocId}` | Things | S+D | Per-location items. **Cross-cuts D (Distribution).** |
| `GET /ItemCategory/{CategoryCode}` | Things | S | |
| `GET /ItemCategories` | Things | S | Hierarchical list. |
| `GET /Item/{ItemNo}/Images` | Things | S | Filename list. |
| `GET /Item/Images/{Filename}` | Things | S | Image binary. |
| `GET /Item/{ItemNo}/Serial/{SerialNo}` | Things | S | SN_SER lookup. |
| `GET /Item/{ItemNo}/Serials/Location/{LocId}` | Things | S+D | Active serials at a location. |

### Inventory — module D (with cost slice in F)

| Method + Path | CRDM class | Spine module | Notes |
|---|---|---|---|
| `GET /Inventory/{LocId}` | Things | D | Per-location inventory of all items. The transfer/SOH workhorse. |
| `GET /Item/{ItemNo}/Inventory/{LocId}` | Things | D | Single-item-single-location IM_INV. |
| `GET /Item/{ItemNo}/InventoryCost/{LocId}` | Things | D+F | **Primary D, secondary F** — cost lives in finance. |
| `GET /Inventory/EC` | Things | D | eCommerce inventory snapshot. |
| `GET /InventoryControl` | Things | D | IM_INV_CTL (valuation method, default location). |
| `GET /Inventory/Locations` | Places | D | IM_LOC list. **Arguably N (Device/Site) primary — SDD §4 puts InventoryLocations in Places**; we keep D here for distribution semantics and flag the SDD overlap. |

### Vendor — module C / J seam

| Method + Path | CRDM class | Spine module | Notes |
|---|---|---|---|
| `GET /VendorItem/{VendorNo}/Item/{ItemNo}` | People+Things | C+J | Vendor-item linkage. **C (Commercial) primary** if framed as B2B-supplier master; **J (Forecast/Order) primary** if framed as procurement input. SDD §6.9 leans J; we adopt that. |

### Store / device — module N

| Method + Path | CRDM class | Spine module | Notes |
|---|---|---|---|
| `GET /Store/{StoreID}` | Places | N | PS_STR. |
| `GET /Store/{StoreID}/Station/{StationID}` | Places | N | PS_STA. |
| `GET /DeviceConfig/{WorkstationID}` | Places | N | **Not in README endpoint chart.** Source file documents `/DeviceConfig/{WorkstationID}` (the README sidebar mis-labels as `/Device_Config`). Discrepancy logged. |

### Tokenization — module F (Secure Pay tender)

| Method + Path | CRDM class | Spine module | Notes |
|---|---|---|---|
| `GET /Store/{StoreId}/Tokenize` | Events | F | Tokenization status. **No APIKey required**, registration option required. |
| `POST /Store/{StoreId}/Tokenize` | Events | F | Run tokenization on the store's cards-on-file. |
| `GET /Stores/Tokenized` | Events | F | Aggregate tokenized count per Secure Pay store. |
| `POST /NSPTransaction` | Events | F | Monetra Secure Pay transaction post-back. **No APIKey, no registration option.** |

### Pay codes / tax — module F

| Method + Path | CRDM class | Spine module | Notes |
|---|---|---|---|
| `GET /PayCode/{Paycode}` | Things | F | PS_PAY_COD. |
| `PATCH /PayCode/{Paycode}` | Things | F | README chart says PATCH; source file is `PUT_PayCode.md`. **Discrepancy logged.** |
| `GET /PayCodes` | Things | F | |
| `GET /TaxCodes` | Things | F | TX_COD list. |

### Gift card — module F (tender) with S (catalog code template)

| Method + Path | CRDM class | Spine module | Notes |
|---|---|---|---|
| `GET /GiftCard/{GiftCardNo}` | Things | F | SY_GFC. |
| `GET /GiftCards` | Things | F | Paginated. |
| `GET /GiftCardCode/{GiftCardCode}` | Things | F+S | SY_GFC_COD — code template. **F primary (tender), S secondary (template / SKU-ish).** |
| `GET /GiftCardCodes` | Things | F+S | |

### eCommerce — module S (with R for customers, F for tender via NSP)

| Method + Path | CRDM class | Spine module | Notes |
|---|---|---|---|
| `GET /EC` | Workflows | S | EC_CTL. |
| `GET /ECCategories` | Things | S | EC_CATEG. The eCommerce catalog hierarchy. |

### Workgroup — module R (template-driven defaults)

| Method + Path | CRDM class | Spine module | Notes |
|---|---|---|---|
| `GET /Workgroup/{WorkgroupID}` | Workflows | R | Template-customer + numbering defaults. **Used by POST /Customer**. |

## Coverage gap report

### Spine modules with rich Counterpoint coverage

- **T (Transactions)** — 10 endpoints. PS_DOC_HDR + nested PS_DOC_LIN /
  PS_DOC_PMT / PS_DOC_NOTE / PS_DOC_TAX / contacts. Full read + write.
  Adequate for Canary's core fact feed.
- **R (Customer)** — 18 endpoints (16 real + 2 stub). AR_CUST + ship-to
  + notes + cards + open items + control + workgroup-driven defaults.
  Best-covered domain in the API.
- **S (Space / Range / Display)** — 9 endpoints. Item master, categories,
  serials, images. eCommerce control + categories add 2 more. Adequate
  for catalog sync.
- **D (Distribution)** — 6 endpoints. Per-location inventory, control
  block, locations list, item-cost-by-location. Adequate for SOH +
  per-location reads. **No transfer endpoints exposed** — transfers
  must be derived from PS_DOC_HDR with transfer-typed DOC_TYP.
- **F (Finance)** — ~12 endpoints across pay codes, tax codes, gift
  cards, tokenization, NSP transactions, plus payment slice of Document.
  Adequate for tender / tax / Secure-Pay closing of the loop.
- **N (Device)** — 3 endpoints (Store, Station, DeviceConfig). Sufficient
  for the device-inventory side of the spine.

### Spine modules with partial / derived coverage

- **A (Asset Management)** — 0 dedicated endpoints. Per SDD §6.4 derived
  from `GET /Items` filtered on a non-saleable / asset flag. Schema
  dimension `ITEM_TYP` (`I` = inventory, `N` = non-inventory) is the
  most likely discriminator; explicit asset flag was not visible in the
  sample-derived schema and remains an SDD §6.4 open question.
- **C (Commercial)** — 0 dedicated endpoints. Derived from `GET /Customers`
  filtered on `CATEG_COD` / `ALLOW_AR_CHRG` / multi-tier indicators on
  `AR_CUST_CTL`, plus `GET /Customer/{CustNo}/OpenItems` for B2B AR. SDD
  §6.6 open questions remain.
- **J (Forecast / Order)** — 1 dedicated endpoint
  (`/VendorItem/{VendorNo}/Item/{ItemNo}`). No PO / replenishment /
  forecast endpoints in this corpus. Confirms SDD §6.9 open question:
  Counterpoint's replenishment engine appears UI-only at v2.4.
- **P (Pricing / Promotion)** — 0 dedicated endpoints. Pricing fields
  exist on `IM_ITEM` (`PRC_1`, `REG_PRC`, `PREF_UNIT_PRC_1`) and on
  `AR_CUST_CTL` (multi-tier flags). Promotions and effective-dating
  endpoints absent. Aligns with SDD §6.11 — deferred until Counterpoint
  exposes promotion endpoints or until a separate pricing system is
  integrated.
- **Q (Loss Prevention)** — 0 dedicated endpoints. **Not a gap** — Q is
  Canary-internal per SDD §6.5; consumes T+R+L+N substrate. The point of
  Q being last in phasing is that Counterpoint doesn't surface it.

### Spine modules with NO coverage

- **L (Labor)** — 0 endpoints. The corpus exposes API-server roles +
  users (treated as `platform` above), NOT Counterpoint employee
  records, timeclock, or scheduling. Confirms SDD §6.12 open question.
  Must be sourced from a separate workforce module or deferred.
- **W (Work Execution)** — 0 endpoints. No task / checklist / workflow
  surface. Confirms SDD §6.13 — must be sourced elsewhere.

### Discrepancies flagged

**File-count discrepancies:**

| Source | Endpoint count | Observation |
|---|---|---|
| `Endpoints/` directory listing | 97 files | Includes 2 stub-only files (`GET_Customer_Address.md`, `GET_Customer_Note.md`) and 1 file missing the `.md` extension (`PATCH_Customer_Address`) and 1 file with stutter extension (`POST_Document_Note.md.md`). |
| README.md endpoint chart | ~84 distinct method+path pairs | Chart omits `/DeviceConfig/{WorkstationID}` (file present, chart absent), and double-counts `Document_Note` PUT (the `POST` link in the chart points to `PUT_Document_Note.md` rather than `POST_Document_Note.md.md`). |
| SDD `ncr-counterpoint-retail-spine-integration.md` §2 + §10 | "99 individual endpoint docs" | Off by 2 vs. the actual file count of 97. Likely a count-from-memory error during SDD authoring. |
| OpenAPI spec produced here | 95 operations across 71 paths | 95 = 97 files − 2 stubs. Reconciles cleanly. |

**README chart vs. source-file discrepancies:**

1. README chart's `Document_Note` POST hyperlink points to
   `PUT_Document_Note.md` instead of `POST_Document_Note.md.md` —
   broken link.
2. README chart row for `/Document/{DocId}/Contact` PATCH actually links
   to a file named `PUT_Document_Contact.md` and the file's header reads
   `PUT /Document/{DocId}/Contact`. Method label inconsistency (chart
   says PATCH, file says PUT).
3. README chart row for `/PayCode/{Paycode}` PATCH links to
   `PUT_PayCode.md` whose header reads `PUT /PayCode/{Paycode}`. Same
   pattern as #2.
4. README chart references `GET_Paycode.md` and `GET_Paycodes.md`
   (lowercase variants); actual files are `GET_PayCode.md` and
   `GET_PayCodes.md` (mixed case). Filename casing inconsistent with
   chart.
5. README chart row for `/Customer/{CustNo}/Card` POST has source file
   header `POST /customer/{custNo}/CARD` (all-different casing).
   Counterpoint REST routing is presumably case-insensitive but this is
   editorial drift in the docs.
6. `GET /DeviceConfig/{WorkstationID}` exists as a file but is missing
   from the README chart.
7. README chart shows `CompanyAdmins/{CompanyName}` (no leading slash)
   for some rows; OpenAPI normalizes to `/CompanyAdmins/{CompanyName}`.

**SDD vs. per-endpoint detail divergences:**

1. SDD §4 puts `InventoryLocations` under **Places (N)**. Per-endpoint
   reading argues **D (Distribution)** is the operative module — the
   endpoint feeds inventory-by-location semantics, not site/device
   inventory. Both are defensible; we map to D in this article and
   flag.
2. SDD §4 People row includes "AdminUser*, Roles" under module **R
   (Customer)** with module **L** as cross-reference. Per-endpoint
   reading: Admin/Roles/Users are API-server platform concerns, NOT
   customer or labor entities — they should be `platform` not R or L.
   This article maps them to `platform` and flags.
3. SDD §4 Things row puts `GiftCard*` under **S, A, P**. Per-endpoint
   reading argues **F primary** (gift card = tender) with S secondary
   for the code template only. This article maps F+S and flags. The
   SDD's "P" attribution for gift cards is hard to justify from the
   endpoint surface and is likely a remnant of an earlier draft.
4. SDD §6.12 Module L cites `Roles, RoleUsers, RolesUsers, RoleEndpoints`
   as candidate endpoints — but the SDD itself flags these as
   "API-level roles, not labor-level". This article confirms: there is
   no labor surface in this API. L coverage = 0.
5. SDD letter scheme overlaps with but does not match the canonical spine
   wiki. The canonical wiki has C / D / F / J / S active; the SDD
   additionally uses T (Transactions), R (Customer), N (Device), Q
   (Loss Prevention), A (Asset), P (Pricing), L (Labor), W (Work
   Execution). For this engagement the SDD's expanded scheme is
   operative, but a future reconciliation pass should either fold the
   SDD letters into the canonical wiki or document why Canary's
   internal module decomposition diverges from the canonical spine
   catalog.

## Related

- `docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md` — the
  SDD whose §4–§6 this article checks endpoint-by-endpoint.
- `docs/sdds/canary/ncr-counterpoint-openapi.yaml` — the OpenAPI 3.0
  rendering of the same surface.
- `Brain/wiki/retail-integration-spine.md` — canonical spine letter
  scheme (C / D / F / J / S active; P / R placeholder).
- `Brain/wiki/ncr-counterpoint-connection-runbook.md` — bring-up runbook
  companion.
- `Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/` — source corpus.
