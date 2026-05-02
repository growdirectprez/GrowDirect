# Chunk 9 — Module Ownership Matrix

**Purpose**: Map every canonical entity to its primary module + cross-module consumers. The 13-module spine (post-rename: M, O, C, E, T, F, A, D, N, P, S, L, Q) is the architectural decomposition; this matrix shows where each entity lives and who touches it.

## The 13-module spine

| Letter | Module | Domain |
|---|---|---|
| **M** | Merchandising | Item master, vendor master, categorization, packs |
| **O** | Orders | Purchase orders, sales orders, fulfillment, allocation, ASN/BOL |
| **C** | Customer | Customer master, addresses, loyalty |
| **E** | Execution / Workflow | Task management, work assignment **(greenfield — no entities in this canonical)** |
| **T** | Transaction Pipeline | POSLog transactions, line items, tenders, discounts, sales audit |
| **F** | Finance | GL accounts, supplier invoices, payments, tender types, ledger |
| **A** | Asset | Locations (stores, warehouses, DCs), location hierarchy |
| **D** | Distribution | Inventory positions, movements, documents, lots |
| **N** | Device | POS terminals, kiosks, mobile **(currently inline in t.transactions.pos_terminal_id; full schema TBD)** |
| **P** | Pricing | Price books, promotions, promotion rules, taxes |
| **S** | Space | Planograms, planogram positions, location zones, location assortment |
| **L** | Labor / People | Employees, role assignments, location assignments |
| **Q** | Loss Prevention | Detection rules, detections, cases, evidence, subjects |

## Canonical entity → module ownership matrix

**Convention**: Primary owner in **bold**. Secondary modules consume but don't own.

### Schema `m` (Merchandising)

| Entity | Primary | Consumed by |
|---|---|---|
| `m.items` | **M** | T (line items), D (inventory), P (pricing), O (PO/SO lines), Q (LP scans) |
| `m.product_categories` | **M** | T (snapshot at sale), F (tax mapping), P (promotion scope), S (planogram scope) |
| `m.vendors` | **M** | O (PO vendor), F (invoice vendor), D (GRN vendor), Q (RTV-fraud subject ref) |
| `m.item_vendors` | **M** | O (PO cost lookup), D (receipt cost), F (3-way match) |
| `m.item_barcodes` | **M** | T (scan resolve), D (cycle count) |
| `m.item_packs` | **M** | D (break-down on receipt), T (sell-as-unit) |

### Schema `l` (Location / Asset)

| Entity | Primary | Consumed by |
|---|---|---|
| `l.locations` | **A** | All other domains (every entity is location-scoped) |
| `l.location_hierarchy` + `_assignments` | **A** | F (tax zones), P (regional promotions), Metrics (rollups) |
| `l.location_zones` | **A** | S (planogram positions), Q (shrink-by-zone), D (cycle-count scope) |
| `l.location_assortment` | **A** + **M** + **S** | T (scan validate), D (replenishment scope), O (replenishment), Q (lost sale signal) |

### Schema `s` (Space)

| Entity | Primary | Consumed by |
|---|---|---|
| `s.planograms` + `_assignments` | **S** | D (replenishment capacity), N (shelf-edge labels) |
| `s.planogram_positions` | **S** | D (capacity-driven replenishment qty), N (shelf labels) |

### Schema `c` (Customer)

| Entity | Primary | Consumed by |
|---|---|---|
| `c.customers` | **C** | T (transaction customer), O (sales order customer), F (invoice bill-to), Q (case subject ref), Marketing |
| `c.customer_addresses` | **C** | O (shipping resolve), F (bill-to), Marketing (geo-segment) |
| `c.loyalty_memberships` | **C** | T (transaction loyalty lookup), Marketing (tier campaigns) |

### Schema `e` (Employee)

| Entity | Primary | Consumed by |
|---|---|---|
| `e.employees` | **L** | T (cashier on transaction), Q (subject), F (manager-approval cross-cuts), Audit |
| `e.employee_role_assignments` | **L** | App (RBAC), T (manager-override authorize) |
| `e.employee_location_assignments` | **L** | T (employee-at-location validate), Scheduling |

### Schema `i` (Inventory / Distribution)

