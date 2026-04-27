---
id: sdd-cp-paycode
title: NCR Counterpoint — PayCode Adapter (Module F)
status: draft-1
version: 0.1.0
date: 2026-04-26
author: GrowDirect Engineering
linear: GRO-TBD
companion-sdds:
  - docs/sdds/canary/ncr-counterpoint-tsp-adapter.md
  - docs/sdds/canary/ncr-counterpoint-module-q-chirp-wiring.md
source-endpoints:
  - GET /PayCodes (full sync, cached 24h)
  - GET /PayCode/{PayCode} (per-code fetch)
source-tables: PS_PAY_COD
target-tables:
  - app.cp_pay_codes (new)
  - sales.transaction_tenders (existing — tender_type normalization)
  - app.poll_watermarks (existing — entity_type 'pay_code')
---

# NCR Counterpoint — PayCode Adapter (Module F)

## 1. Purpose

Counterpoint PayCodes are the merchant's tender taxonomy — the set of
named payment methods accepted at the register. Every `PS_DOC_PMT` record
(payment line on a transaction) carries a `PAY_COD` string that resolves
against this table.

The PayCode adapter has two jobs:

1. **Tender classification:** Sync `PS_PAY_COD` → `app.cp_pay_codes`,
   enabling `sales.transaction_tenders.tender_type` to be populated with
   a canonical type classification (cash / card / ar / gift_card /
   store_credit / check / foreign / other) rather than a raw
   provider-specific code string.

2. **Module Q substrates:** `OPN_DRW` (drawer-opens-on-tender) and
   `PAY_TYP` feed the tender-mix and drawer anomaly rule families
   (Q-TM, Q-DS).

## 2. PAY_TYP taxonomy

The `PAY_TYP` field on each PayCode is the canonical classification:

| PAY_TYP | Meaning | Canonical tender_type |
|---|---|---|
| `C` | Cash | `cash` |
| `K` | Check | `check` |
| `E` | Electronic / EDC card | `card` |
| `A` | A/R charge (account) | `ar` |
| `G` | Gift card (Counterpoint native) | `gift_card` |
| `V` | SVS/service voucher card | `gift_card` |
| `S` | Store credit | `store_credit` |
| `F` | Foreign currency | `foreign` |
| `!` | Other / undefined | `other` |

Canonical tender_type is the CRDM-level classification used in
`sales.transaction_tenders.tender_type`. It normalizes across POS sources:
Square's `CASH_DRAWER` maps to `cash`; Counterpoint's `C`-type PayCode
maps to `cash`. Detection rules operate on canonical types.

## 3. Polling strategy

| Property | Value |
|---|---|
| Endpoint | `GET /PayCodes` |
| Watermark | None — re-sync all pay codes daily. PayCodes is small (< 50 rows typically); full re-sync is cheaper than change tracking. |
| Poll interval | 86400s (daily) |
| Cache | Counterpoint server-caches PayCodes 24h. Send `ServerCache: no-cache` on first poll of the day. |
| Activation ordering | Phase A (reference data, same day as stores + categories) |
| `poll_watermarks` key | `(merchant_id, 'counterpoint', company_alias, 'pay_code')` |

## 4. New table — app.cp_pay_codes

```sql
CREATE TABLE app.cp_pay_codes (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id     UUID NOT NULL REFERENCES app.merchants(id),

    pay_cod         TEXT NOT NULL,           -- PS_PAY_COD.PAY_COD (e.g. "CASH", "VISA")
    pay_typ         TEXT,                    -- A/R/E/C/K/G/V/S/F/! (see §2)
    descr           TEXT,                    -- display description
    canonical_type  TEXT NOT NULL,           -- cash|card|ar|gift_card|store_credit|check|foreign|other

    -- Module Q substrates
    opn_drw         BOOLEAN,                 -- OPN_DRW: Y = opens cash drawer on tender
    edc_auth_flg    TEXT,                    -- O=optional, R=required, N=not used
    is_foreign      BOOLEAN,                 -- foreign currency flag

    -- Operational flags
    allow_for_ords  BOOLEAN,                 -- allowed on orders
    allow_for_lwys  BOOLEAN,                 -- allowed on layaways
    curncy_cod      TEXT,                    -- currency code (HOME or ISO)

    -- Source metadata
    lst_maint_dt    TIMESTAMPTZ,
    lst_maint_usr_id TEXT,

    -- Canary metadata
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),

    UNIQUE (merchant_id, pay_cod)
);

CREATE INDEX idx_cp_pay_codes_merchant_type
    ON app.cp_pay_codes (merchant_id, canonical_type);

CREATE INDEX idx_cp_pay_codes_merchant_opn_drw
    ON app.cp_pay_codes (merchant_id, opn_drw)
    WHERE opn_drw = TRUE;
```

