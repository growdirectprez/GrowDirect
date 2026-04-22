# Parcel Map Engine — Parcel Identity Layer

> **Status:** Production readiness review complete
> **Type:** App Service (Cove)
> **Namespace:** cove
> **Last updated:** 2026-04-13
> **Code location:** `Cove/cove/parcels/`, `Cove/cove/models/parcel*.py`, `Cove/cove/services/tag_services.py`
> **Split from:** Original `parcel-map-engine.md` (47K, 7500 words)
> **Companion SDD:** [[docs/sdds/cove/map-rendering|Map Rendering]] — Leaflet.js, GeoJSON overlays, boundary computation

**Wiki:** [[Brain/wiki/cove-governance|Cove Governance]] | [[Brain/wiki/cove-property-geology|Cove Property & Geology]]
**Architecture:** [[docs/sdds/cove/architecture|Cove Architecture]]
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[Canary/docs/profiles/ops/Tom|Tom]] · **Operator role:** [[Canary/docs/profiles/ops/Jeremy|Jeremy]]

---

## Purpose

The Parcel Identity Layer is the property-identity foundation of Cove. Every governance action — a vote, an assessment, an ARC application — traces back through a Member to a Parcel identified by its county Assessor's Parcel Number (APN). This service owns the data model, CRUD operations, tag system, and contact management for the 81 WPBCA community lots and the 5,500+ peninsula-wide research parcels.

The companion Map Rendering SDD covers Leaflet.js rendering, GeoJSON overlays, boundary parsing, and the land division hierarchy.

---

## Dependencies

| Dependency | Purpose |
|------------|---------|
| `growdirect_postgres` (cove database) | All parcel tables (parcels, parcel_profiles, parcel_tags, parcel_tag_assignments, parcel_contacts, parcel_comments) |
| `growdirect_valkey` (DB 1) | Session backend for Flask-Login |
| Cove auth module | `@login_required`, `current_user.is_board` for board-only routes |
| `cove.forms.CoveForm` | Base form class (CSRF, Tailwind render hints) |
| `cove.services.security.safe_redirect_back` | Open redirect protection on POST redirects |

### Downstream Consumers

| Consumer | What it reads |
|----------|---------------|
| Governance (proposals, ballots) | `Parcel.apn -> Member` — governance chain starts at the parcel |
| Treasury (assessments) | `Parcel.apn -> Assessment` — assessments are levied per APN |
| Member directory | `Parcel.profile` — display name, avatar, bio |
| Board dashboard | Tag assignments and parcel status summaries |
| Map Rendering SDD | `Parcel` model, `get_profile_props()`, `get_tag_props()` for GeoJSON enrichment |

---

## Data Flow & PII Map

### What Enters

| Source | Data | Format |
|--------|------|--------|
| LA County Assessor GIS | Parcel geometry, address, owner name, assessed values, tract/legal info | CSV/GIS import to DB |
| ATTOM API | Mortgage data, ownership classification, enrichment JSON | JSON via API, stored in `enrichment` JSONB |
| CRMLS | Property characteristics (beds, baths, sqft, style) | CSV import |
| Board members (UI) | Tags, tag assignments, comments, contacts | HTTP POST forms |
| Members (UI) | Profile data (display name, avatar, bio, pets) | HTTP POST forms |

### What Is Stored

| Table | PII Fields | Encryption Status | Classification |
|-------|-----------|-------------------|----------------|
| `parcels` | `owner_name` | **Plaintext** | internal |
| `parcels` | `address`, `city`, `zip_code` | Plaintext | public (property records) |
| `parcels` | `assessed_land_value`, `assessed_improvement_value`, `last_sale_price`, `market_value` | Plaintext | internal (board-gated in UI) |
| `parcels` | `mortgage_amount`, `mortgage_rate`, `mortgage_lender`, `mortgage_type` | **Plaintext** | sensitive |
| `parcels` | `equity_estimate` | **Plaintext** | sensitive |
| `parcels` | `enrichment` (JSONB blob from ATTOM) | **Plaintext** | sensitive (may contain owner details) |
| `parcel_contacts` | `name` | **Plaintext** | sensitive |
| `parcel_contacts` | `email` | **Plaintext** | sensitive |
| `parcel_contacts` | `phone` | **Plaintext** | sensitive |
| `parcel_contacts` | `relationship`, `contact_type` | Plaintext | internal |
| `parcel_contacts` | `is_minor` | Plaintext | sensitive (identifies children) |
| `parcel_contacts` | `notes` | **Plaintext** | internal |
| `parcel_profiles` | `display_name` | Plaintext | internal (member-controlled sharing) |
| `parcel_profiles` | `avatar_url` | Plaintext | internal |
| `parcel_profiles` | `bio` | Plaintext | internal |
| `parcel_profiles` | `pets` (JSON) | Plaintext | internal |
| `parcel_comments` | `body` | Plaintext | internal (board-only) |
| `parcel_comments` | `author_id` | Plaintext | internal |
| `parcel_tags` | — | No PII | public within org |
| `parcel_tag_assignments` | `created_by` | Plaintext | internal |

