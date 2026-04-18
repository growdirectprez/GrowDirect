---
type: spec
domain: canary
status: active
created: 2026-03-19
updated: 2026-03-19
---
# PRD — Device Attestation v1.0

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]

**Version:** 1.0
**Date:** March 2, 2026
**Author:** ALX (Chief of Staff)
**Classification:** MAXIMUM CONFIDENTIAL
**Protocol Reference:** `elJeffe_Protocol_Spec_v1.0.md` (Section 5)
**Schema Reference:** `CRDM_v1.1_Alignment_Amendment` (Amendment B)
**Pipeline Reference:** `Inscription_Pipeline_Design_Spec_v1.0.md` (Sections 3.3, 3.4)
**Source Issues:** GRO-45 (Amendment 8: Device Graph), GRO-47 (Inscription Pipeline)
**Gate:** Tom (Merkle tree design), Jim (QA — feature flag permutations), Syd (liability review)

---

## 1. Problem Statement

Canary LP seals commercial events into Bitcoin inscriptions, but the inscription is currently device-blind. It records *what* happened (event hash, timestamp, Merkle root) but not *which hardware processed the transaction*. For loss prevention — the core product — device context is critical. Ghost devices, unauthorized terminal swaps, and rogue peripherals are primary indicators of internal theft and collusion. Without device attestation on the inscription, the permanent on-chain record tells you a transaction happened but cannot tell you whether the device ecosystem was trustworthy when it happened.

This matters to three audiences. For Canary LP merchants, device anomalies are the highest-signal LP alerts (Chirp rules C-901 through C-909). For RaaS consumers — insurers, auditors, franchise compliance teams — device integrity is a trust signal that upgrades a "verified receipt" to a "verified receipt from a trusted device environment." For GrowDirect, device attestation is a premium feature that differentiates standard and enterprise tiers.

Jeffe's directive: *"We should be able to enforce device integrity or not."* Device attestation must be configurable per merchant — ON or OFF — with zero cost penalty for merchants who don't need it.

---

## 2. Goals

### User Goals
- **G-1:** Merchants with device tracking enabled get permanent, on-chain proof that their device environment was intact at the time of each batch inscription.
- **G-2:** RaaS consumers can distinguish between device-attested and non-attested verifications in a single API call.
- **G-3:** Chirp anomaly flags (ghost devices, unauthorized swaps, unknown peripherals) are permanently recorded on Bitcoin when detected — creating an immutable anomaly record for compliance and insurance.
- **G-4:** Merchants without device tracking pay nothing extra and see no difference in their inscription flow.

### Business Goals
- **G-5:** Device attestation is the gate between standard and enterprise tier — it justifies the pricing step-up.
- **G-6:** Insurers and auditors require `device_integrity: true` + zero flags for clean verification. This creates pull demand for merchants to upgrade.
- **G-7:** Anomaly flags on Bitcoin create a permanent, tamper-proof compliance record that GrowDirect competitors cannot replicate without their own inscription infrastructure.

---

## 3. Non-Goals

- **NG-1:** Real-time device monitoring or alerting. Device attestation is a batch-level seal, not a live feed. Real-time alerts remain in the Chirp subsystem.
- **NG-2:** Device provisioning or management. This PRD covers the attestation (proof that devices were known and healthy), not the onboarding of new devices.
- **NG-3:** Device identity on Avalanche L2. Device attestation lives on Bitcoin L1 inscriptions only. L2 has no role in device state.
- **NG-4:** Per-transaction device proof. Attestation is per-batch, matching the Merkle batch boundary. Individual transaction → device mapping is in the CRDM (`transaction_devices` table), not on-chain.
- **NG-5:** Third-party device certification. We attest device presence and integrity within our graph. We do not validate manufacturer certificates or firmware versions.

---

## 4. User Stories

### Merchant (Canary LP Pro / Enterprise)
- **US-1:** As a multi-location retailer, I want each batch inscription to include proof of which devices processed transactions so that if a ghost device appears in my network, the anomaly is permanently recorded and cannot be hidden.
- **US-2:** As a merchant upgrading from standard to pro tier, I want to enable device attestation without migrating data or re-inscribing past batches so that I can start attesting from today forward.
- **US-3:** As a merchant, I want to disable device attestation if I'm a small single-terminal shop where device tracking adds no value, so that my inscriptions stay small and cheap.

