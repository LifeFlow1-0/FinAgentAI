# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.7.1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# TODO: Improvement needed
# - Split requirements into requirements.txt (production) and requirements-dev.txt (development)
# - Use multi-stage Docker builds to separate development and production environments
# - Current setup installs development tools (pytest, flake8, black, isort) in production image
# - This increases image size and includes unnecessary tools in production
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest flake8 black isort

# Copy project files
COPY app/ app/

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 