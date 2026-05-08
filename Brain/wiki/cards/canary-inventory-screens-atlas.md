---
type: reference
status: active
card-type: domain-atlas
card-id: canary-inventory-screens-atlas
card-version: 1
domain: merchandising
layer: application
tags: [canary, inventory, screens, atlas, crud, data-flows, ledger, application-design, functional-requirements]
created: 2026-05-07
last-compiled: 2026-05-07
needs-review: false
---

# Canary Go — Inventory Screens & Data Flows Atlas

The unified application-design reference for every screen, entity, CRUD operation, and data flow across the Canary Go inventory management surface. This card is the navigation layer over the existing module cards: it answers "what screens exist, who can do what on them, and how do changes propagate" in one place. Each module section links to the deeper card.

> **Governing thesis.** Every change to inventory state — sale, receipt, transfer, count, adjustment, return, damage write-off, automated detection — is an **immutable event in one append-only ledger**. Stock-on-hand is never directly mutated; it is a computed projection over the ledger. Every screen in this atlas is either a write to the ledger (with a typed event), a read over the projection, or CRUD over reference entities (items, suppliers, locations) that the ledger references. This single architectural commitment is what makes Canary auditable, time-travelable, hashable for the evidentiary rail, and compatible with the L402 satoshi cost model. **Build the ledger first; everything else is a screen over it.**

---

## Executive summary

Canary Go's inventory surface decomposes into **twelve modules**, organized by data direction relative to the inventory ledger. Reference modules (1–3) define the entities the ledger writes against. Write modules (4–10) are the typed event sources that mutate inventory state. Read modules (11–12) are projections over the ledger.

| # | Module | Direction | Role | Primary card |
|---|---|---|---|---|
| 1 | Catalog & Item Master | Reference | Item entity CRUD | [[canary-item-master-and-catalog]] |
| 2 | Suppliers & Vendors | Reference | Supplier entity CRUD | [[canary-supplier-profile-and-ordering]] |
| 3 | Locations & Zones | Reference | Location entity CRUD | [[store-ops-capability-model]] §1 |
| 4 | Manual Adjustments | Write | Reason-coded direct ledger writes | This card §6 (new) |
| 5 | Cycle Counts & Physical Inventory | Write | Reconciliation events from physical count | [[canary-mobile-task-ux-flows]] Task 3 |
| 6 | Purchase Orders | Write (indirect) | Order lifecycle that resolves to receipts | [[canary-purchase-order-lifecycle]] |
| 7 | Receiving | Write | PO-linked and DSD receipt events | [[canary-receiving]] · [[canary-mobile-task-ux-flows]] Task 1 |
| 8 | Transfers | Write | Paired source/destination ledger events | [[canary-transfer]] |
| 9 | Returns | Write | Restock + refund linkage events | [[canary-returns]] |
| 10 | Replenishment Tasks | Write (indirect) | System-generated picks that move stock between zones | [[canary-mobile-task-ux-flows]] Task 2 · [[retail-replenishment-model]] |
| 11 | Stock-on-Hand & Time Travel | Read | Projections, lookups, time-travel queries | [[canary-inventory]] |
| 12 | Reports & Exception Queue | Read | Dashboards, scorecards, KPIs, alerts | [[canary-ops-dashboard]] · [[canary-multi-store-intelligence]] |

This atlas catalogs **99 screens** across these twelve modules, mapped to **40+ entities**, **10 ledger event types**, and **5 user roles**.

---

## §1 — Architectural spine: the inventory ledger

The single architectural commitment that makes the rest of this atlas coherent. Read this section before any module section.

### The Movement entity

Every inventory state change writes one row to `app.inventory_movements`. The schema is the same regardless of source — manual adjustment, automated detection, sale, receipt, transfer, count, return. Discriminated by `event_type`.

```
app.inventory_movements
─────────────────────────────────────────────────────
movement_id           uuid           PK
tenant_id             uuid           merchant scope
location_id           uuid           which store/zone/bin
item_id               uuid           which SKU
event_type            enum           (see taxonomy below)
quantity_delta        decimal(14,4)  signed; + adds, − removes
unit_cost             decimal(12,4)  cost basis at event time (snapshot)
reason_code           varchar(32)    nullable; required for ADJUSTMENT events
source_ref_type       varchar(32)    PO, RECEIPT, TRANSFER, RETURN, COUNT, etc.
source_ref_id         uuid           foreign reference to source document
event_at              timestamptz    UTC; merchant-local rendered client-side
recorded_at           timestamptz    when row was written (may differ from event_at)
recorded_by_user_id   uuid           nullable for system events
recorded_by_agent     varchar(64)    nullable; system actor on automated events
chain_hash            bytea          hash of (prev_hash || canonical(this row))
prev_hash             bytea          previous chain_hash for this tenant+location
evidence_record_id    uuid           nullable; → canary-fox forensic linkage
device_id             uuid           nullable; capture device for evidentiary rail
notes                 text           operator-supplied context
```

**Append-only, never updated.** A correction is a new movement (`CORRECTION` event_type) that references the original. The original row is never mutated. This is the property the evidentiary rail depends on.

**Chain-hashed.** Every row's `chain_hash` is `sha256(prev_hash || canonical_serialize(row))`. Rolling per-(tenant, location) hash chain. Daily Merkle root anchored to L2 per [[infra-blockchain-evidence-anchor]] · [[canary-evidentiary-rail]].

**Immutable cost snapshot.** `unit_cost` at the time of the event is captured; later cost changes don't rewrite history. This is what makes the satoshi cost-rollup verifiable — every aggregated cost figure traces to event hashes ([[infra-satoshi-cost-rollup]]).

### Stock-on-hand is a projection

`app.inventory_positions` is a *materialized* view, not a source of truth. It's the running sum of `quantity_delta` per (tenant, location, item) up to a cutoff timestamp. The real-time engine ([[canary-inventory-as-a-service]]) keeps this fresh; the historical store ([[canary-inventory]]) computes time-travel positions on demand.

```
app.inventory_positions  (projection, regenerable)
─────────────────────────────────────────────────────
tenant_id, location_id, item_id   composite key
qty_on_hand                        decimal(14,4)
qty_reserved                       decimal(14,4)  (committed to open orders/transfers)
qty_available                      = qty_on_hand − qty_reserved (computed)
last_movement_at                   timestamptz
last_count_at                      timestamptz   (last reconciliation)
position_hash                      bytea         (hash of constituent movement_ids)
```

**Drop and rebuild.** If the projection corrupts, drop the table and recompute from the ledger. This is impossible in mutable-state inventory systems and is the single biggest reliability win of the event-sourced design.

### Event type taxonomy

Nine event types cover every inventory state change. Every screen in this atlas writes one of these (via a typed UI flow) or reads positions derived from them.

| Event type | Source | Sign | Reason required? | Triggered by |
|---|---|---|---|---|
| `RECEIPT` | Goods received against a PO | + | No | [[canary-receiving]] flow |
| `DSD_RECEIPT` | Direct-store-delivery without PO | + | No | Receiving with "Unplanned Delivery" |
| `SALE` | POS transaction | − | No | POS webhook from [[canary-tsp-pipeline]] |
| `RETURN` | Customer return restocked | + | No | [[canary-returns]] flow |
| `TRANSFER_OUT` | Outbound leg of inter-location transfer | − | No | [[canary-transfer]] flow |
| `TRANSFER_IN` | Inbound leg (paired with TRANSFER_OUT) | + | No | [[canary-transfer]] flow |
| `ADJUSTMENT` | Manual operator-driven change | ± | **Yes** | Manual adjustment screen (§6) |
| `COUNT_RECONCILE` | Cycle count discrepancy resolution | ± | Optional | Cycle count flow |
| `DETECTED_LOSS` | Automated detection (Hawk/Bull/Owl) | − | Yes (auto-tag) | Loss detection pipeline |
| `CORRECTION` | Reversal/correction of prior movement | ± | Yes | Admin override screen (§6) |

