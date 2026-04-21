# Secure MOC + Product Wiki — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship `Brain/projects/Secure.md` + 6 wiki articles + 2 working briefs, synthesized from the `/Users/gclyle/secure/` archive and the NAS `~/mnt/nas-archive/Work/Clients/` Secure-era client folders. Along the way, extend `content-engine/engine.py` with an `extract` command that converts Office + PDF files to markdown via `markitdown`.

**Architecture:** The extract command is a pure function (`_extract_file`) separated from the Click CLI wiring, making it testable in isolation. Extracted markdown goes to `Secure/docs/extracted/` (new project dir) and passes through a PII review gate before being ingested to `Brain/raw/inbox/` via the existing `engine.py ingest` command. Wiki articles are synthesized from intake notes, following the existing `canary-*` pattern and the `Brain/templates/wiki-article.md` frontmatter schema (required fields: `last-compiled`, `needs-review` — enforced by `engine.py lint`).

**Tech Stack:** Python 3.14 (system), Click, `markitdown 0.1.5` (already installed, Apache-2.0, MS-maintained), `pytest` for new engine tests, `textutil` (macOS built-in) and `pdftotext` as fallbacks, Obsidian for vault rendering.

**Spec:** [docs/superpowers/specs/2026-04-21-secure-moc-and-wiki-design.md](../specs/2026-04-21-secure-moc-and-wiki-design.md)

