# Google Meet Analytics - Backend Team Presentation

**Date**: January 8, 2026
**Presenter**: Backend Team Lead
**Status**: ✅ Backend Fully Operational

---

## 🎯 TL;DR - What We Built

We have a **production-ready FastAPI backend** that analyzes Google Meet transcripts using AI:
- ✅ **4 working API endpoints**
- ✅ **3 AI models** (emotion, topic, summary)
- ✅ **PostgreSQL database** for persistence
- ✅ **Docker containerization**
- ✅ **Complete documentation**
- ✅ **Ready for Chrome extension integration**

---

## 📊 Live Demo

### Access the API
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### What You'll See
1. **Interactive Swagger UI** - Test all endpoints in browser
2. **Real-time AI analysis** - Emotions, topics, summaries
3. **Database persistence** - All analyses saved
4. **Professional documentation** - Auto-generated API docs

---

## 🤖 AI Analysis Capabilities

### 1. Emotion Analysis
**Model**: RoBERTa (SamLowe/roberta-base-go_emotions)
**What it does**: Detects 28 different emotions from text

**Example Input**:
```
"I'm really excited about this project!
The team is doing amazing work."
```

**Example Output**:
```json
{
  "dominant_emotion": "joy",
  "emotions": [
    {"label": "joy", "score": 0.85},
    {"label": "optimism", "score": 0.78},
    {"label": "excitement", "score": 0.72}
  ]
}
```

**Use Cases**:
- Track team morale over time
- Identify tense moments in meetings
- Measure emotional engagement

---

### 2. Topic Classification
**Model**: BART (facebook/bart-large-mnli)
**What it does**: Classifies meeting topics from 9 categories

**Topics Detected**:
- Technical discussion
- Project planning
- Business strategy
- Team management
- Product development
- Customer feedback
- Budget and finance
- Marketing
- General discussion

**Example Input**:
```
"We discussed the database schema and
API endpoints for the new feature."
```

**Example Output**:
```json
{
  "primary_topic": "technical discussion",
  "topics": [
    {"topic": "technical discussion", "score": 0.95},
    {"topic": "product development", "score": 0.78}
  ]
}
```

**Use Cases**:
- Categorize meetings automatically
- Track topic focus over time
- Identify off-topic discussions

---

### 3. Meeting Summarization
**Model**: BART-CNN (facebook/bart-large-cnn)
**What it does**: Generates concise summaries with key points

**Example Input**:
```
"In today's meeting we discussed the sprint planning.
The team raised concerns about database performance.
We decided to implement caching and optimize queries.
Sarah will lead the database work while John handles
the API improvements. Weekly demos start next Friday."
```

**Example Output**:
```json
{
  "summary": "Team discussed sprint planning with focus on database optimization through caching and query improvements.",
  "key_points": [
    "Team discussed sprint planning",
    "Database optimization through caching",
    "Sarah leads database work, John handles API"
  ],
  "conciseness_score": 0.15,
  "word_count_original": 45,
  "word_count_summary": 7
}
```

**Use Cases**:
- Auto-generate meeting notes
- Create shareable summaries
- Track action items

---

## 🔌 API Endpoints

### 1. Health Check
```bash
GET /health
```
Returns: `{"status": "healthy"}`

---

### 2. Emotion Analysis Only
```bash
POST /api/v1/analyze/emotion
```
**Input**:
```json
{
  "meeting_id": "standup-001",
  "transcript": "Your transcript here..."
}
```
**Returns**: Emotion analysis object

---

### 3. Topic Classification Only
```bash
POST /api/v1/analyze/topic
```
**Input**:
```json
{
  "meeting_id": "standup-001",
  "transcript": "Your transcript here..."
}
```
**Returns**: Topic analysis object

---

### 4. Summary Generation Only
```bash
POST /api/v1/analyze/summary
```
**Input**:
```json
{
  "meeting_id": "standup-001",
  "transcript": "Your transcript here..."
}
```
**Returns**: Summary object

---

### 5. Full Analysis (All Three)
```bash
POST /api/v1/analyze
```
**Input**:
```json
{
  "meeting_id": "standup-001",
  "transcript": "Your transcript here..."
}
```
**Returns**: Complete analysis with emotion + topic + summary
**Also**: Saves to database for historical tracking

---

## 💾 Database Architecture

### Tables Created

**1. meeting_analysis**
- Stores complete analysis results
- Fields: meeting_id, transcript, emotion_data, topic_data, summary_data
- Indexed by meeting_id for fast lookups

**2. emotion_timeline**
- Time-series emotion tracking
- Tracks dominant emotion over time
- Enables emotion drift detection

