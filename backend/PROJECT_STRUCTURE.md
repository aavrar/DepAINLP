# Backend Project Structure

Complete overview of the backend codebase structure and file purposes.

```
backend/
├── app/                                    # Main application package
│   ├── __init__.py                        # Package initializer
│   ├── main.py                            # FastAPI app entry point, CORS, startup
│   │
│   ├── api/                               # API layer
│   │   ├── __init__.py
│   │   ├── routes.py                      # All API endpoints (/analyze, /analyze/emotion, etc.)
│   │   └── deps.py                        # Dependency injection (get_db, get_model_loader)
│   │
│   ├── core/                              # Core configuration
│   │   ├── __init__.py
│   │   ├── config.py                      # Settings class with env vars (Pydantic Settings)
│   │   └── events.py                      # Startup/shutdown events, model loading
│   │
│   ├── db/                                # Database layer
│   │   ├── __init__.py
│   │   ├── session.py                     # SQLAlchemy engine and session factory
│   │   └── base.py                        # Import all models for Alembic
│   │
│   ├── models/                            # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   └── analysis.py                    # MeetingAnalysis, EmotionTimeline, TopicTimeline
│   │
│   ├── schemas/                           # Pydantic models for API
│   │   ├── __init__.py
│   │   └── analysis.py                    # Request/Response schemas (AnalysisRequest, etc.)
│   │
│   ├── services/                          # Business logic
│   │   ├── __init__.py
│   │   ├── model_loader.py                # HuggingFace model loading and management
│   │   └── analysis_service.py            # Analysis orchestration (emotions, topics, summary)
│   │
│   └── utils/                             # Utility functions
│       ├── __init__.py
│       └── preprocessing.py               # Text preprocessing (clean, chunk, split by speaker)
│
├── tests/                                 # Test suite
│   ├── __init__.py
│   ├── conftest.py                        # Pytest fixtures and configuration
│   │
│   ├── api/                               # API endpoint tests
│   │   ├── __init__.py
│   │   └── test_routes.py                 # Test /analyze endpoints
│   │
│   ├── services/                          # Service layer tests
│   │   └── __init__.py
│   │
│   └── unit/                              # Unit tests
│       ├── __init__.py
│       └── test_preprocessing.py          # Test preprocessing utils
│
├── alembic/                               # Database migrations
│   ├── versions/                          # Migration files (auto-generated)
│   ├── env.py                             # Alembic environment configuration
│   ├── script.py.mako                     # Migration template
│   └── README                             # Alembic usage guide
│
├── scripts/                               # Utility scripts
│   ├── init_db.py                         # Create database tables
│   └── test_models.py                     # Test HuggingFace model loading
│
├── .github/                               # GitHub configuration
│   ├── workflows/
│   │   └── backend-ci.yml                 # CI pipeline (lint, test, docker)
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md                  # Bug report template
│   │   └── feature_request.md             # Feature request template
│   └── pull_request_template.md           # PR template
│
├── models/                                # Model cache (gitignored)
│   └── cache/                             # HuggingFace model downloads (~4GB)
│
├── requirements.txt                       # Python dependencies
├── pyproject.toml                         # Black, isort, pytest configuration
├── .pylintrc                              # Pylint configuration
├── .pre-commit-config.yaml                # Pre-commit hooks configuration
├── .gitignore                             # Git ignore patterns
├── .env.example                           # Environment variables template
├── .env.development                       # Development environment template
├── .dockerignore                          # Docker ignore patterns
│
├── Dockerfile                             # Production Docker image
├── Dockerfile.dev                         # Development Docker image
├── docker-compose.yml                     # Local development with PostgreSQL
│
├── alembic.ini                            # Alembic configuration
├── Makefile                               # Common development commands
│
├── README.md                              # Main backend documentation
├── API.md                                 # API endpoint documentation
├── SETUP.md                               # Development setup guide
├── CHANGELOG.md                           # Version history
└── PROJECT_STRUCTURE.md                   # This file
```

## File Purposes

### Application Core

**app/main.py**
- Creates FastAPI application instance
- Configures CORS middleware
- Includes API router
- Defines health check endpoints
- Uses lifespan context manager for startup/shutdown

**app/core/config.py**
- Pydantic Settings for environment variables
- Database connection settings
- Model configuration (names, device, cache)
- CORS origins
- Debug flags

**app/core/events.py**
- Lifespan context manager
- Loads ML models on startup
- Stores model_loader in app.state
- Cleanup on shutdown

### API Layer

**app/api/routes.py**
- POST /api/v1/analyze - Full transcript analysis
- POST /api/v1/analyze/emotion - Emotion analysis only
- POST /api/v1/analyze/topic - Topic classification only
- POST /api/v1/analyze/summary - Summary generation only
- Error handling and logging

**app/api/deps.py**
- get_db() - Database session dependency
- get_model_loader() - Access to ML models from app.state

### Services

**app/services/model_loader.py**
- ModelLoader class
- Loads 3 HuggingFace pipelines:
  - emotion_pipeline (text-classification)
  - topic_pipeline (zero-shot-classification)
  - summary_pipeline (summarization)
- Device management (CPU/GPU)
- Model caching
- Cleanup utilities

