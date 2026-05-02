# Disaster Recovery and Continuity

**Date:** 2026-05-02
**Status:** Draft v0 — founder review pending
**Scope:** Data restoration, infrastructure recovery, return-to-service procedures, and customer continuity in the face of data loss, region outage, or sustained provider failure. Companion to the Incident Response Plan ([[ir-plan-v0.1]]); this doc is the *static recovery architecture* that IR's dynamic response depends on.
**Siblings:**
- [[2026-05-02-agent-commissioning-protocol]] — agent identity and onboarding
- [[2026-05-02-platform-trust-boundary-architecture]] — auth and access posture
- [[ir-plan-v0.1]] — incident response (the dynamic complement)
- [[gcp-deployment-gateway]] — gateway deployment substrate
**Builds on:** [[platform-thesis]] (Cockroach Principle, Rail 4 vendor accountability) · [[concept-substrate-discipline]]

---

## Governing Thesis

**The only DR plan that exists is the one that has been exercised.** Untested DR is fiction. The platform's recovery architecture is the operating embodiment of two existing commitments — the Cockroach Principle (rebuild paths from any storage tier; losing one tier does not destroy the platform) and Rail 4 vendor accountability (multi-cloud capability is a power-diversification asset, exit is exercised quarterly, not contemplated). This doc translates those commitments into specific RPO/RTO targets per data class, the GCP substrate that delivers them, the runbooks that execute them, and the verification gates that confirm a restore is real.

The discipline is data-class-driven. A uniform "back everything up" policy buys the wrong protection at the wrong cost. The evidentiary rail (L2 hash-anchored evidence chain, Fox case records) cannot tolerate loss; the analytics rollups can be regenerated overnight. Same platform, different recovery posture per tier.

---

## Recovery Tiers — Aligned to the Cockroach Principle

The platform thesis already defines four storage tiers per the Cockroach Principle: **S1 hot, S2 warm, S3 cold, S4 chain anchor.** Each tier carries its own RPO/RTO target, its own substrate, its own restore procedure. Losing a single tier degrades; losing all tiers simultaneously is the architectural worst case the recovery architecture is designed against.

### Tier matrix

| Tier | Examples | RPO target | RTO target | GCP substrate | Restore mechanism |
|---|---|---|---|---|---|
| **S1 — hot** | Active transactional Postgres rows (POS events, case management, customer/item/price), Memorystore session and cache | ≤5 minutes | ≤4 hours | Cloud SQL HA + PITR (binlog retention 7 days minimum, 30 days recommended) + cross-region read replica | PITR from primary; failover to cross-region replica if primary region unreachable |
| **S2 — warm** | Recent backups (daily snapshots), Cloud Logging (operational), Cloud Trace, recent embeddings | ≤24 hours | ≤8 hours | Cloud SQL automated backups (35-day retention) + Cloud Logging buckets (30-day retention) + GCS standard tier | Restore from snapshot to staging instance, validate, promote |
| **S3 — cold** | Long-term audit logs, archival Postgres exports, historical embeddings, deprecated tenant data under retention obligation | ≤7 days | ≤72 hours | GCS Nearline / Coldline with lifecycle policy + Cloud SQL exports to GCS (weekly) | Restore archive to staging Cloud SQL, validate, promote or expose for audit |
| **S4 — chain anchor** | L2 blockchain anchor records, hash-chain manifests, evidence chain | ~0 (architecturally cannot lose) | ≤2 hours | GCS multi-regional bucket with Object Versioning + Object Lock + L2 chain itself (external substrate) | Verify chain integrity from L2; reconstitute manifest from anchored hashes; rebuild local index |

### RPO/RTO discipline

- **RPO** (recovery point objective) = how much data we are willing to lose. S4 is ~0 because the chain is the evidentiary rail and loss is not a contract we can write. S1 is 5 minutes because Cloud SQL PITR substrate makes 5-minute RPO cheap; tightening to ~0 (synchronous cross-region replication) is a cost decision worth taking only when a regulated tenant demands it.
- **RTO** (recovery time objective) = how long the customer waits for restoration. S1 is 4 hours because that is the realistic span of a primary-region failover including verification gates; aspiring to 1 hour requires active-active multi-region (a Phase 2 architectural change, not a runbook improvement).
- **Targets are commitments, not aspirations.** Every quarterly DR exercise (§Exercise Cadence) measures actual restore time against target. Failures are postmortemed; targets are revised when reality persistently disagrees.

