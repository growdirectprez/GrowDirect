---
title: Batch Inbox Intake — parse all queued corpora in one run
date: 2026-04-24
type: dispatch
status: ready-to-run
scope: content-engine
---

# Batch Inbox Intake

**Governing thesis:** Six corpora sit in `Brain/raw/inbox/` already cataloged in `_queue.md` but not yet ingested as Brain raw-intake notes. The content engine already knows how to extract Office/PDF to markdown and how to create Brain notes from files — it just needs to be pointed at all six folders in sequence, with per-file failures logged rather than halting the run. This dispatch does that.

## Scope

| Corpus | Files | Project tag | Key tags |
|---|---|---|---|
| `SWINDON/` | 359 | retail | pwc, swindon, sap-retail, broadvision, coe, 1999 |
| `Katz/` | ~100 | retail | pwc, katz, scm, rfp, 2003 |
| `Other Retek Decks/` | 29 | retail | retek, rms, rib, rdm, 2003-2005 |
| `BV Nuggets/` | 6 | retail | broadvision, pwc, lessons-learned, 1999-2000 |
| `EBiz Def Des Dev/` | 3 | retail | pwc, methodology, web-implementation-guide, 2000 |
| `BP/` | 46 | retail | consulting-reference, pwc, mh, petsmart, finance, 1997-1999 |

Explicit non-goals: the six original binary uploads from the earlier session dispatch (Over Short Reporting, Property App, etc.) are not in scope — those have their own intake track.

## Pipeline

```
         ┌──────────────────────────────┐
  src →  │ engine.py extract            │  → Brain/raw/.extract/<folder>/*.md
         │   (markitdown-backed)        │     + .extract-manifest.json
         └──────────────────────────────┘     + .extract-failures.json
                       │
                       ▼
         ┌──────────────────────────────┐
  .md →  │ engine.py ingest             │  → Brain/raw/inbox/<slug>.md
         │   (one call per file)        │     (with frontmatter + tags)
         └──────────────────────────────┘
                       │
                       ▼
         ┌──────────────────────────────┐
         │ engine.py registry build     │  → Brain/REGISTRY.json
         └──────────────────────────────┘
```

Per-file failures at any stage are logged and skipped — the run does not halt.

## Run

```bash
bash /Users/gclyle/GrowDirect/content-engine/batch-intake.sh
```

Nothing else required. The script uses absolute paths and discovers the GrowDirect root on its own.

## What to check afterward

1. **Log** — `Brain/raw/.logs/batch-intake-<timestamp>.log` — full stdout+stderr. Tail for summary: `tail -30 <log>`.
2. **Per-corpus extract manifests** — `Brain/raw/.extract/<folder>/.extract-manifest.json` — which files parsed, which failed.
3. **Per-corpus failures** — `Brain/raw/.extract/<folder>/.extract-failures.json` if any (absent = no failures).
4. **New intake notes** — `Brain/raw/inbox/*.md` with frontmatter `status: unprocessed` — these are the parsed files ready for synthesis.
5. **Registry** — `Brain/REGISTRY.json` — should tick up by the count of new intakes.

## Caveats

- **Not idempotent.** Re-running this dispatch will create duplicate intake notes (engine.py ingest appends `-1`, `-2`, ... rather than overwriting). Run once per session; if the run fails partway, either clean `Brain/raw/inbox/` of the partial intakes before re-running, or narrow the `CORPORA` array in the script to the unfinished folders.
- **Tags are best-effort.** The `--tags` flag on ingest applies to every file in a corpus — good for provenance, rough for nuance. Synthesis passes will retag individual notes as wiki articles are authored.
- **Markitdown quality varies.** `.doc` and `.ppt` (legacy binary formats) sometimes extract with layout noise. `.docx`/`.pptx`/`.pdf` are cleaner. The extract-failures.json will surface what couldn't be parsed at all; partial/noisy extracts still land as intakes.
- **GemKey** and any other founder-memory provenance questions in the queue remain open — this dispatch parses the files but does not resolve identity questions. Those belong in the synthesis pass.

## After this runs

Queue entries for each corpus can be marked as intake-complete. Synthesis (inbox → wiki) remains a separate, founder-called operation.
