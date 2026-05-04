---
screen: /admin/tenants/:id
title: Tenant Detail
role: ADM
wave: Cross
origin: FD
cp_equivalent: "None"
---

# Tenant Detail

**URL:** `/admin/tenants/:id`  
**Primary role:** ADM  
**Entry points:** Tenant list row click; Config Health → tenant row

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Tenant name, status badge, created date, back link | Breadcrumb to /admin/tenants |
| Left column | Tenant info card + adapter config summary | ~40% width |
| Right column | LP Rollout Phase control + backfill progress + sync status panels | ~60% width |
| Action bar | Suspend tenant, Delete tenant (danger), Trigger re-sync | Bottom of left column; destructive actions behind confirmation |

## Key Elements

### Tenant Info Card
Tenant name, primary contact, store count, adapter type. Adapter connection status (connected / disconnected / auth-error). Last adapter poll timestamp.

### Adapter Config Summary
Adapter type displayed; credentials shown as `••••••••` (masked). "Test Connection" button — triggers an on-demand adapter health check without re-saving credentials.

### LP Rollout Phase Control
Phase selector (1–4) with phase descriptions inline:
- Phase 1: Config sync only — no rules firing
- Phase 2: Dry-run mode — rules evaluate but no alerts generated
- Phase 3: LP alerting live — alerts visible to LP users
- Phase 4: Full W-module active — cross-domain exceptions enabled

Advancing phases is audited (appears in `/admin/audit`). Rollback to prior phase is allowed.

### Backfill Progress
Progress bar for historical data backfill (T-module). Shows: total records to import, records imported, estimated completion. If stalled: "Last progress 23 hours ago — potential issue" with manual resume trigger.

### Sync Status Summary
N.1/N.2/N.3 sync status tiles with last-synced timestamp per module. Identical to `/admin/config` detail, surfaced here for completeness.

## Interaction Flows

1. **Advance LP rollout:** ADM reviews backfill as 100% complete, N.1–N.3 synced → changes LP Rollout Phase from 1 to 3 → confirmation modal ("LP alerting will activate for all stores in this tenant") → confirms → phase change audited
2. **Test adapter connection:** ADM clicks "Test Connection" → system sends test request to CP adapter → result appears within 5 seconds: "Connected — CP API responding in 240ms" or error details
3. **Diagnose stalled backfill:** ADM sees backfill stuck at 67% for 2 days → clicks "Resume Backfill" → system restarts from last checkpoint → ADM monitors progress

## UX Callout

The LP Rollout Phase control is the most important element on this screen. Multi-tenant SaaS onboarding requires a graduated activation model — the alternative is tenants getting flooded with alerts the moment they're provisioned, before their teams are trained and their allow-lists are configured. This screen is how ADM manages that graduation deliberately. No CP equivalent exists because CP's activation model is binary: the software is installed or it isn't.

## Navigation Exits

- `/admin/tenants` — back to tenant list
- `/admin/config` — config health across all tenants
- `/admin/users` — users assigned to this tenant

## Open Questions

None.
