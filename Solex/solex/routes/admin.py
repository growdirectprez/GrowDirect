from flask import Blueprint, render_template
from solex.routes.admin_utils import admin_required

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.get("/")
@admin_required
def dashboard():
    return render_template("admin/dashboard.html")
