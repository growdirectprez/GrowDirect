# Archive System

> **Status:** Complete — written from code
> **Namespace:** cove
> **Last updated:** 2026-03-30
> **Code location:** `Cove/cove/archive/`

---

## 1. Overview

The Archive System provides read-only access to the West Portuguese Bend Community Association (WPBCA) historical document collection. It serves ARC committee members, board members, and administrators a browsable, searchable catalog of 53 indexed legal documents spanning from 1929 to the present, with underlying source files organized into a structured directory tree outside the application codebase.

The system is a document viewer, not a document store. No content is written to the database by this module. It reads markdown files and binary originals from `Cove/docs/archive/` on the filesystem, renders them as HTML, and delivers them via gated Flask routes. Separately, documents can be promoted from the archive into the live Vault (database-backed document management) as first-class `Document` records.

The archive's purpose is governance transparency and legal preparedness. It makes the community's founding documents (CC&Rs, easements, bylaws), litigation filings, chain of title, and analytical strategy accessible to the members who need them — with role-based access control and no risk of alteration.

**Key capabilities:**

- Browsable catalog parsed from `INDEX.md` with category and status filtering
- Rendered markdown viewer for narrative documents, timeline, chain of title, transcriptions, and analysis
- Binary file serving (PDF, DOCX, images) directly from the `originals/` subtree
- Semantic link rewriting: relative `.md` and binary links in source documents are converted to app routes at render time
- Path traversal prevention on all file-serving routes
- Promote-to-vault workflow: copy an archive original into the live Vault as a versioned `Document`
- KnowledgeChunk table for pgvector semantic search over the archive corpus (populated externally, queried by the agent module)

---

## 2. Architecture

### Component Diagram

```
Browser
  |
  | HTTP GET /archive/*
  v
Flask (archive_bp, prefix /archive)
  |
  +-- routes.py              # Route handlers, auth guards, arc_required decorator
  |
  +-- services.py            # All business logic: path sanitization, link rewriting,
  |                          # catalog parsing, markdown rendering
  |
  +-- forms.py               # WTForms: ArchiveSearchForm, ArchiveFilterForm,
                             #          PromoteDocumentForm

  Filesystem (read-only)
  Cove/docs/archive/
    INDEX.md                 # Master catalog (53 indexed documents)
    timeline.md              # Chronological community history
    chain-of-title.md        # Ownership succession narrative
    narrative.md             # Community history narrative
    founding/                # Markdown transcriptions (top-level category)
    governance/              # Governance markdown docs
    originals/               # Binary and extended-markdown files
      founding/              # PDFs, scanned originals
      governance/
      property/
      litigation/
      shore-club/
      transcriptions/        # Verbatim OCR/transcribed .md files
      analysis/              # Strategic analysis .md files
      templates/             # Request template .md files
      Historic/              # Historical image scans (JPG)
      city-records/          # City planning documents
      COVE-KNOWLEDGE-BASE.md # Excluded from rendering (internal)
    analysis/                # Top-level analysis subdirectory

  PostgreSQL (knowledge_chunks table)
    KnowledgeChunk           # Chunked corpus with pgvector embeddings
                             # Populated by offline ingestion pipeline
                             # Queried by cove/agent/ (not archive routes)

  Vault (cove/vault/)
    Document / DocumentVersion  # Promote target — archive originals copied here
```

### Request / Data Flow

**Catalog request:**
```
GET /archive/catalog
  → parse_catalog_entries() reads INDEX.md line by line
  → Section headings set current_category
  → Table rows parsed into entry dicts (number, title, date, status, files)
  → File cell links rewritten via _rewrite_catalog_url()
  → Filter/search applied in Python over the entry list
  → Rendered: archive/catalog.html
```

