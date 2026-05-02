# Canary Protocol — Phase 1 Execution Plan

**Plan ID:** `2026-05-02-canary-protocol-phase1-execution-plan`
**Parent dispatch:** [GRO-739](https://linear.app/growdirect/issue/GRO-739)
**Patent reference:** Application 63/991,596 — *Universal Event Notarization, Six-Node Architecture* (filed 2026-02-26)
**Author:** ALX
**Date:** 2026-05-02
**Status:** ACTIVE — ready for pickup

---

## Mission

Ship the publicly-verifiable, patent-aligned **Canary Protocol substrate**. The deliverable is the operating embodiment of Patent Application 63/991,596: the Six-Node Universal Event Notarization pipeline with Bitcoin-sovereign data hierarchy, `.jeffe` namespace identity, L402 sat-gated revenue mechanism, and rebuild/recovery proofs.

By the end of Phase 1, the architecture is live on signet, the protocol is publicly documented at `api.canary.growdirect.io`, and any third party can submit a payload, see it anchored on Bitcoin, and verify it for sats.

---

## What ships at end of Phase 1

- `api.canary.growdirect.io` live — landing, Swagger UI, LNURL-auth, L402 verify demo
- Six-Node pipeline operational end-to-end from webhook intake to Bitcoin signet anchoring
- Canonical OpenAPI 3.0 spec + MCP connector publicly available
- `.jeffe` namespace registration working (signet)
- **Cockroach Principle proven** in CI (three rebuild scenarios passing)
- First merchant signups via LNURL-auth
- Memory bus reseeded; Brain wiki card live; GRO-739 ship comment posted

---

## Dispatch inventory

Eleven active children of GRO-739 (two cancelled in audit, descriptions preserved with forward-pointers):

| GRO | Phase | Dispatch |
|---|---|---|
| 740 | 1.1 | OpenAPI 3.0 generator from canonical SDD |
| 741 | 1.2 | MCP connector wrapping OpenAPI |
| 743 | 1.4 | `api.canary.growdirect.io` site (landing + Swagger + signup + verify demo) |
| 745 | 1.6 | Phase 1 ship comment + memory reseed + Brain wiki card |
| 746 | 1.A | API Gateway (Node 2): HMAC verify + queue publish |
| 747 | 1.B | Triple Subscriber scaffolding (the patent-named innovation) |
| 748 | 1.C | Sub 1 / Node 3: Hash & Seal — L1 Evidence Store |
| 749 | 1.D | Sub 2 / Node 4: Parse & Route — L2 Structured Store |
| 750 | 1.E | Sub 3 / Node 5/6: Merkle & Ordinal — Bitcoin anchor |
| 751 | 1.F | `.jeffe` namespace registration |
| 752 | 1.G | L402 sat-gated Validation API |
| 753 | 1.H | LNURL-auth |
| 754 | 1.I | Rebuild/recovery proof tests (Cockroach Principle) |

Cancelled: GRO-742 (was DMZ ingest, replaced by 746–750), GRO-744 (was API key issuance, replaced by 753).

---

## Dependency graph

```
            ┌──────────────┐
            │ 740 OpenAPI  │ ──────────────────────┐
            │  (no deps)   │                       │
            └──────────────┘                       │
                    │                              │
                    ▼                              ▼
            ┌──────────────┐               ┌──────────────┐
            │  741 MCP     │               │ 743 Public   │
            │  connector   │               │   site       │
            └──────────────┘               └──────┬───────┘
                                                  │ needs 752 + 753
                                                  │
   ┌─── independent pipeline track ───┐
   │                                  │
   ▼                                  │
┌──────────────┐                      │
│ 746 Gateway  │ (no architectural deps)
│   (Node 2)   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ 747 Triple   │
│  Subscriber  │
│  scaffolding │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ 748 Sub 1    │
│  Hash & Seal │
│  (L1)        │
└──────┬───────┘
       │
       ├──────────────┐──────────────────┐
       ▼              ▼                  ▼
┌─────────────┐ ┌─────────────┐   ┌──────────────┐
│ 749 Sub 2   │ │ 750 Sub 3   │   │ 753 LNURL    │
│ Parse&Route │ │ Merkle &    │   │  -auth       │
│ (L2)        │ │ Ordinal (₿) │   │  (minimal)   │
└─────────────┘ └─────┬───────┘   └──────────────┘
                      │
                      ├──────────────┐
                      ▼              ▼
              ┌──────────────┐ ┌──────────────┐
              │ 751 .jeffe   │ │ 752 L402     │
              │  namespace   │ │  Validation  │
              └──────────────┘ └──────────────┘
                      │              │
                      └──────┬───────┘
                             ▼
                     ┌──────────────┐
                     │ 754 Recovery │
                     │  proof tests │
                     └──────────────┘
                             │
                             ▼
                     ┌──────────────┐
                     │ 745 Phase 1  │
                     │  close-out   │
                     └──────────────┘
```

---

## Critical path

The longest sequential chain through Phase 1:

**746 → 747 → 748 → 750 → 752 → 754 → 745**

That's 7 dispatches in series. Everything else either branches off this spine or is independent.

Estimated duration on the critical path (solo, focused):

| Dispatch | Days |
|---|---|
| 746 API Gateway | 2 |
| 747 Triple Subscriber scaffolding | 2–3 |
| 748 Sub 1 Hash & Seal | 2–3 |
| 750 Sub 3 Merkle & Ordinal | 4–6 (highest variance — external deps) |
| 752 L402 Validation API | 3–4 |
| 754 Rebuild/recovery proof tests | 3–4 |
| 745 Close-out | 0.5 |
| **Total** | **17–23 days** |

---

## Parallel tracks

Tracks that can ship without blocking the critical path:

**Track A — Documentation surface (no infra deps):**
- 740 OpenAPI generator (1–2 days)
- 741 MCP connector (2–3 days, after 740)
- 743 Public site v1 with Swagger only (1–2 days, after 740) — full version waits for 752+753

**Track B — Pipeline branches (after 748):**
- 749 Sub 2 Parse & Route (2–3 days) — replays from L1 evidence into L2 structured tables; doesn't block verify path
- 753 LNURL-auth minimal version (2–3 days) — wallet auth without `.jeffe` binding initially

**Track C — Identity layer (after 750):**
- 751 `.jeffe` namespace (2–3 days) — uses 750's ordinal pathway

These tracks can run in parallel with the critical path — total Phase 1 calendar duration is bounded by the critical path, not by total work.

---

## Sequencing recommendation

A reasonable solo execution order:

| Wave | GRO | Why this order |
|---|---|---|
| 1 | **740** | Pure derivative work from canonical SDD. No infra. Unblocks 741 + 743. Momentum start. |
| 2 | **746** | Pipeline foundation. Receives webhooks, validates, queues. Everything else assumes a queue with events. |
| 3 | **747** | The patent-named innovation. Three independent consumers wired to the queue. |
| 4 | **748** | First subscriber. L1 Evidence Store is the bedrock cache; everything above rebuilds from here. |
| 5 | **750** *(parallel: 749)* | Bitcoin anchoring. Highest external risk — start early. 749 (L2 Parse & Route) can run alongside since it only needs 748. |
| 6 | **751** *(parallel: 753, 741)* | `.jeffe` namespace once ordinal pathway works. LNURL-auth and MCP connector start here. |
| 7 | **752** | L402 verify API completes the public storefront. |
| 8 | **743** | Public site stitches it all together (Swagger + LNURL signup + L402 verify demo). |
| 9 | **754** | Recovery proof tests. Three scenarios (L2 fails / L1 fails / total failure). Cockroach Principle proven, not asserted. |
| 10 | **745** | Ship comment, memory reseed, Brain wiki card. |

Calendar projection: **5–8 weeks** for solo focused work, assuming no major blockers on the OrdinalsBot/signet/Lightning regtest setup.

---

## Integration moments

Three points where subsystems plug together — these are the verification checkpoints:

### Checkpoint 1 — End-to-end ingest into L1 (after 746 + 747 + 748)

Submit a webhook → see it land in `protocol.evidence` with valid hash chain → bilateral verification API returns it. Single most important early proof: the gateway and Sub 1 work together end-to-end.

**Verification ritual:**
```bash
curl -X POST $GATEWAY/v1/protocol/webhook/square \
  -H "X-Signature: $HMAC" -d @sample-event.json
# expect 200 OK <5ms

curl $GATEWAY/v1/protocol/evidence/$EVENT_HASH
# expect canonical evidence record with chain_hash
```

### Checkpoint 2 — Bitcoin anchor on signet (after 750)

A batch of chain_hashes from Sub 1 is built into a Merkle tree, inscribed on Bitcoin signet, and the inscription_id is verifiable on a block explorer.

**Verification ritual:**
```bash
curl $GATEWAY/v1/protocol/anchor/$EVENT_HASH
# returns inscription_id + Merkle proof

# Verify on mempool.space/signet/tx/$TXID
```

### Checkpoint 3 — Sat-gated verify with cryptographic proof (after 752)

L402 flow round-trip on regtest Lightning, with the verification response containing the inscription_id from Checkpoint 2.

**Verification ritual:**
```bash
curl $GATEWAY/v1/protocol/verify/$EVENT_HASH
# expect 402 with Lightning invoice

# Pay invoice → get preimage, retry with macaroon+preimage
# expect 200 with verification proof + inscription_id + Merkle path
```

### Checkpoint 4 — Cockroach Principle proven (754)

Three rebuild scenarios pass in CI. This is the integration test for the entire architecture.

---

## Risk register

| Risk | Severity | Mitigation |
|---|---|---|
| **OrdinalsBot signet/testnet support** — API may not support signet ordinals or have rate limits | High | Spike early in 750 build. Fallback: self-hosted `ord` against signet. |
| **Lightning regtest setup time** — LND/CLN regtest with channels for L402 testing has setup overhead | Medium | Allocate 1–2 days in 752; consider Polar (lightning-polar) for fast regtest harness. |
| **Treasury key custody pattern** — production mainnet inscription requires a key-management plan | Medium | Document as runbook in 750; mainnet keys not required for Phase 1 (signet only). |
| **Patent-claim drift** — implementation accidentally drifts from patent claims | High | Each dispatch's DoD includes patent-claim verification; 754 (recovery tests) is the integration proof. |
| **External dependency surprise** — OrdinalsBot or Lightning library changes API mid-build | Low | Pin versions; document in commit messages. |
| **Schema migration sequencing** — `protocol.*` schema accreting across dispatches | Medium | One Alembic migration per dispatch; tests verify schema state per dispatch. |
| **Memory bus drift** — wiki seeded before patent-architecture cards exist | Low | Reseed scheduled in 745 covers all new content; incremental seeds along the way. |

---

## Definition of done — Phase 1

Roll-up criteria, mirrored by GRO-745's ship comment:

- [ ] Six-Node pipeline operational on signet (Source → Gateway → Queue → Triple Subscriber → L1/L2/Bitcoin)
- [ ] Triple Subscriber Pattern proven independent (kill any one, others continue)
- [ ] `.jeffe` namespace registration round-trip on signet
- [ ] L402 sat-gated verification round-trip on Lightning regtest
- [ ] LNURL-auth round-trip with at least one wallet
- [ ] OpenAPI 3.0 spec validates and lints clean
- [ ] MCP connector callable from Claude Desktop with copy-paste config
- [ ] `api.canary.growdirect.io` live with TLS, all sections functional
- [ ] Cockroach Principle proven — all three recovery scenarios pass in CI
- [ ] Memory bus reseeded; `memory_recall("canary protocol live")` surfaces the new card
- [ ] Brain wiki card committed at `Brain/wiki/cards/canary-protocol-phase1-live.md`
- [ ] Recovery runbook committed at `Brain/wiki/cards/canary-protocol-recovery-runbook.md`
- [ ] GRO-739 ship comment posted with all required content + screenshots + commit SHAs
- [ ] All Phase 1 children closed; GRO-739 advances to Phase 2

---

## Phase 2 preview

What unlocks once Phase 1 ships (per parent GRO-739):

- **Tokenomics + paid tiers** — token contract design, free-trial→paid mechanic, Starter/Pro/Enterprise tiers, per-junction satoshi metering, VAR partner revenue share
- **First paid conversion** within 60 days of Phase 2 ship
- **First $10K MRR** within 90 days

Phase 2 inherits the substrate that Phase 1 ships. The L402 metering surface from GRO-752 becomes the ledger Phase 2's tokenomics layer extends.

---

## Working norms

- **Each dispatch ships independently.** Working in topic branches `gclyle/gro-XXX-*` per Linear's auto-generated branch names.
- **Comment on the dispatch on pickup** with status → In Progress and ETA. Comment on completion with commit SHA, output paths, and any GRO follow-ups recommended.
- **Memory bus reseed after each dispatch** that touches `Brain/wiki/` or `docs/sdds/`. Incremental seed is fast.
- **No agent identity names in external-facing artifacts.** The patent, the Method, and the founder are the visible identities; internal agents stay internal.
- **Patent claims are the spine.** Every dispatch's DoD includes a patent-claim verification step. Drift from the patent → file a comment, not a silent change.

---

## Cross-references

- **Patent:** Application 63/991,596 — Universal Event Notarization (FIG. 1–6)
- **PhD position paper:** `docs/_archive/ip-vault/Canary_Bitcoin_Architecture_Research_Paper_v1.0.md`
- **Closed-loop governance:** `Brain/wiki/canary-closed-loop-cost-attribution.md`, `Brain/wiki/cards/platform-closed-loop-attribution.md`
- **Patent visuals (HTML):** `docs/_archive/ip-vault/patent-visuals/Patent_*.html`
- **Canonical data model (developer-facing):** `docs/sdds/go-handoff/canonical-data-model.md`
- **MCP service junctions:** `docs/sdds/go-handoff/mcp-service-junctions.md`
- **Drop-zone CI/CD (already done):** GRO-700
- **Engagement kickoff site GRO** *(work paused, depends on this Phase 1 delivering for content reframe)*: see kickoff-deck dispatch
- **Memories anchoring this plan:**
  - `project_canary_is_customer_of_protocol`
  - `project_canary_chain_is_storage`
  - `project_ship_the_standard_now`
  - `project_mcp_native_virtual_usbc_plug`
  - `project_satoshi_cost_model`
  - `project_rapidpos_go_pivot` (Go is the stack)
