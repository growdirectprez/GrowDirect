# [NAMESPACE NAME] Bylaws

**Namespace identifier:** `[on-chain-string]`
**Genesis block height:** [BLOCK_NNNNNN]
**Bylaws version:** v[N]
**Ratified:** [BLOCK_NNNNNN] (ratification block height)
**Lineage-decay coefficient (α):** [DEFAULT 0.5; namespace-specific override]
**Phase-1 duration:** [DEFAULT 18 months from genesis; namespace-specific override]
**Fiscal year:** [DEFAULT calendar year; or namespace-genesis-anchored]

> Two-layer document. The cultural-layer clauses read as operator language, plain construction, recognizable to a non-technical member on a single read. The technical-layer clauses specify substrate mechanisms precisely. Both are present for every Article. Cross-references at the end of each Article.

---

## Article I — Offices

**Cultural.** The principal office of the namespace is in [WYOMING REGISTERED OFFICE — county and city]. Other offices may be designated by the Board as needed. The namespace identifier `[ID]` serves as the public-facing virtual address.

**Technical.** Wyoming DAO LLC registered office at the address above. Smart-contract registry address `[0x... or bc1q...]`. Namespace identifier inscribed at genesis block [BLOCK_NNNNNN]. Member-facing UX surfaces both physical and virtual addresses.

**Cross-reference.** `reference/06-cultural-technical-mapping.md` Article I.

## Article II — Members

**Cultural.** Members are the holders of ordinals from this namespace's lineage tree. Membership is conferred by the smart-contract issuance of an ordinal; membership terminates only by the holder's voluntary transfer of all their ordinals to another party (or to the namespace treasury). Members have voting rights as specified in Article IV; members have inspection rights as specified in Article IX; members have transfer rights as specified in Article VIII.

**Technical.** Genesis ordinals: [N] minted at the genesis block, distributed to founding cohort per `templates/namespace-genesis-record.md`. Lineage tree maintained on chain via ordinal-transfer history. Lineage depth computed per `reference/02-genesis-ordinal-mechanics.md`. Voting weight `w(d) = 1 / (1 + α·d)` where α = [VALUE]. DAO-action stamping per `reference/02-genesis-ordinal-mechanics.md`.

**Cross-reference.** `reference/02-genesis-ordinal-mechanics.md`; `reference/04-lineage-weighted-voting.md`.

## Article III — Meetings of Members

**Cultural.** The namespace holds an annual meeting on or around [DATE — default: anniversary of genesis block height]. Special meetings may be called by [the founder during Phase 1 / by lineage-weighted-vote thresholds during Phase 2 per Article V]. Members may participate in meetings by [in-person / remote / asynchronously through proposal-and-vote mechanism]. Quorum thresholds vary by proposal type per Article IV.

**Technical.** Annual meeting captured as a smart-contract event at block height ≈ [365-day cadence from genesis]. Special meetings triggered by smart-contract function call meeting threshold conditions. Asynchronous participation via signed transactions to the proposal smart contract. Quorum computed in lineage-weighted-vote terms per `reference/04-lineage-weighted-voting.md`.

**Cross-reference.** `reference/04-lineage-weighted-voting.md`; `reference/08-iteration-loop.md`.

## Article IV — Board of Directors

**Cultural.** The genesis-tier ordinal-holders constitute the founding Board. Additional Board members are added during Phase 1 by founder-mint authority and during Phase 2 by lineage-weighted-vote ratification. Terms align with the fiscal year. Vacancies are filled by Board ratification. Board authority encompasses operational decisions and treasury approvals within the thresholds in Article VII.

**Technical.** Genesis-tier ordinal-holders identified by lineage depth = 0. Phase 1 founder-mint events emit on-chain transactions per `reference/02-genesis-ordinal-mechanics.md`. Phase 2 mint proposals follow `reference/04-lineage-weighted-voting.md` for ratification. Term cadence: [annual at fiscal-year boundary]. Multi-sig signature requirements for treasury actions per Article VII.

**Cross-reference.** `reference/02-genesis-ordinal-mechanics.md`; `reference/04-lineage-weighted-voting.md`; `reference/05-phase-transitions.md`.

## Article V — Officers

**Cultural.** The namespace designates the following officer roles, each filled by ordinal-holders at the appropriate lineage tier and ratified by Board vote: [PRESIDENT / DOMAIN PRINCIPAL / GOVERNANCE PRINCIPAL / OPS PRINCIPAL / TREASURER / SECRETARY — namespace-specific roster]. Officer authority is encoded in smart-contract templates referencing this Article. Officers serve at the Board's confidence; removal follows the alignment-check procedure of Article XIV.