**Markdown document request:**
```
GET /archive/doc/<category>/<slug>
  → resolve_archive_path(category, slug, archive_root)
      → constructs relative path (category/slug.md or originals/transcriptions/slug.md)
      → calls sanitize_path() — rejects ".." traversal, resolves realpath, checks containment
  → File read
  → render_archive_markdown(content, is_board)
      → mistune.create_markdown(plugins=["table","strikethrough"])
      → _sanitize_html() — strips script/iframe/form/event handlers
      → rewrite_links() — _classify_link() per <a href="..."> match
  → Rendered: archive/document_view.html
```

**Binary file request:**
```
GET /archive/originals/<path:filepath>
  → sanitize_path(filepath, originals_dir) — path traversal check
  → Extension → MIME type mapping
  → send_file() with as_attachment=True for non-browser formats (DOCX, etc.)
               with as_attachment=False for PDF, JPG, PNG, TIFF (inline display)
```

**Promote-to-vault request:**
```
GET  /archive/promote/<path:filepath>  → form display, pre-filled title from filename
POST /archive/promote/<path:filepath>
  → sanitize_path() — confirms file exists and is within originals/
  → PromoteDocumentForm.validate_on_submit()
  → vault.services.upload_document(org_id, uploaded_by, filename, file_data, ...)
  → Redirect to vault.document view on success
```

### Key Design Decisions

**Filesystem, not database.** The archive is a static legal corpus. It is updated infrequently (new documents added to the directory tree, INDEX.md updated). Using the filesystem avoids a migration each time a document is added and keeps the source of truth auditable in version control or a shared volume.

**Two-tier storage.** Prose and transcriptions live as `.md` files within category subdirectories. Binary originals (PDFs, DOCX, scans) live under `originals/` and are served directly. Transcriptions of binary files live in `originals/transcriptions/`, giving each document a verbatim text companion that is renderable and searchable.

**Link rewriting at render time.** The source markdown files contain relative links (e.g., `originals/founding/1949-WPBCA-Declaration.pdf`, `originals/transcriptions/1949-Declaration-Verbatim.md`) that are valid in a local filesystem checkout. At render time, `rewrite_links()` converts these to Flask route URLs so they work in the browser without modifying the source files.

**Path sanitization as the security boundary.** No route serves a file without calling `sanitize_path()`. The function uses `os.path.realpath()` to resolve symlinks before checking containment, which defeats both `../` traversal and symlink escape attacks.

**Catalog parsed from INDEX.md.** The master catalog is a markdown table maintained by hand. `parse_catalog_entries()` parses it line by line with section heading detection, table row extraction, and URL rewriting. This means the catalog UI stays synchronized with the actual document index without any ETL process.

**Role gate: arc\_required.** All document viewing routes require the `@arc_required` decorator in addition to `@login_required`. This restricts access to ARC committee members, board members, and admins. The catalog index and top-level archive landing are login-only (no arc requirement), allowing members to see what exists without accessing content.

---

## 3. Data Model

The Archive System does not own any database tables. It reads from the filesystem and writes to the Vault (via `vault.services.upload_document`) on promote. Two database models are relevant:

### Document (`cove/models/vault.py`)

Promote target. A `Document` is created in the Vault when a board or ARC member promotes an archive original.

```python
class Document(db.Model):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String(36), primary_key=True,
                                    default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str] = mapped_column(String(36),
                                                  ForeignKey("organizations.id"),
                                                  nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    # Values: governing_documents, minutes, financial_records,
    #         notices, correspondence, forms, historical
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    access_tier: Mapped[str] = mapped_column(String(10),
                                              default=AccessTier.MEMBER.value)
    # Values: member, arc, board
    current_version: Mapped[int] = mapped_column(Integer, default=1)
    uploaded_by: Mapped[str] = mapped_column(String(36),
                                              ForeignKey("members.id"),
                                              nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow,
                                                  onupdate=datetime.utcnow)

    versions = db.relationship("DocumentVersion", backref="document",
                               order_by="DocumentVersion.version.desc()")
```

