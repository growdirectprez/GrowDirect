# Angel Agent

> **Status:** Proposed — design spec, not yet built
> **Namespace:** angel
> **Date:** 2026-04-06
> **Author:** ALX (COO) / Jeffe (CEO)
> **Pattern:** Canary QA Agent sidecar (GRO-326)
> **Dependencies:** Angel data platform, Cove parcel bridge, ATTOM MCP

---

## 1. Overview

Angel Agent is a Claude-powered conversational assistant that knows every
property on the Palos Verdes peninsula. It runs as a sidecar container (the
same architecture as Canary's QA Agent) and can be embedded as a chat widget
on any website — AngeliqueLyle.com, TheHillPV.com, or a standalone page.

The agent's personality is **Angel** — a warm, knowledgeable AI assistant that
speaks with Angelique Lyle's voice and draws on a proprietary local dataset.
It answers questions about neighborhoods, schools, property history, market
trends, and listings. When a conversation reaches a decision point (ready to
tour, wants a CMA, needs to talk to an agent), Angel captures the lead and
routes it to Angelique via SMS notification and Compass CRM sync.

**What makes Angel different from generic real estate chatbots:**
- Proprietary APN-level data for every parcel on the peninsula (not just active listings)
- Cove's community governance data (HOA membership, Lot H status, tract history)
- ATTOM enrichment (deed history, ownership chain, AVM, school data)
- 2,368 MLS listing records with full transaction history
- Angelique's actual voice and local expertise, not corporate boilerplate

---

## 2. Architecture

### Component Diagram

```
Website (chat widget — JS embed)
    │  POST /api/chat  (JSON, message history + visitor context)
    │
    ▼
Cove Flask App (port 5002)
    │  Blueprint: angel_chat_bp (registered in Cove app)
    │  Rate limiting: 10 req/min per IP
    │  Visitor session tracking (Valkey DB 1)
    │
    │  POST http://angel-agent:8004/chat  (120s timeout)
    ▼
Angel Agent Sidecar (uvicorn ASGI, port 8004)
    │  angel/services/agent/server.py
    │  In-memory rate limiting (30/session, 150/day)
    │  Builds Anthropic client
    │  Passes SYSTEM_PROMPT + tool_definitions + messages
    │
    ▼
Anthropic API (claude-sonnet-4-20250514, max_tokens=4096)
    │  tool_use response blocks
    ▼
angel/services/agent/tools.py  ← tool dispatch (in-process)
    ├── Parcel tools (parcel_lookup, parcel_history, nearby_parcels)
    ├── Listing tools (listing_search, listing_detail, market_stats)
    ├── Community tools (neighborhood_profile, school_info)
    ├── Content tools (cma_summary, listing_strategy)
    └── Lead tools (capture_lead, schedule_callback)
    │
    ▼
Final text response → Cove Flask → Widget
    + lead_captured flag → SMS notification → Compass CRM
```

### Key Design Decisions

**Sidecar pattern (inherited from Canary QA Agent).** The agent runs in its
own container, communicating with Flask via HTTP. Flask has no Anthropic SDK
dependency. The sidecar is stateless — conversation history lives in the
browser widget and is forwarded with each request.

**Consumer-facing, not operator-facing.** Unlike Canary's QA Agent (internal
ops tool), Angel Agent is public-facing. This changes the safety model:
- No write access to any database (read-only tools only)
- No raw data exposure (APN details are summarized, not dumped)
- Conversation is bounded (max 20 turns per session)
- PII handling: visitor phone/email captured only through explicit lead_capture tool
- Fair Housing compliance: never steer based on demographics, income, race, religion

**Personality-first prompting.** The system prompt establishes Angel as
Angelique's AI assistant — not a generic chatbot. It references specific
neighborhoods, school names, local landmarks, and market patterns. This is
the competitive moat: no other agent has an AI that actually knows the Hill.

---

## 3. System Prompt

The system prompt is built from three layers:

### Layer 1: Identity and Voice

```
You are Angel, Angelique Lyle's AI assistant for Palos Verdes real estate.
You help home buyers, sellers, and curious neighbors understand the peninsula
— its neighborhoods, schools, market trends, and property details.

Voice rules:
- First person when speaking as Angel ("I can look that up for you")
- Warm, confident, grounded — never salesy or pushy
- Specific local knowledge — street names, school campuses, neighborhood character
- Lead with empathy — acknowledge that real estate decisions are personal
- When you don't know something, say so and offer to connect them with Angelique

Never say: "stunning," "luxury lifestyle," "dream home," "act fast"
Never: make income or appreciation guarantees
Always: Fair Housing compliant — no steering based on protected classes
```

