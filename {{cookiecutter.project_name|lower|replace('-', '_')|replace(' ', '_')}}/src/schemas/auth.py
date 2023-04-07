"""Auth schemas."""
from .base import BaseRequest, BaseResponse


class RefreshTokenRequest(BaseRequest):
    refresh_token: str


class AccessTokenResponse(BaseResponse):
    token_type: str
    access_token: str
    expires_at: int
    issued_at: int
    refresh_token: str
    refresh_token_expires_at: int
    refresh_token_issued_at: int


class JWTTokenPayload(BaseRequest):
    sub: str
    refresh: bool
    issued_at: int
    expires_at: int
