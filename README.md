# 📧 ML SPAM & PHISHING Detector

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-123%20passed-success)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-86.82%25-brightgreen)](htmlcov/)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-black)](https://github.com/astral-sh/ruff)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Production-ready email classifier for detecting SPAM and PHISHING threats using Machine Learning**

Built with Clean Architecture principles, this tool provides CLI, REST API, and Web UI interfaces for email threat detection, featuring dual classification models trained on real-world datasets.

---

## ✨ Features

- 🎯 **Dual Detection**: Simultaneous SPAM and PHISHING classification
- 🚀 **Multiple Interfaces**:
  - CLI tool with Rich terminal UI
  - REST API with FastAPI
  - Interactive Web Dashboard with Chart.js gauges
- 📊 **ML Pipeline**: Logistic Regression models with TF-IDF vectorization
- 🏗️ **Clean Architecture**: Hexagonal/Ports & Adapters pattern
- 🧪 **Well Tested**: 86.82% coverage with 123 passing tests
- ⚙️ **Configurable**: Environment variables, CLI flags, and settings file
- 📦 **Type-Safe**: Full type hints with Pydantic validation

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/infantesromeroadrian/ML-Spam-Phising-Detector.git
cd ML-Spam-Phising-Detector

# Create virtual environment with uv (recommended)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv sync

# Verify installation
email-classifier --help
```

### Usage

#### CLI - Classify Email

```bash
# From text
email-classifier predict "URGENT! Click here to claim your prize NOW!"
# Output: 🚨 SPAM+PHISHING (95.4% confidence)

# From file
email-classifier predict --file email.txt

# JSON output
email-classifier predict "Test email" --format json

# Detailed analysis
email-classifier predict "Test" --detail detailed
```

#### API - Start Server

```bash
# Start API server
email-classifier-api

# API available at: http://localhost:8000
# Docs: http://localhost:8000/docs
# Web UI: http://localhost:8000/static/index.html
```

#### API - Example Request

```bash
curl -X POST "http://localhost:8000/api/v1/classify" \
  -H "Content-Type: application/json" \
  -d '{
    "email_text": "WINNER! You won $1M! Click NOW!",
    "subject": "URGENT: Claim Prize",
    "sender": "noreply@fake-lottery.com"
  }'
```

**Response:**
```json
{
  "verdict": "SPAM+PHISHING",
  "risk_level": "CRITICAL",
  "spam_probability": 0.923,
  "phishing_probability": 0.987,
  "spam_prediction": "SPAM",
  "phishing_prediction": "PHISHING",
  "confidence": 0.987,
  "is_malicious": true,
  "execution_time_ms": 1.24
}
```

---

## 🏗️ Architecture

### Clean Architecture (Hexagonal)

```
┌─────────────────────────────────────────┐
│     DRIVING ADAPTERS                    │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │   CLI   │  │FastAPI  │  │Frontend │ │
│  │ (Typer) │  │   API   │  │   Web   │ │
│  └────┬────┘  └────┬────┘  └────┬────┘ │
└───────┼───────────┼─────────────┼───────┘
        │           │             │
┌───────▼───────────▼─────────────▼───────┐
│         APPLICATION LAYER                │
│    Use Cases + Dependency Injection      │
└────────────────────┬─────────────────────┘
                     │
┌────────────────────▼─────────────────────┐
│           DOMAIN LAYER                   │
│  Entities · Services · Ports (Pure)     │
└─────────────────────┬───────────────────┘
                      │
┌─────────────────────▼───────────────────┐
│      INFRASTRUCTURE LAYER               │
│  Adapters: Sklearn · Joblib · Rich     │
└─────────────────────────────────────────┘
```

### Key Design Principles

✅ **SOLID Principles**  
✅ **Domain-Driven Design (DDD)**  
✅ **Dependency Inversion** - Domain doesn't know infrastructure  
✅ **Ports & Adapters** - Easy to swap implementations  
✅ **Single Responsibility** - Each module has one job  

---

## 📁 Project Structure

```
.
├── src/ml_engineer_course/
│   ├── domain/                  # Core business logic (pure)
│   │   ├── entities/            # Email, Prediction, Metadata
│   │   ├── services/            # EmailClassifierService
│   │   ├── ports/               # Interfaces (IPredictor, IModelLoader)
│   │   └── constants.py         # Domain constants
│   │
│   ├── application/             # Use cases & orchestration
│   │   ├── use_cases/           # ClassifyEmail, ListModels
│   │   └── container.py         # Dependency Injection
│   │
│   ├── infrastructure/          # Adapters & external integrations
│   │   ├── adapters/            # SklearnPredictor, JoblibModelLoader
│   │   ├── api/                 # FastAPI (routers, schemas)
│   │   ├── cli/                 # Typer CLI
│   │   └── web/                 # Frontend (HTML, CSS, JS)
│   │
│   └── config/
│       └── settings.py          # Pydantic Settings
│
├── tests/                       # 123 tests (unit + integration)
│   ├── unit/                    # Fast, isolated tests
│   └── integration/             # End-to-end tests
│
├── models/                      # ML models (trained separately)
├── pyproject.toml               # Project dependencies
└── uv.lock                      # Locked dependencies
```

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# With coverage report
pytest tests/ --cov=src --cov-report=html

# Open coverage report
open htmlcov/index.html

# Run only unit tests
pytest tests/unit/

# Run only integration tests
pytest tests/integration/
```

