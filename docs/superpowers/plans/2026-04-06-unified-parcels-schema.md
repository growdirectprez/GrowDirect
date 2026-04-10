# Unified Parcels Schema Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Consolidate parcels, research_parcels, and listings property data into one unified `parcels` table.

**Architecture:** Widen `parcels` with real columns for core queryable fields + JSONB `enrichment` column for deep ATTOM data. Strip duplicate property columns from `listings`. Drop `research_parcels`. Two Alembic migrations (A: additive, B: destructive).

**Tech Stack:** SQLAlchemy 2.0 `Mapped[]`, PostgreSQL JSONB, Alembic, pytest

**Spec:** `docs/superpowers/specs/2026-04-06-unified-parcels-schema-design.md`

---

## Chunk 1: Foundation — normalize_apn + Parcel model widening

### Task 1: Extract normalize_apn to canonical location

**Files:**
- Create: `cove/parcels/apn.py`
- Modify: `scripts/import_crmls.py`
- Modify: `scripts/fetch_gis_parcels.py`
- Modify: `tests/test_angel_import.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_apn.py`:

```python
"""Tests for canonical APN normalization utility."""
import pytest
from cove.parcels.apn import normalize_apn


class TestNormalizeApn:
    def test_ten_digit_to_dashed(self):
        assert normalize_apn("7573006008") == "7573-006-008"

    def test_already_dashed(self):
        assert normalize_apn("7573-006-008") == "7573-006-008"

    def test_empty_returns_none(self):
        assert normalize_apn("") is None
        assert normalize_apn(None) is None

    def test_whitespace_stripped(self):
        assert normalize_apn("  7573006008  ") == "7573-006-008"

    def test_seven_digit_not_normalized(self):
        result = normalize_apn("7573006")
        assert result == "7573006"

    def test_thirteen_digit(self):
        result = normalize_apn("7573006008001")
        assert result == "7573-006-008"

    def test_with_alpha_chars(self):
        assert normalize_apn("7556016001") == "7556-016-001"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `docker exec cove_flask python3 -m pytest tests/test_apn.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'cove.parcels.apn'`

- [ ] **Step 3: Create canonical normalize_apn**

Create `cove/parcels/apn.py`:

```python
"""Canonical APN normalization — single source of truth.

All scripts, models, and services import normalize_apn from here.
Format: XXXX-XXX-XXX (dashed, 10 significant digits).
"""
import re


def normalize_apn(raw: str | None) -> str | None:
    """Convert any APN format to Cove canonical: XXXX-XXX-XXX."""
    if not raw:
        return None
    digits = re.sub(r"[^0-9]", "", raw.strip())
    if len(digits) == 10:
        return f"{digits[:4]}-{digits[4:7]}-{digits[7:]}"
    if len(digits) >= 13:
        return f"{digits[:4]}-{digits[4:7]}-{digits[7:10]}"
    return digits if digits else None
```

- [ ] **Step 4: Run test to verify it passes**

Run: `docker exec cove_flask python3 -m pytest tests/test_apn.py -v`
Expected: 7 PASSED

- [ ] **Step 5: Update import sites to use canonical location**

In `scripts/import_crmls.py`, replace the `normalize_apn` function definition (lines 28-41) with:
```python
from cove.parcels.apn import normalize_apn
```

In `scripts/fetch_gis_parcels.py`, replace the `normalize_apn` function (lines 82-87) with:
```python
from cove.parcels.apn import normalize_apn
```

In `tests/test_angel_import.py`, update the import (line 37):
```python
from scripts.import_crmls import (
    # normalize_apn removed — now imported from cove.parcels.apn
    parse_date,
    parse_date_only,
    parse_int,
    parse_float,
    build_address,
    build_agent_name,
    import_batch,
)
from cove.parcels.apn import normalize_apn
```

- [ ] **Step 6: Run all affected tests**

Run: `docker exec cove_flask python3 -m pytest tests/test_apn.py tests/test_angel_import.py -v`
Expected: ALL PASSED

- [ ] **Step 7: Commit**

```bash
git add cove/parcels/apn.py tests/test_apn.py scripts/import_crmls.py scripts/fetch_gis_parcels.py tests/test_angel_import.py
git commit -m "refactor: extract normalize_apn to cove/parcels/apn.py — single source of truth"
```

---

### Task 2: Widen Parcel model with new columns

**Files:**
- Modify: `cove/models/parcel.py`

- [ ] **Step 1: Write test for new Parcel columns**

Add to `tests/test_apn.py` (or create `tests/test_parcel_unified.py`):

```python
"""Tests for unified Parcel model — new columns from listings + ATTOM."""
from datetime import datetime
import pytest
from cove.models.parcel import Parcel