---

## Substrate Per Tier — What Backs Up What

### S1 — Hot transactional data

**Cloud SQL Postgres 17 with HA configuration:**
- Regional HA enabled — synchronous standby in a different zone within the primary region
- PITR enabled with 7-day binlog retention (recommend 30-day for audit-significant tenants)
- Automated backups daily, retained 35 days
- Cross-region read replica in a paired region (e.g., `us-east1` if primary is `us-central1`); promotable on primary-region loss

**Memorystore Redis:**
- BASIC tier acceptable for v0 staging because cache loss is recoverable from Postgres (Streams events durable in Postgres via the Sub 1 substrate per [[gcp-deployment-gateway]])
- STANDARD tier with HA replica for production (~$75/mo at 1 GB)
- No cross-region replica needed; recovery is a fresh Memorystore instance + cache warm-up from Postgres

**Cloud Run service revisions:**
- All revisions retained in Artifact Registry; rollback is a traffic split, not a code change
- Revision history acts as immutable backup of the *application* itself

### S2 — Warm operational data

**Daily Cloud SQL snapshots:**
- Retained 35 days (Cloud SQL automatic backup retention)
- Restored to staging instance for verification, promoted via DNS/connection-string cutover

**Cloud Logging:**
- 30-day retention default; longer for tenants under contractual audit obligations (per [[ir-plan-v0.1]] §detection sources)
- Export to GCS for >30-day retention; export to BigQuery for analytical recovery

**Embeddings (memory bus, qwen3-embedding:8b):**
- Source data (Brain wiki, SDDs) is the canonical record; embeddings are derived
- Embedding index lost = re-seed via `services/memory-bus/scripts/seed_standalone.py`; expected runtime ~15min for current corpus
- Daily Cloud SQL snapshot covers the embedding index as a side effect

### S3 — Cold archival data

**Cloud Storage Nearline / Coldline with lifecycle policies:**
- Postgres weekly logical exports to GCS Nearline; promoted to Coldline at 90 days
- Long-term audit log retention per regulatory requirement (e.g., 7 years for financial records under specific tenant contracts)
- Retrieval cost is non-trivial; restore from S3 requires a planned operation, not an emergency response

**Lifecycle policy hard rules:**
- No deletion lifecycle policy on any S3 bucket. Manual deletion only, with founder authorization, with evidentiary chain anchor of the deletion event.
- Object Versioning enabled on every S3 bucket.
- Cross-region replication to a paired region for tenants under contractual data residency requirements.

### S4 — Chain anchor (the evidentiary tier)

**This is the load-bearing tier.** The platform thesis depends on the evidence chain being incontrovertible. Recovery architecture treats S4 as fundamentally different from S1–S3.

**GCS multi-regional bucket with Object Versioning + Object Lock:**
- Anchor records (L2 hashes, manifest files, evidence chain) stored with retention lock per evidentiary policy
- Multi-regional storage class — survives single-region loss without operator action
- Object Lock prevents deletion within the retention window even by an authenticated admin (defends against insider compromise)

**The L2 chain itself is the external substrate:**
- Anchored hashes published to a Bitcoin L2 (or equivalent) — the chain is recoverable from any L2 node, not from us
- Local manifest index can be reconstituted from the L2 chain plus the hashed source data
- Worst-case S4 recovery: rebuild the manifest by re-walking anchored hashes from the L2 chain. Operationally heavy; architecturally guaranteed.

**Verification on restore is mandatory and non-negotiable.** A restored S4 surface must pass hash-chain integrity verification end-to-end before it is permitted to serve traffic. A surface that cannot prove its chain is the chain does not get to be the chain.

---

## Code, Knowledge, and Configuration Backups

These are not "data tiers" but they need recovery posture. Most of them are already covered by their existing substrate; this section names them explicitly so we do not assume.

