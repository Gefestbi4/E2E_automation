"""
Конфигурация для тестов с PostgreSQL
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import datetime, timedelta
from typing import Optional


class TestSettings(BaseSettings):
    # Используем PostgreSQL для тестов - значения по умолчанию
    DATABASE_URL: str = "postgresql://my_user:my_password@localhost:5432/test_database"
    MONGO_URL: str = "mongodb://my_user:my_password@localhost:27017/test_database"
    REDIS_URL: str = "redis://localhost:6379"

    # Security - значения по умолчанию
    SECRET_KEY: str = "test-secret-key"
    JWT_SECRET_KEY: str = "test_jwt_secret_key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1
    API_KEY: str = "test_api_key"

    # CORS - значения по умолчанию
    CORS_ORIGINS: str = '["http://localhost:3000", "http://frontend:80"]'

    # Application - значения по умолчанию
    LOG_LEVEL: str = "DEBUG"
    DEBUG: str = "True"
    PORT: str = "5000"
    HOST: str = "0.0.0.0"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


test_settings = TestSettings()
