---
screen: /agents
title: Agent Roster
role: ADM | MGR
wave: W3
origin: N
cp_equivalent: "None — CP has no agent infrastructure"
---

# Agent Roster

**URL:** `/agents`  
**Primary role:** ADM; MGR  
**Entry points:** Primary sidebar nav (Agents section)

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Agents", filter bar | |
| Filter bar | Status, Type, Store scope | |
| Main content | Agent roster table | |

## Key Elements

### Agent Roster Table
Columns: Agent Name, Type, Scope (store or cross-store), Status (Active / Paused / Error), Last Run (timestamp), Actions Taken (count in last 24h), Open Flags, Linked MCP Junctions.

**Type values:**
- **Alert Dispatcher:** Routes detection alerts to the correct destination based on alert routing rules. Always-on.
- **Replenishment Monitor:** Checks inventory positions against reorder points; queues replenishment recommendations. Scheduled.
- **Distribution Optimizer:** Generates distribution recommendations from perpetual ledger. Scheduled (default: daily).
- **Anomaly Watcher:** Monitors transaction feed for patterns not covered by named rules. Always-on.
- **Report Scheduler:** Executes scheduled report delivery (flash report email, shrink digest). Scheduled.

**Linked MCP Junctions:** Each agent operates through the MCP junction network. The count shown is how many of the 166 junctions this agent is authorized to read from or write to.

### Open Flags
Count of active flags raised by this agent that require human decision. An alert dispatcher with 0 open flags is functioning normally; one with 14 open flags may have a routing configuration issue or a surge in unresolved alerts.

**Status = Error:** Agent encountered a persistent failure (e.g., MCP junction unreachable, malformed event payload). Error badge + error description on hover. ADM must resolve before the agent resumes.

**Empty state:** "No agents configured. Contact your administrator."

## Interaction Flows

1. **Fleet health check:** ADM opens agent roster → all agents Active, open flags normal → no action needed
2. **Error investigation:** ADM sees Alert Dispatcher in Error state → opens agent detail → error: "MCP junction Q.2 unreachable — last success 2h ago" → checks admin → devops → health → confirms junction is degraded → restores junction → agent auto-resumes
3. **MGR agent visibility:** MGR opens agents → sees store-scoped agents for own store → Replenishment Monitor last ran 6 hours ago, 3 recommendations queued → opens distribution recommendations to review

## UX Callout

The agent roster is the operational surface for the MCP-native layer that defines Canary's architecture. In CP, there is no agent infrastructure — all workflows are human-initiated. Canary's agents are the "always-on" layer that runs between human interactions: they watch the transaction feed, check inventory positions, route alerts, and surface recommendations while the staff is focused on the store floor. The roster gives ADM visibility into whether these agents are working, how often, and where they've flagged issues requiring human attention. The MCP junction count is the observability signal — an agent that touches 40 junctions but has been in Error state for 2 hours has been blind for 2 hours; that's actionable context.

## Navigation Exits

- `/agents/:id` — agent detail

## Open Questions

None.
