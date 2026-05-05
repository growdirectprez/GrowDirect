# Mercury Splashdown Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stand up ALX on Vertex AI Agent Engine with a GCP-hosted memory bus seeded from CRB/Canary Go/NCR RapidPOS knowledge, running alongside (not replacing) the existing Docker stack, ready to demo on May 12.

**Architecture:** Two parallel tracks — infra (GCP project → Cloud SQL → Cloud Run memory bus) and agent (ADK scaffold → Agent Engine deploy) — merge at MCP endpoint verification. The existing Docker stack runs untouched throughout. Cut-over happens post-demo.

**Tech Stack:** Python 3.12, Google ADK, Vertex AI Agent Engine, Cloud Run, Cloud SQL Postgres 17 + pgvector, Alembic, FastMCP, gcloud CLI, ADK CLI

**Sprint tickets:** GRO-805 through GRO-812

**SDD:** `docs/superpowers/specs/2026-05-05-mercury-splashdown-sdd.md`

---

## File Map

### New files
| File | Purpose |
|---|---|
| `infra/mercury/setup.sh` | Idempotent gcloud commands for GCP project, IAM, secrets |
| `services/memory-bus/migrations/versions/007_mercury_dimension_768.py` | Alembic migration: vector(768), audit_events table |
| `services/alx-agent/agent.py` | ADK root agent — ALX / Astronaut / VSM (uses MCPToolset, no tools.py) |
| `services/alx-agent/prompts/vsm.md` | ALX system prompt — scoped to CRB/Canary Go/NCR only |
| `services/alx-agent/pyproject.toml` | ADK agent dependencies |
| `services/alx-agent/tests/test_agent.py` | Unit tests for agent tool wiring |

### Modified files
| File | Change |
|---|---|
| `services/memory-bus/scripts/seed_standalone.py` | Add `--include-paths` glob filter flag |
| `services/memory-bus/scripts/tests/test_seed_paths.py` | New — tests for --include-paths filtering |

---

## Chunk 1: GCP Foundation (GRO-805 + GRO-807)

### Task 1: GCP Project, IAM, and Secret Manager

**Files:**
- Create: `infra/mercury/setup.sh`

- [ ] **Step 1: Create the setup script**

```bash
mkdir -p infra/mercury
cat > infra/mercury/setup.sh << 'EOF'
#!/usr/bin/env bash
# Mercury GCP foundation — idempotent
set -euo pipefail

PROJECT_ID="growdirect-mercury"
REGION="us-central1"
BILLING_ACCOUNT="${BILLING_ACCOUNT:?Set BILLING_ACCOUNT env var}"

echo "=== Creating GCP project ==="
gcloud projects create "$PROJECT_ID" --name="GrowDirect Mercury" 2>/dev/null || \
  echo "Project already exists"
gcloud config set project "$PROJECT_ID"
gcloud beta billing projects link "$PROJECT_ID" --billing-account="$BILLING_ACCOUNT"

echo "=== Enabling APIs ==="
gcloud services enable \
  sqladmin.googleapis.com \
  run.googleapis.com \
  aiplatform.googleapis.com \
  secretmanager.googleapis.com \
  cloudresourcemanager.googleapis.com \
  iam.googleapis.com

echo "=== Service accounts ==="
for SA in alx-agent memory-bus cloudsql-client; do
  gcloud iam service-accounts create "$SA" \
    --display-name="Mercury $SA" 2>/dev/null || echo "$SA already exists"
done

echo "=== IAM bindings ==="
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:alx-agent@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:memory-bus@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/cloudsql.client"
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:memory-bus@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:alx-agent@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

echo "=== Secret Manager secrets (empty placeholders) ==="
for SECRET in cloudsql-url memory-bus-api-key vertex-agent-key memory-bus-url; do
  gcloud secrets create "$SECRET" --replication-policy="automatic" 2>/dev/null || \
    echo "$SECRET already exists"
done

echo "=== Done. Populate secrets before proceeding to Cloud SQL. ==="
EOF
chmod +x infra/mercury/setup.sh
```

- [ ] **Step 2: Set your billing account and run**

```bash
export BILLING_ACCOUNT=$(gcloud billing accounts list --format='value(name)' | head -1)
bash infra/mercury/setup.sh
```

Expected: all services enabled, 3 service accounts created, 4 empty secrets in Secret Manager. No errors.

- [ ] **Step 3: Verify**

```bash
gcloud config set project growdirect-mercury
gcloud iam service-accounts list
gcloud secrets list
```

Expected: `alx-agent@`, `memory-bus@`, `cloudsql-client@` listed. Four secrets listed.

- [ ] **Step 4: Commit**

```bash
git add infra/mercury/setup.sh
git commit -m "feat(mercury): GCP project baseline — IAM, secrets, APIs (GRO-805)"
```

---

