FROM python:3.12.3-slim

# PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files
# PYTHONUNBUFFERED: Forces stdout and stderr to be unbuffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
ARG POETRY_VERSION=1.8.3
RUN pip install "poetry==${POETRY_VERSION}"
COPY pyproject.toml poetry.lock ./

# Install only production dependencies (no dev)
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy application code
COPY . /app/

COPY .env /app/.env

# Add entry scripts
RUN chmod +x /app/scripts/entrypoint.sh /app/scripts/wait-for-db.sh

# Create a non-root user and set permissions
RUN adduser --disabled-password --gecos '' appuser && \
    mkdir -p /app/celery && \
    chown -R appuser:appuser /app && \
    chmod -R u+rw /app/celery

USER appuser

EXPOSE 5000
