# Parcel & Map Engine

> **Status:** Complete — written from code
> **Namespace:** cove
> **Last updated:** 2026-03-30
> **Code location:** `Cove/cove/parcels/`, `Cove/cove/map/`, `Cove/cove/models/parcel*.py`, `Cove/cove/models/research_parcel.py`, `Cove/cove/services/boundary_services.py`, `Cove/cove/services/tag_services.py`

---

## 1. Overview

The Parcel & Map Engine is the geographic and property-identity layer of Cove. Every governance action — a vote, an assessment, an ARC application, a ballot envelope — traces back through a Member to a Parcel identified by its county Assessor's Parcel Number (APN). The engine answers three questions:

1. **What parcels exist?** A list of community lots, their county-sourced property data, and their members.
2. **What is happening at each parcel?** Tags, contacts, comments, board-visible member status, and Lot H research classification.
3. **Where are they, and what surrounds them?** An interactive map with enriched GeoJSON, configurable overlay layers, Lot H research coverage, and board-parseable legal boundary descriptions.

### Scope

The engine covers:
- APN-keyed parcel data and community membership status
- Optional household profile data (ParcelProfile) with member-controlled sharing
- Board-managed annotation tags (ParcelTag / ParcelTagAssignment)
- Parcel contacts (ParcelContact) and internal board comments (ParcelComment)
- Research parcels (ResearchParcel) covering the broader Portuguese Bend peninsula for Lot H restriction research
- A full-screen interactive map built on Leaflet.js with per-role GeoJSON enrichment
- Configurable GeoJSON overlay layers with metes-and-bounds legal description parsing
- Boundary computation from recorded documents using Claude API

### First deployment context

WPBCA (West Portuguese Bend Community Association, Rancho Palos Verdes, CA) operates 81 lots across 5 streets. The ResearchParcel table additionally covers 5,500+ APNs on the Portuguese Bend peninsula for the Lot H Declaration of Protective Restrictions research project (Book 32160, Page 26, recorded 1950).

---

## 2. Architecture

### Component Diagram

```
Browser (Leaflet.js)
    |
    |-- GET /map/                        → map/routes.py → map/index.html
    |-- GET /map/api/geojson             → map/routes.py → map/services.get_enriched_geojson()
    |-- GET /map/api/lot-h               → map/routes.py → map/services.get_lot_h_geojson()
    |-- GET /map/api/neighborhood        → map/routes.py → static file send
    |-- GET /map/api/layers/<file>       → map/routes.py → static file send (path-traversal guarded)
    |-- GET /map/api/layers              → map/routes.py → layer_services.get_full_manifest()
    |-- POST /map/api/boundaries/parse   → map/routes.py → boundary_services.extract_and_compute()
    |-- GET /map/api/research/stats      → map/routes.py → map/services.get_research_stats()
    |-- GET /map/api/research/chart-data → map/routes.py → map/services.get_research_chart_data()
    |-- GET /map/api/research/<apn>      → map/routes.py → map/services.get_research_parcel()
    |
    |-- GET /parcels/                    → parcels/routes.py → parcel list
    |-- GET /parcels/<apn>               → parcels/routes.py → parcel detail
    |-- POST /parcels/tags/create        → parcels/routes.py → tag_services.create_tag()
    |-- POST /parcels/tags/<id>/assign   → parcels/routes.py → tag_services.bulk_assign_tag()
    |-- POST /parcels/tags/<id>/remove   → parcels/routes.py → tag_services.remove_tag_assignment()
    |-- GET /parcels/map                 → 301 redirect → /map/

Service Layer
    map/services.py              ← GeoJSON enrichment, layer manifest, research data
    parcels/services.py          ← Profile/tag property helpers; re-exports from map/services
    services/tag_services.py     ← Tag CRUD (consolidated from board + parcels)
    services/boundary_services.py← Metes-and-bounds parsing, polygon computation, GeoJSON output
    map/layer_services.py        ← Layer manifest CRUD (file-backed JSON)

Data Layer
    PostgreSQL 17 (growdirect_postgres, cove database)
      parcels              ← APN-keyed community lots
      parcel_profiles      ← Household sharing preferences
      parcel_tags          ← Board-defined annotation tags
      parcel_tag_assignments ← Many-to-many: parcels ↔ tags
      parcel_contacts      ← People associated with a parcel address
      parcel_comments      ← Board-internal notes on a parcel
      research_parcels     ← Peninsula-wide Lot H research table

Static Data (mounted volume, Cove/cove/map/data/)
      wpbca-parcels.geojson        ← Community parcel boundaries (from LA County GIS)
      lot-h-parcels.geojson        ← Research parcel boundaries
      neighborhood-parcels.geojson ← Surrounding context parcels (lightweight)
      layers/manifest.json         ← Overlay layer registry
      layers/<slug>.geojson        ← Named overlay layers (easements, zones, etc.)
```

### Request / Data Flow

