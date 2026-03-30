---
type: workorder
domain: tsp
status: active
created: 2026-03-18
updated: 2026-03-19
---
# WORK ORDER: B-059 — TSP PRD Revision (21 Issues + 7 Sync Gaps)

**Created:** February 27, 2026
**Owner:** ALX
**Assigned to:** Condor (IP Sanitization Intern)
**Supervisor:** PhD (Research Framework)
**Priority:** P0 — Blocks Sprint 6 build. Jeremy ON ICE until Critical items resolved.
**Status:** OPEN
**PRD Location:** `_ALX/WorkOrders/output/Condor/PRD_TripleSubscriberPipeline/`
**Source Feedback:** `_ALX/WorkOrders/output/Condor/TSP_ExecutionPlan_DesignFeedback.md`

---

## Why This Work Order Exists

ALX reviewed all 10 Condor PRDs (TSP-00 through TSP-09) against the actual codebase. Found 21 issues and 7 cross-PRD synchronization gaps. **4 Critical issues will cause build failures or data loss if Jeremy codes against the PRDs as written.** This work order provides exact replacement text for every issue so Condor can execute without ambiguity.

**The rule:** Fix what's written below. Don't rewrite sections that aren't listed. Don't add features. Don't reorganize. Surgical edits only.

---

## Execution: 6 Passes with PhD Checkpoints

Condor executes in 6 sequential passes. Each pass addresses a group of related issues. PhD gates each pass before Condor proceeds to the next.

```
Pass 1: Infrastructure Foundation (C-1, C-4)     ─► PhD Checkpoint 1
Pass 2: Schema & Data Model (C-2, H-5, M-5)      ─► PhD Checkpoint 2
Pass 3: Cross-PRD Messaging (C-3, H-1, H-2)      ─► PhD Checkpoint 3
Pass 4: Implementation Feasibility (H-3/H-4, H-6, M-1 through M-4, M-6) ─► PhD Checkpoint 4
Pass 5: Low Priority (L-1 through L-5)            ─┐
Pass 6: Sync Notes + Revision Logs                 ─► PhD Checkpoint 5 (final gate)
```

---

## PASS 1 — Infrastructure Foundation

### C-1: Replace All Kubernetes References with Docker Compose + Gunicorn

**Severity:** CRITICAL
**Affected PRDs:** TSP-01 through TSP-06 (all have "Kubernetes Readiness" sections)
**Root cause:** Condor assumed K8s. Actual infra is Docker Compose (`devops/docker-compose.alpha3x.yml`) with Gunicorn workers (`--workers ${FLASK_WORKERS:-4}`).

#### Action 1a: Rename and rewrite "Kubernetes Readiness" sections

In each of these 6 PRDs, find the section titled **"Kubernetes Readiness"** and replace it entirely with the template below. Preserve the PRD-specific answers to questions 1 and 5 (those are correct). Rewrite questions 2-4.

**Files:**
- `TSP_01_WebhookReceipt.md` — "Kubernetes Readiness" section
- `TSP_02_QueueFanOut.md` — "Kubernetes Readiness" section
- `TSP_03_Sub1_HashSeal.md` — "Kubernetes Readiness" section
- `TSP_04_Sub2_ParseRoute.md` — "Kubernetes Readiness" section
- `TSP_05_Sub3_MerkleOrdinal.md` — "Kubernetes Readiness" section
- `TSP_06_DetectionEngine.md` — "Kubernetes Readiness" section

**Replace each with this template** (adapt the [PRD-SPECIFIC] placeholders from the original text):

```markdown
## Deployment Readiness (Docker Compose)

1. **Stateless?** [KEEP original answer — it is correct in all PRDs]
2. **Horizontal scaling?** Scaling is via Gunicorn `--workers N` flag in the Flask
   container (`devops/docker-compose.alpha3x.yml`, line ~279). For dedicated worker
   processes (queue consumers), add a new service definition to docker-compose.alpha3x.yml
   inheriting the same build context with a different `command:` entrypoint.
   No orchestrator — manual `docker compose up --scale service=N`.
3. **Rolling deployment?** Not supported in Docker Compose. Blue-green deployment via
   `docker compose up -d` with new image tag. Downtime window: ~5 seconds during
   container replacement.
4. **Scaling trigger?** Manual. Monitor via Prometheus metrics + Grafana dashboards.
   Alert threshold: [KEEP original threshold numbers — they're realistic].
5. **Toy store scaling profile?** [KEEP original answer — it is correct in all PRDs]
```

#### Action 1b: Fix scattered K8s references

Search all 10 PRD files for the following terms and replace:

| Find | Replace With |
|------|-------------|
| `K8s secrets` | `.env.alpha3x environment variables` |
| `Kubernetes secrets` | `.env.alpha3x environment variables` |
| `K8s secret` | `.env.alpha3x` |
| `Kubernetes Secret` | `.env.alpha3x` |
| `Injected via environment / K8s secrets` | `Injected via .env.alpha3x, referenced in docker-compose.alpha3x.yml environment block` |
| `K8s readiness probe fails` | `Gunicorn health check fails` |
| `K8s removes from rotation` | `Docker health check marks container unhealthy` |
| `sidecar or standalone pod` | `background thread or standalone Docker service` |
| `Scale consumer pods` | `Increase FLASK_WORKERS or add a dedicated worker container in docker-compose` |
| `scale Sub 2 pods` | `Increase FLASK_WORKERS or add a dedicated worker container` |
| Any remaining `pod` (in K8s context) | `container` or `service` (use judgment) |
| Any remaining `HPA` | Remove or replace with "manual scaling via docker compose" |
| Any remaining `node affinity` | Remove entirely |

**Known locations of scattered refs** (non-exhaustive — grep for "K8s", "Kubernetes", "pod", "HPA"):
- TSP-01 line ~281, ~385, ~453, ~483, ~516
- TSP-02 line ~191, ~208, ~266, ~338
- TSP-05 line ~491
- TSP-07 line ~347, ~459

---

### C-4: Add Valkey Configuration Prerequisite to TSP-02

**Severity:** CRITICAL
**Affected PRD:** `TSP_02_QueueFanOut.md`
**Root cause:** Current `devops/valkey/valkey.conf` is cache-only. LRU eviction will silently drop stream entries. AOF disabled = data loss on restart.

