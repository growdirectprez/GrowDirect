# Spec — LangGraph Local Workflow + Portal Releases Panel

**GRO-813** · authored 2026-05-06 · status: active

---

## Governing thesis

A local LangGraph workflow generates Go code artifacts and gates deploys through the existing Canary devops portal. GCP is only touched at deploy time using idling Cloud Run + Cloud SQL. Zero new cloud infrastructure required.

---

## Subsystem 1 — LangGraph Python package (`langgraph/`)

### What it does
Two LangGraph graphs runnable locally via `langgraph dev`:

**`codegen`** — task description → Go code artifacts → human approval → emit to disk
```
[generate] → [review] → interrupt(human) → [emit] → END
                ↓ (needs_revision)
            [generate]
```

**`deploy`** — service name + image → `gcloud run deploy` → health verify → END
```
[deploy_run] → [verify] → END
                  ↓ (failed)
              interrupt(human)
```

### State contract

```python
class PipelineState(TypedDict):
    task: str                          # human-provided task description
    service: str                       # Cloud Run service name
    artifacts: dict[str, str]          # relative-path → file content
    review_result: str                 # "approved" | "needs_revision" | ""
    revision_count: int                # guard against infinite loops
    deploy_status: str                 # "ok" | "failed" | ""
    error: str                         # last error message
    output_dir: str                    # where to emit (default: out/<service>)
```

### Key decisions
- `uv` for dependency management (not pip/poetry) — lockfile reproducibility
- SQLite checkpointer locally; swap to `PostgresSaver` for Cloud Run via `CHECKPOINT_DB` env var
- `interrupt()` is the only human gate — no parallel branches, no custom reducers yet
- `emit` node writes files to `out/<service>/` + a `apply.sh` that copies files to repo locations
- LLM provider: Anthropic `claude-sonnet-4-5` via `langchain-anthropic`; override via `LLM_MODEL` env var

---

## Subsystem 2 — Portal releases panel (`/devops/releases`)

### What it does
Canary Go devops console section that talks to the LangGraph server API. Shows interrupted threads (pending approvals), renders artifact content, provides approve/reject buttons. Polls every 15s.

### API surface consumed

| LangGraph endpoint | Used for |
|---|---|
| `GET /threads?status=interrupted` | list pending releases |
| `GET /threads/{id}` | thread state + values (artifacts, task, etc.) |
| `POST /threads/{id}/runs` with `command.resume` | approve or reject |

Portal never reads from SQLite/Postgres directly. LangGraph server owns state.

### Key decisions
- `LANGGRAPH_URL` env var, default `http://localhost:2024` — same code runs locally and on Cloud Run
- Graceful offline: when LangGraph server unreachable, panel shows "server offline" badge, rest of devops console unaffected
- `lgClient` is a field on `devops.Handler` — `nil` is valid (offline mode), not a fatal error
- No new GRO audit log entries from the portal itself — the LangGraph graph already emits structured events

---

## File layout

```
GrowDirect/
  langgraph/
    pyproject.toml
    langgraph.json
    Makefile
    .env.example
    graphs/
      __init__.py
      state.py
      codegen.py
      deploy.py
      nodes/
        __init__.py
        generate.py
        review.py
        emit.py
        deploy_run.py
    tests/
      __init__.py
      conftest.py
      test_codegen.py
      test_deploy.py

CanaryGo/
  internal/devops/
    langgraph.go
    langgraph_test.go
    handler.go              (modified)
    templates/
      releases.html
      base.html             (modified)
  .env.example              (new)
```

---

## Standards checklist

- [ ] `make dev` starts `langgraph dev` — engineer is running in ≤15 min
- [ ] `make test` green with zero cloud credentials
- [ ] All Python state `TypedDict`, no `Any`
- [ ] Go client tested with `httptest.NewServer` mock
- [ ] `.env.example` documents every var
- [ ] `go build ./...` clean after all Go changes