| Entity | Primary | Consumed by |
|---|---|---|
| `i.inventory_positions` | **D** | T (scan availability), O (allocation), F (valuation cross-cut), Replenishment, Forecast, Q (shrink) |
| `i.inventory_movements` | **D** | F (stock_ledger_entries — financial valuation), Q (shrink detection on adjustments), Metrics |
| `i.inventory_documents` + `_lines` | **D** | F (3-way match), O (receipt-vs-PO reconciliation), Audit |
| `i.inventory_lots` | **D** | T (lot scan), O (FEFO allocation), Compliance (recall) |

### Schema `o` (Orders)

| Entity | Primary | Consumed by |
|---|---|---|
| `o.purchase_orders` + `_lines` | **O** | F (AP encumbrance, 3-way match), D (receipt expectation), M (item-vendor cost) |
| `o.sales_orders` + `_lines` | **O** | T (POS order completion), F (revenue recognition), C (customer history) |
| `o.fulfillments` + `_lines` | **O** | D (movement on pick), L (employee assignment), Customer (notification) |
| `o.allocations` | **O** | D (ATP computation: on_hand - SUM allocations), T (scan-validate vs allocation) |
| `o.shipping_documents` | **O** | D (expected arrival update), Customer (tracking) |

### Schema `p` (Pricing)

| Entity | Primary | Consumed by |
|---|---|---|
| `p.item_prices` | **P** | T (price resolve), Storefront, Metrics |
| `p.promotions` + `_rules` | **P** | T (promotion evaluate), Metrics (effectiveness) |
| `p.tax_classes` + `p.tax_rates` | **P** + **F** | T (tax compute), F (tax liability aggregate) |

### Schema `f` (Finance)

| Entity | Primary | Consumed by |
|---|---|---|
| `f.tender_types` | **F** | T (every payment), Q (tender pattern detection) |
| `f.gl_accounts` | **F** | F (posting destination), Accounting integration |
| `f.supplier_invoices` + `_lines` | **F** | O (3-way match), F (payment scheduling), Audit |
| `f.payments` + `_invoice_applications` | **F** | F (cash flow), Audit |

### Schema `t` (Transaction Pipeline)

| Entity | Primary | Consumed by |
|---|---|---|
| `t.transactions` | **T** | D (movements), F (tender aggregate), C (loyalty earn), Q (rule eval), Metrics |
| `t.transaction_line_items` | **T** | D (movement-from-line), Q (line pattern detection), Metrics |
| `t.transaction_tenders` | **T** | F (drawer reconciliation), Q (tender pattern) |
| `t.transaction_discounts` | **T** | P (promotion effectiveness), Q (discount abuse), C (loyalty redeem) |
| `t.cashier_actions` | **T** | Q (action pattern), Audit |
| `t.cash_drawer_events` | **T** | F (cash recon), Q (drawer variance), Metrics |
| `t.shift_events` | **T** | L (productivity), Scheduling, Q (shift anomaly) |
| `t.loyalty_events` | **T** | C (balance recompute backstop), Metrics |
| `t.gift_card_events` | **T** | F (deferred revenue), Q (gift-card-fraud) |

### Schema `q` (Loss Prevention)

| Entity | Primary | Consumed by |
|---|---|---|
| `q.detection_rules` | **Q** | (configuration only) |
| `q.detections` | **Q** | Alert (notify), Q (case escalation), Metrics |
| `q.cases` | **Q** | Audit (case history), Metrics (resolution time) |
| `q.case_evidence` | **Q** | Ledger (blockchain anchor), Audit (chain of custody) |
| `q.case_actions` | **Q** | Audit |
| `q.subjects` | **Q** | Q (case primary subject), Audit (subject investigation history) |

### Schema `ledger` (Cost-to-Serve + Accountability)

| Entity | Primary | Consumed by |
|---|---|---|
| `ledger.stock_ledger_entries` | **F** | F (COGS), Metrics (margin) |
| `ledger.ildwac_positions` | **F** | F (L402 charge), Metrics (cost-to-serve) |
| `ledger.rib_batches` | **F** | F (cost averaging → stock_ledger), Metrics (cost trend) |
| `ledger.l402_otb_budgets` | **F** | All operations (gate-check before consuming), Alert (threshold breach) |
| `ledger.blockchain_anchors` | **F** + **Q** | Q (evidence anchor verify), Audit (cryptographic integrity) |

### Schema `app` (Cross-Cutting Platform)

