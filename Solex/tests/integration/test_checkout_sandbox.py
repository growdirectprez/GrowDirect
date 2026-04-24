"""
Sandbox-live integration. Marked `sandbox_live`; skipped by default.

Run with:
  docker compose run --rm -e SOLEX_ENV=testing web pytest -m sandbox_live -v
"""
import os
import pytest
from pathlib import Path

from solex.services.catalog_import import CatalogImporter
from solex.services.checkout import CheckoutService, CartLineIn, CustomerIn
from solex.services.square_client import SquareClient, SquareConfig
from solex.services.inventory import InventoryService
from solex.services.tax import FlatRateTaxStub
from solex.services.shipping import FlatRateShippingStub
from solex.models import Order, Inventory, Product

pytestmark = pytest.mark.sandbox_live

_need = (
    "SQUARE_SANDBOX_ACCESS_TOKEN",
    "SQUARE_SANDBOX_APPLICATION_ID",
    "SQUARE_SANDBOX_LOCATION_ID",
)


@pytest.fixture()
def sandbox_config():
    missing = [v for v in _need if not os.environ.get(v)]
    if missing:
        pytest.skip(f"sandbox creds missing: {missing}")
    return SquareConfig(
        access_token=os.environ["SQUARE_SANDBOX_ACCESS_TOKEN"],
        environment="sandbox",
        location_id=os.environ["SQUARE_SANDBOX_LOCATION_ID"],
        webhook_signature_key=os.environ.get("SQUARE_SANDBOX_WEBHOOK_SIGNATURE_KEY", ""),
    )


@pytest.fixture()
def seed(app, db_session, tmp_path):
    (tmp_path / "catalog").mkdir(exist_ok=True)
    CatalogImporter(db_session, Path("catalog"), tmp_path).import_from_yaml(Path("catalog/products.yaml"))
    db_session.expire_all()
    return db_session.query(Product).filter_by(sku="PET-GUT-60").one()


def test_places_order_against_real_sandbox(app, db_session, seed, sandbox_config):
    product = seed
    square = SquareClient(sandbox_config)
    svc = CheckoutService(
        session=db_session,
        square=square,
        tax=FlatRateTaxStub(rate_pct=0.0),
        shipping=FlatRateShippingStub(flat_cents=500, free_threshold_cents=99999),
        inventory=InventoryService(db_session),
    )
    line = CartLineIn(
        product_id=product.id,
        qty=1,
        price_cents=product.price_cents,
        name=product.name,
        sku=product.sku,
        image_path=product.image_path,
    )
    order = svc.place_order(
        cart_lines=[line],
        customer=CustomerIn(email="sandbox@solex.local", name="Sandbox Buyer"),
        shipping_addr={
            "first_name": "Sandbox", "last_name": "Buyer",
            "line1": "1 Test St", "city": "Test", "region": "CA",
            "postal_code": "94105", "country": "US",
        },
        billing_addr={
            "first_name": "Sandbox", "last_name": "Buyer",
            "line1": "1 Test St", "city": "Test", "region": "CA",
            "postal_code": "94105", "country": "US",
        },
        payment_token="cnon:card-nonce-ok",
    )
    assert order.status == "paid"
    assert order.square_payment_id
    inv = db_session.query(Inventory).filter_by(product_id=product.id).one()
    assert inv.on_hand == (100 if product.sku == "AO-YOUTH-30" else 59)  # PET-GUT-60 starts at 60

    # Clean up: refund the sandbox payment so we don't accumulate garbage
    square.create_refund(order.square_payment_id, order.total_cents, reason="test-cleanup")
