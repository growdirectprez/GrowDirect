import pytest
from graphs.state import PipelineState
from graphs.nodes.generate import generate_node
from graphs.nodes.review import review_node, route_after_review
from graphs.nodes.emit import emit_node
from pathlib import Path
import tempfile


def test_generate_node_populates_artifacts(llm_approved, base_state):
    result = generate_node(base_state, llm=llm_approved)
    assert isinstance(result["artifacts"], dict)
    assert len(result["artifacts"]) > 0


def test_review_node_approved(llm_approved, base_state):
    base_state["artifacts"] = {"cmd/hawk/main.go": "package main\n"}
    result = review_node(base_state, llm=llm_approved)
    assert result["review_result"] == "approved"


def test_review_node_needs_revision(llm_needs_revision, base_state):
    base_state["artifacts"] = {"cmd/hawk/main.go": "package main\n"}
    result = review_node(base_state, llm=llm_needs_revision)
    assert result["review_result"] == "needs_revision"


def test_route_after_review_approved(base_state):
    base_state["review_result"] = "approved"
    assert route_after_review(base_state) == "emit"


def test_route_after_review_needs_revision_under_limit(base_state):
    base_state["review_result"] = "needs_revision"
    base_state["revision_count"] = 1
    assert route_after_review(base_state) == "generate"


def test_route_after_review_needs_revision_over_limit(base_state):
    base_state["review_result"] = "needs_revision"
    base_state["revision_count"] = 3
    assert route_after_review(base_state) == "emit"  # force emit after max revisions


def test_emit_node_writes_files(base_state):
    base_state["artifacts"] = {
        "cmd/hawk/main.go": "package main\nfunc main() {}",
        "internal/hawk/handler.go": "package hawk\n",
    }
    with tempfile.TemporaryDirectory() as tmpdir:
        base_state["output_dir"] = tmpdir
        result = emit_node(base_state)
        assert (Path(tmpdir) / "cmd/hawk/main.go").exists()
        assert (Path(tmpdir) / "internal/hawk/handler.go").exists()
        assert (Path(tmpdir) / "apply.sh").exists()
