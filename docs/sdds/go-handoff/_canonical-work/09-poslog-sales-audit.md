# Chunk 7 — POSLog + Sales Audit Domain (Schema `t`)

**ARTS anchor**: ARTS POSLog (XML standard for POS transaction logging) + ARTS Sales Audit.
**Module**: T (Transaction Pipeline).
**Entities**: 9 (transactions · transaction_line_items · transaction_tenders · transaction_discounts · cashier_actions · cash_drawer_events · shift_events · loyalty_events · gift_card_events).
**Folded from sources**: CRDM 25 POS entities → 9 SMB-2030 canonical via aggregation-table separation (FastFact-style aggregates → metrics schema, not here).

## Domain narrative

ARTS POSLog is the public XML standard for capturing point-of-sale transaction events. Every major POS vendor (NCR, Oracle Retail, IBM, etc.) implements POSLog for output; many implement it for input. SMB-2030 canonical T-schema honors the POSLog field structure but in relational form (Postgres rather than XML).

CRDM's 25 POS entities collapsed by separating **operational events** from **denormalized aggregations**:
- Operational events stay in `t` schema (this chunk) — every transaction, line, tender, discount captured atomically
- Pre-aggregated summaries (CRDM_FastFact ~110 columns, CRDM_ItemFastFact, scorecards) live in `metrics` schema as views/materialized views computed from `t` — they're NOT canonical entities

Returns are modeled as regular transactions with `transaction_type='return'` and `parent_transaction_id` FK to the original. Cancellations are status changes, not separate entities.

The T schema is the **single highest-volume schema** — every POS scan, every receipt, every tender. Indexing strategy is critical. Partitioning by `business_date` is recommended at scale (>10M transactions/year) but not required for SMB-2030 v1 (typical merchant: 50K-1M transactions/year per location).

This is the domain that connects to every other domain via FK: items (line items), customers (loyalty), employees (cashiers), locations (stores), tender_types (payment), promotions (discount source), inventory_movements (stock decrement on sale). Most queries against T are by (location, business_date) range — both are first-class columns.

---

## t.transactions

**ARTS reference**: ARTS POSLog Transaction header.
**Module**: T.

### Schema

```sql
CREATE TABLE t.transactions (
  id                      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id               uuid NOT NULL REFERENCES app.tenants(id),
  transaction_number      text NOT NULL,                              -- POS-native or system-assigned (uniqueness scope below)
  transaction_type        text NOT NULL DEFAULT 'sale',               -- sale | return | exchange | void | no_sale | layaway | quote | training
  parent_transaction_id   uuid REFERENCES t.transactions(id),         -- for returns / exchanges / voids
  location_id             uuid NOT NULL REFERENCES l.locations(id),
  pos_terminal_id         text,                                       -- POSNo (CRDM equivalent); links to n.devices when device schema exists
  cashier_employee_id     uuid REFERENCES e.employees(id),            -- the operator
  customer_id             uuid REFERENCES c.customers(id),            -- the customer (NULL for anonymous)
  loyalty_membership_id   uuid REFERENCES c.loyalty_memberships(id),
  business_date           date NOT NULL,                              -- the trading day (CRDM TradingDay equivalent)
  started_at              timestamptz NOT NULL,                       -- transaction start
  ended_at                timestamptz NOT NULL,                       -- transaction complete
  status                  text NOT NULL DEFAULT 'completed',          -- pending | completed | voided | suspended | recalled
  ticket_number           int,                                         -- TicketNo (per-day sequence)
  item_count              int NOT NULL DEFAULT 0,
  subtotal                numeric(14,4) NOT NULL DEFAULT 0,
  tax_total               numeric(14,4) NOT NULL DEFAULT 0,
  discount_total          numeric(14,4) NOT NULL DEFAULT 0,
  grand_total             numeric(14,4) NOT NULL DEFAULT 0,
  currency                text NOT NULL DEFAULT 'USD',
  channel                 text NOT NULL DEFAULT 'pos',                -- pos | self_checkout | mobile_pos | online | phone
  pos_software_version    text,                                       -- CodeVersion (CRDM equivalent)
  is_training_mode        boolean NOT NULL DEFAULT false,             -- TrainingModeFlg
  is_offline              boolean NOT NULL DEFAULT false,             -- POSOfflineFlg (transaction created offline, synced later)
  is_reentered            boolean NOT NULL DEFAULT false,             -- ReenteredTransactionFlg
  is_suspended            boolean NOT NULL DEFAULT false,
  void_reason             text,                                       -- if voided
  attributes              jsonb NOT NULL DEFAULT '{}',                -- gift receipt printed, VAT receipt, custom flags
  external_ids            jsonb DEFAULT '{}',                         -- {pos_native_id, square_payment_id, processor_ref}
  created_at              timestamptz NOT NULL DEFAULT now(),
  updated_at              timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, location_id, business_date, transaction_number)
);

CREATE INDEX idx_tx_tenant ON t.transactions(tenant_id);
CREATE INDEX idx_tx_location_date ON t.transactions(location_id, business_date);
CREATE INDEX idx_tx_cashier ON t.transactions(cashier_employee_id, business_date);
CREATE INDEX idx_tx_customer ON t.transactions(customer_id) WHERE customer_id IS NOT NULL;
CREATE INDEX idx_tx_loyalty ON t.transactions(loyalty_membership_id) WHERE loyalty_membership_id IS NOT NULL;
CREATE INDEX idx_tx_parent ON t.transactions(parent_transaction_id) WHERE parent_transaction_id IS NOT NULL;
CREATE INDEX idx_tx_started ON t.transactions(started_at);
CREATE INDEX idx_tx_status ON t.transactions(status) WHERE status != 'completed';
CREATE INDEX idx_tx_external_ids ON t.transactions USING gin(external_ids);
```