### What Exits

| Destination | Data | Gating |
|-------------|------|--------|
| Map GeoJSON API (member view) | address, APN, lot email, profile (share-toggled), tags | `@login_required`, share toggles enforced |
| Map GeoJSON API (board view) | Above + owner_name, assessed_value, member_name, assessment_status, membership_status | `is_board` flag in service |
| Parcel list/detail HTML | All parcel fields appropriate to role | `@login_required`, board check in template |
| Tag assignment flash messages | Tag name, parcel count | Board-only routes |

### PII Classification Key

- **public:** Freely visible (address, APN, lot number — all public property records)
- **internal:** Visible to authenticated org members (profile display name, tags, lot email)
- **sensitive:** Must be encrypted at rest, logged on access (contact name, email, phone, mortgage data, financial data, minor status)
- **restricted:** Encrypted, RLS-gated, audited (not applicable in this service — see Elections SDD for ballot data)

---

## API Contract

### HTTP Routes — Parcels Blueprint (`/parcels`)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/parcels/` | `@login_required` | Parcel list with search, tags, board management tools |
| GET | `/parcels/<apn>` | `@login_required` | Parcel detail page |
| POST | `/parcels/tags/create` | `@login_required` + `is_board` | Create tag (board-only) |
| POST | `/parcels/tags/<tag_id>/assign` | `@login_required` + `is_board` | Bulk-assign tag to parcels |
| POST | `/parcels/tags/<tag_id>/remove` | `@login_required` + `is_board` | Bulk-remove tag from parcels |
| GET | `/parcels/map` | — | 301 redirect to `/map/` |

### Forms

**`ParcelSearchForm`** — GET filter, CSRF disabled:
- `q: StringField` — free text (address, APN, owner name), max 255 chars
- `status: SelectField` — Lot H status filter

**`TagCreateForm`** — POST, CSRF enforced:
- `name: StringField` — required, 2-255 chars
- `color: SelectField` — hex choices: Blue, Green, Red, Amber, Purple, Cyan, Gray
- `category: SelectField` — founding | governance | property | threat | custom
- `description: TextAreaField` — optional, max 1000 chars
- `source_url: StringField` — optional, max 500 chars

**`TagAssignForm`** — POST, CSRF enforced:
- `apns: HiddenField` — comma-separated APN list, required
- `comment: TextAreaField` — optional, max 500 chars

**`TagRemoveForm`** — POST, CSRF enforced:
- `apns: HiddenField` — comma-separated APN list, required

### Service Layer

**`cove/parcels/services.py`**

| Function | Signature | Description |
|----------|-----------|-------------|
| `get_profile_props` | `(parcel: Parcel) -> dict` | Profile data shaped for GeoJSON, respecting share toggles. Bio truncated to 100 chars. |
| `get_tag_props` | `(parcel: Parcel) -> list[dict]` | Tag assignments as dicts. Assignment source_url overrides tag default. |
| `get_parcel` | `(apn: str) -> Parcel | None` | Thin wrapper around `db.session.get(Parcel, apn)`. |

**`cove/services/tag_services.py`**

| Function | Signature | Description |
|----------|-----------|-------------|
| `create_tag` | `(org_id, name, color, category, created_by, *, description, source_url) -> ParcelTag` | Create and commit a new tag scoped to org. |
| `assign_tag` | `(apn, tag_id, created_by, *, comment, source_url) -> ParcelTagAssignment` | Single assignment. Raises IntegrityError on duplicate. |
| `bulk_assign_tag` | `(apns, tag_id, created_by, *, comment) -> list[ParcelTagAssignment]` | Multi-parcel assignment in single transaction. |
| `remove_tag_assignment` | `(apn, tag_id) -> None` | Delete assignment. No-op if not found. |
| `get_tags_for_parcel` | `(apn) -> list[dict]` | Serialized tags for a parcel, ordered by name. |
| `list_tags` | `(org_id) -> list[ParcelTag]` | All tags for org, ordered by name. |

