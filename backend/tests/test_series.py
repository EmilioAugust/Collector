from tests.conftest import client

# adding series
def test_adding_series(client, auth_headers):
    response = client.post(
        "/tv_shows/add_series",
        json={
            "tvmaze_id": "169",
            "status": "Watched"
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Series added to your collection."

def test_adding_existing_series(client, auth_headers):
    client.post(
        "/tv_shows/add_series",
        json={
            "tvmaze_id": "169",
            "status": "Watched"
        },
        headers=auth_headers
    )

    response = client.post(
        "/tv_shows/add_series",
        json={
            "tvmaze_id": "169",
            "status": "Watched"
        },
        headers=auth_headers
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Series already exists in collection."

def test_adding_series_without_login(client):
    response = client.post(
        "/tv_shows/add_series",
        json={
            "tvmaze_id": "169",
            "status": "Watched"
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


# testing showing series
def test_showing_series_results(client, auth_headers):
    response = client.get(
        "/tv_shows/show_search_results",
        params={"query": "breaking bad"},
        headers=auth_headers
    )
    data = response.json()
    item = data[0]
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) > 0

    assert "tvmaze_id" in item
    assert "name" in item
    assert "description" in item
    assert "poster" in item
    assert "premiered" in item
    assert "ended" in item

def test_showing_series(client, auth_headers):
    client.post(
        "/tv_shows/add_series",
        json={
            "tvmaze_id": "169",
            "status": "Watching"
        },
        headers=auth_headers
    )

    response = client.get(
        "/tv_shows/show_series",
        headers=auth_headers
    )

    data = response.json()
    item = data[0]
    assert response.status_code == 200
    assert "id" in item
    assert "name" in item
    assert "premiered" in item
    assert "ended" in item
    assert "description" in item
    assert "season_amount" in item
    assert "poster" in item
    assert "imdb_rating" in item
    assert "status" in item

def test_showing_series_empty(client, auth_headers):
    response = client.get(
        "/tv_shows/show_series",
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["error"] == 404
    assert response.json()["detail"] == "List of series is empty"

def test_showing_series_with_status(client, auth_headers):
    client.post(
        "/tv_shows/add_series",
        json={
            "tvmaze_id": "169",
            "status": "Watching"
        },
        headers=auth_headers
    )

    response = client.get(
        "/tv_shows/show_series_status",
        params={"status": "Watching"},
        headers=auth_headers
    )

    data = response.json()
    item = data[0]
    assert response.status_code == 200
    assert "id" in item
    assert "name" in item
    assert "premiered" in item
    assert "ended" in item
    assert "description" in item
    assert "season_amount" in item
    assert "poster" in item
    assert "imdb_rating" in item
    assert "status" in item

#testing deleting series
def test_delete_series(client, auth_headers):
    add_response = client.post(
        "/tv_shows/add_series",
        json={
            "tvmaze_id": "169",
            "status": "Watching"
        },
        headers=auth_headers
    )

    assert add_response.status_code == 200
    assert add_response.json()["message"] == "Series added to your collection."

    series_response = client.get(
        "/tv_shows/show_series_status",
        params={"status": "Watching"},
        headers=auth_headers
    )
    series = series_response.json()
    item = series[0]
    assert series_response.status_code == 200
    assert len(series) == 1
    assert "id" in item

    response = client.delete(
        "/tv_shows/delete_series",
        params={"id": item["id"]},
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json() == {'message': 'Series deleted.'}

def test_delete_series_wrong_id(client, auth_headers):
    response = client.delete(
        "/tv_shows/delete_series",
        params={"id": 5},
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Couldn't find this series"

#testing update status
def test_update_status(client, auth_headers):
    add_response = client.post(
        "/tv_shows/add_series",
        json={
            "tvmaze_id": "169",
            "status": "Watching"
        },
        headers=auth_headers
    )

    series_response = client.get(
        "/tv_shows/show_series",
        headers=auth_headers
    )

    series = series_response.json()
    item = series[0]
    assert series_response.status_code == 200
    assert len(series) == 1
    assert "id" in item

    response = client.put(
        "/tv_shows/update_series_status",
        params={"id": item['id'], "status": "Watched"},
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Series status updated successfully"}


def test_update_status_wrong_id(client, auth_headers):
    response = client.put(
        "/tv_shows/update_series_status",
        params={"id": 5, "status": "Watched"},
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Series not found in your collection"