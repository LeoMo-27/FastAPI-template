from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine

from src.core import config

DEFAULT_DB = config.settings.DB_NAME


async def create_database(url: str):
    """Create the test database if it doesn't exist yet.
    In case it does exist, drop it and create it again.
    """
    url_object = make_url(url)
    database_name = url_object.database
    dbms_url = url_object.set(database=DEFAULT_DB)
    engine = create_async_engine(dbms_url, isolation_level="AUTOCOMMIT")

    async with engine.connect() as conn:
        result = await conn.execute(
            text(f"SELECT 1 FROM pg_database WHERE datname='{database_name}'")
        )
        database_exists = result.scalar() == 1

    if database_exists:
        await drop_database(str(url_object))

    async with engine.connect() as conn:
        await conn.execute(
            text(
                f'CREATE DATABASE "{database_name}" ENCODING "utf8" TEMPLATE template1'
            )
        )
    await engine.dispose()


async def drop_database(url: str):
    """Helper function to drop a database.
    This is used to drop the test database after the tests are done.
    """
    url_object = make_url(url)
    dbms_url = url_object.set(database=DEFAULT_DB)
    engine = create_async_engine(dbms_url, isolation_level="AUTOCOMMIT")
    async with engine.connect() as conn:
        disc_users = """
        SELECT pg_terminate_backend(pg_stat_activity.%(pid_column)s)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = '%(database)s'
          AND %(pid_column)s <> pg_backend_pid();
        """ % {
            "pid_column": "pid",
            "database": url_object.database,
        }
        await conn.execute(text(disc_users))

        await conn.execute(text(f'DROP DATABASE "{url_object.database}"'))
