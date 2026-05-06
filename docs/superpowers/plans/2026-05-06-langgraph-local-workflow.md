# LangGraph Local Workflow + Portal Releases Panel — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Local LangGraph workflow (codegen + deploy graphs) with a Canary devops portal approval panel, deployable to GCP using idling resources.

**Architecture:** Two subsystems sharing a REST API boundary. Python `langgraph/` package runs locally via `langgraph dev`. Go `internal/devops/` portal talks to the LangGraph server API — never the checkpoint store. Same code runs local and on Cloud Run via `LANGGRAPH_URL` env var.

**Tech Stack:** Python 3.12+, uv, LangGraph 0.2+, langchain-anthropic, pytest — Go 1.22+, Chi v5, pgx/v5, httptest

---

## Chunk 1: LangGraph Python package

### Task 1: Scaffold `langgraph/` package

**Files:**
- Create: `langgraph/pyproject.toml`
- Create: `langgraph/langgraph.json`
- Create: `langgraph/Makefile`
- Create: `langgraph/.env.example`
- Create: `langgraph/graphs/__init__.py`
- Create: `langgraph/graphs/nodes/__init__.py`
- Create: `langgraph/tests/__init__.py`

- [ ] **Step 1: Create `langgraph/pyproject.toml`**

```toml
[project]
name = "canary-orchestrator"
version = "0.1.0"
description = "LangGraph local workflow for Canary Go code generation and deployment"
requires-python = ">=3.12"
dependencies = [
    "langgraph>=0.2.0",
    "langgraph-cli>=0.1.0",
    "langchain-anthropic>=0.3.0",
    "langchain-core>=0.3.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]

[tool.pyright]
pythonVersion = "3.12"
typeCheckingMode = "basic"
```

- [ ] **Step 2: Install deps and generate lockfile**

```bash
cd langgraph
uv sync --dev
```

Expected: `uv.lock` created, `.venv/` created.

- [ ] **Step 3: Create `langgraph/langgraph.json`**

```json
{
  "dependencies": ["."],
  "graphs": {
    "codegen": "./graphs/codegen.py:graph",
    "deploy": "./graphs/deploy.py:graph"
  },
  "env": ".env"
}
```

- [ ] **Step 4: Create `langgraph/Makefile`**

```makefile
.PHONY: dev test build lint

dev:
	uv run langgraph dev

test:
	uv run pytest tests/ -v

lint:
	uv run pyright graphs/ tests/

build:
	docker build -t canary-orchestrator .
```

- [ ] **Step 5: Create `langgraph/.env.example`**

```bash
# LangGraph server URL (used by Canary Go portal)
LANGGRAPH_URL=http://localhost:2024

# Anthropic API key for LLM nodes
ANTHROPIC_API_KEY=sk-ant-...

# Override LLM model (default: claude-sonnet-4-5)
LLM_MODEL=claude-sonnet-4-5

# Checkpoint database (blank = SQLite local; set for Postgres on GCP)
# CHECKPOINT_DB=postgresql://user:pass@host:5432/dbname

# GCP project for deploy graph
GCP_PROJECT=your-project-id
GCP_REGION=us-central1
```

- [ ] **Step 6: Create empty `__init__.py` files**

```bash
touch langgraph/graphs/__init__.py
touch langgraph/graphs/nodes/__init__.py
touch langgraph/tests/__init__.py
```

- [ ] **Step 7: Commit scaffold**

```bash
git add langgraph/
git commit -m "feat(langgraph): scaffold Python package — GRO-813"
```

---

### Task 2: State types and test fixtures

**Files:**
- Create: `langgraph/graphs/state.py`
- Create: `langgraph/tests/conftest.py`

- [ ] **Step 1: Write failing test for state shape**

Create `langgraph/tests/test_state.py`:

```python
from graphs.state import PipelineState

def test_pipeline_state_has_required_keys():
    state: PipelineState = {
        "task": "add hawk service",
        "service": "canary-gateway",
        "artifacts": {},
        "review_result": "",
        "revision_count": 0,
        "deploy_status": "",
        "error": "",
        "output_dir": "out/canary-gateway",
    }
    assert state["task"] == "add hawk service"
    assert state["revision_count"] == 0

def test_pipeline_state_artifacts_is_dict():
    state: PipelineState = {
        "task": "", "service": "", "artifacts": {"cmd/hawk/main.go": "package main"},
        "review_result": "", "revision_count": 0,
        "deploy_status": "", "error": "", "output_dir": "",
    }
    assert "cmd/hawk/main.go" in state["artifacts"]
```

- [ ] **Step 2: Run test — expect failure**

```bash
cd langgraph && uv run pytest tests/test_state.py -v
```

Expected: `ImportError: cannot import name 'PipelineState'`

- [ ] **Step 3: Create `langgraph/graphs/state.py`**

```python
from typing import TypedDict


class PipelineState(TypedDict):
    task: str              # human-provided task description
    service: str           # Cloud Run service name / output subdirectory
    artifacts: dict[str, str]   # relative-path → file content
    review_result: str     # "approved" | "needs_revision" | ""
    revision_count: int    # guard: abort after 3 revisions
    deploy_status: str     # "ok" | "failed" | ""
    error: str             # last error message, empty if none
    output_dir: str        # emit destination, default: out/<service>
```

- [ ] **Step 4: Run test — expect pass**

```bash
cd langgraph && uv run pytest tests/test_state.py -v
```

