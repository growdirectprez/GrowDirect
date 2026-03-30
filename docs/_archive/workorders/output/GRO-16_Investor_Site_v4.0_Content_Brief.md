---
type: workorder
domain: business
status: active
created: 2026-03-18
updated: 2026-03-19
---
# GRO-16 — Investor Site v4.0 Content Brief

**Issue:** GRO-16 (B-058)
**Prepared By:** ALX (Chief of Staff)
**Date:** March 2, 2026
**Classification:** MAXIMUM CONFIDENTIAL — Investor Materials
**Gate:** Jess builds v4.0 from this brief. Syd does final content sign-off.
**Done When:** Content brief complete, Jess has spec to build against, Syd reviews for legal.
**Scope:** Content direction + structural changes. No code.

---

## 1. What Changed Since v3.0

The RaaS strategic reframe (GRO-13, March 1–2, 2026) fundamentally shifts GrowDirect's investor positioning. The v3.0 site leads with "Universal Event Notarization" — the protocol layer. v4.0 leads with the business model that the protocol enables: Receipt-as-a-Service.

**The pitch evolution:**

| | v3.0 (Current) | v4.0 (This Brief) |
|---|---|---|
| **Hero lead** | "Universal Event Notarization" | "Any POS. Any Merchant. One API Call." |
| **Product frame** | Canary LP (loss prevention for Square) | Canary LP = beachhead; RaaS = the business |
| **Revenue story** | Subscription + validation sats | Subscription + Validation + RaaS API + Namespace fees |
| **TAM frame** | Square merchants (4M) + $4.7B POS TAM | All POS ($4.5T global retail transactions) |
| **Moat story** | Key custody + historical accumulation | First-mover on verified receipt standard + .jeffe namespace |
| **Architecture** | 6-node pipeline (internal) | Pipeline + RaaS API layer (external-facing) |

> "RaaS. Receipt-as-a-Service. Anyone can hit this service and we will return the receipt."
> — Jeffe, March 1, 2026

---

## 2. Section-by-Section Changes

### 2.1 Gate — NO CHANGE

Keep password gate as-is. Same aesthetic. Same confidentiality framing.

### 2.2 Nav — UPDATE

**Current:** Problem · Solution · Economy · Thesis · Market · Vision · Built

**v4.0:** Problem · Solution · **RaaS** · Economy · Thesis · Market · Vision · Built

Add "RaaS" as a new nav item between Solution and Economy. This is the new centerpiece section.

### 2.3 Hero — MAJOR REWRITE

**Current hero:**
- Eyebrow: "Universal Event Notarization"
- Title: GROWDIRECT
- Sub: "The minter. The time chain. The boss."
- Body: "Every event that matters leaves a record..."
- Stats: 17+ Years Bitcoin Uptime / 0 Minutes Downtime / ∞ Permanence / 0 Trust Required

**v4.0 hero:**
- Eyebrow: "Receipt-as-a-Service"
- Title: GROWDIRECT
- Sub: "Any POS. Any merchant. One API call."
- Body: "Every retail receipt verified against Bitcoin. One sat per verification. Square today. Every POS tomorrow. The first universal receipt verification standard."
- Stats: Keep "17+ Years Bitcoin Uptime" and "0 Trust Required". Replace other two:
  - **1 sat** / Per Verification
  - **$4.5T** / Global Retail TAM
- Patent badge: Keep as-is

**Design note for Art:** The hero needs to feel bigger — this is now a platform story, not just a protocol story. Consider whether the hero background should subtly show the POS integration map (Square, Clover, Toast, Shopify, Lightspeed converging to one point).

### 2.4 Problem (01) — EXPAND

**Current:** "The Record Is Broken" — 3 cards (Polling Gaps, Mutable Records, Trust Required)

**v4.0:** "The Record Is Broken" — 4 cards. Add a fourth card:

**New card: Fragmented Verification**
- Icon: 🔗 (or appropriate)
- Title: "Fragmented Verification"
- Body: "Every POS system is an island. Clover can't verify Square receipts. Toast can't verify Shopify orders. There is no universal standard for proving a transaction happened. Auditors, insurers, and regulators must contact each POS vendor separately — if they can access records at all."

