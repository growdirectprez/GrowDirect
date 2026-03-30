# Test Lab & Scenario Runner

> **Status:** Complete — written from code
> **Namespace:** alx
> **Last updated:** 2026-03-30
> **Code location:** `Canary/canary/services/scenario_runner.py`, `Canary/canary/services/scenario_fire.py`, `Canary/canary/services/scenario_verify.py`, `Canary/canary/services/square_sandbox_seeder.py`, `Canary/canary/blueprints/ops_console.py`

---

## 1. Overview

The Test Lab is a developer-facing feature inside Canary's Ops Console that gives operators a controlled way to generate test data and verify that the full Canary pipeline — Square webhook ingestion, TSP parsing, Chirp rule evaluation, alert creation, Fox case escalation — responds correctly to known transaction patterns.

The system has two distinct execution modes with fundamentally different philosophies:

**Scenario Fire** (`scenario_fire.py`) creates real orders and payments against the Square sandbox API. Square fires webhooks back into Canary through the normal ingestion pipeline. No synthetic data is inserted. Every operation that enters the CRDM arrives via the TSP webhook path.

**Scenario Runner** (`scenario_runner.py`) inserts synthetic data directly into PostgreSQL via raw psycopg2, bypassing RLS and the ingestion pipeline entirely. It is used for two purposes: populating data for visual verification on the merchant dashboard ("Same Glass" pattern), and seeding cross-domain scenarios (timecards, cash drawer shifts, disputes) that cannot be created through the Square API.

A third component, the **Sandbox Seeder** (`square_sandbox_seeder.py`), prepopulates the Square sandbox environment itself with team members and catalog items that scenario fire scripts expect to exist when constructing orders.

After a scenario fires, **Scenario Verify** (`scenario_verify.py`) confirms the expected data landed in the CRDM by running parameterized SQL queries and comparing row counts against per-scenario thresholds.

The Ops Console is sandbox-only. All routes under `/ops/` are blocked unless `SQUARE_ENVIRONMENT == "sandbox"` and the requesting user has an authenticated session with admin role.

---

## 2. Architecture

### Component Diagram

```
Ops Console UI (/ops/)
        |
        | HTTP POST
        v
canary/blueprints/ops_console.py  (sandbox guard + Flask routes)
        |
        +-- /api/scenario/fire       --> scenario_fire.fire_scenario()
        |                                    |
        |                                    +--> chirp_lab.live_fire_order()     --> Square Orders API
        |                                    +--> chirp_lab.live_fire_transaction() --> Square Payments API
        |                                    +--> scenario_fire._create_refund()  --> Square Refunds API
        |                                    +--> cancel_payment()               --> Square Payments API
        |                                    +--> use_case factories (DB seed)   --> PostgreSQL (direct)
        |
        +-- /api/scenario/batch      --> scenario_fire.batch_fire()
        |
        +-- /api/scenario/poll/:id   --> chirp_lab.live_fire_poll()
        |                                    |
        |                                    +--> ingestion_log (did webhook arrive?)
        |                                    +--> sales.transactions (did TSP parse it?)
        |                                    +--> app.alerts (did Chirp fire?)
        |
        +-- /api/scenario/verify-owl --> scenario_verify.run_verification_queries()
        |                                    |
        |                                    +--> SQLAlchemy + direct SQL (no ORM)
        |                                    +--> Joins through transaction_tenders on poll_ids
        |
        +-- /api/sandbox/seed        --> square_sandbox_seeder.SquareSandboxSeeder.seed_all()
        |                                    |
        |                                    +--> Square /team-members API
        |                                    +--> Square /catalog/batch-upsert API
        |
        +-- /api/sandbox/team-members --> seeder.get_team_member_ids()
        +-- /api/sandbox/locations    --> seeder.get_locations()
        |
        +-- /api/scenario/thresholds  --> chirp.rule_definitions.RULE_MAP
        +-- /api/scenario/threshold   --> merchant_rule_config (SQLAlchemy write)

Randomizer (scenario_runner.py) — called from ops_console for "Generate Random" button
        |
        +--> psycopg2 direct connection to canary DB
        +--> Inserts into sales.transactions, app.alerts with sc- prefix IDs
```

### Request / Data Flow

**Scenario Fire flow (real Square API path):**

1. UI sends `POST /ops/api/scenario/fire` with `{"scenario": "refund_detection"}`.
2. `ops_console.api_scenario_fire()` calls `scenario_fire.fire_scenario("refund_detection")`.
3. `fire_scenario` loads the scenario definition from `SCENARIO_REGISTRY` and resolves default `team_member_id` and `location_id` from `EmployeeLocationAssignment` (primary employee/location pair from CRDM).
4. Each step in the scenario's `steps` list is dispatched:
   - `action: "order"` calls `live_fire_order()` from `chirp_lab`, which creates an Order via Square Orders API then attaches a Payment via Square Payments API.
   - `action: "payment"` calls `live_fire_transaction()` for a simple payment with no order.
   - `action: "refund"` or `"partial_refund"` calls `_create_refund()` against Square Refunds API, referencing the `payment_id` recorded from a prior step.
   - `action: "cancel"` calls `cancel_payment()` to void a completed payment.
   - `action: "seed"` calls a use-case factory function from `tests/fixtures/use_cases` that inserts timecard, cash drawer, dispute, or loyalty records directly into the CRDM via the ORM session. Used for cross-domain scenarios where no Square API equivalent exists.
   - `action: "wait"` sleeps for `seconds` to put a temporal gap between steps (e.g., the C-502 post-void scenario needs a 3-minute gap to land in the WATCH tier).
