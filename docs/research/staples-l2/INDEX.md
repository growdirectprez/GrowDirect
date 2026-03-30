---
type: research
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Best Practices in Merchandise Planning: The Foundation of High Performance Retailing

> **Client:** Staples Inc.
> **Consultant:** Management Horizons, A Consulting Division of Price Waterhouse LLP
> **Date:** 1996
> **Format:** PowerPoint 4.0 (OLE2 binary) — 14 presentation files, Level 2 recommendations
> **Author metadata:** "Computer Technology Group", "Michele Kosow"

---

## Extraction Method

Text extracted from OLE2 binary PPT files using `strings -n 8` with noise filters (font names, binary artifacts, template metadata). This is not OCR — diagrams, charts, and embedded images are not captured. Expect gaps in structured content (tables, flowcharts, Visio embeds).

---

## File Inventory

| File | Topic | Slides | Lines | Status |
|------|-------|--------|-------|--------|
| `DIST_REC.PPT` | Distribution Recommendations | 40 | 1,220 | Extracted → `DIST_REC.md` |
| `IMPT_REC.PPT` | Import Recommendations | 32 | 1,307 | Extracted → `IMPT_REC.md` |
| `LOG_REC.PPT` | Logistics Recommendations | 7 | 719 | Extracted → `LOG_REC.md` |
| `MERCHPL2.PPT` | Merchandise Planning | 34 | 520 | Extracted → `MERCHPL2.md` |
| `MPLN_APX.PPT` | Merchandise Planning Appendix | 18 | 240 | Extracted → `MPLN_APX.md` |
| `OPEN.PPT` | Open-to-Buy | 17 | — | Previously extracted → `OPEN.txt` |
| `PEM_RC.PPT` | Promotions/Event Management | 16 | 692 | Extracted → `PEM_RC.md` |
| `PLANOGRA.PPT` | Planogram/Floor Plan | 17 | 304 | Extracted → `PLANOGRA.md` |
| `PM_REC.PPT` | Purchase Order Management | 19 | 739 | Extracted → `PM_REC.md` |
| `POM_RC.PPT` | Purchase Order Management | 17 | 336 | Extracted → `POM_RC.md` |
| `PRICEMAN.PPT` | Price Management | 13 | 258 | Extracted → `PRICEMAN.md` |
| `RDM_REC.PPT` | Replenishment/Demand Management | 36 | 2,092 | Extracted → `RDM_REC.md` |
| `SCIM_REC.PPT` | Supply Chain/Inventory Management | 42 | 2,191 | Extracted → `SCIM_REC.md` |
| `VEND_MAN.PPT` | Vendor Management | 27 | 934 | Extracted → `VEND_MAN.md` |

**Total:** 14 files, 335 slides, ~11,552 lines of extracted text (13 .md files + 1 prior .txt)

---

## Source Location

- **Original files:** `/tmp/stpl_lv2/STAPLES/LEVEL2/`
- **Extracted text:** `~/GrowDirect/docs/sources/stpl_lv2/`

---

## Notes

- PM_REC.PPT and POM_RC.PPT both cover Purchase Order Management — likely different phases or revisions
- MERCHPL2.PPT and MPLN_APX.PPT are the core merchandise planning deck and its appendix
- SCIM_REC.PPT (42 slides, 2,191 lines) and RDM_REC.PPT (36 slides, 2,092 lines) are the largest and most content-rich
- LOG_REC.PPT is the smallest at 7 slides but still yielded 719 lines (Visio diagram metadata)
- Many slides contain embedded Visio flowcharts and diagrams — only text labels survive `strings` extraction
- Line counts include header metadata (~8 lines per file)

---

*Extracted 2026-03-09 | GrowDirect Inc.*
