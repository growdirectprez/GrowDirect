# Chunk 6 — Pricing + Financial Domain (Schemas `p`, `f`)

**ARTS anchor**: ARTS Pricing (PriceList, Promotion, Tax) + ARTS Financial (GLAccount, Tender, SupplierInvoice).
**Modules**: P (Pricing), F (Finance).
**Entities**: 10 (item_prices · promotions · promotion_rules · tax_classes · tax_rates · tender_types · gl_accounts · supplier_invoices · supplier_invoice_lines · payments).
**Folded from sources**: GSLM Price 6 + GSLM Finance 13 + TOM F-Prefix 5 + TOM C010 (price details) → 10 SMB-2030 canonical.

## Domain narrative

Pricing and Financial sit adjacent because they share the tax model (taxes are configured in pricing, computed at transaction, posted to financial). Per F-Prefix subagent finding: "Tax architecture is multi-model from day one — F004/F014 carry parallel sub-groups for VAT (rate-table per code, multi-rate per invoice) and Sales Tax, with v1.0 change record explicitly anticipating country-by-country tax-engine variance." We honor that — tax model supports VAT-style (rate by class) and Sales-Tax-style (rate by location × class) without schema split.

The F-Prefix pattern subagent flagged is critical: **AP three-way match is the implicit governing pattern stitching F001/F015 → F013 → (receipt) → F004 through ReIM into OFi**. This means every supplier invoice must reconcile against PO + receipt — Canary Go enforces this at the schema level (FKs from `f.supplier_invoices.related_po_id` and `f.supplier_invoices.related_receipt_document_id`).

For SMB-2030: most merchants do simple pricing (one price per item, occasional promotion), simple tax (one or two tax classes), simple AP (small vendor list, monthly invoice cadence). Schema supports the simple case (most fields nullable, default tender_types library) with extension capacity for complex merchants without reshape.

---

## p.item_prices

**ARTS reference**: ARTS PriceList / ItemPrice.
**Module**: P.

### Schema

```sql
CREATE TABLE p.item_prices (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id           uuid NOT NULL REFERENCES app.tenants(id),
  item_id             uuid NOT NULL REFERENCES m.items(id) ON DELETE CASCADE,
  location_id         uuid REFERENCES l.locations(id),               -- NULL = default for all locations
  zone_id             uuid REFERENCES l.location_zones(id),          -- NULL = location-wide
  channel             text DEFAULT 'all',                            -- all | brick | web | bopis | marketplace
  price_type          text NOT NULL DEFAULT 'regular',               -- regular | clearance | member | wholesale | cost_plus
  amount              numeric(14,4) NOT NULL,
  currency            text NOT NULL DEFAULT 'USD',
  uom                 text NOT NULL DEFAULT 'EA',                    -- price per EA, LB, KG, etc.
  effective_start     timestamptz NOT NULL DEFAULT now(),
  effective_end       timestamptz,                                    -- NULL = open-ended
  source_promotion_id uuid REFERENCES p.promotions(id),               -- if price came from a promotion
  attributes          jsonb NOT NULL DEFAULT '{}',
  status              text NOT NULL DEFAULT 'active',
  created_at          timestamptz NOT NULL DEFAULT now(),
  updated_at          timestamptz NOT NULL DEFAULT now(),
  -- A given item × location × zone × channel × price_type can only have ONE active price at any moment
  EXCLUDE USING gist (
    tenant_id WITH =, item_id WITH =,
    COALESCE(location_id, '00000000-0000-0000-0000-000000000000'::uuid) WITH =,
    COALESCE(zone_id, '00000000-0000-0000-0000-000000000000'::uuid) WITH =,
    channel WITH =, price_type WITH =,
    tstzrange(effective_start, effective_end, '[)') WITH &&
  ) WHERE (status = 'active')
);

CREATE INDEX idx_iprice_tenant ON p.item_prices(tenant_id);
CREATE INDEX idx_iprice_item ON p.item_prices(item_id);
CREATE INDEX idx_iprice_location ON p.item_prices(location_id);
CREATE INDEX idx_iprice_active_now ON p.item_prices(item_id, location_id, channel) WHERE status = 'active' AND (effective_end IS NULL OR effective_end > now());
```