class TestParcelUnifiedColumns:
    def test_create_parcel_with_property_fields(self, db_session):
        parcel = Parcel(
            apn="7573-006-008",
            address="100 Sea Cove Dr",
            street="Sea Cove",
            city="Rancho Palos Verdes",
            property_type="SFR",
            bedrooms=4,
            bathrooms=3.0,
            sqft=2800,
            lot_size_sqft=15000,
            year_built=1965,
            architectural_style="Contemporary",
            mls_area="167 - PV Dr East",
            subdivision="14649",
        )
        db_session.add(parcel)
        db_session.flush()

        fetched = db_session.get(Parcel, "7573-006-008")
        assert fetched.property_type == "SFR"
        assert fetched.bedrooms == 4
        assert fetched.bathrooms == 3.0
        assert fetched.sqft == 2800
        assert fetched.mls_area == "167 - PV Dr East"

    def test_enrichment_jsonb(self, db_session):
        parcel = Parcel(
            apn="7573-006-009",
            address="101 Sea Cove Dr",
            street="Sea Cove",
            enrichment={"attom": {"property": {"summary": {"yearbuilt": 1965}}}},
            enrichment_source="attom",
            enriched_at=datetime.utcnow(),
        )
        db_session.add(parcel)
        db_session.flush()

        fetched = db_session.get(Parcel, "7573-006-009")
        assert fetched.enrichment["attom"]["property"]["summary"]["yearbuilt"] == 1965
        assert fetched.enrichment_source == "attom"
        assert fetched.enriched_at is not None

    def test_market_value_column(self, db_session):
        parcel = Parcel(
            apn="7573-006-010",
            address="102 Sea Cove Dr",
            street="Sea Cove",
            market_value=2500000,
            last_sale_price=2000000,
            last_sale_date=datetime(2024, 6, 15),
        )
        db_session.add(parcel)
        db_session.flush()

        fetched = db_session.get(Parcel, "7573-006-010")
        assert fetched.market_value == 2500000
        assert fetched.last_sale_date.year == 2024

    def test_city_no_default(self, db_session):
        """City should not default to RPV for South Bay expansion."""
        parcel = Parcel(
            apn="4100-001-001",
            address="100 Manhattan Ave",
            street="Manhattan",
            city="Manhattan Beach",
            zip_code="90266",
        )
        db_session.add(parcel)
        db_session.flush()

        fetched = db_session.get(Parcel, "4100-001-001")
        assert fetched.city == "Manhattan Beach"
        assert fetched.zip_code == "90266"

    def test_city_is_none_when_omitted(self, db_session):
        """City should be None, not 'Rancho Palos Verdes', when not specified."""
        parcel = Parcel(
            apn="4100-001-002",
            address="200 Manhattan Ave",
            street="Manhattan",
        )
        db_session.add(parcel)
        db_session.flush()

        fetched = db_session.get(Parcel, "4100-001-002")
        assert fetched.city is None

    def test_parcel_listing_relationship(self, db_session):
        from cove.models.listing import Listing
        parcel = Parcel(
            apn="7573-006-011",
            address="103 Sea Cove Dr",
            street="Sea Cove",
        )
        db_session.add(parcel)
        db_session.flush()

        listing = Listing(
            mls_number="REL001",
            apn="7573-006-011",
            status="Active",
            source="crmls_tp",
        )
        db_session.add(listing)
        db_session.flush()

        assert len(parcel.listings) == 1
        assert listing.parcel.apn == "7573-006-011"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `docker exec cove_flask python3 -m pytest tests/test_parcel_unified.py -v`
Expected: FAIL — missing columns

- [ ] **Step 3: Update Parcel model**

Modify `cove/models/parcel.py` — add new columns after existing ones:

```python
from datetime import datetime
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from cove.extensions import db


class Parcel(db.Model):
    __tablename__ = "parcels"

    # APN is the primary key — the universal property identifier
    apn: Mapped[str] = mapped_column(String(20), primary_key=True)

    # Org-scoped for WPBCA members; NULL for surrounding lots
    organization_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("organizations.id"), nullable=True
    )

    address: Mapped[str] = mapped_column(String(255), nullable=False)
    street: Mapped[str] = mapped_column(String(100), nullable=False)
    lot_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    state: Mapped[str] = mapped_column(String(2), default="CA")
    zip_code: Mapped[str | None] = mapped_column(String(10), nullable=True)

    # Property characteristics (from CRMLS / ATTOM)
    property_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    bedrooms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    bathrooms: Mapped[float | None] = mapped_column(Float, nullable=True)
    sqft: Mapped[int | None] = mapped_column(Integer, nullable=True)
    architectural_style: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Property data (from county)
    lot_size_sqft: Mapped[int | None] = mapped_column(Integer, nullable=True)
    year_built: Mapped[int | None] = mapped_column(Integer, nullable=True)
    owner_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    use_description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    zoning: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Valuation
    assessed_land_value: Mapped[int | None] = mapped_column(Integer, nullable=True)
    assessed_improvement_value: Mapped[int | None] = mapped_column(Integer, nullable=True)
    market_value: Mapped[int | None] = mapped_column(Integer, nullable=True)
    last_sale_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_sale_price: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Location
    geometry: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    center_lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    center_lon: Mapped[float | None] = mapped_column(Float, nullable=True)
    mls_area: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    subdivision: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Enrichment (ATTOM + other sources)
    enrichment: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    enrichment_source: Mapped[str | None] = mapped_column(String(100), nullable=True)
    enriched_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Legal references
    tract_number: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True)
    map_book: Mapped[str | None] = mapped_column(String(10), nullable=True)
    legal_description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Cove-specific classification
    is_association_member: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    is_combined: Mapped[bool] = mapped_column(Boolean, default=False)
    combined_with_apn: Mapped[str | None] = mapped_column(
        String(20), ForeignKey("parcels.apn"), nullable=True
    )

    # Lot H research
    lot_h_status: Mapped[str] = mapped_column(
        String(30), nullable=False, default="unknown", index=True
    )
    lot_h_on_title: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    # Metadata
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    member: Mapped["Member | None"] = relationship("Member", back_populates="parcel", uselist=False)
    organization: Mapped["Organization | None"] = relationship("Organization", backref="parcels")
    profile: Mapped["ParcelProfile | None"] = relationship("ParcelProfile", back_populates="parcel", uselist=False)
    tag_assignments: Mapped[list["ParcelTagAssignment"]] = relationship("ParcelTagAssignment", back_populates="parcel")
    comments: Mapped[list["ParcelComment"]] = relationship("ParcelComment", back_populates="parcel", order_by="ParcelComment.created_at.desc()")
    contacts: Mapped[list["ParcelContact"]] = relationship(
        "ParcelContact", back_populates="parcel", order_by="ParcelContact.display_order"
    )
    listings: Mapped[list["Listing"]] = relationship(
        "Listing", back_populates="parcel", order_by="Listing.list_date.desc()"
    )

    @property
    def total_assessed_value(self) -> int:
        return (self.assessed_land_value or 0) + (self.assessed_improvement_value or 0)

    @property
    def address_num(self) -> str | None:
        import re
        match = re.match(r"(\d+)", self.address or "")
        return match.group(1) if match else None

    @property
    def lot_email(self) -> str:
        num = self.address_num or str(self.lot_number)
        street_compact = self.street.replace(" ", "")
        domain = "abalonecove.org"
        if self.organization and self.organization.domain:
            domain = self.organization.domain
        return f"{num}{street_compact}@{domain}"

    @property
    def lot_h_status_label(self) -> str:
        labels = {
            "lot_h_direct": "Lot H — Direct Reference",
            "lot_h_probable": "Lot H — Probable",
            "lot_h_confirmed": "Lot H — Confirmed",
            "excepted": "Excepted Tract",
            "released": "Restrictions Released",
            "not_covered": "Not Covered",
            "unknown": "Needs Research",
        }
        return labels.get(self.lot_h_status, self.lot_h_status)

    def __repr__(self):
        return f"<Parcel {self.apn} — {self.address}>"
```

