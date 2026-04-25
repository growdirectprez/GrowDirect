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
    category = "fraud"
    expected_behaviors = [
        "N most-recent paid orders refunded via Square + Refund rows persisted",
        "Inventory restored on full refunds (re-stock adjustments)",
        "REFUND_PATTERN rule fires when configured for refund-velocity detection",
    ]
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
                refund = svc.issue_refund(
                    o, amount, reason=f"scenario:{ctx.tag}",
                    scenario_tag=ctx.tag,
                )
                refunded.append({"order_id": str(o.id), "refund_id": str(refund.id)})
            except Exception as e:
                failed.append({"order_id": str(o.id), "error": str(e)[:200]})
        return {"attempted": len(orders), "refunded": refunded, "failed": failed}
