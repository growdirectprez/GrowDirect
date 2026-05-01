"""ARC component library — reusable SketchUp building components.

Each component is a parametric building element (stud, beam, post, window, etc.)
that can be registered once as a ComponentDefinition and placed many times as
ComponentInstances. This is the 'board by board' library.

Usage:
    from arc.components import ComponentRegistry
    from arc.components.structural import post, beam
    from arc.components.framing import stud_2x6, plate_2x6

    reg = ComponentRegistry()
    post(size_in=3.5, height_in=96.0, registry=reg)
    beam(width_in=3.5, depth_in=11.25, span_in=240.0, registry=reg)

    # All definition code for one build_model call:
    code = reg.all_definition_code()
"""

from arc.components.base import ComponentRegistry, ComponentSpec, SnapPoint

__all__ = ["ComponentRegistry", "ComponentSpec", "SnapPoint"]
