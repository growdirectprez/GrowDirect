# Platform Memory Bus — Implementation Plan

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extract ALX ops memory from Canary into a standalone MCP server using the official Python SDK, making organizational knowledge accessible to all GrowDirect apps.

**Architecture:** Standalone FastMCP service at `~/GrowDirect/services/memory-bus/` with stdio + Streamable HTTP transports. Extracts business logic from `canary/services/alx/memory.py`, wraps 7 functions as MCP tools. Runs as Docker container on the shared `growdirect` network, port 8003.

**Tech Stack:** Python 3.12 / MCP Python SDK (FastMCP) / SQLAlchemy 2.0 / pgvector / PostgreSQL 17 / Ollama (qwen3-embedding:8b)

**Spec:** `docs/superpowers/specs/2026-03-30-platform-memory-bus-design.md`

**GRO Issue:** GRO-172

---

## File Structure

| Action | File | Responsibility |
|--------|------|----------------|
| Create | `services/memory-bus/pyproject.toml` | Dependencies and project metadata |
| Create | `services/memory-bus/Dockerfile` | Container build for memory bus |
| Create | `services/memory-bus/memory_bus/__init__.py` | Package init |
| Create | `services/memory-bus/memory_bus/config.py` | Environment-based configuration |
| Create | `services/memory-bus/memory_bus/embeddings.py` | Ollama embedding generation |
| Create | `services/memory-bus/memory_bus/store.py` | All DB operations (extracted from memory.py) |
| Create | `services/memory-bus/memory_bus/server.py` | FastMCP server with 7 tool declarations |
| Create | `services/memory-bus/tests/__init__.py` | Test package |
| Create | `services/memory-bus/tests/conftest.py` | Test fixtures (DB session, MCP client) |
| Create | `services/memory-bus/tests/test_config.py` | Config loading tests |
| Create | `services/memory-bus/tests/test_embeddings.py` | Embedding generation tests |
| Create | `services/memory-bus/tests/test_store.py` | Store operation tests |
| Create | `services/memory-bus/tests/test_server.py` | MCP tool integration tests |
| Modify | `devops/init-db/01-create-databases.sql` | Rename canary_memory → growdirect_memory, remove memory DDL |
| Move | `Canary/devops/init-db/02-create-memory-db.sql` → `devops/init-db/02-create-memory-db.sql` | Canonical DDL for growdirect_memory tables |
| Modify | `devops/init-db/02-create-memory-db.sql` | Fix CHECK constraint, add layer column, add updated_at |
| Modify | `devops/docker-compose.yml` | Add memory-bus service |
| Move | `Canary/devops/scripts/seed_*.py` → `services/memory-bus/scripts/` | Seed scripts |
| Modify | `Canary/canary/services/owl/institutional.py` | Replace direct import with MCP client call |
| Delete | `Canary/canary/services/alx/memory.py` | Ops memory code extracted |
| Delete | `Canary/canary/services/alx/tools.py` | MCP tool handlers extracted |
| Delete | `Canary/canary/blueprints/alx_api.py` | ALX API blueprint extracted |
| Delete | `Canary/devops/scripts/enrich_cognee_batch.py` | Stale (GRO-198) |
| Delete | `Canary/devops/scripts/embed_seeds.py` | Superseded |
| Delete | `Canary/devops/scripts/refine_tier1_memories.py` | One-time, already applied |
| Delete | `Canary/devops/scripts/sync_vault_to_pgvector.py` | Superseded by MCP |

---

## Chunk 1: Service Scaffold and Config

### Task 1: Project scaffold

