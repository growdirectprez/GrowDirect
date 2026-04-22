# 25 Seacove Site Plan

> **Type:** Reference Document (standalone, no PII, no running service)
> **Status:** Active — survey data transcribed, ~40% of values need verification
> **Date:** 2026-04-06 (ops upgrade 2026-04-13)

**Wiki:** [[Brain/wiki/seacove-project|Seacove Project]] · [[Brain/projects/Seacove|Seacove MOC]]

**Source:** IWS Surveying Boundary/Topographic Survey, Sheet 1 of 1
**Survey Date:** June 20, 2018
**Map Issue Date:** July 20, 2018
**Drafted By:** HP, EHC
**Project No:** 15-354

**Client:** Lyle, Angelique
**Address:** 25 Sea Cove Drive, Rancho Palos Verdes, California 90275
**Assessor's I.D.:** T575-009-012
**Legal Description:** Tract #14649, Lot 69
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[Canary/docs/profiles/ops/Tom|Tom]] · **Operator role:** [[Canary/docs/profiles/ops/Jeremy|Jeremy]]

## Purpose

Machine-readable transcription of the IWS survey for 25 Sea Cove Drive.
Code reads this document and generates a SketchUp model + LayOut drawing that
reproduces the survey exactly. If the generated output matches the original
PDF, the data is correct. No PII, no running service, no external integrations.

---

## 1. Survey Reference Data

### Basis of Bearings

S 40°23'00" E being a radial line to the centerline of Sea Cove Drive as per
Tract Map No. 14649, Map Book 345, Page 23-26, as filed in the records of the
County of Los Angeles.

### Benchmark

Assumed EL = 102.15 at Mag and Washer stamped RCE 28458, being a 15.09' ELY
PROD. of the NLY line of Lot 69, Tract #14649, MLB 345-23-26, as shown hereon.

### Scale

1" = 10' (1 inch equals 10 feet)

### Coordinate System (for model generation)

- **Origin (0, 0):** SW corner of Lot 69 (closest to Sea Cove Dr / south driveway intersection)
- **X axis:** East (positive)
- **Y axis:** North (positive)
- **Z axis:** Up (positive), elevation datum per benchmark above
- **Note:** Survey bearings must be converted to XY coordinates using the basis of bearings above. The bearing reference is a radial line to Sea Cove Drive centerline, not true north.

---

## 2. Property Boundary

Lot 69, Tract #14649. Irregular shape on cul-de-sac.

### Property Corners

Monuments are set at each corner. Survey notes describe monument type at each.

| Corner | Description | Monument |
|--------|-----------|----------|
| SW | Near Sea Cove Dr / south driveway | SET NAG & WASHER STAMPED "RCE 28458" ON S'LY PROD. OF W'LY P.L. | <!-- VERIFY exact position -->
| SE | Near Clipper Road intersection | SET NAG & WASHER STAMPED "RCE 28458" ON S'LY 23.0' S.E. OF P.C. ON RADIAL TO P.L. | <!-- VERIFY -->
| NE | Northeast, near Clipper Road | SET NAG & WASHER STAMPED "RCE 28458" 15.09' ELY PROD. OF NLY LINE (benchmark location) |
| NW | North, near Lot 70 boundary | <!-- VERIFY — monument description not clearly readable -->
| SSW | South, near Lot 68 boundary | SET NAG & WASHER STAMPED "RCE 28458" ON S'LY PROD. OF P.L. S.200' S.E. OF P.C. ON RADIAL TO P.L. | <!-- VERIFY -->

### Boundary Segments

Traced from survey. Bearings and distances along each property line segment.
<!-- NOTE: Many bearings are difficult to read at scan resolution. VERIFY all values against the original paper survey or a full-resolution scan. -->

| Segment | From | To | Bearing | Distance | Notes |
|---------|------|-----|---------|----------|-------|
| South (Sea Cove Dr frontage) | SW corner | SE corner | Curved — cul-de-sac arc | <!-- VERIFY radius and arc length --> | Along Sea Cove Drive right-of-way |
| East | SE corner | NE corner | <!-- VERIFY --> | <!-- VERIFY --> | Along Clipper Road |
| North | NE corner | NW corner | <!-- VERIFY --> | <!-- VERIFY --> | Shared with Lot 70 |
| West | NW corner | SW corner | <!-- VERIFY --> | <!-- VERIFY --> | Shared with Lot 67 |

