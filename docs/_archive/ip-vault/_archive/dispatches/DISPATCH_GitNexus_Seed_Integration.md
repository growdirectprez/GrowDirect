---
type: workorder
domain: canary
status: active
created: 2026-03-19
updated: 2026-03-19
---
# DISPATCH: GitNexus Seed Integration & Semantic Search Configuration
*Issued by Jeffe · March 19, 2026*
*Linear: GRO-240 (Evaluate GitNexus MCP server for ALX code intelligence)*

---

## Situation

Eight curated IP documents (8,450 words) were distilled from the iCloud `Canary_IP` archive into `~/GrowDirect/IP/gitnexus-seed/`. These cover product, architecture, strategy, research, operations, glossary, and data gap analysis — the business/product context that the codebase graph doesn't carry.

GitNexus currently indexes 1,323 files with 6,791 nodes, but:
- **Embeddings: 0** — semantic search is disabled
- **Generated skills: reverted** — GitNexus auto-generated `AGENTS.md` and `.claude/skills/gitnexus/` which were removed (Guardian violation, conflicted with existing skill system)
- **Seed docs are outside the repo tree** — GitNexus only indexes `~/GrowDirect/Canary/`
- **`.gitnexus/` is gitignored** — 97MB binary DB stays local

The seeds exist but GitNexus can't see them and can't search them.

### Constraint from GRO-240
GitNexus previously overwrote `CLAUDE.md` and injected opinionated skills without permission. Any re-index must NOT use flags that regenerate agent files. The Canary skill system (21 skills in `.claude/skills/`) is authoritative — GitNexus provides graph data via MCP tools only.

---

## Step 1: Place seed docs inside the repo tree

GitNexus indexes everything under `repoPath` (`~/GrowDirect/Canary/`). The seed docs live in `~/GrowDirect/IP/gitnexus-seed/`. Symlink them in:

```bash
ln -s ~/GrowDirect/IP/gitnexus-seed ~/GrowDirect/Canary/docs/gitnexus-seed
```

If GitNexus doesn't follow symlinks, copy instead:

```bash
cp -r ~/GrowDirect/IP/gitnexus-seed ~/GrowDirect/Canary/docs/gitnexus-seed
```

**Verify:** `ls ~/GrowDirect/Canary/docs/gitnexus-seed/` shows all 8 files.

---

## Step 2: Embed seed docs + ALX memories with qwen3-embedding-8B

### Why not just use GitNexus embeddings?
GitNexus uses `snowflake-arctic-embed-xs` (33M params, 384 dims) — a tiny code-token model. Good for structural code queries, weak for business prose. The seed docs are dense IP context (product strategy, LP research, data gap analysis). ALX and Owl need a model built for mixed technical prose, not just code symbols.

### Model choice: qwen3-embedding-8B
MTEB #1 (score 70.58). Same model family as Owl's inference engine (qwen3). Instruction-aware — you can prefix queries with task context to improve retrieval. Flexible dimensions (32–2560). 8192 token context window covers every seed document section in a single pass.

### Why 8B is fine
Embedding is a **batch job, not a resident process**. Run it once, store the vectors in pgvector, done. Re-run only when seed content changes (monthly at most). Owl's qwen3:14b is not live in dev — the full 24GB MacBook is available. The 8B model loads at ~9–10GB, runs the batch, unloads. No contention. At 24GB there's even room to run the 8B at Q8 quantization for higher fidelity, or time-share with Owl's 14b later if needed.

### Procedure

```bash
# 1. Pull the embedding model
ollama pull dengcao/Qwen3-Embedding-8B:Q5_K_M

# 2. Embed seed docs — chunk by H2/H3 section, store in pgvector
#    Script: ~/GrowDirect/Canary/devops/scripts/embed_seeds.py (to be written)
#    Input:  ~/GrowDirect/IP/gitnexus-seed/*.md
#    Output: canary_memory.seed_embeddings table
#    Dims:   1024 (balance of quality vs storage; model supports 32–2560)

# 3. Re-embed ALX memories with the same model for consistent vector space
#    Input:  canary_memory.memories (954 existing entries)
#    Output: canary_memory.memories.embedding column (update in place)

# 4. Unload when done
ollama rm dengcao/Qwen3-Embedding-8B:Q5_K_M
```

### Chunking strategy
Each seed doc section (H2/H3 boundary) becomes one embedding. The docs were written with this in mind — every section is self-contained, keyword-dense, 200–500 words. At 1024 dimensions and ~100 sections across 8 files, total vector storage is ~400KB in pgvector. Negligible.

### Dual retrieval path
After embedding, two search paths exist:

| Query Type | Path | Model | Best For |
|------------|------|-------|----------|
| "What connects to what in code" | GitNexus `query` MCP tool | snowflake-arctic-embed-xs (33M) | Symbol relationships, call chains, blast radius |
| "What does this mean / what should I do" | pgvector `memory_recall` | qwen3-embedding-8B | Business context, architectural decisions, gap analysis |

ALX uses both. Owl uses pgvector only (no code navigation needed).

---

## Step 3: Re-index GitNexus (code graph only)

Run the GitNexus re-index to pick up the symlinked seed docs for BM25 keyword search. GitNexus embeddings (`snowflake-arctic-embed-xs`) are optional — the heavy semantic lifting is done by qwen3-embedding-8B in pgvector.

```bash
npx gitnexus analyze ~/GrowDirect/Canary --embeddings --force
```