**Automated vs. manual:** `SALE`, `DETECTED_LOSS` are system-written. `RECEIPT`, `RETURN`, `TRANSFER_*`, `COUNT_RECONCILE` are user-initiated through guided UX. `ADJUSTMENT` and `CORRECTION` are direct manual writes — the highest-friction path, gated by reason code and role permission.

### What this means for every screen in this atlas

- A "create" action on any inventory screen ultimately writes one or more rows to `app.inventory_movements`.
- A "view stock" or "lookup" action reads from `app.inventory_positions` (current) or replays from movements (historical).
- A "fix this number" action is **never** a direct UPDATE on the position. It is always an `ADJUSTMENT` or `CORRECTION` movement with a reason code.
- The inventory ledger is the contract surface for downstream services — [[canary-fox-case-management]] reads it for forensics, canary-bull (forthcoming) reads it for loss intelligence, [[canary-commercial]] reads it for invoice reconciliation, [[canary-ildwac]] reads it for cost-model recompute.

---

## §2 — Module: Catalog & Item Master

**Reference module.** Owns the Item entity. Every ledger event references `item_id`; this module is where those rows are created and maintained. Deeper card: [[canary-item-master-and-catalog]].

### Entities owned

```
app.items                 (the SKU — Level 2 of the 3-level hierarchy)
app.item_styles           (Level 1 — the parent product)
app.item_barcodes         (Level 3 — physical UPCs/PLUs/EANs; many-per-SKU)
app.item_variants         (size × color × flavor matrix dimensions)
app.item_categories       (hierarchical category tree)
app.item_supplier_links   (primary + alternate supplier per item)
app.item_location_links   (display min/max per item per location)
app.item_status_history   (Draft → Active → Trial → Phase-Out → Inactive)
```

### Screen catalog

| # | Screen | Purpose | Primary entity | CRUD | Flowbite recipe |
|---|---|---|---|---|---|
| 2.1 | **Item list** | Browse, search, filter, bulk-action all items | `app.items` | R, bulk U/D | Table with sticky header + filter chips + saved-views + bulk-action toolbar |
| 2.2 | **Item detail (read)** | Full record for one item incl. variants, barcodes, suppliers, current SOH, history | `app.items` (joined) | R | Two-column layout: primary content / metadata sidebar |
| 2.3 | **Item create — scan-to-lookup** | Camera/Bluetooth-scan a barcode; auto-fill from Open Food Facts/UPC DB; confirm | `app.items` + `app.item_barcodes` | C | Multi-step wizard, scanner panel, confirmation card |
| 2.4 | **Item create — supplier CSV import** | Upload supplier catalog CSV; preview; resolve issues; bulk import | `app.items` (batch) | C (batch) | File drop + diff table + validation badges |
| 2.5 | **Item create — manual entry** | Form for items with no barcode and no supplier file (private label, local, bulk produce) | `app.items` | C | Single-page form, progressive disclosure for optional fields |
| 2.6 | **Item edit** | Modify any field on an existing item | `app.items` | U | Same layout as 2.2 with inline-editable fields |
| 2.7 | **Variant matrix editor** | Size × color (or other 2-axis) variant grid editor for apparel | `app.item_styles` + `app.items` | C, R, U | Editable grid; size-run template selector |
| 2.8 | **Bulk price change** | Select N items, apply price change (% or $ delta), preview impact, commit | `app.items` (batch) | U (batch) | Filter-and-select pattern; preview pane shows margin impact |
| 2.9 | **Bulk status change** | Move items between Draft/Active/Trial/Phase-Out/Inactive in batch | `app.item_status_history` | U (batch) | Multi-select + status dropdown + confirm modal |
| 2.10 | **Category tree manager** | Create/rename/reparent categories; drag-to-reorder; show item count per node | `app.item_categories` | C, R, U, D | Tree with drag-drop; right pane shows items in selected node |
| 2.11 | **Item history / audit trail** | Full event log for one item (every adjustment, sale, receipt, count touching this SKU) | `app.inventory_movements` filtered | R | Timeline with event-type filter chips |
| 2.12 | **Barcode manager** | View/add/remove barcodes for one SKU (handle multi-UPC, store-PLU, weight-barcode) | `app.item_barcodes` | C, R, U, D | Sub-table within item detail |

### CRUD ops by role

| Role | C | R | U | D |
|---|---|---|---|---|
| Owner | ✓ | ✓ | ✓ | ✓ (soft) |
| Manager | ✓ | ✓ | ✓ | ✗ |
| Associate | ✗ (except §2.3 scan-to-add) | ✓ | ✗ | ✗ |
| Supplier portal user | ✗ | own items | ✗ | ✗ |
| System (auto) | ✓ (Faire/NuOrder import, GS1 DataSync) | ✓ | ✓ (price feed, content network) | ✗ |

**Delete is soft.** An item never disappears from history; setting status to `Inactive` is the operational equivalent of delete. Only an Owner with explicit confirm can hard-delete a Draft item that has zero ledger movements.

### Data flow into/out of the ledger

| From this module → ledger | When |
|---|---|
| Status flip Draft → Active | First `RECEIPT` event for the item must land before this can complete; status change is recorded in `app.item_status_history`, not the inventory ledger |
| Item delete (hard) | Refused if any movement references the item; otherwise tombstones the item row, no ledger impact |

This module **defines** what items exist; it does not directly write inventory movements. Movements happen via §6–§10.

---

## §3 — Module: Suppliers & Vendors

**Reference module.** Owns the Supplier entity that POs and item-supplier links reference. Deeper card: [[canary-supplier-profile-and-ordering]] · [[canary-receiving]] §vendors · [[retail-vendor-lifecycle]].

### Entities owned

```
app.vendors                       (the supplier record)
app.vendor_contacts               (sales rep, AP contact, dispatcher)
app.vendor_delivery_schedules     (which days, which dock, which window)
app.vendor_lead_times             (COLT + NOLT; auto-calibrated from receipt history)
app.vendor_minimums               (dollar/case minimums + below-minimum action)
app.vendor_terms                  (payment terms, chargeback matrix, return policy)
app.vendor_scorecards             (computed; on-time %, fill rate, short-ship freq)
```

### Screen catalog

| # | Screen | Purpose | Primary entity | CRUD | Flowbite recipe |
|---|---|---|---|---|---|
| 3.1 | **Supplier list** | All vendors, filter by category/status, scorecard glance | `app.vendors` | R | Card grid OR table with scorecard sparkline column |
| 3.2 | **Supplier detail** | Full profile + scorecard + recent POs + linked items | `app.vendors` (joined) | R | Two-column: profile / activity feed |
| 3.3 | **Supplier wizard (5-step)** | 4-minute mobile-first onboarding: identity → schedule → delivery → minimums → control mode | `app.vendors` (and children) | C | Linear stepper, save-and-resume |
| 3.4 | **Supplier edit** | Modify any profile field; history tracked | `app.vendors` | U | Inline-editable detail view |
| 3.5 | **Vendor scorecard** | 90-day rolling: on-time, fill rate, short-ship, lead-time variance | `app.vendor_scorecards` | R | KPI cards + trendline + delivery log table |
| 3.6 | **Item-supplier bulk linker** | Multi-select items, assign to a supplier, set primary or alternate | `app.item_supplier_links` | C, U | Two-pane: items left / supplier picker right |
| 3.7 | **Lead-time calibration prompt** | When auto-calibration suggests a change ("actual avg = 1.8 days, configured = 3"), accept/reject | `app.vendor_lead_times` | U | Banner notification + accept/dismiss |
| 3.8 | **Vendor terms & chargeback matrix** | Define penalty schedules for short-ship, late, damaged ([[retail-chargeback-matrix]]) | `app.vendor_terms` | C, R, U | Matrix editor |

### CRUD ops by role