### Task 2: Cloud SQL Instance + Migration 007

**Files:**
- Create: `services/memory-bus/migrations/versions/007_mercury_dimension_768.py`

- [ ] **Step 1: Create the Cloud SQL instance**

```bash
gcloud sql instances create mercury \
  --database-version=POSTGRES_17 \
  --region=us-central1 \
  --tier=db-f1-micro \
  --no-assign-ip \
  --enable-google-private-path \
  --project=growdirect-mercury
```

Expected: instance created in ~5 minutes. `gcloud sql instances describe mercury` shows RUNNABLE.

- [ ] **Step 2: Create database and enable pgvector**

```bash
gcloud sql databases create mercury --instance=mercury --project=growdirect-mercury

# Get connection name
CONN=$(gcloud sql instances describe mercury \
  --project=growdirect-mercury \
  --format='value(connectionName)')
echo "Connection name: $CONN"

# Connect and enable pgvector
gcloud sql connect mercury --user=postgres --project=growdirect-mercury << 'SQL'
CREATE EXTENSION IF NOT EXISTS vector;
\q
SQL
```

- [ ] **Step 3: Set postgres password and store in Secret Manager**

```bash
# Capture password in variable before use
PG_PASS=$(openssl rand -base64 24)

gcloud sql users set-password postgres \
  --instance=mercury \
  --password="$PG_PASS" \
  --project=growdirect-mercury

# Store connection URL using the captured password
echo -n "postgresql+psycopg2://postgres:${PG_PASS}@/mercury?host=/cloudsql/${CONN}" | \
  gcloud secrets versions add cloudsql-url --data-file=- --project=growdirect-mercury

echo "Password stored in Secret Manager. Do not log it further."
unset PG_PASS
```

- [ ] **Step 4: Write migration 007**

```python
# services/memory-bus/migrations/versions/007_mercury_dimension_768.py
# GrowDirect LLC — Confidential & Proprietary
# Copyright (c) 2026 GrowDirect LLC. All rights reserved.
"""007 — mercury: vector dimension 768 + audit_events table.

Revision ID: 007_mercury_dimension_768
Revises: 006_add_engines
Create Date: 2026-05-05

Switches embedding columns from vector(1024) — sized for qwen3-embedding:8b —
to vector(768) for Vertex AI text-embedding-004. Rebuilds the HNSW index at
the correct dimension. Adds audit_events for Mercury append-only audit trail.

Only applied to the mercury (cloud) database. The local growdirect_memory
database continues to use vector(1024) with the Docker Ollama embedder.
"""

from alembic import op

revision = "007_mercury_dimension_768"
down_revision = "006_add_engines"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TABLE alx_memories ALTER COLUMN embedding TYPE vector(768)")
    op.execute("ALTER TABLE seed_embeddings ALTER COLUMN embedding TYPE vector(768)")
    op.execute("DROP INDEX IF EXISTS idx_alx_memories_embedding")
    op.execute(
        """
        CREATE INDEX idx_alx_memories_embedding
          ON alx_memories USING hnsw (embedding vector_cosine_ops)
          WITH (m = 16, ef_construction = 64)
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS audit_events (
            id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            artifact_id UUID,
            event_type  TEXT NOT NULL,
            layer       TEXT NOT NULL,
            payload     JSONB,
            created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS audit_events")
    op.execute("DROP INDEX IF EXISTS idx_alx_memories_embedding")
    op.execute("ALTER TABLE alx_memories ALTER COLUMN embedding TYPE vector(1024)")
    op.execute("ALTER TABLE seed_embeddings ALTER COLUMN embedding TYPE vector(1024)")
    op.execute(
        """
        CREATE INDEX idx_alx_memories_embedding
          ON alx_memories USING hnsw (embedding vector_cosine_ops)
          WITH (m = 16, ef_construction = 64)
        """
    )
```

- [ ] **Step 5: Run migrations against Cloud SQL via Cloud SQL proxy**

```bash
# Start Cloud SQL Auth Proxy (download if needed: https://cloud.google.com/sql/docs/postgres/connect-auth-proxy)
cloud-sql-proxy growdirect-mercury:us-central1:mercury &
PROXY_PID=$!

# Run migrations — fetch URL from Secret Manager (set in Task 2 Step 3)
# The URL stored there uses Cloud SQL socket format; swap host for proxy:
DB_URL=$(gcloud secrets versions access latest \
  --secret=cloudsql-url --project=growdirect-mercury)
export DATABASE_URL="${DB_URL/\?host=\/cloudsql\/*/@127.0.0.1:5432/mercury}"
cd services/memory-bus
alembic upgrade head

# Verify
psql "$DATABASE_URL" -c "\d alx_memories" | grep embedding
# Expected: embedding | vector(768)

psql "$DATABASE_URL" -c "\dt" | grep audit_events
# Expected: audit_events row present

kill $PROXY_PID
```