**Key changes from current model:**
- Removed `city` default ("Rancho Palos Verdes") — made nullable
- Removed `zip_code` default ("90275") — already nullable
- Renamed `transfer_date` → `last_sale_date`
- Added: `property_type`, `bedrooms`, `bathrooms`, `sqft`, `architectural_style`
- Added: `mls_area` (indexed), `subdivision`
- Added: `market_value`
- Added: `enrichment` (JSONB), `enrichment_source`, `enriched_at`
- Added: `listings` relationship

- [ ] **Step 4: Run test to verify it passes (model only — no migration yet)**

The test won't pass yet because the database schema hasn't been updated. This is expected. We need the migration first (Task 3).

- [ ] **Step 5: Commit model changes**

```bash
git add cove/models/parcel.py tests/test_parcel_unified.py
git commit -m "feat: widen Parcel model — property, location, enrichment columns for unified schema"
```

---

### Task 3: Migration A — Additive schema changes

**Files:**
- Create: `migrations/versions/xxxx_unified_parcels_a_additive.py` (via Alembic)

- [ ] **Step 1: Generate Alembic migration**

Run: `docker exec cove_flask python3 -m alembic revision --autogenerate -m "unified parcels A — add property, enrichment columns"`

- [ ] **Step 2: Review and edit generated migration**

The auto-generated migration should include:
- Add columns to `parcels`: `property_type`, `bedrooms`, `bathrooms`, `sqft`, `architectural_style`, `mls_area`, `subdivision`, `market_value`, `enrichment` (JSONB), `enrichment_source`, `enriched_at`
- Rename `transfer_date` → `last_sale_date`
- Add indexes on `mls_area`, `city`, `zip_code`, `property_type`
- Alter `city` to remove server_default

Verify the migration includes the rename (Alembic often generates drop+add instead of rename). If so, manually replace with:
```python
op.alter_column('parcels', 'transfer_date', new_column_name='last_sale_date')
```

Also verify that `enrichment` uses `postgresql.JSONB` not `sa.JSON`.

Add data migration steps after schema changes:

```python
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # 1. Add new columns to parcels
    op.add_column('parcels', sa.Column('property_type', sa.String(50), nullable=True))
    op.add_column('parcels', sa.Column('bedrooms', sa.Integer(), nullable=True))
    op.add_column('parcels', sa.Column('bathrooms', sa.Float(), nullable=True))
    op.add_column('parcels', sa.Column('sqft', sa.Integer(), nullable=True))
    op.add_column('parcels', sa.Column('architectural_style', sa.String(255), nullable=True))
    op.add_column('parcels', sa.Column('mls_area', sa.String(100), nullable=True))
    op.add_column('parcels', sa.Column('subdivision', sa.String(255), nullable=True))
    op.add_column('parcels', sa.Column('market_value', sa.Integer(), nullable=True))
    op.add_column('parcels', sa.Column('enrichment', postgresql.JSONB(), nullable=True))
    op.add_column('parcels', sa.Column('enrichment_source', sa.String(100), nullable=True))
    op.add_column('parcels', sa.Column('enriched_at', sa.DateTime(), nullable=True))

    # 2. Rename transfer_date -> last_sale_date
    op.alter_column('parcels', 'transfer_date', new_column_name='last_sale_date')

    # 3. Remove city default (was "Rancho Palos Verdes")
    op.alter_column('parcels', 'city', server_default=None, nullable=True)
    op.alter_column('parcels', 'zip_code', server_default=None)

    # 4. Add new indexes
    op.create_index('ix_parcels_mls_area', 'parcels', ['mls_area'])
    op.create_index('ix_parcels_city', 'parcels', ['city'])
    op.create_index('ix_parcels_zip_code', 'parcels', ['zip_code'])
    op.create_index('ix_parcels_property_type', 'parcels', ['property_type'])

    # 5. Migrate research_parcels data (if table exists)
    conn = op.get_bind()
    from sqlalchemy import inspect as sa_inspect
    inspector = sa_inspect(conn)
    if inspector.has_table('research_parcels'):
        conn.execute(sa.text("""
            INSERT INTO parcels (apn, address, street, city, year_built, owner_name,
                use_description, tract_number, map_book, legal_description,
                center_lat, center_lon, lot_h_status, lot_h_on_title,
                assessed_land_value, assessed_improvement_value, notes,
                created_at, updated_at)
            SELECT rp.apn, COALESCE(rp.address, 'Unknown'), COALESCE(rp.address, 'Unknown'),
                rp.city, rp.year_built, NULL,
                rp.use_description, rp.tract_number, rp.map_book, rp.legal_description,
                rp.center_lat, rp.center_lon, COALESCE(rp.lot_h_status, 'unknown'), rp.lot_h_on_title,
                rp.land_value, rp.improvement_value, rp.notes,
                COALESCE(rp.created_at, NOW()), NOW()
            FROM research_parcels rp
            WHERE rp.apn NOT IN (SELECT apn FROM parcels)
        """))

    # 6. Migrate listings property data into parcels (most recent listing per APN wins)
    conn.execute(sa.text("""
        WITH ranked AS (
            SELECT *,
                ROW_NUMBER() OVER (PARTITION BY apn ORDER BY
                    CASE WHEN close_date IS NOT NULL THEN close_date
                         ELSE list_date END DESC NULLS LAST
                ) as rn
            FROM listings
            WHERE apn IS NOT NULL
        )
        UPDATE parcels p SET
            property_type = COALESCE(p.property_type, r.property_type),
            bedrooms = COALESCE(p.bedrooms, r.bedrooms),
            bathrooms = COALESCE(p.bathrooms, r.bathrooms),
            sqft = COALESCE(p.sqft, r.sqft),
            lot_size_sqft = COALESCE(p.lot_size_sqft, r.lot_sqft),
            architectural_style = COALESCE(p.architectural_style, r.architectural_style),
            mls_area = COALESCE(p.mls_area, r.mls_area),
            subdivision = COALESCE(p.subdivision, r.subdivision),
            center_lat = COALESCE(p.center_lat, r.latitude),
            center_lon = COALESCE(p.center_lon, r.longitude),
            enrichment_source = CASE
                WHEN p.enrichment_source IS NULL THEN 'crmls'
                WHEN p.enrichment_source NOT LIKE '%crmls%' THEN p.enrichment_source || ',crmls'
                ELSE p.enrichment_source
            END,
            updated_at = NOW()
        FROM ranked r
        WHERE r.apn = p.apn AND r.rn = 1
    """))

    # 7. Create parcel rows for CRMLS APNs not in parcels
    conn.execute(sa.text("""
        WITH ranked AS (
            SELECT *,
                ROW_NUMBER() OVER (PARTITION BY apn ORDER BY
                    CASE WHEN close_date IS NOT NULL THEN close_date
                         ELSE list_date END DESC NULLS LAST
                ) as rn
            FROM listings
            WHERE apn IS NOT NULL
              AND apn NOT IN (SELECT apn FROM parcels)
        )
        INSERT INTO parcels (apn, address, street, city, zip_code,
            property_type, bedrooms, bathrooms, sqft, lot_size_sqft,
            year_built, architectural_style, center_lat, center_lon,
            mls_area, subdivision, enrichment_source, created_at, updated_at)
        SELECT apn, address, address, city, zip_code,
            property_type, bedrooms, bathrooms, sqft, lot_sqft,
            year_built, architectural_style, latitude, longitude,
            mls_area, subdivision, 'crmls', NOW(), NOW()
        FROM ranked
        WHERE rn = 1
    """))
```

