#!/usr/bin/env python3
"""Reseed ALX Tier 1 memory from the ground up.

Clean slate. Seeds in priority order:
  1. Foundational process maps (STPL, Tesco TOM, IBM Retail BI → Canary mappings)
  2. Architectural SDDs (057-060)
  3. All SDDs (001-056)
  4. Team profiles
  5. Curated work products (deliverables, work orders — skip dispatches/noise)

Skips raw extractions (OM_MAP_v24.md, RETAIL_BI_SOLUTION_V7.md, etc.) — only
the Canary mapping/index documents that synthesize raw source into actionable
architecture knowledge.

Usage (inside Docker container):
    python devops/scripts/seed_memory_foundation.py [--dry-run] [--no-truncate]

Or from host:
    docker compose -f devops/docker-compose.localhost.yml exec flask \
        python devops/scripts/seed_memory_foundation.py --dry-run
"""

import argparse
import os
import re
import sys
import time

# Ensure /app (container workdir) is on Python path for canary imports
if "/app" not in sys.path:
    sys.path.insert(0, "/app")

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

MAX_CHUNK_CHARS = 6000
SESSION_ID = f"seed-foundation-{int(time.time())}"

# All allowed memory types (superset)
ALL_MEMORY_TYPES = [
    "decision", "finding", "context", "architecture",
    "session_summary", "procedure", "team_profile",
    "work_product", "context_block", "foundation",
]

# ---------------------------------------------------------------------------
# Document manifest — ordered by priority
# ---------------------------------------------------------------------------

# Priority 1: Foundational process maps (the "why" behind every detection rule)
FOUNDATION_DOCS = [
    {
        "path": "/app/docs/sources/stpl_lv2/CANARY_PROCESS_MAP.md",
        "memory_type": "foundation",
        "metadata": {
            "source": "stpl_lv2",
            "era": "1996",
            "origin": "Tom Hoover / PwC / Management Horizons",
            "doc_type": "process_map",
            "priority": 1,
        },
    },
    {
        "path": "/app/docs/sources/stpl_lv2/INDEX.md",
        "memory_type": "foundation",
        "metadata": {
            "source": "stpl_lv2",
            "era": "1996",
            "origin": "Tom Hoover / PwC / Management Horizons",
            "doc_type": "index",
            "priority": 1,
        },
    },
    {
        "path": "/app/docs/sources/tesco_tom/CANARY_PROCESS_MAP.md",
        "memory_type": "foundation",
        "metadata": {
            "source": "tesco_tom",
            "era": "2001-2007",
            "origin": "Tesco IT Change Programme",
            "doc_type": "process_map",
            "priority": 1,
        },
    },
    {
        "path": "/app/docs/sources/tesco_tom/INDEX.md",
        "memory_type": "foundation",
        "metadata": {
            "source": "tesco_tom",
            "era": "2001-2007",
            "origin": "Tesco IT Change Programme",
            "doc_type": "index",
            "priority": 1,
        },
    },
    {
        "path": "/app/docs/sources/ibm_retail_bi/CANARY_LINEAGE_MAP.md",
        "memory_type": "foundation",
        "metadata": {
            "source": "ibm_retail_bi",
            "era": "2004-2005",
            "origin": "IBM BluePearl / Steve Gordon / Daniel Graham",
            "doc_type": "lineage_map",
            "priority": 1,
        },
    },
    {
        "path": "/app/docs/sources/ibm_retail_bi/INDEX.md",
        "memory_type": "foundation",
        "metadata": {
            "source": "ibm_retail_bi",
            "era": "2004-2005",
            "origin": "IBM BluePearl / Steve Gordon / Daniel Graham",
            "doc_type": "index",
            "priority": 1,
        },
    },
]

# Priority 2: Architectural SDDs (the vision + ontology alignment)
ARCH_SDD_DIR = "/app/docs/sdds"
ARCH_SDDS = [
    "SDD-057_service_domain_map.md",
    "SDD-058_context_block_design.md",
    "SDD-059_modern_architecture_blueprint.md",
    "SDD-060_process_ontology_alignment.md",
    "SDD-061_institutional_knowledge_service.md",
    "SDD-062_api_gateway.md",
]

# Priority 3: All other SDDs (implementation specs)
# Discovered dynamically from docs/sdds/ excluding arch SDDs above