Expected: 2 passed.

- [ ] **Step 5: Create `langgraph/tests/conftest.py` with MockLLM**

```python
import pytest
from langchain_core.language_models.fake import FakeListChatModel
from langchain_core.messages import AIMessage


def make_mock_llm(responses: list[str]) -> FakeListChatModel:
    """Returns a FakeListChatModel that cycles through the given string responses."""
    return FakeListChatModel(responses=responses)


@pytest.fixture
def llm_approved():
    """LLM that always returns an approved review."""
    return make_mock_llm(["APPROVED"])


@pytest.fixture
def llm_needs_revision():
    """LLM that returns needs-revision once, then approves."""
    return make_mock_llm(["NEEDS_REVISION: missing error handling", "APPROVED"])


@pytest.fixture
def base_state() -> dict:
    return {
        "task": "add a health check endpoint to the hawk service",
        "service": "canary-hawk",
        "artifacts": {},
        "review_result": "",
        "revision_count": 0,
        "deploy_status": "",
        "error": "",
        "output_dir": "out/canary-hawk",
    }
```

- [ ] **Step 6: Commit state + fixtures**

```bash
git add langgraph/graphs/state.py langgraph/tests/conftest.py langgraph/tests/test_state.py
git commit -m "feat(langgraph): PipelineState TypedDict + test fixtures — GRO-813"
```

---

### Task 3: codegen graph nodes

**Files:**
- Create: `langgraph/graphs/nodes/generate.py`
- Create: `langgraph/graphs/nodes/review.py`
- Create: `langgraph/graphs/nodes/emit.py`

- [ ] **Step 1: Write failing tests for node signatures**

Create `langgraph/tests/test_codegen.py`:

```python
import pytest
from graphs.state import PipelineState
from graphs.nodes.generate import generate_node
from graphs.nodes.review import review_node, route_after_review
from graphs.nodes.emit import emit_node
from pathlib import Path
import tempfile


def test_generate_node_populates_artifacts(llm_approved, base_state):
    result = generate_node(base_state, llm=llm_approved)
    assert isinstance(result["artifacts"], dict)
    assert len(result["artifacts"]) > 0


def test_review_node_approved(llm_approved, base_state):
    base_state["artifacts"] = {"cmd/hawk/main.go": "package main\n"}
    result = review_node(base_state, llm=llm_approved)
    assert result["review_result"] == "approved"


def test_review_node_needs_revision(llm_needs_revision, base_state):
    base_state["artifacts"] = {"cmd/hawk/main.go": "package main\n"}
    result = review_node(base_state, llm=llm_needs_revision)
    assert result["review_result"] == "needs_revision"


def test_route_after_review_approved(base_state):
    base_state["review_result"] = "approved"
    assert route_after_review(base_state) == "emit"


def test_route_after_review_needs_revision_under_limit(base_state):
    base_state["review_result"] = "needs_revision"
    base_state["revision_count"] = 1
    assert route_after_review(base_state) == "generate"


def test_route_after_review_needs_revision_over_limit(base_state):
    base_state["review_result"] = "needs_revision"
    base_state["revision_count"] = 3
    assert route_after_review(base_state) == "emit"  # force emit after max revisions


def test_emit_node_writes_files(base_state):
    base_state["artifacts"] = {
        "cmd/hawk/main.go": "package main\nfunc main() {}",
        "internal/hawk/handler.go": "package hawk\n",
    }
    with tempfile.TemporaryDirectory() as tmpdir:
        base_state["output_dir"] = tmpdir
        result = emit_node(base_state)
        assert (Path(tmpdir) / "cmd/hawk/main.go").exists()
        assert (Path(tmpdir) / "internal/hawk/handler.go").exists()
        assert (Path(tmpdir) / "apply.sh").exists()
```

- [ ] **Step 2: Run — expect ImportError**

```bash
cd langgraph && uv run pytest tests/test_codegen.py -v 2>&1 | head -20
```

Expected: `ModuleNotFoundError: No module named 'graphs.nodes.generate'`

- [ ] **Step 3: Create `langgraph/graphs/nodes/generate.py`**

```python
import os
from langchain_core.language_models import BaseChatModel
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from graphs.state import PipelineState

SYSTEM_PROMPT = """You are an expert Go engineer working on the Canary Go platform.
Module: github.com/growdirect-llc/rapidpos
Stack: Go 1.22+, Chi v5, pgx/v5, PostgreSQL 17, Valkey 8
Conventions: UUID PKs, created_at/updated_at on all tables, Chi handlers, pgx direct for simple queries.

When given a task, produce Go source files needed to implement it.
Format your response as a sequence of files, each preceded by a line:
FILE: <relative/path/from/repo/root.go>
followed by the complete file content, then END_FILE.
Produce only files that need to change. Be complete — no placeholders."""

def _default_llm() -> BaseChatModel:
    return ChatAnthropic(
        model=os.getenv("LLM_MODEL", "claude-sonnet-4-5"),
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    )

def _parse_artifacts(text: str) -> dict[str, str]:
    artifacts: dict[str, str] = {}
    parts = text.split("FILE: ")
    for part in parts[1:]:
        lines = part.split("\n", 1)
        if len(lines) < 2:
            continue
        path = lines[0].strip()
        content = lines[1].split("END_FILE")[0].strip()
        artifacts[path] = content
    return artifacts

def generate_node(state: PipelineState, llm: BaseChatModel | None = None) -> dict:
    if llm is None:
        llm = _default_llm()
    
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Task: {state['task']}\n\nService: {state['service']}"),
    ]
    response = llm.invoke(messages)
    artifacts = _parse_artifacts(response.content)
    
    # Fallback: if LLM didn't use FILE: format, store raw as a note
    if not artifacts:
        artifacts["_llm_output.txt"] = response.content

    return {
        "artifacts": artifacts,
        "revision_count": state.get("revision_count", 0),
    }
```

