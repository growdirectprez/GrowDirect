# Design Principles — Canary Go Canonical Data Model

**Working file. Chunk 1.6 output. Ratification gate before entity walks.**

This document locks the design rules every canonical entity in chunks 2-8 must follow. Any rule here that's wrong needs to be wrong in one place, not corrected 80 times during the walk. Read once, ratify, then I execute.

## 1. Anchor: ARTS-compliant, SMB-2030 scoped

**Structural anchor:** ARTS (Association for Retail Technology Standards) — the industry-standard retail operational data model. Originally published by NRF/ARTS, widely implemented by NCR, Oracle Retail, IBM, SAP retail, and most enterprise retail platforms. ARTS dissolved as an org in 2018; the standards remain authoritative.

**ARTS coverage we honor:**
- ARTS Item (product master, hierarchy, attributes)
- ARTS Party (Customer / Employee / Vendor — unified party hierarchy)
- ARTS Location (store, warehouse, hierarchy)
- ARTS Inventory (SKU, stock-on-hand, movements)
- ARTS Pricing (price book, promotions, deals)
- ARTS Tender (payment types, currency)
- ARTS POSLog (transaction event log)
- ARTS Sales Audit
- ARTS Financial (GL hooks, AP, AR, tax)
- ARTS Loyalty
- ARTS Employee (master, role)
- ARTS Device (POS terminal, kiosk, mobile)
- ARTS Planogram

**Local ARTS source PDFs (S10):**
- `ARTS XML Inventory Charter.pdf` + `CR IXRetail Inventory Technical Specification V1.0 20050813.pdf` + `InventoryV2.0.0.xsd`
- `ARTS_LocationV2_Charter_20160202.pdf` + `CR_ARTS_Location_Technical_Specification_V2.0.0_20170301_final.pdf` + `Location V2 Schemas 20170208.zip`
- `LCWD ARTS Planogram Domain Model V2.0.0 20170207.pdf`

For domains where we don't have the local PDF (POSLog, Customer, Item, Pricing, etc.), I use my training knowledge of ARTS canonical structure — naming conventions, entity relationships, attribute patterns. This is well-documented public material.

**Target market: SMB-2030, not enterprise-2010.** Specifically:
- Single store or small fleet (1-100 stores), often 1
- Solo operator wears every hat (per founder memory `project_engine_map_and_main_street_archetype`)
- Single banner (no BusinessDivisions over-decomposition)
- Real-time tech default (Postgres, JSONB, pgvector — not COBOL flat files via BizTalk)
- Agent-driven workflows (MCP services, not human ETL teams)

## 2. Lifecycle: TOM operational clock

ARTS gives the **structure** (what entities exist, what fields, what FKs). TOM (Tesco Operating Model interface specs, S9, 79 fingerprints) gives the **lifecycle dynamics** — when each entity is produced, updated, consumed, by which junction, on what cadence.

**Per founder direction (2026-05-01):** each MCP service at an L3 bus junction is born self-aware of its SLA at that node. The operational clock from TOM is critical for the relationships — it's what makes the canonical executable rather than just descriptive.

**Every canonical entity carries two layers:**
1. **Schema** — ARTS-aligned DDL with PK/FK + UUID strategy + JSONB pragmatism
2. **Operational lifecycle** — the MCP service junctions that touch it (producer, updaters, consumers), each with cadence + SLA

## 3. UUID strategy

| Field | Type | Default | Why |
|---|---|---|---|
| Internal PKs | `uuid` | `gen_random_uuid()` | Stable across systems, no integer-key collision when merging tenants/data |
| Internal FKs | `uuid REFERENCES other(id)` | — | Enforced relational integrity |
| External system IDs (POS-native, vendor-assigned, GS1 GTIN, etc.) | `text` | — | Preserved as data, never as PK |
| Multi-system reconciliation | `app.external_identities` table (already exists in current spec) | — | Maps `(canonical_id, source_system, external_id)` |

**Rule:** UUID PKs everywhere. Never `serial` / `bigserial`. Never composite PKs (composite UNIQUE constraints fine).

## 4. PK / FK conventions

```sql
-- Standard entity skeleton
CREATE TABLE {schema}.{entity} (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id     uuid NOT NULL REFERENCES app.tenants(id),
  {parent_id}   uuid {NOT NULL} REFERENCES {schema}.{parent}(id),
  {natural_key} text NOT NULL,
  ...
  attributes    jsonb DEFAULT '{}',  -- extension fields
  status        text NOT NULL DEFAULT 'active',
  created_at    timestamptz NOT NULL DEFAULT now(),
  updated_at    timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, {natural_key})
);

CREATE INDEX idx_{entity}_tenant ON {schema}.{entity}(tenant_id);
CREATE INDEX idx_{entity}_parent ON {schema}.{entity}({parent_id});
```

