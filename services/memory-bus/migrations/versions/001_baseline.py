"""001 — baseline: capture current growdirect_memory DDL.

Revision ID: 001_baseline
Create Date: 2026-03-30

STAMP PROCEDURE — existing environments:
  cd services/memory-bus && alembic stamp 001_baseline && alembic upgrade head
FRESH INSTALLS:
  cd services/memory-bus && alembic upgrade head
"""

from alembic import op

revision = "001_baseline"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    CREATE TABLE IF NOT EXISTS alx_sessions (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        session_id TEXT UNIQUE NOT NULL,
        started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        closed_at TIMESTAMPTZ,
        status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'closed', 'abandoned')),
        gro_issues JSONB DEFAULT '[]',
        summary TEXT,
        decisions JSONB DEFAULT '[]',
        unresolved JSONB DEFAULT '[]',
        created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );
    CREATE INDEX IF NOT EXISTS idx_sessions_status ON alx_sessions(status);
    CREATE INDEX IF NOT EXISTS idx_sessions_started ON alx_sessions(started_at DESC);

    CREATE TABLE IF NOT EXISTS alx_memories (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        session_id TEXT NOT NULL,
        memory_type TEXT NOT NULL CHECK (memory_type IN (
            'decision', 'finding', 'context', 'architecture',
            'session_summary', 'procedure', 'context_block',
            'work_product', 'team_profile'
        )),
        content TEXT NOT NULL,
        metadata JSONB DEFAULT '{}',
        embedding vector(1024),
        layer TEXT NOT NULL DEFAULT 'shared' CHECK (layer IN ('corp', 'canary', 'cove', 'shared')),
        created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );
    CREATE INDEX IF NOT EXISTS idx_memories_session ON alx_memories(session_id);
    CREATE INDEX IF NOT EXISTS idx_memories_type ON alx_memories(memory_type);
    CREATE INDEX IF NOT EXISTS idx_memories_created ON alx_memories(created_at DESC);
    CREATE INDEX IF NOT EXISTS idx_memories_layer ON alx_memories(layer);

    CREATE TABLE IF NOT EXISTS seed_embeddings (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        source_file TEXT NOT NULL,
        section_path TEXT,
        content TEXT NOT NULL,
        embedding vector(1024) NOT NULL,
        metadata JSONB DEFAULT '{}',
        created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );
    CREATE INDEX IF NOT EXISTS idx_seed_source ON seed_embeddings(source_file);
    CREATE INDEX IF NOT EXISTS idx_seed_embedding_hnsw
        ON seed_embeddings USING hnsw (embedding vector_cosine_ops);
    """)


def downgrade():
    op.execute("DROP TABLE IF EXISTS seed_embeddings CASCADE")
    op.execute("DROP TABLE IF EXISTS alx_memories CASCADE")
    op.execute("DROP TABLE IF EXISTS alx_sessions CASCADE")
