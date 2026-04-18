# growdirect.io — Operations Hub Architecture

**Version:** 1.0  
**Date:** April 15, 2026  
**Status:** Blueprint  

---

## Purpose

growdirect.io is the operations hub for GrowDirect. Not a marketing site. Not a landing page. The spine that every product, every document, every investor asset, and every operational tool hangs off of. Built locally, published out through subdomains managed via DNS.

---

## Subdomain Architecture

```
growdirect.io/                         ← Hub index — the front door
│
├── canary.growdirect.io/              ← Canary LP — product + app
│   ├── /                              Landing (merchant-facing)
│   ├── /app                           Flask app (port 5001)
│   ├── /docs                          Technical docs (CRDM, forensics)
│   └── /atlas                         Mermaid diagram browser (52 figures)
│
├── cove.growdirect.io/                ← Cove — HOA governance + Angel
│   ├── /                              Landing
│   └── /app                           Flask app (port 5002)
│
├── investors.growdirect.io/           ← War Chest — gated investor hub
│   ├── /                              Gate (password) + table of contents
│   ├── /manifesto                     The Complete Thesis (v1.2)
│   ├── /eljeffe                       The Closed Loop (orbital diagram)
│   ├── /warchest/01-the-pitch         11 chapters from War Chest v0.5
│   ├── /warchest/02-eljeffe
│   ├── /warchest/03-the-play
│   ├── /warchest/04-the-product
│   ├── /warchest/05-the-architecture
│   ├── /warchest/06-the-data-model
│   ├── /warchest/07-how-we-build
│   ├── /warchest/08-the-team
│   ├── /warchest/09-compliance
│   ├── /warchest/10-protection
│   ├── /warchest/11-the-article
│   └── /patents                       Patent visualizations (7 figures)
│
├── brand.growdirect.io/               ← Brand system reference
│   ├── /                              Design tokens, palette, typography
│   ├── /canary                        Canary sub-brand guide
│   └── /assets                        Logos, icons, templates
│
├── ops.growdirect.io/                 ← Operations dashboard
│   ├── /                              Status overview
│   ├── /brain                         Brain wiki browser
│   ├── /factory                       Factory process + sprint status
│   └── /diagrams                      Process diagram library
│
└── docs.growdirect.io/                ← Technical documentation
    ├── /canary                        Platform overview, architecture, detection, data model
    ├── /canary/sales-strategy         Sales strategy + gold list
    ├── /cove                          Cove platform docs
    └── /api                           API reference (future)
```

---

## Content Mapping — Existing Assets → Subdomains

### Hub (growdirect.io)

| Asset | Source | Status |
|-------|--------|--------|
| Hub index page | NEW — to be built | Blueprint |
| Brand identity system | Extracted from all existing HTML files | Codified |

### canary.growdirect.io

| Asset | Source | Status |
|-------|--------|--------|
| Product landing | `Canary_LP_Coming_Soon.html` (uploaded) | Exists — needs polish |
| App prototype | `Canary_Prototype_v2.0.html` (uploaded) | Exists — reference |
| Flask app | `Canary/` codebase (port 5001) | Running |
| Atlas browser | `Canary/docs/atlas/browser/` | Running |
| CRDM technical doc | `Canary_CRDM_v2.0.html` (uploaded) | Exists |
| JSONB forensic analysis | `Canary_JSONB_Forensic_Analysis_v1.0.html` (uploaded) | Exists |
| Technical roadshow | `canary_technical_roadshow_v1.0.html` (uploaded) | Exists |
| Landing page (static) | `Canary/static/landing/index.html` | Exists |

### investors.growdirect.io

| Asset | Source | Status |
|-------|--------|--------|
| Gate + index | `index-bf803233.html` (uploaded, War Chest index) | Exists |
| Manifesto | `GrowDirect_Manifesto_Investor.html` (uploaded) | Exists |
| elJeffe diagram | `02-eljeffe-v3.html` (uploaded) | Exists |
| Magazine article | `Canary_LP_Magazine_Article.html` (uploaded) | Exists |
| Component business model | `Canary_Component_Business_Model_v1.0.html` (uploaded) | Exists |
| Factory process | `Canary_Factory_Process_v2.0.html` (uploaded) | Exists |
| Patent visuals (7) | `docs/_archive/ip-vault/patent-visuals/` | Exist |

### brand.growdirect.io

| Asset | Source | Status |
|-------|--------|--------|
| Brand system reference | NEW — extracted from all HTML files | To build |
| Canary sub-brand | Consistent across all Canary HTML | Codified |

