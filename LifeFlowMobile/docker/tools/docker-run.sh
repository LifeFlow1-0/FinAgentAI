#!/bin/bash

# This script helps run the appropriate Docker environment

# Function to display usage info
function show_usage {
  echo "Usage: ./docker-run.sh [environment] [command]"
  echo "Environments:"
  echo "  dev         - Development environment"
  echo "  gamma       - Gamma (staging) environment"
  echo "  prod        - Production environment"
  echo ""
  echo "Commands (optional, only valid with dev environment):"
  echo "  test        - Run tests"
  echo "  start       - Start the development server (default)"
  exit 1
}

# Check if environment argument is provided
if [ $# -eq 0 ]; then
  show_usage
fi

# Process based on environment argument
case "$1" in
  dev)
    if [ "$2" == "test" ]; then
      echo "Running tests in development environment..."
      docker-compose run --rm dev npm test -- --config=jest.config.js
    else
      echo "Starting development environment..."
      docker-compose up dev
    fi
    ;;
  gamma)
    echo "Starting gamma (staging) environment..."
    docker-compose up gamma
    ;;
  prod)
    echo "Starting production environment..."
    docker-compose up prod
    ;;
  *)
    echo "Unknown environment: $1"
    show_usage
    ;;
esac 