This sets up the RaaS solution: one API that verifies any POS receipt.

### 2.5 Solution (02) — LIGHT UPDATE

**Current:** "Capture. Seal. Inscribe." — 3 steps + 6-node pipeline + 4 moat cards

**v4.0 changes:**
- Steps 1–3: Keep as-is. The core pipeline story doesn't change.
- 6-node pipeline: Keep as-is.
- **Add below pipeline:** A new "RaaS API" callout box:

```
┌─────────────────────────────────────────────┐
│  "ONE API. ONE SAT. VERIFIED."              │
│                                              │
│  POST /verify → 402 → Pay 1 sat → 200 OK   │
│  { "verified": true, "block": 884201 }      │
│                                              │
│  Any POS. Any integrator. One endpoint.      │
└─────────────────────────────────────────────┘
```

This is the bridge between "how the protocol works" (Section 02) and "who uses it" (new Section 02b).

- 4 moat cards: Update **Network Effects** card text to reference RaaS specifically:
  - **Current:** "More events mean more inscriptions mean more validation revenue..."
  - **v4.0:** "Every RaaS API call deepens the moat. Every POS integrator who connects adds nodes to the network. Every verification compounds the canonical record's authority. At 10,000+ merchants across multiple POS platforms, RaaS revenue overtakes subscription revenue."

### 2.6 RaaS (NEW SECTION — 02b)

**This is the new centerpiece section.** Insert between Solution (02) and Economy (03).

**Section label:** 02b — The Business Model
**Section title:** Receipt-as-a-Service
**Section intro:** "Canary LP is the beachhead. elJeffe is the protocol. RaaS is the product every POS integrator buys."

**Content blocks:**

**Block 1: The API Surface (code-style display)**

Show the two core endpoints in a dark code block — same aesthetic as the v3.0 pipeline diagram but rendered as API spec:

```
POST /v1/verify
→ 402 Payment Required (1 sat)
→ { "verified": true, "block": 884201, "namespace": "sunrise-coffee.jeffe" }

GET /v1/receipt/sunrise-coffee.jeffe
→ Full receipt history with Merkle proofs
→ Paginated. Permanent. Mathematically verifiable.
```

**Block 2: Who Calls This API (5 audience cards, grid layout)**

| Audience | Icon | Hook |
|----------|------|------|
| POS Integrators | 🔌 | "Clover, Toast, Shopify, Lightspeed. They don't build a blockchain layer. They hit our API." |
| Auditors | 📋 | "One API call per receipt. No special software. No blockchain expertise." |
| Insurance | 🛡 | "Claims substantiated in seconds. Absent or inconsistent records flagged instantly." |
| Regulators | ⚖️ | "Tax authority audit = cross-reference the inscription record. Permanent. Mathematical." |
| SaaS Platforms | 🧩 | "'Verified by elJeffe' becomes a trust badge. Each verification generates protocol revenue." |

**Block 3: Three-Tier Service Architecture**

Visual comparison table (same aesthetic as v3.0 market-grid):

| | Free | Standard | Enterprise |
|---|---|---|---|
| **Domain** | eljeffe.org | eljeffe.io | eljeffe.io |
| **Auth** | API key | L402 Lightning | L402 + SLA |
| **Hash Chain** | Postgres only | Postgres + Merkle | Postgres + Merkle + Avalanche |
| **Inscription** | None | Bitcoin Ordinal | Bitcoin + Avalanche dual-anchor |
| **Price** | $0 | 1 sat / verification | Custom |

**Block 4: Unit Economics (stats row, same style as v3.0 build-row)**

| Stat | Label |
|------|-------|
| 1 sat | Per Verification |
| $0.00085 | Revenue Per Call (at $85K BTC) |
| $310K+ | Annual Revenue at 1M Calls/Day |
| $0 | Marginal Cost (Infrastructure Already Exists) |

**Block 5: Integration Priority (POS map)**

Visual showing POS systems converging to one API:

| POS | Market Share | Status |
|-----|-------------|--------|
| Square | 30% SMB | Done (Phase 1) |
| Clover | 25% SMB | Next |
| Toast | 15% Restaurant | Next |
| Shopify POS | 10% Retail | Planned |
| Lightspeed | 8% Multi-vertical | Planned |

