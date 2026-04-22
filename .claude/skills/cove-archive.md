---
name: cove-archive
roles-primary:[Writer]
description: |
  Document intake and archive management for the WPBCA archive at docs/archive/.
  Use when the user provides a new document (PDF, scan, image, typed text) to add
  to the community archive, when organizing or reorganizing archive files, or when
  updating the INDEX or narrative. Trigger on "add this to the archive", "here's
  a document", "parse this", "file this", or any WPBCA/Abalone Cove governance doc.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Cove Archive — Document Intake & Organization

Manages the WPBCA community archive at `docs/archive/`. Every document follows
the same chain of custody: **physical original -> scan (PDF) -> transcription
(markdown) -> archive entry -> index update**.

**Announce:** "I'm using cove-archive to process [document name]."

## Archive Structure

```
docs/archive/
├── INDEX.md                    — Master catalog of all documents
├── chain-of-title.md           — Legal lineage: PV Corp -> present
├── timeline.md                 — 1882-2026 chronological events
├── narrative.md                — 5-chapter member story
├── stubs.md                    — Documents we need but don't have
├── founding/                   — 1949-1952 declarations and deeds
├── governance/                 — Bylaws, restated declaration
├── property/                   — Assessor maps, title reports, EIR, parcel maps
├── shore-club/                 — Beach club history 1929-1972
├── litigation/                 — Court filings, FPPC complaint
├── analysis/                   — Legal briefs, strategy, research
├── media/                      — Newspaper clippings, photos, artwork
└── originals/                  — ALL source files (PDFs, scans, images)
```

## Intake Workflow

### Step 1: Identify and Categorize
Read the document. Determine what, when, who, and which category.

### Step 2: Store the Original
```bash
cp /path/to/source.pdf docs/archive/originals/{category}/{YYYY}-{descriptive-name}.pdf
```

### Step 3: Transcribe to Markdown
Create `docs/archive/{category}/{name}.md` with metadata table (date, recorded,
author, parties, covers, status, links to original/predecessor/successor/related),
summary, key provisions, **verbatim text** (every word, no edits), cross-references,
and stubs.

### Step 4: Update the Indexes
- **INDEX.md** — add row to category table
- **timeline.md** — add entries for new dates/events
- **narrative.md** — update if document strengthens any chapter
- **stubs.md** — add referenced documents we don't have

### Step 5: Verify Links
All original PDF links and cross-references resolve correctly.

### Step 6: Publish to Vault
If the document should be browsable on abalonecove.org, publish to the vault.

| Archive Category | Vault Category | Public? |
|-----------------|----------------|---------|
| founding | governing_documents | Yes |
| governance | governing_documents | Yes |
| property | archive | No |
| shore-club | archive | Yes |
| litigation | correspondence | No |
| analysis | archive | No |
| media | archive | Yes |

## Rules

- **Verbatim means verbatim.** Every word, every typo, every handwritten note.
- **One document per file.**
- **Links are relative.** `../originals/{category}/file.pdf`
- **Stubs are actionable.** What, why, how to get it.
- **No duplicate files.**

---

*Cove Archive v1.0 — Document Intake & Organization*
