---
title: The Shelf-Edge Label — Compile Target of the SRD Canonical
type: analytical-memo
status: v0.1
tags: [srd, shelf-edge-label, sel, retailspine, canonical-validation, ordering-gate, third-branch, crdm, sysrepublic, f-and-e, kipa, ikb, rms, storeline]
created: 2026-04-24
updated: 2026-04-24
related:
  - "[[retail-integration-spine]]"
  - "[[intactix-canonical-validation]]"
  - "[[third-branch]]"
  - "[[Brain/projects/Secure|Secure MOC]]"
sources:
  - Brain/raw/inbox/srd-shelf-edge-label-interfaces.md  (S039 + S101 combined intake)
  - Brain/raw/inbox/SRD/Interfaces/S039,S041.5,S047,S052.5,S057/S039 - SEL Range and Display from SR to IDS Interface Spec 1.2.doc
  - Brain/raw/inbox/SRD/Interfaces/S093,S095,S100,S101,S102/s101 srd sel (rpp to ids) interface spec 0.2.doc
  - Brain/raw/inbox/SRD/- Store Range/SEL triggers - Spreadsheet - v.1 - 7 Nov.xls  (not yet extracted)
  - Brain/raw/inbox/SRD/- Store Range/SEL individual triggers v.1 - 7 Nov.vsd  (not yet extracted)
last-compiled: 2026-04-24
needs-review: 2026-05-08
---

# The Shelf-Edge Label — Compile Target of the SRD Canonical

> **Provenance boundary.** This memo cites the founder-operator era F&E / Kipa SRD implementation and the CRDM / Sysrepublic relationship as ground-truth evidence. That lineage is private provenance and **does not** carry forward to CATz or any customer-facing blueprint. Public artifacts present the shelf-edge label as an architectural pattern, not as a deployment memory.

**Governing thesis.** The shelf-edge label (SEL) is the compile target of the retail canonical. Every prefix family — planogram (S), merchandising (C), range and display (SRD flat-file), store-level facing overrides (RPP) — must reconcile on a single physical rail tag, daily, in every store, for the canonical to be coherent. If the label prints correctly, the canonical compiles. If the label cannot be printed — missing planogram, missing capacity, missing pack, inconsistent price — the canonical has failed at the one point retail cannot hide. The shelf-edge label is therefore not just one more interface; it is the reconciliation surface that validates every other interface by construction. RetailSpine inherits this property and should expose "label-compilable" as a first-class derived attribute on the canonical.

## Executive summary

| Role in the canonical | Carrier | RetailSpine surface |
|---|---|---|
| Planogram source of truth | JDA Intactix / IKB | S-prefix (planogram, capacity, facings geometry) |
| Range and Display deltas | Store Range (SR) flat files | S039-family SEL delta emitter |
| In-store facing correction | RPP / Product Position | S101 emergency-facings feed |
| Merchandise master | RMS (Retek; later Oracle Retail) | C-prefix (product, UPC, description) |
| Price master | RMS | C010 price/cost leaf |
| Reconciliation target | IDS `SKUItemInStore` | Canonical "product × store × SEL-state" row |
| State-machine of reason | `SRDSEL_Trans.UpdateType ∈ {FULL, RANGE, FACINGS, EMERGENCY}` | Reason-code set on the canonical reconciliation event |
| Physical label delivery | Storeline + **CRDM** (Sysrepublic product) | Label-print capability, out-of-band from the canonical catalog |

**One-line claim:** the shelf-edge label is the lowest-latency, highest-trust operator-visible signal that the retail canonical has reconciled. Every other signal — dashboards, exception reports, reorder suggestions — depends on a data surface the operator cannot physically touch. The label hangs on the rail.

## I. Why the label is load-bearing

Three properties of the shelf-edge label make it the reconciliation surface, not just a downstream artifact.

**1. It is the physical compile target.** The label requires the intersection of planogram, merchandising, price, range, display, pack config, and store-level override to be resolved into a single printable record. If any one input is missing or inconsistent, the label either prints wrong, prints blank, or fails to print. A retailer cannot hide from a wrong label the way they can hide from a wrong dashboard.

**2. It is observer-addressable at scale.** Every store manager, associate, and customer can see a shelf-edge label. The signal surface is the retail physical store. No specialised instrumentation is required to detect a label problem — the aisle itself is the sensor.

**3. It is the last physical artifact the canonical produces.** All upstream work — item setup, planogram authoring, range decision, price management, replenishment calc — resolves to the label. Anything that cannot resolve to a correctly printed label is by definition not part of the canonical the store operates against.