5. `fire_scenario` returns `{ok, scenario, steps, poll_ids, step_count, elapsed_seconds, detail}`. The `poll_ids` list contains Square payment IDs and refund IDs that entered the pipeline.
6. `ops_console` caches `poll_ids` server-side in `_last_fire_poll_ids[scenario_name]` to survive stale browser state.
7. UI polls `GET /ops/api/scenario/poll/<payment_id>` to track pipeline completion (webhook arrived, TSP parsed, alerts fired).
8. UI sends `POST /ops/api/scenario/verify-owl` with `{scenario, poll_ids}` to confirm expected outcomes. `scenario_verify.run_verification_queries()` runs parameterized SQL against PostgreSQL, joining through `sales.transaction_tenders` on `payment_id` to match the exact transactions created by this scenario run.

**Scenario Runner / Randomizer flow (synthetic data path):**

1. UI sends a request to run a named scenario or the randomizer.
2. `scenario_runner.run_scenario(name)` or `run_randomizer(count)` opens a raw psycopg2 connection to the `canary` database.
3. Records are inserted directly into `sales.transactions`, `sales.cash_drawer_shifts`, and `app.alerts` using `INSERT ... ON CONFLICT DO NOTHING`.
4. All generated IDs use the `sc-` prefix (`sc-txn-sale-{hex8}`, `sc-alert-c001-{hex8}`, etc.).
5. No webhook, no TSP, no Chirp. The rule engine is not invoked — alerts are seeded directly.

**Sandbox Seeder flow:**

1. `SquareSandboxSeeder` connects to the Square sandbox API directly (not through the Canary webhook path).
2. `ensure_team_members()` searches for existing team members by name, then creates any that are missing using the Payments API `/team-members` endpoint with idempotency keys.
3. `ensure_round_dollar_catalog()` and `ensure_full_catalog()` batch-upsert catalog items using `/catalog/batch-upsert`.
4. All operations are idempotent — safe to run multiple times.

### Key Design Decisions

**Two modes are not an accident.** Scenario Fire validates the real pipeline end-to-end, including webhook HMAC verification, TSP parsing, and Chirp evaluation. This is necessary for regression testing the actual production code path. Scenario Runner fills the gap for data that cannot be created through Square APIs — timecards, cash drawer events, disputes, loyalty records — and for quickly populating the merchant dashboard without waiting for webhooks.

**Raw psycopg2 in the runner bypasses RLS.** This is intentional. Row-Level Security policies on the `canary` database restrict queries to the currently authenticated merchant. Test data insertion is an admin operation outside the normal request context and must run without a merchant session active. The ORM session relies on `set_current_merchant()` being called at request time — the scenario runner operates outside of Flask requests. See Section 7 for security details.

**`sc-` prefix isolation.** Every ID generated by the runner carries a `sc-` prefix. This makes purge operations trivial: `DELETE FROM table WHERE id LIKE 'sc-%'`. Seed data uses `demo-*` prefixes and is never touched by purge. Square-origin data has Square IDs and is never touched either.

**`poll_ids` for exact verification.** The verify step does not query "last 10 transactions" or "transactions today." It receives the exact Square `payment_id` and `refund_id` values returned by the fire step, then joins through `sales.transaction_tenders` to match the precise rows created by this scenario run. This prevents false positives from earlier test runs or production data.

**Server-side `poll_ids` cache.** `_last_fire_poll_ids` in `ops_console.py` is an in-process dict keyed by scenario name. It exists because browser cache can serve stale JavaScript that does not include `poll_ids` in the verify POST body. The server cache ensures verify always has the IDs from the most recent fire of each scenario.

---

## 3. Data Model

The Test Lab has no models of its own. It writes to existing CRDM tables. The relevant tables and the data shape written by the runner are documented below.

### Scenario-Prefixed ID Format

```
sc-{type}-{uuid4_hex[:8]}

Examples:
  sc-txn-sale-a3f2b1c4       (transaction, type=SALE)
  sc-txn-rfnd-7e8d4a9b       (transaction, type=REFUND)
  sc-alert-c001-2d5f6e3a     (alert, rule C-001)
  sc-case-f4b2c7d1           (Fox case)
  sc-shift-9c3e8a2f          (cash drawer shift)
  sc-evid-1a4b7e6c           (Fox evidence)
  sc-tl-5f2d9c3b             (Fox case timeline entry)
```

Maximum length: `sc-{12}-{8}` = 25 characters, fits in `varchar(36)`.

### Tables Written

**`sales.transactions`** (scenario runner + randomizer)

