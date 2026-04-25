---
classification: confidential
owner: GrowDirect LLC
---

# QA Agent F2+F3 (Linear filing + Atlas inline) Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `file_linear_bug(title, description)` QA-only tool that creates real Linear issues via GraphQL, and strip YAML frontmatter from `atlas_figure` return values so the chat UI renders mermaid diagrams cleanly inline.

**Architecture:** New `canary/services/qa_agent/linear_client.py` wraps Linear's GraphQL API. New handler in `tools.py` composes title + description + auto-appended merchant footer. SYSTEM_PROMPT grows two sections: bug-filing cues, and "include atlas_figure content verbatim." `canary/services/atlas/tools.py` gains frontmatter-stripping before return.

**Tech Stack:** Python 3.12, `requests` (sync, already in deps), Linear GraphQL v1, pytest + unittest.mock.

**Spec:** [docs/superpowers/specs/2026-04-23-qa-agent-linear-filing-atlas-inline-design.md](../specs/2026-04-23-qa-agent-linear-filing-atlas-inline-design.md)

**Linear:** GRO-517 Features 2 and 3; builds on GRO-517 F1 merged at commit `e5bf95c`.

---

## File Structure

**Created:**
- `Canary/canary/services/qa_agent/linear_client.py` — minimal Linear GraphQL client
- `Canary/tests/unit/test_qa_agent_linear_client.py` — 5 unit tests
- `Canary/tests/unit/test_atlas_figure_frontmatter_strip.py` — 5 unit tests
- `Canary/tests/integration/test_qa_agent_file_linear_bug.py` — 4 integration tests

**Modified:**
- `Canary/canary/services/qa_agent/tools.py` — add `file_linear_bug` tool + handler
- `Canary/canary/services/qa_agent/agent.py` — SYSTEM_PROMPT: F2 (bug filing) + F3 (atlas inline) sections
- `Canary/canary/services/atlas/tools.py` — `_handle_atlas_figure` strips YAML frontmatter
- `Canary/devops/docker-compose.localhost.yml` — add `LINEAR_API_KEY` to qa-agent env (GUARDIAN)
- `Canary/.guardian-manifest` — SHA bump for the compose file

**Unchanged but referenced:**
- `canary/services/atlas/service.py::get_figure()` — returns `{"metadata": ..., "content": "<raw file>", ...}`; we strip frontmatter downstream in `_handle_atlas_figure` so the service layer stays a thin file-reader
- `canary/services/qa_agent/server.py` — `handle_chat` already sets the ContextVar before tool dispatch; no changes

**Requires from user (outside commit stream):**
- Add `LINEAR_API_KEY=lin_api_xxx` to `/Users/gclyle/GrowDirect/Canary/.env`. Without this, `file_linear_bug` returns an error envelope and the agent apologizes gracefully. The Feature still merges cleanly without the key — only live E2E verification needs it.

---

## Chunk 1: Linear bug filing (Feature 2)

### Task 1.1: Linear GraphQL client

**Files:**
- Create: `Canary/canary/services/qa_agent/linear_client.py`

- [ ] **Step 1: Create the module skeleton**

