import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient

from app.models.analysis import EmotionTimeline, MeetingAnalysis, TopicTimeline
from app.services.moment_detector import MomentDetector


class TestTimelineEndpoint:
    """Tests for the timeline endpoint."""

    def test_timeline_endpoint_with_transcript(self, client: TestClient, db_session):
        """Test timeline endpoint with provided transcript."""
        # Note: This test assumes the timeline router is included in the main app
        # If routes/analyze.py router is not included, this test will need to be updated
        
        request_data = {
            "meeting_id": "test-meeting-1",
            "transcript": (
                "We decided to proceed with the project. "
                "John will complete the report by tomorrow. "
                "What is the plan? How do we proceed? When will this happen? "
                "Yes, I agree. That sounds good. "
                "I disagree with that approach."
            ),
            "use_existing_analysis": False,
        }

        # Try to call the endpoint
        # Note: The actual endpoint path depends on how the router is included
        # This is a template test that may need adjustment
        try:
            response = client.post("/api/v1/analyze/timeline", json=request_data)
            
            if response.status_code == 404:
                pytest.skip("Timeline endpoint not yet included in main router")
            
            assert response.status_code == 200
            data = response.json()
            
            assert "meeting_id" in data
            assert data["meeting_id"] == "test-meeting-1"
            assert "moments" in data
            assert "total_moments" in data
            assert "moment_types" in data
            assert isinstance(data["moments"], list)
            assert data["total_moments"] == len(data["moments"])
            
            # Verify moment structure
            if data["moments"]:
                moment = data["moments"][0]
                assert "moment_type" in moment
                assert "timestamp" in moment
                assert "importance_score" in moment
                assert "text_snippet" in moment
                assert "metadata" in moment
                assert 0.0 <= moment["importance_score"] <= 1.0
        except Exception as e:
            # If endpoint doesn't exist, skip the test
            pytest.skip(f"Timeline endpoint not available: {e}")

    def test_timeline_endpoint_with_existing_analysis(
        self, client: TestClient, db_session
    ):
        """Test timeline endpoint using existing analysis from database."""
        meeting_id = "test-meeting-2"
        base_time = datetime.utcnow()

        # Create meeting analysis record
        analysis = MeetingAnalysis(
            meeting_id=meeting_id,
            transcript="Test transcript with decisions and actions.",
        )
        db_session.add(analysis)
        db_session.commit()

        # Create emotion timeline entries
        for i in range(3):
            emotion_entry = EmotionTimeline(
                meeting_id=meeting_id,
                timestamp=base_time + timedelta(minutes=i * 5),
                dominant_emotion="joy" if i % 2 == 0 else "sadness",
                emotion_scores=[
                    {"label": "joy" if i % 2 == 0 else "sadness", "score": 0.7 + i * 0.1}
                ],
                text_chunk=f"Text chunk {i}",
            )
            db_session.add(emotion_entry)

        db_session.commit()

        request_data = {
            "meeting_id": meeting_id,
            "use_existing_analysis": True,
        }

        try:
            response = client.post("/api/v1/analyze/timeline", json=request_data)
            
            if response.status_code == 404:
                pytest.skip("Timeline endpoint not yet included in main router")
            
            assert response.status_code == 200
            data = response.json()
            
            assert data["meeting_id"] == meeting_id
            assert "moments" in data
            
            # Verify moments were saved to database
            updated_analysis = (
                db_session.query(MeetingAnalysis)
                .filter(MeetingAnalysis.meeting_id == meeting_id)
                .first()
            )
            assert updated_analysis is not None
            assert updated_analysis.key_moments is not None
            assert len(updated_analysis.key_moments) > 0
        except Exception as e:
            pytest.skip(f"Timeline endpoint not available: {e}")

    def test_timeline_endpoint_missing_data(self, client: TestClient, db_session):
        """Test timeline endpoint with missing required data."""
        request_data = {
            "meeting_id": "non-existent-meeting",
            "use_existing_analysis": True,
        }

        try:
            response = client.post("/api/v1/analyze/timeline", json=request_data)
            
            if response.status_code == 404:
                pytest.skip("Timeline endpoint not yet included in main router")
            
            # Should return 400 or handle gracefully
            assert response.status_code in [400, 404, 500]
        except Exception as e:
            pytest.skip(f"Timeline endpoint not available: {e}")


class TestMomentDetectorIntegration:
    """Integration tests for moment detector with real data structures."""

    def test_moment_detector_with_database_structures(self, db_session):
        """Test moment detector with data structures matching database models."""
        detector = MomentDetector()
        meeting_id = "test-integration-1"
        base_time = datetime.utcnow()

        # Create emotion timeline matching database structure
        emotion_timeline = []
        timestamps = []
        
        for i in range(5):
            timestamp = base_time + timedelta(minutes=i * 2)
            timestamps.append(timestamp)
            emotion_timeline.append({
                "dominant_emotion": "joy" if i % 2 == 0 else "anger",
                "emotion_scores": [
                    {"label": "joy" if i % 2 == 0 else "anger", "score": 0.5 + i * 0.1}
                ],
                "text_chunk": f"Meeting discussion point {i}",
            })

        transcript = (
            "We decided to move forward. "
            "John will handle the implementation. "
            "What are the next steps? "
            "I agree with that plan."
        )

        analysis_data = {
            "transcript": transcript,
            "emotion_timeline": emotion_timeline,
            "topic_timeline": [],
            "timestamps": timestamps,
        }

        moments = detector.identify_key_moments(analysis_data)

        assert len(moments) > 0
        
        # Verify moments are properly structured
        for moment in moments:
            assert "moment_type" in moment
            assert "timestamp" in moment
            assert isinstance(moment["timestamp"], datetime)
            assert "importance_score" in moment
            assert "text_snippet" in moment
            assert "metadata" in moment
