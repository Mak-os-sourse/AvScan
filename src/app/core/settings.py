import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv("settings.env")

class Settings:
    TOKEN: str  = os.getenv("TOKEN")
    DB_URL: str = os.getenv("DB_URL")
    CACHE_HOST: str = os.getenv("CACHE_HOST")
    CACHE_PORT: str = os.getenv("CACHE_PORT")
    PATH_LOGS: Path = Path(os.getenv("PATH_LOGS"))
    BROKER_URL: str = os.getenv("BROKER_URL")
    COEFFICIENT: float = float(os.getenv("COEFFICIENT"))
    FAST_COEFFICIENT: float = float(os.getenv("FAST_COEFFICIENT"))
    HEADLESS: bool = bool(os.getenv("HEADLESS"))
    
settings = Settings()