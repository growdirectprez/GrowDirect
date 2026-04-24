from solex.services.shipping import FlatRateShippingStub

def test_flat_rate_under_threshold():
    s = FlatRateShippingStub(flat_cents=695, free_threshold_cents=9900)
    assert s.quote(5000, "CA").shipping_cents == 695

def test_free_over_threshold():
    s = FlatRateShippingStub(flat_cents=695, free_threshold_cents=9900)
    assert s.quote(15000, "CA").shipping_cents == 0