| Column | Value written |
|--------|--------------|
| `id` | `sc-txn-{type}-{hex8}` |
| `merchant_id` | `demo-sq-farmers-market-0001` (fixed demo merchant) |
| `external_id` | `SQ_SCN_{hex8}` or `SQ_RND_{hex8}` |
| `location_id` | One of the three demo location IDs |
| `employee_id` | One of the five demo employee IDs |
| `transaction_type` | `SALE`, `REFUND`, or `VOID` |
| `transaction_date` | UTC now, optionally backdated by minutes |
| `amount_cents` | Integer, from `CATALOG_ITEMS` or `ROUND_DOLLAR_CATALOG` |
| `source_type` | `"SCENARIO"` |
| `tax_amount_cents`, `discount_amount_cents`, `tip_amount_cents` | `0` |
| `currency` | `"USD"` |
| `created_at`, `updated_at` | UTC now |

**`sales.cash_drawer_shifts`** (cash drawer variance scenario only)

| Column | Value written |
|--------|--------------|
| `id` | `sc-shift-{hex8}` |
| `square_shift_id` | `SQ_SHIFT_SCN_{hex8}` |
| `state` | `"CLOSED"` |
| `opened_at` | 5 hours before close |
| `starting_cash_cents` | `20000` ($200 float) |
| `cash_variance_cents` | Negative, $21–$50 range |

**`app.alerts`** (runner injects for scenarios with `expected_rules`)

| Column | Value written |
|--------|--------------|
| `id` | `sc-alert-{rule}-{hex8}` |
| `rule_id` | e.g. `"C-001"`, `"C-102"` |
| `alert_type` | e.g. `"RAPID_REFUND"`, `"CASH_VARIANCE"` |
| `severity` | `"high"` or `"medium"` |
| `source_table` | `"transactions"` or `"cash_drawer_shifts"` |
| `source_id` | ID of the related transaction/shift |
| `details` | JSON blob with human-readable explanation and threshold values |
| `created_by` | `"scenario_runner"` |

**`app.fox_cases`**, **`app.fox_case_timeline`**, **`app.fox_evidence`** (fox lifecycle and pipeline e2e scenarios only)

Fox cases get `sc-case-{hex8}` IDs. Case numbers are formatted `CASE-{year}-{5-digit-random}`. Evidence records include a real SHA-256 hash of synthetic content and set `previous_chain_hash` / `chain_hash` to `"TRIGGER_WILL_SET"` — the database trigger is expected to compute the final hash chain on insert.

### Scenario Registry Shape (scenario_fire.py)

Each entry in `SCENARIO_REGISTRY` is a Python dict:

```python
{
    "name": str,                  # Display name for the UI
    "description": str,           # Single-sentence explanation
    "tests_rules": List[str],     # Rule IDs expected to fire (e.g. ["C-001"])
    "steps": List[dict],          # Ordered list of actions (see Step Shape below)
    "expected_rules": List[str],  # Rules that must appear in verify results
    "verification_queries": [     # Queries run by scenario_verify
        {"query": str, "expect_min": int}
    ],
}
```

**Step shape by action type:**

`order` — creates an order with line items via Square Orders API, then attaches a payment:
```python
{
    "action": "order",
    "label": str,
    "line_items": [{"name": str, "quantity": str, "base_price_cents": int}],
    "discounts": [{"name": str, "amount_cents": int}],  # optional
    "tip_cents": int,
    "nonce": str,           # "success" | "declined" | "gift_card"
    "skip_payment": bool,   # create order but no payment (C-204 untendered)
    "autocomplete": bool,   # default True; False keeps order in OPEN state
    "team_member_id": str,  # optional override; falls back to primary employee
    "location_id": str,     # optional override; falls back to primary location
}
```

`payment` — simple payment without an order:
```python
{
    "action": "payment",
    "label": str,
    "amount_cents": int,
    "tip_cents": int,
    "nonce": str,
}
```

`refund` / `partial_refund` — refund against a prior step's payment:
```python
{
    "action": "refund",           # or "partial_refund"
    "label": str,
    "refund_step": int,           # zero-based index of the step that created the payment
    "delay_seconds": int,         # optional sleep before executing
    "refund_amount_cents": int,   # partial_refund only; full amount used if absent
}
```

`cancel` — void a completed payment:
```python
{
    "action": "cancel",
    "label": str,
    "cancel_step": int,           # zero-based index of the payment to cancel
}
```

`seed` — insert cross-domain data via use-case factory:
```python
{
    "action": "seed",
    "label": str,
    "seed_fn": str,  # function name in tests/fixtures/use_cases
}
```

`wait` — pause between steps:
```python
{
    "action": "wait",
    "label": str,
    "seconds": int,
}
```

### Scenario Registry Shape (scenario_runner.py)

The runner has its own `SCENARIOS` dict with a simpler structure (no `steps` list):

```python
{
    "name": str,
    "desc": str,
    "expected_rules": List[str],
    "verification_queries": [{"query": str, "expect_min": int}],
}
```

The runner dispatches to named Python functions (`_scenario_happy_path`, etc.) rather than executing a declarative step list.

---

## 4. Interfaces

### HTTP Endpoints

All routes are registered on `ops_console_bp` with URL prefix `/ops/`. All routes require sandbox environment and an authenticated admin session (enforced by `ops_guard` `before_request`).

---

