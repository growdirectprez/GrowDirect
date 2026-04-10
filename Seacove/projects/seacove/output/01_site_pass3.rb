# 01_site_pass3.rb — Pass 3: Corrected proportions from survey comparison
# Source: IWS Surveying Boundary/Topographic Survey, June 20, 2018
# 25 Sea Cove Drive, RPV — Tract #14649, Lot 69
#
# PASS 3 CORRECTIONS FROM PASS 2:
#   - Tighter cul-de-sac arc (true radius curve)
#   - East boundary angles more steeply NNE along Clipper
#   - Pool moved: now directly WEST of house, aligned with south half
#   - Cabana: west of pool, near west PL
#   - North driveway: angled strip from house N side to Clipper Rd (flat, not box)
#   - South driveway: tighter curve in SW corner
#   - House shifted slightly east (more centered in lot)
#   - Walls reduced in height and prominence
#   - Materials softened — less contrast
#
# Usage:
#   load '/Users/gclyle/GrowDirect/ARC/projects/seacove/output/00_helpers.rb'
#   load '/Users/gclyle/GrowDirect/ARC/projects/seacove/output/01_site_pass3.rb'
#   SeacoveSite3.build_all

module SeacoveSite3

  # ==========================================================================
  # LOT BOUNDARY — Lot 69, Tract 14649
  # ==========================================================================
  # Refined from pass 2. Key changes:
  #   - Cul-de-sac arc is tighter (shorter radius, deeper curve)
  #   - East boundary has steeper angle (Clipper Rd runs ~N17E)
  #   - North boundary slight westward slope
  #   - Overall: ~100' wide at north, ~128' deep on west, ~120' on east
  # ==========================================================================

  LOT_BOUNDARY = [
    # --- SW CORNER (origin) ---
    [0.0, 0.0],

    # --- SOUTH BOUNDARY — Sea Cove Dr cul-de-sac ---
    # Tighter arc. Cul-de-sac radius ~50'. The curve bulges south.
    # Arc deepest point is about 15' south of the SW-SE line.
    [8.0, -3.0],
    [16.0, -7.0],
    [24.0, -11.0],
    [32.0, -14.0],
    [40.0, -15.0],         # deepest point of arc
    [48.0, -14.0],
    [56.0, -11.0],
    [64.0, -7.0],
    [72.0, -2.0],

    # --- SE CORNER — Sea Cove meets Clipper Rd ---
    [78.0, 5.0],

    # --- EAST BOUNDARY — Clipper Road (runs ~N17E) ---
    # Steeper angle than pass 2. Clipper Rd angles NNE.
    [80.0, 25.0],
    [82.0, 45.0],
    [84.0, 65.0],
    [86.0, 85.0],
    [88.0, 105.0],

    # --- NE CORNER ---
    [90.0, 120.0],

    # --- NORTH BOUNDARY — shared with Lot 70 ---
    # Slight angle, drops ~2' west to east
    [60.0, 122.0],
    [30.0, 124.0],

    # --- NW CORNER ---
    [0.0, 125.0],

    # Closes to SW corner automatically
  ]

  CORNERS = {
    "SW" => [0.0, 0.0],
    "SE" => [78.0, 5.0],
    "NE" => [90.0, 120.0],
    "NW" => [0.0, 125.0],
  }

  # ==========================================================================
  # HOUSE FOOTPRINT — shifted east from pass 2
  # ==========================================================================
  # Survey shows house roughly centered E-W in lot.
  # ~25' from west PL, ~15' from east PL (at house latitude)
  # ~30' from south PL (straight line, not counting cul-de-sac dip)
  HOUSE_X = 25.0
  HOUSE_Y = 30.0

  # Living wing: south portion, runs E-W
  LIVING_W = 22.5
  LIVING_D = 22.83

  # Bedroom/service wing: east portion, runs N-S
  BEDROOM_W = 19.17
  BEDROOM_D = 44.0

  FF    = 100.00
  RIDGE = 108.82
  EAVE  = 106.82

  # ==========================================================================
  # POOL — directly WEST of house, aligned with house south half
  # ==========================================================================
  # Survey shows pool between house and west PL.
  # Gap between house and pool: ~6'
  # Pool aligned with roughly the south 2/3 of the house
  POOL_X = 6.0
  POOL_Y = 32.0       # aligned with house south edge + a bit
  POOL_W = 13.0        # E-W dimension
  POOL_D = 26.0        # N-S dimension

  # ==========================================================================
  # CABANA — west of pool, near west PL
  # ==========================================================================
  CABANA_X = 2.0
  CABANA_Y = 48.0      # aligned with north half of pool
  CABANA_W = 10.0
  CABANA_D = 14.0

  # ==========================================================================
  # NORTH DRIVEWAY — angled strip from house to Clipper Rd
  # ==========================================================================
  # Runs from N side of house (x~35, y~74) northeast to Clipper (x~88, y~105)
  # About 12' wide
  NORTH_DRIVEWAY = [
    [35.0, 76.0],         # SW corner (near house)
    [88.0, 100.0],        # SE corner (at Clipper)
    [88.0, 112.0],        # NE corner (at Clipper)
    [35.0, 88.0],         # NW corner (near house)
  ]

  # ==========================================================================
  # SOUTH DRIVEWAY — in SW area, curves from Sea Cove Dr
  # ==========================================================================
  SOUTH_DRIVEWAY = [
    [0.0, -4.0],          # entrance at Sea Cove Dr, near SW corner
    [6.0, -2.0],          # along road edge
    [10.0, 4.0],          # turning north into property
    [12.0, 14.0],         # reaching property level
    [8.0, 18.0],          # top of driveway
    [0.0, 16.0],          # west edge
    [-2.0, 8.0],          # angling back
    [-4.0, 0.0],          # back toward road
  ]

  # ==========================================================================
  # CONCRETE AREAS (patios, walkways)
  # ==========================================================================
  # Concrete area south of house (between house and Sea Cove)
  CONC_SOUTH = [
    [25.0, 22.0],
    [63.0, 22.0],
    [63.0, 30.0],
    [25.0, 30.0],
  ]

  # Concrete area east of house (between house and Clipper)
  CONC_EAST = [
    [63.0, 30.0],
    [80.0, 30.0],
    [80.0, 60.0],
    [63.0, 60.0],
  ]

  # Concrete pool deck (surrounds pool)
  CONC_POOL_DECK = [
    [3.0, 28.0],
    [22.0, 28.0],
    [22.0, 62.0],
    [3.0, 62.0],
  ]

  # ==========================================================================
  # WALLS AND FENCES — reduced height from pass 2
  # ==========================================================================
  WALLS_AND_FENCES = [
    # [from_x, from_y, to_x, to_y, type, height_ft]
    # Concrete walls along south (near Sea Cove Dr) — low retaining walls
    [30.0, 8.0,   65.0, 4.0,   "conc_wall", 2.0],

    # Concrete wall near Clipper Rd (east side)
    [76.0, 10.0,  82.0, 35.0,  "conc_wall", 2.0],

    # Concrete wall — between north driveway and landscaping
    [35.0, 75.0,  86.0, 98.0,  "conc_wall", 1.5],

    # Chain link fence — west boundary
    [0.0, 18.0,   0.0, 65.0,   "chain_link", 4.0],
  ]

  # ==========================================================================
  # SPOT ELEVATIONS — refined positions from survey study
  # ==========================================================================
  SPOT_ELEVATIONS = [
    # [x, y, elevation, label]

    # --- House reference ---
    [40.0, 48.0, 100.00, "FF"],

    # --- North area (toward Lot 70) ---
    [50.0, 112.0, 104.12, nil],
    [70.0, 115.0, 103.59, nil],
    [85.0, 118.0, 102.41, nil],
    [55.0, 120.0, 104.61, nil],
    [40.0, 105.0, 100.30, nil],
    [50.0, 100.0, 100.12, nil],

    # --- North driveway area ---
    [60.0, 88.0,  100.12, "CONC"],
    [75.0, 95.0,  100.30, "CONC"],
    [85.0, 105.0, 100.40, "CONC"],

    # --- East area (Clipper Rd) ---
    [86.0, 95.0,  101.85, nil],
    [88.0, 110.0, 100.85, "E/P"],
    [84.0, 60.0,  99.04, nil],
    [82.0, 35.0,  98.25, nil],
    [80.0, 15.0,  96.30, nil],
    [79.0, 8.0,   95.04, "E/P"],
    [85.0, 50.0,  98.21, "TW"],

    # --- South area (house to Sea Cove Dr) ---
    [40.0, 24.0,  100.14, nil],
    [45.0, 18.0,  98.60, nil],
    [50.0, 16.0,  98.42, nil],
    [55.0, 14.0,  98.50, "24\" PALM"],
    [45.0, 10.0,  98.10, nil],
    [55.0, 5.0,   98.04, nil],
    [45.0, 0.0,   97.62, nil],
    [55.0, -2.0,  97.34, nil],
    [60.0, -6.0,  96.91, nil],
    [68.0, -3.0,  95.40, nil],
    [50.0, 6.0,   98.21, "TW"],

    # --- West area (pool/cabana) ---
    [8.0, 55.0,   98.63, "CONC"],
    [10.0, 45.0,  98.55, "CONC"],
    [10.0, 35.0,  98.50, "CONC"],
    [5.0, 62.0,   98.31, nil],
    [12.0, 40.0,  98.22, "CONC"],
    [5.0, 30.0,   98.04, nil],
    [3.0, 68.0,   98.25, "ELEC HYDR"],
    [4.0, 75.0,   98.06, nil],

    # --- SW area ---
    [2.0, 22.0,   96.24, nil],
    [0.0, 16.0,   96.03, nil],
    [-2.0, 8.0,   95.54, nil],
    [-3.0, 3.0,   94.95, nil],
    [5.0, -3.0,   93.54, "CONC"],
    [0.0, -6.0,   93.40, "CONC"],
    [-4.0, -2.0,  92.60, nil],
  ]

  # ==========================================================================
  # SETBACKS (RPV residential, estimated)
  # ==========================================================================
  SETBACKS = { front: 20.0, rear: 15.0, east: 10.0, west: 5.0 }

  # ==========================================================================
  # BUILD METHODS
  # ==========================================================================

  def self.setup_tags(model)
    tags = {}
    begin
      folder = model.layers.add_folder("Site")
      names = [
        "Lot Boundary", "Setbacks", "House Footprint", "Roads",
        "Driveways", "Pool", "Cabana", "Concrete",
        "Spot Elevations", "Walls & Fences", "Landscaping"
      ]
      names.each do |n|
        t = model.layers.add(n)
        folder.add_layer(t) if folder.respond_to?(:add_layer)
        tags[n] = t
      end
    rescue
      names = ["Lot Boundary", "Setbacks", "House Footprint", "Roads",
               "Driveways", "Pool", "Cabana", "Concrete",
               "Spot Elevations", "Walls & Fences", "Landscaping"]
      names.each { |n| tags[n] = model.layers[n] || model.layers.add(n) }
    end
    tags
  end

  def self.tag(model, tags, name)
    tags[name] || model.layers[name] || model.layers.add(name)
  end

  def self.make_material(model, name, r, g, b, a = 255)
    mat = model.materials[name]
    unless mat
      mat = model.materials.add(name)
      mat.color = Sketchup::Color.new(r, g, b, a)
    end
    mat
  end

  # --- Lot Boundary ---
  def self.build_lot(model, tags)
    model.start_operation("Site - Lot Boundary", true)

    grp = model.entities.add_group
    grp.name = "site-lot-boundary"
    grp.layer = tag(model, tags, "Lot Boundary")

    pts = LOT_BOUNDARY.map { |p| SeacoveHelpers.pt(p[0], p[1], 0) }
    face = grp.entities.add_face(pts)
    if face
      face.material = make_material(model, "Lot_Ground", 200, 215, 180, 100)
      face.back_material = make_material(model, "Lot_Ground_Back", 180, 195, 160)
    end

    # Corner markers
    CORNERS.each do |label, coords|
      m = model.entities.add_group
      m.name = "site-corner-#{label}"
      m.layer = tag(model, tags, "Lot Boundary")
      x, y = coords
      s = 1.5
      m.entities.add_edges(
        SeacoveHelpers.pt(x-s, y-s, 0.15), SeacoveHelpers.pt(x+s, y+s, 0.15))
      m.entities.add_edges(
        SeacoveHelpers.pt(x+s, y-s, 0.15), SeacoveHelpers.pt(x-s, y+s, 0.15))
      m.entities.add_circle(
        SeacoveHelpers.pt(x, y, 0.15), Geom::Vector3d.new(0,0,1),
        SeacoveHelpers.ft(s), 16)
    end

    model.commit_operation
    puts "  Lot boundary: #{LOT_BOUNDARY.length} pts, 4 corners"
  end

  # --- Setback Lines ---
  def self.build_setbacks(model, tags)
    model.start_operation("Site - Setbacks", true)

    grp = model.entities.add_group
    grp.name = "site-setbacks"
    grp.layer = tag(model, tags, "Setbacks")

    z = 0.12
    f = SETBACKS[:front]
    r = CORNERS["NW"][1] - SETBACKS[:rear]
    w = SETBACKS[:west]
    e = CORNERS["SE"][0] - SETBACKS[:east]

    # Front (south)
    grp.entities.add_edges(SeacoveHelpers.pt(w, f, z), SeacoveHelpers.pt(e, f, z))
    # Rear (north)
    grp.entities.add_edges(SeacoveHelpers.pt(w, r, z), SeacoveHelpers.pt(e, r, z))
    # West
    grp.entities.add_edges(SeacoveHelpers.pt(w, f, z), SeacoveHelpers.pt(w, r, z))
    # East
    grp.entities.add_edges(SeacoveHelpers.pt(e, f, z), SeacoveHelpers.pt(e, r, z))

    model.commit_operation
    puts "  Setbacks: F=#{SETBACKS[:front]}' R=#{SETBACKS[:rear]}' E=#{SETBACKS[:east]}' W=#{SETBACKS[:west]}'"
  end

  # --- House Footprint ---
  def self.build_house(model, tags)
    model.start_operation("Site - House", true)

    grp = model.entities.add_group
    grp.name = "site-house-footprint"
    grp.layer = tag(model, tags, "House Footprint")

    mat = make_material(model, "House_FP", 175, 155, 135, 160)
    ox, oy = HOUSE_X, HOUSE_Y

    # Living wing
    f1 = grp.entities.add_face(
      SeacoveHelpers.pt(ox, oy, 0.05),
      SeacoveHelpers.pt(ox + LIVING_W, oy, 0.05),
      SeacoveHelpers.pt(ox + LIVING_W, oy + LIVING_D, 0.05),
      SeacoveHelpers.pt(ox, oy + LIVING_D, 0.05))
    f1.material = mat if f1

    # Bedroom wing
    bx = ox + LIVING_W
    f2 = grp.entities.add_face(
      SeacoveHelpers.pt(bx, oy, 0.05),
      SeacoveHelpers.pt(bx + BEDROOM_W, oy, 0.05),
      SeacoveHelpers.pt(bx + BEDROOM_W, oy + BEDROOM_D, 0.05),
      SeacoveHelpers.pt(bx, oy + BEDROOM_D, 0.05))
    f2.material = mat if f2

    model.commit_operation
    east_edge = ox + LIVING_W + BEDROOM_W
    puts "  House: (#{ox}',#{oy}') to (#{east_edge}',#{oy + BEDROOM_D}') L-shape"
  end

  # --- Roads ---
  def self.build_roads(model, tags)
    model.start_operation("Site - Roads", true)

    grp = model.entities.add_group
    grp.name = "site-roads"
    grp.layer = tag(model, tags, "Roads")

    road_mat = make_material(model, "Asphalt", 105, 105, 105)

    # Sea Cove Drive — 24' south of lot boundary arc
    lot_s = LOT_BOUNDARY[0..10]  # SW through SE
    road_outer = lot_s.map { |p| [p[0], p[1] - 24.0] }
    pts = (lot_s + road_outer.reverse).map { |p| SeacoveHelpers.pt(p[0], p[1], -0.15) }
    f1 = grp.entities.add_face(pts)
    f1.material = road_mat if f1

    # Clipper Road — 28' east of lot boundary
    lot_e = LOT_BOUNDARY[10..15]  # SE through NE
    road_e = lot_e.map { |p| [p[0] + 28.0, p[1]] }
    pts2 = (lot_e + road_e.reverse).map { |p| SeacoveHelpers.pt(p[0], p[1], -0.15) }
    f2 = grp.entities.add_face(pts2)
    f2.material = road_mat if f2

    model.commit_operation
    puts "  Roads: Sea Cove Dr (24' wide) + Clipper Rd (28' wide)"
  end

  # --- Driveways ---
  def self.build_driveways(model, tags)
    model.start_operation("Site - Driveways", true)

    grp = model.entities.add_group
    grp.name = "site-driveways"
    grp.layer = tag(model, tags, "Driveways")

    conc_mat = make_material(model, "Concrete_Driveway", 190, 190, 185)

    # North driveway — flat polygon
    pts = NORTH_DRIVEWAY.map { |p| SeacoveHelpers.pt(p[0], p[1], 0.03) }
    f1 = grp.entities.add_face(pts)
    f1.material = conc_mat if f1

    # South driveway
    pts2 = SOUTH_DRIVEWAY.map { |p| SeacoveHelpers.pt(p[0], p[1], 0.02) }
    f2 = grp.entities.add_face(pts2)
    f2.material = conc_mat if f2

    model.commit_operation
    puts "  Driveways: north (to Clipper) + south (from Sea Cove)"
  end

  # --- Pool ---
  def self.build_pool(model, tags)
    model.start_operation("Site - Pool", true)

    grp = model.entities.add_group
    grp.name = "site-pool"
    grp.layer = tag(model, tags, "Pool")

    pool_mat = make_material(model, "Pool_Water", 90, 150, 200, 170)

    f = grp.entities.add_face(
      SeacoveHelpers.pt(POOL_X, POOL_Y, 0.04),
      SeacoveHelpers.pt(POOL_X + POOL_W, POOL_Y, 0.04),
      SeacoveHelpers.pt(POOL_X + POOL_W, POOL_Y + POOL_D, 0.04),
      SeacoveHelpers.pt(POOL_X, POOL_Y + POOL_D, 0.04))
    f.material = pool_mat if f

    model.commit_operation
    puts "  Pool: #{POOL_W}'x#{POOL_D}' at (#{POOL_X}', #{POOL_Y}')"
  end

  # --- Cabana ---
  def self.build_cabana(model, tags)
    model.start_operation("Site - Cabana", true)

    grp = model.entities.add_group
    grp.name = "site-cabana"
    grp.layer = tag(model, tags, "Cabana")

    cab_mat = make_material(model, "Cabana_Structure", 155, 140, 120, 190)

    f = grp.entities.add_face(
      SeacoveHelpers.pt(CABANA_X, CABANA_Y, 0.04),
      SeacoveHelpers.pt(CABANA_X + CABANA_W, CABANA_Y, 0.04),
      SeacoveHelpers.pt(CABANA_X + CABANA_W, CABANA_Y + CABANA_D, 0.04),
      SeacoveHelpers.pt(CABANA_X, CABANA_Y + CABANA_D, 0.04))
    f.material = cab_mat if f

    model.commit_operation
    puts "  Cabana: #{CABANA_W}'x#{CABANA_D}' at (#{CABANA_X}', #{CABANA_Y}')"
  end

  # --- Concrete Areas ---
  def self.build_concrete(model, tags)
    model.start_operation("Site - Concrete", true)

    grp = model.entities.add_group
    grp.name = "site-concrete"
    grp.layer = tag(model, tags, "Concrete")

    conc_mat = make_material(model, "Concrete_Patio", 195, 195, 190, 140)

    [CONC_SOUTH, CONC_EAST, CONC_POOL_DECK].each_with_index do |poly, i|
      pts = poly.map { |p| SeacoveHelpers.pt(p[0], p[1], 0.02) }
      f = grp.entities.add_face(pts)
      f.material = conc_mat if f
    end

    model.commit_operation
    puts "  Concrete: 3 patio/walkway areas"
  end

  # --- Walls & Fences ---
  def self.build_walls(model, tags)
    model.start_operation("Site - Walls & Fences", true)

    grp = model.entities.add_group
    grp.name = "site-walls-fences"
    grp.layer = tag(model, tags, "Walls & Fences")

    WALLS_AND_FENCES.each_with_index do |w, i|
      fx, fy, tx, ty, wtype, ht = w
      wg = grp.entities.add_group
      wg.name = "site-#{wtype}-#{i+1}"

      thick = (wtype == "conc_wall") ? 0.5 : 0.08
      SeacoveHelpers.make_wall(wg, [fx, fy], [tx, ty], thick, ht, 0)

      if wtype == "conc_wall"
        wg.material = make_material(model, "Conc_Wall_Site", 165, 165, 160)
      else
        wg.material = make_material(model, "Chain_Link_Site", 150, 150, 150, 80)
      end
    end

    model.commit_operation
    puts "  Walls & fences: #{WALLS_AND_FENCES.length} segments"
  end

  # --- Spot Elevations ---
  def self.build_elevations(model, tags)
    model.start_operation("Site - Spot Elevations", true)

    grp = model.entities.add_group
    grp.name = "site-spot-elevations"
    grp.layer = tag(model, tags, "Spot Elevations")

    SPOT_ELEVATIONS.each do |e|
      x, y, elev, label = e
      grp.entities.add_cpoint(SeacoveHelpers.pt(x, y, 0.08))
    end

    model.commit_operation
    elevs = SPOT_ELEVATIONS.map { |e| e[2] }
    puts "  Spot elevations: #{SPOT_ELEVATIONS.length} points (#{elevs.min} to #{elevs.max})"
  end

  # ==========================================================================
  # BUILD ALL / BUILD NEXT
  # ==========================================================================
  # --- Dimensions ---
  def self.build_dimensions(model, tags)
    model.start_operation("Site - Dimensions", true)

    grp = model.entities.add_group
    grp.name = "site-dimensions"
    begin
      folder = model.layers.folders.find { |f| f.name == "Site" }
      t = model.layers.add("Dimensions")
      folder.add_layer(t) if folder && folder.respond_to?(:add_layer)
      grp.layer = t
    rescue
      grp.layer = model.layers["Dimensions"] || model.layers.add("Dimensions")
    end

    ents = grp.entities

    # --- Property line dimensions ---
    # West boundary: NW to SW
    nw = CORNERS["NW"]
    sw = CORNERS["SW"]
    ents.add_dimension_linear(
      SeacoveHelpers.pt(sw[0], sw[1], 0),
      SeacoveHelpers.pt(nw[0], nw[1], 0),
      Geom::Vector3d.new(-SeacoveHelpers.ft(5), 0, 0)  # 5' offset west
    )

    # North boundary: NW to NE
    ne = CORNERS["NE"]
    ents.add_dimension_linear(
      SeacoveHelpers.pt(nw[0], nw[1], 0),
      SeacoveHelpers.pt(ne[0], ne[1], 0),
      Geom::Vector3d.new(0, SeacoveHelpers.ft(5), 0)  # 5' offset north
    )

    # East boundary: NE to SE
    se = CORNERS["SE"]
    ents.add_dimension_linear(
      SeacoveHelpers.pt(ne[0], ne[1], 0),
      SeacoveHelpers.pt(se[0], se[1], 0),
      Geom::Vector3d.new(SeacoveHelpers.ft(5), 0, 0)  # 5' offset east
    )

    # South chord: SW to SE (straight-line distance across cul-de-sac)
    ents.add_dimension_linear(
      SeacoveHelpers.pt(sw[0], sw[1], 0),
      SeacoveHelpers.pt(se[0], se[1], 0),
      Geom::Vector3d.new(0, -SeacoveHelpers.ft(8), 0)  # 8' offset south
    )

    # --- House dimensions ---
    ox, oy = HOUSE_X, HOUSE_Y

    # Living wing width
    ents.add_dimension_linear(
      SeacoveHelpers.pt(ox, oy, 0),
      SeacoveHelpers.pt(ox + LIVING_W, oy, 0),
      Geom::Vector3d.new(0, -SeacoveHelpers.ft(3), 0)
    )

    # Living wing depth
    ents.add_dimension_linear(
      SeacoveHelpers.pt(ox, oy, 0),
      SeacoveHelpers.pt(ox, oy + LIVING_D, 0),
      Geom::Vector3d.new(-SeacoveHelpers.ft(3), 0, 0)
    )

    # Bedroom wing width
    bx = ox + LIVING_W
    ents.add_dimension_linear(
      SeacoveHelpers.pt(bx, oy, 0),
      SeacoveHelpers.pt(bx + BEDROOM_W, oy, 0),
      Geom::Vector3d.new(0, -SeacoveHelpers.ft(3), 0)
    )

    # Bedroom wing depth
    ents.add_dimension_linear(
      SeacoveHelpers.pt(bx + BEDROOM_W, oy, 0),
      SeacoveHelpers.pt(bx + BEDROOM_W, oy + BEDROOM_D, 0),
      Geom::Vector3d.new(SeacoveHelpers.ft(3), 0, 0)
    )

    # --- Setback distances from house to property lines ---

    # House to west PL
    ents.add_dimension_linear(
      SeacoveHelpers.pt(0, oy + LIVING_D / 2, 0),
      SeacoveHelpers.pt(ox, oy + LIVING_D / 2, 0),
      Geom::Vector3d.new(0, -SeacoveHelpers.ft(2), 0)
    )

    # House to east PL (at house latitude, interpolate east boundary)
    house_east = ox + LIVING_W + BEDROOM_W
    east_at_house = 83.0  # interpolated east PL x at house y
    ents.add_dimension_linear(
      SeacoveHelpers.pt(house_east, oy + BEDROOM_D / 2, 0),
      SeacoveHelpers.pt(east_at_house, oy + BEDROOM_D / 2, 0),
      Geom::Vector3d.new(0, SeacoveHelpers.ft(2), 0)
    )

    # House to south PL (straight line, not cul-de-sac)
    ents.add_dimension_linear(
      SeacoveHelpers.pt(ox + LIVING_W / 2, 0, 0),
      SeacoveHelpers.pt(ox + LIVING_W / 2, oy, 0),
      Geom::Vector3d.new(-SeacoveHelpers.ft(2), 0, 0)
    )

    # House to north PL
    ents.add_dimension_linear(
      SeacoveHelpers.pt(ox + LIVING_W / 2, oy + BEDROOM_D, 0),
      SeacoveHelpers.pt(ox + LIVING_W / 2, CORNERS["NW"][1], 0),
      Geom::Vector3d.new(-SeacoveHelpers.ft(2), 0, 0)
    )

    # --- Pool dimensions ---
    ents.add_dimension_linear(
      SeacoveHelpers.pt(POOL_X, POOL_Y, 0),
      SeacoveHelpers.pt(POOL_X + POOL_W, POOL_Y, 0),
      Geom::Vector3d.new(0, -SeacoveHelpers.ft(2), 0)
    )
    ents.add_dimension_linear(
      SeacoveHelpers.pt(POOL_X + POOL_W, POOL_Y, 0),
      SeacoveHelpers.pt(POOL_X + POOL_W, POOL_Y + POOL_D, 0),
      Geom::Vector3d.new(SeacoveHelpers.ft(2), 0, 0)
    )

    # --- Gap: house to pool ---
    ents.add_dimension_linear(
      SeacoveHelpers.pt(POOL_X + POOL_W, POOL_Y + POOL_D / 2, 0),
      SeacoveHelpers.pt(HOUSE_X, POOL_Y + POOL_D / 2, 0),
      Geom::Vector3d.new(0, SeacoveHelpers.ft(2), 0)
    )

    model.commit_operation
    puts "  Dimensions: property lines, house, pool, setback gaps"
  end

  PHASES = [
    :build_lot, :build_setbacks, :build_house, :build_roads,
    :build_driveways, :build_pool, :build_cabana, :build_concrete,
    :build_walls, :build_elevations, :build_dimensions
  ]

  def self.build_all
    model = Sketchup.active_model
    tags = setup_tags(model)

    puts "\n=== Building Seacove Site Plan — Pass 3 ==="
    PHASES.each { |phase| send(phase, model, tags) }

    model.active_view.zoom_extents
    puts "\n=== SITE PLAN PASS 3 COMPLETE ==="
    puts "#{PHASES.length} layers built. Toggle tags in Site/ folder."
    puts "Compare against survey PDF — report what needs correction."
  end

  def self.build_next
    @queue ||= PHASES.dup
    item = @queue.shift
    return puts "All site elements built." unless item
    model = Sketchup.active_model
    tags = setup_tags(model)
    send(item, model, tags)
    model.active_view.zoom_extents
    puts "--- #{@queue.length} remaining. .build_next for next ---"
  end

  def self.reset_queue
    @queue = PHASES.dup
    puts "Queue reset. #{@queue.length} phases ready."
  end
end

puts "SeacoveSite3 loaded. PASS 3."
puts "  .build_all   — everything"
puts "  .build_next  — one layer at a time"
puts ""
puts "Corrections from pass 2:"
puts "  - Tighter cul-de-sac arc"
puts "  - Pool moved west of house"
puts "  - North driveway now flat (was rendering as box)"
puts "  - Walls shorter / less prominent"
puts "  - Added concrete patio areas"