---

## Data Model

All models use SQLAlchemy 2.0 `Mapped[]` syntax. Primary keys on non-parcel models are `String(36)` UUIDs (historical pattern; new tables should use native `Mapped[uuid.UUID]`).

### Parcel

APN is the primary key — deliberate exception to the platform UUID standard. See "Known Issues" for full rationale.

```python
class Parcel(db.Model):
    __tablename__ = "parcels"
    apn: Mapped[str] = mapped_column(String(20), primary_key=True)
    organization_id: Mapped[str | None]  # NULL = surrounding context lots
    address, street, lot_number, city, state, zip_code  # Address
    lot_size_sqft, year_built, owner_name, use_description, zoning  # County data
    property_type, bedrooms, bathrooms, sqft, architectural_style  # CRMLS
    assessed_land_value, assessed_improvement_value, last_sale_date, last_sale_price, market_value
    geometry: Mapped[dict | None]  # JSON, client-side rendering only
    center_lat, center_lon, mls_area, subdivision
    tract_number, map_book, legal_description  # Legal refs
    enrichment: Mapped[dict | None]  # JSONB — raw ATTOM response
    mortgage_amount, mortgage_rate, mortgage_type, mortgage_lender  # ATTOM mortgage
    owner_occupied, absentee_owner, corporate_owner, ownership_years, equity_estimate
    is_association_member, is_combined, combined_with_apn  # Classification
    lot_h_status, lot_h_on_title  # Lot H research
    notes, created_at, updated_at
    # Relationships: member, organization, profile, tag_assignments, comments, contacts, listings
```

**Computed properties:** `total_assessed_value`, `address_num`, `lot_email`, `lot_h_status_label`

**Combined lots:** `combined_with_apn` is a self-referential FK. Combined lots share one vote per WPBCA Bylaws Section 5.2.

### ParcelProfile

One optional profile per APN. Member-controlled sharing for directory and map popups.

```python
class ParcelProfile(db.Model):
    __tablename__ = "parcel_profiles"
    id: Mapped[str]  # String(36) UUID
    apn: Mapped[str]  # FK -> parcels.apn, unique
    display_name, avatar_url, bio  # How the owner wants to appear
    pets: Mapped[list | None]  # JSON: [{"name": "Max", "type": "dog", "breed": "Lab"}]
    share_bio, share_household, share_pets, share_avatar  # Sharing toggles
    created_at, updated_at
```

### ParcelContact

People associated with a parcel address. Replaces old `household_members` JSON blob.

```python
class ParcelContact(db.Model):
    __tablename__ = "parcel_contacts"
    # Partial unique index: one primary contact per APN
    id: Mapped[str]  # String(36) UUID
    apn: Mapped[str]  # FK -> parcels.apn, CASCADE delete
    name: Mapped[str]  # String(200), NOT NULL
    email: Mapped[str | None]  # String(254)
    phone: Mapped[str | None]  # String(20)
    contact_type: Mapped[str]  # primary | secondary | household | emergency | tenant
    relationship: Mapped[str]  # owner | co_owner | spouse | child | parent | tenant | other
    is_minor: Mapped[bool]  # Minor cannot be primary contact
    notes: Mapped[str | None]
    display_order: Mapped[int]
    created_at, updated_at
```

**Validation:** `validate_contact()` enforces that a minor cannot be the primary contact.

### ParcelTag / ParcelTagAssignment

Board-created annotation tags with many-to-many junction table.

```python
class ParcelTag(db.Model):
    __tablename__ = "parcel_tags"
    id, organization_id, name, description, color, category, source_url, created_by, created_at

class ParcelTagAssignment(db.Model):
    __tablename__ = "parcel_tag_assignments"
    __table_args__ = (UniqueConstraint("apn", "tag_id", name="uq_parcel_tag"),)
    id, apn, tag_id, comment, source_url, created_by, created_at
```

### ParcelComment

Board-internal notes. Not visible to regular members.

```python
class ParcelComment(db.Model):
    __tablename__ = "parcel_comments"
    id, apn, organization_id, author_id, body, created_at, updated_at
```

---

## Operations

### Startup Sequence

1. Cove Flask app factory creates the app and registers the `parcels_bp` blueprint at `/parcels`.
2. All parcel models are imported via `cove/models/__init__.py` for Alembic detection.
3. No special initialization required — all parcel data is in PostgreSQL.

### Health Checks

The Cove `/health` endpoint covers database connectivity. No parcel-specific health check exists.

### Failure Modes

