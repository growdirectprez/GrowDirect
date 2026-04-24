from typing import Optional
from sqlalchemy.orm import Session
from solex.models import Order, Refund
from solex.services.square_client import SquareClient
from solex.services.inventory import InventoryService


class RefundsService:
    def __init__(self, session: Session, square: SquareClient, inventory: InventoryService):
        self.session = session
        self.square = square
        self.inventory = inventory

    def issue_refund(self, order: Order, amount_cents: int, reason: str,
                     *, scenario_tag: Optional[str] = None) -> Refund:
        sq = self.square.create_refund(order.square_payment_id, amount_cents, reason)
        refund = Refund(
            order_id=order.id,
            square_refund_id=sq.get("id"),
            amount_cents=amount_cents,
            reason=reason,
            scenario_tag=scenario_tag,
        )
        self.session.add(refund)
        self.session.flush()
        if amount_cents >= order.total_cents:
            order.status = "refunded"
            self.inventory.increment_for_refund(refund)
        else:
            order.status = "partially_refunded"
        self.session.commit()
        return refund

    def issue_refund_by_payment_id(self, payment_id: str, amount_cents: int, reason: str) -> Refund:
        """Orphan-payment recovery (spec §4.10). Refund and persist a Refund
        row with order_id=NULL — we have no local Order for this payment."""
        sq = self.square.create_refund(payment_id, amount_cents, reason)
        refund = Refund(
            order_id=None,
            square_refund_id=sq.get("id"),
            amount_cents=amount_cents,
            reason=reason,
        )
        self.session.add(refund)
        self.session.commit()
        return refund
