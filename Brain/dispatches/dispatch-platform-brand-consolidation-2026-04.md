---
type: dispatch
status: ready-for-handoff
date: 2026-04-24
target: claude-code-session
streams: 3
priority: high
tags: [brand-strategy, platform, katz, canary-retail, cbm-v2, vault-scaffolding]
---

# Dispatch — Platform Brand Consolidation (April 2026)

Hand-off brief for a Claude Code session to pull three parallel streams
into a coherent platform-brand foundation. Written by a strategy/brainstorm
session; to be executed by a code session. Expect this to be one focused
sprint — not a multi-week campaign.

---

## Why this exists

An advisor challenged the "one app for this random thing" framing of Canary.
Their point: SMB specialty retailers with online footprint don't need a
point solution, they need a platform they can actually deploy and run their
business on. We've been quietly assembling the content to ship exactly that
across ~80 messages of brainstorm — ARTS standards, Tesco TOM interface
pack, Eagle Eye FR/NFR, Secure 5 inventory, LPMS case management, Heartbeat
store-IoT, DSD vendor variance, retail operating model doctrine — every
domain the Retail OS spine needs is already on the desk.

This dispatch consolidates the strategic pivot into an executable shape.

## The strategic reframe (captured in one paragraph)

GrowDirect LLC is a platform company, not a three-projects-sharing-infra
company. Canary Retail is the revenue-bearing product — a retail operating
system for SMB specialty retailers with online footprint, built on ARTS
standards, POS-agnostic by architecture, shipping the modules nobody else
productizes (Customer, Device, Asset/Bubble) alongside the modules everybody
ships poorly (LP, Transactions). CATz is the delivery methodology — how
GrowDirect designs and deploys, derived from the 2003 Canadian-drug-chain
engagement template, externalized as GrowDirect's professional services
frame. Cove and Angel are hobby/lab tier — they benefit from platform CRDM
work but they're not front of mind for the brand exercise. The internal
Brain becomes the preprocessing layer; CATz and Canary Retail Brain are
the externalized, scrubbed, magic-added sibling vaults.

## Point of view — the four-layer threat posture

A platform that handles money, people, devices, and agents has to stand on
a published threat posture. Canary Retail's is four layers, not one:

1. **Physical — the Bubble.** Every alarm, camera, sensor, EAS gate, lock,
   and reader across Sensormatic / Verkada / ADT / cable-guy-of-the-week
   vendors, registered to site and asset, health-monitored, incident-linked.
   The "Boy in the Bubble" CIO metaphor. Owned by the A-prefix Asset
   Management module.
2. **Digital — Chirp + Fox.** TSP-sealed, hash-chain evidence, rule-driven
   anomaly detection, case-managed disposition. Owned by the T and Q
   prefixes. **Solex is the production transaction source Chirp/Fox
   observe — the Digital layer has a working merchant emitting real
   events, not a synthetic harness.**
3. **Agent — principal-aware.** Every agent knows its principal, its
   authority scope, and its audit trail. Open World 4.0 is an agent-on-agent
   world; an agent that doesn't know who it works for gets exploited.
   Owned by the CBM v2 Agent Strategy cell.
4. **Data — ISO / SOC II / PCI / GDPR / CCPA.** PII map, retention policy,
   right-to-delete, data residency, breach response playbook. Owned by
   the CBM v2 Data Protection & Governance cell.

**Founder credentialing for the Data layer specifically:** the founder
has personally owned ISO 27001 certification (sat through the audit at
a prior acquisition), operated SOC II-certified data centers, executed
breach response, and held consumer-privacy responsibility at
public-company-acquired scale in prior executive roles. This is the
grounding credential that lets Canary Retail claim enterprise-grade
threat posture at SMB price.

