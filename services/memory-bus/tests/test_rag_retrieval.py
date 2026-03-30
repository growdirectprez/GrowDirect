"""Integration tests for RAG retrieval — dual-table semantic search (GRO-240).

Tests run against live canary_memory DB with populated seed_embeddings.
Requires: Ollama running with qwen3-embedding:8b, canary_memory DB with seed data.

Run inside container:
    python3 -m pytest tests/integration/test_rag_retrieval.py -v -m postgres
"""
import pytest
import os
import sys

sys.path.insert(0, "/app")

# Force qwen3 model regardless of container env (which may still have nomic)
os.environ["EMBEDDING_MODEL"] = "qwen3-embedding:8b"

# Skip entire module if CANARY_MEMORY_DB_URL not set (host without DB)
pytestmark = pytest.mark.postgres


@pytest.fixture(scope="module")
def db_session():
    """Get a SQLAlchemy session for canary_memory."""
    from canary.services.alx.memory import _get_session
    session = _get_session()
    yield session
    session.close()


@pytest.fixture(scope="module", autouse=True)
def reset_embedding_globals():
    """Reset lazy-init globals so env var override takes effect."""
    from canary.services.alx import memory
    memory._OLLAMA_URL = None
    memory._EMBED_MODEL = None
    yield


class TestSeedEmbeddingsPopulated:
    """Verify seed_embeddings table has data from the batch embed."""

    def test_seed_embeddings_row_count(self, db_session):
        from sqlalchemy import text
        count = db_session.execute(
            text("SELECT COUNT(*) FROM seed_embeddings")
        ).scalar()
        assert count >= 300, f"Expected 300+ seed embeddings, got {count}"

    def test_seed_embeddings_have_all_tiers(self, db_session):
        from sqlalchemy import text
        rows = db_session.execute(
            text("SELECT DISTINCT metadata->>'tier' FROM seed_embeddings")
        ).fetchall()
        tiers = {r[0] for r in rows}
        assert "ip_seeds" in tiers
        assert "sdd_v2" in tiers
        assert "team_profiles" in tiers

    def test_seed_embeddings_vector_dimensions(self, db_session):
        from sqlalchemy import text
        dims = db_session.execute(
            text("SELECT vector_dims(embedding) FROM seed_embeddings LIMIT 1")
        ).scalar()
        assert dims == 1024, f"Expected 1024-dim vectors, got {dims}"


class TestDualTableSearch:
    """Test memory_semantic_search against live data."""

    def test_search_returns_seed_results(self):
        """Query about Chirp should find IP seed and SDD content."""
        from canary.services.alx.memory import memory_semantic_search
        result = memory_semantic_search("Chirp detection engine loss patterns", limit=5)
        assert result["count"] > 0, "Expected matches for 'Chirp detection engine'"
        assert result["source"] == "pgvector"
        # Should find seed content (memory_type='seed')
        seed_matches = [m for m in result["matches"] if m["memory_type"] == "seed"]
        assert len(seed_matches) > 0, "Expected at least one seed_embeddings match"

    def test_search_returns_relevant_content(self):
        """Results should contain content related to the query."""
        from canary.services.alx.memory import memory_semantic_search
        result = memory_semantic_search("Square webhook transaction processing", limit=5)
        assert result["count"] > 0
        # At least one match should mention Square or webhook or transaction
        contents = " ".join(m["content"].lower() for m in result["matches"])
        assert any(term in contents for term in ["square", "webhook", "transaction"]), \
            "Expected relevant content about Square/webhook/transactions"

    def test_search_similarity_scores_reasonable(self):
        """Similarity scores should be between 0 and 1."""
        from canary.services.alx.memory import memory_semantic_search
        result = memory_semantic_search("Canary product architecture", limit=5)
        for match in result["matches"]:
            assert 0.0 <= match["similarity"] <= 1.0, \
                f"Similarity {match['similarity']} out of range"

    def test_search_with_memory_type_skips_seeds(self):
        """When memory_type filter is set, seed_embeddings should not be searched."""
        from canary.services.alx.memory import memory_semantic_search
        result = memory_semantic_search(
            "architecture decisions", limit=5, memory_type="decision"
        )
        # With empty alx_memories, this should return 0 matches
        # (seeds are skipped when memory_type is set)
        seed_matches = [m for m in result["matches"] if m["memory_type"] == "seed"]
        assert len(seed_matches) == 0, "Seeds should not appear when memory_type filter is set"

    def test_search_team_profiles(self):
        """Search for team member should find operational profiles."""
        from canary.services.alx.memory import memory_semantic_search
        result = memory_semantic_search("ALX agent responsibilities COO", limit=5)
        assert result["count"] > 0
        # Should find team profile content
        contents = " ".join(m["content"].lower() for m in result["matches"])
        assert "alx" in contents, "Expected ALX profile in results"

    def test_search_empty_query_returns_gracefully(self):
        """Empty or minimal query should not crash."""
        from canary.services.alx.memory import memory_semantic_search
        result = memory_semantic_search("", limit=5)
        assert isinstance(result, dict)
        assert "matches" in result

    def test_search_limit_respected(self):
        """Limit parameter should cap results."""
        from canary.services.alx.memory import memory_semantic_search
        result = memory_semantic_search("Canary", limit=3)
        assert len(result["matches"]) <= 3
