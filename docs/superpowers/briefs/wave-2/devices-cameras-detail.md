---
screen: /devices/cameras/:id
title: Camera Detail
role: MGR | ADM | LP
wave: W2
origin: N
cp_equivalent: "None"
---

# Camera Detail

**URL:** `/devices/cameras/:id`  
**Primary role:** MGR; ADM; LP  
**Entry points:** Camera fleet list row

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Camera name, status, store, location | |
| Main content | Camera info panel + event log | |
| Clip viewer | Video clip retrieval (TBD) | Placeholder — feed/clip model undefined |

## Key Elements

Camera detail follows the same pattern as `/devices/:id` — identity panel, connection status, event log. The distinguishing element is the clip viewer: when an LP alert references a camera event, the investigator should be able to retrieve the relevant clip from this screen.

Motion event log and alert-correlation panel are TBD pending camera integration spec.

**Empty state:** Not applicable — camera record exists before reaching this screen.

## Navigation Exits

- `/devices/cameras` — back to camera fleet

## Open Questions

Deferred: camera/sensor integration spec required. Clip retrieval API, retention policy, alert-correlation event linking, and live-feed access controls are all undefined. Stub only until spec is finalized.
