---
date: 2026-05-03
type: weekly-status
week: 2026-W18
week-start: 2026-04-27
week-end: 2026-05-03
author: Alejandro
status: draft
last-compiled: 2026-05-03
needs-review: 2026-05-17
tags: [weekly-status, status-report]
---

# Weekly Status — 2026-W18

> ABCD — Accomplishments · Benefits · Concerns · Do Next. The four-box is
> the narrative layer. The auto-rails below are the inventory layer. If
> the box at the top reads as a duplicate of the rails, the box failed.

## Governing thesis
<!-- One paragraph. The single most important thing about this week. -->

First instance of the weekly ABCD format. The capture system itself is now
in place — template, Bases trackers, auto-rail script. Next week's report
is the first one that exercises the system end-to-end.

## A · Accomplishments
<!-- What got done. Concrete, verifiable, one bullet per item. -->

- Shipped weekly status capture system: ABCD template, SDLC Tracker base,
  NFR Matrix base, `engine.py weekly` command (this dispatch).
- ALXjr sunset confirmed (per CLAUDE.md deprecation note dated 2026-05-01).
- Mini Docker stack parked (GRO-700 v3 drop-zone reframe, 2026-05-01).

## B · Benefits
<!-- Why it mattered. Outcomes, not activities. -->

- Friday cadence now has a single artifact rather than a mental note. Three
  weeks from now there's a trend line instead of a memory.
- Module-level SDLC visibility: 13 spine modules + cross-cutting NFR
  concerns rendered in one Bases view. No more "what state is module X in"
  ambiguity at the start of a planning session.
- ALXjr sunset and mini Docker park reduce operational surface area
  by one entire agent identity and one Docker stack — both were carrying
  weight without proportional output.

## C · Concerns
<!-- Risks, blockers, drift, things slipping. -->

- **MED:** Only 1 of 13 module entity cards exists (T as the worked
  example). The SDLC Tracker base will look sparse until the other 12 are
  scaffolded. Follow-up dispatch needed.
- **MED:** `engine.py weekly` Linear integration is stubbed — closed
  dispatches still need to be hand-pasted from Linear into the rail.
  Acceptable for v0.1; plan a v0.2 with `--linear-token` flag.
- **LOW:** Bases formula syntax (`if(...)`) for the NFR composite score is
  untested against current Obsidian Bases version. May need to fall back
  to flat columns if the formula doesn't parse.

## D · Do Next
<!-- Top 3-5 priorities for next week, ranked. -->

1. Scaffold the remaining 12 module entity cards (R, N, A, Q, C, D, F, J, S, P, L, W) — quick batch, ~30 min.
2. Validate Bases formula syntax in Obsidian — if `if(...)` chains don't render, simplify NFR Matrix.
3. Wire `engine.py weekly --with-linear` against the Linear MCP for the dispatch rail (v0.2).
4. First real Friday run of the weekly process — W19 status, end-to-end with auto-rails.

---

## Auto-rails
<!-- Populated by `engine.py weekly`. Re-run if stale. -->

### Dispatches closed this week
<!-- Linear MCP integration pending — see GRO dispatch. -->
_Hand-paste from Linear's Dispatch project, status=Done, completed-at between 2026-04-27 and 2026-05-03._

### Wiki cards added or updated

