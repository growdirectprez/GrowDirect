import uuid
from solex.services.cart import CartService, CartSnapshot

class MemoryBackend:
    def __init__(self): self.store = {}
    def load(self, key):
        return self.store.get(key) or CartSnapshot(currency="USD", lines=[], subtotal_cents=0)
    def save(self, key, snap): self.store[key] = snap

class FakeProduct:
    def __init__(self, pid, sku, name, price):
        self.id = pid; self.sku = sku; self.name = name
        self.image_path = ""; self.price_cents = price

def test_add_new_line():
    pid = uuid.uuid4()
    svc = CartService(MemoryBackend(), lambda p: FakeProduct(pid, "X", "Widget", 500))
    snap = svc.add("session-1", pid, 2)
    assert len(snap.lines) == 1
    assert snap.subtotal_cents == 1000

def test_add_same_product_stacks_qty():
    pid = uuid.uuid4()
    svc = CartService(MemoryBackend(), lambda p: FakeProduct(pid, "X", "Widget", 500))
    svc.add("session-1", pid, 1)
    snap = svc.add("session-1", pid, 2)
    assert len(snap.lines) == 1
    assert snap.lines[0]["qty"] == 3
    assert snap.subtotal_cents == 1500

def test_remove_zeros_line():
    pid = uuid.uuid4()
    svc = CartService(MemoryBackend(), lambda p: FakeProduct(pid, "X", "Widget", 500))
    svc.add("session-1", pid, 2)
    snap = svc.remove("session-1", pid)
    assert snap.lines == []
    assert snap.subtotal_cents == 0

def test_unknown_product_raises():
    svc = CartService(MemoryBackend(), lambda p: None)
    import pytest
    with pytest.raises(ValueError):
        svc.add("s1", uuid.uuid4(), 1)
