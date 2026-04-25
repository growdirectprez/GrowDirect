# Solex C2 — Productionize the scenario runner UX (Factory Cycle Dispatch)
## Date: 2026-04-25
## Window: ~½ factory cycle (2 working sessions, end-to-end)
## Author: ALX (COO/CoS) for the founder
## Branch in flight: `gclyle/gro-536-solex-live-square-pipeline-sandbox-checkout-end-to-end` (closes when GRO-536 ships)
## Spec authority: `docs/superpowers/specs/2026-04-23-solex-commerce-mockup-design.md` § 4.9
## Supersedes: nothing — this is the next phase after GRO-536's "live Square pipeline" cycle

---

## What this is

GRO-536 shipped the live Square sandbox pipeline. Solex now transacts: real Square charges, real `Order` rows, real inventory decrements, real webhook reconciliation, all observable through Canary's existing OAuth integration. The plumbing is done.

What's *not* done: the admin scenario runner is functional but rough. The lab page lists all 9 scenarios in a flat dropdown, the run history is a chronological dump, and there's no per-scenario detail view that explains what each scenario simulates and why an operator would run it. The current UX is "developer tool that someone forgot to dress up" — fine for the cycle that built it, not fine for a demo or for an operator who didn't write the code.

This cycle takes the existing scenario primitive and gives it the shell a real operator would expect.

**One-line test:** an operator who has never seen Solex before opens `/admin/lab`, picks a scenario from a categorized list, sees a clear preview of what the run will produce, clicks Run, watches the run execute live, drills into the run detail to inspect the synthesized cart and resulting orders/inventory adjustments, and bookmarks the run for later reference. No source-code reading required.

---

## Current state — what's true today

| Area | State | Evidence |
|---|---|---|
| `place_order()` real Square sandbox path | ✅ shipped | GRO-536, `Solex/solex/services/checkout.py:62`, sandbox-live test green |
| `/api/webhooks/square` — verify, dedup, dispatch | ✅ shipped | GRO-536, `Solex/solex/routes/api.py:44` |
| 9 scenarios runnable | ✅ shipped | `Solex/solex/services/scenarios/` |
| `/admin/lab` lists scenarios | ✅ exists, flat list | `Solex/solex/routes/lab.py` |
| `ScenarioRun` row written per execution | ✅ exists | `Solex/solex/models/`, scenario detail at `/admin/lab/runs/<run_id>` |
| Sync vs async execution by count threshold | ✅ exists | `lab.py` `_run_sync()` and `_enqueue()` |
| Per-scenario description + parameter docs | ❌ none | scenarios are runnable but undocumented in UI |
| Run history filters | ❌ chronological dump only | `lab.py` lists all runs |
| Live run progress UI | ❌ no streaming | enqueued runs show "queued" until refresh |
| Categorized scenario picker | ❌ flat list | `lab.html` dropdown |
| Scenario tag inspection | ❌ raw JSON | summary_json shown verbatim |
| Sandbox-live e2e regression marker | ✅ exists | `@pytest.mark.sandbox_live`, 3 tests green |

**Not Solex's problem this cycle:** Canary-side observability of the merchant feed. Canary already sees the transactions. C2 is purely about Solex's operator experience.

---

## Scope decision — locked

**In scope (this cycle):**

1. **Scenario detail metadata** — each scenario in `services/scenarios/` declares a one-paragraph description, expected behaviors, parameter ranges with sensible defaults, and which detection rules it's designed to surface. Surfaced in the lab UI as scenario detail pages.
2. **Categorized scenario picker** — group scenarios by intent (Operations, Loss prevention, Fraud, Customer behavior, Subscriptions). Replace the flat dropdown with a card grid.
3. **Run history filters** — filter `/admin/lab/runs/` by scenario name, status (queued/running/succeeded/failed), date range. Add a "favorite this run" toggle for operators who want to bookmark important runs.
4. **Live progress UI** — for async (RQ-enqueued) runs, an Alpine-driven polling indicator on the run detail page. No SSE/WebSockets — just polling against an existing run-status endpoint.
5. **Run detail enhancement** — instead of dumping `summary_json` verbatim, render a structured view: synthesized cart preview, orders produced, inventory adjustments by reason, scenario-tagged Square events, links to drill into specific orders.

**Explicitly deferred:**

1. Multi-tenant scenarios — every scenario runs against the single seeded merchant.
2. Scenario authoring UI — adding new scenarios still requires Python code, not a form.
3. Scheduling — no "run this scenario every Monday at 9am." The C5 (Cloudflare deploy) cycle can introduce that if Canary needs ongoing background observation traffic.
4. Cross-tenant correlation views — Canary's job, not Solex's.