**Files:**
- Create: `services/memory-bus/pyproject.toml`
- Create: `services/memory-bus/memory_bus/__init__.py`

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p ~/GrowDirect/services/memory-bus/memory_bus
mkdir -p ~/GrowDirect/services/memory-bus/tests
mkdir -p ~/GrowDirect/services/memory-bus/scripts
```

- [ ] **Step 2: Write pyproject.toml**

```toml
[project]
name = "memory-bus"
version = "0.1.0"
description = "GrowDirect platform memory bus — MCP server for organizational knowledge"
requires-python = ">=3.12"
dependencies = [
    "mcp[cli]>=1.9.0",
    "sqlalchemy>=2.0",
    "pgvector>=0.3.0",
    "psycopg2-binary>=2.9",
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

- [ ] **Step 3: Write `__init__.py`**

```python
"""GrowDirect Platform Memory Bus — MCP server for organizational knowledge."""
```

- [ ] **Step 4: Commit**

```bash
git add services/memory-bus/
git commit -m "scaffold: memory-bus service project structure (GRO-172)"
```

---

### Task 2: Config module

**Files:**
- Create: `services/memory-bus/memory_bus/config.py`
- Create: `services/memory-bus/tests/test_config.py`
- Create: `services/memory-bus/tests/__init__.py`
- Create: `services/memory-bus/tests/conftest.py`

- [ ] **Step 1: Write failing test**

```python
# services/memory-bus/tests/test_config.py
import os
import pytest
from memory_bus.config import Config


class TestConfig:
    def test_database_url_from_env(self, monkeypatch):
        monkeypatch.setenv("DATABASE_URL", "postgresql://test:test@localhost/test_db")
        config = Config()
        assert config.database_url == "postgresql://test:test@localhost/test_db"

    def test_database_url_missing_raises(self, monkeypatch):
        monkeypatch.delenv("DATABASE_URL", raising=False)
        with pytest.raises(KeyError):
            Config()

    def test_ollama_url_default(self, monkeypatch):
        monkeypatch.setenv("DATABASE_URL", "postgresql://test:test@localhost/test_db")
        monkeypatch.delenv("OLLAMA_URL", raising=False)
        config = Config()
        assert config.ollama_url == "http://growdirect_ollama:11434"

    def test_embedding_model_default(self, monkeypatch):
        monkeypatch.setenv("DATABASE_URL", "postgresql://test:test@localhost/test_db")
        config = Config()
        assert config.embedding_model == "qwen3-embedding:8b"

    def test_port_default(self, monkeypatch):
        monkeypatch.setenv("DATABASE_URL", "postgresql://test:test@localhost/test_db")
        config = Config()
        assert config.port == 8003
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/GrowDirect/services/memory-bus && python3 -m pytest tests/test_config.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Write config module**

```python
# services/memory-bus/memory_bus/config.py
import os


class Config:
    """Environment-based configuration for the memory bus."""

    def __init__(self):
        self.database_url: str = os.environ["DATABASE_URL"]
        self.ollama_url: str = os.environ.get(
            "OLLAMA_URL", "http://growdirect_ollama:11434"
        )
        self.embedding_model: str = os.environ.get(
            "EMBEDDING_MODEL", "qwen3-embedding:8b"
        )
        self.port: int = int(os.environ.get("PORT", "8003"))
        self.embedding_dimensions: int = 1024
        self.max_text_length: int = 6000
```

- [ ] **Step 4: Write conftest.py**

```python
# services/memory-bus/tests/conftest.py
import os
import pytest

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/growdirect_memory_test",
)
os.environ.setdefault("OLLAMA_URL", "http://growdirect_ollama:11434")
os.environ.setdefault("EMBEDDING_MODEL", "qwen3-embedding:8b")
```

- [ ] **Step 5: Write tests/__init__.py**

Empty file.

- [ ] **Step 6: Run test to verify it passes**

Run: `cd ~/GrowDirect/services/memory-bus && python3 -m pytest tests/test_config.py -v`
Expected: PASS — all 5 tests green

- [ ] **Step 7: Commit**

```bash
git add services/memory-bus/memory_bus/config.py services/memory-bus/tests/
git commit -m "feat: config module with env-based settings (GRO-172)"
```

---

### Task 3: Embeddings module

**Files:**
- Create: `services/memory-bus/memory_bus/embeddings.py`
- Create: `services/memory-bus/tests/test_embeddings.py`

- [ ] **Step 1: Write failing test**

```python
# services/memory-bus/tests/test_embeddings.py
import pytest
from unittest.mock import patch, MagicMock
from memory_bus.embeddings import get_embedding
from memory_bus.config import Config


class TestGetEmbedding:
    def test_returns_list_of_floats_on_success(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "embedding": [0.1] * 1024
        }
        with patch("memory_bus.embeddings.httpx.post", return_value=mock_response):
            config = Config()
            result = get_embedding("test text", config)
            assert result is not None
            assert len(result) == 1024
            assert all(isinstance(v, float) for v in result)

    def test_returns_none_on_connection_error(self):
        with patch("memory_bus.embeddings.httpx.post", side_effect=Exception("connection refused")):
            config = Config()
            result = get_embedding("test text", config)
            assert result is None

    def test_truncates_long_text(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"embedding": [0.1] * 1024}
        with patch("memory_bus.embeddings.httpx.post", return_value=mock_response) as mock_post:
            config = Config()
            long_text = "x" * 10000
            get_embedding(long_text, config)
            call_args = mock_post.call_args
            sent_text = call_args[1]["json"]["input"]
            assert len(sent_text) <= config.max_text_length

    def test_truncates_to_1024_dimensions(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "embedding": [0.1] * 4096  # native dimension
        }
        with patch("memory_bus.embeddings.httpx.post", return_value=mock_response):
            config = Config()
            result = get_embedding("test text", config)
            assert len(result) == 1024
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/GrowDirect/services/memory-bus && python3 -m pytest tests/test_embeddings.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Write embeddings module**

Extract from `canary/services/alx/memory.py` lines 90-134, adapting to take config as parameter:

```python
# services/memory-bus/memory_bus/embeddings.py
import logging
from typing import Optional

import httpx

from memory_bus.config import Config

logger = logging.getLogger(__name__)


def get_embedding(text: str, config: Config) -> Optional[list[float]]:
    """Generate embedding vector via Ollama. Returns None if unavailable."""
    truncated = text[: config.max_text_length]
    try:
        response = httpx.post(
            f"{config.ollama_url}/api/embed",
            json={"model": config.embedding_model, "input": truncated},
            timeout=30.0,
        )
        response.raise_for_status()
        embedding = response.json()["embedding"]
        # Matryoshka truncation: native 4096d → 1024d
        return [float(v) for v in embedding[: config.embedding_dimensions]]
    except Exception:
        logger.warning("Embedding generation failed — storing without vector")
        return None
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/GrowDirect/services/memory-bus && python3 -m pytest tests/test_embeddings.py -v`
Expected: PASS — all 4 tests green

- [ ] **Step 5: Commit**

```bash
git add services/memory-bus/memory_bus/embeddings.py services/memory-bus/tests/test_embeddings.py
git commit -m "feat: embeddings module with Ollama integration (GRO-172)"
```

---

## Chunk 2: Store Module (Core Business Logic)

### Task 4: Store module — DB engine and health check

**Files:**
- Create: `services/memory-bus/memory_bus/store.py`
- Create: `services/memory-bus/tests/test_store.py`

- [ ] **Step 1: Write failing test**

```python
# services/memory-bus/tests/test_store.py
import pytest
from memory_bus.config import Config
from memory_bus.store import MemoryStore


class TestMemoryStoreInit:
    def test_creates_engine(self):
        config = Config()
        store = MemoryStore(config)
        assert store._engine is not None

    def test_health_check_returns_bool(self):
        config = Config()
        store = MemoryStore(config)
        result = store.healthy()
        assert isinstance(result, bool)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/GrowDirect/services/memory-bus && python3 -m pytest tests/test_store.py::TestMemoryStoreInit -v`
