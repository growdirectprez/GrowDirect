# Chunk 5 — Inventory + Distribution Domain (Schema `i`)

**ARTS anchor**: ARTS IXRetail Inventory V1.0 (full local PDF) + InventoryV2.0.0.xsd + ARTS movement / adjustment / receipt / transfer entities.
**Modules**: D (Distribution), with cross-cuts to F (financial valuation in `ledger.stock_ledger_entries`).
**Entities**: 5 (inventory_positions · inventory_movements · inventory_documents · inventory_document_lines · inventory_lots).
**Folded from sources**: CRDM 5 inventory entities + GSLM Supply 19 entities + D-Prefix 18 interfaces → 5 SMB-2030 canonical.

## Domain narrative

ARTS Inventory V2 separates the **state** (current stock-on-hand) from the **events** (what changed it). SMB-2030 keeps that clean split — `inventory_positions` is the rolling balance you query at every POS scan; `inventory_movements` is the append-only event log of every SOH delta. Documents (`inventory_documents` + `_lines`) capture the business intent behind movements — a goods-received note, a stock-count, a transfer-out — with line-level detail. Most movements derive from a document; some are direct (manual adjustment, sale-derived auto-decrement).

The D-Prefix TOM interfaces gave us 18 distinct operational flows for a single retail estate — split because Tesco had 4 named target systems (RMS, ORMS, GFO, TIMS) and each operation needed a copy in each system. Canary Go MCP services consolidate: one canonical movement happens once, junctions fan-out the notification to consumers (forecast, financial, replenishment) instead of materializing the same event in 4 copies.

Inventory lots (lot/serial-tracked items with expiry) is a sub-domain — some merchants (food, Rx, electronics with serials) need it; most SMB don't. Include the table in canonical, but it's empty for merchants that don't lot-track. Cardinality-aware per §9.

---

## i.inventory_positions

**ARTS reference**: ARTS InventoryControlBook (current SOH per item per location).
**Module**: D.

### Schema

```sql
CREATE TABLE i.inventory_positions (
  id                      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id               uuid NOT NULL REFERENCES app.tenants(id),
  item_id                 uuid NOT NULL REFERENCES m.items(id) ON DELETE RESTRICT,
  location_id             uuid NOT NULL REFERENCES l.locations(id) ON DELETE RESTRICT,
  zone_id                 uuid REFERENCES l.location_zones(id),    -- bin-level if zone-tracked; NULL = location-aggregate
  on_hand_quantity        numeric(14,4) NOT NULL DEFAULT 0,
  reserved_quantity       numeric(14,4) NOT NULL DEFAULT 0,        -- allocated but not yet picked (orders awaiting fulfillment)
  on_order_quantity       numeric(14,4) NOT NULL DEFAULT 0,        -- POs placed, not yet received
  in_transit_quantity     numeric(14,4) NOT NULL DEFAULT 0,        -- transfers in-flight
  last_movement_at        timestamptz,
  last_count_at           timestamptz,                              -- last stock-count timestamp (for cycle-count cadence)
  cost_basis              numeric(14,4),                            -- weighted-average cost (financial; cross-references ledger.stock_ledger_entries)
  attributes              jsonb NOT NULL DEFAULT '{}',
  status                  text NOT NULL DEFAULT 'active',           -- active | discontinued | bin_relocated
  created_at              timestamptz NOT NULL DEFAULT now(),
  updated_at              timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, item_id, location_id, COALESCE(zone_id, '00000000-0000-0000-0000-000000000000'::uuid))
);

CREATE INDEX idx_positions_tenant ON i.inventory_positions(tenant_id);
CREATE INDEX idx_positions_item ON i.inventory_positions(item_id);
CREATE INDEX idx_positions_location ON i.inventory_positions(location_id);
CREATE INDEX idx_positions_low_stock ON i.inventory_positions(tenant_id, location_id, item_id) WHERE on_hand_quantity <= 0;
CREATE INDEX idx_positions_unsynced ON i.inventory_positions(last_movement_at) WHERE last_count_at IS NULL OR last_count_at < last_movement_at - interval '30 days';
```

### Operational lifecycle (TOM operational clock)

**Producers** (write to inventory_positions):
- `mcp.inventory.position.materialize` — recomputes from `inventory_movements` deltas (atomic on each movement)
- `mcp.inventory.position.from-stock-count` — direct overwrite from physical count (sets `last_count_at = now()`)

