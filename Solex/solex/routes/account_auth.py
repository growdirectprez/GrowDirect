from flask import Blueprint, render_template, request, redirect, url_for, abort, current_app
from flask_login import login_user, logout_user, login_required
from sqlalchemy import select

from solex.extensions import db, limiter
from solex.services.auth import AuthService
from solex.services.email import EmailService
from solex.models import Customer

bp = Blueprint("account_auth", __name__, url_prefix="/account")


@bp.get("/login")
def login():
    return render_template("auth/admin_login.html", audience="customer")


@bp.post("/login/magic")
@limiter.limit("5 per minute")
def request_magic():
    email = request.form["email"]
    user = db.session.execute(
        select(Customer).where(Customer.email == email)
    ).scalar_one_or_none()
    if user is not None:
        token = AuthService(db.session).issue_magic_link("customer", user.id)
        db.session.commit()
        link = url_for("account_auth.consume_magic", token=token, _external=True)
        try:
            EmailService().send("magic_link", to=email, link=link, audience="customer")
        except Exception:
            current_app.logger.exception("magic link send failed")
    return render_template("auth/magic_link_sent.html")


@bp.get("/login/magic/<token>")
def consume_magic(token):
    user = AuthService(db.session).consume_magic_link("customer", token)
    if user is None:
        abort(401)
    login_user(user)
    db.session.commit()
    return redirect(url_for("storefront.home"))


@bp.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("account_auth.login"))
