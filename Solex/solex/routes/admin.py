from flask import Blueprint, render_template
from sqlalchemy import select, func

from solex.extensions import db
from solex.models import Order, Product, Subscription, ReturnRequest
from solex.routes.admin_utils import admin_required

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.get("/")
@admin_required
def dashboard():
    counts = {
        "orders_total": db.session.scalar(select(func.count()).select_from(Order)) or 0,
        "orders_pending": db.session.scalar(
            select(func.count()).select_from(Order).where(Order.status == "pending")
        ) or 0,
        "products_active": db.session.scalar(
            select(func.count()).select_from(Product).where(Product.active == True)
        ) or 0,
        "subs_active": db.session.scalar(
            select(func.count()).select_from(Subscription).where(Subscription.status == "active")
        ) or 0,
        "returns_pending": db.session.scalar(
            select(func.count()).select_from(ReturnRequest).where(ReturnRequest.status == "pending")
        ) or 0,
    }
    return render_template("admin/dashboard.html", counts=counts)
