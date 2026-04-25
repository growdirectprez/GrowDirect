# GrowDirect LLC — Confidential & Proprietary
# Copyright (c) 2026 GrowDirect LLC. All rights reserved.
"""Alembic environment for growdirect_memory database."""

import os
from alembic import context
from sqlalchemy import create_engine

config = context.config
database_url = os.environ.get(
    "DATABASE_URL",
    "postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/growdirect_memory",
)


def run_migrations_online():
    engine = create_engine(database_url)
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=None)
        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
