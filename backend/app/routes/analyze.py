import logging
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.analysis import EmotionTimeline, MeetingAnalysis, TopicTimeline
from app.schemas.analysis import TimelineMoment, TimelineRequest, TimelineResponse
from app.services.moment_detector import MomentDetector

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/timeline", response_model=TimelineResponse)
async def get_timeline(
    request: TimelineRequest,
    db: Session = Depends(get_db),
):
    """
    Generate a chronological timeline of key moments from a meeting.

    This endpoint analyzes meeting transcripts and emotion/topic timelines
    to identify important moments such as:
    - Emotional peaks and valleys
    - Decision-making language
    - Action items
    - Question clusters
    - Agreement/disagreement spikes
    - Sentiment changes

    The moments are stored in the database and returned in chronological order.
    """
    try:
        moment_detector = MomentDetector()

        # Try to get existing analysis from database
        analysis_record: Optional[MeetingAnalysis] = None
        if request.use_existing_analysis:
            analysis_record = (
                db.query(MeetingAnalysis)
                .filter(MeetingAnalysis.meeting_id == request.meeting_id)
                .first()
            )

        # Prepare analysis data
        analysis_data = {}

        if analysis_record:
            # Use existing analysis
            analysis_data["transcript"] = analysis_record.transcript
            analysis_data["emotion_timeline"] = []
            analysis_data["topic_timeline"] = []
            analysis_data["timestamps"] = []

            # Get emotion timeline entries
            emotion_entries = (
                db.query(EmotionTimeline)
                .filter(EmotionTimeline.meeting_id == request.meeting_id)
                .order_by(EmotionTimeline.timestamp)
                .all()
            )

            for entry in emotion_entries:
                analysis_data["emotion_timeline"].append(
                    {
                        "dominant_emotion": entry.dominant_emotion,
                        "emotion_scores": entry.emotion_scores,
                        "text_chunk": entry.text_chunk,
                    }
                )
                analysis_data["timestamps"].append(entry.timestamp)

            # Get topic timeline entries
            topic_entries = (
                db.query(TopicTimeline)
                .filter(TopicTimeline.meeting_id == request.meeting_id)
                .order_by(TopicTimeline.timestamp)
                .all()
            )

            for entry in topic_entries:
                analysis_data["topic_timeline"].append(
                    {
                        "primary_topic": entry.primary_topic,
                        "topic_scores": entry.topic_scores,
                    }
                )

            # If no timestamps from emotion timeline, create default ones
            if not analysis_data["timestamps"]:
                analysis_data["timestamps"] = [
                    datetime.utcnow() for _ in range(len(analysis_data["emotion_timeline"]))
                ]

        elif request.transcript:
            # Use provided transcript (minimal analysis)
            analysis_data["transcript"] = request.transcript
            analysis_data["emotion_timeline"] = []
            analysis_data["topic_timeline"] = []
            analysis_data["timestamps"] = [datetime.utcnow()]
        else:
            raise HTTPException(
                status_code=400,
                detail="Either use_existing_analysis must be True with existing data, or transcript must be provided",
            )

        # Detect key moments
        moments = moment_detector.identify_key_moments(analysis_data)

        # Convert to TimelineMoment objects
        timeline_moments = [
            TimelineMoment(
                moment_type=m["moment_type"],
                timestamp=m["timestamp"],
                importance_score=m["importance_score"],
                text_snippet=m["text_snippet"],
                metadata=m.get("metadata", {}),
            )
            for m in moments
        ]

        # Count moment types
        moment_types = {}
        for moment in timeline_moments:
            moment_type = moment.moment_type
            moment_types[moment_type] = moment_types.get(moment_type, 0) + 1

        # Save moments to database
        if analysis_record:
            # Update existing record
            analysis_record.key_moments = [
                {
                    "moment_type": m.moment_type,
                    "timestamp": m.timestamp.isoformat(),
                    "importance_score": m.importance_score,
                    "text_snippet": m.text_snippet,
                    "metadata": m.metadata,
                }
                for m in timeline_moments
            ]
            db.commit()
            logger.info(f"Updated key moments for meeting {request.meeting_id}")
        else:
            # Create new record if transcript was provided
            if request.transcript:
                new_analysis = MeetingAnalysis(
                    meeting_id=request.meeting_id,
                    transcript=request.transcript,
                    key_moments=[
                        {
                            "moment_type": m.moment_type,
                            "timestamp": m.timestamp.isoformat(),
                            "importance_score": m.importance_score,
                            "text_snippet": m.text_snippet,
                            "metadata": m.metadata,
                        }
                        for m in timeline_moments
                    ],
                )
                db.add(new_analysis)
                db.commit()
                logger.info(f"Created new analysis with key moments for meeting {request.meeting_id}")

        return TimelineResponse(
            meeting_id=request.meeting_id,
            moments=timeline_moments,
            total_moments=len(timeline_moments),
            moment_types=moment_types,
            created_at=datetime.utcnow(),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Timeline generation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Timeline generation failed: {str(e)}")