#### Action: Add new section to TSP-02

Insert the following section in `TSP_02_QueueFanOut.md` immediately **after** the "Consumer Group Configuration" section and **before** the "Claim Monitor" section:

```markdown
## Valkey Configuration Prerequisite

**CRITICAL: The existing Valkey config (`devops/valkey/valkey.conf`) is cache-only and
INCOMPATIBLE with Streams.** The following changes MUST be applied before any TSP component
can use Valkey Streams.

**Current config (WILL CAUSE DATA LOSS):**

| Setting | Current Value | Problem |
|---------|--------------|---------|
| `maxmemory` | `256mb` | Too small for Streams + cache coexistence |
| `maxmemory-policy` | `allkeys-lru` | LRU eviction will silently DELETE stream entries under memory pressure |
| `appendonly` | `no` | Stream data lost on restart — unprocessed webhook events vanish |
| `databases` | `4` | All four assigned to cache (session, chirp, rate limit, dedup) — no room for Streams |

**Required config changes (Sprint 6 prerequisite):**

```conf
# --- MEMORY ---
maxmemory 512mb
# volatile-lru: only evict keys WITH a TTL. Streams have no TTL, so they survive.
# Cache keys (session, chirp, dedup) all have TTLs and will be evicted normally.
maxmemory-policy volatile-lru

# --- PERSISTENCE ---
# Streams MUST survive restarts — they contain unprocessed webhook events.
appendonly yes
appendfsync everysec

# --- STREAM TUNING ---
stream-node-max-bytes 4096
stream-node-max-entries 100

# --- DATABASES ---
databases 5
```

**Database allocation:**

| DB | Purpose | Eviction Behavior |
|----|---------|-------------------|
| 0 | Flask session cache | volatile-lru (TTL keys) |
| 1 | Chirp rule result cache (ThresholdManager) | volatile-lru (TTL 300s) |
| 2 | Rate limiting counters | volatile-lru (TTL keys) |
| 3 | Square webhook dedup cache | volatile-lru (TTL 86400s) |
| 4 | **Streams** (`canary:events`, `canary:detection`) | **NO eviction** (no TTL set on streams) |

**Owner:** Jeremy (config file update) + Tom (DB allocation review).
**Gate:** Config changes must be deployed and verified BEFORE TSP-01 starts publishing.
**Verification:** `XADD canary:events * test test` → `XLEN canary:events` → returns 1.
Restart Valkey → `XLEN canary:events` still returns 1 (AOF recovery).
```

Also add to TSP-01 and TSP-03 Integration Checklists:
```markdown
- [ ] Valkey config updated per TSP-02 "Valkey Configuration Prerequisite" (volatile-lru, AOF, DB 4)
```

---

### PhD Checkpoint 1

**Verify:**
1. `grep -ri "kubernetes\|k8s\|pod\|HPA\|node affinity" TSP_*.md` returns ZERO results (excluding this changelog note)
2. All 6 "Deployment Readiness" sections reference Docker Compose, Gunicorn, .env.alpha3x
3. TSP-02 has "Valkey Configuration Prerequisite" section with correct config values
4. TSP-01 and TSP-03 Integration Checklists reference the Valkey prereq

**Block if fail:** YES — all other passes depend on infrastructure truth.

---

## PASS 2 — Schema & Data Model

### C-2: Rewrite TSP-01 ingestion_log as Migration Extension

**Severity:** CRITICAL
**Affected PRD:** `TSP_01_WebhookReceipt.md` — "Data Model" section, "Ingestion Log Table" subsection
**Root cause:** PRD proposes new table (`BIGSERIAL` PK, `canary_app` schema). Table already exists as `IngestionLog` in `canary/models/sales/ingestion.py` with UUID PK in `canary_sales` schema.

#### Action: Replace the "Ingestion Log Table" subsection

Find the subsection in TSP-01 that defines the `ingestion_log` DDL (CREATE TABLE with BIGSERIAL) and replace it entirely with:

```markdown
### Ingestion Log Table (EXISTING — Sprint 6 Migration Extension)

**Database:** `canary_sales` (NOT canary_app — matches existing model)
**Table:** `ingestion_log`
**Existing model:** `IngestionLog` in `canary/models/sales/ingestion.py`
**Base class:** `SalesBase` (from `canary/models/base.py`)

**Existing columns (DO NOT MODIFY):**

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID PK (via `generate_uuid`) | NOT BIGSERIAL — existing model uses UUID |
| `merchant_id` | TEXT NOT NULL, indexed | Tenant identifier |
| `source` | TEXT NOT NULL, indexed | `WEBHOOK\|POLLING\|BATCH` |
| `event_id` | TEXT NOT NULL | Square event_id or batch reference |
| `event_type` | TEXT NOT NULL | `PAYMENT\|REFUND\|CUSTOMER\|CATALOG\|INVENTORY\|etc.` |
| `received_at` | TIMESTAMPTZ NOT NULL, indexed | Ingestion receipt timestamp |
| `processed_at` | TIMESTAMPTZ nullable | Processing completion timestamp |
| `status` | TEXT NOT NULL, default `received` | `received\|processing\|complete\|failed` |
| `error_message` | TEXT nullable | Error details if status=failed |

**New columns (Sprint 6 Alembic migration):**

```sql
-- File: canary/migrations/sales/versions/XXX_extend_ingestion_log_for_tsp.py
ALTER TABLE canary_sales.ingestion_log ADD COLUMN IF NOT EXISTS source_event_id TEXT;
ALTER TABLE canary_sales.ingestion_log ADD COLUMN IF NOT EXISTS event_hash BYTEA;
ALTER TABLE canary_sales.ingestion_log ADD COLUMN IF NOT EXISTS ip_address INET;
ALTER TABLE canary_sales.ingestion_log ADD COLUMN IF NOT EXISTS user_agent TEXT;

-- Idempotency constraint: prevent duplicate events from same source
ALTER TABLE canary_sales.ingestion_log
  ADD CONSTRAINT IF NOT EXISTS uq_ingestion_source_event UNIQUE (source, source_event_id);

-- Hash lookup index
CREATE INDEX IF NOT EXISTS idx_ingestion_event_hash
  ON canary_sales.ingestion_log (event_hash);
