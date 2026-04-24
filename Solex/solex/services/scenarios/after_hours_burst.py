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
    window_end_hour: int = 2


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
        if not products:
            return {"error": "no active products"}
        created, failed = [], []
        for i in range(params.count):
            try:
                when = pick_time_in_window(
                    ctx.rng, params.window_start_hour, params.window_end_hour
                )
                product = ctx.rng.choice(products)
                order = emit_order(
                    ctx, products_and_qty=[(product, 1)],
                    placed_at=when, customer_index=i,
                )
                created.append(str(order.id))
            except Exception as e:
                failed.append({"i": i, "error": str(e)[:200]})
        return {"attempted": params.count, "created": created, "failed": failed}