### Operational lifecycle

**Producers**:
- `mcp.pricing.item-price.set` — manual or system price change
- `mcp.pricing.item-price.from-promotion` — promotion start triggers price override
- `mcp.pricing.item-price.expire` — promotion end / clearance complete
- `mcp.pricing.item-price.import-from-pos` — sync from POS-native price (Counterpoint PRICE, Square pricing)

**Consumers**:
- `mcp.transaction.price.resolve` — at every POS scan / web add-to-cart, p99 < 30ms
- `mcp.store-line.price-push` — PLU feed (TOM C023+C027+C045 PLU pattern)
- `mcp.metrics.price-elasticity` — analytics

**SLA at producer**: real-time, p95 < 200ms. EXCLUDE constraint enforces no overlapping active prices for same scope.
**SLA at consumers**: lookup p99 < 30ms (every scan).

### Provenance

- **ARTS reference**: PriceList (location-scoped) + ItemPrice (item-scoped); we unify in single table with nullable location/zone
- **GSLM Price domain**: 6 entities — promotions get separate tables below; basic price collapses here
- **TOM junctions**: C010US (Price details RMS→IDS — RegularPriceChange + ClearPriceChange)
- **Justification**: `EXCLUDE USING gist` with `tstzrange` enforces no two active prices for same scope at same time — Postgres-native temporal exclusion. `price_type` discriminator (regular | clearance | member | wholesale) replaces ARTS's separate price-list-per-type pattern. SMB without per-location pricing simply has all rows with `location_id IS NULL`.

---

## p.promotions

**ARTS reference**: ARTS Promotion (header).
**Module**: P.

### Schema

```sql
CREATE TABLE p.promotions (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id           uuid NOT NULL REFERENCES app.tenants(id),
  promotion_code      text NOT NULL,
  name                text NOT NULL,
  description         text,
  promotion_type      text NOT NULL DEFAULT 'percent_off',           -- percent_off | amount_off | bogo | x_for_y | tier_threshold | bundle | fixed_price | loyalty_member_price
  scope_type          text NOT NULL DEFAULT 'item',                  -- item | category | brand | merchandise_total | tender | customer_segment
  effective_start     timestamptz NOT NULL,
  effective_end       timestamptz,
  active_days         int[] DEFAULT '{1,2,3,4,5,6,7}',               -- ISO day-of-week (1=Monday)
  active_hours        jsonb DEFAULT '{}',                            -- {"start": "08:00", "end": "20:00"}
  active_locations    uuid[],                                        -- NULL = all; array of l.locations.id
  active_channels     text[] DEFAULT '{}',                           -- {} = all
  customer_segments   text[],                                        -- target loyalty tiers / segments
  stackable           boolean NOT NULL DEFAULT false,                -- can stack with other promotions?
  exclusive_with      uuid[],                                        -- IDs of promotions that block this one
  max_uses_total      int,                                           -- across all customers
  max_uses_per_customer int,
  current_uses        int NOT NULL DEFAULT 0,
  attributes          jsonb NOT NULL DEFAULT '{}',
  status              text NOT NULL DEFAULT 'draft',                 -- draft | scheduled | active | paused | expired | cancelled
  created_at          timestamptz NOT NULL DEFAULT now(),
  updated_at          timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, promotion_code)
);

CREATE INDEX idx_promo_tenant ON p.promotions(tenant_id);
CREATE INDEX idx_promo_active ON p.promotions(effective_start, effective_end) WHERE status = 'active';
CREATE INDEX idx_promo_status ON p.promotions(status) WHERE status NOT IN ('expired', 'cancelled');
```

### Operational lifecycle

**Producers**: `mcp.promotion.create`, `mcp.promotion.activate`, `mcp.promotion.pause`, `mcp.promotion.expire-on-schedule`
**Consumers**: `mcp.transaction.promotion.evaluate-applicable` (at every POS line add), `mcp.metrics.promotion-effectiveness`, `mcp.store-line.promotion-push` (C010 promotion feed)

### Provenance