**Technical.** Officer-role assignments mapped to ordinal addresses per the genesis record. Smart-contract authority encoded at deployment. Multi-sig requirements per Article VII for treasury-affecting officer actions. Phase-2 founder removal per `reference/05-phase-transitions.md` (super-majority vote, quorum, notice period, cause documentation).

**Cross-reference.** `reference/05-phase-transitions.md`; `reference/03-dao-treasury-patterns.md`.

## Article VI — Committees

**Cultural.** The Board may establish committees of two or more ordinal-holders for project-scoped working groups. Committees may be spawned from any ordinal-holder cohort meeting the lineage-weighted quorum threshold for committee formation. Committee output is recorded on chain for member visibility.

**Technical.** Committee formation event inscribed at block height. Committee membership encoded in smart-contract sub-DAO instance. Committee output anchored to subsequent block heights per the iteration loop in `reference/08-iteration-loop.md`.

**Cross-reference.** `reference/08-iteration-loop.md`.

## Article VII — Treasury

**Cultural.** The treasury is sat-denominated, held in smart-contract-controlled multi-sig addresses. Inflows include L402 micropayments, customer subscriptions, DAO-ratified data-sharing earnings, capital contributions, and channel-partner license fees. Outflows are categorized as operations / personal-compensation / investment / discretionary / pledge per the founder-benefits taxonomy. Approval thresholds vary by amount per the substrate defaults; namespace-specific overrides are documented below. Reserve held at [DEFAULT 10-30%] of monthly inflow.

**Technical.** Treasury smart-contract address `[0x... or bc1q...]`. Multi-sig threshold: [N-of-M genesis-tier signers]. Approval thresholds:
- ≤$10k equivalent → smart-contract auto-approve per category rules
- $10k-$100k → lineage-weighted simple majority + 30% quorum
- $100k-$1M → super-majority (≥67%) + 40% quorum
- >$1M → founder-initiated + structural-amendment review per `reference/05-phase-transitions.md`

Reserve allocation: [%] of monthly inflow; reserve drawdown requires super-majority + multi-sig.

**Cross-reference.** `reference/03-dao-treasury-patterns.md`; `reference/04-lineage-weighted-voting.md`.

## Article VIII — Membership Tokens (Ordinals)

**Cultural.** Each member's ordinal is their on-chain identity in this namespace. Ordinals are transferable subject to the rules below; transfers carry full lineage history. Members may hold ordinals in self-custodied wallets — the substrate has no custodian. The DAO-action stamping mechanism inscribes governance participation directly into the ordinal as it occurs.

**Technical.** Ordinal mint mechanics per `reference/02-genesis-ordinal-mechanics.md`. Transfer rules:
- Transfer to entities in the trusted network (existing ordinal-holders) → freely permitted; transfer event stamps both sending and receiving ordinals; lineage depth update applied
- Transfer to entities outside the trusted network → requires founder approval (Phase 1) or DAO ratification (Phase 2+)
- Transfer back to namespace treasury → always permitted
- Lineage-splitting transfers → [enabled / disabled per namespace decision]

DAO-action stamping per `reference/02-genesis-ordinal-mechanics.md`.

**Cross-reference.** `reference/02-genesis-ordinal-mechanics.md`.

## Article IX — Books and Records

**Cultural.** All consequential namespace activity is anchored on chain. Members have inspection rights to the full decision trail at and after their ordinal's mint block. The substrate's transparency-by-default principle means there is no private records function the Board controls separately from the chain.

**Technical.** Block-height-anchored decision trail. Universal member inspection via on-chain reads. Off-chain artifacts (proposal text, deck content, etc.) referenced by content hash, with full content stored in IPFS or namespace-specific archive accessible via the smart contract's reference function.

**Cross-reference.** `reference/03-dao-treasury-patterns.md` transparency-by-default; `reference/08-iteration-loop.md` comment provenance.

## Article X — Fiscal Year

**Cultural.** The fiscal year begins on [DATE — default January 1 OR genesis-block anniversary] and ends on [DATE]. The fiscal-year choice affects tax filings, treasury rollups, and annual reporting cadence.

**Technical.** Fiscal-year boundaries inscribed as recurring smart-contract events at the appropriate block heights. Treasury rollup snapshots emitted at fiscal-year close. Tax filings prepared by point-in-time engaged accounting (per the no-shared-services posture in `reference/09-anti-patterns.md` Pattern D).

**Cross-reference.** `reference/03-dao-treasury-patterns.md`; `reference/09-anti-patterns.md` Pattern D.

## Article XI — Dues / Earnings

**Cultural.** The namespace does not collect flat dues. Member contribution flows from MCP marketplace publication (token-earn for use of published services) and from DAO-ratified roles (operations roles compensated from treasury per Article VII). Members may optionally make principal-contribution capital injections, which are inscribed and treasury-tracked.

