---
type: cowork-prompt
status: ready
created: 2026-05-04
audience: Cowork (strategic session)
---

# Cowork Prompt — Sprint Planning: Next Capability Round + Vault Updates

## Context You Need First

Canary is a store operations platform for independent retailers on NCR Counterpoint / RapidPOS. Before planning, read in order:

1. **`Brain/projects/Canary.md`** — full project MOC
2. **`Brain/wiki/cards/store-ops-capability-model.md`** — 7-layer capability synthesis; the build map
3. **CATz vault** — `gh repo clone growdirect-llc/catz /tmp/catz-$$ && ls /tmp/catz-$$/method/` — the delivery framework that drives sequencing
4. **`AGENTS.md`** at repo root — current build state (29 services, 18 capability cards in memory bus)

**Current state as of 2026-05-04:**

- 18 store ops capability cards committed to Brain/wiki/cards/ — enterprise intelligence (RDM/ORMS/RPAS/JDA/GAP) rewritten as Canary build specs
- CanaryGo has 29 Go services implemented; the code has moved ahead of the SDDs — SDDs are documentation debt, not a gate
- Three public vaults: CATz (`catz.growdirect.io`), CRB (`crb.growdirect.io`), NCR (`ncr.growdirect.io`)

---

## What This Session Produces

### 1. Sprint Plan — Next Capability Round

Using the CATz method as the sequencing frame, plan the next round of capability work. The 18 cards define the full store ops surface. The question is which capabilities need to be built or completed to deliver a fully operational store on Canary end to end.

Ground the plan in:
- What a store running on NCR Counterpoint / RapidPOS needs to be fully operational on Canary — receiving, replenishment, task queue, ordering, SOH, reporting
- What the CATz method says about delivery sequencing for the VAR channel
- What is built vs. thin or missing — compare the capability cards against the service list in AGENTS.md
- Build priority rankings at the bottom of each capability card

Output:
- A prioritized capability list (up to 8 items) for the next 4-6 weeks
- For each: one sentence on why it's next, grounded in operational completeness
- Which Linear GRO tickets need to be filed or already exist

### 2. CRB Update — Canary Retail Brain

Six of the 18 new capability cards are ready for the CRB vault. Assess each and push the ones that are ready.

**Candidates:**
- `canary-operations-hub` — hub layout, exception queue, watch list
- `canary-android-pos-integration` — NCR Counterpoint REST integration architecture
- `canary-item-master-and-catalog` — 3-level hierarchy, scan-to-lookup, e-catalog
- `canary-multi-store-intelligence` — portfolio hub, transfer orders
- `canary-space-range-display-on-floor` — live planogram, range status lifecycle, POS location lookup
- `canary-evidentiary-rail` — 4-tier storage, Bitcoin L2 anchor

**Not for CRB:** labor/shift management (internal), demand sensing (formula detail), mobile task UX flows (implementation spec).

Push protocol:
```bash
gh repo clone growdirect-llc/canary-retail-brain /tmp/crb-$$
# copy curated cards from Brain/wiki/cards/ into /tmp/crb-$$/
git -C /tmp/crb-$$ add -A && git -C /tmp/crb-$$ commit -m "content: store ops capability cards" && git -C /tmp/crb-$$ push
rm -rf /tmp/crb-$$
```

### 3. NCR Vault Update

The NCR vault (`ncr.growdirect.io`) serves NCR Counterpoint resellers. It needs to reflect the new capability layer.

Clone and assess: `gh repo clone growdirect-llc/ncr /tmp/ncr-$$`

The Android POS integration card and the operations hub card are the most relevant to an NCR Counterpoint audience. Also check whether the existing module decomposition pages (M, E, F, L, etc.) need updating to reference the capability cards.

### 4. Canary Go Portal Update

The Canary Go Portal (`Brain/wiki/canary-go-portal.md`) is the internal project entry point — it indexes SDDs, Linear links, and build state.

Update it to:
- Reference the 18 new store ops capability cards and the new section in the Canary MOC
- Note that the SDD library is trailing the code — capability cards are the authoritative functional spec
- Confirm the service count and module state match AGENTS.md

---

## Constraints

- Vault content flows GrowDirect → public vaults — never edit vault repos directly; update Brain first
- No named clients in vault content — deployment archetypes only
- CATz method drives sequencing — prioritize by operational completeness, not technical interest
- Code is ahead of SDDs — compare against capability cards, not the SDD library
- No hype copy — every card pushed to a public vault should read as if written for a technical operator, not a pitch deck

---

## Output

Sprint plan at: `docs/superpowers/plans/2026-05-04-capability-sprint-plan.md`

Vault update summary at: `docs/superpowers/plans/2026-05-04-vault-update-summary.md`

File Linear dispatches before closing.
