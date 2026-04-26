---
type: dispatch
status: ready-for-execution
date: 2026-04-25
target: laptop-side Claude Code (drives mini for production deployment via SSH)
priority: high (production deployment phase)
phase: 5 of 5 in NCR Counterpoint retail spine integration
prerequisite: Phases 0-4 complete + founder-approved; mini reconfig (`Brain/dispatches/2026-04-25-mini-reconfig-growdirect-asset.md`) complete
sdd: docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md
build-plan: docs/superpowers/plans/2026-04-25-ncr-counterpoint-spine-build.md
inputs:
  - All Phases 0-4 outputs (TSP adapter complete, all 13 modules implemented or deferred per plan)
  - Brain/wiki/ncr-counterpoint-sandbox-setup-checklist.md (operator prerequisites; per-customer parallel)
  - Brain/wiki/ncr-counterpoint-connection-runbook.md (technical bring-up)
tags: [canary, ncr-counterpoint, cutover, monitoring, phase-5, production-deployment]
---

# Dispatch — Phase 5: Cutover + Monitoring

## Operational discipline

Executes on the laptop; production deployment targets the mini via SSH (per ALXjr-mode). The first deployment is the Boutique Home & Garden chain — but Phase 5 produces **per-customer reusable artifacts**: a deployment runbook, a monitoring/alerting baseline, a capacity-planning model, rollback procedures. Each future customer reuses the runbook with customer-specific parameters.

## Why

Phases 0-4 build the Counterpoint integration capability. Phase 5 ships it. Two outputs:
1. **Per-customer deployment runbook** — template for any Counterpoint customer; first instantiation = the H&G chain
2. **Production monitoring baseline** — what's instrumented, what alerts, what capacity-plans for

Without Phase 5, Phases 0-4 are engineering-complete but not deployable. Phase 5 makes the integration operational.

## Pre-flight reading