**Note:** The `street` column is NOT NULL. For CRMLS-sourced parcels, we set `street = address` as a fallback (the full address string). A future pass can parse street name from the address.

- [ ] **Step 3: Run migration**

Run: `docker exec cove_flask python3 -m alembic upgrade head`
Expected: Migration completes without errors

- [ ] **Step 4: Verify data migration**

Run: `docker exec cove_flask python3 -c "
from cove import create_app; from cove.extensions import db; from cove.models.parcel import Parcel
app = create_app('dev')
with app.app_context():
    total = db.session.query(Parcel).count()
    with_mls = db.session.query(Parcel).filter(Parcel.mls_area.isnot(None)).count()
    with_enrich = db.session.query(Parcel).filter(Parcel.enrichment_source.isnot(None)).count()
    print(f'Total parcels: {total}')
    print(f'With MLS area: {with_mls}')
    print(f'With enrichment source: {with_enrich}')
"`

Expected: Total parcels > 6,900 (5,514 original + ~1,458 from CRMLS)

- [ ] **Step 5: Run model tests**

Run: `docker exec cove_flask python3 -m pytest tests/test_parcel_unified.py tests/test_apn.py -v`
Expected: ALL PASSED

- [ ] **Step 6: Commit**

```bash
git add migrations/versions/ cove/models/parcel.py
git commit -m "feat: migration A — add property, enrichment columns to parcels, migrate listings data"
```

---

## Chunk 2: Listings cleanup + Migration B

### Task 4: Update Listing model — remove property columns, add FK + relationship

**Files:**
- Modify: `cove/models/listing.py`
- Modify: `tests/test_angel_import.py`
- Create: `tests/test_parcel_listing_join.py`

- [ ] **Step 1: Write test for cleaned Listing model**

Add `tests/test_parcel_listing_join.py`:

```python
"""Tests for Listing ↔ Parcel relationship after column cleanup."""
from datetime import date
import pytest
from cove.models.parcel import Parcel
from cove.models.listing import Listing


class TestListingParcelJoin:
    def test_listing_joins_to_parcel(self, db_session):
        parcel = Parcel(
            apn="7573-006-008", address="100 Sea Cove Dr", street="Sea Cove",
            city="RPV", bedrooms=4, bathrooms=3.0, sqft=2800,
        )
        db_session.add(parcel)
        db_session.flush()

        listing = Listing(
            mls_number="JOIN001", apn="7573-006-008", status="Active",
            list_price=2500000, source="crmls_tp",
        )
        db_session.add(listing)
        db_session.flush()

        # Property data comes from parcel
        assert listing.parcel.bedrooms == 4
        assert listing.parcel.address == "100 Sea Cove Dr"
        assert listing.parcel.sqft == 2800

    def test_listing_no_address_column(self):
        """Listing should not have address as a direct column."""
        from sqlalchemy import inspect as sa_inspect
        mapper = sa_inspect(Listing)
        assert 'address' not in [c.key for c in mapper.columns]

    def test_price_per_sqft_from_parcel(self, db_session):
        parcel = Parcel(
            apn="7573-006-012", address="104 Sea Cove Dr", street="Sea Cove",
            sqft=2000,
        )
        db_session.add(parcel)
        db_session.flush()

        listing = Listing(
            mls_number="PPSF003", apn="7573-006-012", status="Closed",
            close_price=2000000, source="crmls_tp",
        )
        db_session.add(listing)
        db_session.flush()

        assert listing.price_per_sqft == 1000

    def test_repr_uses_mls_number(self, db_session):
        listing = Listing(
            mls_number="REPR002", status="Active", source="crmls_tp",
        )
        r = repr(listing)
        assert "REPR002" in r
        assert "Active" in r
```

