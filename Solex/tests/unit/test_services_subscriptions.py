# tests/unit/test_services_subscriptions.py
from unittest.mock import MagicMock
from datetime import datetime, timedelta, timezone
from solex.services.subscriptions import SubscriptionService
from solex.services.square_client import SquareDeclined
from solex.services.checkout import CheckoutService
from solex.services.tax import FlatRateTaxStub
from solex.services.shipping import FlatRateShippingStub
from solex.services.inventory import InventoryService
from solex.models import Subscription, Customer, Product, Inventory, Order


def _seed_cp(db_session):
    c = Customer(email="sub@ex.com", first_name="Sub", last_name="Scriber")
    db_session.add(c); db_session.flush()
    p = Product(sku="S1", slug="s1", name="Subbed", price_cents=2000,
                image_path="", active=True, weight_grams=100)
    db_session.add(p); db_session.flush()
    db_session.add(Inventory(product_id=p.id, on_hand=20))
    c.square_customer_id = "cust_1"
    db_session.commit()
    return c, p


def _svc(db_session, square, email=None):
    checkout = CheckoutService(
        session=db_session, square=square,
        tax=FlatRateTaxStub(0.0),
        shipping=FlatRateShippingStub(flat_cents=0, free_threshold_cents=999999),
        inventory=InventoryService(db_session),
    )
    return SubscriptionService(db_session, square, checkout, email or MagicMock())


def test_create_subscription(app, db_session):
    c, p = _seed_cp(db_session)
    svc = _svc(db_session, MagicMock())
    sub = svc.create(customer=c, product=p, qty=1, cadence_days=30,
                     starting_at=datetime.now(timezone.utc), square_card_id="ccof:ABC")
    assert sub.status == "active"
    assert db_session.query(Subscription).count() == 1


def test_charge_due_happy_path(app, db_session):
    c, p = _seed_cp(db_session)
    sq = MagicMock()
    sq.charge_saved_card.return_value = {"id": "sqp_1", "order_id": "sqo_1"}
    svc = _svc(db_session, sq)
    past = datetime.now(timezone.utc) - timedelta(minutes=1)
    svc.create(customer=c, product=p, qty=2, cadence_days=30,
               starting_at=past, square_card_id="ccof:ABC")
    summary = svc.charge_due_subscriptions()
    assert summary == {"attempted": 1, "succeeded": 1, "failed": 0, "past_due": 0}
    assert db_session.query(Order).filter_by(autoship=True).count() == 1
    inv = db_session.query(Inventory).filter_by(product_id=p.id).one()
    assert inv.on_hand == 18


def test_charge_due_declined_marks_past_due(app, db_session):
    c, p = _seed_cp(db_session)
    sq = MagicMock()
    sq.charge_saved_card.side_effect = SquareDeclined("card expired")
    email = MagicMock()
    svc = _svc(db_session, sq, email=email)
    past = datetime.now(timezone.utc) - timedelta(minutes=1)
    sub = svc.create(customer=c, product=p, qty=1, cadence_days=30,
                     starting_at=past, square_card_id="ccof:BAD")
    summary = svc.charge_due_subscriptions()
    assert summary["failed"] == 1
    db_session.refresh(sub)
    assert sub.status == "past_due"
    email.send.assert_called_once()
    assert db_session.query(Order).count() == 0


def test_three_failures_cancels(app, db_session):
    c, p = _seed_cp(db_session)
    sq = MagicMock(); sq.charge_saved_card.side_effect = SquareDeclined("nope")
    svc = _svc(db_session, sq)
    past = datetime.now(timezone.utc) - timedelta(minutes=1)
    sub = svc.create(customer=c, product=p, qty=1, cadence_days=30,
                     starting_at=past, square_card_id="ccof:BAD")
    for i in range(3):
        svc.charge_due_subscriptions()
        db_session.refresh(sub)
        if sub.status == "cancelled":
            break
        # Reset for next attempt (only if not yet cancelled)
        sub.next_charge_at = datetime.now(timezone.utc) - timedelta(minutes=1)
        sub.status = "active"  # reset so it's due again
        db_session.commit()
    db_session.refresh(sub)
    assert sub.status == "cancelled"


def test_pause_and_resume(app, db_session):
    c, p = _seed_cp(db_session)
    svc = _svc(db_session, MagicMock())
    sub = svc.create(customer=c, product=p, qty=1, cadence_days=30,
                     starting_at=datetime.now(timezone.utc), square_card_id="ccof:ABC")
    svc.pause(sub)
    assert sub.status == "paused"
    svc.resume(sub)
    assert sub.status == "active"
    assert sub.paused_until is None


def test_cancel(app, db_session):
    c, p = _seed_cp(db_session)
    svc = _svc(db_session, MagicMock())
    sub = svc.create(customer=c, product=p, qty=1, cadence_days=30,
                     starting_at=datetime.now(timezone.utc), square_card_id="ccof:ABC")
    svc.cancel(sub)
    assert sub.status == "cancelled"
    assert sub.cancelled_at is not None
