import uuid
from datetime import datetime, timezone
from solex.models.auth import MagicLinkToken


def test_magic_link_token_fields():
    uid = uuid.uuid4()
    expires = datetime(2026, 12, 31, tzinfo=timezone.utc)
    t = MagicLinkToken(
        audience="customer",
        user_id=uid,
        token_hash="abc123",
        expires_at=expires,
    )
    assert t.audience == "customer"
    assert t.user_id == uid
    assert t.token_hash == "abc123"
    assert t.consumed_at is None
