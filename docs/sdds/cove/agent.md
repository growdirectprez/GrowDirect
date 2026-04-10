# SDD: Agent Module

**Status:** Active
**Last updated:** 2026-03-29
**Blueprint:** `agent_bp`, registered at `/agent`

---

## Overview

AI-powered community governance assistant that provides natural language Q&A, meeting agenda generation, notice compliance tracking, quorum status reporting, and a public transparency log. Uses the Anthropic Claude API (claude-haiku-4-5) with injected community and governance context. Currently stateless -- no conversation memory or persistence between requests.

---

## Routes

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/agent/transparency` | Required | Render transparency log with compliance status and query form |
| POST | `/agent/api/ask` | Required | Accept JSON or form POST with `{"question": "..."}`, return agent response |
| GET | `/agent/api/agenda` | Required | Return structured meeting agenda for the current community |
| GET | `/agent/api/quorum` | Required | Return quorum status for all open proposals |

### API Response Formats

`POST /agent/api/ask`:
- Success: `{"answer": "...", "configured": true}`
- API not configured: `{"answer": "The AI agent is not configured...", "configured": false}`
- Missing question: `{"error": "No question provided."}` (400)

`GET /agent/api/agenda`:
- Returns `{"date": "...", "org": "...", "items": [...], "context": "...", "generated_at": "..."}`

`GET /agent/api/quorum`:
- Returns array of `{"proposal_id", "title", "type", "eligible_voters", "votes_cast", "quorum_required", "quorum_met", "participation_rate"}`

---

## Services

**`cove/agent/services.py`**

### Context Builders

| Function | What it does |
|----------|-------------|
| `build_community_context(org_id)` | Queries org, parcels, members, open proposals, and bylaws config to build a text summary of community state for the system prompt |
| `build_governance_context(org_id)` | Queries active proposals (draft/noticed/open) and formats them with type, threshold, and secret ballot status |

### Agent Operations

| Function | What it does |
|----------|-------------|
| `generate_meeting_agenda(org_id, meeting_date=None)` | Builds a structured agenda dict from open proposals -- drafts need review, noticed need opening, open need quorum check |
| `check_notice_compliance(org_id)` | Validates notice periods on all noticed/open proposals against bylaws config. Returns list of compliance issues (empty = compliant). Severity levels: `critical`, `warning` |
| `get_quorum_status(org_id)` | Calls `check_quorum()` and `get_eligible_voter_count()` from governance services for each open proposal. Returns voting progress and whether quorum is met |
| `generate_transparency_log(org_id)` | Returns a list of recent governance activity (proposals from current month onward) for the public transparency page |

### Claude API Integration

| Function | What it does |
|----------|-------------|
| `_get_client()` | Returns an `anthropic.Anthropic` client if `ANTHROPIC_API_KEY` is set, otherwise `None`. Handles missing `anthropic` package gracefully |
| `ask_cove_agent(org_id, question, member_id=None)` | Sends question to Claude claude-haiku-4-5 with community + governance context injected as the system prompt. Returns response text or `None` if API is not configured |

### Context Injection Pattern

The `ask_cove_agent` function constructs a system prompt that includes:

1. **Role definition** -- Cove is an AI community manager for WPBCA
2. **Behavioral rules** -- cite bylaw sections, protect private member data, never reference ocean paths/easements in public context
3. **Community state** (from `build_community_context`) -- org details, parcel/member counts, quorum rules, assessment limits, legislative updates
4. **Active governance** (from `build_governance_context`) -- all draft/noticed/open proposals with type and threshold

The user question is sent as a single user message. No conversation history is maintained between requests.

---

## Forms

**`cove/agent/forms.py`**

| Form | Fields | Description |
|------|--------|-------------|
| `QueryForm` | `question` (StringField, required, 3-1000 chars) | Natural language query input for the AI agent |

Inherits from `CoveForm` (CSRF automatic).

---

## Templates

| Template | Description |
|----------|-------------|
| `agent/transparency.html` | Renders the transparency log, notice compliance issues, and the query form. Referenced in `routes.py` but template is defined in the agent blueprint's `templates` directory |

Note: The blueprint declares `template_folder="templates"`, so agent templates are resolved relative to `cove/agent/templates/`.

---

## Dependencies

- `anthropic` Python package (optional -- gracefully returns `None` if missing)
- `ANTHROPIC_API_KEY` environment variable (optional -- Q&A disabled without it)
- `cove.governance.bylaws_config` -- `load_bylaws_config()` and `get_proposal_defaults()` for quorum/threshold/notice rules
- `cove.governance.services` -- `check_quorum()` and `get_eligible_voter_count()` for live quorum calculations

---

## Design Notes

- **Stateless**: No conversation memory -- each question is independent. Member ID is passed to `ask_cove_agent` but not currently used beyond the call signature.
- **Cost-effective**: Uses claude-haiku-4-5 (not Sonnet/Opus) for member Q&A to keep API costs low.
- **Graceful degradation**: All routes work without the Anthropic API key. The transparency log, agenda, and quorum endpoints use only database queries. Only Q&A requires the API.
- **Privacy safeguards**: System prompt explicitly forbids revealing private member info or referencing ocean access easements in public-facing context.