```

**SQLAlchemy model additions** (add to `canary/models/sales/ingestion.py`):

```python
source_event_id: Mapped[Optional[str]] = mapped_column(
    nullable=True, doc="Event ID from source network (e.g., Square webhook event_id)"
)
event_hash: Mapped[Optional[bytes]] = mapped_column(
    LargeBinary, nullable=True, doc="SHA-256 of raw payload bytes"
)
ip_address: Mapped[Optional[str]] = mapped_column(
    nullable=True, doc="Source IP address for audit trail"
)
user_agent: Mapped[Optional[str]] = mapped_column(
    nullable=True, doc="Source user-agent header"
)
```

**NOT a new table. NOT in canary_app. This is a migration extension of existing canary_sales table.**
```

Also update the Processing Sequence in TSP-01. Find the step that says "Write ingestion_log record" and change it to:
```
Write ingestion_log record to canary_sales (status='accepted') — extends existing IngestionLog model.
SQLAlchemy bind: SalesBase (canary_sales).
```

---

### H-5: Flag TSP-03 Chain Hash as NEW Algorithm

**Severity:** HIGH
**Affected PRD:** `TSP_03_Sub1_HashSeal.md` — chain hash computation section (section 5.2 or equivalent)
**Root cause:** PRD doesn't acknowledge that this is a new algorithm. Existing `hash_chain.py` uses pipe-delimited strings. TSP-03 uses BYTEA concatenation.

#### Action: Add callout box at the beginning of the chain hash section

Insert immediately before the chain hash computation description:

```markdown
### Chain Hash Algorithm — NEW (Not a Modification of Existing)

> **IMPORTANT:** The chain hash algorithm below is NEW and distinct from the existing
> `canary/services/hash_chain.py` implementation. Both coexist.

**Existing algorithm** (`hash_chain.py` — used by `audit_log`, `fox_evidence`):
- Input: `json.dumps(record_data, sort_keys=True) + "|" + (previous_hash or "GENESIS")`
- Concatenation: pipe-delimited string (`|`)
- Output: hex string (64 chars)
- Functions: `compute_entry_hash()`, `compute_evidence_chain_hash()`

**TSP-03 algorithm** (NEW — used by `evidence_records` chain):
- Input: raw BYTEA concatenation of `event_hash + previous_chain_hash`
- Concatenation: binary (no delimiter)
- Output: BYTEA (32 bytes raw, stored as binary in PostgreSQL)

**Why different:** The evidence chain operates on BYTEA hashes (raw SHA-256 digests stored
as binary in PostgreSQL), not string-serialized JSON records. Binary concatenation avoids
encoding ambiguity and is more compact.

**Implementation:** Create `compute_evidence_chain_hash_bytea()` in a new module
`canary/services/evidence_chain.py`. Do NOT modify `compute_entry_hash()` or
`compute_evidence_chain_hash()` in `hash_chain.py` — those serve existing tables.
```

---

### M-5: Add SQLAlchemy Bind Routing to Multi-Schema PRDs

**Severity:** MEDIUM
**Affected PRDs:** TSP-03, TSP-04, TSP-06

#### Action: Add bind routing note to each PRD's Data Model section

Add this subsection to the Data Model section of TSP-03, TSP-04, and TSP-06:

```markdown
### SQLAlchemy Bind Routing

This component writes to PostgreSQL databases routed by Flask-SQLAlchemy multi-bind
configuration. The three databases are configured in `docker-compose.alpha3x.yml`:

| Env Var | Database | SQLAlchemy Base |
|---------|----------|-----------------|
| `DATABASE_URL` | `canary_app` | `AppBase` (default) |
| `DATABASE_URL_SALES` | `canary_sales` | `SalesBase` |
| `DATABASE_URL_METRICS` | `canary_metrics` | `MetricsBase` |

Models declare their bind via their base class (defined in `canary/models/base.py`):
- `AppBase` models → `canary_app` (alerts, detection rules, replay logs)
- `SalesBase` models → `canary_sales` (transactions, ingestion log, evidence records)
- `MetricsBase` models → `canary_metrics` (aggregation tables)
```

Then in each PRD, annotate each table's DDL with the correct bind:
- **TSP-03:** `evidence_records` → `SalesBase` / `canary_sales`
- **TSP-04:** All CRDM tables (transactions, refund_links, etc.) → `SalesBase` / `canary_sales`
- **TSP-06:** `alerts`, `detection_rules`, `merchant_rule_config` → `AppBase` / `canary_app`

---

### PhD Checkpoint 2

**Verify:**
1. TSP-01 ingestion_log DDL uses UUID PK (not BIGSERIAL), `canary_sales` schema (not `canary_app`)
2. TSP-01 new columns match existing model structure (Optional, correct types)
3. TSP-03 has "NEW algorithm" callout distinguishing BYTEA from pipe-delimited
4. TSP-03, TSP-04, TSP-06 all have bind routing sections with correct base class assignments
5. No references to "canary_app" for tables that belong in "canary_sales" (or vice versa)

**Block if fail:** YES — schema errors cascade to all downstream consumers.

---

## PASS 3 — Cross-PRD Messaging Sync

### C-3: Fix TSP-04 Detection Notification (Pub/Sub to Streams)

**Severity:** CRITICAL
**Affected PRD:** `TSP_04_Sub2_ParseRoute.md`
**Root cause:** TSP-04 uses `PUBLISH canary:detection` (pub/sub). TSP-06 correctly uses Streams. Pub/sub is fire-and-forget — if detection engine is down, messages are lost.

#### Action 3a: Replace detection notification subsection

Find the "Detection Notification" subsection in TSP-04 (around the "After successful structured INSERT" description) and replace with:

```markdown
### Detection Notification

After successful structured INSERT, Sub 2 publishes a notification to Valkey Stream
`canary:detection` via XADD (NOT pub/sub — Streams provide durability and backpressure,
consistent with TSP-06 v1.1 architecture):

```
XADD canary:detection * \
  event_id       "evt_01HXYZ789ABC" \
  merchant_id    "offset-coffee-001" \
  event_type     "payment.created" \
  tables_written "transactions,transaction_tenders" \
  row_ids        '{"transactions": "txn_abc123", "transaction_tenders": ["tt_xyz456"]}' \
  parse_failed   "false" \
  parsed_at      "2026-02-26T14:23:01.020Z"
