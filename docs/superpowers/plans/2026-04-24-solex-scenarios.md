# Solex Scenario Runner Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Land `/admin/lab` — an admin-triggered scenario runner that produces cohorts of realistic transactions, refunds, inventory adjustments, subscriptions, and abandoned carts through the real Plan 1/Plan 2 service paths. Each scenario is a named, param-configurable class that declares the Canary chirp rules it exercises. Nine scenarios ship.

**Architecture:** New `ScenarioRun` model + migration 0004 tracks each run. Scenarios live in `solex/services/scenarios/` — a base `Scenario` ABC defines the shape (`name`, `description`, `params_schema`, `run`, `expected_chirps`), a `registry` module auto-discovers subclasses, and each of the 9 scenarios is a focused subclass. Each scenario drives the real `CheckoutService` / `RefundsService` / `SubscriptionService` / `InventoryService` / `Cart` paths — nothing in the Square/DB flow is bypassed, every order is tagged with `scenario_tag` for traceability. Sync execution for small runs (≤5 items); RQ job for larger batches.

**Tech Stack:** Same as Plans 1+2. Python 3.12, Flask 3, SQLAlchemy 2.0, Postgres 17, Valkey 8, RQ, pydantic. New dependency on `pydantic` (already in requirements.txt).

---

## Scope

**This is Plan 3 of 4.** Depends on Plan 1 + Plan 2 code being present.

**In scope:**
- `ScenarioRun` model + Alembic migration 0004
- `Scenario` ABC + `params_schema: pydantic.BaseModel` + `expected_chirps` declaration
- Registry: `solex.services.scenarios.registry` — name → class mapping, auto-discovered
- 9 scenarios:
  1. `normal_retail_day` — 20–40 small-basket purchases across business hours (baseline)
  2. `after_hours_burst` — 5–15 orders at 22:00–02:00 (C-002 AFTER_HOURS)
  3. `round_amount_cluster` — 6–10 orders whose totals end in $0.00 (C-003 ROUND_AMOUNT)
  4. `high_value_sale` — 1–3 orders ≥ $500 (C-001 HIGH_VALUE)
  5. `autoship_cohort` — 15–30 autoship orders via `SubscriptionService.charge_due_subscriptions`
  6. `bulk_reseller_order` — 1–2 orders with 10–30 line items (volume anomaly / MLM flavor)
  7. `refund_wave` — refunds against a cohort of prior orders
  8. `shrink_event` — inventory adjustments with `reason='shrink'`, no offsetting orders (GRO-297)
  9. `cart_abandonment_cohort` — creates and abandons carts at various funnel stages
- `/admin/lab` UI: list scenarios, per-scenario param form, run-detail live summary
- RQ job entrypoint for large scenario runs
- CLI: `python3 -m solex.cli scenarios run <name> [--params-json '{...}']`
- Sandbox-live integration test: run `high_value_sale(count=1)` against real Square sandbox, cleanup

**Out of scope (later plans):**
- Visual fidelity pass matching solexglobal.com (Plan 4)
- Full 25-SKU catalog curation with real imagery (Plan 4)
- Canary read-side integration that verifies which chirps actually fired (post-MVP; see spec §4.9 stub note — for Plan 3 we surface `expected_chirps` declaratively only)
- Multi-merchant / multi-tenant (not planned)

**Definition of done for Plan 3:**
1. `/admin/lab` lists 9 scenarios with name/description/expected-chirps.
2. Clicking a scenario shows a param form; submit creates a `ScenarioRun` row, runs the scenario (sync or RQ), persists `summary_json` with counts + created order IDs.
3. Run-detail page shows status, summary, and links to the created `Order`s (filterable by `scenario_tag`).
4. Admin Orders list (`/admin/orders`) gains an optional `?scenario_tag=<tag>` filter.
5. `pytest tests/unit tests/integration -m "not sandbox_live"` green (should be ~240+ tests).
6. `pytest -m sandbox_live` green (Plan 1 checkout + Plan 2 subscription + Plan 3 high-value scenario).
7. No regression in Plans 1/2 flows.

---

## Prerequisites

- [ ] Plan 2 branch (`plan/solex-operations`) merged or available as the base. This plan's branch `plan/solex-scenarios` branches from there.
- [ ] Shared infra running.
- [ ] Solex stack runnable: `cd ~/GrowDirect/Solex && ./devops/scripts/dev.sh up`.
- [ ] Square sandbox credentials in `Solex/.env`.
- [ ] Linear: file as sub-issue under GRO-521. Reference `Refs GRO-XXX. Plan 3 task N.M.` in commits.

Useful skills:
- @superpowers:test-driven-development
- @superpowers:systematic-debugging
- @superpowers:verification-before-completion

---

## File Structure

### New model

```
Solex/solex/models/
└── scenarios.py            ScenarioRun
```

### New services

```
Solex/solex/services/scenarios/
├── __init__.py             re-exports + registry
├── base.py                 Scenario ABC, SynthesizedCustomer, shared helpers
├── registry.py             name → class map + register() decorator
├── synth.py                fake-data helpers (names, emails, addresses, timestamps)
├── normal_retail_day.py
├── after_hours_burst.py
├── round_amount_cluster.py
├── high_value_sale.py
├── autoship_cohort.py
├── bulk_reseller_order.py
├── refund_wave.py
├── shrink_event.py
└── cart_abandonment_cohort.py
```

### New blueprint

```
Solex/solex/routes/
└── lab.py                  /admin/lab — list + run form + run detail
```

### New templates

```
Solex/solex/templates/admin/lab/
├── list.html
├── run_form.html
└── run_detail.html
```

### New jobs

```
Solex/solex/jobs/
└── scenarios.py            RQ entry: execute_scenario_run(run_id)
```

### Modified files

- `Solex/solex/routes/admin_orders.py` — add `?scenario_tag=<tag>` filter to `list_orders`
- `Solex/solex/templates/admin/orders/list.html` — render scenario_tag column
- `Solex/solex/templates/admin/_layout.html` — add "Lab" sidebar link
- `Solex/solex/cli.py` — add `scenarios run` + `scenarios list`
- `Solex/solex/__init__.py` — register `lab.bp`
- `Solex/solex/models/__init__.py` — export `ScenarioRun`

---

## Chunk 1: ScenarioRun model + base Scenario + registry

### Task 1.1 — `ScenarioRun` model + migration 0004

**Files:**
- Create: `Solex/solex/models/scenarios.py`
- Create: `Solex/tests/unit/test_models_scenario_run.py`
- Modify: `Solex/solex/models/__init__.py`
- Create: `Solex/alembic/versions/0004_scenario_runs.py`

- [ ] **Step 1: Write failing test**

```python
# tests/unit/test_models_scenario_run.py
from datetime import datetime, timezone
from solex.models.scenarios import ScenarioRun

def test_scenario_run_fields():
    r = ScenarioRun(
        scenario_name="normal_retail_day",
        params_json={"count": 10},
        started_at=datetime.now(timezone.utc),
        status="pending",
        summary_json={},
    )
    assert r.scenario_name == "normal_retail_day"
    assert r.status == "pending"
```

- [ ] **Step 2: Verify RED.** Run `pytest tests/unit/test_models_scenario_run.py -v`. Expect ImportError.

- [ ] **Step 3: Write the model**

```python
# solex/models/scenarios.py
import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from solex.models.base import BaseModel

SCENARIO_RUN_STATUSES = ("pending", "running", "succeeded", "failed", "partial")

class ScenarioRun(BaseModel):
    __tablename__ = "scenario_runs"
    scenario_name: Mapped[str] = mapped_column(String(80), nullable=False)
    params_json: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    admin_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("admin_users.id", ondelete="SET NULL"), nullable=True,
    )
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    summary_json: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    __table_args__ = (
        Index("ix_scenario_runs_name", "scenario_name"),
        Index("ix_scenario_runs_status", "status"),
    )
```

Add to `solex/models/__init__.py`:

```python
from solex.models.scenarios import ScenarioRun, SCENARIO_RUN_STATUSES
```

