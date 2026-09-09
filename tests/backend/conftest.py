import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from backend.main import app
from backend.app.db.session import async_engine
from backend.app.db.base import Base
import backend.app.models


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    """Initializes all database tables before test execution."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