```python
"""Minimal Linear GraphQL client for the QA Agent's file_linear_bug tool.

Wraps Linear's v1 GraphQL API (https://api.linear.app/graphql) with just
enough to create an issue and resolve team/project/label IDs by name.
Personal API keys are passed as bare Authorization headers (NO Bearer
prefix — Linear personal keys use literal Authorization: <key>).

GRO-517 Feature 2.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional

import requests

logger = logging.getLogger(__name__)

LINEAR_API_URL = "https://api.linear.app/graphql"


@dataclass
class LinearAPIError(Exception):
    message: str
    request_id: Optional[str] = None

    def __str__(self) -> str:
        return self.message


class LinearClient:
    """One instance per request is fine; cache is per-instance only."""

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("LinearClient requires a non-empty api_key")
        self._api_key = api_key
        self._team_cache: dict[str, str] = {}  # name → id
        self._project_cache: dict[str, str] = {}  # name → id
        self._label_cache: dict[str, str] = {}  # name → id

    def _post(self, query: str, variables: dict | None = None) -> dict:
        """Execute a GraphQL request; raise LinearAPIError on failure."""
        resp = requests.post(
            LINEAR_API_URL,
            json={"query": query, "variables": variables or {}},
            headers={
                "Authorization": self._api_key,
                "Content-Type": "application/json",
            },
            timeout=10,
        )
        request_id = resp.headers.get("x-request-id")
        try:
            body = resp.json()
        except ValueError:
            raise LinearAPIError(
                message=f"Non-JSON response from Linear (status={resp.status_code})",
                request_id=request_id,
            )
        if "errors" in body and body["errors"]:
            first = body["errors"][0]
            raise LinearAPIError(
                message=first.get("message", "Unknown Linear GraphQL error"),
                request_id=first.get("extensions", {}).get("requestId", request_id),
            )
        return body.get("data", {})

    def _resolve_team_id(self, team_name: str) -> str:
        if team_name in self._team_cache:
            return self._team_cache[team_name]
        data = self._post("query { teams { nodes { id name } } }")
        for t in data.get("teams", {}).get("nodes", []):
            if t["name"] == team_name:
                self._team_cache[team_name] = t["id"]
                return t["id"]
        raise LinearAPIError(message=f"Team '{team_name}' not found in Linear workspace")

    def _resolve_project_id(self, team_id: str, project_name: str) -> Optional[str]:
        cache_key = f"{team_id}:{project_name}"
        if cache_key in self._project_cache:
            return self._project_cache[cache_key]
        data = self._post(
            "query($teamId: String!) { team(id: $teamId) { projects { nodes { id name } } } }",
            {"teamId": team_id},
        )
        for p in data.get("team", {}).get("projects", {}).get("nodes", []):
            if p["name"] == project_name:
                self._project_cache[cache_key] = p["id"]
                return p["id"]
        # Graceful: log and proceed without a project binding
        logger.warning("Linear project '%s' not found; filing without project", project_name)
        return None

    def _resolve_label_ids(self, team_id: str, label_names: tuple[str, ...]) -> list[str]:
        if not label_names:
            return []
        # Cache lookup per team
        missing = [n for n in label_names if f"{team_id}:{n}" not in self._label_cache]
        if missing:
            data = self._post(
                "query($teamId: String!) { team(id: $teamId) { labels { nodes { id name } } } }",
                {"teamId": team_id},
            )
            by_name = {lab["name"]: lab["id"] for lab in data.get("team", {}).get("labels", {}).get("nodes", [])}
            for name in label_names:
                key = f"{team_id}:{name}"
                if key in self._label_cache:
                    continue
                lid = by_name.get(name)
                if lid:
                    self._label_cache[key] = lid
                else:
                    logger.warning("Linear label '%s' not found in team; skipping", name)
        return [self._label_cache[f"{team_id}:{n}"] for n in label_names if f"{team_id}:{n}" in self._label_cache]

    def create_issue(
        self,
        title: str,
        description: str,
        team: str = "Growdirect",
        project: str = "Canary",
        labels: tuple[str, ...] = ("Canary Builder", "Bug"),
    ) -> dict:
        """Create an issue; return {id, identifier, url}.

        Raises LinearAPIError on any GraphQL error or missing response fields.
        """
        team_id = self._resolve_team_id(team)
        project_id = self._resolve_project_id(team_id, project)
        label_ids = self._resolve_label_ids(team_id, labels)

        input_vars: dict = {
            "title": title,
            "description": description,
            "teamId": team_id,
            "labelIds": label_ids,
        }
        if project_id:
            input_vars["projectId"] = project_id

        mutation = (
            "mutation($input: IssueCreateInput!) { "
            "issueCreate(input: $input) { "
            "success issue { id identifier url } } }"
        )
        data = self._post(mutation, {"input": input_vars})
        issue = (data.get("issueCreate") or {}).get("issue")
        if not issue or not issue.get("url") or not issue.get("identifier"):
            raise LinearAPIError(
                message=f"Linear response missing url/identifier: {data!r}"
            )
        return {
            "id": issue["id"],
            "identifier": issue["identifier"],
            "url": issue["url"],
        }
```

- [ ] **Step 2: Verify syntax**

```bash
cd /Users/gclyle/GrowDirect/Canary
python3 -m py_compile canary/services/qa_agent/linear_client.py
# Expected: no output
```

- [ ] **Step 3: Commit**

```bash
git add canary/services/qa_agent/linear_client.py
git commit -m "feat(qa-agent): Linear GraphQL client for bug filing [GRO-517]

Minimal LinearClient wrapping the Linear v1 GraphQL API. Resolves team,
project, and label IDs by name with per-instance caching. Graceful on
missing labels (logs + skips). Raises LinearAPIError on any failure
including missing response fields. No Bearer prefix on auth header —
Linear personal keys use bare Authorization: <key>."
```

---

### Task 1.2: `file_linear_bug` tool + SYSTEM_PROMPT F2 update

**Files:**
- Modify: `Canary/canary/services/qa_agent/tools.py`
- Modify: `Canary/canary/services/qa_agent/agent.py`

- [ ] **Step 1: Find the actual symbol names**

The QA tool metadata lives in THREE locations inside `tools.py`:

1. `_QA_HANDLERS` — module-level dict at line 203 (`fire_scenario`, `poll_scenario`, `list_scenarios`, `get_thresholds`)
2. `qa_tools` — LOCAL list variable inside `get_tool_definitions()` at line 98 (Claude API format — uses `input_schema`)
3. `_qa_tool_defs` — LOCAL list variable inside `build_canary_mcp_server()` at line 286 (SDK MCP format — uses `schema`)

All three need `file_linear_bug` added. Note the key name differs between Claude API format (`input_schema`) and SDK format (`schema`).

- [ ] **Step 2: Add module-level `LinearClient` import for clean mocking**

At the top of `tools.py` (with the other module imports, not inside a function), add:

```python
from canary.services.qa_agent.linear_client import LinearClient, LinearAPIError
```

This makes `canary.services.qa_agent.tools.LinearClient` a valid patch target for the integration tests (avoids the standard "patch-where-used" gotcha when the import is inside a function body).

- [ ] **Step 3: Add the Claude API format tool def**

In `get_tool_definitions()` at around line 98, locate the existing `qa_tools = [ ... ]` list. Append:

```python
{
    "name": "file_linear_bug",
    "description": "File a Linear bug report based on the current conversation. Use when the user says 'log this as a bug', 'file this', 'report this as a bug', or similar. Do NOT ask for confirmation; file immediately and return the URL.",
    "input_schema": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "Short, specific title for the bug (< 80 chars). Infer from the conversation."
            },
            "description": {
                "type": "string",
                "description": "Bug description. What the user expected and what they observed. Do NOT include the transcript or merchant ID — those are auto-appended."
            },
        },
        "required": ["title", "description"],
    },
},
```

- [ ] **Step 4: Add the SDK MCP format tool def**

In `build_canary_mcp_server()` at around line 286, locate the existing `_qa_tool_defs = [ ... ]` list. Append the SAME definition but with `schema` instead of `input_schema`:

```python
{
    "name": "file_linear_bug",
    "description": "File a Linear bug report based on the current conversation. Use when the user says 'log this as a bug', 'file this', 'report this as a bug', or similar. Do NOT ask for confirmation; file immediately and return the URL.",
    "schema": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "Short, specific title for the bug (< 80 chars). Infer from the conversation."
            },
            "description": {
                "type": "string",
                "description": "Bug description. What the user expected and what they observed. Do NOT include the transcript or merchant ID — those are auto-appended."
            },
        },
        "required": ["title", "description"],
    },
},
```

- [ ] **Step 5: Add the handler function**

Near `_handle_fire_scenario` et al. at module scope:

```python
def _handle_file_linear_bug(params: dict) -> dict[str, Any]:
    import os
    from canary.db.session_factory import _merchant_ctx
    # LinearClient + LinearAPIError imported at module top (see Step 2)

    title = params.get("title", "").strip()
    description = params.get("description", "").strip()
    if not title or not description:
        return {"error": "title and description are required"}

    api_key = os.getenv("LINEAR_API_KEY")
    if not api_key:
        return {"error": "LINEAR_API_KEY not configured in sidecar env"}

    # Auto-append merchant + source footer
    merchant_id = _merchant_ctx.get()
    footer_lines = ["", "---", "", "## Auto-appended context"]
    if merchant_id:
        footer_lines.append(f"- **Merchant:** `{merchant_id}`")
    footer_lines.append("- **Source:** QA Agent chat (`/ops/qa`)")
    full_description = description + "\n" + "\n".join(footer_lines)

    try:
        client = LinearClient(api_key=api_key)
        result = client.create_issue(title=title, description=full_description)
        return {
            "ok": True,
            "identifier": result["identifier"],
            "url": result["url"],
            "title": title,
        }
    except LinearAPIError as e:
        return {
            "error": f"Linear API error: {e.message}",
            "request_id": e.request_id,
        }
```

- [ ] **Step 6: Register the handler in `_QA_HANDLERS`**

At the existing `_QA_HANDLERS = { ... }` dict around line 203, add the entry:

```python
_QA_HANDLERS = {
    "fire_scenario": _handle_fire_scenario,
    "poll_scenario": _handle_poll_scenario,
    "list_scenarios": _handle_list_scenarios,
    "get_thresholds": _handle_get_thresholds,
    "file_linear_bug": _handle_file_linear_bug,  # NEW for GRO-517 F2
}
```

(Exact symbol name: `_QA_HANDLERS`, all-caps, not `_qa_tool_handlers`.)

- [ ] **Step 7: Update SYSTEM_PROMPT with F2 section**

In `canary/services/qa_agent/agent.py`, find the current `SYSTEM_PROMPT`. Near the "Response style" section (post-GRO-517 F1 update), add a new section BEFORE "Response style":

```
## Filing bugs

If the user says "log this as a bug", "file this", "report this", or similar,
call `file_linear_bug(title, description)` immediately — do not ask for
confirmation. Title is your best short description (< 80 chars). Description
is a brief observed-vs-expected summary. Don't include merchant IDs,
conversation transcripts, or timestamps — those are auto-appended.

After the tool returns, reply: "Filed [<identifier>](<url>): <title>"
```

