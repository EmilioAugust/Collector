import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.database import Base, get_db
from environs import Env

env = Env()
env.read_env(".test.env")
url_database = env("URL_DB")
url_redis = env("URL_REDIS")

engine = create_engine(url_database)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers(client):
    payload = {
        "username": "testfixture",
        "email": "testfixture@example.com",
        "password": "testfixture1"
    }

    client.post('/auth/register', json=payload)
    response = client.post('/auth/token', data=payload)
    token = response.json()['access_token']
    return {"Authorization": f"Bearer {token}"}
