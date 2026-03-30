---
type: spec
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# PRD: Validation API + L402 Gate
**Version:** 1.0
**Owner:** Jeremy
**Depends on:** Sub 3 output (Ordinal inscriptions + merkle proofs), Lightning Network (LNURL / Invoice API), rate limiting, audit logging
**Gates:** Perpetual revenue stream, user-facing SaaS, compliance proof
**Sprint target:** Sprint 7

---

## Purpose

The Validation API is the user-facing endpoint for verifying that an event was notarized on Bitcoin. Given an event_id (or event_hash) and its inscription_id, any user can submit a verification request. The API implements L402 (HTTP 402 + Lightning Protocol): the request returns an invoice, user pays sats, and the API returns cryptographic proof of notarization. Every verification call generates perpetual revenue for GrowDirect.

**Business Model:** One-time payment per verification. Repeatable forever. Event notarized once, verified unlimited times, each verification pays.

**North Star Alignment:** Make integrity verifiable without friction. Pay once per check. Merchant owns the proof forever.

---

## Acceptance Criteria

1. **L402 Payment Gate:** POST /validate without payment → HTTP 402 Payment Required + Lightning invoice. User pays. Payment callback received. Request resubmitted. Returns 200 OK with proof.

2. **Verification Request:** POST /validate body:
   ```json
   {
     "event_id": "evt_stripe_charge_20260226_123456",
     "inscription_id": "i7f9a2c8d3e4f5a6b7c8d9e0f1a2b3c4d",
     "hash": "a3c7f9e2d4b8c1a6e9f2d5c8a3b7e0f1"
   }
   ```

3. **Proof Response (200 OK):**
   ```json
   {
     "verified": true,
     "event_id": "evt_stripe_charge_20260226_123456",
     "hash": "a3c7f9e2d4b8c1a6e9f2d5c8a3b7e0f1",
     "inscription_id": "i7f9a2c8d3e4f5a6b7c8d9e0f1a2b3c4d",
     "bitcoin_block": {
       "height": 850100,
       "hash": "00000000...",
       "timestamp": "2026-02-26T14:35:22Z"
     },
     "merkle_position": 42,
     "merkle_root": "a3c7f9e2d4b8c1a6e9f2d5c8a3b7e0f1",
     "merkle_proof": [
       "b4d8f0e3a5c9d2b7f0e3a6d9b4c8f1a2",
       "c5e9f1d4a6c0d3e8f1a4b7e0d3f6c9a2",
       ...
     ],
     "canonical_authority": "GrowDirect",
     "verified_at": "2026-02-26T15:42:18.123Z",
     "payment_id": "pay_20260226_987654",
     "previous_verification_count": 5
   }
   ```

4. **Merkle Proof Included:** Response includes full merkle_proof. User can independently verify hash is in Merkle root. Proof is canonical (user does not need to trust us, can verify on Bitcoin).

5. **Rate Limiting:** 100 verification requests per unique caller (API key or Lightning node ID) per hour. Return HTTP 429 Too Many Requests if exceeded.

6. **Audit Log:** Every verification request logged: caller (anonymized), event_id, timestamp, payment_status, result. Immutable audit trail.

7. **Multiple Verifications:** Same event can be verified unlimited times. Each verification pays (perpetual revenue). Cost per verification tunable (default: 1 sat).

8. **Invalid Proof Rejection:** If inscription_id or merkle_proof invalid, return 400 Bad Request (no payment required). Example: event not inscribed yet.

9. **Replay Protection:** Payment token tied to single verification request. Cannot reuse token for multiple verifications.

10. **Error Handling:** If Bitcoin RPC fails or Ordinal indexer unavailable, return 503 Service Unavailable (no payment taken). Merchant can retry.

---

## L402 Implementation

**Step 1: Unsigned Request (no payment)**
```
POST /validate
Content-Type: application/json

{
  "event_id": "evt_xyz",
  "inscription_id": "i_abc",
  "hash": "a3c7f9..."
}

↓

HTTP 402 Payment Required
WWW-Authenticate: Bearer macaroon="...", invoice="lnbc..."
Content-Type: application/json

{
  "status": "payment_required",
  "invoice": "lnbc10n1pj7u3v...",
  "description": "Verification of event evt_xyz on Bitcoin",
  "amount_msat": 10000,
  "amount_sat": 10,
  "expires_in": 3600,
  "payment_hash": "...",
  "preimage_witness": "..."
}
```

