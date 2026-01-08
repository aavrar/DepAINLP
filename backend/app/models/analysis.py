from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MeetingAnalysis(Base):
    __tablename__ = "meeting_analysis"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    meeting_id = Column(String(255), index=True, nullable=False)
    transcript = Column(Text, nullable=False)

    emotion_data = Column(JSON, nullable=True)
    topic_data = Column(JSON, nullable=True)
    summary_data = Column(JSON, nullable=True)
    engagement_data = Column(JSON, nullable=True)
    key_moments = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<MeetingAnalysis(id={self.id}, meeting_id={self.meeting_id})>"


class EmotionTimeline(Base):
    __tablename__ = "emotion_timeline"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    meeting_id = Column(String(255), index=True, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    dominant_emotion = Column(String(50), nullable=False)
    emotion_scores = Column(JSON, nullable=False)
    text_chunk = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<EmotionTimeline(meeting_id={self.meeting_id}, emotion={self.dominant_emotion})>"


class TopicTimeline(Base):
    __tablename__ = "topic_timeline"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    meeting_id = Column(String(255), index=True, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    primary_topic = Column(String(255), nullable=False)
    topic_scores = Column(JSON, nullable=False)
    drift_detected = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<TopicTimeline(meeting_id={self.meeting_id}, topic={self.primary_topic})>"
