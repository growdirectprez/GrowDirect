from datetime import datetime, timezone
from solex.models.order import Order, OrderItem, OrderNote, ORDER_STATUSES


def test_order_fields():
    now = datetime.now(timezone.utc)
    o = Order(
        public_token="TOK123",
        customer_email="buyer@example.com",
        customer_name="Jane Doe",
        shipping_address_json={},
        billing_address_json={},
        subtotal_cents=4995,
        total_cents=4995,
        square_order_id="SQ-ORDER-1",
        placed_at=now,
    )
    assert o.public_token == "TOK123"
    assert o.subtotal_cents == 4995


def test_order_statuses():
    assert "pending" in ORDER_STATUSES
    assert "paid" in ORDER_STATUSES


def test_order_item_fields():
    import uuid
    oi = OrderItem(
        order_id=uuid.uuid4(),
        sku_snapshot="AO-YOUTH-30",
        name_snapshot="AO Youth 30ct",
        price_snapshot_cents=4995,
        qty=1,
        line_total_cents=4995,
    )
    assert oi.sku_snapshot == "AO-YOUTH-30"
    assert oi.qty == 1


def test_order_note_fields():
    import uuid
    n = OrderNote(order_id=uuid.uuid4(), body="Note text")
    assert n.body == "Note text"