### Adjacent Properties

| Direction | Property | Owner/Reference |
|-----------|---------|----------------|
| North | Tract #14649, Lot 70 | — |
| South/SW | Tract #14649, Lot 68 | — |
| West | Tract #14649, Lot 67 | — |
| East | Clipper Road right-of-way | Public |
| South | Sea Cove Drive right-of-way | Public (cul-de-sac) |

---

## 3. Spot Elevations

All elevations in feet, datum per benchmark (Assumed EL = 102.15).

Survey convention from legend:
- `XXX.X` = Dirt elevation
- `XXXX.X` = Finished surface elevation (F.S.)
- Annotations: TW = Top of Wall, TH = Top of Header(?), BW = Back of Walk,
  TC = Top of Curb, FF/FS = Finished Floor/Surface, GB = Grade Break,
  E/P = Edge of Pavement, TOBX = Top of Box

### House Elevations (Key Reference Points)

| Label | Elevation | Description |
|-------|-----------|-------------|
| FF | 100.00 | Finished Floor — existing single story house |
| Ridge | 108.82 | Ridge height |
| Eave | 106.82 | Eave height | <!-- VERIFY — partially obscured on scan -->
| Later(?) | — | <!-- VERIFY — annotation near house, partially readable --> |

### North Area (above house, toward Lot 70)

| Position (approx) | Elevation | Surface | Notes |
|-------------------|-----------|---------|-------|
| North driveway, NW area | 104.12 | Concrete | Near lot 70 boundary |
| North driveway, mid | 103.59 | Concrete | <!-- VERIFY --> |
| North driveway, NE | 102.41 | — | Near Clipper Rd |
| North of house, W side | 100.30 | — | Near 4" drain |
| North of house, center | 100.12 | — | <!-- VERIFY --> |
| Water meter area | 103.54 | — | Near NE, along Clipper Rd | <!-- VERIFY -->
| Near NE corner | 102.41 | — | <!-- VERIFY --> |

### East Area (toward Clipper Road)

| Position (approx) | Elevation | Surface | Notes |
|-------------------|-----------|---------|-------|
| Near Clipper Rd, mid-north | 101.85 | — | <!-- VERIFY --> |
| Clipper Rd curb area, NE | 100.85 | E/P | Street sign area |
| Near sewer manhole | — | — | Sewer Manhole Lot 69/71 |
| Clipper Rd, mid-east | 99.04 | — | <!-- VERIFY --> |
| Near SE, Clipper Rd | 98.25 | — | <!-- VERIFY --> |
| Street sign SE | 95.04 | E/P | <!-- VERIFY --> |
| Clipper Rd SE corner area | 96.30 | — | <!-- VERIFY --> |

### South Area (house frontage, toward Sea Cove Dr)

| Position (approx) | Elevation | Surface | Notes |
|-------------------|-----------|---------|-------|
| South of house, near center | 100.14 | — | |
| Concrete area S of house | 98.60 | Conc | |
| S of house, mid | 98.42 | — | |
| Palm tree area | 98.50 | — | Near 24" palm |
| South landscaping, mid | 98.10 | — | |
| South landscaping, east | 98.04 | — | |
| Near Sea Cove Dr, mid | 97.62 | — | |
| Near Sea Cove Dr, SE | 96.91 | — | <!-- VERIFY --> |
| Sea Cove Dr curb, south | 95.09 | — | <!-- VERIFY --> |
| Near SE, along curve | 95.40 | — | <!-- VERIFY --> |
| Conc. wall top, south | 98.21 | TW | <!-- VERIFY --> |
| Landscaping, near street | 97.34 | — | |

### West Area (toward Lot 67, pool/cabana area)

| Position (approx) | Elevation | Surface | Notes |
|-------------------|-----------|---------|-------|
| Cabana area | 98.63 | Conc | <!-- VERIFY --> |
| Pool deck, N side | 98.55 | Conc | <!-- VERIFY --> |
| Pool deck, S side | 98.50 | Conc | <!-- VERIFY --> |
| Near W property line, mid | 98.25 | — | <!-- VERIFY --> |
| W boundary, south area | 97.04 | — | <!-- VERIFY --> |
| Conc. pool area | 98.22 | Conc | |
| Near chain link fence, SW | 96.03 | — | <!-- VERIFY --> |
| Electric hydrant area | 98.25 | — | Elec. Hydr. |
| Near 4" drain, W side | 98.31 | — | <!-- VERIFY --> |
| W landscaping, mid | 98.04 | — | |
| W property line near lot 67 | 96.24 | — | <!-- VERIFY --> |
| Near SW corner | 95.54 | — | <!-- VERIFY --> |
| Car port area | 94.95 | — | <!-- VERIFY --> |
| S driveway, W end | 93.54 | Conc | <!-- VERIFY --> |

