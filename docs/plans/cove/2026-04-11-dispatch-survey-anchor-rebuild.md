# DISPATCH: Survey Anchor Point Rebuild — DXF Registration + Monument Positioning

**Created:** 2026-04-11 (Claude Code session — Tasks 1-5 complete, Task 8 added)
**Updated:** 2026-04-11 (end of session — key pivot)
**Linear:** GRO-493 (parent)
**Spec:** `Cove/docs/plans/2026-04-11-survey-anchor-rebuild-design.md`
**Plan:** `Cove/docs/plans/2026-04-11-survey-anchor-rebuild-plan.md`
**Branch:** main (committed directly)

---

## KEY PIVOT — Use Assessor Boundaries, Not Deed Walks

**The session proved that deed-walk polygons don't work for visual display.**
The Lot 106 deed walk has a 10 ft closure error and produces a polygon that
doesn't align with roads on the map. The cadastral landbase (EPSG:2229) is
225 ft offset from the OSM base tiles.

**What DOES align with the map:** the assessor parcel polygons (the blue outlines).
These are the boundaries users see and trust.

**New approach for Lot 106 visualization:**
Instead of walking the deed description, use the assessor parcels that were
carved from Lot 106. Each subdivision transaction created new APNs. Group them
by transaction to show the Lot 106 subdivision history:

```
Lot 106 (original, ~48 acres)
  ├── Tract 14649 (1949) — 81 lots: 7573-009-*, 7573-010-*, etc.
  ├── Tract 23434 (1957) — Arrowroot/Barkentine: 7573-005-*
  ├── Tract 32977 (1980) → Tract 43725 (1986) — Wong reversion: 7573-006-008 thru 015
  ├── Fire Station (7573-006-900) — county parcel
  ├── Remainder strips (7573-006-017, 018) — PV Corp never-conveyed
  └── Coastal parcels (7573-007-*) — Sea Cove lots 1-3, easement parcels
```

Each group becomes a toggleable layer showing boundaries FROM THE ASSESSOR DATA
(which snaps to the map). The deed walk / survey data goes in the provenance
metadata, not the polygon geometry.

---

## What's Done (this session)

### Task 1: Field Book Transcriptions (COMPLETE — prior session)
8 WPBCA intersection field book pages transcribed.

### Task 2: Coordinate System Ties (PARTIALLY COMPLETE — prior session)
Zone 7 ties require external SPH lookup. Pivot to DXF bridge.

### Task 3: Register DXF to WGS84 (COMPLETE)
- 07094EAS.dxf → WGS84 via Helmert (4 tie points, RMS 0.7 ft)
- Script: `scripts/layers/register_dxf_2007_easement.py`
- Output: `2007-easement-dxf-registered.geojson`

### Task 4: Monument Catalog (COMPLETE — but needs re-anchoring)
- 15 anchor points in `anchor-points.geojson`
- 8 assessor-GIS + 6 cadastral-landbase + 1 field-survey
- **Problem:** cadastral-landbase points are 225 ft offset from base map
- **Fix needed:** drop cadastral positions, use assessor parcel vertices as
  monument positions (or accept they're reference-only, not map-visible)

### Task 5: Re-Anchor Lot 106 (NEEDS REDO — see pivot above)
- Deed walk produces a polygon that doesn't match the map
- The polygon is visible but offset from roads
- **Next session should use assessor parcels instead**

### Task 6: Playbook + Wiki (COMPLETE)
- `PLAYBOOK-FIELDBOOK-TO-ANCHOR.md`
- `survey-monuments.md`
- `coordinate-reference.md` updated

### New Documents Ingested
- `CEFB2190.pdf` — 222 pages, Sea Cove Dr field book (1959). UNPROCESSED.
- `RS220-057-2.pdf` — Record of Survey (2008). Transcribed.
- `IM009157.dgn` + `.zip` — LA County Cadastral Landbase GDB. Extracted.
- `AM1-001.pdf`, `AM1-012.pdf` — Assessor maps.
- `TR1063-091-2.pdf`, `TR0950-014-2.pdf` — Tract maps (dupes of archive).

---

## What Needs Doing (next session)

### Task 8: Build Lot 106 Subdivision History Layers (NEW — replaces Task 5)

Use the assessor parcel polygons grouped by subdivision transaction:

1. **Query RPV parcels GeoJSON** for all APNs in the Lot 106 area:
   - 7573-005-* (Tract 23434)
   - 7573-006-* (remainder strips, fire station, Wong reversion)
   - 7573-007-* (Sea Cove lots 1-3, easement parcels)
   - 7573-008-* (Sea Cove lots, east side)
   - 7573-009-* (Clipper/Barkentine lots)
   - 7573-010-* (Packet Road lots)

2. **Group by transaction:**
   - Tract 14649 (1949) — WPBCA subdivision
   - Tract 23434 (1957) — Arrowroot/Barkentine
   - Tract 32977→43725 (1980/1986) — Wong subdivision/reversion
   - County parcels (fire station, road R/W)
   - Remainder strips (PV Corp)

3. **Build one GeoJSON per group** using the assessor polygon data directly —
   no deed walks, no Helmert transforms. These snap to the base map.

4. **Add to manifest** as toggleable layers under "Remainder Strips & Chain of Title"

5. **Compute the Lot 106 outer boundary** as the union of all sub-parcels.
   This gives the de facto Lot 106 boundary from assessor data.

### Task 9: Fix Anchor Points Layer

The "Historical Anchor Points" name is confusing. Options:
- Rename to "Survey Control Points"
- Split into two layers: "Assessor Reference Points" + "Survey Monuments"
- Or remove the cadastral-sourced points (they don't add value if they
  don't align with the map)

### Task 10: Rename in Manifest

Update `manifest.json`:
- "Historical Anchor Points" → "Survey Control Points" (or remove)
- Add new subdivision history layers

---

## Files to Read First (next session)

1. This dispatch (updated)
2. `Cove/gis-downloads/rpv-parcels.geojson` — 21,120 RPV parcels with assessor polygons
3. `Cove/cove/map/data/layers/manifest.json` — current layer configuration
4. `Cove/cove/map/templates/map/index.html` — map rendering code

## Key Commits

- `ae516e8` — feat(map): survey anchor rebuild (DXF, monuments, Lot 106)
- `4dab978` — fix(map): re-anchor to assessor parcel frame

## What the User Wants to See

**The subdivision history of Lot 106 — each transaction that carved a piece off,
shown as actual assessor boundaries that snap to the map.** Not deed walks.
Not survey monuments floating in space. Actual parcel boundaries.
