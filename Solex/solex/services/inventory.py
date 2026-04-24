from sqlalchemy import select
from sqlalchemy.orm import Session
from solex.models import Inventory, InventoryAdjustment, Order, Refund

class InventoryError(Exception):
    pass

class InventoryService:
    def __init__(self, session: Session):
        self.session = session

    def on_hand(self, product_id) -> int:
        inv = self.session.execute(
            select(Inventory).where(Inventory.product_id == product_id).with_for_update()
        ).scalar_one_or_none()
        return inv.on_hand if inv else 0

    def adjust(self, product_id, delta: int, reason: str, **ctx) -> InventoryAdjustment:
        inv = self.session.execute(
            select(Inventory).where(Inventory.product_id == product_id).with_for_update()
        ).scalar_one_or_none()
        if inv is None:
            inv = Inventory(product_id=product_id, on_hand=0)
            self.session.add(inv)
            self.session.flush()
        inv.on_hand += delta
        adj = InventoryAdjustment(product_id=product_id, delta=delta, reason=reason, **ctx)
        self.session.add(adj)
        self.session.flush()
        return adj

    def decrement_for_order(self, order: Order):
        for item in order.items:
            self.adjust(item.product_id, -item.qty, reason="sale", order_id=order.id)

    def increment_for_refund(self, refund: Refund):
        order = self.session.get(Order, refund.order_id) if refund.order_id else None
        if order is None:
            return
        for item in order.items:
            self.adjust(item.product_id, item.qty, reason="refund",
                        order_id=order.id, refund_id=refund.id)
