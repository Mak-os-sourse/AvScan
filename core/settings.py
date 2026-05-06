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
    
settings = Settings()