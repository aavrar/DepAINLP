# API Documentation

Base URL: `http://localhost:8000/api/v1`

## Authentication

Currently no authentication required. Will be added in future iterations.

## Request/Response Format

All requests and responses use JSON format.

## Common Headers

```
Content-Type: application/json
```

## Endpoints

### 1. Full Transcript Analysis

Performs comprehensive analysis including emotion, topic, and summary.

**Endpoint:** `POST /analyze`

**Request Body:**
```json
{
  "meeting_id": "meet-abc-123",
  "transcript": "The meeting transcript text here...",
  "timestamp": "2024-01-15T10:30:00Z"  // Optional
}
```

**Response:** `200 OK`
```json
{
  "meeting_id": "meet-abc-123",
  "timestamp": "2024-01-15T10:30:00Z",
  "emotion_analysis": {
    "text": "The meeting transcript text here...",
    "emotions": [
      {
        "label": "neutral",
        "score": 0.75
      },
      {
        "label": "optimism",
        "score": 0.15
      }
    ],
    "dominant_emotion": "neutral",
    "timestamp": "2024-01-15T10:30:00Z"
  },
  "topic_analysis": {
    "topics": [
      {
        "topic": "technical discussion",
        "score": 0.85
      },
      {
        "topic": "project planning",
        "score": 0.65
      }
    ],
    "primary_topic": "technical discussion",
    "topic_drift_detected": false
  },
  "summary": {
    "summary": "Brief summary of the meeting...",
    "key_points": [
      "First key point",
      "Second key point"
    ],
    "conciseness_score": 0.15,
    "word_count_original": 500,
    "word_count_summary": 75
  },
  "metadata": {
    "transcript_length": 2500,
    "word_count": 500
  }
}
```

### 2. Emotion Analysis Only

Analyzes emotions/sentiment in the transcript.

**Endpoint:** `POST /analyze/emotion`

**Request Body:**
```json
{
  "meeting_id": "meet-abc-123",
  "transcript": "I'm really excited about this new feature!"
}
```

**Response:** `200 OK`
```json
{
  "text": "I'm really excited about this new feature!",
  "emotions": [
    {
      "label": "joy",
      "score": 0.92
    },
    {
      "label": "excitement",
      "score": 0.78
    },
    {
      "label": "optimism",
      "score": 0.65
    }
  ],
  "dominant_emotion": "joy",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Emotion Labels:**
The model can detect 28 emotions including:
- admiration, amusement, anger, annoyance, approval
- caring, confusion, curiosity, desire, disappointment
- disapproval, disgust, embarrassment, excitement, fear
- gratitude, grief, joy, love, nervousness
- optimism, pride, realization, relief, remorse
- sadness, surprise, neutral

### 3. Topic Classification

Classifies the main topics discussed in the transcript.

**Endpoint:** `POST /analyze/topic`

**Request Body:**
```json
{
  "meeting_id": "meet-abc-123",
  "transcript": "We need to discuss the database schema and API endpoints for the new feature."
}
```

**Response:** `200 OK`
```json
{
  "topics": [
    {
      "topic": "technical discussion",
      "score": 0.95
    },
    {
      "topic": "product development",
      "score": 0.78
    },
    {
      "topic": "project planning",
      "score": 0.45
    }
  ],
  "primary_topic": "technical discussion",
  "topic_drift_detected": false
}
```

**Default Topic Categories:**
- project planning
- technical discussion
- business strategy
- team management
- product development
- customer feedback
- budget and finance
- marketing
- general discussion

### 4. Meeting Summary

Generates a concise summary of the meeting.

**Endpoint:** `POST /analyze/summary`

**Request Body:**
```json
{
  "meeting_id": "meet-abc-123",
  "transcript": "Long meeting transcript with multiple discussion points..."
}
```

**Response:** `200 OK`
```json
{
  "summary": "The team discussed new feature implementation, focusing on database design and API development. Key decisions were made regarding authentication and data storage.",
  "key_points": [
    "The team discussed new feature implementation, focusing on database design and API development",
    "Key decisions were made regarding authentication and data storage"
  ],
  "conciseness_score": 0.12,
  "word_count_original": 450,
  "word_count_summary": 54
}
```

## Error Responses

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "transcript"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Analysis failed: Model not loaded"
}
```

## Rate Limiting

Currently no rate limiting. Will be added in production.

## Pagination

Not applicable for current endpoints. Will be added for future list endpoints.

## Best Practices

1. **Transcript Size**: Keep transcripts under 10,000 words for optimal performance
2. **Meeting ID**: Use unique, descriptive meeting IDs (e.g., "meet-2024-01-15-standup")
3. **Timestamps**: Always include timestamps for better analytics tracking
4. **Error Handling**: Implement retry logic with exponential backoff
5. **Chunking**: For very long meetings, send transcripts in chunks with the same meeting_id

## Response Times

Typical response times (depends on hardware):

- Emotion analysis: 1-3 seconds
- Topic classification: 2-4 seconds
- Summarization: 3-6 seconds
- Full analysis: 5-10 seconds

Times increase with transcript length and decrease with GPU acceleration.

## Example Integration

### JavaScript/TypeScript

```javascript
async function analyzeMeeting(meetingId, transcript) {
  const response = await fetch('http://localhost:8000/api/v1/analyze', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      meeting_id: meetingId,
      transcript: transcript,
      timestamp: new Date().toISOString()
    })
  });

  if (!response.ok) {
    throw new Error(`Analysis failed: ${response.statusText}`);
  }

  return await response.json();
}
```

### Python

```python
import httpx

async def analyze_meeting(meeting_id: str, transcript: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/analyze",
            json={
                "meeting_id": meeting_id,
                "transcript": transcript
            }
        )
        response.raise_for_status()
        return response.json()
```

## Websocket Support

Not currently supported. May be added for real-time streaming analysis.

## Versioning

API is currently at v1. Breaking changes will be released as v2, v3, etc.