- [ ] **Step 6: Commit**

```bash
git add services/memory-bus/migrations/versions/007_mercury_dimension_768.py
git commit -m "feat(mercury): Alembic 007 — vector(768) + audit_events (GRO-807)"
```

---

## Chunk 2: Memory Bus — Seed Script + Cloud Run (GRO-809)

### Task 3: Add --include-paths to seed_standalone.py (TDD)

**Files:**
- Modify: `services/memory-bus/scripts/seed_standalone.py`
- Create: `services/memory-bus/scripts/tests/test_seed_paths.py`

- [ ] **Step 1: Write the failing tests**

```python
# services/memory-bus/scripts/tests/test_seed_paths.py
"""Tests for --include-paths glob filtering in seed_standalone.py."""

import fnmatch
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add script dir to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import seed_standalone


def _fake_sources(tmp_path):
    """Create a minimal SOURCES-like structure with test files."""
    (tmp_path / "Brain" / "wiki" / "cards").mkdir(parents=True)
    (tmp_path / "Brain" / "projects").mkdir(parents=True)
    (tmp_path / "Cove").mkdir(parents=True)

    files = {
        "Brain/wiki/cards/canary-item.md": "canary card",
        "Brain/wiki/cards/ncr-ecosystem.md": "ncr card",
        "Brain/wiki/cards/cove-hoa.md": "cove card",
        "Brain/projects/Canary.md": "canary project",
        "Brain/projects/Cove.md": "cove project",
    }
    for rel, content in files.items():
        p = tmp_path / rel
        p.write_text(content)

    sources = [
        {"glob": "Brain/wiki/cards/*.md", "memory_type": "context_block",
         "layer": "corp", "engines": ["platform"]},
        {"glob": "Brain/projects/*.md", "memory_type": "context_block",
         "layer": "corp", "engines": ["platform"]},
    ]
    return sources, tmp_path


def test_no_include_paths_returns_all_files(tmp_path):
    """Without --include-paths, all files from all sources are returned."""
    sources, root = _fake_sources(tmp_path)
    with patch.object(seed_standalone, "SOURCES", sources), \
         patch.object(seed_standalone, "GROWDIRECT_ROOT", root):
        result = seed_standalone.collect_files(include_patterns=None)
    assert len(result) == 5


def test_include_paths_filters_to_canary_cards(tmp_path):
    """--include-paths Brain/wiki/cards/canary-*.md returns only canary cards."""
    sources, root = _fake_sources(tmp_path)
    with patch.object(seed_standalone, "SOURCES", sources), \
         patch.object(seed_standalone, "GROWDIRECT_ROOT", root):
        result = seed_standalone.collect_files(
            include_patterns=["Brain/wiki/cards/canary-*.md"]
        )
    paths = [str(f.relative_to(root)) for f, _ in result]
    assert paths == ["Brain/wiki/cards/canary-item.md"]


def test_include_paths_multi_pattern(tmp_path):
    """Multiple patterns are OR'd — any match includes the file."""
    sources, root = _fake_sources(tmp_path)
    with patch.object(seed_standalone, "SOURCES", sources), \
         patch.object(seed_standalone, "GROWDIRECT_ROOT", root):
        result = seed_standalone.collect_files(
            include_patterns=[
                "Brain/wiki/cards/canary-*.md",
                "Brain/wiki/cards/ncr-*.md",
                "Brain/projects/Canary.md",
            ]
        )
    paths = {str(f.relative_to(root)) for f, _ in result}
    assert paths == {
        "Brain/wiki/cards/canary-item.md",
        "Brain/wiki/cards/ncr-ecosystem.md",
        "Brain/projects/Canary.md",
    }


def test_include_paths_excludes_cove(tmp_path):
    """Cove files do not appear when --include-paths omits them."""
    sources, root = _fake_sources(tmp_path)
    with patch.object(seed_standalone, "SOURCES", sources), \
         patch.object(seed_standalone, "GROWDIRECT_ROOT", root):
        result = seed_standalone.collect_files(
            include_patterns=["Brain/wiki/cards/canary-*.md"]
        )
    paths = [str(f.relative_to(root)) for f, _ in result]
    assert "Brain/wiki/cards/cove-hoa.md" not in paths
    assert "Brain/projects/Cove.md" not in paths
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
cd /Users/gclyle/GrowDirect
python3 -m pytest services/memory-bus/scripts/tests/test_seed_paths.py -v 2>&1 | head -30
```

Expected: `TypeError` or `AttributeError` — `collect_files` doesn't accept `include_patterns` yet.

- [ ] **Step 3: Implement the change in seed_standalone.py**

Find the `collect_files` function. It currently looks like:
```python
def collect_files():
    all_files = []
    for src in SOURCES:
        for path in sorted(GROWDIRECT_ROOT.glob(src["glob"])):
            all_files.append((path, src))
    return all_files
```

