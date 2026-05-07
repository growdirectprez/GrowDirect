---
title: Declaration 1 — Founding Declaration of the eljeffe DAO LLC
type: declaration
sequence: 01
status: founding act — to be ratified at the genesis block
date: [DATE OF GENESIS BLOCK INSCRIPTION]
inscription: anchored alongside white paper at ordinal 1
---

# Declaration 1 — Founding Declaration

**eljeffe DAO LLC**
*A Wyoming Decentralized Autonomous Organization Limited Liability Company*

---

## Article I — Constitution

The eljeffe DAO LLC is constituted at this block height under the Wyoming Limited Liability Company Act. The entity adopts the structure described in the white paper inscribed on ordinal 1 of the Genesis Pool. The white paper, in its current and any subsequent ratified form, is the foundational specification of the entity's substrate. This Declaration ratifies the entity's existence, identifies its founding cohort, sets its initial parameters, and inscribes the constitutional record at the genesis block.

## Article II — Identity

| Field | Value |
| --- | --- |
| Legal name | eljeffe DAO LLC |
| Jurisdiction | Wyoming |
| Statutory basis | Wyoming Limited Liability Company Act, DAO LLC chapter |
| Management designation | Algorithmic |
| Management mechanism | Smart contract specified in white paper section 5; deployed at the address recorded below |
| Registered office | [Wyoming registered office address] |
| Registered agent | [Wyoming registered agent name and address] |
| EIN | [Employer Identification Number issued at filing] |
| Namespace identifier (on-chain) | `[on-chain-string-inscribed-at-genesis]` |
| Smart-contract address | `[bc1q... or 0x...]` |
| Genesis block height | [BLOCK_NNNNNN] |
| Genesis block hash | `[hex_hash]` |
| White paper inscription txid | `[tx_id of ordinal-1 inscription]` |
| White paper content hash | `[SHA-256 of white paper at inscription]` |
| Bylaws v1 inscription txid | `[tx_id of bylaws-v1 inscription]` |
| Bylaws v1 content hash | `[SHA-256 of bylaws v1 at inscription]` |
| This Declaration's inscription txid | `[tx_id of this declaration]` |
| This Declaration's content hash | `[SHA-256 of this document at inscription]` |

## Article III — The Genesis Pool

The eljeffe DAO LLC's foundational asset is the Genesis Pool: ten million satoshis (10,000,000 sats; 0.1 BTC) earned by the founder through proof-of-work mining and contributed in their entirety to the entity at constitution. The pool's provenance is verifiable on the time chain: mining reward transaction at block [MINING_BLOCK]; receiving wallet at [FOUNDER_WALLET]; transfer to the entity's smart-contract custody at [TRANSFER_TX]. The pool is bounded. It cannot be replenished by minting additional ordinals; subsequent allocations occur only from the existing pool's lineage tree.

**Ordinal 1.** The first ordinal of the Genesis Pool is constituted as the substrate's foundational ordinal. It carries the white paper inscription. It is held in sovereign custody by the entity at the entity's smart-contract address. Ordinal 1 cannot be transferred, sold, or pledged; its disposition is bound to the entity's continued constitution.

**Ordinals 2 through N.** Founding cohort allocations, made from ordinals 2 through N at this block, are recorded in Article V below. Each allocation transfers the named ordinals from the entity's custody to the recipient's sovereign-custody wallet at the address recorded.

**Ordinals N+1 through 10,000,000.** Held in entity treasury at the entity's smart-contract address, available for distribution under the bylaws' founder-mint mechanism (during Phase 1) or under the lineage-weighted-vote ratification mechanism (during Phase 2 and beyond). The treasury balance, allocation events, and remaining-reserve count are continuously visible on chain.

## Article IV — Adopted Bylaws

The eljeffe DAO LLC adopts as its initial bylaws the document inscribed at the txid recorded above. The bylaws v1 specify, at the parameter level for this namespace:

| Parameter | Value at constitution |
| --- | --- |
| Lineage-decay coefficient α | 0.5 (yielding voting weight `w(d) = 1 / (1 + 0.5·d)` per white paper section 2) |
| Phase-1 (founder-mint phase) duration | 18 months from the genesis block |
| Phase-1 → Phase-2 transition trigger | Time-elapsed reaching encoded duration; or founder-initiated early transition |
| Treasury approval — auto-execute threshold | $10,000 equivalent (categorized cash-out per white paper section 2; bylaws Article VII) |
| Treasury approval — simple-majority threshold | $10,001 to $100,000 equivalent (≥50% lineage-weighted vote, ≥30% quorum) |
| Treasury approval — super-majority threshold | $100,001 to $1,000,000 equivalent (≥67% lineage-weighted vote, ≥40% quorum) |
| Treasury approval — structural-amendment threshold | Above $1,000,000 equivalent (founder-initiated + structural-amendment review) |
| Multi-sig threshold for treasury actions | [N-of-M] genesis-tier signers |
| Reserve fraction (treasury) | [%] of monthly inflow held in reserve; reserve drawdown requires super-majority + multi-sig |
| Fiscal year | January 1 to December 31 |
| Transfer rules | Per white paper section 2; trusted-network transfers freely permitted (with on-chain stamping); non-trusted-network transfers require founder approval (Phase 1) or DAO ratification (Phase 2+); transfer to entity treasury always permitted |
| Discussion-period default | 14 days from proposal block height |
| Vote-period default | 7 days from discussion-period close |
| Periodic alignment review cadence | Annual; anchored to genesis-block anniversary |

The bylaws document, inscribed at the txid above, is the authoritative source for these parameters; this Declaration's reproduction is for orientation.

## Article V — Founding Cohort

