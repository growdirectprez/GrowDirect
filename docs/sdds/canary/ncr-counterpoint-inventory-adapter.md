---
id: sdd-cp-inventory
title: NCR Counterpoint — Inventory Adapter (Module D)
status: draft-1
version: 0.1.0
date: 2026-04-26
author: GrowDirect Engineering
linear: GRO-TBD
companion-sdds:
  - docs/sdds/canary/ncr-counterpoint-item-catalog-adapter.md
  - docs/sdds/canary/ncr-counterpoint-module-q-chirp-wiring.md
source-endpoints:
  - GET /InventoryLocations (location-level stock, incremental via RS_UTC_DT)
  - GET /Item/Inventory (per-item across all locations, full)
source-tables: IM_INV
target-tables:
  - app.cp_inventory_snapshots (new)
  - app.poll_watermarks (existing — entity_type 'inventory')
---

# NCR Counterpoint — Inventory Adapter (Module D)

## 1. Purpose

Counterpoint tracks per-item, per-location inventory in `IM_INV`. The inventory
adapter has two jobs:

1. **Shrinkage substrate:** Periodic inventory snapshots feed Module Q rules
   that detect abnormal inventory movement — items disappearing between sessions
   without corresponding sales documents (Q-IS rules: inventory shrinkage,
   live-goods write-off, receiving-dock discrepancies).

2. **Margin substrate:** On-hand qty × cost feeds the margin-floor computation
   in Q-C rules when `lst_cost` is unavailable on the item catalog record.

This adapter is **informational only** — it does not populate `sales.*` tables
and has no effect on transaction parsing. It is a Module Q substrate source.

## 2. Counterpoint Inventory Endpoints

### GET /InventoryLocations

Returns inventory records filtered by location and optionally by modified date.

```
GET /<company>/CPRestAPI/rest/InventoryLocations?Loc={loc_id}&RS_UTC_DT={watermark}
```

Response shape (abbreviated):
```json
{
  "InventoryLocations": [
    {
      "ITEM_NO":       "FERN-4IN",
      "LOC_ID":        "1",
      "QTY_ON_HND":    42.0,
      "QTY_ON_ORD":    0.0,
      "QTY_COMMIT":    5.0,
      "QTY_AVAIL":     37.0,
      "LST_COST":      1.25,
      "AVG_COST":      1.18,
      "LST_CNT_DT":    "2026-04-15T00:00:00",
      "LST_RCV_DT":    "2026-04-10T00:00:00",
      "RS_UTC_DT":     "2026-04-26T14:22:00"
    }
  ]
}
```

### GET /Item/Inventory

Returns full inventory across all locations for a specific item. Used for
targeted on-demand pulls (cache-miss pattern):

```
GET /<company>/CPRestAPI/rest/Item/{ITEM_NO}/Inventory
```

## 3. cp_inventory_snapshots Table (New)

Stores periodic point-in-time inventory snapshots. Not a running ledger —
each row is a snapshot of `(item, location)` at a given timestamp.

```sql
CREATE TABLE app.cp_inventory_snapshots (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id     UUID NOT NULL REFERENCES app.merchants(id),

    item_no         TEXT NOT NULL,          -- IM_INV.ITEM_NO
    loc_id          TEXT NOT NULL,          -- IM_INV.LOC_ID (store)
    snapped_at      TIMESTAMPTZ NOT NULL,   -- time of snapshot (poll time)

    -- Quantity fields
    qty_on_hnd      NUMERIC(12, 4),         -- on-hand qty
    qty_on_ord      NUMERIC(12, 4),         -- on order
    qty_commit      NUMERIC(12, 4),         -- committed (open sales orders)
    qty_avail       NUMERIC(12, 4),         -- available = on_hnd - commit

    -- Cost fields
    lst_cost        NUMERIC(12, 4),         -- last purchase cost
    avg_cost        NUMERIC(12, 4),         -- weighted average cost

    -- Last activity dates
    lst_cnt_dt      DATE,                   -- last physical count date
    lst_rcv_dt      DATE,                   -- last receive date

    -- Source metadata
    rs_utc_dt       TIMESTAMPTZ,            -- IM_INV.RS_UTC_DT (source watermark)

    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- No UNIQUE constraint — multiple snapshots per (item, loc) over time
    -- Partition by merchant_id + snapped_at for query performance
);

CREATE INDEX idx_cp_inv_snapshots_merchant_item_loc
    ON app.cp_inventory_snapshots (merchant_id, item_no, loc_id, snapped_at DESC);

CREATE INDEX idx_cp_inv_snapshots_merchant_loc_snap
    ON app.cp_inventory_snapshots (merchant_id, loc_id, snapped_at DESC);
```

