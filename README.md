# LifeFlow Monorepo

This repository contains both the backend and mobile frontend for the LifeFlow application.

## Project Structure

```
lifeflow/
├── backend/           # FastAPI backend
│   ├── app/          # FastAPI application code
│   ├── config/       # Environment-specific configurations
│   │   ├── dev/     # Development environment
│   │   ├── gamma/   # Staging environment
│   │   └── prod/    # Production environment
│   ├── tests/       # Backend tests
│   ├── .env         # Local environment variables
│   ├── .flake8      # Flake8 configuration
│   ├── .isort.cfg   # Import sorting configuration
│   └── requirements.txt  # Base requirements for all environments
├── mobile/          # React Native frontend
│   ├── app/        # React Native components
│   ├── __tests__/  # Frontend tests
│   └── package.json
├── .github/        # GitHub Actions workflows
│   └── workflows/
│       ├── ci.yml  # Continuous Integration
│       ├── cd.yml  # Continuous Delivery
│       └── aws-deploy.yml  # AWS Deployment
└── package.json    # Monorepo scripts
```

## Prerequisites

- Python 3.9+
- Node.js 14+
- npm or yarn
- React Native development environment

## Development Setup

### Backend Setup

1. Create and activate a virtual environment:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:

```bash
# For development (includes testing and linting tools)
pip3 install -r config/dev/requirements.txt

# For production
pip3 install -r config/prod/requirements.txt
```

3. Set up environment variables:

   - Copy `.env.example` to `.env`
   - Update the values in `.env` with your configuration

4. Run database migrations:

```bash
cd backend
alembic upgrade head
```

5. Start the development server:

```bash
# Using monorepo scripts
npm run backend:dev

# Or manually
cd backend
uvicorn app.main:app --reload
```

6. The API will be available at http://localhost:8000

### Code Quality Tools

The backend uses several tools to maintain code quality:

1. **Black** - Code formatting:

```bash
cd backend
black app tests
```

2. **isort** - Import sorting:

```bash
cd backend
isort app tests
```

3. **Flake8** - Linting:

```bash
cd backend
flake8 app tests
```

## Mobile Setup

1. Install dependencies:

```bash
# Using monorepo scripts
npm run mobile:install

# Or manually
cd mobile
npm install
```

2. Start the React Native development server:

```bash
# Using monorepo scripts
npm run mobile:start

# Or manually
cd mobile
npm run start
```

3. Run on iOS:

```bash
# Using monorepo scripts
npm run mobile:ios

# Or manually
cd mobile
npm run ios
```

4. Run on Android:

```bash
# Using monorepo scripts
npm run mobile:android

# Or manually
cd mobile
npm run android
```

## Testing

### Backend Tests

```bash
# Using monorepo scripts
npm run backend:test

# Or manually
cd backend
python3 -m pytest

# With coverage report
python3 -m pytest --cov=app --cov-report=xml
```

### Mobile Tests

```bash
# Using monorepo scripts
npm run mobile:test

# Or manually
cd mobile
npm test
```

## Environment-Specific Configurations

The backend supports three environments:

1. **Development (dev)**

   - Local development configuration
   - Includes development tools (pytest, black, flake8, isort)
   - Uses SQLite database by default
   - Configuration in `backend/config/dev/`

2. **Staging (gamma)**

   - Staging environment configuration
   - Uses production-like settings
   - Configuration in `backend/config/gamma/`

3. **Production (prod)**
   - Production environment configuration
   - Optimized for performance and security
   - Configuration in `backend/config/prod/`

Each environment has its own:

- `Dockerfile` - Container configuration
- `docker-compose.yml` - Service orchestration
- `requirements.txt` - Environment-specific dependencies

## API Documentation

Once the backend server is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Continuous Integration/Deployment

The project uses GitHub Actions for automation:

1. **CI Workflow** (`ci.yml`)

   - Runs tests
   - Performs code quality checks
   - Validates directory structure
   - Generates test coverage reports

2. **CD Workflow** (`cd.yml`)

   - Performs security scanning
   - Builds Docker images
   - Pushes to container registry
   - Supports multiple environments

3. **AWS Deploy** (`aws-deploy.yml`)
   - Deploys to AWS ECS
   - Environment-specific deployments
   - Includes health checks
   - Automated rollbacks on failure
