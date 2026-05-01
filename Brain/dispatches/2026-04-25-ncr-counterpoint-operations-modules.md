---
type: dispatch
status: ready-for-execution
date: 2026-04-25
target: laptop-side Claude Code
priority: medium
phase: 3 of 5 in NCR Counterpoint retail spine integration
prerequisite: Phase 2 catalog modules (P S) complete + founder-approved
sdd: docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md
build-plan: docs/superpowers/plans/2026-04-25-ncr-counterpoint-spine-build.md
modules: [D, J]
inputs:
  - SDD §6.7 (Module D), §6.9 (Module J)
  - Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/Endpoints/{InventoryLocations,Inventory_ByLocation,Items_ByLocation,VendorItem,Document}
  - Brain/wiki/ncr-counterpoint-document-model.md (Document type taxonomy — XFER, PO, PREQ, RECVR, RTV)
tags: [canary, ncr-counterpoint, operations-modules, phase-3, d, j]
---

# Dispatch — Phase 3: Operations Modules (D J)

## Operational discipline

Executes on the laptop. Phase 2 must be complete (catalog supports D and J — items / inventory snapshots / vendor relationships). Module W is **out of scope** per SDD §6.13 (no Counterpoint coverage; separate effort if pursued).

## Why

Operations modules cover multi-store + workflow surfaces that move beyond single-store sales. Module D (Distribution) handles inter-store transfers + multi-location inventory. Module J (Forecast / Order) handles vendor management + replenishment ordering. Both flow through the **Document omnibus** — transfers are `DOC_TYP: XFER`, POs are `DOC_TYP: PO/PREQ/RECVR/RTV` — so this phase reuses the Phase 1 Module T adapter pattern with type-routing extensions.

**Modules in this phase:**
- **D — Distribution** (inter-store transfers, multi-location inventory, vendor-item relationships)
- **J — Forecast / Order** (POs, purchase requests, receivers, returns-to-vendor, vendor master)

**Sub-phase sequence:** 3a (D) → 3b (J), serial. Document type-routing for D unblocks J.

## Pre-flight reading

1. SDD §6.7 (D), §6.9 (J)
2. `Brain/wiki/ncr-counterpoint-document-model.md` §"DOC_TYP taxonomy" — confirm XFER, PO, PREQ, RECVR, RTV codes against actual sample data when sandbox available
3. Counterpoint endpoint docs: InventoryLocations, Inventory_ByLocation, Items_ByLocation, VendorItem, Document
4. `Brain/wiki/garden-center-operating-reality.md` §"vendor / grower side" — heterogeneous vendor mix, cash-payment receivers, item-code drift

## Scope clarification questions ALXjr asks BEFORE code

1. **Document type-code confirmation** — sample payloads from a sandbox or test DB to confirm DOC_TYP codes: `XFER`, `PO`, `PREQ`, `RECVR`, `RTV`. Currently inferred from Workgroup next-number generators.
2. **Transfer in-flight representation** — does Counterpoint represent in-flight transfers (sent from store A, not yet received at store B)? Search Document fields + check sample payload.
3. **PO + Receiver linkage** — when a Receiver is created against a PO, how is the link captured? Document.PS_DOC_HDR_ORIG_DOC[] (parallel to return-vs-sale link)?
4. **Vendor onboarding ad-hoc** — garden-center reality is mid-season vendor adds. Adapter should accept new vendors without prior provisioning. Confirm.
5. **Cash-vendor-receipt classification** — when staff record a paper invoice as a Receiver with PayCode CASH, the document looks like a normal receiver. Module Q later needs to classify this differently. Capture the metadata path now.

## Operating procedure

### Sub-phase 3a — Module D (Distribution)

1. Read SDD §6.7 + Document model wiki + InventoryLocations / Inventory_ByLocation endpoint docs
2. CRDM mapping: `Workflows.transfers` (Document XFER type), `Things.inventory_by_location` (snapshot), `Places.inventory_locations`
3. TSP adapter: type-route on Document polling to detect XFER documents → Workflows.transfers. Inventory snapshots from Inventory_ByLocation polled hourly (not cached server-side). InventoryLocations rarely changes — daily.
4. MCP tool surface: `get_transfers(date_range, source?, dest?, status?)`, `get_inventory_by_location(item_id)`, `get_low_stock_locations(threshold?)`, `get_inventory_locations()`
5. Test: fixture suite with multi-store transfer scenarios + edge cases (in-flight transfers, partial receives, transfer reversals)
6. Wiki: update `Brain/wiki/canary-module-d-distribution.md` with Counterpoint mapping
7. Founder review gate

