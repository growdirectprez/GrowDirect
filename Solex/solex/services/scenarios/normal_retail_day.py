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
    category = "operations"
    expected_behaviors = [
        "Small cohort of paid orders distributed across daytime hours",
        "No detection rule should fire (clean baseline traffic)",
        "Inventory decrements track normal sale velocity",
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
