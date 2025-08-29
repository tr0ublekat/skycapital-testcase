from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base


DATABASE_URL = "sqlite+aiosqlite:///./tasks.db"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncLocalSession = async_sessionmaker(
    bind=engine, expire_on_commit=False, autoflush=False, autocommit=False
)


Base = declarative_base()


async def get_db():
    """Получение сессии базы данных."""

    async with AsyncLocalSession() as session:
        yield session
