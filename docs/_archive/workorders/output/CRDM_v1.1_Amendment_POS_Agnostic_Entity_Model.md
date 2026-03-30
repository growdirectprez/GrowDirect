---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# CRDM v1.1 Amendment — POS-Agnostic Entity Model

**Issue:** GRO-33 (new)
**Prepared By:** ALX (Chief of Staff)
**Date:** March 2, 2026
**Classification:** Internal — Architecture Amendment
**Origin:** Jeffe directive during GRO-20 review session
**Routes To:** Tom (schema), Jeremy (implementation), Syd (PCI review on identifiers)
**Gate:** Tom validates DDL, Jim QA reviews

---

## 0. Motivation

The CRDM v1.0 entity tables (`products`, `locations`, `employees`, `customers`) carry Square-specific column names (`square_item_id`, `square_employee_id`, `square_location_id`, `square_customer_id`) and model their fields as flat structures mirroring Square's API limitations. This creates three problems:

1. **POS lock-in at the schema level.** When Clover, Toast, or Dutchie parsers land, every entity table needs new `clover_*` / `toast_*` columns — the opposite of canonical.
2. **Square's model is thinner than retail reality.** Square supports one UPC and one SKU per item variation. It has no bundle composition API. Its category hierarchy exists but isn't surfaced in the product table. Merchants who sell kits, use multiple barcode types, or organize employees across regions hit these walls.
3. **The three-part isolation principle demands presentation-layer neutrality.** Per ADR-PLA-001 and the Unified Architecture Thesis (Section 3.3), the vocabulary pack lets a coffee shop call an employee a "Barista" and a location a "Café." But if the database column is `square_employee_id`, we've embedded vendor identity into the layer that should be source-agnostic. The presentation layer can't cleanly abstract what the data layer has already branded.

**Jeffe's directive:** "Don't lock ourselves into the Square model. Be more dynamic. Consider the three-part isolation strategy as it relates to the presentation layer."

---

## 1. Amendment 1: POS-Agnostic External Identity

### Problem

Every entity table has a `square_*_id` column. When we add a second POS, we either:
- Add `clover_*_id`, `toast_*_id`, etc. to every table (column explosion)
- Rename to a generic column and lose provenance (which POS did this entity come from?)

### Solution: `external_identities` Table

One table handles all POS-to-canonical entity mappings. The entity tables themselves become POS-agnostic.

```sql
-- Replaces all square_*_id columns across entity tables
CREATE TABLE canary_app.external_identities (
    id                  UUID            NOT NULL DEFAULT gen_random_uuid(),
    merchant_id         UUID            NOT NULL,
    entity_type         TEXT            NOT NULL,
    entity_id           UUID            NOT NULL,       -- FK to the canonical table
    source_system       TEXT            NOT NULL,       -- 'square', 'clover', 'toast', 'dutchie', etc.
    external_id         TEXT            NOT NULL,       -- the POS-native identifier
    external_id_type    TEXT            NOT NULL DEFAULT 'primary',  -- 'primary', 'secondary', 'legacy'
    metadata            JSONB,                          -- source-specific attrs that don't deserve columns
    synced_at           TIMESTAMPTZ     NOT NULL DEFAULT now(),
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),

    CONSTRAINT pk_external_identities PRIMARY KEY (id),
    CONSTRAINT fk_ei_merchant FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id) ON DELETE CASCADE,
    CONSTRAINT chk_ei_entity_type CHECK (entity_type IN (
        'product', 'product_variation', 'location', 'employee', 'customer',
        'category', 'cash_drawer', 'device', 'transaction', 'order'
    )),
    CONSTRAINT chk_ei_source_system CHECK (source_system IN (
        'square', 'clover', 'toast', 'shopify', 'dutchie', 'cova',
        'lightspeed', 'revel', 'micros', 'ncr', 'manual'
    ))
);

-- Hot lookup: "give me the canonical entity for this Square ID"
CREATE UNIQUE INDEX uix_ei_source_external
    ON external_identities (merchant_id, source_system, entity_type, external_id);

-- Reverse lookup: "what are all external IDs for this canonical entity?"
CREATE INDEX idx_ei_entity
    ON external_identities (merchant_id, entity_type, entity_id);

-- RLS
ALTER TABLE external_identities ENABLE ROW LEVEL SECURITY;
ALTER TABLE external_identities FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON external_identities
    USING (merchant_id = current_setting('app.current_merchant_id')::uuid);
```

### Migration from v1.0

```sql
-- Example: products table migration
INSERT INTO external_identities (merchant_id, entity_type, entity_id, source_system, external_id)
SELECT merchant_id, 'product', id, 'square', square_item_id
FROM products WHERE square_item_id IS NOT NULL;

-- After migration + validation:
ALTER TABLE products DROP COLUMN square_item_id;
```

Same pattern for `employees.square_employee_id`, `locations.square_location_id`, `customers.square_customer_id`.

### Parser Contract Change

The `parse_to_arts_transaction()` interface now returns canonical entity references. The sync worker resolves `external_id → entity_id` via the `external_identities` lookup, or creates a new canonical entity + identity row on first encounter.

```python
# Before (v1.0):
product = db.query(Product).filter(Product.square_item_id == square_id).first()

# After (v1.1):
identity = db.query(ExternalIdentity).filter(
    ExternalIdentity.source_system == 'square',
    ExternalIdentity.entity_type == 'product',
    ExternalIdentity.external_id == square_id,
    ExternalIdentity.merchant_id == merchant_id
).first()
product = db.query(Product).filter(Product.id == identity.entity_id).first()
```

The extra join is trivially fast on the unique index, and the Valkey entity cache (same pattern as vocabulary cache) eliminates the DB hit on warm path.

