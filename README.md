# LifeFlow

LifeFlow is a personal financial management application structured as a monorepo.

## Project Structure

- **backend/** - FastAPI backend application
  - **app/** - Application code
  - **config/** - Environment-specific configuration
  - **tests/** - Unit and integration tests
- **LifeFlowMobile/** - React Native mobile application
  - **app/** - Custom application components
  - **ios/** - iOS platform code
  - **android/** - Android platform code
- **scripts/** - Utility scripts for development and deployment

## Development Strategy

LifeFlow uses a **Docker-centric development approach**. All backend development and testing happens within containers to ensure consistency across environments and simplify onboarding.

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ and npm
- Python 3.11+ (for running local scripts)
- Xcode 14+ (for iOS development)
- Android Studio (for Android development)

### Backend Development Setup

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

3. Initialize the database:
   ```bash
   docker-compose exec api python -m app.init_db
   ```

The API will be available at http://localhost:8000 with documentation at http://localhost:8000/docs.

### Mobile Setup

1. Install dependencies:

   ```bash
   cd LifeFlowMobile
   npm install
   ```

2. For iOS, install CocoaPods dependencies:

   ```bash
   cd LifeFlowMobile/ios
   pod install
   ```

3. Start the mobile app (with backend running):

   ```bash
   cd LifeFlowMobile
   npm run start
   ```

4. In a separate terminal, launch the iOS app:
   ```bash
   cd LifeFlowMobile
   npm run ios
   ```

## Testing Strategy

LifeFlow uses multiple testing approaches to validate both functionality and the build process:

### Automated Tests

Run all automated tests with:

```bash
./scripts/run_tests.sh
```

This script runs:

1. Backend functional tests in a Docker container
2. API connectivity tests
3. Mobile app unit tests

### Component-Specific Tests

#### Backend Functional Tests

```bash
cd backend/config/dev
docker-compose -f docker-compose.test.yml up --build
```

#### Configuration Tests

```bash
cd backend
python -m pytest tests/test_config.py -v
```

#### API Connectivity Tests

```bash
cd scripts
node test_backend_frontend.js
```

#### Mobile Unit Tests

```bash
cd LifeFlowMobile
npm test
```

### Build Process Validation

The Docker build process is automatically validated when running:

```bash
cd backend/config/dev
docker-compose -f docker-compose.test.yml up --build
```

This test ensures:

- Docker container builds successfully
- Environment variables load correctly
- Database initializes properly
- Application can start and respond to requests

## Environment Configuration

LifeFlow uses environment-specific configuration files:

- Development: `backend/config/dev/.env`
- Gamma (Staging): `backend/config/gamma/.env`
- Production: `backend/config/prod/.env`
- Testing: `backend/config/dev/.env.test`

See `backend/config/README.md` for more details on environment setup.

## Deployment

### Development

```bash
cd backend/config/dev
docker-compose up -d
```

### Gamma/Staging

```bash
cd backend/config/gamma
cp .env.example .env
python ../../scripts/generate_key.py --env-file=.env
docker-compose up -d
```

### Production

```bash
cd backend/config/prod
cp .env.example .env
python ../../scripts/generate_key.py --env-file=.env
docker-compose up -d
```
