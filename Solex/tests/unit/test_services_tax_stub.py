from solex.services.tax import FlatRateTaxStub

def test_zero_tax_when_rate_zero():
    stub = FlatRateTaxStub(rate_pct=0.0)
    assert stub.compute(10000, 695, "CA").tax_cents == 0

def test_computes_on_subtotal_plus_shipping():
    stub = FlatRateTaxStub(rate_pct=8.0)
    assert stub.compute(10000, 695, "CA").tax_cents == round(10695 * 0.08)