### Retention policy

Snapshots older than 90 days are eligible for pruning. The rule engine only
needs current + prior-session values for delta computation. A nightly cron
deletes rows where `snapped_at < now() - interval '90 days'`.

## 4. Polling Strategy

| Property | Value |
|---|---|
| Endpoint | `GET /InventoryLocations?Loc={loc_id}` — one call per known store |
| Watermark | `RS_UTC_DT` — incremental, same pattern as all other entities |
| Poll interval | 3600s (hourly) — shrinkage rules need intra-day resolution |
| Activation ordering | Phase C (after stores known); can run concurrently with document polling |
| `poll_watermarks` key | `(merchant_id, 'counterpoint', company_alias, 'inventory')` |

Store IDs come from `app.cp_known_store_ids`. One poll cycle loops over all
known stores and issues one `GET /InventoryLocations?Loc={str_id}` per store.

```python
def poll_inventory(
    db: Session,
    merchant_id: UUID,
    company_alias: str,
    client: CounterpointClient,
) -> PollResult:
    known_stores = db.query(CpKnownStoreId).filter_by(
        merchant_id=str(merchant_id)
    ).all()

    watermark = get_watermark(db, merchant_id, "counterpoint", company_alias, "inventory")
    events = []
    new_watermark = watermark

    for store in known_stores:
        page = client.get(
            "InventoryLocations",
            params={"Loc": store.str_id, "RS_UTC_DT": watermark.isoformat() if watermark else None},
        )
        rows = page.get("InventoryLocations", [])
        for row in rows:
            snapshot = parse_inventory_row(merchant_id, row)
            db.add(snapshot)
            row_dt = parse_dt(row.get("RS_UTC_DT"))
            if row_dt and (new_watermark is None or row_dt > new_watermark):
                new_watermark = row_dt

        events.append(CanonicalEvent(
            provider="counterpoint",
            event_type="inventory.snapshot_taken",
            tenant_id=str(merchant_id),
            occurred_at=datetime.utcnow(),
            external_id=f"{store.str_id}:{watermark}",
            payload={"store_id": store.str_id, "row_count": len(rows)},
            company_alias=company_alias,
        ))

    db.flush()
    return PollResult(events=events, new_watermark=new_watermark, pages_fetched=len(known_stores))
```

## 5. Module Q Substrates

### Q-IS-01 SESSION_INVENTORY_DROP

Detects abnormal on-hand quantity drops within a session period that are not
explained by sales transactions.

