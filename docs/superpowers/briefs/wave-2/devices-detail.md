---
screen: /devices/:id
title: Device Detail
role: MGR | ADM
wave: W2
origin: N
cp_equivalent: "None — CP has no device management surface"
---

# Device Detail

**URL:** `/devices/:id`  
**Primary role:** MGR; ADM  
**Entry points:** Device list row

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Device name, status badge, store, device type | Breadcrumb back to /devices |
| Top section | Device identity + connection info | |
| Main content | Status history + event log | |
| Diagnostic panel | Live diagnostic readings (device-type-specific) | |
| Action bar | Test Connection, Restart Device, Decommission | MGR: Test + Restart only; ADM: all |

## Key Elements

### Device Identity Panel
Fields: Device Name (editable by ADM), Serial Number, Model, Firmware Version, MAC Address, IP Address, Store, Location within store (e.g., "Checkout Lane 4", "Receiving Dock"). Location is free text — used by staff to physically locate the device.

### Connection Status
Last Seen timestamp (exact). Current status. Heartbeat interval (how often the device checks in). Online duration (how long continuously online). For Offline devices: time since last heartbeat.

### Status History
Timeline chart showing Online / Offline / Warning state over the past 7 days. Periods of offline state shown as gaps. Useful for identifying intermittent connectivity issues vs hard failures (a device that drops once a day at the same time vs a device that went offline and never came back have very different patterns).

### Event Log
Time-ordered log of device events: heartbeat received, firmware update applied, configuration change, calibration event (for scales), restart triggered, status changes. Each event has a timestamp and source (system / user / device).

### Diagnostic Panel (device-type-specific)
- **POS Terminal:** Last transaction ID + timestamp, terminal session status, queued transaction count (should be 0), CPU/memory if available.
- **Scale:** Last weight event timestamp, calibration status, last calibration date, drift metric.
- **Scanner:** Last scan timestamp, scan success rate (% of scan events that resolved to a valid item).
- **Receipt Printer:** Last print timestamp, paper level (Low / OK / Out), error state.

### Actions
- **Test Connection:** Sends a ping to the device and displays latency result. "Device responded in 42ms." Useful for quick connectivity confirmation without waiting for the next heartbeat.
- **Restart Device:** Sends a restart command (requires device to support remote restart). Confirmation dialog: "Send restart command to [Device Name]?" Logged in event log.
- **Decommission:** ADM only. Marks device as Decommissioned; removes from active fleet views. Confirmation required. Logs decommission event with user and timestamp.

**Empty state:** Not applicable — device exists before reaching this screen.

## Interaction Flows

1. **Diagnose an offline terminal:** MGR opens device detail for Terminal 3 → status = Offline, Last Seen = 1h 23m ago → status history shows this is the 3rd offline event this week (same time window) → MGR escalates to IT with event log export
2. **Scale calibration check:** MGR opens produce scale detail → drift metric = 0.3g above threshold → calibration date = 22 days ago (threshold = 14 days) → MGR schedules recalibration and adds note to event log
3. **Decommission replaced terminal:** ADM receives report of replaced hardware → opens old terminal's detail → clicks Decommission → confirms → device removed from active views; event log preserved

## UX Callout

The status history timeline is the key operational element on this screen. A single offline event might be a power blip; a recurring offline pattern at the same time every day might be a deliberate disconnection to avoid transaction capture during a specific window. LP investigators looking at a time-correlation between "no alerts from Store 2, Terminal 4" and "high-discount transactions from Store 2" need to know whether Terminal 4 was online or offline during that period. The event log provides this without requiring LP to call IT for device logs.

## Navigation Exits

- `/devices` — back to device list

## Open Questions

None.