### Operational lifecycle

**Producers**:
- `mcp.transaction.start` — when first scan or transaction-open event
- `mcp.transaction.complete` — when payment cleared
- `mcp.transaction.void` — manager-authorized void (creates new void transaction with parent FK)
- `mcp.transaction.return-from-receipt` — return transaction created with parent FK to original
- `mcp.transaction.suspend-and-recall` — suspend / recall flow

**Consumers**:
- `mcp.inventory.movement.from-transaction` — generates inventory movements for sold items
- `mcp.financial.tender-aggregate.by-transaction` — for cash drawer reconciliation
- `mcp.loyalty.points-earn.from-transaction` — earn calculation
- `mcp.metrics.fact-transaction.from-tx` — feeds metrics schema fact tables (TOM J004 Sales TDS→UDD pattern)
- `mcp.q.detection.scan-transaction` — Chirp rules evaluate every transaction (Q module)
- `mcp.audit.transaction.export` — for sales audit reports

**SLA at producer**: real-time, p95 < 500ms (transaction commit includes all related lines/tenders atomically).
**SLA at consumers**: inventory movement < 1s, metrics fact rollup < 5s, Chirp detection < 30s.

### Provenance

- **ARTS reference**: POSLog Transaction header
- **CRDM folded**: `CRDM_Header` + portions of `CRDM_FastFact` (most FastFact columns are aggregations → metrics schema)
- **TOM**: not in TOM corpus (Tesco POS was outside TOM scope; TOM is back-office)
- **Canary current**: `sales.transactions` (4 cols detailed) — superseded; expanded to ARTS POSLog field set
- **Justification**: Single transactions table with `transaction_type` discriminator covers sale/return/exchange/void/no-sale/layaway/quote/training — CRDM's 5+ transaction-flag columns become a single discriminator. Parent FK enables full return/void traceability. `business_date` first-class column (not derived from `started_at`) handles trading-day semantics where the trading day spans midnight (CRDM had explicit TradingDay column for this reason).

---

## t.transaction_line_items

**ARTS reference**: ARTS POSLog SaleLineItem.
**Module**: T.

### Schema

