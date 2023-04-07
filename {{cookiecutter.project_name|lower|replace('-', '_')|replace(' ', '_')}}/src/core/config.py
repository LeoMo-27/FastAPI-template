"""
File with environment variables and general configuration logic.
`SECRET_KEY`, `ENVIRONMENT` etc. map to env variables with the same names.

For project name, version, description we use pyproject.toml
For the rest, we use file `.env` (gitignored), see `.env.example`

See https://pydantic-docs.helpmanual.io/usage/settings/

Note, complex types like lists are read as json-encoded strings.
"""

from pathlib import Path
from secrets import token_hex
from typing import Literal

import toml
from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator

PROJECT_DIR = Path(__file__).parent.parent.parent
PYPROJECT_CONTENT = toml.load(f"{PROJECT_DIR}/pyproject.toml")["tool"]["poetry"]


class Settings(BaseSettings):
    # CORE SETTINGS
    SECRET_KEY: str = token_hex(32)  # Use an environment variable instead.
    ENVIRONMENT: Literal["DEV", "PYTEST", "STG", "PRD"] = "DEV"
    SECURITY_BCRYPT_ROUNDS: int = 12
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 20160  # 14 days
    ACCESS_TOKEN_EXPIRE: int = ACCESS_TOKEN_EXPIRE_MINUTES * 60
    REFRESH_TOKEN_EXPIRE: int = REFRESH_TOKEN_EXPIRE_MINUTES * 60
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"]

    # PROJECT NAME, VERSION AND DESCRIPTION
    PROJECT_NAME: str = PYPROJECT_CONTENT["name"]
    VERSION: str = PYPROJECT_CONTENT["version"]
    DESCRIPTION: str = PYPROJECT_CONTENT["description"]

    # POSTGRESQL DEFAULT DATABASE
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: str
    DB_NAME: str
    DATABASE_URI: str = ""
    TEST_DATABASE_URI: str = ""

    # See https://docs.pydantic.dev/usage/validators/
    @validator("DATABASE_URI")
    def _assemble_default_db_connection(cls, v: str, values: dict[str, str]) -> str:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values["DB_USER"],
            password=values["DB_PASSWORD"],
            host=values["DB_HOST"],
            port=values["DB_PORT"],
            path=f"/{values['DB_NAME']}",
        )

    # See https://docs.pydantic.dev/usage/validators/
    @validator("TEST_DATABASE_URI")
    def _assemble_test_db_connection(cls, v: str, values: dict[str, str]) -> str:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values["DB_USER"],
            password=values["DB_PASSWORD"],
            host=values["DB_HOST"],
            port=values["DB_PORT"],
            path=f"/{values['DB_NAME']}-test",
        )

    class Config:
        env_file = f"{PROJECT_DIR}/.env"
        case_sensitive = True


settings: Settings = Settings()  # type: ignore
