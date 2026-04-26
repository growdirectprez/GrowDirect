---
type: project-moc
status: active
external-repo: https://github.com/growdirect-llc/catz
external-site: https://growdirect-llc.github.io/catz/
audience: investors / partners / clients
local-clone: none (clone-on-demand only — see CLAUDE.md "External Vaults — Clone on Demand")
tags: [catz, method, delivery-framework, public-vault]
---

# CATz — GrowDirect Method Vault

Public-facing knowledge site for the GrowDirect delivery framework. Serves investors, partners, and clients as the canonical reference for how GrowDirect engages, what it delivers, and how the CATz two-phase model works. Content originates in `GrowDirect/Brain/` and is curated outward — not authored directly in this repo.

Served at: https://growdirect-llc.github.io/catz/
Source repo: https://github.com/growdirect-llc/catz

## What it covers

Two-phase SMB retail engagement model, capability framework, roles, playbooks, agent contracts, proof cases, and the welcome journey for new partner/client onboarding. 43 articles across 10 topic folders.

## Access

Cloudflare Access-gated (Option C). Whitelist: gclyle@growdirect.io, bart@rapidpos.com, tim.mooney@maonach.com. Custom domain wiring (prerequisite for Access enforcement) is a pending task.

## Site sections

- [Method](https://growdirect-llc.github.io/catz/method/) — phases, roles, artifacts
- [CBM v2](https://growdirect-llc.github.io/catz/cbm-v2/) — capability building model
- [Proof Cases](https://growdirect-llc.github.io/catz/proof-cases/) — engagement outcomes
- [Welcome Journey](https://growdirect-llc.github.io/catz/welcome-journey/) — new partner onboarding
- [About](https://growdirect-llc.github.io/catz/about/) — GrowDirect LLC identity

## Build stack

Quartz v4 + Canary design system (owl-purple accent `#6639BA`). Deployed via GitHub Actions on push to `main`. Wikilinks render natively — no conversion needed.

## Architecture rationale

See `Brain/dispatches/2026-04-26-three-vault-jekyll-pages-architecture.md` and GRO-606.

## Related

- [[Brain/projects/CanaryRetailBrain]] — sister public vault (product knowledge)
- [[Brain/projects/GrowDirect]] — internal factory; source of truth for content flowing here
- [[Brain/wiki/catz-method]] — method overview wiki article
