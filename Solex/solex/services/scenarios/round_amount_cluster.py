from sqlalchemy import select
from solex.services.scenarios.base import (
    Scenario, ScenarioParams, ScenarioContext, emit_order,
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
    category = "fraud"
    expected_behaviors = [
        "Each generated order has total_cents divisible by 100",
        "Free-shipping threshold cleared so shipping=0 (no rounding noise)",
        "C-003 ROUND_AMOUNT rule should fire on the cluster",
    ]
    params_schema = Params

    @classmethod
    def expected_chirps(cls, params):
        return ["C-003 ROUND_AMOUNT"]

    def run(self, ctx: ScenarioContext, params: Params) -> dict:
        # Prefer products whose price is already % 100 == 0 (e.g., $49.95 won't work;
        # $149.00 would). Falls back to any active product if none match.
        round_products = ctx.session.execute(
            select(Product).where(
                Product.active == True, Product.price_cents % 100 == 0
            )
        ).scalars().all()
        if not round_products:
            round_products = ctx.session.execute(
                select(Product).where(Product.active == True)
            ).scalars().all()
        if not round_products:
            return {"error": "no active products"}

        created, failed = [], []
        free_ship = ctx.config.get("SHIPPING_FREE_THRESHOLD_CENTS", 9900)
        for i in range(params.count):
            try:
                product = ctx.rng.choice(round_products)
                # Buy enough to clear the free-shipping threshold so shipping=0.
                min_qty = max(1, (free_ship // product.price_cents) + 1)
                qty = min_qty
                when = pick_time_in_window(ctx.rng, 10, 18)
                order = emit_order(
                    ctx, products_and_qty=[(product, qty)],
                    placed_at=when, customer_index=i,
                )
                assert order.total_cents % 100 == 0, f"total not round: {order.total_cents}"
                created.append(str(order.id))
            except Exception as e:
                failed.append({"i": i, "error": str(e)[:200]})
        return {"attempted": params.count, "created": created, "failed": failed}
