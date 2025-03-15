# LifeFlow

A FastAPI-based financial transaction management system with Plaid integration.

## System Requirements

- Python 3.9+
- SQLite 3
- pip3

## Project Structure

```
LifeFlow/
├── app/
│   ├── api/
│   │   └── v1/           # API version 1 endpoints
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── routes/           # Route handlers
│   ├── core/            # Core functionality
│   └── database.py      # Database configuration
├── tests/               # Test suite
├── alembic/            # Database migrations
└── requirements.txt    # Project dependencies
```

## Setup Instructions

1. **Create and activate a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:

   ```bash
   pip3 install -r requirements.txt
   ```

3. **Environment Configuration**:
   Create a `.env` file in the project root:

   ```env
   # Database
   DATABASE_PATH=./lifeflow.db

   # Plaid API
   PLAID_CLIENT_ID=your_client_id
   PLAID_SECRET=your_secret
   PLAID_ENV=sandbox  # or development/production
   PLAID_REDIRECT_URI=http://localhost:3000/oauth-redirect

   # Security
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

4. **Initialize Database**:

   ```bash
   # Create database tables
   python3 -m app.init_db
   ```

5. **Run Development Server**:
   ```bash
   uvicorn app.main:app --reload
   ```

## Development Workflow

1. **Running Tests**:

   ```bash
   pytest -v                  # Run all tests
   pytest -v tests/test_*.py  # Run specific test file
   pytest -v -k "test_name"   # Run specific test
   ```

2. **API Documentation**:

   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. **Database Management**:

   ```bash
   # Create new migration
   alembic revision --autogenerate -m "description"

   # Apply migrations
   alembic upgrade head

   # Rollback migration
   alembic downgrade -1
   ```

## Deployment Steps

1. **Production Environment Setup**:

   ```bash
   # Install production dependencies
   pip3 install -r requirements.txt

   # Set production environment variables
   export DATABASE_PATH=/path/to/prod/db.sqlite
   export PLAID_ENV=production
   export PLAID_CLIENT_ID=prod_client_id
   export PLAID_SECRET=prod_secret
   ```

2. **Database Setup**:

   ```bash
   # Apply all migrations
   alembic upgrade head
   ```

3. **Running in Production**:
   ```bash
   # Using Gunicorn (recommended for production)
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

## Security Considerations

1. **API Authentication**:

   - All endpoints require JWT authentication
   - Tokens expire after 30 minutes
   - Use secure headers in production

2. **Database Security**:

   - Use proper file permissions for SQLite database
   - Regular backups recommended
   - Consider using PostgreSQL for production

3. **Plaid Integration**:
   - Store Plaid secrets securely
   - Use environment-specific API keys
   - Implement proper error handling

## Monitoring and Maintenance

1. **Logging**:

   - Application logs in `/var/log/lifeflow/`
   - Use structured logging format
   - Monitor for errors and exceptions

2. **Backups**:

   ```bash
   # Daily database backup
   sqlite3 $DATABASE_PATH ".backup '/path/to/backup/lifeflow_$(date +%Y%m%d).db'"
   ```

3. **Health Checks**:
   - Monitor `/health` endpoint
   - Set up alerts for system metrics
   - Regular security updates

## Common Issues and Solutions

1. **Database Initialization**:
   If tables are missing:

   ```bash
   python3 -m app.init_db
   ```

2. **Plaid Connection Issues**:

   - Verify API keys and environment
   - Check Plaid status page
   - Review error logs

3. **Performance Optimization**:
   - Index heavily queried fields
   - Implement caching where appropriate
   - Monitor query performance

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

[License Information]
