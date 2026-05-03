# 09 — Anti-Patterns

The failure modes prior governance experiments produced, named explicitly, with the substrate's structural correction cross-referenced. Every check in `07-alignment-checks.md` exists because one of these failure modes was real enough to harm real people.

## Why this document is normative

The architecture is not theoretical. The founder has run a version of this play before, in a venture that ended badly enough to make the structural corrections load-bearing. Other governance experiments — Bitcoin's blocksize wars, the DAO of 2016, multiple venture-backed startups absorbed by PE consolidation — produced the same failure modes from different angles. We name them. We cross-reference the substrate mechanism that prevents each. We do not re-litigate. We do not assume good intent will hold against structural pressure.

If a proposed bylaws revision quietly reintroduces any of the patterns below, the alignment checks in `07-alignment-checks.md` flag it. The trusted network may still ratify the change — but they do so consciously, having seen the conflict named.

## A. HR-as-PE-culling

**Prior failure mode.** A traditional HR function, layered on top of an operating company, becomes the mechanism by which a financial sponsor (PE firm, late-stage acquirer) culls headcount on acquisition. The function exists to enforce "fairness" in headcount decisions; in practice the criteria flex to the sponsor's cost-reduction targets. Seven-figure HR spend produces negative cultural value (employees experience the function as adversarial) while serving the sponsor's downside-protection model. The function cannot be reformed — its structural role in the cap-table dynamics is what produces the harm.

**Substrate correction.** The eljeffe Hash and Seal Protocol substrate has no HR function. Contributor relationships are encoded in smart contracts. Onboarding is the trusted-network invitation + first MCP-published contribution + smart-contract-issued auth token. Performance is observable in token-earn rate and DAO-action-stamping density. Off-boarding is the contributor stopping work and the smart contract reflecting the absence; their existing tokens remain theirs (lineage permanence per `02-genesis-ordinal-mechanics.md`). There is no central function to weaponize because the function does not exist.

**Cross-reference.** Alignment check 17 (`07-alignment-checks.md` E.17). Treasury mechanics in `03-dao-treasury-patterns.md` (no salary line for an HR department because no HR department).

## B. Vesting-cliff dilution

**Prior failure mode.** Traditional 4-year vesting with a 1-year cliff means contributors who join early earn nothing for a year, then earn linearly over three years. On PE acquisition, a sponsor frequently strips unvested equity (re-vesting on new terms; replacement of the old plan with a sponsor-friendly plan). The contributor's effective dilution is acute; the "long-term-aligned" framing collapses. Even absent acquisition, the cliff structurally penalizes the contributor most exposed to early risk.

**Substrate correction.** The substrate is structurally cliff-free. Token-earn begins at first contribution; per-contribution sat flow is permanent (per `03-dao-treasury-patterns.md` cash-out categories); no clawback is possible because the chain doesn't allow it. A founder cannot "decide" to claw back tokens earned by a contributor; the smart contract has no clawback function (alignment check 3 ensures no proposed bylaws clause introduces one).

**Cross-reference.** Alignment check 3 (A.3); `02-genesis-ordinal-mechanics.md` lineage permanence; `03-dao-treasury-patterns.md` token-earn → categorized cash-out.

## C. Retainer-legal extraction

**Prior failure mode.** A general counsel function on retainer, or an outside law firm with a retained relationship, produces an incentive to find work to do. Routine matters get escalated; opinion letters proliferate; the legal spend grows in line with the firm's billable-hours target rather than the entity's actual legal exposure. The function becomes a quiet cost line that compounds; sponsor-favorable interpretations of grey areas accumulate; the entity's risk posture drifts toward whatever the firm's other clients prefer.

**Substrate correction.** The substrate uses point-in-time engaged counsel for specific filings — Wyoming entity formation, IP contribution agreement, securities-law analysis if/when token mechanics implicate it, banking relationship facilitation. Each engagement is scoped to the deliverable; the engagement ends when the filing lands. There is no retained relationship; there is no general counsel function. When recurring legal work surfaces (which it will), it surfaces as a contributor-tier engagement against a specific MCP-published service, with token-earn for the work and visibility into the cost via the treasury transparency mechanism (per `03-dao-treasury-patterns.md`).

**Cross-reference.** Alignment check 17 (E.17 — substrate is intentionally department-free); compliance integrity checks 14-16 (E.14-E.16 — substrate-to-auditor translation is a contributor-tier service, not a retained department).

## D. Shared-services-as-extraction

**Prior failure mode.** Consolidated finance, IT, procurement, and HR shared-services functions, sold internally as efficiency-producing, become the operational layer that PE acquirers use to extract margin. The shared function reports up to corporate development rather than to the operating units it serves; cost allocations drift toward the sponsor's preferred numerator; the operating unit loses visibility into its own cost basis. The function is structurally extraction-aligned even when staffed by well-intentioned individuals.

