import os
from flask import Blueprint, render_template, abort, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from sqlalchemy import select
from solex.extensions import db
from solex.models import Subscription
from solex.services.subscriptions import SubscriptionService
from solex.services.square_client import SquareClient, SquareConfig
from solex.services.checkout import CheckoutService
from solex.services.inventory import InventoryService
from solex.services.tax import FlatRateTaxStub
from solex.services.shipping import FlatRateShippingStub

bp = Blueprint("account_subscriptions", __name__, url_prefix="/account/subscriptions")


def _selfserve_enabled() -> bool:
    return os.environ.get("SOLEX_FLAG_SUB_SELFSERVE", "").lower() == "true"


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
        shipping=FlatRateShippingStub(c["SHIPPING_FLAT_CENTS"], c["SHIPPING_FREE_THRESHOLD_CENTS"]),
        inventory=InventoryService(db.session),
    )
    return SubscriptionService(db.session, sq, co)


@bp.get("/")
@login_required
def list_subs():
    subs = db.session.execute(
        select(Subscription).where(Subscription.customer_id == current_user.id)
                            .order_by(Subscription.created_at.desc())
    ).scalars().all()
    return render_template("account/subscriptions/list.html",
                           subs=subs, selfserve=_selfserve_enabled())


@bp.get("/<uuid:sid>")
@login_required
def detail(sid):
    sub = db.session.get(Subscription, sid)
    if sub is None or sub.customer_id != current_user.id:
        abort(404)
    return render_template("account/subscriptions/detail.html",
                           sub=sub, selfserve=_selfserve_enabled())


@bp.post("/<uuid:sid>/cancel")
@login_required
def cancel(sid):
    sub = db.session.get(Subscription, sid)
    if sub is None or sub.customer_id != current_user.id:
        abort(404)
    _svc().cancel(sub)
    flash("Subscription cancelled.", "ok")
    return redirect(url_for("account_subscriptions.list_subs"))


@bp.post("/<uuid:sid>/pause")
@login_required
def pause(sid):
    if not _selfserve_enabled():
        abort(403)
    sub = db.session.get(Subscription, sid)
    if sub is None or sub.customer_id != current_user.id:
        abort(404)
    _svc().pause(sub)
    flash("Subscription paused.", "ok")
    return redirect(url_for("account_subscriptions.detail", sid=sid))


@bp.post("/<uuid:sid>/resume")
@login_required
def resume(sid):
    if not _selfserve_enabled():
        abort(403)
    sub = db.session.get(Subscription, sid)
    if sub is None or sub.customer_id != current_user.id:
        abort(404)
    _svc().resume(sub)
    flash("Subscription resumed.", "ok")
    return redirect(url_for("account_subscriptions.detail", sid=sid))