- [[agent-card-format]] (`Brain/wiki/agent-card-format.md`)
- [[armstrong-garden-centers-proof-case]] (`Brain/wiki/armstrong-garden-centers-proof-case.md`)
- [[bart-mccleskey-rapid-garden-pos]] (`Brain/wiki/bart-mccleskey-rapid-garden-pos.md`)
- [[brain-broken-links-baseline-2026-05-01]] (`Brain/wiki/brain-broken-links-baseline-2026-05-01.md`)
- [[canary-agent-roadmap-batch-to-realtime]] (`Brain/wiki/canary-agent-roadmap-batch-to-realtime.md`)
- [[canary-alerts-guide]] (`Brain/wiki/canary-alerts-guide.md`)
- [[canary-architecture-decisions-index]] (`Brain/wiki/canary-architecture-decisions-index.md`)
- [[canary-architecture]] (`Brain/wiki/canary-architecture.md`)
- [[canary-canonical-positioning]] (`Brain/wiki/canary-canonical-positioning.md`)
- [[canary-chirp-rules]] (`Brain/wiki/canary-chirp-rules.md`)
- [[canary-closed-loop-cost-attribution]] (`Brain/wiki/canary-closed-loop-cost-attribution.md`)
- [[canary-commercial-context]] (`Brain/wiki/canary-commercial-context.md`)
- [[canary-control-state-fit]] (`Brain/wiki/canary-control-state-fit.md`)
- [[canary-data-model]] (`Brain/wiki/canary-data-model.md`)
- [[canary-detection]] (`Brain/wiki/canary-detection.md`)
- [[canary-ej-spine-and-sales-audit]] (`Brain/wiki/canary-ej-spine-and-sales-audit.md`)
- [[canary-fox-case-management]] (`Brain/wiki/canary-fox-case-management.md`)
- [[canary-franchise-play]] (`Brain/wiki/canary-franchise-play.md`)
- [[canary-functional-decomp-gap-ledger]] (`Brain/wiki/canary-functional-decomp-gap-ledger.md`)
- [[canary-go-cadence-ladder]] (`Brain/wiki/canary-go-cadence-ladder.md`)
- [[canary-go-endpoint-library]] (`Brain/wiki/canary-go-endpoint-library.md`)
- [[canary-go-ncr-counterpoint-crosswalk]] (`Brain/wiki/canary-go-ncr-counterpoint-crosswalk.md`)
- [[canary-go-portal]] (`Brain/wiki/canary-go-portal.md`)
- [[canary-go-rapidpos-crosswalk]] (`Brain/wiki/canary-go-rapidpos-crosswalk.md`)
- [[canary-go-satoshi-cost-model]] (`Brain/wiki/canary-go-satoshi-cost-model.md`)
- [[canary-go-square-crosswalk]] (`Brain/wiki/canary-go-square-crosswalk.md`)
- [[canary-go-vs-gk-pos-gap-analysis]] (`Brain/wiki/canary-go-vs-gk-pos-gap-analysis.md`)
- [[canary-location-item-data-model]] (`Brain/wiki/canary-location-item-data-model.md`)
- [[canary-long-arc-atlas]] (`Brain/wiki/canary-long-arc-atlas.md`)
- [[canary-market-positioning]] (`Brain/wiki/canary-market-positioning.md`)
- [[canary-mcp-stack-architecture]] (`Brain/wiki/canary-mcp-stack-architecture.md`)
- [[canary-module-a-asset-management]] (`Brain/wiki/canary-module-a-asset-management.md`)
- [[canary-module-a-functional-decomposition]] (`Brain/wiki/canary-module-a-functional-decomposition.md`)
- [[canary-module-c-commercial]] (`Brain/wiki/canary-module-c-commercial.md`)
- [[canary-module-c-customer]] (`Brain/wiki/canary-module-c-customer.md`)
- [[canary-module-c-functional-decomposition]] (`Brain/wiki/canary-module-c-functional-decomposition.md`)
- [[canary-module-d-distribution]] (`Brain/wiki/canary-module-d-distribution.md`)
- [[canary-module-d-functional-decomposition]] (`Brain/wiki/canary-module-d-functional-decomposition.md`)
- [[canary-module-e-execution]] (`Brain/wiki/canary-module-e-execution.md`)
- [[canary-module-f-finance]] (`Brain/wiki/canary-module-f-finance.md`)
- [[canary-module-f-functional-decomposition]] (`Brain/wiki/canary-module-f-functional-decomposition.md`)
- [[canary-module-j-forecast-order]] (`Brain/wiki/canary-module-j-forecast-order.md`)
- [[canary-module-l-labor-workforce]] (`Brain/wiki/canary-module-l-labor-workforce.md`)
- [[canary-module-l-labor]] (`Brain/wiki/canary-module-l-labor.md`)
- [[canary-module-m-functional-decomposition]] (`Brain/wiki/canary-module-m-functional-decomposition.md`)
- [[canary-module-m-merchandising]] (`Brain/wiki/canary-module-m-merchandising.md`)
- [[canary-module-n-device]] (`Brain/wiki/canary-module-n-device.md`)
- [[canary-module-n-functional-decomposition]] (`Brain/wiki/canary-module-n-functional-decomposition.md`)
- [[canary-module-o-functional-decomposition]] (`Brain/wiki/canary-module-o-functional-decomposition.md`)
- [[canary-module-o-orders]] (`Brain/wiki/canary-module-o-orders.md`)
- [[canary-module-p-functional-decomposition]] (`Brain/wiki/canary-module-p-functional-decomposition.md`)
- [[canary-module-p-pricing-promotion]] (`Brain/wiki/canary-module-p-pricing-promotion.md`)
- [[canary-module-q-counterpoint-rule-catalog]] (`Brain/wiki/canary-module-q-counterpoint-rule-catalog.md`)
- [[canary-module-q-functional-decomposition]] (`Brain/wiki/canary-module-q-functional-decomposition.md`)
- [[canary-module-q-loss-prevention]] (`Brain/wiki/canary-module-q-loss-prevention.md`)
- [[canary-module-r-customer]] (`Brain/wiki/canary-module-r-customer.md`)
- [[canary-module-r-functional-decomposition]] (`Brain/wiki/canary-module-r-functional-decomposition.md`)
- [[canary-module-s-functional-decomposition]] (`Brain/wiki/canary-module-s-functional-decomposition.md`)
- [[canary-module-s-space-range-display]] (`Brain/wiki/canary-module-s-space-range-display.md`)
- [[canary-module-s-space]] (`Brain/wiki/canary-module-s-space.md`)
- [[canary-module-t-transactions]] (`Brain/wiki/canary-module-t-transactions.md`)
- [[canary-module-w-work-execution]] (`Brain/wiki/canary-module-w-work-execution.md`)
- [[canary-sales-strategy]] (`Brain/wiki/canary-sales-strategy.md`)
- [[canary-site-update-instructions]] (`Brain/wiki/canary-site-update-instructions.md`)
- [[canary-tsp-pipeline]] (`Brain/wiki/canary-tsp-pipeline.md`)
- [[accelerator-pack]] (`Brain/wiki/canary/accelerator-pack.yaml`)
- [[investor-deck-recovery-2026-05-03]] (`Brain/wiki/canary/investor-deck-recovery-2026-05-03.md`)
- [[joint-product-positioning-pwc]] (`Brain/wiki/canary/partnership-research/joint-product-positioning-pwc.md`)
- [[rapidpos-feature-map]] (`Brain/wiki/canary/partnership-research/rapidpos-feature-map.md`)
- [[rapidpos-subbrand-feature-map]] (`Brain/wiki/canary/partnership-research/rapidpos-subbrand-feature-map.md`)
- [[agent-alxjr-decision]] (`Brain/wiki/cards/agent-alxjr-decision.md`)
- [[agent-auditor]] (`Brain/wiki/cards/agent-auditor.md`)
- [[agent-canary-builder]] (`Brain/wiki/cards/agent-canary-builder.md`)
- [[agent-cove-builder]] (`Brain/wiki/cards/agent-cove-builder.md`)
- [[axis-adapter]] (`Brain/wiki/cards/axis-adapter.md`)
- [[axis-agent]] (`Brain/wiki/cards/axis-agent.md`)
- [[axis-resource]] (`Brain/wiki/cards/axis-resource.md`)
- [[canary-asset]] (`Brain/wiki/cards/canary-asset.md`)
- [[canary-blockchain-anchor]] (`Brain/wiki/cards/canary-blockchain-anchor.md`)
- [[canary-commercial]] (`Brain/wiki/cards/canary-commercial.md`)
- [[canary-compliance]] (`Brain/wiki/cards/canary-compliance.md`)
- [[canary-cost-center-cross-charge]] (`Brain/wiki/cards/canary-cost-center-cross-charge.md`)
- [[canary-customer]] (`Brain/wiki/cards/canary-customer.md`)
- [[canary-device-contracts]] (`Brain/wiki/cards/canary-device-contracts.md`)
- [[canary-ecom-channel]] (`Brain/wiki/cards/canary-ecom-channel.md`)
- [[canary-employee]] (`Brain/wiki/cards/canary-employee.md`)
- [[canary-field-capture]] (`Brain/wiki/cards/canary-field-capture.md`)
- [[canary-hawk]] (`Brain/wiki/cards/canary-hawk.md`)
- [[canary-ildwac]] (`Brain/wiki/cards/canary-ildwac.md`)
- [[canary-inventory-as-a-service]] (`Brain/wiki/cards/canary-inventory-as-a-service.md`)
- [[canary-inventory]] (`Brain/wiki/cards/canary-inventory.md`)
- [[canary-item]] (`Brain/wiki/cards/canary-item.md`)
- [[canary-l402-otb]] (`Brain/wiki/cards/canary-l402-otb.md`)
- [[canary-meter-model-token-plan]] (`Brain/wiki/cards/canary-meter-model-token-plan.md`)
- [[canary-ops-dashboard]] (`Brain/wiki/cards/canary-ops-dashboard.md`)
- [[canary-pricing]] (`Brain/wiki/cards/canary-pricing.md`)
- [[canary-protocol-gateway-live-on-gcp]] (`Brain/wiki/cards/canary-protocol-gateway-live-on-gcp.md`)
- [[canary-raas]] (`Brain/wiki/cards/canary-raas.md`)
- [[canary-receiving]] (`Brain/wiki/cards/canary-receiving.md`)
- [[canary-report]] (`Brain/wiki/cards/canary-report.md`)
- [[canary-returns]] (`Brain/wiki/cards/canary-returns.md`)
- [[canary-store-brain]] (`Brain/wiki/cards/canary-store-brain.md`)
- [[canary-store-network-integrity]] (`Brain/wiki/cards/canary-store-network-integrity.md`)
- [[canary-transfer]] (`Brain/wiki/cards/canary-transfer.md`)
- [[category-hierarchy]] (`Brain/wiki/cards/category-hierarchy.md`)
- [[channel-revshare-architecture]] (`Brain/wiki/cards/channel-revshare-architecture.md`)
- [[concept-agent-parenting-discipline]] (`Brain/wiki/cards/concept-agent-parenting-discipline.md`)
- [[concept-decision-substrate]] (`Brain/wiki/cards/concept-decision-substrate.md`)
- [[concept-identity-layer-triad]] (`Brain/wiki/cards/concept-identity-layer-triad.md`)
- [[concept-party-taxonomy]] (`Brain/wiki/cards/concept-party-taxonomy.md`)
- [[concept-substrate-discipline]] (`Brain/wiki/cards/concept-substrate-discipline.md`)
- [[counterpoint-product-state-2026]] (`Brain/wiki/cards/counterpoint-product-state-2026.md`)
- [[counterpoint-var-landscape]] (`Brain/wiki/cards/counterpoint-var-landscape.md`)
- [[diagnostic-five-input-forecast]] (`Brain/wiki/cards/diagnostic-five-input-forecast.md`)
- [[fireball-demand-signal-origin]] (`Brain/wiki/cards/fireball-demand-signal-origin.md`)
- [[gap-backbone-architecture]] (`Brain/wiki/cards/gap-backbone-architecture.md`)
- [[gcp-foundation-runbook]] (`Brain/wiki/cards/gcp-foundation-runbook.md`)
- [[geography-hierarchy]] (`Brain/wiki/cards/geography-hierarchy.md`)
- [[gslm-coverage-report-2026-05-03]] (`Brain/wiki/cards/gslm-coverage-report-2026-05-03.md`)
- [[icp-murdochs-reference]] (`Brain/wiki/cards/icp-murdochs-reference.md`)
- [[ilwac-extended-bitcoin-standard]] (`Brain/wiki/cards/ilwac-extended-bitcoin-standard.md`)
- [[infra-blockchain-evidence-anchor]] (`Brain/wiki/cards/infra-blockchain-evidence-anchor.md`)
- [[infra-cadence-ladder]] (`Brain/wiki/cards/infra-cadence-ladder.md`)
- [[infra-dns-topology]] (`Brain/wiki/cards/infra-dns-topology.md`)
- [[infra-feed-tier-contract]] (`Brain/wiki/cards/infra-feed-tier-contract.md`)
- [[infra-l402-otb-settlement]] (`Brain/wiki/cards/infra-l402-otb-settlement.md`)
- [[infra-satoshi-cost-rollup]] (`Brain/wiki/cards/infra-satoshi-cost-rollup.md`)
- [[local-market-agent]] (`Brain/wiki/cards/local-market-agent.md`)
- [[loop2-build-report]] (`Brain/wiki/cards/loop2-build-report.md`)
- [[loop3-decimal-standard]] (`Brain/wiki/cards/loop3-decimal-standard.md`)
- [[lp-device-intelligence-substrate]] (`Brain/wiki/cards/lp-device-intelligence-substrate.md`)
- [[merchant-org-hierarchy]] (`Brain/wiki/cards/merchant-org-hierarchy.md`)
- [[mission-main-street]] (`Brain/wiki/cards/mission-main-street.md`)
- [[ncr-ecosystem-2026]] (`Brain/wiki/cards/ncr-ecosystem-2026.md`)
- [[platform-alx-vsm]] (`Brain/wiki/cards/platform-alx-vsm.md`)
- [[platform-architectural-continuity]] (`Brain/wiki/cards/platform-architectural-continuity.md`)
- [[platform-case-type-registry-pattern]] (`Brain/wiki/cards/platform-case-type-registry-pattern.md`)
- [[platform-closed-loop-attribution]] (`Brain/wiki/cards/platform-closed-loop-attribution.md`)
- [[platform-cryptographic-erasure]] (`Brain/wiki/cards/platform-cryptographic-erasure.md`)
- [[platform-data-classification]] (`Brain/wiki/cards/platform-data-classification.md`)
- [[platform-enterprise-document-services]] (`Brain/wiki/cards/platform-enterprise-document-services.md`)
- [[platform-federal-compliance-spine]] (`Brain/wiki/cards/platform-federal-compliance-spine.md`)
- [[platform-field-capture]] (`Brain/wiki/cards/platform-field-capture.md`)
- [[platform-gateway-thesis]] (`Brain/wiki/cards/platform-gateway-thesis.md`)
- [[platform-general-store-test-lab]] (`Brain/wiki/cards/platform-general-store-test-lab.md`)
- [[platform-geographic-compliance-resolver]] (`Brain/wiki/cards/platform-geographic-compliance-resolver.md`)
- [[platform-inventory-2026-04]] (`Brain/wiki/cards/platform-inventory-2026-04.md`)
- [[platform-l402-ildwac-moat]] (`Brain/wiki/cards/platform-l402-ildwac-moat.md`)
- [[platform-multi-tier-assortment]] (`Brain/wiki/cards/platform-multi-tier-assortment.md`)
- [[platform-parcel-as-anchor]] (`Brain/wiki/cards/platform-parcel-as-anchor.md`)
- [[platform-performance-nfrs]] (`Brain/wiki/cards/platform-performance-nfrs.md`)
- [[platform-pii-hashing]] (`Brain/wiki/cards/platform-pii-hashing.md`)
- [[platform-proof-case]] (`Brain/wiki/cards/platform-proof-case.md`)
- [[platform-property-pack-methodology]] (`Brain/wiki/cards/platform-property-pack-methodology.md`)
- [[platform-pwc-benchmarks]] (`Brain/wiki/cards/platform-pwc-benchmarks.md`)
- [[platform-retailer-lifecycle-test]] (`Brain/wiki/cards/platform-retailer-lifecycle-test.md`)
- [[platform-stack-commitment]] (`Brain/wiki/cards/platform-stack-commitment.md`)
- [[platform-thesis]] (`Brain/wiki/cards/platform-thesis.md`)
- [[platform-wyoming-ecosystem]] (`Brain/wiki/cards/platform-wyoming-ecosystem.md`)
- [[portable-store-founder-intent]] (`Brain/wiki/cards/portable-store-founder-intent.md`)
- [[professor-adrian-beck-total-retail-loss]] (`Brain/wiki/cards/professor-adrian-beck-total-retail-loss.md`)
- [[raas-receipt-as-a-service]] (`Brain/wiki/cards/raas-receipt-as-a-service.md`)
- [[retail-ap-vendor-terms]] (`Brain/wiki/cards/retail-ap-vendor-terms.md`)
- [[retail-assortment-management]] (`Brain/wiki/cards/retail-assortment-management.md`)
- [[retail-backroom-cost-transfer]] (`Brain/wiki/cards/retail-backroom-cost-transfer.md`)
- [[retail-chargeback-matrix]] (`Brain/wiki/cards/retail-chargeback-matrix.md`)
- [[retail-demand-forecasting]] (`Brain/wiki/cards/retail-demand-forecasting.md`)
- [[retail-event-management]] (`Brain/wiki/cards/retail-event-management.md`)
- [[retail-import-management]] (`Brain/wiki/cards/retail-import-management.md`)
- [[retail-inventory-audit]] (`Brain/wiki/cards/retail-inventory-audit.md`)
- [[retail-inventory-valuation-mac]] (`Brain/wiki/cards/retail-inventory-valuation-mac.md`)
- [[retail-item-authorization]] (`Brain/wiki/cards/retail-item-authorization.md`)
- [[retail-merchandise-financial-planning]] (`Brain/wiki/cards/retail-merchandise-financial-planning.md`)
- [[retail-merchandise-hierarchy]] (`Brain/wiki/cards/retail-merchandise-hierarchy.md`)
- [[retail-operations-kpis]] (`Brain/wiki/cards/retail-operations-kpis.md`)
- [[retail-purchase-order-model]] (`Brain/wiki/cards/retail-purchase-order-model.md`)
- [[retail-receiving-disposition]] (`Brain/wiki/cards/retail-receiving-disposition.md`)
- [[retail-replenishment-model]] (`Brain/wiki/cards/retail-replenishment-model.md`)
- [[retail-sales-audit]] (`Brain/wiki/cards/retail-sales-audit.md`)
- [[retail-site-management]] (`Brain/wiki/cards/retail-site-management.md`)
- [[retail-space-range-management]] (`Brain/wiki/cards/retail-space-range-management.md`)
- [[retail-three-way-match]] (`Brain/wiki/cards/retail-three-way-match.md`)
- [[retail-vendor-compliance-standards]] (`Brain/wiki/cards/retail-vendor-compliance-standards.md`)
- [[retail-vendor-lifecycle]] (`Brain/wiki/cards/retail-vendor-lifecycle.md`)
- [[retail-vendor-scorecard]] (`Brain/wiki/cards/retail-vendor-scorecard.md`)
- [[role-binding-model]] (`Brain/wiki/cards/role-binding-model.md`)
- [[runbook-brain-wiki-commit]] (`Brain/wiki/cards/runbook-brain-wiki-commit.md`)
- [[runbook-cowork-memory-bus-setup]] (`Brain/wiki/cards/runbook-cowork-memory-bus-setup.md`)
- [[runbook-create-runbook]] (`Brain/wiki/cards/runbook-create-runbook.md`)
- [[runbook-docker-startup]] (`Brain/wiki/cards/runbook-docker-startup.md`)
- [[runbook-memory-bus-seed]] (`Brain/wiki/cards/runbook-memory-bus-seed.md`)
- [[runbook-vault-publish]] (`Brain/wiki/cards/runbook-vault-publish.md`)
- [[shelf-edge-demand-heartbeat]] (`Brain/wiki/cards/shelf-edge-demand-heartbeat.md`)
- [[signal-civil-services]] (`Brain/wiki/cards/signal-civil-services.md`)
- [[signal-community-intel]] (`Brain/wiki/cards/signal-community-intel.md`)
- [[signal-property-landlord]] (`Brain/wiki/cards/signal-property-landlord.md`)
- [[signal-seasonality]] (`Brain/wiki/cards/signal-seasonality.md`)
- [[signal-social-threat]] (`Brain/wiki/cards/signal-social-threat.md`)
- [[signal-weather-seo]] (`Brain/wiki/cards/signal-weather-seo.md`)
- [[store-network-integrity]] (`Brain/wiki/cards/store-network-integrity.md`)
- [[tier-bulk-window]] (`Brain/wiki/cards/tier-bulk-window.md`)
- [[tier-change-feed]] (`Brain/wiki/cards/tier-change-feed.md`)
- [[tier-daily-batch]] (`Brain/wiki/cards/tier-daily-batch.md`)
- [[tier-reference]] (`Brain/wiki/cards/tier-reference.md`)
- [[tier-stream]] (`Brain/wiki/cards/tier-stream.md`)
- [[var-acquisition-thesis]] (`Brain/wiki/cards/var-acquisition-thesis.md`)
- [[vertical-smb-health-hypothesis]] (`Brain/wiki/cards/vertical-smb-health-hypothesis.md`)
- [[workspace-admin-runbook]] (`Brain/wiki/cards/workspace-admin-runbook.md`)
- [[category-management-engagement-pattern]] (`Brain/wiki/category-management-engagement-pattern.md`)
- [[catz-rapidpos-alignment-notes]] (`Brain/wiki/catz-rapidpos-alignment-notes.md`)
- [[control-state-procurement-requirements]] (`Brain/wiki/control-state-procurement-requirements.md`)
- [[counterpoint-market-gtm-proposal]] (`Brain/wiki/counterpoint-market-gtm-proposal.md`)
- [[crb-fresh-product-support]] (`Brain/wiki/crb-fresh-product-support.md`)
- [[crb-rapidpos-alignment-notes]] (`Brain/wiki/crb-rapidpos-alignment-notes.md`)
- [[delivery-framework-cross-engagement]] (`Brain/wiki/delivery-framework-cross-engagement.md`)
- [[engagement-resource-model-fte-by-week]] (`Brain/wiki/engagement-resource-model-fte-by-week.md`)
- [[engagement-shape-100-day-deployment]] (`Brain/wiki/engagement-shape-100-day-deployment.md`)
- [[garden-center-operating-reality]] (`Brain/wiki/garden-center-operating-reality.md`)
- [[growdirect-the-article]] (`Brain/wiki/growdirect-the-article.md`)
- [[growdirect-the-ask]] (`Brain/wiki/growdirect-the-ask.md`)
- [[growdirect-the-chirp]] (`Brain/wiki/growdirect-the-chirp.md`)
- [[growdirect-the-crdm]] (`Brain/wiki/growdirect-the-crdm.md`)
- [[growdirect-the-demo]] (`Brain/wiki/growdirect-the-demo.md`)
- [[growdirect-the-fox]] (`Brain/wiki/growdirect-the-fox.md`)
- [[growdirect-the-gate]] (`Brain/wiki/growdirect-the-gate.md`)
- [[growdirect-the-glog]] (`Brain/wiki/growdirect-the-glog.md`)
- [[growdirect-the-goose]] (`Brain/wiki/growdirect-the-goose.md`)
- [[growdirect-the-l402]] (`Brain/wiki/growdirect-the-l402.md`)
- [[growdirect-the-market]] (`Brain/wiki/growdirect-the-market.md`)
- [[growdirect-the-mining-moat]] (`Brain/wiki/growdirect-the-mining-moat.md`)
- [[growdirect-the-network]] (`Brain/wiki/growdirect-the-network.md`)
- [[growdirect-the-notary]] (`Brain/wiki/growdirect-the-notary.md`)
- [[growdirect-the-owl]] (`Brain/wiki/growdirect-the-owl.md`)
- [[growdirect-the-patent]] (`Brain/wiki/growdirect-the-patent.md`)
- [[growdirect-the-pipe]] (`Brain/wiki/growdirect-the-pipe.md`)
- [[growdirect-the-pitch]] (`Brain/wiki/growdirect-the-pitch.md`)
- [[growdirect-the-pool]] (`Brain/wiki/growdirect-the-pool.md`)
- [[growdirect-the-rollout]] (`Brain/wiki/growdirect-the-rollout.md`)
- [[growdirect-the-scale]] (`Brain/wiki/growdirect-the-scale.md`)
- [[growdirect-the-team]] (`Brain/wiki/growdirect-the-team.md`)
- [[growdirect-the-vision]] (`Brain/wiki/growdirect-the-vision.md`)
- [[growdirect-viewpoint-virtual-store-manager]] (`Brain/wiki/growdirect-viewpoint-virtual-store-manager.md`)
- [[methodology-ibm-retail-diagnostic]] (`Brain/wiki/methodology-ibm-retail-diagnostic.md`)
- [[murdochs-ranch-home-supply-proof-case]] (`Brain/wiki/murdochs-ranch-home-supply-proof-case.md`)
- [[murdochs-workflow-cards-user-stories-scenarios]] (`Brain/wiki/murdochs-workflow-cards-user-stories-scenarios.md`)
- [[ncr-counterpoint-api-reference]] (`Brain/wiki/ncr-counterpoint-api-reference.md`)
- [[ncr-counterpoint-connection-runbook]] (`Brain/wiki/ncr-counterpoint-connection-runbook.md`)
- [[ncr-counterpoint-document-model]] (`Brain/wiki/ncr-counterpoint-document-model.md`)
- [[ncr-counterpoint-endpoint-spine-map]] (`Brain/wiki/ncr-counterpoint-endpoint-spine-map.md`)
- [[ncr-counterpoint-modernization-path]] (`Brain/wiki/ncr-counterpoint-modernization-path.md`)
- [[ncr-counterpoint-phase-0-context-brief]] (`Brain/wiki/ncr-counterpoint-phase-0-context-brief.md`)
- [[ncr-counterpoint-rapid-pos-relationship]] (`Brain/wiki/ncr-counterpoint-rapid-pos-relationship.md`)
- [[ncr-counterpoint-sandbox-setup-checklist]] (`Brain/wiki/ncr-counterpoint-sandbox-setup-checklist.md`)
- [[ncr-rapidpos-alignment-notes]] (`Brain/wiki/ncr-rapidpos-alignment-notes.md`)
- [[ncr-vault-gap-ledger]] (`Brain/wiki/ncr-vault-gap-ledger.md`)
- [[rapid-pos-counterpoint-market-research-tam]] (`Brain/wiki/rapid-pos-counterpoint-market-research-tam.md`)
- [[rapid-pos-counterpoint-user-pain-points]] (`Brain/wiki/rapid-pos-counterpoint-user-pain-points.md`)
- [[rapidpos-driftpos-platform-brief]] (`Brain/wiki/rapidpos-driftpos-platform-brief.md`)
- [[retail-architecture-patterns]] (`Brain/wiki/retail-architecture-patterns.md`)
- [[retail-data-model-patterns]] (`Brain/wiki/retail-data-model-patterns.md`)
- [[retail-foundation-data]] (`Brain/wiki/retail-foundation-data.md`)
- [[retail-implementation-methodology]] (`Brain/wiki/retail-implementation-methodology.md`)
- [[retail-integration-patterns]] (`Brain/wiki/retail-integration-patterns.md`)
- [[retail-integration-spine]] (`Brain/wiki/retail-integration-spine.md`)
- [[retail-merchandise-planning-otb]] (`Brain/wiki/retail-merchandise-planning-otb.md`)
- [[retail-module-decomposition]] (`Brain/wiki/retail-module-decomposition.md`)
- [[retail-po-from-plan]] (`Brain/wiki/retail-po-from-plan.md`)
- [[retail-promotion-workflow]] (`Brain/wiki/retail-promotion-workflow.md`)
- [[retail-restart-recovery-patterns]] (`Brain/wiki/retail-restart-recovery-patterns.md`)
- [[retail-security-controls]] (`Brain/wiki/retail-security-controls.md`)
- [[retail-sizing-methodology]] (`Brain/wiki/retail-sizing-methodology.md`)
- [[retail-transaction-volume-benchmarks]] (`Brain/wiki/retail-transaction-volume-benchmarks.md`)
- [[retail-vendor-evaluation-criteria]] (`Brain/wiki/retail-vendor-evaluation-criteria.md`)
- [[socal-home-garden-target-customers-brief]] (`Brain/wiki/socal-home-garden-target-customers-brief.md`)
- [[solex-square-integration-notes]] (`Brain/wiki/solex-square-integration-notes.md`)
- [[state-liquor-chain-proof-case]] (`Brain/wiki/state-liquor-chain-proof-case.md`)
- [[store-of-the-future-fresh-planning]] (`Brain/wiki/store-of-the-future-fresh-planning.md`)
- [[voyix-counterpoint-rapid-pos-engagement-context]] (`Brain/wiki/voyix-counterpoint-rapid-pos-engagement-context.md`)

