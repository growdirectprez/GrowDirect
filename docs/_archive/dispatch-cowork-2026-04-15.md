# Cowork Dispatch — April 15, 2026

## Session Summary

Cowork session reformatted the Canary Technical Library documents from real
source files, updated both public-facing site pages, added a Portfolio section
to growdirect-hub.html, and cleaned up old generated files. Everything is ready
to commit and deploy.

---

## What Changed

### 1. Canary Technical Library — 5 Documents Reformatted

Replaced fake generated documents with reformats of the REAL source HTML files
from `.worktrees/goose-credit-system/docs/_archive/`. Each document now uses a
single shared stylesheet (`canary docs.css`) with consistent nav, header,
footer, and cross-links.

| New File | Source |
|---|---|
| `Canary Technical Library/Canary Data Model.html` | `warchest/site/the-crdm.html` |
| `Canary Technical Library/Canary Platform Architecture.html` | `warchest/site/the-architecture.html` |
| `Canary Technical Library/Canary Technical Roadshow.html` | `workorders/output/docs/canary_technical_roadshow_v1.0.html` |
| `Canary Technical Library/Canary Factory Process.html` | `warchest/site/how-we-build.html` |
| `Canary Technical Library/Canary elJeffe Protocol.html` | `warchest/site/eljeffe.html` |

The shared stylesheet was already in place from an earlier session:
`Canary Technical Library/canary docs.css`

### 2. canary.growdirect.io.html — Gated Section Updated

- Technical Deep Dive doc cards now link to the reformatted library files
- Cards are `<a>` tags (clickable) pointing to `Canary Technical Library/*.html`
- Removed "Sales Strategy" and "JSONB Forensic Analysis" cards
- Replaced with "Platform Architecture" and "elJeffe Protocol" cards
- Gate contents list updated to match the 5-doc set
- Description text updated (removed "sales strategy" mention)

### 3. growdirect-hub.html — Portfolio Section Added, What's Built Removed

- **Removed** section 04 "What's Built" (stats, checklist, patent cards)
- **Added** section 04 "The Portfolio" with 4 case-study cards:
  - **Canary LP** — detection engine, enterprise lineage, stats, stack tags
  - **Cove** — HOA governance, Leaflet.js maps, 81 parcels, LA County GIS
  - **Angel** — real estate intelligence, Compass agents, pgvector embeddings
  - **Consulting & Advisory** — 30+ years background, Tesco/Walmart/RTI/SMART, contact
- Nav updated: removed "Built" link, added "Portfolio" anchor link
- Footer updated to match nav
- Section numbers renumbered (Portfolio is now 04)

### 4. Files Deleted

- `Canary Technical Library/Canary Forensic Analysis.html` (wrongly generated)
- `Canary Technical Library/canary-docs.css` (old hyphenated duplicate)
- `canary-docs/` (empty leftover folder — already removed)

---

## Files to Stage

```bash
# New / modified
git add "growdirect-hub.html"
git add "canary.growdirect.io.html"
git add "Canary Technical Library/Canary Data Model.html"
git add "Canary Technical Library/Canary Platform Architecture.html"
git add "Canary Technical Library/Canary Technical Roadshow.html"
git add "Canary Technical Library/Canary Factory Process.html"
git add "Canary Technical Library/Canary elJeffe Protocol.html"
git add "Canary Technical Library/canary docs.css"

# Deleted
git rm "Canary Technical Library/Canary Forensic Analysis.html" 2>/dev/null
git rm "Canary Technical Library/canary-docs.css" 2>/dev/null
```

## Suggested Commit

```
feat(web): reformat technical library from source, add portfolio section

- Reformat 5 Canary Technical Library docs from real War Chest source HTML
- Shared stylesheet (canary docs.css) with consistent nav across all docs
- Update canary.growdirect.io.html gated section with clickable doc cards
- Remove sales strategy from gated content
- Add Portfolio section to growdirect-hub.html (Canary, Cove, Angel, Consulting)
- Remove What's Built section from growdirect-hub.html
- Clean up old generated files
```

---

## Deployment Notes

All files are static HTML. No build step required. Deployment depends on how
growdirect.io and canary.growdirect.io are currently hosted:

- If **GitHub Pages** or similar: push to the deploy branch, files go live
- If **manual upload**: the changed files are all in the repo root and
  `Canary Technical Library/` — upload those paths
- The `Canary Technical Library/` folder must be deployed alongside the site
  files since `canary.growdirect.io.html` links into it with relative paths

### Link Structure to Verify After Deploy

```
growdirect.io (growdirect-hub.html)
  ├── #thesis, #platform, #market, #portfolio (anchor sections)
  ├── canary.growdirect.io.html (nav link)
  └── #gate-section (investor gate, password: eljeffe2026)

canary.growdirect.io (canary.growdirect.io.html)
  ├── Public sections (hero, detection, fox, architecture, pricing)
  ├── #gate-section (technical deep dive, password: canary2026)
  └── Canary Technical Library/
      ├── canary docs.css (shared stylesheet)
      ├── Canary Data Model.html
      ├── Canary Platform Architecture.html
      ├── Canary Technical Roadshow.html
      ├── Canary Factory Process.html
      └── Canary elJeffe Protocol.html
          (each doc links back to ../canary.growdirect.io.html)
```

### Quick Smoke Test After Deploy

1. Load growdirect.io — verify Portfolio section renders with 4 cards
2. Click "Canary" in nav — verify canary site loads
3. Enter `canary2026` at the gate — verify 5 doc cards appear and are clickable
4. Click each doc card — verify document loads with shared styling and nav works
5. Click "← Canary" in any doc nav — verify it returns to the Canary site
