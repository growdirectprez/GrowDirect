#!/usr/bin/env python3
"""Standalone memory bus seeder — no memory_bus package dependency.

Reads Brain/wiki/*.md, docs/sdds/**/*.md, docs/superpowers/plans/*.md
and seeds seed_embeddings via direct psycopg2 + Ollama REST calls.

Default mode is INCREMENTAL: only embeds files that are new or have been
modified since their last seed. Use --drop-first for a full reseed.

Usage:
  # Incremental (default) — run after any wiki/SDD additions:
  python3 services/memory-bus/scripts/seed_standalone.py

  # Full reseed:
  python3 services/memory-bus/scripts/seed_standalone.py --drop-first

  # Preview what would be seeded:
  python3 services/memory-bus/scripts/seed_standalone.py --dry-run
"""

import argparse
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import httpx
import psycopg2

GROWDIRECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

SOURCES = [
    {"glob": "Brain/wiki/*.md", "memory_type": "wiki_article", "layer": "corp"},
    {"glob": "docs/sdds/canary/*.md", "memory_type": "context_block", "layer": "canary"},
    {"glob": "docs/sdds/platform/*.md", "memory_type": "context_block", "layer": "corp"},
    {"glob": "docs/sdds/alx/*.md", "memory_type": "context_block", "layer": "shared"},
    {"glob": "docs/sdds/go-handoff/*.md", "memory_type": "context_block", "layer": "canary-go"},
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
EMBEDDING_DIM = 1024
MAX_TEXT = 6000


def get_embedding(text: str) -> list[float] | None:
    try:
        r = httpx.post(
            f"{OLLAMA_URL}/api/embed",
            json={"model": EMBEDDING_MODEL, "input": text[:MAX_TEXT], "keep_alive": -1},
            timeout=300.0,
        )
        r.raise_for_status()
        return [float(v) for v in r.json()["embeddings"][0][:EMBEDDING_DIM]]
    except Exception as e:
        print(f"  WARN: embedding failed — {e}", file=sys.stderr)
        return None


def collect_files() -> list[tuple[Path, dict]]:
    rows = []
    for src in SOURCES:
        for f in sorted(GROWDIRECT_ROOT.glob(src["glob"])):
            rows.append((f, src))
    return rows


def load_seeded_mtimes(cur) -> dict[str, datetime]:
    """Return {source_file: updated_at} for all rows currently in the table."""
    cur.execute("SELECT source_file, updated_at FROM seed_embeddings")
    return {row[0]: row[1] for row in cur.fetchall()}


def file_mtime(path: Path) -> datetime:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--drop-first", action="store_true")
    args = parser.parse_args()

    all_files = collect_files()

    if args.dry_run:
        print(f"Found {len(all_files)} source files across {len(SOURCES)} globs")
        for f, src in all_files:
            print(f"  [{src['memory_type']:15s}] {f.relative_to(GROWDIRECT_ROOT)}")
        return

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    if args.drop_first:
        cur.execute("TRUNCATE TABLE seed_embeddings")
        conn.commit()
        print("Truncated seed_embeddings — full reseed")
        seeded_mtimes = {}
    else:
        seeded_mtimes = load_seeded_mtimes(cur)

    # Determine which files need embedding
    to_process = []
    up_to_date = 0
    for path, src in all_files:
        rel = str(path.relative_to(GROWDIRECT_ROOT))
        if rel in seeded_mtimes:
            if file_mtime(path) <= seeded_mtimes[rel]:
                up_to_date += 1
                continue
        to_process.append((path, src, rel))

    if not to_process:
        print(f"All {len(all_files)} files up to date — nothing to do")
        cur.close()
        conn.close()
        return

    print(f"Found {len(all_files)} files — {up_to_date} up to date, {len(to_process)} to embed")

    inserted = updated = skipped = failed = 0

    for i, (path, src, rel) in enumerate(to_process, 1):
        content = path.read_text(encoding="utf-8", errors="replace")[:MAX_TEXT]
        if not content.strip():
            skipped += 1
            continue

        is_update = rel in seeded_mtimes
        label = "update" if is_update else "new"
        print(f"[{i:3d}/{len(to_process)}] [{label:6s}] {rel} ...", end=" ", flush=True)

        embedding = get_embedding(content)
        if embedding is None:
            failed += 1
            print("FAILED")
            continue

        meta = {"memory_type": src["memory_type"], "layer": src["layer"], "source_file": rel}

        if is_update:
            cur.execute(
                """
                UPDATE seed_embeddings
                SET content = %s, embedding = %s::vector, metadata = %s, updated_at = now()
                WHERE source_file = %s
                """,
                (content, str(embedding), json.dumps(meta), rel),
            )
            updated += 1
        else:
            cur.execute(
                """
                INSERT INTO seed_embeddings (id, source_file, section_path, content, embedding, metadata)
                VALUES (%s, %s, %s, %s, %s::vector, %s)
                """,
                (str(uuid.uuid4()), rel, rel, content, str(embedding), json.dumps(meta)),
            )
            inserted += 1

        conn.commit()
        print("ok")

    cur.close()
    conn.close()
    print(f"\nDone: {inserted} new, {updated} updated, {skipped} skipped (empty), {failed} failed")


if __name__ == "__main__":
    main()
