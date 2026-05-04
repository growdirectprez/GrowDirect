---
screen: /settings/store/stations
title: POS Stations
role: ADM | MGR
wave: W2
origin: O
cp_equivalent: "Station setup (frmstations) — no device linkage, no operating-hours override, no LP context"
---

# POS Stations

**URL:** `/settings/store/stations`  
**Primary role:** ADM; MGR (read + annotate)  
**Entry points:** Settings → Store section → Stations; store locations detail → Stations link

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "POS Stations — [Store Name]", store selector, Add Station button | |
| Main content | Station table | |

## Key Elements

### Station Table
Columns: Station ID, Station Name, Store, Location Description (e.g., "Checkout Lane 1", "Greenhouse Register"), Device (linked device from /devices if configured), Status (Active / Inactive), Last Transaction (timestamp + transaction ID), LP Notes.

**Station ID:** Matches CP station/workstation code. Used in transaction records — every chirp and transaction is tagged with the station ID from which it originated. This is the join key between transaction data and the physical device.

**Device column:** If this station has been linked to a device record in `/devices`, the device name appears here with its current status indicator (green/red dot). Clicking navigates to the device detail. This is the bridge between the logical station (what CP knows) and the physical terminal (what the device manager knows).

**Last Transaction:** The timestamp and ID of the most recent transaction on this station. A station showing no transactions in the past 4 hours during business hours is either idle or offline — the station list surfaces this without requiring a chirp-feed query.

**LP Notes:** Free text field visible to MGR and LP. Used to annotate stations with operational context: "High-volume self-checkout — expected higher void rate", "Return-only station", "Training station — see training mode settings." LP investigators see these notes in the alert detail when an alert comes from this station.

### Add Station
ADM creates a new station record. Required: Station ID (must match CP station code), Store, Station Name. Optional: Location Description, Device link.

### Station Detail (inline)
Clicking a station shows an editable panel: all fields above plus the ability to link/unlink a device and edit LP notes.

**Inactive stations:** Status = Inactive excludes the station from live monitoring (no alerts, no chirps) but preserves historical transaction data for the station ID.

**Empty state:** "No stations configured for [Store]. Stations are created automatically when the adapter sync processes transactions from this store, or can be added manually."

## Interaction Flows

1. **Link terminal to station:** ADM adds new physical POS terminal to the devices list → opens stations → links device #D-0088 to Station ID #S-03 → station list now shows live device status alongside station record
2. **LP annotation:** LP investigator notices Station 4 at Store 2 generates disproportionate voids → opens stations → adds LP Note: "Cashier turnover location — elevated error rate expected; review monthly" → note appears in future alert details from this station
3. **Inactive station review:** ADM reviewing quarterly cleanup → sees Station 7 has Last Transaction = 6 months ago → confirms with Store MGR that the terminal was removed → sets status = Inactive

## UX Callout

In CP, stations are configuration records for the POS — which terminal is authorized to run which workflows. In Canary, stations are the LP's map of the store's transaction surface. The LP Notes field is the institutional memory that survives staff turnover: when a new LP investigator sees 12 void alerts from Station 4, the note tells them "this is a known high-turnover location with an elevated error rate" before they spend an hour investigating a non-event. Linking stations to device records closes the loop between logical transaction origin and physical hardware state — the combination that enables the device-offline / transaction-gap correlation described in the device detail brief.

## Navigation Exits

- `/settings/store/locations` — back to store locations
- `/devices/:id` — from device column link

## Open Questions

None.
