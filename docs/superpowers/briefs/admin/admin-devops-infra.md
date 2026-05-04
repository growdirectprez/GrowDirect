---
screen: /admin/devops/infra
title: Infrastructure Overview
role: ADM
wave: Cross
origin: FD
cp_equivalent: "None"
---

# Infrastructure Overview

**URL:** `/admin/devops/infra`  
**Primary role:** ADM  
**Entry points:** Admin nav → DevOps → Infrastructure; Health dashboard card click

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Page title "Infrastructure", GCP project selector (if multi-project) | Displays active GCP project ID |
| Resource grid | One tile per major GCP resource type | Two-column layout |
| Cost summary | Monthly spend estimate (current month vs prior) | Right-aligned summary card |
| Event log | Last 20 infrastructure events (scaling, health-check failures, restarts) | Bottom of page |

## Key Elements

### Resource Tiles
One tile per resource class: Cloud Run (services + revision count + current instance count), Cloud SQL (primary + replica — status, disk used %, connection count), Cloud Storage (buckets — size, object count), Pub/Sub (topics + subscriptions — message backlog, oldest undelivered message age), Secret Manager (secret count, last rotation date), VPC / Networking (summary — no deep networking detail). Each tile shows: resource name, status, key metric, direct link to GCP Console (external, opens in new tab).

The tiles are read-only status surfaces. Configuration changes happen in GCP Console directly — this screen is observability only, not a management interface.

### Cost Summary Card
Current month GCP spend (pulled from Billing API) vs prior month. Budget threshold indicator (e.g., "85% of monthly budget used"). No payment actions available here — this is a visibility widget only. ADM uses it to catch runaway resource consumption before the billing cycle closes.

### Infrastructure Event Log
Last 20 events from GCP Logging: Cloud Run instance scale-up/down, Cloud SQL failover, health check failures, restarts. Each event links to the full GCP log entry. Provides context for health status changes without requiring GCP Console access for routine monitoring.

**Empty state on event log:** "No infrastructure events in the past 24 hours." — healthy baseline state.

## Interaction Flows

1. **Diagnose ingest backlog:** ADM sees T-module degraded on health dashboard → navigates to Infra → checks Pub/Sub tile → finds "oldest undelivered message: 4 hours ago" indicating a consumer is not processing → identifies Cloud Run instance for T-module shows 0 healthy instances → escalates to engineering
2. **Monitor post-deployment resource usage:** ADM reviews new deployment → checks Cloud Run tile → confirms instance count scaled appropriately, no excessive memory pressure
3. **Review cost spike:** ADM checks Cost Summary → sees 40% increase vs prior month → identifies Cloud SQL disk usage high → investigates backfill job impact

## UX Callout

Counterpoint has no infrastructure surface — it runs on a local PC and the operator has no visibility into server health whatsoever. Canary's GCP deployment has a dozen separately managed resources whose health directly affects what operators see in the product. This screen is not a replacement for GCP Console — it's a focused summary that answers "is the infrastructure healthy?" without requiring a cloud engineer. The cost tile specifically addresses the accountability rail: cloud providers oversell capacity and hope to cover spikes; Canary measures its own bill and acts on anomalies.

## Navigation Exits

- `/admin/devops/health` — service-level health for correlation
- `/admin/devops/deployments` — deployment log for change context
- GCP Console links (external) — for resource-level management

## Open Questions

None.
