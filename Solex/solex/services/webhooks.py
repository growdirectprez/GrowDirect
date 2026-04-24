from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from solex.models import SquareWebhookEvent, Order
from solex.services.square_client import SquareClient
from solex.services.refunds import RefundsService


class BadSignature(Exception):
    ...


class WebhooksService:
    def __init__(self, session: Session, square: SquareClient, refunds: RefundsService):
        self.session = session
        self.square = square
        self.refunds = refunds

    def handle(self, *, square_event_id: str, event_type: str,
               body: bytes, signature: str, url: str,
               payload: dict) -> SquareWebhookEvent:
        if not self.square.verify_webhook_signature(url, body, signature):
            raise BadSignature()

        # Dedupe via unique constraint on square_event_id
        try:
            event = SquareWebhookEvent(
                square_event_id=square_event_id,
                event_type=event_type,
                payload_json=payload,
                received_at=datetime.now(timezone.utc),
            )
            self.session.add(event)
            self.session.flush()
        except IntegrityError:
            self.session.rollback()
            # Already processed — return the existing row (no-op)
            return self.session.execute(
                select(SquareWebhookEvent).where(
                    SquareWebhookEvent.square_event_id == square_event_id
                )
            ).scalar_one()

        try:
            self._dispatch(event_type, payload)
            event.processed_at = datetime.now(timezone.utc)
        except Exception as e:
            event.error = str(e)[:500]
        self.session.commit()
        return event

    def _dispatch(self, event_type: str, payload: dict):
        data = (payload.get("data") or {}).get("object") or {}
        if event_type == "payment.updated":
            self._handle_payment_updated(data.get("payment") or {})
        elif event_type == "refund.updated":
            self._handle_refund_updated(data.get("refund") or {})
        elif event_type == "order.updated":
            # No-op for Plan 1 — Plan 2's admin UI will use this
            pass

    def _handle_payment_updated(self, payment: dict):
        payment_id = payment.get("id")
        if not payment_id:
            return
        order = self.session.execute(
            select(Order).where(Order.square_payment_id == payment_id)
        ).scalar_one_or_none()
        if order is not None:
            # Normal case: local order exists; webhook is informational for now
            return
        # Orphan-payment recovery
        amount = int(((payment.get("amount_money") or {}).get("amount")) or 0)
        if amount <= 0:
            return
        self.refunds.issue_refund_by_payment_id(payment_id, amount, reason="orphan-recovery")

    def _handle_refund_updated(self, refund: dict):
        from solex.models import Refund
        refund_id = refund.get("id")
        if not refund_id:
            return
        existing = self.session.execute(
            select(Refund).where(Refund.square_refund_id == refund_id)
        ).scalar_one_or_none()
        if existing is None:
            # We don't know about this refund; ignore (may be another app's)
            return
        # Could update status fields if we tracked them; for Plan 1 this is a touchpoint