The founding cohort is constituted at this block. Each member receives the named ordinals at lineage depth 0 (genesis tier), with full voting weight (w = 1.0) per the formula above.

| Role | Member | Sovereign-custody address | Ordinals received | Lineage depth | Voting weight per ordinal |
| --- | --- | --- | --- | --- | --- |
| Domain principal | [Founder name] | `[bc1q...]` | [ordinal-N1 through ordinal-N2] | 0 | 1.000 |
| Governance principal | [Tim — name] | `[bc1q...]` | [ordinal-N3 through ordinal-N4] | 0 | 1.000 |
| Ops/Cloud principal | [TBD per Phase A; ratified by amendment when named] | `[bc1q...]` | [ordinal-N5 through ordinal-N6] | 0 | 1.000 |
| Compliance-architecture lead (contributor-tier — entered via founder-mint) | [TBD] | `[bc1q...]` | [ordinal-N7] | 1 (contributor-tier) | 0.667 |

Founding-cohort additional allocations during the founder-mint phase (Phase 1, defined above) are made by founder-mint events recorded individually in `treasury/mint-events.md` as they occur. Each founder-mint event is inscribed at the block height of issuance and references this Declaration as its constitutional basis.

## Article VI — Officer Designations

The following officer roles are designated at constitution. Officer authority is encoded in smart-contract templates referenced in the bylaws Article V. Officer designations are coextensive with the role; the role's substantive authority belongs to the entity, and ending the role returns the officer-ordinal (when adopted under the addendum's officer-ordinal class — see corresponding amendment when ratified) to the entity for re-issuance.

| Officer | Role-holder at constitution | Authority |
| --- | --- | --- |
| President | [Founder name — Domain principal] | Per white paper section 5; signs commercial agreements within bylaw thresholds; represents the entity in external matters; coordinates Phase A operational program |
| Treasurer | [Genesis-tier holder — TBD] | Per white paper section 2 treasury mechanism; co-signs multi-sig treasury actions; reports treasury state per the substrate's transparency-by-default principle |
| Secretary | [Genesis-tier holder — TBD; Phase-A intent: human; Phase-B+ intent: agentic per addendum officer-ordinal class] | Maintains the on-chain record per white paper section 5; issues conclusive-evidence certificates; handles delinquency notices; generates periodic disclosures |
| Compliance-architecture lead | [Contributor-tier — TBD] | Per dispatched role scope (`outputs/dispatches/B4-compliance-architecture-role.md`); substrate-to-auditor translation; PCI scope ownership; ISO 27001 + SOC 2 readiness; NICS-attestation regulatory engagement |

Officer designations are confirmed by ratification of this Declaration at the genesis block. Subsequent officer changes occur under bylaws Article XIV amendment mechanics.

## Article VII — Adopted Specifications by Reference

The following specifications are adopted by reference at constitution. Each is hash-anchored at the inscription record below; subsequent amendments to these specifications require ratification under bylaws Article XIV.

| Specification | Reference | Content hash at constitution |
| --- | --- | --- |
| White paper v1 | `white-paper/white-paper-v1.md`; ordinal 1 inscription | `[SHA-256]` |
| Bylaws v1 | `bylaws/v1-ratified-[DATE].md`; inscription txid above | `[SHA-256]` |
| Genesis Pool capital thesis | `corp-archives/genesis-pool-capital-thesis.md` | `[SHA-256]` |

## Article VIII — Compliance and External Engagement

At constitution, the entity's compliance posture is initiated under the program defined in the compliance-architecture lead role scope. Specifically:

- **PCI-DSS scope.** No cardholder data flows through entity-controlled systems; tokenization at the payment terminal device per industry standard. SAQ-A or SAQ-A-EP attestation maintained by the compliance-architecture lead.
- **ISO 27001:2022.** Readiness assessment initiated at constitution; Stage 1 audit target month 9; Stage 2 observation period start month 12; certificate issuance target month 18.
- **SOC 2 Type II.** Observation period start month 18; certificate issuance target month 30.
- **State privacy law conformance.** Customer-as-data-owner architectural commitment is documented per the substrate's data-sovereignty position; evolves with the relevant state laws (CCPA, CPRA, VCDPA, CPA, CDPA, and successors) under the compliance-architecture lead's continuous monitoring.

External engagements at constitution: Wyoming counsel engaged on a point-in-time basis for the constitutional filings (this Declaration; articles of organization; EIN application; banking relationship facilitation); Wyoming-chartered banking partner selected for the entity's sat-denominated treasury custody (subject to the parallel disposition of the relevant SPDI-charter relationships).

## Article IX — Records and Inspection

All consequential entity activity is anchored on chain per white paper section 3. Member inspection rights extend to the full decision trail at and after each member's ordinal mint block. Off-chain artifacts (proposal text, deck content, meeting minutes, declarations, partnership records, treasury action narratives) are referenced by content hash; full content is accessible at the entity's record store, with the canonical paths documented in this vault's README.

The vault holding the entity's accumulating governance record is constituted at this Declaration. Subsequent declarations, bylaws amendments, principal-record updates, treasury events, partnership records, and compliance attestations are added to the vault as they occur, each with content-hash anchoring to its inscription block height.

## Article X — Effective Date and Block-Height Anchor

This Declaration is effective at the block height of its inscription. The block height, block hash, transaction txid, and content hash are recorded at the moment of inscription and supersede any drafted placeholders in this document. The Declaration's authoritative version is the inscription; the on-disk version in this vault is the orientation copy.

---

*Inscribed at block height [BLOCK_NNNNNN], block hash `[hex_hash]`, transaction txid `[tx_id]`. Anchored to the time chain.*

*The eljeffe DAO LLC begins.*
