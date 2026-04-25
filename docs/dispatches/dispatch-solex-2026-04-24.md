# Solex — Live Commerce Pipeline (Factory Cycle Dispatch)
## Date: 2026-04-24
## Window: ~1 factory cycle (3–5 working sessions, end-to-end)
## Author: ALX (COO/CoS) for the founder
## Branch in flight: `fix/solex-live-debug-pass` (merge before cycle starts)
## Spec authority: `docs/superpowers/specs/2026-04-23-solex-commerce-mockup-design.md`
## Supersedes: nothing — this is the next phase after Plan 4 visual fidelity wrap-up

---

## What this is

Plan 4 just landed: branded shell, 25-SKU catalog, all storefront/cart/checkout/admin templates rebranded, visual smoke tests green, photo inbox plumbed, 10 live-browser issues fixed. Solex *looks* like a real Solex reseller now. It does not yet *transact* like one — and that's the only thing that matters for Canary.

The next cycle takes Solex from a polished mockup to a live Square-sandbox merchant whose transaction stream Canary can observe through its existing OAuth integration. One workstream, taken cleanly through the 9-stage Factory pipeline. No parallel tracks. No reorganization. Build the load-bearing piece, prove the data flows, hand it off.

**One-line test:** a customer (or scenario runner) clicks Buy on Solex, Square sandbox charges, an `Order` row writes, an `OrderItem` row writes, an `Inventory` decrement writes, the webhook reconciles state, and Canary's OAuth-connected merchant feed sees the transaction within 60 seconds of the click.

**Founder's lens:** if this cycle ships, the demo narrative is *"this is a real-looking commerce site running real Square transactions, and Canary is watching it live."* That's the Primetime hand-off. Until this ships, the Solex demo is a Tailwind page.

---

## Current state — what's true today

| Area | State | Evidence |
|---|---|---|
| Branded shell | ✅ shipped | commits `9c080a4`, `cb1b253`, `7f77559` |
| Catalog (25 SKUs, 4 categories) | ✅ shipped | commit `1aa5714`, `Solex/catalog/products.yaml` |
| Placeholder imagery | ✅ Pillow tile generator | commits `d88d541`, `a81695c` |
| Real photo workflow | ✅ inbox pattern | commit `6443f0a`, `Solex/catalog/inbox/README.md` |
| All UI templates rebranded | ✅ | commits `4e9d966` → `0b792d3` |
| Static pages blueprint | ✅ 9 placeholder pages | commit `7a16d61` |
| Visual smoke tests | ✅ every branded route renders | commit `bf3953c`, `tests/smoke/test_visual_smoke.py` |
| Live browser debug pass | ✅ 10 issues from `/loop` resolved | commit `b3016cd` |
| Catalog import + integration tests | ✅ | `tests/integration/test_catalog_import.py` |
| Bulk reseller order scenario test | ✅ existing | `tests/integration/test_scenario_bulk_reseller_order.py` |
| Sandbox-live `high_value_sale` test | ✅ scaffold exists | commit `aa70f39` |
| Branch hygiene | ⚠️ `fix/solex-live-debug-pass` not merged | git status |
| Square Web Payments SDK | ❌ not wired | grep |
| `square_client.py` (real) | ❌ not built | spec §4.1 |
| `checkout.place_order()` (real) | ❌ stub only | spec §4.3 |
| `/api/webhooks/square` | ❌ not built | spec §4.10 |
| Admin Lab UI for scenarios | ❌ not built | spec §4.9 |
| Cloudflare Access on `solex.growdirect.app` | ❌ not deployed | spec §11.2 |
| Subscriptions (autoship) | ❌ deferred (next cycle) | spec §4.5 |
| Refunds + returns | ❌ deferred (next cycle) | spec §4.6 |