| Role | C | R | U | D |
|---|---|---|---|---|
| Owner | ✓ | ✓ | ✓ | ✓ (soft) |
| Manager | ✓ | ✓ | ✓ | ✗ |
| Associate | ✗ | name + delivery only | ✗ | ✗ |
| Supplier portal user | ✗ | own profile | own contact info | ✗ |
| System (auto) | ✗ | ✓ | scorecard fields, lead-time calibration | ✗ |

### Data flow into/out of the ledger

| Direction | When |
|---|---|
| Vendor → ledger | Every `RECEIPT` movement carries `source_ref_type='RECEIPT'` whose underlying receipt links to a vendor |
| Ledger → vendor scorecard | Daily batch reads `RECEIPT` events vs. PO expected qty/date to compute fill rate, on-time %, short-ship frequency |

---

## §4 — Module: Locations & Zones

**Reference module.** Defines the physical surface that inventory occupies. Every movement carries a `location_id`. Deeper context: [[store-ops-capability-model]] §1 (Inventory & Location Model) · [[canary-space-range-display-on-floor]].

### Entities owned

```
app.locations             (store / warehouse / DC / online channel)
app.zones                 (within-store: sales floor, back-stock, receiving, hold, damage)
app.bins                  (within-zone: aisle/shelf/position addressing)
app.location_classes      (typed by temperature, security, handling)
app.location_capacity     (display min/max per item per bin)
app.location_label_print  (QR/barcode label generation queue)
```

### Screen catalog

| # | Screen | Purpose | Primary entity | CRUD | Flowbite recipe |
|---|---|---|---|---|---|
| 4.1 | **Location list** | Tree view: company → stores → zones → bins | `app.locations` (recursive) | R | Tree nav with live SOH count beside each node |
| 4.2 | **Location detail** | Capacity, classes, current items in this location | `app.locations` (joined) | R | Detail card + item grid |
| 4.3 | **Location create** | New store, zone, or bin with parent picker | `app.locations` | C | Modal form |
| 4.4 | **Zone capacity editor** | Set display min/max per item per zone (drives replenishment) | `app.location_capacity` | C, R, U | Editable grid: items × zones |
| 4.5 | **Bin label printing** | Generate QR/barcode labels for shelf-edge scan confirmation | `app.location_label_print` | C | Print queue + preview |
| 4.6 | **Location transfer history** | All movements that touched this location, filterable | `app.inventory_movements` filtered | R | Timeline + event filters |

### CRUD ops by role

| Role | C | R | U | D |
|---|---|---|---|---|
| Owner | ✓ | ✓ | ✓ | ✓ (refused if non-zero SOH) |
| Manager | ✓ (zones, bins) | ✓ | ✓ | ✗ |
| Associate | ✗ | ✓ | ✗ | ✗ |

---

## §5 — Module: Manual Adjustments & Reason Codes

**Write module.** The highest-friction, most-controlled write path into the ledger. This is how operators correct on-hand without a triggering event (no receipt, no transfer, no count). Examples: spoilage write-off, found stock, cosmetic damage, supplier credit applied. Every entry produces an `ADJUSTMENT` movement with a **mandatory reason code**.

This module is the most-policed surface in the inventory atlas because it is the manual override path. It is also the one with **no existing dedicated card** — this section is the canonical reference until one is split out.

### Entities owned

```
app.inventory_adjustments       (header record per adjustment session)
app.inventory_adjustment_lines  (one per item touched; each generates a movement)
app.adjustment_reason_codes     (configurable; tenant-specific + system-default set)
app.adjustment_approvals        (for adjustments above threshold; manager sign-off)
app.adjustment_attachments      (photos of damaged stock for evidence)
```

### Default reason code set (configurable per tenant)

| Code | Direction | Description | Approval threshold |
|---|---|---|---|
| `SPOILAGE` | − | Perishable past-date or visibly bad | Auto if ≤ $50 |
| `DAMAGE_IN_HOUSE` | − | Cosmetic damage; not sellable | Auto if ≤ $50 |
| `DAMAGE_VENDOR_CREDIT` | − | Vendor will credit; tracked separately | Manager |
| `THEFT_KNOWN` | − | Confirmed shrink (caught on camera, etc.) | Manager + Fox case |
| `THEFT_SUSPECTED` | − | Inferred shrink — distinct from cycle-count discrepancy | Manager + Fox case |
| `FOUND_STOCK` | + | Discovered in back-stock not in system | Manager |
| `RECEIVING_ERROR_FIX` | ± | Late-discovered receipt mistake | Manager + link to receipt |
| `INTERNAL_USE` | − | Sample, store consumption, manager comp | Owner |
| `PRICE_TEST` | − | Pulled for promotional repricing | Auto |
| `PHYSICAL_RECOUNT` | ± | Manual recount outside cycle-count flow | Auto |

Reason codes are extensible per merchant. Codes flow to canary-bull (forthcoming) for shrink pattern analysis and to [[retail-inventory-audit]] for quarterly audit prep.

### Screen catalog

| # | Screen | Purpose | Primary entity | CRUD | Flowbite recipe |
|---|---|---|---|---|---|
| 5.1 | **Adjustment list** | All adjustments, filter by reason, date, item, location, who | `app.inventory_adjustments` | R | Table + filter sidebar + export |
| 5.2 | **New adjustment — single item** | Pick item → enter quantity delta → choose reason → optional photo + note → submit | adjustment + line | C | Single-page form, scanner triggers item lookup |
| 5.3 | **New adjustment — bulk** | Multi-item adjustment session (e.g., end-of-day spoilage sweep through produce) | adjustment + many lines | C | Scan-add list with running cost total |
| 5.4 | **Adjustment detail** | View one adjustment, all lines, attachments, approvals, generated movements | adjustment (joined) | R | Detail with tabs: Lines / Attachments / Approvals / Movements |
| 5.5 | **Adjustment approval queue** | Pending adjustments above threshold; manager review/approve/reject | `app.adjustment_approvals` | R, U | Card list with approve/reject buttons |
| 5.6 | **Reason code admin** | View, add, modify, deactivate reason codes; set thresholds | `app.adjustment_reason_codes` | C, R, U, D (soft) | Table editor |
| 5.7 | **Correction (admin override)** | Reverse a prior movement; produces `CORRECTION` event referencing original | `app.inventory_movements` (new row) | C | Search-and-pick original movement → enter delta to reverse → reason |
| 5.8 | **Adjustment dashboard** | Heatmap by reason × location × week; flags abnormal patterns | computed from movements | R | Heatmap + sparklines |

### CRUD ops by role

| Role | C (single) | C (bulk) | C (correction) | Approve | R own | R all |
|---|---|---|---|---|---|---|
| Owner | ✓ any reason | ✓ | ✓ | ✓ | ✓ | ✓ |
| Manager | ✓ any reason | ✓ | ✓ (with audit) | ✓ (under owner threshold) | ✓ | ✓ |
| Associate | ✓ low-friction codes only (`SPOILAGE`, `DAMAGE_IN_HOUSE`, `PHYSICAL_RECOUNT`) — and only ≤ a per-tenant unit-cost cap | ✗ | ✗ | ✗ | ✓ | ✗ |
| System | `DETECTED_LOSS` only (separate event_type, distinct UI) | ✗ | ✗ | ✗ | ✗ | ✗ |

**Approval threshold logic.** Configured per tenant. Below threshold → auto-approved → movement written immediately. Above threshold → adjustment pends in approval queue; movement is **not** written until approved. On rejection, the adjustment is closed with `rejected` status and no ledger row is produced.

### Data flow into the ledger

```
Adjustment screen (5.2 / 5.3) 
    → app.inventory_adjustments header row
    → app.inventory_adjustment_lines (one per item)
    → IF auto-approve: app.inventory_movements (one ADJUSTMENT row per line)
    → IF pending: app.adjustment_approvals (queued)
       → on approve: write movements
       → on reject: mark adjustment rejected, no movement
```

