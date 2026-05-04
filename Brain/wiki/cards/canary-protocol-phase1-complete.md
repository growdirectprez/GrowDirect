---
type: card
status: complete
date: 2026-05-03
project: Canary Go
tags: [canary, protocol, patent, phase1, bitcoin, lnurl, l402]
last-compiled: 2026-05-03
needs-review: false
---

# Canary Protocol — Phase 1 Complete

Patent Application 63/991,596. Phase 1 delivers the three foundational properties of the Canary Protocol: cryptographic evidence ingestion (Sub 1), Bitcoin-anchored Merkle commitments (Sub 3), L402-gated proof verification (Validation API), Lightning wallet authentication (LNURL-auth), and the Cockroach Principle antifragility proofs.

## What shipped (Wave G, 2026-05-03)

| Dispatch | What it delivers |
|---|---|
| GRO-752 | L402 Validation API — `POST /v1/protocol/verify` (402 gate) + `GET /v1/protocol/verify/{token_id}` (consume + prove) |
| GRO-753 | LNURL-auth — secp256k1 wallet login, JWT session, 4-endpoint flow |
| GRO-754 | Cockroach Principle integration tests — 3 scenarios proving antifragility |

Merged to `main` at commit `60642ad`. Migrations 022–023 deployed to `canary_go` / `canary_go_test`.

## Cockroach Principle — three scenarios

The Cockroach Principle is the antifragility property: any single storage tier can be destroyed and the protocol survives.

| Scenario | Tier destroyed | Recovery path |
|---|---|---|
| A — L1 Loss | `protocol.evidence` wiped | Verify via Bitcoin anchor + Merkle proof held by verifying party |
| B — L2 Loss | Parsed event layer lost | Reconstruct from `raw_payload` in L1; verify content parity |
| C — Full local | All local DB tables wiped | Verify via `merkle_root` + externally-held proofs; zero DB reads |

Run: `make test-cockroach TEST_DATABASE_URL=postgres://...`

## Architecture — five nodes

```
Gateway (Node 2)
  → Sub 1: hash & seal, chain anchoring, append-only evidence
  → Sub 2: parse & route (placeholder — L2 tier proven by Scenario B)
  → Sub 3: Merkle tree, Ordinals inscription, anchors table
  → Validation: L402-gated proof endpoint (revenue surface)
```

Evidence is append-only by PostgreSQL trigger set (`evidence_no_delete`, `evidence_no_truncate`, `evidence_no_update`). The trigger set is the DB-level enforcement of the evidentiary accountability rail.

## L402 Validation API

- `POST /v1/protocol/verify` — takes `{event_hash}`, returns 200 unverified if not anchored yet, 402+`WWW-Authenticate` if no macaroon presented
- `GET /v1/protocol/verify/{token_id}` — consumes token, runs `sub3.VerifyProof`, returns `VerificationResponse` with full anchor provenance (merkle_root, inscription_id, btc_tx_id, btc_block_height, network, leaf_index, proof path, verified bool)
- Stub L402 (HMAC-SHA256 macaroon) for signet/CI; env `VALIDATOR_SECRET` + `VALIDATOR_SATOSHI_PRICE` (default 100)

## LNURL-auth

- Full LNURL-auth §9 flow: QR challenge → wallet handshake → secp256k1 sig verify → JWT issue → UI poll
- Owner ID is UUID v5 derived from linking key (`uuid.NewSHA1(lnurlNamespace, []byte(key))`) — deterministic, stable across wallet re-installs
- Stub mode (`LNURL_STUB=true`) skips secp256k1 for CI
- `sync.Map` pending tokens: known TTL limitation (accumulates until process restart); logged for follow-up

## What's next (Phase 2+)

- Sub 2 full implementation (`protocol.parsed_events`)
- Real OrdinalsBot inscription (replace StubInscriber with live client)
- L402 live Lightning invoice (replace stub with real lnd/CLN integration)
- Token economics layer (Phase 2, GRO-739)
- TEE compute + anonymous protocol (Phase 3)
- S4 chain storage generalization beyond protocol.evidence (Phase 4)

## Cross-references

- [[Brain/wiki/cards/platform-thesis]] — three accountability rails; evidentiary rail is what Phase 1 closes
- `docs/sdds/go-handoff/` — Sub 1, Sub 3, identity SDDs
- GRO-739 (closed) — parent dispatch
- GRO-752, GRO-753, GRO-754 (closed) — individual Wave G dispatches
