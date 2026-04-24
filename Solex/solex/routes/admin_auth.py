from flask import Blueprint, render_template, request, redirect, url_for, abort, current_app
from flask_login import login_user, logout_user, login_required
from sqlalchemy import select

from solex.extensions import db, limiter
from solex.services.auth import AuthService
from solex.services.email import EmailService
from solex.models import AdminUser

bp = Blueprint("admin_auth", __name__, url_prefix="/admin")


@bp.get("/login")
def login():
    return render_template("auth/admin_login.html")


@bp.post("/login")
@limiter.limit("10 per minute")
def login_submit():
    svc = AuthService(db.session)
    user = svc.verify_admin_password(request.form["email"], request.form["password"])
    if user is None:
        return render_template("auth/admin_login.html", error="bad_creds"), 401
    login_user(user)
    db.session.commit()
    return redirect(url_for("storefront.home"))


@bp.post("/login/magic")
@limiter.limit("5 per minute")
def request_magic():
    email = request.form["email"]
    user = db.session.execute(
        select(AdminUser).where(AdminUser.email == email, AdminUser.active == True)
    ).scalar_one_or_none()
    if user is not None:
        token = AuthService(db.session).issue_magic_link("admin", user.id)
        db.session.commit()
        link = url_for("admin_auth.consume_magic", token=token, _external=True)
        try:
            EmailService().send("magic_link", to=email, link=link, audience="admin")
        except Exception:
            current_app.logger.exception("magic link send failed")
    return render_template("auth/magic_link_sent.html")


@bp.get("/login/magic/<token>")
def consume_magic(token):
    user = AuthService(db.session).consume_magic_link("admin", token)
    if user is None:
        abort(401)
    login_user(user)
    db.session.commit()
    return redirect(url_for("storefront.home"))


@bp.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("admin_auth.login"))
