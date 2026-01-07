# 📁 Project Structure Documentation

## Overview

Professional full-stack ML application following modern monorepo best practices.

## Directory Layout

```
spam-phishing-detector/
├── src/                      # 🎯 SOURCE CODE (all application code)
│   ├── backend/              # FastAPI + ML backend
│   └── frontend/             # React + TypeScript frontend
│
├── docs/                     # 📚 DOCUMENTATION
│   ├── README_FULL_STACK.md
│   ├── PROJECT_STRUCTURE.md  (this file)
│   └── [ML theory docs]
│
├── docker-compose.yml        # 🐳 ORCHESTRATION (full-stack deployment)
├── README.md                 # 📖 MAIN DOCUMENTATION (project overview)
├── LICENSE                   # ⚖️ MIT License
└── .gitignore
```

## Source Code (`src/`)

### Backend (`src/backend/`)

```
src/backend/
├── spam_detector/            # Python package (flat layout)
│   ├── domain/               # Business logic
│   ├── application/          # Use cases
│   ├── infrastructure/       # External adapters
│   ├── config/               # Settings
│   └── utils/                # MLflow helpers
│
├── tests/                    # Test suite
│   ├── unit/                 # Unit tests
│   └── integration/          # Integration tests
│
├── models/                   # ML models (Git LFS)
│   ├── v1.0.0/
│   └── *.joblib
│
├── Dockerfile                # Backend container
├── pyproject.toml            # Python dependencies (uv)
├── pytest.ini                # Test config
└── README.md                 # Backend documentation
```

**Key Features:**
- Hexagonal/Clean Architecture
- Type-safe with Pydantic
- 86.82% test coverage
- FastAPI REST API
- Typer CLI tool

**Commands:**
```bash
cd src/backend

# Setup
uv venv && source .venv/bin/activate
uv sync

# Run
spam-detector predict "Email text"
spam-detector-api

# Test
pytest --cov=spam_detector
```

### Frontend (`src/frontend/`)

```
src/frontend/
├── src/                      # React application
│   ├── components/           # UI components
│   │   ├── Header.tsx
│   │   ├── EmailForm.tsx
│   │   ├── GaugeChart.tsx
│   │   └── ResultsPanel.tsx
│   ├── hooks/                # Custom hooks
│   ├── services/             # API client
│   ├── types/                # TypeScript types
│   └── utils/                # Helpers
│
├── public/                   # Static assets
├── Dockerfile                # Frontend container
├── package.json              # Node dependencies
├── vite.config.ts            # Vite config
├── tailwind.config.js        # Tailwind config
└── README.md                 # Frontend documentation
```

**Key Features:**
- React 18 + TypeScript
- Dark glassmorphism UI
- Tailwind CSS styling
- Framer Motion animations
- Chart.js gauges
- React Query state

**Commands:**
```bash
cd src/frontend

# Setup
npm install
echo "VITE_API_URL=http://localhost:8000" > .env

# Run
npm run dev

# Build
npm run build
```

## Documentation (`docs/`)

| File | Purpose |
|------|---------|
| `README_FULL_STACK.md` | Complete setup and architecture guide |
| `PROJECT_STRUCTURE.md` | This file - directory layout |
| `01-introduccion-ml-*.md` | ML theory documentation |
| `02-funcion-hipotesis-*.md` | ML theory documentation |
| `03-funcion-coste-*.md` | ML theory documentation |
| `04-gradient-descent.md` | ML theory documentation |

## Docker Deployment

### Docker Compose (Full Stack)

**File:** `docker-compose.yml` (root)

**Usage:**
```bash
# From root
docker-compose up --build

# Access:
# - Backend:  http://localhost:8000
# - Frontend: http://localhost:5173
```

**Services:**
- `backend`: Uses `src/backend/Dockerfile`
- `frontend`: Uses `src/frontend/Dockerfile`

### Individual Dockerfiles

**Backend:** `src/backend/Dockerfile`
- Multi-stage build (builder + production)
- Python 3.12-slim base
- uv for dependencies
- Health check included

**Frontend:** `src/frontend/Dockerfile`
- Multi-stage build (builder + nginx)
- Node 18-alpine builder
- Nginx alpine production
- Build args for VITE_API_URL

## READMEs

| README | Location | Purpose | Lines |
|--------|----------|---------|-------|
| Main | `/README.md` | Project overview | 264 |
| Backend | `src/backend/README.md` | Backend setup, API docs | 448 |
| Frontend | `src/frontend/README.md` | Frontend setup, components | 517 |
| Full-Stack | `docs/README_FULL_STACK.md` | Complete guide | 369 |
| Models | `src/backend/models/README.md` | ML models info | 106 |

