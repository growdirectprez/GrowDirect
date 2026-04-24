from flask import Blueprint, jsonify, request, abort, current_app
from redis import Redis
from sqlalchemy import text as sql_text

from solex.extensions import db, limiter

bp = Blueprint("api", __name__)


@bp.get("/health")
def health():
    ok = {"ok": True, "db": False, "valkey": False, "version": "0.1.0"}
    try:
        db.session.execute(sql_text("SELECT 1"))
        ok["db"] = True
    except Exception:
        ok["ok"] = False
    try:
        Redis.from_url(current_app.config["VALKEY_URL"]).ping()
        ok["valkey"] = True
    except Exception:
        ok["ok"] = False
    return jsonify(ok), (200 if ok["ok"] else 503)


def _webhook_services():
    from solex.services.square_client import SquareClient, SquareConfig
    from solex.services.inventory import InventoryService
    from solex.services.refunds import RefundsService
    from solex.services.webhooks import WebhooksService
    c = current_app.config
    sq = SquareClient(SquareConfig(
        access_token=c["SQUARE_ACCESS_TOKEN"],
        environment=c["SQUARE_ENVIRONMENT"],
        location_id=c["SQUARE_LOCATION_ID"],
        webhook_signature_key=c["SQUARE_WEBHOOK_SIGNATURE_KEY"],
    ))
    return sq, WebhooksService(
        db.session, sq,
        RefundsService(db.session, sq, InventoryService(db.session)),
    )


@bp.post("/api/webhooks/square")
@limiter.limit("120 per minute")
def square_webhook():
    from solex.services.webhooks import BadSignature
    body = request.get_data()
    sig = request.headers.get("X-Square-HmacSha256-Signature", "")
    url = request.url
    try:
        payload = request.get_json(force=True)
        _, svc = _webhook_services()
        svc.handle(
            square_event_id=payload["event_id"],
            event_type=payload["type"],
            body=body, signature=sig, url=url,
            payload=payload,
        )
    except BadSignature:
        abort(401)
    except KeyError:
        abort(400)
    return "", 204
