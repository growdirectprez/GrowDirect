from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from sqlalchemy import select
from solex.extensions import db
from solex.models import Address

bp = Blueprint("account_addresses", __name__, url_prefix="/account/addresses")

_FIELDS = ("label", "first_name", "last_name", "line1", "line2", "city",
           "region", "postal_code", "country", "phone")


@bp.get("/")
@login_required
def list_addresses():
    addrs = db.session.execute(
        select(Address).where(Address.customer_id == current_user.id)
    ).scalars().all()
    return render_template("account/addresses.html", addresses=addrs)


@bp.post("/")
@login_required
def create():
    data = {f: request.form.get(f) or None for f in _FIELDS}
    data["customer_id"] = current_user.id
    data["country"] = data.get("country") or "US"
    addr = Address(**{k: v for k, v in data.items() if v is not None or k == "customer_id"})
    if not (addr.first_name and addr.last_name and addr.line1 and addr.city
            and addr.region and addr.postal_code):
        flash("All required fields must be filled.", "error")
        return redirect(url_for("account_addresses.list_addresses"))
    db.session.add(addr)
    db.session.commit()
    flash("Address added.", "ok")
    return redirect(url_for("account_addresses.list_addresses"))


@bp.post("/<uuid:aid>/delete")
@login_required
def delete(aid):
    addr = db.session.get(Address, aid)
    if addr is None or addr.customer_id != current_user.id:
        abort(404)
    db.session.delete(addr)
    db.session.commit()
    flash("Address deleted.", "ok")
    return redirect(url_for("account_addresses.list_addresses"))