```sql
-- For a store + date range, compute inventory delta vs. sales quantity
WITH inv_start AS (
    SELECT item_no, loc_id, qty_on_hnd AS qty_start
    FROM app.cp_inventory_snapshots
    WHERE merchant_id = :merchant_id
      AND loc_id = :loc_id
      AND snapped_at = (
          SELECT MAX(snapped_at)
          FROM app.cp_inventory_snapshots
          WHERE merchant_id = :merchant_id
            AND loc_id = :loc_id
            AND snapped_at < :session_start
      )
),
inv_end AS (
    SELECT item_no, loc_id, qty_on_hnd AS qty_end
    FROM app.cp_inventory_snapshots
    WHERE merchant_id = :merchant_id
      AND loc_id = :loc_id
      AND snapped_at = (
          SELECT MAX(snapped_at)
          FROM app.cp_inventory_snapshots
          WHERE merchant_id = :merchant_id
            AND loc_id = :loc_id
            AND snapped_at <= :session_end
      )
),
sales_qty AS (
    SELECT
        ei.external_id AS item_no,
        SUM(tli.quantity) AS qty_sold
    FROM sales.transaction_line_items tli
    JOIN sales.transactions t ON t.id = tli.transaction_id
    JOIN app.external_identities ei
        ON ei.merchant_id = t.merchant_id
       AND ei.source_code = 'counterpoint'
       AND ei.entity_type = 'product'
       AND ei.canary_id = tli.product_id::text
    WHERE t.merchant_id = :merchant_id
      AND t.store_id = (
          SELECT id FROM app.locations
          WHERE merchant_id = :merchant_id
            AND id IN (
                SELECT canary_id::uuid FROM app.external_identities
                WHERE source_code = 'counterpoint'
                  AND entity_type = 'location'
                  AND external_id = :loc_id
            )
      )
      AND t.occurred_at BETWEEN :session_start AND :session_end
    GROUP BY ei.external_id
)
SELECT
    s.item_no,
    i1.qty_start,
    i2.qty_end,
    COALESCE(sq.qty_sold, 0) AS qty_sold,
    (i1.qty_start - i2.qty_end) - COALESCE(sq.qty_sold, 0) AS unexplained_drop
FROM inv_start i1
JOIN inv_end i2 USING (item_no, loc_id)
JOIN app.cp_item_catalog ic
    ON ic.merchant_id = :merchant_id AND ic.item_no = i1.item_no
LEFT JOIN sales_qty sq ON sq.item_no = i1.item_no
CROSS JOIN (SELECT :merchant_id::uuid AS mid) s(mid)
WHERE (i1.qty_start - i2.qty_end) - COALESCE(sq.qty_sold, 0) > :shrinkage_threshold;
```

### Q-IS-02 CASH_VENDOR_PAYMENT_EXPECTED

Detects `DOC_TYP = RECVR` (receiving) documents with a cash tender that are
NOT for known vendor payment use-cases. Garden center allow-list pre-seeds
this as informational. SQL joins `cp_inventory_snapshots` before the receive
date to confirm the receiving doc increased QTY_ON_HND:

```sql
SELECT
    t.id,
    t.occurred_at,
    snap_before.qty_on_hnd AS qty_before_receive,
    snap_after.qty_on_hnd  AS qty_after_receive,
    snap_after.lst_rcv_dt
FROM sales.transactions t
JOIN sales.transaction_line_items tli ON tli.transaction_id = t.id
JOIN app.external_identities ei
    ON ei.entity_type = 'product'
   AND ei.canary_id = tli.product_id::text
   AND ei.source_code = 'counterpoint'
-- snapshot just before receive
LEFT JOIN LATERAL (
    SELECT qty_on_hnd
    FROM app.cp_inventory_snapshots
    WHERE merchant_id = t.merchant_id
      AND item_no = ei.external_id
      AND loc_id = :loc_id
      AND snapped_at < t.occurred_at
    ORDER BY snapped_at DESC LIMIT 1
) snap_before ON TRUE
-- snapshot just after receive
LEFT JOIN LATERAL (
    SELECT qty_on_hnd, lst_rcv_dt
    FROM app.cp_inventory_snapshots
    WHERE merchant_id = t.merchant_id
      AND item_no = ei.external_id
      AND loc_id = :loc_id
      AND snapped_at > t.occurred_at
    ORDER BY snapped_at LIMIT 1
) snap_after ON TRUE
WHERE t.merchant_id = :merchant_id
  AND t.source_doc_type = 'RECVR'
  AND snap_after.qty_on_hnd > snap_before.qty_on_hnd;  -- qty increased: legit receive
```

If `qty_on_hnd` did NOT increase after a RECVR document, the cash tender is
suspicious. Garden center allow-list suppresses this unless configured otherwise.

## 6. New Rule IDs (Module Q Extension)

| Rule ID | Name | Category | Severity |
|---|---|---|---|
| C-1601 | CASH_VENDOR_PAYMENT | inventory_shrink | medium |
| C-1602 | SESSION_INVENTORY_DROP | inventory_shrink | high |
| C-1603 | RECEIVE_NO_INVENTORY_INCREASE | inventory_shrink | medium |
| C-1604 | SEASONAL_WRITE_OFF_SPIKE | inventory_shrink | low |

These extend the `rule_definitions.py` entries from the Module Q Chirp
wiring SDD.