| Asset | Backup substrate | Recovery time |
|---|---|---|
| Application code | GitHub (`growdirectprez/GrowDirect` and downstream public repos) | Continuous; clone is the recovery |
| Container images | Artifact Registry, retained per project policy | Immediate; pull image |
| Brain wiki, SDDs, dispatches | GitHub via the `GrowDirect` repo | Continuous; clone is the recovery |
| Memory bus embeddings | Re-derivable from Brain via `seed_standalone.py` | ~15min restore from source |
| Infrastructure-as-code (if any) | TBD — see Open Question 1 | n/a until IaC adopted |
| Secret Manager records | Versioning enabled (Cloud-native); export not recommended (defeats the purpose) | Restore prior version via Secret Manager UI/API |
| IAM policy | Documented in [[gcp-foundation-runbook]] and [[gcp-deployment-gateway]]; audit log captures all changes | Re-apply from runbook documentation |
| DNS (Cloudflare) | Cloudflare's own redundancy + zone export to Git | Manual zone import from exported file |
| Cloud SQL configuration (instance specs, flags) | Documented in [[gcp-deployment-gateway]]; should also live in Terraform per Open Question 1 | Re-create from documentation |

**The implicit backup that is not implicit:** the founder's local laptop. Recovery from "the founder's laptop is bricked" is fully covered by Git remotes (code + knowledge) and GCP-resident state (production data). The laptop is a workstation, not a system of record. This is intentional and worth re-confirming after any laptop-side workflow change.

---

## Restore Procedures — The Runbook Spine

Each restore is a documented runbook in `Brain/templates/runbook` format, executable by an on-call (which is the founder, at 3am, with adrenaline) without ambiguity. v0 of this doc names the runbooks; the runbooks themselves are written as separate dispatches.

| Runbook | Trigger | Tier(s) involved | Status |
|---|---|---|---|
| `runbook-cloud-sql-pitr-restore.md` | S1 data corruption within PITR window | S1 | Draft pending dispatch |
| `runbook-cloud-sql-cross-region-failover.md` | Primary region unavailable, cross-region replica promotion | S1 | Draft pending dispatch |
| `runbook-cloud-sql-snapshot-restore.md` | S2 restore from automated backup beyond PITR window | S1, S2 | Draft pending dispatch |
| `runbook-gcs-restore-from-archive.md` | S3 archival data retrieval (planned, not emergency) | S3 | Draft pending dispatch |
| `runbook-evidence-chain-verify-and-rebuild.md` | S4 chain integrity event; rebuild local manifest from L2 anchors | S4 | **Critical — draft this first** |
| `runbook-secret-manager-rollback.md` | Compromised or accidentally rotated secret needs prior version restored | n/a (secret tier) | Draft pending dispatch |
| `runbook-multi-cloud-exit.md` | Sustained GCP outage or compromise; cutover to alternate cloud | All tiers | Phase 2 — quarterly exercise per Rail 4, runbook before first exercise |
| `runbook-customer-comms-during-incident.md` | Any S0/S1 per [[ir-plan-v0.1]] | n/a | Sibling to IR plan |

Each runbook contains:
- Trigger conditions and severity escalation per [[ir-plan-v0.1]]
- Pre-restore verification (do not restore over good data)
- Exact commands (gcloud, psql, scripts) — no narrative
- Post-restore verification gates (next section)
- Rollback procedure if restore goes wrong
- Communication checkpoints (who tells whom at which step)
- Postmortem trigger and template reference

---

## Return-to-Service Verification Gates

A restore that has not been verified is not a restore. Every runbook ends with a verification gate appropriate to the tier.

### S1 — Hot transactional data
- Schema verification: migrations applied, expected version present
- Reference data integrity: ARTS POSLOG reference tables present and unchanged
- Smoke test: synthetic webhook → case creation → dashboard render path
- Per-tenant spot check: pick 3 random tenants, confirm their last 24h transaction tail
- RLS policy active: connection without `app.current_tenant_id` set returns zero rows

### S2 — Warm operational data
- Snapshot vintage matches expected timestamp
- Sample query against expected pre-incident state matches recorded sample
- Cross-tier consistency: S1 transactional data references resolve

