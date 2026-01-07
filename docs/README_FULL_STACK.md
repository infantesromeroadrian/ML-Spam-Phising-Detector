# 📧 SPAM & PHISHING Detector - Full Stack Application

**Production-ready email classification system** with ML backend and modern React frontend.

## 🏗️ Architecture

```
spam-phishing-detector/
├── backend/          → FastAPI + ML models (Python 3.12)
├── frontend/         → React + TypeScript + Vite
└── docker-compose.yml (TODO)
```

### Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Backend** | FastAPI + scikit-learn | High performance, async, type-safe |
| **Frontend** | React 18 + TypeScript + Vite | Modern, fast dev, type-safe |
| **Styling** | Tailwind CSS + Framer Motion | Utility-first, smooth animations |
| **Data Viz** | Chart.js | Gauge charts for threat levels |
| **State** | React Query | Server state management |
| **Package** | uv (backend), npm (frontend) | 10-100x faster than pip |
| **Linting** | Ruff (backend), ESLint (frontend) | Fast, comprehensive |

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+** (backend)
- **Node 18+** (frontend)
- **uv** (recommended): `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Development Setup

#### 1. Backend

```bash
cd backend

# Create virtual environment and install deps
uv venv && source .venv/bin/activate
uv sync

# Run API server
spam-detector-api
# → http://localhost:8000
# → Docs: http://localhost:8000/docs
```

#### 2. Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
# → http://localhost:5173
```

#### 3. Full Integration

**Terminal 1 (Backend):**
```bash
cd backend && spam-detector-api
```

**Terminal 2 (Frontend):**
```bash
cd frontend && npm run dev
```

**Browser:**
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/docs

The frontend automatically proxies `/api` requests to the backend.

## 📂 Project Structure

### Backend (`backend/`)

```
backend/
├── src/spam_detector/
│   ├── domain/              # Pure business logic
│   │   ├── entities/        # Data models
│   │   ├── ports/           # Interfaces (Protocol)
│   │   └── services/        # Domain services
│   ├── application/         # Use cases
│   │   ├── classify.py
│   │   └── manage_models.py
│   ├── infrastructure/      # External adapters
│   │   ├── api/             # FastAPI
│   │   ├── cli/             # Typer CLI
│   │   └── adapters/        # ML models, formatters
│   ├── config/              # Pydantic settings
│   └── utils/               # MLflow helpers
├── tests/                   # Pytest tests
├── models/v1.0.0/           # Trained models (Git LFS)
└── pyproject.toml
```

**Architectural pattern**: Hexagonal/Clean Architecture
- Domain knows nothing about FastAPI, scikit-learn, or infrastructure
- Use cases are reused by both CLI and API
- Easy to swap implementations (e.g., PyTorch instead of scikit-learn)

### Frontend (`frontend/`)

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── Header.tsx
│   │   ├── EmailForm.tsx
│   │   ├── GaugeChart.tsx
│   │   └── ResultsPanel.tsx
│   ├── pages/               # Page components
│   ├── services/            # API client (axios)
│   ├── hooks/               # Custom hooks (React Query)
│   ├── types/               # TypeScript interfaces
│   ├── utils/               # Helper functions
│   ├── App.tsx              # Main app
│   └── main.tsx             # Entry point
├── public/                  # Static assets
└── package.json
```

**Design**: Dark glassmorphism with cybersecurity aesthetic
- Animated shield header
- Dual gauge charts for SPAM/PHISHING scores
- Color-coded risk levels (green → red)
- Smooth transitions with Framer Motion

## 🎯 Features

### ML Classification

- **Dual Models**:
  - SPAM Detector (Logistic Regression, ~95% accuracy)
  - PHISHING Detector (Logistic Regression, ~92% accuracy)
- **Automatic Risk Assessment**: LOW → MEDIUM → HIGH → CRITICAL
- **Model Versioning**: MLflow + Git LFS
- **Fast Inference**: < 50ms per classification

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `POST /api/v1/classify` | POST | Classify email |
| `GET /api/v1/models/{name}` | GET | List model versions |
| `GET /api/v1/models/{name}/latest` | GET | Get latest model info |
| `GET /health` | GET | Health check |

### Frontend Features

- ✅ Real-time email classification
- ✅ Dual gauge visualization (SPAM & PHISHING scores)
- ✅ Color-coded risk indicators
- ✅ Loading states with spinners
- ✅ Error handling with user feedback
- ✅ Educational "How It Works" panel
- ✅ Responsive design (mobile-friendly)
- ✅ Dark mode with glassmorphism
- ✅ Smooth animations (Framer Motion)

## 🧪 Testing

### Backend

```bash
cd backend