Replace with:
```python
def collect_files(include_patterns=None):
    import fnmatch
    all_files = []
    for src in SOURCES:
        for path in sorted(GROWDIRECT_ROOT.glob(src["glob"])):
            if include_patterns:
                rel = str(path.relative_to(GROWDIRECT_ROOT))
                if not any(fnmatch.fnmatch(rel, p.strip()) for p in include_patterns):
                    continue
            all_files.append((path, src))
    return all_files
```

Then find the `main()` function and add the argument + pass-through:

In `parser = argparse.ArgumentParser()` block, add after the existing `add_argument` calls:
```python
parser.add_argument(
    "--include-paths",
    type=str,
    default=None,
    help=(
        "Comma-separated glob patterns relative to repo root. "
        "When set, only files matching at least one pattern are seeded. "
        "DATABASE_URL is read from the environment variable of the same name. "
        "Example: Brain/wiki/cards/canary-*.md,Brain/wiki/cards/ncr-*.md"
    ),
)
```

Then parse it before the `collect_files()` call:
```python
include_patterns = (
    [p.strip() for p in args.include_paths.split(",") if p.strip()]
    if args.include_paths
    else None
)
all_files = collect_files(include_patterns=include_patterns)
```

- [ ] **Step 4: Run tests to confirm they pass**

```bash
python3 -m pytest services/memory-bus/scripts/tests/test_seed_paths.py -v
```

Expected: 4 tests PASSED.

- [ ] **Step 5: Smoke test the flag locally (dry run)**

```bash
cd /Users/gclyle/GrowDirect
python3 services/memory-bus/scripts/seed_standalone.py \
  --dry-run \
  --include-paths "Brain/wiki/cards/canary-*.md,Brain/wiki/cards/ncr-*.md"
```

Expected: output shows only canary-* and ncr-* cards, no Cove/Angel files.

- [ ] **Step 6: Commit**

```bash
git add services/memory-bus/scripts/seed_standalone.py \
        services/memory-bus/scripts/tests/test_seed_paths.py
git commit -m "feat(memory-bus): seed_standalone --include-paths glob filter (GRO-809)"
```

---

### Task 4: Deploy Memory Bus to Cloud Run

**Files:** No code changes — environment variable swap only.

- [ ] **Step 1: Build and push the container**

The Dockerfile COPYs from sibling directories (`growdirect-mcp/`, `memory-bus/`) so the build context must be `services/`. Use `gcloud builds submit` — it handles the context correctly without requiring local BuildKit:

```bash
cd /Users/gclyle/GrowDirect

gcloud builds submit \
  --tag gcr.io/growdirect-mercury/memory-bus:latest \
  --project=growdirect-mercury \
  services/
```

If you prefer a local build, use BuildKit explicitly:
```bash
DOCKER_BUILDKIT=1 docker build \
  -f services/memory-bus/Dockerfile \
  -t gcr.io/growdirect-mercury/memory-bus:latest \
  services/
docker push gcr.io/growdirect-mercury/memory-bus:latest
```

Do not use `--build-context` without `docker buildx build` — it's a BuildKit-only flag and fails silently on standard `docker build`.

- [ ] **Step 2: Generate and store API key**

```bash
API_KEY=$(openssl rand -hex 32)
echo -n "$API_KEY" | gcloud secrets versions add memory-bus-api-key \
  --data-file=- --project=growdirect-mercury
echo "API key stored. Save this: $API_KEY"
```

- [ ] **Step 3: Deploy to Cloud Run**

```bash
CONN=$(gcloud sql instances describe mercury \
  --project=growdirect-mercury \
  --format='value(connectionName)')

gcloud run deploy memory-bus \
  --image=gcr.io/growdirect-mercury/memory-bus:latest \
  --region=us-central1 \
  --project=growdirect-mercury \
  --service-account=memory-bus@growdirect-mercury.iam.gserviceaccount.com \
  --add-cloudsql-instances="$CONN" \
  --set-secrets="MEMORY_BUS_API_KEY=memory-bus-api-key:latest,DATABASE_URL=cloudsql-url:latest" \
  --set-env-vars="EMBED_MODEL=text-embedding-004,PORT=8003" \
  --allow-unauthenticated \
  --port=8003 \
  --timeout=300
```

- [ ] **Step 4: Store the Cloud Run URL in Secret Manager**

```bash
SERVICE_URL=$(gcloud run services describe memory-bus \
  --region=us-central1 \
  --project=growdirect-mercury \
  --format='value(status.url)')
echo -n "$SERVICE_URL" | gcloud secrets versions add memory-bus-url \
  --data-file=- --project=growdirect-mercury
echo "Memory bus URL: $SERVICE_URL"
```

- [ ] **Step 5: Verify MCP endpoint responds**