Expected: FAIL with `ImportError`

- [ ] **Step 3: Write store module skeleton**

Extract from `memory.py` lines 38-78. Convert from module-level globals to a class:

```python
# services/memory-bus/memory_bus/store.py
import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

from memory_bus.config import Config
from memory_bus.embeddings import get_embedding

logger = logging.getLogger(__name__)

VALID_MEMORY_TYPES = frozenset([
    "decision", "finding", "context", "architecture",
    "session_summary", "procedure", "context_block",
    "work_product", "team_profile", "foundation",
])

VALID_LAYERS = frozenset(["corp", "canary", "cove", "shared"])

VALID_DOMAINS = frozenset([
    "identity", "tsp", "chirp", "alert", "owl",
    "fox", "analytics", "alx", "raas", "ops", "ui_bff",
])

VALID_BLOCK_TYPES = frozenset([
    "domain_overview", "workflow", "data_model", "api_contract",
])


class MemoryStore:
    """Core storage and retrieval operations for the memory bus."""

    def __init__(self, config: Config):
        self._config = config
        self._engine = create_engine(
            config.database_url,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
        )
        self._session_factory = sessionmaker(bind=self._engine)

    def _session(self) -> Session:
        return self._session_factory()

    def healthy(self) -> bool:
        """Check database connectivity."""
        try:
            with self._session() as session:
                session.execute(text("SELECT 1"))
                return True
        except Exception:
            return False
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/GrowDirect/services/memory-bus && python3 -m pytest tests/test_store.py::TestMemoryStoreInit -v`
Expected: PASS (requires growdirect_memory_test DB — tests run against live DB)

- [ ] **Step 5: Commit**

```bash
git add services/memory-bus/memory_bus/store.py services/memory-bus/tests/test_store.py
git commit -m "feat: store module skeleton with DB engine and health check (GRO-172)"
```

---

### Task 5: Store — session lifecycle (session_start, session_close)

**Files:**
- Modify: `services/memory-bus/memory_bus/store.py`
- Modify: `services/memory-bus/tests/test_store.py`

- [ ] **Step 1: Write failing tests**

```python
# Add to tests/test_store.py

class TestSessionLifecycle:
    def test_session_start_returns_session_id(self):
        config = Config()
        store = MemoryStore(config)
        result = store.session_start(gro_issues=["GRO-172"])
        assert "session_id" in result
        assert result["status"] == "active"

    def test_session_start_with_no_issues(self):
        config = Config()
        store = MemoryStore(config)
        result = store.session_start()
        assert "session_id" in result

    def test_session_close_marks_closed(self):
        config = Config()
        store = MemoryStore(config)
        start = store.session_start(gro_issues=["GRO-172"])
        sid = start["session_id"]
        result = store.session_close(
            session_id=sid,
            summary="Test session completed",
            decisions=["decision 1"],
            unresolved=["item 1"],
        )
        assert result["status"] == "closed"

    def test_session_close_nonexistent_returns_error(self):
        config = Config()
        store = MemoryStore(config)
        result = store.session_close(
            session_id="nonexistent-session",
            summary="Should fail",
        )
        assert "error" in result
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd ~/GrowDirect/services/memory-bus && python3 -m pytest tests/test_store.py::TestSessionLifecycle -v`
Expected: FAIL with `AttributeError`

- [ ] **Step 3: Implement session_start and session_close**

Extract from `memory.py` lines 141-255. Add as methods on `MemoryStore`:

```python
    def session_start(
        self, gro_issues: Optional[list[str]] = None
    ) -> dict[str, Any]:
        """Create a new session and assemble startup context."""
        session_id = f"alx-{uuid.uuid4().hex[:12]}"
        now = datetime.now(timezone.utc)
        gro_list = gro_issues or []

        with self._session() as db:
            db.execute(
                text("""
                    INSERT INTO alx_sessions
                        (id, session_id, started_at, status, gro_issues, created_at)
                    VALUES
                        (:id, :sid, :now, 'active', :gro, :now)
                """),
                {
                    "id": str(uuid.uuid4()),
                    "sid": session_id,
                    "now": now,
                    "gro": gro_list,
                },
            )
            db.commit()

        context = self._assemble_startup_context(gro_list)
        return {
            "session_id": session_id,
            "status": "active",
            "started_at": now.isoformat(),
            "gro_issues": gro_list,
            "startup_context": context,
        }

    def session_close(
        self,
        session_id: str,
        summary: str,
        decisions: Optional[list[str]] = None,
        unresolved: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        """Close a session with summary and decisions."""
        now = datetime.now(timezone.utc)
        import json

        with self._session() as db:
            result = db.execute(
                text("""
                    UPDATE alx_sessions
                    SET status = 'closed',
                        closed_at = :now,
                        summary = :summary,
                        decisions = :decisions,
                        unresolved = :unresolved,
                        updated_at = :now
                    WHERE session_id = :sid AND status = 'active'
                    RETURNING session_id
                """),
                {
                    "sid": session_id,
                    "now": now,
                    "summary": summary,
                    "decisions": json.dumps(decisions or []),
                    "unresolved": json.dumps(unresolved or []),
                },
            )
            row = result.fetchone()
            db.commit()

            if not row:
                return {"error": f"No active session found: {session_id}"}

        # Store summary as memory
        self.memory_store(
            session_id=session_id,
            content=summary,
            memory_type="session_summary",
        )

        return {
            "session_id": session_id,
            "status": "closed",
            "closed_at": now.isoformat(),
        }

    def _assemble_startup_context(self, gro_issues: list[str]) -> str:
        """Build startup context from recent memories and decisions."""
        parts = []
        with self._session() as db:
            # Recent decisions
            rows = db.execute(
                text("""
                    SELECT content, created_at
                    FROM alx_memories
                    WHERE memory_type = 'decision'
                    ORDER BY created_at DESC LIMIT 5
                """)
            ).fetchall()
            if rows:
                parts.append("## Recent Decisions")
                for row in rows:
                    parts.append(f"- {row[0]}")

            # GRO-specific context
            for gro in gro_issues:
                gro_rows = db.execute(
                    text("""
                        SELECT content, memory_type
                        FROM alx_memories
                        WHERE content ILIKE :pattern
                        ORDER BY created_at DESC LIMIT 3
                    """),
                    {"pattern": f"%{gro}%"},
                ).fetchall()
                if gro_rows:
                    parts.append(f"\n## Context for {gro}")
                    for row in gro_rows:
                        parts.append(f"- [{row[1]}] {row[0][:200]}")

        return "\n".join(parts) if parts else "No prior context found."
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd ~/GrowDirect/services/memory-bus && python3 -m pytest tests/test_store.py::TestSessionLifecycle -v`
Expected: PASS — all 4 tests green

