"""VIVA public routes — health check, status."""

from flask import Blueprint, jsonify

public_bp = Blueprint("public", __name__)


@public_bp.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "app": "viva"})