**Discovery deltas from spec** (plan-time facts the spec didn't know):

- Most `~/secure/PROJECTS/` folders are **empty stubs** locally. Only `FM-JDA` (1856 files), `Circuit City` (234), `Fresh&Easy` (85), `CEO Study` (23), `Dumoulin` (14), `CBM/D&G/CIRCUIT CITY WPC` (≤7 each) have content locally. Most of those are **pre-Secure IBM consulting** (2002–2005).
- **Secure-era client content is on the NAS**, not local. Kroger pilot pulls from `~/mnt/nas-archive/Work/Clients/KROGER/` + `~/mnt/nas-archive/Work/Projects/Kroger CRP/` + `~/mnt/nas-archive/Reference/Kroger POS Baseline.pdf`.
- `markitdown 0.1.5` is already installed (`pip list | grep markitdown`) — plan-time checkpoint #1 (dependency flag) is **resolved**. Record it in `content-engine/requirements.txt` for reproducibility.
- NAS share is `//192.168.10.117/archive` (creds: user `gclyle`). Must be mounted at `~/mnt/nas-archive` before Chunk 7.

---

## Chunk 1: Pre-flight + plan-time checkpoints

**Purpose:** Confirm plan-time assumptions with user before any code lands.

- [ ] **Step 1.1: Confirm NAS mount + credentials are available**

  Run: `mount | grep nas-archive`
  Expected: `//GCLYLE@192.168.10.117/archive on /Users/gclyle/mnt/nas-archive (smbfs, ...)`
  If not mounted: `mkdir -p ~/mnt/nas-archive && mount_smbfs //gclyle@192.168.10.117/archive ~/mnt/nas-archive` (will prompt for password).

- [ ] **Step 1.2: Confirm `markitdown` is already on the system**

  Run: `python3 -c "import markitdown; print(markitdown.__version__)"`
  Expected: `0.1.5` (or newer).
  If missing: `pip install markitdown` — per standing instruction, confirm with user first.

- [ ] **Step 1.3: Confirm pilot client (Kroger)**

  User-facing prompt: "Spec pilot is Kroger (NAS-sourced). Confirm or pick Wal-Mart / Harrods / other." Record decision in chunk start comment.

- [ ] **Step 1.4: Confirm PII review gate**

  User-facing prompt: "Default = extract→review→ingest two-step. Confirm, or allow single-step extract→ingest with session-level PII review of intake notes instead." Record decision.

- [ ] **Step 1.5: Verify git clean + plan committed**

  Run: `git status docs/superpowers/plans/2026-04-21-secure-moc-and-wiki.md`
  Expected: plan file exists, may be untracked — commit plan file before starting Chunk 2.

---

## Chunk 2: Engine `extract` command (TDD)

**Purpose:** Add a tested `extract` command to `content-engine/engine.py` that converts Office + PDF files to markdown via `markitdown` with documented fallbacks.

**Files:**
- Create: `content-engine/requirements.txt`
- Create: `content-engine/tests/__init__.py`
- Create: `content-engine/tests/test_extract.py`
- Create: `content-engine/tests/fixtures/sample.docx` (tiny real docx)
- Create: `content-engine/tests/fixtures/sample.pdf` (tiny real pdf)
- Modify: `content-engine/engine.py` (add `_extract_file` helper + `extract` command)

### 2.1 Scaffolding

- [ ] **Step 2.1.1: Create `content-engine/requirements.txt`**

  ```
  click>=8.1
  markitdown>=0.1.5
  ```

- [ ] **Step 2.1.2: Create `content-engine/tests/__init__.py`** (empty file).

- [ ] **Step 2.1.3: Create test fixtures**

  ```bash
  mkdir -p content-engine/tests/fixtures
  # Make a tiny docx via python-docx or copy one from ~/secure
  python3 -c "from docx import Document; d=Document(); d.add_heading('Fixture', 0); d.add_paragraph('hello extract test'); d.save('content-engine/tests/fixtures/sample.docx')"
  # If python-docx not present, copy a known-small docx from ~/secure and rename
  cp "/Users/gclyle/secure/Secure Lite Config.docx" content-engine/tests/fixtures/sample.docx
  # Tiny PDF
  cp "/Users/gclyle/secure/Secure 5 Solution Architecture.pdf" content-engine/tests/fixtures/sample.pdf
  ```

  Use whichever works first. The fixture files must be real Office/PDF — not placeholders — so markitdown has something real to convert.

- [ ] **Step 2.1.4: Commit scaffolding**

  ```bash
  git add content-engine/requirements.txt content-engine/tests/
  git commit -m "chore(content-engine): scaffold tests/ + requirements.txt"
  ```

### 2.2 Write the failing test for `_extract_file`

- [ ] **Step 2.2.1: Write `test_extract.py` — pure-function tests first**

  Create `content-engine/tests/test_extract.py`:

  ```python
  """Tests for engine._extract_file and the `extract` CLI command."""
  import json
  import subprocess
  import sys
  from pathlib import Path

  import pytest
  from click.testing import CliRunner

  REPO_ROOT = Path(__file__).resolve().parents[2]
  ENGINE = REPO_ROOT / "content-engine" / "engine.py"
  FIXTURES = Path(__file__).parent / "fixtures"

  sys.path.insert(0, str(REPO_ROOT / "content-engine"))
  import engine  # noqa: E402


  # ── _extract_file ────────────────────────────────────────────────────

  def test_extract_file_docx_returns_markdown(tmp_path):
      src = FIXTURES / "sample.docx"
      target = tmp_path / "sample.docx.md"
      entry = engine._extract_file(src, target)
      assert entry["status"] == "ok"
      assert entry["method"] == "markitdown"
      assert target.exists()
      text = target.read_text()
      assert len(text) > 0
      # Manifest fields
      assert entry["source_sha256"]
      assert entry["target_path"] == str(target)
      assert entry["extracted_at"].startswith("20")  # ISO-8601
      assert entry["error"] is None

  def test_extract_file_pdf_returns_markdown(tmp_path):
      src = FIXTURES / "sample.pdf"
      target = tmp_path / "sample.pdf.md"
      entry = engine._extract_file(src, target)
      assert entry["status"] == "ok"
      assert entry["method"] in ("markitdown", "pdftotext")
      assert target.exists()
      assert len(target.read_text()) > 0

  def test_extract_file_unsupported_ext_returns_skipped(tmp_path):
      src = tmp_path / "thing.vsd"
      src.write_bytes(b"FAKE VISIO")
      target = tmp_path / "thing.vsd.md"
      entry = engine._extract_file(src, target)
      assert entry["status"] == "skipped"
      assert entry["method"] == "skip"
      assert not target.exists()

  def test_extract_file_nonexistent_source_raises(tmp_path):
      src = tmp_path / "does-not-exist.docx"
      target = tmp_path / "out.md"
      with pytest.raises((FileNotFoundError, OSError)):
          engine._extract_file(src, target)


  # ── extract CLI command ──────────────────────────────────────────────

  def test_extract_cli_dry_run_default(tmp_path):
      """Default is dry-run; no files should be written."""
      # Stage fixtures in a temp source dir
      src_dir = tmp_path / "src"
      src_dir.mkdir()
      (src_dir / "a.docx").write_bytes((FIXTURES / "sample.docx").read_bytes())
      target = tmp_path / "out"

      runner = CliRunner()
      result = runner.invoke(engine.cli, ["extract", str(src_dir), "--target", str(target)])
      assert result.exit_code == 0, result.output
      assert "DRY RUN" in result.output or "dry-run" in result.output.lower()
      # No markdown written
      assert not any(target.rglob("*.md")) if target.exists() else True

  def test_extract_cli_execute_writes_manifest_and_markdown(tmp_path):
      src_dir = tmp_path / "src"
      src_dir.mkdir()
      (src_dir / "a.docx").write_bytes((FIXTURES / "sample.docx").read_bytes())
      (src_dir / "~$a.docx").write_bytes(b"tempfile")  # Office temp — should be skipped
      target = tmp_path / "out"

      runner = CliRunner()
      result = runner.invoke(
          engine.cli,
          ["extract", str(src_dir), "--target", str(target), "--execute"],
      )
      assert result.exit_code == 0, result.output
      # Markdown written preserving tree
      assert (target / "a.docx.md").exists()
      # Temp file skipped by default (--skip-tmp is default)
      assert not (target / "~$a.docx.md").exists()
      # Manifest written
      manifest_path = target / ".extract-manifest.json"
      assert manifest_path.exists()
      manifest = json.loads(manifest_path.read_text())
      assert isinstance(manifest, list)
      ok = [m for m in manifest if m["status"] == "ok"]
      assert len(ok) == 1
      assert ok[0]["source_path"].endswith("a.docx")

  def test_extract_cli_ext_filter(tmp_path):
      """--ext restricts which extensions to process."""
      src_dir = tmp_path / "src"
      src_dir.mkdir()
      (src_dir / "a.docx").write_bytes((FIXTURES / "sample.docx").read_bytes())
      (src_dir / "b.pdf").write_bytes((FIXTURES / "sample.pdf").read_bytes())
      target = tmp_path / "out"

      runner = CliRunner()
      result = runner.invoke(
          engine.cli,
          ["extract", str(src_dir), "--target", str(target), "--ext", "docx", "--execute"],
      )
      assert result.exit_code == 0, result.output
      assert (target / "a.docx.md").exists()
      assert not (target / "b.pdf.md").exists()

  def test_extract_cli_maxdepth_top_level_only(tmp_path):
      src_dir = tmp_path / "src"
      (src_dir / "nested").mkdir(parents=True)
      (src_dir / "top.docx").write_bytes((FIXTURES / "sample.docx").read_bytes())
      (src_dir / "nested" / "deep.docx").write_bytes((FIXTURES / "sample.docx").read_bytes())
      target = tmp_path / "out"

      runner = CliRunner()
      result = runner.invoke(
          engine.cli,
          ["extract", str(src_dir), "--target", str(target), "--maxdepth", "1", "--execute"],
      )
      assert result.exit_code == 0, result.output
      assert (target / "top.docx.md").exists()
      assert not (target / "nested" / "deep.docx.md").exists()
  ```

- [ ] **Step 2.2.2: Run tests — expect failure**

  Run: `cd /Users/gclyle/GrowDirect && python3 -m pytest content-engine/tests/test_extract.py -v`
  Expected: **ALL FAIL** with `AttributeError: module 'engine' has no attribute '_extract_file'` and `No such command 'extract'`.

### 2.3 Implement `_extract_file` and the CLI command

- [ ] **Step 2.3.1: Add constants + helper to `engine.py` top**

  Modify `content-engine/engine.py`. Add after the existing helper functions (right before `# ── CLI ──────────` at ~line 153):

  ```python
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
      Never raises except for I/O problems on the source path itself.

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

      # Unsupported or all fallbacks failed
      if ext not in EXTRACT_DEFAULT_EXTS:
          entry["status"] = "skipped"
          entry["method"] = "skip"
          entry["error"] = f"unsupported extension: .{ext}"
      return entry
  ```

- [ ] **Step 2.3.2: Run pure-function tests — expect the 4 `_extract_file` tests to pass**

  Run: `python3 -m pytest content-engine/tests/test_extract.py::test_extract_file_docx_returns_markdown content-engine/tests/test_extract.py::test_extract_file_pdf_returns_markdown content-engine/tests/test_extract.py::test_extract_file_unsupported_ext_returns_skipped content-engine/tests/test_extract.py::test_extract_file_nonexistent_source_raises -v`
  Expected: **4 PASS**. CLI tests still FAIL.

- [ ] **Step 2.3.3: Add the `extract` Click command**

  Modify `content-engine/engine.py`. Add after the `clean` command (around line 546, right before `# ── Knowledge Layer Commands ──`):

  ```python
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

      # Collect candidates
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

      # Execute
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
  ```

- [ ] **Step 2.3.4: Run full test suite**

  Run: `python3 -m pytest content-engine/tests/test_extract.py -v`
  Expected: **all 8 tests PASS**.

- [ ] **Step 2.3.5: Commit the extract command**

  ```bash
  git add content-engine/engine.py content-engine/tests/
  git commit -m "feat(content-engine): add extract command for binary→markdown"
  ```

### 2.4 Smoke test on real Secure docs

- [ ] **Step 2.4.1: Pilot extract on 3 real files**

  ```bash
  cd /Users/gclyle/GrowDirect
  mkdir -p /tmp/secure-pilot
  python3 content-engine/engine.py extract /Users/gclyle/secure \
    --target /tmp/secure-pilot \
    --maxdepth 1 \
    --ext docx,pdf,xlsx \
    --execute
  ```

  Expected: 16 files processed (top-level only), manifest written, `ok` count ≥14.
  Spot-check output: `cat "/tmp/secure-pilot/Secure 5 Solution Architecture.docx.md" | head -40` — should show real markdown content, not binary garbage.

- [ ] **Step 2.4.2: If OK rate is <90%, diagnose and add fallback**

  If failures exceed 2 of 16, read `/tmp/secure-pilot/.extract-failures.json` and add handling (e.g., install `pdftotext` via `brew install poppler` if multiple PDFs failed — flag the dep to user first).

- [ ] **Step 2.4.3: Discard pilot, clean up**

  ```bash
  rm -rf /tmp/secure-pilot
  ```

---

## Chunk 3: Client classification working brief

**Purpose:** Produce `docs/superpowers/briefs/2026-04-secure-client-split.md` listing every `PROJECTS/` folder + every NAS client dir with an era classification (Secure-era vs pre-Secure) and a local-vs-NAS provenance note. This brief feeds both the pre-Secure stub wiki (Chunk 8) and the Kroger deep-dive (Chunk 7).

**Files:**
- Create: `docs/superpowers/briefs/2026-04-secure-client-split.md`

- [ ] **Step 3.1: Enumerate local `~/secure/PROJECTS/`**

  ```bash
  for d in /Users/gclyle/secure/PROJECTS/*/; do
    n=$(find "$d" -type f 2>/dev/null | wc -l | tr -d ' ')
    first_mtime=$(find "$d" -type f -printf '%T@ %p\n' 2>/dev/null | sort -n | head -1 | awk '{print $1}')
    last_mtime=$(find "$d" -type f -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -1 | awk '{print $1}')
    echo "$n | $d | $first_mtime | $last_mtime"
  done
  ```

  (macOS `find` doesn't support `-printf` — if that fails, use `stat -f '%m %N'` instead.) Capture output for the brief.

- [ ] **Step 3.2: Enumerate NAS `~/mnt/nas-archive/Work/Clients/` + `Work/Projects/`**

  ```bash
  ls ~/mnt/nas-archive/Work/Clients/
  ls ~/mnt/nas-archive/Work/Projects/
  ```

  Capture output.

- [ ] **Step 3.3: Write the brief**

  Structure:

  ```markdown
  ---
  title: Secure Client Split — Era Classification
  date: 2026-04-21
  type: brief
  sprint: secure-sprint-1
  ---

  # Secure Client Split

  ## Purpose
  Classify every client folder in the Secure archive by era: Secure product era
  (~2010–2019) vs. pre-Secure IBM consulting (~2001–2005).

  ## Source locations
  - `/Users/gclyle/secure/PROJECTS/` (local, many empty stubs)
  - `/Users/gclyle/mnt/nas-archive/Work/Clients/` (NAS, where Secure-era content lives)
  - `/Users/gclyle/mnt/nas-archive/Work/Projects/` (NAS)

  ## Classification table

  | Folder | Local files | NAS files | First mtime | Last mtime | Era | Notes |
  |---|---|---|---|---|---|---|
  | Kroger CRP | 0 | ~20 | 2005-ish | 2015-ish | **Secure-era** | Pilot client |
  | Wal-Mart | 0 | TBD | | | Secure-era (Secure 3.2 guide confirms) | |
  | Harrods | 0 | TBD | | | Secure-era | |
  | Staples | 0 | TBD | | | Secure-era | |
  | Toys 'R' Us | 0 | TBD | | | Secure-era | |
  | Fresh&Easy | 85 | TBD | 2008 | | **Pre-Secure** | GMIS/JDA era |
  | Circuit City | 234 | TBD | 2002 | | **Pre-Secure** | IBM consulting |
  | FM-JDA | 1856 | TBD | 2004 | 2005 | **Pre-Secure** | JDA/PMM 2005 |
  | CEO Study | 23 | | 2006 | | **Pre-Secure** | IBM Global CEO Study |
  | CBM | 7 | | | | **Pre-Secure** | Component Business Model |
  | ... | | | | | | |

  ## Decisions
  - **Pilot client = Kroger** (confirmed Chunk 1.3). Source = NAS.
  - Pre-Secure folders covered by stub wiki (Chunk 8). No ingest.
  - Ambiguous folders (NOTES, RETAIL) default to pre-Secure stub.

  ## Open items
  - NAS client folders not yet fully enumerated beyond Kroger. Sprint 2 picks one more.
  ```

  Fill in TBD rows by actually running `ls` / `find` on NAS paths.

- [ ] **Step 3.4: Commit the brief**

  ```bash
  git add docs/superpowers/briefs/2026-04-secure-client-split.md
  git commit -m "brief: Secure client era classification (pre-Secure vs Secure-era)"
  ```

---

## Chunk 4: MOC shell

**Purpose:** Write `Brain/projects/Secure.md` with final frontmatter + placeholder wiki links. Wiki articles don't exist yet; the MOC is the navigation scaffold everything else fills in.

**Files:**
- Create: `Brain/projects/Secure.md`

- [ ] **Step 4.1: Write the MOC using Obsidian MCP**

  Use the `mcp__obsidian__create_note_tool` (or write via filesystem — either works; user's standing instruction is MCP for Brain content):

  ```yaml
  ---
  type: project-moc
  status: archive-active
  tags: [secure, retail, loss-prevention, ibm, appriss, canary-lineage]
  ---

  **Wiki:** [[Brain/Home|Home]]

  # Secure

  Historical retail loss-prevention product suite (IBM / Appriss / Sysrepublic,
  ~2010–2019). Archive project — the product itself is shipped; Brain captures
  the IP and cross-references it into Canary, which is the modern reincarnation.

  ## Status
  Archive. Product history, architecture, and client implementations preserved
  for Canary domain lineage + founder-credibility narrative.

  ## Wiki Articles
  - [[Brain/wiki/secure-platform-overview|Platform Overview]] — what Secure was, product line, positioning vs Canary
  - [[Brain/wiki/secure-architecture|Architecture]] — S5 on-premise solution, SSO, factory/delivery process
  - [[Brain/wiki/secure-lite|Secure Lite]] — product variant (overview + config)
  - [[Brain/wiki/secure-omnichannel|Omnichannel]] — omnichannel positioning + Appriss data spec
  - [[Brain/wiki/secure-client-kroger|Kroger Implementation]] — pilot client deep-dive
  - [[Brain/wiki/secure-retail-career-archive|Pre-Secure Retail Career Archive]] — stub index of pre-Secure IBM consulting work

  ## Source Archive
  - Local (curated product docs): `/Users/gclyle/secure/`
  - NAS (client implementations): `/Users/gclyle/mnt/nas-archive/Work/Clients/` + `Work/Projects/`
  - NAS (complementary): `Work/Clients/SECURE 5/` (2017 EBR4/EBR5), `Email/CLIENTS/SECURE 5/`

  ## Canary Lineage
  - [[docs/superpowers/briefs/2026-04-secure-to-canary-handoff|Secure → Canary Handoff]] — patterns worth porting
  - [[Brain/projects/Canary|Canary]] — forward project (modern retail LP for Square merchants)

  ## Client Implementations
  - **Kroger** — [[Brain/wiki/secure-client-kroger|deep-dive]] (Sprint 1 pilot)
  - Wal-Mart, Harrods, Staples, Toys 'R' Us — Sprint 2+ (sources on NAS)
  - See [[docs/superpowers/briefs/2026-04-secure-client-split|Client Era Classification]] for full list

  ## Related Projects
  - [[Brain/projects/Canary|Canary]] — Canary platform (Secure's forward evolution)
  - [[Brain/wiki/secure-retail-career-archive|Pre-Secure Retail Career]] — earlier IBM consulting era
  ```

- [ ] **Step 4.2: Verify MOC renders**

  Open `Brain/projects/Secure.md` in Obsidian. All wiki links should show as unresolved (red) — this is expected; articles are created in later chunks. The MOC itself should render.

- [ ] **Step 4.3: Commit the MOC**

  ```bash
  git add Brain/projects/Secure.md
  git commit -m "brain: add Secure project MOC (wiki links unresolved until chunks 6-8)"
  ```

---

## Chunk 5: Extract + ingest top-level Secure product docs

**Purpose:** Run the extract pipeline on the 16 top-level product docs, review output for PII, then ingest each into `Brain/raw/inbox/` as raw intake notes the next chunk can synthesize.

**Files:**
- Create: `Secure/docs/extracted/*.md` (16 files)
- Create: `Secure/docs/extracted/.extract-manifest.json`
- Create: `Brain/raw/inbox/secure-*.md` (one per extracted doc)

- [ ] **Step 5.1: Extract top-level product docs**

  ```bash
  cd /Users/gclyle/GrowDirect
  mkdir -p Secure/docs/extracted
  python3 content-engine/engine.py extract /Users/gclyle/secure \
    --target Secure/docs/extracted \
    --maxdepth 1 \
    --ext doc,docx,ppt,pptx,xls,xlsx,pdf \
    --execute
  ```

  Expected: 16 source files processed (15 top-level docs listed in spec + ignore PROJECTS subfolder because maxdepth=1).

- [ ] **Step 5.2: Inspect extraction results**

  ```bash
  cat Secure/docs/extracted/.extract-manifest.json | python3 -m json.tool | head -60
  ls Secure/docs/extracted/*.md
  ```

  Verify ≥14 of 16 succeeded. If failures, read `.extract-failures.json` and decide per-file (retry with fallback, skip, or hand-transcribe). Success criterion: ≥90% `ok`.

- [ ] **Step 5.3: PII review pass** (user gate — see Chunk 1.4)

  If gate is on (default): inspect each `.md` for employee names, store numbers, transaction samples, customer PII. Redact in-place if found. Commit redactions separately for audit trail.

  If gate is off: skip this step; PII review happens on intake notes instead.

- [ ] **Step 5.4: Commit extracted markdown**

  ```bash
  git add Secure/docs/extracted/
  git commit -m "content(secure): extract 16 top-level product docs to markdown"
  ```

- [ ] **Step 5.5: Ingest each extracted file to Brain raw inbox**

  ```bash
  for f in Secure/docs/extracted/*.md; do
    python3 content-engine/engine.py ingest "$f" --project secure --tags "secure,loss-prevention,retail"
  done
  ```

  Expected: ~16 new files in `Brain/raw/inbox/secure-*.md`, each with `status: unprocessed` frontmatter.

- [ ] **Step 5.6: Commit raw intake notes**

  ```bash
  git add Brain/raw/inbox/
  git commit -m "brain: ingest Secure top-level product docs as raw intake notes"
  ```

---

## Chunk 6: Four product wiki articles

**Purpose:** Synthesize 4 Brain wiki articles from the intake notes. Each article must pass `engine.py lint --all` (requires `last-compiled` + `needs-review` frontmatter).

**Files:**
- Create: `Brain/wiki/secure-platform-overview.md`
- Create: `Brain/wiki/secure-architecture.md`
- Create: `Brain/wiki/secure-lite.md`
- Create: `Brain/wiki/secure-omnichannel.md`

**Writing conventions** (apply to ALL wiki articles in this sprint):

- Frontmatter must match `Brain/templates/wiki-article.md` schema. Required fields: `date`, `type: wiki`, `tags: [...]`, `sources: [...]`, `last-compiled: YYYY-MM-DD`, `needs-review: YYYY-MM-DD` (today + 14 days = 2026-05-05).
- `**Wiki:** [[Brain/Home|Home]]` above the H1.
- Sections: `# Title`, `## Summary` (2–3 sentences), `## Details` (main body, can have H2/H3 subsections), `## Related`, `## Sources` (list intake notes + source doc paths).
- No hype copy. Direct, serious, tangible. No "cutting-edge", "industry-leading", "revolutionary".
- No volatile data (no "X rows", "Y customers" — link to DB queries or source doc page instead).
- Target ~200 lines each; no hard cap.

### 6.1 `secure-platform-overview.md`

- [ ] **Step 6.1.1: Read source intake notes**

  ```bash
  cat Brain/raw/inbox/secure-5-solution-architecture.md
  cat Brain/raw/inbox/secure-omnichannel-overview-oct2018.md
  cat Brain/raw/inbox/factory-overview-v2.md
  cat Brain/raw/inbox/new-delivery-process.md
  cat Brain/raw/inbox/secure-lite-overview.md
  ```

- [ ] **Step 6.1.2: Synthesize `Brain/wiki/secure-platform-overview.md`**

  Structure the article to answer:
  - What was Secure? (product line context)
  - Who bought it? (retail LP market, on-prem model)
  - What problem did it solve? (loss prevention, exception-based reporting, retail data pipeline)
  - What was the product shape? (Secure 3 → 5, Lite, Omnichannel — relationships between SKUs)
  - How does it map to Canary today? (forward arrow: same problem, different tech, different buyer)

  `sources` frontmatter field lists the intake note paths.

- [ ] **Step 6.1.3: Run lint**

  Run: `python3 content-engine/engine.py lint Brain/wiki/secure-platform-overview.md`
  Expected: `Clean.`

- [ ] **Step 6.1.4: Commit**

  ```bash
  git add Brain/wiki/secure-platform-overview.md
  git commit -m "brain(secure): add Platform Overview wiki"
  ```

### 6.2 `secure-architecture.md`

- [ ] **Step 6.2.1: Read source intake notes**

  ```bash
  cat Brain/raw/inbox/s5-on-premise-solution-architecture-v1-1-draft.md
  cat Brain/raw/inbox/sso-overview-v2.md
  cat Brain/raw/inbox/factory-overview-v2.md
  cat Brain/raw/inbox/new-delivery-process.md
  cat Brain/raw/inbox/dev-ops.md
  cat Brain/raw/inbox/dev-ops-deliverables.md
  ```

- [ ] **Step 6.2.2: Synthesize `Brain/wiki/secure-architecture.md`**

  Sections to cover:
  - On-premise deployment model (hardware, data residency)
  - Data ingest (POS, BOH, corporate feeds)
  - Detection / exception engine (what Secure classified as "exceptions")
  - Reporting surface (EBR — Exception-Based Reporting)
  - SSO / identity integration
  - Factory + New Delivery Process (their build/release discipline — relevant to Canary)

- [ ] **Step 6.2.3: Lint + commit** (same pattern as 6.1.3–6.1.4)

### 6.3 `secure-lite.md`

- [ ] **Step 6.3.1: Read**

  ```bash
  cat Brain/raw/inbox/secure-lite-overview.md
  cat Brain/raw/inbox/secure-lite-config.md
  ```

- [ ] **Step 6.3.2: Synthesize `Brain/wiki/secure-lite.md`**

  Shorter article — ~100 lines is fine. What Secure Lite was, who it targeted (smaller merchants), how it differed from full Secure, config highlights.

- [ ] **Step 6.3.3: Lint + commit**

### 6.4 `secure-omnichannel.md`

- [ ] **Step 6.4.1: Read**

  ```bash
  cat Brain/raw/inbox/secure-omnichannel-overview-oct2018.md
  cat Brain/raw/inbox/appriss-retail-data-specification-v1-1.md
  cat Brain/raw/inbox/5-1-requirements.md
  cat Brain/raw/inbox/kroger-dsd-requirements.md
  ```

- [ ] **Step 6.4.2: Synthesize `Brain/wiki/secure-omnichannel.md`**

  Sections:
  - Omnichannel positioning (why Secure added this line)
  - Appriss retail data spec relationship (how data flowed in)
  - Requirements model (what 5.1 Requirements.xlsx covered)
  - Kroger DSD requirements as a concrete spec example

- [ ] **Step 6.4.3: Lint + commit**

### 6.5 Checkpoint

- [ ] **Step 6.5.1: Run full lint sweep**

  ```bash
  python3 content-engine/engine.py lint --all
  ```

  Expected: `Clean. All required frontmatter fields present.` Exit code 0.

---

## Chunk 7: Kroger pilot deep-dive

**Purpose:** Extract Kroger source files from NAS, ingest, synthesize `secure-client-kroger.md`. Uses the pipeline proven in Chunks 2 + 5 — no new infrastructure.

**Files:**
- Create: `Secure/docs/extracted/kroger/*.md`
- Create: `Brain/raw/inbox/kroger-*.md`
- Create: `Brain/wiki/secure-client-kroger.md`

- [ ] **Step 7.1: Verify NAS mount**

  Run: `ls ~/mnt/nas-archive/Work/Clients/KROGER/`
  Expected: file listing including `Kroger POS Baseline.pdf`, `.mpp`, `.xlsb` files.
  If not mounted: see Chunk 1.1.

- [ ] **Step 7.2: Extract Kroger sources**

  ```bash
  cd /Users/gclyle/GrowDirect
  mkdir -p Secure/docs/extracted/kroger
  # NAS client folder
  python3 content-engine/engine.py extract ~/mnt/nas-archive/Work/Clients/KROGER \
    --target Secure/docs/extracted/kroger \
    --ext doc,docx,ppt,pptx,xls,xlsx,pdf \
    --execute
  # NAS project folder
  python3 content-engine/engine.py extract ~/mnt/nas-archive/Work/Projects/Kroger\ CRP \
    --target Secure/docs/extracted/kroger \
    --ext doc,docx,ppt,pptx,xls,xlsx,pdf \
    --execute
  # Reference PDFs
  python3 content-engine/engine.py extract ~/mnt/nas-archive/Reference \
    --target Secure/docs/extracted/kroger/reference \
    --maxdepth 1 \
    --ext pdf \
    --execute
  # Local Kroger DSD doc is already in Chunk 5 output — skip
  ```

  Caveats:
  - `.mpp` (MS Project) and `.xlsb` (Excel binary workbook) will likely fail markitdown. Record failures in `.extract-failures.json` and note in the wiki article under "Sources not parsed."
  - Space in folder name `Kroger CRP` — quote properly.

- [ ] **Step 7.3: PII review pass** (if gate is on)

  Inspect extracted `.md` for employee names, store numbers. Redact in-place.

- [ ] **Step 7.4: Commit extracted Kroger markdown**

  ```bash
  git add Secure/docs/extracted/kroger/
  git commit -m "content(secure): extract Kroger source docs from NAS"
  ```

- [ ] **Step 7.5: Ingest**

  ```bash
  for f in Secure/docs/extracted/kroger/*.md Secure/docs/extracted/kroger/reference/*.md; do
    python3 content-engine/engine.py ingest "$f" --project secure --tags "secure,kroger,retail"
  done
  git add Brain/raw/inbox/
  git commit -m "brain: ingest Kroger source docs"
  ```

- [ ] **Step 7.6: Synthesize `Brain/wiki/secure-client-kroger.md`**

  Sections:
  - Relationship summary (timeframe, engagement type, product variants deployed)
  - Deployment context (POS baseline, CRP scope, on-premise)
  - Integration points (DSD — Direct Store Delivery — as captured in `Kroger DSD requirements`)
  - What Secure detected for Kroger (specific exception types, if docs reveal)
  - Lessons / patterns for Canary (link forward to handoff brief in Chunk 9)
  - Sources (list every ingested intake note)

  Frontmatter:
  ```yaml
  ---
  date: 2026-04-21
  type: wiki
  tags: [secure, kroger, retail, loss-prevention, client-implementation]
  sources:
    - Brain/raw/inbox/kroger-pos-baseline.md
    - Brain/raw/inbox/kroger-dsd-requirements.md
    - Brain/raw/inbox/kroger-crp-v1.md
    - ... (list all)
  last-compiled: 2026-04-21
  needs-review: 2026-05-05
  ---
  ```

- [ ] **Step 7.7: Lint + commit**

  ```bash
  python3 content-engine/engine.py lint Brain/wiki/secure-client-kroger.md
  git add Brain/wiki/secure-client-kroger.md
  git commit -m "brain(secure): add Kroger client implementation wiki"
  ```

---

## Chunk 8: Pre-Secure retail career stub

**Purpose:** Single wiki article enumerating the pre-Secure `PROJECTS/` folders with one-line descriptions, eras, and "not ingested — circle back later" status. Built from the classification brief (Chunk 3).

**Files:**
- Create: `Brain/wiki/secure-retail-career-archive.md`

- [ ] **Step 8.1: Synthesize from classification brief**

  Article shape:

  ```markdown
  ---
  date: 2026-04-21
  type: wiki
  tags: [secure, retail-career, ibm-consulting, archive-stub]
  sources:
    - docs/superpowers/briefs/2026-04-secure-client-split.md
  last-compiled: 2026-04-21
  needs-review: 2026-05-05
  ---

  **Wiki:** [[Brain/Home|Home]]

  # Pre-Secure Retail Career Archive

  ## Summary
  Index of pre-Secure IBM / consulting era client folders (~2001–2009) in the
  Secure archive. Not ingested. Stubbed here so the knowledge that these
  folders exist is captured; deeper ingest defers to Sprint 2+ or later.

  ## Details

  ### Populated folders (local)
  | Folder | Files | Era | One-liner |
  |---|---|---|---|
  | FM-JDA | 1856 | 2004–2005 | JDA / PMM consulting, PM artifacts |
  | Circuit City | 234 | 2002+ | IBM consulting — retail |
  | Fresh&Easy | 85 | 2008 | GMIS / JDA implementation |
  | CEO Study | 23 | 2006 | IBM Global CEO Study 2006 (retail POV) |
  | Dumoulin | 14 | | |
  | CBM | 7 | | IBM Component Business Model |
  | D&G | 6 | | |
  | CIRCUIT CITY WPC | 6 | | |

  ### Empty stub folders (content may be on NAS or never existed locally)
  GAP, Harrods, Heartbeat, IBM Method Web, Kroger CRP (NAS-populated),
  MCS Better Business, MCS Project Assessment, NOTES, PA LCB, PB, RETAIL,
  RETEK, SAP, SWINDON, Staples, TODAYMAN, TSA, Toys, Toys 'R' Us, WESTON,
  Wal-Mart — all empty locally.

  ## Related
  - [[Brain/projects/Secure|Secure]] MOC
  - [[Brain/wiki/secure-client-kroger|Kroger]] — the one Sprint 1 pilot
  - [[docs/superpowers/briefs/2026-04-secure-client-split|Client Era Classification]]

  ## Sources
  - `/Users/gclyle/secure/PROJECTS/` (local enumeration)
  - `docs/superpowers/briefs/2026-04-secure-client-split.md`
  ```

- [ ] **Step 8.2: Lint + commit**

  ```bash
  python3 content-engine/engine.py lint Brain/wiki/secure-retail-career-archive.md
  git add Brain/wiki/secure-retail-career-archive.md
  git commit -m "brain(secure): add pre-Secure retail career archive stub"
  ```

---

## Chunk 9: Canary handoff brief

**Purpose:** Mine the extracted Secure content for 5+ concrete patterns/schemas/concepts Canary should adopt or explicitly reject. Output is a working brief under `docs/superpowers/briefs/`, not a wiki article.

**Files:**
- Create: `docs/superpowers/briefs/2026-04-secure-to-canary-handoff.md`

- [ ] **Step 9.1: Re-read the extracted docs with Canary eyes**

  Focus on: Appriss retail data spec, S5 solution architecture, Kroger DSD requirements, 5.1 Requirements, SSO Overview. For each, note:
  - Data schema choices Secure made (entities, relationships, naming)
  - Exception/detection types Secure classified
  - Deployment/delivery discipline (Factory + NDP)
  - SSO/identity model
  - Kroger-specific adaptations worth generalizing

- [ ] **Step 9.2: Write the brief**

  ```markdown
  ---
  title: Secure → Canary Handoff
  date: 2026-04-21
  type: brief
  sprint: secure-sprint-1
  ---

  # Secure → Canary Handoff

  ## Purpose
  Extract 5+ patterns from the Secure archive that Canary should adopt or
  explicitly reject. This is the "what did we already learn 15 years ago"
  brief — not a design doc.

  ## Patterns

  ### 1. [Pattern name] — ADOPT / REJECT / ADAPT
  **Source:** `Secure/docs/extracted/<file>.md` section X
  **What Secure did:** ...
  **Why it matters for Canary:** ...
  **Recommendation:** ...

  ### 2. ...

  ### 3. ...

  ### 4. ...

  ### 5. ...

  ## Explicitly NOT ported
  - [Thing Secure did that Canary should NOT do] — reason

  ## Follow-up Linear issues
  - GRO-XXX: ...
  ```

  Minimum 5 patterns, each with an explicit ADOPT/REJECT/ADAPT call + source file citation + one sentence of rationale.

- [ ] **Step 9.3: Commit**

  ```bash
  git add docs/superpowers/briefs/2026-04-secure-to-canary-handoff.md
  git commit -m "brief: Secure → Canary handoff (5+ patterns)"
  ```

---

## Chunk 10: Registry rebuild, CLAUDE.md update, MOC finalize

**Purpose:** Close the loop. Registry sees the new wiki. CLAUDE.md Projects table gets the new Secure row. MOC linkage is verified.

**Files:**
- Modify: `Brain/REGISTRY.json` (regenerated)
- Modify: `CLAUDE.md` (add Secure row to Projects table)
- Modify: `Brain/projects/Secure.md` (verify all links resolve)

- [ ] **Step 10.1: Final lint sweep**

  ```bash
  python3 content-engine/engine.py lint --all
  ```

  Expected: `Clean.` Exit 0. If not clean: fix the offending articles before proceeding.

- [ ] **Step 10.2: Rebuild registry**

  ```bash
  python3 content-engine/engine.py registry build
  ```

  Expected output includes 6 new Secure wiki articles + 1 MOC in the indexed articles list.

- [ ] **Step 10.3: Verify registry coverage**

  ```bash
  python3 content-engine/engine.py registry check "secure"
  python3 content-engine/engine.py registry check "kroger"
  python3 content-engine/engine.py registry check "loss prevention"
  ```

  Expected: each returns ≥1 matching article with file paths.

- [ ] **Step 10.4: Commit registry**

  ```bash
  git add Brain/REGISTRY.json
  git commit -m "brain: rebuild registry (adds Secure wiki + MOC)"
  ```

- [ ] **Step 10.5: Update `CLAUDE.md` Projects table**

  In `CLAUDE.md`, locate the Projects table (around line 20). Add a row after Seacove:

  ```markdown
  | Secure | `Secure/` | **Archive** | Historical retail LP IP (IBM / Appriss / Sysrepublic 2001–2019). Extracted markdown only — source archive lives at `~/secure/` + NAS `~/mnt/nas-archive/Work/Clients/`. |
  ```

- [ ] **Step 10.6: Commit CLAUDE.md**

  ```bash
  git add CLAUDE.md
  git commit -m "docs: add Secure to CLAUDE.md Projects table"
  ```

- [ ] **Step 10.7: Verify MOC renders in Obsidian**

  Open `Brain/projects/Secure.md`. All wiki links must render as resolved (not red). If any are unresolved:
  - Check filename matches exactly (case-sensitive on some platforms)
  - Run `registry build` again if it's a stale cache

- [ ] **Step 10.8: Final verification checklist**

  - [ ] `Brain/projects/Secure.md` exists and renders
  - [ ] 6 `Brain/wiki/secure-*.md` files exist (including `secure-retail-career-archive.md`)
  - [ ] 2 briefs in `docs/superpowers/briefs/`
  - [ ] Extracted markdown in `Secure/docs/extracted/` + `Secure/docs/extracted/kroger/`
  - [ ] `content-engine/engine.py extract` works; tests pass
  - [ ] `engine.py lint --all` clean
  - [ ] `engine.py registry check "secure"` returns results
  - [ ] CLAUDE.md Projects table has Secure row
  - [ ] Canary handoff brief has ≥5 patterns

- [ ] **Step 10.9: Sprint close**

  ```bash
  git log --oneline -20  # review all Sprint 1 commits
  ```

  Session close: post a one-paragraph summary to the session. No PR needed (work is on main; review is out-of-band per existing GrowDirect practice).

---

## Risks + what to stop for

- **Kroger source files fail extraction at >30% rate.** Stop the sprint, reconsider tooling before writing the wiki. Possible: `.mpp` files need separate handling; `.xlsb` may need LibreOffice conversion (flag dep first).
- **PII surfaces in extracted content.** Stop ingest. Redact in `Secure/docs/extracted/` before any intake note is created. Commit redactions as their own commit for audit trail.
- **Lint fails on wiki articles.** Do not commit until clean. Required fields: `last-compiled`, `needs-review`.
- **Registry fails to find Secure articles after Chunk 10.2.** Check frontmatter `tags:` field parses correctly (must be `[...]` bracketed list). Inspect `Brain/REGISTRY.json` for the article entries.

## Out of scope reminder

This plan does NOT:
- Process any of the 33 non-Kroger `PROJECTS/` folders beyond stubbing them.
- Build a separate `Retail-Career` MOC (stays a wiki stub).
- Produce founder-credibility sales artifacts.
- Migrate `~/secure/` into the repo.
- Update any existing Canary wiki articles (handoff brief identifies targets — Sprint 2 acts on them).