and `__all__`: `"ScenarioRun", "SCENARIO_RUN_STATUSES"`.

- [ ] **Step 4: Run test GREEN.**

- [ ] **Step 5: Generate migration 0004**

```bash
docker compose -f devops/docker-compose.yml run --rm web \
  alembic revision --autogenerate -m "scenario runs"
```

Rename to `Solex/alembic/versions/0004_scenario_runs.py`. Verify:
- `scenario_runs` table present
- `admin_user_id` FK to `admin_users` with `ondelete='SET NULL'`
- Indexes on `scenario_name` and `status`
- `down_revision` matches the previous migration's revision ID

- [ ] **Step 6: Upgrade both DBs**

```bash
docker compose -f devops/docker-compose.yml run --rm web alembic upgrade head
docker compose -f devops/docker-compose.yml run --rm -e SOLEX_ENV=testing web alembic upgrade head
```

- [ ] **Step 7: Commit**

```bash
cd ~/GrowDirect
git add Solex/
git commit -m "solex(models): ScenarioRun + migration 0004

Refs GRO-XXX. Plan 3 task 1.1."
```

### Task 1.2 — Scenario ABC + registry + synth helpers

**Files:**
- Create: `Solex/solex/services/scenarios/__init__.py`
- Create: `Solex/solex/services/scenarios/base.py`
- Create: `Solex/solex/services/scenarios/registry.py`
- Create: `Solex/solex/services/scenarios/synth.py`
- Create: `Solex/tests/unit/test_services_scenarios_base.py`

- [ ] **Step 1: Write the synth helpers** (deterministic given a seed for test stability):

```python
# solex/services/scenarios/synth.py
"""Fake-data generators for scenario cohorts. Deterministic given a seed."""
import random
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass

@dataclass(frozen=True)
class SynthCustomer:
    first_name: str
    last_name: str
    email: str

@dataclass(frozen=True)
class SynthAddress:
    line1: str
    city: str
    region: str
    postal_code: str

_FIRST_NAMES = ("Maya", "Chen", "Priya", "Alex", "Sam", "Jordan", "Taylor",
                "Riley", "Casey", "Morgan", "Avery", "Emerson", "Sage", "Rowan")
_LAST_NAMES = ("Park", "Rivera", "Kim", "Patel", "Nguyen", "Singh", "Hernandez",
               "Ochoa", "Brooks", "Wells", "Vogel", "Tran", "Cole", "Hart")
_CITIES = (("Torrance", "CA", "90503"), ("Redondo Beach", "CA", "90277"),
           ("Palos Verdes Estates", "CA", "90274"), ("San Pedro", "CA", "90731"),
           ("Rolling Hills", "CA", "90274"), ("Manhattan Beach", "CA", "90266"),
           ("Long Beach", "CA", "90802"), ("Carson", "CA", "90745"))

def synth_customer(rng: random.Random, run_tag: str, i: int) -> SynthCustomer:
    first = rng.choice(_FIRST_NAMES)
    last = rng.choice(_LAST_NAMES)
    # Include run_tag + i in email for traceability + uniqueness across runs
    email = f"{first.lower()}.{last.lower()}.{run_tag}.{i}@solex.local"
    return SynthCustomer(first_name=first, last_name=last, email=email)

def synth_address(rng: random.Random) -> SynthAddress:
    num = rng.randint(100, 9999)
    street = rng.choice(("Main St", "Ocean Ave", "Palos Verdes Dr", "Crest Rd",
                         "Hawthorne Blvd", "Torrance Blvd", "Anza Ave"))
    city, region, zip5 = rng.choice(_CITIES)
    return SynthAddress(line1=f"{num} {street}", city=city, region=region, postal_code=zip5)

def pick_time_in_window(rng: random.Random, start_hour: int, end_hour: int,
                        *, base: datetime | None = None) -> datetime:
    """Pick a datetime in today's [start_hour, end_hour) window. end_hour may wrap past midnight
    (e.g., start=22, end=2 means 22:00 of `base` through 02:00 of `base + 1 day`)."""
    base = (base or datetime.now(timezone.utc)).replace(
        hour=0, minute=0, second=0, microsecond=0)
    if end_hour <= start_hour:
        total_minutes = (24 - start_hour + end_hour) * 60
    else:
        total_minutes = (end_hour - start_hour) * 60
    offset = rng.randint(0, total_minutes - 1)
    return base + timedelta(hours=start_hour, minutes=offset)
```

- [ ] **Step 2: Registry**

```python
# solex/services/scenarios/registry.py
from typing import Type

_registry: dict[str, Type] = {}

def register(cls):
    """Class decorator to register a Scenario subclass."""
    name = getattr(cls, "name", None)
    if not name:
        raise ValueError(f"{cls.__name__} has no `name` class attribute")
    if name in _registry:
        raise ValueError(f"scenario name collision: {name}")
    _registry[name] = cls
    return cls

def get(name: str):
    return _registry.get(name)

def all_scenarios():
    return dict(_registry)

def _import_all():
    """Force-import each scenario module so decorators fire."""
    from solex.services.scenarios import (  # noqa: F401
        normal_retail_day, after_hours_burst, round_amount_cluster,
        high_value_sale, autoship_cohort, bulk_reseller_order,
        refund_wave, shrink_event, cart_abandonment_cohort,
    )
```

- [ ] **Step 3: Base Scenario ABC**

```python
# solex/services/scenarios/base.py
import random
import secrets
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import ClassVar, Type

from pydantic import BaseModel
from sqlalchemy.orm import Session

from solex.models import Product, ScenarioRun
from solex.services.scenarios.synth import SynthCustomer, SynthAddress

class ScenarioParams(BaseModel):
    """Base params. Override per-scenario."""
    count: int = 10
    seed: int | None = None  # for deterministic runs

@dataclass(frozen=True)
class ScenarioContext:
    """Everything a scenario's run() gets, so it doesn't need its own factory."""
    session: Session
    run: ScenarioRun
    rng: random.Random
    tag: str  # e.g., "after_hours_burst-<run_id_short>"
    config: dict  # Flask config for SquareClient etc.

class Scenario(ABC):
    name: ClassVar[str]
    description: ClassVar[str] = ""
    params_schema: ClassVar[Type[ScenarioParams]] = ScenarioParams

    @classmethod
    def build_tag(cls, run: ScenarioRun) -> str:
        return f"{cls.name}-{str(run.id)[:8]}"

    @classmethod
    def expected_chirps(cls, params: ScenarioParams) -> list[str]:
        """Declared chirp rules this scenario is designed to trigger.
        Subclasses override. Default: empty."""
        return []

    @abstractmethod
    def run(self, ctx: ScenarioContext, params: ScenarioParams) -> dict:
        """Execute the scenario; return a summary dict that gets persisted
        to ScenarioRun.summary_json."""
        ...

def prepare_context(session: Session, run: ScenarioRun, config: dict) -> ScenarioContext:
    params = run.params_json or {}
    seed = params.get("seed") or secrets.randbits(32)
    rng = random.Random(seed)
    # Record the seed back in params_json for reproducibility
    if not params.get("seed"):
        merged = dict(params); merged["seed"] = seed
        run.params_json = merged
    tag = f"{run.scenario_name}-{str(run.id)[:8]}"
    return ScenarioContext(session=session, run=run, rng=rng, tag=tag, config=config)
```

- [ ] **Step 4: __init__ exports**

```python
# solex/services/scenarios/__init__.py
from solex.services.scenarios.base import (
    Scenario, ScenarioParams, ScenarioContext, prepare_context,
)
from solex.services.scenarios.registry import register, get, all_scenarios, _import_all

__all__ = [
    "Scenario", "ScenarioParams", "ScenarioContext", "prepare_context",
    "register", "get", "all_scenarios", "_import_all",
]
```

- [ ] **Step 5: Tests**

