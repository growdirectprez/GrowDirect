"""scenario run favorites

Revision ID: 0005
Revises: 0004
Create Date: 2026-04-25 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '0005'
down_revision: Union[str, None] = '0004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'scenario_run_favorites',
        sa.Column('admin_user_id', sa.UUID(), nullable=False),
        sa.Column('scenario_run_id', sa.UUID(), nullable=False),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['admin_user_id'], ['admin_users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['scenario_run_id'], ['scenario_runs.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        'uq_scenario_run_favorites_admin_run',
        'scenario_run_favorites',
        ['admin_user_id', 'scenario_run_id'],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index('uq_scenario_run_favorites_admin_run', table_name='scenario_run_favorites')
    op.drop_table('scenario_run_favorites')
