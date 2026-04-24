from flask import Blueprint, render_template, redirect, url_for, flash, abort, request, current_app
from sqlalchemy import select
from solex.extensions import db
from solex.models import Order, Refund
from solex.services.refunds import RefundsService
from solex.services.square_client import SquareClient, SquareConfig
from solex.services.inventory import InventoryService
from solex.routes.admin_utils import admin_required

bp = Blueprint("admin_orders", __name__, url_prefix="/admin/orders")


def _refunds_svc():
    c = current_app.config
    sq = SquareClient(SquareConfig(
        access_token=c["SQUARE_ACCESS_TOKEN"],
        environment=c["SQUARE_ENVIRONMENT"],
        location_id=c["SQUARE_LOCATION_ID"],
        webhook_signature_key=c["SQUARE_WEBHOOK_SIGNATURE_KEY"],
    ))
    return RefundsService(db.session, sq, InventoryService(db.session))


@bp.get("/")
@admin_required
def list_orders():
    tag = request.args.get("scenario_tag")
    q = select(Order).order_by(Order.placed_at.desc()).limit(200)
    if tag:
        q = q.where(Order.scenario_tag == tag)
    orders = db.session.execute(q).scalars().all()
    return render_template("admin/orders/list.html", orders=orders, scenario_tag=tag)


@bp.get("/<uuid:oid>")
@admin_required
def detail(oid):
    order = db.session.get(Order, oid)
    if order is None:
        abort(404)
    refunds = db.session.execute(
        select(Refund).where(Refund.order_id == order.id)
    ).scalars().all()
    return render_template("admin/orders/detail.html", order=order, refunds=refunds)


@bp.post("/<uuid:oid>/refund")
@admin_required
def issue_refund(oid):
    order = db.session.get(Order, oid)
    if order is None:
        abort(404)
    amount_cents = int(request.form.get("amount_cents", order.total_cents))
    reason = request.form.get("reason", "admin refund")
    try:
        _refunds_svc().issue_refund(order, amount_cents, reason)
        flash("Refund issued.", "ok")
    except Exception as exc:
        flash(f"Refund failed: {exc}", "error")
    return redirect(url_for("admin_orders.detail", oid=oid))
