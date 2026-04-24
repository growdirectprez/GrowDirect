"""
Sandbox-live subscription cycle. Marked `sandbox_live`; auto-skips without creds.

Full cycle against the real Square sandbox:
  1. Create a sandbox Customer
  2. Save a card-on-file
  3. Create a local Subscription due now
  4. Run SubscriptionService.charge_due_subscriptions()
  5. Assert Order + SubscriptionCharge landed; inventory decremented; next_charge_at advanced
  6. Cleanup: refund the sandbox payment
"""
import os
from datetime import datetime, timedelta, timezone

import pytest

from solex.services.subscriptions import SubscriptionService
from solex.services.square_client import SquareClient, SquareConfig
from solex.services.checkout import CheckoutService
from solex.services.inventory import InventoryService
from solex.services.tax import FlatRateTaxStub
from solex.services.shipping import FlatRateShippingStub
from solex.models import (
    Subscription,
    SubscriptionCharge,
    Customer,
    Product,
    Inventory,
    Order,
)

pytestmark = pytest.mark.sandbox_live

_REQUIRED_ENV = (
    "SQUARE_SANDBOX_ACCESS_TOKEN",
    "SQUARE_SANDBOX_APPLICATION_ID",
    "SQUARE_SANDBOX_LOCATION_ID",
)


@pytest.fixture()
def sandbox_config():
    missing = [v for v in _REQUIRED_ENV if not os.environ.get(v)]
    if missing:
        pytest.skip(f"sandbox creds missing: {missing}")
    return SquareConfig(
        access_token=os.environ["SQUARE_SANDBOX_ACCESS_TOKEN"],
        environment="sandbox",
        location_id=os.environ["SQUARE_SANDBOX_LOCATION_ID"],
        webhook_signature_key=os.environ.get("SQUARE_SANDBOX_WEBHOOK_SIGNATURE_KEY", ""),
    )


def test_autoship_cycle_against_real_sandbox(app, db_session, sandbox_config):
    square = SquareClient(sandbox_config)

    sq_customer = square.create_customer("autoship-test@solex.local", "Autoship Test")
    assert sq_customer.get("id"), sq_customer

    card = square.save_card_on_file(sq_customer["id"], "cnon:card-nonce-ok")
    assert card.get("id"), card

    local_customer = Customer(
        email="autoship-test@solex.local",
        first_name="Autoship",
        last_name="Test",
        square_customer_id=sq_customer["id"],
    )
    db_session.add(local_customer)
    db_session.flush()

    product = Product(
        sku="AUTOSHIP-TEST",
        slug="autoship-test",
        name="Autoship Test Product",
        short_description="",
        description="",
        price_cents=999,
        image_path="",
        active=True,
        weight_grams=10,
    )
    db_session.add(product)
    db_session.flush()
    db_session.add(Inventory(product_id=product.id, on_hand=10))
    db_session.commit()

    svc = SubscriptionService(
        session=db_session,
        square=square,
        checkout=CheckoutService(
            session=db_session,
            square=square,
            tax=FlatRateTaxStub(0.0),
            shipping=FlatRateShippingStub(flat_cents=0, free_threshold_cents=999999),
            inventory=InventoryService(db_session),
        ),
    )

    past = datetime.now(timezone.utc) - timedelta(minutes=1)
    sub = svc.create(
        customer=local_customer,
        product=product,
        qty=1,
        cadence_days=30,
        starting_at=past,
        square_card_id=card["id"],
    )

    summary = svc.charge_due_subscriptions()
    assert summary == {
        "attempted": 1,
        "succeeded": 1,
        "failed": 0,
        "past_due": 0,
    }, summary

    order = db_session.query(Order).filter_by(autoship=True).one()
    assert order.autoship_subscription_id == sub.id
    assert order.square_payment_id
    assert order.status == "paid"

    charge = db_session.query(SubscriptionCharge).one()
    assert charge.succeeded is True
    assert charge.order_id == order.id

    inv = db_session.query(Inventory).filter_by(product_id=product.id).one()
    assert inv.on_hand == 9

    db_session.refresh(sub)
    assert sub.status == "active"
    assert sub.last_charged_at is not None
    assert sub.next_charge_at > datetime.now(timezone.utc)

    try:
        square.create_refund(
            order.square_payment_id, order.total_cents, reason="test-cleanup"
        )
    except Exception:
        pass