```bash
API_KEY=$(gcloud secrets versions access latest \
  --secret=memory-bus-api-key --project=growdirect-mercury)
SERVICE_URL=$(gcloud secrets versions access latest \
  --secret=memory-bus-url --project=growdirect-mercury)

curl -s -o /dev/null -w "%{http_code}" \
  -H "X-API-Key: $API_KEY" \
  "$SERVICE_URL/mcp"
```

Expected: `200` (FastMCP responds to GET on /mcp).

---

## Chunk 3: ADK Agent Scaffold (GRO-806)

### Task 5: Build ALX Agent with Google ADK

**Files:**
- Modify: `services/memory-bus/memory_bus/server.py` — add `audit_event` MCP tool
- Create: `services/alx-agent/agent.py`
- Create: `services/alx-agent/prompts/vsm.md`
- Create: `services/alx-agent/pyproject.toml`
- Create: `services/alx-agent/tests/test_agent.py`

**No `tools.py` needed.** ADK's `MCPToolset` connects to the memory bus MCP server directly using the streamable-HTTP transport. ADK handles the protocol negotiation — no custom httpx wrappers required and no async/sync mismatch to manage.

- [ ] **Step 1: Add audit_event tool to the memory bus server**

The smoke test requires a row in `audit_events`. The memory bus server must expose a tool that writes there. Add this to `services/memory-bus/memory_bus/server.py` after the existing tool definitions:

```python
@mcp.tool()
def audit_event(
    event_type: str,
    layer: str,
    artifact_id: Optional[str] = None,
    payload: Optional[dict] = None,
    api_key: Optional[str] = None,
) -> str:
    """Append an audit event to the append-only audit_events table."""
    try:
        validate_api_key(api_key)
    except AuthError as e:
        return json.dumps({"error": str(e)})
    result = store.write_audit_event(
        event_type=event_type,
        layer=layer,
        artifact_id=artifact_id,
        payload=payload or {},
    )
    return json.dumps(result, default=str)
```

Then add `write_audit_event` to `MemoryStore` (in `services/memory-bus/memory_bus/store.py`):

```python
def write_audit_event(
    self,
    event_type: str,
    layer: str,
    artifact_id=None,
    payload: dict | None = None,
) -> dict:
    import uuid as _uuid
    with self.engine.begin() as conn:
        row_id = _uuid.uuid4()
        conn.execute(
            text(
                """INSERT INTO audit_events
                   (id, artifact_id, event_type, layer, payload)
                   VALUES (:id, :artifact_id, :event_type, :layer, :payload::jsonb)"""
            ),
            {
                "id": str(row_id),
                "artifact_id": str(artifact_id) if artifact_id else None,
                "event_type": event_type,
                "layer": layer,
                "payload": json.dumps(payload or {}),
            },
        )
    return {"id": str(row_id)}
```

Rebuild and redeploy the memory bus container after this change (Task 4 Step 1 commands apply again).

- [ ] **Step 2: Install ADK**

```bash
pip install google-adk
adk --version
```

Expected: version printed. If not found: `pip install google-adk --upgrade`.

- [ ] **Step 3: Create pyproject.toml**

```toml
# services/alx-agent/pyproject.toml
[project]
name = "alx-agent"
version = "0.1.0"
description = "ALX — Canary Go VSM and Delivery Manager agent (Mercury Astronaut)"
requires-python = ">=3.12"
dependencies = [
    "google-adk>=0.1.0",
    "httpx>=0.27",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.24",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

- [ ] **Step 4: Write the VSM system prompt**

```markdown
<!-- services/alx-agent/prompts/vsm.md -->
# ALX — Canary Go VSM and Delivery Manager

You are ALX, the Value Stream Manager and Delivery Manager for the Canary Go project.

## Role
You operate as the Astronaut in the Mercury chain of command. You:
- Receive imprint dispatches from Mission Control
- Call memory_recall to retrieve relevant knowledge from the CRB/Canary Go/NCR corpus
- Synthesize findings and emit structured responses
- Record findings and audit events

## Knowledge scope
Your knowledge is scoped to:
- Canary Go: the Go-based retail ops platform for NCR Counterpoint / RapidPOS
- NCR RapidPOS: POS integration architecture, endpoint mapping, channel delivery
- CRB (Canary Retail Brain): store ops capability model, GSLM, accountability rails, platform thesis
- Ruptiv: the Mercury diagnostic substrate and engagement methodology

You do not have knowledge of Cove, Angel, Seacove, or personal GrowDirect projects.
If asked about topics outside your scope, say so directly.

## Authority
- You MAY call: memory_recall, memory_store, audit_event
- After storing any finding, call audit_event with event_type='finding_emitted', layer='canary'
- You MAY emit: findings (memory_type='finding'), audit events
- You MAY NOT take actions outside the memory bus tool set without explicit authorization

