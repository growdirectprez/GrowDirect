---
screen: /devices/health
title: Device Health Analytics
role: MGR | ADM | LP
wave: W2
origin: N
cp_equivalent: "None — CP has no device health analytics"
---

# Device Health Analytics

**URL:** `/devices/health`  
**Primary role:** ADM (cross-tenant fleet); MGR (own store); LP (investigative context)  
**Entry points:** Devices section → Health tab; admin devops health → device health link

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Device Health", date range selector | Default: last 7 days |
| Top section | Fleet health KPI tiles | |
| Main content | Health charts + offline event log | |
| Bottom section | Devices requiring attention table | |

## Key Elements

### Fleet Health KPI Tiles
Four tiles for the selected period:
- **Fleet Uptime %:** Average uptime across all active devices. Green ≥ 99%, yellow 95-99%, red < 95%.
- **Offline Events:** Total count of offline state transitions.
- **Mean Time to Restore (MTTR):** Average duration of offline events (from offline start → back online).
- **Devices with Issues:** Count of devices currently in Warning or Offline state.

### Uptime by Store
Bar chart: stores on X-axis, uptime % on Y-axis. Immediately shows which stores have device reliability problems. Clicking a bar filters the offline event log below to that store.

### Offline Event Log
Table: Device Name, Store, Offline Start, Offline End (or "Ongoing"), Duration, Type (Resolved / Ongoing). Sorted by duration descending — longest outages first.

**LP view of this log:** An offline event that starts when a high-alert period begins, or persists only during specific shift windows, is a correlation worth investigating. LP can cross-reference offline events with alert timestamps from the chirp feed.

### Firmware Version Distribution
Pie chart or grouped bar: what firmware versions are in use across the fleet. Highlights out-of-date devices that may be on a security-patched firmware but haven't been updated. ADM-visible only.

### Devices Requiring Attention Table
Auto-populated: any device in Warning or Offline state, sorted by urgency (Offline > Warning), then by duration. Columns: Device Name, Store, Status, Duration, Last Seen, Assigned To (if a remediation owner has been assigned via device detail).

**Empty state:** "All devices are healthy." (shown when Devices Requiring Attention table is empty)

## Interaction Flows

1. **Weekly fleet review:** ADM opens health analytics → fleet uptime = 97.2% → two stores below 95% → clicks their bars in the uptime chart → offline event log filtered to those stores → identifies recurring pattern (both stores have scanner offline events during evening shifts) → flags for store-level investigation
2. **LP correlation:** LP investigator cross-references device health with alert feed → "Terminal 5 at Store 3 had 3 offline events in the past 30 days, each lasting 15-20 minutes" → correlates with transaction gaps → opens case with device events as supporting evidence
3. **Pre-audit readiness:** ADM checks fleet health before a compliance audit → ensures no devices with firmware more than 2 versions behind → remediates 3 devices before audit date

## UX Callout

There is no equivalent to this screen in any retail POS platform. Device health data lives in IT management tools (Jamf, WSUS, Windows Device Manager), completely siloed from the transaction layer. The business value of this screen is the LP correlation it enables: an offline terminal during a "quiet" period is either a fault or a deliberate action. Canary brings device state into the same analytical surface as transaction data. An investigator doesn't need to pull two separate reports and manually correlate timestamps — the device health analytics and the chirp/alert feed exist in the same platform, built for the same investigator.

## Navigation Exits

- `/devices` — back to device fleet list
- `/devices/:id` — from attention table row

## Open Questions

None.
