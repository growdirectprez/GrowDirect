# Chunk 3 — Location + Space Domain (Schemas `l`, `s`)

**ARTS anchor**: ARTS Location V2 (full local PDF spec) + ARTS Planogram V2 + IXRetail Inventory V1.0 (location-portion).
**Modules**: A (Asset), S (Space).
**Entities**: 6 (locations · location_hierarchy · location_zones · planograms · planogram_positions · location_assortment).
**Folded from sources**: GSLM 16 Location + 8 Space entities → 6 SMB-2030 canonical.

## Domain narrative

ARTS Location V2 (March 2017 spec, in our local PDFs) treats Location as the abstract place; physical attributes, addresses, hierarchy, operating hours decompose into 8-12 sub-entities for full enterprise coverage. SMB-2030 doesn't need separate `OperatingHours` and `LocationContact` tables — these collapse into JSONB on the parent `locations` row. Hierarchy is recursive (banner → region → district → store, OR just store, depending on merchant). Within-store zoning (sales floors, departments, aisles, sections) uses a single `location_zones` table — a store with one floor and no zones simply has no rows here.

Space domain is planogram + assortment. `planograms` is the master plan; `planogram_positions` carries the where-does-each-item-sit detail (the S078 "most architecturally rich" interface payload). `location_assortment` answers "what items does this store carry?" — same role as GSLM's `SKUItemsInSalesOutlets` + `PackItemsInSalesOutlets`, simplified to one table with item_type discriminator.

Operational lifecycle in TOM: store master flows IDS → CRDB / IKB / GPM nightly batch (S008, S035, S074). Planogram flows IKB → GPM + SR daily transactional fan-out (S078). For Canary Go MCP services these become real-time push junctions with same producer/consumer relationships but modern cadence (real-time master propagation, daily planogram sync).

---

## l.locations

**ARTS reference**: ARTS Location V2 — RetailStore + Warehouse + DistributionCenter unified.
**Module**: A.

### Schema

```sql
CREATE TABLE l.locations (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id           uuid NOT NULL REFERENCES app.tenants(id),
  location_code       text NOT NULL,                              -- merchant or POS-native code (StoreNo equivalent)
  name                text NOT NULL,
  location_type       text NOT NULL DEFAULT 'store',              -- store | warehouse | distribution_center | dropship | virtual | popup
  parent_location_id  uuid REFERENCES l.locations(id),            -- e.g., distribution center serves stores; nullable
  banner              text,                                        -- merchant banner if multi-banner
  status              text NOT NULL DEFAULT 'active',             -- active | inactive | closed | construction | pending_open
  open_date           date,
  close_date          date,
  remodel_date        date,
  square_footage      int,
  selling_area_sqft   int,
  storage_area_sqft   int,
  channel             text,                                        -- brick | online | hybrid | popup
  format              text,                                        -- supermarket | convenience | specialty | warehouse | etc.
  currency            text NOT NULL DEFAULT 'USD',
  language            text NOT NULL DEFAULT 'en-US',               -- BCP 47
  timezone            text NOT NULL DEFAULT 'America/Los_Angeles', -- IANA
  address             jsonb DEFAULT '{}',                          -- {line1, line2, city, region, postal_code, country, latitude, longitude, county}
  contact             jsonb DEFAULT '{}',                          -- {name, phone, email, manager_name}
  operating_hours     jsonb DEFAULT '{}',                          -- {monday: [{open: "07:00", close: "22:00"}], ...}
  attributes          jsonb NOT NULL DEFAULT '{}',                 -- merchant-defined (e.g., DUNS, integrated POS ind, MSA)
  created_at          timestamptz NOT NULL DEFAULT now(),
  updated_at          timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, location_code)
);

CREATE INDEX idx_locations_tenant ON l.locations(tenant_id);
CREATE INDEX idx_locations_parent ON l.locations(parent_location_id);
CREATE INDEX idx_locations_status ON l.locations(status) WHERE status != 'active';
CREATE INDEX idx_locations_type ON l.locations(location_type);
CREATE INDEX idx_locations_address_gin ON l.locations USING gin(address);
```

### Operational lifecycle (TOM operational clock)

**Producers**:
- `mcp.master.location.create` — real-time on store/warehouse onboard (TOM C012US Store + C013US Warehouse RIB pattern)
- `mcp.master.location.update` — real-time on attribute change

