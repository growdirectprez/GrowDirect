# Chunk 2 — Item Domain (Schema `m`)

**ARTS anchor**: ARTS Item (ODM) + IXRetail Inventory V1.0 + ARTS standard Vendor / Pricing / Hierarchy entities.
**Module**: M (Merchandising).
**Entities**: 6 (items · product_categories · vendors · item_vendors · item_barcodes · item_packs).
**Folded from sources**: GSLM 22 Item entities → 6 SMB-2030 canonical via §9 cardinality rules.

## Domain narrative

The Item domain is the master data spine for everything sold. ARTS canonical decomposes Item across Style/SKU/Pack/Variant/Hierarchy — appropriate for 4,000-store enterprise estates with millions of SKUs. SMB-2030 retailers carry 1K-50K SKUs across 1-100 stores; over-decomposition costs more than it returns. We collapse style variants into JSONB (`attributes`), collapse 6-level merchandise hierarchy into a single recursive `product_categories` table, and keep packs as a single composition table (used only when pack-aware).

Operational lifecycle in TOM: items are produced/updated by `mcp.master.item.*` junctions (replacing C001/C002/C003/C008/C010/C012/C013 RIB pattern), consumed by `mcp.{transaction,forecast,planogram,store-line}.item.lookup` junctions across all downstream domains. Real-time push at producer; consumer freshness varies (real-time for transaction lookup, daily for forecast, half-hourly for missed-barcode recovery).

---

## m.items

**ARTS reference**: ARTS Item (ODM) — Item / SKU / Style consolidated.
**Module**: M.

### Schema

```sql
CREATE TABLE m.items (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id           uuid NOT NULL REFERENCES app.tenants(id),
  sku                 text NOT NULL,                                 -- merchant's primary SKU
  description         text NOT NULL,                                 -- shelf-name (full-text indexed)
  short_description   text,                                          -- receipt-name
  item_type           text NOT NULL DEFAULT 'standard',              -- standard | service | giftcard | tare | pack | bundle
  category_id         uuid REFERENCES m.product_categories(id),      -- canonical category (single FK; see categories table for hierarchy)
  unit_of_measure     text NOT NULL DEFAULT 'EA',                    -- EA | LB | KG | OZ | GAL | etc. (UN/ECE Recommendation 20)
  uom_quantity        numeric(10,4) NOT NULL DEFAULT 1,              -- e.g., 0.5 LB per unit
  default_price       numeric(12,4),                                 -- catalog price; per-location overrides in p.item_prices
  default_cost        numeric(12,4),                                 -- last-known cost; vendor-specific in m.item_vendors
  default_currency    text NOT NULL DEFAULT 'USD',                   -- ISO 4217
  tax_class           text,                                          -- tax classification key (lookup in p.tax_classes)
  food_stamp_eligible boolean NOT NULL DEFAULT false,                -- US SNAP/EBT
  age_restriction     int,                                           -- minimum buyer age (alcohol, tobacco, Rx)
  weighable           boolean NOT NULL DEFAULT false,                -- requires scale at POS
  attributes          jsonb NOT NULL DEFAULT '{}',                   -- style variants (color, size), vertical fields (Rx NDC, food calories), merchant-defined
  status              text NOT NULL DEFAULT 'active',                -- active | discontinued | seasonal | hidden
  created_at          timestamptz NOT NULL DEFAULT now(),
  updated_at          timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, sku)
);

CREATE INDEX idx_items_tenant ON m.items(tenant_id);
CREATE INDEX idx_items_category ON m.items(category_id);
CREATE INDEX idx_items_status ON m.items(status) WHERE status != 'active';
CREATE INDEX idx_items_description_trgm ON m.items USING gin(description gin_trgm_ops);
CREATE INDEX idx_items_attributes ON m.items USING gin(attributes);
```

### Operational lifecycle (TOM operational clock)

**Producers**:
- `mcp.master.item.create` — real-time push when merchant or import creates an item (TOM equivalent: C001US RMS→IDS via RIB JMS)
- `mcp.master.item.update` — real-time push on attribute change (C001US update path)
- `mcp.master.item.delete` — soft-delete via status change (C001US ItemRef delete path)