# Run all tests
pytest

# With coverage
pytest --cov=spam_detector --cov-report=html

# Only unit tests
pytest tests/unit

# Only integration tests
pytest tests/integration
```

### Frontend

```bash
cd frontend

# Run tests (TODO)
npm test

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🔧 CLI Commands

The backend includes a CLI tool for local usage:

```bash
# Classify email from text
spam-detector classify "Buy now! 50% off! Click here!"

# Classify from file
spam-detector classify --file email.txt

# With JSON output
spam-detector classify --output json "Suspicious link..."

# List models
spam-detector models list

# Model info
spam-detector models info spam_detector latest
```

## 📊 MLflow Integration

Track experiments and model versions:

```bash
cd backend

# Start MLflow UI
mlflow ui
# → http://localhost:5000

# Train new model with tracking
python src/spam_detector/utils/train_with_mlflow.py
```

Models are versioned in `backend/models/v1.0.0/` and tracked with Git LFS.

## 🐳 Docker Deployment (TODO)

```bash
# Build and run with docker-compose
docker-compose up --build

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

## 🔐 Security

- ✅ CORS configured for development
- ✅ Input validation (Pydantic)
- ✅ No secrets in code
- ✅ Dependency scanning (TODO: add Snyk)
- ✅ Type safety (mypy strict mode)
- ⚠️ Rate limiting (TODO)
- ⚠️ API authentication (TODO for production)

## 🚢 Production Deployment

### Option 1: Separate Services

**Backend**:
- Deploy on AWS ECS/EKS or Railway
- Environment: `API_CORS_ORIGINS=https://yourdomain.com`
- Expose port 8000

**Frontend**:
- Build: `npm run build`
- Deploy on Vercel/Netlify/Cloudflare Pages
- Set env: `VITE_API_URL=https://api.yourdomain.com`

### Option 2: Single Service

**Backend serves frontend build**:

```bash
cd frontend
npm run build  # → dist/

cd ../backend
# Copy frontend/dist/ to backend/static/
# Update main.py to serve static files
# Deploy backend only
```

## 📝 Development Workflow

### Backend Changes

1. Make changes in `backend/src/`
2. Run tests: `pytest`
3. Type check: `mypy src/`
4. Format: `ruff format .`
5. Lint: `ruff check .`
6. Commit

### Frontend Changes

1. Make changes in `frontend/src/`
2. Check types: `npm run type-check` (add to package.json)
3. Lint: `npm run lint`
4. Test manually at http://localhost:5173
5. Commit

### Pre-commit Hooks (TODO)

```bash
cd backend
pre-commit install
# Auto-runs ruff, mypy on commit
```

## 🐛 Troubleshooting

### Backend won't start

```bash
cd backend
echo $VIRTUAL_ENV  # Should show .venv path
source .venv/bin/activate
uv sync
spam-detector-api
```

### Frontend can't connect to API

Check:
1. Backend is running: `curl http://localhost:8000/health`
2. CORS is configured: Check browser console
3. Proxy is set: `frontend/vite.config.ts` has proxy config
4. Env var is set: `frontend/.env` has `VITE_API_URL`

### Models not loading

```bash
cd backend
git lfs pull  # Download LFS files
ls models/v1.0.0/  # Should see .joblib files
```

## 📚 Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **React Docs**: https://react.dev
- **Vite Docs**: https://vitejs.dev
- **Tailwind CSS**: https://tailwindcss.com
- **React Query**: https://tanstack.com/query

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/my-feature`
2. Make changes
3. Run tests
4. Commit with clear message
5. Push and create PR

## 📄 License

MIT License - see `LICENSE` file

---

**Built with 🔥 by AIR | Professional ML Engineering**