**Uncommitted at platform root** (not Solex's problem, but worth noting before the cycle starts so we don't carry noise):
- 13 modified Brain wiki + project files (canary-* + RetailSpine + Cove)
- ~17 untracked new wiki cards (canary-module-*, growdirect-viewpoint-*, coac-*, cove-*)
- 2 untracked SDDs under `docs/sdds/consulting/`
- 1 untracked skill `.claude/skills/canary-vsm.md`
- 1 untracked `Brain/agents/` dir

→ **Pre-cycle action:** batch-commit Brain changes on a separate branch so this cycle starts clean. ALX owns this housekeeping.

---

## Scope decision — locked

**In scope (this cycle):** the Square sandbox checkout pipeline end-to-end. Spec sections §4.1, §4.2 (cart already partial), §4.3, §4.4 (inventory decrement only — adjustments later), §4.10 (webhooks), §4.11 (catalog import — already done, just verify), and the smallest admin lab UI that can fire one scenario (`high_value_sale`) through the real path.

**Explicitly deferred** to subsequent cycles, in order:
1. Scenario runner — full 9-scenario suite (spec §4.9). After this cycle proves the path works, the runner is "synthesize a cart, call `place_order()` in a loop with `scenario_tag` set." Mostly orchestration over an already-working primitive.
2. Subscriptions / autoship (spec §4.5). Needs cycle 1 done so `place_order(autoship_source=...)` has somewhere to land.
3. Refunds + returns (spec §4.6). Same dependency.
4. Cloudflare Access deployment to `solex.growdirect.app` (spec §11.2). Local dev is enough to demo; staging is a separate, smaller cycle.
5. Real Solex imagery drop-in. Trivial when we have photos.
6. Live-mode flip from sandbox → production Square. Separate spec entirely (spec §1.4).

**Out of scope, full stop:**
- Any change to Canary code. Solex remains zero-coupled (spec §1.3).
- Re-platforming. Flask/Jinja/Tailwind/Alpine, no Node SSR.
- Multi-tenant.

---

## The cycle — 9 stages

| # | Stage | Skill | Owner | Time est | Gate |
|---|---|---|---|---|---|
| 1 | Preflight | `factory-preflight` | ALX | 30 min | GRO open, infra up, branch merged |
| 2 | Research (PhD) | `factory-research` | Research + Tom | 1–2 hr | Square SDK + webhook signing patterns confirmed |
| 3 | Blueprint | `factory-blueprint` | Tom | 2 hr | Plan ≤ 8 tasks, scoped to spec §4.1/4.3/4.10/4.4 |
| 4 | TDD | `canary-tdd` (apply pattern; rename to `solex-tdd` if it sticks) | Jeremy | 2–3 hr | Failing tests committed, RED before GREEN |
| 5 | Assembly | `factory-assembly` | Jeremy | 1–2 sessions | Implementation, one commit per task |
| 6 | Verify | — | Jeremy | 1 hr | All tests green, sandbox-live integration passes |
| 7 | QA | `factory-qa` | Compliance | 1 hr | Data flows, idempotency, zero-coupling check |
| 8 | Ship | `factory-ship` | Jeremy | 30 min | PR, bisectable commits, GRO closed |
| 9 | Close | `factory-close` | ALX | 30 min | Session summary, memory writes, next-cycle hand-off |

**Total:** roughly 3–5 working sessions if nothing surprises us. Square sandbox quirks usually surprise us — budget +1 session for that.

---

## Stage 1 — Preflight

**Inputs:** this dispatch.
**Output:** `preflight_report` (per `factory-preflight` skill).
**Owner:** ALX.

