import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_model_loader
from app.schemas.analysis import (
    AnalysisRequest,
    AnalysisResponse,
    EmotionAnalysis,
    MeetingSummary,
    TopicAnalysis,
)
from app.services.analysis_service import AnalysisService
from app.services.model_loader import ModelLoader

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_transcript(
    request: AnalysisRequest,
    db: Session = Depends(get_db),
    model_loader: ModelLoader = Depends(get_model_loader),
):
    try:
        analysis_service = AnalysisService(model_loader, db)
        result = await analysis_service.analyze_transcript(
            transcript=request.transcript,
            meeting_id=request.meeting_id,
            timestamp=request.timestamp,
        )
        return result
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/analyze/emotion", response_model=EmotionAnalysis)
async def analyze_emotion(
    request: AnalysisRequest,
    model_loader: ModelLoader = Depends(get_model_loader),
):
    try:
        analysis_service = AnalysisService(model_loader, None)
        emotions = await analysis_service.analyze_emotions(request.transcript)
        return emotions
    except Exception as e:
        logger.error(f"Emotion analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Emotion analysis failed: {str(e)}")


@router.post("/analyze/topic", response_model=TopicAnalysis)
async def analyze_topic(
    request: AnalysisRequest,
    model_loader: ModelLoader = Depends(get_model_loader),
):
    try:
        analysis_service = AnalysisService(model_loader, None)
        topics = await analysis_service.analyze_topics(request.transcript)
        return topics
    except Exception as e:
        logger.error(f"Topic analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Topic analysis failed: {str(e)}")


@router.post("/analyze/summary", response_model=MeetingSummary)
async def generate_summary(
    request: AnalysisRequest,
    model_loader: ModelLoader = Depends(get_model_loader),
):
    try:
        analysis_service = AnalysisService(model_loader, None)
        summary = await analysis_service.generate_summary(request.transcript)
        return summary
    except Exception as e:
        logger.error(f"Summary generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Summary generation failed: {str(e)}")