- **ARTS reference**: Promotion
- **GSLM Promotion**: 5 entities (Promotions + PromotionComponents + PromotionComponentDetails + PromotionThresholds + ThresholdIntervals) — folded into promotion + promotion_rules
- **TOM**: C010US (price details with promotion components), C010TR (Promotions RMS→GFO)
- **Justification**: `active_days` / `active_hours` / `active_locations` / `active_channels` collapse what TOM modeled in 4 separate tables. Postgres array types handle multi-value scoping without join tables for queries like "find promotions active at this location on this channel today."

---

## p.promotion_rules

**ARTS reference**: ARTS Promotion Component / Rule.
**Module**: P.

### Schema

```sql
CREATE TABLE p.promotion_rules (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id           uuid NOT NULL REFERENCES app.tenants(id),
  promotion_id        uuid NOT NULL REFERENCES p.promotions(id) ON DELETE CASCADE,
  rule_order          int NOT NULL DEFAULT 1,                        -- sequence (some rules check before others)
  trigger_type        text NOT NULL,                                  -- buy_quantity | spend_amount | own_loyalty_card | scan_coupon | match_basket
  trigger_qualifier   jsonb NOT NULL DEFAULT '{}',                    -- {item_ids: [], category_ids: [], min_quantity: 2, min_amount: 25.00}
  benefit_type        text NOT NULL,                                  -- amount_off | percent_off | fixed_price | free_item | tier_unlock
  benefit_qualifier   jsonb NOT NULL DEFAULT '{}',                    -- {amount: 5.00, percent: 0.20, fixed_price: 10.00, free_item_ids: []}
  created_at          timestamptz NOT NULL DEFAULT now(),
  updated_at          timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_prules_tenant ON p.promotion_rules(tenant_id);
CREATE INDEX idx_prules_promo ON p.promotion_rules(promotion_id);
```

### Operational lifecycle

**Producers**: `mcp.promotion-rule.add`, `mcp.promotion-rule.update`
**Consumers**: `mcp.transaction.promotion.evaluate` — runs at line-add and basket-total to check trigger satisfaction

### Provenance

- **ARTS reference**: PromotionComponent + PromotionComponentDetail
- **GSLM**: PromotionComponents + PromotionComponentDetails + PromotionThresholds + ThresholdIntervals (4 entities → 1 with trigger/benefit JSONB)
- **Justification**: Promotion engines need flexibility — every BOGO/X-for-Y/tier variation has different trigger and benefit semantics. JSONB qualifiers let the rule engine evaluate without schema migration for every new promo type. Rule_order supports sequenced evaluation (e.g., apply customer-tier discount THEN basket-total threshold).

---

## p.tax_classes

**ARTS reference**: ARTS Tax Classification.
**Module**: P (configured) / F (consumed).

### Schema

```sql
CREATE TABLE p.tax_classes (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       uuid NOT NULL REFERENCES app.tenants(id),
  code            text NOT NULL,                                  -- "STD", "FOOD", "RX", "ALCOHOL", "SERVICE", "EXEMPT"
  name            text NOT NULL,
  description     text,
  is_default      boolean NOT NULL DEFAULT false,
  attributes      jsonb NOT NULL DEFAULT '{}',
  status          text NOT NULL DEFAULT 'active',
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, code),
  CONSTRAINT one_default_class EXCLUDE (tenant_id WITH =) WHERE (is_default = true AND status = 'active')
);

CREATE INDEX idx_tclasses_tenant ON p.tax_classes(tenant_id);
```

### Operational lifecycle

**Producers**: `mcp.tax-class.upsert`
**Consumers**: `mcp.master.item.assign-tax-class` (referenced by `m.items.tax_class`), `mcp.tax.compute`

### Provenance

- **ARTS reference**: Tax Classification
- **GSLM**: `Taxes` (1 table — minimal in SQL impl; richer in S0 MDM Finance domain)
- **Justification**: Tax class is the *category* (food, alcohol, standard); rate is per-location-per-class (next table). Single default per tenant via EXCLUDE constraint.

---

## p.tax_rates

**ARTS reference**: ARTS Tax Rate (location × class).
**Module**: P / F.

### Schema

