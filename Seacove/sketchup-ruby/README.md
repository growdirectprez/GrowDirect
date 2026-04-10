# 25 Seacove — SketchUp Ruby Model Components

## How This Works

Each `.rb` file is a self-contained component that builds one piece of the model.
Load them in order in the SketchUp Ruby Console. Each creates its own Tag (Layer)
so you can toggle visibility independently.

**Do NOT try to run them all at once.** Load one, verify it looks right, then load the next.

## File List

| File | What It Builds | Tag(s) Created | Depends On |
|------|---------------|----------------|------------|
| `00_helpers.rb` | Utility functions (ft, pt, make_box, make_wall, etc.) | None | Nothing |
| `01_template_page.rb` | 24x36 ARCH D sheet template with title block | Template-{sheet} | 00_helpers |
| `02_site_plan.rb` | Lot boundary, roads, building footprint outline | Site-Lot, Site-Roads, Site-Footprint | 00_helpers |
| `03_foundation.rb` | Foundation slab and footings | Foundation | 00_helpers |
| `04_walls_1958.rb` | Original 1958 exterior + interior walls | Walls-1958 | 00_helpers |
| `05_posts_beams.rb` | Structural posts and beams | Structure-Posts, Structure-Beams | 00_helpers |
| `06_roof.rb` | Roof planes with overhangs | Roof | 00_helpers |
| `07_addition_1960.rb` | 1960 bedroom addition | Walls-1960, Foundation-1960 | 00_helpers |
| `08_garage.rb` | Garage addition | Walls-Garage | 00_helpers |
| (future) | Kitchen, bathrooms, doors, windows, etc. | Various | 00_helpers |

## Usage in SketchUp

```ruby
# Step 1: Load the helpers (ALWAYS first)
load '/Users/YOU/path/to/ARC/sketchup-ruby/00_helpers.rb'

# Step 2: Load and run the site plan
load '/Users/YOU/path/to/ARC/sketchup-ruby/02_site_plan.rb'
SeacoveSite.build_all

# Step 3: Verify it looks right, then load next component
load '/Users/YOU/path/to/ARC/sketchup-ruby/04_walls_1958.rb'
SeacoveWalls1958.build_all

# Each component tells you what it created in the console output.
# Check the Tags panel to toggle visibility.
```

## Dimension Sources

All dimensions come from the blueprint archive in `/ARC/25 Seacove Blueprints/`.
See `blueprint-dimensions-reference.md` for the full extracted dimension list.

Dimensions marked `# VERIFY` in the code are approximate readings from faded scans
and need field measurement before the model is used for permit drawings.

## Coordinate System

- **Origin (0,0,0):** Southwest corner of lot (near Clipper/Sea Cove intersection)
- **X axis:** East (positive)
- **Y axis:** North (positive)
- **Z axis:** Up (positive)
- **Units:** All functions accept FEET. The helpers convert to inches internally.

## Adding New Components

1. Copy the pattern from an existing component file
2. Use `SeacoveHelpers` functions for geometry (don't write raw SketchUp API calls)
3. Create a tagged group for every piece of geometry
4. Print a summary to the console when the component loads
5. Mark any uncertain dimensions with `# VERIFY`
