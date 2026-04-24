"""Square Python SDK v44 wrapper with retry and typed exceptions.

SDK shape (squareup==44.0.1.20260122, Fern-generated):
  - Import: `from square import Square` with `SquareEnvironment.SANDBOX` enum
  - Methods raise `ApiError` on non-2xx (no `.is_success()` pattern)
  - Returns typed Pydantic objects: resp.order, resp.payment, resp.refund
  - Method signatures are keyword-only TypedDicts, not body=dict
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import uuid
from dataclasses import dataclass
from typing import Optional

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

# Lazy top-level references so tests can patch them without importing Square at
# import time (which would fail if squareup is absent). The actual object is
# resolved in _get_square_class() / _get_api_error_class().
_Square = None
_ApiError = None


def _get_square_class():
    global _Square
    if _Square is None:
        from square import Square as _S  # type: ignore[import]
        _Square = _S
    return _Square


def _get_api_error_class():
    global _ApiError
    if _ApiError is None:
        from square.core.api_error import ApiError as _E  # type: ignore[import]
        _ApiError = _E
    return _ApiError


@dataclass
class SquareConfig:
    access_token: str
    environment: str  # "sandbox" | "production"
    location_id: str
    webhook_signature_key: str


class SquareError(Exception):
    pass


class SquareTransient(SquareError):
    pass


class SquareDeclined(SquareError):
    pass


def _gen_idem_key() -> str:
    return str(uuid.uuid4())


def _env_enum(environment: str):
    """Map 'sandbox'/'production' string to the SDK's SquareEnvironment enum."""
    from square.environment import SquareEnvironment  # type: ignore[import]

    mapping = {
        "sandbox": SquareEnvironment.SANDBOX,
        "production": SquareEnvironment.PRODUCTION,
    }
    return mapping.get(environment.lower(), SquareEnvironment.SANDBOX)