Checklist:
- [ ] Open GRO issue: **"Solex live Square pipeline — sandbox checkout end-to-end."** Tag with `solex`, `factory`, link this dispatch + the spec. Label priority Medium, raise to High once Plan 4 PR merges.
- [ ] Confirm shared infra is healthy: `cd ~/GrowDirect/devops && docker compose ps` — postgres, valkey, ollama all green.
- [ ] Confirm Solex local is healthy: `cd ~/GrowDirect/Solex && ./devops/scripts/dev.sh up` — `/`, `/shop`, `/admin/login`, `/api/webhooks/square` (404 expected, route doesn't exist yet) all respond.
- [ ] Confirm Square sandbox creds in `.env`: `SQUARE_ENVIRONMENT=sandbox`, `SQUARE_SANDBOX_ACCESS_TOKEN`, `SQUARE_SANDBOX_APPLICATION_ID`, `SQUARE_SANDBOX_LOCATION_ID`, `SQUARE_SANDBOX_WEBHOOK_SIGNATURE_KEY` — all present and not placeholders.
- [ ] Merge `fix/solex-live-debug-pass` to `main` via PR, OR confirm with the founder that it lives on past this cycle.
- [ ] Batch-commit the platform-root Brain changes (separate branch, separate PR, not this cycle's concern).
- [ ] Confirm git working tree clean before the new GRO branch cuts.
- [ ] Re-run visual smoke (`pytest tests/smoke/test_visual_smoke.py`) — establish green baseline before changes.

**Gate:** Factory refuses to start if any of the above fail. Do not skip.

---

## Stage 2 — Research (PhD)

**Inputs:** GRO issue + preflight report.
**Output:** `context_bundle` — short brief covering the unknowns.
**Owner:** Research, with Tom on architecture questions.

Investigate, don't implement:
1. **Square Python SDK** — current version, sandbox auth flow, idempotency-key semantics, retry behavior on 5xx, error taxonomy. Confirm `squareup` package name + version pin.
2. **Square Web Payments SDK** — sandbox JS bundle URL, how to pass the location ID, the tokenization → server flow. Confirm we can use the SDK without a Square Application ID being public-domain (we're behind Cloudflare Access later, but local dev needs to work).
3. **Webhook signature verification** — exact algorithm (HMAC-SHA256 over `notification_url + body`), header name, what happens when the signing key rotates.
4. **Idempotency** — Square's `idempotency_key` per request; how Solex generates them; survival across retries.
5. **Webhook event types** to subscribe: `payment.updated`, `refund.updated`, `order.updated` (spec §4.10). Confirm those are the canonical names in current Square API.
6. **Test card nonces** — `cnon:card-nonce-ok`, declined variants, CVV/postal failure tokens — confirm still valid (spec §README §"Square sandbox test cards").
7. **Local webhook tunneling** — `cloudflared tunnel --url http://localhost:5003`, configure resulting URL in Square dev dashboard. Does the tunnel survive a restart? What's the registered path? (`/api/webhooks/square` per spec.)
8. **RQ on Valkey DB 2** — confirm queue isolation from Canary (DB 0) and Cove (DB 1) is working. Job naming convention: `solex.<jobname>`.

Publish findings to `Brain/wiki/solex-square-integration-notes.md`. Cross-reference in the GRO and in this dispatch's "Open questions" section if any unknowns remain.

**Gate:** all 8 areas have a concrete answer or a flagged unknown. No "we'll figure it out in assembly."

---

## Stage 3 — Blueprint

**Inputs:** preflight + context bundle.
**Output:** `docs/superpowers/plans/2026-04-25-solex-live-square-pipeline.md` (or whatever date the blueprint lands).
**Owner:** Tom.

The plan must be ≤ 8 tasks (Factory rule). Proposed task list, in order:

1. **`square_client.py`** (spec §4.1) — wrap `squareup` SDK. `create_order`, `create_payment`, `verify_webhook_signature`. Tenacity retry. Idempotency-key generator. Unit-tested with mocked SDK.
2. **`checkout.place_order()` real implementation** (spec §4.3 steps 1–8) — wire the orchestration. Uses `square_client`, `tax` stub, `shipping` stub, `inventory.decrement_for_order`. Emits an `Order` + `OrderItem`s in one DB transaction. Returns the Order.
3. **Web Payments SDK on `/checkout`** — drop the SDK script tag, render card element, wire `POST /checkout/submit` to consume the payment token, call `place_order()`. Replace the current placeholder checkout form.
4. **`/api/webhooks/square`** (spec §4.10) — signature verify, dedup via `SquareWebhookEvent.square_event_id`, dispatch to `payment.updated` / `refund.updated` / `order.updated` handlers. Orphan-payment auto-refund path stubbed (not yet exercised — refund cycle picks it up).
5. **`SquareWebhookEvent` table + Alembic migration** — append-only, unique on `square_event_id`.
6. **Inventory decrement on order** — `inventory.decrement_for_order(order)` called inside `place_order()`'s DB transaction. `InventoryAdjustment` row written. Existing tests for inventory math become integration tests.
7. **Admin lab MVP — single scenario** — `/admin/lab` route, lists registered scenarios, "Run" button for `high_value_sale` only. The button posts to a sync handler that calls `place_order()` with synthesized cart + `scenario_tag='high_value_sale-<run_id>'`. Renders `ScenarioRun` row with summary.
8. **End-to-end sandbox-live integration test** — extends the existing `test_scenario_bulk_reseller_order` pattern. Boots app, runs catalog import, posts a real card token to Square sandbox, expects `Order.status='paid'`, `Inventory` decremented, `SquareWebhookEvent` arrives within timeout. Marked `sandbox_live`.

Each task gets a Definition of Done (DoD) section in the blueprint. Tom's call on whether to combine 4 + 5 (webhook + table) into one task; the spec treats them as one component.

**Gate:** plan reviewed by ALX. Tasks fit the cycle. No scope creep (subscriptions, refunds, full scenario runner stay deferred).

---

## Stage 4 — TDD

**Inputs:** the plan from Stage 3.
**Output:** failing tests, one per behavior, committed to a `tests/` subtree on the GRO branch.
**Owner:** Jeremy.

Test inventory (mapped to plan tasks):

| Plan task | Test | Layer | Marker |
|---|---|---|---|
| 1 `square_client` | `test_square_client_create_order_idempotency` | unit | mock |
| 1 | `test_square_client_create_payment_handles_4xx` | unit | mock |
| 1 | `test_square_client_create_payment_retries_on_5xx` | unit | mock |
| 1 | `test_verify_webhook_signature_accepts_good` | unit | — |
| 1 | `test_verify_webhook_signature_rejects_tampered` | unit | — |
| 2 `place_order` | `test_place_order_persists_order_and_items` | integration | postgres |
| 2 | `test_place_order_decrements_inventory_in_same_transaction` | integration | postgres |
| 2 | `test_place_order_rolls_back_on_inventory_error` | integration | postgres |
| 2 | `test_place_order_rolls_back_on_square_5xx` | integration | postgres + mock |
| 3 Web SDK | `test_checkout_submit_consumes_token_and_redirects_to_confirmation` | integration | postgres + mock |
| 4 webhook route | `test_webhook_endpoint_401_on_bad_signature` | integration | — |
| 4 | `test_webhook_endpoint_dedups_duplicate_event_id` | integration | postgres |
| 4 | `test_webhook_payment_updated_reconciles_order_status` | integration | postgres |
| 5 migration | `test_square_webhook_event_unique_on_event_id` | integration | postgres |
| 6 inventory | covered above by `test_place_order_decrements_*` | — | — |
| 7 lab MVP | `test_admin_lab_runs_high_value_sale_scenario` | integration | postgres + mock |
| 8 e2e | `test_sandbox_live_high_value_sale_end_to_end` | integration | sandbox_live |

All RED. Commit message: `test(solex): RED — live Square pipeline (GRO-###)`. No GREEN code in this commit.

**Gate:** every test runs and fails for the expected reason (not import errors, not setup errors). Run the suite, paste the failure summary into the GRO.

---

## Stage 5 — Assembly

**Inputs:** plan + failing tests.
**Output:** implementation. One commit per plan task. All tests GREEN by the end.
**Owner:** Jeremy. Tom on architecture questions, Art on the (small) lab UI panel.

Rules of engagement:
- Edit existing files. No `_v2`, no `_new`. Spec §4 names the file paths; use those.
- Schema-qualify every new SQL: `solex.orders`, `solex.inventories`, etc. (Solex uses default `public` schema today; spec doesn't name a schema. **Open question for Tom — keep `public` or move to `solex` schema before this cycle to match Canary's discipline?** Recommend `public` for v1; introducing a schema is its own cycle.)
- Every commit runs the smoke + unit suite locally before push. Integration suite where reachable. Sandbox-live suite at the end.
- Guardian protections on `wsgi.py`, `.env`, `Dockerfile`, `docker-compose.*.yml` apply (CLAUDE.md hard rule). Use the `critical-file-guardian` skill if any of those need touching.
- Stop-and-retriage if a smoke test that was green goes red. Do not paper over.

Suggested commit cadence:
1. `feat(solex): square_client wraps Square SDK with retry + idempotency (GRO-###)`
2. `feat(solex): SquareWebhookEvent model + migration (GRO-###)`
3. `feat(solex): /api/webhooks/square signature-verified + deduped dispatch (GRO-###)`
4. `feat(solex): inventory.decrement_for_order with adjustment ledger (GRO-###)`
5. `feat(solex): checkout.place_order — real Square sandbox path (GRO-###)`
6. `feat(solex): Web Payments SDK on /checkout — token → place_order (GRO-###)`
7. `feat(solex): /admin/lab MVP — high_value_sale scenario runner (GRO-###)`
8. `test(solex): GREEN — sandbox-live end-to-end high_value_sale (GRO-###)`

**Gate:** all unit + integration tests GREEN. Sandbox-live e2e GREEN. Visual smoke still GREEN (we shouldn't have broken any branded route).

---

## Stage 6 — Verify

**Inputs:** implementation.
**Output:** `verify_report` — test counts, regression check, migration status, row-count discipline (per Canary's CLAUDE.md "no lazy pipes" standard, applied here).
**Owner:** Jeremy.

Run the four-step Completeness Gate from `Canary/CLAUDE.md` (the same standard applies to Solex — same founder, same bar):

```bash
# 1. Data goes IN
docker compose exec web pytest tests/integration/test_place_order_persists_order_and_items.py -v
# Expect: row inserted, returned ID, correct schema

# 2. Data comes OUT
docker compose exec web pytest tests/integration/test_checkout_submit_consumes_token_and_redirects_to_confirmation.py -v
# Expect: order retrievable by public_token, fields match what was written

# 3. Row counts match
docker compose exec db psql -U solex -d solex -c "
  SELECT relname, n_live_tup
  FROM pg_stat_user_tables
  WHERE relname IN ('orders', 'order_items', 'inventories', 'inventory_adjustments', 'square_webhook_events')
  ORDER BY relname;"
# Capture before, run sandbox-live e2e, capture after, deltas match expectation

# 4. The route responds
curl -s -X POST http://localhost:5003/api/webhooks/square \
     -H "x-square-hmacsha256-signature: <invalid>" \
     -H "Content-Type: application/json" -d '{}'
# Expect: 401
```

Plus:
- `alembic current` shows new head landed.
- No regressions: `pytest tests/ -m "not sandbox_live"` clean.
- `docker compose logs web` clean of unhandled exceptions during the e2e run.

**Gate:** every check above produces evidence pasted into the GRO. "Tests pass" is not enough — show the data, count the rows, verify the content (CLAUDE.md hard rule).

---

## Stage 7 — QA

**Inputs:** verify report.
**Output:** `qa_report`.
**Owner:** Compliance (with Legal on the trademark-exposure question, Art on the lab UI sanity check).

Targeted checks (not a full audit — this cycle's surface only):

- **Zero-coupling proof:** `grep -r "from canary" Solex/solex/ Solex/tests/` returns nothing. `grep -r "import canary" Solex/` returns nothing. Spec §1.3 is enforceable, not aspirational.
- **Webhook idempotency under replay:** post the same captured event payload to `/api/webhooks/square` twice; second call is a 200 OK no-op, no duplicate state changes.
- **Webhook signature handling:** good → 200, bad → 401, missing header → 400.
- **PII surface:** no card data lands in any Solex table or log line. Card-on-file references are Square tokens only (spec §8). Greppable assertion: `grep -ri "pan\|card_number\|cvv" Solex/solex/ Solex/tests/ | grep -v "test_.*comment"` empty.
- **noindex + Cloudflare gate intent:** every page renders the `<meta name="robots">` tag (spec §8). robots.txt at root disallows. (Cloudflare Access proper is a deferred deployment task; the metadata posture lands now.)
- **Legal banner** on admin pages renders (spec §8 last bullet). Compliance + Legal sign off on the wording.
- **Standards check:** SQLAlchemy 2.0 `Mapped[]` (no `Column()`), UUID PKs, `created_at`/`updated_at` on every new table, env-based config (no hardcoded secrets), schema-qualified inserts (or documented decision otherwise — see Stage 5 open question).

**Gate:** any failure goes back to Assembly. No QA-blessing in the face of a known violation.

---

## Stage 8 — Ship

**Inputs:** qa report.
**Output:** PR merged, GRO closed, Linear updated.
**Owner:** Jeremy, with DevOps eyes on the merge.

- PR title: `Solex live Square pipeline — sandbox checkout e2e (GRO-###)`.
- PR body: link the dispatch (this file), the plan, the spec, the verify + qa reports. Definition of Done checklist from the plan, all checked.
- Bisectable commits (per the cadence in Stage 5). No squash unless a commit is broken — fix or split first.
- Founder reviews + merges. Standard rules: `main` stays green; if anything regresses, revert the PR, don't band-aid.
- Linear: GRO moves to Done. Time logged. Cycle stamped on the issue.
- Tag: `solex-live-square-v1` on the merge commit. Future "live commerce baseline" reference point.

**Gate:** main is green, GRO is closed, tag exists.

---

## Stage 9 — Close

**Inputs:** shipped state.
**Output:** `session_summary` written to memory, Brain wiki updates, next-cycle hand-off.
**Owner:** ALX.

- **Session summary** to memory bus (`alx_memories`): one entry summarizing what shipped, what was deferred, what surprised us. Tagged `solex`, `factory-cycle`, `2026-04-24`.
- **Brain wiki updates:**
  - Append to `Brain/wiki/solex-square-integration-notes.md` (created in Stage 2) with what we actually shipped vs. what we researched.
  - Update `Brain/projects/Canary.md` if we discovered Canary-side observations worth noting (e.g., latency between Solex transaction and Canary alert pickup — useful for the demo narrative).
  - Add a row to a new `Brain/wiki/solex-cycles-log.md` (or extend an existing log if one exists by then) — date, branch, GRO, scope, what shipped, what's parked.
- **Decision log entry:** the Stage 5 open question on `public` vs. `solex` schema, with the choice we made and the reasoning.
- **Risk register update:** any new risks surfaced (e.g., Square sandbox quota limits, webhook delivery flakiness in dev, Cloudflare-tunnel restart fragility). One line each, owner assigned.
- **Next-cycle hand-off:** write the dispatch for the next cycle (Subscriptions OR Scenario Runner — pick one). Save as `docs/dispatches/dispatch-solex-NEXT-<date>.md` and link it in the GRO and in the founder's Linear inbox.

**Gate:** session is over when the next-cycle dispatch is in the dispatches folder and Linear is current.

---

## Open questions to close before Assembly starts

1. **Schema discipline.** Solex tables in `public` (current) or move to a named `solex` schema before this cycle (matches Canary's `app`/`sales`/`metrics` discipline)? *Recommendation: stay in `public` for v1, raise as a separate cycle if it bites us. — Tom to confirm.*
2. **Webhook tunnel for local dev.** `cloudflared tunnel --url http://localhost:5003` ad-hoc per session, or a persistent named tunnel? *Recommendation: ad-hoc for now; persistent only if we keep losing webhook deliveries. — Jeremy.*
3. **Test-card matrix.** Which decline / partial / refunded variants do we cover in unit tests vs. integration vs. sandbox-live? *Recommendation: all in unit (mocked); two in sandbox-live (one happy, one declined); rest deferred. — Compliance.*
4. **Branch strategy.** Cut the new GRO branch from `main` (after `fix/solex-live-debug-pass` merges) or from `fix/solex-live-debug-pass` directly if we need to keep moving? *Recommendation: merge first; cut from `main`. Cleaner.*

ALX collects answers, posts to GRO, then Stage 3 runs.

---

## Parked workstreams (post this cycle, in priority order)

| Cycle | What | Estimated size | Trigger |
|---|---|---|---|
| Solex C2 | Scenario runner — full 9-scenario suite + admin lab UI complete | 1 cycle | This cycle ships clean |
| Solex C3 | Subscriptions / autoship — `Subscription` model + rq-scheduler + card-on-file + `/account/subscriptions` view+cancel | 1 cycle | C2 ships |
| Solex C4 | Refunds + returns — `refunds.issue_refund`, `ReturnRequest`, admin refund UI, refund webhook reconciliation | 1 cycle | C3 ships |
| Solex C5 | Cloudflare Access deployment to `solex.growdirect.app` + persistent tunnel + Cloudflare Pages on the static pages | ½ cycle | When founder wants live demo URL |
| Solex C6 | Real Solex imagery drop-in (replace Pillow tiles) | <½ cycle | Photos arrive in `Solex/catalog/inbox/` |
| Solex C7 | Catalog mirror to Square (`SYNC_CATALOG_TO_SQUARE=true`) — useful for any Canary rules inspecting catalog attributes | ½ cycle | Canary surfaces a rule that needs it |
| Solex C∞ | Sandbox → live-mode flip, design-partner contract, distributor-pricing model | separate spec | External: Solex rep interest |

---

## Key references

| Resource | Path |
|---|---|
| This dispatch | `docs/dispatches/dispatch-solex-2026-04-24.md` |
| Spec authority | `docs/superpowers/specs/2026-04-23-solex-commerce-mockup-design.md` |
| Original playbook (mostly superseded) | `docs/playbook-solex-square-merchant.md` |
| Solex repo | `Solex/` |
| Solex README + runbook | `Solex/README.md` |
| Canary CLAUDE.md (standards we mirror) | `Canary/CLAUDE.md` |
| Platform CLAUDE.md (rule zero, session discipline) | `CLAUDE.md` |
| Factory MOC | `Brain/projects/Factory.md` |
| Method MOC | `Brain/projects/Method.md` |
| Catalog source | `Solex/catalog/products.yaml` |
| Photo inbox | `Solex/catalog/inbox/` |
| Visual smoke | `Solex/tests/smoke/test_visual_smoke.py` |
| Existing sandbox-live test | `Solex/tests/integration/test_scenario_bulk_reseller_order.py` (pattern to extend) |
| Test cards | `Solex/README.md` § "Square sandbox test cards" |

---

## One-page summary for the founder

We just finished making Solex *look* like a real Solex reseller. The next cycle makes it *transact* like one. Single workstream, taken cleanly through preflight → research → blueprint → tdd → assembly → verify → qa → ship → close. Scoped to spec sections §4.1, §4.3, §4.4, §4.10, plus the smallest admin lab that can fire one scenario. Subscriptions, refunds, full scenario runner, and Cloudflare deploy are parked for follow-on cycles in declared order. Three to five sessions if Square sandbox cooperates, plus one for surprises.

Demo narrative after this ships: *"Click Buy on Solex. Watch Canary see it. Same merchant feed any production Square seller would generate."* That's the pitch. This cycle is what turns it from a deck claim into a live click.

---

*Solex | GrowDirect LLC | Confidential — sandbox fixture, not a live business*