- [ ] **Step 8: Verify syntax + imports**

```bash
cd /Users/gclyle/GrowDirect/Canary
python3 -m py_compile canary/services/qa_agent/tools.py canary/services/qa_agent/agent.py
# Expected: no output
python3 -c "
from canary.services.qa_agent.agent import SYSTEM_PROMPT
assert 'file_linear_bug' in SYSTEM_PROMPT or 'log this as a bug' in SYSTEM_PROMPT.lower()
print('prompt has F2 section')
"
```

- [ ] **Step 9: Commit**

```bash
git add canary/services/qa_agent/tools.py canary/services/qa_agent/agent.py
git commit -m "feat(qa-agent): file_linear_bug tool + SYSTEM_PROMPT F2 [GRO-517]

Adds the QA-only file_linear_bug tool that creates Linear issues via
the LinearClient from Task 1.1. Auto-appends merchant ContextVar +
source footer to the description. Returns error envelope when
LINEAR_API_KEY is missing. System prompt instructs the agent to file
on user cues ('log this as a bug') without asking confirmation."
```

---

### Task 1.3: Wire LINEAR_API_KEY into qa-agent service (GUARDIAN)

**Files:**
- Modify: `Canary/devops/docker-compose.localhost.yml` (GUARDIAN)
- Modify: `Canary/.guardian-manifest`

- [ ] **Step 1: Read the qa-agent service block**

```bash
cd /Users/gclyle/GrowDirect/Canary
sed -n '418,445p' devops/docker-compose.localhost.yml
```

Verify the `environment:` block. Add one line:

```yaml
      LINEAR_API_KEY: ${LINEAR_API_KEY:-}
```

(The `:-` default means the var is passed through from the shell/.env; if unset, qa-agent sees an empty string and `_handle_file_linear_bug` returns the "not configured" error envelope — no container crash.)

- [ ] **Step 2: Compute new SHA for the manifest**

```bash
shasum -a 256 devops/docker-compose.localhost.yml
```

- [ ] **Step 3: Update `.guardian-manifest`**

Find the `devops/docker-compose.localhost.yml` entry. Update `sha256`, `last_guardian_edit` (current UTC ISO-8601), and `reason` to `"GRO-517: Add LINEAR_API_KEY pass-through for file_linear_bug tool"`. Also bump the top-level `updated_at`.

- [ ] **Step 4: Commit**

```bash
git add devops/docker-compose.localhost.yml .guardian-manifest
git commit -m "chore(devops): wire LINEAR_API_KEY into qa-agent service [GRO-517]

Pass LINEAR_API_KEY through from .env to the qa-agent container env.
When unset, file_linear_bug returns an error envelope — no container
crash. User adds the actual key to .env separately (guardian-protected,
not part of this commit).

Guardian: manifest SHA256 bumped for docker-compose.localhost.yml."
```

---

## Chunk 2: Atlas frontmatter strip + F3 prompt (Feature 3)

### Task 2.1: Strip YAML frontmatter from atlas_figure return

**Files:**
- Modify: `Canary/canary/services/atlas/tools.py`

- [ ] **Step 1: Read the current handler**

```bash
cd /Users/gclyle/GrowDirect/Canary
sed -n '30,41p' canary/services/atlas/tools.py
```

- [ ] **Step 2: Add frontmatter stripper + integrate**

Add a helper at module scope (near the top of `tools.py`, after imports):

```python
import re as _re

_FRONTMATTER_RE = _re.compile(
    r"^---\s*\n.*?\n---\s*\n+",
    _re.DOTALL,
)


def _strip_yaml_frontmatter(content: str) -> str:
    """Remove a leading YAML frontmatter block (--- ... ---) from a markdown
    string. If no frontmatter is present, return content unchanged."""
    if not content:
        return content
    return _FRONTMATTER_RE.sub("", content, count=1)
```

Update `_handle_atlas_figure`:

```python
def _handle_atlas_figure(params: Dict, context: Dict) -> Dict[str, Any]:
    """Load a full atlas figure by ID. Strips YAML frontmatter from the
    content field so the chat UI doesn't render raw --- metadata blocks."""
    from canary.services.atlas.service import AtlasService
    figure_id = params.get("figure_id", "").strip()
    if not figure_id:
        return {"error": "figure_id is required"}
    svc = AtlasService()
    result = svc.get_figure(figure_id)
    if not result:
        return {"error": f"Figure {figure_id} not found"}
    # GRO-517 F3: strip frontmatter so agent can inline content cleanly.
    if "content" in result and isinstance(result["content"], str):
        result = {**result, "content": _strip_yaml_frontmatter(result["content"])}
    return result
```

