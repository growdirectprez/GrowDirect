# GrowDirect LLC — Confidential & Proprietary
# Copyright (c) 2026 GrowDirect LLC. All rights reserved.
"""Content Engine CLI — intake, deduplicate, flatten, index, triage, ingest.

Reusable across GrowDirect projects. Two layers:

  Filesystem layer (no AI needed):
    scan, dupes, index, flatten, clean

  Knowledge layer (designed for Cowork sessions):
    triage   — read files, generate content previews for session to classify
    ingest   — create Brain raw-intake notes from files
    registry — build/query the Brain knowledge registry

Usage:
    python3 content-engine/engine.py scan Cove/docs
    python3 content-engine/engine.py dupes Cove/docs
    python3 content-engine/engine.py triage Cove/docs --batch 20
    python3 content-engine/engine.py ingest Cove/docs/archive/some-file.md
    python3 content-engine/engine.py registry build
    python3 content-engine/engine.py registry check "founding documents"
"""
import click
import hashlib
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Optional

# ── Helpers ──────────────────────────────────────────────────────────────

SKIP_DIRS = {".git", "__pycache__", "node_modules", ".DS_Store", ".venv", "venv"}
SKIP_FILES = {".DS_Store", "Thumbs.db"}

# Brain paths — relative to GrowDirect root
BRAIN_ROOT = "Brain"
BRAIN_WIKI = "Brain/wiki"
BRAIN_PROJECTS = "Brain/projects"
BRAIN_RAW_INBOX = "Brain/raw/inbox"
BRAIN_REGISTRY = "Brain/REGISTRY.json"


def _find_growdirect_root(start: Path) -> Optional[Path]:
    """Walk up from start to find the GrowDirect root (has CLAUDE.md + Brain/)."""
    current = start.resolve()
    for _ in range(10):
        if (current / "CLAUDE.md").exists() and (current / "Brain").is_dir():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


def _sha256(path: Path) -> str:
    """Compute SHA-256 of a file. Returns empty string on read error."""
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except (OSError, PermissionError):
        return ""


def _scan_tree(root: Path) -> list[dict]:
    """Walk a directory tree and collect file metadata."""
    entries = []
    for item in sorted(root.rglob("*")):
        if item.is_dir():
            continue
        if item.name in SKIP_FILES:
            continue
        if any(part in SKIP_DIRS for part in item.parts):
            continue

        rel = item.relative_to(root)
        stat = item.stat()
        entries.append({
            "path": str(rel),
            "name": item.name,
            "stem": item.stem,
            "ext": item.suffix.lower(),
            "size": stat.st_size,
            "mtime": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
            "depth": len(rel.parts),
            "sha256": _sha256(item),
        })
    return entries


def _stem_key(name: str) -> str:
    """Normalize a filename stem for fuzzy grouping.

    Strips common suffixes like -Verbatim, -ocr, _v2, _copy, (1) etc.
    so that variant files cluster together.
    """
    s = Path(name).stem
    # Strip known variant suffixes
    s = re.sub(r"[-_](?:Verbatim|verbatim|ocr|OCR|copy|Copy|COPY)", "", s)
    # Strip version numbers like _v2, -v3
    s = re.sub(r"[-_]v\d+$", "", s)
    # Strip numbered copies like (1), (2)
    s = re.sub(r"\s*\(\d+\)$", "", s)
    # Lowercase and strip trailing hyphens/underscores
    return s.lower().strip("-_")


def _group_by_hash(entries: list[dict]) -> dict[str, list[dict]]:
    """Group files with identical content (same SHA-256)."""
    by_hash = defaultdict(list)
    for e in entries:
        if e["sha256"]:
            by_hash[e["sha256"]].append(e)
    return {h: files for h, files in by_hash.items() if len(files) > 1}


def _group_by_stem(entries: list[dict]) -> dict[str, list[dict]]:
    """Group files with similar names (variants like -ocr, -Verbatim)."""
    by_stem = defaultdict(list)
    for e in entries:
        key = _stem_key(e["name"])
        by_stem[key].append(e)
    return {s: files for s, files in by_stem.items() if len(files) > 1}


def _flatten_target(entry: dict, seen: set[str]) -> str:
    """Compute a flat target filename, handling collisions."""
    name = entry["name"]
    if name not in seen:
        seen.add(name)
        return name
    # Collision — prefix with parent directory
    parts = Path(entry["path"]).parts
    if len(parts) >= 2:
        prefix = parts[-2]
        candidate = f"{prefix}--{name}"
    else:
        candidate = name
    counter = 1
    base = candidate
    while candidate in seen:
        stem = Path(base).stem
        ext = Path(base).suffix
        candidate = f"{stem}--{counter}{ext}"
        counter += 1
    seen.add(candidate)
    return candidate


# ── Extract helpers (binary → markdown) ──────────────────────────────

EXTRACT_DEFAULT_EXTS = ("doc", "docx", "ppt", "pptx", "xls", "xlsx", "pdf")
EXTRACT_TMP_PATTERNS = ("~$", ".tmp", ".old")

def _is_tmp_file(path: Path) -> bool:
    """Match Office temp artifacts."""
    name = path.name
    if name.startswith("~$"):
        return True
    if path.suffix.lower() in (".tmp", ".old"):
        return True
    return False


def _extract_file(source: Path, target: Path) -> dict:
    """Convert a single binary file to markdown.

    Returns a manifest entry. Writes the markdown to target on success.
    Raises only for I/O problems on the source path itself.

    Attempts, in order:
      1. markitdown (primary)
      2. textutil (macOS .doc fallback)
      3. pdftotext (.pdf fallback)
    Otherwise records status='skipped'.
    """
    if not source.exists():
        raise FileNotFoundError(source)

    ext = source.suffix.lower().lstrip(".")
    entry = {
        "source_path": str(source),
        "source_sha256": _sha256(source),
        "target_path": str(target),
        "method": None,
        "status": "failed",
        "error": None,
        "extracted_at": datetime.now(timezone.utc).isoformat(),
    }

    # Short-circuit: skip unsupported extensions before attempting any conversion
    if ext not in EXTRACT_DEFAULT_EXTS:
        entry["status"] = "skipped"
        entry["method"] = "skip"
        entry["error"] = f"unsupported extension: .{ext}"
        return entry

    target.parent.mkdir(parents=True, exist_ok=True)

    # Primary: markitdown
    try:
        from markitdown import MarkItDown
        md = MarkItDown()
        result = md.convert(str(source))
        content = result.text_content or ""
        if content.strip():
            target.write_text(content, encoding="utf-8")
            entry["method"] = "markitdown"
            entry["status"] = "ok"
            return entry
    except Exception as e:  # noqa: BLE001
        entry["error"] = f"markitdown: {type(e).__name__}: {e}"

    # Fallback for .doc — macOS textutil
    if ext == "doc":
        try:
            import subprocess
            txt = subprocess.check_output(
                ["textutil", "-convert", "txt", "-stdout", str(source)],
                stderr=subprocess.DEVNULL,
            ).decode("utf-8", errors="replace")
            if txt.strip():
                target.write_text(txt, encoding="utf-8")
                entry["method"] = "textutil"
                entry["status"] = "ok"
                entry["error"] = None
                return entry
        except Exception as e:  # noqa: BLE001
            entry["error"] = f"{entry['error']} | textutil: {type(e).__name__}: {e}"

    # Fallback for .pdf — pdftotext
    if ext == "pdf":
        try:
            import subprocess, shutil as sh
            if sh.which("pdftotext"):
                txt = subprocess.check_output(
                    ["pdftotext", str(source), "-"],
                    stderr=subprocess.DEVNULL,
                ).decode("utf-8", errors="replace")
                if txt.strip():
                    target.write_text(txt, encoding="utf-8")
                    entry["method"] = "pdftotext"
                    entry["status"] = "ok"
                    entry["error"] = None
                    return entry
        except Exception as e:  # noqa: BLE001
            entry["error"] = f"{entry['error']} | pdftotext: {type(e).__name__}: {e}"

    # All attempts failed for a supported extension
    return entry


# ── CLI ──────────────────────────────────────────────────────────────────

@click.group()
def cli():
    """Content Engine — intake, deduplicate, flatten, index."""
    pass


@cli.command()
@click.argument("directory", type=click.Path(exists=True, file_okay=False))
@click.option("--json-out", type=click.Path(), help="Write scan results to JSON file")
def scan(directory: str, json_out: str | None):
    """Scan a directory tree and report file inventory."""
    root = Path(directory).resolve()
    click.echo(f"Scanning {root} ...")
    entries = _scan_tree(root)

    # Stats
    ext_counts = defaultdict(int)
    total_size = 0
    max_depth = 0
    for e in entries:
        ext_counts[e["ext"] or "(no ext)"] += 1
        total_size += e["size"]
        max_depth = max(max_depth, e["depth"])

    click.echo(f"\n{'─' * 50}")
    click.echo(f"  Files:      {len(entries):,}")
    click.echo(f"  Total size: {total_size / 1_048_576:.1f} MB")
    click.echo(f"  Max depth:  {max_depth} levels")
    click.echo(f"\n  By extension:")
    for ext, count in sorted(ext_counts.items(), key=lambda x: -x[1]):
        click.echo(f"    {ext:12s} {count:>5}")

    if json_out:
        out = Path(json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(entries, indent=2))
        click.echo(f"\n  Wrote scan data to {out}")