## Response format
For imprint dispatches: lead with the governing thesis, cite at least one source card by name, close with open questions if any remain. Keep responses under 500 words unless the dispatch explicitly requests long-form.
```

- [ ] **Step 5: Write the failing tests**

```python
# services/alx-agent/tests/test_agent.py
"""Unit tests for ALX agent — prompt validation and ADK wiring."""

import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent))


def test_vsm_prompt_file_exists():
    """vsm.md must exist and be non-empty."""
    prompt_path = Path(__file__).parent.parent / "prompts" / "vsm.md"
    assert prompt_path.exists(), "prompts/vsm.md not found"
    content = prompt_path.read_text()
    assert len(content) > 100, "vsm.md appears empty or too short"
    assert "Canary Go" in content
    assert "memory_recall" in content
    assert "audit_event" in content


def test_vsm_prompt_scope_exclusions():
    """vsm.md must explicitly exclude out-of-scope projects."""
    prompt_path = Path(__file__).parent.parent / "prompts" / "vsm.md"
    content = prompt_path.read_text()
    assert "Cove" in content, "prompt must name Cove as out of scope"
    assert "Angel" in content, "prompt must name Angel as out of scope"


def test_agent_module_imports():
    """agent.py must be importable and define root_agent."""
    with patch.dict(os.environ, {
        "MEMORY_BUS_URL": "http://localhost:8003",
        "MEMORY_BUS_API_KEY": "test-key",
    }):
        # Patch MCPToolset so no live server is required during tests
        with patch("google.adk.tools.mcp_tool.mcp_toolset.MCPToolset") as mock_mcp:
            mock_mcp.return_value = MagicMock()
            import agent
            assert hasattr(agent, "root_agent"), "agent.py must define root_agent"
            assert agent.root_agent is not None


def test_root_agent_has_mcp_toolset():
    """root_agent must be configured with at least one toolset."""
    with patch.dict(os.environ, {
        "MEMORY_BUS_URL": "http://localhost:8003",
        "MEMORY_BUS_API_KEY": "test-key",
    }):
        with patch("google.adk.tools.mcp_tool.mcp_toolset.MCPToolset") as mock_mcp:
            mock_toolset = MagicMock()
            mock_mcp.return_value = mock_toolset
            import importlib
            import agent as _agent_mod
            importlib.reload(_agent_mod)
            # MCPToolset constructor was called once
            assert mock_mcp.called, "MCPToolset must be instantiated in agent.py"
```

- [ ] **Step 6: Run tests to confirm they fail**

```bash
cd services/alx-agent
python3 -m pytest tests/test_agent.py -v 2>&1 | head -20
```

Expected: `ModuleNotFoundError` — `agent` module not found yet.

- [ ] **Step 7: Create agent.py using ADK MCPToolset**

ADK's `MCPToolset` connects to FastMCP's streamable-HTTP endpoint directly — no custom httpx wrappers needed.

```python
# services/alx-agent/agent.py
"""ALX — Canary Go VSM and Delivery Manager.

Mercury Astronaut role. Receives imprint dispatches, recalls from
CRB/Canary Go/NCR corpus, emits findings and audit events.
"""

import os
from pathlib import Path

from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHttpServerParams

_PROMPT = (Path(__file__).parent / "prompts" / "vsm.md").read_text()

root_agent = Agent(
    model="claude-sonnet-4-6",
    name="alx",
    description="ALX — Canary Go VSM and Delivery Manager (Mercury Astronaut)",
    instruction=_PROMPT,
    tools=[
        MCPToolset(
            connection_params=StreamableHttpServerParams(
                url=os.environ["MEMORY_BUS_URL"] + "/mcp",
                headers={"X-API-Key": os.environ["MEMORY_BUS_API_KEY"]},
            )
        )
    ],
)
```

**Note on model string:** Vertex AI model IDs for Claude vary by region and availability.
Check the exact identifier: `gcloud ai models list --region=us-central1 --project=growdirect-mercury | grep claude`
Common format: `claude-sonnet-4-6@20260101`. Update agent.py if the string differs.

- [ ] **Step 8: Run tests to confirm they pass**

```bash
cd services/alx-agent
export MEMORY_BUS_URL="http://localhost:8003"
export MEMORY_BUS_API_KEY="test-key"
python3 -m pytest tests/test_agent.py -v
```

Expected: all 4 tests PASSED.

- [ ] **Step 9: Local ADK smoke test against Docker memory bus**

```bash
export MEMORY_BUS_URL="http://localhost:8003"
export MEMORY_BUS_API_KEY="growdirect-memory-dev-key"
cd services/alx-agent
adk run agent.py
```

At the ADK prompt type: `Recall the NCR Counterpoint endpoint mapping`
Expected: response cites at least one NCR card with citation.

- [ ] **Step 10: Commit**

```bash
git add services/memory-bus/memory_bus/server.py \
        services/memory-bus/memory_bus/store.py \
        services/alx-agent/