```sql
CREATE TABLE t.transaction_line_items (
  id                      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id               uuid NOT NULL REFERENCES app.tenants(id),
  transaction_id          uuid NOT NULL REFERENCES t.transactions(id) ON DELETE CASCADE,
  line_number             int NOT NULL,
  item_id                 uuid REFERENCES m.items(id),                -- nullable for unknown items (sold-as-not-on-file)
  barcode_scanned         text,                                       -- the actual barcode (for not-on-file recovery)
  description             text NOT NULL,                              -- snapshot (item description at sale time)
  quantity                numeric(14,4) NOT NULL,
  unit_of_measure         text NOT NULL DEFAULT 'EA',
  unit_price              numeric(14,4) NOT NULL,                     -- price at sale (snapshot from p.item_prices)
  list_price              numeric(14,4),                              -- original price before discounts
  unit_discount           numeric(14,4) NOT NULL DEFAULT 0,
  unit_tax                numeric(14,4) NOT NULL DEFAULT 0,
  extended_price          numeric(14,4) GENERATED ALWAYS AS (quantity * (unit_price - unit_discount)) STORED,
  extended_tax            numeric(14,4) GENERATED ALWAYS AS (quantity * unit_tax) STORED,
  line_total              numeric(14,4) GENERATED ALWAYS AS ((quantity * (unit_price - unit_discount)) + (quantity * unit_tax)) STORED,
  cost_basis              numeric(14,4),                              -- weighted-avg cost at sale (for margin)
  margin                  numeric(14,4) GENERATED ALWAYS AS (((quantity * (unit_price - unit_discount)) - (quantity * COALESCE(cost_basis, 0)))) STORED,
  category_id             uuid REFERENCES m.product_categories(id),    -- snapshot for analytics (item may be re-categorized later)
  zone_id                 uuid REFERENCES l.location_zones(id),        -- where it was scanned (for shrink-by-zone)
  lot_id                  uuid REFERENCES i.inventory_lots(id),        -- if lot-tracked
  inventory_movement_id   uuid REFERENCES i.inventory_movements(id),   -- the resulting stock decrement
  is_void                 boolean NOT NULL DEFAULT false,              -- line voided within transaction
  void_reason             text,
  is_return               boolean NOT NULL DEFAULT false,              -- return line (negative quantity)
  return_reason           text,                                        -- DamagedReceived | NoLongerNeeded | Defective | etc.
  is_weighable            boolean NOT NULL DEFAULT false,
  is_food_stamp_eligible  boolean NOT NULL DEFAULT false,              -- copy of m.items value at sale time (for audit)
  attributes              jsonb NOT NULL DEFAULT '{}',                 -- {gift_wrap, customizations, age_verified_by_employee_id, scan_method}
  created_at              timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, transaction_id, line_number)
);

CREATE INDEX idx_lines_tenant ON t.transaction_line_items(tenant_id);
CREATE INDEX idx_lines_tx ON t.transaction_line_items(transaction_id);
CREATE INDEX idx_lines_item ON t.transaction_line_items(item_id);
CREATE INDEX idx_lines_category ON t.transaction_line_items(category_id);
CREATE INDEX idx_lines_zone ON t.transaction_line_items(zone_id);
CREATE INDEX idx_lines_returns ON t.transaction_line_items(transaction_id) WHERE is_return = true;
CREATE INDEX idx_lines_voids ON t.transaction_line_items(transaction_id) WHERE is_void = true;
CREATE INDEX idx_lines_unknown ON t.transaction_line_items(barcode_scanned) WHERE item_id IS NULL;
```

### Operational lifecycle

**Producers**: `mcp.transaction.line.add`, `mcp.transaction.line.void`, `mcp.transaction.line.return`
**Consumers**: `mcp.inventory.movement.from-line`, `mcp.metrics.fact-sale-line`, `mcp.q.detection.line-pattern` (shrink, sweethearting, scan-then-void)

### Provenance

- **ARTS reference**: POSLog SaleLineItem
- **CRDM folded**: `CRDM_Item` + portions of `CRDM_ItemFastFact`
- **Justification**: Generated columns (`extended_price`, `extended_tax`, `line_total`, `margin`) ensure consistency. `item_id` nullable + `barcode_scanned` populated for not-on-file lines (sold but unrecognized barcode — Q-module signal). Snapshots (description, category_id, is_food_stamp_eligible) preserve sale-time values for audit even when master data changes.

---

## t.transaction_tenders

**ARTS reference**: ARTS POSLog Tender.
**Module**: T.

### Schema

