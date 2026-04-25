# Solex C3 — Subscriptions / autoship UX in /account/ (Factory Cycle Dispatch)
## Date: 2026-04-25
## Window: ~½ factory cycle (2 working sessions, end-to-end)
## Author: ALX (COO/CoS) for the founder
## Predecessor: GRO-549 (C2 — productionized scenario runner UX, tag `solex-lab-v2`)
## Spec authority: `docs/superpowers/specs/2026-04-23-solex-commerce-mockup-design.md` § 4.5
## Supersedes: nothing — this is the next phase after C2

---

## What this is

GRO-549 productionized the admin scenario runner. Operators can drive the lab without reading code. What's still rough: the **customer-facing** subscription experience.

The plumbing exists (`subscriptions.py` 159 lines, `Subscription` + `SubscriptionCharge` models, RQ-scheduler-backed renewal job, card-on-file via Square's customer + card storage, `place_order(autoship_source=...)` wired through). What's missing is the surface a customer would touch: a place to view their active subscriptions, change cadence or quantity, swap the card on file, or cancel.

Right now if a customer subscribed at checkout and wants to cancel, they need to email support. That's a churn lever and a CS tax. C3 closes the loop.

**One-line test:** a customer who subscribed at checkout opens `/account/subscriptions`, sees their active autoship rows with the next charge date, can edit quantity / cadence, swap the saved card, or cancel — all without contacting support. The change persists, the next charge cycle reflects it, and Square's customer + card-on-file tokens get the right calls.

---

## Current state — what's true today

| Area | State | Evidence |
|---|---|---|
| `Subscription` + `SubscriptionCharge` models | ✅ shipped | `Solex/solex/models/subscription.py` |
| Square card-on-file storage | ✅ shipped | `services/square_client.py:save_card_on_file` |
| Subscribe at checkout | ✅ shipped | `services/checkout.py` lines 85-91, exercised by `test_subscribe_at_checkout.py` |
| RQ-scheduler renewal job | ✅ shipped | `services/subscriptions.py:charge_due_subscriptions` |
| `autoship_cohort` scenario exercises full path | ✅ shipped | sandbox-live test green |
| `/account/login` magic-link + password | ✅ shipped | `routes/account_auth.py` |
| `/account/subscriptions` view | ❌ stub | route exists but template renders empty list |
| Subscription cancel | ❌ no surface | DB column exists; no UX |
| Subscription edit (qty / cadence) | ❌ no surface | model supports both; no form |
| Card-on-file swap | ❌ no surface | service supports; no Web Payments SDK on `/account/` |
| Email confirmation on cancel | ❌ no template | `email_logs` exists; `subscription_cancelled` template missing |
| Subscription detail page | ❌ no route | |

---

## Scope decision — locked

**In scope (this cycle):**

1. `/account/subscriptions/` — list active + paused + cancelled, with next charge date. Real query, not stub.
2. `/account/subscriptions/<id>/` detail page — full timeline (charges + status changes), edit form for qty + cadence_days, prominent cancel button.
3. POST `/account/subscriptions/<id>/cancel` — confirms, sets `status='cancelled'`, sends `subscription_cancelled` email, no Square-side cancellation needed (we just stop charging).
4. POST `/account/subscriptions/<id>/edit` — updates qty + cadence_days, recomputes `next_charge_at` based on the new cadence. Single transaction.
5. `/account/subscriptions/<id>/swap-card` — Web Payments SDK on the customer side, tokenizes a new card, calls `square.save_card_on_file()`, updates `Subscription.square_card_id`. This is the smallest possible surface; the full "manage cards" experience is a separate cycle.

**Explicitly deferred to subsequent cycles:**

1. **C4 — refunds + returns admin UX.** Already had its own slot.
2. **Pause / resume.** `status` field supports it. The cycle that needs it is small enough to fold into a follow-on.
3. **Multi-product subscriptions.** Each Subscription row is one product today. Bundling is a model-level change.
4. **Customer-facing usage history.** Nice to have, not load-bearing.

**Out of scope, full stop:**

- Any change to Canary code.
- New Square API surfaces beyond what `square_client` already supports.
- Multi-tenant.

---

## The cycle — compressed (matches C2 cadence)

| # | Stage | Owner | Time est | Gate |
|---|---|---|---|---|
| 1 | Preflight | ALX | 15 min | GRO open, branch cut from main, infra healthy |
| 2 | Blueprint | Tom + Art | 1 hr | Plan ≤ 5 tasks + sketch of `/account/subscriptions/` |
| 3 | TDD | Jeremy | 1 hr | Failing tests for list, detail, cancel, edit, card-swap |
| 4 | Assembly | Jeremy + Art | 1 session | Implementation, one commit per task |
| 5 | Verify | Jeremy | 30 min | Suite green, sandbox-live regression green, manual click-through |
| 6 | QA | Compliance + Art | 30 min | Brand consistency, accessibility, PII surface check |
| 7 | Ship | Jeremy | 30 min | PR, GRO closed, tag `solex-subs-ux-v1` |
| 8 | Close | ALX | 30 min | Wiki update, next-cycle dispatch (C4 refunds/returns admin UX) |

**Total:** ~2 sessions if Web Payments SDK on `/account/` lands cleanly.

---

## Stage 2 — Blueprint preview

Proposed tasks:

1. **`/account/subscriptions/` list rebuild** — real query, brand tokens, links to detail. Show qty / cadence / next_charge_at / product / saved-card tail digits. Tests cover empty, multiple-row, mixed-status cases.

2. **`/account/subscriptions/<id>/` detail page + charge timeline** — card-style header, timeline of `SubscriptionCharge` rows, edit form, cancel button. Tests cover render + charge ordering + auth gate.

3. **POST `/account/subscriptions/<id>/cancel`** — flash confirmation, sets status, sends email, redirects to list. Tests cover auth gate, idempotency, email log row, can't cancel another customer's sub (404).

4. **POST `/account/subscriptions/<id>/edit`** — atomic update of qty + cadence, `next_charge_at = max(now, last_charge + new_cadence)` to avoid double-charges. Tests cover validation, recomputation, auth gate.

5. **`/account/subscriptions/<id>/swap-card`** — GET shows card form (Web Payments SDK), POST tokenizes + persists. Tests cover SDK script tag present, token consumption end-to-end (under sandbox-live marker).

---

## Stage 5 — Verify gates (mirrors C2)

```bash
docker compose -f devops/docker-compose.yml exec -T web pytest -m "not sandbox_live" -q
docker compose -f devops/docker-compose.yml exec -T web pytest -m sandbox_live -v
docker compose -f devops/docker-compose.yml exec -T web pytest tests/smoke/test_visual_smoke.py -v
```

All three green. The autoship-cycle sandbox-live test (`test_subscriptions_sandbox.py`) must keep passing — touching the subscription service surface should not break the existing charge cycle.

---

## Open questions to close before Assembly

1. **Pause vs cancel.** Should the cancel button offer a "pause for 30 days" affordance? *Recommendation: cancel-only for v1; pause is a follow-up. — Tom to confirm.*
2. **Email template tone.** Generic transactional ("Your subscription has been cancelled") or warmer ("Sorry to see you go — here's how to come back")? *Recommendation: generic transactional. The brand already does enough storytelling; cancel emails don't need it. — Brand voice via the brand-voice skill.*
3. **Card swap surface.** Inline on detail page or separate route? *Recommendation: separate route at `/swap-card` — keeps the Web Payments SDK script load isolated, easier to test. — Jeremy.*

---

## Parked workstreams (post C3, in priority order)

| Cycle | What | Trigger |
|---|---|---|
| Solex C4 | Refunds + returns admin UX — `/admin/refunds`, `/admin/returns/<id>` workflow, manual refund issuance form | C3 ships |
| Solex C5 | Cloudflare Access deployment to `solex.growdirect.app` + persistent named tunnel | When founder wants live demo URL |
| Solex C6 | Real Solex imagery drop-in (replace Pillow tiles) | Photos arrive in `Solex/catalog/inbox/` |
| Solex C7 | Catalog mirror to Square (`SYNC_CATALOG_TO_SQUARE=true`) | Canary surfaces a rule that needs catalog attributes |
| Solex C8 | Subscription pause/resume + multi-product bundles | C3 ships and demand surfaces |
| Solex C∞ | Sandbox → live-mode flip, design-partner contract | External: Solex rep interest |

---

## Key references

| Resource | Path |
|---|---|
| This dispatch | `docs/dispatches/dispatch-solex-c3-2026-04-25.md` |
| Spec authority | `docs/superpowers/specs/2026-04-23-solex-commerce-mockup-design.md` § 4.5 |
| Predecessor (C2) | `docs/dispatches/dispatch-solex-c2-2026-04-25.md` |
| Integration notes | `Brain/wiki/solex-square-integration-notes.md` |
| Existing service | `Solex/solex/services/subscriptions.py` |
| Existing model | `Solex/solex/models/subscription.py` |
| Test pattern to extend | `Solex/tests/integration/test_subscribe_at_checkout.py` |
| Sandbox-live regression gate | `Solex/tests/integration/test_subscriptions_sandbox.py` |

---

## One-page summary for the founder

C2 made the lab operator-grade. C3 makes subscriptions customer-grade. Two sessions. View / edit / cancel / swap card — the four moves a customer needs to manage autoship without emailing support. After C3: refunds & returns admin UX (C4), then Cloudflare deploy (C5).

Demo narrative after this ships: *"customer subscribes at checkout, watches the next charge date update when they bump cadence, cancels with one click. End-to-end self-service."*

---

*Solex | GrowDirect LLC | Confidential — sandbox fixture, not a live business*
