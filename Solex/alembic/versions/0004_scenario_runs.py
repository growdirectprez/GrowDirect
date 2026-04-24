"""scenario runs

Revision ID: 0004
Revises: 0003
Create Date: 2026-04-24 14:30:14.630578

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0004'
down_revision: Union[str, None] = '0003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'scenario_runs',
        sa.Column('scenario_name', sa.String(length=80), nullable=False),
        sa.Column('params_json', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('admin_user_id', sa.UUID(), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('summary_json', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['admin_user_id'], ['admin_users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_scenario_runs_name', 'scenario_runs', ['scenario_name'], unique=False)
    op.create_index('ix_scenario_runs_status', 'scenario_runs', ['status'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_scenario_runs_status', table_name='scenario_runs')
    op.drop_index('ix_scenario_runs_name', table_name='scenario_runs')
    op.drop_table('scenario_runs')
