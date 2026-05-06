# Solex Global — Square Merchant on Canary Infrastructure Playbook

Evaluate `solexglobal.com` as an MLM vendor product line and set up a
Square merchant front-end that routes Solex reseller sales through
Canary's infrastructure. Recreate the current "sandbox seller" pattern as
a **Solex seller** — first in sandbox, then (gated) in production Square.

---

## Goal

Demonstrate Canary's loss prevention + ops dashboard stack working for a
real-world niche retail vertical: a single MLM reseller operating as a
Square merchant selling Solex products. Proves out:

1. Canary handles non-brick-and-mortar retail (MLM reseller / direct sales)
2. Canary can be configured for a specific vendor's product catalog
3. The sandbox → production path is exercised end-to-end
4. We have a real, named design partner for beta work

**End state:** a seeded Solex sandbox seller in Canary Test Lab that
looks and behaves like a realistic MLM reseller. Optional later: flip to
a live Square production merchant.

---

## Scope decision — before starting

Two levels of ambition:

- [ ] **Level 1 (sandbox-only):** Reconfigure the existing Canary sandbox
      seeder to produce a Solex-flavored seller. All in Square sandbox.
      No real money, no real merchant. Deliverable: a compelling demo.
      **Time: 1-2 sessions.**
- [ ] **Level 2 (sandbox + production path):** Level 1, plus scaffolding
      for a real Square merchant account taking real Solex sales. Needs
      Solex rep contact, merchant onboarding, tax setup, payment flow.
      **Time: 4-8 sessions + external dependencies.**

Default recommendation: **start Level 1**, validate the demo, then decide
on Level 2 based on Solex rep interest.

Record scope decision: ________________________

---

## Phase 0 — Create Linear issues

- [ ] Create parent Linear issue: **"Solex Global — MLM reseller Square
      merchant on Canary infra"** in Growdirect / Canary project.
- [ ] Description: "Per docs/playbook-solex-square-merchant.md. Evaluate
      solexglobal.com, adapt sandbox seeder for Solex catalog, validate
      Canary rules fire correctly for MLM reseller transaction patterns."
- [ ] Priority: Medium (bump to High if design partner interest confirmed).
- [ ] Note GRO-### and reference in commits.

---

## Phase 1 — Evaluate Solex (external research)

Don't touch code yet. Understand what Solex actually sells and how its
resellers operate.

- [ ] Read `solexglobal.com` in depth. Focus on:
  - **Product categories** — what do they sell? (nutraceuticals, wellness,
    something else?)
  - **SKU count** — rough number of products in catalog
  - **Price tiers** — retail price range, wholesale/reseller price range
  - **MLM structure** — how do resellers buy from Solex, markup, commission
  - **Order patterns** — do resellers order to stock, or drop-ship, or both?
  - **Compliance / health claims** — are there regulated claims we'd need
    to be careful with in any marketing?
- [ ] Document findings in `Brain/wiki/solex-global-overview.md`:
  - Company summary, product categories, reseller model, typical basket
    composition, price ranges, red flags / compliance notes
- [ ] Cross-reference against typical MLM reseller patterns — identify
      what's distinctive about Solex vs. a generic MLM seller.
- [ ] **Decision point:** is Solex a good fit as a demo vertical? If the
      product catalog or compliance story is weird, stop here and pick a
      different target. Record decision.

---

## Phase 2 — Analyze current sandbox seller

Understand what we're replacing before we replace it.

- [ ] Read `Canary/canary/services/square_sandbox_seeder.py`. Current seeder
      produces:
  - 4 team members (Sofia, James, David, Alejandro @growdirect.io)
  - 15-item metaphysical/wellness catalog (sage, palo santo, crystals,
    essential oils, candles — farmers-market spiritual shop vibe)
  - 6 round-dollar gift cards for C-003 round-amount rule testing
- [ ] Read the seed scripts in `Canary/devops/scripts/`:
  - `seed_sandbox.py`, `seed_full_sandbox.py`, `seed_dashboard_sandbox.py`,
    `chirp_sweep_sandbox.py`
