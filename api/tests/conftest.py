import asyncio

import httpx
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession

from app.conf import settings
from app.main import app
from app.db import get_db


Base = declarative_base()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name="db")
async def db_fixture() -> None:
    engine = create_async_engine(settings.POSTGRES_URI, echo=False, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    test_local_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with test_local_session() as session:
        yield session


@pytest_asyncio.fixture
async def test_client(db):
    app.dependency_overrides[get_db] = lambda: db
    async with httpx.AsyncClient(app=app, base_url="http://127.0.0.0:8000") as test_client:
        yield test_client
    app.dependency_overrides.pop(get_db)
