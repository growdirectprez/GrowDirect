---
date: 2026-04-24
type: raw
source:
  - Brain/raw/inbox/SRD/Interfaces/S039,S041.5,S047,S052.5,S057/S039 - SEL Range and Display from SR to IDS Interface Spec 1.2.doc
  - Brain/raw/inbox/SRD/Interfaces/S093,S095,S100,S101,S102/s101 srd sel (rpp to ids) interface spec 0.2.doc
original_source: Tesco Operating Model — F&E / Kipa SRD implementation, 2007
authors:
  - Prasanth Dukaram (S039)
  - Andy Barker (S101)
dates:
  - 2007-05-22 (S039 v1.2)
  - 2007-09-14 (S101 v0.2)
project: third-branch
tags: [srd, shelf-edge-label, sel, f-and-e, kipa, turkey, jda, ikb, store-range, ids, storeline, crdm, sysrepublic, ordering-gate, canonical-validation]
status: unprocessed
---

# SRD Shelf-Edge Label Interfaces — S039 (daily batch) + S101 (emergency facings)

## Source

Two Tesco Operating Model (TOM) integration specifications lifted from the F&E / Kipa SRD corpus:

- **S039** — *SEL Range and Display from SR to IDS*, v1.2, 22 May 2007, Prasanth Dukaram. Daily batch. 19 KB text.
- **S101** — *Space, Range and Display SEL Emergency Facings — RPP to IDS*, v0.2, 14 Sep 2007, Andy Barker. Near-real-time. 14 KB text.

Extracted via `soffice --headless --convert-to txt` from the original `.doc` files under `Brain/raw/inbox/SRD/Interfaces/`.

## Context for intake

The shelf-edge label (SEL) is the physical reconciliation surface of the F&E / Kipa SRD canonical. Every prefix family collides on a single printed rail tag: planogram (S-prefix), merchandising and price (C-prefix and RMS), range and display indicators (SRD flat files), store-level facing overrides (RPP). The label is what Storeline prints, consumed downstream by **CRDM** — Sysrepublic's product for shelf-edge label delivery at F&E. CRDM is the precursor and relationship-entry to what later became the Sysrepublic / Appriss / IBM loss-prevention lineage the founder carried into Secure.

**This interface is for US and Turkey implementation.** That line is in S039 v1.2 verbatim. The international port of the SRD canonical is designed into the interface spec at v1.2, not retrofitted post-F&E.

## Extracted content — S039 (daily batch)

### Scope and purpose

Extracts Range and Display indicators for a product on a store, to be printed on the shelf edge labels, from Store Range (SR) as two flat files, loaded into the IDS via SSIS. Delta upload. Store Range owns delta computation (integration layer carries no business logic — Tesco strategy). Storeline consumes via C023.

### Upstream source

IKB (JDA) sends full planogram refresh for a store whenever any one planogram changes, via Interface 78. SR processes and computes the delta.

### Source flat files (SR outbox)

**SR_SELRange_YYYYMMDDHH24miss.txt** (84-byte records):
- Store Number — `Integer(10)`, retail outlet number
- Product Number — `Char(25)`, Tesco item number of base product
- Display Group — `Char(30)`
- Planogram ID — `Char(16)`
- Range Indicator — `Char(1)` ∈ {0 = Not In Range, 1 = In Centrally proposed range, 2 = In Local Range}
- Product Status — `Char(1)` ∈ {0 = Standard, 1 = New, 2 = Discontinued}

**SR_SELDisplay_YYYYMMDDHH24miss.txt** (58-byte records):
- Store Id — `Integer(10)`
- Product — `Char(25)`
- Number of facings wide — `Integer(10)`
- Number of default labels — `Integer(10)`
- Multi located indicator — `Char(1)`
- Shelf ready packaging — `Char(1)`

Both files carry header (RECTYPE=0, RUNDATE, RUNTIME) and trailer (RECTYPE=9, RECCOUNT) records.

### Target — IDS table `SKUItemInStore` (RIDS v6)