```

TSP-06 (Detection Engine) reads from consumer group `detection-engine` on this stream.

**Cross-PRD Sync:** Synced with TSP-06 v1.1 — uses XADD to `canary:detection` Stream
(not pub/sub). See TSP-06 "Architecture Position" for rationale.
```

#### Action 3b: Fix all remaining pub/sub references in TSP-04

Search TSP-04 for these terms and replace:
- `pub/sub channel` → `Valkey Stream`
- `PUBLISH canary:detection` → `XADD canary:detection *`
- In any sequence diagram: change `canary:detection (pub/sub)` to `canary:detection (Stream)`

---

### H-1: Add Per-Group Claim Timeouts to TSP-02

**Severity:** HIGH
**Affected PRD:** `TSP_02_QueueFanOut.md` — Claim Monitor section

#### Action: Add per-group timeout table to Claim Monitor section

Find the Claim Monitor section in TSP-02. Add this subsection immediately after the description of the XCLAIM mechanism:

```markdown
### Per-Group Claim Timeout Configuration

Each consumer group has different processing characteristics. The Claim Monitor MUST
use per-group timeouts, not a single global timeout:

| Consumer Group | Claim Timeout | Rationale |
|---------------|--------------|-----------|
| `sub1-seal` | 300s (5 min) | Simple hash + INSERT. Should complete in <1s. 5 min is generous. |
| `sub2-parse` | 300s (5 min) | Parse + multi-table INSERT. Should complete in <1s. 5 min is generous. |
| `sub3-merkle` | 7200s (120 min) | Batch accumulation window is ~90 min per TSP-05. Claim timeout MUST exceed batch window or the Claim Monitor will reclaim in-progress batches. |

**Environment variables:**

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `CLAIM_TIMEOUT_SUB1_SEAL` | int (seconds) | 300 | Reclaim threshold for sub1-seal |
| `CLAIM_TIMEOUT_SUB2_PARSE` | int (seconds) | 300 | Reclaim threshold for sub2-parse |
| `CLAIM_TIMEOUT_SUB3_MERKLE` | int (seconds) | 7200 | Reclaim threshold for sub3-merkle |

**Implementation:**

```python
GROUP_TIMEOUTS = {
    "sub1-seal": int(os.getenv("CLAIM_TIMEOUT_SUB1_SEAL", "300")),
    "sub2-parse": int(os.getenv("CLAIM_TIMEOUT_SUB2_PARSE", "300")),
    "sub3-merkle": int(os.getenv("CLAIM_TIMEOUT_SUB3_MERKLE", "7200")),
}

for group, timeout_s in GROUP_TIMEOUTS.items():
    pending = XPENDING canary:events {group} - + COUNT 100
    for msg in pending where idle_time_ms > timeout_s * 1000:
        XCLAIM canary:events {group} worker-recovery {msg.id} {timeout_s * 1000}
```

**Cross-PRD Sync:** Synced with TSP-05 v1.1 — sub3-merkle requires extended claim timeout
to accommodate 90-minute batch accumulation window.
```

---

### H-2: Add Advisory Lock Coordination to TSP-04

**Severity:** HIGH
**Affected PRD:** `TSP_04_Sub2_ParseRoute.md` — after Processing Sequence

#### Action: Add advisory lock section

Insert this new subsection after the Processing Sequence in TSP-04:

```markdown
### Advisory Lock Coordination (TSP-09 Replay Contract)

Before writing structured records for a merchant, Sub 2 MUST acquire a PostgreSQL
advisory lock to prevent concurrent writes during replay operations:

```python
# Before INSERT batch for merchant_id:
lock_id = hashtext('replay:' + merchant_id)
SELECT pg_advisory_lock(%(lock_id)s)

# ... INSERT structured records (transactions, line items, tenders, etc.) ...

# Advisory lock released automatically when connection returns to pool
# (or explicitly via pg_advisory_unlock)
```

**Why:** TSP-09 (Replay & Rebuild) acquires the same lock during replay. This provides
mutual exclusion: if a replay is running for merchant A, live Sub 2 blocks on the lock
for merchant A. Other merchants continue processing normally (the lock is merchant-scoped).

**Performance:** `pg_advisory_lock` is session-level, held per-connection. Lock contention
only occurs during replay (rare operation). Normal processing has zero lock contention
because only one Sub 2 worker processes a given merchant at a time.

**Alternative:** Use `pg_try_advisory_lock()` with retry/backoff if non-blocking is
preferred. Return message to pending list if lock not acquired.

**Cross-PRD Sync:** Synced with TSP-09 v1.1 — replay worker acquires
`pg_advisory_lock(hashtext('replay:' || merchant_id))` and expects Sub 2 to honor the same lock.
```

Also add to TSP-04 Integration Checklist:
```markdown
- [ ] Sub 2 acquires advisory lock before structured writes (TSP-09 replay contract)
- [ ] Lock tested under concurrent replay scenario
```

---

### PhD Checkpoint 3

**Verify:**
1. `grep -i "pub/sub\|PUBLISH canary" TSP_04_*.md` returns ZERO results
2. TSP-04 detection notification uses `XADD canary:detection *` with `row_ids` field
3. TSP-02 has per-group claim timeout table with `sub3-merkle` at 7200s
4. TSP-04 has advisory lock section referencing `pg_advisory_lock(hashtext('replay:' || merchant_id))`
5. Cross-read TSP-02 ↔ TSP-05 on claim timeout — numbers consistent
6. Cross-read TSP-04 ↔ TSP-09 on advisory lock — lock ID formula identical

**Block if fail:** YES — messaging desyncs are build-blockers.

---

## PASS 4 — Implementation Feasibility

### H-3 + H-4: Replace WebSocket with SSE in TSP-06

**Severity:** HIGH
**Affected PRD:** `TSP_06_DetectionEngine.md` — real-time push section
**Root cause:** Flask 3.0 + Gunicorn sync workers don't support WebSocket. Port 3000 conflicts with dev servers.

#### Action: Replace WebSocket section with SSE + future WebSocket plan

Find the WebSocket Push section in TSP-06 and replace entirely with:

```markdown
### Real-Time Alert Push (Merchant Dashboard)

**Phase 1 — Server-Sent Events (SSE) via existing Flask/Gunicorn stack:**

```
GET /api/alerts/stream/{merchant_id}
Accept: text/event-stream
Authorization: Bearer {jwt_token}
```

Response (streaming):
```
event: new_alert
data: {"id": "uuid", "rule_id": "C-102", "alert_type": "CASH_VARIANCE",
       "severity": "HIGH", "merchant_id": "offset-coffee-001",
       "created_at": "2026-02-26T14:23:01.100Z"}

event: new_alert
data: {"id": "uuid", "rule_id": "C-005", ...}
```

**Why SSE for Phase 1:**
1. Flask 3.0 + Gunicorn (sync workers) does not natively support WebSocket
2. SSE works over standard HTTP — no Nginx upgrade configuration, no new Docker service
3. Path-based routing through existing Flask blueprint on port 5001 (same as API)
4. No port conflict (no port 3000 needed)

**Reconnection:** On SSE disconnect, client reconnects with `Last-Event-ID` header.
Server replays missed alerts from in-memory ring buffer (last 50 per merchant).

**Phase 2 — WebSocket upgrade (if SSE latency or fan-out is insufficient):**

Upgrade to WebSocket via `flask-sock` + Gunicorn with `gevent` worker class:
```yaml
# docker-compose.alpha3x.yml change:
command: gunicorn wsgi_alpha3x:app --bind 0.0.0.0:5001 --worker-class gevent --workers 4
```
Requires adding `flask-sock` + `gevent` to `requirements.txt`. WebSocket upgrade happens
on the same port 5001 via path `/ws/alerts/{merchant_id}`. No new port.
```

---

### H-6: Add Spend Gate Sections to TSP-05 and TSP-07

**Severity:** HIGH
**Affected PRDs:** `TSP_05_Sub3_MerkleOrdinal.md`, `TSP_07_L402_ValidationAPI.md`

#### Action: Add this section to both PRDs (near the Configuration section)

```markdown
## Prerequisites — Spend Gate (Requires Jeffe Approval)

Per GrowDirect Principle 9 ("Cloud APIs require explicit spend cap approval.
No unmetered API connections. Ever."), the following external services are NOT YET
APPROVED and MUST NOT be wired without a B-ticket and Jeffe sign-off:

| Service | PRD | Monthly Cost Est. | Sprint | Approval Status |
|---------|-----|-------------------|--------|-----------------|
| OrdinalsBot API | TSP-05 | TBD (per-inscription fee) | 7+ | NOT APPROVED |
| Bitcoin Core Node | TSP-05 | $0 (self-hosted) / $30-100/mo (hosted) | 7+ | NOT APPROVED |
| Strike API | TSP-07 | Free tier (test), TBD (prod) | 7+ | NOT APPROVED |

**Sprint 6 scope (no live API keys required):**
- TSP-05: Merkle tree construction + batch accumulator logic. Mock OrdinalsBot responses
  (simulated inscription_id). No real Bitcoin transactions.
- TSP-07: L402 validation logic + payment hash verification. Strike test environment (free).
  Test invoices only.

**Sprint 7+ gate:** Real API keys require a B-ticket with spend cap and Jeffe sign-off
before ANY live API calls are wired.
```

---

### M-1: Add Webhook Endpoint Migration Note to TSP-01

**Severity:** MEDIUM
**Affected PRD:** `TSP_01_WebhookReceipt.md` — API Contract section

#### Action: Add migration note after the endpoint definition

After the `POST /webhooks/{source}` endpoint definition, add:

```markdown
### Existing Code Migration Note

**Current endpoint:** `POST /webhooks/square` (hardcoded route in `canary/blueprints/webhooks.py`)
**Target endpoint:** `POST /webhooks/{source}` (parameterized per TSP-01)

**Migration path:** The existing blueprint is a scaffold with TODO stubs (no HMAC verification,
stub response only). TSP-01 replaces it entirely:
1. Rename existing `canary/blueprints/webhooks.py` → `webhooks_legacy.py` (reference only)
2. Create new `canary/blueprints/webhooks.py` implementing TSP-01 spec with `{source}` param
3. Update Flask blueprint registration in app factory
4. Phase 1: Only `square` source returns 200; all others return 404 with
   `{"error": "unsupported_source", "message": "Source not registered"}`

The existing `WebhookRouter` class (`canary/services/webhook_router.py`) is the synchronous
predecessor that TSP replaces. Its event-type routing map (payment, refund, order, inventory,
cash_drawer, timecard, gift_card) is reusable as reference for Sub 2 parser dispatch. The
class itself is NOT reused — TSP-01 publishes to Valkey Streams, not direct DB writes.
```

---

### M-2: Add Rule Source Reconciliation to TSP-06

**Severity:** MEDIUM
**Affected PRD:** `TSP_06_DetectionEngine.md` — Data Model section

#### Action: Add reconciliation note

Add this subsection to TSP-06 Data Model:

```markdown
### Rule Source Reconciliation

**Current state:** 26 Chirp rules defined as frozen dataclasses in
`canary/services/chirp/rule_definitions.py` (`RULE_CATALOG` list + `RULE_MAP` dict).
`ThresholdManager` reads from `RULE_MAP` for default threshold lookup.

**PRD assumption:** Rules stored in `detection_rules` DB table (`canary_app`).

**Resolution — dual-source with DB seed:**

**Phase 1 (Sprint 6):** `RULE_CATALOG` remains the source of truth for rule definitions.
On app startup, seed the `detection_rules` DB table FROM `RULE_CATALOG` (idempotent upsert
by `rule_id`). `ThresholdManager` continues using `RULE_MAP` for defaults. The DB table
enables the Chirp Config UI to query rules via API without importing Python code.

**Phase 2 (post-Sprint 6):** If per-tenant rule customization beyond threshold tuning is
needed (custom rule definitions, not just enable/disable), migrate rule authoring to the
DB table and deprecate `RULE_CATALOG`.

**No code change to `rule_definitions.py` in Sprint 6. Startup seed script only.**
```

---

### M-3: Add ThresholdManager Wiring Note to TSP-06

**Severity:** MEDIUM
**Affected PRD:** `TSP_06_DetectionEngine.md`

