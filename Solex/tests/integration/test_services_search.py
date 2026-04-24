"""Integration tests for SearchService — requires real Postgres with tsvector trigger."""
import pytest
from solex.services.search import SearchService
from solex.models import Product, Inventory


def _add_product(db_session, sku, name, description="", active=True):
    p = Product(
        sku=sku, slug=sku.lower(), name=name,
        description=description, short_description="",
        price_cents=1000, image_path="", active=active, weight_grams=10,
    )
    db_session.add(p)
    db_session.flush()
    db_session.add(Inventory(product_id=p.id, on_hand=5))
    db_session.commit()
    # Refresh to pick up trigger-populated search_tsv
    db_session.refresh(p)
    return p


def test_search_finds_product_by_name(app, db_session):
    _add_product(db_session, "SOAP1", "Lavender Soap")
    svc = SearchService(db_session)
    results = svc.search("lavender")
    assert len(results) == 1
    assert results[0].name == "Lavender Soap"


def test_search_finds_product_by_description(app, db_session):
    _add_product(db_session, "CANDLE1", "Beeswax Candle", description="hand-poured soy wax")
    svc = SearchService(db_session)
    results = svc.search("soy wax")
    assert any(r.sku == "CANDLE1" for r in results)


def test_search_excludes_inactive(app, db_session):
    _add_product(db_session, "DISC1", "Discontinued Widget", active=False)
    svc = SearchService(db_session)
    results = svc.search("discontinued")
    assert len(results) == 0


def test_search_empty_query_returns_empty(app, db_session):
    _add_product(db_session, "EMPTY1", "Something")
    svc = SearchService(db_session)
    assert svc.search("") == []
    assert svc.search("   ") == []


def test_search_no_match_returns_empty(app, db_session):
    _add_product(db_session, "NOMATCH1", "Totally Unrelated")
    svc = SearchService(db_session)
    results = svc.search("xyzzyquux")
    assert results == []
