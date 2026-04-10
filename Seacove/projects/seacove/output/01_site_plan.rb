# 01_site_plan.rb — Clean lot outline for LayOut site plan
#
# This creates a MINIMAL SketchUp model ready for LayOut:
#   - Lot boundary outline (Lot 69, Tract 14649)
#   - Corner markers
#   - Property line dimensions
#   - Top-down parallel projection scene named "Site Plan"
#
# LayOut does the sheet, border, title block, and scale (1/8" = 1'-0").
# SketchUp just holds the geometry at 1:1 scale.
#
# Usage:
#   load '/Users/gclyle/GrowDirect/ARC/projects/seacove/output/00_helpers.rb'
#   load '/Users/gclyle/GrowDirect/ARC/projects/seacove/output/01_site_plan.rb'
#   SeacovePlan.build
#
# Then: File → Save As → seacove_site_plan.skp
# Then: Open LayOut → Insert viewport → set scale to 1/8" = 1'-0"

module SeacovePlan

  # ==========================================================================
  # LOT BOUNDARY — Lot 69, Tract 14649 (from IWS 2018 Survey)
  # ==========================================================================
  # Verified: 32 PASS, 0 FAIL (scripts/verify_site_plan.py)
  # Coordinate origin = SW corner of lot

  LOT_BOUNDARY = [
    [0.0, 0.0],          # SW corner
    [10.0, -3.5],         # cul-de-sac arc
    [20.0, -7.5],
    [28.0, -11.0],
    [36.0, -13.5],
    [44.0, -14.5],        # near deepest arc point
    [52.0, -13.5],
    [60.0, -10.0],
    [68.0, -5.0],
    [78.0, 3.0],          # SE corner
    [80.0, 20.0],         # east boundary (Clipper Rd)
    [82.5, 40.0],
    [85.0, 60.0],
    [87.5, 80.0],
    [89.5, 100.0],
    [92.0, 120.0],        # NE corner
    [61.0, 121.5],        # north boundary (Lot 70)
    [30.0, 123.0],
    [0.0, 124.0],         # NW corner
  ]

  CORNERS = {
    "SW" => [0.0, 0.0],
    "SE" => [78.0, 3.0],
    "NE" => [92.0, 120.0],
    "NW" => [0.0, 124.0],
  }

  # ==========================================================================
  # HELPERS
  # ==========================================================================
  def self.mat(model, name, r, g, b, a = 255)
    m = model.materials[name]
    unless m
      m = model.materials.add(name)
      m.color = Sketchup::Color.new(r, g, b, a)
    end
    m
  end

  # ==========================================================================
  # LOT OUTLINE
  # ==========================================================================
  def self.draw_lot(model)
    grp = model.entities.add_group
    grp.name = "Lot Boundary"

    # Lot fill — very light, just enough to see the shape
    pts = LOT_BOUNDARY.map { |p| SeacoveHelpers.pt(p[0], p[1], 0) }
    face = grp.entities.add_face(pts)
    if face
      face.material = mat(model, "Lot_Fill", 240, 245, 230, 40)
      face.back_material = mat(model, "Lot_Fill", 240, 245, 230, 40)
    end

    grp
  end

  # ==========================================================================
  # CORNER MARKERS
  # ==========================================================================
  def self.draw_corners(model)
    grp = model.entities.add_group
    grp.name = "Corner Markers"

    CORNERS.each do |label, c|
      x, y = c
      z = 0.05
      s = 1.5  # marker size

      # Crosshair
      grp.entities.add_edges(
        SeacoveHelpers.pt(x - s, y, z), SeacoveHelpers.pt(x + s, y, z))
      grp.entities.add_edges(
        SeacoveHelpers.pt(x, y - s, z), SeacoveHelpers.pt(x, y + s, z))

      # Circle
      grp.entities.add_circle(
        SeacoveHelpers.pt(x, y, z),
        Geom::Vector3d.new(0, 0, 1),
        SeacoveHelpers.ft(s), 16)
    end

    grp
  end

  # ==========================================================================
  # PROPERTY LINE DIMENSIONS
  # ==========================================================================
  def self.draw_dimensions(model)
    grp = model.entities.add_group
    grp.name = "Property Line Dimensions"
    de = grp.entities

    sw = CORNERS["SW"]
    se = CORNERS["SE"]
    ne = CORNERS["NE"]
    nw = CORNERS["NW"]
    off = 6.0  # dimension offset from boundary

    # West: SW → NW (124')
    de.add_dimension_linear(
      SeacoveHelpers.pt(sw[0], sw[1], 0),
      SeacoveHelpers.pt(nw[0], nw[1], 0),
      Geom::Vector3d.new(-SeacoveHelpers.ft(off), 0, 0))

    # North: NW → NE (92')
    de.add_dimension_linear(
      SeacoveHelpers.pt(nw[0], nw[1], 0),
      SeacoveHelpers.pt(ne[0], ne[1], 0),
      Geom::Vector3d.new(0, SeacoveHelpers.ft(off), 0))

    # East: NE → SE (118')
    de.add_dimension_linear(
      SeacoveHelpers.pt(ne[0], ne[1], 0),
      SeacoveHelpers.pt(se[0], se[1], 0),
      Geom::Vector3d.new(SeacoveHelpers.ft(off), 0, 0))

    # South chord: SW → SE (78')
    de.add_dimension_linear(
      SeacoveHelpers.pt(sw[0], sw[1], 0),
      SeacoveHelpers.pt(se[0], se[1], 0),
      Geom::Vector3d.new(0, -SeacoveHelpers.ft(off), 0))

    grp
  end

  # ==========================================================================
  # SCENE — Top-down parallel projection
  # ==========================================================================
  def self.setup_scene(model)
    # Camera: looking straight down, centered on lot
    cx = 46.0   # roughly center of lot X
    cy = 55.0   # roughly center of lot Y
    height = 200.0

    eye = SeacoveHelpers.pt(cx, cy, height)
    target = SeacoveHelpers.pt(cx, cy, 0)
    up = Geom::Vector3d.new(0, 1, 0)

    cam = Sketchup::Camera.new(eye, target, up)
    cam.perspective = false

    model.active_view.camera = cam

    # Create or update "Site Plan" scene
    pages = model.pages
    scene = pages["Site Plan"]
    if scene
      scene.update
    else
      scene = pages.add("Site Plan")
    end
    scene.use_camera = true
    scene.update

    model.active_view.zoom_extents
    scene.update

    puts "  Scene 'Site Plan' created — top-down parallel projection"
    puts "  In LayOut: Insert → SketchUp Model → select this .skp"
    puts "  Set viewport scale to 1/8\" = 1'-0\" (1:96)"
  end

  # ==========================================================================
  # BUILD
  # ==========================================================================
  def self.build
    model = Sketchup.active_model
    model.start_operation("Site Plan — Lot Outline", true)

    puts "\n=== SITE PLAN — Lot 69, Tract 14649 ==="
    puts "  5765 Sea Cove Drive, Rancho Palos Verdes"
    puts ""

    draw_lot(model)
    puts "  Lot boundary: #{LOT_BOUNDARY.length} points"

    draw_corners(model)
    puts "  Corner markers: SW, SE, NE, NW"

    draw_dimensions(model)
    puts "  Dimensions: 4 property lines"

    model.commit_operation

    setup_scene(model)

    puts ""
    puts "=== DONE ==="
    puts ""
    puts "Next steps:"
    puts "  1. File → Save As → seacove_site_plan.skp"
    puts "  2. Open LayOut"
    puts "  3. File → New → choose D-size (24\"×36\") template"
    puts "  4. File → Insert → select the .skp file"
    puts "  5. Set viewport to 'Site Plan' scene"
    puts "  6. Set scale: 1/8\" = 1'-0\""
    puts "  7. Add border, title block, labels in LayOut"
  end
end

puts "SeacovePlan loaded."
puts "  SeacovePlan.build  — lot outline + dimensions + scene"
