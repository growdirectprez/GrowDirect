---
type: wiki
tags: [foundation, cove, governance, blockchain, davis-stirling, declaration-100, advisory-synthesis]
created: 2026-04-19
sources: [Cove/docs/advisor-memos/2026-04-19-comprehensive-review.md]
status: draft
---

# Foundation Blockchain Proof Layer

A blockchain "proof of record" layer can be added to Declaration 100 Article II §5 reactivation votes and to other HOA governance records — but only as a **supplemental, auditable layer on top of a compliant Davis-Stirling process**. It cannot replace secret-ballot collection or inspector-of-elections oversight.

Distilled working position from a 2026-04-19 advisor memo. Deferred implementation (Epic 3 of the Consolidated Design Spec). Bylaw authorization language should be adopted now; operational build comes later.

## The Core Constraint

Pure on-chain voting where members cryptographically sign ballots with personal keys would violate California secret-ballot requirements (Civ. Code § 5100, § 5115) unless anonymity is engineered (zero-knowledge proofs, blinded signatures, or mixing). Even then, California courts and the Department of Real Estate have not blessed pure on-chain voting for HOAs. A hybrid system — traditional process primary, blockchain supplemental — is the only defensible path today.

## Davis-Stirling Requirements the System Must Respect

- **Secret ballot** (§ 5100, § 5115) for director elections, assessments, bylaw/CC&R amendments, removals
- **Inspector of elections** (§ 5110) — independent supervisor of the entire process, certifies tally without compromising secrecy
- **Verifiability and member inspection rights** (§ 5200, § 5210)
- **Electronic voting allowed** (§ 5100.5, § 5105) if governing documents permit and procedures protect secrecy
- **Record retention** (§ 5210, § 5230) — minimum one year, longer if litigation pending
- **Equal access** (§ 5105) — cannot disadvantage members without reliable tech

## How the Hybrid System Works

### Primary Layer — Davis-Stirling Compliant Process

Cove's application already implements this with the `ballots` + `ballot_envelopes` tables under PostgreSQL Row-Level Security:

- `ballots` table has **no member_id** — the vote is anonymous
- `ballot_envelopes` links `ballot_id` to `member_id`, sealed by RLS; only the `inspector` role can SELECT
- Secret ballot mechanics satisfied at the database level

On top of that:
- Proper notice (3× LA daily + 1× San Pedro paper per Declaration 100, or whatever the bylaws require)
- Meeting with proper quorum; voting weighted per governing document
- Inspector of elections collects ballots or signed institutional resolutions
- Inspector certifies results

### Supplemental Layer — Blockchain Proof of Record

Adds immutable provenance without revealing individual votes:

1. Each participating HOA (the 15+ initiating committee for §V §5) cryptographically signs the Declaration 100 text (or the specific reactivation resolution) with an institutional ECDSA key
2. Signed documents + metadata (date, participating HOAs, aggregated vote tally) are hashed
3. Hashes are anchored to Bitcoin via **OpenTimestamps** (free, Bitcoin-anchored, mature)
4. The Foundation publishes the verification link + Merkle proof on cove.org (public audit trail)
5. Individual vote details stay private — only the hash is public

### Outcome

- The blockchain provides tamper-evident proof that the vote occurred on a specific date, which HOAs signed the Declaration 100 text, and which 15+ HOAs participated
- The official legal record remains the inspector-certified record required by Davis-Stirling
- Strong evidentiary value if reactivation is challenged in court ("the vote happened, here is cryptographic proof signed by the participating HOAs")

## First-Vote Use Case: Name-Change Acknowledgement Proposal

When the Cove governance engine comes online — post Community of Abalone Cove third-director recruitment, post first board adoption of the engine — the **first live vote** should be a low-stakes **Name-Change Acknowledgement Proposal**. This is the ideal platform test vote because:

- **Low stakes** — the rename is already legally in effect (filed with CA SOS, voted with quorum by the previous board); the acknowledgement proposal ratifies it as the go-forward reference point rather than re-deciding it
- **Broad consensus expected** — minimizes risk of member pushback on the engine's first run
- **Good data for the inspector-of-elections process** — validates secret-ballot mechanics on the `ballots` / `ballot_envelopes` architecture with a real vote
- **Creates an immutable timeline anchor** — the hybrid blockchain proof layer timestamps the acknowledgement, giving every subsequent governance action a clean reference point: "as of [date], the community acknowledged its current legal name and the continuity of its history under that name"
- **Closes the turnover loose end** — the previous board's last action was the rename; then the board rolled over and the current 2-of-5 director situation emerged. The acknowledgement vote is the first action of the restored board, which cleanly bookends that transition

