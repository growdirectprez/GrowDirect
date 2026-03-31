"""004 — backfill orphan session records + add session_id FK to alx_memories.

Revision ID: 004_session_fk
Create Date: 2026-03-30
"""

from alembic import op

revision = "004_session_fk"
down_revision = "003_hnsw_index"
branch_labels = None
depends_on = None


def upgrade():
    # Step 1: Create session records for any orphan session_ids
    op.execute("""
    INSERT INTO alx_sessions (session_id, status, started_at, closed_at, summary)
    SELECT
        m.session_id,
        'closed',
        MIN(m.created_at),
        MAX(m.created_at),
        'Backfilled session for orphan memories (migration 004)'
    FROM alx_memories m
    WHERE m.session_id NOT IN (SELECT session_id FROM alx_sessions)
    GROUP BY m.session_id;
    """)

    # Step 2: Add foreign key constraint
    op.execute("""
    ALTER TABLE alx_memories
    ADD CONSTRAINT fk_memories_session
    FOREIGN KEY (session_id) REFERENCES alx_sessions(session_id);
    """)


def downgrade():
    op.execute("""
    ALTER TABLE alx_memories DROP CONSTRAINT IF EXISTS fk_memories_session;
    """)