1. All prior phase outputs (status check: every Phase 1-4 module's wiki article + dispatch acceptance criteria met)
2. `Brain/wiki/ncr-counterpoint-sandbox-setup-checklist.md` — operator prereqs (the customer side parallels this; their VAR enables API option, customer provisions credentials)
3. `Brain/wiki/ncr-counterpoint-connection-runbook.md` — technical bring-up (per-customer instantiation)
4. `Brain/wiki/ncr-counterpoint-api-reference.md` §"Caching policy" + §"Authentication detail" — relevant for production polling cadences + rotation
5. `Brain/dispatches/2026-04-25-mini-reconfig-growdirect-asset.md` — mini hosting target details
6. `docs/audit-2026-04-23/secret-rotation-runbook.md` — credential rotation procedure (Counterpoint per-customer creds rotate quarterly per SDD §3)

## Scope clarification questions ALXjr asks BEFORE code

1. **Cutover window** — for the H&G chain specifically: what's the cutover window? Hard switch (Square → Counterpoint, no overlap) or parallel-run (both feeding CRDM for a period to verify)?
2. **Monitoring sink** — where do alerts go? Linear / PagerDuty / Slack / email? Founder-only or escalation chain?
3. **Capacity-planning baseline** — what transaction volumes are expected per store? How many stores in the H&G chain (was 25 — confirm)? Sets baseline poll cadences + storage estimates.
4. **Rollback trigger criteria** — what failure modes trigger a roll-back to pre-deployment state? Adapter sync failure rate threshold? Detection false-positive rate threshold? Founder approval required for rollback decision?
5. **Customer notification** — does the customer's IT contact get a status portal, periodic reports, both? Sets the customer-facing artifacts.

## Operating procedure

### Sub-phase 5a — Per-customer deployment runbook (template)

1. Customer-side prerequisites checklist:
   - API option enabled in customer's `registration.ini` (via VAR — per `Brain/wiki/ncr-counterpoint-sandbox-setup-checklist.md`)
   - Counterpoint version v8.5.x or v8.6.x verified
   - Counterpoint API server installed at customer site (Windows host, .NET 4.5.2, port reachable)
   - Customer-issued Canary APIKey installed on customer's API server
   - Service-account credentials provisioned (`<company>.<service-user>` with appropriate role + endpoint permissions)
   - Network reachability: Canary infrastructure → customer's Counterpoint API server (typically Cloudflare Tunnel from customer site OR customer-firewall-allowed inbound from Canary)
2. Canary-side per-customer provisioning:
   - Tenant record in Canary (tenant_id, customer name, contact, deployment date)
   - Counterpoint company alias(es) registered (one tenant may have N companies)
   - Encrypted credential storage (per-tenant, per-company)
   - Initial sync schedule (start with backfill of N days; switch to incremental polling)
3. Smoke tests against the customer's API server (per `Brain/wiki/ncr-counterpoint-connection-runbook.md` §"Verify"): GET /SystemInfo → GET /Stores → GET /TaxCodes → GET /Customer/{any-known-id}
4. First sync execution: run backfill in dry-run mode; verify data shapes; flip to live mode after founder approval
5. Customer notification of go-live

### Sub-phase 5b — Production monitoring + alerting baseline

1. Per-endpoint sync telemetry (already in CRDM `sync_telemetry` table per SDD §7.4): timestamp, record count, latency, error count, error code breakdown
2. Drift alerts: if no records in expected window for a given endpoint
3. Auth alerts: any sustained 401 or 403 (creds invalid OR API option disabled)
4. Latency alerts: p95 latency > N seconds (threshold per endpoint type)
5. Volume alerts: record count outside expected band (under = sync stalled; over = anomalous activity)
6. Cache-staleness alerts: if `ServerCache: no-cache` response shows materially different data than recent cached reads
7. Detection-rule fire rate: if Module Q detection rate spikes > N% over baseline (could be real or rule-tuning issue)
8. Alert sink wiring: integrate with founder-decided channel (per scope question above)

### Sub-phase 5c — Capacity-planning model

1. Per-store transaction volume estimate (Documents/day × store-count)
2. CRDM storage projection (rows × bytes per entity × growth rate)
3. Adapter polling cadence calculator (vs. Counterpoint server caching policy + customer's request budget)
4. Memory-bus growth model (per new wiki article ingested via seed_clean.py extension)
5. Mini hosting capacity check (per `Brain/dispatches/2026-04-25-mini-reconfig-growdirect-asset.md`'s §"hardware/OS")

### Sub-phase 5d — Rollback procedures

1. Sync-failure rollback: stop adapter, mark tenant inactive, retain CRDM state (no data loss)
2. Schema-migration rollback (if any CRDM schema changes shipped): backward-migration scripts + retry path
3. Detection-rule rollback: revert to prior rule set, re-evaluate with backfilled data, surface false-positive incidents to operator
4. Full-tenant rollback: nuclear option — disable tenant, escalate to founder, post-mortem

### Sub-phase 5e — H&G chain first deployment

1. Apply 5a runbook with H&G-specific parameters (25 stores per the engagement scope; specific Counterpoint company alias TBD)
2. Run 5b monitoring baseline against H&G traffic
3. Validate Q detection allow-list with garden-center reality (cash-vendor-payments, item-code drift, mix-and-match flats — per `Brain/wiki/garden-center-operating-reality.md`)
4. Cutover handoff: H&G IT contact + operator runbook + escalation chain
5. Post-cutover monitoring window: tightened thresholds for first 30 days; relax to baseline after stabilization
6. Lessons-learned capture: what surprised us → wiki update for next customer

## Cross-cutting work (within this phase)

- **Per-tenant isolation** — every Phase 5 artifact is tenant-aware. Multi-customer parallel deployments must not bleed data or alerts across tenants.
- **Customer-success handoff** — by cutover, the customer's IT contact has a single point-of-contact at GrowDirect, a status portal or reporting cadence, and a defined escalation path.
- **Documentation as deliverable** — the runbook + monitoring baseline + capacity model + rollback procedures are themselves customer artifacts. They get sanitized templates in CATz proof-cases for reuse across future engagements.

## Out of scope

- Any Phase 0-4 module work — those are prerequisites, not in scope for Phase 5
- Module L native build (option d) — separate product roadmap track
- Module W native build (option d) — same
- Alternative payment rails (option e) — same
- Future-customer-specific tuning — happens at next-customer's Phase 5, not in this dispatch's scope

## Acceptance criteria

Phase-level:
- [ ] Per-customer deployment runbook produced + tested via H&G first deployment
- [ ] Production monitoring + alerting baseline live
- [ ] Capacity-planning model documented + validated against actual H&G traffic
- [ ] Rollback procedures documented + (where safe) tested
- [ ] H&G chain go-live successful: all stores syncing, detection rules in dry-run mode for 30 days, no critical alerts
- [ ] Customer-success handoff complete: H&G IT contact has the operator-facing artifacts
- [ ] Lessons-learned captured + wiki updated for next customer

Customer-facing artifacts:
- [ ] Customer-specific deployment summary (sanitized) → can be shared with the customer
- [ ] Operator runbook (internal) → on-call procedures
- [ ] Monitoring dashboard URL or equivalent
- [ ] Escalation chain documented

## Risks (Phase 5 specific)

- **First-customer deployment risk** — H&G is the first; surprises will surface. Plan: dry-run mode + tightened monitoring + 30-day stabilization window.
- **Customer's Counterpoint readiness** — API option must be enabled by their VAR before integration can run. Customer-side dependency; could delay cutover.
- **Cutover-window scope** — parallel-run vs. hard-switch is a customer call. Hard-switch is faster but riskier; parallel-run is safer but doubles operational load during overlap.
- **Detection false-positive rate at scale** — fixture suites approximate; real-customer data may surface patterns the rules misfire on. Mitigate with dry-run mode + operator-tunable thresholds.

## Reporting cadence

Sub-phase checkpoints at 5a (runbook draft), 5b (monitoring live), 5c (capacity model), 5d (rollback documented), 5e (H&G go-live + 30-day stabilization). Founder reviews each.

## Related

- `docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md` — full integration SDD
- `docs/superpowers/plans/2026-04-25-ncr-counterpoint-spine-build.md` — Phase 5 row
- `Brain/dispatches/2026-04-25-ncr-counterpoint-tertiary-modules.md` — Phase 4 (prerequisite, especially Q)
- `Brain/dispatches/2026-04-25-mini-reconfig-growdirect-asset.md` — mini hosting prerequisite
- `Brain/wiki/ncr-counterpoint-sandbox-setup-checklist.md` — operator prereqs (parallel for customer side)
- `Brain/wiki/ncr-counterpoint-connection-runbook.md` — technical bring-up (per-customer)
- `Brain/wiki/garden-center-operating-reality.md` — H&G-specific cutover considerations
- `docs/audit-2026-04-23/secret-rotation-runbook.md` — credential rotation
- (CATz) `proof-cases/specialty-smb-counterpoint-solution-map.md` — engagement-shape this Phase ships against

---

**Dispatch author:** Senior ALX (laptop), 2026-04-25
**Executor:** Laptop-side Claude Code (mini-targeting via SSH for hosting)
**Review gate:** Founder reviews each sub-phase output; H&G first deployment is a hard gate before reuse for next customer
