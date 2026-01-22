import logging
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class MomentDetector:
    """Detects important moments in meeting transcripts based on emotional patterns,
    decision language, action items, and other key indicators.
    """

    # Decision language patterns
    DECISION_PATTERNS = [
        r"\b(?:we|let's|let us|we'll|we will|we should|we need to|we must)\s+(?:decide|decided|deciding|decision)",
        r"\b(?:decide|decided|deciding|decision)\s+(?:to|on|that|whether)",
        r"\b(?:let's|let us)\s+(?:do|go|make|choose|pick|select)",
        r"\b(?:we|I|they)\s+(?:decided|agreed|chose|selected|picked)",
        r"\b(?:final|finalize|finalized|conclusion|conclude)",
        r"\b(?:settle|settled|settling)\s+(?:on|for|with)",
    ]

    # Action item patterns
    ACTION_PATTERNS = [
        r"\b(?:TODO|todo|TBD|tbd|action item|action items)",
        r"\b(?:will|shall|should|must|need to|going to)\s+(?:do|complete|finish|implement|deliver|send|create|make)",
        r"\b(?:assign|assigned|assignment)\s+(?:to|for)",
        r"\b(?:by|deadline|due)\s+(?:tomorrow|next week|end of|EOD|EOB|ASAP|asap)",
        r"\b(?:follow up|follow-up|followup)\s+(?:on|with|about)",
    ]

    # Agreement patterns
    AGREEMENT_PATTERNS = [
        r"\b(?:agree|agreed|agreement|agrees)\b",
        r"\b(?:yes|yeah|yep|yup|sure|absolutely|definitely|exactly|right|correct)\b",
        r"\b(?:I|we)\s+(?:agree|concur|approve|accept|support)\b",
        r"\b(?:sounds good|sounds great|that works|that's fine|that's good)\b",
        r"\b(?:consensus|unanimous|unanimously)\b",
    ]

    # Disagreement patterns
    DISAGREEMENT_PATTERNS = [
        r"\b(?:disagree|disagreed|disagreement|disagrees)\b",
        r"\b(?:no|nope|nah|not really|I don't think|I disagree|I don't agree)\b",
        r"\b(?:but|however|although|though|on the other hand|contrary)\b",
        r"\b(?:object|objection|oppose|opposed|against)\b",
        r"\b(?:concern|concerned|worried|issue|problem|conflict)\b",
    ]

    # Question patterns
    QUESTION_PATTERNS = [
        r"\?",
        r"\b(?:what|when|where|who|why|how|which|whose|whom)\s+",
        r"\b(?:can|could|would|should|will|shall|may|might)\s+(?:you|we|they|I|it)\s+",
        r"\b(?:is|are|was|were|do|does|did|have|has|had)\s+(?:there|it|this|that|he|she|they)\s+",
    ]

    # Urgency keywords
    URGENCY_NOW = ["now", "immediately", "right away", "asap", "urgent", "critical", "emergency"]
    URGENCY_SOON = ["soon", "today", "this week", "by tomorrow", "quickly", "promptly"]
    URGENCY_LATER = ["later", "next week", "eventually", "when possible", "no rush"]

    def __init__(self):
        """Initialize the MomentDetector with compiled regex patterns."""
        self.decision_regex = re.compile(
            "|".join(self.DECISION_PATTERNS), re.IGNORECASE | re.MULTILINE
        )
        self.action_regex = re.compile(
            "|".join(self.ACTION_PATTERNS), re.IGNORECASE | re.MULTILINE
        )
        self.agreement_regex = re.compile(
            "|".join(self.AGREEMENT_PATTERNS), re.IGNORECASE | re.MULTILINE
        )
        self.disagreement_regex = re.compile(
            "|".join(self.DISAGREEMENT_PATTERNS), re.IGNORECASE | re.MULTILINE
        )
        self.question_regex = re.compile(
            "|".join(self.QUESTION_PATTERNS), re.IGNORECASE | re.MULTILINE
        )

    def identify_key_moments(self, analysis_data: Dict) -> List[Dict]:
        """
        Identify key moments from analysis data.

        Args:
            analysis_data: Dictionary containing:
                - transcript: str (full transcript text)
                - emotion_timeline: List[Dict] (list of emotion analysis with timestamps)
                - topic_timeline: Optional[List[Dict]] (list of topic analysis)
                - timestamps: Optional[List[datetime]] (timestamps for each chunk)

        Returns:
            List of moment dictionaries with:
                - moment_type: str
                - timestamp: datetime
                - importance_score: float
                - text_snippet: str
                - metadata: Dict
        """
        moments = []

        transcript = analysis_data.get("transcript", "")
        emotion_timeline = analysis_data.get("emotion_timeline", [])
        topic_timeline = analysis_data.get("topic_timeline", [])
        timestamps = analysis_data.get("timestamps", [])

        # Detect emotional peaks and valleys
        moments.extend(self._detect_emotional_peaks(emotion_timeline, timestamps, transcript))
        moments.extend(self._detect_emotional_valleys(emotion_timeline, timestamps, transcript))

        # Detect decision language
        moments.extend(self._detect_decision_language(transcript, timestamps))

        # Detect action items
        moments.extend(self._detect_action_items(transcript, timestamps))

        # Detect question clusters
        moments.extend(self._detect_question_clusters(transcript, timestamps))

        # Detect agreement/disagreement spikes
        moments.extend(self._detect_agreement_spikes(transcript, timestamps))
        moments.extend(self._detect_disagreement_spikes(transcript, timestamps))

        # Detect sentiment pattern changes
        moments.extend(self._detect_sentiment_changes(emotion_timeline, timestamps, transcript))

        # Sort by timestamp and importance score
        moments.sort(key=lambda x: (x["timestamp"], -x["importance_score"]))

        return moments

    def _detect_emotional_peaks(
        self, emotion_timeline: List[Dict], timestamps: List[datetime], transcript: str
    ) -> List[Dict]:
        """Detect moments with high intensity emotions."""
        moments = []

        if not emotion_timeline:
            return moments

        # Calculate average emotion intensity
        intensities = []
        for entry in emotion_timeline:
            if isinstance(entry, dict):
                emotion_scores = entry.get("emotion_scores", [])
                if isinstance(emotion_scores, list) and emotion_scores:
                    # Get max score as intensity
                    max_score = max(
                        (e.get("score", 0) if isinstance(e, dict) else 0 for e in emotion_scores),
                        default=0,
                    )
                    intensities.append(max_score)

        if not intensities:
            return moments

        avg_intensity = sum(intensities) / len(intensities)
        threshold = avg_intensity * 1.5  # 50% above average

        for i, entry in enumerate(emotion_timeline):
            if isinstance(entry, dict):
                emotion_scores = entry.get("emotion_scores", [])
                if emotion_scores:
                    max_score = max(
                        (
                            e.get("score", 0) if isinstance(e, dict) else 0
                            for e in emotion_scores
                        ),
                        default=0,
                    )

                    if max_score >= threshold:
                        timestamp = (
                            timestamps[i] if i < len(timestamps) else datetime.utcnow()
                        )
                        text_chunk = entry.get("text_chunk", "")
                        dominant_emotion = entry.get("dominant_emotion", "unknown")

                        moments.append(
                            {
                                "moment_type": "emotional_peak",
                                "timestamp": timestamp,
                                "importance_score": min(max_score * 1.2, 1.0),
                                "text_snippet": text_chunk[:200] if text_chunk else "",
                                "metadata": {
                                    "dominant_emotion": dominant_emotion,
                                    "intensity": max_score,
                                    "threshold": threshold,
                                },
                            }
                        )

        return moments

    def _detect_emotional_valleys(
        self, emotion_timeline: List[Dict], timestamps: List[datetime], transcript: str
    ) -> List[Dict]:
        """Detect moments with sudden drops in emotion intensity."""
        moments = []

        if len(emotion_timeline) < 2:
            return moments

        # Calculate intensities
        intensities = []
        for entry in emotion_timeline:
            if isinstance(entry, dict):
                emotion_scores = entry.get("emotion_scores", [])
                if emotion_scores:
                    max_score = max(
                        (
                            e.get("score", 0) if isinstance(e, dict) else 0
                            for e in emotion_scores
                        ),
                        default=0,
                    )
                    intensities.append(max_score)
                else:
                    intensities.append(0)

        # Detect sudden drops (more than 40% decrease)
        for i in range(1, len(intensities)):
            if intensities[i - 1] > 0.3 and intensities[i] < intensities[i - 1] * 0.6:
                timestamp = timestamps[i] if i < len(timestamps) else datetime.utcnow()
                entry = emotion_timeline[i]
                text_chunk = entry.get("text_chunk", "") if isinstance(entry, dict) else ""

                moments.append(
                    {
                        "moment_type": "emotional_valley",
                        "timestamp": timestamp,
                        "importance_score": 0.6,
                        "text_snippet": text_chunk[:200] if text_chunk else "",
                        "metadata": {
                            "previous_intensity": intensities[i - 1],
                            "current_intensity": intensities[i],
                            "drop_percentage": (intensities[i - 1] - intensities[i])
                            / intensities[i - 1]
                            * 100,
                        },
                    }
                )

        return moments

    def _detect_decision_language(
        self, transcript: str, timestamps: List[datetime]
    ) -> List[Dict]:
        """Detect decision-making language in transcript."""
        moments = []

        # Split transcript into sentences
        sentences = re.split(r"[.!?]+", transcript)
        current_pos = 0

        for i, sentence in enumerate(sentences):
            if self.decision_regex.search(sentence):
                # Estimate timestamp (if available, use proportional positioning)
                timestamp = datetime.utcnow()
                if timestamps:
                    progress = current_pos / len(transcript) if transcript else 0
                    idx = min(int(progress * len(timestamps)), len(timestamps) - 1)
                    timestamp = timestamps[idx]

                moments.append(
                    {
                        "moment_type": "decision",
                        "timestamp": timestamp,
                        "importance_score": 0.8,
                        "text_snippet": sentence.strip()[:200],
                        "metadata": {
                            "sentence_index": i,
                            "matched_pattern": "decision_language",
                        },
                    }
                )

            current_pos += len(sentence) + 1

        return moments

    def _detect_action_items(
        self, transcript: str, timestamps: List[datetime]
    ) -> List[Dict]:
        """Detect action items and extract assignment details."""
        moments = []

        # Split into sentences
        sentences = re.split(r"[.!?]+", transcript)
        current_pos = 0

        for i, sentence in enumerate(sentences):
            if self.action_regex.search(sentence):
                # Extract urgency
                urgency = self._classify_urgency(sentence)

                # Try to extract assignee
                assignee = self._extract_assignee(sentence)

                # Estimate timestamp
                timestamp = datetime.utcnow()
                if timestamps:
                    progress = current_pos / len(transcript) if transcript else 0
                    idx = min(int(progress * len(timestamps)), len(timestamps) - 1)
                    timestamp = timestamps[idx]

                moments.append(
                    {
                        "moment_type": "action_item",
                        "timestamp": timestamp,
                        "importance_score": 0.85 if urgency == "now" else 0.7,
                        "text_snippet": sentence.strip()[:200],
                        "metadata": {
                            "urgency": urgency,
                            "assignee": assignee,
                            "sentence_index": i,
                        },
                    }
                )

            current_pos += len(sentence) + 1

        return moments

    def _detect_question_clusters(
        self, transcript: str, timestamps: List[datetime]
    ) -> List[Dict]:
        """Detect clusters of questions (high question density)."""
        moments = []

        # Split into sentences
        sentences = re.split(r"[.!?]+", transcript)
        window_size = 5  # Check 5 sentences at a time
        current_pos = 0

        for i in range(len(sentences) - window_size + 1):
            window = sentences[i : i + window_size]
            question_count = sum(1 for s in window if self.question_regex.search(s))

            # If 3 or more questions in 5 sentences, it's a cluster
            if question_count >= 3:
                cluster_text = " ".join(window[:3])  # First 3 sentences
                timestamp = datetime.utcnow()
                if timestamps:
                    progress = current_pos / len(transcript) if transcript else 0
                    idx = min(int(progress * len(timestamps)), len(timestamps) - 1)
                    timestamp = timestamps[idx]

                moments.append(
                    {
                        "moment_type": "question_cluster",
                        "timestamp": timestamp,
                        "importance_score": min(0.5 + (question_count / 10), 0.9),
                        "text_snippet": cluster_text.strip()[:200],
                        "metadata": {
                            "question_count": question_count,
                            "window_size": window_size,
                            "start_index": i,
                        },
                    }
                )

            current_pos += len(sentences[i]) + 1

        return moments

    def _detect_agreement_spikes(
        self, transcript: str, timestamps: List[datetime]
    ) -> List[Dict]:
        """Detect spikes in agreement language."""
        moments = []

        sentences = re.split(r"[.!?]+", transcript)
        window_size = 3
        current_pos = 0

        for i in range(len(sentences) - window_size + 1):
            window = sentences[i : i + window_size]
            agreement_count = sum(1 for s in window if self.agreement_regex.search(s))

            if agreement_count >= 2:  # 2+ agreements in 3 sentences
                cluster_text = " ".join(window)
                timestamp = datetime.utcnow()
                if timestamps:
                    progress = current_pos / len(transcript) if transcript else 0
                    idx = min(int(progress * len(timestamps)), len(timestamps) - 1)
                    timestamp = timestamps[idx]

                moments.append(
                    {
                        "moment_type": "agreement_spike",
                        "timestamp": timestamp,
                        "importance_score": 0.7,
                        "text_snippet": cluster_text.strip()[:200],
                        "metadata": {
                            "agreement_count": agreement_count,
                            "start_index": i,
                        },
                    }
                )

            current_pos += len(sentences[i]) + 1

        return moments

    def _detect_disagreement_spikes(
        self, transcript: str, timestamps: List[datetime]
    ) -> List[Dict]:
        """Detect spikes in disagreement language."""
        moments = []

        sentences = re.split(r"[.!?]+", transcript)
        window_size = 3
        current_pos = 0

        for i in range(len(sentences) - window_size + 1):
            window = sentences[i : i + window_size]
            disagreement_count = sum(
                1 for s in window if self.disagreement_regex.search(s)
            )

            if disagreement_count >= 2:  # 2+ disagreements in 3 sentences
                cluster_text = " ".join(window)
                timestamp = datetime.utcnow()
                if timestamps:
                    progress = current_pos / len(transcript) if transcript else 0
                    idx = min(int(progress * len(timestamps)), len(timestamps) - 1)
                    timestamp = timestamps[idx]

                moments.append(
                    {
                        "moment_type": "disagreement_spike",
                        "timestamp": timestamp,
                        "importance_score": 0.75,  # Disagreements often more important
                        "text_snippet": cluster_text.strip()[:200],
                        "metadata": {
                            "disagreement_count": disagreement_count,
                            "start_index": i,
                        },
                    }
                )

            current_pos += len(sentences[i]) + 1

        return moments

    def _detect_sentiment_changes(
        self, emotion_timeline: List[Dict], timestamps: List[datetime], transcript: str
    ) -> List[Dict]:
        """Detect sudden sentiment/emotion changes and contradictory emotions."""
        moments = []

        if len(emotion_timeline) < 2:
            return moments

        # Map emotions to sentiment scores (positive/negative)
        emotion_sentiment_map = {
            "joy": 1.0,
            "happiness": 1.0,
            "excitement": 1.0,
            "sadness": -1.0,
            "anger": -1.0,
            "fear": -1.0,
            "disgust": -1.0,
            "neutral": 0.0,
        }

        sentiments = []
        for entry in emotion_timeline:
            if isinstance(entry, dict):
                dominant = entry.get("dominant_emotion", "neutral").lower()
                sentiment = emotion_sentiment_map.get(dominant, 0.0)
                sentiments.append(sentiment)

        # Detect sudden changes (flip from positive to negative or vice versa)
        for i in range(1, len(sentiments)):
            if abs(sentiments[i] - sentiments[i - 1]) >= 1.5:  # Significant change
                timestamp = timestamps[i] if i < len(timestamps) else datetime.utcnow()
                entry = emotion_timeline[i]
                text_chunk = entry.get("text_chunk", "") if isinstance(entry, dict) else ""

                moments.append(
                    {
                        "moment_type": "sentiment_change",
                        "timestamp": timestamp,
                        "importance_score": 0.8,
                        "text_snippet": text_chunk[:200] if text_chunk else "",
                        "metadata": {
                            "previous_sentiment": sentiments[i - 1],
                            "current_sentiment": sentiments[i],
                            "change_magnitude": abs(sentiments[i] - sentiments[i - 1]),
                        },
                    }
                )

        return moments

    def _classify_urgency(self, text: str) -> str:
        """Classify urgency level of action item."""
        text_lower = text.lower()

        for keyword in self.URGENCY_NOW:
            if keyword in text_lower:
                return "now"

        for keyword in self.URGENCY_SOON:
            if keyword in text_lower:
                return "soon"

        for keyword in self.URGENCY_LATER:
            if keyword in text_lower:
                return "later"

        return "unspecified"

    def _extract_assignee(self, text: str) -> Optional[str]:
        """Extract assignee from action item text."""
        # Patterns to find assignees
        patterns = [
            r"(?:assign|assigned|for|to)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
            r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+(?:will|should|must|needs to)",
            r"(?:let|have)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+",
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)

        return None