- [ ] **Step 4: Create `langgraph/graphs/nodes/review.py`**

```python
import os
from typing import Literal
from langchain_core.language_models import BaseChatModel
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from graphs.state import PipelineState

REVIEW_PROMPT = """You are reviewing Go code for the Canary Go platform.
Check for: correct package declarations, missing error handling, missing defer rows.Close(),
missing context propagation, hardcoded credentials, or obvious logic errors.

Respond with exactly one of:
- APPROVED  (if the code is acceptable)
- NEEDS_REVISION: <one-line reason>  (if there are issues)

Do not include any other text."""

MAX_REVISIONS = 3

def _default_llm() -> BaseChatModel:
    return ChatAnthropic(
        model=os.getenv("LLM_MODEL", "claude-sonnet-4-5"),
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    )

def review_node(state: PipelineState, llm: BaseChatModel | None = None) -> dict:
    if llm is None:
        llm = _default_llm()

    artifacts_text = "\n\n".join(
        f"// FILE: {path}\n{content}"
        for path, content in state["artifacts"].items()
    )
    messages = [
        SystemMessage(content=REVIEW_PROMPT),
        HumanMessage(content=f"Task: {state['task']}\n\nCode:\n{artifacts_text}"),
    ]
    response = llm.invoke(messages)
    text = response.content.strip()

    if text.startswith("APPROVED"):
        return {"review_result": "approved"}
    return {"review_result": "needs_revision"}

def route_after_review(state: PipelineState) -> Literal["emit", "generate"]:
    if state["review_result"] == "approved":
        return "emit"
    if state.get("revision_count", 0) >= MAX_REVISIONS:
        return "emit"  # force emit with what we have; human reviews in portal
    return "generate"
```

- [ ] **Step 5: Create `langgraph/graphs/nodes/emit.py`**

```python
from pathlib import Path
from graphs.state import PipelineState

APPLY_SCRIPT_HEADER = """#!/bin/bash
# Generated by Canary orchestrator — review before running
set -euo pipefail
REPO_ROOT="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
"""

def emit_node(state: PipelineState) -> dict:
    output_dir = Path(state.get("output_dir") or f"out/{state['service']}")
    output_dir.mkdir(parents=True, exist_ok=True)

    for rel_path, content in state["artifacts"].items():
        target = output_dir / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)

    # Write apply.sh that copies files from output_dir to repo
    apply_lines = [APPLY_SCRIPT_HEADER]
    for rel_path in state["artifacts"]:
        apply_lines.append(
            f'cp -v "$(dirname "$0")/{rel_path}" "$REPO_ROOT/{rel_path}"'
        )
    apply_script = output_dir / "apply.sh"
    apply_script.write_text("\n".join(apply_lines) + "\n")
    apply_script.chmod(0o755)

    return {"deploy_status": "emitted"}
```

- [ ] **Step 6: Run codegen tests — expect pass**

```bash
cd langgraph && uv run pytest tests/test_codegen.py -v
```

Expected: all 7 tests pass.

- [ ] **Step 7: Commit nodes**

```bash
git add langgraph/graphs/nodes/ langgraph/tests/test_codegen.py
git commit -m "feat(langgraph): codegen nodes (generate, review, emit) — GRO-813"
```

---

### Task 4: Assemble codegen graph + deploy graph

**Files:**
- Create: `langgraph/graphs/codegen.py`
- Create: `langgraph/graphs/nodes/deploy_run.py`
- Create: `langgraph/graphs/deploy.py`
- Create: `langgraph/tests/test_deploy.py`

- [ ] **Step 1: Write failing test for graph assembly**

Add to `langgraph/tests/test_codegen.py`:

```python
from graphs.codegen import graph as codegen_graph

def test_codegen_graph_compiles():
    # Just verify the graph compiles without errors
    assert codegen_graph is not None

def test_codegen_graph_has_expected_nodes():
    node_names = list(codegen_graph.nodes.keys())
    assert "generate" in node_names
    assert "review" in node_names
    assert "emit" in node_names
```

- [ ] **Step 2: Run — expect ImportError**

```bash
cd langgraph && uv run pytest tests/test_codegen.py::test_codegen_graph_compiles -v
```

Expected: `ModuleNotFoundError: No module named 'graphs.codegen'`

- [ ] **Step 3: Create `langgraph/graphs/codegen.py`**

