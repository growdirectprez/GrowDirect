---
title: NCR Counterpoint Document Model
tags: [specs, counterpoint, document, ps_doc_hdr]
nav_order: 53
audience: NCR Counterpoint VARs
last-updated: 2026-04-30
---

---
classification: internal
type: wiki
status: active
date: 2026-04-25
last-compiled: 2026-04-25
needs-review: 2026-05-09
source: github.com/NCRCounterpointAPI/APIGuide v2.4 — GET_Document.md sample payload
companion: Brain/wiki/ncr-counterpoint-api-reference.md
----

# NCR Counterpoint Document Model

The `Document` is Counterpoint's **omnibus transactional container**. A single endpoint family (`GET/POST/PATCH_Document` + nested resources) handles essentially every transactional operation in the platform: sales, returns, voids, transfers between stores, vendor receivers, purchase orders, purchase requests, gift card transactions, return-to-vendor, AR documents.

All differentiation is via the `DOC_TYP` field (and related discriminators). Understanding Document is the single biggest lever for Canary's TSP adapter design.

## Top-level envelope

`GET /Document/{DocId}` returns:

```
{
  "PS_DOC_HDR": {
    DOC_ID, STR_ID, STA_ID, TKT_NO, DOC_TYP, TKT_TYP,
    SAL_LINS, ORD_LINS, RET_LINS, GFC_LINS, BO_LINS, SO_LINS,
    SAL_LIN_TOT, RET_LIN_TOT,
    DRW_ID, DRW_SESSION_ID,
    CUST_NO, USR_ID, SLS_REP,
    STK_LOC_ID, PRC_LOC_ID,
    TAX_COD, NORM_TAX_COD,
    DOC_GUID, IS_DOC_COMMITTED, IS_REL_TKT,
    TKT_DT, RS_UTC_DT, LST_MAINT_DT, LST_MAINT_USR_ID,
    PS_DOC_LIN: [...],          // line items
    PS_DOC_PMT: [...],          // payments
    PS_DOC_NOTE: [...],         // notes
    PS_DOC_PKG_TRK_NO: [...],   // package tracking
    PS_DOC_HDR_TOT: [...],      // totals (subtotal, tax, tender, change, due)
    PS_DOC_TAX: [...],          // tax breakdown by authority
    PS_DOC_HDR_MISC_CHRG: [...],// misc charges
    PS_DOC_HDR_ORIG_DOC: [...], // original-document refs (for returns/voids)
    PS_DOC_AUDIT_LOG: [...],    // full audit trail
    PS_DOC_GFC: [...]           // gift card detail
  },
  "ErrorCode": "SUCCESS"
}
```

**One Document = one transaction** (sale, return, transfer, etc.). Line items, payments, taxes, and audit are all nested in the response — no need for separate calls per nested resource for read.

## DOC_TYP taxonomy

