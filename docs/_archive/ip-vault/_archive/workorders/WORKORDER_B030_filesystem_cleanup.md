---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# WORKORDER B-030 — GrowDirect Filesystem Cleanup + Knowledge Inbox

**Status:** Design Only — Not Yet Built
**Phase 1:** Immediate manual cleanup (one-time, Jeffe executes)
**Phase 2:** Inbox pipeline build (Sprint 6)
**Owner:** ALX (design) → Jeffe (Phase 1 execution) → Jeremy (Phase 2 build)
**Created:** Feb 26, 2026
**Blocker Ref:** B-030 in TRIAGE.md

---

## Proposed Top-Level Structure

```
GrowDirect/
├── _ALX/              ← Operational, unchanged
├── _Inbox/            ← New: drop zone for all intake
├── _Vault/            ← New: PSTs + sensitive archives, preserved as-is
├── _Archive/          ← New: ingested originals, never deleted
├── Canary/            ← Codebase, unchanged
├── Canary_IP/         ← Confidential IP, Condor-only, unchanged
├── Company/           ← Corp structure, unchanged
├── Documents/         ← Timelogs + templates, unchanged
├── Knowledge/         ← Renamed from _Knowledge, clean content only
├── bolt.diy/          ← Third-party app, unchanged
└── growdirect-ops/    ← Ops repo, unchanged
```

---

## Phase 1 — Immediate Manual Cleanup (One-Time, Jeffe Executes)

The following actions are manual and must be performed by Jeffe before the inbox pipeline build begins.
**Do not automate these. Execute once, confirm done, then close Phase 1.**

### File Moves

| Action | Source | Destination |
|---|---|---|
| Move | `GrowDirect/Jeffe/Personal_Docs/` | `~/Personal/` (outside GrowDirect entirely) |
| Move | `GrowDirect/Jeffe/Notes/` | `~/Personal/` (outside GrowDirect entirely) |
| Move | `GrowDirect/Jeffe/Resume/` | `~/Personal/` (outside GrowDirect entirely) |

### Deletions

| Action | Target | Reason |
|---|---|---|
| Delete directory | `GrowDirect/Jeffe/` | Once emptied by moves above |
| Delete directory | `GrowDirect/data/` | Empty directory, no content |
| Delete directory | `GrowDirect/growdirect-ops-tmp/` | Temp directory, no longer needed |
| Delete file | `GrowDirect/CUSOR.rtf` | Already processed, trash |
| Delete file | `GrowDirect/FIG.rtf` | Already processed, trash |
| Delete file | `GrowDirect/PRD.rtf` | Already processed, trash |
| Delete file | `GrowDirect/SEO.rtf` | Already processed, trash |

### Rename

| Action | From | To |
|---|---|---|
| Rename directory | `GrowDirect/_Knowledge/` | `GrowDirect/Knowledge/` |

---

## Hard Boundary Rules (Permanent)

These directories are permanently off-limits to the inbox pipeline and any automated process.
**No script, agent, or pipeline may read from, write to, or reorganize these directories.**

| Directory | Rule | Reason |
|---|---|---|
| `Canary_IP/` | Condor-only. Never touched by inbox pipeline. | Confidential IP |
| `_ALX/` | Operational files. Never touched by inbox pipeline. | System state |
| `Canary/` | Codebase. Never touched by inbox pipeline. | Active development |
| `bolt.diy/` | Third-party app. Never touched. | Vendor code |
| `_Vault/` | Write-once. Never unpacked automatically. PSTs preserved as-is. | Sensitive archives |

---

## Phase 2 — Inbox Pipeline Spec (Design Only — Build Sprint 6)

### Overview

A file watcher monitors `_Inbox/`. On file drop, the pipeline:
1. Scrubs (decide keep/skip/vault/flag)
2. Deduplicates (SHA-256 hash check against manifest)
3. Extracts content
4. Produces output envelope
5. Disposes of original (archive / delete / vault)

---

### Scrub Rules

| Rule | File Types | Action |
|---|---|---|
| Skip (binary junk) | `.dll` `.exe` `.ocx` `.bat` `.atb` `.dat` `.fsf` `.fsm` `.err` `.bmp` `.gif` `.ico` `.avi` `.DS_Store` | Delete immediately. Log deletion. |
| Extract text | `.md` `.txt` `.pdf` `.docx` `.xlsx` `.csv` `.pptx` `.htm` `.html` `.xsd` | Process through pipeline. |
| Vault immediately | `.pst` and any email archive format | Move to `_Vault/` untouched. Log. |
| Flag for Qwen vision (rig only) | `.jpg` `.png` | Mac: flag pending, do not process. Rig: route to Qwen vision pass. |

---

### Dedup Rules

- Compute **SHA-256 hash on file content** at ingest time.
- Manifest stored at `_Archive/manifest.json` — persists across sessions.
- **Duplicate = skip and log. Never process twice.**
- Same file dropped 10 times = processed once. Subsequent drops logged only.

---

### Disposition Rules

| Outcome | Action |
|---|---|
| Successfully ingested | Original moves to `_Archive/YYYY-MM/original-filename` |
| Confirmed duplicate | Log entry only. Original deleted. |
| Binary/junk (scrub skip) | Deleted immediately. Logged. |
| PST / email archive | Moved to `_Vault/` untouched. Logged. |

---

### Output Envelope

Every successfully ingested document produces a JSON record:

```json
{
  "id": "uuid",
  "source_file": "original path + filename",
  "source_type": "pdf|docx|md|...",
  "ingested_at": "ISO timestamp",
  "category": "inferred",
  "title": "extracted or inferred",
  "summary": "2-3 sentences",
  "content": "full extracted text",
  "chunks": ["paragraph-sized chunks for RAG"],
  "metadata": {}
}
```

---

### Bootstrap Pass (One-Time, Runs on First Pipeline Launch)

Processes all existing `Knowledge/` content on the first run:

1. Scan `Knowledge/` recursively.
2. Apply same scrub + dedup rules as live pipeline.
3. Intactix binaries (`.dll`, `.exe`, etc.) → deleted immediately, logged.
4. Intactix readable files (`.txt`, `.xsd`, `.htm`) → ingested then trashed.
5. All other readable Knowledge files → ingested, originals archived to `_Archive/YYYY-MM/`.

---

### Mac vs. Rig

| Environment | Watcher | Vision Pass |
|---|---|---|
| Mac (now, Sprint 6) | Runs locally | No vision. Images flagged pending. |
| Rig (Sprint 6+) | Migrates to Ubuntu | Qwen handles image/vision pass. |

---

## Open Questions (Before Sprint 6 Build)

- Where does the JSON output envelope land? (`Knowledge/` as `.json` sidecar? Separate `_Index/` directory?)
- Who reads the output envelope? (RAG pipeline, search index, both?)
- Does `_Vault/` need an index manifest or is file-system-only sufficient?
- Vision pass output format for flagged images — same envelope or separate?

---

*This work order is design-only. No files moved, no code written.*
*Phase 1 gate: Jeffe confirms cleanup complete before pipeline build begins.*
