---
type: strategy
domain: business
status: active
created: 2026-03-19
updated: 2026-03-19
---
# GrowDirect Production Chain — v0.1
*The map of how the thesis becomes the output.*

**Date:** February 27, 2026
**Owner:** ALX
**Classification:** MAXIMUM CONFIDENTIAL
**Status:** LOCKED v0.1 — Restructure executed Feb 27. manifest.json v3.0 live. Sources renumbered.

---

## The Three Tiers

```
TIER 1: THE MANIFESTO (the thesis)
    │   One document. The master source. The doctrine.
    │   Path: Canary_IP/Markdown/Strategy/GrowDirect_Manifesto_v1.0.md
    │   Owner: ALX on behalf of Jeffe
    │   Rule: Changes here FIRST. Everything downstream rebuilds.
    │
    ▼
TIER 2: THE WAR CHEST SOURCES (the knowledge base)
    │   One file per topic. Each fed by one or more Manifesto sections.
    │   Path: _ALX/WarChest/sources/
    │   Owner: ALX (assembles from agent deliverables)
    │   Rule: Sources update FROM the Manifesto. Never the reverse.
    │
    ▼
TIER 3: THE GOLD BUILD (the minted outputs)
    │   The finished products. Investor site. Briefing pack. Pitch deck. Public site.
    │   Paths: _ALX/WarChest/outputs/ + _ALX/WarChest/site/
    │   Owner: Jess (builds from sources) + ALX (orchestrates)
    │   Rule: Outputs rebuild FROM sources. Test until right. Mint once. Done.
```

---

## Tier 1 → Tier 2 Mapping (Manifesto → War Chest Sources)

Each Manifesto section feeds exactly one War Chest source file. Some source files receive from multiple Manifesto sections.

### FINAL SOURCE NUMBERING (v3.0 — executed Feb 27)

**Spine Sources (00-42):**

| # | Name | Spine | Manifesto | Status |
|---|---|---|---|---|
| `00-the-demo.md` | The Demo | OPEN + ACT 1 | — | 🔴 stub |
| `01-founders-case.md` | The Founder's Case | ACT 2A-2C | I.1-I.3 | 🔴 stub |
| `02-the-pitch.md` | The Pitch | ACT 2D-2E | II.1-II.4 | ✅ written |
| `03-canary.md` | Canary LP | ACT 3A | III.1 | ✅ written |
| `04-the-crdm.md` | The CRDM | ACT 3B | III.2 | ✅ written |
| `05-the-chirp.md` | The Chirp | ACT 3C | III.3 | 🔴 stub |
| `06-the-glog.md` | The gLog | ACT 3D | III.4 | ✅ written |
| `07-compliance.md` | Compliance by Construction | ACT 3E | III.5 | ✅ written |
| `10-the-pool.md` | The Inscription Pool | ACT 4A | IV.1 | 🔴 stub |
| `11-the-notary.md` | The Notarization Service | ACT 4B | IV.2 | 🔴 stub |
| `12-the-gate.md` | The Validation Gate | ACT 4C | IV.3 | 🔴 stub |
| `13-the-scale.md` | The Scaling Model | ACT 4D | IV.4 | 🔴 stub |
| `14-the-mining-moat.md` | Block Space as Write Access | ACT 4E | IV.5 | 🔴 stub |
| `15-the-network.md` | The Network Effect | ACT 4F | IV.6 | 🔴 stub |
| `16-the-vision.md` | The Vision | ACT 4G | IV.7 | 🔴 stub |
| `20-six-nodes.md` | Six-Node Architecture | ACT 5A | V.1 | ✅ written |
| `21-triple-subscriber.md` | Triple Subscriber Pipeline | ACT 5B | V.2 | 🔴 stub |
| `22-the-pipe.md` | The Protocol Pipe | ACT 5C | V.4 | 🔴 stub |
| `23-the-l402.md` | The L402 Gate | ACT 5D | V.5 | 🔴 stub |
| `30-first-mover.md` | First Mover | ACT 6A | VI.1 | ✅ written |
| `31-genesis-pool.md` | The Genesis Pool | ACT 6B | VI.2 | 🔴 stub |
| `32-fee-window.md` | The Fee Window | ACT 6C | VI.3 | 🔴 stub |
| `33-the-patent.md` | The Patent | ACT 6D | VI.4 | 🔴 stub |
| `35-the-market.md` | The Market | ACT 7A | VII.1-VII.2 | ✅ written |
| `36-revenue.md` | Revenue Model | ACT 7B | VII.3 | ✅ written |
| `37-projections.md` | Three-Year Projections | ACT 7C | VII.4 | 🔴 stub |
| `38-the-rollout.md` | The Rollout | ACT 7D | VII.5 | 🔴 stub |
| `40-the-ask.md` | The Ask | ACT 8A-8C | VIII.1-VIII.3 | 🔴 gap (ISS-002) |
| `41-why-now.md` | Why Now | ACT 8D | VIII.4 | 🔴 stub |
| `42-sovereignty.md` | Sovereignty | CLOSE | — | 🔴 stub |

