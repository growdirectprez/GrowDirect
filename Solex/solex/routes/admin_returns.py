from flask import Blueprint, render_template, redirect, url_for, flash, abort, request, current_app
from sqlalchemy import select
from solex.extensions import db
from solex.models import ReturnRequest
from solex.services.returns import ReturnsService
from solex.services.refunds import RefundsService
from solex.services.square_client import SquareClient, SquareConfig
from solex.services.inventory import InventoryService
from solex.routes.admin_utils import admin_required, _load_admin_from_session

bp = Blueprint("admin_returns", __name__, url_prefix="/admin/returns")


def _svc():
    c = current_app.config
    sq = SquareClient(SquareConfig(
        access_token=c["SQUARE_ACCESS_TOKEN"],
        environment=c["SQUARE_ENVIRONMENT"],
        location_id=c["SQUARE_LOCATION_ID"],
        webhook_signature_key=c["SQUARE_WEBHOOK_SIGNATURE_KEY"],
    ))
    return ReturnsService(
        db.session,
        RefundsService(db.session, sq, InventoryService(db.session)),
    )


@bp.get("/")
@admin_required
def list_returns():
    reqs = db.session.execute(
        select(ReturnRequest).order_by(ReturnRequest.created_at.desc())
    ).scalars().all()
    return render_template("admin/returns/list.html", reqs=reqs)


@bp.get("/<uuid:rid>")
@admin_required
def detail(rid):
    req = db.session.get(ReturnRequest, rid)
    if req is None:
        abort(404)
    return render_template("admin/returns/detail.html", req=req)


@bp.post("/<uuid:rid>/approve")
@admin_required
def approve(rid):
    req = db.session.get(ReturnRequest, rid)
    if req is None:
        abort(404)
    admin = _load_admin_from_session()
    try:
        _svc().approve(req, admin)
        flash("Approved + refunded.", "ok")
    except Exception as exc:
        flash(f"Approval failed: {exc}", "error")
    return redirect(url_for("admin_returns.detail", rid=rid))


@bp.post("/<uuid:rid>/deny")
@admin_required
def deny(rid):
    req = db.session.get(ReturnRequest, rid)
    if req is None:
        abort(404)
    admin = _load_admin_from_session()
    reason = request.form.get("reason", "")
    try:
        _svc().deny(req, admin, reason)
        flash("Denied.", "ok")
    except Exception as exc:
        flash(f"Deny failed: {exc}", "error")
    return redirect(url_for("admin_returns.detail", rid=rid))
