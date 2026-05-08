---
last-compiled: 2026-05-08
needs-review: false
type: reference
status: active
tags: [canary, item-master, catalog, screen-flows, ux, item-setup, scan, supplier-csv, manual-entry, functional-requirements]
created: 2026-05-08
gro: GRO-877
---

# Canary — Item Setup Screen Decomposition

The screen-by-screen spec for item creation, decomposing the three flows already locked in [`canary-item-master-and-catalog.md`](canary-item-master-and-catalog.md). This card is the substrate the build dispatch reads to generate templates — it is intentionally schema-aligned (real table names, real enum values from `deploy/schema/02_catalog_items.sql`) so a build agent maps screens to store methods directly without re-deriving the data model.

What's already decided lives in the parent card. This card answers the next question: *what does the operator actually see, what fields, what validation, what writes where.*

---

## Design principles

Inherited from [`canary-mobile-task-ux-flows.md`](canary-mobile-task-ux-flows.md) and reaffirmed here:

1. **One screen, one question.** No 12-field forms. Multi-step wizards over single dense pages.
2. **Scan is the primary input.** Camera or Bluetooth ring scanner. Manual entry is a fallback path, not the default.
3. **Exception is not a dead end.** Barcode not found, supplier file malformed, duplicate detected — every error has a recovery path that keeps the operator moving forward.
4. **Progress is visible.** Step indicators on every multi-screen flow ("3 of 5") so the operator knows where they are.
5. **Tenant boundary is invisible to the operator.** The session cookie carries the tenant; no UI ever asks "which store?" Every write derives `tenant_id` from `tenant.FromContext(r.Context())` (T-B middleware, shipped 2026-05-07).

---

## Common patterns (used in all flows)

### Status badge

Items render a status pill anywhere they appear:

| Status (schema) | Pill | Color | Operator meaning |
|---|---|---|---|
| `active` | ACTIVE | health-green | On the shelf, sellable, replenished |
| `discontinued` | DISCONTINUED | text-muted | No longer carried; historical record |
| `seasonal` | SEASONAL | signal-yellow | In rotation periodically |
| `hidden` | HIDDEN | accent-blue | Set up but not yet exposed at POS |

> ⚠️ **Open question — status lifecycle mismatch.** The schema defines `active | discontinued | seasonal | hidden`. The parent card describes a richer lifecycle (`Draft → Active → On Trial → Phase-Out → Inactive`) with a Draft → Active transition triggered by first receiving confirmation. Either:
> - the schema needs to evolve to match the card (add Draft + On Trial + Phase-Out states), OR
> - the card is aspirational and the schema is authoritative.
>
> **Recommendation:** evolve the schema. The Draft → Active transition is operationally meaningful (prevents ghost items in SOH before the goods arrive). Filed as a follow-on; see "Open questions" at the bottom of this card.

### Error envelope

Every error response uses the canary envelope per `docs/conventions.md`:

```json
{ "code": "duplicate_barcode", "message": "barcode 0123456789012 is already in use by SKU FOO-001" }
```

Client renders the `message` inline; the `code` is the stable contract for client-side branching.

### Tenant scoping (load-bearing)

Every `INSERT` / `UPDATE` carries `tenant_id` derived from the resolved session. **No screen exposes tenant_id as a user-editable field.** A build-agent regression that omits the tenant clamp is the same bug class T-B closed in Sprint 2; the screens here MUST NOT reintroduce it.

### Audit hook (every write)

Every screen that produces a state change writes one row to `app.audit_log` via the existing `audit.NewPgxInserter` (see `internal/protocol/audit/audit.go`). Action codes used in this card:

| Code | Resource | When |
|---|---|---|
| `item.create.scan` | `catalog.items` | Flow A confirms |
| `item.create.import` | `catalog.items` | Flow B import-row commit (one row per imported item) |
| `item.create.manual` | `catalog.items` | Flow C save |
| `item.update` | `catalog.items` | Any subsequent edit from any flow |
| `barcode.add` | `catalog.item_barcodes` | New barcode added (PLU generation, additional UPC) |

The `payload_digest` is the SHA-256 of the canonical-JSON post-state; the receiving team's compliance posture wants every item lifecycle event hashable.

---

## Flow A — Scan-to-Lookup

**Primary flow for grocery, CPG, hardware, general merchandise** — the 70% of items that have a manufacturer barcode and exist in some product-content database. Mobile-first; hardware scanner OR phone camera.

**Entry point:** `/items/new/scan` from the items list, OR a "+ New Item" button on any items page that routes here when the device has a camera.

### A1 — Scan Entry

```
┌─────────────────────────────────────────────┐
│ ← Cancel                          1 of 4    │
│                                             │
│  Scan an item                               │
│  Point the camera at the barcode, or        │
│  enter it below.                            │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │                                     │    │
│  │       [ camera viewfinder ]         │    │
│  │           live overlay              │    │
│  │                                     │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  Or type:  [ ____________________ ]         │
│                                             │
│  [ Skip — enter manually ]                  │
└─────────────────────────────────────────────┘
```