**`GET /ops/`** — Renders the Test Lab single-page Jinja2 template. The template includes the scenario picker, live fire controls, and verification output panels.

---

**`POST /ops/api/scenario/fire`**

Fire a named scenario against the Square sandbox API.

Request body:
```json
{"scenario": "refund_detection"}
```

Response (success):
```json
{
  "ok": true,
  "scenario": "refund_detection",
  "scenario_name": "Rapid Refund (C-001)",
  "steps": [
    {
      "action": "order",
      "label": "Crystal set sale",
      "amount_cents": 2798,
      "line_items": 2,
      "discounts": 0,
      "payment_id": "3x7yZABC...",
      "order_id": "wBqRDE...",
      "status": "COMPLETED"
    },
    {
      "action": "refund",
      "label": "Immediate full refund",
      "payment_id": "3x7yZABC...",
      "refund_id": "rKlmNO...",
      "amount_cents": 2798,
      "status": "PENDING"
    }
  ],
  "poll_ids": ["3x7yZABC...", "rKlmNO..."],
  "step_count": 2,
  "elapsed_seconds": "12.4",
  "detail": "1 order + 1 refund created"
}
```

Response (error):
```json
{"ok": false, "error": "Unknown scenario: bad_name", "available": [...]}
```

---

**`POST /ops/api/scenario/batch`**

Fire multiple scenarios sequentially.

Request body:
```json
{"scenarios": ["happy_path_payment", "refund_detection"]}
```

Omit `scenarios` to fire all scenarios in `SCENARIO_REGISTRY`.

Response:
```json
{
  "ok": true,
  "results": {
    "happy_path_payment": { ... },
    "refund_detection": { ... },
    "_summary": {"total": 2, "succeeded": 2, "failed": 0}
  }
}
```

Individual scenario failures do not abort the batch.

---

**`GET /ops/api/scenario/poll/<payment_id>`**

Poll the pipeline status for a single Square payment ID. Checks three sources in order: `ingestion_log` (did the webhook arrive?), `sales.transactions` (did TSP parse it?), `app.alerts` (did Chirp fire any alerts for it?).

Response:
```json
{
  "ok": true,
  "payment_id": "3x7yZABC...",
  "ingested": true,
  "transaction_id": "uuid-...",
  "alerts": [{"rule_code": "C-001", "severity": "high"}],
  "pipeline_complete": true
}
```

---

**`POST /ops/api/scenario/verify-owl`**

Run SQL verification queries for a completed scenario fire. Compares actual row counts against `expect_min` thresholds defined in `SCENARIO_REGISTRY`.

Request body:
```json
{
  "scenario": "refund_detection",
  "poll_ids": ["3x7yZABC...", "rKlmNO..."]
}
```

If `poll_ids` is absent or empty, the server uses the cached `_last_fire_poll_ids[scenario]` value. If no poll IDs are available for transaction queries, the query falls back to date-scoped results (today).

Response:
```json
{
  "ok": true,
  "scenario": "refund_detection",
  "all_passed": true,
  "results": [
    {
      "query": "refunds today",
      "expect_min": 1,
      "actual_count": 1,
      "passed": true,
      "sql": "SELECT DISTINCT t.id ...",
      "params": {"pid_0": "rKlmNO..."},
      "rows": [{"id": "...", "transaction_type": "RETURN", ...}],
      "query_time_ms": 4.2,
      "error": null
    }
  ]
}
```

---

**`GET /ops/api/scenario/thresholds`**

Returns current threshold values for all rules referenced by any scenario in `SCENARIO_REGISTRY`. Merges `detection_rules` defaults with `merchant_rule_config` overrides for the authenticated merchant.

---

**`POST /ops/api/scenario/threshold`**

Update a single rule's threshold for the authenticated merchant.

Request body:
```json
{"rule_id": "C-001", "key": "seconds", "value": 600}
```

---

**`GET /ops/api/sandbox/team-members`**

Query the Square sandbox for existing team members. Used to populate the employee dropdown in the fire UI.

Response:
```json
{"ok": true, "team_members": [{"name": "Sofia Rodriguez", "id": "TM_..."}]}
```

---

**`GET /ops/api/sandbox/locations`**

Query the Square sandbox for configured locations.

Response:
```json
{"ok": true, "locations": [{"id": "L...", "name": "Torrance Farmers Market", "status": "ACTIVE"}]}
```

---

**`POST /ops/api/sandbox/seed`**

Run the sandbox seeder (team members + round-dollar catalog). Idempotent.

Response:
```json
{
  "ok": true,
  "results": {
    "team_members": {"created": 2, "skipped": 2, "errors": 0},
    "round_dollar_catalog": {"created": 6, "skipped": 0, "errors": 0}
  }
}
```

---

### Programmatic API (Python)

**`scenario_fire.fire_scenario(scenario_name: str) -> Dict`**

Execute a named scenario. Returns the same shape as the HTTP endpoint.

**`scenario_fire.batch_fire(scenario_keys: List[str]) -> Dict`**

Fire multiple scenarios sequentially, continuing on individual failures. Returns per-scenario results plus `_summary`.

**`scenario_runner.run_scenario(scenario_name: str) -> Dict`**

