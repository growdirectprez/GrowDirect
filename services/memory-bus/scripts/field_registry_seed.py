#!/usr/bin/env python3
"""Seed ALX pgvector memory with field registry context blocks.

Chunks the canonical field-registry.json by domain, producing one memory
block per domain. Each block contains the domain's tables, fields, enums,
join maps, and search catalog in a compact markdown format suitable for
ALX memory_recall().

Usage (inside Docker):
    python scripts/field_registry_seed.py docs/field-registry.json [--dry-run] [--force]

From host:
    docker compose -f devops/docker-compose.localhost.yml exec flask \
        python scripts/field_registry_seed.py docs/field-registry.json --force

GRO-265: Field Registry.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

# Ensure project root is on sys.path (for running inside Docker)
_app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _app_dir not in sys.path:
    sys.path.insert(0, _app_dir)

SESSION_ID = "seed-field-registry"


# ===================================================================
# Chunking
# ===================================================================

def chunk_registry(data: dict) -> list[dict]:
    """Split a field registry into domain-sized chunks for pgvector.

    Each chunk contains:
      - content: markdown-formatted domain summary
      - category: "field_registry"
      - tags: domain key, table names
      - metadata: for retrieval and dedup
    """
    chunks = []

    for domain_key, domain in data.get("domains", {}).items():
        label = domain.get("label", domain_key)
        desc = domain.get("description", "")
        tables = domain.get("tables", {})

        lines = [f"# Field Registry: {label}", ""]
        if desc:
            lines.append(f"{desc}")
            lines.append("")

        for table_key, table in tables.items():
            tlabel = table.get("label", table_key)
            tdesc = table.get("description", "")
            schema = table.get("schema", "?")
            immutable = "append-only" if table.get("immutable") else "mutable"

            lines.append(f"## {tlabel} ({schema}.{table_key}, {immutable})")
            lines.append(f"{tdesc}")
            lines.append("")

            fields = table.get("fields", {})
            if fields:
                lines.append("| Field | Type | Label | Searchable |")
                lines.append("|-------|------|-------|-----------|")
                for fk, fd in fields.items():
                    ftype = fd.get("type", "?")
                    flabel = fd.get("label", fk)
                    searchable = "✓" if fd.get("searchable") else ""
                    lines.append(f"| {fk} | {ftype} | {flabel} | {searchable} |")
                lines.append("")

            # Enum summaries (compact)
            for fk, fd in fields.items():
                if fd.get("type") == "enum" and "enum_values" in fd:
                    vals = ", ".join(fd["enum_values"].keys())
                    lines.append(f"**{fk}** values: {vals}")
            lines.append("")

        # Add relevant join maps
        join_maps = data.get("join_maps", {})
        table_names = set(tables.keys())
        relevant_joins = {
            jk: jm for jk, jm in join_maps.items()
            if jm.get("from_table") in table_names or jm.get("to_table") in table_names
        }
        if relevant_joins:
            lines.append("## Relationships")
            for jk, jm in relevant_joins.items():
                desc_text = jm.get("merchant_friendly", jk)
                lines.append(f"- {jm['from_table']} → {jm['to_table']}: {desc_text}")
            lines.append("")

        content = "\n".join(lines)
        table_keys = list(tables.keys())

        chunks.append({
            "content": content,
            "category": "field_registry",
            "domain": domain_key,
            "tags": [domain_key] + table_keys,
            "metadata": {
                "block_type": "field_registry",
                "domain": domain_key,
                "domain_label": label,
                "table_count": len(tables),
                "field_count": sum(len(t.get("fields", {})) for t in tables.values()),
                "source_file": "docs/field-registry.json",
                "content_hash": hashlib.sha256(content.encode()).hexdigest()[:16],
                "version": data.get("version", "1.0.0"),
                "created_by": "seed_field_registry",
            },
        })

    return chunks


# ===================================================================
# Storage
# ===================================================================

def delete_existing_blocks(force: bool, dry_run: bool) -> int:
    """Delete existing field_registry memory blocks."""
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
                    AND metadata->>'block_type' = 'field_registry'
                """),
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


def store_chunk(chunk: dict, dry_run: bool = False) -> bool:
    """Store a single chunk as a context_block memory."""
    domain = chunk["domain"]
    content = chunk["content"]
    metadata = chunk["metadata"]

    if dry_run:
        token_est = len(content) // 4
        print(f"  [DRY RUN] {domain}: ~{token_est} tokens, "
              f"{metadata['table_count']} tables, {metadata['field_count']} fields")
        return True

    try:
        from canary.services.alx.memory import memory_store

        result = memory_store(
            session_id=SESSION_ID,
            content=content,
            memory_type="context_block",
            metadata=metadata,
        )
        return result.get("memory_id") is not None
    except Exception as e:
        print(f"  ERROR storing {domain}: {e}")
        return False


# ===================================================================
# CLI
# ===================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Seed ALX pgvector memory with field registry context blocks"
    )
    parser.add_argument("json_path", help="Path to field-registry.json")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be stored")
    parser.add_argument("--force", action="store_true", help="Delete and re-store existing blocks")
    args = parser.parse_args()

    path = Path(args.json_path)
    if not path.exists():
        print(f"Error: {path} not found")
        sys.exit(1)

    with open(path) as f:
        data = json.load(f)

    chunks = chunk_registry(data)
    print(f"Field Registry Seed: {len(chunks)} domain chunks from {path.name}")

    if args.force:
        deleted = delete_existing_blocks(force=True, dry_run=args.dry_run)
        if deleted:
            print(f"  Deleted {deleted} existing field_registry blocks")

    stored = 0
    for chunk in chunks:
        if store_chunk(chunk, dry_run=args.dry_run):
            stored += 1

    action = "would store" if args.dry_run else "stored"
    print(f"\nSeeded {stored}/{len(chunks)} chunks into alx_memories "
          f"(category=field_registry)")


if __name__ == "__main__":
    main()
