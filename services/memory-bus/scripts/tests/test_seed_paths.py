# services/memory-bus/scripts/tests/test_seed_paths.py
"""Tests for --include-paths glob filtering in seed_standalone.py."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add script dir to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import seed_standalone


def _fake_sources(tmp_path):
    """Create a minimal SOURCES-like structure with test files."""
    (tmp_path / "Brain" / "wiki" / "cards").mkdir(parents=True)
    (tmp_path / "Brain" / "projects").mkdir(parents=True)
    (tmp_path / "Cove").mkdir(parents=True)

    files = {
        "Brain/wiki/cards/canary-item.md": "canary card",
        "Brain/wiki/cards/ncr-ecosystem.md": "ncr card",
        "Brain/wiki/cards/cove-hoa.md": "cove card",
        "Brain/projects/Canary.md": "canary project",
        "Brain/projects/Cove.md": "cove project",
    }
    for rel, content in files.items():
        p = tmp_path / rel
        p.write_text(content)

    sources = [
        {"glob": "Brain/wiki/cards/*.md", "memory_type": "context_block",
         "layer": "corp", "engines": ["platform"]},
        {"glob": "Brain/projects/*.md", "memory_type": "context_block",
         "layer": "corp", "engines": ["platform"]},
    ]
    return sources, tmp_path


def test_no_include_paths_returns_all_files(tmp_path):
    """Without --include-paths, all files from all sources are returned."""
    sources, root = _fake_sources(tmp_path)
    with patch.object(seed_standalone, "SOURCES", sources), \
         patch.object(seed_standalone, "GROWDIRECT_ROOT", root):
        result = seed_standalone.collect_files(include_patterns=None)
    assert len(result) == 5


def test_include_paths_filters_to_canary_cards(tmp_path):
    """--include-paths Brain/wiki/cards/canary-*.md returns only canary cards."""
    sources, root = _fake_sources(tmp_path)
    with patch.object(seed_standalone, "SOURCES", sources), \
         patch.object(seed_standalone, "GROWDIRECT_ROOT", root):
        result = seed_standalone.collect_files(
            include_patterns=["Brain/wiki/cards/canary-*.md"]
        )
    paths = [str(f.relative_to(root)) for f, _ in result]
    assert paths == ["Brain/wiki/cards/canary-item.md"]


def test_include_paths_multi_pattern(tmp_path):
    """Multiple patterns are OR'd — any match includes the file."""
    sources, root = _fake_sources(tmp_path)
    with patch.object(seed_standalone, "SOURCES", sources), \
         patch.object(seed_standalone, "GROWDIRECT_ROOT", root):
        result = seed_standalone.collect_files(
            include_patterns=[
                "Brain/wiki/cards/canary-*.md",
                "Brain/wiki/cards/ncr-*.md",
                "Brain/projects/Canary.md",
            ]
        )
    paths = {str(f.relative_to(root)) for f, _ in result}
    assert paths == {
        "Brain/wiki/cards/canary-item.md",
        "Brain/wiki/cards/ncr-ecosystem.md",
        "Brain/projects/Canary.md",
    }


def test_include_paths_excludes_cove(tmp_path):
    """Cove files do not appear when --include-paths omits them."""
    sources, root = _fake_sources(tmp_path)
    with patch.object(seed_standalone, "SOURCES", sources), \
         patch.object(seed_standalone, "GROWDIRECT_ROOT", root):
        result = seed_standalone.collect_files(
            include_patterns=["Brain/wiki/cards/canary-*.md"]
        )
    paths = [str(f.relative_to(root)) for f, _ in result]
    assert "Brain/wiki/cards/cove-hoa.md" not in paths
    assert "Brain/projects/Cove.md" not in paths
