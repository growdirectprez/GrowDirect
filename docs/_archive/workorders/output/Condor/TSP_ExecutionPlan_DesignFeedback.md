---
type: spec
domain: tsp
status: active
created: 2026-03-18
updated: 2026-03-19
---
# TSP Execution Plan & Design Feedback

## Context

Condor produced 10 PRDs (TSP-00 through TSP-09) specifying the Triple Subscriber Pipeline — a universal webhook notarization system that processes events through three decoupled Valkey Streams consumers: Sub 1 (immutable evidence/hash chain), Sub 2 (structured CRDM store), and Sub 3 (Bitcoin Merkle inscription). The specs also cover a detection engine, L402 validation API, bilateral verification, and replay/rebuild.

Jeffe asked for two deliverables:
1. **Execution plan** — how to build this, in what order, reusing what exists
2. **Design feedback** — issues and improvements to send back to the design team

---

## Part 1: Execution Plan

### Dependency Graph (Build Order)

```
TSP-01 (Webhook Receipt)
  └─► TSP-02 (Queue Fan-Out)
        ├─► TSP-03 (Sub 1 — Hash Seal)      ── parallel track A
        ├─► TSP-04 (Sub 2 — Parse/Route)     ── parallel track B
        │     └─► TSP-06 (Detection Engine)   ── after Sub 2
        └─► TSP-05 (Sub 3 — Merkle)          ── parallel track C
              └─► TSP-07 (L402 Validation)    ── Sprint 7+
                    └─► TSP-08 (Bilateral)    ── Sprint 7+
TSP-09 (Replay/Rebuild) ── after TSP-03 + TSP-04 stable
```

### Infrastructure Prerequisites (Week 0)

| ID | Task | File(s) | Notes |
|----|------|---------|-------|
| A | Rewrite `valkey.conf` | `devops/valkey/valkey.conf` | `maxmemory 2gb`, `maxmemory-policy noeviction`, `appendonly yes`, `appendfsync everysec`, `stream-node-max-bytes 4096`, `stream-node-max-entries 100` |
| B | Add `canary:events` stream init to startup | New: `canary/services/queue/stream_manager.py` | XGROUP CREATE with MKSTREAM, idempotent |
| C | Create `evidence_records` table migration | New migration in `canary/migrations/app/versions/` | DDL from TSP-03 §4 + `prevent_mutation()` trigger reusing pattern from `migrations/sales/versions/003_add_immutability_triggers_financial_tables.py` |
| D | Extend `ingestion_log` schema | New migration in `canary/migrations/sales/versions/` | Add `event_hash`, `source_event_id`, `ip_address`, `user_agent` columns to existing model at `canary/models/sales/ingestion.py` |

### Sprint 6 — Four Parallel Tracks