### Layer 2: Knowledge Context (Injected per request)

```
[Peninsula context — current market snapshot]
Active listings: {count}, Median list price: ${median}
Recent closings (30 days): {count}, Median close: ${median}
Inventory: {months} months supply

[Neighborhood summaries — precomputed from data]
RPV: {summary}  PVE: {summary}  RHE: {summary}  RH: {summary}

[Visitor context — from widget/session]
Page: {current_url}  Referrer: {referrer}  Session: {turn_count} turns
```

### Layer 3: Tool Instructions

```
You have tools to look up specific properties, search listings, check school
info, and generate market comparisons. Use them — don't guess at data.

When the visitor is ready to take a next step (tour, CMA, talk to Angelique),
use the capture_lead tool to collect their phone number and route to Angelique.
Frame this naturally: "I'd love to connect you with Angelique directly — what's
the best number to reach you?"
```

---

## 4. MCP Tools

Angel Agent exposes ~12 tools organized by domain:

### 4.1 Parcel Tools

| Tool | Purpose | Data Source |
|------|---------|------------|
| `parcel_lookup` | Look up a property by APN or address | Cove bridge + Angel listings |
| `parcel_history` | Ownership and transaction history for an APN | ATTOM + listings |
| `nearby_parcels` | Properties within radius of a point or APN | Cove geometry + listings |

**`parcel_lookup` input schema:**
```json
{
  "query": "string — APN, address fragment, or MLS#",
  "include_listing": "boolean — include active/recent listing data (default true)",
  "include_assessment": "boolean — include county assessed values (default false)"
}
```

**`parcel_lookup` output:** Summarized property card (not raw data). Includes
address, beds/baths/sqft, year built, lot size, current status, last sale,
and Cove community membership if applicable.

### 4.2 Listing Tools

| Tool | Purpose | Data Source |
|------|---------|------------|
| `listing_search` | Search listings by criteria (area, price, beds, status) | Angel listings table |
| `listing_detail` | Full detail for a specific MLS# | Angel listings table |
| `market_stats` | Market statistics for an area and time period | Angel market_snapshots |
| `transaction_history` | Recent closed transactions for an area | Angel listings (Closed) |

**`listing_search` input schema:**
```json
{
  "area": "string — RPV, PVE, RHE, RH, or 'peninsula'",
  "status": "string — Active, Closed, Pending, or 'all' (default Active)",
  "min_price": "integer | null",
  "max_price": "integer | null",
  "min_beds": "integer | null",
  "property_type": "string — SFR, Condo, or 'all' (default 'all')",
  "limit": "integer — max results (default 10, max 25)"
}
```

### 4.3 Community Tools

| Tool | Purpose | Data Source |
|------|---------|------------|
| `neighborhood_profile` | Character, amenities, market position of a neighborhood | Knowledge base + data |
| `school_info` | School ratings, feeder patterns, boundaries | GreatSchools + knowledge |
| `commute_estimate` | Drive time / distance from an address to common destinations | Computed |

### 4.4 Strategy Tools

| Tool | Purpose | Data Source |
|------|---------|------------|
| `cma_summary` | Quick comparative market analysis for a property | Listings + assessments |
| `listing_strategy` | Suggested pricing and timeline for a potential listing | Market data + knowledge |
| `concierge_calc` | Compass Concierge ROI estimate for a property | Knowledge base |

### 4.5 Lead Tools

| Tool | Purpose | Side Effect |
|------|---------|------------|
| `capture_lead` | Collect visitor contact info and route to Angelique | Creates Lead record, sends SMS |
| `schedule_callback` | Schedule a specific callback time | Creates Lead + calendar event |

**`capture_lead` input schema:**
```json
{
  "visitor_name": "string",
  "visitor_phone": "string",
  "visitor_email": "string | null",
  "interest": "string — buying, selling, curious, relocation",
  "property_apn": "string | null — if discussing a specific property",
  "notes": "string — conversation summary for Angelique"
}
```

**Side effects:**
1. Create Lead record in Angel database (stage: "contacted")
2. Send SMS to Angelique's phone: "New lead from Angel: {name}, {interest}, {property}"
3. Queue Compass CRM sync (async, via Valkey)

