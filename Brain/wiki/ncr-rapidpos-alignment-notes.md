---
title: NCR Vault–RapidPOS Alignment Notes
type: wiki
project: Canary
created: 2026-04-27
tags: [ncr, rapidpos, alignment, hawk-phase-1]
last-compiled: 2026-04-27
needs-review: false
---

# NCR Vault–RapidPOS Alignment Notes

Read pass of the NCR companion vault (`~/GrowDirect-NCR/`) against two focus questions: (1) where does the vault conflate RapidPOS (delivery partner) with NCR Counterpoint (POS platform)? (2) are the vault content and the SDD suite (12 `ncr-counterpoint-*.md` files) telling the same story?

## Finding 1: RapidPOS vs NCR Counterpoint — Mostly Clean, Two Positioning Gaps

The vault correctly distinguishes the two entities in most places. The CLAUDE.md states: "Audience: NCR Counterpoint VARs (Rapid POS and others evaluating Canary)." The architecture diagram labels Layer 4 as "RapidPOS MCP Server (Canary-powered)" — correctly positioning RapidPOS as the deployment partner, not the platform itself.

**Two conflation points:**

1. **`verticals/gun.md`, `wine-spirits.md`, `beverage.md`, `feed-tack.md`** all say: "Rapid Garden POS serves this vertical on NCR Counterpoint." This implies Rapid Garden POS is the only VAR for these verticals. The vault is titled "Canary for NCR Counterpoint" and aimed at "NCR Counterpoint VARs" (plural). The stub vertical pages should say "NCR Counterpoint VARs serve this vertical" — with Rapid POS as a named example, not the only option.

2. **`modules/index.md` line 6**: "Canary Retail Spine on the RapidPOS L&G Backbone." This title hardcodes RapidPOS as the backbone. The module index should reference "NCR Counterpoint" as the backbone, with L&G as the lead vertical. RapidPOS is how you get to L&G, not the platform itself.

**Why this matters for SDDs:** The SDD suite (`ncr-counterpoint-*.md`, 12 files) is correctly Counterpoint-scoped, not RapidPOS-scoped. The adapter SDDs reference Counterpoint REST endpoints, not RapidPOS-proprietary extensions. If the vault conflates the two, it misrepresents the SDD scope to VARs who aren't RapidPOS.

## Finding 2: Fox Is the Only Case Management Surface Named — Same CRB Gap

Fox appears 30+ times in the NCR vault's module cards. Hawk appears zero times. The NCR vault is a projection of CRB, so the Fox→Hawk gap propagates automatically. Same resolution: SDD Dispatch 5 defines Hawk's relationship to Fox; CRB updates; NCR vault inherits the update on next sync.

**NCR-specific wrinkle:** The deployment guide (`deployment/index.md`) references Fox by name in the RACI matrix (line 76-77: "approves Fox case findings," "Works Fox cases from triage to closure"). This is the most operationally visible Fox reference in any vault — it's in the document a VAR installer reads. When Hawk ships, this page needs to update first.

## Finding 3: NCR Vault Module Cards Are Identical to CRB

Q-loss-prevention.md and T-transaction-pipeline.md in the NCR vault are byte-for-byte identical to their CRB counterparts. This is by design — the companion vault is a projection of Brain/CRB, filtered for NCR audience. But it means:

- No NCR-specific framing has been added to the module cards
- The assumption markers reference "Rapid Garden POS sandbox database" directly, which is appropriate for this vault but assumes RapidPOS is the only path
- ASSUMPTION-Q-08 and ASSUMPTION-T-09 both ask about "Rapid POS proprietary tables on top of standard Counterpoint schema" — correctly identifying the RapidPOS extension question, but a non-RapidPOS VAR reading this vault would wonder whether similar assumptions exist for their proprietary extensions

