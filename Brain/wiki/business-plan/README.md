---
type: index
domain: business-plan
status: active
last-updated: 2026-05-05
last-compiled: 2026-05-05
needs-review: false
confidentiality: Internal only — pre-formation strategic material
---

# Canary Retail — Business Plan & Evidence Package

This directory is the unified business plan and evidence package for Canary Retail / GrowDirect LLC.

**Strictly Confidential. Not for external distribution until founder explicitly authorizes.**

---

## Deck

| File | Audience | Status |
|---|---|---|
| [canary-retail-deck-v1-internal.pptx](deck/canary-retail-deck-v1-internal.pptx) | NDA-gated partnership / investor conversations (names tier-1 retailers) | v1, May 2026 |
| [canary-retail-deck-v1-external.pptx](deck/canary-retail-deck-v1-external.pptx) | External publication — retail archetypes substituted (per feedback_scrub_client_names) | v1, May 2026 |

Deck build script: [deck/build-deck.js](deck/build-deck.js) — regenerate both versions with `node build-deck.js`

Slide source markdown: [deck/source/](deck/source/)

---

## Business Plan Sections (planned — GRO-737, Jeffe-owned)

| Section | Status |
|---|---|
| §1 Vision & thesis | Not started |
| §2 Market | Not started |
| §3 Product & architecture | Backed by canonical-data-model.md + mcp-service-junctions.md |
| §4 Business model | Satoshi cost model — SDD complete, code not started |
| §5 Go-to-market | RapidPOS channel defined; CompanyX GTM TBD |
| §6 Structure & ownership | NewCo formation mechanics TBD |
| §7 Financials | Not started |
| §8 Risks & open questions | Captured in deck slide 11 |

---

## Canonical Evidence Sources

These documents are the authoritative backing for every deck claim:

| Source | Coverage |
|---|---|
| `docs/sdds/go-handoff/canonical-data-model.md` | 65-entity data model, 13-module spine, 9-domain completeness |
| `docs/sdds/go-handoff/mcp-service-junctions.md` | 166 junctions, 10 archetypes |
| `docs/sdds/go-handoff/satoshi-cost-rollup.md` | Six-term cost equation, ILDWAC, L402-OTB |
| `Brain/wiki/cards/platform-thesis.md` v3 | Four accountability rails |
| `Brain/wiki/cards/canary-demand-sensing-smb.md` | Min/Max + Days-of-Supply intelligence layer |

---

## Related Linear Issues

- [GRO-738](https://linear.app/growdirect/issue/GRO-738) — Deck production dispatch (this work)
- [GRO-737](https://linear.app/growdirect/issue/GRO-737) — Business plan document (Jeffe-owned, multi-week)
- [GRO-733](https://linear.app/growdirect/issue/GRO-733) — Cloud architecture + workload SDD
- [GRO-735](https://linear.app/growdirect/issue/GRO-735) — Cloud provider power positioning intelligence