git commit -m "feat(mercury): ADK agent scaffold + audit_event MCP tool (GRO-806)"
```

---

## Chunk 4: Deploy + Seed + Verify + Smoke (GRO-808, GRO-810, GRO-811, GRO-812)

### Task 6: Deploy ALX to Agent Engine (GRO-808)

**Files:** No new files — deploy config only.

- [ ] **Step 1: Confirm Cloud Run memory bus URL is available**

```bash
SERVICE_URL=$(gcloud secrets versions access latest \
  --secret=memory-bus-url --project=growdirect-mercury)
echo "Memory bus: $SERVICE_URL"
```

Expected: a valid `https://memory-bus-*.run.app` URL.

- [ ] **Step 2: Check Agent Engine pricing**

```bash
gcloud ai operations list --region=us-central1 --project=growdirect-mercury 2>/dev/null || true
# Check https://cloud.google.com/vertex-ai/pricing for Agent Engine cost
# Flag to founder before proceeding if per-hour billing applies at dev scale
```

- [ ] **Step 3: Deploy to Agent Engine**

```bash
cd services/alx-agent

API_KEY=$(gcloud secrets versions access latest \
  --secret=memory-bus-api-key --project=growdirect-mercury)
SERVICE_URL=$(gcloud secrets versions access latest \
  --secret=memory-bus-url --project=growdirect-mercury)

adk deploy agent.py \
  --project=growdirect-mercury \
  --region=us-central1 \
  --service-account=alx-agent@growdirect-mercury.iam.gserviceaccount.com \
  --env MEMORY_BUS_URL="$SERVICE_URL" \
  --env MEMORY_BUS_API_KEY="$API_KEY"
```

If `adk deploy` is not yet available in your ADK version, use the manual Cloud Run deploy path:
```bash
docker build -t gcr.io/growdirect-mercury/alx-agent:latest .
docker push gcr.io/growdirect-mercury/alx-agent:latest
gcloud run deploy alx-agent \
  --image=gcr.io/growdirect-mercury/alx-agent:latest \
  --region=us-central1 \
  --project=growdirect-mercury \
  --service-account=alx-agent@growdirect-mercury.iam.gserviceaccount.com \
  --set-secrets="MEMORY_BUS_API_KEY=memory-bus-api-key:latest" \
  --set-env-vars="MEMORY_BUS_URL=$SERVICE_URL"
```

- [ ] **Step 4: Record the Agent Engine endpoint**

```bash
# Get the Agent Engine or Cloud Run URL
AGENT_URL=$(gcloud run services describe alx-agent \
  --region=us-central1 \
  --project=growdirect-mercury \
  --format='value(status.url)' 2>/dev/null || \
  adk list --project=growdirect-mercury --region=us-central1 | grep alx)
echo "Agent endpoint: $AGENT_URL"

# Store it
echo -n "$AGENT_URL" | gcloud secrets versions add vertex-agent-key \
  --data-file=- --project=growdirect-mercury
```

- [ ] **Step 5: Commit endpoint URL to README**

```bash
cat > services/alx-agent/README.md << EOF
# ALX Agent

VSM / Delivery Manager — Mercury Astronaut.

**Agent Engine endpoint:** $(gcloud secrets versions access latest --secret=vertex-agent-key --project=growdirect-mercury)

**Memory bus:** $(gcloud secrets versions access latest --secret=memory-bus-url --project=growdirect-mercury)/mcp

Deployed: $(date -u +%Y-%m-%d)
EOF

git add services/alx-agent/README.md
git commit -m "feat(mercury): Agent Engine deploy — ALX on Vertex AI (GRO-808)"
```

---

### Task 7: Seed Clean Knowledge (GRO-810)

- [ ] **Step 1: Start Cloud SQL proxy**

```bash
cloud-sql-proxy growdirect-mercury:us-central1:mercury &
PROXY_PID=$!
sleep 3
```

- [ ] **Step 2: Export connection string and run scoped seed**

```bash
export DATABASE_URL=$(gcloud secrets versions access latest \
  --secret=cloudsql-url --project=growdirect-mercury)

# Define include paths as a single variable — no line continuations inside the string
INCLUDE="Brain/wiki/cards/canary-*.md,Brain/wiki/cards/ncr-*.md,Brain/wiki/cards/ruptiv-*.md,Brain/wiki/cards/store-ops-capability-model.md,Brain/wiki/cards/platform-thesis.md,Brain/wiki/cards/execution-primer-template.md,Brain/wiki/cards/competitive-landscape.md,Brain/wiki/cards/canary-os-thesis.md,Brain/projects/Canary.md,Brain/projects/RetailSpine.md"

cd /Users/gclyle/GrowDirect
python3 services/memory-bus/scripts/seed_standalone.py \
  --drop-first \
  --include-paths "$INCLUDE"
```

