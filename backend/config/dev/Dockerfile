# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENVIRONMENT=development

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY requirements.txt .
COPY config/dev/requirements.txt ./config/dev/

# Install development dependencies
RUN pip3 install --no-cache-dir -r config/dev/requirements.txt

# Copy project files
COPY app/ app/
COPY tests/ tests/
COPY alembic.ini .
COPY alembic/ alembic/

# Expose port
EXPOSE 8000

# Command to run the application with auto-reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 