```sql
CREATE TABLE t.transaction_tenders (
  id                      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id               uuid NOT NULL REFERENCES app.tenants(id),
  transaction_id          uuid NOT NULL REFERENCES t.transactions(id) ON DELETE CASCADE,
  tender_sequence         int NOT NULL,
  tender_type_id          uuid NOT NULL REFERENCES f.tender_types(id),
  amount                  numeric(14,4) NOT NULL,
  currency                text NOT NULL DEFAULT 'USD',
  cash_back_amount        numeric(14,4) NOT NULL DEFAULT 0,           -- debit cash-back
  change_amount           numeric(14,4) NOT NULL DEFAULT 0,           -- change given (cash)
  card_token              text,                                       -- masked card number (PII tier 2: tokenized, not raw PAN)
  card_last_4             text,
  card_brand              text,                                       -- VISA | MC | AMEX | DISC
  authorization_code      text,
  processor_reference     text,                                       -- gateway transaction ID
  is_voided               boolean NOT NULL DEFAULT false,
  is_refund               boolean NOT NULL DEFAULT false,             -- this tender is the refund leg
  contactless             boolean NOT NULL DEFAULT false,
  attributes              jsonb NOT NULL DEFAULT '{}',                -- gift card balance after, EBT eligible amount, etc.
  created_at              timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, transaction_id, tender_sequence)
);

CREATE INDEX idx_tend_tenant ON t.transaction_tenders(tenant_id);
CREATE INDEX idx_tend_tx ON t.transaction_tenders(transaction_id);
CREATE INDEX idx_tend_type ON t.transaction_tenders(tender_type_id);
CREATE INDEX idx_tend_card ON t.transaction_tenders(card_last_4) WHERE card_last_4 IS NOT NULL;
CREATE INDEX idx_tend_processor ON t.transaction_tenders(processor_reference) WHERE processor_reference IS NOT NULL;
```

### Operational lifecycle

**Producers**: `mcp.transaction.tender.add`, `mcp.transaction.tender.void`, `mcp.transaction.tender.refund`
**Consumers**: `mcp.cash-management.drawer-update`, `mcp.financial.tender-aggregate.daily`, `mcp.q.detection.tender-pattern` (suspicious refund-only-card patterns)

### Provenance

- **ARTS reference**: POSLog Tender
- **CRDM folded**: `CRDM_Tender` (most fields preserved; some columns like SmartCardFlg fold into JSONB)
- **Justification**: Card token only (PII tier 2) — never raw PAN. Cashback and change as separate columns enable proper drawer reconciliation. Multi-tender per transaction (sequence) supports split tender (partial cash + partial card).

---

## t.transaction_discounts

**ARTS reference**: ARTS POSLog Discount + LineDiscount.
**Module**: T.

### Schema

```sql
CREATE TABLE t.transaction_discounts (
  id                      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id               uuid NOT NULL REFERENCES app.tenants(id),
  transaction_id          uuid NOT NULL REFERENCES t.transactions(id) ON DELETE CASCADE,
  discount_sequence       int NOT NULL,
  scope                   text NOT NULL,                              -- transaction | line | tender
  line_item_id            uuid REFERENCES t.transaction_line_items(id) ON DELETE CASCADE,  -- if scope=line
  discount_type           text NOT NULL,                              -- promotion | manual_override | manager_discount | staff_discount | loyalty_redeem | coupon | senior | military | etc.
  source_promotion_id     uuid REFERENCES p.promotions(id),
  promotion_rule_id       uuid REFERENCES p.promotion_rules(id),
  amount                  numeric(14,4) NOT NULL,                     -- the actual amount discounted
  percentage              numeric(5,4),                                -- if percentage-based
  reason_code             text,
  authorized_by_employee_id uuid REFERENCES e.employees(id),         -- manager override
  attributes              jsonb NOT NULL DEFAULT '{}',                -- coupon code, loyalty redemption details
  created_at              timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_disc_tenant ON t.transaction_discounts(tenant_id);
CREATE INDEX idx_disc_tx ON t.transaction_discounts(transaction_id);
CREATE INDEX idx_disc_line ON t.transaction_discounts(line_item_id);
CREATE INDEX idx_disc_promo ON t.transaction_discounts(source_promotion_id);
CREATE INDEX idx_disc_type ON t.transaction_discounts(discount_type);
CREATE INDEX idx_disc_authorizer ON t.transaction_discounts(authorized_by_employee_id) WHERE authorized_by_employee_id IS NOT NULL;
```

### Operational lifecycle

**Producers**: `mcp.transaction.discount.apply`, `mcp.transaction.discount.void`
**Consumers**: `mcp.metrics.discount-effectiveness`, `mcp.q.detection.discount-abuse` (manager-discount frequency, staff-discount patterns), `mcp.loyalty.redeem.from-discount`

### Provenance

- **ARTS reference**: POSLog Discount + LineDiscount
- **CRDM folded**: `CRDM_TransactionDiscount` + `CRDM_ItemDiscount` (2 entities → 1 with `scope` discriminator)
- **Justification**: Single table with `scope` discriminator (transaction-wide, line-specific, tender-specific) covers all discount kinds. `authorized_by_employee_id` is critical for Q-module audit (who approved the override?).

