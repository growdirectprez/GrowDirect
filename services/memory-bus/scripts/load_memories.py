#!/usr/bin/env python3
"""ALX Memory Loader — seed the knowledge graph from project documents.

Reads markdown files, chunks by section headers, deduplicates, and stores
each chunk via the ALX memory_store API. Tier 1 (PostgreSQL) stores are
immediate. Tier 2 (Cognee) enrichment runs in background (fire-and-forget).

Usage:
    python3 devops/scripts/load_memories.py [--tier A|B|all] [--dry-run] [--delay 2]

Options:
    --tier A       Only load Tier A (operational core) documents
    --tier B       Only load Tier B (specs/strategy) documents
    --tier all     Load everything (default)
    --dry-run      Show what would be loaded without calling the API
    --delay N      Seconds between API calls (default: 2)
    --base-url URL API base URL (default: http://localhost:5001)

Linear: GRO-165
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import requests
except ImportError:
    print("ERROR: requests library required. Run: pip3 install requests")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Document manifest — two tiers
# ---------------------------------------------------------------------------

# Tier A: Operational core — critical for daily ALX work.
# These get loaded first and inform every session's context assembly.
TIER_A: List[Dict] = [
    # CLAUDE.md files — the operating instructions
    {
        "path": "~/GrowDirect/Canary/CLAUDE.md",
        "memory_type": "architecture",
        "tags": ["operations", "dev-environment", "coding-standards"],
        "description": "Canary CLAUDE.md — dev environment, architecture, coding standards",
    },
    {
        "path": "~/GrowDirect/CLAUDE.md",
        "memory_type": "architecture",
        "tags": ["operations", "growdirect", "team"],
        "description": "GrowDirect CLAUDE.md — parent org operations and team",
    },
    # Product core
    {
        "path": "~/GrowDirect/docs/extracted/Canary_Product_Blueprint_v1.0.md",
        "memory_type": "architecture",
        "tags": ["product", "blueprint", "core"],
        "description": "Product Blueprint — the what and why of Canary LP",
    },
    {
        "path": "~/GrowDirect/docs/extracted/Canary_HealthCheck_ProductBrief_v1.0.md",
        "memory_type": "architecture",
        "tags": ["product", "health-check", "gtm", "lead-product"],
        "description": "HealthCheck Product Brief — the lead product, GTM strategy",
    },
    {
        "path": "~/GrowDirect/docs/extracted/Canary_Platform_Roadmap_v1.0.md",
        "memory_type": "architecture",
        "tags": ["product", "roadmap", "phases"],
        "description": "Platform Roadmap — phased delivery plan",
    },
    {
        "path": "~/GrowDirect/docs/extracted/Owl_MemoryLayer_Architecture_v1.0.md",
        "memory_type": "architecture",
        "tags": ["owl", "memory", "ai", "architecture"],
        "description": "Owl Memory Layer Architecture — AI memory design",
    },
    {
        "path": "~/GrowDirect/docs/extracted/PRD_Owl_Search_v1.0.md",
        "memory_type": "architecture",
        "tags": ["owl", "search", "prd"],
        "description": "PRD Owl Search — search feature requirements",
    },
    # Infrastructure
    {
        "path": "~/GrowDirect/Canary/docs/infra/lab_network.md",
        "memory_type": "architecture",
        "tags": ["infra", "network", "topology"],
        "description": "Lab Network — device inventory and topology",
    },
    {
        "path": "~/GrowDirect/Canary/docs/infra/deployment_pipeline.md",
        "memory_type": "architecture",
        "tags": ["infra", "deployment", "pipeline"],
        "description": "Deployment Pipeline — scripts, SSH, test gates, tunnels",
    },
    {
        "path": "~/GrowDirect/Canary/docs/infra/infra_roadmap.md",
        "memory_type": "architecture",
        "tags": ["infra", "roadmap", "cloud"],
        "description": "Infrastructure Roadmap — 4-phase plan",
    },
    # Work orders (active context)
    {
        "path": "~/GrowDirect/Canary/docs/workorders/DISPATCH_GRO-165_ALX_MEMORY_BOOTSTRAP.md",
        "memory_type": "context",
        "tags": ["workorder", "GRO-165", "alx", "memory"],
        "description": "GRO-165 Dispatch — ALX memory bootstrap work order",
    },
    {
        "path": "~/GrowDirect/Canary/docs/workorders/OWL_MEMORY_DISPATCH.md",
        "memory_type": "context",
        "tags": ["workorder", "owl", "memory"],
        "description": "Owl Memory Dispatch — Owl memory layer work order",
    },
    {
        "path": "~/GrowDirect/Canary/docs/workorders/GRO-162.md",
        "memory_type": "context",
        "tags": ["workorder", "GRO-162"],
        "description": "GRO-162 — ops dashboard work order",
    },
    # Product Guide (comprehensive reference)
    {
        "path": "~/GrowDirect/docs/extracted/Canary_Product_Guide_v1.0.md",
        "memory_type": "architecture",
        "tags": ["product", "guide", "reference"],
        "description": "Product Guide — comprehensive Canary LP reference",
    },
    # Integration prep
    {
        "path": "~/GrowDirect/docs/extracted/Canary_Integration_Prep_Plan_v1.0.md",
        "memory_type": "context",
        "tags": ["integration", "square", "prep"],
        "description": "Integration Prep Plan — Square integration readiness",
    },
]

# Tier B: Specs and strategy — background context, lower priority.
# Loaded after Tier A. Enrichment runs overnight.
TIER_B: List[Dict] = [
    # Core data model — chunked (these have actionable schema sections)
    {
        "path": "~/GrowDirect/Canary_IP/Markdown/Specs/CRDM_v1.0.md",
        "memory_type": "architecture",
        "tags": ["spec", "crdm", "data-model"],
        "description": "CRDM v1.0 — Canary Reference Data Model",
        "strategy": "sections",
    },
    {
        "path": "~/GrowDirect/Canary_IP/Markdown/Specs/Fox_Data_Model_v2.0_GSLM_Enhanced.md",
        "memory_type": "architecture",
        "tags": ["spec", "fox", "data-model", "case-management"],
        "description": "Fox Data Model v2.0 — case management schema",
        "strategy": "sections",
    },
    # Large reference docs — overview only (first ~6KB captures TOC + key concepts)
    {
        "path": "~/GrowDirect/Canary_IP/Markdown/Specs/Canary_Technical_Requirements_v1.0.md",
        "memory_type": "architecture",
        "tags": ["spec", "requirements", "technical"],
        "description": "Technical Requirements — system requirements spec",
        "strategy": "overview",
    },
    {
        "path": "~/GrowDirect/Canary_IP/Markdown/Specs/Canary_Functional_Requirements_v1.0.md",
        "memory_type": "architecture",
        "tags": ["spec", "requirements", "functional"],
        "description": "Functional Requirements — feature requirements",
        "strategy": "overview",
    },
    {
        "path": "~/GrowDirect/Canary_IP/Markdown/Specs/Canary_Technology_Blueprint_v1.0.md",
        "memory_type": "architecture",
        "tags": ["spec", "technology", "blueprint"],
        "description": "Technology Blueprint — tech stack decisions",
        "strategy": "overview",
    },
    {
        "path": "~/GrowDirect/Canary_IP/Markdown/Specs/elJeffe_Protocol_Spec_v1.0.md",
        "memory_type": "architecture",
        "tags": ["spec", "eljeffe", "protocol", "raas"],
        "description": "elJeffe Protocol — platform protocol specification",
        "strategy": "overview",
    },
    {
        "path": "~/GrowDirect/Canary_IP/Markdown/Specs/GrowDirect_Unified_Data_Model_v1.0.md",
        "memory_type": "architecture",
        "tags": ["spec", "data-model", "unified"],
        "description": "Unified Data Model — cross-system data architecture",
        "strategy": "overview",
    },
    {
        "path": "~/GrowDirect/Canary_IP/Markdown/Specs/Multi_POS_Translation_Layer_Architecture_v1.0.md",
        "memory_type": "architecture",
        "tags": ["spec", "multi-pos", "translation", "integration"],
        "description": "Multi-POS Translation Layer — POS adapter architecture",
        "strategy": "overview",
    },
    # Smaller specs — store whole
    {
        "path": "~/GrowDirect/Canary_IP/Markdown/Specs/Canary_Coding_Standards_v1.0.md",
        "memory_type": "architecture",
        "tags": ["spec", "coding-standards"],
        "description": "Coding Standards — development guidelines",
    },
    {
        "path": "~/GrowDirect/Canary_IP/Markdown/Specs/Implementation_Spec_Jeremy.md",
        "memory_type": "architecture",
        "tags": ["spec", "implementation"],
        "description": "Implementation Spec — developer implementation guide",
        "strategy": "overview",
    },
    # Strategy — overview only for large docs, full for small ones
    {
        "path": "~/GrowDirect/Canary_IP/Markdown/Strategy/Canary_Strategic_Thesis_v1.0.md",
        "memory_type": "context",
        "tags": ["strategy", "thesis", "vision"],
        "description": "Strategic Thesis — market thesis and positioning",
        "strategy": "overview",
    },
    {
        "path": "~/GrowDirect/Canary_IP/Markdown/Strategy/GrowDirect_Manifesto_v1.0.md",
        "memory_type": "context",
        "tags": ["strategy", "manifesto", "philosophy"],
        "description": "GrowDirect Manifesto — founding philosophy",
        "strategy": "overview",
    },
    {
        "path": "~/GrowDirect/Canary_IP/Markdown/Strategy/Canary_Factory_Process_v1.0.md",
        "memory_type": "architecture",
        "tags": ["strategy", "factory-process", "operations"],
        "description": "Factory Process — how we build and ship",
        "strategy": "overview",
    },
    {
        "path": "~/GrowDirect/Canary_IP/Markdown/Strategy/Canary_Data_Strategy_NorthStar_v1.0.md",
        "memory_type": "context",
        "tags": ["strategy", "data", "north-star"],
        "description": "Data Strategy North Star — data architecture vision",
        "strategy": "overview",
    },
    {
        "path": "~/GrowDirect/Canary_IP/Markdown/Strategy/PRODUCTION_CHAIN_v0.1.md",
        "memory_type": "architecture",
        "tags": ["strategy", "production-chain"],
        "description": "Production Chain — build pipeline design",
    },
    {
        "path": "~/GrowDirect/Canary_IP/Markdown/Strategy/PITCH_SPINE_v0.4.md",
        "memory_type": "context",
        "tags": ["strategy", "pitch", "narrative"],
        "description": "Pitch Spine — investor/customer narrative",
    },
    # Code review (remediation baseline) — overview, not every finding
    {
        "path": "~/GrowDirect/docs/extracted/Canary_Code_Review_2026-03-01.md",
        "memory_type": "finding",
        "tags": ["code-review", "findings", "remediation"],
        "description": "Code Review March 1 — 53 findings, remediation baseline",
        "strategy": "overview",
    },
    # Ops Dashboard spec
    {
        "path": "~/GrowDirect/docs/extracted/Canary_Ops_Dashboard_Spec_v1.0.md",
        "memory_type": "architecture",
        "tags": ["spec", "ops-dashboard", "monitoring"],
        "description": "Ops Dashboard Spec — monitoring and operations UI",
    },
]

# Files to explicitly skip (duplicates or stubs)
SKIP_FILES = {
    # Academic Research Paper = UNIVERSAL EVENT NOTARIZATION (same content)
    "UNIVERSAL EVENT NOTARIZATION.md",
    "GrowDirect_AcademicResearchPaper_v1.0.md",
    # Stub files (< 200 bytes)
    "Sprint_Plan_Admin_Module.md",
    "MVP_Scope_Review.md",
    "Canary_Document_Inventory_2026-02-19_v1_0.md",
    # CRDM duplicates (we load the canonical v1.0)
    "CRDM_v1.1_Addendum_Namespace_DeviceAttestation_SourceSystems.md",
    "Tom_CRDM_Schema_Review_2026-02-20.md",
    "CRDM_Gap_Analysis_2026-02-20.md",
    # Correction/delta docs (fold into parent or skip)
    "Canary_Technology_Blueprint_v1.1_Corrections.md",
}


# ---------------------------------------------------------------------------
# Markdown chunker
# ---------------------------------------------------------------------------

def chunk_markdown(
    text: str,
    source_file: str,
    max_chunk: int = 6000,
    min_chunk: int = 300,
    whole_doc_threshold: int = 8000,
) -> List[Dict]:
    """Split markdown into logical chunks by ## headers.

    Returns list of dicts with keys: title, content, section_index.

    Strategy:
    - Docs under whole_doc_threshold → stored as one memory (no splitting)
    - Split on ## (h2) headers — these represent logical sections
    - Adjacent small sections (< min_chunk) get merged together
    - Sections over max_chunk get split on ### (h3) sub-headers
    - Minimum chunk size: min_chunk chars (skip empty/tiny sections)
    """
    # Small docs: store whole — more coherent for entity extraction
    if len(text) <= whole_doc_threshold:
        title_match = re.match(r'^#\s+(.+)', text)
        title = title_match.group(1).strip() if title_match else Path(source_file).stem
        return [{"title": title, "content": text.strip(), "section_index": 0}]

    raw_chunks = []

    # Split on ## headers (keep the header with its content)
    h2_pattern = re.compile(r'^## ', re.MULTILINE)
    parts = h2_pattern.split(text)

    # First part is content before any ## (doc title, intro)
    intro = parts[0].strip()
    if len(intro) > min_chunk:
        title_match = re.match(r'^#\s+(.+)', intro)
        title = title_match.group(1).strip() if title_match else Path(source_file).stem
        raw_chunks.append({
            "title": title,
            "content": intro,
            "section_index": 0,
        })

    # Remaining parts are ## sections
    for i, part in enumerate(parts[1:], start=1):
        lines = part.split('\n', 1)
        section_title = lines[0].strip().rstrip('#').strip()
        section_body = lines[1].strip() if len(lines) > 1 else ""
        full_section = f"## {section_title}\n\n{section_body}".strip()

        if len(full_section) < 80:
            continue  # Skip near-empty sections

        if len(full_section) <= max_chunk:
            raw_chunks.append({
                "title": section_title,
                "content": full_section,
                "section_index": i,
            })
        else:
            # Split large sections on ### sub-headers, then merge small pieces
            sub_chunks = _split_on_h3(section_title, section_body, max_chunk, min_chunk)
            for sc in sub_chunks:
                sc["section_index"] = i
                raw_chunks.append(sc)

    # Merge adjacent small chunks to reduce total count
    return _merge_small_chunks(raw_chunks, min_chunk, max_chunk)


def _split_on_h3(parent_title: str, body: str, max_chunk: int, min_chunk: int) -> List[Dict]:
    """Split a large section by ### sub-headers."""
    h3_pattern = re.compile(r'^### ', re.MULTILINE)
    parts = h3_pattern.split(body)
    chunks = []

    # Intro before any ###
    intro = parts[0].strip()
    if len(intro) > min_chunk:
        chunks.append({
            "title": parent_title,
            "content": f"## {parent_title}\n\n{intro}",
        })

    for part in parts[1:]:
        lines = part.split('\n', 1)
        sub_title = lines[0].strip().rstrip('#').strip()
        sub_body = lines[1].strip() if len(lines) > 1 else ""
        full = f"### {sub_title}\n\n{sub_body}".strip()

        if len(full) < 80:
            continue

        if len(full) <= max_chunk:
            chunks.append({
                "title": f"{parent_title} > {sub_title}",
                "content": full,
            })
        else:
            # Hard split at paragraph boundaries
            paragraphs = re.split(r'\n\n+', full)
            current = ""
            chunk_num = 1
            for para in paragraphs:
                if len(current) + len(para) + 2 > max_chunk and current:
                    chunks.append({
                        "title": f"{parent_title} > {sub_title} (part {chunk_num})",
                        "content": current.strip(),
                    })
                    chunk_num += 1
                    current = para
                else:
                    current = f"{current}\n\n{para}" if current else para
            if current.strip() and len(current.strip()) > min_chunk:
                chunks.append({
                    "title": f"{parent_title} > {sub_title} (part {chunk_num})",
                    "content": current.strip(),
                })

    return chunks


