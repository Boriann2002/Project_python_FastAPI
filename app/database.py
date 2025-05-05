"""
Async database configuration for FastAPI with SQLAlchemy 2.0+
"""

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# URL подключения
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:postgrespassword@db:5432/fitness_db"

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Создаем асинхронный движок
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    """Генератор асинхронных сессий"""
    async with AsyncSessionLocal() as session:
        yield session