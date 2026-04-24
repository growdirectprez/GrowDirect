from flask import Blueprint, render_template
from sqlalchemy import select, func
from solex.extensions import db
from solex.models import Customer, Order, Subscription
from solex.routes.admin_utils import admin_required

bp = Blueprint("admin_customers", __name__, url_prefix="/admin/customers")


@bp.get("/")
@admin_required
def list_customers():
    rows = db.session.execute(
        select(
            Customer,
            func.count(Order.id.distinct()).label("order_count"),
            func.count(Subscription.id.distinct()).label("sub_count"),
        )
        .outerjoin(Order, Order.customer_id == Customer.id)
        .outerjoin(
            Subscription,
            (Subscription.customer_id == Customer.id) & (Subscription.status == "active"),
        )
        .group_by(Customer.id)
        .order_by(Customer.email)
    ).all()
    return render_template("admin/customers/list.html", rows=rows)
