# solex/routes/lab.py
from datetime import datetime, timezone
from flask import Blueprint, render_template, request, redirect, url_for, abort, current_app, flash
from flask_login import current_user
from sqlalchemy import select

from sqlalchemy.exc import IntegrityError
from flask import session as flask_session, jsonify

from solex.extensions import db
from solex.routes.admin_utils import admin_required, _load_admin_from_session
from solex.services.scenarios import registry, prepare_context
from solex.models import ScenarioRun, ScenarioRunFavorite, Order

bp = Blueprint("lab", __name__, url_prefix="/admin/lab")

SYNC_THRESHOLD = 5  # runs bigger than this get enqueued


CATEGORY_LABELS = {
    "operations": "Operations",
    "loss_prevention": "Loss prevention",
    "fraud": "Fraud",
    "customer_behavior": "Customer behavior",
    "subscriptions": "Subscriptions",
}
CATEGORY_ORDER = ["operations", "loss_prevention", "fraud", "customer_behavior", "subscriptions"]


@bp.get("/")
@admin_required
def list_scenarios():
    grouped = registry.by_category()
    categories = []
    for key in CATEGORY_ORDER:
        items = grouped.get(key, [])
        if not items:
            continue
        categories.append({
            "key": key,
            "label": CATEGORY_LABELS[key],
            "scenarios": items,
        })
    recent = db.session.execute(
        select(ScenarioRun).order_by(ScenarioRun.started_at.desc()).limit(25)
    ).scalars().all()
    return render_template("admin/lab/list.html", categories=categories, recent=recent)


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


@bp.get("/runs/")
@admin_required
def list_runs():
    from datetime import datetime, time as _time
    scenario = request.args.get("scenario", "").strip()
    status = request.args.get("status", "").strip()
    favorites_only = request.args.get("favorites", "").strip() in ("1", "true", "on")
    date_from = request.args.get("from", "").strip()
    date_to = request.args.get("to", "").strip()

    q = select(ScenarioRun)
    if scenario:
        q = q.where(ScenarioRun.scenario_name == scenario)
    if status:
        q = q.where(ScenarioRun.status == status)
    if date_from:
        try:
            d = datetime.fromisoformat(date_from)
            q = q.where(ScenarioRun.started_at >= d)
        except ValueError:
            pass
    if date_to:
        try:
            d = datetime.fromisoformat(date_to)
            # treat date_to as end-of-day inclusive
            if d.time() == _time.min:
                d = d.replace(hour=23, minute=59, second=59)
            q = q.where(ScenarioRun.started_at <= d)
        except ValueError:
            pass

    favorited_ids: set = set()
    admin = _load_admin_from_session()
    if admin is not None:
        rows = db.session.execute(
            select(ScenarioRunFavorite.scenario_run_id).where(
                ScenarioRunFavorite.admin_user_id == admin.id
            )
        ).scalars().all()
        favorited_ids = {r for r in rows}
        if favorites_only and favorited_ids:
            q = q.where(ScenarioRun.id.in_(favorited_ids))
        elif favorites_only:
            # no favorites yet — return empty result deterministically
            q = q.where(ScenarioRun.id.is_(None))

    runs = db.session.execute(
        q.order_by(ScenarioRun.started_at.desc()).limit(200)
    ).scalars().all()

    registry._import_all()
    scenario_names = sorted(registry.all_scenarios().keys())

    return render_template(
        "admin/lab/runs.html",
        runs=runs,
        favorited_ids=favorited_ids,
        filters={
            "scenario": scenario, "status": status,
            "favorites": favorites_only,
            "from": date_from, "to": date_to,
        },
        scenario_names=scenario_names,
        statuses=["pending", "running", "succeeded", "partial", "failed"],
    )


@bp.get("/runs/<uuid:run_id>")
@admin_required
def run_detail(run_id):
    from solex.models import InventoryAdjustment, Refund
    run = db.session.get(ScenarioRun, run_id)
    if run is None:
        abort(404)
    tag = f"{run.scenario_name}-{str(run.id)[:8]}"
    tagged_orders = db.session.execute(
        select(Order).where(Order.scenario_tag == tag)
        .order_by(Order.placed_at.desc())
    ).scalars().all()
    tagged_adjustments = db.session.execute(
        select(InventoryAdjustment).where(InventoryAdjustment.scenario_tag == tag)
        .order_by(InventoryAdjustment.created_at.desc())
    ).scalars().all()
    tagged_refunds = db.session.execute(
        select(Refund).where(Refund.scenario_tag == tag)
    ).scalars().all()
    metadata = registry.describe(run.scenario_name) or {}
    # Group adjustments by reason for the structured summary
    adjustments_by_reason: dict[str, list] = {}
    for adj in tagged_adjustments:
        adjustments_by_reason.setdefault(adj.reason or "—", []).append(adj)
    return render_template(
        "admin/lab/run_detail.html",
        run=run,
        metadata=metadata,
        orders=tagged_orders,
        adjustments_by_reason=adjustments_by_reason,
        refunds=tagged_refunds,
        tag=tag,
    )


@bp.get("/runs/<uuid:run_id>/status.json")
@admin_required
def run_status(run_id):
    run = db.session.get(ScenarioRun, run_id)
    if run is None:
        abort(404)
    return jsonify({
        "id": str(run.id),
        "status": run.status,
        "started_at": run.started_at.isoformat() if run.started_at else None,
        "completed_at": run.completed_at.isoformat() if run.completed_at else None,
        "summary_keys": sorted(list((run.summary_json or {}).keys())),
    })


@bp.post("/runs/<uuid:run_id>/favorite")
@admin_required
def toggle_favorite(run_id):
    run = db.session.get(ScenarioRun, run_id)
    if run is None:
        abort(404)
    admin = _load_admin_from_session()
    if admin is None:
        abort(401)
    existing = db.session.execute(
        select(ScenarioRunFavorite).where(
            ScenarioRunFavorite.admin_user_id == admin.id,
            ScenarioRunFavorite.scenario_run_id == run.id,
        )
    ).scalar_one_or_none()
    if existing is not None:
        db.session.delete(existing)
        db.session.commit()
        return "", 204
    fav = ScenarioRunFavorite(admin_user_id=admin.id, scenario_run_id=run.id)
    db.session.add(fav)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()  # raced; treat as already-favorited no-op
    return "", 204


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