- [ ] **Step 3: Verify syntax**

```bash
python3 -m py_compile canary/services/atlas/tools.py
```

- [ ] **Step 4: Commit**

```bash
git add canary/services/atlas/tools.py
git commit -m "feat(atlas): strip YAML frontmatter from atlas_figure content [GRO-517]

atlas_figure previously returned the raw figure file including the
leading '--- figure: ...\n---' frontmatter. When the QA Agent inlines
that content into chat (F3), users saw the --- block above the
rendered mermaid. Strip it server-side here; metadata is already
exposed on the .metadata field for callers that need it."
```

---

### Task 2.2: SYSTEM_PROMPT F3 addition

**Files:**
- Modify: `Canary/canary/services/qa_agent/agent.py`

- [ ] **Step 1: Add the F3 section**

In `agent.py`, find the SYSTEM_PROMPT (already updated by Task 1.2). Add BEFORE "Response style" (and after the F2 "Filing bugs" section):

```
## Atlas diagrams

When the user asks about architecture, data flow, or a specific atlas figure,
call `atlas_figure(figure_id: ...)`. The tool returns a `content` field with
markdown that contains a ```mermaid``` code block. INCLUDE THE FULL `content`
FIELD VERBATIM in your response — do not summarize or link to it. The chat UI
renders mermaid blocks inline. If you return only a summary, the user won't
see the diagram.
```

- [ ] **Step 2: Verify**

```bash
python3 -c "
from canary.services.qa_agent.agent import SYSTEM_PROMPT
assert 'atlas_figure' in SYSTEM_PROMPT
assert 'VERBATIM' in SYSTEM_PROMPT or 'verbatim' in SYSTEM_PROMPT
print('F3 prompt section present')
"
```

- [ ] **Step 3: Commit**

```bash
git add canary/services/qa_agent/agent.py
git commit -m "feat(qa-agent): SYSTEM_PROMPT F3 — inline atlas_figure content [GRO-517]

Instructs the agent to include atlas_figure's content field verbatim
in responses instead of linking. Works with the frontmatter strip from
the previous commit — the returned content is now clean markdown that
qa.html's existing mermaid renderer handles inline."
```

---

## Chunk 3: Tests

### Task 3.1: Linear client unit tests

**Files:**
- Create: `Canary/tests/unit/test_qa_agent_linear_client.py`

- [ ] **Step 1: Create the test file**

