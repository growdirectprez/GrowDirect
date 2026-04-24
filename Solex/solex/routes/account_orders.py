from flask import Blueprint, render_template, abort, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from sqlalchemy import select
from solex.extensions import db
from solex.models import Order, ReturnRequest

bp = Blueprint("account_orders", __name__, url_prefix="/account/orders")


@bp.get("/")
@login_required
def list_orders():
    orders = db.session.execute(
        select(Order).where(Order.customer_id == current_user.id)
                     .order_by(Order.placed_at.desc())
    ).scalars().all()
    return render_template("account/orders/list.html", orders=orders)


@bp.get("/<uuid:oid>")
@login_required
def detail(oid):
    order = db.session.get(Order, oid)
    if order is None or order.customer_id != current_user.id:
        abort(404)
    existing_return = db.session.execute(
        select(ReturnRequest).where(ReturnRequest.order_id == order.id)
    ).scalar_one_or_none()
    return render_template("account/orders/detail.html", order=order, return_request=existing_return)


@bp.get("/<uuid:oid>/return")
@login_required
def return_form(oid):
    order = db.session.get(Order, oid)
    if order is None or order.customer_id != current_user.id:
        abort(404)
    return render_template("account/orders/return_form.html", order=order)


@bp.post("/<uuid:oid>/return")
@login_required
def request_return(oid):
    order = db.session.get(Order, oid)
    if order is None or order.customer_id != current_user.id:
        abort(404)
    reason = (request.form.get("reason") or "").strip()
    if not reason:
        flash("Please describe the issue.", "error")
        return redirect(url_for("account_orders.detail", oid=order.id))

    from solex.services.returns import ReturnsService
    from solex.services.refunds import RefundsService
    from solex.services.square_client import SquareClient, SquareConfig
    from solex.services.inventory import InventoryService
    c = current_app.config
    sq = SquareClient(SquareConfig(
        access_token=c["SQUARE_ACCESS_TOKEN"], environment=c["SQUARE_ENVIRONMENT"],
        location_id=c["SQUARE_LOCATION_ID"], webhook_signature_key=c["SQUARE_WEBHOOK_SIGNATURE_KEY"],
    ))
    ReturnsService(
        db.session,
        RefundsService(db.session, sq, InventoryService(db.session)),
    ).request(order, reason)
    flash("Return request submitted.", "ok")
    return redirect(url_for("account_orders.detail", oid=order.id))
