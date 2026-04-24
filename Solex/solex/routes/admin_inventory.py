from flask import Blueprint, render_template, redirect, url_for, flash, request
from sqlalchemy import select
from solex.extensions import db
from solex.models import Product, Inventory
from solex.services.inventory import InventoryService
from solex.routes.admin_utils import admin_required, _load_admin_from_session

bp = Blueprint("admin_inventory", __name__, url_prefix="/admin/inventory")


@bp.get("/")
@admin_required
def list_inventory():
    rows = db.session.execute(
        select(Product, Inventory)
        .outerjoin(Inventory, Inventory.product_id == Product.id)
        .order_by(Product.name)
    ).all()
    return render_template("admin/inventory/list.html", rows=rows)


@bp.post("/<uuid:pid>/adjust")
@admin_required
def adjust(pid):
    admin = _load_admin_from_session()
    delta = int(request.form["delta"])
    reason = request.form["reason"]
    note = request.form.get("note") or None
    svc = InventoryService(db.session)
    svc.adjust(
        pid, delta, reason,
        admin_user_id=admin.id if admin else None,
        note=note,
    )
    db.session.commit()
    flash(f"Adjusted by {delta:+d} ({reason}).", "ok")
    return redirect(url_for("admin_inventory.list_inventory"))
