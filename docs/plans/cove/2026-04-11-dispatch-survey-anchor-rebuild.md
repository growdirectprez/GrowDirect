# DISPATCH: Survey Anchor Point Rebuild — DXF Registration + Monument Positioning

**Created:** 2026-04-11 (Claude Code session — Tasks 1-2 complete, Task 3 in progress)
**Linear:** GRO-493 (parent)
**Spec:** `Cove/docs/plans/2026-04-11-survey-anchor-rebuild-design.md`
**Plan:** `Cove/docs/plans/2026-04-11-survey-anchor-rebuild-plan.md`
**Branch:** create new from main

---

## What's Done

### Task 1: Field Book Transcriptions (COMPLETE)

8 WPBCA intersection field book pages transcribed to structured markdown:
- `docs/archive/transcriptions/survey-field-books/RDFB-0117-002.md` (1952)
- `docs/archive/transcriptions/survey-field-books/RDFB-0117-020.md` (1964)
- `docs/archive/transcriptions/survey-field-books/RDFB-0117-021.md` (1964)
- `docs/archive/transcriptions/survey-field-books/RDFB-0117-159.md` (1972)
- `docs/archive/transcriptions/survey-field-books/RDFB-0117-171.md` (1972)
- `docs/archive/transcriptions/survey-field-books/PWFB-0117-159A.md` (1987)
- `docs/archive/transcriptions/survey-field-books/PWFB-0117-159B.md` (1998)
- `docs/archive/transcriptions/survey-field-books/PWFB-0117-381.md` (2012)

Key findings from transcriptions:
- P.I. #11 bearing **163°59'45"** confirmed across 3 surveys (1952-1964-1972)
- PVD South curve: **R=1996.65, Δ=16°00'20-24"** consistent across all surveys
- Clipper Road curve: **R=500.00, Δ=13°09'45"**
- Sea Cove Drive curve: **R=350.10, Δ=29°27'27.5"**
- B.C. monument: 63 years of documentation (1949-2012)
- Station discrepancy: B.C. at 159+22.28 (1952) vs 159+23.87 (2012) — 1.59 ft

### Task 2: Coordinate System Ties (PARTIALLY COMPLETE)

Read CEFB 2291 Zone 7 tie pages (155-156) and Wayfarer's Chapel control pages
(131-141). Finding: **Zone 7 ties don't have inline coordinates** — they reference
external SPH control monuments (D-7, C-8, G-6) whose published coordinates are
in other databases. The full Zone 7 transform chain requires looking up those
SPH coordinates externally.

**Pivot:** Instead of the Zone 7 path, use the **25 Sea Cove site survey** as the
anchor bridge. The IWS 2018 boundary survey and the 2007 easement DXF both have
monument positions on Sea Cove Drive that can be matched to satellite imagery.

### Also Done (from earlier in the same session)

- Lot 106 full boundary walked (15 legs, 0.69% closure, 1.53 acres)
- Coates→Brown sub-parcel walked (exact closure, 0.11 acres) + database ingestion
- 11 archive file renames (Word→Wong, Niblock→Brown, LACA corrections)
- All committed and merged to main

---

## What Needs Doing

### Task 3: Register DXF to WGS84

**Source:** `Brain/raw/inbox/07094EAS.dxf` — 2007 easement survey CAD drawing (Denn Engineers, RCE 30826)

**Coordinate system:** Local feet (origin 0,0, range X: 0-2038, Y: -155 to 1496)

**Approach:** Match 2+ lot corner vertices between the DXF local coordinates and
the assessor GIS WGS84 coordinates to compute a Helmert transform.

**DXF lot corner vertices extracted (PROP_LINES layer):**

| DXF (local ft) | Description | Match to |
|-----------------|-------------|----------|
| (1024.56, 649.30) | Lot corner | Assessor GIS vertex for lot on Sea Cove |
| (1042.91, 561.19) | Lot corner | " |
| (900.45, 531.23) | Lot corner | " |
| (1065.33, 453.51) | Lot corner | " |
| (1101.37, 368.30) | Lot corner (near ocean) | " |
| (1380.30, 412.85) | Lot corner | " |
| (1308.64, 848.33) | Lot corner | " |
| (1084.85, 741.31) | Lot corner | " |

