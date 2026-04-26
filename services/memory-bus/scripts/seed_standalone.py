#!/usr/bin/env python3
"""Standalone memory bus seeder — no memory_bus package dependency.

Reads Brain/wiki/*.md, docs/sdds/**/*.md, docs/superpowers/plans/*.md
and seeds seed_embeddings via direct psycopg2 + Ollama REST calls.

Usage:
  DATABASE_URL=postgresql://growdirect:growdirect_dev@localhost:5432/growdirect_memory \
  OLLAMA_URL=http://127.0.0.1:11434 \
  python3 services/memory-bus/scripts/seed_standalone.py [--dry-run] [--drop-first]
"""

import argparse
import json
import os
import sys
import uuid
from pathlib import Path

import httpx
import psycopg2
from psycopg2.extras import execute_values

GROWDIRECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

SOURCES = [
    {"glob": "Brain/wiki/*.md", "memory_type": "wiki_article", "layer": "corp"},
    {"glob": "docs/sdds/canary/*.md", "memory_type": "context_block", "layer": "canary"},
    {"glob": "docs/sdds/platform/*.md", "memory_type": "context_block", "layer": "corp"},
    {"glob": "docs/sdds/alx/*.md", "memory_type": "context_block", "layer": "shared"},
    {"glob": "docs/team/*.md", "memory_type": "team_profile", "layer": "corp"},
    {"glob": "docs/decisions/*.md", "memory_type": "decision", "layer": "corp"},
    {"glob": "docs/superpowers/plans/*.md", "memory_type": "build_plan", "layer": "corp"},
]

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://growdirect:growdirect_dev@localhost:5432/growdirect_memory",
)
EMBEDDING_MODEL = "qwen3-embedding:8b"
EMBEDDING_DIM = 1024  # Matryoshka truncation from native 4096
MAX_TEXT = 6000


def get_embedding(text: str) -> list[float] | None:
    try:
        r = httpx.post(
            f"{OLLAMA_URL}/api/embed",
            json={"model": EMBEDDING_MODEL, "input": text[:MAX_TEXT]},
            timeout=120.0,
        )
        r.raise_for_status()
        return [float(v) for v in r.json()["embeddings"][0][:EMBEDDING_DIM]]
    except Exception as e:
        print(f"  WARN: embedding failed — {e}", file=sys.stderr)
        return None


def collect_files() -> list[tuple[Path, dict]]:
    rows = []
    for src in SOURCES:
        files = sorted(GROWDIRECT_ROOT.glob(src["glob"]))
        for f in files:
            rows.append((f, src))
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--drop-first", action="store_true")
    args = parser.parse_args()

    files = collect_files()
    print(f"Found {len(files)} source files across {len(SOURCES)} globs")

    if args.dry_run:
        for f, src in files:
            print(f"  [{src['memory_type']:15s}] {f.relative_to(GROWDIRECT_ROOT)}")
        return

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    if args.drop_first:
        cur.execute("TRUNCATE TABLE seed_embeddings")
        conn.commit()
        print("Truncated seed_embeddings")

    inserted = skipped = failed = 0

    for i, (path, src) in enumerate(files, 1):
        rel = str(path.relative_to(GROWDIRECT_ROOT))
        content = path.read_text(encoding="utf-8", errors="replace")[:MAX_TEXT]
        if not content.strip():
            skipped += 1
            continue

        print(f"[{i:3d}/{len(files)}] {rel} ...", end=" ", flush=True)
        embedding = get_embedding(content)
        if embedding is None:
            failed += 1
            print("FAILED")
            continue

        meta = {
            "memory_type": src["memory_type"],
            "layer": src["layer"],
            "source_file": rel,
        }

        cur.execute(
            """
            INSERT INTO seed_embeddings (id, source_file, section_path, content, embedding, metadata)
            VALUES (%s, %s, %s, %s, %s::vector, %s)
            ON CONFLICT DO NOTHING
            """,
            (
                str(uuid.uuid4()),
                rel,
                rel,
                content,
                str(embedding),
                json.dumps(meta),
            ),
        )
        conn.commit()
        inserted += 1
        print("ok")

    cur.close()
    conn.close()
    print(f"\nDone: {inserted} inserted, {skipped} skipped (empty), {failed} failed")


if __name__ == "__main__":
    main()
