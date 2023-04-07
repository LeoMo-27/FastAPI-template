from random import randint
from uuid import uuid4

from src.core.security.jwt import jwt_generator
from src.core.security.password import password_generator


class TestUser:
    id: str = str(uuid4())
    email: str = f"test_{randint(0, 10)}@test.com"
    unhashed_password: str = f"testing_user_{randint(0, 10)}"
    password: str = password_generator.get_password_hash(unhashed_password)
    access_token = jwt_generator._generate_jwt_token(
        str(id), 60 * 60 * 24, refresh=False
    )[0]
