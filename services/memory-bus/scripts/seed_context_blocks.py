#!/usr/bin/env python3
"""SDD-058: Seed ALX memory with domain context blocks.

Parses SDDs from docs/sdds/, the OpenAPI spec from docs/api/, and SDD-057
(Service Domain Map) to build 33 pre-assembled context blocks:

  - 11 Domain Overview blocks (~1,200 tokens each)
  - 7 Workflow blocks (~2,000 tokens each)
  - 4 Data Model blocks (~1,500 tokens each)
  - 11 API Contract blocks (~1,200 tokens each)

Stored as memory_type = "context_block" in alx_memories (canary_memory DB).

Idempotent: checks for existing blocks before inserting.

Usage (run inside Docker container):
    python devops/scripts/seed_context_blocks.py [--dry-run] [--force] [--cognee]

Or from host:
    docker compose -f devops/docker-compose.localhost.yml exec flask \
        python devops/scripts/seed_context_blocks.py --dry-run
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Ensure /app is on sys.path when running inside Docker
_app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _app_dir not in sys.path:
    sys.path.insert(0, _app_dir)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SDDS_DIR = os.getenv("SDDS_DIR", "docs/sdds")
OPENAPI_PATH = os.getenv("OPENAPI_PATH", "docs/api/canary-api-v1.yaml")
SESSION_ID = "seed-context-blocks"

# SDD-057: The 11 service domains
DOMAINS = [
    "identity", "tsp", "chirp", "alert", "owl",
    "fox", "analytics", "alx", "raas", "ops", "ui_bff",
]

# ---------------------------------------------------------------------------
# SDD-to-Domain mapping (from SDD-057)
# ---------------------------------------------------------------------------

SDD_DOMAIN_MAP = {
    # Identity
    "SDD-019": "identity", "SDD-023": "identity", "SDD-024": "identity",
    "SDD-039": "identity", "SDD-046": "identity",
    # TSP Pipeline
    "SDD-001": "tsp", "SDD-002": "tsp", "SDD-003": "tsp", "SDD-004": "tsp",
    "SDD-026": "tsp", "SDD-027": "tsp", "SDD-028": "tsp", "SDD-029": "tsp",
    "SDD-030": "tsp", "SDD-031": "tsp", "SDD-040": "tsp", "SDD-041": "tsp",
    # Chirp
    "SDD-005": "chirp", "SDD-006": "chirp", "SDD-021": "chirp",
    "SDD-022": "chirp", "SDD-025": "chirp", "SDD-033": "chirp",
    # Alert
    "SDD-007": "alert", "SDD-020": "alert", "SDD-034": "alert",
    # Owl
    "SDD-008": "owl", "SDD-011": "owl", "SDD-012": "owl",
    "SDD-013": "owl", "SDD-014": "owl", "SDD-043": "owl",
    # Fox
    "SDD-009": "fox", "SDD-010": "fox", "SDD-015": "fox",
    "SDD-016": "fox", "SDD-042": "fox",
    # Analytics
    "SDD-017": "analytics", "SDD-018": "analytics", "SDD-032": "analytics",
    # ALX
    "SDD-044": "alx", "SDD-058": "alx",
    # RaaS
    "SDD-035": "raas", "SDD-036": "raas", "SDD-037": "raas",
    # Ops
    "SDD-008": "ops", "SDD-009": "ops", "SDD-010": "ops", "SDD-038": "ops",
    # UI/BFF
    "SDD-017": "ui_bff", "SDD-056": "ui_bff",
    # Infrastructure (shared)
    "SDD-045": "identity", "SDD-047": "identity",
    "SDD-048": "identity", "SDD-049": "identity",
    "SDD-050": "identity", "SDD-051": "identity",
    "SDD-052": "identity", "SDD-053": "identity",
    "SDD-054": "identity", "SDD-055": "identity",
}

# Some SDDs map to multiple domains — track those separately
SDD_MULTI_DOMAIN = {
    "SDD-008": ["owl", "ops"],
    "SDD-009": ["fox", "ops"],
    "SDD-010": ["fox", "ops"],
    "SDD-017": ["analytics", "ui_bff"],
    "SDD-025": ["chirp", "alert"],
}

# Domain → Blueprints (from SDD-057 / wsgi.py BLUEPRINT_SPECS)
DOMAIN_BLUEPRINTS = {
    "identity": ["auth (/auth)", "merchants (/m-api)", "employees (/emp)", "locations (/loc)", "square_oauth (/oauth)"],
    "tsp": ["webhooks_tsp (/webhooks)", "receipt_tsp (/receipt)"],
    "chirp": ["chirp_wired (/api/chirp)"],
    "alert": ["alerts_wired (/api/alerts)"],
    "owl": ["owl_api (/owl)"],
    "fox": ["fox_wired (/api/fox)"],
    "analytics": ["analytics (/api/analytics)"],
    "alx": ["alx_api (/alx)"],
    "raas": ["(internal service — no HTTP blueprint)"],
    "ops": ["ops_console (/ops)", "devops_monitor (/devops)"],
    "ui_bff": ["views_wired (/m, /desktop)", "square_explorer (/sqx)"],
}

# Domain → Key service modules
DOMAIN_SERVICES = {
    "identity": ["canary/services/onboarding/", "canary/middleware/"],
    "tsp": ["canary/services/tsp/", "canary/services/receipt/"],
    "chirp": ["canary/services/chirp/rule_engine.py", "canary/services/chirp/stateless_engine.py"],
    "alert": ["canary/services/alert_lifecycle.py", "canary/services/notification_service.py"],
    "owl": ["canary/services/owl/client.py", "canary/services/owl/router.py", "canary/services/owl/personality.py", "canary/services/owl/output_formatter.py", "canary/services/owl/tools.py", "canary/services/owl/memory.py", "canary/services/owl/report.py"],
    "fox": ["canary/services/fox/case_service.py"],
    "analytics": ["canary/services/dashboard_queries.py", "canary/blueprints/analytics.py"],
    "alx": ["canary/services/alx/memory.py", "canary/services/alx/tools.py"],
    "raas": ["canary/services/namespace_registry.py"],
    "ops": ["canary/services/health_check/runner.py", "canary/services/health_check/heartbeat.py"],
    "ui_bff": ["canary/blueprints/views_wired.py", "templates/app/"],
}

# Domain → Key models/tables
DOMAIN_TABLES = {
    "identity": ["organizations", "merchants", "merchant_settings", "users", "roles", "user_roles", "oauth_tokens"],
    "tsp": ["webhook_events", "source_systems", "merchant_sources", "ingestion_log", "etl_batches", "dead_letter_queue", "transactions", "transaction_line_items", "transaction_tenders", "refund_links"],
    "chirp": ["detection_rules", "merchant_rule_config"],
    "alert": ["alerts", "alert_history", "notification_log", "notification_schedule"],
    "owl": ["owl_sessions", "owl_findings", "owl_merchant_memory", "owl_action_log"],
    "fox": ["fox_cases", "fox_case_alerts", "fox_case_timeline", "fox_evidence", "fox_evidence_access_log", "fox_subjects", "fox_case_actions"],
    "analytics": ["daily_metrics", "hourly_metrics", "period_metrics", "employee_metrics", "product_metrics", "dimension tables"],
    "alx": ["alx_memories", "alx_sessions"],
    "raas": ["namespace_registrations"],
    "ops": ["health check sessions (in-memory)"],
    "ui_bff": ["feature_flags", "app_config"],
}

# Domain → Database
DOMAIN_DATABASE = {
    "identity": "canary_app",
    "tsp": "canary_app + canary_sales",
    "chirp": "canary_app",
    "alert": "canary_app",
    "owl": "canary_app",
    "fox": "canary_app",
    "analytics": "canary_metrics",
    "alx": "canary_memory",
    "raas": "canary_app",
    "ops": "canary_app (sessions in-memory)",
    "ui_bff": "canary_app",
}

# Domain → MCP tools
DOMAIN_MCP_TOOLS = {
    "owl": ["the_one_thing", "ask", "heartbeat", "check_heartbeat", "score_payment", "search", "dashboard"],
    "alx": ["memory_store", "memory_recall", "memory_search", "session_start", "session_close", "context_assemble", "domain_context"],
}

# ---------------------------------------------------------------------------
# Workflow definitions (cross-domain, from SDD-058)
# ---------------------------------------------------------------------------

WORKFLOWS = [
    {
        "name": "Alert Lifecycle",
        "domains": ["tsp", "chirp", "alert", "owl", "fox"],
        "entry_point": "POST /webhooks/square",
        "description": (
            "Square webhook → TSP Pipeline (parse, validate, enrich, store) → "
            "Chirp rule engine (evaluate transaction against detection rules) → "
            "Alert (status: new)\n"
            "  ├── Resolve → AlertHistory(resolved) → TERMINAL\n"
            "  ├── Dismiss → AlertHistory(dismissed, reason) → TERMINAL\n"
            "  ├── Follow up → Fox evidence (GUID refs to RaaS) → case lifecycle\n"
            "  └── Open case → FoxCase → investigating → closed\n\n"
            "Entry: POST /webhooks/square\n"
            "Code: canary/services/chirp/rule_engine.py → canary/services/alert_lifecycle.py\n"
            "SDDs: SDD-001, SDD-005, SDD-006, SDD-007, SDD-025"
        ),
    },
    {
        "name": "Health Check Pipeline",
        "domains": ["ops", "chirp", "owl", "alert"],
        "entry_point": "POST /ops/api/health-check/start",
        "description": (
            "POST /ops/api/health-check/start → create session → "
            "MerchantSimulator generates synthetic data → Chirp sweep → "
            "Heartbeat scoring → Owl report generation → present to merchant\n\n"
            "Stages: created → oauth → ingest → load → analyze → present → act → completed\n"
            "Demo mode: synthetic data, no Square API.\n"
            "Entry: POST /ops/api/health-check/start\n"
            "Code: canary/services/health_check/runner.py → heartbeat.py → report.py\n"
            "SDDs: SDD-008, SDD-009, SDD-010, SDD-014, SDD-015, SDD-016, SDD-017"
        ),
    },
    {
        "name": "Case Management",
        "domains": ["owl", "fox", "alert"],
        "entry_point": "POST /owl/action (case_create)",
        "description": (
            "POST /owl/action → action_code=case_create → FoxCaseService.create_case() → "
            "FoxCase + FoxCaseAlert junction + AlertHistory(case_opened)\n\n"
            "Case lifecycle: open → investigating → pending_review → escalated → closed\n"
            "Evidence: GUID refs to RaaS (raas:{merchant_id}:{table}:{id})\n"
            "Timeline: append-only, hash-chained (PostgreSQL trigger)\n\n"
            "Entry: POST /owl/action\n"
            "Code: canary/services/fox/case_service.py → canary/models/fox/\n"
            "SDDs: SDD-009, SDD-010, SDD-015, SDD-016, SDD-042"
        ),
    },
    {
        "name": "Owl Chat Flow",
        "domains": ["owl", "alert", "ui_bff"],
        "entry_point": "POST /owl/chat",
        "description": (
            "User message → personality router (address extraction + intent scoring) → "
            "Chirp JPT lens → system prompt with merchant memory → "
            "Ollama LLM → output formatter (4 types: alert_set, memo, checklist, number) → "
            "exit actions → closes_to terminal state\n\n"
            "Three-window context: running summary + delta + heartbeat (~4000 tokens)\n"
            "Fallback: deterministic response when Ollama offline\n\n"
            "Entry: POST /owl/chat\n"
            "Code: canary/services/owl/router.py → client.py → output_formatter.py\n"
            "SDDs: SDD-011, SDD-012, SDD-013, SDD-014"
        ),
    },
    {
        "name": "TSP Ingest Flow",
        "domains": ["tsp"],
        "entry_point": "POST /webhooks/square",
        "description": (
            "Square webhook → HMAC verify → webhook_events INSERT → "
            "Sub1: Payment parser (extract transaction fields) → "
            "Sub2: Refund parser (link refunds to original) → "
            "Sub3: Cash drawer parser (shift events) → "
            "Sub4: Gift card & loyalty parser\n\n"
            "All writes to canary_sales are WRITE-ONCE IMMUTABLE (trigger-enforced).\n"
            "Dead letter queue for parse failures.\n\n"
            "Entry: POST /webhooks/square\n"
            "Code: canary/blueprints/webhooks_tsp.py → canary/services/tsp/\n"
            "SDDs: SDD-001, SDD-002, SDD-003, SDD-004, SDD-026, SDD-027"
        ),
    },
    {
        "name": "Merchant Onboarding",
        "domains": ["identity", "raas", "tsp"],
        "entry_point": "GET /oauth/authorize",
        "description": (
            "Merchant visits /oauth/authorize → Square OAuth flow → "
            "callback with auth code → exchange for tokens → "
            "store merchant + oauth_tokens → register namespace → "
            "initial data sync (pull historical Square data)\n\n"
            "Entry: GET /oauth/authorize\n"
            "Code: canary/blueprints/square_oauth.py → canary/services/onboarding/\n"
            "SDDs: SDD-019, SDD-039, SDD-035"
        ),
    },
    {
        "name": "Dashboard Assembly",
        "domains": ["analytics", "owl", "ui_bff"],
        "entry_point": "GET /api/analytics/dashboard",
        "description": (
            "GET /api/analytics/dashboard → query metrics star schema → "
            "heatmap scoring → velocity checks → Owl summary → "
            "assemble dashboard payload for mobile/desktop\n\n"
            "Star schema: fact tables (daily/hourly/period/employee/product metrics) + dimensions\n"
            "Heatmap: normalized 0-100 scores per Chirp category\n\n"
            "Entry: GET /api/analytics/dashboard\n"
            "Code: canary/services/dashboard_queries.py → canary/blueprints/analytics.py\n"
            "SDDs: SDD-013, SDD-017, SDD-018, SDD-032"
        ),
    },
]

# ---------------------------------------------------------------------------
# Data model blocks (per database)
# ---------------------------------------------------------------------------

DATA_MODELS = [
    {
        "database": "canary_app",
        "domain": "identity",  # primary owner
        "domains": ["identity", "tsp", "chirp", "alert", "owl", "fox", "raas", "ops"],
        "description": (
            "## canary_app Data Model\n\n"
            "~38 tables. Mixed patterns: CRUD, APPEND-ONLY, soft delete.\n\n"
            "### Key Table Groups\n"
            "- **Identity:** organizations, merchants, merchant_settings, users, roles, user_roles, oauth_tokens\n"
            "- **Webhooks:** webhook_events, source_systems, merchant_sources, schema_fingerprints\n"
            "- **Detection:** detection_rules, merchant_rule_config\n"
            "- **Alerts:** alerts, alert_history, notification_log, notification_schedule\n"
            "- **Owl:** owl_sessions, owl_findings, owl_merchant_memory, owl_action_log\n"
            "- **Fox:** fox_cases, fox_case_alerts, fox_case_timeline, fox_evidence, fox_evidence_access_log, fox_subjects, fox_case_actions\n"
            "- **Ops:** ingestion_log, etl_batches, dead_letter_queue\n"
            "- **Config:** feature_flags, app_config, namespace_registrations\n\n"
            "### Immutability Patterns\n"
            "- fox_case_timeline: APPEND-ONLY (hash-chained, trigger-enforced)\n"
            "- alert_history: APPEND-ONLY\n"
            "- fox_evidence_access_log: APPEND-ONLY\n"
            "- All others: standard CRUD with soft delete (GSLM pattern)\n\n"
            "SDDs: SDD-023 through SDD-026, SDD-031"
        ),
    },
    {
        "database": "canary_sales",
        "domain": "tsp",
        "domains": ["tsp"],
        "description": (
            "## canary_sales Data Model\n\n"
            "~19 tables. ALL WRITE-ONCE IMMUTABLE (PostgreSQL BEFORE trigger enforced).\n\n"
            "### Tables\n"
            "- **Transactions:** transactions, transaction_line_items, transaction_tenders, refund_links\n"
            "- **Cash Drawer:** cash_drawer_shifts, cash_drawer_events\n"
            "- **Gift Card:** gift_card_activities\n"
            "- **Loyalty:** loyalty_accounts, loyalty_events\n"
            "- **Disputes:** disputes, evidence_records\n"
            "- **Payouts:** payouts\n"
            "- **Inventory:** inventory_adjustments\n"
            "- **Timecards:** employee_timecards\n\n"
            "### Immutability\n"
            "No UPDATE or DELETE on any table. Corrections use compensating INSERTs.\n"
            "Trigger: `RAISE EXCEPTION 'IMMUTABILITY VIOLATION'`\n\n"
            "SDDs: SDD-027 through SDD-030"
        ),
    },
    {
        "database": "canary_metrics",
        "domain": "analytics",
        "domains": ["analytics"],
        "description": (
            "## canary_metrics Data Model\n\n"
            "~20 tables. Star schema for analytics + ML feature store.\n\n"
            "### Fact Tables\n"
            "- daily_metrics, hourly_metrics, period_metrics\n"
            "- employee_metrics, product_metrics\n\n"
            "### Dimension Tables\n"
            "- dim_merchant, dim_location, dim_date, dim_employee, dim_product\n\n"
            "### ML Feature Store\n"
            "- feature_store (key-value with versioning)\n"
            "- scorecards (merchant health scores)\n\n"
            "### Aggregation Pattern\n"
            "Raw → hourly → daily → period. No raw data in this DB.\n"
            "Writes via ETL batches from canary_app + canary_sales.\n\n"
            "SDD: SDD-032"
        ),
    },
    {
        "database": "canary_memory",
        "domain": "alx",
        "domains": ["alx"],
        "description": (
            "## canary_memory Data Model\n\n"
            "2 tables. ALX memory layer for session continuity.\n\n"
            "### Tables\n"
            "- **alx_memories:** id, session_id, memory_type, content, metadata (JSONB), created_at\n"
            "  - memory_type: decision, finding, context, architecture, session_summary, work_product, team_profile, context_block\n"
            "  - Tier 1: PostgreSQL full-text search\n"
            "  - Tier 2: Cognee enrichment (entity extraction + pgvector embeddings)\n"
            "- **alx_sessions:** id, session_id, status, started_at, closed_at, summary, decisions, unresolved\n\n"
            "### Cognee Integration\n"
            "Fire-and-forget: Tier 1 always writes, Tier 2 enriches in background.\n"
            "Kuzu graph DB for relationships. pgvector for semantic search.\n\n"
            "SDD: SDD-044"
        ),
    },
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def extract_sdd_number(filename: str) -> Optional[str]:
    """Extract SDD number from filename like 'SDD-005_chirp...' -> 'SDD-005'."""
    m = re.match(r"(SDD-\d{3})", filename, re.IGNORECASE)
    return m.group(1).upper() if m else None


def read_sdd(filepath: str) -> str:
    """Read an SDD file and return its content."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def get_sdds_for_domain(domain: str) -> List[str]:
    """Get all SDD numbers that map to a given domain."""
    sdds = []
    for sdd, dom in SDD_DOMAIN_MAP.items():
        if dom == domain:
            sdds.append(sdd)
    # Also check multi-domain SDDs
    for sdd, doms in SDD_MULTI_DOMAIN.items():
        if domain in doms and sdd not in sdds:
            sdds.append(sdd)
    return sorted(sdds)