**Step 2: User Pays (via Lightning wallet)**
- User scans QR code or pastes invoice into Lightning wallet
- Wallet pays 10 sats (or configured amount)
- Payment routed through Lightning Network
- GrowDirect receives payment notification

**Step 3: Signed Request (with proof of payment)**
```
POST /validate
Content-Type: application/json
Authorization: Bearer macaroon="...", preimage="..."

{
  "event_id": "evt_xyz",
  "inscription_id": "i_abc",
  "hash": "a3c7f9..."
}

↓

HTTP 200 OK
Content-Type: application/json

{
  "verified": true,
  "event_id": "evt_xyz",
  "inscription_id": "i_abc",
  "hash": "a3c7f9...",
  "merkle_position": 42,
  "merkle_root": "a3c7f9e2...",
  "merkle_proof": [...],
  "bitcoin_block": {...},
  "canonical_authority": "GrowDirect",
  "verified_at": "2026-02-26T15:42:18.123Z"
}
```

---

## Test Cases

### Happy Path
- Verification request: valid event_id, inscription_id, hash
- Invoice generated: 1 sat, 3600 sec TTL
- User pays via Lightning wallet
- Macaroon validated
- Merkle proof retrieved from database
- Response: verified=true, merkle_proof, bitcoin_block
- Audit log: entry recorded, payment_status=success

