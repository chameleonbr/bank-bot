import os
from pathlib import Path
from pydantic_settings import BaseSettings

# Absolute path to the .env in the agent root (two levels up from this file)
_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    BACKEND_URL: str = "http://localhost:8000"
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    REDIS_URL: str = "redis://localhost:6379/0"
    OPENAI_API_KEY: str = ""
    ENVIRONMENT: str = "development"

    model_config = {"env_file": str(_ENV_FILE), "extra": "ignore"}


settings = Settings()

# Sync critical keys into os.environ so third-party libs (e.g. agno/openai) can find them
if settings.OPENAI_API_KEY:
    os.environ.setdefault("OPENAI_API_KEY", settings.OPENAI_API_KEY)