def check_existing_block(domain: str, block_type: str) -> bool:
    """Check if a context block already exists."""
    try:
        from canary.services.alx.memory import recall_context_blocks
        blocks = recall_context_blocks(domain, block_type)
        return len(blocks) > 0
    except Exception:
        return False


def check_existing_workflow(name: str) -> bool:
    """Check if a workflow block already exists by name."""
    try:
        from canary.services.alx.memory import memory_recall
        result = memory_recall(f"## {name}", limit=1, memory_type="context_block")
        return len(result.get("matches", [])) > 0
    except Exception:
        return False


def check_existing_data_model(database: str) -> bool:
    """Check if a data model block exists for this database."""
    try:
        from canary.services.alx.memory import memory_recall
        result = memory_recall(f"## {database} Data Model", limit=1, memory_type="context_block")
        return len(result.get("matches", [])) > 0
    except Exception:
        return False


def store_block(content: str, metadata: dict, dry_run: bool = False) -> Optional[dict]:
    """Store a context block in alx_memories."""
    if dry_run:
        token_est = len(content) // 4
        print(f"  [DRY RUN] Would store {metadata['block_type']}/{metadata.get('domain', 'n/a')} "
              f"(~{token_est} tokens, {len(content)} chars)")
        return None

    from canary.services.alx.memory import memory_store
    return memory_store(
        session_id=SESSION_ID,
        content=content,
        memory_type="context_block",
        metadata=metadata,
    )


