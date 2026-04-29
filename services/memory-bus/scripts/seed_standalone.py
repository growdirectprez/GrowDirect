#!/usr/bin/env python3
"""Standalone memory bus seeder — no memory_bus package dependency.

Reads Brain/wiki/*.md, Brain/wiki/cards/*.md, docs/sdds/**/*.md,
docs/superpowers/plans/*.md, docs/superpowers/specs/*.md
and seeds alx_memories via direct psycopg2 + Ollama REST calls.

Rows are written with session_id='seed-standalone' so they surface
through memory_recall() exactly like seed_clean.py content.

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
import fcntl
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import httpx
import psycopg2

LOCK_FILE = Path("/tmp/growdirect-seed.lock")

GROWDIRECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

SEED_SESSION_ID = "seed-standalone"

# memory_type must be one of: decision, finding, context, architecture,
#   session_summary, procedure, context_block, work_product, team_profile, foundation
# layer must be one of: corp, canary, cove, shared
SOURCES = [
    {"glob": "Brain/wiki/*.md", "memory_type": "context_block", "layer": "corp"},
    {"glob": "Brain/wiki/cards/*.md", "memory_type": "context_block", "layer": "corp"},
    {"glob": "docs/sdds/canary/*.md", "memory_type": "context_block", "layer": "canary"},
    {"glob": "docs/sdds/platform/*.md", "memory_type": "context_block", "layer": "corp"},
    {"glob": "docs/sdds/alx/*.md", "memory_type": "context_block", "layer": "shared"},
    {"glob": "docs/sdds/go-handoff/*.md", "memory_type": "context_block", "layer": "canary"},
    {"glob": "docs/team/*.md", "memory_type": "team_profile", "layer": "corp"},
    {"glob": "docs/decisions/*.md", "memory_type": "decision", "layer": "corp"},
    {"glob": "docs/superpowers/plans/*.md", "memory_type": "work_product", "layer": "corp"},
    {"glob": "docs/superpowers/specs/*.md", "memory_type": "work_product", "layer": "corp"},
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
    """Return {source_file: updated_at} for all seed-standalone rows in alx_memories."""
    cur.execute(
        "SELECT metadata->>'source_file', updated_at FROM alx_memories WHERE session_id = %s",
        (SEED_SESSION_ID,),
    )
    return {row[0]: row[1] for row in cur.fetchall() if row[0]}


def file_mtime(path: Path) -> datetime:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--drop-first", action="store_true")
    args = parser.parse_args()

    # --- Exclusive lock: only one seed process at a time ---
    if not args.dry_run:
        lock_fh = open(LOCK_FILE, "w")
        try:
            fcntl.flock(lock_fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print(
                f"ERROR: Another seed process is already running (lock held at {LOCK_FILE}).\n"
                "Kill it first: pkill -f seed_standalone.py",
                file=sys.stderr,
            )
            sys.exit(1)
        lock_fh.write(str(os.getpid()))
        lock_fh.flush()
    # -------------------------------------------------------

    all_files = collect_files()

    if args.dry_run:
        print(f"Found {len(all_files)} source files across {len(SOURCES)} globs")
        for f, src in all_files:
            print(f"  [{src['memory_type']:15s}] {f.relative_to(GROWDIRECT_ROOT)}")
        return

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    if args.drop_first:
        cur.execute("DELETE FROM alx_memories WHERE session_id = %s", (SEED_SESSION_ID,))
        conn.commit()
        print(f"Deleted all session_id='{SEED_SESSION_ID}' rows from alx_memories — full reseed")
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

        meta = {
            "source_file": rel,
            "seeded_at": datetime.now(tz=timezone.utc).isoformat(),
            "seeded_by": "seed_standalone.py",
            "source_kind": src.get("source_kind", "document"),
        }

        if is_update:
            cur.execute(
                """
                UPDATE alx_memories
                SET content = %s, embedding = %s::vector, metadata = %s, updated_at = now()
                WHERE session_id = %s AND metadata->>'source_file' = %s
                """,
                (content, str(embedding), json.dumps(meta), SEED_SESSION_ID, rel),
            )
            updated += 1
        else:
            cur.execute(
                """
                INSERT INTO alx_memories
                    (id, session_id, memory_type, content, embedding, metadata, layer, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s::vector, %s, %s, now(), now())
                """,
                (
                    str(uuid.uuid4()),
                    SEED_SESSION_ID,
                    src["memory_type"],
                    content,
                    str(embedding),
                    json.dumps(meta),
                    src["layer"],
                ),
            )
            inserted += 1

        conn.commit()
        print("ok")

    cur.close()
    conn.close()
    print(f"\nDone: {inserted} new, {updated} updated, {skipped} skipped (empty), {failed} failed")


if __name__ == "__main__":
    main()