@cli.command()
@click.argument("directory", type=click.Path(exists=True, file_okay=False))
@click.option("--report", type=click.Path(), help="Write dupes report to markdown file")
def dupes(directory: str, report: str | None):
    """Find duplicate and near-duplicate files."""
    root = Path(directory).resolve()
    click.echo(f"Scanning {root} for duplicates ...")
    entries = _scan_tree(root)

    # Exact duplicates (same hash)
    hash_groups = _group_by_hash(entries)
    # Name variants (similar stems)
    stem_groups = _group_by_stem(entries)

    # Filter stem groups to only those with different hashes (not already caught as exact)
    near_dupes = {}
    for stem, files in stem_groups.items():
        hashes = {f["sha256"] for f in files if f["sha256"]}
        if len(hashes) > 1:  # different content, similar name
            near_dupes[stem] = files

    exact_count = sum(len(v) for v in hash_groups.values())
    wasted = sum(
        sum(f["size"] for f in files[1:])  # all but one copy
        for files in hash_groups.values()
    )

    click.echo(f"\n{'─' * 50}")
    click.echo(f"  Exact duplicate groups:  {len(hash_groups)}")
    click.echo(f"  Exact duplicate files:   {exact_count}")
    click.echo(f"  Wasted space:            {wasted / 1_048_576:.1f} MB")
    click.echo(f"  Near-duplicate groups:   {len(near_dupes)} (same stem, different content)")

    # Show top groups
    if hash_groups:
        click.echo(f"\n  Top exact duplicate groups:")
        sorted_groups = sorted(hash_groups.values(), key=lambda g: -g[0]["size"] * len(g))
        for group in sorted_groups[:10]:
            click.echo(f"\n    [{group[0]['size']:,} bytes × {len(group)} copies]")
            for f in group:
                click.echo(f"      {f['path']}")

    if near_dupes:
        click.echo(f"\n  Near-duplicate groups (variants):")
        for stem, files in sorted(near_dupes.items())[:15]:
            click.echo(f"\n    stem: {stem}")
            for f in files:
                click.echo(f"      {f['path']} ({f['size']:,} bytes)")

    if report:
        out = Path(report)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w") as fp:
            fp.write(f"# Duplicate Report — {root.name}\n\n")
            fp.write(f"Generated: {datetime.now(timezone.utc).isoformat()}\n\n")
            fp.write(f"## Summary\n\n")
            fp.write(f"- Exact duplicate groups: {len(hash_groups)}\n")
            fp.write(f"- Exact duplicate files: {exact_count}\n")
            fp.write(f"- Wasted space: {wasted / 1_048_576:.1f} MB\n")
            fp.write(f"- Near-duplicate groups: {len(near_dupes)}\n\n")

            if hash_groups:
                fp.write(f"## Exact Duplicates\n\n")
                for i, (h, files) in enumerate(
                    sorted(hash_groups.items(), key=lambda x: -x[1][0]["size"] * len(x[1])), 1
                ):
                    fp.write(f"### Group {i} — {files[0]['size']:,} bytes × {len(files)}\n\n")
                    fp.write(f"Hash: `{h[:16]}...`\n\n")
                    for f in files:
                        fp.write(f"- `{f['path']}`\n")
                    fp.write("\n")

            if near_dupes:
                fp.write(f"## Near-Duplicates (Name Variants)\n\n")
                for stem, files in sorted(near_dupes.items()):
                    fp.write(f"### {stem}\n\n")
                    for f in files:
                        fp.write(f"- `{f['path']}` ({f['size']:,} bytes, hash: `{f['sha256'][:12]}...`)\n")
                    fp.write("\n")

        click.echo(f"\n  Wrote report to {out}")


@cli.command()
@click.argument("directory", type=click.Path(exists=True, file_okay=False))
@click.option("--output", "-o", type=click.Path(), default=None,
              help="Output path for manifest (default: <dir>/MANIFEST.json)")
@click.option("--format", "fmt", type=click.Choice(["json", "md"]), default="json",
              help="Output format")
def index(directory: str, output: str | None, fmt: str):
    """Generate a flat manifest/index of all files."""
    root = Path(directory).resolve()
    click.echo(f"Indexing {root} ...")
    entries = _scan_tree(root)

    manifest = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "file_count": len(entries),
        "total_bytes": sum(e["size"] for e in entries),
        "files": entries,
    }

    out_path = Path(output) if output else root / f"MANIFEST.{fmt}"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if fmt == "json":
        out_path.write_text(json.dumps(manifest, indent=2))
    else:
        with open(out_path, "w") as fp:
            fp.write(f"# File Index — {root.name}\n\n")
            fp.write(f"Generated: {manifest['generated']}\n")
            fp.write(f"Files: {manifest['file_count']:,}\n")
            fp.write(f"Total size: {manifest['total_bytes'] / 1_048_576:.1f} MB\n\n")

            # Group by top-level directory
            by_dir = defaultdict(list)
            for e in entries:
                top = Path(e["path"]).parts[0] if len(Path(e["path"]).parts) > 1 else "."
                by_dir[top].append(e)

            for dirname, files in sorted(by_dir.items()):
                fp.write(f"## {dirname}/ ({len(files)} files)\n\n")
                for f in sorted(files, key=lambda x: x["path"]):
                    size_kb = f["size"] / 1024
                    fp.write(f"- `{f['path']}` — {size_kb:.0f} KB\n")
                fp.write("\n")

    click.echo(f"  Wrote {fmt.upper()} manifest to {out_path}")
    click.echo(f"  {manifest['file_count']:,} files, {manifest['total_bytes'] / 1_048_576:.1f} MB")


@cli.command()
@click.argument("directory", type=click.Path(exists=True, file_okay=False))
@click.option("--target", "-t", type=click.Path(), default=None,
              help="Target directory for flat structure (default: <dir>/../<dir>-flat)")
@click.option("--dry-run/--execute", default=True,
              help="Preview moves without executing (default: dry-run)")
@click.option("--skip-dupes/--keep-dupes", default=True,
              help="Skip exact duplicate files (default: skip)")
def flatten(directory: str, target: str | None, dry_run: bool, skip_dupes: bool):
    """Flatten directory tree into a single-level structure.

    By default runs in dry-run mode — prints proposed moves without
    touching any files. Pass --execute to actually move files.
    """
    root = Path(directory).resolve()
    click.echo(f"{'[DRY RUN] ' if dry_run else ''}Flattening {root} ...")
    entries = _scan_tree(root)

    target_dir = Path(target).resolve() if target else root.parent / f"{root.name}-flat"

    # If skipping dupes, identify which files to keep (first occurrence per hash)
    keep = set()
    skip_paths = set()
    if skip_dupes:
        seen_hashes = {}
        for e in entries:
            h = e["sha256"]
            if not h:
                keep.add(e["path"])
                continue
            if h in seen_hashes:
                skip_paths.add(e["path"])
            else:
                seen_hashes[h] = e["path"]
                keep.add(e["path"])
    else:
        keep = {e["path"] for e in entries}

    # Plan moves
    seen_names: set[str] = set()
    moves = []
    for e in entries:
        if e["path"] in skip_paths:
            continue
        flat_name = _flatten_target(e, seen_names)
        moves.append({
            "source": e["path"],
            "target": flat_name,
            "size": e["size"],
        })

    click.echo(f"\n{'─' * 50}")
    click.echo(f"  Files to move:  {len(moves):,}")
    click.echo(f"  Files skipped:  {len(skip_paths):,} (exact duplicates)")
    click.echo(f"  Target dir:     {target_dir}")

    if dry_run:
        click.echo(f"\n  Proposed moves (first 30):\n")
        for m in moves[:30]:
            if m["source"] != m["target"]:
                click.echo(f"    {m['source']}")
                click.echo(f"      → {m['target']}")
            else:
                click.echo(f"    {m['source']} (unchanged)")

        if len(moves) > 30:
            click.echo(f"\n    ... and {len(moves) - 30} more")

        click.echo(f"\n  To execute: re-run with --execute")
        click.echo(f"  To keep dupes: add --keep-dupes")
    else:
        target_dir.mkdir(parents=True, exist_ok=True)
        import shutil
        moved = 0
        for m in moves:
            src = root / m["source"]
            dst = target_dir / m["target"]
            if src.exists():
                shutil.copy2(src, dst)
                moved += 1
        click.echo(f"\n  Copied {moved:,} files to {target_dir}")
        click.echo(f"  Original directory untouched — review and delete manually.")


@cli.command()
@click.argument("directory", type=click.Path(exists=True, file_okay=False))
@click.option("--dry-run/--execute", default=True,
              help="Preview deletions without executing (default: dry-run)")
