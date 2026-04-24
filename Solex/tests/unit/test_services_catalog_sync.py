from unittest.mock import MagicMock
from solex.services.catalog_sync import CatalogSyncService
from solex.models import Product


def test_sync_populates_square_id(app, db_session):
    p = Product(sku="T1", slug="t1", name="Thing", price_cents=1000,
                image_path="", active=True, weight_grams=10)
    db_session.add(p); db_session.commit()
    sq = MagicMock()
    sq.upsert_catalog_item.return_value = {"id": "sqcat_ABC"}
    svc = CatalogSyncService(db_session, sq)
    summary = svc.sync_all()
    assert summary == {"synced": 1, "errored": 0}
    db_session.refresh(p)
    assert p.square_catalog_object_id == "sqcat_ABC"


def test_sync_skips_inactive(app, db_session):
    p = Product(sku="T2", slug="t2", name="Thing", price_cents=1000,
                image_path="", active=False, weight_grams=10)
    db_session.add(p); db_session.commit()
    sq = MagicMock()
    svc = CatalogSyncService(db_session, sq)
    summary = svc.sync_all()
    assert summary["synced"] == 0
    sq.upsert_catalog_item.assert_not_called()


def test_sync_counts_errors(app, db_session):
    p = Product(sku="T3", slug="t3", name="Broken", price_cents=500,
                image_path="", active=True, weight_grams=5)
    db_session.add(p); db_session.commit()
    sq = MagicMock()
    sq.upsert_catalog_item.side_effect = RuntimeError("Square down")
    svc = CatalogSyncService(db_session, sq)
    summary = svc.sync_all()
    assert summary == {"synced": 0, "errored": 1}


def test_sync_does_not_overwrite_existing_square_id(app, db_session):
    p = Product(sku="T4", slug="t4", name="Already Synced", price_cents=750,
                image_path="", active=True, weight_grams=5,
                square_catalog_object_id="sqcat_EXISTING")
    db_session.add(p); db_session.commit()
    sq = MagicMock()
    sq.upsert_catalog_item.return_value = {"id": "sqcat_NEW"}
    svc = CatalogSyncService(db_session, sq)
    summary = svc.sync_all()
    assert summary["synced"] == 1
    db_session.refresh(p)
    # Existing ID preserved — only written when previously null
    assert p.square_catalog_object_id == "sqcat_EXISTING"
