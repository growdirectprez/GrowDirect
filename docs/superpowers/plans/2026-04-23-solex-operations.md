# Solex Operations Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Layer operational surfaces on top of the Plan 1 foundation: admin CRUD for catalog/orders/inventory/customers/subscriptions/returns, customer account self-service (orders, addresses, subscriptions), live autoship subscriptions with scheduled charging, customer-initiated refund/returns flow, cart abandonment emails, product search, and a feature-flagged catalog-mirror to Square's Catalog API.

**Architecture:** Extends the Plan 1 Flask app. Adds `Subscription`, `SubscriptionCharge`, `ReturnRequest` models (+ migration 0002). Adds new blueprints `admin`, `admin_catalog`, `admin_orders`, `admin_inventory`, `admin_customers`, `admin_subscriptions`, `admin_returns`, and `account`, `account_orders`, `account_addresses`, `account_subscriptions`. Adds services `subscriptions`, `returns`, `abandonment`, `search`, `catalog_sync`. Wires RQ-scheduler cron jobs for autoship charging and cart abandonment. Storefront gets `/search`.

**Tech Stack:** Same as Plan 1 — Python 3.12, Flask 3, SQLAlchemy 2.0 `Mapped[]`, Postgres 17, Valkey 8, Tailwind 3 + Alpine 3, squareup SDK sandbox, RQ + rq-scheduler, Flask-Login magic-link, pytest. No new runtime dependencies.

---

## Scope

**This is Plan 2 of 4.** Depends on Plan 1 code being present on the branch.

**In scope:**
- Data model: `Subscription`, `SubscriptionCharge`, `ReturnRequest` + migration 0002
- `SubscriptionService` — create, charge_due, pause, resume, cancel; Square card-on-file
- `ReturnsService` — RMA request → admin approve → refund via existing `RefundsService`
- `AbandonmentService` — sweep stale carts, send recovery emails
- `SearchService` — Postgres tsvector, populate on product upsert, query
- `CatalogSyncService` — mirror local Product catalog to Square Catalog API (feature-flagged)
- Admin dashboard + 6 CRUD surfaces: catalog, orders, inventory, customers, subscriptions, returns
- Customer account: dashboard + 4 surfaces: orders, addresses, subscriptions, return-request form
- RQ scheduler bootstrap + 2 cron jobs: autoship charging (every 15 min), abandonment sweep (every 30 min)
- Storefront `/search` endpoint
- Storefront product-detail page gains "Subscribe & save" autoship option
- Tests: unit + integration + 1 sandbox-live subscription test

**Out of scope (later plans):**
- Scenario runner + 9 scenarios (Plan 3)
- Visual fidelity pass matching solexglobal.com (Plan 4)
- Full 25-SKU catalog curation with real imagery (Plan 4)
- Multi-tenant / multi-merchant support (not planned)
- Live Square mode cut-over (separate spec when we get there)

**Definition of done for Plan 2:**
1. Admin logs in at `/admin/login`, lands on `/admin` dashboard, can navigate to catalog/orders/inventory/customers/subscriptions/returns and complete basic operations.
2. Customer magic-link signs in at `/account/login`, lands on `/account` dashboard, can view orders, request a return, manage addresses, pause/resume/cancel a subscription.
3. A "Subscribe every 30 days" option on a product page creates a `Subscription`. The rq-scheduler cron runs `charge_due_subscriptions()` which charges the saved card via Square and emits a new Order tagged `autoship=true`.
4. A cart left idle ≥ 2h receives an abandonment email (verified in MailHog). A cart abandoned ≥ 24h later gets a second nudge.
5. `/search?q=...` returns relevant products via Postgres full-text.
6. `SOLEX_FLAG_SYNC_CATALOG_TO_SQUARE=true` makes the catalog importer also upsert into Square's Catalog API; default is false.
7. `pytest tests/unit tests/integration tests/smoke` green including all Plan 1 tests. Sandbox-live subscription test green.
8. No regression in Plan 1 flows: browse, cart, guest checkout, webhook orphan recovery all still work.

---

## Prerequisites

- [ ] Linear sub-issue under GRO-521 (create: "Solex — Operations layer (Plan 2)"), reference in commits as `Refs GRO-XXX`.
- [ ] Plan 1 branch `plan/solex-foundation` is available locally (merged to main OR accessible as the branch Plan 2 branches off). This plan assumes its 40 commits are present.
- [ ] `Solex/.env` has real `SQUARE_SANDBOX_*` values (set during Plan 1 final verification).
- [ ] Shared infra running: `cd ~/GrowDirect/devops && docker compose up -d`.
- [ ] Worker container (RQ) reachable via `docker compose exec worker rq info --url redis://:valkey_dev@growdirect_valkey:6379/2`.
- [ ] Fresh worktree / branch for Plan 2: `git checkout -b plan/solex-operations plan/solex-foundation`.

Useful skills:
- @superpowers:test-driven-development
- @superpowers:systematic-debugging
- @superpowers:verification-before-completion

---

## File Structure

### New models

```
Solex/solex/models/
├── subscription.py     Subscription, SubscriptionCharge
└── returns.py          ReturnRequest
```

Modify `Solex/solex/models/__init__.py` to export the new classes.

### New services

```
Solex/solex/services/
├── subscriptions.py    SubscriptionService — create, charge_due, pause/resume/cancel
├── returns.py          ReturnsService — request, approve, reject, complete
├── abandonment.py      AbandonmentService — sweep, record email sends
├── search.py           SearchService — tsvector build + query
└── catalog_sync.py     CatalogSyncService — Square Catalog mirror (feature-flagged)
```

### New blueprints

```
Solex/solex/routes/
├── admin.py                dashboard at /admin
├── admin_catalog.py        /admin/catalog (CRUD)
├── admin_orders.py         /admin/orders (list, detail, refund)
├── admin_inventory.py      /admin/inventory (list, adjust)
├── admin_customers.py      /admin/customers (list, detail)
├── admin_subscriptions.py  /admin/subscriptions (list, detail)
├── admin_returns.py        /admin/returns (list, approve/reject)
├── account.py              /account dashboard
├── account_orders.py       /account/orders + /account/orders/<id>/return
├── account_addresses.py    /account/addresses (CRUD)
└── account_subscriptions.py  /account/subscriptions (view, pause/resume/cancel)
```

### Jobs

```
Solex/solex/jobs/
├── __init__.py
├── scheduler.py            rq-scheduler bootstrap
├── subscriptions.py        charge_due_subscriptions
└── abandonment.py          run_abandonment_sweep
```

### Templates

```
Solex/solex/templates/
├── admin/
│   ├── _layout.html        admin shell (extends base with sidebar)
│   ├── dashboard.html
│   ├── catalog/{list,form}.html
│   ├── orders/{list,detail}.html
│   ├── inventory/list.html
│   ├── customers/list.html
│   ├── subscriptions/list.html
│   └── returns/{list,detail}.html
├── account/
│   ├── _layout.html        customer account shell
│   ├── dashboard.html
│   ├── orders/{list,detail,return_form}.html
│   ├── addresses.html
│   └── subscriptions/{list,detail}.html
├── storefront/
│   └── search.html
└── emails/
    ├── cart_abandonment.{html,txt}
    ├── subscription_charged.{html,txt}
    ├── subscription_failed.{html,txt}
    └── return_approved.{html,txt}
```

### Modified files

- `Solex/solex/routes/storefront.py` — add `/search` route
- `Solex/solex/routes/checkout.py` — honor "save card" flag + autoship-enabled cart line
- `Solex/solex/routes/cart.py` — accept optional `subscription_cadence_days` on add
- `Solex/solex/templates/storefront/product_detail.html` — add "Subscribe & save" toggle
- `Solex/solex/cli.py` — add `scheduler run-local` + `search rebuild` + `catalog sync-to-square`
- `Solex/devops/docker-compose.yml` — add `scheduler` service (rq-scheduler)
- `Solex/solex/__init__.py` — register all new blueprints
- `Solex/solex/extensions.py` — no changes expected; user_loader already there from Plan 1

---

## Chunk 1: Data model additions + migration 0002

### Task 1.1 — Subscription + SubscriptionCharge models

**Files:**
- Create: `Solex/solex/models/subscription.py`
- Create: `Solex/tests/unit/test_models_subscription.py`
- Modify: `Solex/solex/models/__init__.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/unit/test_models_subscription.py
from datetime import datetime, timezone
from solex.models.subscription import Subscription, SubscriptionCharge

def test_subscription_fields():
    s = Subscription(
        qty=1, cadence_days=30, square_card_id="ccof:card_abc",
        next_charge_at=datetime.now(timezone.utc), status="active",
    )
    assert s.cadence_days == 30
    assert s.status == "active"

def test_subscription_charge_fields():
    c = SubscriptionCharge(attempted_at=datetime.now(timezone.utc), succeeded=True)
    assert c.succeeded is True
```

