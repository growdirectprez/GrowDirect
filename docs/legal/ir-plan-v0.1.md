# Incident Response Plan — Canary Protocol (v0.1)

**Status:** v0.1 working document — outside-counsel review required before first activation.
**Owner:** GrowDirect LLC (Canary Protocol)
**Last reviewed:** 2026-05-02
**Source dispatch:** GRO-693
**Scope:** Security incidents broadly — DDoS, key compromise, infrastructure failure, ransomware, supply-chain attack, sub-processor incident
**Companion:** [Breach Runbook v0.1](./breach-runbook-v0.1.md) — scoped specifically to Personal Data breaches under GDPR / state breach laws

---

## 0 · Governing thesis

The IR plan reflects three commitments that distinguish Canary from generic SaaS incident response:

1. **The Cockroach Principle is a recovery asset.** The architecture (per `Brain/wiki/cards/platform-thesis.md` and supporting SDDs) maintains rebuild paths from any tier. S1 (hot) / S2 (warm) / S3 (cold) / S4 (chain anchor) — losing any one tier does not destroy the platform. Recovery is measured, not improvised.
2. **Multi-cloud capability is a power-diversification asset, not just a portability one.** Per platform-thesis Rail 4 (cloud-vendor accountability), credible exit is maintained quarterly. In a sustained provider outage or compromise, exit is exercised, not contemplated.
3. **The evidence chain is the war-room's source of truth.** During an incident, every operator action that touches a system of record gets logged and anchored. After the incident, the chain provides an independently verifiable timeline of who did what when — both for external review (regulator, insurer, customer) and for internal postmortem accuracy.

This plan covers all security incidents. Personal Data breaches are a subclass — the [breach runbook](./breach-runbook-v0.1.md) is the authoritative document for that branch.

---

## 1 · Severity tiers

| Tier | Definition | Example | Activation |
|---|---|---|---|
| **S0 — critical** | Customer-facing service down, or confirmed Personal Data breach (→ breach runbook), or active intrusion in progress | Cloud SQL primary unreachable; ransomware encryption observed; key compromise with active session | All-hands; founder + on-call eng + counsel + insurance immediately |
| **S1 — high** | Significant degradation; partial service down; high-confidence security event with scope undetermined | DDoS exceeding rate-limiter; sub-processor advisory affecting our environment; suspected compromise without confirmed access | On-call + founder; counsel notified; war-room established |
| **S2 — moderate** | Service degradation isolated to single component; no PII implication | Cache layer down; Pub/Sub consumer lag; failed-login burst on single account | On-call; founder informed |
| **S3 — low** | Operational issue caught before customer impact | Monitor false positive; pre-emptive failover triggered; planned maintenance overrun | On-call only; logged for trend tracking |

---

## 2 · Roles

| Role | Responsibility | Current assignee | Backup |
|---|---|---|---|
| **Incident Commander (IC)** | Owns the incident; runs the war room; calls severity; signs off on actions | Founder | On-call eng (rotates) |
| **Eng on-call** | Executes containment, recovery, forensic preservation | On-call eng | Backup on-call |
| **Counsel** | Legal exposure assessment; notification authorization; communications review | [VERIFY] outside counsel — not yet retained | N/A (S0/S1 cannot proceed without counsel) |
| **Communications** | Customer / regulator / press communications | Founder | Counsel |
| **Customer comms** | Direct customer notifications | Founder | On-call eng |
| **Insurance liaison** | Cyber-liability carrier notification and coordination | Founder | [VERIFY] insurance broker |
| **Scribe** | Continuous incident log; timestamps every decision | On-call eng (or designate) | IC |

[COUNSEL REVIEW] — The IR plan cannot operate at S0 / S1 without retained outside counsel. GRO-693 does not retain counsel; the dispatch produces the documents counsel will eventually review. Founder must retain counsel before the first production incident at S1+. This is on the founder's path to launch, not deferrable.

[VERIFY] — Cyber-liability insurance broker and policy must be in place before processing live merchant data. Track in the cyber-liability underwriting workstream (GRO-686 through GRO-699). Per memory `feedback_insurance_prereq_compliance`, those dispatches map 1:1 to underwriting questionnaire items.

---

## 3 · Detection sources

