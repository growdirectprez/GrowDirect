---
type: pitch
domain: business
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Known Issues & Content Gaps

> *Active issues, known limitations, and content gaps in the current briefing.*

---

## Critical Gaps (P0)

These items block investor readiness and require immediate attention.

| ID | Gap | Status | Owner |
|---|---|---|---|
| ISS-001 | **Financial Model** — No revenue model, unit economics, or projections exist. Investors expect CAC/LTV/ARPU/churn analysis and at least illustrative 3-year projections. | Resolved | v2.4 — The Financials (WP-4.4) |
| ISS-002 | **The Ask** — No funding round structure, use of proceeds, or milestone timeline. Cannot close investor conversations without this. | Open | Founder input required |
| ISS-003 | **Standard Disclaimers** — Forward-looking statement disclaimer now added (v2.3). | Resolved | v2.3 |

---

## High Priority (P1)

These items should be addressed before the next external distribution.

| ID | Gap | Status | Owner |
|---|---|---|---|
| ISS-004 | **Market Analysis** — No TAM/SAM/SOM section. Competitive landscape document exists internally but no investor-facing market narrative. | Resolved | v2.4 — The Market (WP-4.3) |
| ISS-005 | **Go-to-Market Plan** — No merchant acquisition strategy or sales motion documented for external audiences. Internal playbook exists. | Open | Sales + Founder |
| ISS-006 | **IP Protection — External Version** — Current protection page contains confidential details (provisional numbers, strategy specifics). Need a redacted external summary with general IP posture only. | Open | Legal |
| ISS-007 | **Money Transmitter Analysis** — Goose (Bitcoin/Lightning payments module) requires legal analysis on money transmitter classification before investor materials can describe payment processing specifics. | Open | Legal |

---

## Content Quality (P2)

| ID | Issue | Status | Owner |
|---|---|---|---|
| ISS-008 | **Naming Inconsistencies** — "El Jeffe" appears in The Play (should be "elJeffe"). "time chain" appears in some sections (should be "timechain"). | Open | Editorial |
| ISS-009 | **Named Competitors** — Some source files reference specific competitors by name (Oracle, AWS). Recommend removing or generalizing to avoid Lanham Act exposure. | Open | Legal review |
| ISS-010 | **Architecture Diagrams** — ASCII diagrams in architecture and data model sections need SVG conversion for professional presentation. | Open | Design |
| ISS-011 | **gLog Standalone Narrative** — gLog concept is currently embedded across three different files (architecture, article, investment thesis). Needs a dedicated standalone section. | Open | Research |
| ISS-012 | **Content Redundancy** — Approximately 40% overlap across investment thesis, article, and compliance sections. Needs editorial pass to reduce duplication. | Open | Editorial |

---

## Navigation & Technical (P2)

| ID | Issue | Status | Owner |
|---|---|---|---|
| ISS-013 | **Embed Pages Not Gated** — Pages with `embed_mode: full` (Economy, Product) are standalone HTML and bypass session authentication. Direct URLs are accessible without password. | Resolved | v2.5 — iframe wrap |
| ISS-014 | **Embed Pages Missing Nav** — Economy and Product pages are raw HTML — no top nav, no prev/next, no footer. Navigation dead-ends. | Resolved | v2.5 — iframe wrap |

---

## Future Enhancements (P3)

| ID | Enhancement | Status |
|---|---|---|
| ISS-015 | Canary Core investor narrative — no standalone overview of the core detection engine exists | Planned |
| ISS-016 | North Star standalone piece — product philosophy page for public site | Planned |
| ISS-017 | Career arc timeline SVG — visual founder journey | Planned |
| ISS-018 | Investor single-page site auto-builder from manifest feeds | Planned |
| ISS-019 | Public site builder (growdirect.io) from public-feed sections | Planned |

---

## Resolution Log

| ID | Resolved In | Resolution |
|---|---|---|
| ISS-001 | v2.4 | The Financials page added — revenue model, unit economics, 3-year projections, operating costs |
| ISS-003 | v2.3 | Disclaimer page added with forward-looking statements, IP notice, confidentiality |
| ISS-004 | v2.4 | The Market page added — TAM/SAM/SOM, competitive landscape, moat analysis, platform play |
| ISS-013 | v2.5 | Embed pages (Economy, Product) wrapped in iframe within standard page template — auth, nav, prev/next, footer all present |
| ISS-014 | v2.5 | Same as ISS-013 — embed pages now have full navigation chrome |
| — | v2.1 | Internal team name reference in product prototype replaced with role label |
| — | v2.2 | elJeffe/Economy duplicate resolved by setting elJeffe feeds to empty |
| — | v2.5 | elJeffe converted from embedded HTML to narrative markdown, re-added to pack feeds |

---

*Last updated: February 27, 2026*
*GrowDirect Confidential*
