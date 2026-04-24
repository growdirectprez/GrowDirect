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


if __name__ == "__main__":
    cli()