### S3 — Cold archival data
- Object integrity: GCS object hash matches recorded hash at archival time
- Sample retrieval: random sample from archive opens and parses

### S4 — Chain anchor (the load-bearing verification)
- **Hash chain end-to-end verification**: every anchored hash in the restored manifest verifies against the L2 chain
- **Fox case chain verification**: every Fox case's evidence chain reconstitutes from the anchor manifest
- **No partial restoration permitted**: a chain that fails verification at any link does not serve traffic; the operator escalates to founder before any decision to publish from a partially-verified chain
- **Reconstitution decision log**: any chain reconstruction is itself an evidentiary event, anchored in the chain post-restore

**The verification gate is the moment of trust.** Restoration without a verification gate is hopeful copying. The gate is what turns the restored substrate back into the substrate.

---

## Failover Topology — v0 vs Phase 2

### v0 (current — single region with cross-region backup recovery)

- Primary region: `us-central1` (Iowa)
- Paired backup region: `us-east1` (South Carolina) — geographically separated, low-latency network path, low cross-region egress cost
- Cross-region read replica for Cloud SQL — promotable on primary-region loss (RTO 1–4 hours)
- Cross-region GCS replication for S4 evidence anchors and S3 archives
- Cloud Run is regional but image is in Artifact Registry (regional, paired); re-deploy to backup region in 30–60 minutes
- DNS cutover via Cloudflare (manual or automated; see Open Question 4)
- **This topology is correct for our scale.** Active-active multi-region is operationally heavier than warranted at MVP traffic and ~$50M ICP scale.

### Phase 2 (active-active multi-region — when warranted)

Trigger conditions for Phase 2:
- A regulated tenant contract demands sub-1-hour RTO
- Sustained traffic profile that makes cross-region failover risk (5+ minute write loss during failover) commercially material
- The SMB Health vertical at HIPAA scale where downtime carries patient-safety implications

Phase 2 architecture would introduce:
- Cloud Spanner or AlloyDB cross-region for Tier S1 data
- Active-active Cloud Run with global load balancer routing
- Conflict resolution policy for any tenant data that may diverge during failover
- Operationally heavier — adds a multi-master complexity tax we do not pay until we have to

### Multi-cloud exit posture (per [[platform-thesis]] Rail 4)

- Multi-cloud is a *power-diversification* commitment, not a steady-state operating model
- Exit is exercised quarterly per Rail 4 — not contemplated, not theoretical, *exercised*
- The exit substrate is documented in `runbook-multi-cloud-exit.md` (to be written before first exercise)
- The exercise scope: bring up the stack on AWS or Azure from cold backup, validate against return-to-service gates, document drift, tear down. Cost: meaningful but not prohibitive at MVP scale; the *exercise* discipline is the value, the resulting alternate stack is teardown-ready.

---

## Exercise Cadence

| Cadence | Exercise | Owner |
|---|---|---|
| Monthly | Snapshot restore to staging — pick a random S1 snapshot, restore, run verification gates | Eng on-call |
| Quarterly | Cross-region failover exercise — promote replica in backup region, smoke-test, fail back | Founder + on-call eng |
| Quarterly | Multi-cloud exit exercise (Rail 4 commitment) — bring up stack on alternate cloud, validate, tear down | Founder |
| Annually | Full DR drill — simulate primary region loss, execute full failover, hold for 24h, fail back. Postmortem published. | Founder + on-call eng + counsel |
| Annually | Evidence chain verification audit — full S4 chain walk, third-party verifier if available | Founder + counsel |
| On every quarterly exercise | Update this doc with measured RPO/RTO actuals; adjust targets if reality persistently disagrees | Founder |

**The first exercise is the one that finds the broken assumption.** The IAM grant that doesn't exist in the failover region. The secret that wasn't replicated. The hardcoded URL in a config file. Plan accordingly: the first exercise of any new runbook is scheduled with extra time and treated as research, not validation.

---

## Customer Communication During Recovery

The IR plan ([[ir-plan-v0.1]] §Communications) covers incident communications. This section covers the *recovery-specific* communication discipline.

