from tests.conftest import client

def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "123tes1t123",
            "email": "123tes11t@example.com",
            "password": "test123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data == {'message': 'User registered!'}

def test_register_existing_user(client):
    payload = {
        "username": "test",
        "email": "test@example.com",
        "password": "test123"
    }

    client.post("/auth/register", json=payload)

    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] in [
        "User already exists.",
        "Email or username already exists."
    ]

def test_login_user(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "login",
            "email": "login@example.com",
            "password": "123pass123"
        }
    )

    response = client.post(
        "/auth/token",
        data={
            "username": "login",
            "password": "123pass123"
        }
    )
    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_wrong_login_user(client):
    payload = {
        "username": "login",
        "password": "pass123"
    }
    response = client.post("/auth/token", data=payload)
    assert response.status_code == 401
    assert response.json()["detail"] in ["Wrong username or password"]

def test_protected_endpoint_requires_auth(client):
    response = client.get("/films/show_movies")

    assert response.status_code == 401