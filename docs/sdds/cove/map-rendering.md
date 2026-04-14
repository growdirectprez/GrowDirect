# Map Rendering

> **Status:** Production readiness review complete
> **Type:** App Service (Cove)
> **Namespace:** cove
> **Last updated:** 2026-04-13
> **Code location:** `Cove/cove/map/`, `Cove/cove/services/boundary_services.py`, `Cove/cove/map/layer_services.py`, `Cove/cove/models/land_division.py`
> **Split from:** Original `parcel-map-engine.md` (47K, 7500 words)
> **Companion SDD:** [Parcel Map Engine](parcel-map-engine.md) — Parcel identity, data model, contacts, tags

**Wiki:** [[Brain/wiki/cove-governance|Cove Governance]]

---

## Purpose

Map Rendering is the geographic visualization and boundary computation layer of Cove. It serves an interactive full-screen Leaflet.js map with enriched GeoJSON overlays, manages a file-backed layer system for easements and legal boundaries, parses metes-and-bounds legal descriptions into GeoJSON polygons using Claude API, and provides the land division hierarchy for Lot H research visualization.

The companion Parcel Identity Layer SDD covers the data model, contact management, and tag system that feed into map enrichment.

---

## Dependencies

| Dependency | Purpose |
|------------|---------|
| `growdirect_postgres` (cove database) | Parcel data for GeoJSON enrichment, LandDivision hierarchy |
| `growdirect_valkey` (DB 1) | Session backend |
| Parcel Identity Layer | `Parcel`, `ParcelProfile`, `ParcelTag` models; `get_profile_props()`, `get_tag_props()` |
| Cove auth module | `@login_required`, `@board_required` for boundary parsing |
| Claude API (`claude-sonnet-4-20250514`) | Legal description extraction for boundary parsing |
| Leaflet.js (npm) | Client-side map rendering |
| Alpine.js (npm) | Map UI interactivity (layer toggles, search, modals) |
| Shapely | Centroid computation for tract label placement |
| Static GeoJSON files | `wpbca-parcels.geojson`, `lot-h-parcels.geojson`, `neighborhood-parcels.geojson` |
| File-backed layer manifest | `layers/manifest.json` — overlay layer registry |

---

## Data Flow & PII Map

### What Enters

| Source | Data | Format |
|--------|------|--------|
| Static GeoJSON files (disk) | Community parcel boundaries, Lot H research parcels, neighborhood context | GeoJSON FeatureCollections |
| PostgreSQL (Parcel table) | Address, profile, tags, owner name, member status | Queried at request time |
| PostgreSQL (LandDivision table) | Land division hierarchy, tract geometry, covenant status | Queried at request time |
| Board member (POST form) | Legal description text, POB coordinates, layer metadata | HTTP POST |
| Claude API response | Structured bearing/distance calls parsed from legal text | JSON |

### What Is Stored

| Location | Data | Encryption | Classification |
|----------|------|------------|----------------|
| `Cove/cove/map/data/wpbca-parcels.geojson` | Parcel boundaries, no PII | N/A (static file) | public |
| `Cove/cove/map/data/lot-h-parcels.geojson` | Research parcel boundaries | N/A (static file) | public |
| `Cove/cove/map/data/layers/*.geojson` | Computed boundary polygons with legal description text | **Plaintext on disk** | internal |
| `Cove/cove/map/data/layers/manifest.json` | Layer registry (names, colors, categories) | Plaintext | internal |
| `land_divisions` table | `owner_name`, `address` | **Plaintext** | internal |
| `land_divisions` table | `land_value`, `improvement_value` | Plaintext | internal |

### What Exits

| Destination | Data | Gating |
|-------------|------|--------|
| Browser (Leaflet.js) — member view | GeoJSON with address, APN, lot email, profile (share-toggled), tags | `@login_required`, share toggles |
| Browser (Leaflet.js) — board view | Above + owner_name, assessed_value, member_name, assessment_status, membership_status | `is_board` service flag |
| Browser — overlay layers | Computed boundary polygons with legal text, source docs | `@login_required` |
| Browser — land division API | Hierarchy with owner_name, address, assessed values, covenant status | `@login_required` |
| Browser — research API | Lot H status, tract info, assessed values | `@login_required` |

### PII Classification

- **public:** Parcel geometry, tract numbers, boundary polygons (all from public county records)
- **internal:** Owner name (from county), land division addresses, assessed values (board-gated where applicable)
- **sensitive:** None stored directly by this service (contact PII is in the Parcel Identity Layer)

