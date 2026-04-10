# SDD: Parcels

**Status:** Active
**Last updated:** 2026-03-29

---

## Overview

Parcel list, detail pages, and tagging system. The interactive Leaflet.js map and GeoJSON API have been moved to the `map` blueprint (`cove/map/`). Tag services are shared via `cove/services/tag_services.py`. Parcels routes are thin HTTP wrappers over the services layer.

---

## Blueprint

- **Variable:** `parcels_bp`
- **Prefix:** `/parcels`
- **Module:** `cove/parcels/routes.py`
- **Registration:** `cove/__init__.py` line 65 — `app.register_blueprint(parcels_bp, url_prefix="/parcels")`
- **Template folder:** `cove/parcels/templates` (blueprint-local via `template_folder="templates"` in Blueprint constructor)

---

## Routes

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/parcels/` | `@login_required` | Parcel list with tag filtering and search |
| POST | `/parcels/tags/create` | `@login_required` + `is_board` | Create a new tag definition scoped to the org |
| POST | `/parcels/tags/<tag_id>/assign` | `@login_required` + `is_board` | Bulk-assign a tag to comma-separated APNs |
| POST | `/parcels/tags/<tag_id>/remove` | `@login_required` + `is_board` | Bulk-remove a tag from comma-separated APNs |
| GET | `/parcels/map` | `@login_required` | Redirects to `/map` (301) |
| GET | `/parcels/<apn>` | `@login_required` | Parcel detail page. Looks up parcel by APN, scoped to current user's org. Joins matching `ResearchParcel` by APN if present. 404 if not found or org mismatch. |

**Routes moved to map module** (see `cove/map/routes.py`): GeoJSON API, Lot H research layer, research stats/chart-data, layer file serving, boundary parsing.

---

## Models

### `Parcel` — `parcels`

Source: `cove/models/parcel.py`

| Column | Type | Notes |
|--------|------|-------|
| `id` | `String(36)` PK | UUID default |
| `organization_id` | `String(36)` FK → `organizations.id` | Required |
| `apn` | `String(20)` unique | Assessor's Parcel Number (e.g. `7573-016-026`) |
| `address` | `String(255)` | Full situs address (e.g. `25 Sea Cove Dr`) |
| `street` | `String(100)` | Street name (e.g. `Sea Cove Drive`) |
| `lot_number` | `Integer` nullable | Legal lot number |
| `city` | `String(100)` | Default `Rancho Palos Verdes` |
| `state` | `String(2)` | Default `CA` |
| `zip_code` | `String(10)` | Default `90275` |
| `lot_size_sqft` | `Integer` nullable | |
| `assessed_land_value` | `Integer` nullable | |
| `assessed_improvement_value` | `Integer` nullable | |
| `year_built` | `Integer` nullable | |
| `owner_name` | `String(255)` nullable | |
| `transfer_date` | `DateTime` nullable | |
| `geometry` | `JSON` nullable | GeoJSON Polygon |
| `is_association_member` | `Boolean` | Default `True`. False for Peppertree, 1 Sea Cove, etc. |
| `is_combined` | `Boolean` | Default `False`. Combined building site = no separate vote |
| `combined_with_id` | `String(36)` FK → `parcels.id` nullable | Self-referential FK for combined lots |
| `notes` | `Text` nullable | |
| `created_at` | `DateTime` | |
| `updated_at` | `DateTime` | |

**Properties:**

| Property | Returns | Logic |
|----------|---------|-------|
| `total_assessed_value` | `int` | `assessed_land_value + assessed_improvement_value` (nulls treated as 0) |
| `address_num` | `str \| None` | Regex extracts leading digits from address |
| `lot_email` | `str` | `{address_num}{StreetCompact}@{org.domain}` — email belongs to the property, not the person |
| `research_data` | `ResearchParcel \| None` | Lazy lookup via `db.session.get(ResearchParcel, self.apn)` |

**Relationships:**

| Name | Target | Cardinality |
|------|--------|-------------|
| `member` | `Member` | 1:1 (`back_populates="parcel"`) |
| `organization` | `Organization` | M:1 (`backref="parcels"`) |
| `profile` | `ParcelProfile` | 1:1 (`back_populates="parcel"`) |
| `tag_assignments` | `ParcelTagAssignment` | 1:M (`back_populates="parcel"`) |

---

### `ParcelProfile` — `parcel_profiles`

Source: `cove/models/parcel_profile.py`

Optional household enrichment per parcel. One profile per APN. All fields optional. Share toggles control what appears in directory and map popups.

| Column | Type | Notes |
|--------|------|-------|
| `id` | `String(36)` PK | UUID default |
| `parcel_id` | `String(36)` FK → `parcels.id` unique | One profile per parcel |
| `display_name` | `String(255)` nullable | How the owner appears publicly |
| `avatar_url` | `String(500)` nullable | |
| `bio` | `Text` nullable | |
| `household_members` | `JSON` nullable | Array of `{"name", "relation"}` dicts |
| `pets` | `JSON` nullable | Array of `{"name", "type", "breed"}` dicts |
| `share_bio` | `Boolean` | Default `True` |
| `share_household` | `Boolean` | Default `False` |
| `share_pets` | `Boolean` | Default `True` |
| `share_avatar` | `Boolean` | Default `True` |
| `updated_at` | `DateTime` | |

**Relationships:** `parcel` → `Parcel` (back_populates="profile")

---

### `ParcelTag` — `parcel_tags`

Source: `cove/models/parcel_tag.py`

Board-created tag definitions for annotating parcels. Tags are ad-hoc annotations: document cross-references, discoveries, flags.

| Column | Type | Notes |
|--------|------|-------|
| `id` | `String(36)` PK | UUID default |
| `organization_id` | `String(36)` FK → `organizations.id` | |
| `name` | `String(255)` | Tag display name |
| `description` | `Text` nullable | |
| `color` | `String(7)` | Hex color, default `#6B7280` |
| `category` | `String(50)` | `founding \| governance \| property \| threat \| custom` — default `custom` |
| `source_url` | `String(500)` nullable | Link to archive document |
| `created_by` | `String(36)` FK → `members.id` | |
| `created_at` | `DateTime` | |