- [ ] **Step 5: Commit**

```bash
git add services/memory-bus/memory_bus/store.py services/memory-bus/tests/test_store.py
git commit -m "feat: session lifecycle — start and close (GRO-172)"
```

---

### Task 6: Store — memory_store

**Files:**
- Modify: `services/memory-bus/memory_bus/store.py`
- Modify: `services/memory-bus/tests/test_store.py`

- [ ] **Step 1: Write failing tests**

```python
class TestMemoryStore:
    def test_store_returns_memory_id(self):
        config = Config()
        store = MemoryStore(config)
        start = store.session_start()
        result = store.memory_store(
            session_id=start["session_id"],
            content="Test memory content",
            memory_type="decision",
        )
        assert "memory_id" in result

    def test_store_with_layer(self):
        config = Config()
        store = MemoryStore(config)
        start = store.session_start()
        result = store.memory_store(
            session_id=start["session_id"],
            content="Cove-specific memory",
            memory_type="architecture",
            layer="cove",
        )
        assert result.get("layer") == "cove"

    def test_store_invalid_type_returns_error(self):
        config = Config()
        store = MemoryStore(config)
        start = store.session_start()
        result = store.memory_store(
            session_id=start["session_id"],
            content="Bad type",
            memory_type="invalid_type",
        )
        assert "error" in result

    def test_store_invalid_layer_returns_error(self):
        config = Config()
        store = MemoryStore(config)
        start = store.session_start()
        result = store.memory_store(
            session_id=start["session_id"],
            content="Bad layer",
            memory_type="decision",
            layer="invalid",
        )
        assert "error" in result
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd ~/GrowDirect/services/memory-bus && python3 -m pytest tests/test_store.py::TestMemoryStore -v`
Expected: FAIL

- [ ] **Step 3: Implement memory_store**

Extract from `memory.py` lines 262-322, add `layer` parameter:

```python
    def memory_store(
        self,
        session_id: str,
        content: str,
        memory_type: str = "context",
        metadata: Optional[dict[str, Any]] = None,
        layer: str = "shared",
    ) -> dict[str, Any]:
        """Persist a memory with optional embedding and layer tag."""
        if memory_type not in VALID_MEMORY_TYPES:
            return {"error": f"Invalid memory_type: {memory_type}. Valid: {sorted(VALID_MEMORY_TYPES)}"}
        if layer not in VALID_LAYERS:
            return {"error": f"Invalid layer: {layer}. Valid: {sorted(VALID_LAYERS)}"}

        memory_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        embedding = get_embedding(content, self._config)

        with self._session() as db:
            if embedding:
                db.execute(
                    text("""
                        INSERT INTO alx_memories
                            (id, session_id, memory_type, content, metadata,
                             embedding, layer, created_at, updated_at)
                        VALUES
                            (:id, :sid, :mtype, :content, :meta,
                             :embedding, :layer, :now, :now)
                    """),
                    {
                        "id": memory_id,
                        "sid": session_id,
                        "mtype": memory_type,
                        "content": content,
                        "meta": json.dumps(metadata or {}),
                        "embedding": str(embedding),
                        "layer": layer,
                        "now": now,
                    },
                )
            else:
                db.execute(
                    text("""
                        INSERT INTO alx_memories
                            (id, session_id, memory_type, content, metadata,
                             layer, created_at, updated_at)
                        VALUES
                            (:id, :sid, :mtype, :content, :meta,
                             :layer, :now, :now)
                    """),
                    {
                        "id": memory_id,
                        "sid": session_id,
                        "mtype": memory_type,
                        "content": content,
                        "meta": json.dumps(metadata or {}),
                        "layer": layer,
                        "now": now,
                    },
                )
            db.commit()

        return {
            "memory_id": memory_id,
            "memory_type": memory_type,
            "layer": layer,
            "has_embedding": embedding is not None,
            "created_at": now.isoformat(),
        }
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd ~/GrowDirect/services/memory-bus && python3 -m pytest tests/test_store.py::TestMemoryStore -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add services/memory-bus/
git commit -m "feat: memory_store with layer tagging and validation (GRO-172)"
```

---

### Task 7: Store — memory_recall (semantic search with fallback chain)

**Files:**
- Modify: `services/memory-bus/memory_bus/store.py`
- Modify: `services/memory-bus/tests/test_store.py`

- [ ] **Step 1: Write failing tests**

