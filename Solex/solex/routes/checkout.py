"""Checkout blueprint — view, submit, and order confirmation routes."""
from flask import Blueprint, render_template, request, jsonify, abort, current_app, session
from redis import Redis
from sqlalchemy import select
from solex.extensions import db
from solex.services.cart import ValkeyCartBackend
from solex.services.checkout import CheckoutService, CartLineIn, CustomerIn, PaymentDeclined
from solex.services.square_client import SquareClient, SquareConfig, SquareError
from solex.services.inventory import InventoryService
from solex.services.tax import FlatRateTaxStub
from solex.services.shipping import FlatRateShippingStub
from solex.models import Order

bp = Blueprint("checkout", __name__)


def _square() -> SquareClient:
    c = current_app.config
    return SquareClient(
        SquareConfig(
            access_token=c["SQUARE_ACCESS_TOKEN"],
            environment=c["SQUARE_ENVIRONMENT"],
            location_id=c["SQUARE_LOCATION_ID"],
            webhook_signature_key=c["SQUARE_WEBHOOK_SIGNATURE_KEY"],
        )
    )


def _cart_backend() -> ValkeyCartBackend:
    return ValkeyCartBackend(Redis.from_url(current_app.config["VALKEY_URL"]))


@bp.get("/checkout")
def view():
    cart_key = session.get("cart_key", "")
    snap = _cart_backend().load(cart_key)
    if not snap.lines:
        return render_template("checkout/empty.html"), 200
    return render_template(
        "checkout/checkout.html",
        cart=snap,
        square_app_id=current_app.config.get("SQUARE_APPLICATION_ID", ""),
        square_location_id=current_app.config.get("SQUARE_LOCATION_ID", ""),
        square_environment=current_app.config.get("SQUARE_ENVIRONMENT", "sandbox"),
    )


@bp.post("/checkout/submit")
def submit():
    data = request.get_json(force=True)
    cart_key = session.get("cart_key", "")
    backend = _cart_backend()
    snap = backend.load(cart_key)

    if not snap.lines:
        return jsonify(error="empty_cart"), 400

    cart_lines = [
        CartLineIn(
            product_id=l["product_id"],
            qty=l["qty"],
            price_cents=l["price_cents"],
            name=l["name"],
            sku=l["sku"],
            image_path=l.get("image_path", ""),
        )
        for l in snap.lines
    ]

    cfg = current_app.config
    svc = CheckoutService(
        session=db.session,
        square=_square(),
        tax=FlatRateTaxStub(rate_pct=cfg["TAX_RATE_PCT"]),
        shipping=FlatRateShippingStub(
            flat_cents=cfg["SHIPPING_FLAT_CENTS"],
            free_threshold_cents=cfg["SHIPPING_FREE_THRESHOLD_CENTS"],
        ),
        inventory=InventoryService(db.session),
    )

    try:
        order = svc.place_order(
            cart_lines=cart_lines,
            customer=CustomerIn(email=data["email"], name=data["name"]),
            shipping_addr=data["shipping_address"],
            billing_addr=data.get("billing_address", data["shipping_address"]),
            payment_token=data["payment_token"],
        )
    except PaymentDeclined as e:
        return jsonify(error="declined", detail=str(e)), 402
    except SquareError as e:
        return jsonify(error="payment_failed", detail=str(e)), 502

    # Clear the cart
    token = order.public_token
    session.pop("cart_key", None)
    if cart_key:
        try:
            backend.redis.delete(backend._k(cart_key))
        except Exception:
            pass

    return jsonify(order_token=token), 200


@bp.get("/order/<token>")
def confirmation(token):
    order = db.session.execute(
        select(Order).where(Order.public_token == token)
    ).scalar_one_or_none()
    if order is None:
        abort(404)
    return render_template("checkout/order_confirmation.html", order=order)
