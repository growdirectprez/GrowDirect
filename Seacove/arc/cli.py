"""ARC CLI — AI Draftsman pipeline commands."""
import json
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
    from arc.ingest.blueprint_reader import extract_pages_from_pdf, normalize_image

    project_dir = PROJECTS_DIR / project
    if not project_dir.exists():
        click.echo(f"Project directory not found: {project_dir}")
        raise SystemExit(1)

    inputs_dir = project_dir / "inputs"
    inputs_dir.mkdir(exist_ok=True)

    blueprint_dir = project_dir / "blueprints"
    if not blueprint_dir.exists():
        click.echo(f"No blueprints directory at {blueprint_dir}")
        click.echo("Create it and add PDF/image files, or symlink to your blueprint folder:")
        click.echo(f"  ln -s /path/to/blueprints {blueprint_dir}")
        raise SystemExit(1)

    pdf_count = 0
    for pdf in sorted(blueprint_dir.glob("*.pdf")) + sorted(blueprint_dir.glob("*.PDF")):
        images = extract_pages_from_pdf(pdf, inputs_dir / "pages")
        norm_dir = inputs_dir / "normalized"
        norm_dir.mkdir(exist_ok=True)
        for img in images:
            normalize_image(img, norm_dir / img.name)
        pdf_count += 1
        click.echo(f"  {pdf.name} -> {len(images)} page(s)")

    click.echo(f"Ingested {pdf_count} PDFs into {inputs_dir}/")


@main.command()
@click.argument("project")
@click.option("--model", default=None, help="Ollama vision model name")
def extract(project: str, model: str | None):
    """Extract dimensions from blueprints using vision AI."""
    from arc.extract.dimension_extractor import extract_dimensions, save_extraction

    inputs_dir = PROJECTS_DIR / project / "inputs" / "normalized"
    if not inputs_dir.exists():
        click.echo(f"No normalized inputs found. Run 'arc ingest {project}' first.")
        raise SystemExit(1)

    extract_dir = PROJECTS_DIR / project / "extractions"
    extract_dir.mkdir(exist_ok=True)

    for image in sorted(inputs_dir.glob("*.png")):
        click.echo(f"Extracting: {image.name}...")
        result = extract_dimensions(image, model=model)
        dims = result.get("dimensions", [])
        high_conf = sum(1 for d in dims if d.get("confidence", 0) >= 0.7)
        save_extraction(result, extract_dir / f"{image.stem}_extraction.json")
        click.echo(f"  {len(dims)} dimensions ({high_conf} high-confidence)")

    click.echo(f"Extractions saved to {extract_dir}/")
    click.echo("Review and correct extractions before running 'arc model'.")


@main.command("model")
@click.argument("project")
@click.option(
    "--model", "ollama_model", default=None,
    help="Ollama text model name (default: $ARC_MODEL_MODEL or llama3.1)",
)
@click.option(
    "--reconcile", is_flag=True, default=False,
    help="Compare extractions against existing spatial_model.json and produce a conflict report.",
)
@click.option(
    "--dry-run", is_flag=True, default=False,
    help="Print result to stdout without writing any files.",
)
def model_cmd(project: str, ollama_model: str | None, reconcile: bool, dry_run: bool):
    """Build spatial model from extraction data.

    Synthesis mode (default): reads all extractions/*.json, calls Ollama text
    model to reason about layout, writes model/spatial_model.json.

    Reconcile mode (--reconcile): diffs new extractions against an existing
    spatial_model.json and writes model/reconciliation_report.json.
    """
    import os
    from arc.model.builder import build_model, DEFAULT_MODEL

    project_dir = PROJECTS_DIR / project
    if not project_dir.exists():
        click.echo(f"Project directory not found: {project_dir}")
        raise SystemExit(1)

    model_name = ollama_model or os.environ.get("ARC_MODEL_MODEL", DEFAULT_MODEL)

    mode = "reconcile" if reconcile else "synthesize"
    click.echo(f"Model stage: {mode} | project={project} | model={model_name}")
    if dry_run:
        click.echo("(dry run — no files will be written)")

    try:
        result, out_path = build_model(
            project_dir,
            model=model_name,
            reconcile=reconcile,
            dry_run=dry_run,
        )
    except FileNotFoundError as exc:
        click.echo(f"Error: {exc}")
        raise SystemExit(1)
    except ValueError as exc:
        click.echo(f"Error: {exc}")
        raise SystemExit(1)

    if dry_run:
        click.echo(json.dumps(result, indent=2))
    else:
        click.echo(f"Written: {out_path}")
        if reconcile:
            report = result
            n_conflicts = len(report.get("conflicts", []))
            n_additions = len(report.get("additions", []))
            n_matches = len(report.get("matches", []))
            click.echo(f"  {n_matches} match(es), {n_conflicts} conflict(s), {n_additions} addition(s)")
            click.echo(f"\n{report.get('summary', '')}")
            if n_conflicts:
                click.echo("\nConflicts:")
                for c in report.get("conflicts", []):
                    sev = c.get("severity", "?").upper()
                    ent = c.get("entity", "?")
                    fld = c.get("field", "?")
                    mv = c.get("model_value")
                    ev = c.get("extracted_value")
                    rec = c.get("recommendation", "")
                    click.echo(f"  [{sev}] {ent}.{fld}: model={mv!r} vs extracted={ev!r}")
                    if rec:
                        click.echo(f"         → {rec}")
        else:
            floors = result.get("structure", {}).get("floors", [])
            total_walls = sum(len(f.get("walls", [])) for f in floors)
            total_rooms = sum(len(f.get("rooms", [])) for f in floors)
            click.echo(f"  {len(floors)} floor(s), {total_rooms} room(s), {total_walls} wall(s)")
            click.echo("\nNext: run 'arc validate' to check consistency.")


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
