"""Tests for EmailService (Task 6.4)."""
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock
import pytest

from solex.models import EmailLog, Order, OrderItem


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_order(db_session):
    order = Order(
        public_token="tok1",
        customer_email="a@b.c",
        customer_name="A B",
        shipping_address_json={},
        billing_address_json={},
        subtotal_cents=1000,
        tax_cents=0,
        shipping_cents=500,
        total_cents=1500,
        square_order_id="sqo1",
        square_payment_id="sqp1",
        placed_at=datetime.now(timezone.utc),
        status="paid",
    )
    db_session.add(order)
    db_session.flush()
    db_session.add(
        OrderItem(
            order_id=order.id,
            sku_snapshot="SK",
            name_snapshot="Widget",
            price_snapshot_cents=1000,
            qty=1,
            line_total_cents=1000,
        )
    )
    db_session.commit()
    return order


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_renders_and_logs_sent_at(app, db_session):
    """Successful send: EmailLog row created with sent_at set."""
    order = _make_order(db_session)

    with app.app_context():
        with patch("solex.services.email.mail") as mock_mail:
            mock_mail.send.return_value = None
            from solex.services.email import EmailService
            EmailService().send("order_confirmation", "a@b.c", order=order)

    logs = db_session.query(EmailLog).all()
    assert len(logs) == 1
    log = logs[0]
    assert log.template == "order_confirmation"
    assert log.to == "a@b.c"
    assert log.sent_at is not None
    assert log.error is None


def test_send_failure_logs_error(app, db_session):
    """On SMTP failure: EmailLog row records error, sent_at is null."""
    order = _make_order(db_session)

    with app.app_context():
        with patch("solex.services.email.mail") as mock_mail:
            mock_mail.send.side_effect = Exception("SMTP timeout")
            from solex.services.email import EmailService
            EmailService().send("order_confirmation", "a@b.c", order=order)

    logs = db_session.query(EmailLog).all()
    assert len(logs) == 1
    log = logs[0]
    assert log.sent_at is None
    assert "SMTP timeout" in log.error


def test_message_subject_is_correct(app, db_session):
    """Verifies the correct subject line is used for order_confirmation."""
    order = _make_order(db_session)
    sent_messages = []

    with app.app_context():
        with patch("solex.services.email.mail") as mock_mail:
            def capture(msg):
                sent_messages.append(msg)
            mock_mail.send.side_effect = capture
            from solex.services.email import EmailService
            EmailService().send("order_confirmation", "a@b.c", order=order)

    assert len(sent_messages) == 1
    assert sent_messages[0].subject == "Your Solex order"
    assert sent_messages[0].recipients == ["a@b.c"]


def test_html_body_contains_order_token(app, db_session):
    """The rendered HTML email includes the order token."""
    order = _make_order(db_session)
    sent_messages = []

    with app.app_context():
        with patch("solex.services.email.mail") as mock_mail:
            def capture(msg):
                sent_messages.append(msg)
            mock_mail.send.side_effect = capture
            from solex.services.email import EmailService
            EmailService().send("order_confirmation", "a@b.c", order=order)

    assert "tok1" in sent_messages[0].html
    assert "tok1" in sent_messages[0].body


def test_checkout_integration_sends_email(db_session, product=None):
    """EmailService.send is called during a successful place_order."""
    # Just verify the hook in CheckoutService calls EmailService.send
    from solex.services.checkout import CheckoutService, CartLineIn, CustomerIn
    from solex.services.tax import FlatRateTaxStub
    from solex.services.shipping import FlatRateShippingStub
    from solex.services.inventory import InventoryService
    from solex.models import Product, Inventory
    from unittest.mock import MagicMock

    p = Product(
        sku="SK2", slug="sk2", name="Gadget",
        price_cents=2000, image_path="", active=True, weight_grams=50,
    )
    db_session.add(p)
    db_session.flush()
    db_session.add(Inventory(product_id=p.id, on_hand=5))
    db_session.commit()

    sq = MagicMock()
    sq.create_order.return_value = {"id": "sq_o_int"}
    sq.create_payment.return_value = {"id": "sq_p_int"}

    send_calls = []

    class FakeEmailService:
        def send(self, *a, **kw):
            send_calls.append((a, kw))

    # EmailService is lazily imported inside the checkout try block; patch the
    # class in its home module so `from solex.services.email import EmailService`
    # resolves to our fake.
    with patch("solex.services.email.EmailService", FakeEmailService):
        svc = CheckoutService(
            session=db_session,
            square=sq,
            tax=FlatRateTaxStub(0.0),
            shipping=FlatRateShippingStub(flat_cents=500, free_threshold_cents=99999),
            inventory=InventoryService(db_session),
        )
        svc.place_order(
            cart_lines=[CartLineIn(product_id=p.id, qty=1, price_cents=2000, name="Gadget", sku="SK2")],
            customer=CustomerIn(email="x@y.z", name="X Y"),
            shipping_addr={"region": "CA"},
            billing_addr={"region": "CA"},
            payment_token="cnon:t",
        )

    assert len(send_calls) == 1
    assert send_calls[0][0][0] == "order_confirmation"
    assert send_calls[0][0][1] == "x@y.z"
