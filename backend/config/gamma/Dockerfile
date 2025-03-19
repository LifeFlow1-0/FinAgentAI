# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENVIRONMENT=gamma

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY requirements.txt .
COPY config/gamma/requirements.txt ./config/gamma/

# Install gamma dependencies
RUN pip3 install --no-cache-dir -r config/gamma/requirements.txt

# Create directory for Prometheus metrics
RUN mkdir -p /tmp/prometheus-metrics && \
    chmod 777 /tmp/prometheus-metrics

# Copy project files
COPY app/ app/

# Expose ports for app and monitoring
EXPOSE 8000 9090

# Command to run the application with monitoring
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"] 