**Relationships:**

| Name | Target | Cardinality |
|------|--------|-------------|
| `assignments` | `ParcelTagAssignment` | 1:M (cascade `all, delete-orphan`) |
| `creator` | `Member` | M:1 |

---

### `ParcelTagAssignment` — `parcel_tag_assignments`

Source: `cove/models/parcel_tag.py`

Join table connecting parcels to tags with per-assignment metadata.

| Column | Type | Notes |
|--------|------|-------|
| `id` | `String(36)` PK | UUID default |
| `parcel_id` | `String(36)` FK → `parcels.id` | |
| `tag_id` | `String(36)` FK → `parcel_tags.id` | |
| `comment` | `Text` nullable | Per-assignment note |
| `source_url` | `String(500)` nullable | Overrides `ParcelTag.source_url` if set |
| `created_by` | `String(36)` FK → `members.id` | |
| `created_at` | `DateTime` | |

**Constraints:** `UniqueConstraint("parcel_id", "tag_id", name="uq_parcel_tag")`

**Relationships:** `parcel` → `Parcel`, `tag` → `ParcelTag`, `creator` → `Member`

---

### `ResearchParcel` — `research_parcels`

Source: `cove/models/research_parcel.py`

Covers ~5,500 LA County parcels across the Portuguese Bend peninsula. Tracks each parcel's relationship to the 1950 Lot "H" Declaration of Protective Restrictions (Book 32160, Page 26). Separate from `Parcel` (which tracks only WPBCA community parcels). Linked to `Parcel` by APN lookup only — no foreign key.

**Primary key: `apn` (not UUID).** This is one of the few models that uses a natural key.

| Column | Type | Notes |
|--------|------|-------|
| `apn` | `String(20)` **PK** | Assessor's Parcel Number |
| `ain` | `String(20)` nullable | Assessor Identification Number |
| `address` | `String(255)` nullable | |
| `city` | `String(100)` nullable | |
| `owner_name` | `String(255)` nullable | |
| `use_description` | `String(255)` nullable | Property use class |
| `assessor_map` | `String(20)` nullable | |
| `map_book` | `String(10)` nullable, indexed | |
| `legal_description` | `Text` nullable | |
| `legal_desc_line1` | `Text` nullable | |
| `legal_desc_line2` | `Text` nullable | |
| `tract_number` | `String(20)` nullable, indexed | |
| `year_built` | `Integer` nullable | |
| `land_value` | `Integer` nullable | |
| `improvement_value` | `Integer` nullable | |
| `center_lat` | `Float` nullable | |
| `center_lon` | `Float` nullable | |
| `geometry` | `JSON` nullable | GeoJSON Polygon |
| `lot_h_status` | `String(30)` indexed, default `unknown` | See status values below |
| `title_searched` | `Boolean` | Default `False` |
| `title_search_date` | `DateTime` nullable | |
| `title_search_result` | `Text` nullable | |
| `lot_h_on_title` | `Boolean` nullable | `None` = not searched |
| `release_recorded` | `Boolean` nullable | |
| `release_document` | `String(255)` nullable | |
| `attom_data` | `JSON` nullable | Raw ATTOM API response |
| `zillow_data` | `JSON` nullable | Raw Zillow data |
| `crmls_data` | `JSON` nullable | Raw CRMLS data |
| `title_data` | `JSON` nullable | Raw title search data |
| `last_sale_date` | `String(20)` nullable | |
| `last_sale_price` | `Integer` nullable | |
| `owner_occupied` | `Boolean` nullable | |
| `zestimate` | `Integer` nullable | |
| `property_type` | `String(100)` nullable | |
| `subdivision_name` | `String(100)` nullable | |
| `notes` | `Text` nullable | |
| `researcher` | `String(100)` nullable | |
| `source` | `String(50)` | Default `la_county_gis` |
| `created_at` | `DateTime` | |
| `updated_at` | `DateTime` | |

