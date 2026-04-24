def execute_scenario_run(run_id: str):
    """RQ entrypoint. Executes a pending/running ScenarioRun."""
    import logging
    from datetime import datetime, timezone

    from solex import create_app
    from solex.extensions import db
    from solex.models import ScenarioRun
    from solex.services.scenarios import registry, prepare_context

    log = logging.getLogger(__name__)
    registry._import_all()
    app = create_app()
    with app.app_context():
        run = db.session.get(ScenarioRun, run_id)
        if run is None:
            log.warning("scenario run not found: %s", run_id)
            return
        cls = registry.get(run.scenario_name)
        if cls is None:
            run.status = "failed"
            run.summary_json = {"error": f"unknown scenario: {run.scenario_name}"}
            run.completed_at = datetime.now(timezone.utc)
            db.session.commit()
            return
        try:
            run.status = "running"; db.session.commit()
            ctx = prepare_context(db.session, run, config=dict(app.config))
            params = cls.params_schema(**run.params_json)
            summary = cls().run(ctx, params)
            run.summary_json = summary
            run.completed_at = datetime.now(timezone.utc)
            failed = summary.get("failed") or []
            attempted = summary.get("attempted") or 0
            if summary.get("error"):
                run.status = "failed"
            elif failed and attempted and len(failed) == attempted:
                run.status = "failed"
            elif failed:
                run.status = "partial"
            else:
                run.status = "succeeded"
        except Exception as e:
            run.status = "failed"
            run.summary_json = {"error": str(e)[:500]}
            run.completed_at = datetime.now(timezone.utc)
        db.session.commit()
        return run.summary_json
