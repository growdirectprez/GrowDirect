# 01_site_pass2.rb — Pass 2: Comprehensive site plan from 2018 IWS Survey
# Source: IWS Surveying Boundary/Topographic Survey, June 20, 2018
# 25 Sea Cove Drive, RPV — Tract #14649, Lot 69
#
# PASS 2 — Lot boundary, house, roads, driveways, pool, cabana,
#          spot elevations, setback lines, improvements.
#
# Basis of bearings: S 40°23'00" E radial to centerline of Sea Cove Dr.
# Benchmark: Assumed EL = 102.15 at mag & washer, NE corner Lot 69.
# Scale: 1" = 10'
#
# Coordinate system:
#   Origin (0,0) = SW corner of lot
#   X = East (positive), Y = North (positive), Z = Up
#   Elevations: survey datum (benchmark EL=102.15 at NE mag & washer)
#
# Load helpers first:
#   load '/Users/gclyle/GrowDirect/ARC/projects/seacove/output/00_helpers.rb'
#   load '/Users/gclyle/GrowDirect/ARC/projects/seacove/output/01_site_pass2.rb'
#   SeacoveSite2.build_all

module SeacoveSite2
  include SeacoveHelpers

  # ==========================================================================
  # LOT BOUNDARY — Lot 69, Tract 14649
  # ==========================================================================
  # Calibrated using house dimensions (42' x 44' L-shape) as scale reference.
  # Lot: ~105' E-W at north boundary, ~126' N-S on east side.
  # South boundary follows Sea Cove Dr cul-de-sac arc.
  #
  # Clockwise from SW corner. Each point annotated with what it represents.
  # ==========================================================================

  LOT_BOUNDARY = [
    # --- SW CORNER (origin) ---
    [0.0, 0.0],            # SW corner — monument: Set Nag & Washer RCE 28458

    # --- SOUTH BOUNDARY — Sea Cove Drive cul-de-sac arc ---
    # The cul-de-sac curves south. Points trace the right-of-way line.
    [10.0, -4.0],          # curve begins, heading east
    [20.0, -8.0],          # continuing along arc
    [30.0, -11.0],         # approaching low point of curve
    [40.0, -12.0],         # deepest point of cul-de-sac arc
    [50.0, -11.0],         # curve rising back
    [60.0, -8.0],          # continuing east
    [70.0, -4.0],          # approaching SE area
    [78.0, 2.0],           # curve meets Clipper Rd approach

    # --- SE CORNER ---
    [82.0, 10.0],          # SE corner — near Sea Cove / Clipper intersection

    # --- EAST BOUNDARY — along Clipper Road ---
    # Runs NNE. Clipper Rd angles slightly as it goes north.
    [85.0, 30.0],          # east line, 20' north of SE
    [88.0, 50.0],          # east line continues
    [91.0, 70.0],          # east line continues
    [93.0, 90.0],          # east line continues
    [95.0, 110.0],         # approaching NE

    # --- NE CORNER ---
    [96.0, 126.0],         # NE corner — benchmark nearby (15.09' ELY prod of NLY line)

    # --- NORTH BOUNDARY — shared with Lot 70 ---
    # Runs roughly west. Slight angle.
    [64.0, 128.0],         # north line, 1/3 from NE
    [32.0, 129.0],         # north line, 2/3 from NE

    # --- NW CORNER ---
    [0.0, 128.0],          # NW corner — shared with Lot 67/70

    # --- WEST BOUNDARY — shared with Lot 67 ---
    # Runs south back to origin. Roughly straight.
    # (polygon closes automatically to SW corner)
  ]

  # Corner indices for labeling
  CORNERS = {
    "SW" => 0,
    "SE" => 9,
    "NE" => 15,
    "NW" => 18,
  }

  # ==========================================================================
  # SETBACK LINES (estimated — RPV zoning TBD)
  # ==========================================================================
  SETBACKS = {
    front: 20.0,    # From Sea Cove Dr (south) — standard residential
    rear: 15.0,     # From north property line
    side_east: 10.0, # From Clipper Rd (corner lot, street-facing side)
    side_west: 5.0,  # From west property line
  }

  # ==========================================================================
  # HOUSE FOOTPRINT
  # ==========================================================================
  # Position calibrated: ~22' from west PL, ~28' from south PL (straight line)
  HOUSE_X = 22.0
  HOUSE_Y = 28.0

  LIVING_WING  = { x: 0.0, y: 0.0, w: 22.5, d: 22.83 }
  BEDROOM_WING = { x: 22.5, y: 0.0, w: 19.17, d: 44.0 }

  # Key elevations
  FF    = 100.00
  RIDGE = 108.82
  EAVE  = 106.82

  # ==========================================================================
  # DRIVEWAYS
  # ==========================================================================
  # North driveway: runs E-W from house area to Clipper Rd
  NORTH_DRIVEWAY = [
    [42.0, 80.0],         # NW corner of driveway (near house)
    [88.0, 80.0],         # NE corner (at Clipper Rd edge)
    [88.0, 92.0],         # SE corner at Clipper
    [42.0, 92.0],         # SW corner
  ]

  # South driveway: curves from Sea Cove Dr to SW area of property
  SOUTH_DRIVEWAY = [
    [-2.0, -8.0],         # entrance at Sea Cove Dr
    [8.0, -6.0],          # along road
    [12.0, 0.0],          # turns north
    [14.0, 10.0],         # curves up to property
    [10.0, 16.0],         # reaches property level
    [0.0, 16.0],          # west edge
    [-4.0, 8.0],          # back toward road
    [-6.0, -2.0],         # loops back
  ]

  # ==========================================================================
  # POOL & CABANA
  # ==========================================================================
  # Pool: west of house, roughly centered N-S
  POOL = {
    x: 6.0,   y: 40.0,
    w: 14.0,  d: 28.0,
  }

  # Cabana: small structure west of pool, near west PL
  CABANA = {
    x: 2.0,   y: 52.0,
    w: 8.0,   d: 12.0,
  }

  # ==========================================================================
  # SPOT ELEVATIONS
  # ==========================================================================
  # [x, y, elevation, label]
  # Positions estimated proportionally from survey scan.
  SPOT_ELEVATIONS = [
    # --- House ---
    [33.0, 45.0, 100.00, "FF"],
    [33.0, 60.0, 108.82, "RIDGE"],
    [33.0, 55.0, 106.82, "EAVE"],

    # --- North area (toward Lot 70) ---
    [50.0, 115.0, 104.12, nil],
    [70.0, 118.0, 103.59, nil],
    [85.0, 120.0, 102.41, nil],
    [30.0, 100.0, 100.30, nil],
    [50.0, 95.0,  100.12, nil],
    [60.0, 120.0, 104.61, nil],

    # --- North driveway ---
    [65.0, 86.0, 100.12, "CONC"],
    [80.0, 86.0, 100.30, "CONC"],

    # --- East area (Clipper Rd) ---
    [90.0, 100.0, 101.85, nil],
    [92.0, 115.0, 100.85, "E/P"],
    [88.0, 65.0,  99.04, nil],
    [85.0, 40.0,  98.25, nil],
    [90.0, 20.0,  96.30, nil],
    [88.0, 10.0,  95.04, "E/P"],

    # --- South area (Sea Cove Dr frontage) ---
    [40.0, 22.0, 100.14, nil],
    [45.0, 18.0, 98.60, nil],
    [50.0, 16.0, 98.42, nil],
    [55.0, 15.0, 98.50, "PALM"],
    [45.0, 10.0, 98.10, nil],
    [50.0, 8.0,  98.04, nil],
    [40.0, 2.0,  97.62, nil],
    [50.0, 0.0,  97.34, nil],
    [55.0, -5.0, 96.91, nil],
    [60.0, -8.0, 95.09, nil],
    [70.0, -2.0, 95.40, nil],

    # --- Concrete wall tops (south) ---
    [55.0, 6.0, 98.21, "TW"],
    [65.0, 4.0, 98.04, "TW"],

    # --- West area (pool / cabana) ---
    [8.0, 58.0,  98.63, "CONC"],
    [10.0, 50.0, 98.55, "CONC"],
    [10.0, 42.0, 98.50, "CONC"],
    [5.0, 65.0,  98.31, nil],
    [12.0, 45.0, 98.22, "CONC"],
    [5.0, 38.0,  98.04, nil],
    [3.0, 70.0,  98.25, "ELEC HYDR"],

    # --- SW area (south driveway, carport) ---
    [2.0, 25.0,  96.24, nil],
    [0.0, 20.0,  96.03, nil],
    [-2.0, 10.0, 95.54, nil],
    [-3.0, 5.0,  94.95, "CARPORT"],
    [5.0, -5.0,  93.54, "CONC"],
    [0.0, -8.0,  93.40, "CONC"],
    [-4.0, -4.0, 92.60, "FLOOD GATE"],

    # --- Landscaping area elevations ---
    [20.0, 8.0,  97.04, nil],
    [15.0, 5.0,  96.08, "TW"],
    [10.0, -2.0, 95.08, "TW"],
  ]

  # ==========================================================================
  # WALLS AND FENCES
  # ==========================================================================
  # [from_x, from_y, to_x, to_y, type, height_ft]
  WALLS_AND_FENCES = [
    # Concrete walls along south boundary (near Sea Cove Dr)
    [25.0, 6.0,  65.0, 6.0,  "conc_wall", 3.0],
    [65.0, 4.0,  78.0, 8.0,  "conc_wall", 3.0],

    # Concrete wall along east (near Clipper)
    [80.0, 12.0, 85.0, 30.0, "conc_wall", 3.0],

    # Chain link fence — west boundary
    [0.0, 20.0,  0.0, 70.0,  "chain_link", 4.0],

    # Concrete wall — north of driveway
    [42.0, 78.0, 88.0, 78.0, "conc_wall", 2.5],
  ]

  # ==========================================================================
  # TREES
  # ==========================================================================
  # [x, y, trunk_diameter_inches, label]
  TREES = [
    [55.0, 14.0, 24, "24\" PALM"],
  ]

  # ==========================================================================
  # TAG FOLDER SETUP
  # ==========================================================================
  def self.setup_tags(model)
    tags = {}
    begin
      folder = model.layers.add_folder("Site")
      tag_names = [
        "Lot Boundary", "Setbacks", "House Footprint", "Roads",
        "Driveways", "Pool & Cabana", "Improvements",
        "Spot Elevations", "Walls & Fences", "Landscaping"
      ]
      tag_names.each do |name|
        t = model.layers.add(name)
        folder.add_layer(t) if folder.respond_to?(:add_layer)
        tags[name] = t
      end
    rescue => e
      # Fallback: flat tags with Site- prefix
      tag_names = [
        "Lot Boundary", "Setbacks", "House Footprint", "Roads",
        "Driveways", "Pool & Cabana", "Improvements",
        "Spot Elevations", "Walls & Fences", "Landscaping"
      ]
      tag_names.each do |name|
        flat = "Site-#{name}"
        t = model.layers[flat] || model.layers.add(flat)
        tags[name] = t
      end
    end
    tags
  end

  def self.get_tag(model, tags, name)
    tags[name] || model.layers.add(name)
  end

  # ==========================================================================
  # BUILD METHODS
  # ==========================================================================

  def self.build_lot(model = nil, tags = nil)
    model ||= Sketchup.active_model
    tags ||= setup_tags(model)
    model.start_operation("Site - Lot Boundary", true)

    # Lot boundary polygon
    group = model.entities.add_group
    group.name = "site-lot-boundary"
    group.layer = get_tag(model, tags, "Lot Boundary")

    pts = LOT_BOUNDARY.map { |p| SeacoveHelpers.pt(p[0], p[1], 0) }
    face = group.entities.add_face(pts)
    if face
      mat = model.materials.add("Lot_Ground")
      mat.color = Sketchup::Color.new(215, 228, 195, 120)
      face.material = mat
    end

    # Property corner markers (X marks)
    CORNERS.each do |label, idx|
      corner_pt = LOT_BOUNDARY[idx]
      marker = model.entities.add_group
      marker.name = "site-corner-#{label}"
      marker.layer = get_tag(model, tags, "Lot Boundary")

      x, y = corner_pt
      sz = 1.5  # 1.5' marker size
      # Draw X
      marker.entities.add_edges(
        SeacoveHelpers.pt(x - sz, y - sz, 0.2),
        SeacoveHelpers.pt(x + sz, y + sz, 0.2)
      )
      marker.entities.add_edges(
        SeacoveHelpers.pt(x + sz, y - sz, 0.2),
        SeacoveHelpers.pt(x - sz, y + sz, 0.2)
      )
      # Draw circle around X
      marker.entities.add_circle(
        SeacoveHelpers.pt(x, y, 0.2),
        Geom::Vector3d.new(0, 0, 1),
        SeacoveHelpers.ft(sz), 16
      )
    end

    model.commit_operation
    puts "Lot boundary: #{LOT_BOUNDARY.length} points, 4 corner markers"
    group
  end

  def self.build_setbacks(model = nil, tags = nil)
    model ||= Sketchup.active_model
    tags ||= setup_tags(model)
    model.start_operation("Site - Setbacks", true)

    group = model.entities.add_group
    group.name = "site-setbacks"
    group.layer = get_tag(model, tags, "Setbacks")

    ents = group.entities

    # Inset the lot boundary by setback distances (simplified — straight offsets)
    # Front setback (from south boundary, roughly 20' north)
    front_y = SETBACKS[:front]
    ents.add_edges(
      SeacoveHelpers.pt(SETBACKS[:side_west], front_y, 0.15),
      SeacoveHelpers.pt(LOT_BOUNDARY[9][0] - SETBACKS[:side_east], front_y, 0.15)
    )

    # Rear setback (from north boundary, roughly 15' south)
    rear_y = LOT_BOUNDARY[15][1] - SETBACKS[:rear]  # NE corner Y minus rear
    ents.add_edges(
      SeacoveHelpers.pt(SETBACKS[:side_west], rear_y, 0.15),
      SeacoveHelpers.pt(LOT_BOUNDARY[15][0] - SETBACKS[:side_east], rear_y, 0.15)
    )

    # West side setback (5' from west PL)
    ents.add_edges(
      SeacoveHelpers.pt(SETBACKS[:side_west], front_y, 0.15),
      SeacoveHelpers.pt(SETBACKS[:side_west], rear_y, 0.15)
    )

    # East side setback (10' from east PL — corner lot)
    east_x = LOT_BOUNDARY[9][0] - SETBACKS[:side_east]
    ents.add_edges(
      SeacoveHelpers.pt(east_x, front_y, 0.15),
      SeacoveHelpers.pt(east_x, rear_y, 0.15)
    )

    model.commit_operation
    puts "Setbacks: front=#{SETBACKS[:front]}' rear=#{SETBACKS[:rear]}' " \
         "east=#{SETBACKS[:side_east]}' west=#{SETBACKS[:side_west]}'"
    group
  end

  def self.build_house(model = nil, tags = nil)
    model ||= Sketchup.active_model
    tags ||= setup_tags(model)
    model.start_operation("Site - House Footprint", true)

    group = model.entities.add_group
    group.name = "site-house-footprint"
    group.layer = get_tag(model, tags, "House Footprint")

    ents = group.entities
    ox, oy = HOUSE_X, HOUSE_Y

    # Living wing
    lw = LIVING_WING
    f1 = ents.add_face(
      SeacoveHelpers.pt(ox + lw[:x],        oy + lw[:y],        0.05),
      SeacoveHelpers.pt(ox + lw[:x] + lw[:w], oy + lw[:y],        0.05),
      SeacoveHelpers.pt(ox + lw[:x] + lw[:w], oy + lw[:y] + lw[:d], 0.05),
      SeacoveHelpers.pt(ox + lw[:x],        oy + lw[:y] + lw[:d], 0.05)
    )
    if f1
      mat = model.materials.add("House_Footprint_Pass2")
      mat.color = Sketchup::Color.new(185, 165, 145, 170)
      f1.material = mat
    end

    # Bedroom wing
    bw = BEDROOM_WING
    f2 = ents.add_face(
      SeacoveHelpers.pt(ox + bw[:x],        oy + bw[:y],        0.05),
      SeacoveHelpers.pt(ox + bw[:x] + bw[:w], oy + bw[:y],        0.05),
      SeacoveHelpers.pt(ox + bw[:x] + bw[:w], oy + bw[:y] + bw[:d], 0.05),
      SeacoveHelpers.pt(ox + bw[:x],        oy + bw[:y] + bw[:d], 0.05)
    )
    f2.material = model.materials["House_Footprint_Pass2"] if f2

    model.commit_operation
    puts "House: offset(#{ox}', #{oy}') Living(#{lw[:w]}'x#{lw[:d]}') " \
         "Bedroom(#{bw[:w]}'x#{bw[:d]}') FF=#{FF} Ridge=#{RIDGE}"
    group
  end

  def self.build_roads(model = nil, tags = nil)
    model ||= Sketchup.active_model
    tags ||= setup_tags(model)
    model.start_operation("Site - Roads", true)

    group = model.entities.add_group
    group.name = "site-roads"
    group.layer = get_tag(model, tags, "Roads")

    ents = group.entities

    # Sea Cove Drive — 24' wide south of lot boundary
    lot_south = LOT_BOUNDARY[0..9]
    road_outer = lot_south.map { |p| [p[0], p[1] - 24.0] }
    sea_cove_pts = lot_south + road_outer.reverse
    pts = sea_cove_pts.map { |p| SeacoveHelpers.pt(p[0], p[1], -0.1) }
    f1 = ents.add_face(pts)
    if f1
      mat = model.materials.add("Road_Asphalt_P2")
      mat.color = Sketchup::Color.new(108, 108, 108)
      f1.material = mat
    end

    # Clipper Road — 30' wide east of lot boundary
    lot_east = LOT_BOUNDARY[9..15]
    road_east = lot_east.map { |p| [p[0] + 30.0, p[1]] }
    clipper_pts = lot_east + road_east.reverse
    pts2 = clipper_pts.map { |p| SeacoveHelpers.pt(p[0], p[1], -0.1) }
    f2 = ents.add_face(pts2)
    if f2
      mat2 = model.materials.add("Road_Clipper_P2")
      mat2.color = Sketchup::Color.new(102, 102, 102)
      f2.material = mat2
    end

    model.commit_operation
    puts "Roads: Sea Cove Dr (24' wide cul-de-sac) + Clipper Rd (30' wide)"
    group
  end

  def self.build_driveways(model = nil, tags = nil)
    model ||= Sketchup.active_model
    tags ||= setup_tags(model)
    model.start_operation("Site - Driveways", true)

    group = model.entities.add_group
    group.name = "site-driveways"
    group.layer = get_tag(model, tags, "Driveways")

    ents = group.entities

    # North driveway
    pts = NORTH_DRIVEWAY.map { |p| SeacoveHelpers.pt(p[0], p[1], 0.03) }
    f1 = ents.add_face(pts)
    if f1
      mat = model.materials.add("Driveway_Conc")
      mat.color = Sketchup::Color.new(195, 195, 190)
      f1.material = mat
    end

    # South driveway
    pts2 = SOUTH_DRIVEWAY.map { |p| SeacoveHelpers.pt(p[0], p[1], 0.02) }
    f2 = ents.add_face(pts2)
    f2.material = model.materials["Driveway_Conc"] if f2

    model.commit_operation
    puts "Driveways: north (E-W to Clipper) + south (curves from Sea Cove)"
    group
  end

  def self.build_pool_cabana(model = nil, tags = nil)
    model ||= Sketchup.active_model
    tags ||= setup_tags(model)
    model.start_operation("Site - Pool & Cabana", true)

    group = model.entities.add_group
    group.name = "site-pool-cabana"
    group.layer = get_tag(model, tags, "Pool & Cabana")

    ents = group.entities

    # Pool
    p = POOL
    f1 = ents.add_face(
      SeacoveHelpers.pt(p[:x],        p[:y],        0.04),
      SeacoveHelpers.pt(p[:x] + p[:w], p[:y],        0.04),
      SeacoveHelpers.pt(p[:x] + p[:w], p[:y] + p[:d], 0.04),
      SeacoveHelpers.pt(p[:x],        p[:y] + p[:d], 0.04)
    )
    if f1
      mat = model.materials.add("Pool_Water")
      mat.color = Sketchup::Color.new(100, 160, 210, 180)
      f1.material = mat
    end

    # Cabana
    c = CABANA
    f2 = ents.add_face(
      SeacoveHelpers.pt(c[:x],        c[:y],        0.04),
      SeacoveHelpers.pt(c[:x] + c[:w], c[:y],        0.04),
      SeacoveHelpers.pt(c[:x] + c[:w], c[:y] + c[:d], 0.04),
      SeacoveHelpers.pt(c[:x],        c[:y] + c[:d], 0.04)
    )
    if f2
      mat2 = model.materials.add("Cabana_Roof")
      mat2.color = Sketchup::Color.new(160, 140, 120, 200)
      f2.material = mat2
    end

    model.commit_operation
    puts "Pool: #{p[:w]}'x#{p[:d]}' at (#{p[:x]}, #{p[:y]})"
    puts "Cabana: #{c[:w]}'x#{c[:d]}' at (#{c[:x]}, #{c[:y]})"
    group
  end

  def self.build_spot_elevations(model = nil, tags = nil)
    model ||= Sketchup.active_model
    tags ||= setup_tags(model)
    model.start_operation("Site - Spot Elevations", true)

    group = model.entities.add_group
    group.name = "site-spot-elevations"
    group.layer = get_tag(model, tags, "Spot Elevations")

    ents = group.entities

    # Place each elevation as a construction point with a small marker
    SPOT_ELEVATIONS.each do |elev|
      x, y, z, label = elev
      # Construction point at XY position, Z = 0 (flat site plan)
      # The elevation value is stored in the label, not as actual Z height
      # (for site plan view, everything is flat)
      cp = ents.add_cpoint(SeacoveHelpers.pt(x, y, 0.1))

      # For key elevations, also place at actual Z for 3D topo view
      if label == "FF" || label == "RIDGE" || label == "EAVE"
        ents.add_cpoint(SeacoveHelpers.pt(x, y, z - FF + 0.1))
      end
    end

    model.commit_operation
    puts "Spot elevations: #{SPOT_ELEVATIONS.length} points placed"
    puts "  Range: #{SPOT_ELEVATIONS.map{|e| e[2]}.min} to #{SPOT_ELEVATIONS.map{|e| e[2]}.max}"
    group
  end

  def self.build_walls_fences(model = nil, tags = nil)
    model ||= Sketchup.active_model
    tags ||= setup_tags(model)
    model.start_operation("Site - Walls & Fences", true)

    group = model.entities.add_group
    group.name = "site-walls-fences"
    group.layer = get_tag(model, tags, "Walls & Fences")

    ents = group.entities

    WALLS_AND_FENCES.each_with_index do |wall, i|
      fx, fy, tx, ty, wtype, height = wall
      wall_grp = ents.add_group
      wall_grp.name = "site-wall-#{wtype}-#{i + 1}"

      thickness = (wtype == "conc_wall") ? 0.5 : 0.1  # feet
      SeacoveHelpers.make_wall(wall_grp, [fx, fy], [tx, ty], thickness, height, 0)

      if wtype == "conc_wall"
        mat = model.materials["Conc_Wall"] || model.materials.add("Conc_Wall")
        mat.color = Sketchup::Color.new(170, 170, 165) unless mat.color
        wall_grp.material = mat
      else
        mat = model.materials["Chain_Link"] || model.materials.add("Chain_Link")
        mat.color = Sketchup::Color.new(160, 160, 160, 100) unless mat.color
        wall_grp.material = mat
      end
    end

    model.commit_operation
    puts "Walls & fences: #{WALLS_AND_FENCES.length} segments"
    group
  end

  # ==========================================================================
  # BUILD ALL
  # ==========================================================================
  def self.build_all
    model = Sketchup.active_model
    tags = setup_tags(model)

    build_lot(model, tags)
    build_setbacks(model, tags)
    build_house(model, tags)
    build_roads(model, tags)
    build_driveways(model, tags)
    build_pool_cabana(model, tags)
    build_spot_elevations(model, tags)
    build_walls_fences(model, tags)

    model.active_view.zoom_extents
    puts "\n=== SITE PLAN PASS 2 COMPLETE ==="
    puts "Tag folder: Site/ with #{tags.length} sub-tags"
    puts "Toggle tags to show/hide layers"
    puts ""
    puts "Compare against survey PDF. What needs correction?"
    puts "Each element can be rebuilt independently."
  end

  # Build incrementally — one element at a time
  def self.build_next
    @queue ||= [
      :build_lot, :build_setbacks, :build_house, :build_roads,
      :build_driveways, :build_pool_cabana, :build_spot_elevations,
      :build_walls_fences
    ]
    item = @queue.shift
    return puts "All site elements built." unless item
    model = Sketchup.active_model
    tags = setup_tags(model)
    send(item, model, tags)
    model.active_view.zoom_extents
    puts "--- #{@queue.length} elements remaining. Call .build_next ---"
  end

end

puts "SeacoveSite2 loaded. PASS 2 — comprehensive site plan."
puts "  .build_all        — everything at once"
puts "  .build_next       — one element at a time"
puts "  .build_lot        — lot boundary only"
puts "  .build_house      — house footprint only"
puts "  .build_roads      — roads only"
puts "  .build_setbacks   — setback lines only"
puts ""
puts "Load with:"
puts "  load '#{__FILE__}'"