**Authoring-rule instruction for the external vault:** capture this
credentialing in `CATz/about/bio-alejandro.md` as *enterprise-grade
credentialing the founder personally owned* — ISO 27001 audit
participation, SOC II data-center operation, breach response, consumer
privacy. **Do not cite the specific prior company by name.** Lineage
stays in internal Brain only per the no-former-company-lineage rule.
The external phrasing is: "founder has personally owned ISO 27001
audit, SOC II data-center operation, and consumer-privacy incident
response in prior executive roles."

**Positioning line (external, safe to use):** "Enterprise-grade threat
posture — physical, digital, agent, and data — shipped as an SMB-priced
platform. Not because we read a SOC II whitepaper. Because our founder
ran SOC II-certified data centers, sat through the ISO 27001 audit, and
owned consumer privacy at a public-company-acquired scale."

## The "store is a little HOA" platform unlock

The insight that reframes the whole stack: a retail store and an HOA parcel
are architecturally the same entity — a physical location with assets
attached, people related to it, governance rules over it, inspections
against it, and exception workflows when something's wrong. That means the
underlying CRDM (People × Places × Things × Events × Workflows) is *one*
model with domain vocabularies layered on top. Canary Retail is the
commercial expression. Cove is the hobby HOA expression. Angel is the
hobby real-estate expression. Platform play is real.

---

## Three streams requiring coordination

### Stream 1 — Vault Scaffolding (external brands)

Stand up two new Obsidian vaults as siblings to `~/GrowDirect/`:

- `~/CATz/` — methodology brand
- `~/Canary-Retail-Brain/` — product brand

**Authoring rules for both vaults (enforced at the top-level README.md):**

- No client names (except as published, attributed references)
- No former-company lineage (no IBM, no Appriss, no Sysrepublic, no
  NCR-era references)
- No raw intake material (that stays in GrowDirect/Brain/raw/)
- All work product attributed to GrowDirect LLC / Canary Retail only
- Adopted-standard references are allowed (ARTS, ISO, PCI, NRF) because
  those are published external standards, not proprietary lineage
- Bios, vendor agreements, licenses, partnerships, published API contracts
  live in CATz (the methodology + the commercial envelope)
- Product architecture, module catalog, integration catalog, abstracted
  case studies live in Canary-Retail-Brain (the product envelope)

**Vault structure for CATz:**

```
CATz/
├── README.md                    # what CATz is, who it's for, authoring rules
├── about/
│   ├── growdirect-llc.md        # the company
│   ├── bio-alejandro.md         # founder bio (externalized)
│   └── licenses-and-standards.md  # ARTS adoption, certifications, partnerships
├── method/
│   ├── overview.md              # CATz in one page
│   ├── phases/
│   │   ├── phase-1-assess-and-design.md
│   │   └── phase-2-select-and-implement.md
│   ├── workstreams/
│   │   ├── commercial.md        # merchandise, pricing, promotion
│   │   ├── supply-chain.md      # forecast, order, distribution
│   │   ├── finance.md           # po, invoice, reconciliation
│   │   ├── store-operations.md
│   │   ├── space-range-display.md
│   │   ├── people-labor.md
│   │   ├── property-assets.md
│   │   ├── loss-prevention.md
│   │   └── technology.md
│   ├── artifacts/
│   │   ├── sdd-template.md
│   │   ├── interface-spec-template.md
│   │   ├── context-diagram-template.md
│   │   └── traceability-matrix-template.md
│   └── roles/
│       ├── architect.md
│       ├── engineer.md
│       ├── writer.md
│       └── pmo.md
├── cbm-v2/                      # GrowDirect CBM extension
│   ├── overview.md              # why CBM needs four new cells
│   ├── agent-strategy.md        # NEW — AI-agent workforce as first-class function
│   ├── data-protection-and-governance.md  # NEW — PII, hash-chain, compliance
│   ├── pmo.md                   # NEW — program management
│   └── arb.md                   # NEW — architecture review board
└── partnerships/
    ├── api-partners.md
    ├── integration-partners.md
    └── standards-bodies.md      # ARTS, NRF, PCI SSC
```

**Vault structure for Canary-Retail-Brain (modeled on CATz):**