**Substrate correction.** Anti-shared-services is a structural posture. Each namespace runs its own treasury (per `03-dao-treasury-patterns.md`); each namespace has its own bylaws (per the structure of this skill); each namespace's contributor relationships are namespace-specific (per `02-genesis-ordinal-mechanics.md` lineage scope). Cross-namespace coordination, when necessary, happens through inter-namespace governance proposals (Phase 3 per `05-phase-transitions.md`), not through a shared central function. There is no "Growdirect Shared Services" entity. There is no shared HR. There is no shared finance. The substrate handles the function; the namespace owns its own data.

**Cross-reference.** Alignment check 17 (E.17); treasury per-namespace scope in `03-dao-treasury-patterns.md`; phase-3 inter-namespace coordination in `05-phase-transitions.md`.

## E. Founder-displacement-by-board-engineering

**Prior failure mode.** A founder builds an operating venture; takes outside capital; the cap table acquires multiple board seats representing the new investors; over multiple rounds the board composition shifts; the board eventually has the votes to displace the founder operationally even though the founder still holds material equity. The displacement happens through procedural maneuvers (board reconstitution, special-committee formation, executive-session resolutions) that are individually defensible and collectively a coup.

**Substrate correction.** Board-equivalent authority on the substrate is genesis-tier ordinal-holder voting weight (per `04-lineage-weighted-voting.md`). Genesis-tier holders carry full weight (1.0) permanently; weight does not decay with time. New ordinals issued post-genesis carry first-tier weight (0.667 with default α = 0.5) at most. Founder-tier voting weight cannot be diluted by issuing new ordinals; it can only be diluted by the founder voluntarily transferring or selling their genesis ordinals. Phase 2 governance can vote to remove a founder from operational roles (e.g., end the President of Retail engagement) under super-majority threshold + cause documentation per `05-phase-transitions.md` — but the founder *retains their ordinals and voting weight*. Their stake is not clawed back. Their operational role can be ended; their position in the lineage cannot be erased.

**Cross-reference.** Alignment checks 12-13 (D.12-D.13); founder removal protections in `05-phase-transitions.md`.

## F. Whale-capture-via-token-accumulation

**Prior failure mode.** In standard one-token-one-vote DAO governance, an entity that accumulates a majority of tokens captures governance regardless of contribution. Vitalik's coin-voting critique is the canonical reference. The accumulator may have purchased their tokens on a secondary market, never having contributed work or risk to the namespace; the accumulator nonetheless gains controlling voting weight. The DAO's governance becomes a function of capital concentration rather than of the namespace's trusted network.

**Substrate correction.** Voting weight is lineage-weighted, not token-weighted (per `04-lineage-weighted-voting.md`). A holder accumulating ordinals at a lower tier does not gain genesis-tier weight; they gain their tier's weight × the count of ordinals at that tier. By tier 5, an ordinal is worth ~33% of a genesis ordinal; by tier 10, ~17%. Accumulating thousands of tier-10 ordinals does not produce founder-tier authority. Sybil attacks fail because lineage is on-chain provenance — splitting a wallet doesn't create new lineage.

**Cross-reference.** Alignment check 10 (C.10 — whale-capture structurally prevented); voting formula and rationale in `04-lineage-weighted-voting.md`.

## G. Governance-by-quorum-manipulation

**Prior failure mode.** Small motivated factions discover that a quorum of 30% (or whatever the threshold) can be reliably assembled by their faction while the broader membership is passive. Proposals that the broader membership would reject pass because the broader membership doesn't show up. Over time, the faction-controlled outcomes accumulate; the broader membership disengages further; the namespace's effective governance is captured by the most motivated minority.

**Substrate correction.** Lineage-weighted quorum requirements are calibrated per proposal type per `04-lineage-weighted-voting.md` — operational decisions at 30%, structural amendments at 50%, founder-tier amendments at 67%. Higher-stakes decisions require higher quorum. The lineage-weighted formula also means a passive holder doesn't artificially distort outcomes (their non-vote counts toward quorum-pool size but not toward yes/no totals); apathy depresses participation but doesn't bias the result. Beyond that, the periodic alignment review (per `07-alignment-checks.md` final section) explicitly asks the trusted network whether quorum thresholds are still right; threshold adjustments themselves require structural-amendment votes.

**Cross-reference.** Alignment check 10 (C.10); quorum mechanics in `04-lineage-weighted-voting.md`; periodic alignment review in `07-alignment-checks.md`.

## H. Customer-data harvesting under TOS cover

**Prior failure mode.** A platform's terms of service are written broadly enough to permit aggregation, anonymization, and resale of customer data. The customer agrees to the TOS as a condition of using the platform; the TOS evolve over time with customer-friendly framing of provisions that are platform-extractive in operation. The customer's effective data sovereignty is zero; the platform's revenue from data productization is material.