**DXF text annotations give bearings and APNs:**
- APNs: 7573-007-020, 021, 030, 031, 034, 035, 036
- Bearings: N 22°55'21" W, N 67°04'28" E, N 16°46'49" W, etc.
- Sea Cove Drive curve: L=500.00', R=350.500' (matches field book R=350.10)

**Steps:**
1. Load assessor GIS parcels for APNs 7573-007-020 through 036
2. Match lot corners between DXF and GIS (by APN + bearing + distance)
3. Compute Helmert transform: DXF local → WGS84
4. Validate: RMS residual < 5 ft
5. Apply transform to all DXF vertices

**Also available:**
- `Cove/docs/archive/originals/property/2018-06-20-IWS-Boundary-Survey-25-SeaCove.pdf`
  — IWS 2018 boundary survey showing RCE 28458 monuments on Sea Cove Drive
  — Basis of bearings: S 40°23'00" E radial to Sea Cove Dr centerline per Tract 14649
- Existing `cove/map/data/layers/lot-69-25-seacove-surveyed.geojson` — may already
  have georeferenced coordinates from this survey
- `cove/map/data/layers/2007-easement-survey-lots1-3.geojson` — existing layer from
  the same DXF (check if already registered)

### Task 4: Build Monument Catalog + Anchor Points GeoJSON

Using the registered DXF coordinates + field book transcriptions:

1. Walk from Sea Cove Drive (DXF) along the field book distances to PVD South
   intersection monuments (B.C., P.I. #11, E.C., P.O.S.T.)
2. Convert each monument to WGS84 using the DXF→WGS84 transform + field book
   distance chain
3. Build enriched `anchor-points.geojson` with:
   - Survey-sourced pins (red, `source_class: field-survey`)
   - Existing assessor pins (gray, `source_class: assessor-gis`)
   - Full provenance chains per monument
4. Quantify the systematic offset between the two sources

### Task 5: Re-Anchor Lot 106 Polygon

Using the new survey-sourced anchor points:
1. Identify POB anchor (NW corner Lot 74 → should correspond to a monument
   near the Clipper/PVD South intersection)
2. Re-georeference both Lot 106 layers with 2+ survey tie points
3. Visual verify on map: POB on pin, leg 01 correct direction

### Task 6: Write Playbook + Wiki

- `docs/archive/wiki/PLAYBOOK-FIELDBOOK-TO-ANCHOR.md`
- `docs/archive/wiki/11-mapping-engineering/survey-monuments.md`
- Update `coordinate-reference.md` with transform parameters

### Task 7: Final Verification

- All layers render correctly on map
- Anchor points visible as independent layer
- Offset between sources quantified
- Commit + merge

---

## Files to Read First

1. This dispatch
2. `Cove/docs/plans/2026-04-11-survey-anchor-rebuild-design.md` (full spec)
3. `Cove/docs/plans/2026-04-11-survey-anchor-rebuild-plan.md` (implementation plan)
4. `Cove/docs/archive/transcriptions/survey-field-books/RDFB-0117-002.md` (key transcription)
5. `Cove/docs/archive/wiki/11-mapping-engineering/coordinate-reference.md`
6. `Cove/docs/archive/wiki/11-mapping-engineering/snap-rules.md`

## Key Files

| File | What |
|------|------|
| `Brain/raw/inbox/07094EAS.dxf` | 2007 easement survey CAD — the anchor bridge |
| `Brain/raw/inbox/RDFB0117-2.pdf` | 1952 intersection survey — key field drawing |
| `cove/map/data/layers/anchor-points.geojson` | Current anchor points (assessor-derived, offset) |
| `cove/map/data/layers/lot-69-25-seacove-surveyed.geojson` | Existing lot 69 layer (check if registered) |
| `scripts/layers/metes_to_geojson.py` | Walk + georeference library |