**3. topic_timeline**
- Time-series topic tracking
- Tracks topic changes over meeting
- Enables topic drift detection

### Database Tech
- **PostgreSQL 15** running in Docker
- **SQLAlchemy ORM** for Python integration
- **Alembic** for migrations
- **JSON columns** for flexible data storage

---

## 🐳 Docker Setup

### What's Running
```bash
docker ps
```
Shows: `meet_analytics_db` (PostgreSQL)

### Start Database
```bash
docker compose up db -d
```

### Check Database
```bash
docker exec -it meet_analytics_db psql -U postgres -d meet_analytics -c "\dt"
```

### View Saved Data
```bash
docker exec -it meet_analytics_db psql -U postgres -d meet_analytics \
  -c "SELECT meeting_id, created_at FROM meeting_analysis LIMIT 5;"
```

---

## 📈 Performance Metrics

### Response Times (CPU)
- Emotion analysis: **1-3 seconds**
- Topic classification: **2-4 seconds**
- Summarization: **3-6 seconds**
- Full analysis: **5-10 seconds**

### Model Loading
- First startup: **30-60 seconds** (one-time)
- Subsequent requests: **Instant** (models cached)

### Model Sizes
- Emotion model: ~500MB
- Topic model: ~1.6GB
- Summary model: ~1.6GB
- **Total**: ~4GB disk space

---

## 🛠 Tech Stack

### Backend
- **Python**: 3.11+
- **Framework**: FastAPI 0.109
- **Server**: Uvicorn with auto-reload
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0

### AI/ML
- **HuggingFace Transformers**: 4.36.2
- **PyTorch**: 2.2+
- **Models**: RoBERTa, BART-MNLI, BART-CNN

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Local development
- **GitHub Actions**: CI/CD
- **pytest**: Testing framework

### Code Quality
- **Black**: Code formatting
- **isort**: Import sorting
- **Pylint**: Linting
- **Pre-commit hooks**: Automated checks

---

## 📚 Documentation

We've created comprehensive documentation:

1. **README.md** - Backend overview and setup
2. **API.md** - Complete API documentation with examples
3. **SETUP.md** - Step-by-step environment setup
4. **CONTRIBUTING.md** - Team workflow and guidelines
5. **PROJECT_STRUCTURE.md** - Codebase architecture
6. **CURRENT.md** - Project status tracking
7. **GitHub Templates** - PR, bug reports, feature requests

All docs are in: `/backend/` and project root

---

## 👥 Team Tasks - Next Sprint

We have **4 team members** and **4 feature tasks**:

### Team Member 1: Speaker Engagement Analytics
**Goal**: Analyze individual speaker metrics

**Tasks**:
- Parse speaker-labeled transcripts
- Calculate speaking time per person
- Measure emotional variance per speaker
- Create engagement scoring
- Build `/api/v1/analyze/speakers` endpoint

**Impact**: Show who dominated conversation, who was quiet, engagement levels

---

### Team Member 2: Topic Drift Detection
**Goal**: Detect when meetings go off-topic

**Tasks**:
- Compare topics across transcript chunks
- Calculate topic similarity scores
- Detect drift threshold crossings
- Track topic transitions
- Generate drift alerts

**Impact**: Identify when meetings lose focus, track topic flow

---

### Team Member 3: Key Moments Identification
**Goal**: Find important moments in meetings

**Tasks**:
- Detect emotional peaks/valleys
- Identify decision keywords
- Find action item mentions
- Cluster questions together
- Rank by importance score
- Build `/api/v1/analyze/timeline` endpoint

**Impact**: Auto-extract highlights, decisions, action items

---

### Team Member 4: Testing & Performance
**Goal**: Ensure code quality and performance

**Tasks**:
- Write integration tests for full pipeline
- Add performance benchmarks
- Test edge cases (empty transcripts, very long text)
- Create Jupyter demo notebook
- Improve logging and error handling
- Document performance characteristics

**Impact**: Reliable, well-tested, production-ready code

---

## 🚀 Development Workflow

### Branch Naming
```
backend/feature-name
backend/fix-bug-description
```

Examples:
- `backend/speaker-engagement`
- `backend/topic-drift`
- `backend/key-moments`

### Making Changes
```bash
# Create branch
git checkout -b backend/your-feature

# Make changes
# ...

# Format and test
make format
make lint
make test

# Commit
git add .
git commit -m "Add speaker engagement analysis"

# Push and create PR
git push origin backend/your-feature
```

### PR Requirements
- ✅ All tests passing
- ✅ Code formatted with Black
- ✅ Linting passes
- ✅ 2 approvals required
- ✅ CI/CD checks pass

---

## 🎯 Success Criteria

