import pytest

# testing adding books
@pytest.mark.parametrize(("olib_id, author, title, cover, status, status_code, expected_result"), [
    ("/works/OL82563W",
     "J. K. Rowling",
     "Harry Potter and the Philosopher's Stone",
     "OL22856696M",
     "Read",
     200,
     {"message": "Book added to your collection."}),
     
     ("/works/OL82563W",
     "J. K. Rowling",
     "Harry Potter and the Philosopher's Stone",
     "OL22856696M",
     "Read",
     409,
     {"detail": "Book already exists in collection."})
])
@pytest.mark.slow
def test_adding_books(client, auth_headers, olib_id, author, title, cover, status, status_code, expected_result):
    response = client.post(
        "/books/add_books",
        json={
            "olib_id": olib_id,
            "author": author,
            "title": title,
            "cover": cover,
            "status": status
        },
        headers=auth_headers
    )
    assert response.status_code == status_code
    assert response.json() == expected_result

def test_adding_book_without_login(client, book_payload):
    response = client.post(
        "/books/add_books",
        json=book_payload,
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

#test showing books
def test_showing_books_search_results(client, auth_headers):
    response = client.get(
        "/books/show_search_results_book",
        params={"query": "harry potter"},
        headers=auth_headers
    )

    data = response.json()
    item = data[0]
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) > 0

    assert "author" in item
    assert "cover" in item
    assert "olib_id" in item
    assert "title" in item

    
def test_showing_books(client, auth_headers, book_payload):
    response = client.get(
        "/books/show_books",
        headers=auth_headers
    )

    data = response.json()
    item = data[0]
    assert response.status_code == 200
    assert "id" in item
    assert "author" in item
    assert "title" in item
    assert "description" in item
    assert "cover" in item
    assert "status" in item

def test_showing_books_with_status(client, auth_headers, book_payload):
    response = client.get(
        "/books/show_books_status",
        params={"status": "Read"},
        headers=auth_headers
    )

    data = response.json()
    item = data[0]
    assert response.status_code == 200
    assert "id" in item
    assert "author" in item
    assert "title" in item
    assert "description" in item
    assert "cover" in item
    assert "status" in item

#testing deleting books
def test_deleting_books(client, auth_headers, book_payload):
    response = client.get(
        "/books/show_books",
        headers=auth_headers
    )

    data = response.json()
    item = data[0]
    assert response.status_code == 200
    assert "id" in item

    delete_response = client.delete(
        "/books/delete_books",
        params={"id": item["id"]},
        headers=auth_headers
    )

    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Book deleted."}

def test_delete_book_wrong_id(client, auth_headers):
    response = client.delete(
        "/books/delete_books",
        params={"id": 3},
        headers=auth_headers
    )
    assert response.status_code == 404
    assert response.json()['detail'] == "Couldn't find book"


#testing update status
def test_update_status(client, auth_headers, book_payload):
    response = client.post(
        "/books/add_books",
        json=book_payload,
        headers=auth_headers
    )

    book_response = client.get(
        "/books/show_books",
        headers=auth_headers
    )

    data = book_response.json()
    item = data[0]
    assert book_response.status_code == 200
    assert "id" in item

    response = client.put(
        "/books/update_books_status",
        params={"id": item["id"], "status": "Reading"},
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Book status updated successfully"}

def test_update_status_wrong_id(client, auth_headers):
    response = client.put(
        "/books/update_books_status",
        params={"id": 3, "status": "Reading"},
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found in your collection"

def test_showing_books_empty(client, auth_headers):
    response = client.get(
        "/books/show_books",
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["error"] == 404
    assert response.json()["detail"] == "List of books is empty"