class SquareClient:
    def __init__(self, cfg: SquareConfig):
        self.cfg = cfg
        Square = _get_square_class()
        self._client = Square(
            token=cfg.access_token,
            environment=_env_enum(cfg.environment),
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, max=4),
        retry=retry_if_exception_type(SquareTransient),
    )
    def create_order(
        self,
        line_items: list[dict],
        taxes_cents: int = 0,
        shipping_cents: int = 0,
        reference_id: Optional[str] = None,
    ) -> dict:
        """Create a Square order and return the order dict."""
        ApiError = _get_api_error_class()

        taxes = []
        if taxes_cents:
            taxes = [
                {
                    "name": "Tax",
                    "type": "ADDITIVE",
                    "applied_money": {"amount": taxes_cents, "currency": "USD"},
                }
            ]

        service_charges = []
        if shipping_cents:
            service_charges = [
                {
                    "name": "Shipping",
                    "calculation_phase": "TOTAL_PHASE",
                    "amount_money": {"amount": shipping_cents, "currency": "USD"},
                }
            ]

        order_params: dict = {"location_id": self.cfg.location_id, "line_items": line_items}
        if taxes:
            order_params["taxes"] = taxes
        if service_charges:
            order_params["service_charges"] = service_charges
        if reference_id:
            order_params["reference_id"] = reference_id

        try:
            resp = self._client.orders.create(
                idempotency_key=reference_id or _gen_idem_key(),
                order=order_params,
            )
        except ApiError as exc:
            self._reraise(exc)

        return resp.order.model_dump()  # type: ignore[union-attr]

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, max=4),
        retry=retry_if_exception_type(SquareTransient),
    )
    def create_payment(
        self,
        source_id: str,
        amount_cents: int,
        order_id: str,
        reference_id: Optional[str] = None,
    ) -> dict:
        """Charge the tokenised card and return the payment dict."""
        ApiError = _get_api_error_class()

        try:
            resp = self._client.payments.create(
                source_id=source_id,
                idempotency_key=reference_id or _gen_idem_key(),
                amount_money={"amount": amount_cents, "currency": "USD"},
                location_id=self.cfg.location_id,
                order_id=order_id,
            )
        except ApiError as exc:
            self._reraise(exc)

        return resp.payment.model_dump()  # type: ignore[union-attr]

    def create_refund(
        self,
        payment_id: str,
        amount_cents: int,
        reason: Optional[str] = None,
    ) -> dict:
        """Issue a refund and return the refund dict."""
        ApiError = _get_api_error_class()

        try:
            resp = self._client.refunds.refund_payment(
                idempotency_key=_gen_idem_key(),
                payment_id=payment_id,
                amount_money={"amount": amount_cents, "currency": "USD"},
                reason=reason or "",
            )
        except ApiError as exc:
            self._reraise(exc)

        return resp.refund.model_dump()  # type: ignore[union-attr]

    def create_customer(self, email: str, name: Optional[str] = None) -> dict:
        """Create a Square customer and return the customer dict."""
        ApiError = _get_api_error_class()

        body: dict = {"email_address": email}
        if name:
            parts = name.split(" ", 1)
            body["given_name"] = parts[0]
            if len(parts) > 1:
                body["family_name"] = parts[1]

        try:
            resp = self._client.customers.create(
                idempotency_key=_gen_idem_key(),
                **body,
            )
        except ApiError as exc:
            self._reraise(exc)

        return resp.customer.model_dump()  # type: ignore[union-attr]

    def save_card_on_file(self, square_customer_id: str, source_id: str) -> dict:
        """Save a card on file for a customer and return the card dict."""
        ApiError = _get_api_error_class()

        try:
            resp = self._client.cards.create(
                idempotency_key=_gen_idem_key(),
                source_id=source_id,
                card={"customer_id": square_customer_id},
            )
        except ApiError as exc:
            self._reraise(exc)

        return resp.card.model_dump()  # type: ignore[union-attr]

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, max=4),
        retry=retry_if_exception_type(SquareTransient),
    )
    def charge_saved_card(
        self,
        square_card_id: str,
        amount_cents: int,
        customer_id: str,
        reference_id: Optional[str] = None,
    ) -> dict:
        """Charge a saved card on file and return the payment dict."""
        ApiError = _get_api_error_class()

        try:
            resp = self._client.payments.create(
                source_id=square_card_id,
                idempotency_key=reference_id or _gen_idem_key(),
                amount_money={"amount": amount_cents, "currency": "USD"},
                location_id=self.cfg.location_id,
                customer_id=customer_id,
            )
        except ApiError as exc:
            self._reraise(exc)

        return resp.payment.model_dump()  # type: ignore[union-attr]

    def upsert_catalog_item(
        self,
        name: str,
        description: str,
        sku: str,
        price_cents: int,
        square_object_id: Optional[str] = None,
    ) -> dict:
        """Create or update a Square Catalog ITEM with a single ITEM_VARIATION.

        Uses batch_upsert with a single-object batch. If square_object_id is
        provided, the existing object is updated; otherwise a new object is
        created using a #-prefixed temp ID.

        Returns a dict with at least an 'id' key for the upserted catalog object.
        """
        ApiError = _get_api_error_class()

        item_id = square_object_id or "#new_item"
        variation_id = f"#{sku}_var" if not square_object_id else f"{square_object_id}_var"

        try:
            resp = self._client.catalog.batch_upsert(
                idempotency_key=_gen_idem_key(),
                batches=[
                    {
                        "objects": [
                            {
                                "type": "ITEM",
                                "id": item_id,
                                "item_data": {
                                    "name": name,
                                    "description": description or "",
                                    "variations": [
                                        {
                                            "type": "ITEM_VARIATION",
                                            "id": variation_id,
                                            "item_variation_data": {
                                                "item_id": item_id,
                                                "name": "Regular",
                                                "sku": sku,
                                                "pricing_type": "FIXED_PRICING",
                                                "price_money": {
                                                    "amount": price_cents,
                                                    "currency": "USD",
                                                },
                                            },
                                        }
                                    ],
                                },
                            }
                        ]
                    }
                ],
            )
        except ApiError as exc:
            self._reraise(exc)

        # The response contains id_mappings for #-prefixed temp IDs.
        # If we used an existing ID, the objects list has the upserted item.
        objects = getattr(resp, "objects", None) or []
        id_mappings = getattr(resp, "id_mappings", None) or []

        # Prefer the real ID from id_mappings (temp ID resolution)
        for mapping in id_mappings:
            client_obj_id = getattr(mapping, "client_object_id", None)
            object_id = getattr(mapping, "object_id", None)
            if client_obj_id == item_id and object_id:
                return {"id": object_id}

        # Fall back to first object in the response
        if objects:
            obj = objects[0]
            obj_id = getattr(obj, "id", None)
            if obj_id:
                return {"id": obj_id}

        return {}

    def verify_webhook_signature(
        self,
        url: str,
        body: bytes,
        header_sig: str,
    ) -> bool:
        """HMAC-SHA256 verification matching Square's webhook signature scheme."""
        expected = base64.b64encode(
            hmac.new(
                self.cfg.webhook_signature_key.encode(),
                (url + body.decode()).encode(),
                hashlib.sha256,
            ).digest()
        ).decode()
        return hmac.compare_digest(expected, header_sig or "")

    def _reraise(self, exc: "ApiError") -> None:  # noqa: F821
        """Map Square ApiError to our typed exceptions and re-raise."""
        status_code = exc.status_code or 500
        errors = exc.errors or []

        if 500 <= status_code < 600:
            raise SquareTransient(errors) from exc

        payment_method_error = any(
            getattr(e, "category", None) == "PAYMENT_METHOD_ERROR" for e in errors
        )
        if status_code == 402 or payment_method_error:
            raise SquareDeclined(errors) from exc

        raise SquareError(errors) from exc