```sql
CREATE TABLE p.tax_rates (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       uuid NOT NULL REFERENCES app.tenants(id),
  tax_class_id    uuid NOT NULL REFERENCES p.tax_classes(id),
  location_id     uuid REFERENCES l.locations(id),                  -- NULL = applies tenant-wide (default)
  jurisdiction    text,                                              -- "CA", "CA-LA-County", "EU-DE", "EU-DE-Berlin" — for tax-engine integration
  rate_type       text NOT NULL DEFAULT 'percentage',                -- percentage | flat_amount | tiered
  rate            numeric(8,6) NOT NULL,                             -- 0.0825 for 8.25%; for tiered, JSONB schedule in attributes
  effective_start date NOT NULL DEFAULT CURRENT_DATE,
  effective_end   date,
  attributes      jsonb NOT NULL DEFAULT '{}',                       -- VAT details, GST/HST distinction, multi-rate schedule
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, tax_class_id, COALESCE(location_id, '00000000-0000-0000-0000-000000000000'::uuid), effective_start)
);

CREATE INDEX idx_trates_tenant ON p.tax_rates(tenant_id);
CREATE INDEX idx_trates_class ON p.tax_rates(tax_class_id);
CREATE INDEX idx_trates_location ON p.tax_rates(location_id);
CREATE INDEX idx_trates_active ON p.tax_rates(tax_class_id, location_id) WHERE effective_end IS NULL OR effective_end > CURRENT_DATE;
```

### Operational lifecycle

**Producers**: `mcp.tax-rate.set`, `mcp.tax-rate.from-tax-engine-sync` (Avalara, TaxJar integration)
**Consumers**: `mcp.tax.compute` (at every transaction), `mcp.financial.tax-liability.aggregate`

### Provenance

- **ARTS reference**: Tax Rate
- **GSLM**: `Taxes` + `ItemTaxesInSalesOutlets` (folded)
- **TOM**: F004/F014 carry tax sub-groups (multi-rate per invoice via VAT) — schema supports this via tiered rate_type + JSONB schedule
- **Justification**: Per F-Prefix subagent finding, multi-model tax (VAT vs Sales Tax) was anticipated from day one. JSONB schedule supports complex rate structures (tiered, brackets, surcharges) without column proliferation. NULL location_id for tenant-wide default; specific location_id for jurisdictional overrides.

---

## f.tender_types

**ARTS reference**: ARTS Tender (master).
**Module**: F.

### Schema

```sql
CREATE TABLE f.tender_types (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       uuid NOT NULL REFERENCES app.tenants(id),
  code            text NOT NULL,                                  -- CASH, VISA, MC, AMEX, EBT, GIFT, STORE_CREDIT, CHECK
  name            text NOT NULL,
  tender_class    text NOT NULL,                                  -- cash | credit_card | debit_card | gift_card | store_credit | check | electronic_check | ebt_snap | wic | crypto
  is_active       boolean NOT NULL DEFAULT true,
  is_change_giving boolean NOT NULL DEFAULT false,                 -- can give change as this tender (cash yes; gift card no)
  is_refundable   boolean NOT NULL DEFAULT true,
  open_drawer     boolean NOT NULL DEFAULT false,                  -- triggers cash drawer (cash, check)
  gl_account_id   uuid REFERENCES f.gl_accounts(id),               -- accounting destination
  rounding_rule   text,                                             -- nearest_cent | nickel | etc. (cash-rounding for currencies that need it)
  attributes      jsonb NOT NULL DEFAULT '{}',
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, code)
);

CREATE INDEX idx_tender_tenant ON f.tender_types(tenant_id);
CREATE INDEX idx_tender_class ON f.tender_types(tender_class);
```

### Operational lifecycle

**Producers**: `mcp.tender-type.upsert`
**Consumers**: `mcp.transaction.tender.lookup` (at every payment), `mcp.cash-management.drawer-open-trigger`, `mcp.financial.tender-aggregate.by-class`

### Provenance

- **ARTS reference**: Tender (master enumeration)
- **CRDM operational**: `CRDM_Tender` is the operational tender event in T schema; this is the master enumeration
- **Justification**: Tender type is master data (a small fixed set per merchant). The actual payment events live in `t.transaction_tenders`. GL account FK enables direct posting to accounting on each tender.

