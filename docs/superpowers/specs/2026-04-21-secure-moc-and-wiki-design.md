---
title: Secure MOC + Product Wiki — Sprint 1
date: 2026-04-21
project: Secure (new)
related:
  - Canary (domain handoff)
  - content-engine (parser pipeline extension)
status: Design approved, ready for implementation plan
---

# Secure MOC + Product Wiki — Sprint 1

## Problem

The `/Users/gclyle/secure/` archive holds 2,251 files from Gary's IBM / Appriss /
Sysrepublic retail loss-prevention career (~2001–2019). The archive contains the
**Secure product suite** (Secure 5, Secure Lite, Omnichannel, SSO, Factory,
Appriss retail spec) plus 33 client implementation folders in `PROJECTS/`.

This is directly adjacent IP to **Canary**, which is rebuilding retail loss
prevention for Square merchants today. None of it is in Brain. The knowledge is
not searchable, not citeable, and not feeding Canary's wiki or SDDs.

Secondary signals outside the curated archive:

- NAS `archive/Work/Clients/SECURE 5/` — 22 files, 2017 EBR4/EBR5 era (5.8MB)
- NAS `archive/Work/Recovered/Secure Files/` — 16K, near-empty
- NAS `archive/Email/CLIENTS/SECURE 5/` — 16K

These are complements to the local archive, not replacements. The local
curated archive is the primary source of truth for Sprint 1.

## Goal

Ship a navigable Brain structure for Secure:

- A Project MOC at `Brain/projects/Secure.md` (modeled on `Canary.md`)
- 4 product wiki articles synthesizing the top-level Secure product docs
- 1 pilot client deep-dive (Kroger)
- 1 stub for the pre-Secure career archive
- 1 Canary-facing handoff brief identifying patterns worth porting

Out of band: extend `content-engine/engine.py` with a binary→markdown extraction
stage so the existing `triage` / `ingest` / `registry` pipeline can work on
Office + PDF files.

## Scope

### In scope (Sprint 1)

- **Engine extension:** new `engine.py extract` command to convert `.doc`,
  `.docx`, `.ppt`, `.pptx`, `.xls`, `.xlsx`, `.pdf` to `.md` via `markitdown`
  with fallback for files that fail.
- **Brain structure:**
  - `Brain/projects/Secure.md` — Project MOC
  - `Brain/wiki/secure-platform-overview.md` — what Secure was, product line,
    architecture shape, positioning vs Canary
  - `Brain/wiki/secure-architecture.md` — S5 on-premise solution architecture,
    SSO, factory/delivery process
  - `Brain/wiki/secure-lite.md` — Secure Lite product variant (overview + config)
  - `Brain/wiki/secure-omnichannel.md` — omnichannel positioning, Appriss retail
    data spec relationship
  - `Brain/wiki/secure-client-kroger.md` — pilot client deep-dive (Kroger CRP +
    DSD)
  - `Brain/wiki/retail-career-archive.md` — stub wiki article indexing the
    pre-Secure `PROJECTS/` client folders with one-line descriptions per folder;
    flagged as "circle back later"
- **Canary handoff brief** (working doc, not wiki):
  `docs/superpowers/briefs/2026-04-secure-to-canary-handoff.md` — patterns,
  schemas, detection concepts, and lessons from Secure that Canary should
  adopt or explicitly reject.
- **Classification working doc:**
  `docs/superpowers/briefs/2026-04-secure-client-split.md` — list of `PROJECTS/`
  folders classified Secure-era vs pre-Secure IBM, with confidence notes.
- **Registry update:** `Brain/REGISTRY.json` rebuilt after ingest so Secure
  content is searchable via `engine.py registry check`.

### Out of scope (future sprints)

- Bulk triage + ingest of the 33 `PROJECTS/` client folders beyond Kroger.
- Deep-dives on Wal-Mart, Harrods, Staples, Toys R Us, Fresh & Easy, Retek, SAP,
  etc.
- A separate `Retail-Career` MOC — stays as a stub wiki article for now.
- Founder-credibility curation (sales-ready subset for Canary).
- NAS deduplication across the three scattered Secure locations.
- Pulling in the NAS `SECURE 5` 2017 era content (22 files) — defer to Sprint 2
  if useful.

## Parser pipeline design

### New command: `engine.py extract`

```
python3 content-engine/engine.py extract <source-dir> \
  --target <output-dir> \
  [--ext doc,docx,ppt,pptx,xls,xlsx,pdf] \
  [--skip-tmp] \
  [--dry-run/--execute]
```