# Priority 4: Team profiles
# Lives in repo at docs/profiles/ — COPY'd into image at /app/docs/profiles/
TEAM_DIR = os.getenv("TEAM_DIR", "/app/docs/profiles")
def _discover_agent_roles(team_dir: str) -> dict:
    """Discover agent roles from profile directory listing."""
    roles = {}
    ops_dir = os.path.join(team_dir, "ops")
    search_dirs = [team_dir, ops_dir]
    for d in search_dirs:
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            if f.endswith(".md"):
                roles[f.replace(".md", "")] = "Team Member"
    return roles

AGENT_ROLES = {}  # populated at runtime from directory listing

# Priority 5: Curated work products
# Lives in repo at docs/work_products/ — COPY'd into image at /app/docs/work_products/
ALX_DIR = os.getenv("ALX_WORK_DIR", "/app/docs/work_products")
# Only ingest deliverables and work orders — skip dispatches, captures, noise
CURATED_CATEGORIES = {"deliverable", "work_order", "war_chest"}


# ---------------------------------------------------------------------------
# Domain doc seeding (v2 — SDD-058 aligned context blocks)
# ---------------------------------------------------------------------------

DOMAIN_DOCS_DIR = "/app/docs/sdds/v2"

# Per-domain metadata enrichment (from SDD-057 + MCP registry)
DOMAIN_META_ENRICHMENT = {
    "identity": {
        "api_paths": ["/auth/*", "/oauth/*", "/api/merchants/*", "/api/employees/*", "/api/locations/*"],
        "mcp_server": "canary-identity",
        "mcp_tools": ["get_merchant", "get_settings", "list_employees", "get_employee", "list_locations", "get_location"],
        "code_entry_points": ["canary/blueprints/auth.py", "canary/services/square_oauth.py", "canary/services/identity/tools.py"],
        "tables": ["organizations", "merchants", "merchant_settings", "users", "roles", "user_roles", "employees", "locations", "square_oauth_tokens"],
        "database": "app",
    },
    "tsp": {
        "api_paths": ["/webhooks/*", "/api/receipt/*"],
        "mcp_server": "canary-tsp",
        "mcp_tools": ["get_ingestion_stats", "get_receipt", "get_stream_health", "get_dead_letters", "replay_event", "verify_merkle"],
        "code_entry_points": ["canary/blueprints/webhooks_tsp.py", "canary/services/tsp/stream_publisher.py"],
        "tables": ["webhook_events", "schema_fingerprints", "transactions", "transaction_line_items", "transaction_tenders"],
        "database": "app+sales",
    },
    "chirp": {
        "api_paths": ["/api/chirp/*", "/chirp/*"],
        "mcp_server": "canary-chirp",
        "mcp_tools": ["get_rules", "get_rule", "evaluate_stateless", "apply_sensitivity", "get_templates", "apply_template", "validate_thresholds", "get_config_summary", "estimate_sensitivity", "get_merchant_thresholds"],
        "code_entry_points": ["canary/services/chirp/rule_engine.py", "canary/services/chirp/stateless_engine.py", "canary/services/chirp/tools.py"],
        "tables": ["detection_rules", "merchant_rule_config"],
        "database": "app",
    },
    "alert": {
        "api_paths": ["/api/alerts/*", "/alert/*"],
        "mcp_server": "canary-alert",
        "mcp_tools": ["lifecycle_summary", "calculate_impact", "rank_alerts", "get_impact_summary", "list_alerts", "get_alert"],
        "code_entry_points": ["canary/services/alert_lifecycle.py", "canary/services/impact_scoring.py"],
        "tables": ["alerts", "alert_history", "notification_log", "notification_schedule"],
        "database": "app",
    },
    "owl": {
        "api_paths": ["/owl/*"],
        "mcp_server": "canary-owl",
        "mcp_tools": ["the_one_thing", "ask", "heartbeat", "check_heartbeat", "score_payment", "search", "dashboard", "knowledge_search"],
        "code_entry_points": ["canary/services/owl/client.py", "canary/services/owl/router.py", "canary/services/owl/tools.py"],
        "tables": ["owl_sessions", "owl_findings", "owl_merchant_memory", "owl_action_log"],
        "database": "app",
    },
    "fox": {
        "api_paths": ["/api/fox/*", "/fox/*"],
        "mcp_server": "canary-fox",
        "mcp_tools": ["create_case", "get_case", "list_cases", "update_case_status", "add_subject", "get_timeline", "verify_chain", "link_alert"],
        "code_entry_points": ["canary/services/fox/case_service.py", "canary/services/fox/tools.py"],
        "tables": ["fox_cases", "fox_case_alerts", "fox_case_timeline", "fox_case_actions", "fox_evidence", "fox_evidence_access_log", "fox_subjects"],
        "database": "app",
    },
    "analytics": {
        "api_paths": ["/api/analytics/*", "/analytics/*"],
        "mcp_server": "canary-analytics",
        "mcp_tools": ["get_dashboard", "get_top_risks", "get_trends", "detect_velocity", "get_period_metrics", "get_drilldown", "score_metrics"],
        "code_entry_points": ["canary/services/dashboard_queries.py", "canary/services/heatmap_scoring.py"],
        "tables": ["daily_metrics", "hourly_metrics", "period_metrics", "velocity_baselines"],
        "database": "metrics",
    },
    "alx": {
        "api_paths": ["/alx/*"],
        "mcp_server": "canary-alx",
        "mcp_tools": ["memory_store", "memory_recall", "memory_search", "session_start", "session_close", "context_assemble", "domain_context"],
        "code_entry_points": ["canary/services/alx/memory.py", "canary/services/alx/tools.py"],
        "tables": ["alx_memories", "alx_sessions"],
        "database": "memory",
    },
    "raas": {
        "api_paths": ["/raas/*"],
        "mcp_server": "canary-raas",
        "mcp_tools": ["resolve_namespace", "ensure_namespace", "register_source", "get_sources", "disconnect_source", "build_key", "link_jeffe"],
        "code_entry_points": ["canary/services/raas/namespace_resolver.py", "canary/services/raas/tools.py"],
        "tables": ["namespace_registrations", "namespace_aliases"],
        "database": "app",
    },
    "ops": {
        "api_paths": ["/ops/*", "/devops/*", "/ops-mcp/*"],
        "mcp_server": "canary-ops",
        "mcp_tools": ["start_health_check", "poll_health_check", "start_simulation", "poll_simulation", "fire_chirp", "run_scenario", "factory_reset", "get_feature_flags"],
        "code_entry_points": ["canary/services/health_check/runner.py", "canary/services/health_check/heartbeat.py"],
        "tables": [],
        "database": "app",
    },
    "ui_bff": {
        "api_paths": ["/m/*", "/desktop/*", "/bff/*"],
        "mcp_server": "canary-bff",
        "mcp_tools": ["get_home_data", "get_chirp_feed", "refresh", "get_feature_flags"],
        "code_entry_points": ["canary/blueprints/views_wired.py", "canary/services/feature_flags.py"],
        "tables": ["feature_flags", "merchant_feature_flags", "app_config", "card_profiles", "blocked_entities"],
        "database": "app",
    },
}

