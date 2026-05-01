---
name: sketchup-guide
description: >
  Translate architectural blueprints into SketchUp 3D models and LayOut 2D construction
  documents. Use when the user asks to "model this in SketchUp", "create a 3D model",
  "build this in SketchUp", "use LayOut", "make construction documents in SketchUp",
  "Trimble SketchUp", "export from SketchUp", or needs guidance on converting
  blueprint dimensions and details into a SketchUp workflow.
metadata:
  version: "0.2.0"
---

# SketchUp & LayOut Modeling Guide

Help users translate architectural blueprint data into SketchUp 3D models and LayOut 2D
construction documents. This skill bridges the gap between paper blueprints (like the
25 Seacove archive) and modern digital modeling.

## Paths to SketchUp

### Path 0: Trimble MCP Connector (PRIMARY — use this first)
The official Trimble SketchUp MCP connector (announced April 28 2026) allows Claude to
interact directly with SketchUp .skp files via a cloud SketchUp session. Enable it in
Claude's MCP connector directory settings (requires Trimble ID + Claude account).

**What the Trimble MCP supports:**
- Create 3D geometry from plain-language descriptions + uploaded images, floor plans, or dimensions
- Direct .skp file generation — no Ruby scripts needed
- Version history tracked within the chat session for rapid iteration
- Paste screenshots back into the chat to point out adjustments
- Output: 2D preview thumbnail + direct .skp download link
- Free tier: up to 30 saved models; paid tier for more

**For ARC projects:** feed the `spatial_model.json` produced by `arc model` directly into
the Trimble MCP as structured input. This replaces the `arc generate` Ruby script stage.
Describe the model's coordinate system, floor layout, and key dimensions; the connector
builds the geometry iteratively.

### Path 1: Guide the User (fallback — no Trimble subscription)
Provide step-by-step SketchUp modeling instructions based on blueprint dimensions. Walk
through the modeling sequence, call out specific measurements, and describe the geometry
to create.

### Path 2: Generate Ruby Scripts via ARC (fallback — offline/scripted workflows)
The ARC pipeline (`arc generate`) produces SketchUp Ruby `.rb` scripts via Jinja2
templates. Run in SketchUp's Ruby Console: Extensions → Ruby Console → load each file.
Use when: fully automated/offline pipeline, no Trimble subscription, or batch processing.
Generated files: `00_helpers.rb`, `04_walls.rb`, `05_structure.rb`, `06_roof.rb`.

### Path 3: SketchUp Web via Browser (legacy — avoid)
Navigate to app.sketchup.com via Claude in Chrome and operate the web modeler directly.
This was a workaround before the Trimble MCP existed. Use only if the MCP is unavailable.