Proposal content (draft, pending HOA counsel review):

> "RESOLVED, that the membership of Community of Abalone Cove, a California Nonprofit Mutual Benefit Corporation (formerly titled West Portuguese Bend Community Association, renamed with the California Secretary of State as the previous board's last action to disassociate the community's corporate name from the Portuguese Bend landslide connotation following the formation of the Portuguese Bend Abatement District), acknowledges the rename as the reference point for all subsequent governance, preserving continuity of the same legal entity and its 1949 founding, 2009 Restated Declaration, 2012 Amended & Restated Bylaws, and all recorded instruments; and that this acknowledgement be hashed and timestamped via the supplemental cryptographic record layer authorized under the Foundation's bylaws and consistent with Davis-Stirling secret-ballot and inspector-of-elections procedures."

The supplemental blockchain timestamp on this vote becomes the first public Merkle-proof-anchored record on cove.org — a durable artifact of the community's governance restart.

## Why This Fits Declaration 100 Article II §5 Specifically

Article II §5 allows 15 property owners to call a meeting and elect 3 trustees with all Community Association of Palos Verdes powers if the Association fails. Voting is weighted by acreage (one vote per one-third acre). This is a rare, high-consequence governance action — the kind where cryptographic proof-of-record provides durable value. See [[cove-declaration-100]].

The reactivation process is private contractual/governance, not a Davis-Stirling director election per se, so the secret-ballot rule may not strictly apply — but if the reactivation affects governance rights or assessments, it could be triggered. Build the hybrid to handle both cases.

## Technical Recommendations

- **Start simple**: OpenTimestamps (Bitcoin L1 anchored, free, mature) is sufficient for proof-of-record. Don't build a new blockchain.
- **Signing**: Institutional ECDSA keypairs for each participating HOA. The Foundation provides a web interface so members don't manage private keys directly.
- **Privacy**: For institutional HOA signing, blinded signatures or ZKPs are usually overkill. For individual member ballots (separate concern), keep those in the existing `ballots` / `ballot_envelopes` architecture.
- **Auditability**: Publish only hashes + Merkle proofs publicly; keep raw signed documents in inspector custody.
- **Cost & timeline**: POC (OpenTimestamps integration + signing UI) achievable in weeks for low cost. Full production engine is Epic 3 — Year 2+.

## Foundation Role Boundaries

The Foundation **facilitates** — provides the platform, templates, timestamping service, verification page. The Foundation **does not**:

- Conduct the vote
- Exercise governance over any HOA
- Certify results (that's the inspector's role)
- Advocate for specific voting outcomes

This keeps the activity educational / procedural-support, permitted under the Foundation's charitable purpose. Build out of crypto-donation-funded R&D (see [[foundation-crypto-donations]]) or LLC R&D with arm's-length licensing to the Foundation (see [[foundation-three-hat-compensation]] arm's-length licensing section).

## Bylaws Authorization Language

Adopt now to preserve future flexibility:

> "The Corporation may develop, host, and provide to interested parties supplemental cryptographic timestamping and record-signing tools for record-keeping in Declaration 100 Article II §5 processes and analogous inter-HOA governance proceedings, provided that all such tools operate as supplemental record-keeping layers only and shall not replace any secret-ballot, inspector-of-elections, or record-retention procedure required by applicable law or governing documents."

## Risk Assessment

- **Low legal risk** if built as a hybrid supplemental layer
- **Medium technical risk** — ensure the inspector can independently verify blockchain proof
- **High upside** — cryptographic provenance strengthens reactivation record against future challenges; aligns with "visible, verifiable, and available for the community to act on" mission

## Open Decisions

- Bitcoin OpenTimestamps only, or permissioned ledger (Hyperledger Fabric) for richer semantics?
- Inspector training on how to independently verify blockchain proofs
- Whether the tool is Foundation-built (Foundation R&D) or LLC-built (commercial product licensed to Foundation arm's-length)
- Exact scope of "inter-HOA governance proceedings" — limit to §V §5 or broader

## Related

- [[foundation-legal-framework]] — MOC
- [[foundation-bylaws]] — Adopts the authorization language at the first board meeting
- [[foundation-crypto-donations]] — How R&D funding could flow
- [[foundation-three-hat-compensation]] — Arm's-length licensing rules if LLC-built
- [[cove-declaration-100]] — The §V §5 reactivation context
- Cove/CLAUDE.md → `ballots` / `ballot_envelopes` architecture (already implements the primary-layer secret-ballot mechanics)
