---
classification: internal
type: sdd
status: draft
date: 2026-05-05
sprint: mercury-splashdown
owner: ALX
linear: pending
companion: Brain/wiki/cards/ruptiv-architecture-partnership-decision.md
---

# SDD — Mercury Splashdown

**Parallel track. SDLC-gated. Rapid.**

GrowDirect's existing Claude Code CLI + Docker memory bus continues running
untouched. Alongside it, this sprint stands up ALX on Vertex AI Agent Engine
with a GCP-hosted memory bus scoped to CRB/Canary Go/NCR RapidPOS knowledge.
May 12 demo runs on Agent Engine. Docker stack decommissioned post-demo.

---

## Context

| Item | State |
|---|---|
| Agent runtime | Claude Code CLI on mini (Docker-dependent) |
| Memory bus | pgvector container at 127.0.0.1:8003 |
| MCP tools | .mcp.json local-only |
| Knowledge scope | Full GrowDirect Brain vault |
| Production deploy | None — local only |

**Target state post-splashdown:**

| Item | State |
|---|---|
| Agent runtime | ALX on Vertex AI Agent Engine (ADK-built) |
| Memory bus | AlloyDB + Cloud Run, GCP-hosted |
| MCP tools | Cloud Run endpoints, reachable from Agent Engine |
| Knowledge scope | CRB + Canary Go capability cards + NCR RapidPOS only |
| Mini | Dev workstation — builds and tests ADK agents locally |

---

## Architecture

```
GROWDIRECT GCP PROJECT (growdirect-mercury)
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│   Vertex AI Agent Engine                                     │
│   └── ALX Agent (ADK)  ←── VSM / Astronaut role             │
│         └── dispatches imprints                             │
│                                                              │
│   Cloud Run Services                                         │
│   ├── memory-bus   :8003  ←── MCP endpoint (tool layer)     │
│   └── [future: connector MCP servers]                       │
│                                                              │
│   AlloyDB (postgres-compatible)                              │
│   └── mercury db                                            │
│         ├── memory_bus schema (pgvector)                    │
│         └── audit_events table (append-only)                │
│                                                              │
│   Cloud Storage                                              │
│   └── mercury-artifacts  ←── transcripts, captures          │
│                                                              │
└──────────────────────────────────────────────────────────────┘

EXISTING (parallel, untouched)
┌──────────────────────────────────┐
│  Claude Code CLI (laptop/mini)   │
│  Docker memory bus (:8003)       │
│  Full Brain vault                │
└──────────────────────────────────┘
```

---

## Components — Eight, Sequenced

### 1 — GCP Project Baseline

**What:** Dedicated GCP project `growdirect-mercury`. Billing attached.
IAM service accounts for Agent Engine, Cloud Run, AlloyDB. Workload Identity
Federation configured. Secret Manager for connection strings and API keys.

**Prereqs:** None.

**Outputs:**
- Project ID: `growdirect-mercury`
- Service accounts: `alx-agent@`, `memory-bus@`, `alloydb-client@`
- Secrets: `alloydb-url`, `memory-bus-api-key`, `vertex-agent-key`

---

### 2 — AlloyDB Instance

**What:** Single AlloyDB cluster in `us-central1`. Primary instance.
Database: `mercury`. pgvector extension enabled.

**Decision — AlloyDB vs Cloud SQL:** At splashdown scale (~60 docs, low
QPS) Cloud SQL postgres is cheaper and simpler. AlloyDB is the upgrade
path when cross-engagement pattern indexing requires it. This sprint uses
**Cloud SQL** (postgres 17, pgvector extension). Connection via Cloud SQL
Auth Proxy or connector library — no AlloyDB connector dependency needed.
Update Component 1 service account to `cloudsql-client` role instead of
`alloydb-client`.

**Prereqs:** Component 1 (GCP project, service accounts).

**Schema — new migration required (blocking):**

The existing Alembic migrations create `vector(1024)` columns sized for
`qwen3-embedding:8b`. Vertex AI `text-embedding-004` produces 768-dim
vectors. pgvector enforces column dimension at insert — a dimension
mismatch causes hard failures. Because this is a fresh instance with
`--drop-first` seeding, the solution is a mercury-specific baseline
migration that overrides the column dimension:

```sql
-- migrations/versions/007_mercury_dimension_768.py
-- Applies AFTER existing baseline migrations
ALTER TABLE alx_memories ALTER COLUMN embedding TYPE vector(768);
ALTER TABLE seed_embeddings ALTER COLUMN embedding TYPE vector(768);
DROP INDEX IF EXISTS idx_alx_memories_embedding;
CREATE INDEX idx_alx_memories_embedding
  ON alx_memories USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);
```

This migration runs after the standard chain
(`001_baseline` → `002_...` → `006_...` → `007_mercury_dimension_768`).

**Audit events table (required for smoke test):**

```sql
-- included in 007_mercury_dimension_768.py
CREATE TABLE IF NOT EXISTS audit_events (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  artifact_id UUID,
  event_type  TEXT NOT NULL,
  layer       TEXT NOT NULL,
  payload     JSONB,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

**Findings:** stored in `alx_memories` with `memory_type = 'finding'`.
No separate findings table. Smoke test queries filter on this column.

**Connection:** Private IP only. Cloud Run services connect via Cloud SQL
Auth Proxy sidecar (standard pattern, no additional library changes).

**Outputs:**
- Cloud SQL instance URI
- `mercury` database with migration 007 applied
- Connection string in Secret Manager

---

### 3 — Memory Bus on Cloud Run

**What:** `services/memory-bus/` containerized and deployed to Cloud Run.
Connection string swapped from localhost pgvector to AlloyDB. No code
changes to the service itself — only environment variables change.

**Prereqs:** Components 1 + 2.

**Environment variables (Cloud Run):**
```
DATABASE_URL=<alloydb-url from Secret Manager>
MEMORY_BUS_API_KEY=<from Secret Manager>
EMBED_MODEL=text-embedding-004          # Vertex AI embeddings
EMBED_BASE_URL=<Vertex AI endpoint>
PORT=8003
```

**Notes:**
- `growdirect-mcp` sibling package ships in the same image (Dockerfile
  already handles this).
- Switch from Ollama `qwen3-embedding:8b` to Vertex AI
  `text-embedding-004` for cloud-native embeddings. Dimension: 768.
  AlloyDB vector column dimension updated accordingly.
- MCP endpoint: `https://memory-bus-<hash>-uc.a.run.app/mcp`
- Auth: API key in `X-API-Key` header (unchanged from local protocol).

**Outputs:**
- Cloud Run service URL
- MCP endpoint reachable from public internet (locked to API key)

---

### 4 — Clean Knowledge Seed

**What:** Seed AlloyDB with CRB/Canary Go/NCR RapidPOS knowledge only.
No personal/property/Cove/Angel content. Fresh embed run against
the scoped card set.

**Prereqs:** Component 3 (memory bus running, AlloyDB reachable).

**Source paths (scoped):**
```
Brain/wiki/cards/canary-*.md
Brain/wiki/cards/ncr-*.md
Brain/wiki/cards/ruptiv-*.md
Brain/wiki/cards/store-ops-capability-model.md
Brain/wiki/cards/platform-thesis.md
Brain/wiki/cards/execution-primer-template.md
Brain/wiki/cards/competitive-landscape.md
Brain/wiki/cards/canary-os-thesis.md
Brain/projects/Canary.md
Brain/projects/RetailSpine.md
CanaryGo/docs/
```

**Excluded explicitly:**
```
Brain/wiki/cards/agent-cove-builder.md
Brain/wiki/cards/agent-auditor.md
Brain/raw/
Brain/projects/Cove.md
Brain/projects/Angel.md
Seacove/
```

**Seed script — scope filtering (GRO-D prerequisite work):**

`seed_standalone.py` does not currently support `--include-paths` or
`--database-url` flags. Before GRO-D can execute, GRO-C must add:
- `--include-paths` flag (comma-separated glob patterns, matched against
  file paths relative to repo root)
