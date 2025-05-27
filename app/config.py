import os
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application configuration settings with MySQL support."""
    
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    JWT_SECRET_KEY: str = Field(
        os.getenv("JWT_SECRET_KEY"),
        description="Secret key for JWT token generation and verification."
    )
    JWT_ALGORITHM: str = Field(
        "HS256",
        description="Algorithm used for JWT token signing."
    )
    JWT_EXPIRE_MINUTES: int = Field(
        30,
        description="Expiration time in minutes for JWT tokens."
    )
    CACHE_EXPIRE_SECONDS: int = Field(
        300,
        description="Cache expiration time in seconds (5 minutes)."
    )
    MAX_POST_SIZE_BYTES: int = Field(
        1024 * 1024,  # 1MB
        description="Maximum allowed size for post content in bytes."
    )

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()