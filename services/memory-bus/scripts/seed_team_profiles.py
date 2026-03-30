#!/usr/bin/env python3
"""GRO-170: Seed ALX Cognee memory with team profiles.

Reads team profile .md files from Company/Team/ and _ALX/ALX.md,
chunks them into digestible sections, and stores directly via the
ALX memory_store Python API (bypasses HTTP/JWT — this is an admin script).

Cognee enrichment fires automatically in the background for each chunk.

Idempotent: checks for existing team_profile memories before inserting.

Usage (run inside Docker container):
    python devops/scripts/seed_team_profiles.py [--dry-run] [--agent NAME]

Or from host (profile files mounted):
    docker compose -f devops/docker-compose.localhost.yml exec flask \
        python devops/scripts/seed_team_profiles.py
"""

import argparse
import json
import os
import re
import sys
import time

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

# Inside Docker, profiles are at /profiles/ (mounted volume)
# On host, they're at ~/GrowDirect/Company/Team/
TEAM_DIR = os.getenv("TEAM_PROFILES_DIR", "/profiles/team")
ALX_PROFILE = os.getenv("ALX_PROFILE_PATH", "/profiles/alx/ALX.md")

# Max chars per memory chunk. Cognee handles ~2000 tokens well.
MAX_CHUNK_CHARS = 6000

def _discover_agents(team_dir: str) -> list:
    """Discover agent profiles from the team directory."""
    if not os.path.isdir(team_dir):
        return []
    return sorted(
        os.path.splitext(f)[0]
        for f in os.listdir(team_dir)
        if f.endswith(".md")
    )


CORE_AGENTS = []  # populated at runtime from directory listing


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read_profile(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def _extract_role(content: str) -> str:
    """Extract role from profile frontmatter (first **Role:** line or header)."""
    m = re.search(r'\*\*Role:\*\*\s*(.+)', content)
    if m:
        return m.group(1).strip()
    # Fallback: first line after the heading
    m = re.search(r'^#\s+.+\n+\*\*(.+?)\*\*', content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return "Team Member"


def chunk_profile(name: str, content: str) -> list:
    """Split a profile into section-based chunks."""
    sections = re.split(r'(?=^## )', content, flags=re.MULTILINE)
    sections = [s.strip() for s in sections if s.strip()]

    chunks = []
    current_chunk = ""

    for section in sections:
        if current_chunk and len(current_chunk) + len(section) > MAX_CHUNK_CHARS:
            chunks.append(current_chunk.strip())
            current_chunk = ""

        if len(section) > MAX_CHUNK_CHARS:
            subsections = re.split(r'(?=^### )', section, flags=re.MULTILINE)
            for sub in subsections:
                if len(current_chunk) + len(sub) > MAX_CHUNK_CHARS:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = sub
                else:
                    current_chunk += "\n\n" + sub
        else:
            current_chunk += "\n\n" + section

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    prefixed = []
    for i, chunk in enumerate(chunks):
        role = _extract_role(content)
        prefix = f"TEAM PROFILE: {name} — {role}\n(Part {i+1}/{len(chunks)})\n\n"
        prefixed.append(prefix + chunk)

    return prefixed


def check_existing(agent_name: str) -> bool:
    """Check if this agent's profile is already in memory (Tier 1 PostgreSQL)."""
    try:
        from canary.services.alx.memory import memory_recall
        result = memory_recall(f"TEAM PROFILE: {agent_name}", limit=1, memory_type="team_profile")
        matches = result.get("matches", [])
        return any(agent_name in m.get("content", "") for m in matches)
    except Exception:
        return False


def store_chunk(session_id: str, agent_name: str, chunk: str, chunk_num: int, total: int) -> dict:
    """Store a profile chunk directly via Python API."""
    from canary.services.alx.memory import memory_store
    return memory_store(
        session_id=session_id,
        content=chunk,
        memory_type="team_profile",
        metadata={
            "agent_name": agent_name,
            "role": "Team Member",  # role extracted from profile frontmatter at chunk time
            "chunk": f"{chunk_num}/{total}",
            "source": f"Company/Team/{agent_name}.md",
            "gro_issue": "GRO-170",
        },
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Seed ALX memory with team profiles")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--agent", type=str, help="Ingest only this agent")
    parser.add_argument("--all", action="store_true", help="Include non-core agents")
    parser.add_argument("--force", action="store_true", help="Skip duplicate check")
    args = parser.parse_args()

    # Verify memory layer is available
    if not args.dry_run:
        try:
            from canary.services.alx.memory import memory_healthy, cognee_available
            if not memory_healthy():
                print("ERROR: ALX memory database not reachable")
                sys.exit(1)
            cognee_ok = cognee_available()
            print(f"ALX memory healthy — Cognee: {'active' if cognee_ok else 'inactive'}")
        except Exception as e:
            print(f"ERROR: Cannot initialize ALX memory: {e}")
            sys.exit(1)

    # Build file list
    if args.agent:
        agents_to_ingest = [args.agent]
    elif args.all:
        agents_to_ingest = []
        if os.path.isdir(TEAM_DIR):
            for f in sorted(os.listdir(TEAM_DIR)):
                if f.endswith(".md"):
                    agents_to_ingest.append(f.replace(".md", ""))
        agents_to_ingest.append("ALX")
    else:
        agents_to_ingest = _discover_agents(TEAM_DIR)
        if os.path.exists(ALX_PROFILE):
            agents_to_ingest.append("ALX")

    print(f"\nAgents to ingest: {', '.join(agents_to_ingest)}")
    print(f"Team dir: {TEAM_DIR}")
    print(f"ALX profile: {ALX_PROFILE}")

    session_id = f"seed-team-profiles-{int(time.time())}"
    total_chunks = 0
    total_skipped = 0

    for agent_name in agents_to_ingest:
        if agent_name == "ALX":
            filepath = ALX_PROFILE
        else:
            filepath = os.path.join(TEAM_DIR, f"{agent_name}.md")

        if not os.path.exists(filepath):
            print(f"  SKIP {agent_name} — file not found: {filepath}")
            continue

        if not args.force and not args.dry_run and check_existing(agent_name):
            print(f"  SKIP {agent_name} — already in memory (use --force to re-ingest)")
            total_skipped += 1
            continue

        content = read_profile(filepath)
        chunks = chunk_profile(agent_name, content)
        print(f"\n  {agent_name}: {len(content):,} chars → {len(chunks)} chunks")

        if args.dry_run:
            for i, chunk in enumerate(chunks):
                print(f"    Chunk {i+1}: {len(chunk):,} chars — {chunk[:80]}...")
            continue

        for i, chunk in enumerate(chunks):
            result = store_chunk(session_id, agent_name, chunk, i + 1, len(chunks))
            mid = result.get("memory_id", "?")[:8]
            cognee = result.get("cognee_enriched", False)
            print(f"    Chunk {i+1}/{len(chunks)}: stored ({mid}...) cognee={cognee}")
            total_chunks += 1
            time.sleep(0.3)

    print(f"\n{'DRY RUN — ' if args.dry_run else ''}Done.")
    print(f"  Stored: {total_chunks} chunks")
    print(f"  Skipped: {total_skipped} agents (already in memory)")
    if total_chunks > 0 and not args.dry_run:
        print(f"  Cognee enrichment running in background (~3-5 min per chunk)")
        print(f"  Session: {session_id}")


if __name__ == "__main__":
    main()
