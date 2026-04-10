"""Spatial model consistency checks."""
from __future__ import annotations
from dataclasses import dataclass
from arc.model.spatial_model import Floor, Project


@dataclass
class ValidationError:
    level: str  # "error" or "warning"
    entity_id: str
    message: str


def validate_project(project: Project) -> list[ValidationError]:
    errors: list[ValidationError] = []
    for floor in project.floors:
        errors.extend(validate_floor(floor))
    return errors


def validate_floor(floor: Floor) -> list[ValidationError]:
    errors: list[ValidationError] = []
    wall_ids = {w.id for w in floor.walls}

    for wall in floor.walls:
        if wall.length_ft < 0.01:
            errors.append(ValidationError("error", wall.id, f"Wall '{wall.id}' has zero length"))
            continue
        for opening in wall.openings:
            if opening.end_position > wall.length_ft + 0.01:
                errors.append(ValidationError("error", wall.id,
                    f"Opening at {opening.position_along_wall}' + {opening.width}' wide = "
                    f"{opening.end_position}' exceeds wall length {wall.length_ft:.1f}'"))
            if opening.sill_height + opening.height > floor.plate_height + 0.01:
                errors.append(ValidationError("warning", wall.id,
                    f"Opening top ({opening.sill_height + opening.height:.1f}') "
                    f"exceeds plate height ({floor.plate_height}') in wall '{wall.id}'"))

    for room in floor.rooms:
        for ref in room.wall_refs:
            if ref not in wall_ids:
                errors.append(ValidationError("error", room.id,
                    f"Room '{room.id}' references non-existent wall '{ref}'"))

    return errors