#### Action: Add wiring note near the detection engine initialization section

```markdown
### ThresholdManager Valkey Wiring

**Current state:** `ThresholdManager.__init__()` in `canary/services/chirp/threshold_manager.py`
accepts `valkey_client=None`. When None, all threshold lookups bypass cache and query
PostgreSQL directly. This works but adds latency to every detection evaluation.

**Sprint 6 requirement:** Wire `valkey_client` during detection engine initialization:

```python
import redis
valkey = redis.Redis.from_url(app.config["VALKEY_URL"], db=1)  # DB 1 = Chirp rule cache
threshold_mgr = ThresholdManager(db_session=session, valkey_client=valkey)
```

**Integration Checklist addition:**
- [ ] ThresholdManager instantiated with live Valkey client (DB 1) in detection engine startup
- [ ] Cache hit/miss logging verified in detection engine test run
```

---

### M-4: Flag Labor Events as Poll-Only in TSP-04

**Severity:** MEDIUM
**Affected PRD:** `TSP_04_Sub2_ParseRoute.md` — event type table

#### Action: Update labor.shift.* rows in the event type mapping table

Find the three `labor.shift.*` rows in TSP-04's event type table and update the Notes column:

```markdown
| `labor.shift.created` | `employee_timecards` | Phase 2 | Mutable | **NOT a webhook event.** Square Labor API is poll-only (B-047). Requires polling adapter (Airflow DAG) to fetch shift data and inject into pipeline as synthetic events. Deferred to Phase 2+ with polling infrastructure. |
| `labor.shift.updated` | `employee_timecards` (upsert) | Phase 2 | Mutable | **Poll-only — see labor.shift.created note.** |
| `labor.shift.closed` | `employee_timecards` (upsert) | Phase 2 | Mutable | **Poll-only — see labor.shift.created note.** |
```

Also add to the Phase 1 Scope section:
```markdown
**Deferred:** Labor API events require polling adapter (Airflow DAG) — not available via
webhook per Jeremy SDK audit (B-047). Affects Chirp rules C-301, C-302, C-303.
```

---

### M-6: Add Alembic Migration Detail to TSP-09 Trigger Bypass

**Severity:** MEDIUM
**Affected PRD:** `TSP_09_ReplayRebuild.md` — trigger bypass / migration prerequisite section

#### Action: Add explicit migration file reference

The existing text about `SET LOCAL canary.replay_mode = 'true'` is correct. Add specifics:

```markdown
**Migration file:** `canary/migrations/sales/versions/XXX_add_replay_bypass_to_prevent_mutation.py`

**Alembic revision dependency:** Chains after Sprint 5 migration 003
(`003_add_immutability_triggers_financial_tables.py`) which created the `prevent_mutation()`
triggers on 6 tables.

**What the migration does:** Alters the `prevent_mutation()` function to check
`current_setting('canary.replay_mode', true)` before raising the exception. If
`canary.replay_mode = 'true'` is set via `SET LOCAL`, mutations are allowed within
that transaction only.

**Applies to:** All tables with `prevent_mutation()` trigger (6 canary_sales tables).

**Verification tests:**
1. Normal `DELETE FROM transactions WHERE ...` → STILL blocked (no replay_mode set)
2. `BEGIN; SET LOCAL canary.replay_mode = 'true'; DELETE FROM transactions WHERE ...; COMMIT;` → succeeds
3. After the transaction, `DELETE` is blocked again (SET LOCAL doesn't leak)
4. Other connections cannot see or use the replay_mode flag from another transaction
```

---

### PhD Checkpoint 4

**Verify:**
1. TSP-06 has SSE for Phase 1, WebSocket (gevent) for Phase 2. No port 3000 reference.
2. TSP-05 and TSP-07 have spend gate sections with "NOT APPROVED" status
3. TSP-01 has webhook endpoint migration note referencing existing scaffold
4. TSP-06 has rule source reconciliation and ThresholdManager wiring notes
5. TSP-04 labor.shift.* rows flagged as poll-only with B-047 reference
6. TSP-09 has Alembic migration detail for trigger bypass

**Block if fail:** NO — these can be iterated during build. But fix before Jeremy starts.

---

## PASS 4b — Grok Review Additions (3 Items)

*Source: External review of the execution plan by Grok (Feb 27). Jeffe approved all three additions.*

### G-1: Week 1 Validation Smoke Tests Per Track

**Root cause:** The Verification section at the end of the execution plan is post-build. There's
no "did this work on Day 3?" early validation. If a consumer is misconfigured, you don't find
out until Week 3.

#### Action: Add a "Week 1 Smoke Test" section to TSP-01, TSP-03, TSP-04, TSP-05

Add this section near the end of each affected PRD (before the Integration Checklist):

**TSP-01 (Webhook Receipt):**
```markdown
### Week 1 Validation Smoke Test

Before proceeding to Week 2, manually verify:
1. `curl -X POST /webhooks/square -H "Content-Type: application/json" -d '{"test": true}'`
   → Returns 401 (HMAC validation rejects unsigned request)
2. Send properly signed test payload → Returns 200 with `event_id`
3. `XLEN canary:events` → Returns 1 (message is in the stream)
4. Check `ingestion_log` table → Row exists with status='accepted', event_hash populated

If any step fails, STOP. Debug before proceeding. Do not build consumers against a
broken publisher.
```

**TSP-03 (Sub 1 — Hash Seal):**
```markdown
### Week 1 Validation Smoke Test

Before proceeding to Week 2, manually verify:
1. Manually `XADD canary:events * event_id test_001 merchant_id test_merchant ...`
2. Check consumer log → sub1-seal picked up the message
3. `SELECT * FROM evidence_records WHERE event_id = 'test_001'` → Row exists
4. Verify `chain_hash` is populated (not NULL)
5. `XACK canary:events sub1-seal <message_id>` → Confirmed acknowledged

If evidence_records row is missing or chain_hash is NULL, the consumer is broken.
```