```python
class TestMemoryRecall:
    def test_recall_returns_matches(self):
        config = Config()
        store = MemoryStore(config)
        start = store.session_start()
        store.memory_store(
            session_id=start["session_id"],
            content="Secret ballot separation is required by Davis-Stirling",
            memory_type="decision",
        )
        result = store.memory_recall(query="ballot separation")
        assert "matches" in result
        assert result["count"] >= 0

    def test_recall_with_type_filter(self):
        config = Config()
        store = MemoryStore(config)
        result = store.memory_recall(
            query="test query",
            memory_type="decision",
        )
        assert "matches" in result

    def test_recall_respects_limit(self):
        config = Config()
        store = MemoryStore(config)
        result = store.memory_recall(query="test", limit=3)
        assert len(result.get("matches", [])) <= 3
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd ~/GrowDirect/services/memory-bus && python3 -m pytest tests/test_store.py::TestMemoryRecall -v`
Expected: FAIL

- [ ] **Step 3: Implement memory_recall**

Extract from `memory.py` lines 325-413. Three-tier fallback: pgvector → full-text → ILIKE:

```python
    def memory_recall(
        self,
        query: str,
        limit: int = 10,
        memory_type: Optional[str] = None,
    ) -> dict[str, Any]:
        """Semantic search with fallback chain: vector → full-text → ILIKE."""
        embedding = get_embedding(query, self._config)

        with self._session() as db:
            # Tier 1: pgvector cosine similarity
            if embedding:
                type_filter = "AND memory_type = :mtype" if memory_type else ""
                rows = db.execute(
                    text(f"""
                        SELECT id, session_id, memory_type, content, metadata,
                               layer, created_at,
                               1 - (embedding <=> :embedding::vector) AS similarity
                        FROM alx_memories
                        WHERE embedding IS NOT NULL {type_filter}
                        ORDER BY embedding <=> :embedding::vector
                        LIMIT :limit
                    """),
                    {
                        "embedding": str(embedding),
                        "limit": limit,
                        **({"mtype": memory_type} if memory_type else {}),
                    },
                ).fetchall()

                if rows:
                    return self._format_recall_results(rows, "vector", query)

            # Tier 2: Full-text search
            type_filter = "AND memory_type = :mtype" if memory_type else ""
            rows = db.execute(
                text(f"""
                    SELECT id, session_id, memory_type, content, metadata,
                           layer, created_at,
                           ts_rank(to_tsvector('english', content),
                                   plainto_tsquery('english', :query)) AS similarity
                    FROM alx_memories
                    WHERE to_tsvector('english', content) @@
                          plainto_tsquery('english', :query) {type_filter}
                    ORDER BY similarity DESC
                    LIMIT :limit
                """),
                {
                    "query": query,
                    "limit": limit,
                    **({"mtype": memory_type} if memory_type else {}),
                },
            ).fetchall()

            if rows:
                return self._format_recall_results(rows, "fulltext", query)

            # Tier 3: ILIKE fallback
            rows = db.execute(
                text(f"""
                    SELECT id, session_id, memory_type, content, metadata,
                           layer, created_at, 0.0 AS similarity
                    FROM alx_memories
                    WHERE content ILIKE :pattern {type_filter}
                    ORDER BY created_at DESC
                    LIMIT :limit
                """),
                {
                    "pattern": f"%{query}%",
                    "limit": limit,
                    **({"mtype": memory_type} if memory_type else {}),
                },
            ).fetchall()

            return self._format_recall_results(rows, "ilike", query)

    def _format_recall_results(
        self, rows: list, source: str, query: str
    ) -> dict[str, Any]:
        """Format recall results into standard response dict."""
        matches = []
        for row in rows:
            matches.append({
                "memory_id": str(row[0]),
                "session_id": row[1],
                "memory_type": row[2],
                "content": row[3],
                "metadata": row[4] if row[4] else {},
                "layer": row[5],
                "created_at": row[6].isoformat() if row[6] else None,
                "similarity": float(row[7]) if row[7] else 0.0,
            })
        return {
            "query": query,
            "matches": matches,
            "count": len(matches),
            "source": source,
        }
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd ~/GrowDirect/services/memory-bus && python3 -m pytest tests/test_store.py::TestMemoryRecall -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add services/memory-bus/
git commit -m "feat: memory_recall with three-tier search fallback (GRO-172)"
```

---

### Task 8: Store — remaining operations (memory_search, context_assemble, domain_context)

**Files:**
- Modify: `services/memory-bus/memory_bus/store.py`
- Modify: `services/memory-bus/tests/test_store.py`

- [ ] **Step 1: Write failing tests**

```python
class TestMemorySearch:
    def test_search_by_session(self):
        config = Config()
        store = MemoryStore(config)
        start = store.session_start()
        store.memory_store(
            session_id=start["session_id"],
            content="searchable content",
            memory_type="finding",
        )
        result = store.memory_search(session_id=start["session_id"])
        assert "memories" in result
        assert result["count"] >= 1

    def test_search_by_type(self):
        config = Config()
        store = MemoryStore(config)
        result = store.memory_search(memory_type="decision")
        assert "memories" in result


class TestContextAssemble:
    def test_assemble_by_topic(self):
        config = Config()
        store = MemoryStore(config)
        result = store.context_assemble(topic="ballot separation")
        assert "context" in result

    def test_assemble_by_gro_issue(self):
        config = Config()
        store = MemoryStore(config)
        result = store.context_assemble(gro_issue="GRO-172")
        assert "context" in result


class TestDomainContext:
    def test_domain_context_valid_domain(self):
        config = Config()
        store = MemoryStore(config)
        result = store.domain_context(domain="owl")
        assert "domain" in result
        assert result["domain"] == "owl"

    def test_domain_context_invalid_domain(self):
        config = Config()
        store = MemoryStore(config)
        result = store.domain_context(domain="invalid")
        assert "error" in result
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd ~/GrowDirect/services/memory-bus && python3 -m pytest tests/test_store.py::TestMemorySearch tests/test_store.py::TestContextAssemble tests/test_store.py::TestDomainContext -v`
Expected: FAIL

- [ ] **Step 3: Implement remaining store methods**

