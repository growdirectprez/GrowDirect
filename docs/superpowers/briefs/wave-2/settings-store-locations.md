---
screen: /settings/store/locations
title: Store Locations
role: ADM
wave: W2
origin: O
cp_equivalent: "Store setup (frmstores) — no geo-coordinates, no operating hours, no mapping integration"
---

# Store Locations

**URL:** `/settings/store/locations`  
**Primary role:** ADM  
**Entry points:** Settings → Store section → Locations

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Store Locations", Add Store button | |
| Main content | Store table | |

## Key Elements

### Store Table
Columns: Store ID, Store Name, Address, City/State, Phone, Status (Active / Inactive), Stations (count), Last Sync (CP sync timestamp for this store's data).

**Last Sync column:** Shows when the Counterpoint adapter last successfully pulled data for this store. If a store's last sync is hours behind all others, it indicates a CP connection issue specific to that store's data path.

### Store Detail (inline drawer or page)
Clicking a store row opens a detail panel or navigates to an edit form:
- **Store Name:** Display name used throughout Canary
- **Store ID:** Matches CP store code (used for adapter mapping)
- **Address fields:** Street, city, state, ZIP
- **Phone / Email:** Contact info for the location
- **Geo-coordinates:** Lat/lon for map integrations (Distribution Recommendations module uses this for proximity scoring)
- **Operating Hours:** Per-day open/close times. Used by alert routing (suppress overnight alerts when store is closed) and by the flash report (define the operating day for hourly breakdowns)
- **Status:** Active / Inactive. Inactive stores are excluded from most reports and alert feeds but their historical data is preserved.
- **Time Zone:** For stores spanning multiple time zones — transaction timestamps are stored in UTC, displayed in store local time.

### Add Store
ADM creates a new store record. Required fields: Store Name, Store ID (must match CP store code), Address, Status = Active. After creation, the adapter sync is configured in admin → config.

**Empty state:** System should always have at least one location; empty state indicates misconfiguration.

## Interaction Flows

1. **New store onboarding:** ADM adds a new store location → enters store ID matching CP store code → sets operating hours → activates → adapter sync begins pulling data for the new location
2. **Store relocation:** MGR notifies ADM of new address → ADM updates address and geo-coordinates → Distribution Recommendations module recalculates proximity to other stores
3. **Inactive store archiving:** Store closes → ADM sets status = Inactive → store excluded from active views but historical transaction and LP data preserved

## UX Callout

CP's store setup (`frmstores`) is a basic record — name, address, and an internal code. Canary's store locations record includes operating hours and geo-coordinates because the platform uses both. Operating hours determine when alerts are noise (a 3am alert for an unmanned store is likely a false positive) vs signal (the same alert at 11am is actionable). Geo-coordinates feed the Distribution Recommendations module's proximity scoring — which stores can receive transfers within acceptable lead time given geography. These aren't cosmetic additions; they're inputs to the intelligence layer.

## Navigation Exits

- `/settings/store/stations` — stations for the selected store
- `/admin/config` — adapter sync configuration per store

## Open Questions

None.
