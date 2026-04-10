# 02_site_plan.rb — Site plan: lot boundary, roads, and building footprint outline
# Based on Page 1 (Plot Plan) of the original 1958 Rucker drawings
#
# IMPORTANT: Many dimensions are approximate readings from faded scans.
# Dimensions marked with comments like "# VERIFY" need field measurement.
# The lot boundary is traced from the plot plan scan proportionally.
#
# Coordinate system:
#   Origin (0,0) = Southwest corner of lot (closest to Clipper/Sea Cove intersection)
#   X axis = East (positive)
#   Y axis = North (positive)
#   Z axis = Up (positive)
#
# Usage:
#   load '/path/to/00_helpers.rb'
#   load '/path/to/02_site_plan.rb'
#   SeacoveSite.create_lot_boundary
#   SeacoveSite.create_roads
#   SeacoveSite.create_building_footprint

module SeacoveSite
  include SeacoveHelpers

  # ============================================================
  # LOT BOUNDARY
  # ============================================================
  # Lot 69, Tract 14649
  # Irregular shape on cul-de-sac. These coordinates are traced
  # from the plot plan proportionally. The actual lot boundary
  # MUST be verified against the recorded tract map or ALTA survey.
  #
  # The lot sits at the intersection of Sea Cove Drive (cul-de-sac)
  # and Clipper Road. Sea Cove curves along the south/southwest.
  # The lot is roughly 120' deep (N-S) and 100' wide (E-W).
  # ============================================================

  # Approximate lot boundary points (feet from SW corner)
  # Traced from plot plan — VERIFY against tract map
  LOT_BOUNDARY = [
    [0, 0],         # SW corner (near Clipper/Sea Cove intersection)
    [10, -5],       # Along curved Sea Cove frontage
    [25, -8],       # Curve continues
    [40, -9],       # Low point of curve
    [55, -8],       # Curve coming back
    [70, -5],       # Near end of cul-de-sac curve
    [85, 0],        # SE corner area (where curve meets straight east line)
    [95, 10],       # East property line begins going north
    [100, 30],      # East line continues # VERIFY
    [102, 60],      # East line continues # VERIFY
    [103, 90],      # East line near NE corner # VERIFY
    [103, 120],     # NE corner # VERIFY
    [70, 122],      # North property line # VERIFY
    [35, 123],      # North line continues # VERIFY
    [0, 120],       # NW corner # VERIFY
  ]

  # ============================================================
  # BUILDING FOOTPRINT (original 1958 house only)
  # ============================================================
  # The house is positioned in the eastern half of the lot.
  # This is the ORIGINAL footprint before the 1960 addition.
  # Approximate placement from plot plan.
  #
  # The house has an L-shaped plan:
  # - Living wing runs E-W (south portion)
  # - Bedroom wing runs N-S (connects at east end)
  # ============================================================

  # Building footprint — original 1958 only
  # These are the OUTER WALL lines, not interior dimensions
  # Origin offset from lot SW corner
  BLDG_OFFSET_X = 25.0  # feet east of lot SW corner # VERIFY
  BLDG_OFFSET_Y = 30.0  # feet north of lot SW corner # VERIFY

  # Living wing (south portion, runs E-W)
  LIVING_WING = {
    x: 0,         # relative to BLDG_OFFSET
    y: 0,
    w: 22.5,      # ~22'-6" E-W width # from floor plan reading
    d: 22.83,     # ~22'-10" N-S depth # from floor plan reading
  }

  # Bedroom/service wing (east portion, runs N-S)
  # This connects to the east end of the living wing and extends north
  BEDROOM_WING = {
    x: 22.5,      # starts at east end of living wing
    y: 0,         # same south wall line as living wing
    w: 19.17,     # ~19'-2" E-W width (kitchen + bedrooms) # VERIFY
    d: 44.0,      # ~44'-0" N-S depth (extends well north) # VERIFY
  }

  def self.create_lot_boundary
    model = Sketchup.active_model
    model.start_operation("Lot Boundary", true)

    group = SeacoveHelpers.tagged_group(model.entities, model, "Site-Lot")
    group.name = "Lot 69 Boundary"
    ents = group.entities

    # Draw lot boundary as a closed polygon
    pts = LOT_BOUNDARY.map { |p| SeacoveHelpers.pt(p[0], p[1], 0) }
    face = ents.add_face(pts)

    if face
      # Light green ground color
      mat = model.materials.add("Lot_Ground")
      mat.color = Sketchup::Color.new(200, 220, 180, 180)
      face.material = mat
    end

    # Add property line labels at corners
    # (Just edges for now — labels added in LayOut)

    model.commit_operation
    puts "Lot boundary created (#{LOT_BOUNDARY.length} points)"
    puts "NOTE: Boundary is approximate — verify against tract map"
    group
  end

  def self.create_roads
    model = Sketchup.active_model
    model.start_operation("Roads", true)

    group = SeacoveHelpers.tagged_group(model.entities, model, "Site-Roads")
    group.name = "Roads"
    ents = group.entities

    # Sea Cove Drive — cul-de-sac curving along south of lot
    # Approximated as a wide arc south of the lot boundary
    # Road is ~24' wide (standard residential cul-de-sac)
    road_offset = 24.0 # feet south of lot line
    road_pts = [
      [-20, -15],
      [0, -24],
      [10, -29],
      [25, -32],
      [40, -33],
      [55, -32],
      [70, -29],
      [85, -24],
      [100, -15],
      # Connect back along lot edge
      [85, 0],
      [70, -5],
      [55, -8],
      [40, -9],
      [25, -8],
      [10, -5],
      [0, 0],
      [-20, 5],
    ]
    pts = road_pts.map { |p| SeacoveHelpers.pt(p[0], p[1], -0.01) }
    face = ents.add_face(pts)
    if face
      mat = model.materials.add("Road_Asphalt")
      mat.color = Sketchup::Color.new(100, 100, 100)
      face.material = mat
    end

    # Clipper Road — runs roughly E-W along south edge of property
    # Below Sea Cove Drive
    clipper_pts = [
      [-30, -33],
      [120, -40],
      [120, -60],
      [-30, -53],
    ]
    pts = clipper_pts.map { |p| SeacoveHelpers.pt(p[0], p[1], -0.02) }
    face2 = ents.add_face(pts)
    if face2
      mat2 = model.materials.add("Road_Clipper")
      mat2.color = Sketchup::Color.new(110, 110, 110)
      face2.material = mat2
    end

    model.commit_operation
    puts "Roads created: Sea Cove Drive (cul-de-sac) + Clipper Road"
    group
  end

  def self.create_building_footprint
    model = Sketchup.active_model
    model.start_operation("Building Footprint", true)

    group = SeacoveHelpers.tagged_group(model.entities, model, "Site-Footprint")
    group.name = "1958 Building Footprint"
    ents = group.entities

    ox = BLDG_OFFSET_X
    oy = BLDG_OFFSET_Y

    # Living wing outline
    lw = LIVING_WING
    living_pts = [
      SeacoveHelpers.pt(ox + lw[:x], oy + lw[:y], 0.01),
      SeacoveHelpers.pt(ox + lw[:x] + lw[:w], oy + lw[:y], 0.01),
      SeacoveHelpers.pt(ox + lw[:x] + lw[:w], oy + lw[:y] + lw[:d], 0.01),
      SeacoveHelpers.pt(ox + lw[:x], oy + lw[:y] + lw[:d], 0.01),
    ]
    face1 = ents.add_face(living_pts)
    if face1
      mat = model.materials.add("Footprint_1958")
      mat.color = Sketchup::Color.new(180, 160, 140, 200)
      face1.material = mat
    end

    # Bedroom wing outline
    bw = BEDROOM_WING
    bed_pts = [
      SeacoveHelpers.pt(ox + bw[:x], oy + bw[:y], 0.01),
      SeacoveHelpers.pt(ox + bw[:x] + bw[:w], oy + bw[:y], 0.01),
      SeacoveHelpers.pt(ox + bw[:x] + bw[:w], oy + bw[:y] + bw[:d], 0.01),
      SeacoveHelpers.pt(ox + bw[:x], oy + bw[:y] + bw[:d], 0.01),
    ]
    face2 = ents.add_face(bed_pts)
    if face2
      face2.material = model.materials["Footprint_1958"]
    end

    model.commit_operation
    puts "Building footprint created (1958 original)"
    puts "  Living wing: #{lw[:w]}' x #{lw[:d]}' at offset (#{ox}, #{oy})"
    puts "  Bedroom wing: #{bw[:w]}' x #{bw[:d]}' at offset (#{ox + bw[:x]}, #{oy + bw[:y]})"
    puts "NOTE: Dimensions are approximate — verify against blueprints"
    group
  end

  # Run all site plan components
  def self.build_all
    create_lot_boundary
    create_roads
    create_building_footprint
    Sketchup.active_model.active_view.zoom_extents
    puts "\n=== Site plan complete ==="
    puts "Tags created: Site-Lot, Site-Roads, Site-Footprint"
    puts "Toggle tags to show/hide each element"
  end

end

puts "SeacoveSite loaded."
puts "  SeacoveSite.create_lot_boundary  — lot boundary polygon"
puts "  SeacoveSite.create_roads         — Sea Cove Dr + Clipper Rd"
puts "  SeacoveSite.create_building_footprint — 1958 house outline"
puts "  SeacoveSite.build_all            — all of the above"
