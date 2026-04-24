from datetime import datetime, timezone
from solex.models.cart import Cart, CartLine


def test_cart_fields():
    now = datetime.now(timezone.utc)
    c = Cart(last_activity_at=now, session_key="abc123")
    assert c.session_key == "abc123"
    assert c.last_activity_at == now


def test_cart_line_fields():
    import uuid
    cl = CartLine(
        cart_id=uuid.uuid4(),
        product_id=uuid.uuid4(),
        qty=2,
        price_snapshot_cents=4995,
    )
    assert cl.qty == 2
    assert cl.price_snapshot_cents == 4995
