"""Admin route protection using the admin_login manager."""
from functools import wraps
from flask import redirect, url_for, request, session
from solex.extensions import admin_login, db
from solex.models import AdminUser
from sqlalchemy import select


def _load_admin_from_session():
    """Load AdminUser from the current session (using _user_id)."""
    user_id = session.get("_user_id")
    if not user_id:
        return None
    try:
        return db.session.execute(
            select(AdminUser).where(AdminUser.id == user_id, AdminUser.active == True)
        ).scalar_one_or_none()
    except Exception:
        return None


def admin_required(f):
    """Require an authenticated AdminUser.

    Uses the session's _user_id to look up an AdminUser directly,
    bypassing the customer_login manager that wins app.login_manager
    when two LoginManagers are registered.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        admin = _load_admin_from_session()
        if admin is None:
            return redirect(url_for("admin_auth.login", next=request.url))
        return f(*args, **kwargs)
    return decorated