---

## 5. Safety and Compliance

### Fair Housing

The agent MUST NOT:
- Steer buyers toward or away from neighborhoods based on race, religion, national origin, sex, familial status, disability, or other protected classes
- Volunteer demographic information about neighborhoods unless asked about specific, lawful topics (school ratings, walkability)
- Make assumptions about a visitor's background or financial situation

The system prompt includes explicit Fair Housing guardrails. Tool outputs are
reviewed to ensure they don't include demographic data that could enable steering.

### Data Protection

- All tools are read-only (no writes to Cove or external systems)
- PII (phone, email) is only collected through the explicit `capture_lead` tool
- Visitor conversation history is not stored server-side (browser-owned, stateless sidecar)
- Rate limiting prevents abuse: 30 messages/session, 150/day per IP

### Compliance Disclosures

Every conversation includes a footer in the widget:
```
Angel is an AI assistant. For professional real estate advice, contact
Angelique Lyle, REALTOR® | DRE# 01475592 | Compass
```

---

## 6. Chat Widget

### Embed Pattern

A lightweight JavaScript widget that can be added to any website:

```html
<!-- Angel Chat Widget -->
<script src="https://thehillpv.com/widget/angel.js" defer></script>
<script>
  AngelChat.init({
    position: 'bottom-right',
    greeting: "Hi! I'm Angel — ask me anything about Palos Verdes.",
    theme: 'warm',      // matches brand palette
    referrer: 'lp'      // or 'thehillpv', 'ownpv'
  });
</script>
```

### Widget States

1. **Collapsed** — Floating action button (FAB) in bottom-right corner.
   Subtle pulse animation on first visit. "Ask Angel" tooltip.
2. **Expanded** — Chat panel (400px wide, 600px tall on desktop; full-screen
   on mobile). Message input, conversation history, typing indicator.
3. **Lead capture** — Inline form within chat flow when `capture_lead` is
   triggered. Phone number field + optional email. Submit → confirmation
   message → continue conversation.

### Visitor Context

The widget passes context with each request:
- `page_url` — current page (helps Angel reference the property being viewed)
- `referrer` — which site (LP, TheHillPV, direct)
- `session_id` — anonymous session for rate limiting
- `turn_count` — conversation depth

---

## 7. Deployment

### Container

```dockerfile
# Dockerfile.angel-agent
FROM python:3.12-slim AS base
WORKDIR /app
COPY requirements-agent.txt .
RUN pip install --no-cache-dir -r requirements-agent.txt
COPY angel/ angel/
COPY knowledge/ knowledge/

FROM base
ENV ANGEL_AGENT_PORT=8004
ENV PYTHONUNBUFFERED=1
EXPOSE 8004
HEALTHCHECK CMD curl -f http://localhost:8004/health || exit 1
CMD ["python", "-m", "angel.services.agent.server"]
```

### Docker Compose

Angel Agent is added to Cove's compose file (no separate Angel Flask — blueprints
run in Cove):

```yaml
# In Cove/devops/docker-compose.yml — add this service to the existing compose

  angel-agent:
    image: angel-agent
    build:
      context: ../
      dockerfile: Dockerfile.angel-agent
    ports:
      - "8004:8004"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - DATABASE_URL=postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/cove
      - ATTOM_API_KEY=${ATTOM_API_KEY}
    networks:
      - growdirect
```

### Port Allocation

| Service | Port |
|---------|------|
| Cove Flask (hosts Angel blueprints) | 5002 |
| Angel Agent sidecar | 8004 |

---

## 8. Metrics and Monitoring

### Conversation Metrics (Valkey counters)

- `angel:conversations:total` — total conversations started
- `angel:conversations:leads` — conversations that produced a lead
- `angel:tools:{tool_name}:calls` — tool invocation counts
- `angel:sessions:avg_turns` — average turns per conversation

### Lead Funnel

```
Conversations started
    → Engaged (3+ turns)
        → Lead captured (phone collected)
            → Compass CRM synced
                → Callback completed
                    → Listing appointment
```

### Health Check

`GET /health` on port 8004 returns:
```json
{
  "status": "ok",
  "model": "claude-sonnet-4-20250514",
  "tools_loaded": 12,
  "uptime_seconds": 86400,
  "conversations_today": 42,
  "leads_today": 3
}
```

---

*Angel Agent SDD — GrowDirect Inc.*
