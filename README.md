# 🛡️ Email Threat Intelligence Platform

[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.109+-green.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-black)](https://github.com/astral-sh/ruff)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Production-ready email threat detection system** using Machine Learning. Dual SPAM + Phishing classification with professional SOC-style dashboard.

![Dashboard Preview](docs/dashboard-preview.png)

## 🏗️ Project Structure

```
ML-Spam-Phishing-Detector/
├── src/
│   ├── backend/                  # FastAPI + ML (Python 3.12)
│   │   ├── spam_detector/        # Hexagonal architecture
│   │   │   ├── domain/           # Business entities
│   │   │   ├── application/      # Use cases
│   │   │   └── infrastructure/   # API, CLI, adapters
│   │   ├── tests/                # Unit + integration tests
│   │   ├── Dockerfile            # Multi-stage, non-root
│   │   └── pyproject.toml        # Dependencies (uv)
│   │
│   └── frontend/                 # Professional SOC Dashboard
│       ├── index.html            # Main dashboard
│       ├── css/styles.css        # Dark theme (1000+ lines)
│       ├── js/app.js             # API client & UI controller
│       ├── nginx.conf            # Nginx configuration
│       └── Dockerfile            # Nginx Alpine
│
├── models/                       # ML models (Git LFS)
│   ├── spam_detector_*_latest.joblib
│   ├── phishing_detector_*_latest.joblib
│   └── v1.0.0/                   # Versioned models
│
├── docker-compose.yml            # Full-stack deployment
└── README.md
```

## ✨ Features

### 🎯 ML Detection
- **Dual Analysis**: SPAM + Phishing classification in parallel
- **High Accuracy**: ~95% SPAM, ~92% Phishing detection
- **Fast Inference**: <10ms per email
- **Threat Intelligence Report**: Risk score, IOCs, trigger words

### 🖥️ SOC-Style Dashboard
- **Dark Theme**: Professional cybersecurity design
- **Real-time Analysis**: Instant classification results
- **Threat Visualization**: Risk gauges, IOC panels, recommendations
- **Sample Threats**: Pre-loaded examples for testing

### 🏛️ Architecture
- **Backend**: Hexagonal/Clean Architecture (FastAPI)
- **Frontend**: Vanilla HTML/CSS/JS (zero dependencies)
- **Containers**: Multi-stage builds, non-root user
- **Models**: Mounted as Docker volume (hot-swap capable)

## 🚀 Quick Start

### Prerequisites
- **Docker** + **Docker Compose** (recommended)
- Or: Python 3.12+ with `uv`

### Option 1: Docker Compose (Recommended)

```bash
# Clone repository
git clone https://github.com/infantesromeroadrian/ML-Spam-Phising-Detector.git
cd ML-Spam-Phising-Detector

# Build and run
docker compose build
docker compose up -d

# Verify containers are healthy
docker compose ps

# Access:
# - Dashboard: http://localhost:3000
# - API Docs:  http://localhost:8000/docs
```

### Option 2: Local Development

```bash
# Backend
cd src/backend
uv venv && source .venv/bin/activate
uv sync
uvicorn spam_detector.infrastructure.api.main:app --reload
# → http://localhost:8000

# Frontend (serve static files)
cd src/frontend
python -m http.server 3000
# → http://localhost:3000
```

## 📊 ML Models

| Model | Algorithm | Accuracy | Dataset Size |
|-------|-----------|----------|--------------|
| SPAM | Logistic Regression | ~95% | 5,572 emails |
| Phishing | Logistic Regression | ~92% | 11,430 emails |

Models use TF-IDF vectorization (5000 features) and are tracked with **Git LFS**.

## 🔌 API Usage

### Health Check

```bash
curl http://localhost:8000/health
```

```json
{
  "status": "healthy",
  "models_loaded": true,
  "models": {"spam": true, "phishing": true}
}
```

### Classify Email

```bash
curl -X POST http://localhost:8000/api/v1/classify \
  -H "Content-Type: application/json" \
  -d '{"email_text": "URGENT! You won $1,000,000! Click here now!"}'
```

```json
{
  "verdict": "SPAM+PHISHING",
  "risk_level": "CRITICAL",
  "is_malicious": true,
  "spam_probability": 0.68,
  "phishing_probability": 0.96,
  "execution_time_ms": 1.2,
  "threat_report": {
    "risk_score": 87,
    "iocs": [
      {"type": "keyword_financial", "value": "winner, prize", "severity": "critical"},
      {"type": "pattern", "value": "$1,000,000", "severity": "medium"}
    ],
    "recommendations": [
      "🚫 Quarantine this email immediately",
      "🔒 Block sender domain"
    ],
    "spam_trigger_words": [
      {"word": "claim", "contribution": 0.82},
      {"word": "prize", "contribution": 0.67}
    ]
  }
}
```

### Interactive API Docs

Visit `http://localhost:8000/docs` for Swagger UI.

## 🐳 Docker Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Compose                        │
├─────────────────────────┬───────────────────────────────┤
│      Frontend           │          Backend              │
│    (Nginx Alpine)       │      (Python 3.12)            │
│                         │                               │
│  ┌─────────────────┐    │    ┌─────────────────────┐    │
│  │   index.html    │    │    │     FastAPI         │    │
│  │   css/styles    │    │    │   /api/v1/classify  │    │
│  │   js/app.js     │────┼───▶│   /health           │    │
│  └─────────────────┘    │    └──────────┬──────────┘    │
│                         │               │               │
│    Port 3000            │    Port 8000  │               │
└─────────────────────────┴───────────────┼───────────────┘
                                          │
                                          ▼
                                ┌─────────────────┐
                                │  models/        │
                                │  (volume mount) │
                                └─────────────────┘
```

**Key Features:**
- Multi-stage builds (minimal image size)
- Non-root user (`appuser`, UID 1001)
- Health checks on both containers
- Models mounted as read-only volume

## 🧪 Testing

```bash
cd src/backend

# Run all tests
pytest

# With coverage
pytest --cov=spam_detector

# Only unit tests
pytest tests/unit
```

## 🎨 Dashboard Features

| Feature | Description |
|---------|-------------|
| **Email Input** | Large text area for pasting emails |
| **Sample Threats** | Pre-loaded SPAM, Phishing, and Combined examples |
| **Risk Gauge** | Visual 0-100 risk score indicator |
| **Dual Verdicts** | Side-by-side SPAM and Phishing results |
| **IOC Panel** | Detected Indicators of Compromise |
| **Trigger Words** | ML feature analysis with contribution scores |
| **Recommendations** | Actionable security guidance |
| **Backend Status** | Real-time API health indicator |

## 🔐 Security

- ✅ Input validation (Pydantic schemas)
- ✅ CORS configured for frontend origin
- ✅ Non-root Docker containers
- ✅ No secrets in codebase
- ✅ Type safety (mypy strict mode)
- ✅ Models mounted read-only

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | HTML5, CSS3, Vanilla JS |
| **Web Server** | Nginx Alpine |
| **Backend** | FastAPI, Pydantic |
| **ML** | scikit-learn, NLTK |
| **Containers** | Docker, Docker Compose |
| **Package Manager** | uv (Python) |
| **Linting** | ruff, mypy |
| **Testing** | pytest |

## 📝 License

MIT License - see [LICENSE](LICENSE)

## 👤 Author

**Adrian Infantes Romero**

---

**⚡ Built for production ML systems with security-first design**