- [ ] **Step 2: Verify RED** — `docker compose -f devops/docker-compose.yml run --rm -e SOLEX_ENV=testing web pytest tests/unit/test_models_subscription.py -v`. Expect `ImportError`.

- [ ] **Step 3: Write the models**

```python
# solex/models/subscription.py
import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy import String, Integer, Boolean, ForeignKey, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from solex.models.base import BaseModel

SUBSCRIPTION_STATUSES = ("active", "paused", "cancelled", "past_due")

class Subscription(BaseModel):
    __tablename__ = "subscriptions"
    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False,
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id", ondelete="RESTRICT"), nullable=False,
    )
    qty: Mapped[int] = mapped_column(Integer, nullable=False)
    cadence_days: Mapped[int] = mapped_column(Integer, nullable=False)
    square_card_id: Mapped[str] = mapped_column(String(120), nullable=False)
    next_charge_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    paused_until: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_charged_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    cancelled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    charges: Mapped[list["SubscriptionCharge"]] = relationship(
        back_populates="subscription", cascade="all, delete-orphan",
    )
    __table_args__ = (
        Index("ix_subs_status", "status"),
        Index("ix_subs_next_charge", "next_charge_at"),
    )

class SubscriptionCharge(BaseModel):
    __tablename__ = "subscription_charges"
    subscription_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("subscriptions.id", ondelete="CASCADE"), nullable=False,
    )
    order_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("orders.id", ondelete="SET NULL"), nullable=True,
    )
    attempted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    succeeded: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    failure_reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    subscription: Mapped[Subscription] = relationship(back_populates="charges")
```

- [ ] **Step 4: Export from `solex/models/__init__.py`**

Add:
```python
from solex.models.subscription import Subscription, SubscriptionCharge, SUBSCRIPTION_STATUSES
```
and to `__all__`: `"Subscription", "SubscriptionCharge", "SUBSCRIPTION_STATUSES"`.

- [ ] **Step 5: Run tests GREEN**

- [ ] **Step 6: Commit**

```bash
git add Solex/
git commit -m "solex(models): Subscription + SubscriptionCharge

Refs GRO-XXX. Plan 2 task 1.1."
```

### Task 1.2 — ReturnRequest model

**Files:**
- Create: `Solex/solex/models/returns.py`
- Create: `Solex/tests/unit/test_models_returns.py`
- Modify: `Solex/solex/models/__init__.py`

- [ ] **Step 1: Write failing test**

```python
# tests/unit/test_models_returns.py
from solex.models.returns import ReturnRequest

def test_return_request_fields():
    r = ReturnRequest(reason="didn't fit", status="pending")
    assert r.status == "pending"
```

- [ ] **Step 2: Verify RED.**

- [ ] **Step 3: Write the model**

```python
# solex/models/returns.py
import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy import String, Text, ForeignKey, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from solex.models.base import BaseModel

RETURN_STATUSES = ("pending", "approved", "denied", "completed")

class ReturnRequest(BaseModel):
    __tablename__ = "return_requests"
    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False,
    )
    customer_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("customers.id", ondelete="SET NULL"), nullable=True,
    )
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    approved_by_admin_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("admin_users.id", ondelete="SET NULL"), nullable=True,
    )
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    refund_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("refunds.id", ondelete="SET NULL"), nullable=True,
    )
    __table_args__ = (
        Index("ix_returns_status", "status"),
        Index("ix_returns_order", "order_id"),
    )
```

- [ ] **Step 4: Export** from `__init__.py`: add `ReturnRequest`, `RETURN_STATUSES`.

- [ ] **Step 5: Run GREEN.**

- [ ] **Step 6: Commit**

```bash
git add Solex/
git commit -m "solex(models): ReturnRequest

Refs GRO-XXX. Plan 2 task 1.2."
```

### Task 1.3 — Migration 0002

**Files:**
- Create: `Solex/alembic/versions/0002_subscriptions_and_returns.py`

- [ ] **Step 1: Generate**

```bash
docker compose -f devops/docker-compose.yml run --rm web \
  alembic revision --autogenerate -m "subscriptions and returns"
```

- [ ] **Step 2: Rename** the generated file to `0002_subscriptions_and_returns.py`. Inspect. Verify:
- `subscriptions`, `subscription_charges`, `return_requests` tables all present
- `subscriptions.product_id` FK has `ondelete='RESTRICT'` (prevents Product delete when subs exist)
- `subscriptions.customer_id` FK has `ondelete='CASCADE'`
- `subscription_charges.subscription_id` FK has `ondelete='CASCADE'`
- `return_requests.order_id` FK has `ondelete='CASCADE'`
- Indexes on `subscriptions.status`, `next_charge_at`, `return_requests.status`, `order_id`

- [ ] **Step 3: Upgrade both DBs**

```bash
docker compose -f devops/docker-compose.yml run --rm web alembic upgrade head
docker compose -f devops/docker-compose.yml run --rm -e SOLEX_ENV=testing web alembic upgrade head
```

- [ ] **Step 4: Verify tables**

```bash
docker exec -i growdirect_postgres psql -U growdirect -d solex -c "\dt" | grep -E "(subscriptions|return_requests)"
```

- [ ] **Step 5: Run full test suite** to confirm no regression:

```bash
docker compose -f devops/docker-compose.yml run --rm -e SOLEX_ENV=testing web pytest -v
```

Expect: all green (~85 tests now).

- [ ] **Step 6: Commit**

```bash
git add Solex/alembic/
git commit -m "solex(models): migration 0002 — subscriptions + return_requests

Refs GRO-XXX. Plan 2 task 1.3."
```

---

## Chunk 2: SubscriptionService + card-on-file + autoship engine

### Task 2.1 — Extend SquareClient with card-on-file methods

**Files:**
- Modify: `Solex/solex/services/square_client.py`
- Create: `Solex/tests/unit/test_square_client_cards.py`

Add `create_customer`, `save_card_on_file`, `charge_saved_card` methods. Adapt to squareup==44 SDK shape.

```python
# append to solex/services/square_client.py
    def create_customer(self, email: str, name: Optional[str] = None) -> dict:
        result = self._client.customers.create(
            email_address=email,
            given_name=name or "",
        )
        self._raise(result)
        return _dump(result.customer)  # adapt helper as in Plan 1

    def save_card_on_file(self, square_customer_id: str, source_id: str) -> dict:
        """source_id is a Square payment token (cnon:...). Returns card object with .id = ccof:..."""
        result = self._client.cards.create(
            idempotency_key=_gen_idem_key(),
            source_id=source_id,
            card={"customer_id": square_customer_id},
        )
        self._raise(result)
        return _dump(result.card)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, max=4),
           retry=retry_if_exception_type(SquareTransient))
    def charge_saved_card(self, square_card_id: str, amount_cents: int,
                          customer_id: str, reference_id: Optional[str] = None) -> dict:
        result = self._client.payments.create(
            source_id=square_card_id,
            customer_id=customer_id,
            idempotency_key=reference_id or _gen_idem_key(),
            amount_money={"amount": amount_cents, "currency": "USD"},
            location_id=self.cfg.location_id,
        )
        self._raise(result)
        return _dump(result.payment)
```

> If `_dump` helper doesn't exist in Plan 1's `square_client.py`, add: `def _dump(obj): return obj.model_dump() if hasattr(obj, "model_dump") else dict(obj)`.

**Unit tests** (mock the SDK):

```python
# tests/unit/test_square_client_cards.py
from unittest.mock import MagicMock, patch
from solex.services.square_client import SquareClient, SquareConfig, SquareDeclined

def _cfg():
    return SquareConfig(access_token="sb", environment="sandbox",
                        location_id="L", webhook_signature_key="whk")

def test_create_customer(mocker):
    mock = MagicMock()
    mock.customers.create.return_value = MagicMock(
        _dump_helper=lambda: None,
    )
    # Adapt based on actual squareup v44 shape discovered during Plan 1
    ...  # flesh in pattern matching the CheckoutService tests

def test_save_card_returns_card_id(mocker):
    ...

def test_charge_saved_card_declined_raises(mocker):
    ...
```

> **Note to executor:** the exact SDK response shape was adapted in Plan 1's `square_client.py` (Fern-generated, Pydantic typed). Pattern-match on what's already there; don't re-derive.

- [ ] **Commit:** `solex(services): SquareClient — customers + cards-on-file + charge_saved_card`.

