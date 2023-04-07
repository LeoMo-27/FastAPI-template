"""Password generation and verification tools."""

from passlib.context import CryptContext

from src.core.config import settings


class PasswordGenerator:
    def __init__(self) -> None:
        self.pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
            bcrypt__rounds=settings.SECURITY_BCRYPT_ROUNDS,
        )

    def verify_password(self, plain_password: str, password: str) -> bool:
        """Verifies plain and hashed password matches

        Applies passlib context based on bcrypt algorithm on plain password.
        """
        return self.pwd_context.verify(plain_password, password)

    def get_password_hash(self, password: str) -> str:
        """Creates hash from password

        Applies passlib context based on bcrypt algorithm on plain password.
        """
        return self.pwd_context.hash(password)


password_generator: PasswordGenerator = PasswordGenerator()
