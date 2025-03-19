# LifeFlow Monorepo

This repository contains both the backend and mobile frontend for the LifeFlow application.

## Project Structure

```
lifeflow/
├── backend/           # FastAPI backend
│   ├── app/           # FastAPI application code
│   ├── config/
│   │   ├── dev/
│   │   │   ├── Dockerfile
│   │   │   ├── docker-compose.yml
│   │   │   └── requirements.txt
│   │   ├── gamma/
│   │   │   ├── Dockerfile
│   │   │   ├── docker-compose.yml
│   │   │   └── requirements.txt
│   │   └── prod/
│   │       ├── Dockerfile
│   │       ├── docker-compose.yml
│   │       └── requirements.txt
│   ├── tests/         # Backend tests
│   └── requirements.txt  # Base requirements for all environments
├── mobile/            # React Native frontend
│   ├── app/           # React Native components
│   ├── __tests__/     # Frontend tests
│   └── package.json
└── README.md
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
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:

```bash
# For development (includes testing and linting tools)
pip install -r config/dev/requirements.txt

# For production
pip install -r config/prod/requirements.txt
```

3. Run database migrations:

   ```
   cd backend
   alembic upgrade head
   ```

4. Start the development server:

   ```
   npm run backend:dev
   ```

   or manually:

   ```
   cd backend
   uvicorn app.main:app --reload
   ```

5. The API will be available at http://localhost:8000

## Mobile Setup

1. Install dependencies:

   ```
   npm run mobile:install
   ```

   or manually:

   ```
   cd mobile
   npm install
   ```

2. Start the React Native development server:

   ```
   npm run mobile:start
   ```

   or manually:

   ```
   cd mobile
   npm run start
   ```

3. Run on iOS:

   ```
   npm run mobile:ios
   ```

   or manually:

   ```
   cd mobile
   npm run ios
   ```

4. Run on Android:
   ```
   npm run mobile:android
   ```
   or manually:
   ```
   cd mobile
   npm run android
   ```

## Running Tests

### Backend Tests

```
npm run backend:test
```

or manually:

```
cd backend
pytest
```

### Mobile Tests

```
npm run mobile:test
```

or manually:

```
cd mobile
npm test
```

## API Documentation

Once the backend server is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
