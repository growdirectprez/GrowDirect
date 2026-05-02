# Data Breach Response Runbook — Canary Protocol (v0.1)

**Status:** v0.1 working document — outside-counsel review required before first activation.
**Owner:** GrowDirect LLC (Canary Protocol)
**Last reviewed:** 2026-05-02
**Source dispatch:** GRO-693
**Scope:** Personal Data breaches under GDPR Art. 33-34, US state breach-notification laws, and CCPA §1798.150
**Companion:** [IR Plan v0.1](./ir-plan-v0.1.md) — broader incident response (DDoS, key compromise, infrastructure failure, ransomware)

---

## 0 · Governing thesis

Three things distinguish breach response in Canary from generic SaaS:

1. **Time is the regulator's currency.** GDPR Art. 33 demands notification to the supervisory authority **within 72 hours of awareness**. State breach laws range from "without unreasonable delay" to fixed windows (e.g., Florida 30 days, Texas 60 days, Vermont 14 days). The runbook is built to make the GDPR clock — slower clocks fall out for free.
2. **The evidence chain is a forensic asset, not a liability.** Every consequential record was hash-anchored to public Bitcoin L2 at creation time (USPTO Application 63/991,596). Any claim that records were tampered with after the fact is independently verifiable. This shortens the forensic phase and strengthens the regulator narrative.
3. **The scope question is answered by architecture, not by audit.** Card data does not flow through Canary (DPA §7.4). A breach of Canary cannot be a cardholder-data breach. A breach **affects** PCI scope only if the merchant's other systems are also compromised — and that is the merchant's IR plan, not Canary's.

---

## 1 · Detection signals

| Source | Signal | Tier (initial) |
|---|---|---|
| Cloud Audit Logs (GCP) | Unauthorized IAM role grant; service account key creation attempt; admin-level API call from unfamiliar source | S0 / S1 |
| Application audit log | Unauthorized data export; admin-tool invocation outside business hours from unfamiliar IP; mass record fetch by single principal | S1 |
| Evidence chain monitor | Hash anchor failure (continuous); inscription delay > SLA; verification mismatch | S2 (operational) — escalates to S0 if it indicates record tampering |
| WAF / Cloudflare | Credential-stuffing burst; SQL injection / XSS pattern hit rate spike | S2 / S1 |
| Sub-processor notification | GCP, Cloudflare, or other sub-processor security advisory affecting Canary's environment | Per advisory — assume S1 until proven otherwise |
| External report | Researcher / customer / vendor reporting suspected breach via `security@growdirect.io` | S1 minimum until triaged |
| Anomaly detection | Outbound data volume spike; geo-anomalous access; failed-login burst on admin accounts | S2 |
| Customer report | Merchant reports their data appearing in unauthorized location | S0 until ruled out |

[COUNSEL REVIEW] — Confirm `security@growdirect.io` is provisioned, monitored, and acknowledged within 24 hours per published security policy. If not, route to founder + on-call until provisioned.

---

## 2 · Severity classification