**Consumers**:
- `mcp.transaction.location.lookup` — real-time at every POS event
- `mcp.inventory.location.position-init` — when location added (initialize inventory positions)
- `mcp.orders.location.assign` — at order routing
- `mcp.forecast.location.refresh` — daily (TOM J087 Store Info IL→GFO equivalent)
- `mcp.planogram.location.assign` — when location ready for planograms
- `mcp.metrics.aggregate.by-location`
- `mcp.store-line.location-attributes-push` — overnight (TOM S035 IDS→IKB pattern)

**SLA at producer**: real-time push, p95 < 200ms, idempotent on `(tenant_id, location_code)`.
**SLA at consumers**: lookup p99 < 50ms; freshness < 5s for transaction, < 24h for forecast/planogram.

### Provenance

- **ARTS reference**: Location V2 — RetailStore + Warehouse + DistributionCenter all conform to one Location entity with type discriminator
- **GSLM folded**: `SalesOutlets` + (parts of) `SalesOutletDepartments` + `SalesOutletHolidays` — operating hours + holidays into JSONB; departments into `location_zones` separately
- **TOM junctions**: C012US (store), C013US (warehouse), S035 (downstream IKB), S008 (downstream CRDB), S074 (downstream GPM), J087 (downstream GFO)
- **Canary current**: `app.locations` + `app.location_hierarchy` — superseded; hierarchy moves to separate table for clarity
- **Justification**: Single `locations` table covers store/warehouse/DC because they share 80% of attributes; type discriminator and partial indexes optimize query paths. Address/contact/operating_hours in JSONB because they're rarely queried structurally and vary by region (US has state, UK has county, JP has prefecture). Latitude/longitude in address JSONB enables geospatial queries with Postgres `point` cast or PostGIS extension.

---

## l.location_hierarchy

**ARTS reference**: ARTS Location V2 — LocationHierarchy.
**Module**: A.

### Schema

```sql
CREATE TABLE l.location_hierarchy (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       uuid NOT NULL REFERENCES app.tenants(id),
  parent_id       uuid REFERENCES l.location_hierarchy(id),     -- NULL for root
  code            text NOT NULL,                                  -- e.g., "WEST_REGION", "DIST_LA_NORTH"
  name            text NOT NULL,
  hierarchy_type  text NOT NULL DEFAULT 'organizational',         -- organizational | distribution | banner | tax_zone
  level           int NOT NULL,                                   -- denormalized depth
  path            ltree,                                          -- materialized path
  attributes      jsonb NOT NULL DEFAULT '{}',
  status          text NOT NULL DEFAULT 'active',
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, hierarchy_type, code)
);

CREATE TABLE l.location_hierarchy_assignments (
  location_id     uuid NOT NULL REFERENCES l.locations(id) ON DELETE CASCADE,
  hierarchy_id    uuid NOT NULL REFERENCES l.location_hierarchy(id) ON DELETE CASCADE,
  PRIMARY KEY (location_id, hierarchy_id)
);

CREATE INDEX idx_loc_hier_tenant ON l.location_hierarchy(tenant_id);
CREATE INDEX idx_loc_hier_parent ON l.location_hierarchy(parent_id);
CREATE INDEX idx_loc_hier_path ON l.location_hierarchy USING gist(path);
CREATE INDEX idx_loc_hier_assign_loc ON l.location_hierarchy_assignments(location_id);
CREATE INDEX idx_loc_hier_assign_hier ON l.location_hierarchy_assignments(hierarchy_id);
```

### Operational lifecycle

**Producers**:
- `mcp.master.location-hierarchy.upsert` — real-time when hierarchy node changes (TOM J002 Location Hierarchy IDS→UDD)
- `mcp.master.location-hierarchy.assign` — real-time when location added to hierarchy node

**Consumers**:
- `mcp.metrics.aggregate.by-hierarchy` — rollup queries (district sales, region performance)
- `mcp.pricing.zone-promotion.scope-by-hierarchy` — promotions targeting a region/banner
- `mcp.financial.tax-zone.resolve` — tax computation

**SLA at producer**: real-time, p95 < 200ms.

### Provenance

- **ARTS reference**: LocationHierarchy
- **GSLM folded**: hierarchy was inline columns on `SalesOutlets` (banner, region) — promoted to separate hierarchy table for multi-hierarchy support
- **Recovery DDL**: `Ref_LocationHierarchy` (from `wmt-ref-location-create.sql`) — Walmart's reference hierarchy, validates the structure
- **TOM junctions**: J002 (Location Hierarchy IDS→UDD), J006 (Commercial Hierarchy IDS→UDD)
- **Justification**: Multiple hierarchy types coexist (organizational, distribution, tax zones, banners). Many-to-many assignments table because a single store may belong to multiple hierarchies (e.g., West Region for ops, Tax Zone CA for finance, Banner X for merchandising).