**Consumers**:
- `mcp.transaction.item.lookup` — real-time, p99 < 50ms (downstream of every POS scan)
- `mcp.inventory.item.position-refresh` — real-time on movement (D028 GRN, D019 adjustment, etc.)
- `mcp.pricing.item.price-resolve` — real-time at quote/checkout
- `mcp.forecast.item.daily-refresh` — daily batch (TOM J052/J054/J057 equivalent)
- `mcp.store-line.item.attributes-push` — overnight + half-hourly emergency (TOM C023+C045+C027 PLU feed)
- `mcp.planogram.item.update` — daily (TOM S036 equivalent)

**SLA at producer**: latency p95 < 200ms, idempotent on `(tenant_id, sku)`, atomicity transactional with attribute writes.
**SLA at consumers**: real-time lookups p99 < 50ms; freshness < 5s for lookup, < 24h for forecast.

### Provenance

- **ARTS Item ODM** (structural anchor) — Item canonical with extension via attributes
- **GSLM folded**: `SKUItems` + `Styles` + `StyleVariants` + `StyleVariantValues` + `StyleVariantGroups` + `StyleVariantGroupAssignments` + `ArticleItems` + `ArticleTypes` + `Merchandise` + `MerchandiseAttributesLanguages` (10 GSLM entities → 1 + JSONB; variant decomposition → `attributes`)
- **CRDM operational counterpart**: `CRDM_Item` is the line-item event in T schema (`t.transaction_line_items`); not the master record
- **TOM junctions touching**: C001US/TR (Product), C002US (Department→category), C003US (Class/SubClass→category), C023/C027/C045/C054 (PLU feed)
- **Canary current**: `app.products` — superseded by `m.items`

### Justification

Single canonical product master with `item_type` discriminator avoids the ARTS Item/SKU/Pack 3-table split that hurts SMB query performance with no scale benefit. Style variants in JSONB (per §5) — merchants without variants pay zero cost; merchants with them get full flexibility. Tax/food-stamp/age fields surface as columns because they're queried structurally at every POS scan. Pricing intentionally split into `p.item_prices` (multi-location overrides) — `default_price` here is the catalog fallback, not the source of truth for sale price.

---

## m.product_categories

**ARTS reference**: ARTS Item Hierarchy (MerchandiseHierarchy collapsed).
**Module**: M.

### Schema

```sql
CREATE TABLE m.product_categories (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       uuid NOT NULL REFERENCES app.tenants(id),
  parent_id       uuid REFERENCES m.product_categories(id),  -- NULL for root
  code            text NOT NULL,                              -- merchant or POS-native category code
  name            text NOT NULL,
  level           int NOT NULL,                               -- depth (0=root); denormalized for query speed
  path            ltree,                                      -- materialized path for subtree queries (Postgres ltree)
  attributes      jsonb NOT NULL DEFAULT '{}',                -- merchant-defined (e.g., margin tier, demand class)
  status          text NOT NULL DEFAULT 'active',
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, code)
);

CREATE INDEX idx_categories_tenant ON m.product_categories(tenant_id);
CREATE INDEX idx_categories_parent ON m.product_categories(parent_id);
CREATE INDEX idx_categories_path ON m.product_categories USING gist(path);
```

### Operational lifecycle

**Producers**:
- `mcp.master.category.upsert` — real-time on hierarchy change (TOM C002US/C003US RIB pattern)

**Consumers**:
- `mcp.master.item.lookup` (FK from items)
- `mcp.metrics.aggregate.by-category` — daily rollup (M and Q modules)
- `mcp.pricing.promotion.scope-by-category`
- `mcp.store-line.hierarchy-push` — daily batch (TOM C024/C025)

**SLA at producer**: real-time, p95 < 100ms, idempotent on `(tenant_id, code)`.

### Provenance

- **ARTS reference**: MerchandiseHierarchy (recursive)
- **GSLM folded**: `BusinessDivisions` + `Departments` + `Classes` + `SubClasses` + `Finelines` + `Sections` (6 levels → recursive single table; depth in `level` column)
- **TOM junctions**: C002US, C003US, C024+C025 (downstream Storeline)
- **Canary current**: not present — net-new
- **Justification**: 6-level enterprise hierarchy is over-decomposition for SMB. Recursive table with `path ltree` supports any depth (1, 3, or 6 levels) without schema change. ltree gist index gives O(log n) subtree queries.