Extract from `memory.py` lines 539-912. Add `memory_search`, `context_assemble`, `recall_context_blocks`, `assemble_domain_context` (renamed to `domain_context`), and `_pick_best_workflow` as methods on `MemoryStore`. Follow the same patterns as the existing methods — raw SQL via `text()`, return dicts.

Key adaptations:
- `memory_search` — lines 539-613, structured filter
- `context_assemble` — lines 616-694, topic/GRO context builder
- `recall_context_blocks` — lines 712-781, internal helper
- `domain_context` (was `assemble_domain_context`) — lines 784-887, domain-scoped assembly
- `_pick_best_workflow` — lines 890-912, keyword overlap scorer

All take `self` as first arg instead of using module globals. All use `self._session()` instead of `_get_session()`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd ~/GrowDirect/services/memory-bus && python3 -m pytest tests/test_store.py -v`
Expected: PASS — all tests green

- [ ] **Step 5: Commit**

```bash
git add services/memory-bus/
git commit -m "feat: memory_search, context_assemble, domain_context (GRO-172)"
```

---

## Chunk 3: MCP Server

### Task 9: FastMCP server with all 7 tools

**Files:**
- Create: `services/memory-bus/memory_bus/server.py`
- Create: `services/memory-bus/tests/test_server.py`

- [ ] **Step 1: Write failing test**

```python
# services/memory-bus/tests/test_server.py
import pytest
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from memory_bus.server import mcp


class TestMCPServer:
    @pytest.mark.asyncio
    async def test_list_tools_returns_seven(self):
        async with ClientSession(*await mcp.get_streamable_http_transport()) as session:
            await session.initialize()
            tools = await session.list_tools()
            tool_names = {t.name for t in tools.tools}
            assert tool_names == {
                "memory_store", "memory_recall", "memory_search",
                "context_assemble", "session_start", "session_close",
                "domain_context",
            }

    @pytest.mark.asyncio
    async def test_session_start_roundtrip(self):
        async with ClientSession(*await mcp.get_streamable_http_transport()) as session:
            await session.initialize()
            result = await session.call_tool(
                "session_start",
                arguments={"gro_issues": ["GRO-TEST"]},
            )
            assert any("session_id" in str(c) for c in result.content)

    @pytest.mark.asyncio
    async def test_store_and_recall_roundtrip(self):
        async with ClientSession(*await mcp.get_streamable_http_transport()) as session:
            await session.initialize()
            # Start session
            start = await session.call_tool("session_start", arguments={})
            # Store
            await session.call_tool("memory_store", arguments={
                "content": "MCP integration test memory",
                "memory_type": "finding",
                "layer": "shared",
            })
            # Recall
            result = await session.call_tool("memory_recall", arguments={
                "query": "MCP integration test",
            })
            assert any("integration test" in str(c).lower() for c in result.content)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd ~/GrowDirect/services/memory-bus && python3 -m pytest tests/test_server.py -v`
Expected: FAIL with `ImportError`

- [ ] **Step 3: Implement MCP server**

```python
# services/memory-bus/memory_bus/server.py
"""GrowDirect Memory Bus — MCP server for organizational knowledge."""
import json
import logging
from typing import Optional

from mcp.server.fastmcp import FastMCP

from memory_bus.config import Config
from memory_bus.store import MemoryStore

logger = logging.getLogger(__name__)

config = Config()
store = MemoryStore(config)

mcp = FastMCP(
    "GrowDirect Memory Bus",
    description="Platform-level organizational knowledge store",
)


@mcp.tool()
def session_start(gro_issues: Optional[list[str]] = None) -> str:
    """Start a new ALX session. Optionally associate GRO issues."""
    result = store.session_start(gro_issues=gro_issues)
    return json.dumps(result, default=str)


@mcp.tool()
def session_close(
    session_id: str,
    summary: str,
    decisions: Optional[list[str]] = None,
    unresolved: Optional[list[str]] = None,
) -> str:
    """Close a session with summary, decisions, and unresolved items."""
    result = store.session_close(
        session_id=session_id,
        summary=summary,
        decisions=decisions,
        unresolved=unresolved,
    )
    return json.dumps(result, default=str)


@mcp.tool()
def memory_store(
    content: str,
    memory_type: str = "context",
    session_id: Optional[str] = None,
    metadata: Optional[dict] = None,
    layer: str = "shared",
) -> str:
    """Store a memory with embedding, layer tag, and type classification."""
    result = store.memory_store(
        session_id=session_id or "unattached",
        content=content,
        memory_type=memory_type,
        metadata=metadata,
        layer=layer,
    )
    return json.dumps(result, default=str)


@mcp.tool()
def memory_recall(
    query: str,
    limit: int = 10,
    memory_type: Optional[str] = None,
) -> str:
    """Semantic search over memories. Falls back: vector → full-text → ILIKE."""
    result = store.memory_recall(
        query=query, limit=limit, memory_type=memory_type
    )
    return json.dumps(result, default=str)


@mcp.tool()
def memory_search(
    session_id: Optional[str] = None,
    memory_type: Optional[str] = None,
    since: Optional[str] = None,
    limit: int = 20,
) -> str:
    """Structured search by session, type, or date."""
    result = store.memory_search(
        session_id=session_id,
        memory_type=memory_type,
        since=since,
        limit=limit,
    )
    return json.dumps(result, default=str)


@mcp.tool()
def context_assemble(
    topic: Optional[str] = None,
    gro_issue: Optional[str] = None,
    limit: int = 15,
) -> str:
    """Assemble a context window for a topic or GRO issue."""
    result = store.context_assemble(
        topic=topic, gro_issue=gro_issue, limit=limit
    )
    return json.dumps(result, default=str)


