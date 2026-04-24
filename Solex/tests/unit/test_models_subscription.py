from datetime import datetime, timezone
from solex.models.subscription import Subscription, SubscriptionCharge

def test_subscription_fields():
    s = Subscription(
        qty=1, cadence_days=30, square_card_id="ccof:card_abc",
        next_charge_at=datetime.now(timezone.utc), status="active",
    )
    assert s.cadence_days == 30
    assert s.status == "active"

def test_subscription_charge_fields():
    c = SubscriptionCharge(attempted_at=datetime.now(timezone.utc), succeeded=True)
    assert c.succeeded is True
