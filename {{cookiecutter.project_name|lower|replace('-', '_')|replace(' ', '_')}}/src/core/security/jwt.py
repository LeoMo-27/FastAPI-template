"""JWT generator used for authentication."""
import time
from typing import Tuple

import jwt

from src.core.config import settings
from src.schemas import AccessTokenResponse


class JWTGenerator:
    def __init__(self) -> None:
        self.jwt_algorithm = "HS256"

    def _generate_jwt_token(
        self, subject: str | int, exp_secs: int, refresh: bool
    ) -> Tuple[str, int, int]:
        """Creates jwt access or refresh token for user.

        Args:
            subject: anything unique to user, id or email etc.
            exp_secs: expire time in seconds
            refresh: if True, this is refresh token
        """

        issued_at = int(time.time())
        expires_at = issued_at + exp_secs

        to_encode: dict[str, int | str | bool] = {
            "issued_at": issued_at,
            "expires_at": expires_at,
            "sub": subject,
            "refresh": refresh,
        }
        encoded_jwt = jwt.encode(
            to_encode,
            key=settings.SECRET_KEY,
            algorithm=self.jwt_algorithm,
        )
        return encoded_jwt, expires_at, issued_at

    def generate_access_token(self, subject: str | int) -> AccessTokenResponse:
        """Generate tokens and return AccessTokenResponse

        Args:
            subject: anything unique to user, id or email etc.
        """

        access_token, expires_at, issued_at = self._generate_jwt_token(
            subject, settings.ACCESS_TOKEN_EXPIRE, refresh=False
        )
        refresh_token, refresh_expires_at, refresh_issued_at = self._generate_jwt_token(
            subject, settings.REFRESH_TOKEN_EXPIRE, refresh=True
        )
        return AccessTokenResponse(
            token_type="Bearer",
            access_token=access_token,
            expires_at=expires_at,
            issued_at=issued_at,
            refresh_token=refresh_token,
            refresh_token_expires_at=refresh_expires_at,
            refresh_token_issued_at=refresh_issued_at,
        )


jwt_generator: JWTGenerator = JWTGenerator()