- `DATABASE_URL` read from environment (already the case) — document
  explicitly so the Cloud Run deploy passes it via Secret Manager

Until those flags exist, the seed runs with `DATABASE_URL` exported
directly and a pre-filtered file list piped in. The GRO-C ticket must
include this script update as a deliverable.

**Run (with updated script):**
```bash
export DATABASE_URL=$(gcloud secrets versions access latest \
  --secret=alloydb-url --project=growdirect-mercury)

python3 services/memory-bus/scripts/seed_standalone.py \
  --include-paths \
    "Brain/wiki/cards/canary-*.md,\
     Brain/wiki/cards/ncr-*.md,\
     Brain/wiki/cards/ruptiv-*.md,\
     Brain/wiki/cards/store-ops-capability-model.md,\
     Brain/wiki/cards/platform-thesis.md,\
     Brain/wiki/cards/execution-primer-template.md,\
     Brain/wiki/cards/competitive-landscape.md,\
     Brain/wiki/cards/canary-os-thesis.md,\
     Brain/projects/Canary.md,\
     Brain/projects/RetailSpine.md,\
     CanaryGo/docs/" \
  --drop-first
```

Note: seed script writes directly to the database (not via Cloud Run MCP
endpoint), bypassing the 60-second Cloud Run timeout. AlloyDB connection
used directly from the dev machine via Cloud SQL proxy.

**Outputs:**
- Seeded database with ~40-60 documents
- Seed log confirming card count and `text-embedding-004` embedding model

---

### 5 — ADK Agent Scaffold

**What:** ALX agent built with Google ADK. VSM / Astronaut role.
Minimum viable agent: accepts an imprint dispatch, calls memory bus
MCP tool for vector recall, emits a finding.

**Prereqs:** Component 1 (GCP project, service accounts).

**Location:** `services/alx-agent/` (new directory in GrowDirect repo).

**ADK structure:**
```
services/alx-agent/
├── agent.py          ← root agent definition (ALX / Astronaut)
├── tools.py          ← MCP tool wrappers
├── prompts/
│   └── vsm.md        ← ALX system prompt (VSM/Delivery Manager role)
└── pyproject.toml
```

**ALX system prompt scope:**
- VSM / Astronaut role (Mercury chain of command)
- Authority: dispatches imprints, calls memory bus tools, emits findings
- Knowledge scope: Canary Go / NCR RapidPOS / CRB only
- No GrowDirect personal/Cove/Angel context

**MCP tool wiring:**
```python
# tools.py — wraps memory bus MCP endpoint
memory_recall = MCPTool(
    endpoint=os.environ["MEMORY_BUS_URL"],
    api_key=os.environ["MEMORY_BUS_API_KEY"],
    tool_name="memory_recall"
)
```

**Outputs:**
- `services/alx-agent/` committed
- Local ADK test passes (`adk run agent.py`)

---

### 6 — Agent Engine Deployment

**What:** ALX agent deployed to Vertex AI Agent Engine. One-command
deploy via ADK CLI.

**Prereqs:** Components 1 + 5 (GCP project + ADK scaffold).

**Deploy:**
```bash
cd services/alx-agent
adk deploy agent.py \
  --project growdirect-mercury \
  --region us-central1 \
  --env MEMORY_BUS_URL=<cloud-run-url> \
  --env MEMORY_BUS_API_KEY=<secret>
```

**Outputs:**
- Agent Engine endpoint URL
- Agent ID in `growdirect-mercury` project
- Agent callable from Claude Code via API key

---

### 7 — MCP Endpoint Reachable from Agent Engine

**What:** Verify that ALX running on Agent Engine can reach the memory
bus MCP endpoint on Cloud Run. Network path: Agent Engine → Cloud Run
(same GCP project, no VPC peering required). API key auth confirmed.

**Prereqs:** Components 3 + 6.

**Test:**
```bash
# From Agent Engine test invocation:
# ALX calls memory_recall("NCR Counterpoint endpoint mapping")
# Expects: at least one card returned with citation
```

**Outputs:**
- Confirmed tool call success in Agent Engine logs
- Latency baseline recorded (target < 2s round-trip)