| Failure | Impact | Behavior |
|---------|--------|----------|
| PostgreSQL down | All parcel operations fail | Flask returns 500; upstream `/health` would fail |
| Missing Parcel for APN lookup | Detail page shows nothing | `abort(404)` |
| Duplicate tag assignment | Bulk assign partially fails | `IntegrityError` propagates as 500 (not gracefully caught) |
| Tag form validation failure | Flash error, redirect back | User sees error message |

### Monitoring

No parcel-specific monitoring is implemented. Required before production:
- Alert on 500 error rate on `/parcels/*` routes
- Alert on database connection failures
- Log parcel contact CRUD operations (PII access)

### Configuration

| Setting | Source | Value |
|---------|--------|-------|
| `DATABASE_URL` | `.env` / compose | `postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/cove` |
| `SESSION_TYPE` | config | `redis` (Valkey) |

No parcel-specific config keys. All infrastructure is standard Cove.

---

## Deployment

### Docker Service

Runs inside `cove_flask` container (Gunicorn on 5002:5000). No separate container.

### AWS Target

- **Compute:** ECS/Fargate (shared Cove task)
- **Database:** RDS PostgreSQL 17 (cove database)
- **Secrets:** AWS Secrets Manager for `DATABASE_URL`, encryption keys
- **Static files:** S3 + CloudFront (if parcel images are added)

### CI/CD

- Standard Cove pipeline: pytest -> Docker build -> ECS deploy
- Database migrations via Alembic (run before deploy)

---

## Code Review Findings

### P0 — Blocks Production

**P0-PME-01: Parcel contact PII stored plaintext**

ParcelContact stores `name`, `email`, and `phone` as plaintext strings in PostgreSQL. These are sensitive PII fields for homeowners and household members, including minors (`is_minor=True`). An HOA database breach would expose personal contact information for every household in the community.

- **Affected tables:** `parcel_contacts` (name, email, phone)
- **Recommended fix:** Field-level AES-256-GCM encryption using the pattern from Canary's `crypto.py`. Encrypt name, email, and phone at write time; decrypt at read time in the service layer.
- **Linear issue:** GRO-xxx

**P0-PME-02: Mortgage and financial data stored plaintext**

The Parcel model stores `mortgage_amount`, `mortgage_rate`, `mortgage_lender`, `mortgage_type`, `equity_estimate`, and the raw `enrichment` JSONB blob (from ATTOM API) without encryption. This is sensitive financial data that could be used for identity theft or targeted scams.

- **Affected tables:** `parcels` (mortgage_*, equity_estimate, enrichment)
- **Recommended fix:** Encrypt the `enrichment` JSONB blob at rest. For individual mortgage columns, apply field-level encryption or consolidate into the encrypted enrichment blob.
- **Linear issue:** GRO-xxx

**P0-PME-03: Owner name visible to all authenticated members via profile fallback**

`get_profile_props()` returns `parcel.owner_name` (from county records) as the `display_name` when no ParcelProfile exists. This means the county-record owner name is served to all authenticated members in the GeoJSON API response, bypassing the board-only gate that protects `owner_name` in the board view. A member who has not set up a profile has their county-record owner name exposed to all neighbors.

- **Affected code:** `cove/parcels/services.py:get_profile_props()` lines 19-23
- **Recommended fix:** Return `None` or a generic placeholder (e.g., "Lot 42") instead of `parcel.owner_name` for member-view callers. The `is_board` flag should gate this fallback.
- **Linear issue:** GRO-xxx

**P0-PME-04: Secrets in .env files**

`DATABASE_URL` and all credentials are stored in `.env` files, not in a secrets manager.

- **Recommended fix:** AWS Secrets Manager + `boto3` retrieval at startup.
- **Linear issue:** GRO-xxx (shared across all SDDs)

### P1 — Before GA

**P1-PME-01: No audit logging for parcel contact CRUD**

ParcelContact records (name, email, phone) can be created, updated, and deleted with no audit trail. There is no record of who accessed or modified contact PII. For HOA compliance, board members accessing member contact information should be logged.

- **Recommended fix:** Add `audit_log` entries for all ParcelContact create/update/delete operations, and for reads of contact data from board-only views.
- **Linear issue:** GRO-xxx

**P1-PME-02: No audit logging for tag operations**

Tag creation and assignment changes (which could be used to classify parcels as "threat" or "delinquent") have no audit trail beyond the `created_by` field on the record itself. Deletions are untracked.

- **Recommended fix:** Log tag create, assign, and remove operations to `audit_log` with actor, action, and target.
- **Linear issue:** GRO-xxx

