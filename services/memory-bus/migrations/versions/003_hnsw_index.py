"""003 — add HNSW index on alx_memories.embedding for vector search performance.

Revision ID: 003_hnsw_index
Create Date: 2026-03-30
"""

from alembic import op

revision = "003_hnsw_index"
down_revision = "002_drop_seed_embeddings"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    CREATE INDEX IF NOT EXISTS idx_alx_memories_embedding_hnsw
    ON alx_memories USING hnsw (embedding vector_cosine_ops);
    """)


def downgrade():
    op.execute("DROP INDEX IF EXISTS idx_alx_memories_embedding_hnsw")