```python
# tests/unit/test_services_scenarios_base.py
import pytest
from unittest.mock import MagicMock
from solex.services.scenarios.base import Scenario, ScenarioParams, prepare_context
from solex.services.scenarios import registry
from solex.models import ScenarioRun
from datetime import datetime, timezone

def test_register_requires_name():
    class Bogus(Scenario):
        def run(self, ctx, params): return {}
    with pytest.raises(ValueError):
        registry.register(Bogus)

def test_register_rejects_duplicates(monkeypatch):
    monkeypatch.setattr(registry, "_registry", {})
    class A(Scenario):
        name = "same"
        def run(self, ctx, params): return {}
    class B(Scenario):
        name = "same"
        def run(self, ctx, params): return {}
    registry.register(A)
    with pytest.raises(ValueError):
        registry.register(B)

def test_prepare_context_records_seed(app, db_session):
    run = ScenarioRun(
        scenario_name="x", params_json={"count": 3},
        started_at=datetime.now(timezone.utc), status="pending", summary_json={},
    )
    db_session.add(run); db_session.flush()
    ctx = prepare_context(db_session, run, config={})
    assert ctx.run.params_json.get("seed") is not None
    assert ctx.rng is not None
    assert ctx.tag.startswith("x-")
```

- [ ] **Step 6: Run tests GREEN.**

- [ ] **Step 7: Commit**

```bash
git add Solex/solex/services/scenarios/ Solex/tests/unit/test_services_scenarios_base.py
git commit -m "solex(scenarios): Scenario ABC + registry + synth helpers

Refs GRO-XXX. Plan 3 task 1.2."
```

---

## Chunk 2: 5 order-emitting scenarios

All five follow the same shape: pick N synthetic customers, build a cart, call `CheckoutService.place_order` with `scenario_tag=ctx.tag` and `placed_at=<synthesized>`. A shared helper makes each subclass small.

### Task 2.1 — Shared `emit_order` helper

**Files:**
- Modify: `Solex/solex/services/scenarios/base.py` — add helper
- Modify: `Solex/solex/services/checkout.py` — verify `scenario_tag` and `placed_at` are honored

`CheckoutService.place_order` already accepts `scenario_tag` and `placed_at` kwargs per Plan 1. Verify the signature. If missing either, surface as a concern — it's required for scenarios.

- [ ] **Step 1: Add helper to `base.py`**

```python
# append to solex/services/scenarios/base.py

from datetime import datetime
from typing import Sequence
from solex.services.checkout import CheckoutService, CartLineIn, CustomerIn
from solex.services.square_client import SquareClient, SquareConfig
from solex.services.inventory import InventoryService
from solex.services.tax import FlatRateTaxStub
from solex.services.shipping import FlatRateShippingStub
from solex.services.scenarios.synth import (
    SynthCustomer, SynthAddress, synth_customer, synth_address,
)
from solex.models import Order, Product

def _square(config: dict) -> SquareClient:
    return SquareClient(SquareConfig(
        access_token=config["SQUARE_ACCESS_TOKEN"],
        environment=config["SQUARE_ENVIRONMENT"],
        location_id=config["SQUARE_LOCATION_ID"],
        webhook_signature_key=config.get("SQUARE_WEBHOOK_SIGNATURE_KEY", ""),
    ))

def _checkout_service(ctx: ScenarioContext) -> CheckoutService:
    return CheckoutService(
        session=ctx.session,
        square=_square(ctx.config),
        tax=FlatRateTaxStub(rate_pct=ctx.config.get("TAX_RATE_PCT", 0.0)),
        shipping=FlatRateShippingStub(
            flat_cents=ctx.config.get("SHIPPING_FLAT_CENTS", 695),
            free_threshold_cents=ctx.config.get("SHIPPING_FREE_THRESHOLD_CENTS", 9900),
        ),
        inventory=InventoryService(ctx.session),
    )

def emit_order(
    ctx: ScenarioContext,
    *,
    products_and_qty: Sequence[tuple[Product, int]],
    placed_at: datetime,
    customer_index: int,
    payment_token: str = "cnon:card-nonce-ok",
) -> Order:
    """Drive a single order through CheckoutService with synth customer + address.
    Returns the persisted Order. Tags it with ctx.tag."""
    cust = synth_customer(ctx.rng, str(ctx.run.id)[:8], customer_index)
    addr = synth_address(ctx.rng)
    lines = [
        CartLineIn(
            product_id=p.id, qty=qty, price_cents=p.price_cents,
            name=p.name, sku=p.sku, image_path=p.image_path or "",
        )
        for p, qty in products_and_qty
    ]
    shipping_addr = {
        "first_name": cust.first_name, "last_name": cust.last_name,
        "line1": addr.line1, "city": addr.city, "region": addr.region,
        "postal_code": addr.postal_code, "country": "US",
    }
    svc = _checkout_service(ctx)
    order = svc.place_order(
        cart_lines=lines,
        customer=CustomerIn(email=cust.email, name=f"{cust.first_name} {cust.last_name}"),
        shipping_addr=shipping_addr,
        billing_addr=shipping_addr,
        payment_token=payment_token,
        scenario_tag=ctx.tag,
        placed_at=placed_at,
    )
    return order
```

- [ ] **Step 2: Verify CheckoutService accepts `scenario_tag` and `placed_at`** — read `solex/services/checkout.py`. If either arg is missing, add them to the signature + forward to the `Order(...)` construction. This is a Plan 1 bug fix if so; commit separately with message `solex(checkout): honor scenario_tag + placed_at kwargs`.

- [ ] **Step 3: Commit**

```bash
git add Solex/
git commit -m "solex(scenarios): emit_order helper — shared checkout driver

Refs GRO-XXX. Plan 3 task 2.1."
```

### Task 2.2 — `normal_retail_day` scenario

**Files:**
- Create: `Solex/solex/services/scenarios/normal_retail_day.py`
- Create: `Solex/tests/integration/test_scenario_normal_retail_day.py`

- [ ] **Step 1: Scenario**

```python
# solex/services/scenarios/normal_retail_day.py
from datetime import timedelta
from sqlalchemy import select
from solex.services.scenarios.base import (
    Scenario, ScenarioParams, ScenarioContext, emit_order,
)
from solex.services.scenarios.synth import pick_time_in_window
from solex.services.scenarios.registry import register
from solex.models import Product

class Params(ScenarioParams):
    count: int = 25
    window_start_hour: int = 9
    window_end_hour: int = 19
    basket_min: int = 1
    basket_max: int = 3

@register
class NormalRetailDay(Scenario):
    name = "normal_retail_day"
    description = "Baseline small-basket retail purchases across business hours. No chirps expected."
    params_schema = Params

    @classmethod
    def expected_chirps(cls, params):
        return []

    def run(self, ctx: ScenarioContext, params: Params) -> dict:
        products = ctx.session.execute(
            select(Product).where(Product.active == True)
        ).scalars().all()
        if not products:
            return {"error": "no active products"}
        created = []
        failed = []
        for i in range(params.count):
            try:
                basket_size = ctx.rng.randint(params.basket_min, params.basket_max)
                items = [(ctx.rng.choice(products), 1) for _ in range(basket_size)]
                when = pick_time_in_window(
                    ctx.rng, params.window_start_hour, params.window_end_hour
                )
                order = emit_order(
                    ctx, products_and_qty=items, placed_at=when, customer_index=i,
                )
                created.append(str(order.id))
            except Exception as e:
                failed.append({"i": i, "error": type(e).__name__, "detail": str(e)[:200]})
        return {"created": created, "failed": failed, "attempted": params.count}
```

- [ ] **Step 2: Integration test (Square mocked, real DB)**

