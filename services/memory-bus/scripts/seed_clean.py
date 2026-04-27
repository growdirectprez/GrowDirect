#!/usr/bin/env python3
# GrowDirect LLC — Confidential & Proprietary
# Copyright (c) 2026 GrowDirect LLC. All rights reserved.
"""Seed memory bus from the clean docs/ tree.

Replaces all legacy seed scripts (seed_context_blocks, seed_memory_foundation,
seed_sdds_v2, seed_team_profiles, seed_work_products, etc.) with one script
that reads from the reorganized document archive (GRO-379).

Sources:
  docs/sdds/**/*.md         → context_block (per namespace layer)
  docs/team/*.md            → team_profile (corp layer)
  docs/decisions/*.md       → decision (corp layer)
  docs/research/*.md        → foundation (canary layer)

Per-app SDD seeds for apps outside the platform repo live with each
app's own seed runner. This script seeds only platform + canary +
shared sources.

Usage:
  # From host (needs DATABASE_URL):
  DATABASE_URL=postgresql://growdirect:growdirect_dev@localhost:5432/growdirect_memory \
    python3 services/memory-bus/scripts/seed_clean.py [--dry-run] [--drop-first]

  # Inside Docker:
  docker exec growdirect_memory_bus python3 scripts/seed_clean.py --drop-first
"""

import argparse
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

# Add memory-bus to path
_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_root))

from memory_bus.config import Config
from memory_bus.embeddings import get_embedding

# ---------------------------------------------------------------------------
# Source definitions
# ---------------------------------------------------------------------------

GROWDIRECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

SOURCES = [
    # SDDs — context blocks, one per namespace
    {
        "glob": "docs/sdds/platform/*.md",
        "memory_type": "context_block",
        "layer": "corp",
        "metadata_extra": {"block_type": "domain_overview"},
    },
    {
        "glob": "docs/sdds/canary/*.md",
        "memory_type": "context_block",
        "layer": "canary",
        "metadata_extra": {"block_type": "domain_overview"},
    },
    {
        "glob": "docs/sdds/alx/*.md",
        "memory_type": "context_block",
        "layer": "shared",
        "metadata_extra": {"block_type": "domain_overview"},
    },
    # Team profiles
    {
        "glob": "docs/team/*.md",
        "memory_type": "team_profile",
        "layer": "corp",
        "metadata_extra": {},
    },
    # Architecture decisions
    {
        "glob": "docs/decisions/*.md",
        "memory_type": "decision",
        "layer": "corp",
        "metadata_extra": {},
    },
    # Research — LP pattern catalog is the high-value one
    {
        "glob": "docs/research/lp-dashboard-pattern-catalog.md",
        "memory_type": "foundation",
        "layer": "canary",
        "metadata_extra": {"domain": "chirp"},
    },
    # Brain dispatches — operating instructions / decisions on what to do
    # Added 2026-04-25 (resolves memory_bus.cli drift identified during the
    # 2026-04-25 RAPID + Secure dispatch runs; extends seed_clean.py
    # additively rather than building the full memory_bus.cli surface).
    {
        "glob": "Brain/dispatches/*.md",
        "memory_type": "dispatch",
        "layer": "corp",
        "metadata_extra": {"source_kind": "operating_instruction"},
    },
    # Brain wiki — synthesis layer (module specs, project context, founder
    # context articles, integration mappings)
    {
        "glob": "Brain/wiki/*.md",
        "memory_type": "wiki_article",
        "layer": "corp",
        "metadata_extra": {"source_kind": "synthesis"},
    },
    # Build plans — operational plans companion to SDDs
    {
        "glob": "docs/superpowers/plans/*.md",
        "memory_type": "build_plan",
        "layer": "corp",
        "metadata_extra": {"source_kind": "operational_plan"},
    },
]


def collect_files(source: dict) -> list[Path]:
    """Resolve glob or file path to list of files."""
    if "file" in source:
        p = GROWDIRECT_ROOT / source["file"]
        return [p] if p.exists() else []
    if "glob" in source:
        return sorted(GROWDIRECT_ROOT.glob(source["glob"]))
    return []


def read_content(path: Path, max_chars: int = 6000) -> str:
    """Read file content, truncating if needed."""
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n[...truncated for embedding]"
    return text


def build_metadata(path: Path, source: dict) -> dict:
    """Build metadata dict for a memory entry."""
    meta = {
        "source_file": str(path.relative_to(GROWDIRECT_ROOT)),
        "seeded_by": "seed_clean.py",
        "seeded_at": datetime.now(timezone.utc).isoformat(),
    }
    meta.update(source.get("metadata_extra", {}))
    return meta


# ---------------------------------------------------------------------------
# Database operations
# ---------------------------------------------------------------------------

def drop_all_memories(engine):
    """Delete all rows from alx_memories and alx_sessions."""
    from sqlalchemy import text
    with engine.connect() as conn:
        count = conn.execute(text("SELECT count(*) FROM alx_memories")).scalar()
        conn.execute(text("DELETE FROM alx_memories"))
        conn.execute(text("DELETE FROM alx_sessions"))
        conn.commit()
    return count


