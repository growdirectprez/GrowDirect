---
type: spec
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# PRD: Webhook Receipt + Queue Ingestion
**Version:** 1.0
**Owner:** Jeremy
**Depends on:** HMAC signature validation library, message queue (RabbitMQ or Kafka), HTTP framework
**Gates:** All downstream subscribers (Sub 1, Sub 2, Sub 3)
**Sprint target:** Sprint 6

---

## Purpose

Webhook Receipt is the entry point for all notarization. Any webhook from any network (Stripe, Square, PayPal, custom, etc.) arrives at the API gateway, has its signature validated, and is published verbatim to the queue. The component must return HTTP 200 within 3 seconds, never fail silent, and ensure every validated webhook enters the queue exactly once.

**North Star Alignment:** Simplify merchant integration. One webhook endpoint, universal signature validation, idempotent.

---

## Acceptance Criteria

1. **Signature Validation:** HMAC signature (per webhook provider specification) is validated before any processing. Rejection produces HTTP 401 with no queue entry.

2. **400 on Missing Header:** If required signature header is absent, return HTTP 400 Malformed Request with no queue entry.

3. **Verbatim Payload:** Raw webhook body is published to queue without modification, transformation, or interpretation. Original encoding preserved.

4. **Event ID Idempotency:** Generated event_id is unique within merchant namespace. Duplicate event_id (same webhook re-posted) returns 200 but does not re-queue.

5. **Queue Publish Atomic:** HTTP 200 returned to webhook sender only after message successfully published to queue. No 200 before queue confirmation.

6. **Latency SLA:** Entire receipt + validation + queue publish completes within 3 seconds. P99 latency < 2 seconds under baseline load.

7. **Burst Capacity:** 500 webhooks in 60 seconds accepted without queue overflow or message loss.

8. **Failed Validation Isolation:** Validation failures (bad signature, malformed header) do not degrade performance for valid webhooks. Failed requests logged but never queued.

9. **Merchant Context:** Merchant identifier extracted from webhook signature or request header and propagated through entire pipeline.

---

## Test Cases

### Happy Path
- Stripe webhook arrives with valid Stripe signature
- Signature validates successfully
- Payload published to queue verbatim
- HTTP 200 returned within 2 seconds
- Downstream subscribers receive identical payload

### Edge Cases
- **Duplicate Webhook:** Same webhook body, same signature, posted twice within 1 second → First returns 200 + queues, second returns 200 + no queue entry
- **Malformed Signature:** Header present but invalid format → HTTP 400, no queue entry
- **Missing Header:** Required signature header absent → HTTP 401, no queue entry
- **Empty Payload:** Valid signature, empty body → Queued verbatim (empty), downstream handles gracefully
- **Large Payload:** 10MB webhook (e.g., image data) → Queued, latency within SLA
- **Non-UTF8 Encoding:** Binary payload with valid signature → Queued as-is, downstream handles

### Toy Store Spike Scenario (REQUIRED)
- Toy store integration sends 500 webhooks in 60-second window (8.3/second, baseline 100/day)
- All 500 webhooks have valid signatures
- All 500 published to queue successfully
- Zero webhooks dropped
- HTTP 200 returned for all within 3 seconds
- System returns to baseline latency within 15 seconds of spike end

### Failure Modes
- **Queue Unavailable:** Queue connection fails. Return HTTP 503 Service Unavailable. Client retries webhook after backoff.
- **Signature Library Fails:** HMAC computation throws exception. Log error, return HTTP 500, do not queue.
- **Rate Limit (future):** If enabled, HTTP 429 Too Many Requests. Log and reject, but do not queue.

---

## Integration Points

**Reads from:**
- HTTP request (webhook POST body, headers)
- HMAC signature validation library
- Merchant registry (to map signature key to merchant_id)

**Writes to:**
- Message queue (verbatim payload + event_id + timestamp + merchant_id)
- Structured logging (signature validation results, queue publish confirmation, latency metrics)

**Queue Message Format:**
```json
{
  "event_id": "evt_1a2b3c4d5e6f7g8h9i",
  "merchant_id": "merchant_12345",
  "received_at": "2026-02-26T14:23:45.123Z",
  "signature_provider": "stripe",
  "raw_payload": "{...original webhook body, verbatim...}",
  "payload_hash": "sha256_hex"
}
```

---

## Non-functional Requirements

| Requirement | Target | Notes |
|-------------|--------|-------|
| **Throughput** | 1,000 webhooks/minute | Supports 50x spike (5,000 in 6 hours = ~14/minute sustained, 500 in 60 seconds burst) |
| **Latency (P50)** | < 500ms | Receipt + validation + queue publish |
| **Latency (P99)** | < 2 seconds | 99% of requests within SLA |
| **Availability** | 99.9% | Excludes scheduled maintenance |
| **Signature schemes** | HMAC-SHA256, HMAC-SHA1, RSA-SHA256 | Extensible per provider |
| **Queue retention** | TBD | Downstream subscribers must drain within queue TTL |
| **Idempotency window** | 24 hours | Duplicate detection within 24-hour sliding window per merchant |

---

## Kubernetes Readiness

1. **Is this component stateless?**
   - **Yes.** No local state. Merchant context retrieved from signature. Queue publish is idempotent (duplicate event_id detected on arrival at Sub 1). Can restart on any node without data loss.

2. **Does it scale horizontally?**
   - **Yes.** 3 instances == 1 instance semantically. Each handles independent webhooks. Idempotency enforced downstream (Sub 1). No session affinity required.

3. **Does it support rolling deployment (v1 and v2 simultaneously safe)?**
   - **Yes.** Both versions use same queue format. Queue message structure is backward compatible. v1 and v2 instances can coexist. Graceful drain on update.

4. **What is the scaling trigger?**
   - **Queue depth metric.** K8s watches message queue backlog size. If queue depth > 10,000 messages for > 1 minute, spawn additional Receipt pod. Target: queue depth < 5,000 at steady state.

5. **Toy store scaling profile (50x spike)?**
   - **Baseline:** 1 instance handles 100 events/day (~1 event per 14 minutes).
   - **50x spike (5,000 events / 6 hours):** 2–3 instances handle 500 events/minute = ~167 events/instance/minute. Single instance can handle 500/min without bottleneck. Scale to 2–3 for queue latency headroom and redundancy.

---

## IP Protection Notes

**Safe to document externally:**
- Triple subscriber pattern (architectural overview)
- Idempotency mechanism (concept, not implementation detail)
- Signature validation (standard HMAC, widely used)

**Do not expose:**
- Specific merchant registry lookup mechanism
- Event ID generation algorithm
- Exact idempotency deduplication window (internal SLA)
- Queue depth monitoring thresholds (scaling policy)

---

## Success Criteria

- [ ] 500 webhooks in 60 seconds: all queued, zero drops
- [ ] Duplicate webhook detection: idempotent within 24 hours
- [ ] Invalid signature: rejected before queue
- [ ] Latency P99 < 2 seconds under baseline + spike load
- [ ] Kubernetes scaling: auto-scales to 2–3 instances during spike
- [ ] Integration test: end-to-end with Sub 1, Sub 2 verify payload verbatim

---

## Open Questions

1. **Signature scheme versioning:** If merchant changes signature key mid-integration, how do we handle stale keys in flight?
2. **Merchant registry source:** Is merchant_id pulled from signature key metadata, request header, or external lookup?
3. **Queue TTL policy:** What is maximum acceptable age for queued message before Sub 1, 2, 3 must have consumed?
4. **Failed validation logging:** Should we PII-mask failed webhook bodies, or log full body for forensics?