```python
# tests/integration/test_scenario_normal_retail_day.py
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from pathlib import Path
from solex.services.scenarios import prepare_context, registry
from solex.services.catalog_import import CatalogImporter
from solex.models import ScenarioRun, Order

def _prep_catalog(db_session, tmp_path):
    (tmp_path / "catalog").mkdir(exist_ok=True)
    CatalogImporter(db_session, Path("catalog"), tmp_path).import_from_yaml(
        Path("catalog/products.yaml"))
    db_session.expire_all()

def _mock_square(mocker):
    sq = MagicMock()
    # SquareClient.create_order + create_payment both return minimal dicts
    counter = {"n": 0}
    def _mk_order(*a, **kw):
        counter["n"] += 1
        return {"id": f"sq_order_{counter['n']}"}
    def _mk_payment(*a, **kw):
        return {"id": f"sq_pay_{counter['n']}"}
    mocker.patch(
        "solex.services.scenarios.base._square",
        return_value=MagicMock(
            create_order=MagicMock(side_effect=_mk_order),
            create_payment=MagicMock(side_effect=_mk_payment),
        ),
    )

def test_normal_retail_day_runs_and_tags(app, db_session, tmp_path, mocker):
    registry._import_all()
    _prep_catalog(db_session, tmp_path)
    _mock_square(mocker)

    run = ScenarioRun(
        scenario_name="normal_retail_day",
        params_json={"count": 5, "seed": 42},
        started_at=datetime.now(timezone.utc), status="running", summary_json={},
    )
    db_session.add(run); db_session.flush()

    ctx = prepare_context(db_session, run, config={
        "SQUARE_ACCESS_TOKEN": "x", "SQUARE_ENVIRONMENT": "sandbox",
        "SQUARE_LOCATION_ID": "L", "SQUARE_WEBHOOK_SIGNATURE_KEY": "",
        "TAX_RATE_PCT": 0.0, "SHIPPING_FLAT_CENTS": 0,
        "SHIPPING_FREE_THRESHOLD_CENTS": 9999999,
    })
    scenario = registry.get("normal_retail_day")()
    summary = scenario.run(ctx, scenario.params_schema(count=5, seed=42))
    assert summary["attempted"] == 5
    assert len(summary["created"]) == 5
    assert not summary["failed"]

    tag = ctx.tag
    orders = db_session.query(Order).filter_by(scenario_tag=tag).all()
    assert len(orders) == 5
    # Each order belongs to the same scenario run
    assert all(o.scenario_tag == tag for o in orders)
```

- [ ] **Step 3: Run tests GREEN.**

- [ ] **Step 4: Commit**

```bash
git add Solex/
git commit -m "solex(scenarios): normal_retail_day

Refs GRO-XXX. Plan 3 task 2.2."
```

### Task 2.3 — `after_hours_burst`

**File:** `Solex/solex/services/scenarios/after_hours_burst.py` + test

```python
# solex/services/scenarios/after_hours_burst.py
from sqlalchemy import select
from solex.services.scenarios.base import (
    Scenario, ScenarioParams, ScenarioContext, emit_order,
)
from solex.services.scenarios.synth import pick_time_in_window
from solex.services.scenarios.registry import register
from solex.models import Product

class Params(ScenarioParams):
    count: int = 10
    window_start_hour: int = 22
    window_end_hour: int = 2  # wraps midnight

@register
class AfterHoursBurst(Scenario):
    name = "after_hours_burst"
    description = "Small cohort of orders between 22:00 and 02:00."
    params_schema = Params

    @classmethod
    def expected_chirps(cls, params):
        return ["C-002 AFTER_HOURS"]

    def run(self, ctx: ScenarioContext, params: Params) -> dict:
        products = ctx.session.execute(
            select(Product).where(Product.active == True)
        ).scalars().all()
        created, failed = [], []
        for i in range(params.count):
            try:
                when = pick_time_in_window(ctx.rng, params.window_start_hour,
                                           params.window_end_hour)
                product = ctx.rng.choice(products)
                order = emit_order(ctx, products_and_qty=[(product, 1)],
                                   placed_at=when, customer_index=i)
                created.append(str(order.id))
            except Exception as e:
                failed.append({"i": i, "error": str(e)[:200]})
        return {"attempted": params.count, "created": created, "failed": failed}
```

Test: same pattern as Task 2.2 — assert all orders have `placed_at` in the 22–02 window.

Commit: `solex(scenarios): after_hours_burst`.

### Task 2.4 — `round_amount_cluster`

**File:** `Solex/solex/services/scenarios/round_amount_cluster.py` + test

Compute per-order qty so that `qty * price_cents + shipping + tax` ends in $0.00. Simplest: pick a product, then solve for qty such that `(qty * price_cents) % 100 == (-shipping_cents - tax_cents) % 100`. For the stub tax/shipping (rate 0, flat 695 under $99 / 0 above), with rate=0 tax=0 and subtotal-based free shipping — pick products with even-dollar prices or calculate.

Implementation — pick a product with `price_cents % 100 == 0`, then any qty works:

```python
# solex/services/scenarios/round_amount_cluster.py
from sqlalchemy import select
from solex.services.scenarios.base import (
    Scenario, ScenarioParams, ScenarioContext, emit_order, _checkout_service,
)
from solex.services.scenarios.synth import pick_time_in_window
from solex.services.scenarios.registry import register
from solex.models import Product

class Params(ScenarioParams):
    count: int = 8

@register
class RoundAmountCluster(Scenario):
    name = "round_amount_cluster"
    description = "Orders whose totals end in $0.00 — suspicious round-dollar clustering."
    params_schema = Params

    @classmethod
    def expected_chirps(cls, params):
        return ["C-003 ROUND_AMOUNT"]

    def run(self, ctx: ScenarioContext, params: Params) -> dict:
        # pick products whose price + flat-rate shipping lands on round dollars
        # easiest: buy enough that subtotal >= free-shipping threshold (shipping=0),
        # then qty * price_cents must itself be % 100 == 0
        round_products = ctx.session.execute(
            select(Product).where(
                Product.active == True, Product.price_cents % 100 == 0
            )
        ).scalars().all()
        if not round_products:
            # fallback: any product, use qty to force round amount (not always possible
            # with flat shipping — try qty=100 to overshoot threshold so shipping=0)
            round_products = ctx.session.execute(
                select(Product).where(Product.active == True)
            ).scalars().all()

        created, failed = [], []
        free_ship = ctx.config.get("SHIPPING_FREE_THRESHOLD_CENTS", 9900)
        for i in range(params.count):
            try:
                product = ctx.rng.choice(round_products)
                # min qty to clear free-ship threshold
                min_qty = max(1, (free_ship // product.price_cents) + 1)
                qty = min_qty
                when = pick_time_in_window(ctx.rng, 10, 18)
                order = emit_order(ctx, products_and_qty=[(product, qty)],
                                   placed_at=when, customer_index=i)
                assert order.total_cents % 100 == 0, f"total not round: {order.total_cents}"
                created.append(str(order.id))
            except Exception as e:
                failed.append({"i": i, "error": str(e)[:200]})
        return {"attempted": params.count, "created": created, "failed": failed}
```

Test: assert every created order has `total_cents % 100 == 0`.

Commit: `solex(scenarios): round_amount_cluster`.

### Task 2.5 — `high_value_sale`

**File:** `Solex/solex/services/scenarios/high_value_sale.py` + test

```python
# solex/services/scenarios/high_value_sale.py
from sqlalchemy import select
from solex.services.scenarios.base import (
    Scenario, ScenarioParams, ScenarioContext, emit_order,
)
from solex.services.scenarios.synth import pick_time_in_window
from solex.services.scenarios.registry import register
from solex.models import Product

class Params(ScenarioParams):
    count: int = 2
    min_total_cents: int = 50000  # $500

@register
class HighValueSale(Scenario):
    name = "high_value_sale"
    description = "Orders totaling >= $500 — high-value transaction cluster."
    params_schema = Params

    @classmethod
    def expected_chirps(cls, params):
        return ["C-001 HIGH_VALUE"]

    def run(self, ctx: ScenarioContext, params: Params) -> dict:
        products = ctx.session.execute(
            select(Product).where(Product.active == True).order_by(Product.price_cents.desc())
        ).scalars().all()
        if not products:
            return {"error": "no active products"}

        created, failed = [], []
        for i in range(params.count):
            try:
                # Pick the most expensive item; scale qty until subtotal >= threshold
                top = products[0]
                qty = max(1, -(-params.min_total_cents // top.price_cents))  # ceil div
                when = pick_time_in_window(ctx.rng, 10, 18)
                order = emit_order(ctx, products_and_qty=[(top, qty)],
                                   placed_at=when, customer_index=i)
                assert order.total_cents >= params.min_total_cents
                created.append(str(order.id))
            except Exception as e:
                failed.append({"i": i, "error": str(e)[:200]})
        return {"attempted": params.count, "created": created, "failed": failed}
```