| Tier | Definition | Examples | Notification clock starts |
|---|---|---|---|
| **S0 — confirmed breach of Personal Data** | Confirmed unauthorized access to, exfiltration of, or alteration of Merchant Personal Data | Database extract observed in dark-web forum; service account key in attacker possession; merchant data in unauthorized third-party tool | At confirmation |
| **S1 — likely breach, scope undetermined** | High-confidence evidence of unauthorized access; scope not yet bounded | Compromised admin credential with active session; SQL injection result observed but extraction unconfirmed | At confirmation of compromise (clock runs while scope is determined — GDPR Art. 33's "awareness" trigger) |
| **S2 — security incident, no PII confirmed** | Security event with potential to escalate; PII access not yet evident | DDoS without observed data egress; SSRF attempt blocked; sub-processor advisory not yet known to affect us | Clock does not start until confirmed S1+ |
| **S3 — false positive / informational** | Reviewed and determined not to be a breach | Misconfigured monitor; researcher report of non-vulnerability | N/A |

**Awareness — what triggers the clock:** GDPR Art. 33 starts the 72-hour clock when the controller becomes "aware" of a breach. For Canary as processor, we are obligated to notify the controller (Merchant) "without undue delay" once we are aware. We treat S0 confirmation and S1 confirmation as awareness events. S2 events are tracked but do not start the clock.

[COUNSEL REVIEW] — Confirm the S1 "awareness while scope undetermined" interpretation. Some counsel argue that awareness requires confirmation of breach, not confirmation of compromise. EU regulators have leaned toward earlier-clock interpretations. Default to the conservative reading.

---

## 3 · The first 4 hours — containment

| Hour | Action | Owner | Output |
|---|---|---|---|
| 0:00 | Triage call: classify severity (§2) | On-call eng + founder | Tier assignment recorded in incident log |
| 0:15 | Open incident in `Brain/wiki/cards/incident-<date>-<id>.md` (per kepano `incident` template) | On-call eng | Incident card with timestamp, signal, initial scope |
| 0:30 | Containment actions for S0/S1: revoke compromised credentials; rotate KMS keys if implicated; isolate affected workloads; disable affected service accounts | On-call eng + founder | Action log entries with timestamps |
| 0:45 | Notify outside counsel (S0/S1) | Founder | Confirmation of counsel engagement |
| 1:00 | Forensic preservation: snapshot affected Cloud SQL instances; export Cloud Audit Logs covering the relevant window; capture container images of affected services. Record hashes and anchor to evidence chain | On-call eng | Snapshot IDs, log export paths, anchor TXIDs |
| 2:00 | Initial scope assessment: which Merchants affected? Which data categories? What is the count? | On-call eng + founder | Scope draft attached to incident card |
| 3:00 | Stakeholder pre-notification list drafted | Founder + counsel | Draft list — Merchants, regulators (jurisdictionally), insurance carrier, board if material |
| 4:00 | First written status update to internal stakeholders | Founder | Internal email + Linear comment on incident issue |

---

## 4 · Notification timelines

The clock starts at the awareness event in §2. Canary's obligation as **processor** is to notify the **Merchant (controller)** without undue delay; the Merchant has the obligation to notify the supervisory authority. In practice we run both clocks in parallel and prepare the Merchant's notification draft.

| Audience | Timeline | Vehicle | Required content |
|---|---|---|---|
| **Merchant (controller)** | Without undue delay; target: within 24 hours of awareness for S0; within 48 hours for S1 with scope-still-developing | Email to order-form contact + portal notification + phone for S0 if applicable | Nature of breach, data categories, approximate number of data subjects, contact for questions, measures taken / proposed (GDPR Art. 33(3)) |
| **Outside counsel** | Within 1 hour for S0/S1 | Phone + email | Full incident state |
| **Insurance carrier (cyber-liability)** | Per policy — typically within 24-72 hours of awareness | Per carrier instructions | Per policy notification form |
| **GDPR supervisory authority** (when Merchant requires Canary to notify on their behalf) | Within 72 hours of Merchant's awareness | Per supervisory authority's portal | GDPR Art. 33(3) elements |
| **US state regulators / AGs** | State-by-state — see §4.1 | Per state | Per state law |
| **Affected Data Subjects** | When required by law and Merchant elects to use Canary's notification template | Email / postal per Merchant election and applicable law | "What happened, what was affected, what we're doing, what you should do" |
| **Public / press** | Only when required by law (e.g., > 500 affected residents trigger CA AG public posting) or when Merchant elects | Per Merchant communications plan | Coordinated with counsel |

[COUNSEL REVIEW] — Confirm the 24-hour Merchant-notification target is commercially defensible. Some processors commit to "within 48 hours" or even "within 72 hours." Tighter is better for trust posture but creates contractual exposure. Confirm cap.

### 4.1 · US state breach-notification windows (selected — full table maintained by counsel)

| State | Window | Statute |
|---|---|---|
| California | Without unreasonable delay; AG notification if > 500 CA residents affected | Cal. Civ. Code §1798.82; CCPA §1798.150 (private right of action) |
| New York | Within "the most expedient time possible" | Gen. Bus. Law §899-aa |
| Texas | Within 60 days; AG notification if > 250 TX residents | Bus. & Com. Code §521.053 |
| Florida | Within 30 days | Fla. Stat. §501.171 |
| Vermont | Within 14 days (preliminary); within 45 days (consumer) | 9 V.S.A. §2435 |
| Illinois | Within "the most expedient time possible" | 815 ILCS 530 |
| Massachusetts | Within "as soon as practicable" | M.G.L. c. 93H |
| Washington | Within 30 days | RCW 19.255 |

[COUNSEL REVIEW] — Maintain a current state-by-state matrix as appendix. Many states updated breach laws in 2024-2025; the table above is illustrative, not authoritative. Counsel must verify each window before notification activity.

---

## 5 · Forensic preservation

Forensic evidence preservation must happen **before** containment actions destroy evidence. The runbook order in §3 sequences this — hour 0:30 containment uses approaches (revoke credentials, rotate keys) that do not destroy logs or snapshots. Hour 1:00 captures the durable evidence.

| Evidence type | Preservation method | Retention | Anchor? |
|---|---|---|---|
| Cloud SQL instance state | Point-in-time backup (Cloud SQL automated) + manual export to Cloud Storage in immutable bucket | 7 years | Hash of export anchored to evidence chain |
| Cloud Audit Logs | Export to Cloud Storage immutable bucket covering ±48h around incident window | 7 years | Hash anchored |
| Application audit log | Already anchored to evidence chain at creation per DPA §7.3 | Permanent (chain) + 7 years (operational copy) | Continuous |
| Container images | Pull current image of all affected services to immutable Artifact Registry tag | 7 years | Hash anchored |
| Network flow logs (VPC) | Export covering ±48h | 7 years | Hash anchored |
| External reports (researcher emails, customer reports) | Archive in incident card with timestamps | 7 years | Hash anchored |

**Why anchor forensic evidence to the chain:** Application 63/991,596's evidence-chain claim allows Canary to prove forensic captures were not modified after collection. Any subsequent challenge to the integrity of the forensic record fails an independent verification check. This is the single largest force multiplier in the breach response — counsel and regulators take less time to validate the chain of custody when it is cryptographically continuous.

[COUNSEL REVIEW] — 7-year retention is conservative but standard for litigation hold. Some counsel recommend longer for GDPR-relevant breaches. Confirm cap.

---

## 6 · Stakeholder communications templates

Templates are starting drafts. Final wording is the founder's and counsel's call per incident.

### 6.1 · Merchant notification (S0/S1) — email

```
Subject: [Action Required] Canary Protocol — Security Incident Notification

[Merchant contact name],

We are writing to notify you of a security incident at Canary Protocol that may have affected your data. We are sending this notification under GDPR Article 33 (where applicable) and under our DPA §[reference].

What happened:
[1-2 sentences — factual, no speculation]

When we became aware:
[Timestamp UTC]

What data may have been affected:
[Data categories from DPA §3]

Approximate number of data subjects affected (if known):
[Number, or "we are still determining the scope and will provide an updated count within 48 hours"]

What we have done:
[Containment actions taken]

What you should do:
[Specific actions — e.g., review accounts, rotate credentials, prepare your own Article 34 notifications if you are the controller]

Who to contact:
For questions, contact [name, role] at security@growdirect.io or [phone].
For escalation, contact [counsel name] at [counsel email].

We will provide our next written update within [24 / 48 / 72 hours] or sooner if material new information emerges.

Sincerely,
[Founder / authorized signatory]
GrowDirect LLC dba Canary Protocol
```

### 6.2 · Regulator notification (GDPR Art. 33) — narrative skeleton

```
1. Nature of the personal data breach
   - Category of breach (confidentiality / integrity / availability)
   - Cause (where known)
   - Vector

2. Categories and approximate number of data subjects concerned
3. Categories and approximate number of personal data records concerned
4. Likely consequences of the personal data breach
5. Measures taken or proposed
   - Containment actions completed
   - Forensic actions completed
   - Mitigation actions for affected data subjects (where applicable)
6. Name and contact details of the data protection officer or other contact point
```

### 6.3 · Internal status update — Slack / Linear comment

```
[INC-YYYY-MM-DD-NN] Status update [N] — [HH:MM UTC]

Severity: [S0/S1/S2]
Clock: [HH:MM elapsed since awareness]
Containment: [DONE / IN PROGRESS / NOT STARTED]
Scope: [N merchants, M data subjects, K records — or "still determining"]
Merchant notifications: [SENT / DRAFT / PENDING]
Counsel: [name] engaged at [HH:MM]
Insurance: [NOTIFIED at HH:MM / PENDING]
Regulator notifications: [LIST or NONE YET]

Next update by: [HH:MM]
```

### 6.4 · Counsel-engagement template

```
[Counsel name],

We are activating the breach response runbook. Initial assessment:
- Severity: [S0/S1]
- Time of awareness: [UTC]
- 72-hour clock expires: [UTC]
- Approximate scope: [N merchants / M data subjects / K records]
- Containment status: [done / in progress]

We need your guidance on:
1. Regulator notification scope (US states, GDPR supervisory authority)
2. Affected-data-subject notification requirement assessment
3. Insurance carrier notification draft review
4. Public communications posture

Incident card: [URL]
Forensic evidence anchored to evidence chain — anchor TXIDs in the card.

Let us know your availability for an immediate call.
```

---

## 7 · Post-incident

| Hour | Action | Owner | Output |
|---|---|---|---|
| Incident close | Final scope written; forensic captures verified against anchors | On-call eng + founder | Verified scope statement in incident card |
| +24h | Postmortem draft begun | Founder | Postmortem in `Brain/wiki/cards/postmortem-<date>-<id>.md` |
| +7 days | Postmortem published internally; Merchant-facing summary drafted | Founder + counsel | Internal postmortem; Merchant summary draft |
| +14 days | Merchant-facing postmortem distributed to affected merchants | Founder | Distribution log in incident card |
| +30 days | Remediation actions tracked to closure as Linear issues; controls update committed to runbook | Founder | Linear cycle of remediation issues; runbook diff |
| +90 days | Tabletop replay of the incident with the runbook's then-current version | Founder + on-call | Replay notes; runbook revision |

---

## 8 · Postmortem template (blameless)

```
# Postmortem — INC-YYYY-MM-DD-NN

## Summary
[1 paragraph — what happened, blast radius, resolution]

## Timeline
[UTC timestamps, key events]

## Detection
[How we found out; how long until detection; what would have caught it sooner]

## Response
[What we did, in order; what worked, what didn't]

## Scope
[Final confirmed scope — merchants, data subjects, records, data categories]

## Root cause
[Technical and process root causes — multiple where applicable]

## Contributing factors
[What made this possible / harder to detect / harder to contain]

## What went well
[Specific things — names, decisions, tools]

## What could have gone better
[Specific — no blame attached]

## Action items
[Linear issues with owners and due dates]

## Lessons for the runbook
[Specific runbook changes proposed]

## Evidence chain anchors
[TXIDs of forensic captures]
```

---

## 9 · Connection to PCI scope

If a Canary breach is suspected to have touched cardholder data — which would mean the data-flow boundary (DPA §7.4) was violated — escalate immediately:

1. Notify QSA (per GRO-695)
2. Notify affected payment processor(s) per their merchant notification requirements
3. Treat as S0 regardless of other classification
4. Coordinate with Merchant's PCI compliance officer

[COUNSEL REVIEW] — Confirm the architectural commitment that "Canary cannot have a cardholder-data breach" is a defensible position. The premise is that PAN/track/CVV does not enter Canary's environment. If post-mortem analysis ever finds a leak path, the architecture itself requires revision, not just the runbook.

---

## Counsel Review Required (consolidated)

1. **§1 detection** — confirm `security@growdirect.io` is provisioned and monitored
2. **§2 severity** — S1 awareness-clock interpretation
3. **§4 notification cap** — 24-hour Merchant target commercially defensible
4. **§4.1 state matrix** — must be maintained current by counsel; this version is illustrative
5. **§5 retention** — 7-year retention vs. longer for GDPR-relevant breaches
6. **§9 PCI architectural premise** — confirm "Canary cannot have a cardholder-data breach" is defensible

---

## Change log

| Version | Date | Changes |
|---|---|---|
| v0.1 | 2026-05-02 | Initial working runbook — GRO-693 |
