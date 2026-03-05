from pydantic import Field, field_validator, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables and .env file.

    Priority (highest to lowest):
    1. Environment variables (from shell, Docker, K8s)
    2. .env file
    3. Default values
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # App settings
    app_env: Literal["development", "staging", "production", "test"] = Field(
        default="development",
        description="Application environment"
    )
    app_port: int = Field(
        default=8000,
        gt=0,
        lt=65536,
        description="Port to run the application on"
    )
    debug: bool = Field(
        default=False,
        description="Enable debug mode"
    )

    # Database
    database_url: PostgresDsn = Field(
        ...,  # Required field
        description="PostgreSQL database connection URL"
    )

    # Security
    secret_key: str = Field(
        ...,  # Required
        min_length=32,
        description="Secret key for JWT/sessions (min 32 chars)"
    )

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Ensure secret key is not a default value."""
        if v in ("change-me", "super-secret"):
            raise ValueError(
                "SECRET_KEY must be changed from default value. "
                "Generate with: python -c 'import secrets; print(secrets.token_urlsafe(32))'"
            )
        return v

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.app_env == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.app_env == "development"


# Singleton instance - loaded once at startup
settings = Settings()