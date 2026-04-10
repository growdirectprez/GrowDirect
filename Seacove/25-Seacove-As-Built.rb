# 25 Sea Cove Drive - As-Built SketchUp Model
# Douglas W. Rucker AIA, 1958
# Rancho Palos Verdes, CA
#
# USAGE: In SketchUp Ruby Console, type:
# load '/Users/gclyle/GrowDirect/ARC/25-Seacove-As-Built.rb'

model = Sketchup.active_model
ents = model.active_entities

model.start_operation("25 Seacove As-Built", true)

# Create Tags
tag_names = ["Site","Foundation","Walls-1958","Walls-1960","Walls-Garage",
             "Roof","Posts","Beams","Pool","Landscape"]
tag_names.each { |t| model.layers.add(t) unless model.layers[t] }

# Helper: make a rectangular box group
def make_box(ents, name, ox, oy, oz, w, d, h, tag)
  grp = ents.add_group
  grp.name = name
  pts = [
    Geom::Point3d.new(ox, oy, oz),
    Geom::Point3d.new(ox+w, oy, oz),
    Geom::Point3d.new(ox+w, oy+d, oz),
    Geom::Point3d.new(ox, oy+d, oz)
  ]
  f = grp.entities.add_face(pts)
  f.pushpull(h) if f
  t = Sketchup.active_model.layers[tag]
  grp.layer = t if t
  grp
end

# Dimensions (feet) - from original blueprints
# Origin 0,0,0 = SW corner of original house
# X = East, Y = North, Z = Up
plate = 8.0
wt = 0.5

# ================================================
# FOUNDATION SLABS
# ================================================
make_box(ents, "Slab_Main", 0, 0, -0.5, 42, 28, 0.5, "Foundation")
make_box(ents, "Slab_Garage", 42, -2, -0.5, 20, 18, 0.5, "Foundation")
make_box(ents, "Slab_Addition", 5, 28, -0.5, 25, 14, 0.5, "Foundation")

# ================================================
# ORIGINAL 1958 HOUSE WALLS
# Living wing: west side, ~28' x 18'
# Bedroom wing: east side, ~24' x 28'
# ================================================

# South walls
make_box(ents, "Wall_S_Living", 0, -wt/2, 0, 28, wt, plate, "Walls-1958")
make_box(ents, "Wall_S_Bedrooms", 28, -wt/2, 0, 14, wt, plate, "Walls-1958")

# North walls
make_box(ents, "Wall_N_Living", 0, 18-wt/2, 0, 28, wt, plate, "Walls-1958")
make_box(ents, "Wall_N_Bedrooms", 18, 28-wt/2, 0, 24, wt, plate, "Walls-1958")

# West wall
make_box(ents, "Wall_West", -wt/2, 0, 0, wt, 18, plate, "Walls-1958")

# East wall
make_box(ents, "Wall_East", 42-wt/2, 0, 0, wt, 28, plate, "Walls-1958")

# Connection wall (living to bedroom at Y=18)
make_box(ents, "Wall_Connect", 18-wt/2, 0, 0, wt, 18, plate, "Walls-1958")

# Interior: Hall wall
make_box(ents, "Wall_Hall", 18, 14-wt/2, 0, 24, wt, plate, "Walls-1958")

# Interior: Bedroom dividers
make_box(ents, "Wall_BR1", 26-wt/2, 14, 0, wt, 14, plate, "Walls-1958")
make_box(ents, "Wall_BR2", 34-wt/2, 14, 0, wt, 14, plate, "Walls-1958")

# Interior: Kitchen partition
make_box(ents, "Wall_Kitchen", 12, 10-wt/2, 0, 6, wt, plate, "Walls-1958")

# Interior: Bathroom walls
make_box(ents, "Wall_Bath_S", 18, 6-wt/2, 0, 6, wt, plate, "Walls-1958")
make_box(ents, "Wall_Bath_W", 24-wt/2, 0, 0, wt, 14, plate, "Walls-1958")

# ================================================
# 1960 BEDROOM ADDITION (Vawter Addition)
# 2 bedrooms + hall + bath, ~25' x 14'
# North of main house
# ================================================

make_box(ents, "Wall_Add_N", 5, 42-wt/2, 0, 25, wt, plate, "Walls-1960")
make_box(ents, "Wall_Add_W", 5-wt/2, 28, 0, wt, 14, plate, "Walls-1960")
make_box(ents, "Wall_Add_E", 30-wt/2, 28, 0, wt, 14, plate, "Walls-1960")
make_box(ents, "Wall_Add_Div", 17-wt/2, 28, 0, wt, 14, plate, "Walls-1960")
make_box(ents, "Wall_Add_Bath", 12, 35-wt/2, 0, 5, wt, plate, "Walls-1960")

# ================================================
# GARAGE ADDITION
# ~20' x 16', east of bedroom wing
# ================================================

make_box(ents, "Wall_Gar_S", 42, -2-wt/2, 0, 20, wt, plate, "Walls-Garage")
make_box(ents, "Wall_Gar_N", 42, 16-wt/2, 0, 20, wt, plate, "Walls-Garage")
make_box(ents, "Wall_Gar_E", 62-wt/2, -2, 0, wt, 18, plate, "Walls-Garage")
# Garage door header
make_box(ents, "Wall_Gar_Header", 44, -2-wt/2, 7, 16, wt, 1, "Walls-Garage")
# Side piers at garage door
make_box(ents, "Wall_Gar_SW", 42, -2-wt/2, 0, 2, wt, plate, "Walls-Garage")
make_box(ents, "Wall_Gar_SE", 60, -2-wt/2, 0, 2, wt, plate, "Walls-Garage")

