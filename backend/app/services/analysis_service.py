import logging
from datetime import datetime
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from app.models.analysis import EmotionTimeline, MeetingAnalysis, TopicTimeline
from app.schemas.analysis import (
    AnalysisResponse,
    EmotionAnalysis,
    EmotionScore,
    KeyMoment,
    MeetingSummary,
    TopicAnalysis,
    TopicScore,
)
from app.services.model_loader import ModelLoader
from app.utils.preprocessing import PreprocessingUtils

logger = logging.getLogger(__name__)


class AnalysisService:
    def __init__(self, model_loader: ModelLoader, db: Optional[Session] = None):
        self.model_loader = model_loader
        self.db = db
        self.preprocessing = PreprocessingUtils()

    async def analyze_emotions(self, text: str) -> EmotionAnalysis:
        try:
            chunks = self.preprocessing.chunk_text(text, max_length=512)
            emotion_pipeline = self.model_loader.get_emotion_pipeline()

            all_emotions = []
            for chunk in chunks:
                if not chunk.strip():
                    continue
                result = emotion_pipeline(chunk)
                all_emotions.extend(result[0])

            aggregated_emotions = self._aggregate_emotions(all_emotions)
            dominant_emotion = max(aggregated_emotions, key=lambda x: x["score"])

            emotion_scores = [
                EmotionScore(label=e["label"], score=e["score"]) for e in aggregated_emotions[:5]
            ]

            return EmotionAnalysis(
                text=text,
                emotions=emotion_scores,
                dominant_emotion=dominant_emotion["label"],
                timestamp=datetime.utcnow(),
            )

        except Exception as e:
            logger.error(f"Emotion analysis failed: {e}")
            raise

    async def analyze_topics(
        self, text: str, candidate_labels: Optional[List[str]] = None
    ) -> TopicAnalysis:
        try:
            if candidate_labels is None:
                candidate_labels = [
                    "project planning",
                    "technical discussion",
                    "business strategy",
                    "team management",
                    "product development",
                    "customer feedback",
                    "budget and finance",
                    "marketing",
                    "general discussion",
                ]

            topic_pipeline = self.model_loader.get_topic_pipeline()
            cleaned_text = self.preprocessing.clean_text(text)

            result = topic_pipeline(cleaned_text, candidate_labels)

            topic_scores = [
                TopicScore(topic=label, score=score)
                for label, score in zip(result["labels"], result["scores"])
            ]

            return TopicAnalysis(
                topics=topic_scores,
                primary_topic=result["labels"][0],
                topic_drift_detected=False,
            )

        except Exception as e:
            logger.error(f"Topic analysis failed: {e}")
            raise

    async def generate_summary(self, text: str) -> MeetingSummary:
        try:
            summary_pipeline = self.model_loader.get_summary_pipeline()
            cleaned_text = self.preprocessing.clean_text(text)

            max_length = min(len(cleaned_text.split()), 150)
            min_length = min(max_length // 2, 30)

            result = summary_pipeline(
                cleaned_text, max_length=max_length, min_length=min_length, do_sample=False
            )

            summary_text = result[0]["summary_text"]
            original_words = len(cleaned_text.split())
            summary_words = len(summary_text.split())

            key_points = self._extract_key_points(summary_text)

            conciseness_score = summary_words / original_words if original_words > 0 else 0.0

            return MeetingSummary(
                summary=summary_text,
                key_points=key_points,
                conciseness_score=conciseness_score,
                word_count_original=original_words,
                word_count_summary=summary_words,
            )

        except Exception as e:
            logger.error(f"Summary generation failed: {e}")
            raise

    async def analyze_transcript(
        self, transcript: str, meeting_id: str, timestamp: Optional[datetime] = None
    ) -> AnalysisResponse:
        try:
            timestamp = timestamp or datetime.utcnow()

            emotion_analysis = await self.analyze_emotions(transcript)
            topic_analysis = await self.analyze_topics(transcript)

            summary = None
            if len(transcript.split()) > 50:
                summary = await self.generate_summary(transcript)

            if self.db:
                self._save_to_database(
                    meeting_id, transcript, emotion_analysis, topic_analysis, summary
                )

            return AnalysisResponse(
                meeting_id=meeting_id,
                timestamp=timestamp,
                emotion_analysis=emotion_analysis,
                topic_analysis=topic_analysis,
                summary=summary,
                metadata={
                    "transcript_length": len(transcript),
                    "word_count": len(transcript.split()),
                },
            )

        except Exception as e:
            logger.error(f"Full transcript analysis failed: {e}")
            raise

    def _aggregate_emotions(self, emotions: List[Dict]) -> List[Dict]:
        emotion_totals = {}
        for emotion in emotions:
            label = emotion["label"]
            score = emotion["score"]
            if label in emotion_totals:
                emotion_totals[label] += score
            else:
                emotion_totals[label] = score

        count = len(emotions)
        averaged = [
            {"label": label, "score": total / count} for label, total in emotion_totals.items()
        ]

        return sorted(averaged, key=lambda x: x["score"], reverse=True)

    def _extract_key_points(self, summary: str) -> List[str]:
        sentences = [s.strip() for s in summary.split(".") if s.strip()]
        return sentences[:3]

    def _save_to_database(
        self,
        meeting_id: str,
        transcript: str,
        emotion_analysis: EmotionAnalysis,
        topic_analysis: TopicAnalysis,
        summary: Optional[MeetingSummary],
    ):
        try:
            analysis_record = MeetingAnalysis(
                meeting_id=meeting_id,
                transcript=transcript,
                emotion_data={
                    "dominant_emotion": emotion_analysis.dominant_emotion,
                    "emotions": [e.dict() for e in emotion_analysis.emotions],
                },
                topic_data={
                    "primary_topic": topic_analysis.primary_topic,
                    "topics": [t.dict() for t in topic_analysis.topics],
                },
                summary_data=summary.dict() if summary else None,
            )
            self.db.add(analysis_record)

            emotion_timeline = EmotionTimeline(
                meeting_id=meeting_id,
                timestamp=datetime.utcnow(),
                dominant_emotion=emotion_analysis.dominant_emotion,
                emotion_scores=[e.dict() for e in emotion_analysis.emotions],
                text_chunk=transcript[:500],
            )
            self.db.add(emotion_timeline)

            topic_timeline = TopicTimeline(
                meeting_id=meeting_id,
                timestamp=datetime.utcnow(),
                primary_topic=topic_analysis.primary_topic,
                topic_scores=[t.dict() for t in topic_analysis.topics],
            )
            self.db.add(topic_timeline)

            self.db.commit()
            logger.info(f"Saved analysis for meeting {meeting_id}")

        except Exception as e:
            logger.error(f"Failed to save to database: {e}")
            self.db.rollback()
            raise