**`lot_h_status` values:**

| Value | Meaning |
|-------|---------|
| `lot_h_direct` | Legal description explicitly references "Lot H" or "Blk H" |
| `lot_h_probable` | In a tract likely subdivided from Lot H land |
| `lot_h_confirmed` | Title search confirmed Lot H restrictions on chain of title |
| `excepted` | In a pre-1950 tract explicitly excepted in the declaration |
| `released` | Restrictions were recorded as released |
| `not_covered` | Outside the Lot H boundary |
| `unknown` | Needs research |

**Properties:**

| Property | Returns | Logic |
|----------|---------|-------|
| `total_assessed_value` | `int` | `land_value + improvement_value` (nulls as 0) |
| `status_label` | `str` | Human-readable label for `lot_h_status` |

---

## Services

Source: `cove/parcels/services.py`

All business logic is in the services layer. Routes delegate to these functions.

### `get_profile_props(parcel: Parcel) -> dict`

Extracts shareable profile data from a parcel for map popups. Returns `display_name`, `avatar_url`, `bio` (truncated to 100 chars if `share_bio` is True), and `pets` (list of pet names if `share_pets` is True). Returns owner_name fallback if no profile exists.

### `get_tag_props(parcel: Parcel) -> list[dict]`

Extracts tag data from a parcel's tag assignments. Returns a list of dicts with `name`, `color`, `source_url` (assignment-level override preferred over tag-level), and `comment`.

### `get_enriched_geojson(org_id: str, is_board: bool) -> dict`

Core GeoJSON enrichment pipeline. Returns a FeatureCollection with all parcel data merged:

1. Loads static `data/wpbca-parcels.geojson` from disk
2. Eager-loads all `Parcel` rows (scoped to `org_id`) with `profile` and `tag_assignments → tag` in one query
3. For each GeoJSON feature, merges: address, street, lot_number, lot_email, APN, community/threat flags, profile props (share toggles respected), tags, and `lot_h_status`
4. Board users (`is_board=True`) additionally receive: `owner_name`, `assessed_value`, `member_name`, `assessment_status`, `membership_status`
5. DB-only parcels not present in the GeoJSON file are appended with stored geometry or a default Point coordinate

### `get_map_layers() -> list[dict]`

Reads the layer manifest from `data/map-layers/manifest.json`. Returns a list of layer definitions (used by the map template to register overlay toggle controls).

### `get_lot_h_geojson() -> dict`

Loads and returns the Lot H research parcel GeoJSON from `data/lot-h-parcels.geojson`. Returns an empty FeatureCollection if the file does not exist.

### `get_research_parcel(apn: str) -> dict | None`

Looks up a single `ResearchParcel` by APN (primary key lookup). Returns a flat dict of all relevant fields or `None` if not found.

### `get_research_stats() -> dict`

Queries aggregate statistics for all research parcels:
- `total_parcels`: total count
- `by_status`: `{lot_h_status: count}` grouped by status
- `by_map_book`: `{map_book: count}` grouped by map book, ordered by map_book

### `get_research_chart_data() -> dict`

Returns chart-ready aggregates:
- `value_by_status`: `{lot_h_status: total_assessed_value}` — sum of `land_value + improvement_value` per status
- `count_by_status`: `{lot_h_status: count}`
- `total_assessed_value`: grand total across all statuses
- `total_parcels`: grand total count

### `get_parcel_with_research(parcel_id: str, org_id: str) -> tuple[Parcel | None, ResearchParcel | None]`

