#!/usr/bin/env python3
"""GRO-170: Seed ALX Cognee memory with _ALX work products.

Scans the _ALX/ filesystem for deliverables, work orders, dispatches,
operational docs, and WarChest content. Chunks and stores each document
via the ALX memory_store Python API (bypasses HTTP/JWT).

Categories:
  - deliverable     — agent output files (by role/domain)
  - work_order      — dispatched work orders
  - dispatch        — session prompts sent to agents
  - capture         — CEO directive captures
  - operational     — DISPATCH, HANDOFF, TRIAGE, etc.
  - war_chest       — investor briefing source content
  - prd             — product requirements documents
  - legal           — legal documents
  - research        — research papers and position papers
  - qa_report       — QA reports

Idempotent: checks for existing memories before inserting.

Usage (run inside Docker container):
    python devops/scripts/seed_work_products.py [--dry-run] [--category NAME] [--force]

Or from host (files mounted):
    docker compose -f devops/docker-compose.localhost.yml exec flask \
        python devops/scripts/seed_work_products.py --dry-run
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

# Inside Docker, _ALX files are at /profiles/alx_work/ (mounted volume)
# On host, they're at ~/GrowDirect/_ALX/
ALX_DIR = os.getenv("ALX_WORK_DIR", "/profiles/alx_work")

# Max chars per memory chunk
MAX_CHUNK_CHARS = 6000

# File extensions we can ingest (text-based only)
INGESTIBLE_EXTENSIONS = {".md", ".yaml", ".yml", ".json", ".txt"}

# Skip these files/patterns
SKIP_PATTERNS = {
    ".DS_Store", ".obsidian", "__pycache__", ".tmp",
    "node_modules", ".git", "bolt.diy",
}

# Agent name mapping for deliverables
AGENT_ROLES = {
    "Art": "UX/Creative Director",
    "research": "Research Framework",
    "legal": "Legal Counsel",
    "eng": "Developer/Quant",
    "docs": "Documentation Lead",
    "qm": "QA Manager/CSM",
    "arch": "Systems Architect",
    "pm": "Program Manager",
    "Will": "Lead Generation",
    "Condor": "Multi-Agent Triangulation",
    "Triangulation": "Cross-Agent Synthesis",
    "ALX": "ALX — Chief of Staff/COO",
}


# ---------------------------------------------------------------------------
# Document categorization
# ---------------------------------------------------------------------------

def categorize_file(filepath: str) -> dict:
    """Determine category, agent, and description for a file."""
    rel = filepath.replace(ALX_DIR, "").lstrip("/")
    parts = rel.split("/")

    info = {
        "category": "operational",
        "agent": "ALX",
        "subcategory": "",
        "description": "",
    }

    # WorkOrders/output/<Agent>/...
    if "WorkOrders/output" in filepath:
        info["category"] = "deliverable"
        # Find agent name from path
        after_output = rel.split("WorkOrders/output/")[-1] if "WorkOrders/output/" in rel else ""
        agent_dir = after_output.split("/")[0] if "/" in after_output else after_output
        if agent_dir in AGENT_ROLES:
            info["agent"] = agent_dir
            info["description"] = AGENT_ROLES[agent_dir]

        # Sub-categorize
        fname = os.path.basename(filepath).lower()
        if "prd" in fname or "PRD" in os.path.basename(filepath):
            info["subcategory"] = "prd"
        elif "patent" in fname:
            info["subcategory"] = "patent"
        elif "qa" in fname or "uat" in fname or "gate" in fname:
            info["subcategory"] = "qa_report"
        elif "legal" in fname or "nda" in fname or "agreement" in fname or "waiver" in fname:
            info["subcategory"] = "legal"
        elif "swagger" in fname or "openapi" in fname:
            info["subcategory"] = "api_spec"
        elif "manifesto" in fname or "thesis" in fname or "position" in fname:
            info["subcategory"] = "research"
        elif "brief" in fname:
            info["subcategory"] = "brief"
        elif "investor" in fname:
            info["subcategory"] = "investor"
        else:
            info["subcategory"] = "deliverable"

    # WorkOrders/dispatches/...
    elif "WorkOrders/dispatches" in filepath:
        info["category"] = "dispatch"
        fname = os.path.basename(filepath)
        # Extract agent from filename (e.g., Jeremy_Sprint5_..._SessionPrompt.md)
        for agent in AGENT_ROLES:
            if fname.startswith(agent) or f"_{agent}_" in fname:
                info["agent"] = agent
                break

    # WorkOrders/captures/...
    elif "WorkOrders/captures" in filepath:
        info["category"] = "capture"
        info["agent"] = "Jeffe"
        info["description"] = "CEO directive capture"

    # WorkOrders/ root (work order files)
    elif "WorkOrders/" in filepath and "output" not in filepath and "dispatches" not in filepath:
        info["category"] = "work_order"
        fname = os.path.basename(filepath)
        for agent in AGENT_ROLES:
            if agent in fname:
                info["agent"] = agent
                break

    # WarChest/sources/...
    elif "WarChest/sources" in filepath:
        info["category"] = "war_chest"
        info["subcategory"] = "investor_source"
        info["description"] = "Investor briefing source content"

    # WarChest/ root
    elif "WarChest/" in filepath:
        info["category"] = "war_chest"
        fname = os.path.basename(filepath)
        if "manifest" in fname:
            info["subcategory"] = "build_config"
        elif "WORKING_PAPERS" in fname:
            info["subcategory"] = "ip_index"
        elif "SKILL" in fname:
            info["subcategory"] = "build_system"

    # Root operational files
    elif any(f in filepath for f in ["DISPATCH.md", "HANDOFF.md", "TRIAGE.md",
                                      "LINEAR_STAGING.md", "PROJECT_MANIFEST.md",
                                      "genesis.md"]):
        info["category"] = "operational"
        info["subcategory"] = "team_operations"

    # ALX.md profile
    elif "ALX.md" in filepath:
        info["category"] = "team_profile"
        info["agent"] = "ALX"

    return info


# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------

def discover_files(base_dir: str, category_filter: str = None) -> list:
    """Walk _ALX/ and find all ingestible files."""
    files = []

    for root, dirs, filenames in os.walk(base_dir):
        # Skip unwanted directories
        dirs[:] = [d for d in dirs if not any(skip in d for skip in SKIP_PATTERNS)]

        # Skip archive directories (too much duplicate content)
        if "archive" in root.split("/") or "sources_v2_archive" in root:
            continue

        # Skip site/ (rendered HTML, not source content)
        if "/WarChest/site/" in root:
            continue

        for fname in sorted(filenames):
            # Skip non-ingestible
            ext = os.path.splitext(fname)[1].lower()
            if ext not in INGESTIBLE_EXTENSIONS:
                continue

            # Skip patterns
            if any(skip in fname for skip in SKIP_PATTERNS):
                continue

            filepath = os.path.join(root, fname)
            info = categorize_file(filepath)

            # Apply category filter
            if category_filter and info["category"] != category_filter:
                continue

            info["filepath"] = filepath
            info["filename"] = fname
            info["size"] = os.path.getsize(filepath)
            files.append(info)

    return files


# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------

def read_file(filepath: str) -> str:
    """Read a text file."""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def chunk_document(filename: str, content: str, info: dict) -> list:
    """Split a document into section-based chunks with metadata prefix."""
    # Split on ## headings
    sections = re.split(r'(?=^## )', content, flags=re.MULTILINE)
    sections = [s.strip() for s in sections if s.strip()]

    if not sections:
        sections = [content]

    chunks = []
    current_chunk = ""

    for section in sections:
        if current_chunk and len(current_chunk) + len(section) > MAX_CHUNK_CHARS:
            chunks.append(current_chunk.strip())
            current_chunk = ""

        if len(section) > MAX_CHUNK_CHARS:
            # Split on ### headings
            subsections = re.split(r'(?=^### )', section, flags=re.MULTILINE)
            for sub in subsections:
                if len(current_chunk) + len(sub) > MAX_CHUNK_CHARS:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    # If single subsection is still too large, force-split
                    if len(sub) > MAX_CHUNK_CHARS:
                        for i in range(0, len(sub), MAX_CHUNK_CHARS):
                            chunks.append(sub[i:i + MAX_CHUNK_CHARS].strip())
                        current_chunk = ""
                    else:
                        current_chunk = sub
                else:
                    current_chunk += "\n\n" + sub
        else:
            current_chunk += "\n\n" + section

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    # Prefix each chunk with metadata
    prefixed = []
    cat_label = info["category"].upper().replace("_", " ")
    agent_label = AGENT_ROLES.get(info["agent"], info["agent"])

    for i, chunk in enumerate(chunks):
        prefix = (
            f"{cat_label}: {filename}\n"
            f"Agent: {agent_label}\n"
        )
        if info.get("subcategory"):
            prefix += f"Type: {info['subcategory']}\n"
        prefix += f"(Part {i + 1}/{len(chunks)})\n\n"
        prefixed.append(prefix + chunk)

    return prefixed


# ---------------------------------------------------------------------------
# Memory operations
# ---------------------------------------------------------------------------

def check_existing(filename: str) -> bool:
    """Check if this file is already in memory."""
    try:
        from canary.services.alx.memory import memory_recall
        result = memory_recall(f"DELIVERABLE: {filename}", limit=1, memory_type="work_product")
        matches = result.get("matches", [])
        return any(filename in m.get("content", "") for m in matches)
    except Exception:
        return False


def store_chunk(session_id: str, info: dict, chunk: str,
                chunk_num: int, total: int) -> dict:
    """Store a document chunk directly via Python API."""
    from canary.services.alx.memory import memory_store
    return memory_store(
        session_id=session_id,
        content=chunk,
        memory_type="work_product",
        metadata={
            "agent": info["agent"],
            "category": info["category"],
            "subcategory": info.get("subcategory", ""),
            "filename": info["filename"],
            "filepath": info["filepath"],
            "chunk": f"{chunk_num}/{total}",
            "gro_issue": "GRO-170",
        },
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Seed ALX memory with _ALX work products")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--category", type=str, help="Only ingest this category")
    parser.add_argument("--force", action="store_true", help="Skip duplicate check")
    parser.add_argument("--limit", type=int, default=0, help="Max files to process (0=all)")
    args = parser.parse_args()

    # Verify memory layer is available
    if not args.dry_run:
        try:
            from canary.services.alx.memory import memory_healthy
            if not memory_healthy():
                print("ERROR: ALX memory database not reachable")
                sys.exit(1)
            print("ALX memory healthy")
        except Exception as e:
            print(f"ERROR: Cannot initialize ALX memory: {e}")
            sys.exit(1)

    # Add work_product to allowed memory types if needed
    if not args.dry_run:
        try:
            from canary.db.session_factory import get_session
            from sqlalchemy import text
            db = get_session()
            # Check if work_product is in the constraint
            result = db.execute(text("""
                SELECT conname, consrc FROM pg_constraint
                WHERE conname = 'alx_memories_memory_type_check'
            """)).fetchone()
            if result and "work_product" not in str(result):
                db.execute(text("""
                    ALTER TABLE alx_memories DROP CONSTRAINT IF EXISTS alx_memories_memory_type_check
                """))
                db.execute(text("""
                    ALTER TABLE alx_memories ADD CONSTRAINT alx_memories_memory_type_check
                    CHECK (memory_type = ANY (ARRAY[
                        'decision', 'finding', 'context', 'architecture',
                        'session_summary', 'procedure', 'team_profile', 'work_product'
                    ]))
                """))
                db.commit()
                print("Added 'work_product' to memory_type constraint")
        except Exception as e:
            print(f"WARNING: Could not update constraint: {e}")
            try:
                db.rollback()
            except Exception:
                pass

    # Discover files
    print(f"\nScanning: {ALX_DIR}")
    files = discover_files(ALX_DIR, category_filter=args.category)
    print(f"Found {len(files)} ingestible files")

    if args.limit:
        files = files[:args.limit]
        print(f"  (limited to {args.limit})")

    # Group by category for reporting
    by_category = {}
    for f in files:
        cat = f["category"]
        by_category.setdefault(cat, []).append(f)

    print("\nBy category:")
    for cat, items in sorted(by_category.items()):
        total_size = sum(i["size"] for i in items)
        print(f"  {cat}: {len(items)} files ({total_size:,} bytes)")

    session_id = f"seed-work-products-{int(time.time())}"
    total_chunks = 0
    total_skipped = 0
    total_errors = 0

    for i, info in enumerate(files):
        filepath = info["filepath"]
        filename = info["filename"]

        if not args.force and not args.dry_run:
            if check_existing(filename):
                total_skipped += 1
                continue

        try:
            content = read_file(filepath)
        except Exception as e:
            print(f"  ERROR reading {filename}: {e}")
            total_errors += 1
            continue

        if not content.strip():
            continue

        chunks = chunk_document(filename, content, info)

        if args.dry_run:
            print(f"  [{info['category']}] {filename}: {len(content):,} chars → {len(chunks)} chunks ({info['agent']})")
            continue

        # Progress every 10 files
        if (i + 1) % 10 == 0:
            print(f"  Progress: {i + 1}/{len(files)} files...")

        for j, chunk in enumerate(chunks):
            try:
                result = store_chunk(session_id, info, chunk, j + 1, len(chunks))
                mid = result.get("memory_id", "?")[:8]
                total_chunks += 1
            except Exception as e:
                print(f"  ERROR storing {filename} chunk {j + 1}: {e}")
                total_errors += 1
            time.sleep(0.1)  # Gentle on the DB

    print(f"\n{'DRY RUN — ' if args.dry_run else ''}Done.")
    print(f"  Files processed: {len(files)}")
    print(f"  Chunks stored: {total_chunks}")
    print(f"  Skipped (existing): {total_skipped}")
    print(f"  Errors: {total_errors}")
    if total_chunks > 0 and not args.dry_run:
        print(f"  Cognee enrichment running in background")
        print(f"  Session: {session_id}")


if __name__ == "__main__":
    main()