**Universal columns** on every entity:
- `id uuid PK`
- `tenant_id uuid NOT NULL REFERENCES app.tenants(id)` — schema-per-tenant strategy already lives in current data-model.md
- `created_at` / `updated_at`
- `attributes jsonb` — extension fields (rule below)
- `status` — soft-state lifecycle column where applicable

**FK rules:**
- All FKs use `uuid REFERENCES`. No string-key FKs.
- `ON DELETE CASCADE` only when the child has zero independent meaning (e.g., line item → transaction). Otherwise `ON DELETE RESTRICT` (default).
- All FKs are indexed.

## 5. JSONB usage rules

**JSONB IS for:**
- Variant attributes (color, size, material — anything where the set of attribute keys differs per item)
- Vertical-specific fields (Rx data on a pharmacy SKU, calorie data on a food SKU)
- Extension fields (merchant-defined attributes, integration-payload echoes)
- Semi-structured payload that might evolve (audit log details, webhook bodies)
- Anything where schema evolution would otherwise require a migration

**JSONB IS NOT for:**
- Identifiers (always typed columns)
- Anything that's queried structurally (`WHERE attributes->>'foo' = 'bar'` is a smell — make it a column)
- Anything indexed for relational integrity
- Anything that has a clear cardinality and stable schema

**When in doubt:** start with a typed column, demote to JSONB only when 3+ variants emerge.

## 6. Entity sizing rule

**Target: 10-30 columns per entity.** If you're at 50+, decompose. If you're at 5, fold into parent.

Counter-examples from sources:
- CRDM_FastFact has ~110 columns → that's a denormalized *aggregate* table, fine for `metrics` schema, NOT for an OLTP entity. SMB-2030 canonical excludes pre-aggregated FastFacts (build aggregations in `metrics` schema as separate entities).
- GSLM SalesOutletSKUItemPromoCompDetails — 5-table joined name → 1 entity that crosses too many concerns. Decompose into store_assortment + assortment_promotion (2 entities).

## 7. Naming conventions

- **Schema names:** lowercase, single word where possible — `m` (master), `t` (transaction), `i` (inventory), `p` (pricing), `f` (financial), `o` (orders), `q` (quality/loss-prevention), `app` (cross-cutting platform)
- **Entity names:** lowercase plural snake_case — `items`, `transactions`, `purchase_orders`
- **Column names:** lowercase singular snake_case — `item_id`, `created_at`, `tenant_id`
- **ARTS naming:** ARTS uses PascalCase singular (`RetailTransaction`, `Item`). We translate to lowercase plural snake_case for Postgres/SMB convention (`retail_transactions`, `items`). Document the mapping in each entity entry.
- **No abbreviations** in entity names. `purchase_orders` not `pos`. `customer_loyalty_memberships` not `cust_lty_mem`.

## 8. Module-schema mapping

Per the 13-module spine (post-rename: M=Merchandising, O=Orders, C=Customer, E=Execution, T=Transaction, F=Finance, A=Asset, D=Distribution, N=Device, P=Pricing, S=Space, L=Labor, Q=Loss Prevention):

| Schema | Modules served | Notes |
|---|---|---|
| `m` (master) | M | items, vendors, categories, attributes |
| `i` (inventory) | D | inventory positions, movements (separate from item master) |
| `t` (transaction) | T | POSLog transactions + line items + tenders |
| `o` (orders) | O | purchase orders, sales orders, fulfillment, ASN, BOL |
| `p` (pricing) | P | price books, promotions, deals, taxes |
| `f` (financial) | F | GL accounts, AP/AR, supplier invoices, three-way match |
| `c` (customer) | C | customer master, loyalty, segments |
| `l` (location) | A, S | stores, hierarchy, sales floors, planograms |
| `e` (employee) | L (people domain) | employees, roles, schedules |
| `n` (device) | N | POS terminals, kiosks, mobile |
| `app` | cross-cutting | identity, tenants, settings, feature flags, audit |
| `q` (loss prevention) | Q | Chirp rules, Fox cases, Hawk incidents, Owl observability |
| `metrics` | reporting | facts, dimensions, ML features (denormalized) |
| `ledger` | F (sub-schema) | RIB batches, stock ledger, ILDWAC positions |
| `memory` | platform | agent memory, sessions |

## 9. Cardinality-aware decomposition

Don't pre-decompose for theoretical scale SMB will never hit. Examples of WHERE we deviate from full enterprise ARTS:

| ARTS / GSLM full | SMB-2030 canonical |
|---|---|
| BusinessDivision → Department → Section → Class → SubClass → FineLine (6 levels, 6 tables) | `m.product_categories` (recursive, 1 table, depth as data) |
| StyleVariants + Values + Groups + Assignments (4 tables) | `attributes jsonb` on `m.items` |
| ArticleItems vs SKUItems vs PackItems (separate tables for different item kinds) | `m.items` with `item_type` column; `m.item_pack_components` for pack relationships only when pack-aware merchant |
| MerchandiseAttributesLanguages (multi-language separate table) | `attributes->>'i18n'` jsonb (single-language v1, multi-lang via JSONB later) |
| SalesOutletSKUItemPromoCompDetails (5-concept join table) | `i.store_assortment` + `p.assortment_promotion` (2 narrow tables) |

**Test for inclusion:** is this decomposition justified by SMB-2030 query patterns or scale? If no, fold.

## 10. Future-proofing for agent reads (the founder's direct question)

Six principles applied to every entity:

1. **Agent-shaped reads** — each entity is one coherent semantic unit. One agent read = one meaningful object. No "join 5 tables to make sense of a single product."
2. **Embedding-friendly** — text columns (descriptions, names, notes) support pgvector semantic search natively. Don't shred descriptive text into normalized lookup tables.
3. **MCP-junction-friendly** — entity boundaries map cleanly to MCP service boundaries. No straddling.
4. **JSONB for variants & extensions** — schema evolution doesn't require a migration.
5. **Cardinality-aware** — see §9.
6. **Standards-conformant** — ARTS-aligned naming and relationships. Future integration with any retail tech speaks our language without translation layers.

## 11. Provenance requirement

Every canonical entity entry documents its provenance trail:

- **ARTS reference** — which ARTS standard (and version) it aligns to
- **GSLM source** — which GSLM entity(ies) it folds (if any)
- **CRDM source** — which CRDM entity it's the operational counterpart for (if any)
- **TOM lifecycle** — which TOM interface fingerprints touch it (which junctions produce/update/consume)
- **Canary current** — which Canary `data-model.md` table it supersedes (if any)
- **Justification** — one sentence on why we made the design choices we did

This is the audit trail that lets the next session (or auditor) understand WHY this canonical looks the way it does.

## 12. Operational lifecycle template

For every entity, a structured "lifecycle" section using TOM fingerprints (S9):

```markdown
#### Operational lifecycle (TOM operational clock)

**Producers** (junctions that create/update this entity):
- `mcp.{domain}.{entity}.create` ← {ARTS event} ← {originating system in TOM}
- `mcp.{domain}.{entity}.update` ← {ARTS event} ← {originating system in TOM}

**Consumers** (junctions that read this entity downstream):
- `mcp.{domain}.{entity}.lookup` (real-time, T module)
- `mcp.{domain}.{entity}.aggregate` (batch, metrics schema)
- `mcp.{domain}.{entity}.replicate` (daily, downstream forecast)

**Cadence at producer:** real-time | event-triggered | scheduled-batch | on-demand
**Cadence at consumers:** {per-consumer SLA}
**Idempotency contract:** {key} (e.g., (tenant_id, sku) for items)
**SLA targets at producer:** latency p95 <X, freshness <Y, atomicity {transactional | eventual}
**Cross-references:** {related junctions, e.g., "produces inventory_movement when consumed"}
```

The values come from the TOM fingerprints we extracted in Chunk 1.5. Each canonical entity references its lifecycle by enumerating which fingerprints touch it.

## 13. Canary platform additions

Canary's loss-prevention / observability / case-management layer (Chirp / Fox / Hawk / Owl / Bull / RaaS / Vault / ILDWAC / blockchain anchor / evidence chain) sits ABOVE ARTS — these aren't ARTS entities, they're Canary platform mechanics. Same design rules apply (UUID PKs, JSONB pragmatism, agent-friendly), but no ARTS provenance.

## Status

- **Chunk 1.6 in progress.** Ratification needed before walks proceed.
- **Resume point:** Chunk 2 — Item domain. ARTS Item structural anchor + TOM C-Prefix lifecycle fingerprints. Target ~6-8 entities (items, product_categories, vendors, item_vendors, item_packs if needed, item_taxes if needed).

## Ratification gate

Five questions for the founder before I proceed:

1. **ARTS as structural anchor + TOM as lifecycle dimension** — yes?
2. **UUID PKs + tenant_id everywhere + standard timestamp columns** — yes?
3. **JSONB for variants/extensions, typed columns for queryables** — yes?
4. **10-30 column target per entity, fold ARTS over-decomposition where SMB doesn't need it** — yes?
5. **Schema-per-domain (m, i, t, o, p, f, c, l, e, n, q + cross-cutting app) within schema-per-tenant pattern** — yes?

Say "yes all five" or call out which ones need adjustment.
