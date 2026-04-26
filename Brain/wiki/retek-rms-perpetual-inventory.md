---
title: Retek RMS — the Perpetual-Inventory Movement Ledger
type: canonical-substrate
status: v0.1
tags: [retail, rms, retek, oracle-retail, perpetual-inventory, stock-ledger, rib, rdm, canonical, three-canonical, branch-b]
created: 2026-04-24
updated: 2026-04-24
related:
  - "[[third-branch]]"
  - "[[intactix-canonical-validation]]"
  - "[[tesco-technical-library]]"
  - "[[srd-shelf-edge-label]]"
  - "[[katz-scm-2003-archetype]]"
  - "[[bp-consulting-library-1997-1999]]"
sources:
  - Brain/raw/.extract/Other Retek Decks/rms-110-ug.pdf.md
  - Brain/raw/.extract/Other Retek Decks/Retek RIB.Ahlens Solution.doc.md
  - Brain/raw/.extract/Other Retek Decks/Pages from rib-101-intg.pdf.md
  - Brain/raw/.extract/Other Retek Decks/Retek.RMS to RDM Interfaces.Ahlens.xls.md
  - Brain/raw/.extract/Other Retek Decks/Retekv10-Modules.Key Blocks.doc.md
  - Brain/raw/.extract/Other Retek Decks/resa-110-ug.pdf.md
  - Brain/raw/.extract/Other Retek Decks/reim-100-ug.pdf.md
  - Brain/raw/inbox/kroger-retek-project-sam-xls.md
last-compiled: 2026-04-24
needs-review: 2026-05-08
---

# Retek RMS — the Perpetual-Inventory Movement Ledger

> **Governing thesis.** The merchandising canonical — the thing the three-canonical story names as "RMS" or "Oracle Retail" alongside SRD and TTL — is not, at its core, an identity master. It is a **perpetual-inventory movement ledger**: every receipt, transfer, adjustment, cycle count, sale, shrink, return-to-vendor, and allocation posts as a signed movement against on-hand, with a cost and retail value attached, keyed to `item × location × time`. The identity master (SKU, UPC, hierarchy, supplier links) is a *supporting attribute set* of the items the ledger moves. SRD's ordering gate and TTL's pack-copy compile gate are both gating *against the ledger*: neither the shelf nor the label can commit until the ledger confirms the item exists, has a cost method, and is conserved through its next movement. Name the ledger and the three-canonical model has a substrate. Leave it unnamed and every other claim in the framework floats.

## I. What the ledger actually is

RMS's Chapter 9 is called *Financial Management* and its central object is the **stock ledger** — literally, the book of stock. From `rms-110-ug.pdf.md`:

> "Both the quantity and value of the stock on hand are adjusted in the stock ledger." (L11722, L11789)
>
> "In the stock ledger, the adjustment is recorded as a transfer between stock on hand and unavailable inventory. No adjustment is made to the stock value." (L11725–11727)
>
> "Stock ledger transactions are written to move the inventory amount associated with an item from the old department, class, and subclass to the new." (L5960–5961)
>
> "Value added taxes are reflected in the stock ledger when the retail method of accounting is used." (L2587)

Every canonical activity — even a *reclassification* that doesn't physically move a carton — generates a stock-ledger transaction because the ledger is the integrity surface of the merchandising system. If the movement does not post, the quantity and value of on-hand fall out of consensus with every downstream system that depends on them (OTB, allocation, replenishment, financial close, shrink budgeting).

### Invariants

Three invariants govern the ledger, all of them visible in the user guide:

1. **Conservation of stock.** Every movement is a signed pair: a decrement on one side, an increment on the other, or a decrement with a matching shrink/adjustment reason. Stock cannot appear or disappear without a posted reason code. RMS enforces this with mandatory reason codes on inventory adjustments: *"When adjusting total stock on hand, you must select a reason for the adjustment. The reason indicates why the total stock on hand must be adjusted."* (`rms-110-ug.pdf.md` L11733–11734).
2. **Cost-method consistency.** The ledger carries both quantity and value. RMS supports Retail Method and Cost Method; every posted movement carries the cost treatment that matches the department's method, and VAT is reflected where retail method is in force (L2587–2588). Landed cost, consignment, and concession departments are each special cases of this invariant — consignment and concession items *"are ordered, invoiced and recorded in the stock ledger"* with accounts-receivable/payable suppressed (L2233–2238).
3. **Cycle-count reconciliation.** Physical reality reconciles to the ledger, not the other way around. A stock count takes a *snapshot*: *"Immediately prior to the scheduled date of the physical stock count, a snapshot is taken of the stock on hand... the results of a physical count are used to adjust the quantity of the stock on hand."* (`rms-110-ug.pdf.md` L14118–14120, L14106–14111). Unit-and-dollar counts write back to the ledger; unit-only counts adjust only quantity.

## II. The canonical movement types

The ledger's native verbs, extracted from the RMS TOC and inventory chapters (`rms-110-ug.pdf.md` L270–328, L9722–9732):

| Movement | Origin | Signed effect | Posts to |
|---|---|---|---|
| **Receipt (PO / BOL)** | Supplier → store/WH | `+qty, +cost` at location | Stock on hand; landed cost capitalized |
| **ASN / receiving** | Supplier → store/WH | `+qty` pending | In-transit; converts to on-hand at receipt |
| **Transfer (intra-company)** | Loc A → Loc B | `-qty` A, `+qty` B | Both locations' on-hand + up-charges |
| **Allocation** | WH → stores (1:N) | Reserves qty, generates stock orders | Pre-movement hold |
| **Sale (POS)** | Store → customer | `-qty, -cost, +retail` | Cogs, sales, stock on hand |
| **Return (customer)** | Customer → store | `+qty, reverse sale` | Salable or unavailable depending on reason |
| **RTV (Return to Vendor)** | Store/WH → supplier | `-qty, cost reversal` | Shrink / supplier debit (L10226–10232) |
| **Inventory adjustment** | In-place | `+/-qty` with reason code | Stock on hand *or* unavailable inventory (L11716–11727) |
| **Cycle count / stock count** | Physical reconcile | delta against snapshot | Writes count-adjustment tx to ledger (L14106–14120) |
| **Shrink** | Derived / adjustment | `-qty, -cost` with shrink reason | Shrink budget vs actuals in stock-ledger (L14010–14012) |
| **Reclassification** | Hierarchy change | value move across dept/class/subclass | Stock ledger, not physical (L5960–5963) |
| **Stock ledger close** | Period end | Aggregated movement posting | GL, OTB, finance (L14015, L6209–6213) |
| **VAT posting** | Per movement | VAT portion of cost/retail | Tax accrual alongside stock ledger (L2557–2588) |

Every capability in the broader suite reads or writes one of these verbs. That is the tangible form of the claim.

## III. RIB — the movement bus

RMS writes the ledger; **RIB (Retek Integration Bus)** is the pre-SOA, pre-Kafka message bus that publishes those movements to every downstream consumer. The Ahlens solution document (`Retek RIB.Ahlens Solution.doc.md`) states it plainly:

> "RIB 10.2 contains over 30 message families... Merchandising – Items, Locations, Hierarchies, Purchase Orders, Vendors, Allocations, Transfers, User Defined Attributes. Distribution Management – ASN, Appointments, Return to Vendor, Space Locations, Receipts (Bill of Lading), Stock Order Status, Order Release, Inventory Adjustments, Inventory Balances. Customer Order Management – Order reserve, Sale, Return. Externally published – Chart of Accounts, Freight Terms, Currency Rates, Vendors, Payment Terms." (L51–60)

The RIB 10.1 Integration Guide (`Pages from rib-101-intg.pdf.md`) names the topology:

> "A single JMS Intelligent Queue Manager. One feature of the RIB is the Error Hospital subsystem used to store and retry messages that have processing problems." (L8–10)

And enumerates publisher/subscriber pairings in a table that is, functionally, the movement catalog:

> "Transaction Data: Inventory Adjustments (RDM → RMS), Customer Sale (RCOM → RMS), Purchase Order (RMS → RDM), Receiving (RDM → RMS), RTV (RDM → RMS), Stock Order (RMS → RDM), Customer Return (RDM → RMS)..." (L344–476)

Two structural points land here. First, RMS is the **authoritative publisher of ledger writes**; RDM (warehouses) and RCOM (customer orders) publish movement *events* that RMS subscribes to and commits to the ledger. Second, the Error Hospital is a first-class architectural component: a movement that fails to subscribe is quarantined for retry, not dropped, because ledger integrity is non-negotiable. This is the 2002 retail-industry instantiation of what is now called **event-driven architecture with a dead-letter queue** — fifteen years ahead of the vocabulary.

## IV. RDM — the analytics flattening

The Ahlens RMS → RDM interface spec (`Retek.RMS to RDM Interfaces.Ahlens.xls.md`) is terse and revealing. Nine channels, each a projection of the ledger into a reporting shape:

| Channel | Example tables | Ledger projection |
|---|---|---|
| Item | Item_SOH, Item_Loc_Hist, Item_Forecast | Current on-hand + movement history |
| Purchase Order | Alloc_Header, Orderhead, Ordersku | In-flight incoming movement |
| Merchandise | Division → Subclass, Dept/Class Forecast & History | Hierarchy rollup of movement facts |
| Organisation | Store, Warehouse, Districts, WH_Store_Assignment | Location dimension |
| Promotions | PromHeader, PromSku, PromStore | Retail-side events driving sales movement |
| Supplier | Sups, Item_Supplier, Freight | Inbound-movement source |
| Invoice | FIF_Invoice_Header/Detail | Cost reconciliation against receipts |
| VAT | VAT_Codes, VAT_Item, VAT_History | Tax layer on movement value |
| Currency | Currency_Rates, Currencies_PP_Rules | Valuation layer |

The data mart is not a separate truth. It is the ledger flattened for reporting, with dimensions (item, location, merch hierarchy) explicit and facts (SOH, history, forecast) time-bound. Every row is derivable from a posted movement.

## V. The module map — every capability as a ledger operation

Retek v10's "Full Suite," as IBM catalogued it in `Retekv10-Modules.Key Blocks.doc.md` L1–263:

| Module | Expansion | Ledger role |
|---|---|---|
| **RMS** | Merchandising System | Owns the ledger; all movements commit here |
| **RDM** | Retek Distribution Mgmt | Publishes ASN/receipt/RTV/adjustment movements |
| **RCOM** | Customer Order Mgmt | Publishes customer sale/return/reserve movements |
| **ReSA** | Sales Audit | Cleans POS transaction log → authorised sales movements to RMS (*"seamless, integrated flow of data from the point-of-sale to major Retek and other external software"* — `resa-110-ug.pdf.md` L255–256) |
| **ReIM** | Invoice Matching | Reconciles supplier invoice → receipts at PO cost; writes cost variance to ledger (*"attempts to automatically match invoices with receivers within user-defined tolerance limits"* — `reim-100-ug.pdf.md` L213–214) |
| **RPM** | Price Management | Writes price/markdown events that revalue on-hand in the ledger |
| **Retek Allocation** | Allocation engine | Reads SOH, writes stock-order movements (RMS→RDM) |
| **RDF / RRO / AIP** | Forecasting + Replenishment | Reads movement history (Item_Loc_Hist, demand), writes order recommendations |
| **Retek POS (RPOS / RSS)** | Point of sale | The *origin* of the sales movement at the store |
| **Range & Space** | Retek's planogram/range module | Reads item master; gates which items the ledger should expect to see move |
| **RTM** | Trade Management | Writes import-cost components into landed-cost layer of ledger |
| **ARI** | Active Retail Intelligence | Subscribes to movement events, fires exception workflows |
| **VMI** | Vendor Managed Inventory | Vendor writes replenishment against ledger-exposed SOH |