```
Canary-Retail-Brain/
├── README.md                    # what Canary Retail is, authoring rules
├── platform/
│   ├── overview.md              # Retail OS positioning, SMB specialty audience
│   ├── spine-13-prefix.md       # C/D/F/J/S/P/T/R/N/L/Q/W/A — the WHOLE platform pitch
│   ├── crdm.md                  # canonical retail data master
│   ├── arts-adoption.md         # POSLog, Customer, Device, Site models
│   └── differentiated-five-add-on.md   # T+R+N+A+Q — the "add-on" layer that distinguishes Canary on top of retail baseline
├── modules/
│   ├── t-transaction-pipeline.md    # TSP, POS-agnostic, webhook-first
│   ├── r-customer.md                # ARTS Customer Model
│   ├── n-device.md                  # ARTS Device Model
│   ├── a-asset-management.md        # Bubble / threat detection / registry
│   ├── q-loss-prevention.md         # Chirp + Fox
│   ├── c-commercial.md              # items, departments, suppliers (roadmap)
│   ├── d-distribution.md            # inventory movement (roadmap)
│   ├── f-finance.md                 # po, invoice (roadmap)
│   ├── j-forecast-order.md          # GFO equivalent (roadmap)
│   ├── s-space-range-display.md     # SRD (roadmap)
│   ├── p-pricing-promotion.md       # Eagle Eye equivalent (roadmap)
│   ├── l-labor-workforce.md         # (roadmap)
│   └── w-work-execution.md          # generalized Chirp+Fox for all domains (roadmap)
├── integrations/
│   ├── pos-adapters.md              # Square (live), Lightspeed/Clover/NCR/RAPID
│   ├── payments.md
│   ├── ecommerce.md                 # Shopify
│   ├── security-hardware.md         # Sensormatic, Verkada, ADT, etc.
│   └── mdm-and-itam.md              # Jamf, Lansweeper, Snipe-IT
├── architecture/
│   ├── service-mesh.md
│   ├── tsp-pipeline.md
│   ├── chirp-engine.md
│   ├── fox-cases.md
│   └── evidence-chain.md
├── case-studies/                # abstracted, no client names
│   ├── smb-specialty-archetype.md
│   ├── multi-store-apparel.md
│   ├── food-and-beverage.md
│   └── sporting-goods.md
└── roadmap/
    ├── v1-differentiated-five.md
    ├── v2-crdm-expansion.md
    └── v3-full-spine.md
```

### Stream 2 — Platform Architecture Consolidation

Produce the canonical architecture document that anchors both vaults.
Single source of truth for the 13-prefix spine, the CRDM, and the CBM v2.

**Artifacts:**

- `Canary-Retail-Brain/platform/spine-13-prefix.md` — the full module map
  with one-liner per module, dependencies, phase assignment
- `Canary-Retail-Brain/platform/crdm.md` — People × Places × Things ×
  Events × Workflows; how it maps to ARTS; how each module plugs in
- `CATz/cbm-v2/overview.md` — standard retail CBM cells plus the four
  extensions, with a comparison table showing what IBM-CBM-2004 missed
- `CATz/cbm-v2/agent-strategy.md` — customer-facing agents vs delivery
  agents, agent roster, agent SDD template, memory bus architecture
- `CATz/cbm-v2/data-protection-and-governance.md` — PII map, hash-chain
  evidence, PCI/GDPR/CCPA posture, audit, retention, right-to-delete,
  data residency
- `CATz/cbm-v2/pmo.md` — sprint methodology, factory pipeline, release
  trains, dispatch pattern (this document is an example)
- `CATz/cbm-v2/arb.md` — ADR governance, design review, tech debt,
  cross-module architecture authority

### Stream 3 — Content Migration & Scrubbing

Selectively promote material from `GrowDirect/Brain/wiki/` and
`GrowDirect/docs/research/` into the two new external vaults with
proper scrubbing.

**Scrub rules (mechanical):**