### ops.growdirect.io

| Asset | Source | Status |
|-------|--------|--------|
| Brain wiki | `Brain/wiki/` (54 articles) | Exists |
| Process diagrams | `Process_Diagrams_Library.html` (uploaded) | Exists |
| Mermaid atlas | `index.html` (uploaded, atlas index) | Exists |
| Factory process | `Canary_Factory_Process_v2.0.html` (uploaded) | Exists |

### docs.growdirect.io

| Asset | Source | Status |
|-------|--------|--------|
| Platform overview | `Brain/wiki/canary-platform-overview.md` | Exists |
| Architecture | `Brain/wiki/canary-architecture.md` | Exists |
| Detection engine | `Brain/wiki/canary-detection.md` | Exists |
| Data model | `Brain/wiki/canary-data-model.md` | Exists |
| Sales strategy | `Brain/wiki/canary-sales-strategy.md` | Exists |
| Workflow | `Brain/wiki/growdirect-workflow.md` | Exists |

---

## Brand System (Codified)

### Colors

```
--ink:           #0D1117    (primary background)
--card:          #161B22    (surface/card)
--border:        #21262D    (borders)
--signal-yellow: #FBBF24    (primary accent — Canary gold)
--accent-gold:   #F59E0B    (secondary accent)
--deep-amber:    #D97706    (tertiary)
--btc-orange:    #F7931A    (Bitcoin references)
--text-primary:  #E5E7EB    (body text)
--text-muted:    #6B7280    (secondary text)
--text-dim:      #4B5563    (labels, captions)
--health-green:  #059669    (positive/success)
--health-red:    #EF4444    (critical/error)
--health-blue:   #3B82F6    (info/links)
```

### Typography

```
Headings:  Space Grotesk (400-700) — clean, technical authority
Body:      Inter (300-700) — readability, professionalism
Code:      Space Mono (400-700) — monospace for labels, data, code
Display:   Playfair Display (400-900) — editorial/investor pieces only
Narrative: DM Serif Display — elJeffe/treasury aesthetic only
Impact:    Bebas Neue — War Chest gate/titles only
```

### Component Patterns

- Dark background, gold accent borders
- Cards: `--card` bg, 1px `--border`, 8-12px radius
- Gold gradient buttons: `linear-gradient(135deg, #FBBF24, #D97706)`
- Section labels: Space Mono, 8-10px, uppercase, letter-spacing 0.15-0.25em
- Blockquotes: 3px gold left border, faint gold background
- Tables: Space Mono headers, hover row highlight
- Navigation: fixed top, backdrop-filter blur, gold active states

### Sub-Brand Variations

| Context | Bg | Accent | Display Font | Tone |
|---------|-----|--------|-------------|------|
| **GrowDirect Hub** | #080808 | #F7931A → #FBBF24 | Bebas Neue | Command center |
| **Canary Product** | #0D1117 | #FBBF24 | Space Grotesk | Professional SaaS |
| **Investor/War Chest** | #060608 | #C8A55A / #E8920F | Playfair Display | Treasury/editorial |
| **Technical Docs** | #0D1117 | #F59E0B | Space Grotesk | Reference |
| **Operations** | #0D1117 | #FBBF24 | Inter | Dashboard |

---

## Implementation Plan

### Phase 1: Hub + Brand (This session)
- Build growdirect.io hub index page
- Build brand.growdirect.io reference page
- Map all existing assets to their subdomain homes

### Phase 2: Investor Subdomain
- Consolidate War Chest into investors.growdirect.io
- Clean up gate mechanism
- Ensure all 11 chapters + manifesto are linked

### Phase 3: Canary Product Subdomain
- Polish the Coming Soon landing
- Link to running Flask app
- Organize technical docs under /docs

### Phase 4: Ops + Docs
- Brain wiki browser
- Process diagram library
- Wiki-to-HTML renderer for docs subdomain

---

## DNS Strategy

All subdomains resolve locally in development. Production deployment TBD — likely Cloudflare Pages or similar static hosting for public assets, with Flask apps behind a reverse proxy.

```
# /etc/hosts (local dev)
127.0.0.1  growdirect.io
127.0.0.1  canary.growdirect.io
127.0.0.1  cove.growdirect.io
127.0.0.1  investors.growdirect.io
127.0.0.1  brand.growdirect.io
127.0.0.1  ops.growdirect.io
127.0.0.1  docs.growdirect.io
```