Test: assert every order `total_cents >= 50000`.

Commit: `solex(scenarios): high_value_sale`.

### Task 2.6 — `bulk_reseller_order`

**File:** `Solex/solex/services/scenarios/bulk_reseller_order.py` + test

```python
# solex/services/scenarios/bulk_reseller_order.py
from sqlalchemy import select
from solex.services.scenarios.base import (
    Scenario, ScenarioParams, ScenarioContext, emit_order,
)
from solex.services.scenarios.synth import pick_time_in_window
from solex.services.scenarios.registry import register
from solex.models import Product

class Params(ScenarioParams):
    count: int = 2
    lines_per_order_min: int = 10
    lines_per_order_max: int = 30

@register
class BulkResellerOrder(Scenario):
    name = "bulk_reseller_order"
    description = "1–2 baskets with 10–30 line items — MLM reseller-to-reseller order flavor."
    params_schema = Params

    @classmethod
    def expected_chirps(cls, params):
        return ["VOLUME_ANOMALY (if configured)"]

    def run(self, ctx: ScenarioContext, params: Params) -> dict:
        products = ctx.session.execute(
            select(Product).where(Product.active == True)
        ).scalars().all()
        if not products:
            return {"error": "no active products"}

        created, failed = [], []
        for i in range(params.count):
            try:
                n = ctx.rng.randint(params.lines_per_order_min, params.lines_per_order_max)
                # distinct items (up to available product count)
                picks = ctx.rng.sample(products, min(n, len(products)))
                items = [(p, ctx.rng.randint(2, 6)) for p in picks]
                when = pick_time_in_window(ctx.rng, 10, 18)
                order = emit_order(ctx, products_and_qty=items,
                                   placed_at=when, customer_index=i)
                assert len(order.items) >= params.lines_per_order_min or len(items) >= len(picks)
                created.append(str(order.id))
            except Exception as e:
                failed.append({"i": i, "error": str(e)[:200]})
        return {"attempted": params.count, "created": created, "failed": failed}
```

Test: assert at least one order has >= 10 lines.

Commit: `solex(scenarios): bulk_reseller_order`.

---

## Chunk 3: 4 specialized scenarios

### Task 3.1 — `autoship_cohort`

**File:** `Solex/solex/services/scenarios/autoship_cohort.py` + test

Creates N Customers with Square customer IDs + saved cards, seeds Subscriptions with `next_charge_at` in the past, runs one `SubscriptionService.charge_due_subscriptions` cycle.

```python
# solex/services/scenarios/autoship_cohort.py
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from solex.services.scenarios.base import (
    Scenario, ScenarioParams, ScenarioContext, _square, _checkout_service,
)
from solex.services.scenarios.synth import synth_customer
from solex.services.scenarios.registry import register
from solex.services.subscriptions import SubscriptionService
from solex.models import Customer, Product, Subscription

class Params(ScenarioParams):
    count: int = 20
    cadence_days: int = 30

@register
class AutoshipCohort(Scenario):
    name = "autoship_cohort"
    description = "Cohort of saved-card customers on autoship; runs one charge cycle."
    params_schema = Params

    @classmethod
    def expected_chirps(cls, params):
        return ["REPEAT_CARD_ON_FILE (if configured)"]

    def run(self, ctx: ScenarioContext, params: Params) -> dict:
        products = ctx.session.execute(
            select(Product).where(Product.active == True)
        ).scalars().all()
        if not products:
            return {"error": "no active products"}

        square = _square(ctx.config)
        created_subs = []
        failed = []
        for i in range(params.count):
            try:
                # Square: create sandbox customer + save card
                sc = synth_customer(ctx.rng, str(ctx.run.id)[:8], i)
                sq_customer = square.create_customer(sc.email,
                                                     f"{sc.first_name} {sc.last_name}")
                card = square.save_card_on_file(sq_customer["id"], "cnon:card-nonce-ok")
                # Local
                cust = Customer(
                    email=sc.email, first_name=sc.first_name, last_name=sc.last_name,
                    square_customer_id=sq_customer["id"],
                )
                ctx.session.add(cust); ctx.session.flush()
                product = ctx.rng.choice(products)
                sub = Subscription(
                    customer_id=cust.id, product_id=product.id, qty=1,
                    cadence_days=params.cadence_days,
                    square_card_id=card["id"],
                    next_charge_at=datetime.now(timezone.utc) - timedelta(minutes=1),
                    status="active",
                )
                ctx.session.add(sub); ctx.session.flush()
                created_subs.append(str(sub.id))
            except Exception as e:
                failed.append({"i": i, "error": str(e)[:200]})
        ctx.session.commit()

        # Now charge due
        svc = SubscriptionService(
            session=ctx.session, square=square,
            checkout=_checkout_service(ctx),
        )
        summary = svc.charge_due_subscriptions()

        # Tag the autoship orders with scenario_tag
        from solex.models import Order
        due_orders = ctx.session.execute(
            select(Order).where(
                Order.autoship == True,
                Order.autoship_subscription_id.in_([uuid_str_to_uuid(s) for s in created_subs]),
                Order.scenario_tag.is_(None),
            )
        ).scalars().all() if created_subs else []
        for o in due_orders:
            o.scenario_tag = ctx.tag
        ctx.session.commit()

        return {
            "subs_created": len(created_subs), "subs_failed": failed,
            "charge_cycle": summary,
        }

def uuid_str_to_uuid(s: str):
    import uuid
    return uuid.UUID(s)
```

Test: use mocked `SquareClient` — `create_customer`, `save_card_on_file`, `charge_saved_card` all return stub dicts. Assert correct number of Subscriptions created + charge_cycle summary.

Commit: `solex(scenarios): autoship_cohort`.

### Task 3.2 — `refund_wave`

**File:** `Solex/solex/services/scenarios/refund_wave.py` + test

Pre-condition: there must be at least N paid orders. Scenario accepts optional `source_scenario_tag` to scope which orders to refund; if absent, picks any recent paid orders.

```python
# solex/services/scenarios/refund_wave.py
from typing import Optional
from sqlalchemy import select
from solex.services.scenarios.base import (
    Scenario, ScenarioParams, ScenarioContext, _square,
)
from solex.services.scenarios.registry import register
from solex.services.refunds import RefundsService
from solex.services.inventory import InventoryService
from solex.models import Order

class Params(ScenarioParams):
    count: int = 6
    source_scenario_tag: Optional[str] = None
    full_refund: bool = True

@register
class RefundWave(Scenario):
    name = "refund_wave"
    description = "Issue a batch of refunds against prior paid orders."
    params_schema = Params

    @classmethod
    def expected_chirps(cls, params):
        return ["REFUND_PATTERN (if configured)"]

    def run(self, ctx: ScenarioContext, params: Params) -> dict:
        q = select(Order).where(Order.status == "paid")
        if params.source_scenario_tag:
            q = q.where(Order.scenario_tag == params.source_scenario_tag)
        q = q.order_by(Order.placed_at.desc()).limit(params.count)
        orders = ctx.session.execute(q).scalars().all()
        if not orders:
            return {"error": "no paid orders to refund"}

        svc = RefundsService(
            session=ctx.session,
            square=_square(ctx.config),
            inventory=InventoryService(ctx.session),
        )
        refunded, failed = [], []
        for o in orders:
            try:
                amount = o.total_cents if params.full_refund else o.total_cents // 2
                refund = svc.issue_refund(o, amount, reason=f"scenario:{ctx.tag}",
                                          scenario_tag=ctx.tag)
                refunded.append({"order_id": str(o.id), "refund_id": str(refund.id)})
            except Exception as e:
                failed.append({"order_id": str(o.id), "error": str(e)[:200]})
        return {"attempted": len(orders), "refunded": refunded, "failed": failed}
```

Test: seed 3 paid orders, run `RefundWave(count=2)`, mock SquareClient.create_refund, assert 2 Refund rows with scenario_tag set and Order.status transitions.

