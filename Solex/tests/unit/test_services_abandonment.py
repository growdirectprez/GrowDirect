from unittest.mock import MagicMock
from datetime import datetime, timedelta, timezone
from solex.services.abandonment import AbandonmentService, FIRST_NUDGE_DELAY
from solex.models import Cart, CartLine, Customer, Product, Inventory


def _seed_customer_with_cart(db_session, activity_ago: timedelta):
    c = Customer(email="lingerer@ex.com", first_name="L")
    db_session.add(c); db_session.flush()
    p = Product(sku="X", slug="x", name="X", price_cents=500,
                image_path="", active=True, weight_grams=1)
    db_session.add(p); db_session.flush()
    db_session.add(Inventory(product_id=p.id, on_hand=10))
    cart = Cart(session_key="sess1", customer_id=c.id, currency="USD",
                last_activity_at=datetime.now(timezone.utc) - activity_ago)
    db_session.add(cart); db_session.flush()
    db_session.add(CartLine(cart_id=cart.id, product_id=p.id, qty=1, price_snapshot_cents=500))
    db_session.commit()
    return cart, c


def test_sweep_sends_first_nudge_for_old_cart(app, db_session):
    cart, c = _seed_customer_with_cart(db_session, FIRST_NUDGE_DELAY + timedelta(minutes=5))
    email = MagicMock()
    summary = AbandonmentService(db_session, email).sweep()
    assert summary["first_nudge"] == 1
    email.send.assert_called_once()
    db_session.refresh(cart)
    assert cart.abandonment_emailed_at is not None


def test_sweep_skips_fresh_cart(app, db_session):
    _seed_customer_with_cart(db_session, timedelta(minutes=10))
    email = MagicMock()
    summary = AbandonmentService(db_session, email).sweep()
    assert summary["first_nudge"] == 0
    email.send.assert_not_called()


def test_sweep_skips_recovered_cart(app, db_session):
    cart, c = _seed_customer_with_cart(db_session, FIRST_NUDGE_DELAY + timedelta(hours=1))
    cart.recovered_at = datetime.now(timezone.utc)
    db_session.commit()
    summary = AbandonmentService(db_session, MagicMock()).sweep()
    assert summary["first_nudge"] == 0
