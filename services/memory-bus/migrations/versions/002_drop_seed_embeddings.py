"""002 — drop seed_embeddings table (unused, not queried by any code).

Revision ID: 002_drop_seed_embeddings
Create Date: 2026-03-30
"""

from alembic import op

revision = "002_drop_seed_embeddings"
down_revision = "001_baseline"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("DROP TABLE IF EXISTS seed_embeddings CASCADE")


def downgrade():
    op.execute("""
    CREATE TABLE seed_embeddings (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        source_file TEXT NOT NULL,
        section_path TEXT,
        content TEXT NOT NULL,
        embedding vector(1024) NOT NULL,
        metadata JSONB DEFAULT '{}',
        created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );
    CREATE INDEX idx_seed_source ON seed_embeddings(source_file);
    CREATE INDEX idx_seed_embedding_hnsw
        ON seed_embeddings USING hnsw (embedding vector_cosine_ops);
    """)
