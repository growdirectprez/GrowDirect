def charge_due_subscriptions():
    """RQ job entrypoint. Runs inside a worker with Flask app context."""
    from solex import create_app
    from solex.extensions import db
    from solex.services.subscriptions import SubscriptionService
    from solex.services.square_client import SquareClient, SquareConfig
    from solex.services.checkout import CheckoutService
    from solex.services.tax import FlatRateTaxStub
    from solex.services.shipping import FlatRateShippingStub
    from solex.services.inventory import InventoryService
    import logging

    app = create_app()
    with app.app_context():
        cfg = app.config
        sq = SquareClient(SquareConfig(
            access_token=cfg["SQUARE_ACCESS_TOKEN"],
            environment=cfg["SQUARE_ENVIRONMENT"],
            location_id=cfg["SQUARE_LOCATION_ID"],
            webhook_signature_key=cfg["SQUARE_WEBHOOK_SIGNATURE_KEY"],
        ))
        co = CheckoutService(
            session=db.session, square=sq,
            tax=FlatRateTaxStub(cfg["TAX_RATE_PCT"]),
            shipping=FlatRateShippingStub(
                cfg["SHIPPING_FLAT_CENTS"], cfg["SHIPPING_FREE_THRESHOLD_CENTS"]),
            inventory=InventoryService(db.session),
        )
        svc = SubscriptionService(db.session, sq, co)
        summary = svc.charge_due_subscriptions()
        logging.getLogger(__name__).info("subscriptions summary=%s", summary)
        return summary