| Field | Type | Required | Validation |
|---|---|---|---|
| `barcode` (camera or manual) | text | ✓ | Length 4-18; numeric or 4/5-digit PLU |

**Decision points:**
- Camera permission denied → show ring-scanner pairing helper + manual entry field (don't block).
- Barcode decoded but length invalid → inline error "barcode looks too short / too long"; stay on screen.
- "Skip — enter manually" → routes to Flow C with empty barcode field.

**No state writes.** Barcode held in client state until A2 completes.

### A2 — Review Auto-Filled Record

After A1, gateway calls a chain of product-content sources (Open Food Facts → UPC Item DB → GS1 → Canary network catalog). First hit returns the auto-filled record.

```
┌─────────────────────────────────────────────┐
│ ← Back                            2 of 4    │
│                                             │
│  Found this item.                           │
│  ┌─────────────────────────────────────┐    │
│  │ Source: Open Food Facts        ✓✓✓  │    │
│  │                                     │    │
│  │ Name:     Organic Whole Milk        │    │
│  │ Brand:    Horizon                   │    │
│  │ Category: Dairy > Milk              │    │
│  │ Pack:     Half Gallon (64 fl oz)    │    │
│  │ Weight:   2.07 lbs                  │    │
│  │ Image:    [thumbnail]               │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  [ Looks right — continue ]                 │
│  [ Edit before saving ]                     │
└─────────────────────────────────────────────┘
```

**Confidence indicator (the ✓✓✓):**

| Source | Confidence | Reason |
|---|---|---|
| Canary network | ✓✓✓✓ | Set up by another Canary merchant; operationally validated |
| GS1 US Registry | ✓✓✓ | Brand-managed; authoritative for major brands |
| Open Food Facts | ✓✓✓ | Community-maintained; depth varies by brand |
| UPC Item DB | ✓✓ | Coverage broad but data shallow |
| (no source) | — | Routes to A2-fallback below |

**Decision points:**
- "Looks right" → A3 (operational fields).
- "Edit before saving" → routes to Flow C with all fields pre-populated; user can change anything.
- Source returned partial data (e.g., name + brand but no category) → render with placeholder text "(needs review)" on missing fields; A3 will require them.

**A2-fallback — Barcode not found in any source:**

```
┌─────────────────────────────────────────────┐
│  Barcode not in any catalog yet.            │
│                                             │
│  No problem — let's set this up by hand.    │
│  We'll save the barcode for next time.      │
│                                             │
│  [ Continue manually ]                      │
└─────────────────────────────────────────────┘
```

→ routes to Flow C with the barcode field pre-filled. The first merchant to set this up populates the Canary network catalog (Phase 3 — opt-in); the next merchant to scan the same barcode gets the ✓✓✓✓ result.

**No state writes.** Auto-filled record held in client state.

### A3 — Operational Fields

The product identity is from A2; A3 collects what the merchant alone knows: where it lives, how it sells, who supplies it.

```
┌─────────────────────────────────────────────┐
│ ← Back                            3 of 4    │
│                                             │
│  Set up "Organic Whole Milk"                │
│                                             │
│  Supplier      [ Horizon Wholesale    ▼ ]   │
│  Category      [ Dairy > Milk         ▼ ]   │
│                                             │
│  Unit cost     [ $ 2.49      ]              │
│  Selling price [ $ 4.99      ]              │
│                  margin: 50.1%              │
│                                             │
│  Case pack     [   12   ] eaches            │
│  Min on hand   [    6   ]                   │
│  Max on hand   [   24   ]                   │
│                                             │
│  Status        ( ) Hidden — not yet at POS  │
│                (•) Active — start selling   │
│                                             │
│  [ Save and add another ] [ Save ]          │
└─────────────────────────────────────────────┘
```

| Field | Type | Required | Validation | Schema column |
|---|---|---|---|---|
| `supplier_id` | uuid | ✓ | exists in `catalog.vendors` for tenant | (link via `catalog.item_vendors`) |
| `category_id` | uuid | optional | exists in `catalog.product_categories` for tenant | `catalog.items.category_id` |
| `default_cost` | money | ✓ | > 0 | `catalog.items.default_cost` |
| `default_price` | money | ✓ | > 0; soft-warn if `default_price ≤ default_cost` | `catalog.items.default_price` |
| `case_pack` | int | ✓ | ≥ 1 | (creates a `pack` item in `catalog.item_packs` if > 1) |
| `min_on_hand` | int | ✓ | ≥ 0; ≤ max | (replenishment params — separate table, not in catalog schema yet — see open questions) |
| `max_on_hand` | int | ✓ | > min | (same) |
| `status` | enum | ✓ | one of `active`, `hidden` | `catalog.items.status` |

**Decision points:**
- `default_price ≤ default_cost` → soft warning "price doesn't cover cost — continue?" (block the save if margin is negative? recommend NO — local clearance items legitimately sell below cost).
- Margin calculator updates live below the price field as the operator types.
- "Save and add another" → on success, return to A1 with empty form (continuous-receiving pattern).
- "Save" → A4.

### A4 — Confirm + Save

Atomic write — all-or-nothing across `catalog.items`, `catalog.item_barcodes`, `catalog.item_vendors`, optional `catalog.item_packs`, and `app.audit_log`.

**Inside the transaction:**

1. `INSERT INTO catalog.items (...) VALUES (...) RETURNING id`
2. `INSERT INTO catalog.item_barcodes (item_id, barcode, barcode_type, is_primary) VALUES (...)` — barcode_type derived from string format (12 digits → `UPC_A`, 13 → `EAN_13`, 14 → `GTIN`/`ITF_14`, 4-5 PLU → `PLU`).
3. `INSERT INTO catalog.item_vendors (item_id, vendor_id, ...)` — link to supplier.
4. `INSERT INTO catalog.item_packs (...)` if case_pack > 1 (the item is its own component; pack item carries the case quantity).
5. `INSERT INTO app.audit_log (action='item.create.scan', resource='catalog.items', resource_id=item_id, payload_digest=...)`.

On commit:
- Operator lands on the new item's detail page with a success toast: "Created. Set up another?"
- Toast includes a "+ Add another" CTA that re-opens A1.

**Failure modes:**

| Failure | Surface | Recovery |
|---|---|---|
| Duplicate barcode in tenant | inline error on A3 with a link to the existing item | "Open existing item" or "Make this a variant" |
| Supplier not found | inline error on A3 supplier picker | "Add new supplier" inline mini-form |
| Margin negative + operator rejects warning | stay on A3 | n/a |
| Network failure mid-save | toast "Couldn't save — your data is intact, try again" | tx rollback; client state preserved; retry button |

---

## Flow B — Supplier CSV Import

**Primary flow for boutique, gift, hardware, apparel SMB** — the operator gets a price list / catalog from their supplier as a CSV (or Excel). Bulk-load 50-500 items in one operation.

**Entry point:** `/suppliers/{id}/import` from the supplier detail page (preferred — supplier context already known), OR `/items/new/import` from the items page (asks for supplier on screen B1).

**Lifecycle backed by `catalog.import_jobs` (NOT YET IN SCHEMA — open question; see bottom):**
`QUEUED → VALIDATING → READY → COMMITTING → FINALIZED` (matches `canary-item.md` bulk-window pattern).

### B1 — Supplier + Template

```
┌─────────────────────────────────────────────┐
│ ← Cancel                          1 of 5    │
│                                             │
│  Import items from a supplier file          │
│                                             │
│  Supplier      [ Horizon Wholesale    ▼ ]   │
│                                             │
│  Need a template?                           │
│  [ Download CSV template (Horizon)        ] │
│  [ Download generic CSV template          ] │
│                                             │
│  Or upload a file you already have:         │
│  [ Choose file...                         ] │
│                                             │
│  Tip: CSV, XLSX, and Numbers all work.      │
└─────────────────────────────────────────────┘
```

| Field | Type | Required | Validation |
|---|---|---|---|
| `supplier_id` | uuid | ✓ | exists in `catalog.vendors` for tenant |
| `file` | upload | ✓ on next step | size ≤ 10 MB; mime ∈ {csv, xlsx, numbers, xls} |

**Decision points:**
- Per-supplier templates exist (column order matched to that supplier's typical export) when the merchant has imported from that supplier before; otherwise the generic template.
- "Choose file" → uploads to a temp store (S3 / GCS / local volume — gated on `STORAGE_BACKEND` env), returns an `import_job_id`, advances to B2.

**State writes:**
- `INSERT INTO catalog.import_jobs (id, tenant_id, supplier_id, status='QUEUED', file_uri, ...)`.

### B2 — Upload + Parse

```
┌─────────────────────────────────────────────┐
│ ← Cancel                          2 of 5    │
│                                             │
│  Reading horizon-feb-2026.xlsx...           │
│                                             │
│  ████████████░░░░░░░░  64%                  │
│                                             │
│  Detected 47 rows, 12 columns               │
│  Best-match field mapping:                  │
│                                             │
│   File column          →  Canary field      │
│   ─────────────────────────────────────     │
│   "UPC"                →  barcode            ✓│
│   "Item"               →  description        ✓│
│   "Pack"               →  case_pack          ✓│
│   "Cost"               →  default_cost       ✓│
│   "MSRP"               →  default_price      ✓│
│   "Brand"              →  attributes.brand   ✓│
│   "Cat"                →  category           ⚠ partial │
│                                             │
│  [ Adjust mapping ]   [ Looks right — preview ] │
└─────────────────────────────────────────────┘
```

| Behavior | Detail |
|---|---|
| Field mapping | Auto-mapped from canary's known column-name aliases; operator can override per column |
| Encoding | Auto-detect UTF-8 / UTF-16 / Windows-1252; fail loudly if undetectable rather than silently mojibake |
| Parsing | Row-by-row; partial-success is the norm — report what parsed, what didn't |

**Decision points:**
- "Adjust mapping" → expanded UI showing all file columns with per-column dropdown of canary fields; useful when the supplier's spreadsheet has unusual column names.
- "Looks right — preview" → triggers validation pass; advances to B3.

**State writes:**
- `UPDATE catalog.import_jobs SET status='VALIDATING', column_mapping=...`.

### B3 — Preview with Row-Level Validation

```
┌─────────────────────────────────────────────┐
│ ← Back                            3 of 5    │
│                                             │
│  47 items found in horizon-feb-2026.xlsx    │
│                                             │
│  ✓ 44 items ready to import                 │
│  ⚠ 3 items need attention:                  │
│  ┌─────────────────────────────────────────┐│
│  │ Row  | Issue              | Action       ││
│  │  12  | missing barcode    | [ Fix inline ]││
│  │  31  | duplicate barcode  | [ Open existing ]││
│  │      | (already SKU MK-101)│                 ││
│  │  38  | case pack = 0      | [ Fix inline ]││
│  └─────────────────────────────────────────┘│
│                                             │
│  Set defaults for these 44 items:           │
│  Status      [ Hidden — set live later ▼ ]  │
│  Min on hand [ — leave blank ▼ ]            │
│  Max on hand [ — leave blank ▼ ]            │
│                                             │
│  [ Fix all 3 ]                              │
│  [ Import 44 and skip the 3 ]               │
│  [ Cancel import ]                          │
└─────────────────────────────────────────────┘
```

| Validation rule | Surface as |
|---|---|
| missing barcode | inline; required for the row to import |
| duplicate barcode in tenant (already exists) | "Open existing" link → opens the existing item in a new tab; option to mark this row as "update existing" rather than create |
| case_pack = 0 or negative | inline; default 1 when the operator clicks Fix |
| price < cost | soft-warn at row level; row imports unless operator unchecks |
| supplier mismatch (file references a vendor name that's not the selected supplier) | row-level warn; operator confirms intent |
| > 1000 rows | warn before commit; recommend splitting into batches |

**Decision points:**
- "Fix all 3" → expands an inline editor with all 3 problem rows; operator fixes; rerun validation.
- "Import 44 and skip the 3" → commits the 44, leaves the 3 in a saved-but-not-imported state on the import_jobs row (operator can return later).
- "Cancel import" → marks job FINALIZED with `status='cancelled'`; nothing writes to `catalog.items`.

**Transaction boundary:** **per-row, NOT atomic batch.** A failure on row 31 shouldn't cost rows 1-30. Each row is its own short tx (item insert + barcode insert + vendor link + audit row + import_jobs row update). The import_jobs row aggregates per-row outcomes for the result screen.

### B4 — Defaults Batch

This screen actually folds into B3 (the "Set defaults for these 44 items" block above). Kept as a separate logical step here because the build agent may want to render it as a distinct screen on mobile (B3 list, B4 defaults form, then commit).

| Field | Type | Required | Applied to |
|---|---|---|---|
| `status` | enum | ✓ | every imported row |
| `min_on_hand` | int | optional | every row; if blank, the build agent flags the item as "needs configuration" |
| `max_on_hand` | int | optional | same |
| `category_id` | uuid | optional | overrides whatever the file said |
| `tax_class` | text | optional | overrides whatever the file said |

### B5 — Result + Diff

```
┌─────────────────────────────────────────────┐
│ ← Done                            5 of 5    │
│                                             │
│  Imported 44 of 47 items                    │
│                                             │
│  ✓ 38 new items created                     │
│  ✓  6 existing items updated                │
│  ⚠  3 rows skipped (see below)              │
│                                             │
│  All 44 imported items have status=hidden   │
│  and "needs configuration" — set min/max    │
│  before they're sellable.                   │
│                                             │
│  [ View imported items ]                    │
│  [ Configure replenishment for all 44 ]     │
│  [ Download skipped-row report (CSV) ]      │
└─────────────────────────────────────────────┘
```

**State writes (final):**
- `UPDATE catalog.import_jobs SET status='FINALIZED', finalized_at=NOW(), summary=...`.
- One `app.audit_log` row per imported item (`action='item.create.import'`), one for the import job itself (`action='import_job.finalize'`).

**Failure modes:**

| Failure | Surface | Recovery |
|---|---|---|
| File malformed (binary garbage, encrypted XLSX) | B2 fails fast; "We couldn't read this file" + tip on common causes | Re-upload, contact support |
| All rows fail validation | B3 with empty "ready" list + full "needs attention" list | "Cancel import" or fix-all path |
| Mid-batch crash (gateway killed during commit) | Resume on next visit to `/suppliers/{id}/import` — the import_jobs row still in `COMMITTING` state has a "Resume" CTA | Per-row idempotency: each row's INSERT is gated on `(tenant_id, sku) NOT IN already-imported-this-job` |
| Operator closes browser mid-flow | Same — import_jobs row holds state for 7 days; abandoned jobs auto-cleanup |

---

## Flow C — Manual Entry

**Primary flow for local, artisan, private label, no-barcode produce** — items with no manufacturer barcode and no supplier file. Also the fallback target for Flow A's "barcode not found" path.

**Entry point:** `/items/new/manual` from the items list, OR routed-from from Flow A (with barcode pre-filled), OR routed-from from Flow A2 ("Edit before saving") with all fields pre-populated.

### C1 — New Item Form

```
┌─────────────────────────────────────────────┐
│ ← Cancel                          1 of N    │
│                                             │
│  New item                                   │
│                                             │
│  Required                                   │
│  ─────────────────────────────────────      │
│  Item name      [ ____________________ ]    │
│                                             │
│  Category       [ Select ▼ ]                │
│                                             │
│  Barcode        [ ____________ ]            │
│                  [ Scan ] [ Generate PLU ]  │
│                                             │
│  Supplier       [ Select ▼ ] [ + new ]      │
│                                             │
│  Unit cost      [ $ ____ ]                  │
│  Selling price  [ $ ____ ]                  │
│                                             │
│  Case pack      [ ____ ] eaches             │
│                                             │
│  [ Save & add details later ]               │
│  [ Save & enrich now → ]                    │
└─────────────────────────────────────────────┘
```

| Field | Type | Required | Validation | Schema |
|---|---|---|---|---|
| `description` (item name) | text | ✓ | 1-200 chars | `catalog.items.description` |
| `category_id` | uuid | ✓ | exists in tenant | `catalog.items.category_id` |
| `barcode` | text | ✓ | unique within tenant; OR clicking "Generate PLU" assigns a 5-digit internal code | `catalog.item_barcodes.barcode` |
| `supplier_id` | uuid | ✓ | exists in tenant | via `catalog.item_vendors` |
| `default_cost` | money | ✓ | > 0 | `catalog.items.default_cost` |
| `default_price` | money | ✓ | > 0 | `catalog.items.default_price` |
| `case_pack` | int | ✓ | ≥ 1 | `catalog.item_packs.quantity` if > 1 |

**Smart defaults:**
- Category pre-filled from the operator's recent items (modal appears: "Same category as last 3 items: Dairy?").
- Supplier pre-filled if the operator was on a supplier detail page when they hit "+ New Item".
- Currency from the tenant config (no per-item currency picker on this screen).

**Decision points:**
- "Generate PLU" → opens C3 (PLU generation flow).
- "+ new" supplier → opens an inline supplier mini-form (name, contact, payment terms — minimal); commits a `catalog.vendors` row, then returns to C1 with the new supplier selected.
- "Save & add details later" → commits with status=`hidden`, item flagged in the items list with a "needs enrichment" badge; lands on items list.
- "Save & enrich now" → commits with status=`hidden`, advances to C2.

**State writes (Save):** same atomic-tx pattern as Flow A4.

### C2 — Optional Enrichment

```
┌─────────────────────────────────────────────┐
│ ← Back                            2 of N    │
│                                             │
│  Add details for "Joe's Local Honey"        │
│                                             │
│  Brand          [ ____________ ]            │
│  Short desc.    [ ____________ ]            │
│                  (prints on receipts)       │
│  Image          [ Upload | URL | none  ]    │
│                                             │
│  Pack details                               │
│  Weight         [ ____ ] [ oz ▼ ]           │
│  Dimensions     [ L _ x W _ x H _ ] in      │
│                                             │
│  Compliance                                 │
│  Tax class      [ Default ▼ ]               │
│  Age restricted [ ] (alcohol/tobacco)       │
│  EBT eligible   [ ]                         │
│  Allergens      [ + ]                       │
│                                             │
│  Country of origin [ ____________ ]         │
│                                             │
│  [ Save details ]   [ Skip — set live ]     │
└─────────────────────────────────────────────┘
```

| Field | Type | Schema column |
|---|---|---|
| `attributes.brand` | text | `catalog.items.attributes` (JSONB) |
| `short_description` | text | `catalog.items.short_description` |
| `attributes.image_url` | text | `catalog.items.attributes` |
| `attributes.weight_oz` | decimal | `catalog.items.attributes` |
| `attributes.dimensions_in` | object | `catalog.items.attributes` |
| `tax_class` | text | `catalog.items.tax_class` |
| `age_restriction` | int | `catalog.items.age_restriction` |
| `food_stamp_eligible` | bool | `catalog.items.food_stamp_eligible` |
| `attributes.allergens` | array | `catalog.items.attributes` |
| `attributes.country_of_origin` | text | `catalog.items.attributes` |

All optional. Empty values stay out of the JSONB column.

**Decision points:**
- "Save details" → updates the item, stays in `hidden` status until either (a) operator explicitly changes status to `active` or (b) first receiving confirmation auto-promotes (per the parent card's lifecycle thinking — gated on the schema-evolution open question above).
- "Skip — set live" → updates status to `active` directly, lands on item detail.

### C3 — PLU Generation Flow

Triggered from C1's "Generate PLU" button. Used for items without barcodes — produce, deli, butcher, local items.

```
┌─────────────────────────────────────────────┐
│ ← Cancel                                    │
│                                             │
│  Generate a barcode label                   │
│                                             │
│  PLU range     ( ) 4-digit produce (4000-4999)│
│                (•) 5-digit private (90000-99999)│
│                ( ) Custom internal code     │
│                                             │
│  Suggested:    93847                        │
│                ✓ unused in your store       │
│                                             │
│  Print label   [ Print 1 ]                  │
│                                             │
│  Or apply later from item detail.           │
│                                             │
│  [ Use 93847 and continue ]                 │
└─────────────────────────────────────────────┘
```

| Range | Use case |
|---|---|
| 4000-4999 | Standard PLU range (industry-standard for produce — e.g., 4053 = "Lemon") |
| 90000-99999 | Private/store-assigned (5-digit, no industry collision) |
| Custom internal | Full free-form; warns if it collides with the merchant's own catalog |

**State writes (on "Use NNNNN and continue"):**
- `INSERT INTO catalog.item_barcodes (item_id, barcode='93847', barcode_type='PLU', is_primary=true)`.
- `app.audit_log` row `action='barcode.add'`.

**Decision points:**
- "Print 1" → renders a printable label (Avery 5160 / Dymo 30252 / receipt printer); the build dispatch picks the print stack.

### C4 — Variant Matrix Builder (apparel two-axis)

For dimension type 3 (size × color matrix). Triggered from C1's category picker when the category has the apparel-style flag set, OR from a "Make this a variant set" CTA on item detail.

```
┌─────────────────────────────────────────────┐
│ ← Back                                      │
│                                             │
│  Variant set: Men's Oxford Shirt            │
│                                             │
│  Colors                                     │
│  [ Blue ] [ White ] [ Navy ] [ + Add ]      │
│                                             │
│  Size run                                   │
│  [ Standard Men's XS-XL ▼ ]                 │
│  → XS, S, M, L, XL                          │
│                                             │
│  ⌐ Generated SKUs (12) ──────────────       │
│  │ Blue / XS    Blue / S    Blue / M  ...│ │
│  │ White / XS   White / S   White / M ...│ │
│  │ Navy / XS    Navy / S    Navy / M  ...│ │
│  └──────────────────────────────────────    │
│                                             │
│  Each SKU needs a barcode at receiving      │
│  (or assign one manually now).              │
│                                             │
│  [ Generate 12 SKUs in Draft ]              │
└─────────────────────────────────────────────┘
```

| Behavior | Detail |
|---|---|
| Colors | Free-form text list; each color becomes a variant axis |
| Size run | Picks from configured size templates (saved at the merchant level, e.g. "Standard Men's XS-XL", "Women's 0-14") |
| Cap | Soft warn at > 50 SKUs; hard block at > 200 (a 200-SKU variant set is almost certainly a misconfiguration) |
| Status of generated SKUs | `hidden` until the operator confirms barcode assignment per SKU OR receives them via Flow B/PO |

**State writes:**
- One parent item in `catalog.items` with `item_type='standard'` and `attributes.style_id` set (the "style" identity).
- N child items, each with their own `catalog.items` row, `item_type='standard'` (variants are still standard items in the schema), `attributes.parent_style_id` pointing at the parent, `attributes.color` and `attributes.size` set.
- No barcodes inserted yet — barcode assignment happens at receiving or via a follow-up screen.
- `app.audit_log` row per generated SKU.

> The schema has `item_type='standard'` as the default — there is no first-class `style` row. The relationship is encoded in `attributes.parent_style_id`. This works but is brittle; a follow-on dispatch should consider promoting style to a column or a separate table for query efficiency.

### C-failure modes

| Failure | Surface | Recovery |
|---|---|---|
| Duplicate `(supplier_id, supplier_sku)` | inline error on C1 | "Open existing" or "Use a different supplier SKU" |
| Duplicate `barcode` (when manually entered) | inline | "Open existing item" or "This is a different size of the same product → variant" path |
| PLU collision (rare; range exhausted in tenant) | inline | Suggest the next free PLU |
| Variant matrix > 200 SKUs | hard block | Recommend splitting into two style sets |

---

## Cross-cutting concerns

### Mobile vs desktop split

| Flow | Primary device | Why |
|---|---|---|
| A — Scan-to-Lookup | Mobile (phone or tablet) | Camera scan, on-floor / receiving-area use, one-handed operation |
| B — Supplier CSV Import | Desktop | File upload + multi-row preview need screen real-estate; rarely done on the floor |
| C — Manual Entry | Both | Owner setup at desktop is common; staff at the counter setting up a local item is mobile |

Field-priority on mobile: every "optional" field collapses behind a "More details ▼" toggle. C1's required-fields-only view IS the mobile default; the "Required + Optional" expansion is desktop-default-open.

### Permissions

Pulled from the JWT claims that T-3's `tokenverify` package validates. `claims.UserType` and `claims.Scopes` gate the surfaces:

| `user_type` | Scan (A) | CSV (B) | Manual (C) | Edit existing | Variant set (C4) |
|---|---|---|---|---|---|
| `read_only` | — | — | — | — | — |
| `regular` | ✓ | — | ✓ (status=hidden only) | — | — |
| `power` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `admin` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `system` | ✓ | ✓ | ✓ | ✓ | ✓ |

A `regular` user can set up an item but cannot promote it to `active` — that's the "owner approval" gate. Admin/power users can promote directly.

Scope-level fine-grain (`items:create`, `items:promote`, `imports:run`) supplements user_type for tenants that want non-default policy. Scopes are additive; user_type is the default.

Server-side gate lives in the chi middleware that wraps `r.Group(...)` for the item-creation routes — extends the existing `requireTenantMiddleware` from T-B with a `requireScope("items:create")` wrapper. Build dispatch creates that wrapper.

### Tenant isolation (load-bearing — DO NOT regress)

Every screen above writes via store methods that derive `tenant_id` from `tenant.FromContext(r.Context())` exclusively. **No screen, no form, no API endpoint exposes a tenant_id field that the client can supply.** The barcode-uniqueness check is `(tenant_id, barcode)` per the schema; the duplicate-barcode error in Flow A4 / C1 is per-tenant by construction.

Sprint 2's T-B middleware closed the cross-tenant exposure that existed when `tenantIDFromCtx` returned `uuid.Nil`. Item-creation screens MUST NOT reintroduce that bug class. The build dispatch should add a regression test that asserts `INSERT` calls fail (or scope to the wrong tenant) when the tenant context is empty.

### State writes per screen — quick reference

| Screen | Tables touched | Audit action |
|---|---|---|
| A1 | none (client state) | — |
| A2 | none (client state) | — |
| A3 | none (client state) | — |
| A4 | `catalog.items`, `catalog.item_barcodes`, `catalog.item_vendors`, `catalog.item_packs?`, `app.audit_log` | `item.create.scan` |
| B1 | `catalog.import_jobs` (insert QUEUED) | — |
| B2 | `catalog.import_jobs` (update VALIDATING + column_mapping) | — |
| B3 | `catalog.import_jobs` (update with row-level outcomes) | — |
| B5 | per row: `catalog.items`, `catalog.item_barcodes`, `catalog.item_vendors`, `catalog.item_packs?`, `app.audit_log`. Once: `catalog.import_jobs` (FINALIZED) | `item.create.import` × N + `import_job.finalize` × 1 |
| C1 (Save) | `catalog.items`, `catalog.item_barcodes`, `catalog.item_vendors`, `catalog.item_packs?`, `app.audit_log` | `item.create.manual` |
| C2 (Save) | `catalog.items` UPDATE, `app.audit_log` | `item.update` |
| C3 | `catalog.item_barcodes`, `app.audit_log` | `barcode.add` |
| C4 | `catalog.items` × N, `app.audit_log` × N | `item.create.manual` × N |

### Audit hooks

Every state-write screen above writes one `app.audit_log` row per state change. The `payload_digest` is `sha256(canonical_json(post_state))` — chained into the protocol-anchor evidence stream when the merchant has Phase 4 SaaS-tier compliance enabled (see `retail-item-authorization.md`). Item-setup events become part of the merchant's compliance evidence chain by default.

For the `item.create.import` action specifically, each row's `payload_digest` covers the new item's full state but the operator's review-and-confirm action on B3 ALSO produces a single `import_job.finalize` row whose digest covers the per-row decisions (which rows imported, which skipped, why) — auditable record of the bulk operation, not just the individual items.

---

## Open questions

These need a decision before the build dispatch picks up. Filed as comments on GRO-877 OR as separate sub-tickets.

> **Update 2026-05-08 (post-GRO-880):** The Counterpoint catalog data-model audit at [[counterpoint-catalog-data-model-audit]] revises several questions below. Most importantly: Counterpoint's REST surface is **narrower than its back-office UI** — Canary's schema is closer to REST altitude than initially feared. Question 4 (first-class style identity) is partially answered: Counterpoint represents grid items as flat sibling rows, not a hierarchical structure, so Canary's current sibling-rows-with-shared-attributes approach is correct. Other questions revised inline below.

1. **Status lifecycle alignment.** Schema has `active | discontinued | seasonal | hidden`; parent card describes `Draft → Active → On Trial → Phase-Out → Inactive`. Recommend evolving the schema to add `draft`, `on_trial`, `phase_out`, `inactive` (a migration). The Draft → Active transition on first receiving is operationally meaningful and worth the schema change. **Counterpoint REST `STAT` data point (per GRO-880 audit): only active/inactive in REST**; richer Canary lifecycle is additive — Counterpoint sync rounds Canary states to active/inactive at the boundary.

2. **`catalog.import_jobs` table.** Referenced extensively in Flow B and listed as an owned table in `canary-item.md`, but **not yet in the schema**. Migration needed before Flow B can ship: `(id, tenant_id, supplier_id, status, file_uri, column_mapping, summary, created_at, finalized_at, ...)` with the lifecycle states from the parent card.

3. **Replenishment params storage.** Flow A's `min_on_hand` / `max_on_hand` fields don't have a home in `catalog.items` — they belong to `replenishment.replenishment_params` or similar (per the parent card's M4 milestone framing). Whether the item-setup screens write directly to that table OR defer the replenishment config to a follow-up screen is a sequencing question. Recommend deferring — keep item-setup focused on identity + commerce attributes, with replenishment as its own dispatch.

4. **First-class style identity.** C4's variant-matrix flow encodes the parent style in `attributes.parent_style_id` (a JSONB field, not a column). For apparel-heavy merchants this becomes the primary item-list query path; JSONB index is fine but a column would be clearer. Recommend: when the apparel two-axis flow ships, add a `style_id` column to `catalog.items` with self-FK and a partial index.

5. **PLU label printing stack.** C3's "Print 1" CTA needs a print path. Avery 5160 + browser-print is the simplest day-one; receipt-printer integration via the POS adapter layer is later. Build dispatch picks one.

6. **Per-row vs atomic-batch transaction boundary on import.** Recommended per-row above (a row 31 failure shouldn't cost rows 1-30) — confirm before build.

7. **Canary network catalog opt-in.** When the first merchant scans a barcode, do they implicitly contribute to the network catalog (Phase 3 build-priority item) or is contribution opt-in? Default-opt-in feels right but has compliance implications (item attributes are operational data; some merchants may consider supplier names sensitive). Recommend explicit opt-in toggle per merchant in tenant config.

---

## Build priority (matches parent card's prioritization)

1. **Flow C — Manual Entry, no-variant only.** Smallest scope; gets a working "+ New Item" path live. Mobile + desktop. Day 1.
2. **Flow A — Scan-to-Lookup with manual fallback.** Adds camera + Open Food Facts + UPC Item DB lookup. Day 2-3.
3. **Flow B — Supplier CSV Import.** Adds the bulk path. Requires `catalog.import_jobs` migration first. Day 3-5.
4. **Flow C — Variant matrix builder (C4).** Apparel-specific; gated on whether Bart's stores include apparel.
5. **Flow C — PLU generation (C3).** Day 1 if produce / local items are common; later if not.
6. **Canary network catalog contribution.** Phase 3 — gated on merchant scale.

---

## See also

- [[canary-item-master-and-catalog]] — parent substrate; this card extends.
- [[counterpoint-catalog-data-model-audit]] — Counterpoint REST IM_ITEM / IM_INV / IM_CATEG / SN_SER / VendorItem field-level shapes; gap report + prioritized migration list.
- [[square-sample-code-mechanics-inventory]] — Square sample-code patterns to lift (catalog batch upsert, idempotency keys, error envelope, webhook URL-in-signature, CSV gotchas, OAuth revoke recovery) and anti-patterns to avoid.
- [[canary-item]] — service card (port, axis, owned tables, cadence-ladder placement).
- [[retail-item-authorization]] — what's NOT in scope (other 3 authorization dimensions).
- [[canary-mobile-task-ux-flows]] — mobile UX precedent + design principles.
- [[rms-replenishment-screen-flows]] — enterprise screen-decomp precedent (Oracle RMS).
- [[Brain/projects/Canary]] — project MOC.
- `CanaryGo/internal/item/item.go` — current Go data model.
- `CanaryGo/deploy/schema/02_catalog_items.sql` — authoritative schema.
- GRO-877 — this card's source dispatch.
