# Google Meet Analytics

A Chrome extension that provides post-meeting analytics for Google Meet sessions using advanced AI analysis.

## Overview

This project analyzes Google Meet transcripts to provide insights including:
- Emotion and sentiment tracking throughout the meeting
- Topic classification and drift detection
- Conciseness metrics and meeting summaries
- Speaker engagement analysis
- Key moment identification
- Timeline visualizations

## Architecture

### Frontend (Chrome Extension)
- React-based dashboard UI
- Manifest V3 Chrome extension
- Content scripts for caption scraping from Google Meet
- Chrome Storage API for local data persistence
- Real-time communication with backend API

### Backend (FastAPI)
- RESTful API server
- HuggingFace transformer models for AI analysis:
  - `SamLowe/roberta-base-go_emotions` - Emotion analysis (28 emotions)
  - `facebook/bart-large-mnli` - Topic classification
  - `facebook/bart-large-cnn` - Meeting summarization
- PostgreSQL database for analytics storage
- Dockerized for easy deployment
- Google Cloud Run ready

## Project Structure

```
DepAIProject/
├── backend/                 # FastAPI backend (COMPLETED)
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Config and startup
│   │   ├── db/             # Database setup
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utilities
│   ├── tests/              # Test suite
│   ├── alembic/            # DB migrations
│   └── docker-compose.yml  # Local development
│
├── frontend/               # Chrome extension (TODO)
│   └── (To be implemented)
│
├── .github/
│   ├── workflows/          # CI/CD pipelines
│   └── ISSUE_TEMPLATE/     # Issue templates
│
├── CONTRIBUTING.md         # Contribution guidelines
└── README.md              # This file
```

## Getting Started

### Backend Setup

See [backend/README.md](backend/README.md) for detailed backend setup instructions.

Quick start:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
docker-compose up
```

API will be available at `http://localhost:8000`

### Frontend Setup

Frontend implementation coming soon.

## Team Structure

### Backend Team (4 members)
- Backend team lead: [Add name]
- Team members: [Add names]
- Responsibilities: API development, ML model integration, database design

### Frontend Team (4 members)
- Frontend team lead: [Add name]
- Team members: [Add names]
- Responsibilities: Chrome extension, UI/UX, caption scraping

## Development Workflow

1. Create branch with team prefix: `backend/feature` or `frontend/feature`
2. Implement feature with tests
3. Run linting and formatting
4. Create Pull Request using template
5. Get 2 approvals
6. Merge to main

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Technology Stack

### Backend
- Python 3.11
- FastAPI
- PostgreSQL 15
- SQLAlchemy 2.0
- HuggingFace Transformers
- PyTorch
- Docker

### Frontend
- React
- TypeScript
- Vite
- Chrome Extension APIs
- TailwindCSS

## API Documentation

Full API documentation available at:
- Interactive docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Markdown: [backend/API.md](backend/API.md)

## Key Features

### Emotion Analysis
- Real-time emotion tracking (28 emotion types)
- Emotional volatility detection
- Sentiment trends over time

### Topic Analysis
- Multi-topic classification
- Topic drift detection
- Discussion focus metrics

### Meeting Summarization
- Abstractive summarization
- Key point extraction
- Conciseness scoring

### Analytics Dashboard
- Visual timeline of emotions
- Topic distribution charts
- Speaker engagement metrics
- Meeting effectiveness scores

## Testing

### Backend
```bash
cd backend
pytest --cov=app
```

### Frontend
Coming soon

## Deployment

### Backend Deployment (Google Cloud Run)

```bash
cd backend
gcloud builds submit --tag gcr.io/PROJECT_ID/meet-analytics-backend
gcloud run deploy meet-analytics-backend \
  --image gcr.io/PROJECT_ID/meet-analytics-backend \
  --platform managed \
  --region us-central1 \
  --memory 4Gi
```

### Frontend Deployment (Chrome Web Store)

Coming soon

## CI/CD

GitHub Actions workflows:
- Backend: Linting, testing, Docker build on PR and merge
- Frontend: Coming soon

## Environment Setup

### Required Tools
- Python 3.11+ (backend)
- Node.js 18+ (frontend)
- PostgreSQL 15+ (backend)
- Docker & Docker Compose
- Git

### Recommended IDE Extensions
- Python: Black, Pylint, Pylance
- JavaScript: ESLint, Prettier
- General: EditorConfig, GitLens

## Contributing

We welcome contributions from all team members! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code style guidelines
- Branch naming conventions
- PR requirements
- Testing standards

## License

MIT License

## Support

- Create an issue using templates in `.github/ISSUE_TEMPLATE/`
- Contact team leads
- Check documentation in respective team folders

## Roadmap

### Phase 1 (Current)
- [x] Backend API setup
- [x] ML model integration
- [x] Database design
- [ ] Frontend extension structure
- [ ] Caption scraping implementation

### Phase 2
- [ ] Real-time analysis pipeline
- [ ] Chrome extension UI
- [ ] User authentication
- [ ] Analytics dashboard

### Phase 3
- [ ] Advanced analytics features
- [ ] Export functionality
- [ ] Team collaboration features
- [ ] Chrome Web Store publication

## Acknowledgments

- AI Club for project organization
- HuggingFace for transformer models
- FastAPI and React communities

## Status

Backend: Ready for development
Frontend: Structure pending

Last updated: January 2024
