import uuid
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from sqlalchemy import select
from solex.extensions import db
from solex.models import Product, Category, Inventory
from solex.routes.admin_utils import admin_required

bp = Blueprint("admin_catalog", __name__, url_prefix="/admin/catalog")


@bp.get("/")
@admin_required
def list_products():
    products = db.session.execute(
        select(Product).order_by(Product.name)
    ).scalars().all()
    return render_template("admin/catalog/list.html", products=products)


@bp.get("/new")
@admin_required
def new_product():
    categories = db.session.execute(
        select(Category).order_by(Category.sort, Category.name)
    ).scalars().all()
    return render_template("admin/catalog/form.html", product=None, categories=categories)


@bp.post("/new")
@admin_required
def create_product():
    f = request.form
    slug = f["slug"].strip()
    existing = db.session.execute(select(Product).where(Product.slug == slug)).scalar_one_or_none()
    if existing:
        flash("Slug already in use.", "error")
        categories = db.session.execute(select(Category).order_by(Category.sort, Category.name)).scalars().all()
        return render_template("admin/catalog/form.html", product=None, categories=categories), 422

    cat_id = f.get("category_id") or None
    if cat_id:
        cat_id = uuid.UUID(cat_id)

    product = Product(
        sku=f["sku"].strip(),
        slug=slug,
        name=f["name"].strip(),
        description=f.get("description", ""),
        short_description=f.get("short_description", ""),
        price_cents=int(f["price_cents"]),
        compare_at_cents=int(f["compare_at_cents"]) if f.get("compare_at_cents") else None,
        image_path=f.get("image_path", ""),
        category_id=cat_id,
        active="active" in f,
        weight_grams=int(f.get("weight_grams", 0)),
    )
    db.session.add(product)
    db.session.flush()

    starting_inventory = int(f.get("starting_inventory", 0))
    if starting_inventory:
        db.session.add(Inventory(product_id=product.id, on_hand=starting_inventory))

    db.session.commit()
    flash("Product created.", "ok")
    return redirect(url_for("admin_catalog.list_products"))


@bp.get("/<uuid:pid>/edit")
@admin_required
def edit_product(pid):
    product = db.session.get(Product, pid)
    if product is None:
        abort(404)
    categories = db.session.execute(
        select(Category).order_by(Category.sort, Category.name)
    ).scalars().all()
    return render_template("admin/catalog/form.html", product=product, categories=categories)


@bp.post("/<uuid:pid>/edit")
@admin_required
def update_product(pid):
    product = db.session.get(Product, pid)
    if product is None:
        abort(404)
    f = request.form
    cat_id = f.get("category_id") or None
    if cat_id:
        cat_id = uuid.UUID(cat_id)
    product.sku = f["sku"].strip()
    product.slug = f["slug"].strip()
    product.name = f["name"].strip()
    product.description = f.get("description", "")
    product.short_description = f.get("short_description", "")
    product.price_cents = int(f["price_cents"])
    product.compare_at_cents = int(f["compare_at_cents"]) if f.get("compare_at_cents") else None
    product.image_path = f.get("image_path", "")
    product.category_id = cat_id
    product.active = "active" in f
    product.weight_grams = int(f.get("weight_grams", 0))
    db.session.commit()
    flash("Product updated.", "ok")
    return redirect(url_for("admin_catalog.list_products"))


@bp.post("/<uuid:pid>/delete")
@admin_required
def delete_product(pid):
    product = db.session.get(Product, pid)
    if product is None:
        abort(404)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted.", "ok")
    return redirect(url_for("admin_catalog.list_products"))
