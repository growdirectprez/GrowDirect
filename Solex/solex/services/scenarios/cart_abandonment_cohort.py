from datetime import datetime, timedelta, timezone

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
    category = "customer_behavior"
    expected_behaviors = [
        "N idle Cart rows aged hours_idle behind now (stale activity)",
        "No Order rows produced (carts never check out)",
        "Abandonment-recovery email sweep can pick up these carts",
    ]
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
            cust = Customer(
                email=sc.email, first_name=sc.first_name, last_name=sc.last_name,
            )
            ctx.session.add(cust)
            ctx.session.flush()
            cart = Cart(
                customer_id=cust.id,
                session_key=f"{ctx.tag}-{i}",
                currency="USD",
                last_activity_at=activity,
            )
            ctx.session.add(cart)
            ctx.session.flush()
            product = ctx.rng.choice(products)
            ctx.session.add(CartLine(
                cart_id=cart.id,
                product_id=product.id,
                qty=1,
                price_snapshot_cents=product.price_cents,
            ))
            created.append({"cart_id": str(cart.id), "customer_id": str(cust.id)})
        ctx.session.commit()
        return {"attempted": params.count, "created": created}
