# SDD: Knowledge Module

**Status:** Active
**Last updated:** 2026-03-29
**Model:** `cove/models/knowledge.py`
**Service:** `cove/services/embedding.py`
**Seed script:** `seed_knowledge.py`

---

## Overview

Granular legal document knowledge base with pgvector embeddings for semantic search. Stores verbatim text chunks from the Cove archive (CC&Rs, bylaws, litigation filings, title reports, city records, historical corporate documents) with full provenance metadata. Designed for precise retrieval of exact legal language, not summarization.

---

## Model

**KnowledgeChunk** (`knowledge_chunks` table) -- `cove/models/knowledge.py`

| Column | Type | Description |
|--------|------|-------------|
| `id` | `String(36)`, PK | UUID, auto-generated |
| `content` | `Text` | Verbatim chunk text (target ~1500 chars) |
| `heading` | `String(500)`, nullable | Section heading hierarchy (e.g., `"Section 5 > Voting Rights"`) |
| `source_file` | `String(500)` | Relative path to the source `.md` file |
| `category` | `String(100)` | Document category (see category list below) |
| `subcategory` | `String(100)`, nullable | Subcategory (primarily for `city_record`: ceqa, builder_remedy, etc.) |
| `doc_date` | `String(20)`, nullable | Date extracted from filename (e.g., `"2012"`, `"2024-08"`, `"1949"`) |
| `chunk_index` | `Integer` | Zero-based position of this chunk within the source document |
| `chunk_total` | `Integer` | Total number of chunks from the source document |
| `extra` | `JSONB`, nullable | Flexible provenance metadata (see below) |
| `embedding` | `Vector(1024)`, nullable | pgvector embedding (qwen3-embedding:8b, cosine distance) |
| `created_at` | `DateTime` | Creation timestamp |
| `updated_at` | `DateTime` | Last update timestamp (auto-updated) |

### Extra JSONB Fields

The `extra` column stores provenance data extracted during chunking:

| Key | Type | Description |
|-----|------|-------------|
| `verbatim` | `bool` | `true` if source filename contains "Verbatim" |
| `apn_refs` | `list[str]` | APN references found in chunk text (pattern: `NNNN-NNN-NNN`) |
| `instrument_refs` | `list[str]` | Recording instrument/document numbers |
| `legal_citations` | `list[str]` | Civil Code, Corp. Code, Gov. Code section references |

---

## Categories

| Category | Source Path | Description |
|----------|------------|-------------|
| `founding` | `docs/archive/founding/` | CC&Rs, declarations, easements (1949-1952) |
| `governance` | `docs/archive/governance/` | Bylaws, restated declarations |
| `litigation` | `docs/archive/litigation/` | Complaints, demurrers, petitions, summons |
| `property` | `docs/archive/property/` | Title reports, easements, assessor maps, EIR geology |
| `analysis` | `docs/archive/analysis/` | Legal briefs, risk assessments, research |
| `city_record` | `docs/archive/originals/city-records/` | City records with subcategories (ceqa, builder_remedy, general_plan, hcd, coastal_commission, council_staff_report, public_correspondence) |
| `shore_club` | `docs/archive/shore-club/` | Historical Abalone Shore Club corporate records (1929-1972) |
| `transcription` | `docs/archive/originals/transcriptions/` | Verbatim legal document transcriptions |
| `security` | `docs/security/` | Security policies and procedures |
| `narrative` | `docs/archive/*.md` (top-level) | Timeline, chain-of-title, narrative, INDEX, stubs |
| `template` | `docs/archive/originals/templates/` | CPRA requests, recorder requests, search templates |

---

## Embedding Service

**`cove/services/embedding.py`**

| Function | Signature | Description |
|----------|-----------|-------------|
| `generate_embedding` | `(text: str) -> list[float] \| None` | Generate a 1024-dim vector via Ollama HTTP API. Returns `None` if Ollama is unreachable. |

