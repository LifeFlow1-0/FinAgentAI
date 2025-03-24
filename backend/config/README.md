# LifeFlow Environment Configuration

This directory contains environment-specific configuration for the LifeFlow backend application.

## Docker-Centric Development Approach

LifeFlow has adopted a Docker-centric development model where:

1. **Local Development Happens in Containers**: All backend development occurs within Docker containers, eliminating "works on my machine" issues.

2. **Environment Parity**: Development, testing, and production environments use the same Docker configuration with environment-specific settings.

3. **Simplified Onboarding**: New developers only need Docker installed to get started, reducing setup complexity.

4. **Consistent Testing**: All tests run in containers that match the production environment.

## Environment Structure

LifeFlow uses a Docker-based workflow with environment-specific configuration files:

- **Development** (`/config/dev/`): For local development with hot-reloading
- **Gamma** (`/config/gamma/`): For staging/testing deployment
- **Production** (`/config/prod/`): For production deployment
- **Testing** (`/config/dev/test`): For running automated tests

Each environment directory contains:

- `Dockerfile` - Environment-specific container configuration
- `docker-compose.yml` - Container orchestration for the environment
- `.env.example` - Template for environment variables (committed to Git)
- `.env` - Actual environment variables with secrets (not committed to Git)

## Setting Up a New Environment

1. Copy the `.env.example` file to `.env` in the same directory:

   ```bash
   cp config/dev/.env.example config/dev/.env
   ```

2. Generate a new encryption key:

   ```bash
   python scripts/generate_key.py --env-file=backend/config/dev/.env
   ```

3. Update other values in the `.env` file as needed.

4. Start the environment:

   ```bash
   cd backend/config/dev
   docker-compose up -d
   ```

5. Initialize the database:
   ```bash
   docker-compose exec api python -m app.init_db
   ```

## Running Tests

LifeFlow includes multiple test suites to validate both functionality and the Docker build process:

### Building and Testing in Docker

To validate the Docker build and run all backend tests:

```bash
cd backend/config/dev
docker-compose -f docker-compose.test.yml up --build
```

This process validates:

- The Docker image builds successfully
- Environment variables are loaded correctly
- The database initializes properly
- All backend functionality works in a container

### Running Specific Test Categories

#### Configuration Tests

```bash
docker-compose exec api python -m pytest tests/test_config.py -v
```

#### Personality API Tests

```bash
docker-compose exec api python -m pytest tests/test_personality_api.py -v
```

#### Plaid Integration Tests

```bash
docker-compose exec api python -m pytest tests/api/v1/test_plaid.py -v
```

#### Transaction Tests

```bash
docker-compose exec api python -m pytest tests/test_transactions.py -v
```

### Connectivity Tests

We include tests to verify communication between system components:

```bash
cd /path/to/LifeFlow/scripts
node test_backend_frontend.js
node test_mobile_integration.js
```

## Environment Variables

Key environment variables include:

- `DATABASE_PATH` - Path to the SQLite database
- `PLAID_CLIENT_ID`, `PLAID_SECRET`, `PLAID_ENV` - Plaid API credentials
- `ENCRYPTION_KEY` - Key for encrypting sensitive data
- `DEBUG` - Boolean flag for development features

See the `.env.example` files for all available options.

## Database Strategy

LifeFlow uses SQLite for all environments:

- **Development**: Database stored in a Docker volume mapped to the host
- **Gamma/Production**: Database stored in a Docker volume at `/app/data/`

This approach was chosen for simplicity and easy data portability.

## Environment Promotion

Changes typically flow through environments in this order:

1. **Development**: For initial development and local testing
2. **Testing**: For automated tests and CI/CD validation
3. **Gamma**: For pre-production/staging validation
4. **Production**: For user-facing deployment

Each promotion maintains the same Docker configuration but uses different environment files.
