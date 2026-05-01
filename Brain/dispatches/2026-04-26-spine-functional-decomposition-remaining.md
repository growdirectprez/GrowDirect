---
type: dispatch
status: ready-for-execution
date: 2026-04-26
target: any Claude session (Sonnet preferred for cost; format is now committed so no Opus-level synthesis required)
priority: medium-high (completes the Counterpoint module catalog — 6 of 13 modules remain)
phase: continuation of CATz Phase II Module Functional Decomposition pass
prerequisite: 7 of 13 module cards complete (Q, T, R, J, S, F, N); CATz template formally promoted; lineage-scrub policy committed
companion-template: CATz/method/artifacts/module-functional-decomposition.md
companion-cards-completed:
  - Brain/wiki/canary-module-q-functional-decomposition.md (★ Canary native — canonical example)
  - Brain/wiki/canary-module-t-functional-decomposition.md (● Full direct, substrate)
  - Brain/wiki/canary-module-r-functional-decomposition.md (● Full direct, with privacy posture L2)
  - Brain/wiki/canary-module-o-functional-decomposition.md (◐ Partial — partial-coverage exemplar)
  - Brain/wiki/canary-module-s-functional-decomposition.md (● Full direct, vertical-distinctive)
  - Brain/wiki/canary-module-f-functional-decomposition.md (● Full direct, cross-cutting)
  - Brain/wiki/canary-module-n-functional-decomposition.md (● Full direct, dense-config)
modules-remaining: [D, C, P, A, L, W]
tags: [canary, ncr-counterpoint, catz-phase-2, functional-decomposition, module-cards]
---

# Dispatch — Complete Spine Module Functional Decomposition (D, C, P, A, L, W)

## Why this dispatch exists

Opus 4.7 token budget exhausted mid-pass through the 13-module functional-decomposition crank. Format is now committed (CATz Phase II artifact promoted at `CATz/method/artifacts/module-functional-decomposition.md`), seven cards landed, lineage-scrub policy locked. **The remaining six modules can be cranked by a Sonnet-class session against the committed template — no Opus-level synthesis required.** This dispatch packages everything a fresh session needs.

## Operational discipline

Executes in any Claude session with access to `/Users/gclyle/GrowDirect/Brain/wiki/` and `/Users/gclyle/Canary-Retail-Brain/modules/`. Sonnet preferred — the work is structured filling-in against an established template, not novel synthesis.

## Pre-flight reading (mandatory; read in this order)

1. **`CATz/method/artifacts/module-functional-decomposition.md`** — the formal template. This card defines the format. Follow it exactly.
2. **One existing card matching the L1 cell shape of the module being drafted** — see "Template-pick by cell shape" below.
3. **`Brain/wiki/ncr-counterpoint-api-reference.md`** — Counterpoint surface for the module being drafted (find the relevant Spine Module section).
4. **`Brain/wiki/ncr-counterpoint-endpoint-spine-map.md`** — per-endpoint × CRDM × spine map.
5. **`Canary-Retail-Brain/modules/{LETTER}-*.md`** — L1 canonical spec for the module being drafted.
6. **`CATz/proof-cases/specialty-smb-counterpoint-solution-map.md`** — confirms L1 cell for the module being drafted.

## Lineage-scrub policy (NON-NEGOTIABLE)

**Do NOT cite specific source methodologies in the body.** No SAP, no RBIS, no Oracle Retail, no Retek, no Katz SCM, no Secure Retail Operating Model, no "industry-standard practice", no "canonical retail process patterns / we extract not invent".

The format presents as Canary's. One-line synthesis acknowledgment in the CATz template covers all lineage; module cards do not repeat it.

Verify with: `grep -in -E "SAP|RBIS|Oracle Retail|Retek|prior-art|canonical retail process|industry standard|industry-standard" <new-card.md>` — must return empty.

## Naming + casing convention (NON-NEGOTIABLE)

- Filename: `canary-module-{lowercase-letter}-functional-decomposition.md`
- Module H1: `# Module {UPPERCASE-LETTER} ({Name}) — Functional Decomposition`
- Sister-card cross-references in Related sections + frontmatter methodology-note: lowercase letter
- Add the **Artifact-layer block** under H1 (mandatory; copy from any existing card)

## Template-pick by cell shape

