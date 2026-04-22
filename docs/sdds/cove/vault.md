# Vault Module

**Status:** Active
**Type:** App Service
**Last updated:** 2026-04-13
**Blueprint:** `vault_bp` at `/documents` (redirected from `/vault` via GRO-395)
**Wiki:** [[Brain/wiki/cove-governance|Cove Governance]] | [[Brain/wiki/cove-legal-framework|Cove Legal Framework]]
**Architecture:** [[docs/sdds/cove/architecture|Cove Architecture]]
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[Canary/docs/profiles/ops/Tom|Tom]] · **Operator role:** [[Canary/docs/profiles/ops/Jeremy|Jeremy]]

---

## Purpose

Document upload, versioning, categorized browsing, and file downloads with role-based access tiers. Documents are assigned an `access_tier` (member, arc, board) that controls visibility. Files are stored on disk with UUID filenames; metadata and version history live in PostgreSQL.

---

## Dependencies

| Dependency | Role | Required |
|------------|------|----------|
| PostgreSQL (`cove` database) | Document/version metadata, embeddings | Yes |
| Filesystem (`UPLOAD_FOLDER`) | Binary file storage | Yes |
| Ollama | Document embeddings for semantic search | No |
| `cove.governance.services._audit` | Audit log writes | Yes |
| `cove.services.file_security.validate_file_path` | Path traversal prevention on downloads | Yes |

---

## Data Flow & PII Map

### What enters
- File uploads via multipart form POST (board members only)
- Document metadata: title, category, description, access_tier

### What's stored

| Table | Field | Classification | Encryption |
|-------|-------|---------------|------------|
| `documents` | `title`, `description` | internal | Plaintext |
| `documents` | `uploaded_by` (FK) | internal | Plaintext (UUID ref) |
| `documents` | `embedding` | internal | Plaintext (Vector(1024)) |
| `document_versions` | `filename` (original name) | internal | Plaintext |
| `document_versions` | `file_path` (disk location) | internal | Plaintext |
| Filesystem | Uploaded files | varies by content | **Not encrypted at rest (P1)** |

### What exits
- File downloads via `send_file()` with `as_attachment=True`
- Document metadata rendered in templates (authenticated users only)

**PII exposure:** Documents themselves may contain PII (member names in minutes, financial records). The vault stores them as opaque blobs -- PII classification depends on document category and access tier.

---

