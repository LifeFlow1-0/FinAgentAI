# LifeFlow

LifeFlow is a personal financial management application.

## Project Structure

- **backend/** - FastAPI backend application
  - **app/** - Application code
  - **config/** - Environment-specific configuration
  - **tests/** - Unit and integration tests
- **mobile/** - React Native mobile application
- **scripts/** - Utility scripts for development and deployment

## Development Setup

LifeFlow uses Docker for development to ensure consistency across environments.

### Prerequisites

- Docker and Docker Compose
- Node.js 16+ and npm
- Python 3.11+ (for running local scripts)

### Backend Setup

1. Set up development environment:

   ```bash
   cd backend/config/dev
   cp .env.example .env
   python ../../scripts/generate_key.py --env-file=.env
   ```

2. Start the development container:
   ```bash
   docker-compose up -d
   ```

The API will be available at http://localhost:8000 with documentation at http://localhost:8000/docs.

### Mobile Setup

1. Install dependencies:

   ```bash
   cd mobile
   npm install
   ```

2. Start the mobile app (with backend running):
   ```bash
   npm run ios
   ```

## Testing

Run all tests with:

```bash
./scripts/run_tests.sh
```

Or run specific tests:

```bash
cd backend/config/dev
docker-compose -f docker-compose.test.yml up --build
```

## Environment Configuration

LifeFlow uses environment-specific configuration files:

- Development: `backend/config/dev/.env`
- Gamma (Staging): `backend/config/gamma/.env`
- Production: `backend/config/prod/.env`
- Testing: `backend/config/dev/.env.test`

See `backend/config/README.md` for more details on environment setup.
