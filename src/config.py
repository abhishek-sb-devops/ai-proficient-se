from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration management via Pydantic Environment Settings."""

    app_name: str = "Scalable URL Shortener API"
    environment: str = Field(default="development", env="ENV")
    base_counter_seed: int = Field(default=10_000_000, env="BASE_COUNTER_SEED")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file_path: str = Field(default="app_errors.log", env="LOG_FILE_PATH")

    class Config:
        env_file = ".env"


settings = Settings()