The ordering gate (see `[[intactix-canonical-validation]] §III.4`) and the label-compilability property are two sides of the same discipline. The ordering gate prevents items from entering the catalog before they have planogram, capacity, and pack. Label-compilability verifies at the shelf that the reconciliation held. The canonical *enters* through the gate and *exits* to the label; the loop is closed when both endpoints agree.

## II. The end-to-end data path

```
┌─────────────────────┐
│  IKB (JDA Intactix) │  — planogram source of truth
│  Space Planning +   │     (S-prefix canonical hub)
│  Floor Planning     │
└──────────┬──────────┘
           │ full planogram refresh per store on any change
           ▼
┌─────────────────────┐
│  Store Range (SR)   │  — delta computation, delta emitter
│  (application layer │     (NOT the integration layer — per
│   — business logic) │      architectural rule, logic is here
└──────────┬──────────┘      and only here)
           │ daily batch → two flat files: SEL Range + SEL Display
           ▼
┌─────────────────────────────────────────────┐
│  Integration Layer (SSIS)                   │
│  S039 — daily batch                         │    ┌─────────────────┐
│  S101 — near-real-time emergency facings ◄──┼────│ RPP (Product    │
│  (integration layer is "dumb plumbing")     │    │ Position) —     │
└──────────┬──────────────────────────────────┘    │ in-store facing │
           │                                       │ correction      │
           ▼                                       └─────────────────┘
┌───────────────────────────────────────────────┐
│  IDS  /  RIDS v7.2                            │
│                                               │
│  SKUItemInStore  (reconciliation target)      │
│  ├─ SRD "Range" attrs: PlanogramID,           │
│  │  ProductStoreStatus, ProductStoreRangeStatus│
│  ├─ SRD "Display" attrs: ShelfFacingsQty,     │
│  │  MultiLocationInd, SELQty                  │
│  └─ non-SRD: WIC/FoodStamp/UoM/desc (from RMS)│
│                                               │
│  SRDSEL_Trans   (reason-code state machine)   │
│  └─ UpdateType ∈ {FULL, RANGE, FACINGS,       │
│                   EMERGENCY}                  │
└──────────┬────────────────────────────────────┘
           │ C023TR / S092 — scheduled extract, filtered by UpdateType
           ▼
┌───────────────────────────────────────────────┐
│  Storeline (store-facing ops)                 │
│  ├─ SRD attributes (via S039 / S101 / S092)   │
│  └─ RMS attributes — price, tax, description  │
└──────────┬────────────────────────────────────┘
           │ user-initiated group-print OR emergency-facings auto-print
           ▼
┌───────────────────────────────────────────────┐
│  CRDM  (Sysrepublic)                          │
│  ─ Shelf-edge label delivery product          │
│  ─ Execution engine for physical print        │
└──────────┬────────────────────────────────────┘
           │
           ▼
   ┌─────────────────┐
   │  SHELF-EDGE     │   ← the compile target.
   │  LABEL on rail  │     if this is wrong, the canonical is wrong.
   └─────────────────┘
```

Two observations about this topology:

**A. The integration layer is intentionally dumb.** Tesco's architectural rule — *"avoid placing any business logic in integration layer processing"* — means the canonical definition lives in Store Range (the application) and in the target schema (IDS). SSIS shuttles bytes. This is the correct shape for MCP-native exposure: the MCP server mediates the canonical schema; no agent-side business logic sits in the transport.

**B. The reconciliation has two latencies.** S039 is overnight batch for bulk label updates. S101 is near-real-time for store-initiated corrections. Both feed the same target table, but `SRDSEL_Trans.UpdateType` preserves the reason distinction downstream. RetailSpine should adopt this two-latency pattern as a canonical property of SEL-class reconciliation events.

## III. The reason-code state machine

`SRDSEL_Trans.UpdateType` is a four-value enum that carries the *why* forward to label-print decisioning:

| Value | Written by | Semantic |
|---|---|---|
| **FULL** | S039 batch | Complete refresh of SRD attributes for a product × store |
| **RANGE** | S039 batch | Range-only change (status, planogram assignment) |
| **FACINGS** | S039 batch | Display-only change (facings wide, SELQty, multi-location, shelf-ready packaging) |
| **EMERGENCY** | S101 near-real-time | In-store-initiated correction of a single facings value |

This is a compact, deployable canonical artifact. RetailSpine should codify it as the **SEL Reconciliation Reason** enum on the canonical reconciliation event. The enum has three useful properties: (1) it distinguishes source latency (batch vs real-time), (2) it distinguishes scope of change (full / range-only / display-only / single field), and (3) it distinguishes authoring authority (central vs in-store).

The Authority Level patch called out in `[[intactix-canonical-validation]] §III.2` is the dimension this enum operates against. EMERGENCY is the label-delivery expression of in-store Authority; FULL / RANGE / FACINGS are expressions of central Authority. The two patches compose.

