"""Dependency functions for the API."""
import time
from collections.abc import AsyncGenerator
from typing import Callable, Type

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.controllers import BaseController, UserController
from src.core import config
from src.core.db import async_db
from src.core.security.jwt import jwt_generator
from src.models import User
from src.schemas import JWTTokenPayload

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="auth/access-token")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_db.async_session() as session:
        yield session


def get_controller(
    controller_class: Type[BaseController],
) -> Callable[[AsyncSession], BaseController]:
    def _get_controller(session: AsyncSession = Depends(get_session)) -> BaseController:
        return controller_class(session)

    return _get_controller


async def get_current_user(
    token: str = Depends(reusable_oauth2),
    controller: UserController = Depends(get_controller(UserController)),
) -> User:
    """Get current user based on the information in the access token
    This function is used as a dependency for all routes that require authentication.
    """
    try:
        payload = jwt.decode(
            token, config.settings.SECRET_KEY, algorithms=[jwt_generator.jwt_algorithm]
        )
    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials.",
        )
    # JWT guarantees payload will be unchanged (and thus valid), no errors here
    token_data = JWTTokenPayload(**payload)

    if token_data.refresh:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, cannot use refresh token",
        )
    now = int(time.time())
    if now < token_data.issued_at or now > token_data.expires_at:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, token expired or not yet valid",
        )

    user = await controller.get_user_by_attribute(attribute="id", value=token_data.sub)
    return user
