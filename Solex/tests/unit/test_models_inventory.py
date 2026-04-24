from solex.models.inventory import Inventory, InventoryAdjustment


def test_inventory_fields():
    i = Inventory(on_hand=50, reorder_at=10)
    assert i.on_hand == 50
    assert i.reorder_at == 10


def test_inventory_adjustment_fields():
    a = InventoryAdjustment(delta=-3, reason="sold")
    assert a.delta == -3
    assert a.reason == "sold"
