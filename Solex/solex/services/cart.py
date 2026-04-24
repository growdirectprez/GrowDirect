import json
from dataclasses import dataclass
from typing import Protocol
from uuid import UUID
from redis import Redis

@dataclass
class CartSnapshot:
    currency: str
    lines: list[dict]
    subtotal_cents: int

class CartBackend(Protocol):
    def load(self, key: str) -> CartSnapshot: ...
    def save(self, key: str, snapshot: CartSnapshot) -> None: ...

class ValkeyCartBackend:
    def __init__(self, redis: Redis, prefix: str = "solex:cart:"):
        self.redis = redis; self.prefix = prefix
    def _k(self, key): return f"{self.prefix}{key}"
    def load(self, key):
        raw = self.redis.get(self._k(key))
        if not raw:
            return CartSnapshot(currency="USD", lines=[], subtotal_cents=0)
        data = json.loads(raw)
        return CartSnapshot(**data)
    def save(self, key, snap):
        self.redis.setex(self._k(key), 7 * 24 * 3600, json.dumps(snap.__dict__))

class CartService:
    def __init__(self, backend: CartBackend, catalog_get_product):
        self.backend = backend
        self.get_product = catalog_get_product

    def add(self, key, product_id: UUID, qty: int) -> CartSnapshot:
        snap = self.backend.load(key)
        product = self.get_product(product_id)
        if product is None:
            raise ValueError("unknown product")
        for line in snap.lines:
            if line["product_id"] == str(product_id):
                line["qty"] += qty
                break
        else:
            snap.lines.append(dict(
                product_id=str(product_id), sku=product.sku, name=product.name,
                image_path=product.image_path, qty=qty,
                price_cents=product.price_cents,
            ))
        self._retotal(snap)
        self.backend.save(key, snap)
        return snap

    def update_qty(self, key, product_id, qty):
        snap = self.backend.load(key)
        snap.lines = [l for l in snap.lines
                      if not (l["product_id"] == str(product_id) and qty == 0)]
        for line in snap.lines:
            if line["product_id"] == str(product_id):
                line["qty"] = qty
        self._retotal(snap)
        self.backend.save(key, snap)
        return snap

    def remove(self, key, product_id):
        return self.update_qty(key, product_id, 0)

    def _retotal(self, snap):
        snap.subtotal_cents = sum(l["qty"] * l["price_cents"] for l in snap.lines)
