# Backend Development Setup Guide

Step-by-step guide for setting up the backend development environment.

## Prerequisites

Before starting, ensure you have:
- Python 3.11 or higher installed
- PostgreSQL 15 or higher (or Docker)
- Git installed
- 4GB+ free RAM (for ML models)
- 5GB+ free disk space (for model cache)

Check versions:
```bash
python --version  # Should be 3.11+
psql --version    # Should be 15+
docker --version  # Optional but recommended
```

## Step 1: Clone and Navigate

```bash
cd backend
```

## Step 2: Python Virtual Environment

### On macOS/Linux:
```bash
python -m venv venv
source venv/bin/activate
```

### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

## Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- FastAPI and Uvicorn
- HuggingFace Transformers and PyTorch
- SQLAlchemy and PostgreSQL driver
- Testing and development tools

Installation may take 5-10 minutes depending on your connection.

## Step 4: Environment Configuration

```bash
cp .env.example .env
```

Edit `.env` with your preferred editor:
```bash
nano .env  # or vim, code, etc.
```

Key variables to configure:
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/meet_analytics
HUGGINGFACE_CACHE_DIR=./models/cache
MODEL_DEVICE=cpu  # Use 'cuda' if you have NVIDIA GPU
DEBUG=True
```

## Step 5: Database Setup

### Option A: Using Docker (Recommended)

Start PostgreSQL with Docker Compose:
```bash
docker-compose up db -d
```

Verify it's running:
```bash
docker ps
```

### Option B: Local PostgreSQL

Install PostgreSQL 15+ and create database:
```bash
psql -U postgres
CREATE DATABASE meet_analytics;
\q
```

## Step 6: Initialize Database

```bash
python scripts/init_db.py
```

You should see:
```
Creating database tables...
Database tables created successfully!
```

## Step 7: Test Model Loading

This step downloads the ML models (first time only):
```bash
python scripts/test_models.py
```

Expected output:
```
Testing model loading...
Loading emotion analysis model...
Emotion model loaded successfully
Loading topic classification model...
Topic model loaded successfully
Loading summarization model...
Summary model loaded successfully

Testing emotion analysis...
All tests passed!
```

Models will be cached in `./models/cache/` (about 4GB total).

## Step 8: Run Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 9: Verify Installation

Open your browser and visit:
- API root: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

Test the API:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"healthy"}
```

## Step 10: Install Development Tools

### Pre-commit Hooks

```bash
pre-commit install
```

Test the hooks:
```bash
pre-commit run --all-files
```

### VSCode Extensions (if using VSCode)

Install these extensions:
- Python
- Pylance
- Black Formatter
- isort
- GitLens

## Step 11: Run Tests

```bash
pytest
```

Expected output:
```
====== test session starts ======
collected 5 items

tests/api/test_routes.py ..
tests/unit/test_preprocessing.py ...

====== 5 passed in 2.34s ======
```

## Troubleshooting

### Issue: ModuleNotFoundError

Solution: Ensure virtual environment is activated
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Issue: Database connection failed

Solution: Check PostgreSQL is running
```bash
docker-compose ps  # If using Docker
# or
sudo service postgresql status  # If using local PostgreSQL
```

### Issue: CUDA out of memory

Solution: Switch to CPU mode in `.env`
```env
MODEL_DEVICE=cpu
```

### Issue: Model download fails

Solution: Check internet connection and disk space
```bash
df -h  # Check disk space
ping huggingface.co  # Check connectivity
```

### Issue: Port 8000 already in use

Solution: Use different port or kill existing process
```bash
lsof -ti:8000 | xargs kill  # macOS/Linux
# or
uvicorn app.main:app --reload --port 8001
```

## Docker Development (Alternative)

If you prefer using Docker for everything:

```bash
docker-compose up
```

This starts both PostgreSQL and the API server.

Access the API at http://localhost:8000

## Next Steps

1. Read the [API.md](API.md) documentation
2. Review [CONTRIBUTING.md](../CONTRIBUTING.md) for workflow
3. Check existing issues for tasks to work on
4. Join the backend team channel
5. Attend the next team sync

## Quick Reference

### Common Commands

Start dev server:
```bash
uvicorn app.main:app --reload
```

Run tests:
```bash
pytest
pytest --cov=app
```

Format code:
```bash
black .
isort .
```

Lint code:
```bash
pylint app
```

Database migrations:
```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### File Locations

- Main app: `app/main.py`
- API routes: `app/api/routes.py`
- Models: `app/services/model_loader.py`
- Database models: `app/models/analysis.py`
- Tests: `tests/`
- Config: `app/core/config.py`

## Getting Help

- Check this guide first
- Review closed issues on GitHub
- Ask in backend team channel
- Create issue with `question` label
- Contact backend team lead

## Verification Checklist

- [ ] Python 3.11+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Database running
- [ ] Environment variables configured
- [ ] Database tables created
- [ ] Models downloaded and cached
- [ ] Dev server running
- [ ] Tests passing
- [ ] Pre-commit hooks installed

If all items are checked, you're ready to develop!

Welcome to the team!
