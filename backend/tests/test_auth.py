import pytest

@pytest.mark.parametrize("username, email, password, status_code, expected_result", [
    ("123tes1t123511", "123tes1123t6@example.com", "test123", 200, {'message': 'User registered!'}),
    ("123tes1t123511", "123tes1123t6@example.com", "test123", 400, {'detail': 'User already exists.'}),
])
def test_register_user(client, username, email, password, status_code, expected_result):
    response = client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password
        }
    )
    assert response.status_code == status_code
    assert response.json() == expected_result

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