## 7. Garden-Center Vertical Context

Inventory shrinkage in a garden center has legitimate seasonal explanations:
- **Live-goods write-offs:** Plants die; inventory drops without a sale. The
  `C-1602` threshold must be tuned with the `seasonal_baselines` config in
  the allow-list profile.
- **Vendor invoice cash payments:** RECVR + cash is standard for small
  spot-buy vendors at a garden center. The `C-1601` allow-list distinguishes
  expected cash vendor payment from suspicious cash removals.
- **Receiving dock variance:** Live-goods counts are approximate. A `C-1603`
  fire on a `RECVR` that showed a smaller-than-expected inventory increase
  is noise at small quantities; threshold-based suppression applies.

The garden-center vertical profile (seeded at activation) sets:
```python
GARDEN_CENTER_ALLOW_LISTS["C-1601"] = {
    "cash_vendor_payment": True,
    "route_to_queue": "ad_hoc_vendor_review",
}
GARDEN_CENTER_ALLOW_LISTS["C-1604"] = {
    "mode": "informational",
    "seasonal_baselines": {
        "Q1": 0.08,   # 8% write-off rate acceptable
        "Q2": 0.12,
        "Q3": 0.06,
        "Q4": 0.04,
    },
}
```

## 8. Activation Ordering

Inventory polling starts in Phase C alongside document polling, but requires
Phase A1 (stores) to be complete (location IDs must be known before the
per-store poll loop runs). There is no dependency on Phase B.

## 9. Acceptance Criteria

**AC-D-01 — Snapshot creation:** After one inventory poll cycle, `cp_inventory_snapshots`
contains rows for each known location with `snapped_at` set to the poll time.

**AC-D-02 — Watermark advance:** The `poll_watermarks` row for `entity_type = 'inventory'`
advances after each poll cycle to the highest `RS_UTC_DT` seen in the response.

**AC-D-03 — Delta query:** The Q-IS-01 query returns a non-zero `unexplained_drop`
for a test scenario where 10 units of `FERN-4IN` disappear between snapshots with
only 5 sold in the session.

**AC-D-04 — Retention pruning:** The nightly prune cron deletes snapshot rows
with `snapped_at < now() - interval '90 days'`. No snapshot rows from the last
90 days are deleted.

**AC-D-05 — Multi-store loop:** An inventory poll for a merchant with 3 stores
issues 3 `GET /InventoryLocations` calls (one per store) in a single poll cycle.

## 10. Open Questions

| ID | Question | Impact |
|---|---|---|
| D-OQ-01 | `GET /InventoryLocations` without a `Loc` filter: does it return all locations at once, or does the endpoint require a location ID? If bulk is supported, the per-store loop collapses to one call. Confirm against sandbox. | Poll efficiency |
| D-OQ-02 | Write-off transactions in Counterpoint: does a live-goods write-off generate a `PS_DOC` of a specific `DOC_TYP` (e.g., `ADJUST`), or is it a direct `IM_INV` update with no document? If the latter, inventory delta is the only signal — no document evidence. | Q-IS-02 rule completeness |
| D-OQ-03 | `QTY_ON_HND` for bulk/weighed items (qty_decs > 0): are fractional quantities reflected accurately in the API response for items like bulk soil or fertilizer sold by weight? | Q-IS shrinkage threshold calibration |
| D-OQ-04 | Snapshot frequency vs. Counterpoint server load: garden center deployments may be on modest hardware. Hourly inventory polls across all items may be heavy. Confirm whether Rapid POS standard configs have rate limits or pagination on `GET /InventoryLocations`. | Poll interval setting |

---

## Related

- `docs/sdds/canary/ncr-counterpoint-item-catalog-adapter.md` — cp_item_catalog (lst_cost, is_weighed); deferred inventory polling to this SDD
- `docs/sdds/canary/ncr-counterpoint-module-q-chirp-wiring.md` — Q-IS rule family; garden-center allow-lists
- `docs/sdds/canary/ncr-counterpoint-store-station-adapter.md` — cp_known_store_ids (source of loc_id values for poll loop)
- `Brain/wiki/ncr-counterpoint-api-reference.md` — Counterpoint endpoint reference (§ Inventory)
