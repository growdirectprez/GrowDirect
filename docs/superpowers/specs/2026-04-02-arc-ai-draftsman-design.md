# ARC — AI Draftsman Design Spec

**Date:** 2026-04-02
**Status:** Draft
**Author:** Jeffe + ALX brainstorm session

---

## 1. What ARC Is

ARC is an AI draftsman — a conversational pipeline tool that reads architectural
blueprints, photos, and descriptions, builds an internal spatial model of the
structure, and generates SketchUp Ruby scripts and LayOut documents that produce
accurate 3D models and permit-ready 2D construction drawing sets.

ARC is **not** a Flask web app. It has no auth, no multi-tenancy, no browser UI.
It is a tool you pick up and use directly on your own projects.

**Target user:** Jeffe, on real projects (Seacove remodel first). Productization
comes later, after the pipeline proves accurate.

**Platform:** macOS desktop, SketchUp Pro subscription, SketchUp 2024+.

---

## 2. Isolation & Guardrails

**Hard guardrail:** ARC never exposes itself as an MCP server. No other app,
agent, or builder can call into ARC. It is not discoverable on the platform.

- No MCP endpoint registration
- No memory bus participation
- No Linear/GRO dispatch
- No factory pipeline stages
- Directory boundary: everything stays inside `GrowDirect/ARC/`

**What ARC CAN use:**
- Ollama for vision/embeddings (read-only consumer via localhost:11434)
- PostgreSQL if persistence is needed later (own `arc` database)
- Valkey if caching becomes useful
- Local filesystem for all input/output

---

## 3. Pipeline Architecture

Five stages, each independent. Output of one stage is input to the next via files.

```
Ingest → Extract → Model → Design → Generate
```

### Stage 1: Ingest

Accept raw inputs and normalize them for processing.

| Input type | Format | Handler |
|-----------|--------|---------|
| Scanned blueprints | PDF, PNG, JPG, TIFF | `ingest/blueprint_reader.py` |
| Site photos | PNG, JPG | `ingest/photo_reader.py` |
| Natural language descriptions | Text (CLI or file) | `ingest/description.py` |

Output: normalized images/text in the project's `inputs/` directory.

**SketchUp model import (.skp):** Deferred to v1+. The `.skp` binary format has
no Python-native parser. Importing existing models requires running a Ruby export
script inside SketchUp first to dump geometry to JSON, which ARC can then read.
For v0, existing model knowledge comes from blueprints and descriptions.

### Stage 2: Extract

Use vision AI to read dimensions, room layouts, structural elements,
and annotations from blueprint images. Extract calls `arc/llm/vision.py`
which handles all Ollama vision model communication.

| Component | Purpose |
|-----------|---------|
| `extract/dimension_extractor.py` | Wall lengths, room sizes, annotations, scale factors |
| `extract/element_detector.py` | Doors, windows, fixtures, structural members |
| `extract/sheet_classifier.py` | Classify sheet type: floor plan, elevation, section, site plan |

All extract components call `arc/llm/vision.py` for image analysis.

Output: structured extraction JSON with confidence scores per dimension.

**Accuracy target:** Extracted dimensions within 6 inches of ground truth for v0.

### Vision Model Strategy

Blueprint dimension extraction from scanned architectural drawings is a hard
vision task: reading faded annotations, understanding scale bars, parsing
dimension chains with leaders. Current approach:

- **Model:** Ollama with a vision-capable model (e.g., `llava:34b` or
  `qwen2-vl:72b`). The specific model will be determined by benchmark
  testing against `blueprint-dimensions-reference.md` ground truth data.
  The platform's `qwen3-embedding:8b` is for embeddings only, not vision.
- **Fallback:** When vision confidence is below threshold (configurable,
  default 0.7), the dimension is flagged `"needs_verification": true` in
  the extraction JSON. The user manually corrects these values before
  proceeding to the Model stage.
- **Human-in-the-loop:** For v0, expect significant manual correction.
  The pipeline is designed so you can edit the extraction JSON directly
  before running `arc model`. The goal is to reduce manual work over time
  as the vision prompts and model improve, not to eliminate it on day one.

### Stage 3: Model

Build an internal spatial representation of the structure from extracted data.

