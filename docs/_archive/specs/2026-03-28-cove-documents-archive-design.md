# Cove Documents & Archive Redesign

**Date:** 2026-03-28
**Status:** Draft
**App:** Cove (HOA governance)

---

## Problem

The current Vault blueprint treats all documents as org-wide with a binary `is_public` flag. The Archive blueprint has no access control beyond login. There is no way to distinguish between community disclosures, confidential board materials, ARC documents, and research/working documents. There is no path to promote research documents from the Archive into the member-facing library.

## Design

### Three-Tier Access Model for Community Documents

Rename the Vault to **Community Documents**. Replace the `is_public` boolean with an `access_tier` enum:

| Tier | Audience | Examples |
|------|----------|----------|
| `member` | All authenticated WPBCA members | CC&Rs, bylaws, meeting minutes, financial reports, Davis-Stirling required disclosures, FAQs, policy statements |
| `arc` | ARC committee members + board directors + admins | Architectural guidelines, ARC review templates, ARC working documents |
| `board` | Current directors and admins | Executive session notes, legal correspondence, vendor contracts, confidential board materials |

Access enforcement:
- `member` tier: any authenticated member
- `arc` tier: members with `can_access_arc` permission, board role, or admin role
- `board` tier: members with board or admin role

Higher-privilege users see all tiers at or below their level (board/admin sees everything, ARC sees member + ARC, members see member only).

**Note on `is_public` removal:** The existing `is_public` flag was intended for unauthenticated public access. This design intentionally removes anonymous access — all documents require login. No documents currently served to the public internet lose availability; Davis-Stirling required disclosures are available to all authenticated members via the `member` tier.

### Data Model Changes

**Document model:**
- Add `access_tier` column: PostgreSQL Enum type `AccessTier` with values `member`, `arc`, `board`, default `member`
- Drop `is_public` column
- Migration: `is_public=True` maps to `member`, `is_public=False` maps to `board`

**Role model:**
- Add `can_access_arc: Mapped[bool]` permission flag alongside existing flags (`can_vote`, `can_manage_members`, etc.), default `False`

**Member model:**
- Add `is_arc` property (analogous to existing `is_board`, `is_admin`, `is_inspector`) that checks for any active role with `can_access_arc=True`

No new models. No changes to `DocumentVersion`.

### Archive Access Gate

The Archive splits into two access levels:

**Member-accessible (read-only, as today):**
- `/archive/` — narrative landing page
- `/archive/timeline` — chronological history
- `/archive/chain` — chain of title
- `/archive/catalog` — document catalog (merged view of archive entries + live vault documents)

These community history pages remain available to all authenticated members. They contain public historical context, not research materials.

**ARC/board/admin-gated:**
- `/archive/doc/<category>/<slug>` — individual document viewer (research documents)
- `/archive/originals/<path:filepath>` — binary files
- `/archive/data/<filename>` — CSV/JSON data files
- `POST /archive/request/<path:filepath>` — request original document
- Promote action (new, see below)

Access check: `member.is_arc or member.is_board or member.is_admin`. Board directors have full Archive access, same as ARC members.

The Archive remains filesystem-based. No database tables, no changes to the markdown + originals structure. The Archive is the research/dev sandbox workspace.

### Promote Action: Archive to Community Documents

New feature on Archive document pages (ARC/admin-gated routes only): a "Promote to Community Documents" button.

**Flow:**
1. User views an Archive document (original PDF, image, or .docx)
2. Clicks "Promote to Community Documents"
3. `GET /archive/promote/<path:filepath>` renders a form: select access tier, category, title, optional description
4. `POST /archive/promote/<path:filepath>` handles submission: copies the file from Archive filesystem into Vault storage (UUID-named), creates a new `Document` + `DocumentVersion` record in the database
5. The Archive original stays untouched — this is an explicit copy, not a move

**Embeddings:** Promoted documents do not get embeddings generated at promote time. Embedding generation is deferred to a background process or manual trigger, consistent with how the existing Vault handles uploads. The `embedding` column on `DocumentVersion` is nullable.

