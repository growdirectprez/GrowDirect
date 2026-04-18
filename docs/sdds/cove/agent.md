# Agent Module

**Status:** Active
**Type:** App Service (with external API dependency)
**Last updated:** 2026-04-13
**Blueprint:** `agent_bp` at `/agent`
**Wiki:** [[Brain/wiki/cove-governance|Cove Governance]]
**Architecture:** [[docs/sdds/cove/architecture|Cove Architecture]]

---

## Purpose

AI-powered community governance assistant providing natural language Q&A, meeting agenda generation, notice compliance tracking, quorum status reporting, and a public transparency log. Uses the Anthropic Claude API (claude-haiku-4-5) with injected community and governance context. Currently stateless -- no conversation memory between requests.

---

## Dependencies

| Dependency | Role | Required |
|------------|------|----------|
| PostgreSQL (`cove` database) | Organization, parcel, member, proposal data for context building | Yes |
| `anthropic` Python package | Claude API client | No (graceful degradation) |
| `ANTHROPIC_API_KEY` env var | API authentication | No (Q&A disabled without it) |
| `cove.governance.bylaws_config` | Quorum rules, thresholds, notice periods | Yes |
| `cove.governance.services` | `check_quorum()`, `get_eligible_voter_count()` | Yes (for quorum endpoint) |

---

## Data Flow & PII Map

### What enters
- User questions via JSON or form POST (text only, no file uploads)
- Organization ID from session (for context building)

### What's stored
**Nothing.** The agent module creates no database records. Context is built from read-only queries.

### What exits
- **Agent Q&A response**: Claude API response text (JSON)
- **Agenda**: Structured meeting agenda from current governance state (JSON)
- **Quorum status**: Voting progress per open proposal (JSON)
- **Transparency log**: Recent governance activity (rendered HTML)
- **To Anthropic API**: System prompt containing community context (member counts, proposal titles, bylaws rules -- no individual PII)

### PII Classification

| Data | Classification | Notes |
|------|---------------|-------|
| User question | internal | Sent to Anthropic API in user message |
| Community context (system prompt) | internal | Aggregate counts, no individual member data |
| Proposal titles in context | internal | Governance records, not personal |
| Agent response | internal | May reference governance rules, no member PII |

**PII safeguards in system prompt:**
- Explicitly forbids revealing private member info (phone, personal email)
- Forbids referencing ocean paths or easements in public context
- Board access check not yet implemented (member_id passed but unused)

---

## API Contract

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/agent/transparency` | `login_required` | Transparency log with compliance status and query form |
| POST | `/agent/api/ask` | `login_required` | Natural language Q&A (JSON or form POST) |
| GET | `/agent/api/agenda` | `login_required` | Structured meeting agenda |
| GET | `/agent/api/quorum` | `login_required` | Quorum status for open proposals |

### Response Formats

**`POST /agent/api/ask`:**
- Success: `{"answer": "...", "configured": true}`
- Not configured: `{"answer": "The AI agent is not configured...", "configured": false}`
- Missing question: `{"error": "No question provided."}` (400)

**`GET /agent/api/agenda`:**
- `{"date": "...", "org": "...", "items": [...], "context": "...", "generated_at": "..."}`

**`GET /agent/api/quorum`:**
- Array of `{"proposal_id", "title", "type", "eligible_voters", "votes_cast", "quorum_required", "quorum_met", "participation_rate"}`

---

## Services (`cove/agent/services.py`)

### Context Builders

| Function | Description |
|----------|-------------|
| `build_community_context(org_id)` | Queries org, parcels, members, proposals, bylaws to build system prompt context |
| `build_governance_context(org_id)` | Formats active proposals with type, threshold, secret ballot status |

### Agent Operations

| Function | Description |
|----------|-------------|
| `generate_meeting_agenda(org_id, meeting_date)` | Structured agenda from open proposals |
| `check_notice_compliance(org_id)` | Validates notice periods against bylaws config; returns compliance issues with severity |
| `get_quorum_status(org_id)` | Voting progress per open proposal |
| `generate_transparency_log(org_id)` | Recent governance activity (current month onward) |

### Claude API Integration

| Function | Description |
|----------|-------------|
| `_get_client()` | Returns `anthropic.Anthropic` client or `None` |
| `ask_cove_agent(org_id, question, member_id)` | Sends question to Claude claude-haiku-4-5 with injected context |

**Context injection pattern:** System prompt includes role definition, behavioral rules, community state, and active governance. Single user message (no history). Member ID accepted but not used.

---

## Operations

### Startup
No module-specific startup. Anthropic client created on first request.

### Health Checks
No module-specific health check. API availability checked on each request via `_get_client()`.

### Failure Modes

| Failure | Impact | Recovery |
|---------|--------|----------|
| `ANTHROPIC_API_KEY` not set | Q&A returns "not configured"; agenda/quorum/transparency work normally | Set env var |
| `anthropic` package not installed | Same as above | `pip install anthropic` |
| Anthropic API rate limited | Q&A request fails | Retry with backoff |
| Anthropic API error | Q&A returns None, route returns "not configured" | Transparent to user |
| DB down | Context builders fail, all routes 500 | Automatic reconnect |

### Configuration

| Variable | Required | Default |
|----------|----------|---------|
| `ANTHROPIC_API_KEY` | No | (none -- Q&A disabled) |

### Monitoring
- Alert on: Anthropic API error rate, API cost per day
- Normal: <50 Q&A requests/day for 81-member HOA

---

## Deployment

Standard Cove deployment. No module-specific infrastructure beyond the Anthropic API key.

- **AWS**: `ANTHROPIC_API_KEY` in Secrets Manager
- **Cost**: claude-haiku-4-5 pricing (~$0.001/request typical)

---

## Code Review Findings

| # | Severity | Finding | Recommended Fix |
|---|----------|---------|----------------|
| 1 | **P0** | No rate limiting on `/agent/api/ask` -- any authenticated user can make unlimited Anthropic API calls (cost exposure) | Add Flask-Limiter: e.g., 10 requests/minute per user |
| 2 | **P1** | `member_id` passed to `ask_cove_agent` but never used -- no per-role context filtering | Implement: board members get fuller context; regular members get redacted context |
| 3 | **P1** | No audit trail for Q&A interactions -- cannot track what questions were asked or who asked them | Add audit log entries for agent queries (store question, not full response) |
| 4 | **P1** | System prompt privacy rules are advisory (prompt-level) not enforced (code-level) -- Claude could still leak info if jailbroken | Add post-processing filter on agent responses to strip detected PII patterns |
| 5 | **P1** | Anthropic API errors caught silently -- `_get_client()` returns None for any error, no logging | Add structured error logging for API failures |
| 6 | **P2** | Stateless -- no conversation memory, each question is independent | Add session-based conversation context for multi-turn Q&A |
| 7 | **P2** | Transparency log only shows proposals from current month onward -- no historical depth | Add configurable lookback period |
| 8 | **P2** | No caching for community/governance context -- rebuilt on every request | Cache context in Valkey with 5-minute TTL |

---

## Production Readiness Checklist

- [x] No PII stored (agent creates no database records)
- [ ] Rate limiting on `/agent/api/ask` (P0 -- cost exposure)
- [ ] Secrets in AWS Secrets Manager (`ANTHROPIC_API_KEY`)
- [x] Health check endpoint responds (via app-level `/health`)
- [ ] Audit logging for Q&A interactions
- [x] Graceful degradation without API key
- [x] Error responses don't leak internals
- [ ] Post-processing PII filter on agent responses
- [ ] API cost monitoring and alerting
- [ ] Per-role context filtering (board vs member)