**Consumers**:
- `mcp.transaction.scan.check-availability` — real-time at POS (do we have it?)
- `mcp.orders.fulfillment.allocate` — reserve quantity for an order
- `mcp.replenishment.demand.compute` — replenishment trigger (TOM J010 Current SOH GFO→UDD)
- `mcp.forecast.position.snapshot` — daily snapshot (TOM J010 nightly)
- `mcp.inventory.report.daily` — daily reporting (TOM D029 Inventory Report RMS→TIMS, D033 Storeline→GFO)
- `mcp.audit.shrink.compare-to-count` — Q-module shrink detection

**SLA at producer**: real-time on each movement, atomic with movement insert (transactional), p95 < 100ms.
**SLA at consumers**: lookup p99 < 30ms; freshness < 2s for transaction-scan.

### Provenance

- **ARTS reference**: InventoryControlBook (current state per item × location)
- **GSLM**: not richly modeled in S0 SQL implementation; the MDM site Supply domain has 19 entities including stock position
- **CRDM operational**: implicit (CRDM_Item operational reduces inventory; CRDM_GoodsReceived increases)
- **TOM junctions**: J010 (Current SOH GFO→UDD), D029 (RMS→TIMS report), D033 (Storeline→GFO report)
- **Canary current**: `ledger.stock_ledger_entries` is the financial-valuation counterpart — physical SOH is here, financial valuation there
- **Justification**: Reserved + on-order + in-transit columns are essential for "available-to-promise" calculations (orders fulfillment) — not separate tables because they're always queried together with on-hand. Cost basis denormalized for read speed; source-of-truth for cost is `ledger.stock_ledger_entries`. COALESCE-PK pattern allows location-aggregate (zone_id NULL) and bin-level positions to coexist.

---

## i.inventory_movements

**ARTS reference**: ARTS InventoryMovement (event log).
**Module**: D.

### Schema

```sql
CREATE TABLE i.inventory_movements (
  id                      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id               uuid NOT NULL REFERENCES app.tenants(id),
  item_id                 uuid NOT NULL REFERENCES m.items(id) ON DELETE RESTRICT,
  location_id             uuid NOT NULL REFERENCES l.locations(id) ON DELETE RESTRICT,
  zone_id                 uuid REFERENCES l.location_zones(id),
  lot_id                  uuid REFERENCES i.inventory_lots(id),
  movement_type           text NOT NULL,                            -- goods_receipt | adjustment | transfer_in | transfer_out | rtv | sale | return | write_off | cycle_count_correction | reservation | release_reservation
  quantity_delta          numeric(14,4) NOT NULL,                   -- signed; positive = increase, negative = decrease
  movement_at             timestamptz NOT NULL DEFAULT now(),
  source_document_id      uuid REFERENCES i.inventory_documents(id),  -- nullable for direct movements (manual adjustment)
  source_document_line_id uuid REFERENCES i.inventory_document_lines(id),
  source_transaction_id   uuid,                                       -- t.transactions(id) — sale-derived movements
  reason_code             text,                                       -- damaged | theft | spoilage | recount_corrected | etc.
  reference                text,                                       -- merchant or external reference (PO #, RTV #, etc.)
  performed_by_user_id    uuid REFERENCES app.users(id),
  performed_by_employee_id uuid REFERENCES e.employees(id),
  cost_basis              numeric(14,4),                              -- cost at time of movement (snapshot)
  attributes              jsonb NOT NULL DEFAULT '{}',
  created_at              timestamptz NOT NULL DEFAULT now()
  -- NOTE: no updated_at — this is append-only
);

CREATE INDEX idx_movements_tenant ON i.inventory_movements(tenant_id);
CREATE INDEX idx_movements_item ON i.inventory_movements(item_id);
CREATE INDEX idx_movements_location ON i.inventory_movements(location_id);
CREATE INDEX idx_movements_at ON i.inventory_movements(movement_at);
CREATE INDEX idx_movements_type ON i.inventory_movements(movement_type);
CREATE INDEX idx_movements_document ON i.inventory_movements(source_document_id);
CREATE INDEX idx_movements_transaction ON i.inventory_movements(source_transaction_id) WHERE source_transaction_id IS NOT NULL;
CREATE INDEX idx_movements_position_recompute ON i.inventory_movements(tenant_id, item_id, location_id, COALESCE(zone_id, '00000000-0000-0000-0000-000000000000'::uuid), movement_at DESC);
```

### Operational lifecycle