def clean(directory: str, dry_run: bool):
    """Remove exact duplicates, web junk, empty placeholders, and consolidate diverged copies.

    Actions performed:
    1. Delete exact duplicate files (keeps the copy with the shortest path)
    2. Delete web archive artifacts (_files/ directories with thumbnails, js, css)
    3. Delete empty placeholder files (≤ 1 byte .md files)
    4. Consolidate diverged copies: when the same document exists in two
       directories with different content, keep the larger (more complete) version

    By default runs in dry-run mode. Pass --execute to actually delete files.
    """
    root = Path(directory).resolve()
    click.echo(f"{'[DRY RUN] ' if dry_run else ''}Cleaning {root} ...")
    entries = _scan_tree(root)

    to_delete: list[dict] = []  # {"path": str, "reason": str, "size": int}

    # ── 1. Exact duplicates: keep most canonical path ──────────────────
    hash_groups = _group_by_hash(entries)
    for h, files in hash_groups.items():
        # Prefer paths containing "originals/" as canonical, then shortest path
        def _canonical_rank(f):
            has_originals = "originals/" in f["path"]
            return (0 if has_originals else 1, len(f["path"]), f["path"])
        ranked = sorted(files, key=_canonical_rank)
        keeper = ranked[0]
        for dupe in ranked[1:]:
            to_delete.append({
                "path": dupe["path"],
                "reason": f"exact dupe of {keeper['path']}",
                "size": dupe["size"],
            })

    # ── 2. Web archive junk (_files/ directories) ───────────────────────
    for e in entries:
        if "_files/" in e["path"] and e["ext"] in ("", ".js", ".css", ".ico"):
            # Don't double-count if already caught as exact dupe
            if not any(d["path"] == e["path"] for d in to_delete):
                to_delete.append({
                    "path": e["path"],
                    "reason": "web archive artifact",
                    "size": e["size"],
                })

    # ── 3. Empty placeholders (≤ 1 byte .md files) ──────────────────────
    for e in entries:
        if e["ext"] == ".md" and e["size"] <= 1:
            if not any(d["path"] == e["path"] for d in to_delete):
                to_delete.append({
                    "path": e["path"],
                    "reason": "empty placeholder",
                    "size": e["size"],
                })

    # ── 4. Diverged copies (same stem in different dirs, diff content) ──
    #    Keep the larger file. Only applies to .md and .html files where
    #    the name is identical (not just stem-similar like PDF+md pairs).
    by_name: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        if e["ext"] in (".md", ".html"):
            by_name[e["name"].lower()].append(e)

    # Directories that represent intentionally different document types
    SKIP_DIR_PAIRS = {frozenset({"plans", "specs"}), frozenset({"superpowers/plans", "superpowers/specs"})}

    for name, files in by_name.items():
        if len(files) < 2:
            continue
        # Only consider files in DIFFERENT directories
        dirs = {str(Path(f["path"]).parent) for f in files}
        if len(dirs) < 2:
            continue
        # Skip intentional document-type pairs (plans vs specs)
        if any(frozenset(dirs) == pair for pair in SKIP_DIR_PAIRS):
            continue
        # All must have different hashes (otherwise caught by exact dupe)
        hashes = {f["sha256"] for f in files}
        if len(hashes) == 1:
            continue
        # Keep the largest (most complete), delete the rest
        ranked = sorted(files, key=lambda f: -f["size"])
        keeper = ranked[0]
        for lesser in ranked[1:]:
            if not any(d["path"] == lesser["path"] for d in to_delete):
                to_delete.append({
                    "path": lesser["path"],
                    "reason": f"diverged copy of {keeper['path']} ({keeper['size']:,} > {lesser['size']:,} bytes)",
                    "size": lesser["size"],
                })

    # ── Summary ─────────────────────────────────────────────────────────
    by_reason = defaultdict(list)
    for d in to_delete:
        by_reason[d["reason"].split(" of ")[0].split(" (")[0]].append(d)

    total_saved = sum(d["size"] for d in to_delete)
    click.echo(f"\n{'─' * 60}")
    click.echo(f"  Files to delete: {len(to_delete):,}")
    click.echo(f"  Space freed:     {total_saved / 1_048_576:.1f} MB")
    click.echo(f"\n  By reason:")
    for reason, items in sorted(by_reason.items()):
        click.echo(f"    {reason:25s} {len(items):>4} files")

    click.echo(f"\n  Deletions:")
    for d in sorted(to_delete, key=lambda x: x["path"]):
        click.echo(f"    ✗ {d['path']}")
        click.echo(f"      {d['reason']}")

    if dry_run:
        click.echo(f"\n  To execute: re-run with --execute")
    else:
        deleted = 0
        errors = 0
        for d in to_delete:
            target = root / d["path"]
            try:
                target.unlink()
                deleted += 1
            except OSError as e:
                click.echo(f"    ERROR: {d['path']}: {e}")
                errors += 1

        # Clean up empty directories left behind
        empty_dirs_removed = 0
        for dirpath in sorted(root.rglob("*"), reverse=True):
            if dirpath.is_dir() and not any(dirpath.iterdir()):
                dirpath.rmdir()
                empty_dirs_removed += 1

        click.echo(f"\n  Deleted {deleted:,} files ({errors} errors)")
        click.echo(f"  Removed {empty_dirs_removed} empty directories")


@cli.command()
@click.argument("directory", type=click.Path(exists=True, file_okay=False))
@click.option("--target", "-t", type=click.Path(), required=True,
              help="Output directory for extracted markdown")
@click.option("--ext", default=",".join(EXTRACT_DEFAULT_EXTS),
              help=f"Comma-separated extensions to process (default: {','.join(EXTRACT_DEFAULT_EXTS)})")
@click.option("--maxdepth", type=int, default=None,
              help="Limit recursion depth (1 = top-level only)")
@click.option("--skip-tmp/--keep-tmp", default=True,
              help="Skip Office temp artifacts (~$*, *.tmp, *.old). Default: skip.")
@click.option("--dry-run/--execute", default=True,
              help="Preview extractions without writing (default: dry-run)")
def extract(directory: str, target: str, ext: str, maxdepth: int | None,
            skip_tmp: bool, dry_run: bool):
    """Convert Office + PDF files to markdown via markitdown.

    Walks DIRECTORY, filters by extension, writes one .md per source file
    to TARGET preserving the source tree. Writes a manifest file
    .extract-manifest.json and .extract-failures.json in TARGET.

    Default is dry-run. Pass --execute to write output.
    """
    root = Path(directory).resolve()
    target_root = Path(target).resolve()
    exts = {e.strip().lstrip(".").lower() for e in ext.split(",") if e.strip()}

    click.echo(f"{'[DRY RUN] ' if dry_run else ''}Extracting from {root}")
    click.echo(f"  Target:    {target_root}")
    click.echo(f"  Exts:      {sorted(exts)}")
    click.echo(f"  Maxdepth:  {maxdepth or 'unlimited'}")

    candidates: list[Path] = []
    for item in sorted(root.rglob("*")):
        if item.is_dir():
            continue
        if item.name in SKIP_FILES:
            continue
        if any(part in SKIP_DIRS for part in item.parts):
            continue
        if item.suffix.lower().lstrip(".") not in exts:
            continue
        if skip_tmp and _is_tmp_file(item):
            continue
        if maxdepth is not None:
            rel = item.relative_to(root)
            if len(rel.parts) > maxdepth:
                continue
        candidates.append(item)

    click.echo(f"  Files:     {len(candidates)}")

    if dry_run:
        click.echo("\n  Would extract (first 30):")
        for c in candidates[:30]:
            rel = c.relative_to(root)
            click.echo(f"    {rel}")
        if len(candidates) > 30:
            click.echo(f"    ... and {len(candidates) - 30} more")
        click.echo("\n  To execute: re-run with --execute")
        return

    target_root.mkdir(parents=True, exist_ok=True)
    manifest: list[dict] = []
    failures: list[dict] = []
    ok = failed = skipped = 0
    for c in candidates:
        rel = c.relative_to(root)
        dest = target_root / (str(rel) + ".md")
        try:
            entry = _extract_file(c, dest)
        except Exception as e:  # noqa: BLE001
            entry = {
                "source_path": str(c),
                "source_sha256": "",
                "target_path": str(dest),
                "method": None,
                "status": "failed",
                "error": f"{type(e).__name__}: {e}",
                "extracted_at": datetime.now(timezone.utc).isoformat(),
            }
        manifest.append(entry)
        if entry["status"] == "ok":
            ok += 1
        elif entry["status"] == "skipped":
            skipped += 1
        else:
            failed += 1
            failures.append(entry)

    (target_root / ".extract-manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False)
    )
    if failures:
        (target_root / ".extract-failures.json").write_text(
            json.dumps(failures, indent=2, ensure_ascii=False)
        )

    click.echo(f"\n  OK:       {ok}")
    click.echo(f"  Failed:   {failed}")
    click.echo(f"  Skipped:  {skipped}")
    click.echo(f"  Manifest: {target_root / '.extract-manifest.json'}")
    if failures:
        click.echo(f"  Failures: {target_root / '.extract-failures.json'}")


# ── Knowledge Layer Commands ─────────────────────────────────────────────