```python
"""Unit tests for LinearClient (GRO-517 F2).

Mocks requests.post — never touches the real Linear API.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from canary.services.qa_agent.linear_client import LinearClient, LinearAPIError


def _make_response(body: dict, status: int = 200, request_id: str = "req-1"):
    mock = MagicMock()
    mock.status_code = status
    mock.headers = {"x-request-id": request_id}
    mock.json.return_value = body
    return mock


@patch("canary.services.qa_agent.linear_client.requests.post")
def test_create_issue_sends_graphql_mutation(mock_post):
    # 3 calls expected: team lookup, project lookup, label lookup, then mutation
    mock_post.side_effect = [
        _make_response({"data": {"teams": {"nodes": [{"id": "team-1", "name": "Growdirect"}]}}}),
        _make_response({"data": {"team": {"projects": {"nodes": [{"id": "proj-1", "name": "Canary"}]}}}}),
        _make_response({"data": {"team": {"labels": {"nodes": [
            {"id": "lab-1", "name": "Canary Builder"},
            {"id": "lab-2", "name": "Bug"},
        ]}}}}),
        _make_response({"data": {"issueCreate": {"success": True, "issue": {
            "id": "iss-1", "identifier": "GRO-999", "url": "https://linear.app/.../GRO-999"
        }}}}),
    ]

    client = LinearClient(api_key="lin_api_test")
    result = client.create_issue(title="Test bug", description="Observed X; expected Y")

    assert result == {
        "id": "iss-1",
        "identifier": "GRO-999",
        "url": "https://linear.app/.../GRO-999",
    }

    # The last call is the mutation — verify auth header + body shape
    last_call = mock_post.call_args_list[-1]
    assert last_call.kwargs["headers"]["Authorization"] == "lin_api_test"
    assert "Bearer" not in last_call.kwargs["headers"]["Authorization"]
    assert "issueCreate" in last_call.kwargs["json"]["query"]
    assert last_call.kwargs["json"]["variables"]["input"]["teamId"] == "team-1"
    assert last_call.kwargs["json"]["variables"]["input"]["projectId"] == "proj-1"
    assert set(last_call.kwargs["json"]["variables"]["input"]["labelIds"]) == {"lab-1", "lab-2"}


@patch("canary.services.qa_agent.linear_client.requests.post")
def test_resolves_team_project_labels_once(mock_post):
    # Same 4 responses as above, then repeat just the mutation for the second create
    base_responses = [
        _make_response({"data": {"teams": {"nodes": [{"id": "team-1", "name": "Growdirect"}]}}}),
        _make_response({"data": {"team": {"projects": {"nodes": [{"id": "proj-1", "name": "Canary"}]}}}}),
        _make_response({"data": {"team": {"labels": {"nodes": [{"id": "lab-1", "name": "Canary Builder"}, {"id": "lab-2", "name": "Bug"}]}}}}),
        _make_response({"data": {"issueCreate": {"success": True, "issue": {
            "id": "iss-1", "identifier": "GRO-999", "url": "https://linear.app/1"
        }}}}),
        _make_response({"data": {"issueCreate": {"success": True, "issue": {
            "id": "iss-2", "identifier": "GRO-1000", "url": "https://linear.app/2"
        }}}}),
    ]
    mock_post.side_effect = base_responses

    client = LinearClient(api_key="lin_api_test")
    client.create_issue(title="First", description="x")
    client.create_issue(title="Second", description="y")

    # 3 lookups + 2 mutations = 5 calls total (not 6 + 2)
    assert mock_post.call_count == 5


@patch("canary.services.qa_agent.linear_client.requests.post")
def test_raises_linear_api_error_on_graphql_errors(mock_post):
    mock_post.return_value = _make_response({
        "errors": [{"message": "Team not found", "extensions": {"requestId": "req-xyz"}}]
    })

    client = LinearClient(api_key="lin_api_test")
    with pytest.raises(LinearAPIError) as exc_info:
        client.create_issue(title="x", description="y")

    assert "Team not found" in exc_info.value.message
    assert exc_info.value.request_id == "req-xyz"


@patch("canary.services.qa_agent.linear_client.requests.post")
def test_label_lookup_handles_missing_label(mock_post):
    """If 'Canary Builder' doesn't exist, file without it — don't fail-closed."""
    mock_post.side_effect = [
        _make_response({"data": {"teams": {"nodes": [{"id": "team-1", "name": "Growdirect"}]}}}),
        _make_response({"data": {"team": {"projects": {"nodes": [{"id": "proj-1", "name": "Canary"}]}}}}),
        _make_response({"data": {"team": {"labels": {"nodes": [{"id": "lab-2", "name": "Bug"}]}}}}),
        _make_response({"data": {"issueCreate": {"success": True, "issue": {
            "id": "iss-1", "identifier": "GRO-999", "url": "https://linear.app/x"
        }}}}),
    ]

    client = LinearClient(api_key="lin_api_test")
    result = client.create_issue(title="x", description="y")

    assert result["identifier"] == "GRO-999"
    # Mutation call labelIds should only contain lab-2
    mutation_call = mock_post.call_args_list[-1]
    assert mutation_call.kwargs["json"]["variables"]["input"]["labelIds"] == ["lab-2"]


@patch("canary.services.qa_agent.linear_client.requests.post")
def test_missing_url_or_identifier_raises(mock_post):
    mock_post.side_effect = [
        _make_response({"data": {"teams": {"nodes": [{"id": "team-1", "name": "Growdirect"}]}}}),
        _make_response({"data": {"team": {"projects": {"nodes": [{"id": "proj-1", "name": "Canary"}]}}}}),
        _make_response({"data": {"team": {"labels": {"nodes": [{"id": "lab-1", "name": "Canary Builder"}, {"id": "lab-2", "name": "Bug"}]}}}}),
        _make_response({"data": {"issueCreate": {"success": True, "issue": {
            "id": "iss-1", "identifier": None, "url": None  # malformed
        }}}}),
    ]

    client = LinearClient(api_key="lin_api_test")
    with pytest.raises(LinearAPIError, match="missing url/identifier"):
        client.create_issue(title="x", description="y")
```

- [ ] **Step 2: Run the tests**

```bash
cd /Users/gclyle/GrowDirect/Canary
python3 -m pytest tests/unit/test_qa_agent_linear_client.py -v
# Expected: 5 passed
```

- [ ] **Step 3: Commit**

```bash
git add tests/unit/test_qa_agent_linear_client.py
git commit -m "test(qa-agent): Linear client unit tests [GRO-517]

5 tests: happy-path mutation shape + auth header, cache-once behavior,
GraphQL error handling, graceful missing-label degradation, defensive
parsing when issueCreate returns malformed response."
```

---

### Task 3.2: Atlas frontmatter strip unit tests

**Files:**
- Create: `Canary/tests/unit/test_atlas_figure_frontmatter_strip.py`

- [ ] **Step 1: Create the test file**

