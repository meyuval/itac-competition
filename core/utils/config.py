from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    base_url: str = "https://arena.itac.co.il"
    api_base: str = "https://arena.itac.co.il/api/public/v1"
    fan_email: str = ""
    fan_password: str = ""
    fan_api_key: str = ""
    organization_api_key: str = ""
    api_key_header: str = "X-API-Key"
    default_timeout_ms: int = 15000
    ssl_verify: bool = True
    log_level: str = "INFO"

settings = Settings()
