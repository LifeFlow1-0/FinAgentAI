from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import all models here so that Base has them before being imported by Alembic 