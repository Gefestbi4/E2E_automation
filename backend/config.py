from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import datetime, timedelta
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://my_user:my_password@postgres:5432/my_database"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()