def run_abandonment_sweep():
    from solex import create_app
    from solex.extensions import db
    from solex.services.abandonment import AbandonmentService
    import logging

    app = create_app()
    with app.app_context():
        summary = AbandonmentService(db.session).sweep()
        logging.getLogger(__name__).info("abandonment summary=%s", summary)
        return summary
