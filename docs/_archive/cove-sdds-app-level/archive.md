# SDD: Archive

**Status:** Active
**Last updated:** 2026-03-29

**Wiki:** [[Brain/wiki/cove-governance|Cove Governance]]

## Overview

Filesystem-based document archive for community history. Markdown files in `docs/archive/` are rendered on request using `mistune`. No owned database tables — only the `request_original` route writes to DB (audit log). The `/archive/catalog` route merges archive entries with live vault documents.

Blueprint: `archive_bp` at `/archive`. Services in `cove/archive/services.py`.

## Routes

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/archive/` | login | Landing page with cards linking to timeline, chain, catalog, bylaws |
| GET | `/archive/timeline` | login | Renders `docs/archive/timeline.md` via `document_view.html` |
| GET | `/archive/chain` | login | Renders `docs/archive/chain-of-title.md` via `document_view.html` |
| GET | `/archive/bylaws` | login | Governance documents section |
| GET | `/archive/catalog` | login | Parses `INDEX.md` + merges live vault docs; filterable table with category choices from `_SECTION_CATEGORY_MAP` |
| GET | `/archive/doc/<category>/<slug>` | login | Individual document viewer; checks for matching original file |
| GET | `/archive/data/<filename>` | login | Serve `.csv`, `.json`, `.geojson` from `data/` directory |
| GET | `/archive/originals/<path:filepath>` | login | Serve PDF/image originals; extension-allowlisted |
| POST | `/archive/request/<path:filepath>` | login | Flash confirmation message to user (audit log write not yet implemented) |
| GET | `/archive/promote/<path:filepath>` | `arc_required` | Show promote-to-vault form |
| POST | `/archive/promote/<path:filepath>` | `arc_required` | Copy archive file to Community Documents vault |

All paths pass through `sanitize_path` before `send_file`. Transcriptions resolve under `originals/transcriptions/`. Files in `EXCLUDED_FILES` (`stubs.md`, `COVE-KNOWLEDGE-BASE.md`) return 404.

## Filesystem Layout

| Path | Contents |
|------|----------|
| `docs/archive/narrative.md` | Community story entry point |
| `docs/archive/timeline.md` | Chronological community history |
| `docs/archive/chain-of-title.md` | Property ownership chain |
| `docs/archive/INDEX.md` | Master catalog table (parsed at request time) |
| `docs/archive/{founding,governance,...}/` | Category markdown files |
| `docs/archive/originals/` | PDFs, images, transcription `.md` files |

## Models Used (no owned tables)

- `Member` + `MemberRole` — queried for `arc_required` decorator checks
- Note: `request_original` currently only flashes a message; audit log write is planned but not yet implemented

## Services (`cove/archive/services.py`)

| Function | What it does |
|----------|--------------|
| `sanitize_path(relative, base_dir)` | Rejects `..` traversal and symlink escapes; returns resolved absolute path or `None` |
| `resolve_archive_path(category, slug, root)` | Maps category+slug to `.md` filepath; handles transcriptions sub-path; returns `None` for excluded files |
| `render_archive_markdown(content, is_board)` | Renders markdown with `mistune` (table + strikethrough plugins), then calls `rewrite_links` |
| `rewrite_links(html, is_board)` | Rewrites relative hrefs: `.md` → `/archive/doc/...`, binary files → `/archive/originals/...`, out-of-tree → stripped to `<span>` |
| `parse_catalog_entries()` | Parses `INDEX.md` markdown tables by section heading; returns `(entries, categories)`. Each entry: `{number, title, date, recording_info, status, category, files, status_class}` |
| `classify_status(status)` | Returns badge class: `active`, `historical`, `superseded`, `draft`, `filed`, or `pending` |

`_classify_link` and `_rewrite_catalog_url` are internal helpers for link rewriting and catalog URL normalization.

Catalog section headings map to categories via `_SECTION_CATEGORY_MAP`. "Documents Still Needed" and "Request Templates" sections are skipped.

## Forms

| Form | File | Fields |
|------|------|--------|
| `ArchiveFilterForm` | `cove/archive/forms.py` | Category select, search text |
| `ArchiveSearchForm` | `cove/archive/forms.py` | Search query field |
| `PromoteDocumentForm` | `cove/archive/forms.py` | Title, category, description for vault promotion |

## Templates

Templates are blueprint-local in `cove/archive/templates/archive/`:

| Template | Notes |
|----------|-------|
| `index.html` | Landing page with cards linking to timeline, chain, catalog, bylaws |
| `document_view.html` | Shared viewer used by timeline, chain, and individual documents; renders `content` HTML; inline PDF viewer if `original_path` set |
| `catalog.html` | Filterable table; Alpine.js category filter; status badges; file links |
| `bylaws.html` | Governance documents section |
| `promote.html` | Form for promoting archive documents to vault |