**Design note for Art:** This section needs a hero diagram — a visual showing multiple POS systems on the left, all flowing through one "RaaS API" gateway in the center, and Bitcoin on the right. The message is convergence: many inputs, one standard, one permanent record.

### 2.7 Economy (03) — UPDATE

**Current:** "Closed Loop. Perpetual." — Loop diagram + 4 ownership tiers

**v4.0 changes:**
- Loop diagram: **Add RaaS revenue as a fifth arc label or as an annotation** showing external revenue flowing into the loop. Currently the diagram shows Treasury → Mint → Contract → Revenue in a closed loop. RaaS revenue is external — it enters from outside the loop (POS integrators, auditors, etc.). This is important: it shows the loop is not just self-referential but also attracts external capital.
- Ownership tiers: Keep as-is. The 4 levels still apply.
- **Add below tiers:** Revenue stream breakdown card:

```
Four Revenue Streams (Additive)

1. Subscription    → Canary LP merchants. Monthly SaaS.
2. Validation      → Anyone querying past inscriptions. Continues after churn.
3. RaaS API        → External POS integrators and third parties. New stream. Zero additional infrastructure.
4. Namespace       → Annual .jeffe name registration fees.

Key: Streams 2–4 generate revenue from infrastructure that already exists.
```

### 2.8 Thesis (03b) — EXPAND

**Current:** "From tLog to gLog" — founder story + architecture comparison + compliance

**v4.0 changes:**
- Keep the tLog → gLog narrative. It's powerful and doesn't change.
- **Add after the gLog Inscription Pipeline diagram:** A new "From gLog to RaaS" bridge:

"The gLog makes the record permanent. RaaS makes the record accessible. Any POS integrator, auditor, insurer, or regulator can verify any receipt with one API call. The gLog is the infrastructure. RaaS is the business that runs on it."

- Keep compliance by architecture card as-is.
- Keep career arc as-is.

### 2.9 Market (04) — MAJOR EXPAND

**Current:** "The Beachhead" — 3 stats (4M Square, $132B shrinkage, $4.7B POS TAM) + competitor comparison

**v4.0 changes:**
- **Reframe the section title:** "The Beachhead — and Everything After"
- **Update stats grid:** Change from 3 to 4 stats:

| Stat | Label | Sub |
|------|-------|-----|
| 4M+ | Square Merchants | Beachhead. Zero LP tools on marketplace. Done. |
| $4.5T | Global Retail Transactions | Every POS. Every merchant. The full TAM. |
| $132B | Annual U.S. Shrinkage | The problem that opens the door. |
| 6 | POS Platforms in Pipeline | Square (done) → Clover → Toast → Shopify → Lightspeed → standalone |

- Competitor comparison: **Keep but add a third column** — "RaaS Advantage":
  - Enterprise incumbents: no universal API, no cross-POS verification
  - Canary advantage: keep as-is
  - **RaaS advantage:** "Not competing with LP tools. Competing with the absence of a standard. First-mover on universal receipt verification. No incumbent because no one has built this."

### 2.10 Vision (05) — LIGHT UPDATE

**Current:** 6 use cases (Retail, Healthcare, Supply Chain, Legal, Creative Rights, Government)

**v4.0:** Keep all 6. Add context that RaaS is the delivery mechanism for all verticals — the API is the same regardless of whether the event is a retail receipt, a prescription record, or a custody handoff. Schema-agnostic by design.

Update the section intro:
- **Current:** "Every industry where events matter and records can be disputed."
- **v4.0:** "RaaS is not limited to retail. Any industry where events matter and records can be disputed. Same API. Same sat. Same permanence."

### 2.11 Built (06) — UPDATE STATS

**Current stats:** 536 tests / 0 failures / 22 immutability triggers / 9 patent claims

**v4.0 stats:** Update to current numbers (Jeremy to provide latest test count). Add:
- **RaaS API endpoints:** 3 (verify, receipt history, namespace resolution)
- **.jeffe namespace:** Live