### RaaS Consumer (Insurer / Auditor)
- **US-4:** As an insurance claims analyst, I want to see whether a verified receipt came from a device-attested environment so that I can differentiate high-confidence verifications (attested, zero flags) from basic verifications (unattested).
- **US-5:** As a franchise compliance officer, I want to query which batches had device anomaly flags so that I can investigate locations where unauthorized hardware appeared.
- **US-6:** As an auditor, I want to independently verify the device Merkle root against the on-chain inscription so that I don't have to trust GrowDirect's API — the math proves it.

### Platform Operator (GrowDirect)
- **US-7:** As the platform operator, I want device attestation to be a feature flag per merchant namespace so that I can turn it on for enterprise pilots without affecting the rest of the fleet.
- **US-8:** As the platform operator, I want the inscription payload to stay under 500 bytes even with full device attestation + flags so that inscription costs remain predictable.

---

## 5. Requirements

### Must-Have (P0)

**R-1: Feature Flag — Per-Merchant Configuration**

Device attestation is controlled by a feature flag in the `merchant_feature_flags` table (or equivalent configuration store), keyed to the merchant's namespace.

*Acceptance Criteria:*
- [ ] Flag key: `device_attestation`, values: `on` / `off`
- [ ] Default for new merchants: `off`
- [ ] Flag change takes effect on the next batch (does not retroactively modify past inscriptions)
- [ ] Admin endpoint: `PUT /admin/merchants/{id}/features` to toggle the flag
- [ ] Flag state is cached in Sub 3's batch builder for the duration of a batch cycle

**R-2: Device Merkle Tree Construction**

When `device_attestation = on`, Sub 3 builds a parallel Merkle tree over the `transaction_devices` rows linked to events in the current batch.

*Acceptance Criteria:*
- [ ] Leaf hash: `sha256(device_id || device_type || transaction_id || timestamp)` — byte concatenation, UTF-8 encoded, no separator
- [ ] Tree construction: binary Merkle tree, same algorithm as event tree (duplicate last leaf to fill power-of-2)
- [ ] Output: `device_root` (root hash), `device_count` (unique devices in batch)
- [ ] Device tree shares the same batch boundary as the event tree (same events, same time range)
- [ ] If a batch contains events with no linked devices (e.g., manual entries), those events contribute zero device leaves — the device tree only contains actual device records

**R-3: Chirp Flag Collection**

When `device_attestation = on`, Sub 3 queries the `chirp_alerts` table for device-related Chirp rules triggered by events in the current batch.

*Acceptance Criteria:*
- [ ] Query scope: Chirp rules C-901 through C-909 (device anomaly rules only)
- [ ] Output: deduplicated array of rule codes (e.g., `["C-901", "C-904"]`)
- [ ] If no device Chirp rules fired: `flags: []` (empty array, not null)
- [ ] Flag collection completes before inscription payload assembly — flags are part of the payload

**R-4: Inscription Payload — Attestation Block**

The `attestation` block is included in the `merkle_batch` inscription payload when `device_attestation = on`. Omitted entirely when `off`.

*Acceptance Criteria:*
- [ ] When ON:
  ```json
  "attestation": {
    "device_integrity": true,
    "device_count": 3,
    "device_root": "<sha256 hash>",
    "flags": ["C-901"]
  }
  ```
- [ ] When OFF: `"attestation"` key is absent from the JSON (not `null`, not `{}` — absent)
- [ ] `device_integrity` is `true` if zero flags, `false` if any flags present
- [ ] Payload size: ≤ 450 bytes with attestation + flags, ≤ 300 bytes without attestation

**R-5: Post-Inscription Storage — Device Fields**

The `merkle_batches` table stores device attestation data for operational queries.

*Acceptance Criteria:*
- [ ] Columns: `device_attestation_enabled` (boolean), `device_root` (text, nullable), `device_count` (integer, nullable), `device_flags` (text[], nullable)
- [ ] When OFF: `device_attestation_enabled = false`, device columns are NULL
- [ ] When ON: all device columns populated from tree construction output
- [ ] Indexed: `device_attestation_enabled` for filtering attested vs. unattested batches

**R-6: RaaS Verification Response — Device Attestation**

The `/v1/verify` endpoint includes device attestation data when available and requested.

*Acceptance Criteria:*
- [ ] Request parameter: `include_device: true` (optional, default false)
- [ ] When device data exists and requested:
  ```json
  "device_attestation": {
    "integrity": true,
    "device_count": 3,
    "flags": [],
    "device_proof_available": true
  }
  ```
