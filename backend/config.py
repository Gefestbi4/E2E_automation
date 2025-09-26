from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import datetime, timedelta
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://my_user:my_password@postgres:5432/my_database"
    MONGO_URL: str = "mongodb://my_user:my_password@mongodb:27017/my_database"
    REDIS_URL: str = "redis://redis:6379"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_SECRET_KEY: str = "jwt_secret_key_here"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    API_KEY: str = "test_api_key"
    CORS_ORIGINS: str = '["http://localhost:3000", "http://frontend:80"]'
    LOG_LEVEL: str = "INFO"
    DEBUG: str = "False"
    PORT: str = "5000"
    HOST: str = "0.0.0.0"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
