# ============================================
# Multi-stage build for production-ready API
# ============================================

# -------------------- Builder Stage --------------------
FROM python:3.14-slim AS builder

# Install uv (modern Python package manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files (README.md required by pyproject.toml)
COPY pyproject.toml uv.lock README.md ./

# Install dependencies to /app/.venv (frozen lockfile, no dev deps)
RUN uv sync --frozen --no-dev

# -------------------- Production Stage --------------------
FROM python:3.14-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser -u 1001 appuser

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY --chown=appuser:appuser spam_detector/ /app/spam_detector/

# Create models directory (will be mounted as volume)
RUN mkdir -p /app/models && chown -R appuser:appuser /app/models

# Ensure venv is in PATH
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Enhanced health check (validates /health endpoint)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application with uvicorn (using environment variables for config)
CMD ["uvicorn", "spam_detector.infrastructure.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
