
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

# Базовый класс для моделей SQLAlchemy
Base = declarative_base()

# Настройка подключения к БД (URL берётся из переменных окружения)
SQLALCHEMY_DATABASE_URL= "postgresql+asyncpg://postgres:postgrespassword@db:5432/fitness_db"

# Асинхронный движок SQLAlchemy
engine: AsyncEngine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Фабрика сессий
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_async_session() -> AsyncSession:
    """Генератор асинхронных сессий для Dependency Injection в FastAPI."""
    async with async_session_maker() as session:
        yield session