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
| Existing SketchUp models | .skp | `ingest/skp_reader.py` |
| Natural language descriptions | Text (CLI or file) | `ingest/description.py` |

Output: normalized images/text in the project's `inputs/` directory.

### Stage 2: Extract

Use vision AI (Ollama) to read dimensions, room layouts, structural elements,
and annotations from blueprint images.

| Component | Purpose |
|-----------|---------|
| `extract/dimension_extractor.py` | Wall lengths, room sizes, annotations, scale factors |
| `extract/element_detector.py` | Doors, windows, fixtures, structural members |
| `extract/sheet_classifier.py` | Classify sheet type: floor plan, elevation, section, site plan |

Output: structured extraction JSON with confidence scores per dimension.

**Accuracy target:** Extracted dimensions within 6 inches of ground truth for v0.

### Stage 3: Model

Build an internal spatial representation of the structure from extracted data.

| Component | Purpose |
|-----------|---------|
| `model/spatial_model.py` | Core data structure: rooms, walls, openings, dimensions |
| `model/constraints.py` | Lot boundaries, setbacks, building codes |
| `model/serialization.py` | Save/load spatial model as JSON |

The spatial model is the heart of ARC. Everything downstream reads from it.

### Stage 4: Design

Given the existing structure and constraints, propose remodel modifications.

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

JSON representation of the building. All dimensions in feet (construction standard).

```json
{
  "project": "seacove",
  "address": "25 Seacove Dr, Rancho Palos Verdes, CA 90275",
  "lot": {
    "boundaries": [[x, y], ...],
    "setbacks": { "front": 20, "rear": 15, "side_left": 5, "side_right": 5 },
    "slope": null
  },
  "structure": {
    "floors": [
      {
        "level": 0,
        "label": "Ground Floor",
        "plate_height": 8.0,
        "rooms": [
          {
            "id": "kitchen-01",
            "label": "Kitchen",
            "polygon": [[0,0], [12,0], [12,14], [0,14]],
            "walls": [
              {
                "from": [0,0], "to": [12,0],
                "type": "exterior",
                "thickness_in": 6,
                "openings": [
                  {
                    "type": "door",
                    "position_along_wall": 4.0,
                    "width": 3.0,
                    "height": 6.67,
                    "sill_height": 0.0
                  }
                ]
              }
            ],
            "fixtures": [
              { "type": "sink", "position": [6, 13.5] },
              { "type": "range", "position": [3, 13.5] }
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
        "boundary": [[x,y], ...],
        "z_base": 8.83
      }
    ]
  },
  "site": {
    "roads": [...],
    "driveway": [...],
    "trees": [...],
    "pool": { ... }
  },
  "sources": [
    {
      "type": "blueprint",
      "file": "inputs/as-built-floor-plan.pdf",
      "page": 1,
      "confidence": 0.92
    }
  ]
}
```

Key properties:
- **Polygon-based rooms** — handles L-shapes, angled walls
- **Openings on walls** — positioned along wall segments with exact dimensions
- **Confidence scores** — low confidence flags manual verification needed
- **Multiple sources per fact** — cross-reference catches errors
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
├── arc/                          # Python source
│   ├── __init__.py
│   ├── cli.py                    # Entry point
│   ├── ingest/
│   │   ├── __init__.py
│   │   ├── blueprint_reader.py
│   │   ├── photo_reader.py
│   │   ├── skp_reader.py
│   │   └── description.py
│   ├── extract/
│   │   ├── __init__.py
│   │   ├── dimension_extractor.py
│   │   ├── element_detector.py
│   │   └── sheet_classifier.py
│   ├── model/
│   │   ├── __init__.py
│   │   ├── spatial_model.py
│   │   ├── constraints.py
│   │   └── serialization.py
│   ├── design/
│   │   ├── __init__.py
│   │   ├── layout_engine.py
│   │   └── code_compliance.py
│   ├── generate/
│   │   ├── __init__.py
│   │   ├── sketchup_ruby.py
│   │   └── layout_template.py
│   └── llm/
│       ├── __init__.py
│       ├── vision.py
│       └── embeddings.py
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
model = Sketchup.active_model
ents = model.active_entities
model.start_operation("{{ project.label }} - Walls", true)

{% for floor in structure.floors %}
# === {{ floor.label }} ===
{% for room in floor.rooms %}
{% for wall in room.walls %}
# {{ room.label }} - {{ wall.type }} wall
wall_grp = SeacoveHelpers.tagged_group(ents, model, "Walls/{{ wall.type | capitalize }}")
wall_grp.name = "Wall_{{ room.id }}_{{ loop.index0 }}"
SeacoveHelpers.make_wall(
  wall_grp,
  [{{ wall.from[0] }}, {{ wall.from[1] }}],
  [{{ wall.to[0] }}, {{ wall.to[1] }}],
  {{ wall.thickness_in / 12.0 }},
  {{ floor.plate_height }}
)

{% if wall.openings %}
# Cut openings
{% for opening in wall.openings %}
cutter = SeacoveHelpers.tagged_group(ents, model, "Temp")
SeacoveHelpers.make_box(cutter,
  {{ opening.cut_origin_x }}, {{ opening.cut_origin_y }}, {{ opening.sill_height }},
  {{ opening.width }}, {{ wall.thickness_in / 12.0 + 0.1 }}, {{ opening.height }}
)
wall_grp = wall_grp.subtract(cutter)
{% endfor %}
{% endif %}

{% endfor %}
{% endfor %}
{% endfor %}

model.commit_operation
puts "Walls complete: {{ structure.floors | sum(attribute='rooms') | length }} rooms"
```

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
