---
type: dispatch
status: ready-for-alxjr
date: 2026-04-25
target: claude-code-session on Mac mini (ALXjr namespace = ALX, Canary Retail Ops Agent)
priority: high
unblocks: Canary Counterpoint integration; Boutique H&G chain (Engagement 2) deployment readiness
parallel-with: 2026-04-25-secure-engagement-archive-deep-dive.md (still running on laptop)
inputs:
  - /Users/gclyle/GrowDirect/Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/ — public Counterpoint REST API repo (cloned 2026-04-25, 99 endpoints + 21K README + Basics + Installation docs)
  - /Users/gclyle/GrowDirect/Brain/wiki/canary-tsp-pipeline.md — current TSP architecture (Square source)
  - /Users/gclyle/GrowDirect/Brain/wiki/canary-data-model.md — current CRDM entity definitions
tags: [canary, tsp, crdm, counterpoint, integration, mini-dispatch, dispatch-driven]
---

# Dispatch — Rebuild TSP + CRDM for Counterpoint; Flow Data to CRDM First

## Operational discipline (read first)

This dispatch executes on the Mac mini under the production-dispatch-driven discipline. The mini's ALX does not do free-form work. This document is the programmed instruction. If anything is ambiguous, surface it for founder decision and wait — do not improvise.

## Why this exists

The Boutique Home & Garden chain (Engagement 2 retailer) runs NCR Counterpoint. Canary's existing TSP currently ingests Square. To support the chain — and to make Canary a Counterpoint-fluent platform beyond this one retailer — the platform needs to:

1. Rebuild the TSP to accept Counterpoint as a source (in addition to or replacing Square depending on scope answer below)
2. Refactor or extend the CRDM to handle Counterpoint's entity shapes
3. **Flow Counterpoint data into the CRDM first** — before any downstream Canary module (Chirp/Fox detection, analytics, dashboards) consumes it

"CRDM first" means: the canonical model is the priority destination. Get data INTO the canonical model; downstream modules read from it as designed. Do not bypass the CRDM, do not let adapters write directly to module-specific tables.

## Pre-flight reading (required before any code)

Before touching code, read in order:

1. `Brain/wiki/canary-tsp-pipeline.md` — current TSP architecture (the Square pipeline). Understand the adapter pattern, the boundary contract, where data lands.
2. `Brain/wiki/canary-data-model.md` — current CRDM entity definitions. Note which entities exist, which are populated by Square, and which are sparse.
3. `Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/README.md` — Counterpoint API entry point (~21K). Auth model, conventions, on-prem assumptions.
4. `Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/Basics/` — auth, conventions, headers.
5. `Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/InstallationAndConfiguration/` — what the customer's environment must look like for the API to be reachable.
6. The `Endpoints/` index. Identify the first-priority subset (8-12 endpoints) for analytics ingestion: transactions, ticket lines, items, customers, employees, returns/voids, discounts, store config, payment methods, taxes.

Produce a one-paragraph pre-flight summary covering: TSP architecture as it stands today, CRDM coverage, Counterpoint API's salient properties (auth, on-prem deployment, basic-auth via Counterpoint user creds, API user option gate at customer site).

## Scope clarification questions ALXjr asks BEFORE starting code

The directive uses the word "rebuild." Three scope dimensions need founder decision before code begins. Surface these and wait:

1. **Rebuild = extend or rewrite?** Extend = add a Counterpoint adapter alongside the existing Square adapter; both sources flow into the same CRDM. Rewrite = restructure the TSP architecture (e.g., source-agnostic core, adapter plugins, new abstraction). Likely intent is "extend" but confirm; the cost difference is large.
2. **CRDM changes — additive or breaking allowed?** Counterpoint's entity shapes may not match Square's exactly (e.g., Counterpoint distinguishes orders / tickets / line-items differently; has stronger employee + register modeling). Options: (a) translate at the adapter boundary so CRDM stays unchanged; (b) extend CRDM additively (new optional fields); (c) breaking changes with migration. Default to (a)→(b); never (c) without explicit authorization.
3. **Phasing.** Phase A only (Counterpoint adapter → CRDM, validate end-to-end with no downstream consumers wired)? Or A + downstream wiring in the same dispatch? Recommend Phase A only; downstream is a separate dispatch.

Wait for founder answers before proceeding to code. Do not guess.

