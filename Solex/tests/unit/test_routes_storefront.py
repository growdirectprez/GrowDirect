import pytest


def test_shop_lists_products(client, seed_catalog):
    resp = client.get("/shop")
    assert resp.status_code == 200
    assert b"AO Youth" in resp.data


def test_product_detail_by_slug(client, seed_catalog):
    resp = client.get("/products/ao-youth-30")
    assert resp.status_code == 200
    assert b"AO Youth" in resp.data


def test_product_detail_404_for_missing(client, seed_catalog):
    assert client.get("/products/nope").status_code == 404


def test_home_renders(client, seed_catalog):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Solex" in resp.data
