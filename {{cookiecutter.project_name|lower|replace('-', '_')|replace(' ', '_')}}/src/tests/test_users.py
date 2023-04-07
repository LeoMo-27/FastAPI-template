from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.main import app
from src.models import User
from src.tests.conftest import TEST_USER


async def test_get_current_user(client: AsyncClient, default_user_headers):
    response = await client.get(
        app.url_path_for("read_current_user"), headers=default_user_headers
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": TEST_USER.id,
        "email": TEST_USER.email,
    }


async def test_delete_current_user(
    client: AsyncClient, default_user_headers, default_user, db_session: AsyncSession
):
    response = await client.delete(
        app.url_path_for("delete_user", id=default_user.id),
        headers=default_user_headers,
    )
    assert response.status_code == 204
    result = await db_session.execute(select(User).where(User.id == TEST_USER.id))
    user = result.scalars().first()
    assert user is None


async def test_update_current_user(
    client: AsyncClient, default_user_headers, default_user, db_session: AsyncSession
):
    response = await client.patch(
        app.url_path_for("update_user", id=default_user.id),
        headers=default_user_headers,
        json={"email": "new_test_email@test.com"},
    )
    assert response.status_code == 200
    result = await db_session.execute(select(User).where(User.id == TEST_USER.id))
    user = result.scalars().first()
    assert user is not None
    assert user.email != TEST_USER.email


async def test_register_new_user(
    client: AsyncClient, default_user_headers, db_session: AsyncSession
):
    response = await client.post(
        app.url_path_for("register_new_user"),
        headers=default_user_headers,
        json={
            "email": "new_user@test.com",
            "password": "another_password",
        },
    )
    assert response.status_code == 201
    result = await db_session.execute(
        select(User).where(User.email == "new_user@test.com")
    )
    user = result.scalars().first()
    assert user is not None
