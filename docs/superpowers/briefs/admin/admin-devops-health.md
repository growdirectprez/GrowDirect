---
screen: /admin/devops/health
title: Service Health Dashboard
role: ADM
wave: Cross
origin: FD
cp_equivalent: "None"
---

# Service Health Dashboard

**URL:** `/admin/devops/health`  
**Primary role:** ADM  
**Entry points:** Admin nav → DevOps → Health; automated alert notification deep-link

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Page title "Service Health", last-refreshed timestamp, auto-refresh toggle | Refreshes every 60s when toggle on |
| Top row | Aggregate status tiles: Overall, API, Ingest Pipeline, Adapters, MCP Junctions | Color-coded: green/yellow/red |
| Main content | Service grid — one card per service/module | Two-column grid |
| Bottom section | Active incident log (open incidents) + recent events | Time-ordered |

## Key Elements

### Service Status Tiles (Top Row)
Five aggregate tiles summarizing health by subsystem. Clicking a tile scrolls to the relevant service cards. If any service in a group is degraded, the tile shows yellow; if any is down, red.

### Service Cards (Main Grid)
One card per service. Each card shows: Service name, Current status (Healthy / Degraded / Down), Uptime (last 30 days), Latency (p50/p99, last 5 min), Error rate (%), Alert threshold (what triggers a status change). Cards are linked to logs: click → navigates to `/admin/devops/infra` or opens a log panel.

Services covered: API Gateway, T-module Ingest, D-module Perpetual Ledger, Q-module Rule Engine, N-module Config Sync, F-module Finance Processor, Memory Bus (pgvector), MCP Junction Layer (aggregate health), Database (primary + replica), Valkey/cache.

**Empty state (all healthy):** Full green grid — "All services healthy" banner at top.

### Active Incident Log
Open incidents only — any service that has been in degraded or down state for > 5 minutes generates an incident record. Columns: Incident ID, Service, Started, Duration (running), Severity, Assigned (blank until someone picks it up). Resolved incidents move to Recent Events.

### Recent Events
Last 20 status transitions: service name, from state, to state, timestamp. Provides quick context for whether a current degradation is a new onset or the tail of a longer event.

## Interaction Flows

1. **Triage alert notification:** ADM receives a PagerDuty-style alert → clicks deep link → lands on Health dashboard → identifies red card for "Q-module Rule Engine" → sees latency spike from 40ms to 2,400ms p99 → clicks card → log panel opens → identifies database query bottleneck
2. **Check before deployment:** ADM navigates here before initiating a deployment via `/admin/devops/deployments` → confirms all services green → proceeds
3. **Review overnight incident:** ADM checks morning status → sees resolved incident from 3am: "T-module Ingest: degraded for 14 minutes" → reviews recent events for root cause context

## UX Callout

Counterpoint is a Windows desktop application with no cloud health surface — if it's running, it's running; if it's not, the cashier calls IT. Canary's distributed GCP architecture has 10+ services that can degrade independently. This screen is how ADM knows which one is causing a user-visible problem without needing SSH access or a cloud console. The aggregate status tiles answer the question "is anything wrong right now?" in under 3 seconds — critical for an on-call ADM who isn't a Kubernetes engineer.

## Navigation Exits

- `/admin/devops/deployments` — deployment log; check what changed recently
- `/admin/devops/infra` — infrastructure view for deeper diagnosis
- `/agents/junctions` — MCP junction health (linked from junction tile)

## Open Questions

None.
