---
classification: confidential
owner: GrowDirect LLC
---

# Code Dispatch — April 22, 2026

## Subject

Rebuild `devops/seeds/level_b_demo.py` against the current consolidated
schema (`canary` DB with `app` / `sales` / `metrics` schemas) and wire it
into `/oauth/merchant-reset` so one click wipes a merchant and reseeds
them into a **known-good, story-rich demo state** with a full multi-month
timeline.

The finished reset flow: click "Reset My Store" → land on `/auth/join` →
Connect with Square → `/welcome` → Complete Setup → bird ring →
`/home` with every screen lit up and every metric populated.

## Scope

One new demo reseeder, one new endpoint flag, one new integration test.
No changes to OAuth redirect targets, no changes to detection rules,
no changes to the HC pipeline, no changes to Square SDK usage.

## The story the data must tell

The seeded merchant is **Default Test Account** (Square sandbox
`MLE55GCYANCYT`) operating **3 farmers markets** (Torrance, Redondo Beach,
Rolling Hills). The central narrative is **Suspicious Steve's descent**:
he started clean in February and slowly slid into active fraud by April.

### Steve's arc across the timeline

| Phase | Window | Behavior | Signals |
|---|---|---|---|
| **Baseline** | 2026-02-01 → 2026-02-21 | Normal. Standard sales, no refunds, no after-hours, no cash variance. | Risk score 0.00–0.15. No alerts. |
| **Drift** | 2026-02-22 → 2026-03-14 | Occasional ambiguous refunds (~1/week). One-off after-hours transaction. Small cash shortages under threshold. | Risk score 0.15–0.35. 1–2 soft alerts, none critical. |
| **Pattern** | 2026-03-15 → 2026-04-05 | Rapid-refund pattern emerges — sells → refunds within 5 min, 2–3×/week. Cash variance crosses C-102 threshold twice. After-hours transactions on Mon + Wed. | Risk score 0.35–0.70. 4–6 alerts firing across C-001, C-002, C-004, C-102. |
| **Active** | 2026-04-06 → today | Daily rapid-refund. Refund rate >15% on Torrance Saturdays. Cash variance every shift. Fox case opened, evidence chain started. | Risk score 0.70–0.92. 8–12 alerts, Fox case `demo-fox-case-0000000000000001` with 3+ evidence items. |

The other four employees (Sofia, Alejandro, James, David) stay clean —
their risk scores stay <0.20 throughout. Contrast matters.

### What populates on every screen after reseed

| Screen | Expected state |
|---|---|
| `/home` dashboard | Today's alerts, today's top risks, this-week's transaction trend with realistic peaks on Saturdays (market day) |
| `/chirps` (alerts) | 8–12 active alerts of varying severity, dates spanning last 30d |
| `/owl` | Historical baseline sufficient. Trend charts show 11 weeks of data. Suspicious Steve at top of risk leaderboard. |
| `/fox` | One open case for Steve with 3+ evidence records, timeline events, and linked alerts |
| `/cash-drawer` | Recent shift history with reconciled + unreconciled shifts; variance events tied to Steve's shifts |
| `/employees` | 5 employees, Steve's risk trend graph ramping up across 11 weeks, others flat-low |
| `/metrics` or equivalent | `employee_daily_metrics`, `hourly_metrics`, `daily_metrics`, `entity_risk_scores`, `risk_score_history` — all populated across the full Feb-Apr window |

## Files on disk (verify before touching)

```
Canary/devops/seeds/level_b_demo.py          21,840 bytes  (old — two-DB split, hardcoded creds, unqualified tables)
Canary/canary/blueprints/square_oauth_wired.py               (reset endpoints already patched w/ belt-and-suspenders onboarded flip)
Canary/devops/scripts/test_reset.py                          (merchant_reset / factory_reset — leave untouched)
Canary/docs/MERCHANT_PROFILE.md                              (narrative source of truth — reference, don't edit)
```

## Schema delta since original seed

