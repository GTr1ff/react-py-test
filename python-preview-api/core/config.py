from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    ENV: str = "development"
    DEBUG: bool = False
    DATABASE_URI: str | None = None
    LOG_DIR: str = "logs"
    LOG_LEVEL: str = "WARNING"

settings = Settings()