---

## l.location_zones

**ARTS reference**: ARTS RetailStore — within-store geography.
**Module**: A (with cross-cuts to S for planogram positioning).

### Schema

```sql
CREATE TABLE l.location_zones (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       uuid NOT NULL REFERENCES app.tenants(id),
  location_id     uuid NOT NULL REFERENCES l.locations(id) ON DELETE CASCADE,
  parent_zone_id  uuid REFERENCES l.location_zones(id),
  code            text NOT NULL,                          -- e.g., "FLOOR_1", "GROCERY_AISLE_3", "ENDCAP_5"
  name            text NOT NULL,
  zone_type       text NOT NULL DEFAULT 'department',     -- floor | department | aisle | section | endcap | bin | shelf | cooler
  level           int NOT NULL,                            -- depth within location
  path            ltree,
  geometry        jsonb DEFAULT '{}',                      -- {coordinates, dimensions} for store-mapping later
  attributes      jsonb NOT NULL DEFAULT '{}',
  status          text NOT NULL DEFAULT 'active',
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, location_id, code)
);

CREATE INDEX idx_zones_tenant ON l.location_zones(tenant_id);
CREATE INDEX idx_zones_location ON l.location_zones(location_id);
CREATE INDEX idx_zones_parent ON l.location_zones(parent_zone_id);
CREATE INDEX idx_zones_path ON l.location_zones USING gist(path);
```

### Operational lifecycle

**Producers**:
- `mcp.master.location-zone.upsert` — when store layout configured
- `mcp.master.location-zone.from-planogram-derive` — planogram-driven zone creation

**Consumers**:
- `mcp.planogram.position.assign-zone` — every planogram position references a zone
- `mcp.transaction.line-item.zone-attribute` — for shrink/loss-by-zone analytics
- `mcp.inventory.cycle-count.scope-by-zone`

**SLA at producer**: not time-critical (configuration data).

### Provenance

- **ARTS reference**: ARTS extends Location with sub-zone concepts (departments, sections)
- **GSLM folded**: `SalesFloors` + `SalesFloorsInSalesOutlet` + `Sections` + `SalesOutletDepartments` (4 entities → 1 with `zone_type` discriminator + recursive parent)
- **TOM junctions**: C012US carries store hierarchy fields that imply zones; explicit zone management is in S033 IDS→IKB pattern
- **Justification**: Single recursive table with discriminator handles 0-level (no zones) through N-level (floor → dept → aisle → shelf → bin) without schema change. Geometry as JSONB allows future store-mapping/AR overlays without column changes.

---

## s.planograms

**ARTS reference**: ARTS Planogram V2 (LCWD ARTS Planogram Domain Model V2.0 — local PDF).
**Module**: S.

### Schema

```sql
CREATE TABLE s.planograms (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id           uuid NOT NULL REFERENCES app.tenants(id),
  planogram_code      text NOT NULL,                      -- merchant-assigned (e.g., "GROCERY_GR_VALID_24Q1")
  name                text NOT NULL,
  category_id         uuid REFERENCES m.product_categories(id),  -- the merchandise category this plans
  effective_start     date,
  effective_end       date,                               -- NULL for indefinite
  layout_dimensions   jsonb DEFAULT '{}',                 -- {width_cm, height_cm, depth_cm, shelf_count, etc.}
  status              text NOT NULL DEFAULT 'draft',      -- draft | approved | active | retired
  approved_by         uuid REFERENCES app.users(id),
  approved_at         timestamptz,
  attributes          jsonb NOT NULL DEFAULT '{}',
  created_at          timestamptz NOT NULL DEFAULT now(),
  updated_at          timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, planogram_code)
);

CREATE TABLE s.planogram_assignments (
  planogram_id    uuid NOT NULL REFERENCES s.planograms(id) ON DELETE CASCADE,
  location_id     uuid NOT NULL REFERENCES l.locations(id) ON DELETE CASCADE,
  zone_id         uuid REFERENCES l.location_zones(id),
  assigned_at     timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (planogram_id, location_id, COALESCE(zone_id, '00000000-0000-0000-0000-000000000000'::uuid))
);

CREATE INDEX idx_planograms_tenant ON s.planograms(tenant_id);
CREATE INDEX idx_planograms_category ON s.planograms(category_id);
CREATE INDEX idx_planograms_status ON s.planograms(status);
CREATE INDEX idx_planogram_assign_loc ON s.planogram_assignments(location_id);
```

