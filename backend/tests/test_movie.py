from tests.conftest import client

# testing movie adding
def test_add_movie(client, auth_headers):
    response = client.post(
        "/films/add_movies",
        json={
            "imdb_id": "tt0068646",
            "status": "Watched"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Movie added to your collection."}

def test_add_existing_movie(client, auth_headers):
    client.post(
        "/films/add_movies",
        json={
            "imdb_id": "tt0068646",
            "status": "Watched"
        },
        headers=auth_headers
    )

    response = client.post(
        "/films/add_movies",
        json={
            "imdb_id": "tt0068646",
            "status": "Watched"
        },
        headers=auth_headers
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "Movie already exists in collection."

def test_add_movie_without_login(client):
    response = client.post(
        "/films/add_movies",
        json={
            "imdb_id": "tt0068646",
            "status": "Watched"
        },
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

# testing showing movies
def test_movie_search_results(client, auth_headers):
    response = client.get(
        "/films/show_search_results",
        params={
            "query": "godfather",
        },
        headers=auth_headers
    )
    data = response.json()
    item = data[0]
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) > 0

    assert "Title" in item
    assert "Year" in item
    assert "imdbID" in item
    assert "Type" in item
    assert "Poster" in item

def test_showing_movies(client, auth_headers):
    client.post(
        "/films/add_movies",
        json={
            "imdb_id": "tt0068646",
            "status": "Watched"
        },
        headers=auth_headers
    )
    response = client.get(
        "/films/show_movies",
        headers=auth_headers
    )
    data = response.json()
    item = data[0]
    assert response.status_code == 200
    assert "id" in item
    assert "name" in item
    assert "description" in item
    assert "year" in item
    assert "imdb_rating" in item
    assert "poster" in item
    assert "status" in item

def test_showing_movies_empty(client, auth_headers):
    response = client.get(
        "/films/show_movies",
        headers=auth_headers
    )
    data = response.json()
    assert response.status_code == 200
    assert data.get("error") == 404
    assert data.get("detail") == "List of movies is empty"


def test_showing_movies_with_status(client, auth_headers):
    response = client.post(
        "/films/add_movies",
        json={
            "imdb_id": "tt0068646",
            "status": "Watched"
        },
        headers=auth_headers
    )

    response = client.get(
        "/films/show_movies_status",
        headers=auth_headers,
        params={"status": "Watched"}
    )
    data = response.json()
    item = data[0]
    assert response.status_code == 200
    assert "id" in item
    assert "name" in item
    assert "description" in item
    assert "year" in item
    assert "imdb_rating" in item
    assert "poster" in item
    assert "status" in item

# testing deleteing movies
def test_delete_movies(client, auth_headers):
    add_response = client.post(
        "/films/add_movies",
        json={
            "imdb_id": "tt0068646",
            "status": "Watched"
        },
        headers=auth_headers
    )
    assert add_response.status_code == 200
    assert add_response.json() == {"message": "Movie added to your collection."}

    movies_response = client.get(
        "/films/show_movies",
        headers=auth_headers
    )
    movies = movies_response.json()
    item = movies[0]
    assert movies_response.status_code == 200
    assert len(movies) == 1
    assert "id" in item

    response = client.delete(
        "/films/delete_movies",
        params={"id": item["id"]},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json() == {'message': 'Movie deleted.'}

def test_delete_movies_wrong_id(client, auth_headers):
    response = client.delete(
        "/films/delete_movies",
        params={"id": 5},
        headers=auth_headers
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Couldn't find this movie"

# testing updating status

def test_update_status(client, auth_headers):
    add_response = client.post(
        "/films/add_movies",
        json={
            "imdb_id": "tt0068646",
            "status": "Watched"
        },
        headers=auth_headers
    )
    assert add_response.status_code == 200
    assert add_response.json() == {"message": "Movie added to your collection."}

    movies_response = client.get(
        "/films/show_movies",
        headers=auth_headers
    )
    movies = movies_response.json()
    item = movies[0]
    assert movies_response.status_code == 200
    assert len(movies) == 1
    assert "id" in item

    response = client.put(
        "/films/update_movies_status",
        params={"id": item["id"], "status": "Watching"},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Movie status updated successfully"}

def test_update_status_wrong_id(client, auth_headers):
    response = client.put(
        "/films/update_movies_status",
        params={"id": 7, "status": "Watching"},
        headers=auth_headers
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found in your collection"