- [ ] Read `Canary/tests/integration/test_seed_sandbox.py` +
      `tests/unit/test_square_sandbox_seeder.py` to understand test
      coverage.
- [ ] Note: seeder refuses to run against production
      (`SQUARE_ENVIRONMENT != "sandbox"` gate). Good — keep that.
- [ ] Also read GRO-297 (inventory adjustments + ordering for shrink rule
      testing) — it extends the same seeder and must stay compatible.

---

## Phase 3 — Design the Solex seller profile

Decision-making phase. Produce a short spec before changing code.

- [ ] Pick a reseller identity:
  - Business name (e.g., "Bonsall Wellness Direct" — MLM reseller names are
    typically local + wellness-themed)
  - Location (real or fictitious)
  - Team member count and roles (solo reseller? family operation?
    distributor + downline?)
- [ ] Pick a catalog subset from Solex:
  - 10-20 representative SKUs covering the product categories found in
    Phase 1
  - Real Solex product names + SKUs (maintains authenticity) OR thinly
    disguised placeholders (avoids legal concerns)
  - Price points spanning realistic range from Phase 1
- [ ] Pick transaction patterns the seeder should generate:
  - Retail customer purchases (1-3 item baskets)
  - Reseller-to-reseller purchases (bulk orders, 5-20 items)
  - Autoship recurring orders (if Solex uses them)
  - Returns / exchanges
- [ ] Identify which Canary chirp rules this catalog should exercise:
  - C-001 HIGH_VALUE — pick a high-ticket Solex item
  - C-002 AFTER_HOURS — depends on transaction timing, not catalog
  - C-003 ROUND_AMOUNT — include round-dollar SKUs (like the gift cards)
  - Others that make sense for MLM reseller patterns
- [ ] Write up the spec at `Brain/wiki/solex-seller-spec.md`.

---

## Phase 4 — Implement the Solex seeder

Code. Keep the existing seeder working — don't break the current demo.

- [ ] Design decision: **extend** `SquareSandboxSeeder` with a `seller_profile`
      parameter, OR create a new `SolexSandboxSeeder` class that shares the
      base. Prefer the first (one class, parameterized) to avoid code
      duplication.
- [ ] Refactor constants (`TEAM_MEMBERS`, `CATALOG`) out of module scope
      into named profiles:
  - `DEFAULT_PROFILE` = current metaphysical shop (preserves demo)
  - `SOLEX_PROFILE` = new Solex reseller profile
  - Make `SquareSandboxSeeder(profile="solex")` the API
- [ ] Add Solex team members + catalog constants in a new file
      `canary/services/sandbox_profiles/solex.py` (or similar) to keep the
      seeder file clean.
- [ ] Add a CLI flag: `python3 -m canary.services.square_sandbox_seeder
      --profile solex --all`
- [ ] Update tests:
  - Existing tests keep passing with default profile
  - New tests for Solex profile (team member count, catalog count, SKU
    format)
- [ ] Run the new seeder against Square sandbox. Verify via Square sandbox
      dashboard (or the Square API) that team + catalog look right.

---

## Phase 5 — Generate Solex transaction scenarios

The seeder populates catalog + team. Transaction generation is separate.

- [ ] Check `Canary/devops/scripts/seed_full_sandbox.py` + `chirp_sweep_sandbox.py`
      for how transaction scenarios are generated today.
- [ ] Design 3-5 Solex-specific transaction scenarios:
  - "Normal reseller day" — mix of small customer orders
  - "Bulk autoship day" — recurring large orders
  - "Shrink event" — missing inventory scenario
  - "Round-amount pattern" — suspicious round-dollar clustering
  - "After-hours suspicious activity" — C-002 trigger
- [ ] Implement each as a named scenario callable from Test Lab.
- [ ] Wire them into the Canary Test Lab UI so a demo walkthrough can
      trigger each.
- [ ] Verify each scenario fires the expected chirp rules at the expected
      severities.