| Module | L1 cell | Template card to start from | Notes |
|---|---|---|---|
| **D** — Distribution | ◐ Partial (Document XFER + per-location inventory direct; transfer logic Canary-native) | `canary-module-o-functional-decomposition.md` | Partial-coverage shape; tag Canary-native vs substrate-supplied per L2 |
| **C** — Commercial / B2B | ◐ Derived (from R + AR + Customer fields + OpenItems) | `canary-module-o-functional-decomposition.md` | Derived module — first of its kind. May want to invent a "derived module" sub-template here. Most L3s read from R + F substrate; minimal own-data; light L2 set (4-5 likely) |
| **P** — Pricing / Promotion | ◐ Derived (from Item prices + CustomerControl multi-tier flags + per-line PS_DOC_LIN_PRICE) | `canary-module-o-functional-decomposition.md` | Derived module. Cross-cuts heavily with J (J.8 promotional-isolation) and Q (Q-DM family). Source: companion `Brain/wiki/retail-promotion-workflow.md` for promotion lifecycle (use as companion, NOT lineage) |
| **A** — Asset Management | ◐ Derived (from Item flags — ITEM_TYP, asset/non-saleable indicators) | `canary-module-o-functional-decomposition.md` | Lightest derived module; small L2 set (3-4 likely). Per Solution Map: SMB scale rarely needs deep asset coverage — keep scope honest |
| **L** — Labor / Workforce | ✗ → ★ Canary-native option (d) OR ◯ External vendor (Homebase/Deputy/etc) | `canary-module-q-functional-decomposition.md` IF building ★; new template needed IF ◯ | **STRATEGIC DECISION REQUIRED before drafting.** Bart Monday call (2026-04-27 1pm PST) is the natural surface for this. Memory `project_canary_native_labor_module_opportunity.md` holds prior thinking. Flag in dispatch comment if you proceed without the decision. |
| **W** — Work Execution | ✗ → ★ Canary-native option (d) OR ◯ External vendor (Beekeeper/YOOBIC/etc) | Same as L | Same strategic decision. L and W are likely answered together. |

## Per-module quick-context cards

Below — for each remaining module — the source artifacts the new functional-decomp card should pull from. These are the same `Brain/wiki/*` entries the existing cards reference.

### D — Distribution

- **Counterpoint coverage:** `Inventory_ByLocation`, `InventoryControl`, `InventoryCost`, `InventoryEC`, `InventoryLocations`, `Items_ByLocation`, `Item_Inventory`, plus DOC_TYP=XFER through Document family
- **L1 cell rationale:** ◐ Partial — per-location inventory snapshots are direct; transfer workflow runs through Document omnibus (no dedicated transfer endpoint); transfer-loss pattern detection is Canary-native
- **L2 sketch (6-7):** D.1 inventory snapshot ingestion / D.2 per-location item attribution / D.3 transfer detection (DOC_TYP=XFER) / D.4 transfer-loss reconciliation / D.5 multi-store distribution recommendations (Canary-native) / D.6 cross-module substrate contracts
- **Companion cards:** `retail-merchandise-planning-otb.md` (allocation methods + pre-pack), `retail-po-from-plan.md` (allocation-to-PO + short-ship), `garden-center-operating-reality.md` (multi-store transfer reality)
- **Q cross-cuts:** Q-IS-03 (transfer-loss pattern) reads from D
- **Existing Canary wiki:** `Brain/wiki/canary-module-d-distribution.md` (if exists; check via Glob)

### C — Commercial / B2B

- **Counterpoint coverage:** None dedicated; derived from `AR_CUST.CATEG_COD` (tier), `AR_CUST_CTL` (multi-tier flags), `AR_CUST.NO_CR_LIM`/`CR_RATE`/`BAL`, `Customer_OpenItems` (AR aging), customer behavior pattern from T
- **L1 cell rationale:** ◐ Derived — no own endpoints; reads R + F substrate
- **L2 sketch (4-5):** C.1 B2B classification derivation / C.2 per-customer credit posture / C.3 AR ledger surface (cross-cut with F.6) / C.4 B2B-specific Q rules (cross-cut with Q) / C.5 cross-module contracts
- **Companion cards:** `garden-center-operating-reality.md` (landscaper / wholesale / project tier reality)
- **R cross-cuts:** Inherits R.2 (tier identity), R.3 (loyalty + AR), R.6 (investigator surface)
- **F cross-cuts:** Inherits F.6 (AR ledger), F.6.5 (B2B credit decisioning hooks)
- **Existing Canary wiki:** `Brain/wiki/canary-module-m-merchandising.md`

