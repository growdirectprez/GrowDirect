# SDD: Vault Module

**Status:** Active
**Last updated:** 2026-03-29
**Blueprint:** `/vault` prefix, `vault_bp`

## Overview

Document upload, versioning, categorized browsing, and file downloads with role-based access tiers. Documents are assigned an `access_tier` (member, arc, board) that controls visibility — members see member-tier docs, ARC members see member + arc, board sees all. Files are stored on disk with UUID filenames; metadata and version history live in PostgreSQL.

---

## Routes

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/vault/` | `login_required` | Document library with category tabs and title search |
| GET | `/vault/upload` | `login_required` | Upload form |
| POST | `/vault/upload` | `login_required` | Process upload: validate, save file, create `Document` + v1 `DocumentVersion`, audit |
| GET | `/vault/<doc_id>` | `login_required` | Document detail: metadata, version history, download links; board sees "New Version" button |
| GET | `/vault/<doc_id>/download` | `login_required` | Download latest version via `send_file` with `as_attachment=True` |
| GET | `/vault/<doc_id>/download/<version_id>` | `login_required` | Download a specific version via `send_file` with `as_attachment=True` |
| POST | `/vault/<doc_id>/version` | `login_required` | Upload a new version of an existing document |

All document routes check `doc.organization_id == current_user.organization_id` (403 otherwise).

---

## Models

### `Document` (`documents`)

| Column | Type | Notes |
|--------|------|-------|
| `id` | String(36) PK | UUID |
| `organization_id` | FK -> organizations | |
| `title` | String(500) | |
| `category` | String(50) | See CATEGORIES below |
| `description` | Text nullable | |
| `access_tier` | String(10) | Access level: `member`, `arc`, or `board` |
| `current_version` | Integer | Incremented on each new version |
| `uploaded_by` | FK -> members | |
| `embedding` | `Vector(1024)` | For semantic search via cosine distance |
| `created_at` | DateTime | |
| `updated_at` | DateTime | `onupdate=datetime.utcnow` |

`Document.versions` -> `[DocumentVersion]`, ordered by `version.desc()`.

### `DocumentVersion` (`document_versions`)

| Column | Type | Notes |
|--------|------|-------|
| `id` | String(36) PK | UUID |
| `document_id` | FK -> documents | |
| `version` | Integer | Sequential, starts at 1 |
| `filename` | String(500) | Original upload filename |
| `file_path` | String(1000) | Absolute path to UUID-named file on disk |
| `file_size` | Integer | Bytes |
| `mime_type` | String(100) | Guessed via `mimetypes` |
| `change_notes` | Text nullable | |
| `uploaded_by` | FK -> members | |

---

## Services

### `cove/vault/services.py`

**Constants:**
- `CATEGORIES`: `[governing_documents, minutes, financial_records, notices, correspondence, forms, historical]`
- `ALLOWED_EXTENSIONS`: `{pdf, doc, docx, xls, xlsx, png, jpg, jpeg, gif, txt}`

| Function | What it does |
|----------|-------------|
| `allowed_file(filename)` | Checks extension against `ALLOWED_EXTENSIONS` |
| `upload_document(org_id, uploaded_by, filename, file_data, title, category, description, access_tier, upload_folder, user_max_tier)` | Validates category + extension + tier access; creates `Document`; calls `_create_version_internal` for v1; audits `document.uploaded`; returns `Document` or `None` |
| `get_user_max_tier(member)` | Returns the highest `AccessTier` the member can access based on roles (`is_board` → board, `is_arc` → arc, else member) |
| `_create_version_internal(doc_id, uploaded_by, filename, file_data, version_number, change_notes, upload_folder)` | Saves file as `{uuid}.{ext}` in upload folder; creates `DocumentVersion`; handles both `FileStorage` (`.save()`) and file-like objects; returns `DocumentVersion` or `None` |
| `get_document(doc_id)` | `db.session.get(Document, doc_id)` |
| `list_documents(org_id, category, search, public_only)` | Filtered select with optional `ilike` title search; ordered by `updated_at desc` |
| `get_version(version_id)` | `db.session.get(DocumentVersion, version_id)` |
| `create_version(doc_id, uploaded_by, filename, file_data, change_notes, upload_folder)` | Validates file; increments `doc.current_version`; calls `_create_version_internal`; audits `document.versioned`; returns `DocumentVersion` or `None` |

Audit calls go through `_audit` imported from `cove.governance.services`.

---

## Forms

### `DocumentUploadForm` (Flask-WTF)

Fields: `title`, `description`, `category` (SelectField from `CATEGORIES`), `file` (FileField), `access_tier` (SelectField: member/arc/board), `submit`.

### `DocumentVersionForm` (Flask-WTF)

Fields: `file` (FileField), `change_notes` (TextAreaField), `submit`.

### `DocumentSearchForm` (Flask-WTF)

Used for the index page search/filter bar (instantiated with `meta={"csrf": False}`).

---

## Templates

| File | What it renders |
|------|----------------|
| `vault/index.html` | Title search bar; category tab strip; document grid (cards showing title, category badge, description excerpt, version, updated date); empty state with upload link |
| `vault/upload.html` | Upload form: title, description, category select, drag-and-drop file zone, public checkbox; WTForms field rendering with inline error display |
| `vault/document.html` | Document header (title, category, public badge, version); description block; metadata grid (created, updated, version count); download-latest button; version history timeline (v# badge, filename, size, MIME, change notes, per-version download); Alpine.js toggle for new-version form (board only) |

---

## Notes

- Files are served via `send_file(version.file_path, download_name=version.filename, as_attachment=True, mimetype=version.mime_type)` — using the full file path directly from the `DocumentVersion.file_path` column.
- `UPLOAD_FOLDER` is set in app config; mounted as a Docker volume (`../uploads:/app/uploads`) in dev.
- `list_documents` always filters by `org_id`; `public_only=False` is used for the vault index (authenticated members see all org documents).
- No delete route exists — documents and versions are append-only.
- Embedding column uses `Vector(1024)` (1024-dimension vectors from `qwen3-embedding:8b` model via Ollama).