---

## Phase 6 — Validation

Does it actually look like a real Solex reseller?

- [ ] Side-by-side compare: transaction history in the Solex sandbox vs.
      what a real MLM reseller's Square history might look like. Feels
      real? Or too synthetic?
- [ ] Run a full Canary demo on the Solex merchant:
  - Ops Dashboard (GRO-144 work) shows sensible KPIs
  - Chirp rules fire on the scenario transactions
  - Owl search answers natural-language questions about the seller
- [ ] Screen-record a 5-minute demo walkthrough. Keep for sales use.

---

## Phase 7 (Level 2 only) — Production Square path

Skip entirely if you're at Level 1. This phase assumes a real Solex rep
is interested and a real reseller is willing to route transactions
through Canary.

- [ ] Identify the actual reseller who will be the merchant of record.
      Contract them as a design partner (free Canary for N months in
      exchange for data access + logo rights).
- [ ] Onboard them as a real Square merchant (if not already). Standard
      Square business signup, tax ID, bank account.
- [ ] Install Canary's OAuth integration on their Square account.
- [ ] Import their real catalog (don't fake it in production — pull from
      Solex's actual catalog API if available, or manual entry).
- [ ] Let transactions flow for 30 days. Monitor chirp rules for false
      positives specific to MLM reseller patterns (bulk reseller purchases
      will look like wholesale distribution — probably trip volume rules).
- [ ] Tune rule thresholds based on real MLM traffic. Document the
      configuration in `Brain/wiki/canary-mlm-tuning.md`.
- [ ] Case study: with reseller permission, write it up as sales
      collateral.

---

## Non-obvious considerations

- **MLM compliance is a minefield.** Any positioning that could be read as
  endorsing an MLM business model needs legal review. Keep Canary's
  positioning strictly about the reseller's operational risk (shrink,
  fraud, ops), not about MLM recruiting or income claims.
- **Solex may have terms of use** about downstream product data usage.
  Level 1 (thinly disguised sandbox) sidesteps this; Level 2 may need
  written sign-off.
- **Reseller-to-reseller purchases skew chirp rule baselines.** Bulk orders
  look like abnormal volume. Rules need tuning, not just turned off.
- **Autoship recurring orders** can trip card-on-file rules or repeat
  transaction detection. Worth thinking through.
- **Square won't host some MLM categories.** Check Square's prohibited
  business list against Solex's actual product category before Level 2.
  If it's supplements, it may need an underwriting review.

---

## What I already know from initial recon

Full site of `solexglobal.com` is ~1MB — too dense to summarize inline.
The first task in Phase 1 is a proper read-through. Saved at
`/var/folders/gl/q3fw2kns0gsff15xgdqr0lmh0000gn/T/claude-hostloop-plugins/a6d1d0a6ad761998/projects/...` (temp
path — refetch when you start Phase 1, don't rely on the cache).

Canary's existing sandbox seller is a farmers-market metaphysical shop:
sage, crystals, palo santo, essential oils. Cute, but not representative
of MLM reseller patterns. That's exactly why the Solex profile is useful.

---

## Related Linear context

- **GRO-297** — Sandbox seeder extension for inventory/ordering. Should
  merge cleanly with Solex profile work.
- **GRO-326** — QA Agent (in-progress). Useful for running Solex
  scenarios interactively once the seeder is ready.
- **GRO-144, GRO-129** — Ops Dashboard + Owl. Will be demoed on the Solex
  merchant.

---

## Sizing

**Level 1 (sandbox-only):**
- Phase 1 (Solex research): 2-3 hours
- Phase 2 (current seeder audit): 1 hour
- Phase 3 (Solex seller spec): 2 hours
- Phase 4 (seeder code): 4-8 hours
- Phase 5 (scenarios): 4-6 hours
- Phase 6 (validation + demo): 2-3 hours
- **Total: 2-3 sessions**

**Level 2 (production):** add 4-8 sessions + external dependencies on
Solex rep + real reseller design partner. Not timeboxed.
