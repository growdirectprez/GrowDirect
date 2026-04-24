import pytest
from unittest.mock import patch, MagicMock
from solex.services.cart import CartSnapshot, ValkeyCartBackend


class _MemoryBackend:
    """In-memory cart backend for route-level tests (no Valkey needed)."""
    def __init__(self):
        self._store = {}

    def load(self, key) -> CartSnapshot:
        return self._store.get(key, CartSnapshot(currency="USD", lines=[], subtotal_cents=0))

    def save(self, key, snap: CartSnapshot) -> None:
        self._store[key] = snap


@pytest.fixture()
def cart_backend():
    """Patch ValkeyCartBackend with in-memory implementation for tests."""
    backend = _MemoryBackend()
    with patch("solex.routes.cart.ValkeyCartBackend") as mock_cls, \
         patch("solex.routes.cart.Redis") as mock_redis:
        mock_cls.return_value = backend
        mock_redis.from_url.return_value = MagicMock()
        yield backend


def test_add_to_cart_returns_updated_snapshot(client, seed_catalog, cart_backend):
    product = seed_catalog.products[0]
    resp = client.post("/cart/add", data={"product_id": str(product.id), "qty": 2})
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["lines"][0]["qty"] == 2
    assert body["subtotal_cents"] == 2 * product.price_cents


def test_cart_json_empty_by_default(client, cart_backend):
    resp = client.get("/cart.json")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["lines"] == []
    assert body["subtotal_cents"] == 0