**Technical.** L402 micropayment mechanism wraps each MCP port; payment routes to contributor wallet attached to the gate. Token-earn formula per `reference/03-dao-treasury-patterns.md`. Principal-contribution capital injections inscribed to treasury smart contract; contributor receives ordinals at the contribution-tier lineage depth per Article II.

**Cross-reference.** `reference/03-dao-treasury-patterns.md`; `reference/02-genesis-ordinal-mechanics.md`.

## Article XII — Seal

**Cultural.** The namespace's institutional seal is its smart-contract address; the namespace identifier is its public-facing imprint. On-chain signatures from the appropriate ordinal-holders authenticate institutional acts.

**Technical.** Smart-contract address `[0x... or bc1q...]`. Namespace identifier `[ID]`. Signing-authority mapping in `templates/namespace-genesis-record.md`.

**Cross-reference.** `reference/02-genesis-ordinal-mechanics.md`.

## Article XIII — Waiver of Notice

**Cultural.** Members may waive notice requirements by signed acknowledgement. The acknowledgement is recorded on chain as part of the relevant proposal or governance event. Once waived, the notice cannot be retroactively claimed.

**Technical.** Smart-contract-encoded acknowledgement function. Waiver event inscribed with the corresponding proposal's block-height reference. Auth-token signature required.

**Cross-reference.** `reference/08-iteration-loop.md`.

## Article XIV — Amendments

**Cultural.** This bylaws document is amended through the iteration loop in `reference/08-iteration-loop.md`. Phase 1 amendments require founder-led drafting + lineage-weighted vote (founder weight dominates by structural design). Phase 2+ amendments require lineage-weighted vote per amendment scope:
- Operational clause changes → simple majority + 30% quorum
- Treasury threshold changes → super-majority + 40% quorum
- Structural amendments (substrate primitives, mint authority, voting formulas) → ≥75% + 50% quorum
- Founder-mint authority changes → founder consent (multi-sig) + structural-amendment threshold from non-founder vote

Every amendment runs through the alignment checks in `reference/07-alignment-checks.md` before ratification. Failed checks must be addressed or explicitly overridden.

**Technical.** Amendment proposal artifact per `templates/amendment-proposal.md`. Discussion period [DEFAULT 14 days from proposal block height]. Vote period [DEFAULT 7 days from discussion close]. Threshold check at vote close. Ratification event inscribed at the next available block. Amendment effective at ratification block height + [TIMELOCK if any].

**Cross-reference.** `reference/05-phase-transitions.md`; `reference/07-alignment-checks.md`; `reference/08-iteration-loop.md`.

---

## Cultural-only clauses (no programmatic enforcement)

The following are values statements that influence the technical-layer interpretation in edge cases but do not have direct smart-contract enforcement:

1. **Liberty.** This namespace exists to protect its members from extraction — by financial sponsors, by platforms, by intermediaries who would harvest what the members built. Members own their work, their records, and their name on chain.
2. **Justice.** The math is the same for every party. No backdoor for the platform. No special access for the regulator. No favorable treatment for the well-connected.
3. **The American Way.** Independent enterprise as the engine. Trusted local nodes, federally legitimate. Nobody extracts from anyone.

These statements influence the alignment-check responses (per `reference/07-alignment-checks.md` category F) and the trusted network's interpretation of edge-case clauses. They are not decoration.

---

## Appendix A — Alignment-check report at ratification

[GENERATED at ratification — pass/fail per check from `reference/07-alignment-checks.md`. Failures with override rationale documented per check. See `templates/alignment-review.md` for the periodic-review artifact.]

## Appendix B — Comment ledger reference

[CONTENTS of `templates/comment-ledger.md` for this version's iteration cycle. Captures the comments from the trusted network that informed the drafting of this version.]

## Appendix C — Substrate cross-references

- The eljeffe Hash and Seal Protocol (`outputs/position-paper-eljeffe-io.md`) — the substrate technical foundation
- Genesis Pool wiki (`Brain/wiki/growdirect-genesis-pool.md`) — origin of the namespace's founding ordinal inventory
- Wyoming DAO LLC statute (Wyo. Stat. Ann. § 17-31-101 et seq.) — legal substrate giving these bylaws regulatory standing
- Cove (Python/Flask proposal engine) — the reference implementation of the iteration loop in `reference/08-iteration-loop.md`

---

*Bylaws v[N] of [NAMESPACE]. Ratified at block height [BLOCK_NNNNNN]. Hash: `[bylaws_v[N]_hash]`.*
*Anchored to the Bitcoin time chain.*