```python
import os
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.postgres import PostgresSaver
from graphs.state import PipelineState
from graphs.nodes.generate import generate_node
from graphs.nodes.review import review_node, route_after_review
from graphs.nodes.emit import emit_node

def _get_checkpointer():
    db_url = os.getenv("CHECKPOINT_DB")
    if db_url:
        return PostgresSaver.from_conn_string(db_url)
    return SqliteSaver.from_conn_string(".checkpoints.db")

def build_graph(checkpointer=None):
    builder = StateGraph(PipelineState)

    builder.add_node("generate", generate_node)
    builder.add_node("review", review_node)
    builder.add_node("emit", emit_node)

    builder.set_entry_point("generate")
    builder.add_edge("generate", "review")
    builder.add_conditional_edges("review", route_after_review, {
        "emit": "emit",
        "generate": "generate",
    })
    builder.add_edge("emit", END)

    cp = checkpointer if checkpointer is not None else _get_checkpointer()
    return builder.compile(checkpointer=cp, interrupt_after=["emit"])

# Module-level graph instance for langgraph.json
graph = build_graph()
```

- [ ] **Step 4: Create `langgraph/graphs/nodes/deploy_run.py`**

```python
import os
import subprocess
from graphs.state import PipelineState

def deploy_run_node(state: PipelineState) -> dict:
    project = os.getenv("GCP_PROJECT", "")
    region  = os.getenv("GCP_REGION", "us-central1")
    service = state["service"]

    if not project:
        return {"deploy_status": "failed", "error": "GCP_PROJECT not set"}

    cmd = [
        "gcloud", "run", "deploy", service,
        "--source", f"out/{service}",
        "--region", region,
        "--project", project,
        "--quiet",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            return {"deploy_status": "failed", "error": result.stderr[:500]}
        return {"deploy_status": "ok", "error": ""}
    except subprocess.TimeoutExpired:
        return {"deploy_status": "failed", "error": "gcloud deploy timed out after 5 minutes"}
    except FileNotFoundError:
        return {"deploy_status": "failed", "error": "gcloud not found in PATH"}
```

- [ ] **Step 5: Create `langgraph/tests/test_deploy.py`**

```python
import pytest
from unittest.mock import patch, MagicMock
from graphs.nodes.deploy_run import deploy_run_node


def test_deploy_node_fails_without_gcp_project(base_state):
    with patch.dict("os.environ", {}, clear=False):
        # Ensure GCP_PROJECT is not set
        import os
        os.environ.pop("GCP_PROJECT", None)
        result = deploy_run_node(base_state)
    assert result["deploy_status"] == "failed"
    assert "GCP_PROJECT" in result["error"]


def test_deploy_node_handles_gcloud_not_found(base_state):
    with patch.dict("os.environ", {"GCP_PROJECT": "test-project"}):
        with patch("subprocess.run", side_effect=FileNotFoundError):
            result = deploy_run_node(base_state)
    assert result["deploy_status"] == "failed"
    assert "gcloud not found" in result["error"]


def test_deploy_node_success(base_state):
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stderr = ""
    with patch.dict("os.environ", {"GCP_PROJECT": "test-project"}):
        with patch("subprocess.run", return_value=mock_result):
            result = deploy_run_node(base_state)
    assert result["deploy_status"] == "ok"
```

- [ ] **Step 6: Create `langgraph/graphs/deploy.py`**

```python
import os
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.postgres import PostgresSaver
from graphs.state import PipelineState
from graphs.nodes.deploy_run import deploy_run_node

def route_after_deploy(state: PipelineState):
    if state.get("deploy_status") == "ok":
        return END
    return "interrupt_on_failure"

def build_graph(checkpointer=None):
    builder = StateGraph(PipelineState)
    builder.add_node("deploy_run", deploy_run_node)
    builder.set_entry_point("deploy_run")
    builder.add_conditional_edges("deploy_run", route_after_deploy, {
        END: END,
        "interrupt_on_failure": END,  # interrupt_after handles the pause
    })

    cp = checkpointer if checkpointer is not None else _get_checkpointer()
    return builder.compile(checkpointer=cp, interrupt_after=["deploy_run"])

def _get_checkpointer():
    db_url = os.getenv("CHECKPOINT_DB")
    if db_url:
        return PostgresSaver.from_conn_string(db_url)
    return SqliteSaver.from_conn_string(".checkpoints.db")

graph = build_graph()
```

- [ ] **Step 7: Run all Python tests**

```bash
cd langgraph && uv run pytest tests/ -v
```

Expected: all tests pass.

- [ ] **Step 8: Verify `langgraph dev` starts**

```bash
cd langgraph && cp .env.example .env  # fill in ANTHROPIC_API_KEY
uv run langgraph dev &
sleep 3 && curl -s http://localhost:2024/threads | head -c 100
```

Expected: JSON response (empty array or `{"threads":[]}`).

- [ ] **Step 9: Stop server and commit**

```bash
kill %1 2>/dev/null; true
git add langgraph/graphs/ langgraph/tests/test_deploy.py
git commit -m "feat(langgraph): codegen + deploy graphs assembled — GRO-813"
```

---

## Chunk 2: Go portal integration

### Task 5: LangGraph Go client

**Files:**
- Create: `CanaryGo/internal/devops/langgraph.go`
- Create: `CanaryGo/internal/devops/langgraph_test.go`

- [ ] **Step 1: Write failing tests**

Create `CanaryGo/internal/devops/langgraph_test.go`:

```go
package devops

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

func TestLangGraphClient_PendingReleases(t *testing.T) {
	threads := []Thread{
		{
			ID:        "thread-abc",
			Status:    "interrupted",
			Values:    map[string]any{"task": "add hawk handler", "service": "canary-hawk"},
			CreatedAt: time.Now(),
			UpdatedAt: time.Now(),
		},
	}
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/threads" || r.URL.Query().Get("status") != "interrupted" {
			http.Error(w, "unexpected path", http.StatusNotFound)
			return
		}
		w.Header().Set("Content-Type", "application/json")
		_ = json.NewEncoder(w).Encode(threads)
	}))
	defer srv.Close()

	client := NewLangGraphClient(srv.URL)
	got, err := client.PendingReleases(context.Background())
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if len(got) != 1 {
		t.Fatalf("expected 1 thread, got %d", len(got))
	}
	if got[0].ID != "thread-abc" {
		t.Errorf("expected thread-abc, got %s", got[0].ID)
	}
}

func TestLangGraphClient_PendingReleases_ServerOffline(t *testing.T) {
	client := NewLangGraphClient("http://localhost:19999") // nothing listening
	got, err := client.PendingReleases(context.Background())
	if err == nil {
		t.Fatal("expected error for offline server")
	}
	if got != nil {
		t.Errorf("expected nil slice on error, got %v", got)
	}
}

func TestLangGraphClient_Resume(t *testing.T) {
	called := false
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost || r.URL.Path != "/threads/thread-xyz/runs" {
			http.Error(w, "unexpected", http.StatusNotFound)
			return
		}
		called = true
		var body map[string]any
		_ = json.NewDecoder(r.Body).Decode(&body)
		cmd, _ := body["command"].(map[string]any)
		if cmd["resume"] != "approved" {
			http.Error(w, "wrong resume value", http.StatusBadRequest)
			return
		}
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte(`{"run_id":"run-1"}`))
	}))
	defer srv.Close()

	client := NewLangGraphClient(srv.URL)
	err := client.Resume(context.Background(), "thread-xyz", "codegen", "approved")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if !called {
		t.Error("handler was not called")
	}
}

func TestLangGraphClient_GetThread(t *testing.T) {
	thread := Thread{
		ID:     "thread-abc",
		Status: "interrupted",
		Values: map[string]any{"task": "add hawk"},
	}
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/threads/thread-abc" {
			http.Error(w, "not found", http.StatusNotFound)
			return
		}
		_ = json.NewEncoder(w).Encode(thread)
	}))
	defer srv.Close()

	client := NewLangGraphClient(srv.URL)
	got, err := client.GetThread(context.Background(), "thread-abc")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if got.Status != "interrupted" {
		t.Errorf("expected interrupted, got %s", got.Status)
	}
}
```

- [ ] **Step 2: Run — expect compile failure**

```bash
cd CanaryGo && go test ./internal/devops/... 2>&1 | head -20
```

Expected: `undefined: NewLangGraphClient`

- [ ] **Step 3: Create `CanaryGo/internal/devops/langgraph.go`**

```go
// Package devops — LangGraph API client.
//
// Talks to a running LangGraph server (local langgraph dev or Cloud Run).
// The server URL is read from LANGGRAPH_URL env var at Handler construction
// time; the client itself is stateless.
package devops

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"time"
)

// Thread is a LangGraph thread (one graph execution with checkpoint history).
type Thread struct {
	ID        string         `json:"thread_id"`
	Status    string         `json:"status"`    // "interrupted" | "idle" | "busy" | "error"
	Values    map[string]any `json:"values"`    // PipelineState fields
	CreatedAt time.Time      `json:"created_at"`
	UpdatedAt time.Time      `json:"updated_at"`
}

// LangGraphClient is a thin HTTP client for the LangGraph server REST API.
type LangGraphClient struct {
	baseURL string
	http    *http.Client
}

// NewLangGraphClient creates a client targeting baseURL (e.g. "http://localhost:2024").
func NewLangGraphClient(baseURL string) *LangGraphClient {
	return &LangGraphClient{
		baseURL: baseURL,
		http:    &http.Client{Timeout: 8 * time.Second},
	}
}

// PendingReleases returns threads with status=interrupted (awaiting human approval).
func (c *LangGraphClient) PendingReleases(ctx context.Context) ([]Thread, error) {
	req, err := http.NewRequestWithContext(ctx, http.MethodGet,
		c.baseURL+"/threads?status=interrupted", nil)
	if err != nil {
		return nil, err
	}
	resp, err := c.http.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	if resp.StatusCode >= 400 {
		return nil, fmt.Errorf("langgraph: GET /threads status %d", resp.StatusCode)
	}
	var threads []Thread
	if err := json.NewDecoder(resp.Body).Decode(&threads); err != nil {
		return nil, fmt.Errorf("langgraph: decode threads: %w", err)
	}
	return threads, nil
}

// GetThread returns the full state of a single thread.
func (c *LangGraphClient) GetThread(ctx context.Context, id string) (*Thread, error) {
	req, err := http.NewRequestWithContext(ctx, http.MethodGet,
		c.baseURL+"/threads/"+id, nil)
	if err != nil {
		return nil, err
	}
	resp, err := c.http.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	if resp.StatusCode == http.StatusNotFound {
		return nil, fmt.Errorf("langgraph: thread %s not found", id)
	}
	if resp.StatusCode >= 400 {
		return nil, fmt.Errorf("langgraph: GET /threads/%s status %d", id, resp.StatusCode)
	}
	var t Thread
	if err := json.NewDecoder(resp.Body).Decode(&t); err != nil {
		return nil, fmt.Errorf("langgraph: decode thread: %w", err)
	}
	return &t, nil
}

// Resume sends a command to an interrupted thread, resuming graph execution.
// decision is passed as command.resume — conventionally "approved" or "rejected".
func (c *LangGraphClient) Resume(ctx context.Context, threadID, assistantID, decision string) error {
	body, err := json.Marshal(map[string]any{
		"assistant_id": assistantID,
		"command":      map[string]any{"resume": decision},
	})
	if err != nil {
		return err
	}
	req, err := http.NewRequestWithContext(ctx, http.MethodPost,
		c.baseURL+"/threads/"+threadID+"/runs",
		bytes.NewReader(body))
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", "application/json")
	resp, err := c.http.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	if resp.StatusCode >= 400 {
		return fmt.Errorf("langgraph: resume thread %s status %d", threadID, resp.StatusCode)
	}
	return nil
}
```