**Why multiple READMEs?**
- Standard practice in large projects
- Each component has its own documentation
- Easier for developers to find relevant info
- Separation of concerns

## Development Files (Not in Git)

These directories are `.gitignore`d but useful for development:

```
├── historyMD/               # Development notes
│   ├── FASE1_COMPLETADA.md
│   ├── MLFLOW_WORKFLOW_GUIDE.md
│   └── [other notes]
│
├── data/                    # Datasets (local)
├── notebooks/               # Jupyter notebooks (local)
├── mlruns/                  # MLflow artifacts
├── mlflow.db               # MLflow database
│
└── [component-specific]:
    ├── src/backend/.venv/   # Python virtual env
    ├── src/backend/htmlcov/ # Coverage reports
    ├── src/frontend/node_modules/ # Node deps
    └── src/frontend/dist/   # Build output
```

## What Was Cleaned Up

### Removed (Legacy from Root)

- ❌ `ml-course-venv/` - Old virtual environment
- ❌ `htmlcov/` - Legacy coverage reports
- ❌ `.coverage` - Legacy coverage data
- ❌ `pyproject.toml` - Moved to `src/backend/`
- ❌ `pytest.ini` - Moved to `src/backend/`
- ❌ `uv.lock` - Moved to `src/backend/`
- ❌ `tests/` - Moved to `src/backend/tests/`
- ❌ `models/` - Moved to `src/backend/models/`

### Kept (Gitignored, Useful)

- ✅ `historyMD/` - Development notes
- ✅ `README_DEV.md` - Development readme
- ✅ `DEPLOYMENT_CHECKLIST.md` - Deployment notes
- ✅ `data/` - Local datasets
- ✅ `notebooks/` - Jupyter notebooks
- ✅ `mlruns/`, `mlflow.db` - MLflow artifacts

## Git Structure

```
* 6453bc6 (HEAD -> main, tag: v2.0.0)
  refactor: organize code into src/ directory with proper structure

* 7e059cf
  refactor: complete full-stack restructure with modern React frontend

* 7782a6a (tag: v1.0.0, origin/main)
  feat: add professional MLflow tracking and Git LFS model versioning
```

**Tags:**
- `v1.0.0` - Original backend (before full-stack refactor)
- `v2.0.0` - Full-stack with professional structure

## Best Practices Followed

1. ✅ **Monorepo Structure** - All code in `src/`
2. ✅ **Separation of Concerns** - Backend/Frontend isolated
3. ✅ **Multiple READMEs** - Component-specific docs
4. ✅ **Docker Support** - Compose + individual Dockerfiles
5. ✅ **Clean Root** - Only essential configs in root
6. ✅ **Gitignore** - Development artifacts excluded
7. ✅ **Type Safety** - TypeScript + Pydantic
8. ✅ **Testing** - Comprehensive test suites
9. ✅ **Documentation** - Multiple levels of docs
10. ✅ **Versioning** - Git tags for releases

## Next Steps for Developers

### New Developer Setup

```bash
# 1. Clone repo
git clone <repo-url>
cd spam-phishing-detector

# 2. Backend setup
cd src/backend
uv venv && source .venv/bin/activate
uv sync

# 3. Frontend setup
cd ../frontend
npm install

# 4. Run full stack
# Terminal 1:
cd src/backend && spam-detector-api

# Terminal 2:
cd src/frontend && npm run dev
```

### Adding New Features

**Backend:**
1. Create feature branch
2. Add code in `src/backend/src/spam_detector/`
3. Add tests in `src/backend/tests/`
4. Run: `pytest && mypy src/ && ruff check .`
5. Update `src/backend/README.md` if needed

**Frontend:**
1. Create feature branch
2. Add components in `src/frontend/src/components/`
3. Update types in `src/frontend/src/types/`
4. Run: `npm run lint && npm run build`
5. Update `src/frontend/README.md` if needed

## Deployment

### Development
```bash
docker-compose up
```

### Production

**Option 1: Separate Deployments**
- Backend → Railway, Render, AWS ECS
- Frontend → Vercel, Netlify, Cloudflare Pages

**Option 2: Full Stack Docker**
- Build: `docker-compose build`
- Deploy: Push to container registry
- Run: `docker-compose up -d` on server

## Questions?

See:
- Main README: `/README.md`
- Backend docs: `src/backend/README.md`
- Frontend docs: `src/frontend/README.md`
- Full-stack guide: `docs/README_FULL_STACK.md`

---

**Last Updated:** 2026-01-07  
**Version:** v2.0.0  
**Maintained by:** Adrian Infantes Romero