The seed was written when Canary had two databases. Current reality:

- **One DB** (`canary`), three schemas (`app`, `sales`, `metrics`).
- `app.merchants.merchant_id` was **renamed to `source_merchant_id`** (commit `7d723b9`).
- All table references need to be schema-qualified (`app.merchants`, `sales.transactions`, `metrics.employee_daily_metrics`) — the seed currently uses bare table names.
- Connection must use `growdirect` / `growdirect_dev` against DB `canary`, host from `SEED_PG_HOST` (inside Flask container → `postgres`; outside → `localhost`).
- `sales.transactions.created_at` and `updated_at` currently have a **hardcoded literal default** of `2026-04-01 04:33:12.27643`. The seed must pass explicit timestamps on every INSERT — never rely on the column default.

## Change 1 — Rewrite `devops/seeds/level_b_demo.py`

Replace the file. Keep the idempotent `ON CONFLICT DO NOTHING` pattern,
the stable seed IDs (so reseeding is deterministic), and the overall
structure. Change:

1. Single `conn()` function → one DB (`canary`), schema-qualified inserts.
2. Credential config reads env (`SEED_PG_USER=growdirect`, `SEED_PG_PASS=growdirect_dev`, `SEED_PG_DB=canary` defaults).
3. Rename every `INSERT INTO merchants` → `INSERT INTO app.merchants` etc.
4. Update `merchants` column — drop old `merchant_id`, use `source_merchant_id` where the old code used `merchant_id` for the external Square ID.
5. **New: timeline generation.** The seed generates data from **2026-02-01 00:00 PST** through **today (NOW() at seed time)**. Every INSERT passes explicit `created_at` and `transaction_date`. No reliance on column defaults.
6. **New: Steve's risk arc.** See story table above. The seed writes:
   - `sales.transactions` — ~40 transactions/market-day × 3 markets × 11 weeks ≈ 1,300 transactions. Saturdays heavy, weekdays lighter.
   - `sales.refund_links` — refund pairs mapped to the "Drift → Pattern → Active" progression above.
   - `sales.cash_drawer_shifts` + `sales.cash_drawer_events` — one shift per market-day per closing employee. Variance events tied to Steve's shifts in the Pattern/Active phases.
   - `app.alerts` — 8–12 dated across the Pattern/Active windows. Severity climbs with phase.
   - `app.alert_history` — state transitions for the closed alerts.
   - `app.fox_cases` + `app.fox_case_timeline` + `app.fox_evidence` — the Steve case, evidence linked to his rapid-refund + cash variance alerts.
   - `metrics.employee_daily_metrics` — one row per employee per day across the full window.
   - `metrics.hourly_metrics` + `metrics.daily_metrics` — aggregate rollups for the dashboard.
   - `metrics.entity_risk_scores` — current score per employee.
   - `metrics.risk_score_history` — daily risk score per employee across the full window so the trend graph draws.
   - `metrics.metric_baselines` — baseline rows so Owl doesn't re-bootstrap.

7. **New: idempotency.** The seed is safe to run multiple times. Use stable UUIDs derived from `uuid.uuid5(namespace, stable_name)` so the same inputs always produce the same IDs. `ON CONFLICT DO NOTHING` on every insert.
8. **New: clean-first mode.** A `--wipe` flag (or `clean_first=True` keyword) does `DELETE FROM ... WHERE merchant_id = '<demo-merchant-id>'` across every seeded table before inserting. This is what the reset endpoint will call.

## Change 2 — New importable entry point

In the rewritten seed, expose:

```python
def seed_demo(clean_first: bool = True) -> dict:
    """Idempotent demo reseeder. Returns dict with table-by-table row counts."""
```

`clean_first=True` deletes everything for the demo merchant (by `merchant_id`)
before inserting. `clean_first=False` keeps existing rows, skips on
conflict (useful for first-run bootstrap).