### P — Pricing / Promotion

- **Counterpoint coverage:** No Pricing or Promotion endpoint family. Derived from Item prices (`IM_ITEM.PRC_1`, `REG_PRC`, `PREF_UNIT_PRC_1`, `LST_COST`), CustomerControl multi-tier flags, per-line `PS_DOC_LIN_PRICE` (the OUTPUT of pricing rules captured per ticket)
- **L1 cell rationale:** ◐ Derived — observes pricing decisions, doesn't model rules
- **L2 sketch (5-6):** P.1 multi-tier price derivation / P.2 promotion lifecycle (Canary-native — references retail-promotion-workflow.md) / P.3 markdown management / P.4 elasticity tracking / P.5 mass maintenance + linked items / P.6 cross-module contracts (J.8 promotional-isolation, Q.2.1 discount-and-markdown family)
- **Companion cards:** `retail-promotion-workflow.md` (entire lifecycle — companion not lineage), `retail-merchandise-planning-otb.md` (OTB cross-cut)
- **J cross-cuts:** J.3 (OTB), J.8 (promotional-vs-base-demand isolation)
- **Q cross-cuts:** Q-DM-01/02/03 read pricing decisions; Q-MM-01 reads bundle pricing
- **Existing Canary wiki:** `Brain/wiki/canary-module-p-pricing-promotion.md`

### A — Asset Management

- **Counterpoint coverage:** None dedicated; derived from `IM_ITEM.ITEM_TYP` (`I` inventory / `N` non-inventory), STAT, asset-flag patterns
- **L1 cell rationale:** ◐ Derived — view over S
- **L2 sketch (3-4):** A.1 asset-item identification (derived from S) / A.2 asset lifecycle tracking (derived from movement) / A.3 cross-module contracts
- **Companion cards:** Minimal — A is a thin module
- **Existing Canary wiki:** `Brain/wiki/canary-module-a-asset-management.md`
- **Note:** Per Solution Map specialty-smb proof case, A is "use Counterpoint derived — asset-tracking depth not typically needed at SMB scale." Keep scope honest; don't over-decompose.

### L — Labor / Workforce

- **Counterpoint coverage:** ✗ Zero. No Employee, Timeclock, or Schedule endpoints. (`User`/`Role` endpoints are API-server access management, not labor.)
- **Strategic options:**
  - (a) Defer — leave gap open
  - (d) ★ Canary-native build — POS-data-native scheduling, one-stop-shop wedge
  - (◯) External vendor — Homebase / Deputy / When I Work / TimeForge
- **DECISION REQUIRED before drafting.** Surface via Bart Monday call. Reference memories: `project_canary_native_labor_module_opportunity.md`, `project_canary_canonical_positioning.md`.
- **If decision = ★:** template from Q card (Canary-native shape); L2s likely include workforce ingestion / scheduling / forecast-integration / labor-cost-reconciliation / surface
- **If decision = ◯:** invent the ◯ template — first of its kind; L2s would be vendor-data-ingest / Canary-side projection / cross-module surface

### W — Work Execution

- **Counterpoint coverage:** ✗ Zero. No task / checklist / workflow surface.
- **Strategic options:** Same as L (defer / ★ native / ◯ external)
- **External alternatives:** Beekeeper, YOOBIC, Foko Retail
- **DECISION REQUIRED — likely answered jointly with L.**

## Recommended sequence

1. **D first** (clean partial-coverage shape; mirrors J template; ~1 card)
2. **A second** (smallest derived module; warm-up for the C and P derived shape; ~1 small card)
3. **C and P third** (parallel batch — both ◐ derived; can be cranked together; ~2 cards)
4. **L and W last** (require strategic decision from Bart Monday; defer until decision made)

After D + A + C + P are done, **11 of 13 modules are decomposed** with consistent format. L and W close the matrix once the strategic decision is made.

## Acceptance criteria per card