| Source | Signals | Severity gate |
|---|---|---|
| Cloud Audit Logs (GCP) | IAM grants, key creation attempts, admin API calls | Per audit policy → S0/S1/S2 |
| Application logs | Errors, latency anomalies, audit-event anomalies | S2 baseline; S1 on PII implication |
| Cloud Monitoring alerts | Service-level objective violations; resource exhaustion | S2 baseline; S1 on customer impact |
| Cloudflare WAF | Attack pattern bursts; rate-limiter triggers | S2 baseline; S1 on rate-limiter overrun |
| Sub-processor advisories | GCP Security Command Center; Cloudflare advisories; OrdinalsBot or Lightning provider notifications | Per advisory severity |
| Evidence chain monitor | Anchor failure; verification mismatch | S1 — chain integrity is core IP |
| External — researcher / customer / vendor | `security@growdirect.io` reports | S1 minimum until triaged |
| External — regulator / law enforcement | Subpoena, inquiry, advisory | S0 — counsel-led from intake |

---

## 4 · Activation flow

```
Detection signal arrives
    ↓
On-call eng triages within 15 minutes
    ↓
Severity assigned (§1)
    ↓
S2/S3 → on-call manages; founder informed at end of shift
S1    → activate war room; notify founder + counsel within 1 hour
S0    → activate war room immediately; notify founder + counsel + insurance within 30 minutes
    ↓
War room established (§5)
    ↓
Containment → recovery → postmortem
```

---

## 5 · War-room procedures

| Element | Specification |
|---|---|
| **Activation criterion** | S0 or S1 |
| **Channel** | Dedicated Slack / chat channel `inc-YYYY-MM-DD-NN` plus video bridge for active phases |
| **Roll call (first 5 min)** | IC, on-call, scribe minimum. Counsel and insurance dialed in for S0 |
| **Log discipline** | Every decision recorded with timestamp; every action recorded with operator + timestamp; scribe maintains the log; log committed to incident card every 30 min |
| **Decision authority** | IC has final call. Counsel has veto on regulatory / customer comms. Founder has veto on commercial decisions |
| **Status cadence** | Internal status update every 60 min (S0) or 120 min (S1); external status update at IC's discretion with counsel review |
| **Stand-down criterion** | IC declares; recovery validated; forensic preservation complete; postmortem owner assigned |
| **Anchor cadence** | Forensic captures and key decision points anchored to evidence chain in real time during the incident |

---

## 6 · Containment patterns by incident type

### 6.1 · DDoS

| Step | Action |
|---|---|
| 1 | Confirm Cloudflare WAF is engaged at appropriate ruleset; escalate to higher-tier protection if available |
| 2 | Rate-limit aggressive sources at edge; do not blackhole legitimate traffic |
| 3 | Notify customers if customer-facing latency exceeds SLA |
| 4 | If sustained: engage Cloudflare support; coordinate with GCP networking |
| 5 | Postmortem: capacity planning + WAF rule update |

### 6.2 · Key compromise (service account, KMS, secret)

| Step | Action |
|---|---|
| 1 | Immediately disable the compromised credential / rotate the key |
| 2 | Audit all activity by the credential since last known-good state via Cloud Audit Logs |
| 3 | If activity touched Personal Data → escalate to breach runbook |
| 4 | Rotate dependent credentials (defense in depth); reissue with least-privilege scope review |
| 5 | Anchor compromise window and rotation event to evidence chain |
| 6 | Postmortem: how was credential exposed; tightening of KMS / Secret Manager access |

### 6.3 · Infrastructure failure (Cloud SQL, Cloud Run, Pub/Sub)

| Step | Action |
|---|---|
| 1 | Confirm scope: single-zone, single-region, single-service, or broader |
| 2 | Failover to standby (Cloud SQL HA) or scale alternate path |
| 3 | If sustained provider issue: assess multi-cloud exit per platform-thesis Rail 4 |
| 4 | Customer comms: status page update within 15 min of confirmed customer-facing impact |
| 5 | Recovery: verify data integrity post-failover via evidence-chain comparison; backfill any gap |
| 6 | Postmortem: provider SLA assertion; credit claim filed; multi-cloud drill scheduled if not recent |

### 6.4 · Ransomware

| Step | Action |
|---|---|
| 1 | Isolate affected workloads from network immediately |
| 2 | Do not pay ransom; do not negotiate with attacker without counsel |
| 3 | Verify backups are intact and not encrypted (immutable bucket isolation should prevent this — confirm) |
| 4 | Restore from clean backup; rebuild affected services from container images in immutable Artifact Registry |
| 5 | Forensic preservation of attacker artifacts before wipe |
| 6 | Treat as S0 breach if PII could have been exfiltrated; activate breach runbook in parallel |
| 7 | Notify FBI IC3 and applicable state law enforcement per counsel guidance |
| 8 | The Cockroach Principle — every tier is independently rebuildable; ransomware on any single tier does not require ransom payment |

### 6.5 · Supply-chain attack (compromised dependency)

