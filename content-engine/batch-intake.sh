#!/usr/bin/env bash
# batch-intake.sh — extract + ingest every queued inbox corpus in one run.
#
# Governing thesis: the content engine already knows how to extract Office/PDF
# to markdown (`engine.py extract`) and how to create Brain raw-intake notes
# from files (`engine.py ingest`). This script wires them together for the
# six corpora currently queued in Brain/raw/inbox/_queue.md so they can all
# be parsed in one unattended run. Per-file failures are logged and do NOT
# halt the pipeline.
#
# Pipeline:
#   1. For each corpus folder: engine.py extract → Brain/raw/.extract/<folder>/
#   2. For each extracted .md: engine.py ingest → Brain/raw/inbox/<slug>.md
#   3. engine.py registry build
#
# Run:
#   bash /Users/gclyle/GrowDirect/content-engine/batch-intake.sh
#
# Output:
#   - Per-corpus extract dirs under Brain/raw/.extract/
#   - Per-corpus .extract-manifest.json and .extract-failures.json
#   - Raw-intake notes in Brain/raw/inbox/
#   - Full run log in Brain/raw/.logs/batch-intake-<timestamp>.log
#
# NOT idempotent: re-running creates additional numbered intake notes
# (engine.py ingest appends -1, -2, ... to avoid overwrites). One-shot.

set -uo pipefail

# ── Paths ────────────────────────────────────────────────────────────────
ROOT="/Users/gclyle/GrowDirect"
ENGINE="$ROOT/content-engine/engine.py"
INBOX="$ROOT/Brain/raw/inbox"
EXTRACT_ROOT="$ROOT/Brain/raw/.extract"
LOG_DIR="$ROOT/Brain/raw/.logs"

TS="$(date +%Y%m%d-%H%M%S)"
mkdir -p "$LOG_DIR" "$EXTRACT_ROOT"
LOG="$LOG_DIR/batch-intake-$TS.log"

# ── Corpora in scope ─────────────────────────────────────────────────────
# Format:  <folder-under-inbox>|<project-tag>|<comma-separated-tags>
CORPORA=(
  "SWINDON|retail|pwc,swindon,sap-retail,broadvision,coe,1999"
  "Katz|retail|pwc,katz,scm,rfp,2003"
  "Other Retek Decks|retail|retek,rms,rib,rdm,2003-2005"
  "BV Nuggets|retail|broadvision,pwc,lessons-learned,1999-2000"
  "EBiz Def Des Dev|retail|pwc,methodology,web-implementation-guide,2000"
  "BP|retail|consulting-reference,pwc,mh,petsmart,finance,1997-1999"
)

# ── Header ───────────────────────────────────────────────────────────────
log() { echo "$*" | tee -a "$LOG"; }

{
  echo "==============================================="
  echo "Batch intake run: $TS"
  echo "Root:    $ROOT"
  echo "Inbox:   $INBOX"
  echo "Extract: $EXTRACT_ROOT"
  echo "Log:     $LOG"
  echo "Corpora: ${#CORPORA[@]}"
  echo "==============================================="
} | tee "$LOG"

# ── Pass 1: extract ──────────────────────────────────────────────────────
log ""
log "### Pass 1/3: extract binaries → markdown"

for spec in "${CORPORA[@]}"; do
  IFS='|' read -r folder project tags <<< "$spec"
  src="$INBOX/$folder"
  dst="$EXTRACT_ROOT/$folder"

  log ""
  log "── EXTRACT: $folder"

  if [[ ! -d "$src" ]]; then
    log "   [SKIP] Not found: $src"
    continue
  fi

  if python3 "$ENGINE" extract "$src" --target "$dst" --execute >> "$LOG" 2>&1; then
    log "   [OK]   extract complete: $folder"
  else
    log "   [WARN] extract exited non-zero for $folder — continuing"
  fi
done

# ── Pass 2: ingest every extracted .md ───────────────────────────────────
log ""
log "### Pass 2/3: ingest extracted markdown → Brain raw-intake notes"

total_ok=0
total_fail=0
for spec in "${CORPORA[@]}"; do
  IFS='|' read -r folder project tags <<< "$spec"
  extract_dir="$EXTRACT_ROOT/$folder"

  log ""
  log "── INGEST: $folder  (project=$project tags=$tags)"

  if [[ ! -d "$extract_dir" ]]; then
    log "   [SKIP] No extract dir for $folder"
    continue
  fi

  count=0
  fail=0
  while IFS= read -r -d '' md; do
    if python3 "$ENGINE" ingest "$md" --project "$project" --tags "$tags" >> "$LOG" 2>&1; then
      count=$((count+1))
    else
      fail=$((fail+1))
      log "   [WARN] ingest failed: $md"
    fi
  done < <(find "$extract_dir" -type f -name "*.md" ! -name ".*" -print0)

  log "   [OK]   ingest complete: $folder  OK=$count FAIL=$fail"
  total_ok=$((total_ok+count))
  total_fail=$((total_fail+fail))
done

# ── Pass 3: registry build ───────────────────────────────────────────────
log ""
log "### Pass 3/3: rebuild registry"

if python3 "$ENGINE" registry build >> "$LOG" 2>&1; then
  log "   [OK]   registry rebuild complete"
else
  log "   [WARN] registry build exited non-zero"
fi

# ── Summary ──────────────────────────────────────────────────────────────
{
  echo ""
  echo "==============================================="
  echo "Done:    $(date +%Y%m%d-%H%M%S)"
  echo "Intakes: OK=$total_ok  FAIL=$total_fail"
  echo "Log:     $LOG"
  echo "==============================================="
} | tee -a "$LOG"
