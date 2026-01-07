"""FastAPI application entry point."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from ...application import Container
from ...config import settings
from .routers import classify, models


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Manage application lifespan events.

    Handles startup and shutdown:
    - Startup: Initialize DI container, load models
    - Shutdown: Cleanup resources
    """
    # Startup: Initialize container
    container = Container(settings)

    # Store container in app state for dependency injection
    app.state.container = container

    yield

    # Shutdown: cleanup if needed
    # (Currently no cleanup needed, but hook is here for future)


# Create FastAPI application
app = FastAPI(
    title="Email Classifier API",
    description="""
    **SPAM & PHISHING Detection API**

    High-performance email classification system using dual machine learning models
    to detect spam and phishing threats.

    ## Features

    - **Dual Classification**: Separate spam and phishing detection models
    - **Risk Assessment**: Automatic risk level categorization (LOW/MEDIUM/HIGH/CRITICAL)
    - **Model Versioning**: Multiple model versions with metadata
    - **Fast**: Optimized for low-latency predictions
    - **Type-Safe**: Full Pydantic validation on inputs and outputs

    ## Usage

    1. **Classify Email**: POST to `/api/v1/classify` with email text
    2. **List Models**: GET `/api/v1/models/{model_name}` for available versions
    3. **Latest Model**: GET `/api/v1/models/{model_name}/latest` for current version

    ## Architecture

    Built using Clean Architecture / Hexagonal Architecture principles:
    - **Domain Layer**: Pure business logic (entities, rules)
    - **Application Layer**: Use cases (orchestration)
    - **Infrastructure Layer**: FastAPI, ML models, formatters

    This API is a *driving adapter* that reuses the same use cases as the CLI tool.
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url=settings.docs_path,
    redoc_url=settings.redoc_path,
    openapi_url="/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.api_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    classify.router,
    prefix=settings.api_base_path,
    tags=["Classification"],
)
app.include_router(
    models.router,
    prefix=settings.api_base_path,
    tags=["Models"],
)

# Frontend is now a separate React app
# In dev: runs on http://localhost:5173
# In prod: build and serve via nginx or serve static build here


@app.get("/", tags=["Health"], response_class=HTMLResponse)
def root() -> str:
    """
    Root endpoint - Redirect to frontend UI.

    Returns:
        HTML page with links to frontend and API docs
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Email Classifier</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                margin: 0;
                color: white;
                text-align: center;
            }
            .container {
                max-width: 600px;
                padding: 2rem;
            }
            h1 {
                font-size: 3rem;
                margin-bottom: 1rem;
            }
            p {
                font-size: 1.25rem;
                margin-bottom: 2rem;
                opacity: 0.9;
            }
            .links {
                display: flex;
                gap: 1rem;
                justify-content: center;
                flex-wrap: wrap;
            }
            a {
                display: inline-block;
                padding: 1rem 2rem;
                background: white;
                color: #667eea;
                text-decoration: none;
                border-radius: 0.5rem;
                font-weight: 600;
                transition: transform 0.2s;
            }
            a:hover {
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📧 Email Classifier</h1>
            <p>AI-Powered SPAM & PHISHING Detection</p>
            <div class="links">
                <a href="http://localhost:5173" target="_blank">🚀 Launch App (Dev)</a>
                <a href="/docs">📚 API Docs</a>
                <a href="/redoc">📖 Reference</a>
            </div>
        </div>
    </body>
    </html>
    """


@app.get("/health", tags=["Health"])
def health() -> dict[str, str]:
    """
    Health check endpoint.

    Returns:
        Health status
    """
    return {"status": "healthy"}


def run_api() -> None:
    """
    Run the API server with uvicorn.

    This is the entry point for the CLI command: email-classifier-api
    """
    import uvicorn

    uvicorn.run(
        "spam_detector.infrastructure.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
        workers=settings.api_workers,
    )


if __name__ == "__main__":
    run_api()