# Filename → SDD-057 domain
FILENAME_DOMAIN_MAP = {
    "identity.md": "identity",
    "webhook-pipeline.md": "tsp",
    "chirp.md": "chirp",
    "alert.md": "alert",
    "owl.md": "owl",
    "fox.md": "fox",
    "analytics.md": "analytics",
    "alx.md": "alx",
    "raas.md": "raas",
    "ops.md": "ops",
    "ui-bff.md": "ui_bff",
    "architecture.md": "cross_cutting",
    "data-model.md": "cross_cutting",
}

# Heading text → SDD-058 block_type
HEADING_BLOCK_TYPE_MAP = {
    "overview": "domain_overview",
    "platform overview": "domain_overview",
    "infrastructure": "domain_overview",
    "patterns": "domain_overview",
    "target state": "domain_overview",
    "api contracts": "api_contract",
    "data model": "data_model",
    "app schema": "data_model",
    "sales schema": "data_model",
    "metrics schema": "data_model",
    "memory schema": "data_model",
    "workflows": "workflow",
    # raas.md uses non-standard section names
    "namespace resolution": "api_contract",
    "onboarding pipeline": "workflow",
    "dependencies and cross-domain contracts": "domain_overview",
    # data-model.md cross-cutting patterns
    "cross-cutting patterns": "domain_overview",
    # ui-bff.md
    "rendering & design system": "workflow",
    "data models": "data_model",
}


