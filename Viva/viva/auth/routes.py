"""VIVA auth routes — Jeffe-only access."""

from flask import Blueprint

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login")
def login():
    """Login placeholder — VIVA is internal, Jeffe-only."""
    # Defer to platform auth pattern when ready
    return "VIVA auth — not yet implemented", 501