Every line of that inventory is either a producer of ledger writes, a consumer of ledger reads, or a reconciliation against ledger state. The ledger is not one module among many; it is the substrate across which the modules communicate.

## VI. The three-canonical correction

Restate the claim with the substrate named:

```
        ┌──────────────────────┐    ┌──────────────────────┐
        │   TTL — spec         │    │   SRD — planogram    │
        │   what the product   │    │   where the product  │
        │   is                 │    │   is                 │
        │   (compile gate)     │    │   (ordering gate)    │
        └──────────┬───────────┘    └───────────┬──────────┘
                   │ gates for                  │ gates against
                   │ items the ledger           │ the ledger
                   ▼                            ▼
    ┌──────────────────────────────────────────────────────┐
    │  RMS — perpetual-inventory movement ledger           │
    │  (identity master attached)                          │
    │                                                      │
    │  Movements: receipt · transfer · adjustment · cycle  │
    │  count · sale · shrink · RTV · allocation · reclass  │
    │  · period close                                      │
    │                                                      │
    │  Invariants: conservation · cost-method consistency  │
    │  · cycle-count reconciliation                        │
    │                                                      │
    │  Bus: RIB (30+ message families, Error Hospital)     │
    │  Mart: RDM (ledger flattened for reporting)          │
    └──────────────────────────────────────────────────────┘
```

**SRD's ordering gate gates against the ledger.** An item is not orderable at a location until the planogram assigns it, capacity is set, and the pack configuration reconciles — meaning: the ledger is ready to receive the item's receipts and post its movements without violating conservation or cost-method consistency. The gate is upstream of the first receipt.

**TTL's pack-copy compile gate gates for items the ledger holds.** A shelf-edge label cannot compile until the ledger confirms the item is live at the location with a known cost, a known retail, a known UoM. The gate is downstream of the last specification write but upstream of physical merchandising.

Both gates are valid *because* the ledger is authoritative. Take the ledger away and the gates have nothing to gate against.

## VII. Cross-references

- [[third-branch]] — the three-canonical framing carried the ledger implicitly; this article makes it load-bearing.
- [[intactix-canonical-validation]] — Intactix's ordering gate is the planogram-side enforcement; the thing it enforces *on* is this ledger.
- [[tesco-technical-library]] — TTL's compile gate produces physical labels only for ledger-confirmed items.
- [[katz-scm-2003-archetype]] — the 2003 mid-market drug/pharmacy RFP evaluated Retek against four other vendors; the ledger-plus-bus pattern is the shape being compared.
- [[bp-consulting-library-1997-1999]] — Cluster B `980128ib.doc` investment-buying/MRP smoking gun is a primary-source indictment of SAP's inability to provide ledger-substrate-grade replenishment in 1998; Retek's architecture is the counter-example.
- `Brain/raw/inbox/kroger-retek-project-sam-xls.md` — IBM BIS Kroger Retek CRP engagement, 2001, sibling deployment context.

---

*Primary sources: `/Users/gclyle/GrowDirect/Brain/raw/.extract/Other Retek Decks/rms-110-ug.pdf.md`, `.../Retek RIB.Ahlens Solution.doc.md`, `.../Pages from rib-101-intg.pdf.md`, `.../Retek.RMS to RDM Interfaces.Ahlens.xls.md`, `.../Retekv10-Modules.Key Blocks.doc.md`, `.../resa-110-ug.pdf.md`, `.../reim-100-ug.pdf.md`. All extracted via the content engine on 2026-04-24. Retek v10.x user-guide line numbers as cited.*