## Operating procedure

1. **Pre-flight reading complete + summary produced.** Founder reviews; confirms understanding before scope questions.
2. **Scope questions answered.** Founder commits to extend-vs-rewrite, CRDM change posture, and phasing.
3. **Phase A — Counterpoint adapter:**
   a. Extract Counterpoint endpoint → CRDM entity mapping. Document as a table: each priority endpoint → which CRDM entity it populates → translation notes (field-to-field, type coercion, ID strategy).
   b. Define the adapter's boundary contract (Counterpoint API call → CRDM upsert). Idempotency strategy. Backfill vs. incremental cadence. Error/retry semantics.
   c. Implement the adapter as a new TSP source (parallel module to the Square adapter, same pattern).
   d. Tests against the public Counterpoint API surface (mock or NCR sandbox if accessible).
4. **Phase B — CRDM extensions (only if Phase A reveals gaps + founder authorizes):**
   a. Gap register: Counterpoint entity shapes the current CRDM doesn't represent.
   b. Proposed CRDM extensions (default: additive). Migration scripts for any DB schema changes.
   c. Backfill plan for the Square pipeline if CRDM additions affect it.
5. **Phase C — End-to-end flow validation:**
   a. Test fixture: representative Counterpoint API responses (transactions, items, customers, etc.) covering normal + edge cases.
   b. Flow fixture data through the adapter into CRDM. Verify entity counts, referential integrity, idempotency under replay.
   c. Validate against the SMB collapse principle: a single Counterpoint adapter should populate ~70% of the canonical capability surface for an SMB H&G retailer.
6. **Documentation:**
   a. Runbook: how to add a new Counterpoint customer (API option enable, auth setup, first sync, monitoring).
   b. Integration spec wiki article in `Brain/wiki/` summarizing the adapter pattern.
   c. Gap register: what's not covered, what would need additional work.

## Out of scope (do NOT do)

- Do NOT touch downstream Canary modules (Chirp, Fox, analytics, dashboards) in this dispatch. CRDM-first means CRDM is the only output target. Downstream wiring is a separate dispatch.
- Do NOT integrate against a specific customer's Counterpoint instance. This dispatch builds the adapter against the public API surface; customer-specific deployment (Boutique H&G) is a separate engagement.
- Do NOT deviate from the dispatch into free-form exploration. If scope ambiguity arises mid-execution, surface it for founder decision and wait.
- Do NOT commit code without founder review. Each phase produces drafts; founder reviews before merge.
- Do NOT chat with the founder about non-dispatch topics. Production discipline.

## Acceptance criteria

- [ ] Pre-flight reading complete; one-paragraph summary delivered
- [ ] Scope clarification questions answered by founder; commitments documented
- [ ] Phase A: Counterpoint adapter implemented; tests pass against public Counterpoint API surface
- [ ] Phase B: CRDM gap register produced; extensions implemented if authorized
- [ ] Phase C: end-to-end flow validated with fixture data; documentation produced
- [ ] Runbook + integration spec wiki article landed
- [ ] Memory-bus ingestion of the new wiki article (or explicit deferral note pending memory_bus.cli drift fix)

## Reporting cadence

- Checkpoint at end of each phase. Founder reviews before next phase begins.
- Surface blockers immediately; do not grind through ambiguity.
- Report format: one-page status — what's done, what's next, what's blocked.

## Related

- `dispatches/2026-04-25-rapid-pos-deep-dive.md` — original corpus-mining dispatch (now obsolete; the Counterpoint corpus is in hand and the integration target shifted from "RAPID-as-mystery" to "Counterpoint REST API"). Kept for provenance.
- `Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/` — local clone of the public Counterpoint API repo (this dispatch's primary input)
- `CATz/agents/ALXjr.md` — the persona executing this dispatch
- `Brain/wiki/canary-tsp-pipeline.md` — TSP architecture (input)
- `Brain/wiki/canary-data-model.md` — CRDM entity definitions (input)
- Memory: `project_sandbox_vs_mini_separation.md` — the production-dispatch-driven discipline this dispatch operates under

---

**Dispatch author:** Founder via senior ALX (laptop/sandbox), 2026-04-25
**Executor:** ALXjr / Mac mini (production-dispatch-driven)
**Review gate:** Founder reviews pre-flight summary, scope answers, and each phase output before the next phase begins