def heading_to_block_type(heading: str) -> str | None:
    """Map a ## heading to an SDD-058 block_type."""
    text = heading.lstrip("#").strip().lower()
    return HEADING_BLOCK_TYPE_MAP.get(text)


def filename_to_domain(filename: str) -> str:
    """Map a domain doc filename to SDD-057 domain."""
    return FILENAME_DOMAIN_MAP.get(filename, "cross_cutting")


def extract_sdd_refs(content: str) -> list[str]:
    """Extract SDD-NNN references from markdown content."""
    return sorted(set(re.findall(r"SDD-\d{3}", content)))


def chunk_domain_doc(content: str, filename: str) -> list[dict]:
    """Split a domain doc on ## boundaries, producing context_block chunks.

    Sections with no matching block_type are stored with block_type=None —
    they won't match block_type filters but will still be found via semantic search.

    Note: `re` is already imported at the top of this file.
    """
    domain = filename_to_domain(filename)
    enrichment = DOMAIN_META_ENRICHMENT.get(domain, {})
    sections = re.split(r'(?=^## )', content, flags=re.MULTILINE)
    sections = [s.strip() for s in sections if s.strip() and s.strip().startswith("## ")]

    chunks = []
    for section in sections:
        heading_line = section.split("\n")[0]
        block_type = heading_to_block_type(heading_line)

        # Sub-chunk if section exceeds MAX_CHUNK_CHARS
        if len(section) > MAX_CHUNK_CHARS:
            sub_chunks = chunk_document(section, max_chars=MAX_CHUNK_CHARS)
        else:
            sub_chunks = [section]

        for sub in sub_chunks:
            sdd_refs = extract_sdd_refs(sub)
            meta = {
                "block_type": block_type,
                "domain": domain,
                "domains": [domain] if domain != "cross_cutting" else [],
                "sdd_refs": sdd_refs,
                "filename": filename,
                "token_estimate": len(sub) // 4,
                "version": "2.0",
                "created_by": "seed_memory_foundation",
                "priority": 2,
                # SDD-058 enrichment fields
                "api_paths": enrichment.get("api_paths", []),
                "mcp_server": enrichment.get("mcp_server", ""),
                "mcp_tools": enrichment.get("mcp_tools", []),
                "code_entry_points": enrichment.get("code_entry_points", []),
                "tables": enrichment.get("tables", []),
                "database": enrichment.get("database", ""),
            }
            chunks.append({
                "content": sub,
                "memory_type": "context_block",
                "metadata": meta,
            })

    # Add chunk N/M numbering
    total = len(chunks)
    for i, chunk in enumerate(chunks):
        chunk["metadata"]["chunk"] = f"{i+1}/{total}"

    return chunks


def seed_domain_docs(dry_run: bool = False) -> int:
    """Seed v2 domain docs as context_block memories."""
    print("\n" + "=" * 60)
    print("DOMAIN DOCS: v2 Context Blocks (SDD-058)")
    print("=" * 60)

    docs_dir = DOMAIN_DOCS_DIR
    if not os.path.exists(docs_dir):
        # Fallback for host-side execution
        docs_dir = os.path.join(
            os.path.dirname(__file__), "..", "..", "docs", "sdds", "v2"
        )
        docs_dir = os.path.abspath(docs_dir)

    if not os.path.exists(docs_dir):
        print(f"  SKIP: Domain docs directory not found at {docs_dir}")
        return 0

    total = 0
    for filename in sorted(os.listdir(docs_dir)):
        if not filename.endswith(".md"):
            continue

        filepath = os.path.join(docs_dir, filename)
        content = read_file(filepath)
        if not content:
            continue

        chunks = chunk_domain_doc(content, filename)
        print(f"  {filename}: {len(chunks)} context blocks")

        for chunk in chunks:
            prefix = f"DOMAIN DOC: {filename}\n{chunk['metadata']['domain']}"
            prefixed_content = f"{prefix}\n\n{chunk['content']}"
            if store_memory(prefixed_content, chunk["memory_type"],
                           chunk["metadata"], dry_run):
                total += 1

    print(f"  -> {total} context block memories stored")
    return total


# ---------------------------------------------------------------------------
# Chunking (same proven pattern from seed_work_products.py)
# ---------------------------------------------------------------------------

