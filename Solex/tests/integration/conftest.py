import pytest
from unittest.mock import MagicMock
from pathlib import Path
from solex.services.catalog_import import CatalogImporter


@pytest.fixture()
def scenario_catalog(app, db_session, tmp_path):
    """Seed catalog into the test DB. Returns list of Products."""
    (tmp_path / "catalog").mkdir(exist_ok=True)
    CatalogImporter(
        db_session, Path("catalog"), tmp_path,
    ).import_from_yaml(Path("catalog/products.yaml"))
    db_session.expire_all()
    from solex.models import Product
    return db_session.query(Product).filter_by(active=True).all()


@pytest.fixture()
def mock_square_for_scenarios(mocker):
    """Patch solex.services.scenarios.base._square so scenarios don't hit Square."""
    counter = {"n": 0}

    def _order(*a, **kw):
        counter["n"] += 1
        return {"id": f"sq_order_{counter['n']}"}

    def _payment(*a, **kw):
        return {"id": f"sq_pay_{counter['n']}"}

    client = MagicMock(
        create_order=MagicMock(side_effect=_order),
        create_payment=MagicMock(side_effect=_payment),
    )
    mocker.patch("solex.services.scenarios.base._square", return_value=client)
    return client


@pytest.fixture()
def scenario_config():
    """Base config dict for prepare_context."""
    return {
        "SQUARE_ACCESS_TOKEN": "test",
        "SQUARE_ENVIRONMENT": "sandbox",
        "SQUARE_LOCATION_ID": "L",
        "SQUARE_WEBHOOK_SIGNATURE_KEY": "",
        "TAX_RATE_PCT": 0.0,
        "SHIPPING_FLAT_CENTS": 0,
        "SHIPPING_FREE_THRESHOLD_CENTS": 1,   # free shipping always
    }
