---
type: wiki
tags: [cove, abalonecove, publication, 0-clipper, editorial]
created: 2026-04-17
last-compiled: 2026-04-18
needs-review: 2026-05-02
---

# abalonecove.org

Public editorial site for the Abalone Cove Foundation. A long-form investigative article about the 0 Clipper Road development proposal, the legal and geological history of the Palos Verdes south coast, and the regulatory layers that were supposed to protect it.

## Status

Active development. First draft complete and author-reviewed. Major structural rewrite in progress (April 2026). Hosted on GitHub Pages at abalonecove.org (CNAME set, Cloudflare DNS).

## What This Is

A single long-form article (~7,000+ words) written in the voice of an HOA community member who used AI tools to research the history of Abalone Cove and the legal record behind a proposed 16-unit development on an active landslide. The site is the article. Everything else supports the read.

**Thesis:** This land has never been built on for a reason. The public record proves it. The system designed to protect it doesn't work unless someone does the homework.

**Voice:** First-person, community member. Restrained, factual, planning-committee appropriate. Charles C. Mann's *1491* as tonal reference — an investigative mind surprised by what they found.

## Repo

`~/abalonecove/` — separate repo from GrowDirect. GitHub Pages deployment.

## Site Structure

| Page | Path | What it is |
|------|------|------------|
| Article | `/index.html` | Main narrative |
| Evidence Room | `/evidence/` | 24+ linked primary source documents |
| Map | `/map/` | Interactive Leaflet map with layer controls |
| Timeline | `/timeline/` | Chronological overview |
| Sign | `/sign/` | Action / petition page |
| About | `/about/` | About the foundation |

## Article Sections (current structure)

1. **What's a Quorum?** — HOA meeting cold open, $300/year budget, SB 9 fight
2. **The Layers** — Tongva/Cabrillo, Bixby partition, Lot H vellum, Vanderlip, Olmsted plan, Declaration 1, PVE development map, Portuguese Bend Red Tile District, Declarations 100/101, Filiorum grant deed, 2014 redevelopment conveyance, microfilm discovery, deed images
3. **Cityhood** — PVE covenant model, Rolling Hills (gated, 1,739 pop, $250K+ income), RPV 1973, Coastal Specific Plan 1978, Moratorium, *Monks v. RPV* (2008), permanent moratorium 2025, FEMA $42M buyout, Montrose DDT / Superfund, Tongva / Sepulveda authority question
4. **Condos vs. the Beach** — 1972 Shore Club vote, Karl Rodi, Dick Karshner, park created
5. **The Wong Subdivision** — 1980 Tract 32977, four SFR lots + open space, 1986 reversion, previous owners, Clipper Development LLC, Hankey Capital loan
6. **The Rezoning** — Three ordinances in 63 days, density miscalculation, FPPC complaint, litigation (24TRCP00352), HCD confirmation city doesn't need Site 16, Dudek named as consultant (also holds PVE contract)
7. **The Research** — Garage discovery, Betty's archive, Doug Rucker, Vanderlip signature, AI methodology, Lot H correction, Declaration 100/101 discovery, GIS mapping
8. **Current Conditions** — Road conditions, HOA budget, regulatory asymmetry, leftovers/Parcel 106 framing, PV Blue Butterfly (ESA), proposal (revert to Wong), 501(c)(3)

## Evidence Room Documents

24+ transcribed primary sources organized by category:
- **Declarations** — Dec 1, 100, 101, Lot H, One, One-A, easements, 2009 restated
- **Litigation** — FPPC complaint, demurrer, opposition, city council comment
- **Shore Club** — Board docs, Filiorum lease, Karshner proposal, fact sheet
- **Geological** — County surveyor CSB 1082-2, CSB 1082-3
- **Tract Maps** — 1880 Rancho patent, Tract 14649
- **Chain of Title** — title chain document

## Key Findings Documented

### Dudek (consultant)
Encinitas-based environmental/planning firm. Holds housing element contracts for both RPV and PVE simultaneously. Funded by state HCD grants (SB 2 + LEAP). Presented to RPV planning commission April 2025.