### Task 2.2 — SubscriptionService (create, charge_due, pause/resume/cancel)

**Files:**
- Create: `Solex/solex/services/subscriptions.py`
- Create: `Solex/tests/unit/test_services_subscriptions.py`

```python
# solex/services/subscriptions.py
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from solex.models import (
    Subscription, SubscriptionCharge, Customer, Product, Order, OrderItem,
)
from solex.services.square_client import SquareClient, SquareDeclined, SquareError
from solex.services.checkout import CheckoutService, CartLineIn, CustomerIn
from solex.services.email import EmailService

class SubscriptionError(Exception): ...

class SubscriptionService:
    def __init__(self, session: Session, square: SquareClient,
                 checkout: CheckoutService, email: Optional[EmailService] = None):
        self.session = session
        self.square = square
        self.checkout = checkout
        self.email = email or EmailService()

    # -- customer-facing lifecycle ---------------------------------------

    def create(self, *, customer: Customer, product: Product, qty: int,
               cadence_days: int, starting_at: datetime,
               square_card_id: str) -> Subscription:
        sub = Subscription(
            customer_id=customer.id,
            product_id=product.id,
            qty=qty,
            cadence_days=cadence_days,
            square_card_id=square_card_id,
            next_charge_at=starting_at,
            status="active",
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
        # push next_charge_at forward if it's in the past
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

    # -- scheduler-facing ------------------------------------------------

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
                self.email.send(
                    "subscription_failed", to=self._customer_email(sub),
                    subscription=sub, failure_reason=str(e),
                )
            except SquareError as e:
                summary["failed"] += 1
                self._record(sub, None, succeeded=False, failure=f"error: {e}", now=now)
                sub.status = "past_due"
            self.session.commit()
        return summary

    # -- internals -------------------------------------------------------

    def _charge_one(self, sub: Subscription, now: datetime) -> Order:
        customer = self.session.get(Customer, sub.customer_id)
        product = self.session.get(Product, sub.product_id)
        if customer is None or product is None:
            raise SubscriptionError("subscription references missing customer/product")

        # Use checkout.place_order via card-on-file path: no Square payment token from the
        # browser — we charge the saved card directly and wrap into an Order.
        payment = self.square.charge_saved_card(
            square_card_id=sub.square_card_id,
            amount_cents=product.price_cents * sub.qty,
            customer_id=customer.square_customer_id,
            reference_id=f"autoship:{sub.id}:{now.isoformat()}",
        )
        # Compose an Order row manually — bypass CheckoutService because this flow
        # skips tokenization and already has the payment in hand.
        from secrets import token_urlsafe
        order = Order(
            public_token=token_urlsafe(16),
            customer_id=customer.id,
            customer_email=customer.email,
            customer_name=f"{customer.first_name or ''} {customer.last_name or ''}".strip() or customer.email,
            shipping_address_json={},   # address captured on subscription signup in Plan 2b;
            billing_address_json={},    # for MVP, subscriptions ship to default address (TBD)
            subtotal_cents=product.price_cents * sub.qty,
            tax_cents=0,
            shipping_cents=0,
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
        # decrement inventory
        from solex.services.inventory import InventoryService
        InventoryService(self.session).decrement_for_order(order)
        return order

    def _record(self, sub: Subscription, order: Optional[Order],
                *, succeeded: bool, failure: Optional[str], now: datetime):
        self.session.add(SubscriptionCharge(
            subscription_id=sub.id,
            order_id=order.id if order else None,
            attempted_at=now,
            succeeded=succeeded,
            failure_reason=failure,
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
```

> **Important invariant:** `charge_one` shortcuts `CheckoutService.place_order` because there's no browser-side tokenization. If the shape of `Order` diverges later, the two paths must stay in sync. A shared `_persist_order_from_payment` helper is an acceptable refactor if drift becomes visible.

**Tests** (mock Square):

```python
# tests/unit/test_services_subscriptions.py
from unittest.mock import MagicMock
from datetime import datetime, timedelta, timezone
from solex.services.subscriptions import SubscriptionService
from solex.services.square_client import SquareDeclined
from solex.services.checkout import CheckoutService
from solex.services.tax import FlatRateTaxStub
from solex.services.shipping import FlatRateShippingStub
from solex.services.inventory import InventoryService
from solex.services.email import EmailService
from solex.models import Subscription, Customer, Product, Inventory, Order, SubscriptionCharge

def _seed_cp(db_session):
    c = Customer(email="sub@ex.com", first_name="Sub", last_name="Scriber")
    db_session.add(c); db_session.flush()
    p = Product(sku="S1", slug="s1", name="Subbed", price_cents=2000,
                image_path="", active=True, weight_grams=100)
    db_session.add(p); db_session.flush()
    db_session.add(Inventory(product_id=p.id, on_hand=20))
    c.square_customer_id = "cust_1"
    db_session.commit()
    return c, p

def _svc(db_session, square, checkout=None, email=None):
    checkout = checkout or CheckoutService(
        session=db_session, square=square,
        tax=FlatRateTaxStub(0.0),
        shipping=FlatRateShippingStub(flat_cents=0, free_threshold_cents=999999),
        inventory=InventoryService(db_session),
    )
    return SubscriptionService(db_session, square, checkout, email or MagicMock())

def test_create_subscription(app, db_session):
    c, p = _seed_cp(db_session)
    svc = _svc(db_session, MagicMock())
    sub = svc.create(customer=c, product=p, qty=1, cadence_days=30,
                     starting_at=datetime.now(timezone.utc), square_card_id="ccof:ABC")
    assert sub.status == "active"
    assert db_session.query(Subscription).count() == 1

def test_charge_due_happy_path(app, db_session):
    c, p = _seed_cp(db_session)
    sq = MagicMock()
    sq.charge_saved_card.return_value = {"id": "sqp_1", "order_id": "sqo_1"}
    svc = _svc(db_session, sq)
    past = datetime.now(timezone.utc) - timedelta(minutes=1)
    svc.create(customer=c, product=p, qty=2, cadence_days=30,
               starting_at=past, square_card_id="ccof:ABC")
    summary = svc.charge_due_subscriptions()
    assert summary == {"attempted": 1, "succeeded": 1, "failed": 0, "past_due": 0}
    assert db_session.query(Order).filter_by(autoship=True).count() == 1
    inv = db_session.query(Inventory).filter_by(product_id=p.id).one()
    assert inv.on_hand == 18  # 20 - 2

def test_charge_due_declined_marks_past_due(app, db_session):
    c, p = _seed_cp(db_session)
    sq = MagicMock()
    sq.charge_saved_card.side_effect = SquareDeclined("card expired")
    email = MagicMock()
    svc = _svc(db_session, sq, email=email)
    past = datetime.now(timezone.utc) - timedelta(minutes=1)
    sub = svc.create(customer=c, product=p, qty=1, cadence_days=30,
                     starting_at=past, square_card_id="ccof:BAD")
    summary = svc.charge_due_subscriptions()
    assert summary["failed"] == 1
    db_session.refresh(sub)
    assert sub.status == "past_due"
    email.send.assert_called_once()
    assert db_session.query(Order).count() == 0

def test_three_failures_cancels(app, db_session):
    c, p = _seed_cp(db_session)
    sq = MagicMock(); sq.charge_saved_card.side_effect = SquareDeclined("nope")
    svc = _svc(db_session, sq)
    past = datetime.now(timezone.utc) - timedelta(minutes=1)
    sub = svc.create(customer=c, product=p, qty=1, cadence_days=30,
                     starting_at=past, square_card_id="ccof:BAD")
    for _ in range(3):
        svc.charge_due_subscriptions()
        sub.next_charge_at = datetime.now(timezone.utc) - timedelta(minutes=1)
        db_session.commit()
    db_session.refresh(sub)
    assert sub.status == "cancelled"

def test_pause_and_resume(app, db_session):
    c, p = _seed_cp(db_session)
    svc = _svc(db_session, MagicMock())
    sub = svc.create(customer=c, product=p, qty=1, cadence_days=30,
                     starting_at=datetime.now(timezone.utc), square_card_id="ccof:ABC")
    svc.pause(sub)
    assert sub.status == "paused"
    svc.resume(sub)
    assert sub.status == "active"
    assert sub.paused_until is None

def test_cancel(app, db_session):
    c, p = _seed_cp(db_session)
    svc = _svc(db_session, MagicMock())
    sub = svc.create(customer=c, product=p, qty=1, cadence_days=30,
                     starting_at=datetime.now(timezone.utc), square_card_id="ccof:ABC")
    svc.cancel(sub)
    assert sub.status == "cancelled"
    assert sub.cancelled_at is not None
```