Never accept a merchant_id as an argument — the demo merchant is
hardcoded (`MERCHANT_ID = "demo-sq-farmers-market-0001"` at module top).
The reseeder only ever touches the demo merchant. Real merchants are
untouchable.

## Change 3 — Wire into the reset endpoint

In `Canary/canary/blueprints/square_oauth_wired.py`, the
`merchant_reset_endpoint` already exists. Add an optional reseed step:

```python
# After the existing merchant_reset + belt-and-suspenders onboarded flip:
if request.json and request.json.get("reseed"):
    try:
        from devops.seeds.level_b_demo import seed_demo
        seed_result = seed_demo(clean_first=True)
        logger.info("merchant-reset: reseeded demo, rows=%s", seed_result)
    except Exception as e:
        logger.error("merchant-reset: reseed failed: %s", e)
        # Don't fail the reset on reseed error — user still gets clean slate
```

In `templates/app/settings.html` where the reset button lives, add a
small checkbox next to the "Reset My Store" action: **"Reseed with demo
data"** — default ON in sandbox, hidden in prod. The existing JS (line
797–804) already POSTs to `/oauth/merchant-reset` — extend the body to
include `{reseed: checkbox.checked}`.

## Change 4 — Flip `onboarded=true` at seed end

After seeding succeeds, the reseeder sets `onboarded=true` and
`onboarded_at=now()` on the demo merchant's `app.merchant_sources` row.
This means: reset-with-reseed produces a **fully onboarded** merchant
who can land on `/home` directly with data — no welcome/HC flow needed.

If the user wants the welcome flow back, they do `?reseed=0` or uncheck
the box and the existing `/welcome` → Complete Setup path still runs.

## Change 5 — Integration test

`Canary/tests/integration/test_demo_reseed.py`:

```python
import pytest
from devops.seeds.level_b_demo import seed_demo, MERCHANT_ID

@pytest.mark.postgres
def test_reseed_idempotent(pg_session):
    r1 = seed_demo(clean_first=True)
    r2 = seed_demo(clean_first=True)
    assert r1 == r2  # row counts identical across runs

@pytest.mark.postgres
def test_reseed_populates_all_surfaces(pg_session):
    seed_demo(clean_first=True)
    for table, min_rows in [
        ("sales.transactions", 1000),
        ("app.alerts", 8),
        ("app.fox_cases", 1),
        ("app.fox_evidence", 3),
        ("metrics.employee_daily_metrics", 400),  # 5 emp * ~80d
        ("metrics.risk_score_history", 400),
    ]:
        count = pg_session.execute(
            f"SELECT count(*) FROM {table} WHERE merchant_id = %s",
            (MERCHANT_ID,),
        ).scalar()
        assert count >= min_rows, f"{table} had only {count}"

@pytest.mark.postgres
def test_reseed_steve_arc(pg_session):
    seed_demo(clean_first=True)
    # Steve's most recent risk score should be >= 0.70 (Active phase)
    steve_score = pg_session.execute(
        "SELECT risk_score FROM metrics.entity_risk_scores "
        "WHERE merchant_id = %s AND entity_id = 'demo-emp-suspicious-steve-001' "
        "AND entity_type = 'employee'",
        (MERCHANT_ID,),
    ).scalar()
    assert steve_score >= 0.70
    # Sofia should stay low
    sofia_score = pg_session.execute(
        "SELECT risk_score FROM metrics.entity_risk_scores "
        "WHERE merchant_id = %s AND entity_id = 'demo-emp-sofia-rodriguez-001'",
        (MERCHANT_ID,),
    ).scalar()
    assert sofia_score <= 0.20
```

## Verify locally

```bash
cd ~/GrowDirect/Canary
python3 devops/seeds/level_b_demo.py --wipe
# Expect: row count summary. Watch for any skip errors.

docker compose -f devops/docker-compose.localhost.yml exec flask \
  curl -s -X POST -H "Content-Type: application/json" \
       -d '{"reseed": true}' http://localhost:5001/oauth/merchant-reset
# Expect: {"ok": true, "redirect": "/auth/join"} — logs show "reseeded demo, rows={...}"

# Click-through:
#  open http://localhost:5001 in browser, Connect with Square, every screen populated.
```