---

## API Contract

### HTTP Routes — Map Blueprint (`/map`)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/map/` | `@login_required` | Full-screen interactive map page (CSP-hardened) |
| GET | `/map/api/geojson` | `@login_required` | Enriched GeoJSON FeatureCollection (role-gated) |
| GET | `/map/api/lot-h` | `@login_required` | Lot H research parcel GeoJSON (static file) |
| GET | `/map/api/neighborhood` | `@login_required` | Neighborhood context GeoJSON (static file) |
| GET | `/map/api/layers/<filename>` | `@login_required` | Serve named overlay layer file (path-traversal guarded) |
| GET | `/map/api/layers` | `@login_required` | Layer manifest (JSON) |
| GET | `/map/api/categories` | `@login_required` | Layer categories (stub, returns empty) |
| GET | `/map/api/presets` | `@login_required` | Saved layer presets (stub, returns empty) |
| POST | `/map/api/boundaries/parse` | `@login_required` + `@board_required` | Parse legal description into GeoJSON boundary |
| GET | `/map/api/land-divisions` | `@login_required` | Land division GeoJSON (filterable) |
| GET | `/map/api/land-divisions/centroids` | `@login_required` | Tract label centroid coordinates |
| GET | `/map/api/land-divisions/<id>` | `@login_required` | Single land division with ancestry |
| GET | `/map/api/land-divisions/<id>/tree` | `@login_required` | Nested subtree from division |
| GET | `/map/api/lot-h/blast-zone` | `@login_required` | Covenant territory parcels |
| GET | `/map/api/lot-h/parcel/<apn>` | `@login_required` | Single land division leaf by APN |
| GET | `/map/api/overlays` | `@login_required` | Image overlay manifest |
| GET | `/map/data/overlays/<filename>` | `@login_required` | Serve image overlay file |
| GET | `/map/data/previews/<filename>` | `@login_required` | Serve survey preview image |

