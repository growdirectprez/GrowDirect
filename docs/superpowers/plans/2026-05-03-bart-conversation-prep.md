---
title: Bart conversation prep — 12 DriftPOS-team OQs structured for 90-min Zoom
type: plan
status: ready-for-call
date: 2026-05-03
linear: GRO-762
parent: GRO-739
source: docs/sdds/go-handoff/driftpos-integration.md §10
last-compiled: 2026-05-03
needs-review: 2026-08-03
---

# Bart conversation prep — DriftPOS integration OQs

## Mission

Twelve open questions from the DriftPOS ↔ Canary integration contract spec ([driftpos-integration.md §10](../../sdds/go-handoff/driftpos-integration.md)) that require Bart's team's confirmation. None of them block contract publication; all should be resolved before pilot. This document organizes them for a 90-minute Zoom session — each OQ formatted as: question / why Canary needs the answer / Canary's recommendation if forced unilateral / Bart's expected position per founder context / decision space.

**Format note:** the OQ block is for Bart's review in the call; the "Canary recommendation" line is the position to defend if Bart doesn't have a strong preference. The "Bart's expected" line is the founder's read on what's realistic — used to gauge whether to push or accept.

---

## Pre-call checklist (founder)

Before the Zoom:

- [ ] **Confirm attendees**: Bart + DriftPOS engineering lead (the person who will write the .NET adapter); Canary side: founder + ALX (notes)
- [ ] **Send Bart in advance** (24h before):
  - [`docs/sdds/go-handoff/driftpos-integration.md`](../../sdds/go-handoff/driftpos-integration.md) §1-3 (Identity Rule, Wire Inventory, API Surface) — the contract baseline
  - This OQ doc — Bart can pre-read and arrive with positions
  - The 130-capability map ([GRO-721 / CAN-RES-001](https://linear.app/growdirect/issue/GRO-721)) — context for who-owns-what
- [ ] **Decide what's deferrable**: OQ-1 (mTLS vs JWT), OQ-4 (queue cap), OQ-7 (UI button) can be deferred to pilot-config-time without blocking the contract. OQ-2 (network token), OQ-3 (idempotency), OQ-5 (UUID assignment), OQ-11 (PCI scope) cannot — they're load-bearing for the wire spec
- [ ] **Pick a note-taking model**: live shared Google Doc vs Granola transcript vs both. Granola is the founder's default; the "agent in the call" pattern (per memory `feedback_no_call_prep_theater`) means ALX gets the transcript, not pre-written talking points
- [ ] **90-min agenda**: 5-min framing, 60 min (12 OQs × 5 min each), 15-min wrap (decisions, owners, follow-ups), 10-min buffer
- [ ] **Decide what gets committed in-meeting** vs follow-up. Any decision that triggers a schema change or SDD revision is a follow-up dispatch, not an in-meeting commit

---

## OQ-1 — mTLS vs JWT for register↔back-half

**Question:** Does DriftPOS support mTLS client certificates today, or is JWT-only fallback required for pilot?

**Why Canary needs the answer:** Determines whether the Canary credential-management UX needs to handle cert provisioning (ACME-style per-register issuance, rotation, revocation) at pilot kickoff. mTLS at GA is non-negotiable for the patent-architecture's Node 2 trust posture; JWT-only is acceptable for pilot if we have a clean upgrade path.

**Canary's recommendation if forced unilateral:** `mtls_or_jwt` mode for pilot (gateway accepts either; tenant-config flag elects which); tighten to `mtls`-required for GA.

**Bart's expected position per founder context:** likely JWT-only initially — DriftPOS's .NET stack speaks JWT natively; mTLS cert management is real engineering work Bart's team hasn't done before. Founder's read: he'll commit to mTLS by GA but want the JWT bridge for pilot.

**Decision space:**
- **If Bart says JWT-only for pilot:** accept; gateway's existing JWT handler is wired; track mTLS readiness as a separate DriftPOS milestone (Loop 3 backlog dispatch)
- **If Bart says mTLS-ready:** great — design the per-register cert provisioning flow as a Phase D backlog item (ACME-style)
- **If Bart says "what's mTLS?":** explain in 2 minutes; default to JWT-only; mTLS becomes a Q3 conversation

---

## OQ-2 — Ingenico pinpad network token availability

**Question:** Does DriftPOS's Ingenico pinpad return a stable network-tokenized fingerprint per card? Or does Canary need to fall back to `self_computed` (last4 + brand + zip5) for `payment_fingerprint.value`?

**Why Canary needs the answer:** Per [`party-identity-design.md`](../../sdds/go-handoff/party-identity-design.md) §B fingerprint quality matrix, network-token fingerprints land at quality 0.85+ and trigger Rule 1 (strong-match party resolution); self-computed fingerprints land at 0.4 (per OQ Resolution Pack §A.1 OQ-1.2 founder-approved 2026-05-03) and are clustering signal only. The party-resolution latency budget assumes Rule 1 hits in <50ms p99 — with self-computed fallback the rule fires less often, the 200ms p99 wire latency budget gets harder to meet, and the entire DriftPOS checkout stalls more visibly.

**Canary's recommendation if forced unilateral:** Self-computed fallback acceptable for v1 with `quality_score=0.4` (per OQ Resolution Pack §A.1 OQ-1.2). Plan for Ingenico network-token integration as v1.1.

**Bart's expected position per founder context:** Bart probably hasn't asked Ingenico whether they expose this. The pinpad's PCI scope owns the cardholder data; Ingenico does provide tokenization endpoints in their P2PE flow. Likely answer: "I'll ask my Ingenico contact." Founder's read: 2-week follow-up.

**Decision space:**
- **If Bart confirms YES:** quality goes to 0.85+; the fingerprint becomes a Rule 1 anchor; party resolution gets dramatically faster + more accurate
- **If Bart says NO or unknown:** ship v1 with self-computed; document the upgrade path; flag as a v1.1 dispatch

---

## OQ-3 — Idempotency-Key honor on retry

**Question:** Can DriftPOS respect the `Idempotency-Key` semantics (storing the key on first submission and resubmitting the same key on retry) for offline-replay?

**Why Canary needs the answer:** If DriftPOS generates a fresh key on each retry, duplicates will not be deduped at Sub2's `(tenant_id, location_id, business_date, transaction_number)` UPSERT key — the merchant's transaction count inflates, every dashboard count breaks, and Fox starts seeing phantom void-pattern detections.

**Canary's recommendation if forced unilateral:** Yes — **required for safety**. This is non-negotiable for the wire contract.

**Bart's expected position per founder context:** Bart will want to say yes; the .NET HttpClient idempotency pattern is well-established. The risk is that his offline-queue replay flow regenerates the key from `register_number + transaction_number` on every reattempt instead of persisting the original — which is wrong but easy to do.

**Decision space:**
- **If Bart says YES + persists original key:** done; document the replay protocol in §4 of the SDD
- **If Bart says YES but key is regenerated:** push back hard; this is a correctness bug not a design choice; offer to write the spec text Bart's team needs to implement
- **If Bart says NO:** the contract is broken; Canary cannot accept duplicate-prone replay; make this a pilot-blocker

---

## OQ-4 — DriftPOS offline-queue capacity

**Question:** What's DriftPOS's offline outage queue capacity? (How many transactions can a register queue before it must refuse new sales?)

**Why Canary needs the answer:** Determines whether `replay-batch` max size of 1000 is appropriate, or needs to be 10K+. Pilot merchants in regions with unreliable connectivity (rural specialty retail, ranch supply, garden centers off the suburban grid) routinely run hours-to-days offline. A 1000-transaction cap that translates to ~3 hours at peak is too small for those use cases.

**Canary's recommendation if forced unilateral:** Configure for 10K transaction queue; size the replay-batch endpoint to handle 10K rows + 4-hour worst-case backlog window.

**Bart's expected position per founder context:** Unknown — flag for Bart to bring data. DriftPOS likely uses SQLite for the offline queue; the cap is whatever they sized the local disk for. Probably between 5K and 50K based on industry norms.

**Decision space:**
- **If Bart says < 5K:** push for higher; 5K is too small for pilot's expected use cases
- **If Bart says 10K-50K:** good; replay-batch endpoint sized accordingly
- **If Bart says >50K:** great; no Canary-side change needed

---

## OQ-5 — Per-register UUID assignment authority

**Question:** Does DriftPOS maintain per-register UUID assignment server-side, or does each register self-assign?

**Why Canary needs the answer:** Self-assigned UUIDs create idempotency-namespace collision risk if a register is re-imaged (loses local UUID, generates new one, replays old transactions under new identity → looks like a new register's first sale, not a replay).

**Canary's recommendation if forced unilateral:** Server-side via Canary registration endpoint. Register asks Canary at boot for its UUID (auth'd by per-merchant API key); Canary assigns and tracks.

**Bart's expected position per founder context:** DriftPOS likely uses register-side GUIDs today (each register self-assigns at install). Founder's read: Bart will resist a server-side flip because it changes the install flow. Need to make the case that the flip is small.

**Decision space:**
- **If Bart agrees to server-side:** great; specify the registration endpoint in §3 of the SDD
- **If Bart wants register-side:** acceptable IF combined with strong re-image detection (registers must persist UUID through re-image, OR if re-imaged, register attempts to reclaim its prior UUID via a Canary lookup-by-prior-IP/MAC). Document the constraint
- **If Bart says "we already do client GUIDs":** dig into the re-image protocol; either way ship the spec text

---

## OQ-6 — Receipt-numbering reconciliation on offline reconnect

**Question:** Does DriftPOS print receipts during offline operation? If so, how does it reconcile receipt-numbering with Canary on reconnect?

**Why Canary needs the answer:** Receipt number uniqueness is enforced on `(tenant_id, location_id, business_date, transaction_number)` — register must guarantee no collision. If DriftPOS prints receipts offline using local register-day numbering, and Canary's authoritative numbering is server-side, the two diverge during outages. Reconciliation strategy must be specified or the merchant ends up with two receipts numbered "0001" for the same business day.

**Canary's recommendation if forced unilateral:** Local register-day numbering during offline; reconciled on replay via the (location_id, business_date, register_id, register_local_seq) compound key. Server-authoritative numbering only for transactions originating online.

**Bart's expected position per founder context:** DriftPOS almost certainly prints offline (offline checkout is the pilot's whole point). Bart's reconciliation answer is the live question.

**Decision space:**
- **If Bart has a plan:** validate it covers business-day rollover during outage (a register that's offline across midnight needs to know which date to assign)
- **If Bart doesn't have a plan:** offer Canary's recommendation; commit Bart's team to implementing it
- **If Bart says "we don't print offline":** unlikely given pilot use case, but if so, simplify the spec — server-authoritative numbering becomes the only mode

---

## OQ-7 — Cashier UI "mark as LP-relevant" button

**Question:** What's DriftPOS's stance on the `evidence_trigger` capability? Does the cashier UI surface a "mark as LP-relevant" button?

**Why Canary needs the answer:** The wire supports it (an `evidence_trigger` field on the transaction event signals Sub 1 to create a `q.case_evidence` row immediately, even without a detection). The UX decision — whether the cashier sees a button to flag a suspicious transaction — is Bart's.

**Canary's recommendation if forced unilateral:** Optional — surface only if merchant configures it. Per-merchant feature flag in `app.merchant_settings.cashier_lp_button_enabled` (default false; loss-prevention-conscious merchants opt in).

**Bart's expected position per founder context:** Bart probably hasn't thought about this. It's a small UX surface; he'll say "we can add a button." Founder's read: defer to pilot — see if any merchant actually wants it before building.

**Decision space:**
- **If Bart says YES we'll add it:** great; specify the button's wire payload (`{"evidence_trigger": true, "trigger_reason": "manual"}`) in §3
- **If Bart says NO:** acceptable; the wire still supports it for any other front-end (mobile-rep app, manager dashboard) that wants to send it
- **If "later":** acceptable; document as a v1.1 capability

---

## OQ-8 — Push vs poll change-feed cadence

**Question:** Will DriftPOS implement the change-feed pull cadence (`/changes?since=`) or rely solely on push notifications?

**Why Canary needs the answer:** Push notifications can be lost (network blip, gateway redelivery failure, register-side crash mid-receive). 30s pull catches gaps. Without the pull backstop, register caches drift from canonical truth silently.

**Canary's recommendation if forced unilateral:** Both — push + 30s pull as backstop. The combined model is what every modern SaaS does; documented in §4 Eventing Pattern of the SDD.

**Bart's expected position per founder context:** Bart will want to say "push only" because it's simpler. Push back: industry-standard architectures use both for the reason above.

**Decision space:**
- **If Bart agrees to both:** confirm the pull endpoint shape (`GET /v1/changes?since={iso8601}` returns delta events)
- **If Bart says "push only":** document the risk; track silent-cache-drift as an operational risk in the pilot success criteria
- **If Bart says "what's a change-feed?":** explain in 3 min; default to "both"

---

## OQ-9 — EBT acceptance certification path

**Question:** EBT acceptance — does DriftPOS handle USDA SNAP eligibility logic locally, or does Canary need to expose a real-time eligibility check endpoint?

**Why Canary needs the answer:** Per [GRO-721 capability map row #84](https://linear.app/growdirect/issue/GRO-721), EBT eligibility is a register-side responsibility (the cashier needs an immediate yes/no at scan time; round-tripping to Canary adds 200ms latency at every scan). But the rule logic varies by USDA's SNAP-eligible items list which DriftPOS would need to maintain.

**Canary's recommendation if forced unilateral:** DriftPOS handles locally per their processor's certified flow (Ingenico will have an EBT-certified cert path). Canary stores the SNAP eligibility flag on `m.items.is_food_stamp_eligible` (column already exists per canonical schema) and pushes it to DriftPOS via the master-data sync.

**Bart's expected position per founder context:** EBT is hard. Bart's team probably hasn't certified for EBT yet. If pilot merchants need EBT (likely — feed/garden/specialty retail often serves SNAP customers), Bart needs an EBT-certified payment processor in the integration.

**Decision space:**
- **If Bart says we handle EBT:** confirm the cert path; document the Canary-side eligibility flag flow
- **If Bart says we don't yet:** flag as a pilot constraint — pilot merchants can't accept SNAP through DriftPOS
- **If Bart asks Canary to expose a real-time check:** push back — that's not the right architecture; offer to spec the master-data flow instead

---

## OQ-10 — Three-level void semantics

**Question:** Does DriftPOS track three-level void semantics (transaction, line, sub-line) like Toast, or simpler register-level void only?

**Why Canary needs the answer:** Toast's three-level model is restaurant-specific (split a check, void one entree from one diner). SMB retail rarely uses sub-line voids — they void transactions or void lines. Spec needs to match what DriftPOS actually emits or the void wire format becomes a translation layer.

**Canary's recommendation if forced unilateral:** Simpler — register-level + line-level. Sub-line voids reserved for future restaurant-vertical adapters.

**Bart's expected position per founder context:** DriftPOS is built for retail not restaurants; Bart will say "transaction + line." Likely a quick yes-no.

**Decision space:**
- **If Bart says transaction + line:** done; spec stays as-is
- **If Bart says all three levels:** unlikely but accommodatable; specify the sub-line void wire shape
- **If Bart asks "what's a sub-line void?":** explain in 1 min; default to transaction + line

---

## OQ-11 — DriftPOS PCI scope certification

**Question:** What's DriftPOS's PCI scope as a cardholder-data-handling app — is it certified at the level required for an SMB merchant's PCI-DSS attestation?

**Why Canary needs the answer:** Bart's team must complete this independently; Canary's PCI posture (out of scope until phase 4 per [`docs/sdds/canary-go/gcp-deployment-gateway.md`](../../sdds/canary-go/gcp-deployment-gateway.md)) is **conditional on DriftPOS owning the cardholder-data interaction**. If DriftPOS isn't PCI-DSS-attested at the right level, Canary inherits cardholder-data-handling responsibility — which would force phase 4 PCI scope to land in pilot, not in 2027.

**Canary's recommendation if forced unilateral:** Required — PCI-DSS Level 2 SAQ-D minimum for the pilot. No way around it.

**Bart's expected position per founder context:** Critical question. Bart needs to either show his current PCI attestation or commit to getting one. If his current stack is PCI-out-of-scope (e.g., card data goes pinpad → processor → register's reference token only), great; if his register handles raw PAN, that's a problem.

**Decision space:**
- **If Bart shows attestation:** verify the cert level (SAQ-A, SAQ-A-EP, SAQ-B-IP, SAQ-C, SAQ-D — the higher letters mean more scope); SAQ-D is fine, anything less needs scope review
- **If Bart says "we're PCI-out-of-scope via P2PE":** ideal; verify the P2PE cert is valid
- **If Bart says "we don't have one":** pilot-blocker; either Canary takes on PCI scope (changes the entire phase 4 timeline) or Bart's team gets attested before pilot

---

## OQ-12 — Conformance test suite in DriftPOS CI

**Question:** Will DriftPOS support the conformance test suite as part of its CI?

**Why Canary needs the answer:** Without Bart-side CI on conformance, regressions may go undetected until they hit a merchant. Canary's substrate proves correctness from its side; Bart's adapter is the OTHER side of the wire. Both must hold the contract for the integration to work.

**Canary's recommendation if forced unilateral:** Strongly recommended. Canary publishes the conformance suite (a docker-compose harness that simulates every wire interaction); Bart's team runs it on every PR.

**Bart's expected position per founder context:** Bart's a serious engineer; he'll say yes to CI conformance. The work is wiring it up to his .NET test runner. Reasonable lift.

**Decision space:**
- **If Bart agrees:** great; commit a Canary-side dispatch to publish the conformance suite + provide a sample DriftPOS-side runner config
- **If Bart says no CI but yes manual:** acceptable for pilot; flag as a tech-debt item for GA
- **If Bart says no period:** push back; this is the wire-correctness gate. If he can't do CI, find another way (Canary runs the conformance suite against his sandbox nightly)

---

## §Wrap — items to capture from the call

For each OQ:
- [ ] Decision (Canary's recommendation accepted? Modified? Different?)
- [ ] Owner (DriftPOS-side action vs Canary-side action vs joint follow-up)
- [ ] Timeline (pilot-blocker vs v1.1 vs deferred)
- [ ] Follow-up dispatch needed? (file in Linear during the call if obvious)

For the integration as a whole:
- [ ] Pilot date target (informs whether OQ-11 PCI-scope is a Q3 sprint or a Q4 program)
- [ ] First merchant target (RapidPOS-affiliated? new? — affects which capability subset matters)
- [ ] CI conformance: who hosts the harness, how is access provisioned, what's the cadence

---

## Cross-references

- [`docs/sdds/go-handoff/driftpos-integration.md`](../../sdds/go-handoff/driftpos-integration.md) §10 — original OQs (verbatim)
- [`docs/superpowers/plans/2026-05-03-oq-resolution-pack.md`](2026-05-03-oq-resolution-pack.md) — companion doc with the 22 founder-decided OQs (this doc covers the 12 deferred to Bart)
- [`Brain/wiki/canary/partnership-research/rapidpos-subbrand-feature-map.md`](../../../Brain/wiki/canary/partnership-research/rapidpos-subbrand-feature-map.md) — DriftPOS / RapidPOS context
- [GRO-759](https://linear.app/growdirect/issue/GRO-759) — DriftPOS integration contract spec (parent of these OQs)
- [GRO-721](https://linear.app/growdirect/issue/GRO-721) — Capability map (130 capabilities split DriftPOS / Canary / Both)
- Memory `feedback_no_call_prep_theater` — pre-load context + live Granola monitor + post-call ingest, NOT pre-written scripts
- Memory `project_bart_var_partnership` — the broader VAR / whitelabel context behind why this conversation matters
