def test_health(client):
    response = client.get("/")
    assert response.status_code in (200, 404)