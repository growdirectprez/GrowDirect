from solex.models.returns import ReturnRequest

def test_return_request_fields():
    r = ReturnRequest(reason="didn't fit", status="pending")
    assert r.status == "pending"