## API Contract

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/documents/` | `login_required` | Document library with category tabs and search |
| GET | `/documents/upload` | `login_required` + `board_required` | Upload form |
| POST | `/documents/upload` | `login_required` + `board_required` | Process upload |
| GET | `/documents/<doc_id>` | `login_required` | Document detail with version history |
| GET | `/documents/<doc_id>/download` | `login_required` | Download latest version |
| GET | `/documents/<doc_id>/download/<version_id>` | `login_required` | Download specific version |
| POST | `/documents/<doc_id>/version` | `login_required` + `board_required` | Upload new version |
| GET | `/documents/bylaws` | `login_required` | Redirect to governing_documents category |
| GET | `/documents/minutes` | `login_required` | Redirect to minutes category |

### Access Tier Enforcement

Every document read checks two gates:
1. **Organization scoping:** `doc.organization_id == current_user.organization_id` (403 otherwise)
2. **Tier check:** `_check_doc_tier_access(doc)` verifies user's max tier includes the document's tier

Tier hierarchy: `member < arc < board`. Board sees all; ARC sees member + arc; member sees member only.

Upload routes additionally use `@board_required` decorator -- only board members can upload or version documents.

---

## Models

### `Document` (`documents`)

| Column | Type | Notes |
|--------|------|-------|
| `id` | String(36) PK | UUID |
| `organization_id` | FK -> organizations | Tenant scoping |
| `title` | String(500) | |
| `category` | String(50) | governing_documents, minutes, financial_records, notices, correspondence, forms, historical |
| `description` | Text nullable | |
| `access_tier` | String(10) | `member`, `arc`, or `board` |
| `current_version` | Integer | Incremented per version |
| `uploaded_by` | FK -> members | |
| `embedding` | Vector(1024) | Semantic search |
| `created_at` / `updated_at` | DateTime | |

### `DocumentVersion` (`document_versions`)

| Column | Type | Notes |
|--------|------|-------|
| `id` | String(36) PK | UUID |
| `document_id` | FK -> documents | |
| `version` | Integer | Sequential from 1 |
| `filename` | String(500) | Original upload name |
| `file_path` | String(1000) | Path to UUID-named file on disk |
| `file_size` | Integer | Bytes |
| `mime_type` | String(100) | Guessed via `mimetypes` |
| `change_notes` | Text nullable | |
| `uploaded_by` | FK -> members | |

---

## Services (`cove/vault/services.py`)

| Function | Description |
|----------|-------------|
| `upload_document(...)` | Validates tier, category, extension; creates Document + v1 version; audits |
| `create_version(...)` | Validates file; increments version; audits |
| `list_documents(org_id, category, search, user_max_tier)` | Filtered query with tier-based access control and ILIKE search (escaped) |
| `get_document(doc_id)` | Simple lookup |
| `get_version(version_id)` | Simple lookup |
| `search_documents_semantic(org_id, query, limit)` | Cosine distance search via pgvector |
| `get_user_max_tier(user)` | Returns AccessTier enum based on roles |

File storage: UUID-named files in `UPLOAD_FOLDER`. Extension preserved from original filename.

---

## Operations

### Startup
No module-specific startup. Upload directory created by app factory.

### Health Checks
No module-specific health check. Depends on DB connection and filesystem write access.

### Failure Modes

| Failure | Impact | Recovery |
|---------|--------|----------|
| DB down | All routes return 500 | Automatic reconnect via pool pre-ping |
| Filesystem full | Upload fails, returns None | Manual disk cleanup |
| Ollama down | Semantic search returns no results | Graceful -- embedding is None |
| File missing from disk | Download returns 404 via `validate_file_path` | Manual file restoration |

### Monitoring

- Alert on: upload failures (service returns None), disk usage on upload volume
- Normal: <100 documents per org, <10 versions per document

---

## Deployment

- **Docker**: Files stored in mounted volume (`../uploads:/app/uploads`)
- **AWS**: EFS mount for upload volume, shared across ECS tasks
- **Backup**: Upload volume needs independent backup (not in DB dumps)
- **Migration**: Alembic for schema; file volume must persist across deploys

---

## Code Review Findings

| # | Severity | Finding | Recommended Fix |
|---|----------|---------|----------------|
| 1 | **P0** | Uploaded files not encrypted at rest on disk | Encrypt files before writing to disk, decrypt on read |
| 2 | **P1** | No audit trail for document downloads -- only uploads and versioning are audited | Add `document.downloaded` audit entry in download routes |
| 3 | **P1** | `file_path` stored as absolute path in DB -- ties data to specific filesystem layout | Store relative paths; resolve against `UPLOAD_FOLDER` at runtime |
| 4 | **P1** | No file size validation beyond `MAX_CONTENT_LENGTH` (50MB global) -- no per-category limits | Enforce `MAX_DOCUMENT_SIZE` (25MB) in service layer |
| 5 | **P1** | No virus/malware scanning on uploaded files | Add ClamAV or equivalent before file storage |
| 6 | **P2** | No pagination on document list -- loads all org documents | Add server-side pagination (offset/limit) |
| 7 | **P2** | Embedding generation not triggered on upload -- only available via seed script | Generate embedding asynchronously on document creation |
| 8 | **P2** | No delete capability -- documents are append-only | Add soft delete with board authorization |

---

## Production Readiness Checklist

- [ ] Uploaded files encrypted at rest
- [ ] Secrets in AWS Secrets Manager
- [x] Health check endpoint responds (via app-level `/health`)
- [ ] Audit logging for downloads (currently only uploads/versions)
- [ ] Data retention policy for documents
- [x] Rate limiting (via app-level limiter)
- [x] Error responses don't leak internals (404 on path validation failure)
- [x] Access tier enforcement on all read routes
- [ ] File size validation per category
- [ ] Virus scanning on uploads
