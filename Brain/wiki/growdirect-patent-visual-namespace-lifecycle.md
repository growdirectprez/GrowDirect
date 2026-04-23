---
date: 2026-04-22
type: wiki
tags: [growdirect, patent-visuals, patent, namespace, raas, lifecycle]
sources:
  - docs/_archive/ip-vault/patent-visuals/Patent_Namespace_Lifecycle_v1.0.html
last-compiled: 2026-04-22
needs-review: 2026-05-06
---

**Wiki:** [[Brain/Home|Home]]

# Patent Schematic — Namespace Lifecycle v1.0 (FIG. 5)

Rendered SVG schematic filed as **FIG. 5** in Patent Application 63/991,596. Version 1.0.

## What the Figure Depicts

The lifecycle of a namespace entry in the Registration-as-a-Service (RaaS) model:

1. **Register** — an entity (merchant, transaction, alert, case) requests a namespace slot
2. **Mint** — the system issues a RaaS UUID, an Ordinal inscription, and a Lightning wallet address
3. **Seed** — the wallet is funded with satoshis to drive internal plumbing (L402-gated tool dispatch, MCP metering)
4. **Transact** — every subsequent action against the entry is paid via Lightning from its wallet
5. **Renew / Retire** — the wallet can be topped up or the namespace can sunset

## Why It Matters

This figure supports patent claims for **metered micro-payment dispatch** and **DOME** (L402-gated DAO) architecture. Every namespace entry becomes a self-funding economic unit — a Lightning wallet with an Ordinal identity — rather than a row in a database.

The lifecycle is the visual proof of the tokenomics model: subscriptions fund a liquidity pool, which seeds namespace wallets, which pay for internal services via L402. No central billing. No intermediary. The namespace *is* the account.

## Related

- [[Brain/projects/GrowDirect|GrowDirect MOC]]
- [[Brain/wiki/growdirect-working-papers|Working Papers Structure]]
- [[Brain/wiki/growdirect-the-l402|The L402]] — Lightning-native paywall
- [[Brain/wiki/growdirect-the-gate|The Gate]] — L402 licensing enforcement
- [[Brain/wiki/growdirect-genesis-pool|The Genesis Pool]] — seed funding
- [[Brain/wiki/growdirect-the-patent|The Patent]] — IP strategy

## Sources

- `docs/_archive/ip-vault/patent-visuals/Patent_Namespace_Lifecycle_v1.0.html` — the rendered SVG schematic