### DocumentVersion (`cove/models/vault.py`)

Each promoted document gets a first `DocumentVersion` with the binary content, MIME type, and file size. Subsequent re-uploads create additional versions with incremented `version` numbers.

```python
class DocumentVersion(db.Model):
    __tablename__ = "document_versions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True,
                                    default=lambda: str(uuid.uuid4()))
    document_id: Mapped[str] = mapped_column(String(36),
                                              ForeignKey("documents.id"),
                                              nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    filename: Mapped[str] = mapped_column(String(500), nullable=False)
    file_path: Mapped[str] = mapped_column(String(1000), nullable=False)
    # Relative path within UPLOAD_FOLDER
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)  # bytes
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    change_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    uploaded_by: Mapped[str] = mapped_column(String(36),
                                              ForeignKey("members.id"),
                                              nullable=False)
    embedding: Mapped[list | None] = mapped_column(Vector(1024), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
```

### KnowledgeChunk (`cove/models/knowledge.py`)

The semantic search corpus. Each chunk represents a granular passage from an archive document, embedded with `qwen3-embedding:8b` (1024 dimensions). The archive module does not write to this table; it is populated by a separate offline ingestion pipeline. The `agent` module queries it via cosine distance.

```python
class KnowledgeChunk(db.Model):
    __tablename__ = "knowledge_chunks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True,
                                    default=lambda: str(uuid.uuid4()))

    # Content
    content: Mapped[str] = mapped_column(Text, nullable=False)
    heading: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Provenance
    source_file: Mapped[str] = mapped_column(String(500), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    # Values: founding, governance, litigation, property, analysis,
    #         city_record, shore_club, transcription, security, narrative
    subcategory: Mapped[str | None] = mapped_column(String(100), nullable=True)
    doc_date: Mapped[str | None] = mapped_column(String(20), nullable=True)
    # Extracted from filename: "2012", "2024-08", "1949"

    # Chunk position
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    chunk_total: Mapped[int] = mapped_column(Integer, nullable=False)

    # Flexible provenance (JSONB)
    extra: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    # Stores: verbatim flag, original filename, recording instrument numbers,
    #         APN references, legal citations, etc.

    # Embedding
    embedding: Mapped[list | None] = mapped_column(Vector(1024), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow,
                                                  onupdate=datetime.utcnow)
```

**Similarity query pattern:**

```python
from cove.models.knowledge import KnowledgeChunk
from sqlalchemy import text

chunks = db.session.execute(
    text("SELECT * FROM knowledge_chunks ORDER BY embedding <=> :q LIMIT :k"),
    {"q": str(query_vector), "k": 10}
).fetchall()
```

### Filesystem Layout

The archive root is resolved at runtime:

```python
os.path.join(current_app.root_path, "..", "docs", "archive")
# resolves to: Cove/docs/archive/
```

Key paths within the archive root:

| Path | Contents |
|------|----------|
| `INDEX.md` | Master catalog — 53 indexed documents as of 2026-03-25 |
| `timeline.md` | Chronological community history |
| `chain-of-title.md` | Ownership succession narrative |
| `narrative.md` | Community history narrative |
| `founding/*.md` | Markdown docs in the founding category |
| `governance/*.md` | Governance markdown docs |
| `originals/founding/` | Founding PDFs and OCR versions |
| `originals/governance/` | Governance PDFs and Word docs |
| `originals/property/` | Property records, title reports |
| `originals/litigation/` | Court filings, FPPC complaint |
| `originals/shore-club/` | Shore Club historical documents |
| `originals/transcriptions/` | Verbatim .md transcriptions of binary files |
| `originals/analysis/` | Strategic analysis .md files |
| `originals/templates/` | CPRA and records request templates |
| `originals/Historic/` | Historical image scans (JPG) |
| `originals/city-records/` | RPV planning documents |
| `originals/COVE-KNOWLEDGE-BASE.md` | Internal reference — excluded from rendering |
| `stubs.md` | Internal tracking — excluded from rendering |