```python
"""Unit tests for YAML frontmatter stripping in atlas_figure (GRO-517 F3).

Mocks AtlasService.get_figure to return synthetic figure data.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from canary.services.atlas.tools import _handle_atlas_figure, _strip_yaml_frontmatter


def test_strip_removes_frontmatter():
    content = "---\nfigure: pipe-001\ntitle: Pipeline\n---\n\n# Title\n\n```mermaid\ngraph TD\nA-->B\n```\n"
    result = _strip_yaml_frontmatter(content)
    assert result.startswith("# Title")
    assert "figure: pipe-001" not in result


def test_strip_noop_without_frontmatter():
    content = "# Title\n\n```mermaid\ngraph TD\nA-->B\n```\n"
    assert _strip_yaml_frontmatter(content) == content


def test_strip_noop_on_empty():
    assert _strip_yaml_frontmatter("") == ""


@patch("canary.services.atlas.tools.AtlasService")
def test_atlas_figure_strips_frontmatter(mock_svc_cls):
    mock_svc = MagicMock()
    mock_svc.get_figure.return_value = {
        "metadata": {"figure": "x", "title": "X"},
        "content": "---\nfigure: x\ntitle: X\n---\n\n# Body\n\n```mermaid\ngraph TD\nA-->B\n```\n",
        "path": "/tmp/x.md",
    }
    mock_svc_cls.return_value = mock_svc

    result = _handle_atlas_figure({"figure_id": "x"}, {})

    assert result["content"].startswith("# Body")
    assert "figure: x" not in result["content"]
    # Metadata untouched
    assert result["metadata"]["figure"] == "x"


@patch("canary.services.atlas.tools.AtlasService")
def test_atlas_figure_no_frontmatter_passthrough(mock_svc_cls):
    mock_svc = MagicMock()
    raw = "# Just body\n\n```mermaid\ngraph TD\nA-->B\n```\n"
    mock_svc.get_figure.return_value = {"metadata": {}, "content": raw, "path": "/tmp/y.md"}
    mock_svc_cls.return_value = mock_svc

    result = _handle_atlas_figure({"figure_id": "y"}, {})

    assert result["content"] == raw
```

- [ ] **Step 2: Run**

```bash
python3 -m pytest tests/unit/test_atlas_figure_frontmatter_strip.py -v
# Expected: 5 passed
```

- [ ] **Step 3: Commit**

```bash
git add tests/unit/test_atlas_figure_frontmatter_strip.py
git commit -m "test(atlas): frontmatter strip unit tests [GRO-517]

5 tests on _strip_yaml_frontmatter (regex behavior) and
_handle_atlas_figure (integration with AtlasService)."
```

---

### Task 3.3: file_linear_bug integration tests

**Files:**
- Create: `Canary/tests/integration/test_qa_agent_file_linear_bug.py`

- [ ] **Step 1: Create the test file**

```python
"""Integration tests for file_linear_bug tool handler (GRO-517 F2).

Mocks LinearClient — never calls the real Linear API. Uses the real
_merchant_ctx ContextVar from session_factory.
"""

from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

import pytest

from canary.db.session_factory import set_merchant_context, clear_merchant_context

pytestmark = pytest.mark.postgres


@pytest.fixture
def fake_linear_client():
    mock = MagicMock()
    mock.create_issue.return_value = {
        "id": "iss-1",
        "identifier": "GRO-999",
        "url": "https://linear.app/growdirect/issue/GRO-999",
    }
    with patch("canary.services.qa_agent.tools.LinearClient", return_value=mock) as ctor_mock:
        yield ctor_mock, mock


def test_file_linear_bug_happy_path_with_merchant_context(
    fake_linear_client, monkeypatch, test_merchant,
):
    monkeypatch.setenv("LINEAR_API_KEY", "lin_api_test")
    _, client_mock = fake_linear_client

    token = set_merchant_context(str(test_merchant.id))
    try:
        from canary.services.qa_agent.tools import execute_tool
        result = execute_tool("file_linear_bug", {
            "title": "Alert count off",
            "description": "User saw 5, agent reported 3.",
        })
    finally:
        clear_merchant_context(token)

    assert result.get("ok") is True
    assert result["identifier"] == "GRO-999"
    assert result["url"] == "https://linear.app/growdirect/issue/GRO-999"

    client_mock.create_issue.assert_called_once()
    call_kwargs = client_mock.create_issue.call_args.kwargs
    desc = call_kwargs["description"]
    assert "Auto-appended context" in desc
    assert str(test_merchant.id) in desc
    assert "Source: QA Agent chat" in desc


def test_file_linear_bug_no_merchant_context_still_files(
    fake_linear_client, monkeypatch,
):
    """Graceful degradation branch: no merchant bound, tool still fires."""
    monkeypatch.setenv("LINEAR_API_KEY", "lin_api_test")
    _, client_mock = fake_linear_client

    # Do NOT set_merchant_context
    from canary.services.qa_agent.tools import execute_tool
    result = execute_tool("file_linear_bug", {
        "title": "Anon bug",
        "description": "Something broke.",
    })

    assert result.get("ok") is True
    desc = client_mock.create_issue.call_args.kwargs["description"]
    assert "Source: QA Agent chat" in desc
    # No merchant line
    assert "**Merchant:**" not in desc


def test_file_linear_bug_no_api_key_returns_error(monkeypatch):
    """Missing env var returns structured error — no network call."""
    monkeypatch.delenv("LINEAR_API_KEY", raising=False)

    from canary.services.qa_agent.tools import execute_tool
    result = execute_tool("file_linear_bug", {
        "title": "x",
        "description": "y",
    })

    assert "error" in result
    assert "LINEAR_API_KEY" in result["error"]


def test_file_linear_bug_requires_title_and_description():
    """Input validation before any client instantiation."""
    from canary.services.qa_agent.tools import execute_tool
    r1 = execute_tool("file_linear_bug", {"title": "", "description": "y"})
    r2 = execute_tool("file_linear_bug", {"title": "x", "description": ""})
    assert "error" in r1
    assert "error" in r2
```