**P1-PME-03: Duplicate tag assignment causes 500 error**

`bulk_assign_tag()` does not catch the `IntegrityError` from the `UniqueConstraint("apn", "tag_id")`. If a board member assigns a tag to a parcel that already has it, the route returns an unhandled 500 error.

- **Recommended fix:** Catch `IntegrityError` in `bulk_assign_tag()`, skip duplicates, and flash an informative message.
- **Linear issue:** GRO-xxx

**P1-PME-04: No data retention policy for parcel contacts**

ParcelContact records accumulate indefinitely. Former tenants, ex-spouses, and moved-away household members remain in the database with no automated cleanup or archival.

- **Recommended fix:** Implement retention policy: contacts marked inactive after ownership transfer, purged after 12 months of inactivity.
- **Linear issue:** GRO-xxx

**P1-PME-05: Board-only access check uses inline `if not current_user.is_board`**

Tag CRUD routes use inline `if not current_user.is_board: abort(403)` instead of the `@board_required` decorator used by the map boundary parse route. This is inconsistent and easy to miss in code review.

- **Recommended fix:** Replace inline board checks with `@board_required` decorator on all three tag routes.
- **Linear issue:** GRO-xxx

**P1-PME-06: No rate limiting on parcel API endpoints**

Authenticated users can call `/parcels/` and the tag CRUD endpoints without rate limits. A compromised session could scrape all parcel data.

- **Recommended fix:** Flask-Limiter on all `/parcels/*` routes (e.g., 60/minute for reads, 10/minute for writes).
- **Linear issue:** GRO-xxx

### P2 — Post-Launch

**P2-PME-01: `String(36)` UUID pattern on non-parcel models**

All non-parcel models use `String(36)` UUIDs instead of native `Mapped[uuid.UUID]`. Works correctly but is not platform standard.

- **Recommended fix:** Migrate to native UUID columns in a future schema update. Low risk, low urgency.

**P2-PME-02: `owner_name` stored on both Parcel and ParcelContact**

County-sourced `owner_name` on the Parcel model duplicates what should be in the primary ParcelContact record. This creates ambiguity about which is authoritative.

- **Recommended fix:** Designate ParcelContact `contact_type='primary'` as the source of truth. Deprecate `Parcel.owner_name` over time.

**P2-PME-03: ParcelSearchForm search is client-side only**

The `ParcelSearchForm` `q` field is rendered but search filtering appears to be handled client-side (Alpine.js). No server-side query filtering exists in the route.

- **Recommended fix:** Add server-side filtering for large-scale deployments. Acceptable for 81 lots.

---

## Known Issues & Design Decisions

### APN as primary key — deliberate exception to platform UUID standard

The `parcels.apn` and `research_parcels.apn` use the county APN as PK. This is correct because APN is the canonical, universal identifier for real property in LA County. It exists in county records, title documents, tax rolls, and all property APIs. The chain `Parcel (APN) -> Member -> Vote` is the foundation of HOA governance. Introducing a UUID PK would require translation at every import boundary and an additional join through every governance operation.

**Constraints:** APN values are treated as immutable. New downstream tables FK to `parcels.apn (String(20))`.

### Board-view gating in service, not route

The `is_board` flag is passed into `get_enriched_geojson()`, which controls field inclusion. This keeps gating logic in one place and ensures deterministic JSON shape.

### Profile sharing consent

`ParcelProfile` share toggles default to conservative settings (`share_household = False`). `get_profile_props()` enforces toggles — fields are `None` when the toggle is off.

### Data isolation by organization

Parcel list filters by `Parcel.organization_id == current_user.organization_id`. Tags scoped by org on `ParcelTag`. Comments scoped by org on `ParcelComment`. No cross-org parcel access.

---

## Production Readiness Checklist

- [ ] PII encrypted at rest (parcel contacts: name, email, phone; mortgage data; enrichment JSONB)
- [ ] Secrets in AWS Secrets Manager (not .env)
- [ ] Health check endpoint responds (covered by Cove `/health`)
- [ ] Audit logging for sensitive operations (contact CRUD, tag operations, board-view data access)
- [ ] Data retention policy implemented (parcel contacts, inactive member data)
- [ ] Rate limiting on parcel endpoints
- [ ] Error responses don't leak internals (duplicate tag assignment returns 500 with IntegrityError trace)
- [ ] Board-only routes use `@board_required` decorator consistently
- [ ] Owner name fallback in `get_profile_props()` does not leak county data to non-board members
