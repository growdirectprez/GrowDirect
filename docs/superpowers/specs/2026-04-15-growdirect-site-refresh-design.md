---
classification: confidential
owner: GrowDirect LLC
---

# GrowDirect.io Site Package Refresh — Design Spec

**Date:** 2026-04-15
**Status:** Design — approved for planning
**Scope:** Consolidate, update, and package all growdirect.io static site assets

---

## Purpose

Consolidate the scattered growdirect.io site files into a single deployable
package with accurate content that reflects the current state of the codebase
(April 2026), not the manifesto snapshots from February/March 2026.

Key drivers:
- Rule counts wrong everywhere (29 → 37 rules, 8 → 10 categories)
- Pricing section is fiction (3-tier subscriptions → Goose credit system)
- Goose module card describes BTCPay/LNURL-auth (wrong — it's Strike/macaroons)
- Gated investor links point to Brain raw inbox (breaks on deploy)
- Technical Library docs mix accurate content with aspirational claims
- Source assets scattered across repo root, Brain inbox, iCloud archive
- No cohesive deployable package exists

---

## Architecture Decision: `site/` Directory

All deployable static files live in `site/` at the repo root. Cloudflare Pages
(or any static host) points at this directory. No build step required except
one optional Redoc generation for the Swagger spec.

**Why not repo root:** Site files are currently mixed with `Canary/`, `Cove/`,
`Brain/`, etc. A dedicated directory keeps the deployable package separate
from the codebase.

**Why not a build system:** These are standalone HTML files with inline CSS.
A build system adds complexity with no benefit at this scale. Each file is
self-contained and can be opened locally with `file://`.

---

## File Structure

```
site/
├── index.html                              ← growdirect.io hub
├── canary/
│   └── index.html                          ← canary.growdirect.io
├── docs/
│   ├── canary-data-model.html              ← Technical Library
│   ├── canary-platform-architecture.html
│   ├── canary-technical-roadshow.html
│   ├── canary-factory-process.html
│   ├── canary-eljeffe-protocol.html
│   ├── canary-magazine-article.html        ← from iCloud Product_Sites
│   ├── canary-jsonb-forensic.html          ← from iCloud Product_Sites
│   ├── canary-crdm-mapping.html            ← from iCloud Product_Sites
│   ├── canary-fox-spec.html                ← from iCloud Product_Sites
│   ├── canary-api-reference.html           ← generated from Swagger YAML via Redoc
│   └── eljeffe-swagger.yaml                ← OpenAPI 3.0 spec (raw YAML)
├── investor/
│   ├── index.html                          ← investor briefing (manifesto rendered)
│   └── eljeffe.html                        ← orbital diagram (animated SVG)
├── css/
│   └── shared.css                          ← shared variables, nav, footer, gate
└── legal/
    ├── terms.html
    ├── privacy.html
    └── disclaimer.html
```

---

## Source File Mapping

| Destination | Current Location | Action |
|-------------|-----------------|--------|
| `site/index.html` | `growdirect-hub.html` (repo root) | Move + update content |
| `site/canary/index.html` | `canary.growdirect.io.html` (repo root) | Move + update content |
| `site/docs/canary-data-model.html` | `Canary Technical Library/Canary Data Model.html` | Move + rename + update |
| `site/docs/canary-platform-architecture.html` | `Canary Technical Library/Canary Platform Architecture.html` | Move + rename + update |
| `site/docs/canary-technical-roadshow.html` | `Canary Technical Library/Canary Technical Roadshow.html` | Move + rename + update |
| `site/docs/canary-factory-process.html` | `Canary Technical Library/Canary Factory Process.html` | Move + rename + update |
| `site/docs/canary-eljeffe-protocol.html` | `Canary Technical Library/Canary elJeffe Protocol.html` | Move + rename + update |
| `site/docs/canary-magazine-article.html` | iCloud `Product_Sites/Canary_LP_Magazine_Article.html` | Copy in + update |
| `site/docs/canary-jsonb-forensic.html` | iCloud `Product_Sites/Canary_JSONB_Forensic_Analysis_v1.0.html` | Copy in + update |
| `site/docs/canary-crdm-mapping.html` | iCloud `Product_Sites/Canary_CRDM_v2.0.html` | Copy in + update |
| `site/docs/canary-fox-spec.html` | iCloud `Product_Sites/Fox_Module_Technical_Specification_v1.0.html` | Copy in + update |
| `site/docs/eljeffe-swagger.yaml` | iCloud `Jeremy_gLog_Swagger_v1.0.yaml` | Copy in + update |
| `site/docs/canary-api-reference.html` | Generated | `npx @redocly/cli build-docs` from YAML |
| `site/investor/index.html` | `Brain/raw/inbox/growdirect_investor.html` | Move + update |
| `site/investor/eljeffe.html` | `Brain/raw/inbox/02-eljeffe-v3.html` | Move |
| `site/css/shared.css` | New | Extract from existing inline styles |
| `site/legal/*.html` | `docs/legal/*.html` | Copy |

---

## Content Updates

### Global Number Corrections

Everywhere these appear (hub hero, platform section, pipeline, portfolio card,
canary site detection section, Technical Library docs, magazine article):

| Claim | Old | New |
|-------|-----|-----|
| Detection rules | 29 | **37** |
| Categories | 8 | **10** |
| Tests passing | 536 | **Remove** (volatile) |
| Execution tiers | 3 | 3 (correct) |

New categories to add where rule catalogs appear: Gift Card (2 rules),
Dispute (3), Invoice (3), Loyalty (4), Composite (1).

Remove "Refund-to-Different-Card" from the canary site rule table — doesn't
exist in `rule_definitions.py`.

### Hub (`site/index.html`)

**Hero stats:** Update "29 Detection Rules Live" → "37"

**Platform section — Goose card (line 1203-1208):** Rewrite entirely:
- Old: "BTCPay Server integration for Lightning Network payment acceptance.
  LNURL-auth passwordless merchant login. Sat-denominated subscription billing
  with zero payment processing fees."
- New: Describe Strike API credit system, gas schedule, treasury-funded
  onboarding, macaroon-based L402 gating. Mark as "Building" not "Phase 2".

**Platform section — Chirp card:** Update "29 detection rules across 8
categories" → "37 detection rules across 10 categories"

**Pipeline diagram:** Update "29 rules · 3 tiers" → "37 rules · 3 tiers"

**Portfolio — Canary card:**
- Remove "536 Tests Passing" stat
- Update "29 Detection Rules" → "37"
- Change "Bitcoin-anchored audit trail via Ordinal inscription" to reflect
  current state: evidence chain with INSERT-only enforcement and hash chains
  is built; Bitcoin inscription is infrastructure, not a user-facing feature

**Portfolio — Cove and Angel cards:** Review for accuracy against current code.

**Gated investor section:** Fix all links to point to `investor/` and `docs/`
relative paths. All cards must link to real files. Remove any card that doesn't
have a backing file.

Dead cards to fix:
- Manifesto → `investor/index.html`
- elJeffe orbital → `investor/eljeffe.html`
- War Chest → remove or link to actual file if it exists
- Component Business Model → remove (Dog, Bull, Heron, Hawk don't exist)
- CRDM → `docs/canary-data-model.html`
- Patent Visualizations → remove unless files exist
- JSONB Forensic → `docs/canary-jsonb-forensic.html`
- Magazine Article → `docs/canary-magazine-article.html`

Add new cards for:
- API Reference → `docs/canary-api-reference.html`
- Fox Case Management → `docs/canary-fox-spec.html`
- CRDM Mapping → `docs/canary-crdm-mapping.html`

### Canary Site (`site/canary/index.html`)

**Pricing section (lines 1246-1294):** Replace 3-tier fiction with actual
Goose credit model:
- Free onboarding: treasury-funded credits at Square OAuth completion
- Gold list alerts always free (the hook)
- Usage-based metering: operations cost credits from a single balance
- Self-service refills via Lightning (any wallet)
- Soft degradation: credits low → premium features gate, alerts stay free
- No specific sat amounts (tunable via gas schedule)

**Detection section:** Update rule count, add missing categories.

**Gated section:** Link doc cards to `../docs/` relative paths. Update
list of contents to match actual doc set.

**Rule catalog table:** Update to include all 37 rules across 10 categories.
Remove "Refund-to-Different-Card" (doesn't exist in code).

### Technical Library Docs (`site/docs/`)

**canary-data-model.html:** Update rule counts. Content is accurate.

**canary-platform-architecture.html:** Update rule counts. Content is accurate.

**canary-technical-roadshow.html:** Update rule counts. Mark L402 validation
gate as "Roadmap — Sprint 7+" per code comments. Update architecture claims
to match current TSP implementation.

**canary-factory-process.html:** Content is accurate. No changes needed
beyond consistent nav/footer.

**canary-eljeffe-protocol.html:** Major rewrite needed.
- Reposition from "selling point" to "technical architecture reference"
- Honest about what's built: inscription schema, evidence_records table,
  INSERT-only enforcement, hash chains, Merkle batching tables
- Honest about what's roadmap: Genesis Pool minting, merchant treasuries,
  L402 validation gate, Ordinals API integration, self-custody
- Frame Bitcoin as infrastructure integrity layer, not feature gate
- Remove claims about merchant self-minting, perpetual royalty revenue
  from minting (none of this is built)

**canary-magazine-article.html:** Number pass (29→37, 8→10). Narrative
about democratizing LP is durable — keep it.

**canary-jsonb-forensic.html:** Needs content update for new rule categories
(Gift Card, Dispute, Invoice, Loyalty, Composite). Add field mappings for
the 11+ new rules.

**canary-crdm-mapping.html:** Update for Goose wallet tables
(merchant_wallets, wallet_transactions, gas_schedule, macaroon_tokens,
strike_invoices). Check schema against current models/.

**canary-fox-spec.html:** Check against current `canary/fox/` code. Update
any stale specifics.

**eljeffe-swagger.yaml:** Update description to clarify this is spec/roadmap,
not live API. Keep the OpenAPI structure — it's well-written. Consider
updating server URL from `jeffe.io` to something more current.

**canary-api-reference.html:** Generate from the YAML via Redoc. Static
HTML, no server needed.

### Investor Assets (`site/investor/`)

**index.html (investor briefing):** Review for stale numbers and claims.
This renders the manifesto — it inherits whatever the manifesto says.
At minimum update rule counts.

**eljeffe.html (orbital diagram):** No content changes — it's an animated
SVG visualization. Just move to correct location.

### Manifesto V.3 Rewrite

**File:** `Brain/raw/inbox/GrowDirect_Manifesto_v1.2.md`

**Section V.3 — The Subscription Model (lines ~699-738):** Rewrite to
describe the Goose credit system as designed in
`docs/superpowers/specs/2026-04-15-canary-account-credit-system-design.md`:

- Replace Basic/Treasury/Full Node tiers with credit-based model
- Treasury-funded onboarding (100,000 sats default)
- Gas schedule with tunable per-operation costs
- Gold list alerts always free
- Soft degradation on credit exhaustion
- Strike Lightning API for self-service refills
- L402 macaroon authentication
- Update break-even math to reflect credit model economics

**Other manifesto sections needing number updates:**
- III.1 (26 → 37 rules, 8 → 10 categories)
- III.3 (26 → 37 rules)
- V.4 Protocol Pipe Mermaid diagram ("26 Chirp rules" → "37")
- Appendix C status map (frozen at Sprint 5/6 — update to current state)

### Styling Consistency

**Shared CSS (`site/css/shared.css`):** Extract common patterns:
- CSS custom properties (color palette — Canary dark theme)
- Nav bar (fixed, backdrop-blur, logo + links + CTA)
- Footer (copyright, nav links, contact)
- Gate pattern (password input, unlock JS, gated content reveal)
- Typography (Inter body, Space Grotesk headings, Space Mono monospace)
- Section structure (label, title, intro, grid)

**Per-file approach:** Each HTML file links `css/shared.css` for the common
pieces and keeps page-specific styles in an inline `<style>` block. This
keeps files openable as standalone `file://` URLs while sharing the design
language.

**Consistent nav on all docs:** Every doc in `site/docs/` gets:
- "← Canary" link back to `../canary/`
- "GrowDirect" link back to `../`
- Doc title in the nav

**Consistent footer on all pages:**
- `© 2026 GrowDirect DAO LLC`
- Nav links appropriate to the page context
- `lyle@growdirect.io` contact

---

## Files to Delete After Migration

| File | Reason |
|------|--------|
| `growdirect-hub.html` (repo root) | Replaced by `site/index.html` |
| `canary.growdirect.io.html` (repo root) | Replaced by `site/canary/index.html` |
| `Canary Technical Library/` (entire directory) | Replaced by `site/docs/` |
| `Brain/raw/inbox/growdirect_investor.html` | Moved to `site/investor/` |
| `Brain/raw/inbox/02-eljeffe-v3.html` | Moved to `site/investor/` |
| `knowledge-architecture.html` (repo root) | Archive to `docs/_archive/` |
| `Angel/askangel-home.html` | Evaluate — archive if not part of site package |

---

## What's NOT In Scope

- **Deployment config** (Cloudflare Pages, DNS, CNAME) — separate task
- **Mobile responsiveness rewrite** — check obvious breaks, don't redesign
- **New content creation** (merchant functional guides) — future task
- **Atlas browser** — stays in `Canary/docs/atlas/`, it's an app feature
- **Canary v0 site** (iCloud `canary-rd/website/`) — superseded, don't pull in
- **War Chest site** (iCloud `WarChest/site/`) — superseded by investor briefing

---

## Success Criteria

1. `site/` directory is self-contained — can be deployed by pointing any
   static host at it
2. Every number matches the codebase (37 rules, 10 categories, no volatile stats)
3. Every link in every page resolves to a real file in the package
4. Goose is described as the credit system it actually is
5. Bitcoin/L402 is positioned as infrastructure, not selling point
6. All docs share consistent nav, footer, and visual language
7. Manifesto V.3 matches the Goose spec
8. No files remain in repo root or Brain raw inbox that belong in `site/`
