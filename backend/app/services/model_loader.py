import logging
import os
from typing import Any, Dict, Optional

import torch
from transformers import pipeline

from app.core.config import settings

logger = logging.getLogger(__name__)


class ModelLoader:
    def __init__(self):
        self.emotion_pipeline: Optional[Any] = None
        self.topic_pipeline: Optional[Any] = None
        self.summary_pipeline: Optional[Any] = None
        self.device = self._get_device()
        self._ensure_cache_dir()

    def _get_device(self) -> str:
        if settings.MODEL_DEVICE == "auto":
            return "cuda" if torch.cuda.is_available() else "cpu"
        return settings.MODEL_DEVICE

    def _ensure_cache_dir(self):
        os.makedirs(settings.HUGGINGFACE_CACHE_DIR, exist_ok=True)

    async def load_all_models(self):
        logger.info(f"Loading models on device: {self.device}")

        os.environ["TRANSFORMERS_CACHE"] = settings.HUGGINGFACE_CACHE_DIR
        os.environ["HF_HOME"] = settings.HUGGINGFACE_CACHE_DIR

        try:
            logger.info("Loading emotion analysis model...")
            self.emotion_pipeline = pipeline(
                "text-classification",
                model=settings.EMOTION_MODEL_NAME,
                device=self.device,
                top_k=None,
            )
            logger.info("Emotion model loaded successfully")

            logger.info("Loading topic classification model...")
            self.topic_pipeline = pipeline(
                "zero-shot-classification",
                model=settings.TOPIC_MODEL_NAME,
                device=self.device,
            )
            logger.info("Topic model loaded successfully")

            logger.info("Loading summarization model...")
            self.summary_pipeline = pipeline(
                "summarization",
                model=settings.SUMMARY_MODEL_NAME,
                device=self.device,
            )
            logger.info("Summary model loaded successfully")

        except Exception as e:
            logger.error(f"Error loading models: {e}")
            raise

    def get_emotion_pipeline(self):
        if self.emotion_pipeline is None:
            raise RuntimeError("Emotion model not loaded")
        return self.emotion_pipeline

    def get_topic_pipeline(self):
        if self.topic_pipeline is None:
            raise RuntimeError("Topic model not loaded")
        return self.topic_pipeline

    def get_summary_pipeline(self):
        if self.summary_pipeline is None:
            raise RuntimeError("Summary model not loaded")
        return self.summary_pipeline

    def cleanup(self):
        logger.info("Cleaning up models")
        self.emotion_pipeline = None
        self.topic_pipeline = None
        self.summary_pipeline = None
        if self.device == "cuda":
            torch.cuda.empty_cache()
