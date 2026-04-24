from datetime import datetime, timezone
from solex.models.ops import SquareWebhookEvent, EmailLog


def test_square_webhook_event_fields():
    now = datetime.now(timezone.utc)
    e = SquareWebhookEvent(
        square_event_id="evt_123",
        event_type="payment.completed",
        payload_json={"foo": "bar"},
        received_at=now,
    )
    assert e.square_event_id == "evt_123"
    assert e.event_type == "payment.completed"
    assert e.processed_at is None


def test_email_log_fields():
    el = EmailLog(template="order_confirmation", to="buyer@example.com")
    assert el.template == "order_confirmation"
    assert el.sent_at is None
