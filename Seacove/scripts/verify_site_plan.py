#!/usr/bin/env python3
"""Verify site plan geometry against survey data.

Runs WITHOUT SketchUp — pure math. Computes distances, areas, positions
from the coordinates in the Ruby scripts and compares against known
survey reference values.

Usage:
    python3 scripts/verify_site_plan.py
"""
import math
import sys


# =========================================================================
# CURRENT MODEL COORDINATES — must match 01_site_pass4.rb exactly
# =========================================================================

LOT_BOUNDARY = [
    [0.0, 0.0],        # SW corner
    [10.0, -3.5],
    [20.0, -7.5],
    [28.0, -11.0],
    [36.0, -13.5],
    [44.0, -14.5],     # near deepest arc point
    [52.0, -13.5],
    [60.0, -10.0],
    [68.0, -5.0],
    [78.0, 3.0],        # SE corner
    [80.0, 20.0],
    [82.5, 40.0],
    [85.0, 60.0],
    [87.5, 80.0],
    [89.5, 100.0],
    [92.0, 120.0],      # NE corner
    [61.0, 121.5],
    [30.0, 123.0],
    [0.0, 124.0],       # NW corner
]

CORNERS = {
    "SW": (0.0, 0.0),
    "SE": (78.0, 3.0),
    "NE": (92.0, 120.0),
    "NW": (0.0, 124.0),
}

HOUSE_X, HOUSE_Y = 23.0, 29.0
LIVING_W, LIVING_D = 22.5, 22.833
BEDROOM_W, BEDROOM_D = 19.167, 44.0
HOUSE_TOTAL_W = 41.667

POOL = {"x": 5.0, "y": 31.0, "w": 14.0, "d": 28.0}
CABANA = {"x": 1.0, "y": 47.0, "w": 10.0, "d": 14.0}

FF = 100.00
RIDGE = 108.82
EAVE = 106.82

# Foundation constants (from pass 4)
FOOTING_WIDTH_IN = 12.0
FOOTING_DEPTH_IN = 18.0
SLAB_THICKNESS_IN = 4.0
INTERIOR_FOOTING_DEPTH_IN = 12.0

# Perimeter footing path — L-shaped house outline (centerlines)
PERIMETER_FOOTING = [
    [HOUSE_X, HOUSE_Y],                                      # house SW
    [HOUSE_X + HOUSE_TOTAL_W, HOUSE_Y],                      # house SE
    [HOUSE_X + HOUSE_TOTAL_W, HOUSE_Y + BEDROOM_D],          # bedroom NE
    [HOUSE_X + LIVING_W, HOUSE_Y + BEDROOM_D],               # bedroom NW (inside corner)
    [HOUSE_X + LIVING_W, HOUSE_Y + LIVING_D],                # living NE (inside corner)
    [HOUSE_X, HOUSE_Y + LIVING_D],                            # living NW
]

# Interior footings
INTERIOR_FOOTINGS = [
    {"from": [HOUSE_X, HOUSE_Y + 11.0],
     "to": [HOUSE_X + LIVING_W, HOUSE_Y + 11.0],
     "label": "Kitchen/Living bearing wall"},
    {"from": [HOUSE_X + LIVING_W + 9.5, HOUSE_Y],
     "to": [HOUSE_X + LIVING_W + 9.5, HOUSE_Y + BEDROOM_D],
     "label": "Hallway bearing wall"},
    {"from": [HOUSE_X + LIVING_W, HOUSE_Y + LIVING_D],
     "to": [HOUSE_X + HOUSE_TOTAL_W, HOUSE_Y + LIVING_D],
     "label": "Bedroom/service divider"},
]

FIREPLACE = {"x": HOUSE_X + 8.0, "y": HOUSE_Y + 5.0, "w": 5.0, "d": 3.0}


