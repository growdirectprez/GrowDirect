import pytest

PAGE_SLUGS = ("about", "events", "university", "blog", "resources",
              "privacy", "refunds", "shipping", "terms")


@pytest.mark.parametrize("slug", PAGE_SLUGS)
def test_static_page_renders(client, slug):
    resp = client.get(f"/{slug}")
    assert resp.status_code == 200
    # Title should appear in the rendered HTML
    assert b"placeholder" in resp.data.lower() or b"draft" in resp.data.lower()


def test_unknown_static_page_404(client):
    # The pages blueprint doesn't register arbitrary slugs
    assert client.get("/nonexistent-static-page").status_code == 404