- [ ] **Step 2: Update Listing model**

Modify `cove/models/listing.py` — remove property columns, update properties and repr:

```python
"""Angel module — MLS listing and listing event models.

Tables live in the cove database. APN links listings to Cove parcels.
Listing is a pure MLS transaction record — property data lives on Parcel.
Schema reference: docs/superpowers/specs/2026-04-06-unified-parcels-schema-design.md
"""

import uuid
from datetime import date, datetime
from sqlalchemy import String, Integer, Float, DateTime, Date, ForeignKey, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from cove.extensions import db


class Listing(db.Model):
    """One row per MLS listing. Property data on Parcel via APN join."""

    __tablename__ = "listings"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    mls_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    apn: Mapped[str | None] = mapped_column(
        String(20), ForeignKey("parcels.apn"), nullable=True, index=True
    )

    # Listing state
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    list_price: Mapped[int | None] = mapped_column(Integer, nullable=True)
    close_price: Mapped[int | None] = mapped_column(Integer, nullable=True)
    list_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    close_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    dom: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cdom: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Agents
    listing_agent_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    listing_agent_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    listing_office: Mapped[str | None] = mapped_column(String(255), nullable=True)
    buyer_agent_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    buyer_agent_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    buyer_office: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Financials
    hoa_fee: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tax_amount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    buyer_compensation: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Content
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)
    virtual_tour_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Raw data — full Top Producer row preserved for reprocessing
    raw_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Import tracking
    source: Mapped[str] = mapped_column(String(20), nullable=False, default="crmls_tp")
    batch_id: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Metadata
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    parcel: Mapped["Parcel | None"] = relationship("Parcel", back_populates="listings")
    events: Mapped[list["ListingEvent"]] = relationship(
        "ListingEvent", back_populates="listing", order_by="ListingEvent.event_date.desc()"
    )

    @property
    def price_per_sqft(self) -> int | None:
        price = self.close_price or self.list_price
        sqft = self.parcel.sqft if self.parcel else None
        if price and sqft and sqft > 0:
            return round(price / sqft)
        return None

    @property
    def is_angelique(self) -> bool:
        name = "angelique lyle"
        la = (self.listing_agent_name or "").lower()
        ba = (self.buyer_agent_name or "").lower()
        return name in la or name in ba

    def __repr__(self):
        return f"<Listing {self.mls_number} ({self.status})>"


class ListingEvent(db.Model):
    """Status changes and price changes over time (from Agent Hot Sheet data)."""

    __tablename__ = "listing_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    mls_number: Mapped[str] = mapped_column(
        String(20), ForeignKey("listings.mls_number"), nullable=False, index=True
    )
    event_type: Mapped[str] = mapped_column(String(30), nullable=False)
    event_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    old_value: Mapped[str | None] = mapped_column(String(100), nullable=True)
    new_value: Mapped[str | None] = mapped_column(String(100), nullable=True)
    source: Mapped[str] = mapped_column(String(20), nullable=False, default="hot_sheet")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    listing: Mapped["Listing"] = relationship("Listing", back_populates="events")

    def __repr__(self):
        return f"<ListingEvent {self.mls_number} {self.event_type} @ {self.event_date}>"
```

- [ ] **Step 3: Update import_crmls.py — upsert parcels first, then listings**

Modify `scripts/import_crmls.py`. The `import_batch` function needs to:
1. For each row, upsert a `parcels` row with property data
2. Then upsert a `listings` row with only transaction data

Replace the `data = dict(...)` block (lines 140-178) and surrounding logic:

```python
from cove.models.parcel import Parcel
from cove.parcels.apn import normalize_apn

# In import_batch, replace the data dict:

                apn = normalize_apn(row.get("Parcel Number", ""))

                # 1. Upsert parcel (property data)
                if apn:
                    existing_parcel = db.session.get(Parcel, apn)
                    parcel_data = dict(
                        address=build_address(row),
                        street=build_address(row),
                        city=(row.get("City") or "").strip() or None,
                        zip_code=(row.get("Zip Code") or "").strip() or None,
                        property_type=(row.get("Property Sub Type") or "").strip() or None,
                        bedrooms=parse_int(row.get("Bedrooms Total")),
                        bathrooms=parse_float(row.get("Bathrooms Total Integer")),
                        sqft=parse_int(row.get("Living Area")),
                        lot_size_sqft=parse_int(row.get("Lot Size Square Feet")),
                        year_built=parse_int(row.get("Year Built")),
                        architectural_style=(row.get("Architectural Style") or "").strip() or None,
                        center_lat=parse_float(row.get("Latitude")),
                        center_lon=parse_float(row.get("Longitude")),
                        mls_area=(row.get("MLS Area") or "").strip() or None,
                        subdivision=(row.get("Tax Tract Number") or "").strip() or None,
                    )
                    if existing_parcel:
                        for key, value in parcel_data.items():
                            if value is not None:
                                setattr(existing_parcel, key, value)
                        if not existing_parcel.enrichment_source:
                            existing_parcel.enrichment_source = "crmls"
                        elif "crmls" not in existing_parcel.enrichment_source:
                            existing_parcel.enrichment_source += ",crmls"
                        existing_parcel.updated_at = datetime.utcnow()
                    else:
                        new_parcel = Parcel(apn=apn, **parcel_data)
                        new_parcel.enrichment_source = "crmls"
                        db.session.add(new_parcel)
                        db.session.flush()

                # 2. Upsert listing (transaction data only)
                data = dict(
                    mls_number=mls,
                    apn=apn,
                    status=(row.get("Standard Status") or "Unknown").strip(),
                    list_price=parse_int(row.get("List Price")),
                    close_price=parse_int(row.get("Close Price")),
                    list_date=parse_date_only(row.get("Listing Contract Date")),
                    close_date=parse_date_only(row.get("Close Date")),
                    dom=parse_int(row.get("Days Active in MLS")),
                    cdom=parse_int(row.get("Cumulative Days Active In MLS")),
                    listing_agent_name=build_agent_name("List Agent First Name", "List Agent Last Name", row),
                    listing_agent_email=(row.get("List Agent Email") or "").strip() or None,
                    listing_office=(row.get("List Office Name") or "").strip() or None,
                    buyer_agent_name=build_agent_name("Buyer Agent First Name", "Buyer Agent Last Name", row),
                    buyer_agent_email=None,
                    buyer_office=(row.get("Buyer Office Name") or "").strip() or None,
                    hoa_fee=parse_int(row.get("Association Fee")),
                    tax_amount=None,
                    buyer_compensation=(row.get("Buyer Agency Compensation") or "").strip() or None,
                    remarks=(row.get("Public Remarks") or "").strip() or None,
                    virtual_tour_url=(row.get("Virtual Tour URL Unbranded") or "").strip() or None,
                    raw_data={k: v for k, v in row.items() if v and v.strip()},
                    source="crmls_tp",
                    batch_id=batch_id,
                )
```

