---
date: 2026-04-22
type: wiki
tags: [growdirect, warchest, crdm, data-model, retail-lp]
sources:
  - docs/_archive/ip-vault/warchest/sources/04-the-crdm.md
last-compiled: 2026-04-22
needs-review: 2026-05-06
---

**Wiki:** [[Brain/Home|Home]]

# The Data Model

> *"Our soil is our data model, built at enterprise scale, time-tested, hundreds of billions of rows processed, billions saved."*

---

## The CRDM — Canary Retail Data Model

The CRDM is not invented. It descends from a proven enterprise loss prevention data architecture that processed hundreds of billions of rows across the world's largest retailers. Three generations of the same canonical schema pattern, refined across decades of real-world deployment.

### Provenance

| Generation | System | Deployed At | Era |
|---|---|---|---|
| **TDS (Till Data Store)** | Bidirectional data store for register configuration, items, price files, and enterprise-to-store metadata | Tesco worldwide | 2000s |
| **SMART System** | Canonical abstraction layer for aggressive retail acquisition and consolidation across international markets | Walmart International (Central/South America) | 2010s |
| **CRDM** | Third-generation canonical schema targeting Square SMB merchants | Canary LP | 2026 |

The orchestration layer that fed TDS was RTI (Real Time Integrator) — a lightweight Windows service agent for real-time data movement deployed across Tesco worldwide, Ross Stores, and Delta Airlines. RTI is the direct ancestor of Canary's webhook listeners and polling workers.

---

## Seven Canonical Data Sources

These are the seven data domains that feed any retail LP platform. They were defined in an enterprise LP data specification that the founder reviewed and signed off on. Every new POS integration must map to these same seven sources.

| # | Source | What It Is | Key LP Signals |
|---|---|---|---|
| 1 | **Transaction Header** | One record per POS transaction. The backbone. | Voids, cancels, transaction velocity |
| 2 | **Tender / Payment** | How the customer paid — cash, card, crypto, gift card | Split tenders, unusual payment mixes |
| 3 | **Line Items** | Every item in every basket | Sweethearting, selective scanning, quantity manipulation |
| 4 | **Employee & Timecards** | Who was on the clock, what they touched | After-hours activity, refund velocity by employee |
| 5 | **Product / Article** | Item master — what's in the store | Inventory ghosts, high-shrinkage items |
| 6 | **Store / Location** | Where transactions happen | Cross-location patterns, geographic fraud clusters |
| 7 | **Customer** | Who's buying — loyalty, returns history | Return fraud rings, organized retail crime |

### Coverage Analysis

The CRDM maps every enterprise ancestor field to a Canary column with explicit gap analysis. Current Square API coverage:

| Source | Fields Mapped | Coverage |
|---|---|---|
| Transaction Header | 18 of 28 | 64% |
| Tender / Payment | 10 of 13 | 77% |
| Line Items | 14 of 21 | 67% |
| Employee + Timecards | 9 of 10 + 4 new | 90%+ |
| Product / Article | 7 of 11 | 64% |
| Store / Location | 12 of 17 | 71% |
| Customer | 3 of 7 | 43% |

The gap analysis guides the roadmap: each missing field is a specific API call or webhook expansion.

---

## The Evidence Chain

The CRDM enforces three tiers of data integrity:

### Tier 1: Financial Ledger (Append-Only)
Transactions, refund links, cash drawer events, gift card activities. No UPDATE. No DELETE. Financial data is a ledger — you don't erase entries.

### Tier 2: Evidentiary (Insert-Only)
Case evidence, evidence access logs, case timelines. Enforced by database triggers. If the platform accuses someone, the evidence chain must be unbroken.

### Tier 3: Audit Trail (Hash-Chained)
Every audit log entry includes the SHA-256 hash of the previous entry. Tamper with one record, the chain breaks downstream. The same principle that secures Bitcoin secures the Canary audit trail.

---

## Chirp Detection Registry

The CRDM powers the Chirp detection engine — 22 rules that watch for loss patterns across the seven canonical data sources:

| Category | Example Chirps |
|---|---|
| **Refund anomalies** | Excessive refunds, refund-without-sale, refund velocity spikes |
| **Void patterns** | Post-sale voids, void-after-cash, high void ratios |
| **Cash handling** | Cash drawer opened without sale, excessive no-sales |
| **Employee behavior** | After-hours transactions, discount abuse, timecard anomalies |
| **Inventory** | Ghost items, receiving discrepancies, high-shrinkage SKUs |
| **Payment** | Split tender manipulation, gift card laundering |

Every Chirp rule traces to specific CRDM fields. When a new POS integration maps to the canonical schema, all 22 detection rules work automatically.

---

## Why It Matters

The data model is the soil. The detection engine, analytics, and Bitcoin inscription all grow from it.

- **Enterprise lineage** means the schema handles edge cases that SMB tools have never seen
- **POS-agnostic design** means adding a new POS integration is a parser, not a rewrite
- **Immutability tiers** mean the evidence chain is as strong as the architecture allows
- **Bitcoin anchoring** means the gLog inscription pipeline reads directly from the CRDM evidence store

The founder built this schema once for the largest retailers on earth. This is the third generation — refined, battle-tested, and now Bitcoin-native.

---

*GrowDirect Confidential*
*Patent Pending — Provisional 63/991,596*

## Related

- [[Brain/projects/GrowDirect|GrowDirect MOC]]
- [[Brain/wiki/growdirect-working-papers|Working Papers Structure]]

## Sources

- `docs/_archive/ip-vault/warchest/sources/04-the-crdm.md` — the war-chest source this card summarizes