- [ ] **Step 4: Run tests — expect pass**

```bash
cd CanaryGo && go test ./internal/devops/... -run TestLangGraphClient -v
```

Expected: 4 tests pass.

- [ ] **Step 5: Commit**

```bash
git add CanaryGo/internal/devops/langgraph.go CanaryGo/internal/devops/langgraph_test.go
git commit -m "feat(devops): LangGraph Go client with httptest coverage — GRO-813"
```

---

### Task 6: Wire client into Handler + add routes

**Files:**
- Modify: `CanaryGo/internal/devops/handler.go`
- Modify: `CanaryGo/internal/devops/templates/base.html`
- Create: `CanaryGo/.env.example`

- [ ] **Step 1: Add `lgClient` to Handler and new routes**

In `handler.go`, add `lgClient *LangGraphClient` to the `Handler` struct (after `squareSvc`):

```go
type Handler struct {
	pool      *pgxpool.Pool
	rdb       *redis.Client
	logger    *zap.Logger
	tmpl      *template.Template
	squareSvc *squareauth.Service
	lgClient  *LangGraphClient  // nil = LangGraph server offline/disabled
}
```

Update `New()` — add `lgClient` construction after `squareSvc` param:

```go
func New(pool *pgxpool.Pool, rdb *redis.Client, logger *zap.Logger, squareSvc *squareauth.Service) *Handler {
	// ... existing code ...
	lgURL := os.Getenv("LANGGRAPH_URL")
	if lgURL == "" {
		lgURL = "http://localhost:2024"
	}
	return &Handler{
		pool:      pool,
		rdb:       rdb,
		logger:    logger,
		tmpl:      tmpl,
		squareSvc: squareSvc,
		lgClient:  NewLangGraphClient(lgURL),
	}
}
```

Add to `Mount()` inside the `/devops` route group:

```go
r.Get("/releases",                h.releasesPage)
r.Get("/releases/state",          h.releasesState)
r.Post("/releases/{id}/approve",  h.approveRelease)
r.Post("/releases/{id}/reject",   h.rejectRelease)
```

Add template parse for `"templates/releases.html"` in `New()`.

Add handler methods:

```go
func (h *Handler) releasesPage(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	w.Header().Set("Cache-Control", "no-store")
	if err := h.tmpl.ExecuteTemplate(w, "base.html", map[string]any{
		"Page": "releases",
	}); err != nil {
		h.logger.Error("releases template", zap.Error(err))
	}
}

type releasesStateResp struct {
	Pending []Thread `json:"pending"`
	Server  string   `json:"server"`
	Online  bool     `json:"online"`
}

func (h *Handler) releasesState(w http.ResponseWriter, r *http.Request) {
	ctx, cancel := context.WithTimeout(r.Context(), 5*time.Second)
	defer cancel()

	resp := releasesStateResp{
		Server:  h.lgClient.baseURL,
		Pending: []Thread{},
		Online:  false,
	}
	threads, err := h.lgClient.PendingReleases(ctx)
	if err != nil {
		h.logger.Debug("langgraph offline", zap.Error(err))
	} else {
		resp.Online = true
		resp.Pending = threads
	}

	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Cache-Control", "no-store")
	_ = json.NewEncoder(w).Encode(resp)
}

func (h *Handler) approveRelease(w http.ResponseWriter, r *http.Request) {
	h.resumeRelease(w, r, "approved")
}

func (h *Handler) rejectRelease(w http.ResponseWriter, r *http.Request) {
	h.resumeRelease(w, r, "rejected")
}

func (h *Handler) resumeRelease(w http.ResponseWriter, r *http.Request, decision string) {
	threadID := chi.URLParam(r, "id")
	if err := r.ParseForm(); err != nil {
		http.Error(w, `{"error":"bad request"}`, http.StatusBadRequest)
		return
	}
	assistantID := r.FormValue("assistant_id")
	if assistantID == "" {
		assistantID = "codegen"
	}

	ctx, cancel := context.WithTimeout(r.Context(), 10*time.Second)
	defer cancel()

	if err := h.lgClient.Resume(ctx, threadID, assistantID, decision); err != nil {
		h.logger.Error("langgraph resume", zap.Error(err))
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusBadGateway)
		_ = json.NewEncoder(w).Encode(map[string]any{"ok": false, "error": err.Error()})
		return
	}
	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(map[string]any{"ok": true, "decision": decision})
}
```

- [ ] **Step 2: Add Releases nav item to `base.html`**

After the Square nav item:
```html
<a href="/devops/releases" class="sidebar-item{{if eq .Page "releases"}} active{{end}}">
  <span>🚀</span> Releases
</a>
```

