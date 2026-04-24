from datetime import datetime, timedelta, timezone
import uuid

from sqlalchemy import select

from solex.services.scenarios.base import (
    Scenario, ScenarioParams, ScenarioContext, _square, _checkout_service,
)
from solex.services.scenarios.synth import synth_customer
from solex.services.scenarios.registry import register
from solex.services.subscriptions import SubscriptionService
from solex.models import Customer, Product, Subscription, Order


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
                sc = synth_customer(ctx.rng, str(ctx.run.id)[:8], i)
                sq_customer = square.create_customer(
                    sc.email, f"{sc.first_name} {sc.last_name}"
                )
                card = square.save_card_on_file(sq_customer["id"], "cnon:card-nonce-ok")
                cust = Customer(
                    email=sc.email, first_name=sc.first_name, last_name=sc.last_name,
                    square_customer_id=sq_customer["id"],
                )
                ctx.session.add(cust)
                ctx.session.flush()
                product = ctx.rng.choice(products)
                sub = Subscription(
                    customer_id=cust.id, product_id=product.id, qty=1,
                    cadence_days=params.cadence_days,
                    square_card_id=card["id"],
                    next_charge_at=datetime.now(timezone.utc) - timedelta(minutes=1),
                    status="active",
                )
                ctx.session.add(sub)
                ctx.session.flush()
                created_subs.append(str(sub.id))
            except Exception as e:
                failed.append({"i": i, "error": str(e)[:200]})
        ctx.session.commit()

        # Run the due-charge cycle
        svc = SubscriptionService(
            session=ctx.session,
            square=square,
            checkout=_checkout_service(ctx),
        )
        summary = svc.charge_due_subscriptions()

        # Tag the autoship orders that just landed
        if created_subs:
            sub_uuids = [uuid.UUID(s) for s in created_subs]
            autoship_orders = ctx.session.execute(
                select(Order).where(
                    Order.autoship == True,
                    Order.autoship_subscription_id.in_(sub_uuids),
                    Order.scenario_tag.is_(None),
                )
            ).scalars().all()
            for o in autoship_orders:
                o.scenario_tag = ctx.tag
            ctx.session.commit()

        return {
            "subs_created": len(created_subs),
            "subs_failed": failed,
            "charge_cycle": summary,
        }
