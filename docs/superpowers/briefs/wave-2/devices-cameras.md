---
screen: /devices/cameras
title: Camera Fleet
role: MGR | ADM | LP
wave: W2
origin: N
cp_equivalent: "None"
---

# Camera Fleet

**URL:** `/devices/cameras`  
**Primary role:** MGR; ADM; LP  
**Entry points:** Devices section → Cameras tab

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Cameras", store selector | |
| Main content | Camera table | Camera name, store, location, status, last event |
| Action bar | Add Camera (ADM only) | |

## Key Elements

Camera fleet list view follows the same pattern as `/devices` — name, store, location, status (Online / Offline / Warning), last event timestamp. Each camera row links to `/devices/cameras/:id`.

Integration with LP alert flow is TBD pending camera integration spec: camera event correlation with alert timestamps (e.g., motion detected at register at time of void alert) is the target behavior.

**Empty state:** "No cameras registered. Contact your administrator to configure camera integration."

## Navigation Exits

- `/devices/cameras/:id` — camera detail

## Open Questions

Deferred: camera/sensor integration spec required. Video feed access model (live vs clip retrieval), storage integration (NVR vs cloud), and alert-correlation event schema are undefined. Stub only until spec is finalized.