**Out of scope, full stop:**

- Any change to Canary code (zero-coupling rule).
- Re-platforming. Stays Flask/Jinja/Tailwind/Alpine.
- New Square API surfaces — this cycle is pure Solex frontend on existing service primitives.

---

## The cycle — compressed

GRO-536 demonstrated that the 9-stage Factory pipeline compresses naturally when most of the work is already done. C2 is closer to a UX-polish cycle than a build cycle, so the pipeline is shorter:

| # | Stage | Skill | Owner | Time est | Gate |
|---|---|---|---|---|---|
| 1 | Preflight | `factory-preflight` | ALX | 15 min | GRO open, branch cut, infra up |
| 2 | Blueprint | `factory-blueprint` | Tom + Art | 1 hr | Plan ≤ 5 tasks, mockup or hand-sketch of new lab page |
| 3 | TDD | `factory-tdd` | Jeremy | 1 hr | Failing tests for filters, scenario metadata loader, status endpoint |
| 4 | Assembly | `factory-assembly` | Jeremy + Art | 1 session | Implementation, one commit per task |
| 5 | Verify | — | Jeremy | 30 min | Suite green, sandbox-live regression green, manual click-through |
| 6 | QA | `factory-qa` | Compliance + Art | 30 min | Visual consistency with brand, accessibility on the new card grid, no PII regressions |
| 7 | Ship | `factory-ship` | Jeremy | 30 min | PR, GRO closed, tag `solex-lab-v2` |
| 8 | Close | `factory-close` | ALX | 30 min | Wiki updates, next-cycle dispatch (C3 subscriptions UX) |

**Total:** ~2 working sessions if mockups land cleanly. Most of the work is templating + Alpine wiring, not new service code.

---

## Stage 2 — Blueprint (preview)

Proposed task list, in order:

1. **Scenario metadata schema + loader** — extend each scenario class with `description`, `category`, `expected_behaviors`, `param_schema` properties. Loader exposes `registry.describe(name)` returning a structured dict.
2. **`/admin/lab/` rewrite — categorized card grid** — Jinja template + Tailwind cards grouped by category. Each card surfaces description and "Run" CTA.
3. **`/admin/lab/scenarios/<name>/` detail page** — full scenario description, parameter form (no more raw JSON), "Run with these params" button.
4. **`/admin/lab/runs/` filter UI** — Alpine-driven filters (scenario, status, date range, favorites). New `favorite` boolean column on `ScenarioRun` with default false.
5. **Run detail rebuild** — structured summary panel: cart preview table, orders table linking to `/admin/orders/<id>`, inventory adjustments grouped by reason, scenario-tagged Square events table. Live progress poll for async runs.

Each task gets a Definition of Done in the blueprint.

---

## Stage 3 — TDD (preview)

| Plan task | Test | Layer |
|---|---|---|
| 1 | `test_scenario_registry_describes_all_nine` | unit |
| 1 | `test_scenario_metadata_categories_are_canonical` | unit |
| 2 | `test_admin_lab_renders_categorized_grid` | unit (route render) |
| 3 | `test_admin_lab_scenario_detail_renders_param_form` | unit |
| 3 | `test_admin_lab_scenario_run_with_params_persists_run` | integration |
| 4 | `test_admin_lab_runs_filter_by_scenario_and_status` | integration |
| 4 | `test_admin_lab_runs_favorite_toggles_persistence` | integration |
| 5 | `test_admin_lab_run_detail_renders_structured_summary` | integration |
| 5 | `test_admin_lab_run_detail_polls_status_endpoint` | unit (Alpine + JS sanity) |

All RED first. No GREEN code in the TDD commit.

---

## Stage 5 — Verify

Run all four gates from the GRO-536 cycle's verify pattern:

```bash
# Smoke
docker compose -f devops/docker-compose.yml exec -T web pytest tests/smoke/ -v

# Unit + integration
docker compose -f devops/docker-compose.yml exec -T web pytest -m "not sandbox_live" -q

# Sandbox-live regression (must still pass — we shouldn't break the pipeline)
docker compose -f devops/docker-compose.yml exec -T web pytest -m sandbox_live -v

# Visual smoke
docker compose -f devops/docker-compose.yml exec -T web pytest tests/smoke/test_visual_smoke.py -v
```

Plus a manual click-through:
- Lab landing page renders the card grid, all 9 scenarios visible, descriptions readable.
- Click a scenario → detail page renders, params form accepts input.
- Run a scenario → progress indicator shows, run detail page renders structured summary.
- Filter run history by status=succeeded → only succeeded runs visible.
- Favorite a run → persists across page reload.