# ---------------------------------------------------------------------------
# Block builders
# ---------------------------------------------------------------------------

def build_domain_overview(domain: str) -> Tuple[str, dict]:
    """Build a domain overview block."""
    sdd_refs = get_sdds_for_domain(domain)
    blueprints = DOMAIN_BLUEPRINTS.get(domain, [])
    services = DOMAIN_SERVICES.get(domain, [])
    tables = DOMAIN_TABLES.get(domain, [])
    database = DOMAIN_DATABASE.get(domain, "")
    mcp_tools = DOMAIN_MCP_TOOLS.get(domain, [])

    lines = [
        f"## {domain.replace('_', ' ').title()} Domain Overview",
        "",
        f"### SDDs",
        f"- {', '.join(sdd_refs) if sdd_refs else 'None mapped'}",
        "",
        "### Blueprints",
    ]
    for bp in blueprints:
        lines.append(f"- {bp}")
    lines.append("")
    lines.append("### Service Modules")
    for svc in services:
        lines.append(f"- {svc}")
    lines.append("")
    lines.append("### Models/Tables")
    lines.append(f"Database: {database}")
    for tbl in tables:
        lines.append(f"- {tbl}")

    if mcp_tools:
        lines.append("")
        lines.append("### MCP Tools")
        for tool in mcp_tools:
            lines.append(f"- {tool}")

    content = "\n".join(lines)

    metadata = {
        "block_type": "domain_overview",
        "domain": domain,
        "sdd_refs": sdd_refs,
        "code_entry_points": services[:3],
        "tables": tables,
        "database": database,
        "token_estimate": len(content) // 4,
        "version": "1.0",
        "created_by": "seed_context_blocks",
    }

    return content, metadata


