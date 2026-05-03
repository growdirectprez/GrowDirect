# Canary Protocol — Wave G: L402 · LNURL-auth · Cockroach Principle

**Plan ID:** `2026-05-03-canary-wave-g-l402-lnurl-recovery`
**Parent dispatch:** [GRO-739](https://linear.app/growdirect/issue/GRO-739)
**Patent reference:** Application 63/991,596 — *Universal Event Notarization, Six-Node Architecture*
**Author:** ALX · **Date:** 2026-05-03
**Mode:** state · subagent-driven · worktrees per dispatch

---

## State at wave open

Waves A–F are merged to main (`ebe7a28`). The Six-Node pipeline is structurally complete:

| Node | Dispatch | Status |
|------|----------|--------|
| Node 2 — Gateway | GRO-746 | ✅ merged |
| Node 3 — Sub 1 Hash & Seal | GRO-748 | ✅ merged |
| Node 4 — Sub 2 Parse & Route | GRO-749 | ✅ merged |
| Node 5/6 — Sub 3 Merkle & Ordinal | GRO-750 | ✅ merged |
| `.jeffe` Namespace registration | GRO-751 | ✅ merged |
| MCP route group (28 tools) | GRO-767 | ✅ merged |
| OpenAPI / MCP connector | GRO-740/741 | carried forward |
| Public site | GRO-743 | carried forward |

Migration sequence is at `021_protocol_namespace`. Next migration slot: `022`.

---

## Wave G mission

Close Phase 1. Three code dispatches + one close-out ritual:

1. **GRO-752** — L402 sat-gated Validation API (the revenue proof)
2. **GRO-753** — LNURL-auth (the identity proof)
3. **GRO-754** — Cockroach Principle recovery tests (the antifragility proof)
4. **GRO-745** — Phase 1 ship comment + memory reseed + Brain wiki card

GCP deployment (Phase 1.J) runs in parallel with GRO-752/753 if bandwidth allows; it does not block code dispatch completion.

---

## Dependency graph

```
GRO-751 (namespace) ─────┐
GRO-750 (anchor)  ────────┤
GRO-748 (evidence)────────┤──► GRO-752 L402 Validation
                          │
GRO-751 (raas_uuid) ──────┘

GRO-752 (L402 challenge) ─► GRO-753 LNURL-auth (consume L402 token)

GRO-746 + 748 + 750 + 751 ► GRO-754 Cockroach proofs (exercises full pipeline)

GRO-752 + 753 done ───────► GRO-745 ship comment + wiki
```

**Execution order:** 752 and 753 sequentially (753 depends on 752's L402 token machinery); 754 can start after 750/748 but benefits from 752 being merged. Ship GRO-745 last.

---

## GRO-752 — L402 sat-gated Validation API

**Dispatch:** [GRO-752](https://linear.app/growdirect/issue/GRO-752)
**Phase:** 1.G
**Branch:** `gro-752-l402-validation`
**Worktree:** `.worktrees/gro-752-l402-validation`
**Migration slot:** `022_protocol_validation.up.sql`
**Port:** `:8096` (new `cmd/validator/`)

### What it does

A caller submits an `event_hash` and pays satoshis (via L402 challenge/response) to receive a Merkle proof that the event is anchored on Bitcoin. This is the patent's "evidentiary verification" path and the first real revenue surface.

### Schema — migration 022

```sql
-- ledger.l402_verification_tokens
-- One-time payment token for a single proof retrieval.
CREATE TABLE IF NOT EXISTS ledger.l402_verification_tokens (
    token_id        uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
    event_hash      text        NOT NULL,
    satoshi_price   bigint      NOT NULL DEFAULT 100,
    status          text        NOT NULL DEFAULT 'pending'
                    CHECK (status IN ('pending','paid','consumed','expired')),
    preimage_hash   text,           -- HOLD: populated by Lightning payment
    created_at      timestamptz NOT NULL DEFAULT now(),
    expires_at      timestamptz NOT NULL DEFAULT now() + interval '24 hours',
    consumed_at     timestamptz
);

CREATE INDEX IF NOT EXISTS idx_l402_token_event ON ledger.l402_verification_tokens(event_hash);
```

### API surface

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/v1/protocol/verify` | Issue L402 challenge for an event_hash |
| `GET`  | `/v1/protocol/verify/{token_id}` | Consume paid token → return proof |

**POST `/v1/protocol/verify`**
- Body: `{"event_hash": "<sha256-hex>"}`
- If no `Authorization: L402 ...` header: `402 Payment Required` with `WWW-Authenticate: L402 macaroon="...", invoice="lnbc..."` header
- If valid L402 token presented: `200` with `VerificationResponse` (see below)
- Stub mode (no Lightning node): return `status: "stub"` with proof included directly (enables dev/signet testing without LN)

**GET `/v1/protocol/verify/{token_id}`**
- After external payment, caller polls this to consume the token and get the proof
- `200`: `VerificationResponse`
- `402`: token not yet paid
- `410`: token consumed or expired
- `404`: not found

**VerificationResponse:**
```json
{
  "event_hash": "...",
  "anchor_id": "...",
  "merkle_root": "...",
  "inscription_id": "stub:...",
  "btc_tx_id": "...",
  "btc_block_height": 0,
  "network": "signet",
  "anchor_status": "inscribed",
  "leaf_index": 2,
  "merkle_proof": [
    {"sibling_hash": "...", "position": "left"},
    {"sibling_hash": "...", "position": "right"}
  ],
  "anchored_at": "2026-05-03T...",
  "verified": true,
  "satoshi_price": 100
}
```

### Implementation

**`internal/protocol/validate/`**

- `store.go` — `ValidationStore` interface + `PgxStore` backing `ledger.l402_verification_tokens` and reading `protocol.evidence_anchors` + `protocol.anchors`
- `handler.go` — HTTP layer; `Handler{Store ValidationStore, Budget *billing.Store, Logger *zap.Logger}`
- `l402.go` — stub L402 challenge/response: `IssueMacaroon(eventHash string) (macaroon, invoice string)` + `VerifyMacaroon(token string) bool`. Real Lightning node wired in Phase 2; stub returns deterministic macaroon from HMAC-SHA256 of `(secret, event_hash, token_id)`.

**`cmd/validator/main.go`**
- Env: `VALIDATOR_SECRET` (32-byte hex; HMAC signing key), `VALIDATOR_SATOSHI_PRICE` (default `100`), `VALIDATOR_PORT` (default `:8096`)
- Reads `DATABASE_URL` from env (standard)
- Mounts on `/v1/protocol/verify`

**Gateway mount** — add `validator.Handler.Mount(r)` in `cmd/gateway/main.go`. The gateway is the single ingress; validator is an internal package mounted under it, not a standalone process in Phase 1.

### Key invariants

- A `validation_token` can only be consumed once (`status: consumed`); second call returns `410`
- `stub` mode is enabled when `ORDINALSBOT_API_KEY` is empty (consistent with sub3 stub logic)
- Proof retrieval calls `sub3.VerifyProof(root, leaf, proof)` before returning `verified: true`
- If the event is not yet anchored: `{"verified": false, "anchor_status": "pending", "message": "event not yet anchored"}`

---

## GRO-753 — LNURL-auth

**Dispatch:** [GRO-753](https://linear.app/growdirect/issue/GRO-753)
**Phase:** 1.H
**Branch:** `gro-753-lnurl-auth`
**Worktree:** `.worktrees/gro-753-lnurl-auth`
**Migration slot:** `023_lnurl_auth.up.sql`
**Depends on:** GRO-752 merged (L402 `validator` package wired in gateway)

### What it does

Merchants authenticate to the Canary Protocol API using a Lightning wallet (LNURL-auth). No passwords, no OAuth redirect. A QR code encodes a `k1` challenge; the wallet signs it with a derived key; the server verifies and issues a session token. This is the first-party login surface for `api.canary.growdirect.io`.

### Schema — migration 023

```sql
-- app.lnurl_auth_challenges
CREATE TABLE IF NOT EXISTS app.lnurl_auth_challenges (
    k1              text        PRIMARY KEY,  -- 32-byte random hex
    linked_id       uuid,                     -- populated after auth
    status          text        NOT NULL DEFAULT 'pending'
                    CHECK (status IN ('pending','used','expired')),
    created_at      timestamptz NOT NULL DEFAULT now(),
    expires_at      timestamptz NOT NULL DEFAULT now() + interval '5 minutes'
);

-- app.lnurl_linked_keys
-- Maps a linking public key to an identity in the system.
CREATE TABLE IF NOT EXISTS app.lnurl_linked_keys (
    linking_key     text        PRIMARY KEY,  -- compressed secp256k1 pubkey hex
    owner_id        uuid        NOT NULL,
    owner_type      text        NOT NULL DEFAULT 'merchant'
                    CHECK (owner_type IN ('merchant','user','agent')),
    first_seen_at   timestamptz NOT NULL DEFAULT now(),
    last_auth_at    timestamptz NOT NULL DEFAULT now()
);
```

### API surface (LNURL spec §9)

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/v1/auth/lnurl` | Return LNURL-auth URL (base58-encoded) |
| `GET` | `/v1/auth/lnurl/challenge` | Issue k1 challenge (wallet calls this) |
| `GET` | `/v1/auth/lnurl/callback` | Verify wallet signature, issue session token |
| `GET` | `/v1/auth/session` | Poll: did k1 complete? Returns session token when ready |

**Flow:**
1. UI calls `GET /v1/auth/lnurl` → receives `lnurl1...` encoded URL → display as QR
2. Wallet decodes URL → calls `GET /v1/auth/lnurl/challenge?tag=login&k1=...`
3. Wallet signs k1 with its node key → `GET /v1/auth/lnurl/callback?tag=login&k1=...&sig=...&key=...`
4. Server verifies secp256k1 signature over k1 with linking key
5. Server marks challenge `used`, upserts `lnurl_linked_keys`, issues JWT session token
6. UI polls `GET /v1/auth/session?k1=...` → receives `{"status":"ok","token":"..."}` when complete

**Session token:** JWT signed with `LNURL_JWT_SECRET`. Claims: `sub` = owner_id, `key` = linking_key, `iat`, `exp` (24h). Phase 1 uses HS256; Phase 2 migrates to RS256.

### Implementation

**`internal/auth/lnurl/`**

- `store.go` — `LNURLStore` interface: `InsertChallenge`, `GetChallenge`, `MarkUsed`, `UpsertLinkedKey`
- `crypto.go` — `VerifySignature(k1, sig, key string) (bool, error)` — secp256k1 ECDSA via `github.com/btcsuite/btcd/btcec/v2`
- `session.go` — `IssueJWT(ownerID uuid.UUID, linkingKey string, secret []byte) (string, error)` + `ValidateJWT`
- `handler.go` — HTTP layer, polls for k1 status

**`cmd/gateway/main.go`** — mount `lnurl.Handler.Mount(r)` under `/v1/auth/`

**Dependencies to add:**
- `github.com/btcsuite/btcd/btcec/v2` — secp256k1 (already widely used in Go Lightning tooling)
- `github.com/golang-jwt/jwt/v5` — JWT

Flag these as new dependencies per memory `feedback_flag_dependency_changes` before committing.

### Key invariants

- k1 challenges expire after 5 minutes; expired challenges return `410 Gone`
- Same k1 used twice: second callback returns `409 Conflict`
- `lnurl_linked_keys` is upserted: same linking key may auth multiple times (updates `last_auth_at`)
- Signature verification uses the k1 as the signed message (LNURL spec: wallet signs `H(k1)` with Schnorr or ECDSA — implement ECDSA first)
- Stub mode (env `LNURL_STUB=true`): callback endpoint accepts any signature, returns valid session token. Used in CI and signet demo.

---

## GRO-754 — Cockroach Principle Recovery Proof Tests

**Dispatch:** [GRO-754](https://linear.app/growdirect/issue/GRO-754)
**Phase:** 1.I
**Branch:** `gro-754-cockroach-proofs`
**Worktree:** `.worktrees/gro-754-cockroach-proofs`
**No new migrations.** Integration tests only.

### What it does

Proves that losing any single storage tier does not destroy evidence or the ability to reconstruct. Three scenarios, each a Go integration test that manipulates real DB state and then reconstructs. These run in CI against `canary_go_test`.

### The three scenarios

**Scenario A — L1 loss (hot tier wiped)**

Setup: Write 5 events through Sub 1 → anchor them via Sub 3 → confirm `evidence_anchors` + `anchors` rows exist.

Destroy: `TRUNCATE protocol.evidence CASCADE` (test DB only).

Reconstruct: from `protocol.anchors` + `protocol.evidence_anchors` — the Merkle root and proof paths survive. Any event whose hash is independently known (from the originating system) can be re-verified against the Merkle root alone. Assert: `sub3.VerifyProof(merkleRoot, eventHash, proof)` returns `true` without `protocol.evidence` existing.

Pass condition: proof verification succeeds against the Bitcoin-anchored Merkle root with only the caller's own event hash — no L1 row needed.

**Scenario B — L2 loss (structured parse results wiped)**

Setup: Write 5 events → Sub 2 parses them → `protocol.parsed_events` / `protocol.structured_store` populated.

Destroy: `TRUNCATE protocol.parsed_events CASCADE` (or equivalent Sub 2 output table).

Reconstruct: replay from `protocol.evidence` (L1 raw payloads survive). Call the Sub 2 parse logic directly on the raw payload bytes from L1. Assert: re-parsed output is byte-for-byte identical to original parse.

Pass condition: L2 can be reconstructed from L1 without any external data source.

**Scenario C — Full local loss (L1 + L2 wiped, only chain anchor survives)**

Setup: Write 5 events → anchor → confirm inscription_id on `protocol.anchors` (signet, stub inscriber).

Destroy: `TRUNCATE protocol.evidence CASCADE` (cascades to evidence_anchors and parsed_events).

Reconstruct: the Bitcoin inscription (even stub) carries the Merkle root. Given: (a) the Merkle root from the anchor row, (b) the event hash known to the originating system, (c) the Merkle proof path stored in `evidence_anchors` before the cascade. But wait — `evidence_anchors` cascades on evidence delete. So the real test here is that the proof path was delivered to and retained by the verifying party before the loss event.

Assert: A party that previously called `GET /v1/protocol/verify` and stored the response JSON can independently verify `sub3.VerifyProof(merkleRoot, eventHash, proofFromResponse)` against the Merkle root alone. The chain is the only surviving reference. `verified: true`.

Pass condition: The antifragility property is that the chain-anchored Merkle root outlives every local tier. An external verifier needs only: their event hash + their stored proof path + the on-chain Merkle root. No Canary server required.

### Test file layout

```
internal/protocol/cockroach/
    cockroach_test.go          — TestScenarioA, TestScenarioB, TestScenarioC
    helpers_test.go            — writeTestEvents(), anchorTestBatch(), truncateTable()
```

**Test helpers:**
- `writeTestEvents(t, pool, n int) []string` — inserts n events into `protocol.evidence` directly via SQL, returns slice of event_hashes
- `anchorTestBatch(t, pool, hashes []string) *sub3.AnchorResult` — calls `sub3.WriteAnchor` with StubInscriber
- `truncateTable(t, pool, table string)` — `EXECUTE FORMAT('TRUNCATE %I CASCADE', table)` — parameterized to prevent injection

Tags: `//go:build integration` — skip in unit test runs, require `TEST_DATABASE_URL` env.

CI job: `make test-cockroach` → `go test -tags integration ./internal/protocol/cockroach/...`

### Key invariants

- Tests always run against `canary_go_test` (never `canary_go`)
- TRUNCATE is wrapped in a deferred `t.Cleanup` restore — tests seed + truncate + verify then restore the table (re-insert the seeded rows) so subsequent tests don't see empty state
- Alternatively: use `t.Cleanup(func() { pool.Exec(ctx, "ROLLBACK") })` with a test transaction — but TRUNCATE is DDL and non-transactional in Postgres. Use explicit re-insert in cleanup.
- StubInscriber is always used — these tests do not hit OrdinalsBot

---

## GRO-745 — Phase 1 Ship Comment + Memory Reseed + Brain Wiki Card

**Dispatch:** [GRO-745](https://linear.app/growdirect/issue/GRO-745)
**Phase:** 1.6 (close-out ritual)
**Execute after:** GRO-752, GRO-753, GRO-754 merged

### Actions (coordinator, not subagent)

**1. Ship comment on GRO-739** (parent dispatch)

Post to Linear via `save_comment` on GRO-739:

> **Phase 1 complete — `loop4-wave-g` merged to main.**
>
> All eleven protocol dispatches (GRO-746 through GRO-754) are merged. The Six-Node Canary Protocol pipeline (Patent Application 63/991,596) is live on signet:
>
> - **Node 2** — API Gateway: HMAC-verified webhook intake + event queue publish
> - **Node 3** — Sub 1: SHA-256 hash & seal, write-once L1 evidence store, chain-hash linkage
> - **Node 4** — Sub 2: payload parse & route, L2 structured store
> - **Nodes 5/6** — Sub 3: binary Merkle tree over decoded bytes, OrdinalsBot inscription (stub/signet), Bitcoin anchor registry
> - **Namespace** — `.jeffe` registration with RaaS UUID + ordinal inscription
> - **Validation** — L402 sat-gated proof retrieval (100 sat/verify)
> - **Auth** — LNURL-auth (secp256k1, JWT session, stub mode for CI)
> - **Cockroach Principle** — three rebuild scenarios pass in CI: L1 loss, L2 loss, full local loss
>
> **What next:** GCP deployment (Phase 1.J, `2026-05-03-canary-gcp-blinking-multi-track-kickoff.md`) + GRO-740 OpenAPI spec + GRO-743 public site.

**2. Memory reseed**

```bash
python3 services/memory-bus/scripts/seed_standalone.py
```

Confirm seed log shows Canary Go protocol articles embedded.

**3. Brain wiki card**

Create `Brain/wiki/cards/canary-protocol-phase1-complete.md` via Obsidian MCP:

```markdown
---
type: project-milestone
status: complete
date: 2026-05-03
gro: GRO-739
patent: 63/991,596
---

# Canary Protocol Phase 1 — Complete

The Six-Node Universal Event Notarization pipeline (patent 63/991,596) is
implemented end-to-end in CanaryGo. All protocol tables live in the
`protocol` and `ledger` schemas; migrations 015–023 cover the full span.

## What shipped

Six nodes, three accountability rails, one Cockroach-proven antifragility
property. The chain IS the S4 storage tier — an external verifier needs
only their event hash + their stored Merkle proof + the on-chain root.
No Canary server required to reconstruct truth.

## What's next

GCP deployment → public `api.canary.growdirect.io` → OpenAPI spec + MCP
connector → first merchant signups via LNURL-auth.
```

**4. Update GRO-739 status → Done** via `save_issue`.

---

## Phase 1.J — GCP Deployment

**Plan:** `docs/superpowers/plans/2026-05-03-canary-gcp-blinking-multi-track-kickoff.md`
**Runbook:** `CanaryGo/deploy/runbook-gateway-deploy.md`

This track runs in parallel with GRO-752/753/754 if a second session is available (e.g., Cowork running GCP while Claude Code runs code dispatches). If running single-threaded, execute after GRO-754 merges.

GCP deployment does not depend on Wave G code changes — the gateway that deploys for GCP blinking is the current `cmd/gateway/` at `ebe7a28`. Wave G features (validator, LNURL) are additive mounts on the gateway; they can be deployed incrementally.

---

## Execution checklist

```
[ ] Worktree: .worktrees/gro-752-l402-validation (branch from main @ ebe7a28)
[ ] GRO-752: migration 022 + internal/protocol/validate/ + cmd/validator/ + gateway mount
[ ] GRO-752: spec review → code quality review → merge
[ ] Worktree: .worktrees/gro-753-lnurl-auth (branch from main post-752)
[ ] GRO-753: add btcd/btcec/v2 + golang-jwt/v5 (flag to founder before commit)
[ ] GRO-753: migration 023 + internal/auth/lnurl/ + gateway mount
[ ] GRO-753: spec review → code quality review → merge
[ ] Worktree: .worktrees/gro-754-cockroach-proofs (branch from main post-752)
[ ] GRO-754: internal/protocol/cockroach/ integration tests (3 scenarios)
[ ] GRO-754: make test-cockroach target in Makefile
[ ] GRO-754: spec review → code quality review → merge
[ ] GRO-745: ship comment on GRO-739 · memory reseed · Brain wiki card · GRO-739 → Done
[ ] Phase 1.J: GCP deployment per blinking kickoff plan
[ ] Clean up worktrees post-merge
[ ] git push origin main
```

---

## Merge tag

Loop 4 Wave G merges tagged `loop4-wave-g`:

```
loop4-wave-g: GRO-752 L402 validation, GRO-753 LNURL-auth, GRO-754 Cockroach proofs
```

---

## Cross-references

- `docs/superpowers/plans/2026-05-02-canary-protocol-phase1-execution-plan.md` — Phase 1 dispatch inventory
- `docs/superpowers/plans/2026-05-03-canary-gcp-blinking-multi-track-kickoff.md` — GCP deployment
- `CanaryGo/deploy/migrations/022_*` through `023_*` — new schema
- `internal/protocol/sub3/merkle.go` — VerifyProof used by validator and cockroach tests
- `internal/billing/` — OTB budget store wired into L402 validation
- `Brain/wiki/growdirect-patent-visual-namespace-lifecycle.md` — RaaS lifecycle (FIG. 5)
