
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost/db"
    TELEGRAM_BOT_TOKEN: str = "your_telegram_bot_token"
    TELEGRAM_CHAT_ID: str = "your_telegram_chat_id"
    SENTRY_DSN: str | None = None
    REDIS_URL: str = "redis://localhost"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
