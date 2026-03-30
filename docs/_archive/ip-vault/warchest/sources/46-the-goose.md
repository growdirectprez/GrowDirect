---
type: pitch
domain: goose
status: active
created: 2026-03-18
updated: 2026-03-19
---
# The Goose — Bitcoin Money Machine

> "Lays golden sats while you sleep — zero fees, zero middlemen, all yours."

---

## Overview

The Goose is Canary's crypto commerce module — a self-hosted BTCPay Server integration that plugs directly into Square's ecosystem. It lets merchants accept Bitcoin and Lightning Network payments with instant settlement, zero chargebacks, and fees that make Visa look like a loan shark.

Square rolled out Lightning support in late 2025. The Goose turns that into a turnkey product for the 4M+ merchants already on the platform — no crypto expertise required. Scan a QR, receive sats, auto-convert to USD or stack BTC. The merchant doesn't need to understand Lightning any more than they understand Visa's interchange network.

The hidden layer: a silent micro-fee engine on Lightning swaps (0.1% arbitrage on conversions) that generates revenue for GrowDirect without friction. The Goose lays golden eggs while the merchant sleeps.

---

## Core Features

### Lightning Integration
- BTCPay Server fork, self-hosted or cloud-hosted (Voltage-style deployment)
- Zero processing fees through end of 2026, then 1% max (vs. 2.6% + $0.10 on Square card processing)
- Instant settlement finality — no 2-day ACH wait, no chargebacks, no disputes

### Square Bridge
- Hooks into Square POS for seamless fiat/crypto toggle at the register
- Customer scans QR code, pays in sats — merchant receives BTC or USD via auto-conversion
- Unified reporting: crypto and fiat transactions appear in the same Canary dashboard
- Multi-location support: franchise HQ sees aggregate crypto flow across all stores

### Hidden App Layer
- Silent micro-fees on Lightning swap conversions (0.1% arbitrage spread)
- Revenue generation without merchant-facing friction
- Feeds into Owl for predictive yield optimization (e.g., "charge 0.5% on high-risk transactions")

### Wallet Agnostic
- Works with Muun, Phoenix, Wallet of Satoshi, Strike, Cash App — any Lightning-compatible wallet
- Keeps it retail-friendly: no wallet lock-in, no custodial requirements
- Bitkey (Block's self-custody wallet) integration for merchants who want to hold their own keys

### Fraud Shield
- Ties into Owl for real-time anomaly detection on crypto transactions
- Flags refund loops, wash trading, Lightning spam, and suspicious conversion patterns
- Cross-references with Canary's existing RefundRadar for unified fraud view

---

## Why It Wins

- **Square's 4M+ merchants** just got BTC payment capability — The Goose is the product that makes it usable
- **You own the stack** — no Coinbase, no Stripe, no third-party custodian taking a cut
- **Sound money rails** — Austrian economics in practice: zero inflation tax, instant settlement, cryptographic proof
- **De minimis tax exemption** — Block's legislative push for tax-free BTC transactions under $200 makes everyday Bitcoin payments practical
- **Franchise multiplier** — one corporate Goose deployment cascades to every franchisee location

---

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Flask + Celery for async Lightning node management |
| Lightning | LND or c-lightning backend |
| Caching | Redis for mempool and channel state |
| Auth | RBAC from Canary — admin sees sats flow, clerks see USD totals |
| Database | PostgreSQL time-series for transaction history |
| API | RESTful v1 endpoints, webhook-driven event processing |

---

## Roadmap

| Phase | Timeline | Deliverables |
|---|---|---|
| **Alpha** | Q1 2026 | Beta with 10 Square merchants, BTCPay fork deployed, basic Lightning receive |
| **Beta** | Q2 2026 | Full Square API integration, auto-conversion (BTC ↔ USD), multi-location support |
| **v1.0** | Q3 2026 | Owl feed for predictive yield, franchise rollout, micro-fee engine live |
| **v1.5** | Q4 2026 | Bitkey integration, cross-border payments, advanced treasury management |

---

## Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Regulatory scrutiny on Lightning | Self-hosted BTCPay = non-custodial, merchant controls keys. Block's CLARITY Act lobbying provides regulatory cover |
| BTC volatility | Auto-conversion to USD at point of sale. Merchants choose: hold BTC, convert instantly, or split |
| Square API changes | Abstract Square integration behind adapter layer. Goose works with or without Square bridge |
| Money transmitter classification | Non-custodial architecture means GrowDirect never holds merchant funds. Legal review required per jurisdiction |

---

## Integration Points

| Module | How Goose Connects |
|---|---|
| **Canary** | Crypto transactions flow through RefundRadar. Shared RBAC, shared dashboard |
| **Owl** | Feeds Lightning transaction data for analytics. Receives risk scores for dynamic fee adjustment |
| **Fox** | Crypto fraud cases auto-created when Goose detects wash trading or suspicious patterns |

---

*Version: 1.0 — February 2026*
*GrowDirect Confidential*
