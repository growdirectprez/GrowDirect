from unittest.mock import MagicMock
import pytest
from solex.services.webhooks import WebhooksService, BadSignature
from solex.models import SquareWebhookEvent, Order
from datetime import datetime, timezone


def _sq(verify_return=True):
    sq = MagicMock()
    sq.verify_webhook_signature.return_value = verify_return
    return sq


def _refunds_mock():
    m = MagicMock()
    m.issue_refund_by_payment_id.return_value = None
    return m


def test_bad_signature_raises(db_session):
    svc = WebhooksService(db_session, _sq(verify_return=False), _refunds_mock())
    with pytest.raises(BadSignature):
        svc.handle(square_event_id="e1", event_type="payment.updated",
                   body=b"{}", signature="bogus", url="http://x", payload={})


def test_happy_path_no_orphan(db_session):
    order = Order(
        public_token="t", customer_email="a@b.c", customer_name="A",
        shipping_address_json={}, billing_address_json={},
        subtotal_cents=100, total_cents=100,
        square_order_id="o1", square_payment_id="p1",
        placed_at=datetime.now(timezone.utc), status="paid",
    )
    db_session.add(order); db_session.commit()

    refunds = _refunds_mock()
    svc = WebhooksService(db_session, _sq(), refunds)
    payload = {"data": {"object": {"payment": {"id": "p1", "amount_money": {"amount": 100}}}}}
    svc.handle(square_event_id="e-local", event_type="payment.updated",
               body=b"{}", signature="sig", url="http://x", payload=payload)
    refunds.issue_refund_by_payment_id.assert_not_called()

    events = db_session.query(SquareWebhookEvent).all()
    assert len(events) == 1
    assert events[0].processed_at is not None


def test_orphan_payment_triggers_refund(db_session):
    refunds = _refunds_mock()
    svc = WebhooksService(db_session, _sq(), refunds)
    payload = {"data": {"object": {"payment": {"id": "p-orphan", "amount_money": {"amount": 2500}}}}}
    svc.handle(square_event_id="e-orphan", event_type="payment.updated",
               body=b"{}", signature="sig", url="http://x", payload=payload)
    refunds.issue_refund_by_payment_id.assert_called_once_with("p-orphan", 2500, reason="orphan-recovery")


def test_dedup_ignores_second_delivery(db_session):
    refunds = _refunds_mock()
    svc = WebhooksService(db_session, _sq(), refunds)
    payload = {"data": {"object": {"payment": {"id": "p2", "amount_money": {"amount": 500}}}}}
    svc.handle(square_event_id="dup", event_type="payment.updated",
               body=b"{}", signature="sig", url="http://x", payload=payload)
    svc.handle(square_event_id="dup", event_type="payment.updated",
               body=b"{}", signature="sig", url="http://x", payload=payload)
    assert db_session.query(SquareWebhookEvent).count() == 1
    # First handle did one orphan-refund; second was a no-op
    assert refunds.issue_refund_by_payment_id.call_count == 1