### GeoJSON Response — Member View (per feature)

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
    "lot_h_status": "lot_h_direct",
    "lot_h_status_label": "Lot H - Direct Reference",
    "display_name": "The Smith Family",
    "tags": [{"name": "Easement Issue", "color": "#dc2626"}],
    "comment_count": 3
  }
}
```

### Board-Only Additional Properties

```json
{
  "owner_name": "John Smith",
  "assessed_value": 1250000,
  "member_name": "John Smith",
  "assessment_status": "current",
  "membership_status": "active"
}
```

### Boundary Parse Form (`BoundaryParseForm`)

POST, CSRF enforced, `@board_required`:
- `legal_description: TextAreaField` — required, min 20 chars
- `pob_lat / pob_lng: StringField` — Point of Beginning coordinates
- `name: StringField` — layer display name, 2-255 chars
- `slug: StringField` — kebab-case, validated `^[a-z0-9-]+$`
- `source_doc: StringField` — required source document reference
- `recording_ref: StringField` — optional recording reference
- `color: SelectField` — map color
- `category: SelectField` — community | legal | regulatory | easement | proposals | heritage | custom

---

## Service Layer

### `cove/map/services.py`

| Function | Description |
|----------|-------------|
| `get_enriched_geojson(org_id, is_board)` | Primary GeoJSON endpoint. Queries Parcels with eager-loaded profile/tags/member/comments. Merges DB data into properties. Board flag gates owner name, assessed value, member status. |
| `get_lot_h_geojson()` | Reads and returns `lot-h-parcels.geojson` from disk. Empty FeatureCollection if absent. |
| `get_map_layers()` | Reads `layers/manifest.json` from disk. Marks `pending: True` for layers without files. |
| `get_land_divisions_geojson(*, before, relationship, parent_id)` | GeoJSON FeatureCollection of LandDivision nodes with optional filters. |
| `get_division_with_ancestry(division_id)` | Single division with ancestors and direct children. |
| `get_subtree(division_id)` | Nested tree rooted at a division. |
| `get_blast_zone(*, status, ownership_type, detail)` | Non-excepted, non-government land divisions. Optional summary mode. |
| `get_parcel_by_apn(apn)` | Land division leaf node by APN with ancestry. |
| `get_tract_centroids()` | Centroid coordinates for tract label placement (uses Shapely). |

### `cove/services/boundary_services.py`

Metes-and-bounds legal description parser and polygon computer.

| Function | Description |
|----------|-------------|
| `parse_bearing_string(text)` | Parse surveyor bearing (e.g., "N 45 30 00 E") into components. |
| `bearing_to_azimuth(prefix, degrees, minutes, seconds, suffix)` | Convert bearing to compass azimuth (0-360). |
| `traverse_call(start, azimuth, distance_ft)` | Compute next point from start + azimuth + distance. Earth constants at 33.74N. |
| `compute_polygon(pob, calls)` | Chain traverse calls into closed polygon ring. Returns `[(lng, lat), ...]`. |
| `extract_legal_description(text, api_key)` | Send legal text to Claude API, get structured bearing/distance JSON. |
| `extract_and_compute(text, pob, api_key)` | Full pipeline: extract -> convert bearings -> compute polygon. |
| `generate_boundary_geojson(...)` | Wrap polygon in GeoJSON FeatureCollection with full provenance. |
| `save_boundary(slug, geojson, layers_dir, ...)` | Write GeoJSON file + upsert manifest entry. Idempotent. |

### `cove/map/layer_services.py`

File-backed manifest CRUD.

| Function | Description |
|----------|-------------|
| `get_full_manifest()` | Returns `{categories, layers, presets}`. |
| `validate_slug(slug)` | Enforces `^[a-z0-9-]+$`. |
| `validate_geojson_filename(filename)` | Blocks path traversal (`..`, `/`, `\`), non-`.geojson`. |

---

## Operations

### Startup Sequence

1. Cove Flask app factory registers `map_bp` blueprint at `/map`.
2. Static GeoJSON files are expected at `Cove/cove/map/data/` (volume-mounted in dev).
3. Layer manifest at `Cove/cove/map/data/layers/manifest.json` is loaded on first request.
4. No database initialization required — models are shared with Parcel Identity Layer.

### Health Checks

No map-specific health check. Covered by Cove `/health` (database connectivity).

### Failure Modes

| Failure | Impact | Behavior |
|---------|--------|----------|
| `wpbca-parcels.geojson` missing | Map loads with no community parcels | Returns empty FeatureCollection, no exception |
| `lot-h-parcels.geojson` missing | No research overlay | Returns empty FeatureCollection |
| `manifest.json` missing | No overlay layers | Returns `{sections: [], layers: []}` |
| PostgreSQL down | GeoJSON enrichment fails | 500 on `/map/api/geojson` |
| Claude API failure | Boundary parse fails | Returns `{"error": "Boundary parse failed."}`, 500 |
| LLM returns invalid JSON | Parse error propagates | `ValueError` -> 500 handler |
| Invalid POB coordinates | Bad polygon computation | Returns 400 with validation message |
| Path traversal attempt on `/api/layers/<filename>` | Blocked | `abort(400)` |
| Layer file not found | 404 | `abort(404)` |

### Monitoring

No map-specific monitoring is implemented. Required before production:
- Alert on Claude API failure rate (boundary parsing)
- Alert on 500 error rate on `/map/*` routes
- Monitor GeoJSON response size (currently ~81 features, could grow)
- Log boundary parse operations (who parsed what, when)

### Configuration

| Setting | Source | Value |
|---------|--------|-------|
| `DATABASE_URL` | `.env` / compose | Standard Cove connection |
| `ANTHROPIC_API_KEY` | `.env` | Required for boundary parsing |
| GeoJSON data directory | Hardcoded | `Cove/cove/map/data/` |
| Layer manifest | Hardcoded | `Cove/cove/map/data/layers/manifest.json` |
| Basis of Bearings | Code constant | S 40d 23m 00s E, Tract Map 14649 |
| Earth constants | `boundary_services.py` | `FT_PER_DEG_LAT = 364567.0`, `FT_PER_DEG_LNG = 303470.0` at 33.74N |

### CSP Policy

The map page uses a Talisman-enforced Content Security Policy:
- `script-src: 'self' 'unsafe-eval'` — required for Alpine.js `new Function()` in `x-data`
- `img-src: 'self' data: https://*.tile.openstreetmap.org https://server.arcgisonline.com` — tile providers
- `style-src: 'self' 'unsafe-inline' https://fonts.googleapis.com` — Leaflet inline styles + fonts
- Nonce required for inline scripts (`content_security_policy_nonce_in=["script-src"]`)

---

## Deployment

### Docker Service

Runs inside `cove_flask` container. GeoJSON data directory is volume-mounted from `Cove/cove/` -> `/app/cove/`. Boundary-parsed GeoJSON files persist to host via mount.

### AWS Target

- **Compute:** ECS/Fargate (shared Cove task)
- **Database:** RDS PostgreSQL 17
- **Secrets:** AWS Secrets Manager for `ANTHROPIC_API_KEY`, `DATABASE_URL`
- **Static GeoJSON:** Baked into container image or S3 with EFS mount for generated layers

### CI/CD

- Standard Cove pipeline
- GeoJSON files included in Docker build context
- Generated boundary layers must be preserved across deploys (persistent volume or S3)

---

## Security

### Path Traversal Protection

`GET /map/api/layers/<filename>` rejects:
- Filenames not ending with `.geojson`
- Filenames containing `/` or `..`

`GET /map/data/overlays/<filename>` and `/map/data/previews/<filename>` apply the same `..` and `/` checks.

`layer_services.validate_geojson_filename()` applies identical rules for programmatic use.

### Board-Only Boundary Parsing

`POST /map/api/boundaries/parse` uses `@board_required` decorator. Non-board members receive 403.

### GeoJSON Board Gating

The `is_board` flag is set from `current_user.is_board` at the route level and passed into `get_enriched_geojson()`. The service has no session access — gating is deterministic based on the flag.

### CSRF

All POST forms inherit from `CoveForm`. CSRF enforced globally via `CSRFProtect(app)`.

### LandDivision Data Access

Land division endpoints serve data to all authenticated members (no board gate). This is intentional — the land division hierarchy is research data, not private HOA records. However, `owner_name` and assessed values from county records are included in responses.

---

## Code Review Findings

### P0 — Blocks Production

**P0-MR-01: Anthropic API key in .env file**

`ANTHROPIC_API_KEY` is stored in `.env`, not a secrets manager. This key provides access to the Claude API and could incur unbounded costs if leaked.

- **Recommended fix:** AWS Secrets Manager + `boto3` retrieval at startup.
- **Linear issue:** GRO-xxx (shared across all SDDs)

**P0-MR-02: No authentication on Claude API calls**

`extract_legal_description()` reads the API key from the env var with no validation that the caller is authorized. If the boundary parse endpoint were accidentally made public (e.g., `@board_required` removed during refactor), any user could trigger Claude API calls at the operator's expense.

- **Recommended fix:** Add a defense-in-depth check in `extract_and_compute()` that validates the caller has board role before proceeding with the API call.
- **Linear issue:** GRO-xxx

**P0-MR-03: LandDivision `owner_name` exposed to all authenticated users**

Land division API endpoints (`/api/land-divisions/*`, `/api/lot-h/blast-zone`, `/api/lot-h/parcel/<apn>`) return `owner_name` from county records to all authenticated members, not just board. For 5,500+ parcels, this exposes current property owner names to anyone with a Cove account.

- **Affected code:** `cove/map/services.py:_division_to_dict()` line 146
- **Recommended fix:** Gate `owner_name` behind an `is_board` flag on land division endpoints, consistent with the community parcel GeoJSON gating.
- **Linear issue:** GRO-xxx

### P1 — Before GA

**P1-MR-01: No audit logging for boundary parse operations**

Board members can parse legal descriptions and create overlay layers with no audit trail. Generated boundaries become permanent map layers that all members see.

- **Recommended fix:** Log boundary parse operations to `audit_log` with actor, source document, slug, and timestamp.
- **Linear issue:** GRO-xxx

**P1-MR-02: No rate limiting on map API endpoints**

All `/map/api/*` endpoints are unprotected by rate limiting. A compromised session could scrape the entire GeoJSON dataset including all parcel data, land divisions, and research parcels.

- **Recommended fix:** Flask-Limiter on all `/map/api/*` routes (e.g., 30/minute for GeoJSON, 5/minute for boundary parse).
- **Linear issue:** GRO-xxx

**P1-MR-03: Generated boundary layers persist with no access control**

Once a boundary is parsed and saved, the GeoJSON file is accessible to any authenticated user via `/map/api/layers/<slug>.geojson`. There is no per-layer access control. Legal description text (from recorded deeds) is embedded in the GeoJSON properties.

- **Recommended fix:** For current scale (one HOA), this is acceptable. Add access control if layers become org-scoped in multi-tenant deployment.
- **Linear issue:** GRO-xxx

**P1-MR-04: Error responses may leak exception details**

The boundary parse error handler catches `Exception` broadly and previously returned `f"Boundary parse failed: {e}"` which could expose Claude API error details or stack trace fragments. The current code returns a generic message, but the `logger.exception()` call writes full traces to logs.

- **Recommended fix:** Verify logs are not exposed to clients. The current generic error message is correct.
- **Linear issue:** GRO-xxx

**P1-MR-05: `unsafe-eval` in CSP for Alpine.js**

The map page CSP includes `'unsafe-eval'` to support Alpine.js's standard build which uses `new Function()`. This weakens XSS protection.

- **Recommended fix:** Switch to Alpine.js CSP build (`@alpinejs/csp`) which avoids `eval`. This eliminates `unsafe-eval` from the CSP.
- **Linear issue:** GRO-xxx

**P1-MR-06: No data retention policy for generated layers**

Boundary-parsed GeoJSON files accumulate in `layers/` with no cleanup mechanism. The manifest grows indefinitely.

- **Recommended fix:** Add soft-delete to manifest entries. Archive layers older than the retention window. For current scale (handful of layers), this is low urgency.
- **Linear issue:** GRO-xxx

### P2 — Post-Launch

**P2-MR-01: Hardcoded GeoJSON data paths**

GeoJSON data directory and manifest path are hardcoded in `map/services.py` and `map/routes.py`. No configuration override possible.

- **Recommended fix:** Move to config keys (`MAP_DATA_DIR`, `MAP_LAYERS_DIR`) for flexibility in deployment.

**P2-MR-02: No caching on static GeoJSON files**

`wpbca-parcels.geojson` and `lot-h-parcels.geojson` are read from disk on every request. For 81 community parcels this is fast, but the 5,500+ Lot H file could benefit from caching.

- **Recommended fix:** Add `Cache-Control` headers or Valkey cache for static GeoJSON files.

**P2-MR-03: Shapely lazy import in production path**

`get_tract_centroids()` uses `from shapely.geometry import shape as shapely_shape` inside the function body. If Shapely is not installed, this silently swallows the exception and skips centroids.

- **Recommended fix:** Make Shapely a required dependency or add a startup check that warns if missing.

**P2-MR-04: ResearchParcel model documented in original SDD but not found in codebase**

The original SDD documents a `ResearchParcel` model and several service functions (`get_research_stats`, `get_research_chart_data`, `get_research_parcel`). These are not present in the current codebase — the `LandDivision` model appears to have superseded this design. The SDD should reflect the actual implementation.

- **Recommended fix:** Confirm whether ResearchParcel was replaced by LandDivision and update the SDD accordingly. Remove phantom code references.

---

## Testing

### Unit Tests

- `test_parse_bearing_string`: Valid formats (spaced, compact, with symbols), invalid raises `ValueError`
- `test_bearing_to_azimuth`: All four quadrants, boundary cases (due north, due south)
- `test_traverse_call`: Known coordinate traversal against surveyed control point
- `test_compute_polygon`: Ring closure, correct (lng, lat) GeoJSON ordering
- `test_get_profile_props`: Share toggle enforcement, default to owner name fallback
- `test_get_tag_props`: Assignment source_url override, null tag handling

### Integration Tests

- `test_geojson_member_view`: Board-gated fields absent for member-role caller
- `test_geojson_board_view`: Board-gated fields present for board-role caller
- `test_boundary_parse_board_only`: Non-board member receives 403
- `test_layer_file_path_traversal`: Rejects `../../../etc/passwd.geojson`

### Smoke Tests

- `GET /map/` returns 200 for authenticated member
- `GET /map/api/geojson` returns valid GeoJSON FeatureCollection

### Test Fixtures

- `org`, `member` (member role), `board_member` (board role), `parcel` (bound to org), `parcel_profile` (with all toggles), `parcel_tag` + `assignment`

---

## Production Readiness Checklist

- [ ] PII encrypted at rest (owner_name on land_divisions if classified as sensitive)
- [ ] Secrets in AWS Secrets Manager (`ANTHROPIC_API_KEY`, `DATABASE_URL`)
- [ ] Health check endpoint responds (covered by Cove `/health`)
- [ ] Audit logging for boundary parse operations
- [ ] Data retention policy for generated boundary layers
- [ ] Rate limiting on map API endpoints
- [ ] Error responses don't leak internals (verified: generic error message on boundary parse)
- [ ] CSP tightened (remove `unsafe-eval` by switching to Alpine.js CSP build)
- [ ] LandDivision owner_name gated behind board role for non-research endpoints
- [ ] Generated layers have access control for multi-tenant deployment
