"""Checkout blueprint — view, submit, and order confirmation routes."""
from datetime import datetime, timedelta, timezone
from uuid import UUID
from flask import Blueprint, render_template, request, jsonify, abort, current_app, session
from flask_login import current_user
from redis import Redis
from sqlalchemy import select
from solex.extensions import db
from solex.services.cart import ValkeyCartBackend
from solex.services.checkout import CheckoutService, CartLineIn, CustomerIn, PaymentDeclined
from solex.services.square_client import SquareClient, SquareConfig, SquareError
from solex.services.inventory import InventoryService
from solex.services.tax import FlatRateTaxStub
from solex.services.shipping import FlatRateShippingStub
from solex.models import Order, Customer, Product

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

    # Subscription pre-flight: if any cart line has cadence_days, enforce login + store token
    has_sub_lines = any(l.get("cadence_days") for l in snap.lines)
    if has_sub_lines:
        if not (current_user.is_authenticated and isinstance(current_user, Customer)):
            return jsonify(error="login_required_for_subscription"), 400
        if not data.get("store_payment_token"):
            return jsonify(error="store_payment_token_required_for_subscription"), 400

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

    # Link the order to the logged-in customer if not already set
    if current_user.is_authenticated and isinstance(current_user, Customer):
        if order.customer_id is None:
            order.customer_id = current_user.id
            db.session.commit()

    # Post-checkout subscription creation
    sub_next_charge_at = None
    if has_sub_lines:
        sq = _square()
        customer = current_user  # already verified above
        try:
            if not customer.square_customer_id:
                sq_cust = sq.create_customer(
                    customer.email,
                    f"{customer.first_name or ''} {customer.last_name or ''}".strip() or customer.email,
                )
                customer.square_customer_id = sq_cust["id"]
                db.session.commit()

            card = sq.save_card_on_file(customer.square_customer_id, data["store_payment_token"])

            from solex.services.subscriptions import SubscriptionService

            cfg = current_app.config
            sub_svc = SubscriptionService(
                db.session, sq,
                CheckoutService(
                    session=db.session, square=sq,
                    tax=FlatRateTaxStub(cfg["TAX_RATE_PCT"]),
                    shipping=FlatRateShippingStub(cfg["SHIPPING_FLAT_CENTS"], cfg["SHIPPING_FREE_THRESHOLD_CENTS"]),
                    inventory=InventoryService(db.session),
                ),
            )

            for line in snap.lines:
                cadence = int(line.get("cadence_days") or 0)
                if cadence <= 0:
                    continue
                product = db.session.get(Product, UUID(line["product_id"]))
                if product is None:
                    continue
                starting_at = datetime.now(timezone.utc) + timedelta(days=cadence)
                sub_svc.create(
                    customer=customer, product=product, qty=line["qty"],
                    cadence_days=cadence, starting_at=starting_at,
                    square_card_id=card["id"],
                )
                sub_next_charge_at = sub_next_charge_at or starting_at
        except Exception as exc:
            # Subscription setup failures are non-fatal — order already placed.
            # Log and surface to caller so the frontend can inform the customer.
            current_app.logger.exception("subscription setup failed after successful payment")
            # Clear the cart before returning
            token = order.public_token
            session.pop("cart_key", None)
            if cart_key:
                try:
                    backend.redis.delete(backend._k(cart_key))
                except Exception:
                    pass
            return jsonify(order_token=token, subscription_error=str(exc)), 200

    # Clear the cart
    token = order.public_token
    session.pop("cart_key", None)
    if cart_key:
        try:
            backend.redis.delete(backend._k(cart_key))
        except Exception:
            pass

    resp_body = {"order_token": token}
    if sub_next_charge_at:
        resp_body["subscription_next_charge"] = sub_next_charge_at.strftime("%Y-%m-%d")
    return jsonify(resp_body), 200


@bp.get("/order/<token>")
def confirmation(token):
    order = db.session.execute(
        select(Order).where(Order.public_token == token)
    ).scalar_one_or_none()
    if order is None:
        abort(404)
    return render_template("checkout/order_confirmation.html", order=order)