def insert_memory(engine, config, content, memory_type, layer, metadata, dry_run=False):
    """Insert a single memory with embedding."""
    from sqlalchemy import text

    memory_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)

    if dry_run:
        return memory_id, False

    embedding = get_embedding(content, config)

    with engine.connect() as conn:
        if embedding:
            conn.execute(
                text("""
                    INSERT INTO alx_memories
                        (id, session_id, memory_type, content, metadata,
                         embedding, layer, created_at, updated_at)
                    VALUES
                        (:id, 'seed-clean', :mtype, :content, :meta,
                         :embedding, :layer, :now, :now)
                """),
                {
                    "id": memory_id,
                    "mtype": memory_type,
                    "content": content,
                    "meta": json.dumps(metadata),
                    "embedding": str(embedding),
                    "layer": layer,
                    "now": now,
                },
            )
        else:
            conn.execute(
                text("""
                    INSERT INTO alx_memories
                        (id, session_id, memory_type, content, metadata,
                         layer, created_at, updated_at)
                    VALUES
                        (:id, 'seed-clean', :mtype, :content, :meta,
                         :layer, :now, :now)
                """),
                {
                    "id": memory_id,
                    "mtype": memory_type,
                    "content": content,
                    "meta": json.dumps(metadata),
                    "layer": layer,
                    "now": now,
                },
            )
        conn.commit()

    return memory_id, embedding is not None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def ensure_seed_session(engine):
    """Create a session record for seed-clean if one doesn't exist."""
    from sqlalchemy import text
    session_id = "seed-clean"
    now = datetime.now(timezone.utc).isoformat()
    with engine.connect() as conn:
        existing = conn.execute(
            text("SELECT 1 FROM alx_sessions WHERE session_id = :sid"),
            {"sid": session_id},
        ).fetchone()
        if not existing:
            conn.execute(
                text("""
                INSERT INTO alx_sessions (session_id, status, started_at, summary)
                VALUES (:sid, 'active', :now, 'Seed script session')
                """),
                {"sid": session_id, "now": now},
            )
            conn.commit()


def close_seed_session(engine):
    """Mark the seed-clean session as closed."""
    from sqlalchemy import text
    session_id = "seed-clean"
    now = datetime.now(timezone.utc).isoformat()
    with engine.connect() as conn:
        conn.execute(
            text("""
            UPDATE alx_sessions
            SET status = 'closed', closed_at = :now, summary = 'Seed complete'
            WHERE session_id = :sid
            """),
            {"sid": session_id, "now": now},
        )
        conn.commit()


def get_existing_source_files(engine) -> set[str]:
    """Return set of source_file paths already in alx_memories."""
    from sqlalchemy import text
    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT metadata->>'source_file' FROM alx_memories WHERE metadata->>'source_file' IS NOT NULL")
        ).fetchall()
    return {r[0] for r in rows}


def main():
    parser = argparse.ArgumentParser(description="Seed memory bus from clean docs/")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be seeded")
    parser.add_argument("--drop-first", action="store_true", help="Drop all existing memories first")
    parser.add_argument("--incremental", action="store_true",
                        help="Skip files already seeded (by source_file metadata)")
    args = parser.parse_args()

    config = Config()

    from sqlalchemy import create_engine
    engine = create_engine(config.database_url)

    if args.drop_first and not args.dry_run:
        count = drop_all_memories(engine)
        print(f"Dropped {count} existing memories")

    existing_files: set[str] = set()
    if args.incremental:
        existing_files = get_existing_source_files(engine)
        print(f"Incremental mode: {len(existing_files)} files already seeded")

    if not args.dry_run:
        ensure_seed_session(engine)

    total = 0
    embedded = 0
    skipped = 0

    for source in SOURCES:
        files = collect_files(source)
        if not files:
            pattern = source.get("glob") or source.get("file")
            print(f"  SKIP (no files): {pattern}")
            continue

        for path in files:
            rel = path.relative_to(GROWDIRECT_ROOT)

            if args.incremental and str(rel) in existing_files:
                skipped += 1
                continue

            content = read_content(path)
            metadata = build_metadata(path, source)
            layer = source["layer"]
            mtype = source["memory_type"]

            if args.dry_run:
                print(f"  DRY: {rel} → {mtype} [{layer}] ({len(content)} chars)")
                total += 1
                continue

            mid, has_emb = insert_memory(
                engine, config, content, mtype, layer, metadata,
            )
            status = "+" if has_emb else "~"
            print(f"  {status} {rel} → {mtype} [{layer}]")
            total += 1
            if has_emb:
                embedded += 1

    action = "Would seed" if args.dry_run else "Seeded"
    print(f"\n{action}: {total} memories ({embedded} with embeddings)")
    if skipped:
        print(f"Skipped (already seeded): {skipped}")

    if not args.dry_run:
        close_seed_session(engine)


if __name__ == "__main__":
    main()
