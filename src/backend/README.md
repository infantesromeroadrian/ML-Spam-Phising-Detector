# 🔐 SPAM & PHISHING Detector - Backend

**Production-ready ML backend** for email classification using scikit-learn.

## 🏗️ Architecture

This backend follows **Hexagonal (Clean) Architecture**:

```
backend/
├── spam_detector/           # Python package (flat layout)
│   ├── domain/              # Business logic (framework-agnostic)
│   │   ├── entities/        # Data models (Email, Prediction, etc.)
│   │   ├── ports/           # Interfaces (Protocol classes)
│   │   └── services/        # Domain services
│   ├── application/         # Use cases (orchestration)
│   │   ├── classify.py
│   │   └── manage_models.py
│   ├── infrastructure/      # External adapters
│   │   ├── api/             # FastAPI (driving adapter)
│   │   ├── cli/             # Typer CLI (driving adapter)
│   │   └── adapters/        # ML models, loaders (driven adapters)
│   ├── config/              # Pydantic settings
│   └── utils/               # MLflow helpers
├── tests/                   # Pytest tests
├── models/                  # Trained models (Git LFS)
├── pyproject.toml
└── README.md
```

**Key principle**: Domain layer has ZERO dependencies on infrastructure (no FastAPI, no scikit-learn imports in domain/).

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **uv** (recommended): `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Installation

```bash
# Clone and enter directory
cd backend

# Create virtual environment
uv venv

# Activate (Linux/Mac)
source .venv/bin/activate
# Or (Windows)
.venv\Scripts\activate

# Install dependencies
uv sync

# Verify installation
spam-detector --help
```

### Download Models

Models are tracked with Git LFS:

```bash
# If not already installed
git lfs install

# Pull LFS files
git lfs pull
```

Models will be in `backend/models/`.

## 📋 Usage

### CLI Tool

```bash
# Classify email from text
spam-detector predict "Buy now! 50% off! Limited time!"

# From file
spam-detector predict --file email.txt

# JSON output
spam-detector predict --output json "Suspicious email..."

# Verbose mode
spam-detector -v predict "Email text"

# List models
spam-detector models list

# Model info
spam-detector models info spam_detector latest
```

### API Server

```bash
# Start API server
spam-detector-api

# Or with uvicorn directly
uvicorn spam_detector.infrastructure.api.main:app --reload

# API will be available at:
# - http://localhost:8000
# - Docs: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `POST /api/v1/classify` | POST | Classify email |
| `GET /api/v1/models/{name}` | GET | List model versions |
| `GET /api/v1/models/{name}/latest` | GET | Get latest model info |
| `GET /health` | GET | Health check |

#### Example: Classify Email

```bash
curl -X POST http://localhost:8000/api/v1/classify \
  -H "Content-Type: application/json" \
  -d '{
    "email_text": "URGENT! You won a lottery! Click here now!"
  }'
```

**Response:**

```json
{
  "verdict": "PHISHING",
  "risk_level": "HIGH",
  "is_malicious": true,
  "spam_label": "HAM",
  "spam_probability": 0.50,
  "spam_model_version": "20260105_194602",
  "phishing_label": "PHISHING",
  "phishing_probability": 0.985,
  "phishing_model_version": "20260105_195259",
  "execution_time_ms": 1.81,
  "threat_report": {
    "risk_score": 84,
    "iocs": [...],
    "threat_vectors": [...],
    "recommendations": [...]
  }
}
```

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=spam_detector --cov-report=html

# Only unit tests
pytest tests/unit

# Only integration tests
pytest tests/integration

# Specific test file
pytest tests/unit/test_email_classifier.py

# Verbose
pytest -v
```

Coverage report will be in `htmlcov/index.html`.

## 🔧 Development

### Code Quality

```bash
# Format code
ruff format .

# Lint
ruff check .

# Fix auto-fixable issues
ruff check --fix .

# Type check
mypy src/

# All checks
ruff check . && mypy src/ && pytest
```

### Configuration

Settings are managed via Pydantic Settings in `src/spam_detector/config/settings.py`.

Environment variables (optional):

```bash
# Models directory
export EMAIL_CLASSIFIER_MODELS_DIR=/path/to/models

# API settings
export API_HOST=0.0.0.0
export API_PORT=8000
export API_CORS_ORIGINS='["http://localhost:5173"]'

# Logging
export LOG_LEVEL=INFO
```

### MLflow Integration

Track experiments and model versions:

```bash
# Start MLflow UI
mlflow ui
# → http://localhost:5000

