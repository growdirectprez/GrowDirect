---
screen: /admin/tenants
title: Tenant Management
role: ADM
wave: Cross
origin: FD
cp_equivalent: "None"
---

# Tenant Management

**URL:** `/admin/tenants`  
**Primary role:** ADM  
**Entry points:** Admin nav; Config Health screen → tenant name link

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Page title "Tenants", New Tenant button | New Tenant triggers provisioning wizard |
| Filter bar | Search (name/ID), Status filter, LP Phase filter | Filters apply instantly |
| Main content | Paginated tenant table | One row per tenant |

## Key Elements

### Tenant Table
Columns: Tenant Name, Tenant ID (UUID, truncated), Status (Active / Suspended / Provisioning), Store Count, LP Rollout Phase (1–4), Adapter Type (NCR Counterpoint / Rapid Garden POS / other), Config Sync (✓/⚠/✗), Created Date.

LP Rollout Phase maps to the Q-module deployment lifecycle: Phase 1 = Config sync active; Phase 2 = LP rules enabled in dry-run; Phase 3 = LP alerting live; Phase 4 = Full W-module active.

**Empty state:** Not applicable — multi-tenant ADM view always has at least one tenant.

### Status Badge
- Active: all services running, LP rules firing normally
- Provisioning: initial setup in progress (config sync, backfill, adapter auth)
- Suspended: intentionally paused (billing, compliance hold)

### New Tenant Wizard (triggered from header button)
Step 1: Tenant name, primary contact email, store count. Step 2: Adapter type and connection credentials (ADM enters; not visible after save). Step 3: LP rollout phase assignment. Step 4: Confirm + provision.

## Interaction Flows

1. **Provision new tenant:** ADM clicks New Tenant → wizard opens → fills tenant details + adapter config → sets LP Phase 1 → confirms → provisioning job starts → row appears in table with "Provisioning" status
2. **Advance tenant to Phase 3:** ADM clicks tenant row → navigates to `/admin/tenants/:id` → LP Rollout Phase control → advances to Phase 3 → LP alerting activates for this tenant
3. **Suspend tenant:** ADM clicks tenant row → detail screen → Suspend action → all LP detection pauses, user access preserved but data ingestion stops

## UX Callout

This screen exists because Canary is a multi-tenant SaaS platform, not a single-store installation. There is no CP equivalent — CP is per-store, per-machine. The LP Rollout Phase column is critical for managing phased customer onboarding: a new tenant starting at Phase 1 (config sync only) should not accidentally have full LP alerting active. This screen gives ADM the control plane for that graduation.

## Navigation Exits

- `/admin/tenants/:id` — tenant detail, LP rollout phase management, adapter config
- `/admin/config` — config health for all tenants

## Open Questions

None.