def _preview_file(path: Path, max_lines: int = 30) -> str:
    """Read first N lines of a text file. Returns empty string for binary."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            lines = []
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                lines.append(line.rstrip())
            return "\n".join(lines)
    except (OSError, UnicodeDecodeError):
        return ""


def _load_registry(gd_root: Path) -> dict:
    """Load the Brain registry, or return empty structure."""
    reg_path = gd_root / BRAIN_REGISTRY
    if reg_path.exists():
        return json.loads(reg_path.read_text())
    return {"generated": None, "articles": [], "topics": {}}


@cli.command()
@click.argument("directory", type=click.Path(exists=True, file_okay=False))
@click.option("--batch", "-b", default=20, help="Number of files to triage per run")
@click.option("--ext", default=".md", help="File extension to triage (default: .md)")
@click.option("--output", "-o", type=click.Path(), default=None,
              help="Output path for triage manifest")
def triage(directory: str, batch: int, ext: str, output: str | None):
    """Generate a triage manifest with content previews for session review.

    Reads files, extracts previews, checks Brain registry for overlap,
    and outputs a structured manifest that a Cowork session can act on.
    The session (Claude) provides the intelligence — this command provides
    the structured input.
    """
    root = Path(directory).resolve()
    gd_root = _find_growdirect_root(root)
    registry = _load_registry(gd_root) if gd_root else {"topics": {}}

    click.echo(f"Triaging {root} (batch={batch}, ext={ext}) ...")

    # Collect eligible files, sorted by size desc (biggest = most content)
    candidates = []
    for item in sorted(root.rglob(f"*{ext}")):
        if item.is_dir():
            continue
        if any(part in SKIP_DIRS for part in item.parts):
            continue
        rel = str(item.relative_to(root))
        candidates.append({"abs": item, "rel": rel, "size": item.stat().st_size})

    candidates.sort(key=lambda c: -c["size"])
    batch_items = candidates[:batch]

    click.echo(f"  {len(candidates)} total {ext} files, triaging top {len(batch_items)}")

    # Build registry keyword set for overlap detection
    known_keywords = set()
    for topic, articles in registry.get("topics", {}).items():
        known_keywords.add(topic.lower())
        for a in articles:
            for kw in a.get("keywords", []):
                known_keywords.add(kw.lower())

    # Generate triage entries
    triage_items = []
    for item in batch_items:
        preview = _preview_file(item["abs"])
        # Extract likely keywords from filename
        stem_words = set(re.split(r"[-_]", Path(item["rel"]).stem.lower()))
        stem_words -= {"md", "the", "and", "of", "for", "in", "a", "to", "on"}

        # Check overlap with Brain
        overlap = stem_words & known_keywords
        brain_coverage = "covered" if len(overlap) >= 2 else "partial" if overlap else "unknown"

        triage_items.append({
            "path": item["rel"],
            "size": item["size"],
            "brain_coverage": brain_coverage,
            "overlapping_topics": sorted(overlap),
            "preview": preview[:2000],  # Cap preview length
        })

    manifest = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "source": str(root),
        "total_files": len(candidates),
        "batch_size": len(batch_items),
        "brain_registry_loaded": bool(registry.get("generated")),
        "items": triage_items,
    }

    out_path = Path(output) if output else root / "TRIAGE.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))

    # Summary
    coverage = defaultdict(int)
    for t in triage_items:
        coverage[t["brain_coverage"]] += 1

    click.echo(f"\n{'─' * 50}")
    click.echo(f"  Triage manifest:  {out_path}")
    click.echo(f"  Files triaged:    {len(triage_items)}")
    click.echo(f"  Brain coverage:")
    for status, count in sorted(coverage.items()):
        click.echo(f"    {status:12s} {count:>4}")
    click.echo(f"\n  Next: open TRIAGE.json in a Cowork session to classify each file.")


@cli.command()
@click.argument("filepath", type=click.Path(exists=True, dir_okay=False))
@click.option("--project", "-p", default=None, help="Project tag (canary, etc.)")
@click.option("--tags", "-t", default=None, help="Comma-separated tags")
def ingest(filepath: str, project: str | None, tags: str | None):
    """Create a Brain raw-intake note from a file.

    Reads the file, extracts content, and creates a properly formatted
    note in Brain/raw/inbox/ following the raw-intake template.
    The note is created with status=unprocessed so a session can later
    compile it into a wiki article.
    """
    source = Path(filepath).resolve()
    gd_root = _find_growdirect_root(source)
    if not gd_root:
        click.echo("ERROR: Could not find GrowDirect root (need CLAUDE.md + Brain/)")
        raise SystemExit(1)

    inbox = gd_root / BRAIN_RAW_INBOX
    inbox.mkdir(parents=True, exist_ok=True)

    # Read content
    content = _preview_file(source, max_lines=500)
    if not content:
        click.echo(f"ERROR: Could not read {source}")
        raise SystemExit(1)

    # Generate note filename from source
    rel_to_gd = source.relative_to(gd_root) if source.is_relative_to(gd_root) else source
    note_name = source.stem.lower()
    # Sanitize for filesystem
    note_name = re.sub(r"[^a-z0-9_-]", "-", note_name)
    note_path = inbox / f"{note_name}.md"

    # Avoid overwriting
    if note_path.exists():
        counter = 1
        while note_path.exists():
            note_path = inbox / f"{note_name}-{counter}.md"
            counter += 1

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    tag_list = [t.strip() for t in tags.split(",")] if tags else []
    if project:
        tag_list.insert(0, project)

    frontmatter = f"""---
date: {today}
type: raw
source: {rel_to_gd}
tags: [{', '.join(tag_list)}]
project: {project or ''}
status: unprocessed
---"""

    note_content = f"""{frontmatter}

# {source.stem}

## Source
File: `{rel_to_gd}`
Size: {source.stat().st_size:,} bytes