| Component | Purpose |
|-----------|---------|
| `model/spatial_model.py` | Core data structure: rooms, walls, openings, dimensions |
| `model/constraints.py` | Lot boundaries, setbacks, building codes |
| `model/serialization.py` | Save/load spatial model as JSON |

The spatial model is the heart of ARC. Everything downstream reads from it.

### Stage 4: Design (v1+ only)

Given the existing structure and constraints, propose remodel modifications.
This stage is **not needed for v0** (which models the as-built only) and will
not be implemented until the Extract → Model → Generate pipeline is proven.

| Component | Purpose |
|-----------|---------|
| `design/layout_engine.py` | Propose floor plan modifications |
| `design/code_compliance.py` | RPV building code validation |

Output: modified spatial model JSON with proposed changes annotated.

### Stage 5: Generate

Produce SketchUp Ruby scripts and LayOut documents from the spatial model.

**Tier 1 output (v0):** Single `.rb` script for 3D model
**Tier 2 output (v1):** `.rb` model script + `.rb` LayOut document script
**Tier 3 output (future):** SketchUp extension (.rbz) with interactive panel

| Component | Purpose |
|-----------|---------|
| `generate/sketchup_ruby.py` | Emit .rb scripts for SketchUp model creation |
| `generate/layout_template.py` | Emit .rb scripts for LayOut drawing set creation |

---

## 4. Spatial Model Data Structure

JSON representation of the building. All dimensions in feet unless noted.
Inch-denominated fields use an `_in` suffix (e.g., `thickness_in`).

**Coordinate system:** X = East, Y = North, Z = Up. Origin is project-specific
(e.g., SW corner of lot for Seacove). Room polygons are 2D `[x, y]` at the
floor's Z origin (`level * floor_to_floor_height`). Walls extrude vertically
from the polygon at the floor's Z.

**Schema version:** The top-level `schema_version` field tracks format changes.

### Wall Topology

Walls are **top-level entities per floor**, not nested inside rooms. A physical
wall exists once, with references to the rooms on each side. This prevents
duplicate geometry when two rooms share a wall.

```json
{
  "schema_version": 1,
  "project": "seacove",
  "address": "25 Seacove Dr, Rancho Palos Verdes, CA 90275",
  "coordinate_system": { "x": "east", "y": "north", "z": "up", "origin": "SW corner of lot" },
  "lot": {
    "boundaries": [[0, 0], [80, 0], [80, 60], [0, 60]],
    "setbacks": { "front": 20, "rear": 15, "side_left": 5, "side_right": 5 },
    "slope": null
  },
  "structure": {
    "floors": [
      {
        "level": 0,
        "label": "Ground Floor",
        "plate_height": 8.0,
        "z_origin": 0.0,
        "rooms": [
          {
            "id": "kitchen-01",
            "label": "Kitchen",
            "polygon": [[0,0], [12,0], [12,14], [0,14]],
            "wall_refs": ["wall-s-living", "wall-kitchen-east", "wall-n-kitchen", "wall-west"],
            "fixtures": [
              { "type": "sink", "position": [6, 13.5] },
              { "type": "range", "position": [3, 13.5] }
            ]
          }
        ],
        "walls": [
          {
            "id": "wall-s-living",
            "from": [0, 0], "to": [28, 0],
            "type": "exterior",
            "thickness_in": 6,
            "rooms": { "interior": "kitchen-01", "exterior": null },
            "openings": [
              {
                "type": "door",
                "position_along_wall": 14.0,
                "width": 3.0,
                "height": 6.67,
                "sill_height": 0.0
              }
            ],
            "sources": [
              { "ref": "as-built-floor-plan", "confidence": 0.95 }
            ]
          }
        ]
      }
    ]
  },
  "structural": {
    "posts": [
      { "position": [2, 0], "size_in": 4, "material": "douglas_fir" }
    ],
    "beams": [
      { "from": [-2, 9], "to": [30, 9], "width_in": 4, "depth_in": 10, "z": 8.0 }
    ]
  },
  "roof": {
    "planes": [
      {
        "label": "Living Wing",
        "type": "flat",
        "slope": 0.25,
        "overhang": 3.5,
        "boundary": [[0, 0], [28, 0], [28, 18], [0, 18]],
        "z_base": 8.83
      }
    ]
  },
  "site": {
    "roads": [],
    "driveway": [],
    "trees": [],
    "pool": {}
  },
  "sources": [
    {
      "id": "as-built-floor-plan",
      "type": "blueprint",
      "file": "inputs/as-built-floor-plan.pdf",
      "page": 1
    }
  ],
  "conflicts": []
}
```

