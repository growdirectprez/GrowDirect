from sqlalchemy import select

from solex.services.scenarios.base import Scenario, ScenarioParams, ScenarioContext
from solex.services.scenarios.registry import register
from solex.services.inventory import InventoryService
from solex.models import Product, Inventory


class Params(ScenarioParams):
    count: int = 6           # number of SKUs to shrink
    min_delta: int = 1
    max_delta: int = 4


@register
class ShrinkEvent(Scenario):
    name = "shrink_event"
    description = "Inventory shrink across several SKUs with no offsetting sales."
    category = "loss_prevention"
    expected_behaviors = [
        "Negative InventoryAdjustment rows with reason=shrink across N SKUs",
        "No offsetting Order rows (shrink is loss, not sale)",
        "GRO-297 SHRINK_EVENT rule should fire on aggregate negative delta",
    ]
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