**app/services/analysis_service.py**
- AnalysisService class
- analyze_emotions() - Chunks text, runs emotion analysis, aggregates
- analyze_topics() - Zero-shot classification with candidate labels
- generate_summary() - Abstractive summarization with key points
- analyze_transcript() - Orchestrates all analyses
- _save_to_database() - Persists results to PostgreSQL

### Database

**app/models/analysis.py**
- MeetingAnalysis - Main analysis results table
- EmotionTimeline - Time-series emotion data
- TopicTimeline - Time-series topic data
- JSON columns for flexibility

**app/db/session.py**
- SQLAlchemy engine creation
- SessionLocal factory
- Connection pooling configuration

**app/schemas/analysis.py**
- AnalysisRequest - API request schema
- AnalysisResponse - Complete analysis response
- EmotionAnalysis, TopicAnalysis, MeetingSummary - Component schemas
- Validation and documentation

### Utilities

**app/utils/preprocessing.py**
- clean_text() - Remove extra whitespace
- chunk_text() - Split into model-sized chunks
- extract_speakers() - Parse speaker names
- split_by_speaker() - Separate by speaker for engagement analysis

### Tests

**tests/conftest.py**
- Pytest configuration
- Database fixtures with SQLite
- FastAPI TestClient fixture

**tests/api/test_routes.py**
- Test all API endpoints
- Test request/response schemas
- Test error handling

**tests/unit/test_preprocessing.py**
- Test all preprocessing utilities
- Test edge cases

### Docker

**Dockerfile**
- Production image
- Multi-stage build
- Non-root user
- Optimized layers

**Dockerfile.dev**
- Development image
- Hot reload support
- Debug tools included

**docker-compose.yml**
- PostgreSQL service
- API service with volume mounts
- Health checks
- Shared network

### Configuration Files

**.env.example / .env.development**
- Template for environment variables
- All required settings documented
- Safe defaults for development

**pyproject.toml**
- Black configuration (line-length: 100)
- isort configuration (black profile)
- pytest configuration (coverage, async)

**.pylintrc**
- Pylint rules
- Disabled checks for FastAPI patterns
- Line length: 100

**.pre-commit-config.yaml**
- Automatic code formatting
- Linting on commit
- Prevents committing bad code

**alembic.ini**
- Database migration configuration
- Migration path
- Logging configuration

**Makefile**
- Common development commands
- make dev, make test, make format, etc.
- Docker shortcuts

## Key Design Patterns

### Dependency Injection
- FastAPI's Depends() for database and model access
- Clean separation of concerns
- Easy testing with mocks

### Service Layer
- Business logic separated from API layer
- Reusable across different endpoints
- Testable independently

### Repository Pattern (Light)
- SQLAlchemy models separate from Pydantic schemas
- Database operations in service layer
- Clear data flow

### Configuration Management
- Pydantic Settings for type-safe config
- Environment-based configuration
- Validation at startup

### Error Handling
- Try-except in service layer
- HTTPException in API layer
- Detailed logging

## Data Flow

1. **Request arrives** → routes.py
2. **Dependencies injected** → deps.py provides DB session and models
3. **Service called** → analysis_service.py orchestrates analysis
4. **Models used** → model_loader.py provides HuggingFace pipelines
5. **Data preprocessed** → preprocessing.py cleans and chunks text
6. **Results validated** → Pydantic schemas ensure correct format
7. **Data persisted** → SQLAlchemy models save to PostgreSQL
8. **Response returned** → JSON serialized by FastAPI

## Extension Points

### Adding New Analysis Types
1. Add method to AnalysisService
2. Add endpoint in routes.py
3. Add schema in schemas/analysis.py
4. Add tests

### Adding New Models
1. Add model name to config.py
2. Load in model_loader.py
3. Create service method
4. Create endpoint

### Adding Database Tables
1. Create model in models/
2. Import in db/base.py
3. Generate migration: `alembic revision --autogenerate`
4. Apply: `alembic upgrade head`

## Development Workflow

1. **Start services**: `make docker-up` or `docker-compose up`
2. **Run dev server**: `make dev` or `uvicorn app.main:app --reload`
3. **Make changes**: Edit files in app/
4. **Test**: `make test` or `pytest`
5. **Format**: `make format` or `black . && isort .`
6. **Commit**: Pre-commit hooks run automatically
7. **Push**: CI pipeline runs tests and linting

## Where to Start

### For New Features
1. Define schema in `schemas/analysis.py`
2. Implement in `services/analysis_service.py`
3. Add endpoint in `api/routes.py`
4. Write tests in `tests/`

### For Bug Fixes
1. Write failing test in `tests/`
2. Fix in relevant service/util
3. Ensure test passes
4. Check no regressions

### For Model Changes
1. Update model name in `core/config.py`
2. Modify loader in `services/model_loader.py`
3. Test with `scripts/test_models.py`
4. Update documentation

## Important Notes

- Models are loaded once at startup (saves time)
- Database sessions are per-request (thread-safe)
- All text is preprocessed before analysis
- Results are cached in PostgreSQL
- API is fully async-capable
- CORS configured for Chrome extensions

## Next Steps

After understanding the structure:
1. Read SETUP.md to get environment running
2. Review API.md for endpoint details
3. Check CONTRIBUTING.md for workflow
4. Pick an issue to work on
5. Ask questions in team channel

Happy coding!
