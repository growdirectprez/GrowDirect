# GrowDirect LLC — Confidential & Proprietary
# Copyright (c) 2026 GrowDirect LLC. All rights reserved.
"""007 — mercury: vector dimension 768 + audit_events table.

Revision ID: 007_mercury_dimension_768
Revises: 006_add_engines
Create Date: 2026-05-05

Switches embedding columns from vector(1024) — sized for qwen3-embedding:8b —
to vector(768) for Vertex AI text-embedding-004. Rebuilds the HNSW index at
the correct dimension. Adds audit_events for Mercury append-only audit trail.

Only applied to the mercury (cloud) database. The local growdirect_memory
database continues to use vector(1024) with the Docker Ollama embedder.
"""

from alembic import op

revision = "007_mercury_dimension_768"
down_revision = "006_add_engines"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TABLE alx_memories ALTER COLUMN embedding TYPE vector(768)")
    op.execute("ALTER TABLE seed_embeddings ALTER COLUMN embedding TYPE vector(768)")
    op.execute("DROP INDEX IF EXISTS idx_alx_memories_embedding")
    op.execute(
        """
        CREATE INDEX idx_alx_memories_embedding
          ON alx_memories USING hnsw (embedding vector_cosine_ops)
          WITH (m = 16, ef_construction = 64)
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS audit_events (
            id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            artifact_id UUID,
            event_type  TEXT NOT NULL,
            layer       TEXT NOT NULL,
            payload     JSONB,
            created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS audit_events")
    op.execute("DROP INDEX IF EXISTS idx_alx_memories_embedding")
    op.execute("ALTER TABLE alx_memories ALTER COLUMN embedding TYPE vector(1024)")
    op.execute("ALTER TABLE seed_embeddings ALTER COLUMN embedding TYPE vector(1024)")
    op.execute(
        """
        CREATE INDEX idx_alx_memories_embedding
          ON alx_memories USING hnsw (embedding vector_cosine_ops)
          WITH (m = 16, ef_construction = 64)
        """
    )
