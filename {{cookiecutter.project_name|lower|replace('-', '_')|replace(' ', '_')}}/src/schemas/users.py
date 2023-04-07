"""User schemas."""
from pydantic import EmailStr

from .base import BaseRequest, BaseResponse


class UserCreateRequest(BaseRequest):
    email: EmailStr
    password: str


class UserUpdateRequest(BaseRequest):
    email: EmailStr | None = None
    password: str | None = None


class UserResponse(BaseResponse):
    id: str
    email: EmailStr
