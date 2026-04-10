# 01_site_pass4.rb — Pass 4: Precision lot + foundation layer
# Source: IWS Survey (2018), Rucker Foundation Plan (1958), Rucker Floor Plan (1958)
#
# PASS 4 — Focus on precision:
#   - Lot boundary refined using house footprint as scale calibration
#   - Foundation layer added (perimeter footings, interior footings, slab)
#   - House dimensions locked from floor plan dimension chains
#   - All coordinates verified by scripts/verify_site_plan.py
#
# Usage:
#   load '/Users/gclyle/GrowDirect/ARC/projects/seacove/output/00_helpers.rb'
#   load '/Users/gclyle/GrowDirect/ARC/projects/seacove/output/01_site_pass4.rb'
#   SeacoveSite4.build_all

module SeacoveSite4

  # ==========================================================================
  # HOUSE DIMENSIONS — HIGH CONFIDENCE (from 1958 Rucker floor plan)
  # ==========================================================================
  # Living wing (west): 22'-6" wide x 22'-10" deep
  # Bedroom wing (east): 19'-2" wide x 44'-0" deep
  # Total width: 41'-8" (22'-6" + 19'-2")
  # The L-shape: bedroom wing extends north beyond living wing by 21'-2"
  LIVING_W  = 22.5     # 22'-6"
  LIVING_D  = 22.833   # 22'-10"
  BEDROOM_W = 19.167   # 19'-2"
  BEDROOM_D = 44.0     # 44'-0"
  HOUSE_TOTAL_W = 41.667  # 41'-8"

  # ==========================================================================
  # HOUSE POSITION ON LOT — calibrated from survey
  # ==========================================================================
  # Using house as ruler on survey:
  #   West PL to house: ~0.55 x house width = ~23'
  #   House to east PL (at mid-height): ~0.4 x house width = ~17'
  #   South baseline to house: ~0.66 x house depth = ~29'
  #   House north edge to north PL: ~1.15 x house depth = ~51'
  HOUSE_X = 23.0    # feet east from SW corner to house SW corner
  HOUSE_Y = 29.0    # feet north from SW-SE baseline to house S edge

  # Derived house corners (for verification)
  # SW corner of house: (23.0, 29.0)
  # SE corner of house: (23.0 + 41.667, 29.0) = (64.667, 29.0)
  # NW corner of living: (23.0, 29.0 + 22.833) = (23.0, 51.833)
  # NE corner of bedroom: (64.667, 29.0 + 44.0) = (64.667, 73.0)

  # Key elevations (from survey — exact)
  FF    = 100.00
  RIDGE = 108.82
  EAVE  = 106.82

  # ==========================================================================
  # LOT BOUNDARY — Lot 69, Tract 14649
  # ==========================================================================
  # Calibrated: lot width at house latitude = house width + west gap + east gap
  #   = 41.67 + 23 + 17 = 81.67' → east PL at x≈82 at y=51 (house mid)
  # East boundary angles NNE (Clipper Rd), so it's x≈78 at south, x≈92 at north.
  # North boundary spans ~92' (NW at x=0, NE at x≈92)
  # West boundary is ~125' (NW at y=125, SW at y=0)
  #
  # Cul-de-sac arc: the deepest point is ~15' below the SW-SE baseline.
  # SW at (0,0), SE at approximately (78, 5) — the SE corner is slightly
  # north of the SW corner because Sea Cove curves up to meet Clipper.
  # ==========================================================================

  LOT_BOUNDARY = [
    # SW corner (origin)
    [0.0, 0.0],

    # South boundary — Sea Cove Dr cul-de-sac arc
    # Modeled as points on a circular arc, deepest ~15' below baseline
    [10.0, -3.5],
    [20.0, -7.5],
    [28.0, -11.0],
    [36.0, -13.5],
    [44.0, -14.5],     # near deepest
    [52.0, -13.5],
    [60.0, -10.0],
    [68.0, -5.0],

    # SE corner
    [78.0, 3.0],

    # East boundary — Clipper Rd (NNE, ~7° east of north)
    [80.0, 20.0],
    [82.5, 40.0],
    [85.0, 60.0],
    [87.5, 80.0],
    [89.5, 100.0],

    # NE corner
    [92.0, 120.0],

    # North boundary — shared with Lot 70 (slight westward rise)
    [61.0, 121.5],
    [30.0, 123.0],

    # NW corner
    [0.0, 124.0],

    # West boundary closes to SW (straight south)
  ]

  CORNERS = {
    "SW" => [0.0, 0.0],
    "SE" => [78.0, 3.0],
    "NE" => [92.0, 120.0],
    "NW" => [0.0, 124.0],
  }

  # ==========================================================================
  # FOUNDATION — from 1958 Rucker Foundation Plan (Page 2)
  # ==========================================================================
  # Slab on grade. 4" concrete slab.
  # Perimeter footings: 12" wide x 18" deep, 2 #4 rebar continuous
  # Interior bearing wall footings: 12" wide x 12" deep
  #
  # Foundation outline matches house footprint with footings centered
  # on wall lines. Footing paths are the centerlines.
  #
  # Foundation plan also shows:
  #   - Fireplace foundation (thicker, deeper footing mass)
  #   - Interior bearing walls (kitchen/living divider, hallway walls)

  FOOTING_WIDTH_IN = 12.0    # 12" = 1'
  FOOTING_DEPTH_IN = 18.0    # 18" = 1'-6"
  SLAB_THICKNESS_IN = 4.0    # 4"
  INTERIOR_FOOTING_DEPTH_IN = 12.0  # 12" = 1'

  # Perimeter footing path — follows house outline (L-shape)
  # These are centerline coordinates of the footing, not face of wall
  # The footing is 12" wide centered on the wall line
  PERIMETER_FOOTING = [
    # Start at SW corner of house, go clockwise
    [HOUSE_X, HOUSE_Y],                                         # house SW
    [HOUSE_X + HOUSE_TOTAL_W, HOUSE_Y],                         # house SE
    [HOUSE_X + HOUSE_TOTAL_W, HOUSE_Y + BEDROOM_D],             # bedroom NE
    [HOUSE_X + LIVING_W, HOUSE_Y + BEDROOM_D],                  # bedroom NW (inside corner)
    [HOUSE_X + LIVING_W, HOUSE_Y + LIVING_D],                   # living NE (inside corner)
    [HOUSE_X, HOUSE_Y + LIVING_D],                               # living NW
    # closes back to house SW
  ]

  # Interior bearing wall footings (estimated from foundation plan)
  # These run under the main interior walls that support the roof structure
  INTERIOR_FOOTINGS = [
    # Kitchen/living divider — runs E-W through the living wing
    { from: [HOUSE_X, HOUSE_Y + 11.0], to: [HOUSE_X + LIVING_W, HOUSE_Y + 11.0],
      label: "Kitchen/Living bearing wall" },

    # Main hallway wall — runs N-S through bedroom wing
    { from: [HOUSE_X + LIVING_W + 9.5, HOUSE_Y],
      to: [HOUSE_X + LIVING_W + 9.5, HOUSE_Y + BEDROOM_D],
      label: "Hallway bearing wall" },

    # Cross wall — bedroom dividers (E-W walls in bedroom wing)
    { from: [HOUSE_X + LIVING_W, HOUSE_Y + LIVING_D],
      to: [HOUSE_X + HOUSE_TOTAL_W, HOUSE_Y + LIVING_D],
      label: "Bedroom/service divider" },
  ]

  # Fireplace foundation — larger mass footing for the fireplace
  # Located in the living room area (estimated position)
  FIREPLACE_FOUNDATION = {
    x: HOUSE_X + 8.0,    # 8' from west wall of living wing
    y: HOUSE_Y + 5.0,    # 5' from south wall
    w: 5.0,              # 5' wide
    d: 3.0,              # 3' deep
    depth_in: 24.0,       # 24" deep (deeper than standard footings)
  }

  # Slab boundary = house footprint
  SLAB_BOUNDARY = PERIMETER_FOOTING.dup

  # ==========================================================================
  # SITE FEATURES (carried forward from pass 3, refined)
  # ==========================================================================

  # Pool — west of house
  POOL = { x: 5.0, y: 31.0, w: 14.0, d: 28.0 }

  # Cabana — west of pool
  CABANA = { x: 1.0, y: 47.0, w: 10.0, d: 14.0 }

  # North driveway — narrow strip from house NE area to Clipper Rd
  # ~10' wide concrete driveway
  NORTH_DRIVEWAY = [
    [HOUSE_X + LIVING_W + 2.0, HOUSE_Y + BEDROOM_D + 1.0],  # SW
    [HOUSE_X + LIVING_W + 2.0, HOUSE_Y + BEDROOM_D + 11.0], # NW
    [87.0, 108.0],                                            # NE (at Clipper)
    [87.0, 98.0],                                             # SE (at Clipper)
  ]

  # South driveway — curved path from Sea Cove Dr to house area
  # Stays within lot boundary
  SOUTH_DRIVEWAY = [
    [2.0, 0.0], [8.0, 2.0], [12.0, 8.0],
    [14.0, 16.0], [10.0, 20.0], [4.0, 18.0],
    [0.0, 10.0], [0.0, 0.0],
  ]

  # Concrete areas — proportional to house
  CONC_SOUTH = [
    [HOUSE_X, HOUSE_Y - 4.0],
    [HOUSE_X + HOUSE_TOTAL_W, HOUSE_Y - 4.0],
    [HOUSE_X + HOUSE_TOTAL_W, HOUSE_Y],
    [HOUSE_X, HOUSE_Y],
  ]

  CONC_EAST = [
    [HOUSE_X + HOUSE_TOTAL_W, HOUSE_Y],
    [HOUSE_X + HOUSE_TOTAL_W + 8.0, HOUSE_Y],
    [HOUSE_X + HOUSE_TOTAL_W + 8.0, HOUSE_Y + 20.0],
    [HOUSE_X + HOUSE_TOTAL_W, HOUSE_Y + 20.0],
  ]

  CONC_POOL_DECK = [
    [3.0, 29.0], [20.0, 29.0], [20.0, 61.0], [3.0, 61.0],
  ]

  # Walls and fences
  WALLS_AND_FENCES = [
    [28.0, 7.0, 68.0, 3.0, "conc_wall", 2.0],
    [76.0, 8.0, 82.0, 30.0, "conc_wall", 2.0],
    [0.0, 18.0, 0.0, 68.0, "chain_link", 4.0],
  ]

  # Spot elevations (refined positions)
  SPOT_ELEVATIONS = [
    [HOUSE_X + 15.0, HOUSE_Y + 15.0, 100.00, "FF"],
    [50.0, 112.0, 104.12, nil],
    [70.0, 115.0, 103.59, nil],
    [84.0, 118.0, 102.41, nil],
    [40.0, 105.0, 100.30, nil],
    [55.0, 120.0, 104.61, nil],
    [65.0, 88.0, 100.12, "CONC"],
    [80.0, 95.0, 100.30, "CONC"],
    [84.0, 60.0, 99.04, nil],
    [82.0, 35.0, 98.25, nil],
    [80.0, 12.0, 96.30, nil],
    [40.0, 22.0, 100.14, nil],
    [50.0, 16.0, 98.42, nil],
    [55.0, 13.0, 98.50, "PALM"],
    [45.0, 8.0, 98.10, nil],
    [45.0, 0.0, 97.62, nil],
    [60.0, -5.0, 96.91, nil],
    [10.0, 50.0, 98.55, "CONC"],
    [10.0, 38.0, 98.50, "CONC"],
    [5.0, 62.0, 98.31, nil],
    [3.0, 68.0, 98.25, nil],
    [2.0, 22.0, 96.24, nil],
    [0.0, 14.0, 96.03, nil],
    [5.0, -3.0, 93.54, "CONC"],
    [0.0, -6.0, 93.40, "CONC"],
  ]

  SETBACKS = { front: 20.0, rear: 15.0, east: 10.0, west: 5.0 }

  # ==========================================================================
  # TAG SETUP
  # ==========================================================================
  def self.setup_tags(model)
    tags = {}
    folders = {}
    begin
      site_f = model.layers.add_folder("Site")
      fnd_f = model.layers.add_folder("Foundation")
      folders["Site"] = site_f
      folders["Foundation"] = fnd_f

      site_tags = ["Lot Boundary", "Setbacks", "House Footprint", "Roads",
                   "Driveways", "Pool", "Cabana", "Concrete",
                   "Spot Elevations", "Walls & Fences", "Dimensions"]
      site_tags.each do |n|
        t = model.layers.add(n)
        site_f.add_layer(t) if site_f.respond_to?(:add_layer)
        tags[n] = t
      end

      fnd_tags = ["Perimeter Footings", "Interior Footings",
                  "Fireplace Foundation", "Slab"]
      fnd_tags.each do |n|
        t = model.layers.add(n)
        fnd_f.add_layer(t) if fnd_f.respond_to?(:add_layer)
        tags[n] = t
      end
    rescue => e
      puts "Tag folder fallback: #{e.message}"
      all_tags = ["Lot Boundary", "Setbacks", "House Footprint", "Roads",
                  "Driveways", "Pool", "Cabana", "Concrete",
                  "Spot Elevations", "Walls & Fences", "Dimensions",
                  "Perimeter Footings", "Interior Footings",
                  "Fireplace Foundation", "Slab"]
      all_tags.each { |n| tags[n] = model.layers[n] || model.layers.add(n) }
    end
    tags
  end

  def self.tag(model, tags, name)
    tags[name] || model.layers[name] || model.layers.add(name)
  end

  def self.mat(model, name, r, g, b, a = 255)
    m = model.materials[name]
    unless m
      m = model.materials.add(name)
      m.color = Sketchup::Color.new(r, g, b, a)
    end
    m
  end

  # ==========================================================================
  # SITE BUILD METHODS
  # ==========================================================================

  def self.build_lot(model, tags)
    model.start_operation("Lot Boundary", true)
    grp = model.entities.add_group
    grp.name = "site-lot-boundary"
    grp.layer = tag(model, tags, "Lot Boundary")

    pts = LOT_BOUNDARY.map { |p| SeacoveHelpers.pt(p[0], p[1], 0) }
    face = grp.entities.add_face(pts)
    face.material = mat(model, "Lot", 210, 220, 195, 60) if face

    CORNERS.each do |label, c|
      m = model.entities.add_group
      m.name = "site-corner-#{label}"
      m.layer = tag(model, tags, "Lot Boundary")
      x, y = c
      s = 1.5
      m.entities.add_edges(
        SeacoveHelpers.pt(x-s, y-s, 0.2), SeacoveHelpers.pt(x+s, y+s, 0.2))
      m.entities.add_edges(
        SeacoveHelpers.pt(x+s, y-s, 0.2), SeacoveHelpers.pt(x-s, y+s, 0.2))
      m.entities.add_circle(
        SeacoveHelpers.pt(x, y, 0.2), Geom::Vector3d.new(0,0,1),
        SeacoveHelpers.ft(s), 16)
    end
    model.commit_operation
    puts "  Lot: #{LOT_BOUNDARY.length} pts"
  end

  def self.build_setbacks(model, tags)
    model.start_operation("Setbacks", true)
    grp = model.entities.add_group
    grp.name = "site-setbacks"
    grp.layer = tag(model, tags, "Setbacks")
    z = 0.12
    f, r = SETBACKS[:front], CORNERS["NW"][1] - SETBACKS[:rear]
    w, e = SETBACKS[:west], CORNERS["SE"][0] - SETBACKS[:east]
    grp.entities.add_edges(SeacoveHelpers.pt(w, f, z), SeacoveHelpers.pt(e, f, z))
    grp.entities.add_edges(SeacoveHelpers.pt(w, r, z), SeacoveHelpers.pt(e, r, z))
    grp.entities.add_edges(SeacoveHelpers.pt(w, f, z), SeacoveHelpers.pt(w, r, z))
    grp.entities.add_edges(SeacoveHelpers.pt(e, f, z), SeacoveHelpers.pt(e, r, z))
    model.commit_operation
    puts "  Setbacks: F=#{SETBACKS[:front]}' R=#{SETBACKS[:rear]}'"
  end

  def self.build_house(model, tags)
    model.start_operation("House Footprint", true)
    grp = model.entities.add_group
    grp.name = "site-house-footprint"
    grp.layer = tag(model, tags, "House Footprint")
    house_mat = mat(model, "House_FP", 175, 155, 135, 160)
    ox, oy = HOUSE_X, HOUSE_Y

    # Living wing
    f1 = grp.entities.add_face(
      SeacoveHelpers.pt(ox, oy, 0.05),
      SeacoveHelpers.pt(ox + LIVING_W, oy, 0.05),
      SeacoveHelpers.pt(ox + LIVING_W, oy + LIVING_D, 0.05),
      SeacoveHelpers.pt(ox, oy + LIVING_D, 0.05))
    f1.material = house_mat if f1

    # Bedroom wing
    bx = ox + LIVING_W
    f2 = grp.entities.add_face(
      SeacoveHelpers.pt(bx, oy, 0.05),
      SeacoveHelpers.pt(bx + BEDROOM_W, oy, 0.05),
      SeacoveHelpers.pt(bx + BEDROOM_W, oy + BEDROOM_D, 0.05),
      SeacoveHelpers.pt(bx, oy + BEDROOM_D, 0.05))
    f2.material = house_mat if f2

    model.commit_operation
    puts "  House: (#{ox}',#{oy}') L-shape #{HOUSE_TOTAL_W}' x #{BEDROOM_D}'"
  end

  def self.build_roads(model, tags)
    model.start_operation("Roads", true)
    grp = model.entities.add_group
    grp.name = "site-roads"
    grp.layer = tag(model, tags, "Roads")
    road = mat(model, "Asphalt", 130, 130, 125, 100)

    lot_s = LOT_BOUNDARY[0..9]
    outer = lot_s.map { |p| [p[0], p[1] - 24.0] }
    pts = (lot_s + outer.reverse).map { |p| SeacoveHelpers.pt(p[0], p[1], -0.15) }
    f = grp.entities.add_face(pts)
    f.material = road if f

    lot_e = LOT_BOUNDARY[9..15]
    e_outer = lot_e.map { |p| [p[0] + 28.0, p[1]] }
    pts2 = (lot_e + e_outer.reverse).map { |p| SeacoveHelpers.pt(p[0], p[1], -0.15) }
    f2 = grp.entities.add_face(pts2)
    f2.material = road if f2

    model.commit_operation
    puts "  Roads: Sea Cove + Clipper"
  end

  def self.build_driveways(model, tags)
    model.start_operation("Driveways", true)
    grp = model.entities.add_group
    grp.name = "site-driveways"
    grp.layer = tag(model, tags, "Driveways")
    c = mat(model, "Conc_Driveway", 195, 195, 190, 100)

    pts = NORTH_DRIVEWAY.map { |p| SeacoveHelpers.pt(p[0], p[1], 0.03) }
    f = grp.entities.add_face(pts)
    f.material = c if f

    pts2 = SOUTH_DRIVEWAY.map { |p| SeacoveHelpers.pt(p[0], p[1], 0.02) }
    f2 = grp.entities.add_face(pts2)
    f2.material = c if f2

    model.commit_operation
    puts "  Driveways: north + south"
  end

  def self.build_pool(model, tags)
    model.start_operation("Pool", true)
    grp = model.entities.add_group
    grp.name = "site-pool"
    grp.layer = tag(model, tags, "Pool")
    p = POOL
    f = grp.entities.add_face(
      SeacoveHelpers.pt(p[:x], p[:y], 0.04),
      SeacoveHelpers.pt(p[:x]+p[:w], p[:y], 0.04),
      SeacoveHelpers.pt(p[:x]+p[:w], p[:y]+p[:d], 0.04),
      SeacoveHelpers.pt(p[:x], p[:y]+p[:d], 0.04))
    f.material = mat(model, "Pool", 90, 150, 200, 170) if f
    model.commit_operation
    puts "  Pool: #{p[:w]}'x#{p[:d]}'"
  end

  def self.build_cabana(model, tags)
    model.start_operation("Cabana", true)
    grp = model.entities.add_group
    grp.name = "site-cabana"
    grp.layer = tag(model, tags, "Cabana")
    c = CABANA
    f = grp.entities.add_face(
      SeacoveHelpers.pt(c[:x], c[:y], 0.04),
      SeacoveHelpers.pt(c[:x]+c[:w], c[:y], 0.04),
      SeacoveHelpers.pt(c[:x]+c[:w], c[:y]+c[:d], 0.04),
      SeacoveHelpers.pt(c[:x], c[:y]+c[:d], 0.04))
    f.material = mat(model, "Cabana", 155, 140, 120, 190) if f
    model.commit_operation
    puts "  Cabana: #{c[:w]}'x#{c[:d]}'"
  end

  def self.build_concrete(model, tags)
    model.start_operation("Concrete", true)
    grp = model.entities.add_group
    grp.name = "site-concrete"
    grp.layer = tag(model, tags, "Concrete")
    c = mat(model, "Conc_Patio", 200, 200, 195, 80)
    [CONC_SOUTH, CONC_EAST, CONC_POOL_DECK].each do |poly|
      pts = poly.map { |p| SeacoveHelpers.pt(p[0], p[1], 0.02) }
      f = grp.entities.add_face(pts)
      f.material = c if f
    end
    model.commit_operation
    puts "  Concrete: 3 areas"
  end

  def self.build_walls(model, tags)
    model.start_operation("Walls & Fences", true)
    grp = model.entities.add_group
    grp.name = "site-walls-fences"
    grp.layer = tag(model, tags, "Walls & Fences")
    WALLS_AND_FENCES.each_with_index do |w, i|
      fx, fy, tx, ty, wt, ht = w
      wg = grp.entities.add_group
      wg.name = "site-#{wt}-#{i+1}"
      thick = (wt == "conc_wall") ? 0.5 : 0.08
      SeacoveHelpers.make_wall(wg, [fx, fy], [tx, ty], thick, ht, 0)
      wg.material = mat(model, "CW", 165, 165, 160) if wt == "conc_wall"
    end
    model.commit_operation
    puts "  Walls: #{WALLS_AND_FENCES.length} segments"
  end

  def self.build_elevations(model, tags)
    model.start_operation("Spot Elevations", true)
    grp = model.entities.add_group
    grp.name = "site-spot-elevations"
    grp.layer = tag(model, tags, "Spot Elevations")
    SPOT_ELEVATIONS.each { |e| grp.entities.add_cpoint(SeacoveHelpers.pt(e[0], e[1], 0.08)) }
    model.commit_operation
    puts "  Elevations: #{SPOT_ELEVATIONS.length} points"
  end

  # ==========================================================================
  # FOUNDATION BUILD METHODS
  # ==========================================================================

  def self.build_perimeter_footings(model, tags)
    model.start_operation("Perimeter Footings", true)
    grp = model.entities.add_group
    grp.name = "fnd-perimeter-footings"
    grp.layer = tag(model, tags, "Perimeter Footings")

    footing_w = FOOTING_WIDTH_IN / 12.0  # 1.0'
    footing_d = FOOTING_DEPTH_IN / 12.0  # 1.5'

    # Draw footing as a wall segment around the perimeter
    # The footing is below grade: z goes from -footing_d to 0
    path = PERIMETER_FOOTING
    (0...path.length).each do |i|
      j = (i + 1) % path.length
      p1 = path[i]
      p2 = path[j]
      seg = grp.entities.add_group
      seg.name = "fnd-footing-P#{format('%02d', i+1)}"
      SeacoveHelpers.make_wall(seg, p1, p2, footing_w, footing_d, -footing_d)
    end

    grp.material = mat(model, "Concrete_Footing", 170, 170, 165)
    model.commit_operation

    # Compute total footing length
    total = 0.0
    (0...path.length).each do |i|
      j = (i + 1) % path.length
      dx = path[j][0] - path[i][0]
      dy = path[j][1] - path[i][1]
      total += Math.sqrt(dx*dx + dy*dy)
    end
    puts "  Perimeter footings: #{path.length} segments, #{total.round(1)}' total"
    puts "    #{FOOTING_WIDTH_IN}\" wide x #{FOOTING_DEPTH_IN}\" deep"
  end

  def self.build_interior_footings(model, tags)
    model.start_operation("Interior Footings", true)
    grp = model.entities.add_group
    grp.name = "fnd-interior-footings"
    grp.layer = tag(model, tags, "Interior Footings")

    footing_w = FOOTING_WIDTH_IN / 12.0
    int_d = INTERIOR_FOOTING_DEPTH_IN / 12.0

    INTERIOR_FOOTINGS.each_with_index do |f, i|
      seg = grp.entities.add_group
      seg.name = "fnd-footing-I#{format('%02d', i+1)}"
      SeacoveHelpers.make_wall(seg, f[:from], f[:to], footing_w, int_d, -int_d)
    end

    grp.material = mat(model, "Concrete_Footing", 170, 170, 165)
    model.commit_operation
    puts "  Interior footings: #{INTERIOR_FOOTINGS.length} segments"
    INTERIOR_FOOTINGS.each { |f| puts "    #{f[:label]}" }
  end

  def self.build_fireplace_foundation(model, tags)
    model.start_operation("Fireplace Foundation", true)
    grp = model.entities.add_group
    grp.name = "fnd-fireplace"
    grp.layer = tag(model, tags, "Fireplace Foundation")

    fp = FIREPLACE_FOUNDATION
    depth = fp[:depth_in] / 12.0
    SeacoveHelpers.make_box(grp, fp[:x], fp[:y], -depth, fp[:w], fp[:d], depth)

    grp.material = mat(model, "Concrete_Mass", 160, 160, 155)
    model.commit_operation
    puts "  Fireplace foundation: #{fp[:w]}'x#{fp[:d]}' x #{fp[:depth_in]}\" deep"
  end

  def self.build_slab(model, tags)
    model.start_operation("Slab", true)
    grp = model.entities.add_group
    grp.name = "fnd-slab"
    grp.layer = tag(model, tags, "Slab")

    slab_t = SLAB_THICKNESS_IN / 12.0
    pts = SLAB_BOUNDARY.map { |p| SeacoveHelpers.pt(p[0], p[1], 0) }
    face = grp.entities.add_face(pts)
    if face
      face.reverse! if face.normal.z > 0  # push down
      face.pushpull(SeacoveHelpers.ft(slab_t))
      grp.material = mat(model, "Concrete_Slab", 180, 180, 175, 150)
    end

    model.commit_operation
    puts "  Slab: #{SLAB_THICKNESS_IN}\" thick, L-shape"
  end

  # ==========================================================================
  # DIMENSIONS
  # ==========================================================================
  def self.build_dimensions(model, tags)
    model.start_operation("Dimensions", true)
    grp = model.entities.add_group
    grp.name = "site-dimensions"
    grp.layer = tag(model, tags, "Dimensions")
    ents = grp.entities

    sw, se, ne, nw = CORNERS["SW"], CORNERS["SE"], CORNERS["NE"], CORNERS["NW"]
    ox, oy = HOUSE_X, HOUSE_Y

    # Property lines
    ents.add_dimension_linear(
      SeacoveHelpers.pt(sw[0], sw[1], 0), SeacoveHelpers.pt(nw[0], nw[1], 0),
      Geom::Vector3d.new(-SeacoveHelpers.ft(5), 0, 0))
    ents.add_dimension_linear(
      SeacoveHelpers.pt(nw[0], nw[1], 0), SeacoveHelpers.pt(ne[0], ne[1], 0),
      Geom::Vector3d.new(0, SeacoveHelpers.ft(5), 0))
    ents.add_dimension_linear(
      SeacoveHelpers.pt(ne[0], ne[1], 0), SeacoveHelpers.pt(se[0], se[1], 0),
      Geom::Vector3d.new(SeacoveHelpers.ft(5), 0, 0))

    # House dims
    ents.add_dimension_linear(
      SeacoveHelpers.pt(ox, oy, 0), SeacoveHelpers.pt(ox + LIVING_W, oy, 0),
      Geom::Vector3d.new(0, -SeacoveHelpers.ft(3), 0))
    ents.add_dimension_linear(
      SeacoveHelpers.pt(ox + LIVING_W, oy, 0),
      SeacoveHelpers.pt(ox + HOUSE_TOTAL_W, oy, 0),
      Geom::Vector3d.new(0, -SeacoveHelpers.ft(3), 0))
    ents.add_dimension_linear(
      SeacoveHelpers.pt(ox, oy, 0), SeacoveHelpers.pt(ox, oy + LIVING_D, 0),
      Geom::Vector3d.new(-SeacoveHelpers.ft(3), 0, 0))
    ents.add_dimension_linear(
      SeacoveHelpers.pt(ox + HOUSE_TOTAL_W, oy, 0),
      SeacoveHelpers.pt(ox + HOUSE_TOTAL_W, oy + BEDROOM_D, 0),
      Geom::Vector3d.new(SeacoveHelpers.ft(3), 0, 0))

    # Gaps house to PL
    ents.add_dimension_linear(
      SeacoveHelpers.pt(0, oy + 11, 0), SeacoveHelpers.pt(ox, oy + 11, 0),
      Geom::Vector3d.new(0, SeacoveHelpers.ft(1), 0))
    ents.add_dimension_linear(
      SeacoveHelpers.pt(ox + LIVING_W/2, 0, 0),
      SeacoveHelpers.pt(ox + LIVING_W/2, oy, 0),
      Geom::Vector3d.new(-SeacoveHelpers.ft(2), 0, 0))

    model.commit_operation
    puts "  Dimensions: property lines + house + gaps"
  end

  # ==========================================================================
  # BUILD ALL / INCREMENTAL
  # ==========================================================================
  SITE_PHASES = [
    :build_lot, :build_setbacks, :build_house, :build_roads,
    :build_driveways, :build_pool, :build_cabana, :build_concrete,
    :build_walls, :build_elevations, :build_dimensions
  ]

  FOUNDATION_PHASES = [
    :build_perimeter_footings, :build_interior_footings,
    :build_fireplace_foundation, :build_slab
  ]

  ALL_PHASES = SITE_PHASES + FOUNDATION_PHASES

  def self.build_site
    model = Sketchup.active_model
    tags = setup_tags(model)
    puts "\n=== Building Site ==="
    SITE_PHASES.each { |p| send(p, model, tags) }
    model.active_view.zoom_extents
    puts "=== Site complete ==="
  end

  def self.build_foundation
    model = Sketchup.active_model
    tags = setup_tags(model)
    puts "\n=== Building Foundation ==="
    FOUNDATION_PHASES.each { |p| send(p, model, tags) }
    model.active_view.zoom_extents
    puts "=== Foundation complete ==="
  end

  def self.build_all
    model = Sketchup.active_model
    tags = setup_tags(model)
    puts "\n=== Building Site + Foundation — Pass 4 ==="
    ALL_PHASES.each { |p| send(p, model, tags) }
    model.active_view.zoom_extents
    puts "\n=== PASS 4 COMPLETE ==="
    puts "Site: #{SITE_PHASES.length} layers"
    puts "Foundation: #{FOUNDATION_PHASES.length} layers"
    puts "Tag folders: Site/, Foundation/"
  end

  def self.build_next
    @queue ||= ALL_PHASES.dup
    item = @queue.shift
    return puts "All phases built." unless item
    model = Sketchup.active_model
    tags = setup_tags(model)
    send(item, model, tags)
    model.active_view.zoom_extents
    puts "--- #{@queue.length} remaining ---"
  end
end

puts "SeacoveSite4 loaded. PASS 4 — site + foundation."
puts "  .build_all         — everything"
puts "  .build_site        — site only"
puts "  .build_foundation  — foundation only"
puts "  .build_next        — one phase at a time"
