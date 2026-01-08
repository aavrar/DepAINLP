from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="allow")

    ENVIRONMENT: str = "development"

    DATABASE_URL: str = Field(
        default="postgresql://postgres:password@localhost:5432/meet_analytics"
    )
    DATABASE_ECHO: bool = False

    HUGGINGFACE_CACHE_DIR: str = "./models/cache"
    MODEL_DEVICE: str = "cpu"

    CORS_ORIGINS: List[str] = ["http://localhost:3000", "chrome-extension://*"]

    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Google Meet Analytics API"
    DEBUG: bool = True

    LOG_LEVEL: str = "INFO"

    EMOTION_MODEL_NAME: str = "SamLowe/roberta-base-go_emotions"
    TOPIC_MODEL_NAME: str = "facebook/bart-large-mnli"
    SUMMARY_MODEL_NAME: str = "facebook/bart-large-cnn"


settings = Settings()
