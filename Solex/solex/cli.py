from pathlib import Path
import click
from solex import create_app
from solex.extensions import db
from solex.services.catalog_import import CatalogImporter


@click.group()
def cli(): ...


@cli.group()
def catalog(): ...


@catalog.command("import")
@click.option("--path", default="catalog/products.yaml", show_default=True)
def import_catalog(path):
    app = create_app()
    with app.app_context():
        importer = CatalogImporter(
            session=db.session,
            catalog_root=Path("catalog"),
            static_root=Path("solex/static"),
        )
        counts = importer.import_from_yaml(Path(path))
        click.echo(f"imported: {counts}")


@catalog.command("generate-placeholders")
def catalog_generate_placeholders():
    """Generate placeholder PNGs for every SKU in products.yaml."""
    from pathlib import Path
    import yaml
    from solex.services.placeholder_gen import generate
    data = yaml.safe_load(Path("catalog/products.yaml").read_text())
    skus = [p["sku"] for p in data.get("products", [])]
    out = Path("solex/static/catalog/images")
    count = generate(skus, out)
    click.echo(f"generated: {count} PNG tiles at {out}")


@catalog.command("sync-to-square")
def sync_to_square():
    """Sync all active products to Square Catalog (requires SQUARE env vars)."""
    import os
    from solex.services.catalog_sync import CatalogSyncService
    from solex.services.square_client import SquareClient, SquareConfig

    app = create_app()
    with app.app_context():
        cfg = SquareConfig(
            access_token=os.environ["SQUARE_SANDBOX_ACCESS_TOKEN"],
            environment=os.environ.get("SQUARE_ENVIRONMENT", "sandbox"),
            location_id=os.environ["SQUARE_SANDBOX_LOCATION_ID"],
            webhook_signature_key=os.environ.get("SQUARE_SANDBOX_WEBHOOK_SIGNATURE_KEY", ""),
        )
        summary = CatalogSyncService(db.session, SquareClient(cfg)).sync_all()
        click.echo(f"sync complete: {summary}")


@cli.group()
def admin(): ...


@admin.command("create-seed-user")
@click.option("--email", default="dev@solex.local")
@click.option("--password", default="password")
def create_seed(email, password):
    from sqlalchemy import select
    from solex.models import AdminUser
    from solex.services.auth import AuthService

    app = create_app()
    with app.app_context():
        existing = db.session.execute(
            select(AdminUser).where(AdminUser.email == email)
        ).scalar_one_or_none()
        if existing:
            click.echo(f"exists: {email}")
            return
        user = AdminUser(email=email, active=True)
        db.session.add(user)
        db.session.flush()
        AuthService(db.session).set_admin_password(user, password)
        db.session.commit()
        click.echo(f"created: {email}")


@cli.group()
def scheduler(): ...


@scheduler.command("run")
def scheduler_run():
    """Run rq-scheduler in the foreground. Used by the scheduler container."""
    from solex.jobs.scheduler import run_forever
    run_forever()


@scheduler.command("schedule-once")
def scheduler_schedule_once():
    """Register (or re-register) cron jobs idempotently; don't run forever."""
    from solex.jobs.scheduler import schedule_recurring_jobs
    ids = schedule_recurring_jobs()
    click.echo(f"scheduled: {ids}")


@cli.group()
def scenarios(): ...


@scenarios.command("list")
def scenarios_list():
    from solex.services.scenarios import registry
    registry._import_all()
    for name, cls in sorted(registry.all_scenarios().items()):
        click.echo(f"{name:30s} {cls.description}")


@scenarios.command("run")
@click.argument("name")
@click.option("--params-json", default="{}")
def scenarios_run(name, params_json):
    import json
    from datetime import datetime, timezone
    from solex.services.scenarios import registry, prepare_context
    registry._import_all()
    cls = registry.get(name)
    if cls is None:
        click.echo(f"unknown scenario: {name}"); raise SystemExit(1)
    app = create_app()
    with app.app_context():
        from solex.models import ScenarioRun
        params = cls.params_schema(**json.loads(params_json))
        run = ScenarioRun(
            scenario_name=name, params_json=params.model_dump(),
            started_at=datetime.now(timezone.utc), status="running", summary_json={},
        )
        db.session.add(run); db.session.commit()
        ctx = prepare_context(db.session, run, config=dict(app.config))
        summary = cls().run(ctx, params)
        run.summary_json = summary
        run.completed_at = datetime.now(timezone.utc)
        run.status = "succeeded" if not summary.get("failed") else "partial"
        db.session.commit()
        click.echo(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    cli()