| Field | Type | Source |
|---|---|---|
| SKUID | Varchar(25) | key |
| StoreID | Int | key |
| FoodStampInd | Char(1) | non-SRD |
| WICInd | Char(1) | non-SRD |
| MeasureOfEach | Numeric(12,4) | non-SRD |
| MeasureOfPrice | Numeric(12,4) | non-SRD |
| ShelfFacingsQty | Smallint | SRD "Display" |
| MultiLocationInd | Char(1) | SRD "Display" |
| PricingUOM | Varchar(4) | non-SRD |
| PlanogramID | Varchar(25) | SRD "Range" |
| ProductStoreStatus | Tinyint | SRD "Range" |
| ProductStoreRangeStatus | Tinyint | SRD "Range" |
| SELQty | Tinyint | SRD "Display" |
| LocalSKUDescription | Varchar(250) | non-SRD |
| LocalShortSKUDescription | Varchar(120) | non-SRD |
| LastUpdateDateTime | Datetime | admin |

### Transport

SSIS package `TOM.S039.SRtoIDS.SELRangeAndDisplayIndicators.dtsx`. Scheduled batch, daily. Stored procedure `S039_UpdateSELRangeandDisplayInd_usp.sql`. SR archives processed files to `../StoreRange/ARCHIVE`.

### Glossary as shipped

| Term | Definition |
|---|---|
| IKB | Intactix Knowledge Base — SQL Server DB provided by JDA Intactix to maintain Space Planning and Floor Planning data |
| RMS | Retek Merchandising System — Tesco US Merchandising operations; governs merch operations, receives base master & transaction data, provides to next-level operational systems |
| PP | Product Position — SQL Server DB capturing capacity information for products not part of planogram |
| IMOF | Integration Management Operational Framework — pluggable audit / exception / rules / scheduling for BizTalk, RTI, SSIS |
| EAI | Enterprise Application Integration |
| EIA | Enterprise Information Architecture |

## Extracted content — S101 (emergency facings, near-real-time)

### Scope and purpose

When an in-store user performs product mapping and finds that actual facings on a shelf differ from what the central planogram specifies, RPP emits a record. S101 reads that record from the RPP holding table in near-real-time (Autosys scheduled), loads it into IDS, marks the source record processed. Downstream C023TR (S092) extracts this to Storeline, **which immediately prints a label for the person doing the mapping to replace on the shelf**.

> *"Interface S101 is not currently required in the US, as product mapping of exceptions is not performed at this time."* (S101, §1.1)

Meaning: the emergency-facings capability was designed into the canonical but operationally enabled only on the international side.

### Background quote — the SRD + Storeline + Label contract

> *"SRD manages a group of attributes which are required either to appear on Storeline shelf-edge-labels (SELs) or to be used by Storeline in its processes to produce the SELs. These attributes are configured in JDA by the planogramming process, and from there passed to StoreRange and RPP. At certain points in the item in store lifecycle, StoreRange issues these attributes via files SR39 and SR92, which are required in an overnight feed to the IDS (S039TR) and onwards to Storeline (C023TR). The Storeline user will select when and how to group-print labels, which will contain both the SRD attributes together with RMS-sourced attributes (e.g. Price). Labels will not be automatically printed as part of this process."*
>
> *"Where product mapping indicates an in-store deviation from facings created on the planogram, the RPP application ("product-mapping" application) will emit a record on the emergency facings feed. Interface S101 transfers this in near real-time to IDS, and S092 from there to Storeline. This feed only corrects the 'facings' attribute (sending all others as null), and will result in a label being immediately printed in-store for the person doing the product mapping to replace on the shelf."*

### Source table (RPP)

`tbl_ProductFacingsDetails_Outbound`:
- SKUID `varchar(50)`
- StoreID `int`
- FacingWide `int`
- IL_Time_Stamp `datetime` — null-select gate; updated on completion to prevent reprocessing
- (insert/amend audit + soft-delete fields ignored)

### Target — IDS `SKUItemInStore` (subset) + new `SRDSEL_Trans`

