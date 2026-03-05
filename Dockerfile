# This Dockerfile is used to create a production-ready image
# for a FastAPI application managed with Poetry.

# ============================================================
# 1. Builder Stage — Install Poetry, Dependencies, and App
# ============================================================
FROM python:3.11-slim AS builder

# Environment variables for Poetry
ENV POETRY_VERSION=2.1.4 \
    POETRY_HOME=/opt/poetry \
    PATH=/opt/poetry/bin:$PATH \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies for Poetry and build tools
RUN apt-get update \
    && apt-get install --no-install-recommends -y curl build-essential \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy only dependency files first (better Docker caching)
COPY pyproject.toml poetry.lock README.md ./

# Required for poetry to build the app package
COPY src ./src

# Install dependencies (no dev dependencies, no root virtualenv)
RUN poetry config virtualenvs.create false \
    && poetry install --without dev

# ============================================================
# 2. Final Stage — Slim, Production-Ready Image
# ============================================================
FROM python:3.11-slim

ENV PYTHONPATH="/app/src:${PYTHONPATH}" \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONUNBUFFERED=1

# Install curl for health checks
RUN apt-get update \
    && apt-get install --no-install-recommends -y curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy installed app + dependencies from builder stage
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app/src ./src

# Note: .env is NOT copied into the image for security reasons.
# Environment variables should be provided at runtime via:
# - docker run -e or --env-file
# - docker-compose environment or env_file
# - Kubernetes ConfigMaps/Secrets

EXPOSE 8000
CMD ["uvicorn", "awesomeapp.main:app", "--host", "0.0.0.0", "--port", "8000"]