### South Driveway / SW Area

| Position (approx) | Elevation | Surface | Notes |
|-------------------|-----------|---------|-------|
| S driveway entrance | 93.40 | Conc | Near Lot 68 |
| S driveway mid | 94.17 | Conc | <!-- VERIFY --> |
| Hood gate area | 92.60 | — | Near flood gate F.L. 92.50 | <!-- VERIFY -->
| Near SW, Lot 68 boundary | 94.95 | — | <!-- VERIFY --> |

---

## 4. Existing Improvements

### House

- **Type:** Existing single story house
- **Finished Floor (FF):** 100.00
- **Ridge Elevation:** 108.82
- **Eave Elevation:** 106.82 <!-- VERIFY -->
- **Roof Material:** <!-- not noted on survey -->
- **Exterior:** <!-- not noted on survey -->

### Pool

- **Location:** West side of property, south of cabana
- **Material:** Concrete
- **Shape:** Rectangular <!-- VERIFY exact dimensions -->
- **Surrounding deck:** Concrete

### Cabana

- **Location:** West of pool, near west property line
- **Type:** Structure <!-- VERIFY dimensions and type -->

### Driveways

| Driveway | Location | Material | Notes |
|----------|---------|----------|-------|
| North | North side of house, runs E-W to Clipper Rd | Concrete | "CONCRETE DRIVEWAY" |
| South | SW side of property, curves from Sea Cove Dr | Concrete | "CONCRETE DRIVEWAY" |

### Hardscape (Non-Driveway Concrete)

| Area | Location | Material | Notes |
|------|---------|----------|-------|
| Patio/walkway S of house | Between house and Sea Cove Dr | Concrete | "CONC." labeled |
| Patio area E of house | Between house and Clipper Rd | Concrete | "CONC." labeled |
| Pool deck | Around pool | Concrete | |

### Walls and Fences

| Type | Location | Notes |
|------|---------|-------|
| Concrete wall (CONC. WALL) | Along portions of south boundary, near Sea Cove Dr | Multiple segments |
| Concrete wall | Along portions of east boundary, near Clipper Rd | |
| Concrete wall | Between property and north driveway | Near PH 20.4' | <!-- VERIFY -->
| Chain link fence | West boundary area, near Lot 67 | "CHAIN LINK FENCE" |
| Block line fence (B.L.F.?) | Near SW area | <!-- VERIFY --> |
| Car port fence | Near SW corner | <!-- VERIFY --> |

### Trees and Landscaping

| Type | Location | Size | Notes |
|------|---------|------|-------|
| Palm | S of house, near Sea Cove Dr | 24" | "24' PALM" |
| Landscaping | South strip between house and Sea Cove Dr | — | "LANDSCAPING" labeled |
| Landscaping | West side between pool and boundary | — | "LANDSCAPING" labeled |
| Landscaping | SW corner near Lot 68 | — | "LANDSCAPING" labeled |
| Landscaping | Along north side | — | Near Lot 70 boundary |

---

## 5. Utilities and Drainage

| Feature | Location | Notes |
|---------|---------|-------|
| 4" drain | North of house, west side | Runs toward Sea Cove Dr |
| 4" drain | West of pool area | <!-- VERIFY direction --> |
| 4" drain | South area, near house | |
| 4" drain | East of house | Near Clipper Rd |
| Sewer manhole | East side, near Clipper Rd | "SEWER MANHOLE LOT 69/71" |
| Electric hydrant | West side, near property line | "ELEC. HYDR." |
| Water meter | NE area, near Clipper Rd | "WATER MTR." <!-- VERIFY --> |

---

## 6. Roads

### Sea Cove Drive

- **Type:** Cul-de-sac (dead-end with turnaround)
- **Location:** Curves along south and southwest boundary of Lot 69
- **Surface:** Asphalt (assumed)
- **Curb:** Concrete curb present (TC elevations noted)
- **Width:** <!-- VERIFY — standard residential ~24' -->

