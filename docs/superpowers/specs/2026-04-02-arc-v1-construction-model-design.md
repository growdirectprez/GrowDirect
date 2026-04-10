# ARC v1 — Construction-Sequence Model Generation

**Date:** 2026-04-02
**Status:** Draft
**Author:** Jeffe + ALX brainstorm session
**Builds on:** `docs/superpowers/specs/2026-04-02-arc-ai-draftsman-design.md` (v0 spec)

---

## 1. What This Changes

ARC v0 generates a basic 3D model — solid wall boxes, posts, beams, roof slabs.
It works, but it looks like an abstract diagram, not a building.

ARC v1 generates a **construction-accurate, 1:1 scale model** organized by
construction phase. The model is built the way a contractor builds a house:
site → foundation → framing → roof. Each phase is a Tag Folder in SketchUp.
Each element is a named, lockable component.

**Scope shift from v0:** The v0 spec defined v1 as LayOut document generation.
That scope is now deferred to v2. v1 focuses on construction-accurate modeling
with survey data, foundation modeling, incremental build, and round-trip sync.
LayOut viewports and drawing set generation come after the model is right.

**Purpose:** Produce a model accurate enough to generate permit-ready
construction drawings at 1/4" = 1'-0" scale via SketchUp LayOut.

**Starting point:** The 2018 IWS boundary/topographic survey of 25 Sea Cove
Drive — professional surveyed coordinates, not traced from 1958 hand drawings.

---

## 2. Core Design Principles

### Build Like a House

The generation sequence mirrors real construction:

1. **Site** — lot boundary, topo, roads, existing improvements
2. **Foundation** — continuous footings, interior footings, slab, stem walls
3. **Framing/Walls** — wall assemblies (one component per wall section)
4. **Structure** — posts, beams, headers
5. **Framing/Roof** — rafters, ridge beams
6. **Roofing** — finished roof surface
7. **Openings** — doors and windows placed in framed walls

Each phase can be toggled on/off to see the house at any stage of construction.

### Component Granularity: One Wall Assembly

The model element is **one wall section as a complete assembly** — not
individual studs, but not a monolithic box either. A wall component contains
its full construction detail (framing visible in section cuts). You build
wall by wall: generate it, verify against the blueprint, lock it, move on.

Components are **not** individual lumber members. That's too granular. You can:
- Toggle any wall's visibility via its tag
- Select and inspect a wall component
- Swap a wall out for the remodel version
- Section-cut through it to see internal structure

### Lock After Verify

Once a space is verified against the blueprints, its components get locked
in SketchUp (right-click → Lock). Locked geometry can't be accidentally
edited or moved. This prevents drift as you build out the rest of the model.

### Round-Trip Sync

Changes made in SketchUp flow back to the spatial model:

```
Spatial Model (JSON)
    ↓ arc generate
Ruby Scripts (.rb)
    ↓ load in SketchUp
SketchUp Model
    ↓ manual adjustments
SketchUp Model (modified)
    ↓ export script (Ruby)
Updated Spatial Model (JSON)
    ↓ arc generate
Updated Ruby Scripts
```

An export Ruby script runs inside SketchUp, walks all named components,
reads their current position/dimensions, and writes back to JSON. This
requires consistent naming conventions on every component — the name is
the key that maps SketchUp geometry back to the spatial model.

**Naming convention:** `{phase}-{type}-{id}`
- `site-lot-boundary`
- `fnd-footing-P01` (perimeter footing 1)
- `fnd-slab-main`
- `wall-ext-N01` (exterior wall north 1)
- `wall-int-K01` (interior wall kitchen 1)
- `str-post-A1` (structural post at grid A1)
- `str-beam-ridge-living`
- `roof-plane-living`

---

## 3. SketchUp Organization

### Tag Folder / Tag Hierarchy

```
Site/
    Lot Boundary
    Topography
    Roads
    Driveway
    Pool
    Landscaping
    Fences & Walls
Foundation/
    Perimeter Footings
    Interior Footings
    Slab
    Stem Walls
    Fireplace Foundation
Walls/
    Exterior
    Interior
    (individual wall tags as needed for complex areas)
Structure/
    Posts
    Beams
    Headers
Roof/
    Framing
    Surface
Openings/
    Doors
    Windows
```

Tags control **visibility only** (standard SketchUp practice). Geometry
isolation comes from Groups and Components.

### Component vs Group Strategy

- **Components** for elements that repeat or might be swapped: wall
  assemblies, door/window units, structural posts of the same size
