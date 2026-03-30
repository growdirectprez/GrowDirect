#!/usr/bin/env python3
"""Seed ALX memory with v2 SDD context blocks.

Reads the 13 domain-level SDDs from docs/sdds/v2/, chunks each file by ##
headers (each heading is a self-contained pgvector chunk), and stores them
via ALX memory_store() with memory_type="context_block".

Usage (inside Docker):
    python devops/scripts/seed_sdds_v2.py [--dry-run] [--force] [--file chirp.md]

From host:
    docker compose -f devops/docker-compose.localhost.yml exec flask \
        python devops/scripts/seed_sdds_v2.py --force

Linear: GRO-261 (code review SDD update)
"""

import argparse
import hashlib
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple

# Ensure /app is on sys.path when running inside Docker
_app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _app_dir not in sys.path:
    sys.path.insert(0, _app_dir)

SDDS_V2_DIR = os.path.join(_app_dir, "docs", "sdds", "v2")
SESSION_ID = "seed-sdds-v2"

# Domain name from filename (strip .md)
DOMAIN_MAP = {
    "architecture": "architecture",
    "identity": "identity",
    "webhook-pipeline": "tsp",
    "data-model": "data_model",
    "chirp": "chirp",
    "alert": "alert",
    "fox": "fox",
    "owl": "owl",
    "analytics": "analytics",
    "ops": "ops",
    "raas": "raas",
    "ui-bff": "ui_bff",
    "alx": "alx",
}


def chunk_by_headers(content: str, filename: str) -> List[Tuple[str, str]]:
    """Split markdown content into chunks at ## headers.

    Returns list of (heading, chunk_text) tuples.
    The file-level # heading is included as the first chunk's prefix.
    """
    chunks = []
    lines = content.split("\n")
    current_heading = filename  # fallback
    current_lines = []

    for line in lines:
        if line.startswith("## "):
            # Save previous chunk
            if current_lines:
                text = "\n".join(current_lines).strip()
                if text and len(text) > 50:  # Skip tiny chunks
                    chunks.append((current_heading, text))
            current_heading = line.lstrip("# ").strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    # Last chunk
    if current_lines:
        text = "\n".join(current_lines).strip()
        if text and len(text) > 50:
            chunks.append((current_heading, text))

    return chunks


def content_hash(text: str) -> str:
    """SHA-256 hash of content for dedup."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def delete_existing_sdd_blocks(domain: str, force: bool, dry_run: bool) -> int:
    """Delete existing context_block memories for this domain."""
    if not force or dry_run:
        return 0

    try:
        from canary.services.alx.memory import _get_session
        from sqlalchemy import text

        db = _get_session()
        try:
            result = db.execute(
                text("""
                    DELETE FROM alx_memories
                    WHERE memory_type = 'context_block'
                    AND metadata->>'source_file' LIKE :pattern
                """),
                {"pattern": f"%{domain}%"},
            )
            deleted = result.rowcount
            db.commit()
            return deleted
        except Exception as e:
            db.rollback()
            print(f"  WARNING: Could not delete existing blocks: {e}")
            return 0
        finally:
            db.close()
    except Exception:
        return 0


def store_chunk(heading: str, text: str, domain: str, source_file: str,
                chunk_index: int, dry_run: bool = False) -> bool:
    """Store a single chunk as a context_block memory."""
    if dry_run:
        token_est = len(text) // 4
        print(f"  [DRY RUN] {heading} (~{token_est} tokens, {len(text)} chars)")
        return True

    try:
        from canary.services.alx.memory import memory_store

        metadata = {
            "block_type": "sdd_v2",
            "domain": domain,
            "source_file": source_file,
            "heading": heading,
            "chunk_index": chunk_index,
            "content_hash": content_hash(text),
            "version": "2.0",
            "created_by": "seed_sdds_v2",
        }

        result = memory_store(
            session_id=SESSION_ID,
            content=text,
            memory_type="context_block",
            metadata=metadata,
        )
        return result.get("memory_id") is not None
    except Exception as e:
        print(f"  ERROR storing {heading}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Seed ALX memory with v2 SDD context blocks")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be stored")
    parser.add_argument("--force", action="store_true", help="Delete and re-store existing blocks")
    parser.add_argument("--file", type=str, help="Only seed one file (e.g., chirp.md)")
    args = parser.parse_args()

    print("=" * 60)
    print("SDD v2 Context Block Seeder")
    print("=" * 60)

    # Check memory layer
    if not args.dry_run:
        try:
            from canary.services.alx.memory import memory_healthy
            if not memory_healthy():
                print("ERROR: ALX memory database not reachable")
                sys.exit(1)
            print("Memory layer: OK")
        except Exception as e:
            print(f"ERROR: Cannot connect to memory layer: {e}")
            sys.exit(1)

    # Find SDD files
    sdd_dir = Path(SDDS_V2_DIR)
    if not sdd_dir.exists():
        print(f"ERROR: SDD directory not found: {SDDS_V2_DIR}")
        sys.exit(1)

    files = sorted(sdd_dir.glob("*.md"))
    if args.file:
        files = [f for f in files if f.name == args.file]
        if not files:
            print(f"ERROR: File not found: {args.file}")
            sys.exit(1)

    total_chunks = 0
    total_stored = 0
    total_deleted = 0

    for filepath in files:
        stem = filepath.stem  # e.g., "chirp"
        domain = DOMAIN_MAP.get(stem, stem)
        content = filepath.read_text(encoding="utf-8")
        chunks = chunk_by_headers(content, stem)

        print(f"\n--- {filepath.name} ({len(chunks)} chunks, domain={domain}) ---")

        # Delete existing blocks if --force
        if args.force:
            deleted = delete_existing_sdd_blocks(stem, args.force, args.dry_run)
            if deleted:
                print(f"  Deleted {deleted} existing blocks")
                total_deleted += deleted

        for i, (heading, text) in enumerate(chunks):
            success = store_chunk(heading, text, domain, filepath.name, i, dry_run=args.dry_run)
            total_chunks += 1
            if success:
                total_stored += 1
                if not args.dry_run:
                    token_est = len(text) // 4
                    print(f"  STORED [{i}] {heading} (~{token_est} tokens)")

    print(f"\n{'=' * 60}")
    print(f"Done. {total_stored}/{total_chunks} chunks stored.")
    if total_deleted:
        print(f"  Deleted: {total_deleted} old blocks")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
