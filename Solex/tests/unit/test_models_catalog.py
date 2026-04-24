from solex.models.catalog import Category, Product, ProductTag


def test_category_fields():
    c = Category(name="Supplements", slug="supplements", sort=1)
    assert c.name == "Supplements"


def test_product_fields():
    p = Product(
        sku="AO-YOUTH-30",
        slug="ao-youth-30",
        name="AO Youth 30ct",
        description="...",
        price_cents=4995,
        image_path="catalog/images/ao-youth-30.jpg",
        active=True,
        weight_grams=120,
    )
    assert p.sku == "AO-YOUTH-30"
    assert p.price_cents == 4995


def test_product_tag_links_to_product():
    t = ProductTag(tag="wellness")
    assert t.tag == "wellness"
