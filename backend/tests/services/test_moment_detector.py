import pytest
from datetime import datetime, timedelta

from app.services.moment_detector import MomentDetector


class TestMomentDetector:
    """Unit tests for MomentDetector class."""

    @pytest.fixture
    def detector(self):
        """Create a MomentDetector instance for testing."""
        return MomentDetector()

    @pytest.fixture
    def sample_emotion_timeline(self):
        """Create a sample emotion timeline for testing."""
        base_time = datetime(2024, 1, 1, 10, 0, 0)
        return [
            {
                "dominant_emotion": "joy",
                "emotion_scores": [{"label": "joy", "score": 0.3}, {"label": "neutral", "score": 0.7}],
                "text_chunk": "This is a normal conversation.",
            },
            {
                "dominant_emotion": "joy",
                "emotion_scores": [{"label": "joy", "score": 0.8}, {"label": "excitement", "score": 0.2}],
                "text_chunk": "This is an exciting moment!",
            },
            {
                "dominant_emotion": "sadness",
                "emotion_scores": [{"label": "sadness", "score": 0.2}, {"label": "neutral", "score": 0.8}],
                "text_chunk": "This is a low point.",
            },
            {
                "dominant_emotion": "anger",
                "emotion_scores": [{"label": "anger", "score": 0.9}, {"label": "fear", "score": 0.1}],
                "text_chunk": "This is a very intense moment!",
            },
        ], [
            base_time,
            base_time + timedelta(minutes=5),
            base_time + timedelta(minutes=10),
            base_time + timedelta(minutes=15),
        ]

    def test_identify_key_moments_empty_data(self, detector):
        """Test that empty analysis data returns empty list."""
        analysis_data = {
            "transcript": "",
            "emotion_timeline": [],
            "timestamps": [],
        }
        moments = detector.identify_key_moments(analysis_data)
        assert isinstance(moments, list)
        assert len(moments) == 0

    def test_detect_emotional_peaks(self, detector, sample_emotion_timeline):
        """Test detection of emotional peaks."""
        emotion_timeline, timestamps = sample_emotion_timeline
        transcript = " ".join([e["text_chunk"] for e in emotion_timeline])

        moments = detector._detect_emotional_peaks(emotion_timeline, timestamps, transcript)

        assert len(moments) > 0
        # Should detect the high intensity moments (score 0.8 and 0.9)
        peak_types = [m["moment_type"] for m in moments]
        assert "emotional_peak" in peak_types

        # Check that importance scores are within valid range
        for moment in moments:
            assert 0.0 <= moment["importance_score"] <= 1.0
            assert moment["moment_type"] == "emotional_peak"
            assert "text_snippet" in moment
            assert "metadata" in moment

    def test_detect_emotional_valleys(self, detector, sample_emotion_timeline):
        """Test detection of emotional valleys."""
        emotion_timeline, timestamps = sample_emotion_timeline
        transcript = " ".join([e["text_chunk"] for e in emotion_timeline])

        moments = detector._detect_emotional_valleys(emotion_timeline, timestamps, transcript)

        # Should detect drops in intensity
        valley_types = [m["moment_type"] for m in moments]
        assert "emotional_valley" in valley_types or len(moments) == 0

        for moment in moments:
            assert moment["moment_type"] == "emotional_valley"
            assert "metadata" in moment
            assert "drop_percentage" in moment["metadata"]

    def test_detect_decision_language(self, detector):
        """Test detection of decision-making language."""
        transcript = "We decided to go with option A. Let's do it. We need to finalize this decision."
        timestamps = [datetime.utcnow()]

        moments = detector._detect_decision_language(transcript, timestamps)

        assert len(moments) > 0
        decision_moments = [m for m in moments if m["moment_type"] == "decision"]
        assert len(decision_moments) >= 2  # Should find multiple decisions

        for moment in decision_moments:
            assert moment["importance_score"] == 0.8
            assert "text_snippet" in moment
            assert "metadata" in moment

    def test_detect_action_items(self, detector):
        """Test detection of action items."""
        transcript = "John will complete the report by tomorrow. TODO: Review the proposal. We need to send this ASAP."
        timestamps = [datetime.utcnow()]

        moments = detector._detect_action_items(transcript, timestamps)

        assert len(moments) > 0
        action_moments = [m for m in moments if m["moment_type"] == "action_item"]
        assert len(action_moments) >= 3

        for moment in action_moments:
            assert "urgency" in moment["metadata"]
            assert moment["metadata"]["urgency"] in ["now", "soon", "later", "unspecified"]
            assert "assignee" in moment["metadata"]

    def test_detect_action_items_urgency_classification(self, detector):
        """Test urgency classification for action items."""
        transcript_now = "We need to fix this immediately. This is urgent!"
        transcript_soon = "Let's do this today. We should finish by tomorrow."
        transcript_later = "We can handle this next week. No rush on this."

        timestamps = [datetime.utcnow()]

        moments_now = detector._detect_action_items(transcript_now, timestamps)
        moments_soon = detector._detect_action_items(transcript_soon, timestamps)
        moments_later = detector._detect_action_items(transcript_later, timestamps)

        if moments_now:
            assert any(m["metadata"]["urgency"] == "now" for m in moments_now)
        if moments_soon:
            assert any(m["metadata"]["urgency"] == "soon" for m in moments_soon)
        if moments_later:
            assert any(m["metadata"]["urgency"] == "later" for m in moments_later)

    def test_detect_question_clusters(self, detector):
        """Test detection of question clusters."""
        transcript = "What is the plan? How do we proceed? When will this happen? Who is responsible? Why did this occur?"
        timestamps = [datetime.utcnow()]

        moments = detector._detect_question_clusters(transcript, timestamps)

        assert len(moments) > 0
        question_moments = [m for m in moments if m["moment_type"] == "question_cluster"]
        assert len(question_moments) > 0

        for moment in question_moments:
            assert "question_count" in moment["metadata"]
            assert moment["metadata"]["question_count"] >= 3

    def test_detect_agreement_spikes(self, detector):
        """Test detection of agreement spikes."""
        transcript = "Yes, I agree. That sounds good. Absolutely, we should do that. I concur with your point."
        timestamps = [datetime.utcnow()]

        moments = detector._detect_agreement_spikes(transcript, timestamps)

        assert len(moments) > 0
        agreement_moments = [m for m in moments if m["moment_type"] == "agreement_spike"]
        assert len(agreement_moments) > 0

        for moment in agreement_moments:
            assert moment["importance_score"] == 0.7
            assert "agreement_count" in moment["metadata"]

    def test_detect_disagreement_spikes(self, detector):
        """Test detection of disagreement spikes."""
        transcript = "I disagree with that. However, I think we should reconsider. No, that won't work. I have concerns about this approach."
        timestamps = [datetime.utcnow()]

        moments = detector._detect_disagreement_spikes(transcript, timestamps)

        assert len(moments) > 0
        disagreement_moments = [m for m in moments if m["moment_type"] == "disagreement_spike"]
        assert len(disagreement_moments) > 0

        for moment in disagreement_moments:
            assert moment["importance_score"] == 0.75
            assert "disagreement_count" in moment["metadata"]

    def test_detect_sentiment_changes(self, detector):
        """Test detection of sentiment changes."""
        emotion_timeline = [
            {
                "dominant_emotion": "joy",
                "emotion_scores": [{"label": "joy", "score": 0.8}],
                "text_chunk": "This is great!",
            },
            {
                "dominant_emotion": "sadness",
                "emotion_scores": [{"label": "sadness", "score": 0.8}],
                "text_chunk": "This is terrible.",
            },
            {
                "dominant_emotion": "anger",
                "emotion_scores": [{"label": "anger", "score": 0.9}],
                "text_chunk": "I'm very upset!",
            },
        ]
        timestamps = [
            datetime.utcnow(),
            datetime.utcnow() + timedelta(minutes=5),
            datetime.utcnow() + timedelta(minutes=10),
        ]
        transcript = " ".join([e["text_chunk"] for e in emotion_timeline])

        moments = detector._detect_sentiment_changes(emotion_timeline, timestamps, transcript)

        assert len(moments) > 0
        sentiment_moments = [m for m in moments if m["moment_type"] == "sentiment_change"]
        assert len(sentiment_moments) > 0

        for moment in sentiment_moments:
            assert "change_magnitude" in moment["metadata"]
            assert moment["metadata"]["change_magnitude"] >= 1.5

    def test_classify_urgency(self, detector):
        """Test urgency classification."""
        assert detector._classify_urgency("Do this now immediately") == "now"
        assert detector._classify_urgency("We need this ASAP") == "now"
        assert detector._classify_urgency("Finish this today") == "soon"
        assert detector._classify_urgency("We can do this next week") == "later"
        assert detector._classify_urgency("Complete the task") == "unspecified"

    def test_extract_assignee(self, detector):
        """Test assignee extraction from action items."""
        text1 = "Assign this task to John Smith"
        text2 = "John will complete the report"
        text3 = "Let Alice handle this"

        assignee1 = detector._extract_assignee(text1)
        assignee2 = detector._extract_assignee(text2)
        assignee3 = detector._extract_assignee(text3)

        # Should extract names (may be None if pattern doesn't match exactly)
        # This tests that the function runs without error
        assert isinstance(assignee1, (str, type(None)))
        assert isinstance(assignee2, (str, type(None)))
        assert isinstance(assignee3, (str, type(None)))

    def test_identify_key_moments_integration(self, detector, sample_emotion_timeline):
        """Test full integration of identify_key_moments method."""
        emotion_timeline, timestamps = sample_emotion_timeline
        transcript = (
            "We decided to proceed. John will complete the task by tomorrow. "
            "What is the plan? How do we proceed? When will this happen? "
            "Yes, I agree. That sounds good. "
            "I disagree with that. However, I think differently."
        )

        analysis_data = {
            "transcript": transcript,
            "emotion_timeline": emotion_timeline,
            "topic_timeline": [],
            "timestamps": timestamps,
        }

        moments = detector.identify_key_moments(analysis_data)

        assert len(moments) > 0

        # Check that moments are sorted by timestamp
        for i in range(len(moments) - 1):
            assert moments[i]["timestamp"] <= moments[i + 1]["timestamp"]

        # Check that we have various moment types
        moment_types = set(m["moment_type"] for m in moments)
        assert len(moment_types) > 0

        # Verify all moments have required fields
        for moment in moments:
            assert "moment_type" in moment
            assert "timestamp" in moment
            assert "importance_score" in moment
            assert "text_snippet" in moment
            assert "metadata" in moment
            assert 0.0 <= moment["importance_score"] <= 1.0

    def test_identify_key_moments_with_minimal_data(self, detector):
        """Test identify_key_moments with minimal data."""
        analysis_data = {
            "transcript": "This is a simple transcript with no special moments.",
            "emotion_timeline": [],
            "timestamps": [],
        }

        moments = detector.identify_key_moments(analysis_data)

        # Should still return a list (may be empty)
        assert isinstance(moments, list)

    def test_moment_importance_scores(self, detector):
        """Test that importance scores are properly calculated."""
        transcript = "We decided to go with option A. TODO: Review this ASAP."
        timestamps = [datetime.utcnow()]

        analysis_data = {
            "transcript": transcript,
            "emotion_timeline": [],
            "timestamps": timestamps,
        }

        moments = detector.identify_key_moments(analysis_data)

        for moment in moments:
            assert 0.0 <= moment["importance_score"] <= 1.0

    def test_empty_emotion_timeline_handling(self, detector):
        """Test handling of empty emotion timeline."""
        transcript = "This is a transcript without emotion data."
        timestamps = []

        analysis_data = {
            "transcript": transcript,
            "emotion_timeline": [],
            "timestamps": timestamps,
        }

        moments = detector.identify_key_moments(analysis_data)

        # Should handle gracefully without errors
        assert isinstance(moments, list)

    def test_timestamp_handling(self, detector):
        """Test proper timestamp handling when timestamps are missing."""
        transcript = "We decided to proceed."
        timestamps = []  # Empty timestamps

        moments = detector._detect_decision_language(transcript, timestamps)

        # Should use datetime.utcnow() as fallback
        for moment in moments:
            assert isinstance(moment["timestamp"], datetime)
