from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from solex.config import resolve_config
from solex.extensions import Base

# Import models so MetaData is populated (none yet; added in Chunk 3):
# import solex.models  # noqa

config = context.config
cfg = resolve_config()
config.set_main_option("sqlalchemy.url", cfg.SQLALCHEMY_DATABASE_URI)
if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