- [ ] **Step 3: Create `CanaryGo/.env.example`**

```bash
# LangGraph server (local dev: langgraph dev; GCP: Cloud Run URL)
LANGGRAPH_URL=http://localhost:2024

# Square OAuth
SQUARE_APPLICATION_ID=
SQUARE_APPLICATION_SECRET=
SQUARE_REDIRECT_URI=http://localhost:8080/auth/square/callback

# Database
DATABASE_URL=postgres://growdirect:growdirect_dev@localhost:5432/canary_gcp?sslmode=disable

# Valkey
VALKEY_URL=redis://:valkey_dev@localhost:6379/2

# Dev console (set any non-empty value to enable /devops)
DEV_CONSOLE=1

# Secrets backend: pgx (dev) | sm (GCP Secret Manager)
SECRET_BACKEND=pgx
```

- [ ] **Step 4: Verify build**

```bash
cd CanaryGo && go build ./... 2>&1
```

Expected: no output (clean build).

- [ ] **Step 5: Run full test suite**

```bash
cd CanaryGo && go test ./internal/devops/... -v
```

Expected: all tests pass including new LangGraph client tests.

- [ ] **Step 6: Commit**

```bash
git add CanaryGo/internal/devops/handler.go \
        CanaryGo/internal/devops/templates/base.html \
        CanaryGo/.env.example
git commit -m "feat(devops): wire LangGraph client into Handler + releases routes — GRO-813"
```

---

### Task 7: Releases HTML template

**Files:**
- Create: `CanaryGo/internal/devops/templates/releases.html`

- [ ] **Step 1: Create the template**

```html
{{template "base.html" .}}

{{define "title"}}Releases — Canary Devops{{end}}

{{define "content"}}
<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:4px;">
  <h1 class="page-title">Releases</h1>
  <div class="refresh-indicator" id="refresh-indicator">
    <div class="refresh-spinner" id="refresh-spinner"></div>
    <span id="refresh-ts">—</span>
  </div>
</div>
<p class="page-subtitle">
  LangGraph pending approvals · <span id="server-url" class="ts"></span>
  <span id="server-badge" class="badge" style="margin-left:6px;"></span>
</p>

<div class="ops-grid-4" style="grid-template-columns:repeat(2,1fr);margin-bottom:16px;">
  <div class="stat-tile">
    <div class="stat-value" id="stat-pending">—</div>
    <div class="stat-label">Pending Approval</div>
  </div>
  <div class="stat-tile">
    <div class="stat-value" id="stat-server">—</div>
    <div class="stat-label">Server Status</div>
  </div>
</div>

<div class="ops-card">
  <div class="ops-section-title">Pending Releases</div>
  <div id="releases-wrap">
    <div class="empty-state">Loading…</div>
  </div>
</div>
{{end}}

{{define "scripts"}}
<script>
const fmtTime = ts => {
  if (!ts) return '—';
  const d = new Date(ts);
  return d.toLocaleString([], {month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit'});
};

function artifactsHtml(values) {
  const artifacts = values?.artifacts || {};
  const keys = Object.keys(artifacts);
  if (!keys.length) return '<span class="ts">no artifacts yet</span>';
  return keys.map(k =>
    `<div class="artifact-file">
      <div class="artifact-path">${k}</div>
      <pre class="artifact-content">${escHtml(artifacts[k] || '').slice(0, 800)}${artifacts[k]?.length > 800 ? '\n… (truncated)' : ''}</pre>
    </div>`
  ).join('');
}

function escHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function renderReleases(threads) {
  const wrap = document.getElementById('releases-wrap');
  if (!threads || threads.length === 0) {
    wrap.innerHTML = '<div class="empty-state">No pending releases. Run a codegen graph to generate one.</div>';
    return;
  }
  wrap.innerHTML = threads.map(t => `
    <div class="release-card" id="card-${t.thread_id}">
      <div class="release-header">
        <div>
          <span class="hash">${t.thread_id}</span>
          <span class="badge badge-amber" style="margin-left:8px">awaiting approval</span>
        </div>
        <span class="ts">${fmtTime(t.updated_at)}</span>
      </div>
      <div class="release-task">
        <span class="ts">Task:</span> ${escHtml(t.values?.task || '—')}
        &nbsp;·&nbsp;
        <span class="ts">Service:</span> ${escHtml(t.values?.service || '—')}
      </div>
      <div class="release-artifacts">${artifactsHtml(t.values)}</div>
      <div class="release-actions">
        <button class="approve-btn" onclick="decide('${t.thread_id}', '${t.values?.assistant_id || 'codegen'}', 'approved', this)">
          ✓ Approve
        </button>
        <button class="reject-btn" onclick="decide('${t.thread_id}', '${t.values?.assistant_id || 'codegen'}', 'rejected', this)">
          ✗ Reject
        </button>
        <span class="decision-result" id="decision-${t.thread_id}"></span>
      </div>
    </div>
  `).join('');
}

async function decide(threadID, assistantID, decision, btn) {
  const resultEl = document.getElementById('decision-' + threadID);
  btn.disabled = true;
  resultEl.textContent = '…';
  try {
    const resp = await fetch(`/devops/releases/${threadID}/${decision === 'approved' ? 'approve' : 'reject'}`, {
      method: 'POST',
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: 'assistant_id=' + encodeURIComponent(assistantID),
    });
    const d = await resp.json();
    if (d.ok) {
      resultEl.textContent = decision === 'approved' ? '✓ approved — graph resuming' : '✗ rejected';
      resultEl.style.color = decision === 'approved' ? 'var(--green)' : 'var(--red)';
      document.getElementById('card-' + threadID).style.opacity = '0.5';
    } else {
      resultEl.textContent = '✗ ' + (d.error || 'failed');
      resultEl.style.color = 'var(--red)';
      btn.disabled = false;
    }
  } catch(e) {
    resultEl.textContent = '✗ ' + e.message;
    resultEl.style.color = 'var(--red)';
    btn.disabled = false;
  }
}

async function refresh() {
  const spinner = document.getElementById('refresh-spinner');
  const tsEl    = document.getElementById('refresh-ts');
  spinner.style.display = 'block';
  try {
    const resp = await fetch('/devops/releases/state');
    if (!resp.ok) throw new Error('HTTP ' + resp.status);
    const d = await resp.json();

    document.getElementById('server-url').textContent = d.server || '';
    const badge = document.getElementById('server-badge');
    if (d.online) {
      badge.textContent = 'online';
      badge.className = 'badge badge-green';
    } else {
      badge.textContent = 'offline';
      badge.className = 'badge badge-red';
    }

    const pending = (d.pending || []).length;
    const pendEl = document.getElementById('stat-pending');
    pendEl.textContent = pending;
    pendEl.className = 'stat-value ' + (pending > 0 ? 'amber' : 'green');

    const srvEl = document.getElementById('stat-server');
    srvEl.textContent = d.online ? 'online' : 'offline';
    srvEl.className = 'stat-value ' + (d.online ? 'green' : 'red');

    renderReleases(d.pending);
    tsEl.textContent = 'updated ' + new Date().toLocaleTimeString();
  } catch(e) {
    tsEl.textContent = 'error: ' + e.message;
  } finally {
    spinner.style.display = 'none';
  }
}

refresh();
setInterval(refresh, 15000);
</script>

<style>
.release-card {
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 16px;
  margin-bottom: 12px;
  background: var(--surface-2);
}
.release-card:last-child { margin-bottom: 0; }
.release-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.release-task { font-size: 13px; margin-bottom: 12px; }
.release-artifacts { margin-bottom: 12px; }
.artifact-file { margin-bottom: 8px; }
.artifact-path {
  font-family: var(--mono);
  font-size: 11px;
  color: var(--text-secondary);
  margin-bottom: 4px;
}
.artifact-content {
  background: var(--surface-3);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 8px 12px;
  font-family: var(--mono);
  font-size: 11px;
  line-height: 1.5;
  overflow-x: auto;
  max-height: 200px;
  overflow-y: auto;
  white-space: pre;
}
.release-actions { display: flex; align-items: center; gap: 8px; }
.approve-btn {
  background: rgba(52,211,153,0.15);
  border: 1px solid rgba(52,211,153,0.3);
  color: #34d399;
  padding: 4px 14px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  font-family: inherit;
  font-weight: 600;
}
.approve-btn:hover { background: rgba(52,211,153,0.25); }
.approve-btn:disabled { opacity: 0.5; cursor: default; }
.reject-btn {
  background: rgba(248,113,113,0.1);
  border: 1px solid rgba(248,113,113,0.3);
  color: #f87171;
  padding: 4px 14px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  font-family: inherit;
}
.reject-btn:hover { background: rgba(248,113,113,0.2); }
.reject-btn:disabled { opacity: 0.5; cursor: default; }
.decision-result { font-size: 12px; }
.badge-amber { background: rgba(251,191,36,0.15); color: #fbbf24; }
</style>
{{end}}
```