Commit: `solex(scenarios): refund_wave`.

### Task 3.3 — `shrink_event`

**File:** `Solex/solex/services/scenarios/shrink_event.py` + test

```python
# solex/services/scenarios/shrink_event.py
from sqlalchemy import select
from solex.services.scenarios.base import Scenario, ScenarioParams, ScenarioContext
from solex.services.scenarios.registry import register
from solex.services.inventory import InventoryService
from solex.models import Product, Inventory

class Params(ScenarioParams):
    count: int = 6          # number of SKUs to shrink
    min_delta: int = 1
    max_delta: int = 4

@register
class ShrinkEvent(Scenario):
    name = "shrink_event"
    description = "Inventory shrink across several SKUs with no offsetting sales."
    params_schema = Params

    @classmethod
    def expected_chirps(cls, params):
        return ["GRO-297 SHRINK_EVENT"]

    def run(self, ctx: ScenarioContext, params: Params) -> dict:
        rows = ctx.session.execute(
            select(Product, Inventory).join(Inventory, Inventory.product_id == Product.id)
            .where(Product.active == True, Inventory.on_hand > 0)
        ).all()
        if not rows:
            return {"error": "no inventory to shrink"}

        picks = ctx.rng.sample(rows, min(params.count, len(rows)))
        svc = InventoryService(ctx.session)
        shrunk, failed = [], []
        for product, inv in picks:
            try:
                delta = -min(
                    ctx.rng.randint(params.min_delta, params.max_delta),
                    inv.on_hand,
                )
                adj = svc.adjust(product.id, delta, reason="shrink", scenario_tag=ctx.tag)
                shrunk.append({
                    "product_id": str(product.id), "sku": product.sku,
                    "delta": delta, "adjustment_id": str(adj.id),
                })
            except Exception as e:
                failed.append({"product_id": str(product.id), "error": str(e)[:200]})
        ctx.session.commit()
        return {"attempted": len(picks), "shrunk": shrunk, "failed": failed}
```

Test: seed 3 products with inventory; run `ShrinkEvent(count=2)`; assert 2 `InventoryAdjustment` rows with `reason='shrink'` and matching scenario_tag; `on_hand` decreased.

Commit: `solex(scenarios): shrink_event`.

### Task 3.4 — `cart_abandonment_cohort`

**File:** `Solex/solex/services/scenarios/cart_abandonment_cohort.py` + test

Creates `Customer` + `Cart` + `CartLine` rows with a stale `last_activity_at`. Doesn't trigger the abandonment sweep inline — leaves it to the `AbandonmentService` cron (or an admin smoke test).

```python
# solex/services/scenarios/cart_abandonment_cohort.py
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from sqlalchemy import select
from solex.services.scenarios.base import Scenario, ScenarioParams, ScenarioContext
from solex.services.scenarios.synth import synth_customer
from solex.services.scenarios.registry import register
from solex.models import Customer, Cart, CartLine, Product

class Params(ScenarioParams):
    count: int = 10
    hours_idle: int = 3

@register
class CartAbandonmentCohort(Scenario):
    name = "cart_abandonment_cohort"
    description = "Creates stale carts belonging to synth customers; abandonment sweep can nudge them."
    params_schema = Params

    @classmethod
    def expected_chirps(cls, params):
        return []

    def run(self, ctx: ScenarioContext, params: Params) -> dict:
        products = ctx.session.execute(
            select(Product).where(Product.active == True)
        ).scalars().all()
        if not products:
            return {"error": "no active products"}

        activity = datetime.now(timezone.utc) - timedelta(hours=params.hours_idle)
        created = []
        for i in range(params.count):
            sc = synth_customer(ctx.rng, str(ctx.run.id)[:8], i)
            cust = Customer(email=sc.email, first_name=sc.first_name, last_name=sc.last_name)
            ctx.session.add(cust); ctx.session.flush()
            cart = Cart(
                customer_id=cust.id, session_key=f"{ctx.tag}-{i}",
                currency="USD", last_activity_at=activity,
            )
            ctx.session.add(cart); ctx.session.flush()
            product = ctx.rng.choice(products)
            ctx.session.add(CartLine(
                cart_id=cart.id, product_id=product.id, qty=1,
                price_snapshot_cents=product.price_cents,
            ))
            created.append({"cart_id": str(cart.id), "customer_id": str(cust.id)})
        ctx.session.commit()
        return {"attempted": params.count, "created": created}
```

Test: run with count=3, assert 3 Carts + 3 CartLines + 3 Customers created; `last_activity_at` is in the past.

Commit: `solex(scenarios): cart_abandonment_cohort`.

---

## Chunk 4: Lab UI + CLI + RQ entry

### Task 4.1 — Lab blueprint

**Files:**
- Create: `Solex/solex/routes/lab.py`
- Create: `Solex/solex/templates/admin/lab/list.html`
- Create: `Solex/solex/templates/admin/lab/run_form.html`
- Create: `Solex/solex/templates/admin/lab/run_detail.html`
- Modify: `Solex/solex/__init__.py` — register
- Modify: `Solex/solex/templates/admin/_layout.html` — add "Lab" sidebar link
- Create: `Solex/tests/unit/test_routes_lab.py`

```python
# solex/routes/lab.py
from datetime import datetime, timezone
from flask import Blueprint, render_template, request, redirect, url_for, abort, current_app, flash
from flask_login import current_user
from sqlalchemy import select
from solex.extensions import db
from solex.routes.admin_utils import admin_required
from solex.services.scenarios import registry, prepare_context
from solex.models import ScenarioRun, Order

bp = Blueprint("lab", __name__, url_prefix="/admin/lab")

SYNC_THRESHOLD = 5  # runs bigger than this get enqueued

@bp.get("/")
@admin_required
def list_scenarios():
    registry._import_all()
    scenarios = []
    for name, cls in sorted(registry.all_scenarios().items()):
        # Build a default params instance to display expected_chirps
        params = cls.params_schema()
        scenarios.append({
            "name": name,
            "description": cls.description,
            "expected_chirps": cls.expected_chirps(params),
        })
    recent = db.session.execute(
        select(ScenarioRun).order_by(ScenarioRun.started_at.desc()).limit(25)
    ).scalars().all()
    return render_template("admin/lab/list.html", scenarios=scenarios, recent=recent)

@bp.route("/scenarios/<name>", methods=["GET", "POST"])
@admin_required
def run_form(name):
    registry._import_all()
    cls = registry.get(name)
    if cls is None:
        abort(404)
    if request.method == "POST":
        raw = {k: v for k, v in request.form.items() if k != "csrf_token"}
        # Coerce obvious types
        params_kwargs = _coerce_form_to_params(cls.params_schema, raw)
        try:
            params = cls.params_schema(**params_kwargs)
        except Exception as e:
            flash(f"Invalid params: {e}", "error")
            return render_template("admin/lab/run_form.html",
                                   name=name, cls=cls, form=raw)
        run = ScenarioRun(
            scenario_name=name,
            params_json=params.model_dump(),
            admin_user_id=current_user.id if hasattr(current_user, "id") else None,
            started_at=datetime.now(timezone.utc),
            status="pending",
            summary_json={},
        )
        db.session.add(run); db.session.commit()

        # Decide sync vs RQ
        count = params_kwargs.get("count") or getattr(params, "count", 0) or 0
        if count <= SYNC_THRESHOLD:
            _run_sync(run)
        else:
            _enqueue(run)
        return redirect(url_for("lab.run_detail", run_id=run.id))

    return render_template("admin/lab/run_form.html",
                           name=name, cls=cls, form={})

@bp.get("/runs/<uuid:run_id>")
@admin_required
def run_detail(run_id):
    run = db.session.get(ScenarioRun, run_id)
    if run is None:
        abort(404)
    tagged_orders = db.session.execute(
        select(Order).where(Order.scenario_tag.like(f"{run.scenario_name}-{str(run.id)[:8]}%"))
    ).scalars().all()
    return render_template("admin/lab/run_detail.html", run=run, orders=tagged_orders)

def _coerce_form_to_params(schema_cls, raw: dict) -> dict:
    """Coerce HTML form strings into pydantic-friendly types by consulting the schema."""
    out = {}
    fields = schema_cls.model_fields
    for k, v in raw.items():
        if k not in fields or v == "":
            continue
        annot = fields[k].annotation
        try:
            if annot is int or annot is type(None) | int:
                out[k] = int(v)
            elif annot is bool:
                out[k] = v.lower() in ("1", "true", "on", "yes")
            else:
                out[k] = v
        except Exception:
            out[k] = v
    return out

def _run_sync(run: ScenarioRun):
    from solex.services.scenarios.base import prepare_context
    cls = registry.get(run.scenario_name)
    if cls is None:
        run.status = "failed"
        run.summary_json = {"error": f"unknown scenario: {run.scenario_name}"}
        db.session.commit()
        return
    try:
        run.status = "running"
        db.session.commit()
        ctx = prepare_context(db.session, run, config=dict(current_app.config))
        scenario = cls()
        params = cls.params_schema(**run.params_json)
        summary = scenario.run(ctx, params)
        run.summary_json = summary
        run.completed_at = datetime.now(timezone.utc)
        if summary.get("failed") and len(summary["failed"]) == summary.get("attempted"):
            run.status = "failed"
        elif summary.get("failed"):
            run.status = "partial"
        else:
            run.status = "succeeded"
    except Exception as e:
        run.status = "failed"
        run.summary_json = {"error": str(e)[:500]}
        run.completed_at = datetime.now(timezone.utc)
    db.session.commit()

def _enqueue(run: ScenarioRun):
    from redis import Redis
    from rq import Queue
    q = Queue("solex-default", connection=Redis.from_url(current_app.config["VALKEY_URL"]))
    q.enqueue("solex.jobs.scenarios.execute_scenario_run", str(run.id))
```