### Sub-phase 3b — Module J (Forecast / Order)

1. Read SDD §6.9 + Document model wiki § PO / PREQ / RECVR / RTV types + VendorItem endpoint
2. CRDM mapping: `Workflows.purchase_orders` (PO + PREQ types), `Workflows.receivers` (RECVR type), `Workflows.returns_to_vendor` (RTV type), `People.vendors` (from VendorItem and Document.ITEM_VEND_NO)
3. TSP adapter: type-route on Document polling to detect PO/PREQ/RECVR/RTV → respective Workflows entities. VendorItem polled daily. **No replenishment-engine endpoint** — replenishment recommendations stay UI-only or external.
4. MCP tool surface: `get_open_purchase_orders(vendor?, status?)`, `get_receivers(date_range)`, `get_vendor(vendor_id)`, `get_vendor_items(vendor_id)`, `get_pending_returns_to_vendor()`
5. Test: fixture suite covering vendor-document workflows + ad-hoc vendor onboarding + cash-vendor-receipt classification
6. Wiki: update `Brain/wiki/canary-module-o-orders.md`
7. Founder review gate

## Cross-cutting work (within this phase)

- **Document type-routing** as a first-class concept — the polling loop reads Document, dispatches to Workflows.transfers / purchase_orders / receivers / returns_to_vendor / sales (Phase 1 T) based on DOC_TYP. Pattern documented + reusable.
- **Vendor master deduplication** — if same vendor appears with slight variations (different vendor numbers across store companies in multi-company deployments), adapter needs to handle. Default: preserve as-is, flag for analytics layer.
- **Cash-vendor-receipt metadata path** — preserve PayCode + original-document linkage so Module Q can classify legitimate cash payments differently from fraud-pattern signals.

## Out of scope

- Module E (Execution) — confirmed absent from Counterpoint REST per SDD §6.13. Separate effort.
- Replenishment-engine integration — UI-only in Counterpoint; if customers need automated replenishment, license a forecasting tool (external) or build native (Canary option d future).
- Vendor portal / vendor-side communication — Counterpoint's API doesn't expose vendor-facing surfaces; out of scope.

## Acceptance criteria

Per module:
- [ ] CRDM mapping documented + tested
- [ ] Document type-routing handles all relevant DOC_TYP codes
- [ ] MCP tool surface exposed
- [ ] Fixture suite covers happy path + edge cases (in-flight, ad-hoc onboarding, cash-vendor-receipt)
- [ ] Wiki updated

Phase-level:
- [ ] Module D + Module J complete
- [ ] Document type-routing pattern documented as reusable concept
- [ ] DOC_TYP code list confirmed against sandbox data (or marked as pending)

## Risks (Phase 3 specific)

- **DOC_TYP code list still partial** — five inferred (XFER, PO, PREQ, RECVR, RTV); actual codes need sandbox confirmation. Risk: discovery during Phase 3 surfaces additional types not anticipated.
- **In-flight transfer modeling** — without confirming Counterpoint's in-flight semantics, adapter design might be incomplete. Mitigate: inspect transfer-sample data once sandbox is up.
- **Vendor data quality variance** — garden-center vendor mix produces noisy data. Adapter must flag-and-ingest, not reject; tracking + reconciliation become Module Q + analytics-layer concerns.

## Reporting cadence

Sub-phase checkpoint at 3a, 3b. Founder review.

## Related

- `docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md` — §6.7, §6.9
- `docs/superpowers/plans/2026-04-25-ncr-counterpoint-spine-build.md` — Phase 3 row
- `Brain/dispatches/2026-04-25-ncr-counterpoint-catalog-modules.md` — Phase 2 (prerequisite)
- `Brain/wiki/ncr-counterpoint-document-model.md` — Document omnibus
- `Brain/wiki/garden-center-operating-reality.md` — vendor-mix domain reality

---

**Dispatch author:** Senior ALX (laptop), 2026-04-25
**Executor:** Laptop-side Claude Code
**Review gate:** Founder reviews pre-flight summary, scope answers, each sub-phase output