---

## t.cashier_actions

**ARTS reference**: ARTS POSLog OperationalEvent.
**Module**: T (Q-relevant).

### Schema

```sql
CREATE TABLE t.cashier_actions (
  id                      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id               uuid NOT NULL REFERENCES app.tenants(id),
  transaction_id          uuid REFERENCES t.transactions(id),         -- nullable for between-transaction actions
  location_id             uuid NOT NULL REFERENCES l.locations(id),
  cashier_employee_id     uuid NOT NULL REFERENCES e.employees(id),
  pos_terminal_id         text,
  action_type             text NOT NULL,                              -- key_lock_change | manager_override | drawer_open | price_check | item_lookup | suspend | recall | training_mode_toggle | refund_authorize
  performed_at            timestamptz NOT NULL DEFAULT now(),
  authorized_by_employee_id uuid REFERENCES e.employees(id),         -- if requires manager auth
  details                 jsonb NOT NULL DEFAULT '{}',                -- action-specific payload
  attributes              jsonb NOT NULL DEFAULT '{}',
  created_at              timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_actions_tenant ON t.cashier_actions(tenant_id);
CREATE INDEX idx_actions_tx ON t.cashier_actions(transaction_id) WHERE transaction_id IS NOT NULL;
CREATE INDEX idx_actions_cashier ON t.cashier_actions(cashier_employee_id, performed_at);
CREATE INDEX idx_actions_type ON t.cashier_actions(action_type);
CREATE INDEX idx_actions_authorizer ON t.cashier_actions(authorized_by_employee_id) WHERE authorized_by_employee_id IS NOT NULL;
```

### Operational lifecycle

**Producers**: `mcp.cashier.action.log` — every cashier action logged
**Consumers**: `mcp.q.detection.action-pattern` (override frequency, drawer-open without sale), `mcp.audit.cashier-activity-report`

### Provenance

- **ARTS reference**: POSLog OperationalEvent
- **CRDM folded**: `CRDM_OperatorAction`
- **Justification**: Critical for Q-module shrink detection — patterns like "frequent manager overrides by cashier X" or "drawer opens without transaction" are first-class signals.

---

## t.cash_drawer_events

**ARTS reference**: ARTS Sales Audit — drawer open/close, count.
**Module**: T.

### Schema

```sql
CREATE TABLE t.cash_drawer_events (
  id                      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id               uuid NOT NULL REFERENCES app.tenants(id),
  location_id             uuid NOT NULL REFERENCES l.locations(id),
  pos_terminal_id         text NOT NULL,
  cashier_employee_id     uuid REFERENCES e.employees(id),
  event_type              text NOT NULL,                              -- shift_start_count | shift_end_count | mid_shift_count | paid_in | paid_out | safe_drop | float_pull
  event_at                timestamptz NOT NULL DEFAULT now(),
  expected_amount         numeric(14,4),                              -- system-computed expected balance
  counted_amount          numeric(14,4),                              -- physically counted
  variance                numeric(14,4) GENERATED ALWAYS AS (COALESCE(counted_amount, 0) - COALESCE(expected_amount, 0)) STORED,
  reason                  text,
  paid_in_out_amount      numeric(14,4),                              -- for paid_in / paid_out events
  reference               text,                                       -- supplier name (paid_out), invoice ref (paid_in)
  attributes              jsonb NOT NULL DEFAULT '{}',
  created_at              timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_drawer_tenant ON t.cash_drawer_events(tenant_id);
CREATE INDEX idx_drawer_location_terminal ON t.cash_drawer_events(location_id, pos_terminal_id, event_at);
CREATE INDEX idx_drawer_cashier ON t.cash_drawer_events(cashier_employee_id, event_at);
CREATE INDEX idx_drawer_variance ON t.cash_drawer_events(location_id) WHERE variance IS NOT NULL AND variance != 0;
```

### Operational lifecycle

**Producers**: `mcp.cash-drawer.shift-start`, `mcp.cash-drawer.count`, `mcp.cash-drawer.paid-in`, `mcp.cash-drawer.paid-out`, `mcp.cash-drawer.shift-end`
**Consumers**: `mcp.financial.cash-reconciliation`, `mcp.q.detection.drawer-variance`, `mcp.metrics.cashier-accuracy`