---

## f.gl_accounts

**ARTS reference**: ARTS GLAccount.
**Module**: F.

### Schema

```sql
CREATE TABLE f.gl_accounts (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       uuid NOT NULL REFERENCES app.tenants(id),
  parent_id       uuid REFERENCES f.gl_accounts(id),
  code            text NOT NULL,                                  -- merchant chart of accounts code
  name            text NOT NULL,
  account_type    text NOT NULL,                                  -- asset | liability | equity | revenue | expense | contra
  account_subtype text,                                           -- current_asset | inventory | accounts_payable | sales | cogs | etc.
  is_postable     boolean NOT NULL DEFAULT true,                  -- false for parent rollups
  currency        text NOT NULL DEFAULT 'USD',
  attributes      jsonb NOT NULL DEFAULT '{}',
  status          text NOT NULL DEFAULT 'active',
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, code)
);

CREATE INDEX idx_gl_tenant ON f.gl_accounts(tenant_id);
CREATE INDEX idx_gl_parent ON f.gl_accounts(parent_id);
CREATE INDEX idx_gl_type ON f.gl_accounts(account_type);
```

### Operational lifecycle

**Producers**: `mcp.gl-account.upsert` (manual or sync from accounting system)
**Consumers**: `mcp.financial.tender-post`, `mcp.financial.invoice-post`, `mcp.financial.cogs-post`

### Provenance

- **ARTS reference**: GLAccount
- **TOM**: F-Prefix uses GL coding throughout — F004 ReIM posts into OFi GL accounts
- **Justification**: Standard chart of accounts with parent FK for hierarchy (rollups). Per F-Prefix subagent finding, "GL coding is downstream — F-prefix interfaces are operational pipes; GL account assignment happens inside OFi after ReIM posting." We model GL accounts as canonical because Canary Go integrates with QuickBooks / Xero / NetSuite — needs to know merchant's account structure.

---

## f.supplier_invoices

**ARTS reference**: ARTS SupplierInvoice (AP).
**Module**: F.

### Schema

```sql
CREATE TABLE f.supplier_invoices (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id           uuid NOT NULL REFERENCES app.tenants(id),
  invoice_number      text NOT NULL,                              -- vendor's invoice number
  vendor_id           uuid NOT NULL REFERENCES m.vendors(id),
  invoice_date        date NOT NULL,
  due_date            date,
  related_po_id       uuid REFERENCES o.purchase_orders(id),      -- three-way match: invoice ↔ PO
  related_receipt_document_id uuid REFERENCES i.inventory_documents(id),  -- invoice ↔ receipt (third leg)
  status              text NOT NULL DEFAULT 'received',           -- received | matched | discrepancy | approved | paid | disputed | cancelled
  subtotal            numeric(14,4) NOT NULL,
  tax_total           numeric(14,4) NOT NULL DEFAULT 0,
  shipping_total      numeric(14,4) NOT NULL DEFAULT 0,
  discount_total      numeric(14,4) NOT NULL DEFAULT 0,
  grand_total         numeric(14,4) NOT NULL,
  currency            text NOT NULL DEFAULT 'USD',
  match_status        text NOT NULL DEFAULT 'pending',            -- pending | matched | partial_match | mismatch | manual_override
  match_variance      numeric(14,4),                              -- variance vs PO + receipt
  approval_user_id    uuid REFERENCES app.users(id),
  approved_at         timestamptz,
  attributes          jsonb NOT NULL DEFAULT '{}',                -- vendor_credit_note_ref, payment_terms_override, original_doc_url
  created_at          timestamptz NOT NULL DEFAULT now(),
  updated_at          timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, vendor_id, invoice_number)
);

CREATE INDEX idx_sinv_tenant ON f.supplier_invoices(tenant_id);
CREATE INDEX idx_sinv_vendor ON f.supplier_invoices(vendor_id);
CREATE INDEX idx_sinv_po ON f.supplier_invoices(related_po_id);
CREATE INDEX idx_sinv_receipt ON f.supplier_invoices(related_receipt_document_id);
CREATE INDEX idx_sinv_status ON f.supplier_invoices(status) WHERE status NOT IN ('paid', 'cancelled');
CREATE INDEX idx_sinv_due ON f.supplier_invoices(due_date) WHERE status = 'approved';
```