**`SRDSEL_Trans`** (created by S101, written by both S039 and S101):

| Field | Format | Notes |
|---|---|---|
| SKUID | varchar(25) NOT NULL | |
| StoreID | integer NOT NULL | |
| UpdateType | varchar(10) NOT NULL | **"FULL" / "RANGE" / "FACINGS" / "EMERGENCY"** — S039TR inserts one of the first 3; S101 always inserts "EMERGENCY"; C023TR uses this to decide which rows and which fields to extract for each run |
| InsertDateTime | datetime NOT NULL | sysdatetime of insertion |
| ExtractDateTime | datetime NULL | null until successful extract |
| BatchNumber | integer NULL | null until successful extract |

### Scheduling contract

S101 must run as a required precursor to C023TR (S092). If the regular S039TR / C023TR batch is running, S101 waits; otherwise it runs immediately once the regular cycle completes. Operational cut-through for urgent shelf correction.

## End-to-end path (derived)

```
┌─────────────────────┐
│  IKB (JDA Intactix) │  — planogram source of truth
└──────────┬──────────┘
           │ Interface 78 — full planogram refresh per store
           ▼
┌─────────────────────┐
│  Store Range (SR)   │  — delta computation, flat-file emitter
└──────────┬──────────┘
           │ S039 — SR_SELRange + SR_SELDisplay flat files (daily batch)
           ▼                                 ┌─────────────────────┐
┌─────────────────────┐                      │   RPP / Product     │
│   IDS / RIDS v7.2   │ <──────── S101 ──────│   Position          │
│   SKUItemInStore    │  (emergency facings, │   (in-store mapping)│
│   + SRDSEL_Trans    │   near-real-time)    └─────────────────────┘
└──────────┬──────────┘
           │ C023TR / S092 — extract to Storeline
           ▼
┌─────────────────────┐         ┌─────────────────────┐
│   Storeline         │ ◄───────│   RMS (Retek)       │
│   (shelf-edge       │         │   price + desc      │
│    label engine)    │         └─────────────────────┘
└──────────┬──────────┘
           │ physical shelf-edge label print
           ▼
┌─────────────────────┐
│   CRDM              │  — Sysrepublic's label delivery product
│   (Sysrepublic)     │     founder's first engagement with Sysrepublic
└─────────────────────┘
```

## Notes for synthesis

Key findings that feed `Brain/wiki/srd-shelf-edge-label.md` and `[[intactix-canonical-validation]]`:

1. **The label is the compile target of the canonical.** Every prefix family must reconcile at the physical rail for the label to print correctly. If the label can't print, the canonical is broken.

2. **Four update types as the state machine of reconciliation.** FULL / RANGE / FACINGS / EMERGENCY is a compact state-machine for *why the label is being reprinted*. This is a first-class canonical artifact worth codifying in RetailSpine as the SEL reconciliation reason-code set.

3. **The canonical was dual-national at v1.2.** *"This interface is for US and Turkey implementation."* The Walmart International canonical didn't invent portability; portability was a design property of the F&E spec from day one.

4. **Store Range, not integration layer, owns delta computation.** *"Tesco strategy to avoid placing any business logic in integration layer processing."* The canonical is emitted clean; the integration layer is dumb plumbing. This is the architectural discipline RetailSpine and the MCP exposure should preserve.

5. **The emergency-facings path is the in-store operator proof.** When a mapper finds shelf reality ≠ planogram, the label prints on the spot. This is the 2007 operator-visible equivalent of what bubble + agents + MCP should now do continuously and invisibly.

6. **CRDM = Sysrepublic's label product.** The relationship to Sysrepublic traces through the shelf edge, a decade before the LP / xBR / Secure work. This belongs in the Secure MOC as prior-art relationship.

7. **RMS is explicitly Retek.** Pre-Oracle acquisition of Retek (Apr 2005 → closed Jun 2005). At 2007 it's still being called "Retek Merchandising System" in live Tesco integration documents.