**SDD alignment:** The SDD suite correctly treats Rapid POS extensions as an assumption to validate, not a hard dependency. The adapter SDDs (`ncr-counterpoint-tsp-adapter.md`, `ncr-counterpoint-item-catalog-adapter.md`) operate against standard Counterpoint endpoints. Rapid POS extensions are documented as optional scope. The vault and SDDs tell the same story here.

## Finding 4: The Deployment Guide Is the NCR Vault's Distinctive Contribution

`deployment/index.md` is the most operationally specific document in any of the three vaults. It defines:
- A 5-section CATz-aligned deployment frame (Frame / People / Agents / Model / Blueprint)
- A concrete 6-module Phase 1 activation sequence (S → I → F → R → D → Q)
- A responsibility matrix with four named roles (Owner/Operator, Store Manager, LP Investigator, VAR Installer)
- A 7-day activation timeline with explicit gates
- Phase 2 capabilities already enabled by Phase 1 substrate

This document is what turns the module cards into an actual deployment playbook. It references the SDD suite indirectly (through the module links) and is consistent with the SDD activation sequence.

**SDD alignment:** The deployment guide's activation sequence (reference data → entity seeding → live polling + detection) matches the SDD suite's `ncr-counterpoint-merchant-onboarding.md` flow. No drift detected.

## Finding 5: The Agent Layer (ALX/VSM) Is Forward-Positioned

The NCR vault positions ALX/VSM heavily — dedicated pages for `agents/index.md`, `agents/vsm.md`, `agents/architecture.md`. The five-layer architecture diagram puts "RapidPOS MCP Server (Canary-powered)" at Layer 4 with specific MCP tool surfaces and response time targets (<200ms inventory, <300ms diagnosis, <500ms transaction authorization).

**This is aspirational.** The live code has no MCP server endpoint, no ALX agent deployed, and no customer-facing Claude interaction. The SDD suite covers the data ingestion layer (Phases 0-4 of the spine build), not the agent layer.

This is not a drift issue — the vault explicitly positions this as the co-sell vision, and the deployment guide grounds Phase 1 in what exists (detection, not agents). But a VAR reading the agents section may assume ALX is deployable today. The vault should more explicitly stage ALX as Phase 2/3 capability.

## Finding 6: NCR Context Page Has Strong Competitive Claims

`ncr-context/index.md` makes sourced competitive claims:
- NCR stock down 40% since December 2025
- Revenue declining 13-18% (2026 guidance)
- NCR's Voyix Commerce Platform is "microservices on top of legacy data models"

These claims are sourced but dated (April 2026). They're defensible as of the vault creation date. The SDDs don't make competitive claims — correctly, SDDs are technical specs, not positioning.

**Scrub note (2026-05-01):** an MCP-firsts boast claim ("No enterprise physical retail POS has a native MCP endpoint as of April 2026") was previously listed here and in the NCR vault; removed during sales-claims scrub. See commit log.

**The vault and SDDs have clean separation:** competitive positioning lives in the vault (`ncr-context/`, `why-canary/`); technical spec lives in the SDDs. No bleed between them.

## Finding 7: Vertical Playbooks Are L&G-Heavy, Stubs Elsewhere

`verticals/lawn-garden.md` and `verticals/armstrong.md` are fully developed. The remaining four verticals (gun, feed-tack, beverage, wine-spirits) are one-paragraph stubs. All stubs incorrectly say "Rapid Garden POS serves this vertical" (see Finding 1).

The Armstrong proof case (`verticals/armstrong.md`) is the most sales-ready artifact in the vault — 31 locations, ESOP-owned, SoCal geography overlap with RapidPOS. It correctly frames Canary's value against the specific garden center operating reality.

**SDD alignment:** The SDDs are vertical-agnostic (they operate against Counterpoint endpoints, not vertical-specific configurations). The vertical packs (Q.6 garden-center allow-lists) are documented in the module cards and rule catalog, which are shared between CRB and NCR vault. No drift.

