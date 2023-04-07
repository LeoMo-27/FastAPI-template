"""Pytest configuration file.

Used to execute code before running tests, in this case we want to use test database.
"""
import asyncio
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine

from src.core.db import async_db
from src.main import app
from src.models import Base, User

from .utils.test_database import create_database, drop_database
from .utils.test_user import TestUser

TEST_USER = TestUser()
TEST_DATABASE_URL = async_db.set_async_db_uri


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        client.headers.update({"Host": "localhost"})
        yield client


@pytest.fixture(scope="session")
async def database(event_loop):
    await create_database(TEST_DATABASE_URL)

    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

    try:
        yield TEST_DATABASE_URL
    finally:
        await drop_database(TEST_DATABASE_URL)


@pytest.fixture(scope="session")
async def sqla_engine(database):
    async with async_db.async_engine.begin() as conn:
        yield conn


@pytest.fixture(scope="session")
async def db_session(sqla_engine):
    async with async_db.async_session() as session:
        yield session


@pytest_asyncio.fixture
async def default_user(database) -> User:
    async with async_db.async_session() as session:
        result = await session.execute(select(User).where(User.id == TEST_USER.id))
        user = result.scalars().first()
        if user is None:
            new_user = User(
                email=TEST_USER.email,
                password=TEST_USER.password,
            )
            new_user.id = TEST_USER.id
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user
        return user


@pytest.fixture
def default_user_headers(default_user: User):
    return {"Authorization": f"Bearer {TEST_USER.access_token}"}