### Declaration 101 / Shoreline Park Crosswalk (verified 2026-04-17)
The five Shoreline Park parcels conveyed to the city in 2014 are subdivisions of Declaration 101 Parcels 1 and 5. Five match points verified: same Lot H, same Case 2373, same Mean High Tide Line, same road right-of-way, same PV Corp → Filiorum deed chain. Declarations 100 and 101 were never referenced in the 2014 conveyance. Documented in [[Brain/wiki/cove-rpv-redevelopment-conveyance|RPV Redevelopment Conveyance]] wiki.

### Olmsted History (verified)
FLO Sr. died 1903 — zero connection to PV. FLO Jr. built house at 2101 Rosita Place, Malaga Cove (Hunt & Chambers, 1925-27). Library of Congress holds 385 plans for the PV project (Job #05950).

### Montrose Chemical / DDT
1,700 tons DDT discharged via White Point outfall (1947-1982). 110 tons remain on PV Shelf (17 sq mi). 25,000-100,000 barrels on seafloor. $140M Superfund settlement (2000). Fish advisories active since 1985. Abalone Cove SMCA established 2010/2012 under MLPA (not DDT-driven, but same waters).

## Images

| Image | File | Location in article |
|-------|------|-------------------|
| Pre-development aerial | hdl-10584 | Hero |
| Postcard | hdl-15658 | Break after Section 1 |
| Lot H partition map | hdl-13328 | Layers — Bixby |
| 1914 Olmsted topo | Topo_1914.png | Layers — Vanderlip purchase |
| PVE development map | 69.jpeg | Layers — Declaration 1 |
| Olmsted site plan | olmsted 1.jpg | Layers — Portuguese Bend |
| Filiorum deed (grant) | filiorum-deed-grant.jpeg | Layers — after microfilm |
| Filiorum deed (restrictions) | filiorum-deed-restrictions.jpeg | Layers — page six |
| Neptune Fountain / La Venta | Unknown-1.jpeg, Unknown.jpeg | Removed (Lawyer Brothers section replaced) |
| Gruen master plan | 1953-gruen crop | Removed (Coastal Wall replaced) |
| Field book survey | Screenshot 1.19.43 | Break before Research |
| Doug Rucker rendering | original rendering.png | Research |
| Abalone Cove beach | IMG_0346.jpeg | Closing |

## Editorial Decisions

- **No rhetoric.** Facts do the work. The reader draws conclusions.
- **Planning committee appropriate.** Could be handed to a commissioner.
- **Dudek named.** With PVE dual-contract flagged.
- **Lot H correction preserved.** Admitting the CC&R strategy was wrong builds credibility.
- **"It's a creek" closer in Layers.** Physical reality, not legal argument.
- **501(c)(3) framing:** Fund the survey and legal opinion nobody else has done.

## What's Still Needed

- [ ] Fire station tie-back (Shell station, Parcel 106)
- [ ] AI reveal woven into narrative after reader sees Olmsted plans
- [ ] Surveyor's notation thread (CSB 1082-2 → Book 10226 → Declarations 100/101)
- [ ] CSB 1082-2 image (need PNG/JPG, only have PDF)
- [ ] Granicus video pull — April 8 or 22, 2025 planning commission meeting (Dudek presenter name, exact quote)
- [ ] CPRA request for Dudek contract and invoices
- [ ] Fact cards: Montrose/DDT, Tongva/Sepulveda, Abalone Cove marine preserve
- [ ] Declaration 1 external link (check PVEHA or county recorder)

## Related

- [[Brain/projects/Cove|Cove MOC]]
- [[Brain/wiki/cove-0-clipper|0 Clipper Road]]
- [[Brain/wiki/cove-rpv-redevelopment-conveyance|RPV Redevelopment Conveyance]]
- [[Brain/wiki/cove-legal-framework|Legal Framework]]
- [[Brain/wiki/cove-property-geology|Property & Geology]]
- [[Brain/wiki/cove-community-history|Community History]]
