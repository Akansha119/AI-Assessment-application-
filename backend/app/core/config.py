"""AssessIQ application configuration."""
from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "assessiq"
    app_env: str = Field(default="development", alias="APP_ENV")
    app_debug: bool = Field(default=True, alias="APP_DEBUG")
    secret_key: str = Field(default="change-me-in-production", alias="APP_SECRET_KEY")

    # Database
    database_url: str = Field(
        default="postgresql+psycopg://assessiq:assessiq@localhost:5432/assessiq",
        alias="DATABASE_URL",
    )

    # Security / JWT
    jwt_secret_key: str = Field(default="change-me-jwt-secret", alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    jwt_access_token_expire_minutes: int = Field(
        default=15, alias="JWT_ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    jwt_refresh_token_expire_days: int = Field(
        default=7, alias="JWT_REFRESH_TOKEN_EXPIRE_DAYS"
    )

    # Redis / Celery
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    celery_broker_url: str = Field(
        default="redis://localhost:6379/0", alias="CELERY_BROKER_URL"
    )
    celery_result_backend: str = Field(
        default="redis://localhost:6379/0", alias="CELERY_RESULT_BACKEND"
    )

    # AI provider (provider-independent)
    ai_provider: str = Field(default="mock", alias="AI_PROVIDER")
    ai_provider_api_key: str = Field(default="", alias="AI_PROVIDER_API_KEY")
    ai_provider_base_url: str = Field(default="", alias="AI_PROVIDER_BASE_URL")
    ai_model_default: str = Field(default="gpt-4o-mini", alias="AI_MODEL_DEFAULT")
    ai_temperature: float = Field(default=0.3, alias="AI_TEMPERATURE")
    ai_max_tokens: int = Field(default=2000, alias="AI_MAX_TOKENS")
    ai_rate_limit_per_min: int = Field(default=20, alias="AI_RATE_LIMIT_PER_MIN")

    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost:3000"], alias="CORS_ORIGINS"
    )

    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_format: str = Field(default="json", alias="LOG_FORMAT")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
