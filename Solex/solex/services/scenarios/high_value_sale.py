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
    category = "fraud"
    expected_behaviors = [
        "One or more orders with total_cents >= min_total_cents",
        "Square charges succeed; payment_token = card-nonce-ok",
        "Inventory decrements on the top-priced active product",
    ]
    params_schema = Params

    @classmethod
    def expected_chirps(cls, params):
        return ["C-001 HIGH_VALUE"]

    def run(self, ctx: ScenarioContext, params: Params) -> dict:
        products = ctx.session.execute(
            select(Product).where(Product.active == True)
            .order_by(Product.price_cents.desc())
        ).scalars().all()
        if not products:
            return {"error": "no active products"}

        created, failed = [], []
        for i in range(params.count):
            try:
                top = products[0]
                qty = max(1, -(-params.min_total_cents // top.price_cents))
                when = pick_time_in_window(ctx.rng, 10, 18)
                order = emit_order(
                    ctx, products_and_qty=[(top, qty)],
                    placed_at=when, customer_index=i,
                )
                assert order.total_cents >= params.min_total_cents
                created.append(str(order.id))
            except Exception as e:
                failed.append({"i": i, "error": str(e)[:200]})
        return {"attempted": params.count, "created": created, "failed": failed}