**Producers**:
- `mcp.inventory.movement.from-goods-receipt` — D028 GRN equivalent
- `mcp.inventory.movement.from-adjustment` — D019/D020 adjustment
- `mcp.inventory.movement.from-transfer` — D036/D038 transfer
- `mcp.inventory.movement.from-rtv` — D030/D032/D035 RTV
- `mcp.inventory.movement.from-sale` — derived from t.transactions completion
- `mcp.inventory.movement.from-cycle-count` — D029 stock-count corrections
- `mcp.inventory.movement.reserve` — soft reservation for orders
- `mcp.inventory.movement.release-reservation` — order cancelled or fulfilled

**Consumers**:
- `mcp.inventory.position.materialize` — every movement triggers position recompute (atomic in same transaction)
- `mcp.financial.stock-ledger.post` — financial valuation entry per movement (Canary `ledger.stock_ledger_entries`)
- `mcp.audit.shrink.detect` — pattern detection on adjustment movements (Q module)
- `mcp.metrics.movement-velocity` — daily/weekly aggregations
- `mcp.replenishment.signal.from-receipt` — receipt completion triggers replenishment recalc

**SLA at producer**: real-time, atomic with position update (transactional), append-only (no updates ever).
**Consumer freshness**: position recompute synchronous in same transaction; downstream consumers async <5s.

### Provenance

- **ARTS reference**: InventoryMovement (one event per atomic SOH change)
- **GSLM Supply (S0)**: 19 entities — most fold here as movement_type variants
- **CRDM folded**: `CRDM_GoodsReceived` + `CRDM_StockAdjustment` + `CRDM_SupplierReturn` + `CRDM_Transfer` + `CRDM_WebItemReturn` (5 CRDM entities → 1 movement table with discriminator)
- **TOM junctions**: D028 (GRN RWMS→TIMS), D019/D020/D033 (adjustments), D029/D022 (stock counts), D030/D032/D035 (RTV), D036/D037/D038 (transfers)
- **Canary current**: `ledger.stock_ledger_entries` is financial counterpart; `i.inventory_movements` is physical
- **Justification**: Append-only event log gives us full audit trail and replay capability. Position table can always be recomputed from movements (sum of deltas) — useful for debugging, reconciling with physical counts. Movement-type discriminator avoids 5+ separate tables (one per movement kind) per §9 cardinality rule. Single index `idx_movements_position_recompute` supports the position-materialization query path.

---

## i.inventory_documents

**ARTS reference**: ARTS InventoryDocument (header for receipt/transfer/count/return).
**Module**: D.

### Schema

```sql
CREATE TABLE i.inventory_documents (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id           uuid NOT NULL REFERENCES app.tenants(id),
  document_type       text NOT NULL,                              -- goods_receipt | transfer_out | transfer_in | rtv | stock_count | adjustment_batch
  document_number     text NOT NULL,                              -- merchant-assigned (PO# for receipt, RTV# for return, etc.)
  source_location_id  uuid REFERENCES l.locations(id),            -- origin (transfers, RTVs); NULL for receipts
  destination_location_id uuid REFERENCES l.locations(id),         -- destination (receipts, transfers); NULL for RTVs
  vendor_id           uuid REFERENCES m.vendors(id),               -- for receipts and RTVs
  related_order_id    uuid,                                        -- o.purchase_orders(id) when known — Chunk 5b
  status              text NOT NULL DEFAULT 'draft',               -- draft | in_progress | completed | cancelled | reconciled
  expected_at         timestamptz,
  completed_at        timestamptz,
  total_quantity      numeric(14,4),                               -- sum of line quantities (denormalized)
  total_cost          numeric(14,4),                               -- sum of line cost (denormalized)
  performed_by_user_id uuid REFERENCES app.users(id),
  attributes          jsonb NOT NULL DEFAULT '{}',                 -- carrier, BOL #, packing list URL, photo evidence URLs
  created_at          timestamptz NOT NULL DEFAULT now(),
  updated_at          timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, document_type, document_number)
);

CREATE INDEX idx_idocs_tenant ON i.inventory_documents(tenant_id);
CREATE INDEX idx_idocs_type ON i.inventory_documents(document_type);
CREATE INDEX idx_idocs_status ON i.inventory_documents(status) WHERE status NOT IN ('completed', 'cancelled');
CREATE INDEX idx_idocs_destination ON i.inventory_documents(destination_location_id);
CREATE INDEX idx_idocs_source ON i.inventory_documents(source_location_id);
CREATE INDEX idx_idocs_vendor ON i.inventory_documents(vendor_id);
CREATE INDEX idx_idocs_related_order ON i.inventory_documents(related_order_id);
```