- [ ] **Step 4: Update tests**

Modify `tests/test_angel_import.py`:

1. All `Listing()` constructors that pass `address=`, `city=`, `sqft=`, etc. must be updated to create a `Parcel` first, then create the `Listing` with just `apn` pointing to it.

2. Update `test_listing_fields_parsed` — assertions for property fields should check via `listing.parcel.bedrooms` etc.

3. Update `test_price_per_sqft` — create a Parcel with sqft, then Listing with close_price.

4. Update `test_repr` — no longer checks for address in repr.

5. Remove `TestNormalizeApn` class (moved to `tests/test_apn.py`).

- [ ] **Step 5: Run tests to verify they fail (migration B not yet applied)**

Run: `docker exec cove_flask python3 -m pytest tests/test_parcel_listing_join.py -v`
Expected: FAIL — old columns still exist in DB, FK not yet added

- [ ] **Step 6: Commit model + script + test changes (pre-migration B)**

```bash
git add cove/models/listing.py scripts/import_crmls.py tests/test_angel_import.py tests/test_parcel_listing_join.py
git commit -m "feat: clean Listing model — remove property columns, add parcel FK + relationship"
```

---

### Task 5: Migration B — Destructive changes

**Files:**
- Create: `migrations/versions/xxxx_unified_parcels_b_destructive.py`

- [ ] **Step 1: Generate migration**

Run: `docker exec cove_flask python3 -m alembic revision --autogenerate -m "unified parcels B — drop listing property cols, drop research_parcels"`

- [ ] **Step 2: Review and edit migration**

Verify it includes:
1. NULL out malformed APNs on listings (prevents FK violation)
2. Add FK constraint: `listings.apn` → `parcels.apn`
3. Drop columns from `listings`
4. Drop `research_parcels` table (if exists)
5. Drop indexes on dropped columns (e.g., `ix_listings_mls_area`)

**Note:** Migration B is non-reversible. The downgrade should raise `NotImplementedError` — column data cannot be restored after drop.

```python
def upgrade():
    conn = op.get_bind()

    # 1. NULL out any listing APNs that don't exist in parcels (malformed or failed normalization)
    conn.execute(sa.text("""
        UPDATE listings SET apn = NULL
        WHERE apn IS NOT NULL
          AND apn NOT IN (SELECT apn FROM parcels)
    """))

    # 2. Add FK constraint
    op.create_foreign_key(
        'fk_listings_apn_parcels', 'listings', 'parcels', ['apn'], ['apn']
    )

    # 3. Drop redundant columns from listings
    for col in ['address', 'city', 'zip_code', 'property_type', 'bedrooms',
                'bathrooms', 'sqft', 'lot_sqft', 'year_built',
                'architectural_style', 'latitude', 'longitude',
                'mls_area', 'subdivision']:
        op.drop_column('listings', col)

    # 4. Drop research_parcels if it exists
    from sqlalchemy import inspect as sa_inspect
    inspector = sa_inspect(conn)
    if inspector.has_table('research_parcels'):
        op.drop_table('research_parcels')

def downgrade():
    raise NotImplementedError(
        "Migration B is destructive — column data cannot be restored. "
        "Restore from backup if rollback is needed."
    )
```

- [ ] **Step 3: Run migration**

Run: `docker exec cove_flask python3 -m alembic upgrade head`
Expected: Migration completes

- [ ] **Step 4: Run full test suite**

Run: `docker exec cove_flask python3 -m pytest tests/test_apn.py tests/test_parcel_unified.py tests/test_parcel_listing_join.py tests/test_angel_import.py -v`
Expected: ALL PASSED

- [ ] **Step 5: Commit**

```bash
git add migrations/versions/
git commit -m "feat: migration B — drop listing property columns, drop research_parcels, add listings.apn FK"
```

---

## Chunk 3: ATTOM enrichment rewrite + cleanup

### Task 6: Rewrite enrich_attom.py to target Parcel

**Files:**
- Modify: `scripts/enrich_attom.py`
- Create: `tests/test_attom_enrichment.py`

- [ ] **Step 1: Write test for ATTOM enrichment**

```python
"""Tests for ATTOM enrichment writing to unified Parcel model."""
from datetime import datetime
from unittest.mock import patch, MagicMock
import pytest
from cove.models.parcel import Parcel


class TestAttomEnrichment:
    def test_enrich_writes_to_parcel(self, db_session):
        """Enrichment should write to Parcel, not ResearchParcel."""
        parcel = Parcel(
            apn="7573-006-008", address="100 Sea Cove Dr", street="Sea Cove",
        )
        db_session.add(parcel)
        db_session.flush()

        # Simulate ATTOM enrichment
        parcel.enrichment = {
            "detail": {"property": [{"summary": {"yearbuilt": 1965}}]},
            "assessment": {"property": [{"assessment": {"market": {"mktTtlValue": 2500000}}}]},
        }
        parcel.enrichment_source = "county_gis,attom"
        parcel.enriched_at = datetime.utcnow()
        parcel.market_value = 2500000
        db_session.flush()

        fetched = db_session.get(Parcel, "7573-006-008")
        assert fetched.enrichment["detail"]["property"][0]["summary"]["yearbuilt"] == 1965
        assert fetched.market_value == 2500000
        assert "attom" in fetched.enrichment_source

    def test_enrichment_source_appends(self, db_session):
        parcel = Parcel(
            apn="7573-006-009", address="101 Sea Cove Dr", street="Sea Cove",
            enrichment_source="county_gis",
        )
        db_session.add(parcel)
        db_session.flush()

        # Append ATTOM
        parcel.enrichment_source = parcel.enrichment_source + ",attom"
        db_session.flush()

        assert parcel.enrichment_source == "county_gis,attom"
```