**Behavior:**

1. Walk `<source-dir>`, filter by extension.
2. For each file, call `markitdown` to convert to markdown.
3. Write the markdown to `<output-dir>/<relative-path>.md`, preserving tree
   structure (not flattened — keeps provenance).
4. On failure, fall back to:
   - `.doc` → `textutil -convert txt` (macOS built-in) or `catdoc`
   - `.pdf` → `pdftotext`
   - `.xls` → `libreoffice --headless --convert-to csv` or `xlrd`
   - record failure in `<output-dir>/.extract-failures.json`
5. Write `<output-dir>/.extract-manifest.json` with per-file source hash,
   extraction method, extraction status.
6. Skip Office temp artifacts (`~$*.docx`, `.tmp`, `.old`).

**Dependency:** `markitdown` (MS-maintained, Apache-2.0). Pinned in
`content-engine/requirements.txt` or the engine's venv. Per user standing
instruction: dependency add is flagged, approved, committed, and image rebuilt
before use.

### Pilot test

Run `extract` on three files from `~/secure/` before scaling:

- `Secure 5 Solution Architecture.docx` (complex Word doc with diagrams)
- `Secure Omnichannel Overview-Oct2018.pdf` (PDF)
- `5.1 Requirements.xlsx` (9.6MB Excel — largest top-level file)

If all three produce usable markdown, proceed. If not, add fallback pathways
for that file type before scaling.

### Scale-out targets (Sprint 1)

- Top-level `~/secure/*.{docx,doc,pdf,pptx,xlsx}` — 16 files
- `~/secure/PROJECTS/Kroger CRP/` — all files
- `~/secure/PROJECTS/NOTES/` — likely contains architecture notes worth mining

Output goes to `Secure/docs/extracted/` (new project dir; mirrors the mental
model of `Cove/docs/archive/`).

## Brain structure

### Project MOC: `Brain/projects/Secure.md`

Modeled on `Canary.md`. Frontmatter:

```yaml
type: project-moc
status: archive-active
tags: [secure, retail, loss-prevention, ibm, appriss, canary-lineage]
```

Sections:

1. **Status** — archive (product shipped, company history), active for Canary
   cross-reference.
2. **Wiki Articles** — the 6 articles above.
3. **Source Archive** — pointer to `~/secure/` local + NAS paths.
4. **Canary Lineage** — link to `secure-to-canary-handoff.md` brief + relevant
   Canary wiki articles that draw on Secure thinking.
5. **Client Implementations** — link to Kroger deep-dive + pointer to stub for
   future deep-dives.
6. **Related Projects** — `Brain/projects/Canary.md` (forward) and
   `retail-career-archive.md` (pre-Secure).

### Wiki articles

Each article follows `Brain/templates/` structure (check `Brain/templates/` for
the wiki template before writing; match existing `angel-*` and `canary-*`
patterns).

- **`secure-platform-overview.md`** — synthesis of all top-level product docs.
  Answers: what was Secure, who bought it, what problem did it solve, what was
  the architecture, how does it map to Canary today. Draws on: `Secure 5
  Solution Architecture`, `Secure Omnichannel Overview`, `Factory Overview v2`,
  `New Delivery Process`, `Secure Lite Overview`.

- **`secure-architecture.md`** — deeper technical article. S5 on-premise
  architecture, SSO integration, factory/delivery process. Draws on:
  `S5 On Premise Solution Architecture v1.1 Draft`, `SSO Overview v2`,
  `Factory Overview v2`, `New Delivery Process`, `Dev Ops`, `Dev Ops
  Deliverables`.

- **`secure-lite.md`** — product variant. Draws on: `Secure Lite Overview`,
  `Secure Lite Config`.

- **`secure-omnichannel.md`** — omnichannel positioning + data model. Draws on:
  `Secure Omnichannel Overview-Oct2018.pdf`, `Appriss Retail Data Specification
  v1.1.pdf`, `5.1 Requirements.xlsx`, `Kroger DSD requirements.docx`.

- **`secure-client-kroger.md`** — Kroger implementation deep-dive. Draws on:
  all files in `~/secure/PROJECTS/Kroger CRP/` + `Kroger DSD requirements.docx`
  + any Wal-Mart cross-references that mention Kroger.

- **`retail-career-archive.md`** — stub article. One-line per pre-Secure client
  folder with its era (IBM consulting 2001–2005, CEO Study 2006, etc.), size,
  and status "Not ingested — circle back later." Keeps the knowledge that these
  folders exist without ingesting them.