### Operational lifecycle

**Producers**:
- `mcp.inventory.document.create` — draft document at intent (PO arrival expected, transfer scheduled)
- `mcp.inventory.document.complete` — when physical activity done (sets `completed_at`, `status='completed'`, triggers movement creation)
- `mcp.inventory.document.cancel` — abort

**Consumers**:
- `mcp.inventory.document.audit-trail` — query all activity for a location/period
- `mcp.financial.three-way-match` — match receipt document against PO and supplier invoice (F-Prefix F004 pattern)

**SLA at producer**: real-time create; complete is the trigger event for downstream movements.

### Provenance

- **ARTS reference**: InventoryDocument header
- **TOM junctions touching**: D016 (PO Download), D028 (GRN), D029 (stock count), D030 (RTV dispatch), D036 (stock transfer)
- **Justification**: Single document table with `document_type` discriminator covers all five physical-inventory-change document kinds. Status field discriminates draft (intent) → in_progress (executing) → completed (movements posted) → reconciled (matched against expected). Related-order FK cross-references Orders domain (Chunk 5b) for receipt-vs-PO reconciliation.

---

## i.inventory_document_lines

**ARTS reference**: ARTS InventoryDocumentLine.
**Module**: D.

### Schema

```sql
CREATE TABLE i.inventory_document_lines (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id           uuid NOT NULL REFERENCES app.tenants(id),
  document_id         uuid NOT NULL REFERENCES i.inventory_documents(id) ON DELETE CASCADE,
  line_number         int NOT NULL,
  item_id             uuid NOT NULL REFERENCES m.items(id) ON DELETE RESTRICT,
  expected_quantity   numeric(14,4),                              -- planned (for receipts vs PO, transfers vs request)
  actual_quantity     numeric(14,4),                              -- physically counted/received
  variance_quantity   numeric(14,4) GENERATED ALWAYS AS (COALESCE(actual_quantity, 0) - COALESCE(expected_quantity, 0)) STORED,
  variance_reason     text,                                       -- damaged | short | over | wrong_item | quality_reject
  unit_cost           numeric(14,4),                              -- per-unit cost at receipt
  lot_id              uuid REFERENCES i.inventory_lots(id),
  attributes          jsonb NOT NULL DEFAULT '{}',
  created_at          timestamptz NOT NULL DEFAULT now(),
  updated_at          timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, document_id, line_number)
);

CREATE INDEX idx_idoc_lines_tenant ON i.inventory_document_lines(tenant_id);
CREATE INDEX idx_idoc_lines_document ON i.inventory_document_lines(document_id);
CREATE INDEX idx_idoc_lines_item ON i.inventory_document_lines(item_id);
CREATE INDEX idx_idoc_lines_variance ON i.inventory_document_lines(document_id) WHERE variance_quantity != 0;
```

### Operational lifecycle

**Producers**:
- `mcp.inventory.document-line.add` — at document creation (from PO lines for receipts, from transfer order lines for transfers)
- `mcp.inventory.document-line.update-actual` — at physical count

**Consumers**:
- `mcp.inventory.movement.from-document-line` — when document completed, generates one movement per line
- `mcp.audit.variance.report` — for variance reports (received vs ordered)

**SLA at producer**: real-time.

### Provenance

- **ARTS reference**: InventoryDocumentLine
- **Justification**: Generated `variance_quantity` column eliminates application-level variance computation (always consistent with stored values). Allows variance reports without table scans.

---

## i.inventory_lots

**ARTS reference**: ARTS Lot / Serial Tracking (optional).
**Module**: D.
**Optional**: only used by lot/serial-tracked merchants (food, Rx, electronics with serials).

### Schema

