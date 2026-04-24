import uuid
import pytest
from solex.models import Product, Category, Inventory, InventoryAdjustment, Order, OrderItem
from solex.services.inventory import InventoryService
from datetime import datetime, timezone


def _make_product(session, sku="TEST-001"):
    cat = Category(slug="test-cat", name="Test", sort=0)
    session.add(cat)
    session.flush()
    prod = Product(
        sku=sku,
        slug=f"test-product-{sku.lower()}",
        name="Test Product",
        price_cents=1000,
        active=True,
        weight_grams=100,
    )
    session.add(prod)
    session.flush()
    return prod


def test_adjust_creates_adj_and_updates_on_hand(app, db_session):
    with app.app_context():
        prod = _make_product(db_session)
        inv_row = Inventory(product_id=prod.id, on_hand=10)
        db_session.add(inv_row)
        db_session.flush()

        svc = InventoryService(db_session)
        adj = svc.adjust(prod.id, -3, reason="sale")

        assert isinstance(adj, InventoryAdjustment)
        assert adj.delta == -3
        assert adj.reason == "sale"
        assert inv_row.on_hand == 7


def test_adjust_inserts_inventory_when_missing(app, db_session):
    with app.app_context():
        prod = _make_product(db_session, sku="TEST-002")

        svc = InventoryService(db_session)
        adj = svc.adjust(prod.id, 5, reason="initial")

        assert adj.delta == 5
        inv = db_session.execute(
            __import__("sqlalchemy", fromlist=["select"]).select(Inventory)
            .where(Inventory.product_id == prod.id)
        ).scalar_one()
        assert inv.on_hand == 5


def test_decrement_for_order(app, db_session):
    with app.app_context():
        prod = _make_product(db_session, sku="TEST-003")
        inv_row = Inventory(product_id=prod.id, on_hand=20)
        db_session.add(inv_row)
        db_session.flush()

        order = Order(
            public_token="tok-abc123",
            customer_email="test@example.com",
            customer_name="Test Customer",
            shipping_address_json={"line1": "123 Main St"},
            billing_address_json={"line1": "123 Main St"},
            subtotal_cents=2000,
            tax_cents=0,
            shipping_cents=0,
            total_cents=2000,
            currency="USD",
            status="paid",
            square_order_id="sq-order-001",
            placed_at=datetime.now(timezone.utc),
        )
        db_session.add(order)
        db_session.flush()

        item = OrderItem(
            order_id=order.id,
            product_id=prod.id,
            sku_snapshot="TEST-003",
            name_snapshot="Test Product",
            image_path_snapshot="",
            price_snapshot_cents=1000,
            qty=2,
            line_total_cents=2000,
        )
        db_session.add(item)
        db_session.flush()

        svc = InventoryService(db_session)
        svc.decrement_for_order(order)

        assert inv_row.on_hand == 18
        adj = db_session.execute(
            __import__("sqlalchemy", fromlist=["select"]).select(InventoryAdjustment)
            .where(InventoryAdjustment.order_id == order.id)
        ).scalar_one()
        assert adj.delta == -2
        assert adj.reason == "sale"