Execute a named synthetic-data scenario. Returns `{ok, transactions, alerts, detail, verify}`.

**`scenario_runner.run_randomizer(count: int) -> Dict`**

Generate `count` random transactions (capped at 50). Returns `{ok, transactions, alerts, detail}`.

**`scenario_runner.purge_scenario_data() -> Dict`**

Delete all rows with `id LIKE 'sc-%'` from all target tables. Disables and re-enables triggers around the delete to bypass immutability constraints. Blocked in production environments by an env check. Returns per-table deletion counts.

**`scenario_runner.get_scenario_counts() -> Dict`**

Count live scenario rows across all tables. Returns per-table counts plus `total`.

**`scenario_runner.reseed_baseline() -> Dict`**

Invoke `devops/seeds/level_b_demo.py` via subprocess to reset baseline demo data.

**`square_sandbox_seeder.SquareSandboxSeeder(dry_run=False)`**

Construct a seeder instance. Raises `RuntimeError` if `SQUARE_ENVIRONMENT != "sandbox"` or `SQUARE_ACCESS_TOKEN` is not set.

**`SquareSandboxSeeder.seed_all() -> Dict[str, SeedResult]`**

Run `ensure_team_members()` and `ensure_round_dollar_catalog()`. Returns `{phase: SeedResult}`.

**`SquareSandboxSeeder.get_team_member_ids() -> Dict[str, str]`**

Return `{display_name: square_team_member_id}` for all team members currently in the sandbox.

**`SquareSandboxSeeder.get_locations() -> List[Dict[str, str]]`**

Return `[{id, name, status}]` for all Square locations.

---

## 5. Service Layer

### scenario_fire.py

The primary service for Scenario Fire mode. Contains:

- **`SCENARIO_REGISTRY`** — The authoritative registry of all runnable scenarios. 20+ entries covering payment rules (C-001 through C-008), order rules (C-201 through C-204), void rules (C-502), cash drawer rules (C-101, C-102), timecard rules (C-301, C-302), gift card rules (C-601, C-602), loyalty rules (C-802, C-803), dispute rules (C-D01 through C-D03), and composite scenarios (pipeline_e2e, high_risk_day, busy_register).

- **`fire_scenario(scenario_name)`** — Dispatches a scenario by iterating its `steps` list. Before executing steps, resolves default `team_member_id` and `location_id` from `EmployeeLocationAssignment` via ORM query. Tracks `payment_ids_by_step` and `amounts_by_step` as it progresses so that later `refund`/`cancel` steps can reference earlier payments by step index. Returns `poll_ids` (Square IDs of created payments and refunds for pipeline tracking).

- **`batch_fire(scenario_keys)`** — Sequential batch execution. Catches and records individual scenario failures without aborting the batch. Returns per-scenario results and a `_summary` dict.

- **`_create_refund(client, payment_id, amount_cents)`** — Issues a refund via `client.refunds.refund_payment()`. Requires `amount_cents` to be explicitly provided by the caller (computed from `amounts_by_step` in `fire_scenario`). Raises `RuntimeError` on zero or missing amount to prevent silent full-amount refunds.

### scenario_runner.py

The synthetic data insertion service. Contains:

- **`SCENARIOS`** — Metadata registry for the runner's named scenarios (8 scenarios). Separate from `scenario_fire.SCENARIO_REGISTRY`.

- **`run_scenario(scenario_name)`** — Dispatches to one of the named Python functions via a lookup dict. Each function opens a psycopg2 connection, inserts records, commits, and returns a summary dict.

- **Individual scenario functions** — `_scenario_happy_path`, `_scenario_refund_detection`, `_scenario_void_pattern`, `_scenario_cash_drawer_variance`, `_scenario_employee_risk`, `_scenario_multi_location`, `_scenario_fox_lifecycle`, `_scenario_pipeline_e2e`. Each seeds a specific data pattern for visual verification on the merchant dashboard.

- **`run_randomizer(count)`** — Generates random transactions with weighted probability:
  - 60% normal sales (`SALE`)
  - 15% rapid refund pairs (`SALE` + `REFUND`); generates C-001 alert when gap <= 15 minutes
  - 10% void transactions (`VOID`)
  - 10% after-hours transactions; always generates C-004 alert
  - 5% high-value refunds ($100–$500); always generates C-007 alert

  All records inserted in a single connection with a final `commit()`.

- **`purge_scenario_data()`** — Iterates all target tables in FK-safe delete order (evidence → timeline → cases → alerts → transactions/shifts). Disables triggers with `ALTER TABLE ... DISABLE TRIGGER ALL`, deletes `WHERE id LIKE 'sc-%'`, then re-enables in a `finally` block. The production environment guard is checked redundantly before and inside the trigger-manipulation block.

- **Helper functions** — `_conn(db)` opens a psycopg2 connection using env vars (`SEED_PG_HOST`, `PG_HOST`, `PG_PORT`, `PG_USER`, `PG_PASS`). `_insert(cur, table, row)` executes a parameterized `INSERT ... ON CONFLICT DO NOTHING`. `_scenario_id(prefix)` generates `sc-{prefix}-{hex8}` IDs.

### scenario_verify.py

Post-fire verification service. Contains:

- **`run_verification_queries(queries, merchant_id, poll_ids)`** — Iterates the `verification_queries` list from a scenario's registry entry. For each query, calls `_build_verify_sql` to get parameterized SQL, executes it against the CRDM using SQLAlchemy, and compares `actual_count >= expect_min`.

  Before each query, sets `statement_timeout = '5000'` and calls `set_current_merchant(:mid)` to establish the RLS context. Results include the raw SQL, row previews (up to 25), query time, and pass/fail.

- **`_build_verify_sql(query_label, merchant_id, poll_ids)`** — Maps named query labels to SQL templates. Supported labels: `"last transaction"`, `"refunds today"`, `"how many transactions today"`, `"high severity alerts"`. When `poll_ids` are present, transaction queries join through `sales.transaction_tenders tt ON tt.transaction_id = t.id` and filter by payment ID, order ID, or tender payment ID via `IN` clause. Alert queries always scope to today — there is no payment-to-alert join path.

- **`_poll_id_params(poll_ids, params)`** — Generates named SQLAlchemy bind parameter placeholders (`pid_0`, `pid_1`, ...) and mutates `params` in place.

### square_sandbox_seeder.py

Idempotent Square sandbox population service. Contains:

- **`SquareSandboxSeeder`** — Wraps `requests` calls to `https://connect.squareupsandbox.com/v2` with the `Authorization: Bearer {token}` header and Square-Version `2025-01-23`. The `_api(method, path, data)` helper returns the parsed JSON response body or `None` on HTTP error (warning logged).

- **`ensure_team_members()`** — Searches existing team members by `POST /team-members/search`, builds a name-to-id map, creates missing members one at a time. Returns `SeedResult` with `created`, `skipped`, `errors`, and `ids`.

- **`_ensure_catalog_items(items, category)`** — Searches existing catalog items by `POST /catalog/search`, builds a set of existing names, then batch-upserts missing items using `POST /catalog/batch-upsert`. Each item gets a client-side temporary ID (`#item-{sku}`) for the upsert operation.

- **`SeedResult` dataclass** — `created: int`, `skipped: int`, `errors: int`, `ids: Dict[str, str]`, `total` (computed property).

- **CLI entry point** — `python3 -m canary.services.square_sandbox_seeder [--dry-run] [--team] [--catalog] [--full-catalog] [--all]`. Loads `.env` from project root when run standalone.

**Fixed team members:**
| Name | Email | Role |
|------|-------|------|
| Sofia Rodriguez | sofia@growdirect.io | shift_lead |
| James Chen | james@growdirect.io | cashier |
| David Thompson | david@growdirect.io | cashier |
| Alejandro Castillo | alex@growdirect.io | weekend |

**Fixed catalog items:** 15 standard items (sage bundles, crystals, candles, oils, etc.) plus 6 round-dollar items (Market Gift Cards: $5–$50 in $5/$10/$15/$20/$25/$50 denominations). Round-dollar items are specifically priced for C-003 (ROUND_AMOUNT_PATTERN) testing.

---

## 6. Configuration

### Environment Variables

| Variable | Source | Purpose |
|----------|--------|---------|
| `SQUARE_ENVIRONMENT` | `.env` | Must be `"sandbox"` for all Test Lab operations. `ops_guard` blocks requests and `SquareSandboxSeeder` raises if this is not set. |
| `SQUARE_ACCESS_TOKEN` | `.env` | Bearer token for Square API calls. Required by both scenario_fire (via `_get_square_client()`) and `SquareSandboxSeeder`. |
| `SEED_PG_HOST` | `.env` | PostgreSQL host for the scenario runner psycopg2 connection. Falls back to `PG_HOST`, then `"postgres"`. |
| `PG_PORT` | `.env` | PostgreSQL port. Default `5432`. |
| `PG_USER` | `.env` | Database user. Default `"canary"`. |
| `PG_PASS` / `PG_PASSWORD` | `.env` | Database password. Default `"canary_dev_2026"`. |
| `CANARY_ENV` | `.env` | Checked by `purge_scenario_data()` — blocks trigger manipulation and purge in `production`. |

### Reference IDs

The scenario runner and randomizer use hardcoded reference IDs that match the demo data seeded by `devops/seeds/level_b_demo.py`:

**Merchant:** `demo-sq-farmers-market-0001`

**Locations:**
- `demo-loc-torrance-farmers-0001` (Torrance Farmers Market)
- `demo-loc-redondo-farmers-0001` (Redondo Beach Farmers Market)
- `demo-loc-rollinghills-0001` (Rolling Hills Market)

**Employees:**
- `demo-emp-suspicious-steve-001` (used for scenarios that should trigger alerts)
- `demo-emp-sofia-rodriguez-001`
- `demo-emp-alejandro-castillo-01`
- `demo-emp-james-chen-00000001`
- `demo-emp-david-thompson-00001`

### Square API Version

The seeder targets Square API version `2025-01-23` via the `Square-Version` request header. Scenario fire uses the Square Python SDK (version pinned in `requirements.txt`); the SDK version determines the API version used for Orders, Payments, and Refunds.

---

## 7. Security & Compliance

### Sandbox Guard