---

## 4. Interfaces

### Blueprint Registration

```python
archive_bp = Blueprint("archive", __name__, template_folder="templates")
# Registered in cove/__init__.py at prefix /archive
```

### Routes

| Method | URL | Auth | Description |
|--------|-----|------|-------------|
| GET | `/archive/` | login\_required | Landing page |
| GET | `/archive/timeline` | login\_required | Community timeline (timeline.md) |
| GET | `/archive/chain` | login\_required | Chain of title (chain-of-title.md) |
| GET | `/archive/bylaws` | login\_required | Governance documents index (lists governance/*.md files) |
| GET | `/archive/catalog` | login\_required | Full catalog with filter and search |
| GET | `/archive/doc/<category>/<slug>` | login\_required + arc\_required | Rendered markdown document viewer |
| GET | `/archive/data/<filename>` | login\_required + arc\_required | Data file download (CSV, JSON, GeoJSON, TSV) |
| GET | `/archive/originals/<path:filepath>` | login\_required + arc\_required | Binary file server (PDF, DOCX, images) |
| POST | `/archive/request/<path:filepath>` | login\_required + arc\_required | Log request for physical document |
| GET | `/archive/promote/<path:filepath>` | login\_required + arc\_required | Promote-to-vault form |
| POST | `/archive/promote/<path:filepath>` | login\_required + arc\_required | Promote-to-vault submission |

### Access Tiers

The `arc_required` decorator enforces the higher access gate:

```python
def arc_required(f):
    """Restrict route to ARC, board, or admin members."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not (current_user.is_arc or current_user.is_board or current_user.is_admin):
            abort(403)
        return f(*args, **kwargs)
    return decorated
```

- `login_required` only: catalog, timeline, chain, bylaws index — members can see what exists
- `login_required` + `arc_required`: document viewing, binary files, data files, promote — ARC/board/admin only

### Forms

**ArchiveSearchForm** — full-text search over catalog entries

| Field | Type | Validation |
|-------|------|------------|
| `q` | StringField | Optional, max 200 chars |

**ArchiveFilterForm** — catalog filter by category and status

| Field | Type | Validation | Notes |
|-------|------|------------|-------|
| `category` | SelectField | Optional | Choices populated at runtime from `parse_catalog_entries()` |
| `status` | SelectField | Optional | Choices: active, historical, superseded, draft, filed, pending |

**PromoteDocumentForm** — promote archive original to vault

| Field | Type | Validation | Notes |
|-------|------|------------|-------|
| `title` | StringField | Required, 2-500 chars | Pre-filled from filename |
| `category` | SelectField | Required | Choices from `vault.services.CATEGORIES` |
| `access_tier` | SelectField | Required | Filtered by user's max tier at runtime |
| `description` | TextAreaField | Optional, max 2000 chars | |

All forms inherit from `CoveForm` (extends `FlaskForm`), which provides CSRF automatically.

---

## 5. Service Layer

All business logic lives in `Cove/cove/archive/services.py`. Routes call service functions; no business logic lives in route handlers.

### `sanitize_path(relative: str, base_dir: str) -> str | None`

The core security function used by every file-serving route.

**Algorithm:**
1. Reject immediately if `".."` appears anywhere in the relative path string.
2. Construct candidate path: `os.path.join(base_dir, relative)`.
3. Resolve to absolute path with `os.path.realpath()` — this resolves symlinks and normalizes the path.
4. Check containment: the resolved path must start with `os.path.realpath(base_dir) + os.sep` (or equal the base dir itself).
5. Check existence: `os.path.isfile(resolved)` must be true.
6. Return resolved absolute path on success, `None` on any failure.

The use of `os.path.realpath()` before the containment check is critical: it defeats symlink attacks where a file within the base directory points outside it.

### `resolve_archive_path(category: str, slug: str, archive_root: str) -> str | None`

Maps a `(category, slug)` URL pair to a filesystem path, handling three location patterns:

| Input | Resolved path |
|-------|---------------|
| `category=""`, `slug="narrative"` | `archive_root/narrative.md` |
| `category="founding"`, `slug="1949-declaration"` | `archive_root/founding/1949-declaration.md` |
| `category="transcriptions"`, `slug="1949-Verbatim"` | `archive_root/originals/transcriptions/1949-Verbatim.md` |

Files in `EXCLUDED_FILES` (`stubs.md`, `COVE-KNOWLEDGE-BASE.md`) return `None` regardless of path. After constructing the relative path, delegates to `sanitize_path()` for all security checks.

### `_classify_link(href: str) -> tuple[str, str]`

Classifies a single link `href` extracted from rendered HTML and returns a `(link_type, rewritten_url)` tuple. Called per-match by `rewrite_links()`.

| href pattern | link\_type | rewritten\_url |
|---|---|---|
| `http://...`, `https://...`, `mailto:...`, `#...` | `external` | original href |
| Starts with `..` | `out_of_tree` | `""` |
| Extension in `_ORIGINAL_EXTENSIONS` | `original` | `/archive/originals/<path>` |
| `originals/transcriptions/X.md` | `doc` | `/archive/doc/transcriptions/X` |
| `category/X.md` (two-part) | `doc` | `/archive/doc/category/X` |
| `X.md` (top-level) | `doc` | `/archive/doc/X` |
| All other | `external` | original href |

`_ORIGINAL_EXTENSIONS = {".pdf", ".docx", ".doc", ".jpg", ".jpeg", ".png", ".tiff", ".tif"}`

If the href already starts with `originals/`, it is preserved. If it is a bare binary filename, `originals/` is prepended before constructing the route URL.

### `rewrite_links(html: str, is_board: bool) -> str`

Post-processes rendered HTML to convert all `<a href="...">` tags. Uses `_LINK_RE = re.compile(r'<a\s+href="([^"]*)"', re.IGNORECASE)` to find matches.

- `original` and `doc` links: `href` attribute replaced with the rewritten URL.
- `out_of_tree` links: the `<a>` tag is replaced with `<span class="text-cove-600">`, and a second-pass regex closes the span, discarding the `</a>` closer. The link text is preserved; only the anchor is removed.
- `external` links: left unchanged.

The `is_board` parameter is accepted for future board-only content filtering but is not currently used in the replacement logic.

### `_rewrite_catalog_url(url: str) -> str`

Used by catalog parsing (not by the markdown renderer). Handles the same URL patterns as `_classify_link` but is applied to raw URLs extracted from INDEX.md table cells before HTML rendering occurs.

Special case: out-of-tree relative paths (e.g., `../../data/wpbca-parcels-seed.csv`) are converted to `/archive/data/<filename>` by extracting the final meaningful path component.

### `render_archive_markdown(content: str, is_board: bool) -> str`

Full rendering pipeline for a markdown document:

1. `mistune.create_markdown(plugins=["table", "strikethrough"])` — renders markdown to HTML with table and strikethrough support.
2. `_sanitize_html(html)` — strips `<script>`, `<iframe>`, `<object>`, `<embed>`, `<form>` tags and all `on*` event handler attributes using regex.
3. `rewrite_links(html, is_board)` — rewrites all relative links to app routes.

Returns the final HTML string for template rendering.

### `parse_catalog_entries() -> tuple[list[dict], list[str]]`

Parses `INDEX.md` into a list of entry dicts and a list of category names. State machine over lines:

1. `## Heading` lines: extract category name via `_SECTION_CATEGORY_MAP`. Skip `"Documents Still Needed"` and `"Request Templates"` sections.
2. Table separator rows (`|---|---|`): set `in_table = True`.
3. Header rows (first cell is `"#"`): capture column names.
4. Data rows: map cells to column names, extract standard fields, call `_parse_file_links()` on the File cell.

Entry dict shape:

```python
{
    "number": str,           # "#" column
    "title": str,            # "Document" column, bold markers stripped
    "date": str,             # "Date" column
    "recording_info": str,   # "Recording Info" or "Purpose" column
    "status": str,           # "Status" column
    "category": str,         # Mapped from section heading
    "files": list[dict],     # [{"label": str, "url": str}, ...]
    "status_class": str,     # active | historical | superseded | draft | filed | pending
}
```

### `classify_status(status: str) -> str`

Maps a raw status string to a badge class:

| Keywords in status | Badge class |
|--------------------|-------------|
| "in force", "current", "active" | `active` |
| "superseded" | `superseded` |
| "draft" | `draft` |
| "pending" | `pending` |
| "filed", "served" | `filed` |
| (default) | `historical` |

### `_sanitize_html(html: str) -> str`

Strips dangerous HTML constructs from mistune-rendered output:

- Removes `<script>`, `<iframe>`, `<object>`, `<embed>`, `<form>` tags and their full content (including nested content, using `re.DOTALL`).
- Removes self-closing variants of the same tags.
- Strips all `on*` event handler attributes (both quoted and unquoted forms).

---

## 6. Configuration

The archive module requires no dedicated configuration keys beyond what the base app provides.

**Runtime paths** are constructed relative to `current_app.root_path`:

```python
archive_root = os.path.join(current_app.root_path, "..", "docs", "archive")
# current_app.root_path = Cove/cove/
# archive_root          = Cove/docs/archive/
```

**Vault promote** reads `UPLOAD_FOLDER` from app config (default `"uploads"`) — passed through to `vault.services.upload_document`.

**No environment variables** are specific to this module. Access control relies on `Member.is_arc`, `Member.is_board`, and `Member.is_admin` properties set by the auth and member modules.

**EXCLUDED_FILES** is a module-level constant:

```python
EXCLUDED_FILES = {"stubs.md", "COVE-KNOWLEDGE-BASE.md"}
```

Adding files to this set prevents them from being served via any archive route, regardless of whether a URL can be constructed for them.

---

## 7. Security & Compliance

### Path Traversal Prevention

Every file-serving route passes user-controlled path components through `sanitize_path()` before any file operation. The function provides three layers of defense:

1. **String check:** `".."` anywhere in the relative path string is rejected before any filesystem call. This stops the most common traversal patterns at zero cost.
2. **Realpath resolution:** `os.path.realpath()` resolves both `../` sequences and symlinks. A symlink within `originals/` pointing to `/etc/passwd` would be resolved to its target before the containment check, causing it to fail.
3. **Prefix containment:** The resolved absolute path must start with `os.path.realpath(base_dir) + os.sep`. The trailing `os.sep` prevents a base dir of `/foo/bar` from matching a file at `/foo/bar-sensitive`.

Routes enforce their own base directories:
- `document()` and `resolve_archive_path()`: base is `archive_root`
- `originals()` and `promote_form/submit()`: base is `archive_root/originals/`
- `data_file()`: base is `archive_root`; additionally enforces an explicit extension allowlist (`{".csv", ".json", ".geojson", ".tsv"}`)

### Upload Validation (Promote Workflow)

The promote workflow reads a file from the archive (already sanitized) rather than accepting an upload from the browser. The security boundary is `sanitize_path()` confirming the source file is within `originals/`. The vault's `upload_document` service handles MIME type detection and storage on receipt.

### HTML Sanitization

Markdown source files may contain embedded HTML. The `_sanitize_html()` function strips executable content (`<script>`, `<iframe>`, event handlers) before the rendered HTML reaches the template. This prevents stored XSS if a source document were modified to contain malicious markup.

### Role Gating

- **Catalog and top-level pages:** `@login_required` — authenticated members can see what documents exist, not their content.
- **Document content, binary files, data files:** `@login_required` + `@arc_required` — restricted to ARC committee, board, and admin.
- **Promote:** same `@arc_required` gate; the promote form additionally filters available `access_tier` choices to tiers at or below the promoting user's own maximum tier, preventing privilege escalation on promoted documents.

### CSRF

All forms inherit from `CoveForm` (`FlaskForm`), which enables CSRF by default via the `csrf = CSRFProtect()` extension. The catalog search and filter forms are submitted as GET requests and use `meta={"csrf": False}` since they carry no state-changing data.

---

## 8. Error Handling

| Condition | Response |
|-----------|----------|
| Path traversal detected by `sanitize_path()` | `None` returned → `abort(404)` in route |
| File not found (sanitize\_path returns None) | `abort(404)` |
| File is in `EXCLUDED_FILES` | `abort(404)` via `resolve_archive_path` returning None |
| `data_file` extension not in allowlist | `abort(403)` |
| User lacks ARC/board/admin role | `abort(403)` via `arc_required` decorator |
| `PromoteDocumentForm` validation failure | Re-render form with inline errors (no redirect) |
| `vault.services.upload_document` returns None | Flash error, re-render promote form |
| `INDEX.md` not present | `parse_catalog_entries()` returns `([], [])` — catalog renders empty |
| Timeline or chain-of-title `.md` not found | `sanitize_path` returns None → `abort(404)` |

There is no custom error page at the archive blueprint level. HTTP 403 and 404 are handled by Cove's global error handlers.

The request-original route (`/archive/request/<path:filepath>`) does not validate whether the requested file exists — it logs a flash message and redirects. This is intentional: the route covers physical documents that may not have digital counterparts.

---

## 9. Testing

The archive module has no dedicated test file as of this writing. The following test surface is required for full coverage:

### Unit Tests (services)

- `sanitize_path`: valid path returns resolved absolute path; `..` in path returns None; symlink escaping base dir returns None; non-existent file returns None.
- `resolve_archive_path`: category/slug maps to correct path; transcriptions category maps to `originals/transcriptions/`; excluded filenames return None.
- `_classify_link`: all link type branches (external, out\_of\_tree, original binary, markdown doc, transcription, top-level).
- `rewrite_links`: out-of-tree links produce `<span>` with text preserved; original links get `/archive/originals/` prefix; doc links get `/archive/doc/` prefix.
- `classify_status`: all keyword branches map to expected badge classes.
- `parse_catalog_entries`: parses a known INDEX.md fixture to correct entry count, category list, file links; skips "Documents Still Needed" section; handles table header variations.
- `_sanitize_html`: script tags and content removed; iframe removed; on* attributes stripped.

### Integration Tests (routes)

- `GET /archive/` — 200 for authenticated member.
- `GET /archive/catalog` — 200 with entries populated; category filter returns subset; status filter returns subset; query filter matches title.
- `GET /archive/doc/founding/<valid-slug>` — 200 for ARC user; 403 for member-only user.
- `GET /archive/doc/<category>/<slug>` with traversal slug — 404.
- `GET /archive/originals/<valid-pdf>` — 200, `application/pdf` content type, `Content-Disposition: inline`.
- `GET /archive/originals/<valid-docx>` — 200, DOCX MIME type, `Content-Disposition: attachment`.
- `GET /archive/data/<valid-csv>` — 200, file sent as attachment.
- `GET /archive/data/<filename>.exe` — 403.
- `GET /archive/promote/<valid-path>` — 200, form pre-populated.
- `POST /archive/promote/<valid-path>` with valid form — redirects to vault document view; document exists in DB.
- `POST /archive/promote/<valid-path>` with invalid form — re-renders form with errors.

### Fixtures Required

- Temporary archive root with known directory structure (founding/, originals/transcriptions/, INDEX.md stub).
- ARC user fixture and member-only user fixture.
- Sample PDF binary in originals/ for promote tests.

---

## 10. Dependencies

### Upstream

| Dependency | Role |
|------------|------|
| `flask_login.current_user` | Auth check in `arc_required` and all routes |
| `cove.vault.services.upload_document` | Promote workflow — creates Document + DocumentVersion in vault |
| `cove.vault.services.get_user_max_tier` | Promote workflow — restricts available access\_tier choices |
| `cove.vault.services.TIER_HIERARCHY` | Promote workflow — maps user max tier to allowed tier set |
| `cove.vault.services.CATEGORIES` | `PromoteDocumentForm.category` choices |
| `cove.forms.CoveForm` | Base class for all archive forms |
| `mistune` | Markdown → HTML rendering (Python package) |
| `Cove/docs/archive/` (filesystem) | Source of all rendered and served content |

### Downstream

| Consumer | Usage |
|----------|-------|
| `cove/agent/` | Queries `knowledge_chunks` table populated from the archive corpus |
| `cove/vault/` | Receives promoted documents via `upload_document` |
| `Cove/cove/mcp/server.py` | MCP Knowledge Server — exposes `knowledge_ingest_document`, `knowledge_add_chunk`, and search tools over stdio. Uses `growdirect-mcp` platform package (`GrowDirectRegistry`, `GrowDirectTool`). See `docs/sdds/alx/mcp-service-layer.md`. |

### Shared Infrastructure

| Service | Usage |
|---------|-------|
| `growdirect_postgres` | `knowledge_chunks` table (pgvector); `documents`/`document_versions` tables (vault) |
| Filesystem volume | `Cove/docs/archive/` mounted in the Flask container for document serving |

The archive module itself makes no network calls and no database queries. All I/O is filesystem reads and writes (the latter only via vault services on promote).

---

## 11. Known Issues & Reconciliation

**INDEX.md count discrepancy.** The stub described "528 docs" but the current INDEX.md header reads "53 documents" as of 2026-03-25. The 528 figure likely referred to the total number of `KnowledgeChunk` rows in the knowledge base rather than the number of indexed legal documents. No code depends on either count.

**`is_board` parameter unused in link rewriting.** `render_archive_markdown` and `rewrite_links` both accept `is_board: bool` and pass it through, but the current implementation does not gate any content on it. The parameter is a hook for future board-only redaction of specific link targets (e.g., strategy documents visible only to board members). No work is required; the signature is stable.

**`request_original` route is a stub.** `POST /archive/request/<path:filepath>` logs a flash message and redirects but creates no database record. A physical document request model (tracking requestor, document reference, status, board follow-up) was deferred to a future issue. The current behavior is documented and intentional for MVP.

**String(36) UUIDs.** `Document` and `DocumentVersion` use `String(36)` primary keys (formatted UUID strings) rather than the platform standard `Mapped[uuid.UUID]`. This is a Cove-wide historical pattern, not specific to the archive module. New tables should use native UUID. Do not propagate this pattern.

**No pagination on catalog.** `parse_catalog_entries()` loads all entries into Python memory and filters in-process. At 53 current entries this is negligible. If the catalog grows significantly, server-side pagination should be added to the route before the filter/search pass.

**KnowledgeChunk ingestion pipeline not in this module.** The `knowledge_chunks` table is populated by an offline script (not part of `cove/archive/`). If the archive corpus changes significantly, the ingestion pipeline must be re-run manually to keep embeddings current. No automated sync exists.

**`stubs.md` and `COVE-KNOWLEDGE-BASE.md` exclusion is string-matched, not path-matched.** `EXCLUDED_FILES` contains bare filenames. If these files were placed in a subdirectory, they would not be excluded because `resolve_archive_path` constructs a `filename` of `"{slug}.md"` and checks it against the set. Files with these exact slugs placed in subdirectories would be accessible. This is an acceptable limitation given the controlled directory structure.
