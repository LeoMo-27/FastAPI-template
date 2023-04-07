from httpx import AsyncClient

from src.main import app
from src.models import User
from src.tests.conftest import TEST_USER


async def test_auth_access_token(client: AsyncClient, default_user: User):
    response = await client.post(
        app.url_path_for("login_access_token"),
        data={
            "username": TEST_USER.email,
            "password": TEST_USER.unhashed_password,
        },
    )
    assert response.status_code == 200
    token = response.json()
    assert token["token_type"] == "Bearer"
    assert "access_token" in token
    assert "expires_at" in token
    assert "issued_at" in token
    assert "refresh_token" in token
    assert "refresh_token_expires_at" in token
    assert "refresh_token_issued_at" in token


async def test_auth_access_token_fail_no_user(client: AsyncClient):
    response = await client.post(
        app.url_path_for("login_access_token"),
        data={
            "username": "xxx",
            "password": "yyy",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found."}


async def test_auth_refresh_token(client: AsyncClient, default_user: User):
    response = await client.post(
        app.url_path_for("login_access_token"),
        data={
            "username": TEST_USER.email,
            "password": TEST_USER.unhashed_password,
        },
    )
    refresh_token = response.json()["refresh_token"]

    new_token_response = await client.post(
        app.url_path_for("refresh_token"), json={"refresh_token": refresh_token}
    )
    assert new_token_response.status_code == 200
    token = new_token_response.json()
    assert token["token_type"] == "Bearer"
    assert "access_token" in token
    assert "expires_at" in token
    assert "issued_at" in token
    assert "refresh_token" in token
    assert "refresh_token_expires_at" in token
    assert "refresh_token_issued_at" in token
