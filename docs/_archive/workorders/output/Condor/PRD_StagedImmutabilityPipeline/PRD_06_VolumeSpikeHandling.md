---
type: spec
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# PRD: Volume Spike Handling — Queue Backpressure
**Version:** 1.0
**Owner:** Jeremy + Tom (collaborative)
**Depends on:** Message queue, Sub 1 + Sub 2 + Sub 3 throughput profiles, load balancer, monitoring
**Gates:** Production readiness, SLA compliance, toy store deployment
**Sprint target:** Sprint 6

---

## Purpose

Volume Spike Handling is a cross-cutting specification that describes how the entire staged immutability pipeline (Nodes 1–6) responds to sustained traffic spikes. The system must gracefully accept 50x traffic volume (5,000 events in 6 hours instead of 100 events in 24 hours) without dropping events, losing data, or violating forensic guarantees. This PRD defines queue backpressure behavior, subscriber independence, graceful degradation of detection latency, and recovery to baseline.

**North Star Alignment:** Scale with merchants. Never reject events. Always preserve forensic integrity.

---

## Acceptance Criteria

1. **No Event Loss:** 50x volume spike (baseline 100/day → 5,000 in 6 hours = ~14/minute sustained, 500/minute burst). All events queued, none dropped. Evidence store receives all events.

2. **Independent Subscriber Throughput:** Sub 1, Sub 2, Sub 3 process independently. Sub 1 cannot be blocked by Sub 2 or Sub 3 slowness. If Sub 2 fails or backs up, Sub 1 continues. If Sub 3 (Ordinal minting) falls behind, Sub 1 and Sub 2 unaffected.

3. **Evidence Integrity Never Degrades:** Sub 1 hash-chain integrity guaranteed even under 50x spike. No records skipped, no hashes corrupted, chain links unbroken.

4. **Detection Latency Degrades Gracefully:** Sub 2 may fall behind during spike. Detection results delayed but not lost. Sub 2 catches up within SLA (15 min) after spike ends.

5. **Queue Depth Monitoring:** Real-time metric: queue depth (messages not yet consumed by any subscriber). Alert if depth > 10,000 for > 1 minute. Autoscale subscribers if triggered.

6. **HTTP 200 Still in 3 Seconds:** Sub 1 (Webhook Receipt, PRD_01) returns 200 to webhook sender within 3 seconds, even under spike. Messages published to queue before 200 returned.

7. **Subscriber Scaling:** If queue depth exceeds threshold, autoscale Sub 1 / Sub 2 / Sub 3 pods independently. Target: queue depth < 5,000 at steady state.

8. **No Manual Intervention:** System automatically scales and recovers from 50x spike. No operator action required to prevent data loss.

9. **Return to Baseline:** Within 15 minutes of spike end, detection latency returns to baseline (< 15 seconds from event receipt to detection available).

10. **Toy Store Test Scenario:** 5,000 events in 6 hours. All in evidence store. Chain integrity verified. Detection results available for all 5,000 within SLA. System returns to baseline within 15 min.

---

## System Model Under Spike

```
Spike Profile:
  Baseline: 100 events / 24 hours = 4.2 events / hour = 0.07 events / second
  Spike: 5,000 events / 6 hours = 833 events / hour = 0.23 events / second
  Spike Factor: 50x (but only 6-hour window, not sustained indefinitely)

Queue Behavior:
  Ingest rate: 0.23 events/sec (500 events in 60 seconds burst)
  Sub 1 throughput (evidence store): ~10 inserts/sec (50x = 5 inserts/sec needed, headroom 2x)
  Sub 2 throughput (structured store): ~10 parses+inserts/sec (similar)
  Sub 3 throughput (batch accumulation): asynchronous, not blocking

Queue Depth Target:
  Baseline: < 100 messages (all subscribers keeping up)
  During spike: < 5,000 messages (evidence store still ingesting faster than queue arrival)
  Peak: < 10,000 messages (alert threshold, trigger autoscale)
  After spike: decay to < 100 within 15 minutes
```

---

## Queue Backpressure Mechanism

**If Queue Depth > 10,000 (Alarm Threshold):**
1. Autoscale Sub 1 instances: spawn 1 additional pod
2. Autoscale Sub 2 instances: spawn 1 additional pod
3. Monitor queue depth every 30 seconds
4. If still > 10,000 after 1 minute, spawn additional pod

**If Queue Depth > 20,000 (Critical Threshold):**
1. Spawn 2 additional pods simultaneously (urgent)
2. Log alert: "Critical queue depth. Spike may be larger than anticipated."
3. Operator notified

**If Queue Depth > 50,000 (Saturation Threshold):**
1. Spawn all available pod capacity
2. Begin rate-limiting new webhook submissions: return HTTP 503 (temporary)
3. Existing queued events continue processing
4. Resume accepting webhooks when queue depth < 10,000

---

