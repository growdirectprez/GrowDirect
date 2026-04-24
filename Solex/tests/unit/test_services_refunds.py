from unittest.mock import MagicMock
from datetime import datetime, timezone
from solex.services.refunds import RefundsService
from solex.services.inventory import InventoryService
from solex.models import Order, OrderItem, Refund, Inventory, Product


def _order_with_item(db_session):
    p = Product(sku="A", slug="a", name="A", price_cents=1000,
                image_path="", active=True, weight_grams=1)
    db_session.add(p); db_session.flush()
    db_session.add(Inventory(product_id=p.id, on_hand=5))
    order = Order(
        public_token="t1", customer_email="a@b.c", customer_name="A",
        shipping_address_json={}, billing_address_json={},
        subtotal_cents=1000, tax_cents=0, shipping_cents=0, total_cents=1000,
        square_order_id="o1", square_payment_id="p1",
        placed_at=datetime.now(timezone.utc), status="paid",
    )
    db_session.add(order); db_session.flush()
    db_session.add(OrderItem(order_id=order.id, product_id=p.id, sku_snapshot="A",
                             name_snapshot="A", price_snapshot_cents=1000, qty=1,
                             line_total_cents=1000))
    # decrement inventory like a sale would have
    inv = db_session.query(Inventory).filter_by(product_id=p.id).one()
    inv.on_hand = 4
    db_session.commit()
    return order, p


def test_full_refund_restores_inventory(app, db_session):
    order, product = _order_with_item(db_session)
    sq = MagicMock(); sq.create_refund.return_value = {"id": "sqr_1"}
    svc = RefundsService(db_session, sq, InventoryService(db_session))
    refund = svc.issue_refund(order, 1000, reason="customer-request")
    assert refund.square_refund_id == "sqr_1"
    db_session.refresh(order)
    assert order.status == "refunded"
    inv = db_session.query(Inventory).filter_by(product_id=product.id).one()
    assert inv.on_hand == 5


def test_partial_refund_does_not_restore_inventory(app, db_session):
    order, product = _order_with_item(db_session)
    sq = MagicMock(); sq.create_refund.return_value = {"id": "sqr_2"}
    svc = RefundsService(db_session, sq, InventoryService(db_session))
    refund = svc.issue_refund(order, 500, reason="customer-request")
    db_session.refresh(order)
    assert order.status == "partially_refunded"
    inv = db_session.query(Inventory).filter_by(product_id=product.id).one()
    assert inv.on_hand == 4


def test_orphan_refund_creates_refund_with_null_order(app, db_session):
    sq = MagicMock(); sq.create_refund.return_value = {"id": "sqr_3"}
    svc = RefundsService(db_session, sq, InventoryService(db_session))
    refund = svc.issue_refund_by_payment_id("p-orphan", 5000, reason="orphan-recovery")
    assert refund.order_id is None
    assert refund.square_refund_id == "sqr_3"