Configuration:
- **Service:** Ollama at `OLLAMA_URL` (default: `http://localhost:11434`, Docker: `http://growdirect_ollama:11434`)
- **Model:** `qwen3-embedding:8b` -- 1024 dimensions (Matryoshka truncated from native 4096d)
- **API endpoint:** `POST /api/embed`
- **Text truncation:** Input capped at 6000 chars to stay within model context window
- **Timeout:** 15 seconds
- **Failure mode:** Returns `None` gracefully, logs at DEBUG level. Callers must handle `None`.

### Similarity Search Pattern

Cosine distance via pgvector `<=>` operator:

```sql
SELECT id, content, heading, source_file
FROM knowledge_chunks
ORDER BY embedding <=> :query_vector
LIMIT 10;
```

---

## Seed Script

**`seed_knowledge.py`** -- standalone CLI script (runs inside Docker container or from host via `docker exec`).

### Usage

```bash
# Inside container
python3 seed_knowledge.py [--dry-run] [--no-embed] [--verbose]

# From host
docker exec cove_flask python3 seed_knowledge.py --dry-run
```

### File Discovery

- Scans `docs/archive/` and `docs/security/` recursively for `.md` files (excludes `README.md`)
- Files sorted by path for deterministic ordering

### Chunking Strategy

1. **Split on `##` headings** -- major document sections
2. **Split on `###` sub-headings** -- within sections
3. **Split on `####` sub-sub-headings** -- within sub-sections
4. **Split on paragraph boundaries** (double newline) -- within sub-sub-sections
5. **Last resort: split on sentence boundaries** -- never splits mid-sentence

Constraints:
- **Target chunk size:** ~1500 chars (`MAX_CHUNK_CHARS`)
- **Minimum viable chunk:** 50 chars (`MIN_CHUNK_CHARS`) -- smaller fragments are discarded
- **Never splits mid-paragraph** -- legal language must stay intact

### Provenance Extraction

During chunking, the script extracts structured metadata into the `extra` JSONB column:
- **APN references:** Regex `\b\d{4}-\d{3}-\d{3}\b`
- **Recording instrument numbers:** Regex for "Instrument No." / "Document No." patterns
- **Legal citations:** Civil Code, Corp. Code, Gov. Code section references

### Embedding Generation

- Each chunk is embedded with a provenance prefix: `[category] heading:\ncontent`
- Uses Ollama HTTP API (same model as the embedding service)
- Text truncated to 6000 chars before embedding
- Timeout: 30 seconds per chunk (longer than service default due to batch processing)

### Database Operations

- **Truncate-and-reload**: Full rebuild on each run (`TRUNCATE TABLE knowledge_chunks`)
- Uses raw psycopg2 (not SQLAlchemy) for bulk insert performance
- Commits after each file for progress safety
- Connection string from `DATABASE_URL` env var

### Archive Scale

- **Source directories:** `docs/archive/`, `docs/security/`
- **Archive files:** ~148 files
- **Total chunks:** ~4567 chunks
- Spans founding documents (1949) through current litigation (2024-2026)

---

## Design Notes

- **Verbatim preservation**: Chunks maintain exact legal language. The `verbatim` flag in `extra` marks chunks from verbatim transcriptions that should never be paraphrased.
- **Heading hierarchy**: Nested headings are joined with ` > ` separator (e.g., `"Section 5 > Voting Rights > Quorum"`) for context in search results.
- **Category detection is path-based**: The `detect_category()` function maps file paths to categories using directory structure, not content analysis.
- **Dual embedding functions**: `seed_knowledge.py` has its own `generate_embedding()` that mirrors `cove/services/embedding.py` but with a longer timeout (30s vs 15s) for batch processing. Both use the same Ollama model and truncation strategy.
- **No incremental updates**: The seed script always truncates and rebuilds. There is no mechanism for adding individual documents without re-seeding the entire knowledge base.