Every `ADJUSTMENT` movement carries `source_ref_type='ADJUSTMENT'` and `source_ref_id` pointing to the adjustment line. Reason code stored on the movement directly so analytics doesn't have to join.

### Why this module matters disproportionately

The shrink loss the U.S. retail industry posts every year is mostly recorded through this surface — or worse, never recorded at all. A merchant who can't differentiate "sold but mis-rung" from "stolen" from "damaged but not written off" can't manage shrink, can't reconcile margin, can't pass audit ([[retail-inventory-audit]] · [[professor-adrian-beck-total-retail-loss]]). The reason-code taxonomy + approval gate + photo-evidence capture is what turns this from a hand-wavy "adjustment" into the auditable shrink record that backs Canary's L402 evidentiary rail.

---

## §6 — Module: Cycle Counts & Physical Inventory

**Write module.** Reconciliation events comparing physical count to ledger projection. Discrepancies write `COUNT_RECONCILE` movements. Mobile flow already documented in [[canary-mobile-task-ux-flows]] Task 3 — this section adds the admin-side and reporting screens.

### Entities owned

```
app.cycle_counts             (header per count session)
app.cycle_count_lines        (one per location-item counted)
app.cycle_count_schedules    (rotation: which zones get counted on what cadence)
app.physical_inventory_runs  (full-store wall-to-wall counts)
app.reconciliation_runs      (the reconciliation event spanning ledger + count)
```

### Screen catalog

| # | Screen | Purpose | Primary entity | CRUD | Flowbite recipe |
|---|---|---|---|---|---|
| 6.1 | **Count schedule calendar** | View upcoming + past counts; configure rotation rules per zone | `app.cycle_count_schedules` | C, R, U, D | Calendar view + config drawer |
| 6.2 | **New count session** | Assign zone, assign counter, set due date | `app.cycle_counts` | C | Form with zone tree picker |
| 6.3 | **Count list** | Open counts, my assigned counts, completed counts | `app.cycle_counts` | R | Tabbed list |
| 6.4 | **Mobile count flow** | Scan location → count items → confirm → discrepancy → reason → adjust (5 sub-screens) | count + lines + movements | C, R, U | See [[canary-mobile-task-ux-flows]] §Task 3 |
| 6.5 | **Count detail / review** | All lines, all discrepancies, supervisor sign-off | `app.cycle_counts` (joined) | R, U | Detail with discrepancy filter chips |
| 6.6 | **Discrepancy investigation** | One discrepancy: history of item, recent movements, video timeline if available | aggregated | R | Investigation panel — see [[canary-evidentiary-rail]] |
| 6.7 | **Physical inventory dashboard** | Full-store count progress; live reconciliation as zones complete | `app.physical_inventory_runs` | R, U | Progress bars per zone + running discrepancy total |
| 6.8 | **Count accuracy report** | Per-zone, per-counter accuracy over time | computed from movements | R | Trend chart + leaderboard |

### CRUD ops by role

| Role | C (count) | Execute count | Approve discrepancies | R own | R all |
|---|---|---|---|---|---|
| Owner | ✓ | ✓ | ✓ | ✓ | ✓ |
| Manager | ✓ | ✓ | ✓ | ✓ | ✓ |
| Associate | ✗ | ✓ assigned | ✗ | ✓ | ✗ |

### Data flow into the ledger