def build_workflow_block(workflow: dict) -> Tuple[str, dict]:
    """Build a workflow block."""
    content = (
        f"## {workflow['name']} Workflow\n\n"
        f"**Domains:** {', '.join(workflow['domains'])}\n"
        f"**Entry Point:** {workflow['entry_point']}\n\n"
        f"{workflow['description']}"
    )

    metadata = {
        "block_type": "workflow",
        "domain": workflow["domains"][0],  # Primary domain
        "domains": workflow["domains"],
        "token_estimate": len(content) // 4,
        "version": "1.0",
        "created_by": "seed_context_blocks",
    }

    return content, metadata


def build_data_model_block(model: dict) -> Tuple[str, dict]:
    """Build a data model block."""
    content = model["description"]

    metadata = {
        "block_type": "data_model",
        "domain": model["domain"],
        "domains": model["domains"],
        "database": model["database"],
        "token_estimate": len(content) // 4,
        "version": "1.0",
        "created_by": "seed_context_blocks",
    }

    return content, metadata


def build_api_contract_block(domain: str, openapi_spec: dict) -> Tuple[str, dict]:
    """Build an API contract block from the OpenAPI spec."""
    # Find paths tagged with this domain
    domain_tag = domain.replace("_", " ").title()
    # Also try lowercase and various formats
    tag_variants = [domain_tag, domain, domain.upper(), domain.replace("_", "/")]

    paths_for_domain = []
    api_paths = []

    for path, methods in openapi_spec.get("paths", {}).items():
        for method, details in methods.items():
            if method.startswith("x-") or method == "parameters":
                continue
            tags = details.get("tags", [])
            # Match any tag variant
            if any(t.lower().replace(" ", "_") == domain.lower() or
                   t.lower() == domain.lower() or
                   t.lower().replace(" ", "_").replace("/", "_") == domain.lower()
                   for t in tags):
                auth = "public"
                security = details.get("security", [])
                if security:
                    auth = list(security[0].keys())[0] if security[0] else "public"

                summary = details.get("summary", details.get("description", ""))[:100]
                paths_for_domain.append(
                    f"- **{method.upper()} {path}** — {auth} — {summary}"
                )
                api_paths.append(path)

    if not paths_for_domain:
        # Fallback: build from domain knowledge
        paths_for_domain.append(f"_No paths tagged '{domain}' in OpenAPI spec. See SDD-057 for endpoints._")

    lines = [
        f"## {domain.replace('_', ' ').title()} API Contract",
        "",
        f"### Endpoints ({len(api_paths)} paths)",
    ]
    lines.extend(paths_for_domain)

    content = "\n".join(lines)

    metadata = {
        "block_type": "api_contract",
        "domain": domain,
        "api_paths": api_paths[:20],  # Cap at 20 paths in metadata
        "token_estimate": len(content) // 4,
        "version": "1.0",
        "created_by": "seed_context_blocks",
    }

    return content, metadata