- [ ] Filename: `canary-module-{lowercase-letter}-functional-decomposition.md` in `/Users/gclyle/GrowDirect/Brain/wiki/`
- [ ] Frontmatter complete (matches existing card pattern)
- [ ] Artifact-layer block under H1
- [ ] Governing thesis with explicit L1 cell rationale
- [ ] Executive summary table with quantified counts
- [ ] L1→L2→L3 framework block
- [ ] L2 sections each with: Purpose / L3 process table / User stories / Companion cards
- [ ] Substrate contract registry section (last L2 or its own section)
- [ ] Assumption markers tagged `ASSUMPTION-{LETTER}-NN` with what-it-blocks + resolution-path
- [ ] Customer-specific overrides format (reserved, empty)
- [ ] Operating notes with cast of actors
- [ ] Related section linking to companion cards + sister cards
- [ ] **Lineage scrub clean** — `grep -in -E "SAP|RBIS|Oracle Retail|Retek|prior-art|canonical retail process|industry standard|industry-standard"` returns empty
- [ ] Cross-card references use lowercase letters

## State of the matrix at this dispatch

| Module | L1 cell | Status |
|---|---|---|
| Q | ★ Canary native | ✓ done |
| T | ● Full direct | ✓ done |
| R | ● Full direct | ✓ done |
| J | ◐ Partial | ✓ done |
| S | ● Full direct | ✓ done |
| F | ● Full direct | ✓ done |
| N | ● Full direct | ✓ done |
| **D** | **◐ Partial** | **PENDING — this dispatch** |
| **C** | **◐ Derived** | **PENDING — this dispatch** |
| **P** | **◐ Derived** | **PENDING — this dispatch** |
| **A** | **◐ Derived** | **PENDING — this dispatch** |
| **L** | **★ or ◯ (decision needed)** | **PENDING — this dispatch + strategic decision** |
| **W** | **★ or ◯ (decision needed)** | **PENDING — this dispatch + strategic decision** |

## Bart Monday context (2026-04-27 1pm PST)

The Bart call is the natural surface for two things this dispatch needs:

1. **L and W strategic decision** — VAR-channel partner's view on what L&G customers pay for separately
2. **Assumption-marker discovery agenda** — 71 markers across the 7 completed cards; highest-leverage gaps (Q-05, Q-12, T-01/02/06, R-03, J-06, J-08, S-04, S-07, F-01, F-03, N-02) need real-customer or partner input

Reference: `Brain/wiki/socal-home-garden-target-customers-brief.md` for the call-prep brief.

## Companion artifacts (read once for context)

- `CATz/method/artifacts/module-functional-decomposition.md` — formal template (just promoted)
- `CATz/method/artifacts/solution-map.md` — L1 artifact this card sits below
- `CATz/proof-cases/specialty-smb-counterpoint-solution-map.md` — Solution Map proof-case for the Counterpoint archetype
- `Brain/wiki/retail-merchandise-planning-otb.md` — OTB / planning pyramid (companion for J, P)
- `Brain/wiki/retail-po-from-plan.md` — PO chain (companion for J, D)
- `Brain/wiki/retail-promotion-workflow.md` — promotion lifecycle (companion for P, J.8)
- `Brain/wiki/garden-center-operating-reality.md` — vertical context across all modules
- `Brain/wiki/ncr-counterpoint-rapid-pos-relationship.md` — feature-to-API mapping
- `Brain/wiki/canary-module-q-counterpoint-rule-catalog.md` — 23-rule Q catalog (substrate for Q's L2/L3)

## Out of scope for this dispatch

- Sharpening the Solution Map proof-case (separate pass after all 13 cards land)
- Drafting the L1 code/schema crosswalk wikis for Q/T/R (the 2nd artifact-layer for those modules — the existing Brain wiki carries J/P/F/C but not Q/T/R)
- Writing SDDs for the new module cards (L4 work; lives in Canary product repo)
- Bart Monday call execution

## Completion

Comment on this dispatch (in Linear if Linear-tracked, or as a follow-up dispatch file) listing:
- Cards completed (filenames)
- Cards deferred (with reason — e.g., "L deferred pending Bart Monday")
- Lineage-scrub pass result
- Any new ASSUMPTION-* markers worth surfacing immediately
- One-paragraph synthesis: format held / drift observed / template improvements suggested

## Related dispatches

- `Brain/dispatches/2026-04-25-tsp-crdm-counterpoint-flow.md` — Phase 0 (engineering)
- `Brain/dispatches/2026-04-25-ncr-counterpoint-priority-modules.md` — Phase 1 (engineering)
- `Brain/dispatches/2026-04-25-ncr-counterpoint-tertiary-modules.md` — Phase 4 (engineering — Q + A + C SDD/build work)
- This dispatch is **methodology-track** (CATz Phase II artifact filling), not engineering-track. Both run in parallel.
