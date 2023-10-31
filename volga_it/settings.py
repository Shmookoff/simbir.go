from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    DATABASE_URI: PostgresDsn

    JWT_ACCESS_SECRET: str
    JWT_ACCESS_TTL_SECONDS: int


settings = Settings.model_validate({})