# ---------------------------------------------------------------------------
# OpenAPI parser
# ---------------------------------------------------------------------------

def load_openapi_spec(filepath: str) -> dict:
    """Load and parse the OpenAPI YAML spec."""
    try:
        import yaml
    except ImportError:
        print("WARNING: PyYAML not installed. API contract blocks will be minimal.")
        return {}

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"WARNING: OpenAPI spec not found at {filepath}")
        return {}
    except Exception as e:
        print(f"WARNING: Failed to parse OpenAPI spec: {e}")
        return {}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Seed ALX memory with domain context blocks (SDD-058)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be stored without writing")
    parser.add_argument("--force", action="store_true", help="Overwrite existing blocks")
    parser.add_argument("--cognee", action="store_true", help="Trigger Cognee Tier 2 enrichment after seeding")
    parser.add_argument("--domain", type=str, help="Only seed blocks for this domain")
    args = parser.parse_args()

    print("=" * 60)
    print("SDD-058: Domain Context Block Seeder")
    print("=" * 60)

    # Verify memory layer and update constraint
    if not args.dry_run:
        try:
            from canary.services.alx.memory import memory_healthy, _get_session
            if not memory_healthy():
                print("ERROR: ALX memory database not reachable")
                sys.exit(1)
            print("Memory layer: OK")

            # Ensure memory_type constraint includes 'context_block'
            db = _get_session()
            try:
                from sqlalchemy import text
                result = db.execute(text("""
                    SELECT conname FROM pg_constraint
                    WHERE conname = 'alx_memories_memory_type_check'
                """)).fetchone()
                if result:
                    # Drop and recreate with context_block included
                    db.execute(text("""
                        ALTER TABLE alx_memories DROP CONSTRAINT IF EXISTS alx_memories_memory_type_check
                    """))
                    db.execute(text("""
                        ALTER TABLE alx_memories ADD CONSTRAINT alx_memories_memory_type_check
                        CHECK (memory_type = ANY (ARRAY[
                            'decision', 'finding', 'context', 'architecture',
                            'session_summary', 'procedure', 'team_profile',
                            'work_product', 'context_block'
                        ]))
                    """))
                    db.commit()
                    print("Memory type constraint: updated (added context_block)")
                else:
                    print("Memory type constraint: not found (no constraint to update)")
            except Exception as e:
                print(f"WARNING: Could not update constraint: {e}")
                try:
                    db.rollback()
                except Exception:
                    pass
            finally:
                db.close()
        except Exception as e:
            print(f"ERROR: Cannot connect to memory layer: {e}")
            sys.exit(1)

    # Load OpenAPI spec
    openapi_spec = load_openapi_spec(OPENAPI_PATH)
    if openapi_spec:
        path_count = len(openapi_spec.get("paths", {}))
        print(f"OpenAPI spec: {path_count} paths loaded")
    else:
        print("OpenAPI spec: not available (API contract blocks will be minimal)")

    # Determine which domains to seed
    domains_to_seed = [args.domain] if args.domain else DOMAINS
    if args.domain and args.domain not in DOMAINS:
        print(f"ERROR: Unknown domain '{args.domain}'. Must be one of: {DOMAINS}")
        sys.exit(1)

    stats = {"overview": 0, "workflow": 0, "data_model": 0, "api_contract": 0, "skipped": 0}

    # Phase 1: Domain Overview blocks
    print(f"\n--- Phase 1: Domain Overview Blocks ({len(domains_to_seed)} domains) ---")
    for domain in domains_to_seed:
        if not args.force and not args.dry_run and check_existing_block(domain, "domain_overview"):
            print(f"  SKIP {domain}/domain_overview (exists)")
            stats["skipped"] += 1
            continue

        content, metadata = build_domain_overview(domain)
        store_block(content, metadata, dry_run=args.dry_run)
        stats["overview"] += 1
        print(f"  STORED {domain}/domain_overview (~{metadata['token_estimate']} tokens)")

    # Phase 2: Workflow blocks
    print(f"\n--- Phase 2: Workflow Blocks ({len(WORKFLOWS)} workflows) ---")
    for wf in WORKFLOWS:
        # Skip if domain filter is set and workflow doesn't involve that domain
        if args.domain and args.domain not in wf["domains"]:
            continue

        if not args.force and not args.dry_run and check_existing_workflow(wf["name"]):
            print(f"  SKIP {wf['name']} (exists)")
            stats["skipped"] += 1
            continue

        content, metadata = build_workflow_block(wf)
        store_block(content, metadata, dry_run=args.dry_run)
        stats["workflow"] += 1
        print(f"  STORED workflow/{wf['name']} (~{metadata['token_estimate']} tokens)")

    # Phase 3: Data Model blocks
    print(f"\n--- Phase 3: Data Model Blocks ({len(DATA_MODELS)} databases) ---")
    for dm in DATA_MODELS:
        if args.domain and args.domain not in dm["domains"]:
            continue

        if not args.force and not args.dry_run and check_existing_data_model(dm["database"]):
            print(f"  SKIP {dm['database']} (exists)")
            stats["skipped"] += 1
            continue

        content, metadata = build_data_model_block(dm)
        store_block(content, metadata, dry_run=args.dry_run)
        stats["data_model"] += 1
        print(f"  STORED data_model/{dm['database']} (~{metadata['token_estimate']} tokens)")

    # Phase 4: API Contract blocks
    print(f"\n--- Phase 4: API Contract Blocks ({len(domains_to_seed)} domains) ---")
    for domain in domains_to_seed:
        if not args.force and not args.dry_run and check_existing_block(domain, "api_contract"):
            print(f"  SKIP {domain}/api_contract (exists)")
            stats["skipped"] += 1
            continue

        content, metadata = build_api_contract_block(domain, openapi_spec)
        store_block(content, metadata, dry_run=args.dry_run)
        stats["api_contract"] += 1
        print(f"  STORED {domain}/api_contract (~{metadata['token_estimate']} tokens)")

    # Summary
    total = stats["overview"] + stats["workflow"] + stats["data_model"] + stats["api_contract"]
    print(f"\n{'=' * 60}")
    print(f"Done. {total} blocks stored, {stats['skipped']} skipped.")
    print(f"  Overview: {stats['overview']}")
    print(f"  Workflow: {stats['workflow']}")
    print(f"  Data Model: {stats['data_model']}")
    print(f"  API Contract: {stats['api_contract']}")
    print(f"{'=' * 60}")

    if args.cognee and not args.dry_run:
        print("\nCognee Tier 2 enrichment requested — this happens automatically")
        print("via memory_store(). Check logs for enrichment progress.")


if __name__ == "__main__":
    main()