- [ ] **Step 3: Verify seed results**

```bash
psql "$DATABASE_URL" -c "SELECT COUNT(*) FROM alx_memories WHERE session_id='seed-standalone';"
# Expected: 40-60 rows

psql "$DATABASE_URL" -c "SELECT content FROM alx_memories WHERE content ILIKE '%NCR%' LIMIT 1;"
# Expected: NCR-related card content
```

- [ ] **Step 4: Spot-check via memory bus MCP endpoint**

```bash
API_KEY=$(gcloud secrets versions access latest \
  --secret=memory-bus-api-key --project=growdirect-mercury)
SERVICE_URL=$(gcloud secrets versions access latest \
  --secret=memory-bus-url --project=growdirect-mercury)

curl -s \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"method":"tools/call","params":{"name":"memory_recall","arguments":{"query":"NCR Counterpoint endpoint mapping","limit":3}}}' \
  "$SERVICE_URL/mcp" | python3 -m json.tool | head -30
```

Expected: JSON with at least one result containing NCR card content.

```bash
kill $PROXY_PID
```

---

### Task 8: MCP Verification + Smoke Test (GRO-811 + GRO-812)

- [ ] **Step 1: Invoke ALX on Agent Engine with recall prompt**

```bash
AGENT_URL=$(gcloud secrets versions access latest \
  --secret=vertex-agent-key --project=growdirect-mercury)
API_KEY=$(gcloud secrets versions access latest \
  --secret=memory-bus-api-key --project=growdirect-mercury)

# Via ADK CLI or direct HTTP — adjust to your ADK version
adk invoke \
  --project=growdirect-mercury \
  --region=us-central1 \
  --agent=alx \
  --message="Recall the NCR Counterpoint endpoint mapping"
```

- [ ] **Step 2: Check Agent Engine logs for successful tool call (GRO-811)**

```bash
gcloud logging read \
  'resource.type="aiplatform.googleapis.com/Agent"' \
  --project=growdirect-mercury \
  --limit=20 \
  --format='value(textPayload)' | grep -E "memory_recall|tool_call|error"
```

Expected: `memory_recall` tool call logged, no errors, latency < 2s. Record baseline latency in a comment on GRO-811.

- [ ] **Step 3: Run end-to-end smoke test dispatch with timing (GRO-812)**

```bash
START=$(date +%s%3N)

adk invoke \
  --project=growdirect-mercury \
  --region=us-central1 \
  --agent=alx \
  --message="Summarize the NCR RapidPOS integration architecture"

END=$(date +%s%3N)
echo "Latency: $((END - START))ms"
# Expected: < 5000ms
```

- [ ] **Step 4: Verify finding + audit event written to Cloud SQL**

```bash
cloud-sql-proxy growdirect-mercury:us-central1:mercury &
PROXY_PID=$!
sleep 3

export DATABASE_URL=$(gcloud secrets versions access latest \
  --secret=cloudsql-url --project=growdirect-mercury)

# Finding check
psql "$DATABASE_URL" -c \
  "SELECT id, memory_type, created_at FROM alx_memories WHERE memory_type='finding' ORDER BY created_at DESC LIMIT 1;"
# Expected: one row with memory_type='finding', recent timestamp

# Audit event check
psql "$DATABASE_URL" -c \
  "SELECT id, event_type, layer, created_at FROM audit_events ORDER BY created_at DESC LIMIT 1;"
# Expected: one row, recent timestamp

kill $PROXY_PID
```

- [ ] **Step 5: Confirm all 5 smoke test pass criteria**

Checklist:
- [ ] No errors in Agent Engine logs
- [ ] Finding row in `alx_memories` (memory_type='finding')
- [ ] Audit event row in `audit_events`
- [ ] Response cited at least one CRB card by name
- [ ] End-to-end latency < 5s (verified by `$((END - START))ms` output above)

- [ ] **Step 6: Post results to GRO-812 and mark sprint complete**

Post a comment on GRO-812 with:
- Timestamp
- Agent Engine endpoint URL
- Memory bus Cloud Run URL
- Latency baseline (from GRO-811)
- SQL query results confirming finding + audit event

- [ ] **Step 7: Final commit**

```bash
git add -A
git commit -m "feat(mercury): splashdown complete — ALX live on Agent Engine (GRO-812)"
```

---

## Post-Splashdown: Cut-Over Prep (not part of this sprint)

After May 12 demo passes:
1. File a new dispatch for Docker decommission
2. Decide on `.mcp.json` dual-profile strategy (option a in SDD) before routing Claude Code to cloud memory bus
3. Verify Obsidian MCP still points to local vault (unaffected by memory bus migration)
