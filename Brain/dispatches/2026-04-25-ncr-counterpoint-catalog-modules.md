---
type: dispatch
status: ready-for-execution
date: 2026-04-25
target: laptop-side Claude Code
priority: high
phase: 2 of 5 in NCR Counterpoint retail spine integration
prerequisite: Phase 1 priority modules (T R F L N) complete + founder-approved
sdd: docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md
build-plan: docs/superpowers/plans/2026-04-25-ncr-counterpoint-spine-build.md
modules: [P, S]
inputs:
  - SDD §6.10 (Module S), §6.11 (Module P)
  - Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/Endpoints/{Item*,ItemCategor*,ItemSerial*,Item_*,Inventory*,VendorItem,EC,ECCategories}
  - Brain/wiki/ncr-counterpoint-document-model.md (PS_DOC_LIN_PRICE pricing-rule capture)
  - Brain/wiki/garden-center-operating-reality.md (multi-tier pricing, mix-and-match, item-code drift)
tags: [canary, ncr-counterpoint, catalog-modules, phase-2, p, s]
---

# Dispatch — Phase 2: Catalog Modules (P S)

## Operational discipline

Executes on the laptop. Phase 1 (priority modules) must be complete; this phase builds on N (store/station context for items) and R (customer tier for pricing). Founder reviews each sub-phase. No production deployment until Phase 5.

## Why

Catalog modules are H&G-critical and unlock the customer-tier-priced + mix-and-match-flat behaviors that distinguish garden-center retail. Module S (Space / Range / Display) covers the items + categories + inventory surface; Module P (Pricing / Promotion) is **derived from S + R** because Counterpoint exposes no Pricing/Promotion endpoint family — pricing rules surface only as outputs (PS_DOC_LIN_PRICE per ticket line).

**Modules in this phase:**
- **S — Space / Range / Display** (items, categories, item serials, item images, inventory snapshots, vendor-item relationships)
- **P — Pricing / Promotion** (DERIVED — no dedicated endpoints; computes from Item base prices + Customer.CATEG_COD tier + observed PS_DOC_LIN_PRICE rules per transaction)

**Sub-phase sequence:**
- 2a: Module S (catalog backbone — items + categories)
- 2b: Module P (pricing derivation built on S + Phase-1 R)

## Pre-flight reading

1. SDD §6.10 (S) + §6.11 (P revised — no dedicated endpoints, derived only)
2. Counterpoint Items / ItemCategories / Inventory / VendorItem endpoint docs in `Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/Endpoints/`
3. `Brain/wiki/ncr-counterpoint-document-model.md` §"Line items" — pricing-decision capture in PS_DOC_LIN_PRICE
4. `Brain/wiki/garden-center-operating-reality.md` — multi-tier pricing, mix-and-match flats, perishable / live-goods, item-code drift

Produce a one-page pre-flight summary covering: confirmed endpoint list, garden-center-specific field discoveries (mix-match codes, attribute codes, plant-multi-name conventions), tier representation in Customer.CATEG_COD, and how PS_DOC_LIN_PRICE captures the price-rule trail.

## Scope clarification questions ALXjr asks BEFORE code

1. **Item lifecycle policy** — garden-center catalogs are seasonal + volatile. How does Canary handle item retirement (soft-delete with history retained vs. hard delete)? What's the CRDM convention?
2. **Multi-tier pricing model** — derive at consume-time (every read computes), materialize per (customer × item × store) tuple, or hybrid (recent + on-demand)? Cost / latency tradeoff.
3. **Multi-name plants** — botanical / common / Spanish names: confirm via real garden-center data which fields are used (likely ADDL_DESCR_1/2/3 or attribute codes). May need primary research.
4. **Item-code drift** — when the same plant has multiple ITEM_NO records over time, does the adapter try to deduplicate (fuzzy match) or preserve history? Default: preserve; flag for analytics layer to handle.
5. **Mix-and-match groups** — MIX_MATCH_COD on Item + per-line MIX_MATCH_COD on PS_DOC_LIN. CRDM model for the group itself: a separate Things.mix_match_groups entity, or just a tag on items?

## Operating procedure

### Sub-phase 2a — Module S

1. Read SDD §6.10 + Item / ItemCategories / ItemSerial / Item_Images / Item_Inventory / Inventory* / VendorItem endpoint docs
2. CRDM mapping: `Things.items`, `Things.item_categories`, `Things.item_serials`, `Things.item_images`, `Things.item_inventory_by_location`, `Things.vendor_items`
3. TSP adapter: full sync nightly + incremental on item-edit events (RS_UTC_DT > last_sync). Inventory levels poll continuously (not cached server-side). Items metadata polls daily (24h server cache).
4. Garden-center field surfacing: ATTR_COD_1/2 (plant attributes), MIX_MATCH_COD (mix-match group), CATEG_COD/SUBCAT_COD (2-level), ADDL_DESCR_1/2/3 (additional descriptions — may carry botanical/Spanish names)
5. MCP tool surface: `get_items(category?, status?)`, `get_item(item_id)`, `get_item_categories()`, `get_item_inventory(item_id)`, `get_item_images(item_id)`, `search_items_by_attribute(attr_cod, value)` (new — H&G-relevant)
6. Test: fixture suite with H&G-shaped data (plants with multi-name fields, mix-match groups, fractional units, perishable flags)
7. Wiki: update `Brain/wiki/canary-module-s-space-range-display.md` with Counterpoint-mapping section
8. Founder review gate

