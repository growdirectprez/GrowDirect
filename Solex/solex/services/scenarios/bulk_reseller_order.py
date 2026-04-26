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
    category = "customer_behavior"
    expected_behaviors = [
        "Small number of orders, each with 10-30 distinct OrderItem lines",
        "Inventory decrements concentrated across many SKUs at once",
        "VOLUME_ANOMALY rule fires when configured for line-count outliers",
    ]
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
                picks = ctx.rng.sample(products, min(n, len(products)))
                items = [(p, ctx.rng.randint(2, 6)) for p in picks]
                when = pick_time_in_window(ctx.rng, 10, 18)
                order = emit_order(
                    ctx, products_and_qty=items,
                    placed_at=when, customer_index=i,
                )
                created.append(str(order.id))
            except Exception as e:
                failed.append({"i": i, "error": str(e)[:200]})
        return {"attempted": params.count, "created": created, "failed": failed}