# =========================================================================
# SURVEY REFERENCE VALUES (from IWS survey, what we're trying to match)
# =========================================================================
SURVEY_REF = {
    # Property line lengths
    "west_boundary_length": {"value": 124.0, "tolerance": 3.0, "confidence": "MED",
                             "note": "NW to SW, shared with Lot 67"},
    "north_boundary_length": {"value": 92.0, "tolerance": 3.0, "confidence": "MED",
                              "note": "NW to NE, shared with Lot 70"},
    "east_boundary_length": {"value": 118.0, "tolerance": 3.0, "confidence": "MED",
                             "note": "NE to SE, along Clipper Rd"},
    "south_chord_length": {"value": 78.0, "tolerance": 3.0, "confidence": "MED",
                           "note": "SW to SE straight line (actual is arc)"},

    # South boundary arc length
    "south_arc_length": {"value": 95.0, "tolerance": 10.0, "confidence": "LOW",
                         "note": "Total length along cul-de-sac arc from SW to SE"},

    # Lot area
    "lot_area_sqft": {"value": 10500, "tolerance": 1000, "confidence": "LOW",
                      "note": "Rough estimate — typical RPV lot is 8000-15000 sqft"},

    # House position
    "house_to_west_pl": {"value": 23.0, "tolerance": 3.0, "confidence": "MED"},
    "house_to_east_pl": {"value": 17.0, "tolerance": 5.0, "confidence": "MED",
                         "note": "East PL varies due to Clipper Rd angle"},
    "house_to_south_pl": {"value": 29.0, "tolerance": 3.0, "confidence": "MED",
                          "note": "To straight SW-SE baseline, not arc"},
    "house_to_north_pl": {"value": 51.0, "tolerance": 5.0, "confidence": "LOW"},

    # House dimensions (from 1958 Rucker plans — exact)
    "living_wing_width": {"value": 22.5, "tolerance": 0.1, "confidence": "HIGH"},
    "living_wing_depth": {"value": 22.833, "tolerance": 0.1, "confidence": "HIGH"},
    "bedroom_wing_width": {"value": 19.167, "tolerance": 0.1, "confidence": "HIGH"},
    "bedroom_wing_depth": {"value": 44.0, "tolerance": 0.1, "confidence": "HIGH"},
    "house_total_width": {"value": 41.667, "tolerance": 0.1, "confidence": "HIGH",
                          "note": "Living + Bedroom wing width"},

    # Elevations (from survey — exact)
    "ff_elevation": {"value": 100.00, "tolerance": 0.01, "confidence": "HIGH"},
    "ridge_elevation": {"value": 108.82, "tolerance": 0.01, "confidence": "HIGH"},
    "eave_elevation": {"value": 106.82, "tolerance": 0.5, "confidence": "MED"},
    "ridge_minus_ff": {"value": 8.82, "tolerance": 0.01, "confidence": "HIGH",
                       "note": "Roof height above finished floor"},

    # Cul-de-sac arc
    "arc_depth": {"value": 15.0, "tolerance": 3.0, "confidence": "MED",
                  "note": "Deepest point below SW-SE line"},

    # East boundary angle
    "east_boundary_bearing_deg": {"value": 6.0, "tolerance": 3.0, "confidence": "MED",
                                  "note": "Degrees east of true north (Clipper angles)"},

    # Pool
    "pool_to_west_pl": {"value": 5.0, "tolerance": 3.0, "confidence": "LOW"},
    "pool_to_house_gap": {"value": 4.0, "tolerance": 3.0, "confidence": "LOW",
                          "note": "Gap between pool east edge and house west edge"},
    "pool_south_edge_y": {"value": 31.0, "tolerance": 5.0, "confidence": "LOW",
                          "note": "Should be near house south edge Y"},
    "pool_north_edge_y": {"value": 59.0, "tolerance": 5.0, "confidence": "LOW",
                          "note": "Should be within house N-S extent"},

    # Foundation checks
    "perimeter_footing_length": {"value": 171.3, "tolerance": 5.0, "confidence": "HIGH",
                                 "note": "Total linear feet of perimeter footing (L-shape perimeter)"},
    "slab_area_living": {"value": 513.7, "tolerance": 10.0, "confidence": "HIGH",
                         "note": "Living wing slab area: 22.5 x 22.833"},
    "slab_area_bedroom": {"value": 843.3, "tolerance": 10.0, "confidence": "HIGH",
                          "note": "Bedroom wing slab area: 19.167 x 44.0"},
    "slab_area_total": {"value": 1357.1, "tolerance": 15.0, "confidence": "HIGH",
                        "note": "Total slab area (living + bedroom wings)"},
    "fireplace_inside_house": {"value": 1.0, "tolerance": 0.01, "confidence": "HIGH",
                               "note": "1.0 = yes, fireplace foundation is inside house footprint"},
    "interior_footings_inside_house": {"value": 1.0, "tolerance": 0.01, "confidence": "HIGH",
                                       "note": "1.0 = all interior footings within house boundary"},
    "hallway_footing_length": {"value": 44.0, "tolerance": 1.0, "confidence": "HIGH",
                               "note": "Hallway bearing wall runs full bedroom wing depth"},
}


# =========================================================================
# GEOMETRY HELPERS
# =========================================================================

def dist(p1, p2):
    """Distance between two 2D points."""
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def polyline_length(points, start_idx, end_idx):
    """Total length along polyline from start to end index."""
    total = 0.0
    for i in range(start_idx, end_idx):
        total += dist(points[i], points[i + 1])
    return total


