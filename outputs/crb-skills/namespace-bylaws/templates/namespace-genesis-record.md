# [NAMESPACE NAME] — Genesis Record

**Document type:** Birth-event record. Inscribed once, at the namespace's genesis block. The canonical reference for everything that follows.

---

## Identity

| Field | Value |
| --- | --- |
| Namespace name | [HUMAN-READABLE NAME] |
| Namespace identifier (on-chain string) | `[id-string]` |
| Domain | [domain-of-application — e.g., "retail vertical," "WPBCA HOA," "firearms-dealer pilot"] |
| Parent operating entity | [WYOMING LLC / DAO LLC name; entity number; date of formation] |
| Sister namespaces (if any) | [list with identifiers] |

## Genesis block

| Field | Value |
| --- | --- |
| Block height | [BLOCK_NNNNNN] |
| Block hash | `[hex_hash]` |
| Block timestamp | [ISO-8601 datetime] |
| Inscription transaction txid | `[tx_id]` |
| Bylaws v1 content hash | `[hex_hash]` |
| Cultural-technical mapping table content hash | `[hex_hash]` |

The inscription event at this block included: the namespace identifier, the bylaws v1 hash, the cultural-technical mapping table hash, and the founding-cohort ordinals (one per principal at minimum, plus founding-cohort allocation reserve).

## Founding ordinals

Per `reference/02-genesis-ordinal-mechanics.md`, genesis ordinals are minted at the genesis block and held by the founding cohort. Each carries lineage depth = 0 (the highest weight per `reference/04-lineage-weighted-voting.md`).

| Ordinal sequence # | Holder role | Holder address (sovereign custody) | Notes |
| --- | --- | --- | --- |
| 1 | [Domain principal] | `[bc1q...]` | [founder seed contribution; per memo] |
| 2 | [Governance principal] | `[bc1q...]` | [Tim per memo] |
| 3 | [Ops principal — TBD per epic open decision #1] | `[bc1q...]` | [third principal] |
| 4-N | [founding-cohort reserve / compliance-architecture lead / etc.] | `[bc1q...]` | [contribution-tier holders entered during Phase 1] |

Total ordinals minted at genesis: [N]
Reserve held in treasury for Phase-1 distribution: [N]
Reserve held for Phase-2+ DAO-ratified distribution: [N]

## Phase configuration

| Field | Value |
| --- | --- |
| Phase 1 duration | [18 months default; namespace override if any] |
| Phase 1 → Phase 2 trigger | [time-elapsed / founder-initiated / namespace-state event] |
| Phase 2 → Phase 3 trigger (optional) | [multi-vertical / network-event criteria] |
| Lineage-decay coefficient α | [0.5 default; namespace-specific override] |

## Treasury configuration

| Field | Value |
| --- | --- |
| Treasury smart-contract address | `[0x... or bc1q...]` |
| Multi-sig threshold | [N-of-M genesis-tier signers] |
| Reserve allocation (% of monthly inflow) | [10-30% default; namespace override] |
| Threshold $10k auto-approve categories | [operations / discretionary / etc.] |
| Threshold $10k-$100k quorum | [30% default; override] |
| Threshold $100k-$1M quorum | [40% default; override] |

## Initial bylaws

The bylaws v1 document is referenced by the content hash above. Full document at `[path or IPFS reference]`. The Articles I-XIV per `templates/bylaws-document.md`.

Ratification of bylaws v1: this genesis record is itself the ratification, anchored to the genesis block height.

## Founding-cohort responsibilities (Phase 1)

| Principal role | Responsibilities | Compensation source |
| --- | --- | --- |
| Domain principal | [strategy / IP stewardship / vertical expertise] | [token-earn + L402 + role salary if applicable] |
| Governance principal | [bylaws stewardship / DAO-process oversight] | [token-earn + L402 + role salary if applicable] |
| Ops principal | [cloud architecture / substrate operation] | [token-earn + L402 + role salary if applicable] |
| Compliance-architecture lead (contributor-tier) | [substrate-to-auditor translation / PCI/ISO/SOC 2] | [token-earn + L402 + relevant cash for runway] |

Per `outputs/dispatches/B4-compliance-architecture-role.md` and per the memo to principals.

## Forward citations

This genesis record is the substrate's foundation document for [NAMESPACE]. Subsequent governance events (proposals, votes, treasury actions, mint events, phase transitions) all reference back to this record as the provenance root. The record itself is immutable; it cannot be amended (only superseded by the namespace's dissolution and the formation of a successor namespace, which would itself begin with a new genesis record).

## Cross-references

- `reference/02-genesis-ordinal-mechanics.md` — the substrate primitives this record instantiates
- `reference/05-phase-transitions.md` — the phase configuration this record locks
- `templates/bylaws-document.md` — the bylaws v1 document this record references
- `outputs/position-paper-eljeffe-io.md` — the protocol this namespace runs on
- `outputs/memo-to-principals-retail-vertical.md` — the founding proposal that established the principal cohort

---

*Genesis record for [NAMESPACE]. Inscribed at block height [BLOCK_NNNNNN].*
*The blocks are written. We were there.*
