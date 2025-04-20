from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models.user import User
from app.models.transaction import Transaction
from app.models.plaid import PlaidItem, PlaidAccount
from app.models.personality import PersonalityProfile
from app.models.onboarding_session import OnboardingSession

# Make sure all models are registered with Base.metadata
_ = [User.__table__, Transaction.__table__, PlaidItem.__table__, 
     PlaidAccount.__table__, PersonalityProfile.__table__, OnboardingSession.__table__]

SQLALCHEMY_DATABASE_URL = "sqlite://"

@pytest.fixture
def test_db():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    # Debug: Print out all tables
    inspector = inspect(engine)
    print("\nTables in database:", inspector.get_table_names())

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    yield TestClient(app)

def test_create_and_fetch_session(client):
    r = client.post("/api/v1/session")
    assert r.status_code == 201
    sid = r.json()["id"]

    r2 = client.get(f"/api/v1/session/{sid}")
    assert r2.status_code == 200
    assert r2.json()["id"] == sid 