**TSP-04 (Sub 2 — Parse/Route):**
```markdown
### Week 1 Validation Smoke Test

Before proceeding to Week 2, manually verify:
1. Manually `XADD canary:events * event_id test_002 event_type payment.created ...`
   (with a valid Square-like payment payload in the raw_payload field)
2. Check consumer log → sub2-parse picked up the message
3. `SELECT * FROM transactions WHERE source_event_id = 'test_002'` → Row exists
4. `XLEN canary:detection` → Returns 1 (detection notification was published)
5. `XACK canary:events sub2-parse <message_id>` → Confirmed acknowledged

If CRDM table is empty or canary:detection has no entry, parser dispatch is broken.
```

**TSP-05 (Sub 3 — Merkle Accumulator):**
```markdown
### Week 1 Validation Smoke Test (Sprint 6 scope: logic only, no Bitcoin)

Before proceeding to Week 2, manually verify:
1. Manually `XADD canary:events * event_id test_003 merchant_id test_merchant ...`
2. Check consumer log → sub3-merkle picked up the message
3. Verify message is held in batch accumulator (not immediately ACKed)
4. After batch window expires (or manually trigger flush):
   - Merkle tree root hash is computed and logged
   - All batch messages are XACKed
5. Verify deterministic ordering: re-run same events → same Merkle root

If Merkle root is non-deterministic or messages ACK before batch completes,
the accumulator logic is broken.
```

---

### G-2: Track D (Merkle) Risk Callout

**Root cause:** Track D (TSP-05 Merkle tree construction) is the riskiest pure-new-code piece
in Sprint 6. Unlike Tracks A/B/C which heavily reuse existing parsers, routers, and rules,
Track D is entirely novel logic with no existing code to lean on.

#### Action: Add risk callout to TSP-05

Add this section to TSP-05, immediately after the "Purpose" section:

```markdown
### Risk Assessment — Sprint 6 Highest-Risk Track

**This is the riskiest new-code track in Sprint 6.** Unlike Sub 1 (reuses trigger patterns)
and Sub 2 (reuses existing parsers + routing), the Merkle accumulator has:

- No existing code to build on — 100% new logic
- Novel batch accumulation pattern (90-min window, deterministic ordering)
- Correctness requirement: same inputs MUST produce identical Merkle root (deterministic)
- Edge cases: partial batches, consumer restart mid-batch, out-of-order delivery

**Mitigations:**
1. **Extra code review attention:** Track D PRs get 2 reviewers minimum (Jeremy + Tom)
2. **Property-based testing:** Use Hypothesis or similar to fuzz the Merkle tree builder
   with random event orderings → assert deterministic root
3. **Sprint 6 scope is deliberately limited:** Tree logic + tests only. No Bitcoin integration.
   This isolates the risk from external API dependencies.
4. **Week 1 smoke test** (see above) validates the basic accumulate → flush → compute cycle
   before building batch optimization logic in Week 2.
```

---

### G-3: Consolidated Review Document (Sprint 6 Kickoff Prep)

**Root cause:** Before Jeremy starts coding, the full team needs a single document that
consolidates the 10 PRDs + execution plan + design feedback into a reviewable package.
External review estimates this raises success probability from ~30% to ~60%.

#### Action: Add to TSP-00 Index — Consolidated Review Doc Section

Add this section to TSP-00 (Master Index):

```markdown
## Pre-Build Consolidated Review Document

Before Sprint 6 coding begins, Condor produces a single consolidated review document
structured as follows:

1. **Executive Summary** (1 page) — What TSP is, business value, key deferrals, biggest
   risks, desired outcome of review
2. **Architecture Flow Diagram** — Mermaid diagram showing webhook → HMAC → XADD → fan-out
   → 3 subscribers → detection → future Bitcoin/L402. Color-coded: green (existing reuse),
   blue (new Sprint 6), yellow (deferred Sprint 7+), red (persistent storage)
3. **PRD Inventory Table** — All 10 PRDs: title, status, dependencies, sprint target, notes
4. **Execution Plan** — Dependency graph, Week 0 prerequisites, 4 parallel tracks, reuse matrix
5. **Consolidated Design Feedback** — All issues by priority tier + cross-PRD sync gaps
6. **Riskiest Seams** — Deep-dive on: replay + advisory locks + triggers, Sub 3 90-min claim,
   detection trigger mechanism, Valkey sizing under load, future L402/Bitcoin seams
7. **Week 1 Smoke Tests** — Per-track validation criteria
8. **Decisions Needed** — Explicit yes/no list for Sprint 6 kickoff meeting

**Output file:** `_ALX/WorkOrders/output/Condor/TSP_ConsolidatedReview_v1.0.md`
**Timing:** Delivered AFTER Pass 6 of this work order (revised PRDs must be final first)
**Feeds:** Sprint 6 kickoff meeting. Jeremy reads this before writing any code.
```

---

### PhD Checkpoint 4b (Grok Additions)

**Verify:**
1. TSP-01, TSP-03, TSP-04, TSP-05 all have "Week 1 Validation Smoke Test" sections
2. Each smoke test has concrete, observable steps (not vague "verify it works")
3. TSP-05 has "Risk Assessment" section calling out Track D as highest-risk
4. TSP-00 has "Pre-Build Consolidated Review Document" section with 8-point structure
5. Consolidated doc output path is specified

**Block if fail:** NO — but strongly recommended before Jeremy starts.

---

## PASS 5 — Low Priority

Add brief placeholder notes to the relevant PRDs. These do not block the build.

**L-1** — Add to TSP-05 and TSP-07:
```markdown
**Business Model Integration:** See `ElJeffe_BusinessModel_Addendum.md` for Genesis Pool
economics, Layer pricing, and pool allocation logic. Concrete integration deferred to Sprint 7+.
```

**L-2** — Add to TSP-00 Index:
```markdown
**Monitoring & Alerting:** Prometheus metrics + Grafana dashboards for consumer lag, stream
memory usage, hash chain gap detection. Specification deferred — Jeremy defines during
implementation. Ops appendix to follow.
```

**L-3** — Add to TSP-02 (after consumer group configuration):
```markdown
**Consumer Group Naming Convention:** `sub{N}-{function}` for the three pipeline subscribers
(sub1-seal, sub2-parse, sub3-merkle). Additional consumer groups use descriptive names
(e.g., `detection-engine` for TSP-06). All groups documented in this section.
```