### Operational lifecycle

**Producers**: `mcp.supplier-invoice.from-vendor` (F004 / F014 ReIM pattern), `mcp.supplier-invoice.three-way-match` (auto-match against PO + receipt)
**Consumers**: `mcp.payment.create-from-invoice`, `mcp.financial.gl-post.invoice`, `mcp.metrics.ap-aging`

### Provenance

- **ARTS reference**: SupplierInvoice (AP)
- **TOM**: F004 (Supplier Invoice TIMS→ReIM), F014 (Tesco Invoice from ReIM to TIMS)
- **Justification**: FK to both PO and receipt enables three-way match at schema level. `match_status` discriminator captures the matching outcome explicitly. Per F-Prefix subagent finding, "three-way matching is the implicit governing pattern" — Canary Go makes it explicit.

---

## f.supplier_invoice_lines

**ARTS reference**: ARTS SupplierInvoiceLine.
**Module**: F.

### Schema

```sql
CREATE TABLE f.supplier_invoice_lines (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id           uuid NOT NULL REFERENCES app.tenants(id),
  invoice_id          uuid NOT NULL REFERENCES f.supplier_invoices(id) ON DELETE CASCADE,
  line_number         int NOT NULL,
  related_po_line_id  uuid REFERENCES o.purchase_order_lines(id),     -- three-way match at line level
  related_receipt_line_id uuid REFERENCES i.inventory_document_lines(id),
  item_id             uuid REFERENCES m.items(id),                    -- nullable for non-merchandise lines (freight, fees)
  description         text NOT NULL,
  quantity            numeric(14,4),
  unit_cost           numeric(14,4),
  line_total          numeric(14,4) NOT NULL,
  tax_amount          numeric(14,4) NOT NULL DEFAULT 0,
  gl_account_id       uuid REFERENCES f.gl_accounts(id),              -- override GL account for this line
  match_variance      numeric(14,4),                                  -- variance vs PO line / receipt line
  attributes          jsonb NOT NULL DEFAULT '{}',
  created_at          timestamptz NOT NULL DEFAULT now(),
  updated_at          timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, invoice_id, line_number)
);

CREATE INDEX idx_sinvline_tenant ON f.supplier_invoice_lines(tenant_id);
CREATE INDEX idx_sinvline_invoice ON f.supplier_invoice_lines(invoice_id);
CREATE INDEX idx_sinvline_po_line ON f.supplier_invoice_lines(related_po_line_id);
CREATE INDEX idx_sinvline_receipt_line ON f.supplier_invoice_lines(related_receipt_line_id);
```

### Operational lifecycle

**Producers**: `mcp.supplier-invoice-line.add`, `mcp.supplier-invoice-line.three-way-match-line`
**Consumers**: `mcp.financial.line-variance-report`, `mcp.financial.gl-post.line`

### Provenance

- **ARTS reference**: SupplierInvoiceLine
- **TOM**: F004/F014 invoice line records
- **Justification**: Line-level three-way match (vs PO line + receipt line) catches discrepancies at item granularity. Item FK nullable because some invoice lines are non-merchandise (freight, fees, adjustments).

---

## f.payments

**ARTS reference**: ARTS Payment (AP outbound).
**Module**: F.

### Schema

