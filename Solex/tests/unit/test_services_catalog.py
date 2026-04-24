from solex.models import Product, Category
from solex.services.catalog import CatalogService


def _make_category(session, slug="cat-1"):
    cat = Category(slug=slug, name="Category One", sort=1)
    session.add(cat)
    session.flush()
    return cat


def _make_product(session, cat, slug="prod-active", active=True, sku="SKU-A"):
    prod = Product(
        sku=sku,
        slug=slug,
        name="Active Product",
        price_cents=1000,
        active=active,
        weight_grams=100,
        category_id=cat.id,
    )
    session.add(prod)
    session.flush()
    return prod


def test_list_products_returns_only_active(app, db_session):
    with app.app_context():
        cat = _make_category(db_session)
        _make_product(db_session, cat, slug="prod-active", active=True, sku="SKU-A")
        _make_product(db_session, cat, slug="prod-inactive", active=False, sku="SKU-B")

        svc = CatalogService(db_session)
        results = svc.list_products()
        assert len(results) == 1
        assert results[0].slug == "prod-active"


def test_get_product_returns_by_slug(app, db_session):
    with app.app_context():
        cat = _make_category(db_session, slug="cat-2")
        prod = _make_product(db_session, cat, slug="find-me", sku="SKU-C")

        svc = CatalogService(db_session)
        found = svc.get_product("find-me")
        assert found is not None
        assert found.id == prod.id


def test_get_product_returns_none_for_unknown(app, db_session):
    with app.app_context():
        svc = CatalogService(db_session)
        assert svc.get_product("does-not-exist") is None
