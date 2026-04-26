import random
import secrets
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar, Sequence, Type

from pydantic import BaseModel
from sqlalchemy.orm import Session

from solex.models import ScenarioRun, Product, Order
from solex.services.checkout import CheckoutService, CartLineIn, CustomerIn
from solex.services.square_client import SquareClient, SquareConfig
from solex.services.inventory import InventoryService
from solex.services.tax import FlatRateTaxStub
from solex.services.shipping import FlatRateShippingStub
from solex.services.scenarios.synth import synth_customer, synth_address


class ScenarioParams(BaseModel):
    """Base params. Override per-scenario."""
    count: int = 10
    seed: int | None = None


@dataclass(frozen=True)
class ScenarioContext:
    session: Session
    run: ScenarioRun
    rng: random.Random
    tag: str
    config: dict


class Scenario(ABC):
    name: ClassVar[str]
    description: ClassVar[str] = ""
    category: ClassVar[str] = ""
    expected_behaviors: ClassVar[list[str]] = []
    params_schema: ClassVar[Type[ScenarioParams]] = ScenarioParams

    @classmethod
    def build_tag(cls, run: ScenarioRun) -> str:
        return f"{cls.name}-{str(run.id)[:8]}"

    @classmethod
    def expected_chirps(cls, params: ScenarioParams) -> list[str]:
        return []

    @abstractmethod
    def run(self, ctx: ScenarioContext, params: ScenarioParams) -> dict: ...


def prepare_context(session: Session, run: ScenarioRun, config: dict) -> ScenarioContext:
    params = run.params_json or {}
    seed = params.get("seed") or secrets.randbits(32)
    rng = random.Random(seed)
    if not params.get("seed"):
        merged = dict(params); merged["seed"] = seed
        run.params_json = merged
    tag = f"{run.scenario_name}-{str(run.id)[:8]}"
    return ScenarioContext(session=session, run=run, rng=rng, tag=tag, config=config)


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
    return svc.place_order(
        cart_lines=lines,
        customer=CustomerIn(email=cust.email, name=f"{cust.first_name} {cust.last_name}"),
        shipping_addr=shipping_addr,
        billing_addr=shipping_addr,
        payment_token=payment_token,
        scenario_tag=ctx.tag,
        placed_at=placed_at,
    )