### Edge Cases
- **Event Not Yet Inscribed:** event_id valid, but inscription_id not on Bitcoin yet (< 10 min old). Return 400 Bad Request: "Event not yet confirmed on blockchain. Retry in 10 minutes."
- **Invalid Merkle Proof:** inscription_id exists, but merkle_proof does not reconstruct to root. Return 400 Bad Request: "Merkle proof validation failed. Event may be corrupted."
- **Hash Mismatch:** hash provided does not match stored hash. Return 400 Bad Request: "Hash does not match inscription. Request rejected."
- **Payment Not Received:** Invoice issued, but user doesn't pay within 1 hour. Return 402 with new invoice on retry.
- **Expired Invoice:** User tries to submit signed request with stale macaroon. Return 402 with fresh invoice.
- **Rate Limit:** Caller exceeds 100 requests/hour. Return 429 Too Many Requests: "Rate limit exceeded. Retry after 1 hour."
- **Duplicate Payment:** User pays same invoice twice (edge case, shouldn't happen with well-behaved wallets). Detect duplicate payment_hash. Return 200 (idempotent).

### Toy Store Spike Scenario
- 5,000 events notarized during spike (batched into 6 Ordinals)
- Post-spike, toy store merchant validates sample of 100 events
- Each verification: 1 request per event, 1 sat payment per request
- Total: 100 sat revenue from single merchant validation session
- Repeatable: merchant can validate same 100 events again tomorrow, another 100 sats
- Scaling: 1,000 merchants each verifying 10 events per month = 10,000 verifications = 10,000 sats perpetual monthly revenue

### Failure Modes
- **Bitcoin RPC Down:** Cannot retrieve block height or Merkle proof. Return 503 Service Unavailable. Payment not taken (no payment sent until 200 returned).
- **Lightning Network Congestion:** Invoice generation slow. Return 402 with partial invoice (user may try again).
- **Macaroon Library Failure:** Macaroon validation throws exception. Return 500 Internal Error. Log for ops. Payment refunded (manual process).
- **Audit Log Full:** Audit log disk full. Verification still completes, but audit entry fails. Separate alert to ops.

---

## Integration Points

**Reads from:**
- Sub 3 output: inscription_id, merkle_proof, merkle_position, merkle_root, bitcoin_block per event (stored in evidence_store)
- Bitcoin RPC: block confirmation status (is block in canonical chain?)
- Lightning Node: invoice generation, payment verification

**Writes to:**
- Audit log: request_id, caller_id, event_id, timestamp, payment_id, result
- Metrics: verification_count, revenue_sats_total, request_latency
- Structured logging: all requests (including rejected)

**Validation API Schema:**
```sql
CREATE TABLE validation_api_calls (
  call_id SERIAL PRIMARY KEY,
  requested_at TIMESTAMP NOT NULL,
  event_id VARCHAR(255),
  inscription_id VARCHAR(255),
  hash VARCHAR(64),
  caller_id VARCHAR(255),  -- API key hash or Lightning node ID
  payment_status VARCHAR(50),  -- "pending", "paid", "failed"
  payment_id VARCHAR(255),
  payment_hash VARCHAR(64),
  amount_sat INT,
  result VARCHAR(50),  -- "verified", "not_found", "invalid_proof", "rate_limit"
  response_time_ms INT,
  ip_address INET,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_validation_caller_time
  ON validation_api_calls(caller_id, created_at DESC);
```

---

## Non-functional Requirements

| Requirement | Target | Notes |
|-------------|--------|-------|
| **Invoice Generation Latency** | < 500ms | User sees QR code quickly |
| **Verification Latency (post-payment)** | < 1 second | Merkle proof lookup is O(log N) |
| **Rate Limiting** | 100 requests/hour per caller | Tunable per plan (future) |
| **Payment Processing** | Near-instant (Lightning) | Settlement via Lightning, not on-chain |
| **Macaroon TTL** | 3600 seconds | Invoice and payment proof expire after 1 hour |
| **Audit Log Retention** | Permanent | Immutable, never purged |
| **API Availability** | 99.9% | Excluding scheduled maintenance |
| **Merkle Proof Size** | < 1KB per event | Allow independent verification without large downloads |

---

## Kubernetes Readiness

1. **Is this component stateless?**
   - **Yes.** Validation API reads from database (evidence store, audit log), calls external services (Bitcoin RPC, Lightning node). No local state. Pod restart does not affect functionality.

2. **Does it scale horizontally?**
   - **Yes.** Multiple instances handle independent verification requests. No session affinity. All instances produce identical proof for same input.

3. **Does it support rolling deployment?**
   - **Yes.** Stateless. v1 and v2 coexist. Both use same database schema. No coordination needed.

4. **What is the scaling trigger?**
   - **HTTP request rate.** K8s watches requests/second to /validate endpoint. If > 100 req/sec, spawn additional pod.

5. **Toy store scaling profile?**
   - **Baseline:** 1 instance handles sporadic verification requests (maybe 1–10/day).
   - **High load (1,000 merchants validating samples):** 1 instance sustains ~100 requests/second easily. Scale to 2–3 instances for redundancy, not throughput.

---

## Revenue Model

**Per-Verification Payment:**
- Default: 1 sat per verification
- Tunable: governance policy (future)
- Repeatable: same event verified 1,000 times = 1,000 sats revenue

**Projected Revenue (Example):**
- 100,000 notarized events in first year
- Average 5 verifications per event (regulatory audits, merchant spot-checks, third-party validation)
- 500,000 total verifications
- 500,000 sats (~$250 at $0.0005/sat, varies with BTC price)
- Perpetual: every notarized event generates revenue forever

**Revenue Scaling:**
- More merchants → more notarized events
- More trust in notarization → more verification calls per event
- Revenue increases quadratically (both axes)

---

## IP Protection Notes

**Safe to document externally:**
- L402 protocol (public standard, widely documented)
- Lightning Network (public Bitcoin layer 2)
- Merkle proof verification (public, open-source libraries available)
- Payment model (sat-per-verification is transparent)

**Crown Jewels (do not expose):**
- Exact macaroon implementation (internal auth mechanism)
- Rate limiting thresholds (policy, tuned for load)
- Audit log schema and retention (compliance-sensitive)
- Invoice generation logic (payment flow details)
- Caller ID anonymization strategy (privacy implementation)

---

## Success Criteria

- [ ] L402 flow complete: invoice generated, payment accepted, proof returned
- [ ] Merkle proof independently verifiable: user can reconstruct root from leaf + proof
- [ ] Rate limiting enforced: caller exceeding 100/hour gets 429
- [ ] Audit log immutable: all requests logged with timestamp, caller, result
- [ ] Multiple verifications: same event verified 5 times, 5 sat payments collected
- [ ] Bitcoin unavailable: API returns 503, no payment taken
- [ ] Macaroon validation: invalid proof rejected with 400
- [ ] Integration test: end-to-end verification with real (testnet) Lightning payment

---

## Open Questions

1. **Caller Identification:** How do we identify unique callers without requiring authentication? Lightning node ID? IP + API key? Hybrid?
2. **Payment Custody:** Where do sats go after payment? Treasury address? Multi-sig? Cold storage?
3. **Pricing Governance:** Is sat-per-verification fixed forever, or tunable by policy?
4. **Refund Policy:** If verification fails (Bitcoin RPC error), do we refund the sat payment? How?
5. **Subscription Model:** Should we offer monthly verification subscriptions (unlimited calls for flat fee) as alternative to pay-per-call?
6. **International Compliance:** Do L402 micropayments face regulatory hurdles (AML, KYC)? Test with legal.
7. **Macaroon Key Rotation:** How often do we rotate macaroon signing keys? Impact on audit log?