# ================================================
# EXPOSED POSTS (4x4 Douglas Fir)
# ================================================

ps = 4.0/12.0  # 4 inches

# South face posts (living wing)
5.times do |i|
  x = 2 + i * 6.0
  make_box(ents, "Post_S#{i}", x-ps/2, -ps/2, 0, ps, ps, plate, "Posts")
end

# North face posts (living wing)
5.times do |i|
  x = 2 + i * 6.0
  make_box(ents, "Post_N#{i}", x-ps/2, 18-ps/2, 0, ps, ps, plate, "Posts")
end

# Corner posts
[[42,0],[42,14],[42,28],[18,28],[0,0],[0,18]].each_with_index do |p,i|
  make_box(ents, "Post_C#{i}", p[0]-ps/2, p[1]-ps/2, 0, ps, ps, plate, "Posts")
end

# ================================================
# BEAMS (4x10 exposed)
# ================================================

bw = 4.0/12.0
bh = 10.0/12.0

# Ridge beam - living wing (E-W)
make_box(ents, "Beam_Ridge_Liv", -2, 9-bw/2, plate, 32, bw, bh, "Beams")

# Ridge beam - bedroom wing (E-W)
make_box(ents, "Beam_Ridge_Bed", 18, 14-bw/2, plate, 26, bw, bh, "Beams")

# Exposed rafters - living wing (N-S, every 4')
8.times do |i|
  rx = 1 + i * 3.5
  rw = 2.0/12.0
  rh = 6.0/12.0
  make_box(ents, "Rafter_#{i}", rx-rw/2, -3, plate-rh, rw, 24, rh, "Beams")
end

# ================================================
# ROOFS - Flat panels (low slope approximated as flat)
# With 3.5' overhangs
# ================================================

ov = 3.5
roof_t = 0.4  # roof thickness

# Living wing roof
make_box(ents, "Roof_Living", -ov, -ov, plate+bh, 28+2*ov+2, 18+2*ov, roof_t, "Roof")

# Bedroom wing roof
make_box(ents, "Roof_Bedroom", 18-ov, -ov, plate+bh-0.3, 24+2*ov, 28+2*ov, roof_t, "Roof")

# Addition roof
make_box(ents, "Roof_Addition", 5-ov, 28-1, plate+0.3, 25+2*ov, 14+ov+1, roof_t, "Roof")

# Garage roof
make_box(ents, "Roof_Garage", 42-1, -2-ov, plate-0.5, 20+ov+1, 18+2*ov, roof_t, "Roof")

# ================================================
# POOL (west of house)
# ================================================

# Pool deck
make_box(ents, "Pool_Deck", -24, -2, 0, 22, 22, 0.3, "Pool")

# Pool (sunken)
pool_grp = ents.add_group
pool_grp.name = "Pool_Water"
pf = pool_grp.entities.add_face(
  [-20, 2, -0.1], [-6, 2, -0.1], [-6, 14, -0.1], [-20, 14, -0.1]
)
pf.pushpull(4) if pf  # 4' deep
t = model.layers["Pool"]
pool_grp.layer = t if t

# ================================================
# SITE ELEMENTS
# ================================================

# Sea Cove Drive
make_box(ents, "SeaCove_Dr", -30, -20, -0.2, 100, 14, 0.2, "Site")

# Clipper Road
make_box(ents, "Clipper_Rd", -30, -20, -0.2, 14, 80, 0.2, "Site")

# Driveway
make_box(ents, "Driveway", 44, -20, -0.1, 12, 18, 0.15, "Site")

# ================================================
# PALM TREES (simplified as cylinders)
# ================================================

[[10,24,25],[-8,10,22],[35,-15,28],[-15,35,20],[50,20,24]].each_with_index do |t,i|
  tree = ents.add_group
  tree.name = "Palm_#{i}"
  c = tree.entities.add_circle([t[0],t[1],0], [0,0,1], 0.4, 8)
  tf = tree.entities.add_face(c)
  tf.pushpull(t[2]) if tf
  # Crown
  cr = tree.entities.add_circle([t[0],t[1],t[2]], [0,0,1], 3.5, 8)
  cf = tree.entities.add_face(cr)
  cf.pushpull(2) if cf
  tag = model.layers["Landscape"]
  tree.layer = tag if tag
end

# ================================================
# FRONT DOOR
# ================================================

make_box(ents, "Front_Door", 14, -0.6, 0, 3, 0.3, 7, "Walls-1958")

model.commit_operation

# Set camera to aerial view
eye = Geom::Point3d.new(80, -60, 60)
target = Geom::Point3d.new(20, 15, 4)
up = Geom::Vector3d.new(0, 0, 1)
cam = Sketchup::Camera.new(eye, target, up)
model.active_view.camera = cam

# Zoom to fit
model.active_view.zoom_extents

puts ""
puts "==== 25 SEA COVE DRIVE - MODEL LOADED ===="
puts "Tags: #{tag_names.join(', ')}"
puts "Toggle tags to show/hide building phases"
puts ""
puts "NEXT: Refine dimensions against blueprint PDFs"
puts "Original architect: Douglas W. Rucker AIA, 1958"
puts ""
