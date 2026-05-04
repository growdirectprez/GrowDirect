---
screen: /devices
title: Device Fleet Overview
role: MGR | ADM
wave: W2
origin: N
cp_equivalent: "None — CP has no device management surface"
---

# Device Fleet Overview

**URL:** `/devices`  
**Primary role:** MGR (store-scoped); ADM (cross-tenant)  
**Entry points:** Primary sidebar nav (Devices section)

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Page title "Devices", summary counts | |
| Filter bar | Store, Device Type, Status | |
| Main content | Device table | |

## Key Elements

### Summary Counts (Header)
Four tiles: **Total Devices** · **Online** · **Offline** · **Needs Attention** (yellow/red status). At a glance, MGR knows if a device issue exists before reading the table.

### Device Table
Columns: Device Name, Store, Device Type (Terminal / Scale / Scanner / Printer), Model, Last Seen (timestamp), Status badge (Online / Offline / Warning / Decommissioned), IP Address, Actions.

**Status definitions:**
- **Online:** Heartbeat received within the configured interval (default: 5 min).
- **Offline:** No heartbeat for > configured offline threshold (default: 15 min). Row tint: orange.
- **Warning:** Heartbeat active but device reporting degraded state (low battery, paper jam, calibration drift on scales). Row tint: yellow.
- **Decommissioned:** Manually retired. Hidden by default; toggle to show in filter.

**Last Seen column:** Human-readable ("2 minutes ago", "3 hours ago"). Hover shows exact timestamp. Sorts descending — longest-absent devices surface at top.

**Device Type icons:** Distinct icon per device type for fast visual scanning without reading the Type column text.

### Add Device
ADM-only button. Opens device registration flow (out of scope for this brief; placeholder for device onboarding spec). Appears for ADM only; MGR sees read-only view of their store's devices.

**Empty state:** "No devices registered for this store. Contact your system administrator to add devices."

## Interaction Flows

1. **Morning station check:** MGR opens Devices → sees 1 Offline (POS terminal 3 at checkout lane 4) → clicks to open detail → sees Last Seen = 47 minutes ago → initiates reboot or contacts IT
2. **Scale calibration warning:** MGR sees Warning status on produce scale → detail shows "calibration drift detected — last calibration 18 days ago" → schedules recalibration
3. **ADM fleet overview:** ADM filters to Tenant X → sees all 6 stores' devices → two stores showing Offline terminals → flags for remediation

## UX Callout

There is no equivalent to this screen in CP. CP's terminal management is entirely outside the POS — hardware is managed by IT or the VAR via Windows device management tools, with no visibility from within the POS application. Canary's device list exists because Canary is MCP-native and the device layer is part of the intelligence surface. A POS terminal going offline for 47 minutes is either a technical fault or a deliberate disconnection — from LP's perspective, those look different, and neither is visible in CP. Having device status alongside transaction data means that "no transactions from terminal 3 between 2pm and 3pm" can be cross-referenced against "terminal 3 was offline between 2pm and 3pm" — same event, very different explanations.

## Navigation Exits

- `/devices/:id` — device detail
- `/devices/health` — device health analytics
- `/devices/cameras` — camera subfleet (placeholder)
- `/devices/sensors` — sensor subfleet (placeholder)

## Open Questions

None.