The `ops_guard` function registered as `before_request` on `ops_console_bp` returns `403` if `SQUARE_ENVIRONMENT != "sandbox"`. This is a process-level guard — the ops console cannot be reached in production environments regardless of auth state.

`SquareSandboxSeeder.__init__` performs the same check and raises `RuntimeError` immediately if instantiated outside sandbox. This prevents the seeder from being called programmatically in production even if the route guard is bypassed.

### Raw psycopg2 and RLS Bypass

The scenario runner and randomizer use raw psycopg2 connections rather than the SQLAlchemy ORM. This bypasses Row-Level Security entirely: the connection authenticates as the `canary` database user (not through the per-request `set_current_merchant()` RLS context used by the ORM).

This is acceptable for the following reasons:

1. **Operations are sandbox-only.** `purge_scenario_data()` blocks in production via the `CANARY_ENV` check. The Ops Console routes are blocked at the Flask level by `ops_guard`. There is no code path that runs the scenario runner against production data.

2. **Writes are restricted to scenario-prefixed IDs.** The runner only inserts rows with `sc-` prefix IDs and reads nothing from the database. It cannot access or modify existing merchant data.

3. **The demo merchant ID is hardcoded.** All scenario runner inserts target `MERCHANT_ID = "demo-sq-farmers-market-0001"`. Production merchant data is never in scope.

4. **The RLS bypass is necessary by design.** Scenario seeding is an admin operation that runs outside of a merchant request context. The ORM pattern requires `set_current_merchant()` to be called within a Flask request — the runner cannot satisfy this requirement.

The `purge_scenario_data()` function additionally uses `ALTER TABLE ... DISABLE TRIGGER ALL` to bypass immutability triggers on tables like `app.alerts` and `app.fox_evidence`. This is necessary because those tables have insert-only triggers that prevent deletion. The triggers are always re-enabled in a `finally` block.

### Authentication

All Ops Console routes require a valid Flask-Login session. The `load_session_user()` call in `ops_guard` redirects unauthenticated requests to `/auth/login-page`. There is no API key or token-only access path for the Test Lab.

### Square Credentials

`SQUARE_ACCESS_TOKEN` is read from environment/`.env` at instantiation time. It is never logged. The seeder's `_api()` helper logs HTTP errors but does not log request bodies or auth headers.

---

## 8. Error Handling

### Scenario Fire

Individual step failures within a scenario are caught and recorded in the `steps` list with `"status": "ERROR"` and an `"error"` field. The scenario returns `"ok": true` even if some steps failed — the caller can inspect individual step statuses. Exceptions from `_get_square_client()` are a fatal error that returns `"ok": false` immediately before any steps are attempted.

Declined payment steps (nonce `"declined"`) are treated as expected failures: the step is recorded as `"status": "DECLINED"` and the scenario continues normally.

`batch_fire` wraps each individual `fire_scenario()` call in a try/except. Per-scenario exceptions do not abort the batch. The `_summary.failed` count includes both explicit `ok=false` results and uncaught exceptions.

### Scenario Runner

Each scenario function propagates exceptions back to `run_scenario()`, which catches them and returns `{"ok": false, "error": str(e)}`. psycopg2 connection errors (e.g., database unreachable) will bubble up as errors in the response.

The randomizer operates in a single transaction per `_conn()` call. If the `c.commit()` fails, the entire batch of random transactions is rolled back.

### Sandbox Seeder

`_api()` returns `None` on HTTP errors (non-200/201 responses) and logs a warning. Callers check for `None` returns and increment `result.errors`. The seeder continues past individual failures — if one team member create fails, it proceeds to the next.

### Scenario Verify

Each verification query result includes an `"error"` field (normally `None`). SQL execution failures are caught, logged, and returned as `{"passed": false, "actual_count": 0, "error": str(e)}`. The overall `"all_passed"` key in the verify response reflects whether all queries passed; a single failed query sets it to `False`.

A `statement_timeout` of 5 seconds is set for each verification query to prevent long-running queries from blocking the UI.

---

## 9. Testing

The Test Lab services have no dedicated unit test files in `tests/unit/` or `tests/integration/`. Coverage is exercised indirectly:

- `scenario_runner.py` is exercised by running it manually via the Ops Console or by calling `run_scenario()` / `run_randomizer()` in dev.
- `scenario_fire.py` requires an active Square sandbox environment and live network access; it cannot run in the standard pytest test suite.
- `scenario_verify.py` is exercised by the verify step after a fire, not by isolated unit tests.
- `square_sandbox_seeder.py` can be invoked from the CLI with `--dry-run` to validate the logic without writing to Square.

The use-case factory functions imported by `scenario_fire` for `"seed"` action steps (`seed_uc02_off_clock_ghost`, `seed_uc05_cash_drawer_manipulation`, etc.) are defined in `tests/fixtures/use_cases` and are tested as part of the fixture layer for integration tests.

---

## 10. Dependencies

### Upstream