**Substrate correction.** Customer-owned data is structural (per `06-cultural-technical-mapping.md` Article XI mapping; `03-dao-treasury-patterns.md` data-sharing earnings flow to *customers*). Per-tenant cryptographic isolation means the platform structurally holds no aggregable customer data. Cross-customer use requires DAO ratification with stake-weighted vote — which means customers themselves vote on whether their cohort's data participates in any cross-customer analysis. A bylaws clause permitting platform-level data resale would fail alignment checks 5-7 (B.5-B.7) and could not be ratified without explicit override that itself becomes an on-chain governance event the customer base sees.

**Cross-reference.** Alignment checks 5-7 (B.5-B.7); customer-owned data architecture in companion skill `data-sovereignty-architecture` (per v2 prompt).

## I. Vest-then-strip on transition

**Prior failure mode.** Contributors vest equity over multiple years against the expectation that the equity will be valuable at exit. On acquisition, the sponsor restructures the equity (replacement plan with new vesting; sponsor-determined valuation that drops the strike price below the vested value; mandatory rollover into illiquid acquirer instruments). The contributor's realized return is a fraction of the headline vesting amount.

**Substrate correction.** Token-earn is not equity-vesting. Tokens are earned per contribution and inscribed permanently; sat-denominated cost basis means appreciation tracks Bitcoin appreciation (which is structural, not sponsor-determined); tokens can be cashed out per the categorized cash-out taxonomy (`03-dao-treasury-patterns.md`) at the contributor's discretion. There is no "exit event" that resets the model. There is no acquirer that can replace the substrate. The substrate is the substrate; the contributor's tokens remain theirs through any organizational evolution of the namespace operating company.

**Cross-reference.** Alignment checks 1-3 (A.1-A.3); token-earn flow in `03-dao-treasury-patterns.md`.

## J. Anti-trust-as-pretext-for-extraction

**Prior failure mode.** A platform claims anti-trust risk as the rationale for divesting profitable customer relationships, restructuring contractor arrangements, or exiting markets — when the actual driver is sponsor preference for asset-light financialization. The anti-trust framing is defensible enough to be hard to challenge externally; the operational impact is the loss of customer continuity, contributor relationships, and operating-unit identity.

**Substrate correction.** The substrate is structurally not a position from which anti-trust extraction is straightforward. Customer-owned data + DAO-governance + lineage-weighted voting means no central authority can unilaterally divest a customer relationship; the customer's ordinal tier and the customer's data sovereignty mean the relationship is not the platform's to dispose of. Compliance posture (per `data-sovereignty-architecture` companion skill) is documented for ISO 27001 + PCI-DSS + the relevant state privacy laws by construction; an anti-trust framing for restructuring would have to overcome the substrate's documented evidence rather than overlay a top-down narrative on a complicit operating company.

**Cross-reference.** Alignment checks 5-7 (B.5-B.7); compliance integrity checks 14-17 (E.14-E.17).

## How this document evolves

The list above is not closed. As the trusted network operates the substrate, new failure modes will surface — failure modes specific to particular namespaces, particular vertical applications, particular partner-network dynamics. Each new failure mode gets named here, with the substrate's structural correction cross-referenced (or, if no correction exists, flagged as an open architectural item for the trusted network's attention).

Adding a new anti-pattern is itself a bylaws amendment — the change goes through `08-iteration-loop.md`. Removing an anti-pattern requires structural-amendment threshold (≥75% lineage-weighted vote, ≥50% quorum) per `04-lineage-weighted-voting.md`. We can name new failure modes easily; we make it deliberately hard to forget the ones we've already named.

## Cross-references

- `02-genesis-ordinal-mechanics.md` — the lineage-permanence and DAO-action-stamping mechanisms that prevent E (founder-displacement), I (vest-then-strip)
- `03-dao-treasury-patterns.md` — the categorized cash-out and transparency-by-default mechanisms that prevent A (HR-as-PE-culling), B (vesting-cliff), C (retainer-legal), I (vest-then-strip)
- `04-lineage-weighted-voting.md` — the formula and quorum mechanics that prevent F (whale-capture), G (quorum-manipulation)
- `05-phase-transitions.md` — the time-bounded founder-mint phase and graceful-exit mechanics that prevent E (founder-displacement)
- `06-cultural-technical-mapping.md` — the two-layer discipline that prevents H (TOS-cover data harvesting) by making cultural intent the prevailing reading
- `07-alignment-checks.md` — the 23 checks that operationalize each anti-pattern's structural correction
- `08-iteration-loop.md` — how new anti-patterns get added to this document via the comment-and-revision loop
- v2 prompt failure-modes table — `outputs/prompt-crb-v2-operational-cto-entry.md` "Failure modes from prior run" section; this document expands and formalizes that table
