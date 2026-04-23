---
title: QA Agent Tier 1 — Linear bug filing + Atlas inline rendering
date: 2026-04-23
project: Canary
linear:
  - GRO-517 (Features 2 and 3)
  - Parent GRO-326, predecessors GRO-389, Feature 1
status: Design approved, ready for implementation plan
---

# QA Agent Tier 1 — Features 2 & 3 (bundled spec)

Two small features of GRO-517. Both lightweight, both sidecar-side. Bundled into
one spec/plan/branch because they're each only a few files of change and don't
share code.

## Feature 2 — Linear bug filing from chat

### Problem

Users hit bugs, realize it mid-conversation, and say "log this as a bug." Today
the QA Agent can only apologize. Jeffe has to stop, context-switch to Linear,
compose the issue from scratch. The conversation context (what tool calls fired,
what the agent saw) is the exact thing a bug report needs and is already in
memory.

### Goal

Agent invokes a new QA-only tool `file_linear_bug(title, description)` that
creates a real Linear issue with: the chat thread's last few turns, the list of
tool calls invoked, the merchant ID (from ContextVar), and sensible defaults
for team/project/labels. Agent replies with the Linear issue URL.

### Scope

**In:**
- `file_linear_bug(title, description)` tool in `canary/services/qa_agent/tools.py`
- Minimal Linear GraphQL client in `canary/services/qa_agent/linear_client.py`
- `LINEAR_API_KEY` env var wiring (compose + .env)
- SYSTEM_PROMPT section instructing the agent when to offer the tool
- Unit + integration tests with mocked Linear API

**Out (deferred):**
- Attaching the conversation as a file (description-only for Tier 1)
- Per-merchant routing (everything goes to team `Growdirect`, project `Canary`)
- UI affordance for the user to edit the drafted bug before it files (v2 consideration)
- Rate limiting specific to bug filing (existing chat rate limits apply)

### Architecture

```
User: "hey, this alert count looks wrong — log it as a bug"
    ↓
Claude (SYSTEM_PROMPT trained to recognize "log as bug" cues)
    ↓ tool_use
file_linear_bug(title: "Alert count inconsistent", description: "User saw 5 alerts but agent returned 3. [merchant details]")
    ↓
tools.py _handle_file_linear_bug:
  1. Pull merchant UUID from _merchant_ctx
  2. Pull session_id + prior tool_calls from context dict (if passed) or reconstruct from `messages`
  3. Append structured context block to description
  4. Call linear_client.create_issue(...) with defaults
    ↓
linear_client.create_issue:
  - POST https://api.linear.app/graphql
  - headers: Authorization: <LINEAR_API_KEY>
  - mutation: issueCreate(input: {teamId, projectId, title, description, labelIds})
  - resolve team/project/label IDs on first call, cache for session
    ↓
Returns {url, identifier, id}
    ↓
Agent responds: "Filed [GRO-XYZ](https://linear.app/.../GRO-XYZ): Alert count inconsistent"
```

### Component 1 — Linear client

**File:** `canary/services/qa_agent/linear_client.py` (new)

Single-responsibility module:
- `class LinearClient` — wraps the GraphQL endpoint
- Method `create_issue(title, description, team="Growdirect", project="Canary", labels=("Canary Builder", "Bug")) -> dict`
- Uses `requests` (already in Canary's deps) for sync HTTP from the async sidecar — called in a threadpool via `asyncio.to_thread` from the tool handler if needed, or just synchronously since tool dispatch is inside the sidecar's HTTP handler and a ~500ms Linear call is acceptable.
- On startup OR first call, resolves team ID + project ID + label IDs via one-time GraphQL queries; cached on the client instance.
- Raises `LinearAPIError` with `.message` and `.request_id` on failure.

### Component 2 — QA tool handler

**File:** `canary/services/qa_agent/tools.py` (modified)

Add to the `_qa_tool_defs` list:

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
                "description": "Bug description. Include what the user expected and what they observed. Do NOT include the conversation transcript or merchant ID — those are auto-appended."
            },
        },
        "required": ["title", "description"],
    },
},
```

Add `_handle_file_linear_bug`:

```python
def _handle_file_linear_bug(params: dict) -> dict[str, Any]:
    import os
    from canary.db.session_factory import _merchant_ctx
    from canary.services.qa_agent.linear_client import LinearClient, LinearAPIError

    title = params.get("title", "").strip()
    description = params.get("description", "").strip()
    if not title or not description:
        return {"error": "title and description are required"}

    api_key = os.getenv("LINEAR_API_KEY")
    if not api_key:
        return {"error": "LINEAR_API_KEY not configured in sidecar env"}

    # Auto-append merchant + context (if available)
    merchant_id = _merchant_ctx.get()
    auto_footer = "\n\n---\n\n## Auto-appended context\n"
    if merchant_id:
        auto_footer += f"- **Merchant:** `{merchant_id}`\n"
    auto_footer += "- **Source:** QA Agent chat (`/ops/qa`)\n"
    # Note: conversation transcript is passed in via params["_session_context"]
    # when called from execute_tool — leaves a hook for future use. For Tier 1
    # we file with just title + description + merchant. Agent should put
    # observed/expected in the description.

    full_description = description + auto_footer

    client = LinearClient(api_key=api_key)
    try:
        result = client.create_issue(title=title, description=full_description)
        return {
            "ok": True,
            "identifier": result["identifier"],  # e.g., "GRO-520"
            "url": result["url"],
            "title": title,
        }
    except LinearAPIError as e:
        return {"error": f"Linear API error: {e.message}", "request_id": e.request_id}