Keep the checklist items. Add new items:
- ✓ RaaS API design — `POST /v1/verify`, `GET /v1/receipt/{name}`, `GET /v1/resolve/{name}`
- ✓ CRDM v1.1 amendment — POS-agnostic entity model (external_identities table)
- ✓ .jeffe namespace architecture — NameRegistry contract spec complete
- ✓ Three-tier service architecture — Free (eljeffe.org) / Standard (eljeffe.io) / Enterprise

### 2.12 Closing — UPDATE QUOTE

**Current:** "If it really happened, then you should be able to prove exactly when — without a doubt."

**v4.0 options for Jess to evaluate:**
- Option A (keep current): Still powerful. Still relevant.
- Option B (RaaS-forward): "Any POS. Any merchant. One API call. One sat. One truth."
- Option C (hybrid): Keep current quote, add a second line below: "Now anyone can verify it."

**Recommendation:** Option A stays. The closing should be timeless, not product-specific.

---

## 3. Design System Notes for Art

### Preserve from v3.0
- Dark theme (#0D0D0D base, #141414 card, #1A1A1A dim)
- BTC orange (#F7931A) / Gold (#FBBF24) / Green (#22C55E) palette
- Federal intaglio watermark pattern (background SVG)
- Font stack: Bebas Neue / DM Sans / DM Serif Display / Space Mono
- Password gate aesthetic
- Animated SVG loop diagram
- Code-block aesthetic for technical content

### New for v4.0
- **RaaS section needs its own visual identity** within the existing system. Suggestion: a subtle gradient shift — the section background could use a very faint BTC orange tint instead of the neutral dim, signaling "this is the new thing"
- **POS convergence diagram:** SVG showing 5+ POS logos converging to a single RaaS API endpoint. Same node/circle aesthetic as the 6-node pipeline.
- **API code blocks:** Monospace code rendering for the endpoint specs. Same Space Mono + dark card aesthetic.
- **Revenue stream visual:** Consider a stacked/additive diagram showing subscription as the base, then validation, RaaS, and namespace stacking on top. Shows how revenue compounds.

---

## 4. Content Do-Not-Change List

These elements are locked and should not be altered without Syd sign-off:

1. Patent reference: 63/991,596 · Filed February 26, 2026
2. Forward-looking statement disclaimer
3. Genesis Pool: 10,000,000 from founder's 0.1 BTC F2Pool mining reward
4. "Strictly Confidential" / "Private Distribution Only" language
5. Founder career arc (Big Four → IBM Systems → SaaS Pioneer → Bitcoin-Native)
6. tLog → gLog narrative and comparison diagram

---

## 5. New Content Requiring Syd Review

Before publishing, Syd must review and clear:

1. **RaaS regulatory positioning:** The site now explicitly describes "Receipt-as-a-Service" as a product. Syd needs to confirm this doesn't create unintended regulatory obligations (see GRO-13 legal questions L-3, L-5, L-6).
2. **"1 sat per verification" pricing language:** Public disclosure of pricing model. Confirm no issues with Lightning micropayment characterization.
3. **POS integration claims:** We say Square is "Done" and others are "Next" / "Planned." Syd should confirm we're not creating contractual obligations or partnership implications.
4. **TAM expansion to $4.5T:** This is a large number. Need to cite source and ensure it's defensible in investor context.
5. **.jeffe namespace claims:** The site will reference the namespace system. Syd should confirm no trademark issues with the namespace branding.
6. **Three-tier service description:** Publicly describing free/standard/enterprise tiers with domain routing. Confirm no issues.

---

## 6. Routing

| Agent | Action | Deliverable |
|-------|--------|-------------|
| **Jess** | Build v4.0 HTML from this content brief | `growdirect_investor_v4.0.html` |
| **Art** | Design new RaaS section, POS convergence diagram, revenue stream visual, updated hero background | Design mockups |
| **Syd** | Review 6 new content items flagged in Section 5 | Legal clearance memo |
| **Tom** | Provide latest test counts and any new "Built" items for Section 06 | Updated metrics |
| **Will** | Align LEO playbook messaging with new hero language | Playbook update |

---

*ALX | GRO-16 | March 2, 2026*
*MAXIMUM CONFIDENTIAL*
