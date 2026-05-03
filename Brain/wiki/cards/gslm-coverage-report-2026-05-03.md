---
title: GSLM 9-domain Coverage Report — 2026-05-03
type: coverage-report
status: active
date: 2026-05-03
linear: GRO-722
parent: GRO-763
authority: GSLM Walmart-International 2009 canonical-model exemplar
provenance: memory project_gslm_provenance
last-compiled: 2026-05-03
needs-review: 2026-08-03
---

# GSLM 9-domain Coverage Report

Static analysis of `CanaryGo/deploy/schema/*.sql` against the Global Store Logical Model (GSLM) — the 9-domain canonical-model exemplar the founder's team defined for Walmart International's 2009 banner-rollout work. GSLM is used here as a **completeness checklist**, not a schema source. Entities listed in GSLM but missing from canonical schema flag potential gaps; entities present in canonical but absent from GSLM are documented as one-way differences (Canary's accountability rails are intentionally richer than the 2009 spec).

## Summary

- **Canonical tables analyzed:** 88
- **Platform plumbing (passthrough):** 32
- **GSLM entities checked:** 81
- **GSLM entities mapped:** 61 (75%)
- **Domains with full core coverage:** 6/9

| Domain | Tables | Core entities | Core mapped | Extension mapped | Gaps (core) |
|---|---|---|---|---|---|
| Item | 6 | 6 | 6/6 | 0/4 | — |
| Customer | 3 | 5 | 3/5 | 0/2 | Party (canonical identity), Household (decisioning unit) |
| Employee | 9 | 7 | 7/7 | 0/2 | — |
| Vendor | 5 | 5 | 4/5 | 0/2 | VendorTerm (payment terms) |
| Location | 7 | 6 | 6/6 | 1/2 | — |
| Pricing | 6 | 8 | 6/8 | 0/1 | Markdown, PriceTier (cost-plus envelope) |
| Inventory | 7 | 8 | 8/8 | 0/1 | — |
| Transaction | 9 | 10 | 10/10 | 0/0 | — |
| Operations | 10 | 9 | 9/9 | 1/3 | — |

## Item

**Canonical tables:**

- `l.location_assortment`
- `m.item_barcodes`
- `m.item_packs`
- `m.item_vendors`
- `m.items`
- `m.product_categories`

**Entities mapped:**

- Item → `m.items`
- ItemHierarchy/Category → `m.product_categories`
- Barcode/GTIN → `m.item_barcodes`
- Pack/UOM → `m.item_packs`
- ItemVendor (sourcing) → `m.item_vendors`
- AssortmentList → `l.location_assortment`

**Gaps:**

- Brand (extension)
- ItemAttribute (extensible) (extension)
- ItemImage/MediaAsset (extension)
- ItemSubstitute/CrossRef (extension)

## Customer

**Canonical tables:**

- `c.customer_addresses`
- `c.customers`
- `c.loyalty_memberships`

**Entities mapped:**

- Customer → `c.customers`
- CustomerAddress → `c.customer_addresses`
- LoyaltyMember → `c.loyalty_memberships`

**Gaps:**

- CustomerSegment (extension)
- CustomerEvent (lifecycle) (extension)
- Party (canonical identity) (**core**)
- Household (decisioning unit) (**core**)

## Employee

**Canonical tables:**

- `app.employee_location_assignments`
- `app.user_employee_links`
- `app.user_roles`
- `app.users`
- `e.employee_location_assignments`
- `e.employee_role_assignments`
- `e.employees`
- `t.cashier_actions`
- `t.shift_events`

**Entities mapped:**

- Employee → `e.employees`
- EmployeeRole/Assignment → `e.employee_role_assignments`, `app.user_roles`
- User (auth-side) → `app.users`
- User-Employee link → `app.user_employee_links`
- EmployeeLocationAssignment → `e.employee_location_assignments`, `app.employee_location_assignments`
- Shift → `t.shift_events`
- TimeClock/Punch → `t.cashier_actions`

**Gaps:**

- EmployeeAvailability (extension)
- Compensation (extension)

## Vendor

**Canonical tables:**

- `f.payment_invoice_applications`
- `f.payments`
- `f.supplier_invoice_lines`
- `f.supplier_invoices`
- `m.vendors`

**Entities mapped:**

- Vendor → `m.vendors`
- SupplierInvoice → `f.supplier_invoices`
- SupplierInvoiceLine → `f.supplier_invoice_lines`
- VendorPayment → `f.payments`, `f.payment_invoice_applications`

**Gaps:**

- VendorContact (extension)
- VendorTerm (payment terms) (**core**)
- VendorPerformance/Scorecard (extension)

## Location

**Canonical tables:**

- `l.location_hierarchy`
- `l.location_hierarchy_assignments`
- `l.location_zones`
- `l.locations`
- `s.planogram_assignments`
- `s.planogram_positions`
- `s.planograms`

**Entities mapped:**

- Location/Site → `l.locations`
- LocationHierarchy → `l.location_hierarchy`, `l.location_hierarchy_assignments`
- LocationZone (back-of-house) → `l.location_zones`
- Planogram → `s.planograms`
- PlanogramAssignment → `s.planogram_assignments`
- PlanogramPosition (slot) → `s.planogram_positions`
- Department/Aisle/Bay/Shelf _(extension)_ → `l.location_zones`

**Gaps:**

- ServiceArea (delivery zone) (extension)

## Pricing

**Canonical tables:**

- `f.tender_types`
- `p.item_prices`
- `p.promotion_rules`
- `p.promotions`
- `p.tax_classes`
- `p.tax_rates`

**Entities mapped:**

- ItemPrice (per item × location) → `p.item_prices`
- Promotion → `p.promotions`
- PromotionRule → `p.promotion_rules`
- TaxRate → `p.tax_rates`
- TaxClass → `p.tax_classes`
- TenderType (config) → `f.tender_types`

**Gaps:**

- Markdown (**core**)
- Coupon (extension)
- PriceTier (cost-plus envelope) (**core**)

## Inventory

**Canonical tables:**

- `i.inventory_document_lines`
- `i.inventory_documents`
- `i.inventory_lots`
- `i.inventory_movements`
- `i.inventory_positions`
- `ledger.stock_ledger_entries`
- `o.allocations`

**Entities mapped:**

- InventoryPosition (on-hand) → `i.inventory_positions`
- InventoryMovement (audit trail) → `i.inventory_movements`
- InventoryDocument (count/RTV) → `i.inventory_documents`
- InventoryDocumentLine → `i.inventory_document_lines`
- Lot → `i.inventory_lots`
- Reservation/Allocation → `o.allocations`
- CycleCount (campaign) → `i.inventory_documents`
- StockLedgerEntry (financial) → `ledger.stock_ledger_entries`

**Gaps:**

- SerialUnit (extension)

## Transaction

**Canonical tables:**

- `t.cash_drawer_events`
- `t.cashier_actions`
- `t.gift_card_events`
- `t.loyalty_events`
- `t.shift_events`
- `t.transaction_discounts`
- `t.transaction_line_items`
- `t.transaction_tenders`
- `t.transactions`

**Entities mapped:**

- Transaction (sale/return/exchange) → `t.transactions`
- TransactionLineItem → `t.transaction_line_items`
- TransactionTender → `t.transaction_tenders`
- TransactionDiscount → `t.transaction_discounts`
- CashDrawerEvent → `t.cash_drawer_events`
- CashierAction (audit) → `t.cashier_actions`
- GiftCardEvent → `t.gift_card_events`
- LoyaltyEvent → `t.loyalty_events`
- ShiftEvent → `t.shift_events`
- Return/Void/Refund (subtypes) → `t.transactions`

**Gaps:**

- _(none — full coverage)_

## Operations

**Canonical tables:**

- `i.inventory_documents`
- `i.inventory_movements`
- `o.allocations`
- `o.fulfillment_lines`
- `o.fulfillments`
- `o.purchase_order_lines`
- `o.purchase_orders`
- `o.sales_order_lines`
- `o.sales_orders`
- `o.shipping_documents`

**Entities mapped:**

- PurchaseOrder → `o.purchase_orders`
- PurchaseOrderLine → `o.purchase_order_lines`
- SalesOrder → `o.sales_orders`
- SalesOrderLine → `o.sales_order_lines`
- Fulfillment (pick/pack/ship) → `o.fulfillments`, `o.fulfillment_lines`
- Allocation (soft-reserve) → `o.allocations`
- ShippingDocument (BOL/manifest) → `o.shipping_documents`
- ReceivingDoc (ASN) → `i.inventory_documents`
- PutAway _(extension)_ → `i.inventory_movements`
- ReturnToVendor (RTV) → `i.inventory_documents`

**Gaps:**

- Replenishment (extension)
- Workflow (cross-cutting orchestration) (extension)

## Top cross-domain gaps (prioritized)

Ranked by impact on the platform mission (operational / financial / evidentiary accountability). Core gaps surface here before extension gaps.

1. **Customer · Party (canonical identity)** (core)
2. **Customer · Household (decisioning unit)** (core)
3. **Vendor · VendorTerm (payment terms)** (core)
4. **Pricing · Markdown** (core)
5. **Pricing · PriceTier (cost-plus envelope)** (core)
6. Item · Brand (extension)
7. Item · ItemAttribute (extensible) (extension)
8. Item · ItemImage/MediaAsset (extension)
9. Item · ItemSubstitute/CrossRef (extension)
10. Customer · CustomerSegment (extension)

## Cross-references

- Memory `project_gslm_provenance` — origin of GSLM as canonical-model exemplar
- [`docs/sdds/go-handoff/canonical-data-model.md`](../../../docs/sdds/go-handoff/canonical-data-model.md) — schema source of truth
- [`docs/sdds/go-handoff/canonical-data-model-party-edits.md`](../../../docs/sdds/go-handoff/canonical-data-model-party-edits.md) — party schema (lands GRO-763 Phase B.5)
- [`services/canary-protocol/coverage/gslm-runner.py`](../../../services/canary-protocol/coverage/gslm-runner.py) — the runner that produced this report
