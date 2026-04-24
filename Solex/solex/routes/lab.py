# solex/routes/lab.py
from datetime import datetime, timezone
from flask import Blueprint, render_template, request, redirect, url_for, abort, current_app, flash
from flask_login import current_user
from sqlalchemy import select

from solex.extensions import db
from solex.routes.admin_utils import admin_required
from solex.services.scenarios import registry, prepare_context
from solex.models import ScenarioRun, Order

bp = Blueprint("lab", __name__, url_prefix="/admin/lab")

SYNC_THRESHOLD = 5  # runs bigger than this get enqueued


@bp.get("/")
@admin_required
def list_scenarios():
    registry._import_all()
    scenarios = []
    for name, cls in sorted(registry.all_scenarios().items()):
        params = cls.params_schema()
        scenarios.append({
            "name": name,
            "description": cls.description,
            "expected_chirps": cls.expected_chirps(params),
        })
    recent = db.session.execute(
        select(ScenarioRun).order_by(ScenarioRun.started_at.desc()).limit(25)
    ).scalars().all()
    return render_template("admin/lab/list.html", scenarios=scenarios, recent=recent)


@bp.route("/scenarios/<name>", methods=["GET", "POST"])
@admin_required
def run_form(name):
    registry._import_all()
    cls = registry.get(name)
    if cls is None:
        abort(404)
    if request.method == "POST":
        raw = {k: v for k, v in request.form.items() if k != "csrf_token"}
        params_kwargs = _coerce_form_to_params(cls.params_schema, raw)
        try:
            params = cls.params_schema(**params_kwargs)
        except Exception as e:
            flash(f"Invalid params: {e}", "error")
            return render_template("admin/lab/run_form.html",
                                   name=name, cls=cls, form=raw)
        admin_id = None
        try:
            if current_user.is_authenticated:
                admin_id = current_user.id
        except Exception:
            pass
        run = ScenarioRun(
            scenario_name=name,
            params_json=params.model_dump(),
            admin_user_id=admin_id,
            started_at=datetime.now(timezone.utc),
            status="pending",
            summary_json={},
        )
        db.session.add(run); db.session.commit()

        count = params_kwargs.get("count") or getattr(params, "count", 0) or 0
        if count <= SYNC_THRESHOLD:
            _run_sync(run)
        else:
            _enqueue(run)
        return redirect(url_for("lab.run_detail", run_id=run.id))

    return render_template("admin/lab/run_form.html",
                           name=name, cls=cls, form={})


@bp.get("/runs/<uuid:run_id>")
@admin_required
def run_detail(run_id):
    run = db.session.get(ScenarioRun, run_id)
    if run is None:
        abort(404)
    tag = f"{run.scenario_name}-{str(run.id)[:8]}"
    tagged_orders = db.session.execute(
        select(Order).where(Order.scenario_tag == tag)
    ).scalars().all()
    return render_template("admin/lab/run_detail.html", run=run, orders=tagged_orders)


def _coerce_form_to_params(schema_cls, raw: dict) -> dict:
    out = {}
    fields = schema_cls.model_fields
    for k, v in raw.items():
        if k not in fields or v == "":
            continue
        annot = fields[k].annotation
        try:
            if annot is int:
                out[k] = int(v)
            elif annot is bool:
                out[k] = v.lower() in ("1", "true", "on", "yes")
            else:
                out[k] = v
        except Exception:
            out[k] = v
    return out


def _run_sync(run: ScenarioRun):
    cls = registry.get(run.scenario_name)
    if cls is None:
        run.status = "failed"
        run.summary_json = {"error": f"unknown scenario: {run.scenario_name}"}
        db.session.commit()
        return
    try:
        run.status = "running"
        db.session.commit()
        ctx = prepare_context(db.session, run, config=dict(current_app.config))
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


def _enqueue(run: ScenarioRun):
    from redis import Redis
    from rq import Queue
    q = Queue("solex-default", connection=Redis.from_url(current_app.config["VALKEY_URL"]))
    q.enqueue("solex.jobs.scenarios.execute_scenario_run", str(run.id))
