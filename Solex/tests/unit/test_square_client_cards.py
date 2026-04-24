"""Tests for SquareClient customers + cards-on-file + charge_saved_card (Task 2.1)."""
from unittest.mock import MagicMock
from tenacity import RetryError
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


def _mock_square_client(mocker, customers_return=None, customers_side_effect=None,
                         cards_return=None, cards_side_effect=None,
                         payments_return=None, payments_side_effect=None):
    """Patch _get_square_class so SquareClient() uses a mock SDK instance."""
    import solex.services.square_client as _mod

    mock_sq = MagicMock()

    if customers_return is not None:
        mock_sq.customers.create.return_value = customers_return
    if customers_side_effect is not None:
        mock_sq.customers.create.side_effect = customers_side_effect

    if cards_return is not None:
        mock_sq.cards.create.return_value = cards_return
    if cards_side_effect is not None:
        mock_sq.cards.create.side_effect = cards_side_effect

    if payments_return is not None:
        mock_sq.payments.create.return_value = payments_return
    if payments_side_effect is not None:
        mock_sq.payments.create.side_effect = payments_side_effect

    mock_class = MagicMock(return_value=mock_sq)
    mocker.patch.object(_mod, "_get_square_class", return_value=mock_class)
    _mod._Square = None
    return mock_sq


def _customer_response(customer_id="cust_abc"):
    resp = MagicMock()
    customer = MagicMock()
    customer.model_dump.return_value = {"id": customer_id, "email_address": "a@b.c"}
    resp.customer = customer
    return resp


def _card_response(card_id="ccof:token123"):
    resp = MagicMock()
    card = MagicMock()
    card.model_dump.return_value = {"id": card_id, "customer_id": "cust_1"}
    resp.card = card
    return resp


def _payment_response(payment_id="sqp_789"):
    resp = MagicMock()
    payment = MagicMock()
    payment.model_dump.return_value = {"id": payment_id, "status": "COMPLETED"}
    resp.payment = payment
    return resp


def _api_error(status_code=400, category="API_ERROR", code="UNKNOWN"):
    from square.core.api_error import ApiError
    return ApiError(status_code=status_code, body={"errors": [{"category": category, "code": code}]})


# --- create_customer ---

def test_create_customer_returns_dict(cfg, mocker):
    _mock_square_client(mocker, customers_return=_customer_response("cust_abc"))
    sc = SquareClient(cfg)
    result = sc.create_customer("a@b.c", "Alice Smith")
    assert isinstance(result, dict)
    assert result["id"] == "cust_abc"


def test_create_customer_no_name(cfg, mocker):
    _mock_square_client(mocker, customers_return=_customer_response("cust_xyz"))
    sc = SquareClient(cfg)
    result = sc.create_customer("no@name.com")
    assert result.get("id") == "cust_xyz"


def test_create_customer_passes_email(cfg, mocker):
    mock_sq = _mock_square_client(mocker, customers_return=_customer_response())
    sc = SquareClient(cfg)
    sc.create_customer("test@ex.com", "Bob")
    call_kwargs = mock_sq.customers.create.call_args.kwargs
    assert call_kwargs["email_address"] == "test@ex.com"
    assert call_kwargs["given_name"] == "Bob"


def test_create_customer_error_raises_square_error(cfg, mocker):
    err = _api_error(status_code=400, category="INVALID_REQUEST_ERROR", code="BAD_REQUEST")
    _mock_square_client(mocker, customers_side_effect=err)
    sc = SquareClient(cfg)
    with pytest.raises(SquareError):
        sc.create_customer("bad@ex.com")


# --- save_card_on_file ---

def test_save_card_returns_card_id(cfg, mocker):
    _mock_square_client(mocker, cards_return=_card_response("ccof:abc123"))
    sc = SquareClient(cfg)
    card = sc.save_card_on_file("cust_1", "cnon:card-nonce-ok")
    assert card["id"] == "ccof:abc123"


def test_save_card_passes_source_and_customer(cfg, mocker):
    mock_sq = _mock_square_client(mocker, cards_return=_card_response())
    sc = SquareClient(cfg)
    sc.save_card_on_file("cust_99", "cnon:nonce")
    call_kwargs = mock_sq.cards.create.call_args.kwargs
    assert call_kwargs["source_id"] == "cnon:nonce"
    assert call_kwargs["card"]["customer_id"] == "cust_99"


def test_save_card_error_raises_square_error(cfg, mocker):
    err = _api_error(status_code=400, category="INVALID_REQUEST_ERROR", code="INVALID_CARD")
    _mock_square_client(mocker, cards_side_effect=err)
    sc = SquareClient(cfg)
    with pytest.raises(SquareError):
        sc.save_card_on_file("cust_1", "cnon:bad")


# --- charge_saved_card ---

def test_charge_saved_card_success(cfg, mocker):
    _mock_square_client(mocker, payments_return=_payment_response("sqp_789"))
    sc = SquareClient(cfg)
    result = sc.charge_saved_card("ccof:token", 2000, "cust_1")
    assert result["id"] == "sqp_789"


def test_charge_saved_card_passes_correct_args(cfg, mocker):
    mock_sq = _mock_square_client(mocker, payments_return=_payment_response())
    sc = SquareClient(cfg)
    sc.charge_saved_card("ccof:abc", 5000, "cust_42", reference_id="ref:001")
    call_kwargs = mock_sq.payments.create.call_args.kwargs
    assert call_kwargs["source_id"] == "ccof:abc"
    assert call_kwargs["amount_money"] == {"amount": 5000, "currency": "USD"}
    assert call_kwargs["customer_id"] == "cust_42"
    assert call_kwargs["idempotency_key"] == "ref:001"


def test_charge_saved_card_declined_raises(cfg, mocker):
    err = _api_error(status_code=402, category="PAYMENT_METHOD_ERROR", code="CARD_DECLINED")
    _mock_square_client(mocker, payments_side_effect=err)
    sc = SquareClient(cfg)
    with pytest.raises(SquareDeclined):
        sc.charge_saved_card("ccof:expired", 1000, "cust_1")


def test_charge_saved_card_transient_retries(cfg, mocker):
    err = _api_error(status_code=500, category="API_ERROR", code="INTERNAL_SERVER_ERROR")
    _mock_square_client(mocker, payments_side_effect=err)
    sc = SquareClient(cfg)
    with pytest.raises((SquareTransient, RetryError)):
        sc.charge_saved_card("ccof:token", 1000, "cust_1")