---

## 2. Amendment 2: Multi-Identifier Product Registry

### Problem

Square provides one `sku` and one `upc` per `CatalogItemVariation`. The `upc` field accepts 12-14 digit GTINs but doesn't discriminate type. In retail reality, a single product may carry a UPC-A (North America), an EAN-13 (Europe), an ISBN (books), and an internal SKU — all pointing to the same physical item.

For LP, this matters: barcode swapping (ringing up a cheap item's barcode for an expensive product) is a top-5 shrink method. Multi-identifier cross-referencing is how you catch it.

### Solution: `product_identifiers` Table

```sql
CREATE TABLE canary_app.product_identifiers (
    id                  UUID            NOT NULL DEFAULT gen_random_uuid(),
    merchant_id         UUID            NOT NULL,
    product_id          UUID            NOT NULL,
    identifier_type     TEXT            NOT NULL,
    identifier_value    TEXT            NOT NULL,
    source              TEXT            NOT NULL DEFAULT 'square',
    is_primary          BOOLEAN         NOT NULL DEFAULT false,
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),

    CONSTRAINT pk_product_identifiers PRIMARY KEY (id),
    CONSTRAINT fk_pi_merchant FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id) ON DELETE CASCADE,
    CONSTRAINT fk_pi_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    CONSTRAINT chk_pi_identifier_type CHECK (identifier_type IN (
        'UPC-A', 'UPC-E', 'EAN-13', 'EAN-8', 'GTIN-14',
        'ISBN-10', 'ISBN-13', 'SKU', 'PLU', 'INTERNAL', 'CUSTOM'
    )),
    CONSTRAINT chk_pi_source CHECK (source IN (
        'square_sku', 'square_upc', 'manual', 'import', 'scan', 'clover', 'toast'
    )),
    CONSTRAINT uix_pi_merchant_type_value UNIQUE (merchant_id, identifier_type, identifier_value)
);

-- "What product does this barcode belong to?"
CREATE INDEX idx_pi_value_lookup
    ON product_identifiers (merchant_id, identifier_value);

-- "What identifiers does this product have?"
CREATE INDEX idx_pi_product
    ON product_identifiers (merchant_id, product_id);

-- RLS
ALTER TABLE product_identifiers ENABLE ROW LEVEL SECURITY;
ALTER TABLE product_identifiers FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON product_identifiers
    USING (merchant_id = current_setting('app.current_merchant_id')::uuid);
```

### GTIN Type Inference from Square

On Square sync, auto-detect identifier type from string length:

| Length | Assigned Type | Standard |
|--------|--------------|----------|
| 8 | EAN-8 | European short-form |
| 12 | UPC-A | North American standard |
| 13 | EAN-13 | International standard |
| 14 | GTIN-14 | Case/carton level |
| Other | CUSTOM | Merchant-specific |

Square's `sku` field → type `SKU`, source `square_sku`.
Square's `upc` field → type inferred from length, source `square_upc`.

### Chirp Integration

New detection rule candidate for future sprint:

| Rule ID | Rule | Signal |
|---------|------|--------|
| C-701 | `BARCODE_MISMATCH` | Line item scanned with identifier that maps to a different product than recorded |
| C-702 | `ORPHAN_IDENTIFIER` | Barcode scanned at POS doesn't match any registered product identifier |

---

## 3. Amendment 3: Product Bundles and Composition

### Problem

Square supports Bundle Items and Combo Items in the Dashboard, but the Catalog API does not expose bundle composition (which child items make up the bundle). We see bundles as single line items — we can't decompose them to detect component-level shrink.

### Solution: `product_compositions` Table

```sql
CREATE TABLE canary_app.product_compositions (
    id                  UUID            NOT NULL DEFAULT gen_random_uuid(),
    merchant_id         UUID            NOT NULL,
    parent_product_id   UUID            NOT NULL,       -- the bundle/kit/combo
    child_product_id    UUID            NOT NULL,       -- component item
    quantity            NUMERIC(10,3)   NOT NULL DEFAULT 1,
    composition_type    TEXT            NOT NULL DEFAULT 'bundle',
    source              TEXT            NOT NULL DEFAULT 'manual',
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),

    CONSTRAINT pk_product_compositions PRIMARY KEY (id),
    CONSTRAINT fk_pc_merchant FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id) ON DELETE CASCADE,
    CONSTRAINT fk_pc_parent FOREIGN KEY (parent_product_id) REFERENCES products(id) ON DELETE CASCADE,
    CONSTRAINT fk_pc_child FOREIGN KEY (child_product_id) REFERENCES products(id) ON DELETE CASCADE,
    CONSTRAINT chk_pc_composition_type CHECK (composition_type IN ('bundle', 'kit', 'combo', 'recipe')),
    CONSTRAINT chk_pc_source CHECK (source IN ('square', 'manual', 'import', 'clover', 'toast')),
    CONSTRAINT chk_pc_quantity_positive CHECK (quantity > 0),
    CONSTRAINT uix_pc_parent_child UNIQUE (merchant_id, parent_product_id, child_product_id)
);

-- RLS
ALTER TABLE product_compositions ENABLE ROW LEVEL SECURITY;
ALTER TABLE product_compositions FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON product_compositions
    USING (merchant_id = current_setting('app.current_merchant_id')::uuid);
```

### Products Table Amendment

```sql
ALTER TABLE products
    ADD COLUMN is_composite   BOOLEAN     NOT NULL DEFAULT false,
    ADD COLUMN composite_type TEXT        CHECK (composite_type IN ('bundle', 'kit', 'combo', 'recipe', NULL));
```

- `is_composite = true` + rows in `product_compositions` = bundle/kit
- `is_composite = false` = regular sellable item
- Today the composition table is mostly `source = 'manual'` (Square API doesn't expose it). Future POS integrations may populate automatically.

---

## 4. Amendment 4: Category Hierarchy

### Problem

CRDM v1.0 has no category table. The products table references Square's `category_id` but doesn't model the hierarchy that Square's `CatalogCategory` supports (parent_category). Without hierarchy, Chirp rules can't scope to "all items in Apparel → Shoes" — they'd need flat lists.

### Solution: `categories` Table with Self-Referential Hierarchy

```sql
CREATE TABLE canary_app.categories (
    id                  UUID            NOT NULL DEFAULT gen_random_uuid(),
    merchant_id         UUID            NOT NULL,
    category_name       TEXT            NOT NULL,
    parent_category_id  UUID,                           -- NULL = root level
    hierarchy_path      TEXT,                           -- materialized: 'Apparel/Shoes/Running'
    hierarchy_depth     SMALLINT        NOT NULL DEFAULT 0,
    sort_order          SMALLINT        NOT NULL DEFAULT 0,
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),
    db_status           TEXT            NOT NULL DEFAULT 'active',

    CONSTRAINT pk_categories PRIMARY KEY (id),
    CONSTRAINT fk_cat_merchant FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id) ON DELETE CASCADE,
    CONSTRAINT fk_cat_parent FOREIGN KEY (parent_category_id) REFERENCES categories(id),
    CONSTRAINT chk_cat_no_self_ref CHECK (id != parent_category_id)
);

-- "All categories for this merchant, ordered"
CREATE INDEX idx_cat_merchant ON categories (merchant_id, hierarchy_path);

-- "All children of a category"
CREATE INDEX idx_cat_parent ON categories (merchant_id, parent_category_id);

-- Product → Category link (replaces flat category_id on products)
ALTER TABLE products
    ADD COLUMN category_id UUID,
    ADD CONSTRAINT fk_prod_category FOREIGN KEY (category_id) REFERENCES categories(id);

-- RLS
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE categories FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON categories
    USING (merchant_id = current_setting('app.current_merchant_id')::uuid);
```

### Materialized Path vs. Closure Table

Chose **materialized path** (`hierarchy_path = 'Apparel/Shoes/Running'`) over closure table because:
- Square's maximum category depth is ~5 levels — closure table is overengineered
- Materialized path supports `LIKE 'Apparel/Shoes/%'` queries for Chirp rule scoping
- Path is recomputed on category sync — not a write-heavy table

---

## 5. Amendment 5: POS-Agnostic Entity Core Fields

### Problem

Entity tables carry `square_*` naming throughout. Even beyond the ID columns, field names like `square_product` (channel type on transactions) embed vendor identity where canonical terms should live.

### Solution: Rename to Canonical Terms

This aligns the data layer with the presentation layer vocabulary system. The token registry (B-068-B) already defines canonical terms: `employee.label.singular`, `location.label.singular`, etc. The database should speak the same language.

| Current Column | Canonical Column | Table | Notes |
|---------------|-----------------|-------|-------|
| `square_employee_id` | Removed → `external_identities` | employees | See Amendment 1 |
| `square_item_id` | Removed → `external_identities` | products | See Amendment 1 |
| `square_location_id` | Removed → `external_identities` | locations | See Amendment 1 |
| `square_customer_id` | Removed → `external_identities` | customers | See Amendment 1 |
| `square_product` (channel) | `source_channel` | transactions | 'SQUARE_POS', 'SQUARE_ONLINE', etc. |
| `employee_name` | `display_name` | employees | POS-agnostic — works for any source |
| `product_name` | `display_name` | products | Same pattern |
| `location_name` | `display_name` | locations | Same pattern |

### Presentation Layer Alignment

With canonical column names, the vocabulary resolution chain becomes clean:

```
Database column: employees.display_name = "Jane Smith"
Vocabulary token: employee.label.singular = "Barista" (coffee shop) / "Budtender" (dispensary)
API response:
{
    "entity_type_key": "employee.label.singular",
    "entity_type_display": "Barista",      ← from vocabulary pack
    "display_name": "Jane Smith",           ← from canonical column
    "identifiers": [                        ← from external_identities + product_identifiers
        {"source": "square", "external_id": "TMjKx9Z..."},
        {"source": "manual", "external_id": "EMP-0042"}
    ]
}
```

The three-part isolation principle expressed at every layer:
- **Bitcoin layer:** `hash_chain(merchant_id)` — cryptographic isolation
- **Postgres layer:** `RLS(merchant_id)` + monthly partitions — relational isolation
- **Presentation layer:** `vocabulary_pack(merchant_id)` + canonical column names — linguistic isolation

No vendor name in the database. No vendor name in the API response. No vendor name in the UI. The POS is an input source, not an identity.

---

## 6. Amendment 6: Dynamic Entity Attributes

### Problem

Locations, employees, and customers all have POS-specific attributes that don't deserve dedicated columns but need to be queryable. Square locations have `capabilities` arrays. Clover employees have `role` objects. Toast locations have `service_area` metadata. Hard-coding these as columns defeats the POS-agnostic goal.

### Solution: Extend Existing JSONB Pattern

CRDM v1.0 already uses Pattern 3 (JSONB + Extracted Columns) on transactions. Apply the same pattern to entity tables:

```sql
ALTER TABLE employees
    ADD COLUMN attributes JSONB NOT NULL DEFAULT '{}';

ALTER TABLE locations
    ADD COLUMN attributes JSONB NOT NULL DEFAULT '{}';

ALTER TABLE customers
    ADD COLUMN attributes JSONB NOT NULL DEFAULT '{}';

ALTER TABLE products
    ADD COLUMN attributes JSONB NOT NULL DEFAULT '{}';
```

**Convention:** Extracted columns for fields needed by Chirp rules or hot queries. `attributes` JSONB for everything else. The parser decides what to extract vs. what to stash.

Example — Square employee sync:
```json
{
    "square_status": "ACTIVE",
    "square_created_at": "2024-01-15T09:00:00Z",
    "wage_setting": {"job_title": "Cashier", "hourly_rate_cents": 1600},
    "assigned_locations": ["LOC1", "LOC2"]
}
```

GIN index on `attributes` for any JSONB queries that prove necessary:
```sql
CREATE INDEX idx_emp_attributes ON employees USING GIN (attributes);
```

---

## 7. Amendment 7: Location-Product Authorization Matrix

### Problem

One of the deepest structural gaps in most retail data models — including Square's — is the absence of a **location-level authorized product catalog**. Square's Catalog API lets you toggle item visibility per location, but this is a soft UI preference, not a controlled authorization boundary. There is no concept of "this item is *prohibited* at this location" with enforcement and detection.

In enterprise LP, the authorized product list (APL) is a critical control:

- **Diversion detection:** An employee at Location A sells a product that's only authorized at Location B — this is either inventory diversion, a fulfillment error, or deliberate fraud
- **Regulatory compliance:** Cannabis dispensaries can only sell products licensed for their specific location. A product authorized at one dispensary may be illegal at another (different municipality, different license class)
- **Franchise control:** Franchise operators may only sell approved menu items. Unauthorized additions bypass quality control and royalty calculations
- **Pricing integrity:** A product authorized at a flagship location at $50 may not be authorized at an outlet location — selling it there at any price is a policy violation
- **Shrink attribution:** If inventory shrinks at Location A but that product was never authorized there, it was never supposed to be there in the first place — the shrink source is elsewhere in the supply chain

Square doesn't enforce this because Square is a POS, not an LP system. **This is exactly the gap Canary fills.**

### Solution: `location_product_authorizations` Table

```sql
CREATE TABLE canary_app.location_product_authorizations (
    id                  UUID            NOT NULL DEFAULT gen_random_uuid(),
    merchant_id         UUID            NOT NULL,
    location_id         UUID            NOT NULL,
    product_id          UUID,                           -- NULL = category-level rule
    category_id         UUID,                           -- NULL = product-level rule
    authorization_type  TEXT            NOT NULL DEFAULT 'authorized',
    effective_from      TIMESTAMPTZ     NOT NULL DEFAULT now(),
    effective_to        TIMESTAMPTZ,                    -- NULL = indefinite
    source              TEXT            NOT NULL DEFAULT 'manual',
    reason              TEXT,
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),
    created_by          UUID,

    CONSTRAINT pk_lpa PRIMARY KEY (id),
    CONSTRAINT fk_lpa_merchant FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id) ON DELETE CASCADE,
    CONSTRAINT fk_lpa_location FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE CASCADE,
    CONSTRAINT fk_lpa_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    CONSTRAINT fk_lpa_category FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    CONSTRAINT chk_lpa_authorization_type CHECK (authorization_type IN (
        'authorized',       -- explicitly allowed at this location
        'prohibited',       -- explicitly banned at this location
        'restricted',       -- allowed with conditions (manager override, time-of-day, etc.)
        'seasonal'          -- authorized only within effective_from → effective_to window
    )),
    CONSTRAINT chk_lpa_source CHECK (source IN (
        'pos_sync', 'manual', 'import', 'compliance', 'franchise_agreement'
    )),
    -- Must specify either product_id or category_id (or both for intersection)
    CONSTRAINT chk_lpa_target CHECK (product_id IS NOT NULL OR category_id IS NOT NULL)
);

-- "Is this product authorized at this location right now?"
CREATE INDEX idx_lpa_lookup
    ON location_product_authorizations (merchant_id, location_id, product_id)
    WHERE effective_to IS NULL OR effective_to > now();

-- "What's authorized at this location?" (full catalog view)
CREATE INDEX idx_lpa_location_catalog
    ON location_product_authorizations (merchant_id, location_id, authorization_type);

-- "Where is this product authorized?" (distribution view)
CREATE INDEX idx_lpa_product_distribution
    ON location_product_authorizations (merchant_id, product_id, location_id);

-- Category-level authorizations
CREATE INDEX idx_lpa_category
    ON location_product_authorizations (merchant_id, location_id, category_id)
    WHERE category_id IS NOT NULL;

-- RLS
ALTER TABLE location_product_authorizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE location_product_authorizations FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON location_product_authorizations
    USING (merchant_id = current_setting('app.current_merchant_id')::uuid);
```

### Resolution Logic

Authorization checks cascade from most specific to least:

```
1. Product + Location (exact match — most specific)
2. Category + Location (all products in this category at this location)
3. Default: AUTHORIZED (if no rule exists, item is assumed sellable everywhere)
```

The default-authorized model means merchants don't have to pre-populate the entire matrix. They only need to define exceptions: "Product X is prohibited at Location Y" or "Category Z is restricted to Locations A and B." The table is sparse — same philosophy as the vocabulary table.

### Chirp Integration

Three new detection rules enabled by this table:

| Rule ID | Rule | Signal | Severity |
|---------|------|--------|----------|
| C-801 | `UNAUTHORIZED_PRODUCT_SALE` | Transaction line item contains a product prohibited at the transaction's location | HIGH — always fires |
| C-802 | `RESTRICTED_PRODUCT_NO_OVERRIDE` | Restricted product sold without manager override flag | MEDIUM |
| C-803 | `SEASONAL_PRODUCT_OUT_OF_WINDOW` | Seasonal product sold outside its `effective_from → effective_to` window | MEDIUM |

Rule C-801 is the big one. In enterprise LP, unauthorized product sales are a top-tier alert — they indicate either inventory diversion, policy violation, or system misconfiguration. Every one gets investigated.

### Square Sync Behavior

Square's `CatalogItem` has a `present_at_location_ids` and `absent_at_location_ids` array. On catalog sync:

- `present_at_location_ids` → create `authorization_type = 'authorized'` rows for those locations
- `absent_at_location_ids` → create `authorization_type = 'prohibited'` rows for those locations
- If both are empty → product is available everywhere (Square default) → no rows created (Canary default-authorized)
- `source = 'pos_sync'` for all Square-derived rows

This gives us a baseline. Merchants can then add manual rules on top: "This product is also restricted at Location C because of the franchise agreement" (`source = 'franchise_agreement'`).

### Presentation Layer Alignment

The authorization status is vocabulary-driven. Token examples from the registry:

| Token Key | Default (en-US) | Coffee Shop | Cannabis |
|-----------|----------------|-------------|----------|
| `authorization.status.authorized` | Authorized | Approved | Licensed |
| `authorization.status.prohibited` | Prohibited | Not Available | Not Licensed |
| `authorization.status.restricted` | Restricted | Manager Only | Compliance Hold |
| `authorization.alert.unauthorized_sale` | Unauthorized Product Sale | Unapproved Item Sold | Unlicensed Product Detected |

The alert language adapts to the vertical. A cannabis merchant sees "Unlicensed Product Detected" — which is meaningful and actionable in their regulatory context. A coffee shop sees "Unapproved Item Sold." Same detection rule, different vocabulary. The three-part isolation principle at work.

---

## 8. Amendment 8: Device Graph — Thing of Thing

### Problem

CRDM v1.0 stores `device_id` as a flat string on the `transactions` table — a reference to whichever terminal processed the payment. But "device" is the wrong abstraction. A transaction doesn't touch one device. It touches a **graph of devices**: the POS terminal, the card reader attached to it, the customer's phone that tapped to pay, the barcode scanner that rang up the items, the cash drawer that opened, the receipt printer that fired, the scale that weighed the produce, the security camera that recorded the interaction.

Every one of these emits metadata. Every one of them is identifiable. And today we're capturing exactly one: the POS terminal ID, as a string, with no entity behind it.

**The principle: we never drop data.** If a device touched the transaction, we capture its identity and metadata. We parse what's useful now. We stash the rest in JSONB. When something becomes valuable later — and it always does — we promote it to a column. We never go back to the POS and ask "what did the card reader's firmware version say six months ago?" because we already have it.

**Thing of thing:** Devices form a hierarchy. A card reader is a component of a terminal. A terminal is stationed at a register position. A register position is at a location. A customer's phone is a transient participant in the transaction — it's not owned by the merchant, but it contributed an NFC tap event, a device fingerprint, an IP address. An IoT scale is a peripheral that contributed a weight measurement. Each of these is a "thing" and each can be a child of another "thing."

### Solution: `devices` Table (Hierarchical, Open-Type)

```sql
CREATE TABLE canary_app.devices (
    id                  UUID            NOT NULL DEFAULT gen_random_uuid(),
    merchant_id         UUID            NOT NULL,
    location_id         UUID,                           -- current assigned location (NULL = unassigned/transient)
    parent_device_id    UUID,                           -- self-referential: card reader → terminal → station
    display_name        TEXT,                           -- merchant-given name ("Register 1", "Bar Terminal")
    device_class        TEXT            NOT NULL,       -- broad classification
    device_type         TEXT            NOT NULL,       -- specific type within class
    ownership           TEXT            NOT NULL DEFAULT 'merchant',
    manufacturer        TEXT,
    model               TEXT,
    serial_number       TEXT,
    firmware_version    TEXT,
    protocol            TEXT,                           -- how this device communicates (USB, BLE, NFC, WiFi, Ethernet, API)
    status              TEXT            NOT NULL DEFAULT 'active',
    paired_at           TIMESTAMPTZ,
    last_seen_at        TIMESTAMPTZ,
    capabilities        TEXT[],                         -- array of capability tags: ['payment', 'nfc', 'chip', 'magstripe', 'print', 'scan', 'weigh']
    raw_metadata        JSONB           NOT NULL DEFAULT '{}',  -- NEVER DROP DATA. Full device payload from source, unparsed.
    attributes          JSONB           NOT NULL DEFAULT '{}',  -- Parsed/extracted fields for query. Promoted from raw_metadata when valuable.
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),
    db_status           TEXT            NOT NULL DEFAULT 'active',

    CONSTRAINT pk_devices PRIMARY KEY (id),
    CONSTRAINT fk_dev_merchant FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id) ON DELETE CASCADE,
    CONSTRAINT fk_dev_location FOREIGN KEY (location_id) REFERENCES locations(id),
    CONSTRAINT fk_dev_parent FOREIGN KEY (parent_device_id) REFERENCES devices(id),
    CONSTRAINT chk_dev_no_self_ref CHECK (id != parent_device_id),
    CONSTRAINT chk_dev_device_class CHECK (device_class IN (
        'pos',              -- Point-of-sale systems (terminals, registers, kiosks)
        'peripheral',       -- Attached hardware (card reader, scanner, printer, scale, cash drawer)
        'customer',         -- Customer-owned devices (phone tap, wallet app, browser)
        'iot',              -- IoT sensors (scale, temperature, door sensor, camera)
        'infrastructure',   -- Network/comms (router, access point, gateway)
        'virtual'           -- Software-only (e-commerce session, API client, mobile app instance)
    )),
    CONSTRAINT chk_dev_ownership CHECK (ownership IN (
        'merchant',         -- Merchant-owned hardware (terminal, reader, printer)
        'customer',         -- Customer-owned device (phone, laptop — transient participant)
        'vendor',           -- Vendor-provided (loaner terminal, POS-provider hardware)
        'third_party',      -- Third-party integration device (delivery tablet, loyalty kiosk)
        'unknown'           -- Source didn't identify ownership
    )),
    CONSTRAINT chk_dev_status CHECK (status IN (
        'active',           -- operational
        'inactive',         -- unpaired or decommissioned
        'offline',          -- not seen within expected window
        'maintenance',      -- known downtime
        'compromised',      -- flagged by LP — do not trust
        'transient'         -- customer device or ephemeral session — appears and disappears
    ))
);

-- "All devices at this location"
CREATE INDEX idx_dev_location
    ON devices (merchant_id, location_id)
    WHERE db_status = 'active';

-- "Find device by serial number"
CREATE UNIQUE INDEX uix_dev_serial
    ON devices (merchant_id, serial_number)
    WHERE serial_number IS NOT NULL;

-- "Stale devices" — not seen recently
CREATE INDEX idx_dev_last_seen
    ON devices (merchant_id, last_seen_at)
    WHERE status = 'active';

-- "All children of a device" (thing-of-thing traversal)
CREATE INDEX idx_dev_parent
    ON devices (merchant_id, parent_device_id)
    WHERE parent_device_id IS NOT NULL;

-- "All devices of a class" (e.g., all customer devices, all IoT)
CREATE INDEX idx_dev_class
    ON devices (merchant_id, device_class);

-- Capability search (e.g., "all devices with NFC capability")
CREATE INDEX idx_dev_capabilities
    ON devices USING GIN (capabilities);

-- JSONB search on raw metadata — we never drop data, so we need to query it
CREATE INDEX idx_dev_raw_metadata
    ON devices USING GIN (raw_metadata);

-- RLS
ALTER TABLE devices ENABLE ROW LEVEL SECURITY;
ALTER TABLE devices FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON devices
    USING (merchant_id = current_setting('app.current_merchant_id')::uuid);
```

### Device Type Registry

The `device_class` + `device_type` combination is deliberately open-ended. We define the initial set but the CHECK constraint is on `device_class` only — `device_type` is freeform text within each class because hardware evolves faster than our schema.

| Class | Example Types | Ownership | Typical Parent |
|-------|-------------|-----------|----------------|
| **pos** | terminal, register, kiosk, mobile_pos, self_checkout | merchant | NULL (root) |
| **peripheral** | card_reader, barcode_scanner, receipt_printer, cash_drawer, scale, label_printer, pin_pad | merchant | pos device |
| **customer** | phone_nfc, phone_wallet, browser, wearable | customer | NULL (transient) |
| **iot** | weight_scale, temperature_sensor, door_sensor, security_camera, people_counter | merchant | NULL or infrastructure |
| **infrastructure** | router, access_point, gateway, hub | merchant | NULL |
| **virtual** | ecommerce_session, api_client, mobile_app, webhook_source | varies | NULL |

### The Device Graph — Thing of Thing

```
Location: Downtown Café
└── Station 1 (pos/register, merchant)
    ├── Square Terminal T2 (pos/terminal, merchant)
    │   ├── Built-in Card Reader (peripheral/card_reader, merchant)
    │   ├── Built-in Receipt Printer (peripheral/receipt_printer, merchant)
    │   └── Built-in Barcode Scanner (peripheral/barcode_scanner, merchant)
    ├── Cash Drawer (peripheral/cash_drawer, merchant)
    └── Digital Scale (iot/weight_scale, merchant)
└── Station 2 (pos/register, merchant)
    ├── iPad POS (pos/mobile_pos, merchant)
    └── Square Reader (peripheral/card_reader, merchant)
└── [Transient — no parent]
    ├── Customer iPhone (customer/phone_nfc, customer) — tapped to pay at Station 1
    ├── Customer Android (customer/phone_wallet, customer) — used Google Pay at Station 2
    └── DoorDash Tablet (pos/mobile_pos, third_party) — delivery order processing
```

Every node in this graph is a row in `devices`. The `parent_device_id` creates the hierarchy. Customer devices are `ownership = 'customer'`, `status = 'transient'` — they appear when a tap event happens and we capture their fingerprint, then they're not seen again until the next visit.

### Transaction-Device Linkage

A single transaction can touch multiple devices. The terminal processed it, the card reader captured the payment, the customer's phone provided the NFC tap. This is a many-to-many relationship:

```sql
CREATE TABLE canary_sales.transaction_devices (
    id                  UUID            NOT NULL DEFAULT gen_random_uuid(),
    merchant_id         UUID            NOT NULL,
    transaction_id      UUID            NOT NULL,
    device_id           UUID            NOT NULL,
    interaction_type    TEXT            NOT NULL,       -- what role this device played
    interaction_at      TIMESTAMPTZ     NOT NULL DEFAULT now(),
    raw_metadata        JSONB           NOT NULL DEFAULT '{}',  -- device-specific payload for this interaction
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),

    CONSTRAINT pk_txn_devices PRIMARY KEY (id),
    CONSTRAINT fk_td_merchant FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id) ON DELETE CASCADE,
    CONSTRAINT fk_td_transaction FOREIGN KEY (transaction_id) REFERENCES canary_sales.transactions(id),
    CONSTRAINT fk_td_device FOREIGN KEY (device_id) REFERENCES canary_app.devices(id),
    CONSTRAINT chk_td_interaction_type CHECK (interaction_type IN (
        'processed',        -- POS terminal that processed the transaction
        'payment_capture',  -- Card reader / NFC reader that captured payment
        'customer_tap',     -- Customer device that initiated contactless payment
        'scanned',          -- Barcode scanner that scanned items
        'printed',          -- Receipt printer that printed the receipt
        'drawer_opened',    -- Cash drawer that opened
        'weighed',          -- Scale that measured product weight
        'observed',         -- Security camera that recorded the transaction
        'delivered',        -- Delivery device that handled fulfillment
        'authorized',       -- Device that provided manager authorization
        'unknown'           -- Source didn't specify interaction type
    ))
);

-- "What devices touched this transaction?"
CREATE INDEX idx_td_transaction
    ON transaction_devices (merchant_id, transaction_id);

-- "What transactions did this device participate in?"
CREATE INDEX idx_td_device
    ON transaction_devices (merchant_id, device_id, interaction_at DESC);

-- "All payment captures" (for card reader analytics)
CREATE INDEX idx_td_interaction
    ON transaction_devices (merchant_id, interaction_type, interaction_at DESC);

-- NEVER DROP DATA — raw device interaction payloads
CREATE INDEX idx_td_raw_metadata
    ON transaction_devices USING GIN (raw_metadata);

-- RLS
ALTER TABLE transaction_devices ENABLE ROW LEVEL SECURITY;
ALTER TABLE transaction_devices FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON transaction_devices
    USING (merchant_id = current_setting('app.current_merchant_id')::uuid);
```

### The "Never Drop Data" Contract

Every device interaction produces metadata. Some of it is immediately useful (device_id, interaction_type, timestamp). Most of it isn't — yet. The `raw_metadata` JSONB column on both `devices` and `transaction_devices` captures everything the source sends, unparsed.

**The promotion pipeline:**

```
1. RAW INGEST:    raw_metadata JSONB ← everything the source sends, verbatim
2. PARSE NOW:     attributes JSONB ← fields we know are useful today (extracted by parser)
3. PROMOTE LATER: ALTER TABLE ADD COLUMN ← when a JSONB field proves valuable, promote to column
4. NEVER:         DROP, DELETE, or overwrite raw_metadata — it's the audit trail
```

Example — today we don't parse a card reader's NFC antenna model from Square's device components payload. But if a vulnerability is discovered in a specific NFC chipset next year, we can query `raw_metadata @> '{"components": [{"type": "nfc", "model": "PN532"}]}'` across every device interaction we've ever recorded. The data was always there. We just didn't need it yet.

### Square Sync Mapping

| Square Field | Canary Column | Notes |
|-------------|---------------|-------|
| `device.id` | `external_identities.external_id` | POS-native device ID |
| `device.attributes.type` | `device_type` | TERMINAL → 'terminal' |
| `device.attributes.manufacturer` | `manufacturer` | "Square" |
| `device.attributes.model` | `model` | "T2" etc. |
| `device.attributes.manufacturers_id` | `serial_number` | Physical serial |
| `device.attributes.version` | `firmware_version` | Software version |
| `device.location_id` | `location_id` (via external_identities) | Assigned location |
| `device.name` | `display_name` | Merchant-assigned name |
| `device.status` | `status` | Map Square status → Canary status |
| `device.attributes.components` | `raw_metadata.components` | Full component array — card readers, batteries, network interfaces. Parse capabilities[] from this. |
| Payment `source_type` | transaction_devices `interaction_type` | Maps to 'customer_tap' for NFC, 'payment_capture' for chip/swipe |
| Payment `device_details` | transaction_devices `raw_metadata` | Full payment device context — NEVER DROP |

### Chirp Integration

| Rule ID | Rule | Signal | Severity |
|---------|------|--------|----------|
| C-901 | `GHOST_DEVICE` | Transaction references a device_id not in the device registry | HIGH — always fires |
| C-902 | `DEVICE_LOCATION_MISMATCH` | Transaction location ≠ device's assigned location | HIGH |
| C-903 | `OFFLINE_BATCH_SUBMISSION` | Device submits >10 transactions after >4 hours offline | MEDIUM |
| C-904 | `DEVICE_SWAP_MID_SHIFT` | Employee's transactions switch devices within same shift | LOW — informational |
| C-905 | `UNAUTHORIZED_DEVICE_PAIRING` | New device paired without matching an approved hardware request | MEDIUM |
| C-906 | `STALE_FIRMWARE` | Device firmware version older than threshold (PCI risk) | LOW — compliance |
| C-907 | `ORPHAN_PERIPHERAL` | Peripheral device (reader, scanner) not linked to any POS parent | MEDIUM — potential rogue device |
| C-908 | `CUSTOMER_DEVICE_VELOCITY` | Same customer device fingerprint appears at >3 locations in 24h | LOW — potential card testing |
| C-909 | `DEVICE_CAPABILITY_DOWNGRADE` | Device loses a capability between syncs (e.g., chip reader disabled) | MEDIUM — potential tampering |

### Presentation Layer Vocabulary

| Token Key | Default (en-US) | Coffee Shop | Cannabis |
|-----------|----------------|-------------|----------|
| `device.label.singular` | Device | Register | Station |
| `device.label.plural` | Devices | Registers | Stations |
| `device.class.pos` | POS Terminal | Register | Checkout Station |
| `device.class.peripheral` | Peripheral | Accessory | Component |
| `device.class.customer` | Customer Device | Customer Phone | Patient Device |
| `device.class.iot` | Sensor | Sensor | Compliance Sensor |
| `device.status.compromised` | Compromised | Flagged | Quarantined |
| `device.alert.ghost_device` | Unregistered Device | Unknown Register | Unlicensed Station |

Same three-part isolation: the device entity is merchant-scoped (RLS), its evidence is hash-chained, and its label adapts to the merchant's vocabulary. The device graph is the physical world's representation of the same isolation principle.

---

## 9. Summary: New Table Inventory

| Table | Database | Amendment | Purpose |
|-------|----------|-----------|---------|
| `external_identities` | canary_app | 1 | POS-agnostic entity ID mapping |
| `product_identifiers` | canary_app | 2 | Multi-barcode registry (UPC, EAN, ISBN, SKU, PLU) |
| `product_compositions` | canary_app | 3 | Bundle/kit/combo component mapping |
| `categories` | canary_app | 4 | Hierarchical product categorization |
| `location_product_authorizations` | canary_app | 7 | Location-level authorized product catalog |
| `devices` | canary_app | 8 | Device graph — any device that touches a transaction (POS, peripheral, customer, IoT, infrastructure, virtual) |
| `transaction_devices` | canary_sales | 8 | Many-to-many: which devices participated in which transaction, with interaction type and raw metadata |

### Columns Added to Existing Tables

| Table | Column | Amendment |
|-------|--------|-----------|
| `products` | `is_composite`, `composite_type`, `category_id`, `attributes` | 3, 4, 6 |
| `employees` | `attributes` | 6 |
| `locations` | `attributes` | 6 |
| `customers` | `attributes` | 6 |
| `transactions` | `device_entity_id` (FK → devices) | 8 |

### Columns Removed from Existing Tables

| Table | Column | Replacement |
|-------|--------|-------------|
| `products` | `square_item_id` | `external_identities` |
| `employees` | `square_employee_id` | `external_identities` |
| `locations` | `square_location_id` | `external_identities` |
| `customers` | `square_customer_id` | `external_identities` |

### Columns Renamed

| Table | Old | New | Reason |
|-------|-----|-----|--------|
| `products` | `product_name` | `display_name` | Canonical, POS-agnostic |
| `employees` | `employee_name` | `display_name` | Same |
| `locations` | `location_name` | `display_name` | Same |
| `transactions` | `square_product` | `source_channel` | Vendor-neutral channel identifier |

---

## 9. Presentation Layer Contract

Per ADR-PLA-001, every API response returns both token keys and resolved display strings. With this amendment, the entity APIs gain full vocabulary integration:

```json
{
    "entity": {
        "id": "uuid-...",
        "display_name": "Jane Smith",
        "entity_type": {
            "key": "employee.label.singular",
            "display": "Barista"
        },
        "identifiers": [
            {"type": "primary", "source": "square", "value": "TMjKx9Z..."},
            {"type": "SKU", "source": "manual", "value": "EMP-0042"}
        ],
        "attributes": {}
    },
    "locale": "en-US",
    "vocabulary_active": true
}
```

The presentation layer never sees "square." The data layer never hardcodes "Barista." Each layer does its job. The isolation principle holds.

---

## 10. Relationship to Existing Work

| Document | Relationship |
|----------|-------------|
| **CRDM v1.0** | This amendment extends, not replaces. v1.0 remains authoritative for transaction tables, Chirp rules, and design patterns. |
| **ADR-PLA-001** | This amendment implements the data-layer counterpart of the presentation-layer architecture. |
| **B-068-D Vocabulary Schema** | Vocabulary resolution now applies to entity API responses, not just screen labels. Token registry may need expansion. |
| **B-068-B Token Registry** | 32 vocabulary-overridable tokens already cover entity labels (employee, location, etc.). No registry changes needed for this amendment. |
| **GRO-20 Alignment Audit** | Multi-identifier and bundle gaps identified in GRO-20 are resolved by Amendments 2 and 3. |
| **GRO-18 Multi-Tenant Options** | RLS policies on all new tables follow the same Pattern 1 (shared schema + RLS) recommended in GRO-18. |
| **Multi-POS Translation Layer** | Parser interface updated: parsers write to `external_identities` instead of `square_*_id` columns. |

---

## 11. Open Questions for Tom

1. **Migration order:** Should we migrate `external_identities` first (unblocks all entity tables), or do it table-by-table?
2. **Products.UPC and Products.SKU columns:** Remove entirely (replaced by `product_identifiers`), or keep as denormalized hot-path copies with `product_identifiers` as the authoritative source?
3. **Category hierarchy sync frequency:** Real-time webhook or daily batch? Square category changes are infrequent.
4. **`attributes` JSONB schema validation:** Enforce per-source JSON Schema in the parser, or leave freeform with GIN index?
5. **`hierarchy_path` maintenance:** Trigger-based (auto-recompute on parent change) or application-layer (recompute on sync)?
6. **Authorization matrix default behavior:** Default-authorized (sparse — only store exceptions) or default-empty (merchants must explicitly authorize products per location)? Sparse is recommended for SMB — less setup friction — but cannabis/franchise verticals may need default-empty for compliance.
7. **C-801 enforcement vs. detection:** Should `UNAUTHORIZED_PRODUCT_SALE` be detection-only (alert after the fact) or should the API gateway block the transaction pre-insert? Detection-only is simpler and aligns with "we don't add to the stress" — but regulated verticals may need pre-insert blocking.
8. **Authorization token registry expansion:** Amendment 7 introduces 4+ new vocabulary tokens (`authorization.status.*`, `authorization.alert.*`). Should these be added to the B-068-B token registry now, or deferred to Sprint 8+ with the authorization UI?

---

*ALX | CRDM v1.1 Amendment | March 2, 2026*
*"No vendor name in the database. No vendor name in the API response. No vendor name in the UI. The POS is an input source, not an identity."*