| Dependency | Usage |
|------------|-------|
| Square Sandbox API (`connect.squareupsandbox.com/v2`) | All Scenario Fire operations: create orders, payments, refunds, cancel payments; seed team members and catalog items |
| `canary.services.health_check.chirp_lab` | `live_fire_order()`, `live_fire_transaction()`, `cancel_payment()`, `_get_square_client()` — imported at call time inside `fire_scenario()` |
| `canary.db.session_factory.get_session` | SQLAlchemy session for `EmployeeLocationAssignment` lookup and scenario verify queries |
| `canary.models.app.employee_links.EmployeeLocationAssignment` | Resolve default `team_member_id` / `location_id` before executing scenario steps |
| `canary.models.app.employees.Employee` | Join for employee-location lookup |
| `canary.models.app.locations.Location` | Join for employee-location lookup |
| `canary.services.chirp.rule_definitions.RULE_MAP` | Fetch threshold definitions for the `/api/scenario/thresholds` endpoint |
| `tests.fixtures.use_cases` | Cross-domain seed functions for `"seed"` action steps |
| `psycopg2` | Direct database connection for scenario runner and randomizer |
| `requests` | HTTP client for sandbox seeder Square API calls |
| Flask `g.merchant_id` | Merchant context for scenario verify queries |

### Downstream

| Consumer | Dependency |
|----------|------------|
| Ops Console UI (`/ops/` template) | Renders scenario list, fire controls, poll progress, and verify results from these services |
| Canary pipeline (TSP, Chirp) | Scenario fire creates real Square orders/payments; Square webhooks enter the TSP → Chirp pipeline |
| `app.alerts`, `sales.transactions`, `app.fox_cases`, etc. | Written by scenario runner and fire pipeline |

### Shared Infrastructure

| Resource | Usage |
|----------|-------|
| `growdirect_postgres` (canary database) | Both psycopg2 (runner) and SQLAlchemy (verify, employee lookup) connect here |
| `growdirect_valkey` | Used by Flask session (authentication); not used directly by Test Lab services |

---

## 11. Known Issues & Reconciliation

### Code Location: Flat Services Root

The three Test Lab services (`scenario_runner.py`, `scenario_fire.py`, `scenario_verify.py`) live directly under `canary/services/` rather than in a dedicated `canary/services/test_lab/` subdirectory. This is inconsistent with the platform's Microservice Delivery Pattern, which calls for `canary/services/<service_name>/` with `__init__.py`, `service.py`, `routes.py`, and `models.py`.

**Impact:** Imports are stable and functional. The flat layout creates no runtime bugs. However, it makes the boundary between Test Lab services and production services less obvious, and the routes live in `ops_console.py` rather than a service-local `routes.py`.

**Recommended resolution:** Consolidate into `canary/services/test_lab/` with:
- `test_lab/runner.py` (from `scenario_runner.py`)
- `test_lab/fire.py` (from `scenario_fire.py`)
- `test_lab/verify.py` (from `scenario_verify.py`)
- `test_lab/seeder.py` (from `square_sandbox_seeder.py`)
- `test_lab/__init__.py` re-exporting the public API

Routes can remain in `ops_console.py` given the tight UI coupling, or be extracted to `test_lab/routes.py` and registered as a sub-blueprint.

### Duplicate Scenario Registry

`scenario_runner.SCENARIOS` and `scenario_fire.SCENARIO_REGISTRY` are separate registries with overlapping scenario keys (`happy_path_payment`, `refund_detection`, etc.) but different structures and different execution engines. The UI must be aware of which registry is being queried. There is no single authoritative scenario list.

**Impact:** A scenario named `refund_detection` in the runner (direct SQL insert) is a different operation from `refund_detection` in the fire registry (real Square API call). The Ops Console UI differentiates these as "Scenario Runner" and "Scenario Fire" modes. The naming overlap is a latent source of confusion.

**Recommended resolution:** Either merge the registries into a single authoritative list with an `execution_mode` field (`"fire"` vs `"runner"`), or rename the runner scenarios to make the distinction explicit (e.g., `refund_detection_synthetic`).

### No Isolated Tests for Test Lab Services

`scenario_fire.py`, `scenario_runner.py`, and `scenario_verify.py` have no dedicated test files. The scenario fire path cannot run in CI because it requires a live Square sandbox. The runner can be exercised in CI against the test database, but this has not been implemented.

**Impact:** Regressions in the Test Lab are caught only when an operator runs the Ops Console manually in a dev environment.

**Recommended resolution:** Add unit tests for `scenario_runner.py` against the test database (`canary_test`) and mock-based unit tests for `scenario_fire.py` to cover the step dispatch logic without hitting Square.

### Reseed Baseline Uses `python` Not `python3`

`reseed_baseline()` calls `subprocess.run(["python", ...])`. The platform standard is `python3`. On some environments, `python` may not be in PATH or may resolve to Python 2.

**Impact:** `reseed_baseline()` may fail silently or use the wrong Python interpreter.

**Recommended resolution:** Change the subprocess call to `["python3", ...]`.

### `purge_scenario_data` Duplicate Production Guard

The production environment check in `purge_scenario_data()` is duplicated — the same `if os.getenv('CANARY_ENV') == 'production': raise RuntimeError(...)` block appears twice in sequence. The second check is dead code.

**Impact:** No functional issue. Dead code adds minor confusion.

**Recommended resolution:** Remove the duplicate check.