**Do NOT run `--skills`.** GRO-240 documents that GitNexus auto-generated files conflicted with the Canary skill system and were reverted. The 21 skills in `.claude/skills/` are hand-built and authoritative. GitNexus provides graph data via MCP tools only.

**Verify:** `meta.json` shows `"embeddings"` > 0 and `"files"` increased from 1,323.

---

## Step 4: Test dual retrieval

### pgvector (qwen3-embedding-8B vectors)
```
memory_recall("elJeffe protocol inscription pipeline")
memory_recall("CRDM v1.1 amendment scorecard external_identities")
memory_recall("blocked chirp rules data gaps")
memory_recall("IBM retail BI lineage tLog gLog")
memory_recall("line_item_discounts sweethearting C-203")
```

### GitNexus (code graph + BM25 + snowflake vectors)
```
gitnexus_query("elJeffe protocol inscription pipeline")
gitnexus_query("TspService process_webhook seal parse merkle")
gitnexus_query("Chirp detection rule evaluation")
```

Compare results. pgvector should dominate on business/strategy/gap queries. GitNexus should dominate on symbol-level code navigation. If both return useful results for the same query, that's the overlap zone where either path works.

---

## Step 5: Register seed provenance in ALX memory

```
memory_store:
  topic: "gitnexus seed documents"
  content: "8 curated IP docs in ~/GrowDirect/Canary/docs/gitnexus-seed/ covering
           product (01), architecture (02), strategy (03), research (04),
           operations (05), glossary (06), data gaps (07), plus index (00).
           Embedded with qwen3-embedding-8B into canary_memory.seed_embeddings.
           GitNexus also indexes them for BM25 keyword search.
           Two retrieval paths: memory_recall for business context,
           gitnexus_query for code graph navigation."
```

---

## Step 6: Write embed_seeds.py

Deliverable: `~/GrowDirect/Canary/devops/scripts/embed_seeds.py`

The script should:
1. Read each markdown file from the seed directory
2. Split on H2/H3 headers (each section = one chunk)
3. Prepend each chunk with its file name and section path as metadata
4. Call Ollama embedding API (`POST /api/embeddings`) with qwen3-embedding-8B
5. Store vectors in `canary_memory.seed_embeddings` (new table)
6. Optionally re-embed existing `canary_memory.memories` rows for vector space consistency
7. Report: chunks embedded, dimensions, total storage, time elapsed

Table schema:
```sql
CREATE TABLE canary_memory.seed_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_file TEXT NOT NULL,        -- e.g. '01_PRODUCT.md'
    section_path TEXT NOT NULL,        -- e.g. 'Chirp — Detection Engine'
    content TEXT NOT NULL,             -- raw section text
    embedding vector(1024) NOT NULL,   -- qwen3-embedding-8B output
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_seed_embeddings_vector
    ON canary_memory.seed_embeddings
    USING hnsw (embedding vector_cosine_ops);
```

---

## Seed Document Manifest

| File | Words | Retrieval Keywords |
|------|-------|--------------------|
| `00_INDEX.md` | 531 | manifest, source map, chunking, embedding |
| `01_PRODUCT.md` | 1,030 | TSP, Chirp, Fox, Owl, ALX, RaaS, detection rules, blocked rules |
| `02_ARCHITECTURE.md` | 1,681 | CRDM, elJeffe, Merkle, pipeline, amendment scorecard, data coverage |
| `03_STRATEGY.md` | 887 | tLog, gLog, market thesis, competitive, GTM, revenue, cannabis |
| `04_RESEARCH.md` | 887 | IBM BI, RDWM, RBST, RSDM, LP patterns, ARTS, Alpha3X |
| `05_OPERATIONS.md` | 978 | team, Factory Process, deploy, lab network, testing, GitNexus |
| `06_GLOSSARY.md` | 1,258 | enums, GRO issues, target tables, file paths, Chirp ranges |
| `07_DATA_GAPS.md` | 1,198 | amendments, migration sequence, external_identities, parser gaps |

---

## Expected Outcome

After steps 1–5, a GitNexus `query("how does Canary detect sweethearting")` should return:
- `01_PRODUCT.md` — C-203 rule definition + blocked status
- `07_DATA_GAPS.md` — line_item_modifiers dependency
- `02_ARCHITECTURE.md` — parser gap in Tier 1
- Plus any codebase files in `canary/services/chirp/` that reference the rule

That's the full-stack retrieval: business context from the seeds + code context from the graph.

---

## GRO-240 Open Tasks (Context)

These tasks from the existing GitNexus evaluation issue are complementary to this seed work:

- [ ] Configure GitNexus MCP server in `.claude/settings.json`
- [ ] Test `gitnexus_impact` on a high-connectivity symbol (e.g., `TspService.process_webhook`)
- [ ] Test `gitnexus_query` vs `memory_recall` — compare results for same question
- [ ] Evaluate token/context cost — does it bloat the context window?
- [ ] Decide: integrate into canary-debug/canary-blueprint skills, or keep as optional tool?
- [ ] Add `npx gitnexus analyze` to post-commit hook or session startup?

The seed integration (this dispatch) feeds Step 2 of GRO-240 — once embeddings are enabled and seeds are indexed, the `gitnexus_query` vs `memory_recall` comparison becomes meaningful because both systems will have business context to search against.

---

*Canary LP | GrowDirect Inc. | Confidential*
