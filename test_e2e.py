import pytest
import requests
import time


def urls(end):
    return "https://cryptic-garden-19358-66c5851b2ced.herokuapp.com/api/" + end


def auth():
    url = urls("users/token/")
    headers = {"Content-Type": "application/json"}
    data = {
        "username": "test@test",
        "password": "test",
    }
    response = requests.post(url, json=data, headers=headers)
    token = response.json().get("access")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def headers():
    return auth()


class TestBookAPI:
    @pytest.fixture
    def book_id(self, headers):
        url = urls("books/create/")
        headers = {"Content-Type": "application/json", **headers}
        data = {
            "title": "The Great Gatsby",
            "author": 1,
            "genre": "Classic",
            "publication_date": "1925-04-10",
            "price": 100,
            "quantity": 10,
        }
        response = requests.post(url, json=data, headers=headers)
        book_id = response.json()["id"]
        yield book_id
        url_delete = urls(f"books/delete/{book_id}/")
        requests.delete(url_delete, headers=headers)

    def test_create_book(self, headers):
        url = urls("books/create/")
        create_book_headers = {"Content-Type": "application/json", **headers}
        data = {
            "title": "The Great Gatsby",
            "author": 1,
            "genre": "Classic",
            "publication_date": "1925-04-10",
            "price": 100,
            "quantity": 10,
        }
        response = requests.post(url, json=data, headers=create_book_headers)
        assert response.status_code == 201
        assert "id" in response.json()
        assert response.json()["title"] == data["title"]
        assert response.json()["author"] == data["author"]
        assert response.json()["genre"] == data["genre"]
        assert response.json()["publication_date"] == data["publication_date"]
        assert response.json()["price"] == data["price"]
        assert response.json()["quantity"] == data["quantity"]

    def test_get_book_list(self):
        url = urls("books/")
        response = requests.get(url)
        assert response.status_code == 200
        assert len(response.json()) > 0

    def test_get_book_detail(self, headers, book_id):
        url = urls(f"books/{book_id}/")
        response = requests.get(url)
        assert response.status_code == 200
        assert response.json()["id"] == book_id

    def test_update_book(self, headers, book_id):
        url = urls(f"books/update/{book_id}/")
        headers = {"Content-Type": "application/json", **headers}
        data = {
            "title": "The Great",
            "author": 1,
            "genre": "drama",
            "publication_date": "1925-04-10",
            "price": 100,
            "quantity": 10,
        }
        response = requests.put(url, json=data, headers=headers)
        assert response.status_code == 200
        assert response.json()["title"] == data["title"]
        assert response.json()["author"] == data["author"]
        assert response.json()["genre"] == data["genre"]
        assert response.json()["publication_date"] == data["publication_date"]
        assert response.json()["price"] == data["price"]
        assert response.json()["quantity"] == data["quantity"]

    def test_delete_book(self, headers, book_id):
        url = urls(f"books/delete/{book_id}/")
        response = requests.delete(url, headers=headers)
        assert response.status_code == 204
        assert response.text == ""


class TestAuthorAPI:
    @pytest.fixture
    def author_id(self, headers):
        url = urls("authors/create/")
        create_author_headers = {"Content-Type": "application/json", **headers}
        data = {
            "name": f"F. Scott Fitzgerald",
        }
        response = requests.post(url, json=data, headers=create_author_headers)
        author_id = response.json().get("id")
        yield author_id
        url_delete = urls(f"authors/delete/{author_id}/")
        requests.delete(url_delete, headers=headers)

    def test_create_author(self, headers):
        url = urls("authors/create/")
        create_author_headers = {"Content-Type": "application/json", **headers}
        data = {
            "name": f"F. Scott Fitzgerald",
        }
        response = requests.post(url, json=data, headers=create_author_headers)
        assert response.status_code == 201
        assert "id" in response.json()
        assert response.json()["name"] == data["name"]

    def test_get_author_list(self, headers):
        url = urls("authors/")
        response = requests.get(url)
        assert response.status_code == 200
        assert len(response.json()) > 0

    def test_get_author_detail(self, headers, author_id):
        url = urls(f"authors/{author_id}/")
        response = requests.get(url)
        assert response.status_code == 200
        assert response.json()["id"] == author_id

    def test_update_author(self, headers, author_id):
        url = urls(f"authors/update/{author_id}/")
        update_author_headers = {"Content-Type": "application/json", **headers}
        data = {
            "name": "F. Scott",
        }
        response = requests.put(url, json=data, headers=update_author_headers)
        assert response.status_code == 200
        assert response.json()["name"] == data["name"]

    def test_delete_author(self, headers, author_id):
        url = urls(f"authors/delete/{author_id}/")
        response = requests.delete(url, headers=headers)
        assert response.status_code == 204
        assert response.text == ""


class TestUserAPI:
    def test_create_user(self):
        url = urls("users/register/")
        create_user_headers = {"Content-Type": "application/json"}
        data = {
            "username": f"test@user{int(time.time())}",
            "password": "test",
        }
        response = requests.post(url, json=data, headers=create_user_headers)
        assert response.status_code == 201
        assert response.json()["username"] == data["username"]

    def test_token(self):
        url = urls("users/token/")
        data = {
            "username": "test@user",
            "password": "test",
        }
        response = requests.post(url, json=data)
        assert response.status_code == 200
        assert "access" in response.json()
        assert "refresh" in response.json()


class TestOrderAPI:
    @pytest.fixture
    def book_id(self, headers):
        url = urls("books/create/")
        create_book_headers = {"Content-Type": "application/json", **headers}
        data = {
            "title": "The Great Gatsby",
            "author": 1,
            "genre": "drama",
            "publication_date": "1925-04-10",
            "price": 100,
            "quantity": 10,
        }
        response = requests.post(url, json=data, headers=create_book_headers)
        book_id = response.json().get("id")
        yield book_id
        url_delete = urls(f"books/delete/{book_id}/")
        requests.delete(url_delete, headers=headers)

    def test_create_order(self, headers, book_id):
        url = urls("order/")
        create_order_headers = {"Content-Type": "application/json"}
        data = {"order": [{"book_id": book_id, "quantity": 4}]}

        response = requests.post(url, json=data, headers=create_order_headers)
        assert response.status_code == 200
        assert "id" in response.json()
        assert "url" in response.json()

    def test_get_order_list(self, headers):
        url = urls("orders/")
        response = requests.get(url)
        assert response.status_code == 200
        assert len(response.json()) > 0