```sql
CREATE TABLE f.payments (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id           uuid NOT NULL REFERENCES app.tenants(id),
  payment_number      text NOT NULL,
  vendor_id           uuid NOT NULL REFERENCES m.vendors(id),
  payment_method      text NOT NULL,                              -- check | ach | wire | credit_card | virtual_card
  payment_date        date NOT NULL,
  amount              numeric(14,4) NOT NULL,
  currency            text NOT NULL DEFAULT 'USD',
  bank_account_id     uuid,                                       -- references app.bank_accounts in current Canary spec
  reference_number    text,                                       -- check #, wire ref, ACH trace
  status              text NOT NULL DEFAULT 'scheduled',          -- scheduled | issued | cleared | voided | bounced
  cleared_at          timestamptz,
  attributes          jsonb NOT NULL DEFAULT '{}',
  created_at          timestamptz NOT NULL DEFAULT now(),
  updated_at          timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, payment_number)
);

CREATE TABLE f.payment_invoice_applications (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id           uuid NOT NULL REFERENCES app.tenants(id),
  payment_id          uuid NOT NULL REFERENCES f.payments(id) ON DELETE CASCADE,
  invoice_id          uuid NOT NULL REFERENCES f.supplier_invoices(id),
  amount_applied      numeric(14,4) NOT NULL,
  created_at          timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_pay_tenant ON f.payments(tenant_id);
CREATE INDEX idx_pay_vendor ON f.payments(vendor_id);
CREATE INDEX idx_pay_status ON f.payments(status) WHERE status IN ('scheduled', 'issued');
CREATE INDEX idx_pay_invapp_payment ON f.payment_invoice_applications(payment_id);
CREATE INDEX idx_pay_invapp_invoice ON f.payment_invoice_applications(invoice_id);
```

### Operational lifecycle

**Producers**: `mcp.payment.schedule-from-invoice`, `mcp.payment.issue`, `mcp.payment.bank-clear`, `mcp.payment.void`
**Consumers**: `mcp.financial.gl-post.payment`, `mcp.metrics.cash-flow-projection`

### Provenance

- **ARTS reference**: Payment (AP)
- **TOM**: not modeled in F-Prefix corpus (Tesco's payment was downstream of OFi)
- **Justification**: Many-to-many payment-invoice via `payment_invoice_applications` supports multi-invoice payments (single check covers multiple invoices) and partial payments (one invoice paid across multiple cheques).

---

## Domain summary

**10 entities (+ 1 join), 2 schemas (p, f), 2 modules (P + F)**:
- `p.item_prices` (~16 cols, EXCLUDE temporal constraint) — multi-scope pricing
- `p.promotions` (~22 cols, array scoping) — header
- `p.promotion_rules` (~7 cols, JSONB triggers/benefits) — flexible rules
- `p.tax_classes` (~9 cols, EXCLUDE single-default) — tax category master
- `p.tax_rates` (~12 cols) — location × class effective-dated
- `f.tender_types` (~12 cols) — payment method master
- `f.gl_accounts` (~13 cols, recursive parent) — chart of accounts
- `f.supplier_invoices` (~22 cols, three-way match FKs) — AP invoice
- `f.supplier_invoice_lines` (~14 cols) — invoice detail with line-level match
- `f.payments` + `f.payment_invoice_applications` (~14 + 4 cols) — AP payment with many-to-many invoice application

**Folded from sources**:
- GSLM Price 6 entities → 5 (Promotion 5-table chain → 2 with JSONB triggers)
- GSLM Finance 13 entities (S0 MDM site) → 5 essentials (tender, GL, AP invoice + lines, payment)
- TOM F-Prefix 5 interfaces → 5 entities + ~10 MCP service junctions
- TOM C010US (price details) → `p.item_prices` + `p.promotions`

**MCP service junctions defined for this domain (~22)**:
- Pricing: item-price.set, item-price.from-promotion, item-price.expire, item-price.import-from-pos, promotion.{create,activate,pause,expire-on-schedule}, promotion-rule.{add,update}, tax-class.upsert, tax-rate.set, tax-rate.from-tax-engine-sync
- Financial: tender-type.upsert, gl-account.upsert, supplier-invoice.from-vendor, supplier-invoice.three-way-match, supplier-invoice-line.add, supplier-invoice-line.three-way-match-line, payment.{schedule-from-invoice, issue, bank-clear, void}
- Cross-cutting consumers: tax.compute, transaction.price.resolve, transaction.tender.lookup, financial.gl-post.{tender, invoice, cogs, payment}, metrics.{price-elasticity, ap-aging, cash-flow-projection}

## Status

- **Chunk 6 complete.** 10 ARTS-aligned Pricing + Financial entities. Three-way match instrumented. Multi-model tax supported.
- **Resume**: Chunk 7 — POSLog + Sales Audit (t schema). ARTS POSLog standard + CRDM operational POS as concrete reference. Target ~8-10 entities.