### `canonical_type` derivation

```python
PAY_TYP_TO_CANONICAL = {
    "C": "cash",
    "K": "check",
    "E": "card",
    "A": "ar",
    "G": "gift_card",
    "V": "gift_card",
    "S": "store_credit",
    "F": "foreign",
}

def derive_canonical_type(pay_typ: str) -> str:
    return PAY_TYP_TO_CANONICAL.get(pay_typ, "other")
```

`canonical_type` is computed at parse time and stored — never re-derived
at query time. If a future Counterpoint version adds new PAY_TYP codes,
update the mapping and re-sync.

## 5. Transaction tender normalization

The existing `sales.transaction_tenders` table stores `tender_type` as a
free-text field (currently populated from Square's tender types). For
Counterpoint transactions, `parse_cp_transaction()` in the TSP adapter
resolves `PS_DOC_PMT.PAY_COD` → canonical type:

```python
def resolve_tender_type(
    db,
    merchant_id: UUID,
    pay_cod: str,
    company_alias: str,
) -> str:
    """Resolve Counterpoint PAY_COD to canonical tender_type string."""
    row = db.query(CpPayCode).filter_by(
        merchant_id=str(merchant_id),
        pay_cod=pay_cod,
    ).first()
    if row:
        return row.canonical_type
    # Unknown pay code — queue cache-miss, return 'other' for now
    emit_cache_miss_event("pay_code", pay_cod, merchant_id, company_alias)
    return "other"
```

`sales.transaction_tenders` requires no schema changes — `tender_type`
already accepts arbitrary strings and the canonical values used here
(`cash`, `card`, `ar`, etc.) are a subset of the Square values already in
use.

## 6. Module Q substrates

### Q-TM-01 CASH_ONLY_REGISTER

The rule computes `cash_share` as the fraction of a session's tendered
amount paid with cash-type tenders. The PayCode table is the source of
truth for which PAY_COD values classify as cash:

```sql
SELECT
    t.store_id,
    t.drawer_session_id,
    SUM(CASE WHEN pc.canonical_type = 'cash' THEN td.amount_cents ELSE 0 END)::float
    / NULLIF(SUM(td.amount_cents), 0) AS cash_share
FROM sales.transaction_tenders td
JOIN sales.transactions t ON t.id = td.transaction_id
LEFT JOIN app.external_identities ei
    ON ei.merchant_id = t.merchant_id
   AND ei.source_code = 'counterpoint'
   AND ei.entity_type = 'pay_code'  -- new entity_type for PayCode bridge
   AND ei.external_id = td.source_pay_code
LEFT JOIN app.cp_pay_codes pc ON pc.merchant_id = t.merchant_id
    AND pc.pay_cod = td.source_pay_code
WHERE t.merchant_id = :merchant_id
  AND t.occurred_at >= :session_start
GROUP BY t.store_id, t.drawer_session_id;
```

**Note:** `td.source_pay_code` is a new column on `sales.transaction_tenders`
(see §7). It stores the raw PAY_COD string for later resolution, in addition
to the already-resolved `tender_type`.

### Q-TM-02 TENDER_SWAP

Detecting a swap from card to cash (or vice versa) requires knowing the
original tender type. The `OPN_DRW` flag helps: if the original tender had
`OPN_DRW = False` (card) but the drawer opened during the transaction
(audit log event), and the final tender is cash (`OPN_DRW = True`), that's
the signature.

### Q-DS-01 DRAWER_SESSION_SHRINKAGE

`OPN_DRW = True` pay codes are the events that affect drawer balance.
A drawer reconciliation detects if the number of OPN_DRW tender events ×
average cash tender amount diverges from the drawer count at session close.

## 7. Additive column — sales.transaction_tenders

One new column on the existing table to preserve the raw PAY_COD for join
back to `cp_pay_codes` at query time:

```python
# Alembic migration: add source_pay_code to sales.transaction_tenders
source_pay_code: Mapped[Optional[str]] = mapped_column(
    String(20), nullable=True,
    doc="Raw PAY_COD string from Counterpoint PS_DOC_PMT. "
        "NULL for Square tenders. Resolves to tender_type via cp_pay_codes."
)
```

The TSP adapter's `parse_cp_transaction()` populates `source_pay_code`
from `PS_DOC_PMT.PAY_COD` on each tender row. `tender_type` is
simultaneously set to the resolved canonical value.

## 8. Activation ordering

PayCode sync runs in Phase A (reference data), alongside stores and
item categories:

```
Phase A:
  ├── Store sync
  ├── CustomerControl sync
  ├── ItemCategories sync
  └── PayCode sync  ← this adapter
```

Document parsing depends on PayCodes being loaded so that
`resolve_tender_type()` has data. If PayCodes are missing (e.g., Phase A
was skipped), the adapter logs a warning and assigns `tender_type = 'other'`
for all tenders in that Document, queuing a PayCode re-sync.

## 9. Event types

| CanonicalEvent.event_type | Trigger |
|---|---|
| `pay_code.catalog_refreshed` | After successful `GET /PayCodes` sync |

Sub2 dispatch:

```python
EVENT_TYPE_PARSERS: dict[tuple[str, str], Callable] = {
    ...
    ("counterpoint", "pay_code.catalog_refreshed"): parse_cp_pay_codes,
}
```

## 10. New tables summary

| Object | Schema | Action | Notes |
|---|---|---|---|
| `cp_pay_codes` | app | CREATE | PayCode taxonomy |
| `transaction_tenders.source_pay_code` | sales | ADD COLUMN | Raw PAY_COD for join back |

## 11. Acceptance criteria

**AC-F-01 — Initial sync:** After PayCode sync, `app.cp_pay_codes` contains
rows for the tenant's configured pay codes. `PAY_COD = "VISA"` resolves to
`canonical_type = "card"`. `PAY_COD = "CASH"` resolves to `canonical_type = "cash"`.
`PAY_COD = "A/R"` resolves to `canonical_type = "ar"`.

**AC-F-02 — Drawer flag:** `cp_pay_codes` rows where `opn_drw = True` include
cash and store-credit types. Card types (`PAY_TYP = E`) have `opn_drw = False`.

**AC-F-03 — Tender normalization:** A transaction Document with
`PS_DOC_PMT.PAY_COD = "VISA"` produces a `sales.transaction_tenders` row
with `tender_type = "card"` and `source_pay_code = "VISA"`.

**AC-F-04 — Unknown pay code fallback:** A Document with `PAY_COD = "CHECK"`
(not yet in `cp_pay_codes`) produces `tender_type = "other"` and queues a
`pay_code.catalog_refreshed` on-demand sync. After the sync, the tender row's
type is not retroactively updated (acceptable for initial deployment; may
refine in Phase 2).

**AC-F-05 — Cash-share query:** The Q-TM-01 query returns the correct
`cash_share` fraction for a test session where 3 of 5 transactions used
cash tenders.

## 12. Open questions

| ID | Question | Impact |
|---|---|---|
| F-OQ-01 | Full PAY_TYP value space. The sample data shows C, K, E, A, G, V, S, F. Are there other values in production Counterpoint deployments (particularly garden center configs)? Confirm against sandbox. | PAY_TYP_TO_CANONICAL completeness |
| F-OQ-02 | Garden center cash-vendor payments use CASH pay code. The Q-IS-02 allow-list classifies `DOC_TYP=RECVR + CASH tender` as legitimate. Does this apply to any CASH tender on a RECVR document, or only specific `PAY_COD` values? Some stores configure separate vendor-payment pay codes. | Q-IS-02 allow-list precision |
| F-OQ-03 | Foreign currency tenders (`IS_FOREIGN = True`): are these present in any US garden center deployment? If not, `canonical_type = 'foreign'` is dead code for Phase 1. | Scope clarity |

---

## Related

- `docs/sdds/canary/ncr-counterpoint-tsp-adapter.md` — PS_DOC_PMT mapping; calls `resolve_tender_type()`
- `docs/sdds/canary/ncr-counterpoint-module-q-chirp-wiring.md` — Q-TM rules consuming canonical_type
- `Brain/wiki/ncr-counterpoint-api-reference.md` — Counterpoint endpoint reference (§ Module F)
