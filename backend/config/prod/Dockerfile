# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENVIRONMENT=production

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser

# Copy requirements files
COPY requirements.txt .
COPY config/prod/requirements.txt ./config/prod/

# Install production dependencies
RUN pip3 install --no-cache-dir -r config/prod/requirements.txt

# Create directory for Prometheus metrics
RUN mkdir -p /tmp/prometheus-metrics && \
    chmod 777 /tmp/prometheus-metrics

# Copy project files
COPY app/ app/

# Set ownership to non-root user
RUN chown -R appuser:appuser /app /tmp/prometheus-metrics

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Command to run the application with Gunicorn and Uvicorn workers
CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"] 