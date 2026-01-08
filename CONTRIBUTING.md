# Contributing Guidelines

Thank you for contributing to the Google Meet Analytics project! This document outlines our development workflow and best practices.

## Team Structure

- **Frontend Team** (4 members): Chrome extension development
- **Backend Team** (4 members): API and ML model development

## Branch Naming Convention

### Frontend Branches
```
frontend/feature-name
frontend/fix-issue-description
frontend/refactor-component-name
```

Examples:
- `frontend/caption-scraper`
- `frontend/fix-storage-bug`
- `frontend/refactor-dashboard`

### Backend Branches
```
backend/feature-name
backend/fix-issue-description
backend/refactor-service-name
```

Examples:
- `backend/emotion-analysis`
- `backend/fix-database-connection`
- `backend/refactor-model-loader`

## Git Workflow

### 1. Creating a New Feature

```bash
git checkout main
git pull origin main

git checkout -b backend/your-feature-name
```

### 2. Making Changes

```bash
git add .
git commit -m "Add emotion analysis endpoint"
```

Commit message format:
- Use present tense ("Add feature" not "Added feature")
- Be descriptive but concise
- Reference issue numbers when applicable

Examples:
```
Add emotion analysis endpoint (#23)
Fix database connection timeout
Update model loading error handling
Refactor preprocessing utils for clarity
```

### 3. Pushing Changes

```bash
git push origin backend/your-feature-name
```

### 4. Creating a Pull Request

1. Go to GitHub and create a new Pull Request
2. Use the PR template
3. Fill in all required sections
4. Link related issues
5. Request reviews from 2 team members

### 5. Code Review Process

- PRs require **2 approvals** before merging
- Address all review comments
- Keep discussions focused and constructive
- Use suggestions feature for small changes

### 6. Merging

- Use "Squash and merge" for feature branches
- Use "Rebase and merge" for hotfixes
- Delete branch after merging

## Code Style Guidelines

### Backend (Python)

#### Formatting
- Use **Black** for code formatting
- Use **isort** for import sorting
- Line length: 100 characters

```bash
black .
isort .
```

#### Linting
- Use **Pylint** with provided `.pylintrc`
- Maintain score above 8.0

```bash
pylint app
```

#### Naming Conventions
- Functions/variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private methods: `_leading_underscore`

#### Documentation
- Add docstrings for public functions and classes
- Use type hints for all function parameters and returns

```python
def analyze_emotions(text: str, max_length: int = 512) -> EmotionAnalysis:
    """
    Analyze emotions in the provided text.

    Args:
        text: The text to analyze
        max_length: Maximum token length for processing

    Returns:
        EmotionAnalysis object with detected emotions
    """
    pass
```

### Frontend (JavaScript/TypeScript)

Will be defined by frontend team lead.

## Testing Requirements

### Backend

- Write tests for all new features
- Maintain minimum 80% code coverage
- Test files mirror source structure

```
app/services/analysis_service.py
tests/services/test_analysis_service.py
```

Run tests before committing:
```bash
pytest
pytest --cov=app --cov-report=term-missing
```

### Frontend

Will be defined by frontend team lead.

## Pre-commit Hooks

Install pre-commit hooks:
```bash
pre-commit install
```

This will automatically:
- Format code with Black
- Sort imports with isort
- Run Pylint checks
- Check for trailing whitespace
- Validate YAML/JSON files

## Development Environment

### Backend Setup

1. Python 3.11+
2. Virtual environment
3. PostgreSQL 15+
4. Install dependencies: `pip install -r requirements.txt`

### Environment Variables

Never commit `.env` files. Always use `.env.example` as template.

## Issue Tracking

### Creating Issues

Use the appropriate template:
- Bug Report
- Feature Request

Fill in all required fields:
- Clear description
- Team (Frontend/Backend)
- Steps to reproduce (for bugs)
- Acceptance criteria (for features)

### Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Documentation improvements
- `frontend` - Frontend-specific
- `backend` - Backend-specific
- `high-priority` - Needs immediate attention
- `good-first-issue` - Good for newcomers

## Pull Request Guidelines

### PR Checklist

Before submitting a PR, ensure:
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] Meaningful commit messages
- [ ] PR description is complete

### PR Reviews

As a reviewer:
- Review within 24 hours if possible
- Be constructive and specific
- Suggest improvements, don't just criticize
- Approve only if you'd be comfortable deploying the code

As an author:
- Respond to all comments
- Don't take feedback personally
- Ask for clarification if needed
- Make requested changes or explain why not

## Communication

### Slack/Discord Channels

- `#frontend-team` - Frontend discussions
- `#backend-team` - Backend discussions
- `#general` - General project updates
- `#code-review` - PR review requests

### Meetings

- Weekly team sync: Mondays 2pm
- Bi-weekly demo: Fridays 3pm
- Daily standups: Optional, async in Slack

## Database Migrations

### Backend

Always create migrations for schema changes:

```bash
alembic revision --autogenerate -m "Add emotion_timeline table"
alembic upgrade head
```

Never modify existing migrations. Create new ones.

## Deployment

### Backend Deployment

Deployment to Google Cloud Run is handled by CI/CD after merging to `main`.

Manual deployment:
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/meet-analytics-backend
gcloud run deploy
```

## Troubleshooting

### Common Issues

#### Models not loading
- Check `HUGGINGFACE_CACHE_DIR` permissions
- Ensure sufficient disk space (5GB+)
- Verify internet connection for first download

#### Database connection errors
- Verify PostgreSQL is running
- Check `DATABASE_URL` in `.env`
- Ensure database exists

#### Tests failing
- Clear test database: `rm test.db`
- Update dependencies: `pip install -r requirements.txt`
- Check for port conflicts (5432, 8000)

## Questions?

- Check existing documentation
- Search closed issues
- Ask in team Slack channel
- Create a new issue with `question` label

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Assume good intentions
- Keep discussions professional

## Recognition

Contributors will be recognized in:
- README.md
- Release notes
- Team meetings

Thank you for contributing!
