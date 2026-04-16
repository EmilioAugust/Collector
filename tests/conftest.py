import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import app
from app import Base, get_db
from environs import Env

env = Env()
env.read_env(".test.env")
url_database = env("TEST_URL_DB")
url_clean_database = env("TEST_URL_CLEAN_DB")

engine = create_engine(url_database)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

clean_engine = create_engine(url_clean_database)
CleanTestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=clean_engine)

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

# Normal Database
@pytest.fixture(scope="function")
def db():
    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

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

# Payloads

@pytest.fixture
def book_payload():
    payload = {
        "olib_id": "/works/OL82563W",
        "author": "J. K. Rowling",
        "title": "Harry Potter and the Philosopher's Stone",
        "cover": "OL22856696M",
        "status": "Read"
    }
    return payload

@pytest.fixture
def movie_payload():
    return {
            "imdb_id": "tt0068646",
            "status": "Watched"
        }

@pytest.fixture
def series_payload():
    return {
            "tvmaze_id": "169",
            "status": "Watched"
        }