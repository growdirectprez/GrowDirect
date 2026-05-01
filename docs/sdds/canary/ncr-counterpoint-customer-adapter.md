---
id: sdd-cp-customer
title: NCR Counterpoint — Customer Entity Adapter (Module C)
status: draft-1
version: 0.1.0
date: 2026-04-26
author: GrowDirect Engineering
linear: GRO-TBD
companion-sdds:
  - docs/sdds/canary/ncr-counterpoint-tsp-adapter.md
  - Canary/docs/sdds/v2/identity.md
  - Canary/docs/sdds/v2/external-identities.md
  - Canary/docs/sdds/v2/data-model.md
source-endpoints:
  - GET /Customers (RS_UTC_DT watermarked bulk sync)
  - GET /Customer/{CustNo} (per-record fetch)
  - GET /CustomerControl (tier taxonomy, cached)
source-tables: AR_CUST, AR_CUST_NOTE, AR_SHIP_ADRS, AR_CUST_CARDS, AR_CTL
target-tables:
  - app.customers (existing — additive columns only)
  - app.cp_customer_profiles (new)
  - app.external_identities (existing — new rows)
  - app.poll_watermarks (existing — new entity_type)
---

# NCR Counterpoint — Customer Entity Adapter (Module C)

## 1. Purpose and scope

This SDD specifies how the Canary TSP adapter maps NCR Counterpoint customer
records (`AR_CUST`) into Canary's customer registry (`app.customers`) and the
new Counterpoint-specific attribute table (`app.cp_customer_profiles`).

It covers:
- Polling strategy and watermark mechanics for customer sync
- Field-level mapping: which AR_CUST fields enter Canary, which are excluded (PII)
  and why, which go to new tables
- The `external_identities` bridge (CUST_NO → Canary customer UUID)
- `CustomerControl` (`AR_CTL`) — tier taxonomy sync
- Module Q integration: how CATEG_COD, DISC_PCT, and ALLOW_AR_CHRG become
  loss-prevention substrates
- New table DDL and additive columns on `app.customers`
- Acceptance criteria and open questions

**Not covered here:** transaction-level customer references (CUST_NO on
Document records — covered in `ncr-counterpoint-tsp-adapter.md`), card-on-file
management (`AR_CUST_CARDS` — deferred, see Q-CRD.1), address management
for order fulfillment.

## 2. Architecture overview

```
Counterpoint REST API
  GET /Customers?StartDate={watermark}        -- RS_UTC_DT-filtered page
  GET /Customer/{CUST_NO}                      -- per-record refresh
  GET /CustomerControl                         -- tier taxonomy (24h cache)
           │
           ▼
  CounterpointCustomerPoller
  (POSAdapter subclass — poll_intervals: 3600s / entity: customer)
           │
           ├── Emits CanonicalEvent(event_type="customer.upserted")
           ├── Emits CanonicalEvent(event_type="customer_control.refreshed")
           │
           ▼
  canary:events stream (Valkey)
           │
           ▼
  Sub2 — CustomerUpsertParser
           │
           ├── PII strip: NAM, FST_NAM, LST_NAM, ADRS_1, PHONE_1, PHONE_2,
           │              CITY, STATE, ZIP_COD, LOY_CARD_NO (if == phone)
           │
           ├── Route non-PII payload to:
           │     app.customers           (LTV projection fields, first/last_seen)
           │     app.cp_customer_profiles (tier, loyalty, AR, B2B flags)
           │     app.external_identities (CUST_NO bridge)
           │
           └── Route tier taxonomy:
                 app.cp_tier_definitions  (from AR_CTL + CATEG_COD space)
```

**Key design decision — separate attribute table:** `app.customers` is the
vendor-agnostic profile table, already in production. Counterpoint-specific
fields (CATEG_COD, LOY_PTS_BAL, ALLOW_AR_CHRG, etc.) go into
`app.cp_customer_profiles` rather than polluting the core customer table.
This preserves multi-source clarity: a customer who exists in both Square and
Counterpoint has one `app.customers` row, one `app.external_identities` row
per source, and one `app.cp_customer_profiles` row for their Counterpoint
attributes.

## 3. Polling strategy