### Provenance

- **ARTS reference**: Sales Audit drawer events
- **CRDM folded**: `CRDM_CashOfficeSafe` + `CRDM_PaidIn_PaidOut`
- **Canary current**: `sales.cash_drawer_shifts` + `sales.cash_drawer_events` — this consolidates and enriches
- **Justification**: Generated `variance` column makes shrink-detection queries O(1) per event. Cash drawer variance is the second-most-watched Q signal after refund-fraud.

---

## t.shift_events

**ARTS reference**: ARTS Sales Audit — operator session.
**Module**: T.

### Schema

```sql
CREATE TABLE t.shift_events (
  id                      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id               uuid NOT NULL REFERENCES app.tenants(id),
  location_id             uuid NOT NULL REFERENCES l.locations(id),
  pos_terminal_id         text NOT NULL,
  cashier_employee_id     uuid NOT NULL REFERENCES e.employees(id),
  shift_start             timestamptz NOT NULL,
  shift_end               timestamptz,                                 -- NULL = active shift
  transaction_count       int NOT NULL DEFAULT 0,                     -- denormalized
  total_sales             numeric(14,4),                               -- denormalized
  starting_drawer_amount  numeric(14,4),
  ending_drawer_amount    numeric(14,4),
  attributes              jsonb NOT NULL DEFAULT '{}',
  created_at              timestamptz NOT NULL DEFAULT now(),
  updated_at              timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, location_id, pos_terminal_id, cashier_employee_id, shift_start)
);

CREATE INDEX idx_shifts_tenant ON t.shift_events(tenant_id);
CREATE INDEX idx_shifts_location ON t.shift_events(location_id);
CREATE INDEX idx_shifts_cashier ON t.shift_events(cashier_employee_id);
CREATE INDEX idx_shifts_active ON t.shift_events(location_id) WHERE shift_end IS NULL;
```

### Operational lifecycle

**Producers**: `mcp.shift.start`, `mcp.shift.end`, `mcp.shift.update-running-totals`
**Consumers**: `mcp.metrics.cashier-productivity`, `mcp.q.detection.shift-anomaly`, `mcp.scheduling.actual-vs-planned`

### Provenance

- **ARTS reference**: Sales Audit operator session
- **Justification**: Denormalized counts and totals on shift row for fast cashier-shift performance queries without re-aggregating transactions.

---

## t.loyalty_events

**ARTS reference**: ARTS Loyalty Event (earn / redeem / adjustment).
**Module**: T.

### Schema

```sql
CREATE TABLE t.loyalty_events (
  id                      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id               uuid NOT NULL REFERENCES app.tenants(id),
  loyalty_membership_id   uuid NOT NULL REFERENCES c.loyalty_memberships(id),
  transaction_id          uuid REFERENCES t.transactions(id),         -- if event is transaction-derived
  event_type              text NOT NULL,                              -- earn | redeem | manual_adjustment | tier_upgrade | tier_downgrade | bonus | expire | enroll
  points_delta            bigint NOT NULL,                            -- signed; positive = added, negative = used
  amount_basis            numeric(14,4),                              -- $ amount that earned the points
  reason                  text,
  attributes              jsonb NOT NULL DEFAULT '{}',
  created_at              timestamptz NOT NULL DEFAULT now()
  -- append-only
);

CREATE INDEX idx_loyalty_evt_tenant ON t.loyalty_events(tenant_id);
CREATE INDEX idx_loyalty_evt_member ON t.loyalty_events(loyalty_membership_id, created_at);
CREATE INDEX idx_loyalty_evt_tx ON t.loyalty_events(transaction_id) WHERE transaction_id IS NOT NULL;
CREATE INDEX idx_loyalty_evt_type ON t.loyalty_events(event_type);
```

### Operational lifecycle

**Producers**: `mcp.loyalty.event.from-transaction`, `mcp.loyalty.event.manual-adjustment`, `mcp.loyalty.event.tier-evaluate`
**Consumers**: `mcp.loyalty.points-balance.recompute` (sum-of-deltas — backstop for c.loyalty_memberships.points_balance), `mcp.metrics.loyalty-engagement`

### Provenance

- **ARTS reference**: Loyalty Event
- **CRDM folded**: `CRDM_LoyaltyCard` + `CRDM_PointsCoupon`
- **Justification**: Append-only event log gives full audit trail and recompute capability. The denormalized `c.loyalty_memberships.points_balance` is updated atomically with each event; `t.loyalty_events` is the source of truth.

