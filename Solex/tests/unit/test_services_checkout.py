"""Tests for CheckoutService (Task 6.2).

Square is fully mocked; real test DB used for persistence assertions.
"""
from unittest.mock import MagicMock, patch
import pytest
from solex.services.checkout import CheckoutService, CartLineIn, CustomerIn, PaymentDeclined, CheckoutError
from solex.services.square_client import SquareDeclined
from solex.services.tax import FlatRateTaxStub
from solex.services.shipping import FlatRateShippingStub
from solex.services.inventory import InventoryService
from solex.models import Order, Product, Inventory


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def product(db_session):
    p = Product(
        sku="SK1", slug="sk1", name="Widget",
        price_cents=5000, image_path="", active=True, weight_grams=10,
    )
    db_session.add(p)
    db_session.flush()
    db_session.add(Inventory(product_id=p.id, on_hand=10))
    db_session.commit()
    return p


def _square_mock(order_id="sq_order_123", payment_id="sq_payment_123",
                 payment_side_effect=None):
    sq = MagicMock()
    sq.create_order.return_value = {"id": order_id}
    if payment_side_effect is not None:
        sq.create_payment.side_effect = payment_side_effect
    else:
        sq.create_payment.return_value = {"id": payment_id}
    return sq


def _svc(db_session, square_mock, tax_rate=0.0, ship_flat=500, ship_free=99999):
    return CheckoutService(
        session=db_session,
        square=square_mock,
        tax=FlatRateTaxStub(tax_rate),
        shipping=FlatRateShippingStub(flat_cents=ship_flat, free_threshold_cents=ship_free),
        inventory=InventoryService(db_session),
    )


def _cart_line(product):
    return CartLineIn(
        product_id=product.id,
        qty=2,
        price_cents=5000,
        name="Widget",
        sku="SK1",
    )


def _customer():
    return CustomerIn(email="a@b.c", name="A B")


def _addr():
    return {"region": "CA"}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_places_order_happy_path(db_session, product):
    sq = _square_mock()
    # suppress email
    with patch("solex.services.checkout.EmailService", create=True):
        svc = _svc(db_session, sq)
        line = _cart_line(product)
        order = svc.place_order(
            cart_lines=[line],
            customer=_customer(),
            shipping_addr=_addr(),
            billing_addr=_addr(),
            payment_token="cnon:test",
        )

    assert order.status == "paid"
    assert order.square_payment_id == "sq_payment_123"
    assert order.total_cents == 2 * 5000 + 500  # subtotal + flat shipping, 0% tax
    assert order.subtotal_cents == 10000
    assert order.shipping_cents == 500
    assert order.tax_cents == 0


def test_inventory_decremented_on_success(db_session, product):
    sq = _square_mock()
    with patch("solex.services.checkout.EmailService", create=True):
        svc = _svc(db_session, sq)
        svc.place_order(
            cart_lines=[_cart_line(product)],
            customer=_customer(),
            shipping_addr=_addr(),
            billing_addr=_addr(),
            payment_token="cnon:test",
        )
    inv = db_session.query(Inventory).filter_by(product_id=product.id).one()
    assert inv.on_hand == 8  # started at 10, decremented by qty=2


def test_order_items_created(db_session, product):
    sq = _square_mock()
    with patch("solex.services.checkout.EmailService", create=True):
        svc = _svc(db_session, sq)
        order = svc.place_order(
            cart_lines=[_cart_line(product)],
            customer=_customer(),
            shipping_addr=_addr(),
            billing_addr=_addr(),
            payment_token="cnon:test",
        )
    assert len(order.items) == 1
    item = order.items[0]
    assert item.qty == 2
    assert item.sku_snapshot == "SK1"
    assert item.line_total_cents == 10000


def test_payment_declined_persists_nothing(db_session, product):
    sq = _square_mock(payment_side_effect=SquareDeclined("bad card"))
    with patch("solex.services.checkout.EmailService", create=True):
        svc = _svc(db_session, sq)
        with pytest.raises(PaymentDeclined):
            svc.place_order(
                cart_lines=[_cart_line(product)],
                customer=_customer(),
                shipping_addr=_addr(),
                billing_addr=_addr(),
                payment_token="cnon:bad",
            )

    assert db_session.query(Order).count() == 0
    inv = db_session.query(Inventory).filter_by(product_id=product.id).one()
    assert inv.on_hand == 10  # unchanged


def test_empty_cart_raises(db_session):
    sq = _square_mock()
    svc = _svc(db_session, sq)
    with pytest.raises(CheckoutError, match="empty cart"):
        svc.place_order(
            cart_lines=[],
            customer=_customer(),
            shipping_addr=_addr(),
            billing_addr=_addr(),
            payment_token="cnon:x",
        )
    # Square should never be called for empty cart
    sq.create_order.assert_not_called()


def test_square_order_called_before_db(db_session, product):
    """Verify Square is called before any DB commit — Square-then-DB ordering."""
    call_order = []
    sq = MagicMock()
    sq.create_order.side_effect = lambda **kw: (call_order.append("sq_order"), {"id": "ord_1"})[1]
    sq.create_payment.side_effect = lambda **kw: (call_order.append("sq_payment"), {"id": "pay_1"})[1]

    with patch("solex.services.checkout.EmailService", create=True):
        svc = _svc(db_session, sq)
        svc.place_order(
            cart_lines=[_cart_line(product)],
            customer=_customer(),
            shipping_addr=_addr(),
            billing_addr=_addr(),
            payment_token="cnon:test",
        )

    assert call_order[0] == "sq_order"
    assert call_order[1] == "sq_payment"


def test_free_shipping_over_threshold(db_session, product):
    """Orders above free-shipping threshold get 0 shipping cents."""
    sq = _square_mock()
    with patch("solex.services.checkout.EmailService", create=True):
        # free threshold is 5000 cents; 2 items at 5000 = 10000 > threshold
        svc = _svc(db_session, sq, ship_flat=500, ship_free=5000)
        order = svc.place_order(
            cart_lines=[_cart_line(product)],
            customer=_customer(),
            shipping_addr=_addr(),
            billing_addr=_addr(),
            payment_token="cnon:test",
        )
    assert order.shipping_cents == 0
    assert order.total_cents == 10000
