from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "URL Shortener Microservice"
    environment: str = Field(default="development", validation_alias="ENV")
    base_counter_seed: int = Field(default=10_000_000, validation_alias="BASE_COUNTER_SEED")
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    log_file_path: str = Field(default="app_errors.log", validation_alias="LOG_FILE_PATH")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