---

## Stage 6 — QA

**Targeted checks:**

- Brand consistency: card grid uses `solex-cream` background, `solex-teal` CTAs, Cormorant + Inter typography. No raw `bg-stone-900` left over from earlier templates.
- Accessibility: scenario cards have proper headings, "Run" buttons are real `<button>`s not `<div>` clicks, status badges have `aria-label`.
- PII surface: scenario param forms don't accept anything that would land in a card token field. Cart preview uses test-card data only.
- Zero-coupling: `grep -r "from canary" Solex/solex/ Solex/tests/` empty. `grep -r "import canary" Solex/` empty.
- No regressions to GRO-536 surfaces: `/checkout`, `/api/webhooks/square`, `place_order()` paths unchanged.

---

## Stage 7 — Ship

- PR title: `Solex C2 — productionize scenario runner UX (GRO-XXX)`
- Tag: `solex-lab-v2` on the merge commit. (`solex-live-square-v1` from GRO-536 stays as the live-pipeline reference point.)
- Linear: GRO closes. Cycle stamped on the issue. Hand-off in description.

---

## Stage 8 — Close

- Append a row to `Brain/wiki/solex-square-integration-notes.md` documenting the C2 UX surface.
- Decision log entry: scenario metadata schema choice (frozen-dataclass on the scenario class vs. external YAML).
- Next-cycle dispatch: C3 (subscriptions UX surface in `/account/`). Save as `docs/dispatches/dispatch-solex-c3-<date>.md`.

---

## Open questions to close before Assembly starts

1. **Scenario metadata location.** Inline on the scenario class as class attributes, or external YAML loaded by the registry? *Recommendation: inline class attributes — co-locates description with code, no second source of truth. — Tom to confirm.*
2. **Live progress mechanism.** Alpine polling against `/admin/lab/runs/<run_id>/status.json` or a single SSE endpoint? *Recommendation: polling — simpler, no streaming infra, the runs are short. — Jeremy.*
3. **Favorite scope.** Per-admin-user or global? *Recommendation: per-user (Flask-Login user_id on the favorite). — Compliance.*

ALX collects answers, posts to GRO, then Stage 3 runs.

---

## Parked workstreams (post this cycle, in priority order)

| Cycle | What | Trigger |
|---|---|---|
| Solex C3 | Subscriptions / autoship UX in `/account/` — view/cancel/upgrade card-on-file. Service exists; views don't. | C2 ships |
| Solex C4 | Refunds + returns admin UX — `RefundsService` exists but no `/admin/refunds` workflow surface | C3 ships |
| Solex C5 | Cloudflare Access deployment to `solex.growdirect.app` + persistent named tunnel | C4 ships or sooner if external demo URL needed |
| Solex C6 | Real Solex imagery drop-in (replace Pillow tiles) | Photos arrive in `Solex/catalog/inbox/` |
| Solex C7 | Catalog mirror to Square (`SYNC_CATALOG_TO_SQUARE=true`) | Canary surfaces a rule that needs catalog attributes |
| Solex C∞ | Sandbox → live-mode flip, design-partner contract | External: Solex rep interest |

---

## Key references

| Resource | Path |
|---|---|
| This dispatch | `docs/dispatches/dispatch-solex-c2-2026-04-25.md` |
| Spec authority | `docs/superpowers/specs/2026-04-23-solex-commerce-mockup-design.md` § 4.9 |
| GRO-536 close artifact | `Brain/wiki/solex-square-integration-notes.md` |
| Solex repo | `Solex/` |
| Solex README + runbook | `Solex/README.md` |
| Existing lab route | `Solex/solex/routes/lab.py` |
| Scenario registry | `Solex/solex/services/scenarios/` |
| Lab template (will be rewritten) | `Solex/solex/templates/admin/lab.html` |
| Test pattern to extend | `Solex/tests/integration/test_scenario_*.py` |

---

## One-page summary for the founder

GRO-536 shipped the live Square pipeline. Solex transacts. C2 is the UX cycle that turns the scenario runner from a developer tool into something an operator can drive without reading code. Two sessions if mockups land cleanly, plus one for surprises. After C2: subscriptions UX (C3), refunds/returns admin UX (C4), then Cloudflare Access (C5).

Demo narrative after this ships: *"open the lab, pick a scenario, watch it run, drill into the run, see Canary catch the patterns it surfaced. End-to-end, in a browser, without me typing in a terminal."* That's the operator demo for Canary prospects.

---

*Solex | GrowDirect LLC | Confidential — sandbox fixture, not a live business*
