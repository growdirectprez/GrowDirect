# GrowDirect LLC — Confidential & Proprietary
# Copyright (c) 2026 GrowDirect LLC. All rights reserved.
"""006 — add engines: text[] applicability column to alx_memories.

Revision ID: 006_add_engines
Create Date: 2026-04-30

Per docs/sdds/platform/memory-bus.md §11. The engines column is the
canonical applicability tag — six engine primitives (loyalty, voting,
store-ops, web-store, operations, geospatial) plus 'platform' for
substrate. Backfilled from the legacy 'layer' column. The 'layer'
column is retained for backward compatibility but is no longer the
canonical applicability filter — 'engines' is.

Backfill mapping:
  layer 'corp', 'shared'  -> engines '{platform}'
  layer 'canary'          -> engines '{operations}'
  layer 'cove'            -> engines '{loyalty,voting}'

A GIN index supports the `engines && :requested_engines` overlap
query pattern used by the recall tools.
"""

from alembic import op

revision = "006_add_engines"
down_revision = "005_drop_layer_check"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    ALTER TABLE alx_memories
    ADD COLUMN engines text[] NOT NULL DEFAULT '{platform}';
    """)

    op.execute("""
    UPDATE alx_memories SET engines = '{platform}'
    WHERE layer IN ('corp', 'shared');
    """)
    op.execute("""
    UPDATE alx_memories SET engines = '{operations}'
    WHERE layer = 'canary';
    """)
    op.execute("""
    UPDATE alx_memories SET engines = '{loyalty,voting}'
    WHERE layer = 'cove';
    """)

    op.execute("""
    CREATE INDEX IF NOT EXISTS idx_alx_memories_engines
    ON alx_memories USING gin (engines);
    """)


def downgrade():
    op.execute("DROP INDEX IF EXISTS idx_alx_memories_engines")
    op.execute("ALTER TABLE alx_memories DROP COLUMN IF EXISTS engines")