```

### Component 3 — Compose + env wiring

**File:** `Canary/devops/docker-compose.localhost.yml` (modified)

Add `LINEAR_API_KEY` to the `qa-agent` service environment block. Value from `.env` (user adds `LINEAR_API_KEY=lin_api_xxx` to their `.env` before rebuilding the sidecar). Without it, the tool returns an error envelope rather than crashing.

**Note:** `.env` is guardian-protected. User approved the env addition; still needs a `critical-file-guardian` touch to land (or direct edit since user granted guardian permission earlier). Implementation plan calls this out.

### Component 4 — SYSTEM_PROMPT addition

Add near the "Response style" section in `canary/services/qa_agent/agent.py`:

```
## Filing bugs

If the user says "log this as a bug", "file this", "report this", or similar,
call `file_linear_bug(title, description)` immediately — do not ask for
confirmation. Title is your best short description of the issue (< 80 chars).
Description is a brief summary of what the user observed vs expected. Don't
include merchant IDs, conversation transcripts, or timestamps — those are
auto-appended server-side.

After the tool returns, reply with the Linear identifier and a clickable link:
"Filed [GRO-XYZ](<url>): <title>"
```

## Feature 3 — Atlas inline rendering

### Problem

`atlas_figure` returns a figure dict whose `content` field contains markdown
with embedded ` ```mermaid``` ` code blocks. Today the agent summarizes or
links to it; the user has to navigate to view the diagram. The chat UI already
loads mermaid.js and renders ` ```mermaid``` ` blocks inline (`qa.html:336-337`)
— but only when the markdown is in the agent's response text.

### Goal

When the agent calls `atlas_figure`, it includes the figure's `content` field
verbatim in its response. The mermaid block renders inline. One prompt
instruction, zero template changes, zero tool-result payload changes.

### Scope

**In:**
- SYSTEM_PROMPT instruction telling the agent to include the full `content` of
  the atlas figure in its response (not just a link).

**Out (deferred):**
- PNG/SVG rendering for non-mermaid figures (all current figures are mermaid)
- Caching rendered diagrams server-side
- Server-side injection of the mermaid block if the agent forgets (possible
  future safety net; deferred unless the prompt proves unreliable)

### Architecture

No code change. The pipeline is:

```
User: "show me the alert pipeline diagram"
    ↓
Claude (SYSTEM_PROMPT trained to include atlas content verbatim)
    ↓ tool_use
atlas_figure(figure_id: "pipe-001")
    ↓
handler returns {title, content: "# Title\n```mermaid\ngraph TD...\n```", ...}
    ↓
Claude's next turn: text response embeds the content verbatim
    ↓
qa.html renderMarkdown catches the ```mermaid block → renders inline via mermaid.js
```

### SYSTEM_PROMPT addition

Add near the tools section:

```
## Atlas diagrams

When the user asks about architecture, data flow, or a specific atlas figure,
call `atlas_figure(figure_id: ...)`. The tool returns a `content` field with
markdown that contains a mermaid code block. INCLUDE THE FULL `content` FIELD
VERBATIM in your response — do not summarize or link to it. The chat UI
renders mermaid blocks inline. If you return only a summary, the user won't see
the diagram.
```

## Testing

### Feature 2