@mcp.tool()
def domain_context(
    domain: str,
    topic: Optional[str] = None,
    token_budget: int = 4000,
) -> str:
    """Full domain context assembly with token budget."""
    result = store.domain_context(
        domain=domain, topic=topic, token_budget=token_budget
    )
    return json.dumps(result, default=str)


# Health check for Docker healthcheck
@mcp.custom_route("/health", methods=["GET"])
async def health(request):
    from starlette.responses import JSONResponse
    healthy = store.healthy()
    return JSONResponse(
        {"service": "memory-bus", "healthy": healthy},
        status_code=200 if healthy else 503,
    )


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=config.port)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd ~/GrowDirect/services/memory-bus && python3 -m pytest tests/test_server.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add services/memory-bus/memory_bus/server.py services/memory-bus/tests/test_server.py
git commit -m "feat: FastMCP server with 7 tools and health endpoint (GRO-172)"
```

---

### Task 10: Dockerfile

**Files:**
- Create: `services/memory-bus/Dockerfile`

- [ ] **Step 1: Write Dockerfile**

```dockerfile
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY memory_bus/ memory_bus/

EXPOSE 8003

CMD ["python3", "-m", "memory_bus.server"]
```

- [ ] **Step 2: Commit**

```bash
git add services/memory-bus/Dockerfile
git commit -m "feat: Dockerfile for memory-bus service (GRO-172)"
```

---

## Chunk 4: Database Migration and Infra

### Task 11: Update init-db scripts

**Files:**
- Modify: `devops/init-db/01-create-databases.sql`
- Move + Modify: `Canary/devops/init-db/02-create-memory-db.sql` → `devops/init-db/02-create-memory-db.sql`

- [ ] **Step 1: Update 01-create-databases.sql**

Change `canary_memory` references to `growdirect_memory`. Remove memory table DDL from this file (it stays in `02-create-memory-db.sql`). Add `growdirect_memory_test` database creation.

- [ ] **Step 2: Move and update 02-create-memory-db.sql**

```bash
cp ~/GrowDirect/Canary/devops/init-db/02-create-memory-db.sql ~/GrowDirect/devops/init-db/02-create-memory-db.sql
```

Update the moved file:
- Change `\c canary_memory` → `\c growdirect_memory`
- Fix CHECK constraint on `alx_memories.memory_type` to include: `context_block`, `work_product`, `team_profile`, `foundation`
- Add `layer` column: `layer TEXT NOT NULL DEFAULT 'shared' CHECK (layer IN ('corp', 'canary', 'cove', 'shared'))`
- Add `updated_at TIMESTAMPTZ DEFAULT NOW()` to `alx_memories` and `seed_embeddings`
- Add index: `CREATE INDEX idx_alx_memories_layer ON alx_memories(layer);`
- Add update trigger for `updated_at`
- Duplicate the DDL block for `growdirect_memory_test`

- [ ] **Step 3: Commit**

```bash
git add devops/init-db/
git commit -m "db: rename canary_memory to growdirect_memory, fix schema gaps (GRO-172)"
```

---

### Task 12: Add memory-bus to docker-compose.yml

**Files:**
- Modify: `devops/docker-compose.yml`

- [ ] **Step 1: Add memory-bus service**

Add the service block from the spec (with healthcheck) after the `ollama` service. Add port 8003 to the platform port allocation.

- [ ] **Step 2: Test docker build**

```bash
cd ~/GrowDirect/devops && docker compose build memory-bus
```

Expected: builds successfully

- [ ] **Step 3: Test docker run**

```bash
cd ~/GrowDirect/devops && docker compose up -d memory-bus
docker logs growdirect_memory_bus
```

Expected: server starts, health check passes

- [ ] **Step 4: Commit**

```bash
git add devops/docker-compose.yml
git commit -m "infra: add memory-bus service to shared docker-compose (GRO-172)"
```

---

## Chunk 5: Canary Cleanup

### Task 13: Move seed scripts

**Files:**
- Move: `Canary/devops/scripts/seed_*.py` → `services/memory-bus/scripts/`
- Delete: stale scripts

- [ ] **Step 1: Move active seed scripts**

```bash
for f in seed_context_blocks.py seed_memory_foundation.py seed_work_products.py \
         seed_team_profiles.py seed_sdds_v2.py embed_memories_batch.py \
         load_memories.py ingest_tier2_batch.py field_registry_seed.py; do
    cp ~/GrowDirect/Canary/devops/scripts/$f ~/GrowDirect/services/memory-bus/scripts/$f 2>/dev/null