Templates:

```html
{# admin/lab/list.html #}
{% extends "admin/_layout.html" %}
{% block admin_main %}
<h1 class="text-2xl font-semibold mb-6">Lab</h1>
<h2 class="font-semibold mb-3">Scenarios</h2>
<ul class="divide-y mb-8">
  {% for s in scenarios %}
  <li class="py-3">
    <div class="flex justify-between">
      <div>
        <a href="{{ url_for('lab.run_form', name=s.name) }}" class="font-medium">{{ s.name }}</a>
        <p class="text-sm text-stone-500">{{ s.description }}</p>
        {% if s.expected_chirps %}<p class="text-xs text-stone-400">Expects: {{ s.expected_chirps | join(', ') }}</p>{% endif %}
      </div>
      <a href="{{ url_for('lab.run_form', name=s.name) }}" class="text-sm underline">Run →</a>
    </div>
  </li>
  {% endfor %}
</ul>
<h2 class="font-semibold mb-3">Recent runs</h2>
<table class="w-full text-sm">
  <thead><tr class="border-b text-left"><th>Scenario</th><th>Started</th><th>Status</th></tr></thead>
  <tbody>
    {% for r in recent %}
    <tr class="border-b"><td class="py-2"><a href="{{ url_for('lab.run_detail', run_id=r.id) }}" class="underline">{{ r.scenario_name }}</a></td>
      <td>{{ r.started_at.strftime('%Y-%m-%d %H:%M') }}</td><td>{{ r.status }}</td></tr>
    {% endfor %}
  </tbody>
</table>
{% endblock %}
```

```html
{# admin/lab/run_form.html #}
{% extends "admin/_layout.html" %}
{% block admin_main %}
<h1 class="text-2xl font-semibold mb-2">{{ name }}</h1>
<p class="text-stone-500 mb-6">{{ cls.description }}</p>
<form method="post" class="max-w-md space-y-3">
  <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
  {% for fname, field in cls.params_schema.model_fields.items() %}
  <label class="block">
    <span class="text-sm">{{ fname }}</span>
    <input type="text" name="{{ fname }}"
           value="{{ form.get(fname, field.default if field.default is not none else '') }}"
           class="w-full border p-2">
  </label>
  {% endfor %}
  <button type="submit" class="bg-stone-900 text-white px-4 py-2">Run</button>
</form>
{% endblock %}
```

```html
{# admin/lab/run_detail.html #}
{% extends "admin/_layout.html" %}
{% block admin_main %}
<h1 class="text-xl font-semibold mb-2">{{ run.scenario_name }}</h1>
<p class="text-sm text-stone-500 mb-4">{{ run.started_at.strftime('%Y-%m-%d %H:%M:%S') }} — <strong>{{ run.status }}</strong></p>
<section class="mb-6">
  <h2 class="font-semibold mb-2">Params</h2>
  <pre class="bg-stone-100 p-3 text-xs overflow-auto">{{ run.params_json | tojson(indent=2) }}</pre>
</section>
<section class="mb-6">
  <h2 class="font-semibold mb-2">Summary</h2>
  <pre class="bg-stone-100 p-3 text-xs overflow-auto">{{ run.summary_json | tojson(indent=2) }}</pre>
</section>
<section>
  <h2 class="font-semibold mb-2">Tagged orders ({{ orders | length }})</h2>
  {% if orders %}
  <ul class="divide-y text-sm">
    {% for o in orders %}
    <li class="py-2"><a href="{{ url_for('admin_orders.detail', oid=o.id) }}" class="underline">{{ o.public_token }}</a> — ${{ '%.2f' % (o.total_cents / 100) }} — {{ o.status }}</li>
    {% endfor %}
  </ul>
  {% else %}<p class="text-stone-500">None.</p>{% endif %}
</section>
{% endblock %}
```

Modify `admin/_layout.html` sidebar: add `<a href="/admin/lab/" class="block">Lab</a>` after "Returns" link.

Register blueprint in `solex/__init__.py`: `app.register_blueprint(lab.bp)`.

Tests: unauthenticated → 302/401; authenticated admin GET /admin/lab/ → 200 with all 9 scenarios listed; POST run_form with `count=3` creates ScenarioRun row.

Commit: `solex(lab): /admin/lab — list + run form + run detail`.

### Task 4.2 — RQ job entry + CLI

**Files:**
- Create: `Solex/solex/jobs/scenarios.py`
- Modify: `Solex/solex/cli.py` — add `scenarios list` + `scenarios run`
- Create: `Solex/tests/unit/test_jobs_scenarios.py`

```python
# solex/jobs/scenarios.py
def execute_scenario_run(run_id: str):
    """RQ entrypoint."""
    import logging
    from solex import create_app
    from solex.extensions import db
    from solex.models import ScenarioRun
    from solex.services.scenarios import registry, prepare_context
    from datetime import datetime, timezone

    registry._import_all()
    app = create_app()
    with app.app_context():
        run = db.session.get(ScenarioRun, run_id)
        if run is None:
            logging.getLogger(__name__).warning("scenario run not found: %s", run_id)
            return
        cls = registry.get(run.scenario_name)
        if cls is None:
            run.status = "failed"
            run.summary_json = {"error": f"unknown scenario: {run.scenario_name}"}
            run.completed_at = datetime.now(timezone.utc)
            db.session.commit()
            return
        try:
            run.status = "running"; db.session.commit()
            ctx = prepare_context(db.session, run, config=dict(app.config))
            scenario = cls()
            params = cls.params_schema(**run.params_json)
            summary = scenario.run(ctx, params)
            run.summary_json = summary
            run.completed_at = datetime.now(timezone.utc)
            if summary.get("failed") and len(summary["failed"]) == summary.get("attempted"):
                run.status = "failed"
            elif summary.get("failed"):
                run.status = "partial"
            else:
                run.status = "succeeded"
        except Exception as e:
            run.status = "failed"
            run.summary_json = {"error": str(e)[:500]}
            run.completed_at = datetime.now(timezone.utc)
        db.session.commit()
        return run.summary_json
```

CLI (append to existing `solex/cli.py`):