## Sprint chunks (execution order)

1. **Engine `extract` command** — implement, test on the three pilot files,
   verify markdown is useful.
2. **Client classification** — write `secure-client-split.md` based on folder
   names + file mtimes + a filename scan. Output: confirmed Secure-era list.
3. **MOC shell** — write `Brain/projects/Secure.md` with placeholder links to
   the 6 wiki articles.
4. **Extract + ingest top-level Secure product docs** (16 files) — into
   `Brain/raw/inbox/` via existing `engine.py ingest`.
5. **Synthesize 4 product wiki articles** from the intake notes, using
   `Brain/templates/` for structure.
6. **Pilot client deep-dive: Kroger** — extract `PROJECTS/Kroger CRP/` + the
   Kroger DSD doc, synthesize `secure-client-kroger.md`.
7. **Stub `retail-career-archive.md`** — from the classification working doc.
8. **Canary handoff brief** — mine the extracted Secure content for patterns
   worth porting. Write to `docs/superpowers/briefs/`.
9. **Registry rebuild** — `python3 content-engine/engine.py registry build`.
10. **MOC finalize** — update `Brain/projects/Secure.md` links, verify all
    articles render in Obsidian.

## Success criteria

- `Brain/projects/Secure.md` exists, renders, links resolve in Obsidian.
- 6 wiki articles exist, each under 200 lines, each cites specific source files
  from `~/secure/`.
- `engine.py extract` converts the 16 top-level docs + Kroger folder with ≥90%
  success rate. Any failures are logged in `.extract-failures.json` with reason.
- `engine.py registry check "secure"` returns the new wiki articles.
- Canary handoff brief identifies at least 5 concrete patterns/schemas/concepts
  Canary should adopt or explicitly reject, each with a source file citation.
- No hype copy — per standing feedback, all text is direct, serious, tangible.
- No volatile data in wiki — row counts and stats that belong in the DB stay
  out of Brain.

## Risks + unknowns

- **`markitdown` quality on 2001–2005 `.doc` files.** Old Word binary format
  can be messy. Mitigation: fallback chain (`textutil` → `catdoc` → skip with
  failure logged).
- **`.vsd` Visio files** (71 in archive). `markitdown` does not handle Visio.
  Out of scope Sprint 1; note in risks doc if any top-level file is `.vsd`.
  None are in top-level or Kroger CRP on spot-check.
- **Classification confidence** for ambiguous folders (`NOTES`, `RETAIL`,
  generic names). Acceptable to mark "unclassified — pre-Secure stub" in doubt.
- **PII in extracted content.** Client implementation docs may contain employee
  names, store numbers, transaction samples. Review before Brain intake.
  Mitigation: extract to `Secure/docs/extracted/` first, review, then ingest —
  do not push to `Brain/raw/inbox/` directly from `extract`.
- **Scope creep.** The temptation to deep-dive more clients than Kroger in
  Sprint 1. Resist. Ship one pilot cleanly, let Sprint 2 decide the next.

## Non-goals / explicit deferrals

- This sprint does NOT touch the NAS scattered Secure content beyond noting its
  existence in the MOC.
- This sprint does NOT build a second MOC for pre-Secure IBM work. That's a
  stub wiki article only. A proper `Retail-Career` MOC is a future decision.
- This sprint does NOT produce founder-credibility sales artifacts for Canary.
  That's a downstream curation pass using the extracted content as source.
- This sprint does NOT migrate `~/secure/` into the repo. The archive stays at
  its current path; Brain articles reference it by absolute path.

## File locations summary

| Artifact | Path |
|---|---|
| Source archive | `/Users/gclyle/secure/` (unchanged) |
| Extracted markdown | `Secure/docs/extracted/` (new) |
| Raw intake notes | `Brain/raw/inbox/` (existing) |
| Wiki articles | `Brain/wiki/secure-*.md` (new) + `retail-career-archive.md` |
| MOC | `Brain/projects/Secure.md` (new) |
| Working briefs | `docs/superpowers/briefs/2026-04-secure-*.md` (new) |
| Engine code | `content-engine/engine.py` (new `extract` command) |
| Registry | `Brain/REGISTRY.json` (rebuilt) |

## Dependencies on user

- Confirm `markitdown` as the extraction tool (user standing instruction: flag
  dependency changes, approve, commit, rebuild).
- Confirm Kroger as the pilot client (vs. Wal-Mart or Harrods).
- Confirm PII review gate: extracted docs stay in `Secure/docs/extracted/`
  until user signs off, then ingested.
