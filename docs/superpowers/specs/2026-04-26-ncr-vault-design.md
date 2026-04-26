---
title: NCR Vault — ncr.growdirect.io
date: 2026-04-26
status: approved
type: spec
gro: TBD
author: GrowDirect LLC
---

# NCR Vault Design Spec

## What it is

A Cloudflare-fronted partner vault at `ncr.growdirect.io` serving co-sell enablement content for NCR Counterpoint VARs — starting with Rapid Garden POS (Bart McCleskey) and expanding to the full Counterpoint VAR channel. GrowDirect is the factory; this vault is the downstream curated surface.

## Why it exists

CATz = the GrowDirect method. CRB = the Canary product, vendor-neutral. NCR vault = Canary *on Counterpoint*, VAR-specific. The three vaults have distinct audiences and distinct access postures; NCR vault fills the gap where a VAR needs the co-sell story grounded in the actual platform their customers run.

## Architecture

Follows the established three-vault pattern:

| Property | Value |
|---|---|
| Repo | `growdirect-llc/ncr` (public, `growdirect-llc` org) |
| Domain | `ncr.growdirect.io` (Cloudflare-fronted) |
| Build | Quartz v4, mirroring CATz/CRB stack |
| Access | Cloudflare Access-gated — VAR whitelist |
| Clone rule | No persistent local clone; transient `gh repo clone` cycles only |
| Content source | `GrowDirect/Brain/` — curated outward, never authored directly in the vault |

## Site sections

### Partner lane (commercial)

| Path | Purpose |
|---|---|
| `verticals/lawn-garden` | L&G operating reality, pain points, Canary module fit — ships full at launch |
| `verticals/feed-tack` | Feed & tack vertical — stub at launch |
| `verticals/gun` | Gun store vertical — stub at launch |
| `verticals/beverage` | Beverage vertical — stub at launch |
| `verticals/wine-spirits` | Wine & spirits vertical — stub at launch |
| `why-canary/` | "Enterprise layer on top of Counterpoint" positioning, TAM, pain theme catalog |
| `pitch/` | Leave-behinds and one-pagers; grows with the channel |

### Technical lane

| Path | Purpose |
|---|---|
| `integration/` | Counterpoint API surface: endpoint spine map, document model, API reference digest |
| `modules/` | L1–L4 process decomposition of the Canary Retail Spine on the RapidPOS L&G backbone |
| `sandbox/` | Connection runbook, sandbox setup checklist, path to demo |

## L1–L4 process decomposition (modules/)

The `modules/` section organizes the 13-module ARTS spine as a four-level process hierarchy, grounded in the RapidPOS L&G operating context.

| Level | What it is | Example |
|---|---|---|
| L1 | Business domain (RBIS-derived) | Store Operations Management |
| L2 | Canary module | Q — Loss Prevention |
| L3 | Process group | Transaction Monitoring |
| L4 | Activity → Counterpoint endpoint → L&G adaptation | Discount abuse detection → `SY_DOC / SY_DOC_LIN` → mix-and-match pricing allow-list |

At launch: `modules/index.md` carries the full L1–L4 framework table. Each of the 13 modules gets a stub article with correct L2/L3 headers. Q (Loss Prevention) and J (Forecast & Order) ship with L4 content, as they are highest-leverage for L&G.

## Content sourcing map

| Vault section | Brain sources |
|---|---|
| `verticals/lawn-garden` | `garden-center-operating-reality`, `rapid-pos-counterpoint-user-pain-points`, `socal-home-garden-target-customers-brief` |
| `why-canary/` | `voyix-counterpoint-rapid-pos-engagement-context`, `rapid-pos-counterpoint-market-research-tam`, `canary-raas-positioning` |
| `integration/` | `ncr-counterpoint-api-reference`, `ncr-counterpoint-document-model`, `ncr-counterpoint-endpoint-spine-map` |
| `modules/` | All 13 `canary-module-*-functional-decomposition.md` cards + `canary-module-q-counterpoint-rule-catalog` |
| `sandbox/` | `ncr-counterpoint-connection-runbook`, `ncr-counterpoint-sandbox-setup-checklist` |
| `pitch/` | Output from `claude-design-briefs-bart-monday.md` assets (once produced) |

## Cloudflare setup

Same pattern as CATz and CRB:
- GitHub Pages on `main` branch
- Cloudflare proxied A/CNAME record for `ncr.growdirect.io`
- Cloudflare Access policy — VAR whitelist (bart@rapidpos.com + gclyle@growdirect.io + tim.mooney@maonach.com to start)

## Brain MOC

`GrowDirect/Brain/projects/NCR.md` — external-pointing MOC following the CATz/CRB convention.

## What this spec does NOT cover

- Content population beyond L&G vertical and Q/J modules at launch
- Cloudflare Access wiring (follow-up task once Pages is live)
- Feed & tack / gun / beverage / wine & spirits vertical content
- Pitch asset production (depends on Monday Bart call output)
