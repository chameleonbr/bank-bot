from pathlib import Path
from pydantic_settings import BaseSettings

# Absolute path to the .env in the backend root (two levels up from this file)
_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "sqlite:///./finbank.db"
    ENVIRONMENT: str = "development"

    model_config = {"env_file": str(_ENV_FILE), "extra": "ignore"}


settings = Settings()