### Commits of substance

- `29da90f` fix(auth): GRO-753 review fixes — uuid v5, updated_at, op order, LNURL_SCHEME, sync.Map comment
- `a25b5bd` fix(auth): GRO-753 spec fix — pollSession ErrNotFound returns 410 not 404
- `6ab615d` feat(auth): GRO-753 LNURL-auth — migration 023, internal/auth/lnurl/, secp256k1 verify, JWT session, gateway mount
- `dfd4e52` fix(protocol): GRO-752 review fixes — MaxBytesReader, error envelope, updated_at, nil-guards, logger
- `9bf666b` feat(protocol): GRO-752 L402 sat-gated Validation API — migration 022, internal/protocol/validate/, gateway mount
- `bd4a73b` outputs: wave session deliverable — retail vertical proposal
- `fdf9874` plan: Wave G — L402 validation, LNURL-auth, Cockroach proofs (GRO-752/753/754/745)
- `7f84d5b` fix(protocol): GRO-751 review fixes — migration, store interface, updated_at
- `2efa9e0` feat(protocol): GRO-751 .jeffe namespace registration — mint, inscribe, verify
- `9375410` fix(protocol): sub3 review fixes — tx isolation, byte-hash, failed-anchor audit (GRO-750)
- `af80acb` feat(protocol): Sub 3 Merkle & Ordinal anchor worker (GRO-750)
- `344217f` loop4-wave-e: GRO-767 Wave E complete — MCP route group, 28 tools, report migration 019
- `fe1d380` feat(gateway): mount MCP route group — 26 tools, 7 modules (GRO-767)
- `5b656fa` feat(report): Storer interface + PgxStore + migration 019 (GRO-767)
- `f73d7ca` feat(mcp): returns + report tools (GRO-767)
- `0b1b404` feat(mcp): customer + employee tools (GRO-767)
- `a60fe52` feat(mcp): asset tools — list/get_item/shrink_movements/flag (GRO-767)
- `a219586` feat(mcp): analytics tools — sales/basket/cohort/velocity/shrink (GRO-767)
- `993b455` feat(mcp): alert tools — list/get/stats/acknowledge/resolve/suppress (GRO-767)
- `5b096f2` feat(mcp): registry + JSON-RPC 2.0 handler skeleton (GRO-767)
- `78324f5` loop4-wave-d: Phase F port assignments for Wave D services
- `2fe6b3f` loop4-wave-d: Phase E returns + report modules
- `84f23d0` loop4-wave-d: Phase D customer + employee modules
- `98915b0` loop4-wave-d: Phase C asset module (inventory positions + flag write)
- `ea366af` loop4-wave-d: Phase B analytics module (sales/basket/cohort/velocity/shrink)
- `b41029b` loop4-wave-d: Phase A alert module (lifecycle + threshold engine)
- `f85c788` loop4-wave-c: Phase D carry-forwards (credential store + sqlc retrofit)
- `b9e28ab` loop4-wave-c: Phase C.3 Owl dashboard surface + obs wiring
- `f000d15` loop4-wave-c: case management + Hawk read-side wiring (Phase B)
- `379e3f1` loop4-wave-c: Bull billing — L402 + OTB + cost rollup (Phase A)
- `3dc50fe` loop4-wave-b: chirp rules + party-based subject resolution (Phase C.1+C.2)
- `82a31d8` loop4-wave-b: transaction module + three-way-match workflow (Phase B.1+B.4)
- `2c0aa53` loop4-wave-b: gateway admin endpoints — DLQ list + replay (Phase A.3)
- `27f708c` loop4-wave-b: internal/tsp sequence tracking + gap detection (Phase A.2)
- `2ac295e` loop4-wave-b: webhook substrate — DLQ + idempotency + backpressure (Phase A.1)
- `e1e21ce` loop4-wave-a: identity, auth, tenant model rebuild (Phase C)
- `912d3c8` loop4-wave-a: party substrate schema (Phase B.5)
- `d238eb3` loop4-wave-a: workflow substrate (schema + Go package, Phase B.4)
- `d762a52` loop4-wave-a: app.merchant_settings.de_merge_audit_visibility (Phase B.3)
- `fecf8ce` loop4-wave-a: f.markup_envelope_tiers config table + seed (Phase B.2)
- `b4b96d2` loop4-wave-a: GSLM 9-domain coverage runner + 2026-05-03 report (Phase B.1)
- `b78eb7a` loop4-wave-a: canary-go CI workflow (Phase A.3)
- `aa19831` loop4-wave-a: internal/obs observability scaffold (Phase A.2)
- `b6fc5a6` loop4-wave-a: codify monorepo conventions + amend sqlc rule (Phase A.1)
- `503f6cd` GRO-762 Phase D: Loop 3 backlog — 15 items prioritized
- `f8a295a` GRO-762 Phase C: Bart conversation prep — 12 DriftPOS OQs structured for 90-min Zoom
- `1975923` loop3-wave1: shopspring/decimal substrate + retrofit roadmap (B.4)
- `66f556e` loop3-wave1: fox.SubjectResolver + lazy-mode subjectFromDetection (B.3)
- `57cd2ce` loop3-wave1: f.tender_types source-default seed + Sub2 wiring (B.2)
- `67f98b6` loop3-wave1: l.locations.timezone wired into Chirp after-hours rule (B.1)
- `8ce8386` GRO-762 Phase A: OQ Resolution Pack — 22 founder-approved decisions
- `26386f6` gitignore: block .nsf files (folded GRO-736 NSF history strip)
- `2fb17fe` deposit: regulation-spec template + 4 filled regulations + 3 federal case-types
- `21e3472` GRO-733: cloud architecture + workload SDD + portability code-review
- `99247d7` GRO-760: RapidPOS sub-brand feature map — gun, garden, liquor, feed & tack (CAN-RES-002)
- `5aab99d` GRO-726: Counterpoint VAR landscape — Card 3 market intelligence
- `e442cf0` GRO-759: DriftPOS ↔ Canary integration contract spec (CAN-DESIGN-001)
- `6d7f7fb` GRO-734: Party identity + fingerprinting + householding SDD
- `53ae761` deposit: parcel-as-anchor + geo-compliance + property-pack methodology + federal-compliance spine
- `8e69a15` GRO-684: M1/M2/M3 coverage assessment post-Loop-2
- `f3854ff` loop2-wave4: closure report — 7 modules shipped, ~47 SDD findings, Loop 3 regen targets prioritized
- `586c912` loop2-wave3i: integration-test seed fixes + fox FK bug fix
- `248f757` loop2-wave3: gate cmd/identity tests under integration tag (Tier-3 known-broken pre-Loop 2)
- `69b39a6` loop2-owl: read-only merchant intelligence aggregator (GRO-761 Wave 2)
- `8808613` deposit: canary-hawk universal envelope + case-type registry pattern
- `b927c43` loop2-sub2: dispatcher + Square + Counterpoint + Clover adapter substrate
- `d2e76c7` loop2-pricing: price-resolve service end-to-end (Wave 2)
- `ba7918e` loop2-chirp: 7 baseline rules + evaluator engine (Wave 2)
- `9cc5d4c` loop2-inventory: position read + movement append over canonical i.* tables
- `a7af9e2` loop2-fox: case-management module wired to q.cases / q.case_evidence / q.case_actions
- `f87bcd1` loop2-item: master-data CRUD + barcode resolve keystone
- `ebb3d27` loop2-wave1: hand-written Go types for 14 canonical schemas (88 tables)
- `2b9c00b` session-cleanup: pending Brain wiki + plan files before Loop 2 dispatch
- `5690a7d` loop1: declarative schema replaces migration discipline (88 tables, 14 schemas)
- `6697bbf` brain: capture canary-protocol-gateway-live-on-gcp runbook card after Wave 4 deploy
- `a5e8171` analysis: joint product positioning — PwC three-phase on GRO-721 findings
- `4564a73` GRO-756: deploy-gateway.sh fixes (5 issues from Wave 4 deploy) + Dockerfile go 1.24->1.25
- `3fa74c9` strategy: lock OQ-6 — Apache License, Version 2.0 for open-protocol leave-behind
- `8c17666` strategy: substrate captures v2 + identity layer + SMB Health hypothesis
- `4df49bf` strategy: lock gateway thesis + accelerator pack manifest
- `b74f71f` GRO-756: Phase 1.J GCP deployment design + scripts + runbook
- `8491350` GRO-687: SDD — Secrets Manager integration for canary-gateway
- `ecbc7ad` GRO-687: SmResolver — GCP Secret Manager-backed Resolver
- `ff5da9d` GRO-687: migration 018 — add secret_sm_ref column to protocol.source_secrets
- `3946909` GRO-748: bilateral verification API — GET /v1/protocol/evidence/{event_hash}
- `c368dc3` GRO-748: Sub 1 (Hash & Seal) — chain library + worker + tests
- `cba31a6` GRO-748: migration 017 — protocol.evidence (write-once L1 Index)
- `dba425d` legal: GRO-693 — v0.1 DPA + subprocessor list + breach runbook + IR plan
- `44c7144` GRO-694: wire audit middleware into gateway protocol routes
- `7324414` GRO-694: protocol audit middleware (chi-compatible)
- `8aeb133` GRO-694: extend app.audit_log with protocol-specific columns
- `a6d83a3` plans: next-session kickoff for the GCP-API-Blinking MVP
- `f71e123` GRO-746: integration smoke test + latency baseline against real Postgres + Valkey
- `3336876` GRO-746: API Gateway (Node 2) — HMAC verify + payload hash + queue publish
- `d711142` phase-1-plan: capture Canary Protocol Phase 1 execution plan + kickoff deck draft
- `22faff3` brain: platform-thesis card-version 3 — fourth accountability rail
- `1228305` canonical-data-model: Chunk 10 — final SDDs rendered
- `cb8c832` canonical-data-model: Chunk 9b — MCP Service Junction Inventory (166 junctions)
- `bef4c78` canonical-data-model: Chunk 9 — Module ownership matrix (65 entities)
- `fae3276` canonical-data-model: Chunk 8 — Canary platform mechanics (15 entities)
- `8b1c829` canonical-data-model: Chunk 7 — POSLog + Sales Audit (t schema, 9 entities)
- `20b30f4` canonical-data-model: Chunk 6 — Pricing + Financial (p+f schemas, 10 entities)
- `88e05d6` canonical-data-model: Chunk 5b — Orders (o schema, 8 entities, greenfield closure)
- `bdd5772` canonical-data-model: Chunk 5 — Inventory + Distribution (i schema, 5 entities)
- `765fce2` canonical-data-model: Chunk 4 — Party (Customer + Employee, c+e schemas, 6 entities)
- `0cdeaa8` canonical-data-model: Chunk 3 — Location + Space (l, s schemas, 6 entities)
- `a4601c5` canonical-data-model: Chunk 2 — Item domain (m schema, 6 entities)
- `158fcdd` canonical-data-model: Chunk 1.6 — design principles + ARTS anchor
- `44aa2b7` canonical-data-model: ARTS pivot — S10 added, Chunk 1.6 next
- `a859037` canonical-data-model: Chunk 1.5 — 79 operational fingerprints captured
- `e17aa80` canonical-data-model: Chunk 1 — add S9 (TOM Interface Design Docs)
- `1da62eb` canonical-data-model: Chunk 1 revised — discovered GSLM MDM site
- `555d243` canonical-data-model: Chunk 1 — source inventory + alias map
- `cbcce46` brain: Bart-call deployment questions for RAAS / Counterpoint / RapidPOS
- `24e9a57` fix: Q-rule count reconciliation — 23→24 rules, 10→11 categories (GRO-603)
- `c12d903` research: Gap Backbone architecture + RaaS product + VAR acquisition thesis cards
- `295714a` research: NCR ecosystem + Counterpoint product state 2026 intelligence cards
- `c8ec85d` brain: ALXjr sunset (decision approved) + mini housekeeping followup note
- `de57088` sdd: reconcile cross-SDD classification drift (GRO-720)
- `0f081ed` test: trigger redeploy
- `e070d83` research: RapidPOS feature map — DriftPOS/Canary boundary (CAN-RES-001)
- `1a033b1` docs: DEPLOY.md update — Cloud SQL + dbcheck details
- `97a05a6` ci: add cmd/dbcheck Cloud SQL connectivity smoke-test service
- `3a2fdef` docs: DEPLOY.md — drop-zone CI/CD workflow for collaborators
- `9a79b09` ci: rename /healthz to /health + deploy authenticated-only
- `bb5ec54` ci: add --quiet to gcloud run deploy in cloudbuild.yaml
- `2797b5e` ci: cloudbuild.yaml + cmd/hello smoke-test service for the drop-zone pipeline
- `5f8e0cc` chore: archive Condor redirect stub from team folder
- `e62241b` sweep: agent card cleanup — ALX VSM rewrite + Canary/Cove Builder cards + ALXjr decision
- `1748022` sweep: GRO-700 Phase 0.5 — strategic surface alignment with GCP shift
- `8f0f38e` brain: GRO-700 Phase 0 audit memos (laptop + mini)
- `1923677` brain: GCP foundation runbook — org, project canary-rapidpos, APIs, SA baseline (2026-05-01)
- `8a926b9` brain: add workspace-admin-runbook card (GRO-719)
- `a1035b4` refactor: module letter rename — Brain + SDDs (C→M, J→O, R→C, W→E)
- `71bb9be` spec: module letter rename canonical mapping (C→M, J→O, R→C, W→E)
- `4cf7b2c` content: reframe EJ Spine and Sales Audit article as Canary IP
- `ffda6a0` content: scrub residual sales-claim phrasing from internal wiki
- `7f0ccef` wiki: broken-links categorization baseline + canonical-positioning stub + path fix
- `7111db1` wiki+sdd: vendor crosswalks (Square / RapidPOS / NCR) + multi-VAR rev-share refinement
- `884eb0d` sdd+wiki+cards: satoshi cost rollup — full pricing model + buildable spec
- `0b610a9` cards: 23 domain-module cards for newly-documented services
- `cfd6ae6` sdd+cards: feed-tier-contract buildable spec + 10 cadence-ladder cards
- `809f690` sdd: 23 service endpoint contracts — tier-shaped, external-quality
- `7dcb65d` wiki: cadence ladder + tier dimension across endpoint strategy
- `5406542` wiki: GK-POS gap analysis + Canary Go endpoint library
- `ceed24b` wiki: long-arc atlas — 12 mermaids spanning strategic spine, compliance, architecture
- `c2b3948` brain: adopt kepano obsidian-skills method — Bases + 6 DevOps entity templates
- `275b19d` ncr-publish: stage 6 foundational specs alongside modernization article
- `ceb7398` wiki: scrub NCR modernization article — kill bravado, jargon, AI tells
- `32c52c7` memory-bus: §11 engine applicability — migration 006 + curation allowlist
- `910da7f` wiki: DriftPOS platform brief + NCR modernization path
- `1109292` Clarify Kroger engagement scope: near-real-time, all divisions, LP-scoped
- `0f53113` Beck card: add Fakety → McCarrek → Kroger practitioner chain
- `4feac8a` Extend Beck card: SEG/BI-LO implementation + agent training significance
- `a1ead29` Add Professor Adrian Beck reference card and recruiter brief v0.1
- `b41ba0e` church: store of the future — grocery and fresh planning implications deep dive
- `4893230` brain: platform-state inventory and Wave 1 gap analysis (GRO-703)
- `1e6b4c1` church: bitcoin standard — cost center cross-charge and meter model cards
- `ca9fef4` brain: PA LCB intake + control-state synthesis
- `83080d2` brain: Murdoch's recon — 4,021 PDPs, 47 stores, full site map
- `7d4e974` sdds: Wave 4 polish — retail-lifecycle-test-data scaffold
- `db0d720` sdds: Wave 3 Batch 4 polish — cross-cutting + ops
- `c8aa10b` sdds: Wave 3 Batch 3 polish — POS adapters + ecom
- `f38de99` sdds: Wave 3 Batch 2 polish — commercial / operational cluster
- `48a8db6` sdds: Wave 3 Batch 1 polish — detection / LP cluster
- `a55056b` sdds: Wave 2 polish session log
- `a315f34` sdds: Wave 2 Batch 3 polish — Optional Features (ildwac, blockchain-anchor)
- `c8c413c` sdds: Wave 2 Batch 2 polish — receipt chain (raas, factory, agent-contracts)
- `904f735` sdds: Wave 1 + Wave 2 Batch 1 polish — substrate + architecture spine
- `68ed2d1` brain: GCP commitment thread — 3 platform cards capturing stack, continuity, moat
- `fc7c6ca` brain: 4 platform cards — PII hashing, multi-tier assortment, crypto erasure, data classification
- `4d3cd31` sdds: fix low-entropy PII hash; add data classification inventory
- `c810527` sdds: reconcile go-handoff ports; reframe Solex; add multi-tier assortment
- `bd864d0` sdds: rename hawk.md → hawk-case-management.md
- `55af26a` sdds: complete go-handoff SDD library — 25 new files
- `883d43f` license: Apache 2.0 for CanaryGo; SPDX headers on all go-handoff SDDs; add sdd-writer skill
- `3442596` sdds: add ops-dashboard, store-brain
- `5c68938` sdds: add ildwac, device-contracts; update inventory-as-a-service
- `432fc99` sdds: add inventory-as-a-service
- `e1ffb82` sdds: add raas, settings, ecom-channel, factory-pipeline, retail-lifecycle-test-data
- `f947315` brain: add NFRs, PwC benchmarks, store network integrity, vault publish runbook; update card directory
- `5a5f1ff` brain: add performance NFRs, PwC benchmarks, store network integrity; update card directory
- `b670927` church: EDS architecture, RaaS rewrite, field capture, Wyoming ecosystem, Murdoch's ICP, platform proof case, infrastructure displacement
- `826ebe8` feat: gap-fill sprint — 5 new retail domain cards + index update
- `160b1fc` feat: modernization pass — Platform (2030) sections on all 17 retail domain cards
- `eb4d638` knowledge: add 17 retail domain cards from Retek corpus, scrubbed
- `83c42d2` feat(brain): add meta-runbook — when and how to create a runbook card
- `b0a14df` feat(brain): add runbook card-type + three starter runbooks
- `a958d43` fix(memory-bus): seed_standalone writes to alx_memories, not seed_embeddings
- `d6ac108` feat(memory-bus): seed lock + cards/ + specs/ scope; add franchise-play, market-positioning, ilwac, portable-store cards
- `cc895f1` feat(memory-bus): add docs/sdds/go-handoff to seed scope — layer canary-go
- `600fe7a` feat(sdds): Canary Go SDD corpus v1.1 — ILDWAC, RaaS, agent contracts, attack plan (GRO-668)
- `1fb05b0` feat(canarygo): M1 Foundation complete — all gate checks passed
- `fa89f2b` fix(canarygo): Makefile test target — add Valkey password and extend SESSION_SECRET to 32+ bytes
- `101c428` feat(canarygo): all 19 service stubs compiling — M1 service skeleton complete
- `e45246e` fix(canarygo): use r.Context() for Valkey revocation check — honor request cancellation
- `99f8790` chore(canarygo): identity service verified running in Docker — curl :8086/health → ok
- `8ce101a` fix(canarygo): Dockerfile Go 1.24, Valkey auth URL, remove broken migrate image dep
- `b711a1b` feat(canarygo): identity service — /health + /sessions/validate, all stubs wired
- `91622be` chore(canarygo): pin pgvector-go v0.2.1 — required for sqlc vector type override
- `211d575` feat(canarygo): auth package — JWT sign/verify, bearer middleware
- `4d547f5` feat(canarygo): internal packages — crdm, arts, tenant, pagination, testutil
- `5e69e11` feat(canarygo): db package with pgxpool Connect helper
- `17accb5` feat(canarygo): config package with fail-fast env loader
- `4c36d9a` feat(canarygo): sqlc v2 config + seed queries for identity and tsp
- `375d708` feat(canarygo): 14 DDL migrations — CRDM, identity, multi-POS substrate, fox evidence chain
- `33351eb` fix(claude): Mini Docker Gate startup — CanaryGo compose is deploy/ not devops/
- `f41403a` feat(canarygo): Dockerfile.identity + docker-compose.yml with shared growdirect network
- `7391ab2` feat(canarygo): Makefile with migrate, sqlc-gen, test, build targets
- `0b67e7a` feat(canarygo): agent context CLAUDE.md
- `2cd5abf` feat(canarygo): directory scaffold per go-module-layout SDD
- `c957247` chore(canarygo): pin go directive to 1.22 minimum — avoids toolchain floor constraint
- `e8ea371` chore(canarygo): remove root main.go stub — deps anchored by cmd/ packages
- `4a8fbfb` feat(canarygo): initialize Go module github.com/growdirect-llc/rapidpos
- `da2758c` feat(brain): ALX as VSM card — store systems architect, S1-S5 spine mapping, brain-as-runtime framing
- `7ef3a8f` fix(repo): GRO-555 — remove broken ownpalosverdes symlink; add closed-loop cost attribution wiki card
- `e74680f` fix(devops): GRO-555 — fix Ollama healthcheck (ollama list, not curl)
- `0843382` docs(brain): GRO-601 — rename Q-RESTRICTED-ITEM-SALE to Q-CP-01
- `b1b33c1` docs(sdd): GRO-587 — remove pre-revision §6.12/§6.13 duplicates, fix Phase 3 removes Module W
- `17df34e` feat(canarygo): M1 Foundation implementation plan
- `43a2e4e` feat(specs): Canary Go M1 Foundation design — skeleton-first approach
- `1573e11` docs(brain): canary-go-portal — add agent card network section
- `902a7a7` chore(claude): full audit pass — Canary frozen, Go active, SDD paths, memory examples
- `97e6a33` docs(brain): repair agent card index — add 3 missing cards, platform-thesis type
- `2c9cad7` feat(brain): GRO-604 MOC trickle-down — platform thesis + Canary Go + edge arch
- `1076888` feat(brain): GRO-616 NCR Counterpoint + Rapid POS wiki expansion
- `cea1f42` chore(claude): session types + platform mission + Canary Go clean break
- `1c2b332` feat(brain): retailer lifecycle test methodology card
- `1ae0c50` feat(brain): platform thesis — SMB ICP positioning + four beats
- `db43019` feat(brain): platform thesis card + L402 OTB settlement stub
- `dfe4ead` feat(brain): blockchain evidence anchor card + format spec update
- `915e7df` feat(brain): agent card format + 11 local market intelligence cards
- `bca40b4` feat(agent-pmo): extend architecture design — org hierarchy, local market intelligence layer
- `0ca69f6` feat(canary-go): agent PMO architecture design + Brain wiki portal
- `d6d709f` docs(canary): canary.growdirect.io content brief + site update instructions
- `e4c70de` sdd(go-handoff): go-module-layout + platform reframe — full spine, ARTS-native, GCP, whitelabel
- `ad292b1` feat(go-handoff): Canary Go build specification — 16 SDDs + microservice architecture
- `602eb7a` plan(sales): GRO-626 + GRO-627 implementation plan — ARTS alignment + TransactionFact
- `e9c5b46` fix(seed): align memory_type values with alx_memories CHECK constraint
- `e8cd885` sdd(analytics): Phase 3 Bull distribution metrics stub
- `2695ea9` sdd(platform-overview): POS-agnostic product definition, Hawk+Bull in module map
- `f0e1109` sdd(architecture): multi-POS purpose, Hawk+Bull in domain table
- `f0bef70` sdd(alx): hawk card context + multi-POS cutover-aware VSM routing
- `13ab8a4` sdd(data-model): add hawk schema (8 tables) and bull schema stub (4 planned)
- `ed8a3ca` sdd(raas): multi-source namespace model — Counterpoint alongside Square
- `6687968` sdd(owl): Phase 4 stub — Hawk card corpus as recall surface
- `24267ca` sdd(chirp): multi-POS rule substrate — Counterpoint audit surface addendum
- `24037e3` sdd(tsp): multi-POS ingress model — Counterpoint poll alongside Square webhook
- `e110a0a` sdd(bull): new — Phase 3 stub for distribution intelligence (Module D native)
- `837f152` sdd(hawk): new — ops contract for case management card factory
- `bf9b74b` sdd(fox): hawk positioning addendum — fox is EBR class inside hawk
- `6a2618e` brain(ncr): NCR vault alignment notes — VAR positioning vs RapidPOS delivery partner split
- `bdc6107` brain(crb): module alignment notes — fox/hawk drift, module D gating
- `15c9291` brain(catz): RapidPOS alignment notes — read pass observations
- `7a91632` docs: hawk phase-1 plan, canary site vaults spec, rapidpos site brief, devops backup script
- `f15081c` fix: engine.py Python 3.9 compat (Path|None -> Optional[Path]), CATz CLAUDE.md markdown
- `11d0784` brain: health scan 2026-04-27 — frontmatter pass (67 articles), CATz wiki init (58 articles)
- `dcf4df5` brain(ncr): wire NCR vault — gap analysis, 3 back-fills, CLAUDE.md, seed incremental mode
- `6625f21` spec(hawk+bull): second-pass reviewer fixes — vendor FK removal, entity_id format, Phase 2 DDL step
- `1991d12` spec(hawk+bull): fix 7 reviewer issues — schema FKs, circular dep, action counts, evidence chain
- `8520427` spec(hawk+bull): Hawk case management factory + Bull DSD vendor analytics design
- `e5658c0` spec(ncr): tighten NCR vault wiring spec after two review passes
- `c7366e4` spec(ncr): NCR vault framework wiring design
- `9709559` skill(canary): alx-startup — mini UAT site startup checklist
- `2870efc` moc(canary): add NCR Counterpoint SDD section + solution guide entry point
- `f55a27b` sdd(canary): Counterpoint solution guide — Frame/People/Agents/Model/Blueprint

## Cross-week thread
<!-- What from last week's "Do Next" landed? What slipped? -->

_First instance — no prior week to thread against. Threading begins W19._
