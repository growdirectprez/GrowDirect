---
screen: /agents/:id
title: Agent Detail
role: ADM | MGR
wave: W3
origin: N
cp_equivalent: "None — CP has no agent infrastructure"
---

# Agent Detail

**URL:** `/agents/:id`  
**Primary role:** ADM; MGR  
**Entry points:** Agent roster row

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Agent name, type, status badge | Breadcrumb back to /agents |
| Top section | Agent identity + configuration summary | |
| Tab bar | Activity / Flags / MCP Junctions / Configuration | |
| Tab content | Tab-dependent | |

## Tabs

### Activity Tab
Timeline of agent actions over the selected period (default: last 24h). Each entry: timestamp, action type (alert routed, recommendation created, report sent, flag raised), action detail, outcome (success / failed / skipped).

**Volume chart:** Bar chart of actions per hour. Agents with scheduled runs show pulse patterns; always-on agents show continuous low-volume activity. An unusual spike or a flat-zero period during normal operating hours are both anomalies worth investigating.

### Flags Tab
List of open flags raised by this agent awaiting human decision. Each flag: flag type, raised timestamp, context (what triggered the flag), status (Open / Acknowledged / Resolved), assigned to.

**Flags vs. Alerts:** Flags are internal agent-to-human communications within Canary's operational layer. Alerts are LP-facing notifications to the investigation team. An Alert Dispatcher might raise a flag: "Alert routing rule for B2B class has no destination configured — 3 alerts unrouted." That's an operational flag, not an LP alert.

### MCP Junctions Tab
List of MCP junctions this agent is authorized to interact with. Columns: Junction ID, Name, Permission (read / write), Last Used, Status (Healthy / Degraded / Unreachable).

**Junction health is agent-specific context.** If the Alert Dispatcher depends on junction Q.2 (the alert dispatch junction) and Q.2 is Unreachable, the agent's Error status is explained. This tab shows exactly which junctions the agent relies on and their current health.

### Configuration Tab
Agent-specific parameters. For scheduled agents: run schedule (cron expression or named interval), retry behavior, pause/resume control. For always-on agents: watchdog interval, failure threshold (how many consecutive failures before status = Error).

**Pause/Resume:** ADM can pause any agent (temporarily suspends its activity). Used during maintenance, testing, or when a configuration change needs to propagate before the agent runs again.

**Empty state per tab:** "No [activity/flags/junctions/configuration] for this agent."

## Interaction Flows

1. **Error diagnosis:** ADM opens Alert Dispatcher detail → Activity tab → last 10 entries all failed with "junction Q.2 unreachable" → MCP Junctions tab confirms Q.2 = Unreachable → investigates Q.2 separately → restores junction → agent auto-resumes
2. **Flag resolution:** ADM opens Replenishment Monitor → Flags tab → 3 open flags: "item #8812 below reorder point for 14 days — PO not created" → ADM creates PO → closes flags
3. **Configuration adjustment:** ADM opens Distribution Optimizer → Configuration tab → currently scheduled daily at 2am → store operations need it to run at 6am for morning buyer review → updates schedule → saves

## UX Callout

The MCP Junctions tab is the observability feature that makes Canary's "166 junctions" architecture tangible. Rather than a count in a spec, each agent shows exactly which junctions it uses, with real-time health status. When something goes wrong — alerts not routing, recommendations not updating — the agent detail's junction health tab is the diagnostic starting point. This is standard practice in service mesh architecture (circuit breaker visibility per service dependency); Canary brings that operational discipline to the retail software layer where it has never existed before.

## Navigation Exits

- `/agents` — back to agent roster
- `/admin/devops/health` — from junction health alert

## Open Questions

None.
