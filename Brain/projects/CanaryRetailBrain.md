---
type: project-moc
status: active
external-repo: https://github.com/growdirect-llc/canary-retail-brain
external-site: https://growdirect-llc.github.io/canary-retail-brain/
audience: investors / partners / clients
local-clone: none (clone-on-demand only — see CLAUDE.md "External Vaults — Clone on Demand")
tags: [canary, retail-brain, product-knowledge, public-vault, arts]
---

# Canary Retail Brain — Product Knowledge Vault

Public-facing knowledge site for the Canary retail OS product. Serves prospects, partners, and investors as the canonical reference for what Canary is, how the 13-module ARTS-native spine works, and what the platform delivers to SMB multi-store operators on NCR Counterpoint. Content originates in `GrowDirect/Brain/` and is curated outward.

Served at: https://growdirect-llc.github.io/canary-retail-brain/
Source repo: https://github.com/growdirect-llc/canary-retail-brain

## What it covers

ARTS-native 13-module spine (A, C, D, F, J, L, N, P, Q, R, S, T, W), platform architecture, case studies, and integration documentation. 49 articles. Each module article has a paired `.manifest.yaml` with the detailed functional design.

## Access

Cloudflare Access-gated (Option C). Whitelist: gclyle@growdirect.io, bart@rapidpos.com, tim.mooney@maonach.com. Custom domain wiring (prerequisite for Access enforcement) is a pending task.

## Site sections

- [Modules](https://growdirect-llc.github.io/canary-retail-brain/modules/) — 13-module spine, each with manifest
- [Platform](https://growdirect-llc.github.io/canary-retail-brain/platform/) — architecture, method, schema
- [Case Studies](https://growdirect-llc.github.io/canary-retail-brain/case-studies/) — deployment outcomes
- [Integrations](https://growdirect-llc.github.io/canary-retail-brain/integrations/) — POS connectors, API surface

## Build stack

Quartz v4 + Canary design system (beak-gold accent `#BF8700`). Deployed via GitHub Actions on push to `main`. 18 active branches from prior mini dispatches remain unmerged — do not merge without founder coordination.

## Architecture rationale

See `Brain/dispatches/2026-04-26-three-vault-jekyll-pages-architecture.md` and GRO-606.

## Related

- [[Brain/projects/CATz]] — sister public vault (method + delivery framework)
- [[Brain/projects/GrowDirect]] — internal factory; source of truth for content flowing here
- [[Brain/projects/Canary]] — Canary app project MOC (code and SDDs)
- [[Brain/wiki/canary-platform-overview]] — platform overview wiki article