def closed_polyline_length(points):
    """Total length of a closed polyline (last point connects to first)."""
    total = 0.0
    n = len(points)
    for i in range(n):
        total += dist(points[i], points[(i + 1) % n])
    return total


def polygon_area(points):
    """Signed area of polygon using shoelace formula."""
    n = len(points)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += points[i][0] * points[j][1]
        area -= points[j][0] * points[i][1]
    return abs(area) / 2.0


def point_in_polygon(px, py, polygon):
    """Ray-casting point-in-polygon test."""
    n = len(polygon)
    inside = False
    j = n - 1
    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        if ((yi > py) != (yj > py)) and (px < (xj - xi) * (py - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


def interpolate_boundary_x(boundary, y_target, start_idx, end_idx):
    """Linear interpolation of X at a given Y along boundary segment range."""
    for i in range(start_idx, end_idx):
        y1, y2 = boundary[i][1], boundary[i+1][1]
        if (y1 <= y_target <= y2) or (y2 <= y_target <= y1):
            if abs(y2 - y1) < 0.001:
                return boundary[i][0]
            t = (y_target - y1) / (y2 - y1)
            return boundary[i][0] + t * (boundary[i+1][0] - boundary[i][0])
    return None


# =========================================================================
# COMPUTE MODEL MEASUREMENTS
# =========================================================================

def compute_measurements():
    """Compute all measurements from current model coordinates."""
    m = {}

    # Property line lengths
    sw_idx, se_idx, ne_idx, nw_idx = 0, 9, 15, 18

    # West boundary: NW → SW (straight line)
    m["west_boundary_length"] = dist(LOT_BOUNDARY[nw_idx], LOT_BOUNDARY[sw_idx])

    # North boundary: NE → NW (polyline through 15→16→17→18)
    m["north_boundary_length"] = polyline_length(LOT_BOUNDARY, ne_idx, nw_idx)

    # East boundary: SE → NE (polyline through 9→10→...→15)
    m["east_boundary_length"] = polyline_length(LOT_BOUNDARY, se_idx, ne_idx)

    # South chord: SW to SE straight line
    m["south_chord_length"] = dist(LOT_BOUNDARY[sw_idx], LOT_BOUNDARY[se_idx])

    # Lot area
    m["lot_area_sqft"] = polygon_area(LOT_BOUNDARY)

    # House position relative to property lines
    m["house_to_west_pl"] = HOUSE_X
    m["house_to_south_pl"] = HOUSE_Y

    # House to east PL — interpolate east boundary at house midpoint Y
    house_mid_y = HOUSE_Y + BEDROOM_D / 2.0
    house_east_edge = HOUSE_X + HOUSE_TOTAL_W
    east_pl_x = interpolate_boundary_x(LOT_BOUNDARY, house_mid_y, se_idx, ne_idx)
    if east_pl_x:
        m["house_to_east_pl"] = east_pl_x - house_east_edge
    else:
        m["house_to_east_pl"] = None

    # House to north PL
    house_north_edge = HOUSE_Y + BEDROOM_D
    m["house_to_north_pl"] = CORNERS["NW"][1] - house_north_edge

    # House dimensions
    m["living_wing_width"] = LIVING_W
    m["living_wing_depth"] = LIVING_D
    m["bedroom_wing_width"] = BEDROOM_W
    m["bedroom_wing_depth"] = BEDROOM_D
    m["house_total_width"] = HOUSE_TOTAL_W

    # Elevations
    m["ff_elevation"] = FF
    m["ridge_elevation"] = RIDGE
    m["eave_elevation"] = EAVE
    m["ridge_minus_ff"] = RIDGE - FF

    # Cul-de-sac arc depth
    sw, se = LOT_BOUNDARY[sw_idx], LOT_BOUNDARY[se_idx]
    max_depth = 0.0
    for pt in LOT_BOUNDARY[sw_idx:se_idx+1]:
        if abs(se[0] - sw[0]) > 0.001:
            t = (pt[0] - sw[0]) / (se[0] - sw[0])
            line_y = sw[1] + t * (se[1] - sw[1])
            depth = line_y - pt[1]
            max_depth = max(max_depth, depth)
    m["arc_depth"] = max_depth

    # Pool position
    m["pool_to_west_pl"] = POOL["x"]
    m["pool_to_house_gap"] = HOUSE_X - (POOL["x"] + POOL["w"])
    m["pool_south_edge_y"] = POOL["y"]
    m["pool_north_edge_y"] = POOL["y"] + POOL["d"]

    # South boundary arc length
    m["south_arc_length"] = polyline_length(LOT_BOUNDARY, sw_idx, se_idx)

    # East boundary bearing angle
    se_pt = LOT_BOUNDARY[se_idx]
    ne_pt = LOT_BOUNDARY[ne_idx]
    dx = ne_pt[0] - se_pt[0]
    dy = ne_pt[1] - se_pt[1]
    bearing_rad = math.atan2(dx, dy)
    m["east_boundary_bearing_deg"] = math.degrees(bearing_rad)

    # --- FOUNDATION CHECKS ---

    # Perimeter footing total linear footage
    m["perimeter_footing_length"] = closed_polyline_length(PERIMETER_FOOTING)

    # Slab areas
    m["slab_area_living"] = LIVING_W * LIVING_D
    m["slab_area_bedroom"] = BEDROOM_W * BEDROOM_D
    m["slab_area_total"] = m["slab_area_living"] + m["slab_area_bedroom"]

    # Fireplace inside house check
    fp_cx = FIREPLACE["x"] + FIREPLACE["w"] / 2.0
    fp_cy = FIREPLACE["y"] + FIREPLACE["d"] / 2.0
    # Simple check: fireplace center within living wing rectangle
    in_living = (HOUSE_X <= fp_cx <= HOUSE_X + LIVING_W and
                 HOUSE_Y <= fp_cy <= HOUSE_Y + LIVING_D)
    m["fireplace_inside_house"] = 1.0 if in_living else 0.0

    # Interior footings all inside house boundary
    # Build L-shaped house polygon for containment test
    house_poly = [
        [HOUSE_X, HOUSE_Y],
        [HOUSE_X + HOUSE_TOTAL_W, HOUSE_Y],
        [HOUSE_X + HOUSE_TOTAL_W, HOUSE_Y + BEDROOM_D],
        [HOUSE_X + LIVING_W, HOUSE_Y + BEDROOM_D],
        [HOUSE_X + LIVING_W, HOUSE_Y + LIVING_D],
        [HOUSE_X, HOUSE_Y + LIVING_D],
    ]
    all_inside = True
    for ftg in INTERIOR_FOOTINGS:
        f, t = ftg["from"], ftg["to"]
        mid = [(f[0] + t[0]) / 2.0, (f[1] + t[1]) / 2.0]
        if not point_in_polygon(mid[0], mid[1], house_poly):
            all_inside = False
            break
    m["interior_footings_inside_house"] = 1.0 if all_inside else 0.0

    # Hallway footing length
    hall = INTERIOR_FOOTINGS[1]  # hallway bearing wall
    m["hallway_footing_length"] = dist(hall["from"], hall["to"])

    return m


# =========================================================================
# COMPARE AND REPORT
# =========================================================================

def verify():
    """Compare model measurements against survey references."""
    measurements = compute_measurements()

    print("=" * 72)
    print("SITE PLAN VERIFICATION — Pass 4")
    print("Comparing model coordinates against survey reference values")
    print("=" * 72)
    print()

    pass_count = 0
    warn_count = 0
    fail_count = 0
    skip_count = 0

    for key, ref in SURVEY_REF.items():
        model_val = measurements.get(key)
        ref_val = ref["value"]
        tol = ref["tolerance"]
        conf = ref["confidence"]
        note = ref.get("note", "")

        if model_val is None:
            print(f"  SKIP  {key}: could not compute")
            skip_count += 1
            continue

        diff = abs(model_val - ref_val)
        pct = (diff / ref_val * 100) if ref_val != 0 else 0

        if diff <= tol:
            status = "PASS"
            pass_count += 1
        elif diff <= tol * 2:
            status = "WARN"
            warn_count += 1
        else:
            status = "FAIL"
            fail_count += 1

        indicator = {"PASS": "  OK  ", "WARN": " WARN ", "FAIL": "**FAIL**"}[status]
        print(f"  {indicator} {key}")
        print(f"         model={model_val:.2f}  survey={ref_val:.2f}  "
              f"diff={diff:.2f} ({pct:.1f}%)  tol=±{tol:.1f}  [{conf}]")
        if note:
            print(f"         {note}")
        print()

    print("-" * 72)
    print(f"Results: {pass_count} PASS, {warn_count} WARN, {fail_count} FAIL, {skip_count} SKIP")
    print()

    if fail_count > 0 or warn_count > 0:
        print("ISSUES TO FIX:")
        for key, ref in SURVEY_REF.items():
            model_val = measurements.get(key)
            if model_val is None:
                continue
            diff = abs(model_val - ref["value"])
            if diff > ref["tolerance"]:
                direction = "too large" if model_val > ref["value"] else "too small"
                print(f"  - {key}: {direction} by {diff:.1f}' "
                      f"(model={model_val:.1f}, survey={ref['value']:.1f})")
        print()

    return fail_count == 0 and warn_count == 0


if __name__ == "__main__":
    ok = verify()
    sys.exit(0 if ok else 1)