For the v0 ICP (private retail businesses up to ~$50M, founder selling personally), customer comms during a recovery event is **the founder calling the affected merchants directly**. Not a status page. Not an email blast. A phone call.

Reasons this is the right v0 posture:
- The customer base is small enough that per-merchant calls are operationally feasible
- The founder relationship is the differentiator at this scale; outsourcing it during an incident is the wrong moment to outsource
- A status page suggests a scale of operation we do not have; a personal call demonstrates the accountability rail we do

Reasons this graduates at scale:
- Customer base growth past ~50 active merchants makes per-call comms operationally infeasible
- A 24/7 status page becomes table-stakes as soon as the merchant base spans time zones or includes contracted-uptime accounts
- Phase 2 comms infrastructure: status.growdirect.io (or equivalent), automated incident timelines, per-tenant impact assessments

**The graduation trigger is operational, not aspirational.** Build the status page when the call list exceeds the founder's available hours during a typical incident; not before.

---

## Open Questions

These are the choices I cannot make for you. v1 of this doc resolves them.

1. **Infrastructure-as-Code adoption — Terraform now or after stabilization?** The current state is partly documented (per [[gcp-deployment-gateway]]), partly tribal. Terraform makes the configuration itself a first-class backed-up artifact. Recommend: Terraform-from-day-one for *new* GCP resources; document existing resources in `import` blocks rather than re-creating. Worth a sibling SDD if we agree.
2. **Cross-region read replica enablement — when does Phase 1 turn it on?** Replica adds ~$50/mo for our MVP scale. Worth turning on now if the founder wants quarterly cross-region failover exercises to be real (per Rail 4); worth deferring if MVP cost discipline is the higher priority. Recommend: enable now, treat as the cost of the Rail 4 commitment.
3. **Multi-cloud exit substrate — AWS or Azure as the secondary?** Both work. AWS has the deeper SMB and partner ecosystem; Azure has the M365 / SMB Health integration story per [[vertical-smb-health-hypothesis]]. Recommend: AWS for v0 (broader ecosystem, more documented patterns); Azure becomes the secondary-secondary if SMB Health vertical demands it.
4. **DNS cutover automation — manual via Cloudflare dashboard or scripted via API?** Manual is simpler and operator-attention-forcing during an incident. Scripted is faster but adds complexity to test and risk to maintain. Recommend: scripted with a manual confirmation step (operator runs the script, script asks "are you sure" with the diff, operator confirms).
5. **Customer comms graduation trigger — exact merchant count threshold?** Recommend: ~50 active merchants OR first contracted-uptime SLA, whichever comes first. Earlier than that and we are pre-paying operational complexity for a problem we don't have.
6. **Evidence chain verification — third-party verifier substrate?** A trusted third-party verifier of the L2 chain integrity strengthens the evidentiary rail's credibility (especially for litigation use). Worth scoping; not v0 critical. Founder gate: who would the trusted third party be — a notary service, a partnered law firm, or a customer-selected verifier?
7. **Backup retention beyond Cloud SQL's 35-day default — for tenants under regulatory holds?** Specific tenants may have legal-hold or regulatory-retention requirements that exceed Cloud SQL's standard backup window. Recommend: per-tenant retention extension via weekly logical exports to GCS Coldline, retained per the tenant's contractual or regulatory window. Worth surfacing in onboarding so we don't discover the requirement after the fact.

---

## Related

- [[ir-plan-v0.1]] — incident response (the dynamic complement to this static recovery architecture)
- [[platform-thesis]] — Cockroach Principle (S1/S2/S3/S4) and Rail 4 vendor accountability
- [[concept-substrate-discipline]] — fractal rule for substrate vs module separation
- [[gcp-deployment-gateway]] — gateway-level deployment substrate
- [[gcp-foundation-runbook]] — substrate provisioning state and IAM policy
- [[2026-05-02-platform-trust-boundary-architecture]] — sibling SDD for auth and access posture
- [[2026-05-02-agent-commissioning-protocol]] — agent identity model
- [[breach-runbook-v0.1]] — Personal Data breach branch under [[ir-plan-v0.1]]
- Future: `runbook-evidence-chain-verify-and-rebuild.md` — the load-bearing S4 runbook