Looks up a `Parcel` by UUID, verifies org ownership. If found, also looks up the matching `ResearchParcel` by APN. Returns `(None, None)` on not found or org mismatch.

---

## Forms

Source: `cove/parcels/forms.py`

### `ParcelSearchForm`

Inherits from `CoveForm`. CSRF disabled (`class Meta: csrf = False`) because it is submitted via GET.

| Field | Type | Validators | Notes |
|-------|------|------------|-------|
| `q` | `StringField` | `Optional`, `Length(max=255)` | Placeholder: "Address, APN, or owner name" |
| `status` | `SelectField` | `Optional` | Choices: All statuses, Clear, Encumbered, Released, Under Review, Unknown |

---

## Templates

All templates are blueprint-local at `cove/parcels/templates/parcels/`.

| Template | Lines | Description |
|----------|-------|-------------|
| `map.html` | 228 | Leaflet.js interactive map. Alpine.js component (`parcelMap()`) manages init, layer toggling, and popup rendering. Includes search/filter bar (ParcelSearchForm), board view badge, layer overlay toggles from manifest, and links to research stats API. |
| `detail.html` | 187 | Full parcel detail page. Two-column grid: left card shows parcel details (address, lot number, street, owner, APN, lot email, assessed values, lot size, year built, association/combined status, notes). Right card shows Lot H research data if a matching ResearchParcel exists (status, tract, map book, legal description, title search evidence, sale history). Back-link to map. Board flag passed for conditional display. |

---

## GeoJSON / Map Integration

### Data Flow

```
Static GeoJSON files (disk)
  ├── data/wpbca-parcels.geojson     → base parcel boundaries (GIS export)
  ├── data/lot-h-parcels.geojson     → Lot H research overlay
  └── data/map-layers/*.geojson      → additional overlay layers
            ↓
services.get_enriched_geojson()      → merges with Parcel + Profile + Tag DB data
            ↓
/parcels/api/geojson                 → JSON response to browser
            ↓
Leaflet.js (map.html)               → renders polygons, popups, layer controls
```

### Leaflet.js Usage

- Map container: `#parcel-map` (600px height)
- Alpine.js component `parcelMap()` handles initialization and state
- GeoJSON loaded via `fetch()` to `/parcels/api/geojson` and `/parcels/api/lot-h`
- Overlay layers loaded from `/parcels/api/layers/<filename>` based on manifest
- Popups show: address, APN, lot email, profile data (display name, avatar, bio, pets), tags with colors
- Board users see additional financial and membership data in popups
- Layer toggle controls for each overlay in the manifest

### Role-Based Data Filtering

The GeoJSON endpoint returns different property sets based on `is_board`:

**All authenticated users see:**
- `apn`, `address`, `street`, `lot_number`, `lot_email`
- `is_community`, `is_threat`
- Profile data (respecting share toggles): `display_name`, `avatar_url`, `bio`, `pets`
- Tags: `name`, `color`, `source_url`, `comment`
- `lot_h_status`, `lot_h_status_label`

**Board members additionally see:**
- `owner_name`, `assessed_value`
- `member_name`, `assessment_status`, `membership_status`

---

## APN as Primary Key

The parcels module is the clearest expression of the APN-first pattern in Cove.

### How It Works

1. **`Parcel` model** uses `apn` as a unique indexed column (UUID is the technical PK for ORM consistency, but APN is the domain identifier)
2. **`ResearchParcel` model** uses `apn` directly as its primary key — no UUID. This is one of the few models with a natural key, reflecting the fact that the parcel IS the APN in county records
3. **Cross-model linking** between `Parcel` and `ResearchParcel` happens by APN lookup, not by foreign key. `Parcel.research_data` is a property that calls `db.session.get(ResearchParcel, self.apn)`. `get_parcel_with_research()` does the same in the service layer
4. **GeoJSON enrichment** keys the entire merge on APN: the static GeoJSON file has `properties.apn`, and DB parcels are indexed into a `{apn: parcel}` dict for O(1) lookup
5. **Lot email derivation** flows from the parcel's address, not from any member or user record. The email belongs to the property

### Why No FK Between Parcel and ResearchParcel

`Parcel` covers ~93 WPBCA community lots. `ResearchParcel` covers ~5,500 LA County parcels across the entire Portuguese Bend peninsula. Most research parcels have no corresponding `Parcel` row. A FK would either require 5,500 `Parcel` rows (wrong — they are not community parcels) or leave 5,400+ NULLs. APN lookup is the correct join strategy for this relationship.
