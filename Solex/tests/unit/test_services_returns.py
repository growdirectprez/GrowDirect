from unittest.mock import MagicMock
from datetime import datetime, timezone
import pytest
from solex.services.returns import ReturnsService, ReturnsError
from solex.services.refunds import RefundsService
from solex.services.inventory import InventoryService
from solex.models import (
    Order, OrderItem, AdminUser, Product, Inventory, ReturnRequest
)


def _seed(db_session):
    p = Product(sku="R1", slug="r1", name="R Product", price_cents=2000,
                image_path="", active=True, weight_grams=1)
    db_session.add(p); db_session.flush()
    db_session.add(Inventory(product_id=p.id, on_hand=5))
    order = Order(
        public_token="ret1", customer_email="cust@example.com",
        customer_name="Cust", shipping_address_json={}, billing_address_json={},
        subtotal_cents=2000, tax_cents=0, shipping_cents=0, total_cents=2000,
        square_order_id="sqo_ret1", square_payment_id="sqp_ret1",
        placed_at=datetime.now(timezone.utc), status="paid",
    )
    db_session.add(order); db_session.flush()
    db_session.add(OrderItem(
        order_id=order.id, product_id=p.id,
        sku_snapshot="R1", name_snapshot="R Product",
        price_snapshot_cents=2000, qty=1, line_total_cents=2000,
    ))
    admin = AdminUser(email="admin@solex.local", active=True)
    db_session.add(admin)
    db_session.commit()
    return order, admin


def _make_service(db_session, square_mock=None, email_mock=None):
    sq = square_mock or MagicMock()
    sq.create_refund.return_value = {"id": "sqr_ret1"}
    inv_svc = InventoryService(db_session)
    refunds = RefundsService(db_session, sq, inv_svc)
    email = email_mock or MagicMock()
    return ReturnsService(db_session, refunds, email)


def test_request_creates_pending_return(app, db_session):
    order, admin = _seed(db_session)
    svc = _make_service(db_session)
    req = svc.request(order, reason="Wrong size")
    assert req.id is not None
    assert req.status == "pending"
    assert req.order_id == order.id
    assert req.reason == "Wrong size"


def test_approve_completes_return_and_issues_refund(app, db_session):
    order, admin = _seed(db_session)
    svc = _make_service(db_session)
    req = svc.request(order, reason="Damaged")
    result = svc.approve(req, admin)
    assert result.status == "completed"
    assert result.refund_id is not None
    assert result.resolved_at is not None
    assert result.approved_by_admin_user_id == admin.id


def test_approve_sends_email(app, db_session):
    order, admin = _seed(db_session)
    email = MagicMock()
    svc = _make_service(db_session, email_mock=email)
    req = svc.request(order, reason="Damaged")
    svc.approve(req, admin)
    email.send.assert_called_once()
    call_kwargs = email.send.call_args
    assert call_kwargs[0][0] == "return_approved"


def test_approve_raises_if_not_pending(app, db_session):
    order, admin = _seed(db_session)
    svc = _make_service(db_session)
    req = svc.request(order, reason="X")
    svc.approve(req, admin)
    with pytest.raises(ReturnsError, match="cannot approve"):
        svc.approve(req, admin)


def test_deny_sets_denied_status(app, db_session):
    order, admin = _seed(db_session)
    svc = _make_service(db_session)
    req = svc.request(order, reason="Y")
    result = svc.deny(req, admin, reason="Policy violation")
    assert result.status == "denied"
    assert result.resolved_at is not None
    assert result.approved_by_admin_user_id == admin.id


def test_deny_raises_if_not_pending(app, db_session):
    order, admin = _seed(db_session)
    svc = _make_service(db_session)
    req = svc.request(order, reason="Z")
    svc.deny(req, admin)
    with pytest.raises(ReturnsError, match="cannot deny"):
        svc.deny(req, admin)