- [ ] Run GREEN. Commit: `solex(services): SubscriptionService + autoship charging`.

---

## Chunk 3: Returns service + ReturnRequest flow

### Task 3.1 — ReturnsService

**Files:**
- Create: `Solex/solex/services/returns.py`
- Create: `Solex/tests/unit/test_services_returns.py`

```python
# solex/services/returns.py
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session
from solex.models import ReturnRequest, Order, AdminUser
from solex.services.refunds import RefundsService
from solex.services.email import EmailService

class ReturnsError(Exception): ...

class ReturnsService:
    def __init__(self, session: Session, refunds: RefundsService,
                 email: Optional[EmailService] = None):
        self.session = session
        self.refunds = refunds
        self.email = email or EmailService()

    def request(self, order: Order, reason: str) -> ReturnRequest:
        req = ReturnRequest(
            order_id=order.id, customer_id=order.customer_id,
            reason=reason, status="pending",
        )
        self.session.add(req); self.session.commit()
        return req

    def approve(self, req: ReturnRequest, admin: AdminUser) -> ReturnRequest:
        if req.status != "pending":
            raise ReturnsError(f"cannot approve from status={req.status}")
        order = self.session.get(Order, req.order_id)
        refund = self.refunds.issue_refund(order, order.total_cents,
                                           reason=f"return:{req.id}")
        req.refund_id = refund.id
        req.status = "completed"
        req.approved_by_admin_user_id = admin.id
        req.resolved_at = datetime.now(timezone.utc)
        self.session.commit()
        try:
            self.email.send("return_approved", to=order.customer_email,
                            order=order, return_request=req)
        except Exception:
            pass
        return req

    def deny(self, req: ReturnRequest, admin: AdminUser, reason: str = "") -> ReturnRequest:
        if req.status != "pending":
            raise ReturnsError(f"cannot deny from status={req.status}")
        req.status = "denied"
        req.approved_by_admin_user_id = admin.id
        req.resolved_at = datetime.now(timezone.utc)
        self.session.commit()
        return req
```

**Tests** mock `RefundsService`:

```python
# tests/unit/test_services_returns.py
from unittest.mock import MagicMock
from datetime import datetime, timezone
from solex.services.returns import ReturnsService, ReturnsError
from solex.models import Order, ReturnRequest, AdminUser, Refund

def _seed_order(db_session):
    o = Order(public_token="t", customer_email="c@x.y", customer_name="C",
              shipping_address_json={}, billing_address_json={},
              subtotal_cents=1000, tax_cents=0, shipping_cents=0, total_cents=1000,
              square_order_id="o", square_payment_id="p",
              placed_at=datetime.now(timezone.utc), status="paid")
    db_session.add(o); db_session.commit()
    return o

def test_request_creates_pending(app, db_session):
    o = _seed_order(db_session)
    refunds = MagicMock()
    svc = ReturnsService(db_session, refunds, email=MagicMock())
    req = svc.request(o, "too small")
    assert req.status == "pending"

def test_approve_issues_refund(app, db_session):
    o = _seed_order(db_session)
    refunds = MagicMock()
    refunds.issue_refund.return_value = Refund(
        id=None, order_id=o.id, amount_cents=1000, reason="x",
    )
    svc = ReturnsService(db_session, refunds, email=MagicMock())
    req = svc.request(o, "damaged")
    admin = AdminUser(email="a@b.c", active=True)
    db_session.add(admin); db_session.commit()
    svc.approve(req, admin)
    assert req.status == "completed"
    refunds.issue_refund.assert_called_once()

def test_approve_twice_raises(app, db_session):
    o = _seed_order(db_session)
    refunds = MagicMock(); refunds.issue_refund.return_value = Refund(order_id=o.id, amount_cents=1000, reason="x")
    svc = ReturnsService(db_session, refunds, email=MagicMock())
    req = svc.request(o, "x")
    admin = AdminUser(email="a@b.c", active=True); db_session.add(admin); db_session.commit()
    svc.approve(req, admin)
    import pytest
    with pytest.raises(ReturnsError):
        svc.approve(req, admin)
```

- [ ] Commit: `solex(services): ReturnsService — request/approve/deny`.

---

## Chunk 4: Abandonment + Search + Catalog-sync (feature-flagged)

### Task 4.1 — AbandonmentService

**Files:**
- Create: `Solex/solex/services/abandonment.py`
- Create: `Solex/tests/unit/test_services_abandonment.py`

Abandoned cart model: for Plan 1, guest carts were Valkey-only. Plan 2 needs persistent Carts to track abandonment. Two approaches:
- (a) Persist every cart with any line; write-through on mutations.
- (b) Mirror Valkey → DB only when TTL-based conditions are met.

Choose **(a)** — persistent `Cart` rows keyed by session_key or customer_id. The `Cart` model already exists from Plan 1 (unused until now).

Modify `Solex/solex/services/cart.py`:

- Add a `DbCartBackend` that writes through to `Cart` + `CartLine` on every `save()`. Use this when the request has `session["cart_key"]` established.
- Keep `ValkeyCartBackend` for hot-path reads; `DbCartBackend` is write-through for durability.

Actually simpler: extend `ValkeyCartBackend.save` to also upsert into the DB:

```python
# solex/services/cart.py — add to ValkeyCartBackend.save, after redis.setex:
        # Write-through to Postgres for abandonment sweep
        self._persist_to_db(key, snap)

    def _persist_to_db(self, key: str, snap):
        from solex.extensions import db
        from solex.models import Cart, CartLine
        from datetime import datetime, timezone
        from sqlalchemy import select, delete
        cart = db.session.execute(
            select(Cart).where(Cart.session_key == key)
        ).scalar_one_or_none()
        if cart is None:
            cart = Cart(session_key=key,
                        last_activity_at=datetime.now(timezone.utc),
                        currency=snap.currency)
            db.session.add(cart)
            db.session.flush()
        else:
            cart.last_activity_at = datetime.now(timezone.utc)
            cart.recovered_at = datetime.now(timezone.utc) if cart.abandonment_emailed_at else None
            db.session.execute(delete(CartLine).where(CartLine.cart_id == cart.id))
        from uuid import UUID
        for line in snap.lines:
            db.session.add(CartLine(
                cart_id=cart.id,
                product_id=UUID(line["product_id"]),
                qty=line["qty"],
                price_snapshot_cents=line["price_cents"],
            ))
        db.session.commit()
```

> The existing `ValkeyCartBackend` tests (in-memory backend) don't exercise this path — they use `MemoryBackend`. No regression in Plan 1 tests.

**AbandonmentService:**

```python
# solex/services/abandonment.py
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session
from solex.models import Cart, Product
from solex.services.email import EmailService

FIRST_NUDGE_DELAY = timedelta(hours=2)
SECOND_NUDGE_DELAY = timedelta(hours=24)

class AbandonmentService:
    def __init__(self, session: Session, email: EmailService | None = None):
        self.session = session
        self.email = email or EmailService()

    def sweep(self, *, now: datetime | None = None) -> dict:
        now = now or datetime.now(timezone.utc)
        summary = {"first_nudge": 0, "second_nudge": 0, "skipped": 0}
        # First nudge: carts idle ≥ 2h with lines, not yet emailed, customer_id present
        first = self.session.execute(
            select(Cart).where(
                Cart.last_activity_at <= now - FIRST_NUDGE_DELAY,
                Cart.abandonment_emailed_at.is_(None),
                Cart.recovered_at.is_(None),
                Cart.customer_id.is_not(None),
            )
        ).scalars().all()
        for cart in first:
            if not cart.lines:
                summary["skipped"] += 1; continue
            self._send_nudge(cart, "first", now)
            cart.abandonment_emailed_at = now
            summary["first_nudge"] += 1
        # Second nudge: idle ≥ 24h since first email, not recovered
        second = self.session.execute(
            select(Cart).where(
                Cart.abandonment_emailed_at.is_not(None),
                Cart.abandonment_emailed_at <= now - SECOND_NUDGE_DELAY,
                Cart.recovered_at.is_(None),
                Cart.customer_id.is_not(None),
            )
        ).scalars().all()
        for cart in second:
            self._send_nudge(cart, "second", now)
            # Mark as emailed again by pushing timestamp; second sweep won't re-email.
            # Simple: mark `recovered_at = now` to suppress further sends.
            cart.recovered_at = now  # "we gave up" signal
            summary["second_nudge"] += 1
        self.session.commit()
        return summary

    def _send_nudge(self, cart: Cart, stage: str, now: datetime):
        if cart.customer_id is None:
            return
        from solex.models import Customer
        customer = self.session.get(Customer, cart.customer_id)
        if customer is None:
            return
        try:
            self.email.send("cart_abandonment", to=customer.email,
                            cart=cart, stage=stage)
        except Exception:
            pass
```