## Sub 1 (Evidence Store) Behavior Under Spike

| Scenario | Behavior | Evidence Integrity |
|----------|----------|-------------------|
| Queue depth < 5,000 | Process at max sustainable rate (~10 INSERTs/sec) | Perfect (no backlog) |
| Queue depth 5,000–10,000 | Process at max rate, queue accumulating | Perfect (evidence guaranteed) |
| Queue depth > 10,000 | Autoscale triggered, second instance spawned | Perfect (both instances independent) |
| Queue depth > 20,000 | Autoscale urgent, 2 pods spawned | Perfect (no skips, no loss) |

**Key Property:** Sub 1 never drops evidence. Worst case: backlog in queue, but all eventually stored.

---

## Sub 2 (Structured Store) Behavior Under Spike

| Scenario | Detection Latency | SLA Impact |
|----------|------------------|-----------|
| Queue depth < 1,000 | < 5 seconds | Exceeds SLA |
| Queue depth 1,000–5,000 | 5–15 seconds | At SLA |
| Queue depth 5,000–10,000 | 15–60 seconds | Exceeds SLA temporarily |
| Queue depth > 10,000 | Up to 5 minutes | Temporary miss, recovers after spike |

**Graceful Degradation:** Detection latency increases linearly with queue depth during spike. No events lost. All detection results eventually available. SLA recovers within 15 min after spike end.

---

## Sub 3 (Ordinal Minter) Behavior Under Spike

Sub 3 is asynchronous, not blocking. It batches events every 10 minutes (or per batch policy). During spike:
- Queue accumulates events
- Sub 3 continues batching at its normal rate
- Some events wait > 10 min for next Ordinal batch
- No data loss: all eventually inscribed
- Blockchain immutability unchanged

**Key Property:** Sub 3 failure or delay does not block Sub 1 or Sub 2. Evidence and detection unaffected.

---

## Detection Spike Scenario — Detailed Walkthrough

**T = 0:00** Spike begins. 500 webhooks in 60 seconds.

```
T=0:00–1:00
  Ingest: 500 webhooks queued
  Queue depth: 500
  Sub 1: ingesting at 10 events/sec → 60 events stored
  Queue depth: 500 - 60 = 440
  Sub 2: parsing at 10 events/sec → 60 detection runs
  Detection latency: < 5 seconds (queue small)

T=1:00–2:00
  Ingest: +500 webhooks (1,000 total in queue)
  Sub 1: +60 events stored (120 total)
  Sub 2: +60 events detected (120 total)
  Queue depth: 1,000 - 120 = 880
  Detection latency: still < 5 seconds (queue < 2,000)

T=2:00–3:00
  Ingest: +500 webhooks (1,500 total in queue)
  Sub 1 + Sub 2: process 120 combined
  Queue depth: 1,500 - 120 = 1,380
  Detection latency: 10–15 seconds (queue > 1,000)

T=3:00–4:00
  Ingest: +500 webhooks (1,880 in queue)
  Sub 1 + Sub 2: process 120 combined
  Queue depth: 1,880 - 120 = 1,760
  Detection latency: 15–30 seconds
  Autoscale check: queue depth < 5,000, no scale yet

T=4:00–5:00
  Ingest: +500 webhooks (2,260 in queue)
  Sub 1 + Sub 2: process 120 combined
  Queue depth: 2,260 - 120 = 2,140
  Detection latency: 30–60 seconds

T=5:00–6:00
  Ingest: +500 webhooks (2,640 in queue)
  Sub 1 + Sub 2: process 120 combined
  Queue depth: 2,640 - 120 = 2,520
  Detection latency: 60 seconds (but recoverable)

T=6:00 (Spike ends)
  No new webhooks
  Queue depth: 2,520 existing
  Sub 1 + Sub 2: process at full rate (no queue pressure)
  Queue drains: 2,520 / (60 events/min) = 42 minutes

T=6:42
  Queue empty
  All events detected
  System returns to baseline
```

**Result:** All 5,000 events stored in evidence. Detection latency degraded during spike but all completed. No data loss.

---

## Queue Depth Metrics & Monitoring

**KPIs to Monitor:**

| Metric | Baseline | Spike | Recovery |
|--------|----------|-------|----------|
| Queue depth (messages) | < 100 | 1,000–2,500 | < 100 (T+42 min) |
| Sub 1 throughput (events/sec) | 0.07 | 10 | 10 |
| Sub 2 throughput (events/sec) | 0.07 | 10 | 10 |
| Detection latency (seconds) | < 5 | < 60 | < 5 (T+42 min) |
| P99 HTTP response time | < 1 sec | < 3 sec | < 1 sec |
| Pod count (Sub 1) | 1 | 1–2 | 1 |
| Pod count (Sub 2) | 1 | 1–2 | 1 |