## Raw content
{content}

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
"""

    note_path.write_text(note_content)
    click.echo(f"  Created: {note_path.relative_to(gd_root)}")
    click.echo(f"  Source:  {rel_to_gd}")
    click.echo(f"  Status:  unprocessed")
    click.echo(f"\n  Next: process this note in a Cowork session —")
    click.echo(f"  fill in Key Takeaways, link to wiki articles, then")
    click.echo(f"  update status to 'processed' or 'compiled'.")


@cli.group()
def registry():
    """Build and query the Brain knowledge registry."""
    pass


@registry.command("build")
def registry_build():
    """Scan Brain wiki articles and build REGISTRY.json.

    The registry maps topics and keywords to existing wiki articles,
    so sessions can check what Brain already knows before creating
    new content.
    """
    gd_root = _find_growdirect_root(Path.cwd())
    if not gd_root:
        click.echo("ERROR: Run from within GrowDirect (need CLAUDE.md + Brain/)")
        raise SystemExit(1)

    wiki_dir = gd_root / BRAIN_WIKI
    projects_dir = gd_root / BRAIN_PROJECTS

    articles = []

    # Scan wiki articles
    for md in sorted(wiki_dir.glob("*.md")) if wiki_dir.exists() else []:
        content = md.read_text(encoding="utf-8", errors="replace")

        # Extract frontmatter tags
        tags = []
        fm_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if fm_match:
            fm = fm_match.group(1)
            tag_match = re.search(r"tags:\s*\[([^\]]*)\]", fm)
            if tag_match:
                tags = [t.strip() for t in tag_match.group(1).split(",") if t.strip()]

        # Extract title and first paragraph (skip frontmatter)
        body = re.sub(r"^---\n.*?\n---\n*", "", content, count=1, flags=re.DOTALL)
        lines = body.split("\n")
        title = ""
        summary = ""
        for line in lines:
            if line.startswith("# ") and not title:
                title = line[2:].strip()
            elif title and line.strip() and not line.startswith("#") and not line.startswith("|"):
                summary = line.strip()
                break

        # Keywords: tags + filename + title + section headings
        keywords = set(tags)
        for word in re.split(r"[-_\s]+", md.stem.lower()):
            if len(word) > 2:
                keywords.add(word)
        if title:
            for word in re.split(r"[-_\s,()]+", title.lower()):
                if len(word) > 3:
                    keywords.add(word)
        # Also pull from ## headings in the body
        for heading in re.findall(r"^#{1,3}\s+(.+)$", body, re.MULTILINE):
            for word in re.split(r"[-_\s,()]+", heading.lower()):
                if len(word) > 3:
                    keywords.add(word)

        articles.append({
            "path": str(md.relative_to(gd_root)),
            "title": title,
            "summary": summary[:200],
            "tags": tags,
            "keywords": sorted(keywords),
            "type": "wiki",
        })

    # Scan project MOCs
    for md in sorted(projects_dir.glob("*.md")) if projects_dir.exists() else []:
        content = md.read_text(encoding="utf-8", errors="replace")
        lines = content.split("\n")
        title = md.stem
        summary = ""
        for line in lines:
            if line.startswith("# "):
                title = line[2:].strip()
            elif line.strip() and not line.startswith("#") and not line.startswith("---") and not line.startswith("|") and not line.startswith("type:"):
                summary = line.strip()
                break

        articles.append({
            "path": str(md.relative_to(gd_root)),
            "title": title,
            "summary": summary[:200],
            "tags": [],
            "keywords": sorted({w for w in re.split(r"[-_\s]+", md.stem.lower()) if len(w) > 2}),
            "type": "project-moc",
        })

    # Build topic index (keyword → articles that cover it)
    topics: dict[str, list[dict]] = defaultdict(list)
    for a in articles:
        for kw in a["keywords"]:
            topics[kw].append({"path": a["path"], "title": a["title"]})

    registry_data = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "article_count": len(articles),
        "topic_count": len(topics),
        "articles": articles,
        "topics": dict(sorted(topics.items())),
    }

    reg_path = gd_root / BRAIN_REGISTRY
    reg_path.write_text(json.dumps(registry_data, indent=2, ensure_ascii=False))

    click.echo(f"  Registry built: {reg_path.relative_to(gd_root)}")
    click.echo(f"  Articles indexed:  {len(articles)}")
    click.echo(f"  Topics indexed:    {len(topics)}")
    click.echo(f"\n  Articles:")
    for a in articles:
        click.echo(f"    [{a['type']:12s}] {a['path']}")
        click.echo(f"                  {a['title']}")


@registry.command("check")
@click.argument("query")
def registry_check(query: str):
    """Check if Brain already covers a topic.

    Searches the registry for matching keywords and shows which
    wiki articles are relevant. Use this BEFORE creating new content.
    """
    gd_root = _find_growdirect_root(Path.cwd())
    if not gd_root:
        click.echo("ERROR: Run from within GrowDirect (need CLAUDE.md + Brain/)")
        raise SystemExit(1)

    reg = _load_registry(gd_root)
    if not reg.get("generated"):
        click.echo("  Registry not built yet. Run: engine.py registry build")
        raise SystemExit(1)

    # Tokenize query
    query_words = {w.lower() for w in re.split(r"[-_\s]+", query) if len(w) > 2}
    topics = reg.get("topics", {})

    # Find matching topics
    matches: dict[str, set] = defaultdict(set)  # article path → matched keywords
    for word in query_words:
        # Exact match
        if word in topics:
            for art in topics[word]:
                matches[art["path"]].add(word)
        # Partial match
        for topic_key, arts in topics.items():
            if word in topic_key or topic_key in word:
                for art in arts:
                    matches[art["path"]].add(topic_key)

    if not matches:
        click.echo(f"  No Brain coverage found for: {query}")
        click.echo(f"  This topic may need a new wiki article.")
        return

    # Rank by number of matching keywords
    ranked = sorted(matches.items(), key=lambda x: -len(x[1]))

    click.echo(f"  Brain coverage for: {query}\n")
    for path, keywords in ranked:
        # Find article details
        art = next((a for a in reg["articles"] if a["path"] == path), None)
        title = art["title"] if art else path
        click.echo(f"    {title}")
        click.echo(f"    └─ {path}")
        click.echo(f"       matched: {', '.join(sorted(keywords))}")
        click.echo()


# ── Lint ────────────────────────────────────────────────────────────────

# Required frontmatter fields on every wiki article. Values must parse as
# ISO-8601 dates (YYYY-MM-DD). Keep this list in sync with
# Brain/templates/wiki-article.md.
WIKI_REQUIRED_FIELDS = ("last-compiled", "needs-review")


def _parse_frontmatter(content: str) -> tuple[str, str, str] | None:
    """Split a markdown file into (open_fence, frontmatter_body, close_fence_plus_rest).

    Returns None if no frontmatter block is found.
    """
    m = re.match(r"^(---\n)(.*?)(\n---\n?)", content, re.DOTALL)
    if not m:
        return None
    return m.group(1), m.group(2), m.group(3)


def _git_committer_date(path: Path) -> str | None:
    """Return last commit date for path as YYYY-MM-DD, or None if not committed."""
    import subprocess
    try:
        out = subprocess.check_output(
            ["git", "log", "-1", "--format=%cs", "--", str(path)],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        return out or None
    except Exception:
        return None


def _backfill_date(path: Path) -> str:
    """Best date for a file: last commit date, else filesystem mtime."""
    import os
    d = _git_committer_date(path)
    if d:
        return d
    return datetime.fromtimestamp(os.path.getmtime(path)).date().isoformat()


def _add_days(iso_date: str, days: int) -> str:
    from datetime import date, timedelta
    y, m, d = (int(x) for x in iso_date.split("-"))
    return (date(y, m, d) + timedelta(days=days)).isoformat()


def _lint_wiki_file(path: Path, fix: bool) -> tuple[list[str], list[str]]:
    """Lint a single wiki markdown file.

    Returns (violations, fixes_applied). Each is a list of human-readable strings.
    """
    content = path.read_text(encoding="utf-8", errors="replace")
    parsed = _parse_frontmatter(content)
    if not parsed:
        return ([f"{path}: missing frontmatter block"], [])

    open_fence, fm, close_fence = parsed

    violations: list[str] = []
    fixes: list[str] = []
    new_fm = fm

    for field in WIKI_REQUIRED_FIELDS:
        if re.search(rf"^{re.escape(field)}:", new_fm, re.MULTILINE):
            continue
        if not fix:
            violations.append(f"{path}: missing '{field}'")
            continue
        # Compute default value
        if field == "last-compiled":
            value = _backfill_date(path)
        elif field == "needs-review":
            # Anchor off last-compiled if present, else backfill date
            lc_match = re.search(
                r"^last-compiled:\s*[\"']?(\d{4}-\d{2}-\d{2})",
                new_fm,
                re.MULTILINE,
            )
            anchor = lc_match.group(1) if lc_match else _backfill_date(path)
            value = _add_days(anchor, 14)
        else:  # pragma: no cover — future-proofing
            value = _backfill_date(path)
        new_fm = new_fm.rstrip("\n") + f"\n{field}: {value}"
        fixes.append(f"{path}: set '{field}: {value}'")

    if fix and new_fm != fm:
        new_content = open_fence + new_fm + close_fence + content[len(open_fence) + len(fm) + len(close_fence):]
        path.write_text(new_content, encoding="utf-8")

    return (violations, fixes)


@cli.command()
@click.argument("paths", nargs=-1, type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--fix", is_flag=True, help="Backfill missing frontmatter fields in place.")
@click.option("--all", "scan_all", is_flag=True, help="Lint every Brain/wiki/*.md file.")
def lint(paths: tuple[Path, ...], fix: bool, scan_all: bool):
    """Lint Brain wiki frontmatter. Flags articles missing required fields.

    Required fields: last-compiled, needs-review.

    Usage:
        engine.py lint --all                  # check every wiki article
        engine.py lint --all --fix            # backfill missing fields
        engine.py lint Brain/wiki/foo.md      # check a single file
        engine.py lint $(git diff --cached --name-only | grep Brain/wiki/)  # precommit

    Exit code: 0 if clean, 1 if violations found (in check mode).
    """
    gd_root = _find_growdirect_root(Path.cwd())
    if not gd_root:
        click.echo("ERROR: Run from within GrowDirect (need CLAUDE.md + Brain/)")
        raise SystemExit(2)

    if scan_all and paths:
        click.echo("ERROR: pass PATHS or --all, not both.")
        raise SystemExit(2)

    if scan_all:
        wiki_dir = gd_root / BRAIN_WIKI
        targets = sorted(wiki_dir.glob("*.md")) if wiki_dir.exists() else []
    elif paths:
        targets = [p.resolve() for p in paths if p.suffix == ".md"]
    else:
        click.echo("ERROR: pass file paths or --all.")
        raise SystemExit(2)

    # Only lint files under Brain/wiki
    wiki_prefix = (gd_root / BRAIN_WIKI).resolve()
    filtered = [t for t in targets if str(t.resolve()).startswith(str(wiki_prefix))]

    all_violations: list[str] = []
    all_fixes: list[str] = []
    for t in filtered:
        v, f = _lint_wiki_file(t, fix=fix)
        all_violations.extend(v)
        all_fixes.extend(f)

    if fix:
        click.echo(f"  Files checked: {len(filtered)}")
        click.echo(f"  Fixes applied: {len(all_fixes)}")
        for msg in all_fixes:
            click.echo(f"    + {msg}")
        if all_violations:
            click.echo(f"  Remaining violations: {len(all_violations)}")
            for msg in all_violations:
                click.echo(f"    - {msg}")
            raise SystemExit(1)
        return

    click.echo(f"  Files checked: {len(filtered)}")
    if not all_violations:
        click.echo("  Clean. All required frontmatter fields present.")
        return
    click.echo(f"  Violations: {len(all_violations)}")
    for msg in all_violations:
        click.echo(f"    - {msg}")
    click.echo("\n  Fix with: python3 content-engine/engine.py lint --all --fix")
    raise SystemExit(1)


# ── Weekly status ───────────────────────────────────────────────────

# ABCD weekly status reports live here. Friday-cadence: scaffold the file,
# auto-populate the inventory rails (closed dispatches, wiki adds, commits),
# fill the four boxes by hand. See Brain/status/weekly/_index.md.

BRAIN_STATUS_WEEKLY = "Brain/status/weekly"


def _iso_week_range(week_str: str | None) -> tuple[str, str, str]:
    """Resolve a YYYY-Www string to (week_label, monday_iso, sunday_iso).

    Pass None to use the current week. Week boundaries are ISO-8601:
    Monday is day 1, Sunday is day 7.
    """
    from datetime import date, timedelta

    if week_str is None:
        today = date.today()
        iso_year, iso_week, _ = today.isocalendar()
    else:
        m = re.match(r"^(\d{4})-W(\d{1,2})$", week_str)
        if not m:
            raise click.BadParameter(
                f"--week must be YYYY-Www (e.g. 2026-W18), got {week_str!r}"
            )
        iso_year = int(m.group(1))
        iso_week = int(m.group(2))

    # ISO week N starts on the Monday of that week. date.fromisocalendar
    # is the canonical resolver (Python 3.8+).
    monday = date.fromisocalendar(iso_year, iso_week, 1)
    sunday = monday + timedelta(days=6)
    label = f"{iso_year}-W{iso_week:02d}"
    return label, monday.isoformat(), sunday.isoformat()


def _git_log_lines(gd_root: Path, since: str, until: str, paths: list[str] | None = None) -> list[str]:
    """Run git log over a date range, return formatted lines.

    Returns empty list if git fails (e.g. not in a repo). Filters merge
    commits and one-line commits whose subject is purely formatting noise.
    """
    import subprocess

    cmd = [
        "git", "-C", str(gd_root),
        "log",
        f"--since={since}",
        f"--until={until} 23:59:59",
        "--no-merges",
        "--pretty=format:%h\t%s",
    ]
    if paths:
        cmd.append("--")
        cmd.extend(paths)

    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True)
    except Exception:
        return []

    lines = []
    for raw in out.strip().splitlines():
        if not raw.strip():
            continue
        if "\t" in raw:
            sha, subj = raw.split("\t", 1)
        else:
            sha, subj = raw[:7], raw[8:]
        # Skip pure noise — typo-only and whitespace-only commits.
        subj_lower = subj.lower().strip()
        if subj_lower in ("typo", "whitespace", "format", "formatting"):
            continue
        lines.append(f"- `{sha}` {subj}")
    return lines


def _git_changed_files(gd_root: Path, since: str, until: str, path_prefix: str) -> list[str]:
    """Files under path_prefix that changed in the given range. One bullet per file."""
    import subprocess

    try:
        out = subprocess.check_output(
            [
                "git", "-C", str(gd_root),
                "log",
                f"--since={since}",
                f"--until={until} 23:59:59",
                "--name-only",
                "--no-merges",
                "--pretty=format:",
                "--", path_prefix,
            ],
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except Exception:
        return []

    files = sorted({line.strip() for line in out.splitlines() if line.strip()})
    return [f"- [[{Path(f).stem}]] (`{f}`)" for f in files]


def _replace_section(content: str, heading: str, replacement: str) -> str:
    """Replace the body of a markdown section identified by its heading.

    Walks until the next heading at the same level and replaces the body.
    The heading itself is preserved. If the heading is not found, returns
    the content unchanged.
    """
    # Find the heading line. Must match exactly (case-sensitive).
    pattern = re.compile(
        rf"(^{re.escape(heading)}\s*\n)(.*?)(?=^#{{1,6}}\s|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    if not pattern.search(content):
        return content
    return pattern.sub(rf"\1{replacement}\n", content, count=1)


# ── HTML rendering for weekly status ────────────────────────────────

_HTML_STYLE = """
:root {
  color-scheme: light dark;
  --bg: #fafaf9; --fg: #1c1917; --muted: #57534e;
  --border: #e7e5e4; --card-bg: #ffffff; --rail-bg: #f5f5f4;
  --a-color: #059669; --b-color: #0284c7;
  --c-color: #d97706; --d-color: #7c3aed;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0c0a09; --fg: #fafaf9; --muted: #a8a29e;
    --border: #292524; --card-bg: #1c1917; --rail-bg: #292524;
  }
}
* { box-sizing: border-box; }
html, body { background: var(--bg); color: var(--fg); }
body {
  font-family: ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
  font-size: 16px; line-height: 1.55; margin: 0;
  padding: 2.5rem 1.5rem 4rem;
}
.container { max-width: 1100px; margin: 0 auto; }
header {
  margin-bottom: 2.5rem; padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--border);
}
header .meta {
  color: var(--muted); font-size: 0.8rem;
  letter-spacing: 0.08em; text-transform: uppercase;
  margin-bottom: 0.5rem;
}
header h1 {
  font-size: 2.5rem; font-weight: 700; margin: 0;
  letter-spacing: -0.02em;
}
header .subtitle {
  margin-top: 0.75rem; color: var(--muted); font-style: italic;
  border-left: 2px solid var(--border); padding-left: 0.75rem;
  font-size: 0.95rem;
}
section { margin-bottom: 2rem; }
h2 {
  font-size: 1.15rem; font-weight: 600; margin: 0 0 0.75rem;
  letter-spacing: -0.01em;
}
h3 {
  font-size: 0.95rem; font-weight: 600; margin: 1.25rem 0 0.5rem;
  color: var(--muted);
}
.thesis {
  background: var(--card-bg);
  border: 1px solid var(--border); border-left: 4px solid var(--fg);
  padding: 1.25rem 1.5rem; border-radius: 4px;
}
.abcd-grid {
  display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;
  margin-bottom: 2rem;
}
@media (max-width: 720px) { .abcd-grid { grid-template-columns: 1fr; } }
.box {
  background: var(--card-bg); border: 1px solid var(--border);
  border-left-width: 4px; border-radius: 4px;
  padding: 1.25rem 1.5rem;
}
.box-a { border-left-color: var(--a-color); }
.box-b { border-left-color: var(--b-color); }
.box-c { border-left-color: var(--c-color); }
.box-d { border-left-color: var(--d-color); }
.box-a h2 { color: var(--a-color); }
.box-b h2 { color: var(--b-color); }
.box-c h2 { color: var(--c-color); }
.box-d h2 { color: var(--d-color); }
.content ul, .content ol { margin: 0; padding-left: 1.25rem; }
.content li { margin-bottom: 0.4rem; }
.content p:first-child { margin-top: 0; }
.content p:last-child { margin-bottom: 0; }
.content a {
  color: inherit; text-decoration: underline;
  text-decoration-thickness: 1px; text-underline-offset: 2px;
}
.content code {
  background: var(--rail-bg); padding: 0.1em 0.35em;
  border-radius: 3px; font-size: 0.875em;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
}
.content em { color: var(--muted); }
.content blockquote {
  margin: 0.5rem 0; padding: 0.5rem 0.9rem;
  border-left: 2px solid var(--border); color: var(--muted);
}
.rails {
  background: var(--rail-bg); border-radius: 4px;
  padding: 1.25rem 1.5rem;
}
.rails h2 { color: var(--muted); }
.rails h3:first-of-type { margin-top: 0; }
.thread { padding: 0 0.25rem; color: var(--muted); }
footer {
  margin-top: 3rem; padding-top: 1rem;
  border-top: 1px solid var(--border);
  color: var(--muted); font-size: 0.8rem;
  display: flex; justify-content: space-between;
  flex-wrap: wrap; gap: 0.5rem;
}
.placeholder {
  color: var(--muted); font-style: italic; font-size: 0.95rem;
}
@media print {
  body { padding: 0; background: white; color: black; }
  .container { max-width: none; padding: 1cm; }
  .box, .thesis, .rails {
    background: white; border-color: #ccc;
    page-break-inside: avoid;
  }
  .abcd-grid { page-break-inside: avoid; }
  footer { color: #666; }
}
"""

_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Weekly Status — {label}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>{style}</style>
</head>
<body>
<div class="container">
<header>
  <div class="meta">{week_label} · {date_range} · {author}</div>
  <h1>{title}</h1>
  {subtitle_html}
</header>

<section class="thesis">
  <h2>Governing thesis</h2>
  <div class="content">{thesis_html}</div>
</section>

<section class="abcd-grid">
  <article class="box box-a">
    <h2>A · Accomplishments</h2>
    <div class="content">{a_html}</div>
  </article>
  <article class="box box-b">
    <h2>B · Benefits</h2>
    <div class="content">{b_html}</div>
  </article>
  <article class="box box-c">
    <h2>C · Concerns</h2>
    <div class="content">{c_html}</div>
  </article>
  <article class="box box-d">
    <h2>D · Do Next</h2>
    <div class="content">{d_html}</div>
  </article>
</section>

<section class="rails">
  <h2>Activity (auto-rails)</h2>
  <div class="content">{rails_html}</div>
</section>

<section class="thread">
  <h2>Cross-week thread</h2>
  <div class="content">{thread_html}</div>
</section>

<footer>
  <span>Generated {generated_at} by <code>content-engine/engine.py weekly</code></span>
  <span>Source: <code>{source_path}</code></span>
</footer>
</div>
</body>
</html>
"""


def _md_to_html(md: str) -> str:
    """Render a markdown fragment to HTML.

    Strips HTML comments first (they leak <!-- … --> if not removed),
    then runs python-markdown with extras for tables and sane lists.
    """
    if not md or not md.strip():
        return '<p class="placeholder">_(empty)_</p>'

    # Strip HTML comments — they're notes to the author, not for rendering.
    cleaned = re.sub(r"<!--.*?-->", "", md, flags=re.DOTALL).strip()
    if not cleaned:
        return '<p class="placeholder">_(no content)_</p>'

    # Convert wikilinks [[Foo]] / [[Foo|Bar]] to plain HTML links so they
    # don't render as literal text. Target points at .md (Obsidian-style).
    def _wikilink(m: re.Match) -> str:
        target = m.group(1)
        label = m.group(2) or target
        return f'<a href="{target}.md">{label}</a>'
    cleaned = re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", _wikilink, cleaned)

    try:
        import markdown as md_lib
        html = md_lib.markdown(
            cleaned,
            extensions=["extra", "sane_lists", "nl2br"],
            output_format="html5",
        )
    except ImportError:
        # Minimal fallback — paragraphs + bullets + bold/italic + code + links.
        html = _minimal_md_to_html(cleaned)
    return html


def _minimal_md_to_html(md: str) -> str:
    """Fallback markdown converter for when python-markdown isn't available.

    Handles the small subset that weekly status reports actually use.
    """
    lines = md.splitlines()
    out: list[str] = []
    in_list = False
    in_para: list[str] = []

    def _flush_para():
        if in_para:
            text = " ".join(in_para)
            text = _inline_md(text)
            out.append(f"<p>{text}</p>")
            in_para.clear()

    for line in lines:
        stripped = line.strip()
        if not stripped:
            _flush_para()
            if in_list:
                out.append("</ul>")
                in_list = False
            continue
        # Headings (h3 only — h2 is the section)
        if stripped.startswith("### "):
            _flush_para()
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append(f"<h3>{_inline_md(stripped[4:])}</h3>")
            continue
        # Bullets
        m = re.match(r"^[-*]\s+(.*)$", stripped)
        if m:
            _flush_para()
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{_inline_md(m.group(1))}</li>")
            continue
        # Numbered
        m = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if m:
            _flush_para()
            if not in_list:
                out.append("<ol>")
                in_list = True
            out.append(f"<li>{_inline_md(m.group(2))}</li>")
            continue
        # Otherwise paragraph line
        in_para.append(stripped)

    _flush_para()
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def _inline_md(text: str) -> str:
    """Inline markdown — bold, italic, code, links."""
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def _parse_weekly_sections(content: str) -> dict:
    """Parse a weekly status markdown file into named sections.

    Returns a dict with keys: frontmatter (dict), title (str), subtitle (str),
    thesis, a, b, c, d, rails, thread (each a body string, possibly empty).
    """
    out = {
        "frontmatter": {},
        "title": "Weekly Status",
        "subtitle": "",
        "thesis": "", "a": "", "b": "", "c": "", "d": "",
        "rails": "", "thread": "",
    }

    body = content
    fm_match = re.match(r"^---\n(.*?)\n---\n", body, re.DOTALL)
    if fm_match:
        try:
            import yaml
            out["frontmatter"] = yaml.safe_load(fm_match.group(1)) or {}
        except Exception:
            out["frontmatter"] = {}
        body = body[fm_match.end():]

    h1_match = re.match(r"^\s*# (.+)\n", body)
    if h1_match:
        out["title"] = h1_match.group(1).strip()
        body = body[h1_match.end():]

    # Blockquote subtitle (consecutive lines starting with >)
    bq_match = re.match(r"^\s*((?:>.*\n)+)", body)
    if bq_match:
        sub = re.sub(r"^>\s?", "", bq_match.group(1), flags=re.MULTILINE).strip()
        out["subtitle"] = sub
        body = body[bq_match.end():]

    # Split by H2 headings. Strip horizontal rules.
    body = re.sub(r"^---\s*$", "", body, flags=re.MULTILINE)

    # Collect H2 sections including their bodies.
    sections = re.split(r"^## (.+)$", body, flags=re.MULTILINE)
    # sections[0] is whatever came before the first H2
    for i in range(1, len(sections), 2):
        heading = sections[i].strip()
        section_body = sections[i + 1] if i + 1 < len(sections) else ""
        section_body = section_body.strip()
        key = _weekly_section_key(heading)
        if key in out:
            out[key] = section_body
        elif key == "rails-with-children":
            # Auto-rails section — its H3 children become the rails body
            out["rails"] = section_body

    return out


def _weekly_section_key(heading: str) -> str:
    """Map a section heading to a canonical key in the parsed dict."""
    h = heading.lower()
    if "governing thesis" in h:
        return "thesis"
    if h.startswith("a ·") or "accomplishments" in h:
        return "a"
    if h.startswith("b ·") or "benefits" in h:
        return "b"
    if h.startswith("c ·") or "concerns" in h:
        return "c"
    if h.startswith("d ·") or "do next" in h:
        return "d"
    if "auto-rails" in h or "activity" in h:
        return "rails-with-children"
    if "cross-week" in h or "thread" in h:
        return "thread"
    return ""


def _render_weekly_html(md_path: Path, gd_root: Path) -> str:
    """Render a weekly status markdown file as a self-contained HTML page."""
    content = md_path.read_text(encoding="utf-8")
    parsed = _parse_weekly_sections(content)
    fm = parsed["frontmatter"]

    week_label = fm.get("week", parsed["title"].replace("Weekly Status — ", "").strip() or "—")
    week_start = fm.get("week-start", "")
    week_end = fm.get("week-end", "")
    if week_start and week_end:
        date_range = f"{week_start} → {week_end}"
    elif fm.get("date"):
        date_range = str(fm["date"])
    else:
        date_range = ""
    author = fm.get("author", "")

    subtitle_html = ""
    if parsed["subtitle"]:
        # Render subtitle as a simple div, not full markdown
        sub = re.sub(r"\s+", " ", parsed["subtitle"]).strip()
        subtitle_html = f'<div class="subtitle">{sub}</div>'

    try:
        rel_source = md_path.relative_to(gd_root)
    except ValueError:
        rel_source = md_path

    return _HTML_TEMPLATE.format(
        label=week_label,
        style=_HTML_STYLE,
        week_label=week_label,
        date_range=date_range,
        author=author,
        title=parsed["title"],
        subtitle_html=subtitle_html,
        thesis_html=_md_to_html(parsed["thesis"]),
        a_html=_md_to_html(parsed["a"]),
        b_html=_md_to_html(parsed["b"]),
        c_html=_md_to_html(parsed["c"]),
        d_html=_md_to_html(parsed["d"]),
        rails_html=_md_to_html(parsed["rails"]),
        thread_html=_md_to_html(parsed["thread"]),
        generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        source_path=str(rel_source),
    )


@cli.command()
@click.option("--week", default=None,
              help="ISO week label like 2026-W18 (default: current week)")
@click.option("--force", is_flag=True,
              help="Overwrite existing markdown if present")
@click.option("--dry-run", is_flag=True,
              help="Preview rails without writing")
@click.option("--html/--no-html", default=True,
              help="Also render an HTML companion (default: yes)")
@click.option("--html-only", is_flag=True,
              help="Re-render HTML from existing markdown only — don't touch md")
def weekly(week: str | None, force: bool, dry_run: bool,
           html: bool, html_only: bool):
    """Scaffold a weekly ABCD status file with auto-populated rails.

    Creates Brain/status/weekly/YYYY-Www-status.md from the template if it
    doesn't exist, then populates three rails by querying git:

      - Wiki cards added or updated     (Brain/wiki/ commits in week range)
      - Commits of substance            (all non-merge commits in range)
      - Dispatches closed this week     (placeholder — Linear MCP needed)

    Run on Friday afternoon. Fill the ABCD boxes by hand once the rails
    are in place.

    Examples:
        engine.py weekly                    # current week
        engine.py weekly --week 2026-W18    # specific week
        engine.py weekly --dry-run          # preview only
        engine.py weekly --force            # re-scaffold even if file exists
    """
    gd_root = _find_growdirect_root(Path.cwd())
    if not gd_root:
        click.echo("ERROR: Run from within GrowDirect (need CLAUDE.md + Brain/)")
        raise SystemExit(1)

    label, monday_iso, sunday_iso = _iso_week_range(week)
    out_dir = gd_root / BRAIN_STATUS_WEEKLY
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{label}-status.md"
    html_path = out_dir / f"{label}-status.html"

    click.echo(f"Weekly status — {label}")
    click.echo(f"  Range:    {monday_iso} → {sunday_iso}")
    click.echo(f"  MD file:  {out_path.relative_to(gd_root)}")
    if html or html_only:
        click.echo(f"  HTML:     {html_path.relative_to(gd_root)}")

    # --html-only: re-render html from existing md, skip everything else.
    if html_only:
        if not out_path.exists():
            click.echo(f"ERROR: --html-only requires existing markdown at {out_path}")
            raise SystemExit(1)
        html_doc = _render_weekly_html(out_path, gd_root)
        html_path.write_text(html_doc, encoding="utf-8")
        click.echo(f"\n  Wrote {html_path.relative_to(gd_root)} ({len(html_doc):,} bytes)")
        return

    # Compute the auto-rails first so we can show them in dry-run mode.
    wiki_lines = _git_changed_files(gd_root, monday_iso, sunday_iso, "Brain/wiki")
    commit_lines = _git_log_lines(gd_root, monday_iso, sunday_iso)

    rails = {
        "### Dispatches closed this week": (
            "<!-- Linear MCP integration pending — see GRO dispatch. -->\n"
            "_Hand-paste from Linear's Dispatch project, "
            f"status=Done, completed-at between {monday_iso} and {sunday_iso}._\n"
        ),
        "### Wiki cards added or updated": (
            "\n".join(wiki_lines) + "\n" if wiki_lines else "_No wiki changes in range._\n"
        ),
        "### Commits of substance": (
            "\n".join(commit_lines) + "\n" if commit_lines else "_No commits in range._\n"
        ),
    }

    if dry_run:
        click.echo("\n[DRY RUN] Rail preview:\n")
        for heading, body in rails.items():
            click.echo(heading)
            click.echo(body)
        click.echo("  To write: re-run without --dry-run")
        return

    # Scaffold from template if file doesn't exist (or --force given).
    template_path = gd_root / "Brain/templates/weekly-status.md"

    if out_path.exists() and not force:
        click.echo("  Status:   exists — populating rails only")
        content = out_path.read_text(encoding="utf-8")
    else:
        if not template_path.exists():
            click.echo(f"ERROR: template not found: {template_path}")
            raise SystemExit(1)
        click.echo("  Status:   scaffolding from template")
        content = template_path.read_text(encoding="utf-8")
        # Substitute Templater placeholders with concrete dates.
        content = re.sub(
            r"<%\s*tp\.date\.now\([^)]*\)\s*%>",
            "REPLACE_ME",  # placeholder — we'll patch known fields below
            content,
        )
        # Patch known frontmatter fields to concrete values.
        replacements = {
            "date: REPLACE_ME": f"date: {sunday_iso}",
            "week: REPLACE_ME-WREPLACE_ME": f"week: {label}",
            "week-start: REPLACE_ME": f"week-start: {monday_iso}",
            "week-end: REPLACE_ME": f"week-end: {sunday_iso}",
            "last-compiled: REPLACE_ME": f"last-compiled: {sunday_iso}",
            "needs-review: REPLACE_ME": f"needs-review: {_add_days(sunday_iso, 14)}",
        }
        for old, new in replacements.items():
            content = content.replace(old, new)
        # Patch the H1 too.
        content = re.sub(
            r"^# Weekly Status — REPLACE_ME-WREPLACE_ME",
            f"# Weekly Status — {label}",
            content,
            count=1,
            flags=re.MULTILINE,
        )

    # Replace the rail sections.
    for heading, body in rails.items():
        content = _replace_section(content, heading, body)

    out_path.write_text(content, encoding="utf-8")
    click.echo(f"\n  Wrote {out_path.relative_to(gd_root)}")
    click.echo(f"  Wiki adds:  {len(wiki_lines)}")
    click.echo(f"  Commits:    {len(commit_lines)}")

    if html:
        html_doc = _render_weekly_html(out_path, gd_root)
        html_path.write_text(html_doc, encoding="utf-8")
        click.echo(f"  Wrote {html_path.relative_to(gd_root)} ({len(html_doc):,} bytes)")

    click.echo(f"\n  Next: open the file and fill the ABCD boxes (~15 min).")
    if html:
        click.echo(f"  After editing md, refresh html with: engine.py weekly --week {label} --html-only")


# ── Method queries ──────────────────────────────────────────────────

# Repo-relative defaults; overridable in tests via monkeypatch.
# Resolved from Path.cwd() at command invocation time so tests that mock these
# paths take effect.
METHOD_SKILLS_DIR = Path(".claude/skills")
METHOD_TEMPLATES_DIR = Path("Brain/templates")


def _parse_list_field(value: str) -> list[str]:
    """Parse `[A, B, C]` or `A, B, C` or `A` into a list of names."""
    v = value.strip().strip("[]")
    if not v:
        return []
    return [x.strip() for x in v.split(",") if x.strip()]


def _method_meta(path: Path) -> dict:
    """Extract role/stage metadata from a file's YAML frontmatter.

    Recognized keys:
      - name (skill identity)
      - roles-primary, roles-assist, stage (skill tagging, Sprint C)
      - method-role, method-stage (template tagging, Sprint C)
      - type (template type marker)
    Missing keys return empty values. Non-frontmatter files return an empty dict.
    """
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    m = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not m:
        return {}
    fm = m.group(1)
    out = {
        "name": "",
        "type": "",
        "roles-primary": [],
        "roles-assist": [],
        "stage": "",
        "method-role": "",
        "method-stage": "",
    }
    for line in fm.splitlines():
        line_m = re.match(r"^([a-zA-Z-]+):\s*(.*)$", line)
        if not line_m:
            continue
        key, val = line_m.group(1), line_m.group(2).strip()
        if key in ("roles-primary", "roles-assist"):
            out[key] = _parse_list_field(val)
        elif key in ("name", "type", "stage", "method-role", "method-stage"):
            out[key] = val
    return out


@cli.group()
def method():
    """Query the GrowDirect Method graph — roles, stages, skills, templates."""
    pass


@method.command("skills-for")
@click.option("--role", default=None, help="Filter to skills this role uses")
@click.option("--stage", default=None, help="Filter to skills that implement this stage")
@click.option("--primary-only", is_flag=True, default=False,
              help="Only match roles-primary (skip roles-assist)")
def method_skills_for(role: str | None, stage: str | None, primary_only: bool):
    """List skills filtered by role and/or stage.

    Examples:
      engine.py method skills-for --role ALX
      engine.py method skills-for --stage blueprint
      engine.py method skills-for --role Jeremy --stage tdd
      engine.py method skills-for --role Tom --primary-only
    """
    if not role and not stage:
        raise click.UsageError("Pass --role and/or --stage.")

    skills_dir = METHOD_SKILLS_DIR
    if not skills_dir.is_absolute():
        skills_dir = (Path.cwd() / skills_dir) if not skills_dir.exists() else skills_dir

    if not skills_dir.exists():
        click.echo(f"No skills dir at {skills_dir}")
        return

    matches: list[tuple[str, dict]] = []
    for path in sorted(skills_dir.glob("*.md")):
        meta = _method_meta(path)
        if not meta.get("name"):
            continue
        if role:
            primary = meta["roles-primary"]
            assist = meta["roles-assist"]
            if role not in primary and (primary_only or role not in assist):
                continue
        if stage and meta["stage"] != stage:
            continue
        matches.append((path.stem, meta))

    header = []
    if role:
        header.append(f"role={role}{' (primary only)' if primary_only else ''}")
    if stage:
        header.append(f"stage={stage}")
    click.echo(f"Skills matching {', '.join(header)}: {len(matches)}")
    click.echo()
    for name, meta in matches:
        marker = "primary" if role and role in meta["roles-primary"] else "assist" if role else ""
        stage_note = f"  [stage: {meta['stage']}]" if meta["stage"] else ""
        role_note = f"  [{marker}]" if marker else ""
        click.echo(f"  {name}{role_note}{stage_note}")


@method.command("templates-for")
@click.option("--role", required=True, help="Filter to templates authored by this role")
def method_templates_for(role: str):
    """List Brain templates authored by a given role."""
    tpl_dir = METHOD_TEMPLATES_DIR
    if not tpl_dir.is_absolute():
        tpl_dir = (Path.cwd() / tpl_dir) if not tpl_dir.exists() else tpl_dir

    if not tpl_dir.exists():
        click.echo(f"No templates dir at {tpl_dir}")
        return

    matches = []
    for path in sorted(tpl_dir.glob("*.md")):
        meta = _method_meta(path)
        if meta.get("method-role") == role:
            matches.append((path.stem, meta))

    click.echo(f"Templates for method-role={role}: {len(matches)}")
    click.echo()
    for name, meta in matches:
        stage = meta.get("method-stage") or ""
        stage_note = f"  [stage: {stage}]" if stage else ""
        click.echo(f"  {name}{stage_note}")


@method.command("roles")
def method_roles():
    """List roles and their stage coverage (based on skill frontmatter)."""
    skills_dir = METHOD_SKILLS_DIR
    if not skills_dir.is_absolute():
        skills_dir = (Path.cwd() / skills_dir) if not skills_dir.exists() else skills_dir
    if not skills_dir.exists():
        click.echo(f"No skills dir at {skills_dir}")
        return

    # Role -> {primary: {stage: [skill]}, assist: {stage: [skill]}}
    index: dict[str, dict[str, dict[str, list[str]]]] = defaultdict(
        lambda: {"primary": defaultdict(list), "assist": defaultdict(list)}
    )
    for path in sorted(skills_dir.glob("*.md")):
        meta = _method_meta(path)
        if not meta.get("name"):
            continue
        stage = meta["stage"] or "(unscoped)"
        for r in meta["roles-primary"]:
            index[r]["primary"][stage].append(meta["name"])
        for r in meta["roles-assist"]:
            index[r]["assist"][stage].append(meta["name"])

    if not index:
        click.echo("No tagged skills found.")
        return

    for role in sorted(index):
        data = index[role]
        p_count = sum(len(v) for v in data["primary"].values())
        a_count = sum(len(v) for v in data["assist"].values())
        click.echo(f"\n  {role}: {p_count} primary, {a_count} assist")
        for stage in sorted(data["primary"]):
            skills = data["primary"][stage]
            click.echo(f"    [primary] {stage}: {', '.join(skills)}")
        for stage in sorted(data["assist"]):
            skills = data["assist"][stage]
            click.echo(f"    [assist]  {stage}: {', '.join(skills)}")


@method.command("stats")
def method_stats():
    """Summary counts — tagged vs untagged skills + templates + stage coverage."""
    skills_dir = METHOD_SKILLS_DIR
    if not skills_dir.is_absolute():
        skills_dir = (Path.cwd() / skills_dir) if not skills_dir.exists() else skills_dir
    tpl_dir = METHOD_TEMPLATES_DIR
    if not tpl_dir.is_absolute():
        tpl_dir = (Path.cwd() / tpl_dir) if not tpl_dir.exists() else tpl_dir

    s_tagged = s_untagged = 0
    stage_counts: dict[str, int] = defaultdict(int)
    role_counts: dict[str, int] = defaultdict(int)
    if skills_dir.exists():
        for p in skills_dir.glob("*.md"):
            meta = _method_meta(p)
            if not meta.get("name"):
                continue
            if meta["roles-primary"] or meta["roles-assist"]:
                s_tagged += 1
                for r in meta["roles-primary"]:
                    role_counts[r] += 1
                if meta["stage"]:
                    stage_counts[meta["stage"]] += 1
            else:
                s_untagged += 1

    t_tagged = t_untagged = 0
    if tpl_dir.exists():
        for p in tpl_dir.glob("*.md"):
            meta = _method_meta(p)
            if meta.get("method-role"):
                t_tagged += 1
            else:
                t_untagged += 1

    click.echo(f"\nSkills:    {s_tagged} tagged, {s_untagged} untagged")
    click.echo(f"Templates: {t_tagged} tagged, {t_untagged} untagged")
    click.echo(f"Tagged: {s_tagged + t_tagged}  Untagged: {s_untagged + t_untagged}")

    if stage_counts:
        click.echo("\n  Stage coverage (skills):")
        for stage, n in sorted(stage_counts.items()):
            click.echo(f"    {stage:12s} {n}")

    if role_counts:
        click.echo("\n  Role coverage (primary skills):")
        for r, n in sorted(role_counts.items(), key=lambda x: -x[1]):
            click.echo(f"    {r:12s} {n}")


if __name__ == "__main__":
    cli()