**L-4** — Add to TSP-00 Index:
```markdown
**Integration Test Strategy:** End-to-end test covering webhook receipt → stream → 3 consumers
→ detection → alert. Specification deferred to Jim (QA). Test plan required before Sprint 6
QA gate.
```

**L-5** — Add to TSP-05 and TSP-09:
```markdown
**IP Classification:** The Merkle batch accumulator algorithm (TSP-05) and replay cursor
mechanism (TSP-09) are Crown Jewels per Condor registry. External documentation describes
behavior, not implementation. Patent provisional covers both (Application #63/991,596).
```

---

## PASS 6 — Cross-PRD Sync Notes + Revision Logs

### Action 6a: Add Cross-PRD Sync notes

For each of the 7 sync gaps, add a "Cross-PRD Sync" note to BOTH sides of the gap:

| Gap | PRD A (add note) | PRD B (add note) | Note Text |
|-----|------------------|------------------|-----------|
| 1. Pub/Sub → Streams | TSP-04 (fixed in C-3) | TSP-06 | "Synced: detection notification uses XADD to canary:detection Stream (not pub/sub)" |
| 2. Claim timeout | TSP-02 (fixed in H-1) | TSP-05 | "Synced: sub3-merkle claim timeout = 7200s to accommodate 90-min batch window" |
| 3. Advisory locks | TSP-04 (fixed in H-2) | TSP-09 | "Synced: Sub 2 acquires pg_advisory_lock(hashtext('replay:' || merchant_id)) before writes" |
| 4. Trigger bypass | TSP-09 (fixed in M-6) | Migration 003 ref | "Synced: Alembic migration adds replay_mode check to prevent_mutation()" |
| 5. ingestion_log schema | TSP-01 (fixed in C-2) | Existing code ref | "Synced: ingestion_log is migration extension of existing canary_sales table (UUID PK)" |
| 6. Hash algorithm | TSP-03 (fixed in H-5) | hash_chain.py ref | "Synced: TSP-03 uses NEW BYTEA algorithm in evidence_chain.py; hash_chain.py unchanged" |
| 7. K8s → Compose | All 6 PRDs (fixed in C-1) | docker-compose ref | "Synced: all deployment sections reference Docker Compose + Gunicorn (no K8s)" |

### Action 6b: Update Revision Logs in all 10 PRDs

Bump every PRD from v1.1 to **v1.2**. In each PRD's Revision Log table, add:

```markdown
| 1.2 | Feb [date], 2026 | Condor (B-059 revision under PhD supervision) | [List specific issues fixed in this PRD] |
```

Example for TSP-04:
```markdown
| 1.2 | Feb XX, 2026 | Condor (B-059) | Fixed: C-1 (K8s→Compose), C-3 (pub/sub→Streams), H-2 (advisory locks), M-4 (labor poll-only), M-5 (bind routing). Sync notes added for gaps 1, 3. |
```

---

### PhD Checkpoint 5 (Final Gate)

Run the full 15-point acceptance criteria matrix:

| # | Criterion | Check Method | Pass? |
|---|-----------|-------------|-------|
| AC-1 | Zero occurrences of "Kubernetes", "K8s", "pod", "HPA", "node affinity" | `grep -ri` all 10 files | |
| AC-2 | All "Deployment Readiness" sections reference Docker Compose + Gunicorn | Section review | |
| AC-3 | TSP-01 ingestion_log: UUID PK, canary_sales, migration extension | DDL review | |
| AC-4 | TSP-04: XADD (not PUBLISH), no "pub/sub" remaining | `grep -i "pub/sub\|PUBLISH" TSP_04` | |
| AC-5 | TSP-06: XREADGROUP on canary:detection stream | Section review | |
| AC-6 | TSP-02: Valkey Configuration Prerequisite section exists | Section review | |
| AC-7 | TSP-02: Per-group claim timeout table, sub3-merkle = 7200s | Table review | |
| AC-8 | TSP-04: Advisory lock section matches TSP-09 lock formula | Cross-check formula | |
| AC-9 | TSP-06: SSE (Phase 1) + WebSocket/gevent (Phase 2), no port 3000 | Section review | |
| AC-10 | TSP-03: "NEW algorithm" callout, does not modify hash_chain.py | Section review | |
| AC-11 | TSP-05 + TSP-07: Spend gate sections with "NOT APPROVED" | Section review | |
| AC-12 | All 7 sync gaps have notes on both sides | Cross-read all 10 files | |
| AC-13 | TSP-04: labor.shift.* flagged poll-only with B-047 ref | Table review | |
| AC-14 | TSP-03/04/06: SQLAlchemy bind routing sections | Section review | |
| AC-15 | All 10 PRDs bumped to v1.2 with revision log entries | Revision log check | |

**All 15 must pass.** If any fail, Condor fixes in a micro-pass and PhD re-checks that item only.

**When all 15 pass:** PhD marks B-059 as DELIVERED. ALX updates TRIAGE. Jeremy comes off ice.

---

## Summary: Issue-to-PRD Matrix

| Issue | TSP-00 | TSP-01 | TSP-02 | TSP-03 | TSP-04 | TSP-05 | TSP-06 | TSP-07 | TSP-08 | TSP-09 |
|-------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| C-1 | | X | X | X | X | X | X | | | |
| C-2 | | X | | | | | | | | |
| C-3 | | | | | X | | (ref) | | | |
| C-4 | | (ref) | X | (ref) | | | | | | |
| H-1 | | | X | | | (ref) | | | | |
| H-2 | | | | | X | | | | | (ref) |
| H-3/H-4 | | | | | | | X | | | |
| H-5 | | | | X | | | | | | |
| H-6 | | | | | | X | | X | | |
| M-1 | | X | | | | | | | | |
| M-2 | | | | | | | X | | | |
| M-3 | | | | | | | X | | | |
| M-4 | | | | | X | | | | | |
| M-5 | | | | X | X | | X | | | |
| M-6 | | | | | | | | | | X |
| L-1 | | | | | | X | | X | | |
| L-2 | X | | | | | | | | | |
| L-3 | | | X | | | | | | | |
| L-4 | X | | | | | | | | | |
| L-5 | | | | | | X | | | | X |

**Most-touched PRDs:** TSP-04 (6 issues), TSP-06 (5 issues), TSP-01 (4 issues), TSP-02 (4 issues)