**Track A: Webhook Receipt + Queue (TSP-01 → TSP-02)**
- Week 1: HMAC validation middleware, raw-body capture, XADD publisher
- Week 2: Consumer group setup, Claim Monitor process, Stream Trimmer
- Key reuse: `canary/blueprints/webhooks.py` (extend, don't replace), `canary/services/webhook_router.py` (REPLACE sync DB writes with XADD, REUSE event-type routing logic)

**Track B: Sub 1 — Hash Seal (TSP-03)**
- Week 1: `sub1_seal` consumer, evidence_records writer, chain hash (BYTEA concat — new function, do NOT reuse `hash_chain.py` pipe-delimited format)
- Week 2: Advisory lock serialization per merchant, write-once trigger, gap detection
- Key reuse: Trigger pattern from `migrations/sales/versions/003_add_immutability_triggers_financial_tables.py`
- Key note: Existing `canary/services/hash_chain.py` uses different algorithm — KEEP for existing uses, create `evidence_chain.py` for TSP-03

**Track C: Sub 2 — Parse/Route (TSP-04)**
- Week 1: `sub2_parse` consumer, parser dispatch
- Week 2: CRDM table writes, idempotency, XACK
- Key reuse: ALL existing parsers (`square_payment_parser.py`, `square_order_parser.py`, `square_auxiliary_parsers.py`) — refactor to accept raw dict input instead of webhook envelope

**Track D: Sub 3 — Merkle (TSP-05, logic only)**
- Week 2–3: Merkle tree construction, batch accumulator, deterministic leaf ordering
- Sprint 6 scope: Tree logic + tests only. OrdinalsBot/Bitcoin inscription deferred to Sprint 7+

**Post-Tracks (Week 3–4):**
- Detection Engine (TSP-06): Wire `sub2_parse` completion → Chirp evaluation → WebSocket push
- Key reuse: `canary/services/chirp/rule_engine.py` (REUSE fully), `canary/services/chirp/rule_definitions.py` (26 rules already defined)
- Add to detection models: `event_id`, `title`, `description` columns + dedup constraint (`canary/models/app/detection.py`)

### Sprint 7+ Deferrals

| PRD | Reason |
|-----|--------|
| TSP-05 Bitcoin inscription | No OrdinalsBot API key, no Bitcoin Core node provisioned |
| TSP-07 L402 Validation | No Strike API key, Lightning infra not provisioned |
| TSP-08 Bilateral Verification | Depends on TSP-07 |
| TSP-09 Replay/Rebuild | Needs TSP-03 + TSP-04 stable in production first |

### Reuse vs Replace Matrix

| Component | Action | Notes |
|-----------|--------|-------|
| `webhook_router.py` | REPLACE flow / REUSE routing | Swap DB writes for XADD, keep event dispatch map |
| `square_*_parser.py` (3 files) | REUSE / refactor input | Accept raw dict, not webhook envelope |
| `rule_engine.py` | REUSE fully | Wire as TSP-06 consumer callback |
| `rule_definitions.py` | REUSE | 26 rules already cataloged |
| `threshold_manager.py` | REUSE / wire Valkey | `valkey_client` is None — connect it |
| `hash_chain.py` | KEEP (don't touch) | Different algorithm — create new `evidence_chain.py` for TSP-03 |
| `ingestion.py` model | EXTEND | Add missing columns via migration |
| `detection.py` models | EXTEND | Add `event_id`, `title`, `description`, dedup constraint |
| `valkey.conf` | REPLACE entirely | Cache config → Streams config |
| Migration 003 triggers | REUSE pattern | Copy `prevent_mutation()` for `evidence_records` |

---

## Part 2: Design Feedback for Condor/PhD

### Critical (Must Fix Before Build)

**C-1: Kubernetes references throughout — no K8s exists**
All PRDs reference K8s pods, HPA scaling, node affinity. Actual infra is Docker Compose (`devops/docker-compose.alpha3x.yml`). Every deployment/scaling section needs rewrite for Compose + Gunicorn workers.
- Affected: TSP-01 §8, TSP-02 §7, TSP-03 §8, TSP-04 §8, TSP-05 §9, TSP-06 §8

**C-2: `ingestion_log` schema mismatch**
TSP-01 proposes `ingestion_log` with BIGSERIAL PK in `canary_app`. Existing table has UUID PK in `canary_sales`, missing `event_hash`, `source_event_id`, `ip_address`, `user_agent`. PRD should specify this as a migration/extension, not a new table.
- Affected: TSP-01 §4
- Existing: `canary/models/sales/ingestion.py`

**C-3: TSP-04 still references pub/sub for detection notification**
TSP-04 §5.4 says "PUBLISH canary:detection:trigger" but TSP-06 changed to Streams consumer pattern. Cross-PRD desync — one says pub/sub, the other says Streams.
- Affected: TSP-04 §5.4, TSP-06 §3

**C-4: Valkey config assumptions are wrong**
All PRDs assume Streams-ready Valkey. Actual config: `maxmemory 256mb`, `allkeys-lru`, `appendonly no`. LRU eviction will silently DROP stream entries. AOF off means stream data lost on restart.
- Affected: TSP-02 §3 (entire fan-out depends on this)
- Fix: `devops/valkey/valkey.conf`

### High (Should Fix Before Build)

**H-1: Per-group claim timeouts missing from TSP-02**
TSP-05 needs 90-minute claim timeout for `sub3-merkle` (batch accumulation window). TSP-02 §3 doesn't specify per-group timeout configuration. Claim Monitor in TSP-02 §5 uses single timeout for all groups.
- Affected: TSP-02 §3, §5

**H-2: Advisory lock coordination not in TSP-04**
TSP-09 §5.2 requires Sub 2 to participate in advisory lock coordination during replay. TSP-04 has no mention of advisory locks. Add lock acquisition before CRDM writes.
- Affected: TSP-04 §5

**H-3: PORT=3000 conflict**
TSP-06 §5.4 WebSocket on port 3000 conflicts with potential dev server ports. Should use a dedicated port or path-based routing through existing Gunicorn.
- Affected: TSP-06 §5.4

**H-4: Flask is not async — WebSocket assumption**
TSP-06 assumes WebSocket push from Flask. Flask 3.0 with Gunicorn doesn't natively support WebSocket. Need either flask-sock, gevent worker, or SSE fallback. PRD should specify the mechanism.
- Affected: TSP-06 §5.4

**H-5: Chain hash algorithm differs from existing code**
TSP-03 specifies BYTEA concatenation: `SHA256(prev_hash || event_hash || merchant_id || seq)`. Existing `hash_chain.py` uses pipe-delimited string: `SHA256(f"{prev}|{payload}|{merchant}|{seq}")`. PRD should explicitly acknowledge this is a NEW algorithm, not a modification of existing.
- Affected: TSP-03 §5.2

**H-6: No Bitcoin Core or Strike API provisioned**
TSP-05 references OrdinalsBot API, TSP-07 references Strike API. Neither service is provisioned, no API keys exist, no spend caps approved. These should be flagged as Sprint 7+ prerequisites with explicit Jeffe approval for spend.
- Affected: TSP-05 §6, TSP-07 §4

### Medium (Should Fix During Build)

**M-1: Webhook endpoint path mismatch**
TSP-01 proposes `/webhooks/{source}`. Existing endpoint is `/webhooks` (no source param). Migration path not specified.
- Affected: TSP-01 §3
- Existing: `canary/blueprints/webhooks.py`

**M-2: RULE_CATALOG not loaded from DB**
TSP-06 assumes rules from `detection_rules` table. Existing `rule_definitions.py` has 26 hardcoded dataclass rules in `RULE_CATALOG`. PRD should specify migration strategy (seed DB from catalog? dual-read?).
- Affected: TSP-06 §4
- Existing: `canary/services/chirp/rule_definitions.py`

**M-3: ThresholdManager Valkey not wired**
`threshold_manager.py` has `valkey_client = None`. TSP-06 assumes working cache layer. Need explicit wiring step.
- Affected: TSP-06 §4
- Existing: `canary/services/chirp/threshold_manager.py`

**M-4: Timecard webhook availability**
TSP-04 maps `labor.shift.*` events. Jeremy's SDK audit (P0-1) confirms Labor API is poll-only, no webhooks. PRD should note this as poll-based or deferred.
- Affected: TSP-04 §5.3

**M-5: Three-database routing not specified**
PRDs reference tables across `canary_app`, `canary_sales`, `canary_metrics` but consumer code doesn't specify which SQLAlchemy bind to use for which write. Should add bind annotations.
- Affected: TSP-03 §4 (canary_app), TSP-04 §5 (canary_sales), TSP-06 §4 (canary_app)

**M-6: Replay trigger bypass mechanism**
TSP-09 uses `SET LOCAL canary.replay_mode = 'true'` to bypass immutability triggers. This requires triggers to check `current_setting('canary.replay_mode', true)`. Existing triggers in migration 003 don't have this check.
- Affected: TSP-09 §5.2
- Existing: `canary/migrations/sales/versions/003_add_immutability_triggers_financial_tables.py`

### Low (Nice to Have)

**L-1: El Jeffe business model bridge incomplete**
TSP-05/TSP-07 reference Genesis Pool and Layer concepts from `ElJeffe_BusinessModel_Addendum.md` but don't specify concrete integration points (pricing tiers, pool allocation logic).
- Affected: TSP-05 §7, TSP-07 §6

**L-2: Monitoring/alerting not specified**
No PRD covers operational monitoring: consumer lag alerts, stream memory usage, hash chain gap detection dashboards. Should add ops appendix.
- Affected: All PRDs

**L-3: Consumer group naming convention**
TSP-02 uses `sub1-seal`, `sub2-parse`, `sub3-merkle`. Detection engine in TSP-06 would need a 4th group name. Naming convention should be formalized.
- Affected: TSP-02 §3, TSP-06 §3

**L-4: Test strategy gaps**
PRDs include unit test examples but no integration test strategy for the full pipeline (webhook → stream → 3 consumers → detection → alert). Should add end-to-end test plan.
- Affected: TSP-00 §6

**L-5: IP classification scope**
TSP-00 §7 IP protection summary is thorough but doesn't classify the Merkle batch accumulator algorithm or the replay cursor mechanism. Both may be patentable.
- Affected: TSP-00 §7

### Cross-PRD Synchronization Gaps

| Gap | PRDs | Issue |
|-----|------|-------|
| Pub/Sub vs Streams | TSP-04 ↔ TSP-06 | Detection trigger mechanism disagrees |
| Claim timeout config | TSP-02 ↔ TSP-05 | Sub3 needs 90min, TSP-02 doesn't support per-group |
| Advisory locks | TSP-04 ↔ TSP-09 | Replay requires locks Sub2 doesn't implement |
| Trigger bypass | TSP-09 ↔ Migration 003 | Replay mode check not in existing triggers |
| ingestion_log schema | TSP-01 ↔ existing code | New table vs extend existing |
| Hash algorithm | TSP-03 ↔ hash_chain.py | BYTEA concat vs pipe-delimited string |
| K8s vs Compose | All PRDs ↔ actual infra | Every scaling section wrong |

---

## Verification

After execution, verify by:
1. Send a test webhook → confirm it appears in `canary:events` stream (XLEN)
2. Confirm all 3 consumer groups process the entry (XINFO GROUPS)
3. Check `evidence_records` has chain-hashed row with correct prev_hash linkage
4. Check CRDM tables have parsed structured data
5. Trigger a detection rule → confirm alert created with `event_id` linkage
6. Run `make test` — all existing + new tests pass
7. Attempt UPDATE on `evidence_records` → confirm trigger blocks it
