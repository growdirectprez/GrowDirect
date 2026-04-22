# Archive System

**Status:** Active
**Type:** App Service
**Last updated:** 2026-04-13
**Blueprint:** `archive_bp` at `/archive`
**Code location:** `Cove/cove/archive/`
**Wiki:** [[Brain/wiki/cove-governance|Cove Governance]] | [[Brain/wiki/cove-legal-framework|Cove Legal Framework]] | [[Brain/wiki/cove-community-history|Cove Community History]]
**Architecture:** [[docs/sdds/cove/architecture|Cove Architecture]]
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[docs/team/Writer|Writer]] · **Operator role:** [[docs/team/ALX|ALX]]

---

## Purpose

Read-only access to the WPBCA historical document collection. Serves a browsable, searchable catalog of 53+ indexed legal documents spanning 1929 to present, rendered from markdown source files and binary originals on the filesystem. Includes a promote-to-vault workflow for archiving originals into the live document management system. The archive is a document viewer, not a document store -- no content is written to the database by this module.

---

## Dependencies

| Dependency | Role | Required |
|------------|------|----------|
| Filesystem (`Cove/docs/archive/`) | Source of all served content | Yes |
| `mistune` (Python package) | Markdown-to-HTML rendering | Yes |
| `cove.vault.services.upload_document` | Promote workflow target | Yes |
| `cove.vault.services.get_user_max_tier` | Tier filtering for promote form | Yes |
| PostgreSQL | Not used directly by archive routes (knowledge_chunks queried by agent) | No |

---

## Data Flow & PII Map

### What enters
- HTTP requests with user-controlled path segments (category, slug, filepath)
- Promote form submissions (title, category, access_tier, description)

### What's stored
**Nothing in the database.** Archive reads from filesystem only. Promoted documents go to Vault (see vault SDD).

### What exits
- Rendered HTML from markdown source files
- Binary file downloads (PDF, DOCX, images)
- Data file downloads (CSV, JSON, GeoJSON, TSV)
- Promoted documents (to Vault via `upload_document`)

### PII Classification
**Low PII risk.** Archive content is legal documents, governance records, and historical materials. Some documents may reference property owners by name (public record). No member PII is collected, stored, or transmitted by this module.

---

## API Contract

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/archive/` | `login_required` + ARC gate | Landing page |
| GET | `/archive/timeline` | `login_required` + ARC gate | Community timeline |
| GET | `/archive/chain` | `login_required` + ARC gate | Chain of title |
| GET | `/archive/bylaws` | `login_required` + ARC gate | Governance documents index |
| GET | `/archive/catalog` | `login_required` + ARC gate | Full catalog with filter and search |
| GET | `/archive/doc/<category>/<slug>` | `login_required` + ARC gate | Rendered markdown viewer |
| GET | `/archive/data/<filename>` | `login_required` + ARC gate | Data file download (CSV/JSON/GeoJSON/TSV only) |
| GET | `/archive/originals/<path:filepath>` | `login_required` + ARC gate | Binary file server |
| POST | `/archive/request/<path:filepath>` | `login_required` + ARC gate | Log request for physical document |
| GET/POST | `/archive/promote/<path:filepath>` | `login_required` + ARC gate | Promote to vault |

### Access Control

The ARC gate is a `before_request` hook registered on the archive blueprint in `cove/__init__.py`. It requires `current_user.is_arc` (which includes board and admin). Non-ARC authenticated members receive 403.

---

## Security: Path Traversal Prevention

**`sanitize_path(relative, base_dir)`** -- the core security boundary. Every file-serving route passes user-controlled path segments through this function.

Three layers of defense:
1. **String check**: Rejects `".."` anywhere in the path
2. **Realpath resolution**: `os.path.realpath()` resolves symlinks before containment check
3. **Prefix containment**: Resolved path must start with `realpath(base_dir) + os.sep`

Routes enforce their own base directories:
- `doc` routes: base is `archive_root`
- `originals` routes: base is `archive_root/originals/`
- `data` routes: base is `archive_root` + extension allowlist (`{.csv, .json, .geojson, .tsv}`)

### HTML Sanitization

`_sanitize_html()` strips `<script>`, `<iframe>`, `<object>`, `<embed>`, `<form>` tags and all `on*` event handlers from markdown-rendered HTML. Prevents stored XSS from modified source files.

### Link Rewriting

`rewrite_links()` converts relative filesystem links in markdown to Flask route URLs at render time. Out-of-tree links are converted to `<span>` elements (link disabled, text preserved).

---

## Operations

### Startup
No module-specific startup. Archive root resolved at runtime: `os.path.join(current_app.root_path, "..", "docs", "archive")`.

### Health Checks
No module-specific health check. Failure mode: if archive directory is missing, catalog returns empty; document routes return 404.

### Failure Modes

| Failure | Impact | Recovery |
|---------|--------|----------|
| Archive directory missing/empty | Catalog empty, all doc routes 404 | Mount/restore archive volume |
| INDEX.md missing | Catalog renders empty | Restore INDEX.md |
| Source markdown malformed | Rendering may produce empty or broken HTML | Fix source file |
| Symlink escape attempt | `sanitize_path` rejects via realpath check | Logged; no action needed |

### Configuration
No module-specific env vars. Uses `UPLOAD_FOLDER` for promote workflow.

`EXCLUDED_FILES = {"stubs.md", "COVE-KNOWLEDGE-BASE.md"}` -- bare filename exclusion list.

---

## Deployment

- **Docker**: Archive directory mounted as volume (`../docs/archive:/app/docs/archive:ro`)
- **AWS**: Archive content on EFS (read-only mount for Flask; read-write for content updates)
- **CI/CD**: Archive updates deployed as volume content, not code changes

---

## Code Review Findings

| # | Severity | Finding | Recommended Fix |
|---|----------|---------|----------------|
| 1 | **P1** | `request_original` route is a stub -- logs flash message but creates no database record | Implement physical document request model or remove route |
| 2 | **P1** | `EXCLUDED_FILES` uses bare filenames, not full paths -- same filename in subdirectory would not be excluded | Use full path matching or path-aware exclusion |
| 3 | **P1** | No audit trail for document access, file downloads, or promote actions | Add audit logging for all archive access |
| 4 | **P2** | No pagination on catalog (all entries loaded into memory) | Add server-side pagination at ~100+ entries |
| 5 | **P2** | `is_board` parameter accepted by `render_archive_markdown` and `rewrite_links` but unused | Remove or implement board-only content filtering |
| 6 | **P2** | No automated sync between archive filesystem and `knowledge_chunks` table | Add file watcher or post-update hook to trigger re-seeding |
| 7 | **P2** | INDEX.md count discrepancy ("53 documents" header vs actual count may drift) | Auto-generate count from parsed entries |

---

## Production Readiness Checklist

- [x] No PII stored (filesystem read-only, legal documents)
- [ ] Secrets in AWS Secrets Manager
- [x] Path traversal prevention on all file-serving routes (sanitize_path)
- [x] HTML sanitization on rendered markdown (_sanitize_html)
- [ ] Audit logging for archive access
- [x] Role gating (ARC/board/admin required for document content)
- [x] Error responses don't leak internals (404 on path validation failure)
- [x] CSRF protection on promote form (via CoveForm)
- [ ] Physical document request workflow implemented
- [ ] Archive filesystem backup strategy defined
