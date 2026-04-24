from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import select
from solex.extensions import db
from solex.models import Order, Subscription, Address

bp = Blueprint("account", __name__, url_prefix="/account")


@bp.get("/")
@login_required
def dashboard():
    recent_orders = db.session.execute(
        select(Order).where(Order.customer_id == current_user.id)
                     .order_by(Order.placed_at.desc()).limit(5)
    ).scalars().all()
    active_subs = db.session.execute(
        select(Subscription).where(
            Subscription.customer_id == current_user.id,
            Subscription.status == "active",
        )
    ).scalars().all()
    addresses = db.session.execute(
        select(Address).where(Address.customer_id == current_user.id)
    ).scalars().all()
    return render_template("account/dashboard.html",
                           orders=recent_orders, subs=active_subs, addresses=addresses)
