from collections.abc import AsyncGenerator

from backend.app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

# Determine connection arguments based on database dialect (PostgreSQL vs SQLite)
is_sqlite = settings.DATABASE_URL.startswith("sqlite")
connect_args = {"check_same_thread": False} if is_sqlite else {}

# Async Engine for FastAPI route handlers
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
    connect_args=connect_args,
)

# Async Session Factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Sync Engine for Migrations, CLI utilities, and test scripts
sync_connect_args = {"check_same_thread": False} if settings.DATABASE_SYNC_URL.startswith("sqlite") else {}
sync_engine = create_engine(
    settings.DATABASE_SYNC_URL,
    echo=False,
    connect_args=sync_connect_args,
)

SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency yielding an async database session per request."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def get_sync_db() -> Session:
    """Provides a standalone synchronous database session for scripts and CLI tasks."""
    return SyncSessionLocal()
