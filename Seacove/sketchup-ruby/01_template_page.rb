# 01_template_page.rb — 24x36 ARCH D drawing template
# Matches the 2020 RPG CAD Services permit submission format
#
# Creates a flat rectangle representing the sheet, with title block outline
# on the right side. This is a REFERENCE PLANE for the model —
# the actual permit sheets will be produced in LayOut, not in the model.
#
# However, having the template in the model helps verify scale and proportion.
#
# Usage:
#   load '/path/to/00_helpers.rb'
#   load '/path/to/01_template_page.rb'
#   SeacoveTemplate.create_sheet("A-1", "EXISTING FLOOR PLAN")

module SeacoveTemplate
  include SeacoveHelpers

  # ARCH D sheet: 24" x 36" (2' x 3')
  SHEET_W = 3.0  # 36 inches = 3 feet
  SHEET_H = 2.0  # 24 inches = 2 feet

  # Title block on right side: 1.5" wide = 0.125 feet
  TITLE_BLOCK_W = 0.125  # 1.5 inches in feet

  # Border inset: 0.5" = 0.0417 feet
  BORDER = 0.0417

  # Drawing area (inside border, left of title block)
  DRAW_W = SHEET_W - TITLE_BLOCK_W - (BORDER * 2)
  DRAW_H = SHEET_H - (BORDER * 2)

  def self.create_sheet(sheet_number = "A-1", sheet_title = "FLOOR PLAN", origin_x = 0, origin_y = 0)
    model = Sketchup.active_model
    model.start_operation("Create Sheet #{sheet_number}", true)

    # Create group on "Template" tag
    group = SeacoveHelpers.tagged_group(model.entities, model, "Template-#{sheet_number}")
    group.name = "Sheet #{sheet_number}: #{sheet_title}"

    ents = group.entities

    # Sheet outline (24 x 36, landscape)
    sheet_pts = [
      SeacoveHelpers.pt(origin_x, origin_y, 0),
      SeacoveHelpers.pt(origin_x + SHEET_W, origin_y, 0),
      SeacoveHelpers.pt(origin_x + SHEET_W, origin_y + SHEET_H, 0),
      SeacoveHelpers.pt(origin_x, origin_y + SHEET_H, 0)
    ]
    sheet_face = ents.add_face(sheet_pts)
    if sheet_face
      # Make it white
      mat = model.materials.add("Sheet_White")
      mat.color = Sketchup::Color.new(255, 255, 255)
      sheet_face.material = mat
      sheet_face.back_material = mat
    end

    # Border line (0.5" inset)
    b = BORDER
    border_pts = [
      SeacoveHelpers.pt(origin_x + b, origin_y + b, 0.001),
      SeacoveHelpers.pt(origin_x + SHEET_W - b, origin_y + b, 0.001),
      SeacoveHelpers.pt(origin_x + SHEET_W - b, origin_y + SHEET_H - b, 0.001),
      SeacoveHelpers.pt(origin_x + b, origin_y + SHEET_H - b, 0.001)
    ]
    ents.add_edges(
      border_pts[0], border_pts[1],
      border_pts[1], border_pts[2],
      border_pts[2], border_pts[3],
      border_pts[3], border_pts[0]
    )

    # Title block divider line (vertical, 1.5" from right edge)
    tb_x = origin_x + SHEET_W - TITLE_BLOCK_W - b
    ents.add_edges(
      SeacoveHelpers.pt(tb_x, origin_y + b, 0.001),
      SeacoveHelpers.pt(tb_x, origin_y + SHEET_H - b, 0.001)
    )

    # Title block subdivisions (matching 2020 format)
    # The title block has sections from bottom up:
    # - Sheet number box (large, bottom)
    # - Scale, Job No, Date, Drawn By
    # - Engineer stamp area
    # - Sheet title
    # - Project info (Job Site)
    # - Prepared By (firm info)

    tb_left = tb_x
    tb_right = origin_x + SHEET_W - b
    tb_bottom = origin_y + b
    tb_top = origin_y + SHEET_H - b

    # Horizontal dividers in title block (approximate positions)
    dividers_y = [
      tb_bottom + 0.125,   # Bottom of sheet number box (1.5")
      tb_bottom + 0.25,    # Above scale/date fields (3")
      tb_bottom + 0.375,   # Above engineer stamp (4.5")
      tb_bottom + 0.625,   # Above sheet title (7.5")
      tb_bottom + 1.0,     # Above project info (12")
    ]

    dividers_y.each do |y|
      ents.add_edges(
        SeacoveHelpers.pt(tb_left, y, 0.001),
        SeacoveHelpers.pt(tb_right, y, 0.001)
      )
    end

    model.commit_operation
    puts "Sheet #{sheet_number} template created (24\"x36\" ARCH D)"
    puts "Drawing area: #{(DRAW_W * 12).round(1)}\" x #{(DRAW_H * 12).round(1)}\""
    group
  end

  # Create a scale reference bar at the bottom of the drawing area
  # Useful for verifying 1/4" = 1'-0" scale
  def self.create_scale_bar(origin_x = 0, origin_y = -0.1)
    model = Sketchup.active_model
    model.start_operation("Scale Bar", true)

    group = SeacoveHelpers.tagged_group(model.entities, model, "Template-Scale")
    group.name = "Scale Reference Bar"
    ents = group.entities

    # At 1/4" = 1'-0" scale, 1 foot in real life = 0.25" on paper
    # Draw tick marks at 1-foot intervals for 10 feet
    (0..10).each do |i|
      x = origin_x + (i * 1.0) # 1 foot intervals in model space
      tick_h = (i % 5 == 0) ? 0.05 : 0.025 # taller ticks at 0, 5, 10
      ents.add_edges(
        SeacoveHelpers.pt(x, origin_y, 0),
        SeacoveHelpers.pt(x, origin_y + tick_h, 0)
      )
    end

    # Baseline
    ents.add_edges(
      SeacoveHelpers.pt(origin_x, origin_y, 0),
      SeacoveHelpers.pt(origin_x + 10.0, origin_y, 0)
    )

    model.commit_operation
    puts "Scale bar created: 10'-0\" reference at 1/4\" = 1'-0\""
    group
  end

end

puts "SeacoveTemplate loaded. Usage: SeacoveTemplate.create_sheet('A-1', 'FLOOR PLAN')"
