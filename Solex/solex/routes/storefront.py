from flask import Blueprint, render_template, abort
from solex.extensions import db
from solex.services.catalog import CatalogService

bp = Blueprint("storefront", __name__)


def _catalog():
    return CatalogService(db.session)


@bp.get("/")
def home():
    products = _catalog().list_products()[:4]
    return render_template("storefront/home.html", products=products)


@bp.get("/shop")
def shop():
    return render_template("storefront/shop.html",
                           products=_catalog().list_products(),
                           categories=_catalog().list_categories())


@bp.get("/shop/<slug>")
def shop_by_category(slug):
    products = _catalog().list_products(category_slug=slug)
    return render_template("storefront/shop.html",
                           products=products,
                           categories=_catalog().list_categories(),
                           active_slug=slug)


@bp.get("/products/<slug>")
def product_detail(slug):
    product = _catalog().get_product(slug)
    if product is None or not product.active:
        abort(404)
    return render_template("storefront/product_detail.html", product=product)