Document types span at least the following (inferred from Workgroup's NXT_*_NO numbering generators in `GET_Workgroup`):

| Code | Type | Workgroup counter |
|---|---|---|
| `T` | Ticket / sale | (none — uses TKT_NO) |
| `?` | Order | (uses ORD_LINS in header) |
| `?` | Return | RET_LINS > 0; LIN_TYP "R" on lines |
| `?` | Void | likely a separate DOC_TYP; needs verification |
| `XFER` | Inter-store transfer | NXT_XFER_NO |
| `RECVR` | Receiver (receiving from vendor) | NXT_RECVR_NO |
| `PO` | Purchase order | NXT_PO_NO |
| `PREQ` | Purchase request | NXT_PREQ_NO |
| `RTV` | Return to vendor | NXT_RTV_NO |
| `STC` | (likely) Stock count / stock transfer | NXT_STC_NO |
| `EVENT` | Event/promo? | NXT_EVENT_NO |
| `GFC` | Gift card transaction | NXT_GFC_NO |
| `AR_DOC` | AR document | NXT_AR_DOC_NO |

**Open verification needed:** read additional sample payloads or test database to confirm exact DOC_TYP code strings. The sample for a sale shows `DOC_TYP: "T"` and `TKT_TYP: "T"` — need to see returns, transfers, etc.

**Implication for Canary adapter:** the TSP `Documents` polling loop must filter by DOC_TYP and route to the correct CRDM event entity. One endpoint, many event types. This is GOOD because it simplifies the polling loop; it requires careful type-routing on ingest.

## Header fields (`PS_DOC_HDR`)

Key fields for Canary ingestion:

| Field | Use |
|---|---|
| `DOC_ID` | Primary key — idempotency anchor |
| `DOC_GUID` | Cross-system unique identifier |
| `DOC_TYP` | Type discriminator |
| `STR_ID`, `STA_ID` | Store + station (Module N context) |
| `TKT_NO` | Human-readable ticket number |
| `DRW_ID`, `DRW_SESSION_ID` | Cash drawer + session — useful for day-end + Module Q |
| `CUST_NO` | Customer (or "CASH" for non-customer transactions) |
| `USR_ID`, `SLS_REP` | User entering / sales rep — Module L (degraded — only API users, not full employees) |
| `STK_LOC_ID`, `PRC_LOC_ID` | Stock + price location codes |
| `TAX_COD`, `NORM_TAX_COD` | Tax code applied (NORM = no override) |
| `IS_DOC_COMMITTED` | Y/N — committed vs draft |
| `IS_REL_TKT` | Y/N — released ticket flag |
| `IS_OFFLINE` | bool — was processed offline (offline-mode store) |
| `RS_UTC_DT` | UTC timestamp — primary sort/filter key for incremental polling |
| `TKT_DT` | Local-time ticket date |
| `LST_MAINT_DT`, `LST_MAINT_USR_ID` | Last modification audit |

`SAL_LINS` / `RET_LINS` / `GFC_LINS` / `BO_LINS` (backorder) / `SO_LINS` (special order) — all line counts in header. **Polling logic:** filter on `RS_UTC_DT > last_sync_timestamp`; route by `DOC_TYP` and the line-count fields.

## Line items (`PS_DOC_LIN[]`)

Each line carries:

| Field | Use |
|---|---|
| `LIN_SEQ_NO` | Position |
| `LIN_TYP` | "S" sale, "R" return, others (kit parts? service?) |
| `ITEM_NO`, `DESCR`, `CATEG_COD`, `SUBCAT_COD` | Item identity + classification |
| `ITEM_VEND_NO` | Vendor (for vendor analysis / Module J) |
| `QTY_SOLD`, `QTY_NUMER`, `QTY_DENOM`, `QTY_UNIT` | Quantity in fractional form (e.g., 1/4 lb) |
| `PRC`, `REG_PRC`, `CALC_PRC`, `EXT_PRC`, `EXT_COST` | Multiple price + cost views |
| `MIX_MATCH_COD`, `MIX_MATCH_CONTRIB`, `MIX_MATCH_PRC_BASED_ON` | Mix-and-match group + contribution |
| `IS_DISCNTBL`, `HAS_PRC_OVRD` | Discountable + price-override flags |
| `TAX_AMT_ALLOC` | Tax allocated to this line |
| `STK_LOC_ID`, `PRC_LOC_ID` | Stock + price loc per line (can differ from header) |
| `BARCOD` | Barcode scanned |
| `IS_FOOD_STMP_ELIG`, `IS_KIT_PAR` | Eligibility + kit parent flags |
| `LIN_GUID` | Per-line cross-system identifier |
| `PS_DOC_LIN_CELL[]` | Cell detail (multi-dimension items) |
| `PS_DOC_LIN_SER[]` | Serial numbers attached to this line |
| `PS_DOC_LIN_PRICE[]` | Pricing rule that produced this price |
| `PS_DOC_LIN_PROMPT[]` | Prompts (custom data captured at sale) |

**Pricing rule capture (`PS_DOC_LIN_PRICE`):**
```
{
  "PRC_JUST_STR": "Price-1",     // human-readable rationale
  "PRC_GRP_TYP": "!",            // price group type
  "PRC_RUL_SEQ_NO": -1,          // pricing rule ID applied
  "PRC_BRK_DESCR": "I",          // price break descriptor
  "PRC_SEQ_NO": 1,               // sequence within breaks
  "QTY_PRCD": 1,                 // qty priced at this break
  "UNIT_PRC": 349.99
}
```

This means **pricing logic is captured at transaction time per line.** Canary can recover the pricing decision retrospectively from any ticket; we don't need to model live pricing rules — we observe their output.

## Payments (`PS_DOC_PMT[]`)

Each payment carries:

| Field | Use |
|---|---|
| `PMT_SEQ_NO` | Position |
| `PAY_COD`, `DESCR` | Tender code + label (CASH, VISA, etc.) |
| `PAY_COD_TYP` | Tender type category |
| `PMT_LIN_TYP` | Line type (sale T, refund R, etc.) |
| `AMT`, `HOME_CURNCY_AMT` | Amount in tender currency + home currency |
| `EXCH_RATE_NUMER`, `EXCH_RATE_DENOM`, `EXCH_LOSS` | FX detail |
| `CURNCY_COD` | Currency code |
| `CARD_IS_NEW`, `SWIPED`, `SECURE_ECOMM_TRX` | Card flags |
| `EDC_AUTH_FLG` | Authorization status |
| `SIG_IMG`, `SIG_IMG_VECTOR` | Signature capture (PII concern) |
| `PS_DOC_PMT_APPLY[]` | Apply-to instructions (sale vs AR-charge vs deposit) |
| `PS_DOC_PMT_PROMPT[]` | Prompts captured during payment |

**PII concern:** `SIG_IMG` is a captured signature image. Canary's adapter MUST exclude or redact this field at ingest — never persist signature images.

## Taxes (`PS_DOC_TAX[]`)

Multi-authority tax breakdown is modeled directly:

```
[
  { "AUTH_COD": "MEMPHIS", "TAX_AMT": 7,    "TXBL_LIN_AMT": 349.99, "RUL_COD": "TAX" },
  { "AUTH_COD": "SHELBY",  "TAX_AMT": 10.5, "TXBL_LIN_AMT": 349.99, "RUL_COD": "TAX" },
  { "AUTH_COD": "TN",      "TAX_AMT": 14,   "TXBL_LIN_AMT": 349.99, "RUL_COD": "TAX" }
]
```

City + County + State tax stacked. ARTS-compatible. **Critical for Module F**: tax detail is per-document, not just a total — Canary can do tax-authority reconciliation without joining external data.

## Header totals (`PS_DOC_HDR_TOT[]`)

Comprehensive: SUB_TOT, TOT_LIN_DISC, TOT_HDR_DISC, TOT_GFC_AMT, TOT_SVC_AMT, TOT_MISC, TAX_AMT, NORM_TAX_AMT, TOT_TND, TOT_CHNG, AMT_DUE, TOT (final), TOT_HDR_DISCNTBL_AMT, TOT_EXT_COST, TOT_WEIGHT, TOT_CUBE.

Canary can compute margin (TOT - TOT_EXT_COST) directly from each ticket. Gross margin per ticket is observable.

## Audit log (`PS_DOC_AUDIT_LOG[]`)

Every Document carries its own audit log:

```
{
  "LOG_SEQ_NO": 1,
  "DOC_TYP": "T",
  "CURR_DT": "2016-04-24T22:38:44.0000000",
  "CURR_STR_ID": "20",
  "CURR_STA_ID": "20-1",
  "CURR_DRW_ID": "20-1",
  "CURR_USR_ID": "MGR",
  "CURR_WKSTN_NAM": "WUSMJ185111-T75",
  "CURR_DB_NAM": "QATestGolf",
  "ACTIV": "N",
  "LOG_ENTRY": "Entered a new ticket",
  "PS_DOC_AUDIT_LOG_TOT": [...]
}
```

**Critical for Module Q (Loss Prevention):** the audit log captures user, workstation, drawer, and timestamp for every state change on the Document. This is the substrate for fraud detection rules (suppressed-sale patterns, refund-without-original-ticket patterns, drawer-anomaly patterns). Canary's Q module reads against this directly.

## Original document references (`PS_DOC_HDR_ORIG_DOC[]`)

For returns and voids, this array references the original sale document. **Resolves SDD Q2 partially:** returns are linked to their originating ticket via this array; voids likely use the same mechanism. Canary's adapter joins return → original sale via `PS_DOC_HDR_ORIG_DOC`.

## Implications for Canary

### Adapter design

- **Single polling endpoint** for the whole T+D+J family of events (sales, returns, voids, transfers, POs)
- **Type-route on ingest** by DOC_TYP — different CRDM event entity per type
- **Idempotency** keyed on DOC_ID
- **Incremental polling** keyed on RS_UTC_DT > last_sync (UTC timestamp, sortable)
- **Pagination** via Counterpoint API's skip/take (per Basics/Requests.md)

### CRDM extensions implied

Counterpoint Document → CRDM mapping suggests CRDM should accommodate:

- `Events.transactions` — DOC_TYP "T" (and similar sale codes)
- `Events.returns` — DOC_TYP for returns + RET_LINS > 0
- `Events.voids` — DOC_TYP for voids
- `Events.transfers` — DOC_TYP "XFER"
- `Events.purchase_orders` — DOC_TYP "PO" / "PREQ" / "RECVR" / "RTV"
- `Events.gift_card_transactions` — DOC_TYP "GFC"
- `Events.audit_log_entries` — flattened from PS_DOC_AUDIT_LOG (Module Q substrate)
- `Events.transaction_lines` — flattened from PS_DOC_LIN
- `Events.transaction_payments` — flattened from PS_DOC_PMT
- `Events.transaction_taxes` — flattened from PS_DOC_TAX (multi-authority)
- `Events.pricing_decisions` — flattened from PS_DOC_LIN_PRICE (per-line pricing rule applied)
- `Events.signatures_captured` — boolean flag only; raw image NOT persisted

### Module impacts

- **Module T:** primary consumer of Documents
- **Module D:** transfers come through Documents (DOC_TYP "XFER"), not a separate endpoint
- **Module J:** purchase orders + receivers + RTVs come through Documents
- **Module F:** payment + tax detail flows from Document nested arrays
- **Module Q:** audit log + pricing decisions provide rich fraud-detection substrate
- **Module N:** STR_ID + STA_ID + DRW_ID associations via Document
- **Module S:** ITEM_NO + categorization referenced from line items

### Privacy / PII

- `SIG_IMG`, `SIG_IMG_VECTOR` — signature images. **REDACT at ingest.**
- `CUST_NO` may be tied to PII via Customer record. Canary's tenant-isolation rules apply.
- Card masking — PAN data is tokenized via Counterpoint's tokenization utility; Canary should never see raw PAN.

## Open verifications still needed

- Full DOC_TYP code list (sample exhaustive set; current sample only shows "T")
- Void DOC_TYP code (and whether voids reference original via PS_DOC_HDR_ORIG_DOC)
- Other LIN_TYP codes beyond "S" and "R" (kits? services? GFC?)
- TKT_TYP vs DOC_TYP distinction (both fields present, sometimes the same)
- `IS_OFFLINE` semantics — what happens at sync time?
- Behavior of `IS_DOC_COMMITTED: "N"` documents — do they appear in GET / should we ingest them?

These need additional sample payloads (returns, transfers, voids) or direct testing against an NCR sandbox.