## IV. Why CRDM matters beyond the label

CRDM (Sysrepublic's product) was the physical-print execution engine at F&E. That role — out-of-band label delivery on top of the canonical catalog — is structurally the same role the Sysrepublic LP platforms later played over D-prefix movement events at Secure-era customers: **out-of-band consumption of a canonical data surface, feeding a capability the retailer treats as table-stakes operational infrastructure**.

The relationship pattern recurs across a decade:

| Era | Canonical surface | Sysrepublic product | Retailer |
|---|---|---|---|
| ~2007–2013 | IDS `SKUItemInStore` + `SRDSEL_Trans` | **CRDM** — shelf-edge label delivery | Tesco F&E / Kipa |
| ~2010–2019 | POS journal, D-prefix movement events, J010 SOH | **xBR / Secure-era LP platforms** | multiple grocery, including Southeastern Grocers |

In both cases Sysrepublic consumed a canonical surface a central team maintained, and produced a capability the store directly felt — labels or shrink attribution. This is the commercial pattern the Third Branch LP wedge inherits, and the reason the Sysrepublic relationship has depth the 2016 xBR engagement alone does not explain.

**See also:** `[[Brain/projects/Secure|Secure MOC]]` — the Secure lineage should note CRDM / F&E as the prior-art entry point to the Sysrepublic relationship, not the 2016 SEG xBR engagement.

## V. What RetailSpine should codify

Three concrete additions fall out of the SEL analysis:

**1. `Product.label_compilable[store_id]` as a derived Boolean.**
Symmetric to the ordering-gate attribute (`Product.orderable_at_location[store_id]`). Defined as:

```
label_compilable(product, store) :=
    Planogram(product, store) ≠ null
  ∧ Capacity(product, store) > 0
  ∧ Product.pack_config reconciles shelf geometry
  ∧ Product.price(store) ≠ null
  ∧ Product.description ≠ null
  ∧ Product.uom ≠ null
  ∧ StoreRange.status(product, store) ∈ {Standard, New}
```

If `orderable_at_location` is the entry gate, `label_compilable` is the exit gate. Any agent that mutates a product × store record should see both as preconditions for a valid state transition.

**2. `SEL Reconciliation Reason` as a canonical enum.**
Lift the F&E `UpdateType` set verbatim — FULL / RANGE / FACINGS / EMERGENCY — as the RetailSpine reason-code for SEL-class reconciliation events. The enum becomes an MCP-addressable filter: *"give me every FACINGS-class reconciliation in the last 24 hours where `label_compilable` resolved to false"* is the sort of query the LP agent and the merchandise agent both want.

**3. Two-latency reconciliation as a canonical property.**
Expose the SEL reconciliation event with explicit `latency ∈ {batch, real-time}`. The S039 / S101 pattern is the reference: batch for bulk central authoring; real-time for single-cell in-store correction. Agents should be able to subscribe to either or both.

Each addition is small, each is directly named in the 2007 F&E spec, and each becomes a sharper MCP-native interface against what the SRD canonical already describes.

## VI. How the label closes the Third Branch loop

Stated at the thesis altitude (see `[[third-branch]]`):

- The **bubble** observes what is actually on the shelf (physical facings, tag presence, pricing consistency).
- The **spine** (RetailSpine) carries the canonical definition of what *should* be on the shelf.
- The **agents** reconcile the two, operating the `SEL Reconciliation Reason` state machine continuously.
- The **label** is the printed proof of reconciliation — the 2026 equivalent of what Storeline + CRDM compiled in 2007, but now continuous, bubble-verified, and agent-operated.
- **Sats** price the reconciliation — each successful label-compile is attributable, each failure is economically measurable.

The Third Branch thesis is, at this altitude, an argument that the 2007 F&E discipline was correct at the shelf and wrong everywhere else it ran. The shelf part always worked — the rail tag compiled or it didn't, and the operators acted on that signal. Extending that same reconciliation discipline into the customer domain, the LP domain, and the merchandising-feedback domain is what the bubble + MCP + agents make possible that the 2007 stack could not.

The label was the proof then. It remains the proof.

---

*Sources: intake `Brain/raw/inbox/srd-shelf-edge-label-interfaces.md`; raw specs S039 v1.2 (Prasanth Dukaram, 22 May 2007) and S101 v0.2 (Andy Barker, 14 Sep 2007) under `Brain/raw/inbox/SRD/Interfaces/`. Canonical grammar from `[[retail-integration-spine]]`. Companion memos: `[[intactix-canonical-validation]]`, `[[third-branch]]`. Secure lineage: `[[Brain/projects/Secure|Secure MOC]]`.*