### Operational lifecycle

**Producers**:
- `mcp.space.planogram.upsert` — when planogram designed (in JDA-equivalent or merchant tool)
- `mcp.space.planogram.assign-location` — when planogram applied to a store/zone

**Consumers**:
- `mcp.space.position.lookup` (FK from planogram_positions)
- `mcp.store-line.planogram-push` — daily (TOM S078 IKB→GPM+SR pattern)
- `mcp.inventory.replenishment.use-planogram-capacity` — capacity-driven replenishment (TOM S075 GPM→SR pattern)

**SLA at producer**: not time-critical (planning data); idempotent on `(tenant_id, planogram_code)`.

### Provenance

- **ARTS reference**: ARTS Planogram V2 — local PDF spec
- **GSLM folded**: `Planogram` (1 table — minimal in GSLM SQL implementation; richer in S0 MDM site Space domain)
- **TOM junctions**: S078 (IKB→GPM+SR — the "most architecturally rich SRD interface"), S057 (Store Range Data IKB→SR), S075 (Capacity GPM→SR)
- **Justification**: Composite PK on assignments uses COALESCE-on-zone trick to allow location-wide planograms (zone_id NULL) and zone-specific planograms in same table. Layout dimensions in JSONB because planogram layout systems vary (grid-based, freeform, 3D coordinate); merchant can switch tools without schema change.

---

## s.planogram_positions

**ARTS reference**: ARTS Planogram V2 — Position / Facing.
**Module**: S.

### Schema

```sql
CREATE TABLE s.planogram_positions (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id           uuid NOT NULL REFERENCES app.tenants(id),
  planogram_id        uuid NOT NULL REFERENCES s.planograms(id) ON DELETE CASCADE,
  item_id             uuid NOT NULL REFERENCES m.items(id) ON DELETE RESTRICT,
  shelf_number        int,                                -- 1=top, N=bottom
  position_on_shelf   int,                                -- 1=left, N=right
  facings             int NOT NULL DEFAULT 1,             -- horizontal facings count
  capacity_units      int,                                -- max units this position holds
  orientation         text DEFAULT 'face_forward',        -- face_forward | sideways | hanging | etc.
  geometry            jsonb DEFAULT '{}',                 -- {x_cm, y_cm, width_cm, height_cm}
  attributes          jsonb NOT NULL DEFAULT '{}',
  created_at          timestamptz NOT NULL DEFAULT now(),
  updated_at          timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, planogram_id, item_id, shelf_number, position_on_shelf)
);

CREATE INDEX idx_positions_tenant ON s.planogram_positions(tenant_id);
CREATE INDEX idx_positions_planogram ON s.planogram_positions(planogram_id);
CREATE INDEX idx_positions_item ON s.planogram_positions(item_id);
```

### Operational lifecycle

**Producers**:
- `mcp.space.position.upsert` — when planogram positions defined

**Consumers**:
- `mcp.store-line.position-push` — daily (TOM S078 transactional fan-out to GPM+SR)
- `mcp.inventory.replenishment.calc-by-position` — uses capacity for replenishment qty
- `mcp.shelf-edge.label-print` — TOM S075 GPM→SR capacity drives label print

**SLA at producer**: not time-critical (planning); high volume per planogram (50-500 positions per planogram typical).
**SLA at consumers**: daily push, transactional fan-out across two downstream targets (GPM and SR per S078 pattern).

### Provenance

- **ARTS reference**: ARTS Planogram V2 — Position / Facing detail
- **GSLM folded**: not present in GSLM SQL; in S0 MDM Space domain
- **TOM junctions**: S078 (IKB→GPM+SR — the rich one), S075 (GPM→SR capacity), S077 (GFO→SR actual range feedback)
- **Justification**: Single position-per-row enables flexibility (item-on-shelf, item-in-bin, item-on-endcap all share the same row shape). Geometry JSONB because positioning is rarely queried structurally beyond same-shelf adjacency.

---

## l.location_assortment

**ARTS reference**: ARTS Item-Location association (Range / Assortment).
**Module**: M (item-side) + A (location-side) + S (planogram-side).

### Schema