---

## m.vendors

**ARTS reference**: ARTS Vendor / Supplier (Party hierarchy).
**Module**: M (with cross-cuts to F for AP and D for receiving).

### Schema

```sql
CREATE TABLE m.vendors (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       uuid NOT NULL REFERENCES app.tenants(id),
  vendor_code     text NOT NULL,                          -- merchant-assigned or POS-native
  name            text NOT NULL,                          -- legal/trading name
  short_name      text,
  vendor_type     text NOT NULL DEFAULT 'supplier',       -- supplier | manufacturer | distributor | broker | dropship
  primary_contact jsonb DEFAULT '{}',                     -- {name, email, phone, fax}
  address         jsonb DEFAULT '{}',                     -- {line1, line2, city, region, postal_code, country, timezone}
  payment_terms   text,                                   -- 'NET30' | 'COD' | 'PREPAY' | etc.
  currency        text DEFAULT 'USD',                     -- ISO 4217
  tax_id          text,                                   -- EIN/VAT/TIN — sensitive (PII tier 2)
  attributes      jsonb NOT NULL DEFAULT '{}',
  status          text NOT NULL DEFAULT 'active',         -- active | inactive | hold
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, vendor_code)
);

CREATE INDEX idx_vendors_tenant ON m.vendors(tenant_id);
CREATE INDEX idx_vendors_status ON m.vendors(status) WHERE status != 'active';
CREATE INDEX idx_vendors_name_trgm ON m.vendors USING gin(name gin_trgm_ops);
```

### Operational lifecycle

**Producers**:
- `mcp.master.vendor.upsert` — real-time on RMS supplier change (TOM C008US RIB pattern)
- `mcp.master.vendor.from-financial-sync` — F-Prefix F012 (OFi → RMS) — vendor master originates in financial system, syncs to operational

**Consumers**:
- `mcp.master.item-vendor.lookup` (FK from item_vendors)
- `mcp.orders.purchase-order.assign-vendor`
- `mcp.financial.invoice.match-vendor` (three-way match — F004/F014)
- `mcp.distribution.goods-received.note-vendor` (D028 GRN)

**SLA at producer**: real-time push, idempotent on `(tenant_id, vendor_code)`.

### Provenance

- **ARTS reference**: Vendor (Party subtype)
- **GSLM**: `Vendors` (1 table — minimal in GSLM SQL implementation; richer in S0 MDM site Supply domain)
- **TOM junctions**: C008US (operational), F012 (financial-source-of-truth pattern)
- **Canary current**: not present — net-new
- **Justification**: Financial-system origin (F012 OFi→RMS) is a critical pattern — vendor master has dual lineage (financial onboarding + operational ops). Both consumed by the same canonical entity. Address and contact in JSONB because internationalization variability (US uses state, UK uses county, JP uses prefecture).

---

## m.item_vendors

**ARTS reference**: ARTS ItemVendor (Vendor-Item association).
**Module**: M.

### Schema

```sql
CREATE TABLE m.item_vendors (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id           uuid NOT NULL REFERENCES app.tenants(id),
  item_id             uuid NOT NULL REFERENCES m.items(id) ON DELETE CASCADE,
  vendor_id           uuid NOT NULL REFERENCES m.vendors(id) ON DELETE RESTRICT,
  vendor_sku          text,                              -- vendor's identifier for the item
  vendor_description  text,                              -- vendor's catalog description
  unit_cost           numeric(12,4),                     -- vendor's per-unit cost
  case_pack_qty       int DEFAULT 1,                     -- units per case
  min_order_qty       int DEFAULT 1,
  lead_time_days      int,
  is_primary          boolean NOT NULL DEFAULT false,    -- the default vendor for this item
  country_of_origin   text,                              -- ISO 3166 alpha-2
  attributes          jsonb NOT NULL DEFAULT '{}',
  status              text NOT NULL DEFAULT 'active',
  created_at          timestamptz NOT NULL DEFAULT now(),
  updated_at          timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, item_id, vendor_id),
  CONSTRAINT one_primary_per_item EXCLUDE (item_id WITH =) WHERE (is_primary = true AND status = 'active')
);

CREATE INDEX idx_item_vendors_tenant ON m.item_vendors(tenant_id);
CREATE INDEX idx_item_vendors_item ON m.item_vendors(item_id);
CREATE INDEX idx_item_vendors_vendor ON m.item_vendors(vendor_id);
CREATE INDEX idx_item_vendors_primary ON m.item_vendors(item_id) WHERE is_primary = true;
```

