---
screen: /devices/sensors/:id
title: Sensor Detail
role: MGR | ADM
wave: W2
origin: N
cp_equivalent: "None"
---

# Sensor Detail

**URL:** `/devices/sensors/:id`  
**Primary role:** MGR; ADM  
**Entry points:** Sensor fleet list row

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Sensor name, status, store, location, sensor type | |
| Main content | Sensor identity panel + reading history | |
| Alert threshold panel | Configurable thresholds per sensor type (TBD) | |

## Key Elements

Sensor detail follows the same pattern as `/devices/:id` — identity panel, connection status, event log. The distinguishing element is the reading history chart: temperature sensors show a time-series of readings, door sensors show open/close events, motion sensors show detection events.

Threshold configuration (e.g., "alert if temperature > 90°F in cold storage area") and LP event correlation (door sensor open event during closed hours) are TBD pending sensor integration spec.

**Empty state:** Not applicable — sensor record exists before reaching this screen.

## Navigation Exits

- `/devices/sensors` — back to sensor fleet

## Open Questions

Deferred: camera/sensor integration spec required. Reading schema per sensor type, threshold configuration model, alert routing for sensor events, and LP correlation rules are all undefined. Stub only until spec is finalized.