```python
@cli.group()
def scenarios(): ...

@scenarios.command("list")
def scenarios_list():
    from solex.services.scenarios import registry
    registry._import_all()
    for name, cls in sorted(registry.all_scenarios().items()):
        click.echo(f"{name:30s} {cls.description}")

@scenarios.command("run")
@click.argument("name")
@click.option("--params-json", default="{}")
def scenarios_run(name, params_json):
    import json
    from datetime import datetime, timezone
    from solex.services.scenarios import registry, prepare_context
    registry._import_all()
    cls = registry.get(name)
    if cls is None:
        click.echo(f"unknown scenario: {name}")
        raise SystemExit(1)
    app = create_app()
    with app.app_context():
        from solex.models import ScenarioRun
        params = cls.params_schema(**json.loads(params_json))
        run = ScenarioRun(
            scenario_name=name, params_json=params.model_dump(),
            started_at=datetime.now(timezone.utc), status="running", summary_json={},
        )
        db.session.add(run); db.session.commit()
        ctx = prepare_context(db.session, run, config=dict(app.config))
        summary = cls().run(ctx, params)
        run.summary_json = summary
        run.completed_at = datetime.now(timezone.utc)
        run.status = "succeeded" if not summary.get("failed") else "partial"
        db.session.commit()
        click.echo(json.dumps(summary, indent=2, default=str))
```

Test: unit-test `execute_scenario_run` with a mocked registry that returns a toy scenario; assert status transitions `pending → running → succeeded`.

Commit: `solex(jobs): RQ entry for scenario runs + CLI scenarios run/list`.

### Task 4.3 — Admin Orders filter by `scenario_tag`

**Files:**
- Modify: `Solex/solex/routes/admin_orders.py` — accept `?scenario_tag=...`
- Modify: `Solex/solex/templates/admin/orders/list.html` — render scenario_tag column
- Modify: `Solex/tests/unit/test_admin_orders.py` — new test

```python
# admin_orders.py list_orders — replace query:
@bp.get("/")
@admin_required
def list_orders():
    tag = request.args.get("scenario_tag")
    q = select(Order).order_by(Order.placed_at.desc()).limit(200)
    if tag:
        q = q.where(Order.scenario_tag == tag)
    orders = db.session.execute(q).scalars().all()
    return render_template("admin/orders/list.html", orders=orders, scenario_tag=tag)
```

Template: render `{{ order.scenario_tag or '' }}` as a column; add a `?scenario_tag=` filter input at the top.

Commit: `solex(admin): orders list — scenario_tag filter`.

---

## Chunk 5: Sandbox-live + final matrix + PR

### Task 5.1 — Sandbox-live scenario test

**File:** `Solex/tests/integration/test_scenario_sandbox.py`

```python
"""Sandbox-live test: run high_value_sale(count=1) against the real Square sandbox.
Marked `sandbox_live`; auto-skips without creds."""
import os
from datetime import datetime, timezone
from pathlib import Path
import pytest
from solex.services.catalog_import import CatalogImporter
from solex.services.scenarios import registry, prepare_context
from solex.models import ScenarioRun, Order
from solex.services.square_client import SquareClient, SquareConfig

pytestmark = pytest.mark.sandbox_live

_REQUIRED = ("SQUARE_SANDBOX_ACCESS_TOKEN", "SQUARE_SANDBOX_APPLICATION_ID",
             "SQUARE_SANDBOX_LOCATION_ID")

def test_high_value_scenario_against_sandbox(app, db_session, tmp_path):
    missing = [v for v in _REQUIRED if not os.environ.get(v)]
    if missing:
        pytest.skip(f"sandbox creds missing: {missing}")

    (tmp_path / "catalog").mkdir(exist_ok=True)
    CatalogImporter(db_session, Path("catalog"), tmp_path).import_from_yaml(
        Path("catalog/products.yaml"))
    db_session.expire_all()

    registry._import_all()
    cls = registry.get("high_value_sale")
    run = ScenarioRun(
        scenario_name="high_value_sale",
        params_json={"count": 1, "seed": 7},
        started_at=datetime.now(timezone.utc), status="running", summary_json={},
    )
    db_session.add(run); db_session.flush()

    ctx = prepare_context(db_session, run, config={
        "SQUARE_ACCESS_TOKEN": os.environ["SQUARE_SANDBOX_ACCESS_TOKEN"],
        "SQUARE_ENVIRONMENT": "sandbox",
        "SQUARE_LOCATION_ID": os.environ["SQUARE_SANDBOX_LOCATION_ID"],
        "SQUARE_WEBHOOK_SIGNATURE_KEY": os.environ.get("SQUARE_SANDBOX_WEBHOOK_SIGNATURE_KEY", ""),
        "TAX_RATE_PCT": 0.0,
        "SHIPPING_FLAT_CENTS": 0,
        "SHIPPING_FREE_THRESHOLD_CENTS": 1,
    })
    summary = cls().run(ctx, cls.params_schema(count=1, seed=7))
    assert summary["attempted"] == 1
    assert len(summary["created"]) == 1
    assert not summary["failed"]

    order = db_session.query(Order).filter_by(scenario_tag=ctx.tag).one()
    assert order.status == "paid"
    assert order.total_cents >= 50000
    assert order.square_payment_id

    # Cleanup: refund the sandbox payment
    sq = SquareClient(SquareConfig(
        access_token=os.environ["SQUARE_SANDBOX_ACCESS_TOKEN"],
        environment="sandbox",
        location_id=os.environ["SQUARE_SANDBOX_LOCATION_ID"],
        webhook_signature_key=os.environ.get("SQUARE_SANDBOX_WEBHOOK_SIGNATURE_KEY", ""),
    ))
    try:
        sq.create_refund(order.square_payment_id, order.total_cents, reason="test-cleanup")
    except Exception:
        pass
```

Run:
```bash
docker compose -f devops/docker-compose.yml run --rm -e SOLEX_ENV=testing web \
  pytest tests/integration/test_scenario_sandbox.py -v -m sandbox_live
```

Commit: `solex(tests): sandbox-live scenario — high_value_sale cycle`.

### Task 5.2 — Final test matrix

```bash
cd ~/GrowDirect/Solex
docker compose -f devops/docker-compose.yml run --rm -e SOLEX_ENV=testing web \
  pytest tests/unit tests/integration -m "not sandbox_live" 2>&1 | tail -5
docker compose -f devops/docker-compose.yml run --rm -e SOLEX_ENV=testing web \
  pytest -m sandbox_live 2>&1 | tail -5
```

Expect: all green. Target ~240 unit/integration + 3 sandbox-live tests.

Browser smoke:
```bash
./devops/scripts/dev.sh up
sleep 3
# Log in as admin
# Navigate to /admin/lab/
# Run shrink_event with count=3 (sync — no Square call)
# Inspect /admin/orders?scenario_tag=shrink_event-<runid>
# Run normal_retail_day with count=3 (sync, 3 real sandbox orders)
# Verify 3 orders appear at /admin/orders filtered by tag
./devops/scripts/dev.sh down
```

No commit needed for 5.2 — verification only.

### Task 5.3 — Push + Open PR

```bash
cd ~/GrowDirect
git push -u origin plan/solex-scenarios
```

```bash
gh pr create --base plan/solex-operations \
  --title "feat: solex scenarios — /admin/lab + 9 canned scenarios" \
  --body "<full body per Plan 2 convention — summary, links, in/out scope, known issues, test plan checkboxes>"
```

---

## Plan 3 — Done criteria (repeat)

- [ ] `/admin/lab` lists all 9 scenarios with name/description/expected chirps
- [ ] Each scenario runs inline for small counts and via RQ for large
- [ ] Every `Order`, `Refund`, `InventoryAdjustment`, `Cart` emitted by a scenario is tagged with `scenario_tag`
- [ ] Admin Orders page supports `?scenario_tag=...` filter
- [ ] Sandbox-live `high_value_sale` test passes
- [ ] Full test matrix green (~240 unit/integration + 3 sandbox-live)
- [ ] No regression in Plans 1/2

## What's next (for context, not execution)

- **Plan 4 — Visual fidelity:** Tailwind theme matching solexglobal.com, hero sections, real imagery, full 25-SKU catalog. No new functionality — pure design polish.
