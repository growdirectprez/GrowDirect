# solex/services/subscriptions.py
from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from solex.models import (
    Subscription, SubscriptionCharge, Customer, Product, Order, OrderItem,
)
from solex.services.square_client import SquareClient, SquareDeclined, SquareError
from solex.services.checkout import CheckoutService
from solex.services.email import EmailService

class SubscriptionError(Exception): ...

class SubscriptionService:
    def __init__(self, session: Session, square: SquareClient,
                 checkout: CheckoutService, email: Optional[EmailService] = None):
        self.session = session
        self.square = square
        self.checkout = checkout
        self.email = email or EmailService()

    def create(self, *, customer: Customer, product: Product, qty: int,
               cadence_days: int, starting_at: datetime,
               square_card_id: str) -> Subscription:
        sub = Subscription(
            customer_id=customer.id, product_id=product.id, qty=qty,
            cadence_days=cadence_days, square_card_id=square_card_id,
            next_charge_at=starting_at, status="active",
        )
        self.session.add(sub); self.session.commit()
        return sub

    def pause(self, sub: Subscription, *, until: Optional[datetime] = None) -> Subscription:
        sub.status = "paused"
        sub.paused_until = until
        self.session.commit()
        return sub

    def resume(self, sub: Subscription) -> Subscription:
        sub.status = "active"
        sub.paused_until = None
        now = datetime.now(timezone.utc)
        if sub.next_charge_at < now:
            sub.next_charge_at = now + timedelta(days=1)
        self.session.commit()
        return sub

    def cancel(self, sub: Subscription) -> Subscription:
        sub.status = "cancelled"
        sub.cancelled_at = datetime.now(timezone.utc)
        self.session.commit()
        return sub

    def charge_due_subscriptions(self, *, now: Optional[datetime] = None) -> dict:
        now = now or datetime.now(timezone.utc)
        due = self.session.execute(
            select(Subscription).where(
                Subscription.status == "active",
                Subscription.next_charge_at <= now,
            )
        ).scalars().all()

        summary = {"attempted": 0, "succeeded": 0, "failed": 0, "past_due": 0}
        for sub in due:
            summary["attempted"] += 1
            try:
                order = self._charge_one(sub, now)
                summary["succeeded"] += 1
                self._record(sub, order, succeeded=True, failure=None, now=now)
                sub.last_charged_at = now
                sub.next_charge_at = now + timedelta(days=sub.cadence_days)
            except SquareDeclined as e:
                summary["failed"] += 1
                self._record(sub, None, succeeded=False, failure=f"declined: {e}", now=now)
                failures = self._recent_failures(sub)
                if failures >= 3:
                    sub.status = "cancelled"
                    sub.cancelled_at = now
                else:
                    sub.status = "past_due"
                try:
                    self.email.send(
                        "subscription_failed", to=self._customer_email(sub),
                        subscription=sub, failure_reason=str(e),
                    )
                except Exception:
                    pass
            except SquareError as e:
                summary["failed"] += 1
                self._record(sub, None, succeeded=False, failure=f"error: {e}", now=now)
                sub.status = "past_due"
            self.session.commit()
        return summary

    def _charge_one(self, sub: Subscription, now: datetime) -> Order:
        customer = self.session.get(Customer, sub.customer_id)
        product = self.session.get(Product, sub.product_id)
        if customer is None or product is None:
            raise SubscriptionError("subscription references missing customer/product")

        payment = self.square.charge_saved_card(
            square_card_id=sub.square_card_id,
            amount_cents=product.price_cents * sub.qty,
            customer_id=customer.square_customer_id,
            # Square caps idempotency_key at 45 chars. Keep short + deterministic
            # within a charge period so retries dedupe: 8 hex of sub id + unix mins.
            reference_id=f"s{sub.id.hex[:8]}{int(now.timestamp() // 60)}",
        )
        from secrets import token_urlsafe
        order = Order(
            public_token=token_urlsafe(16),
            customer_id=customer.id,
            customer_email=customer.email,
            customer_name=f"{customer.first_name or ''} {customer.last_name or ''}".strip() or customer.email,
            shipping_address_json={},
            billing_address_json={},
            subtotal_cents=product.price_cents * sub.qty,
            tax_cents=0, shipping_cents=0,
            total_cents=product.price_cents * sub.qty,
            status="paid",
            square_order_id=payment.get("order_id") or payment["id"],
            square_payment_id=payment["id"],
            autoship=True,
            autoship_subscription_id=sub.id,
            placed_at=now,
        )
        self.session.add(order); self.session.flush()
        self.session.add(OrderItem(
            order_id=order.id, product_id=product.id,
            sku_snapshot=product.sku, name_snapshot=product.name,
            image_path_snapshot=product.image_path,
            price_snapshot_cents=product.price_cents, qty=sub.qty,
            line_total_cents=product.price_cents * sub.qty,
        ))
        self.session.flush()
        from solex.services.inventory import InventoryService
        InventoryService(self.session).decrement_for_order(order)
        return order

    def _record(self, sub: Subscription, order: Optional[Order],
                *, succeeded: bool, failure: Optional[str], now: datetime):
        self.session.add(SubscriptionCharge(
            subscription_id=sub.id,
            order_id=order.id if order else None,
            attempted_at=now, succeeded=succeeded, failure_reason=failure,
        ))

    def _recent_failures(self, sub: Subscription) -> int:
        rows = self.session.execute(
            select(SubscriptionCharge).where(
                SubscriptionCharge.subscription_id == sub.id
            ).order_by(SubscriptionCharge.attempted_at.desc()).limit(3)
        ).scalars().all()
        return sum(1 for c in rows if not c.succeeded)

    def _customer_email(self, sub: Subscription) -> str:
        customer = self.session.get(Customer, sub.customer_id)
        return customer.email if customer else ""