**Unit** — `tests/unit/test_qa_agent_linear_client.py` (new)

- `test_create_issue_sends_graphql_mutation` — mock `requests.post`; assert the
  request URL is `https://api.linear.app/graphql`, body contains
  `issueCreate(input: ...)`, headers include `Authorization: <key>`.
- `test_resolves_team_project_labels_once` — create two issues; assert
  team/project/label lookup queries fire only on the first call.
- `test_raises_linear_api_error_on_graphql_errors` — mock a response containing
  `errors: [{message: ..., requestId: ...}]`; assert `LinearAPIError` raised
  with those fields.

**Integration** — `tests/integration/test_qa_agent_file_linear_bug.py`
(new, `@pytest.mark.postgres`)

- `test_file_linear_bug_happy_path_with_merchant_context` — mock
  `linear_client.LinearClient`; set merchant ContextVar; call
  `execute_tool("file_linear_bug", {"title": ..., "description": ...})`; assert
  mock `create_issue` was called with a description containing the merchant
  UUID; assert returned dict has `url` and `identifier`.
- `test_file_linear_bug_no_api_key_returns_error` — no env var; assert
  `{"error": "...API key not configured..."}` returned, no network call.

### Feature 3

Prompt-only behaviour — not practical to unit-test against mocked Anthropic
(the prompt isn't evaluated there). Covered by manual smoke in the completeness
gate: navigate to `/ops/qa`, ask "show me the chirp pipeline diagram," verify
the response contains a rendered mermaid SVG in the chat bubble.

If the prompt proves unreliable in real use (agent links instead of inlining),
add server-side post-processing in `handle_chat`: scan `all_tool_calls` for
`atlas_figure`, fetch the content, inject a `\n\n<mermaid-content>` suffix into
the response text. Deferred unless needed.

## Completeness gate

1. **Bug filing data in:** from `/ops/qa`, say "log this as a bug — the alert
   count on /chirps looked wrong." Agent calls `file_linear_bug`, returns a
   URL.
2. **Bug filing data out:** open the URL in Linear. Confirm:
   - Title + description from the agent
   - Auto-footer contains merchant UUID + `Source: QA Agent chat (/ops/qa)`
   - Issue is in team `Growdirect`, project `Canary`, has labels `Canary
     Builder` + `Bug`
3. **Atlas diagram inline:** navigate `/ops/qa`, ask "show me the detection
   pipeline atlas diagram." Agent response contains a mermaid block that
   renders as an SVG inline in the chat bubble (not a markdown link).
4. **Unit + integration tests:** 3 unit + 2 integration tests pass against the
   live test DB.

## Linear closeout

- Update GRO-517: Features 2 and 3 shipped. The issue can be closed as Done
  once Feature 1 + 2 + 3 are all confirmed live. GRO-519 (drawer unification)
  remains open as a separate follow-up.

## Risks and non-goals

- **LINEAR_API_KEY must be added to `.env`.** Without it, the tool returns an
  error and the agent apologizes gracefully. Not a code failure mode.
- **Linear API rate limits.** Linear allows ~1500 requests/hour for personal
  API keys — the sidecar's in-process limits (50/session, 200/day) cap bug
  filing well below Linear's ceiling.
- **Agent may forget to inline mermaid content.** Feature 3 is prompt-only.
  If reliability is poor, add the server-side injection noted in Testing.
- **Description truncation.** Linear issue descriptions max at ~65KB. Current
  design appends a short auto-footer; well within limits. Not handled.
- **No authentication on `file_linear_bug`.** Anyone with admin access to
  `/ops/qa` can file Linear issues. Acceptable — admin gating is enforced at
  the Flask blueprint level, not the sidecar.

## Commit strategy

1. `feat(qa-agent): Linear GraphQL client for bug filing [GRO-517]` — linear_client.py
2. `feat(qa-agent): file_linear_bug tool + SYSTEM_PROMPT update [GRO-517]` — tools.py + agent.py
3. `chore(devops): wire LINEAR_API_KEY into qa-agent service [GRO-517]` — docker-compose.localhost.yml
4. `feat(qa-agent): SYSTEM_PROMPT — inline atlas_figure mermaid content [GRO-517]` — agent.py (small Feature 3 addition; may combine with #2 depending on coherence)
5. `test(qa-agent): Linear client + file_linear_bug integration [GRO-517]` — 2 test files

5 commits, bisectable. User updates `.env` separately (outside the commit
stream — .env is gitignored).