- [ ] **Step 2: Verify build**

```bash
cd CanaryGo && go build ./... 2>&1
```

Expected: clean.

- [ ] **Step 3: Run full test suite**

```bash
cd CanaryGo && go test ./... -count=1 2>&1 | tail -10
```

Expected: all pass.

- [ ] **Step 4: Commit**

```bash
git add CanaryGo/internal/devops/templates/releases.html
git commit -m "feat(devops): releases approval UI template — GRO-813"
```

---

### Task 8: Final integration check + GRO-813 close

**Files:**
- No new files — verification only

- [ ] **Step 1: Run all Go tests**

```bash
cd CanaryGo && go test ./... -count=1 -v 2>&1 | grep -E "PASS|FAIL|ok"
```

Expected: all `ok` lines, no `FAIL`.

- [ ] **Step 2: Run all Python tests**

```bash
cd /Users/gclyle/GrowDirect/langgraph && uv run pytest tests/ -v 2>&1 | tail -15
```

Expected: all passed.

- [ ] **Step 3: Verify `go build ./...` clean**

```bash
cd CanaryGo && go build ./... 2>&1
```

Expected: no output.

- [ ] **Step 4: Smoke-test `langgraph dev` starts**

```bash
cd /Users/gclyle/GrowDirect/langgraph
uv run langgraph dev &
sleep 4 && curl -sf http://localhost:2024/ok && echo " server healthy"
kill %1 2>/dev/null; true
```

Expected: `server healthy` or a 200 response.

- [ ] **Step 5: Final commit and close GRO-813**

```bash
git add -A
git status  # confirm only expected files
git commit -m "demo(langgraph): GRO-813 complete — local workflow + portal releases panel"
```

Update GRO-813 status to Done in Linear with artifact paths.