- [ ] When device data does not exist: `"device_attestation": null`
- [ ] When not requested: `device_attestation` key omitted from response
- [ ] Device proof endpoint (P1) returns the full Merkle path for independent verification

### Nice-to-Have (P1)

**R-7: Device Merkle Proof Endpoint**

A dedicated endpoint for auditors and sophisticated RaaS consumers to retrieve the full device Merkle proof for independent verification.

*Acceptance Criteria:*
- [ ] Endpoint: `GET /v1/verify/{event_hash}/device-proof`
- [ ] Returns: device leaf hash, sibling hashes, path to device_root
- [ ] L402 gated (same 1 sat/call as primary verification)
- [ ] Returns 404 if the batch was not device-attested

**R-8: Device Attestation Dashboard Widget**

Canary LP dashboard displays device attestation status per batch for merchants with the feature enabled.

*Acceptance Criteria:*
- [ ] Shows: batch ID, device count, integrity status, flag count
- [ ] Flags link to the corresponding Chirp alert detail
- [ ] Visual indicator: green (integrity, no flags), yellow (integrity, with flags), gray (not attested)

**R-9: Batch-Level Device Report**

Downloadable report for compliance teams showing device attestation history across batches.

*Acceptance Criteria:*
- [ ] Filter by: date range, integrity status, flag presence
- [ ] Export: CSV and PDF
- [ ] Includes: batch_id, inscription_id, device_count, device_root, flags, block_height

**R-10: Device Attestation Toggle in Merchant Settings**

Merchants (enterprise tier) can toggle device attestation on/off from their dashboard.

*Acceptance Criteria:*
- [ ] Toggle only available for merchants on pro/enterprise tier
- [ ] Warning when disabling: "Future batches will not include device attestation. Past inscriptions are not affected."
- [ ] Audit log entry when toggled

### Future Considerations (P2)

**R-11: Per-Device Verification**

Verify a specific device's participation in a specific batch, with Merkle proof returning the device-level leaf.

**R-12: Device Health Score**

Aggregate device attestation data across batches to compute a rolling device health score per merchant. Clean batches (integrity=true, zero flags) contribute positive signal. Flagged batches degrade the score.

**R-13: Cross-Batch Device Anomaly Detection**

Detect patterns across batches — e.g., a device that appears in one location's batch then another location's batch within an impossible timeframe (device teleportation). This extends Chirp from single-event to cross-batch analysis.

**R-14: L1-Only Device Verification**

Enable third-party verifiers to reconstruct the device Merkle tree from on-chain data alone, without GrowDirect's API. Requires the verifier to have the device record list for the batch (same pattern as L1-only event verification).

---

## 6. Success Metrics

### Leading Indicators (Week 1–4 post-launch)

| Metric | Target | Measurement |
|--------|--------|-------------|
| Enterprise merchants enabling device attestation | 80% of enterprise tier within 30 days | Feature flag activation rate |
| Device tree construction success rate | 99.9% | Sub 3 error logs — device tree failures / total attested batches |
| Inscription payload size (attested) | ≤ 450 bytes average | Payload size monitoring |
| RaaS calls with `include_device: true` | 15% of total verify calls within 30 days | API analytics |
| Chirp flag capture rate | 100% of device Chirp alerts in batch window captured | Cross-reference chirp_alerts vs. inscription flags |

### Lagging Indicators (Month 2–6)

| Metric | Target | Measurement |
|--------|--------|-------------|
| Enterprise tier upgrade rate | 20% increase in standard → enterprise upgrades citing device attestation | CRM attribution |
| Insurance partner verification calls | 50% of insurer RaaS calls include device flag | API analytics by consumer segment |
| Compliance audit pass rate | 100% of device-attested merchants pass audit with zero manual device review | Partner feedback |
| Anomaly detection rate | Device attestation flags identify 30% more device anomalies vs. Chirp-only alerts | Comparative analysis |

---

## 7. Technical Architecture

### Parallel Merkle Tree Design

```
Event Merkle Tree:                    Device Merkle Tree:
    merkle_root                           device_root
      /     \                               /     \
   h(e1+e2)  h(e3+e4)                 h(d1+d2)  h(d3+d4)
   /    \      /    \                  /    \      /    \
 h(e1) h(e2) h(e3) h(e4)          h(d1) h(d2) h(d3) h(d4)

Where:
  e(n) = sha256(event_id || event_hash || timestamp)
  d(n) = sha256(device_id || device_type || transaction_id || timestamp)
```