- [ ] **Step 2: Rewrite enrich_attom.py**

Replace entire file. Key changes:
- Import `Parcel` instead of `ResearchParcel`
- Write extracted fields to Parcel columns (`year_built`, `market_value`, etc.)
- Store full ATTOM response in `enrichment` JSONB
- Update `enrichment_source` and `enriched_at`
- Prioritize by `enriched_at IS NULL` then oldest enrichment

```python
"""Enrich parcels with ATTOM property data.

Queries the ATTOM API for each APN in the parcels table and stores
both extracted fields and the full response in enrichment JSONB.
Respects rate limits (1,000/day free trial).

Usage:
    python scripts/enrich_attom.py              # run all (up to daily limit)
    python scripts/enrich_attom.py --limit 50   # run 50
    python scripts/enrich_attom.py --apn 7573-006-024  # single APN
"""
import json
import os
import sys
import time
import argparse
import urllib.request
import urllib.parse
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from cove import create_app
from cove.extensions import db
from cove.models.parcel import Parcel
from cove.parcels.apn import normalize_apn
from sqlalchemy import select

ATTOM_API_KEY = os.environ.get("ATTOM_API_KEY", "")
ATTOM_BASE = "https://api.gateway.attomdata.com"
FIPS = "06037"  # LA County

ENDPOINTS = [
    "/propertyapi/v1.0.0/property/detail",
    "/propertyapi/v1.0.0/property/detailwithschools",
    "/propertyapi/v1.0.0/sale/detail",
    "/propertyapi/v1.0.0/assessment/detail",
]


def attom_query(endpoint: str, apn: str) -> dict | None:
    """Query a single ATTOM endpoint by APN (stripped format)."""
    apn_stripped = apn.replace("-", "")
    params = urllib.parse.urlencode({"apn": apn_stripped, "fips": FIPS})
    url = f"{ATTOM_BASE}{endpoint}?{params}"

    req = urllib.request.Request(url)
    req.add_header("apikey", ATTOM_API_KEY)
    req.add_header("Accept", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            if data.get("status", {}).get("code") == 0:
                return data
            return None
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print(f"    Rate limited! Waiting 60s...")
            time.sleep(60)
            return attom_query(endpoint, apn)
        elif e.code == 403:
            print(f"    403 Forbidden — daily limit reached")
            return "LIMIT_REACHED"
        else:
            print(f"    HTTP {e.code} for {apn}")
            return None
    except Exception as e:
        print(f"    Error: {e}")
        return None


def enrich_parcel(parcel: Parcel) -> dict:
    """Pull all ATTOM data for a single parcel and update the row."""
    attom_data = {}
    calls = 0

    for endpoint in ENDPOINTS:
        name = endpoint.split("/")[-1]
        result = attom_query(endpoint, parcel.apn)

        if result == "LIMIT_REACHED":
            return {"status": "limit_reached", "calls": calls}

        if result:
            attom_data[name] = result

            if name == "detail" and result.get("property"):
                prop = result["property"][0]
                summary = prop.get("summary", {})
                addr = prop.get("address", {})
                loc = prop.get("location", {})

                parcel.use_description = parcel.use_description or summary.get("propertyType")
                parcel.year_built = parcel.year_built or summary.get("yearbuilt")
                parcel.sqft = parcel.sqft or summary.get("livingSize")
                lat = loc.get("latitude")
                lon = loc.get("longitude")
                if lat:
                    parcel.center_lat = parcel.center_lat or float(lat)
                if lon:
                    parcel.center_lon = parcel.center_lon or float(lon)

            if name in ("detail", "sale") and result.get("property"):
                prop = result["property"][0]
                sale = prop.get("sale", {})
                amt_data = sale.get("saleAmountData", {})
                if amt_data.get("saleAmt"):
                    parcel.last_sale_price = parcel.last_sale_price or int(amt_data["saleAmt"])

            if name == "assessment" and result.get("property"):
                prop = result["property"][0]
                market = prop.get("assessment", {}).get("market", {})
                if market.get("mktTtlValue"):
                    parcel.market_value = int(market["mktTtlValue"])
                if market.get("mktLandValue"):
                    parcel.assessed_land_value = parcel.assessed_land_value or int(market["mktLandValue"])
                if market.get("mktImprValue"):
                    parcel.assessed_improvement_value = parcel.assessed_improvement_value or int(market["mktImprValue"])

        calls += 1
        time.sleep(0.3)

    if attom_data:
        parcel.enrichment = {**(parcel.enrichment or {}), **attom_data}
        if parcel.enrichment_source and "attom" not in parcel.enrichment_source:
            parcel.enrichment_source += ",attom"
        elif not parcel.enrichment_source:
            parcel.enrichment_source = "attom"
        parcel.enriched_at = datetime.utcnow()
        parcel.updated_at = datetime.utcnow()

    return {"status": "ok", "calls": calls, "endpoints": list(attom_data.keys())}


def main():
    parser = argparse.ArgumentParser(description="Enrich parcels with ATTOM data")
    parser.add_argument("--limit", type=int, default=250)
    parser.add_argument("--apn", type=str)
    args = parser.parse_args()

    if not ATTOM_API_KEY:
        print("ERROR: ATTOM_API_KEY not set in environment")
        sys.exit(1)

    app = create_app("dev")
    with app.app_context():
        if args.apn:
            parcel = db.session.get(Parcel, normalize_apn(args.apn))
            if not parcel:
                print(f"APN {args.apn} not found")
                return
            print(f"Enriching {parcel.apn}...")
            result = enrich_parcel(parcel)
            db.session.commit()
            print(f"  Result: {result}")
            return

        query = (
            select(Parcel)
            .where(
                (Parcel.enriched_at.is_(None)) |
                (Parcel.enrichment_source.not_like("%attom%"))
            )
            .order_by(Parcel.enriched_at.asc().nullsfirst())
            .limit(args.limit)
        )
        parcels = db.session.scalars(query).all()

        print(f"Enriching {len(parcels)} parcels with ATTOM data...")
        print(f"API key: {ATTOM_API_KEY[:8]}...")
        print(f"Estimated API calls: {len(parcels) * len(ENDPOINTS)}")

        total_calls = 0
        enriched = 0
        for i, parcel in enumerate(parcels):
            print(f"[{i+1}/{len(parcels)}] {parcel.apn}")
            result = enrich_parcel(parcel)

            if result["status"] == "limit_reached":
                print(f"\nDaily limit reached after {enriched} parcels.")
                db.session.commit()
                return

            total_calls += result["calls"]
            enriched += 1

            if enriched % 25 == 0:
                db.session.commit()

        db.session.commit()
        print(f"\nDone! Enriched {enriched} parcels with {total_calls} API calls.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Run tests**

Run: `docker exec cove_flask python3 -m pytest tests/test_attom_enrichment.py -v`
Expected: ALL PASSED

- [ ] **Step 4: Commit**

```bash
git add scripts/enrich_attom.py tests/test_attom_enrichment.py
git commit -m "feat: rewrite enrich_attom.py to target unified Parcel model with JSONB enrichment"
```

---

### Task 7: Delete legacy files

**Files:**
- Delete: `cove/models/research_parcel.py` (if it exists)
- Delete: `scripts/seed_research_parcels.py`
- Delete: `scripts/archive_research_parcels.py`

- [ ] **Step 1: Check and delete files**

```bash
# Check if research_parcel model exists
ls -la cove/models/research_parcel.py 2>/dev/null
# Delete legacy scripts
rm -f cove/models/research_parcel.py
rm -f scripts/seed_research_parcels.py
rm -f scripts/archive_research_parcels.py
```

- [ ] **Step 2: Verify no remaining imports**

Run: `grep -r "research_parcel\|ResearchParcel" cove/ scripts/ tests/ --include="*.py"`
Expected: No matches (or only in migration history files, which is fine)

Also verify `cove/models/__init__.py` does not import `ResearchParcel` (it shouldn't — already confirmed absent). And verify `cove/map/services.py` has no `ResearchParcel` references.

- [ ] **Step 3: Run full test suite**

Run: `docker exec cove_flask python3 -m pytest tests/ -v --ignore=tests/test_tsp.py --ignore=tests/test_canary.py`
Expected: ALL PASSED

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "chore: delete research_parcels legacy — model, seed, archive scripts"
```

