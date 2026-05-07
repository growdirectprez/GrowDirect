---
title: eljeffe DAO LLC — vault README
status: vault scaffold; awaits constitutional acts to populate
created: 2026-05-03
---

# eljeffe DAO LLC — vault

This vault holds the accumulating governance record of the **eljeffe DAO LLC**. The entity is constituted at the genesis-block inscription event recorded in `declarations/01-founding-declaration.md`. The substrate operating the entity is specified in `white-paper/white-paper-v1.md`, inscribed on ordinal 1 of the Genesis Pool at constitution.

This vault is intentionally a **separate root** from the platform / R&D / skill-library work that produces the entity's tools. Tools live in `~/GrowDirect/`; this vault holds the governance record those tools eventually produce when run against the entity. Once the user has created `~/eljeffe/` on the host and granted access, this vault relocates from `outputs/eljeffe-vault/` to `~/eljeffe/` with a single `mv` command.

## Why this vault is its own root

The substrate's operating record accumulates over decades. It is the constitutional history of the entity. Co-locating it with the platform-development repo conflates two different categories of artifact: tools change frequently and follow a software-development cadence; constitutional acts are sparse, permanent, and follow an inscription cadence. Different categories want different roots.

The vault structure also intentionally has no prior-art discussion in any of its constitutional documents. The white paper and the founding Declaration stand alone as the foundational specification of a new patentable structure.

## Vault structure

```
eljeffe/
├── README.md                                    ← this file
├── white-paper/
│   └── white-paper-v1.md                        ← inscribed on ordinal 1
├── declarations/
│   ├── 01-founding-declaration.md               ← Declaration 1 — the founding act
│   └── (subsequent declarations as constitutional acts occur)
├── bylaws/
│   ├── v1-ratified-[DATE].md                    ← bylaws v1 (template at outputs/crb-skills/namespace-bylaws/templates/bylaws-document.md)
│   ├── amendments/
│   │   └── (per-amendment proposal + alignment-check + ratification record)
│   └── (subsequent ratified versions)
├── minutes/
│   └── 2026/
│       └── (board / principal meeting minutes by date)
├── principals/
│   ├── domain-principal-record.md
│   ├── governance-principal-record.md
│   ├── ops-principal-record.md                  ← TBD per Phase A third-principal naming
│   └── (subsequent principal additions or transitions)
├── treasury/
│   ├── mint-events.md                           ← every founder-mint and DAO-ratified mint
│   ├── treasury-actions.md                      ← categorized cash-out events
│   └── reserve-record.md                        ← reserve balance over time
├── partnerships/
│   ├── (RapidPOS channel-partner license — once executed)
│   ├── (DriftPOS partnership record — once formalized)
│   └── (subsequent partnership records)
├── compliance/
│   ├── pci-scope-position.md                    ← maintained by compliance-architecture lead
│   ├── iso27001-readiness.md
│   ├── iso27001-stage1-audit-record.md          ← when audit completes
│   ├── iso27001-stage2-observation-record.md
│   ├── iso27001-certificate.md                  ← when issued
│   ├── soc2-observation.md
│   └── (subsequent attestations and surveillance audit records)
└── corp-archives/
    └── (inbound documents that become governance reference — counsel opinions, audit work papers, regulatory correspondence)
```

## How the vault populates

The vault is empty at constitution except for the white paper and Declaration 1. It populates over time as governance acts occur, each inscribed at its block of occurrence and recorded in the vault as the orientation copy.

| Vault path | Populated by | Trigger |
| --- | --- | --- |
| `white-paper/` | Founder + DAO ratification | Genesis-block inscription event |
| `declarations/` | Founder + DAO ratification | Constitutional acts (founding, annexation, namespace spawn, dissolution) |
| `bylaws/v1-ratified-...md` | Bylaws skill output (`~/GrowDirect/outputs/crb-skills/namespace-bylaws/templates/bylaws-document.md` filled in for the namespace) | Genesis-block inscription event |
| `bylaws/amendments/` | Amendment-proposal artifacts produced through the iteration loop | Each ratified amendment |
| `minutes/` | Secretary (initially human; per addendum, transitions to agentic) | Each board / principal meeting |
| `principals/` | Each principal at appointment | Each principal addition or transition |
| `treasury/mint-events.md` | Smart-contract emission, plus orientation copy | Each mint event (founder-mint or DAO-ratified) |
| `treasury/treasury-actions.md` | Smart-contract emission, plus orientation copy | Each treasury action above auto-execute threshold |
| `partnerships/` | Counterparty-signed agreement, plus orientation copy | Each executed partnership |
| `compliance/` | Compliance-architecture lead | Each scoping document, audit milestone, attestation |
| `corp-archives/` | Inbound | Each external document becoming governance reference |

## Authoritative source

The on-chain inscription is the authoritative version of every constitutional document. The on-disk version in this vault is the orientation copy — readable, navigable, indexable — but where the on-disk version differs from the on-chain inscription, the on-chain inscription prevails. Every document in this vault carries its inscription txid and content hash in its frontmatter; verifying the on-disk version against the inscription is a deterministic operation any party with a node can perform.

## Relationship to other GrowDirect-platform vaults

| Vault | Holds | Relationship to this vault |
| --- | --- | --- |
| `~/GrowDirect/` | Platform code, R&D, skills, Brain wiki, prior research | Produces the tools whose outputs populate this vault |
| `~/GrowDirect/Cove/` | Cove proposal-engine application + WPBCA HOA governance records | Reference proposal-engine implementation; per company-formation epic dispatch C6, integrates with this vault's substrate via APIs and smart-contract reads/writes |
| `~/GrowDirect/Brain/` | Curated knowledge, MOCs, project context | Source of substrate research; this vault references but does not duplicate |
| `~/GrowDirect/outputs/` | Wave session deliverables, scoping documents, dispatches | Operational artifacts; constitutional acts they enable populate this vault |

## Migration path (when ready)

When `/Users/gclyle/eljeffe/` is created on the host and granted via `request_cowork_directory`:

```bash
mv /Users/gclyle/GrowDirect/outputs/eljeffe-vault /Users/gclyle/eljeffe
```

The vault contents move cleanly. The `outputs/eljeffe-vault/` path becomes a no-op. Any cross-references in `~/GrowDirect/` that point at vault content should be updated to the new path.

---

*The eljeffe DAO LLC vault. Constituted at the genesis-block inscription event. The substrate begins.*
