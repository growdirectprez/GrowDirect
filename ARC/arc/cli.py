"""ARC CLI — AI Draftsman pipeline commands."""
import click
from pathlib import Path

PROJECTS_DIR = Path(__file__).parent.parent / "projects"


@click.group()
@click.version_option(package_name="arc")
def main():
    """ARC — AI Draftsman. Blueprint to SketchUp pipeline."""
    pass


@main.command()
@click.argument("project")
def ingest(project: str):
    """Normalize inputs (PDFs, photos, descriptions) for a project."""
    project_dir = PROJECTS_DIR / project
    if not project_dir.exists():
        click.echo(f"Project directory not found: {project_dir}")
        raise SystemExit(1)
    click.echo(f"Ingesting inputs for project: {project}")


@main.command()
@click.argument("project")
def extract(project: str):
    """Extract dimensions from blueprints using vision AI."""
    click.echo(f"Extracting dimensions for project: {project}")


@main.command("model")
@click.argument("project")
def model_cmd(project: str):
    """Build spatial model from extraction data."""
    click.echo(f"Building spatial model for project: {project}")


@main.command()
@click.argument("project")
def validate(project: str):
    """Validate spatial model consistency."""
    from arc.model.serialization import load_project
    from arc.model.validator import validate_project as _validate

    model_path = PROJECTS_DIR / project / "model" / "spatial_model.json"
    if not model_path.exists():
        click.echo(f"Model not found: {model_path}")
        raise SystemExit(1)

    proj = load_project(model_path)
    errors = _validate(proj)
    if not errors:
        click.echo("Model is valid. No errors found.")
    else:
        for err in errors:
            icon = "ERROR" if err.level == "error" else "WARN"
            click.echo(f"  [{icon}] {err.entity_id}: {err.message}")
        error_count = sum(1 for e in errors if e.level == "error")
        if error_count:
            click.echo(f"\n{error_count} error(s) found.")
            raise SystemExit(1)


@main.command()
@click.argument("project")
@click.option(
    "--output-dir", "-o",
    default=None,
    help="Output directory for .rb files. Defaults to projects/<project>/ruby/",
)
def generate(project: str, output_dir: str | None):
    """Generate SketchUp Ruby scripts from spatial model."""
    from arc.model.serialization import load_project
    from arc.model.validator import validate_project as _validate
    from arc.generate.sketchup_ruby import generate_ruby_scripts

    model_path = PROJECTS_DIR / project / "model" / "spatial_model.json"
    if not model_path.exists():
        click.echo(f"Model not found: {model_path}")
        raise SystemExit(1)

    proj = load_project(model_path)

    errors = _validate(proj)
    error_count = sum(1 for e in errors if e.level == "error")
    if error_count:
        for err in errors:
            if err.level == "error":
                click.echo(f"  [ERROR] {err.entity_id}: {err.message}")
        click.echo(f"\n{error_count} validation error(s). Fix model before generating.")
        raise SystemExit(1)

    out_dir = Path(output_dir) if output_dir else PROJECTS_DIR / project / "ruby"
    generated = generate_ruby_scripts(proj, out_dir)

    click.echo(f"Generated {len(generated)} file(s) in {out_dir}:")
    for path in generated:
        click.echo(f"  {path.name}")