def chunk_document(content: str, prefix: str = "", max_chars: int = MAX_CHUNK_CHARS) -> list:
    """Split document on ## / ### headings, respecting max_chars."""
    sections = re.split(r'(?=^## )', content, flags=re.MULTILINE)
    sections = [s.strip() for s in sections if s.strip()]

    if not sections:
        sections = [content]

    chunks = []
    current_chunk = ""

    for section in sections:
        if current_chunk and len(current_chunk) + len(section) > max_chars:
            chunks.append(current_chunk.strip())
            current_chunk = ""

        if len(section) > max_chars:
            subsections = re.split(r'(?=^### )', section, flags=re.MULTILINE)
            for sub in subsections:
                if len(current_chunk) + len(sub) > max_chars:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    if len(sub) > max_chars:
                        for i in range(0, len(sub), max_chars):
                            chunks.append(sub[i:i + max_chars].strip())
                        current_chunk = ""
                    else:
                        current_chunk = sub
                else:
                    current_chunk += "\n\n" + sub
        else:
            current_chunk += "\n\n" + section

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    # Prefix each chunk (sanitize prefix — filenames may contain codenames)
    if prefix:
        prefix = sanitize_content(prefix)
        prefixed = []
        for i, chunk in enumerate(chunks):
            header = f"{prefix}\n(Part {i + 1}/{len(chunks)})\n\n"
            prefixed.append(header + chunk)
        return prefixed

    return chunks


def sanitize_content(text: str) -> str:
    """Strip proprietary codenames before ingestion.

    CRDM → CDM / Canary Data Model
    TSP  → Webhook Pipeline (conceptual uses only, not code paths)

    Source files stay untouched — this only cleans what enters memory.
    """
    # --- CRDM → CDM ---
    text = re.sub(r"CRDM \(Canary Reference Data Model\)", "Canary Data Model (CDM)", text)
    text = re.sub(r"\(CRDM\)", "(CDM)", text)
    text = re.sub(r"CRDMSearchableBuilder", "Searchable Query Builder (legacy)", text)
    for old, new in [
        ("CRDM tables", "CDM tables"),
        ("CRDM format", "CDM format"),
        ("CRDM records", "CDM records"),
        ("CRDM model", "CDM model"),
        ("CRDM query", "CDM query"),
        ("CRDM accuracy", "CDM accuracy"),
        ("CRDM Model Mapping", "CDM Model Mapping"),
        ("CRDM Model", "CDM Model"),
        ("CRDM v1.1", "CDM v1.1"),
        ("CRDM v1.0", "CDM v1.0"),
        ("into CRDM", "into CDM"),
    ]:
        text = text.replace(old, new)
    text = re.sub(r"(?<!`)CRDM(?!`)", "Canary Data Model", text)
    text = re.sub(r"(?<!`)Crdm(?!`)", "Canary Data Model", text)
    text = re.sub(r"(?<!`)crdm(?!`)", "Canary Data Model", text)
    # Also catch backtick-wrapped CRDM references (style guide entries etc.)
    text = re.sub(r"`CRDM`", "`CDM`", text)

    # --- TSP → Webhook Pipeline (conceptual only) ---
    for old, new in [
        ("TSP Consumer Pipeline", "Webhook Consumer Pipeline"),
        ("TSP consumer pipeline", "Webhook consumer pipeline"),
        ("TSP Pipeline", "Webhook Pipeline"),
        ("TSP pipeline", "Webhook pipeline"),
        ("TSP Consumer", "Webhook Consumer"),
        ("TSP consumers", "Webhook consumers"),
        ("TSP Parsers", "Webhook Parsers"),
        ("TSP parsers", "Webhook parsers"),
        ("TSP Ingest Flow", "Webhook Ingest Flow"),
        ("TSP Webhook Receipt", "Webhook Receipt"),
        ("TSP webhook receiver", "Webhook receiver"),
        ("TSP Sub", "Webhook Sub"),
        ("TSP writes", "Webhook pipeline writes"),
    ]:
        text = text.replace(old, new)
    # Component IDs
    text = re.sub(r"(?<!`)TSP-01(?!`)", "WH-01", text)
    text = re.sub(r"(?<!`)TSP-03(?!`)", "WH-03", text)
    text = re.sub(r"(?<!`)TSP-05(?!`)", "WH-05", text)
    # Lineage refs
    text = text.replace("elJeffe/TSP/Canary", "elJeffe/Canary")
    text = text.replace("elJeffe/TSP", "elJeffe")
    # Standalone TSP
    text = re.sub(r"(?<!`)(?<![\w/.-])TSP(?![\w/.-])(?!`)", "Webhook Pipeline", text)

    # Cleanup double spaces
    text = re.sub(r"  +", " ", text)
    return text