- Client names → archetypes (per existing `feedback_scrub_client_names.md`)
- Former-company references → removed
- Specific client engagement details → kept only if abstracted to pattern
- Lineage citations → removed from external vaults (prior art stays in
  internal Brain only)
- Dates → kept if published or abstracted to year-level

**Promotion candidates for CATz (methodology):**

- `secure-retail-operating-model-2006` → `CATz/method/workstreams/` split
  across the 8 domains (Commercial, Finance, Supply Chain, Retail Ops,
  Space/Range/Display, Forecast/Ordering, People, Property)
- `secure-property-services-operating-model-2002` → RACI patterns into
  `CATz/method/roles/`
- `secure-eagle-eye-fnr-2018` → traceability-matrix template into
  `CATz/method/artifacts/`
- `docs/playbooks/playbook-method-katz-reverse-engineer.md` → the method itself
  into `CATz/method/phases/`

**Promotion candidates for Canary-Retail-Brain (product):**

- `canary-platform-overview` → `platform/overview.md` (scrubbed of any
  prior-art lineage)
- `canary-architecture` → `architecture/service-mesh.md`
- `canary-detection` → `architecture/chirp-engine.md`
- `canary-fox-case-management` → `architecture/fox-cases.md`
- `canary-tsp-pipeline` → `architecture/tsp-pipeline.md`
- `canary-chirp-rules` → `modules/q-loss-prevention.md`
- `canary-data-model` → `platform/crdm.md`

**Content that stays internal (Brain only):**

- All `secure-*` wiki articles (prior art, client-specific history)
- All `Brain/raw/inbox/*` intakes
- All `docs/research/*` research folders
- All deployment-archetype client-specific material
- Anything with unscrubbed client names
- Anything with former-company lineage

---

## Decisions already made

| Decision | Answer |
|---|---|
| Vault locations | `~/CATz/` and `~/Canary-Retail-Brain/` as siblings under home |
| Vault purpose split | CATz = methodology; Canary-Retail-Brain = product |
| Internal Brain role | Preprocessing layer; stays at `~/GrowDirect/Brain/` |
| CATz as public brand | Working name only; public brand TBD (trademark risk with Katz Group) |
| Brand mark family | Watchful-observer: cats + mice + canary (surveillance + protection) |
| Cove / Angel | Hobby/lab tier; stay in Brain; not in brand exercise |
| Platform pitch | Full 13-prefix spine — pitch the WHOLE thing (the platform, end-to-end) |
| Operational lead / focus | Differentiated-Five (T+R+N+A+Q) framed as the "add-on" layer — what Canary Retail adds on top of retail baseline that nobody else ships |
| CBM v2 extensions | Agent Strategy, Data Protection & Governance, PMO, ARB |
| Authoring rules | No client names, no former-company lineage, all GrowDirect LLC / Canary Retail |

## Open decisions (flag in session, escalate if blocking)

| Decision | Options | Recommendation |
|---|---|---|
| Public methodology brand | CATz / CATz-derived / new name | Defer — needs trademark check |
| Agent strategy: customer-facing vs delivery-internal | Both / customer-only / delivery-only | Both, with distinction in CBM v2 doc |
| Cove/Angel content handling | Stay in Brain / minimal Canary-Retail-Brain mention / full separate vaults | Stay in Brain for now |
| ARTS license / membership posture | Member / reference-only / adopter | Flag — 500MB of NRF ARTS materials already downloaded; find them |

---

## Sequencing

Execute in this order to avoid rework:

1. **Scaffold both vaults** (Stream 1) — empty skeleton, READMEs with
   authoring rules, folder structure as specified above. 30-45 min.
2. **Write the spine + CRDM + CBM v2 core docs** (Stream 2) — the
   anchoring architecture documents. These don't depend on content
   migration; they're new writing grounded in this dispatch + the
   prior brainstorm. 2-3 hours.