| Property | Value |
|---|---|
| Endpoint | `GET /Customers` |
| Watermark field | `RS_UTC_DT` |
| Watermark params | `StartDate={last_event_ts}` |
| Poll interval | 3600s (hourly) |
| Cold start behavior | No `StartDate` — pulls all customers. Handled by `is_initial_load=True` flag in watermark record. |
| `poll_watermarks` key | `(merchant_id, 'counterpoint', company_alias, 'customer')` |
| Error handling | Exponential backoff (5s → 40s × 3). On persistent 401/403, set merchant source status = `credential_error`; halt polling. |
| Cache behavior | Customer data is NOT server-cached. No `ServerCache` header needed on customer polls. |
| CustomerControl cadence | Once per day. Poll separately; watermark entity_type = `'customer_control'`. |

### Pagination

`GET /Customers` accepts `Page` and `Rows` query params. Adapter pages until
the response contains fewer records than `Rows` (last page signal).

Recommended page size: 500 rows. For initial load of a large customer base
(e.g., 50k records), set `Rows=500` and iterate to completion before advancing
the watermark. Write watermark only after all pages are successfully consumed.

## 4. PII enforcement

The AR_CUST record contains substantial PII. Canary's privacy-first posture
(established for Square) carries unchanged into Counterpoint:

**Strip before storing (never enter Canary's DB):**

| AR_CUST field | PII class | Notes |
|---|---|---|
| `NAM` | Full name | |
| `NAM_UPR` | Full name (normalized) | |
| `FST_NAM`, `FST_NAM_UPR` | First name | |
| `LST_NAM`, `LST_NAM_UPR` | Last name | |
| `SALUTATION` | Name prefix | |
| `ADRS_1`, `ADRS_2` | Street address | |
| `CITY`, `STATE`, `ZIP_COD` | Address components | |
| `PHONE_1`, `PHONE_2` | Phone numbers | |
| `RPT_EMAIL` | Email indicator (may imply stored email) | |
| `LOY_CARD_NO` | Loyalty card — inspect value. If == PHONE_1 (common practice), strip. Otherwise: hash+store in `app.cp_customer_profiles.loy_card_hash` for cross-ticket correlation only. |
| `CUST_FST_LST_NAM` | Derived full name | |
| `CUST_NAM_TYP` | Name format flag (indirect) | May retain if needed for record routing — assess. |
| `AR_CUST_NOTE[].NOTE` | Free-text note (RTF) | Strip. Rich text may contain PII. |
| `AR_CUST_NOTE[].NOTE_TXT` | Plain-text note | Strip. |
| `AR_SHIP_ADRS[].NAM` | Shipping name | Strip. |
| `AR_SHIP_ADRS[].ADRS_1`, `.CITY`, `.STATE`, `.ZIP_COD` | Shipping address | Strip. |

`AR_CUST_CARDS` (card-on-file): not consumed at this stage. Deferred pending
card-tokenization strategy decision (see Q-CRD.1).

**PII stripping is enforced in Sub2 at parse time**, before the raw payload
is written to `sales.evidence_records`. The raw Sub1 record stores the
complete Counterpoint response; Sub2's parsed output contains no PII.

> Implementation note: `parse_cp_customer()` receives the full AR_CUST dict
> and immediately pops all PII fields before any further processing.
> The strip list is a module-level constant — easy to audit, easy to extend.

## 5. Field mapping — app.customers (additive columns)

The existing `app.customers` table has `square_customer_id` as its
vendor-specific key. For Counterpoint customers, the vendor key goes in
`app.external_identities`. The `app.customers` table receives only the
vendor-agnostic aggregates, which ARE derivable from AR_CUST:

| app.customers column | Source | Derivation |
|---|---|---|
| `id` | Generated | UUID on first upsert |
| `merchant_id` | Context | From poll context |
| `lifetime_value_cents` | Derived from transactions | NOT from AR_CUST (Counterpoint LTV fields carry cumulative figures but in native currency, not cents; compute from synced transactions for consistency) |
| `transaction_count` | Derived from transactions | NOT from AR_CUST.NO_OF_ORDS (orders, not transactions) |
| `first_seen_at` | `AR_CUST.FST_SAL_DAT` | Direct; null → leave null |
| `last_seen_at` | `AR_CUST.LST_SAL_DAT` | Direct |
| `db_status` | Derived | `active` if RS_STAT=1; `archived` if RS_STAT=0 |

**`square_customer_id` on Counterpoint rows:** the existing column has a
NOT NULL constraint (inferred from model). Two options:
1. Add a nullable `vendor_customer_id` and deprecate `square_customer_id`
2. Keep `square_customer_id` NOT NULL and leave it `NULL`-sentinel for
   Counterpoint rows, accepting a short-term schema constraint violation

Recommended: Option 1 as part of the multi-POS schema migration (see
`ncr-counterpoint-tsp-adapter.md §5` for the same multi-POS migration pattern).
This is a Phase 0b Alembic migration (see open question R-OQ-01).

## 6. New table — app.cp_customer_profiles

Stores Counterpoint-specific non-PII customer attributes. One row per
(merchant_id, cust_no). Updated on each customer sync.

### DDL

```sql
CREATE TABLE app.cp_customer_profiles (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id         UUID NOT NULL REFERENCES app.merchants(id),
    cust_no             TEXT NOT NULL,
    categ_cod           TEXT,            -- pricing tier / customer category
    cust_typ            TEXT,            -- customer type code (A=retail, C=cash, etc.)
    allow_ar_chrg       BOOLEAN,         -- B2B account-charge flag
    allow_tkts          BOOLEAN,         -- allowed to transact
    allow_ords          BOOLEAN,         -- allowed to place orders
    allow_lwys          BOOLEAN,         -- allowed layaways
    terms_cod           TEXT,            -- payment terms (NET30, COD, etc.)
    tax_cod             TEXT,            -- assigned tax code
    disc_pct            NUMERIC(5,2),    -- blanket discount % (Module Q substrate)
    str_id              TEXT,            -- home store
    sls_rep             TEXT,            -- assigned sales rep
    -- Loyalty fields (non-PII after LOY_CARD_NO strip)
    loy_pgm_cod         TEXT,            -- loyalty program code
    loy_pts_bal         INTEGER,         -- current points balance
    tot_loy_pts_earnd   INTEGER,         -- lifetime earned
    tot_loy_pts_rdm     INTEGER,         -- lifetime redeemed
    tot_loy_pts_adj     INTEGER,         -- lifetime adjusted
    loy_card_hash       TEXT,            -- SHA-256 of LOY_CARD_NO (only if not == phone)
    lst_loy_earn_tkt_dt TIMESTAMPTZ,     -- last earning ticket datetime
    lst_loy_rdm_tkt_dt  TIMESTAMPTZ,     -- last redeem ticket datetime
    -- AR / B2B fields
    bal                 NUMERIC(12,2),   -- current AR balance
    ord_bal             NUMERIC(12,2),   -- outstanding order balance
    no_of_ords          INTEGER,         -- open order count
    lwy_bal             NUMERIC(12,2),   -- layaway balance outstanding
    no_of_lwys          INTEGER,         -- open layaway count
    no_cr_lim           BOOLEAN,         -- no credit limit flag
    cr_rate             TEXT,            -- credit rating (AAA, etc.)
    -- Source metadata
    is_ecomm_cust       BOOLEAN,
    ecomm_created_cust  BOOLEAN,
    lst_maint_dt        TIMESTAMPTZ,     -- last maintenance in Counterpoint
    lst_maint_usr_id    TEXT,            -- user who last modified
    rs_utc_dt           TIMESTAMPTZ NOT NULL,  -- watermark
    rs_stat             INTEGER,         -- record status (1=active, 0=inactive)
    -- Canary metadata
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (merchant_id, cust_no)
);

CREATE INDEX idx_cp_cust_profiles_merchant_categ
    ON app.cp_customer_profiles (merchant_id, categ_cod);

CREATE INDEX idx_cp_cust_profiles_merchant_active
    ON app.cp_customer_profiles (merchant_id, rs_stat);
```

### SQLAlchemy model (sketch)

```python
class CpCustomerProfile(AppBase, TenantMixin):
    __tablename__ = "cp_customer_profiles"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    cust_no: Mapped[str] = mapped_column(String(20), nullable=False)

    # Tier / classification
    categ_cod: Mapped[Optional[str]] = mapped_column(String(20))
    cust_typ: Mapped[Optional[str]] = mapped_column(String(10))
    allow_ar_chrg: Mapped[Optional[bool]]
    allow_tkts: Mapped[Optional[bool]]
    allow_ords: Mapped[Optional[bool]]
    allow_lwys: Mapped[Optional[bool]]
    terms_cod: Mapped[Optional[str]] = mapped_column(String(20))
    tax_cod: Mapped[Optional[str]] = mapped_column(String(20))
    disc_pct: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))
    str_id: Mapped[Optional[str]] = mapped_column(String(20))
    sls_rep: Mapped[Optional[str]] = mapped_column(String(20))

    # Loyalty
    loy_pgm_cod: Mapped[Optional[str]] = mapped_column(String(20))
    loy_pts_bal: Mapped[Optional[int]]
    tot_loy_pts_earnd: Mapped[Optional[int]]
    tot_loy_pts_rdm: Mapped[Optional[int]]
    tot_loy_pts_adj: Mapped[Optional[int]]
    loy_card_hash: Mapped[Optional[str]] = mapped_column(String(64))
    lst_loy_earn_tkt_dt: Mapped[Optional[datetime]]
    lst_loy_rdm_tkt_dt: Mapped[Optional[datetime]]

    # AR / B2B
    bal: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    ord_bal: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    no_of_ords: Mapped[Optional[int]]
    lwy_bal: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    no_of_lwys: Mapped[Optional[int]]
    no_cr_lim: Mapped[Optional[bool]]
    cr_rate: Mapped[Optional[str]] = mapped_column(String(10))

    # Source metadata
    is_ecomm_cust: Mapped[Optional[bool]]
    ecomm_created_cust: Mapped[Optional[bool]]
    lst_maint_dt: Mapped[Optional[datetime]]
    lst_maint_usr_id: Mapped[Optional[str]] = mapped_column(String(20))
    rs_utc_dt: Mapped[datetime] = mapped_column(nullable=False)
    rs_stat: Mapped[Optional[int]]

    __table_args__ = (
        UniqueConstraint("merchant_id", "cust_no", name="uq_cp_cust_profile_merchant_cust"),
        Index("idx_cp_cust_profiles_merchant_categ", "merchant_id", "categ_cod"),
    )
```

## 7. external_identities bridge

Every AR_CUST record that enters Canary gets a row in `app.external_identities`:

| external_identities column | Value |
|---|---|
| `entity_type` | `'customer'` |
| `entity_id` | Canary customer UUID (from `app.customers.id`) |
| `source_code` | `'counterpoint'` |
| `external_id` | `AR_CUST.CUST_NO` (the string account number, e.g. `"1000"`) |
| `is_primary` | `True` if this is the only source; `False` if the customer is also in Square |

**Forward resolution** (Counterpoint CUST_NO → Canary UUID): used when a
Document record references a CUST_NO — the TSP adapter resolves it via:

```python
def resolve_customer(db, merchant_id: UUID, cust_no: str) -> Optional[UUID]:
    row = db.query(ExternalIdentity).filter_by(
        merchant_id=str(merchant_id),
        source_code="counterpoint",
        entity_type="customer",
        external_id=cust_no,
    ).first()
    return UUID(row.entity_id) if row else None
```

If `cust_no` is the Counterpoint "walk-in" or "cash sale" sentinel (typically
`"CASH"` or blank), return `None` — anonymous transaction, no customer linkage.

**Reverse resolution** (Canary UUID → Counterpoint CUST_NO): used by ALX
and Fox when preparing investigation context:

```python
cp_id = db.query(ExternalIdentity.external_id).filter_by(
    merchant_id=str(merchant_id),
    entity_type="customer",
    entity_id=str(canary_customer_uuid),
    source_code="counterpoint",
).scalar()
```

## 8. CustomerControl (AR_CTL) — tier taxonomy

`GET /CustomerControl` returns the system-level AR configuration. The
fields relevant to Canary:

| AR_CTL field | Use |
|---|---|
| `USE_LOY_PGMS` | Boolean — is loyalty active for this tenant? |
| `NO_MAX_WRTOFF_AMT` | AR write-off max flag (informational for Module Q) |
| `RS_UTC_DT` | Watermark for `customer_control` entity_type |

CustomerControl does not contain the CATEG_COD value space — that lives
implicitly in the set of distinct CATEG_COD values across AR_CUST records.
**Tier taxonomy is bootstrapped from initial customer sync** (distinct
CATEG_COD values → `app.cp_tier_definitions`). New tiers discovered during
incremental sync are inserted automatically.

### app.cp_tier_definitions

```sql
CREATE TABLE app.cp_tier_definitions (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID NOT NULL REFERENCES app.merchants(id),
    categ_cod   TEXT NOT NULL,
    discovered_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    record_count  INTEGER NOT NULL DEFAULT 0,
    UNIQUE (merchant_id, categ_cod)
);
```

Populated by: `CustomerControlSyncService.sync_tier_definitions(merchant_id)`.
Called after each full customer page batch completes.

## 9. Module Q integration

The customer attributes synced by this adapter are the substrate for several
Chirp detection rules that apply to the garden center vertical (and generalize
to any Counterpoint vertical with multi-tier pricing):

### Rule substrate map

| Field | Rule family | Detection logic |
|---|---|---|
| `categ_cod` | Q-M.4 (Customer-Tier Anomaly) | If ticket-level discount or pricing tier on PS_DOC_LIN exceeds what `categ_cod` authorizes per the tier policy, flag. |
| `disc_pct` | Q-M.3 (Blanket Discount Override) | If `PS_DOC_HDR.DISC_AMT / subtotal > disc_pct + threshold`, flag as unauthorized discount. |
| `allow_ar_chrg` | Q-AR.1 (Unauthorized Charge Account) | If a Document records AR charge (`PMT_COD` = AR tender) against a customer where `allow_ar_chrg=False`, flag. |
| `allow_tkts` | Q-AR.2 (Suspended Customer Sale) | If Document references a CUST_NO where `allow_tkts=False`, flag. |
| `loy_pts_bal` | Q-LOY.1 (Loyalty Balance Manipulation) | If earned points on a ticket exceed expected earn rate × ticket total by > threshold, compare against `loy_pts_bal` delta. |
| `terms_cod` | Q-AR.3 (Terms Mismatch) | If AR charge terms on Document do not match `terms_cod` for the customer, flag for manual review. |
| `cust_typ` | Q-M.5 (Customer Type Misclassification) | If a `CUST_TYP=C` (cash) customer accumulates AR balance > 0, flag. |

Rule definitions are seeded into `app.detection_rules` via Chirp catalog.
The substrate columns above are read at detection time from
`app.cp_customer_profiles` joined through `app.external_identities`.

## 10. Event types in the canary:events stream

| CanonicalEvent.event_type | Trigger |
|---|---|
| `customer.upserted` | New or updated customer from `GET /Customers` watermark poll |
| `customer.initial_load_complete` | Emitted once after initial bulk sync completes |
| `customer_control.refreshed` | After successful `GET /CustomerControl` poll |

Sub2 dispatch:

```python
EVENT_TYPE_PARSERS: dict[tuple[str, str], Callable] = {
    ...  # existing entries
    ("counterpoint", "customer.upserted"):          parse_cp_customer,
    ("counterpoint", "customer_control.refreshed"): parse_cp_customer_control,
}
```

## 11. Parser function shapes

### parse_cp_customer

```python
def parse_cp_customer(
    event: CanonicalEvent,
    db: Session,
) -> CpCustomerParseResult:
    """
    Input:  CanonicalEvent.payload = AR_CUST dict (full record, as-polled)
    Output: CpCustomerParseResult containing:
              - customer_id: UUID (created or resolved)
              - cust_no: str
              - profile: CpCustomerProfile (upsert target)
              - ext_identity: ExternalIdentity (upsert target)
              - first_seen_at / last_seen_at: Optional[datetime]
    Side effects: none (caller commits)
    PII strip: applied immediately at function entry (module-level PII_STRIP_FIELDS constant)
    """
```

### PII strip constant

```python
PII_STRIP_FIELDS = frozenset({
    "NAM", "NAM_UPR", "FST_NAM", "FST_NAM_UPR", "LST_NAM", "LST_NAM_UPR",
    "SALUTATION", "ADRS_1", "ADRS_2", "CITY", "STATE", "ZIP_COD",
    "PHONE_1", "PHONE_2", "RPT_EMAIL",
    "CUST_FST_LST_NAM", "CUST_NAM_TYP",
    # Notes and addresses stripped at array level — not individual fields
    # LOY_CARD_NO handled conditionally (see §4)
})

def strip_pii(record: dict) -> dict:
    clean = {k: v for k, v in record.items() if k not in PII_STRIP_FIELDS}
    clean.pop("AR_CUST_NOTE", None)
    clean.pop("AR_SHIP_ADRS", None)
    clean.pop("AR_CUST_CARDS", None)
    # Conditional LOY_CARD_NO handling
    loy_card = clean.pop("LOY_CARD_NO", None)
    phone = record.get("PHONE_1", "")
    if loy_card and loy_card != phone:
        import hashlib
        clean["loy_card_hash"] = hashlib.sha256(loy_card.encode()).hexdigest()
    return clean
```

## 12. Upsert pattern

Customer records are upserted (not appended) — a customer may be polled
multiple times as their record changes. The upsert keyed on
`(merchant_id, cust_no)` for `cp_customer_profiles`, and
`(merchant_id, source_code, entity_type, external_id)` for `external_identities`.

For `app.customers`, `first_seen_at` is set only on initial insert
(never overwritten backward). `last_seen_at` is updated if the polled value
is more recent.

PostgreSQL upsert (via SQLAlchemy `on_conflict_do_update`):

```python
stmt = pg_insert(CpCustomerProfile).values(**profile_data)
stmt = stmt.on_conflict_do_update(
    constraint="uq_cp_cust_profile_merchant_cust",
    set_={k: stmt.excluded[k] for k in UPSERT_COLUMNS},
)
db.execute(stmt)
```

`UPSERT_COLUMNS` excludes `id`, `merchant_id`, `cust_no`, `created_at`.

## 13. Additive columns on app.customers (Alembic migration)

The existing `square_customer_id` column will be made nullable in the
multi-POS schema migration (shared with the transaction adapter migration).
No additional columns are added to `app.customers` for Counterpoint —
the Counterpoint-specific data lives in `cp_customer_profiles`.

Migration that accompanies this SDD:

```python
# Alembic migration: make square_customer_id nullable (multi-POS prep)
op.alter_column("customers", "square_customer_id", nullable=True, schema="app")
op.alter_column("customers", "first_seen_at", nullable=True, schema="app")
op.alter_column("customers", "last_seen_at", nullable=True, schema="app")
```

## 14. poll_watermarks entry

New entity_type rows added by this adapter:

```sql
-- Inserted by adapter.seed_data() on first activation for a merchant
INSERT INTO app.poll_watermarks
    (merchant_id, source_code, company_alias, entity_type, last_polled_at)
VALUES
    ({merchant_id}, 'counterpoint', {company_alias}, 'customer',        now()),
    ({merchant_id}, 'counterpoint', {company_alias}, 'customer_control', now())
ON CONFLICT DO NOTHING;
```

## 15. New tables summary — Alembic migration checklist

| Table | Schema | Action | Purpose |
|---|---|---|---|
| `cp_customer_profiles` | app | CREATE | Counterpoint-specific non-PII attributes |
| `cp_tier_definitions` | app | CREATE | Distinct CATEG_COD taxonomy per merchant |
| `customers.square_customer_id` | app | ALTER nullable | Multi-POS migration (shared with TSP adapter) |

## 16. Acceptance criteria

**AC-R-01 — Initial load:** A fresh tenant activation with 5 seed customers
in Counterpoint results in 5 `app.customers` rows, 5 `app.cp_customer_profiles`
rows, and 5 `app.external_identities` rows after the first full poll cycle.
No PII fields appear in any Canary table.

**AC-R-02 — Incremental sync:** After updating one customer's CATEG_COD in
Counterpoint (simulated via direct DB edit), the next hourly poll updates the
corresponding `cp_customer_profiles.categ_cod`. Other rows are unchanged.
Watermark advances to the modified customer's RS_UTC_DT.

**AC-R-03 — Forward resolution:** A Document record with CUST_NO `"1000"`
resolves to the correct Canary customer UUID via `resolve_customer()`.
CUST_NO `"CASH"` (walk-in sentinel) returns `None` without error.

**AC-R-04 — PII strip:** `parse_cp_customer()` returns a result with no
`NAM`, `FST_NAM`, `LST_NAM`, `ADRS_1`, `PHONE_1`, `CITY`, `STATE`,
`ZIP_COD`, `AR_CUST_NOTE`, `AR_SHIP_ADRS`, or `AR_CUST_CARDS` keys
present in any field of the stored profile or evidence record.

**AC-R-05 — LOY_CARD_NO handling:** If `LOY_CARD_NO == PHONE_1`, neither
field is stored and `loy_card_hash` is NULL. If `LOY_CARD_NO != PHONE_1`
and is non-empty, `loy_card_hash` is populated with the SHA-256 hex digest.

**AC-R-06 — Module Q substrate:** For a customer with `categ_cod="RETAIL"`,
Chirp rule Q-M.4 query returns the correct tier for the test merchant. For a
customer with `allow_ar_chrg=False`, Q-AR.1 rule evaluates as expected when
a Document contains AR tender for that CUST_NO.

**AC-R-07 — CustomerControl sync:** After a successful
`customer_control.refreshed` event, `app.cp_tier_definitions` contains one
row per distinct CATEG_COD observed in the merchant's customer base.

**AC-R-08 — Multi-POS coexistence:** A customer known to both Square and
Counterpoint has exactly one `app.customers` row and two `external_identities`
rows: one for `source_code='square'`, one for `source_code='counterpoint'`.
`cp_customer_profiles` exists for the Counterpoint identity only.

## 17. Open questions

| ID | Question | Impact |
|---|---|---|
| R-OQ-01 | Multi-POS Alembic migration timing — does `square_customer_id` nullable alter ship with the TSP adapter migration or separately? | Schema migration coordination |
| R-OQ-02 | Walk-in / anonymous customer sentinel value in the tenant's Counterpoint instance. Is it always `"CASH"`, or is it configurable per company? If configurable, need a `pos_tenant_credentials` field to store it. | Forward resolution correctness |
| R-OQ-03 | `LOY_CARD_NO` format in garden center deployments. Is it always a phone number, or are barcode-based cards used? Impacts strip vs. hash decision. | PII enforcement |
| R-OQ-04 | Counterpoint customer update rate. A 31-store retailer with 50k customers: how many customers change per hour? Determines if hourly poll interval is efficient or if a lower cadence (e.g., 4h) is appropriate for staging. | Poll interval tuning |
| R-OQ-05 | Does Counterpoint expose a "customer created" event type (via RS_STAT transitions) that would let Canary distinguish new customers from updates? Or is RS_UTC_DT the only signal? | Bootstrapping vs. incremental differentiation |
| R-OQ-06 | B2B pricing tiers: does CATEG_COD directly encode the contractor vs. retail distinction for garden center deployments, or does the retailer use a separate custom field? Clarify with Bart. | Module Q rule accuracy (Q-M.4) |

---

## Related

- `docs/sdds/canary/ncr-counterpoint-tsp-adapter.md` — Document/sales mapping; references CUST_NO resolution from this SDD
- `Canary/docs/sdds/v2/identity.md` — Identity system; merchant registration; OAuth
- `Canary/docs/sdds/v2/external-identities.md` — External identity bridge; cross-DB linking design
- `Canary/docs/sdds/v2/data-model.md` — Core `app.customers` table definition
- `Brain/wiki/canary-module-c-customer.md` — Module C wiki overview
- `Brain/wiki/ncr-counterpoint-api-reference.md` — Counterpoint endpoint reference (§ Module C — Customer)
- `Brain/wiki/canary-module-q-counterpoint-rule-catalog.md` — Module Q rules referencing R substrate (Q-M.3, Q-M.4, Q-AR.1–3)
- `Brain/wiki/garden-center-operating-reality.md` — Vertical context; multi-tier customer pricing