**Supporting Detail (45-53):**

| # | Name | Detail For | Status |
|---|---|---|---|
| `45-the-fox.md` | The Fox | 03-canary, 05-the-chirp | ✅ written |
| `46-the-goose.md` | The Goose | 12-the-gate | ✅ written |
| `47-the-owl.md` | The Owl | 04-the-crdm | ✅ written |
| `48-investment-thesis.md` | Investment Thesis | 01-founders-case, 06-the-glog | ✅ written |
| `49-how-we-build.md` | How We Build | internal | ✅ written |
| `50-the-team.md` | The Team | standalone | ✅ written |
| `51-the-article.md` | The Article | press | ✅ written |
| `52-the-economy-legacy.html` | Economy (Legacy) | being split into 10-16 | ⬜ legacy |
| `53-the-product.html` | Product Prototype | standalone | ✅ written |

**Utility (90-93):**

| # | Name | Status |
|---|---|---|
| `90-disclaimer.md` | Legal disclaimers | ✅ |
| `91-changelog.md` | Version history | ✅ |
| `92-issues.md` | Known gaps + issues | ✅ |
| `93-references.md` | Bibliography | ✅ |

---

## Tier 2 → Tier 3 Mapping (Sources → Gold Build Outputs)

| Output | What It Is | Sources It Pulls | Status |
|---|---|---|---|
| **Investor Site** | Single-page scrolling narrative. Password-gated. The "read this before we meet" package. | All investor-tagged sources | v3.0 delivered. Syd sign-off pending. |
| **Briefing Pack** | Multi-page site. Full catalog. Deep dives. The "due diligence" package. | All sources | v0.6 on disk |
| **Pitch Deck** | Presentation. The live demo companion. Follows the Spine. | Spine-mapped sources only | 🔴 NOT YET BUILT |
| **Public Site** | growdirect.io. No gate. Public-safe only. | Public-tagged sources only | v0.1 parked |

---

## The Production Flow (step by step)

```
1. JEFFE SPEAKS or AGENT DELIVERS
   └─ Raw input: conversation, decision, research, analysis

2. ALX UPDATES THE MANIFESTO
   └─ Right section. Right status. Manifesto tag noted.

3. ALX UPDATES THE WAR CHEST SOURCE
   └─ The source file that maps to that Manifesto section.
   └─ Source is investor-readable prose. Not internal notes.

4. JESS REBUILDS THE OUTPUT
   └─ Which output? Check the "feeds" tag in manifest.json.
   └─ Test build. Review. Fix. Test again.

5. SYD SIGNS OFF (if investor-facing)
   └─ Legal review. Approved language. No unapproved claims.

6. GOLD BUILD — MINT
   └─ Version locked. Archived. Deployed.
   └─ The output is canonical. It does not change.
   └─ Next change = next version = next mint.
```

---

## What's Missing (gaps to fill, in order)

| Priority | Gap | What It Needs | Blocked By |
|---|---|---|---|
| 1 | `00-founders-case.md` | Manifesto I.1-I.3 prose → investor-grade source | B-056 (evidence hunt) for completion, but draft can proceed |
| 2 | `00-the-demo.md` | The live demo script. What happens on screen. What Jeffe says. | Sprint 6 Track 1 (protocol pipe must work) |
| 3 | `17-the-ask.md` | Round structure, proceeds, milestones | ISS-002 — Jeffe input |
| 4 | `18-sovereignty.md` | The Close. SMS → URL → rehydrate. DR thesis. | Needs writing — no blocker |
| 5 | Pitch Deck (Tier 3) | The presentation file. Follows the Spine. | All Tier 2 sources must be ready |
| 6 | Layers 4-7 in `02-the-economy.html` | Business model layers not yet in War Chest format | Manifesto IV is written — just needs source conversion |

---

## Naming Cleanup — EXECUTED

Full renumber executed Feb 27, 2026. All sources renumbered to match Spine order. Old sources archived to `sources_v2_archive/`. manifest.json updated to v3.0. See FINAL SOURCE NUMBERING table above.

---

## Rules (for every session, every agent)

1. **Manifesto first.** If the thinking changed, the Manifesto changes before anything else.
2. **Sources second.** The War Chest source updates from the Manifesto. Never the reverse.
3. **Outputs third.** Outputs rebuild from sources. Never from raw inputs.
4. **One thing at a time.** Update one Manifesto section. Update its source. Test the output. Confirm. Move on.
5. **Test before mint.** Every output gets test builds. Gold Build = version locked, archived, deployed. No edits after mint.
6. **Syd before distribution.** Nothing investor-facing ships without Syd sign-off.

---

*Production Chain v0.1 — LOCKED Feb 27, 2026*
*Restructure executed. Sources renumbered. manifest.json v3.0 live.*
*Old sources preserved in `sources_v2_archive/` until v3.0 outputs confirmed.*
