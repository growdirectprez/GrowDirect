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