> Abandonment only nudges *logged-in* customers (we don't have email for guest carts). Guest carts just expire in Valkey.

Tests: mock `EmailService`, create Cart with `last_activity_at` ≥2h ago, sweep, assert `abandonment_emailed_at` set + email.send called.

- [ ] Commit: `solex(services): AbandonmentService + Cart DB write-through`.

### Task 4.2 — SearchService (Postgres tsvector)

**Files:**
- Create: `Solex/solex/services/search.py`
- Create: `Solex/alembic/versions/0003_products_tsvector.py`
- Create: `Solex/tests/integration/test_services_search.py`
- Modify: `Solex/solex/services/catalog.py` — add `search()` method that delegates
- Modify: `Solex/solex/services/catalog_import.py` — call `SearchService.rebuild_for(product)` after upsert

**Migration 0003** — add a `tsvector` column + GIN index + trigger:

```python
# alembic/versions/0003_products_tsvector.py
"""products tsvector"""
from alembic import op
import sqlalchemy as sa

revision = "0003"
down_revision = "0002"

def upgrade():
    op.execute("""
        ALTER TABLE products ADD COLUMN search_tsv tsvector;
        CREATE INDEX ix_products_search_tsv ON products USING GIN (search_tsv);
        CREATE FUNCTION products_tsv_update() RETURNS trigger AS $$
        BEGIN
          NEW.search_tsv :=
            setweight(to_tsvector('english', coalesce(NEW.name,'')), 'A') ||
            setweight(to_tsvector('english', coalesce(NEW.short_description,'')), 'B') ||
            setweight(to_tsvector('english', coalesce(NEW.description,'')), 'C') ||
            setweight(to_tsvector('english', coalesce(NEW.sku,'')), 'A');
          RETURN NEW;
        END
        $$ LANGUAGE plpgsql;
        CREATE TRIGGER products_tsv_trigger
          BEFORE INSERT OR UPDATE ON products
          FOR EACH ROW EXECUTE FUNCTION products_tsv_update();
        UPDATE products SET id = id;  -- force trigger to populate existing rows
    """)

def downgrade():
    op.execute("""
        DROP TRIGGER IF EXISTS products_tsv_trigger ON products;
        DROP FUNCTION IF EXISTS products_tsv_update;
        DROP INDEX IF EXISTS ix_products_search_tsv;
        ALTER TABLE products DROP COLUMN IF EXISTS search_tsv;
    """)
```

Upgrade both DBs:
```bash
docker compose run --rm web alembic upgrade head
docker compose run --rm -e SOLEX_ENV=testing web alembic upgrade head
```

**Service:**

```python
# solex/services/search.py
from sqlalchemy import text
from sqlalchemy.orm import Session
from solex.models import Product

class SearchService:
    def __init__(self, session: Session):
        self.session = session

    def query(self, q: str, limit: int = 20):
        if not q or not q.strip():
            return []
        # plainto_tsquery is forgiving to natural-language input
        rows = self.session.execute(
            text("""
                SELECT id FROM products
                WHERE active = true
                  AND search_tsv @@ plainto_tsquery('english', :q)
                ORDER BY ts_rank(search_tsv, plainto_tsquery('english', :q)) DESC
                LIMIT :limit
            """),
            {"q": q, "limit": limit},
        ).all()
        ids = [r[0] for r in rows]
        if not ids:
            return []
        return self.session.query(Product).filter(Product.id.in_(ids)).all()

    def rebuild_all(self) -> int:
        # Trigger handles this by updating each row; alternative:
        self.session.execute(text("UPDATE products SET id = id"))
        self.session.commit()
        return self.session.execute(text("SELECT COUNT(*) FROM products WHERE search_tsv IS NOT NULL")).scalar() or 0
```

**Storefront route:**

Modify `solex/routes/storefront.py`:

```python
from solex.services.search import SearchService

@bp.get("/search")
def search():
    q = (request.args.get("q") or "").strip()
    results = SearchService(db.session).query(q) if q else []
    return render_template("storefront/search.html", q=q, results=results)
```

**Template** `templates/storefront/search.html`:

```html
{% extends "base.html" %}
{% block main %}
<h1 class="text-2xl font-semibold mb-4">Search{% if q %}: "{{ q }}"{% endif %}</h1>
<form method="get" class="mb-6">
  <input name="q" value="{{ q }}" placeholder="Search products…" class="border p-2 w-64">
  <button type="submit" class="bg-stone-900 text-white px-3 py-2">Search</button>
</form>
<ul class="grid grid-cols-2 md:grid-cols-3 gap-6">
  {% for p in results %}
  <li>
    <a href="{{ url_for('storefront.product_detail', slug=p.slug) }}">
      <div class="text-sm font-medium">{{ p.name }}</div>
      <div class="text-xs text-stone-500">${{ '%.2f' % (p.price_cents / 100) }}</div>
    </a>
  </li>
  {% endfor %}
</ul>
{% if q and not results %}<p class="text-stone-500">No matches.</p>{% endif %}
{% endblock %}
```

**Add search box to base nav** (optional but cheap — drop a `<form>` in `base.html` header).

Tests:

```python
# tests/integration/test_services_search.py
from solex.services.search import SearchService

def test_search_finds_by_name(app, db_session, seed_catalog):
    hits = SearchService(db_session).query("youth")
    assert any(p.sku == "AO-YOUTH-30" for p in hits)

def test_search_finds_by_short_description(app, db_session, seed_catalog):
    hits = SearchService(db_session).query("frequency")
    assert any(p.sku == "AO-SCAN-V1" for p in hits)

def test_search_empty_query_returns_empty(app, db_session, seed_catalog):
    assert SearchService(db_session).query("") == []
```

- [ ] Commit: `solex(services): SearchService + /search + migration 0003 tsvector`.

### Task 4.3 — CatalogSyncService (feature-flagged)

**Files:**
- Create: `Solex/solex/services/catalog_sync.py`
- Create: `Solex/tests/unit/test_services_catalog_sync.py`
- Modify: `Solex/solex/services/catalog_import.py` — optionally call sync after import
- Modify: `Solex/solex/cli.py` — add `catalog sync-to-square` subcommand

```python
# solex/services/catalog_sync.py
from sqlalchemy import select
from sqlalchemy.orm import Session
from solex.models import Product
from solex.services.square_client import SquareClient

class CatalogSyncService:
    def __init__(self, session: Session, square: SquareClient):
        self.session = session
        self.square = square

    def sync_all(self) -> dict:
        products = self.session.execute(
            select(Product).where(Product.active == True)
        ).scalars().all()
        summary = {"synced": 0, "errored": 0}
        for p in products:
            try:
                obj = self._upsert(p)
                if not p.square_catalog_object_id and obj.get("id"):
                    p.square_catalog_object_id = obj["id"]
                summary["synced"] += 1
            except Exception:
                summary["errored"] += 1
        self.session.commit()
        return summary

    def _upsert(self, p: Product) -> dict:
        # Minimal Square ITEM + ITEM_VARIATION upsert. Exact API shape depends
        # on squareup==44's CatalogApi / catalog service. Placeholder pattern:
        return self.square.upsert_catalog_item(
            name=p.name,
            description=p.description,
            sku=p.sku,
            price_cents=p.price_cents,
            square_object_id=p.square_catalog_object_id,
        )
```

> Add an `upsert_catalog_item` method to `SquareClient` — wrap the Catalog API's `upsertCatalogObject` with the Item + Variation shape. If the SDK exposes it differently, adapt as you did in Plan 1 for orders/payments.

**Feature-flag integration** in `catalog_import.py`:

```python
# after self.session.commit() in import_from_yaml:
        if os.environ.get("SOLEX_FLAG_SYNC_CATALOG_TO_SQUARE", "").lower() == "true":
            from solex.services.catalog_sync import CatalogSyncService
            from solex.services.square_client import SquareClient, SquareConfig
            cfg = SquareConfig(
                access_token=os.environ["SQUARE_SANDBOX_ACCESS_TOKEN"],
                environment=os.environ.get("SQUARE_ENVIRONMENT", "sandbox"),
                location_id=os.environ["SQUARE_SANDBOX_LOCATION_ID"],
                webhook_signature_key=os.environ.get("SQUARE_SANDBOX_WEBHOOK_SIGNATURE_KEY", ""),
            )
            CatalogSyncService(self.session, SquareClient(cfg)).sync_all()
```

**CLI:**

```python
# solex/cli.py — add to catalog group:
@catalog.command("sync-to-square")
def sync_to_square():
    app = create_app()
    with app.app_context():
        from solex.services.square_client import SquareClient, SquareConfig
        cfg = SquareConfig(
            access_token=app.config["SQUARE_ACCESS_TOKEN"],
            environment=app.config["SQUARE_ENVIRONMENT"],
            location_id=app.config["SQUARE_LOCATION_ID"],
            webhook_signature_key=app.config["SQUARE_WEBHOOK_SIGNATURE_KEY"],
        )
        sq = SquareClient(cfg)
        from solex.services.catalog_sync import CatalogSyncService
        summary = CatalogSyncService(db.session, sq).sync_all()
        click.echo(f"synced: {summary}")
```

Tests: mock `SquareClient.upsert_catalog_item`; assert `square_catalog_object_id` gets persisted on the first call.

- [ ] Commit: `solex(services): CatalogSyncService + feature flag`.

---

## Chunk 5: Admin — shared harness + catalog CRUD

### Task 5.1 — Admin shared harness

**Files:**
- Create: `Solex/solex/routes/admin.py`
- Create: `Solex/solex/templates/admin/_layout.html`
- Create: `Solex/solex/templates/admin/dashboard.html`
- Modify: `Solex/solex/__init__.py` — register `admin.bp`

```python
# solex/routes/admin.py
from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import select, func
from solex.extensions import db
from solex.models import Order, Product, Subscription, ReturnRequest

bp = Blueprint("admin", __name__, url_prefix="/admin")

@bp.get("/")
@login_required
def dashboard():
    counts = {
        "orders_total": db.session.scalar(select(func.count()).select_from(Order)),
        "orders_pending": db.session.scalar(select(func.count()).where(Order.status == "pending")),
        "products_active": db.session.scalar(select(func.count()).where(Product.active == True)),
        "subs_active": db.session.scalar(select(func.count()).where(Subscription.status == "active")),
        "returns_pending": db.session.scalar(select(func.count()).where(ReturnRequest.status == "pending")),
    }
    return render_template("admin/dashboard.html", counts=counts)
```

**`admin/_layout.html`** — extends `base.html`, adds a sidebar with links to each admin surface.

```html
{% extends "base.html" %}
{% block main %}
<div class="flex gap-6">
  <aside class="w-56 shrink-0">
    <h3 class="font-semibold mb-3">Admin</h3>
    <nav class="space-y-1 text-sm">
      <a href="{{ url_for('admin.dashboard') }}" class="block">Dashboard</a>
      <a href="{{ url_for('admin_catalog.list_products') }}" class="block">Catalog</a>
      <a href="{{ url_for('admin_orders.list_orders') }}" class="block">Orders</a>
      <a href="{{ url_for('admin_inventory.list_inventory') }}" class="block">Inventory</a>
      <a href="{{ url_for('admin_customers.list_customers') }}" class="block">Customers</a>
      <a href="{{ url_for('admin_subscriptions.list_subs') }}" class="block">Subscriptions</a>
      <a href="{{ url_for('admin_returns.list_returns') }}" class="block">Returns</a>
      <a href="{{ url_for('admin_auth.logout') }}" class="block text-stone-500 mt-4">Sign out</a>
    </nav>
  </aside>
  <section class="flex-1">{% block admin_main %}{% endblock %}</section>
</div>
{% endblock %}
```

**`admin/dashboard.html`:**

```html
{% extends "admin/_layout.html" %}
{% block admin_main %}
<h1 class="text-2xl font-semibold mb-6">Dashboard</h1>
<div class="grid grid-cols-2 md:grid-cols-3 gap-4">
  {% for label, value in [
    ("Orders total", counts.orders_total),
    ("Orders pending", counts.orders_pending),
    ("Products active", counts.products_active),
    ("Subs active", counts.subs_active),
    ("Returns pending", counts.returns_pending),
  ] %}
  <div class="border rounded p-4">
    <div class="text-xs text-stone-500">{{ label }}</div>
    <div class="text-2xl font-semibold">{{ value or 0 }}</div>
  </div>
  {% endfor %}
</div>
{% endblock %}
```

Register in `create_app`: `app.register_blueprint(admin.bp)`. (Do NOT csrf.exempt — admin surfaces use forms.)

Unit test: admin unauthenticated → redirect to login. Logged-in → 200.

```python
# tests/unit/test_routes_admin.py
def test_dashboard_redirects_anonymous(client):
    resp = client.get("/admin/", follow_redirects=False)
    assert resp.status_code in (302, 401)

def test_dashboard_authenticated(client, db_session):
    from solex.models import AdminUser
    from solex.services.auth import AuthService
    u = AdminUser(email="dash@solex.local", active=True); db_session.add(u); db_session.flush()
    AuthService(db_session).set_admin_password(u, "pw")
    db_session.commit()
    client.post("/admin/login", data={"email": u.email, "password": "pw"})
    resp = client.get("/admin/")
    assert resp.status_code == 200
    assert b"Dashboard" in resp.data
```

- [ ] Commit: `solex(admin): dashboard + shared layout`.

### Task 5.2 — Admin catalog CRUD

**Files:**
- Create: `Solex/solex/routes/admin_catalog.py`
- Create: `Solex/solex/templates/admin/catalog/list.html`
- Create: `Solex/solex/templates/admin/catalog/form.html`
- Create: `Solex/tests/unit/test_admin_catalog.py`
- Modify: `Solex/solex/__init__.py`

Standard Flask-WTF forms. Only primary fields editable via UI (advanced fields stay under YAML importer's scope):

- Name, slug, sku, short_description, description, price_cents, active, category_id, weight_grams, image_path

```python
# solex/routes/admin_catalog.py
from flask import Blueprint, render_template, redirect, url_for, request, abort, flash
from flask_login import login_required
from sqlalchemy import select
from solex.extensions import db
from solex.models import Product, Category, Inventory

bp = Blueprint("admin_catalog", __name__, url_prefix="/admin/catalog")

@bp.get("/")
@login_required
def list_products():
    products = db.session.execute(select(Product).order_by(Product.name)).scalars().all()
    return render_template("admin/catalog/list.html", products=products)

@bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        p = _from_form(Product())
        db.session.add(p); db.session.flush()
        # ensure inventory row
        inv = Inventory(product_id=p.id, on_hand=int(request.form.get("starting_inventory", 0)))
        db.session.add(inv); db.session.commit()
        flash("Product created", "ok")
        return redirect(url_for("admin_catalog.edit", pid=p.id))
    return render_template("admin/catalog/form.html", product=None,
                           categories=db.session.query(Category).all())

@bp.route("/<uuid:pid>/edit", methods=["GET", "POST"])
@login_required
def edit(pid):
    p = db.session.get(Product, pid)
    if p is None: abort(404)
    if request.method == "POST":
        _from_form(p)
        db.session.commit()
        flash("Saved", "ok")
        return redirect(url_for("admin_catalog.edit", pid=p.id))
    return render_template("admin/catalog/form.html", product=p,
                           categories=db.session.query(Category).all())

@bp.post("/<uuid:pid>/deactivate")
@login_required
def deactivate(pid):
    p = db.session.get(Product, pid)
    if p is None: abort(404)
    p.active = False
    db.session.commit()
    return redirect(url_for("admin_catalog.list_products"))

def _from_form(p: Product) -> Product:
    p.name = request.form["name"]
    p.slug = request.form["slug"]
    p.sku = request.form["sku"]
    p.short_description = request.form.get("short_description", "")
    p.description = request.form.get("description", "")
    p.price_cents = int(request.form["price_cents"])
    p.image_path = request.form.get("image_path", "")
    p.active = bool(request.form.get("active"))
    p.weight_grams = int(request.form.get("weight_grams", 0))
    cid = request.form.get("category_id") or None
    p.category_id = cid
    return p
```

Templates: `list.html` renders the products table with "edit" and "deactivate" buttons. `form.html` renders fields + submit.

Register: `app.register_blueprint(admin_catalog.bp)`.

Test: POST create → product persists + inventory row. Edit → fields update. Deactivate → `active=False`.

- [ ] Commit: `solex(admin): catalog CRUD`.

---

## Chunk 6: Admin — orders + refunds + inventory

### Task 6.1 — Admin orders (list + detail + admin-initiated refund)

**Files:**
- Create: `Solex/solex/routes/admin_orders.py`
- Create: `Solex/solex/templates/admin/orders/list.html`
- Create: `Solex/solex/templates/admin/orders/detail.html`
- Create: `Solex/tests/unit/test_admin_orders.py`

Standard list + detail pages.

```python
# solex/routes/admin_orders.py
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from sqlalchemy import select
from solex.extensions import db
from solex.models import Order, Refund
from solex.services.refunds import RefundsService
from solex.services.square_client import SquareClient, SquareConfig
from solex.services.inventory import InventoryService
from flask import current_app

bp = Blueprint("admin_orders", __name__, url_prefix="/admin/orders")

def _refunds():
    c = current_app.config
    sq = SquareClient(SquareConfig(
        access_token=c["SQUARE_ACCESS_TOKEN"], environment=c["SQUARE_ENVIRONMENT"],
        location_id=c["SQUARE_LOCATION_ID"], webhook_signature_key=c["SQUARE_WEBHOOK_SIGNATURE_KEY"],
    ))
    return RefundsService(db.session, sq, InventoryService(db.session))

@bp.get("/")
@login_required
def list_orders():
    orders = db.session.execute(
        select(Order).order_by(Order.placed_at.desc()).limit(200)
    ).scalars().all()
    return render_template("admin/orders/list.html", orders=orders)

@bp.get("/<uuid:oid>")
@login_required
def detail(oid):
    order = db.session.get(Order, oid)
    if order is None: abort(404)
    return render_template("admin/orders/detail.html", order=order)

@bp.post("/<uuid:oid>/refund")
@login_required
def refund(oid):
    order = db.session.get(Order, oid)
    if order is None: abort(404)
    amount = int(request.form.get("amount_cents", order.total_cents))
    reason = request.form.get("reason", "admin-initiated")
    _refunds().issue_refund(order, amount, reason=reason)
    flash("Refunded", "ok")
    return redirect(url_for("admin_orders.detail", oid=order.id))
```

Templates show order lines, addresses, payment IDs, refund list, and a refund form.

- [ ] Commit: `solex(admin): orders — list + detail + admin-initiated refund`.

### Task 6.2 — Admin inventory (list + adjust)

**Files:**
- Create: `Solex/solex/routes/admin_inventory.py`
- Create: `Solex/solex/templates/admin/inventory/list.html`
- Create: `Solex/tests/unit/test_admin_inventory.py`

List shows product + on_hand + recent adjustments. Adjust form writes an `InventoryAdjustment` with admin_user_id + reason via `InventoryService.adjust`.

```python
# solex/routes/admin_inventory.py
from flask import Blueprint, render_template, redirect, url_for, request, abort, flash
from flask_login import login_required, current_user
from sqlalchemy import select
from solex.extensions import db
from solex.models import Product, Inventory, InventoryAdjustment
from solex.services.inventory import InventoryService

bp = Blueprint("admin_inventory", __name__, url_prefix="/admin/inventory")

@bp.get("/")
@login_required
def list_inventory():
    rows = db.session.execute(
        select(Product, Inventory).join(Inventory, Inventory.product_id == Product.id).order_by(Product.name)
    ).all()
    return render_template("admin/inventory/list.html", rows=rows)

@bp.post("/<uuid:pid>/adjust")
@login_required
def adjust(pid):
    delta = int(request.form["delta"])
    reason = request.form.get("reason", "correction")
    note = request.form.get("note", "")
    svc = InventoryService(db.session)
    svc.adjust(pid, delta, reason=reason, admin_user_id=current_user.id, note=note)
    db.session.commit()
    flash(f"Adjusted {delta:+d} ({reason})", "ok")
    return redirect(url_for("admin_inventory.list_inventory"))
```

Test: authenticated admin posts adjust, `on_hand` updates, adjustment row has `admin_user_id` populated.

- [ ] Commit: `solex(admin): inventory — list + adjust`.

---

## Chunk 7: Admin — customers + subscriptions + returns

### Task 7.1 — Admin customers (list)

**Files:**
- Create: `Solex/solex/routes/admin_customers.py`
- Create: `Solex/solex/templates/admin/customers/list.html`
- Test + commit: `solex(admin): customers list`.

Read-only list with email, order count, subscription count. Plan 3 extends; Plan 2 is just listing.

### Task 7.2 — Admin subscriptions (list + detail + force-pause/cancel)

**Files:**
- Create: `Solex/solex/routes/admin_subscriptions.py`
- Create: `Solex/solex/templates/admin/subscriptions/list.html`
- Create: `Solex/solex/templates/admin/subscriptions/detail.html`
- Test + commit: `solex(admin): subscriptions — list + detail + ops actions`.

Show status, next_charge_at, last_charged_at, recent charges. Admin can force-pause or cancel.

### Task 7.3 — Admin returns (list + approve/deny)

**Files:**
- Create: `Solex/solex/routes/admin_returns.py`
- Create: `Solex/solex/templates/admin/returns/list.html`
- Create: `Solex/solex/templates/admin/returns/detail.html`
- Test + commit: `solex(admin): returns — list + approve/deny`.

List pending returns. Detail shows order + lines. Approve calls `ReturnsService.approve`; deny prompts for reason.

---

## Chunk 8: Customer account — dashboard + orders + addresses

### Task 8.1 — Customer account dashboard

**Files:**
- Create: `Solex/solex/routes/account.py`
- Create: `Solex/solex/templates/account/_layout.html`
- Create: `Solex/solex/templates/account/dashboard.html`
- Test + commit: `solex(account): dashboard`.

Dashboard shows recent orders, active subscriptions, saved addresses at a glance. Uses `customer_login.unauthorized_handler` pattern (if not already wired — verify `login_view = "account_auth.login"`).

### Task 8.2 — Customer order history + detail

**Files:**
- Create: `Solex/solex/routes/account_orders.py`
- Create: `Solex/solex/templates/account/orders/list.html`
- Create: `Solex/solex/templates/account/orders/detail.html`
- Create: `Solex/solex/templates/account/orders/return_form.html`
- Test + commit: `solex(account): orders — history + detail + return form`.

Customer-scoped queries (`Order.customer_id == current_user.id`). Includes a "Request return" button that opens `return_form.html` and POSTs to account-side return endpoint.

### Task 8.3 — Customer addresses CRUD

**Files:**
- Create: `Solex/solex/routes/account_addresses.py`
- Create: `Solex/solex/templates/account/addresses.html`
- Test + commit: `solex(account): addresses CRUD`.

Standard address book: list, add, edit, delete.

---

## Chunk 9: Customer subscriptions + return request flow

### Task 9.1 — Customer subscription management

**Files:**
- Create: `Solex/solex/routes/account_subscriptions.py`
- Create: `Solex/solex/templates/account/subscriptions/list.html`
- Create: `Solex/solex/templates/account/subscriptions/detail.html`
- Test + commit: `solex(account): subscription view + cancel`.

**Per spec:** customer-facing pause/resume/skip is stubbed behind feature flag `SOLEX_FLAG_SUB_SELFSERVE` (default false). View + cancel are always available. The UI shows the flag-gated actions as disabled buttons with tooltip "contact support" when flag is off.

### Task 9.2 — Customer-initiated return request

**Files:**
- Modify: `Solex/solex/routes/account_orders.py` — add `POST /account/orders/<id>/return`
- Create: `Solex/tests/unit/test_account_returns.py`

```python
# account_orders.py — add:
@bp.post("/<uuid:oid>/return")
@login_required
def request_return(oid):
    order = db.session.get(Order, oid)
    if order is None or order.customer_id != current_user.id:
        abort(404)
    reason = request.form.get("reason", "").strip()
    if not reason:
        flash("Please describe the issue.", "error")
        return redirect(url_for("account_orders.detail", oid=order.id))
    from solex.services.returns import ReturnsService
    from solex.services.refunds import RefundsService
    from solex.services.square_client import SquareClient, SquareConfig
    from solex.services.inventory import InventoryService
    from flask import current_app
    c = current_app.config
    sq = SquareClient(SquareConfig(
        access_token=c["SQUARE_ACCESS_TOKEN"], environment=c["SQUARE_ENVIRONMENT"],
        location_id=c["SQUARE_LOCATION_ID"], webhook_signature_key=c["SQUARE_WEBHOOK_SIGNATURE_KEY"],
    ))
    ReturnsService(db.session, RefundsService(db.session, sq, InventoryService(db.session))).request(order, reason)
    flash("Return request submitted.", "ok")
    return redirect(url_for("account_orders.detail", oid=order.id))
```

Test: logged-in customer requests return, `ReturnRequest.status == 'pending'` persists.

- [ ] Commit: `solex(account): customer-initiated return request`.

### Task 9.3 — Product detail "Subscribe & save"

**Files:**
- Modify: `Solex/solex/templates/storefront/product_detail.html`
- Modify: `Solex/solex/routes/cart.py` — cart add accepts optional cadence (for Plan 2 the cart stays agnostic; subscription creation happens at checkout)
- Modify: `Solex/solex/routes/checkout.py` — if line has cadence + customer logged in + saved card, create a subscription via `SubscriptionService.create` after order completes
- Test + commit: `solex(subs): subscribe & save at checkout`.

> **Note**: the simplest path is: storefront line says `subscription_cadence_days` in the cart JSON; checkout reads it, after order creation (payment succeeded, card saved to Square Cards API via `save_card_on_file` if customer logged in), `SubscriptionService.create()` schedules the first charge at `now + cadence_days`. If not logged in, surface an inline "sign in first" message.

Full details in the implementer's task prompt — the spec's acceptance criterion is: 1-click "Subscribe every 30 days" on a product page creates a subscription after checkout, and the scheduler fires the second charge.

---

## Chunk 10: Jobs + scheduler bootstrap

### Task 10.1 — RQ-scheduler bootstrap + compose service

**Files:**
- Create: `Solex/solex/jobs/__init__.py`
- Create: `Solex/solex/jobs/scheduler.py`
- Create: `Solex/solex/jobs/subscriptions.py`
- Create: `Solex/solex/jobs/abandonment.py`
- Modify: `Solex/devops/docker-compose.yml` — add `scheduler` service
- Modify: `Solex/solex/cli.py` — add `scheduler run-local`

```python
# solex/jobs/scheduler.py
"""rq-scheduler bootstrap. Call from CLI or compose service."""
import logging
from datetime import datetime, timezone, timedelta
from redis import Redis
from rq_scheduler import Scheduler
from solex import create_app
from solex.config import resolve_config

log = logging.getLogger(__name__)

def build():
    cfg = resolve_config()
    conn = Redis.from_url(cfg.VALKEY_URL)
    return Scheduler(connection=conn, queue_name="solex-default")

def schedule_recurring_jobs():
    sched = build()
    # Clear prior entries with same IDs so restarts are idempotent
    for job in sched.get_jobs():
        if job.id.startswith("solex:"):
            sched.cancel(job)

    sched.cron(
        "*/15 * * * *", id="solex:charge_due_subscriptions",
        func="solex.jobs.subscriptions.charge_due_subscriptions",
    )
    sched.cron(
        "*/30 * * * *", id="solex:abandonment_sweep",
        func="solex.jobs.abandonment.run_abandonment_sweep",
    )
    log.info("scheduled recurring jobs")

def run_forever():
    schedule_recurring_jobs()
    import rq_scheduler
    sched = build()
    sched.run()
```

```python
# solex/jobs/subscriptions.py
def charge_due_subscriptions():
    from solex import create_app
    from solex.extensions import db
    from solex.services.subscriptions import SubscriptionService
    from solex.services.square_client import SquareClient, SquareConfig
    from solex.services.checkout import CheckoutService
    from solex.services.tax import FlatRateTaxStub
    from solex.services.shipping import FlatRateShippingStub
    from solex.services.inventory import InventoryService
    app = create_app()
    with app.app_context():
        cfg = app.config
        sq = SquareClient(SquareConfig(
            access_token=cfg["SQUARE_ACCESS_TOKEN"], environment=cfg["SQUARE_ENVIRONMENT"],
            location_id=cfg["SQUARE_LOCATION_ID"], webhook_signature_key=cfg["SQUARE_WEBHOOK_SIGNATURE_KEY"],
        ))
        co = CheckoutService(
            session=db.session, square=sq,
            tax=FlatRateTaxStub(cfg["TAX_RATE_PCT"]),
            shipping=FlatRateShippingStub(cfg["SHIPPING_FLAT_CENTS"], cfg["SHIPPING_FREE_THRESHOLD_CENTS"]),
            inventory=InventoryService(db.session),
        )
        summary = SubscriptionService(db.session, sq, co).charge_due_subscriptions()
        import logging; logging.getLogger(__name__).info(f"subscriptions summary={summary}")
```

```python
# solex/jobs/abandonment.py
def run_abandonment_sweep():
    from solex import create_app
    from solex.extensions import db
    from solex.services.abandonment import AbandonmentService
    app = create_app()
    with app.app_context():
        summary = AbandonmentService(db.session).sweep()
        import logging; logging.getLogger(__name__).info(f"abandonment summary={summary}")
```

**docker-compose additions:**

```yaml
  scheduler:
    image: solex-worker
    container_name: solex_scheduler
    build:
      context: ..
      dockerfile: devops/Dockerfile
    command: ["python3", "-m", "solex.cli", "scheduler", "run"]
    env_file: ../.env
    volumes: [...]  # same as worker
    networks: [growdirect]
```

**CLI:**

```python
# solex/cli.py
@cli.group()
def scheduler(): ...

@scheduler.command("run")
def run():
    from solex.jobs.scheduler import run_forever
    run_forever()

@scheduler.command("schedule-once")
def schedule_once():
    from solex.jobs.scheduler import schedule_recurring_jobs
    schedule_recurring_jobs()
```

Tests: unit-test `schedule_recurring_jobs` with a mocked `Scheduler` (assert cron entries registered).

- [ ] Commit: `solex(jobs): rq-scheduler bootstrap + autoship + abandonment cron`.

---

## Chunk 11: Integration + sandbox-live subscription + final smoke + PR

### Task 11.1 — Sandbox-live subscription test

**Files:**
- Create: `Solex/tests/integration/test_subscriptions_sandbox.py`

```python
@pytest.mark.sandbox_live
def test_autoship_cycle_against_sandbox(app, db_session, sandbox_config):
    """Full cycle: save card via sandbox, create subscription due now, run
    charge_due_subscriptions, assert an Order + SubscriptionCharge landed."""
    # 1. Create a Square sandbox customer
    # 2. Tokenize a test card (cnon:card-nonce-ok) via the Cards sandbox
    # 3. Save card-on-file
    # 4. Create Customer + Subscription in local DB with saved card
    # 5. Run SubscriptionService.charge_due_subscriptions(now=<past>)
    # 6. Assert: Order created, SubscriptionCharge.succeeded=True, next_charge_at moved forward
    # Cleanup: issue a refund for the Square payment
```

Implement with the actual squareup v44 API shape you discovered in Plan 1 (see `solex/services/square_client.py`).

- [ ] Commit: `solex(tests): sandbox-live subscription charge cycle`.

### Task 11.2 — Final test matrix

```bash
cd ~/GrowDirect/Solex
./devops/scripts/dev.sh up
docker compose -f devops/docker-compose.yml run --rm -e SOLEX_ENV=testing web pytest tests/unit tests/integration -m "not sandbox_live" -v
docker compose -f devops/docker-compose.yml run --rm -e SOLEX_ENV=testing web pytest -m sandbox_live -v
./devops/scripts/dev.sh down
```

Expect: all green. Target ~130+ tests.

### Task 11.3 — Open PR

Title: `feat: solex operations — admin UI, autoship, returns, search, abandonment`
Body: summarize Plan 2 scope, list in/out, note dependencies on Plan 1 branch, list known issues / manual verification checklist.

---

## Plan 2 — Done criteria (repeat)

- [ ] Admin can do end-to-end: log in → dashboard → edit a product → process an order refund → approve a return → view a subscription
- [ ] Customer can: magic-link login → see order history → request a return → manage addresses → view + cancel subscription
- [ ] Subscribing to a product via checkout creates a live `Subscription`; rq-scheduler cron charges it on cadence; Canary sees the autoship Order
- [ ] `docker compose exec web python3 -m solex.cli scheduler schedule-once` installs both cron entries; `rq info` shows them queued
- [ ] Guest cart left idle receives an abandonment email (MailHog verification)
- [ ] `/search?q=red+light` finds the red-light belt product
- [ ] `SOLEX_FLAG_SYNC_CATALOG_TO_SQUARE=true` + `catalog sync-to-square` creates Square Catalog entries
- [ ] `pytest` full matrix green
- [ ] No regression in Plan 1 flows
- [ ] PR opened, reviewed, merged

---

## What's next (for context, not execution)

- **Plan 3 — Scenario runner:** `/admin/lab` + 9 scenarios (normal day, after-hours, round-amount, high-value, autoship cohort, bulk reseller, refund wave, shrink event, cart abandonment). Requires Plan 1+2 services — specifically `SubscriptionService` and `ReturnsService` for the subscription/refund-wave scenarios.
- **Plan 4 — Visual fidelity:** Tailwind theme matching solexglobal.com, hero sections, real imagery, full 25-SKU catalog.
