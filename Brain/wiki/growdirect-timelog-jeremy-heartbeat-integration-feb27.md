---
date: 2026-04-22
type: wiki
tags: [growdirect, timelog, jeremy, heartbeat, integration-test, b-064, pipeline]
sources:
  - docs/_archive/ip-vault/timelogs/2026/02-February/daily/2026-02-27_Jeremy_HeartbeatIntegration.md
last-compiled: 2026-04-22
needs-review: 2026-05-06
---

**Wiki:** [[Brain/Home|Home]]

# Session — Jeremy: Heartbeat Integration Testing (Feb 27, 2026)

**Filed by:** ALX | Claude Code (Opus 4.6) | Session s7
**Duration:** ~2.5h effective (long-running with Docker rebuilds + wait times)

Executed the 9-step B-064 integration test sequence. Full end-to-end pipeline verification against real Docker services. **Found and fixed 4 bugs during testing.**

## Work Product — Files Modified

| File | Change | PRD Trace |
|---|---|---|
| `canary/migrations/sales/versions/004_extend_ingestion_log_for_tsp.py` | Fixed `down_revision` from `"003"` to `"003_immutability_triggers"` (Alembic chain break) | TSP-01 |
| `canary/services/tsp/stream_publisher.py` | Added `socket_timeout=30`, `socket_connect_timeout=5` to `Redis.from_url()` | TSP-02 |
| `canary/db/session_factory.py` | Changed `_set_rls_context(self, connection, _)` → `_=None` (SQLAlchemy event signature fix) | Infrastructure |
| `canary/services/evidence_chain.py` | Cast `memoryview` to `bytes()` in `compute_chain_hash()` concatenation | TSP-03 |
| `requirements.txt` | Changed `squareup>=43.0.0` → `squareup` (per Jeffe: always take latest, never pin) | B-063 |

## Integration Test Results — 9/9 PASS

| Step | Test | Result |
|---|---|---|
| 1 | Docker services up (Postgres + Valkey + Flask) | PASS |
| 2 | Alembic migrations 004–006 applied | PASS |
| 3 | Flask webhook endpoint responds (GET → 405) | PASS |
| 4 | Sub 1 worker connects and blocks on XREADGROUP | PASS |
| 5 | Sub 3 worker connects and blocks on XREADGROUP | PASS |
| 6 | Test webhook POST → 200 OK, ULID assigned | PASS |
| 7 | Evidence sealed in evidence_records (chain linked) | PASS |
| 8 | Mock inscription in inscription_pool (confirmed) | PASS |
| 9 | Receipt endpoint returns full proof JSON | PASS |

## B-063 SDK Version Check — 0.25h

Verified squareup SDK version per standing directive. Upgraded v41.0.0 → v44.0.1 (latest). Updated `requirements.txt` per Jeffe directive to remove version pin.

## Token Consumption

| Category | Tokens | Est. Cost |
|---|---|---|
| Input (new) | 328 | $0.00 |
| Cache creation | 561,672 | $10.53 |
| Cache read | 33,785,648 | $63.35 |
| Output | 2,539 | $0.19 |
| **TOTAL** | **34,350,187** | **$74.07** |

**Model:** Claude Opus 4.6 (307 API calls)
**Cache hit rate:** 98.4% (excellent — well above 85% target)

### Allocation by Deliverable

| Deliverable | Est. Cost |
|---|---|
| Docker + migration debugging | ~$22 |
| Sub 1/Sub 3 worker debugging (socket timeout, RLS, memoryview) | ~$32 |
| Webhook testing + receipt verification | ~$12 |
| TRIAGE/HANDOFF updates | ~$8 |

### Efficiency Notes

- **Cache hit rate 98.4%** — excellent context reuse despite 4 container rebuilds
- **High token spend** driven by iterative debugging cycle (5 test webhook attempts to resolve 4 sequential bugs)
- **Each bug required container rebuild** (code baked into Docker image, no volume mount for app code) — future optimization: mount `/app` as volume in dev compose
- **Context continuation** from prior session added overhead but preserved full debugging history
- **Cost per bug fix:** ~$14.81 (higher than baseline due to iterative Docker rebuild cycle)

## Key Decisions

1. `squareup` version pin removed — Jeffe directive: "always take latest certified SDK, not be specific"
2. `BATCH_TIME_THRESHOLD_SECONDS=10` used for testing (production default 600s) — temporary override, not committed
3. All 4 bug fixes are surgical (<5 lines each) and trace to PRDs per B-064 rule

## Session Summary

Pipeline proven end-to-end: webhook received → HMAC verified → SHA-256 hashed → published to Valkey stream → Sub 1 sealed evidence with chain hash → Sub 3 built Merkle tree + mock inscription → receipt endpoint returned full verified proof JSON. Four infrastructure-level bugs discovered and fixed during testing. **Next gate: live Square webhook from Jeffe's phone.**

## Related

- [[Brain/projects/GrowDirect|GrowDirect MOC]]
- [[Brain/wiki/growdirect-working-papers|Working Papers Structure]]
- [[Brain/wiki/growdirect-triple-subscriber|Triple Subscriber Pipeline]]
- [[Brain/wiki/growdirect-timelog-b059-execution-feb27|B-059 Execution]] — PRDs being implemented
- [[Brain/wiki/growdirect-the-pipe|The Protocol Pipe]] — end-to-end data flow

## Sources

- `docs/_archive/ip-vault/timelogs/2026/02-February/daily/2026-02-27_Jeremy_HeartbeatIntegration.md`
