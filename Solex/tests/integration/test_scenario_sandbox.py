"""Sandbox-live scenario test: run high_value_sale(count=1) against the real
Square sandbox. Marked `sandbox_live`; auto-skips without creds."""
import os
from datetime import datetime, timezone
from pathlib import Path

import pytest

from solex.services.catalog_import import CatalogImporter
from solex.services.scenarios import registry, prepare_context
from solex.services.square_client import SquareClient, SquareConfig
from solex.models import ScenarioRun, Order

pytestmark = pytest.mark.sandbox_live

_REQUIRED = (
    "SQUARE_SANDBOX_ACCESS_TOKEN",
    "SQUARE_SANDBOX_APPLICATION_ID",
    "SQUARE_SANDBOX_LOCATION_ID",
)


def test_high_value_scenario_against_sandbox(app, db_session, tmp_path):
    missing = [v for v in _REQUIRED if not os.environ.get(v)]
    if missing:
        pytest.skip(f"sandbox creds missing: {missing}")

    (tmp_path / "catalog").mkdir(exist_ok=True)
    CatalogImporter(db_session, Path("catalog"), tmp_path).import_from_yaml(
        Path("catalog/products.yaml")
    )
    db_session.expire_all()

    registry._import_all()
    cls = registry.get("high_value_sale")
    run = ScenarioRun(
        scenario_name="high_value_sale",
        params_json={"count": 1, "seed": 7},
        started_at=datetime.now(timezone.utc),
        status="running",
        summary_json={},
    )
    db_session.add(run)
    db_session.flush()

    config = {
        "SQUARE_ACCESS_TOKEN": os.environ["SQUARE_SANDBOX_ACCESS_TOKEN"],
        "SQUARE_ENVIRONMENT": "sandbox",
        "SQUARE_LOCATION_ID": os.environ["SQUARE_SANDBOX_LOCATION_ID"],
        "SQUARE_WEBHOOK_SIGNATURE_KEY": os.environ.get(
            "SQUARE_SANDBOX_WEBHOOK_SIGNATURE_KEY", ""
        ),
        "TAX_RATE_PCT": 0.0,
        "SHIPPING_FLAT_CENTS": 0,
        "SHIPPING_FREE_THRESHOLD_CENTS": 1,
    }
    ctx = prepare_context(db_session, run, config=config)
    summary = cls().run(ctx, cls.params_schema(count=1, seed=7))

    assert summary["attempted"] == 1, summary
    assert len(summary["created"]) == 1, summary
    assert not summary["failed"], summary

    order = db_session.query(Order).filter_by(scenario_tag=ctx.tag).one()
    assert order.status == "paid"
    assert order.total_cents >= 50000
    assert order.square_payment_id

    sq = SquareClient(
        SquareConfig(
            access_token=os.environ["SQUARE_SANDBOX_ACCESS_TOKEN"],
            environment="sandbox",
            location_id=os.environ["SQUARE_SANDBOX_LOCATION_ID"],
            webhook_signature_key=os.environ.get(
                "SQUARE_SANDBOX_WEBHOOK_SIGNATURE_KEY", ""
            ),
        )
    )
    try:
        sq.create_refund(
            order.square_payment_id, order.total_cents, reason="test-cleanup"
        )
    except Exception:
        pass