### Sub-phase 2b — Module P (derived)

1. Read SDD §6.11 (revised — derived only) + Customer.CATEG_COD field semantics + PS_DOC_LIN_PRICE structure
2. CRDM mapping (derived): `Things.item_prices` (computed view), `Things.customer_tiers` (computed view), `Events.pricing_decisions` (sourced from PS_DOC_LIN_PRICE flattened)
3. TSP adapter: NO direct Pricing/Promotion endpoint polling. Instead:
   - Customer.CATEG_COD → tier ID per customer (synced via Module R)
   - Item.PRC_1, REG_PRC, etc. → base prices (synced via Module S)
   - PS_DOC_LIN_PRICE on transaction lines → pricing-decision events (synced via Module T)
   - **Pricing logic lives in the CRDM materialization layer**, not the adapter
4. MCP tool surface (computed at consume-time):
   - `get_price(item_id, customer_id?, store?)` — derives from Item base + Customer tier + recent observed pricing
   - `get_pricing_tier(customer_id)` — derives from Customer.CATEG_COD
   - `list_observed_pricing_rules(item_id, date_range)` — sources from PS_DOC_LIN_PRICE
5. Test: fixture suite covering tier scenarios (retail / landscaper / commercial), multi-store pricing, mix-and-match line pricing
6. Wiki: update `Brain/wiki/canary-module-p-pricing-promotion.md` with the derived-only architecture
7. Founder review gate

## Cross-cutting work (within this phase)

- **CRDM materialization layer** — first-class concept introduced here. Computed views over Counterpoint primitives. Document the pattern; subsequent modules (Q especially) will use it.
- **Catalog volatility handling** — item lifecycle (active / retired / discontinued) tracked + propagated into CRDM. Avoid rejecting deleted items — flag and retain.
- **Multi-store inventory snapshot** — Item × Location grid. Storage strategy: per-(item, location) row vs. JSON column with all locations. Decide based on CRDM convention.

## Out of scope

- Do NOT touch Modules D / J / A / C / Q yet (Phases 3 + 4)
- Do NOT integrate against the H&G chain customer's specific data (Phase 5)
- Do NOT build a new Counterpoint Pricing/Promotion endpoint — this phase confirms there is no such endpoint and works within that constraint
- Do NOT commit code without founder review per sub-phase

## Acceptance criteria

Per module:
- [ ] CRDM mapping documented (S: direct; P: derived)
- [ ] TSP adapter implemented + integration-tested
- [ ] MCP tool surface exposed
- [ ] Fixture suite with H&G-shaped data
- [ ] Wiki article updated

Phase-level:
- [ ] Module S + Module P complete
- [ ] CRDM materialization layer pattern documented
- [ ] H&G-specific fields (mix-match, plant attributes, multi-name conventions if confirmed) handled

## Risks (Phase 2 specific)

- **Multi-tier pricing complexity** — derivation logic for tiered pricing has many edge cases (per-customer overrides, promotion stacking, time-windowed pricing). Risk: scope balloons.
- **Multi-name plant convention not confirmed** — without sandbox or customer data, can't verify which fields hold botanical / Spanish names. Adapter may need a pluggable name-extraction layer.
- **Performance** — large item catalogs (10K+ SKUs typical for mid-size garden centers) plus multi-tier pricing + multi-store inventory means CRDM materialization layer must scale.

## Reporting cadence

Sub-phase checkpoint at end of 2a, 2b. Founder reviews. Surface blockers immediately.

## Related

- `docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md` — §6.10, §6.11
- `docs/superpowers/plans/2026-04-25-ncr-counterpoint-spine-build.md` — Phase 2 row
- `Brain/dispatches/2026-04-25-ncr-counterpoint-priority-modules.md` — Phase 1 (prerequisite)
- `Brain/wiki/ncr-counterpoint-document-model.md` — pricing-rule capture in PS_DOC_LIN_PRICE
- `Brain/wiki/garden-center-operating-reality.md` — H&G domain reality

---

**Dispatch author:** Senior ALX (laptop), 2026-04-25
**Executor:** Laptop-side Claude Code
**Review gate:** Founder reviews pre-flight summary, scope answers, each sub-phase output before next sub-phase