- [ ] **Step 2: Run**

```bash
CANARY_DB_URL="postgresql://growdirect:growdirect_dev@localhost:5432/canary" \
  python3 -m pytest tests/integration/test_qa_agent_file_linear_bug.py -v -m postgres
# Expected: 4 passed
```

- [ ] **Step 3: Commit**

```bash
git add tests/integration/test_qa_agent_file_linear_bug.py
git commit -m "test(qa-agent): file_linear_bug integration tests [GRO-517]

4 tests covering execute_tool dispatch of file_linear_bug: happy path
with merchant ContextVar in auto-footer, graceful no-merchant branch,
missing-env-var error envelope, and input validation on empty title/
description. LinearClient mocked throughout."
```

---

## Verification Checklist (end of session)

- [ ] 5 Linear-client unit tests pass
- [ ] 5 atlas-frontmatter unit tests pass
- [ ] 4 file_linear_bug integration tests pass (@pytest.mark.postgres)
- [ ] Full regression: `pytest tests/unit/test_session_factory_standalone.py tests/unit/test_qa_agent_context_header.py tests/integration/test_qa_agent_chat.py tests/integration/test_qa_agent_chat_with_context.py tests/integration/test_qa_agent_db.py` still passes
- [ ] Rebuild qa-agent: `docker compose -f devops/docker-compose.localhost.yml up -d --build qa-agent`
- [ ] `docker logs canary_localhost_qa_agent` shows standalone-mode init, no errors
- [ ] **Requires user-added `LINEAR_API_KEY`** — live gate:
  - curl `/chat` with `[Page: /chirps | Merchant: ... | Visible: ...]\n\nlog this as a bug - the alert count was wrong` → agent calls `file_linear_bug` → response contains a real `GRO-xxx` identifier and URL
  - Open the URL in Linear, verify title/description/labels/project/merchant footer
- [ ] atlas gate:
  - `curl /chat` with `show me the detection pipeline atlas diagram`
  - Agent calls `atlas_figure` and response text contains ` ```mermaid ` (not a markdown link)

## Commit Trail Expected

1. `feat(qa-agent): Linear GraphQL client for bug filing [GRO-517]` — linear_client.py
2. `feat(qa-agent): file_linear_bug tool + SYSTEM_PROMPT F2 [GRO-517]` — tools.py + agent.py
3. `chore(devops): wire LINEAR_API_KEY into qa-agent service [GRO-517]` — compose + manifest
4. `feat(atlas): strip YAML frontmatter from atlas_figure content [GRO-517]` — atlas/tools.py
5. `feat(qa-agent): SYSTEM_PROMPT F3 — inline atlas_figure content [GRO-517]` — agent.py
6. `test(qa-agent): Linear client unit tests [GRO-517]` — test file
7. `test(atlas): frontmatter strip unit tests [GRO-517]` — test file
8. `test(qa-agent): file_linear_bug integration tests [GRO-517]` — test file

8 commits, bisectable. Tests grouped into 3 commits (one per test file) rather than one giant tests commit — aids bisect into individual test files.

## Skills to Invoke During Execution

- `@superpowers:test-driven-development` for Tasks 3.1, 3.2, 3.3 (test-first preferred)
- `@superpowers:verification-before-completion` before claiming done

## What I need from the user

1. **`LINEAR_API_KEY=lin_api_xxx` added to `/Users/gclyle/GrowDirect/Canary/.env`** — required for the live E2E gate. Without it, all commits merge cleanly and all tests pass (mocks handle absence), but the live `file_linear_bug` call fails with the configured error message. Not a blocker for merging.