## Out of scope

- Changing the OAuth callback flow (already as-designed in commit `7f5e907`).
- Editing `test_reset.py` — the `merchant_reset` / `factory_reset` functions keep their current behavior. Reseed is additive.
- Real Square API calls during reseed — seed is DB-only, no HTTP out.
- Multi-merchant demos. Only `MERCHANT_ID = "demo-sq-farmers-market-0001"` is seeded.
- Fixing `sales.transactions.created_at` / `updated_at` column defaults. Separate bug, separate GRO.
- Modernizing `devops/scripts/test_reset.py`'s per-table error handling (the `rows_purged=0` lie). Separate bug.
- The `DisputesClient.list(limit=...)` Square SDK mismatch in the onboarding pipeline. Separate bug.

## Known adjacent bugs to file as separate Linear issues

1. **`sales.transactions.created_at` has a hardcoded literal default.** Column default should be `now()` or `CURRENT_TIMESTAMP`. Migration required.
2. **`test_reset.py._purge_db_counts` silently swallows per-table errors** and reports `rows_purged=0`. Change to log per-table failures and return structured errors.
3. **`DisputesClient.list(limit=...)` Square SDK breaking change** in the onboarding pipeline initial_sync. Update kwarg.

## Linear

Create a parent issue under **Canary** project: "Demo reseed — restore
Level B Farmers Market story with multi-month timeline." Link this
dispatch in the description. File the three adjacent bugs above as
child issues (blocking? no — independent).

## Commit

One commit per Change. Four commits total:

```
feat(demo): rewrite level_b_demo.py for single-DB schema with 11-week timeline

Ports the Level B Saturday Farmers Market seed to the consolidated canary
DB (three schemas: app, sales, metrics). Adds a multi-month timeline from
2026-02-01 through NOW that tells Suspicious Steve's descent arc:
baseline → drift → pattern → active. Other employees stay clean.

- Schema-qualified inserts across all tables
- Explicit created_at / transaction_date on every row (no default reliance)
- Populates metrics tables so Owl baselines and risk trend graphs draw
- Idempotent via stable uuid5 IDs + ON CONFLICT DO NOTHING
- New --wipe flag (and seed_demo(clean_first=True) API) for reset path
- Stays DB-only, no Square API calls
```

```
feat(canary): wire demo reseed into /oauth/merchant-reset

Adds optional reseed=true flag to the merchant-reset endpoint. When set,
calls seed_demo(clean_first=True) after the wipe + onboarded flip, so
one POST produces a fully populated demo-ready merchant. Sandbox only.
UI checkbox on settings.html defaults ON in sandbox, hidden in prod.
```

```
test(canary): integration tests for demo reseed — idempotency + coverage + Steve arc

Three tests: two identical runs produce identical row counts; all screen
surfaces have minimum populated row counts; Steve's risk score clears
0.70 while Sofia stays under 0.20. Postgres-only (pg_session fixture).
```

```
docs(canary): MERCHANT_PROFILE.md — add timeline + Steve's phase table

Updates the narrative source-of-truth doc with the four-phase arc table
and the per-screen coverage table. Keeps the seed code and the story doc
in sync.
```

## Definition of done

1. `python3 devops/seeds/level_b_demo.py --wipe` runs clean, prints row-count summary, exits 0.
2. Running it twice produces identical row counts (idempotent).
3. POST `/oauth/merchant-reset` with `{"reseed": true}` reseeds the demo merchant in <10s.
4. After reseed, every screen in the table above is populated — no empty states.
5. Steve's risk score graph shows a rising trend across 11 weeks. Sofia's stays flat-low.
6. `pytest tests/integration/test_demo_reseed.py -m postgres` passes green.
7. All four commits pushed, parent Linear issue closed, three adjacent bugs filed as separate issues.