A discrepancy write produces a **single** `COUNT_RECONCILE` movement per item with `quantity_delta = counted_qty − projection_qty`. The movement carries the `cycle_count_line_id` as `source_ref_id`, optional reason code (e.g., `THEFT_SUSPECTED` if Bull's pattern engine flagged it), and the counter's user id.

**The cycle count is the sanity check on the ledger projection.** If reconciliations are large or frequent in a zone, the ledger is out of sync with reality — typically a receiving error, transfer never reconciled, or shrink. Bull subscribes to count-reconcile events for cross-store loss correlation ([[canary-multi-store-intelligence]]).

---

## §7 — Module: Purchase Orders

**Write module (indirect).** POs don't directly write to the inventory ledger — receipts do. But the PO is the contract that receipts are validated against, so it sits in the same logical pipeline. Deeper card: [[canary-purchase-order-lifecycle]].

### Entities owned

```
app.purchase_orders        (PO header)
app.po_lines               (one per item ordered)
app.po_status_history      (state machine transitions with timestamps)
app.po_transmissions       (EDI 850 / email / portal record per send)
app.po_receipts            (link to receipts; 1 PO can have many receipts on partial)
```

### Screen catalog

| # | Screen | Purpose | Primary entity | CRUD | Flowbite recipe |
|---|---|---|---|---|---|
| 7.1 | **PO dashboard / list** | All POs, filter by status, supplier, date | `app.purchase_orders` | R | Table + saved filters + status-color badges |
| 7.2 | **PO status board (kanban)** | Drag-or-watch: Draft → Submitted → Confirmed → In Transit → Received | `app.purchase_orders` | R, U (status-only) | Kanban (Flowbite kanban) with column-per-state |
| 7.3 | **PO detail** | Full record, line items, transmission history, linked receipts | `app.purchase_orders` (joined) | R, U (pre-submit) | Three-section: header / lines table / activity timeline |
| 7.4 | **PO create — system-proposed review** | Algorithm-proposed lines, edit qtys, drop lines, add lines, supplier-min check live | `app.purchase_orders` | C | Form with running-total panel + min-warning banner |
| 7.5 | **PO create — manual** | Empty PO, scan-add or search-add items, set delivery date | `app.purchase_orders` | C | Same shape as 7.4, no proposed lines |
| 7.6 | **PO line editor** | Inline qty/cost/delivery-date edit per line | `app.po_lines` | U | Inline-editable table row |
| 7.7 | **PO transmit** | Send via the supplier's chosen channel; capture transmission record | `app.po_transmissions` | C | Compose-style screen (subject/body for email, portal walkthrough, EDI confirm) |
| 7.8 | **PO cancel / amend** | Pre-receipt amendments and cancellations with notify-supplier flow | `app.purchase_orders` | U, D (logical) | Modal with reason + notify checkbox |
| 7.9 | **PO three-way match dashboard** | PO + receipt + invoice variance review ([[retail-three-way-match]]) | aggregated | R | Variance table with approve/exception actions |

### CRUD ops by role

| Role | C | R | U (pre-submit) | U (post-submit) | Cancel | Transmit |
|---|---|---|---|---|---|---|
| Owner | ✓ | ✓ | ✓ | qty-down only | ✓ | ✓ |
| Manager | ✓ | ✓ | ✓ | qty-down only | ✓ | ✓ |
| Associate | ✗ | own + assigned | ✗ | ✗ | ✗ | ✗ |
| System (Auto mode) | ✓ when supplier on Auto | ✓ | ✗ | ✗ | ✗ | ✓ |

### Data flow

```
PO (Submitted) → external supplier (EDI 850 / email / portal)
              → app.po_transmissions row
              → no inventory ledger movement yet

Supplier confirms → PO status → Confirmed (per-line back-order flags possible)

Goods arrive → §7 Receiving flow → RECEIPT movements written against ledger
            → app.po_receipts links the receipts back to PO lines
            → PO transitions to Received (partial) or Received (complete)

Invoice arrives → canary-commercial three-way match
               → on match: PO transitions to Reconciled → Closed
               → on variance: exception queue
```

POs are the most external-facing module — every PO crosses a trust boundary into the supplier's system. The transmission record is the contract evidence.

---

## §8 — Module: Receiving

**Write module — primary positive ledger source.** Where goods physically enter the store and the ledger records them. Two flow types: **PO-linked** (expected goods, validated against an open PO) and **DSD** (direct-store-delivery without prior PO; rep walks in with stock, common in beverage and produce). Service contract: [[canary-receiving]]. Mobile flow: [[canary-mobile-task-ux-flows]] Task 1.

### Entities owned

```
app.receipts             (header per delivery)
app.receipt_lines        (one per item received; each writes a RECEIPT movement)
app.receipt_variances    (short, over, damaged, wrong-item flags per line)
app.dsd_receipts         (subtype: vendor visit without prior PO)
app.supplier_credits     (queued when receipt has DAMAGED or REFUSED variance)
```

### Screen catalog

| # | Screen | Purpose | Primary entity | CRUD | Flowbite recipe |
|---|---|---|---|---|---|
| 8.1 | **Receiving dashboard** | Today's expected deliveries, in-progress sessions, recent completions | `app.receipts` | R | Card grid: by status |
| 8.2 | **PO receive flow** | Mobile: scan case → match line → confirm qty → exception → putaway direction → location scan → next | receipt + lines + movements | C | See [[canary-mobile-task-ux-flows]] §Task 1 |
| 8.3 | **DSD receive** | No-PO: pick supplier → scan items → enter qty + cost → submit | receipt + lines + movements | C | Scan-list view; cost field per line |
| 8.4 | **Receipt detail** | One receipt: lines, variances, attachments, generated movements, linked PO | `app.receipts` (joined) | R | Tabs: Lines / Variances / Movements / Documents |
| 8.5 | **Receiving exceptions queue** | All flagged variances pending manager action | `app.receipt_variances` | R, U | Filterable list with bulk-action toolbar |
| 8.6 | **Supplier credit queue** | Damage/refused-line claims pending supplier acknowledgment | `app.supplier_credits` | C, R, U | Pipeline: opened → submitted → credited → closed |
| 8.7 | **Resume receiving session** | Mid-flight receiving sessions paused (cellular dead-zone, end-of-shift) | `app.receipts` (state=in-progress) | R, U | List of resumable sessions per device |
| 8.8 | **Putaway override** | Manager view of recent putaway decisions; flag misplaced stock | aggregated | R, U | Recent-events feed |

### CRUD ops by role

| Role | Start session | Confirm line | Flag exception | Approve variance | Submit credit | R |
|---|---|---|---|---|---|---|
| Owner | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Manager | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Associate | ✓ assigned | ✓ | ✓ | ✗ | ✗ | own session |

### Data flow into the ledger

Each `Confirm line` action in the mobile flow writes **one** `RECEIPT` (or `DSD_RECEIPT`) movement: `quantity_delta = received_qty`, `unit_cost = po_line.cost` (or DSD-entered cost), `source_ref_type='RECEIPT'`, `source_ref_id=receipt_line.id`, `location_id=putaway_zone.id`. **SOH updates immediately** at scan-confirm — never at session close. This is the operating principle the analytics layer depends on (real-time velocity = real-time SOH).

---

## §9 — Module: Transfers

**Write module — paired ledger events.** Inter-location stock movement. Every transfer line writes **two** ledger movements: a `TRANSFER_OUT` at the source and a `TRANSFER_IN` at the destination. In-transit period is bracketed by the two events. Service contract: [[canary-transfer]].

### Entities owned

```
app.transfers           (header)
app.transfer_lines      (one per item; produces 2 movements per line)
app.transfer_events     (state machine transitions)
app.transfer_variances  (SHORT, OVER, DAMAGED, MISSING per line)
```

### State machine

`CREATED → IN_TRANSIT → RECEIVED → RECONCILED` with `CANCELED` and `DISPUTED → ESCALATED-TO-FOX` branches. Source: [[canary-transfer]].

### Screen catalog

| # | Screen | Purpose | Primary entity | CRUD | Flowbite recipe |
|---|---|---|---|---|---|
| 9.1 | **Transfer list** | All transfers, filter by source/dest/status | `app.transfers` | R | Table + status badges |
| 9.2 | **Transfer create** | Source location → destination location → add lines (scan or search) → submit | `app.transfers` + lines | C | Two-pane source/dest + scan-add list |
| 9.3 | **Transfer ship (source-side)** | Scan items being shipped; produces `TRANSFER_OUT` movements | `app.transfer_lines` | U → C movements | Scan-confirm flow per line |
| 9.4 | **Transfer in-transit dashboard** | All transfers currently in flight; expected arrivals | filtered list | R | Card grid by destination |
| 9.5 | **Transfer receive (destination-side)** | Scan arrivals; reconcile against shipped quantity; produce `TRANSFER_IN` movements | `app.transfer_lines` | U → C movements | Scan-confirm flow with shipped-qty reference |
| 9.6 | **Transfer variance review** | Discrepancies between shipped and received; route to dispute or accept | `app.transfer_variances` | C, R, U | Variance table |
| 9.7 | **Transfer dispute escalation** | Escalate variance to Fox case for forensic review | `app.transfer_events` | C → Fox case | Escalation form |
| 9.8 | **Multi-location PO fan-out** | After receiving a multi-location PO at central DC, one-click create transfers to each store | `app.transfers` (batch) | C (batch) | "Receive and distribute" button on PO receipt → confirm fan-out modal |

**Screen 9.8 is the killer pattern.** Lifted conceptually from Lightspeed Retail's "Receive and distribute delivery." For the small DC + 2-5 stores ICP, this collapses 3-7 separate screens into one click. Worth treating as a first-class capability and probably its own SDD.

### CRUD ops by role

| Role | C | Ship | Receive | Dispute | Approve dispute |
|---|---|---|---|---|---|
| Owner | ✓ | ✓ | ✓ | ✓ | ✓ |
| Manager | ✓ | ✓ | ✓ | ✓ | ✓ |
| Associate | ✗ | ✓ assigned | ✓ assigned | ✗ | ✗ |

### Data flow into the ledger

```
Ship action (Screen 9.3)
  → for each line: write TRANSFER_OUT movement at source location
  → quantity_delta = −shipped_qty
  → source_ref = transfer_line.id
  → transfer state → IN_TRANSIT

Receive action (Screen 9.5)
  → for each line: write TRANSFER_IN movement at destination location
  → quantity_delta = +received_qty
  → if received_qty != shipped_qty: produce transfer_variance
  → source_ref = transfer_line.id
  → transfer state → RECEIVED

Reconciliation
  → if no variance: state → RECONCILED
  → if variance: state → DISPUTED
  → if dispute material: state → ESCALATED-TO-FOX (Fox case opened, blocks RECONCILED)
```

The paired-movement design means **stock in transit is invisible to both source and destination on-hand** — exactly correct. It's not at the source (already shipped) and not at the destination (not yet received). A separate `qty_in_transit` projection sums un-paired `TRANSFER_OUT` events for visibility.

---

## §10 — Module: Returns

**Write module.** Customer return restocked into inventory. Refunds happen at the POS or payment processor — Canary owns the inventory restock and the disposition decision. Service contract: [[canary-returns]]. Loss-detection linkage: [[canary-fox-case-management]].

### Entities owned

```
app.returns          (header)
app.return_lines     (one per item)
app.return_events    (state machine transitions)
app.return_reasons   (catalog: defective / wrong size / changed mind / damaged in shipment / etc.)
```

### State machine

`REQUESTED → AUTHORIZED → RESTOCKED → REFUNDED → CLOSED` with `DECLINED` and `ESCALATED → Fox case` branches. Source: [[canary-returns]].

### Screen catalog

| # | Screen | Purpose | Primary entity | CRUD | Flowbite recipe |
|---|---|---|---|---|---|
| 10.1 | **Returns list** | All returns, filter by status, customer, item, reason | `app.returns` | R | Table + filter sidebar |
| 10.2 | **Return create** | Scan original receipt or look up customer → select items returned → reason code | `app.returns` | C | Receipt scanner → line-pick → reason selector |
| 10.3 | **Return restock decision** | For each line: sellable / damaged / defective; produces RETURN movement (sellable only) | `app.return_lines` | U → C movement | Per-line disposition picker |
| 10.4 | **Return detail** | Full record: lines, dispositions, generated movements, refund link | `app.returns` (joined) | R | Detail with timeline |
| 10.5 | **Return escalation review** | Returns flagged for fraud (no receipt, frequent customer, high-value, pattern match) | `app.return_events` | R, U | Investigation queue |
| 10.6 | **Return reasons admin** | Configure tenant-specific return reason codes and auto-authorization rules | `app.return_reasons` | C, R, U, D | Table editor |

### Disposition rule

`RETURN` movement is written **only** for lines marked sellable. Damaged/defective dispositions produce an `ADJUSTMENT` movement with reason `DAMAGE_VENDOR_CREDIT` or `DAMAGE_IN_HOUSE` and queue a supplier credit if the return reason was vendor-fault. This is what keeps the ledger clean: damaged stock never gets put back to floor, never appears in available-for-sale projection.

### CRUD ops by role

| Role | C | Authorize | Restock decision | Escalate | Auto-decline override |
|---|---|---|---|---|---|
| Owner | ✓ | ✓ | ✓ | ✓ | ✓ |
| Manager | ✓ | ✓ | ✓ | ✓ | ✓ |
| Associate | ✓ within auto-auth params | ✗ | ✓ | flag-only | ✗ |

### Data flow into the ledger

```
Authorize action
  → no ledger write yet; state → AUTHORIZED

Restock decision (per line)
  → if sellable: write RETURN movement; quantity_delta = +qty; location = chosen restock zone
  → if damaged/defective: write ADJUSTMENT movement; quantity_delta = 0 (item never re-entered ledger)
        but supplier_credit row queued if vendor-attributable
  → state → RESTOCKED

Refund (POS/processor side, not Canary)
  → Canary records refund event_at via webhook from canary-tsp
  → state → REFUNDED → CLOSED
```

---

## §11 — Module: Replenishment & Par Levels

**Write module (indirect — produces tasks, not movements directly).** The automation rail. Algorithms compute reorder quantities and fire either replenishment tasks (back-stock → floor pick) or proposed POs (back-to-supplier reorder). Movements happen when the tasks complete. Deeper coverage: [[retail-replenishment-model]] · [[canary-mobile-task-ux-flows]] §Task 2 · [[store-ops-capability-model]] §2.

### Entities owned

```
app.replenishment_methods      (Min/Max | Days-of-Supply | Dynamic per item-location)
app.replenishment_parameters   (min units, max units, days-window, service level, etc.)
app.replenishment_tasks        (system-generated work items)
app.replenishment_proposals    (system-proposed PO lines awaiting review)
app.shift_waves                (batched task plans per shift)
```

### Three escalating methods (progressive disclosure to operator)

| Level | Method | Inputs | When to use |
|---|---|---|---|
| 1 | **Min/Max** | min units, max units, increment | Default for low-velocity or new items |
| 2 | **Days-of-Supply** | days to hold, lead time | Mid-velocity items where velocity is steady |
| 3 | **Dynamic** | service level %, lead time, lost-sales factor | High-velocity items where stockouts are costly |

Velocity feed is the POS sale stream from [[canary-tsp-pipeline]]. Without sales velocity, only Level 1 is available.

### Screen catalog

| # | Screen | Purpose | Primary entity | CRUD | Flowbite recipe |
|---|---|---|---|---|---|
| 11.1 | **Replenishment task queue** | All open tasks, filter by zone/priority/age | `app.replenishment_tasks` | R, U (assign) | Kanban or priority-sorted list |
| 11.2 | **Mobile pick flow** | Assigned task → pick from back-stock → deliver to floor → confirm | task + 2 movements (TRANSFER pair within store) | C, U | See [[canary-mobile-task-ux-flows]] §Task 2 |
| 11.3 | **Replenishment parameter editor** | Per-item: choose method, set parameters, preview ROQ | `app.replenishment_parameters` | C, R, U | Method picker + parameter form + live ROQ preview |
| 11.4 | **Bulk parameter editor** | Apply method/params to many items at once (e.g., entire category on Min/Max with case-pack increment) | parameters (batch) | U (batch) | Filter-and-select + apply |
| 11.5 | **Shift wave plan** | Time-budgeted batch of tasks for a shift, ordered by zone proximity | `app.shift_waves` | C, R, U | Kanban with crew assignment |
| 11.6 | **Proposed PO review** | System-proposed PO lines (when an item should be reordered from supplier) | `app.replenishment_proposals` | R, U | Same shape as PO §7.4 — this *becomes* a PO when approved |
| 11.7 | **Replenishment exceptions** | Tasks the associate couldn't complete (location empty, item not found, blocked) | `app.replenishment_tasks` (state=exception) | R, U | Exception queue with reason filter |
| 11.8 | **Replenishment hit-rate report** | % of tasks completed before SOH hits zero, per zone, per shift | computed | R | Trend chart + zone heatmap |
| 11.9 | **Auto-replenishment opt-in prompt** | "You ordered [item] manually 3 times. Add to auto-replenishment?" | `app.replenishment_methods` | C | Banner + accept/dismiss |

### Floor↔back-stock movement

When an associate completes a replenishment task (mobile flow Task 2), Canary writes a **paired** movement: one `TRANSFER_OUT` from the back-stock bin and one `TRANSFER_IN` to the floor location, both with `source_ref_type='REPLENISHMENT_TASK'`. This is intra-store stock motion treated as a transfer — same architecture as inter-store, smaller scale.

### CRUD ops by role

| Role | Configure params | Pick task | Override priority | Approve proposed PO | View reports |
|---|---|---|---|---|---|
| Owner | ✓ | ✓ | ✓ | ✓ | ✓ |
| Manager | ✓ | ✓ | ✓ | ✓ | ✓ |
| Associate | ✗ | ✓ assigned | ✗ | ✗ | own |

---

## §12 — Module: Stock-on-Hand & Time Travel

**Read module.** Projections and queries over the ledger. The interface most users actually use day-to-day to answer "do I have this in stock?" and "what was on-hand at [time]?" Service contract: [[canary-inventory]] · [[canary-inventory-as-a-service]].

### Read surfaces

```
app.inventory_positions        (current snapshot, materialized)
app.inventory_positions_t      (time-travel: state at any historical timestamp)
app.inventory_in_transit       (TRANSFER_OUT events without paired TRANSFER_IN)
app.inventory_reserved         (committed-to-orders projection)
```

### Screen catalog

| # | Screen | Purpose | Primary entity | CRUD | Flowbite recipe |
|---|---|---|---|---|---|
| 12.1 | **Item SOH view** | One item: SOH per location, in-transit, reserved, available | positions joined | R | Location table with sparkline |
| 12.2 | **Location SOH view** | One location: all items present with current quantity | positions filtered | R | Searchable item table |
| 12.3 | **Time-travel query** | "What was SOH of item X at location Y on date Z" | replay or `_t` view | R | Date picker + result card |
| 12.4 | **Stock movement history** | Per item: every movement (sale, receipt, transfer, count, adjustment) chronological | `app.inventory_movements` filtered | R | Timeline with event-type chips |
| 12.5 | **Multi-location SOH compare** | One item across all locations side-by-side | positions pivoted | R | Comparison table |
| 12.6 | **Lookup widget** (POS-side) | Embedded SOH check from the POS terminal during a sale | positions | R | Compact widget — see [[canary-android-pos-integration]] |
| 12.7 | **Position snapshot export** | Bulk export of positions at as-of time | bulk window | R | Export form + delivery via [[tier-bulk-window]] |

### CRUD ops by role

| Role | R | Time-travel | Bulk export |
|---|---|---|---|
| Owner | ✓ | ✓ | ✓ |
| Manager | ✓ | ✓ | ✓ |
| Associate | ✓ | scoped to own location | ✗ |
| External (auditor, vendor) | scoped | as-of-only | with API key |

This module is **read-only.** Any "fix this number" instinct is wrong here — corrections go through §5 (Manual Adjustments). The architectural rule: positions are projections; the source of truth is the movement ledger.

---

## §13 — Module: Reports & Exception Queue

**Read module.** Aggregations, dashboards, KPIs, and the cross-cutting exception surface that flags things needing human attention. Many of these draw from multiple modules. Deeper coverage: [[canary-ops-dashboard]] · [[canary-multi-store-intelligence]] · [[retail-operations-kpis]].

### Screen catalog

| # | Screen | Purpose | Source | Flowbite recipe |
|---|---|---|---|---|
| 13.1 | **Inventory dashboard** | KPI tiles: SOH value, slow-movers, in-transit, low-stock count, recent adjustments, shrink % | aggregated | KPI cards + trend sparklines |
| 13.2 | **Shrinkage report** | Adjustments tagged shrink/theft/damage by zone × time × reason | filtered movements | Heatmap + drill-down |
| 13.3 | **Slow-mover / dead-stock report** | Items with low velocity vs. carrying cost; markdown candidates | computed (cost-to-serve) | Table sorted by cost-to-revenue ratio |
| 13.4 | **Receiving accuracy report** | Per-supplier short-ship %, fill rate, exception frequency | from receipts + variances | Supplier scorecard list |
| 13.5 | **Cycle count accuracy** | Per-zone, per-counter discrepancy frequency and magnitude | from count reconciles | Trend + leaderboard |
| 13.6 | **Replenishment hit-rate** | % tasks completed before stockout, per zone | from tasks + movements | Trend chart |
| 13.7 | **Margin waterfall (per SKU)** | Revenue − COGS − cost-to-serve = true margin; satoshi-traceable | aggregated; satoshi events | Waterfall chart with hash-trace drill |
| 13.8 | **Multi-store SOH comparison** | Same item across all stores; identifies imbalance and transfer opportunities | positions pivoted | Comparison table |
| 13.9 | **Exception queue (cross-module)** | All open exceptions: receiving variances, transfer disputes, count discrepancies, returns escalations, replenishment failures | unioned | Filterable feed grouped by source |
| 13.10 | **Audit trail explorer** | Investigator surface: every movement on an item, location, vendor, or user, with chain-hash verification | filtered movements + chain-hash check | Timeline + verification badge |

### Exception queue is the *single* manager workflow

Owner-operators don't sit at dashboards. They get pinged when something needs them. Screen 13.9 is the surface that consolidates every "needs human" signal across the inventory atlas into one queue. Every other read screen is for diagnosis after the fact. The exception queue is the operating workflow.

### CRUD ops by role

| Role | View dashboards | Export | Audit-trail drill |
|---|---|---|---|
| Owner | ✓ all | ✓ | ✓ |
| Manager | ✓ all | ✓ | ✓ |
| Associate | own location KPIs | ✗ | ✗ |
| External auditor | scoped | with API key | ✓ chain-verify |

---

## §14 — Master CRUD matrix (roles × ledger event types)

The single matrix that answers "who can write what kind of movement to the ledger." This is the authorization contract surface.

| Event type | Owner | Manager | Associate | System | External |
|---|---|---|---|---|---|
| `RECEIPT` | ✓ | ✓ | ✓ assigned | via EDI ASN auto-receive (opt-in) | ✗ |
| `DSD_RECEIPT` | ✓ | ✓ | ✓ | ✗ | ✗ |
| `SALE` | ✗ direct | ✗ direct | ✗ direct | ✓ POS webhook | ✗ |
| `RETURN` | ✓ | ✓ | ✓ within auto-auth | ✗ | ✗ |
| `TRANSFER_OUT` | ✓ | ✓ | ✓ assigned | replenishment task auto-pair | ✗ |
| `TRANSFER_IN` | ✓ | ✓ | ✓ assigned | replenishment task auto-pair | ✗ |
| `ADJUSTMENT` | ✓ any reason | ✓ any reason | ✓ low-friction codes only | ✗ | ✗ |
| `COUNT_RECONCILE` | ✓ | ✓ | ✓ assigned counter | ✗ | ✗ |
| `DETECTED_LOSS` | ✗ | ✗ | ✗ | ✓ Hawk/Bull/Owl | ✗ |
| `CORRECTION` | ✓ with audit | ✓ with audit | ✗ | ✗ | ✗ |

**Read access** to the ledger is broad (everyone reads positions for their scope) but **write access** is narrow and typed. Every write goes through a typed UI flow that produces a specific event type. There is no generic "edit on-hand" path. This is intentional and load-bearing.

---

## §15 — Data flow map: automated vs. manual triggers

What writes to the ledger, classified by origin.

### Automated writes

| Source | Event type | Trigger | Where the screen is |
|---|---|---|---|
| POS sale webhook ([[canary-tsp-pipeline]]) | `SALE` | Real-time on POS transaction | None (system) — visible on §12 history |
| POS void/return webhook | `RETURN` (sub-flow) | POS-initiated return at register | §10 detail view |
| EDI 856 ASN auto-receive | `RECEIPT` | Optional supplier integration | §8.4 receipt detail |
| Hawk loss detection ([[canary-fox-case-management]]) | `DETECTED_LOSS` | Pattern match on transaction stream | §13.9 exception queue |
| Bull cross-store correlation | `DETECTED_LOSS` | Cross-location pattern | §13.9 exception queue |
| Owl ambient surveillance | `DETECTED_LOSS` | Computer vision flag | §13.9 exception queue |
| Replenishment task auto-pair | `TRANSFER_OUT` + `TRANSFER_IN` | Associate completes a replenishment pick | §11.2 mobile pick flow |
| Faire / NuOrder order import | item creation (no movement) | External marketplace order received | §2.4 supplier CSV import |
| GS1 DataSync (Phase 3) | item update (no movement) | Supplier publishes catalog change | §2.6 item edit (auto-applied) |

### Manual writes (UI-driven)

| Source | Event type | Trigger | Screen |
|---|---|---|---|
| PO receive flow | `RECEIPT` | Operator scans goods at receiving dock | §8.2 PO receive flow |
| DSD receive flow | `DSD_RECEIPT` | Vendor walks in with stock; operator scans | §8.3 DSD receive |
| Transfer ship | `TRANSFER_OUT` | Source operator scans outbound | §9.3 transfer ship |
| Transfer receive | `TRANSFER_IN` | Destination operator scans inbound | §9.5 transfer receive |
| Cycle count discrepancy | `COUNT_RECONCILE` | Counter records actual vs. system | §6.4 mobile count |
| Return restock | `RETURN` | Sellable disposition on returned line | §10.3 restock decision |
| Manual adjustment (single) | `ADJUSTMENT` | Operator records spoilage/damage/found stock | §5.2 new adjustment |
| Manual adjustment (bulk) | `ADJUSTMENT` × N | End-of-day spoilage sweep, etc. | §5.3 bulk adjustment |
| Admin correction | `CORRECTION` | Reverse a prior movement after error discovery | §5.7 correction screen |

### The unifying picture

```
                     ┌─────────────────────────────────────┐
                     │   app.inventory_movements (ledger)  │
                     │   append-only · chain-hashed        │
                     │   nine event types                  │
                     └──────────────────┬──────────────────┘
                                        │
   ┌────────────────────────────────────┼────────────────────────────────────┐
   │                                    │                                    │
   ▼                                    ▼                                    ▼
┌────────────┐                    ┌────────────┐                    ┌────────────┐
│ AUTOMATED  │                    │  MANUAL    │                    │  PROJECTIONS│
│ WRITES     │                    │  WRITES    │                    │  (READS)    │
├────────────┤                    ├────────────┤                    ├────────────┤
│ POS sales  │                    │ Receiving  │                    │ Positions  │
│ POS returns│                    │ Adjustments│                    │ In-transit │
│ EDI ASN    │                    │ Counts     │                    │ Reserved   │
│ Hawk/Bull  │                    │ Transfers  │                    │ Time-trav  │
│ Replenish  │                    │ Returns    │                    │ History    │
│  task      │                    │ Corrections│                    │ Reports    │
│  pair      │                    │            │                    │ Exceptions │
└────────────┘                    └────────────┘                    └────────────┘
```

Every screen in this atlas falls into one of those three columns. Knowing which column a screen lives in tells you the validation surface, the role gate, and the audit posture.

---

## §16 — Build sequence (priority order for Canary Go)

The atlas is the destination; this is the path.

### Wave 1 — the ledger and its first three writes

1. **Movement ledger schema + projection** — `app.inventory_movements` table, `app.inventory_positions` projection, chain-hash machinery, time-travel query. Without this, nothing else writes.
2. **Item master CRUD (§2)** — item list, detail, scan-to-add, manual entry. Pre-populates the entity that movements reference.
3. **Manual adjustment screen (§5.2)** — the highest-policed write path; first proof that the ledger works end-to-end with reason codes, approval gating, and chain-hashing.
4. **Stock-on-hand view (§12.1, §12.2)** — read surface that proves positions are correct.

This is the minimum viable inventory system. A merchant can add items, manually adjust stock, and see current positions. Everything else is layered on this foundation.

### Wave 2 — the operational loop

5. **Supplier setup (§3)** — wizard + scorecard; prerequisite for PO flow.
6. **PO list + manual create (§7.1, §7.5)** — manual ordering before automated proposals.
7. **PO receive flow (§8.2)** — first automated `RECEIPT` movement source. Mobile-first.
8. **PO three-way match (§7.9)** — closes the loop with [[canary-commercial]].

After Wave 2, a merchant can run a complete operational loop: order → receive → adjust → know stock.

### Wave 3 — multi-location

9. **Locations & zones (§4)** — multi-bin within one store, then multi-store.
10. **Transfers (§9)** — paired-movement design.
11. **Multi-location PO fan-out (§9.8)** — the killer pattern.
12. **Multi-location SOH compare (§12.5)** — visibility across stores.

### Wave 4 — automation

13. **POS sale webhook (`SALE` event source)** — the velocity feed unlocks Level 2 and Level 3 replenishment.
14. **Replenishment task generation (§11.1, §11.2)** — Min/Max first, then Days-of-Supply.
15. **Cycle count flow (§6)** — once velocity is captured, count cadence makes sense.
16. **Returns flow (§10)** — once POS integration exists.

### Wave 5 — intelligence

17. **Detected-loss event source** — Hawk/Bull/Owl integration writes `DETECTED_LOSS` events.
18. **Exception queue (§13.9)** — the cross-module manager workflow.
19. **Reports & dashboards (§13.1–13.8)** — once data depth allows them to be informative.
20. **Cost-to-serve drill (§13.7)** — the satoshi rail closes the analytics loop.

### Wave 6 — partner ecosystem

21. **Supplier portal (read-scoped views into 3.2, 13.4)** — vendors see their own scorecard.
22. **EDI 850/856 transmission and auto-receive** — for suppliers who want it.
23. **GS1 DataSync subscription (Phase 3)** — automated item-master maintenance.
24. **Faire / NuOrder import (Phase 2)** — boutique/gift channel.

---

## §17 — Implementation layer notes

### Component framework

Per [[platform-stack-commitment]], Canary Go's web admin runs on **Tailwind 3.x + Alpine.js 3.x**. The component layer is **Flowbite** (MIT, Tailwind-native, Alpine-compatible) supplemented by **Headless UI** for accessibility-critical primitives. Every "Flowbite recipe" column in the screen tables above maps to a specific Flowbite component or pattern. None of this card's screens require React.

Mobile flows ([[canary-mobile-task-ux-flows]]) target Android — same Tailwind component classes, served from the same backend, rendered in a WebView shell or as a PWA. One UI codebase, two delivery targets.

### Why not Polaris or Big Design

Shopify Polaris is licensed under a custom Shopify-Source license that requires non-Shopify applications to be "visually distinct from Shopify products and services as determined by Shopify in its sole discretion" — non-starter for an external commercial product. BigCommerce Big Design's LICENSE file is missing on `main`; treat as unverified until that's resolved. Both are React-only regardless. Flowbite + Headless UI is the answer for our stack.

### NCR Counterpoint vocabulary anchor

For ICP retailers migrating from NCR Counterpoint ([[ncr-counterpoint-functional-decomposition]]), the screens above use NCR-aligned vocabulary wherever possible: "item maintenance" rather than "product editor"; "receivings" rather than "intake"; "inventory adjustment" rather than "stock correction"; "physical count" rather than "audit." This is operational-mental-model preservation, not pixel-imitation. The vocabulary mapping is itself worth a future card.

### Lightspeed pattern reference

The transfer fan-out pattern (§9.8) is conceptually borrowed from Lightspeed Retail X-Series's "Receive and distribute delivery." Their multi-location PO documentation is the best public reference for the workflow shape. We rebuild it ground-up — but the operational concept is the lift.

---

## §18 — What this card replaces and what it doesn't

**Replaces:** the lack of a single navigable index across the inventory module surface. Anyone joining the build can read this card and know every screen, every entity, every event type, every role permission in one place.

**Does not replace:** the deeper module cards. Each module section here points at the canonical card for that module — those remain authoritative for their depth. This card is the atlas; those are the cities.

**Open items this card surfaces (no existing card covers them yet):**

1. **Manual Adjustments (§5)** has no dedicated card today. This atlas is currently the only reference. Worth splitting into a `canary-adjustments` card when the build reaches that wave.
2. **Locations & Zones (§4)** is partially covered in [[store-ops-capability-model]] §1 but not as a dedicated entity card. Worth `canary-locations` when multi-store work begins.
3. **The Inventory Ledger schema (§1)** is referenced across many service cards but not consolidated. Worth a `canary-inventory-ledger` SDD-equivalent card.
4. **The Multi-Location PO Fan-Out (§9.8)** is the highest-value differentiating UX pattern in the atlas. Worth a dedicated SDD with state-machine, edge cases (partial receipt, damaged-on-receipt, vendor short-shipped, partial fan-out), and screens.
5. **The Exception Queue (§13.9)** — cross-module manager workflow — is referenced but not yet specified. Worth `canary-exception-queue`.

These five gaps are the next logical cards to spawn from this atlas.

---

## See also

**Service contracts (the entities this atlas references):**
- [[canary-inventory]] · [[canary-inventory-as-a-service]] · [[canary-receiving]] · [[canary-transfer]] · [[canary-returns]]
- [[canary-item]] · [[canary-tsp-pipeline]] · [[canary-commercial]] · [[canary-fox-case-management]] · canary-bull (forthcoming)

**Functional design cards (the depth behind module sections):**
- [[canary-item-master-and-catalog]] · [[canary-purchase-order-lifecycle]] · [[canary-supplier-profile-and-ordering]] · [[canary-mobile-task-ux-flows]]
- [[store-ops-capability-model]] · [[retail-replenishment-model]] · [[retail-three-way-match]] · [[retail-receiving-disposition]] · [[retail-purchase-order-model]]
- [[canary-evidentiary-rail]] · [[canary-multi-store-intelligence]] · [[canary-ops-dashboard]]

**Source pattern references:**
- [[ncr-counterpoint-functional-decomposition]] — vocabulary and mental-model anchor
- [[shopify-competitive-decomposition]] — what the SaaS-native admin reference looks like
- [[rdm-wms-core-concepts]] · [[rdm-inbound-and-receiving]] · [[rms-replenishment-screen-flows]] — enterprise WMS/RMS source patterns

**Architectural and accountability rails:**
- [[platform-stack-commitment]] · [[platform-thesis]] · [[infra-blockchain-evidence-anchor]] · [[infra-satoshi-cost-rollup]] · [[canary-l402-otb]]

**Project MOC:** [[Brain/projects/Canary]]