def _merge_small_chunks(chunks: List[Dict], min_size: int, max_size: int) -> List[Dict]:
    """Merge adjacent small chunks to reduce total count.

    Two adjacent chunks both under min_size get combined if the result
    stays under max_size.
    """
    if not chunks:
        return chunks

    merged = [chunks[0]]
    for chunk in chunks[1:]:
        prev = merged[-1]
        combined_len = len(prev["content"]) + len(chunk["content"]) + 4

        # Merge if both are small and result fits
        if (len(prev["content"]) < min_size or len(chunk["content"]) < min_size) \
                and combined_len <= max_size:
            merged[-1] = {
                "title": f"{prev['title']} + {chunk['title']}",
                "content": f"{prev['content']}\n\n{chunk['content']}",
                "section_index": prev.get("section_index", 0),
            }
        else:
            merged.append(chunk)

    return merged


# ---------------------------------------------------------------------------
# Dedup engine
# ---------------------------------------------------------------------------

def content_hash(text: str) -> str:
    """SHA-256 hash of normalized content for dedup."""
    # Normalize whitespace for comparison
    normalized = re.sub(r'\s+', ' ', text.strip().lower())
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# API client
# ---------------------------------------------------------------------------

def store_memory(
    base_url: str,
    session_id: str,
    content: str,
    memory_type: str,
    metadata: Dict,
    dry_run: bool = False,
) -> Optional[Dict]:
    """Call the ALX memory_store API."""
    if dry_run:
        return {"dry_run": True, "stored": True, "memory_id": "dry-run"}

    url = f"{base_url}/alx/tools/memory_store"
    payload = {
        "params": {
            "content": content,
            "memory_type": memory_type,
            "session_id": session_id,
            "metadata": metadata,
        },
    }

    for attempt in range(3):
        try:
            resp = requests.post(url, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            if data.get("ok"):
                return data.get("result", {})
            else:
                print(f"  ERROR: {data.get('error', 'unknown')}")
                return None
        except requests.RequestException as e:
            if attempt < 2:
                wait = (attempt + 1) * 5
                print(f"  RETRY ({attempt+1}/3): {e} — waiting {wait}s")
                time.sleep(wait)
            else:
                print(f"  API ERROR: {e}")
                return None


def start_loader_session(base_url: str, dry_run: bool = False) -> str:
    """Generate a loader session ID.

    Uses a deterministic session ID (not the session_start API) to avoid
    blocking on Cognee context assembly during bulk loads.
    """
    if dry_run:
        return "loader-dry-run"

    # Verify the API is reachable before starting
    try:
        resp = requests.get(f"{base_url}/alx/health", timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if not data.get("healthy"):
            print(f"ERROR: ALX memory layer unhealthy: {data}")
            sys.exit(1)
    except requests.RequestException as e:
        print(f"ERROR: Cannot reach ALX API at {base_url}: {e}")
        print("Is the Flask container running? Try: curl http://localhost:5001/health")
        sys.exit(1)

    # Generate session ID directly — avoids slow session_start context assembly
    from datetime import datetime, timezone
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"alx-loader-{ts}"


# ---------------------------------------------------------------------------
# Main loader
# ---------------------------------------------------------------------------

def load_tier(
    manifest: List[Dict],
    tier_name: str,
    base_url: str,
    session_id: str,
    delay: float,
    dry_run: bool,
    seen_hashes: set,
) -> Tuple[int, int, int]:
    """Load a tier of documents. Returns (stored, skipped, errors)."""
    stored = 0
    skipped = 0
    errors = 0

    print(f"\n{'='*60}")
    print(f"Loading Tier {tier_name}: {len(manifest)} documents")
    print(f"{'='*60}")

    for doc_idx, doc in enumerate(manifest, 1):
        path = Path(os.path.expanduser(doc["path"]))
        print(f"\n[{doc_idx}/{len(manifest)}] {doc['description']}")
        print(f"  File: {path}")

        if not path.exists():
            print(f"  SKIP: file not found")
            skipped += 1
            continue

        if path.name in SKIP_FILES:
            print(f"  SKIP: in skip list")
            skipped += 1
            continue

        # Read and chunk
        text = path.read_text(encoding="utf-8", errors="replace")
        if len(text) < 100:
            print(f"  SKIP: too small ({len(text)} bytes)")
            skipped += 1
            continue

        strategy = doc.get("strategy", "sections")
        if strategy == "overview":
            # Store just the first ~6KB as a single overview memory.
            # Captures title, TOC, intro, and key concepts without
            # generating dozens of sub-chunks from deep structure.
            overview = text[:6000].strip()
            # Don't cut mid-sentence — find last paragraph break
            last_break = overview.rfind('\n\n')
            if last_break > 3000:
                overview = overview[:last_break].strip()
            title_match = re.match(r'^#\s+(.+)', overview)
            title = title_match.group(1).strip() if title_match else path.stem
            chunks = [{"title": title, "content": overview, "section_index": 0}]
        else:
            chunks = chunk_markdown(text, str(path))
        print(f"  Chunks: {len(chunks)} sections ({len(text):,} bytes)")

        for chunk_idx, chunk in enumerate(chunks, 1):
            ch = content_hash(chunk["content"])
            if ch in seen_hashes:
                print(f"    [{chunk_idx}/{len(chunks)}] DEDUP: {chunk['title'][:50]}")
                skipped += 1
                continue
            seen_hashes.add(ch)

            metadata = {
                "source_file": str(path),
                "source_doc": doc["description"],
                "section_title": chunk["title"],
                "section_index": chunk.get("section_index", 0),
                "tags": doc.get("tags", []),
                "loader": "load_memories.py",
                "tier": tier_name,
                "content_hash": ch,
            }

            gro_tags = [t for t in doc.get("tags", []) if t.startswith("GRO-")]
            if gro_tags:
                metadata["gro_issue"] = gro_tags[0]

            result = store_memory(
                base_url=base_url,
                session_id=session_id,
                content=chunk["content"],
                memory_type=doc["memory_type"],
                metadata=metadata,
                dry_run=dry_run,
            )

            if result and result.get("stored"):
                status = "PENDING" if result.get("cognee_enriched") == "pending" else "T1"
                mid = result.get("memory_id", "?")[:8]
                print(f"    [{chunk_idx}/{len(chunks)}] {status} {mid} | {chunk['title'][:50]}")
                stored += 1
            else:
                print(f"    [{chunk_idx}/{len(chunks)}] FAIL | {chunk['title'][:50]}")
                errors += 1

            if not dry_run and delay > 0:
                time.sleep(delay)

    return stored, skipped, errors


def main():
    parser = argparse.ArgumentParser(description="ALX Memory Loader — seed the knowledge graph")
    parser.add_argument("--tier", choices=["A", "B", "all"], default="all",
                        help="Which tier to load (default: all)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be loaded without calling API")
    parser.add_argument("--delay", type=float, default=2.0,
                        help="Seconds between API calls (default: 2)")
    parser.add_argument("--base-url", default="http://localhost:5001",
                        help="ALX API base URL (default: http://localhost:5001)")
    args = parser.parse_args()

    print("=" * 60)
    print("ALX Memory Loader — GRO-165")
    print("=" * 60)
    print(f"  Tier:     {args.tier}")
    print(f"  Dry run:  {args.dry_run}")
    print(f"  Delay:    {args.delay}s between stores")
    print(f"  API:      {args.base_url}")

    # Determine manifest
    manifests = []
    if args.tier in ("A", "all"):
        manifests.append(("A", TIER_A))
    if args.tier in ("B", "all"):
        manifests.append(("B", TIER_B))

    total_docs = sum(len(m) for _, m in manifests)
    print(f"  Documents: {total_docs}")

    # Start session
    session_id = start_loader_session(args.base_url, args.dry_run)
    print(f"  Session:  {session_id}")
    print()

    # Track dedup across tiers
    seen_hashes = set()
    total_stored = 0
    total_skipped = 0
    total_errors = 0

    for tier_name, manifest in manifests:
        s, sk, e = load_tier(
            manifest, tier_name, args.base_url, session_id,
            args.delay, args.dry_run, seen_hashes,
        )
        total_stored += s
        total_skipped += sk
        total_errors += e

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"  Stored:     {total_stored}")
    print(f"  Skipped:    {total_skipped} (dedup + missing + too small)")
    print(f"  Errors:     {total_errors}")
    print(f"  Session:    {session_id}")

    if total_stored > 0 and not args.dry_run:
        est_minutes = total_stored * 4
        est_hours = est_minutes / 60
        print(f"\n  Cognee enrichment: ~{total_stored} background tasks")
        print(f"  Estimated time:    ~{est_hours:.1f} hours ({est_minutes} min)")
        print(f"  Status: fire-and-forget — check Flask logs for progress")
        print(f"    docker compose -f devops/docker-compose.localhost.yml logs flask | grep cognee-enrich")

    if args.dry_run:
        print(f"\n  DRY RUN — no API calls made. Remove --dry-run to execute.")


if __name__ == "__main__":
    main()
