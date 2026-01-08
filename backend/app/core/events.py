import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.services.model_loader import ModelLoader

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.PROJECT_NAME}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")

    logger.info("Loading ML models...")
    model_loader = ModelLoader()

    try:
        await model_loader.load_all_models()
        app.state.model_loader = model_loader
        logger.info("All models loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load models: {e}")
        raise

    yield

    logger.info("Shutting down application")
    if hasattr(app.state, "model_loader"):
        app.state.model_loader.cleanup()
