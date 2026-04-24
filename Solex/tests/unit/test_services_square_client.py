"""Tests for the SquareClient wrapper (Task 6.1).

All Square API calls are mocked. The v44 SDK raises ApiError on non-2xx;
there is no is_success()/result.body pattern.
"""
from unittest.mock import MagicMock, patch
import pytest
from solex.services.square_client import (
    SquareClient,
    SquareConfig,
    SquareDeclined,
    SquareTransient,
    SquareError,
)


@pytest.fixture
def cfg():
    return SquareConfig(
        access_token="sb-test",
        environment="sandbox",
        location_id="L123",
        webhook_signature_key="whk",
    )


def _mock_square_client(mocker, orders_side_effect=None, payments_side_effect=None,
                         refunds_side_effect=None, orders_return=None,
                         payments_return=None, refunds_return=None):
    """Patch _get_square_class so SquareClient() uses a mock SDK instance."""
    import solex.services.square_client as _mod

    mock_sq = MagicMock()

    if orders_return is not None:
        mock_sq.orders.create.return_value = orders_return
    if orders_side_effect is not None:
        mock_sq.orders.create.side_effect = orders_side_effect

    if payments_return is not None:
        mock_sq.payments.create.return_value = payments_return
    if payments_side_effect is not None:
        mock_sq.payments.create.side_effect = payments_side_effect

    if refunds_return is not None:
        mock_sq.refunds.refund_payment.return_value = refunds_return
    if refunds_side_effect is not None:
        mock_sq.refunds.refund_payment.side_effect = refunds_side_effect

    mock_class = MagicMock(return_value=mock_sq)
    mocker.patch.object(_mod, "_get_square_class", return_value=mock_class)
    # Also reset the cached _Square so each test is clean
    _mod._Square = None
    return mock_sq


# --- Helpers to build mock responses ---

def _order_response(order_id="ord_123"):
    resp = MagicMock()
    order = MagicMock()
    order.model_dump.return_value = {"id": order_id, "location_id": "L123"}
    resp.order = order
    return resp


def _payment_response(payment_id="pay_456"):
    resp = MagicMock()
    payment = MagicMock()
    payment.model_dump.return_value = {"id": payment_id, "status": "COMPLETED"}
    resp.payment = payment
    return resp


def _refund_response(refund_id="ref_789"):
    resp = MagicMock()
    refund = MagicMock()
    refund.model_dump.return_value = {"id": refund_id, "status": "COMPLETED"}
    resp.refund = refund
    return resp


def _api_error(status_code=400, category="API_ERROR", code="UNKNOWN"):
    from square.core.api_error import ApiError

    err = ApiError(status_code=status_code, body={"errors": [{"category": category, "code": code}]})
    return err


# --- Tests ---

def test_create_order_success(cfg, mocker):
    _mock_square_client(mocker, orders_return=_order_response("ord_123"))
    sc = SquareClient(cfg)
    result = sc.create_order(
        line_items=[
            {"name": "Widget", "quantity": "1", "base_price_money": {"amount": 100, "currency": "USD"}}
        ]
    )
    assert result["id"] == "ord_123"


def test_create_order_passes_location_and_line_items(cfg, mocker):
    mock_sq = _mock_square_client(mocker, orders_return=_order_response())
    sc = SquareClient(cfg)
    sc.create_order(line_items=[{"name": "X", "quantity": "1"}])
    call_kwargs = mock_sq.orders.create.call_args.kwargs
    assert call_kwargs["order"]["location_id"] == "L123"
    assert call_kwargs["order"]["line_items"] == [{"name": "X", "quantity": "1"}]


def test_create_order_with_taxes_and_shipping(cfg, mocker):
    mock_sq = _mock_square_client(mocker, orders_return=_order_response())
    sc = SquareClient(cfg)
    sc.create_order(
        line_items=[{"name": "X", "quantity": "1"}],
        taxes_cents=100,
        shipping_cents=500,
    )
    call_kwargs = mock_sq.orders.create.call_args.kwargs
    assert call_kwargs["order"]["taxes"]
    assert call_kwargs["order"]["service_charges"]


def test_create_payment_success(cfg, mocker):
    _mock_square_client(mocker, payments_return=_payment_response("pay_456"))
    sc = SquareClient(cfg)
    result = sc.create_payment("cnon:test", 1500, "ord_123")
    assert result["id"] == "pay_456"


def test_create_payment_declined_raises(cfg, mocker):
    err = _api_error(status_code=402, category="PAYMENT_METHOD_ERROR", code="CARD_DECLINED")
    _mock_square_client(mocker, payments_side_effect=err)
    sc = SquareClient(cfg)
    with pytest.raises(SquareDeclined):
        sc.create_payment("cnon:bad", 500, "ord_1")


def test_create_payment_500_raises_transient(cfg, mocker):
    from tenacity import RetryError
    err = _api_error(status_code=500, category="API_ERROR", code="INTERNAL_SERVER_ERROR")
    _mock_square_client(mocker, payments_side_effect=err)
    sc = SquareClient(cfg)
    # tenacity retries 3 times then wraps in RetryError (cause is SquareTransient)
    with pytest.raises((SquareTransient, RetryError)):
        sc.create_payment("cnon:test", 500, "ord_1")


def test_create_refund_success(cfg, mocker):
    _mock_square_client(mocker, refunds_return=_refund_response("ref_789"))
    sc = SquareClient(cfg)
    result = sc.create_refund("pay_456", 500, reason="damaged")
    assert result["id"] == "ref_789"


def test_create_refund_passes_payment_id(cfg, mocker):
    mock_sq = _mock_square_client(mocker, refunds_return=_refund_response())
    sc = SquareClient(cfg)
    sc.create_refund("pay_999", 200)
    call_kwargs = mock_sq.refunds.refund_payment.call_args.kwargs
    assert call_kwargs["payment_id"] == "pay_999"
    assert call_kwargs["amount_money"] == {"amount": 200, "currency": "USD"}


def test_webhook_signature_verify_roundtrip(cfg):
    import base64, hashlib, hmac as _hmac
    sc = SquareClient.__new__(SquareClient)  # skip SDK init
    sc.cfg = cfg
    body = b'{"type":"test"}'
    url = "https://example.com/hook"
    sig = base64.b64encode(
        _hmac.new(b"whk", (url + body.decode()).encode(), hashlib.sha256).digest()
    ).decode()
    assert sc.verify_webhook_signature(url, body, sig) is True
    assert sc.verify_webhook_signature(url, body, "bogus") is False
    assert sc.verify_webhook_signature(url, body, "") is False