### Operational lifecycle

**Producers**:
- `mcp.master.item-vendor.assign` — real-time when item-vendor link created (subset of C001US payload — StyleSupplier, SKUSupplier, PackSupplier)
- `mcp.master.item-vendor.update-cost` — when cost changes (vendor PO ack F013)

**Consumers**:
- `mcp.orders.purchase-order.lookup-vendor-cost` — at PO creation
- `mcp.orders.suggest-replenishment-vendor` — daily forecast (J100 Item-Warehouse-Supplier pattern)
- `mcp.financial.invoice.cost-validate` — three-way match against received invoice

**SLA at producer**: real-time, EXCLUDE constraint enforces single primary vendor per item per tenant.

### Provenance

- **ARTS reference**: ItemVendor association
- **GSLM**: `SKUItemVendors` (folded — collapses Style/SKU/Pack vendor associations into single canonical)
- **TOM junctions**: C001US carries Style/SKU/Pack-Supplier as part of product master payload; J003 (Supplier Authority Data); J100 (Item-Warehouse-Supplier — denormalized for forecast)
- **Justification**: Single association table with all 3 GSLM variants folded. EXCLUDE constraint guarantees database-level uniqueness of primary vendor (no application-layer enforcement gap).

---

## m.item_barcodes

**ARTS reference**: ARTS Item Identification (UPC/EAN/GTIN).
**Module**: M.

### Schema

```sql
CREATE TABLE m.item_barcodes (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       uuid NOT NULL REFERENCES app.tenants(id),
  item_id         uuid NOT NULL REFERENCES m.items(id) ON DELETE CASCADE,
  barcode         text NOT NULL,                       -- the scan-string (UPC-A 12, EAN-13, GTIN-14, ITF-14, GS1 DataBar)
  barcode_type    text NOT NULL DEFAULT 'GTIN',        -- GTIN | UPC_A | EAN_13 | ITF_14 | DATABAR | INTERNAL | PLU
  uom_quantity    numeric(10,4) NOT NULL DEFAULT 1,    -- units this barcode represents (case = 12, individual = 1)
  is_primary      boolean NOT NULL DEFAULT false,
  attributes      jsonb NOT NULL DEFAULT '{}',
  status          text NOT NULL DEFAULT 'active',
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, barcode)
);

CREATE INDEX idx_barcodes_tenant ON m.item_barcodes(tenant_id);
CREATE INDEX idx_barcodes_item ON m.item_barcodes(item_id);
CREATE UNIQUE INDEX idx_barcodes_lookup ON m.item_barcodes(tenant_id, barcode) WHERE status = 'active';
```

### Operational lifecycle

**Producers**:
- `mcp.master.item-barcode.assign` — at item creation (multiple barcodes per item)
- `mcp.master.item-barcode.recover-not-on-file` — when POS scans unknown barcode (C027 NoF half-hourly recovery cycle)

**Consumers**:
- `mcp.transaction.scan-resolve` — every POS scan, p99 < 30ms
- `mcp.inventory.cycle-count.scan-resolve`

**SLA at producer**: real-time. Active-barcode unique constraint prevents duplicate scans resolving to multiple items.

### Provenance

- **ARTS reference**: Item Identification (multiple identifiers per Item)
- **GSLM**: not separately modeled (barcodes lived in SKU table)
- **TOM junctions**: C001US payload (EAN field), C027 (Not-on-File half-hourly recovery — critical for SMB-2030 where new SKUs scan-fail)
- **Justification**: Separate table because items have many barcodes (one per UoM, one per pack size) and barcodes need fast unique-key lookup. Conditional unique index allows historical/inactive barcodes to retain rows for audit without blocking new active assignments.

---

## m.item_packs

**ARTS reference**: ARTS Item Composition / Pack Hierarchy.
**Module**: M.
**Optional**: only used by pack-aware merchants. SMB-2030 default deployment can skip this table.