**Alerting Thresholds:**
- Queue depth > 10,000 for > 1 min → Alert "Queue backing up"
- Queue depth > 20,000 for > 30 sec → Alert "Critical queue depth"
- Detection latency > 60 sec → Alert "Detection SLA breached" (informational during spike, critical after)
- Sub 1 INSERT latency > 200ms P99 → Alert "Evidence store latency degraded"

---

## Failure Mode: Subscriber Stalled

**Scenario:** Sub 2 (Structured Store) crashes mid-spike.

**System Behavior:**
1. Sub 2 pod fails. Messages remain in queue.
2. Sub 1 and Sub 3 continue independently. No impact.
3. Evidence store still receiving all events.
4. Kubernetes restarts Sub 2 pod.
5. Sub 2 resumes consuming queue from where it left off.
6. Missing detection results are back-filled (replay if needed).
7. Queue drains normally.

**Evidence Integrity:** Not affected. Sub 1 has all evidence.

---

## Toy Store Spike Test Plan

**Pre-Test:**
1. Establish baseline: measure 100 events/day ingest pattern for 1 week
2. Verify Sub 1, Sub 2, Sub 3 each processing independently
3. Confirm queue depth < 100 at baseline

**Test Execution (T=0 to T=6 hours):**
1. Send 5,000 toy store webhooks over 6-hour window
2. Monitor queue depth, Sub 1 throughput, Sub 2 detection latency every 30 seconds
3. Record autoscale events (if any)
4. Track all events to confirmation (evidence store + detection results)

**Post-Test (T=6 to T=7 hours):**
1. Verify queue empty
2. Count evidence_store records: should be 5,000 (+ baseline)
3. Verify hash chain integrity: run Bilateral Verification on sample (10 events) across range
4. Verify detection results available for all 5,000 events
5. Measure recovery time: when did queue depth return to < 100? (Target: 15 min)

**Success Criteria:**
- [ ] All 5,000 events in evidence store
- [ ] Zero events dropped
- [ ] Hash chain unbroken
- [ ] Detection results available for all 5,000 within SLA
- [ ] Queue depth returned to baseline within 15 minutes
- [ ] System handled spike without manual intervention

---

## Non-functional Requirements

| Requirement | Target | Notes |
|-------------|--------|-------|
| **Max queue depth (alarm)** | 10,000 messages | Trigger autoscale |
| **Queue drain rate** | 60 events/minute combined (Sub 1 + Sub 2) | Allows recovery from spike |
| **Evidence integrity SLA** | 100% | No records lost, chain unbroken |
| **Detection SLA (spike window)** | Results available within 60 sec after event parsed | Temporary miss during peak is acceptable |
| **Detection SLA (post-spike)** | Results available within 15 sec after event receipt | Recovers to baseline |
| **Autoscale response time** | < 2 minutes to spawn new pod | Queue alarm → pod running |
| **HTTP 200 latency (spike)** | < 3 seconds | No degradation from baseline |

---

## Kubernetes Readiness (System-Level)

1. **Auto-scaling:** K8s HPA configured to watch queue depth metric. Scales Sub 1, Sub 2, Sub 3 independently based on respective queue consumption rates.

2. **Resource Limits:** Each subscriber pod has CPU/memory limits. If limits hit, K8s may throttle. Monitor for resource saturation during spike.

3. **PDB (Pod Disruption Budget):** Define PDB to ensure minimum instances remain during node eviction.

4. **Monitoring:** Prometheus scrapes queue depth, subscriber throughput, latency metrics. Grafana dashboards for ops visibility.

---

## IP Protection Notes

**Safe to document externally:**
- Queue backpressure concept (standard architecture)
- Graceful degradation narrative (industry best practice)
- Spike recovery mechanism (scaling, not proprietary)

**Crown Jewels (do not expose):**
- Exact queue depth thresholds (10,000, 20,000, 50,000)
- Autoscale trigger policy (proprietary SLA enforcement)
- Subscriber independence implementation details
- Queue-to-subscriber mapping (system topology)

---

## Success Criteria

- [ ] 5,000 events in 6-hour spike: all in evidence store, zero drops
- [ ] Queue depth never exceeds 20,000 (without operator intervention)
- [ ] Detection latency degrades to < 60 sec during spike, recovers to < 5 sec within 15 min
- [ ] Sub 1, Sub 2, Sub 3 independently resilient (one failure doesn't cascade)
- [ ] Kubernetes autoscale functional (queue depth triggers scale-up)
- [ ] Full toy store spike test passes all criteria

---

## Open Questions

1. **Rate limiting ceiling:** At what ingest rate (> 50x) do we begin rejecting webhooks?
2. **Ordinal batching:** Does Sub 3 batch window (10 min) create unfair delay for recent events? Adjust batch window during spike?
3. **Detection priority:** During spike, should high-priority merchants get detection results first (unfair)?
4. **Queue strategy:** Should we use priority queue (Sub 1 first, then Sub 2, Sub 3 asynchronously)?