## Finding 8: SDD Suite and NCR Vault Are Telling the Same Story

The 12-file SDD suite (`docs/sdds/canary/ncr-counterpoint-*.md`) plus the spine integration SDD and delivery spec are consistent with the NCR vault's integration page and module cards:

| SDD File | NCR Vault Reference | Consistent? |
|---|---|---|
| `ncr-counterpoint-tsp-adapter.md` | T module card + integration page | Yes — poll-based ingestion, Document omnibus, provider-keyed parsing |
| `ncr-counterpoint-retail-spine-integration.md` | Module index + deployment guide | Yes — 13-module spine, ARTS alignment, Phase 1 scope |
| `ncr-counterpoint-auth-adapter.md` | Integration page (auth model) | Yes — HTTP Basic + APIKey |
| `ncr-counterpoint-store-station-adapter.md` | Deployment guide §S module | Yes — store/station config as first substrate |
| `ncr-counterpoint-item-catalog-adapter.md` | Deployment guide §I module | Yes — item master + categories |
| `ncr-counterpoint-paycode-adapter.md` | Deployment guide §F module | Yes — PAY_TYP canonical mapping |
| `ncr-counterpoint-customer-adapter.md` | Deployment guide §R module | Yes — AR_CUST, PII discipline |
| `ncr-counterpoint-inventory-adapter.md` | D module card + deployment §D | Yes — per-location polling, snapshot delta |
| `ncr-counterpoint-module-q-chirp-wiring.md` | Q module card + rule catalog | Yes — 10 families, garden-center allow-lists |
| `ncr-counterpoint-merchant-onboarding.md` | Deployment guide §6 activation | Yes — same phase sequence |
| `ncr-counterpoint-square-coupling-audit.md` | T card §T.3.9 (Square legacy) | Yes — substrate decoupling scope |
| `pos-adapter-substrate.md` | T card §T.1 (adapter ingress) | Yes — multi-provider abstraction |

**No story drift detected between the SDD suite and the NCR vault.** The SDDs are the technical implementation of what the vault describes to VARs.

## Summary — NCR Vault Actions

| Finding | Current State | Action | Priority |
|---|---|---|---|
| Vertical stubs conflate RapidPOS with NCR | 4 stubs say "Rapid Garden POS serves this vertical" | Change to "NCR Counterpoint VARs serve…" with RapidPOS as example | Low — stubs, not live content |
| Module index title hardcodes RapidPOS | "Canary Retail Spine on the RapidPOS L&G Backbone" | Change to "…on the NCR Counterpoint Backbone" | Low |
| Fox → Hawk gap | Same as CRB — 30+ Fox mentions, zero Hawk | Inherits fix from CRB sync after SDD Dispatch 5 | Hawk Phase 1 |
| Deployment guide RACI names Fox | Operationally visible to VAR installers | Update as part of Hawk CRB sweep | Hawk Phase 1 |
| ALX/VSM staging | Positioned heavily but aspirational | Add explicit Phase staging note to agent pages | Medium — avoids overpromise |
| SDD suite consistency | Vault and SDDs tell same story | No action | None |

**The NCR vault is the healthiest of the three companion vaults for RapidPOS alignment.** It was built Counterpoint-first (not Square-first like CRB), its deployment guide is the most operationally concrete artifact in any vault, and the SDD suite backing it is consistent. The two fixes needed are naming (RapidPOS ≠ all VARs) and Fox→Hawk (inherited from CRB).

## Related

- [[catz-rapidpos-alignment-notes]] — CATz vault read pass
- [[crb-rapidpos-alignment-notes]] — CRB vault read pass
- [[ncr-vault-gap-ledger]] — NCR vault coverage audit
- [[ncr-counterpoint-rapid-pos-relationship]] — VAR clarification article
- `docs/superpowers/plans/2026-04-27-hawk-phase-1.md` — Hawk Phase 1 plan
