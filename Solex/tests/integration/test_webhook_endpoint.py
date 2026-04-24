import json
import hmac
import hashlib
import base64


def _sign(url: str, body: bytes, key: str) -> str:
    return base64.b64encode(
        hmac.new(key.encode(), (url + body.decode()).encode(), hashlib.sha256).digest()
    ).decode()


def _make_payload():
    return {
        "event_id": "evt_test_1",
        "type": "payment.updated",
        "data": {"object": {"payment": {"id": "p-test", "amount_money": {"amount": 1500}}}},
    }


def test_webhook_accepts_valid_signature(app, client, db_session, monkeypatch):
    key = "test-whk"
    monkeypatch.setitem(app.config, "SQUARE_WEBHOOK_SIGNATURE_KEY", key)
    # Stub the orphan-recovery refund to avoid hitting real Square
    from solex.services import square_client as sq_module
    monkeypatch.setattr(
        sq_module.SquareClient,
        "create_refund",
        lambda self, payment_id, amount_cents, reason=None: {"id": "sqr_stub"},
    )
    payload = _make_payload()
    body = json.dumps(payload).encode()
    url = "http://localhost/api/webhooks/square"
    sig = _sign(url, body, key)
    resp = client.post(
        "/api/webhooks/square",
        data=body,
        headers={
            "X-Square-HmacSha256-Signature": sig,
            "Content-Type": "application/json",
        },
    )
    assert resp.status_code == 204
    from solex.models import SquareWebhookEvent
    assert db_session.query(SquareWebhookEvent).count() == 1


def test_webhook_rejects_bad_signature(app, client, monkeypatch):
    monkeypatch.setitem(app.config, "SQUARE_WEBHOOK_SIGNATURE_KEY", "test-whk")
    payload = _make_payload()
    body = json.dumps(payload).encode()
    resp = client.post(
        "/api/webhooks/square",
        data=body,
        headers={
            "X-Square-HmacSha256-Signature": "wrong-sig",
            "Content-Type": "application/json",
        },
    )
    assert resp.status_code == 401


def test_webhook_rejects_missing_event_id(app, client, monkeypatch):
    key = "test-whk"
    monkeypatch.setitem(app.config, "SQUARE_WEBHOOK_SIGNATURE_KEY", key)
    # Payload missing event_id — should 400
    payload = {"type": "payment.updated"}
    body = json.dumps(payload).encode()
    url = "http://localhost/api/webhooks/square"
    sig = _sign(url, body, key)
    resp = client.post(
        "/api/webhooks/square",
        data=body,
        headers={
            "X-Square-HmacSha256-Signature": sig,
            "Content-Type": "application/json",
        },
    )
    assert resp.status_code == 400
