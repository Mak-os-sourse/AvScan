from pydantic import PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    TOKEN: str
    DB_URL: PostgresDsn
    PATH_LOGS: Path
    REDIS_URL: RedisDsn
    COEFFICIENT: float
    FAST_COEFFICIENT: float
    HEADLESS: bool
    QUEUE_NAME: str
    
    model_config = SettingsConfigDict(env_file="settings.env")
    
settings = Settings()