```sql
CREATE TABLE i.inventory_lots (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id           uuid NOT NULL REFERENCES app.tenants(id),
  item_id             uuid NOT NULL REFERENCES m.items(id) ON DELETE RESTRICT,
  lot_number          text NOT NULL,                              -- batch/lot/serial number
  lot_type            text NOT NULL DEFAULT 'batch',              -- batch | serial | expiry | catch_weight
  expiry_date         date,                                       -- for date-tracked items
  manufacture_date    date,
  received_at         timestamptz,
  vendor_id           uuid REFERENCES m.vendors(id),
  source_document_id  uuid REFERENCES i.inventory_documents(id),  -- the receipt that introduced this lot
  status              text NOT NULL DEFAULT 'active',             -- active | quarantine | recalled | exhausted | expired
  attributes          jsonb NOT NULL DEFAULT '{}',                -- catch-weight, country-of-origin, FDA NDC, etc.
  created_at          timestamptz NOT NULL DEFAULT now(),
  updated_at          timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, item_id, lot_number)
);

CREATE INDEX idx_lots_tenant ON i.inventory_lots(tenant_id);
CREATE INDEX idx_lots_item ON i.inventory_lots(item_id);
CREATE INDEX idx_lots_expiry ON i.inventory_lots(expiry_date) WHERE expiry_date IS NOT NULL AND status = 'active';
CREATE INDEX idx_lots_status ON i.inventory_lots(status) WHERE status != 'active';
```

### Operational lifecycle

**Producers**:
- `mcp.inventory.lot.create` — at goods receipt (when item is lot-tracked)
- `mcp.inventory.lot.recall` — recall event (sets `status='recalled'`)
- `mcp.inventory.lot.expire` — scheduled job (when expiry_date < today)

**Consumers**:
- `mcp.transaction.lot.scan-resolve` — at POS for lot-tracked items
- `mcp.inventory.fefo.allocate` — first-expiry-first-out allocation for orders
- `mcp.compliance.recall.locate-stock` — find all stock of a recalled lot
- `mcp.audit.expiry.report` — daily report of items approaching expiry

**SLA at producer**: real-time at receipt; idempotent on `(tenant_id, item_id, lot_number)`.

### Provenance

- **ARTS reference**: ARTS Lot/Serial Tracking
- **GSLM**: not modeled (Walmart Item domain didn't model lots)
- **CRDM**: not modeled (POS-only)
- **TOM junctions**: not in TOM corpus
- **Justification**: Lot is referenced from `inventory_movements.lot_id` and `inventory_document_lines.lot_id` for full traceability. Recall capability (status='recalled' + locate-stock query) is a regulatory requirement for food/Rx merchants. Optional for non-lot-tracked merchants — table simply remains empty.

---

## Domain summary

**5 entities, 1 schema (i), 1 module (D)**:
- `i.inventory_positions` (~16 cols) — current SOH per item × location, with reserved/on-order/in-transit
- `i.inventory_movements` (~17 cols, append-only) — atomic event log per SOH change, all movement types unified
- `i.inventory_documents` (~17 cols) — header for receipts/transfers/counts/RTVs
- `i.inventory_document_lines` (~12 cols) — per-line detail with generated variance column
- `i.inventory_lots` (~14 cols, optional) — lot/serial/expiry tracking

**Folded from sources**:
- CRDM 5 inventory entities (`GoodsReceived`, `Transfer`, `StockAdjustment`, `SupplierReturn`, `WebItemReturn`) → 1 unified `inventory_movements` table with `movement_type` discriminator
- GSLM Supply 19 entities (S0 MDM site) → 5 SMB-2030 canonical (most folded as movement_types or attribute JSONB)
- TOM 18 D-Prefix interfaces → 8 MCP service junction patterns (movement-from-{receipt,adjustment,transfer,rtv,sale,count,reservation,release})

**MCP service junctions defined for this domain (~17)**:
- Position writers: position.materialize, position.from-stock-count
- Movement creators: movement.from-{goods-receipt, adjustment, transfer, rtv, sale, cycle-count}, movement.{reserve, release-reservation}
- Document lifecycle: document.create, document.complete, document.cancel, document-line.add, document-line.update-actual, movement.from-document-line
- Lot lifecycle: lot.create, lot.recall, lot.expire
- Consumers: scan.check-availability, fulfillment.allocate, replenishment.demand.compute, forecast.position.snapshot, inventory.report.daily, audit.shrink.detect, three-way-match (cross-cuts F), audit.variance.report, fefo.allocate, compliance.recall.locate-stock, audit.expiry.report

## Status

- **Chunk 5 complete.** 5 ARTS-Inventory-V2-aligned entities with full TOM D-Prefix lifecycle bindings.
- **Resume**: Chunk 5b — Orders domain (o schema, greenfield via J-Prefix). Target ~6-8 entities (purchase_orders, sales_orders, fulfillment_orders, allocations, ASN, BOL).
