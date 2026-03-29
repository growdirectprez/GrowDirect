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
| `arc` | ARC committee members + board directors | Architectural guidelines, ARC review templates, public-facing ARC informational documents |
| `board` | Current directors only | Executive session notes, legal correspondence, vendor contracts, confidential board materials |

Access enforcement:
- `member` tier: any authenticated member
- `arc` tier: members with `can_access_arc` permission or board role
- `board` tier: members with board role only

Higher-privilege users see all tiers at or below their level (board sees everything, ARC sees member + ARC, members see member only).

### Data Model Changes

**Document model:**
- Add `access_tier` column: `String`, one of `member`, `board`, `arc`, default `member`
- Drop `is_public` column
- Migration: `is_public=True` maps to `member`, `is_public=False` maps to `board`

**Role model:**
- Add `can_access_arc` boolean permission flag alongside existing flags (`can_vote`, `can_manage_members`, etc.)

No new models. No changes to `DocumentVersion`.

### Archive Access Gate

All Archive routes (`/archive/*`) get an ARC/admin role check. Currently they only require `@login_required`. After this change, only users with `can_access_arc` or board role can access the Archive.

The Archive remains filesystem-based. No database tables, no changes to the markdown + originals structure. The Archive is the research/dev sandbox workspace.

### Promote Action: Archive to Community Documents

New feature on Archive document pages: a "Promote to Community Documents" button.

**Flow:**
1. User views an Archive document (markdown or original PDF/image)
2. Clicks "Promote to Community Documents"
3. Form appears: select access tier, category, title, optional description
4. On submit: the file is copied from the Archive filesystem into Vault storage (UUID-named), a new `Document` + `DocumentVersion` record is created in the database
5. The Archive original stays untouched — this is an explicit copy, not a move

**Why copy, not link:** Archive content is local filesystem / dev sandbox material. Community Documents are database-tracked records that ship with QA/prod deployments. Keeping them separate means Archive files never accidentally leak into production builds.

Only files in `/archive/originals/` can be promoted (binary files: PDFs, images). Markdown narrative documents are not promotable — they are research context, not standalone documents.

### Route Changes

**Community Documents (Vault blueprint):**
- Routes keep the `/vault/` prefix (internal naming; UI displays "Community Documents")
- Index page: tier filter tabs visible based on user role
  - Members see: all member-tier docs
  - ARC members see: member + ARC tabs
  - Board members see: member + ARC + board tabs
- Upload form: `access_tier` dropdown replaces `is_public` checkbox
- Document detail page: tier badge displayed

**Archive blueprint:**
- All routes gated to ARC/admin role
- New route: `POST /archive/promote/<path:filepath>` — shows promote form, handles file copy + Document creation
- Existing routes unchanged otherwise

### What Stays the Same

- Archive filesystem structure (markdown + originals, `INDEX.md` catalog, category folders)
- Document versioning in Community Documents
- Semantic search / pgvector embeddings on Document model
- Append-only policy (no delete routes)
- Category system within Community Documents (`governing_documents`, `minutes`, `financial_records`, `notices`, `correspondence`, `forms`, `archive`)
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
