# 01_site_pass1.rb — Pass 1: Site plan from 2018 IWS Survey
# Source: IWS Surveying Boundary/Topographic Survey, June 20, 2018
# 25 Sea Cove Drive, RPV — Tract #14649, Lot 69
#
# PASS 1 — Lot boundary and main dimensions only.
# Coordinates estimated from survey scan proportionally.
# Load 00_helpers.rb first.
#
# Basis of bearings: S 40°23'00" E being a radial line to
# the centerline of Sea Cove Drive.
# Benchmark: Assumed EL = 102.15 at mag & washer (NE corner area)
#
# Coordinate system for this model:
#   Origin (0,0) = SW-most corner of lot (near south driveway / Sea Cove)
#   X = East (positive), Y = North (positive), Z = Up
#   Note: Survey north is rotated ~40° from drawing vertical per basis of bearings.
#   For this pass, we align the lot with SketchUp axes as seen on the survey.
#
# Usage:
#   load '/Users/gclyle/GrowDirect/ARC/projects/seacove/output/00_helpers.rb'
#   load '/Users/gclyle/GrowDirect/ARC/projects/seacove/output/01_site_pass1.rb'
#   SeacoveSite1.build_lot
#   SeacoveSite1.build_house_footprint
#   SeacoveSite1.build_roads
#   SeacoveSite1.build_all

