import time

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError

from src.api.dependencies import get_controller
from src.controllers import UserController
from src.core import config
from src.core.security.jwt import jwt_generator
from src.core.security.password import password_generator
from src.schemas import AccessTokenResponse, JWTTokenPayload, RefreshTokenRequest

router = APIRouter()


@router.post("/access-token", response_model=AccessTokenResponse)
async def login_access_token(
    controller: UserController = Depends(get_controller(UserController)),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """OAuth2 compatible token, get an access token for future requests using username and password"""

    user = await controller.get_user_by_attribute(
        attribute="email", value=form_data.username
    )

    if not password_generator.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    return jwt_generator.generate_access_token(str(user.id))


@router.post("/refresh-token", response_model=AccessTokenResponse)
async def refresh_token(
    input: RefreshTokenRequest,
    controller: UserController = Depends(get_controller(UserController)),
):
    """OAuth2 compatible token, get an access token for future requests using refresh token"""
    try:
        payload = jwt.decode(
            input.refresh_token,
            config.settings.SECRET_KEY,
            algorithms=[jwt_generator.jwt_algorithm],
        )
    except (jwt.DecodeError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, unknown error",
        )

    token_data = JWTTokenPayload(**payload)

    if not token_data.refresh:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, cannot use access token",
        )
    now = int(time.time())
    if now < token_data.issued_at or now > token_data.expires_at:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, token expired or not yet valid",
        )

    user = await controller.get_user_by_attribute(attribute="id", value=token_data.sub)

    return jwt_generator.generate_access_token(str(user.id))