3. **Migrate selected content** (Stream 3) — pull the promotion
   candidates, scrub them, place them. 2-3 hours.
4. **Cross-link** — internal Brain references external vault articles
   where appropriate (e.g., `Brain/projects/Canary.md` gets a note
   pointing to `Canary-Retail-Brain/`). External vaults never
   reference internal Brain.

Total estimated session: one focused day (5-7 hours).

## Acceptance criteria

Session is done when:

- [ ] Both vaults exist at specified locations with README.md +
      authoring rules visible at the root
- [ ] Every folder listed in the vault structure exists (empty is OK
      if not-yet-populated; placeholder README.md inside)
- [ ] The five anchoring docs exist with first-draft content:
  - [ ] `Canary-Retail-Brain/platform/overview.md`
  - [ ] `Canary-Retail-Brain/platform/spine-13-prefix.md`
  - [ ] `Canary-Retail-Brain/platform/crdm.md`
  - [ ] `CATz/method/overview.md`
  - [ ] `CATz/cbm-v2/overview.md`
- [ ] At least 3 Canary-Retail-Brain articles and 3 CATz articles
      migrated from Brain with scrubbing verified (no client names,
      no prior-company references, nothing internal)
- [ ] `Brain/projects/Canary.md` updated with a single line pointing
      to the external vault
- [ ] A session log committed describing what was done, what was
      deferred, and any scrub-rule edge cases encountered

## Out of scope (do NOT do in this session)

- Code changes to `Canary/`, `Cove/`, or any runtime service
- Database migrations
- External marketing copy, landing pages, or public website content
- Graphic design, logos, or visual identity (comes after words are
  right)
- Full SDD rewrites (stay with first-draft quality; polish comes later)
- Cove / Angel content migration (hobby tier, stays in internal Brain)
- Heartbeat/Fireball playbook execution (separate dispatch; don't
  conflate)
- Interface Design Documents intake processing (separate dispatch)
- Trademark / legal clearance for CATz as public brand (deferred
  decision)

## Handoff notes for the code session

- The user (Alejandro) is a solo founder using Claude Code for this
  work. Expect human review after each vault's skeleton lands.
- Per `GrowDirect/CLAUDE.md`: build working outputs; don't organize
  for the sake of organizing. This dispatch is the plan; execute it.
  Don't re-plan.
- The 500MB NRF ARTS materials mentioned in the brainstorm are
  somewhere local (possibly `/Users/gclyle/mnt/nas-archive/` or an
  old `~/secure/` folder). Don't block on finding them — note as
  open TODO in the session log and proceed.
- The Heartbeat/Fireball material at `Brain/raw/inbox/Heartbeat/` is
  prior art that stays internal. It informs the architecture but
  doesn't get promoted to the external vaults.
- The Interface Design Documents (Tesco TOM pack) at
  `Brain/raw/inbox/Interface Design Documents/` are also internal
  prior art; don't surface them in external vaults.
- Use existing `content-engine/` tools for any intake/ingest work.
- Obsidian wikilinks should work within each vault; cross-vault
  links use relative paths from the vault root.
- Commit work in small logical batches. Don't do one giant commit
  at the end.

## References

- `GrowDirect/CLAUDE.md` — platform rules, session discipline
- `GrowDirect/docs/playbooks/playbook-method-katz-reverse-engineer.md` — CATz
  method source of truth
- `GrowDirect/docs/playbooks/playbook-heartbeat-blueprint.md` — Heartbeat
  playbook (separate dispatch)
- `GrowDirect/Brain/projects/Canary.md` — Canary project MOC
- `GrowDirect/Brain/projects/Method.md` — Method MOC (factory pipeline)
- `GrowDirect/Brain/projects/Secure.md` — Secure MOC (prior-art
  lineage, stays internal)

---

## Stream 4 — Solex Worked-Example Anchoring

