from logging.config import fileConfig
from alembic import context
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
import sys
import os

sys.path.append(os.getcwd())

from app.database import Base, SQLALCHEMY_DATABASE_URL

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url").replace("+asyncpg", "")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    """Run migrations using async engine."""
    connectable = create_async_engine(SQLALCHEMY_DATABASE_URL)

    async with connectable.connect() as connection:
        # Получаем синхронное соединение через run_sync
        def sync_migration(conn):
            context.configure(
                connection=conn,
                target_metadata=target_metadata
            )
            with context.begin_transaction():
                context.run_migrations()

        await connection.run_sync(sync_migration)


def run_migrations_online():
    """Run migrations in 'online' mode."""
    if SQLALCHEMY_DATABASE_URL.startswith("postgresql+asyncpg"):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(run_async_migrations())
        finally:
            loop.close()
    else:
        from sqlalchemy import engine_from_config
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy."
        )
        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata
            )
            with context.begin_transaction():
                context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()