# Train new model with tracking
python src/spam_detector/utils/train_with_mlflow.py
```

Models are versioned in `models/` and tracked with Git LFS.

## 📦 Package Structure

### Domain Layer (Pure Business Logic)

```python
from spam_detector.domain.entities import Email, SinglePrediction
from spam_detector.domain.services import RiskAssessmentService

# No infrastructure dependencies!
email = Email(text="Suspicious email")
# Process...
```

### Application Layer (Use Cases)

```python
from spam_detector.application import EmailClassifierUseCase

# Orchestrates domain services and infrastructure
classifier = EmailClassifierUseCase(container)
result = classifier.execute(email_text)
```

### Infrastructure Layer (Adapters)

```python
# FastAPI adapter
from spam_detector.infrastructure.api.main import app

# CLI adapter  
from spam_detector.infrastructure.cli.main import app as cli_app

# ML adapter
from spam_detector.infrastructure.adapters.sklearn_predictor import SklearnPredictor
```

## 🐳 Docker

### Build Image

```bash
docker build -t spam-detector-backend .
```

### Run Container

```bash
docker run -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  spam-detector-backend
```

### Docker Compose

```bash
# From project root
docker-compose up backend
```

## 🔐 Security

- ✅ Input validation with Pydantic
- ✅ CORS configured (development: `*`, production: whitelist)
- ✅ No secrets in code
- ✅ Type safety with mypy strict mode
- ✅ Dependency scanning (add Snyk/Dependabot)
- ⚠️ Rate limiting (TODO for production)
- ⚠️ API authentication (TODO for production)

## 📊 Model Information

### SPAM Detector

- **Algorithm**: Logistic Regression
- **Vectorizer**: TF-IDF (max 5000 features)
- **Accuracy**: ~95%
- **Training samples**: 5,572
- **Inference time**: <10ms

### PHISHING Detector

- **Algorithm**: Logistic Regression
- **Vectorizer**: TF-IDF (max 5000 features)
- **Accuracy**: ~92%
- **Training samples**: 11,430
- **Inference time**: <10ms

### Risk Levels

| Score | Level | Description |
|-------|-------|-------------|
| 0-25 | LOW | Safe email |
| 26-50 | MEDIUM | Caution advised |
| 51-75 | HIGH | Likely malicious |
| 76-100 | CRITICAL | Immediate action required |

## 🚢 Production Deployment

### Environment Setup

```bash
# Production settings
export API_RELOAD=false
export API_WORKERS=4
export API_CORS_ORIGINS='["https://yourdomain.com"]'
export LOG_LEVEL=WARNING
```

### Deployment Options

**Option 1: Docker**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

**Option 2: Railway/Render**
- Push to GitHub
- Connect repository
- Set environment variables
- Deploy

**Option 3: AWS ECS/EKS**
- Build and push image to ECR
- Create ECS task definition
- Deploy to ECS/EKS cluster

### Health Checks

```bash
# Basic health
curl http://localhost:8000/health

# API docs (should be disabled in prod)
curl http://localhost:8000/docs
```

## 🐛 Troubleshooting

### Models not loading

```bash
# Ensure Git LFS is installed
git lfs install
git lfs pull

# Check models directory
ls -la models/
# Should see .joblib files

# Verify symlinks
ls -la models/*_latest.joblib
```

### Import errors

```bash
# Reinstall package in editable mode
uv sync

# Verify installation
python -c "from spam_detector.infrastructure.api.main import app; print('OK')"
```

### Tests failing

```bash
# Update test dependencies
uv sync

# Clear cache
pytest --cache-clear

# Run with verbose output
pytest -vv
```

### API won't start

```bash
# Check port availability
lsof -i :8000

# Kill process on port 8000
kill -9 $(lsof -t -i:8000)

# Start with different port
uvicorn spam_detector.infrastructure.api.main:app --port 8001
```

## 📚 Resources

- **FastAPI**: https://fastapi.tiangolo.com
- **Pydantic**: https://docs.pydantic.dev
- **scikit-learn**: https://scikit-learn.org
- **MLflow**: https://mlflow.org
- **uv**: https://github.com/astral-sh/uv

## 🤝 Contributing

1. Create feature branch
2. Make changes
3. Run tests: `pytest`
4. Type check: `mypy src/`
5. Format: `ruff format .`
6. Lint: `ruff check .`
7. Commit and push
8. Create PR

## 📄 License

MIT License - see LICENSE file

---

**Built with 💪 for production ML systems**