| Entity | Primary | Consumed by |
|---|---|---|
| `app.tenants` | platform | Every other entity |
| `app.users` | platform | Every state-changing operation (audit attribution), RBAC |
| `app.audit_log` | platform | Compliance, support, Q (forensic timeline) |
| `app.external_identities` | platform | Every entity with external system origin (POS, processor, accounting) |

### Schema `memory` (Agent Memory)

| Entity | Primary | Consumed by |
|---|---|---|
| `memory.alx_memories` | platform | Agent operations, semantic recall |
| `memory.alx_sessions` | platform | Agent context loading |

## Module coverage summary

| Module | Owns (entity count) | Status |
|---|---|---|
| **M** Merchandising | 6 | ✅ ARTS-aligned, GSLM-folded |
| **A** Asset | 4 | ✅ ARTS Location V2 anchored |
| **S** Space | 2 | ✅ ARTS Planogram V2 anchored |
| **C** Customer | 3 | ✅ ARTS Party-Customer aligned, sparse-by-default |
| **L** Labor | 3 | ✅ ARTS Party-Employee, no pay rate stored |
| **D** Distribution | 5 | ✅ ARTS Inventory V2, append-only movement log |
| **O** Orders | 8 | ✅ Greenfield closed via TOM J-Prefix; 3-way match instrumented |
| **P** Pricing | 5 (3 + 2 shared with F) | ✅ Multi-model tax, JSONB rules |
| **F** Finance | 9 (4 f + 5 ledger) | ✅ AP, GL, payment, ILDWAC, L402-OTB, blockchain anchor |
| **T** Transaction | 9 | ✅ ARTS POSLog, append-only events, generated computed cols |
| **Q** LP | 6 | ✅ Fox + Hawk consolidated, evidence chain anchored |
| **E** Execution / Workflow | 0 | ⚠️ **Greenfield not closed in this canonical** — task management TBD |
| **N** Device | 0 (inline) | ⚠️ Currently inline as `t.transactions.pos_terminal_id` text; full Device schema TBD |

**13 modules · 11 fully covered · 2 deferred** (E and N — both legitimately greenfield with no source material to reference; require fresh design later).

## Cross-cutting (not module-owned)

| Schema | Entities | Role |
|---|---|---|
| `app` | 4 (tenants, users, audit_log, external_identities) | Platform fabric — referenced by every module |
| `memory` | 2 (alx_memories, alx_sessions) | Agent persistence |

## Total canonical entity count

**65 canonical entities across 11 schemas:**

| Schema | Entities |
|---|---|
| `m` Merchandising | 6 |
| `l` Location | 4 (locations + hierarchy + assignments + zones + assortment) |
| `s` Space | 2 (planograms + assignments + positions) |
| `c` Customer | 3 |
| `e` Employee | 3 |
| `i` Inventory | 5 |
| `o` Orders | 8 |
| `p` Pricing | 5 |
| `f` Finance | 5 |
| `t` Transaction | 9 |
| `q` Loss Prevention | 6 |
| `ledger` | 5 |
| `app` | 4 (essentials; ~10 more preserved as-is from current Canary spec) |
| `memory` | 2 (preserved) |
| **TOTAL designed** | **65** (+ ~12 preserved from current Canary spec = ~77 in operational canonical) |

Within the 60-80 entity target per Chunk 1.6 design principles. Folded down from:
- GSLM ~102 entities (across 9 domains)
- CRDM 25 POS entities
- TOM 79 fingerprints (operational lifecycle bindings, not entities)
- Canary current ~116 entities (many platform-only and superseded)

Compression ratio: roughly **~250 source entities → ~77 canonical**, achieved through:
- ARTS-anchored decomposition (industry standard, no over-decomposition)
- JSONB pragmatism for variants/extensions
- Discriminator columns for type variants (transaction_type, document_type, movement_type, case_type, etc.)
- Recursive tables with ltree for hierarchies
- COALESCE-PK pattern for nullable-FK uniqueness
- EXCLUDE constraints for temporal and exclusivity rules
- Generated columns for derived values

## Status

- **Chunk 9 complete.** Module ownership matrix locked. 65 canonical entities mapped to 11 of 13 modules (E and N legitimately deferred).
- **Resume**: Chunk 9b — MCP Service Junction Inventory. Consolidate the ~150+ MCP service junctions sprinkled across chunks 2-8 into a single SLA-spec inventory.