done
```

- [ ] **Step 2: Update imports in moved scripts**

Each script currently does `from canary.services.alx.memory import ...`. Update to:
```python
from memory_bus.store import MemoryStore
from memory_bus.config import Config
```

- [ ] **Step 3: Delete stale scripts from Canary**

```bash
rm ~/GrowDirect/Canary/devops/scripts/enrich_cognee_batch.py
rm ~/GrowDirect/Canary/devops/scripts/embed_seeds.py
rm ~/GrowDirect/Canary/devops/scripts/refine_tier1_memories.py
rm ~/GrowDirect/Canary/devops/scripts/sync_vault_to_pgvector.py
```

- [ ] **Step 4: Commit**

```bash
git add services/memory-bus/scripts/ && git add -u
git commit -m "chore: move seed scripts to memory-bus, delete stale scripts (GRO-172)"
```

---

### Task 14: Delete ops memory code from Canary

**Files:**
- Delete: `Canary/canary/services/alx/memory.py`
- Delete: `Canary/canary/services/alx/tools.py`
- Delete: `Canary/canary/blueprints/alx_api.py`
- Delete: `Canary/devops/init-db/02-create-memory-db.sql`

- [ ] **Step 1: Update institutional.py**

Replace direct import with MCP client call:

```python
# canary/services/owl/institutional.py
# Replace:
#   from canary.services.alx.memory import memory_semantic_search
# With:
async def _memory_recall_via_mcp(query: str, limit: int = 5) -> dict:
    """Query memory bus MCP for institutional context."""
    try:
        import httpx
        response = httpx.post(
            "http://growdirect_memory_bus:8003/mcp/v1/tools/memory_recall",
            json={"query": query, "limit": limit},
            timeout=5.0,
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        logger.debug("Memory bus not available for institutional context")
        return {"matches": [], "count": 0}
```

Note: The exact MCP client integration pattern depends on the SDK's HTTP client. During assembly, test option 1 (direct MCP call <5ms) first. If latency is too high, implement Valkey caching.

- [ ] **Step 2: Delete ops memory files**

```bash
rm ~/GrowDirect/Canary/canary/services/alx/memory.py
rm ~/GrowDirect/Canary/canary/services/alx/tools.py
rm ~/GrowDirect/Canary/canary/blueprints/alx_api.py
rm ~/GrowDirect/Canary/devops/init-db/02-create-memory-db.sql
```

- [ ] **Step 3: Remove moved seed scripts from Canary**

```bash
for f in seed_context_blocks.py seed_memory_foundation.py seed_work_products.py \
         seed_team_profiles.py seed_sdds_v2.py embed_memories_batch.py \
         load_memories.py ingest_tier2_batch.py field_registry_seed.py; do
    rm ~/GrowDirect/Canary/devops/scripts/$f 2>/dev/null
done
```

- [ ] **Step 4: Update any remaining imports in Canary**

Search for broken imports:
```bash
cd ~/GrowDirect/Canary && grep -rn "from canary.services.alx.memory" --include="*.py"
cd ~/GrowDirect/Canary && grep -rn "from canary.services.alx.tools" --include="*.py"
cd ~/GrowDirect/Canary && grep -rn "from canary.blueprints.alx_api" --include="*.py"
```

Fix or remove each reference found.

- [ ] **Step 5: Remove CANARY_MEMORY_DB_URL from Canary env**

Remove `CANARY_MEMORY_DB_URL` from `Canary/devops/docker-compose.yml` environment section (if present) and `Canary/.env`.

- [ ] **Step 6: Verify Canary still starts**

```bash
cd ~/GrowDirect/Canary/devops && docker compose up -d flask
docker logs canary_flask --tail 20
```

Expected: no `ImportError`, no `ModuleNotFoundError`, Owl search still works.

- [ ] **Step 7: Commit**

```bash
cd ~/GrowDirect && git add -u && git add Canary/
git commit -m "cleanup: remove ops memory code from Canary (GRO-172)"
```

---

### Task 15: Update tests

**Files:**
- Modify or move: `Canary/tests/integration/test_rag_retrieval.py`
- Modify or move: `Canary/tests/unit/test_context_blocks.py`
- Modify or move: `Canary/tests/unit/test_owl_api_sessions.py`

- [ ] **Step 1: Assess each test file**

Read each test file. Determine if it tests:
- Ops memory (→ move to `services/memory-bus/tests/`)
- Owl product knowledge (→ stays in Canary, remove memory imports)
- Both (→ split)

- [ ] **Step 2: Move or update tests accordingly**

- [ ] **Step 3: Run Canary test suite**

```bash
cd ~/GrowDirect/Canary && python3 -m pytest tests/ -v --timeout=60
```

Expected: all tests pass (ops memory tests moved, Owl tests updated)

- [ ] **Step 4: Run memory-bus test suite**

```bash
cd ~/GrowDirect/services/memory-bus && python3 -m pytest tests/ -v
```

Expected: all tests pass

- [ ] **Step 5: Commit**

```bash
git add -u && git add services/memory-bus/tests/ Canary/tests/
git commit -m "test: relocate ops memory tests to memory-bus, update Canary tests (GRO-172)"
```

---

## Chunk 6: Smoke Test and Documentation

### Task 16: End-to-end smoke test

**Files:**
- Create: `services/memory-bus/tests/test_smoke.py`

- [ ] **Step 1: Write smoke test**

```python
# services/memory-bus/tests/test_smoke.py
import pytest


class TestSmoke:
    @pytest.mark.asyncio
    async def test_store_recall_roundtrip(self):
        """Acceptance criterion: memory_store → memory_recall returns content."""
        from mcp import ClientSession
        from memory_bus.server import mcp

        async with ClientSession(*await mcp.get_streamable_http_transport()) as session:
            await session.initialize()

            # Start session
            await session.call_tool("session_start", arguments={"gro_issues": ["GRO-SMOKE"]})

            # Store with layer
            await session.call_tool("memory_store", arguments={
                "content": "Secret ballot separation is required by Davis-Stirling Civil Code 5100",
                "memory_type": "decision",
                "layer": "cove",
            })

            # Recall
            result = await session.call_tool("memory_recall", arguments={
                "query": "secret ballot separation",
            })

            content_str = str(result.content)
            assert "ballot" in content_str.lower() or "separation" in content_str.lower()
```

- [ ] **Step 2: Run smoke test**

Run: `cd ~/GrowDirect/services/memory-bus && python3 -m pytest tests/test_smoke.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add services/memory-bus/tests/test_smoke.py
git commit -m "test: end-to-end smoke test for memory bus (GRO-172)"
```

---

### Task 17: Update CLAUDE.md port allocation

**Files:**
- Modify: `~/GrowDirect/CLAUDE.md`

- [ ] **Step 1: Add memory bus to port allocation table**

Add row: `| Memory Bus MCP | 8003 |`

- [ ] **Step 2: Update Database Layout table**

Add rows for `growdirect_memory` and `growdirect_memory_test`. Remove `canary_memory` reference.

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: add memory bus to port allocation and database layout (GRO-172)"
```
