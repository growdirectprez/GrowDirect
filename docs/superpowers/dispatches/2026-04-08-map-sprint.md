# Map Sprint Dispatch — 2026-04-08

**Issues:** GRO-485, GRO-486, GRO-369, GRO-403
**Scope:** Fix Leaflet init, QA Declaration 101 layers, overlay cleanup, SVG map polish
**Strategy:** Disable broken overlays, ship only verified layers

---

## Sequence & Dependencies

```
GRO-485 (Leaflet fix)         ← BLOCKER — map page blank, no tiles/parcels
  ├──→ GRO-486 (Decl 101 QA)  ← 6 layers built, need visual verification
  └──→ GRO-369 (overlay cleanup) ← disable ~12 misaligned, rebuild 4 derived

GRO-403 (SVG polish)          ← INDEPENDENT — separate community SVG map
```

GRO-403 runs in parallel with the Leaflet track since it touches `cove/community/`
and `static/img/community-tract-map.svg` — no shared files with the `/map` module.

---

## GRO-485 — Leaflet Not Initializing

**Priority:** High (blocker)
**Status:** Backlog → In Progress

The map page at `/map` loads UI chrome (sidebar, timeline, hierarchy panel, search)
but Leaflet never renders tiles or parcels. The canvas is blank.

**Investigation targets:**
- Browser console JS errors during `_initMap()` / Alpine `init()`
- `manifest.layers | tojson` output — bad JSON crashes Alpine before Leaflet runs
- Recent changes to `cove/map/templates/map/index.html` or `cove/map/services.py`
- Verify `L` (Leaflet global) is defined before `parcelMap()` runs
- Check `static/js/leaflet.js` exists and is served

**Acceptance:** Tiles render, 81 parcels render, no console errors, layer toggles work.

---

## GRO-486 — Declaration 101 Layer QA

**Priority:** Medium (blocked by 485)
**Status:** Backlog

Six GeoJSON files exist in `cove/map/data/layers/` and are registered in
`manifest.json` under "PV Corp Era" > "Declaration No. 101 (1929)". All
`defaultOn: false`.

**QA checklist:**
- Toggle each layer on — verify render
- Parcel 4 (335 ac) wraps around Parcels 2, 3, 7
- Parcels 1 & 5 (coastal) align with PV Drive South corridor
- Compare shared boundaries with Filiorum layers — should overlap
- Flag Parcels 1 & 5 curve errors (large closure — 1,542 ft and 2,695 ft)

**Note:** Parcel 6 not built yet (illegible distance from microfilm).

---

## GRO-369 — Overlay Cleanup (Scoped Down)

**Priority:** High
**Status:** In Progress
**Scope change:** "Disable broken, ship correct" — not full rebuild

16 overlay layers in `cove/map/data/layers/` are positioned ~1km east of actual
parcels. Root cause: boundary parser POB coordinates don't match LA County GIS
coordinate system.

**Keep (derive from existing parcel data):**
- Tract 14649 boundary — union/convex hull of 81 parcels from `wpbca-parcels.geojson`
- 0 Clipper Road — pull geometry from LA County GIS for APN 7573-006-024
- Declaration No. One (1949) — union of all 81 lots
- Declaration One-A (Lots 1-5) — union of lots 1-5

**Remove/disable:** All other misaligned overlays (~12 layers) — easements, coastal
zone, landslide moratorium, R-22, Smith-Anderson deed. Move to `data/layers/disabled/`
or remove from manifest.

**Follow-up issue (not this sprint):** Source official RPV/CCC GIS data for
regulatory and easement layers.

---

## GRO-403 — SVG Community Map Polish

**Priority:** Medium
**Status:** Backlog → In Progress (parallel track)

The SVG tract map (`static/img/community-tract-map.svg` and
`cove/community/templates/community/tract-map.svg`) is v1 — functional but needs
visual polish.

**Items:**
1. Street labels on road centerlines (currently at lot centroid median) — font 9-10px
2. Badge alignment per block — snap to consistent line per street block
3. Coastline curvature — extend viewport or use park polygon southern edge
4. Verify all 5 tract polygons visible (not clipped by viewport)
5. Wire SVG into community page template — replace Leaflet with inline SVG + Alpine interactivity

**Files:**
- `static/img/community-tract-map.svg` — the SVG source
- `cove/community/templates/community/tract-map.svg` — template copy
- `cove/community/templates/community/index.html` — community page (currently Leaflet-based)
- `cove/community/routes.py` — community blueprint

---

## Risks

- GRO-485 may be a simple JS error or may reveal deeper template/data issues
- GRO-369 overlay cleanup may reveal layers that other features depend on (check before removing)
- SVG map (403) may need road centerline geometry data that doesn't exist yet

---

*Dispatch by Cove builder | 2026-04-08*
