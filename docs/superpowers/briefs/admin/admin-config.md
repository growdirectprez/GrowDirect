---
screen: /admin/config
title: System Config Health
role: ADM
wave: Cross
origin: O
cp_equivalent: "None — Counterpoint has no cloud-side config health surface"
---

# System Config Health

**URL:** `/admin/config`  
**Primary role:** ADM  
**Entry points:** Admin nav; automated alert when config ingestion fails

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Page title "Config Health", Last-checked timestamp (auto-refreshes every 5 min) | Shows freshness of the health data |
| Summary banner | Summary counts: tenants synced, tenants with issues, tenants in backfill | Green/yellow/red aggregate status |
| Main content | Tenant table — one row per tenant | Primary working surface |
| Detail drawer | Opens on row click — error detail, manual re-sync trigger | Side panel, non-destructive |

## Key Elements

### Tenant Table
Columns: Tenant Name, N.1 Sync Status (Store Config — stores/locations), N.2 Sync Status (Item Catalog), N.3 Sync Status (Customer/AR config), LP Substrate Status (drawer thresholds / discount caps / void/comp reason codes — populated or missing), Last Sync Timestamp, Backfill Progress (%), Error Indicator (red icon if last sync failed).

**Status values:** ✓ Current (synced within expected interval), ⚠ Stale (last sync > threshold), ✗ Failed (last sync returned error), — Not started.

**Empty state:** Not applicable — table always shows at least one row (the provisioned tenant).

### LP Substrate Status
Specific flag for whether the four N.4 configuration values (drawer threshold, discount cap, void reasons, comp reasons) are populated for this tenant. If LP Substrate = "Missing", detection rules that depend on these thresholds will not fire — a critical operational gap. This column is the canary-in-the-coal-mine for new tenant onboarding.

### Detail Drawer
Opens on row click: last sync error message (verbatim), last 5 sync attempts with timestamps and outcomes, manual "Re-sync Now" button per config module. Re-sync is non-destructive — overwrites stale config with fresh data from CP API.

### PCI / Tokenization Status Panel
Below the tenant table: a summary of tokenization status per tenant (P1 gap from L4 delta). Indicates whether the tenant's card payment flow has tokenization active. ADM alert surface for PCI compliance posture without requiring a full audit tool.

## Interaction Flows

1. **Identify LP-dark tenant:** ADM scans table → sees Tenant "Sunrise Garden Center" has LP Substrate = Missing → clicks row → drawer shows N.4 fields not yet populated → ADM triggers config re-sync → monitors for ✓ status
2. **Diagnose failed sync:** ADM sees red ✗ indicator on Tenant "Mesa Feeds" → clicks row → drawer shows error: "Connection refused to CP REST API: timeout after 30s" → ADM contacts tenant to verify CP service is running
3. **Monitor backfill progress:** New tenant just provisioned → ADM monitors Backfill Progress column → watches it increment from 0% to 100% as historical data loads → confirms N.1–N.3 sync complete before enabling LP monitoring

## UX Callout

This screen has no Counterpoint equivalent because CP is not a cloud system — there is no "sync status" in a single-store Windows installation. For Canary's multi-tenant SaaS model, config health is an operational prerequisite: a tenant whose config hasn't synced is a tenant without LP coverage, and the ADM has no other way to know. The LP Substrate Status column specifically prevents the scenario where a tenant thinks Canary is monitoring their store but detection rules are actually silently suppressed due to missing threshold configuration.

## Navigation Exits

- `/settings/store/drawer` — if LP Substrate issues detected (link from drawer)
- `/admin/tenants/:id` — tenant detail for full provisioning context

## Open Questions

None.
