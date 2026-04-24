from solex.models.refund import Refund


def test_refund_fields():
    r = Refund(amount_cents=1000, reason="customer_request")
    assert r.amount_cents == 1000
    assert r.reason == "customer_request"
    assert r.order_id is None
    assert r.square_refund_id is None