### Schema

```sql
CREATE TABLE m.item_packs (
  id                uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id         uuid NOT NULL REFERENCES app.tenants(id),
  pack_item_id      uuid NOT NULL REFERENCES m.items(id) ON DELETE CASCADE,    -- the parent (case/bundle)
  component_item_id uuid NOT NULL REFERENCES m.items(id) ON DELETE RESTRICT,   -- the child (each unit)
  quantity          numeric(10,4) NOT NULL,                                    -- e.g., 12 for "12-pack"
  pack_type         text NOT NULL DEFAULT 'case',                              -- case | bundle | kit | mix
  attributes        jsonb NOT NULL DEFAULT '{}',
  created_at        timestamptz NOT NULL DEFAULT now(),
  updated_at        timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, pack_item_id, component_item_id)
);

CREATE INDEX idx_packs_tenant ON m.item_packs(tenant_id);
CREATE INDEX idx_packs_pack ON m.item_packs(pack_item_id);
CREATE INDEX idx_packs_component ON m.item_packs(component_item_id);
```

### Operational lifecycle

**Producers**:
- `mcp.master.item-pack.compose` — when pack defined

**Consumers**:
- `mcp.inventory.pack.break-down` — when pack received and decomposed to components
- `mcp.transaction.pack.sell-as-unit` — when pack sold whole

**SLA at producer**: not time-critical (master data); idempotent on `(tenant_id, pack_item_id, component_item_id)`.

### Provenance

- **ARTS reference**: Item Composition
- **GSLM folded**: `PackItems` + `PackBreakout` + `PackItemBreakout` (3 tables → 1; pack_type column captures the variant)
- **TOM junctions**: C001US carries Pack and PackSupplier in payload; D028 GRN handles pack-receipt
- **Justification**: GSLM had 3 tables for pack mechanics (item-as-pack, breakdown, breakout). All collapse to "pack composes components in quantity" — one table, one row per (pack, component) pair.

---

## Domain summary

**6 entities, 1 domain (Merchandising), 1 schema (m)**:
- `m.items` (~25 cols) — master record
- `m.product_categories` (~10 cols) — recursive hierarchy
- `m.vendors` (~14 cols) — supplier master
- `m.item_vendors` (~13 cols) — many-to-many with cost/lead-time
- `m.item_barcodes` (~9 cols) — scan-key lookup
- `m.item_packs` (~8 cols, optional) — composition

**Folded from sources**:
- GSLM 22 Item entities → 6 canonical (73% reduction via JSONB and recursive collapse, no functional loss)
- TOM C-Prefix 11 interfaces → 6 entities + 11 lifecycle bindings (each entity touched by multiple junctions)
- ARTS Item ODM core preserved; SMB-2030 cardinality-aware decomposition rules applied per §9

**Net new** (not in any source): `m.item_barcodes` as separate entity (was field on SKU in GSLM), justified by C027 lifecycle pattern + active-barcode uniqueness constraint requirement.

**MCP service junctions defined for this domain (12)**:
- Producers: `mcp.master.item.{create,update,delete}`, `mcp.master.category.upsert`, `mcp.master.vendor.upsert`, `mcp.master.vendor.from-financial-sync`, `mcp.master.item-vendor.{assign,update-cost}`, `mcp.master.item-barcode.{assign,recover-not-on-file}`, `mcp.master.item-pack.compose`
- Consumers: `mcp.transaction.item.lookup`, `mcp.transaction.scan-resolve`, `mcp.inventory.item.position-refresh`, `mcp.pricing.item.price-resolve`, `mcp.forecast.item.daily-refresh`, `mcp.store-line.item.attributes-push`, `mcp.planogram.item.update`, `mcp.metrics.aggregate.by-category`, `mcp.orders.purchase-order.lookup-vendor-cost`, `mcp.financial.invoice.match-vendor`, etc.

These will be consolidated into the Chunk 9b MCP Service Junction Inventory.

## Status

- **Chunk 2 complete.** 6 ARTS-aligned Item entities with TOM operational lifecycle bindings.
- **Resume**: Chunk 3 — Location + Space domain (l schema). ARTS Location V2 anchor (we have full PDF spec) + S-Prefix lifecycle. Target ~6-8 entities.
