from flask import Blueprint, render_template, redirect, url_for, flash, abort, current_app
from sqlalchemy import select
from solex.extensions import db
from solex.models import Subscription
from solex.services.subscriptions import SubscriptionService
from solex.services.square_client import SquareClient, SquareConfig
from solex.services.checkout import CheckoutService
from solex.services.inventory import InventoryService
from solex.services.tax import FlatRateTaxStub
from solex.services.shipping import FlatRateShippingStub
from solex.routes.admin_utils import admin_required

bp = Blueprint("admin_subscriptions", __name__, url_prefix="/admin/subscriptions")


def _svc():
    c = current_app.config
    sq = SquareClient(SquareConfig(
        access_token=c["SQUARE_ACCESS_TOKEN"],
        environment=c["SQUARE_ENVIRONMENT"],
        location_id=c["SQUARE_LOCATION_ID"],
        webhook_signature_key=c["SQUARE_WEBHOOK_SIGNATURE_KEY"],
    ))
    co = CheckoutService(
        session=db.session,
        square=sq,
        tax=FlatRateTaxStub(c["TAX_RATE_PCT"]),
        shipping=FlatRateShippingStub(
            c["SHIPPING_FLAT_CENTS"],
            c["SHIPPING_FREE_THRESHOLD_CENTS"],
        ),
        inventory=InventoryService(db.session),
    )
    return SubscriptionService(db.session, sq, co)


@bp.get("/")
@admin_required
def list_subs():
    subs = db.session.execute(
        select(Subscription).order_by(Subscription.created_at.desc())
    ).scalars().all()
    return render_template("admin/subscriptions/list.html", subs=subs)


@bp.get("/<uuid:sid>")
@admin_required
def detail(sid):
    sub = db.session.get(Subscription, sid)
    if sub is None:
        abort(404)
    return render_template("admin/subscriptions/detail.html", sub=sub)


@bp.post("/<uuid:sid>/pause")
@admin_required
def force_pause(sid):
    sub = db.session.get(Subscription, sid)
    if sub is None:
        abort(404)
    _svc().pause(sub)
    flash("Paused.", "ok")
    return redirect(url_for("admin_subscriptions.detail", sid=sid))


@bp.post("/<uuid:sid>/cancel")
@admin_required
def force_cancel(sid):
    sub = db.session.get(Subscription, sid)
    if sub is None:
        abort(404)
    _svc().cancel(sub)
    flash("Cancelled.", "ok")
    return redirect(url_for("admin_subscriptions.detail", sid=sid))