**Map page load (member view):**
1. Browser requests `GET /map/` → `map/routes.py:index()` loads layer manifest from `map/services.get_map_layers()`, renders `map/index.html` with URL parameters for the three GeoJSON endpoints.
2. Leaflet initializes in the browser. JavaScript fires `GET /map/api/geojson`.
3. `map/routes.py:geojson()` calls `map/services.get_enriched_geojson(org_id, is_board=False)`.
4. Service loads `wpbca-parcels.geojson` from disk (pre-built county GIS export).
5. Service queries all Parcels for the org with eager-loaded Profile and TagAssignments.
6. For each GeoJSON feature, the service merges DB data: address, lot email, profile props (respecting share toggles), and tag props.
7. Board-gated fields (`owner_name`, `assessed_value`, `assessment_status`, `membership_status`) are omitted for member-role callers.
8. Result is a GeoJSON FeatureCollection returned as JSON. Leaflet renders polygon boundaries and popups client-side.

**Board-only map view:** Same flow with `is_board=True`. Service adds owner name, total assessed value, and linked member's assessment/membership status to each feature's properties.

**Boundary parsing (board-only):**
1. Board member submits `POST /map/api/boundaries/parse` with a pasted legal description and Point of Beginning coordinates.
2. Route validates `BoundaryParseForm` (WTForms, CSRF enforced), calls `boundary_services.extract_and_compute(text, pob)`.
3. `extract_and_compute` sends the legal text to Claude API (`claude-sonnet-4-20250514`) via `extract_legal_description()`. The LLM returns structured JSON with bearing/distance calls.
4. Each bearing string is parsed with `parse_bearing_string()` and converted to an azimuth with `bearing_to_azimuth()`.
5. `compute_polygon()` chains traverse calls from the POB into a closed ring of `(lng, lat)` tuples.
6. `generate_boundary_geojson()` wraps the polygon in a FeatureCollection with full provenance metadata (source doc, recording reference, computation chain).
7. `save_boundary()` writes the file to `layers/` and upserts the entry in `layers/manifest.json`.
8. Route returns `{"status": "ok", "slug": ..., "filepath": ...}`.

**Tag assignment (board-only):**
1. Board member selects parcels on the list or detail page, submits `TagAssignForm` (hidden APN field, comma-separated).
2. Route parses APNs from the hidden field and calls `tag_services.bulk_assign_tag()` in a single transaction.
3. `ParcelTagAssignment` rows are created with a `UniqueConstraint("apn", "tag_id")` — duplicate assignments are blocked at the database level.

### Key Design Decisions

**APN as primary key.** The `parcels` table uses `apn: Mapped[str] = mapped_column(String(20), primary_key=True)` instead of a UUID. This is a deliberate exception to the GrowDirect platform UUID standard. Full rationale is in Section 11.

**Client-side rendering, no PostGIS.** Parcel geometry is stored as JSON in the `geometry` column and served as GeoJSON to Leaflet.js for client-side rendering. This avoids a PostGIS dependency and keeps queries simple. Spatial queries are not required for the current feature set. If proximity search or server-side spatial operations are needed in the future, a PostGIS migration path is available without changing the data shape.

**Static GeoJSON files for base layers.** The community parcel boundaries (`wpbca-parcels.geojson`), Lot H coverage (`lot-h-parcels.geojson`), and neighborhood context (`neighborhood-parcels.geojson`) are pre-built from the LA County Assessor GIS and served as static files. This avoids per-request database reads for geometry-heavy data that changes rarely. DB enrichment is merged on top in the service layer at request time.

**Service consolidation.** `tag_services` and `boundary_services` were consolidated from duplicated implementations in `cove/board/` and `cove/parcels/` during the tech debt audit of 2026-03-29 and now live in `cove/services/`. `parcels/services.py` re-exports from `map/services.py` for backward compatibility.

**Board-view gating in the service, not the route.** The `is_board` flag is passed into `get_enriched_geojson()`, which controls field inclusion. This keeps the gating logic in one place and ensures the JSON shape is deterministic regardless of how the endpoint is called.

---

## 3. Data Model

All models use SQLAlchemy 2.0 `Mapped[]` syntax. Primary keys on non-parcel models are `String(36)` UUIDs (historical pattern; new tables should use native `Mapped[uuid.UUID]`).

### Parcel

```python
class Parcel(db.Model):
    __tablename__ = "parcels"

    apn: Mapped[str] = mapped_column(String(20), primary_key=True)
    organization_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("organizations.id"), nullable=True)

    # Address
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    street: Mapped[str] = mapped_column(String(100), nullable=False)
    lot_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    city: Mapped[str] = mapped_column(String(100), default="Rancho Palos Verdes")
    state: Mapped[str] = mapped_column(String(2), default="CA")
    zip_code: Mapped[str] = mapped_column(String(10), default="90275")

    # County property data
    lot_size_sqft: Mapped[int | None] = mapped_column(Integer, nullable=True)
    year_built: Mapped[int | None] = mapped_column(Integer, nullable=True)
    owner_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    use_description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    zoning: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # County assessed values
    assessed_land_value: Mapped[int | None] = mapped_column(Integer, nullable=True)
    assessed_improvement_value: Mapped[int | None] = mapped_column(Integer, nullable=True)
    transfer_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_sale_price: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Geometry (JSON, client-side only — no PostGIS)
    geometry: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    center_lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    center_lon: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Legal references
    tract_number: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True)
    map_book: Mapped[str | None] = mapped_column(String(10), nullable=True)
    legal_description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Classification
    is_association_member: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    is_combined: Mapped[bool] = mapped_column(Boolean, default=False)
    combined_with_apn: Mapped[str | None] = mapped_column(String(20), ForeignKey("parcels.apn"), nullable=True)

    # Lot H research
    lot_h_status: Mapped[str] = mapped_column(String(30), nullable=False, default="unknown", index=True)
    lot_h_on_title: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    member: Mapped["Member | None"] = relationship("Member", back_populates="parcel", uselist=False)
    organization: Mapped["Organization | None"] = relationship("Organization", backref="parcels")
    profile: Mapped["ParcelProfile | None"] = relationship("ParcelProfile", back_populates="parcel", uselist=False)
    tag_assignments: Mapped[list["ParcelTagAssignment"]] = relationship("ParcelTagAssignment", back_populates="parcel")
    comments: Mapped[list["ParcelComment"]] = relationship("ParcelComment", back_populates="parcel", order_by="ParcelComment.created_at.desc()")
    contacts: Mapped[list["ParcelContact"]] = relationship("ParcelContact", back_populates="parcel", order_by="ParcelContact.display_order")
```