- **Groups** for one-off geometry: lot boundary, slab, custom shapes
- Every piece of geometry gets a **name** matching the naming convention

### Scenes (Drawing Views)

Pre-configured scenes for construction drawing output:

| Scene | View | Scale | Shows | Hides |
|-------|------|-------|-------|-------|
| Site Plan | Top-down ortho | 1/8" = 1'-0" | Site/* | Everything else |
| Foundation Plan | Top-down ortho | 1/4" = 1'-0" | Foundation/*, Site/Lot Boundary | Walls, Roof |
| Floor Plan | Top-down ortho + section | 1/4" = 1'-0" | Walls/*, Openings/* | Roof, Site (except lot) |
| Roof Plan | Top-down ortho | 1/4" = 1'-0" | Roof/* | Walls, Foundation |
| Elevations (N/S/E/W) | Side ortho | 1/4" = 1'-0" | All except Site | Topo, Roads |
| Sections | Side ortho + section plane | 1/4" = 1'-0" | All | — |
| 3D Overview | Perspective | — | All | — |

---

## 4. Spatial Model Changes (Schema Version 2)

The v0 spatial model (schema_version 1) lacks site data, foundation data,
and construction phase metadata. Schema version 2 adds:

### New: Site Model

Populated from the 2018 IWS survey.

```json
{
  "site": {
    "survey": {
      "source": "IWS Surveying, June 20, 2018",
      "benchmark": { "elevation": 102.15, "description": "Mag and washer at NE corner Lot 69" },
      "scale": "1 inch = 10 feet"
    },
    "lot": {
      "tract": "14649",
      "lot_number": "69",
      "boundary": [
        { "point": [0, 0], "elevation": null, "description": "SW corner" },
        { "point": [85, 0], "elevation": null, "bearing": "S 40°23'00\" E" }
      ]
    },
    "topography": {
      "spot_elevations": [
        { "position": [40, 30], "elevation": 100.00, "label": "FF existing house" },
        { "position": [45, 35], "elevation": 108.82, "label": "Ridge" }
      ],
      "contour_interval": null
    },
    "improvements": {
      "house": {
        "description": "Existing single story house",
        "ff_elevation": 100.00,
        "ridge_elevation": 108.82,
        "eave_elevation": 106.82
      },
      "pool": { "boundary": [], "material": "concrete" },
      "cabana": { "boundary": [] },
      "driveways": [
        { "label": "North driveway", "boundary": [], "material": "concrete" },
        { "label": "South driveway", "boundary": [], "material": "concrete" }
      ],
      "walls_and_fences": [
        { "type": "concrete_wall", "from": [], "to": [], "height": null },
        { "type": "chain_link_fence", "from": [], "to": [], "height": null }
      ]
    },
    "roads": [
      { "label": "Sea Cove Drive", "type": "cul-de-sac", "centerline": [] },
      { "label": "Clipper Road", "type": "through-street", "centerline": [] }
    ],
    "utilities": {
      "sewer_manhole": { "position": [], "label": "Sewer Manhole Lot 69/71" },
      "drains": []
    }
  }
}
```

### New: Foundation Model

```json
{
  "foundation": {
    "type": "slab_on_grade",
    "slab": {
      "thickness_in": 4,
      "boundary": [],
      "elevation": null
    },
    "footings": [
      {
        "id": "fnd-footing-P01",
        "type": "continuous",
        "path": [[0, 0], [28, 0]],
        "width_in": 12,
        "depth_in": 18,
        "rebar": "2 #4 cont.",
        "description": "South perimeter footing"
      }
    ],
    "stem_walls": [
      {
        "id": "fnd-stem-S01",
        "footing_ref": "fnd-footing-P01",
        "height_in": 6,
        "thickness_in": 6
      }
    ],
    "fireplace_foundation": {
      "boundary": [],
      "depth_in": 24,
      "description": "Fireplace mass foundation"
    }
  }
}
```

### Updated: Wall Model

Walls gain a richer assembly description:

```json
{
  "id": "wall-ext-N01",
  "from": [0, 44], "to": [22.5, 44],
  "type": "exterior",
  "thickness_in": 6,
  "assembly": {
    "studs": "2x4 @ 16\" o.c.",
    "sheathing": "1/2\" plywood",
    "exterior_finish": "stucco",
    "interior_finish": "1/2\" drywall"
  },
  "openings": []
}
```

The `assembly` field is informational — it documents what the wall contains
but the generated component renders the wall as a solid at the correct
thickness. Section detail comes from the assembly description, not from
modeling every stud.

The construction phase is determined by the Tag Folder assignment (walls are
always in `Walls/`), not by a field on the wall — no redundant metadata.

### Schema Migration

- `schema_version` bumps to `2`
- Loader reads both v1 and v2; v1 models get these defaults:
  - `site`: `null` (no survey data)
  - `foundation`: `null` (not modeled)
  - `wall.assembly`: `null` (no detail)
  - Interior fixtures: deferred (v0 `fixtures` arrays are preserved but not generated)
- `validate` command checks the new fields

---

## 5. Generator Changes

### Script Output Structure

v1 generates more scripts, organized by construction phase:

```
00_helpers.rb          — utility functions (unchanged from v0)
01_components.rb       — reusable component definitions (door, window, post types)
02_site.rb             — lot boundary, topo, roads, improvements from survey
03_foundation.rb       — footings, slab, stem walls
04_walls.rb            — wall assemblies with openings
05_structure.rb        — posts, beams, headers
06_roof.rb             — roof planes
07_scenes.rb           — camera positions, tag visibility presets
08_export.rb           — round-trip: read model back to JSON
```

**Changes from v0:** v0 produced 4 files (00, 04, 05, 06). v1 adds site,
foundation, components, scenes, and export. Interior fixtures (`07_interior.rb`
from the v0 spec's aspirational list) are deferred — not needed for existing
conditions modeling.

`01_components.rb` defines SketchUp ComponentDefinitions for repeated elements
(door types, window types, post sizes). Phase scripts instantiate these
definitions rather than building geometry inline. This enables the swap
workflow — replace a 3068 door component with a 6068 for the remodel.

### Incremental Build Support

Each phase script supports both `build_all` and `build_next` patterns:

```ruby
module SeacoveFoundation
  # Build everything at once
  def self.build_all
    build_perimeter_footings
    build_interior_footings
    build_slab
    build_stem_walls
    lock_all
  end

  # Build one element at a time for verification
  def self.build_next
    # Tracks state in a class variable
    @queue ||= [:perimeter_footings, :interior_footings, :slab, :stem_walls]
    item = @queue.shift
    return puts "All foundation elements built." unless item
    send("build_#{item}")
    puts "Built: #{item}. #{@queue.length} remaining. Call .build_next for next."
  end

  # Lock all components in this phase
  def self.lock_all
    # Find all groups/components tagged under Foundation/
    model = Sketchup.active_model
    model.entities.each do |e|
      next unless e.respond_to?(:layer)
      next unless e.layer&.folder&.name == "Foundation"
      e.locked = true
    end
    puts "Foundation locked."
  end
end
```

### Export Script (Round-Trip)

`08_export.rb` reads the current SketchUp model and writes a **geometry-only**
JSON file. This is NOT a complete spatial model — it contains only the fields
that SketchUp can provide (positions, dimensions, names). A separate
`arc merge` CLI command overlays this geometry export onto the existing
spatial model, updating positions and dimensions while preserving metadata
fields (assembly descriptions, rebar specs, source references, confidence
scores) that only exist in the spatial model.

**Field ownership:**

| Field type | Owned by | Example |
|-----------|---------|---------|
| Geometry (positions, dimensions) | SketchUp export | `from`, `to`, `boundary`, `path` |
| Metadata (descriptions, specs) | Spatial model JSON | `assembly`, `rebar`, `description`, `sources` |
| Identity (names, IDs) | Both (must match) | `id`, component `name` |

The export script recursively walks all entities (including those nested
inside groups and components) to find named elements:

```ruby
module SeacoveExport
  def self.to_json(output_path)
    model = Sketchup.active_model
    data = { "schema_version" => 2, "project" => "seacove", "geometry" => {} }

    walk_entities(model.entities, data["geometry"])

    File.write(output_path, JSON.pretty_generate(data))
    puts "Geometry exported to #{output_path}"
    puts "Run 'arc merge seacove' to update the spatial model."
  end

  def self.walk_entities(entities, geo)
    entities.each do |entity|
      next unless entity.respond_to?(:name) && entity.name && !entity.name.empty?

      case entity.name
      when /^wall-/
        geo["walls"] ||= []
        geo["walls"] << extract_wall_geometry(entity)
      when /^fnd-/
        geo["foundation"] ||= []
        geo["foundation"] << extract_foundation_geometry(entity)
      when /^str-/
        geo["structure"] ||= []
        geo["structure"] << extract_structure_geometry(entity)
      when /^site-/
        geo["site"] ||= []
        geo["site"] << extract_site_geometry(entity)
      end

      # Recurse into groups and components
      if entity.respond_to?(:entities)
        walk_entities(entity.entities, geo)
      end
    end
  end
end
```

---

## 6. Seacove First Pass: Site Survey

The first thing generated is the site plan from the 2018 IWS survey.

### What Gets Modeled

From the survey sheet:

| Element | Source Data | Model Component |
|---------|-----------|----------------|
| Lot boundary | Bearings + distances | Closed polygon at surveyed positions |
| Spot elevations | ~60+ survey points | 3D points (TIN surface deferred to v2) |
| Existing house footprint | Outline on survey | Flat polygon at FF=100.00 |
| Pool + cabana | Outlines on survey | Flat polygons |
| Concrete driveways | Outlines on survey | Flat polygons |
| Sea Cove Drive | Road edge lines | Polygon with curb |
| Clipper Road | Road edge lines | Polygon with curb |
| Concrete walls | Line segments | Extruded walls |
| Chain link fences | Line segments | Line + height |
| Sewer manhole | Point | Cylinder |
| Trees / landscaping | Areas on survey | Boundary polygons |

### Coordinate System

The IWS survey uses bearings and distances (e.g., "S 40°23'00\" E"). These
are converted to XY coordinates manually before data entry into the spatial
model. The conversion uses the SW corner of the lot as origin (0, 0) and
the survey's bearing reference (radial line to Sea Cove Drive centerline)
to establish the X/Y axes. Spot elevations use the survey benchmark
(EL = 102.15 at mag and washer, NE corner Lot 69).

### Workflow

1. Convert survey bearings/distances to XY coordinates (manual calculation)
2. Hand-enter coordinates into `spatial_model.json` (site section)
3. `arc generate seacove` produces `02_site.rb`
4. Load in SketchUp — verify lot shape, road alignment, house position
5. Adjust in SketchUp if needed
6. Run `08_export.rb` to sync changes back to JSON
7. Lock the site layer
8. Proceed to foundation (from 1958 foundation plan blueprint)

### Why Start Here

- Survey is the most accurate document (professional surveyor, 2018)
- Establishes the coordinate system and benchmark for everything else
- Lot boundary, setbacks, and topo drive all permit decisions
- House footprint from survey validates against 1958 blueprints

---

## 7. Blueprint Parsing Pipeline (Deferred)

The iterative crop-and-extract pipeline for automating dimension reading
from PDF scans is **deferred** until the construction model generation is
proven. For v1, dimensions are hand-entered from the blueprints.

When implemented, the pipeline will:
- Take a blueprint page and crop it into component regions
- Run vision AI on each crop individually (not whole-page scans)
- Human verifies each extracted dimension before it enters the model
- Confidence scores flag uncertain readings

This is a separate design spec and implementation cycle.

---

## 8. Technology Changes from v0

| Concern | v0 | v1 |
|---------|----|----|
| Site data | Approximate, hand-coded in Ruby | Surveyed coordinates in spatial model |
| Foundation | Not modeled | Full foundation model (footings, slab, stem walls) |
| Wall detail | Solid boxes | Assembly components with metadata |
| Script count | 4 files | 8 files (by construction phase) |
| Build mode | All-at-once only | Incremental (build_next) + all-at-once |
| Round-trip | None | Export script reads SketchUp back to JSON |
| Tag structure | Flat tags | Tag Folders by construction phase |
| Component naming | Ad-hoc | `{phase}-{type}-{id}` convention |
| Locking | None | Lock after verification |
| Schema version | 1 | 2 (backward-compatible reader) |

---

## 9. What ARC v1 Does NOT Do

Everything from v0 "does not" list, plus:

- No automated blueprint extraction (deferred — hand-enter for now)
- No individual stud-level framing detail (wall assemblies are components)
- No material takeoffs (future — component counts enable this)
- No structural calculations (geometry only)
- No topographic surface generation from spot elevations (points only for v1)
- No automatic scene/viewport setup in LayOut (that's v2)

---

## 10. Done Criteria

### v1 Complete When

- Site plan generates from survey data and renders correctly in SketchUp
- Foundation generates from 1958 blueprint data (hand-entered)
- Walls generate as named, lockable components organized by Tag Folders
- Incremental build works (build_next adds one element at a time)
- Round-trip export script reads SketchUp model back to JSON
- Scene presets configured for Floor Plan, Elevations, Site Plan views
- Seacove model matches existing house well enough to overlay on survey
- Model at 1/4" = 1'-0" scale in LayOut viewport is legible
