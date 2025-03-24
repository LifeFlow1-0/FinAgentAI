# LifeFlow Environment Configuration

This directory contains environment-specific configuration for the LifeFlow backend application.

## Environment Structure

LifeFlow uses a Docker-based workflow with environment-specific configuration files:

- **Development**: For local development with hot-reloading (`/config/dev/`)
- **Gamma**: For staging/testing deployment (`/config/gamma/`)
- **Production**: For production deployment (`/config/prod/`)

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

## Running Tests

To run tests in a Docker container:

```bash
cd backend/config/dev
docker-compose -f docker-compose.test.yml up --build
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

- **Development**: Database stored at project root
- **Gamma/Production**: Database stored in a Docker volume at `/app/data/`

This approach was chosen for simplicity and easy data portability.