### Sprint 1 (Completed) ✅
- [x] Backend API running
- [x] 4 endpoints working
- [x] Database operational
- [x] Docker setup complete
- [x] Documentation written

### Sprint 2 (Next 2 Weeks)
- [ ] 4 new features implemented
- [ ] Test coverage >85%
- [ ] All 8 endpoints working
- [ ] Code reviews completed
- [ ] Integration tests passing

### Sprint 3 (Week 3-4)
- [ ] Frontend Chrome extension starts
- [ ] Backend deployed to Google Cloud Run
- [ ] End-to-end integration
- [ ] Performance optimization
- [ ] User testing begins

---

## 🔥 Demo Time!

### Live Demo Steps

1. **Open API Docs**
   - Go to: http://localhost:8000/docs
   - Show Swagger UI interface

2. **Test Emotion Analysis**
   - Use happy transcript: "Amazing work team!"
   - Show emotion scores
   - Use frustrated transcript: "This is so frustrating!"
   - Show different emotions detected

3. **Test Topic Analysis**
   - Use technical transcript
   - Show topic classification
   - Explain use cases

4. **Test Full Analysis**
   - Use realistic meeting transcript
   - Show all three analyses together
   - Show response time

5. **Check Database**
   - Show saved records
   - Demonstrate persistence
   - Show timeline tables

---

## 🤔 Q&A - Common Questions

**Q: How accurate are the AI models?**
A: Very accurate for their tasks. RoBERTa for emotions is state-of-the-art. BART models are industry-standard for NLP.

**Q: Can we use our own custom models?**
A: Yes! Just update model names in `config.py` and restart. The architecture supports any HuggingFace model.

**Q: What about real-time analysis?**
A: Current version is batch processing. Real-time would need WebSocket support (future enhancement).

**Q: How do we deploy to production?**
A: Google Cloud Run (documented). Single command deploy with Docker.

**Q: Can it handle multiple languages?**
A: Current models are English-only. We can add multilingual models.

**Q: What about speaker diarization (who said what)?**
A: That's Team Member 1's task! Speaker parsing and engagement metrics.

**Q: How much does it cost to run?**
A: Free locally. Production costs ~$20-50/month on Cloud Run (depends on usage).

**Q: Is it secure?**
A: Currently no authentication. We'll add API keys before production deployment.

---

## 📋 Next Steps

### This Week
1. **Team Onboarding** (Today)
   - Run through this presentation
   - Get everyone's environment set up
   - Answer questions

2. **Task Assignment** (Today)
   - Assign 4 team members to 4 tasks
   - Create GitHub issues for each
   - Set up project board

3. **Kickoff** (This Week)
   - First team standup
   - Review code structure together
   - Set sprint goals

### Next 2 Weeks
- Daily standups (async in Slack)
- Code reviews
- Feature development
- Weekly demos

### Weeks 3-4
- Integration testing
- Documentation updates
- Performance tuning
- Deployment preparation

---

## 🎓 Resources for Team

### Getting Started
- **Setup Guide**: `/backend/SETUP.md`
- **Contributing**: `/CONTRIBUTING.md`
- **API Docs**: http://localhost:8000/docs

### Learning Resources
- FastAPI Tutorial: https://fastapi.tiangolo.com/tutorial/
- HuggingFace Docs: https://huggingface.co/docs
- SQLAlchemy Tutorial: https://docs.sqlalchemy.org/tutorial/

### Communication
- GitHub Issues: Questions and bugs
- Slack: `#backend-team` channel
- Weekly Sync: [TBD]

---

## 💪 What Makes This Special

### 1. Production-Ready Code
- Proper error handling
- Comprehensive logging
- Input validation
- Scalable architecture

### 2. Best Practices
- Type hints throughout
- Dependency injection
- Service layer pattern
- Clean code principles

### 3. Developer Experience
- Auto-formatting
- Pre-commit hooks
- Interactive API docs
- Hot-reload development

### 4. Team Collaboration
- Clear documentation
- GitHub templates
- Code review process
- CI/CD automation

---

## 🎉 Conclusion

### What We Accomplished
✅ Built a fully functional AI-powered backend
✅ 4 working API endpoints
✅ 3 AI models integrated
✅ Database persistence
✅ Docker containerization
✅ Complete documentation
✅ Production-ready architecture

### What's Next
🚀 Onboard team members
🚀 Build 4 advanced features
🚀 Start Chrome extension
🚀 Deploy to cloud
🚀 Launch MVP

### Thank You!
Questions?

---

**Access Everything**:
- Code: `/Users/aahadvakani/Desktop/DepAIProject/`
- API: http://localhost:8000/docs
- Docs: `/backend/README.md`
- Status: `/CURRENT.md`
