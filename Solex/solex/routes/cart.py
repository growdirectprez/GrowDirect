from flask import Blueprint, request, jsonify, session, render_template, current_app
from uuid import UUID
import secrets
from redis import Redis
from solex.extensions import db, csrf
from solex.services.cart import CartService, ValkeyCartBackend
from solex.services.catalog import CatalogService

bp = Blueprint("cart", __name__)


def _session_key() -> str:
    key = session.get("cart_key")
    if not key:
        key = secrets.token_urlsafe(16)
        session["cart_key"] = key
    return key


def _service() -> CartService:
    redis = Redis.from_url(current_app.config["VALKEY_URL"])
    backend = ValkeyCartBackend(redis)
    catalog = CatalogService(db.session)
    return CartService(backend, catalog.get_product_by_id)


@bp.get("/cart")
def view():
    snap = _service().backend.load(_session_key())
    return render_template("cart/cart.html", cart=snap)


@bp.get("/cart.json")
def as_json():
    snap = _service().backend.load(_session_key())
    return jsonify(snap.__dict__)


@bp.post("/cart/add")
def add():
    product_id = UUID(request.form["product_id"])
    qty = max(1, int(request.form.get("qty", 1)))
    snap = _service().add(_session_key(), product_id, qty)
    return jsonify(snap.__dict__), 200


@bp.post("/cart/update")
def update():
    product_id = UUID(request.form["product_id"])
    qty = max(0, int(request.form["qty"]))
    snap = _service().update_qty(_session_key(), product_id, qty)
    return jsonify(snap.__dict__), 200


@bp.post("/cart/remove")
def remove():
    product_id = UUID(request.form["product_id"])
    snap = _service().remove(_session_key(), product_id)
    return jsonify(snap.__dict__), 200
