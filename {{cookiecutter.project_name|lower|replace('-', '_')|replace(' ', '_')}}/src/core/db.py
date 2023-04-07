"""
SQLAlchemy async engine and sessions tools

https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
"""

from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.pool import Pool as SQLAlchemyPool

from src.core import config


class AsyncDatabase:
    def __init__(self):
        self.async_engine: AsyncEngine = create_async_engine(
            url=self.set_async_db_uri,
            pool_pre_ping=True,
        )
        self.async_session = async_sessionmaker(
            self.async_engine, expire_on_commit=False
        )
        self.pool: SQLAlchemyPool = self.async_engine.pool

    @property
    def set_async_db_uri(self) -> str | PostgresDsn:
        """
        Set the database uri for the async engine, depending on the environment
        """
        if config.settings.ENVIRONMENT == "PYTEST":
            database_uri = config.settings.TEST_DATABASE_URI
        else:
            database_uri = config.settings.DATABASE_URI

        return database_uri


async_db: AsyncDatabase = AsyncDatabase()