---

### 8 — Smoke Test

**What:** End-to-end splashdown verification. ALX dispatches one
imprint, recalls one card, emits one finding, audit-event written.
If this passes, splashdown is complete.

**Prereqs:** All components 1-7.

**Scenario:**
```
Dispatch: "Summarize the NCR RapidPOS integration architecture"
Expected:
  - memory_recall returns ncr-ecosystem-2026.md citation
  - ALX emits finding (written to AlloyDB findings table)
  - audit-event appended to audit_events table
  - Response in < 5s
```

**Pass criteria:**
- No errors in Agent Engine logs
- Finding record in `alx_memories` where `memory_type = 'finding'`
- Audit event row in `audit_events` table
- Response cites at least one CRB card

---

## Dependency Graph

```
1 → 2 → 3 → 4
1 → 5 → 6 → 7 (requires 3) → 8 (requires 4+6+7)
```

**Critical path:** 1 → 5 → 6 → 7 → 8  (ADK scaffold is on the critical path)
**Parallel track A:** 1 → 2 → 3 → 4  (infra + seed, unblocks 7)
**Merge point:** 7 requires both 3 (memory bus live) and 6 (Agent Engine live)

---

## Linear Sprint — 8 GRO Tickets

| # | Title | Prereqs | Priority |
|---|---|---|---|
| GRO-A | GCP project baseline — `growdirect-mercury`, IAM, secrets | — | Urgent |
| GRO-B | AlloyDB instance — `mercury` db, pgvector, private IP | GRO-A | Urgent |
| GRO-C | Memory bus Cloud Run deploy — AlloyDB connection | GRO-B | Urgent |
| GRO-D | Clean knowledge seed — CRB/CanaryGo/NCR only | GRO-C | High |
| GRO-E | ADK agent scaffold — ALX VSM/Astronaut, local test | GRO-A | Urgent |
| GRO-F | Agent Engine deploy — ALX on Vertex | GRO-E | Urgent |
| GRO-G | MCP endpoint verification — Agent Engine → Cloud Run | GRO-C + GRO-F | High |
| GRO-H | Smoke test — end-to-end imprint → finding → audit | GRO-D + GRO-G | High |

All tickets filed in the `Dispatch` project. Target: `any`. Agent: `ALX`.

---

## What This Is Not

- Not a Mercury substrate build (imprint schema, charter signing, A2A
  wiring, propagation agents) — those are the next sprint
- Not a Canary Go code migration — CanaryGo stays in its own stack
- Not a Brain vault migration — full vault stays local/Obsidian
- Not a Docker decommission — Docker runs until post-demo cut-over

---

## Cut-Over Gate

After May 12 demo passes smoke test on Agent Engine:

1. Docker memory bus stack parked (`docker compose stop`)
2. Mini `.mcp.json` updated to point to Cloud Run endpoint
3. Local Claude Code sessions route to cloud memory bus
4. Docker stack decommissioned (GRO ticket filed separately)

**Important:** Post-cut-over, local Claude Code sessions calling
`memory_recall` will query the cloud memory bus which holds only
~60 scoped documents (CRB/Canary Go/NCR). Queries for Cove, Angel,
or personal Brain content will return empty results with no warning.
Two options: (a) maintain a local `.mcp.json` profile for full-vault
work that still points to the Docker bus, or (b) accept the scope
restriction and route full-vault queries through Obsidian search
instead. Decision required before cut-over. Default: option (a).

---

## Open Questions

| Q | Owner | Status |
|---|---|---|
| Vertex AI `text-embedding-004` vs `textembedding-gecko` — which for retail domain? | ALX | Open — default to `text-embedding-004` (newer, higher quality) |
| AlloyDB vs Cloud SQL | ALX | **Resolved — Cloud SQL for splashdown sprint** |
| Agent Engine pricing model — per-call or per-hour? | ALX | Open — verify before GRO-F |
| Cut-over `.mcp.json` profile strategy — dual profile vs. scope restriction | ALX | Open — resolve before cut-over, not before splashdown |