**Current Coverage:** 86.82% (123 tests passing)

---

## ⚙️ Configuration

### Environment Variables

All settings can be configured via environment variables with prefix `EMAIL_CLASSIFIER_`:

```bash
# Model settings
export EMAIL_CLASSIFIER_MODELS_DIR=/path/to/models

# API settings
export EMAIL_CLASSIFIER_API_HOST=0.0.0.0
export EMAIL_CLASSIFIER_API_PORT=8000

# Output settings
export EMAIL_CLASSIFIER_DEFAULT_FORMAT=json
export EMAIL_CLASSIFIER_VERBOSE=true
```

### Settings File

Create `.env` file in project root:

```env
EMAIL_CLASSIFIER_MODELS_DIR=models
EMAIL_CLASSIFIER_API_PORT=8000
EMAIL_CLASSIFIER_DEFAULT_FORMAT=text
EMAIL_CLASSIFIER_VERBOSE=false
```

---

## 🔧 Development

### Setup Development Environment

```bash
# Install with all dev dependencies
uv sync

# Install pre-commit hooks (optional)
uv add --dev pre-commit
pre-commit install

# Run linter
ruff check src/

# Auto-fix linting issues
ruff check src/ --fix

# Format code
ruff format src/

# Type checking (if mypy is installed)
mypy src/
```

### Training New Models

Models are trained separately using Jupyter notebooks (not included in this repo).

To use your own models:

1. Train your model with scikit-learn Logistic Regression
2. Save model components using joblib:
   ```python
   import joblib
   from datetime import datetime
   
   timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
   joblib.dump(model, f"models/spam_detector_model_{timestamp}.joblib")
   joblib.dump(vectorizer, f"models/spam_detector_vectorizer_{timestamp}.joblib")
   joblib.dump(metadata, f"models/spam_detector_metadata_{timestamp}.joblib")
   ```
3. Place models in `models/` directory

**Expected model structure:**
- `{model_name}_model_{timestamp}.joblib` - Trained model
- `{model_name}_vectorizer_{timestamp}.joblib` - TF-IDF vectorizer
- `{model_name}_metadata_{timestamp}.joblib` - Model metadata (accuracy, date, etc.)

Supported model names: `spam_detector`, `phishing_detector`

---

## 📊 Tech Stack

| Category | Technology |
|----------|-----------|
| **Language** | Python 3.10+ |
| **ML Framework** | scikit-learn |
| **NLP** | NLTK, TF-IDF |
| **CLI** | Typer, Rich |
| **API** | FastAPI, Uvicorn |
| **Frontend** | Vanilla JS, Chart.js |
| **Validation** | Pydantic |
| **Testing** | pytest, pytest-cov |
| **Code Quality** | Ruff |
| **Package Manager** | uv |

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests: `pytest tests/`
5. Ensure coverage >80%: `pytest --cov=src`
6. Format code: `ruff format src/`
7. Commit changes (`git commit -m 'feat: add amazing feature'`)
8. Push to branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

**Code Requirements:**
- ✅ Tests passing (pytest)
- ✅ Coverage >80%
- ✅ Type hints on all functions
- ✅ Docstrings on public APIs
- ✅ Ruff formatting applied

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **scikit-learn** - Machine learning framework
- **FastAPI** - Modern web framework
- **Typer** - CLI framework
- **Rich** - Terminal formatting
- **Chart.js** - Interactive charts

---

## 📧 Contact

**Adrian Infantes Romero**  
GitHub: [@infantesromeroadrian](https://github.com/infantesromeroadrian)

---

## 🎓 Learning Outcomes

This project demonstrates:

- ✅ **Clean Architecture** in Python (Hexagonal/Ports & Adapters)
- ✅ **Domain-Driven Design** practical implementation
- ✅ **Dependency Injection** without frameworks
- ✅ **Type Safety** with Pydantic and type hints
- ✅ **Test-Driven Development** (86% coverage)
- ✅ **Multiple Interface Patterns** (CLI, API, Web)
- ✅ **MLOps Basics** (model versioning, metadata tracking)

**Perfect for demonstrating ML Engineering skills in interviews and portfolios.**

---

**Made with ❤️ by Adrian Infantes**
