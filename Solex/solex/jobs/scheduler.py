"""rq-scheduler bootstrap."""
import logging
import os
from redis import Redis
from rq_scheduler import Scheduler

log = logging.getLogger(__name__)


def _connection() -> Redis:
    return Redis.from_url(os.environ["VALKEY_URL"])


def build() -> Scheduler:
    return Scheduler(connection=_connection(), queue_name="solex-default")


def schedule_recurring_jobs() -> list[str]:
    """Idempotently register the recurring jobs. Returns list of job IDs."""
    sched = build()
    # Remove any existing jobs with our IDs so restarts are clean
    for job in sched.get_jobs():
        jid = getattr(job, "id", "")
        if jid in ("solex:charge_due_subscriptions", "solex:abandonment_sweep"):
            sched.cancel(job)

    job_ids = []
    j1 = sched.cron(
        "*/15 * * * *",
        id="solex:charge_due_subscriptions",
        func="solex.jobs.subscriptions.charge_due_subscriptions",
        queue_name="solex-default",
    )
    job_ids.append(j1.id if hasattr(j1, "id") else "solex:charge_due_subscriptions")
    j2 = sched.cron(
        "*/30 * * * *",
        id="solex:abandonment_sweep",
        func="solex.jobs.abandonment.run_abandonment_sweep",
        queue_name="solex-default",
    )
    job_ids.append(j2.id if hasattr(j2, "id") else "solex:abandonment_sweep")
    log.info("scheduled recurring jobs: %s", job_ids)
    return job_ids


def run_forever():
    schedule_recurring_jobs()
    sched = build()
    sched.run()