def read_file(filepath: str) -> str:
    """Read a text file, return empty string on error."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            return sanitize_content(f.read())
    except Exception as e:
        print(f"  WARNING: Cannot read {filepath}: {e}")
        return ""


# ---------------------------------------------------------------------------
# Store helper
# ---------------------------------------------------------------------------

def store_memory(content: str, memory_type: str, metadata: dict,
                 dry_run: bool = False) -> bool:
    """Store a single memory chunk. Returns True on success."""
    if dry_run:
        return True

    try:
        from canary.services.alx.memory import memory_store
        result = memory_store(
            session_id=SESSION_ID,
            content=content,
            memory_type=memory_type,
            metadata=metadata,
        )
        return result.get("stored", False)
    except Exception as e:
        print(f"    ERROR storing: {e}")
        return False


# ---------------------------------------------------------------------------
# Seed functions by priority
# ---------------------------------------------------------------------------

def seed_foundations(dry_run: bool = False) -> int:
    """Priority 1: Foundational process maps and lineage documents."""
    print("\n" + "=" * 60)
    print("PRIORITY 1: Foundational Process Architecture")
    print("=" * 60)

    total = 0
    for doc in FOUNDATION_DOCS:
        filepath = doc["path"]
        if not os.path.exists(filepath):
            print(f"  SKIP (not found): {filepath}")
            continue

        content = read_file(filepath)
        if not content:
            continue

        filename = os.path.basename(filepath)
        prefix = f"FOUNDATION: {filename}\nSource: {doc['metadata']['origin']} ({doc['metadata']['era']})"
        chunks = chunk_document(content, prefix=prefix)

        print(f"  {filename}: {len(chunks)} chunks ({len(content):,} chars)")

        for i, chunk in enumerate(chunks):
            meta = {**doc["metadata"], "filename": filename, "chunk": f"{i+1}/{len(chunks)}"}
            if store_memory(chunk, doc["memory_type"], meta, dry_run):
                total += 1

    print(f"  -> {total} foundation memories stored")
    return total


def seed_arch_sdds(dry_run: bool = False) -> int:
    """Priority 2: Architectural SDDs (057-060)."""
    print("\n" + "=" * 60)
    print("PRIORITY 2: Architectural SDDs")
    print("=" * 60)

    total = 0
    for sdd_file in ARCH_SDDS:
        filepath = os.path.join(ARCH_SDD_DIR, sdd_file)
        if not os.path.exists(filepath):
            print(f"  SKIP (not found): {filepath}")
            continue

        content = read_file(filepath)
        if not content:
            continue

        sdd_num = sdd_file.split("_")[0]  # "SDD-057"
        prefix = f"ARCHITECTURE SDD: {sdd_file}\n{sdd_num}"
        chunks = chunk_document(content, prefix=prefix)

        print(f"  {sdd_file}: {len(chunks)} chunks ({len(content):,} chars)")

        for i, chunk in enumerate(chunks):
            meta = {
                "sdd": sdd_num,
                "filename": sdd_file,
                "group": "architecture",
                "chunk": f"{i+1}/{len(chunks)}",
                "priority": 2,
            }
            if store_memory(chunk, "architecture", meta, dry_run):
                total += 1

    print(f"  -> {total} architectural SDD memories stored")
    return total


def seed_sdds(dry_run: bool = False) -> int:
    """Priority 3: All other SDDs (001-056)."""
    print("\n" + "=" * 60)
    print("PRIORITY 3: Implementation SDDs (001-056)")
    print("=" * 60)

    total = 0
    arch_set = set(ARCH_SDDS)

    if not os.path.exists(ARCH_SDD_DIR):
        print(f"  SKIP: SDD directory not found at {ARCH_SDD_DIR}")
        return 0

    sdd_files = sorted([
        f for f in os.listdir(ARCH_SDD_DIR)
        if f.startswith("SDD-") and f.endswith(".md") and f not in arch_set
    ])

    for sdd_file in sdd_files:
        filepath = os.path.join(ARCH_SDD_DIR, sdd_file)
        content = read_file(filepath)
        if not content:
            continue

        sdd_num = sdd_file.split("_")[0]
        prefix = f"SDD: {sdd_file}\n{sdd_num}"
        chunks = chunk_document(content, prefix=prefix)

        print(f"  {sdd_file}: {len(chunks)} chunks")

        for i, chunk in enumerate(chunks):
            meta = {
                "sdd": sdd_num,
                "filename": sdd_file,
                "group": "implementation",
                "chunk": f"{i+1}/{len(chunks)}",
                "priority": 3,
            }
            if store_memory(chunk, "architecture", meta, dry_run):
                total += 1

    print(f"  -> {total} implementation SDD memories stored")
    return total


def seed_team_profiles(dry_run: bool = False) -> int:
    """Priority 4: Team profiles."""
    print("\n" + "=" * 60)
    print("PRIORITY 4: Team Profiles")
    print("=" * 60)

    total = 0

    for agent_name, role in sorted(AGENT_ROLES.items()):
        filepath = os.path.join(TEAM_DIR, f"{agent_name}.md")

        # ALX profile is in _ALX root, not team dir
        if agent_name == "ALX":
            filepath = os.path.join(ALX_DIR, "ALX.md")

        if not os.path.exists(filepath):
            print(f"  SKIP (not found): {agent_name} at {filepath}")
            continue

        content = read_file(filepath)
        if not content:
            continue

        prefix = f"TEAM PROFILE: {agent_name} — {role}"
        chunks = chunk_document(content, prefix=prefix)

        print(f"  {agent_name}: {len(chunks)} chunks")

        for i, chunk in enumerate(chunks):
            meta = {
                "agent_name": agent_name,
                "role": role,
                "chunk": f"{i+1}/{len(chunks)}",
                "source": filepath,
                "priority": 4,
            }
            if store_memory(chunk, "team_profile", meta, dry_run):
                total += 1

    print(f"  -> {total} team profile memories stored")
    return total


def seed_work_products(dry_run: bool = False) -> int:
    """Priority 5: Curated work products (deliverables + work orders only)."""
    print("\n" + "=" * 60)
    print("PRIORITY 5: Curated Work Products")
    print("=" * 60)

    total = 0
    ingestible_exts = {".md", ".yaml", ".yml", ".json", ".txt"}
    skip_patterns = {".DS_Store", ".obsidian", "__pycache__", ".tmp",
                     "node_modules", ".git", "bolt.diy"}

    if not os.path.exists(ALX_DIR):
        print(f"  SKIP: ALX directory not found at {ALX_DIR}")
        return 0

    files = []
    for root, dirs, filenames in os.walk(ALX_DIR):
        dirs[:] = [d for d in dirs if not any(s in d for s in skip_patterns)]

        # Skip archives and site renders
        if "archive" in root.split("/") or "sources_v2_archive" in root:
            continue
        if "/WarChest/site/" in root:
            continue

        for fname in sorted(filenames):
            ext = os.path.splitext(fname)[1].lower()
            if ext not in ingestible_exts:
                continue
            if any(s in fname for s in skip_patterns):
                continue

            filepath = os.path.join(root, fname)
            category = _categorize_work_product(filepath)

            if category not in CURATED_CATEGORIES:
                continue

            files.append({
                "filepath": filepath,
                "filename": fname,
                "category": category,
                "agent": _extract_agent(filepath, fname),
            })

    print(f"  Found {len(files)} curated work product files")

    for info in files:
        content = read_file(info["filepath"])
        if not content or len(content) < 50:
            continue

        prefix = f"WORK PRODUCT ({info['category'].upper()}): {info['filename']}\nAgent: {info['agent']}"
        chunks = chunk_document(content, prefix=prefix)

        for i, chunk in enumerate(chunks):
            meta = {
                "agent": info["agent"],
                "category": info["category"],
                "filename": info["filename"],
                "filepath": info["filepath"],
                "chunk": f"{i+1}/{len(chunks)}",
                "priority": 5,
            }
            if store_memory(chunk, "work_product", meta, dry_run):
                total += 1

    print(f"  -> {total} work product memories stored")
    return total


def _categorize_work_product(filepath: str) -> str:
    """Simple category assignment for work products."""
    if "WorkOrders/output" in filepath:
        return "deliverable"
    elif "WorkOrders/dispatches" in filepath:
        return "dispatch"
    elif "WorkOrders/captures" in filepath:
        return "capture"
    elif "WorkOrders/" in filepath:
        return "work_order"
    elif "WarChest/" in filepath:
        return "war_chest"
    return "operational"


def _extract_agent(filepath: str, filename: str) -> str:
    """Extract agent name from filepath or filename."""
    agents = [
        # Agent names discovered from profile directory at runtime
        "Tom", "Eva", "Will", "Condor", "ALX",
    ]
    if "WorkOrders/output/" in filepath:
        for agent in agents:
            if f"/{agent}/" in filepath:
                return agent
    for agent in agents:
        if filename.startswith(agent) or f"_{agent}_" in filename:
            return agent
    return "ALX"


# ---------------------------------------------------------------------------
# Database setup
# ---------------------------------------------------------------------------

def update_constraint(dry_run: bool = False):
    """Ensure all memory types are in the CHECK constraint."""
    if dry_run:
        print("[DRY RUN] Would update memory_type constraint")
        return

    try:
        from canary.services.alx.memory import _get_session
        from sqlalchemy import text

        db = _get_session()

        # Drop and recreate with all types
        types_sql = ", ".join(f"'{t}'" for t in ALL_MEMORY_TYPES)
        db.execute(text(
            "ALTER TABLE alx_memories DROP CONSTRAINT IF EXISTS alx_memories_memory_type_check"
        ))
        db.execute(text(f"""
            ALTER TABLE alx_memories ADD CONSTRAINT alx_memories_memory_type_check
            CHECK (memory_type = ANY (ARRAY[{types_sql}]))
        """))
        db.commit()
        print(f"Memory type constraint updated: {ALL_MEMORY_TYPES}")
    except Exception as e:
        print(f"WARNING: Could not update constraint: {e}")
        try:
            db.rollback()
        except Exception:
            pass


def truncate_memories(dry_run: bool = False):
    """Clean slate — drop all existing memories."""
    if dry_run:
        print("[DRY RUN] Would TRUNCATE alx_memories")
        return

    try:
        from canary.services.alx.memory import _get_session
        from sqlalchemy import text

        db = _get_session()
        count = db.execute(text("SELECT COUNT(*) FROM alx_memories")).scalar()
        db.execute(text("TRUNCATE TABLE alx_memories"))
        db.commit()
        print(f"TRUNCATED alx_memories ({count} rows removed)")
    except Exception as e:
        print(f"ERROR truncating: {e}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Reseed ALX Tier 1 memory from the ground up"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be seeded without writing")
    parser.add_argument("--no-truncate", action="store_true",
                        help="Add to existing memories instead of clean slate")
    parser.add_argument("--only", type=str,
                        choices=["foundation", "arch-sdds", "domain-docs", "sdds", "team", "work"],
                        help="Only run one seed phase")
    args = parser.parse_args()

    print(f"ALX Tier 1 Memory Reseed")
    print(f"Session: {SESSION_ID}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print(f"Truncate: {'no' if args.no_truncate else 'yes'}")

    # Verify memory layer
    if not args.dry_run:
        try:
            from canary.services.alx.memory import memory_healthy
            if not memory_healthy():
                print("ERROR: ALX memory database not reachable")
                sys.exit(1)
            print("ALX memory: healthy")
        except Exception as e:
            print(f"ERROR: Cannot initialize ALX memory: {e}")
            sys.exit(1)

    # Update constraint to include all types
    update_constraint(args.dry_run)

    # Clean slate
    if not args.no_truncate:
        truncate_memories(args.dry_run)

    # Seed in priority order
    grand_total = 0

    if not args.only or args.only == "foundation":
        grand_total += seed_foundations(args.dry_run)

    if not args.only or args.only == "arch-sdds":
        grand_total += seed_arch_sdds(args.dry_run)

    if not args.only or args.only == "domain-docs":
        grand_total += seed_domain_docs(args.dry_run)

    if not args.only or args.only == "sdds":
        grand_total += seed_sdds(args.dry_run)

    if not args.only or args.only == "team":
        grand_total += seed_team_profiles(args.dry_run)

    if not args.only or args.only == "work":
        grand_total += seed_work_products(args.dry_run)

    print("\n" + "=" * 60)
    print(f"COMPLETE: {grand_total} total memories stored")
    print(f"Session: {SESSION_ID}")
    print("=" * 60)


if __name__ == "__main__":
    main()