module SeacoveSite1
  include SeacoveHelpers

  # ==========================================================================
  # LOT BOUNDARY — Lot 69, Tract 14649
  # ==========================================================================
  # Traced from survey scan. Clockwise from SW corner.
  # The south boundary follows Sea Cove Drive cul-de-sac (curved).
  # East boundary runs along Clipper Road.
  # North boundary shared with Lot 70.
  # West boundary shared with Lot 67.
  #
  # These are ESTIMATED coordinates from the scan — expect corrections.
  # ==========================================================================

  # Property corners (main vertices of lot boundary)
  # [x, y] in feet from origin (SW corner)
  LOT_BOUNDARY = [
    # SW corner — origin, near south driveway / Sea Cove Dr
    [0, 0],
    # South boundary — follows Sea Cove Dr cul-de-sac arc
    # The cul-de-sac curves south then east
    [8, -6],          # curve begins
    [18, -10],        # low point of arc
    [30, -12],        # continuing east
    [42, -11],        # past midpoint
    [54, -8],         # curve rising back
    [66, -3],         # approaching Clipper Rd
    [74, 2],          # near SE, curve meets straight line
    # SE corner area — where Sea Cove meets Clipper Rd
    [80, 10],         # SE corner
    # East boundary — runs NNE along Clipper Rd
    [84, 30],
    [87, 50],
    [90, 70],
    [92, 90],
    [94, 110],
    # NE corner
    [95, 125],
    # North boundary — runs west, shared with Lot 70
    [60, 127],
    [30, 128],
    # NW corner
    [0, 126],
    # West boundary — runs south, shared with Lot 67
    # (closes back to origin)
  ]

  # ==========================================================================
  # EXISTING HOUSE FOOTPRINT (from survey annotation)
  # ==========================================================================
  # "EXISTING SINGLE STORY HOUSE"
  # FF = 100.00, Ridge = 108.82, Eave = 106.82
  # L-shaped plan: living wing (E-W) + bedroom wing (N-S)
  # Position estimated from survey scan
  HOUSE_OFFSET_X = 22.0  # feet east of lot SW corner
  HOUSE_OFFSET_Y = 28.0  # feet north of lot SW corner

  # Living wing (south portion, runs E-W) — from 1958 plans
  LIVING_WING = { x: 0, y: 0, w: 22.5, d: 22.83 }

  # Bedroom/service wing (east portion, runs N-S)
  BEDROOM_WING = { x: 22.5, y: 0, w: 19.17, d: 44.0 }

  # Key elevations
  FF_ELEVATION = 100.00
  RIDGE_ELEVATION = 108.82
  EAVE_ELEVATION = 106.82

  # ==========================================================================
  # METHODS
  # ==========================================================================

  def self.create_tag_folders(model)
    # Create Site tag folder with sub-tags
    # SketchUp 2021+ supports tag folders
    begin
      site_folder = model.layers.add_folder("Site")
      ["Lot Boundary", "House Footprint", "Roads", "Driveways",
       "Pool", "Improvements", "Spot Elevations", "Landscaping"].each do |tag_name|
        tag = model.layers.add(tag_name)
        site_folder.add_layer(tag) if site_folder.respond_to?(:add_layer)
      end
      puts "Tag folder 'Site/' created with sub-tags"
    rescue => e
      # Fallback for older SketchUp: flat tags
      puts "Tag folders not supported, using flat tags: #{e.message}"
      ["Site-Lot Boundary", "Site-House Footprint", "Site-Roads",
       "Site-Driveways", "Site-Pool", "Site-Improvements"].each do |tag_name|
        model.layers.add(tag_name)
      end
    end
  end

  def self.build_lot
    model = Sketchup.active_model
    model.start_operation("Site - Lot Boundary", true)

    create_tag_folders(model)

    # --- Lot boundary polygon ---
    group = model.entities.add_group
    group.name = "site-lot-boundary"
    begin
      group.layer = model.layers["Lot Boundary"]
    rescue
      group.layer = model.layers["Site-Lot Boundary"] || model.layers.add("Site-Lot Boundary")
    end

    ents = group.entities
    pts = LOT_BOUNDARY.map { |p| SeacoveHelpers.pt(p[0], p[1], 0) }
    face = ents.add_face(pts)
    if face
      mat = model.materials.add("Lot_Ground")
      mat.color = Sketchup::Color.new(210, 225, 190, 150)
      face.material = mat
    end

    # --- Property corner markers ---
    corners = {
      "SW" => LOT_BOUNDARY[0],
      "SE" => LOT_BOUNDARY[9],   # [80, 10]
      "NE" => LOT_BOUNDARY[14],  # [95, 125]
      "NW" => LOT_BOUNDARY[17],  # [0, 126]
    }

    corners.each do |label, pt_coords|
      marker = model.entities.add_group
      marker.name = "site-corner-#{label}"
      begin
        marker.layer = model.layers["Lot Boundary"]
      rescue
        marker.layer = model.layers["Site-Lot Boundary"] || model.layers.add("Site-Lot Boundary")
      end
      # Draw a small X at each corner
      sz = 1.0 # 1 foot marker
      x, y = pt_coords
      marker.entities.add_edges(
        SeacoveHelpers.pt(x - sz, y - sz, 0.1),
        SeacoveHelpers.pt(x + sz, y + sz, 0.1)
      )
      marker.entities.add_edges(
        SeacoveHelpers.pt(x + sz, y - sz, 0.1),
        SeacoveHelpers.pt(x - sz, y + sz, 0.1)
      )
    end

    model.commit_operation
    puts "=== Lot boundary created ==="
    puts "  #{LOT_BOUNDARY.length} boundary points"
    puts "  Corners: SW(0,0) SE(80,10) NE(95,125) NW(0,126)"
    puts "  PASS 1 — verify shape against survey, report corrections"
    group
  end

  def self.build_house_footprint
    model = Sketchup.active_model
    model.start_operation("Site - House Footprint", true)

    group = model.entities.add_group
    group.name = "site-house-footprint"
    begin
      group.layer = model.layers["House Footprint"]
    rescue
      group.layer = model.layers["Site-House Footprint"] || model.layers.add("Site-House Footprint")
    end

    ents = group.entities
    ox = HOUSE_OFFSET_X
    oy = HOUSE_OFFSET_Y

    # Living wing
    lw = LIVING_WING
    pts1 = [
      SeacoveHelpers.pt(ox + lw[:x], oy + lw[:y], 0.05),
      SeacoveHelpers.pt(ox + lw[:x] + lw[:w], oy + lw[:y], 0.05),
      SeacoveHelpers.pt(ox + lw[:x] + lw[:w], oy + lw[:y] + lw[:d], 0.05),
      SeacoveHelpers.pt(ox + lw[:x], oy + lw[:y] + lw[:d], 0.05),
    ]
    f1 = ents.add_face(pts1)
    if f1
      mat = model.materials.add("House_Footprint")
      mat.color = Sketchup::Color.new(180, 160, 140, 180)
      f1.material = mat
    end

    # Bedroom wing
    bw = BEDROOM_WING
    pts2 = [
      SeacoveHelpers.pt(ox + bw[:x], oy + bw[:y], 0.05),
      SeacoveHelpers.pt(ox + bw[:x] + bw[:w], oy + bw[:y], 0.05),
      SeacoveHelpers.pt(ox + bw[:x] + bw[:w], oy + bw[:y] + bw[:d], 0.05),
      SeacoveHelpers.pt(ox + bw[:x], oy + bw[:y] + bw[:d], 0.05),
    ]
    f2 = ents.add_face(pts2)
    if f2
      f2.material = model.materials["House_Footprint"]
    end

    model.commit_operation
    puts "=== House footprint placed ==="
    puts "  Offset from lot SW: (#{ox}', #{oy}')"
    puts "  Living wing: #{lw[:w]}' x #{lw[:d]}'"
    puts "  Bedroom wing: #{bw[:w]}' x #{bw[:d]}'"
    puts "  FF=#{FF_ELEVATION}, Ridge=#{RIDGE_ELEVATION}, Eave=#{EAVE_ELEVATION}"
    group
  end

  def self.build_roads
    model = Sketchup.active_model
    model.start_operation("Site - Roads", true)

    group = model.entities.add_group
    group.name = "site-roads"
    begin
      group.layer = model.layers["Roads"]
    rescue
      group.layer = model.layers["Site-Roads"] || model.layers.add("Site-Roads")
    end

    ents = group.entities

    # Sea Cove Drive — cul-de-sac, curves south of lot boundary
    # Road is approx 24' wide south of the property line
    road_south = LOT_BOUNDARY[0..9].map { |p| [p[0], p[1] - 24] }
    road_pts = LOT_BOUNDARY[0..9].reverse + road_south
    pts = road_pts.map { |p| SeacoveHelpers.pt(p[0], p[1], -0.1) }
    face = ents.add_face(pts)
    if face
      mat = model.materials.add("Road_SeaCove")
      mat.color = Sketchup::Color.new(110, 110, 110)
      face.material = mat
    end

    # Clipper Road — runs along east boundary
    # Road is approx 30' wide east of the property line
    clipper_inner = LOT_BOUNDARY[9..14]
    clipper_outer = clipper_inner.map { |p| [p[0] + 30, p[1]] }
    clipper_pts = clipper_inner + clipper_outer.reverse
    pts2 = clipper_pts.map { |p| SeacoveHelpers.pt(p[0], p[1], -0.1) }
    face2 = ents.add_face(pts2)
    if face2
      mat2 = model.materials.add("Road_Clipper")
      mat2.color = Sketchup::Color.new(105, 105, 105)
      face2.material = mat2
    end

    model.commit_operation
    puts "=== Roads created ==="
    puts "  Sea Cove Drive (cul-de-sac) — 24' wide"
    puts "  Clipper Road — 30' wide"
    group
  end

  def self.build_all
    build_lot
    build_house_footprint
    build_roads
    Sketchup.active_model.active_view.zoom_extents
    puts "\n=== Site plan pass 1 complete ==="
    puts "Compare against survey PDF. Report what's wrong."
    puts "We'll iterate until the boundary matches exactly."
  end

end

puts "SeacoveSite1 loaded."
puts "  SeacoveSite1.build_lot             — lot boundary polygon"
puts "  SeacoveSite1.build_house_footprint — existing house outline"
puts "  SeacoveSite1.build_roads           — Sea Cove Dr + Clipper Rd"
puts "  SeacoveSite1.build_all             — all of the above"
puts ""
puts "PASS 1 — bearing points are estimated. Tell me what's wrong."