**Computed properties:**
- `total_assessed_value` → `(assessed_land_value or 0) + (assessed_improvement_value or 0)`
- `address_num` → regex extracts leading integer from `address`
- `lot_email` → `{address_num}{street_compact}@{org.domain}` (e.g., `25SeaCove@abalonecove.org`)
- `lot_h_status_label` → human-readable label for the `lot_h_status` enum string

**Combined lots:** `combined_with_apn` is a self-referential FK to `parcels.apn`. Combined lots share one vote per WPBCA Bylaws Section 5.2.

**`organization_id` nullable:** Parcels with `organization_id = NULL` are surrounding lots loaded from county data for map context. They are not association members and have no associated Member record.

---

### ParcelProfile

One optional profile per APN. Records household information that a member chooses to share with neighbors via the directory and map popups.

```python
class ParcelProfile(db.Model):
    __tablename__ = "parcel_profiles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    apn: Mapped[str] = mapped_column(String(20), ForeignKey("parcels.apn"), nullable=False, unique=True)

    display_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)

    # JSON: [{"name": "Max", "type": "dog", "breed": "Lab"}, ...]
    pets: Mapped[list | None] = mapped_column(JSON, nullable=True)

    # Sharing toggles — control what appears in directory and map popup
    share_bio: Mapped[bool] = mapped_column(Boolean, default=True)
    share_household: Mapped[bool] = mapped_column(Boolean, default=False)
    share_pets: Mapped[bool] = mapped_column(Boolean, default=True)
    share_avatar: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    parcel: Mapped["Parcel"] = relationship("Parcel", back_populates="profile")
```

Note: `household_members` was migrated to `parcel_contacts` table (migration `a1c2e3f4g5h6`). The JSON pets field remains on the profile.

---

### ParcelTag

Tags are board-created annotations that classify parcels and appear as colored overlays in map popups. They connect parcels to evidence — archive documents, external sources, legal references.

```python
class ParcelTag(db.Model):
    __tablename__ = "parcel_tags"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    color: Mapped[str] = mapped_column(String(7), nullable=False, default="#6B7280")
    category: Mapped[str] = mapped_column(String(50), nullable=False, default="custom")
    # category values: founding | governance | property | threat | custom
    source_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_by: Mapped[str] = mapped_column(String(36), ForeignKey("members.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
```

---

### ParcelTagAssignment

Junction table connecting tags to parcels. The `UniqueConstraint("apn", "tag_id")` prevents double-tagging at the database level. Assignment-level `source_url` overrides the tag's default URL (used when different parcels have different documentary evidence for the same tag type).

```python
class ParcelTagAssignment(db.Model):
    __tablename__ = "parcel_tag_assignments"
    __table_args__ = (UniqueConstraint("apn", "tag_id", name="uq_parcel_tag"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    apn: Mapped[str] = mapped_column(String(20), ForeignKey("parcels.apn"), nullable=False)
    tag_id: Mapped[str] = mapped_column(String(36), ForeignKey("parcel_tags.id"), nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_by: Mapped[str] = mapped_column(String(36), ForeignKey("members.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
```

---

### ParcelContact

Contacts replace the old `household_members` JSON blob on ParcelProfile. Each row is one person associated with a parcel address. A partial unique index on `(apn)` where `contact_type = 'primary'` enforces one primary contact per parcel at the database level.