Key properties:
- **Walls are top-level per floor** — each physical wall exists once with room references on each side; no duplicate geometry
- **Polygon-based rooms** — handles L-shapes, angled walls
- **Openings on walls** — positioned along wall segments with exact dimensions
- **Per-dimension source + confidence** — each wall/opening tracks which source it came from and how confident the extraction was
- **Conflicts array** — when sources disagree (e.g., floor plan says 12' but elevation implies 12'6"), the conflict is recorded for manual resolution
- **Schema version** — `schema_version: 1` enables future format migration
- **Structural members separate from room geometry** — posts, beams, roof planes

---

## 5. Generated Ruby Code Architecture

### What Changes from Current Hand-Written Scripts

The current Seacove scripts use `make_box` for everything. ARC-generated code
will use the full SketchUp Pro Ruby API:

| Current pattern | ARC-generated pattern |
|----------------|----------------------|
| Groups for everything | Components for repeated elements (doors, windows, posts) |
| `make_box` walls | `make_wall` with proper thickness + boolean `subtract` for openings |
| No openings | Solid operations to cut doors/windows through walls |
| No scenes | Scenes pre-configured for plan, elevation, section views |
| Basic tags | Tag folders (Structure/, Site/, Landscape/) |
| No sections | Section planes for section cut views |
| No dimensions | `add_dimension_linear` on key measurements |
| No profiles | `followme` for eave profiles, moldings |
| Single monolithic script | Modular component scripts loaded in sequence |

### Generated Script Structure

```ruby
# 00_helpers.rb    — SeacoveHelpers module (unit conversion, geometry utils)
# 01_components.rb — Component definitions (door_3068, window_4040, post_4x4, etc.)
# 02_site.rb       — Lot boundary, roads, topography
# 03_foundation.rb — Slabs, footings
# 04_walls.rb      — Walls with openings cut via boolean subtract
# 05_structure.rb  — Posts, beams
# 06_roof.rb       — Roof planes with overhangs
# 07_interior.rb   — Fixtures, cabinets, finishes
# 08_scenes.rb     — Camera positions, tag visibility, section planes
# 09_layout.rb     — LayOut document: viewports, dimensions, title block, PDF export
```

### Component Definition Pattern

```ruby
# Define once
defn = model.definitions.add("Door_3068")
# ... build door geometry in defn.entities ...

# Instance everywhere
walls.each do |wall|
  wall[:openings].each do |opening|
    if opening[:type] == "door"
      transform = calculate_door_transform(wall, opening)
      entities.add_instance(defn, transform)
    end
  end
end
```

### Boolean Opening Cuts

```ruby
# Wall is a manifold solid group
wall_group = build_wall_solid(wall_data)

# Cutting box for each opening
opening_data[:openings].each do |opening|
  cutter = build_opening_cutter(wall_data, opening)
  wall_group = wall_group.subtract(cutter)  # Pro only
end
```

### Scene Creation for Drawing Views

```ruby
# Floor plan (top-down orthographic)
page = model.pages.add("Floor Plan")
page.use_camera = true
cam = Sketchup::Camera.new(center_eye_above, center_target, Y_AXIS)
cam.perspective = false
cam.height = building_width * 12 * 1.2  # inches, with margin
page.camera = cam

# Set tag visibility: show walls, hide roof
page.set_visibility(model.layers["Roof"], false)
page.set_visibility(model.layers["Structure/Posts"], true)

# Section cut
sp = entities.add_section_plane([section_point, section_normal])
page.use_section_planes = true
```

### LayOut Document Generation

```ruby
doc = Layout::Document.new("/templates/ARCH_D_24x36.layout")

# Title block on shared layer
tb_layer = doc.layers.add("Title Block", true)
# ... build title block with auto-text fields ...

# Sheet A1 - Site Plan
page = doc.pages[0]
page.name = "A1 - SITE PLAN"
bounds = Geom::Bounds2d.new(1.5, 2.0, 19.0, 13.0)
vp = Layout::SketchUpModel.new("/path/to/model.skp", bounds)
vp.current_scene = vp.scenes.index("Site Plan")
vp.render_mode = Layout::SketchUpModel::VECTOR_RENDER
vp.perspective = false
vp.scale = 0.0625  # 1/16" = 1'-0"
vp.display_background = false
doc.add_entity(vp, content_layer, page)

# Dimensions connected to model geometry
dim = Layout::LinearDimension.new(start_pt, end_pt, offset)
doc.add_entity(dim, dim_layer, page)

# Export
doc.save("/output/seacove_permit_set.layout")
doc.export("/output/seacove_permit_set.pdf", { dpi: 300 })
```

---

## 6. Directory Structure

```
ARC/
├── CLAUDE.md                     # ARC-specific rules (references platform parent)
├── arc/                          # Python source
│   ├── __init__.py
│   ├── cli.py                    # Entry point — commands: ingest, extract, model, validate, generate
│   ├── ingest/
│   │   ├── __init__.py
│   │   ├── blueprint_reader.py
│   │   ├── photo_reader.py
│   │   └── description.py
│   ├── extract/                  # Calls llm/vision.py for all image analysis
│   │   ├── __init__.py
│   │   ├── dimension_extractor.py
│   │   ├── element_detector.py
│   │   └── sheet_classifier.py
│   ├── model/
│   │   ├── __init__.py
│   │   ├── spatial_model.py
│   │   ├── validator.py          # Model consistency checks (walls connect, openings fit)
│   │   ├── constraints.py
│   │   └── serialization.py
│   ├── design/                   # v1+ only — not implemented for v0
│   │   └── (empty until needed)
│   ├── generate/
│   │   ├── __init__.py
│   │   ├── sketchup_ruby.py
│   │   └── layout_template.py
│   └── llm/                      # Shared service layer — all Ollama communication
│       ├── __init__.py
│       ├── vision.py             # Image analysis for Extract stage
│       └── embeddings.py         # Text embeddings (future use)
├── templates/
│   ├── ruby/                     # Ruby code templates (Jinja2)
│   │   ├── helpers.rb.j2
│   │   ├── components.rb.j2
│   │   ├── walls.rb.j2
│   │   ├── scenes.rb.j2
│   │   └── layout_doc.rb.j2
│   └── layout/                   # LayOut document templates
│       └── ARCH_D_24x36.layout
├── projects/
│   └── seacove/
│       ├── inputs/               # Scanned blueprints, photos
│       ├── model/                # Spatial model JSON
│       ├── output/               # Generated .rb and .layout files
│       └── ground_truth/         # Known-good dimensions for validation
├── reference/
│   ├── rpv-building-codes.md
│   ├── sketchup-api-patterns.md  # Proven Ruby API patterns for code generator
│   └── layout-api-patterns.md    # Proven LayOut API patterns
├── tests/
│   ├── test_extract_accuracy.py  # Extracted vs ground truth dimensions
│   ├── test_spatial_model.py     # Model serialization/validation
│   ├── test_ruby_generation.py   # Generated Ruby syntax/structure validation
│   └── test_layout_generation.py # Generated LayOut script validation
├── requirements.txt
└── pyproject.toml
```

---

## 7. Ruby Code Generation Strategy

ARC generates Ruby code using **Jinja2 templates** populated from the spatial model.
This is NOT string concatenation — it's structured template rendering.

### Why Jinja2 Templates

- Separates Ruby syntax from generation logic
- Templates can be tested and validated independently
- Ruby patterns are visible and editable (not buried in Python string builders)
- Same template engine used across the GrowDirect platform

### Template Example: Wall Generation

```ruby
# walls.rb.j2
# Walls are top-level per floor (not nested in rooms) to avoid duplicate geometry.
# Opening cut positions are computed by the Python generator from position_along_wall
# and wall direction before template rendering.

model = Sketchup.active_model
ents = model.active_entities
model.start_operation("{{ project_label }} - Walls", true)

{% for floor in floors %}
# === {{ floor.label }} (Z origin: {{ floor.z_origin }}') ===
{% for wall in floor.walls %}
# {{ wall.id }} — {{ wall.type }}
wall_grp = SeacoveHelpers.tagged_group(ents, model, "Walls/{{ wall.type | capitalize }}")
wall_grp.name = "{{ wall.id }}"
SeacoveHelpers.make_wall(
  wall_grp,
  [{{ wall.from_x }}, {{ wall.from_y }}],
  [{{ wall.to_x }}, {{ wall.to_y }}],
  {{ wall.thickness_ft }},
  {{ floor.plate_height }}
)

{% if wall.openings %}
# Cut openings (positions pre-computed by generator)
{% for opening in wall.openings %}
cutter = SeacoveHelpers.tagged_group(ents, model, "Temp")
SeacoveHelpers.make_box(cutter,
  {{ opening.cut_x }}, {{ opening.cut_y }}, {{ opening.sill_height }},
  {{ opening.width }}, {{ wall.thickness_ft + 0.01 }}, {{ opening.height }}
)
wall_grp = wall_grp.subtract(cutter)
{% endfor %}
{% endif %}

{% endfor %}
{% endfor %}

model.commit_operation
{% set total_rooms = floors | map(attribute='rooms') | map('length') | sum %}
puts "Walls complete: {{ total_rooms }} rooms across {{ floors | length }} floors"
```

Note: The Python generator (`generate/sketchup_ruby.py`) pre-computes derived
fields (`cut_x`, `cut_y`, `thickness_ft`, `from_x`, etc.) from the spatial
model before passing context to Jinja2. Templates receive flat, render-ready
values — they do not compute geometry.

---

## 8. First Milestone: Seacove Validation

### Inputs Already Available

| File | Type |
|------|------|
| `25 Seacove Blueprints/` | Scanned as-built drawings (multiple sheets) |
| `seacove scans/` | Site photos |
| `blueprint-dimensions-reference.md` | Hand-extracted ground truth dimensions |
| `25-Seacove-As-Built.rb` | Hand-written monolithic Ruby script |
| `sketchup-ruby/` | Hand-written modular Ruby scripts |

### Validation Loop

1. Feed as-built blueprints into `arc extract`
2. Compare extracted dimensions against `blueprint-dimensions-reference.md`
3. Build spatial model from extractions
4. Generate Ruby scripts from spatial model
5. Compare generated `.rb` output against hand-written scripts
6. Run generated script in SketchUp Pro, visually verify

### "Done" Criteria for v0

- `arc extract` reads Seacove blueprints and produces spatial model JSON with
  dimensions within 6 inches of ground truth
- `arc generate` produces a `.rb` script that uses components, proper wall
  thickness, boolean opening cuts, tag folders, and scenes
- The generated script runs in SketchUp Pro and produces a recognizable
  Seacove model with correct room shapes and proportions
- Not pixel-perfect. Not permit-ready. Pipeline works end-to-end.

### "Done" Criteria for v1

- LayOut document generation script produces a multi-sheet drawing set:
  A0 Cover, A1 Site Plan, A2 Floor Plan, A3 Elevations, A4 Sections
- Viewports reference SketchUp scenes at correct scales
- Title block with auto-text fields (project name, date, sheet number)
- Dimensions connected to model geometry
- PDF export at 300 dpi
- Drawing set is recognizable as a permit submission (not necessarily
  complete enough to actually submit)

---

## 9. Technology Choices

| Concern | Choice | Reason |
|---------|--------|--------|
| Language | Python 3.12 | Platform standard |
| Vision AI | Ollama (shared instance) | Already running, no external API dependency |
| Template engine | Jinja2 | Platform standard, handles Ruby syntax cleanly |
| Spatial model format | JSON | Human-readable, easy to inspect/edit, no DB needed |
| Ruby target | SketchUp 2024+ Ruby API | Pro subscription, boolean solids, EntitiesBuilder |
| LayOut target | LayOut 2024+ Ruby API | Full document creation from Ruby |
| Testing | pytest | Platform standard |
| CLI framework | Click or argparse | Simple, no web server needed |

---

## 10. What ARC Does NOT Do

- No web UI — CLI and conversational only
- No multi-tenancy — single user tool
- No MCP server — invisible to platform
- No real-time SketchUp integration (v0/v1) — generates scripts, you run them
- No structural engineering calculations — geometry only
- No cost estimation — dimensions and drawings only
- No 3D Warehouse integration — all components built from scratch
- No DWG export via API — PDF only (DWG requires SketchUp GUI menu)
