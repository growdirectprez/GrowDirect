# SDD: Board Module

**Status:** Active
**Last updated:** 2026-03-29
**Blueprint:** `/board` prefix, `board_bp`

## Overview

Board-only administrative interface covering the dashboard, member roster, parcel contact management, and bulletin notifications. Tag management routes are in the parcels blueprint; boundary parsing is in the map blueprint. Both use shared services in `cove/services/`.

---

## Routes

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/board/` | `@board_required` | Dashboard: member count, quick nav |
| GET | `/board/members` | `@board_required` | Member roster table with client-side search |
| GET | `/board/diagrams` | `@board_required` | Diagrams page |
| GET/POST | `/board/bulletin` | `@board_required` | Send a notification bulletin to all active members |
| GET | `/board/parcels/<apn>/contacts` | `@board_required` | List and manage contacts for a parcel |
| POST | `/board/parcels/<apn>/contacts/add` | `@board_required` | Add a new contact to a parcel |
| GET/POST | `/board/parcels/<apn>/contacts/<contact_id>/edit` | `@board_required` | Edit an existing parcel contact |
| POST | `/board/parcels/<apn>/contacts/<contact_id>/delete` | `@board_required` | Delete a parcel contact |

All routes use `@login_required` plus the `@board_required` decorator from `cove/auth/decorators.py`.

**Routes moved to other modules (not in board):**
- Tag CRUD → `cove/parcels/routes.py` (uses `cove/services/tag_services.py`)
- Boundary parsing → `cove/map/routes.py` (uses `cove/services/boundary_services.py`)

---

## Forms

**`cove/board/forms.py`**

Tag forms (`TagCreateForm`, `TagAssignForm`, `TagRemoveForm`) are defined in `cove/parcels/forms.py`, not in the board module. See the parcels SDD.

### `BulletinForm` (extends `CoveForm`)

| Field | Type | Validators | Notes |
|-------|------|------------|-------|
| `title` | `StringField` | DataRequired, Length(5-255) | Bulletin subject line |
| `body` | `TextAreaField` | DataRequired, Length(10-5000) | Message body |

`BoundaryParseForm` is defined in `cove/map/forms.py`. See the map module.

### `ParcelContactForm` (extends `CoveForm`)

| Field | Type | Validators | Notes |
|-------|------|------------|-------|
| `name` | `StringField` | DataRequired, Length(max=255) | Contact name |
| `email` | `StringField` | Optional, Email, Length(max=255) | |
| `phone` | `StringField` | Optional, Length(max=20) | |
| `contact_type` | `SelectField` | DataRequired | owner, resident, tenant, emergency, etc. |
| `relationship` | `StringField` | Optional, Length(max=100) | Relationship to property |
| `is_minor` | `BooleanField` | | Under 18 flag |
| `notes` | `TextAreaField` | Optional, Length(max=1000) | |

---

## Models

### `ParcelTag` (`parcel_tags`)

| Column | Type | Notes |
|--------|------|-------|
| `id` | String(36) PK | UUID |
| `organization_id` | FK -> organizations | Scope |
| `name` | String(255) | |
| `color` | String(7) | Hex, default `#6B7280` |
| `category` | String(50) | `founding`, `governance`, `property`, `threat`, `regulatory`, `geographic`, `custom` |
| `description` | Text nullable | |
| `source_url` | String(500) nullable | Default link for this tag |
| `created_by` | FK -> members | |

### `ParcelTagAssignment` (`parcel_tag_assignments`)

| Column | Type | Notes |
|--------|------|-------|
| `id` | String(36) PK | UUID |
| `parcel_id` | FK -> parcels | |
| `tag_id` | FK -> parcel_tags | |
| `comment` | Text nullable | Assignment-level note |
| `source_url` | String(500) nullable | Overrides tag's `source_url` when present |
| `created_by` | FK -> members | |

Unique constraint: `(parcel_id, tag_id)`. Cascade delete from `ParcelTag`.

---

## Services

### Shared services (consolidated 2026-03-29)

Tag and boundary services were consolidated from module-local copies into shared modules:
- **Tag services**: `cove/services/tag_services.py` — see parcels SDD for full API
- **Boundary services**: `cove/services/boundary_services.py` — see map module for full API

### Notification integration

The bulletin route uses `notify_all_members()` from `cove/notifications/services.py` to send a notification (type `"bulletin"`) with email delivery to all active members.

---

## Templates

| File | What it renders |
|------|----------------|
| `board/dashboard.html` | Stats grid (member count, parcel count); quick-action cards; board-tools nav grid |
| `board/members.html` | Member table (name, lot email, status, onboarded, vote weight); Alpine.js client-side search |
| `board/diagrams.html` | Diagrams page |
| `board/bulletin.html` | Bulletin send form: subject and message body |
| `board/parcel_contacts.html` | Contact list for a parcel; add/edit/delete forms; display order |

---

## Notes

- Board module uses the `@board_required` decorator from `cove/auth/decorators.py` on all routes.
- Parcel contact CRUD operates directly on `db.session` in routes (no services layer yet — tech debt item for Phase 2).
- Tag management and boundary parsing have been moved to the parcels and map modules respectively; shared services live in `cove/services/`.