Solex is not a hobby project; it's the first live commerce front-end
for Canary Retail and a partnership test client. As an operating
merchant against the Square sandbox, it produces real transactions,
refunds, inventory adjustments, subscriptions, and webhook events.
That makes it the **production transaction source** that Chirp/Fox
observe — the Digital layer of the four-layer threat posture runs
against a working merchant, not a synthetic harness.

Stream 4 promotes the existing internal worked-example crosswalk
into the externally-facing Canary-Retail-Brain vault so every claim
in `platform/overview.md` and `platform/spine-13-prefix.md` has
concrete evidence backing it — a single minimal e-commerce app
populates ~70% of the canonical retail capability surface. This is
the "SMB collapse" story made real.

### Artifacts

- **Promote:** `Brain/wiki/retail-spine-solex-crosswalk.md` → 
  `Canary-Retail-Brain/platform/worked-example-solex.md`.
  Scrubbed per authoring rules (no prior-art lineage, no internal
  codename links). The coverage tables — Component → BST,
  Data-flow → BST, Scenario → BST, Data-model → BST dimensions /
  measures — all promote as-is; they're GrowDirect-owned structural
  content with no client / prior-engagement material.
- **Cross-reference:** update `Canary-Retail-Brain/platform/overview.md`
  to include the three "SMB collapse" observations as a featured
  callout (Multi-Channel + Corporate Finance compress cleanly;
  Customer compresses well; Merchandising / Store-Ops are where
  the missing operational schemas surface).
- **Cross-reference:** update `Canary-Retail-Brain/platform/
  spine-13-prefix.md` to use the Merchandising / Store-Ops gap list
  as the "why these modules exist" justification for each
  non-Differentiated-Five prefix. Concretely:
  - **C** — commercial catalog covers Merchandising Assortment gaps
    identified in Solex (single-channel, no multi-store allocation)
  - **D** — distribution closes the multi-location-inventory gap
    (Solex is single-warehouse; enterprise requires warehouse +
    store + transit tiers)
  - **F** — finance closes the vendor-surface gap (Solex collapses
    vendor into Square fees + bank receipts)
  - **J** — forecast/order closes the on-order-inventory gap
    (Solex has no PO/replenishment surface)
  - **S** — space/range/display closes the planogram gap
    (out-of-scope for online-only; in-scope for physical retail
    Canary Retail also addresses)
  - **P** — pricing/promotion extends Solex's promo-code stub into
    a full promotion engine
  - **L** — labor closes the staffing gap (Solex has no employee
    surface; Canary Retail does)
  - **W** — work execution generalizes Chirp+Fox beyond LP to all
    domains once the module spine is full

- **Internal-only:** the `retail-spine-solex-crosswalk.md` and
  `retail-integration-spine.md` sources stay in internal Brain. The
  promoted external article references "GrowDirect's e-commerce
  reference implementation" without linking back to prior-art
  integration-spine lineage.

### Acceptance criteria

- `Canary-Retail-Brain/platform/worked-example-solex.md` exists with
  confidentiality frontmatter and the full coverage tables
- `platform/overview.md` has a featured "SMB collapse" callout
  citing the three observations; cross-links to
  `worked-example-solex.md`
- `platform/spine-13-prefix.md` per-prefix section for C/D/F/J/S/P/L/W
  each cites the specific Solex-surfaced gap it closes
- Four-layer threat posture section (this dispatch, above) names
  Solex as the Digital-layer production transaction source

### Out of scope for Stream 4

- Building additional Solex features
- Running the retail-diagnostic skill against Solex (separate dispatch)
- Promoting Solex internals (spec, SDDs, scenarios) to the external
  vault — those stay internal
- Exposing Solex's Square sandbox merchant ID or any site-specific
  configuration in external-facing content

---

**Dispatch author:** Cowork strategy session, 2026-04-24
**Executor:** Claude Code session (next)
**Review gate:** Human review after vault scaffolding (Stream 1 complete)
before Stream 2/3 begin. Stream 4 added 2026-04-24 after CATz +
Canary-Retail-Brain scaffolding landed; runs without requiring
additional review gates.
