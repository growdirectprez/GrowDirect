"""005 — drop CHECK constraint on alx_memories.layer.

Revision ID: 005_drop_layer_check
Create Date: 2026-04-24

The original 001_baseline migration encoded a closed allowlist of layer
values directly in a CHECK constraint. That coupled the platform memory
bus to the apps it could serve, which contradicts the design intent
that memory-bus is platform infrastructure and apps are namespace-
scoped tenants. Validation of supported layers belongs at the app
boundary (VALID_LAYERS in memory_bus.store), not in the database.

This migration drops the CHECK constraint. The default value remains
'shared'. Existing rows are unaffected. App-side validation continues
to gate writes per the VALID_LAYERS frozenset.
"""

from alembic import op

revision = "005_drop_layer_check"
down_revision = "004_session_fk"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    ALTER TABLE alx_memories
    DROP CONSTRAINT IF EXISTS alx_memories_layer_check;
    """)


def downgrade():
    # Restoring the original allowlist would require re-asserting an
    # opinion about which layer values are valid. The downgrade
    # intentionally restores only the schema-shape constraint with no
    # value list — DBAs reverting this migration should add the
    # specific allowlist they want as a follow-up.
    op.execute("""
    ALTER TABLE alx_memories
    ADD CONSTRAINT alx_memories_layer_check
    CHECK (layer IS NOT NULL AND layer <> '');
    """)