| Step | Action |
|---|---|
| 1 | Identify scope of dependency usage (which services depend on which version) |
| 2 | Pin to last-known-good version; rebuild and redeploy affected services |
| 3 | Audit logs for indicators-of-compromise specific to the dependency advisory |
| 4 | If compromise period overlaps production exposure: forensic preservation + breach runbook activation |
| 5 | Update dependency management process if structural gap identified |

### 6.6 · Sub-processor incident

| Step | Action |
|---|---|
| 1 | Receive advisory from GCP / Cloudflare / OrdinalsBot / Lightning provider |
| 2 | Assess Canary's exposure to the specific advisory |
| 3 | Apply provider-recommended mitigations |
| 4 | If our environment is affected → activate appropriate IR branch (key rotation, breach runbook, etc.) |
| 5 | Notify Merchants if our service is affected; reference sub-processor advisory in notification |
| 6 | Postmortem: sub-processor selection / contractual SLA review |

---

## 7 · Recovery validation

Recovery is not declared until:

| Check | Method |
|---|---|
| Service is fully operational | Synthetic monitor passes; customer traffic patterns normal |
| Data integrity is verified | Evidence-chain anchors compared against current state; no record drift |
| Compromise vectors are closed | New credentials issued; old credentials confirmed inactive in audit logs; affected vulnerability patched |
| Forensic preservation is complete | Snapshots, log exports, container images captured per breach runbook §5 |
| Customer comms are aligned | Status page reflects current state; no open customer escalations referencing the incident |
| Postmortem owner is named | Linear issue assigned with due date |

The IC declares recovery. Recovery declaration anchors to the evidence chain.

---

## 8 · Multi-cloud exit drill (planned, per platform-thesis Rail 4)

| Element | Specification |
|---|---|
| Cadence | Quarterly |
| Drill type | Tabletop (Q1 / Q3) and live partial-failover (Q2 / Q4) |
| Acceptance criterion | Production traffic served from alternate provider within stated RTO; data integrity verified via evidence chain |
| Owner | Founder + on-call eng |
| Output | Drill log committed to `Brain/wiki/cards/`; runbook and infrastructure gaps tracked as Linear issues |

[COUNSEL REVIEW] — Multi-cloud capability is a competitive and accountability commitment per platform-thesis Rail 4, but it is also expensive to maintain. Confirm with counsel that we do not need to *contractually commit* multi-cloud capability to merchants in v0.1 — it is an internal posture and a marketing claim, not a customer SLA term, until otherwise decided.

---

## 9 · Tabletop exercises

| Frequency | Scenario | Output |
|---|---|---|
| Quarterly | One scenario per quarter (rotate through DDoS, key compromise, infrastructure failure, ransomware, sub-processor incident, breach) | Replay notes; runbook revisions; gap-tracking Linear issues |
| Pre-launch | Full IR-plan tabletop with founder + counsel + on-call | Sign-off that team is ready to operate |
| Post-incident | Replay the incident with the then-current runbook within 90 days | Runbook diff; updated playbooks |

---

## 10 · Connections to other documents

| Document | Connection |
|---|---|
| [`breach-runbook-v0.1.md`](./breach-runbook-v0.1.md) | The Personal Data branch of this IR plan. When an incident escalates to confirmed PII exposure, the breach runbook governs |
| [`dpa-template-v0.1.md`](./dpa-template-v0.1.md) | DPA §7 (Security measures) and §8 (Sub-processors) — the contractual commitments this plan operationalizes |
| [`subprocessor-list-v0.1.md`](./subprocessor-list-v0.1.md) | Sub-processor advisory channels (§3, §6.6) |
| `Brain/wiki/cards/platform-thesis.md` | The four accountability rails — Rail 4 (cloud-vendor) is operationalized here in §6.3 and §8 |
| `Brain/wiki/cards/gcp-foundation-runbook.md` | GCP project / IAM baseline that this plan assumes |
| GRO-693 | The dispatch that produced this plan |
| GRO-695 | QSA engagement (PCI Service Provider scope) |
| GRO-686 through GRO-699 | Cyber-liability insurance prereqs — must close before live merchant data |

---

## Counsel Review Required (consolidated)

1. **§2 roles** — outside counsel must be retained before any S0/S1 incident
2. **§2 insurance** — cyber-liability carrier and broker must be in place before live merchant data
3. **§6.4 ransomware** — confirm "do not pay" policy is consistent with insurance carrier requirements; some policies allow ransom payment under specific conditions
4. **§8 multi-cloud** — confirm we are not contractually committing multi-cloud to merchants in v0.1
5. **§10 PCI integration** — coordinate with GRO-695 QSA engagement for IR-plan elements that map to PCI-DSS §12.10 (Incident Response)

---

## Change log

| Version | Date | Changes |
|---|---|---|
| v0.1 | 2026-05-02 | Initial working plan — GRO-693 |