```python
class ParcelContact(db.Model):
    __tablename__ = "parcel_contacts"
    __table_args__ = (
        db.Index("ix_parcel_contacts_primary_unique", "apn", unique=True,
                 postgresql_where=text("contact_type = 'primary'")),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    apn: Mapped[str] = mapped_column(String(20), ForeignKey("parcels.apn", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str | None] = mapped_column(String(254))
    phone: Mapped[str | None] = mapped_column(String(20))
    contact_type: Mapped[str] = mapped_column(String(20), default=ContactType.HOUSEHOLD.value)
    relationship: Mapped[str] = mapped_column(String(20), default=ContactRelationship.OTHER.value)
    is_minor: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str | None] = mapped_column(Text)
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

**ContactType enum values:** `primary`, `secondary`, `household`, `emergency`, `tenant`
**ContactRelationship enum values:** `owner`, `co_owner`, `spouse`, `child`, `parent`, `tenant`, `other`

Both enums are Python enums for code safety. Database columns are `String(20)` — no PostgreSQL ENUM types (avoids migration pain on enum changes).

**Validation rule:** A minor (`is_minor=True`) cannot be the primary contact (`contact_type='primary'`). Enforced by `validate_contact()` in the model module.

---

### ParcelComment

Board-internal notes on a parcel. Not visible to regular members. Scoped to org for multi-tenancy.

```python
class ParcelComment(db.Model):
    __tablename__ = "parcel_comments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    apn: Mapped[str] = mapped_column(String(20), ForeignKey("parcels.apn"), nullable=False, index=True)
    organization_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id"), nullable=False)
    author_id: Mapped[str] = mapped_column(String(36), ForeignKey("members.id"), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

---

### ResearchParcel

A separate table covering the entire Portuguese Bend peninsula (~5,500+ APNs) for the Lot H Declaration of Protective Restrictions research project. Does not belong to any organization. APN is the primary key (same reasoning as `parcels`).

```python
class ResearchParcel(db.Model):
    __tablename__ = "research_parcels"

    apn: Mapped[str] = mapped_column(String(20), primary_key=True)
    ain: Mapped[str | None] = mapped_column(String(20), nullable=True)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    owner_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    use_description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    assessor_map: Mapped[str | None] = mapped_column(String(20), nullable=True)
    map_book: Mapped[str | None] = mapped_column(String(10), nullable=True, index=True)
    legal_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    legal_desc_line1: Mapped[str | None] = mapped_column(Text, nullable=True)
    legal_desc_line2: Mapped[str | None] = mapped_column(Text, nullable=True)
    tract_number: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True)
    year_built: Mapped[int | None] = mapped_column(Integer, nullable=True)
    land_value: Mapped[int | None] = mapped_column(Integer, nullable=True)
    improvement_value: Mapped[int | None] = mapped_column(Integer, nullable=True)
    center_lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    center_lon: Mapped[float | None] = mapped_column(Float, nullable=True)
    geometry: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Lot H research status
    lot_h_status: Mapped[str] = mapped_column(String(30), nullable=False, default="unknown", index=True)
    # lot_h_direct | lot_h_probable | lot_h_confirmed | excepted | released | not_covered | unknown

    # Evidence chain
    title_searched: Mapped[bool] = mapped_column(default=False)
    title_search_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    title_search_result: Mapped[str | None] = mapped_column(Text, nullable=True)
    lot_h_on_title: Mapped[bool | None] = mapped_column(nullable=True)  # None = not yet searched
    release_recorded: Mapped[bool | None] = mapped_column(nullable=True)
    release_document: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Raw API responses (full data store)
    attom_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    zillow_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    crmls_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    title_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Enrichment
    last_sale_date: Mapped[str | None] = mapped_column(String(20), nullable=True)
    last_sale_price: Mapped[int | None] = mapped_column(Integer, nullable=True)
    owner_occupied: Mapped[bool | None] = mapped_column(nullable=True)
    zestimate: Mapped[int | None] = mapped_column(Integer, nullable=True)
    property_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    subdivision_name: Mapped[str | None] = mapped_column(String(100), nullable=True)

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    researcher: Mapped[str | None] = mapped_column(String(100), nullable=True)
    source: Mapped[str] = mapped_column(String(50), default="la_county_gis")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

**Computed properties:**
- `total_assessed_value` → `(land_value or 0) + (improvement_value or 0)`
- `status_label` → human-readable label for `lot_h_status`

**Lot H status values and meaning:**

| Value | Meaning |
|-------|---------|
| `lot_h_direct` | Legal description explicitly references "Lot H" or "Blk H" |
| `lot_h_probable` | In a tract likely subdivided from Lot H land |
| `lot_h_confirmed` | Title search confirmed Lot H restrictions on chain of title |
| `excepted` | In a pre-1950 tract explicitly excepted in the declaration |
| `released` | Restrictions were recorded as released |
| `not_covered` | Outside the Lot H boundary |
| `unknown` | Needs research |

---

## 4. Interfaces

### HTTP Routes — Map Blueprint (`/map`)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/map/` | `@login_required` | Full-screen interactive map page |
| GET | `/map/api/geojson` | `@login_required` | Enriched GeoJSON FeatureCollection (role-gated) |
| GET | `/map/api/lot-h` | `@login_required` | Lot H research parcel GeoJSON |
| GET | `/map/api/neighborhood` | `@login_required` | Neighborhood context GeoJSON (static file) |
| GET | `/map/api/layers/<filename>` | `@login_required` | Serve named overlay layer file |
| GET | `/map/api/layers` | `@login_required` | Layer manifest (JSON) |
| GET | `/map/api/categories` | `@login_required` | Layer categories |
| GET | `/map/api/presets` | `@login_required` | Saved layer presets |
| GET | `/map/api/research/stats` | `@login_required` | Research parcel status statistics |
| GET | `/map/api/research/chart-data` | `@login_required` | Research aggregates by status (count + assessed value) |
| GET | `/map/api/research/<apn>` | `@login_required` | Single research parcel by APN |
| POST | `/map/api/boundaries/parse` | `@login_required` + `@board_required` | Parse legal description → GeoJSON boundary |

**`/map/api/geojson` response shape (member view, per feature):**
```json
{
  "type": "Feature",
  "geometry": { "type": "Polygon", "coordinates": [[...]] },
  "properties": {
    "apn": "7573-009-012",
    "address": "25 Sea Cove Dr",
    "street": "Sea Cove Dr",
    "lot_number": 69,
    "lot_email": "25SeaCove@abalonecove.org",
    "is_community": true,
    "is_threat": false,
    "lot_h_status": "lot_h_direct",
    "lot_h_status_label": "Lot H — Direct Reference",
    "display_name": "The Smith Family",
    "avatar_url": "https://...",
    "bio": "We moved here in 2018...",
    "pets": ["Max", "Bella"],
    "tags": [
      {
        "name": "Easement Issue",
        "color": "#dc2626",
        "source_url": "https://...",
        "comment": "See deed Book 42615"
      }
    ]
  }
}
```

**Board-only additional fields in properties:**
```json
{
  "owner_name": "John Smith",
  "assessed_value": 1250000,
  "member_name": "John Smith",
  "assessment_status": "current",
  "membership_status": "active"
}
```

### HTTP Routes — Parcels Blueprint (`/parcels`)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/parcels/` | `@login_required` | Parcel list with search |
| GET | `/parcels/<apn>` | `@login_required` | Parcel detail page |
| POST | `/parcels/tags/create` | `@login_required` + `is_board` check | Create tag (board-only) |
| POST | `/parcels/tags/<tag_id>/assign` | `@login_required` + `is_board` check | Bulk-assign tag to parcels |
| POST | `/parcels/tags/<tag_id>/remove` | `@login_required` + `is_board` check | Bulk-remove tag from parcels |
| GET | `/parcels/map` | — | 301 redirect to `/map/` |

### Forms

**`ParcelSearchForm`** — GET filter, CSRF disabled:
- `q: StringField` — free text (address, APN, owner name), max 255 chars
- `status: SelectField` — Lot H status filter

**`TagCreateForm`** — POST, CSRF enforced:
- `name: StringField` — required, 2–255 chars
- `color: SelectField` — hex choices: Blue, Green, Red, Amber, Purple, Cyan, Gray
- `category: SelectField` — `founding | governance | property | threat | custom`
- `description: TextAreaField` — optional, max 1000 chars
- `source_url: StringField` — optional, max 500 chars

**`TagAssignForm`** — POST, CSRF enforced:
- `apns: HiddenField` — comma-separated APN list, required
- `comment: TextAreaField` — optional, max 500 chars

**`TagRemoveForm`** — POST, CSRF enforced:
- `apns: HiddenField` — comma-separated APN list, required

**`BoundaryParseForm`** — POST, CSRF enforced:
- `legal_description: TextAreaField` — required, min 20 chars
- `pob_lat: StringField` — Point of Beginning latitude, required
- `pob_lng: StringField` — Point of Beginning longitude, required
- `name: StringField` — layer display name, 2–255 chars
- `slug: StringField` — kebab-case slug, validated `^[a-z0-9-]+$`
- `source_doc: StringField` — source document reference, required
- `recording_ref: StringField` — optional recording reference
- `color: SelectField` — map color
- `category: SelectField` — `community | legal | regulatory | easement | proposals | heritage | custom`

---

## 5. Service Layer

### `cove/map/services.py`

**`get_enriched_geojson(org_id: str, is_board: bool) → dict`**

The primary GeoJSON endpoint handler. Loads the static `wpbca-parcels.geojson` from disk, then queries all `Parcel` records for `org_id` with eager-loaded `profile` and `tag_assignments → tag` relationships. Merges DB data into GeoJSON feature properties. Board flag gates inclusion of owner name, assessed value, and member status fields. DB-only parcels (present in database but missing from the GeoJSON file) are appended as Point features at the parcel's `center_lat/center_lon` or a default coordinate.

**`get_lot_h_geojson() → dict`**

Reads and returns `lot-h-parcels.geojson` from disk. Returns an empty FeatureCollection if the file is absent.

**`get_research_parcel(apn: str) → dict | None`**

Looks up a single `ResearchParcel` by APN via `db.session.get()`. Returns a flat dict with all research fields serialized, or `None` if not found.

**`get_research_stats() → dict`**

Aggregates `ResearchParcel` counts grouped by `lot_h_status` and `map_book`. Returns `total_parcels`, `by_status`, and `by_map_book` dicts.

**`get_research_chart_data() → dict`**

Aggregates `ResearchParcel` by `lot_h_status` to produce both count and total assessed value per status. Used to render status distribution charts on the research dashboard.

**`get_map_layers() → list[dict]`**

Reads `layers/manifest.json` from disk. Marks layers with no `file` entry as `pending: True`. Returns the layers list.

---

### `cove/parcels/services.py`

**`get_profile_props(parcel: Parcel) → dict`**

Returns profile data shaped for GeoJSON feature properties, respecting sharing toggles. If no profile exists, returns owner name from county data and nulls for all optional fields. `bio` is truncated to 100 characters. `pets` is a list of pet names only (not full pet objects).

**`get_tag_props(parcel: Parcel) → list[dict]`**

Returns all tag assignments for a parcel as a list of dicts. Assignment-level `source_url` overrides the tag-level default when present.

**`get_parcel(apn: str) → Parcel | None`**

Thin wrapper around `db.session.get(Parcel, apn)`.

**Re-exports from `map/services.py`:** `get_enriched_geojson`, `get_lot_h_geojson`, `get_map_layers`, `get_research_chart_data`, `get_research_parcel`, `get_research_stats`

---

### `cove/services/tag_services.py`

**`create_tag(org_id, name, color, category, created_by, *, description, source_url) → ParcelTag`**

Creates and commits a new `ParcelTag` scoped to the organization.

**`assign_tag(apn, tag_id, created_by, *, comment, source_url) → ParcelTagAssignment`**

Creates a single `ParcelTagAssignment`. Will raise an integrity error if the `(apn, tag_id)` pair already exists (use `bulk_assign_tag` for user-facing operations that need graceful handling).

**`bulk_assign_tag(apns, tag_id, created_by, *, comment) → list[ParcelTagAssignment]`**

Assigns a tag to multiple parcels in a single transaction. Each assignment is added before a single `db.session.commit()`.

**`remove_tag_assignment(apn, tag_id) → None`**

Finds and deletes the `ParcelTagAssignment` for the given pair. No-op if not found.

**`get_tags_for_parcel(apn) → list[dict]`**

Returns all tags for a parcel as serialized dicts. Source URL resolution: assignment URL overrides tag default. Ordered by tag name.

**`list_tags(org_id) → list[ParcelTag]`**

Returns all tags for the organization ordered by name.

---

### `cove/services/boundary_services.py`

Metes-and-bounds legal description parser and polygon computer.

**`parse_bearing_string(text: str) → dict`**

Parses a surveyor bearing string in formats: `N 45 30 00 E`, `S 40d23m00s E`, `N45d30m00sE`. Normalizes degree/minute/second symbols and extracts prefix, degrees, minutes, seconds, suffix.

**`bearing_to_azimuth(prefix, degrees, minutes, seconds, suffix) → float`**

Converts a parsed bearing to a compass azimuth (0–360 degrees clockwise from north). Standard quadrant conversion: N/E → direct, S/E → 180-d, S/W → 180+d, N/W → 360-d.

**`traverse_call(start: tuple, azimuth: float, distance_ft: float) → tuple`**

Computes the end point of a single metes-and-bounds call. Uses earth constants calibrated to 33.74° latitude (Abalone Cove): `FT_PER_DEG_LAT = 364567.0`, `FT_PER_DEG_LNG = 303470.0`.

**`compute_polygon(pob: tuple, calls: list[dict]) → list[tuple]`**

Chains traverse calls from the POB into a closed polygon ring. Returns `[(lng, lat), ...]` in GeoJSON coordinate order. Automatically closes the ring.

**`extract_legal_description(text: str, api_key: str | None) → dict`**

Sends the legal description text to Claude API (`claude-sonnet-4-20250514`, max 2000 tokens) with a structured extraction prompt. Returns `{"pob_description": str, "calls": [{"bearing": str, "distance_ft": float}, ...], "notes": str}`. Handles markdown code block wrappers in the LLM response. Raises `ValueError` on parse failure.

**`extract_and_compute(text: str, pob: tuple, api_key: str | None) → tuple[list[tuple], dict]`**

Full pipeline: extract → convert bearings to azimuths → compute polygon. Returns `(polygon, extraction_result)`.

**`generate_boundary_geojson(...) → dict`**

Wraps a computed polygon in a GeoJSON FeatureCollection with full provenance: source document, recording reference, raw legal text, hex color, category, parse timestamp, and the computation chain for reproducibility.

**`save_boundary(slug, geojson, layers_dir, name, color, category, default_on) → str`**

Writes the GeoJSON file to `layers/<slug>.geojson` and upserts the layer entry in `layers/manifest.json`. Idempotent — existing entry with same `id` is replaced. Returns the absolute file path.

---

### `cove/map/layer_services.py`

File-backed manifest CRUD. All operations read/write `layers/manifest.json`.

**`get_full_manifest() → dict`** — Returns `{categories, layers, presets}`.
**`get_categories() → list`** — Returns categories list.
**`get_presets() → list`** — Returns presets list.
**`validate_slug(slug: str) → str`** — Enforces `^[a-z0-9-]+$` pattern.
**`validate_geojson_filename(filename: str) → str`** — Blocks path traversal (rejects `..`, `/`, `\`) and non-`.geojson` extensions.

---

## 6. Configuration

No Parcel & Map Engine-specific config keys. The engine uses standard Cove infrastructure:

| Setting | Source | Value |
|---------|--------|-------|
| `DATABASE_URL` | `.env` / compose env | `postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/cove` |
| `ANTHROPIC_API_KEY` | `.env` | Required for boundary parsing (Claude API call) |
| GeoJSON data directory | Hardcoded in `map/services.py` | `Cove/cove/map/data/` |
| Layer manifest | Hardcoded in `map/services.py` | `Cove/cove/map/data/layers/manifest.json` |
| Layers directory | Hardcoded in `map/routes.py` + `boundary_services.py` | `Cove/cove/map/data/layers/` |
| Basis of Bearings | Code comment + constant | S 40d 23m 00s E, Tract Map 14649, Map Book 345, Pages 23–26 |
| Earth constants | `boundary_services.py` | `FT_PER_DEG_LAT = 364567.0`, `FT_PER_DEG_LNG = 303470.0` at 33.74° N |

The GeoJSON data directory is volume-mounted in dev (`Cove/cove/` → `/app/cove/`). GeoJSON files created by boundary parsing are written into the container at `cove/map/data/layers/`, which persists to the host via the mount.

---

## 7. Security & Compliance

### Authentication

All parcel and map routes require `@login_required`. Unauthenticated requests redirect to `/auth/login?next=<original_url>`.

### Board-only operations

Three parcels routes enforce `current_user.is_board` and call `abort(403)` on failure:
- `POST /parcels/tags/create`
- `POST /parcels/tags/<id>/assign`
- `POST /parcels/tags/<id>/remove`

The boundary parse endpoint uses the `@board_required` decorator from `cove.auth.decorators`.

### Directory visibility and the `is_board` gate

**Member view** of the map returns: address, APN, lot email, profile data (respecting sharing toggles), and tags. It does not expose: owner name (county record), assessed value, linked member's assessment or membership status.

**Board view** additionally exposes: `owner_name`, `assessed_value`, `member_name`, `assessment_status`, `membership_status`. This gate is applied in `get_enriched_geojson(is_board=True/False)`. The flag is set from `current_user.is_board` at the route level and passed into the service — the service itself has no session access.

### Data isolation by organization

The parcel list query filters by `Parcel.organization_id == current_user.organization_id`. Tags are scoped by `organization_id` on `ParcelTag`. Comments are scoped by `organization_id` on `ParcelComment`. There is no cross-organization parcel access.

Parcels with `organization_id = NULL` (surrounding context lots) are excluded from the parcel list and detail views. They appear only in the map's static GeoJSON file.

### Path traversal protection

`GET /map/api/layers/<filename>` rejects requests where:
- `filename` does not end with `.geojson`
- `filename` contains `/` or `..`

`layer_services.validate_geojson_filename()` applies the same rules for programmatic use.

### Profile sharing consent

`ParcelProfile` share toggles (`share_bio`, `share_household`, `share_pets`, `share_avatar`) default to conservative settings (`share_household = False`). `get_profile_props()` in `parcels/services.py` enforces these toggles — fields are returned as `None` when the toggle is off, regardless of whether data exists.

### CSRF

All POST forms inherit from `CoveForm` (which extends Flask-WTForms `FlaskForm`). CSRF is enabled globally via `CSRFProtect(app)`. `ParcelSearchForm` explicitly disables CSRF (`class Meta: csrf = False`) because it is submitted via GET.

### ResearchParcel isolation

`ResearchParcel` data is not org-scoped and is accessible to any authenticated member via the research API endpoints. This is intentional — the Lot H research is community-facing and not sensitive.

---

## 8. Error Handling

| Scenario | Behavior |
|----------|----------|
| APN not found in `GET /parcels/<apn>` | `abort(404)` |
| Non-board member attempts tag create/assign/remove | `abort(403)` |
| Non-board member attempts boundary parse | `@board_required` → 403 |
| Invalid slug in `GET /map/api/layers/<filename>` | `abort(400)` |
| Layer file not found | `abort(404)` |
| Research parcel APN not found | `abort(404)` |
| `wpbca-parcels.geojson` missing from disk | Returns empty FeatureCollection `{"type": "FeatureCollection", "features": []}` — no exception |
| `lot-h-parcels.geojson` missing from disk | Returns empty FeatureCollection — no exception |
| `layers/manifest.json` missing | Returns empty layers list — no exception |
| Claude API failure in boundary parsing | `except Exception as e: return jsonify({"error": f"Boundary parse failed: {e}"}), 500` |
| LLM returns invalid JSON | `extract_legal_description()` raises `ValueError`, propagates to the 500 handler above |
| `pob_lat`/`pob_lng` not parseable as float | Returns `{"error": "Point of Beginning must be valid decimal coordinates."}`, 400 |
| Tag form validation failure | `flash("Tag creation failed. Check the form.", "error")` + redirect |
| Tag assignment with no APNs | `flash("No parcels selected.", "error")` + redirect |
| Duplicate tag assignment | `UniqueConstraint("apn", "tag_id")` raises database integrity error — not currently caught at the service layer; will surface as a 500 on the bulk assign route |

---

## 9. Testing

The Parcel & Map Engine tests live in the standard Cove pytest suite.

### Unit tests

- `test_parse_bearing_string`: Valid formats (spaced, compact, with symbols), invalid input raises `ValueError`.
- `test_bearing_to_azimuth`: All four quadrants (NE, SE, SW, NW), boundary cases (due north = 0, due south = 180).
- `test_traverse_call`: Known APN coordinate traversal against surveyed control point.
- `test_compute_polygon`: Ring closure, correct (lng, lat) GeoJSON ordering.
- `test_get_profile_props`: Share toggle enforcement — field suppressed when toggle is off, default to owner name when no profile.
- `test_get_tag_props`: Assignment-level source_url override, null tag handling.
- `validate_contact`: Minor cannot be primary contact.

### Integration tests

- `test_parcel_list_auth`: Unauthenticated request redirects to login.
- `test_parcel_list_org_scope`: Only parcels for the authenticated member's org are returned.
- `test_parcel_detail_not_found`: Returns 404 for unknown APN.
- `test_tag_create_board_only`: Member without board role receives 403.
- `test_tag_assign_bulk`: Creates correct number of assignments; duplicate blocked.
- `test_tag_remove_bulk`: Removes assignments; no-op on missing assignment.
- `test_geojson_member_view`: Board-gated fields absent for member-role caller.
- `test_geojson_board_view`: Board-gated fields present for board-role caller.
- `test_research_parcel_detail`: Known APN returns correct status label.
- `test_research_stats`: Returns correct counts by status.
- `test_boundary_parse_board_only`: Non-board member receives 403.
- `test_layer_file_path_traversal`: Rejects `../../../etc/passwd.geojson`.

### Smoke tests

- `GET /map/` returns 200 for authenticated member.
- `GET /map/api/geojson` returns valid GeoJSON FeatureCollection.
- `GET /parcels/` returns 200.

### Test fixtures

- `org`, `member` (member role), `board_member` (board role), `parcel` (bound to org), `parcel_profile` (with all toggles), `parcel_tag` + `assignment`.

---

## 10. Dependencies

### Upstream

| Dependency | Purpose |
|------------|---------|
| `parcels.organization_id → organizations.id` | All community parcels are scoped to an organization |
| `parcels.apn ← members.parcel_apn` | One-to-one: member linked to their parcel |
| `parcel_tags.created_by → members.id` | Tag authorship |
| `parcel_tag_assignments.created_by → members.id` | Assignment authorship |
| `parcel_comments.author_id → members.id` | Comment authorship |
| `parcel_comments.organization_id → organizations.id` | Comment scoping |
| `cove.auth.decorators.board_required` | Route-level board enforcement |
| `cove.forms.CoveForm` | Base form class (CSRF, Tailwind render hints) |

### Downstream

| Consumer | What it reads |
|----------|---------------|
| Governance (proposals, ballots) | `Parcel.apn → Member` — the governance chain starts at the parcel |
| Treasury (assessments) | `Parcel.apn → Assessment` — assessments are levied per APN |
| Member directory | `Parcel.profile` — display name, avatar, bio in the directory |
| Board dashboard | Tag assignments and parcel status summaries |

### Shared Infrastructure

| Service | Role |
|---------|------|
| `growdirect_postgres` (cove database) | All parcel tables |
| LA County Assessor GIS | Source for `wpbca-parcels.geojson`, parcel geometry, and ResearchParcel data |
| Claude API (`claude-sonnet-4-20250514`) | Legal description extraction for boundary parsing |
| Leaflet.js (npm) | Client-side map rendering — no CDN |
| Alpine.js (npm) | Map UI interactivity (layer toggles, modals) — no CDN |

---

## 11. Known Issues & Reconciliation

### APN as primary key — deliberate exception to platform UUID standard

**The standard:** GrowDirect platform requires UUID primary keys on every table.

**The exception:** `parcels.apn` (`String(20)`) and `research_parcels.apn` (`String(20)`) use the county Assessor's Parcel Number as the primary key.

**Why this is correct:**

The APN is the canonical, universal identifier for real property in Los Angeles County. It exists independently of Cove — in county tax rolls, title documents, recorded deeds, assessor GIS exports, and all third-party property data APIs (ATTOM, CRMLS, Zillow). Every piece of property data in the system is keyed to an APN. Introducing a UUID as the primary key would require either (a) a lookup translation at every import boundary, or (b) making the UUID the internal key and APN a unique secondary index, with a FK from every downstream table that currently FK's to `parcels.apn`.

The chain `Parcel (APN) → Member → Vote` is the foundation of HOA governance. If APN were not the PK, every ballot, assessment, and ARC application would require an additional join through a UUID-to-APN translation layer. The APN is stable across ownership transfers — when a lot sells, the APN stays, the member changes, and the lot email forwarding is updated. This is only practical because APN is the immutable identifier.

**Constraints this creates:**
- APN values must not be modified once created (treated as immutable — county reassignment is extremely rare and would require a data migration).
- Lookups by APN use `db.session.get(Parcel, apn)` directly — UUID-style lookup patterns apply unchanged with the APN as the key.
- New downstream tables should FK to `parcels.apn (String(20))` rather than a UUID column.

**ResearchParcel is the same decision** applied to the 5,500-parcel research dataset. The APN is the join key between the county GIS export, the Lot H status assignment, and any future title search integration.

### Parcel → Member → Vote chain

The governance identity chain is: a lot has an APN, an APN has a Parcel record, a Parcel has a Member, a Member casts a Ballot. Breaking or bypassing this chain is a governance integrity failure. Combined lots (two APNs mapped to one membership via `combined_with_apn`) share one vote per Bylaws Section 5.2. The `Member.voting_weight` field accommodates this when needed.

### GeoJSON file-backed layers vs. database-backed layers

Overlay layers (easements, zone boundaries, research boundaries) are stored as `.geojson` files in `cove/map/data/layers/` with a file-backed `manifest.json` registry. This is intentional for the current scale (a handful of named layers for one community). If the layer count grows significantly, or if layers need version history or access control, migrating the manifest to a database table is a defined next step. The `layer_services.py` API is designed to make this substitution localized.

### `String(36)` UUID pattern on non-parcel models

All non-parcel models in the Parcel & Map Engine use `String(36)` primary keys (UUID stored as string) rather than the platform-standard `Mapped[uuid.UUID]` with native UUID column type. This is a historical holdover from early Cove development. It works correctly but is not the platform standard. New tables should use native `Mapped[uuid.UUID]` with `default=uuid.uuid4`. Existing tables should not be changed without a measured migration.

### Duplicate tag assignment not gracefully handled

`tag_services.bulk_assign_tag()` does not catch the `IntegrityError` that will be raised by the `UniqueConstraint("apn", "tag_id")` on duplicate assignment. The route will return a 500 in this case. A future fix should catch `IntegrityError`, roll back the transaction, and flash an informative message. Tracked separately.