---

## t.gift_card_events

**ARTS reference**: ARTS Gift Card Activity.
**Module**: T.

### Schema

```sql
CREATE TABLE t.gift_card_events (
  id                      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id               uuid NOT NULL REFERENCES app.tenants(id),
  gift_card_id            uuid NOT NULL,                              -- references app.gift_cards (current Canary spec)
  transaction_id          uuid REFERENCES t.transactions(id),
  event_type              text NOT NULL,                              -- activate | reload | redeem | refund | expire | inquiry | adjustment
  amount_delta            numeric(14,4) NOT NULL,                     -- signed
  balance_after           numeric(14,4) NOT NULL,
  authorization_code      text,
  attributes              jsonb NOT NULL DEFAULT '{}',
  created_at              timestamptz NOT NULL DEFAULT now()
  -- append-only
);

CREATE INDEX idx_gc_tenant ON t.gift_card_events(tenant_id);
CREATE INDEX idx_gc_card ON t.gift_card_events(gift_card_id, created_at);
CREATE INDEX idx_gc_tx ON t.gift_card_events(transaction_id) WHERE transaction_id IS NOT NULL;
CREATE INDEX idx_gc_type ON t.gift_card_events(event_type);
```

### Operational lifecycle

**Producers**: `mcp.gift-card.event.from-transaction`, `mcp.gift-card.event.from-online-portal`
**Consumers**: `mcp.gift-card.balance.compute`, `mcp.financial.deferred-revenue.aggregate-gift-cards`, `mcp.q.detection.gift-card-fraud-pattern`

### Provenance

- **ARTS reference**: Gift Card Activity
- **CRDM folded**: `CRDM_GiftCard` (operational events; the gift card master is `app.gift_cards` in current Canary spec, preserved)
- **Justification**: Append-only event log. Gift card balance is a financial liability (deferred revenue) — accurate event log enables both customer-facing balance display and financial-statement gift-card-liability calculation.

---

## Domain summary

**9 entities, 1 schema (t), 1 module (T)**:
- `t.transactions` (~30 cols) — header with parent FK for returns/voids
- `t.transaction_line_items` (~24 cols, 4 generated) — full POSLog line detail
- `t.transaction_tenders` (~15 cols) — multi-tender, card-tokenized
- `t.transaction_discounts` (~13 cols) — single table with scope discriminator
- `t.cashier_actions` (~10 cols) — operator action log
- `t.cash_drawer_events` (~13 cols, generated variance) — drawer reconciliation
- `t.shift_events` (~13 cols) — operator session with denormalized totals
- `t.loyalty_events` (~9 cols, append-only) — earn/redeem log
- `t.gift_card_events` (~9 cols, append-only) — gift card activity log

**Folded from sources**:
- CRDM 25 POS entities → 9 transaction entities (others: aggregations like `CRDM_FastFact`, `CRDM_ItemFastFact` → metrics schema; movements like `CRDM_GoodsReceived`, `CRDM_StockAdjustment`, etc. → i schema (Chunk 5); customer/employee → c/e schemas)

**MCP service junctions defined for this domain (~22)**:
- Transaction: start, complete, void, return-from-receipt, suspend-and-recall, line.{add, void, return}, tender.{add, void, refund}, discount.{apply, void}
- Cashier: action.log
- Cash drawer: shift-start, count, paid-in, paid-out, shift-end
- Shift: start, end, update-running-totals
- Loyalty: event.from-transaction, event.manual-adjustment, event.tier-evaluate
- Gift card: event.from-transaction, event.from-online-portal
- Cross-cutting consumers: inventory.movement.from-transaction, financial.tender-aggregate.daily, metrics.fact-transaction, q.detection.scan-transaction, audit.transaction.export, q.detection.{action-pattern, drawer-variance, tender-pattern, gift-card-fraud-pattern}, loyalty.points-balance.recompute, gift-card.balance.compute

## Status

- **Chunk 7 complete.** 9 ARTS-POSLog-aligned transaction entities. CRDM 25 POS entities folded with aggregates correctly routed to metrics schema.
- **Resume**: Chunk 8 — Canary platform mechanics (Chirp / Fox / Hawk / Owl / ILDWAC / identity / audit / etc.). Target ~10-15 entities. These sit ABOVE ARTS — Canary-specific.
