# Google Meet Analytics - Backend API

FastAPI-based backend service for analyzing Google Meet transcripts using HuggingFace transformer models.

## Features

- Real-time emotion/sentiment analysis using RoBERTa
- Topic classification and drift detection using BART
- Meeting summarization with conciseness metrics
- PostgreSQL database for storing analysis results
- RESTful API with automatic documentation
- Docker support for easy deployment
- Comprehensive test suite

## Tech Stack

- FastAPI 0.109.0
- Python 3.11
- PostgreSQL 15
- HuggingFace Transformers
- SQLAlchemy 2.0
- Docker & Docker Compose

## Project Structure

```
backend/
├── app/
│   ├── api/              # API routes and dependencies
│   ├── core/             # Configuration and startup events
│   ├── db/               # Database setup
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic (model loader, analysis)
│   ├── utils/            # Utility functions
│   └── main.py           # Application entry point
├── tests/                # Test suite
├── alembic/              # Database migrations
├── scripts/              # Utility scripts
├── requirements.txt      # Python dependencies
├── Dockerfile            # Production Docker image
├── docker-compose.yml    # Local development setup
└── .env.example          # Environment variables template
```

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+ (or use Docker Compose)
- 4GB+ RAM for model loading

### Local Development Setup

1. Clone the repository and navigate to backend:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Start PostgreSQL (using Docker):
```bash
docker-compose up db -d
```

6. Initialize database:
```bash
python scripts/init_db.py
```

7. Run the development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Docker Development

Run everything with Docker Compose:

```bash
docker-compose up
```

This starts both PostgreSQL and the API server with hot-reload enabled.

## Model Information

The backend uses three HuggingFace models:

1. **Emotion Analysis**: `SamLowe/roberta-base-go_emotions`
   - 28 emotion classifications
   - ~500MB model size

2. **Topic Classification**: `facebook/bart-large-mnli`
   - Zero-shot classification
   - ~1.6GB model size

3. **Summarization**: `facebook/bart-large-cnn`
   - Abstractive summarization
   - ~1.6GB model size

Models are cached locally in `./models/cache/` to avoid re-downloading.

## API Endpoints

### Health & Status

- `GET /` - Root endpoint with API info
- `GET /health` - Health check

### Analysis Endpoints

All analysis endpoints are prefixed with `/api/v1`

- `POST /api/v1/analyze` - Full transcript analysis
- `POST /api/v1/analyze/emotion` - Emotion analysis only
- `POST /api/v1/analyze/topic` - Topic analysis only
- `POST /api/v1/analyze/summary` - Summary generation only

See `API.md` for detailed endpoint documentation.

## Database Setup

### Using Alembic Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback:
```bash
alembic downgrade -1
```

### Direct Initialization

For development/testing:
```bash
python scripts/init_db.py
```

## Testing

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app --cov-report=html
```

Run specific test file:
```bash
pytest tests/api/test_routes.py -v
```

Test model loading:
```bash
python scripts/test_models.py
```

## Code Quality

Format code:
```bash
black .
isort .
```

Lint code:
```bash
pylint app
```

Run pre-commit hooks:
```bash
pre-commit install
pre-commit run --all-files
```

## Environment Variables

Key environment variables (see `.env.example` for all):

- `DATABASE_URL` - PostgreSQL connection string
- `HUGGINGFACE_CACHE_DIR` - Model cache directory
- `MODEL_DEVICE` - cpu/cuda/auto for model inference
- `CORS_ORIGINS` - Allowed CORS origins
- `DEBUG` - Enable debug mode

## Deployment

### Docker Production Build

```bash
docker build -t meet-analytics-backend .
docker run -p 8000:8000 --env-file .env meet-analytics-backend
```

### Google Cloud Run

1. Build and push to Container Registry:
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/meet-analytics-backend
```

2. Deploy to Cloud Run:
```bash
gcloud run deploy meet-analytics-backend \
  --image gcr.io/PROJECT_ID/meet-analytics-backend \
  --platform managed \
  --region us-central1 \
  --memory 4Gi
```

## Development Workflow

1. Create a new branch: `backend/feature-name`
2. Make your changes
3. Run tests and linting
4. Commit with descriptive messages
5. Push and create a PR
6. Wait for 2 approvals
7. Merge to main

## Team Members

Backend Team (4 members):
- Add your names here

## Contributing

See `CONTRIBUTING.md` for detailed contribution guidelines.

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Create an issue using the bug report or feature request template
- Contact the backend team lead
- Check API documentation at `/docs`