Both trees share the same batch boundary. Verification can check either root independently. The event tree proves *what happened*. The device tree proves *what hardware was involved*.

### Chirp Rule Codes (Device Anomaly)

| Code | Rule | Description |
|------|------|-------------|
| C-901 | Ghost Device | Device ID in transaction not registered in `devices` table |
| C-902 | Stale Device | Device not seen in > 30 days, suddenly active |
| C-903 | Device Velocity | Same device processes transactions at two locations within impossible timeframe |
| C-904 | Device Swap | Terminal serial number changed mid-shift |
| C-905 | Unauthorized Pairing | Peripheral paired to terminal without admin authorization |
| C-906 | Device Offline Gap | Device was offline during transaction window (clock drift or tampering) |
| C-907 | Firmware Mismatch | Reported firmware version doesn't match expected for device model |
| C-908 | Root Detection | Customer device shows root/jailbreak indicators |
| C-909 | Duplicate Device | Same device ID appears in multiple merchant namespaces |

### Inscription Cost Impact

| Config | Payload Size | Cost (~10 sat/vbyte) |
|--------|-------------|---------------------|
| Device OFF | ~300 bytes | $0.50–$2.00 |
| Device ON, no flags | ~400 bytes | $0.75–$2.50 |
| Device ON, with flags | ~450 bytes | $0.85–$3.00 |

Cost delta is trivial. The feature flag is a product decision, not a cost decision.

---

## 8. Open Questions

| # | Question | Owner | Blocking? |
|---|----------|-------|-----------|
| Q-1 | If a merchant enables device attestation mid-stream, do we backfill device data for events already in the batch buffer? Or does attestation start from the next clean batch? | Tom | Yes — affects batch builder logic |
| Q-2 | Should `device_integrity` be a boolean or a score? Boolean is simpler but loses nuance (e.g., 1 flag out of 100 devices vs. 50 flags). | Tom + Jim | No — boolean for v1, score for P2 |
| Q-3 | If the Chirp subsystem is down when a batch fires, do we inscribe without flags (potentially missing anomalies) or hold the batch? | Tom | Yes — affects error handling |
| Q-4 | Does Syd see liability exposure if a merchant has device attestation OFF and an incident occurs that device tracking would have caught? "You could have known" argument. | Syd | No — but needs answer before enterprise rollout |
| Q-5 | Should the device Merkle tree include customer devices (phones used for payment) or only merchant-owned hardware? | Jeffe | Yes — affects leaf computation and privacy |
| Q-6 | Is the `flags` array in the inscription payload exhaustive (every flag code) or just present/absent (at least one flag fired)? | Tom | No — current spec includes specific codes |

---

## 9. Timeline Considerations

| Phase | Dependency | Notes |
|-------|-----------|-------|
| Phase 0 (PoC) | Event Merkle tree working on testnet | Device attestation OFF for Phase 0 — validate event tree first |
| Phase 1 (Sandbox) | CRDM `devices` + `transaction_devices` tables populated | Cannot build device tree without device data flowing |
| Phase 2 (Device Attestation) | Phase 1 complete + enterprise pilot merchants identified | First attested inscription on testnet |
| Phase 3 (Production) | Jim QA sign-off on all feature flag permutations | Mainnet device attestation |

**Hard dependency:** Device attestation requires the `devices` and `transaction_devices` tables from GRO-45 Amendment 8 to be populated with real data from at least one POS integration. Without device data, the device Merkle tree has no leaves.

---

## 10. Document Lineage

| Source | What was absorbed | Section |
|--------|------------------|---------|
| CRDM v1.1 Amendment B | Parallel Merkle tree design, feature flag behavior, inscription payload schema | §5 R-2, R-3, R-4, §7 |
| GRO-46 Sovereign Architecture | L1-only device verification concept | §5 R-14 |
| GRO-45 Amendment 8 | `devices` + `transaction_devices` DDL (referenced, not duplicated) | §5 R-2, §9 |
| Inscription Pipeline Design Spec | Device Merkle tree construction algorithm, Chirp flag collection | §5 R-2, R-3 |
| elJeffe Protocol Spec v1.0 Section 5 | Protocol-level attestation block definition | §5 R-4, §7 |

---

*PRD — Device Attestation v1.0 | March 2, 2026*
*MAXIMUM CONFIDENTIAL*
