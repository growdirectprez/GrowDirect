---
screen: /devices/sensors
title: Sensor Fleet
role: MGR | ADM
wave: W2
origin: N
cp_equivalent: "None"
---

# Sensor Fleet

**URL:** `/devices/sensors`  
**Primary role:** MGR; ADM  
**Entry points:** Devices section → Sensors tab

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Sensors", store selector | |
| Main content | Sensor table | Sensor name, store, location, type, status, last reading |
| Action bar | Add Sensor (ADM only) | |

## Key Elements

Sensor fleet list view follows the same pattern as `/devices` — name, store, location, sensor type (Temperature / Humidity / Door / Motion / EAS), status (Online / Offline / Warning), last reading, last event timestamp. Each sensor row links to `/devices/sensors/:id`.

Sensor types relevant to retail operations: temperature sensors for plant/cold storage areas, door/entry sensors for access monitoring, EAS (electronic article surveillance) integration for loss prevention correlation.

**Empty state:** "No sensors registered. Contact your administrator to configure sensor integration."

## Navigation Exits

- `/devices/sensors/:id` — sensor detail

## Open Questions

Deferred: camera/sensor integration spec required. Sensor event schema, EAS integration model, temperature threshold alerting, and LP correlation rules for door/motion sensors are undefined. Stub only until spec is finalized.