---

### Task 8: Final verification

- [ ] **Step 1: Verify parcel count**

```bash
docker exec cove_flask python3 -c "
from cove import create_app; from cove.extensions import db; from cove.models.parcel import Parcel
from cove.models.listing import Listing
app = create_app('dev')
with app.app_context():
    parcels = db.session.query(Parcel).count()
    listings = db.session.query(Listing).count()
    linked = db.session.query(Listing).filter(Listing.apn.isnot(None)).count()
    enriched = db.session.query(Parcel).filter(Parcel.enrichment_source.isnot(None)).count()
    with_beds = db.session.query(Parcel).filter(Parcel.bedrooms.isnot(None)).count()
    print(f'Parcels: {parcels}')
    print(f'Listings: {listings}')
    print(f'Listings with APN link: {linked}')
    print(f'Parcels with enrichment source: {enriched}')
    print(f'Parcels with bedrooms: {with_beds}')
"
```

Expected:
- Parcels > 6,900
- Listings = 2,301
- Enriched parcels > 0
- Parcels with bedrooms > 0 (from CRMLS data migration)

- [ ] **Step 2: Verify no research_parcels table**

```bash
docker exec cove_flask python3 -c "
from cove import create_app; from cove.extensions import db
app = create_app('dev')
with app.app_context():
    result = db.session.execute(db.text(\"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'research_parcels')\"))
    print(f'research_parcels exists: {result.scalar()}')
"
```

Expected: `research_parcels exists: False`

- [ ] **Step 3: Run complete test suite**

Run: `docker exec cove_flask python3 -m pytest tests/ -v`
Expected: ALL PASSED

- [ ] **Step 4: Final commit if any cleanup needed**

```bash
git add -A
git commit -m "chore: unified parcels schema — final verification pass"
```

---

## Notes

### Deployment constraint
Migration B, the updated Listing model, updated `import_crmls.py`, and updated `enrich_attom.py` must ship together in a single deploy. Tasks 4-5 create a window where the codebase is inconsistent with the database schema — this is expected during development but must not be deployed incrementally.

### Data quality: CRMLS-sourced parcels
Parcels created from CRMLS data in Migration A step 7 use `street = address` (the full address string) as a fallback since the `street` column is NOT NULL. These parcels are non-Cove (no `organization_id`), so the `lot_email` property won't generate meaningful emails for them. A future pass can parse street names from full addresses.

### ATTOM API key rotation
The current `enrich_attom.py` has a hardcoded API key fallback (`60fa8a874c7c7f37cca7a32dc658e5bb`). The rewritten version removes this. The old key should be rotated since it was committed to source history.

### `zip_code` server_default
The current model uses Python-side `default="90275"`, not a server default. The migration's `server_default=None` call is a no-op in PostgreSQL but harmless. If Alembic warns about it, the line can be removed.
