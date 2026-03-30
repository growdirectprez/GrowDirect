#!/usr/bin/env python3
"""Batch-embed all ALX memories using qwen3-embedding-8B via Ollama.

Reads alx_memories from PostgreSQL, generates 1024-dim embeddings via
Ollama's /api/embed endpoint, and stores them in the embedding column.

GRO-240: Upgraded from nomic-embed-text (768d) to qwen3-embedding-8B (1024d).

Skips memories that already have embeddings unless --force is used.

Run inside container:
    python3 devops/scripts/embed_memories_batch.py [--batch-size 50] [--dry-run] [--force]
"""
import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error

sys.path.insert(0, "/app")


OLLAMA_URL = os.getenv("OWL_URL", "http://host.docker.internal:11434")
# EMBEDDING_MODEL may have "ollama/" prefix (for litellm routing) — strip it
_raw_model = os.getenv("EMBEDDING_MODEL", "qwen3-embedding:8b")
EMBED_MODEL = _raw_model.replace("ollama/", "")


def get_ollama_embedding(text: str) -> list:
    """Get embedding vector from Ollama's /api/embed endpoint."""
    payload = json.dumps({
        "model": EMBED_MODEL,
        "input": text,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/embed",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())

    # Ollama returns {"embeddings": [[...vector...]]}
    embeddings = result.get("embeddings", [])
    if not embeddings:
        raise ValueError(f"No embeddings returned: {result}")
    # Matryoshka truncation: 4096d → 1024d (pgvector HNSW limit)
    return embeddings[0][:1024]


def get_memories(session, force=False, memory_type=None, limit=None):
    """Fetch memories that need embedding."""
    from sqlalchemy import text

    where_clauses = []
    params = {}

    if not force:
        where_clauses.append("embedding IS NULL")

    if memory_type:
        where_clauses.append("memory_type = :mt")
        params["mt"] = memory_type

    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)

    sql = f"""
        SELECT id, memory_type, content, (embedding IS NOT NULL) as has_embedding
        FROM alx_memories
        {where_sql}
        ORDER BY created_at
    """

    if limit:
        sql += " LIMIT :lim"
        params["lim"] = limit

    return session.execute(text(sql), params).fetchall()


def embed_batch(session, memories, batch_num, total_batches):
    """Embed a batch of memories and store vectors."""
    from sqlalchemy import text

    print(f"\n  Batch {batch_num}/{total_batches}: {len(memories)} memories")

    succeeded = 0
    failed = 0
    t0 = time.time()

    for m in memories:
        mem_id = str(m[0])
        mem_type = m[1]
        content = m[2]

        try:
            # Truncate to stay within nomic-embed-text's 8192 token window.
            # Some dense content (SDDs with code) has high token:char ratio.
            if len(content) > 4000:
                content = content[:4000]

            vec = get_ollama_embedding(content)

            # Store as pgvector format: [0.1, 0.2, ...]
            vec_str = "[" + ",".join(str(v) for v in vec) + "]"

            session.execute(
                text("UPDATE alx_memories SET embedding = :vec WHERE id = :id"),
                {"vec": vec_str, "id": mem_id},
            )
            succeeded += 1

        except Exception as e:
            print(f"    FAIL {mem_id[:8]} ({mem_type}): {e}")
            failed += 1

    session.commit()
    elapsed = time.time() - t0
    rate = len(memories) / elapsed if elapsed > 0 else 0
    print(f"  Done in {elapsed:.1f}s ({rate:.1f} mem/s) — {succeeded} ok, {failed} failed")

    return {"batch": batch_num, "succeeded": succeeded, "failed": failed, "time": elapsed}


def main():
    parser = argparse.ArgumentParser(description="Batch-embed ALX memories with nomic-embed-text")
    parser.add_argument("--batch-size", type=int, default=50, help="Memories per batch (default: 50)")
    parser.add_argument("--type", type=str, default=None, help="Filter by memory_type")
    parser.add_argument("--limit", type=int, default=None, help="Max memories to process")
    parser.add_argument("--force", action="store_true", help="Re-embed memories that already have embeddings")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be embedded")
    args = parser.parse_args()

    from canary.services.alx.memory import _get_session

    # Verify Ollama connectivity
    print(f"Ollama URL: {OLLAMA_URL}")
    print(f"Embed model: {EMBED_MODEL}")
    try:
        test_vec = get_ollama_embedding("test")
        print(f"Ollama OK — {len(test_vec)}-dim vectors")
    except Exception as e:
        print(f"ERROR: Cannot reach Ollama: {e}")
        sys.exit(1)

    session = _get_session()
    try:
        memories = get_memories(session, force=args.force, memory_type=args.type, limit=args.limit)
        print(f"\nMemories to embed: {len(memories)}")

        if args.dry_run:
            print("DRY RUN — would embed these memories:")
            types = {}
            for m in memories:
                mt = m[1]
                types[mt] = types.get(mt, 0) + 1
            for mt, count in sorted(types.items()):
                print(f"  {mt}: {count}")
            return

        if not memories:
            print("Nothing to embed — all memories already have embeddings.")
            return

        # Process in batches
        batch_size = args.batch_size
        batches = [memories[i:i + batch_size] for i in range(0, len(memories), batch_size)]
        total_batches = len(batches)
        print(f"Processing {total_batches} batches of ~{batch_size}")

        results = []
        overall_start = time.time()

        for i, batch in enumerate(batches, 1):
            result = embed_batch(session, batch, i, total_batches)
            results.append(result)

        overall_time = time.time() - overall_start
        total_ok = sum(r["succeeded"] for r in results)
        total_fail = sum(r["failed"] for r in results)

        print(f"\n{'='*60}")
        print(f"COMPLETE: {total_ok} embedded, {total_fail} failed in {overall_time:.0f}s ({overall_time/60:.1f} min)")

        # Verify
        row = session.execute(
            __import__("sqlalchemy").text(
                "SELECT COUNT(*) FROM alx_memories WHERE embedding IS NOT NULL"
            )
        ).scalar()
        print(f"Memories with embeddings: {row}")

    finally:
        session.close()


if __name__ == "__main__":
    main()
