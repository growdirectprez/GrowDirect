"""CheckoutService — orchestrates Square payment + DB order creation.

Critical invariant: Square API calls happen BEFORE the DB transaction.
If Square fails, nothing persists locally. If DB fails after Square
succeeded, the webhook orphan-recovery path (Task 7.x) handles refunds.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from secrets import token_urlsafe
from typing import Optional

from sqlalchemy.orm import Session

from solex.models import Order, OrderItem
from solex.services.inventory import InventoryService
from solex.services.shipping import ShippingService
from solex.services.square_client import SquareClient, SquareDeclined, SquareError
from solex.services.tax import TaxService


@dataclass
class CartLineIn:
    product_id: str
    qty: int
    price_cents: int
    name: str
    sku: str
    image_path: str = ""


@dataclass
class CustomerIn:
    email: str
    name: str


class CheckoutError(Exception):
    pass


class PaymentDeclined(CheckoutError):
    pass


class CheckoutService:
    def __init__(
        self,
        session: Session,
        square: SquareClient,
        tax: TaxService,
        shipping: ShippingService,
        inventory: InventoryService,
    ):
        self.session = session
        self.square = square
        self.tax = tax
        self.shipping = shipping
        self.inventory = inventory

    def place_order(
        self,
        cart_lines: list[CartLineIn],
        customer: CustomerIn,
        shipping_addr: dict,
        billing_addr: dict,
        payment_token: str,
        *,
        autoship_source: Optional[str] = None,
        scenario_tag: Optional[str] = None,
        placed_at: Optional[datetime] = None,
    ) -> Order:
        if not cart_lines:
            raise CheckoutError("empty cart")

        placed_at = placed_at or datetime.now(timezone.utc)

        subtotal = sum(l.qty * l.price_cents for l in cart_lines)
        ship_quote = self.shipping.quote(subtotal, shipping_addr.get("region", ""))
        tax_calc = self.tax.compute(subtotal, ship_quote.shipping_cents, shipping_addr.get("region", ""))
        total = subtotal + tax_calc.tax_cents + ship_quote.shipping_cents

        square_lines = [
            {
                "name": l.name,
                "quantity": str(l.qty),
                "base_price_money": {"amount": l.price_cents, "currency": "USD"},
            }
            for l in cart_lines
        ]

        # Square calls FIRST — before any DB write
        try:
            sq_order = self.square.create_order(
                line_items=square_lines,
                taxes_cents=tax_calc.tax_cents,
                shipping_cents=ship_quote.shipping_cents,
            )
            sq_payment = self.square.create_payment(
                source_id=payment_token,
                amount_cents=total,
                order_id=sq_order["id"],
            )
        except SquareDeclined as e:
            raise PaymentDeclined(str(e)) from e

        # DB writes only after successful Square charge
        order = Order(
            public_token=token_urlsafe(16),
            customer_email=customer.email,
            customer_name=customer.name,
            shipping_address_json=shipping_addr,
            billing_address_json=billing_addr,
            subtotal_cents=subtotal,
            tax_cents=tax_calc.tax_cents,
            shipping_cents=ship_quote.shipping_cents,
            total_cents=total,
            status="paid",
            square_order_id=sq_order["id"],
            square_payment_id=sq_payment["id"],
            scenario_tag=scenario_tag,
            autoship=bool(autoship_source),
            placed_at=placed_at,
        )
        self.session.add(order)
        self.session.flush()

        for l in cart_lines:
            self.session.add(
                OrderItem(
                    order_id=order.id,
                    product_id=l.product_id,
                    sku_snapshot=l.sku,
                    name_snapshot=l.name,
                    image_path_snapshot=l.image_path,
                    price_snapshot_cents=l.price_cents,
                    qty=l.qty,
                    line_total_cents=l.qty * l.price_cents,
                )
            )
        self.session.flush()

        self.inventory.decrement_for_order(order)
        self.session.commit()

        try:
            from solex.services.email import EmailService  # noqa: PLC0415
            EmailService().send("order_confirmation", order.customer_email, order=order)
        except Exception:
            # Email failure must not crash the checkout response
            pass

        return order