```sql
CREATE TABLE l.location_assortment (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id           uuid NOT NULL REFERENCES app.tenants(id),
  location_id         uuid NOT NULL REFERENCES l.locations(id) ON DELETE CASCADE,
  item_id             uuid NOT NULL REFERENCES m.items(id) ON DELETE CASCADE,
  zone_id             uuid REFERENCES l.location_zones(id),
  assortment_tier     text NOT NULL DEFAULT 'store_carry',  -- store_carry | warehouse_only | expanded_storefront | dropship | deleted
  effective_start     date,
  effective_end       date,
  source_planogram_id uuid REFERENCES s.planograms(id),     -- if assortment driven by planogram
  attributes          jsonb NOT NULL DEFAULT '{}',
  status              text NOT NULL DEFAULT 'active',
  created_at          timestamptz NOT NULL DEFAULT now(),
  updated_at          timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, location_id, item_id, COALESCE(zone_id, '00000000-0000-0000-0000-000000000000'::uuid))
);

CREATE INDEX idx_assortment_tenant ON l.location_assortment(tenant_id);
CREATE INDEX idx_assortment_location ON l.location_assortment(location_id);
CREATE INDEX idx_assortment_item ON l.location_assortment(item_id);
CREATE INDEX idx_assortment_active ON l.location_assortment(location_id, status) WHERE status = 'active';
```

### Operational lifecycle

**Producers**:
- `mcp.assortment.upsert` — when item authorized for location (manual or planogram-derived)
- `mcp.assortment.from-planogram-derive` — automatic from planogram positions
- `mcp.assortment.lifecycle-event` — new product launch / discontinuation (TOM S047 launches/delists)

**Consumers**:
- `mcp.transaction.scan-validate` — verify item is sellable at this location
- `mcp.orders.replenishment.scope-by-assortment` — only order what's carried
- `mcp.inventory.position.scope-by-assortment` — only track for assorted items
- `mcp.forecast.demand.scope-by-assortment` (TOM J009 Authorised Range)
- `mcp.metrics.lost-sale.detect` — scan for non-assorted item = lost sale signal

**SLA at producer**: real-time on assortment change.
**SLA at consumers**: lookup p99 < 30ms (real-time during POS scan).

### Provenance

- **ARTS reference**: ARTS Item-Location association (Range)
- **GSLM folded**: `SKUItemsInSalesOutlets` + `PackItemsInSalesOutlets` (2 entities → 1 with item-type-discriminator already on `m.items`)
- **TOM junctions**: J009 (Authorised Range and Shelf Capacities GFO→UDD), S047 (Store Range, Capacity, New/Discontinued SR→GFO), S077 (Actual Range GFO→SR)
- **Memory reference**: `project_multi_tier_assortment_model` — three-tier model (store / warehouse / expanded) — implemented via `assortment_tier` column
- **Justification**: Single assortment table with `assortment_tier` column captures the founder's documented three-tier model (store/warehouse/expanded) plus dropship and deleted states. `source_planogram_id` traceability lets assortment changes be reversed if planogram retired. COALESCE-PK pattern allows location-wide and zone-specific assortment in same table.

---

## Domain summary

**6 entities, 2 schemas (l, s), 2 modules (A + S)**:
- `l.locations` (~24 cols) — store/warehouse/DC unified
- `l.location_hierarchy` + `l.location_hierarchy_assignments` (~10 + 2 cols) — multi-hierarchy
- `l.location_zones` (~12 cols) — within-location recursive
- `s.planograms` + `s.planogram_assignments` (~14 + 4 cols) — master + location binding
- `s.planogram_positions` (~13 cols) — item placement detail
- `l.location_assortment` (~13 cols) — item-location authorization with multi-tier

**Folded from sources**:
- GSLM 16 Location entities → 3 (`l.locations` collapses store/warehouse/DC; `l.location_zones` collapses 4 inside-store entities; hierarchy promoted to separate)
- GSLM 8 Space entities → 3 (`s.planograms` master, `s.planogram_positions` detail, `l.location_assortment` for the SKU-in-store relationship)

**MCP service junctions defined for this domain (~16)**:
- Producers: location create/update, hierarchy upsert/assign, zone upsert, planogram upsert/assign-location, position upsert, assortment upsert/from-planogram/lifecycle-event
- Consumers: transaction lookup, scan-validate, inventory position-init, orders assign + replenishment scope, forecast refresh, planogram push, position push (transactional fan-out per S078), shelf-edge label print, metrics aggregate by location/hierarchy, lost-sale detect

## Status

- **Chunk 3 complete.** 6 ARTS-Location-V2-aligned entities with TOM S-Prefix lifecycle bindings.
- **Resume**: Chunk 4 — Party domain (Customer + Employee + Vendor cross-reference). ARTS Party hierarchy. Target ~5-7 entities.