### Clipper Road

- **Type:** Through-street, runs roughly NE-SW along east side
- **Location:** East of Lot 69
- **Surface:** Asphalt (assumed)
- **Curb:** Concrete curb present
- **Street signs:** Noted at intersection with Sea Cove Dr
- **Width:** <!-- VERIFY -->

---

## 7. Drawing Requirements

### Sheet Format

- **Sheet size:** To be determined (our own template — not IWS format)
- **Title block:** Custom GrowDirect/ARC format
- **Scale:** 1" = 10' (matching survey)
- **North arrow:** Required — compass rose per survey orientation
- **Legend:** Required — reproduce survey legend symbols

### Drawing Contents (must match survey)

The generated drawing must reproduce all of the following from the original:

1. **Property boundary** — closed polygon with bearing/distance labels on each segment
2. **Property corner monuments** — symbol + description at each corner
3. **Spot elevations** — all points with elevation labels
4. **Contour representation** — spot elevations positioned correctly
5. **Existing house footprint** — with FF, Ridge, Eave callouts
6. **All improvements** — pool, cabana, driveways, patios, walls, fences
7. **Landscaping areas** — boundary polygons with labels
8. **Trees** — symbol + size callout
9. **Utilities** — drain lines, sewer manhole, electrical, water
10. **Roads** — Sea Cove Dr cul-de-sac curve + Clipper Rd with curb lines
11. **Adjacent lots** — labeled (Lot 67, 68, 70)
12. **Survey notes** — basis of bearings, benchmark, scale

### Acceptance Criteria

Overlay the generated drawing on the original survey PDF. Every labeled
feature must appear in the correct position within 1' tolerance. Every
elevation must match exactly. Every improvement must be represented.

---

## 8. VERIFY Items

The following items could not be read with confidence from the PDF scan and
must be verified against the original paper survey or a higher-resolution scan:

1. **All property boundary bearings and distances** — most are not legible at scan resolution
2. **Exact property corner monument descriptions** — partially readable
3. **Eave elevation** — appears to be 106.82 but partially obscured
4. **Many spot elevations** — approximately 40% of values are marked VERIFY above
5. **Pool and cabana dimensions** — boundaries not dimensioned on survey
6. **Wall heights** — TW (top of wall) elevations partially readable
7. **Drain pipe routes** — general direction visible but exact paths unclear
8. **Cul-de-sac arc geometry** — radius and arc length not clearly readable
9. **Clipper Road right-of-way width** — not dimensioned
10. **Several improvement boundaries** — exact corners of driveways, patios

### Resolution Strategy

These items should be resolved by:
- Reading the original paper survey at IWS Surveying's office
- Requesting a digital DWG/DXF file from IWS (if available)
- Field measurement for features still existing
- Cross-referencing with the Tract Map (Map Book 345, Pages 23-26)

---

## Dependencies

| Dependency | Type | Required |
|------------|------|----------|
| SketchUp Pro | 3D model generation | Yes (local install) |
| LayOut | 2D construction document generation | Yes (part of SketchUp Pro) |
| IWS Survey PDF | Source document | Yes (on file) |
| Tract Map (Map Book 345, pp 23-26) | Boundary verification | For VERIFY items |

---

## Data Flow & PII Map

No PII. This document contains only property survey data (elevations, bearings,
improvement locations). Owner name appears as the survey client identifier
(public record — recorded with LA County).

---

## Operations

This is a standalone reference document consumed by SketchUp model-building
scripts. No running service, no health checks, no deployment.

**File location:** `docs/sdds/arc/seacove-site-plan.md`
**SketchUp models:** `Seacove/` directory (separate from platform infra)

---

## Code Review Findings

### P2 — Post-Launch

| # | Finding | Recommended Fix | Linear |
|---|---------|----------------|--------|
| 1 | ~40% of elevation values marked VERIFY — model accuracy limited until resolved | Schedule IWS office visit or request DWG file | — |
| 2 | All boundary bearings/distances unverified — model cannot reproduce closed polygon | Critical for any permit-ready drawings; resolution required | — |

---

## Production Readiness Checklist

N/A — reference document for SketchUp pipeline. Not a deployed service.

---

*25 Seacove Site Plan — GrowDirect Inc.*