**Why copy, not link:** Archive content is local filesystem / dev sandbox material. Community Documents are database-tracked records that ship with QA/prod deployments. Keeping them separate means Archive files never accidentally leak into production builds.

**Promotable file types:** Files in `/archive/originals/` with extensions matching the existing `ALLOWED_EXTENSIONS` list (pdf, doc, docx, xls, xlsx, png, jpg, jpeg, gif, txt). Markdown narrative documents are not promotable — they are research context, not standalone documents.

### Upload Permissions

Upload and version creation follow the same tier rules as read access:
- Any authenticated member can upload `member`-tier documents
- ARC, board, and admin members can upload `arc`-tier documents
- Board and admin members can upload `board`-tier documents

The upload form's `access_tier` dropdown only shows tiers the current user has permission to use.

### Service Layer Changes

The `list_documents()` service function currently accepts a `public_only: bool` parameter. This is replaced with tier-aware filtering:
- Accept the current user's role context
- Return only documents the user is authorized to see based on their highest access level
- The filtering happens in the query (server-side), not in the template

The `upload_document()` service validates that the uploader has permission for the selected `access_tier`.

The promote form's category dropdown uses the same `CATEGORIES` constant from `vault/services.py` (updated to include `historical` in place of `archive`).

### Route Changes

**Community Documents (Vault blueprint):**
- Routes keep the `/vault/` prefix (internal naming; UI displays "Community Documents")
- Index page: tier filter tabs visible based on user role
  - Members see: all member-tier docs
  - ARC members see: member + ARC tabs
  - Board members see: member + ARC + board tabs
- Upload form: `access_tier` dropdown replaces `is_public` checkbox (choices filtered by user role)
- Document detail page: tier badge displayed, 403 if user lacks access
- All existing templates updated: `vault/upload.html` (dropdown), `vault/index.html` (tier tabs + filtering), `vault/document.html` (tier badge)

**Archive blueprint:**
- Community pages remain member-accessible (narrative, timeline, chain, catalog)
- `/archive/catalog` filters vault documents by viewer's access level when merging with archive entries
- Research/document pages gated to ARC/board/admin role
- New routes: `GET/POST /archive/promote/<path:filepath>` — both ARC/board/admin-gated, CSRF-protected promote form and handler
- Existing routes unchanged otherwise

### Category Cleanup

Rename the existing `archive` category in the Vault category list to `historical` to avoid naming confusion with the Archive blueprint.

Updated category list: `governing_documents`, `minutes`, `financial_records`, `notices`, `correspondence`, `forms`, `historical`.

Update the `CATEGORIES` constant in `vault/services.py` and the `DocumentUploadForm` category choices. The promote form reuses the same constant.

### Migration

A single Alembic migration handles all schema changes:
1. Add `access_tier` Enum column with default `member`
2. Migrate data: `is_public=True` → `member`, `is_public=False` → `board`
3. Drop `is_public` column
4. Update `category='archive'` → `category='historical'`
5. Add `can_access_arc` boolean to `roles` table with default `False`

### What Stays the Same

- Archive filesystem structure (markdown + originals, `INDEX.md` catalog, category folders)
- Document versioning in Community Documents
- Semantic search / pgvector embeddings on Document model
- Append-only policy (no delete routes)
- Organization-scoped data access
- Audit logging on uploads and promotions

### Davis-Stirling Compliance

The `member` tier satisfies California Civil Code requirements for document availability:
- Section 5200: annual budget report and disclosures
- Section 4525: document inspection rights
- Section 5210: financial statement distribution

Board-confidential materials (executive session records per Civil Code 4935) stay in the `board` tier, not accessible to general membership.

## Out of Scope

- 501(c)(5) organization structure — future project, research materials live in Archive for now
- Document workflows / approval processes
- Collaborative editing or comments on documents
- Full-text search beyond existing title ilike + semantic embeddings
- OCR or text extraction from uploaded files
- Document expiration or retention policies
- Per-document access control (tier-based, not per-document ACLs)
- Anonymous/unauthenticated public document access
