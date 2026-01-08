from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    meeting_id: str = Field(..., description="Unique identifier for the meeting")
    transcript: str = Field(..., description="Transcript text to analyze")
    timestamp: Optional[datetime] = Field(
        default=None, description="Timestamp of the transcript chunk"
    )


class EmotionScore(BaseModel):
    label: str = Field(..., description="Emotion label (e.g., joy, anger, neutral)")
    score: float = Field(..., ge=0.0, le=1.0, description="Confidence score for the emotion")


class EmotionAnalysis(BaseModel):
    text: str = Field(..., description="Text chunk analyzed")
    emotions: List[EmotionScore] = Field(..., description="List of detected emotions")
    dominant_emotion: str = Field(..., description="Most prominent emotion")
    timestamp: Optional[datetime] = None


class TopicScore(BaseModel):
    topic: str = Field(..., description="Topic label")
    score: float = Field(..., ge=0.0, le=1.0, description="Relevance score")


class TopicAnalysis(BaseModel):
    topics: List[TopicScore] = Field(..., description="Detected topics")
    primary_topic: str = Field(..., description="Main topic of discussion")
    topic_drift_detected: bool = Field(
        default=False, description="Whether topic drift was detected"
    )


class MeetingSummary(BaseModel):
    summary: str = Field(..., description="Generated summary of the meeting")
    key_points: List[str] = Field(default_factory=list, description="Key discussion points")
    conciseness_score: float = Field(
        ..., ge=0.0, le=1.0, description="Ratio of summary length to original length"
    )
    word_count_original: int
    word_count_summary: int


class SpeakerEngagement(BaseModel):
    speaker_id: Optional[str] = None
    word_count: int
    speaking_time_ratio: float
    emotion_variance: float = Field(
        ..., description="Measure of emotional volatility during speaking"
    )


class KeyMoment(BaseModel):
    timestamp: datetime
    description: str
    emotion: str
    importance_score: float = Field(..., ge=0.0, le=1.0)


class AnalysisResponse(BaseModel):
    meeting_id: str
    timestamp: datetime
    emotion_analysis: EmotionAnalysis
    topic_analysis: TopicAnalysis
    summary: Optional[MeetingSummary] = None
    speaker_engagement: Optional[List[SpeakerEngagement]] = None
    key_moments: Optional[List[KeyMoment]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AnalysisResult(BaseModel):
    id: int
    meeting_id: str
    created_at: datetime
    emotion_data: Dict
    topic_data: Dict
    summary_data: Optional[Dict] = None

    class Config:
        from_attributes = True
